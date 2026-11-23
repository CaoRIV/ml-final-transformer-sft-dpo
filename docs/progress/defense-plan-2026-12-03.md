# Hoàn thành dự án ngày 01/12 và vấn đáp ngày 03/12/2026

**Hạn hoàn thành toàn dự án: 23h59 ngày 01/12/2026**, theo mốc Hà cung cấp. **Ngày vấn đáp: 03/12/2026.** Hà xác nhận cách nộp và hiện vật cần mang; không đợi đến ngày vấn đáp mới hoàn thành sản phẩm. Các mốc rà soát và khóa bản bên dưới là mốc nội bộ. Căn cứ về phạm vi: phần I–II tr. 1–2 và Đề tài 9 tr. 18–19; xem [ma trận yêu cầu](requirements-matrix.md) và [kế hoạch A–D](team-execution-plan.md).

## 1. Chọn cách làm nào?

**Chia theo luồng việc, không chia theo người.** Hà thực hiện chính; Thế và Hưng luân phiên rà từng đầu việc A–D theo [cách nhóm phối hợp](team-execution-plan.md#2-nhóm-phối-hợp-thế-nào). Gửi kết quả nhỏ để rà ngay, không đợi xong một phần. Riêng cặp DPO vẫn cần Thế và Hưng cùng chấm độc lập từng cặp; Hà phân xử sau khi khóa nhãn và đo đồng thuận.

1. **A–C:** ưu tiên kiểm attention/mặt nạ và DPO loss để có bằng chứng không phụ thuộc dữ liệu D. Tiếp theo hoàn thiện decoder, LoRA, mô hình ký tự, rà sáu chứng minh và giải các bài đã đủ đầu vào.
2. **Nguồn và khảo sát:** kiểm quyền dùng, hiệu lực và QA, đồng thời chuẩn bị khảo sát. Chốt đồng ý bằng văn bản, ẩn danh, kho riêng và mốc rút trước khi mời người tham gia. Giữ test riêng để không lọt vào huấn luyện hoặc chọn cấu hình.
3. **GPU và tinh chỉnh:** kiểm [Colab](../../notebooks/00_environment_check.ipynb) trong phiên mới; sàng lọc một ứng viên theo tiếng Việt, giấy phép và phiên bản. Chỉ chạy SFT trên QA đã được phép dùng và chia tập; đo riêng DPO vì còn mô hình tham chiếu.

Rà khả năng kịp phần D tối 26/11. Chưa đủ căn cứ cam kết mọi phần sẽ kịp: [báo cáo QA](../data/admin-pilot-report.json) ghi 0 QA sẵn sàng huấn luyện; chưa có khảo sát thực, checkpoint SFT/DPO hay số đo phiên GPU mới.

Bỏ việc không trực tiếp phục vụ đề: giao diện, triển khai RAG/PPO, mở rộng sang thủ tục ngoài phạm vi, làm nhiều phiên bản trình bày. Soạn khung báo cáo dựa trên hồ sơ có sẵn và bổ sung bằng chứng khi có; không viết trước kết quả.

## 2. Lịch bàn giao nội bộ

| Ngày | Việc cả nhóm làm | Bằng chứng cần có cuối mốc |
|---|---|---|
| **23–24/11** | Xác nhận cách nộp, yêu cầu vấn đáp, Q/K/V C.1 và bộ số C.4. Kiểm Colab và kho lưu. Cùng kiểm một QA với nguồn, chuẩn bị khảo sát và rà bản đầu A.1/A.4, C.2. | Log môi trường, danh sách nguồn/QA còn vướng và phép kiểm A đầu tiên. Không chờ phản hồi mới làm phần độc lập. |
| **25–26/11** | Rà PE/decoder, LoRA và điều kiện chạy mô hình ký tự. Nếu QA đủ điều kiện, chạy SFT thử, lưu và kiểm khôi phục checkpoint; sinh lô cặp để đo tốc độ chấm độc lập và thử DPO nếu đủ đầu vào. Chỉ khảo sát sau khi đủ điều kiện. | Cuối 26/11: số dữ liệu thật đủ điều kiện, kết quả kiểm A, checkpoint hoặc lý do chưa có, tốc độ chấm và dự báo GPU để xem phần D có kịp không. |
| **27–30/11** | Hoàn tất và rà A–C. Nếu lịch D khả thi, khóa QA/validation/test, chốt nhãn độc lập và đo đồng thuận trước phân xử; chạy SFT/DPO, kiểm nối A–D và đánh giá ba phiên bản trên test đã khóa. Soạn datasheet theo số thật. | **Tối 30/11:** tập hợp kết quả và minh chứng A–D để tích hợp. Nếu có phần trễ, ghi yêu cầu chưa đạt và số thực; không dồn huấn luyện hoặc chấm mới sang ngày đóng gói. |
| **01/12** | Hà tổng hợp; Thế và Hưng rà lại báo cáo, lệnh tái lập, kết quả, liên kết và quyền chia sẻ theo lượt. Cả nhóm chốt gói nội bộ lúc **20h00**. | **Hạn hoàn thành: 23h59 ngày 01/12/2026.** Gói cuối gồm báo cáo, mã/môi trường/script, dữ liệu hợp lệ hoặc script thu thập kèm datasheet, model card và phụ lục AI. Hà nộp theo kênh được xác nhận. |
| **02/12** | Cả nhóm diễn tập với gói đã khóa: luân phiên trình bày và hỏi chéo cả A–D. | Tập dùng demo hoặc log thật dự phòng. Không dự trù ngày này để huấn luyện, chấm hoặc viết tiếp báo cáo. |
| **03/12** | Cả nhóm vấn đáp bằng bản đã hoàn thành. | Phân biệt minh họa, kết quả thật và yêu cầu chưa đạt nếu có. |

## 3. Cổng quyết định tối 26/11: có mở rộng D không?

Chỉ coi **hoàn tất phần D trước 23h59 ngày 01/12** là khả thi khi cả ba điều kiện dưới đây có bằng chứng và công việc còn lại kịp mốc bàn giao tối 30/11. Không qua một điều kiện thì vẫn làm phần D có thể thực hiện hợp lệ, nhưng báo **rủi ro trễ** thay vì cam kết sẽ đủ kết quả.

| Điều kiện | Cách kiểm nhanh và hành động |
|---|---|
| **Nguồn, QA và test đủ đường đi** | Có danh mục nguồn hợp lệ đủ độ phủ, phiên bản và split rõ; có checkpoint SFT pilot từ QA được phép. Lấy số QA còn thiếu và số kiểm thủ công còn thiếu ở từng split chia cho tốc độ thực đo của nhóm; phải đủ giờ trước khi khóa dữ liệu. Đề yêu cầu ≥2.000 QA và kiểm thủ công ≥20% (ít nhất 400 nếu có đúng 2.000). Có quy trình đồng ý đã chốt, lịch thu và số câu khảo sát hợp lệ thực có; không ước tính test bằng câu tự sinh. |
| **Hai người có đủ giờ chấm** | Đo phút/cặp từng người ở lô hiệu chuẩn; dùng tỷ lệ cặp giữ lại chỉ như ước tính để tính số cặp thô còn phải sinh/chấm, gồm phần validation riêng. Tính giờ cho **từng** người và thêm thời gian Hà phân xử sau khóa nhãn. Ví dụ giả định: 700 cặp thô × 2 phút/cặp = **23 giờ 20 phút mỗi người**, chưa kể hiệu chuẩn, phân xử, chấm mù và làm các phần khác. Nếu mỗi người chỉ có 3 giờ/ngày trong 27–30/11, năng lực giả định là **360 cặp mỗi người**, không phải 720 cặp có đủ hai nhãn. Dùng tốc độ và lịch thực, không dùng số giả định để tuyên bố khả thi. |
| **GPU và đánh giá đủ quỹ thời gian** | Dự báo từ thời lượng SFT/DPO pilot, độ dài chuỗi, số bước và bộ nhớ reference đã kiểm. Tính cả sinh ứng viên, validation, 5 lần chạy độc lập hoặc 5 fold theo đề, khả năng bị ngắt, lưu/khôi phục và giờ chấm mù/CI trên test. Phần SFT cho các run cuối có thể bắt đầu khi QA đã khóa; DPO chỉ bắt đầu khi cặp và nhãn đã khóa. Không nhân 5 lần sinh từ một checkpoint thành 5 run. Nếu còn thiếu input hoặc chưa đo được phần nối tiếp quan trọng, coi lịch D cuối là chưa xác nhận. |

**Nếu không qua cổng:** Hà báo giảng viên ngay với bảng *đã có / còn thiếu / lý do / lịch có thể làm*. Chỉ đổi hạn hoặc yêu cầu khi giảng viên đồng ý. Nếu không có điều chỉnh, vẫn khóa gói đúng **23h59 ngày 01/12**, ghi rõ mục chưa đạt và bàn giao phần có bằng chứng; không gọi đó là đã hoàn thành toàn bộ đề. Không gọi pilot là tập chính, không bịa đồng ý/nhãn, không lấy test để chọn cấu hình và không bỏ qua quyền dữ liệu để kịp hạn.

## 4. Gói vấn đáp tối thiểu và cách diễn tập

- **Mở đầu:** dùng ví dụ trong [giới thiệu cho người mới](../project-overview.md) để nói bài toán, hai mô hình khác nhau ra sao và câu trả lời tốt nghĩa là gì.
- **Minh chứng A–C:** một lệnh kiểm attention/causal mask, kiểm LoRA với cập nhật khác 0 và DPO loss/gradient nếu đã chạy; sáu chứng minh trong [PDF B](../theory/part-b.pdf) sau rà soát; lời giải C và nguồn của số đầu vào. Nếu có PPL, chỉ ra validation split và log. Nếu C.1 thiếu Q/K/V, giải thích quy trình với ví dụ gắn nhãn, không gọi đó là bài chính thức.
- **Minh chứng D:** một đường truy vết *câu hỏi → đoạn nguồn → quyết định kiểm* không lộ dữ liệu hạn chế; trình bày count thật và kiểm độc lập. Nếu đã có kết quả cuối, báo đúng ba mô hình, ảo giác/từ chối, tỷ lệ thắng + khoảng tin cậy, số run và đối chiếu loss/gradient A–D. Nếu chưa, chỉ demo hiện vật đã chạy hoặc minh họa có nhãn, nói rõ còn thiếu gì. Demo không được kể như kết quả thực nghiệm.
- **Ba người hỏi chéo:** tại sao chia $\sqrt{d_k}$; vì sao causal mask ảnh hưởng đẳng biến; vì sao merge LoRA không đổi đầu ra; SFT khác DPO thế nào và reference làm gì; vì sao DPO cộng log-prob chuỗi còn PPL lấy trung bình theo token; làm sao test người thật không lọt vào train; khi nào không thể kết luận DPO tốt hơn.
- **Kiểm gói đã hoàn thành ngày 01/12:** báo cáo LaTeX 25–40 trang đủ chứng minh; Git có môi trường và script tái lập; dữ liệu hoặc script thu thập kèm datasheet; model card phần D. Phụ lục khai báo AI phải đúng quy định đề. Ảnh log hoặc video dự phòng chỉ dùng bằng chứng thật, không thay sản phẩm cuối.
