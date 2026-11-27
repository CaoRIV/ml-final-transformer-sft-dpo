# Đề tài 9 — Kiến trúc Transformer và tinh chỉnh mô hình ngôn ngữ

Nhóm xây dựng **trợ lý hỏi đáp thủ tục hộ tịch–chứng thực tại Hà Nội**: câu trả lời cần có nguồn để kiểm tra, và trợ lý phải nói rõ khi không đủ căn cứ. Đề gồm hai nhánh: tự viết Transformer nhỏ để hiểu cách mô hình hoạt động (A–C), rồi tinh chỉnh và đánh giá một mô hình tiếng Việt có sẵn cho bài toán thủ tục (D).

**Nhóm:** Cao Văn Hà (trưởng nhóm, tổng hợp và nộp bài), Hà Mạnh Thế, Trần Duy Hưng.

[Cách nhóm làm việc](#cách-nhóm-làm-việc) · [Hồ sơ và đề gốc](#hồ-sơ-và-đề-gốc) · [Chạy kiểm tra](#chạy-kiểm-tra)

## Bắt đầu ở đây

1. [Giới thiệu bài tập lớn](docs/project-overview.md) — đọc trước để hiểu nhóm xây gì và sẽ đánh giá ra sao; không cần biết trước về Transformer, SFT hay DPO.
2. [Cách phối hợp và rà soát](docs/progress/team-execution-plan.md#2-nhóm-phối-hợp-thế-nào) — xem cách Hà làm bản đầu, Thế và Hưng luân phiên rà, rồi cả nhóm chốt kết quả. [Kế hoạch A–D](docs/progress/team-execution-plan.md) ghi cách làm và đầu ra của từng phần.
3. [Lịch hoàn thành và vấn đáp](docs/progress/defense-plan-2026-12-03.md#2-lịch-bàn-giao-nội-bộ) — **hoàn thành toàn dự án muộn nhất 23h59 ngày 01/12/2026**. Ngày 02/12 diễn tập trên bản đã khóa; ngày 03/12 vấn đáp.

## Cách nhóm làm việc

**Không chia cứng A–D cho từng người.** Hà thực hiện chính, tổng hợp và nộp bài. Thế và Hưng luân phiên rà soát, chạy lại phép kiểm hoặc đối chiếu nguồn; cả ba cùng tham gia và hiểu toàn bộ dự án.

| Cần làm gì? | Mở ở đây |
|---|---|
| **A — Cài đặt và kiểm chứng** | [A.1: mã PyTorch](src/attention.py) · [Notebook dẫn xuất và kiểm decoder trên CPU](notebooks/01_attention_decoder.ipynb) · [Kế hoạch phần A](docs/progress/team-execution-plan.md#a--tự-cài-đặt-và-kiểm-chứng-20-điểm-tr-1-và-18). |
| **B — Chứng minh** | [Sáu chứng minh bản nháp](docs/theory/part-b.pdf) để cả nhóm rà và hỏi chéo. |
| **C — Bài tập** | [C.1: tính tay causal attention trên bộ Q/K/V minh họa](notebooks/08_causal_attention_example.ipynb) · [C.2: chi phí Transformer block](notebooks/05_transformer_block_cost.ipynb) · [C.3: LoRA Q/V và bộ nhớ QLoRA](notebooks/06_lora_qlora_cost.ipynb) · [C.4: loss, gradient DPO và ảnh hưởng của β](notebooks/07_dpo_loss_gradient.ipynb). |
| **D — Dữ liệu và mô hình** | [Quy trình từ nguồn tới đánh giá](docs/progress/team-execution-plan.md#d--dữ-liệu-tinh-chỉnh-và-đánh-giá-trợ-lý-30-điểm-tr-19) · [Kiểm QA mẫu](docs/data/admin-pilot.md) · [Khảo sát và đồng ý](docs/data/consent-and-survey.md) · [Notebook Colab](notebooks/00_environment_check.ipynb). |

**Riêng chấm cặp DPO:** Thế và Hưng **đều chấm từng cặp độc lập**, không luân phiên chia cặp. Hà phân xử sau khi khóa nhãn và đo đồng thuận. Xem [hướng dẫn chấm](docs/data/annotation-guide.md).

## Hồ sơ và đề gốc

| Cần tìm | Mở ở đây |
|---|---|
| **Đề của giảng viên** | [Danh mục bài tập lớn và các bài báo tham khảo](references/README.md). Dùng bản đề ngày 12/11/2026: phần I–II tr. 1–2, Đề tài 9 tr. 18–19. |
| **Danh sách yêu cầu cần đạt** | [Ma trận đối chiếu yêu cầu](docs/progress/requirements-matrix.md): xem yêu cầu theo mục, trang nguồn, đầu ra và trạng thái. |
| **Đề cương tuần 1** | [PDF để đọc](docs/proposal/proposal.pdf) · [Markdown để sửa](docs/proposal/proposal.md) · [LaTeX sinh tự động](docs/proposal/proposal.tex). |
| **Kế hoạch dữ liệu tuần 1** | [PDF để đọc](docs/proposal/data-plan.pdf) · [Markdown để sửa](docs/proposal/data-plan.md) · [LaTeX sinh tự động](docs/proposal/data-plan.tex). |
| **Chứng minh phần B** | [PDF bản nháp](docs/theory/part-b.pdf) · [Nguồn LaTeX chỉnh trực tiếp](docs/theory/part-b.tex). |
| **Sổ nguồn, mẫu QA, Truyện Kiều và biểu mẫu** | [Mục lục tài liệu dữ liệu](docs/data/README.md), có hướng dẫn mở bộ mẫu và chạy kiểm tra. |
| **Những gì đã làm và chưa làm** | [Bối cảnh và tiến độ](docs/progress/project-context.md) · [Nhật ký hỗ trợ AI](docs/progress/ai-use.md). |

**Trạng thái trong repo:** A.1–A.4 có mã và kiểm số học; [A.2 có PPL validation trên Kaggle](docs/data/char-corpus.md). C.1–C.4 đều có lời giải đã kiểm trên CPU; C.1 và C.4 ghi rõ đầu vào minh họa, còn C.3 ước lượng bộ nhớ chứ không đo peak GPU. Hai hồ sơ tuần 1 và sáu chứng minh B vẫn là bản nháp. [Pilot](docs/data/admin-pilot.md) đã có 20/20 kết luận rà nội dung nhưng 0 QA đủ điều kiện train; chưa có tập SFT chính, test khảo sát, SFT/DPO hay đánh giá ba mô hình. Hai PDF tuần 1 không thay báo cáo cuối LaTeX 25–40 trang.

## Chạy kiểm tra

### A.1 — chạy trên CPU

Từ thư mục gốc, trong môi trường có PyTorch: `python -m unittest discover -s tests -p "test_attention.py" -v`. Để xem dẫn xuất và ví dụ tính tay, chạy tuần tự [notebook A.1](notebooks/01_attention_decoder.ipynb). Trên Colab, dùng CPU, đưa thư mục `src/` và `tests/` của bản repo vào thư mục làm việc; không cần Drive, GPU, dữ liệu QA hoặc cài lại PyTorch.

### A.2 — LM ký tự và perplexity validation

Chạy [notebook A.2](notebooks/04_char_lm.ipynb) trên CPU để kiểm `abc → bcd`, gradient qua decoder A.1, PPL và checkpoint trên dữ liệu minh họa. Lệnh kiểm riêng: `python -m unittest discover -s tests -p "test_char_lm*.py" -v`.

Corpus A.2 dùng **bản Quốc ngữ Trương Vĩnh Ký 1911**, không dùng bản audit `206607`. Xem [dữ liệu và bước xác nhận của nhóm](docs/data/char-corpus.md#4-chuẩn-bị-cục-bộ-và-xác-nhận-quyền) trước khi chạy ô cuối notebook trên Colab GPU. Lệnh tương đương từ gốc repo (đổi `--output` thành đường dẫn bền vững và riêng trên Colab):

```sh
python -m scripts.train_char_lm --manifest .cache/char-corpus/manifest-1911.json --artifact-dir .cache/char-corpus/prepared-1911 --rights-attestation .cache/char-corpus/rights-1911.json --output runs/a2-kieu-1911 --device cuda
```

Giữ cùng cấu hình, hiện vật và thư mục đích; thêm `--resume` sau khi ngắt. `summary.json` tổng hợp PPL validation từng seed 41–45 và trung bình ± SD mẫu. Lệnh không huấn luyện nếu thiếu xác nhận khớp manifest.

Nếu dùng Kaggle, xem [các bước chạy riêng tư và lưu output](docs/data/char-corpus.md#6-chạy-a2-trên-kaggle). Dùng `--platform kaggle` với xác nhận có phạm vi `a2-local-and-kaggle`; xác nhận và gói Colab không đổi.

### A.3 — kiểm LoRA và gộp trọng số trên CPU

Từ thư mục gốc, dùng môi trường A.1: `python -m unittest discover -s tests -p "test_lora.py" -v`. [Notebook A.3](notebooks/03_lora_linear.ipynb) dẫn xuất cập nhật hạng thấp, thực hiện hai bước SGD minh họa và đo sai khác trước/sau gộp. [LoRALinear](src/lora.py) bọc trực tiếp `nn.Linear`; `merged = layer.merge()` trả lớp tuyến tính độc lập để suy luận. Không cần GPU, PEFT hoặc mô hình nền tải ngoài.

### A.4 — kiểm loss DPO trên CPU

Chạy `python -m unittest discover -s tests -p "test_dpo.py" -v` từ thư mục gốc, dùng lại môi trường A.1. [Hàm `dpo_loss`](src/dpo.py) nhận bốn tổng log-xác suất đáp án; [notebook A.4](notebooks/02_dpo_loss.ipynb) dẫn xuất từ Bradley–Terry và kiểm dấu gradient. Các số là minh họa, không cần GPU/cặp ưu tiên thật và không thay phép đối chiếu minibatch ở D.

### C.2 — đếm tham số và phép tính của một Transformer block

Chạy [notebook C.2](notebooks/05_transformer_block_cost.ipynb) trên CPU để đối chiếu công thức với `DecoderBlock` A.1: `numel()` đếm tham số học, PyTorch Profiler đối chiếu FLOP của các tích ma trận forward. Không cần corpus, checkpoint, GPU hoặc huấn luyện lại A.2.

### C.3 — LoRA Q/V và bộ nhớ QLoRA

Chạy tuần tự [notebook C.3](notebooks/06_lora_qlora_cost.ipynb) bằng môi trường PyTorch A.1. Cấu hình Qwen được ghi theo revision cố định; các ô chạy offline, không tải mô hình. Bảng kết quả tách số tham số học, bộ nhớ thường trú và phần phụ thuộc microbatch/độ dài chuỗi. Không dùng các tổng này thay phép đo peak GPU cho D.3.

### D.3 — chuẩn bị SFT trên Kaggle

**Pilot `release-01` trên máy nhóm:** nhóm đã cho phép dùng đúng bản này trên Kaggle Private. Import [notebook đã điền hash](.cache/d3-kaggle/D3-pilot-release-01.ipynb); tạo hai Dataset **Private** từ [ZIP mã](.cache/d3-kaggle/d3-code-14831bf6344b.zip) và [ZIP dữ liệu](.cache/d3-kaggle/d3-release-dd847b1219c4.zip), rồi gắn cả hai vào Notebook **Private** qua **Add Input**. Điền `CODE_INPUT` và `RELEASE_INPUT` bằng **Copy path**; dùng đường dẫn ZIP nếu còn nguyên, hoặc thư mục chứa `scripts/` hay `manifest.json` nếu Kaggle đã giải nén. Giữ `INSTALL_PACKAGES = RUN_TRAIN = False` trong lượt kiểm CPU. Đã kiểm hai ZIP thật tại máy nhóm: `release-valid`, 18 train + 6 validation; chưa chạy GPU.

Các tệp `.cache/` chỉ có ở máy chuẩn bị, không nằm trong Git. Với máy khác có quyền và đúng release, tạo lại hai ZIP theo bước 3 (gói mã: chạy `python scripts/package_d3_kaggle.py` không tham số), dùng [notebook gốc](notebooks/09_d3_sft_kaggle.ipynb) và điền SHA-256 manifest từ máy nhóm.

**Mô hình cho pilot, chưa phải kết luận cho tập chính.** `Qwen/Qwen2.5-1.5B-Instruct`, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`. [Model card đúng revision](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/989aa7980e4cf806f80c7fef2b1adb7bc71aa306/README.md) nêu 1,54B tham số và hỗ trợ tiếng Việt ở phần mô tả đa ngôn ngữ; không phải bằng chứng mô hình trả lời đúng thủ tục Hà Nội. [Apache-2.0 §2, §4](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct/blob/989aa7980e4cf806f80c7fef2b1adb7bc71aa306/LICENSE) cho phép dùng/sửa phục vụ nghiên cứu, có nghĩa vụ nếu phân phối lại; không cấp quyền đối với QA hay khảo sát của nhóm. Dùng [QLoRA NF4](https://github.com/huggingface/transformers/blob/v4.57.6/docs/source/en/quantization/bitsandbytes.md) và [adapter PEFT](https://github.com/huggingface/peft/blob/v0.18.0/docs/source/developer_guides/quantization.md) trên Q/V để đối chiếu thiết kế với C.3.

**Sau kiểm định:**

1. Theo [cổng D.2](docs/data/README.md#2-kiểm-thủ-công-và-phát-hành-bản-sft-nội-bộ): xử lý `rework`/`rejected`, rà nguồn, quyền và trùng nghĩa, lập biên bản thật, chạy `check` với `--review`, `--audit` và `--output`. Chỉ `pilot_sft_ready` mở pilot; `main_sft_ready` mới mở thí nghiệm tập chính. Không đổi nhãn/manifest bằng tay.
2. Kiểm tại máy nhóm: `python scripts/train_d3_sft.py --release <thu-muc-release> --output .cache/d3-check --check-only`. Lấy SHA-256 của **manifest đã phát hành** bằng `Get-FileHash -Algorithm SHA256 <duong-dan-manifest.json>` (PowerShell; dùng chuỗi hex chữ thường). Xác nhận quyền đưa đúng bản lên Kaggle Private, **khác** với quyền huấn luyện nội bộ. Chưa có quyền nền tảng thì giữ dữ liệu trên máy nhóm.
3. Khi có quyền, chạy `python scripts/package_d3_kaggle.py --release <thu-muc-release> --allow-private-kaggle <sha256-chu-thuong>`. Gắn riêng ZIP này vào **Notebook Private**; chỉ có `manifest.json`, `train.jsonl`, `validation.jsonl`. Không gắn cả repo, snapshot, phiếu, audit hay `USER_TEST`. Điền `RELEASE_INPUT` và `MANIFEST_SHA256`; SHA-256 bắt nhầm/sửa file, không xác thực ai đã duyệt.
4. Sau khi cổng đạt, chọn **GPU**, chạy pilot 2 epoch, seed 41. Lưu **Save Version** riêng tư, giữ toàn bộ output. Mở phiên sạch để nối lại từ checkpoint epoch 1 cùng cấu hình; đối chiếu tiến độ và validation với lần chạy liên tục. Ghi tên version Kaggle, release/hash, cấu hình, peak VRAM và chênh lệch quan sát được. Nếu OOM hoặc vượt `MAX_LENGTH`, không cắt mất câu trả lời/căn cứ; điều chỉnh cấu hình và chạy lại với định danh mới. Không dùng kết quả A.2 thay phép đo này.

Trong tab **Output** của version đã lưu, giữ `run_manifest.json` (mã, dữ liệu và môi trường), `metrics.jsonl` (chỉ số từng epoch), `summary.json`, `best_adapter/` và cả thư mục `checkpoints/`. Khi resume, gắn version có toàn bộ checkpoint, không chỉ tải mỗi file trọng số. Nhóm dùng các tệp này để lập model card; giữ riêng tư, không đưa checkpoint vào Git.

**Kế hoạch chọn cấu hình trên tập chính (đề xuất, chưa có kết quả).** Giữ nguyên release, prompt, max length và seed 41. Chạy bốn cấu hình `(r, α, LR)` lần lượt `(8,16,1e-4)`, `(4,16,1e-4)`, `(8,8,1e-4)`, `(8,16,2e-4)`; mỗi cấu hình chấm validation ở cuối epoch 1 và 2. Chọn tổ hợp và epoch có NLL trung bình **theo token đáp án** nhỏ nhất trên cùng validation; nếu bằng nhau ưu tiên ít epoch, rank nhỏ rồi thứ tự trên. Đây là tìm kiếm giới hạn ngân sách, không khẳng định tối ưu toàn cục. Ghi cả các cấu hình thua/OOM; không xem `USER_TEST`. Sáu QA validation của pilot chỉ để thử đường chạy, không chốt siêu tham số từ sáu câu đó.

Với cấu hình và số epoch đã khóa, dùng checkpoint **đúng epoch đã chọn** cho từng seed 41–45; không chọn lại epoch theo từng seed. Báo cả năm lần huấn luyện (có thể tái sử dụng đúng checkpoint seed 41 nếu cấu hình và lịch học khớp), trung bình và SD mẫu. Chỉ chuyển sang sinh cặp D.4 từ adapter SFT thật đã định danh; NLL/PPL không thay đánh giá đúng nội dung, trích dẫn và ảo giác ở D.5.

### Hỏi thử adapter D.3 trên Kaggle Private

Import [notebook hỏi thử](notebooks/10_d3_hoi_thu_kaggle.ipynb) vào notebook **Private** mới. Gắn `D3-code` đã giải nén và output riêng của **lần train liên tục seed 41**. Không cần `D3-Release`, `USER_TEST` hay hồ sơ cá nhân. `RUN_DIR` trỏ đến thư mục có `run_manifest.json`, `summary.json`, `best_adapter/`; `CODE_DIR` trỏ đến thư mục có `src/` và `requirements-d3.txt`. Chọn T4, bật Internet cho mô hình công khai và chạy tuần tự. Notebook chỉ nạp base đã ghim revision và adapter epoch 2 để sinh văn bản, không train/resume hoặc gọi API sinh.

Sau dòng `Sẵn sàng hỏi thử`, đổi chuỗi trong ô `hoi('…')` rồi chạy riêng ô đó. Hai câu minh họa kiểm cách trả lời trong/ngoài phạm vi; đối chiếu văn bản gốc trước khi dùng đáp án. Không tính các câu này là khảo sát, nhãn DPO hoặc kết quả D.5.

### Colab

1. Mở [notebook kiểm tra môi trường](notebooks/00_environment_check.ipynb) bằng Colab, chọn runtime GPU và chạy tuần tự từ phiên sạch. Notebook không cài lại PyTorch hoặc tải mô hình.
2. Đọc trạng thái GPU: `passed` nghĩa là phép tính thử đã chạy; `not_run` không phải đạt. Chạy lại khi đổi phiên. Phiên trước Hà báo T4 15.360 MiB và phép tính CUDA thành công; kết quả đó không chứng minh SFT hoặc DPO vừa bộ nhớ.
3. Lưu báo cáo JSON và danh sách gói trước khi kết thúc phiên. Mặc định chúng nằm trong `/content/environment_checks`; để lưu vào Drive, dùng `MOUNT_DRIVE = True` và chọn `OUTPUT_DIR` dưới `/content/drive/MyDrive/` sau khi cấp quyền. Nếu không dùng Drive thì tải báo cáo xuống.

### Biên dịch và kiểm dữ liệu

- **Hồ sơ tuần 1:** sửa Markdown rồi chạy `python scripts/build_week1_pdfs.py` từ thư mục gốc. Cần Pandoc và Tectonic; xem [hướng dẫn biên dịch](docs/proposal/README.md). Không sửa tay hai tệp LaTeX sinh tự động.
- **Phần B:** sửa nguồn LaTeX trực tiếp. Biên dịch từ thư mục gốc bằng `tectonic --outdir docs/theory docs/theory/part-b.tex` hoặc chạy XeLaTeX hai lượt từ `docs/theory/`.
- **QA và Truyện Kiều:** dùng [các lệnh kiểm trong gói dữ liệu](docs/data/README.md#chạy-lại-kiểm-tra). Kiểm tra tự động không thay kiểm thủ công, và clone repo không có bộ mẫu riêng.

## Quy tắc làm việc trong repo

- **Mã và kết quả:** mã thuật toán dùng lại đặt trong `src/` khi triển khai; notebook điều khiển và giải thích thí nghiệm. Mỗi lần chạy lưu seed, cấu hình, phiên bản mã/dữ liệu/mô hình, môi trường và kết quả. Nếu cần tiếp tục huấn luyện, lưu cả bước hiện tại, trạng thái optimizer, scheduler và bộ sinh số ngẫu nhiên, không chỉ adapter. Kiểm tương thích thư viện trước khi đổi môi trường, không cài lại PyTorch tùy tiện.
- **Dữ liệu riêng:** không đưa token, `.env` chứa bí mật, phiếu đồng ý, dữ liệu định danh, khảo sát thô, test đã khóa, checkpoint, trọng số hay cache lên Git. `data/review/` và `.cache/` bị Git bỏ qua; chỉ nhận bộ mẫu qua kho được phép chia sẻ. Lưu dữ liệu lớn và checkpoint ở kho riêng có kiểm soát, kèm thông tin phiên bản.
- **Chia sẻ repo:** không tự push hoặc công khai. Sáu PDF trong `references/` đã được Git theo dõi; `.gitignore` không gỡ chúng. Kiểm tra quyền phân phối trước khi đẩy hoặc công khai; nếu chưa rõ, chỉ chia sẻ thông tin trích dẫn/đường dẫn theo quyền cho phép.
