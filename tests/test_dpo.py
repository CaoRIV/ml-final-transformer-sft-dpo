"""Kiểm DPO từ log-xác suất chuỗi minh họa, không dùng dữ liệu người chấm."""

import math
import unittest

import torch
from torch.nn.functional import cross_entropy

from src.dpo import dpo_loss


class DPOLossTest(unittest.TestCase):
    def test_equal_odds_and_increasing_preference(self):
        pw, pl, rw, rl = torch.tensor([-2., -3., -4., -5.], dtype=torch.float64).unbind()
        loss = dpo_loss(pw, pl, rw, rl, beta=0.5)
        self.assertAlmostEqual(loss.item(), math.log(2))
        self.assertLess(dpo_loss(pw + 1, pl, rw, rl, beta=0.5).item(), loss.item())

    def test_minibatch_matches_two_class_likelihood_and_gradient(self):
        beta = 0.7
        w, l, rw, rl = [torch.tensor(v, dtype=torch.float64, requires_grad=True) for v in (
            [-10., -3., -7.], [-4., -8., -8.], [-8., -4., -4.], [-5., -6., -5.])]
        loss = dpo_loss(w, l, rw, rl, beta=beta)
        # Hai lớp [chosen, rejected]; nhãn đúng luôn là lớp 0.
        scores = beta * torch.stack((w - rw.detach(), l - rl.detach()), dim=1)
        expected = cross_entropy(scores, torch.zeros(3, dtype=torch.long))
        torch.testing.assert_close(loss, expected)
        loss.backward()
        grad_w, grad_l = torch.autograd.grad(expected, (w, l))
        torch.testing.assert_close(w.grad, grad_w)
        torch.testing.assert_close(l.grad, grad_l)
        self.assertIsNone(rw.grad)
        self.assertIsNone(rl.grad)

    def test_extreme_margins_remain_finite(self):
        w = torch.tensor([-1001., -1.], requires_grad=True)
        l = torch.tensor([-1., -1001.])
        ref = torch.full_like(w, -2.)
        loss = dpo_loss(w, l, ref, ref, beta=1.)
        torch.testing.assert_close(loss, torch.tensor(500.))
        loss.backward()
        torch.testing.assert_close(w.grad, torch.tensor([-0.5, 0.]))

    def test_invalid_beta_and_unpaired_batches(self):
        x = torch.tensor([-2., -3.])
        for beta in (0., -1., float('nan'), float('inf')):
            with self.subTest(beta=beta), self.assertRaises(ValueError):
                dpo_loss(x, x, x, x, beta=beta)
        for other in (x[:1], x[:, None]):
            with self.subTest(shape=other.shape), self.assertRaises(ValueError):
                dpo_loss(x, x, x, other, beta=1.)
        with self.assertRaises(ValueError):
            dpo_loss(*(x[:0] for _ in range(4)), beta=1.)


if __name__ == '__main__':
    unittest.main()
