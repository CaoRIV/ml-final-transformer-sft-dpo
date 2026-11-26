"""Chuẩn bị input Kaggle; không đăng nhập, upload hay cấp quyền cho nguồn."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / '.cache' / 'd3-kaggle'
sys.path.insert(0, str(ROOT))


def package(files, name):
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, 'w') as zf:
        for path, content in files.items():
            entry = zipfile.ZipInfo(path, date_time=(2020, 1, 1, 0, 0, 0))
            zf.writestr(entry, content, compress_type=zipfile.ZIP_DEFLATED)
    blob = archive.getvalue()
    digest = hashlib.sha256(blob).hexdigest()
    DEST.mkdir(parents=True, exist_ok=True)
    out = DEST / f'{name}-{digest[:12]}.zip'
    if not out.exists():
        with out.open('xb') as f:
            f.write(blob)
    elif out.read_bytes() != blob:
        raise ValueError(f'Gói đã tồn tại với nội dung khác: {out.name}')
    print(f'{out.relative_to(ROOT)}  sha256={digest}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path, help='Thư mục mới đã được lệnh check D.2 phát hành')
    parser.add_argument('--allow-private-kaggle', metavar='MANIFEST_SHA256', help='Chỉ điền hash release sau khi nhóm cho phép đưa đúng bản lên Kaggle Private')
    args = parser.parse_args()
    if bool(args.release) != bool(args.allow_private_kaggle):
        parser.error('Gói QA cần cả --release và --allow-private-kaggle MANIFEST_SHA256.')
    if args.release:
        from src.d3_data import load_release
        manifest, _ = load_release(args.release)
        payload = {name: (args.release / name).read_bytes() for name in ('manifest.json', 'train.jsonl', 'validation.jsonl')}
        identity = hashlib.sha256(payload['manifest.json']).hexdigest()
        if (identity != args.allow_private_kaggle or json.loads(payload['manifest.json']) != manifest
                or any(hashlib.sha256(payload[key]).hexdigest() != manifest['files'][key] for key in ('train.jsonl', 'validation.jsonl'))):
            parser.error('Phiên bản dữ liệu không khớp bản được phép đưa lên Kaggle.')
        print('MANIFEST_SHA256 =', identity)
        package(payload, 'd3-release')
    else:
        names = ['requirements-d3.txt', 'scripts/train_d3_sft.py', 'src/d3_data.py']
        package({name: (ROOT / name).read_bytes() for name in names}, 'd3-code')


if __name__ == '__main__':
    main()
