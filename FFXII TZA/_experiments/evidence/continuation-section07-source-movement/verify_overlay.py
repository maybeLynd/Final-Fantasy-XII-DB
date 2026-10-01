#!/usr/bin/env python3
"""Read-only preflight for the Section 07 changed-files overlay (Python 3.10+).

Pass --target the existing FFXII TZA directory, not its parent. No files are written.
Exit 0: all replacements match expected preimages/already-applied output and new
files are absent/already applied. Exit 1: conflicts. Exit 2: invalid input.
This checks exact bytes, not the correctness of any research claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

HERE = Path(__file__).resolve().parent

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def classify(target: Path, row: dict) -> dict:
    name = row['path']
    pure = PurePosixPath(name)
    if not isinstance(name, str) or '\\' in name or pure.is_absolute() or '..' in pure.parts:
        raise ValueError(f'Unsafe manifest path: {name!r}')
    candidate = target.joinpath(*pure.parts)
    if not candidate.resolve().is_relative_to(target):
        raise ValueError(f'Path escapes target: {name}')
    before, after = row['before_sha256'], row['after_sha256']
    current = digest(candidate) if candidate.is_file() else None
    if candidate.exists() and not candidate.is_file():
        state = 'conflict_nonfile'
    elif current == after:
        state = 'already_applied'
    elif current is None and before is None:
        state = 'new_file'
    elif before is not None and current == before:
        state = 'expected_preimage'
    else:
        state = 'conflict'
    return {'path': name, 'state': state, 'expected_before': before,
            'expected_after': after, 'actual_sha256': current}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, default=HERE / 'PATCH_MANIFEST.json')
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.is_dir():
        raise ValueError('Target must be the existing FFXII TZA directory')
    manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
    paths = [row['path'] for row in manifest['files']]
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate manifest paths')
    rows = [classify(target, row) for row in manifest['files']]
    conflicts = [row for row in rows if row['state'].startswith('conflict')]
    print(json.dumps({'section': manifest['section'], 'read_only': True,
        'target': str(target), 'compatible': not conflicts, 'conflicts': len(conflicts),
        'files': rows, 'note': 'Merge newer local edits; do not blindly replace conflicts. '
        'The manifest itself has no self-hash.'}, indent=2))
    return 1 if conflicts else 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Overlay check error: {exc}', file=sys.stderr)
        raise SystemExit(2)
