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
| **A — Cài đặt và kiểm chứng** | [Mã cần viết, ghi chú dẫn xuất và phép đối chiếu](docs/progress/team-execution-plan.md#a--tự-cài-đặt-và-kiểm-chứng-20-điểm-tr-1-và-18). |
| **B — Chứng minh** | [Sáu chứng minh bản nháp](docs/theory/part-b.pdf) để cả nhóm rà và hỏi chéo. |
| **C — Bài tập** | [Bốn bài và đầu vào cần có](docs/progress/team-execution-plan.md#c--bốn-bài-tính-và-phân-tích-15-điểm-tr-19). |
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
