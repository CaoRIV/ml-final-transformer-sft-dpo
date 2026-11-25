"""Vòng huấn luyện A.2 có checkpoint theo epoch và tiếp tục xác định được."""

from __future__ import annotations

import ast
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import random
import re
import subprocess
import sys
import tempfile
from typing import Any, Mapping

import torch
from torch import Tensor
from torch.nn import functional as F

from .char_lm import CharacterLM, validation_metrics


_CHECKPOINT_VERSION = 1
_CHECKPOINT_NAME = re.compile(r"checkpoint_epoch_(\d{4,})\.pt$")
_REQUIRED_CONFIG = frozenset({"d_model", "n_heads", "d_ff", "n_layers", "epochs", "batch_size", "lr"})


def _normalize_config(config: Mapping[str, Any]) -> dict[str, int | float]:
    if not isinstance(config, dict) or set(config) != _REQUIRED_CONFIG:
        raise ValueError(f"config phải là dict đúng các khóa: {sorted(_REQUIRED_CONFIG)}")

    normalized: dict[str, int | float] = {}
    for key in ("d_model", "n_heads", "d_ff", "n_layers", "epochs", "batch_size"):
        value = config[key]
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError(f"config[{key!r}] phải là số nguyên dương")
        normalized[key] = value

    lr = config["lr"]
    if isinstance(lr, bool) or not isinstance(lr, (int, float)) or not math.isfinite(lr) or lr <= 0:
        raise ValueError("config['lr'] phải là số thực dương hữu hạn")
    normalized["lr"] = float(lr)
    if normalized["d_model"] % normalized["n_heads"]:
        raise ValueError("d_model phải chia hết cho n_heads")
    return normalized


def _validate_vocab(token_to_id: Mapping[str, int]) -> dict[str, int]:
    if not isinstance(token_to_id, dict) or len(token_to_id) < 2:
        raise ValueError("token_to_id phải là dict có ít nhất hai token")
    vocab: dict[str, int] = {}
    for token, index in token_to_id.items():
        if not isinstance(token, str) or isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("token_to_id phải ánh xạ chuỗi sang số nguyên")
        vocab[token] = index
    if set(vocab.values()) != set(range(len(vocab))):
        raise ValueError("ID trong token_to_id phải liên tiếp từ 0 đến V-1")
    return vocab


def _validate_windows(windows: Tensor, name: str, vocab_size: int) -> None:
    if not isinstance(windows, Tensor) or windows.dtype != torch.long or windows.device.type != "cpu":
        raise ValueError(f"{name} phải là LongTensor trên CPU")
    if windows.ndim != 2 or windows.size(0) < 1 or windows.size(1) < 2:
        raise ValueError(f"{name} phải có dạng [N,T+1], với N >= 1 và T >= 1")
    minimum, maximum = torch.aminmax(windows)
    if minimum.item() < 0 or maximum.item() >= vocab_size:
        raise ValueError(f"ID token trong {name} nằm ngoài token_to_id")


def _tensor_fingerprint(tensor: Tensor) -> str:
    """Băm byte tensor mà không phụ thuộc NumPy hoặc layout storage ban đầu."""
    raw = tensor.contiguous().view(torch.uint8).flatten().tolist()
    digest = hashlib.sha256(bytes(raw)).hexdigest()
    return f"sha256:{digest}"


