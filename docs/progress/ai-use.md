# Nhật ký hỗ trợ AI — nguyên liệu cho phụ lục

Đây là ghi nhận hỗ trợ, không phải xác nhận nhóm đã đáp ứng quy định tài khoản AI. Đề gốc phần II trang2 ghi: “Không dùng bản AI miễn phí”. Nhóm cần bảo đảm công cụ sử dụng phù hợp; không diễn giải quy định này thành cấm Colab miễn phí.

## Phiên chuẩn bị hồ sơ tuần1

- Công cụ: trợ lý lập trình AI trong workspace, có hỗ trợ soạn tài liệu bởi các tác vụ AI song song. Chưa xác minh gói tài khoản/dịch vụ mà nhóm sử dụng.
- Phạm vi: kiểm kê Git/tài liệu; đọc và đối chiếu PDF; soạn bảng yêu cầu, đề cương, kế hoạch dữ liệu, hướng dẫn repo và bối cảnh bàn giao; tạo notebook kiểm tra môi trường; thực thi kiểm tra cục bộ và sửa lỗi ô lưu báo cáo.
- Không thực hiện: khảo sát con người, gán nhãn ưu tiên thật, thu thập mẫu thủ tục, huấn luyện, tạo kết quả đánh giá, thay thế bài giải Q/K/V chính thức.
- Dữ liệu đầu vào: yêu cầu người dùng và sáu PDF có sẵn trong workspace; thông số phiên Colab trước do người dùng cung cấp, không nhận là kết quả agent.
- Trách nhiệm nhóm: đọc lại nguồn, xác minh các giả thiết, lựa chọn phạm vi/mô hình, hiểu và giải thích được code và chứng minh; ghi sửa đổi do thành viên thực hiện, công cụ/phiên bản và phạm vi AI ở các phiên sau. Chưa ghi tên người kiểm duyệt vì chưa có xác nhận.

Khi lập báo cáo cuối, chuyển nhật ký này thành phụ lục khai báo trung thực, bổ sung các lần hỗ trợ về code/chứng minh/dữ liệu và phần đã được con người kiểm chứng. Không ghi “không dùng AI” hoặc coi văn bản AI là nguồn học thuật thay năm bài báo/đề gốc.

## Phiên dàn trang hồ sơ tuần 1

- Hỗ trợ AI: rà soát trạng thái đã chốt/còn mở; chỉnh diễn đạt để không nhầm chấp thuận kế hoạch với kết quả; tạo mẫu LaTeX, bộ lọc Pandoc và script sinh/biên dịch hai PDF từ Markdown.
- Giữ Markdown làm nguồn nội dung; không tạo kết quả khảo sát, huấn luyện hoặc đồng thuận người chấm. Nguồn LaTeX/PDF không phải bằng chứng đã hoàn thành A–D.
- Công cụ biên dịch portable và công cụ kiểm tra PDF được chuẩn bị ngoài repo, tách khỏi môi trường huấn luyện. Bằng chứng biên dịch và giới hạn kiểm tra được cập nhật trong hồ sơ tiến độ sau khi chạy.
- Chưa có xác nhận nhóm đã duyệt nội dung cuối hoặc xác minh loại tài khoản AI; các thành viên vẫn chịu trách nhiệm đọc, hiểu và bảo vệ tài liệu.

## Phiên kiểm chứng dữ liệu tuần 1

- AI nghiên cứu nguồn quốc gia/Hà Nội, kiểm robots/điều khoản, đọc trang động và tệp phụ lục; lưu metadata và snapshot hash. Phát hiện khác biệt thời hạn trích lục, chưa kết luận nguồn nào hiện hành hoặc quyền huấn luyện/phân phối.
- AI biên soạn 20 QA nghiên cứu từ nguồn đã đọc, đối chiếu 21 trích đoạn và chạy kiểm cấu trúc/gate phát hành. Không phải khảo sát thật; số QA được con người phê duyệt vẫn bằng 0. Dữ liệu nháp và trích đoạn giữ ngoài Git.
- AI soạn bộ đồng ý/khảo sát, riêng tư và rubric/phiếu chấm. Chưa mời hoặc thu dữ liệu người tham gia, chưa gán nhãn DPO.
- AI xác minh revision Truyện Kiều, chạy audit kỹ thuật trên nguồn rendered được robots cho phép, tạo corpus/split/vocabulary/windows trong cache với nhãn research-only. API metadata đã được đọc trong bước nghiên cứu trước khi xác định robots chặn `/w/`; sau đó không lặp API/raw, chỉ dùng route `/wiki/` được cho phép. Không che giấu giới hạn này.
- Đã phát hiện, tái hiện và sửa việc theo redirect trước kiểm URL đích trong script corpus; có kiểm thử hồi quy. Không dùng kết quả kiểm kỹ thuật làm xác nhận quyền hoặc thành tích huấn luyện.
- Cập nhật hồ sơ và biên dịch PDF từ Markdown; mọi review quyền, review thủ công, consent và nhãn con người vẫn cần sự kiện thật và audit riêng.

