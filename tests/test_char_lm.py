"""A.2: rò token tương lai và PPL bị lệch do trung bình theo batch."""

import math
import unittest

import torch
from torch import nn

from src.char_lm import CharacterLM, validation_metrics


class CharacterLMTest(unittest.TestCase):
    def test_future_char_does_not_change_prefix_logits(self):
        with torch.random.fork_rng(devices=[]), torch.no_grad():
            torch.random.default_generator.manual_seed(42)
            model = CharacterLM(5, 4, 8, 2, 16, 2).eval()
            a, b = model(torch.tensor([[1, 2, 3, 4], [1, 2, 0, 0]])).unbind()
            torch.testing.assert_close(a[:2], b[:2])
            self.assertFalse(torch.allclose(a[2:], b[2:]))

    def test_ppl_uses_shifted_targets_including_unk_and_last_short_batch(self):
        # Với mọi input: P(UNK=0)=1/4, P(1)=3/4. Ba cửa sổ có tổng cộng 6 target.
        log_probs = torch.tensor([[0.25, 0.75], [0.25, 0.75]], dtype=torch.float64).log()
        oracle = nn.Embedding.from_pretrained(log_probs)
        windows = torch.tensor([[0, 1, 1], [0, 1, 1], [1, 0, 0]])
        stats = validation_metrics(oracle, windows, 2, torch.device('cpu'))
        nll = -(4 * math.log(0.75) + 2 * math.log(0.25)) / 6
        self.assertEqual(stats['validation_tokens'], 6)
        self.assertAlmostEqual(stats['validation_nll'], nll)
        self.assertAlmostEqual(stats['validation_ppl'], math.exp(nll))
        self.assertTrue(oracle.training)
