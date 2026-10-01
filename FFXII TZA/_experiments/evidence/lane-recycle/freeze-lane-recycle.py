"""Freeze conditional ticket/recycler evidence without a natural safety claim."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'lane-recycle-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'lane-recycle-result-01.json').read_text());c=json.loads((W/'lane-recycle-controls-01/result.json').read_text())
for tag,driver,key in [('lane-recycle-capture-01','capture-lane-recycle.py','driver_sha256'),('lane-recycle-positive-01','prove-lane-recycle.py','checker_sha256'),('lane-recycle-controls-run-01','control-lane-recycle.py','driver_sha256')]:
    s=json.loads((W/(tag+'.status.json')).read_text())
    if s.get('exit')!=0 or s.get(key)!=sha(W/driver) or not (W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-lane-recycle.py'):raise ValueError('positive missing/stale')
if c.get('status')!='PASS_ACTUAL_RECYCLE_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=4 or c['positive_reused']['sha256']!=sha(W/'lane-recycle-result-01.json'):raise ValueError('controls incomplete/stale')
if any(x['exit']==0 or not x['expected_error_seen'] or not x['result_absent'] for x in c['refusals']):raise ValueError('refusal incomplete')
pins=r['source_pins']+r['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('source/receipt changed')
paths={x['path'] for x in pins}|{'lane-recycle-method-01.json','lane-recycle-result-01.json','prove-lane-recycle.py','control-lane-recycle.py','freeze-lane-recycle.py'}
paths|={tag+s for tag in ['lane-recycle-positive-01','lane-recycle-controls-run-01'] for s in ['.stdout','.stderr','.status.json']}
paths|={p.relative_to(W).as_posix() for p in (W/'lane-recycle-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/lane-recycle/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('qualified native path budget exceeded; no unchanged publication attempt')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
    p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Lane callback identity and conditional local recycling

Method A, verified shipping machine-code rules. Producer valid; independent
review and canonical incorporation pending. Full L1+L2 goal remains ACTIVE.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
imagebase120000; shared reviewed adapter in actual invocation path. Three new
complete bodies/1001B and retained qualified lane source reused without recapture.

Player version: a load-completion ticket names a resource slot and lane. The
completion checks who owns that slot now. That check alone does not identify
the owner that originally submitted the load. The examined recycler also does
not use the pending flag as a local guard. We still need the real service rules
that prevent old completions from arriving after reuse; no gameplay failure or
unsafe natural sequence is claimed by these local rules.

2E6EB0 builds callback2E4E50 with DWORDtag=(u16 sub-record+20<<16)|lane.
The receiver splits high16 slot/low16 lane, then compares CURRENT sub-record+5C
with CURRENT node+24 selected by CURRENT+22. No original submitting-generation
operand is in this tag. A coherent current generation is not an old-ticket fence.

Reached2E6A80 tests loaded+24|mask28 to call2E9470. Complete2E9470 never
reads pending+34 or calls another function: after normal valid-list operations
it invalidates node index and puts the same storage on free head0215FD70.
Nonzero pending alone does not prevent this local push.2E2660 subsequently
clears all32 lane handles and pending+34 while rebinding node/generation,
without making a release call for the old handles. Natural outstanding-read
or actual reuse histories are outside this proof.

The additional named group-release writer2E4000 tests requested+2C before its
enqueue arm, so an already-requested lane alone does not cause a new enqueue
there either. A different lane or other producer may queue the same shared node.
This is not a global proof of no relink producer.

Pending+34 is not sufficient evidence of a newly accepted asynchronous read:
the requester can set it on an existing-nonzero-handle arm without32E620, and
the new-request arm sets it AFTER32E620 returns. Input/call sent, queue accepted,
completion executed and consequences remain distinct.

Premises: valid array/list/metadata/lane0..31, normal ABI/returns and no
interfering writes. No natural late callback, overlap, leak, crash or universal
safety/unsafety result. Other service contracts could prevent late delivery.
Composed static paths are not native runs or evidence of gameplay reachability.

Reproduce capture/reducer in a writable copy within this repo with the exact
reference EXE and fresh outputs. Actual CLI controls reuse positive01 and
refuse failed capture, missing retained source, changed ticket field and inverted
recycler gate; no result from refusal. Producer checks, independent acceptance
and canonical incorporation remain separate. No external audit credit.

Consumers: FABLE current-owner versus submitting-owner lifetime semantics;
OPUS actual recycle site, ticket and pending preconditions; FRONTIER exact future
scheduling question. Next: original caller/service cancellation/drain guarantees
with accepted IO identity, rather than pending-bit sampling or a forced callback.
No game/PC/native/emulated execution, instruments, save/config/reference changes.
''',encoding='utf8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='FROZEN_PRODUCER_VALID_INDEPENDENT_PENDING',members=members,member_count=len(members),native_path_units=units,exe_sha256=r['exe_sha256'],method='A STATIC_ONLY',native_runs=0,live_runs=0,new_whole_runtime_rows_closed=0),indent=2)+'\n')
print(json.dumps(dict(folder=out.name,members=len(members),manifest_sha256=sha(out/'manifest.json'),native_path_units=units)))