## Phiên soạn Phần B — Chứng minh lý thuyết

- AI đối chiếu sáu yêu cầu với đề gốc tr. 18 và đọc các phần liên quan của Attention, LoRA và DPO. AI soạn toàn bộ bản nháp LaTeX B.1–B.6, gồm phát biểu, giả thiết, các bước chứng minh, diễn giải và ví dụ minh họa; biên dịch và kiểm PDF.
- Không dùng ví dụ minh họa thay đầu vào chính thức của Phần C. Không có kết quả huấn luyện hoặc thẩm định của giảng viên. Nhóm chưa xác nhận duyệt nội dung; từng thành viên cần tự rà soát và giải thích được cả sáu chứng minh. Chưa xác minh loại tài khoản AI.

## Phiên soạn kế hoạch phối hợp nhóm

- AI đọc lại phần I–II và Đề tài 9, đối chiếu với đề cương, kế hoạch dữ liệu và bằng chứng trong repo; soạn kế hoạch nội bộ về quy trình, đầu ra, nghiệm thu và phụ thuộc A–D. Không thay nhóm xác nhận phân công, kiểm thủ công, thu dữ liệu hoặc huấn luyện.

## Phiên chuẩn bị vấn đáp 03/12

- AI soạn bản giới thiệu phổ thông và lịch chuẩn bị theo ngày vấn đáp người dùng cung cấp. Phân tích tải chấm bằng ví dụ giả định, không đo tốc độ người chấm/GPU và không xác nhận thời điểm nộp hoặc kết quả mới.

## Phiên chỉnh văn phong kế hoạch nhóm

- AI viết lại kế hoạch A–D bằng tiếng Việt dễ đọc, làm rõ phần dẫn xuất bắt buộc ở A, phân biệt yêu cầu của đề với lựa chọn của nhóm và tách mốc vấn đáp khỏi hạn nộp chưa xác nhận. Không thay đổi phân công đã chốt hoặc tuyên bố kết quả thực nghiệm mới.

## Phiên tổ chức lại README

- AI sắp xếp README thành lộ trình đọc chung, liên kết theo vai trò, hồ sơ và hướng dẫn chạy kiểm tra. Không sửa yêu cầu, lịch hay trạng thái thực nghiệm.

## Phiên cập nhật hạn hoàn thành

- AI cập nhật lịch ngược theo hạn 23h59 ngày 01/12/2026 do người dùng cung cấp, tách ngày diễn tập và vấn đáp khỏi thời gian hoàn thiện sản phẩm. Không xác nhận thêm kết quả hoặc thay đổi yêu cầu học phần.

## Phiên cập nhật cách phối hợp nhóm

- AI cập nhật README, kế hoạch, lịch bàn giao và đề cương theo quyết định của người dùng: Hà thực hiện chính, Thế và Hưng rà luân phiên, không giao cố định A–D theo người. Không đổi hạn, quy trình chấm DPO hoặc trạng thái thực nghiệm.

## Rà sơ bộ pilot QA trước vòng kiểm của Hà — 24/11/2026

