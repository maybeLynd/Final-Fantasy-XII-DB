"""Four actual checked CLI refusals, using one already validated positive."""
import hashlib,json
from pathlib import Path
import shutil,subprocess,sys
W=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
BASE=['capture-filecache-fill-key-provenance.py','qualify-filecache-failure-thunks.py','validate-title-source-annotations.py','prove_owner_reload_order.py',
 'filecache-fill-key-resolver-source-01.json','filecache-release-allocator-thunks-qualified-01.json']
for tag in ['filecache-fill-key-resolver-capture-01','filecache-release-allocator-thunks-qualification-01']:BASE.extend(tag+x for x in ['.status.json','.stdout','.stderr'])
def main():
 out=W/'filecache-fill-and-failure-controls-01'
 if out.exists():raise ValueError('immutable controls exist')
 out.mkdir();rows=[]
 defs=[('failed-resolver','filecache-fill-key-resolver-capture-01.status.json','required producer upstream failed'),
       ('incomplete-resolver','filecache-fill-key-resolver-source-01.json','required original complete boundary/identity failed'),
       ('coherent-output-pointer-change','filecache-fill-key-resolver-source-01.json','required original complete boundary/identity failed'),
       ('false-malloc-import','filecache-release-allocator-thunks-qualified-01.json','malloc declaration/reference wrong')]
 for tag,name,error in defs:
  d=out/tag;d.mkdir()
  for n in BASE:shutil.copy2(W/n,d/n)
  p=d/name;v=json.loads(p.read_text())
  if tag=='failed-resolver':v['exit']=1
  elif tag=='incomplete-resolver':
   q=v['ranges'][0];q['instructions']=q['instructions'][:-1];b=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']));q.update(end_exclusive=hex(int(q['start'],16)+len(b)),sha256=hashlib.sha256(b).hexdigest())
  elif tag=='coherent-output-pointer-change':
   q=v['ranges'][0];i=next(i for i in q['instructions'] if i['pc']=='0x59efd7');i.update(bytes='4d8d4f30',args='r9, [r15 + 0x30]');i['memory'][0]['displacement']=0x30
   q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
  else:v['malloc_import_declaration']['name']='operator new'
  p.write_text(json.dumps(v,indent=2)+'\n');dest=d/'result.json'
  cmd=[sys.executable,str(W/'prove-filecache-fill-and-failure.py'),'--source',str(d),'--out',str(dest)]
  r=subprocess.run(cmd,cwd=W,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
  (d/'stdout').write_bytes(r.stdout);(d/'stderr').write_bytes(r.stderr)
  row=dict(tag=tag,command=cmd,exit=r.returncode,terminal=True,expected_error=error,result_absent=not dest.exists(),changed_file=name,changed_sha256=sha(p),inherited_from_baseline={n:sha(d/n) for n in BASE if n!=name},passed=r.returncode!=0 and error in r.stderr.decode(errors='replace') and not dest.exists())
  (d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
 r=dict(status='PASS_FOUR_ACTUAL_REFUSALS' if all(x['passed'] for x in rows) else 'INVALID',complete=all(x['passed'] for x in rows),cases=rows,driver_sha256=sha(Path(__file__)),producer_sha256=sha(W/'prove-filecache-fill-and-failure.py'))
 (out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(rows))
 if not r['complete']:raise ValueError('controls incomplete/failed')
if __name__=='__main__':main()
