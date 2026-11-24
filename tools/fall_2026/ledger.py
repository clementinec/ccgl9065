"""Maintain the anonymous Fall 2026 exhibition ledger. See README.md."""
import argparse
import csv
import hashlib
import json
import os
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = ROOT / 'data/students_2026_fall_public.json'
PORTFOLIOS = HERE / 'portfolios.csv'
RECEIPTS = HERE / 'reviewed_files.csv'
COMPONENTS = ('collage', 'essay', 'video')
RECEIPT_FIELDS = ('component', 'submission_hash', 'portfolio_id', 'decision')


def fingerprint(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def submission_hash(path):
    # Scope content to its LMS submission so two students can submit identical files.
    match = re.match(r'^(\d+) - ', path.name)
    if not match:
        return None
    return hashlib.sha256(f'{match[1]}:{fingerprint(path)}'.encode()).hexdigest()


def write_csv(path, fields, rows):
    with NamedTemporaryFile('w', dir=path.parent, newline='', encoding='utf-8',
                            delete=False) as stream:
        writer = csv.DictWriter(stream, fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    os.replace(stream.name, path)


def portfolio_rows():
    manifest = json.loads(MANIFEST.read_text())
    rows = []
    for p in manifest['portfolios']:
        row = {'portfolio_id': p['id'], 'title': p['title']}
        for component in COMPONENTS:
            asset = p[component]
            url = asset.get('url')
            if not url:
                value = ''
            elif component == 'essay' and asset.get('text'):
                value = hashlib.sha256(asset['text'].encode()).hexdigest()
            elif url.startswith(('https://', 'http://')):
                value = url
            else:
                value = fingerprint(ROOT / url)
            row[component] = value
        rows.append(row)
    ids = {r['portfolio_id'] for r in rows}
    if len(ids) != len(rows) or len(ids) != manifest['count']:
        raise ValueError('Duplicate portfolio ID or inconsistent manifest count')
    return sorted(rows, key=lambda r: r['portfolio_id'])


def receipts():
    with RECEIPTS.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('sync', help='refresh portfolio coverage from the gallery')
    pending = commands.add_parser('pending', help='list unreviewed files locally')
    record = commands.add_parser('record', help='record one reviewed file')
    for cmd in (pending, record):
        cmd.add_argument('component', choices=COMPONENTS)
        cmd.add_argument('path', type=Path)
    record.add_argument('decision', choices=('imported', 'excluded'))
    record.add_argument('--portfolio', help='anonymous gallery ID for an imported file')
    args = parser.parse_args()
    if args.command == 'sync':
        write_csv(PORTFOLIOS, ('portfolio_id', 'title', *COMPONENTS), portfolio_rows())
        return

    rows = receipts()
    known = {(r['component'], r['submission_hash']) for r in rows}
    if args.command == 'pending':
        if not args.path.is_dir():
            parser.error('Supply an unpacked assignment export directory')
        files = [p for p in sorted(args.path.iterdir()) if p.is_file()
                 and not p.name.startswith('.') and p.name.lower() != 'manifest.txt']
        new = [p for p in files if (args.component, submission_hash(p)) not in known]
        for path in new:
            print(path.name)
        print(f'{len(new)} to review out of {len(files)} files')
        return

    if args.decision == 'imported':
        assets = {r['portfolio_id']: r[args.component] for r in portfolio_rows()}
        if not assets.get(args.portfolio):
            parser.error('Supply a gallery ID with this component present')
    elif args.portfolio:
        parser.error('Omit --portfolio for an excluded file')
    signature = submission_hash(args.path)
    if signature is None:
        parser.error('Expected an LMS filename beginning with a numeric submission ID and " - "')
    receipt = dict(component=args.component, submission_hash=signature,
                   portfolio_id=args.portfolio or '', decision=args.decision)
    if receipt in rows:
        return
    rows.append(receipt)
    write_csv(RECEIPTS, RECEIPT_FIELDS,
              sorted(rows, key=lambda r: (r['component'], r['portfolio_id'], r['submission_hash'])))


if __name__ == '__main__':
    main()
