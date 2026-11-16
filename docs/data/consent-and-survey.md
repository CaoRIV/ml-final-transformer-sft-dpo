# Đồng ý tham gia và khảo sát câu hỏi người dùng

> **Trạng thái:** biểu mẫu và quy trình vận hành trước thu thập; không phải bằng chứng đã mời, đã có consent hoặc đã nhận bất kỳ câu trả lời nào. Không đưa phiếu đã ký, token đã cấp, câu hỏi thô hay dữ liệu người tham gia vào Git.

Các gate vận hành dưới đây là biện pháp quản trị nội bộ của bản nháp để nhóm xác nhận quy định áp dụng; không khẳng định đề bài đã yêu cầu một quy trình phê duyệt đạo đức riêng ngoài văn bản đồng ý và bảo vệ dữ liệu. Không coi tài liệu này là tư vấn hoặc xác nhận tuân thủ pháp lý.

## 1. Điều kiện được phép mở khảo sát

Không mời người tham gia, không phát phiếu, không tạo biểu mẫu trực tuyến công khai và không nhập câu hỏi vào hệ thống nghiên cứu cho đến khi **tất cả** điều kiện sau được ghi nhận trong sổ vận hành riêng ngoài Git:

1. Giảng viên hoặc đơn vị/nhà trường có thẩm quyền đã xác nhận hình thức đồng ý bằng văn bản hoặc điện tử được dùng cho môn học/nghiên cứu này, phạm vi người tham gia và kênh liên hệ khiếu nại. Hiện chưa có xác nhận đó; tài liệu này không khẳng định đã đáp ứng yêu cầu pháp lý hay quy chế nội bộ.
2. Nhóm xác nhận phạm vi khảo sát chỉ là câu hỏi thông tin chung về thủ tục hộ tịch–chứng thực tại Hà Nội, phương án lưu trữ mã hóa ngoài Git, và đầu mối theo **vai trò** để người tham gia hỏi/rút dữ liệu. Không tự ghi tên trường, email, số điện thoại hoặc đường dẫn biểu mẫu khi chưa được xác nhận.
3. Cao Văn Hà, với vai trò phụ trách lưu trữ vận hành, đã tạo kho riêng mã hóa và sổ token; Hà Mạnh Thế và Trần Duy Hưng không cần truy cập phiếu consent hay bảng liên kết định danh để chấm DPO.
4. Nhóm đã thống nhất lịch, địa điểm/kênh được phép, người hướng dẫn phiên khảo sát và ngày “đóng liên kết rút”. Lịch chỉ được ghi vào sổ vận hành riêng sau khi có xác nhận ở mục 1.
5. Người hướng dẫn đã đọc quy trình xử lý câu trả lời vô tình có thông tin cá nhân ở mục 5 và có bản giấy của văn bản bên dưới. Không dùng Google Forms, Microsoft Forms, form công khai, chatbot hay API bên thứ ba để thu câu trả lời trong protocol này: các hệ thống đó có thể tự lưu bản nháp/autosave trước khi nhóm kiểm tra ẩn danh.

Nếu một điều kiện không đạt, trạng thái là **chưa mở khảo sát**. Có thể tiếp tục chuẩn bị tài liệu, nhưng không được coi đó là pilot hay thu thập thực tế.

## 2. Hình thức thu thập được khuyến nghị

Mặc định dùng **phiếu giấy tại chỗ hoặc phỏng vấn có người ghi phiếu**. Người tham gia tự đọc văn bản đồng ý; nếu đồng ý, họ ký/đánh dấu trên phiếu consent tách riêng và nhận một token ngẫu nhiên. Phiếu khảo sát chỉ mang token đó, không mang tên hay chữ ký. Khi phỏng vấn, người ghi đọc nguyên văn câu hỏi, ghi đúng ý người tham gia và không hỏi thêm thông tin nhận diện.

