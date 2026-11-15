# Đề cương bản nháp — Đề tài 9: Transformer, SFT và DPO cho trợ lý hỏi đáp thủ tục hành chính công

> **Trạng thái:** bản nháp tuần 1 để chốt phạm vi, dữ liệu và phân công. Những nội dung ghi “đề xuất” chưa phải dữ liệu đã thu thập, thí nghiệm đã chạy hay quyết định cuối cùng. Mục tiêu dàn trang nội bộ là khoảng 5–7 trang cho đề cương này và 3–5 trang cho `data-plan.md`; tài liệu Markdown hiện chưa được dàn trang nên không tuyên bố đã đạt độ dài đó.
>
> **Căn cứ đề bài:** Đề tài 9 yêu cầu cài đặt Transformer, LoRA và hàm mất mát DPO; huấn luyện mô hình ký tự nhỏ; sau đó xây dựng trợ lý hỏi đáp thủ tục hành chính với tối thiểu 2.000 cặp chỉ dẫn có trích dẫn, ít nhất 500 cặp ưu tiên và đánh giá mô hình gốc/SFT/SFT+DPO. Phần D có tỷ trọng 30/100; đề bài cũng yêu cầu kết quả trung bình ± độ lệch chuẩn trên ít nhất 5 lần chạy hoặc 5 phần gập, và quản lý phiên bản nguồn thủ tục.

## 1. Mục tiêu, phạm vi và người dùng

### 1.1. Vấn đề và mục tiêu

Nhóm xây dựng và đánh giá một **trợ lý hỏi đáp bằng tiếng Việt về thủ tục hành chính công trong phạm vi được chốt**, nhằm trả lời có căn cứ cho các câu hỏi thường gặp như thành phần hồ sơ, trình tự, thời hạn, lệ phí và căn cứ pháp lý. Câu trả lời được kỳ vọng nêu rõ trích dẫn tới đoạn nguồn đã lưu; khi câu hỏi nằm ngoài phạm vi dữ liệu hoặc không đủ căn cứ, hệ thống phải từ chối hoặc nêu giới hạn thay vì tự suy đoán.

Mục tiêu học thuật là nối liền bốn phần bắt buộc của Đề tài 9:

- **A — phát triển phương pháp:** tự cài đặt khối Transformer giải mã và các thành phần được yêu cầu; tự cài đặt LoRA và mất mát DPO.
- **B — lý thuyết:** trình bày các chứng minh về attention, mã hóa vị trí, LoRA, DPO và cross-entropy/PPL theo đề bài.
- **C — bài tập và kiểm chứng:** giải các bài tính attention, độ phức tạp, LoRA/QLoRA và giá trị–gradient DPO; kiểm chứng số học các kết quả liên quan.
- **D — ứng dụng:** tạo bộ dữ liệu có nguồn gốc rõ ràng, SFT một mô hình nguồn mở phù hợp tiếng Việt và tiếp tục tối ưu DPO từ dữ liệu ưu tiên do người đánh giá lập.
Phần B sẽ liệt kê và chứng minh đầy đủ sáu mệnh đề của đề bài: (B.1) phương sai $q^\top k$ và hệ số $1/\sqrt{d_k}$; (B.2) đẳng biến hoán vị khi không có mã hóa vị trí; (B.3) ma trận quay khối cho mã hóa hình sin; (B.4) bốn tính chất LoRA; (B.5) nghiệm tối ưu DPO có chính quy KL từ Bradley–Terry; và (B.6) tương đương giữa tối thiểu cross-entropy kỳ vọng và KL, cùng liên hệ PPL. Phần A xác định rõ causal mask gán logit token tương lai giá trị $-\infty$ trước softmax. Khi chứng minh B.5, báo cáo phải nêu các giả thiết như $\beta>0$, hỗ trợ của $\pi_{ref}$ bao phủ các đáp án đang xét và hằng số chuẩn hóa $Z(x)$ hữu hạn/dương; không dùng công thức ngoài các điều kiện đó. Bài C.4 sẽ tính giá trị **và gradient** DPO từ log-xác suất chính sách/tham chiếu cho `chosen` và `rejected`, rồi phân tích ảnh hưởng của $\beta$.

