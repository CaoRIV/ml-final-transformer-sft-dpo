# Gói kiểm chứng dữ liệu tuần 1

Đây là bộ hiện vật phục vụ đề cương/kế hoạch dữ liệu, không phải release huấn luyện hoặc dữ liệu khảo sát đã thu thập. Phạm vi: Hà Nội, hộ tịch–chứng thực; Truyện Kiều chỉ cho mô hình ký tự phần A.

## Đọc theo thứ tự

1. [Hiệu lực và quyền dùng nguồn D.1](source-audit.md), [sổ nguồn, URL và hash](source-ledger.json).
2. [Mẫu 20 QA nghiên cứu: vị trí, bằng chứng và cách review](admin-pilot.md), [báo cáo kiểm cấu trúc](admin-pilot-report.json).
3. [Provenance/audit Truyện Kiều](char-corpus.md), [báo cáo số đo thực](char-corpus-audit-report.json).
4. [Văn bản đồng ý và phiếu khảo sát](consent-and-survey.md).
5. [Lưu trữ, ẩn danh và rút dữ liệu](privacy-workflow.md).
6. [Phiếu kiểm QA, rubric DPO và đánh giá mù](annotation-guide.md).
7. [Triển khai D.2: tạo QA, kiểm thủ công, khóa riêng khảo sát](#triển-khai-d2).

## Trạng thái bàn giao

| Nhánh | Đã có | Còn chặn |
|---|---|---|
| Nguồn thủ tục | D.1: đã đối chiếu 5 họ, có 1818/1852 và phụ lục, biểu lệ phí Hà Nội 98/2026, hồ sơ xác nhận đúng mã `2.002516`; có căn cứ dùng chính văn công khai để soạn QA | Chưa chốt toàn bộ quy trình/kênh Hà Nội; không dùng nguyên trạng 9 snapshot pilot cho train/phân phối |
| QA | 20 QA pilot cũ đã được nhóm rà nội dung; D.2 có 24 QA ứng viên mới, căn cứ chính văn, chia họ và khóa mẫu kiểm | Hai gói đều chưa đủ điều kiện train. Pilot cũ không được chuyển nguyên trạng; tập chính còn thiếu QA và kiểm thủ công. |
| Corpus ký tự | [Trương Vĩnh Ký 1911](char-corpus.md), 3.254 dòng; đã có PPL validation 5 seed từ `summary.json` người dùng gửi | Chưa đối chiếu log môi trường và checkpoint Kaggle; hiện vật riêng ngoài Git |
| Khảo sát/chấm | Consent/phiếu giấy, quy trình riêng tư, công cụ khóa `USER_TEST` cho evaluator và rubric | Chưa có phê duyệt vận hành, người tham gia, consent hợp lệ, `USER_TEST`, checkpoint SFT hay nhãn DPO. |

## Chạy lại kiểm tra

Các lệnh chạy từ thư mục gốc repo, dùng thư viện chuẩn Python. Không cài lại PyTorch.

```sh
python scripts/validate_admin_pilot.py --output docs/data/admin-pilot-report.json
python scripts/validate_admin_pilot.py --require-training-ready
python -m unittest discover -s tests -p "test_char_corpus.py" -v
```

- Lệnh đầu kiểm dữ liệu nghiên cứu cục bộ và tạo báo cáo; nó không cấp quyền/nhãn con người.
- Lệnh thứ hai hiện phải trả **mã 2**, vì train release đang bị chặn. Không sửa cờ thành `true` để làm lệnh đạt.
- Kiểm thử hồi quy dùng HTTP loopback cục bộ để bảo đảm không theo redirect đến một đích chưa được robots kiểm; không truy cập mạng Internet.
- Khi clone repo mới, `data/review/admin-pilot-v1/` và `.cache/admin-source-audit/` không có vì đã ignored. Cần nhận bundle riêng đã được kiểm quyền từ người phụ trách trước khi kiểm lại; không tự tạo snapshot hoặc nhãn thay thế để làm lệnh đạt. Hash giúp đối chiếu đúng phiên bản, không thay quyền chia sẻ.

Để chuẩn bị hoặc kiểm tra lại corpus Truyện Kiều 1911, xem [lệnh và hồ sơ nguồn](char-corpus.md#4-chuẩn-bị-cục-bộ-và-xác-nhận-quyền). Giữ file nguồn và hiện vật dưới `.cache/char-corpus/` hoặc kho riêng; khi chuẩn bị lại, chọn đường dẫn đích mới. Không dùng snapshot audit `206607` để train.

## Triển khai D.2

Đề tài 9, tr. 19 yêu cầu ≥2.000 QA có trích dẫn sinh bán tự động, kiểm thủ công ≥20%, test là câu hỏi thật từ khảo sát tách khỏi huấn luyện. Thiết kế của nhóm giữ ≥2.000 **train** với validation riêng; pilot ≤100 QA được rà 100% trước khi dùng cho SFT thử. QA vòng `admin-pilot-v1` và đánh giá 20/20 của nhóm vẫn được bảo toàn, nhưng không chuyển kết luận v1/v2 sang trường hợp đã đổi nguồn.

### Hồ sơ pilot — `d2-official-seed-v2`

| Họ thủ tục | Split đã khóa | QA ứng viên |
|---|---|---:|
| Cấp bản sao trích lục hộ tịch | `train` | 10 |
| Chứng thực chữ ký (không phải chữ ký người dịch) | `train` | 6 |
| Cải chính hộ tịch | `train` | 2 |
| Xác nhận thông tin hộ tịch | `validation` | 6 |
| Chứng thực bản sao | `holdout` | 0 |

- **Thành phần và mục đích:** 24 QA tiếng Việt do AI soạn từ chính văn, 24 mệnh đề gắn 23 đoạn trích của 7 chứng cứ D.1. Bản v2 làm rõ thủ tục/kênh khi hỏi và sửa hai dẫn chứng bị lấy nhầm từ phần chữ ký người dịch trong bản nháp v1. Không dùng nội dung hay kết luận kiểm của 20 QA pilot cũ.
- **Căn cứ và quyền:** các câu về thời hạn kèm Quyết định 2163 chỉ nói theo phương án Bộ Tư pháp, không khẳng định Hà Nội đã triển khai; thời gian theo 1852 là **dự kiến**. Câu phí 858 chỉ về biểu phí chứng thực chữ ký tại UBND cấp xã; chưa đưa biểu lệ phí hộ tịch Hà Nội 98/2026 vào pilot (bản kiểm không có lớp chữ đủ để định vị bằng trình trích hiện tại). Chỉ làm việc với chính văn công khai theo [rà quyền D.1](source-audit.md#53-quyền-dùng-phân-loại-nội-dung-trước-khi-đưa-vào-dữ-liệu); không tự động mở huấn luyện hay công khai dữ liệu.
- **Trạng thái:** kiểm tự động định vị 24/24 mệnh đề trên snapshot đúng hash; bộ lọc từ vựng không báo cặp Jaccard ≥0,85. Sau đó nhóm duyệt 24/24 QA, chốt biên bản và phát hành `d2-official-seed-v2-release-01` để chạy [pilot SFT nội bộ](../progress/project-context.md#d3--kết-quả-pilot-do-nhóm-chạy-trên-kaggle). Việc phát hành chỉ áp dụng cho đúng bản đó; không suy ra chất lượng của tập chính hoặc quyền đưa lô mới lên Kaggle.
- **Lưu trữ:** giữ kết quả trong `data/review/d2/d2-official-seed-v2/`, snapshot dưới `.cache/admin-source-audit/d1/`. Chia sẻ mã/metadata theo quyền dự án, không đẩy các thư mục này hoặc hồ sơ khảo sát lên Git. Khi đổi chính văn/câu/đáp, tăng phiên bản liên quan và chạy lại cả kiểm citation và khóa split.

### Tập chính D.2 — lô ứng viên b01

Recipe `scripts/d2_main_b01_recipes.json` là phiên bản tích lũy: giữ nguyên nội dung và split của 24 QA v2, thêm **57 QA train** (26 chứng thực chữ ký, 17 cấp bản sao trích lục, 14 cải chính hộ tịch). Tổng **75 train, 6 validation**. Có tình huống đủ căn cứ để trả lời, thiếu căn cứ để nêu chi phí/giờ làm việc cụ thể, và ngoài phạm vi như giấy phép lao động. Không lấy câu hỏi thị thực trong demo, họ xác nhận thông tin hộ tịch, họ holdout hay khảo sát làm ví dụ train.

Trên máy nhóm, mở `data/review/d2/d2-official-main-b01/manual-review.csv`. Phiếu có 20 dòng (18 train, 2 validation), lấy ≥20% từng tầng rồi làm tròn lên, seed 42. Trong đó 14 dòng mới và 6 dòng kế thừa; không chép nhãn pilot sang phiếu của version này. Kiểm câu hỏi, từng mệnh đề và nguồn tại trang/đoạn tương ứng theo [rubric](annotation-guide.md#32-phiếu-kiểm-qa--trường-bắt-buộc). Đặc biệt, `BTP-PL-163` tr. 285–288 có lớp chữ trích bị mất ký tự: mở **trang PDF hiển thị** chứ không dùng riêng văn bản tách tự động để duyệt. Không đủ căn cứ thì ghi `rework` và nêu điểm cần sửa.

Lệnh tái tạo trên CPU vào **thư mục mới** (không tạo đè lên phiếu đang kiểm), và lệnh kiểm bản đang dùng:

```sh
python scripts/prepare_d2_qa.py prepare --stage main --recipes scripts/d2_main_b01_recipes.json --output data/review/d2/d2-official-main-b01-rebuild
python scripts/prepare_d2_qa.py check --recipes scripts/d2_main_b01_recipes.json --candidate data/review/d2/d2-official-main-b01 --review data/review/d2/d2-official-main-b01/manual-review.csv
```

**Chưa phát hành:** kiểm tự động định vị được 84 mệnh đề trên 82 đoạn thuộc 9 chứng cứ; không phát hiện cặp gần trùng ở ngưỡng Jaccard 0,85. Kết quả này không chứng minh đúng nghĩa hay hiệu lực hiện hành. Còn thiếu 1.925 QA train, kiểm người và biên bản nhóm. Lô sau cần thêm điều khoản/thủ tục có nguồn đã rà quyền và hiệu lực, khóa split theo họ trước khi soạn; không đạt chỉ tiêu bằng cách đổi cách diễn đạt. Tách test khảo sát người thật; quyền Kaggle Private của `release-01` không áp dụng cho b01.

### Tập chính D.2 — lô ứng viên b02

Tệp `data/review/d2/d2-official-main-b02/qa-moi.csv` chỉ chứa **54 câu mới**: 27 về chứng thực chữ ký, 17 về cải chính/bổ sung hộ tịch và 10 về cấp bản sao trích lục. Bốn cột là họ thủ tục, câu hỏi, đáp án có số văn bản và vị trí trích, nguồn gốc có URL. Đây là tệp đọc QA, không phải phiếu cần điền.

Lô tích lũy `qa.jsonl` ở cùng thư mục có **129 train, 6 validation**. Tái tạo bằng lệnh `prepare --stage main` như trên với recipe `scripts/d2_main_b02_recipes.json` và một thư mục đầu ra mới. Đã đối chiếu các trang hiển thị của phụ lục 163 với đoạn neo máy đọc, giữ phạm vi của từng văn bản (ví dụ mức phí *ghi trong phụ lục* không phải số tiền mọi hồ sơ phải nộp). Hai lần kiểm thủ công 20 và 24 câu giữ nguyên; không chuyển nhãn từ pilot sang 54 câu mới. Chưa phát hành b02 để huấn luyện.

### Tập chính D.2 — lô ứng viên b03

Mở [400 câu tích lũy](../../data/review/d2/d2-official-main-b03/qa-400.csv) hoặc [chỉ 265 câu mới](../../data/review/d2/d2-official-main-b03/qa-moi.csv). CSV dùng UTF-8, gồm họ thủ tục, split, câu hỏi, đáp án kèm vị trí dẫn và URL chính văn. Các tệp trong `data/review/` là bản làm việc nội bộ, không có trên bản clone sạch.

B03 giữ 135 QA cũ và thêm 265 câu train: **394 train, 6 validation**. Câu mới dùng phụ lục 163/QĐ-BTP, phụ lục 858/QĐ-BTP và 753/VBHN-BTP; gồm khai sinh, khai tử, kết hôn, tình trạng hôn nhân, nhận cha mẹ con, giám hộ, giám sát giám hộ, chứng thực di chúc, từ chối nhận di sản và giao dịch. Quy định chung trong nước không xác nhận việc triển khai tại từng xã Hà Nội. Với phụ lục 163 có lớp chữ trích xuất lỗi, mở đúng trang PDF để đọc, không lấy đoạn chữ lỗi làm câu trả lời.

Để tái tạo gói ứng viên trên CPU từ các snapshot đúng hash, chạy vào **thư mục mới**:

```sh
python scripts/prepare_d2_qa.py prepare --stage main --ledger docs/data/source-ledger-b03.json --recipes scripts/d2_main_b03_recipes.json --output data/review/d2/d2-official-main-b03
python scripts/prepare_d2_qa.py check --ledger docs/data/source-ledger-b03.json --recipes scripts/d2_main_b03_recipes.json --candidate data/review/d2/d2-official-main-b03
```

`prepare` tạo JSONL, nguồn, manifest và mẫu phân tầng; hai CSV xem nhanh ở trên là bản xuất từ JSONL. [Sổ nguồn b03](source-ledger-b03.json) kế thừa bằng chứng của D.1, không đổi sổ đã ghim của release-01. B03 là **ứng viên**, chưa có biên bản phát hành và không nằm trong quyền đưa release-01 lên Kaggle. Hai lô đã kiểm thủ công giữ nguyên, không tự chuyển quyết định vào bản này.

### 1. Tạo và xem QA ứng viên trên CPU

Python 3.11+ và `pypdf==6.21.4`; không cần PyTorch/Colab/Kaggle. Nếu thiếu bộ đọc PDF, cài `python -m pip install pypdf==6.21.4` trong môi trường dữ liệu riêng. Lấy từng bản chính văn trong recipe theo `url` và lưu đúng `snapshot_path` trong `d1_review.evidence` của [sổ nguồn](source-ledger.json); với `BTP-2163`, lấy archive được dẫn, giải nén đúng `member` của `appendix` và giữ tên trong `appendix.snapshot_path`. Công cụ không tải mạng, không dùng HTML/video pilot để thay thế khi thiếu PDF/DOCX; dừng nếu SHA-256 không khớp.

```sh
python scripts/prepare_d2_qa.py prepare --output data/review/d2/d2-official-seed-v2
python scripts/prepare_d2_qa.py review-sheet --candidate data/review/d2/d2-official-seed-v2
```

Trên máy đã có gói v2, mở thẳng [phiếu rút gọn `manual-review-short.csv`](../../data/review/d2/d2-official-seed-v2/manual-review-short.csv). Chỉ chạy `prepare` nếu chưa có gói, và chỉ chạy `review-sheet` nếu chưa có phiếu rút gọn; hai lệnh không ghi đè hiện vật cũ. Gói **ứng viên** giữ tại `data/review/d2/` đã ignore. `qa.jsonl` lưu câu/đáp với citation theo từng mệnh đề; `source-spans.json` ghi URL, locator, đoạn đối chiếu và SHA-256. Trích đoạn phải khớp đúng một lần trên trang PDF hoặc trong một đoạn DOCX của bản đã hash. Cả hai phiếu mang đủ câu, đáp án, nguồn và mẫu đã chọn. `near-duplicates.json` liệt kê cặp câu qua Jaccard trigram ≥0,85 để rà, không thay kiểm trùng nghĩa.

**Mở rộng thành tập chính:** dùng `prepare --stage main --recipes đường_dẫn_json --output thư_mục_phiên_bản_mới`. Tham chiếu [recipe thực](../../scripts/d2_seed_recipes.json): phân bổ `family_splits` trước khi tạo câu, chừa `holdout` và không soạn QA cho nó; `key` ổn định và `record_version` mới khi đổi nội dung/nguồn; mỗi claim có một đoạn chính văn đã kiểm và nằm trong danh sách bằng chứng được phép cho họ thủ tục trong sổ D.1. Mỗi QA phải đại diện một nhu cầu thông tin riêng, không nhân bản câu diễn đạt lại để đủ số. Mở rộng danh mục nguồn hợp lệ trong phạm vi Hà Nội–hộ tịch/chứng thực trước khi đặt chỉ tiêu số lượng khả thi. Chỉ dùng mức giá hoặc thời hạn cho đúng kênh, văn bản và mốc hiệu lực đã kiểm.

### 2. Kiểm thủ công và phát hành bản SFT nội bộ

1. **Pilot – dùng phiếu rút gọn:** giữ nguyên A–D (`qa_review_id`, câu hỏi, đáp án, nguồn). Chỉ điền E–H:
   - `decision`: chọn `approved` chỉ sau khi mở và đối chiếu **tất cả** đoạn nguồn, thấy câu rõ nghĩa, đáp án đúng và đủ, dẫn nguồn đúng văn bản/vị trí, đúng phạm vi/điều kiện/kênh, không có thông tin bịa, dữ liệu cá nhân hoặc dấu hiệu trùng/rò đã phát hiện. Quyết định này là xác nhận gộp của người kiểm cho các tiêu chí trên, không phải nhãn do công cụ điền. Chọn `rework` nếu câu nhập nhằng, cần sửa hoặc chưa đủ căn cứ; chọn `rejected` nếu cần loại.
   - `review_note`: được để trống nếu `approved`; nếu `rework`/`rejected`, ghi lý do ngắn và nêu nguồn hoặc nhóm câu liên quan nếu nghi lỗi theo lô.
   - `reviewer_id`, `reviewed_at`: nhập mã người kiểm và giờ kiểm thật dạng ISO-8601 có múi giờ (`+07:00` nếu kiểm tại Việt Nam). Có thể điền cùng một mã và thời điểm nếu các dòng thực sự được kiểm trong cùng phiên và thời điểm ghi nhận đó là của phiên. Giữ định dạng CSV UTF-8, không đổi tên cột.

   Sau khi điền, chạy:

   ```sh
   python scripts/prepare_d2_qa.py check --candidate data/review/d2/d2-official-seed-v2 --review data/review/d2/d2-official-seed-v2/manual-review-short.csv
   ```

   `check` nhận phiếu rút gọn trực tiếp; không cần nhập lại vào phiếu 27 cột. Mã thoát `2` là còn chặn, `1` là lỗi đầu vào. Lệnh không phát hành dữ liệu khi thiếu biên bản hoặc không có `--output`.

   **Phiếu đầy đủ `manual-review.csv`** vẫn dùng được cho pilot và là phiếu áp dụng cho tập chính. Giữ nguyên cột đã điền; đối chiếu điều kiện/kênh/phiên bản, rồi ghi mã người kiểm, thời điểm, mã span đã kiểm (phân cách `;`), bốn tiêu chí, ba cờ lỗi, quyết định và lý do. `follow_up_batch_key` chỉ điền khi nghi lỗi theo lô. Xem [quy tắc kiểm QA](annotation-guide.md#32-phiếu-kiểm-qa--trường-bắt-buộc).
2. `sample.json` khóa mẫu trước khi chấm: pilot chọn toàn bộ; tập chính chọn ngẫu nhiên có seed `ceil(20% × số QA)` trong **từng tầng của từng split** theo phạm vi, nguồn/phiên bản và nguồn gốc câu. Tổng từng split vì thế đạt ít nhất `ceil(20% × tổng split)`. Nếu cần sửa câu, trích dẫn, split hoặc cả batch, giữ phiếu cũ và tạo phiên bản mới.
3. Người phụ trách lập JSON audit trong kho riêng với các trường `dataset_version`, `candidate_manifest_sha256` (lấy từ `check`), `reviewer_id`, `reviewed_at`, `rights_scope`, `source_and_split_verified`, `semantic_duplicate_audit`, `distinct_near_pairs`, `notes`. Chỉ ghi `rights_scope = internal_research_training`, `source_and_split_verified = true` và `semantic_duplicate_audit = no_unresolved` sau khi chính nhóm đã xác minh nguồn/hiệu lực, phạm vi nội bộ và không còn trùng nghĩa/rò rỉ. `distinct_near_pairs` là danh sách `left`, `right`, `reason` với từng cặp cảnh báo đã đối chiếu và thực sự khác nghĩa; nếu trùng cần sửa và tái tạo gói, không đánh dấu giữ. `notes` ghi phạm vi và việc đã kiểm, không chứa dữ liệu người.
4. Thêm `--audit` trỏ biên bản và `--output` trỏ **thư mục mới** vào lệnh `check` mới xuất được `train.jsonl`, `validation.jsonl`, `qa.jsonl`, `overlap-qa.jsonl` tối giản cho người đánh giá và manifest. Nếu `prepare` đã dùng `--recipes`/`--ledger` tùy chỉnh thì truyền đúng hai file đó cho `check`. Không gán `approved` cho QA ngoài mẫu. `pilot_sft_ready` không có nghĩa đủ 2.000, có `USER_TEST` hoặc hoàn tất D.2; `main_sft_ready` chỉ xác nhận cổng QA SFT với bằng chứng do nhóm đã nhập.

**Biên bản cho lô `d2-official-seed-v2` (24 QA đã duyệt).** Trên máy nhóm, sao chép [bản nháp riêng](../../data/review/d2/d2-official-seed-v2/batch-audit.draft.json) thành `batch-audit.json` cùng thư mục. Không đổi `dataset_version` hoặc hash manifest; không cần sửa lại phiếu CSV. Người phụ trách rà ba điểm trước khi ký:

| Điểm cần xác nhận | Bằng chứng cần đối chiếu | Chỉ ghi khi đạt |
|---|---|---|
| Quyền dùng | Đối chiếu 7 hiện vật trong `source-spans.json` với [sổ nguồn D.1](source-audit.md#5-kết-quả-xác-minh-d1-ngày-25112026), nhất là §5.3: chỉ dùng chính văn hành chính và phần phụ lục đã xác minh để soạn QA nghiên cứu nội bộ; không dùng lại snapshot cổng hoặc video của pilot cũ. | `"rights_scope": "internal_research_training"` |
| Hiệu lực, phạm vi và chia tập | Kiểm số hiệu, phiên bản, kênh và địa bàn. Không suy 2163 đã thay 1818 tại Hà Nội; ngày hiệu lực 163 lấy từ Điều 2, không từ bìa phụ lục. Đối chiếu `qa.jsonl` với `manifest.json`: train = trích lục (10), chứng thực chữ ký (6), cải chính hộ tịch (2); validation = xác nhận thông tin hộ tịch (6); chứng thực bản sao để riêng, không có QA. | `"source_and_split_verified": true` |
| Trùng nghĩa và rò giữa hai tập | So sánh ý hỏi, điều kiện và đáp án trong và giữa hai tập. Xem riêng hai câu validation cùng dùng B.4 của 1852: thời hạn thông thường và thời hạn khi phải xác minh. `near-duplicates.json` rỗng chỉ nói bộ lọc từ vựng không cảnh báo; không chứng minh hai câu khác nghĩa. Không mở `USER_TEST` để làm bước này. | `"semantic_duplicate_audit": "no_unresolved"`; giữ `distinct_near_pairs` là `[]` vì lô này không có cặp do bộ lọc báo. |

Ghi `reviewer_id` bằng mã người thực sự rà lô, `reviewed_at` bằng thời điểm người đó kết luận (ISO 8601 có múi giờ, không chép giờ kiểm từng QA). Bổ sung vào `notes` kết luận thực tế, nhất là lý do giữ hoặc xử lý cặp dùng chung B.4. Nếu còn nghi vấn, giữ trạng thái chưa đạt, ghi điểm cần xử lý và **không phát hành**. Nếu phải sửa QA hoặc split, tạo phiên bản mới; không dùng biên bản gắn hash cũ.

**Chỉ sau khi đã ký**, chạy từ gốc repo bằng PowerShell (đường dẫn `$release` phải chưa tồn tại):

```powershell
$lot = 'data/review/d2/d2-official-seed-v2'
$release = 'data/review/d2/d2-official-seed-v2-release-01'
python scripts/prepare_d2_qa.py check --candidate $lot --review "$lot/manual-review-short.csv" --audit "$lot/batch-audit.json" --output $release
if ($LASTEXITCODE -eq 0) { python scripts/train_d3_sft.py --release $release --output .cache/d3-check --check-only }
```

`pilot_sft_ready` cho phép kiểm đầu vào D.3 trên máy nhóm; việc đưa đúng bản phát hành lên Kaggle Private cần [xác nhận riêng](../../README.md#d3--chuẩn-bị-sft-trên-kaggle). Không tải biên bản, phiếu kiểm hay snapshot nguồn lên Kaggle.

### 3. Thu và khóa `USER_TEST` độc lập

**Trước khi mời người thật:** người phụ trách xin chấp thuận hình thức đồng ý bằng văn bản, đối tượng và kênh; hoàn thành G-01–G-06 theo [quy trình riêng tư](privacy-workflow.md#31-gate-trước-thu-thập) và dùng [phiếu khảo sát hiện có](consent-and-survey.md). Không tạo dữ liệu thử thay người thật, không nhập phiếu thô, consent, liên hệ hay nội dung khảo sát vào Git/Chat/API. Người đánh giá có thể phối hợp thu song song nếu các cổng thu thập đã đạt; không tiết lộ câu hỏi cho nhóm soạn QA, tune hoặc chấm DPO. Đưa vào `USER_TEST` các họ chưa dùng ở train/validation (ưu tiên họ khóa `holdout`) và câu ngoài phạm vi khi phù hợp; không dùng câu test để bổ sung corpus.

**Khi đã có dữ liệu thật đã ẩn danh** trong kho L3 và QA SFT đã khóa, người đánh giá sao chép `overlap-qa.jsonl` của đúng phiên bản SFT vào kho riêng và đối chiếu SHA-256 với manifest SFT. Công cụ chỉ đọc L3 đúng schema §4.1 và export tối giản này; kiểm consent/redaction theo trạng thái, họ thủ tục, trùng chuẩn hóa và gần trùng từ vựng. Người đánh giá tự kiểm trùng nghĩa và ghi biên bản, không gửi dữ liệu cho người train. Nếu đổi tập QA SFT, kiểm lại rò rỉ với hash mới.

```sh
python scripts/prepare_d2_survey.py --help
python scripts/prepare_d2_survey.py --survey <L3-ngoai-repo.jsonl> --attestation <bien-ban-ngoai-repo.json> --qa <overlap-qa-ngoai-repo.jsonl> --output <thu-muc-rieng-ngoai-repo> --version <phien-ban-USER_TEST>
```

Các đường dẫn trong dòng thứ hai là tham số cần thay bằng đường dẫn thật; cả bốn nằm ngoài repo trong kho riêng. Biên bản `--attestation` chứa `attestation_version`, `attested_at`, `gates`, `semantic_overlap_clearance`: `gates` có đúng G-01 đến G-06, mỗi cổng đã đạt ghi `status: pass` và `evidence_source: operator_provided`. Phần rà trùng nghĩa ghi `status: cleared`, `evaluator_role_id`, `cleared_at`, `qa_file_sha256`, `survey_records_reviewed: true` **chỉ sau khi đã thực hiện**. Công cụ xuất riêng `user_test.jsonl` và `manifest.private.json`; chỉ số tổng hợp in trong terminal, không hiện câu hỏi/mã người tham gia. Công cụ không chứng thực người tham gia, consent hoặc redaction và không cấp quyền công khai.

## Việc nhóm thực hiện tiếp

- Hà tổng hợp các quyết định/văn bản còn thiếu; nhóm rà soát nguồn, quyền và các QA nháp. Không lấy kết quả AI làm quota kiểm thủ công.
- Thế/Hưng chuẩn bị chấm độc lập sau khi có SFT thật; Hà phân xử sau khi khóa nhãn. Không chia đôi cặp cho hai người.
- Xác nhận hình thức đồng ý theo quy định áp dụng, lịch, kênh liên hệ, kho riêng và thời hạn rút trước khi mời người khảo sát. Chưa phát hành biểu mẫu công khai.
- Không dùng câu hỏi test để bổ sung QA train/validation, prompt DPO hoặc chọn cấu hình. Không đưa consent/dữ liệu người vào Git hoặc API ngoài.

Cập nhật trạng thái chỉ từ sự kiện có thật. Gói này không đánh dấu A–D, 2.000 QA, 500 cặp, khảo sát hoặc huấn luyện là hoàn thành.
