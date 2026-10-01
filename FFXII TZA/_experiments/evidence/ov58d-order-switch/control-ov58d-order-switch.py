"""Focused synthetic refusals through the actual source proof CLI."""
import copy,hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=pathlib.Path(sys.argv[1]);out.mkdir();base=json.loads((W/'ov58d-order-switch-source-02.json').read_text());good=json.loads((W/'ov58d-order-switch-capture-02.status.json').read_text());rows=[]
 for tag,error in [('failed-capture','failed/missing capture prerequisite'),('wrong4049-selector','table differs from shipping reference'),('changed-status-subtract','code differs from shipping reference'),('missing-selector-table','missing/different original tables'),('wrong-store-role','memory/address/access annotation disagrees')]:
  c=out/tag;c.mkdir();v=copy.deepcopy(base);st=copy.deepcopy(good)
  if tag=='failed-capture':st['exit']=1
  if tag=='wrong4049-selector':
   t=next(t for t in v['tables'] if t['address']=='0x2fe54c');b=bytearray.fromhex(t['bytes'])
   if b[3]!=1:raise ValueError('selector preimage changed')
   b[3]=3;t['bytes']=b.hex();t['sha256']=hashlib.sha256(b).hexdigest()
  if tag=='changed-status-subtract':
   q=v['ranges'][0];i=next(i for i in q['instructions'] if i['pc']=='0x2fdf1f')
   if i['bytes']!='448d42af':raise ValueError('subtract preimage changed')
   i.update(bytes='448d42ae',args='r8d, [rdx - 0x52]');i['memory'][0]['displacement']=-0x52
   q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
  if tag=='missing-selector-table':v['tables']=[t for t in v['tables'] if t['address']!='0x2fe54c']
  if tag=='wrong-store-role':next(i for i in v['ranges'][0]['instructions'] if i['pc']=='0x2fde83')['memory'][0]['role']='r'
  v['synthetic_fixture']='Intentionally invalid source input, not shipping/native/live evidence';p=c/'ov58d-order-switch-source-02.json';p.write_text(json.dumps(v,indent=2)+'\n');st['source_sha256']=sha(p)
  sp=c/'capture-status.json';sp.write_text(json.dumps(st,indent=2)+'\n');shutil.copyfile(W/'capture-ov58d-order-switch.py',c/'capture-ov58d-order-switch.py')
  result=c/'invalid-result.json';argv=[sys.executable,str(W/'prove-ov58d-order-switch.py'),str(c),str(sp),str(result)];z=subprocess.run(argv,capture_output=True,timeout=45)
  (c/'stdout').write_bytes(z.stdout);(c/'stderr').write_bytes(z.stderr)
  r={'case':tag,'argv':argv,'exit':z.returncode,'terminal':True,'expected_error':error,'expected_error_seen':error.encode() in z.stderr,'invalid_result_absent':not result.exists(),'checker_sha256':sha(W/'prove-ov58d-order-switch.py')};(c/'status.json').write_text(json.dumps(r,indent=2)+'\n')
  if z.returncode==0 or not r['expected_error_seen'] or not r['invalid_result_absent']:raise ValueError('invalid/incomplete/nondiscriminating control '+tag)
  rows.append(r)
 (out/'result.json').write_text(json.dumps({'status':'PASS_FIVE_ACTUAL_CLI_REFUSALS_INDEPENDENT_PENDING','cases':rows,'driver_sha256':sha(pathlib.Path(__file__)),'native_runs':0,'live_runs':0,'limits':'Synthetic code/data/status mutations, not original/native execution or independent acceptance'},indent=2)+'\n');print('Five actual byte/table/role/prerequisite refusals; invalid result absent')
if __name__=='__main__':main()