Với B.2, chứng minh trước cho attention không mask; nếu có mask $M$, phải đồng thời biến đổi thành $PMP^\top$. Giữ nguyên causal mask nói chung không bảo toàn đẳng biến với mọi hoán vị. Mọi chứng minh phải nêu kích thước tensor, tính độc lập cần thiết và dùng log tự nhiên.

Mục tiêu đánh giá nội bộ có thể hướng tới mức 85–90/100, nhưng đây **không phải cam kết điểm số**. Điểm chỉ có thể được xác định bởi hội đồng sau khi xem toàn bộ chứng minh, mã nguồn, dữ liệu, tính tái lập và bảo vệ.

### 1.2. Phạm vi có chủ ý hẹp

Phạm vi địa phương, nhóm thủ tục và tập văn bản chính thức **chưa chốt**. Trước khi thu thập, nhóm sẽ chọn một địa phương/cơ quan và một số nhóm thủ tục mà nhóm có thể truy vết văn bản công khai, phiên bản và ngày hiệu lực. Thiết kế ban đầu có thể dùng mẫu **5–10 thủ tục và 20–50 câu hỏi–đáp** để thử quy trình, nhưng đây chỉ là đề xuất thăm dò, chưa phải dữ liệu tồn tại hay một phạm vi đã được phê duyệt.

Trong phạm vi đã chọn, sản phẩm tập trung vào hỏi đáp một lượt có trích dẫn, dựa trên mô tả thủ tục và văn bản/cổng công khai được phép sử dụng. Sản phẩm không thay thế tư vấn pháp lý, không đưa ra quyết định hành chính, không xử lý hồ sơ thật và không yêu cầu người dùng cung cấp dữ liệu cá nhân.

Ngoài phạm vi của đề cương này:

- Không triển khai RAG; RAG chỉ được nhắc như hướng mở rộng mà đề bài đã gợi ý cho Đề tài 11.
- Không triển khai PPO hoặc bất kỳ vòng học tăng cường trực tuyến nào; nhánh ưu tiên dùng DPO ngoại tuyến theo đề bài.
- Không khẳng định cập nhật tri thức thời gian thực. Mỗi câu trả lời phải mang theo căn cứ/phiên bản nguồn đã biết; thủ tục thay đổi cần thu thập lại và gán phiên bản mới.

### 1.3. Người dùng và tình huống sử dụng

Người dùng mục tiêu là người dân hoặc sinh viên cần **định hướng ban đầu** về một thủ tục trong phạm vi được công bố. Họ có thể hỏi “cần những giấy tờ gì?”, “nộp theo các bước nào?”, “thời hạn/chi phí là bao lâu?” hoặc “căn cứ nào nói điều này?”. Trợ lý phải ưu tiên câu trả lời ngắn, dễ kiểm tra và liên kết/trích đoạn nguồn hơn là giọng điệu tự tin.

Người dùng không nên dùng hệ thống cho tình huống khẩn cấp, tranh chấp, trường hợp cá nhân có ngoại lệ hoặc thủ tục ngoài nhóm đã công bố. Với các trường hợp đó, mẫu trả lời cần chỉ ra rằng người dùng phải kiểm tra cổng/cơ quan có thẩm quyền. Việc khảo sát người dùng thật để lập tập test chỉ diễn ra khi có văn bản đồng ý, có thể rút lại theo quy trình khảo sát, và dữ liệu được ẩn danh trước khi lưu.

## 2. Kiến trúc công việc: hai nhánh và cầu nối A–D

### 2.1. Nhánh 1 — nền tảng tự cài đặt cho Phần A–C

