"""Offline guard/source checks only; do not import native sender or run pulse."""
import ast,copy,hashlib,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=Path.cwd()
text=(HERE/'pulse-candidate.py').read_text();tree=ast.parse(text)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='check_extra_budget')
ns={};exec(compile(ast.Module(body=[node],type_ignores=[]),'budget-function','exec'),ns)
check=ns['check_extra_budget'];now=1000
comparison=json.loads((HERE/'comparison.json').read_text())
stopped=(HERE/'stopped-budget.json').read_bytes()
assert hashlib.sha256(stopped).hexdigest()==comparison['stopped_budget_sha256']
actual=json.loads(stopped)
assert actual['attempts']==2 and actual['status']=='STOP_LOSS_REACHED_INPUT'
cases=[]
def reject(name,b):
 try:check(b,now)
 except AssertionError:cases.append({'name':name,'rejected':True})
 else:raise AssertionError('unapproved/unbounded budget accepted '+name)
reject('actual stopped record has no extra grant',actual)
valid={'limit_attempts':2,'attempts':3,'additional_recovery_authorization':{
 'approved_by':'user','user_message':'SYNTHETIC POSITIVE ONLY - NOT AUTHORIZATION',
 'limit_attempts':1,'attempt_number':3,'consumed_before_launch':True,
 'task':'ASTRA-S19-INPUT-ONE-REQUALIFICATION','max_seconds':360,'started_unix':999,
 'max_pulses':2,'pulses_started':0}}
assert check(valid,now) is True
q=copy.deepcopy(valid);q['attempts']=0;reject('reset original attempt history',q)
q=copy.deepcopy(valid);q['additional_recovery_authorization']['approved_by']='ASTRA';reject('self-approved extra',q)
q=copy.deepcopy(valid);q['additional_recovery_authorization']['limit_attempts']=2;reject('overbroad extra allowance',q)
q=copy.deepcopy(valid);q['additional_recovery_authorization']['started_unix']=0;reject('expired recovery',q)
q=copy.deepcopy(valid);q['additional_recovery_authorization']['pulses_started']=2;reject('pulse limit exhausted',q)
q=copy.deepcopy(valid);q['additional_recovery_authorization']['consumed_before_launch']=False;reject('unconsumed launch allowance',q)
compile(text,str(HERE/'pulse-candidate.py'),'exec')
original=ast.parse(comparison['original_pulse_function_source'])
f=lambda t:next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='pulse')
assert ast.dump(f(original))==ast.dump(f(tree))
assert 'extra[\'pulses_started\'] += 1' in text and 'assert time.time() <= extra_deadline' in text
assert "assert a.key == 'Enter'" in text
r={'result':'PASS_OFFLINE_REUSE_GUARDS','cases':len(cases),'negative_controls':cases,
 'positive':'Synthetic explicit consumed one-extra/2-pulse/6min record; NOT USER AUTHORIZATION',
 'unchanged_pulse_function':True,'compile_only':True,'native_functions_executed':False,
 'frozen_stopped_budget_sha256':hashlib.sha256(stopped).hexdigest(),
 'live_result':None,'limits':'Pure budget/source guard qualification; actual IO/session guards and current native support require fresh controls before input.'}
(HERE/'validation.json').write_text(json.dumps(r,indent=2)+'\n')
print('PASS',len(cases),'guard refusals; frozen stopped budget verified; native/pulse not executed')
