"""Freeze a bounded read-only query/early-return proof, preserving the failed producer."""
import hashlib,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for tag,pin in [('capture-mode-query-01','05173bedcdc789bdfa04524460d77967f95ad31aefe04d453ff2186f68c32008'),('prove-mode-query-02','e83a3f7b3e717c41f9a5b8292684d59c04c82e242d01c0df2d978f185cc9f9f0')]:
 s=json.loads((P/(tag+'.status.json')).read_text())
 if s['terminal'] is not True or s['exit']!=0 or s['exception'] is not None or s['driver_sha256']!=pin:raise ValueError('Required successful run missing '+tag)
s=json.loads((P/'control-mode-query-status-01.status.json').read_text())
if s['terminal'] is not True or s['exit']!=0 or s['exception'] is not None:raise ValueError('Actual CLI control incomplete')
r=json.loads((P/'result-mode-query-02.json').read_text());c=json.loads((P/'controls-mode-query-status-01/result.json').read_text())
if r.get('producer_complete') is not True or len(r['controls'])!=5 or c.get('status')!='ACTUAL_CLI_REFUSAL_WITHOUT_RESULT' or not c['result_absent']:raise ValueError('Incomplete proof/controls')
if sha(P/'prove-mode-query-boundary.v1.preimage.py')!='07640581e4e902856593ba58c34e35920a5dbc69e18f254d815282df122f316d':raise ValueError('Failed producer not preserved')
f=json.loads((P/'prove-mode-query-01.status.json').read_text())
if f['terminal'] is not True or f['exit']!=1 or (P/'result-mode-query-01.json').exists():raise ValueError('Historical failure mislabelled')
for pin in r['source_pins']:
 if sha(P/pin['path'])!=pin['sha256']:raise ValueError('Bound source changed')
out=W/'uq147-mode-query-frozen-ready'
if out.exists():raise ValueError('Immutable fresh packet required')
out.mkdir()
names=['MODE-QUERY-QUESTION.md','capture-mode-query-boundary.py','prove-mode-query-boundary.py','prove-mode-query-boundary.v1.preimage.py','control-mode-query-status.py','source-mode-query-01.json','source-boundary-01.json','source-selector-01.json','result-mode-query-02.json']
for tag in ['preview-field-mode-01','preview-field-id-01','prepare-mode-capture-01','capture-mode-query-01','prove-mode-query-01','prove-mode-query-02','control-mode-query-status-01','capture-boundary-01','capture-selector-01']:
 names += [tag+'.status.json',tag+'.stdout',tag+'.stderr']
for tag in ['field-mode','field-id','payload-access','image-access']:
 names += ['lookup-mode-'+tag+'-01'+ext for ext in ['.json','.status.json','.stdout','.stderr']]
for name in names:shutil.copyfile(P/name,out/name)
shutil.copytree(P/'controls-mode-query-status-01',out/'controls-mode-query-status-01')
shutil.copyfile(W/'prepare-uq147-mode-query-capture.py',out/'prepare-uq147-mode-query-capture.py')
shutil.copyfile(Path(__file__),out/Path(__file__).name)
(out/'README.md').write_text('''# UQ147 read-only mode query and early-return boundary

Player question: does calling the summon-cleanup routine guarantee that the summon has ended before commands are recalculated?

MethodA, original complete bytes/CFG/access composition. New133B closes377C20->3148F0->2EF2B0->2EF640. No object writes or opaque callbacks on normal paths; CALL/RET and balanced private stack operations remain premises. Source identity EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8/base120000. Three unique.pdata roots and one declared closed8B direct-target leaf without a root. Actual shared reviewed access-role adapter and shipping byte validator are used, not raw Capstone access flags. No emulator/native/game execution or runtime pointers observed.

Reference image address02164280+200+1044 forms fieldDWORD021654C4; signednegative field index clamps0. Descriptor02ADD100 NULL or unsigned index>=count returns0; otherwise byte pair at8/9+3*index yields bit15.30D9A0 mode query reads battle pointer/mode twice: first bits3/2, then field flag, then second bits1/0. Those reads are not atomic; mode1 counterexample premises require stable readable state/no interference.

With both mode reads1 and fieldhelperfalse,3138D0(0) can return for NULL roster unit or pending/committed action113 before311CF0 and its own5AD0 write. NonNULL committed113 case requires flagbit14clear or pending!=113; pending113 early return requires bit14set. Selected paths contain only private stack writes plus closed read-only query/selector calls. Therefore the invocation alone does not universally guarantee a state change. This is conditional implementation evidence, not proof that naturally initialized summonerKO reaches the supplied state or that full cleanup/command lifecycle is settled. KO admission, mode/member/status persistence across prior/later helpers, ownership/lifetime/scheduling/presentation and fullUQ147 remain OPEN. Existing same-call predecessor6d74079f is not a live observation.

Raw receipts, source identities, current producer, five specifically diagnosed source-record mutations and one actual CLI failed-upstream refusal are retained. Mutations are labelled static controls, not FF12 execution. Actual positive prove02 reused by the status control. First prove01 failed before output because its instruction-count guard said37 instead of qualified23+8+5+2=38. Its original producer07640581 and terminal1 receipts survive; corrected producer e83a3f7b adds the missing explicit descriptor-load identity. No failed run earns PASS.

Reproduction uses the declared ASTRA working layout: stage into runtime-residue-method-retriage/uq147-summoner-cleanup-order with shared validate-title-source-annotations.py7c4ea9f6, reg_tracking5fcc6484 and original capture-index-path cbfb9b43. Retained caller/selector source and upstream receipts are dependencies from6d74079f/UQ147-local-boundaries. Template capture-dismiss-selector4dde5e09 is in that predecessor. Current producer needs these source/receipt files and the shared validator; preparation/capture also needs the declared template and shared capture dependency. Use fresh output names; do not rerun the original frozen receipt. Manifest integrity is not independent acceptance or an ORACLE pre-execution seal.

Consumer: FABLE capability policy UQ147 and OPUS command seam. Independent review/canonical qualified incorporation pending. No whole formerly-runtime row closed. No PC/game/save/config/reference or peer-process change occurred, no detach/restoration required. FullL1L2+accepted deployedM0M5 goal ACTIVE/NOT_MET; menu allowance spent/unapproved,EXP127invalid,K14acceptedclosed.
''')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(schema_version=1,status='FROZEN_PRODUCER_VALID_NOT_INDEPENDENTLY_ACCEPTED',method='A bounded original CFG/effect composition',members=members),indent=2)+'\n')
print(json.dumps(dict(path=str(out),members=len(members),manifest_sha256=sha(out/'manifest.json'))))