Nhánh này phục vụ yêu cầu “từ đầu”, không dùng mô-đun attention dựng sẵn cho phần cài đặt cốt lõi. Các thành phần dự kiến gồm: scaled dot-product attention, multi-head attention, causal mask, positional encoding hình sin và một block Transformer decoder bằng PyTorch; mô hình ngôn ngữ mức ký tự nhỏ; lớp LoRA bao quanh linear layer với cơ chế hợp nhất trọng số khi suy luận; và hàm mất mát DPO.

Mô hình ký tự nhỏ chỉ dùng văn bản tiếng Việt thuộc phạm vi công cộng hoặc giấy phép mở đã được kiểm tra. Nhóm sẽ tách train/validation riêng và báo cáo PPL validation. Đây là bài kiểm chứng kiến trúc/phương pháp, không phải mô hình trợ lý Phần D và không được dùng văn bản hành chính chưa có quyền sử dụng.

Cần kiểm chứng từng hạng mục có thể quan sát được: causal mask không lộ token tương lai; shape/head của attention đúng; tham số LoRA trainable bằng $r(d+k)$; hợp nhất LoRA bảo toàn đầu ra trong sai số số học; hàm DPO có dấu và gradient nhất quán với công thức. Các bài C.1–C.4, gồm C.4 về giá trị–gradient DPO và ảnh hưởng của $\beta$, sẽ được giải và dùng làm phép kiểm tra độc lập, không thay cho đánh giá ứng dụng.

### 2.2. Nhánh 2 — ứng dụng SFT rồi DPO cho Phần D

Nhánh ứng dụng bắt đầu từ dữ liệu chỉ dẫn có trích dẫn và một mô hình nền mã nguồn mở hỗ trợ tiếng Việt. Quy trình dự kiến: khóa phiên bản nguồn và chia dữ liệu; SFT; sinh hai ứng viên trả lời từ checkpoint SFT cho mỗi prompt; hai người đánh giá độc lập chọn câu trả lời tốt hơn theo rubric; phân xử bất đồng; sau đó DPO với checkpoint SFT đóng băng làm mô hình tham chiếu.

**Qwen2.5-1.5B-Instruct** là một ứng viên, không phải lựa chọn cuối cùng. Lựa chọn mô hình sẽ phụ thuộc giấy phép dùng cho nghiên cứu, khả năng tiếng Việt, tokenizer, khả năng nạp với QLoRA và kết quả pilot. Thông tin từ phiên Colab trước do người dùng báo là T4 15.360 MiB, `torch 2.14.1+cu130`, CUDA 13 hoạt động; nhóm chưa tự đo các thông số này. Vì vậy không coi đó là bảo đảm đủ VRAM: cần pilot SFT và pilot DPO riêng, với tham chiếu DPO được nạp/điều phối theo cách tương thích bộ nhớ. Checkpoint, manifest và trạng thái resume có thể lưu Drive nếu quyền/lưu lượng cho phép; điều này là thiết kế cần kiểm tra, không phải cam kết không gián đoạn.

SFT pilot phải xuất hiện sớm cuối tuần 1 hoặc đầu tuần 2 để có checkpoint tạo ứng viên cho dữ liệu DPO. Không được giả định đã có 500 cặp ưu tiên trước khi hai người chấm hoàn tất quy trình. Mục tiêu bảo thủ để khóa kế hoạch là đủ **2.000 QA train** và **500 preference pairs train**, cộng validation riêng; con số thực chỉ được báo sau khi thu thập, kiểm tra và phân chia.

### 2.3. Cầu nối bắt buộc từ A sang D

