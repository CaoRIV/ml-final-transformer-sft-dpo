# Luồng riêng tư, ẩn danh và bàn giao dữ liệu người

> **Trạng thái:** protocol trước vận hành. Chưa có dữ liệu người tham gia, phiếu consent, token, kho riêng hoặc xác nhận tổ chức. Mọi bảng/ID dưới đây là schema và quy tắc, không phải bản ghi đã tồn tại.

Các gate về kênh thu, quyền truy cập và xác nhận vận hành là thiết kế quản trị nội bộ đề xuất; chúng không phải trích nguyên văn một quy trình phê duyệt đạo đức bắt buộc trong đề gốc. Nhóm cần đối chiếu quy định thực tế của học phần/nhà trường trước khi áp dụng.

## 1. Nguyên tắc và ranh giới

`USER_TEST` chỉ có thể hình thành từ câu hỏi người dùng thực sau consent hợp lệ. Nó không phải nguồn để viết QA, train SFT, tạo DPO, tune prompt hay chọn siêu tham số. Mục đích duy nhất là test/evaluation đã khóa của bài tập lớn; công bố chỉ ở dạng tổng hợp hoặc trích dẫn đã ẩn danh, sau review.

Quy trình áp dụng các nguyên tắc sau:

- **Tối thiểu dữ liệu:** không thu tên, email, số điện thoại, mã sinh viên, địa chỉ, tuổi chính xác, số hồ sơ/giấy tờ, ảnh giấy tờ, tài khoản mạng xã hội, dữ liệu sức khỏe/tài chính hay thông tin nhận diện tương tự trong khảo sát.
- **Tách lớp:** consent có chữ ký (nếu hình thức đã được phê duyệt yêu cầu), sổ liên kết token và câu hỏi đã redaction không cùng tệp/thư mục/quyền truy cập. Dataset nghiên cứu không chứa định danh trực tiếp.
- **Không tạo vết số hóa sớm:** không dùng form công khai, Google Forms, Microsoft Forms, chatbot, API hoặc kênh có autosave để nhận câu trả lời. Ưu tiên phiếu giấy/phỏng vấn tại chỗ; chỉ bản đã redaction mới được nhập kho nghiên cứu.
- **Giới hạn mục đích:** không dùng câu hỏi để đánh giá con người, liên hệ lại, tuyển dụng, quảng cáo, tư vấn cá nhân, cá nhân hóa hoặc ngoài bài tập lớn. Không công bố nhóm người tham gia “thật” hay thuộc tính nhóm nếu chưa có dữ liệu hợp lệ và đánh giá nguy cơ tái nhận diện.
- **Không hứa sai về ẩn danh:** trước khi hủy sổ liên kết, token có thể nối một phiếu khảo sát với phiếu consent riêng; đó là pseudonymous trong phạm vi vận hành, không phải “vô danh tuyệt đối”. Sau khi hủy liên kết, dữ liệu nghiên cứu không còn cách hợp lý để tái nhận diện theo protocol này.
- **Không có dữ liệu người trong Git:** repository chỉ chứa protocol, schema rỗng và mã xử lý không nhạy cảm. Không commit phiếu, scan, ảnh, nhật ký token, câu hỏi thô, câu hỏi đã redaction, hash có thể làm định danh đơn lẻ, hoặc export dữ liệu.

## 2. Mô hình dữ liệu và quyền truy cập

