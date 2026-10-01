#!/usr/bin/env python3
"""Read-only overlay preflight. Never writes, merges, deletes or fixes target files."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def inspect(target: Path, entries: list[dict]) -> dict:
    if not target.is_dir():raise ValueError('target must be the existing FFXII TZA directory')
    records=[]
    for row in entries:
        rel=PurePosixPath(row['path'])
        if rel.is_absolute() or '..' in rel.parts or '\\' in row['path']:
            raise ValueError('unsafe manifest path')
        p=target.joinpath(*rel.parts)
        if any(q.is_symlink() for q in [p,*p.parents] if q!=target.parent):
            status='CONFLICT_SYMLINK'
        elif not p.exists():
            status='NEW_FILE' if row['before_sha256'] is None else 'MISSING_BASE'
        elif not p.is_file():status='CONFLICT_NOT_FILE'
        else:
            actual=sha(p)
            status=('ALREADY_UPDATED' if actual==row['after_sha256'] else
                    'READY_TO_REPLACE' if actual==row['before_sha256'] else 'CONFLICT_NEWER_OR_DIFFERENT')
        records.append({'path':row['path'],'status':status})
    good={'NEW_FILE','READY_TO_REPLACE','ALREADY_UPDATED'}
    return {'compatible':all(r['status'] in good for r in records),'files':records,'read_only':True,
            'notice':'A conflict needs merging. Do not overwrite newer peer work. This check does not modify files.'}

def main() -> None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--target',type=Path,required=True)
    a=p.parse_args();m=json.loads(Path(__file__).with_name('PATCH_MANIFEST.json').read_text())
    out=inspect(a.target,m['files']);print(json.dumps(out,indent=2));raise SystemExit(0 if out['compatible'] else 1)
if __name__=='__main__':main()
