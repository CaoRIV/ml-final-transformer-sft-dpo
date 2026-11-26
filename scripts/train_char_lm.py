"""A.2: chạy 5 model độc lập trên cùng bộ cửa sổ đã được phép huấn luyện.

Từ thư mục gốc: python -m scripts.train_char_lm --help
"""

import argparse
import json
import math
from pathlib import Path
import statistics

import torch

from src.char_lm_data import CorpusLoadError, load_prepared_corpus
from src.char_lm_train import run_seed


SEEDS = (41, 42, 43, 44, 45)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', required=True, type=Path)
    p.add_argument('--artifact-dir', required=True, type=Path, help='Thư mục output của prepare_char_corpus')
    p.add_argument('--rights-attestation', required=True, type=Path, help='Xác nhận nội bộ khớp SHA-256 của manifest 1911')
    p.add_argument('--output', required=True, type=Path, help='Thư mục mới cho kết quả và checkpoint')
    p.add_argument('--resume', action='store_true', help='Nối lại cùng thí nghiệm, không tạo seed trùng')
    p.add_argument('--device', choices=('cpu', 'cuda'), default='cpu')
    p.add_argument('--platform', choices=('colab', 'kaggle'), default='colab',
                   help='Phạm vi bắt buộc trong xác nhận quyền')
    p.add_argument('--epochs', type=int, default=5)
    p.add_argument('--batch-size', type=int, default=16)
    p.add_argument('--lr', type=float, default=0.001)
    p.add_argument('--d-model', type=int, default=64)
    p.add_argument('--n-heads', type=int, default=4)
    p.add_argument('--d-ff', type=int, default=128)
    p.add_argument('--n-layers', type=int, default=2)
    args = p.parse_args()
    config = {k: getattr(args, k) for k in ('d_model', 'n_heads', 'd_ff', 'n_layers', 'epochs', 'batch_size', 'lr')}
    if not all(math.isfinite(v) and v > 0 for v in config.values()) or args.d_model % args.n_heads:
        p.error('Cấu hình phải hữu hạn, dương và d_model chia hết cho n_heads.')
    if args.device == 'cuda' and not torch.cuda.is_available():
        p.error('Không có CUDA trong phiên hiện tại. Bật GPU hoặc dùng --device cpu.')
    # Kiểm quyền và dữ liệu trước cả việc tạo output hay khởi tạo model.
    try:
        train, val, vocab, data_id = load_prepared_corpus(
            args.manifest, args.artifact_dir, args.rights_attestation, platform=args.platform,
        )
    except CorpusLoadError as error:
        p.error(str(error))
    run_experiment(train, val, vocab, data_id, config, args.output, torch.device(args.device), args.resume)


def run_experiment(train, val, vocab, data_id, config, output: Path, device: torch.device, resume=False):
    if resume and not output.is_dir():
        raise FileNotFoundError('--resume cần đúng thư mục thí nghiệm đã tạo')
    if not resume:
        output.mkdir(parents=True, exist_ok=False)
    results = []
    for seed in SEEDS:
        directory = output / f'seed-{seed}'
        result = run_seed(train, val, vocab, data_id, config, seed, directory,
                          device, resume=resume and directory.exists())
        results.append(result)
        print(f"seed={seed} validation_tokens={result['validation_tokens']} PPL={result['validation_ppl']:.4f}", flush=True)
    ppls = [row['validation_ppl'] for row in results]
    summary = {'data_id': data_id, 'config': config, 'seeds': SEEDS, 'runs': results,
               'unit': 'independent training seed', 'validation_ppl_mean': statistics.mean(ppls),
               'validation_ppl_sample_sd': statistics.stdev(ppls)}
    tmp = output / 'summary.json.tmp'
    tmp.write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    tmp.replace(output / 'summary.json')
    print(f"Validation PPL (trung bình ± SD mẫu, 5 seed): {summary['validation_ppl_mean']:.4f} ± {summary['validation_ppl_sample_sd']:.4f}")


if __name__ == '__main__':
    main()
