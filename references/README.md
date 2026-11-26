# Kiểm kê tài liệu tham khảo

## Phạm vi và trạng thái

Thư mục này hiện có **6 PDF**: năm bài báo nền tảng cho Đề tài 9 và một bản đề bài. Bản đề là *Danh mục 20 bài tập lớn: Học máy cơ bản, mô hình ngôn ngữ lớn, học tăng cường và tích hợp*, ngày **12/11/2026**, ghi **46 trang** (trang 1/46 trong PDF), trong đó Đề tài 9 nằm ở trang 18–19.

**Đầu vào còn mở:** chưa có ma trận Q/K/V giảng viên cấp cho C.1 hay bộ số quy định cho C.4; nguồn hành chính chưa đủ bằng chứng hiệu lực/quyền dùng. Corpus A.2 đã chọn [Truyện Kiều bản Trương Vĩnh Ký 1911](../docs/data/char-corpus.md) với phạm vi dùng nội bộ. Không thiếu tệp nào trong danh sách sáu PDF tham khảo.

Các PDF là tư liệu nguồn của kho. Không tự xóa, đổi tên hoặc chỉnh sửa chúng; nếu chúng đang được Git theo dõi thì phải giữ nguyên trạng thái đó. Tình trạng quyền phân phối/lưu trữ lại của từng PDF **chưa được kiểm chứng**. Vì vậy, trước khi chia sẻ kho công khai hoặc phân phối lại các tệp, cần kiểm tra giấy phép/điều khoản tại nguồn chính thức; việc có tệp trong kho không tự nó xác nhận quyền phân phối.

## Danh mục tệp

|Tệp cục bộ|Loại và nhận dạng nguồn|Phiên bản/ấn bản thể hiện trong PDF|Liên kết nguồn chính|Vai trò đối với Đề tài 9|
|---|---|---|---|---|
|`Attention.pdf`|Vaswani et al., **Attention Is All You Need**|arXiv:1706.03762v7, 02/08/2023; NIPS 2017|[arXiv abs](https://arxiv.org/abs/1706.03762)|Transformer: chú ý tích vô hướng có chia tỷ lệ, đa đầu, mặt nạ nhân quả, vị trí hình sin và độ phức tạp self-attention.|
|`LoRA.pdf`|Hu et al., **LoRA: Low-Rank Adaptation of Large Language Models**|arXiv:2106.09685v2, 16/10/2021; PDF ghi “Version 2”|[arXiv abs](https://arxiv.org/abs/2106.09685)|Cập nhật hạng thấp, đóng băng trọng số gốc, hợp nhất trọng số và số tham số huấn luyện.|
|`QLora.pdf`|Dettmers et al., **QLoRA: Efficient Finetuning of Quantized LLMs**|arXiv:2305.14314v1, 23/05/2023; preprint under review|[arXiv abs](https://arxiv.org/abs/2305.14314)|QLoRA 4-bit, NF4, double quantization, paged optimizers và lưu ý về bộ nhớ.|
|`RLHF.pdf`|Ouyang et al., **Training language models to follow instructions with human feedback**|arXiv:2203.02155v1, 04/03/2022|[arXiv abs](https://arxiv.org/abs/2203.02155)|Ngữ cảnh SFT, dữ liệu so sánh do người gán nhãn, đánh giá preference và các tiêu chí helpful/honest/harmless. Không phải yêu cầu triển khai PPO của Đề tài 9.|
|`DPO.pdf`|Rafailov et al., **Direct Preference Optimization: Your Language Model is Secretly a Reward Model**|arXiv:2305.18290v3, 29/07/2024; NeurIPS 2023|[arXiv abs](https://arxiv.org/abs/2305.18290)|Dẫn xuất mục tiêu DPO từ Bradley–Terry và chính sách tham chiếu; huấn luyện ưu tiên trực tiếp không cần reward model/RL vòng lặp.|
|`DANH MỤC BÀI TẬP LỚN CUỐI KÌ MÔN HỌC MÁY CƠ BẢN.pdf`|TS. Phạm Văn Khánh, **Danh mục 20 bài tập lớn: Học máy cơ bản, mô hình ngôn ngữ lớn, học tăng cường và tích hợp**|Ngày 12/11/2026; 46 trang|Tệp đề bài cục bộ; chưa có URL nguồn được xác nhận|Nguồn yêu cầu chấm, tiến độ, sản phẩm nộp và toàn bộ A–D của Đề tài 9.|

## Phạm vi đã đọc trực tiếp

Danh sách này chỉ ghi phần đã đọc để lập ma trận yêu cầu; không ngụ ý đã tái lập thí nghiệm hay xác nhận mọi kết quả trong bài báo.

- **Đề bài:** trang 1–4 (mục tiêu, quy định, tổng quan Đề tài 9) và trang 18–19 (toàn bộ Đề tài 9, A–D).
- **Attention:** tr. 1–6; Abstract, §1–§3.5 và mở đầu §4. Đã đọc phần kiến trúc encoder/decoder, scaled dot-product attention, multi-head attention, causal masking, FFN, positional encoding và bảng độ phức tạp.
- **LoRA:** tr. 1–5; Abstract, §1–§4.2. Đã đọc bài toán thích nghi, tham số hóa $W_0 + BA$, khởi tạo/hệ số tỉ lệ, hợp nhất khi suy luận và vị trí áp dụng trong Transformer.
- **QLoRA:** tr. 1–8; Abstract, §1–§4 và §5.1. Đã đọc block-wise quantization, adapter, NF4, double quantization, paged optimizers, định nghĩa QLoRA, các giới hạn/bằng chứng thực nghiệm được tác giả nêu và cấu hình huấn luyện minh họa.
- **RLHF:** tr. 1–10; Abstract, §1, §3.1–§3.6. Đã đọc chuỗi SFT → reward model → PPO, nguồn/gán nhãn dữ liệu, cách thu thập so sánh và khung đánh giá. Đây là nền tảng đối chiếu khái niệm, không biến PPO thành hạng mục của Đề tài 9.
- **DPO:** tr. 1–10; Abstract, §1, §3–§4, §5.1–§5.2, §6–§7. Đã đọc RLHF tiền đề, Bradley–Terry, mục tiêu KL-ràng buộc, dẫn xuất DPO, pipeline ưu tiên ngoại tuyến, thiết lập/giới hạn đánh giá và thảo luận.

## Ranh giới diễn giải

- Đề bài bắt buộc **SFT và DPO** cho ứng dụng Đề tài 9 (tr. 19). QLoRA là phương án phục vụ yêu cầu “LoRA hoặc QLoRA”, còn Qwen2.5-1.5B-Instruct chỉ là ứng viên nếu sau này nhóm chọn; chưa có quyết định mô hình trong tài liệu này.
- RLHF/PPO được đọc để phân biệt DPO với pipeline reward-model + RL; chúng **không** là hạng mục triển khai của Đề tài 9. RAG chỉ được nêu trong đề như hướng mở rộng thuộc Đề tài 11, nên **không** nằm trong phạm vi triển khai hiện tại.
- Các con số/kết quả trong năm bài báo là kết quả của tác giả trên thiết lập của họ, không phải kết quả của nhóm. Không suy ra tính khả thi, hiệu năng hoặc mục tiêu điểm số của dự án từ các kết quả đó.
