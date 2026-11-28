#!/usr/bin/env python3
"""Script tái lập cho yêu cầu G7 (đề tr. 2, mục II).

Chạy từ gốc kho mã:

    python scripts/reproduce.py

Script này tái lập **những gì tái lập được trên CPU, không cần GPU, mạng,
dữ liệu QA hay checkpoint**:

  1. Ghi nhận môi trường thực tế.
  2. Chạy bộ kiểm tự động.
  3. Tính lại số tham số và MAC của C.2, đối chiếu với `DecoderBlock` A.1.
  4. Tính lại số tham số LoRA của C.3, đối chiếu với `LoRALinear` A.3.
  5. Tính lại loss và gradient DPO của C.4, đối chiếu với `dpo_loss` A.4.
  6. Tính lại trung bình và SD perplexity A.2 từ NLL từng seed đã ghi.
  7. Đối chiếu các con số trong báo cáo với tài liệu nguồn.

Script **không** tái lập: huấn luyện A.2 trên Kaggle, SFT pilot D.3, hay bất
kỳ số đo GPU nào. Những kết quả đó cần phần cứng và dữ liệu nằm ngoài kho mã;
xem mục Tái lập của báo cáo để biết hiện vật nào còn thiếu.

Mã trả về 0 nếu mọi phép đối chiếu khớp, 1 nếu có mục lệch.
"""

from __future__ import annotations

import io
import math
import re
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Console Windows mặc định không phải UTF-8; tránh UnicodeEncodeError.
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PASS: list[str] = []
FAIL: list[str] = []


def check(tag: str, got, want, tol: float = 0.0) -> None:
    if isinstance(want, float) or isinstance(got, float):
        good = abs(float(got) - float(want)) <= tol
    else:
        good = got == want
    (PASS if good else FAIL).append(f"{tag}: mong đợi {want}, tính được {got}")
    print(f"  [{'OK' if good else '!!'}] {tag}: {got}")


def section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# ---------------------------------------------------------------- 1. môi trường
def step_environment() -> None:
    section("1. Môi trường thực tế")
    import torch

    print(f"  Python          : {sys.version.split()[0]}")
    print(f"  PyTorch         : {torch.__version__}")
    print(f"  CUDA khả dụng   : {torch.cuda.is_available()}")
    print(f"  Gốc kho mã      : {ROOT}")
    print("\n  Môi trường GPU của D.3 khai báo ở requirements-d3.txt;")
    print("  PyTorch/CUDA lấy từ image Kaggle và không thay thế.")


# ------------------------------------------------------------------- 2. bộ kiểm
def step_tests() -> None:
    section("2. Bộ kiểm tự động")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    tail = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()][-1:]
    print("  " + (tail[0] if tail else "(không có đầu ra)"))
    (PASS if proc.returncode == 0 else FAIL).append(
        f"pytest thoát với mã {proc.returncode}"
    )
    print(f"  [{'OK' if proc.returncode == 0 else '!!'}] pytest")


