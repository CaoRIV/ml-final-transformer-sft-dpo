# Model card — trợ lý hỏi đáp thủ tục hộ tịch và chứng thực tại Hà Nội

**Hiện vật bắt buộc theo đề** (phần II tr. 2: "model card cho mô hình D").
Cấu trúc theo *Model Cards for Model Reporting* (Mitchell và cộng sự).

> **Trạng thái: CÓ ADAPTER PILOT, CHƯA CÓ MÔ HÌNH CUỐI.**
> Đã chạy xong một lượt SFT pilot trên 24 QA đã duyệt, có adapter và số đo thật.
> Chưa chạy trên tập chính, chưa chọn cấu hình, chưa đủ 5 seed, và **chưa huấn
> luyện DPO**. Model card này ghi (a) những gì đã đo được, và (b) các ô còn trống,
> đánh dấu `— chưa đo`.
>
> Không điền số vào các ô đó trước khi có lượt huấn luyện và đánh giá thật.

Tài liệu liên quan: [datasheet](../data/datasheet.md) ·
[báo cáo cuối kỳ](../report/report.tex) · [hướng dẫn chấm](../data/annotation-guide.md) ·
[ma trận yêu cầu](../progress/requirements-matrix.md)

---

## 1. Chi tiết mô hình

### 1.1. Mô hình nền — **đã chốt**

| Thuộc tính | Giá trị |
|---|---|
| Tên | `Qwen/Qwen2.5-1.5B-Instruct` |
| Revision khóa | `989aa7980e4cf806f80c7fef2b1adb7bc71aa306` |
| Giấy phép | Apache-2.0 |
| Số tham số | ~1,54 tỷ (`1.543.714.304` phần tử, đối chiếu metadata safetensors) |
| Nằm trong khoảng đề yêu cầu (0,5–3B) | ✅ |
| Hỗ trợ tiếng Việt | ✅ |

**Kiến trúc:** 28 khối; chiều ẩn 1536; 12 đầu Q, 2 đầu K/V (grouped-query
attention), mỗi đầu 128 chiều; chiều trung gian FFN 8960; từ vựng 151.936;
`tie_word_embeddings=true`.

Hệ quả cho LoRA: trọng số Q là `1536 × 1536`, còn V là `256 × 1536`.

### 1.2. Phương pháp tinh chỉnh dự kiến

| Giai đoạn | Phương pháp | Trạng thái |
|---|---|---|
| SFT pilot (24 QA) | QLoRA NF4 double quant, FP16, adapter ở `q_proj` và `v_proj` | ✅ **đã chạy** |
| SFT tập chính (394 QA) | như trên | **chưa chạy** |
| Tối ưu ưu tiên | DPO, reference = checkpoint SFT cố định | **chưa huấn luyện** |

**Cấu hình pilot đã chạy:** `r=8`, `alpha=16`, dropout 0, learning rate `1e-4`,
batch 1, độ dài tối đa 512, 2 epoch, seed 41.

**Siêu tham số:** chọn trên **validation**, không dùng test. Hiện mới chạy **một**
cấu hình, nên chưa có việc chọn nào diễn ra — giá trị cuối `— chưa chọn`.

**Số tham số học theo rank** (đã kiểm bằng `src/lora.py` trên meta tensor):

| rank `r` | Q | V | Tổng | % so với mô hình nền |
|---:|---:|---:|---:|---:|
| 4 | 344.064 | 200.704 | **544.768** | 0,035% |
| 8 | 688.128 | 401.408 | **1.089.536** | 0,071% |
| 16 | 1.376.256 | 802.816 | **2.179.072** | 0,141% |

Công thức: `P = 28·(1536+1536)·r + 28·(1536+256)·r = 136.192·r`.

### 1.3. Người phát triển

Nhóm ba sinh viên: Cao Văn Hà (trưởng nhóm), Hà Mạnh Thế, Trần Duy Hưng. Bài tập
lớn môn Học máy cơ bản, Đề tài 9.

---

## 2. Mục đích sử dụng

### 2.1. Dùng cho

Trả lời câu hỏi tiếng Việt về **năm họ thủ tục** hộ tịch và chứng thực **tại Hà
Nội**:

| Họ thủ tục | Mã |
|---|---|
| Cấp bản sao trích lục hộ tịch / bản sao giấy khai sinh | `2.000635` |
| Chứng thực bản sao từ bản chính | `2.000815` |
| Chứng thực chữ ký | `2.000884` |
| Thay đổi, cải chính, bổ sung hộ tịch, xác định lại dân tộc | `1.004859` |
| Xác nhận thông tin hộ tịch | `2.002516` |

