"""Exercise the real prepare() path on private synthetic board/files.

No actual publication claim, board write, or database write. The stand-in board
only admits the immutable-input gate so the copied-review prerequisite is tested.
"""
import hashlib, importlib.util, json, tempfile, sys
from pathlib import Path
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
W=P.parent
ROOT=next(p for p in P.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
producer=W/'prepare-residue-packet-publication.py'
spec=importlib.util.spec_from_file_location('guarded_publisher_path_control',producer)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=P/'publisher-path-control-01.json'
if out.exists():raise ValueError('existing control receipt: never replace')
receipt=dict(method='synthetic private preparation invocation, no publication or semantic credit',
             producer_sha256=hashlib.sha256(producer.read_bytes()).hexdigest(),
             controller_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
with tempfile.TemporaryDirectory(prefix='astra_review_path_') as tmp:
    base=Path(tmp);root=base/'root';work=base/'work';frozen=work/'frozen';frozen.mkdir(parents=True)
    document=frozen/'fable-render-control-REVIEW.md'
    document.write_bytes(b'[original script](rv_clear.py)\n')
    data=document.read_bytes()
    manifest=dict(members=[dict(path=document.name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())])
    mf=frozen/'manifest.json';mf.write_text(json.dumps(manifest))
    id='SYNTHETIC-ASTRA-RENDER-LINK-CONTROL'
    resources=[dict(key='@publication'),dict(key='file:database/ffxii tza/_index/_inbox/astra.md'),
               dict(key='file:database/ffxii tza/_experiments/evidence/control')]
    board=base/'board.json';board.write_text(json.dumps(dict(tasks=[dict(id=id,status='ACTIVE',agent='ASTRA',resources=resources)])))
    inbox=root/'Database/FFXII TZA/_index/_inbox/ASTRA.md';inbox.parent.mkdir(parents=True);inbox.write_bytes(b'private original handoff\n')
    m.ROOT=root;m.W=work;m.team.BOARD=board
    m.team.board_status=lambda p:(True,'private stand-in only')
    m.JOBS[id]=dict(slug='control',pairs=[['frozen','control',1,hashlib.sha256(mf.read_bytes()).hexdigest()]])
    try:m.prepare(id)
    except ValueError as e:
        receipt.update(exception=repr(e),expected_diagnostic='copied render review link unresolved before copying' in str(e))
    else:raise AssertionError('real prepare path accepted missing referent')
    receipt.update(preparation_output_absent=not (work/'publication-control-01').exists(),
                   canonical_output_absent=not (root/'Database/FFXII TZA/_experiments/evidence/control').exists(),
                   handoff_unchanged=inbox.read_bytes()==b'private original handoff\n')
    if not all(receipt[k] for k in ['expected_diagnostic','preparation_output_absent','canonical_output_absent','handoff_unchanged']):
        raise AssertionError('missing-review prerequisite did not stop actual prepare before writes')
    # Positive gate control: local referent exists, the same default helper now reads it.
    (frozen/'rv_clear.py').write_bytes(b'# private script identity control\n')
    positive=m.verify_copied_render_review_links(frozen,root/'Database/FFXII TZA/_experiments/evidence/control')
    if positive['status']!='VERIFIED_COPIED_REVIEW_LINKS' or len(positive['links'])!=1:
        raise AssertionError('positive detection control failed')
    receipt['positive_helper_control']=positive
receipt['status']='INVOCATION_PATH_CONTROL_PASS'
out.write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: real prepare prerequisite refused before writes; positive helper detected referent')
