import argparse,hashlib,json,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;R=W/'run-01';sha=lambda b:hashlib.sha256(b).hexdigest();p=argparse.ArgumentParser();p.add_argument('--raw',type=Path);a=p.parse_args();r=json.loads((a.raw or R/'raw.json').read_text())
assert r['terminal'] and r['exception'] is None and r['current_status_assignment_equal'],'INVALID_OR_INCOMPLETE'
assert r['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
q=json.loads((W/'capture-terminal.json').read_text());assert q['terminal'] and q['returncode']==0 and not q['stderr']
H=R/'source/Database/Tools/analysis-kit/gfz-scripts'
for name,z in r['sources'].items():
 data=(R/'original-team.py').read_bytes() if name=='team.py' else (H/name).read_bytes();assert sha(data)==z['sha256'];q=subprocess.run(['git','rev-parse',r['source_commit']+':'+z['path']],capture_output=True,text=True);assert q.returncode==0 and q.stdout.strip()==z['blob'];assert subprocess.run(['git','hash-object','--stdin'],input=data,capture_output=True).stdout.decode().strip()==z['blob']
assert (H/'team.py').read_bytes()==(R/'labelled-child-entry-guard.py').read_bytes()+(R/'original-team.py').read_bytes() and sha((H/'team.py').read_bytes())==r['private_team_with_guard_sha256']
assert sha((R/'original-fixture.json').read_bytes())==r['fixture_sha256'] and sha((R/'current-parent-preimage.py').read_bytes())==r['current_parent_sha256']
cs={x['name']:x for x in r['cases']};assert len(cs)==len(r['cases'])==3 and set(cs)=={'zero-marker','nonzero-marker','nonzero-error'},'MISSING_CASE'
for name,x in cs.items():
 assert x['terminal'] and x['board_unchanged'] and not x['stderr']
 assert '--apply' in x['argv'] and '--board' in x['argv'] and x['argv'][-1]=='--json'
 assert json.loads(x['stdout'])==x['report'] and len(x['report'])==1 and x['report'][0]['transition']=='REPAIR'
 c=x['child'];assert not c['real_writer_executed'] and '--file' in c['argv'] and '--board' in c['argv'] and c['received_op']['action']=='add'
 assert json.loads((R/(name+'-child.json')).read_text())==c
 assert sha((R/(name+'-board.json')).read_bytes())==r['fixture_sha256']
 expected=(0,0,'created') if name=='zero-marker' else (1,0,'created') if name=='nonzero-marker' else (1,1,'FAILED:')
 assert c['exit_code']==expected[0] and x['returncode']==expected[1] and x['report'][0]['status'].startswith(expected[2]),'OUTCOME_CHANGED'
print('REJECT_REQUIRED_WRITER_NONZERO_SWALLOWED; SUBSTITUTED_CHILD_SCOPE_ONLY')
