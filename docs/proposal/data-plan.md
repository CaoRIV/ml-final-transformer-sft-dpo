# Kế hoạch dữ liệu bản nháp — Trợ lý hỏi đáp thủ tục hành chính công

> **Trạng thái:** bản nháp kế hoạch tuần 1 có sổ nguồn, pilot QA, hồ sơ corpus A.2 và biểu mẫu vận hành. Pilot có 20/20 kết luận rà nội dung nhưng chưa có QA được phát hành để huấn luyện; chưa có khảo sát thật hoặc dữ liệu DPO. Đây không phải datasheet của một release đã được chấp nhận.

## 1. Mục đích, ranh giới và quyết định tiền điều kiện

Bộ dữ liệu phục vụ ba mục tiêu tách biệt:

1. huấn luyện/kiểm chứng mô hình ngôn ngữ ký tự nhỏ ở nhánh Phần A từ corpus có quyền dùng;
2. SFT trợ lý hỏi đáp thủ tục bằng câu hỏi–đáp có citation tới đoạn nguồn;
3. DPO từ cặp câu trả lời SFT cho cùng prompt, do tối thiểu hai người chấm độc lập đánh giá; và test tách biệt bằng câu hỏi người dùng thật nếu có consent.

Đề tài không triển khai PPO hay RAG; báo cáo D.5 thảo luận giới hạn của tinh chỉnh với tri thức thay đổi nhanh và RAG như hướng mở rộng. Không coi mô hình là nguồn pháp lý, không thu hồ sơ cá nhân, không thu thông tin định danh để “cá nhân hóa” câu trả lời. Dataset chỉ nhằm kiểm chứng nghiên cứu trong phạm vi thủ tục đã công bố, không thay thế cổng/cơ quan có thẩm quyền.

Trước bất kỳ thu thập tự động hoặc khảo sát nào, nhóm phải kiểm tra ba điều kiện vận hành:

1. **Danh mục thủ tục và phiên bản nguồn nào** nằm trong phạm vi Hà Nội/hộ tịch–chứng thực đã thống nhất?
2. **Có thể tiếp cận người khảo sát với đồng ý bằng văn bản hay không?** Kế hoạch khảo sát đã được chấp thuận, nhưng chỉ gọi là test người dùng thật khi thực sự thu thập hợp lệ.
3. **Lịch chấm độc lập và phân xử thế nào?** Phương án Thế/Hưng chấm độc lập, Hà phân xử đã được đồng ý; cần hướng dẫn chấm và bố trí thời gian.

Người dùng đã đồng ý phương án Hà Nội/hộ tịch–chứng thực, Truyện Kiều cho mô hình ký tự, khảo sát sinh viên/người thân và bố trí Hà Mạnh Thế–Trần Duy Hưng chấm độc lập, Cao Văn Hà phân xử. Đây là chấp thuận kế hoạch, không phải bằng chứng đã có người tham gia, nhãn hay quyền thu thập D. Nhóm gồm Cao Văn Hà (trưởng nhóm, tổng hợp và nộp bài), Hà Mạnh Thế, Trần Duy Hưng. Theo lịch Hà cung cấp, hạn hoàn thành là 23h59 ngày 01/12/2026, vấn đáp ngày 03/12/2026; cách nộp cần xác nhận với giảng viên. Mô hình, GPU và nơi lưu phần D chưa chốt.

### 1.1. Phương án dữ liệu đã được đồng ý

**Đã được người dùng đồng ý về phương án:** địa bàn Hà Nội; đối tượng trọng tâm là sinh viên/người trẻ và gia đình; nhóm thủ tục hộ tịch–chứng thực. Bắt đầu mẫu nhỏ từ cấp bản sao trích lục hộ tịch/bản sao giấy khai sinh và chứng thực bản sao từ bản chính; xem xét thêm chứng thực chữ ký, xác nhận thông tin hộ tịch, cải chính/bổ sung hộ tịch sau khi kiểm tra từng nguồn. Không coi các trường hợp cấp bản sao cho từng loại giấy tờ là nhiều thủ tục độc lập chỉ để tăng số lượng. Chưa đưa đất đai, tranh chấp, yếu tố nước ngoài vào phạm vi chính.

Vòng kiểm nguồn đầu đã lưu **9 nguồn cho 5 họ thủ tục ứng viên**, cùng thời điểm truy xuất, hash bản trích xuất, kết quả kiểm robots và điều khoản. Xem [sổ metadata nguồn](../data/source-ledger.json) và [phân tích nguồn](../data/source-audit.md).

- Cổng quốc gia đã đọc: trích lục `2.000635`, chứng thực bản sao `2.000815`, chứng thực chữ ký `2.000884`, cải chính/bổ sung hộ tịch `1.004859`.
- Cổng Hà Nội/Ô Chợ Dừa đã đọc bằng trình duyệt: bài trích lục, tệp phương án được bài liên kết, hướng dẫn chứng thực bản sao, xác nhận thông tin hộ tịch; riêng cải chính chỉ đọc mô tả video, chưa kiểm nội dung video.
- Có **khác biệt thời hạn trích lục**: trang quốc gia nêu trong ngày/ngày làm việc kế tiếp; phụ lục phương án Hà Nội B.4 ghi dự kiến 03 ngày, có thể đến 10 ngày khi kiểm tra/xác minh. Tệp liên kết chưa phải quyết định đầy đủ có số/ngày được kiểm rõ. Không chọn một thời hạn làm đáp án hiện hành khi chưa giải quyết khác biệt.