- AI đối chiếu 20 QA bản 1 với 21 đoạn dẫn, kiểm ngữ cảnh bản lưu và mở lại bốn trang thủ tục quốc gia; phân biệt câu hỏi mơ hồ, đáp án mất điều kiện, trích dẫn thiếu và giới hạn phiên bản. Đề xuất sửa từng câu trong `data/review/admin-pilot-v1/ai-review-v1.md` (nội bộ, ngoài Git).
- Không thay dữ liệu gốc, không điền phiếu của Hà, không xác minh hiệu lực pháp lý hoặc cấp quyền dùng nguồn. Nhận xét AI không được tính vào số QA đã kiểm thủ công.
- AI tạo một phiếu nội bộ để Hà kiểm lần lượt 20 QA: chép câu hỏi, đáp án và đoạn dẫn của đúng phiên bản, để trống toàn bộ kết luận và thông tin lượt kiểm. Không tính việc tạo phiếu là kiểm định của con người.
- Theo yêu cầu của Hà, AI điền cột minh họa riêng cho `PILOT-001` (phân biệt vai trò trong câu hỏi với độ đúng của đáp án); cột kết luận của người kiểm vẫn trống.
- AI bổ sung cột mẫu cho `PILOT-002` đến `PILOT-020` dựa trên vòng rà sơ bộ trước đó; không thay câu hỏi, đáp án, trích dẫn hay ghi kết quả vào cột của Hà.
- Khi nhóm chưa có thời gian kiểm thủ công, AI chạy validator ngoại tuyến và lưu báo cáo riêng `auto-check-report.json`: 20 QA qua kiểm cấu trúc, 21 trích đoạn khớp bản lưu, 0 QA được người duyệt, 0 QA đủ điều kiện huấn luyện. Không điền phiếu thủ công.
- AI bổ sung hướng dẫn dùng metadata điền sẵn để giảm thao tác và ghi riêng tiến độ 1/20 do Hà báo. Không gán lượt kiểm cho một ID, sao chép kết luận hay thay đổi nhãn của người kiểm.
- AI rút gọn giao diện ghi nhận ở đầu phiếu thành một dòng cho mỗi QA, giữ nguyên phần kiểm chi tiết. Không điền dữ liệu của người kiểm hoặc đổi trạng thái phê duyệt.
- AI thêm một dòng minh họa riêng cho `PILOT-001` trong bảng rút gọn; giờ ghi rõ là ví dụ, không điền vào dòng người kiểm.
- Sau khi Hà thông báo đã kiểm, AI đọc và tổng hợp các kết luận có trong bảng nhanh, chỉ ra các dòng cần đối chiếu lại. Không sửa phiếu của Hà hoặc phê duyệt dữ liệu.
- Ở lượt rà lại, AI tổng hợp số đếm mới và phân biệt phần giải thích đã bổ sung với trích dẫn trong QA gốc; không sửa quyết định của Hà.
- AI ghi năm và múi giờ theo xác nhận của Hà, đối chiếu ghi chú đã sửa ở 002 và 004; giữ nguyên các kết luận thủ công.

## Cài đặt và kiểm A.1

- AI viết `src/attention.py`, notebook dẫn xuất và bộ kiểm; dùng SDPA/MultiheadAttention của PyTorch chỉ ở phía đối chiếu. AI chạy trên CPU cục bộ, không chạy GPU hoặc Colab thay nhóm. Thành viên cần tự chạy lại và giải thích phép che, tách/ghép head và hai nhánh residual. Không có lượt huấn luyện nào ở bước này.

## Cài đặt và kiểm A.4

- AI triển khai hàm DPO, soạn notebook dẫn xuất và bộ kiểm CPU bằng số minh họa. AI đối chiếu loss và gradient theo log-xác suất policy; không tạo nhãn người, dùng checkpoint hoặc xác nhận kết quả phần D. Nhóm cần tự chạy lại và giải thích vai trò reference, beta và dấu gradient.

## Cài đặt và kiểm A.3

- AI triển khai lớp LoRA bọc `nn.Linear`, notebook dẫn xuất và bộ kiểm CPU; chạy đối chiếu số tham số, cập nhật hai ma trận và gộp sau cập nhật khác 0. Thành viên cần tự chạy lại và giải thích vì sao B khởi tạo bằng 0 không chặn việc học ở bước đầu, cũng như vì sao lớp gộp chỉ cần một phép tuyến tính.

## Cài đặt A.2 — mô hình ngôn ngữ ký tự

