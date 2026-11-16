# Hướng dẫn kiểm QA, gán nhãn preference DPO và đánh giá mù

> **Trạng thái:** protocol trước vận hành con người. Đã có 20 QA nháp do agent biên soạn và kiểm cấu trúc ở kho nghiên cứu riêng, nhưng **chưa có QA được con người phê duyệt**, candidate SFT, nhãn người chấm, agreement, cặp DPO hay kết quả đánh giá. Schema/quy tắc không phải record gán nhãn thật.

## 1. Phạm vi, vai trò và điều kiện mở việc

Hướng dẫn này áp dụng cho ba luồng tách biệt:

1. kiểm thủ công QA SFT theo citation;
2. gán nhãn hai đáp án SFT cho cùng prompt để tạo `DPO_PAIR`;
3. đánh giá mù cuối cùng trên tập **khác** dữ liệu DPO.

Cao Văn Hà tổng hợp vận hành và chỉ phân xử **sau** khi nhãn độc lập đã bị khóa. Hà Mạnh Thế và Trần Duy Hưng chấm độc lập mọi cặp DPO hợp lệ; không chia đôi số cặp giữa hai người. Không người nào được tự xem nhãn của người còn lại trước khi khóa. Khi chưa xác nhận được lịch và quyền truy cập, chỉ có thể chuẩn bị rubric, không được ghi nhận là đã chấm.

Chỉ phê duyệt QA cho huấn luyện khi source provenance/quyền dùng/phiên bản và citation span đã được chấp nhận theo `data-plan.md`. Có thể rà soát nghiên cứu trước đó để tìm lỗi hoặc ghi `uncertain`, nhưng không nâng thành dữ liệu được phép dùng. Chỉ mở DPO labeling khi đồng thời có:

- checkpoint SFT thực, tokenizer, prompt template và config generation đã đóng băng cho batch;
- đúng hai candidate được sinh cho **cùng một prompt**; text cùng candidate ID bất biến sau khi phát hành cho rater;
- citation/source span có thể kiểm đối chiếu, và batch không có dữ liệu `USER_TEST`;
- `pair_id`, `prompt_id`/`qa_id`, split cấp họ thủ tục và provenance đã được tạo;
- giao diện/phiếu chấm đảm bảo mỗi rater có ánh xạ A/B riêng, không thấy model/checkpoint identity, canonical candidate ID, nhãn hay lý do của người kia.

`USER_TEST` luôn bị tách: không được dùng làm QA authoring, prompt DPO, calibration, tập nhãn DPO hoặc chọn tiêu chí. Việc không có `USER_TEST` hợp lệ không cho phép tạo câu hỏi giả và gọi đó là khảo sát.
Split được khóa trước authoring/generation: mọi QA/DPO thuộc cùng `procedure_family_id` (và các paraphrase/span liên quan theo audit) phải ở một split nhất quán; không random từng câu để làm rò quy trình. Mọi câu của một `respondent_cluster_id` ở `USER_TEST` cùng nằm trong tập heldout, không được rải sang train/validation hoặc dùng làm prompt DPO. Bất kỳ xung đột nào phát hiện sau audit tạo dataset/split version mới trước huấn luyện, không được nới rule sau khi xem metric.


## 2. Quy tắc chung về record và dữ liệu cấm

- ID (`qa_id`, `pair_id`, `candidate_id`, `annotation_id`, `evaluation_pair_id`) là UUID/chuỗi bất biến, không mã hóa nội dung hay danh tính. Không đổi ID để che sửa lỗi.
- Bản ghi tạo thành append-only audit trail. Thay đổi text, citation, split, rubric hoặc label tạo `record_version` mới và liên kết `supersedes`; record cũ không bị ghi đè.
- Không đưa vào annotation reason tên, số liên hệ, hồ sơ, địa chỉ, thông tin sức khỏe/tài chính hoặc dữ liệu người tham gia. Flag privacy là lý do loại, không phải nơi chép lại PII.
- `candidate_0_id`/`candidate_1_id` là thứ tự canonical chỉ để lưu trữ. Ký hiệu A/B rater nhìn thấy là thứ tự hiển thị ngẫu nhiên, riêng cho từng rater và lưu tách trong `display_map`.
- Không sửa candidate sau khi rater có thể thấy nó. Nếu lỗi generation/citation cần sửa, loại cặp và sinh `pair_id`/candidate version mới; không dùng nhãn cũ.
- Chất lượng văn phong, độ dài, sự tự tin hoặc câu chữ giống người chấm **không** là lý do ưu tiên độc lập. Chỉ dùng chúng khi ảnh hưởng trực tiếp đến đúng/sai, đầy đủ, citation, an toàn hoặc khả năng từ chối theo rubric.

