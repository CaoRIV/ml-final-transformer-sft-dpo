# Truyện Kiều — corpus ký tự có provenance

> **Nguồn A.2 đã chốt:** *Kim, Vân, Kiều truyện* — Nguyễn Du, bản Quốc ngữ Trương Vĩnh Ký, F.-H. Schneider, ấn bản thứ ba, 1911. Dữ liệu lấy từ phần thơ ở Wikisource revision `206466`, đối chiếu mẫu với scan. Revision `206607` là audit lịch sử, không dùng để huấn luyện hoặc tải Colab. Xem [chuẩn bị và xác nhận quyền](#4-chuẩn-bị-cục-bộ-và-xác-nhận-quyền).

Corpus này chỉ dành cho A.2 (mô hình ngôn ngữ ký tự). Nó không phải nguồn cho SFT/DPO hành chính và PPL trên nó không đại diện cho văn xuôi hành chính.

## 1. Nguồn audit lịch sử — revision 206607

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

Trong đợt [audit lịch sử](char-corpus-audit-report.json) ngày 2026-11-16 UTC, [`robots.txt`](https://vi.wikisource.org/robots.txt) chặn raw revision và Action API dưới `/w/`, không chặn URL `/wiki/Truyện_Kiều?oldid=206607`. Lần audit đã tải đúng một rendered revision, kiểm redirect/MIME/page ID/revision và lưu kết quả research-only ngoài Git. Quy trình audit cũ không còn là lệnh chuẩn bị A.2. Robots quy định truy cập tự động, không phải giấy phép sử dụng.

Tài liệu [MediaWiki API etiquette](https://www.mediawiki.org/wiki/API:Etiquette) (primary documentation, đọc ngày 2026-11-16 UTC) yêu cầu User-Agent có thông tin liên hệ, request tuần tự, caching và `maxlag` cho tác vụ không tương tác. Audit không gọi API; phần này chỉ ghi lại vì API metadata ban đầu đã được quan sát trước khi robots được kiểm.

### 2.2 Rà soát quyền revision 206607 — chưa đủ căn cứ

Rà soát `2026-11-25` (UTC), giới hạn ở **phần thơ chữ Quốc ngữ** của revision `206607`; không xét hình minh họa, lời giới thiệu hoặc chú thích ngoài khối thơ. Đề bài bản `12/11/2026`, tr. 18, A.2 yêu cầu chính văn bản huấn luyện phải thuộc phạm vi công cộng hoặc có giấy phép mở; Truyện Kiều là ví dụ, không bắt buộc một revision.

| Hạng mục | Bằng chứng và kết luận |
|---|---|
| Tác phẩm văn học gốc | [Bảo tàng Lịch sử Quốc gia](https://baotanglichsu.vn/VI/Articles/3098/18842/than-the-va-su-nghiep-cua-djai-thi-hao-nguyen-du-1765-1820.html) ghi Nguyễn Du mất năm 1820. [Luật Sở hữu trí tuệ hợp nhất 160/2026/VBHN-LQ-VPQH](https://congbaocdn.chinhphu.vn/180507251028987904/2026/10/6/470657-1791273236_v1_1791273883_signed.pdf#page=24), Điều 27 khoản 2(b), (c) và Điều 43, cho căn cứ kết luận **tác phẩm gốc thuộc về công chúng tại Việt Nam**. Vẫn tôn trọng tên tác phẩm, ghi tên tác giả và bảo vệ sự toàn vẹn theo Điều 19, Điều 27 khoản 1. Không tuyên bố trạng thái ở mọi nước. |
| Phần thơ của đúng revision | [Revision 206607](https://vi.wikisource.org/wiki/Truyện_Kiều?oldid=206607) có nhãn phạm vi công cộng cuối trang nhưng không ghi ấn bản làm nền cho thân thơ Quốc ngữ; chú thích ảnh Chiêm Vân Thị chỉ định danh ảnh. [Thảo luận “Bản này là bản nào?”](https://vi.wikisource.org/wiki/Thảo_luận:Truyện_Kiều#Bản_này_là_bản_nào?) dẫn nguồn của một **bản cũ** tới Hội Bảo tồn Di sản Chữ Nôm và ghi nhận câu chữ đã được sửa. Đối chiếu trực tiếp: câu 8 ở [revision 15878](https://vi.wikisource.org/wiki/Truyện_Kiều?oldid=15878) dùng “có lục”, còn `206607` dùng “cổ lục”. Đây là bằng chứng có sửa, không phải bằng chứng xác định nguồn của toàn bộ câu chữ. |
| Nguồn số hóa được dẫn | [Danh mục của Hội Bảo tồn Di sản Chữ Nôm](https://nomfoundation.org/nom-project/Tale-of-Kieu) xác nhận 1866 là niên đại **bản khắc Nôm**, còn phần Quốc ngữ là công trình phiên âm, khảo dị của **Nguyễn Quảng Tuân, xuất bản năm 2004**. Ấn bản này dùng bản 1871 bổ khuyết 36 trang thiếu. [Điều khoản của Hội](https://nomfoundation.org/About-the-Foundation/Terms-of-use?uiLang=en) có phép sử dụng phi thương mại trong phạm vi nhất định kèm ghi nguồn, nhưng không xác lập giấy phép mở hay quyền huấn luyện và xử lý đám mây cho chính văn bản cần dùng. Không kết luận mọi phiên âm đều có bản quyền, hay toàn bộ `206607` là bản 2004. |
| Phần đóng góp Wikisource | [Điều khoản Wikimedia §7.1, §7.3, §7.6–8](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content) phân biệt nội dung do người có quyền cấp phép với nội dung nhập từ ngoài. [CC BY-SA 4.0 §1–3](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en) chỉ cấp quyền mà bên cấp phép có thẩm quyền cấp. Nhãn trang và giấy phép mặc định của đóng góp không giải quyết quyền lớp Quốc ngữ nhập từ bên ngoài. Nếu sau này dùng một bản có phần đóng góp được cấp phép CC BY-SA, giữ ghi công và liên kết nguồn/giấy phép, ghi các thay đổi; áp dụng ShareAlike khi chia sẻ bản phái sinh thuộc phạm vi giấy phép. Không tự suy ra giấy phép của trọng số mô hình. |
| Ngoại lệ nghiên cứu và Colab | Khoản 5 Điều 7 của [Luật SHTT hợp nhất](https://congbaocdn.chinhphu.vn/180507251028987904/2026/10/6/470657-1791273236_v1_1791273883_signed.pdf#page=9) và Điều 37a–37c được bổ sung bởi [Nghị định 134/2026/NĐ-CP](https://congbaocdn.chinhphu.vn/180507251028987904/2026/4/29/469388-1777368984_v1_1777430941_signed.pdf#page=10) quy định đường sử dụng dữ liệu được bảo hộ cho huấn luyện phi thương mại có điều kiện, gồm công bố/tiếp cận hợp pháp và không ảnh hưởng bất hợp lý đến khai thác tác phẩm. Chưa xác lập đủ điều kiện cho revision này; ngoại lệ cũng **không** biến dữ liệu thành phạm vi công cộng hay giấy phép mở theo đề. [Điều khoản Colab](https://research.google.com/colaboratory/tos_v6.html#connected-services-and-content) và [Google, bản Việt Nam](https://policies.google.com/terms?hl=vi#toc-permission) yêu cầu người dùng có quyền cần thiết; notebook hoặc thư mục riêng tư không thay căn cứ đó. |

**Quyết định vận hành:** tiếp tục giữ `206607` ở trạng thái audit. Không tạo attestation, không bật `training_allowed`, không huấn luyện cục bộ/Colab, không đăng corpus. Đây là kết luận về **độ đầy đủ của bằng chứng**, không phải kết luận Wikisource đăng trái phép. Nếu giữ revision này, cần tài liệu truy nguyên phần thơ sau các sửa đổi và căn cứ phạm vi công cộng/giấy phép mở áp dụng cho chính phần đó; xác nhận phạm vi xử lý qua Colab và ghi công trước khi dùng.

### 2.3 Căn cứ chọn bản Quốc ngữ Trương Vĩnh Ký 1911

- [Trang nhan đề scan](https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c0/Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf/page1-330px-Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf.jpg) ghi Trương Vĩnh Ký, ấn bản thứ ba, F.-H. Schneider, Sài Gòn, 1911. [Hồ sơ scan Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf#Licensing) ghi người phiên âm mất năm 1898, bản in 1911 và gắn nhãn bản quét cơ học `PD-scan`. Căn cứ rõ hơn cho **phần thơ Quốc ngữ của ấn bản này**: Điều 27/43 tại Việt Nam; với Hoa Kỳ, hồ sơ Commons phù hợp với thời hạn tối đa 95 năm của tác phẩm xuất bản thời kỳ đó ([U.S. Copyright Office, Circular 15A](https://www.copyright.gov/circs/circ15a.pdf), mục tác phẩm trước 1978 và tác phẩm nước ngoài).
- Nguồn phiên chép là [phần thơ Wikisource, revision 206466](<https://vi.wikisource.org/wiki/Truyện_Kiều_(bản_Trương_Vĩnh_Ký_1911)/Kim,_Vân,_Kiều_truyện?oldid=206466>) và [mục lục gắn với bản quét](https://vi.wikisource.org/wiki/Mục_lục:Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf). Trạng thái “Cần phê chuẩn” của mục lục nói về chất lượng phiên chép, không thay kết luận về quyền. Ghi công Nguyễn Du, Trương Vĩnh Ký, nguồn Wikisource và lịch sử cộng tác; không gộp quyền của phần thơ cổ với mọi nội dung hiện đại trên trang.

## 3. Bản đóng băng và phạm vi dữ liệu 1911

- Scan tải từ Commons có 7.264.816 byte. SHA-1 `0932d2a6189454300c1e79a69cd27d8fc43633f6` khớp hồ sơ Commons; SHA-256 `d60d1b9620300aa0e31dfdf12a3499e3eb72f2236191dd5a9f70cc696711e5d8` khóa trong script.
- Snapshot HTML UTF-8 của đúng trang `25612`, revision `206466`: SHA-256 `fc877689bfa3df5c6bd5674adee9326ff6fd3c3db53cefb9ff5e0dea08758976`. Trang nhúng nhiều trang con; giữ **byte snapshot và hash corpus**, không coi riêng `oldid` là khóa toàn bộ chữ hiển thị. Khi chuẩn bị lại, script dừng nếu hash của phần thơ đã trích thay đổi.
- Đối chiếu mẫu hình trang [14](https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c0/Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf/page14-330px-Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf.jpg), [101](https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c0/Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf/page101-330px-Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf.jpg), [200](https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c0/Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf/page200-330px-Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf.jpg) của PDF: câu mở, đoạn giữa, câu kết phân biệt được với đề mục/số chú thích. [Trang 100](https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c0/Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf/page100-330px-Kim_Van_Kieu_truyen_Truong_Vinh_Ky.pdf.jpg) là tranh có chú thích bên dưới. Đây là đối chiếu chọn mẫu, không phải kiểm thủ công từng dòng hay tuyên bố bản phiên chép không lỗi.
- Trích các khối thơ, không lấy đề mục, hình/chú thích ảnh và tham chiếu chú thích. Loại đúng ba cách đọc thay thế trong ngoặc: `hay là iêm-liềm`, `oanh`, `đờn`; giữ dạng chữ đứng ngoài ngoặc. Không hiện đại hóa chính tả; chuẩn hóa NFC, gộp khoảng trắng nội dòng và dùng LF. Corpus khóa SHA-256 `eddbb40a3f4ad421d8b089f95ad139a372b20c4ec8621a929ba6aa6f9c63abcb`.

## 4. Chuẩn bị cục bộ và xác nhận quyền

Chạy từ gốc repo với Python 3.10+, không cần PyTorch/GPU ở bước chuẩn bị:

```powershell
python -m scripts.prepare_char_corpus `
  --source-html .cache/char-corpus/source-1911-206466.html `
  --scan-pdf .cache/char-corpus/source-1911.pdf `
  --output-dir .cache/char-corpus/prepared-1911 `
  --manifest .cache/char-corpus/manifest-1911.json
```

Khi nguồn chưa có, thêm `--fetch` để lấy đúng URL HTML và PDF sau khi kiểm `robots.txt`; không gọi API/raw và không theo redirect. Không ghi đè file nguồn hay hiện vật đã có. Khi cần tái tạo, dùng đường dẫn output và manifest mới; xác nhận cũ chỉ khớp **đúng byte của manifest đã duyệt**.

Thư mục `prepared-1911/` chứa `corpus.txt`, `train.txt`, `validation.txt`, `vocab.json`, `train_windows.jsonl`, `validation_windows.jsonl`. Cắt prefix train 90% và suffix validation 10% theo code point **trước khi** học từ vựng và tạo cửa sổ. Context mặc định 128, stride 128; phần đuôi không đủ cửa sổ bị loại. Vocab chỉ từ train; ký tự validation chưa gặp mang ID `<UNK>` 0. Manifest ghi hash, kích thước và thông số của từng hiện vật.

**Trước khi chạy A.2 trên Colab:** người duyệt thật của nhóm đối chiếu nguồn, phạm vi chỉ phần thơ, ghi công và quyền đưa dữ liệu sang Colab. Chỉ khi đồng ý, lưu JSON riêng ở `.cache/char-corpus/rights-1911.json` (UTF-8, không BOM):

| Trường | Giá trị khi người duyệt chấp thuận |
|---|---|
| `status` | Chuỗi `approved` |
| `evaluated_for` | Chuỗi `a2-local-and-colab` (huấn luyện nội bộ và xử lý trên Colab, không phải phê duyệt phát hành) |
| `training_allowed` | Boolean `true`, không phải chuỗi |
| `manifest_sha256` | SHA-256 chữ thường của đúng `manifest-1911.json` |
| `reviewer_id` | Mã nội bộ của thành viên thực sự duyệt |
| `reviewed_at_utc` | Thời điểm duyệt thực, ISO 8601 UTC, hậu tố `Z` hoặc `+00:00` |

Lấy hash trên PowerShell: `(Get-FileHash .cache/char-corpus/manifest-1911.json -Algorithm SHA256).Hash.ToLowerInvariant()`. **Không sửa manifest để tự phê duyệt.** Khi có xác nhận, chuyển `prepared-1911/`, manifest và tệp xác nhận vào kho riêng được nhóm phép dùng; không cần đưa scan/HTML lên Colab chỉ để train. Làm theo ô cuối [notebook A.2](../../notebooks/04_char_lm.ipynb). Giữ nguồn, corpus, cửa sổ, hồ sơ duyệt và checkpoint ngoài Git.

## 5. Kết quả chuẩn bị đã kiểm

| Đại lượng | Giá trị |
|---|---:|
| Dòng thơ | 3.254 |
| Code point NFC cả corpus | 104.181 |
| Code point train / validation | 93.762 / 10.419 |
| Cửa sổ train / validation, context 128 | 732 / 81 |
| Code point đuôi không dùng train / validation | 65 / 50 |
| Từ vựng học từ train (gồm UNK) | 127 |
| Target được chấm ở validation / số target UNK | 10.368 / 1 |

Đã kiểm SHA-256 của 6 hiện vật, ghép lại đúng văn bản sau NFC, tái dựng ID và cửa sổ độc lập trên từng split. SHA-256 của manifest thực tại `.cache/char-corpus/manifest-1911.json`: `b8024b1edee0528c5d50dae4bc9f1b353564e6d42aaa40a6c14ce2d30a381990`. CLI từ chối khi thiếu xác nhận, không tạo thư mục huấn luyện. Không có PPL chính thức.
