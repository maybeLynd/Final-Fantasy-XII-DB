"""Freeze the new selected higher-caller proof, retaining upstream receipts."""
import hashlib,importlib.util,json,pathlib,shutil
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-resize-drain-caller-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'texture-resize-drain-caller-result-01.json').read_text());c=json.loads((W/'texture-resize-drain-caller-controls-01/result.json').read_text())
if not r.get('producer_complete') or r['checker_sha256']!=sha(W/'prove-texture-resize-drain-caller.py') or c['status']!='PASS_ACTUAL_HIGHER_RESIZE_REFUSALS_INDEPENDENT_PENDING' or len(c['refusals'])!=4 or any(q['exit']==0 or not q['result_absent'] or not q['expected_error_seen'] for q in c['refusals']):raise ValueError('required producer/control incomplete')
s=importlib.util.spec_from_file_location('actual_annotations',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
for q in r['source_pins']:
    if sha(W/q['path'])!=q['sha256']:raise ValueError('source preimage changed')
    S.validate(json.loads((W/q['path']).read_text()))
for q in r['prerequisite_result_pins']:
    if sha(W/q['path'])!=q['sha256'] or json.loads((W/q['path']).read_text()).get('producer_complete') is not True:raise ValueError('upstream result changed/failed')
paths=[q['path'] for q in r['source_pins']+r['prerequisite_result_pins']]
paths+=['capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','capture-texture-resize-drain-caller.py','prove-texture-resize-drain-caller.py','control-texture-resize-drain-caller.py','freeze-texture-resize-drain-caller.py','texture-resize-higher-caller-preparation-04.json','prove-texture-copy-capacity-caller.py','prove-texture-copy-construction.py','prove-title-cleanup-count-selector.py','texture-resize-drain-caller-result-01.json']
paths += [p.relative_to(W).as_posix() for p in sorted((W/'texture-resize-drain-caller-controls-01').rglob('*')) if p.is_file()]
paths += [p.relative_to(W).as_posix() for pattern in ('texture-resize-drain-caller-capture-01.*','texture-resize-drain-caller-positive-01.*','texture-resize-drain-caller-controls-invocation-01.*') for p in sorted(W.glob(pattern))]
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in dict.fromkeys(paths):
    p=out/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,p)
(out/'README.md').write_text("""# Original texture higher caller: wait before selected resize

Method A STATIC_ONLY; producer checked, independent acceptance and canonical
consumption pending. Question: can628100 reach627DA0 before its same-object
62B100 wait returns? Complete153-byte body and three chained normal fragments
show it cannot. The wait call and argument setup dominate the resize. The
BC-gated62BCB0 failure exits before both; not every invocation runs the wait.

This is a source call-order invariant, not a timing sample. Under stable valid
oldcount>=1/storage and normal terminating callees, retained62B100 visits each
old element and observes its signed-nonpositive counter before proceeding.
These observations are sequential. Negative counters also pass. It does not
prove simultaneous zeros, no pending jobs, no keys, no later counter rise,
termination, cancellation or safe lifetime. Sleep identification/accepted
OPUS stride/type/constructor evidence is reused, not rerun or counted here.

The lower selected resize already provesK=min(newN,masked oldcount), preserving
copied counter/userdata and conditionally freeing old storage. Those immutable
producer receipts/raw inputs are required and requalified, not new experiments.
Their independent reviews remain separately scoped. The new proof must not
turn its earlier local absence of waits into an absence in higher callers.

After successful resize this higher caller selects NULL/inline/pointer for
masked count0/1/>1 and reads QWORD[selected]. With valid positive oldcount,
requestednewN0, successful normally returning callees and no interfering/alias
writes, a null read follows. This conditional source discriminator creates an
upstream positive-count-domain obligation. It is not proof the game supplies0,
a natural crash or arbitrary malformed-input safety. Native service and
resource-binding effects, full upstream callers/count writers remain OPEN.

Reproduce with existing analysis Python and a fresh result:

    python <packet>/prove-texture-resize-drain-caller.py <fresh.json>

Whole shipping-body hashes, decoded annotation/access-role agreement, actual
reviewed shared adapter, raw unwind chains, complete CFG and domination are
checked by the actual CLI. Missing/changed/failed required upstream receipts
cannot pass. Four CLI controls reuse one positive: consistent branch bypassing
wait, missing final fragment, failed capacity result and missing wait source.
They are synthetic producer controls, not native/live runs or independent
acceptance. Raw-reference preparation04 is a candidate locator only; it is not
complete caller coverage and no raw-pattern absence claim is made.

Exact EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000; raw/tool receipts and shared adapter identities are preserved.
OPUS owns selected caller/count/ABI contracts. FABLE owns wait-versus-lifetime
semantics. Next cheapest discriminator: verified628100 callers and ordinary
count-domain/interference producers. Use a source invariant before any process
collector. No initialized scene, shader/resource success, natural timing,
thread/frame, ownership/reuse or all-counter-writer proof is inferred.

No game/native/emulated/PC/input/instrument/save/config/reference writes; bounded
own scripts exited. K14 closed/accepted, menu spent/unapproved, EXP127 invalid.
No wholeOV or full-goal completion. Producer result, independent review and
canonical consumption are separate; the L1+L2/M0-M5 goal remains ACTIVE/NOT_MET.
""",encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VERIFIED_INDEPENDENT_PENDING',members=members),indent=2)+'\n')
print('Frozen higher caller',len(members),sha(out/'manifest.json'))