## 3. Kiểm thủ công QA SFT theo citation

### 3.1. Đơn vị và cỡ kiểm

Một `qa_record` chỉ được review khi mọi mệnh đề thông tin chính trong `answer_text` có `claim_coverage` chỉ rõ `source_span_id` và trạng thái hỗ trợ. QA thiếu nguồn đủ căn cứ phải bị gắn `needs_refusal`, sửa để giới hạn/từ chối, hoặc loại; người review không được tự bổ sung kiến thức ngoài span.

Với **mỗi split SFT được dùng** cho train hoặc validation, chọn mẫu ngẫu nhiên phân tầng theo `scope_group`, `question_origin` và nguồn/phiên bản, cỡ tối thiểu:

$$n_{manual} = \lceil 0{,}20 \times N_{split} \rceil.$$

Vì vậy nếu train có 2.000 QA thì cần kiểm ít nhất 400 QA train; validation có quota riêng theo công thức, không dùng 400 train để thay thế. Pilot có tối đa 100 QA phải được người review kiểm thủ công **100%** trước khi dùng cho bất kỳ mục đích huấn luyện/pipeline nào. Đây là quota kiểm thực tế: không đánh dấu `reviewed` hoặc `approved` trước khi người thực hiện ghi review.
Kiểm tự động hoặc AI-assisted check chỉ có thể tạo cờ `duplicate_candidate`, `citation_missing`, `format_error` hay rủi ro tương tự. Nó dùng một record/audit tách với phiếu `qa_manual_review`, không được tự đổi `decision` thành `approved`, không thay quota review người, và không được dùng cùng một kết quả AI làm “người kiểm” thứ hai.


Nếu phát hiện lỗi hệ thống (cùng template, span, source version, procedure family hoặc generator), dừng phát hành batch liên quan, audit rộng hơn mẫu 20%, sửa/loại batch và tạo version mới. Không chỉ sửa những record tình cờ được lấy mẫu.

### 3.2. Phiếu kiểm QA — trường bắt buộc

Người review nhìn QA, citation span và metadata nguồn cần thiết; họ ghi một phiếu `qa_manual_review` cho từng `qa_id` được lấy mẫu.

| Trường | Kiểu/giá trị | Quy tắc ghi |
|---|---|---|
| `qa_review_id` | ID bất biến | Một lần review cho một phiên bản QA |
| `qa_id`, `qa_record_version`, `dataset_version` | FK/string | Trỏ đúng record/release được kiểm |
| `reviewer_id`, `reviewed_at` | ID vai trò, ISO-8601 | Không dùng tên người tham gia |
| `sampling_stratum`, `sampling_seed`, `sampled_at` | string/int/time | Chứng minh lấy mẫu phân tầng tái lập |
| `source_version_ids`, `citation_span_ids_checked` | mảng FK | Những nguồn/span thực đã mở để kiểm |
| `content_correctness` | `pass`, `fail`, `uncertain` | Mỗi mệnh đề chính đúng với span hay không |
| `completeness` | `pass`, `fail`, `not_applicable` | Trả lời đủ phần câu hỏi trong phạm vi span |
| `citation_verifiability` | `pass`, `fail` | Citation trỏ đúng span, locator và phiên bản |
| `scope_and_refusal` | `pass`, `fail`, `not_applicable` | Có giới hạn/từ chối đúng nếu thiếu căn cứ/ngoài scope |
| `hallucination_flag` | boolean | Có claim thông tin không được span hỗ trợ |
| `privacy_flag` | boolean | Có PII/chi tiết không được phép trong QA/citation render |
| `duplicate_or_leakage_flag` | boolean | Dấu hiệu trùng/rò split cần audit tiếp |
| `decision` | `approved`, `rework`, `rejected` | `approved` chỉ khi không có lỗi chặn |
| `reason_codes`, `review_note` | mảng mã/text ngắn | Không chép PII; nêu claim/span hoặc mã lỗi |
| `follow_up_batch_key` | nullable string | Template/source/family cần audit nếu lỗi hệ thống |

