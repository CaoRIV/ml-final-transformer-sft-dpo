# Bối cảnh, quyết định và tiến độ

## Phạm vi phiên làm việc

Hồ sơ tuần 1 của Đề tài 9 — Kiến trúc Transformer và tinh chỉnh mô hình ngôn ngữ; trợ lý hỏi đáp thủ tục hành chính công. Không khởi động lại chọn đề tài. Mục tiêu 85–90/100 là định hướng, không bảo đảm. Nhóm gồm ba sinh viên tại một trường đại học ở Hà Nội: Cao Văn Hà, Hà Mạnh Thế, Trần Duy Hưng. Cao Văn Hà là trưởng nhóm, thực hiện chính, tổng hợp và nộp bài; tên trường/lớp chưa chốt.

## Kiểm kê ban đầu và nguồn quyết định

Workspace ban đầu chỉ có `.git/` và sáu PDF trong `references/`; không có `AGENTS.md`, code, notebook hoặc tài liệu kế hoạch. Không phát hiện nhiều bản đề trong kiểm kê này. Đề đang dùng: “DANH MỤC BÀI TẬP LỚN CUỐI KÌ MÔN HỌC MÁY CƠ BẢN.pdf”, ngày in trên tài liệu 12/11/2026, 46 trang. Đã đọc phần I, toàn bộ phần II và toàn bộ Đề tài 9. Trang II = 2, Đề tài 9 = 18–19 đúng bối cảnh người dùng. Danh sách và nội dung liên quan của năm bài báo được ghi riêng trong `references/README.md`.

Git ban đầu sạch trên nhánh `main`, có upstream `origin/main`; remote cấu hình `https://github.com/CaoRIV/ml-final-transformer-sft-dpo.git`. Đây là quan sát cấu hình cục bộ, không phải kiểm tra quyền mạng, trạng thái công khai hay cho phép push. Cả sáu PDF đã tracked từ trước. Không commit/push hoặc thay đổi lịch sử trong phiên này. Chưa xác minh quyền phân phối PDF; `.gitignore` mới không gỡ file đã tracked.

## Đã chốt theo người dùng/đề gốc

- Đề tài, ứng dụng, ưu tiên tuần 1; không triển khai PPO hoặc RAG ở giai đoạn này.
- Hai nhánh: Transformer ký tự tự cài đặt và tinh chỉnh mô hình tiền huấn luyện tiếng Việt 0,5–3B.
- Laptop không có GPU đủ mạnh. A.2 đã chạy trên Kaggle sau khi Colab không chạy được theo thông tin người dùng; chưa chốt môi trường cho phần D.
- Giữ code/tài liệu/cấu hình trong một repo; dữ liệu riêng và trọng số nặng không vào Git. Chỉ push sau yêu cầu rõ.
- Theo yêu cầu gốc: A20/B25/C15/D30, báo cáo/tái lập/bảo vệ10; báo cáo cuối LaTeX25–40 trang. Các ngưỡng dữ liệu, kiểm định và yêu cầu đánh giá nằm trong bảng đối chiếu, không được ngầm giảm.
- Trong mọi phase, đối chiếu từng đầu việc và tiêu chí hoàn thành với PDF đề gốc (mục I–II, Đề tài 9 tr. 18–19). Kế hoạch, tài liệu tham khảo và ví dụ minh họa không thay yêu cầu hoặc đầu vào chính thức; ghi riêng giả định và các yêu cầu chưa có bằng chứng.
- Người dùng đã đồng ý phương án dữ liệu: Hà Nội, hộ tịch–chứng thực; Truyện Kiều cho mô hình ký tự; khảo sát sinh viên/người thân và hai người chấm độc lập là Hà Mạnh Thế, Trần Duy Hưng, với Cao Văn Hà phân xử sau khi khóa nhãn. Chấp thuận phương án không xác nhận đã có dữ liệu, sự đồng ý của người khảo sát hoặc quyền dùng nguồn; các số lượng khảo sát/sinh cặp là mục tiêu vận hành, chưa đo.
- Cả nhóm cùng tham gia A–D, không giao cố định theo phần. Thế và Hưng luân phiên rà soát các đầu việc do Hà thực hiện chính. Việc luân phiên không áp dụng cho hai nhãn DPO độc lập.

## Đề xuất kỹ thuật, chưa phải phê duyệt của người dùng

