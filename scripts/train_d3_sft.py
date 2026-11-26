"""D.3 SFT QLoRA trainer for the verified D2 release.

Example:
    python scripts/train_d3_sft.py --release PATH --output PATH --seed 41 \
      --rank 8 --alpha 16 --lr 0.0001 --epochs 1 --max-length 512

Use ``--check-only`` to validate a release before a GPU/package/model-download gate.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import random
import shutil
import sys
import tempfile
import time
from typing import Any, Iterable, Mapping

# Make ``python scripts/train_d3_sft.py`` resolve the repository namespace package.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.d3_data import load_release

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
MODEL_REVISION = "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
REQUIRED_VERSIONS = {
    "transformers": "4.57.6",
    "peft": "0.18.0",
    "accelerate": "1.12.0",
    "bitsandbytes": "0.48.2",
}
FORMAT_VERSION = 1


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stable_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(_stable_json(value))
    os.replace(temporary, path)


def _tree_hashes(directory: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            files[path.relative_to(directory).as_posix()] = _sha256_file(path)
    return files


def _atomic_directory(target: Path, populate) -> None:
    """Publish a fully populated directory, never a partial checkpoint."""
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{target.name}.tmp-", dir=target.parent))
    try:
        populate(staging)
        if target.exists():
            raise FileExistsError(f"Không ghi đè checkpoint/artifact đã tồn tại: {target}")
        os.replace(staging, target)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def _validate_release(release: Path) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    manifest, splits = load_release(release)
    if not isinstance(manifest, dict):
        raise ValueError("load_release phải trả về manifest dict")
    if not isinstance(splits, dict) or set(splits) != {"train", "validation"}:
        raise ValueError("Release chỉ được có hai split train và validation; USER_TEST không được phép dùng")
    for split_name in ("train", "validation"):
        rows = splits[split_name]
        if not isinstance(rows, list) or not rows:
            raise ValueError(f"Split {split_name} phải là list QA không rỗng")
        if not all(isinstance(row, dict) for row in rows):
            raise ValueError(f"Split {split_name} chứa bản ghi không phải object")
    return manifest, splits

def _release_manifest_hash(release: Path, manifest: Mapping[str, Any]) -> str:
    """Fingerprint the exact release-manifest file bytes accepted by d3_data."""
    del manifest
    return _sha256_file(release / "manifest.json")




def _check_report(release: Path, manifest: Mapping[str, Any], splits: Mapping[str, list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "check": "release-valid",
        "release": str(release.resolve()),
        "manifest_sha256": _release_manifest_hash(release, manifest),
        "split_rows": {name: len(splits[name]) for name in ("train", "validation")},
        "model": {"id": MODEL_ID, "revision": MODEL_REVISION},
        "training_dependencies_not_imported": True,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", required=True, type=Path, help="Thư mục release D2 tối giản đã được duyệt")
    parser.add_argument("--output", type=Path, help="Thư mục artifact SFT mới hoặc run đang resume")
    parser.add_argument("--seed", type=int, default=41)
    parser.add_argument("--rank", type=int, default=8, help="LoRA rank")
    parser.add_argument("--alpha", type=int, default=16, help="LoRA alpha")
    parser.add_argument("--lr", type=float, default=0.0001)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--resume", type=Path, help="Checkpoint epoch-* hoặc output run chứa checkpoints")
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--stop-after-epoch", type=int, help="Dừng có chủ ý sau epoch này để kiểm smoke resume")
    parser.add_argument("--check-only", action="store_true", help="Chỉ kiểm release; không import torch/HF hay tải model")
    args = parser.parse_args()
    if args.output is None and not args.check_only:
        parser.error("--output là bắt buộc khi không dùng --check-only")
    if args.rank <= 0 or args.alpha <= 0 or args.epochs <= 0 or args.max_length <= 1 or args.batch_size <= 0:
        parser.error("rank, alpha, epochs, max-length và batch-size phải dương; max-length >= 2")
    if args.stop_after_epoch is not None and not 1 <= args.stop_after_epoch <= args.epochs:
        parser.error("stop-after-epoch phải nằm trong [1, epochs]")
    if not math.isfinite(args.lr) or args.lr <= 0:
        parser.error("lr phải hữu hạn và dương")
    return args


def _require_training_dependencies():
    mismatches: list[str] = []
    for package, expected in REQUIRED_VERSIONS.items():
        try:
            actual = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            mismatches.append(f"{package} chưa cài (cần {expected})")
        else:
            if actual != expected:
                mismatches.append(f"{package}={actual} (cần {expected})")
    if mismatches:
        raise RuntimeError("Phiên D.3 cần package phiên bản đã chốt: " + "; ".join(mismatches))

    import torch
    from peft import LoraConfig, TaskType, get_peft_model, get_peft_model_state_dict, prepare_model_for_kbit_training, set_peft_model_state_dict
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    return (torch, LoraConfig, TaskType, get_peft_model, get_peft_model_state_dict,
            prepare_model_for_kbit_training, set_peft_model_state_dict,
            AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig)


def _set_seeds(torch, seed: int) -> None:
    """Set all stochastic state before tokenizer/model/adapter initialization."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # Deterministic kernels make validation/checkpoint comparison reproducible.
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.backends.cudnn.benchmark = False
    torch.use_deterministic_algorithms(True, warn_only=True)


