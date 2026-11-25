"""A.4 — Direct Preference Optimization (Rafailov et al., phương trình 7)."""

import math

from torch import Tensor
from torch.nn.functional import logsigmoid


def dpo_loss(
    policy_chosen: Tensor,
    policy_rejected: Tensor,
    ref_chosen: Tensor,
    ref_rejected: Tensor,
    *,
    beta: float,
) -> Tensor:
    """Trả loss vô hướng, trung bình theo cặp; reference không nhận gradient.

    Bốn tensor số thực cùng shape (vô hướng hoặc [B], B > 0). Mỗi giá trị
    là tổng log-xác suất tự nhiên hữu hạn của token đáp án cho cùng prompt,
    không gồm prompt/padding. Khi tính từ token, nên cộng ở float32 trở lên.
    """
    if not math.isfinite(beta) or beta <= 0:
        raise ValueError('beta phải hữu hạn và dương')
    inputs = (policy_chosen, policy_rejected, ref_chosen.detach(), ref_rejected.detach())
    if policy_chosen.ndim > 1 or not policy_chosen.numel() or any(t.shape != policy_chosen.shape for t in inputs):
        raise ValueError('Cần bốn log-xác suất chuỗi cùng shape: vô hướng hoặc [B], B > 0')
    if not all(t.is_floating_point() for t in inputs):
        raise TypeError('Log-xác suất phải là tensor số thực')
    # Không thực hiện phép trừ hoặc nhân beta ở độ chính xác nửa.
    pw, pl, rw, rl = (t if t.element_size() >= 4 else t.float() for t in inputs)
    margin = (pw - pl) - (rw - rl)
    return -logsigmoid(beta * margin).mean()
