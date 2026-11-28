# Đề tài 9 · Transformer, SFT và DPO cho trợ lý hỏi đáp thủ tục hành chính

Nhóm xây dựng trợ lý tiếng Việt trong phạm vi **hộ tịch và chứng thực tại Hà Nội**. Mục tiêu là trả lời có căn cứ, nêu điều kiện áp dụng và không đoán khi thiếu thông tin. A–C giải thích và kiểm chứng thuật toán; D dùng dữ liệu có nguồn để tinh chỉnh và đánh giá trợ lý. **Bản có thể hỏi thử hiện nay là SFT pilot trên Kaggle Private**, không phải mô hình đã hoàn thành DPO hay hệ thống tư vấn chính thức.

**Mốc của nhóm:** chốt gói nội bộ lúc 20h00, hạn hoàn thành **23h59 ngày 01/12/2026**; vấn đáp ngày 03/12. Xem [lịch bàn giao](docs/progress/defense-plan-2026-12-03.md). Yêu cầu chấm lấy từ [đề ngày 12/11/2026](references/README.md), tr. 1–2 và 18–19; theo dõi từng yêu cầu trong [ma trận A–D](docs/progress/requirements-matrix.md).

## Vừa pull về: bắt đầu từ đâu?

| Bạn cần làm gì? | Việc đầu tiên | Bàn giao cho ai? |
|---|---|---|
| **Thế và Hưng: rà QA b03 (D.2)** | Nhận `offline-review-b03.zip` từ Hà qua kênh riêng. Giải nén, đọc `HUONG-DAN.md`; Thế mở `phieu-ra-the.csv`, Hưng mở `phieu-ra-hung.csv`. **Không cần GPU, Python hay chạy lại `prepare`.** | Gửi lại CSV đã điền cho Hà. Không sửa trực tiếp `qa.jsonl` hay phiếu của người kia. |
| **Hà: tổng hợp kết quả D.2** | Giữ bản gốc trên máy có dữ liệu b03. Dùng lệnh ghép trong `HUONG-DAN.md` để lấy đúng 84 dòng mẫu, rồi chạy `check` theo [quy trình phát hành](docs/data/README.md). | Báo số thực đã rà, lỗi cần sửa và điều kiện còn thiếu. Có phiếu không đồng nghĩa đã được phép train. |
| **Hà: chuẩn bị chấm thử; Thế và Hưng: hiệu chuẩn D.4** | Hà dùng [notebook 10](notebooks/10_d3_hoi_thu_kaggle.ipynb) để sinh 10 cặp từ adapter thật. **Mỗi người chấm cả 10 cặp** theo [rubric](docs/data/annotation-guide.md), không xem phiếu của nhau. | Gửi riêng hai phiếu cho Hà. Hà khóa nhãn, quy A/B về cùng đáp án và đo đồng thuận **trước** khi phân xử. Lô thử không tính vào 500 cặp. |
| **Nhóm: chuẩn bị khảo sát `USER_TEST`** | Hà xác nhận các điều kiện [G-01–G-06](docs/data/privacy-workflow.md) trước khi mời. Đề xuất Thế chuyển lời mời cho lớp/người thân từ đủ 18 tuổi; người chấm DPO không nhận hoặc đọc câu hỏi test. | Người được phân quyền thu bằng [phiếu consent và khảo sát tách riêng](docs/data/consent-and-survey.md), ẩn danh và khóa test ngoài Git. Chưa đủ điều kiện thì chưa thu. |

**Vì sao không thấy ZIP sau `git pull`?** Git có mã, notebook, tài liệu và hướng dẫn. Phiếu nằm trên máy chuẩn bị tại `data/review/d2/d2-official-main-b03/offline-review-b03.zip`; `data/review/` và `.cache/` không đi theo Git. Không cần gửi cả cache. Trong ZIP có đoạn trích, vị trí, URL và `nguon-ra-offline.csv` để tải văn bản trước khi làm offline. Nếu lớp chữ PDF bị lỗi, mở đúng trang gốc trước khi duyệt.

