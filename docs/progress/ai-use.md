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