- Token gồm mã ngẫu nhiên do nhóm tạo trước phiên; một người chỉ dùng một `respondent_cluster_id` cho tất cả câu hỏi họ tự nguyện cung cấp. Token không mã hóa tên, thời gian sinh, lớp, số điện thoại hay địa chỉ.
- Phiếu consent có thể giữ token để phục vụ rút dữ liệu trong thời hạn đã công bố. Phiếu này và sổ liên kết token–phiếu consent là hồ sơ riêng mã hóa/khóa vật lý, không được nhập vào dataset, không gửi cho người chấm, không dùng để huấn luyện, và không vào Git.
- Phiếu khảo sát không hỏi, không ghi và không để người hướng dẫn tự điền tên, email, số điện thoại, mã sinh viên, địa chỉ, số hồ sơ, số giấy tờ, ảnh/chụp giấy tờ, tình trạng sức khỏe/tài chính hay thông tin định danh tương tự.
- Sau khi hết thời hạn rút và đã xử lý các yêu cầu hợp lệ, người phụ trách hủy sổ liên kết token–consent. Bản ghi nghiên cứu còn lại chỉ có token cụm ngẫu nhiên và câu hỏi đã redaction; khi đó không thể truy lại người cụ thể. Đây là lý do không thể hứa xóa một câu hỏi theo cá nhân sau mốc này.

Không mặc định người quen, sinh viên trong lớp, thành viên câu lạc bộ hoặc người thân là đã đồng ý. Không có điểm, quà, ưu tiên học tập, phạt, áp lực từ giảng viên/nhóm hay lợi ích vật chất nào gắn với việc tham gia hoặc từ chối.

## 3. Văn bản thông tin và đồng ý — bản người tham gia đọc

Nội dung dưới đây phải được phát/đọc nguyên văn trước khi có câu trả lời khảo sát. Chỉ thay thông tin liên hệ bằng **kênh chính thức đã được giảng viên/nhà trường xác nhận**, không tự tạo liên hệ giả.

---

### Thông tin dành cho người tham gia

**Tên hoạt động:** Khảo sát câu hỏi người dùng cho bài tập lớn về trợ lý hỏi đáp thủ tục hành chính công.

**Mục đích:** Nhóm thực hiện bài tập lớn muốn hiểu người dùng từ 18 tuổi trở lên thường muốn hỏi gì về một số thủ tục hộ tịch và chứng thực tại Hà Nội. Các câu hỏi hợp lệ, sau khi đã loại thông tin riêng tư, có thể chỉ được dùng làm tập kiểm tra tách biệt để đánh giá mô hình trả lời câu hỏi. Hoạt động này không tư vấn pháp lý, không giải quyết hồ sơ và không thay thế cơ quan có thẩm quyền.
**Quy mô dự kiến:** Nhóm đặt mục tiêu vận hành ban đầu mời khoảng **50–80** người, nhưng đây chỉ là mục tiêu kế hoạch, không phải chỉ tiêu bắt buộc, không bảo đảm đủ người và không là lý do gây áp lực để bạn tham gia hoặc trả lời đủ câu hỏi.


**Bạn sẽ làm gì:** Nếu đồng ý, bạn có thể cho biết câu hỏi bạn thực sự muốn tìm hiểu. Bạn có thể viết hoặc nói **0, 1, 2, hoặc 3 câu hỏi**; không bắt buộc phải đủ 2–3 câu. Không có câu trả lời “đúng”. Xin không ghi tên, thông tin liên hệ, số hồ sơ, số giấy tờ, địa chỉ cụ thể, ảnh giấy tờ hoặc thông tin riêng tư của bạn/người khác.

**Điều kiện tham gia:** Chỉ người từ đủ 18 tuổi trở lên mới được tham gia. Việc tham gia hoàn toàn tự nguyện. Bạn có thể không tham gia, bỏ qua bất kỳ mục nào, hoặc dừng bất kỳ lúc nào trước khi nộp phiếu mà không bị bất lợi, không ảnh hưởng điểm số, quan hệ học tập/công việc hay bất kỳ quyền lợi nào. Không có thù lao, điểm thưởng hoặc hình thức ép buộc.

**Cách dữ liệu được xử lý:** Phiếu khảo sát dùng một mã ngẫu nhiên, không dùng tên. Trước khi được nhập vào dữ liệu nghiên cứu, nhóm sẽ kiểm tra và xóa/che thông tin nhận diện; câu hỏi không thể làm sạch mà vẫn giữ nghĩa sẽ bị loại. Câu hỏi đã làm sạch có thể được xử lý bằng phần mềm và mô hình AI/ngôn ngữ để đánh giá nghiên cứu. Nhóm không gửi câu hỏi thô hoặc câu hỏi còn chi tiết riêng tư vào API/dịch vụ AI bên ngoài. Không dùng dữ liệu này để nhận diện, quảng cáo, chấm điểm hay ra quyết định về bạn.

