# Đề tài 9 — Kiến trúc Transformer và tinh chỉnh mô hình ngôn ngữ

Nhóm xây dựng **trợ lý hỏi đáp thủ tục hộ tịch–chứng thực tại Hà Nội**: câu trả lời cần có nguồn để kiểm tra, và trợ lý phải nói rõ khi không đủ căn cứ. Đề gồm hai nhánh: tự viết Transformer nhỏ để hiểu cách mô hình hoạt động (A–C), rồi tinh chỉnh và đánh giá một mô hình tiếng Việt có sẵn cho bài toán thủ tục (D).

**Nhóm:** Cao Văn Hà (trưởng nhóm, tổng hợp và nộp bài), Hà Mạnh Thế, Trần Duy Hưng.

[Đọc theo vai trò](#đọc-theo-vai-trò) · [Hồ sơ và đề gốc](#hồ-sơ-và-đề-gốc) · [Chạy kiểm tra](#chạy-kiểm-tra)

## Bắt đầu ở đây

1. [Giới thiệu bài tập lớn](docs/project-overview.md) — đọc trước để hiểu nhóm xây gì và sẽ đánh giá ra sao; không cần biết trước về Transformer, SFT hay DPO.
2. [Ai làm gì trước?](docs/progress/team-execution-plan.md#2-ai-làm-gì-trước) — tìm tên mình, xem việc cần bắt đầu và kết quả cần giao. [Kế hoạch A–D đầy đủ](docs/progress/team-execution-plan.md) giải thích cách làm và cách kiểm từng mục.
3. [Lịch chuẩn bị vấn đáp 03/12](docs/progress/defense-plan-2026-12-03.md#2-lịch-bàn-giao-nội-bộ) — xem mốc bàn giao và việc mỗi người cần làm. **03/12/2026 là ngày vấn đáp được thông báo cho nhóm; chưa xác nhận đây cũng là hạn nộp cuối.**

## Đọc theo vai trò

Phân công chuyên môn dưới đây là đề xuất; vai trò trưởng nhóm và cách chấm độc lập DPO đã thống nhất.

| Ai | Mở những mục nào? | Việc bắt đầu |
|---|---|---|
| **Thế — cài đặt và bài tập** | [Phần A: cài đặt, dẫn xuất và kiểm chứng](docs/progress/team-execution-plan.md#a--tự-cài-đặt-và-kiểm-chứng-20-điểm-tr-1-và-18) · [Phần C: bốn bài tập](docs/progress/team-execution-plan.md#c--bốn-bài-tính-và-phân-tích-15-điểm-tr-19) · [Bản nháp B](docs/theory/part-b.pdf) | Bắt đầu attention, mặt nạ nhân quả và hàm mất mát DPO bằng ví dụ có kết quả tham chiếu. Bàn giao cả mã, kết quả đối chiếu và ghi chú dẫn xuất; rà B.1–B.3. |
| **Hưng — nguồn, QA và khảo sát** | [Những điểm còn vướng ở nguồn](docs/data/source-audit.md) · [Cách mở và kiểm 20 câu hỏi–đáp nháp](docs/data/admin-pilot.md) · [Phiếu khảo sát và đồng ý](docs/data/consent-and-survey.md) · [Quy trình ẩn danh](docs/data/privacy-workflow.md) | Dẫn cả nhóm kiểm một QA với trang nguồn, ghi câu nào cần sửa hoặc chưa đủ căn cứ. Chốt điều kiện khảo sát trước khi thu và rà B.4–B.6. |
| **Hà — tích hợp, huấn luyện và nộp bài** | [Phần D: dữ liệu đến đánh giá](docs/progress/team-execution-plan.md#d--dữ-liệu-tinh-chỉnh-và-đánh-giá-trợ-lý-30-điểm-tr-19) · [Notebook Colab](notebooks/00_environment_check.ipynb) · [Hồ sơ cần nộp](docs/progress/team-execution-plan.md#5-khi-nào-bàn-giao-và-nộp-gì) | Xác nhận hạn và sản phẩm cần nộp với giảng viên; xin Q/K/V cho C.1 và hỏi cách lấy số C.4. Kiểm môi trường GPU trước khi lên lịch huấn luyện. |

**Cả nhóm:** dùng [bản nháp sáu chứng minh](docs/theory/part-b.pdf) để hỏi chéo, không chỉ đọc phần mình phụ trách. Sau khi có đầu ra SFT thật, Thế và Hưng **đều chấm từng cặp, không xem nhãn của nhau**; Hà phân xử sau khi khóa nhãn và đo đồng thuận. Xem [hướng dẫn chấm](docs/data/annotation-guide.md).

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

**Trạng thái trong repo:** hai hồ sơ tuần 1 và sáu chứng minh là bản nháp. [Báo cáo kiểm mẫu](docs/data/admin-pilot-report.json) ghi **20 QA nháp, 0 QA đủ điều kiện huấn luyện**. Chưa có khảo sát thật, checkpoint SFT/DPO hay kết quả đánh giá. Hai PDF tuần 1 không thay báo cáo cuối LaTeX 25–40 trang.

## Chạy kiểm tra

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
