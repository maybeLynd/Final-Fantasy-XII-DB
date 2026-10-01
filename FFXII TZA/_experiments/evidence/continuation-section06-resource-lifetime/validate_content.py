#!/usr/bin/env python3
"""Read-only Section06 canonical-content verification. Requires supplied PyYAML.

--preimages and --baseline-hashes are optional audit inputs retained by the producer.
Without them, validates current content, links, schemas, declared layout and pinned
output hashes (when PATCH_MANIFEST exists). It never changes the database.
Writes only the explicitly selected --output JSON file.
"""
from __future__ import annotations
import argparse, ast, hashlib, json, re, sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
import yaml
HERE=Path(__file__).resolve().parent
TARGETS={'EfxCallerTemplate','RenderResourceEntry','RenderResourceEntryBuffer'}
NEW_PAGE='02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def table(p):
    raw=p.read_bytes(); lines=raw.decode('utf-8').splitlines()
    header=lines[0].split('\t'); rows=[]
    for n,line in enumerate(lines[1:],2):
        if not line: continue
        parts=line.split('\t')
        if len(parts)!=len(header): raise ValueError(f'{p.name}:{n}: nonrectangular row')
        rows.append(dict(zip(header,parts)))
    return rows

def run(db:Path,pre:Path|None,base:Path|None):
    out={'section':'SECTION-06','read_only':True,'errors':[]};errors=out['errors']
    pre_records=json.loads((HERE/'canonical_preimages.json').read_text())
    changed=[r['path'] for r in pre_records];md=[db/p for p in changed if p.endswith('.md')]+[db/NEW_PAGE,HERE/'README.md',HERE/'REVIEW.md']
    links=[];frontmatter=[];external=[]
    pending={'results/content_validation.json'}
    for p in md:
        text=p.read_text(encoding='utf-8')
        if text.startswith('---\n'):
            try:
                data=yaml.safe_load(text.split('---',2)[1]);assert isinstance(data,dict)
                frontmatter.append({'path':str(p.relative_to(db)),'valid':True})
            except Exception as exc: errors.append(f'{p.name}: frontmatter {exc}')
        for match in re.finditer(r'\[[^\]\n]*\]\(([^\)\n]+)\)',text):
            u=match.group(1).strip().strip('<>'); parsed=urlsplit(u)
            if parsed.scheme or not parsed.path: continue
            # Inline Markdown file links only; section anchors not certified.
            name=unquote(parsed.path);dest=(p.parent/name).resolve()
            planned=(p.parent==HERE and name in pending)
            if not dest.is_relative_to(db):
                external.append({'source':str(p.relative_to(db)),'target':u,'available':dest.exists(),'scope':'inherited external reference; not shipped or validated'})
                continue
            exists=dest.exists() or planned
            links.append({'source':str(p.relative_to(db)),'target':u,'exists':exists})
            if not exists:errors.append(f'{p.name}: broken file link {u}')
    out['frontmatter']=frontmatter;out['markdown_file_links']=links;out['external_file_references']=external
    types=table(db/'_types/types.tsv');fields=table(db/'_types/fields.tsv')
    tmap={r['type']:r for r in types};out['target_layouts']=[]
    for name in sorted(TARGETS):
        size=int(tmap[name]['size'],0);mask=bytearray(size);chosen=[r for r in fields if r['type']==name]
        for r in chosen:
            a=int(r['offset'],0);n=int(r['size'],0)
            if a<0 or a+n>size:errors.append(f'{name}:out-of-bounds {a}+{n}');continue
            for i in range(a,a+n):mask[i]+=1
        gaps=sum(x==0 for x in mask);overlap=sum(x>1 for x in mask)
        out['target_layouts'].append({'type':name,'size':size,'fields':len(chosen),'gap_bytes':gaps,'overlap_bytes':overlap})
        if gaps or overlap:errors.append(f'{name}: gaps/overlaps')
    assert tmap['RenderResourceEntryBuffer']['size']=='0x20'
    assert len([r for r in fields if r['type'] in TARGETS])==41
    opaque=[r for r in fields if r['type']=='RenderResourceEntryBuffer' and int(r['offset'],0) in (4,28)]
    assert len(opaque)==2 and all(r['confidence']=='UNKNOWN' for r in opaque)
    contract=db/'02-Resource-And-Asset-Pipeline/CONTRACT-resource-input-ownership.md'
    numbers=[int(x) for x in re.findall(r'^## (\d+)\.',contract.read_text(),re.M)]
    assert numbers==list(range(1,17));out['ownership_contract_sections']=numbers
    out['python_parse']=[]
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text());out['python_parse'].append(p.name)
    out['json_parse']=[]
    for p in HERE.rglob('*.json'):
        json.loads(p.read_text());out['json_parse'].append(str(p.relative_to(HERE)))
    if pre:
        unchanged={}
        for r in pre_records:
            if sha(pre/r['path'])!=r['sha256']:errors.append('wrong preimage '+r['path'])
        for filename in ['types.tsv','fields.tsv']:
            a=(pre/'_types'/filename).read_bytes().splitlines(keepends=True);b=(db/'_types'/filename).read_bytes().splitlines(keepends=True)
            def unrelated(lines):return [l for l in lines if l.split(b'\t',1)[0].decode('utf-8').strip() not in TARGETS]
            assert unrelated(a)==unrelated(b),(filename,'unrelated TSV line changed')
            unchanged[filename]={'byte_identical_non_target_lines':len(unrelated(a))}
        out['unrelated_tsv_preservation']=unchanged
    if base:
        source=json.loads(base.read_text());unexpected=[];same=0
        for name,digest in source.items():
            p=db/name
            if not p.is_file():unexpected.append({'path':name,'error':'missing'})
            elif sha(p)==digest:same+=1
            elif name not in changed:unexpected.append({'path':name,'error':'unexpected modification'})
        out['baseline_files']=len(source);out['unchanged_baseline_files']=same;out['unexpected_baseline_changes']=unexpected
        if unexpected:errors.append('Unexpected baseline changes')
        assert same==len(source)-len(changed)
    manifest=HERE/'PATCH_MANIFEST.json'
    if manifest.exists():
        records=json.loads(manifest.read_text())['files'];checked=0
        for r in records:
            # This report is generated by the check and pinned at final packaging.
            if r['path'].endswith('/results/content_validation.json'):continue
            if sha(db/r['path'])!=r['after_sha256']:errors.append('manifest mismatch '+r['path'])
            checked+=1
        out['manifest_output_hashes_checked']=checked
    out['passed']=not errors
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--database',required=True,type=Path);p.add_argument('--preimages',type=Path);p.add_argument('--baseline-hashes',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    report=run(a.database.resolve(),a.preimages,a.baseline_hashes)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':report['passed'],'errors':report['errors'],'file_links':len(report['markdown_file_links']),'layouts':report['target_layouts']},indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':
    try:raise SystemExit(main())
    except (AssertionError,ValueError,OSError,KeyError,SyntaxError) as exc:
        print(f'Content check failed: {exc}',file=sys.stderr);raise SystemExit(2)