**Lưu trữ và công bố:** Phiếu đồng ý có chữ ký (nếu được dùng) và sổ liên kết mã được lưu tách biệt, riêng tư, mã hóa hoặc khóa vật lý ngoài Git. Dữ liệu nghiên cứu đã làm sạch được giới hạn truy cập theo vai trò. Báo cáo, trình bày hoặc phát hành chỉ dùng số liệu tổng hợp và/hoặc ví dụ đã ẩn danh sau khi kiểm tra; không công bố tên, thông tin liên hệ hay phiếu của bạn. Nhóm không hứa công bố dataset có câu hỏi người dùng.

**Rút tham gia:** Bạn nhận một token ngẫu nhiên. Trước ngày “đóng liên kết rút” được thông báo tại phiên khảo sát, bạn có thể dùng token đó liên hệ qua kênh chính thức do giảng viên/nhà trường xác nhận để yêu cầu hủy các câu hỏi gắn với token. Sau khi nhóm đã xử lý yêu cầu và hủy liên kết token–phiếu consent, dữ liệu còn lại không thể nối lại với một người cụ thể; từ thời điểm đó, nhóm không thể xác định để xóa riêng dữ liệu của bạn. Bạn vẫn có thể báo quan ngại sau mốc này qua kênh chính thức, nhưng không hứa có thể truy xuất bản ghi vô danh.

**Câu hỏi hoặc khiếu nại:** Hỏi người phụ trách hoạt động của nhóm hoặc kênh giảng viên/nhà trường **đã được xác nhận trước khi mở khảo sát**. Nếu chưa có kênh xác nhận, hoạt động chưa được mở.

### Lựa chọn đồng ý

Hãy chọn **một** phương án:

- [ ] **Tôi xác nhận tôi từ đủ 18 tuổi, đã đọc/nghe thông tin trên, hiểu việc tham gia là tự nguyện và đồng ý cung cấp câu hỏi theo mô tả.**
- [ ] **Tôi không đồng ý tham gia.**

Nếu chọn “không đồng ý” hoặc không xác nhận đủ 18 tuổi, không thu câu hỏi và không cấp bản ghi nghiên cứu.

**Token rút dữ liệu:** ____________________  
**Phiên bản văn bản consent:** `CONSENT-v1.0`  
**Ngày phiên khảo sát:** ____ / ____ / ______  

**Xác nhận bằng văn bản theo hình thức đã được phê duyệt:**  
Chữ ký/đánh dấu của người tham gia: ____________________  
Người hướng dẫn phiên: ____________________

---

## 4. Phiếu khảo sát — bản người tham gia trả lời

Phiếu này tách khỏi phiếu consent. Không in hoặc viết tên người tham gia trên phiếu.

**Token:** ____________________  
**Phiên bản khảo sát:** `SURVEY-v1.0`

### A. Xác nhận điều kiện

1. Bạn xác nhận mình từ đủ 18 tuổi?
   - [ ] Có
   - [ ] Không
   - [ ] Không muốn trả lời

2. Bạn đã chọn “đồng ý tham gia” ở phiếu thông tin và đồng ý riêng?
   - [ ] Có
   - [ ] Không
   - [ ] Không muốn trả lời

> Nếu không chọn “Có” ở cả hai câu trên, dừng phiếu; không ghi câu hỏi vào dữ liệu nghiên cứu.

### B. Phạm vi câu hỏi (chọn nếu bạn muốn)

3. Câu hỏi bạn muốn tìm hiểu có liên quan đến Hà Nội không?
   - [ ] Có
   - [ ] Không
   - [ ] Chưa rõ
   - [ ] Không muốn trả lời

4. Câu hỏi thuộc nhóm nào? Có thể chọn một hoặc nhiều; không cần biết chính xác.
   - [ ] Cấp bản sao/trích lục hộ tịch hoặc bản sao giấy khai sinh
   - [ ] Chứng thực bản sao từ bản chính
   - [ ] Chứng thực chữ ký
   - [ ] Xác nhận, cải chính hoặc bổ sung thông tin hộ tịch
   - [ ] Nhóm khác trong hộ tịch–chứng thực
   - [ ] Chưa rõ nhóm thủ tục
   - [ ] Không muốn trả lời

### C. Câu hỏi của bạn

Bạn có thể để trống, hoặc tự viết/nói tối đa ba câu hỏi mà bạn thực sự muốn biết. Không cần cố nghĩ đủ số lượng. **Không ghi thông tin cá nhân, số hồ sơ, địa chỉ, số giấy tờ hoặc nội dung riêng tư.** Không có câu hỏi mẫu hoặc câu trả lời mẫu trên phiếu, để không gợi ý hay làm rò rỉ nội dung test.

- Câu hỏi 1 (không bắt buộc):  
  ____________________________________________________________________________

