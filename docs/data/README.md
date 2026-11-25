# Gói kiểm chứng dữ liệu tuần 1

Đây là bộ hiện vật phục vụ đề cương/kế hoạch dữ liệu, không phải release huấn luyện hoặc dữ liệu khảo sát đã thu thập. Phạm vi: Hà Nội, hộ tịch–chứng thực; Truyện Kiều chỉ cho mô hình ký tự phần A.

## Đọc theo thứ tự

1. [Kiểm nguồn thủ tục và những điểm còn thiếu](source-audit.md), [sổ metadata nguồn](source-ledger.json).
2. [Mẫu 20 QA nghiên cứu: vị trí, bằng chứng và cách review](admin-pilot.md), [báo cáo kiểm cấu trúc](admin-pilot-report.json).
3. [Provenance/audit Truyện Kiều](char-corpus.md), [báo cáo số đo thực](char-corpus-audit-report.json).
4. [Văn bản đồng ý và phiếu khảo sát](consent-and-survey.md).
5. [Lưu trữ, ẩn danh và rút dữ liệu](privacy-workflow.md).
6. [Phiếu kiểm QA, rubric DPO và đánh giá mù](annotation-guide.md).

## Trạng thái bàn giao

| Nhánh | Đã có | Còn chặn |
|---|---|---|
| Nguồn thủ tục | 9 nguồn nghiên cứu, 5 họ thủ tục ứng viên, URL/thời điểm/hash và kiểm robots/terms | Quyền dùng/phân phối, hiệu lực; khác biệt thời hạn trích lục; nguồn Hà Nội/mã quốc gia hoặc biểu phí còn thiếu |
| QA | 20 QA do AI biên soạn, 21 trích đoạn; script kiểm cấu trúc | 0 human approval, 0 QA sẵn sàng train; không phải test khảo sát |
| Corpus ký tự | [Trương Vĩnh Ký 1911](char-corpus.md), 3.254 dòng từ revision `206466`; đã kiểm dữ liệu và xác nhận riêng khớp manifest | Chờ chạy Colab GPU; hiện vật ngoài Git |
| Khảo sát/chấm | Văn bản thông tin/đồng ý, phiếu hỏi, quy trình riêng tư và rubric | Chưa có phê duyệt vận hành, người tham gia, consent, checkpoint SFT hoặc nhãn DPO |

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

## Việc nhóm thực hiện tiếp

- Hà tổng hợp các quyết định/văn bản còn thiếu; nhóm rà soát nguồn, quyền và các QA nháp. Không lấy kết quả AI làm quota kiểm thủ công.
- Thế/Hưng chuẩn bị chấm độc lập sau khi có SFT thật; Hà phân xử sau khi khóa nhãn. Không chia đôi cặp cho hai người.
- Xác nhận hình thức đồng ý theo quy định áp dụng, lịch, kênh liên hệ, kho riêng và thời hạn rút trước khi mời người khảo sát. Chưa phát hành biểu mẫu công khai.
- Không dùng câu hỏi test để bổ sung QA train/validation, prompt DPO hoặc chọn cấu hình. Không đưa consent/dữ liệu người vào Git hoặc API ngoài.

Cập nhật trạng thái chỉ từ sự kiện có thật. Gói này không đánh dấu A–D, 2.000 QA, 500 cặp, khảo sát hoặc huấn luyện là hoàn thành.
