# Mẫu QA nghiên cứu tuần 1 — chưa được phát hành

## 1. Đã có gì

Đã soạn **20 QA bởi agent**, thuộc **5 họ thủ tục**, liên kết **21 trích đoạn** từ các nguồn đã đọc. Đây là câu hỏi biên soạn để thử quy trình, **không phải câu hỏi khảo sát người thật**, không phải cặp ưu tiên DPO và chưa phải tập SFT đã phê duyệt.

Hiện vật cục bộ, đã bị Git bỏ qua:

- `data/review/admin-pilot-v1/qa.jsonl`: câu hỏi, đáp án, citation, nguồn gốc AI, trạng thái review và cờ rủi ro.
- `data/review/admin-pilot-v1/source-spans.json`: trích đoạn nguyên văn đã chuẩn hóa NFC/khoảng trắng, locator, hash và liên kết phiên bản nguồn.
- `data/review/admin-pilot-v1/review-sheet.md`: bản đọc dễ rà soát cho thành viên, đủ 20 câu/đáp án, trích đoạn, URL/locator/hash và cờ rủi ro; chưa có phiếu/nhãn con người. Dùng bản này cùng hướng dẫn chấm, không coi nội dung agent viết là review thủ công.
- `.cache/admin-source-audit/`: bản đọc nguồn và chính sách dùng để đối chiếu hash/trích đoạn.

Sổ metadata được theo dõi trong repo: [source-ledger.json](source-ledger.json). Báo cáo không chứa nội dung QA hoặc trích đoạn: [admin-pilot-report.json](admin-pilot-report.json). Lý do giữ nguồn/candidate ngoài Git là chưa xác nhận quyền dùng/phân phối phần nội dung cụ thể; không chuyển chúng vào `data/samples/` khi gate chưa được giải quyết. Nếu nhận bản clone chỉ có repo mà không có các hiện vật riêng, script phải báo thiếu input, không tạo QA/snapshot thay thế.

## 2. Các trạng thái không được nhập nhằng

| Hạng mục | Bằng chứng thực tế |
|---|---|
| QA biên soạn nghiên cứu | 20, mỗi họ thủ tục 4 QA |
| Trích đoạn có vị trí trong snapshot | 21 |
| Nguồn trong sổ kiểm chứng | 9, không đồng nghĩa 9 nguồn đã được duyệt |
| QA được con người phê duyệt | **0** |
| QA đủ điều kiện huấn luyện | **0** |
| Câu hỏi khảo sát / cặp DPO / nhãn ưu tiên | **Chưa có** |

Mọi record đều `label_status = draft`, `split = unassigned`, `human_review.status = pending`, `training_allowed = false`, `redistribution_allowed = false`. Các QA có giới hạn nguồn/thời điểm, không được dùng làm câu trả lời pháp lý hiện hành cho người dân. Riêng câu thời hạn trích lục dẫn cả hai nguồn đang khác nhau, không tự chọn thời hạn thuận tiện hơn.

## 3. Phép kiểm đã thực thi

Từ thư mục gốc repo:

```sh
python scripts/validate_admin_pilot.py --output docs/data/admin-pilot-report.json
```

Đã chạy và đạt kiểm cấu trúc: hash snapshot nguồn/chính sách, hash trích đoạn, vị trí nguyên văn sau chuẩn hóa, liên kết ID/URL/locator/citation marker, nguồn gốc biên soạn và ID/câu hỏi không trùng chính xác. Không có cặp câu hỏi vượt ngưỡng Jaccard trigram 0,85 trong lần kiểm; **điều này không chứng minh hết gần trùng ngữ nghĩa**.

Đã kiểm các đầu vào lỗi bằng bản sao trong bộ nhớ, không sửa dữ liệu thật: bật cờ train khi chưa có review; đổi URL citation; thay trích đoạn bằng text không có trong nguồn; sai hash snapshot; lặp câu hỏi. Cả năm trường hợp bị từ chối.

Lệnh kiểm gate phát hành:

```sh
python scripts/validate_admin_pilot.py --require-training-ready
```

Đã chạy: thoát **mã 2**, đúng kỳ vọng `Training release blocked`. Mã 0 của kiểm cấu trúc ở lệnh đầu không có nghĩa QA đã đúng pháp lý, được human review hoặc được phép huấn luyện. Script không chứng minh tính suy ra của từng đáp án từ nguồn và không cấp quyền sử dụng nội dung.

## 4. Bàn giao cho nhóm

1. Mở QA nội bộ cùng đúng snapshot/URL/locator. Đọc [kết quả kiểm nguồn](source-audit.md) trước, đặc biệt khác biệt thời hạn trích lục và thiếu biểu lệ phí Hà Nội.
2. Rà soát nghiên cứu có thể ghi `uncertain`/lỗi khi nguồn chưa đủ; không phê duyệt dữ liệu dùng cho huấn luyện trước khi giải quyết quyền và phiên bản.
3. Dùng [phiếu kiểm QA](annotation-guide.md) cho từng QA của pilot. Mục tiêu nội bộ kiểm thủ công toàn bộ pilot, không tính kết quả agent thay cho người review.
4. Ghi reviewer, thời điểm, phiên bản, kết quả từng tiêu chí và lý do. Không đánh dấu `approved` chỉ vì script đạt hoặc citation tồn tại.
5. Nếu đổi đáp án, nguồn hay trích đoạn, tạo phiên bản mới và chạy lại kiểm. Không sửa nguồn để làm trích đoạn cũ khớp.
6. Chỉ sau các gate nguồn/quyền, review và split mới xem xét phát hành; không tự chuyển 20 QA này thành `USER_TEST`. Chưa dùng chúng sinh cặp DPO khi chưa có checkpoint SFT thật.

## 5. Tái lập và giới hạn

Validator dùng Python chuẩn, không mạng, không cần PyTorch. Báo cáo có SHA-256 của hai file pilot để truy vết; report là bằng chứng của đúng bản file đã kiểm, không phải cam kết các bản tương lai cũng đạt. Snapshot là bản trích xuất của công cụ đọc/DOM, không phải hash byte của HTML/PDF gốc. Chưa có full-source ingest hoặc crawler tự động được phê duyệt.