Cầu nối không dừng ở việc đặt hai nhánh cạnh nhau. Trên **minibatch thật của dữ liệu Phần D**, nhóm sẽ dùng cùng prompt, `chosen`, `rejected`, attention mask và token mask trả lời để tính log-xác suất chuỗi dưới mô hình chính sách và mô hình tham chiếu. Với vanilla DPO, log-xác suất mỗi đáp án là **tổng** log-prob các token thuộc phần trả lời đã mask, không phải trung bình theo token như phép tính PPL; loss là trung bình các loss ví dụ theo batch. Hàm tự cài đặt phải tính:

$$
L_{DPO}=-\frac{1}{B}\sum_i\log\sigma\left(\beta\left[(\log\pi_\theta(y_w|x)-\log\pi_{ref}(y_w|x))-(\log\pi_\theta(y_l|x)-\log\pi_{ref}(y_l|x))\right]\right).
$$

Đối chiếu với thư viện DPO được phép dùng ở Phần D sẽ ghi lại: tổng log-prob `chosen`/`rejected` cho từng ví dụ, reward margin/loss theo minibatch, masking, reduction và gradient. Với cùng minibatch và trạng thái tham số ban đầu, đối chiếu gradient autograd theo logit có mask hoặc tham số adapter có thể so sánh được; không chỉ so scalar loss. Đầu vào phải là log-prob thực từ forward pass, **không** là số ngẫu nhiên hay ví dụ làm sẵn. Sai khác chỉ được kết luận sau khi cố định tokenizer, padding, truncation, prompt template, dấu margin, token mask, cách tổng token trả lời và batch reduction. Kết quả đối chiếu là bằng chứng rằng thành phần A tham gia trực tiếp vào pipeline D, như yêu cầu chung của đề bài.

Trong pipeline D, LoRA tự cài đặt có thể được dùng làm phép kiểm tra trên linear toy/mini-model; việc fine-tune quy mô Phần D có thể dùng thư viện chuẩn theo quy định Phần D. Nếu hai cách không thể so sánh cùng kiến trúc/tokenizer, báo cáo phải nói rõ giới hạn thay vì suy diễn tương đương.

## 3. Dữ liệu, chất lượng và đạo đức

Kế hoạch vận hành chi tiết nằm trong [data-plan.md](data-plan.md). Tóm tắt các yêu cầu không được lược bỏ:

1. **Nguồn thủ tục:** chỉ thu thập trang/tệp công khai mà việc sử dụng được phép, tuân thủ điều khoản, robots.txt và giới hạn tần suất. Với mỗi đoạn, lưu URL/cơ quan, thời điểm truy xuất, phiên bản/ngày hiệu lực khi có, giấy phép/điều khoản đã kiểm tra và span nguồn có thể trích lại. Không suy diễn nguồn hành chính trước khi địa phương và nhóm thủ tục được chốt.
2. **SFT:** đề bài yêu cầu ít nhất 2.000 cặp QA có citation và kiểm định thủ công ít nhất 20%. Citation phải trỏ tới span nguồn được lưu, không chỉ tới tên website. Train, validation và test tách theo nhóm thủ tục/nguồn để giảm rò rỉ gần trùng lặp.
3. **DPO:** đề bài yêu cầu tối thiểu 500 cặp so sánh, mỗi cặp là hai câu trả lời SFT cho cùng prompt do ít nhất hai người đánh giá độc lập. Rubric gồm đúng nội dung, đầy đủ, trích dẫn đúng và từ chối đúng phạm vi. Cặp bất đồng được phân xử sau khi đã lưu nhãn độc lập; báo cáo tỷ lệ đồng thuận và cách phân xử.
4. **Test người dùng:** câu hỏi khảo sát thật phải tách hoàn toàn với train/validation, thu thập có consent bằng văn bản và ẩn danh trước khi lưu. Nếu chưa có quyền tiếp cận người khảo sát, không được gọi tập test là “câu hỏi thật”; phải ghi rõ là thiếu điều kiện.

