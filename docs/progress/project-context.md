# Bối cảnh, quyết định và tiến độ

## Phạm vi phiên làm việc

Hồ sơ tuần 1 của Đề tài 9 — Kiến trúc Transformer và tinh chỉnh mô hình ngôn ngữ; trợ lý hỏi đáp thủ tục hành chính công. Không khởi động lại chọn đề tài. Mục tiêu 85–90/100 là định hướng, không bảo đảm. Nhóm dự kiến ba người, hiện dùng Thành viên 1/2/3.

## Kiểm kê ban đầu và nguồn quyết định

Workspace ban đầu chỉ có `.git/` và sáu PDF trong `references/`; không có `AGENTS.md`, code, notebook hoặc tài liệu kế hoạch. Không phát hiện nhiều bản đề trong kiểm kê này. Đề đang dùng: “DANH MỤC BÀI TẬP LỚN CUỐI KÌ MÔN HỌC MÁY CƠ BẢN.pdf”, ngày in trên tài liệu 12/11/2026, 46 trang. Đã đọc phần I, toàn bộ phần II và toàn bộ Đề tài 9. Trang II = 2, Đề tài 9 = 18–19 đúng bối cảnh người dùng. Danh sách và nội dung liên quan của năm bài báo được ghi riêng trong `references/README.md`.

Git ban đầu sạch trên nhánh `main`, có upstream `origin/main`; remote cấu hình `https://github.com/CaoRIV/ml-final-transformer-sft-dpo.git`. Đây là quan sát cấu hình cục bộ, không phải kiểm tra quyền mạng, trạng thái công khai hay cho phép push. Cả sáu PDF đã tracked từ trước. Không commit/push hoặc thay đổi lịch sử trong phiên này. Chưa xác minh quyền phân phối PDF; `.gitignore` mới không gỡ file đã tracked.

## Đã chốt theo người dùng/đề gốc

- Đề tài, ứng dụng, ưu tiên tuần 1; không triển khai PPO hoặc RAG ở giai đoạn này.
- Hai nhánh: Transformer ký tự tự cài đặt và tinh chỉnh mô hình tiền huấn luyện tiếng Việt 0,5–3B.
- Laptop không có GPU đủ mạnh; huấn luyện dự kiến ở Colab T4. Kết quả T4 do người dùng báo, không phải agent đo.
- Giữ code/tài liệu/cấu hình trong một repo; dữ liệu riêng và trọng số nặng không vào Git. Chỉ push sau yêu cầu rõ.
- Theo yêu cầu gốc: A20/B25/C15/D30, báo cáo/tái lập/bảo vệ10; báo cáo cuối LaTeX25–40 trang. Các ngưỡng dữ liệu, kiểm định và yêu cầu đánh giá nằm trong bảng đối chiếu, không được ngầm giảm.

## Đề xuất kỹ thuật, chưa phải phê duyệt của người dùng

- Qwen2.5-1.5B-Instruct là ứng viên, chưa chốt license/revision/tokenizer/config. Ưu tiên pilot QLoRA, không hứa vừa VRAM hay thời gian.
- Dùng DPO loss tự cài đặt ở A để so sánh loss/gradient trên logprob minibatch thật của D; không chỉ so sánh số giả rồi coi đã tích hợp.
- Đề cương khoảng5–7 trang, kế hoạch dữ liệu3–5 trang sau dàn trang; chưa đo số trang Markdown. Mẫu5–10 thủ tục và20–50 QA được kiểm nguồn là mốc nội bộ, chưa thu thập.
- Thiết kế cụ thể và phân công tạm trong hai bản nháp; không thay thế xác nhận của nhóm.

## Vấn đề còn mở

| Vấn đề | Cần làm | Ảnh hưởng |
|---|---|---|
| Phần I nói 2 tuần, phần II có tuần 3 | Hỏi giảng viên; tạm theo phần II, chưa đặt ngày | Lịch nộp |
| Địa phương và nhóm thủ tục | Người dùng chọn phạm vi; sau đó kiểm tra nguồn thực | Mẫu và chiến lược thu thập |
| Khảo sát và người chấm | Xác định nhóm người thật có thể tiếp cận, ít nhất2người chấm độc lập, consent | Test thật và500cặp DPO |
| Model nền, corpus ký tự | Kiểm tra nguồn/license và pilot | Huấn luyện A/D |
| Ngân sách Colab/Drive | Xác nhận khả năng dùng, đường dẫn lưu bền vững | 5 lần chạy và resume |
| Tên/phân công | Nhóm điền sau | Nộp hồ sơ |
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

1. Chốt địa phương, nhóm thủ tục và khả năng khảo sát/chấm độc lập.
2. Kiểm tra điều khoản/robots/nguồn hiện hành, lấy mẫu5–10 thủ tục và20–50QA nếu được phép; lưu URL/thời điểm/hash/đoạn dẫn, kiểm thủ công toàn bộ mẫu.
3. Hoàn thiện hồ sơ tuần1 từ mẫu thực; xác nhận lịch giảng viên.
4. Chạy notebook Colab, lưu báo cáo bền vững; chốt API/package theo tài liệu chính thức rồi pilot SFT và DPO riêng.
5. SFT sơ bộ cần đủ sớm để sinh và chấm dữ liệu DPO trước mốc tuần2; nếu không đạt phải báo rủi ro và xin điều chỉnh, không giả dữ liệu hay âm thầm giảm yêu cầu.
