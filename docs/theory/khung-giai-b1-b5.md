# Khung giải B.1 và B.5 — để tự giải lại nhanh

Mục đích: giúp thành viên **tự giải lại** hai chứng minh nặng nhất trong 60–90 phút
thay vì 3–4 tiếng, mà vẫn là tự giải chứ không phải đọc thuộc.

Cách dùng: che [bản đầy đủ](part-b.tex) lại. Mỗi bước dưới đây cho **nước đi**, không
cho phép biến đổi. Bạn tự viết phần đại số vào giấy. Giải xong mới mở `part-b.tex` so.

Nếu một bước bạn không tự viết ra được sau 5 phút → mở đúng mục đó trong
`part-b.tex`, đọc, gấp lại, viết lại từ đầu. Đừng đọc cả bài.

---

## B.1 — Var(q·k) = d_k và vì sao chia √d_k

**Ước lượng: 30 phút.**

### Giả thiết phải nhớ (viết ra trước khi tính)

`q, k ∈ R^{d_k}`. Toàn bộ **2d_k** thành phần **độc lập lẫn nhau**, mỗi thành phần
kỳ vọng 0, phương sai 1.

> ⚠️ Giả thiết độc lập được dùng **hai lần, hai vai trò khác nhau**. Nhớ chỗ nào
> dùng cái gì — thầy hay vặn đúng điểm này.

### Phần 1: tính phương sai

| # | Nước đi | Bạn tự viết |
|---|---|---|
| 1 | Đặt `Z_i = q_i · k_i`. Từ `Var(q_i) = E[q_i²] − (E[q_i])²` và `E[q_i] = 0`, suy ra gì? | `E[q_i²] = ?` |
| 2 | Dùng độc lập **lần 1** (giữa `q_i` và `k_i`) để tách `E[Z_i]` và `E[Z_i²]` thành tích | `E[Z_i] = ?`, `E[Z_i²] = ?` ⟹ `Var(Z_i) = ?` |
| 3 | Dùng độc lập **lần 2** (giữa chỉ số `i ≠ j`): `Z_i` và `Z_j` là hàm của hai nhóm biến nào? Suy ra `Cov(Z_i, Z_j) = ?` | |
| 4 | `q·k = Σ Z_i`. Viết công thức phương sai của tổng, gồm cả số hạng hiệp phương sai | `Var(q·k) = Σ Var(Z_i) + 2Σ Cov(...) = ?` |
| 5 | Chia `√d_k` rồi dùng `Var(cX) = c² Var(X)` | `Var(q·k / √d_k) = ?` |

**Tự kiểm:** ra `d_k` ở bước 4 và `1` ở bước 5.

### Phần 2: vì sao giúp giảm bão hòa softmax

| # | Nước đi | Bạn tự viết |
|---|---|---|
| 6 | Viết `s_i = e^{z_i} / Σ e^{z_j}`. Lấy đạo hàm `∂s_i/∂z_j` bằng quy tắc thương | Kết quả gọn lại thành `s_i(δ_ij − s_j)` |
| 7 | Giả sử `z_a` hơn mọi điểm khác ít nhất `g > 0`. Viết `s_a` dưới dạng `1/(1 + Σ_{j≠a} e^{−(z_a−z_j)})` rồi chặn dưới | `s_a ≥ 1/(1 + (m−1)e^{−g})` |
| 8 | Cho `g → ∞`: `s_a → ?`, các `s_j` khác `→ ?`, và theo bước 6 thì Jacobian `→ ?` | |

### Hai câu thầy hay vặn

**Hỏi:** *"Softmax bất biến khi cộng hằng số vào cả hàng. Vậy phương sai có ý nghĩa gì?"*

> Phương sai điều khiển **độ phân tán giữa các điểm**, không phải mức tuyệt đối. Chia
> `√d_k` co mọi **hiệu** `z_i − z_j` theo cùng hệ số `1/√d_k`. Bão hòa phụ thuộc hiệu,
> nên chia làm giảm bão hòa.

**Hỏi:** *"Giả thiết này có đúng với mô hình đã huấn luyện không?"*

> Không. Đây là mô hình giả định **tại khởi tạo**. Kết quả giải thích *lý do chọn*
> thang điểm, không khẳng định mọi hàng đều không bão hòa, cũng không khẳng định toạ
> độ `q, k` thực tế là độc lập hay phương sai đơn vị.

---

## B.5 — Nghiệm tối ưu có phạt KL → loss DPO

**Ước lượng: 40–50 phút.** Đây là bài nặng nhất và bị hỏi nhiều nhất.

### Giả thiết phải nhớ

Cố định câu hỏi `x`. `β > 0`. `π_ref` cố định. Tập đáp án hữu hạn không rỗng;
hỗ trợ `S_x = {y : π_ref(y|x) > 0}`. Chỉ tối ưu trên các `π` có hỗ trợ **nằm trong**
`S_x` — vì gán khối lượng dương ngoài `S_x` cho KL vô hạn.

### Phần 1: xây nghiệm ứng viên