Robots Trung tâm Hà Nội/Ô Chợ Dừa yêu cầu cách 5 giây; robots VPCP và kho CDN trả 404 trong lần kiểm. Điều khoản quốc gia yêu cầu tuân thủ pháp luật khi dùng lại, footer Hà Nội yêu cầu ghi nguồn; **chưa xác nhận giấy phép cho dataset/huấn luyện/phân phối phần nội dung cụ thể**. Không thu dữ liệu hồ sơ cá nhân. Các bản lưu/trích đoạn và QA nghiên cứu giữ ngoài Git, chưa đưa vào SFT.

Để đạt 2.000 QA có giá trị, đánh giá độ phủ sau mẫu 5–10 thủ tục/20–50 QA; nếu nguồn không đủ tình huống độc lập thì đề xuất mở rộng trong hộ tịch–chứng thực, không nhân bản hàng trăm cách diễn đạt của cùng câu hỏi. Chưa hứa số lượng thủ tục cần thiết trước kiểm kê.

**Corpus ký tự đã chọn:** *Truyện Kiều*, bản Quốc ngữ Trương Vĩnh Ký 1911, từ phần thơ Wikisource revision `206466` có bản quét đối chiếu. [Hồ sơ corpus](../data/char-corpus.md) ghi nguồn, căn cứ chọn, tách train/validation, hiện vật và bước xác nhận trước huấn luyện. Revision `206607` chỉ là [audit nghiên cứu lịch sử](../data/char-corpus-audit-report.json); không dùng hiện vật, hash hay số đo của nó cho bản 1911. Corpus thơ không đại diện văn xuôi hành chính và không đưa vào SFT.

**Khảo sát test đề xuất:** mời người từ 18 tuổi trở lên trong lớp, câu lạc bộ và mạng lưới người thân có nhu cầu tìm hiểu thủ tục. Mục tiêu vận hành ban đầu 50–80 người, mỗi người tự đặt 2–3 câu hỏi thật sự muốn biết; tương ứng 100–240 câu thô trước lọc, không bảo đảm số test hợp lệ. Đề không ấn định số người hay số câu test này. Không yêu cầu mỗi người cố nghĩ đủ số câu, không đưa QA mẫu hoặc câu trả lời mô hình cho họ chép. Thu tự nguyện, không gắn điểm học tập, không mặc định đồng ý vì quen biết.

Biểu mẫu dự kiến hỏi: đồng ý tham gia sau thông tin mục đích/quyền rút; đã đủ 18 tuổi hay chưa; từng làm/đang tìm hiểu nhóm thủ tục nào (không hỏi số hồ sơ); câu hỏi muốn được giải đáp; câu hỏi có đang liên quan Hà Nội hay không. Không thu tên, mã sinh viên, email tự động, địa chỉ cụ thể hoặc ảnh giấy tờ. Xác nhận hình thức đồng ý điện tử đáp ứng yêu cầu bằng văn bản trước thu; biểu mẫu không được lưu tự động nội dung nhạy cảm chưa kiểm soát. Hướng dẫn người tham gia không nhập PII và có quy trình ẩn danh trước lưu dữ liệu nghiên cứu. Cần quy định rõ thời hạn rút trước khi phá liên kết định danh; sau ẩn danh hoàn toàn không hứa truy tìm được dữ liệu từng người.

Bộ vận hành đã soạn: [thông tin/đồng ý và phiếu khảo sát](../data/consent-and-survey.md), [quy trình riêng tư](../data/privacy-workflow.md), [hướng dẫn kiểm QA và chấm ưu tiên](../data/annotation-guide.md). Phương án mặc định dùng phiếu giấy/phỏng vấn tại chỗ để kiểm ẩn danh trước số hóa; chưa mở Google Forms hoặc khảo sát công khai. Trước thu thập cần xác nhận hình thức đồng ý, kênh liên hệ, kho riêng, thời hạn rút và người phụ trách; không coi bản nháp protocol là chấp thuận pháp lý hay đã có người tham gia.

Khảo sát chủ yếu sinh viên là mẫu thuận tiện, không đại diện toàn bộ cư dân Hà Nội. Giữ câu hỏi ngoài phạm vi phát sinh tự nhiên để đánh giá từ chối; nếu không đủ, thu thêm câu hỏi thật cho nhóm này, không giả câu hỏi AI là khảo sát. Khóa test và tách họ thủ tục theo thiết kế trước tạo QA train; các câu bị trùng/rò rỉ phải xử lý trước huấn luyện, không sau khi xem điểm.

**Phương án chấm DPO đã được đồng ý:** Hà Mạnh Thế và Trần Duy Hưng chấm độc lập; Cao Văn Hà phân xử sau khi khóa nhãn và tính đồng thuận. Ba người tập chấm một lô hiệu chuẩn riêng trước khi chấm chính thức; lịch thực hiện cần xác định. Đề xuất sinh khoảng 650–750 cặp thô, giữ ít nhất 500 cặp train hợp lệ và validation riêng sau loại hòa/lỗi; số sinh này không bảo đảm đủ cặp hợp lệ. Đáp án phải sinh từ checkpoint SFT thật, không viết tay chosen/rejected thay thế. Hai người cùng chấm mọi cặp, không chia đôi 250 cặp/người. Chấm mù đánh giá cuối phải dùng tập khác dữ liệu DPO; nếu không có người chấm ngoài nhóm, nêu giới hạn thiên lệch nội bộ.

