"""Freeze one bounded bank-dispatch proof after its actual prerequisites pass."""
import hashlib, importlib.util, json, pathlib, shutil, subprocess

W=pathlib.Path(__file__).resolve().parent;out=W/'texture-async-bank-dispatch-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'texture-async-bank-dispatch-result-01.json').read_text())
c=json.loads((W/'texture-async-bank-dispatch-controls-01/result.json').read_text())
for prefix,driver,key in [('texture-async-bank-dispatch-positive-01','prove-texture-async-bank-dispatch.py','checker_sha256'),('texture-async-bank-dispatch-controls-run-01','control-texture-async-bank-dispatch.py','driver_sha256')]:
    status=json.loads((W/(prefix+'.status.json')).read_text())
    if status.get('exit')!=0 or status.get(key)!=sha(W/driver) or not (W/(prefix+'.stdout')).read_bytes().strip() or (W/(prefix+'.stderr')).read_bytes().strip():raise ValueError('required actual producer/control invocation failed or missing')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-texture-async-bank-dispatch.py') or r.get('helper_sha256')!=sha(W/'prove-title-queue-consumption.py'):raise ValueError('required positive result incomplete/stale')
if c.get('status')!='PASS_ACTUAL_BANK_DISPATCH_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=4 or c.get('checker_sha256')!=r['checker_sha256'] or c.get('positive_reused',{}).get('sha256')!=sha(W/'texture-async-bank-dispatch-result-01.json'):raise ValueError('required concrete controls incomplete/stale')
if any(q.get('exit')==0 or q.get('result_absent') is not True or q.get('expected_error_seen') is not True for q in c['refusals']):raise ValueError('required concrete refusal failed')
spec=importlib.util.spec_from_file_location('bank_freeze_actual_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
for pin in r['source_pins']:
    if sha(W/pin['path'])!=pin['sha256']:raise ValueError('required original source moved')
    S.validate(json.loads((W/pin['path']).read_text()))
for pin in r['required_invocation_receipts']:
    if sha(W/pin['path'])!=pin['sha256']:raise ValueError('required original invocation receipt moved')
paths={p['path'] for p in r['source_pins']}|{p['path'] for p in r['required_invocation_receipts']}
paths|={'texture-async-bank-dispatch-method-01.json','texture-async-bank-dispatch-result-01.json','prove-texture-async-bank-dispatch.py','control-texture-async-bank-dispatch.py','freeze-texture-async-bank-dispatch.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py'}
paths|={'texture-async-bank-dispatch-positive-01'+suffix for suffix in ('.stdout','.stderr','.status.json')}
paths|={'texture-async-bank-dispatch-controls-run-01'+suffix for suffix in ('.stdout','.stderr','.status.json')}
paths|={p.relative_to(W).as_posix() for p in (W/'texture-async-bank-dispatch-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/texture-async-bank-dispatch/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('required supported native path budget exceeded before copy')
if any(not (W/p).is_file() for p in paths):raise ValueError('required packet member missing before copy')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in sorted(paths):
    target=out/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,target)
(out/'README.md').write_text('''# Texture bank submission is distinct from key execution

Method A STATIC_ONLY; producer checked, independent review/canonical consumption
pending. Original EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. Six exact byte ranges close three normal CFGs and a 15-byte tail
callback; no native/emulated/game code executed and no stub establishes effects.

185A50 passes its pre-call DWORD bank[1F7F590] zero-extended in R8D, callback
186610 in RDX and incoming RCX to5FEA50. After normal return it rereads the
global bank, INC32/AND3/stores it and returns the new bank in EAX. It overwrites
submission status without testing it. Under unchanged/no-interference calls,
four invocations rotate all four residues; those invocations are not frames.

5FEA50 saves callback/data, rejects NULL callback with1, otherwise calls600B30
with EDX0/R8D1 and conditionally context vslot10 if AL0. These are opaque
boundaries. Afterward it attempts a128B cursor reservation, wrapping to begin
when needed under unsigned bounds. A nonNULL reservation sets batch begin if
unset/end and writes DWORD opcode2F at0, QWORD callback at8 and data at10,
then returns0. Failed reservation returns0D without payload writes. This body
contains no direct call of the saved callback, but opaque callees are not a
transitive no-callback proof. A conditional post-opaque empty-buffer state
produces0D while185A50 still advances; not a natural allocation-failure witness.

186610 reads DWORD[input+10], loads the CURRENT context[1F7F5B8] and tails
62EBC0. The stored shape is compatible with passing the command's address,
but the actual opcode2F interpreter and that callback ABI remain OPEN. A record
written is not a command executed. The context is not saved in this command.

62EBC0 selects one bank at context+56*zeroextend32(EDX), starts at bank+10 and
ends at sentinel bank+8. It calls key[node+20] virtual slot0 BEFORE16D6D0
computes the live tree successor. This is different from1F7F598/186230's pair
queue with a captured end. On normal completion it rereads root bank+18, calls
220390 for a subtree and allocator record bank+30 slot18(record,node,28h),
then resets the links/root/color/count28. Callback/tree mutation, subtree and
allocator effects remain opaque. Container count28 is not texture element38,
nor GPU completion. Finite valid stable tree/buffer/ABI premises are explicit.

Raw capture uses the shared reviewed role adapter and actual byte re-decoding.
Complete normal fragments are matched through exact parent triples, not shared
unwind addresses. The candidate retool view supplied positive address discovery
only: no all-writer/caller, indirect-reference or negative-coverage claim.
Reproduce the local proof with existing analysis Python and fresh output:

    python <packet>/prove-texture-async-bank-dispatch.py <fresh.json>

Four actual CLI refusals reuse the positive: consistently changed opcode,
consistently moved data offset, missing normal consumer tail and failed capture
exit. Failed upstream invocation cannot become semantic PASS. The default
freezer also checks actual producer/control exits, nonempty positive output,
current driver/result/raw identities and concrete refusal results. Driver,
input, case, result and invocation receipts remain immutable. Producer controls
are not independent review, and publication is not canonical acceptance.

OPUS owns the128B record/callback/return ABI and distinct counters. FABLE owns
bank submission versus execution, traversal and lifetime/scheduling premises.
Next discriminator: original opcode2F interpreter branch, callback argument and
command stepping; then natural initialized caller/scheduling if still needed.
Actual initialized bank/context, reachability, timing/thread, native success,
natural pending work in another bank, counter38 writers and lifetime stay OPEN.

Player version: the game writes a request and moves to the next work bank. A
failed request still moves the bank. We know how the bank-processing routine
handles keys; we have not yet proved which interpreter executes that request.

Cleanup: only read-only shipping/retained files and disposable control copies;
finite foreground scripts terminate. No PC/game/input/native/instrument/save/
config/reference or unrelated-process mutation. Parked menu spent/unapproved;
EXP127 invalid. Full L1+L2 goal ACTIVE/NOT_MET; no wholeOV row closed here.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native path units',units,'manifest',sha(out/'manifest.json'))
