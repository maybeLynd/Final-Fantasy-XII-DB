"""One immutable local removal proof; qualify actual exits before copying."""
import hashlib, importlib.util, json, pathlib, shutil, subprocess

W=pathlib.Path(__file__).resolve().parent;out=W/'texture-async-removal-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'texture-async-removal-result-01.json').read_text())
c=json.loads((W/'texture-async-removal-controls-01/result.json').read_text())
for prefix,driver,key in [('texture-async-removal-positive-01','prove-texture-async-removal.py','checker_sha256'),('texture-async-removal-controls-run-01','control-texture-async-removal.py','driver_sha256')]:
    status=json.loads((W/(prefix+'.status.json')).read_text())
    if status.get('exit')!=0 or status.get(key)!=sha(W/driver) or not (W/(prefix+'.stdout')).read_bytes().strip() or (W/(prefix+'.stderr')).read_bytes().strip():raise ValueError('required actual producer/control invocation failed or missing')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-texture-async-removal.py') or r.get('helper_sha256')!=sha(W/'prove-title-queue-consumption.py'):raise ValueError('required positive result incomplete/stale')
if c.get('status')!='PASS_ACTUAL_SELECTED_BANK_REMOVAL_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=4 or c.get('checker_sha256')!=r['checker_sha256'] or c.get('positive_reused',{}).get('sha256')!=sha(W/'texture-async-removal-result-01.json'):raise ValueError('required concrete controls incomplete/stale')
if any(q.get('exit')==0 or q.get('result_absent') is not True or q.get('expected_error_seen') is not True for q in c['refusals']):raise ValueError('required concrete refusal failed')
spec=importlib.util.spec_from_file_location('removal_freeze_actual_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
for pin in r['source_pins']:
    if sha(W/pin['path'])!=pin['sha256']:raise ValueError('required original source moved')
    S.validate(json.loads((W/pin['path']).read_text()))
for pin in r['required_invocation_receipts']:
    if sha(W/pin['path'])!=pin['sha256']:raise ValueError('required original invocation receipt moved')
paths={p['path'] for p in r['source_pins']}|{p['path'] for p in r['required_invocation_receipts']}
paths|={'texture-async-removal-method-01.json','texture-async-removal-result-01.json','prove-texture-async-removal.py','control-texture-async-removal.py','freeze-texture-async-removal.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','capture-texture-async-removal-helpers-before-root-fix-01.py'}
paths|={'texture-async-removal-helpers-capture-01'+suffix for suffix in ('.stdout','.stderr','.status.json')}
paths|={'texture-async-removal-positive-01'+suffix for suffix in ('.stdout','.stderr','.status.json')}
paths|={'texture-async-removal-controls-run-01'+suffix for suffix in ('.stdout','.stderr','.status.json')}
paths|={p.relative_to(W).as_posix() for p in (W/'texture-async-removal-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/texture-async-removal/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('required supported native path budget exceeded before copy')
if any(not (W/p).is_file() for p in paths):raise ValueError('required packet member missing before copy')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in sorted(paths):
    target=out/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,target)
(out/'README.md').write_text('''# Texture cleanup removes a key from the selected current bank

Method A STATIC_ONLY. Producer checked; independent review and canonical
consumption pending. Original EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No shipping/native/emulated/game code executed; no stubs establish
native effects. Accepted OPUS caller/release facts are reused, not recounted.

Question: what does62EC70 remove, and does this establish all-bank cancellation,
completion/drain or the texture element's wait-counter changes? The complete
204B normal wrapper selects context+56*zeroextend32(incomingR8D). It performs
two unsigned pointer-key searches in that one tree, node key+20, right+0, left+8,
root bank+18, sentinel bank+8. On a valid finite ordered unique-key tree, the
lower-bound candidate and final >= comparison admit equality only. A miss exits
before decrement, helpers and allocator. No local bank-range check or loop over
other banks exists. The retained original62BD75 caller loads context[01F7F5B8]
and bank DWORD[01F7F590] at release time, skips the call for null context, and
passes the selected element+40 key. It does not pass a captured queue-time bank.

On a hit, DEC32 bank+28 precedes16D6D0(node),16DA60(node,sentinel), then the
allocator record bank+30 slot18(record,node,28h). Only the two pre-call searches
loop in the wrapper; those calls/decrement occur at most once under normal
terminating returns. The count is the container count under distinct-allocation
premises, not an explicit write to texture element+38. Four original helper
bodies close to pointer-header loads/stores at0/8/10/18 and two call-free rotation
leaves, with no global/RIP read or async-key payload dereference/callback target.
Valid contained node/sentinel links are required. The remaining allocator slot18
is opaque; native effects, transitive callback behavior and concurrent races stay
open. Header footprints are not a malformed-pointer safety proof.

A useful discriminator needs no opaque effects: key queued in bank0, current
release bank1 empty, distinct valid banks. The original normal path returns from
the empty selected bank without any call or access to bank0. Thus the wrapper
alone does not cancel every bank unconditionally. This conditional counterexample
is a source/control-flow derivation, not proof of a naturally changed bank or a
shipping use-after-free. Whether normal bank changes occur with a pending texture,
whether drain prevents this case and who writes element+38 remain separate.

The first82B pdata entry is not the whole wrapper. It was retained once; only
122B missing normal continuations were added after matching exact parent triples.
Helper preparation first guessed two no-unwind leaves and refused before any
helper capture. Original driver/failure retained, no PASS or semantic dependency.
Actual16DA60 is867B pdata root;16D6D0 is68B leaf. Adjacent16DDD0 shares an unwind
address but is not joined to that root. Its four direct calls required only two
additional call-free leaves (92/88B). Full normal CFGs close. These are byte and
instruction coverage, not experiment totals or exception-path certification.

Reproduce with existing analysis Python and a fresh output:

    python <packet>/prove-texture-async-removal.py <fresh.json>

Four actual producer CLI refusals reuse the successful positive: consistent
changed bank stride, consistent changed key offset, missing normal tail and
failed helper-capture exit. Actual default reader/freezer qualifies nonempty
source, shared reviewed byte/access roles, normal CFG, invocation exits/output,
current drivers and result/control preimages. Required upstream failure cannot
be suppressed by a later PASS. Empty successful stderr is legitimate; missing
or empty positive stdout is not. All original driver/input/case/result receipts
remain immutable. The known native publication argument limit is checked before
copy; no publisher guard, lock, byte policy or board protection is bypassed.

Consumers: OPUS owns type/contract qualifications for selected-bank removal,
ownedBlock and distinct pendingCount; FABLE owns scheduling/cancellation/lifetime.
Do not edit their claimed consumers or treat publication as independent acceptance.
Next cheapest question is original bank-global writer/caller ordering or element
counter writer closure if unowned and still needed. Existing RNG-page correction
route remains separate; this does not silently reclassify its whole family.

Player version: cleanup targets the currently selected queue bank. If a pending
update were left in another bank, this wrapper by itself would not find it. We
have proved the conditional behavior, not that players encounter that state.

Cleanup: read-only reference/retained bytes and disposable control copies; finite
foreground scripts terminate. No PC/game/input/native/instrument/save/config/
reference or unrelated-process mutation. Parked menu allowance spent/unapproved;
EXP127 invalid. Full L1+L2 goal ACTIVE/NOT_MET; no wholeOV row closed here.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native path units',units,'manifest',sha(out/'manifest.json'))