`uncertain` không được đổi thành `pass` vì văn phong trôi chảy. Nó dẫn tới `rework` hoặc `rejected` cho đến khi có căn cứ nguồn. Một QA được sửa sau review phải đi lại luồng citation và review theo phiên bản mới nếu được chọn/thuộc batch bị mở rộng audit.

## 4. Rubric lựa chọn preference DPO

Mỗi rater chọn **một** nhãn sau cho A và B đã được đảo thứ tự:

- **A tốt hơn:** A tốt hơn B một cách rõ ràng theo rubric.
- **B tốt hơn:** B tốt hơn A một cách rõ ràng theo rubric.
- **Tương đương:** cả hai đáp án tương đương về chất lượng đối với prompt và nguồn; không có ưu thế rõ ràng đáng để huấn luyện preference.
- **Không hợp lệ/không đủ điều kiện:** không thể tạo so sánh công bằng hoặc cặp vi phạm điều kiện, ví dụ candidate bị cắt hỏng, candidate trùng hệt, thiếu nguồn/span để đối chiếu, prompt/candidate chứa PII, sai prompt, lỗi hiển thị, hoặc provenance không đầy đủ.

Rater phải ưu tiên các trục theo thứ tự sau, ghi mã lý do áp dụng:

1. **Đúng với nguồn (`correctness`):** mệnh đề thông tin có được source span hỗ trợ; không đổi địa phương/điều kiện/hiệu lực; không bịa.
2. **Đầy đủ trong phạm vi (`completeness`):** trả lời các phần có thể trả lời của prompt, nêu điều kiện/giới hạn thiết yếu đã có căn cứ, không thêm chi tiết không cần thiết.
3. **Citation có thể kiểm (`citation`):** citation đúng span/phiên bản và thật sự chống đỡ claim; citation sai hoặc trang chung không hỗ trợ claim là lỗi.
4. **Từ chối/giới hạn đúng (`refusal_scope`):** khi prompt ngoài phạm vi, thiếu căn cứ hoặc có rủi ro, đáp án không đoán và hướng người dùng kiểm nguồn/cơ quan phù hợp; đồng thời không từ chối sai câu có đủ căn cứ trong scope.
5. **Khả năng dùng được (`clarity_after_substance`):** chỉ sau bốn trục trên; cấu trúc rõ được ghi nhận nếu làm người dùng hiểu đúng, không ưu ái phong cách hoa mỹ.

Mã lý do chuẩn hóa: `supported_claims`, `unsupported_claim`, `missing_required_condition`, `wrong_locality_or_version`, `citation_mismatch`, `citation_missing`, `appropriate_refusal`, `incorrect_refusal`, `scope_violation`, `privacy_risk`, `duplicate_candidates`, `generation_truncation`, `source_unavailable`, `display_error`, `equivalent_substance`. Có thể ghi nhiều mã. Rater viết nhận xét ngắn dẫn chiếu candidate A/B và claim/citation, không viết lại thông tin nhạy cảm.

### Khi nào là hòa, khi nào là ưu tiên không cân bằng

Chọn **Tương đương** nếu hai đáp án đều đúng/đủ ở mức tương tự, cùng có một hạn chế nhỏ tương đương, hoặc khác nhau chủ yếu ở văn phong/độ dài mà không làm đổi bốn trục đầu. Không buộc chọn một bên chỉ vì DPO cần chosen/rejected.

