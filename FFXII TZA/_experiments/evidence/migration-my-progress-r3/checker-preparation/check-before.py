import argparse,hashlib,json
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reduce(w,rawpath):
 d=rawpath.parent;r=json.loads(rawpath.read_text())
 assert r['finished'] is True and 'fatal' not in r and r['source_and_inputs_unchanged'] is True,'INCOMPLETE_CAPTURE'
 assert r['commit'].startswith('69bbf8c81') and r['prior_commit']=='037557884af3ed9b687b6bb8b2a34855c0703cdd'
 assert sha(w/'capture.py')==r['driver_sha256'] and sha(w/'probe.py')==r['probe_sha256']
 assert len(r['sources'])==3
 for rel,p in r['sources'].items():
  data=(d/'source'/rel).read_bytes();assert hashlib.sha256(data).hexdigest()==p['sha256'] and len(data)==p['bytes']
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==p['blob']
 assert sha(d/'retained-manifest.json')==r['retained_manifest_sha256'] and sha(d/'subsystems.tsv')==r['subsystems_sha256']
 idx={p['path']:p for p in json.loads((d/'retained-manifest.json').read_text())['members']}
 assert r['subsystems_sha256']==idx['core-01/subsystems.tsv']['sha256']
 cases={c['name']:c for c in r['cases']};assert len(cases)==len(r['cases'])==4 and set(cases)=={'zero-measure','thirty-measure','zero-ready-view','thirty-ready-view'},'MISSING_CASE'
 for name,c in cases.items():
  assert c==json.loads((d/name/'receipt.json').read_text())
  assert sha(d/name/'input.json')==c['input_sha256']==idx[c['origin']]['sha256']
  assert c['returncode']==0 and not c['stderr'] and c['terminal'] is True and c['parse_error'] is None,'UPSTREAM_FAILED'
  p=c['parsed'];assert isinstance(p,dict) and 'result' in p and 'exception' in p and p['exception'] is None,'MISSING_RESULT'
  assert json.loads(c['stdout'])==p and p['kind']==c['kind'] and len(p['modules'])==3
  args=c['args'];assert len(args)==12 and args[1]=='-B' and Path(args[2]).name=='probe.py' and args[3]=='--source' and args[5]=='--input' and args[7]=='--kind' and args[9]=='--subsystems'
  out=p['result']
  if name=='zero-measure':assert out['ready'] is False and out['measured'] is False and 'T' in out['failed'] and out['terminal']=={'accepted':None,'required':30}
  elif name=='thirty-measure':assert out['ready'] is True and out['measured'] is True and not out['failed'] and out['terminal']=={'accepted':30,'required':30}
  elif name=='zero-ready-view':assert isinstance(out,str) and 'DATABASE READY claimed' in out
  else:assert out is None  # explicit original check_progress success, not missing data
 return {'verdict':'ACCEPT_SCOPED_FIXED_TERMINAL_REQUIREMENT','source_commit':r['commit'],'changed_source_observations':4,
         'zero_measure':'FAILED_T_UNMEASURED_NOT_READY_REQUIRED30','zero_ready_view':'REFUSED','thirty_controls':'PRESERVED',
         'actual_terminal_audits':'NOT_RUN','normal_builder_deployment':'NOT_CERTIFIED','full_M0_M5_or_L1_L2':False,
         'independent_acceptance_of_evidence':'PENDING'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args();w=Path(__file__).resolve().parent
 result=reduce(w,a.raw or w/'run-01/raw.json')
 if a.out:a.out.write_text(json.dumps(result,indent=2)+'\n')
 print('ACCEPT_SCOPED_FIXED_TERMINAL_REQUIREMENT',json.dumps(result,sort_keys=True))
