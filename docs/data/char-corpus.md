# Truyện Kiều — corpus ký tự có provenance

> **Trạng thái:** đã chạy audit kỹ thuật trên revision `206607` qua đường `/wiki/` được robots cho phép. Đã tạo corpus, split, vocabulary, cửa sổ và manifest thực tế **chỉ trong `.cache/char-corpus/`**, không phải dữ liệu được phép huấn luyện/phân phối. Chưa có review quyền của nhóm; không tạo `data/samples/char-corpus-manifest.json` giả trạng thái sẵn sàng. [Báo cáo audit](char-corpus-audit-report.json) chứa số đo thực, không chứa thân tác phẩm.

Corpus này chỉ dành cho A.2 (mô hình ngôn ngữ ký tự). Nó không phải nguồn cho SFT/DPO hành chính và PPL trên nó không đại diện cho văn xuôi hành chính.

## 1. Bản nguồn đã đóng băng

| Thuộc tính | Giá trị đã xác minh |
|---|---|
| Tác phẩm / tác giả hiển thị | *Truyện Kiều* / Nguyễn Du |
| Wikisource page ID | `7350` |
| Revision đóng băng | `206607` |
| Parent revision | `205132` |
| Thời điểm revision (UTC) | `2026-11-07T14:26:11Z` |
| Rendered revision endpoint cho audit | <https://vi.wikisource.org/wiki/Truyện_Kiều?oldid=206607> |
| Permalink người đọc | <https://vi.wikisource.org/w/index.php?title=Truyện_Kiều&oldid=206607> |
| Raw revision (chỉ local-input mode, không tự fetch) | <https://vi.wikisource.org/w/index.php?title=Truyện_Kiều&oldid=206607&action=raw> |
| MediaWiki SHA-1 wikitext | `9910643b961054303306d3ace187dcd8dbbd4f3b`, quan sát trong API metadata **trước** khi kiểm robots; không phải SHA-1 bytes local đã tải trong repo. |
| Truy vấn metadata primary | <https://vi.wikisource.org/w/api.php?action=query&prop=revisions&titles=Truyện_Kiều&rvstartid=206607&rvendid=206607&rvprop=ids%7Ctimestamp%7Csha1&format=json&formatversion=2> |
| Tình trạng current lúc quan sát | API trả `206607` là revision mới nhất trước khi robots được kiểm. Không lặp API vì `/w/` bị robots chặn; rendered URL `oldid` tự báo `wgRevisionId=206607` và `wgArticleId=7350`. |

Revision là identity dùng để tái lập, **không** phải bằng chứng bản Kiều này là bản phê bình chuẩn hay là một bản số hóa đã được cấp quyền riêng. Wikitext revision hiển thị tác giả Nguyễn Du và phần giới thiệu; người review quyền phải ghi rõ bản in/bản chuyển tự hoặc provenance của bản số hóa mà họ dựa vào, thay vì chỉ suy diễn từ tên tác phẩm.

## 2. Kiểm tra truy cập tự động và quyền

### 2.1 Robots: chỉ audit một URL `/wiki/` đã pin

