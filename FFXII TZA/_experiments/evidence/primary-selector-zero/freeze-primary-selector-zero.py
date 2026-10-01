"""Freeze reference caller's constant selector proof, exact sources/receipts."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'primary-selector-zero-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'primary-selector-zero-result-01.json').read_text());c=json.loads((W/'primary-selector-zero-controls-01/result.json').read_text())
for tag,d,key in [('primary-selector-zero-capture-01','capture-primary-selector-zero.py','driver_sha256'),('primary-selector-zero-positive-01','prove-primary-selector-zero.py','checker_sha256'),('primary-selector-zero-controls-run-01','control-primary-selector-zero.py','driver_sha256')]:
 st=json.loads((W/(tag+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get(key)!=sha(W/d) or not(W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-primary-selector-zero.py'):raise ValueError('positive missing/stale')
if c.get('status')!='PASS_ACTUAL_SELECTOR_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=3 or c.get('checker_sha256')!=r['checker_sha256'] or c['positive_reused']['sha256']!=sha(W/'primary-selector-zero-result-01.json'):raise ValueError('controls incomplete/stale')
if any(x.get('exit')==0 or not x.get('expected_error_seen') or not x.get('result_absent') for x in c['refusals']):raise ValueError('concrete refusal failed')
pins=r['source_pins']+r['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('required source changed')
paths={x['path'] for x in pins}|{'primary-selector-zero-method-01.json','primary-selector-zero-result-01.json','prove-primary-selector-zero.py','control-primary-selector-zero.py','freeze-primary-selector-zero.py'}
paths|={tag+s for tag in ['primary-selector-zero-positive-01','primary-selector-zero-controls-run-01'] for s in ['.stdout','.stderr','.status.json']}
paths|={p.relative_to(W).as_posix() for p in (W/'primary-selector-zero-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/primary-selector-zero/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md'];units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('native path budget exceeded')
if any(not(W/p).is_file() for p in paths):raise ValueError('required member missing')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
 p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Original32FCA0 always selects the indexed primary loader

Method A:3 original shipping bytes plus the retained complete caller range.
Producer valid, independent acceptance and canonical incorporation pending.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No native/emulated/live run or repeated caller census.

The proposed initialized option/state question has a cheaper answer.
Original5C5230 is XOR EAX,EAX;RET. This is the verified shipping leaf, not an
injected fixture stub. It returns0 independent of incoming arguments/state.
All three32FCA0 prefix classes zero localR13D: either direct mode-gate arm
clears it, or TEST of that0 givesZF1 and SETNE writes0 into an already cleared
register. The complete original caller has no other local assignment before
the later selector TEST. Intermediate normally returning ABI-compliant callees
preserve nonvolatileR13/R14; exceptions/ABI violations remain outside the proof.

At33000C TEST R13D runs BEFORE33000F restores the saved caller register. Only
MOVs intervene beforeJE330030, so its flags survive. The branch selects330310,
not3306E0, on normal unmodified execution of this caller. Restoring a nonzero
saved R13 cannot reverse the earlier condition. This removes a live option/state
observation need for this edge. It does not prove3306E0 unreachable from every
other caller or establish actual entry, payload success or owner lifetime.

Reproduce the reducer into a fresh result with existing analysis Python:

    python <packet>/prove-primary-selector-zero.py <fresh.json>

Exact full image, original leaf/caller bytes and annotations are checked. The
actual capture uses the reviewed shared role adapter and its store,LEA,RMW
controls. Three actual CLI refusals reuse the positive: failed capture, a
coherent nonconstant leaf, and SETNE->SETE with unchanged instruction count.
Changed code or failed prerequisites cannot yield a semantic result. Producer
controls are distinct from independent project acceptance.

FABLE/OPUS's existing bts consumer tasks take this additive caller selection
after scoped independent SPEC review. Earlier primary-admission35525e9 is
conditional on null size override; retain that limit. Existing DG6 says the
override array is cleared and no producer was found, with an indirect-pointer
instrument blind spot. Consume that existing result; do not rerun its census or
silently promote the absence claim to an unlimited alias proof.

Player version: the normal loader's switch always chooses the indexed file
path in the reference game code. We can settle that part without opening FF12.
Other loading paths and actual script availability are still separate questions.

Cleanup: finite shipping-file reads/private refusal copies only; no PC/game/
input/instrument/save/config/reference or peer-process changes. Full goal
ACTIVE/NOT_MET; menu allowance remains spent/unapproved, EXP127 remains invalid.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native units',units,'manifest',sha(out/'manifest.json'))
