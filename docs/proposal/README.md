# Hồ sơ tuần 1: Markdown, LaTeX và PDF

## Tệp bàn giao

| Tài liệu | Nội dung gốc | Nguồn LaTeX sinh tự động | PDF đã biên dịch |
|---|---|---|---|
| Đề cương | [proposal.md](proposal.md) | [proposal.tex](proposal.tex) | [proposal.pdf](proposal.pdf) |
| Kế hoạch dữ liệu | [data-plan.md](data-plan.md) | [data-plan.tex](data-plan.tex) | [data-plan.pdf](data-plan.pdf) |

**Cả hai là bản nháp tuần 1, chưa phải xác nhận đã nộp hoặc đã hoàn thành dữ liệu/thí nghiệm.** Phạm vi Hà Nội/hộ tịch–chứng thực, Truyện Kiều và phương án khảo sát/chấm đã được người dùng đồng ý. Tên trường/lớp, hạn/định dạng nộp, lịch thực hiện, ngân sách Colab và mô hình nền cuối chưa có xác nhận đầy đủ. Không điền giả các thông tin đó vào bìa.

PDF giữ toàn bộ nội dung của Markdown, bao gồm bảng và schema chi tiết, không phải bản tóm tắt cắt bớt. Mục tiêu 5–7/3–5 trang từng trao đổi là đề xuất nội bộ, không phải giới hạn của đề gốc. Không thu nhỏ chữ đến mức khó đọc chỉ để đạt số trang. Báo cáo LaTeX 25–40 trang là sản phẩm cuối kỳ khác với hai hồ sơ này.

## Một nguồn nội dung duy nhất

Sửa `proposal.md` và `data-plan.md`, sau đó chạy lại lệnh build. Không sửa tay `proposal.tex`/`data-plan.tex`: đây là các bản sinh tự động, chứa hash SHA-256 của Markdown đầu vào ở phần comment. Mẫu chung là `week1-template.tex`; bộ lọc `week1-format.lua` chỉ xử lý tiêu đề, ngắt dòng tên trường schema và chuyển liên kết giữa hai tài liệu sang PDF. Tiêu đề H1 của Markdown được thay bằng tiêu đề trang đầu có tên nhóm; toàn bộ nội dung thân được giữ lại.

## Biên dịch từ thư mục gốc repo

Cần Python 3.10 trở lên (thư viện chuẩn), **Pandoc** và **Tectonic**. Các bản dùng để tạo lần đầu: Pandoc 3.14, Tectonic 0.17.0. Công cụ portable có thể đặt ngoài repo; không cần thay đổi PyTorch hoặc môi trường huấn luyện.

```sh
python scripts/build_week1_pdfs.py
```

Nếu công cụ không ở PATH, chỉ rõ đường dẫn, đặt trong dấu ngoặc kép nếu có khoảng trắng:

```sh
python scripts/build_week1_pdfs.py --pandoc "C:/tools/pandoc/pandoc.exe" --tectonic "C:/tools/tectonic/tectonic.exe"
```

Nguồn tải chính thức:
- [Pandoc 3.14](https://github.com/jgm/pandoc/releases/tag/3.14).
- [Tectonic 0.17.0](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0).

Không commit executable, archive tải về hoặc cache. Lần chạy đầu Tectonic cần mạng để tải bundle LaTeX/font; các lần sau tái sử dụng cache. Script lưu log biên dịch vào `.cache/week1-build/` (đã bị Git bỏ qua) và sao chép hai PDF thành công vào thư mục này.

## Biên dịch trực tiếp từ LaTeX

Hai tệp `.tex` là tài liệu độc lập, không đọc Markdown trong lúc chạy LaTeX. Từ `docs/proposal/`, có thể chạy:

```sh
tectonic proposal.tex
tectonic data-plan.tex
```

Hoặc dùng XeLaTeX/Overleaf, chọn XeLaTeX và biên dịch mỗi tệp hai lần để cập nhật liên kết/bảng. Nguồn dùng font TeX Gyre Termes/Heros/Cursor bằng tên tệp OTF trong TeX, không phụ thuộc font Windows; công thức dùng Computer Modern. Cách Overleaf/XeLaTeX là hướng dẫn thay thế, không phải bằng chứng đã kiểm trên dịch vụ đó.

## Bằng chứng bản biên dịch hiện tại

- Đề cương: **7 trang**; kế hoạch dữ liệu: **11 trang**, gồm toàn bộ bảng schema chi tiết.
- Đã chạy script biên dịch bằng Pandoc 3.14/Tectonic 0.17.0; đã xem ảnh tổng quan toàn bộ trang và kiểm tra chi tiết trang đầu, công thức DPO, bảng schema.
- Hash Markdown khớp comment trong LaTeX; trích xuất được đầy đủ ba tên thành viên và mục cuối; không có trang trắng. Mọi font trong hai PDF đều được nhúng.
- Log LaTeX cuối không có `Overfull`, thiếu ký tự, font shape không xác định hoặc cảnh báo thay font; kiểm tra hình học không thấy text nằm ngoài khổ trang.
- Tectonic trên máy này vẫn in chẩn đoán Fontconfig thiếu cấu hình mặc định. Biên dịch thoát mã 0; nguồn đã chỉ định tệp font từ bundle, và các kiểm tra font nhúng/ký tự ở trên đạt. Chưa kiểm chứng trên Overleaf hoặc máy khác.


## Các việc còn thiếu để chốt bản nộp

1. Kiểm danh mục thủ tục, nguồn quốc gia/Hà Nội, hiệu lực, điều khoản và robots; chốt bản số hóa Truyện Kiều trước nhập kho.
2. Thực hiện mẫu thủ tục/QA nếu được phép và kiểm thủ công; mẫu 5–10 thủ tục/20–50 QA là mục tiêu nội bộ, không phải ngưỡng nộp tuần 1.
3. Chuẩn bị biểu mẫu đồng ý/khảo sát, quy trình ẩn danh và rubric chấm, lịch huy động người thật.
4. Bổ sung thông tin trường/lớp và phân công chuyên môn, ngân sách, nơi lưu bền vững; hỏi giảng viên lịch 2 tuần/tuần 3 và hình thức nộp.
5. Nhóm đọc, hiểu và rà soát hai tài liệu trước nộp; ghi phạm vi AI vào nhật ký/phụ lục theo yêu cầu. PDF biên dịch được không đồng nghĩa các công việc nghiên cứu trên đã hoàn tất.
