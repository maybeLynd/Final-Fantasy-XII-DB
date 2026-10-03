"""Freeze the current conditional UQ147 results; not whole-question acceptance."""
import hashlib, json, shutil
from pathlib import Path
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['PLAN.md','SELECTOR-QUESTION.md',
 'capture-dismiss-boundary.py','capture-boundary-01.status.json','capture-boundary-01.stdout','capture-boundary-01.stderr','source-boundary-01.json',
 'capture-request-tail.py','capture-request-tail-01.status.json','capture-request-tail-01.stdout','capture-request-tail-01.stderr','source-request-tail-01.json',
 'reduce-request-tail-boundary.py','reduce-request-tail-02.status.json','reduce-request-tail-02.stdout','reduce-request-tail-02.stderr','result-request-tail-boundary-02.json',
 'capture-defeat-boundary.py','capture-defeat-boundary-01.status.json','capture-defeat-boundary-01.stdout','capture-defeat-boundary-01.stderr','source-defeat-boundary-01.json',
 'prove-defeat-recompute-boundary.py','prove-defeat-boundary-01.status.json','prove-defeat-boundary-01.stdout','prove-defeat-boundary-01.stderr','result-defeat-boundary-01.json',
 'capture-dismiss-selector-boundary.py','capture-selector-01.status.json','capture-selector-01.stdout','capture-selector-01.stderr','source-selector-01.json',
 'prove-dismiss-selector-boundary.py','prove-selector-01.status.json','prove-selector-01.stdout','prove-selector-01.stderr','result-selector-01.json']
for prefix in ['preview-class3-lookup-01','preview-class3-object-01','preview-unit-reader-01','lookup-class3-lookup-01','lookup-index-table-01','lookup-actor-unit-leaf-01']:
    names += [prefix+x for x in ['.status.json','.stdout','.stderr']]
    if prefix.startswith('lookup'):names.append(prefix+'.json')
for n in names:
    if not (P/n).is_file():raise ValueError('Missing exact receipt/input '+n)
    if n.endswith('.status.json'):
        s=json.loads((P/n).read_text())
        if s.get('terminal') is not True or s.get('exit')!=0 or s.get('exception') is not None:raise ValueError('Failed/incomplete run '+n)
for n in ['result-defeat-boundary-01.json','result-selector-01.json']:
    if json.loads((P/n).read_text()).get('producer_complete') is not True:raise ValueError('Incomplete result '+n)
tail=json.loads((P/'result-request-tail-boundary-02.json').read_text())
tail_status=json.loads((P/'reduce-request-tail-02.status.json').read_text())
if sha(P/'result-request-tail-boundary-02.json')!='ebcd389e88a1d96c25715b13b8af238d716e5ced5c0952bdd89c76d8f129168f':raise ValueError('Original completed legacy result changed')
if tail.get('status')!='BOUNDED_NOTIFICATION_WRITE_BRANCH_EXCLUDED_NATURAL_KO_STILL_OPEN' or tail.get('driver_sha256')!='b4a8732fab891ecece0117f9e3bda681416528abec532730d2d3b4d527f75f2a' or sha(P/'reduce-request-tail-boundary.py')!=tail['driver_sha256'] or tail_status['driver_sha256']!=tail['driver_sha256']:
    raise ValueError('Exact completed legacy tail-result schema required')
if tail.get('source_sha256')!=sha(P/'source-request-tail-01.json') or tail.get('annotation_agreement',{}).get('status')!='VERIFIED_BYTE_ANNOTATION_AGREEMENT' or tail['annotation_agreement'].get('instruction_records',0)<=0:
    raise ValueError('Legacy tail result source/annotation prerequisite missing')
out=W/'uq147-local-boundaries-frozen-ready';out.mkdir()
for n in names:shutil.copyfile(P/n,out/n)
for n in ['prepare-uq147-selector-capture.py']:
    shutil.copyfile(W/n,out/n)
shutil.copyfile(Path(__file__),out/Path(__file__).name)
for src,dst in [('freeze-uq147-local-boundaries.before-schema-fix.py','freeze-attempt01-driver.py'),('freeze-uq147-boundaries-01.status.json','freeze-attempt01.status.json'),('freeze-uq147-boundaries-01.stdout','freeze-attempt01.stdout'),('freeze-uq147-boundaries-01.stderr','freeze-attempt01.stderr')]:
    shutil.copyfile(W/src,out/dst)
(out/'publication-tail-source-map-01.json').write_text(json.dumps(dict(producer_complete=True,
    method='Exact source qualification adapter for completed legacy tail-result schema; not a new scientific result',
    source_pins=[dict(path='source-request-tail-01.json',sha256=sha(P/'source-request-tail-01.json'))],
    result=dict(path='result-request-tail-boundary-02.json',sha256=sha(P/'result-request-tail-boundary-02.json')),
    actual_completed_status=dict(path='reduce-request-tail-02.status.json',sha256=sha(P/'reduce-request-tail-02.status.json')),
    limits='The legacy bounded semantic result and limits remain unchanged; publication annotation map only. Independent review/wholeUQ147 acceptance remain pending.'),indent=2)+'\n')
