"""A.1: self-attention nhân quả cho decoder-only LM, không dùng attention dựng sẵn."""

import math

import torch
from torch import Tensor, nn


def causal_mask(length: int, *, device: torch.device | None = None) -> Tensor:
    """[T,T], True tại cột j > hàng i (bị chặn); luôn giữ đường chéo."""
    return torch.ones(length, length, dtype=torch.bool, device=device).triu_(1)


def scaled_dot_product_attention(
    q: Tensor, k: Tensor, v: Tensor, blocked: Tensor | None = None
) -> tuple[Tensor, Tensor]:
    """Đầu vào [...,T,D]; trả (tổng có trọng số, xác suất trên các key).

    blocked là mặt nạ bool broadcast được lên scores; mỗi query cần ít nhất
    một key hợp lệ. None nghĩa là không che, không phải chế độ nhân quả.
    """
    scores = (q @ k.transpose(-2, -1)) * (q.size(-1) ** -0.5)
    if blocked is not None:
        scores.masked_fill_(blocked, float('-inf'))
    weights = scores.softmax(dim=-1)
    return weights @ v, weights


class CausalSelfAttention(nn.Module):
    """Chiếu Q/K/V một lần, tính các head song song, ghép rồi chiếu về D."""

    def __init__(self, d_model: int, n_heads: int, max_len: int):
        super().__init__()
        if d_model < 1 or n_heads < 1 or d_model % n_heads:
            raise ValueError('d_model phải dương và chia hết cho n_heads dương')
        if max_len < 1:
            raise ValueError('max_len phải dương')
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        self.register_buffer('blocked', causal_mask(max_len), persistent=False)

    def forward(self, x: Tensor) -> Tensor:
        batch, length, width = x.shape
        if not 0 < length <= self.blocked.size(0):
            raise ValueError('Độ dài chuỗi ngoài phạm vi causal mask')
        # [B,T,3,H,Dh] -> 3 tensor [B,H,T,Dh]; không trộn trục head và token.
        q, k, v = self.qkv(x).view(batch, length, 3, self.n_heads, self.head_dim).permute(2, 0, 3, 1, 4).unbind(0)
        heads, _ = scaled_dot_product_attention(q, k, v, self.blocked[:length, :length])
        return self.out_proj(heads.transpose(1, 2).reshape(batch, length, width))


class SinusoidalPositionEncoding(nn.Module):
    """Cộng PE cố định vào embedding [B,T,D], đúng một lần trước chồng block."""

    def __init__(self, d_model: int, max_len: int):
        super().__init__()
        if min(d_model, max_len) < 1:
            raise ValueError('d_model và max_len phải dương')
        freq = torch.exp(torch.arange(0, d_model, 2, dtype=torch.float32) * (-math.log(10000.0) / d_model))
        angles = torch.arange(max_len, dtype=freq.dtype)[:, None] * freq
        table = torch.empty(max_len, d_model, dtype=freq.dtype)
        table[:, 0::2] = angles.sin()
        table[:, 1::2] = angles[:, :d_model // 2].cos()
        self.register_buffer('table', table, persistent=False)

    def forward(self, x: Tensor) -> Tensor:
        if x.ndim != 3 or x.size(-1) != self.table.size(1) or not 0 < x.size(1) <= self.table.size(0):
            raise ValueError('PE cần [B,T,d_model] với 0 < T <= max_len')
        return x + self.table[:x.size(1)].to(dtype=x.dtype)


class DecoderBlock(nn.Module):
    """Pre-LN, hai nhánh residual, FFN theo từng vị trí; không cross-attention."""

    def __init__(self, d_model: int, n_heads: int, d_ff: int, max_len: int):
        super().__init__()
        if d_ff < 1:
            raise ValueError('d_ff phải dương')
        self.attn = CausalSelfAttention(d_model, n_heads, max_len)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(nn.Linear(d_model, d_ff), nn.ReLU(), nn.Linear(d_ff, d_model))

    def forward(self, x: Tensor) -> Tensor:
        x = x + self.attn(self.norm1(x))
        return x + self.ffn(self.norm2(x))