Các nguồn, dữ liệu, phiên bản và hướng dẫn gán nhãn cần được đóng gói thành datasheet; mô hình cuối cùng cần model card. Cả hai là sản phẩm nộp được yêu cầu, không chỉ là ghi chú nội bộ.

## 4. Huấn luyện, chọn siêu tham số và đánh giá

### 4.1. Lựa chọn và thí nghiệm có kiểm soát

Mô hình nền chỉ được chốt sau khi kiểm tra giấy phép và pilot SFT. Các cấu hình LoRA/QLoRA, hạng $r$, $\alpha$, learning rate, số epoch, độ dài chuỗi, batch/gradient accumulation, $\beta$ DPO và giải mã sẽ được ghi bằng manifest. Không khóa giá trị số chỉ vì chúng phổ biến: siêu tham số chỉ được chọn trên validation theo quy định đề bài; test chỉ dùng cho báo cáo cuối.

DPO dùng checkpoint SFT đã chọn làm `ref`, đóng băng trong một run. Với seed $s$, thiết kế run ghép là `SFT_s → DPO_s`, trong đó `ref = SFT_s`; preference dataset, split, rubric và candidate đã phân xử được khóa chung từ pilot trước khi chạy 5 seed, nên không đòi hỏi gán nhãn lại 500 cặp cho mỗi seed. Nhóm cần lưu fingerprint checkpoint, tokenizer, prompt template và split dữ liệu để các run sau tái lập đúng cặp so sánh. Dữ liệu validation DPO tách riêng khỏi 500 cặp train đề xuất; không tối ưu $\beta$ trên test.

Nếu ngân sách GPU không đủ cho 5 run độc lập của cấu hình cuối, nhóm sẽ xin điều chỉnh **với giảng viên** và ghi rõ tác động; thỏa thuận nội bộ của nhóm không thay thế điều chỉnh đó. **Không** âm thầm giảm số run. Năm lần sinh câu trả lời từ cùng checkpoint không phải năm run; chúng chỉ đo biến thiên decoding nếu thiết kế có chủ đích.

### 4.2. So sánh và chỉ số

So sánh tối thiểu là mô hình gốc, SFT và SFT+DPO, trên cùng tập test khóa và prompt template tương ứng. Đánh giá câu trả lời gồm:

- độ chính xác thông tin khi đối chiếu span nguồn;
- tính đầy đủ với yêu cầu trong câu hỏi;
- tỷ lệ citation đúng (citation có thật và hỗ trợ đúng mệnh đề);
- tỷ lệ ảo giác/khẳng định không có căn cứ;
- tỷ lệ từ chối đúng cho câu hỏi ngoài phạm vi hoặc thiếu căn cứ;
- đánh giá mù theo cặp của người chấm, tỷ lệ thắng và khoảng tin cậy.

Các run SFT/DPO độc lập dùng 5 seed ghép như trên; đơn vị tổng hợp là run, báo cáo mean và **sample standard deviation** ($n-1$), không nhân bản mỗi prompt hay mỗi generation thành run. Baseline mô hình gốc được khóa theo một checkpoint/config cố định và không được gán sample SD bằng cách lặp suy luận/nhân bản output; nếu có ngẫu nhiên decoding phải báo giao thức riêng, không gọi đó là biến thiên huấn luyện. Khoảng tin cậy của đánh giá mù phải bootstrap theo **đơn vị câu hỏi**; nếu khảo sát có nhiều câu từ cùng người, bootstrap theo **cụm người khảo sát**. Không xem các quan sát seed × prompt là độc lập để làm CI hẹp giả tạo. Số câu có chấm, số cụm, cách bootstrap và seed phải được báo cáo.

Không có số liệu nào trong đề cương này là kết quả. Chỉ sau khi test được khóa, chấm mù và lưu biểu mẫu mới được báo cáo chỉ số/CI.

## 5. Phân công tạm thời cho 3 người

Tên thành viên chưa được cung cấp; dưới đây là vai trò tạm, phải thay bằng tên và người chịu trách nhiệm cụ thể trước khi nộp.

