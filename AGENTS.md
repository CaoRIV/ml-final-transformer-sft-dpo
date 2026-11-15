# Hướng dẫn tiếp nối dự án

## Nguồn và phạm vi

- Trao đổi/tài liệu tiếng Việt. Đề tài 9 đã chốt; không chọn lại đề tài.
- Đọc `docs/progress/project-context.md`, bảng yêu cầu, đề cương/kế hoạch dữ liệu và file gốc liên quan trước khi sửa.
- Nguồn ưu tiên: PDF đề trong `references/`, ngày 12/11/2026, 46 trang; phần I tr.1, II tr.2, Đề tài 9 tr.18–19. Không lấy prompt hay kế hoạch thay yêu cầu giảng viên. Ghi rõ bản và trang nếu có bản mới.
- Hiện ưu tiên đề cương/kế hoạch dữ liệu tuần 1, không tự mở rộng giao diện, PPO hay triển khai RAG. RAG chỉ thảo luận mở rộng.
- A/B/C/D lần lượt 20/25/15/30 điểm; báo cáo/tái lập/bảo vệ 10. LaTeX cuối kỳ 25–40 trang, Git/môi trường/script tái lập, datasheet và model card bắt buộc.
- Tạm theo mốc phần II tuần 1/2/3; thời lượng 2 tuần ở phần I cần xác nhận. Không tự đặt hạn nộp.

## Tính trung thực và dữ liệu

- Mọi đề xuất, giả định, lựa chọn chưa chốt phải có nhãn. Không bịa nguồn, QA đã kiểm chứng, khảo sát người thật, điểm người chấm, kết quả huấn luyện hay đồng thuận.
- Phân biệt kiểm tra agent chạy và thông tin người dùng cung cấp. T4/torch/CUDA của phiên trước không phải môi trường hiện tại.
- SFT tối thiểu 2.000 QA có dẫn nguồn, kiểm định thủ công ít nhất 20%; test là câu hỏi khảo sát người thật tách biệt. DPO tối thiểu 500 cặp từ câu trả lời của SFT, mỗi cặp ít nhất hai người chấm độc lập; đo đồng thuận trước phân xử.
- Tôn trọng điều khoản nguồn, robots.txt, giới hạn truy cập. Công khai để đọc không đồng nghĩa được phân phối lại. Dữ liệu con người cần văn bản đồng ý, ẩn danh trước khi lưu dữ liệu nghiên cứu; phiếu đồng ý định danh để riêng, không vào Git.
- Tách train/validation/test và nhóm gần trùng; không dùng test chọn cấu hình. Không dùng AI sinh để thay khảo sát thật.

## Cài đặt và thí nghiệm

- A: PyTorch tự viết attention, multi-head, causal mask, sinusoidal PE, decoder, LM ký tự tiếng Việt giấy phép mở/phạm vi công cộng, LoRA merge, DPO loss. Thư viện chuẩn chỉ là tham chiếu cho phần phải tự viết.
- B: đủ 6 chứng minh với giả thiết/kích thước; mask ảnh hưởng đẳng biến hoán vị; DPO cần beta>0, hỗ trợ phân phối và chuẩn hóa hữu hạn. Log tự nhiên; phân biệt tổng logprob chuỗi DPO và trung bình token perplexity.
- C: Q/K/V chính thức chưa có; dữ liệu minh họa phải gắn nhãn, không thay đề giảng viên.
- D được dùng thư viện; ít nhất một cài đặt A phải dùng/so sánh trong D. Thiết kế hiện đề xuất đối chiếu custom DPO loss và gradient trên minibatch thật.
- Mô hình D 0,5–3B hỗ trợ tiếng Việt, giấy phép nghiên cứu phù hợp. Qwen2.5-1.5B-Instruct chỉ ứng viên; QLoRA ưu tiên đề xuất, chưa đo VRAM SFT/DPO.
- Không cài lại PyTorch tùy tiện. Kiểm tra tài liệu chính thức hiện hành trước khi chọn API/phiên bản. Không giả định quyền Drive/GitHub.
- Cố định seed; ít nhất 5 lần chạy độc lập hoặc 5 fold. Không coi 5 câu sinh từ cùng checkpoint là 5 lần huấn luyện. Ghi rõ đơn vị lặp, SD mẫu, đơn vị lấy mẫu khoảng tin cậy.
- Code dùng lại trong `src/`, notebook điều khiển và giải thích, chạy tuần tự phiên sạch; output gọn, không bí mật. Lưu cấu hình, seed, code revision, data version, model revision, môi trường và kết quả. Checkpoint lưu bền vững và kiểm tra resume thực tế.
- Không hứa DPO tốt hơn SFT. Báo cả kết quả âm, giới hạn, sai số và đánh đổi tính toán.

## Git và bàn giao

- Không ghi đè/xóa công việc hiện hữu. Không tạo cây file rỗng để giả tiến độ.
- Không push, force-push, công khai repo hoặc sửa lịch sử khi chưa có yêu cầu. Remote hiện có không phải quyền push được giao.
- PDF hiện đã tracked; ignore không gỡ được. Quyền phân phối chưa kiểm chứng: không tự xóa, ghi rủi ro và xin quyết định khi cần công khai.
- Không đưa secret, dữ liệu cá nhân/khảo sát thô/consent, checkpoint và mô hình nền vào repo.
- Cập nhật tiến độ theo bằng chứng file/kiểm tra, không đánh dấu yêu cầu thực nghiệm xong vì đã lập kế hoạch.
- Ghi phạm vi hỗ trợ AI vào `docs/progress/ai-use.md` để chuyển sang phụ lục; mỗi thành viên phải hiểu toàn bộ chứng minh/code. Giữ đúng quy định “Không dùng bản AI miễn phí”; không diễn giải thành cấm Colab miễn phí. Chưa xác minh loại tài khoản AI nhóm đang dùng.
