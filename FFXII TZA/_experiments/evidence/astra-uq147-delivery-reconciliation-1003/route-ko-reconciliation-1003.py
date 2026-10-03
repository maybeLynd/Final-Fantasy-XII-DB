"""Once-only supported coordination after read-only reconciliation; no publisher replay."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ROOT = next(p for p in W.parents if (p / 'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
KIT = ROOT / 'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0, str(KIT))
import team

D = W / 'uq147-ko-reconciliation-routes-01'
D.mkdir()
PUB = 'ASTRA-PUBLISH-UQ147-KO-RELEASE-PARTITION-1003'
FRONTIER = 'ASTRA-REQ-FRONTIER-UQ147-INTERRUPTED-PUBLISH-1003'
REVIEW = 'ASTRA-REQ-SPEC-UQ147-KO-RELEASE-PARTITION-1003'
C = 'd02293770e149fae885dbf77c8282b8f7ed1399d'
record = 'Database/Tools/work/ASTRA/runtime-residue-method-retriage/uq147-ko-publication-reconciliation-01/'

def board():
    ok, why = team.board_status(team.BOARD)
    if not ok:
        raise RuntimeError(why)
    return json.loads(team.read_board_text(team.BOARD))

def apply(op, tag):
    b = board()
    if op['action'] == 'add' and any(t['id'] == op['task']['id'] for t in b['tasks']):
        raise RuntimeError('Already routed; reconcile without replay')
    if op['action'] in {'checkpoint', 'block'}:
        t = next(t for t in b['tasks'] if t['id'] == op['task'])
        if t['status'] != 'ACTIVE' or t.get('agent') != 'ASTRA':
            raise RuntimeError('Current owner/state changed')
        (D / (tag + '.preimage.json')).write_text(json.dumps(dict(revision=b['revision'], task=t), indent=2))
    p = D / (tag + '.operation.json')
    p.write_text(json.dumps(op, indent=2))
    argv = [sys.executable, '-B', str(KIT / 'team.py'), 'apply', '--agent', 'ASTRA',
            '--session', 'SOL-ASTRA-ko-interruption-reconciliation-1003', '--file', str(p),
            '--expect-revision', str(b['revision'])]
    r = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, timeout=45)
    (D / (tag + '.receipt.json')).write_text(json.dumps(dict(argv=argv, terminal=True,
        exit=r.returncode, stdout=r.stdout.decode(errors='replace'), stderr=r.stderr.decode(errors='replace')), indent=2))
    if r.returncode or b'Saved revision ' not in r.stdout:
        raise RuntimeError('Supported write refused; preserve, no replay')
    print(tag, r.stdout.decode().strip(), flush=True)

r = json.loads((W / 'uq147-ko-publication-reconciliation-01/result.json').read_text())
v = json.loads((W / 'uq147-ko-publication-reconciliation-01/candidate-blob-verification.json').read_text())
p = json.loads((W / 'uq147-ko-publication-reconciliation-01/process-observation.json').read_text())
if r['status'] != 'RECONCILED_READ_ONLY' or v['status'] != 'EXACT_CANDIDATE_BLOBS_VERIFIED' or v['commit'] != C or v['exact_paths'] != 69:
    raise RuntimeError('Required read-only verification absent')
if p['root_present'] or p['descendants'] or p['control_child_terminal_exit'] is None:
    raise RuntimeError('Attributable publisher processes/control not terminal')
if hashlib.sha256((ROOT / 'Database/FFXII TZA/_experiments/evidence/uq147-ko-release-partition/manifest.json').read_bytes()).hexdigest() != 'ff4cd43a997cb98df7007fdd1e8b2fd73ffc317fee4abcf0fa6e3f7310ac2458':
    raise RuntimeError('Scientific payload moved')

task = dict(id=FRONTIER, kind='request', priority='P1', requester='ASTRA', assigned_to='SWE2-FRONTIER',
    target='Adjudicate interrupted ASTRA publication and correct its actual timeout/receipt invocation',
    scope='One interrupted publisher; exact candidate and process/receipt limits, no board restore or peer cleanup',
    question='Delivery02 killed controller PID48564 after outer runner150s. Exact candidate '+C+' exists and all69 reviewed paths/blobs/message verify, but controller captured publisher stdout in RAM and never persisted it. TEAM requires the publisher committed-sha line; no terminal publisher status/commit-verification/finish receipt exists. Please establish a sanctioned recovery or a precise unresolved receipt disposition without treating Git HEAD or exact candidate integrity as recovered stdout. Investigate actual runner->controller->bash lifetime/output boundary and provide the smallest continuation/recording fix with interrupted-after-commit control; no unchanged republish. ASTRA blocks its own task to free the active lease, retains exact state. Process Toolhelp positive child/parent control passed, recorded root absent/no attributable descendants; exited intermediates can break ancestry, CIM query denied, no global absence or peer termination claimed. Also prior supported boardcheck returned epoch3 versus journal4 error/45817, now two fresh checks pass epoch4/50322; cause unknown, no restore/replay/bypass done. Notify once, preserve prior mismatch and current recovery; do not invent a rollback diagnosis.',
    known_evidence=record+'result.json, candidate-blob-verification.json, process-observation.json; publication-uq147-ko-release-partition-01/automated-publication-attempt-01.json; uq147-ko-release-partition-deliver-02.status.json terminalfalse/TimeoutExpired; genericcontroller eb288544/publisher ac899c6f/delivery13490778; no publisher terminal outputs.',
    missing_information='Publisher pinned stdout/terminal identity or authorized recovery adjudication, and tested actual interrupted invocation fix',
    why_it_matters='Release contention and prevent scientific evidence from being lost or repeated after a durable commit; actual delivery prerequisite, not generic maintenance',
    what_is_blocked='Only publication bookkeeping/complete delivery; original-byte scientific review can proceed from the explicit candidate',
    completion='Exact identity and terminal/cleanup limits adjudicated; no fabricated publisher exit; invocation control rejects incomplete success',
    dependencies=[], resources=[dict(key='request:'+FRONTIER.lower())])
apply(dict(action='add', task=task), 'frontier-once')
apply(dict(action='block', task=PUB, dependencies=[FRONTIER],
    resume_when='FRONTIER/OPUS supplies sanctioned missing-receipt reconciliation and any required attributable-process check, supported boardcheck passes, then same ASTRA resumes with fresh operation; never repeat publisher.',
    note='Interrupted delivery, not scientific invalidation: candidate '+C+' exact69paths/blobs verified read-only, missing committed-sha stdout/publisher exit remains unproved. Recorded controller absent/controlled snapshot no attributable descendants; broken exited ancestry/CIM denial limits retained, no peer killed. Own active publication lease released by supported BLOCKED transition; task/file history retained. '+FRONTIER+' notified once with exact evidence. Full goal ACTIVE/NOT_MET; independent scientific review uses candidate bytes only, no claim that delivery completed.'), 'block-own-publication')

evidence='Explicit candidate '+C+'; README/source/raw/proof/control in _experiments/evidence/uq147-ko-release-partition. Manifestff4cd43a 66 members; '+record+'candidate-blob-verification.json proves69 exact planned paths, NOT completed publisher receipt. New original310780225B/three unwindfragments source119783a7; 308270120B sourceb8060112; EXE73461d08/base120000; actualshared roleadapter5fcc6484/validator7c4ea9f6 on3sources. Produceraac8b52c proof02/four labelled source-record controls/6da57ac2 actualCLI failed-upstream exit1/noresult. Accepted copyd7500f9f/independent49d0564f2/source31c27/result3d07 reused, not rerun. OPUS9811b61f5/ORACLEf7bbac4ef/censusb9b821cda alreadyDONE. Originalfailed legacy-schema/CRLF preparations preserved separately. Publication bookkeeping BLOCKED, no claim publisher terminal0.'
q='Review original BT3107BE/JB3107C3: bit22 SET skips contributorEA8 decrement/EA4 clear; CLEAR+nonnulltarget+presentmask admits. EXP198/autostatus §310780 reverse enable. Only four direct objectwrites, no direct714/BA0/battlemode store, opaque effects open. Separate308270 BT/JAE skips onCLEAR; SET normally calls30EDA0 after30C970. Reads separated by calls, no atomic invariance. Accepted copy[6B0,BA0) includes714/saved64/B88/excludesBA0; restore may replace, neednot erase command. Assess scientific code/controls directly from exact Git candidate; do not accept publication completion. NaturalKO/Esper pending113 admission, transitive helper effects/lifetime/scheduling/fullUQ147 remain open. No duplicate native/copy/fullcampaign or external test credit.'
for id, owner, target, question, deps in [
    (REVIEW, 'SWE2-AUDIT-SPEC', 'Independent scientific review of KO cleanup predicate correction', q, []),
    ('ASTRA-REQ-OPUS-UQ147-KO-RELEASE-PARTITION-1003', 'OPUS', 'Propagate accepted predicate/copy-domain corrections into owning consumers',
     'After SPEC acceptance, correct CONTRACT-auto-status-rebuild §310780 reversed bit22 predicate and §13an stale730/480copy. Route affected EXP198/EXP231 prose through actual owner. Preserve raw historic results; analyze only dependent prose/producer/check paths. EXP091 clear-bit fixture and accepted corrected copy regression already exist, no blanket rerun/census repair. Return exact affected clauses and any smallest missing regression. Candidate review is not completed publication; task bookkeeping remains FRONTIER-owned.', [REVIEW]),
    ('ASTRA-REQ-FABLE-UQ147-KO-RELEASE-PARTITION-1003', 'FABLE', 'Consume accepted KO cleanup partition into UQ147 composition',
     'After SPEC acceptance, consume clear-bit contributor bookkeeping versus separately read set-bit restore. No direct714 write does not mean command preserved: accepted copy includes714; saved command neednot erase. Reads separated by calls, no atomic bit invariant. Owning status/party/UQ147 clauses only; OPUS owns autostatus/experiment propagation. NaturalKO/pending113 admission and timing/lifetime remain open. Return exact owning clause or already-covered provenance; no repeated experiment.', [REVIEW])]:
    task = dict(id=id, kind='request', priority='P2', requester='ASTRA', assigned_to=owner,
        target=target, scope='One original-code predicate correction and accepted copy-domain consumption',
        question=question, known_evidence=evidence, missing_information='Scoped independent scientific verdict or exact canonical propagation',
        why_it_matters='Reversed predicate inverts reconstruction branch; old copy range wrongly implies current command stability',
        what_is_blocked='Only affected clauses/composition premises; no full UQ147 closure or publisher acceptance',
        completion='Qualified scientific verdict/canonical clauses, original history and limitations preserved',
        dependencies=deps, resources=[dict(key='request:'+id.lower())])
    if id == REVIEW:
        task['reviews'] = PUB
    apply(dict(action='add', task=task), owner+'-once')

note='Checkpoint95 recovery supplement: fresh boardcheck/current passes epoch4/50322 after prior epoch3/journal4 mismatch; no restore/replay. Candidate'+C+' 69exact reviewedpaths/blobverified, missingpublisherstdout/exit notfabricated; ownpublishing taskBLOCKED freesactivelease, FRONTIER requestonce. SPEC scientific reviewfromimmutablecandidate once, OPUS/FABLE consumersafterverdict; newreview notacceptance. Root48564absent/noToolhelpattributeddescendants withpositivechild control, exitedancestry/CIMlimits/nopeerkills. Next target-fixup2FEAD0/globalgate30C0E0 retained/originalstatic question underexistingownedW; originalpreviews only, no native/live. Parkedmenu spent/unapproved, EXP127INVALID, K14acceptedclosed. FullL1L2/M0M5goalACTIVE/NOT_MET; do not repeat settled predicate/copy controls.'
for id, tag in [('FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929', 'parent-current'), ('FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON', 'uq147-current')]:
    apply(dict(action='checkpoint', task=id, note=note), tag)

(D / 'HANDOFF.md').write_text('Current recovery supplement, not full completion\n\n'+note+'\n\nFuture handoff refresh must use current board and actual adjudication; the committed checkpoint95 publication header is a prepared package, not delivery proof. No retries of the old controller or parked menu. Failed delivery02 remains immutable.\n')