(out/'README.md').write_text('''# UQ147 conditional KO-cleanup and Dismiss boundaries

For the player: on a conditional KO-cleanup path, FF12 requests Dismiss and recalculates capabilities immediately in the same function. The Dismiss selector reads the fourth active-party slot without a KO/status filter or cleanup. This does not establish which naturally initialized gameplay states reach the path or when Dismiss actually executes.

Method A / STATIC_ONLY. Producer-valid only; independent review and canonical consumption pending. No original-code, native, emulator, game or PC session. Existing EXP198/S20 and OPUS reviewer runs were read, not rerun or counted as ours.

Three bounded results:

- `result-defeat-boundary-01.json`: after reaching003010F6 with flag0, mode query1 and designated-member lookup equal to the KO-cleanup receiver, original0030111C setsECX0, calls003138D0, then immediately calls0023B040 after normal return. No intervening world-tick dispatcher. Earlier cleanup/party arms and natural admission are separate. Complete371B300FC0 and106B31B770 qualified from shipping bytes.
- `result-request-tail-boundary-02.json`: every normal317E60 tail passes(1,0) to25AAD0. Under normalABI its savedEBX1 excludes five local publication writes and2F1710 callback; the earlier resolver still executes. This does not prove all earlier helper effects or global mode preservation. Complete87B317E60 and82B25AAD0 qualified.
- `result-selector-01.json`:3138D0's mode1 leg passes index3 to31B8C0. Closed31B8C0/263750/263E30 composition readsQWORD0209A208, returnsNULL for an empty actor slot, otherwise readsQWORDactor+30. It has no health/status read, object write, allocation or opaque callback. This is roster index3, not ActorStorage class3. The31B8C0 body is31B with a unique .pdata root;263750/263E30 are23B/5B closed direct-target leaf spans without .pdata roots. No roots were invented. CALL/RET private stack effects and readabletable/actor/ABI/noninterference remain premises.

Exact image: SHA25673461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, base120000. Raw maps, actual finite exit/terminal/exception receipts, physical extents/bytes, reviewed shared access-role adapter and actual current annotation qualification are preserved. The new selector source adds59B; earlier583/169/477B are retained inputs, not new experiments. Three selector source-record mutations require their specific diagnostics; failed-upstream status control is in-process, not an actual CLI refusal. Defeat proof has three source-record controls. Local/static controls do not establish natural KO reachability.

Caller correction: OPUS c480be5436695f2de4adfbeba1ff0ae735d8c2e5 canonically records all three311CF0 refusal paths. ASTRA's contrary caller allegation was wrong:311C7B/311CA6 in311B20 plus31395D in3138D0 are three sites in TWO functions. Preserve the original record and additive correction in the current operating handoff. No duplicate completed census/regression was run.

Still OPEN: realKO admission, initialized roster/member+5AD5 relationship, mode+5B04/KO/member persistence across preceding and later command helpers, request versus acceptance/commit/execution, mask7/override-clear natural reachability, scheduling, ownership/lifetime and presentation. World-update mode1 menu is not battle-runtime mode1 summon. A composed original-path feasibility result would not automatically prove normal gameplay reaches it.

Consumer: FABLE capability-inhibition-policy UQ147, OPUS command-seam ABI/contracts. Review the exact partial boundaries, then update only their qualified owning clauses; do not close wholeUQ147 or request a game session by historical RT label. Next discriminator is intervening command/helper mode/member/status effects and original KO-admission path. Do not repeat these settled local controls, EXP198/S20 fixtures or the parked menu attempt.

The capture wrapper reuses the reviewed capture-index-path dependency from the canonical gauge packet64cb2c0c, and the current shared annotation validator in the owned ASTRA work root. Run drivers with their declared repository layout/dependencies and fresh outputs. First freeze attempt01 failed before any output because it assumed every historical result had producer_complete; the completed tail reducer instead has an exact bounded status schema. Its failed driver/status/stdout/stderr are retained. The corrected freezer requires the exact original result digest/schema/driver/source/actual successful receipt, and emits a publication source-map adapter without modifying or rerunning that result. No failed freeze is credited as a successful run. This frozen result is an immutable current receipt, not a committed-before-execution ORACLE seal. Independent acceptance is separate.

No save/config/reference/process/PC change occurred; no detach/restoration was needed. FullL1L2 and independently accepted deployedM0M5 goal ACTIVE/NOT_MET. K14 closed;EXP127 invalid; menu setup allowance spent and extension unapproved.
''')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(schema_version=1,method='A STATIC_ONLY conditional local boundaries',status='FROZEN_PRODUCER_VALID_NOT_INDEPENDENTLY_ACCEPTED',members=members),indent=2)+'\n')
print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))
