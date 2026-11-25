"""Kiểm LoRA CPU: đếm tham số, gradient khi học và xuất lớp suy luận."""

import unittest

import torch
from torch import nn
from torch.nn.functional import linear

from src.lora import LoRALinear


class LoRALinearTest(unittest.TestCase):
    def setUp(self):
        self.addCleanup(torch.set_rng_state, torch.get_rng_state())
        torch.random.default_generator.manual_seed(42)

    def test_initial_function_and_trainable_count(self):
        for rank in (1, 2, 4):
            with self.subTest(rank=rank):
                base = nn.Linear(7, 4, dtype=torch.float64)
                x = torch.randn(3, 7, dtype=base.weight.dtype)
                before = base(x).detach()
                layer = LoRALinear(base, rank=rank, alpha=6.)
                torch.testing.assert_close(layer(x), before, rtol=0, atol=0)
                trainable = {k: v.numel() for k, v in layer.named_parameters() if v.requires_grad}
                self.assertEqual(trainable, {'A': rank * 7, 'B': 4 * rank})

    def test_two_steps_adapt_only_factors_and_propagate_input_gradient(self):
        base = nn.Linear(7, 4, dtype=torch.float64)
        w0, b0 = base.weight.detach().clone(), base.bias.detach().clone()
        layer = LoRALinear(base, rank=2, alpha=6.)
        x = torch.randn(3, 7, dtype=torch.float64, requires_grad=True)
        target = torch.randn(3, 4, dtype=x.dtype)
        for step in range(2):
            layer.zero_grad(set_to_none=True)
            x.grad = None
            loss = (layer(x) - target).square().mean()
            loss.backward()
            self.assertGreater(x.grad.norm().item(), 0.)
            self.assertIsNone(base.weight.grad)
            self.assertIsNone(base.bias.grad)
            self.assertEqual(layer.A.grad.norm().item() > 0., step > 0)
            self.assertGreater(layer.B.grad.norm().item(), 0.)
            with torch.no_grad():
                for p in (layer.A, layer.B):
                    p.add_(p.grad, alpha=-0.05)
        torch.testing.assert_close(base.weight, w0, rtol=0, atol=0)
        torch.testing.assert_close(base.bias, b0, rtol=0, atol=0)
        self.assertFalse(torch.allclose(layer(x), linear(x, w0, b0)))

    def test_nonzero_adapter_agrees_with_dense_oracle_before_and_after_merge(self):
        for bias in (False, True):
            with self.subTest(bias=bias), torch.no_grad():
                base = nn.Linear(7, 4, bias=bias, dtype=torch.float64)
                layer = LoRALinear(base, rank=2, alpha=6.)
                layer.B.normal_()
                x = torch.randn(2, 5, 7, dtype=base.weight.dtype)
                w0 = base.weight.clone()
                delta = 3. * (layer.B @ layer.A)
                self.assertEqual(torch.linalg.matrix_rank(delta).item(), 2)
                expected = linear(x, w0 + delta, base.bias)
                self.assertFalse(torch.allclose(expected, base(x)))
                merged = layer.merge()
                self.assertIs(type(merged), nn.Linear)
                torch.testing.assert_close(layer(x), expected)
                torch.testing.assert_close(merged(x), expected)
                torch.testing.assert_close(layer.merge()(x), expected)
                torch.testing.assert_close(base.weight, w0, rtol=0, atol=0)
                layer.B.zero_()
                torch.testing.assert_close(merged(x), expected)


if __name__ == '__main__':
    unittest.main()
