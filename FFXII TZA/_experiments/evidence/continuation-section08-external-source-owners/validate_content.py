#!/usr/bin/env python3
"""Validate this overlay's documents/new type without claiming whole-database acceptance.

Usage: python validate_content.py --database '/path/to/FFXII TZA'
Python 3.10+ and PyYAML are required. The tool only reads files and prints JSON.
"""
from __future__ import annotations
import argparse
import ast
import csv
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
TYPE = 'IndexedExternalSourceRequest'
NEW = '02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md'

def rows(path: Path) -> list[dict]:
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def validate(database: Path) -> dict:
    import yaml
    database = database.resolve()
    if not database.is_dir():
        raise ValueError('The database directory does not exist')
    pre = json.loads((HERE/'canonical_preimages.json').read_text())
    docs = [database/p for p in pre if p.endswith('.md')]
    docs += [database/NEW, HERE/'REVIEW.md', HERE/'README.md']
    frontmatter = []
    contracts = []
    links = []
    unavailable = []
    broken = []
    for doc in docs:
        text = doc.read_text(encoding='utf-8')
        if text.startswith('---\n'):
            fm = yaml.safe_load(text.split('---\n', 2)[1])
            if not isinstance(fm, dict):
                raise ValueError(f'Frontmatter must be an object: {doc}')
            frontmatter.append(str(doc.relative_to(database)))
            if fm.get('contract'):
                sections = [int(x) for x in re.findall(r'^##\s+(\d+)\.', text, re.M)]
                if sections[:16] != list(range(1,17)):
                    raise ValueError(f'The existing numbered contract structure changed: {doc}')
                contracts.append(str(doc.relative_to(database)))
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text):
            target = target.strip().strip('<>')
            if target.startswith(('#','https://','http://','mailto:')):
                continue
            # These documents use plain file destinations, not Markdown title strings.
            target = unquote(target.split('#',1)[0])
            if not target:
                continue
            dest = (doc.parent/target).resolve()
            item = {'document':str(doc.relative_to(database)), 'target':target}
            if dest.is_file():
                links.append(item)
            elif not dest.is_relative_to(database) and 'Tools/' in dest.as_posix():
                unavailable.append(item)
            else:
                broken.append(item)
    if broken:
        raise ValueError('Broken database/evidence links: '+json.dumps(broken))
    tr = [r for r in rows(database/'_types/types.tsv') if r['type']==TYPE]
    fr = [r for r in rows(database/'_types/fields.tsv') if r['type']==TYPE]
    if len(tr)!=1 or len(fr)!=9 or int(tr[0]['size'],0)!=0x1C:
        raise ValueError('Unexpected new type population or extent')
    if tr[0]['readiness']!='SIGNATURE RESOLVED':
        raise ValueError('Do not silently promote this new type')
    expected=json.loads((HERE/'canonical_type_addition.json').read_text())
    headers_t=list(rows(database/'_types/types.tsv')[0])
    headers_f=list(rows(database/'_types/fields.tsv')[0])
    if [tr[0][k] for k in headers_t]!=expected['type_row']:
        raise ValueError('Canonical type differs from the declared addition')
    if [[r[k] for k in headers_f] for r in fr]!=expected['field_rows']:
        raise ValueError('Canonical fields differ from the declared addition')
    intervals=sorted((int(r['offset'],0),int(r['size'])) for r in fr)
    end=0
    for start,size in intervals:
        if start!=end or size<=0:
            raise ValueError('New type has an unexpected gap/overlap')
        end=start+size
    if end!=0x1C:
        raise ValueError('New layout does not cover its extent')
    # Exact old bytes can be recovered by removing only this new type's lines.
    import hashlib
    unrelated=[]
    for rel in ['_types/types.tsv','_types/fields.tsv']:
        b=(database/rel).read_bytes()
        old=b''.join(line for line in b.splitlines(keepends=True)
                     if not line.startswith((TYPE+'\t').encode()))
        got=hashlib.sha256(old).hexdigest()
        if got!=pre[rel]:
            raise ValueError('An unrelated existing type/field line changed: '+rel)
        unrelated.append({'file':rel,'original_bytes_recovered':True,'sha256':got})
    scripts=[]
    for path in sorted(HERE.glob('*.py')):
        ast.parse(path.read_text(),filename=path.name)
        scripts.append(path.name)
    return {'section':'SECTION-08','status':'PASS','read_only':True,
            'strict_frontmatter_files':frontmatter,'contracts_with_16_sections':contracts,
            'existing_file_links':len(links),'unavailable_external_tool_links':unavailable,
            'broken_local_links':broken,'new_types':1,'new_fields':9,
            'new_type_extent':'0x1C','gap_or_overlap':False,
            'unrelated_type_field_bytes':unrelated,'python_sources_parsed':scripts,
            'limits':'Content/shape validation only, not semantic peer acceptance or every anchor check.'}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(validate(args.database),indent=2))
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError,ValueError,KeyError,TypeError,ImportError) as exc:
        print(f'Content check failed: {exc}',file=sys.stderr)
        raise SystemExit(2)
