#!/usr/bin/env python3
"""Read-only Section09 content/row/link validation; not semantic or L2 acceptance.
Python3.10+ and PyYAML. --database names the merged FFXII TZA directory.
Results are printed to stdout; this checker never rewrites the database.
"""
from __future__ import annotations
import argparse,ast,csv,hashlib,io,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
import yaml
HERE=Path(__file__).resolve().parent
TARGET='IndexedExternalSourceRequest'
MECHANISM='02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md'

def digest(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def parse_rows(path:Path)->list[dict]:
    text=path.read_text(encoding='utf-8-sig')
    reader=csv.DictReader(io.StringIO(text),delimiter='\t')
    result=list(reader)
    if any(None in r or any(v is None for v in r.values()) for r in result):
        raise ValueError(f'Nonrectangular selected TSV: {path}')
    return result

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--database',type=Path,required=True)
    args=ap.parse_args();db=args.database.resolve(strict=True)
    pre=json.loads((HERE/'canonical_preimages.json').read_text());rowmap=json.loads((HERE/'canonical_row_changes.json').read_text())
    docs=[db/x for x in pre if x.endswith('.md')]+[db/MECHANISM]+sorted(HERE.glob('*.md'))
    documents=[];links=[];external=[];failures=[]
    for p in docs:
        if not p.is_file():raise ValueError(f'Missing expected document: {p}')
        text=p.read_text()
        if text.startswith('---\n'):
            end=text.find('\n---',4)
            if end<0:raise ValueError(f'Missing frontmatter end: {p}')
            fm=yaml.safe_load(text[4:end])
            if not isinstance(fm,dict):raise ValueError(f'Nonmapping frontmatter: {p}')
            if fm.get('external_production',{}).get('section')!='SECTION-09':raise ValueError(f'Stale touched production metadata: {p}')
        if p.name.startswith('CONTRACT-'):
            headings=[int(x) for x in re.findall(r'^## (\d+)\.',text,re.M)]
            if headings!=list(range(1,17)):raise ValueError(f'Contract structure differs: {p}: {headings}')
        # Fenced code is not a link inventory. Relative file links only; anchors are not independently checked.
        body=re.sub(r'```.*?```','',text,flags=re.S)
        for raw in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',body):
            target=raw.strip().split(' "',1)[0].strip('<>')
            if urlsplit(target).scheme or target.startswith('#'):continue
            part=unquote(target.split('#',1)[0])
            if not part:continue
            q=(p.parent/part).resolve()
            rec={'from':str(p.relative_to(db)) if p.is_relative_to(db) else p.name,'target':target,'exists':q.is_file()}
            if not q.is_relative_to(db):external.append(rec)
            else:
                links.append(rec)
                if not q.is_file():failures.append(rec)
        documents.append({'path':str(p.relative_to(db)) if p.is_relative_to(db) else p.name,'strict_frontmatter':text.startswith('---\n')})
    if failures:raise ValueError('Broken database-local links: '+json.dumps(failures))
    comparisons={}
    for rel,key in [('_types/types.tsv','types_after'),('_types/fields.tsv','fields_after')]:
        p=db/rel;raw=p.read_bytes();rows=parse_rows(p);selected=[r for r in rows if r['type']==TARGET]
        if selected!=rowmap[key]:raise ValueError(f'Unexpected current type rows: {rel}')
        unrelated=b''.join(l for l in raw.splitlines(keepends=True) if not l.startswith((TARGET+'\t').encode()))
        if digest(unrelated)!=rowmap['unrelated_sha256'][rel]:raise ValueError(f'Unrelated TSV bytes changed: {rel}')
        comparisons[rel]={'target_rows':len(selected),'unrelated_bytes_identical':True}
    types=rowmap['types_after'];fields=rowmap['fields_after']
    if len(types)!=1 or types[0]['size']!='0x1C' or types[0]['readiness']!='SIGNATURE RESOLVED' or len(fields)!=10:raise ValueError('Type size/readiness/count drift')
    pos=0
    for r in sorted(fields,key=lambda r:int(r['offset'],0)):
        if int(r['offset'],0)!=pos:raise ValueError('Target type gap or overlap')
        pos+=int(r['size'],0)
    if pos!=0x1C:raise ValueError('Target field extent differs')
    a=json.loads((HERE/'results/native_baseline.json').read_text());b=json.loads((HERE/'results/native_repeat.json').read_text())
    if a!=b or a['checks']!=190 or len(a['cases'])!=190 or a['failures'] or not all(r['pass'] and r['actual']==r['expected'] for r in a['cases']):raise ValueError('Invalid baseline/repeat')
    names={r['name'] for r in a['cases']}
    if len(names)!=190:raise ValueError('Duplicate case names')
    variants=json.loads((HERE/'variant_plan.json').read_text());variant_names={r['variant'] for r in variants}
    for row in parse_rows(HERE/'claim_matrix.tsv'):
        if not set(row['assertions'].split(';'))<=names:raise ValueError(f'Claim references absent assertion: {row["claim"]}')
        if row['affected_mutations'] and not set(row['affected_mutations'].split(';'))<=variant_names:raise ValueError('Unknown claim mutation')
    mutation_results=json.loads((HERE/'results/code_mutations.json').read_text())
    if len(mutation_results)!=10 or not all(x['rejected'] for x in mutation_results):raise ValueError('Mutation failures incomplete')
    json_files=[]
    for p in sorted(HERE.rglob('*.json')):
        json.loads(p.read_text());json_files.append(str(p.relative_to(HERE)))
    py_files=[]
    for p in sorted(HERE.glob('*.py')):
        ast.parse(p.read_text(),filename=str(p));py_files.append(p.name)
    print(json.dumps({'section':'SECTION-09','status':'PASS','read_only':True,'scope':'Touched canonical files plus this section evidence only; no semantic/peer acceptance implied.','documents':documents,'database_local_links_checked':len(links),'broken_database_local_links':[],'external_links':external,'type_checks':comparisons,'target_layout_bytes':pos,'target_layout_gaps_or_overlaps':0,'native_assertions_verified':190,'claim_groups':7,'strict_json_files':len(json_files),'python_files_parsed':len(py_files),'links':links},indent=2))
    return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,KeyError,TypeError,yaml.YAMLError) as exc:
        print('Section09 content validation failed: '+str(exc),file=sys.stderr);raise SystemExit(2)
