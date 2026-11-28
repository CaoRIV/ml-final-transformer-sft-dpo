# Báo cáo cuối kỳ — cách biên dịch và cách sửa

**Trạng thái: bản nháp chưa nhóm duyệt.** Đầu trang còn ghi
`Bản nháp chưa nhóm duyệt`; chỉ đổi sau khi cả ba thành viên xác nhận nội dung.

## Biên dịch

```
tectonic docs/report/report.tex
```

Hoặc XeLaTeX ba lượt (để mục lục và tham chiếu chéo ổn định):

```
xelatex -output-directory=docs/report docs/report/report.tex
```

Cần font `texgyretermes` (TeX Gyre Termes, có trong TeX Live). Không đặt
`\setmonofont` để tránh phụ thuộc thêm font.

## Cấu trúc

| Tệp | Nội dung | Yêu cầu của đề |
|---|---|---|
| `report.tex` | Preamble, trang bìa, mục lục, thư mục tham khảo | G7 |
| `sections/00-tom-tat.tex` | Tóm tắt | |
| `sections/01-gioi-thieu.tex` | Bài toán, phạm vi, đầu vào/đầu ra, phân công | G1, G12 |
| `sections/02-phan-a.tex` | Dẫn xuất → cài đặt → đối chiếu cho A.1–A.4 | A, G2 |
| `sections/03-phan-b.tex` | Sáu chứng minh B.1–B.6 | B, G3 |
| `sections/04-phan-c.tex` | Bốn bài tập C.1–C.4 | C, G4 |
| `sections/05-phan-d.tex` | Trạng thái thực tế D.1–D.5 | D, G5 |
| `sections/06-tai-lap.tex` | Môi trường, seed, bộ kiểm, hạng mục còn thiếu | G8 |
| `sections/07-dao-duc.tex` | Nguồn, quyền, dữ liệu người, ranh giới AI | G9 |
| `sections/08-gioi-han.tex` | Giới hạn, rủi ro, hướng mở rộng | |
| `sections/09-phu-luc-ai.tex` | Khai báo phạm vi dùng AI | G11 |

Hai hiện vật G7 còn lại nằm ngoài thư mục này:
[datasheet](../data/datasheet.md) và [model card](../model/model-card.md).

## Quy ước phải giữ khi sửa

1. **Nhãn trạng thái.** Mỗi hạng mục dùng `\dalam`, `\motphan` hoặc `\chualam` theo
   **bằng chứng file**, không theo kế hoạch. Một hạng mục đã lập kế hoạch nhưng
   chưa chạy vẫn là `\chualam`.
2. **Không điền số chưa đo.** Các ô `— chưa đo` trong model card và các mục
   `\chualam` trong báo cáo chỉ được điền sau khi có lượt chạy thật.
3. **Phân biệt số đo với số minh họa.** C.1 và C.4 dùng đầu vào minh họa có ghi
   nguồn; không trình bày chúng như số liệu đề chính thức.
4. **Logarit tự nhiên** xuyên suốt.
5. **Ký hiệu toán** dùng chung macro với `docs/theory/part-b.tex` (`\E`, `\R`, `\PE`,
   `\Attn`, `\PPL`, `\pref`, `\pdata`, `\dmodel`, `\KL`, …). Nếu thêm macro, thêm ở
   cả hai tệp.

## Việc còn lại trước khi nộp

- [ ] Ba thành viên đọc và xác nhận nội dung → đổi `\fancyhead[R]` ở `report.tex`
      dòng 29 và dòng trạng thái ở trang bìa.
- [ ] Phần B: Thế và Hưng tự giải lại B.1–B.6 → đổi `\fancyhead[R]` trong
      `docs/theory/part-b.tex` dòng 24 và dòng trạng thái dòng 49, rồi cập nhật sáu
      dòng B1–B6 trong [ma trận yêu cầu](../progress/requirements-matrix.md).
- [ ] Kiểm độ dài: đề yêu cầu **25–40 trang**. Đếm sau lần biên dịch đầu; nếu thiếu,
      bổ sung ở Phần D khi có kết quả thật, **không** nhồi nội dung.
- [ ] Hỏi giảng viên về bộ Q/K/V chính thức cho C.1 và bộ log-xác suất cho C.4
      (xem dòng vấn đề mở trong ma trận yêu cầu).
- [ ] Bổ sung log môi trường và checkpoint của A.2 (đang thiếu PyTorch/CUDA version).
- [ ] Cập nhật `sections/09-phu-luc-ai.tex` nếu có thêm phiên hỗ trợ AI; nguồn là
      [docs/progress/ai-use.md](../progress/ai-use.md).
