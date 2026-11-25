"""Đối chiếu A.1 trên CPU; chỉ dùng attention thư viện ở phía tham chiếu."""

import math
import unittest

import torch
from torch import nn
from torch.nn import functional as F

from src.attention import (
    CausalSelfAttention, DecoderBlock, SinusoidalPositionEncoding,
    causal_mask, scaled_dot_product_attention,
)


class AttentionTest(unittest.TestCase):
    def setUp(self):
        rng = torch.random.fork_rng(devices=[])
        rng.__enter__()
        self.addCleanup(rng.__exit__, None, None, None)
        torch.random.default_generator.manual_seed(42)

    def test_mask_probabilities_and_weighted_sum(self):
        q = torch.zeros(1, 1, 3, 2)
        v = torch.tensor([2., 4., 12.]).view(1, 1, 3, 1)
        out, weights = scaled_dot_product_attention(q, q, v, causal_mask(3))
        expected = torch.tensor([[1, 0, 0], [.5, .5, 0], [1/3, 1/3, 1/3]])
        torch.testing.assert_close(weights[0, 0], expected)
        torch.testing.assert_close(out.flatten(), torch.tensor([2., 3., 6.]))

    def test_attention_matches_torch_with_and_without_mask(self):
        q, k, v = torch.randn(3, 2, 3, 5, 4, dtype=torch.float64).unbind()
        for causal in (False, True):
            with self.subTest(causal=causal):
                out, _ = scaled_dot_product_attention(q, k, v, causal_mask(5) if causal else None)
                ref = F.scaled_dot_product_attention(q, k, v, is_causal=causal, dropout_p=0.)
                torch.testing.assert_close(out, ref, rtol=1e-10, atol=1e-12)

    def test_heads_match_reference_with_identical_projections(self):
        attn = CausalSelfAttention(12, 3, max_len=8).double()
        ref = nn.MultiheadAttention(12, 3, batch_first=True, dropout=0.).double()
        with torch.no_grad():
            ref.in_proj_weight.copy_(attn.qkv.weight)
            ref.in_proj_bias.copy_(attn.qkv.bias)
            ref.out_proj.load_state_dict(attn.out_proj.state_dict())
        x = torch.randn(2, 5, 12, dtype=torch.float64, requires_grad=True)
        # Dựng mặt nạ tham chiếu độc lập với causal_mask tự viết.
        idx = torch.arange(x.size(1))
        expected, _ = ref(x, x, x, attn_mask=idx[:, None] < idx[None, :])
        actual = attn(x)
        torch.testing.assert_close(actual, expected, rtol=1e-10, atol=1e-12)
        probe = torch.randn_like(actual)
        grad = torch.autograd.grad(actual, x, probe)[0]
        grad_ref = torch.autograd.grad(expected, x, probe)[0]
        torch.testing.assert_close(grad, grad_ref, rtol=1e-10, atol=1e-12)

    def test_sinusoidal_pairs_and_unpaired_last_dimension(self):
        x = torch.randn(2, 4, 5)
        actual = SinusoidalPositionEncoding(5, 8)(x)
        expected = torch.tensor([
            [(math.sin if j % 2 == 0 else math.cos)(p / 10000 ** (2 * (j // 2) / 5))
             for j in range(5)] for p in range(4)
        ])
        torch.testing.assert_close(actual, x + expected)

    def test_decoder_prefix_is_independent_of_all_future_tokens(self):
        embed = nn.Embedding(16, 12)
        pos = SinusoidalPositionEncoding(12, 8)
        block = DecoderBlock(12, 3, 24, 8)
        ids = torch.tensor([[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]])
        changed = ids.clone()
        changed[:, 2:] += 6
        with torch.no_grad():
            out = block(pos(embed(ids)))
            other = block(pos(embed(changed)))
            prefix = block(pos(embed(ids[:, :2])))
        torch.testing.assert_close(out[:, :2], other[:, :2])
        torch.testing.assert_close(out[:, :2], prefix)
        self.assertFalse(torch.allclose(out[:, 2:], other[:, 2:]))


if __name__ == '__main__':
    unittest.main()
