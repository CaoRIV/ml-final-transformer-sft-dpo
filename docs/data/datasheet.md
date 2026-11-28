# Datasheet — bộ dữ liệu hỏi đáp thủ tục hộ tịch và chứng thực tại Hà Nội

**Hiện vật bắt buộc theo đề** (phần II tr. 2: "dữ liệu hoặc script thu thập + datasheet").
Cấu trúc theo *Datasheets for Datasets* (Gebru và cộng sự).

> **Trạng thái: CHƯA PHÁT HÀNH.** Bộ dữ liệu chính thức chưa tồn tại. Datasheet này
> mô tả (a) những gì đã có thật trong kho mã, và (b) đặc tả của bộ dữ liệu dự kiến,
> với nhãn rõ ràng cho từng phần. Mọi con số dưới đây là số đếm được từ hiện vật
> thật, không phải mục tiêu đã đạt.
>
> Lô pilot **v2** đã duyệt 24/24 và phát hành nội bộ (`pilot_sft_ready`). Lô pilot
> **v1** giữ ở `release_status: "not_ready"`, `human_approved_qa_count: 0` — số
> trong `admin-pilot-report.json` là kiểm cấu trúc, không phải kiểm người.

Tài liệu liên quan: [rà soát nguồn D.1](source-audit.md) ·
[triển khai D.2](README.md#triển-khai-d2) · [hướng dẫn chấm](annotation-guide.md) ·
[quy trình riêng tư](privacy-workflow.md) · [đồng ý và khảo sát](consent-and-survey.md) ·
[ma trận yêu cầu](../progress/requirements-matrix.md)

---

## 1. Động cơ

**Bộ dữ liệu được tạo để làm gì?**
Tinh chỉnh một mô hình ngôn ngữ 0,5–3B thành trợ lý hỏi đáp về thủ tục hộ tịch và
chứng thực tại Hà Nội, cho Đề tài 9 của bài tập lớn môn Học máy cơ bản. Yêu cầu đầu
ra: nêu đúng thông tin và điều kiện áp dụng, **dẫn nguồn** để người dùng kiểm tra,
và **nói rõ khi ngoài phạm vi hoặc chưa đủ căn cứ** thay vì đoán.

**Ai tạo?**
Nhóm ba sinh viên: Cao Văn Hà (trưởng nhóm), Hà Mạnh Thế, Trần Duy Hưng. Không có
đơn vị tài trợ.

**Ai cấp kinh phí?**
Không có. Đây là bài tập học phần.

---

## 2. Thành phần

### 2.1. Ba tập con dự kiến

| Tập | Nội dung | Nguồn | Ngưỡng của đề | Hiện có |
|---|---|---|---:|---:|
| `TRAIN` | QA có trích dẫn, sinh bán tự động từ chính văn | Văn bản quy phạm/hành chính công khai | — | 394 ứng viên |
| `VALIDATION` | Như train, tách hoàn toàn | Như train | — | 6 ứng viên |
| `USER_TEST` | **Câu hỏi của người dùng thực**, thu qua khảo sát | Người tham gia có văn bản đồng ý | bắt buộc | **0** |
| **Tổng QA** | | | **≥ 2.000** | **400 ứng viên** |
| **Kiểm thủ công** | | | **≥ 20% (≥ 400)** | **24 đã duyệt** |

**Đã phát hành:** chỉ lô pilot v2 — 24 QA, duyệt 24/24, cổng trả `pilot_sft_ready`,
đầu vào D.3 `release-valid` (18 train, 6 validation). Lô này đã dùng để chạy SFT
pilot thật.

**Tập chính (chưa phát hành):** mở rộng theo từng lô — b01 thêm 57 QA train, b02
thêm 54, b03 thêm 265. Recipe nằm ở `scripts/d2_main_b0{1,2,3}_recipes.json`, nguồn
bổ sung ở `docs/data/source-ledger-b03.json`. Các lô mới có cả câu **cần từ chối**
hoặc nói rõ giới hạn nguồn.

**Lô pilot v1 (bản trước, giữ lại để tham chiếu):** 20 QA, 21 đoạn trích, 9 nguồn.
Validator ngoại tuyến xác nhận 20/20 qua kiểm cấu trúc và 21/21 đoạn trích khớp bản
lưu. Số QA được **người** duyệt: **0**.

### 2.2. Một bản ghi QA gồm những gì

| Trường | Mô tả |
|---|---|
| `question` | Câu hỏi tiếng Việt |
| `answer` | Đáp án nêu thông tin **và điều kiện áp dụng** |
| `citations[]` | Số hiệu văn bản, điều/mục, phiên bản, URL |
| `spans[]` | Đoạn trích nguyên văn làm căn cứ, có hash bản lưu |
| `procedure_family` | Một trong năm họ thủ tục (§2.3) |
| `split` | `TRAIN` / `VALIDATION` / `USER_TEST` |
| `source_sha256` | Hash của tệp nguồn đã tải |
| `retrieved_at` | Thời điểm truy xuất |

### 2.3. Năm họ thủ tục trong phạm vi

| Họ thủ tục | Mã | Trạng thái căn cứ |
|---|---|---|
| Cấp bản sao trích lục hộ tịch / bản sao giấy khai sinh | `2.000635` | ⚠️ thời hạn **chưa thống nhất** giữa QĐ 1818 và QĐ 2163 |
| Chứng thực bản sao từ bản chính | `2.000815` | Đã xác minh Điều 20 NĐ 23/2015 (hợp nhất 753/VBHN-BTP) |
| Chứng thực chữ ký | `2.000884` | Đã xác minh phụ lục QĐ 858; chưa chốt quy trình tại Hà Nội |
| Thay đổi, cải chính, bổ sung hộ tịch, xác định lại dân tộc | `1.004859` | Đã xác minh QĐ 163 và biểu lệ phí NQ 98/2026/NQ-HĐND |
| Xác nhận thông tin hộ tịch | `2.002516` | Đã xác minh QĐ 1852 |

### 2.4. Dữ liệu ưu tiên cho DPO (D.4) — **chưa tồn tại**

| Thuộc tính | Ngưỡng của đề | Hiện có |
|---|---:|---:|
| Số cặp so sánh | ≥ 500 | **0** |
| Người đánh giá độc lập mỗi cặp | ≥ 2 **người thật** | **0** |
| Mức đồng thuận đã đo | bắt buộc | **chưa đo** |

Mỗi cặp dự kiến gồm: `prompt`, `response_a`, `response_b` (hai đáp án **từ cùng một
checkpoint SFT thật**, cùng prompt), `rater_1_label`, `rater_2_label`, lý do, và
nhãn phân xử. Hai nhãn do Hà Mạnh Thế và Trần Duy Hưng tạo **độc lập**; không chia
đôi số cặp.

### 2.5. Dữ liệu cá nhân

**Có.** Tập `USER_TEST` chứa câu hỏi do người thật viết, có thể vô tình chứa chi
tiết cá nhân (tình huống gia đình, giấy tờ). Vì vậy:

- Ẩn danh **trước khi lưu** làm dữ liệu nghiên cứu.
- Phiếu đồng ý có định danh **không vào Git**; lưu riêng, mã hóa.
- Sổ token liên kết định danh do Cao Văn Hà giữ; Thế và Hưng **không** truy cập.

### 2.6. Nội dung có thể gây hại

Không có nội dung xúc phạm hay nhạy cảm theo nghĩa thông thường. Rủi ro thực tế là
khác: **đáp án sai về thủ tục pháp lý gây hại cho người dùng.** Hai nguồn sai đã
nhận diện:

1. **Thời hạn cấp trích lục.** QĐ 1818/QĐ-TTPVHCC (hiệu lực 01/01/2026) ghi dự kiến
   3 ngày làm việc, tối đa 10 ngày nếu xác minh. QĐ 2163/QĐ-BTP (30/09/2026) ghi
   trong ngày tiếp nhận, hoặc ngày làm việc kế tiếp nếu sau 15 giờ. Chưa tìm được
   văn bản triển khai 2163 tại Hà Nội, cũng chưa có văn bản xác nhận 1818 bị thay
   thế. → **Không dùng "3/10 ngày" làm đáp án chung hiện hành.**
2. **Lệ phí.** Thông tư 226/2016/TT-BTC là căn cứ phí **chứng thực**, không phải
   biểu lệ phí **hộ tịch** Hà Nội (biểu hiện hành ở NQ 98/2026/NQ-HĐND). → Không
   trộn hai khái niệm.

---

## 3. Quá trình thu thập

### 3.1. QA từ chính văn (bán tự động)

1. Rà nguồn quốc gia (Cổng Dịch vụ công) và cổng Hà Nội, tìm **văn bản gốc** đứng
   sau trang hiển thị.
2. Lưu URL, thời điểm truy xuất và SHA-256 của tệp tải. Kiểm chữ ký CMS về toàn
   vẹn nội dung trên các PDF Hà Nội (**không** thẩm định chuỗi tin cậy).
3. Soạn recipe trích đoạn từ chính văn; mỗi QA phải neo vào đoạn trích có hash.
4. CLI chọn mẫu phân tầng theo họ thủ tục.
5. **Cổng phát hành** từ chối xuất SFT khi dữ liệu chưa đạt điều kiện.
6. Người thật kiểm thủ công trên phiếu; cột kết luận của người kiểm để trống cho
   đến khi họ điền.

### 3.2. Câu hỏi khảo sát cho `USER_TEST` — **chưa thực hiện**

Thu từ sinh viên và người thân, có văn bản đồng ý, kèm mốc để người tham gia rút
dữ liệu. **Chưa mời hay thu dữ liệu của bất kỳ ai.**

**Tại sao không sinh bằng máy?** Mục đích của `USER_TEST` là đo khả năng tổng quát
sang *cách người dân thật diễn đạt* — thường thiếu thuật ngữ, thiếu bối cảnh, hoặc
mô tả tình huống cá nhân thay vì hỏi tên thủ tục. Dùng AI sinh câu hỏi sẽ phá chính
phép đo đó, vì câu hỏi mang phân phối của mô hình. Quy tắc nội bộ của nhóm cấm việc
này.

### 3.3. Tuân thủ truy cập

| Nguồn | Quan sát | Quy tắc áp dụng |
|---|---|---|
| `dichvucong.gov.vn/robots.txt` | `*` cho `/`, chặn đường hồ sơ, nộp/sửa, SSO, đăng nhập | Không truy cập các đường bị chặn |
| `ttpvhcc.hanoi.gov.vn`, `ochodua.hanoi.gov.vn` | `Allow: /`, `Crawl-delay: 5` | Truy xuất tuần tự, cách ≥ 5 giây, không crawl toàn cổng |
| `vpcp.dichvucong.gov.vn`, CDN | `robots.txt` trả HTTP 404 | **Không có robots ≠ có giấy phép.** Chỉ theo đúng tệp đính kèm mà bài chính thức dẫn |

---

## 4. Tiền xử lý và tách tập

- Tách `TRAIN` / `VALIDATION` / `USER_TEST` **trước** mọi bước xử lý tiếp.
- Tách **nhóm gần trùng**: cùng họ thủ tục và cùng câu hỏi không được nằm ở hai tập.
- Công cụ kiểm riêng chặn rò rỉ `USER_TEST`, chặn đường dẫn thiếu, trùng họ, trùng
  câu.
- **Không dùng tập test để chọn cấu hình.**

---

## 5. Mục đích sử dụng

**Dùng cho:** SFT và DPO cho trợ lý hỏi đáp thủ tục trong phạm vi năm họ thủ tục
trên, tại Hà Nội, theo các văn bản đã ghi phiên bản.

**Không dùng cho:**

- Tư vấn pháp lý. Giá trị pháp lý thuộc về **văn bản gốc**, không thuộc mô hình.
- Suy rộng sang tỉnh/thành khác, hay sang các họ thủ tục ngoài danh mục §2.3.
- Kết luận về quy định **hiện hành** khi dữ liệu còn mâu thuẫn chưa giải quyết
  (§2.6).

**Giới hạn theo thời gian.** Kiến thức thủ tục thay đổi nhanh. Mô hình tinh chỉnh
đóng băng kiến thức tại thời điểm huấn luyện và **không tự biết** khi văn bản đổi.
Vì vậy mỗi đáp án phải dẫn số hiệu và phiên bản văn bản.

---

## 6. Phân phối

**Chưa phân phối, và chưa có căn cứ để phân phối.**

| Loại nội dung | Kết luận |
|---|---|
| Chính văn quy phạm và văn bản hành chính | Khoản 2 Điều 15 Luật SHTT (VBHN 160/2026) và khoản 2 Điều 8 VBHN 6154/2026: **không thuộc phạm vi bảo hộ quyền tác giả**. Có căn cứ dùng làm nguồn soạn QA kèm dẫn chứng đầy đủ. |
| Trang tin, bài hướng dẫn, video, snapshot web | Chỉ dùng để **tìm** và đối chiếu văn bản. Điều khoản Cổng quốc gia yêu cầu dùng lại đúng pháp luật; footer Hà Nội ghi `All Rights Reserved` và yêu cầu ghi nguồn. **Chưa** có căn cứ lấy nguyên văn hay phân phối lại. |
| Ngoại lệ nghiên cứu/huấn luyện AI | Khoản 5 Điều 7 Luật SHTT và Điều 37a–37c NĐ 17/2023 (sửa bởi 134/2026) có cơ chế dùng có điều kiện. Nhóm **ghi nhận nhưng không dựa vào** nó để duyệt hiện vật pilot — đây không phải giấy phép cào hay phân phối snapshot. |

**Không vào Git:** secret; dữ liệu cá nhân; khảo sát thô; phiếu đồng ý; checkpoint;
mô hình nền. Đường dẫn bị bỏ qua: `/data/*` (trừ `/data/samples/`), `.cache/`,
`/consent/`, `/surveys_raw/`.

---

## 7. Bảo trì

**Đầu mối:** Cao Văn Hà, phụ trách lưu trữ vận hành theo vai trò đã thống nhất —
không phải chủ sở hữu dữ liệu để dùng ngoài mục đích đã nêu.

**Phiên bản:** mỗi bản ghi mang `source_sha256` và `retrieved_at`; mỗi lô có manifest
ghi hash, kích thước và thông số từng hiện vật.

**Khi văn bản nguồn thay đổi:** tạo **phiên bản QA mới**, không sửa tại chỗ. Giữ
bản cũ kèm phạm vi áp dụng của nó. (Ví dụ đã xảy ra: `PILOT-004 v2` được giữ làm
kết quả rà hai bản nguồn cũ; nếu cần nói về thời hạn hiện hành thì phải tạo phiên
bản có QĐ 2163.)

**Xóa theo yêu cầu người tham gia:** có mốc rút dữ liệu; quy trình hủy và báo sự cố
ghi ở [privacy-workflow.md](privacy-workflow.md).

---

## 8. Hạng mục còn thiếu

| # | Hạng mục | Trạng thái |
|---|---|---|
| 1 | ≥ 2.000 QA có trích dẫn | 400 ứng viên |
| 2 | ≥ 20% kiểm thủ công bởi người thật | 24 đã duyệt |
| 3 | `USER_TEST` từ khảo sát người thật có consent | chưa có |
| 4 | ≥ 500 cặp ưu tiên, 2 người chấm độc lập, có đo đồng thuận | chưa có |
| 5 | Phát hành bộ nguồn huấn luyện (cổng D.2 chưa mở) | chưa |
| 6 | Hiện vật pilot trên máy hiện tại (ngoài Git) | cần bàn giao riêng |

**Ba hạng mục 2, 3, 4 cần người thật và không nén được bằng công sức của mã.**
