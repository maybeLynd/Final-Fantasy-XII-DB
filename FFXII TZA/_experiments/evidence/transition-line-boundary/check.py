import argparse,ast,hashlib,json,subprocess
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest();ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path);a=ap.parse_args();r=json.loads((a.raw or W/'run-02/raw.json').read_text());R=W/'run-02'
assert r['terminal'] and r['exception'] is None and r['selected_current_admission_ast_equal'],'INCOMPLETE_OR_INVALID'
assert r['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((R/'driver-before-run.py').read_bytes())
q=json.loads((W/'capture-terminal.json').read_text());assert q['terminal'] and q['returncode']==0 and not q['stderr']
for name,s in r['sources'].items():
 p=R/'source/Database/Tools/analysis-kit/gfz-scripts'/name;b=p.read_bytes();assert sha(b)==s['sha256'];z=subprocess.run(['git','rev-parse',r['source_commit']+':'+s['path']],capture_output=True,text=True);assert z.returncode==0 and z.stdout.strip()==s['blob']
 assert subprocess.run(['git','hash-object','--stdin'],input=b,capture_output=True).stdout.decode().strip()==s['blob']
assert sha((R/'prior-valid-input.json').read_bytes())==r['prior_input_sha256']
def selected(text):
 out={}
 for n in ast.parse(text).body:
  if isinstance(n,(ast.FunctionDef,ast.Assign)):
   key=n.name if isinstance(n,ast.FunctionDef) else (n.targets[0].id if isinstance(n.targets[0],ast.Name) else '')
   if key in ['VERDICT','SHA','link_problem','plan','_op']:out[key]=ast.dump(n,include_attributes=False)
 return out
current=(R/'current-transitions-preimage.py').read_bytes();assert sha(current)==r['sources']['transitions.py']['current_sha256']
assert selected(current.decode())==selected((R/'source/Database/Tools/analysis-kit/gfz-scripts/transitions.py').read_text())

cs={c['name']:c for c in r['cases']};assert len(cs)==len(r['cases'])==4 and set(cs)=={'valid-full40','commit-full40-lf','commit-full40-crlf','verdict-lf'},'MISSING_CASE'
for name,c in cs.items():
 assert c['terminal'] and c['returncode']==0 and not c['stderr'] and c['board_unchanged'] and not c['writer_invoked'],'FAILED_UPSTREAM'
 assert c['argv'][-1]=='--json' and '--apply' not in c['argv'] and c['argv'][1]=='-B'
 b=(R/(name+'.json')).read_bytes();assert sha(b)==c['input_sha256'];x=json.loads(b)['tasks'][0]
 assert json.loads(c['stdout'])==c['report'] and len(c['report'])==len(c['original_plan'])==1
 expected='MALFORMED' if name=='commit-full40-crlf' else 'INCORPORATE';assert c['report'][0]['transition']==c['original_plan'][0][0]==expected
 if name=='commit-full40-lf':
  assert len(x['reviews']['commit'])==41 and x['reviews']['commit']==r['source_commit']+'\n'
  assert c['original_plan'][0][3]['task']['transition_of']['commit']==x['reviews']['commit'],'NEWLINE_NOT_FORWARDED'
 if name=='verdict-lf':assert x['result_refs']==['verdict:ACCEPT\n']
assert json.loads((W/'run-01/failure.json').read_text())['cases_executed']==0
print('REJECT_EXACT_FIELD_ADMISSION; TRAILING_LF_ACCEPTED; PRIOR_NAMED_CASES_RETAINED')
