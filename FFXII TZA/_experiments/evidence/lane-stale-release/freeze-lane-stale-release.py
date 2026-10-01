"""Freeze the exact conditional stale-lane packet; no runtime-counter target."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'lane-stale-release-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'lane-stale-release-result-01.json').read_text());c=json.loads((W/'lane-stale-release-controls-01/result.json').read_text())
for tag,driver,key in [('lane-stale-release-capture-01','capture-lane-stale-release.py','driver_sha256'),('lane-stale-release-positive-01','prove-lane-stale-release.py','checker_sha256'),('lane-stale-release-controls-run-01','control-lane-stale-release.py','driver_sha256')]:
    s=json.loads((W/(tag+'.status.json')).read_text())
    if s.get('exit')!=0 or s.get(key)!=sha(W/driver) or not (W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-lane-stale-release.py'):raise ValueError('positive missing/stale')
if c.get('status')!='PASS_ACTUAL_STALE_LANE_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=4 or c['positive_reused']['sha256']!=sha(W/'lane-stale-release-result-01.json'):raise ValueError('controls incomplete/stale')
if any(x['exit']==0 or not x['expected_error_seen'] or not x['result_absent'] for x in c['refusals']):raise ValueError('refusal incomplete')
pins=r['source_pins']+r['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('source/receipt changed')
paths={x['path'] for x in pins}|{'lane-stale-release-method-01.json','lane-stale-release-result-01.json','prove-lane-stale-release.py','control-lane-stale-release.py','freeze-lane-stale-release.py'}
paths|={tag+s for tag in ['lane-stale-release-positive-01','lane-stale-release-controls-run-01'] for s in ['.stdout','.stderr','.status.json']}
paths|={p.relative_to(W).as_posix() for p in (W/'lane-stale-release-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/lane-stale-release/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('qualified native path budget exceeded; no unchanged publication attempt')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
    p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Requested-before-stale lane completion: direct enqueue ruled out

Method A, conditional shipping-code branch/dataflow proof. Producer valid;
required independent review and canonical incorporation pending. FullgoalACTIVE.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
imagebase120000;787 bytes in five complete local bodies. Actual shared reviewed
access-role adapter, source/annotation identities and checked invocation receipts.

Player version: if a resource lane was already marked for release before loading
finished, a stale-owner completion does not itself put that lane on the cleanup
queue. A helper previously suspected of doing this only adjusts a reference
count. This does not prove a gameplay leak: existing queue membership, other
relink paths and the game's actual sequence still matter.

Under valid records/lane0..31, normal ABI/returns, no interference and unchanged
requested bit,2E4E50 first sets loaded and clears pending, then its stale/null
owner arm passes the same sub-record and lane to2EAFA0. Already-requested takes
2EAFB2 directly toRET2EB026 before any call or memory write. Thus it neither
creates nor removes existing sweep membership. It does not unpin or register
on that local stale branch. No callee-opaque effect is needed for this early arm.

Distinguishing original positive: requested0/loaded1 marks and publishes a node
to sweep head0215FD90. Requested0/unloaded pending-or28 marks without enqueue;
inactive leaves it unchanged. Eight relevant Boolean partitions express these
verified branch consequences; they are not eight original executions.

2EB890 searches the owner, validates generation and updates only the laneWORD
at sub-record+E0+2*lane. The decrement wraps as16-bit arithmetic; the next test
uses the signed result, and clamp0 additionally requires a bit in+38|+3C. It has
no calls or queue/global writes. It is on the valid-owner/nonzero-handle requested
branch of completion, not the stale branch, and cannot locally repair enqueue.

Reached2E6A80 releases only requested AND loaded lanes, then unlinks its node
without testing pending+34. It conditionally frees the sub-record only when
loaded+24|mask28 is0. This raises a later-completion relink requirement under
specific interleavings; the scheduler, other producers and opaque callee effects
are outside this proof.2E2660 clears the masks and binds owner generation from
the free list; no direct sweephead store occurs there.

Do not infer unconditional leak, safety, natural stale reachability, eventual
release, handle pin/free completion, general invalid-index safety or allOV25/21
closure. Prior membership is explicitly variable. The original callback has
low16 lane/high16 record-index decoding; our valid-lane premise is essential.

Reproduce capture/reducer in a writable copy within this repository with the
verified shipping EXE available and fresh output names. Four actual CLI controls
reuse the sufficient positive and refuse failed capture, missing source, inverted
request gate and changed count operation with no result. Missing is not empty.
No game/native/emulated execution, PC control, save/config/reference mutation.

Consumers: FABLE existingOV25 carried lane question, OPUS conditional release
retry/ownership contract, FRONTIER lifetime preparation. Next discriminator if
natural progress is required: actual list relink producers and callback lifetime
invariant, by source analysis before a live collector. No new general observer.
''',encoding='utf8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='FROZEN_PRODUCER_VALID_INDEPENDENT_PENDING',members=members,member_count=len(members),native_path_units=units,exe_sha256=r['exe_sha256'],method='A STATIC_ONLY',native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0),indent=2)+'\n')
print(json.dumps(dict(folder=out.name,members=len(members),manifest_sha256=sha(out/'manifest.json'),native_path_units=units)))