# ----------------------------------------------------------------------- 3. C.2
def step_c2() -> None:
    section("3. C.2 — tham số và MAC của một khối decoder")
    import torch
    from src.attention import DecoderBlock

    d, f, n, heads = 64, 128, 128, 4
    formula_params = 4 * d * d + 2 * d * f + 9 * d + f
    formula_mac = 4 * n * d * d + 2 * n * d * f + 2 * n * n * d

    check("công thức 4d²+2df+9d+f", formula_params, 33_472)
    check("công thức 4nd²+2ndf+2n²d", formula_mac, 6_291_456)
    check("hai tích attention chiếm 1/3 MAC", 2 * n * n * d, formula_mac // 3)

    # doi chieu voi lop that
    for h in (4, 8):
        block = DecoderBlock(d, h, f, max_len=256).eval()
        live = sum(p.numel() for p in block.parameters() if p.requires_grad)
        check(f"numel() thực của DecoderBlock, {h} head", live, formula_params)

    with torch.inference_mode():
        DecoderBlock(d, heads, f, max_len=256).eval()(torch.zeros(1, n, d))
    PASS.append("forward một khối chạy được ở n=128")
    print("  [OK] forward một khối chạy được ở n=128")


# ----------------------------------------------------------------------- 4. C.3
def step_c3() -> None:
    section("4. C.3 — tham số LoRA ở Q/V của Qwen2.5-1.5B-Instruct")
    from torch import nn
    from src.lora import LoRALinear

    layers, d, heads, kv_heads = 28, 1536, 12, 2
    kv = kv_heads * (d // heads)
    check("hệ số P_Q = 28(1536+1536)", layers * (d + d), 86_016)
    check("hệ số P_V = 28(1536+256)", layers * (d + kv), 50_176)
    check("hệ số P = 136.192", layers * (d + d) + layers * (d + kv), 136_192)

    expected = {4: 544_768, 8: 1_089_536, 16: 2_179_072}
    for rank, want in expected.items():
        total = 0
        for out_features in (heads * (d // heads), kv):
            base = nn.Linear(d, out_features, bias=True, device="meta")
            adapter = LoRALinear(base, rank=rank, alpha=rank)
            total += layers * sum(
                p.numel() for p in adapter.parameters() if p.requires_grad
            )
        check(f"LoRALinear đếm thực, r={rank}", total, want)


# ----------------------------------------------------------------------- 5. C.4
def step_c4() -> None:
    section("5. C.4 — loss và gradient DPO")
    import torch
    from src.dpo import dpo_loss

    logps = (math.log(0.2), math.log(0.1), math.log(0.4), math.log(0.1))
    inputs = tuple(
        torch.tensor(x, dtype=torch.float64, requires_grad=True) for x in logps
    )
    loss = dpo_loss(*inputs, beta=1.0)
    gw, gl, grw, grl = torch.autograd.grad(loss, inputs, allow_unused=True)

    check("loss = ln 3", round(loss.item(), 6), round(math.log(3), 6), 1e-9)
    check("∂L/∂p_w = −2/3", round(gw.item(), 6), round(-2 / 3, 6), 1e-9)
    check("∂L/∂p_l = +2/3", round(gl.item(), 6), round(2 / 3, 6), 1e-9)
    check("reference không nhận gradient", (grw, grl), (None, None))

    # margin = 0 -> loss = ln 2 voi moi beta; gradient = beta/2
    for beta in (0.1, 1.0, 2.0, 8.0):
        eq = tuple(
            torch.tensor(x, dtype=torch.float64, requires_grad=True)
            for x in (math.log(0.4), math.log(0.1), math.log(0.4), math.log(0.1))
        )
        li = dpo_loss(*eq, beta=beta)
        gi = torch.autograd.grad(li, eq[:2])[0]
        check(f"margin=0, β={beta}: loss = ln 2", round(li.item(), 9),
              round(math.log(2), 9), 1e-9)
        check(f"margin=0, β={beta}: |gradient| = β/2", round(abs(gi.item()), 9),
              round(beta / 2, 9), 1e-9)


# ----------------------------------------------------------------------- 6. A.2
def step_a2() -> None:
    section("6. A.2 — tổng hợp perplexity từ NLL từng seed")
    seed_nll = {41: 2.326985, 42: 2.328789, 43: 2.321075, 44: 2.318854, 45: 2.313612}
    ppls = []
    for seed, nll in seed_nll.items():
        ppl = math.exp(nll)
        ppls.append(ppl)
        print(f"  seed {seed}: NLL {nll:.6f} -> PPL {ppl:.4f}")
    check("trung bình PPL", round(statistics.fmean(ppls), 4), 10.1948, 1e-9)
    check("SD mẫu PPL (mẫu số 4)", round(statistics.stdev(ppls), 4), 0.0628, 1e-9)
    check("số target được chấm = 81 cửa sổ × 128", 81 * 128, 10_368)
    print("\n  Lưu ý: đây là tổng hợp lại từ NLL đã ghi, KHÔNG phải huấn luyện lại.")
    print("  Lượt huấn luyện gốc chạy trên Kaggle; log môi trường còn thiếu.")


# --------------------------------------------- 7. doi chieu bao cao voi nguon
def step_report_vs_sources() -> None:
    section("7. Đối chiếu số trong báo cáo với tài liệu nguồn")
    report_a = read("docs/report/sections/02-phan-a.tex")
    corpus = read("docs/data/char-corpus.md")
    report_d = read("docs/report/sections/05-phan-d.tex")
    ctx = read("docs/progress/project-context.md")

    # Corpus 1911 dang thuc dung (char-corpus.md muc 5), KHONG phai revision 206607.
    for value in ("3.254", "104.181", "93.762", "10.419", "127", "732 / 81", "10.368"):
        in_report = value in report_a
        in_source = value in corpus
        tag = f"A.2 corpus 1911 «{value}» có ở cả báo cáo và nguồn"
        (PASS if (in_report and in_source) else FAIL).append(tag)
        print(f"  [{'OK' if in_report and in_source else '!!'}] {tag}")

    # So cua revision 206607 da bi loai, khong duoc dung lam so lieu A.2.
    for stale in ("104.204", "93.783", "10.421"):
        leaked = stale in report_a
        tag = f"số của revision 206607 đã bị loại «{stale}» KHÔNG còn trong báo cáo"
        (FAIL if leaked else PASS).append(tag)
        print(f"  [{'!!' if leaked else 'OK'}] {tag}")

    # Pilot D.3 do nhom cung cap.
    for value in ("1,509630", "1,242314", "4,525054", "3,463617", "1.235", "388"):
        both = value in report_d and value in ctx
        tag = f"D.3 pilot «{value}» khớp project-context"
        (PASS if both else FAIL).append(tag)
        print(f"  [{'OK' if both else '!!'}] {tag}")

    check("exp(1,509630)", round(math.exp(1.509630), 6), 4.525054, 1e-5)
    check("exp(1,242314)", round(math.exp(1.242314), 6), 3.463617, 1e-5)


# ------------------------------------------------- 8. cau truc nguon bao cao
def step_report_structure() -> None:
    section("8. Cấu trúc nguồn báo cáo LaTeX")
    main = ROOT / "docs/report/report.tex"
    text = re.sub(r"(?<!\\)%.*", "", main.read_text(encoding="utf-8"))
    inputs = re.findall(r"\\input\{([^}]+)\}", text)
    files = [main]
    missing = []
    for rel in inputs:
        path = main.parent / (rel if rel.endswith(".tex") else rel + ".tex")
        (files if path.is_file() else missing).append(path)
    check("mọi \\input tồn tại", len(missing), 0)

    labels, refs = set(), []
    for path in files:
        body = re.sub(r"(?<!\\)%.*", "", path.read_text(encoding="utf-8"))
        labels |= set(re.findall(r"\\label\{([^}]+)\}", body))
        refs += re.findall(r"\\(?:eq)?ref\{([^}]+)\}", body)
    check("số tham chiếu treo", len([r for r in refs if r not in labels]), 0)
    print(f"  {len(labels)} nhãn, {len(refs)} tham chiếu")
    print("\n  Chưa biên dịch ở đây: cần tectonic hoặc XeLaTeX.")
    print("  Yêu cầu 25–40 trang vì vậy CHƯA được xác nhận bằng script này.")


def main() -> int:
    print(__doc__.split("Mã trả về")[0].strip())
    for step in (step_environment, step_tests, step_c2, step_c3, step_c4,
                 step_a2, step_report_vs_sources, step_report_structure):
        try:
            step()
        except Exception as exc:  # noqa: BLE001
            FAIL.append(f"{step.__name__} lỗi: {exc!r}")
            print(f"  [!!] {step.__name__} lỗi: {exc!r}")

    section("Tổng hợp")
    print(f"  Khớp : {len(PASS)}")
    print(f"  Lệch : {len(FAIL)}")
    for item in FAIL:
        print(f"    !! {item}")
    if FAIL:
        print("\n  KẾT QUẢ: CÓ MỤC LỆCH — xem danh sách trên.")
        return 1
    print("\n  KẾT QUẢ: mọi phép đối chiếu tái lập được trên CPU đều khớp.")
    print("  Các kết quả cần GPU (A.2 Kaggle, SFT pilot D.3) không nằm trong phạm vi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
