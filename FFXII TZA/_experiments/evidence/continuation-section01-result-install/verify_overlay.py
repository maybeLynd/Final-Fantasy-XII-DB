#!/usr/bin/env python3
"""Read-only preflight for a SECTION-01 copy/merge. Does not copy or change files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--target',type=Path,required=True,help='Existing FFXII TZA database folder, not its parent.')
    args=ap.parse_args()
    target=args.target.resolve()
    if not target.is_dir(): ap.error('Target folder does not exist')
    manifest=json.loads((Path(__file__).parent/'PATCH_MANIFEST.json').read_text(encoding='utf-8'))
    results=[]
    for row in manifest['files']:
        p=(target/row['path']).resolve()
        if not p.is_relative_to(target): raise ValueError('Unsafe manifest path')
        got=digest(p) if p.is_file() else None
        if got==row['updated_sha256']: status='ALREADY_UPDATED'
        elif row['original_sha256'] is not None and got==row['original_sha256']: status='BASE_MATCH'
        elif row['original_sha256'] is None and got is None and not p.exists(): status='NEW_FILE'
        else: status='CONFLICT'
        results.append({'path':row['path'],'status':status,'current_sha256':got})
    conflicts=[r for r in results if r['status']=='CONFLICT']
    print(json.dumps({'target':str(target),'conflicts':len(conflicts),'files':results,
                      'action':'Merge conflicting local changes; do not blindly overwrite.' if conflicts else 'All listed files are at the baseline, already updated, or new. Merge folders; do not delete unlisted files.',
                      'note':'PATCH_MANIFEST.json excludes itself to avoid recursive hashing.'},indent=2))
    return 1 if conflicts else 0


if __name__=='__main__':
    try: raise SystemExit(main())
    except (OSError,ValueError,KeyError) as exc: raise SystemExit(f'Overlay preflight failed: {exc}')
