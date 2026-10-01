"""Normalize retained UI/HTTP bytes only; never repeats capture after schema error."""
import argparse,hashlib,json,re
from pathlib import Path
W=Path(__file__).resolve().parent;D=W/'deployed-01';O=W/'deployed-ui-02'
ap=argparse.ArgumentParser();ap.add_argument('--progress',type=Path,default=O/'progress.json');ap.add_argument('--out',type=Path,default=O/'normalized.json');a=ap.parse_args()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((O/'raw.json').read_text())
assert r['finished'] is False and r['fatal']['type']=='KeyError' and r['fatal']['reason']=="'key'"
assert sha(W/'browser-receipt.py')==r['driver_sha256'],'Keep original failed driver'
for x in r['requests']:assert sha(O/(x['name']+'.json'))==x['sha256']
for n,v in r['files'].items():assert sha(D/n)==v['sha256'] and (D/n).stat().st_size==v['bytes']
ax=(D/'browser-expanded.txt').read_text();ids=re.findall(r'text ((?:DA|DD):[^\r\n]+)',ax)
assert len(ids)==len(set(ids))==16
p=json.loads(a.progress.read_text());c=next(x for x in p['view']['progress']['categories'] if x['code']=='W')
assert len(c['items'])==16 and all(isinstance(x.get('k'),str) and x['k'] for x in c['items']), 'Missing/empty original item k is not valid empty output'
assert set(ids)=={x['k'] for x in c['items']}
assert (c['accepted'],c['total'])==(690,831)
a0=json.loads((O/'status-before.json').read_text());a1=json.loads((O/'status-after.json').read_text())
assert a0['generation']==a1['generation']==p['meta']['generation']==r['browser_generation']
assert not a0['problems'] and not a1['problems'] and a0['required'][0]=='progress'
v={'finished':True,'method':'Read-only normalization of retained HTTP/AX/screenshot; no fresh UI or HTTP capture',
 'raw_sha256':sha(O/'raw.json'),'normalizer_sha256':sha(__file__),
 'correction':'Original browser binding driver wrongly requested item key; actual item field is k. Original failed driver/raw preserved; reprocessed same retained bytes. No new experiment credit.',
 'generation':r['browser_generation'],'ids':ids,'category':c,
 'reader_stale':[a0['reader_stale'],a1['reader_stale']],
 'closed':r['closed'],'limits':r['limits']}
assert v['reader_stale']==[False,False]
if a.out.exists():assert json.loads(a.out.read_text())==v,'Immutable normalization'
else:a.out.write_text(json.dumps(v,indent=2)+'\n')
print('RETAINED_BROWSER_HTTP_BOUND_NO_RECAPTURE',v['generation'],len(ids),flush=True)
