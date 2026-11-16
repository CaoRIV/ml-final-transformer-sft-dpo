# Kiểm nguồn thủ tục Hà Nội — vòng nghiên cứu tuần 1

## Kết luận và giới hạn

Đã đọc 9 nguồn cho 5 họ thủ tục ứng viên, kiểm 5 URL robots và điều khoản Cổng Dịch vụ công quốc gia. Đây là **kiểm tra của agent**, không phải thẩm định pháp lý hay kiểm định thủ công của nhóm. Chưa nguồn nào được phê duyệt cho huấn luyện hoặc phân phối dataset. Sổ máy đọc được là [source-ledger.json](source-ledger.json), có URL, thời điểm UTC, kiểu bản trích xuất, đường dẫn bản lưu cục bộ và SHA-256.

Không thu danh sách hồ sơ đã xử lý, thông tin công dân, tài khoản, giấy tờ thật; không đăng nhập hay nộp thủ tục. Chỉ nghiên cứu các mô tả thủ tục công khai. Bản nguồn/trích đoạn và QA nghiên cứu được giữ ở thư mục đã bị Git bỏ qua, không sao chép toàn văn cổng vào repo.

## 1. Danh mục đối chiếu

| Họ thủ tục | Nguồn quốc gia đã đọc | Nguồn Hà Nội đã đọc | Kết luận hiện tại |
|---|---|---|---|
| Cấp bản sao trích lục hộ tịch/bản sao giấy khai sinh, `2.000635` | [NAT-EXTRACT](https://vpcp.dichvucong.gov.vn/p/home/dvc-tthc-thu-tuc-hanh-chinh-chi-tiet.html?ma_thu_tuc=1943) | [HN-EXTRACT: bài công bố 05/01/2026](https://ttpvhcc.hanoi.gov.vn/cai-cach-hanh-chinh-va-tin-khac/ha-noi-tai-cau-truc-thu-tuc-cap-ban-sao-trich-luc-ho-tich-ban-sao-giay-khai-sinh-tiet-kiem-hon-160-ty-dong-moi-nam-2850260102122029782.htm), [HN-ANNEX: tệp phương án liên kết từ bài](https://sqhx-hanoi.mediacdn.vn/91579363132710912/2026/1/2/qd-1818-pl-17673355608911154670020.pdf) | **Giữ lại để giải quyết khác biệt thời hạn/phiên bản**, không chọn tùy ý một nguồn. |
| Chứng thực bản sao từ bản chính, `2.000815` | [NAT-COPY](https://vpcp.dichvucong.gov.vn/p/home/dvc-tthc-thu-tuc-hanh-chinh-chi-tiet.html?ma_thu_tuc=2630) | [HN-COPY: Ô Chợ Dừa, 18/09/2025](https://ochodua.hanoi.gov.vn/cai-cach-hanh-chinh/thu-tuc-chung-thuc-ban-sao-tu-ban-chinh-giay-to-van-ban-2832250922082409942.htm) | Đã đọc hướng dẫn địa phương bằng trình duyệt, không còn chỉ metadata; cần kiểm phiên bản và mối quan hệ nộp online–đối chiếu bản chính. |
| Chứng thực chữ ký, `2.000884` | [NAT-SIGN](https://vpcp.dichvucong.gov.vn/p/home/dvc-tthc-thu-tuc-hanh-chinh-chi-tiet.html?ma_thu_tuc=2886) | Chưa có nguồn địa phương đủ để xác nhận áp dụng hiện hành | Chưa phê duyệt hướng dẫn hiện hành Hà Nội, nhất là phí/thời hạn. |
| Thay đổi, cải chính, bổ sung thông tin hộ tịch, xác định lại dân tộc, `1.004859` | [NAT-CORRECT](https://vpcp.dichvucong.gov.vn/p/home/dvc-tthc-thu-tuc-hanh-chinh-chi-tiet.html?ma_thu_tuc=6790) | [HN-CORRECT: hướng dẫn video 08/08/2025](https://ttpvhcc.hanoi.gov.vn/video/huong-dan-cong-dan-thuc-hien-thu-tuc-thay-doi-cai-chinh-bo-sung-thong-tin-ho-tich-xac-dinh-lai-dan-toc-truc-tuyen-tren-cong-dich-vu-cong-quoc-gia-2850250807084550697.htm) | Chỉ đọc được mô tả ngắn của video, chưa phiên âm/kiểm video; chưa có biểu lệ phí Hà Nội được đối chiếu. |
| Xác nhận thông tin hộ tịch | Chưa xác minh đúng hồ sơ quốc gia/quyết định hiện hành | [HN-CONFIRM: hướng dẫn 25/09/2025](https://ttpvhcc.hanoi.gov.vn/video/huong-dan-cong-dan-thuc-hien-thu-tuc-xac-nhan-thong-tin-ho-tich-truc-tuyen-toan-trinh-tren-cong-dich-vu-cong-quoc-gia-2850250922112613773.htm) | Đã đọc các bước bằng trình duyệt; **không tự gán mã thủ tục từ địa phương khác**. UI và hiệu lực cần kiểm tiếp. |

Đây là 5 **họ thủ tục ứng viên**, không phải 5 thủ tục đã hoàn tất hồ sơ dữ liệu. Không đếm bản sao từng loại giấy tờ hay từng nguồn trùng nhau thành thủ tục mới.

## 2. Những khác biệt phải xử lý trước huấn luyện

### Trích lục: thời hạn chưa thống nhất

- NAT-EXTRACT nêu trong ngày tiếp nhận, hoặc ngày làm việc kế tiếp nếu nhận sau 15 giờ mà chưa giải quyết ngay.
- HN-ANNEX, trang 2, B.4 ghi **thời gian dự kiến 03 ngày làm việc**, trường hợp kiểm tra/xác minh có thể kéo dài nhưng không quá 10 ngày làm việc.
- Bài HN-EXTRACT nhắc Quyết định 1818/QĐ-TTPVHCC ngày 24/12/2025 và hiệu lực 01/01/2026. Tuy nhiên, tệp liên kết thực tế là 7 trang phương án/phụ lục; phần số/ngày quyết định trong text còn trống, không phải bản quyết định đầy đủ đã ký được xác minh.
- Không suy ra pháp lý chỉ từ bài tin hoặc chữ “dự kiến”. Cần tìm quyết định hoàn chỉnh, kiểm chữ ký/bản công bố, văn bản sửa đổi và cách áp dụng hiện hành. Cho đến đó, câu hỏi thời hạn Hà Nội phải giới hạn/từ chối kết luận chắc chắn.

### Phí và cách nộp: không trộn các khái niệm

- Bảng **chi phí tuân thủ/chi phí tiết kiệm** của HN-ANNEX không phải biểu phí/lệ phí phải nộp. Không dùng con số trong bảng đó để kết luận miễn phí hiện nay.
- NAT-CORRECT nói mức lệ phí cụ thể do HĐND tỉnh/thành phố quyết định; thiếu văn bản Hà Nội thì không tự điền số tiền.
- NAT-COPY mô tả trực tiếp, HN-COPY hướng dẫn chuẩn bị/nộp online. Hai mô tả có thể là các giai đoạn/kênh khác nhau, chưa đủ để kết luận mâu thuẫn pháp luật hoặc bỏ yêu cầu bản chính.
- Trang chi tiết có trường trình tự/địa chỉ trống hoặc nhắc cấp/cơ quan cần kiểm lại. Không diễn giải ô trống thành “không yêu cầu”, không dùng địa chỉ Bộ Tư pháp như điểm tiếp nhận chung cho Hà Nội.

## 3. Truy cập và quyền dùng nguồn

| Nguồn chính sách | Quan sát thực tế | Quy tắc áp dụng cho giai đoạn này |
|---|---|---|
| [Robots dichvucong.gov.vn](https://dichvucong.gov.vn/robots.txt) | Nhóm `*` cho phép `/`, chặn đường hồ sơ, nộp/sửa hồ sơ, SSO, đăng nhập/đăng ký | Không truy cập các đường dữ liệu cá nhân/nộp hồ sơ; robots chỉ áp dụng đúng origin. |
| [Robots vpcp.dichvucong.gov.vn](https://vpcp.dichvucong.gov.vn/robots.txt) | HTTP 404 | Không tìm thấy tệp, **không** đồng nghĩa có giấy phép nội dung; không lấy robots host chính gán cho subdomain. |
| [Robots Trung tâm Hà Nội](https://ttpvhcc.hanoi.gov.vn/robots.txt), [Ô Chợ Dừa](https://ochodua.hanoi.gov.vn/robots.txt) | `Allow: /`, `Crawl-delay: 5` | Truy xuất nghiên cứu tuần tự, cách ít nhất 5 giây; không crawl toàn cổng hoặc tải danh sách hồ sơ. |
| [Robots kho CDN](https://sqhx-hanoi.mediacdn.vn/robots.txt) | HTTP 404 | Chỉ theo đúng tệp đính kèm công khai đã được bài chính thức dẫn; chưa duyệt phân phối toàn văn. |
| [Điều khoản Cổng quốc gia](https://vpcp.dichvucong.gov.vn/p/home/dvc-dieu-khoan-su-dung.html) | Sử dụng lại thông tin phải theo pháp luật; cấm truy cập/copy/công khai trái phép và gây cản trở | Chưa tìm thấy giấy phép mở rõ ràng cho dataset/huấn luyện; giữ gate quyền. |
| Footer cổng Trung tâm Hà Nội | Có `All Rights Reserved` và yêu cầu ghi rõ nguồn khi phát hành lại thông tin | Ghi công đúng nguồn; không suy diễn thành quyền huấn luyện/phân phối dataset không giới hạn. |

Nguồn là cơ quan công không tự làm mọi thành phần trang thành public domain. Không đưa bản lưu đầy đủ, ảnh, bài tin hoặc trích đoạn vào `data/samples/` chỉ vì đọc được công khai. Cần giải quyết quyền dùng phần nội dung cụ thể trước khi phát hành/huấn luyện. Nếu không có căn cứ đủ, chuyển sang văn bản hành chính/phụ lục chính thức có điều kiện sử dụng được kiểm rõ hoặc xin phép; không lách kiểm soát truy cập.

## 4. Hiện vật và bước tiếp nối

- Metadata có thể theo dõi trong Git: `docs/data/source-ledger.json`, tài liệu này và báo cáo kiểm tra không chứa toàn văn nguồn.
- Bản lưu nghiên cứu: `.cache/admin-source-audit/`, đã ignored. SHA-256 áp dụng cho **bản trích xuất đã lưu**, không mạo nhận là hash HTML/PDF gốc. Dữ liệu snapshot có thể không tái tạo byte-for-byte từ URL khi công cụ đọc hoặc nguồn đổi; cần giữ bản đã hash để audit.
- Mẫu QA/trích đoạn nội bộ: `data/review/admin-pilot-v1/`, đã ignored; xem [admin-pilot.md](admin-pilot.md). Đây không phải khảo sát, SFT release hoặc dữ liệu được kiểm thủ công.
- Bước còn lại: reviewer nhóm kiểm nội dung, tìm bản quyết định/biểu phí/nguồn địa phương còn thiếu, quyết định quyền dùng theo căn cứ cụ thể rồi mới mở rộng. Không nâng trạng thái nguồn thành `approved` từ kết quả kiểm hash/citation của script.

Tra cứu bổ sung theo số `1818/QĐ-TTPVHCC`, ngày `24/12/2025` trên miền Hà Nội và theo cụm trích lục vẫn chỉ tìm được bài HN-EXTRACT cùng các kết quả không đủ làm bản quyết định tương ứng. Chưa tìm được bản quyết định đầy đủ trong các lượt tra cứu này; không khẳng định nó không tồn tại, không dùng quyết định số khác hoặc quy định của tỉnh khác để lấp chỗ thiếu.
