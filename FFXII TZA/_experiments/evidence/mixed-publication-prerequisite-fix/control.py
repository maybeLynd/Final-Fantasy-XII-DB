"""Exercise the actual owned prepared publish path; stop before any Git command."""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
out=W/sys.argv[1]
if out.exists():raise ValueError('fresh control output required')
driver=W/'deliver-gauge-checkpoint77.py'
sys.argv=[str(driver),'--load-only']
s=importlib.util.spec_from_file_location('actual_delivery_job',driver);d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
m=d.publisher();id=d.ID
prereq=W/'publication-ov42-gauge-and-checkpoint77-01/source-annotations-prerequisite-01.json'
original=Path.read_text;value=json.loads(original(prereq));cases=[]
class BeforeGit(Exception):pass
def before_git(argv,**kwargs):
    if argv[:2]!=['git','hash-object']:raise AssertionError('unexpected checked subprocess boundary')
    raise BeforeGit('typed guard and immutable path checks passed; stopped before Git')
m.checked_run=before_git
for name,mutation,accept in [
    ('actual-mixed-science-owner',None,True),
    ('empty-required-qualifications','empty',False),
    ('missing-scientific-source-check','missing_science',False),
    ('owner-falsely-labelled-scientific','false_science',False),
    ('partial-owner-falsely-labelled-complete','false_complete',False)]:
    v=copy.deepcopy(value)
    if mutation=='empty':v['qualifications']=[]
    if mutation=='missing_science':v['qualifications'][0]['source_checks']=[]
    if mutation=='false_science':v['qualifications'][1]['status']='VERIFIED_PREREQUISITE'
    if mutation=='false_complete':v['qualifications'][1]['status']='OWNER_TRANSITION_RECEIPTS_NOT_SCIENTIFIC_ANNOTATION'
    def read(path,*args,**kwargs):
        return json.dumps(v) if path.resolve()==prereq.resolve() else original(path,*args,**kwargs)
    Path.read_text=read
    try:
        try:m.publish_prepared(id)
        except BeforeGit as e:observed='BEFORE_GIT';diagnostic=str(e)
        except ValueError as e:observed='REFUSED_BEFORE_GIT';diagnostic=str(e)
        else:raise AssertionError('actual publication path returned without bounded control stop')
    finally:Path.read_text=original
    expected='BEFORE_GIT' if accept else 'REFUSED_BEFORE_GIT'
    if observed!=expected:raise AssertionError('upstream failure wrongly passed '+name+': '+diagnostic)
    cases.append(dict(id=name,expected=expected,observed=observed,diagnostic=diagnostic))
if (prereq.parent/'automated-publication-attempt-01.json').exists():raise AssertionError('control reached actual publisher')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out.write_text(json.dumps(dict(status='ACTUAL_MIXED_PREREQUISITE_PATH_CONTROLS_PASS',cases=cases,
    delivery_sha256=sha(driver),publisher_source_sha256=sha(W/'prepare-residue-packet-publication.py'),
    controller_sha256=sha(Path(__file__)),prepared_qualification_sha256=sha(prereq),
    limits='Virtual qualification input mutations on actual owned prepared path; Git command intercepted before invocation. No board/files/Git publication/FF12 execution. Administrative owner history never becomes scientific closure; independent procedure review remains required.'),indent=2)+'\n')
print('PASS five actual publish-path controls; no Git/publication/game mutation')