- [D.3](../../README.md#d3--chuẩn-bị-sft-trên-kaggle) cố định Qwen2.5-1.5B-Instruct và revision của C.3 làm cấu hình **thử pilot**, chưa phải lựa chọn cuối cho tập chính. Dùng QLoRA trên Q/V; chưa chạy GPU hay đo VRAM.
- Dùng DPO loss tự cài đặt ở A để so sánh loss/gradient trên logprob minibatch thật của D; không chỉ so sánh số giả rồi coi đã tích hợp.
- Đề cương khoảng5–7 trang, kế hoạch dữ liệu3–5 trang sau dàn trang; chưa đo số trang Markdown. Mẫu5–10 thủ tục và20–50 QA được kiểm nguồn là mốc nội bộ, chưa thu thập.

## Vấn đề còn mở

| Vấn đề | Cần làm | Ảnh hưởng |
|---|---|---|
| Phần I nói 2 tuần, phần II có tuần 3 | Theo hạn hoàn thành 01/12 Hà cung cấp; hỏi giảng viên cách nộp và yêu cầu tại buổi vấn đáp | Lịch bàn giao và nộp |
| Nguồn hiện hành và quyền dùng | [Rà D.1](../data/source-audit.md): có bản 1818/1852, 2163, biểu lệ phí 98 và căn cứ sử dụng chính văn theo Điều 15 Luật SHTT; còn kiểm phạm vi triển khai Hà Nội theo kênh | Có thể soạn QA từ đoạn chính văn đã xác minh; 9 snapshot pilot chưa dùng để train/phân phối |
| Vận hành khảo sát và chấm | Đã soạn consent/survey/privacy/rubric; cần xác nhận hình thức đồng ý, kho riêng, kênh liên hệ, mốc rút và lịch trước mở | Chưa có người tham gia/consent/nhãn thật |
| Mô hình và GPU phần D | Đã đối chiếu model card (1,54B, có tiếng Việt) và Apache-2.0 của revision pilot; còn chạy QLoRA trên release D.2, đo bộ nhớ, lưu bền vững và kiểm resume phiên mới | Chưa chốt cấu hình cuối hoặc kiểm chất lượng tiếng Việt trên tác vụ. PPL A.2 không thay phép đo D.3/D.4 |
| Lưu trữ A.2 | Giữ Version #1 riêng tư; lưu log môi trường và đối chiếu checkpoint với cấu hình và metadata của lần chạy | Có PPL validation từ `summary.json`; chưa đối chiếu độc lập các checkpoint và log Kaggle |
| Lịch rà và chấm | Chốt thời gian rà luân phiên theo đầu việc và thời gian chấm DPO độc lập của cả hai người | Tiến độ trước hạn hoàn thành |
| Q/K/V bài C.1 | Theo Hà, giảng viên không cung cấp ma trận. Đã chọn [bộ số minh họa](#c1--bộ-ma-trận-minh-họa) theo yêu cầu của Hà. | Ghi rõ nguồn tự sinh trong bài làm; không coi đây là bộ số chính thức. |
| Logprob C.4 | Đã có lời giải tổng quát và ví dụ minh họa; thay đầu vào nếu giảng viên yêu cầu bộ số riêng | Không gắn số minh họa thành số đề gốc hoặc số đo trên checkpoint |
| Quyền PDF và remote | Kiểm tra quyền chia sẻ, xác nhận remote trước push | Không công khai ngoài ý muốn |
| Quy định AI | Giữ nguyên “Không dùng bản AI miễn phí”; nhóm xác nhận loại công cụ đang dùng | Liêm chính; không suy ra cấm Colab miễn phí |

## Bằng chứng kiểm tra giai đoạn khởi tạo (lịch sử)

- Đã kiểm kê và đọc tài liệu gốc nêu trên; chưa thu thập thủ tục, khảo sát, QA, cặp ưu tiên hoặc chạy huấn luyện.
- Đã chạy tuần tự tất cả ô code của `00_environment_check.ipynb` trong một namespace sạch bằng Python3.11.6 trên máy hiện tại; output ghi JSON môi trường và danh sách gói vào thư mục tạm, đọc lại JSON xác nhận tách nguồn bằng chứng. Đã xóa thư mục tạm sau kiểm tra.
- Lần kiểm tra đầu phát hiện lỗi escape xuống dòng trong ô lưu báo cáo; đã sửa và chạy lại thành công.
- Máy hiện tại không có PyTorch trong interpreter kiểm tra; `nvidia-smi` không tìm thấy. Notebook báo `gpu_smoke.status = not_run`, lý do `PyTorch is not installed`; **không có bằng chứng GPU chạy tại máy này**.
- Chưa chạy giao diện Colab, nhánh mount Drive, CUDA hay SFT/DPO. Người dùng cần chạy notebook trong phiên Colab mới. Không cài lại PyTorch trong phiên này.
- Kiểm tra cấu trúc JSON notebook, cell ID duy nhất và output sạch: đạt. Chưa kiểm bằng schema `nbformat` vì thư viện này không có trong interpreter hiện tại.
- Kiểm tra liên kết Markdown cục bộ trong 8 tài liệu: 7 liên kết, không có liên kết trỏ tới file thiếu tại thời điểm kiểm tra.

## Thứ tự tiếp theo sau đối chiếu đề gốc và kế hoạch tuần 1

**Điểm lệch tiến độ:** kế hoạch đặt SFT pilot cuối tuần 1/đầu tuần 2 để tạo cặp DPO sớm. Hiện chưa có QA được phép dùng cho pilot SFT và chưa có checkpoint SFT, nên chưa thể mở chấm preference. C.3 có thể làm song song, không được chờ xong C mới xử lý đường găng dữ liệu D.

1. Làm **D.1 → D.2** trước: gỡ tắc hiệu lực/quyền nguồn trong đúng phạm vi Hà Nội–hộ tịch/chứng thực và lập split theo họ thủ tục. Song song chuẩn bị điều kiện khảo sát; chỉ thu dữ liệu người thật khi đủ consent và quy trình ẩn danh.
2. Chỉ chạy **SFT pilot** khi có QA pilot hợp lệ. Khóa checkpoint, template và cấu hình sinh để Thế/Hưng chấm độc lập, khóa nhãn, đo đồng thuận rồi Hà mới phân xử. Tiếp tục mở rộng dữ liệu chính; giữ ≥2.000 QA có dẫn nguồn, ≥20% kiểm thủ công, ≥500 cặp từ SFT có hai nhãn độc lập và test khảo sát tách biệt. Báo rủi ro theo [lịch bàn giao](defense-plan-2026-12-03.md); không tự giảm ngưỡng hay đổi hạn.
3. Song song: nhóm rà A.1–A.4 và sáu chứng minh B, lưu log/checkpoint A.2; dùng bộ số minh họa đã ghi nguồn cho C.1 và C.4. Giữ [ma trận yêu cầu](requirements-matrix.md) làm tiêu chí nghiệm thu, bao gồm cầu nối A–D trên minibatch thật, so ba hệ trên test khóa và thảo luận RAG trong D.5 — không triển khai RAG/PPO.

## Bàn giao bản LaTeX/PDF tuần 1

- Hiện có `docs/proposal/proposal.tex` + `proposal.pdf` (**7 trang**) và `data-plan.tex` + `data-plan.pdf` (**12 trang** sau cập nhật audit); cả hai giữ đầy đủ nội dung Markdown và giới hạn trạng thái.
- Markdown tiếp tục là nguồn nội dung; `scripts/build_week1_pdfs.py` sinh LaTeX bằng Pandoc và biên dịch bằng Tectonic. Mẫu/bộ lọc và hướng dẫn tái lập nằm trong `docs/proposal/`.
- Đã đồng bộ những đoạn còn nói phạm vi/người chấm chưa được đồng ý; phân biệt chấp thuận kế hoạch với dữ liệu, consent, quyền dùng nguồn và kết quả thực tế.
- Đã biên dịch bằng Pandoc 3.14/Tectonic 0.17.0 portable ngoài repo, xác thực SHA-256 archive theo bản phát hành chính thức. Không cài lại PyTorch; công cụ xem PDF cài vào thư mục riêng ngoài môi trường ML.
- Kiểm tra: đã xem tổng quan mọi trang, chi tiết trang đầu/công thức/bảng; font nhúng; tên tiếng Việt và mục cuối; hash Markdown–LaTeX; không trang trắng hoặc text ngoài khổ giấy. Log cuối không có overfull, thiếu glyph hoặc cảnh báo thay font. Tectonic còn chẩn đoán Fontconfig thiếu cấu hình mặc định, nhưng dùng tệp font bundle chỉ định trực tiếp và thoát mã 0. Chưa kiểm Overleaf/máy khác.
- Đây vẫn là **bản nháp chưa nộp**. Đã có QA nháp nghiên cứu, audit corpus và bộ biểu mẫu; chưa có dữ liệu được phê duyệt, xác nhận vận hành khảo sát, consent thật hoặc huấn luyện. Biên dịch PDF không thay thế các bằng chứng đó.

## Gói kiểm chứng dữ liệu đã triển khai

- Danh mục và kết quả: `docs/data/README.md`, `source-audit.md`, `source-ledger.json`. Đã đọc 9 nguồn cho 5 họ thủ tục, kiểm 5 robots URL và điều khoản quốc gia; nguồn Hà Nội động đã được đọc bằng trình duyệt. Chưa phê duyệt hiệu lực/phân phối/huấn luyện. Phụ lục trích lục Hà Nội ghi thời hạn dự kiến khác trang quốc gia và thiếu số/ngày quyết định trong bản trích; không tự chọn một số làm đáp án hiện hành.
- Pilot riêng: `data/review/admin-pilot-v1/qa.jsonl` và `source-spans.json` (ignored): **20 QA agent-authored, 21 span, 0 human approval, 0 train-ready**. Snapshot/chính sách ở `.cache/admin-source-audit/` (ignored). Report công khai metadata tại `docs/data/admin-pilot-report.json`, không chứa toàn văn/QA.
- Đã chạy `scripts/validate_admin_pilot.py`: hash snapshot/policy/span, vị trí quote, ID/URL/locator/citation và duplicate screening đạt. 5 tình huống lỗi bị từ chối; `--require-training-ready` thoát mã2 đúng kỳ vọng, không coi kiểm cấu trúc là kiểm thủ công.
- Đã chạy audit Truyện Kiều bằng Python3.12, chỉ fetch robots và URL `/wiki/` pinned được cho phép: **3.254 dòng, 104.204 code point, split93.783/10.421, vocab133 gồmUNK, 732/81 windows độ dài128**. Đã kiểm hash, ghép split, train-only vocab và mọi cửa sổ; output research-only dưới `.cache/char-corpus/audit-206607-final/`, report metadata tại `docs/data/char-corpus-audit-report.json`. Chưa duyệt quyền/training.
- Phát hiện/reproduce việc urllib theo redirect trước kiểm URL; đã sửa chặn trước request đích. Smoke HTTP loopback trước/sau và `python -m unittest discover -s tests -p \"test_char_corpus.py\" -v`: 1 test đạt. Không kiểm raw-wikitext mode với attestation quyền thật.
- Đã soạn `consent-and-survey.md`, `privacy-workflow.md`, `annotation-guide.md`: bản người tham gia đọc/điền, quy trình ẩn danh/lưu/rút, QA review và hai nhãn độc lập/đo đồng thuận trước phân xử. Chưa mở khảo sát, không có dữ liệu người hoặc DPO giả.
- Các phần cần con người còn nguyên: xác nhận vận hành/consent theo quy định áp dụng, review nguồn/quyền/QA, tổ chức khảo sát/chấm, thông tin trường/lớp, lịch, ngân sách và Colab. Không commit/push trong gói này.
- Đã biên dịch lại hai PDF sau cập nhật audit bằng công cụ portable hiện có; kiểm hash Markdown–LaTeX, tên tiếng Việt, nội dung audit/mục cuối, font nhúng và hình học đạt; không có overfull/thiếu glyph/thay font trong log. Đã xem tổng quan mọi trang và mục bằng chứng mới ở trang cuối data-plan. Chưa kiểm trên Overleaf/máy khác; chẩn đoán Fontconfig thiếu cấu hình mặc định của Tectonic vẫn còn như lần trước.

## Bản nháp Phần B — Chứng minh lý thuyết

- [Nguồn LaTeX độc lập](../theory/part-b.tex) và [PDF 7 trang](../theory/part-b.pdf) trình bày đủ B.1–B.6 theo đề gốc tr. 18. Có phản ví dụ cho causal mask cố định, điều kiện hỗ trợ/chuẩn hóa của DPO và phân biệt trung bình theo token của PPL với tổng log-xác suất chuỗi trong DPO.
- Đã biên dịch bằng Tectonic portable 0.17.0, xem dàn trang toàn bộ 7 trang, kiểm mục lục, phông nhúng, liên kết nguồn và biên trang. Log LaTeX không có overfull, thiếu ký tự, thay phông hay tham chiếu chưa phân giải. Tectonic có chẩn đoán cấu hình Fontconfig như lần biên dịch tuần 1, nhưng đã tạo PDF thành công. Chưa kiểm Overleaf.
- Bản nháp có hỗ trợ AI, chưa được nhóm rà soát hoặc nộp. Không phải báo cáo cuối kỳ hay bằng chứng hoàn thành các phần A, C, D.

## Kế hoạch phối hợp ba thành viên

- [Kế hoạch thực hiện và bàn giao](team-execution-plan.md) diễn giải mục I–II và Đề tài 9 thành đầu vào, đầu ra, quy trình và điều kiện nghiệm thu A–D; tách các mốc bắt buộc khỏi mục tiêu nội bộ.
- Hà thực hiện chính xuyên suốt và tổng hợp; Thế và Hưng luân phiên rà từng đầu việc trong A–D. Phương án Thế/Hưng cùng chấm độc lập từng cặp DPO, Hà phân xử, không đổi.

## Hạn hoàn thành 01/12 và vấn đáp 03/12/2026

- Người dùng chốt **23h59 ngày 01/12/2026** là hạn hoàn thành toàn dự án; **03/12/2026** là ngày vấn đáp. Hà xác nhận cách nộp và hiện vật cần mang; không coi ngày 02/12 là thời gian để hoàn thiện sản phẩm.
- [Giới thiệu bài tập lớn](../project-overview.md) dành cho người ngoài nhóm. [Lịch bàn giao và vấn đáp](defense-plan-2026-12-03.md) đặt mốc rà khả năng hoàn tất D tối 26/11, bàn giao minh chứng tối 30/11 và khóa nội bộ lúc 20h00 ngày 01/12. Đây là kế hoạch, không phải bằng chứng đã hoàn thành hoặc được giảm yêu cầu.

## Tiến độ kiểm pilot QA — 24/11/2026

- **Hà báo đã tự đối chiếu 1/20 câu và thấy ổn.** Chưa ghi nhận ID và kết luận chi tiết của lượt này trong thông tin Hà cung cấp; không tự gán `approved`. 19 câu còn lại chưa có báo cáo đã kiểm thủ công.
- **Kiểm bằng máy:** báo cáo `data/review/admin-pilot-v1/auto-check-report.json` ghi 20 QA qua kiểm cấu trúc, 21 trích đoạn khớp bản lưu, 0 QA được phê duyệt trong dữ liệu và 0 QA đủ điều kiện huấn luyện. Không cộng hai loại số đếm. Mức kiểm thủ công ≥20% của tập chính vẫn chưa đạt; chưa có xác nhận giảng viên cho thay đổi.

## Cập nhật sau khi Hà điền phiếu nhanh

- Phiếu nội bộ `manual-review-20-qa-v1.md` đã có giờ, kết luận và lý do cho **20/20 QA pilot**: 17 “Chấp nhận”, 2 “Sửa câu hỏi” (001, 004), 1 “Chưa rõ” (006). Đây là kết luận nội dung của người kiểm, không phải nhãn phát hành. Mã người kiểm, ngày và múi giờ ở đầu phiếu còn trống.
- Trước khi chốt, đối chiếu lại 002 (nhân thân khác cư trú), 003–004 (phạm vi phụ lục và thời hạn), 019 (dẫn đủ hai nhánh cư trú). Không đổi kết luận gốc của Hà. Kết quả pilot không thay mức kiểm thủ công của tập chính.
- Sau lượt Hà rà lại, vẫn là **20 QA riêng biệt**: 18 “Chấp nhận”, 2 “Sửa câu hỏi” (001, 004), không còn “Chưa rõ”. 006 đã đổi kết luận; 003 đã ghi phạm vi phụ lục B.2; 019 đã giải thích cả hai nhánh nhưng khi sửa QA cần mở rộng trích đoạn tương ứng. Còn lệch căn cứ ở 002 (ghi cư trú thay vì nhân thân), 004 (chưa đối chiếu SPAN-021 để kết luận về thời hạn ở Hà Nội). Thông tin lượt kiểm ở đầu phiếu vẫn trống; không đổi trạng thái huấn luyện.
- Bản phiếu tiếp theo đã ghi mã người kiểm và ngày/tháng trong từng mục chi tiết: RV01 kiểm 8 câu, RV02 kiểm 6, RV03 kiểm 6 (22–24/11); cả 20 dòng bảng nhanh có giờ, kết luận và lý do. Không cần chép lại mã/ngày lên đầu cho từng người. Chưa thấy năm và múi giờ của các lượt kiểm được ghi ở phần thông tin chung. 002 đã bổ sung điều kiện về nhân thân nhưng còn câu về cư trú; 004 đã dẫn cả hai span nhưng kết luận “chắc chắn” chưa phù hợp với nguồn Hà Nội ghi thời hạn dự kiến. Không thay đổi kết luận của thành viên.
- Hà xác nhận tất cả lượt kiểm thuộc năm 2026, múi giờ UTC+07:00; đã ghi chung ở đầu phiếu. Lý do của 002 nay chỉ nói về thông tin nhân thân được tự điền; 004 đã phân biệt thời hạn nguồn quốc gia với thời gian dự kiến ở Hà Nội, không còn hẹn chắc. Đây là cập nhật phiếu rà nội dung, không phải duyệt phiên bản QA sửa đổi hoặc phát hành dữ liệu.
- Đối chiếu bản phiếu hiện tại: **20/20** có kết luận nội dung (**18 “Chấp nhận”, 2 “Sửa câu hỏi”**: 001 và 004), năm 2026, UTC+07:00. Cả 20 record JSONL vẫn `pending`/`unassigned`, không bật `training_allowed`; hash của JSONL và spans vẫn khớp báo cáo kiểm cấu trúc. Không quy đổi “Chấp nhận” nội dung thành `approved` hay quota kiểm thủ công của tập SFT chính.
- Hà xác nhận `PILOT-001` và `PILOT-004` v2 đều được chấp nhận về nội dung, không cần sửa thêm. Đã lưu hai kết luận do Hà cung cấp vào phiếu v2; chưa điền mã, ngày/giờ và chi tiết đối chiếu của lượt v2. Tổng vẫn là 20 QA khác nhau. Không đổi trạng thái huấn luyện.

## A.1 — bằng chứng triển khai trên CPU

- [Mã](../../src/attention.py), [notebook dẫn xuất và minh họa](../../notebooks/01_attention_decoder.ipynb), [kiểm số học](../../tests/test_attention.py). Đầu vào tensor tự tạo; seed 42, cấu hình minh họa B=2, T=5, D=12, H=3, D_ff=24. Không dùng dữ liệu hành chính hoặc bản văn ký tự.
- AI đã thực thi tuần tự các ô code trong tiến trình Python 3.12.0 sạch, PyTorch 2.15.0+cpu trong môi trường riêng `.cache/a1-cpu` trên Windows. Trọng số ví dụ cho đầu ra `[2, 3, 6]`; đổi giá trị cuối thành 120 cho `[2, 3, 42]`. Đầu ra block `(2, 5, 12)`, sai khác tiền tố lớn nhất khi đổi token cuối: `0.0`. Cả 5 kiểm thử CPU đạt, gồm đối chiếu đầu ra/gradient MHA và PE. PyTorch cảnh báo không có NumPy; các phép kiểm chạy hoàn toàn bằng tensor PyTorch.
- Tái lập trong môi trường đã tạo từ thư mục gốc: `.cache\a1-cpu\Scripts\python.exe -m unittest discover -s tests -p "test_attention.py" -v`. Chưa chạy giao diện Colab hoặc đo GPU. Đây không phải A.2–A.4, PPL hay 5 lần huấn luyện; nếu bước sau cần GPU thì bàn giao notebook để Hà chạy trên Colab.

## A.4 — bằng chứng kiểm loss DPO trên CPU

- [Hàm loss](../../src/dpo.py), [dẫn xuất và ví dụ](../../notebooks/02_dpo_loss.ipynb), [bộ kiểm](../../tests/test_dpo.py). Đã thực thi tuần tự các ô code trong tiến trình sạch của môi trường A.1 (Python 3.12.0, PyTorch 2.15.0+cpu); không cài thêm gói, không dùng số ngẫu nhiên. Cảnh báo thiếu NumPy không ảnh hưởng các phép kiểm tensor.
- Với một cặp minh họa, beta 0,5 và độ chênh policy bằng reference: loss 0,69314718, gradient theo hai log-xác suất policy là −0,25 và +0,25. Tăng log-xác suất chosen thêm 1 thì loss còn 0,47407698. Cả 4 kiểm thử CPU đạt, gồm so loss/gradient với cross-entropy hai lớp trên minibatch và kiểm biên ±1000.
- Không dùng dữ liệu người, không huấn luyện. Cầu nối A–D trên minibatch SFT/DPO thật và bài C.4 chính thức chưa được xác nhận bởi các kiểm tra này.

## A.3 — bằng chứng kiểm LoRA trên CPU

- [Lớp LoRALinear](../../src/lora.py), [notebook dẫn xuất](../../notebooks/03_lora_linear.ipynb) và [bộ kiểm](../../tests/test_lora.py). AI chạy các ô code tuần tự trong tiến trình sạch của môi trường A.1: Python 3.12.0, PyTorch 2.15.0+cpu, float64, seed 42. Không cài thêm gói. Có cảnh báo thiếu NumPy; các phép tính chỉ dùng tensor PyTorch.
- Với k=12, d=8, r=2, alpha=6: 40 tham số học, 96 trọng số nền và 8 phần tử bias đóng băng. Sau hai bước SGD trên tensor minh họa, cập nhật có hạng 2; đầu ra khác lớp nền tối đa 0,334292. Sai khác lớn nhất trước/sau gộp là 4,44 × 10⁻¹⁶. Cả 3 kiểm thử đạt, gồm lớp có/không có bias, nhiều rank, gradient và đối chiếu `linear` với trọng số gộp tường minh. Không phải kết quả tinh chỉnh phần D hoặc đo tốc độ/VRAM.

## A.2 — đã có PPL validation do nhóm chạy

- [Notebook A.2](../../notebooks/04_char_lm.ipynb) dùng [LM ký tự](../../src/char_lm.py) với decoder A.1; [lệnh huấn luyện](../../scripts/train_char_lm.py) chạy độc lập seed 41–45, tổng hợp PPL trung bình và SD mẫu. Mỗi seed lưu cấu hình, danh tính dữ liệu, trạng thái model/optimizer/RNG và kết quả validation vào checkpoint cuối từng epoch.
- AI đã chạy tuần tự các ô notebook từ tiến trình sạch: Python 3.12.0, PyTorch 2.15.0+cpu, CUDA không khả dụng. `abc → bcd`: NLL tính từ logits và cross-entropy đều là 1,967676. Trên **chuỗi minh họa tự tạo**, 2 epoch, 9 target validation mỗi seed: PPL trung bình 3,7951 ± 0,5770 (SD mẫu, 5 seed). Không phải kết quả của văn bản tiếng Việt được chọn.
- 7 kiểm thử CPU đạt, gồm: không nhìn ký tự tương lai; PPL khi minibatch cuối ngắn và có UNK; cửa sổ không vượt split; nạp fixture qua pipeline thật và từ chối khi artifact bị sửa; chặn thiếu quyền huấn luyện; ngắt rồi resume trùng trọng số khi chạy liên tục trên CPU; từ chối resume nhầm seed.
- [Rà soát quyền ngày 25/11/2026](../data/char-corpus.md#22-rà-soát-quyền-revision-206607--chưa-đủ-căn-cứ) không xác lập được quyền cho phần Quốc ngữ của `206607`. Revision cũ được giữ dưới dạng audit, không dùng cho Colab hoặc huấn luyện.

### Chuyển nguồn sang Trương Vĩnh Ký 1911

- Theo yêu cầu của Hà, nguồn A.2 đã đổi sang *Kim, Vân, Kiều truyện*, bản Trương Vĩnh Ký 1911. AI đối chiếu chọn mẫu với scan đã kiểm checksum và chạy chuẩn bị trên CPU: **3.254 dòng, 104.181 code point**, 732 cửa sổ train/81 validation với context 128, vocab train-only 127 token, một target validation mang UNK. Điểm cắt và dữ liệu thực được ghi trong `.cache/char-corpus/manifest-1911.json`.
- Loader đã kiểm hash, split, vocab và cửa sổ của bộ thật; từ chối manifest audit `206607` và ngăn CLI huấn luyện khi chưa có `rights-1911.json` khớp manifest. Không huấn luyện thật, tạo xác nhận thay nhóm hay tải dữ liệu lên Colab. Xem [hướng dẫn bàn giao](../data/char-corpus.md#4-chuẩn-bị-cục-bộ-và-xác-nhận-quyền).
- Đã chạy các ô notebook theo thứ tự trên CPU và **11 kiểm thử đạt** (7 LM, 3 trích xuất, 1 redirect). Bài chạy 5 seed trong notebook vẫn chỉ là minh họa.
- Người dùng đã xác nhận phạm vi huấn luyện nội bộ và xử lý Colab. AI chỉ ghi thông tin người dùng cung cấp vào xác nhận riêng gắn SHA-256 của manifest, đóng gói bản chạy tại `.cache/a2-colab/`; đã chạy ô xác minh để giải nén và kiểm dữ liệu/quyền trên CPU. Notebook dừng đúng khi không có CUDA; chưa tải lên Drive, chạy GPU hay có PPL chính thức.
- Người dùng báo Colab không chạy được và đã xác nhận riêng phạm vi Kaggle. Gói cục bộ `.cache/a2-kaggle/` dùng cùng manifest và cấu hình 5 seed; không mang checkpoint Colab. AI đã kiểm nạp gói dạng ZIP và đã giải nén trên CPU (732/81 cửa sổ); CLI Kaggle từ chối xác nhận chỉ dành cho Colab.
- Người dùng gửi `summary.json` từ Kaggle. AI đối chiếu manifest, cấu hình, 5 seed độc lập, 10.368 ký tự đích validation mỗi seed và tính lại toàn bộ chỉ số. [Kết quả A.2](../data/char-corpus.md#7-kết-quả-validation-a2-trên-kaggle): PPL **10,1948 ± 0,0628** (SD mẫu). Chưa đối chiếu log môi trường hoặc checkpoint Kaggle.
- Người dùng xác nhận output Kaggle đầy đủ. Ảnh đầu hiển thị `summary.json`, các thư mục `seed-41` đến `seed-45` và checkpoint epoch 1–5 của `seed-41`; bốn thư mục còn lại đang thu gọn. Ảnh tiếp theo hiển thị notebook `Chay-A2-Kaggle`, **Version #1 — Successful**, với cấu hình phiên `GPU T4 x2`. Chưa đối chiếu log PyTorch/CUDA, số GPU thực dùng hoặc nội dung checkpoint của version. Không cần chạy lại để lấy PPL.

## C.1 — Bộ ma trận minh họa

Theo Hà, giảng viên không cung cấp Q/K/V. Bộ sau được sinh ngẫu nhiên để nhóm tính tay, **không phải dữ liệu giảng viên cấp** (đề gốc tr. 19). Dùng 3 token, một head, $d_k=d_v=2$. Khởi tạo `rng = random.Random(577893521)` một lần trong Python; lấy `rng.randint(-2, 2)` theo hàng, lần lượt cho Q, K, V:

| Token | Q | K | V |
|---|---|---|---|
| 1 | (−2, 0) | (−1, −1) | (−1, 0) |
| 2 | (−1, −2) | (2, 1) | (−1, 1) |
| 3 | (1, −2) | (0, 2) | (0, −1) |

Mốc đối chiếu: $QK^\top$ có ba hàng `(2, −4, 0)`, `(3, −4, −4)`, `(1, 0, −4)`. Sau khi chia cho $\sqrt{2}$, che các cột $j>i$ trước softmax theo hàng rồi nhân V, đầu ra làm tròn 6 chữ số là `(−1, 0)`, `(−1, 0.007035)`, `(−0.980855, 0.304771)`. Đã đối chiếu phép tính vô hướng với A.1 trên CPU, float64.

[Lời giải C.1 từng token](../../notebooks/08_causal_attention_example.ipynb) trình bày ma trận điểm sau scale/mask, cách chuẩn hóa từng hàng và tổng có trọng số trên V. Đã chạy notebook trên CPU, xác nhận đúng bộ số theo seed và đối chiếu cả trọng số attention lẫn đầu ra với A.1. Sai khác tuyệt đối lớn nhất của đầu ra so với biểu thức tính tay: $1,30\times10^{-17}$.

## C.2 — số tham số và phép tính một block

- [Lời giải và kiểm CPU](../../notebooks/05_transformer_block_cost.ipynb), theo đề tr. 19, dùng đúng `DecoderBlock` A.1. Một khối có $4d^2+2df+9d+f$ tham số; một forward dense trên một chuỗi dùng $4nd^2+2ndf+2n^2d$ MAC ở các tích ma trận, với $d=d_{model}$, $f=d_{ff}$. Mask không giảm kích thước tích dense.
- AI chạy hai ô code tuần tự với Python 3.12.0, PyTorch 2.15.0+cpu. `numel()` khớp từng lớp và tổng; `aten::addmm` và `aten::bmm` khớp công thức ở $n=64,128,256$ và khi đổi 4 sang 8 head mà giữ $d$ cố định. Ở cấu hình A.2 ($d=64$, $f=128$, $h=4$, $n=128$): **33.472 tham số, 6.291.456 MAC = 12.582.912 FLOP matmul**. Không phải FLOP toàn mô hình, chi phí backward hay đo thời gian thực tế.

## C.3 — tham số LoRA Q/V và bộ nhớ 4 bit

- [Notebook C.3](../../notebooks/06_lora_qlora_cost.ipynb) dùng Qwen2.5-1.5B-Instruct revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`. Do GQA, V chỉ có 256 chiều ra, Q có 1.536. Tổng tham số học cả 28 khối là `136192 × r`; `numel()` của `LoRALinear` A.3 trên tensor meta khớp cho cả ba rank. Tổng tham số nền trước lượng tử hóa khớp metadata safetensors: 1.543.714.304.
- Đã chạy tuần tự bằng Python 3.12.0, PyTorch 2.15.0+cpu. Kịch bản không offload, NF4 + double quantization, phần nền còn lại 16 bit, adapter/grad/hai moment FP32: tổng thường trú lần lượt 1,0726 / 1,0807 / 1,0969 GiB. Với microbatch 1, chuỗi 512, cộng các đầu vào khối được checkpoint và hai tensor FP32 cỡ logits: 1,6932 / 1,7013 / 1,7175 GiB. Không phải peak thực đo hoặc bằng chứng T4 chạy vừa; không huấn luyện hay chọn mô hình D.3.

## C.4 — loss và gradient của một cặp DPO

- [Notebook C.4](../../notebooks/07_dpo_loss_gradient.ipynb) dẫn từ logit B.5 đến hai gradient theo log-xác suất policy và công thức gradient theo tham số mô hình. Với **số minh họa**, tỷ số xác suất chosen/rejected là 2 ở policy và 4 ở reference. Tại β = 1: margin = −ln 2, loss = ln 3 và gradient theo hai log-xác suất policy là (−2/3, +2/3). PDF tr. 19 không kèm bộ số.
- Đã chạy toàn bộ ô bằng Python 3.12.0, PyTorch 2.15.0+cpu, float64. So công thức vô hướng với A.4/autograd cho margin âm, bằng 0 và dương ở β = 0,1; 1; 2; 8. Reference không nhận gradient. Đây là bài tính, không huấn luyện hay chọn β cho D.4.

## D.1 — đối chiếu nguồn ngày 25/11/2026

- Đã xác minh quyết định và phụ lục 1818/1852 của Hà Nội, mã xác nhận thông tin hộ tịch `2.002516`, biểu lệ phí 98/2026 và phụ lục trích lục theo 2163/QĐ-BTP. B.3 của 2163 khớp thời hạn nguồn quốc gia; chưa xác nhận văn bản triển khai tại Hà Nội hoặc việc thay thế 1818. [Bảng theo từng thủ tục](../data/source-audit.md) ghi các mức đã xác minh và giới hạn.
- Điều 15 khoản 2 Luật SHTT cho căn cứ dùng phần văn bản hành chính/quy phạm chính thức để soạn QA; không suy quyền từ việc trang web công khai. Giữ dữ liệu/pilot ngoài Git, không đổi nhãn hoặc bật quyền train/phân phối của 9 nguồn cũ. Bước D.2 bắt đầu bằng gắn từng mệnh đề với đoạn của văn bản đã kiểm, không chuyển nguyên trạng pilot vào train.

## D.2 — pilot chính văn và cổng phát hành

- Đã tạo `d2-official-seed-v2`: 24 QA ứng viên, gồm 18 train (ba họ) và 6 validation (xác nhận hộ tịch); chứng thực bản sao là `holdout`, không có QA. Python CPU đối chiếu 24/24 mệnh đề với 23 đoạn từ 7 chứng cứ chính văn theo SHA-256; 0 cảnh báo gần trùng từ vựng. Đây là kiểm tự động, không phải 24 lượt kiểm thủ công. Giữ kết quả rà 20/20 của `admin-pilot-v1` nguyên trạng.
- Nhóm duyệt 24/24 QA và chốt biên bản nội bộ; giữ hai câu validation cùng dẫn B.4 của 1852 vì thời hạn thông thường và thời hạn tối đa khi cần xác minh là hai điều kiện khác nhau. Đã phát hành `data/review/d2/d2-official-seed-v2-release-01`: `pilot_sft_ready`, 18 train + 6 validation. Nhóm cho phép dùng bản này trên Kaggle Private (SHA-256 manifest `73771db3ea89245114009d7bc0488966f83382606db16c2573545480ff97af74`). Tập chính vẫn thiếu so với 2.000 train và chưa có `USER_TEST`. Xem [quy trình D.2](../data/README.md#triển-khai-d2).
- Công cụ evaluator chặn đầu vào khảo sát trong repo, dữ liệu thiếu, câu trùng sau chuẩn hóa và họ thủ tục lẫn SFT. Chỉ nhóm có thể xác nhận G-01–G-06, tổ chức khảo sát có đồng ý bằng văn bản, kiểm ẩn danh và khóa test riêng. Tập chính phải mở rộng nguồn hợp lệ và soạn QA khác nghĩa, sau đó đủ ≥2.000 train và ≥20% review từng split; không suy từ QA đã đếm ở pilot ra chỉ tiêu đã đạt.

## D.3 — kết quả pilot do nhóm chạy trên Kaggle

- Đã đối chiếu `metrics.jsonl` và `summary.json` do nhóm gửi, lưu bản gốc trong `.cache/d3-kaggle/received-seed-41/`. Seed 41 hoàn thành 2/2 epoch, không dừng sớm. Mỗi epoch có 1.235 token train và 388 token validation được giám sát. Validation NLL: 1,509630 → 1,242314; PPL: 4,525054 → 3,463617, khớp `exp(NLL)`. Epoch 2 được chọn. Peak bộ nhớ CUDA theo PyTorch: allocated 2,402 GiB, reserved 2,725 GiB; đây không phải tổng VRAM toàn thiết bị.
- Theo nội dung `run_manifest.json` nhóm gửi: Qwen/Qwen2.5-1.5B-Instruct revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, QLoRA NF4 double quantization, FP16, Q/V, rank 8, alpha 16, dropout 0, LR `1e-4`, batch 1, độ dài tối đa 512. Môi trường ghi nhận: Tesla T4, Python 3.13.16, torch 2.11.0+cu130, CUDA 13.0. Đã tính lại bốn SHA-256 từ hiện vật tại máy nhóm: manifest release-01, hai tệp Python trong ZIP mã và chat template tokenizer đều khớp. Đây là đối chiếu nội dung do nhóm cung cấp, không phải chạy lại trên GPU.
- Resume GPU: theo `resumed_from.json` do nhóm cung cấp, lần chạy nối từ `checkpoints/epoch-0001` của lượt seed 41, `best_epoch_before_resume=1`. Đối chiếu bản ghi epoch 2 với log liên tục: cùng 1.235 token train, train NLL 1,7503168111870646; cùng 388 token validation, NLL 1,2423135324851753 và PPL 3,463617393874577. Chỉ hai trường peak VRAM khác (resume − liên tục: allocated −1.290.240 byte, reserved +2.097.152 byte). Đạt kiểm tra nối lại theo chỉ số đã ghi; chưa so sánh trọng số adapter từng byte hay đánh giá câu trả lời. Không tính resume là seed độc lập hoặc hoàn tất D.3 tập chính.
- Hỏi thử trên Kaggle (ảnh do nhóm cung cấp): mô hình sinh được hai đáp án, nhưng đều không đạt mục tiêu của câu minh họa. Với xác nhận thông tin hộ tịch, mô hình trả 15/30 ngày làm việc và tự nhận “mới nhất”; phụ lục 1852/QĐ-TTPVHCC, B.4 tr. 3 ghi dự kiến 03 ngày, nếu cần kiểm tra/xác minh thì không quá 10 ngày làm việc. Với thị thực du lịch Nhật Bản, mô hình hướng dẫn thay vì nêu ngoài phạm vi. Cả hai chỉ ghi `[1]` không có nguồn truy xuất trong đầu ra. Giữ đây là quan sát định tính, không phải điểm D.5 hay nhãn DPO. Không chuyển hai QA validation cùng dẫn B.4 vào train để sửa kết quả demo.

## D.2 — lô đầu của tập chính sau khi hỏi thử

- [Bản ứng viên b01](../data/README.md#tập-chính-d2--lô-ứng-viên-b01) thêm 57 câu train; giữ nội dung, dẫn nguồn và split của 24 QA cũ. Tổng 75 train, 6 validation. Không thêm câu demo hoặc nguồn validation vào train; không dùng khảo sát. Chưa chạy lại SFT và chưa đo được việc mở rộng có cải thiện trợ lý hay không.
- Kiểm trên CPU: 84 mệnh đề định vị được, 0 cảnh báo gần trùng từ vựng; hash manifest `release-01` không đổi. Lệnh `check` chặn do chưa đạt 2.000 train, 0/18 phiếu train và 0/2 phiếu validation được duyệt ở bản này, chưa có biên bản lô. Nhóm kiểm `data/review/d2/d2-official-main-b01/manual-review.csv` và bổ sung nguồn cho lô kế tiếp; không tải b01 lên Kaggle theo quyền của pilot.
- **B02:** tiếp tục soạn, không mở lại hai đợt kiểm thủ công. [Lô mới](../data/README.md#tập-chính-d2--lô-ứng-viên-b02) thêm 54 QA train (59 mệnh đề, 4 chứng cứ); tổng 129 train và 6 validation. Kiểm tự động xác nhận 81 QA b01 không đổi ngoài phiên bản bộ dữ liệu và đối chiếu CSV khớp 54 câu mới. Không dùng test, không phát hành, không chạy huấn luyện.
- **B03:** [400 QA tích lũy, có CSV riêng cho 265 câu mới](../data/README.md#tập-chính-d2--lô-ứng-viên-b03). Tổng 394 train, 6 validation; không thêm câu hỏi khảo sát hay trộn họ validation vào train. Mẫu phân tầng do công cụ chọn gồm 82 train và 2 validation; đây là số được chọn, không phải số đã duyệt. Hai lần kiểm cũ giữ nguyên; chưa phát hành b03 hay chạy lại trợ lý.

### Bàn giao nội bộ trước hạn 01/12

- Phân biệt **394 bản ghi train** với **394 câu mới**. Đối chiếu theo `qa_id`, `record_version`, câu hỏi, đáp án, split, span và phiên bản nguồn: 18 train và cả 6 validation b03 giữ nguyên so với pilot release-01. Vì vậy 376 câu train nằm ngoài pilot đó. Mẫu b03 có 82 train + 2 validation, trong đó 7 train + 2 validation trùng nội dung pilot. Không cộng lượt kiểm pilot lần thứ hai, cũng không chép nhãn/căn giờ pilot vào phiếu b03; cổng hiện tại kiểm phiếu theo đúng mẫu và phiên bản.
- **Phân công đề xuất, chưa phải xác nhận tham gia:** Thế và Hưng có thể chia đôi việc rà QA. Ưu tiên dòng thuộc mẫu chính thức trước. Riêng hiệu chuẩn và DPO, **mỗi người chấm cùng toàn bộ các cặp** trên phiếu riêng, ghi thời lượng thật, khóa nhãn trước khi trao đổi; Hà quy về cùng ID đáp án rồi mới tính đồng thuận và phân xử. Mười cặp hiệu chuẩn không tính vào 500.
- `USER_TEST`: Thế đề nghị mời lớp và người thân. Hà phụ trách xác nhận G-01–G-06 và quyền truy cập trước khi mời; Thế chỉ chuyển lời mời tới người từ đủ 18 tuổi, không nhận phiếu hoặc xem câu hỏi. Người thu/kiểm ẩn danh được chỉ định riêng; nếu chưa bố trí được vai trò tách khỏi soạn QA, tune và chấm DPO thì chưa thu. Dùng [phiếu consent và khảo sát tách riêng](../data/consent-and-survey.md); không phát Google Forms hay nhận câu trả lời qua chat.
- **Quyết định lịch đề xuất:** ngay sau hiệu chuẩn, so thời gian còn trống của từng người với số cặp thực sự có thể hoàn thành, kể cả cặp hòa/loại và thời gian GPU cho DPO, D.5. Nếu không khả thi, Hà xin gia hạn ngay; nếu chưa được chấp thuận, giữ hạn 23h59 ngày 01/12 và nộp số liệu thực, nêu rõ phần thiếu. Không đợi đủ 394 phiếu mới tổ chức các việc độc lập này.
