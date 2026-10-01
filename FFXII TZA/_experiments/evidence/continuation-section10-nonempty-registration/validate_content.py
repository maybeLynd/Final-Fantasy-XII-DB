#!/usr/bin/env python3
"""Read-only Section10 content/link/assertion check. Not semantic or L2 acceptance."""
from __future__ import annotations
import argparse,ast,csv,hashlib,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
import yaml
HERE=Path(__file__).resolve().parent
MECHANISM='02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--database',type=Path,required=True);a=ap.parse_args();db=a.database.resolve(strict=True)
 post=json.loads((HERE/'canonical_postimages.json').read_text())
 for name,h in post.items():
  if sha(db/name)!=h:raise ValueError('Changed canonical output: '+name)
 names=json.loads((HERE/'canonical_preimages.json').read_text())
 docs=[db/n for n in names]+[db/MECHANISM]+sorted(HERE.glob('*.md'))
 links=[];ext=[];pages=[]
 for p in docs:
  s=p.read_text(encoding='utf-8')
  if s.startswith('---\n'):
   end=s.index('\n---',4);m=yaml.safe_load(s[4:end])
   if m.get('external_production',{}).get('section')!='SECTION-10':raise ValueError('Stale production metadata: '+str(p))
  body=re.sub(r'```.*?```','',s,flags=re.S)
  for raw in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',body):
   target=raw.strip().split(' "',1)[0].strip('<>')
   if urlsplit(target).scheme or target.startswith('#'):continue
   q=(p.parent/unquote(target.split('#',1)[0])).resolve();row=dict(source=str(p.relative_to(db)),target=target,exists=q.is_file())
   if not q.is_relative_to(db):ext.append(row)
   else:
    links.append(row)
    if not q.is_file():raise ValueError('Broken local file link: '+json.dumps(row))
  pages.append(str(p.relative_to(db)))
 rec=json.loads((HERE/'results/native_baseline.json').read_text());rep=json.loads((HERE/'results/native_repeat.json').read_text())
 assert rec==rep and rec['checks']==159 and rec['failures']==0
 cn={r['name'] for r in rec['cases']};assert len(cn)==159 and all(r['pass'] and r['actual']==r['expected'] for r in rec['cases'])
 vs=json.loads((HERE/'variant_plan.json').read_text());vn={v['variant'] for v in vs}
 outcomes=json.loads((HERE/'results/code_mutations.json').read_text());assert len(outcomes)==len(vs)==8
 for x in outcomes:
  assert x['rejected'] and [r['name'] for r in x['record']['cases'] if not r['pass']]==[x['required_failure']]
 claims=list(csv.DictReader((HERE/'claim_matrix.tsv').open(),delimiter='\t'))
 for x in claims:
  assert set(x['assertions'].split(';'))<=cn
  if x['affected_mutations']:assert set(x['affected_mutations'].split(';'))<=vn
 jf=list(HERE.rglob('*.json'))
 for p in jf:json.loads(p.read_text())
 pf=list(HERE.glob('*.py'))
 for p in pf:ast.parse(p.read_text(),str(p))
 print(json.dumps(dict(section='SECTION-10',status='PASS',read_only=True,canonical_hashes=len(post),documents=pages,database_local_links_checked=len(links),broken_database_local_links=[],external_links=ext,native_assertions=159,mutants=8,claim_groups=len(claims),json_files=len(jf),python_files=len(pf),links=links,limits='File/metadata/assertion consistency; not independent semantic acceptance. Fragment anchors and external absent tools are not certified.'),indent=2))
if __name__=='__main__':
 try:main()
 except (OSError,ValueError,KeyError,AssertionError,yaml.YAMLError) as e:print('Section10 validation failed: '+str(e),file=sys.stderr);raise SystemExit(2)