Chọn A/B khi một bên có ưu thế thực chất: một candidate có claim không được hỗ trợ, bỏ điều kiện cần thiết, citation không kiểm được, xử lý sai scope/từ chối, hoặc bên kia khắc phục rõ ràng khác biệt đó. “A ngắn hơn”, “B có vẻ tự tin hơn” hay “câu chữ thích hơn” không đủ để phá hòa.

Chọn **Không hợp lệ** thay vì hòa khi không thể đánh giá công bằng. Cặp không hợp lệ không biến thành tie và không được đưa DPO. Tie cũng không được đưa DPO: hai kết quả này phải được báo riêng.

## 5. Phiếu nhãn độc lập và schema `preference_pair`

### 5.1. Phiếu mỗi rater thực sự điền

Mỗi rater nhận `pair_id`, prompt, source/citation material được phép đối chiếu và hai đáp án mang nhãn A/B. Họ không nhận `candidate_0_id`, `candidate_1_id`, checkpoint/model identity, nhãn/lý do của rater còn lại, hoặc quyết định phân xử.

| Trường phiếu | Giá trị/cách điền |
|---|---|
| `pair_id`, `pair_version`, `rubric_version` | Hệ thống điền, rater kiểm phiên bản |
| `prompt_text` hoặc `prompt_id` | Prompt đóng băng của cặp |
| `A_text`, `B_text` | Hai candidate theo display map bí mật với rater |
| `source_material_ids` | Span/citation có thể kiểm, không phải nhãn người khác |
| `rater_id`, `started_at`, `submitted_at` | Audit độc lập |
| `label_raw` | Chọn đúng một: `A`, `B`, `tie`, `invalid` |
| `reason_codes` | Chọn các mã rubric áp dụng |
| `reason_text` | Nhận xét ngắn dựa trên nguồn, không PII |
| `blocking_issue` | `none`, `source`, `privacy`, `generation`, `display`, `provenance`, `other` |
| `attestation` | “Tôi chưa xem nhãn/lý do của rater khác cho cặp này.” |

Hệ thống/điều phối viên lưu **riêng** `rater_display_map`, chẳng hạn ánh xạ `A`/`B` đến canonical candidate, không hiện ánh xạ cho rater. Nó phải được tạo trước khi phát cặp, riêng cho mỗi rater, bằng randomization đã lưu seed/audit và phải đảo cân bằng trên batch. Normalization không được thực hiện bằng đoán thứ tự A/B.

### 5.2. Record kho `preference_pair`

| Trường | Kiểu/giá trị | Ràng buộc vận hành |
|---|---|---|
| `pair_id`, `pair_version` | ID/string bất biến | Cặp mới nếu candidate/prompt bị sửa |
| `split` | `train`, `validation`, `test` | Group split theo prompt/procedure family trước nhãn |
| `qa_id` hoặc `prompt_id`, `prompt_text_hash` | FK/hash | Cùng một prompt cho hai candidate; không dùng `USER_TEST` |
| `procedure_family_id`, `scope_group` | string | Không rải cùng family qua split |
| `sft_checkpoint_id`, `tokenizer_id`, `prompt_template_id` | ID/hash | Provenance đóng băng |
| `generation_config` | object bất biến | seed, temperature, top-p, max tokens và setting liên quan |
| `candidate_0_id`, `candidate_1_id` | ID bất biến | Canonical, không lộ cho rater |
| `candidate_0_text_hash`, `candidate_1_text_hash` | SHA-256 | Phát hiện sửa text sau nhãn |
| `candidate_0_citation_ids`, `candidate_1_citation_ids` | mảng FK | Citation để reviewer đối chiếu |
| `rater_1_id`, `rater_2_id` | ID vai trò/pseudonymous | Là Hà Mạnh Thế và Trần Duy Hưng theo phân công đã chốt, không thay phiên chia đôi cặp |
| `rater_1_display_map`, `rater_2_display_map` | object bí mật | A/B → candidate ID, khác/đảo cân bằng theo rater |
| `rater_1_label_raw`, `rater_2_label_raw` | `A`, `B`, `tie`, `invalid` | Khóa trước khi xem nhãn còn lại |
| `rater_1_label_normalized`, `rater_2_label_normalized` | `candidate_0`, `candidate_1`, `tie`, `invalid` | Derived từ raw + map, dùng thống kê |
| `rater_1_reason_codes`, `rater_2_reason_codes` | mảng mã | Lưu nguyên bản sau submit |
| `rater_1_at`, `rater_2_at` | timestamp | Audit độc lập |
| `independent_agreement` | `agree_winner`, `agree_tie`, `agree_invalid`, `disagree`, `pending` | Derived **trước** phân xử |
| `adjudication_label` | `candidate_0`, `candidate_1`, `exclude`, null | Chỉ sau khóa nhãn và thống kê sơ bộ |
| `adjudicator_id`, `adjudicated_at`, `adjudication_reason` | audit | Cao Văn Hà phân xử theo nguồn/rubric, không sửa raw labels |
| `chosen_candidate_id`, `rejected_candidate_id` | derived/null | Chỉ có với strict preference cuối cùng |
| `status` | `pending`, `labeled`, `adjudicated`, `excluded` | Không suy ra completed khi chưa có nhãn thật |