- AI viết LM dùng decoder A.1, mã đọc dữ liệu có kiểm quyền, vòng huấn luyện, tính PPL, lưu/khôi phục checkpoint, notebook và bộ kiểm. Ví dụ `abc → bcd` và các chuỗi ngắn do AI tạo chỉ dùng kiểm mã, không thay corpus tiếng Việt hoặc số liệu thực nghiệm. AI không phê duyệt quyền cho bản số hóa, không chạy Colab thay nhóm.
- Thành viên cần tự giải thích cách dịch target một vị trí, vì sao tách văn bản trước khi tạo cửa sổ, và vì sao lấy tổng NLL chia tổng số target trước khi tính hàm mũ. Khi nhóm chạy trên corpus đã duyệt, ghi riêng ai thực hiện, revision, cấu hình và kết quả từng seed.
- AI tra Luật Sở hữu trí tuệ, điều khoản nền tảng, nhãn quyền và nguồn phiên âm của revision `206607`; đối chiếu một khác biệt giữa hai revision và tìm scan Trương Vĩnh Ký 1911 làm phương án thay thế. [Rà soát](../data/char-corpus.md#22-rà-soát-quyền-revision-206607--chưa-đủ-căn-cứ) không phải attestation, không ký thay người có thẩm quyền, không đổi corpus hoặc tải dữ liệu lên Colab.
- Theo yêu cầu đổi nguồn, AI tải hai snapshot có kiểm robots, kiểm checksum scan, đối chiếu mẫu trang thơ và viết bộ trích, chuẩn bị, xác minh dữ liệu bản Trương Vĩnh Ký 1911. AI chuyển lệnh và notebook sang manifest mới, không thực hiện kiểm từng dòng, không ký xác nhận thay thành viên và không huấn luyện bộ thật.
- AI lưu xác nhận từ mã người duyệt, thời điểm và phạm vi do người dùng cung cấp, đóng gói mã/dữ liệu và tạo notebook Colab. AI kiểm bước giải nén, hash và xác nhận cục bộ; không duyệt thay người dùng, tải lên Drive hay chạy Colab.
- AI lưu xác nhận Kaggle do người dùng cung cấp, thêm kiểm phạm vi nền tảng cho CLI, đóng gói notebook và đo kết quả bước kiểm dữ liệu trên CPU. Không tạo dataset/notebook trên tài khoản Kaggle hoặc chạy huấn luyện thay người dùng.
- AI đối chiếu `summary.json` do người dùng cung cấp, tính lại NLL→PPL từng seed và thống kê tổng hợp, rồi ghi bảng vào hồ sơ corpus. Không chạy lại huấn luyện hoặc xác nhận phần cứng Kaggle từ JSON.

## C.2 — đếm tham số và phép tính

- AI dẫn xuất số tham số và MAC theo kích thước tensor của `DecoderBlock` A.1, rồi chạy notebook CPU để đối chiếu `numel()` và FLOP matmul do profiler ước lượng. Nhóm cần giải thích được tại sao $h(d/h)=d$ và vì sao causal mask A.1 không chia đôi MAC.

## Đối chiếu lại tiến độ với đề gốc

- AI đối chiếu đề (tr. 1–2, 18–19), hồ sơ tuần 1, bảng nhanh QA hiện tại và metadata Kaggle; sửa trạng thái, tách test khỏi schema cặp DPO, đưa điều kiện SFT pilot và thảo luận RAG vào điểm rà. Không sửa phiếu người kiểm, bản ghi QA, quyền dữ liệu hay kết quả huấn luyện.
- AI soạn bản sửa `PILOT-001` (làm rõ vai trò ủy quyền) và `PILOT-004` (giữ đủ điều kiện và tách hai mốc nguồn) để nhóm kiểm lại trên phiếu v2. Không điền kết luận người kiểm hoặc đổi dữ liệu pilot v1.
- Sau khi Hà báo kết quả, AI chép lại hai kết luận do Hà cung cấp vào phiếu v2. Không tự chấm, điền chi tiết người kiểm chưa cung cấp hoặc đổi trạng thái release.

## D.1 — kiểm nguồn thủ tục

- AI truy tìm văn bản công khai, đối chiếu số hiệu, ngày, phạm vi, phụ lục và căn cứ quyền tác giả; lưu URL, thời điểm và SHA-256. AI kiểm chữ ký CMS về toàn vẹn nội dung trên bốn PDF Hà Nội, không thẩm định chuỗi tin cậy. Không đăng nhập, lấy hồ sơ công dân, tự phê duyệt nguồn hoặc đổi kết luận kiểm thủ công của nhóm.

## D.2 — tạo QA ứng viên và kiểm cổng dữ liệu

- AI soạn recipe từ chính văn, kiểm SHA-256 và đoạn trích, sửa nhầm dẫn chứng chữ ký người dịch trong bản nháp, triển khai CLI chọn mẫu phân tầng và cổng xuất SFT. Chạy trên CPU với 24 QA ứng viên; gói chỉ ghi `draft` và phiếu v2 để trống. Không điền nhãn hoặc chuyển kết quả kiểm của 20 QA cũ.
- AI cài công cụ kiểm tách `USER_TEST` và kiểm nhánh chặn đường dẫn/dữ liệu thiếu, trùng họ, trùng câu. Việc thử phần so khớp chỉ dùng prompt QA chính văn trong bộ nhớ, không tạo record khảo sát. Không tuyển người, xem phiếu thật, làm consent, gán nhãn người kiểm hay phát hành dữ liệu huấn luyện.
- AI rút gọn phiếu nhập tay cho 24 QA pilot từ 27 xuống 8 cột, giữ nguyên câu hỏi, đáp án, trích đoạn, mẫu kiểm và phiếu gốc. Đã thử cổng với phiếu trống và bản sao tạm để kiểm định dạng; không điền kết quả kiểm định thật và không giảm số QA phải được người kiểm.

## C.3 — LoRA và QLoRA trên một cấu hình Qwen

- AI đối chiếu đề tr. 19, cấu hình Qwen khóa revision, mã Qwen2 và giả định double quantization của bài QLoRA; viết notebook và chạy các ô tuần tự trên CPU để kiểm số tham số bằng lớp A.3. Phần bộ nhớ là ước lượng theo các tensor được nêu, không có phép đo GPU, tải checkpoint hay kết quả huấn luyện. Nhóm cần giải thích vì sao V nhỏ hơn Q và vì sao bộ nhớ tĩnh không phải peak khi huấn luyện.

## C.4 — tính loss, gradient DPO và xét β

- AI đối chiếu đề tr. 19, B.5 và Eq. (7) của bài DPO; tự đặt bốn log-xác suất minh họa, trình bày phép thế số và kiểm loss/gradient với A.4 và autograd trên CPU. Các ca so sánh tác động của β là phép tính xác định, không phải nhãn ưu tiên thật hay kết quả D.4. Nhóm cần giải thích vì sao policy có thể ưu tiên chosen nhưng margin DPO vẫn âm.

## C.1 — chọn đầu vào minh họa

- Theo yêu cầu của Hà, AI sinh ma trận Q/K/V với seed `577893521`, lưu đầu vào tái lập và kiểm kết quả attention nhân quả bằng mã A.1 trên CPU. Việc giảng viên không cung cấp ma trận là thông tin do Hà báo; không ghi bộ tự sinh là dữ liệu chính thức.
- AI soạn phép tính tay C.1 cho từng token trên đúng bộ ma trận đã chọn, chạy notebook CPU để so khớp softmax và đầu ra với hàm attention A.1. Không thay đổi ma trận hay nguồn gốc của ví dụ.

## D.3 — chuẩn bị pilot SFT trong lúc nhóm kiểm D.2

- AI đối chiếu D.3 tr. 19 với model card và Apache-2.0 đúng revision Qwen; chuẩn bị bộ nạp release D.2, mã QLoRA, notebook Kaggle, đóng gói tối thiểu và phương án so `r`, `alpha`, LR, epoch trên validation. Không đọc/sửa phiếu đang điền, không cấp quyền nền tảng, không tạo biên bản thay người kiểm.
- CPU: 7 test bộ nạp/mask qua; thêm một câu minh họa độc lập với tokenizer Qwen đúng revision: 71 token prompt bị che, giải mã 19 token đích khớp nguyên đáp án có dấu, trích dẫn và đúng một EOS. Đã chạy forward trên Qwen thu nhỏ, trọng số khởi tạo, adapter Q/V; không dùng QA thật. Đây là kiểm phần mềm, không tính vào quota QA hay số lần huấn luyện. Chưa có kết quả SFT, số đo VRAM Kaggle, resume GPU hoặc checkpoint đủ làm đầu vào D.4.
- Đã chạy các ô notebook cục bộ với ZIP chỉ chứa mã: không có release thì không train; sai hash thì dừng; CLI từ chối manifest `candidate_only` của lô 24. Với mô hình thu nhỏ và token số tự đặt, checkpoint khôi phục đúng trọng số adapter, trạng thái AdamW, RNG CPU và thứ tự trộn. Không suy rộng phép kiểm này thành resume QLoRA trên Kaggle.

## Kiểm định A–C theo đề gốc

- AI đọc đề ngày 12/11/2026 (tr. 1–2, 18–19), đối chiếu mã, notebook, sáu chứng minh LaTeX và các bài báo trong `references/`. Làm rõ trong ma trận đâu là công thức lấy từ bài báo và đâu là chứng minh tự dẫn xuất; không ghi sự rà soát của AI thành phê duyệt của nhóm hay giảng viên.
- Trên Python 3.12.0, PyTorch 2.15.0+cpu: 24 kiểm thử liên quan phần A đạt; chạy lại các ô tính C.1–C.4. Tính lại PPL từ NLL từng seed trong JSON Kaggle và so hash manifest A.2; năm file Python của pipeline trong ZIP khớp từng byte với mã được kiểm. Không huấn luyện lại hoặc mở checkpoint Kaggle.
- Kiểm độc lập bằng số: B.1 duyệt đủ 256 cặp vector dấu độc lập ở chiều 4, phương sai trước/sau chia tỷ lệ là 4/1; B.2 sai khác do hoán vị không mask dưới $5\times10^{-16}$, còn giữ mask nhân quả cố định cho phản ví dụ; B.3 kiểm dịch 3 vị trí trên 4 cặp sin/cos (sai số tối đa $6,44\times10^{-8}$ với bảng FP32); B.5 và B.6 đối chiếu đồng nhất thức KL trên phân phối hữu hạn. Đây là kiểm số bổ trợ, không thay chứng minh. C.1 vẫn dùng ma trận minh họa, không ghi là dữ liệu được giảng viên chấp thuận.
- C.4: phát hiện và sửa câu khẳng định nghiệm tối ưu luôn đổi theo β. Nếu reward hằng trên hỗ trợ của reference cho một prompt, chuẩn hóa triệt tiêu hệ số mũ chung và nghiệm vẫn là reference; bảng loss/gradient tại policy cố định không đổi.

## D.2 — chuẩn hóa thời điểm kiểm pilot

- Theo xác nhận của nhóm, AI đổi định dạng 24 giá trị `reviewed_at` sang ISO 8601 với `+07:00`, giữ nguyên ngày, giờ và phút. Nhóm thực hiện kiểm định và ghi quyết định; AI không chấm QA hoặc điền lý do. Lệnh `check` chấp nhận toàn bộ phiếu, chỉ còn thiếu biên bản chung của lô.
- AI chuẩn bị bản nháp biên bản chung của lô v2 từ manifest, phiếu và hồ sơ D.1; nêu riêng hai câu validation dùng chung đoạn B.4 của 1852 để nhóm rà theo ý nghĩa. Chạy `check` với bản nháp: đúng lô, chỉ còn chặn ở biên bản. Không ký thay người rà, không xác nhận quyền Kaggle, không phát hành hoặc huấn luyện.
- Sau khi nhóm cung cấp mã người chốt, thời điểm và lý do giữ hai câu, AI ghi lại quyết định vào biên bản riêng, không thay đổi phiếu. Chạy cổng D.2 trên hồ sơ thật: `pilot_sft_ready`. Kiểm đầu vào D.3 bằng `--check-only`: `release-valid` (18 train, 6 validation). Không tải dữ liệu lên Kaggle hoặc chạy SFT.
- D.3 pilot: sau khi nhóm cho phép `release-01` trên Kaggle Private, AI đóng gói riêng mã và ba tệp dữ liệu tối thiểu, điền hash manifest vào bản notebook bàn giao. Chạy các ô notebook với hai ZIP trên CPU (`release-valid`), kiểm offline token đáp án giải mã khớp cả trích dẫn cho 18 train và 6 validation; chuỗi dài nhất lần lượt 197 và 190 token ở giới hạn 512. Không upload, tải trọng số hay huấn luyện; chưa có số đo GPU hoặc kết quả resume.
- AI đọc hai log pilot Kaggle do nhóm gửi, đối chiếu epoch tốt nhất và PPL từ validation NLL, quy đổi số byte peak sang GiB; không huấn luyện, không nạp checkpoint và không xác nhận resume từ hai log này.
- AI đối chiếu nội dung run manifest do nhóm gửi với hash của manifest release, hai tệp Python đã đóng gói và chat template lưu tại máy nhóm. Bốn hash khớp; chưa có log resume.
- Nhóm chạy resume trên Kaggle và gửi nội dung `resumed_from.json` cùng dòng metrics epoch 2. AI đối chiếu với log lần chạy liên tục đã lưu; chỉ hai trường bộ nhớ đỉnh khác. AI không chạy GPU, mở trọng số hay thực hiện đánh giá độc lập trên người dùng.
- AI triển khai notebook hỏi thử riêng cho Kaggle (suy luận từ `best_adapter/`, không tái huấn luyện), viết hai câu minh họa, dùng lại prompt SFT và kiểm đường sinh trên CPU với Qwen2 thu nhỏ cùng adapter thử. Không dùng `USER_TEST`, không ghi đáp án mô hình thử thành kết quả pilot và chưa chạy adapter thật trên Kaggle.
- AI đọc ảnh hai đầu ra hỏi thử do nhóm gửi, đối chiếu câu thời hạn với đoạn chính văn 1852 đã lưu và nhận diện lỗi không từ chối câu ngoài phạm vi. Không chấm thay người đánh giá D.5 hoặc tạo cặp DPO.

## D.2 — mở rộng tập chính, lô b01

- AI soạn 57 QA train mới từ chính văn D.1, gồm cả câu cần từ chối hoặc nói rõ giới hạn nguồn; giữ nguyên 24 QA cũ và split. Với câu mới từ phụ lục 163 có lớp chữ lỗi, chỉ dùng các trang 285–288 đã đối chiếu bản hiển thị và yêu cầu người kiểm mở PDF. Không sử dụng khảo sát, câu visa demo hoặc dữ liệu trả lời của người dùng.
- AI chạy tạo ứng viên và đối chiếu hash, định vị đoạn nguồn, phân tách tài liệu train/validation, nhãn nháp và mẫu phân tầng. AI không điền quyết định người kiểm, không lập biên bản thay nhóm, không phát hành, upload hay huấn luyện. Các số 75 train và 6 validation là số ứng viên tích lũy, không phải số QA tập chính đã duyệt.
- B02: AI soạn 54 QA train (59 mệnh đề) từ chính văn 753/VBHN-BTP và phụ lục 858, 163, 1818; đối chiếu bản PDF hiển thị đối với các trang lỗi lớp chữ của phụ lục 163. AI dựng bộ ứng viên, so khớp CSV câu mới với JSONL và xác nhận 81 câu cũ giữ nguyên nội dung. Không sửa phiếu hoặc ghi nhận kiểm định người cho các câu mới.
- B03: AI soạn và biên tập 265 QA train bằng tiếng Việt từ chính văn 163, 858 và 753; thay mã mục nội bộ bằng tên thủ tục trong câu hỏi, gộp các điều kiện đi cùng nhau và phân biệt thời hạn thường với trường hợp phải xác minh. AI dùng CPU để định vị đoạn theo trang và hash, dựng 400 QA tích lũy, xuất hai CSV. Việc khớp nguồn tự động không chứng minh đáp án đúng về pháp lý hoặc thay kiểm thủ công. Không dùng dữ liệu khảo sát, điền phiếu người kiểm, đưa dữ liệu lên Kaggle hoặc huấn luyện.

## Rà Phần B và vá lỗ hổng B.3 — 26/11/2026

- Theo yêu cầu của Thế, AI rà lại từng bước sáu chứng minh B.1–B.6 và đối chiếu ký hiệu với `src/attention.py`, `src/lora.py`, `src/dpo.py`, `src/char_lm.py`. Kết luận: các phép toán đúng, không tìm thấy lỗi suy luận; `z_θ` của B.5 khớp `margin` trong A.4, quy tắc tổng hợp của B.6 khớp `validation_metrics`, bốn tiểu mệnh đề B.4 khớp `LoRALinear`.
- AI tìm được một lỗ hổng thật: B.3 phát biểu cho `PE(p) ∈ R^{2m}` (số chiều chẵn), nhưng `SinusoidalPositionEncoding` nhận `d_model` lẻ và khi đó tính chất `PE(p+Δ) = M_Δ PE(p)` không còn đúng ở toạ độ `sin` lẻ cặp. AI soạn phần bổ sung `\subsection*{Phạm vi: mệnh đề cần số chiều chẵn}` trong `docs/theory/part-b.tex`, gồm bổ đề độc lập tuyến tính (lập luận Vandermonde trên các nút `e^{iω_i}`) và suy luận bác bỏ. Đây là phần **thêm vào**, không sửa phần chứng minh đã có.
- Việc chuyển B từ "bản nháp" sang "đã duyệt" vẫn thuộc nhóm: AI không đổi `\fancyhead[R]{Bản nháp}`, không đổi dòng trạng thái ở đầu tài liệu, và không đổi sáu dòng B1–B6 trong ma trận yêu cầu. Thế và Hưng cần tự giải lại chứng minh rồi mới cập nhật trạng thái.

## Soạn báo cáo cuối kỳ, datasheet và model card — 26/11/2026

- Theo yêu cầu của Thế ("làm những việc bạn có thể làm"), AI soạn ba hiện vật G7 còn thiếu: `docs/report/report.tex` cùng mười tệp trong `docs/report/sections/`, `docs/data/datasheet.md`, và `docs/model/model-card.md`. AI cũng soạn phụ lục khai báo AI (G11) từ chính tệp này.
- Nội dung lấy từ hiện vật đã có trong kho mã. AI đối chiếu lại từng con số với notebook và tài liệu nguồn trước khi ghi: PPL 10,1948 ± 0,0628 và bảng 5 seed từ `char-corpus.md`; cấu hình A.2 (2 block, d_model 64, 4 head, d_ff 128, batch 16, AdamW lr 0,001); 33.472 tham số và 6.291.456 MAC từ notebook C.2, kiểm lại bằng tay theo `4d²+2df+9d+f` và `4nd²+2ndf+2n²d`; 544.768 / 1.089.536 / 2.179.072 và `P = 136.192r` từ notebook C.3; bộ ma trận C.1 seed `577893521` với bảng trọng số/đầu ra; `L = ln 3`, gradient `(−2/3, +2/3)` từ notebook C.4; năm họ thủ tục và hai mâu thuẫn nguồn (thời hạn trích lục 1818 so với 2163; phí chứng thực 226/2016/TT-BTC so với lệ phí hộ tịch NQ 98) từ `source-audit.md`; các số pilot D.2 từ `admin-pilot-report.json` và `docs/data/README.md`.
- AI chạy `python -m pytest -q` trên môi trường cục bộ và ghi đúng kết quả quan sát được: 30 test qua, 1 bỏ qua, 13 subtest qua, 8,38 giây; Python 3.14.3, PyTorch 2.12.1+cpu, `torch.cuda.is_available()` là `False`.
- Mọi hạng mục trong báo cáo mang nhãn `[đã thực hiện]`, `[một phần]` hoặc `[chưa thực hiện]` theo bằng chứng file. D.4 và D.5 ghi `[chưa thực hiện]`; D.2 ghi 24/2.000 QA và 0 QA được người duyệt; D.3 ghi chưa có lượt huấn luyện nào; yêu cầu G5 ghi chưa đóng. Các ô số đo của model card để trống với dấu `— chưa đo`.
- AI không tạo kết quả thực nghiệm mới, không đổi trạng thái hạng mục nào trong ma trận yêu cầu, không điền phiếu kiểm, không tạo nhãn ưu tiên, không chạy huấn luyện và không commit. Báo cáo mang nhãn `Bản nháp chưa nhóm duyệt` ở đầu trang cho tới khi nhóm xác nhận.
- Chưa xác minh loại tài khoản AI của nhóm; mỗi thành viên vẫn phải tự đọc, hiểu và bảo vệ được nội dung báo cáo khi vấn đáp.

## Dựng phiếu rà soát cho Thế — 26/11/2026

- Theo yêu cầu của Thế, AI dựng `docs/progress/review-log-the.md`: phiếu ghi lại việc rà soát theo quy ước nhóm, chia năm phần (chạy kiểm mã, đọc 4 file `src/`, tự giải lại B.1–B.6, đối chiếu một bài C, và các việc đang bị chặn). AI ghi phần "Việc cần làm", lệnh cần chạy và kết quả mong đợi của bộ kiểm.
- **Toàn bộ cột "Kết quả của Thế" và cột ngày để trống.** AI không điền kết quả rà soát, không ký thay, và không đổi trạng thái B1–B6 trong ma trận yêu cầu. Việc đổi trạng thái chỉ diễn ra sau khi Thế điền phiếu và báo nhóm.
- AI nêu trong phiếu rằng trước khi chấm cặp DPO, Thế phải đọc hướng dẫn chấm và xác nhận bằng văn bản chỉ nhận dữ liệu được phân quyền, không nhận phiếu đồng ý hay khảo sát thô.

## Cập nhật báo cáo theo commit 0f96676 — 28/11/2026

- Sau khi nhóm pull commit `0f96676` của Hà, AI đối chiếu lại báo cáo với trạng thái mới và sửa các số đã lạc hậu: D.2 từ 24 lên 400 QA ứng viên và 24 QA đã duyệt; D.3 từ "chưa huấn luyện" sang kết quả pilot thật (seed 41, validation NLL 1,509630 → 1,242314, PPL 4,525054 → 3,463617, peak allocated 2,402 GiB, resume tái lập đúng chỉ số, bốn SHA-256 khớp). Thêm mục ghi hai lỗi quan sát được khi hỏi thử adapter pilot. Cập nhật tương ứng datasheet và model card.
- AI sửa một khẳng định sai do chính AI viết trong bản nháp báo cáo mục C.4: trước đó ghi nghiệm tối ưu "cũng thay đổi" theo β mà không nêu điều kiện. Theo bản sửa của nhóm ở notebook 07, nghiệm chỉ thay đổi nếu reward không hằng trên hỗ trợ của reference; nếu `R(x,y)=c(x)` trên hỗ trợ đó thì `π* = π_ref` với mọi `β>0`. Báo cáo nay ghi cả tỷ số tối ưu và trường hợp ngoại lệ.
- Khi gộp `ai-use.md`, AI giữ nguyên toàn bộ mục của Hà và chỉ thêm ba mục của phiên trước vào sau; không ghi đè, không xóa dòng nào. Không commit, không push.
- Các số đo pilot đều là nội dung do nhóm cung cấp từ Kaggle; AI không chạy GPU, không mở checkpoint và không tạo kết quả mới.