| Lớp | Nội dung được phép | Vị trí/biện pháp | Người được truy cập | Tuyệt đối không được làm |
|---|---|---|---|---|
| L0 — phiếu consent | Văn bản consent, chữ ký/đánh dấu nếu đã phê duyệt, token, ngày phiên | Bản giấy khóa vật lý **hoặc** kho riêng mã hóa ngoài Git | Cao Văn Hà và người được xác nhận tối thiểu theo quy định của giảng viên/nhà trường | Không scan vào repo, không gửi người chấm, không nhập vào dataset |
| L1 — sổ liên kết | Token ↔ vị trí phiếu consent; trạng thái/rút, không thêm liên hệ nếu không bắt buộc | Kho riêng mã hóa, tách L0/L2 | Cao Văn Hà | Không dùng để ghép câu trả lời với danh tính sau mốc hủy liên kết |
| L2 — vùng redaction tạm | Phiếu câu hỏi có token, chỉ trong lúc lọc PII | Khóa vật lý/kho riêng mã hóa; xóa/hủy theo lịch | Người nhập liệu được giao và người kiểm redaction | Không gửi API/AI, chat, email hay storage công khai |
| L3 — `USER_TEST` đã redaction | Câu hỏi sạch, ID ngẫu nhiên, nhóm thủ tục thô, audit tối thiểu | Kho dữ liệu riêng mã hóa ngoài Git | Evaluator được chỉ định sau khi test bị khóa | Không đưa người author QA, người tune hoặc rater DPO truy cập trước tổng kết |
| L4 — báo cáo | Count tổng hợp, phương pháp, chỉ số; ví dụ chỉ khi đã kiểm nguy cơ | Kho báo cáo/repo khi được phép | Nhóm nộp bài | Không công bố raw question, token, nhóm nhỏ có thể nhận diện, phiếu consent |

Cao Văn Hà là đầu mối phụ trách lưu trữ và bàn giao theo vai trò đã thống nhất, không phải chủ sở hữu dữ liệu để dùng ngoài mục đích đã nêu. Hà Mạnh Thế và Trần Duy Hưng chấm preference DPO trên dữ liệu nguồn/SFT; họ không nhận L0–L2 và không xem `USER_TEST` trước khi protocol đánh giá yêu cầu.

## 3. Luồng thực thi bắt buộc

### 3.1. Gate trước thu thập

Trước bất cứ lần mời/phiên nào, lập checklist riêng với kết quả `pass`, `not_pass` hoặc `not_applicable`; không thay `not_pass` bằng mô tả miệng.

| Gate | Tiêu chí pass | Nếu không pass |
|---|---|---|
| G-01: xác nhận tổ chức | Giảng viên/đơn vị có thẩm quyền xác nhận hình thức written/electronic consent, đối tượng ≥18, kênh liên hệ và quy tắc áp dụng | Không mở khảo sát; không suy diễn consent mẫu này có hiệu lực pháp lý |
| G-02: kênh thu | Chỉ định phiếu giấy/phỏng vấn không autosave; không có form/API công khai | Không thay tạm bằng Google Forms hay link chat |
| G-03: lưu trữ | L0–L3 tồn tại ngoài Git, mã hóa/khóa, có quyền theo vai trò và quy trình xóa | Không phát phiếu/không nhận câu hỏi |
| G-04: staff handoff | Người hướng dẫn, người nhập liệu và người kiểm redaction đã nhận bản `CONSENT-v1.0`/`SURVEY-v1.0` và quy tắc PII | Không giao việc tự phát hoặc tự động hóa thu thập |
| G-05: mốc rút | Nhóm chốt và thông báo ngày đóng liên kết, cách token được dùng, hành động sau mốc | Không hứa có thể xóa sau khi đã vô danh hóa |
| G-06: test firewall | Kho `USER_TEST` và ACL đã tách khỏi authoring/SFT/DPO/tuning; cách khóa split đã xác định | Không ingest dữ liệu người vào kho chung |

Chỉ consent **bằng văn bản/điện tử theo hình thức G-01 đã xác nhận** mới đủ điều kiện. Một checkbox trong công cụ chưa được phê duyệt không tự làm cho consent hợp lệ.

### 3.2. Từ người tham gia đến record nghiên cứu

