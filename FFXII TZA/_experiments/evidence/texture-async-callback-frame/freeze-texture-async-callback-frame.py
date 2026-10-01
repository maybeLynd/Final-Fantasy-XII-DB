"""Qualify actual invocations and freeze additive retained callback ABI proof."""
import hashlib,importlib.util,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'texture-async-callback-frame-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'texture-async-callback-frame-result-01.json').read_text());c=json.loads((W/'texture-async-callback-frame-controls-01/result.json').read_text())
for prefix,driver,key in [('texture-async-callback-frame-positive-02','prove-texture-async-callback-frame.py','checker_sha256'),('texture-async-callback-frame-controls-run-01','control-texture-async-callback-frame.py','driver_sha256')]:
 status=json.loads((W/(prefix+'.status.json')).read_text())
 if status.get('exit')!=0 or status.get(key)!=sha(W/driver) or not (W/(prefix+'.stdout')).read_bytes().strip() or (W/(prefix+'.stderr')).read_bytes().strip():raise ValueError('required actual producer/control invocation failed or missing')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-texture-async-callback-frame.py') or r.get('helper_sha256')!=sha(W/'prove-title-queue-consumption.py'):raise ValueError('required positive incomplete/stale')
if c.get('status')!='PASS_ACTUAL_CALLBACK_FRAME_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=4 or c.get('checker_sha256')!=r['checker_sha256'] or c.get('positive_reused',{}).get('sha256')!=sha(W/'texture-async-callback-frame-result-01.json'):raise ValueError('required controls incomplete/stale')
if any(q.get('exit')==0 or q.get('result_absent') is not True or q.get('expected_error_seen') is not True for q in c['refusals']):raise ValueError('required concrete refusal failed')
spec=importlib.util.spec_from_file_location('callback_frame_freeze_roles',W/'validate-title-source-annotations.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
for pin in r['source_pins']:
 if sha(W/pin['path'])!=pin['sha256']:raise ValueError('required original source moved')
 S.validate(json.loads((W/pin['path']).read_text()))
for pin in r['required_invocation_receipts']:
 if sha(W/pin['path'])!=pin['sha256']:raise ValueError('required original prerequisite receipt moved')
paths={p['path'] for p in r['source_pins']+r['required_invocation_receipts']}
paths|={'texture-async-callback-frame-method-01.json','texture-async-callback-frame-result-01.json','prove-texture-async-callback-frame.py','control-texture-async-callback-frame.py','freeze-texture-async-callback-frame.py','capture-index-path.py','validate-title-source-annotations.py','prove-title-queue-consumption.py','prove-texture-async-callback-frame-before-focused-source-fix-01.py'}
for prefix in ('texture-async-callback-frame-positive-01','texture-async-callback-frame-positive-02','texture-async-callback-frame-controls-run-01'):
 paths|={prefix+suffix for suffix in ('.stdout','.stderr','.status.json')}
paths|={p.relative_to(W).as_posix() for p in (W/'texture-async-callback-frame-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/texture-async-callback-frame/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('required supported native path budget exceeded before copy')
if any(not (W/p).is_file() for p in paths):raise ValueError('required packet member missing before copy')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in sorted(paths):
 target=out/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,target)
(out/'README.md').write_text('''# Queued bank reaches a transient callback frame

Method A RETAINED STATIC_ONLY. Producer checked; independent/canonical acceptance
pending. Reuses FABLE's published BG11 answer7e4af33d5 and ASTRA's retained source
confirmation, rather than recapturing or repeating that closed question. Original
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. New composition with bank-dispatch e2506a55e2e59cbe2a111eed7a79ea57888f5338
supplies the local ABI connection that packet correctly left unproved.

Original60A410's opcode2F arm at60A899 reads raw command callback+8 and data+10.
It builds a24B stack frame: field0=executorR14, field8=&stackSlot[rsp+50],
field10=QWORD command+10. At60A8D6 it invokes the callback with RCX=&frame,
NOT the raw128B command. Optional60B750 flush before construction remains an
opaque normally returning/native-ABI boundary; no native effects inferred.

For185A50->5FEA50->186610, command+10 contains the pre-submission DWORD bank
zero-extended throughR8D.186610 reads DWORD frame+10 intoEDX and freshly loads
global context1F7F5B8 intoRCX before tailing62EBC0. It therefore selects the
queued bank, not current bank-global1F7F590 at callback time. Context is current,
bank is captured. This is conditional original-code dataflow, not actual live
scheduling, pointer identity/stability/lifetime or thread/event observation.

Normal callback return resumes at60A8D9, jumps to128B source/biased-cursor
advance and compares the end before next dispatch. This local order does not
prove synchronous completion with the submitting caller, frame frequency,
initialized producer/consumer storage or a safe context change. A transient
stack frame is not a persistent portable object. Counter38 writers/drain,
natural pending work, all-bank cancellation and native graphics effects remain
OPEN. We do not close a wholeOV row or recount the already-retired BG11 request.

Reproduce using existing analysis Python and fresh output:

    python <packet>/prove-texture-async-callback-frame.py <fresh.json>

The checker verifies exact retained shipping ranges and actual reviewed access
roles/byte decoding, original two-level dispatch table bytes and concrete frame/
callback operations. It qualifies the actual bank producer's exit/result/source
preimages. The retained BG11 capture is focused source, not the newer wrapper
schema. First positive01 refused that schema mismatch before any result; original
driver and failed invocation retained. The fix qualifies the actual focused
bytes/roles/identity and preserves the narrower branch scope; it does not alter
raw input or declare the full interpreter/exception paths certified. It also
uses the existing validator's real ROOT interface. Positive02 is valid.

Four actual producer CLI refusals reuse positive02: consistently moved frame
data load, consistently narrowed bank read, missing frame store and failed bank
producer exit. All require nonzero exit, expected error and absent result.
Default freezer requires actual successful producer/control invocation receipts
and current immutable driver/input/result hashes. Empty stderr is normal; absent
positive stdout is not. Producer controls are not independent acceptance.

Return this additive ABI result through the existing bank-dispatch SPEC/OPUS/
FABLE tasks, not duplicate their census or edit their claimed consumers. OPUS
needs separate128B command/24B callback-frame types and bank/context read times;
FABLE needs the captured-bank/current-context traversal/scheduling premises.
Next: selected original submit/flush/drain caller ordering or element38 writer
closure if still needed/unowned, before considering real-process scheduling.

Player version: a queued texture update remembers which work bank it belongs
to, even after the game advances its current bank. The callback fetches its
scheduler context later, so context lifetime is still an unresolved requirement.

Cleanup: finite offline reducer and disposable control files; no new capture,
native/emulated/live execution or PC/game/input/instrument/save/config/reference/
unrelated-process mutation. Menu spent/unapproved, EXP127 invalid, K14 accepted;
fullL1+L2 goal ACTIVE/NOT_MET. Publication/review waits block only their consumers.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A RETAINED STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native path units',units,'manifest',sha(out/'manifest.json'))
