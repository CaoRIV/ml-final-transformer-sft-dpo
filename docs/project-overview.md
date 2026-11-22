# Trợ lý hỏi đáp thủ tục hành chính: nhóm đang làm gì?

*Bài tập lớn môn Học máy cơ bản — Đề tài 9. Nhóm: Cao Văn Hà, Hà Mạnh Thế và Trần Duy Hưng.*

## Bài toán, qua một ví dụ

Bạn muốn chứng thực bản sao một giấy tờ ở Hà Nội nhưng không biết phải chuẩn bị gì. Thay vì tự đọc nhiều trang hướng dẫn, bạn có thể hỏi: **“Tôi muốn chứng thực bản sao một giấy tờ tại Hà Nội. Tôi cần chuẩn bị gì?”**

Trợ lý mà nhóm muốn xây dựng sẽ tóm tắt các giấy tờ và điều kiện liên quan, rồi chỉ ra mục trên trang chính thức để bạn kiểm tra. Nếu thiếu thông tin để xác định trường hợp của bạn, trợ lý cần nói rõ điều còn thiếu; nếu câu hỏi nằm ngoài nhóm thủ tục đã học, nó cần từ chối thay vì đoán. Đây là **ví dụ về cách trợ lý nên hoạt động**, không phải kết quả mô hình đã tạo hay hướng dẫn làm một hồ sơ thật.

Nhóm chỉ tập trung vào **hộ tịch và chứng thực tại Hà Nội**, chẳng hạn cấp bản sao trích lục hộ tịch và chứng thực bản sao. Đây là bài nghiên cứu sinh viên, không phải hệ thống tiếp nhận hồ sơ, dịch vụ tư vấn pháp lý hay nguồn thay thế cơ quan có thẩm quyền. Thủ tục có thể thay đổi; người dùng vẫn cần kiểm tra thông tin mới nhất trên cổng chính thức.

## Nhóm sẽ làm những gì?

**1. Tự xây một mô hình nhỏ để hiểu máy tạo văn bản ra sao.** Nhóm tự viết các bộ phận chính của Transformer bằng Python/PyTorch. Có thể hình dung Transformer vừa đọc một đoạn văn vừa xác định phần nào trong đoạn có ích để đoán phần tiếp theo. Mô hình nhỏ tập đoán **ký tự kế tiếp** trên văn bản tiếng Việt được phép dùng, dự kiến là *Truyện Kiều*. Đây là bài tập để hiểu công nghệ và kiểm tra phép tính, **không phải** mô hình trả lời thủ tục. Nhóm còn phải chứng minh các công thức và làm bài tính tay để kiểm tra lại mã.

**2. Dạy một mô hình tiếng Việt có sẵn cách trả lời thủ tục.** Nhóm dùng mô tả trên cổng dịch vụ công quốc gia và cổng Hà Nội để soạn ít nhất **2.000 cặp câu hỏi–đáp có nguồn**, kiểm thủ công ít nhất **20%**. Mô hình học từ những đáp án mẫu này; bước đó gọi là **SFT** (học từ ví dụ có đáp án). Để giảm bộ nhớ, nhóm dự kiến dùng **LoRA/QLoRA**: chủ yếu huấn luyện các phần bổ sung nhỏ, không cập nhật toàn bộ mô hình.

**3. Dạy mô hình phân biệt câu trả lời tốt và kém.** Với cùng một câu hỏi, mô hình sau SFT tạo hai đáp án. Hai người đọc và chấm độc lập: câu nào đúng hơn, đủ hơn, dẫn nguồn tốt hơn? Đề yêu cầu ít nhất **500 cặp so sánh** như vậy và báo mức độ hai người đồng ý. Mô hình học từ các lựa chọn này qua **DPO** (học từ cặp câu trả lời có ưu tiên). Một phần mã nhóm tự viết ở bước 1 sẽ dùng để kiểm tra phép tính trong bước này.

## Làm sao biết mô hình có tiến bộ?

Nhóm sẽ đặt **cùng bộ câu hỏi** cho ba phiên bản: mô hình gốc, mô hình đã học từ đáp án mẫu, và mô hình học thêm từ lựa chọn của người chấm. Câu hỏi kiểm tra phải do **người thật tự đặt qua khảo sát**, có đồng ý bằng văn bản, đã ẩn danh trước khi lưu dữ liệu nghiên cứu và không đem đi huấn luyện hay chọn cấu hình. Người chấm so sánh hai đáp án mà không biết mô hình nào viết.

Điều quan trọng không phải câu trả lời nghe trôi chảy hay tự tin hơn, mà là **thông tin có đúng nguồn không, có bịa thêm không, và có biết dừng khi không đủ căn cứ không**. DPO có thể giúp hoặc không; nhóm chỉ kết luận sau khi đo. Kết quả cuối cần có báo cáo so sánh, mã và hướng dẫn để người khác kiểm tra lại, không nhất thiết có một ứng dụng web.

## Nhóm đã tới đâu?

Đã có bản nháp đề cương, kế hoạch dữ liệu, sáu chứng minh và **20 câu hỏi–đáp nháp để thử quy trình kiểm nguồn**. Theo báo cáo hiện có, mẫu này mới qua kiểm tra cấu trúc, chưa được con người duyệt và chưa đủ điều kiện huấn luyện. Chưa có kết quả khảo sát hoặc kết quả chứng minh trợ lý trả lời tốt hơn.

Muốn xem cách ba thành viên phối hợp, đọc [kế hoạch thực hiện A–D](progress/team-execution-plan.md). Muốn xem yêu cầu của giảng viên và bằng chứng cần nộp, đọc [bảng đối chiếu yêu cầu](progress/requirements-matrix.md).