## 2. Bốn nguồn/lớp dữ liệu và tiêu chí nhập kho

| Mã lớp | Mục đích | Nguồn được phép và đơn vị thu thập | Điều kiện nhập kho | Không được suy diễn |
|---|---|---|---|---|
| `CHAR_CORPUS` | Huấn luyện LM ký tự nhỏ cho Phần A, báo cáo PPL validation | Văn bản tiếng Việt thuộc phạm vi công cộng hoặc có giấy phép mở, ví dụ Truyện Kiều **nếu** phiên bản/tình trạng quyền được kiểm tra | Tài liệu có URL/định danh, giấy phép hoặc căn cứ phạm vi công cộng, bản lưu/fingerprint và split train/val | Không dùng nội dung hành chính chưa rõ quyền; không gọi corpus là dữ liệu Phần D |
| `ADMIN_SOURCE` | Làm căn cứ cho QA/citation | Mô tả thủ tục công khai tại **Cổng Dịch vụ công quốc gia và cổng của địa phương đã chốt**, cùng văn bản/căn cứ công khai liên quan | Kiểm tra điều khoản, robots.txt và giới hạn truy cập; lưu thời điểm, phiên bản/ngày hiệu lực khi có, URL và span | Không bịa URL/cơ quan/văn bản; không lấy dữ liệu cá nhân hay vượt kiểm soát truy cập |
| `SFT_QA` và `DPO_PAIR` | SFT, validation và DPO | QA được tạo từ `ADMIN_SOURCE`; hai ứng viên trả lời sinh từ checkpoint SFT trên prompt đã khóa | Citation xác minh; SFT kiểm thủ công theo mức tối thiểu từng split; preference có hai nhãn độc lập, rồi mới phân xử | Không ghi nhận 2.000 QA hoặc 500 cặp khi chưa đủ count đã kiểm; không dùng một người chấm thay cho hai người |
| `USER_TEST` | Test độc lập và đánh giá mù | Câu hỏi do người dùng thật cung cấp qua khảo sát sau consent bằng văn bản | Ẩn danh trước lưu; tách hoàn toàn train/val; lưu consent-state không lưu định danh; kiểm tra thuộc cụm người khảo sát | Không dùng câu hỏi “tự nghĩ ra” và gọi là khảo sát thật; không giữ tên, liên hệ, hồ sơ hay dữ liệu nhạy cảm không cần thiết |

Cách triển khai ưu tiên là **đủ 2.000 QA train và 500 cặp DPO train, cộng validation riêng**, vì train/validation không nên dùng chung record. Đây là đề xuất bảo thủ để đáp ứng ngưỡng của đề bài sau chia tách, không phải cam kết số lượng đã có. Quy mô `USER_TEST` sẽ chỉ được đặt sau khi biết khả năng khảo sát và số cụm người tham gia; không làm đầy bằng dữ liệu mô phỏng.

Đã chuẩn bị mẫu **20 QA nháp cho 5 họ thủ tục**, kèm 21 trích đoạn, chỉ để kiểm quy trình nghiên cứu. Script đã kiểm hash, vị trí trích đoạn và cấu trúc citation; **0 QA được human phê duyệt, 0 QA đủ điều kiện huấn luyện**. Xem [báo cáo pilot](../data/admin-pilot.md). Các record ở `data/review/admin-pilot-v1/` bị Git bỏ qua do quyền/phiên bản và review chưa hoàn tất. Pilot không thay thế bộ train yêu cầu, không phải test khảo sát và không phải ngưỡng nộp tuần 1.

## 3. Sổ nguồn, provenance và phiên bản

Mọi item nguồn đi qua sổ nguồn trước khi sinh QA. Không scrape hàng loạt trước khi kiểm điều kiện của từng domain và biểu mẫu nguồn.

### 3.1. Schema `source_document`

| Trường | Kiểu/gợi ý | Ý nghĩa |
|---|---|---|
| `source_id` | UUID/chuỗi bất biến | Khóa nội bộ của một tài liệu/phiên bản nguồn |
| `source_type` | enum: `char_corpus`, `service_page`, `legal_text`, `guidance` | Loại nguồn; không dùng tên mơ hồ |
| `publisher_or_authority` | string | Tác giả/cơ quan phát hành đúng như nguồn thể hiện |
| `title` | string | Tiêu đề tài liệu/trang |
| `canonical_url` | URL | URL chuẩn hoặc định danh công khai; lưu nguyên văn |
| `retrieved_at_utc` | ISO-8601 | Thời điểm nhóm truy xuất |
| `published_at` / `effective_from` / `effective_to` | nullable date | Ngày công bố/hiệu lực/hết hiệu lực nếu nguồn công bố |
| `source_version_label` | nullable string | Ký hiệu phiên bản/số văn bản; không tự đặt thành “mới nhất” |
| `content_hash` | SHA-256 | Fingerprint bản nội dung đã dùng |
| `license_or_terms_url` | URL/text | Nơi kiểm tra giấy phép/điều khoản dùng |
| `robots_checked_at` | nullable ISO-8601 | Thời điểm kiểm robots, nếu thu từ web |
| `access_method` | enum + note | tải tay/API/crawl được phép; rate-limit áp dụng |
| `scope_group` | string | Nhóm thủ tục đã chốt để phục vụ split |
| `ingest_status` | enum | `pending_review`, `accepted`, `rejected`, `superseded` |
| `reviewer_id` | pseudonymous ID | Người kiểm provenance/quyền; không là PII công khai |
| `notes` | text | Giới hạn, thay đổi hoặc lý do loại |

