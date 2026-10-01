"""Freeze ARD width proof with complete actual invocation and refusal receipts."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'ard-callback-width-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'ard-callback-width-result-01.json').read_text());c=json.loads((W/'ard-callback-width-controls-01/result.json').read_text())
for n,d,k in [('ard-callback-width-positive-01','prove-ard-callback-width.py','checker_sha256'),('ard-callback-width-controls-run-01','control-ard-callback-width.py','driver_sha256'),('ard-callback-width-capture-01','capture-ard-callback-width.py','driver_sha256')]:
 st=json.loads((W/(n+'.status.json')).read_text())
 if st.get('exit')!=0 or st.get(k)!=sha(W/d) or not (W/(n+'.stdout')).read_bytes().strip() or (W/(n+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale '+n)
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-ard-callback-width.py') or r.get('helper_sha256')!=sha(W/'prove-title-queue-consumption.py'):raise ValueError('required positive failed/stale')
if c.get('status')!='PASS_ACTUAL_ARD_WIDTH_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=3 or c.get('checker_sha256')!=r['checker_sha256'] or c.get('positive_reused',{}).get('sha256')!=sha(W/'ard-callback-width-result-01.json'):raise ValueError('required controls incomplete/stale')
if any(x.get('exit')==0 or x.get('result_absent') is not True or x.get('expected_error_seen') is not True for x in c['refusals']):raise ValueError('required concrete refusal failed')
pins=r['source_pins']+r['required_invocation_receipts']
for x in pins:
 if sha(W/x['path'])!=x['sha256']:raise ValueError('required source/receipt moved')
paths={x['path'] for x in pins}|{'ard-callback-width-method-01.json','ard-callback-width-result-01.json','prove-ard-callback-width.py','control-ard-callback-width.py','freeze-ard-callback-width.py'}
paths|={n+s for n in ['ard-callback-width-positive-01','ard-callback-width-controls-run-01'] for s in ['.stdout','.stderr','.status.json']}
paths|={p.relative_to(W).as_posix() for p in (W/'ard-callback-width-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/ard-callback-width/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md'];units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('native reviewed path budget exceeded before copy')
if any(not (W/p).is_file() for p in paths):raise ValueError('required member missing before copy')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
 q=out/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,q)
(out/'README.md').write_text('''# ARD read destination is distinct from its callback root

Method A STATIC_ONLY,825 original bytes: complete loader normal fragments,
binder and pointer tag. Producer checked, independent review/incorporation
pending. EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000. No native/emulated/live/CRT execution or new placement sample.

3EA820 obtains a pointer from36A100, tags it through36C660 and tests fullRAX.
The normally returning tag preserves its full incoming pointer viaRBX. At
3EA971 the loader supplies that fullRAX asR8 read destination to32E620, but at
3EA976 it saves onlyEAX into DWORD descriptor+8. Descriptor+10 names3EA710.
Submission is not queue acceptance or an executed callback.

3EA710 starts MOV EBP,ECX at3EA732. That zeroextends the lowDWORD into64-bitRBP,
including inputs with bit31 set. It also MOV ECX,ECX before the tag call. No other
local assignment changes the savedRBP until AFTER3EA809 publishes it as a qword
at02B5E0C0. Under normal ABI-preserving callees, every normal execution of this
writer publishes0..FFFFFFFF. This is a writer invariant, not an all-writer census
or global lifetime guarantee. Unload zero is not evidence of successful loading.

Therefore that published-root sample cannot recover a full high allocator result.
A future observer answering GR18 must record fullRAX at3EA93E, orR8 at3EA97F,
and prove object/request/callback identity and session health. A hypothetical
high read destination and its low callback root are different storage identities
unless separate mapping evidence says otherwise. No high bits are restored here.
Actual allocator placement and normal queued reachability still need sufficient
evidence; no claim a natural high allocation or resulting fault happened.

Nor does a low root guarantee low section pointers. The binder SIGN-extends the
resolver's lowDWORD and adds it to that root in64bits. Conditional rootFFFFFF00
plus offset1000 produces100000F00. This is arithmetic under supplied values, not
shipped data or a native/live run. Whole-buffer extents, section/row identity,
reward-store truncation and actual allocation placement have separate bounds.

Retained EXP077/078 already cover initializer high-pointer retention and controlled
original allocator-link effects. EXP079 records low placement in one actual
title/loaded session. They were read, not rerun, and none gives an alltime placement
guarantee. Their reported controls/external reviews are not new tests by this package.
Do not spend runtime sampling a root whose highbits this writer already discards.

Reproduce the source proof with existing analysis Python into a fresh output:

    python <packet>/prove-ard-callback-width.py <fresh.json>

Exact original .pdata parent triples qualify both loader continuations. The
actual capture and reducer use the reviewed shared access-role adapter and
byte redecoding. Full image/range/driver identity, actual exit/output and complete
normal binder/tag control flow are checked. Three actual CLI refusals reuse the
valid positive: failed capture exit, consistently changed root-input register,
missing loader tail. Missing evidence cannot become a valid empty success.
Immutable driver/input/case/result/receipts retained; producer controls are not
independent semantic acceptance. No historical mutation campaigns rerun.

OPUS consumes the GR18/full-pointer-versus-callback-root distinction; FABLE
consumes binder parameter width and signed64-bitsection arithmetic limits. Keep
natural placement/queue/lifetime gaps open. No whole GR18/OV/AQ row closure.

Player version: battle data can be read into one address while the later binding
code uses only that address's lower32bits. Looking at the later root alone cannot
tell us where Windows/the allocator put the original buffer. We are checking that
handoff before asking for gameplay evidence.

Cleanup: finite source reads/disposable refusal copies only. No game/PC/input/
instrument/native/save/config/reference or peer-process mutation. Full goal
ACTIVE/NOT_MET; menu spent/unapproved and EXP127 invalid remain unchanged.
''',encoding='utf-8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native units',units,'manifest',sha(out/'manifest.json'))