1. Người hướng dẫn phát văn bản consent, xác nhận người tham gia tự xác nhận từ đủ 18 tuổi và cho phép từ chối/dừng không bất lợi. Không hỏi lý do từ chối.
2. Sau khi họ chọn đồng ý, cấp một `respondent_cluster_id` là token ngẫu nhiên. Token được dùng cho tối đa ba câu hỏi của cùng người để khai báo cụm bootstrap, không dùng làm profile.
3. Thu phiếu survey tách với phiếu consent. Người hướng dẫn kiểm nhanh PII trước khi nhận; câu có PII được người tham gia tự sửa hoặc bị loại. Không chụp hay nhập bản thô.
4. Người nhập liệu chép vào L2, loại PII thêm một lần, rồi tạo record L3 chỉ khi người kiểm redaction xác nhận. Nếu không thể giữ nghĩa sau redaction, hủy câu hỏi; không suy đoán/thay chữ giúp người tham gia.
5. Từ L3, gán `test_split_status = heldout`; tạo manifest riêng hạn chế truy cập. Không tạo QA, paraphrase, candidate DPO hoặc few-shot prompt từ nó.
6. Xử lý yêu cầu rút bằng token trong thời hạn. Xóa/hủy mọi phần L2/L3 khớp token và ghi audit hành động ở L1; không lưu lý do rút trong dataset.
7. Đến ngày đóng liên kết, sau khi xử lý yêu cầu còn lại, hủy L1 theo cách khiến token L3 không thể nối tới người. Từ đó cấm trả lời yêu cầu truy xuất/xóa theo cá nhân bằng một lời hứa không thực hiện được; vẫn tiếp nhận phản ánh qua kênh chính thức đã xác nhận.

Không có bước nào tạo record `granted`, `heldout`, `withdrawn` hay `redacted` nếu sự kiện thật chưa xảy ra. Schema không phải dữ liệu.

## 4. Schema tối thiểu và quy tắc bất biến

Các schema này tồn tại để triển khai kho riêng, không phải file dữ liệu trong repository.

### 4.1. Record nghiên cứu `user_survey_record`

| Trường | Kiểu/giá trị cho phép | Quy tắc riêng tư |
|---|---|---|
| `survey_question_id` | UUID ngẫu nhiên, bất biến | Một ID cho một câu hỏi được chấp nhận sau redaction |
| `respondent_cluster_id` | token UUID ngẫu nhiên | Không dẫn xuất từ danh tính; dùng duy nhất cho grouping/bootstrap |
| `consent_version` | string, ví dụ version văn bản đang dùng | Không chứa tên/chữ ký |
| `consent_status` | `granted` hoặc `withdrawn` | Chỉ `granted` mới được nhập L3; không tạo giá trị giả |
| `consented_at` / `withdrawn_at` | ISO-8601 hoặc null | Chỉ thời điểm vận hành tối thiểu; không thay thế phiếu consent |
| `question_text_redacted` | text | Đã loại PII; nếu không làm sạch được thì không có record |
| `hanoi_relation` | `yes`, `no`, `unknown`, `not_answered` | Phân loại do người tham gia chọn, không suy diễn địa chỉ |
| `scope_group` | enum/thẻ nhóm thủ tục thô | Không ghi hồ sơ/cơ quan/địa chỉ cụ thể |
| `survey_channel` | `paper_in_person` hoặc `interview_in_person` | Không lưu địa điểm/lớp/đơn vị chi tiết |
| `redaction_status` | `approved` hoặc `rejected` | L3 chỉ giữ `approved`; reason riêng không chứa PII nếu cần audit |
| `redaction_reviewer_id` | ID vai trò/pseudonymous | Không dùng danh tính người tham gia |
| `test_split_status` | `heldout` hoặc `excluded` | Bất biến sau khóa, trừ removal do rút/vi phạm privacy |
| `dataset_version`, `created_at` | version/timestamp | Audit release; không là định danh người |

Không giữ `human_status`, `participant_name`, `email`, `phone`, `student_id`, `signature`, `consent_scan`, `raw_question`, `contact_details` hoặc trường tương đương trong record nghiên cứu. `consent_status` chỉ là trạng thái dựa trên sự kiện thực, không phải chứng nhận rằng một người tồn tại.

