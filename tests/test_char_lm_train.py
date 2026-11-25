"""A.2: tiếp tục checkpoint CPU phải trùng tuyệt đối với lượt chạy liên tục."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import torch

import src.char_lm_train as training
from src.char_lm_train import run_seed


class InterruptedTraining(RuntimeError):
    pass


class CharacterLMTrainTest(unittest.TestCase):
    def setUp(self):
        self.train = torch.tensor([
            [0, 1, 2, 3, 4],
            [1, 2, 3, 4, 5],
            [2, 3, 4, 5, 6],
            [3, 4, 5, 6, 7],
            [7, 6, 5, 4, 3],
            [6, 5, 4, 3, 2],
        ], dtype=torch.long)
        self.validation = torch.tensor([
            [0, 2, 4, 6, 1],
            [7, 5, 3, 1, 0],
        ], dtype=torch.long)
        self.vocab = {str(index): index for index in range(8)}
        self.config = {
            "d_model": 8,
            "n_heads": 2,
            "d_ff": 16,
            "n_layers": 1,
            "epochs": 3,
            "batch_size": 2,
            "lr": 1e-2,
        }
        self.device = torch.device("cpu")

    def _checkpoint(self, run_dir: Path) -> dict:
        return torch.load(
            run_dir / "checkpoint_epoch_0003.pt", map_location="cpu", weights_only=True,
        )

    def test_interrupted_resume_matches_continuous_cpu_exactly(self):
        with tempfile.TemporaryDirectory() as temporary, torch.random.fork_rng(devices=[]):
            root = Path(temporary)
            continuous_dir = root / "continuous"
            resumed_dir = root / "resumed"

            continuous = run_seed(
                self.train, self.validation, self.vocab, "synthetic-v1", self.config,
                1234, continuous_dir, self.device,
            )

            original_save = training._save_checkpoint

            def save_then_interrupt(path: Path, checkpoint: dict) -> None:
                original_save(path, checkpoint)
                if checkpoint["epoch"] == 1:
                    raise InterruptedTraining("Mô phỏng ngắt sau checkpoint epoch 1")

            with patch.object(training, "_save_checkpoint", side_effect=save_then_interrupt):
                with self.assertRaises(InterruptedTraining):
                    run_seed(
                        self.train, self.validation, self.vocab, "synthetic-v1", self.config,
                        1234, resumed_dir, self.device,
                    )

            resumed = run_seed(
                self.train, self.validation, self.vocab, "synthetic-v1", self.config,
                1234, resumed_dir, self.device, resume=True,
            )

            self.assertEqual(continuous, resumed)
            continuous_checkpoint = self._checkpoint(continuous_dir)
            resumed_checkpoint = self._checkpoint(resumed_dir)
            self.assertEqual(continuous_checkpoint["epoch"], resumed_checkpoint["epoch"])
            self.assertEqual(continuous_checkpoint["step"], resumed_checkpoint["step"])
            for name, tensor in continuous_checkpoint["model_state"].items():
                torch.testing.assert_close(tensor, resumed_checkpoint["model_state"][name], rtol=0, atol=0)

    def test_resume_rejects_incompatible_seed_without_overwriting(self):
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = Path(temporary) / "seed"
            run_seed(
                self.train, self.validation, self.vocab, "synthetic-v1", self.config,
                1234, run_dir, self.device,
            )
            before = self._checkpoint(run_dir)
            with self.assertRaisesRegex(ValueError, "Seed không khớp"):
                run_seed(
                    self.train, self.validation, self.vocab, "synthetic-v1", self.config,
                    5678, run_dir, self.device, resume=True,
                )
            after = self._checkpoint(run_dir)
            self.assertEqual(before["seed"], after["seed"])
            self.assertEqual(before["step"], after["step"])


if __name__ == "__main__":
    unittest.main()