Nếu phát hiện văn bản bị thay thế, tạo `source_id`/phiên bản mới hoặc liên kết `supersedes_source_id`; không ghi đè bản cũ rồi mất khả năng tái lập. Khi nguồn thiếu ngày hiệu lực, trường phải là null và báo cáo nêu giới hạn.

### 3.2. Schema `source_span`

Citation phải trỏ đến span bất biến của bản nguồn đã lưu, không chỉ đến trang chủ.

| Trường | Kiểu/gợi ý | Ý nghĩa |
|---|---|---|
| `span_id` | UUID | Khóa span |
| `source_id` | FK `source_document` | Bản nguồn chứa span |
| `locator_type` | `heading`, `article_clause`, `page`, `char_offset`, `xpath` | Cách xác định vị trí |
| `locator_start`, `locator_end` | string/int | Biên span tái lập trong bản đã hash |
| `heading_path` | nullable string | Đường dẫn đề mục/Điều–Khoản khi có |
| `quoted_text` | text | Đoạn trích đã chuẩn hóa tối thiểu để review |
| `normalization_version` | string | Quy tắc trích xuất/chuẩn hóa áp dụng |
| `span_hash` | SHA-256 | Fingerprint span |
| `claim_tags` | array | Ví dụ: `required_documents`, `process`, `time_limit`, `fee`, `legal_basis` |
| `review_status` | enum | `unreviewed`, `verified`, `rejected`, `stale` |

`quoted_text` và bản nguồn có thể cần hạn chế quyền truy cập nếu điều khoản nguồn yêu cầu; public manifest chỉ nên công khai URL, locator và hash khi không được phép phân phối toàn văn.

## 4. Schema cho QA SFT, DPO và test

### 4.1. Schema `qa_record`

| Trường | Kiểu/gợi ý | Ý nghĩa |
|---|---|---|
| `qa_id` | UUID | Khóa bất biến |
| `record_version` | semver/string | Phiên bản record sau chỉnh sửa |
| `split` | `train`, `validation`, `test_user`, `holdout` | Split khóa; test user không được đưa lại train |
| `scope_group` | string | Nhóm thủ tục để split theo nhóm |
| `procedure_family_id` | string | Họ thủ tục; dùng phát hiện rò rỉ cùng quy trình |
| `question_text` | text | Prompt tiếng Việt đã loại PII |
| `question_origin` | `authoring`, `user_survey`, `paraphrase` | Nguồn gốc câu hỏi, không nói mơ hồ “thật” |
| `answer_text` | text | Đáp án SFT tham chiếu, có giới hạn/ từ chối khi phù hợp |
| `citation_span_ids` | array FK | Một hoặc nhiều span chống đỡ từng mệnh đề chính |
| `citation_rendering` | text | Dạng citation hiển thị cho mô hình/người chấm |
| `source_version_ids` | array FK | Phiên bản nguồn thực sự dùng |
| `claim_coverage` | structured array | Claim → span_id → trạng thái đủ/không đủ căn cứ |
| `language` | `vi` | Ngôn ngữ |
| `provenance` | structured object | Tác giả/generator, thời điểm, template, record nguồn |
| `label_status` | enum | `draft`, `citation_checked`, `approved`, `rejected`, `superseded` |
| `labeler_id`, `reviewer_id` | pseudonymous IDs | Người tạo/kiểm; không đưa PII vào dataset |
| `quality_flags` | array | `needs_refusal`, `stale_source`, `ambiguous`, `duplicate_candidate`... |
| `created_at`, `updated_at` | ISO-8601 | Audit trail |

QA sinh bán tự động chỉ được chấp nhận sau review theo citation. Với **mỗi split SFT có dùng cho huấn luyện/chọn cấu hình**, lấy mẫu ngẫu nhiên phân tầng theo `scope_group`, `question_origin` và nguồn với khối lượng ít nhất $\lceil0{,}20N_{split}\rceil$; vì vậy riêng 2.000 QA train cần kiểm thủ công ít nhất 400 record, và validation cũng có mẫu kiểm riêng theo quy tắc này. Lưu `qa_id`, reviewer, ngày, kiểm đủ citation/đúng nội dung/đúng scope và quyết định. Nếu lỗi hệ thống xuất hiện, mở rộng review hoặc sửa batch có liên quan; không chỉ thay vài mẫu lỗi.

### 4.2. Schema `preference_pair`