### 4.2. Audit redaction riêng

Audit tối thiểu chỉ giữ `survey_question_id`, người xử lý theo ID vai trò, thời điểm, hành động (`approved`, `rework`, `rejected`, `withdrawn_removed`) và mã lý do chuẩn hóa. Ví dụ mã lý do: `direct_identifier`, `case_number`, `document_image`, `third_party_identifier`, `meaning_lost_after_redaction`. Không chép lại PII vào lý do.

Mọi sửa nội dung sau `approved` phải sinh phiên bản mới, lưu hash/nguồn thay đổi trong kho riêng, và review redaction lại. Không sửa im lặng để phù hợp mô hình.

## 5. Xử lý sự cố và yêu cầu rút

| Tình huống | Hành động ngay | Hành động tiếp theo |
|---|---|---|
| Người tham gia ghi PII trên phiếu | Không số hóa/copy; đề nghị người đó tự bỏ hoặc hủy câu | Nếu không làm sạch được, tiêu hủy câu hỏi theo cách an toàn |
| Phiếu/ảnh vô tình vào thiết bị/kênh không được phép | Dừng nhập liệu; hạn chế truy cập; báo Cao Văn Hà và kênh tổ chức đã xác nhận | Xử lý theo quy định đã được xác nhận; không che giấu hoặc commit vào Git |
| Token yêu cầu rút trước mốc | Đối chiếu L1 riêng, tạm khóa record liên quan | Hủy L2/L3 liên quan, cập nhật audit, xác nhận qua kênh chính thức nếu có thể |
| Mất khả năng bảo đảm tách quyền | Dừng truy cập/đánh giá `USER_TEST` | Khôi phục ACL/kho trước khi tiếp tục; nếu không, loại dữ liệu khỏi nghiên cứu |
| Nhận câu hỏi ngoài phạm vi hoặc không đủ căn cứ | Giữ `heldout` chỉ nếu đã sạch và consent hợp lệ; không dùng để bổ sung train | Protocol đánh giá có thể chấm khả năng từ chối; không biến thành QA authored |

## 6. Giữ, hủy và công bố

Thời hạn giữ phải được chốt cùng G-01 trước khi mở khảo sát; tài liệu này không tự đặt một thời hạn. Khi kết thúc mục đích môn học hoặc đến mốc hủy đã được phê duyệt, Cao Văn Hà thực hiện hủy L0–L3 theo lịch riêng và ghi chỉ bằng chứng tối thiểu về hành động hủy, không ghi PII vào repo.

Trước mọi ví dụ câu hỏi trong báo cáo, người phụ trách riêng tư kiểm tra lại: (a) không còn PII hoặc tổ hợp chi tiết có thể nhận diện, (b) không tiết lộ token, consent, kênh/địa điểm cụ thể, (c) không làm lộ người thứ ba, và (d) công bố có cần thiết không. Nếu không vượt được kiểm tra, chỉ báo cáo aggregate hoặc không công bố ví dụ.

## 7. Bàn giao thủ công trước khi dùng bản nháp

Trước ngày hoạt động thật, Cao Văn Hà cần nhận bàn giao có xác nhận từ cả nhóm về: phiên bản form; gate G-01…G-06; lịch/địa điểm/kênh được phê duyệt; người hướng dẫn; người nhập và kiểm redaction; mốc rút; vị trí L0–L3; quyền truy cập; quy trình hủy và báo sự cố. Hà Mạnh Thế và Trần Duy Hưng cần xác nhận riêng rằng họ chỉ nhận dữ liệu DPO được phân quyền, không nhận consent/survey raw.

Đây là checklist giao việc thủ công, không phải ủy quyền tự động thu người tham gia. Chỉ sau approvals vận hành thực tế, bản nháp có thể được dùng; không có “mock pass”, record mẫu hay báo cáo thành công thay thế cho approvals.