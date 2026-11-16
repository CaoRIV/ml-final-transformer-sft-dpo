# Bối cảnh, quyết định và tiến độ

## Phạm vi phiên làm việc

Hồ sơ tuần 1 của Đề tài 9 — Kiến trúc Transformer và tinh chỉnh mô hình ngôn ngữ; trợ lý hỏi đáp thủ tục hành chính công. Không khởi động lại chọn đề tài. Mục tiêu 85–90/100 là định hướng, không bảo đảm. Nhóm gồm ba sinh viên tại một trường đại học ở Hà Nội: Cao Văn Hà, Hà Mạnh Thế, Trần Duy Hưng. Cao Văn Hà là trưởng nhóm, phụ trách tổng hợp và nộp bài theo xác nhận của người dùng; tên trường và phân công chuyên môn chưa chốt.

## Kiểm kê ban đầu và nguồn quyết định

Workspace ban đầu chỉ có `.git/` và sáu PDF trong `references/`; không có `AGENTS.md`, code, notebook hoặc tài liệu kế hoạch. Không phát hiện nhiều bản đề trong kiểm kê này. Đề đang dùng: “DANH MỤC BÀI TẬP LỚN CUỐI KÌ MÔN HỌC MÁY CƠ BẢN.pdf”, ngày in trên tài liệu 12/11/2026, 46 trang. Đã đọc phần I, toàn bộ phần II và toàn bộ Đề tài 9. Trang II = 2, Đề tài 9 = 18–19 đúng bối cảnh người dùng. Danh sách và nội dung liên quan của năm bài báo được ghi riêng trong `references/README.md`.

Git ban đầu sạch trên nhánh `main`, có upstream `origin/main`; remote cấu hình `https://github.com/CaoRIV/ml-final-transformer-sft-dpo.git`. Đây là quan sát cấu hình cục bộ, không phải kiểm tra quyền mạng, trạng thái công khai hay cho phép push. Cả sáu PDF đã tracked từ trước. Không commit/push hoặc thay đổi lịch sử trong phiên này. Chưa xác minh quyền phân phối PDF; `.gitignore` mới không gỡ file đã tracked.

## Đã chốt theo người dùng/đề gốc

- Đề tài, ứng dụng, ưu tiên tuần 1; không triển khai PPO hoặc RAG ở giai đoạn này.
- Hai nhánh: Transformer ký tự tự cài đặt và tinh chỉnh mô hình tiền huấn luyện tiếng Việt 0,5–3B.
- Laptop không có GPU đủ mạnh; huấn luyện dự kiến ở Colab T4. Kết quả T4 do người dùng báo, không phải agent đo.
- Giữ code/tài liệu/cấu hình trong một repo; dữ liệu riêng và trọng số nặng không vào Git. Chỉ push sau yêu cầu rõ.
- Theo yêu cầu gốc: A20/B25/C15/D30, báo cáo/tái lập/bảo vệ10; báo cáo cuối LaTeX25–40 trang. Các ngưỡng dữ liệu, kiểm định và yêu cầu đánh giá nằm trong bảng đối chiếu, không được ngầm giảm.
- Người dùng đã đồng ý phương án dữ liệu: Hà Nội, hộ tịch–chứng thực; Truyện Kiều cho mô hình ký tự; khảo sát sinh viên/người thân và hai người chấm độc lập là Hà Mạnh Thế, Trần Duy Hưng, với Cao Văn Hà phân xử sau khi khóa nhãn. Chấp thuận phương án không xác nhận đã có dữ liệu, sự đồng ý của người khảo sát hoặc quyền dùng nguồn; các số lượng khảo sát/sinh cặp là mục tiêu vận hành, chưa đo.

## Đề xuất kỹ thuật, chưa phải phê duyệt của người dùng

- Qwen2.5-1.5B-Instruct là ứng viên, chưa chốt license/revision/tokenizer/config. Ưu tiên pilot QLoRA, không hứa vừa VRAM hay thời gian.
- Dùng DPO loss tự cài đặt ở A để so sánh loss/gradient trên logprob minibatch thật của D; không chỉ so sánh số giả rồi coi đã tích hợp.
- Đề cương khoảng5–7 trang, kế hoạch dữ liệu3–5 trang sau dàn trang; chưa đo số trang Markdown. Mẫu5–10 thủ tục và20–50 QA được kiểm nguồn là mốc nội bộ, chưa thu thập.
- Thiết kế cụ thể và phân công tạm trong hai bản nháp; không thay thế xác nhận của nhóm.

## Vấn đề còn mở

| Vấn đề | Cần làm | Ảnh hưởng |
|---|---|---|
| Phần I nói 2 tuần, phần II có tuần 3 | Hỏi giảng viên; tạm theo phần II, chưa đặt ngày | Lịch nộp |
| Danh mục thủ tục và nguồn cụ thể | Phạm vi Hà Nội/hộ tịch–chứng thực đã được đồng ý; kiểm văn bản, hiệu lực, điều khoản và robots trước thu thập | Mẫu và chiến lược thu thập |
| Tổ chức khảo sát và chấm | Phương án người khảo sát/người chấm đã được đồng ý; cần lịch, biểu mẫu đồng ý, quy trình ẩn danh và rubric trước thực hiện | Test thật và 500 cặp DPO |
| Model nền, bản văn ký tự | Model nền còn mở; chọn Truyện Kiều nhưng cần đóng băng bản số hóa, điều kiện sử dụng và hash trước nhập kho | Huấn luyện A/D |
| Ngân sách Colab/Drive | Xác nhận khả năng dùng, đường dẫn lưu bền vững | 5 lần chạy và resume |
| Phân công chuyên môn | Trưởng nhóm và phương án Thế/Hưng chấm độc lập, Hà phân xử đã được đồng ý; còn bố trí lịch và xác nhận phân công chuyên môn | Nộp hồ sơ và tổ chức thực hiện |
| Q,K,V bài C.1 | Xin dữ liệu chính thức giảng viên | Không tự tạo đáp án chính thức |
| Logprob C.4 | Xác nhận bộ số giảng viên yêu cầu nếu có | Không gắn số minh họa thành đề gốc |
| Quyền PDF và remote | Kiểm tra quyền chia sẻ, xác nhận remote trước push | Không công khai ngoài ý muốn |
| Quy định AI | Giữ nguyên “Không dùng bản AI miễn phí”; nhóm xác nhận loại công cụ đang dùng | Liêm chính; không suy ra cấm Colab miễn phí |

