"""Freeze only a completed source proof and its actual relevant controls."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'title-root-retirement-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'title-root-retirement-result-01.json').read_text());c=json.loads((W/'title-root-retirement-controls-01/result.json').read_text())
for n,d,k in [('title-root-retirement-positive-01','prove-title-root-retirement.py','checker_sha256'),('title-root-retirement-controls-run-01','control-title-root-retirement.py','driver_sha256'),('title-root-retirement-capture-02','capture-title-root-retirement.py','driver_sha256')]:
 st=json.loads((W/(n+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get(k)!=sha(W/d) or not (W/(n+'.stdout')).read_bytes().strip() or (W/(n+'.stderr')).read_bytes().strip():raise ValueError('required actual invocation failed or stale '+n)
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-title-root-retirement.py') or r.get('helper_sha256')!=sha(W/'prove-title-queue-consumption.py'):raise ValueError('required positive incomplete/stale')
if c.get('status')!='PASS_ACTUAL_TITLE_RETENTION_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=3 or c.get('checker_sha256')!=r['checker_sha256'] or c.get('positive_reused',{}).get('sha256')!=sha(W/'title-root-retirement-result-01.json'):raise ValueError('required concrete controls incomplete/stale')
if any(q.get('exit')==0 or q.get('result_absent') is not True or q.get('expected_error_seen') is not True for q in c['refusals']):raise ValueError('required refusal failed')
pins=r['source_pins']+r['retained_source_pins']+r['required_invocation_receipts']
for p in pins:
 if sha(W/p['path'])!=p['sha256']:raise ValueError('required source/receipt moved')
paths={p['path'] for p in pins}|{'title-root-retirement-method-01.json','title-root-retirement-result-01.json','prove-title-root-retirement.py','control-title-root-retirement.py','freeze-title-root-retirement.py','capture-title-root-retirement-before-binding-preflight-fix-01.py'}
paths|={n+s for n in ['title-root-retirement-capture-01','title-root-retirement-positive-01','title-root-retirement-controls-run-01'] for s in ['.stdout','.stderr','.status.json']}
paths|={p.relative_to(W).as_posix() for p in (W/'title-root-retirement-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/title-root-retirement/'+p for p in sorted(paths|{'README.md','manifest.json','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md'];units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('native reviewed path budget exceeded before copy')
if any(not (W/p).is_file() for p in paths):raise ValueError('required member missing')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for name in sorted(paths):
 t=out/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,t)
(out/'README.md').write_text('''# Title closing is distinct from local notification revocation

Method A: retained original title/constructor/notification/release bytes plus two
missing root bodies. Producer checked; independent review and incorporation are
pending. Original EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No native, emulated or live game execution.

The actual title initialization starts its two requests, then loads root0208EA28
at394117 and passes this asset to244960. If parentless, attachment248220 stores
the parent and propagates bit5 directly from root flags40. Original247AE0 creates
roots0208EA20/28/30; their message1 handler2445D0 ORs23 into flags40. Successful,
valid, unchanged initialization therefore makes root retention applicable to the
title asset. It does not prove an observed initialized root or natural timing.

245020 broadcasts message18 before REREADING bit5. Still set:2473F0(self,0),
clear bit1/setbit10, retain storage. Clear:tail2482E0. Message/opaque helper
mutation remains a premise; initial root membership alone is not perpetual
lifetime. The requests precede attachment, which also limits timing inferences.

After its established ordinary sealed/equal/custom-zero ticket gates,2495C0 reads
raw owner ticket+8, rejectsNULL, reads current handler owner+0, rejectsNULL and
sends16. The full byte-qualified owner-use window reads no owner flags40,
generation or publication02AEE4C0. Ticket flags are distinct from owner flags.
Title394070 message16 simply ORs readybit0 at+C0. A valid retained post-teardown
boundary with that handler unchanged and ordinary gates satisfied permits this
local ready-bit write despite bit10 and cleared publication. This refutes inherent
local revocation; it is a conditional source witness, NOT observed late delivery.

Physical2482E0 nulls the handler before disposing storage. A still-backed,
unreused pool slot withNULL suppresses notification. Released slots can be
selected by244F50 and reinitialized by2465F0 with a new handler; NULL is not a
permanent identity token. No claim surviving tickets or actual ABA/reuse occurs.
Heap validity, external cancellation/drain, whole scheduling and natural pending
teardown remain open. No arbitrary teardown replay or safety guarantee follows.

The reducer reuses accepted sender/guard inputs and SECTION04 original code,
not its scripted native fixtures. Retained TXT is byte matched/redecoded and its
memory roles use the reviewed shared adapter in the actual path. New root export
uses the same reviewed adapter and three store/LEA/RMW controls. Complete source
identity, actual capture exit/stdout/stderr and positive/control receipts are checked.

Reproduce only into a fresh output with the existing analysis Python:

    python <packet>/prove-title-root-retirement.py <fresh.json>

Three actual CLI refusals reuse the positive: failed capture exit, coherently
changed root retention opcode, and missing ordinary owner body. No failed or
zero-case run passes. First export preparation used a mistyped handwritten LEA
displacement and refused BEFORE export; original driver/exit1 are retained. The
fix derives displacement from the named target, and capture02 is the valid export.
No earlier conclusion depended on that failed preflight. Driver/input/case/result
and all refusal inputs are immutable. Controls are not independent acceptance.

FABLE owns title OV31 conditional root/deferral incorporation and OV29 semantics;
OPUS owns raw-owner/current-handler contracts and lifetime limits. Independent
review must check primary source and preserve these premises before consuming.
Next discriminator: can original ticket retirement/scheduling prevent a surviving
ordinary ticket across physical handler null/reuse? Read cancellation/queue source
before designing automatic process observation. Natural overlap still requires
its own sufficient evidence, not historical RT labels or more positive samples.

Player version: closing the title screen can leave its object in memory briefly.
The loading notification routine calls its current handler if the ticket permits it;
it does not itself check whether the title object is closing. Other systems may
prevent a late call. That coordination is still being investigated.

Only finite offline scripts/disposable controls; no PC/game/input/instrument/
save/config/reference or unrelated-process changes. Full goal ACTIVE/NOT_MET;
wholeOV closures0. Parked menu allowance unchanged; EXP127 stays invalid.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A RETAINED/STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native units',units,'manifest',sha(out/'manifest.json'))