Đã đọc nguồn primary [`https://vi.wikisource.org/robots.txt`](https://vi.wikisource.org/robots.txt) ngày 2026-11-16 UTC. Với `User-agent: *`, rules `Disallow: /w/` và `Disallow: /api/` chặn raw revision và Action API; chúng **không** chặn route `/wiki/Truyện_Kiều?oldid=206607` (các rule `/wiki/` trong robots là cho một số `Special:` cụ thể). Vì thế script không có fetch raw/API/crawl: `--audit-rendered` chỉ (1) tải `robots.txt` với User-Agent định danh, (2) xác nhận URL `/wiki/` đúng này được phép, (3) tải đúng một rendered revision, rồi từ chối redirect, MIME khác HTML, page ID hoặc revision ID sai. Nó lưu mọi output dưới `.cache/char-corpus/` và gắn trạng thái research-only. Robots vẫn **không phải giấy phép**.

Tài liệu [MediaWiki API etiquette](https://www.mediawiki.org/wiki/API:Etiquette) (primary documentation, đọc ngày 2026-11-16 UTC) yêu cầu User-Agent có thông tin liên hệ, request tuần tự, caching và `maxlag` cho tác vụ không tương tác. Audit không gọi API; phần này chỉ ghi lại vì API metadata ban đầu đã được quan sát trước khi robots được kiểm.

### 2.2 Gate quyền: chưa đạt

Các nguồn primary đã đối chiếu ngày 2026-11-16 UTC:

1. [Quy định bản quyền của Wikisource tiếng Việt](https://vi.wikisource.org/wiki/Wikisource:Quy_định_về_bản_quyền) nói các tác phẩm Wikisource phải thuộc phạm vi công cộng hoặc có giấy phép tương thích; nếu không ghi khác, đóng góp thành viên được phát hành CC BY-SA 4.0/GFDL.
2. [Điều khoản sử dụng của Wikimedia Foundation](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use/vi) nói người tái sử dụng chịu trách nhiệm theo luật áp dụng và phải tuân thủ điều khoản/quy định dự án.
3. [CC BY-SA 4.0 deed](https://creativecommons.org/licenses/by-sa/4.0/deed.vi) yêu cầu ghi công, liên kết giấy phép và báo thay đổi; tác phẩm phái sinh phải theo cùng giấy phép. Deed cũng nói không có bảo đảm và các quyền khác có thể vẫn hạn chế việc dùng.
4. [Hướng dẫn phạm vi công cộng của Wikisource tiếng Việt](https://vi.wikisource.org/wiki/Trợ_giúp:Phạm_vi_công_cộng) tự mô tả là tóm lược, không phải chỉ dẫn pháp luật đầy đủ, và tách điều kiện Việt Nam/Hoa Kỳ theo thời điểm công bố/tác giả.

Những nguồn này là provenance/terms của nền tảng, **không cho phép nhóm khẳng định “public domain trên toàn thế giới”** hoặc tự khẳng định quyền của một bản chuyển tự/số hóa cụ thể. Trước khi ingest, người phụ trách phải review độc lập cả: (a) tình trạng của tác phẩm gốc theo phạm vi sử dụng, (b) quyền/giấy phép của bản số hóa hoặc chuyển tự đúng revision, và (c) nghĩa vụ attribution/share-alike nếu phần đóng góp Wikisource được dùng. Không có attestation đó thì dừng — không tạo corpus “ready”, không train và không commit raw text.

## 3. Ranh giới trích xuất đã quy định

Audit dùng đúng `div.poem` trong rendered HTML của revision pin, bỏ `span.OptionText` chứa số dòng, HTML/page chrome, menu, tiêu đề, ảnh, giới thiệu, category và ghi chú ngoài poem. Local raw mode dùng đúng một `<poem>` và bỏ balanced MediaWiki template (ví dụ `{{số|5}}`), HTML comment, dòng trống/indent và toàn bộ nội dung ngoài `<poem>`. Cả hai mode fail-closed nếu marker không khớp.

Các marker dưới đây được dùng làm control; lần audit thực tế đã xác nhận dòng đầu/cuối và 3.254 dòng. Hash wikitext từ API vẫn chỉ là metadata đã quan sát, không phải hash raw bytes được script tải.

| Marker | Giá trị expected / provenance |
|---|---|
| SHA-1 raw wikitext | `9910643b961054303306d3ace187dcd8dbbd4f3b`, quan sát qua API trước robots; local raw mode kiểm lại bytes nếu được cấp source. |
| Dòng đầu | `Trăm năm trong cõi người ta,` |
| Dòng cuối | `Mua vui cũng được một vài trống canh.` |
| Số dòng thơ | Expected và actual audit đều `3254`; chi tiết số đo trong báo cáo audit. |
| Chuẩn hóa | Unicode NFC; line ending LF; whitespace trong từng dòng gộp một khoảng trắng; một LF cuối mỗi dòng |

SHA-256, số ký tự, split, vocabulary và windows chỉ là **actual artifacts** trong manifest do một lần run tạo ở `.cache`; không ghi trước con số nào.

## 4. Chuẩn bị cục bộ và gate quyền

### Điều kiện môi trường

- Python chuẩn 3.10+; chỉ dùng standard library, không cài `torch` hay package mới.
- Để kiểm kỹ thuật ngay, không cần raw file hay quyền đã phê duyệt: script tự kiểm robots rồi chỉ tải rendered endpoint đã pin, và bắt buộc output nằm trong `.cache/char-corpus/`.

Lệnh smoke/audit research-only mà parent có thể chạy:

```powershell
python scripts/prepare_char_corpus.py `
  --audit-rendered `
  --output-dir .cache/char-corpus/audit-206607 `
  --manifest .cache/char-corpus/audit-206607-manifest.json `
  --train-fraction 0.9 `
  --sequence-length 128
```

Manifest từ lệnh này có `status: research_only_not_approved_for_training_or_distribution`, raw rendered HTML và tất cả text/window chỉ ở `.cache`. Nó kiểm exact boundaries, NFC, contiguous split, train-only vocabulary, UNK policy, artifact hashes/counts — nhưng **không** là consent/quyền dùng để train hay phát hành.

### Local preparation sau gate quyền

Chỉ khi reviewer quyền có căn cứ thật, raw wikitext có thể được lưu private như `.cache/char-corpus/truyen-kieu-oldid-206607.wikitext` (UTF-8 byte-for-byte, không BOM/đổi line ending) và dùng `--source-wikitext`. Khi đó thêm `--rights-attestation` JSON có các trường thật: `status: "approved"`, `source_title`, `source_revision: 206607`, `source_wikitext_sha1`, `reviewer_id`, `reviewed_at_utc`, `retrieved_at_utc`, `digitization_provenance`, `basis_urls`. Không commit mẫu attestation giả.

```powershell
python scripts/prepare_char_corpus.py `
  --source-wikitext .cache/char-corpus/truyen-kieu-oldid-206607.wikitext `
  --rights-attestation .cache/char-corpus/rights-attestation.json `
  --output-dir .cache/char-corpus/prepared-206607 `
  --manifest .cache/char-corpus/char-corpus-manifest-206607.json `
  --train-fraction 0.9 `
  --sequence-length 128
```

Chỉ sau review quyền và review manifest về việc chia sẻ metadata mới có thể đặt **bản sao manifest actual đã review** ở `data/samples/char-corpus-manifest.json`. Raw HTML/wikitext, corpus/split/window luôn ở `.cache/` hoặc kho dữ liệu được kiểm quyền, không đưa Git theo tài liệu này.

## 5. Output, split và chống leakage

Với input đạt audit hoặc gate quyền, `--output-dir` mới sẽ chứa:

| File | Nội dung |
|---|---|
| `source-rendered-206607.html` | Chỉ audit mode: snapshot rendered source để đối chiếu hash, trong `.cache` bắt buộc. |
| `corpus.txt` | Toàn bộ dòng thơ đã extract/NFC, không page chrome hay line numbers. |
| `train.txt`, `validation.txt` | Prefix/suffix **liền kề theo Unicode code point** của `corpus.txt`; ghép lại đúng bằng corpus và không overlap. |
| `vocab.json` | Character vocabulary học **chỉ từ train**; `<UNK>` có ID 0. Ký tự validation chưa gặp train mã hóa 0, không làm giàu vocabulary. |
| `train_windows.jsonl`, `validation_windows.jsonl` | Các cặp `input_ids`/`target_ids` next-character, stride = sequence length. Mỗi cửa sổ đủ `L+1` code point và nằm hoàn toàn trong đúng split. |

Pipeline split trước windowing, nên target của cửa sổ train không bao giờ đọc code point validation (và ngược lại). Tail không đủ một cửa sổ bị loại, được đếm trong manifest; window không vượt boundary. Manifest ghi count/codepoint/hash thực của tất cả artifacts, revision URL, rules normalization, UNK policy, boundary và số window.

## 6. Các điều kiện fail-closed

Audit dừng nếu robots không cho phép đúng URL, redirect/MIME/revision/page ID không khớp, không thấy `div.poem`, hoặc marker đầu/cuối/3.254 dòng sai. Local raw mode còn dừng nếu source bytes không đúng SHA-1, không phải UTF-8/BOM, không đúng một `<poem>`, template/link/HTML còn trong poem, hay attestation quyền thiếu/sai. Cả hai mode từ chối output/manifest đã tồn tại; audit bắt buộc `.cache/char-corpus/`, không tự thăng trạng thái training/release và không ghi đè artifact cũ.

## 7. Bằng chứng chạy và giới hạn

Đã thực thi chế độ `--audit-rendered` bằng Python 3.12 trên máy hiện tại, với output cuối ở `.cache/char-corpus/audit-206607-final/` và manifest `.cache/char-corpus/audit-206607-final-manifest.json`. Không cài lại PyTorch hoặc huấn luyện mô hình.

- Corpus NFC có **104.204 Unicode code point**, 3.254 dòng; train/validation lần lượt 93.783/10.421 code point, ghép lại đúng corpus.
- Từ vựng học từ train có 133 token gồm `<UNK>`; bản validation này có 0 code point ngoài từ vựng. Đây là kết quả quan sát, không giả định các corpus khác cũng như vậy.
- Với độ dài 128, đã tạo và kiểm từng cửa sổ: 732 train, 81 validation; input/target khớp đúng đoạn trong split của chính nó, không vượt ranh giới.
- Hash của mọi hiện vật khớp manifest. Đổi marker dòng đầu trên bản sao HTML bị từ chối đúng kỳ vọng.
- Phát hiện lúc kiểm thử: urllib mặc định từng theo redirect rồi mới kiểm URL cuối. Đã sửa để từ chối **trước** khi truy cập đích redirect chưa được robots kiểm; kiểm thử HTTP loopback quan sát đích bị chặn không nhận request. Kiểm thử hồi quy được giữ trong `tests/test_char_corpus.py`.
- Chưa kiểm nhánh raw-wikitext với attestation quyền thật, chưa có phê duyệt huấn luyện/phân phối; số đo audit kỹ thuật không thay thế việc đó.