## 6. Trình tự hai người chấm, khóa nhãn và phân xử

1. Điều phối viên tạo immutable pair batch, kiểm hash candidate/provenance và randomize display map độc lập. Hai rater nhận **toàn bộ** cặp batch theo lịch, không nhận một nửa mỗi người.
2. Mỗi rater chấm độc lập, nộp phiếu và khóa nhãn của chính họ. Nếu phải sửa lỗi nhập, tạo amendment audit trước khi nhãn còn lại được mở; không xóa dấu vết.
3. Khi cả hai đã khóa hoặc batch đóng theo quy tắc đã công bố, hệ thống normalize A/B → candidate ID, tính `independent_agreement` và thống kê sơ bộ. Cao Văn Hà chưa xem/chọn bất kỳ winner nào trước bước này.
4. Nếu cùng chọn `candidate_0` hoặc `candidate_1`, cặp có strict preference nhất trí; vẫn phải qua kiểm hash/split trước khi DPO ingest. Nếu cùng `tie`, loại khỏi DPO và báo là hòa nhất trí. Nếu cùng `invalid`, loại và báo lý do invalid.
5. Nếu bất đồng winner–winner hoặc winner–tie, Cao Văn Hà đối chiếu prompt, nguồn, rubric và lý do đã khóa. Hà có thể chọn một candidate **chỉ khi** rubric/source cho strict preference rõ; nếu chứng cứ vẫn cân bằng hoặc không đủ, chọn `exclude`. Không dùng phân xử để ép tie thành winner chỉ nhằm đạt quota.
6. Nếu ít nhất một nhãn `invalid`, ưu tiên điều tra blocking issue. Cặp thường bị `exclude`; chỉ tạo cặp mới sau khi lỗi được sửa như một record mới. Không giữ candidate cũ và sửa im lặng.
7. Chỉ strict preference có `chosen_candidate_id` và `rejected_candidate_id`, provenance đầy đủ, split hợp lệ, không PII và không lỗi blocking mới được xuất DPO. Cặp tie, invalid, excluded và pair thiếu hai nhãn không thành `DPO_PAIR` train/validation.

Cao Văn Hà lưu lý do phân xử; không được ghi đè nhãn raw, normalised label hay lý do của Hà Mạnh Thế/Trần Duy Hưng. Nếu availability không cho hai người chấm mọi cặp, dừng cặp đó thay vì gắn “hai đánh giá” không có thật.

## 7. Agreement báo cáo trước phân xử

Tính thống kê trên các cặp có **cả hai** nhãn normalized hợp lệ trong tập:

$$\mathcal{C}_{valid} = \{i: y_{i,1}, y_{i,2} \in \{candidate\_0, candidate\_1, tie\}\}.$$

