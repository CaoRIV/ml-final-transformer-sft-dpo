# Trợ lý hỏi đáp thủ tục hành chính tiếng Việt

Dự án nghiên cứu Transformer, tinh chỉnh có giám sát (SFT) và tối ưu theo cặp ưu tiên (DPO) cho bài toán hỏi đáp về **hộ tịch và chứng thực tại Hà Nội**. Mục tiêu là trả lời câu hỏi về hồ sơ, thời hạn và lệ phí dựa trên văn bản có thể kiểm chứng, đồng thời từ chối khi không đủ căn cứ.

**Trạng thái:** đã chạy SFT thử nghiệm với Qwen2.5-1.5B-Instruct trên Kaggle. Chưa huấn luyện DPO hoặc đánh giá trên câu hỏi khảo sát của người dùng. Bản thử nghiệm không thay thế hướng dẫn của cơ quan có thẩm quyền.

[Báo cáo kỹ thuật](docs/report/README.md) · [Hồ sơ dữ liệu](docs/data/datasheet.md) · [Hồ sơ mô hình](docs/model/model-card.md) · [Yêu cầu Đề tài 9](docs/progress/requirements-matrix.md)

## Bắt đầu trên CPU

Từ thư mục gốc, dùng môi trường Python đã cài PyTorch. Lệnh sau kiểm tra cơ chế attention và causal mask mà không cần GPU, dữ liệu riêng hay checkpoint:

```sh
python -m unittest discover -s tests -p "test_attention.py" -v
```

Để chạy bộ kiểm và đối chiếu các số liệu A–C với báo cáo, dùng môi trường có thêm `pytest`:

```sh
python scripts/reproduce.py
```

[Script tái lập](scripts/reproduce.py) tính lại số tham số, số phép tính và gradient; với mô hình ký tự, script tổng hợp perplexity từ các lần chạy đã ghi. Lệnh này không huấn luyện lại mô hình.

## Nội dung nghiên cứu

| Phần | Nội dung | Mã và tài liệu |
|---|---|---|
| A · Cài đặt | Tự viết Transformer decoder, mô hình ngôn ngữ ký tự, LoRA và hàm mất mát DPO bằng PyTorch. Mô hình ký tự học trên *Truyện Kiều* bản 1911, độc lập với trợ lý hành chính. | [Mã nguồn](src/) · [Corpus ký tự](docs/data/char-corpus.md) · [Kiểm thử](tests/) |
| B · Lý thuyết | Sáu chứng minh về attention, mã hóa vị trí, LoRA, DPO và mối liên hệ giữa cross-entropy, KL và perplexity. | [Bản thảo LaTeX](docs/theory/part-b.tex) |
| C · Kiểm chứng | Tính attention có mask, chi phí decoder, số tham số và bộ nhớ LoRA/QLoRA, loss và gradient DPO. Bộ nhớ ở C.3 là ước lượng, không phải số đo GPU. | [Các notebook tính toán](notebooks/) |
| D · Ứng dụng | Soạn QA có trích dẫn từ văn bản chính thức và huấn luyện SFT. Bước đánh giá theo đề bài là so sánh mô hình gốc, SFT và SFT+DPO trên cùng tập test độc lập. | [Quy trình dữ liệu](docs/data/README.md) · [Script huấn luyện SFT](scripts/train_d3_sft.py) |

## Kết quả SFT thử nghiệm

Nhóm tinh chỉnh Qwen2.5-1.5B-Instruct bằng QLoRA 4-bit trên Tesla T4 (seed 41, hai epoch). Bản `release-01` gồm **18 QA huấn luyện và 6 QA validation** đã kiểm thủ công. Perplexity trên 388 token trả lời của tập validation giảm từ **4,53 xuống 3,46**; chạy nối từ checkpoint epoch 1 cho cùng NLL và perplexity ở epoch 2.

Perplexity không đo độ đúng của câu trả lời hành chính. Khi hỏi thử, mô hình **trả sai thời hạn xác nhận thông tin hộ tịch** và **không từ chối câu hỏi về thị thực Nhật Bản**. [Nhật ký thí nghiệm](docs/progress/project-context.md#d3--kết-quả-pilot-do-nhóm-chạy-trên-kaggle) ghi cấu hình, kết quả chạy nối và hai trường hợp này.

[Lô b03](docs/data/README.md#tập-chính-d2--lô-ứng-viên-b03) có 400 QA ứng viên, **đã bao gồm** 24 QA của pilot; đây chưa phải tập huấn luyện đã phát hành. Yêu cầu của đề là ít nhất 2.000 QA có trích dẫn, kiểm thủ công ít nhất 20%, và ít nhất 500 cặp ưu tiên được hai người chấm độc lập.

### D.3 — chuẩn bị SFT trên Kaggle

- **Huấn luyện:** mở [notebook SFT](notebooks/09_d3_sft_kaggle.ipynb) trên Kaggle Private với gói mã và `release-01`. Kiểm tra đầu vào trên CPU với `INSTALL_PACKAGES=False`, `RUN_TRAIN=False`; chỉ bật GPU để huấn luyện sau khi thấy `release-valid`. Các phiên bản thư viện nằm trong [requirements-d3.txt](requirements-d3.txt).
- **Hỏi thử mà không huấn luyện lại:** mở [notebook suy luận](notebooks/10_d3_hoi_thu_kaggle.ipynb). `CODE_DIR` trỏ tới gói mã chứa `src/`; `RUN_DIR` trỏ tới thư mục kết quả chứa `run_manifest.json`, `summary.json` và `best_adapter/`. Chạy tuần tự rồi nhập câu hỏi vào `hoi(...)`.

Dữ liệu phát hành nội bộ và checkpoint không đi kèm bản clone. Quyền sử dụng `release-01` trên Kaggle Private không áp dụng cho b03. Phiếu đã điền, văn bản đồng ý và dữ liệu khảo sát không đưa lên Git; xem [quy trình bảo vệ dữ liệu](docs/data/privacy-workflow.md).

## Tài liệu

- [Đề cương](docs/proposal/proposal.md) và [tài liệu tham khảo](references/README.md): phạm vi nghiên cứu, đề gốc và các bài báo nền tảng.
- [Sổ kiểm nguồn](docs/data/source-audit.md) và [hướng dẫn gán nhãn](docs/data/annotation-guide.md): căn cứ cho đáp án, tiêu chí kiểm QA và chấm cặp ưu tiên.
- [Tiến độ và bàn giao](docs/progress/project-context.md) và [kế hoạch phối hợp](docs/progress/team-execution-plan.md): quyết định, bằng chứng và phân công của nhóm.
