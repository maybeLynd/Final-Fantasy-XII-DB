import argparse,hashlib,json,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';H=R/'source/Database/Tools/analysis-kit/gfz-scripts';sha=lambda b:hashlib.sha256(b).hexdigest();p=argparse.ArgumentParser();p.add_argument('--raw',type=Path);a=p.parse_args();r=json.loads((a.raw or R/'raw.json').read_text())
assert r['terminal'] and r['exception'] is None and r['verdict']=='ACCEPT_SCOPED_EXACT_FIELDS_AND_CALLER_STATUS_R3','INVALID_OR_INCOMPLETE'
assert r['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
t=json.loads((W/'capture-terminal.json').read_text());assert t['terminal'] and t['returncode']==0 and not t['stderr'],'CAPTURE_FAILED'
def git(*args):
 q=subprocess.run(['git',*args],capture_output=True);assert q.returncode==0,(args,q.stderr);return q.stdout
for n,z in r['sources'].items():
 b=(R/'original-team.py').read_bytes() if n=='team.py' else (H/n).read_bytes();assert sha(b)==z['sha256'] and git('show',r['source_commit']+':'+z['path'])==b and git('rev-parse',r['source_commit']+':'+z['path']).decode().strip()==z['blob']
assert (H/'team.py').read_bytes()==(R/'labelled-child-entry-guard.py').read_bytes()+(R/'original-team.py').read_bytes() and sha((H/'team.py').read_bytes())==r['guarded_team_sha256']
old=Path('Database/FFXII TZA/_experiments/evidence/migration-transitions-r2');mb=(old/'manifest.json').read_bytes();assert sha(mb)==r['prior_manifest_sha256'] and git('show',r['prior_commit']+':'+(old/'manifest.json').as_posix())==mb;members={m['path']:m for m in json.loads(mb)['members']};ob=(R/'prior-raw.json').read_bytes();assert sha(ob)==r['prior_raw_sha256']==members['run-01/raw.json']['sha256'];olds={x['name']:x for x in json.loads(ob)['cases']}
regs={x['name']:x for x in r['regression']};assert len(regs)==len(r['regression'])==13 and set(regs)==set(olds),'MISSING_REGRESSION'
fields={x['name']:x for x in r['fields']};expected={'valid-full40':'INCORPORATE','commit-full40-lf':'MALFORMED','commit-full40-crlf':'MALFORMED','verdict-lf':'VERDICT-MISSING'};assert len(fields)==len(r['fields'])==4 and set(fields)==set(expected),'MISSING_FIELD'
for group,rows in [('regression',regs),('fields',fields)]:
 for name,x in rows.items():
  d=R/group/name;b=(d/'TEAM.json').read_bytes();assert sha(b)==x['input_sha256'] and x['board_unchanged'] and not x['writer_invoked']
  assert '--apply' not in x['argv'] and x['terminal'] and x['returncode']==0 and not x['stderr'] and json.loads(x['stdout'])==x['report'] and len(x['report'])==len(x['original_plan'])==1
  want=olds[name]['expected'] if group=='regression' else expected[name];assert x['report'][0]['transition']==x['expected']==want
  assert x==json.loads((d/'receipt.json').read_text()),'RECEIPT_CHANGED'
  if group=='regression':rel='run-01/'+name+'/TEAM.json';assert sha(b)==members[rel]['sha256'] and git('show',r['prior_commit']+':'+(old/rel).as_posix())==b
  else:
   op=x['original_plan'][0][3]
   if name=='valid-full40':assert op['task']['transition_of']['commit']==r['source_commit'] and x['report'][0]['status']=='planned'
   else:assert op is None and x['report'][0]['status']=='-'
writers={x['name']:x for x in r['writer']};expected={'zero-marker':(0,'created',0,'none'),'nonzero-marker':(1,'FAILED:',1,'none'),'nonzero-error':(1,'FAILED:',1,'none'),'zero-no-marker':(0,'FAILED:',1,'none'),'exists-absent':(1,'FAILED:',1,'none'),'exists-derived-id':(1,'exists',0,'derived'),'exists-other-id':(1,'FAILED:',1,'other')};assert len(writers)==len(r['writer'])==7 and set(writers)==set(expected),'MISSING_WRITER'
op=r['writer_plan'][0][3];wantop=op|{'task':op['task']|{'requester':'SWE2-FRONTIER'}};nid=op['task']['id'];base=(old/'run-01/valid-reject/TEAM.json').read_bytes();assert sha(base)==members['run-01/valid-reject/TEAM.json']['sha256']
for name,x in writers.items():
 d=R/'writer'/name;c=x['child'];code,status,pc,mode=expected[name]
 assert x['terminal'] and x['returncode']==pc and x['report'][0]['status'].startswith(status),'WRITER_OUTCOME'
 assert '--apply' in x['argv'] and not x['stderr'] and json.loads(x['stdout'])==x['report'] and len(x['report'])==1
 assert c['exit_code']==code and c['private_intervention']==mode and not c['real_writer_executed'] and c['received_op']==wantop
 assert c==json.loads((d/'child.json').read_text()) and x==json.loads((d/'receipt.json').read_text()),'RECEIPT_CHANGED'
 b=(d/'TEAM.json').read_bytes();assert sha(b)==x['after_sha256']==c['board_after_sha256'] and sha(base)==x['input_sha256']==c['board_before_sha256']
 ids={z['id'] for z in json.loads(b)['tasks']};assert (nid in ids)==(mode=='derived') and (nid+'-OTHER' in ids)==(mode=='other')
 if mode=='none':assert b==base
 assert x['temp_op_removed'] and '--file' in c['argv'] and '--board' in c['argv']
print('ACCEPT_SCOPED_EXACT_FIELDS_AND_CALLER_STATUS_R3; NO_REAL_WRITER_PARITY')