def _source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_revision(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip()


def _provenance(device: torch.device) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    sources = {
        "src/char_lm.py": _source_hash(Path(__file__).with_name("char_lm.py")),
        "src/char_lm_train.py": _source_hash(Path(__file__)),
        "git_revision": _git_revision(root),
    }
    encoded = json.dumps(sources, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
    return {
        "source_fingerprint": f"sha256:{hashlib.sha256(encoded).hexdigest()}",
        "sources": sources,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "torch": str(torch.__version__),
            "torch_cuda": None if torch.version.cuda is None else str(torch.version.cuda),
            "device": str(device),
        },
    }


def _metadata(
    train: Tensor,
    validation: Tensor,
    token_to_id: dict[str, int],
    data_id: str,
    config: dict[str, int | float],
    device: torch.device,
) -> dict[str, Any]:
    provenance = _provenance(device)
    return {
        "data": {
            "data_id": data_id,
            "train_shape": list(train.shape),
            "train_fingerprint": _tensor_fingerprint(train),
            "validation_shape": list(validation.shape),
            "validation_fingerprint": _tensor_fingerprint(validation),
        },
        "token_to_id": token_to_id,
        "config": config,
        "context_length": train.size(1) - 1,
        "source_fingerprint": provenance["source_fingerprint"],
        "provenance": provenance,
    }


def _cpu_copy(value: Any) -> Any:
    if isinstance(value, Tensor):
        return value.detach().cpu().clone()
    if isinstance(value, dict):
        return {key: _cpu_copy(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_cpu_copy(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_cpu_copy(item) for item in value)
    return value


def _rng_snapshot(device: torch.device, shuffle_generator: torch.Generator) -> dict[str, Any]:
    snapshot: dict[str, Any] = {
        "python": repr(random.getstate()),
        "torch_cpu": torch.get_rng_state().cpu().clone(),
        "shuffle": shuffle_generator.get_state().cpu().clone(),
    }
    if device.type == "cuda":
        snapshot["torch_cuda"] = [state.cpu().clone() for state in torch.cuda.get_rng_state_all()]
    return snapshot


def _restore_rng(snapshot: Any, device: torch.device, shuffle_generator: torch.Generator) -> None:
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("python"), str):
        raise ValueError("Checkpoint có trạng thái RNG không hợp lệ")
    try:
        python_state = ast.literal_eval(snapshot["python"])
    except (SyntaxError, ValueError) as error:
        raise ValueError("Checkpoint có trạng thái RNG Python không hợp lệ") from error
    torch_state = snapshot.get("torch_cpu")
    shuffle_state = snapshot.get("shuffle")
    if not isinstance(torch_state, Tensor) or not isinstance(shuffle_state, Tensor):
        raise ValueError("Checkpoint thiếu trạng thái RNG PyTorch")
    random.setstate(python_state)
    torch.set_rng_state(torch_state.cpu())
    shuffle_generator.set_state(shuffle_state.cpu())
    if device.type == "cuda" and "torch_cuda" in snapshot:
        cuda_states = snapshot["torch_cuda"]
        if not isinstance(cuda_states, list) or not all(isinstance(state, Tensor) for state in cuda_states):
            raise ValueError("Checkpoint có trạng thái CUDA RNG không hợp lệ")
        torch.cuda.set_rng_state_all([state.cpu() for state in cuda_states])


def _checkpoint_paths(run_dir: Path) -> list[tuple[int, Path]]:
    checkpoints: list[tuple[int, Path]] = []
    for candidate in run_dir.iterdir():
        match = _CHECKPOINT_NAME.fullmatch(candidate.name)
        if match is not None:
            checkpoints.append((int(match.group(1)), candidate))
    return sorted(checkpoints)


def _load_checkpoint(path: Path, run_dir: Path) -> dict[str, Any]:
    if path.is_symlink() or path.resolve().parent != run_dir.resolve():
        raise ValueError("Từ chối checkpoint ngoài run_dir hoặc symbolic link")
    try:
        checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    except TypeError as error:
        raise RuntimeError("PyTorch hiện tại phải hỗ trợ torch.load(..., weights_only=True)") from error
    if not isinstance(checkpoint, dict):
        raise ValueError("Checkpoint không có dạng dict tin cậy")
    return checkpoint


def _save_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    """Ghi tệp tạm cùng thư mục rồi thay tên; không ghi đè checkpoint đã có."""
    if path.exists():
        raise FileExistsError(f"Từ chối ghi đè checkpoint: {path}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            torch.save(checkpoint, handle)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            raise FileExistsError(f"Từ chối ghi đè checkpoint: {path}")
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _make_checkpoint(
    model: CharacterLM,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    step: int,
    seed: int,
    metadata: dict[str, Any],
    metrics: dict[str, float | int],
    device: torch.device,
    shuffle_generator: torch.Generator,
) -> dict[str, Any]:
    return {
        "format_version": _CHECKPOINT_VERSION,
        "epoch": epoch,
        "step": step,
        "seed": seed,
        "model_state": _cpu_copy(model.state_dict()),
        "optimizer_state": _cpu_copy(optimizer.state_dict()),
        "rng": _rng_snapshot(device, shuffle_generator),
        "metadata": metadata,
        "metrics": dict(metrics),
    }


def _check_resume_compatibility(checkpoint: dict[str, Any], metadata: dict[str, Any], seed: int) -> None:
    if checkpoint.get("format_version") != _CHECKPOINT_VERSION:
        raise ValueError("Phiên bản checkpoint không tương thích")
    if checkpoint.get("seed") != seed:
        raise ValueError("Seed không khớp checkpoint")
    saved_metadata = checkpoint.get("metadata")
    if not isinstance(saved_metadata, dict):
        raise ValueError("Checkpoint thiếu metadata")
    for key in ("data", "token_to_id", "config", "context_length", "source_fingerprint"):
        if saved_metadata.get(key) != metadata[key]:
            raise ValueError(f"Checkpoint không tương thích ở metadata.{key}")
    if not isinstance(checkpoint.get("epoch"), int) or checkpoint["epoch"] < 0:
        raise ValueError("Checkpoint có epoch không hợp lệ")
    if not isinstance(checkpoint.get("step"), int) or checkpoint["step"] < 0:
        raise ValueError("Checkpoint có step không hợp lệ")
    if not isinstance(checkpoint.get("model_state"), dict) or not isinstance(checkpoint.get("optimizer_state"), dict):
        raise ValueError("Checkpoint thiếu trạng thái model hoặc optimizer")
    if not isinstance(checkpoint.get("rng"), dict):
        raise ValueError("Checkpoint thiếu trạng thái RNG")
    if not isinstance(checkpoint.get("metrics"), dict):
        raise ValueError("Checkpoint thiếu validation metrics")


def _completed_result(checkpoint: dict[str, Any], seed: int) -> dict[str, float | int]:
    metrics = checkpoint["metrics"]
    required = ("validation_nll", "validation_ppl", "validation_tokens")
    if any(key not in metrics for key in required):
        raise ValueError("Checkpoint thiếu validation metrics")
    return {**metrics, "seed": seed}


def run_seed(
    train: Tensor,
    validation: Tensor,
    token_to_id: dict[str, int],
    data_id: str,
    config: dict[str, Any],
    seed: int,
    run_dir: Path,
    device: torch.device,
    resume: bool = False,
) -> dict[str, float | int]:
    """Huấn luyện một seed và lưu checkpoint hoàn tất từng epoch.

    `run_dir` mới là bắt buộc khi chạy mới. Với `resume=True`, thư mục chưa có
    hoặc trống được khởi động lại an toàn; thư mục có nội dung khác phải có
    checkpoint hợp lệ. Chỉ validation được đánh giá sau mỗi epoch và checkpoint
    giữ kết quả đó.
    """
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed < 2**63:
        raise ValueError("seed phải là số nguyên trong [0, 2**63)")
    if not isinstance(data_id, str) or not data_id:
        raise ValueError("data_id phải là chuỗi không rỗng")
    if not isinstance(run_dir, Path):
        raise TypeError("run_dir phải là pathlib.Path")
    if not isinstance(device, torch.device):
        raise TypeError("device phải là torch.device")

    normalized_config = _normalize_config(config)
    vocab = _validate_vocab(token_to_id)
    _validate_windows(train, "train", len(vocab))
    _validate_windows(validation, "validation", len(vocab))
    if train.size(1) != validation.size(1):
        raise ValueError("train và validation phải có cùng T+1")
    metadata = _metadata(train, validation, vocab, data_id, normalized_config, device)

    checkpoint: dict[str, Any] | None = None
    if resume:
        if run_dir.exists():
            if not run_dir.is_dir():
                raise ValueError("run_dir resume phải là thư mục")
            checkpoints = _checkpoint_paths(run_dir)
            if not checkpoints:
                if any(run_dir.iterdir()):
                    raise FileNotFoundError("run_dir resume có nội dung nhưng không có checkpoint")
            else:
                named_epoch, checkpoint_path = checkpoints[-1]
                checkpoint = _load_checkpoint(checkpoint_path, run_dir)
                _check_resume_compatibility(checkpoint, metadata, seed)
                if checkpoint["epoch"] != named_epoch:
                    raise ValueError("Tên checkpoint không khớp epoch đã lưu")
        else:
            run_dir.mkdir(parents=True)
    else:
        if run_dir.exists():
            raise FileExistsError("run_dir đã tồn tại; dùng resume=True để tiếp tục")
        run_dir.mkdir(parents=True)

    if checkpoint is not None and checkpoint["epoch"] > normalized_config["epochs"]:
        raise ValueError("Checkpoint có epoch vượt config['epochs']")
    if checkpoint is not None and checkpoint["epoch"] == normalized_config["epochs"]:
        return _completed_result(checkpoint, seed)

    if checkpoint is None:
        random.seed(seed)
        torch.manual_seed(seed)
        if device.type == "cuda":
            torch.cuda.manual_seed_all(seed)
        shuffle_generator = torch.Generator().manual_seed(seed)
        completed_epoch = 0
        step = 0
    else:
        shuffle_generator = torch.Generator()
        completed_epoch = checkpoint["epoch"]
        step = checkpoint["step"]

    model = CharacterLM(
        len(vocab), train.size(1) - 1, normalized_config["d_model"],
        normalized_config["n_heads"], normalized_config["d_ff"], normalized_config["n_layers"],
    ).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=normalized_config["lr"])

    if checkpoint is not None:
        try:
            model.load_state_dict(checkpoint["model_state"])
            optimizer.load_state_dict(checkpoint["optimizer_state"])
        except (KeyError, RuntimeError, ValueError) as error:
            raise ValueError("Checkpoint không khớp trạng thái model/optimizer") from error
        _restore_rng(checkpoint["rng"], device, shuffle_generator)

    model.train()
    for epoch in range(completed_epoch + 1, normalized_config["epochs"] + 1):
        order = torch.randperm(train.size(0), generator=shuffle_generator)
        for start in range(0, train.size(0), normalized_config["batch_size"]):
            indices = order[start:start + normalized_config["batch_size"]]
            batch = train.index_select(0, indices).to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(batch[:, :-1])
            loss = F.cross_entropy(logits.flatten(0, 1), batch[:, 1:].reshape(-1))
            loss.backward()
            optimizer.step()
            step += 1

        metrics = validation_metrics(model, validation, normalized_config["batch_size"], device)
        checkpoint_path = run_dir / f"checkpoint_epoch_{epoch:04d}.pt"
        _save_checkpoint(
            checkpoint_path,
            _make_checkpoint(model, optimizer, epoch, step, seed, metadata, metrics, device, shuffle_generator),
        )

    return {**metrics, "seed": seed}
