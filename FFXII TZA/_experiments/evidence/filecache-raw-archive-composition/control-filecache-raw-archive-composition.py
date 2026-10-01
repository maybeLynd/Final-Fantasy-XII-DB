"""Actual admission refusals for the bounded original-stage composition proof."""
import hashlib,json
from pathlib import Path
import shutil,subprocess,sys
W=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
BASE=['capture-filecache-format-boundary.py','filecache-format-boundary-source-01.json','filecache-format-boundary-capture-01.status.json',
 'filecache-format-boundary-capture-01.stdout','filecache-format-boundary-capture-01.stderr','validate-title-source-annotations.py','prove_owner_reload_order.py']
def main():
 out=W/'filecache-raw-archive-composition-controls-01'
 if out.exists():raise ValueError('immutable controls exist')
 out.mkdir();rows=[]
 for tag,name,error in [('failed-upstream','filecache-format-boundary-capture-01.status.json','format capture failed'),
 ('incomplete-formatter','filecache-format-boundary-source-01.json','required complete original body identity failed'),
 ('changed-short-format','filecache-format-boundary-source-01.json','exact original short format literal failed'),
 ('wrong-formatter-import','filecache-format-boundary-source-01.json','static formatter import attribution failed')]:
  d=out/tag;d.mkdir()
  for n in BASE:shutil.copy2(W/n,d/n)
  p=d/name;v=json.loads(p.read_text())
  if tag=='failed-upstream':v['exit']=1
  elif tag=='incomplete-formatter':
   q=v['ranges'][0];q['instructions']=q['instructions'][:-1];b=bytes.fromhex(''.join(i['bytes'] for i in q['instructions']));q.update(end_exclusive=hex(int(q['start'],16)+len(b)),sha256=hashlib.sha256(b).hexdigest())
  elif tag=='changed-short-format':
   v['exact_literal'].update(bytes='256400',sha256=hashlib.sha256(b'%d\0').hexdigest())
  else:v['static_format_import']['name']='__stdio_common_vswprintf'
  p.write_text(json.dumps(v,indent=2)+'\n');dest=d/'result.json'
  cmd=[sys.executable,str(W/'prove-filecache-raw-archive-composition.py'),'--source',str(d),'--out',str(dest)]
  r=subprocess.run(cmd,cwd=W,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
  (d/'stdout').write_bytes(r.stdout);(d/'stderr').write_bytes(r.stderr)
  row=dict(tag=tag,command=cmd,terminal=True,exit=r.returncode,expected_error=error,result_absent=not dest.exists(),passed=r.returncode!=0 and error in r.stderr.decode(errors='replace') and not dest.exists(),changed_file=name,changed_sha256=sha(p),inherited_from_baseline={n:sha(d/n) for n in BASE if n!=name})
  (d/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
 r=dict(status='PASS_FOUR_ACTUAL_REFUSALS' if all(x['passed'] for x in rows) else 'INVALID',complete=all(x['passed'] for x in rows),cases=rows,driver_sha256=sha(Path(__file__)),producer_sha256=sha(W/'prove-filecache-raw-archive-composition.py'))
 (out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(rows))
 if not r['complete']:raise ValueError('actual controls failed/incomplete')
if __name__=='__main__':main()