## Bằng chứng kiểm tra cục bộ

- Đã kiểm kê và đọc tài liệu gốc nêu trên; chưa thu thập thủ tục, khảo sát, QA, cặp ưu tiên hoặc chạy huấn luyện.
- Đã chạy tuần tự tất cả ô code của `00_environment_check.ipynb` trong một namespace sạch bằng Python3.11.6 trên máy hiện tại; output ghi JSON môi trường và danh sách gói vào thư mục tạm, đọc lại JSON xác nhận tách nguồn bằng chứng. Đã xóa thư mục tạm sau kiểm tra.
- Lần kiểm tra đầu phát hiện lỗi escape xuống dòng trong ô lưu báo cáo; đã sửa và chạy lại thành công.
- Máy hiện tại không có PyTorch trong interpreter kiểm tra; `nvidia-smi` không tìm thấy. Notebook báo `gpu_smoke.status = not_run`, lý do `PyTorch is not installed`; **không có bằng chứng GPU chạy tại máy này**.
- Chưa chạy giao diện Colab, nhánh mount Drive, CUDA hay SFT/DPO. Người dùng cần chạy notebook trong phiên Colab mới. Không cài lại PyTorch trong phiên này.
- Kiểm tra cấu trúc JSON notebook, cell ID duy nhất và output sạch: đạt. Chưa kiểm bằng schema `nbformat` vì thư viện này không có trong interpreter hiện tại.
- Kiểm tra liên kết Markdown cục bộ trong 8 tài liệu: 7 liên kết, không có liên kết trỏ tới file thiếu tại thời điểm kiểm tra.

## Tiến độ và bước tiếp nối

Hồ sơ nháp, bảng đối chiếu, hướng dẫn repo và notebook môi trường là sản phẩm của phiên này; không phải bằng chứng đã hoàn thành A–D. Chưa có datasheet/model card/LaTeX cuối kỳ vì chưa tới giai đoạn và chưa có dữ liệu/mô hình.

1. Cụ thể hóa phạm vi đã đồng ý thành danh mục thủ tục/nguồn; chuẩn bị biểu mẫu đồng ý, khảo sát và hướng dẫn chấm; xác định lịch và trách nhiệm thực hiện.
2. Kiểm tra điều khoản/robots/nguồn hiện hành, lấy mẫu5–10 thủ tục và20–50QA nếu được phép; lưu URL/thời điểm/hash/đoạn dẫn, kiểm thủ công toàn bộ mẫu.
3. Hoàn thiện hồ sơ tuần1 từ mẫu thực; xác nhận lịch giảng viên.
4. Chạy notebook Colab, lưu báo cáo bền vững; chốt API/package theo tài liệu chính thức rồi pilot SFT và DPO riêng.
5. SFT sơ bộ cần đủ sớm để sinh và chấm dữ liệu DPO trước mốc tuần2; nếu không đạt phải báo rủi ro và xin điều chỉnh, không giả dữ liệu hay âm thầm giảm yêu cầu.

## Bàn giao bản LaTeX/PDF tuần 1

- Đã tạo `docs/proposal/proposal.tex` + `proposal.pdf` (**7 trang**) và `data-plan.tex` + `data-plan.pdf` (**11 trang**); cả hai giữ toàn bộ nội dung Markdown, không cắt bảng/schema để ép số trang nội bộ.
- Markdown tiếp tục là nguồn nội dung; `scripts/build_week1_pdfs.py` sinh LaTeX bằng Pandoc và biên dịch bằng Tectonic. Mẫu/bộ lọc và hướng dẫn tái lập nằm trong `docs/proposal/`.
- Đã đồng bộ những đoạn còn nói phạm vi/người chấm chưa được đồng ý; phân biệt chấp thuận kế hoạch với dữ liệu, consent, quyền dùng nguồn và kết quả thực tế.
- Đã biên dịch bằng Pandoc 3.14/Tectonic 0.17.0 portable ngoài repo, xác thực SHA-256 archive theo bản phát hành chính thức. Không cài lại PyTorch; công cụ xem PDF cài vào thư mục riêng ngoài môi trường ML.
- Kiểm tra: đã xem tổng quan mọi trang, chi tiết trang đầu/công thức/bảng; font nhúng; tên tiếng Việt và mục cuối; hash Markdown–LaTeX; không trang trắng hoặc text ngoài khổ giấy. Log cuối không có overfull, thiếu glyph hoặc cảnh báo thay font. Tectonic còn chẩn đoán Fontconfig thiếu cấu hình mặc định, nhưng dùng tệp font bundle chỉ định trực tiếp và thoát mã 0. Chưa kiểm Overleaf/máy khác.
- Đây vẫn là **bản nháp chưa nộp**. Chưa có mẫu thủ tục/QA đã kiểm duyệt, biểu mẫu khảo sát/đồng ý hoàn chỉnh, nguồn được nhập kho hoặc huấn luyện. Biên dịch PDF không thay thế các bằng chứng đó.
