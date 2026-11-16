# Nhật ký hỗ trợ AI — nguyên liệu cho phụ lục

Đây là ghi nhận hỗ trợ, không phải xác nhận nhóm đã đáp ứng quy định tài khoản AI. Đề gốc phần II trang2 ghi: “Không dùng bản AI miễn phí”. Nhóm cần bảo đảm công cụ sử dụng phù hợp; không diễn giải quy định này thành cấm Colab miễn phí.

## Phiên chuẩn bị hồ sơ tuần1

- Công cụ: trợ lý lập trình AI trong workspace, có hỗ trợ soạn tài liệu bởi các tác vụ AI song song. Chưa xác minh gói tài khoản/dịch vụ mà nhóm sử dụng.
- Phạm vi: kiểm kê Git/tài liệu; đọc và đối chiếu PDF; soạn bảng yêu cầu, đề cương, kế hoạch dữ liệu, hướng dẫn repo và bối cảnh bàn giao; tạo notebook kiểm tra môi trường; thực thi kiểm tra cục bộ và sửa lỗi ô lưu báo cáo.
- Không thực hiện: khảo sát con người, gán nhãn ưu tiên thật, thu thập mẫu thủ tục, huấn luyện, tạo kết quả đánh giá, thay thế bài giải Q/K/V chính thức.
- Dữ liệu đầu vào: yêu cầu người dùng và sáu PDF có sẵn trong workspace; thông số phiên Colab trước do người dùng cung cấp, không nhận là kết quả agent.
- Trách nhiệm nhóm: đọc lại nguồn, xác minh các giả thiết, lựa chọn phạm vi/mô hình, hiểu và giải thích được code và chứng minh; ghi sửa đổi do thành viên thực hiện, công cụ/phiên bản và phạm vi AI ở các phiên sau. Chưa ghi tên người kiểm duyệt vì chưa có xác nhận.

Khi lập báo cáo cuối, chuyển nhật ký này thành phụ lục khai báo trung thực, bổ sung các lần hỗ trợ về code/chứng minh/dữ liệu và phần đã được con người kiểm chứng. Không ghi “không dùng AI” hoặc coi văn bản AI là nguồn học thuật thay năm bài báo/đề gốc.

## Phiên dàn trang hồ sơ tuần 1

- Hỗ trợ AI: rà soát trạng thái đã chốt/còn mở; chỉnh diễn đạt để không nhầm chấp thuận kế hoạch với kết quả; tạo mẫu LaTeX, bộ lọc Pandoc và script sinh/biên dịch hai PDF từ Markdown.
- Giữ Markdown làm nguồn nội dung; không tạo kết quả khảo sát, huấn luyện hoặc đồng thuận người chấm. Nguồn LaTeX/PDF không phải bằng chứng đã hoàn thành A–D.
- Công cụ biên dịch portable và công cụ kiểm tra PDF được chuẩn bị ngoài repo, tách khỏi môi trường huấn luyện. Bằng chứng biên dịch và giới hạn kiểm tra được cập nhật trong hồ sơ tiến độ sau khi chạy.
- Chưa có xác nhận nhóm đã duyệt nội dung cuối hoặc xác minh loại tài khoản AI; các thành viên vẫn chịu trách nhiệm đọc, hiểu và bảo vệ tài liệu.

## Phiên kiểm chứng dữ liệu tuần 1

- AI nghiên cứu nguồn quốc gia/Hà Nội, kiểm robots/điều khoản, đọc trang động và tệp phụ lục; lưu metadata và snapshot hash. Phát hiện khác biệt thời hạn trích lục, chưa kết luận nguồn nào hiện hành hoặc quyền huấn luyện/phân phối.
- AI biên soạn 20 QA nghiên cứu từ nguồn đã đọc, đối chiếu 21 trích đoạn và chạy kiểm cấu trúc/gate phát hành. Không phải khảo sát thật; số QA được con người phê duyệt vẫn bằng 0. Dữ liệu nháp và trích đoạn giữ ngoài Git.
- AI soạn bộ đồng ý/khảo sát, riêng tư và rubric/phiếu chấm. Chưa mời hoặc thu dữ liệu người tham gia, chưa gán nhãn DPO.
- AI xác minh revision Truyện Kiều, chạy audit kỹ thuật trên nguồn rendered được robots cho phép, tạo corpus/split/vocabulary/windows trong cache với nhãn research-only. API metadata đã được đọc trong bước nghiên cứu trước khi xác định robots chặn `/w/`; sau đó không lặp API/raw, chỉ dùng route `/wiki/` được cho phép. Không che giấu giới hạn này.
- Đã phát hiện, tái hiện và sửa việc theo redirect trước kiểm URL đích trong script corpus; có kiểm thử hồi quy. Không dùng kết quả kiểm kỹ thuật làm xác nhận quyền hoặc thành tích huấn luyện.
- Cập nhật hồ sơ và biên dịch PDF từ Markdown; mọi review quyền, review thủ công, consent và nhãn con người vẫn cần sự kiện thật và audit riêng.