| Trường | Kiểu/gợi ý | Ý nghĩa |
|---|---|---|
| `pair_id` | UUID | Khóa cặp ưu tiên |
| `pair_version` | string | Phiên bản cặp/rubric |
| `split` | `train`, `validation` | Chỉ chia cặp ưu tiên DPO thành train/validation theo nhóm; chấm mù cuối trên `USER_TEST` là luồng riêng, không tạo `DPO_PAIR` từ test |
| `qa_id` / `prompt_id` | FK | Cùng một prompt cho hai ứng viên |
| `prompt_text` | text/hash | Prompt chính xác đã sinh; có thể tham chiếu nếu lặp |
| `sft_checkpoint_id` | string/hash | Checkpoint sinh ứng viên |
| `generation_config` | JSON | temperature, top-p, max tokens, seed và template |
| `candidate_0_id`, `candidate_1_id`, `candidate_0_text`, `candidate_1_text` | ID bất biến + text | Hai candidate theo thứ tự canonical, độc lập với A/B hiển thị cho từng người chấm |
| `candidate_0_citations`, `candidate_1_citations` | array FK/text | Citation người chấm có thể đối chiếu |
| `rubric_version` | string | Phiên bản hướng dẫn chấm |
| `rater_1_id`, `rater_2_id` | pseudonymous IDs | Danh tính vận hành tối thiểu của hai người chấm độc lập |
| `rater_1_display_map`, `rater_2_display_map` | JSON | Ánh xạ A/B được hiển thị → `candidate_0_id`/`candidate_1_id`; cho phép đảo thứ tự riêng từng người |
| `rater_1_label_raw`, `rater_2_label_raw` | `A`, `B`, `tie`, `invalid` | Nhãn độc lập như người chấm đã thấy |
| `rater_1_label_normalized`, `rater_2_label_normalized` | `candidate_0`, `candidate_1`, `tie`, `invalid` | Nhãn quy về candidate thực bằng display map; dùng cho agreement |
| `rater_1_reason`, `rater_2_reason` | coded/text | Lý do theo rubric, hạn chế PII |
| `rater_1_at`, `rater_2_at` | ISO-8601 | Audit thời điểm |
| `independent_agreement` | derived | Đồng ý/bất đồng **trước** phân xử, dựa trên nhãn normalized |
| `adjudication_label` | `candidate_0`, `candidate_1`, `exclude`, null | Quyết định sau bất đồng |
| `adjudicator_id`, `adjudicated_at`, `adjudication_reason` | audit fields | Ai/quy tắc đã phân xử |
| `chosen_text`, `rejected_text` | derived | Chỉ tạo sau khi có nhãn quyết định |
| `provenance` | structured | Record/SFT checkpoint/nguồn liên quan |
| `status` | enum | `pending`, `labeled`, `adjudicated`, `excluded` |

Hai người chấm phải xem candidate với thứ tự A/B đã đảo ngẫu nhiên, độc lập và không biết nhãn của nhau. Họ dùng rubric: (i) đúng với span nguồn, (ii) đầy đủ yêu cầu, (iii) citation đúng và có thể kiểm tra, (iv) từ chối đúng khi ngoài phạm vi/thiếu căn cứ, (v) không bịa. `tie` và `invalid` là kết quả hợp lệ; cặp như vậy không được ép thành preference train. Trước phân xử, tính tỷ lệ đồng thuận trên nhãn `normalized` và Cohen’s $\kappa$ trên các nhãn hợp lệ `{candidate_0, candidate_1, tie}`; `invalid` được báo riêng và loại khỏi mẫu tính $\kappa$ theo protocol này. Sau khi lưu nhãn độc lập, bất đồng mới được phân xử bằng quy tắc đã công bố (ví dụ người thứ ba hoặc họp có biên bản); báo cáo tỷ lệ đồng thuận, $\kappa$, tỷ lệ loại và cách xử lý, không chỉ ghi nhãn cuối.

### 4.3. Schema `user_survey_record` và tách dữ liệu con người

| Trường | Kiểu/gợi ý | Ý nghĩa |
|---|---|---|
| `survey_question_id` | UUID ngẫu nhiên | Khóa câu hỏi đã ẩn danh |
| `respondent_cluster_id` | UUID ngẫu nhiên, tách bảng liên hệ | Cụm bootstrap, không dùng định danh thật |
| `consent_version` | string | Phiên bản văn bản consent mà người trả lời đã đồng ý |
| `consent_status`, `consented_at` | enum/time | Chỉ nhận `granted` trước khi ingest |
| `withdrawn_at` | nullable time | Dấu vết xóa/loại nếu rút đồng ý |
| `question_text_redacted` | text | Câu hỏi đã xóa PII trước lưu dataset |
| `scope_group` | string | Kiểm tra thuộc phạm vi |
| `survey_channel` | coarse enum | Kênh tổng quát, không lưu liên hệ/địa chỉ chính xác |
| `test_split_status` | `eligible`, `excluded`, `heldout` | Khóa khỏi train/val/prompt authoring |
| `redaction_reviewer_id`, `redaction_status` | audit | Ai kiểm ẩn danh và trạng thái |

Văn bản consent, thông tin liên hệ (nếu cần để vận hành khảo sát) và câu hỏi đã ẩn danh phải lưu tách lớp truy cập. Dataset phân tích không chứa tên, số điện thoại, địa chỉ, mã hồ sơ, ảnh giấy tờ, thông tin sức khỏe/tài chính hoặc định danh tương tự. Nếu một câu hỏi chứa chi tiết không thể ẩn danh mà vẫn giữ ý nghĩa, loại nó. Khi chưa có khảo sát hợp lệ, `USER_TEST` không được tạo bằng placeholder.

## 5. Quy trình tạo dữ liệu và kiểm soát chất lượng

### 5.1. Ingest nguồn → span → QA

