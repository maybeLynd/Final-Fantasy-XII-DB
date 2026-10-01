#!/usr/bin/env python3
"""Read-only selected-document/type validation; output is a separate receipt if requested.
Requires Python3.10+ and PyYAML. Does not certify semantics or global database completion.
"""
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path
from urllib.parse import unquote
import yaml
HERE=Path(__file__).resolve().parent

def records(path:Path)->list[dict]:
    lines=path.read_bytes().decode('utf-8').split('\n')
    headers=lines[0].rstrip('\r').split('\t');out=[]
    for line in lines[1:]:
        if not line:continue
        cells=line.rstrip('\r').split('\t')
        if len(cells)!=len(headers):raise ValueError(f'Nonrectangular target store {path}')
        out.append(dict(zip(headers,cells)))
    return out

def check(database:Path)->dict:
    database=database.resolve(strict=True)
    paths=json.loads((HERE/'modified_paths.json').read_text())+[json.loads((HERE/'new_mechanism_path.json').read_text())]
    docs=[database/p for p in paths if p.endswith('.md')]+[HERE/'REVIEW.md',HERE/'README.md']
    # Receipts are checked for existence, not considered semantic evidence merely because linked.
    links=[];front=[]
    for path in docs:
        text=path.read_text()
        if text.startswith('---\n'):
            parsed=yaml.safe_load(text.split('---',2)[1]);
            if not isinstance(parsed,dict):raise ValueError('Frontmatter is not a mapping')
            front.append({'path':str(path.relative_to(database)) if path.is_relative_to(database) else path.name,'pass':True})
        for m in re.finditer(r'\[[^\]\n]*\]\(([^)\n]+)\)',text):
            link=m[1].strip().strip('<>')
            if not link or link.startswith(('#','http:','https:','mailto:')):continue
            target=unquote(link.split('#',1)[0]);p=(path.parent/target).resolve()
            status='EXISTS' if p.exists() else ('EXTERNAL_NOT_SUPPLIED' if not p.is_relative_to(database) else 'MISSING')
            links.append({'source':str(path.relative_to(database)) if path.is_relative_to(database) else path.name,'target':link,'status':status})
    missing=[x for x in links if x['status']=='MISSING']
    if missing:raise ValueError('Missing database-local links: '+json.dumps(missing))
    t=records(database/'_types/types.tsv');f=records(database/'_types/fields.tsv')
    expected=json.loads((HERE/'canonical_row_changes.json').read_text());rowchecks=[]
    for x in expected:
        table=t if x['table']=='types.tsv' else f;a=x['after']
        match=[r for r in table if r['type']==a['type'] and ('offset' not in a or r['offset']==a['offset'])]
        if match!=[a]:raise ValueError('Current row differs from delivered claim '+a['type'])
        rowchecks.append({'table':x['table'],'type':a['type'],'offset':a.get('offset'),'pass':True})
    layouts=[]
    for name in ('ActorResourceEntry','ActorWaitSlot'):
        size=int(next(r['size'] for r in t if r['type']==name),0);cover=[0]*size
        rows=[r for r in f if r['type']==name]
        for r in rows:
            off=int(r['offset'],0);n=int(r['size'],0)
            if off<0 or off+n>size:raise ValueError('Extent overflow')
            for j in range(off,off+n):cover[j]+=1
        if any(v!=1 for v in cover):raise ValueError('Target type has gap/overlap')
        layouts.append({'type':name,'size':size,'rows':len(rows),'exact_coverage':True})
    return {'status':'PASS','frontmatter':front,'links':links,'local_file_links':sum(x['status']=='EXISTS' for x in links),'external_not_supplied':[x for x in links if x['status']=='EXTERNAL_NOT_SUPPLIED'],'row_changes_checked':rowchecks,'layouts':layouts,'semantics_certified':False}

def main()->None:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--database',required=True,type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    result=check(a.database);text=json.dumps(result,indent=2)+'\n'
    if a.output:
        if a.output.exists():raise SystemExit('Output exists; choose a new receipt path')
        a.output.write_text(text)
    print(text)
if __name__=='__main__':main()