def _rng_state(torch) -> dict[str, Any]:
    return {
        "python": random.getstate(),
        "torch_cpu": torch.get_rng_state().cpu(),
        "torch_cuda": [state.cpu() for state in torch.cuda.get_rng_state_all()],
    }


def _restore_rng(torch, state: Mapping[str, Any]) -> None:
    if not isinstance(state, Mapping) or not {"python", "torch_cpu", "torch_cuda"} <= set(state):
        raise ValueError("Checkpoint thiếu RNG state để resume xác định")
    random.setstate(state["python"])
    torch.set_rng_state(state["torch_cpu"].cpu())
    torch.cuda.set_rng_state_all([item.cpu() for item in state["torch_cuda"]])


def _runtime_identity(torch) -> dict[str, Any]:
    props = torch.cuda.get_device_properties(0)
    return {
        "python": sys.version,
        "torch": torch.__version__,
        "cuda_runtime": torch.version.cuda,
        "gpu": {
            "name": torch.cuda.get_device_name(0),
            "total_vram_bytes": props.total_memory,
            "compute_capability": [props.major, props.minor],
        },
        "packages": {name: importlib.metadata.version(name) for name in REQUIRED_VERSIONS},
    }


def _run_config(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "seed": args.seed,
        "lora_rank": args.rank,
        "lora_alpha": args.alpha,
        "learning_rate": args.lr,
        "epochs": args.epochs,
        "max_length": args.max_length,
        "batch_size": args.batch_size,
        "precision": "fp16-autocast-no-grad-scaler",
        "quantization": {"load_in_4bit": True, "type": "nf4", "double_quant": True, "compute_dtype": "float16"},
        "lora_targets": ["q_proj", "v_proj"],
        "lora_dropout": 0.0,
    }


def _make_manifest(args: argparse.Namespace, release: Path, release_manifest: Mapping[str, Any], tokenizer, torch) -> dict[str, Any]:
    chat_template = getattr(tokenizer, "chat_template", None)
    if not isinstance(chat_template, str) or not chat_template:
        raise ValueError("Tokenizer phải có chat_template cố định để mã hóa SFT")
    tokenizer_config = {
        "name_or_path": tokenizer.name_or_path,
        "vocab_size": tokenizer.vocab_size,
        "pad_token": tokenizer.pad_token,
        "pad_token_id": tokenizer.pad_token_id,
        "eos_token": tokenizer.eos_token,
        "eos_token_id": tokenizer.eos_token_id,
        "padding_side": tokenizer.padding_side,
        "truncation_side": tokenizer.truncation_side,
        "chat_template_sha256": hashlib.sha256(chat_template.encode("utf-8")).hexdigest(),
    }
    return {
        "format_version": FORMAT_VERSION,
        "model": {"id": MODEL_ID, "revision": MODEL_REVISION},
        "config": _run_config(args),
        "release": {
            "path": str(release.resolve()),
            "manifest": copy.deepcopy(dict(release_manifest)),
            "manifest_sha256": _release_manifest_hash(release, release_manifest),
        },
        "tokenizer": tokenizer_config,
        "source": {
            "scripts/train_d3_sft.py": _sha256_file(Path(__file__)),
            "src/d3_data.py": _sha256_file(_ROOT / "src" / "d3_data.py"),
        },
        "runtime": _runtime_identity(torch),
    }


