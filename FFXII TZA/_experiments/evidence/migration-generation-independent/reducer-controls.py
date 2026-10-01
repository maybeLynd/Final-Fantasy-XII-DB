import copy, json, subprocess, sys
from pathlib import Path
W=Path(__file__).resolve().parent;r=json.loads((W/'run-01/raw.json').read_text());d=W/'reducer-controls';assert not d.exists();d.mkdir();receipts=[]
for name in ('incomplete','missing-case','hide-duplicate-certification','unverified-cleanup'):
 q=copy.deepcopy(r)
 if name=='incomplete':q['finished']=False
 elif name=='missing-case':q['cases']=[c for c in q['cases'] if c['name']!='mixed-zip']
 elif name=='hide-duplicate-certification':next(c for c in q['cases'] if c['name']=='duplicate-zip-member')['observed']['label']='UNVERIFIED'
 else:q['owned_process_cleanup'][0]['terminal']=False
 p=d/(name+'.json');p.write_text(json.dumps(q,indent=2)+'\n');out=d/(name+'-result.json')
 x=subprocess.run([sys.executable,'-B',str(W/'check.py'),'--raw',str(p),'--out',str(out)],capture_output=True,text=True,timeout=10)
 assert x.returncode!=0 and not out.exists()
 receipts.append({'name':name,'returncode':x.returncode,'stdout':x.stdout,'stderr':x.stderr,'result_created':out.exists()})
(W/'reducer-controls.json').write_text(json.dumps(receipts,indent=2)+'\n')
print('FOUR_ALTERED_RECEIPTS_REFUSED',flush=True)
