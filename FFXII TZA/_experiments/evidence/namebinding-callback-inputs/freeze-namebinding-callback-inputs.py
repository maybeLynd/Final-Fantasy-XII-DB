"""Freeze bounded original callback input proof, not gameplay error recovery."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'namebinding-callback-inputs-frozen-ready';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if out.exists():raise ValueError('immutable packet exists')
r=json.loads((W/'namebinding-callback-inputs-result-01.json').read_text());c=json.loads((W/'namebinding-callback-inputs-controls-01/result.json').read_text())
for tag,d,key in [('namebinding-callback-inputs-capture-01','capture-namebinding-callback-inputs.py','driver_sha256'),('namebinding-callback-inputs-positive-01','prove-namebinding-callback-inputs.py','checker_sha256'),('namebinding-callback-inputs-controls-run-01','control-namebinding-callback-inputs.py','driver_sha256')]:
 st=json.loads((W/(tag+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get(key)!=sha(W/d) or not(W/(tag+'.stdout')).read_bytes().strip() or(W/(tag+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale')
if r.get('producer_complete') is not True or r['checker_sha256']!=sha(W/'prove-namebinding-callback-inputs.py'):raise ValueError('positive missing/stale')
if c.get('status')!='PASS_ACTUAL_CALLBACK_INPUT_CONTROLS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=3 or len(c.get('original_detection_controls',[]))!=2 or c['positive_reused']['sha256']!=sha(W/'namebinding-callback-inputs-result-01.json'):raise ValueError('controls incomplete')
if any(not(x['exit'] and x['expected_error_seen'] and x['result_absent']) for x in c['refusals']):raise ValueError('refusal incomplete')
pins=r['source_pins']+r['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('positive prerequisite changed')
paths={x['path'] for x in pins}|{'namebinding-callback-inputs-result-01.json','namebinding-callback-inputs-method-01.json','prove-namebinding-callback-inputs.py','control-namebinding-callback-inputs.py','freeze-namebinding-callback-inputs.py'}
paths|={tag+ext for tag in ['namebinding-callback-inputs-positive-01','namebinding-callback-inputs-controls-run-01'] for ext in ['.status.json','.stdout','.stderr']}
paths|={p.relative_to(W).as_posix() for p in(W/'namebinding-callback-inputs-controls-01').rglob('*')if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/namebinding-callback-inputs/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md'];units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('qualified native path budget exceeded')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
 p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Original name-binding callback ignores incoming success and destination

Method A original-code input invariant; no native/live experiment. Producer
valid; independent review and owning FABLE/OPUS consumption pending. Full L1+L2
database goal ACTIVE/NOT_MET. Whole OV19/21 and natural IO/recovery remain OPEN.

Player version: this callback does not use the incoming read success/failure
flag. Its next steps use the resource record and followup result. Therefore a
ready flag alone cannot certify that correct file contents arrived.

Retained complete2E4D20 takes its record from sign-extended ECX. Before it
replaces R8D/RDX, it calls original32F3D0,36B130,409090. The bounded proof expands
32F3D0 into the original408B30/408B10 getters and5C5230. Six early bodies200B
newly captured through the reviewed adapter; full callback retained, not
recaptured.5C5230 is the verified shipping zero stub, not a replacement with
assumed native storage effects.

The proof traverses every branch successor over (pc, live input mask), expands
the exact early call graph and closes loops. It refuses reads of any alias of
incoming RDX/R8 before a full32/64-bit overwrite. It never assumes a CALL clears
volatile registers.409090 unconditionally replaces RDX and may replace R8D;
2E4D78 replaces R8D from record+14, and2E4D7C replaces RDX with RAX. Both incoming
arguments are dead before opaque36C660; no read or stored copy preceded them.
Consequently changing only incoming success0/1 or destination cannot alter
the modeled callback effects under fixed valid record/memory and ordinary ABI.

Ready18mask02 still depends on2EA6E0 returning0. Other registration/removal,
postprocessing, descriptor, IO/count writers and actual scheduling claims are
separate. This does not establish that a natural failed read invokes the
callback, successful content, validity of arbitrary pointers, full lifetime,
exceptions/interference/timing side channels or game-level recovery.

Exact shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
imagebase120000. Full original byte identity and reviewed memory annotations
checked. An original CMP read and MOV overwrite exercise the producer's
register-alias detection policy; they are static controls, not calls from
interior addresses. Three actual CLI refusal controls reject failed capture,
a coherent changed early call target, and missing retained callback. No failed
or partial run emits a result. Sufficient positive reused rather than repeated.

Reproduce with prove-namebinding-callback-inputs.py in a writable repo copy,
original executable/toolkit and fresh output. Producer controls and independent
acceptance remain distinct. No game/PC/native/emulated/instrument/save/config/
reference/peer-process mutation. No external run/test credit or live ratio.
''',encoding='utf8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p))for p in sorted(out.rglob('*'))if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='FROZEN_PRODUCER_VALID_INDEPENDENT_PENDING',members=members,member_count=len(members),native_path_units=units,method=r['method'],exe_sha256=r['exe_sha256'],native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0),indent=2)+'\n')
print(json.dumps(dict(folder=out.name,members=len(members),manifest_sha256=sha(out/'manifest.json'),native_path_units=units)))