def _encode_rows(rows: Iterable[dict[str, Any]], tokenizer, max_length: int, split_name: str) -> list[dict[str, list[int]]]:
    # Deliberately import the release interface only: it owns template/assistant masking policy.
    from src.d3_data import encode_qa

    encoded: list[dict[str, list[int]]] = []
    for row in rows:
        item = encode_qa(row, tokenizer, max_length)
        if not isinstance(item, dict) or set(item) != {"input_ids", "attention_mask", "labels"}:
            raise ValueError(f"encode_qa trả cấu trúc không hợp lệ cho split {split_name}")
        fields = [item["input_ids"], item["attention_mask"], item["labels"]]
        if not all(isinstance(field, list) for field in fields) or not fields[0] or len(fields[0]) > max_length:
            raise ValueError(f"encode_qa trả sequence rỗng/quá max_length ở {split_name}")
        if len(fields[0]) != len(fields[1]) or len(fields[0]) != len(fields[2]):
            raise ValueError(f"encode_qa trả các field lệch độ dài ở {split_name}")
        if any(label != -100 and not isinstance(label, int) for label in item["labels"]):
            raise ValueError(f"labels không hợp lệ ở {split_name}")
        if not any(label != -100 for label in item["labels"]):
            raise ValueError(f"Không có token assistant được giám sát ở {split_name}")
        encoded.append({key: list(value) for key, value in item.items()})
    return encoded


def _batches(torch, rows: list[dict[str, list[int]]], batch_size: int, pad_token_id: int, shuffle: bool, generator=None):
    indexes = list(range(len(rows)))
    if shuffle:
        permutation = torch.randperm(len(indexes), generator=generator).tolist()
        indexes = [indexes[index] for index in permutation]
    for start in range(0, len(indexes), batch_size):
        selected = [rows[index] for index in indexes[start:start + batch_size]]
        width = max(len(row["input_ids"]) for row in selected)
        input_ids = torch.full((len(selected), width), pad_token_id, dtype=torch.long)
        attention_mask = torch.zeros((len(selected), width), dtype=torch.long)
        labels = torch.full((len(selected), width), -100, dtype=torch.long)
        for position, row in enumerate(selected):
            length = len(row["input_ids"])
            input_ids[position, :length] = torch.tensor(row["input_ids"], dtype=torch.long)
            attention_mask[position, :length] = torch.tensor(row["attention_mask"], dtype=torch.long)
            labels[position, :length] = torch.tensor(row["labels"], dtype=torch.long)
        yield {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}


