"""Source comparison and scoped pulse reuse candidate; NO native imports/input."""
import ast,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=Path.cwd()
old=ROOT/'Database/FFXII TZA/_experiments/evidence/input-registration-live-title/reuse'
sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((old/'title-enter.json').read_text())
sources={n.replace('\\','/'):h for n,h in r['sources'].items()}
inventory={n:{'captured_sha256':h,'current_sha256':sha((ROOT/n).read_bytes()),'identical':sha((ROOT/n).read_bytes())==h} for n,h in sources.items()}
sender='Database/Tools/analysis-kit/gfz-scripts/runtime_input_probe.py'
assert inventory[sender]['identical'] and sources[sender]=='7a635333e0a842ca140cc64e03d98b4e70cd9944cea776a8f064c3f279c76fae'
assert r['key']=='Enter' and r['registration']=='EXPECTED_HELD_STATE_OBSERVED_AND_RELEASED' and r['down_accepted']==2 and r['up_accepted']==2 and .35<=r['held_elapsed']<.4
text=(old/'pulse.py').read_text();candidate=text
for a,b in [
 ('REPO = HERE.parents[5]','REPO = HERE.parents[4]'),
 ('EVIDENCE = HERE.parent.parent',"EVIDENCE = REPO / 'Database/FFXII TZA/_experiments/evidence'"),
 ("HERE.parent / 'resumed/input_sample.py'","EVIDENCE / 'input-registration-live-title/resumed/input_sample.py'"),
 ("t['id'] == 'ASTRA-INPUT-REUSE-CONTROL'","t['id'] == 'ASTRA-S19-INPUT-ONE-REQUALIFICATION'"),
 ('    a = p.parse_args()',"    a = p.parse_args()\n    assert a.key == 'Enter', 'Only the approved Enter recovery is allowed'\n    assert not a.out.exists()\n    extra_deadline = require_extra_budget()"),
 ('        def guard():','        def guard():\n            assert time.time() <= extra_deadline, \'STOP: bounded extra recovery expired\'')]:
 assert candidate.count(a)==1,a;candidate=candidate.replace(a,b)
guard='''def require_extra_budget(now=None):
    """Existing stopped S19 record must contain an explicit consumed extra grant."""
    import team
    board = json.loads(team.BOARD.read_text())
    task_id = 'ASTRA-S19-INPUT-ONE-REQUALIFICATION'
    task = next(t for t in board['tasks'] if t['id'] == task_id)
    assert task['agent'] == 'ASTRA' and task['status'] == 'ACTIVE'
    held = {r['key'] for r in task.get('claimed_resources', task['resources'])}
    assert '@runtime' in held and 'file:database/tools/work/astra/body-pool-occupancy/setup-budget.json' in held
    claim = next(h for h in reversed(board['history']) if h['operation'].get('task') == task_id and h['operation']['action'] == 'claim')
    assert claim['session'] == 'ASTRA-gpt6sol-20260927-s19-input-requalification'
    budget_path = REPO / 'Database/Tools/work/ASTRA/body-pool-occupancy/setup-budget.json'
    budget = json.loads(budget_path.read_text())
    check_extra_budget(budget, time.time() if now is None else now)
    extra = budget['additional_recovery_authorization']
    extra['pulses_started'] += 1
    # Exclusive @runtime + exact budget-file claim serialize this scoped receipt.
    tmp = budget_path.with_name('setup-budget.input-pulse.tmp')
    with tmp.open('x', encoding='utf-8') as f:
        json.dump(budget, f, indent=2)
        f.write('\\n')
    tmp.replace(budget_path)
    return extra['started_unix'] + extra['max_seconds']


def check_extra_budget(budget, now):
    assert budget['limit_attempts'] == 2 and budget['attempts'] == 3, 'Original limit/history must remain; one approved extra only'
    extra = budget.get('additional_recovery_authorization', {})
    assert extra.get('approved_by') == 'user' and extra.get('user_message'), 'No explicit bounded extra authorization'
    assert extra.get('limit_attempts') == 1 and extra.get('attempt_number') == 3
    assert extra.get('consumed_before_launch') is True
    assert extra.get('task') == 'ASTRA-S19-INPUT-ONE-REQUALIFICATION'
    assert extra.get('max_seconds') == 360 and 0 <= now-extra['started_unix'] <= 360
    assert extra.get('max_pulses') == 2 and 0 <= extra.get('pulses_started', 2) < 2
    return True


'''
candidate=candidate.replace('def main():',guard+'def main():',1)
# The candidate cannot run today: original stopped budget has no grant.
(HERE/'pulse-candidate.py').write_text(candidate)
original_tree=ast.parse(text);candidate_tree=ast.parse(candidate)
orig_pulse=next(n for n in original_tree.body if isinstance(n,ast.FunctionDef) and n.name=='pulse')
new_pulse=next(n for n in candidate_tree.body if isinstance(n,ast.FunctionDef) and n.name=='pulse')
assert ast.dump(orig_pulse)==ast.dump(new_pulse)
compile(candidate,str(HERE/'pulse-candidate.py'),'exec')
stopped=(ROOT/'Database/Tools/work/ASTRA/body-pool-occupancy/setup-budget.json').read_bytes()
assert json.loads(stopped)['attempts']==2 and json.loads(stopped)['status']=='STOP_LOSS_REACHED_INPUT'
(HERE/'stopped-budget.json').write_bytes(stopped)
toolchain=json.loads((old/'toolchain.json').read_text());py=Path(toolchain['executable'])
proof={'method':'A retained method/source comparison, no fresh game qualification',
 'historical_title_receipt':str((old/'title-enter.json').relative_to(ROOT)).replace('\\','/'),
 'historical_receipt_sha256':sha((old/'title-enter.json').read_bytes()),
 'historical_title_image_sha256':sha((old/'title-after-enter-0.jpg').read_bytes()),
 'historical_registration':r['registration'],'hold_seconds':r['held_elapsed'],
 'sources':inventory,'source_changes':[n for n,v in inventory.items() if not v['identical']],
 'interpreter_current_sha256':sha(py.read_bytes()),'interpreter_captured_sha256':toolchain['executable_sha256'],
 'candidate_sha256':sha(candidate.encode()),'pulse_function_ast_identical':True,
 'original_pulse_function_source':ast.get_source_segment(text,orig_pulse),
 'stopped_budget_sha256':sha(stopped),
 's19_comparison':'Sky calls had no held/released raw registration receipt. Their failure neither refutes the separately qualified dual-form method nor establishes duration/packet/API/focus causality.',
 'limits':'Existing historical positives not rerun or re-awarded; current support changed requires fresh qualification. Candidate cannot run without explicit consumed extra authorization in existing budget. No budget file/TEAM/library changes made by preparation.'}
(HERE/'comparison.json').write_text(json.dumps(proof,indent=2)+'\n')
print('RECOVERED unchanged sender/pulse; support changes',proof['source_changes'],'candidate refuses current exhausted budget',flush=True)
