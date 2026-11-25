"""A.2: LM ký tự nhân quả, dùng trực tiếp decoder và mã vị trí của A.1."""

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F

from .attention import DecoderBlock, SinusoidalPositionEncoding


class CharacterLM(nn.Module):
    """Nhận ID [B,T], trả logits [B,T,V] dự đoán ký tự kế tiếp tại từng vị trí."""

    def __init__(self, vocab_size: int, context_length: int, d_model: int,
                 n_heads: int, d_ff: int, n_layers: int):
        super().__init__()
        if vocab_size < 2 or n_layers < 1:
            raise ValueError('Cần ít nhất hai token (kể cả UNK) và một decoder block')
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.position = SinusoidalPositionEncoding(d_model, context_length)
        self.blocks = nn.Sequential(*(
            DecoderBlock(d_model, n_heads, d_ff, context_length) for _ in range(n_layers)
        ))
        self.norm = nn.LayerNorm(d_model)
        self.readout = nn.Linear(d_model, vocab_size)

    def forward(self, ids: Tensor) -> Tensor:
        hidden = self.position(self.embedding(ids))
        return self.readout(self.norm(self.blocks(hidden)))


@torch.inference_mode()
def validation_metrics(model: nn.Module, windows: Tensor, batch_size: int,
                       device: torch.device) -> dict[str, float | int]:
    """PPL trên các target được chấm, kể cả UNK. Không lấy trung bình PPL các batch."""
    if batch_size < 1 or windows.ndim != 2 or windows.size(0) == 0 or windows.size(1) < 2:
        raise ValueError('Cần các cửa sổ [N,T+1] không rỗng và batch_size dương')
    was_training = model.training
    model.eval()
    try:
        nll_sum = torch.zeros((), dtype=torch.float64, device=device)
        for batch in windows.split(batch_size):
            batch = batch.to(device)
            logits = model(batch[:, :-1])
            nll_sum += F.cross_entropy(logits.flatten(0, 1), batch[:, 1:].reshape(-1), reduction='sum')
        token_count = windows.size(0) * (windows.size(1) - 1)
        nll = nll_sum.item() / token_count
        return {'validation_tokens': token_count, 'validation_nll': nll, 'validation_ppl': math.exp(nll)}
    finally:
        model.train(was_training)