**Đầu vào:** một câu hỏi tiếng Việt do người dùng tự diễn đạt. Không giả định người
dùng biết tên thủ tục, số hiệu văn bản hay thuật ngữ hành chính.

**Đầu ra mong muốn:** đáp án nêu đúng thông tin **và điều kiện áp dụng**, kèm **dẫn
nguồn** (số hiệu văn bản, điều/mục, phiên bản) để người dùng kiểm tra. Nếu câu hỏi
ngoài phạm vi hoặc chưa đủ căn cứ trong dữ liệu, mô hình phải **nói rõ** thay vì
đoán.

### 2.2. **Không** dùng cho

- ❌ **Tư vấn pháp lý.** Giá trị pháp lý thuộc về văn bản gốc, không thuộc mô hình.
- ❌ Thủ tục ở tỉnh/thành khác, hoặc các họ thủ tục ngoài danh mục trên.
- ❌ Quyết định hành chính tự động, hoặc thay thế cán bộ tiếp nhận hồ sơ.
- ❌ Kết luận về quy định **hiện hành** khi nguồn còn mâu thuẫn chưa giải quyết (§5.1).
- ❌ Xử lý dữ liệu cá nhân của người dùng: mô hình không được dùng để tra cứu hồ sơ.

### 2.3. Người dùng dự kiến

Người dân cần tra cứu thủ tục trước khi đến nơi tiếp nhận. **Không** nhằm vào cán
bộ dùng cho quyết định nghiệp vụ.

---

## 3. Dữ liệu huấn luyện

Xem [datasheet](../data/datasheet.md) để biết đầy đủ. Tóm lại:

| Tập | Ngưỡng của đề | Hiện có |
|---|---:|---:|
| QA có trích dẫn | ≥ 2.000 | 24 ứng viên |
| Kiểm thủ công | ≥ 20% (≥ 400) | **0 đã duyệt** |
| `USER_TEST` (khảo sát người thật) | bắt buộc | **0** |
| Cặp ưu tiên DPO | ≥ 500, 2 người chấm độc lập | **0** |

Nguồn: **chính văn** quy phạm và văn bản hành chính công khai — nhóm nội dung không
thuộc phạm vi bảo hộ quyền tác giả theo khoản 2 Điều 15 Luật SHTT (VBHN 160/2026).
Trang tin, bài hướng dẫn và video chỉ dùng để **tìm** và đối chiếu văn bản, không
chuyển nguyên trạng vào tập train.

---

## 4. Đánh giá

### 4.1. Giao thức dự kiến (D.5)

Ba mốc model trên **cùng** tập test (`USER_TEST`), ba nhóm chỉ số:

| Chỉ số | Định nghĩa |
|---|---|
| Độ chính xác đối chiếu nguồn | Đáp án nêu đúng điều kiện áp dụng **và** dẫn đúng nguồn |
| Hallucination | Tỷ lệ phát biểu không có căn cứ trong nguồn đã dẫn |
| Từ chối đúng | Tỷ lệ từ chối đúng khi câu hỏi ngoài phạm vi hoặc chưa đủ căn cứ |

Kèm **blind human pairwise evaluation**: người đánh giá không biết đáp án thuộc
model nào, thứ tự trình bày được xáo; win rate báo cáo **kèm khoảng tin cậy**, ghi
rõ đơn vị lấy mẫu.

### 4.2. Kết quả

| Chỉ số | Base | SFT | SFT+DPO |
|---|---|---|---|
| Độ chính xác đối chiếu nguồn | — chưa đo | — chưa đo | — chưa đo |
| Hallucination | — chưa đo | — chưa đo | — chưa đo |
| Từ chối đúng khi ngoài phạm vi | — chưa đo | — chưa đo | — chưa đo |
| Win rate (blind pairwise) + CI | — chưa đo | — chưa đo | — chưa đo |

**Chưa có kết quả D.5 nào.** Tập test khảo sát chưa có, mốc SFT+DPO chưa tồn tại,
người đánh giá mù chưa được bố trí.

### 4.2b. Số đo đã có từ pilot SFT (không phải chỉ số D.5)

| Epoch | Validation NLL | Validation PPL |
|---:|---:|---:|
| 1 | 1,509630 | 4,525054 |
| 2 | **1,242314** | **3,463617** |

Seed 41, 2/2 epoch, 1.235 token train và 388 token validation mỗi epoch; epoch 2
được chọn theo validation NLL. ⚠️ Đây là perplexity trên 6 câu validation của lô
pilot — **không** phải độ chính xác, không phải chỉ số D.5, và không so được với
mô hình khác.