1. Chốt domain/cơ quan/nhóm thủ tục; kiểm điều khoản, robots.txt, tần suất và phạm vi truy cập trước ingest.
2. Lưu metadata `source_document`, bản/manifest hoặc hash; không sửa im lặng. Phân đoạn theo đề mục, Điều–Khoản, trang hoặc offset có thể tái xác định.
3. Lập `source_span`; người kiểm xác nhận span có thể trả lời claim nào.
4. Phân bổ họ thủ tục vào split trước khi soạn hoặc sinh QA. Soạn QA theo template nhưng không vượt phạm vi span. Mỗi mệnh đề chính phải liên kết span; nếu nguồn không đủ, giới hạn đáp án hoặc từ chối.
5. Kiểm citation thủ công với khối lượng $\lceil0{,}20N_{split}\rceil$ cho từng split SFT dùng cho train/validation; riêng 2.000 QA train tối thiểu là 400 record. Lưu kết quả review và sửa theo batch khi phát hiện lỗi chung.
6. Sau rà chất lượng và audit rò rỉ, khóa split hiện vật, tạo manifest số lượng/hashes rồi chuẩn bị dữ liệu huấn luyện.

Nhóm không nên chờ đủ toàn bộ 2.000 QA mới thử pipeline. Cuối tuần 1 hoặc đầu tuần 2, sau khi có pilot đúng quyền và citation, chạy **SFT pilot sớm** để phát hiện lỗi tokenizer/template/citation/VRAM và để checkpoint SFT tạo ứng viên DPO. Pilot không được biến thành tuyên bố rằng 500 cặp DPO đã tồn tại.

### 5.2. Tạo preference cho DPO

1. Đóng băng checkpoint SFT pilot hoặc checkpoint đã chọn, tokenizer và prompt template.
2. Với cùng mỗi prompt, sinh hai candidate theo config đã ghi (có diversity đủ để nảy sinh lựa chọn); lưu seed/config/checkpoint, không sửa text sau khi thấy nhãn.
3. Randomize A/B và giao cho hai người đánh giá độc lập dùng rubric có ví dụ/calibration.
4. Khóa hai nhãn ban đầu, tính agreement; chỉ sau đó phân xử bất đồng theo quy tắc đã công bố. `tie`, `invalid` hoặc không đủ căn cứ bị loại khỏi train DPO và vẫn lưu lý do.
5. Tách train/validation DPO bằng khóa nhóm prompt/thủ tục, công bố count cuối theo `status`; không trộn cặp cùng prompt qua split.

Ngưỡng đề bài là ít nhất 500 cặp so sánh. Kế hoạch chỉ có thể coi “500 train pairs” đạt khi cặp đã qua hai nhãn, phân xử nếu cần, kiểm dữ liệu và split. Tính `pair_id` raw, số chấm độc lập, số đồng thuận/bất đồng, số bị loại và số train/validation riêng; không báo một con số gộp che mất cặp không dùng được.

### 5.3. Kiểm soát trùng lặp, near duplicate và rò rỉ split

- Chuẩn hóa Unicode (NFC), khoảng trắng và dạng citation trước khi so exact hash; lưu phiên bản chuẩn hóa.
- Phát hiện near duplicate bằng chữ ký n-gram/MinHash hoặc embedding đã được chọn trong manifest, sau đó review thủ công các cặp qua ngưỡng. Không chỉ so text đáp án: phải xét prompt, procedure family, source span và paraphrase.
- Split cấp **nhóm thủ tục/họ thủ tục** và khi phù hợp theo nguồn/phiên bản, thay vì random từng QA. `holdout` là một hay nhiều họ thủ tục không có QA, source span hay paraphrase liên quan trong train/validation; nó đo khả năng khái quát sang tri thức thủ tục chưa thấy, không phải bằng chứng mô hình biết pháp lý mới.
- Giữ toàn bộ `USER_TEST` ngoài authoring, SFT, DPO train/val, tuning prompt và selection hyperparameter. Nếu người khảo sát gửi nhiều câu hỏi, tất cả phải nằm trong một `respondent_cluster_id` và không được phân tán qua split.
- Sau split chạy audit cross-split: exact hash, near-duplicate candidates, shared `source_span_id`, shared `procedure_family_id`, prompt/candidate DPO và `respondent_cluster_id`. Chiến lược strict split này không được nới sau khi xem kết quả mô hình; nếu cần sửa xung đột trước train, tạo split/dataset version mới và ghi lý do.

## 6. Split, phiên bản và quyền truy cập

Mỗi release dữ liệu phải có `dataset_version`, ngày tạo, danh sách file + SHA-256, phiên bản nguồn, quy tắc chuẩn hóa, nhãn và rubric; manifest chia tập, số lượng theo trạng thái và changelog. Bất kỳ thay đổi nào ảnh hưởng text, citation, nhãn, split hoặc nguồn tạo release mới. Huấn luyện phải tham chiếu một `dataset_version` bất biến.

Quyền truy cập tối thiểu:

- **Raw/source có điều kiện:** người phụ trách dữ liệu; không công bố lại nếu điều khoản không cho phép.
- **QA/DPO đã review:** nhóm thực hiện, có audit log thay đổi.
- **Survey consent/liên hệ:** người được ủy quyền tối thiểu; không chuyển cho người chấm/huấn luyện.
- **User test đã ẩn danh, khóa:** evaluator được chỉ định; không đưa cho người tune mô hình cho đến khi khóa thử nghiệm theo kế hoạch.