`invalid`, nhãn thiếu và cặp lỗi hiển thị bị loại khỏi mẫu số của $\kappa$ theo protocol này, nhưng phải báo count/tỷ lệ riêng. Tỷ lệ đồng thuận pre-adjudication là tỷ lệ hai nhãn normalized giống nhau trên $\mathcal{C}_{valid}$; bao gồm đồng thuận `tie`, vì đây là một nhãn hợp lệ và xử lý đối xứng với hai candidate.

Với ba category trên, dùng Cohen’s kappa:

$$\kappa=\frac{p_o-p_e}{1-p_e},$$

trong đó $p_o$ là tỷ lệ đồng thuận quan sát và $p_e$ là tỷ lệ đồng thuận kỳ vọng từ biên phân phối nhãn của hai rater. Báo: `N_total`, `N_valid_both`, `N_invalid_or_missing`, ma trận 3×3 normalized, $p_o$, $p_e$, $\kappa$, tỷ lệ tie, tỷ lệ invalid, và tỷ lệ bất đồng trước phân xử.

Nếu $p_e=1$, mẫu số bằng 0 và $\kappa$ **không xác định**; báo `kappa = undefined (p_e = 1)` cùng ma trận/count, không thay bằng 0, 1 hoặc giá trị thuận tiện. Không tính kappa sau adjudication, không coi decision của Cao Văn Hà là nhãn độc lập, và không suy ra agreement cao chỉ từ một category phổ biến.

## 8. Calibration trước nhãn chính

Ba người có thể cùng làm một lô calibration nhỏ để thống nhất cách dùng rubric, nhưng lô này phải gồm ví dụ **tổng hợp/hư cấu chỉ để minh họa** hoặc record đã được phép dùng rõ ràng. Nó mang nhãn `calibration_only = true`, `not_sft = true`, `not_dpo = true`, không được export vào SFT/DPO/test và không được tính vào quota 500 cặp. Nếu rubric đủ rõ mà chưa có ví dụ an toàn, có thể bỏ calibration; không được tạo QA/candidate giả rồi tính như dữ liệu thật.

Calibration tập trung vào: citation hỗ trợ không đầy đủ; khác biệt điều kiện/thẩm quyền địa phương; câu trả lời ngoài scope cần từ chối; hòa thực chất; và invalid do thiếu nguồn/PII. Sau calibration, chỉ version rubric đã chốt mới dùng cho batch chính; thay rubric giữa batch tạo version và ghi scope ảnh hưởng.

## 9. Đánh giá mù pairwise cuối cùng — tách khỏi DPO

Đánh giá cuối cùng so sánh base, SFT và SFT+DPO trên `USER_TEST` hợp lệ đã khóa; nếu không có `USER_TEST` hợp lệ, báo thiếu tập test người dùng thực thay vì thay bằng prompt train-derived. Cặp đánh giá phải thỏa tất cả điều kiện:

- prompt/evaluation pair **không** thuộc DPO train/validation, không là QA authoring, không là calibration, không là candidate đã dùng để chọn hyperparameter;
- không có overlap prompt, paraphrase gần, `source_span_id`, `procedure_family_id` hay `respondent_cluster_id` trái split policy với dữ liệu train/validation; audit leakage diễn ra trước mở nhãn;
- evaluator không biết identity/thứ tự model; display A/B được randomize độc lập và lưu map tách biệt;
- cặp có thể dùng cùng prompt cho so sánh mô hình đã định trước, nhưng mỗi so sánh lưu `evaluation_pair_id` riêng, model IDs chỉ mở sau khi khóa nhãn;
- rubric evaluation dùng đúng/đầy đủ/citation/hallucination/từ chối; không chấm “văn hay” thay chất lượng; `tie` và `invalid` có nghĩa như mục 4.

### Schema `blind_evaluation_pair`