- Câu hỏi 2 (không bắt buộc):  
  ____________________________________________________________________________

- Câu hỏi 3 (không bắt buộc):  
  ____________________________________________________________________________

## 5. Xử lý tại phiên và sau phiên

1. **Sàng lọc trước thu:** người hướng dẫn nhắc lại không ghi PII; nếu người tham gia đã ghi thông tin định danh, mời họ tự gạch bỏ/viết lại. Nếu họ không muốn hoặc chi tiết là cần thiết để hiểu câu hỏi, không thu câu đó.
2. **Không số hóa thô:** không chụp phiếu bằng điện thoại cá nhân, không gửi qua chat/email, không đưa vào công cụ AI/API. Phiếu khảo sát tạm thời được cất khóa; phiếu consent tách hẳn khỏi phiếu khảo sát.
3. **Redaction hai bước:** Cao Văn Hà hoặc người được nhóm chỉ định chép câu hỏi vào kho riêng mã hóa chỉ sau khi loại PII; một người kiểm tra khác xác nhận `redaction_status`. Nếu còn PII, quay lại bản giấy chỉ để làm sạch hoặc hủy câu hỏi; không copy phần thô vào dataset.
4. **Ghi nhận tối thiểu:** với mỗi câu hỏi đủ điều kiện chỉ ghi `survey_question_id`, `respondent_cluster_id` (token ngẫu nhiên), phiên bản consent, trạng thái redaction, nhóm thủ tục thô, cờ Hà Nội, kênh thu ở mức tổng quát (`paper_in_person` hoặc `interview_in_person`) và trạng thái khóa test. Không ghi trạng thái giả như “đã có người tham gia”; bản ghi chỉ được tạo sau sự kiện thật.
5. **Rút trước mốc:** khi nhận token qua kênh đã xác nhận, đối chiếu sổ liên kết riêng, loại toàn bộ bản ghi/câu hỏi thuộc token khỏi kho nghiên cứu, ghi thời điểm và hành động trong nhật ký riêng không chứa PII trong dataset. Không dùng câu hỏi đã rút cho authoring, SFT, DPO, tuning hoặc đánh giá.
6. **Đóng liên kết:** sau mốc đã thông báo và sau khi giải quyết yêu cầu tồn đọng, hủy liên kết token–consent. Khi đó `respondent_cluster_id` vẫn cho phép bootstrap theo cụm trong dữ liệu nhưng không cho phép tái nhận diện.
7. **Khóa test:** câu hỏi đạt redaction được đặt `heldout` trước khi người tạo QA, người tune hay người chấm DPO xem nội dung. Chúng không được dùng làm prompt authoring, paraphrase, SFT, DPO train/validation hoặc chọn siêu tham số.

## 6. Bàn giao con người và lịch vận hành tối thiểu

| Mốc | Người/nhóm chịu trách nhiệm | Việc phải hoàn tất | Bằng chứng riêng, không đưa Git |
|---|---|---|---|
| Trước mở | Cả nhóm; giảng viên/đơn vị có thẩm quyền | Xác nhận hình thức consent, kênh liên hệ, lịch/địa điểm và người hướng dẫn | Xác nhận theo quy định áp dụng |
| Trước từng phiên | Cao Văn Hà; người hướng dẫn | Token ngẫu nhiên, phiếu bản đúng version, kho mã hóa/khóa vật lý, hướng dẫn redaction | Sổ vận hành không chứa dữ liệu khảo sát |
| Trong phiên | Người hướng dẫn | Đọc văn bản, kiểm tuổi/consent, không ép buộc, tách phiếu consent–survey | Chỉ phiếu thật nếu người tham gia tự nguyện |
| Sau từng phiên | Người phụ trách nhập liệu + người kiểm redaction | Loại PII trước nhập, khóa test, ghi audit tối thiểu | Nhật ký redaction riêng |
| Đến mốc rút | Cao Văn Hà | Xử lý toàn bộ token rút hợp lệ, hủy bản ghi liên quan | Nhật ký rút riêng |
| Sau đóng liên kết | Cả nhóm xác nhận; Cao Văn Hà thực hiện | Hủy liên kết token–consent; giữ dữ liệu đã ẩn danh theo giới hạn mục đích | Biên bản nội bộ riêng |

Không có bước nào tự động thu người tham gia hoặc tạo dữ liệu giả. Chỉ sau khi các gate được phê duyệt và sự kiện thật xảy ra, nhóm mới được dùng bản nháp này làm protocol vận hành.