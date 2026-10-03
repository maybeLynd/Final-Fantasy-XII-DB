"""Freeze one original branch correction and exact affected consumer preimages."""
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;P=W/'uq147-summoner-cleanup-order'
ROOT=next(p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
E=ROOT/'Database/FFXII TZA/_experiments/evidence';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((P/'result-ko-release-partition-02.json').read_text());status=json.loads((P/'prove-ko-release-partition-02.status.json').read_text())
if result.get('producer_complete') is not True or len(result.get('controls',[]))!=4 or result['driver_sha256']!='aac8b52cc0b60928c3526cd1690c4c8cfe087d76967e8e03ee775b9986643c53' or status.get('terminal') is not True or status.get('exit')!=0 or status.get('exception') is not None or status['driver_sha256']!=result['driver_sha256']:raise ValueError('Actual proof incomplete')
st=json.loads((P/'control-ko-release-status-01.status.json').read_text());c=json.loads((P/'ko-release-status-control-01/control-result.json').read_text())
if st.get('terminal') is not True or st.get('exit')!=0 or st.get('exception') is not None or c.get('status')!='ACTUAL_CLI_FAILED_UPSTREAM_REFUSED':raise ValueError('Actual CLI control incomplete')
out=W/'uq147-ko-release-partition-frozen-ready-02';out.mkdir()
for name in ['source-ko-release-01.json','source-restore-gate-01.json','capture-ko-release-boundary.py','capture-restore-gate-boundary.py','prove-ko-release-partition.py','prove-ko-release-partition.v1.preimage.py','result-ko-release-partition-02.json','control-ko-release-status.py','KO-RELEASE-NEXT-QUESTION.md','lookup-ko-release-01.json','lookup-restore-gate-01.json']:
    shutil.copyfile(P/name,out/name)
for tag in ['capture-ko-release-01','capture-restore-gate-01','prove-ko-release-partition-01','prove-ko-release-partition-02','control-ko-release-status-01','preview-ko-release-01','preview-restore-gate-01','lookup-restore-gate-01']:
    for suffix in ['.status.json','.stdout','.stderr']:shutil.copyfile(P/(tag+suffix),out/(tag+suffix))
shutil.copytree(P/'ko-release-status-control-01',out/'ko-release-status-control-01')
for name in ['prepare-ko-release-capture.py','prepare-restore-gate-capture.py']:shutil.copyfile(W/name,out/name)
for tag in ['prepare-ko-release-01','prepare-restore-gate-01']:
    for suffix in ['.status.json','.stdout','.stderr']:shutil.copyfile(W/(tag+suffix),out/(tag+suffix))
cp=out/'retained-copy';cp.mkdir()
for name in ['source-01.json','result-01.json','proof-01.status.json','capture-01.status.json','manifest.json','README.md']:shutil.copyfile(E/'suspend-restore-copy-origin'/name,cp/name)
pre=out/'consumer-preimages';pre.mkdir();consumers=[]
items=[('EXP-198-unlink-carrier-family-exec.md','_experiments/EXP-198-unlink-carrier-family-exec.md','bit22\n  set AND','Wrong enable predicate: original BT/JB skips when set; EXP091 already says clear admits bookkeeping.'),('CONTRACT-auto-status-rebuild.md','10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md','`q[obj]` bit22 and','Same reversed predicate; §13an also carries obsolete +730/480 snapshot-copy prose.'),('EXP-231-detach-siblings-exec.md','_experiments/EXP-231-detach-siblings-exec.md','0x480-byte','Stale snapshot bounds: accepted d7500f9f/49d0564f2, OPUS9811b61f5 and ORACLEf7bbac4ef establish +6B0/4F0.')]
for name,rel,needle,issue in items:
    src=ROOT/'Database/FFXII TZA'/rel;raw=src.read_bytes()
    if needle not in raw.decode().replace('\r\n','\n'):raise ValueError('Consumer changed: reconcile before routing '+rel)
    (pre/name).write_bytes(raw);consumers.append(dict(path='Database/FFXII TZA/'+rel,sha256=hashlib.sha256(raw).hexdigest(),match=needle,issue=issue,required_action='Owner additive correction/reopening of affected inference; preserved historical raw results, no old experiment rerun'))
for name,rel in [('EXP-091-commit-callees-exec.md','_experiments/EXP-091-commit-callees-exec.md'),('copy_range_check.py','_index/candidates/opus-suspend-copy-origin-1001/copy_range_check.py')]:
    shutil.copyfile(ROOT/'Database/FFXII TZA'/rel,pre/name)
(out/'consumer-correction.json').write_text(json.dumps(dict(status='PRODUCER_IDENTIFIED_CONTRADICTION_REVIEW_PENDING',consumers=consumers,retained_accepted_copy=result['retained_copy'],harness_limit='Current EXP091 harness positive bit22-clear fixup and accepted copy regression consumed, not executed here. No invalidation of all old numerical results from wrong summaries.'),indent=2))
shutil.copyfile(Path(__file__),out/Path(__file__).name)
shutil.copyfile(W/'freeze-ko-release-partition.v1.preimage.py',out/'freeze-ko-release-partition.v1.preimage.py')
for suffix in ['.status.json','.stdout','.stderr']:shutil.copyfile(W/('freeze-ko-release-partition-01'+suffix),out/('freeze-ko-release-partition-01'+suffix))
(out/'README.md').write_text('''# KO cleanup partitions target release and action restoration

Method A; exact EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, base120000. Question: what can the earlier310780 cleanup establish before Dismiss/recompute? Complete original225B/three chained unwind fragments plus connecting308270120B/root are retained, with actual reviewed store/LEA/RMW controls and original byte/metadata comparison. No native/emulator/game execution.

Original310780 target bookkeeping is admitted with nonNULL receiver/stats/target, bit22 CLEAR and target mask bit present. BT003107BE/JB003107C3 skips when bit22 SET. EXP198 and auto-status contract currently state the reverse; exact consumer preimages/contradiction are retained. EXP091 already has correct branch prose and a named clear-bit fixture, so do not award this as a previously unknown whole mechanism.

The complete local write set is target byteEA8 decrement/DWORDEA4 mask, acting flags0 and byte694. There is no direct local714/BA0/battle-mode write, under explicit private separated stack and ordinary field identities. Opaque helpers are not effect-free. Eight call boundaries are enumerated. Two complete local CFGs cover normal branches only, not exceptions, callback effects or live reachability.

In308270 the separate BT0030827B/JAE00308280 skips restoration when bit22 CLEAR. SET reaches30EDA0 after the earlier30C970 returns. Flags are read at different times; callbacks/interference may change them. Reuse accepted d7500f9f/49d0564f2 source-domain proof: restore covers[unit+6B0,unit+BA0), including committed714/savedoffset64 and B88, excluding pendingBA0. It can replace the current command with saved contents; no requirement that those contents erase it. OPUS9811b61f5 and ORACLEf7bbac4ef already consume/regress that domain. EXP231 and auto-status §13an still carry old730/480 prose and need owner propagation, not another copy/native experiment. Snapshot pointer validity/nonaliasing/natural ownership/lifetime remain open.

Actual positive produceraac8b52c/proof02 completed, four cause-specific labelled source-record semantic controls, plus6da57ac2 actualCLI failed-upstream control exits1/noresult. Record controls are not altered shipping code or native runs. Failed firstproducer701acdde stopped beforeoutput because the legacy copy result lacks exe_sha256; corrected producer requires its exact driver/source_pins and actual completed proof status, original EXE identity from the pinned source. Failure/preimage/raw receipts retained; no missing field silently accepted.

The lookup's no covering map applies only to searched source maps. Existing canonical/native evidence must also be read before choosing capture: EXP091/198/231 and existing copy correction were then consumed. New physical captures verify this contradiction/composition; they do not earn new old-experiment credit. No repeated79-pair/native-copy or full542-case campaign. Use existing sources before expanding any opaque helper. First freezer refused before manifest on CRLF-versus-LF text matching; raw consumer bytes were unchanged. Corrected matcher normalizes line endings only for finding the exact predicate and preserves original preimage bytes. Partial folder01/failed driver/raw receipts retained; only folder02 is qualified.

Reproduce prove-ko-release-partition.py with its exact working/canonical dependencies and a fresh output. Immutable copies preserve inputs/receipts; original layout dependencies are disclosed. Published producer/source pins, role validator and accepted-copy dependencies remain separate from new independent acceptance. SPEC review, OPUS affected contract/experiment correction and FABLE UQ147 composition pending. Zero whole formerly-runtime rows newly closed; natural summonerKO/Dismiss admission, transitive effects, initialized process state, timing and presentation remain OPEN.

No PC/game/input/attach/native/emulator/save/config/reference/peer-process action. Own finite helpers terminal. FullL1L2+required independently accepted deployedM0M5 ACTIVE/NOT_MET. Parked menu spent/unapprovedextension; EXP127 INVALID/crashunknown; K14 closed. Next seek existing evidence for native target-fixup/callback effects or a static natural pending/committed action invariant; no repeated settled helper probes.
''')
members=[dict(path=p.relative_to(out).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
(out/'manifest.json').write_text(json.dumps(dict(schema_version=1,status='FROZEN_PRODUCER_VALID_NOT_INDEPENDENTLY_ACCEPTED',members=members),indent=2)+'\n')
print(json.dumps(dict(members=len(members),manifest_sha256=sha(out/'manifest.json'))))