| Trường | Nội dung/ràng buộc |
|---|---|
| `evaluation_pair_id`, `evaluation_version` | ID bất biến, tách `pair_id` DPO |
| `test_question_id`, `respondent_cluster_id` | FK trong kho test khóa; cluster chỉ dùng phân tích, không lộ evaluator |
| `comparison_id` | So sánh định trước, ví dụ base-vs-SFT; không hiện tên model cho evaluator |
| `candidate_left_id`, `candidate_right_id` | ID output bất biến; model mapping niêm phong |
| `display_map` | A/B → candidate ID, tạo trước nhãn |
| `answer_A`, `answer_B`, `citation_material_ids` | Material evaluator kiểm; không chứa PII |
| `evaluator_id`, `label_raw`, `label_normalized`, `reason_codes`, `submitted_at` | Nhãn mù và audit |
| `validity_status` | `valid`, `invalid`, `excluded_privacy`, `excluded_technical` |
| `cluster_definition_version` | Khai báo đơn vị cụm được dùng cho CI |
| `model_mapping_revealed_at` | Chỉ có sau khóa toàn bộ nhãn cần thiết |

Protocol không cấm tuyệt đối người chấm DPO tham gia đánh giá cuối, nhưng nếu evaluator thuộc nội bộ nhóm hoặc từng chấm DPO thì phải nêu rõ giới hạn thiên lệch trong báo cáo; không mô tả là đánh giá độc lập từ bên ngoài.

### Win rate và khoảng tin cậy

Sau khi mở model map của các nhãn hợp lệ, với một mô hình đang xét, đặt $W$, $T$, $L$ lần lượt là số thắng, hòa và thua trong một comparison đã định trước. Báo:

$$\operatorname{WinRate}=\frac{W+0{,}5T}{W+T+L}.$$

`invalid`/technical/privacy exclusions không vào mẫu số và phải báo riêng cùng lý do. Dùng **95% bootstrap theo `respondent_cluster_id`**: resample cụm có hoàn lại, giữ mọi question/evaluation pair thuộc cùng cụm trong lần resample, tính lại statistic; báo số cụm, số câu, số cặp hợp lệ, số lần resample, seed, percentile CI và `cluster_definition_version`. Nếu mỗi câu độc lập theo thiết kế và không có lặp người, khai báo cluster là `test_question_id`; không mặc định mỗi seed×prompt hay mỗi answer là quan sát độc lập.

Không dùng bootstrap câu-level khi một người đã gửi nhiều câu mà token cụm còn tồn tại. Không gộp các comparison khác nhau, các seed training hoặc nhiều decode của cùng output thành quan sát độc lập để làm CI hẹp. Nếu số cụm không đủ cho CI có ý nghĩa, vẫn báo count/điểm ước lượng kèm giới hạn; không bịa CI.

## 10. Checklist bàn giao trước vận hành

- [ ] Nhóm xác nhận người tạo QA, reviewer QA, Hà Mạnh Thế, Trần Duy Hưng, Cao Văn Hà và evaluator (nếu có) cùng lịch tối thiểu.
- [ ] Source/citation review, schema version, split policy và ACL đã được xác nhận; không có `USER_TEST` trong authoring/DPO batch.
- [ ] Pilot QA ≤100 nếu được dùng đã có review người thật 100%; các split khác có kế hoạch lấy mẫu $\lceil0{,}20N\rceil$.
- [ ] Checkpoint/config/candidate hash và A/B maps được đóng băng trước rater.
- [ ] Cả hai rater nhận toàn bộ cặp, biết `tie`/`invalid` là hợp lệ và biết không ưu ái văn phong.
- [ ] Raw labels được khóa; agreement normalized và kappa pre-adjudication được tính/báo trước phân xử.
- [ ] Chỉ strict preferences cuối cùng được đưa DPO; tie/invalid/exclude có count tách biệt.
- [ ] Evaluation set/pairs khác DPO, model map sealed, cluster rule và bootstrap CI 95% được công bố trước chấm.

Các ô checklist chỉ được đánh dấu sau sự kiện thực có audit tương ứng. Chúng không thay thế dữ liệu, nhãn human hay approval.