| Vai trò tạm | Trách nhiệm chính | Điểm giao nhận |
|---|---|---|
| Thành viên 1 — phương pháp | A: Transformer ký tự, LoRA, DPO custom; kiểm chứng C; đối chiếu loss/gradient minibatch thật với thư viện | API/kiểm thử đơn vị, notebook kiểm chứng, bảng sai khác log-prob/loss/gradient |
| Thành viên 2 — dữ liệu | sổ nguồn, ingest/phiên bản/span, QA SFT, split và khử gần trùng; điều phối consent/ẩn danh và hai nhãn preference | manifest dữ liệu, datasheet, mẫu citation đã kiểm, split khóa, nhãn thô + phân xử |
| Thành viên 3 — lý thuyết, báo cáo & đánh giá | B.1–B.6 và tích hợp báo cáo; pilot SFT/DPO, manifest run, chấm mù, thống kê và model card | bản chứng minh có giả thiết, báo cáo tích hợp, checkpoint/seed record, bảng baseline/SFT/DPO |

Mọi thành viên phải hiểu phần mình bảo vệ và có thể bị vấn đáp về **bất kỳ** đoạn mã hoặc chứng minh nào, không chỉ phần được phân công. Hai người chấm preference có thể là thành viên trong nhóm hoặc người đủ điều kiện khác, nhưng danh tính/vai trò, tính độc lập khi chấm và xung đột lợi ích phải được chốt trước. Không mặc định “hai người” đã sẵn có.

## 6. Tiến độ và mốc bàn giao

| Thời điểm | Công việc cần hoàn thành | Bằng chứng cần lưu |
|---|---|---|
| Tuần 1, đầu–giữa tuần | Chốt địa phương, nhóm thủ tục, quyền dùng nguồn; thiết kế schema/rubric/split; khởi tạo mô hình ký tự và DPO custom | đề cương, data plan, sổ nguồn, mẫu record, quyết định phạm vi |
| Tuần 1, cuối tuần | Thu thập/chuẩn hóa pilot hợp lệ; kiểm citation trên mẫu; SFT pilot sớm nếu dữ liệu tối thiểu sẵn sàng | dữ liệu pilot có provenance, log kiểm tra, checkpoint pilot hoặc ghi rõ blocker |
| Tuần 2, đầu | Hoàn thành hoặc tiến gần ngưỡng dữ liệu D theo tiến độ thực; dùng checkpoint SFT để tạo ứng viên DPO; chấm độc lập và phân xử | version dataset, nhãn thô + quyết định phân xử, agreement |
| Tuần 2, theo mốc đề bài | Hoàn thành Phần A, B và bộ dữ liệu Phần D theo yêu cầu báo cáo tiến độ | mã/phân tích A–C, datasheet, số lượng đã kiểm chứng (không suy diễn) |
| Tuần 3 | Run cuối theo ngân sách đã chấp thuận, chấm mù/test, báo cáo/model card/tái lập và chuẩn bị bảo vệ | manifest run, kết quả + CI, model card, repository/tập lệnh |

Các mốc phản ánh quy định đề bài: tuần 1 nộp đề cương và kế hoạch dữ liệu, tuần 2 báo cáo tiến độ với A/B/dữ liệu D, tuần 3 nộp và bảo vệ. Tuy nhiên phần cấu trúc chung cũng mô tả nhóm 3 sinh viên thực hiện trong “2 tuần”, nên mốc tuần 3 tạo mâu thuẫn lịch trong chính đề bài. Kế hoạch này không tự coi tuần 3 là gia hạn: nhóm phải xác nhận với giảng viên mốc áp dụng và báo cáo trung thực phần nào chưa hoàn thành.

## 7. Rủi ro, giảm thiểu và quyết định cần chốt

