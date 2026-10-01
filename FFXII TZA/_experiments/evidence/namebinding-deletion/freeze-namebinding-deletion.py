"""Freeze exact local deletion evidence; producer/review/consumption separate."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'namebinding-deletion-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'namebinding-deletion-result-01.json').read_text());c=json.loads((W/'namebinding-deletion-controls-01/result.json').read_text())
for tag,driver,key in [('namebinding-deletion-capture-01','capture-namebinding-deletion.py','driver_sha256'),('namebinding-deletion-positive-01','prove-namebinding-deletion.py','checker_sha256'),('namebinding-deletion-controls-run-01','control-namebinding-deletion.py','driver_sha256')]:
    s=json.loads((W/(tag+'.status.json')).read_text())
    if s.get('exit')!=0 or s.get(key)!=sha(W/driver) or not (W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-namebinding-deletion.py'):raise ValueError('positive missing/stale')
if c.get('status')!='PASS_ACTUAL_DELETION_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=4 or c['positive_reused']['sha256']!=sha(W/'namebinding-deletion-result-01.json'):raise ValueError('controls incomplete/stale')
if any(x['exit']==0 or not x['expected_error_seen'] or not x['result_absent'] for x in c['refusals']):raise ValueError('refusal incomplete')
pins=r['source_pins']+r['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('source/receipt changed')
paths={x['path'] for x in pins}|{'namebinding-deletion-method-01.json','namebinding-deletion-result-01.json','prove-namebinding-deletion.py','control-namebinding-deletion.py','freeze-namebinding-deletion.py'}
paths|={tag+s for tag in ['namebinding-deletion-positive-01','namebinding-deletion-controls-run-01'] for s in ['.stdout','.stderr','.status.json']}
paths|={p.relative_to(W).as_posix() for p in (W/'namebinding-deletion-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/namebinding-deletion/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('qualified native path budget exceeded; no unchanged publication attempt')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
    p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Name-binding removal, completion and release drain

Method A, original shipping code; conditional local rules. Producer valid;
independent review and canonical consumption pending. Full L1+L2 goal ACTIVE.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
imagebase120000. Five full bodies and explicit command prefix/tail slices.
Shared reviewed access-role adapter used by the actual capture and verifier.

Player version: removing a script resource during loading can mark it for
deletion without freeing it immediately. When that load completes, the marked
record skips normal registration and follow-up work. The later cleanup drain
can release the backing. A second flag is an explicit exception; its natural
states and the actual timing remain open.

2EAEB0 marks18|04 and returns with no other memory write/call if18mask02=0
AND19mask04=0. Otherwise it advances the stamp, unlinks and retires the record.
19mask04 bypasses this mark-only arm; no meaning or safe natural coexistence
with a pending read is inferred from its value.

2E4D20 unpins first.18mask04 causes18|08 and skips41E580 registration.
2EA6E0 returns0 early under04; callback then sets02 and retires the record.
Without04, follow-up allocation may return1, so the callback does NOT always
set02. Successful follow-up sets02 at the reached2E60F0 completion tail.
Its full interpreter/command scheduling is outside the prefix/tail evidence.

2E6D60 requires2E6900(0)==0 and a selected retired record with nonzero+10
handle to enter this cleanup path.18mask08 OR19mask04 skips41E490 unregister,
but not2E9360. Zero-handle selected records locally bypass that cleanup call.
2E9360 requests child/secondary releases, calls369800(primary+10), then clears
the handle after normal return and recycles the record. Opaque callee effects,
actual allocator completion, natural delivery and list progress remain open.

The canonical name-binding page ALREADY establishes the16-bit stamp width.
This package corroborates it locally: INC DWORD+24 then clear WORD+26 means
(old+1)&FFFF, not an unlimited32-bit fence. Five algebraic boundary checks are
not original executions; neither a new stamp discovery nor a live guarantee.

Valid record/list/metadata, normal ABI/returns and no interfering writes are
premises. MOVSXD completion argument and low32 comparisons do not prove general
64-bit pointer placement. No malformed-state safety, actual timing, natural
equal-key/full-bank reachability, wholeOV21/OV25 closure or single-delivery claim.

Reproduce capture/reducer in a writable copy within this repo with the verified
shipping EXE present. Use fresh output names. The CLI controls reuse the sufficient
positive and preserve failed-capture, changed-mask, changed-highword-clear and
missing-source refusals with no result. Missing evidence is not empty evidence.
No native/live/game/control/save/config/reference or peer-process changes.

Consumers: FABLE deletion-policy carried residue and precise mask naming;
OPUS conditional completion/release ownership; FRONTIER existingOV25 box and
OV21 preparation. Independent verdict precedes closure. Next discriminator:
trace the producer of19mask04 before any natural pending-overlap claim.
''',encoding='utf8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='FROZEN_PRODUCER_VALID_INDEPENDENT_PENDING',members=members,member_count=len(members),native_path_units=units,exe_sha256=r['exe_sha256'],method='A STATIC_ONLY',native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0),indent=2)+'\n')
print(json.dumps(dict(folder=out.name,members=len(members),manifest_sha256=sha(out/'manifest.json'),native_path_units=units)))
