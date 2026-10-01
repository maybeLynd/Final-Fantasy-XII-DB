#!/usr/bin/env python3
"""Content/extent/source-preservation checks. Requires PyYAML; not needed for install."""
from __future__ import annotations
import argparse,ast,csv,hashlib,json,re
from pathlib import Path
from urllib.parse import unquote
import yaml
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--database',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    db=a.database.resolve();base=a.baseline.resolve();modified=json.loads((HERE/'modified_paths.json').read_text())
    new=json.loads((HERE/'new_mechanism_path.json').read_text())['path'];docs=[db/x for x in modified+[new] if x.endswith('.md')]+[HERE/'REVIEW.md']
    front=[];links=[];external=[]
    for file in docs:
        text=file.read_text()
        if text.startswith('---'):
            data=yaml.safe_load(text.split('---',2)[1]);front.append(file.relative_to(db).as_posix())
            old=base/file.relative_to(db)
            if old.exists() and old.read_text().startswith('---'):
                oldfm=old.read_text().split('---',2)[1]
                # Strict parser may not accept old unquoted provenance. Compare historical audit text directly.
                if 'audit:' in oldfm and oldfm[oldfm.index('audit:'):].split('local_production_date:')[0].strip()!=text.split('---',2)[1].split('local_production_date:')[0].split('audit:',1)[1].join(['audit:','']).strip():
                    raise AssertionError('historical audit block changed: '+str(file))
        if file.name.startswith('CONTRACT-'):
            nums=set(re.findall(r'^## (\d+)\. ',text,re.M))
            if not {str(i) for i in range(1,17)}<=nums:raise AssertionError('contract sections '+str(file))
        for match in re.finditer(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)',text):
            href=match.group(1).strip().strip('<>')
            if href.startswith(('http:','https:','mailto:','#')):continue
            relative=unquote(href.split('#',1)[0]);t=(file.parent/relative).resolve()
            if not t.is_relative_to(db):external.append({'source':str(file.relative_to(db)),'link':href,'status':'OUTSIDE_DATABASE_NOT_VALIDATED'});continue
            if not t.is_file():raise AssertionError(f'broken local file link: {file}: {href}')
            links.append({'source':str(file.relative_to(db)),'link':href})
    targets={'VmValueStack':0x284,'ActorWaitSlot':0x28};layout=[]
    fr=list(csv.DictReader((db/'_types/fields.tsv').open(),delimiter='\t'))
    for name,size in targets.items():
        rows=[r for r in fr if r['type']==name];seen=[0]*size
        for r in rows:
            lo=int(r['offset'],16);n=int(r['size'],0)
            if lo<0 or lo+n>size:raise AssertionError('extent bound')
            for i in range(lo,lo+n):seen[i]+=1
        if any(x!=1 for x in seen):raise AssertionError('gap/overlap '+name)
        layout.append({'type':name,'size':size,'rows':len(rows),'gaps':0,'overlaps':0})
    for fn in ['types.tsv','fields.tsv']:
        def unrelated(path):return [line for line in path.read_bytes().splitlines(keepends=True) if not any(line.startswith((k+'\t').encode()) for k in targets)]
        if unrelated(db/'_types'/fn)!=unrelated(base/'_types'/fn):raise AssertionError('unrelated TSV lines changed')
    syntax=[]
    for path in HERE.glob('*.py'):ast.parse(path.read_text());syntax.append(path.name)
    # All historical files outside the exact replacements must remain byte-identical.
    unchanged=[]
    for pth in base.rglob('*'):
        if pth.is_file():
            rel=pth.relative_to(base).as_posix()
            if rel not in modified:
                if sha(pth)!=sha(db/rel):raise AssertionError('unrelated file changed: '+rel)
                unchanged.append(rel)
    result={'status':'PASS','yaml_blocks':len(front),'local_file_links':len(links),'external_links_unvalidated':external,
            'anchor_fragments':'not independently validated; file targets checked','layouts':layout,'unrelated_tsv_lines_identical':True,'python_syntax':syntax,'unrelated_files_identical':len(unchanged)}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    (a.output.parent/'unchanged_files.json').write_text(json.dumps({'count':len(unchanged),'method':'Full before/after SHA256 on every baseline file except the ten listed replacements.','files':unchanged},indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