| Rủi ro | Tác động | Giảm thiểu/kích hoạt quyết định |
|---|---|---|
| Phạm vi nguồn quá rộng hoặc văn bản thay đổi | Citation lỗi thời, khối lượng không kiểm soát | Chốt phạm vi hẹp; lưu version/effective date/span; không trộn phiên bản không xác định |
| Không đủ quyền/điều khoản thu thập | Không thể dùng nguồn hoặc khảo sát | Kiểm tra trước ingest; tuân thủ robots/rate limit; dừng nguồn không rõ quyền; không thu người dùng khi thiếu consent |
| 2.000 QA/500 cặp không kịp kiểm chất lượng | Không đạt yêu cầu dữ liệu hoặc nhãn yếu | Pilot pipeline sớm, kiểm thủ công theo tỷ lệ, tách validation; báo cáo count thực, không bịa đủ ngưỡng |
| Thiếu hai người chấm độc lập hoặc người khảo sát | Preference/test không đúng thiết kế | Chốt người chấm và khả năng khảo sát ngay tuần 1; nếu không có consent/người dùng, ghi rõ không có test người dùng thật thay vì gán nhãn giả |
| T4/QLoRA hết bộ nhớ hoặc run gián đoạn | Không chạy được SFT/DPO đáng tin cậy | Pilot SFT rồi DPO với ref riêng; giảm cấu hình sau validation/pilot có log; lưu checkpoint/manifest để resume khi hạ tầng cho phép |
| 5 run vượt ngân sách | Không đáp ứng báo cáo tái lập | Dự trù 5 seed ngay từ thiết kế; nếu không đủ, xin điều chỉnh với giảng viên và ghi rõ, không đổi âm thầm hay chỉ dựa vào đồng thuận nội bộ |
| Rò rỉ split/gần trùng | Test quá lạc quan | Nhóm theo thủ tục/nguồn, lọc exact/near duplicate và audit citation trước khóa test |

Tối thiểu cần chốt ngay: **(1)** địa phương/cơ quan và nhóm thủ tục; **(2)** khả năng tiếp cận người khảo sát với consent để tạo test thật; **(3)** hai người sẽ chấm preference độc lập. Đồng thời cần xác nhận quyền dùng nguồn cụ thể và mô hình nền sau pilot. Không chốt các điểm này, nhóm không nên tuyên bố đã có dữ liệu hành chính, phạm vi hộ gia đình hay benchmark hoàn chỉnh.

## 8. Tài nguyên và sản phẩm dự kiến

Đề bài khuyến nghị GPU từ 16 GB cho Đề tài 9. Cấu hình T4 nêu ở trên là thông tin báo cáo từ phiên Colab trước và gần ngưỡng này, nên được xem là điều kiện cần pilot chứ không phải năng lực đã xác nhận. Tài nguyên lưu trữ cần chứa bản nguồn hợp lệ, dữ liệu đã ẩn danh, manifest/checkpoint và log; quyền Drive, dung lượng, giữ phiên và chính sách resume vẫn chưa chốt.

Sản phẩm cuối theo đề bài dự kiến gồm báo cáo LaTeX 25–40 trang, repository Git có mô tả môi trường và script tái lập, dữ liệu hoặc script thu thập kèm datasheet và model card. Đề cương này không tuyên bố các sản phẩm đó đã tồn tại.

## 9. Tài liệu căn cứ

1. TS. Phạm Văn Khánh, *Danh mục 20 bài tập lớn: Học máy cơ bản, mô hình ngôn ngữ lớn, học tăng cường và tích hợp*, ngày 12/11/2026: Phần I–II (tr. 1–2) và Đề tài 9 (tr. 18–19).
2. Các URL/văn bản hành chính cụ thể sẽ chỉ được thêm vào sổ nguồn sau khi chốt địa phương, nhóm thủ tục và kiểm tra điều kiện sử dụng; đề cương không giả định hay dựng sẵn các nguồn này.