Nếu không thể phát hành raw data, repository vẫn phải chứa script thu thập/biến đổi hợp lệ, schema, manifest/hash và hướng dẫn tái lập trong phạm vi điều khoản. Datasheet cuối phải mô tả nguồn gốc, giấy phép, lọc, PII/consent, split, giới hạn và cách yêu cầu xóa/rút dữ liệu con người.

## 7. Kế hoạch đánh giá và thống kê

### 7.1. Đơn vị đánh giá

So sánh mô hình gốc, SFT và SFT+DPO trên cùng `USER_TEST` khóa nếu khảo sát hợp lệ. Người chấm mù model identity và thứ tự phương án; họ kiểm tính đúng nội dung, đủ ý, citation đúng, ảo giác và từ chối đúng. Vì hệ không có RAG và không cập nhật tri thức thời gian thực, điểm tốt trên `holdout` không cho phép suy ra câu trả lời đúng cho văn bản pháp lý mới/chưa có trong nguồn; giới hạn này phải nêu trong báo cáo. Nếu chưa có `USER_TEST`, báo cáo trung thực rằng thiếu tập test người dùng thật thay vì thay nó bằng train-derived QA.

Protocol khóa phải định nghĩa mẫu số trước khi chấm:

- **Độ chính xác mệnh đề thông tin (claim accuracy):** số mệnh đề được người chấm xác nhận đúng và được nguồn hỗ trợ / tổng mệnh đề thông tin trong các câu trả lời được chấm. Mệnh đề không xác định hoặc không đủ nguồn vẫn ở mẫu số, không ở tử số; báo riêng số lượng này. Câu trả lời không có mệnh đề thông tin được đánh giá ở chỉ số từ chối, không tự cho accuracy bằng 1.
- **Tỷ lệ ảo giác theo câu trả lời:** số câu trả lời có ít nhất một mệnh đề thông tin không được nguồn hỗ trợ / tổng câu trả lời được chấm. Đây là định nghĩa vận hành “không được nguồn hỗ trợ”, không khẳng định mọi mệnh đề đó sai trong thế giới thực; báo số câu bị loại do lỗi kỹ thuật riêng.
- **Từ chối ngoài phạm vi:** số câu ngoài phạm vi hoặc không có căn cứ mà mô hình từ chối/điều hướng đúng / tổng câu thuộc nhóm đó. **Từ chối sai trong phạm vi:** số câu trong phạm vi, có căn cứ đủ và được protocol xem là trả lời được nhưng mô hình từ chối / tổng câu trong nhóm này; đây không được gộp thành “từ chối đúng”.
- **Win rate chấm mù theo cặp:** $(W+0{,}5T)/(W+T+L)$, trong đó $W,T,L$ là số thắng, hòa, thua của một mô hình trên các cặp hợp lệ; báo số `invalid`/loại riêng.

Mọi CI là **95% bootstrap** theo cụm người khảo sát (`respondent_cluster_id`) khi một người có nhiều câu; nếu mỗi câu thuộc người khác hoặc không có lặp người, đơn vị cluster chính là câu hỏi. Nêu số câu, số cụm, số lần resample, statistic và seed bootstrap; không coi các quan sát seed × prompt là độc lập.

### 7.2. Năm run và chọn cấu hình

Đề bài yêu cầu trung bình ± độ lệch chuẩn trên ít nhất 5 run hoặc 5 fold. Đề xuất chạy 5 seed **độc lập** cho cấu hình cuối (cố định dataset split và protocol); mỗi run phải có seed, checkpoint, config, môi trường và log riêng. Với seed $s$, chuỗi run là `SFT_s → DPO_s` với `ref = SFT_s`; tập ưu tiên đã khóa chung từ pilot, không phải chấm lại 500 cặp cho mỗi seed. Nhánh mô hình ký tự Phần A cũng chạy ít nhất 5 seed độc lập để báo validation PPL. Báo cáo mean và sample SD:

$$s=\sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2},\qquad n=5.$$

Năm lần generation/decoding từ một checkpoint chỉ là biến thiên đầu ra, **không** phải năm run. Baseline checkpoint/config cố định không được gán sample SD bằng lặp output. Tương tự, không gộp các quan sát seed × prompt như thể chúng độc lập để tạo CI hẹp; variation across training run và uncertainty across questions là hai tầng khác nhau, cần báo riêng hoặc dùng quy trình tổng hợp đã định trước.

Tất cả hyperparameter (mô hình nền, LoRA/QLoRA $r$, $\alpha$, learning rate, epoch, length, DPO $\beta$, generation template) chỉ chọn bằng validation. Test khóa chỉ dùng một lần cho tổng kết. Nếu tính toán không đủ để hoàn thành 5 run, nhóm phải xin điều chỉnh **với giảng viên** và ghi rõ số run thực hiện cùng lý do; không ngầm giảm chuẩn, không chỉ dựa vào đồng thuận nội bộ, và không thay 5 seed bằng 5 generations.

### 7.3. Cầu nối A–D cần dữ liệu thật

Để đáp ứng yêu cầu phần A tham gia so sánh hoặc dùng trực tiếp ở D, một minibatch từ `DPO_PAIR` Phần D đã review sẽ được token hóa theo template SFT/DPO. Cả custom DPO và thư viện chuẩn nhận cùng `input_ids`, response token mask, candidate chosen/rejected, policy/ref checkpoint và reduction. Với vanilla DPO, `sequence log-prob` là **tổng** log-prob token thuộc phần trả lời đã mask và loss là trung bình theo ví dụ trong batch, không chuẩn hóa trung bình token như PPL. Log artifact phải lưu `pair_id` (hoặc hash nếu dữ liệu hạn chế), length/mask, tổng log-prob chosen/rejected, margin, loss, gradient đã chọn để đối chiếu và sai khác số học.

