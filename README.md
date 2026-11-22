# Đề tài 9 — Kiến trúc Transformer và tinh chỉnh mô hình ngôn ngữ

Ứng dụng: trợ lý hỏi đáp thủ tục hành chính công. Giai đoạn hiện tại: **hồ sơ tuần 1**. Đã có audit nguồn, 20 QA nháp nghiên cứu và audit corpus ký tự; chưa có dữ liệu được con người phê duyệt cho huấn luyện, khảo sát thật, checkpoint hoặc kết quả đánh giá. Mục tiêu làm việc 85–90/100, không phải cam kết điểm.

## Đọc hồ sơ

- [Giới thiệu bài tập lớn cho người mới](docs/project-overview.md): bài toán, cách nhóm dạy mô hình và cách kiểm tra kết quả qua ví dụ.
- [Kế hoạch tới buổi vấn đáp 03/12](docs/progress/defense-plan-2026-12-03.md): lịch bàn giao, điều kiện mở rộng phần D và phương án nếu không kịp.
- [Kế hoạch phối hợp của Hà, Hưng và Thế](docs/progress/team-execution-plan.md): đầu vào, đầu ra, cách làm, nghiệm thu và bàn giao A–D.
- [Kiểm kê và tài liệu gốc](references/README.md).
- [Bảng đối chiếu yêu cầu](docs/progress/requirements-matrix.md).
- [Bối cảnh, quyết định, tiến độ](docs/progress/project-context.md).
- Đề cương tuần 1: [Markdown](docs/proposal/proposal.md), [PDF](docs/proposal/proposal.pdf), [LaTeX](docs/proposal/proposal.tex).
- Kế hoạch dữ liệu: [Markdown](docs/proposal/data-plan.md), [PDF](docs/proposal/data-plan.pdf), [LaTeX](docs/proposal/data-plan.tex).
- Phần B — sáu chứng minh: [LaTeX](docs/theory/part-b.tex), [PDF](docs/theory/part-b.pdf). Bản nháp để nhóm rà soát; biên dịch từ thư mục gốc với `tectonic --outdir docs/theory docs/theory/part-b.tex`, hoặc dùng XeLaTeX hai lượt từ `docs/theory/`. Tệp `.tex` là nguồn chỉnh sửa trực tiếp.
- [Nhật ký hỗ trợ AI](docs/progress/ai-use.md).
- [Gói kiểm chứng dữ liệu tuần 1](docs/data/README.md): sổ nguồn, pilot QA, audit Truyện Kiều, biểu mẫu khảo sát và hướng dẫn chấm.

Đề gốc ngày 12/11/2026: phần II trang 2; Đề tài 9 trang 18–19. Mốc tuần 3 ở phần II mâu thuẫn thời lượng 2 tuần ở phần I. Người dùng báo vấn đáp ngày 03/12/2026; vẫn cần xác nhận đây có đồng thời là hạn nộp cuối và giảng viên yêu cầu bàn giao gì tại buổi đó.

Hai PDF là bản nháp giữ đầy đủ nội dung Markdown, có kết quả audit nghiên cứu nhưng chưa xác nhận dữ liệu đủ điều kiện huấn luyện hoặc đã nộp. [Hướng dẫn biên dịch lại](docs/proposal/README.md) bằng `python scripts/build_week1_pdfs.py` (cần Pandoc và Tectonic). Markdown là nguồn nội dung; không sửa tay hai tệp LaTeX sinh tự động.

## Kiểm tra môi trường Colab

1. Mở `notebooks/00_environment_check.ipynb` bằng Colab, chọn runtime GPU.
2. Chạy tuần tự từ phiên sạch. Notebook không cài hoặc nâng cấp PyTorch, không tải mô hình.
3. Ô đầu cấu hình mặc định lưu báo cáo trong `/content/environment_checks` (tạm thời). Để lưu bền vững, đặt `MOUNT_DRIVE = True` và `OUTPUT_DIR` thành thư mục dưới `/content/drive/MyDrive/`; chạy ô mount và chấp thuận quyền trong Colab. Chưa giả định agent có quyền Drive.
4. Sau khi chạy, lưu JSON và tệp phiên bản gói từ thư mục in ra. Nếu không mount Drive, tải chúng xuống trước khi phiên kết thúc.
5. GPU smoke test phải báo `passed`; kết quả `not_run` không phải GPU đạt. Chạy lại notebook khi đổi phiên Colab.

Notebook dùng thư viện chuẩn Python và PyTorch có sẵn. Chưa chốt môi trường huấn luyện nên chưa tạo `requirements.txt` giả định phiên bản. Trước khi cài Transformers/PEFT/TRL/bitsandbytes phải kiểm tra tài liệu chính thức và tương thích môi trường đo thực tế. Kiểm tra này **không chứng minh SFT hay DPO vừa VRAM**.

Thông tin người dùng đã cung cấp từ một phiên trước: Tesla T4, 15.360 MiB (15 GiB), PyTorch `2.14.1+cu130`, CUDA của PyTorch `13.0`, CUDA khả dụng và nhân ma trận thành công. Đây không phải kết quả agent chạy và không áp đặt cho phiên sau.

## Tổ chức theo giai đoạn

Hiện có `references/`, `docs/proposal/`, `docs/progress/`, `docs/data/`, `notebooks/`, các script build/kiểm dữ liệu trong `scripts/` và kiểm thử hồi quy trong `tests/`. QA/trích đoạn nghiên cứu chưa được duyệt ở `data/review/`, corpus/bản nguồn ở `.cache/`, đều bị Git bỏ qua. Khi bắt đầu cài thuật toán, mã dùng lại vào `src/`; notebook điều khiển thí nghiệm, không sao chép thuật toán. Chỉ bổ sung cấu hình/huấn luyện/kết quả/LaTeX cuối kỳ khi có công việc thực, không tạo thư mục rỗng.

## Git, dữ liệu và quyền phân phối

Repository đã có Git và remote `origin` cấu hình; chưa xác minh quyền truy cập hoặc trạng thái công khai. Không push nếu chưa được yêu cầu và xác nhận remote. Sáu PDF đã được Git theo dõi từ trước: `.gitignore` không gỡ chúng và không xóa lịch sử. **Cần kiểm tra quyền phân phối trước lần công khai/push tiếp theo**; nếu chưa rõ, giữ riêng và chia sẻ thông tin trích dẫn/đường dẫn thay vì PDF. Không tự xóa công việc hiện hữu.

Không commit token, `.env`, dữ liệu định danh, phiếu đồng ý, câu hỏi khảo sát thô, checkpoint, trọng số, cache. Dữ liệu lớn/checkpoint ở Drive hoặc kho riêng có kiểm soát, có manifest phiên bản và hướng dẫn lấy lại khi được phép. Chỉ dữ liệu mẫu đã ẩn danh, có quyền chia sẻ mới đưa vào `data/samples/`.

Mỗi thí nghiệm về sau phải lưu seed, cấu hình, phiên bản code/dữ liệu/mô hình, môi trường và kết quả; checkpoint tiếp tục huấn luyện phải có cả trạng thái optimizer, scheduler, bước hiện tại và RNG, không chỉ adapter.