| # | Nước đi | Bạn tự viết |
|---|---|---|
| 1 | Viết mục tiêu `J_x(π) = Σ π_y R_y − β Σ π_y log(π_y/q_y)` với `q_y = π_ref(y\|x)` | |
| 2 | Đặt `Z(x) = Σ_{y∈S_x} q_y exp(R_y/β)`. Vì sao `0 < Z(x) < ∞`? | (tập hữu hạn, hỗ trợ không rỗng, số hạng dương hữu hạn) |
| 3 | Định nghĩa `π*(y\|x) = q_y exp(R_y/β) / Z(x)`. Kiểm `Σ π* = 1` | |

### Phần 2: chứng minh π* là nghiệm **duy nhất** — đây là trục của bài

| # | Nước đi | Bạn tự viết |
|---|---|---|
| 4 | Từ định nghĩa `π*`, lấy log: `log(π*_y / q_y) = ?` | `= R_y/β − log Z(x)` |
| 5 | Thế kết quả bước 4 vào `β·KL(π‖π*) = β Σ π_y log(π_y/π*_y)`, tách ra, dùng `Σ π_y = 1` | **Ra đẳng thức trung tâm:** `β·KL(π‖π*) = β log Z(x) − J_x(π)` |
| 6 | Đọc bước 5: cực đại `J_x` ⟺ cực tiểu `KL(π‖π*)`. Vì sao `β log Z(x)` không ảnh hưởng? | (không phụ thuộc `π`) |
| 7 | Để chứng minh **duy nhất** mà không cần KKT: dùng `−log t ≥ 1 − t`, dấu bằng chỉ tại `t = 1`. Áp cho `t = π*_y / π_y` trên `T = {y : π_y > 0}` | `KL(π‖π*) ≥ Σ_{y∈T}(π_y − π*_y) = 1 − Σ_{y∈T} π*_y ≥ 0` |
| 8 | Nếu `KL = 0` thì hai bất đẳng thức ở bước 7 buộc điều gì? | (bđt đầu ⟹ `π = π*` trên `T`; bđt sau ⟹ `π*` không có khối lượng ngoài `T`) |

**Tự kiểm:** bước 5 là chỗ duy nhất phải biến đổi đại số thật. Viết được bước 5 là
coi như xong nửa bài.

### Phần 3: Bradley–Terry → loss DPO

| # | Nước đi | Bạn tự viết |
|---|---|---|
| 9 | Viết xác suất Bradley–Terry `Pr(y_w ≻ y_l)` dạng phân số, rồi gọn thành `σ(·)` | `= σ(R_w − R_l)` |
| 10 | **Giải nghịch** bước 4 theo reward | `R(x,y) = β log(π*(y\|x)/π_ref(y\|x)) + β log Z(x)` |
| 11 | Lấy **hiệu** hai đáp án **cùng một `x`**. Hạng nào triệt tiêu? | (`β log Z(x)` triệt tiêu) |
| 12 | Thay `π*` chưa biết bằng `π_θ`, đặt `z_θ = β[log(π_θ(y_w)/π_ref(y_w)) − log(π_θ(y_l)/π_ref(y_l))]`. Viết loss = −log-hợp-lý, lấy trung bình | `L_DPO = −E[log σ(z_θ)]` |

**Tự kiểm dấu:** nếu hai log-tỷ số bằng nhau thì `z_θ = 0` và loss một cặp
`= −log(1/2) = log 2 ≈ 0,693`.

### Bốn câu thầy hay vặn

| Hỏi | Trả lời |
|---|---|
| *"Reference để làm gì?"* | `π_ref` là mốc đo lệch. Không có nó thì theo bước 10, `R` chỉ xác định tới một hằng số, và phạt KL mất nghĩa. |
| *"`Z(x)` đâu rồi? Sao không phải tính?"* | Triệt tiêu ở bước 11 khi lấy hiệu hai đáp án **cùng một câu hỏi**. **Không** triệt tiêu nếu hai đáp án thuộc hai câu hỏi khác nhau — đó là lý do dữ liệu ưu tiên phải ghép theo cùng prompt. |
| *"`β > 0` cần ở đâu?"* | Ba chỗ: để `Z(x)` hữu hạn (bước 2), để chia `R_y/β` (bước 4), và để `argmax J = argmin KL` ở bước 6 không đổi chiều. |
| *"Chứng minh duy nhất — duy nhất cái gì?"* | Duy nhất của **`π*`** với reward đã cho, khi tối ưu trên các phân phối. **Không** phải duy nhất của tham số `θ` khi học từ hữu hạn cặp. Hai thứ khác nhau. |

---

## Sau khi giải xong

1. Mở [part-b.tex](part-b.tex) so từng bước.
2. Điền kết quả vào [phiếu rà soát](../progress/review-log-the.md), phần 3, dòng 3.1
   và 3.2, kèm ngày.
3. Bốn bài còn lại (B.2, B.3, B.4, B.6) chỉ cần **đọc hiểu mạch**, không cần giải lại —
   mỗi bài một ý chính, đã ghi ở dòng 3.3–3.6 của phiếu.
4. Khi cả 6 dòng đã điền → báo nhóm để đổi trạng thái B1–B6 trong
   [ma trận yêu cầu](../progress/requirements-matrix.md) và bỏ nhãn `Bản nháp` ở
   `part-b.tex` dòng 24 và 49.

**Không ai điền hộ bước 2.** Đó là lời khai rằng bạn hiểu, và vấn đáp 03/12 sẽ kiểm
đúng điều đó.
