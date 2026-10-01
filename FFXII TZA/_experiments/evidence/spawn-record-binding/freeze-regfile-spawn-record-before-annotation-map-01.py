"""Freeze the bounded same-record binding and exact failure/control history."""
import hashlib,json,pathlib,shutil,subprocess
W=pathlib.Path(__file__).resolve().parent;out=W/'regfile-spawn-record-frozen-ready'
if out.exists():raise ValueError('immutable packet exists')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((W/'regfile-spawn-record-result-01.json').read_text());c=json.loads((W/'regfile-spawn-record-controls-01/result.json').read_text())
for tag,driver,key in [('regfile-spawn-record-capture-01','capture-regfile-spawn-record.py','driver_sha256'),('regfile-spawn-record-positive-02','prove-regfile-spawn-record.py','checker_sha256'),('regfile-spawn-record-controls-run-01','control-regfile-spawn-record.py','driver_sha256')]:
    s=json.loads((W/(tag+'.status.json')).read_text())
    if s.get('exit')!=0 or s.get(key)!=sha(W/driver) or not (W/(tag+'.stdout')).read_bytes().strip() or (W/(tag+'.stderr')).read_bytes().strip():raise ValueError('required invocation failed/stale')
if r.get('producer_complete') is not True or r.get('checker_sha256')!=sha(W/'prove-regfile-spawn-record.py'):raise ValueError('positive missing/stale')
if c.get('status')!='PASS_ACTUAL_RECORD_BINDING_REFUSALS_INDEPENDENT_PENDING' or len(c.get('refusals',[]))!=4 or c['positive_reused']['sha256']!=sha(W/'regfile-spawn-record-result-01.json'):raise ValueError('controls incomplete/stale')
if any(x['exit']==0 or not x['expected_error_seen'] or not x['result_absent'] for x in c['refusals']):raise ValueError('refusal incomplete')
pins=r['source_pins']+r['required_invocation_receipts']
if any(sha(W/x['path'])!=x['sha256'] for x in pins):raise ValueError('source/receipt changed')
failed=json.loads((W/'regfile-spawn-record-positive-01.status.json').read_text())
if failed['exit']==0 or failed['checker_sha256']!=sha(W/'prove-regfile-spawn-record-before-return-path-control-01.py'):raise ValueError('historical failure missing')
paths={x['path'] for x in pins}|{'regfile-spawn-record-method-01.json','regfile-spawn-record-result-01.json','prove-regfile-spawn-record.py','control-regfile-spawn-record.py','freeze-regfile-spawn-record.py','prove-regfile-spawn-record-before-return-path-control-01.py','regfile-spawn-record-authored-01/manifest.json'}
paths|={tag+s for tag in ['regfile-spawn-record-positive-01','regfile-spawn-record-positive-02','regfile-spawn-record-controls-run-01'] for s in ['.stdout','.stderr','.status.json']}
paths|={p.relative_to(W).as_posix() for p in (W/'regfile-spawn-record-controls-01').rglob('*') if p.is_file()}
projected=['Database/FFXII TZA/_experiments/evidence/spawn-record-binding/'+p for p in sorted(paths|{'manifest.json','README.md','.gitattributes'})]+['Database/FFXII TZA/_index/_inbox/ASTRA.md']
units=len(subprocess.list2cmdline(projected).encode('utf-16-le'))//2
if units>24000:raise ValueError('qualified native path budget exceeded; no unchanged publication attempt')
out.mkdir();(out/'.gitattributes').write_bytes(b'* -text\n** -text\n')
for n in sorted(paths):
    p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/n,p)
(out/'README.md').write_text('''# Spawn selection keeps the authored actor's script-register bank

Method A, conditional original-code dataflow. Producer valid; required
independent review and canonical consumption pending. Full database goal ACTIVE.
EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
imagebase120000; no game, native or emulated execution.

Player version: one enemy script can contain several spawn/respawn routines.
Changing the spawn selection changes which routine the same actor record uses.
On the proved path those routines share the actor's script variables; a spawn
selection does not create a fresh bank of variables. This does not establish
which routines actually run, in what order, or what values gameplay leaves.

Returned RC16 already narrowed the old live-only question: a different authored
actor does not inherit this record within a pool. Its register persistence,
pool clear/release and read-before-write evidence are reused, not recounted.
The new discriminator is the identity passed from selection to the interpreter.

Original setentrygroup34FA70 passes the same actor to lists0,1,4,2,3 using one
popped selection.25AD10 reads that actor's function metadata, stores selection
at+F6 and maps spawn/respawn to override7/14.25AF60 resolves its self ordinal
through the current manager's owning pool. Under coherent manager/self identity,
valid metadata and normal ABI/no-interference premises, this returns the same
record. Do not generalize to corrupt/cross-manager/encoded-ID states.

The retained raw gol_b01 section has monster_00 at authored ordinal26, one
entry/function table containing spawn00..05 and respawn00..05. Raw CP932 names
are joined to IDs; decompiler labels are not used to identify the entries.
The six entry functions are a companion control; empty talk/touch lists remain
absent. This is one bounded authored control, not a repeated corpus census.

269860 reads that record's spawn/respawn override and submits a function request
to that record.3DB6E0 selects its active entry;3DBDC0 starts its PC from its
function table and bytecode base. Retained25DF00 supplies the same actor inRDX;
25E4C0 preserves it inR15, the established script-register bank base. Selecting,
submitting, starting and actually executing bytecode remain distinct stages.
Natural occurrence, repeated execution order/cause, interference and exact I1
values are not established. SpawnKeep's BattleStats block is a separate object.

Ten original bodies are qualified from retained regfile/SECTION12 evidence;
only seven missing spans are read afresh. The actual capture invokes the shared
reviewed memory-role adapter with store/LEA/RMW controls. Original bytes, full
image identity, source pins and required exit/result/exception status are checked.
SECTION12's external assertions/reviews and RC16 counts are not tests run here.

The first producer refused before creating a result: a flat address filter
counted an early failure-return POP RDI as if it could reach submission. The
producer now follows original normal CFG predecessors of the call; that POP and
RET cannot reach it. The failed invocation/preimage remain immutable. The actual
return-path control is recorded in the positive and reused by the control tool.
Four actual CLI refusals test failed capture, a coherently changed actor argument,
changed authored selector and missing retained input. No invalid/zero-case run
is counted as passing. Controls are producer checks, not project acceptance.

Reproduce with existing analysis Python into a fresh output:

    python <packet>/prove-regfile-spawn-record.py <fresh.json>

Consumer: FABLE semantic RC16; OPUS/SWE2-CONTRACT interpreter/register/selector
contracts; FRONTIER's AQ11 prepared-live premise. Canonical pages are peer-owned.
Retain accepted clear/persistence bounds and unproved takeover-reader reachability.
No claim that the whole OV16/AQ11 database obligation has completed from this
conditional packet. Menu allowance remains spent/unapproved; EXP127 remains
invalid. Cleanup: all finite children terminal; no PC/game/input/instrument,
save/config/reference writes or peer process changes.
''',encoding='utf8')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(status='PRODUCER_VALID_INDEPENDENT_PENDING',method='A STATIC_ONLY',members=members,native_path_budget_units=units),indent=2)+'\n')
print('Frozen',len(members),'members; native units',units,'manifest',sha(out/'manifest.json'))