### 4.2c. Hỏi thử adapter pilot — hai lỗi quan sát được

| # | Lỗi |
|---|---|
| 1 | Trả "15/30 ngày làm việc" cho thủ tục xác nhận thông tin hộ tịch và tự nhận là mới nhất. Phụ lục 1852/QĐ-TTPVHCC B.4 tr. 3 ghi **dự kiến 03 ngày**, tối đa 10 ngày nếu phải xác minh |
| 2 | **Không từ chối câu ngoài phạm vi**: hỏi thị thực du lịch Nhật Bản, mô hình hướng dẫn thay vì nêu rõ ngoài phạm vi |

Cả hai đáp án chỉ ghi `[1]` không kèm nguồn truy xuất được.

Lỗi #2 đúng là hiện tượng giả thuyết ở §4.3 dự đoán. ⚠️ Hai câu, một adapter huấn
luyện trên 24 QA, không có người đánh giá mù → **quan sát định tính, không phải
phép đo**.

### 4.3. Giả thuyết của nhóm (chưa kiểm chứng)

DPO giúp nhiều nhất ở chỉ số **từ chối đúng**, vì "từ chối đúng cách" là thứ khó dạy
bằng SFT — dữ liệu SFT gồm các cặp câu hỏi–đáp án, nên nó dạy mô hình *luôn* trả
lời.

Đây là **giả thuyết**, không phải kết quả. Nhóm **không hứa DPO tốt hơn SFT** và sẽ
báo cả kết quả âm.

### 4.4. Chỉ số đã có cho mô hình khác (không liên quan tới trợ lý này)

Phần A.2 của bài tập có một mô hình ngôn ngữ **ký tự** tự cài đặt, huấn luyện trên
*Truyện Kiều* bản Trương Vĩnh Ký 1911: **PPL validation 10,1948 ± 0,0628** (trung
bình ± SD mẫu, 5 seed độc lập).

⚠️ Đây là mô hình khác, dữ liệu khác, mục đích khác (chứng minh cài đặt Transformer
đúng). **Không** phải chỉ số của trợ lý thủ tục.

---

## 5. Giới hạn và rủi ro

### 5.1. Nguồn còn mâu thuẫn — rủi ro cao nhất

1. **Thời hạn cấp trích lục `2.000635`.** QĐ 1818/QĐ-TTPVHCC (hiệu lực 01/01/2026)
   ghi dự kiến 3 ngày làm việc, tối đa 10 ngày nếu xác minh. QĐ 2163/QĐ-BTP
   (30/09/2026) ghi trong ngày tiếp nhận, hoặc ngày làm việc kế tiếp nếu sau 15
   giờ. Chưa tìm được văn bản triển khai 2163 tại Hà Nội, cũng chưa có văn bản xác
   nhận 1818 bị thay thế.
   → **Mô hình không được trả lời "3 ngày" như quy định hiện hành.**
2. **Lệ phí.** Thông tư 226/2016/TT-BTC là căn cứ phí **chứng thực**; biểu lệ phí
   **hộ tịch** Hà Nội hiện hành ở NQ 98/2026/NQ-HĐND. Trộn hai khái niệm tạo đáp án
   sai khó phát hiện.

### 5.2. Kiến thức đóng băng

Mô hình tinh chỉnh ghi kiến thức vào **trọng số** tại thời điểm huấn luyện và
**không tự biết** khi văn bản thay đổi. Giảm nhẹ trong phạm vi hiện tại:

- Buộc đáp án dẫn số hiệu **và phiên bản** văn bản.
- Soạn QA gắn với **từng văn bản và phạm vi của nó**, thay vì phát biểu "hiện hành".
- Dạy mô hình từ chối khi chưa đủ căn cứ.

Hướng mở rộng đúng cho vấn đề này là **truy xuất tăng cường (RAG)** — Đề tài 11
trong danh mục của đề. Nhóm **chỉ thảo luận**, không triển khai; RAG ngoài phạm vi
Đề tài 9.

### 5.3. Giới hạn kỹ thuật

| Hạng mục | Trạng thái |
|---|---|
| Peak VRAM cho SFT pilot | ✅ **đã đo**: allocated 2,402 GiB, reserved 2,725 GiB (Tesla T4, cấu hình §1.2). Là số của tiến trình, không phải tổng VRAM thiết bị |
| Peak VRAM cho SFT tập chính | **chưa đo** (394 QA, chuỗi dài hơn) |
| Peak VRAM cho DPO | **chưa đo.** DPO cần giữ thêm reference policy |
| Resume trên GPU thật | ✅ **đã kiểm**: resume từ `epoch-0001` tái lập đúng NLL/PPL epoch 2; chỉ hai trường peak VRAM lệch |
| Độ dài ngữ cảnh | 512 token ở pilot; chuỗi dài nhất 197 (train) và 190 (validation) |
| Thông lượng suy luận | **chưa đo** |

