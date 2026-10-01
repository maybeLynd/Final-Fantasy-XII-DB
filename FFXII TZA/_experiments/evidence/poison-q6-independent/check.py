import argparse,hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest()
a=argparse.ArgumentParser();a.add_argument('--raw',type=Path);args=a.parse_args();rawpath=args.raw or W/'run-01/raw.json';r=json.loads(rawpath.read_text());s=json.loads((W/'source.json').read_text());P=W/'private-source'
assert r['terminal'] is True and r['exception'] is None and r['downstream_started'] is True,'INVALID_OR_INCOMPLETE_CAPTURE'
assert r['reference']==s and r['driver_sha256']==sha((W/'capture.py').read_bytes())==sha((W/'run-01/driver-before-run.py').read_bytes())
assert (W/'run-01/tool-receipt.json').exists() and json.loads((W/'run-01/tool-receipt.json').read_text())['exit_code']==0
for x in s['records']:
 b=(P/x['copy']).read_bytes();assert sha(b)==x['sha256']
 q=subprocess.run(['git','rev-parse',x['commit']+':'+x['path']],capture_output=True,text=True);assert q.returncode==0 and q.stdout.strip()==x['blob']
 assert subprocess.run(['git','hash-object','--stdin'],input=b,capture_output=True).stdout.decode().strip()==x['blob']
assert sha((P/'stage2-00386c70.bin').read_bytes())==s['image']['stage2_bytes_sha256']
assert r['module_paths']['check'].replace('\\','/').endswith('/private-source/check.py') and r['module_paths']['poison'].replace('\\','/').endswith('/private-source/poison.py')
p=r['prerequisite'];assert p['ok'] is True and p['total']==p['pass']==6 and len(p['results'])==6 and all(x['pass_'] is True for x in p['results'].values()),'UPSTREAM_FAILED_OR_MISSING'
o=r['original_case_results'];assert o['fails']==0 and len(o['cases'])==14
assert o==json.loads((P/'poison_result.json').read_text())
for name,x in o['cases'].items():assert x['verdict']=='PASS' and x['observed']['ran'] is True and not x['observed']['outside'] and not x['observed']['faults'],name
b=r['independent_boundaries'];expected=['below_critical_line','equal_critical_line','nonpositive_removes_critical','stop_poison_low_hp','bubble_equal_line'];assert sorted(b)==sorted(expected),'INCOMPLETE_BOUNDARIES'
for name,x in b.items():
 z=x['observed'];assert x['verdict']=='PASS' and z['ran'] is True and not z['outside'] and not z['faults'] and x['guard_unchanged'] is True and not x['stats_write_observed'] and x['stage_order']==[1,2,3,4,5]
 assert z['hp_delta']==0 and not(z['flagA']&0x100)
 assert any(t['pc']=='0x386f95' and t['r8d']==x['fixture']['hp'] for t in x['trace'])
 assert (bool(z['apply']&(1<<29)),bool(z['remove']&(1<<29)))==((True,False) if name in ['below_critical_line','stop_poison_low_hp'] else (False,True))
assert r['judge_controls']['valid']==[] and r['judge_controls']['wrong_hp_delta']
c=json.loads((W/'prerequisite-control.json').read_text());assert c['terminal'] and c['returncode']!=0 and 'UPSTREAM_FAILED_OR_MISSING' in c['stderr'] and not c['shipping_code_executed']
f=json.loads((W/'static-control.json').read_text());assert f['original']['reachable_return'] and f['original']['return_path_omitting_gate'] is None and f['control']['return_path_omitting_gate'] and f['mutation']['original_byte_binding_refuses']
g=json.loads((W/'cleanup.json').read_text());assert g['reference_unchanged'] and g['graph_unchanged'] and all(z['unchanged_since_preparation'] for z in g['originals']) and not g['live_game_or_pc_control_used'] and g['private_capture_process_terminal']
print('SCOPED_Q6_SUPPORTED; NO_LIVE_OR_SINK_CLOSURE; OWN_ACCEPTANCE_PENDING')
