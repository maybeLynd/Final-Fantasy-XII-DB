import argparse,hashlib,json,zipfile
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reduce(w,rawpath):
 r=json.loads(rawpath.read_text());d=rawpath.parent
 assert r['finished'] is True and r['source_unchanged'] is True and 'fatal' not in r,'INCOMPLETE_CAPTURE'
 assert r['commit']=='b6e6de3f0080cd311336c04d68cf17516c228dff'
 assert r['driver_sha256']==sha(w/'capture.py')
 data=(d/'generation.py').read_bytes();assert sha(d/'generation.py')==r['source_sha256']
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['source_blob']
 assert r['source_blob']=='b3955bd182656cd5b2ae9987cd396b8c7b02ac16'
 assert sha(d/'retained-manifest.json')==r['retained_manifest_sha256'] and sha(d/'retained-raw.json')==r['retained_raw_sha256']
 idx={m['path']:m for m in json.loads((d/'retained-manifest.json').read_text())['members']}
 prior=json.loads((d/'retained-raw.json').read_text());old=next(c for c in prior['cases'] if c['name']=='unknown-input-state')
 assert prior['finished'] and old['label']=='VERIFIED' and old['cli']['returncode']==0
 cs={c['name']:c for c in r['cases']};assert len(cs)==len(r['cases'])==3 and set(cs)=={'positive','unknown-input-state','duplicate-zip-member'},'MISSING_CASE'
 for n,c in cs.items():
  assert c==json.loads((d/(n+'-receipt.json')).read_text()) and c['exception'] is None
  p=d/(n+'.zip');pin=idx['run-01/'+n+'.zip'];assert sha(p)==pin['sha256']==c['sha256'] and p.stat().st_size==pin['bytes']==c['bytes']
  with zipfile.ZipFile(p) as z:assert c['entries']==[{'name':x.filename,'sha256':hashlib.sha256(z.read(x)).hexdigest()} for x in z.infolist()]
  label='VERIFIED' if n=='positive' else 'UNVERIFIED';q=c['cli']
  assert c['label']==label and q['terminal'] is True and q['returncode']==(0 if n=='positive' else 1) and not q['stderr'],'WRONG_CLI_STATUS'
  assert q['stdout'].startswith(label+' ') and json.loads(q['stdout'][len(label)+1:])==c['info']
  assert len(q['args'])==5 and q['args'][1]=='-B' and q['args'][3]=='verify-zip' and Path(q['args'][4]).name==n+'.zip'
 assert 'unknown state' in cs['unknown-input-state']['info']['reason'] and 'ASTRA_LABELLED_UNKNOWN_STATE' in cs['unknown-input-state']['info']['reason']
 assert 'duplicate member names' in cs['duplicate-zip-member']['info']['reason']
 with zipfile.ZipFile(d/'positive.zip') as z:base=json.loads(z.read('MANIFEST.json'));bn=set(z.namelist())
 with zipfile.ZipFile(d/'unknown-input-state.zip') as z:bad=json.loads(z.read('MANIFEST.json'));nn=set(z.namelist())
 changed=[k for k in base['inputs'] if base['inputs'][k]!=bad['inputs'][k]];assert len(changed)==1
 k=changed[0];assert base['inputs'][k]['state']=='present' and not base['inputs'][k].get('external')
 assert bad['inputs'][k]['state']=='ASTRA_LABELLED_UNKNOWN_STATE' and bn-nn=={'inputs/'+k} and not nn-bn
 assert base['outputs']==bad['outputs'] and base['generation']==bad['generation']
 return {'verdict':'ACCEPT_SCOPED_UNKNOWN_STATE_REPAIR','source_commit':r['commit'],'changed_reader_cases':3,
         'prior_unknown_archive':'VERIFIED_OLD_SOURCE_RETAINED','now_unknown_archive':'UNVERIFIED_EXIT1',
         'valid_control':'VERIFIED_EXIT0','duplicate_control':'UNVERIFIED_EXIT1','normal_builder_or_deployed_reader':'NOT_CERTIFIED',
         'whole_manifest_authentication':'OUTSIDE_MEMBER_CHECK_SIDE_CAR_REMAINS_REQUIRED',
         'full_M1_or_L1_L2':False,'independent_acceptance_of_this_evidence':'PENDING'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args();w=Path(__file__).resolve().parent
 result=reduce(w,a.raw or w/'run-01/raw.json')
 if a.out:a.out.write_text(json.dumps(result,indent=2)+'\n')
 print('ACCEPT_SCOPED_UNKNOWN_STATE_REPAIR',json.dumps(result,sort_keys=True))
