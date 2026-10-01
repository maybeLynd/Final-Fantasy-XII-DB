"""Discriminate routing admission without more contended writes after feasibility timeout."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent; R = W / 'read-only-01'; prior = W / 'run-01'
assert not R.exists(), 'Retain read-only run'
old = json.loads((prior / 'raw.json').read_text())
assert old['finished'] is False and old['fatal']['type'] == 'TimeoutExpired'
here = prior / 'source/Database/Tools/analysis-kit/gfz-scripts'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for n, s in old['sources'].items(): assert sha(here / n) == s['sha256']
spec = importlib.util.spec_from_file_location('readonly_fixture_team', here / 'team.py')
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
assert T.ROOT == prior / 'source'
R.mkdir()
rv = {'author': 'OPUS', 'commit': old['sources']['transitions.py']['last_commit'], 'record': 'Database/Tools/analysis-kit/gfz-scripts/transitions.py'}
decls = [
 ('valid-reject', rv, ['verdict:REJECT'], 'ASTRA', 'REPAIR'),
 ('valid-accept', dict(rv, incorporation_owner='FABLE'), ['verdict:ACCEPT'], 'ASTRA', 'INCORPORATE'),
 ('no-owner', rv, ['verdict:ACCEPT'], 'ASTRA', 'ACCEPTED'),
 ('missing-verdict', rv, ['receipt:only'], 'ASTRA', 'VERDICT-MISSING'),
 ('conflicting-verdict', rv, ['verdict:ACCEPT','verdict:REJECT'], 'ASTRA', 'VERDICT-CONFLICT'),
 ('malformed-string', 'wrong type', ['verdict:REJECT'], 'ASTRA', 'MALFORMED'),
 ('missing-commit', dict(rv, commit=None), ['verdict:REJECT'], 'ASTRA', 'MALFORMED'),
 ('typed-commit', dict(rv, commit={'not':'a SHA'}), ['verdict:REJECT'], 'ASTRA', 'MALFORMED'),
 ('non-sha-commit', dict(rv, commit='not a SHA'), ['verdict:REJECT'], 'ASTRA', 'MALFORMED'),
 ('typed-record', dict(rv, record={'not':'a path'}), ['verdict:REJECT'], 'ASTRA', 'MALFORMED'),
 ('self-review', dict(rv, incorporation_owner='FABLE'), ['verdict:ACCEPT'], 'OPUS', 'independent-review-refusal'),
 ('typed-author', dict(rv, author=['OPUS']), ['verdict:REJECT'], 'ASTRA', 'MALFORMED')]
raw = {'method': 'A actual immutable transition CLI DRY RUN on validated labelled fixtures, no board writes',
       'driver_sha256': sha(__file__), 'source_tree_commit': old['source_tree_commit'], 'sources': old['sources'],
       'prior_partial_raw_sha256': sha(prior / 'raw.json'), 'cases': [], 'finished': False,
       'limits': 'Original apply campaign INCOMPLETE after valid reject and timeout at valid accept. Nested writer later produced private incorporation row/journal but response/descendant cleanup not independently proven. Unmodified lock uses one Local mutex name for all board paths; potential production contention is a bounded hypothesis, not proven timeout cause. No additional apply or unchanged retry. Dry-run proves admitted plans, not execution/duplicate or racing closure.'}
stamp = '2026-09-29T06:30:00+00:00'
for name, reviews, refs, reviewer, expected in decls:
 d = R / name; d.mkdir(); bp = d / 'TEAM.json'
 t = {'id':'REVIEW-'+name.upper(), 'kind':'research','priority':'P2','agent':reviewer,'assigned_to':reviewer,
      'status':'DONE','target':'labelled read-only fixture','scope':'synthetic routing admission','completion':'fixture only',
      'checkpoint':'verdict:ACCEPT in prose is not a structured ref','started_at':stamp,'updated_at':stamp,
      'dependencies':[],'resources':[{'key':'request:fixture/'+name}], 'reviews':copy.deepcopy(reviews),'result_refs':refs}
 agents = {n:{'agent_id':n,'primary_specialty':'fixture only','current_task':[],'claimed_scope':[],
      'dependencies':[],'blockers':[],'last_checkpoint':stamp,'status':'READY'} for n in T.AGENTS}
 b = {'schema_version':1,'phase':'DATABASE','revision':0,'recovery_epoch':0,'agents':agents,'tasks':[t],'history':[],'checkpoints':[]}
 T.refresh(b);T.validate(b);bp.write_text(json.dumps(b,indent=2)+'\n');before=sha(bp)
 args=[str(Path(sys._base_executable)),'-B',str(here/'transitions.py'),'--board',str(bp),'--json']
 p=subprocess.run(args,capture_output=True,text=True,timeout=5)
 try: report=json.loads(p.stdout)
 except json.JSONDecodeError: report=None
 assert before==sha(bp),'Dry run mutated fixture'
 c={'name':name,'expected':expected,'input_sha256':before,'args':args,'returncode':p.returncode,
    'stdout':p.stdout,'stderr':p.stderr,'parsed_report':report,'board_unchanged':True,'timed_out':False,'child_reaped':True}
 (d/'receipt.json').write_text(json.dumps(c,indent=2)+'\n');raw['cases'].append(c)
raw['finished']=True
(R/'raw.json').write_text(json.dumps(raw,indent=2)+'\n')
print('READONLY_CONTROLS',[(c['name'],c['returncode'],None if c['parsed_report'] is None else c['parsed_report'][0]['transition']) for c in raw['cases']],flush=True)
