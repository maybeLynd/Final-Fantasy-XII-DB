"""One changed-source, read-only review. Never execute --apply or recreate old run."""
import copy, hashlib, importlib.util, json, platform, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ROOT = W.parents[4]
R = W / 'run-01'
OLD = ROOT / 'Database/FFXII TZA/_experiments/evidence/migration-transitions-independent'
assert not R.exists(), 'Immutable run exists; inspect instead of replaying'
def sha(data): return hashlib.sha256(data).hexdigest()
def git(*args):
    p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    assert p.returncode == 0, p.stderr.decode(errors='replace')
    return p.stdout
commit = git('rev-parse', 'f21fe8044').decode().strip()
prior_commit = '888afe2e4375bf2010566cfe0b5c4b8b3d5018dc'
manifest_bytes = (OLD / 'manifest.json').read_bytes()
assert git('show', prior_commit + ':' + (OLD/'manifest.json').relative_to(ROOT).as_posix()) == manifest_bytes
members = {x['path']: x for x in json.loads(manifest_bytes)['members']}
def prior(rel):
    b = (OLD / rel).read_bytes(); m = members[rel]
    assert len(b) == m['bytes'] and sha(b) == m['sha256'], rel
    assert git('show', prior_commit + ':' + (OLD/rel).relative_to(ROOT).as_posix()) == b, rel
    return b
old_raw_bytes = prior('read-only-01/raw.json')
old_raw = json.loads(old_raw_bytes)
assert old_raw['finished'] and len(old_raw['cases']) == 12
names = [c['name'] for c in old_raw['cases']]
assert len(set(names)) == 12
expected = {n: 'MALFORMED' for n in names}
expected.update({'valid-reject':'REPAIR','valid-accept':'INCORPORATE','no-owner':'ACCEPTED',
 'missing-verdict':'VERDICT-MISSING','conflicting-verdict':'VERDICT-CONFLICT','self-review':'SELF-REVIEW'})
R.mkdir()
here = R/'source/Database/Tools/analysis-kit/gfz-scripts'; here.mkdir(parents=True)
raw = {'format':'ASTRA-transition-admission-r2-1','method':'A: published original repository Python CLI and plan, read-only labelled fixtures',
 'source_commit':commit,'driver_sha256':sha(Path(__file__).read_bytes()),
 'python':{'executable':sys.executable,'base_executable':sys._base_executable,'version':sys.version,'platform':platform.platform()},
 'prior_commit':prior_commit,'prior_manifest_sha256':sha(manifest_bytes),'prior_raw_sha256':sha(old_raw_bytes),
 'sources':{},'cases':[],'finished':False,'write_controls':'NOT_EXECUTED: apply/race/idempotence/failed-writer and prior descendant cleanup remain open'}
(R/'prior-read-only-raw.json').write_bytes(old_raw_bytes)
(R/'prior-limitations.md').write_bytes(prior('README.md'))
for name in ('transitions.py','team.py'):
    rel='Database/Tools/analysis-kit/gfz-scripts/'+name
    data=git('show',commit+':'+rel);(here/name).write_bytes(data)
    raw['sources'][name]={'path':rel,'sha256':sha(data),'bytes':len(data),'blob':git('rev-parse',commit+':'+rel).decode().strip()}
sys.path.insert(0,str(here))
spec=importlib.util.spec_from_file_location('original_transition_r2',here/'transitions.py')
T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)
assert T.team.ROOT == R/'source' and Path(T.team.__file__).resolve() == (here/'team.py').resolve()
inputs=[(n,prior('read-only-01/'+n+'/TEAM.json'),'reused byte-identical immutable fixture') for n in names]
extra=json.loads(dict((n,b) for n,b,_ in inputs)['self-review'])
extra['tasks'][0]['result_refs']=['verdict:REJECT']
inputs.append(('self-review-reject',(json.dumps(extra,indent=2)+'\n').encode(),'minimal change: self-review ACCEPT ref becomes REJECT; same source task identity'))
expected['self-review-reject']='SELF-REVIEW'
def save(): (R/'raw.json').write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
save()
try:
    for name, data, origin in inputs:
        d=R/name;d.mkdir();bp=d/'TEAM.json';bp.write_bytes(data)
        b=json.loads(data);T.team.validate(b)
        before=sha(data)
        args=[str(Path(sys._base_executable)),'-B',str(here/'transitions.py'),'--board',str(bp),'--json']
        assert '--apply' not in args
        p=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',timeout=5)
        parsed=None;parse_error=None
        try: parsed=json.loads(p.stdout)
        except json.JSONDecodeError as e: parse_error=str(e)
        plans=T.plan(copy.deepcopy(b))
        c={'name':name,'origin':origin,'expected':expected[name],'input_sha256':before,
           'args':args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'parsed_report':parsed,
           'parse_error':parse_error,'original_plan':plans,'board_unchanged':sha(bp.read_bytes())==before,
           'timed_out':False,'child_reaped':True,'writer_invoked':False}
        (d/'receipt.json').write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
        raw['cases'].append(c);save()
    raw['finished']=True;save()
except BaseException as e:
    raw['fatal']={'type':type(e).__name__,'detail':str(e)};save();raise
print('CAPTURE_FINISHED',len(raw['cases']),[(c['name'],c['returncode'],c['parsed_report']) for c in raw['cases']],flush=True)
