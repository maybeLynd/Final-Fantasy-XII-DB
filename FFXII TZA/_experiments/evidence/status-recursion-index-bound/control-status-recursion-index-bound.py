"""Actual prerequisite/original-bound refusals; synthetic inputs only."""
import copy,hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=pathlib.Path(sys.argv[1]);out.mkdir();v0=json.loads((W/'status-recursion-index-bound-source-01.json').read_text());s0=json.loads((W/'status-recursion-index-bound-capture-01.status.json').read_text());rows=[]
 for tag,error in [('failed-capture','capture prerequisite failed or missing'),('changed-loop-bound','loop bytes differ from shipping reference'),('missing-loop','missing/different loop source')]:
  c=out/tag;c.mkdir();v=copy.deepcopy(v0);st=copy.deepcopy(s0)
  if tag=='failed-capture':st['exit']=1
  if tag=='missing-loop':v['ranges']=v['ranges'][:1]
  if tag=='changed-loop-bound':
   q=v['ranges'][1];i=next(i for i in q['instructions'] if i['pc']=='0x30e6d4')
   if i['bytes']!='83ff20':raise ValueError('loop-bound mutation preimage changed')
   i.update(bytes='83ff40',args='edi, 0x40');q['sha256']=hashlib.sha256(bytes.fromhex(''.join(i['bytes'] for i in q['instructions']))).hexdigest()
  v['synthetic_fixture']='Invalid-source regression fixture, not original execution';p=c/'status-recursion-index-bound-source-01.json';p.write_text(json.dumps(v,indent=2)+'\n');st['source_sha256']=sha(p);sp=c/'capture-status.json';sp.write_text(json.dumps(st,indent=2)+'\n');shutil.copyfile(W/'capture-status-recursion-index-bound.py',c/'capture-status-recursion-index-bound.py')
  result=c/'invalid-result.json';argv=[sys.executable,str(W/'prove-status-recursion-index-bound.py'),str(c),str(sp),str(result)];z=subprocess.run(argv,capture_output=True,timeout=45);(c/'stdout').write_bytes(z.stdout);(c/'stderr').write_bytes(z.stderr)
  r={'case':tag,'argv':argv,'exit':z.returncode,'terminal':True,'expected_error':error,'expected_error_seen':error.encode() in z.stderr,'invalid_result_absent':not result.exists(),'checker_sha256':sha(W/'prove-status-recursion-index-bound.py')};(c/'status.json').write_text(json.dumps(r,indent=2)+'\n')
  if z.returncode==0 or not r['expected_error_seen'] or not r['invalid_result_absent']:raise ValueError('control invalid/incomplete '+tag)
  rows.append(r)
 (out/'result.json').write_text(json.dumps({'status':'PASS_THREE_ACTUAL_RECURSION_REFUSALS_INDEPENDENT_PENDING','cases':rows,'driver_sha256':sha(pathlib.Path(__file__)),'native_runs':0,'live_runs':0,'limits':'Producer synthetic regressions, not original-code executions or independent acceptance'},indent=2)+'\n');print('Three actual failed/missing/changed-bound refusals; no invalid result')
if __name__=='__main__':main()
