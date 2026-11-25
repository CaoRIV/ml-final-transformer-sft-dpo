# Bối cảnh, quyết định và tiến độ

## Phạm vi phiên làm việc

Hồ sơ tuần 1 của Đề tài 9 — Kiến trúc Transformer và tinh chỉnh mô hình ngôn ngữ; trợ lý hỏi đáp thủ tục hành chính công. Không khởi động lại chọn đề tài. Mục tiêu 85–90/100 là định hướng, không bảo đảm. Nhóm gồm ba sinh viên tại một trường đại học ở Hà Nội: Cao Văn Hà, Hà Mạnh Thế, Trần Duy Hưng. Cao Văn Hà là trưởng nhóm, thực hiện chính, tổng hợp và nộp bài; tên trường/lớp chưa chốt.

## Kiểm kê ban đầu và nguồn quyết định

Workspace ban đầu chỉ có `.git/` và sáu PDF trong `references/`; không có `AGENTS.md`, code, notebook hoặc tài liệu kế hoạch. Không phát hiện nhiều bản đề trong kiểm kê này. Đề đang dùng: “DANH MỤC BÀI TẬP LỚN CUỐI KÌ MÔN HỌC MÁY CƠ BẢN.pdf”, ngày in trên tài liệu 12/11/2026, 46 trang. Đã đọc phần I, toàn bộ phần II và toàn bộ Đề tài 9. Trang II = 2, Đề tài 9 = 18–19 đúng bối cảnh người dùng. Danh sách và nội dung liên quan của năm bài báo được ghi riêng trong `references/README.md`.

Git ban đầu sạch trên nhánh `main`, có upstream `origin/main`; remote cấu hình `https://github.com/CaoRIV/ml-final-transformer-sft-dpo.git`. Đây là quan sát cấu hình cục bộ, không phải kiểm tra quyền mạng, trạng thái công khai hay cho phép push. Cả sáu PDF đã tracked từ trước. Không commit/push hoặc thay đổi lịch sử trong phiên này. Chưa xác minh quyền phân phối PDF; `.gitignore` mới không gỡ file đã tracked.

## Đã chốt theo người dùng/đề gốc

- Đề tài, ứng dụng, ưu tiên tuần 1; không triển khai PPO hoặc RAG ở giai đoạn này.
- Hai nhánh: Transformer ký tự tự cài đặt và tinh chỉnh mô hình tiền huấn luyện tiếng Việt 0,5–3B.
- Laptop không có GPU đủ mạnh; huấn luyện dự kiến ở Colab T4. Kết quả T4 do người dùng báo, không phải agent đo.
- Giữ code/tài liệu/cấu hình trong một repo; dữ liệu riêng và trọng số nặng không vào Git. Chỉ push sau yêu cầu rõ.
- Theo yêu cầu gốc: A20/B25/C15/D30, báo cáo/tái lập/bảo vệ10; báo cáo cuối LaTeX25–40 trang. Các ngưỡng dữ liệu, kiểm định và yêu cầu đánh giá nằm trong bảng đối chiếu, không được ngầm giảm.
- Người dùng đã đồng ý phương án dữ liệu: Hà Nội, hộ tịch–chứng thực; Truyện Kiều cho mô hình ký tự; khảo sát sinh viên/người thân và hai người chấm độc lập là Hà Mạnh Thế, Trần Duy Hưng, với Cao Văn Hà phân xử sau khi khóa nhãn. Chấp thuận phương án không xác nhận đã có dữ liệu, sự đồng ý của người khảo sát hoặc quyền dùng nguồn; các số lượng khảo sát/sinh cặp là mục tiêu vận hành, chưa đo.
- Cả nhóm cùng tham gia A–D, không giao cố định theo phần. Thế và Hưng luân phiên rà soát các đầu việc do Hà thực hiện chính. Việc luân phiên không áp dụng cho hai nhãn DPO độc lập.

## Đề xuất kỹ thuật, chưa phải phê duyệt của người dùng

- Qwen2.5-1.5B-Instruct là ứng viên, chưa chốt license/revision/tokenizer/config. Ưu tiên pilot QLoRA, không hứa vừa VRAM hay thời gian.
- Dùng DPO loss tự cài đặt ở A để so sánh loss/gradient trên logprob minibatch thật của D; không chỉ so sánh số giả rồi coi đã tích hợp.
- Đề cương khoảng5–7 trang, kế hoạch dữ liệu3–5 trang sau dàn trang; chưa đo số trang Markdown. Mẫu5–10 thủ tục và20–50 QA được kiểm nguồn là mốc nội bộ, chưa thu thập.

## Vấn đề còn mở

| Vấn đề | Cần làm | Ảnh hưởng |
|---|---|---|
| Phần I nói 2 tuần, phần II có tuần 3 | Theo hạn hoàn thành 01/12 Hà cung cấp; hỏi giảng viên cách nộp và yêu cầu tại buổi vấn đáp | Lịch bàn giao và nộp |
| Nguồn hiện hành và quyền dùng | Đã kiểm 9 nguồn/5 họ thủ tục, robots/terms và lưu hash; còn khác biệt thời hạn trích lục, quyết định/biểu phí hoặc nguồn xác nhận thiếu | Chưa được phát hành/huấn luyện từ pilot |
| Vận hành khảo sát và chấm | Đã soạn consent/survey/privacy/rubric; cần xác nhận hình thức đồng ý, kho riêng, kênh liên hệ, mốc rút và lịch trước mở | Chưa có người tham gia/consent/nhãn thật |
| Model nền, quyền bản văn ký tự | Model nền còn mở; corpus Trương Vĩnh Ký 1911 đã chuẩn bị, người duyệt nhóm đã xác nhận dùng nội bộ A.2 và xử lý trên Colab | Chờ người dùng chạy trên Colab GPU |
| Ngân sách Colab/Drive | Xác nhận khả năng dùng, đường dẫn lưu bền vững | 5 lần chạy và resume |
| Lịch rà và chấm | Chốt thời gian rà luân phiên theo đầu việc và thời gian chấm DPO độc lập của cả hai người | Tiến độ trước hạn hoàn thành |
| Q,K,V bài C.1 | Xin dữ liệu chính thức giảng viên | Không tự tạo đáp án chính thức |
| Logprob C.4 | Xác nhận bộ số giảng viên yêu cầu nếu có | Không gắn số minh họa thành đề gốc |
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