⚠️ **Không** suy từ ước lượng C.3 rằng một GPU cụ thể chạy vừa SFT hay DPO.

### 5.4. Thiên lệch

- **Phạm vi địa lý:** chỉ Hà Nội. Không suy rộng.
- **Cách diễn đạt:** `USER_TEST` dự kiến thu từ sinh viên và người thân — một mẫu
  hẹp về tuổi và mức quen thuộc với thủ tục hành chính. Hiệu năng với nhóm người
  dùng khác **chưa đo**.
- **Nhãn ưu tiên:** chỉ hai người chấm, cùng là thành viên nhóm. Mức đồng thuận
  phải được **đo và báo cáo**, không giả định.

---

## 6. Môi trường và tái lập

| | |
|---|---|
| Môi trường CPU cục bộ (kiểm phần mềm) | Python 3.14.3, PyTorch 2.12.1+cpu, CUDA không khả dụng |
| Môi trường GPU đã dùng (pilot D.3) | Tesla T4, Python 3.13.16, torch 2.11.0+cu130, CUDA 13.0; `transformers==4.57.6`, `peft==0.18.0`, `accelerate==1.12.0`, `bitsandbytes==0.48.2` |
| Seed | 41 (pilot). Các seed còn lại **chưa chạy** |
| Số lần chạy độc lập | ≥ 5 theo yêu cầu đề — hiện **1 seed**; resume không tính là seed thứ hai |
| Toàn vẹn hiện vật | 4 SHA-256 khớp: manifest release-01, hai tệp Python trong ZIP mã, chat template tokenizer |

**Đã kiểm trên CPU (không phải kết quả huấn luyện):** 7 test bộ nạp/mask qua; với
một câu minh họa dùng tokenizer Qwen đúng revision: 71 token prompt bị che, giải mã
19 token đích khớp nguyên đáp án có dấu và trích dẫn, đúng một EOS; forward trên
Qwen thu nhỏ với trọng số khởi tạo và adapter Q/V chạy được.

**Cổng an toàn đã kiểm:** ZIP chỉ chứa mã thì không train; sai hash thì dừng; CLI
từ chối manifest `candidate_only` của lô 24 QA. Quy trình **không thể** vô tình
huấn luyện trên dữ liệu chưa duyệt.

---

## 7. Cân nhắc đạo đức

- **Dữ liệu người:** cần văn bản đồng ý; ẩn danh trước khi lưu; phiếu đồng ý định
  danh để riêng, không vào Git. Xem [privacy-workflow.md](../data/privacy-workflow.md).
- **Phân quyền:** người chấm nhãn DPO **không** nhận consent, khảo sát thô, hay
  `USER_TEST` trước khi giao thức đánh giá cho phép.
- **Không bịa:** không tạo nhãn người chấm, mức đồng thuận, khảo sát hay kết quả
  huấn luyện bằng AI.
- **Khai báo AI:** phạm vi hỗ trợ AI ghi tại
  [docs/progress/ai-use.md](../progress/ai-use.md) và phụ lục báo cáo.
- **Không phân phối** checkpoint hay mô hình nền trong Git.

---

## 8. Hạng mục phải hoàn thành trước khi model card này có hiệu lực

| # | Hạng mục | Chặn bởi |
|---|---|---|
| 1 | Phát hành ≥ 2.000 QA, ≥ 20% kiểm thủ công | người kiểm thật |
| 2 | Thu `USER_TEST` từ khảo sát người thật có consent | người tham gia thật |
| 3 | Chạy SFT, đo VRAM, kiểm resume GPU, chọn adapter theo validation | hạng mục 1 |
| 4 | Thu ≥ 500 cặp ưu tiên, 2 người chấm độc lập, đo đồng thuận | hạng mục 3 |
| 5 | Huấn luyện DPO, chọn `beta` trên validation DPO | hạng mục 4 |
| 6 | Đánh giá ba mốc + blind pairwise + CI | hạng mục 2, 5 |
| 7 | Đối chiếu `src/dpo.py` (A.4) trên minibatch ưu tiên **thật** (yêu cầu G5) | hạng mục 4 |

Hạng mục 1, 2, 4, 6 cần **người thật** và không nén được bằng công sức của mã.