Đây là đối chiếu trên log-prob và gradient từ forward/backward pass **thật**, không dùng scalar điền tay. Với trạng thái tham số chung, so sánh gradient autograd theo logit đã mask hoặc tham số adapter có thể đối chiếu. Trước khi quy lỗi khác biệt, kiểm tokenizer, padding side, mask prompt/response, truncation, label shift, beta, ref adapter và batch reduction. Kết quả chỉ được kết luận sau run; kế hoạch này không khẳng định sai số hay độ khớp đã đo.

## 8. Rủi ro dữ liệu và điều kiện dừng

| Rủi ro | Dấu hiệu | Hành động |
|---|---|---|
| Nguồn thiếu quyền/robots hoặc thay đổi | Không xác minh được terms/phiên bản; hash khác sau truy xuất | Không ingest/không phân phối; ghi rejected/superseded và thay nguồn hợp lệ sau khi chốt phạm vi |
| Citation không hỗ trợ claim | Review phát hiện span không nói điều đáp án khẳng định | Sửa/loại QA, gắn `needs_refusal`; audit các record chung template/span |
| QA/pair chưa đủ số lượng đã kiểm | Count `approved`/`adjudicated` thấp | Pilot và điều phối sớm; báo count thật; không đánh dấu hoàn thành ngưỡng |
| Thiếu hai người chấm | Không có nhãn độc lập | Dừng tạo train DPO từ cặp đó; chốt người chấm trước khi mở rộng generation |
| Không có consent/khảo sát | Không có `granted` hoặc PII chưa redaction | Không lưu vào test; không tuyên bố test người dùng thật |
| Near duplicate/rò rỉ split | Audit phát hiện chung prompt/span/family/cluster | Di chuyển/loại record, tạo split version mới trước train; ghi quyết định |
| GPU/budget làm chậm pilot/5 run | OOM hoặc hết quota | Pilot SFT và DPO ref riêng; log cấu hình; xin điều chỉnh minh bạch nếu không thể đáp ứng 5 run |

## 9. Deliverables tuần 1 và mốc tuần 2

**Tuần 1:** chốt ba tiền điều kiện; tạo sổ nguồn/schema/rubric và split policy; kiểm một mẫu nguồn hợp lệ; thử 5–10 thủ tục/20–50 QA chỉ khi quyền và phạm vi đã được chốt; khởi động SFT pilot cuối tuần 1 nếu có dữ liệu pilot đủ điều kiện.

**Cuối tuần 1–đầu tuần 2:** dùng checkpoint pilot để tạo candidate DPO, chạy hai người chấm độc lập và thống kê agreement; tiếp tục tăng dữ liệu SFT/DPO theo count đã review. Mốc tuần 2 của đề bài là bộ dữ liệu Phần D cùng A/B cho báo cáo tiến độ; vì vậy cần ưu tiên thiết lập pipeline preference sớm thay vì đợi đến sau khi đóng dữ liệu SFT.

Không có mục nào trong tài liệu này tuyên bố rằng 2.000 QA, 500 cặp, khảo sát thật, checkpoint hay 5 run đã hoàn thành. Mọi số liệu cuối phải dẫn về dataset/run manifest tương ứng.

## 10. Bằng chứng hiện tại và điều kiện bàn giao tiếp

| Hiện vật | Đã thực hiện | Chưa được suy ra |
|---|---|---|
| Sổ nguồn, robots/terms và bản đọc có hash | 9 nguồn, 5 họ thủ tục; ghi rõ thiếu nguồn/khác biệt phiên bản | Không có nghĩa tất cả nguồn còn hiệu lực, được phép train/phân phối |
| Pilot QA | 20 QA agent-authored, 21 trích đoạn; kiểm cấu trúc; phiếu người rà ghi 18 “Chấp nhận”, 2 “Sửa câu hỏi” | Không thay kiểm thủ công tập chính, không phải khảo sát; 0 bản ghi `approved`, 0 QA đủ điều kiện train |
| Truyện Kiều, bản Trương Vĩnh Ký 1911 | Nhóm chạy A.2 trên Kaggle riêng tư; `summary.json` có PPL validation 10,1948 ± 0,0628 (SD mẫu, 5 seed) | Không phải số đo VRAM phần D, chưa đối chiếu log/checkpoint Kaggle và không suy ra quyền phân phối lại |
| Consent/khảo sát/chấm | Có văn bản mẫu, quy trình ẩn danh và phiếu/rubric | Chưa có xác nhận vận hành, consent, người tham gia hoặc nhãn thật |

Ưu tiên trước mắt: giải quyết hiệu lực/quyền nguồn D, khác biệt thời hạn và biểu phí; sửa và kiểm lại hai QA bị gắn cờ; chốt hình thức consent, lịch và kho riêng. SFT pilot trước mốc dữ liệu tuần 2 đang thiếu đầu vào; chỉ chạy khi QA đủ điều kiện và báo rủi ro nếu không kịp, không đánh dấu hoàn thành dựa trên kế hoạch.