## Tiến độ và bước tiếp nối

Hồ sơ nháp, bảng đối chiếu, hướng dẫn repo và notebook môi trường là sản phẩm của phiên này; không phải bằng chứng đã hoàn thành A–D. Chưa có datasheet/model card/LaTeX cuối kỳ vì chưa tới giai đoạn và chưa có dữ liệu/mô hình.

1. Giải quyết khác biệt phiên bản/thời hạn nguồn, bổ sung quyết định/biểu phí và nguồn đối chiếu còn thiếu; nhóm review quyền và QA nháp trước khi mở rộng.
2. Nhận bàn giao bộ biểu mẫu, chốt hình thức consent, kho riêng, kênh liên hệ, mốc rút và lịch; không phát hành khảo sát khi gate chưa đạt.
3. Rà soát hồ sơ tuần 1 có kết quả audit; bổ sung trường/lớp và xác nhận mốc/định dạng nộp với giảng viên.
4. Chạy notebook Colab, lưu báo cáo bền vững; chốt API/package theo tài liệu chính thức rồi pilot SFT và DPO riêng.
5. SFT sơ bộ cần đủ sớm để sinh và chấm dữ liệu DPO trước mốc tuần2; nếu không đạt phải báo rủi ro và xin điều chỉnh, không giả dữ liệu hay âm thầm giảm yêu cầu.

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

## A.2 — đường huấn luyện đã kiểm, chưa có PPL trên Truyện Kiều

- [Notebook A.2](../../notebooks/04_char_lm.ipynb) dùng [LM ký tự](../../src/char_lm.py) với decoder A.1; [lệnh huấn luyện](../../scripts/train_char_lm.py) chạy độc lập seed 41–45, tổng hợp PPL trung bình và SD mẫu. Mỗi seed lưu cấu hình, danh tính dữ liệu, trạng thái model/optimizer/RNG và kết quả validation vào checkpoint cuối từng epoch.
- AI đã chạy tuần tự các ô notebook từ tiến trình sạch: Python 3.12.0, PyTorch 2.15.0+cpu, CUDA không khả dụng. `abc → bcd`: NLL tính từ logits và cross-entropy đều là 1,967676. Trên **chuỗi minh họa tự tạo**, 2 epoch, 9 target validation mỗi seed: PPL trung bình 3,7951 ± 0,5770 (SD mẫu, 5 seed). Không phải kết quả của văn bản tiếng Việt được chọn.
- 7 kiểm thử CPU đạt, gồm: không nhìn ký tự tương lai; PPL khi minibatch cuối ngắn và có UNK; cửa sổ không vượt split; nạp fixture qua pipeline thật và từ chối khi artifact bị sửa; chặn thiếu quyền huấn luyện; ngắt rồi resume trùng trọng số khi chạy liên tục trên CPU; từ chối resume nhầm seed.
- [Rà soát quyền ngày 25/11/2026](../data/char-corpus.md#22-rà-soát-quyền-revision-206607--chưa-đủ-căn-cứ) không xác lập được quyền cho phần Quốc ngữ của `206607`. Revision cũ được giữ dưới dạng audit, không dùng cho Colab hoặc huấn luyện.

### Chuyển nguồn sang Trương Vĩnh Ký 1911

- Theo yêu cầu của Hà, nguồn A.2 đã đổi sang *Kim, Vân, Kiều truyện*, bản Trương Vĩnh Ký 1911. AI đối chiếu chọn mẫu với scan đã kiểm checksum và chạy chuẩn bị trên CPU: **3.254 dòng, 104.181 code point**, 732 cửa sổ train/81 validation với context 128, vocab train-only 127 token, một target validation mang UNK. Điểm cắt và dữ liệu thực được ghi trong `.cache/char-corpus/manifest-1911.json`.
- Loader đã kiểm hash, split, vocab và cửa sổ của bộ thật; từ chối manifest audit `206607` và ngăn CLI huấn luyện khi chưa có `rights-1911.json` khớp manifest. Không huấn luyện thật, tạo xác nhận thay nhóm hay tải dữ liệu lên Colab. Xem [hướng dẫn bàn giao](../data/char-corpus.md#4-chuẩn-bị-cục-bộ-và-xác-nhận-quyền).
- Đã chạy các ô notebook theo thứ tự trên CPU và **11 kiểm thử đạt** (7 LM, 3 trích xuất, 1 redirect). Bài chạy 5 seed trong notebook vẫn chỉ là minh họa.
- Người dùng đã xác nhận phạm vi huấn luyện nội bộ và xử lý Colab. AI chỉ ghi thông tin người dùng cung cấp vào xác nhận riêng gắn SHA-256 của manifest, đóng gói bản chạy tại `.cache/a2-colab/`; đã chạy ô xác minh để giải nén và kiểm dữ liệu/quyền trên CPU. Notebook dừng đúng khi không có CUDA; chưa tải lên Drive, chạy GPU hay có PPL chính thức.