**Ưu tiên trên phiếu:** mỗi người nhận 197 câu train và 1 câu validation. Lọc `is_official_sample=true` để làm **42 dòng/người** trước (41 train + 1 validation). Các dòng này đã nằm trong phiếu, không chấm thêm lần hai. Đừng nhầm với DPO: **D.2 chia câu giữa hai người; D.4 cần hai đánh giá độc lập cho từng cặp.**

## Tiến độ và giới hạn của kết quả

| Phần | Đã có bằng chứng | Chưa thể kết luận |
|---|---|---|
| **A · Cài đặt** | [Attention và decoder](notebooks/01_attention_decoder.ipynb), [LM ký tự](notebooks/04_char_lm.ipynb), [LoRA](notebooks/03_lora_linear.ipynb), [DPO loss](notebooks/02_dpo_loss.ipynb). A.2 đã chạy 5 seed trên [Truyện Kiều bản 1911](docs/data/char-corpus.md). | Kiểm DPO loss trên ví dụ số chưa thay phép đối chiếu loss và gradient trên minibatch thật của D. |
| **B · Chứng minh** | [Nguồn LaTeX của sáu chứng minh](docs/theory/part-b.tex) đã bổ sung điều kiện số chiều chẵn cho B.3. | Chưa được nhóm duyệt. Thế và Hưng tự giải lại; có [khung B.1/B.5](docs/theory/khung-giai-b1-b5.md) và [phiếu rà của Thế](docs/progress/review-log-the.md). |
| **C · Bài tập** | Đã đối chiếu trên CPU: [C.1 attention](notebooks/08_causal_attention_example.ipynb), [C.2 chi phí decoder](notebooks/05_transformer_block_cost.ipynb), [C.3 LoRA/QLoRA](notebooks/06_lora_qlora_cost.ipynb), [C.4 loss và gradient](notebooks/07_dpo_loss_gradient.ipynb). | Đầu vào C.1 và C.4 là minh họa, không phải số giảng viên cấp. Bộ nhớ C.3 là ước lượng, không phải peak VRAM đo được. |
| **D.1–D.2 · Nguồn và QA** | Có [sổ kiểm nguồn](docs/data/source-audit.md). Pilot `release-01` đã duyệt 24/24 (18 train + 6 validation). [B03](docs/data/README.md#tập-chính-d2--lô-ứng-viên-b03) có 400 QA **ứng viên**: 394 train + 6 validation, gồm lại 24 QA pilot. | B03 chưa phát hành. Không cộng 24 pilot vào 400, không lấy 20 QA rà sơ bộ làm quota tập chính. Đề cần ≥2.000 QA có trích dẫn và ≥20% kiểm thủ công; 400 **ứng viên** không có nghĩa là 400 **đã kiểm**. |
| **D.3 · SFT** | Qwen2.5-1.5B-Instruct + QLoRA đã chạy trên Kaggle T4, seed 41. Epoch 2 có PPL validation **3,46**; chạy nối từ epoch 1 tái lập NLL/PPL epoch 2 theo [log pilot](docs/progress/project-context.md#d3--kết-quả-pilot-do-nhóm-chạy-trên-kaggle). | Chưa huấn luyện tập chính. Khi hỏi thử, mô hình trả sai thời hạn và không từ chối câu visa ngoài phạm vi. PPL không đo độ chính xác pháp lý. |
| **D.4–D.5 · DPO và đánh giá** | Có đường xuất phiếu hiệu chuẩn và hướng dẫn chấm. | Chưa có bằng chứng đủ 500 cặp, mô hình DPO hoặc kết quả so sánh mù base/SFT/SFT+DPO trên câu hỏi khảo sát thật. |

## Chạy kiểm tra

**Trên máy thành viên:** chạy lệnh từ thư mục gốc của repo bằng môi trường Python đã có PyTorch. Kiểm nhanh A.1 không cần mạng, dữ liệu riêng hay GPU:

```sh
python -m unittest discover -s tests -p "test_attention.py" -v
```

Để kiểm riêng A.2, A.3 hoặc A.4, thay mẫu tên tệp lần lượt bằng `test_char_lm*.py`, `test_lora.py` hoặc `test_dpo.py`. Trước bàn giao báo cáo, môi trường cần thêm `pytest`; dùng lệnh sau để chạy bộ kiểm và đối chiếu số liệu A–C với báo cáo. Lệnh **không** huấn luyện lại hoặc xác minh được kết quả GPU:

```sh
python scripts/reproduce.py
```

### D.3 — chuẩn bị SFT trên Kaggle

- **Muốn hỏi thử, không cần train lại:** import [notebook 10](notebooks/10_d3_hoi_thu_kaggle.ipynb) vào Kaggle Private, bật T4 và gắn hai input: `CODE_DIR` là thư mục `D3-code` chứa `src/` và `requirements-d3.txt`; `RUN_DIR` là output lần train liên tục chứa `run_manifest.json`, `summary.json` và `best_adapter/`. Chạy tuần tự rồi đổi câu trong `hoi(...)`. Giữ `PREPARE_OFFLINE_REVIEW=False` khi chỉ demo.
- **Muốn xuất 10 cặp hiệu chuẩn:** trong cùng notebook, gắn thêm `D3-Release` **release-01** bằng *Add Input*, điền `PAIR_RELEASE_INPUT` bằng *Copy path* đến thư mục có `manifest.json`, `train.jsonl`, `validation.jsonl`; đặt `PREPARE_OFFLINE_REVIEW=True`. Trong `/kaggle/working/d3-offline-review-10/`, gửi riêng `phieu-01.csv` cho Thế và `phieu-02.csv` cho Hưng; Hà giữ `batch-provenance.private.json`. Không gửi cả thư mục cho người chấm.
- **Muốn tái lập lượt train pilot:** dùng [notebook 09](notebooks/09_d3_sft_kaggle.ipynb) với gói mã, release đã duyệt và SHA-256 của **manifest**, không phải của ZIP. Giữ `INSTALL_PACKAGES=False` và `RUN_TRAIN=False` để kiểm đầu vào trên CPU trước; chỉ chuyển sang GPU sau `release-valid`. Lưu *Save Version* riêng tư với cả `best_adapter/` lẫn `checkpoints/`. [Script đóng gói](scripts/package_d3_kaggle.py) không tự upload. Quyền dùng Kaggle Private của release-01 **không áp dụng cho b03**.

**Kế hoạch tập chính, chưa chạy:** sau khi có `main_sft_ready`, so sánh rank, alpha, learning rate và epoch trên validation; khóa cấu hình trước các lượt seed 41–45. Không chọn cấu hình bằng `USER_TEST`, không tính một lần resume thành một lần huấn luyện độc lập.

## Nơi cập nhật khi công việc thay đổi

- **Tiến độ và phân công:** ghi kết quả có bằng chứng vào [nhật ký dự án](docs/progress/project-context.md), đối chiếu [yêu cầu giảng viên](docs/progress/requirements-matrix.md). Hà tổng hợp và nộp; cả ba thành viên cần hiểu toàn bộ A–D theo [kế hoạch phối hợp](docs/progress/team-execution-plan.md).
- **Dữ liệu và mô hình:** quy trình tạo, kiểm và phát hành nằm ở [hướng dẫn D.2](docs/data/README.md). Ghi phạm vi dữ liệu trong [datasheet](docs/data/datasheet.md), cấu hình, kết quả và giới hạn mô hình trong [model card](docs/model/model-card.md). Không commit phiếu đã điền, consent, khảo sát, token, trọng số hay checkpoint. Không công khai PDF tham khảo khi chưa xác minh quyền phân phối.
- **Báo cáo cuối kỳ:** sửa [báo cáo LaTeX](docs/report/report.tex) theo [hướng dẫn biên dịch và rà trước nộp](docs/report/README.md); yêu cầu 25–40 trang, bản hiện tại chưa được nhóm duyệt. Ghi phạm vi hỗ trợ AI vào [nhật ký AI](docs/progress/ai-use.md) để chuyển sang phụ lục.
- **Tài liệu nền:** [tổng quan cho người mới](docs/project-overview.md), [đề cương](docs/proposal/proposal.md), [kế hoạch dữ liệu](docs/proposal/data-plan.md) và [cách dựng PDF tuần 1](docs/proposal/README.md). Hồ sơ tuần 1 không thay báo cáo cuối kỳ.
