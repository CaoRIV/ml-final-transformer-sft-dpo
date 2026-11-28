# Phiếu rà soát — Hà Mạnh Thế

Phiếu này để ghi lại việc rà soát theo
[cách nhóm phối hợp](team-execution-plan.md#2-nhóm-phối-hợp-thế-nào).
**Cột "Kết quả của Thế" do Thế tự điền.** AI dựng phiếu và ghi phần "Việc cần làm",
không điền kết quả.

Cách điền: làm đúng việc ở cột giữa, rồi ghi vào cột cuối. Ghi `OK` nếu đúng, hoặc
ghi ngắn chỗ thấy lạ. Ghi cả ngày.

---

## Phần 1 — Chạy lại phép kiểm mã (nhanh nhất, làm trước)

Mở terminal ở thư mục gốc repo, chạy:

```powershell
python -m pytest -q
```

Kết quả mong đợi: `30 passed, 1 skipped, 13 subtests passed`.

| # | Việc cần làm | Kết quả của Thế | Ngày |
|---|---|---|---|
| 1.1 | Chạy `python -m pytest -q`, ghi lại dòng kết quả cuối | | |
| 1.2 | Chạy `python -c "import torch; print(torch.__version__)"`, ghi phiên bản | | |

---

## Phần 2 — Đọc 4 file code (mỗi file 20–40 dòng)

Chỉ cần **mở ra đọc** và trả lời được câu hỏi ở cột giữa. Không cần sửa gì.

| # | File | Câu hỏi phải trả lời được | Kết quả của Thế | Ngày |
|---|---|---|---|---|
| 2.1 | [src/attention.py](../../src/attention.py) | Dòng `triu_(1)` làm gì? Vì sao phải che **trước** softmax? | | |
| 2.2 | [src/lora.py](../../src/lora.py) | Vì sao `B` khởi tạo bằng 0 mà adapter vẫn học được? | | |
| 2.3 | [src/dpo.py](../../src/dpo.py) | Vì sao `ref_chosen` phải `.detach()`? | | |
| 2.4 | [src/char_lm.py](../../src/char_lm.py) | Vì sao cộng tổng NLL rồi mới chia, không lấy trung bình PPL từng batch? | | |

Gợi ý: cả 4 câu đều có lời giải trong [báo cáo mục Phần A](../report/sections/02-phan-a.tex).
Nhưng phải tự nói lại được, không đọc thuộc.

---

## Phần 3 — Tự giải lại chứng minh (quan trọng nhất, 25 điểm)

Lấy **giấy bút**, giải lại từ đầu. Không chép. Giải xong thì so với
[part-b.tex](../theory/part-b.tex).

| # | Bài | Phải tự viết ra được | Kết quả của Thế | Ngày |
|---|---|---|---|---|
| 3.1 | **B.1** | `Var(q·k) = d_k`, và vì sao chia `√d_k` | | |
| 3.2 | **B.5** | `π* = π_ref·exp(R/β)/Z(x)`, rồi ra được loss DPO | | |
| 3.3 | B.2 | Đọc hiểu: vì sao causal mask phá đẳng biến hoán vị | | |
| 3.4 | B.3 | Đọc hiểu: vì sao số chiều lẻ thì mệnh đề sai | | |
| 3.5 | B.4 | Đọc hiểu: vì sao merge LoRA không đổi đầu ra | | |
| 3.6 | B.6 | Đọc hiểu: vì sao DPO cộng log-prob cả chuỗi, PPL lại chia theo token | | |

**Làm 3.1 và 3.2 trước.** Bốn cái sau chỉ cần đọc hiểu mạch.

Khi cả 6 dòng đã điền → báo Hà để đổi trạng thái B từ "chưa duyệt" sang "đã duyệt"
trong [ma trận yêu cầu](requirements-matrix.md) và bỏ dấu `Bản nháp` ở
`part-b.tex` dòng 24 và 49.

---

## Phần 4 — Đối chiếu 1 bài tập tính toán

Chọn **một** bài, giải lại rồi so với notebook.

| # | Bài | Gợi ý | Kết quả của Thế | Ngày |
|---|---|---|---|---|
| 4.1 | C.2 (dễ nhất) | Tự đếm tham số 1 khối với `d=64, f=128`. Phải ra **33.472** | | |

Công thức để tự đếm: `4d² + 2df + 9d + f`. Notebook đối chiếu:
[05_transformer_block_cost.ipynb](../../notebooks/05_transformer_block_cost.ipynb).

---

## Phần 5 — Việc đang bị chặn (chưa làm được)

| # | Việc | Chặn bởi |
|---|---|---|
| 5.1 | Chấm ≥500 cặp DPO (chấm **toàn bộ**, không chia với Hưng) | Hà chưa có checkpoint SFT |
| 5.2 | Rà gói nộp (báo cáo, lệnh tái lập, link, quyền chia sẻ) | 01/12 |

Trước khi làm 5.1, phải đọc [hướng dẫn chấm](../data/annotation-guide.md) và xác nhận
bằng văn bản là chỉ nhận dữ liệu DPO được phân quyền, **không** nhận phiếu đồng ý
hay khảo sát thô.

---

## Ghi chú thêm của Thế

<!-- Viết tự do ở đây: chỗ nào thấy sai, chỗ nào chưa hiểu, câu hỏi cho Hà -->