def _validation_metrics(torch, model, rows: list[dict[str, list[int]]], batch_size: int, pad_token_id: int) -> dict[str, float | int]:
    """Token-mean causal NLL, without batch-size weighting or test data."""
    model.eval()
    total_nll = 0.0
    total_tokens = 0
    with torch.inference_mode():
        for batch in _batches(torch, rows, batch_size, pad_token_id, shuffle=False):
            batch = {name: value.to("cuda", non_blocking=True) for name, value in batch.items()}
            with torch.autocast(device_type="cuda", dtype=torch.float16):
                logits = model(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"], use_cache=False).logits
            targets = batch["labels"][:, 1:]
            summed = torch.nn.functional.cross_entropy(
                logits[:, :-1, :].float().reshape(-1, logits.size(-1)),
                targets.reshape(-1), ignore_index=-100, reduction="sum",
            )
            count = int((targets != -100).sum().item())
            total_nll += float(summed.item())
            total_tokens += count
    if total_tokens == 0:
        raise ValueError("Validation không có assistant token sau causal shift")
    nll = total_nll / total_tokens
    return {"validation_tokens": total_tokens, "validation_nll": nll, "validation_ppl": math.exp(nll)}


def _checkpoint_manifest(directory: Path, epoch: int, run_identity_hash: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    hashes = _tree_hashes(directory)
    return {
        "format_version": FORMAT_VERSION,
        "complete": True,
        "epoch": epoch,
        "run_manifest_sha256": run_identity_hash,
        "metrics": dict(metrics),
        "files": hashes,
    }


def _save_checkpoint(torch, model, optimizer, shuffle_generator, get_peft_model_state_dict, output: Path, epoch: int,
                     run_identity_hash: str, metrics: Mapping[str, Any], best_record: Mapping[str, Any]) -> Path:
    checkpoint = output / "checkpoints" / f"epoch-{epoch:04d}"

    def populate(directory: Path) -> None:
        adapter_dir = directory / "adapter"
        model.save_pretrained(adapter_dir, safe_serialization=True, save_embedding_layers=False)
        state = {
            "format_version": FORMAT_VERSION,
            "epoch": epoch,
            "adapter_state": {name: tensor.detach().cpu() for name, tensor in get_peft_model_state_dict(model).items()},
            "optimizer_state": optimizer.state_dict(),
            "rng_state": _rng_state(torch),
            "shuffle_generator_state": shuffle_generator.get_state(),
            "metrics": dict(metrics),
            "best_record": copy.deepcopy(dict(best_record)),
        }
        torch.save(state, directory / "training_state.pt")
        manifest = _checkpoint_manifest(directory, epoch, run_identity_hash, metrics)
        _atomic_json(directory / "checkpoint_manifest.json", manifest)

    _atomic_directory(checkpoint, populate)
    return checkpoint


def _verify_checkpoint(path: Path, expected_run_identity_hash: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_dir():
        raise ValueError(f"Checkpoint không hợp lệ: {path}")
    manifest_path = path / "checkpoint_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Checkpoint thiếu manifest hoàn tất: {path}") from error
    if (manifest.get("format_version") != FORMAT_VERSION or manifest.get("complete") is not True
            or manifest.get("run_manifest_sha256") != expected_run_identity_hash):
        raise ValueError("Checkpoint không khớp run identity hoặc chưa hoàn tất")
    expected = manifest.get("files")
    if not isinstance(expected, dict) or "training_state.pt" not in expected or "adapter/adapter_config.json" not in expected:
        raise ValueError("Checkpoint manifest thiếu file bắt buộc")
    actual = _tree_hashes(path)
    # The manifest cannot hash itself; all other payload bytes must match exactly.
    actual.pop("checkpoint_manifest.json", None)
    if actual != expected:
        raise ValueError(f"Checksum checkpoint không khớp: {path}")
    return manifest


def _find_resume_checkpoint(path: Path, expected_run_identity_hash: str) -> Path:
    if path.name.startswith("epoch-"):
        _verify_checkpoint(path, expected_run_identity_hash)
        return path
    candidates = sorted((path / "checkpoints").glob("epoch-*"), reverse=True)
    failures: list[str] = []
    for candidate in candidates:
        try:
            _verify_checkpoint(candidate, expected_run_identity_hash)
            return candidate
        except ValueError as error:
            failures.append(str(error))
    suffix = f" ({failures[0]})" if failures else ""
    raise ValueError(f"Không tìm thấy checkpoint hoàn tất có thể resume dưới {path}{suffix}")


def _load_resume(torch, model, optimizer, shuffle_generator, set_peft_model_state_dict, checkpoint: Path,
                 expected_run_identity_hash: str) -> tuple[int, dict[str, Any], dict[str, Any]]:
    _verify_checkpoint(checkpoint, expected_run_identity_hash)
    state = torch.load(checkpoint / "training_state.pt", map_location="cpu", weights_only=True)
    if not isinstance(state, dict) or state.get("format_version") != FORMAT_VERSION:
        raise ValueError("training_state checkpoint không hợp lệ")
    epoch = state.get("epoch")
    best_record = state.get("best_record")
    if (not isinstance(epoch, int) or epoch < 1 or not isinstance(best_record, dict)
            or not isinstance(best_record.get("epoch"), int)
            or not isinstance(best_record.get("validation_nll"), (int, float))):
        raise ValueError("training_state thiếu best record hợp lệ")
    adapter_state = state.get("adapter_state")
    generator_state = state.get("shuffle_generator_state")
    if not isinstance(adapter_state, dict) or generator_state is None:
        raise ValueError("training_state thiếu adapter hoặc shuffle state")
    result = set_peft_model_state_dict(model, adapter_state, adapter_name="default")
    unexpected = getattr(result, "unexpected_keys", [])
    if unexpected:
        raise ValueError(f"Adapter checkpoint có key lạ: {unexpected}")
    optimizer.load_state_dict(state.get("optimizer_state"))
    _restore_rng(torch, state.get("rng_state"))
    shuffle_generator.set_state(generator_state.cpu())
    return epoch, copy.deepcopy(best_record), state


def _save_best_adapter(model, output: Path, checkpoint: Path, epoch: int, metrics: Mapping[str, Any]) -> None:
    target = output / "best_adapter"
    if target.exists():
        backup = output / ".best_adapter.previous"
        if backup.exists():
            shutil.rmtree(backup)
        os.replace(target, backup)
    else:
        backup = None
    try:
        def populate(directory: Path) -> None:
            model.save_pretrained(directory, safe_serialization=True, save_embedding_layers=False)
            _atomic_json(directory / "selection.json", {
                "selected_checkpoint": str(checkpoint.relative_to(output)),
                "epoch": epoch,
                "criterion": "minimum validation token-mean NLL",
                "metrics": dict(metrics),
            })
        _atomic_directory(target, populate)
    except BaseException:
        if backup is not None and backup.exists():
            os.replace(backup, target)
        raise
    else:
        if backup is not None:
            shutil.rmtree(backup)


def _copy_prior_best_adapter(output: Path, resume_checkpoint: Path, best_record: Mapping[str, Any],
                             expected_run_identity_hash: str) -> None:
    """Materialize a prior selected adapter in fresh Kaggle working storage."""
    best_epoch = best_record.get("epoch")
    if not isinstance(best_epoch, int) or best_epoch < 1:
        raise ValueError("Checkpoint không chỉ ra epoch best hợp lệ")
    source_checkpoint = resume_checkpoint.parent / f"epoch-{best_epoch:04d}"
    _verify_checkpoint(source_checkpoint, expected_run_identity_hash)
    source_adapter = source_checkpoint / "adapter"
    target = output / "best_adapter"
    if target.exists():
        raise FileExistsError(f"best_adapter đã tồn tại trong output mới: {target}")

    def populate(directory: Path) -> None:
        shutil.copytree(source_adapter, directory, dirs_exist_ok=True)
        _atomic_json(directory / "selection.json", {
            "selected_checkpoint": str(source_checkpoint.resolve()),
            "epoch": best_epoch,
            "criterion": "minimum validation token-mean NLL",
            "metrics": dict(best_record),
            "copied_from_read_only_resume": True,
        })

    _atomic_directory(target, populate)


def _write_metrics(output: Path, row: Mapping[str, Any]) -> None:
    metrics_path = output / "metrics.jsonl"
    with metrics_path.open("a", encoding="utf-8", newline="\n") as destination:
        destination.write(_stable_json(dict(row)).decode("utf-8"))
        destination.flush()
        os.fsync(destination.fileno())


def _run_identity(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Fields that must remain byte-identical when a Kaggle session resumes."""
    return {
        "format_version": manifest["format_version"],
        "model": manifest["model"],
        "config": manifest["config"],
        "release_manifest_sha256": manifest["release"]["manifest_sha256"],
        "tokenizer": manifest["tokenizer"],
        "source": manifest["source"],
    }


def _prepare_run(output: Path, manifest: Mapping[str, Any], resume: Path | None) -> str:
    run_manifest_path = output / "run_manifest.json"
    incoming_identity = _stable_json(_run_identity(manifest))
    if output.exists():
        if not output.is_dir():
            raise FileExistsError(f"--output không phải thư mục: {output}")
        if not resume:
            raise FileExistsError("--output đã tồn tại; dùng thư mục mới hoặc --resume")
        try:
            existing = json.loads(run_manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError("Output resume thiếu run_manifest.json hợp lệ") from error
        if _stable_json(_run_identity(existing)) != incoming_identity:
            raise ValueError("Cấu hình/release/tokenizer/source của resume không khớp run identity")
    else:
        output.mkdir(parents=True, exist_ok=False)
        _atomic_json(run_manifest_path, manifest)
    return hashlib.sha256(incoming_identity).hexdigest()


def main() -> None:
    args = _parse_args()
    try:
        release_manifest, splits = _validate_release(args.release)
        if args.check_only:
            print(json.dumps(_check_report(args.release, release_manifest, splits), ensure_ascii=False, sort_keys=True))
            return
        (torch, LoraConfig, TaskType, get_peft_model, get_peft_model_state_dict,
         prepare_model_for_kbit_training, set_peft_model_state_dict,
         AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig) = _require_training_dependencies()
        if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
            raise RuntimeError("D.3 SFT yêu cầu chính xác một CUDA GPU cho QLoRA")
        compute_capability = torch.cuda.get_device_capability(0)
        if compute_capability < (6, 0):
            raise RuntimeError(f"GPU cần compute capability >= 6.0, nhận {compute_capability[0]}.{compute_capability[1]}")
        _set_seeds(torch, args.seed)
        torch.cuda.reset_peak_memory_stats(0)

        # No remote/model work occurs before release validation and seed initialization.
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION, trust_remote_code=False, use_fast=True)
        tokenizer.padding_side = "right"
        if tokenizer.pad_token_id is None:
            if tokenizer.eos_token_id is None:
                raise ValueError("Tokenizer không có pad_token hoặc eos_token để padding an toàn")
            tokenizer.pad_token = tokenizer.eos_token
        train_rows = _encode_rows(splits["train"], tokenizer, args.max_length, "train")
        validation_rows = _encode_rows(splits["validation"], tokenizer, args.max_length, "validation")
        run_manifest = _make_manifest(args, args.release, release_manifest, tokenizer, torch)
        run_identity_hash = _prepare_run(args.output, run_manifest, args.resume)

        quantization = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16,
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, trust_remote_code=False, quantization_config=quantization,
            torch_dtype=torch.float16, device_map={"": 0}, low_cpu_mem_usage=True, use_safetensors=True,
        )
        base_model.config.use_cache = False
        base_model = prepare_model_for_kbit_training(base_model, use_gradient_checkpointing=True)
        model = get_peft_model(base_model, LoraConfig(
            r=args.rank, lora_alpha=args.alpha, target_modules=["q_proj", "v_proj"],
            lora_dropout=0.0, bias="none", task_type=TaskType.CAUSAL_LM,
        ))
        model.train()
        trainable = [parameter for parameter in model.parameters() if parameter.requires_grad]
        if not trainable:
            raise RuntimeError("Không tìm thấy LoRA parameter trainable")
        optimizer = torch.optim.AdamW(trainable, lr=args.lr)

        generator = torch.Generator(device="cpu")
        generator.manual_seed(args.seed)
        start_epoch = 1
        best_record: dict[str, Any] | None = None
        if args.resume:
            resume_checkpoint = _find_resume_checkpoint(args.resume, run_identity_hash)
            completed_epoch, best_record, _ = _load_resume(
                torch, model, optimizer, generator, set_peft_model_state_dict, resume_checkpoint, run_identity_hash,
            )
            start_epoch = completed_epoch + 1
            source_run = resume_checkpoint.parents[1]
            if args.output.resolve() != source_run.resolve():
                if not (args.output / "best_adapter").exists():
                    _copy_prior_best_adapter(args.output, resume_checkpoint, best_record, run_identity_hash)
                _atomic_json(args.output / "resumed_from.json", {
                    "checkpoint": str(resume_checkpoint.resolve()),
                    "source_run": str(source_run.resolve()),
                    "best_epoch_before_resume": best_record["epoch"],
                })
        last_completed_epoch = start_epoch - 1
        for epoch in range(start_epoch, args.epochs + 1):
            model.train()
            train_nll_sum = 0.0
            train_tokens = 0
            for batch in _batches(torch, train_rows, args.batch_size, tokenizer.pad_token_id, shuffle=True, generator=generator):
                batch = {name: value.to("cuda", non_blocking=True) for name, value in batch.items()}
                optimizer.zero_grad(set_to_none=True)
                # T4 FP16 autocast is intentional. Do not use GradScaler: unscale rejects FP16 LoRA grads.
                with torch.autocast(device_type="cuda", dtype=torch.float16):
                    outputs = model(**batch, use_cache=False)
                    loss = outputs.loss
                if not torch.isfinite(loss):
                    raise FloatingPointError(f"Loss không hữu hạn ở epoch {epoch}")
                loss.backward()
                optimizer.step()
                token_count = int((batch["labels"][:, 1:] != -100).sum().item())
                train_nll_sum += float(loss.detach().item()) * token_count
                train_tokens += token_count
            if train_tokens == 0:
                raise ValueError("Train không có assistant token sau causal shift")
            validation = _validation_metrics(torch, model, validation_rows, args.batch_size, tokenizer.pad_token_id)
            metrics = {
                "epoch": epoch,
                "train_tokens": train_tokens,
                "train_token_mean_nll": train_nll_sum / train_tokens,
                **validation,
                "peak_vram_bytes": int(torch.cuda.max_memory_allocated(0)),
                "peak_vram_reserved_bytes": int(torch.cuda.max_memory_reserved(0)),
            }
            is_best = best_record is None or validation["validation_nll"] < best_record["validation_nll"]
            if is_best:
                best_record = copy.deepcopy(metrics)
            checkpoint = _save_checkpoint(
                torch, model, optimizer, generator, get_peft_model_state_dict, args.output, epoch,
                run_identity_hash, metrics, best_record,
            )
            if is_best:
                _save_best_adapter(model, args.output, checkpoint, epoch, metrics)
            _write_metrics(args.output, {**metrics, "checkpoint": str(checkpoint.relative_to(args.output)), "is_best": is_best})
            print(json.dumps({"epoch": epoch, **validation, "is_best": is_best}, ensure_ascii=False), flush=True)
            last_completed_epoch = epoch
            if args.stop_after_epoch == epoch:
                break

        summary = {
            "run_manifest": "run_manifest.json",
            "metrics": "metrics.jsonl",
            "best_adapter": "best_adapter",
            "selection_metric": "minimum validation token-mean NLL",
            "requested_epochs": args.epochs,
            "completed_epochs": last_completed_epoch,
            "stopped_early": last_completed_epoch < args.epochs,
            "best_epoch": None if best_record is None else best_record["epoch"],
            "seed": args.seed,
        }
        _atomic_json(args.output / "summary.json", summary)
    except (OSError, ValueError, RuntimeError, FloatingPointError) as error:
        raise SystemExit(f"D3 SFT lỗi: {error}") from error


if __name__ == "__main__":
    main()
