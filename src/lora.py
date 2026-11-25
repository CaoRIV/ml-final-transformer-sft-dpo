"""A.3 — LoRA cho nn.Linear có trọng số dấu phẩy động (không lượng tử hóa)."""

from copy import deepcopy
import math

import torch
from torch import Tensor, nn
from torch.nn.functional import linear


class LoRALinear(nn.Module):
    """Bọc trực tiếp lớp nền và đóng băng cả weight lẫn bias của lớp đó.

    Khi lưu/nạp state_dict của wrapper, dùng lại cùng cấu hình rank và alpha.
    merge() xuất lớp suy luận riêng, không thay đổi wrapper để học tiếp.
    """

    def __init__(self, base: nn.Linear, rank: int, alpha: float):
        super().__init__()
        if not 1 <= rank <= min(base.in_features, base.out_features):
            raise ValueError('rank phải nằm trong [1, min(in_features, out_features)]')
        if not math.isfinite(alpha) or alpha <= 0:
            raise ValueError('alpha phải hữu hạn và dương')
        self.scale = alpha / rank
        self.A = nn.Parameter(base.weight.new_empty(rank, base.in_features))
        self.B = nn.Parameter(base.weight.new_zeros(base.out_features, rank))
        nn.init.normal_(self.A, std=base.in_features ** -0.5)
        self.base = base.requires_grad_(False)
        self.base.zero_grad(set_to_none=True)

    def forward(self, x: Tensor) -> Tensor:
        # Không tạo ma trận BA kích thước d × k trong mỗi lượt forward.
        return torch.add(self.base(x), linear(linear(x, self.A), self.B), alpha=self.scale)

    @torch.no_grad()
    def merge(self) -> nn.Linear:
        """Trả nn.Linear độc lập chứa W + (alpha/rank) BA và bias gốc."""
        merged = deepcopy(self.base)
        merged.weight.addmm_(self.B, self.A, alpha=self.scale)
        return merged.eval()
