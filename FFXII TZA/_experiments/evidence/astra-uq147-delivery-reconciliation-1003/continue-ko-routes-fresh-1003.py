"""Fresh current-state continuation after unrelated board revision changed; no replay."""
import json
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ROOT = next(p for p in W.parents if (p/'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
KIT = ROOT/'Database/Tools/analysis-kit/gfz-scripts'
sys.path.insert(0,str(KIT)); import team
D = W/'uq147-ko-reconciliation-routes-fresh-02'; D.mkdir()
PUB = 'ASTRA-PUBLISH-UQ147-KO-RELEASE-PARTITION-1003'
FRONTIER = 'ASTRA-REQ-FRONTIER-UQ147-INTERRUPTED-PUBLISH-1003'
REVIEW = 'ASTRA-REQ-SPEC-UQ147-KO-RELEASE-PARTITION-1003'
old = W/'uq147-ko-reconciliation-routes-01/SWE2-AUDIT-SPEC-once.receipt.json'
old_status = json.loads(old.read_text())
if old_status['exit'] != 1 or old_status['stdout'] or 'expected revision 50340, board is at 50341' not in old_status['stderr']:
    raise RuntimeError('Different prior failure; no continuation')

def board():
    ok,why=team.board_status(team.BOARD)
    if not ok:raise RuntimeError(why)
    return json.loads(team.read_board_text(team.BOARD))

def apply(op, tag):
    b=board()
    p=next(t for t in b['tasks'] if t['id']==PUB)
    if p['status']!='BLOCKED' or p.get('agent')!='ASTRA' or FRONTIER not in p['dependencies']:
        raise RuntimeError('Publication state changed; reconcile')
    if op['action']=='add' and any(t['id']==op['task']['id'] for t in b['tasks']):
        raise RuntimeError('Existing task: no duplicate routing')
    if op['action']=='checkpoint':
        t=next(t for t in b['tasks'] if t['id']==op['task'])
        if t['status']!='ACTIVE' or t.get('agent')!='ASTRA':raise RuntimeError('Owner changed')
    (D/(tag+'.preimage.json')).write_text(json.dumps(dict(revision=b['revision'],epoch=b.get('recovery_epoch'),publication=p),indent=2))
    dest=D/(tag+'.fresh-operation.json');dest.write_text(json.dumps(op,indent=2))
    # team.py's under-lock integrity/task checks supply atomic admission. An
    # unrelated peer checkpoint need not force a repeat of this absent request.
    argv=[sys.executable,'-B',str(KIT/'team.py'),'apply','--agent','ASTRA','--session','SOL-ASTRA-ko-reconciled-routes-fresh-1003','--file',str(dest)]
    r=subprocess.run(argv,stdin=subprocess.DEVNULL,capture_output=True,timeout=45)
    (D/(tag+'.receipt.json')).write_text(json.dumps(dict(argv=argv,terminal=True,exit=r.returncode,stdout=r.stdout.decode(errors='replace'),stderr=r.stderr.decode(errors='replace')),indent=2))
    if r.returncode or b'Saved revision ' not in r.stdout:raise RuntimeError('Refused; no replay')
    print(tag,r.stdout.decode().strip(),flush=True)

# Rebase the absent request from its immutable proposal after checking that the
# original transaction did not land. Do not repeat the frontier or block ops.
spec=json.loads((W/'uq147-ko-reconciliation-routes-01/SWE2-AUDIT-SPEC-once.operation.json').read_text())['task']
spec['known_evidence'] += ' Fresh route follows explicit unrelated revision-conflict refusal; original operation unlanded, current publication remains BLOCKED. No original operation is replayed.'
apply(dict(action='add',task=spec),'SPEC-fresh')
for owner,target,question in [
 ('OPUS','Propagate accepted predicate/copy-domain corrections into owning consumers','After SPEC acceptance, correct CONTRACT-auto-status-rebuild §310780 reversedbit22 and §13an stale730/480copy. Coordinate additive EXP198/EXP231 correction with actual owner. Preserve raw historicresults, identify dependent prose/check paths; EXP091 clearbit fixture/acceptedcopyregression/OPUS9811/ORACLEf7bb/censusb9b8 alreadyDONE and not rerun. New candidate science review is not completed publication; bookkeeping stays FRONTIER request.'),
 ('FABLE','Consume accepted KO cleanup partition into UQ147 composition','After SPEC acceptance, consume bit22-clear contributorbookkeeping versus separately read bit22-set restore. No direct714write doesnot mean preservedcommand because acceptedcopy includes714, savedcommand neednoterase. Reads separatedbycalls/noatomicinvariance. Ownstatus/party/UQ147 only; OPUS hasautostatus/experiment propagation. NaturalKO/Esperpending113 admission/lifetime/timing remainOPEN. Exactclause oralreadycoveredprovenance, no repeat.')]:
    t=dict(id='ASTRA-REQ-'+owner+'-UQ147-KO-RELEASE-PARTITION-1003',kind='request',priority='P2',requester='ASTRA',assigned_to=owner,target=target,scope=spec['scope'],question=question,known_evidence=spec['known_evidence'],missing_information='Exact owning canonical propagation after scoped scientific review',why_it_matters=spec['why_it_matters'],what_is_blocked=spec['what_is_blocked'],completion=spec['completion'],dependencies=[REVIEW],resources=[dict(key='request:astra-req-'+owner.lower()+'-uq147-ko-release-partition-1003')])
    apply(dict(action='add',task=t),owner+'-fresh')
note='Checkpoint95 recovery supplement: boardcheck passed epoch4/50322 after prior epoch3/journal4 mismatch, causeUNKNOWN/no restore/replay. Candidate d02293770e149fae885dbf77c8282b8f7ed1399d exact69plannedpaths/blobs verified; publisherstdout/exit stillmissing, no fakefinish. Ownpublishing taskBLOCKED freesactivelease; FRONTIER request50339once, block50340. SPECroute firstrefused50340->50341 beforewrite; freshlyabsent route admitted once, OPUS/FABLE follow scopedverdict, no duplicate. Toolhelp root48564absent/no attributable descendants/positivechildclosed; exitedancestry and deniedCIM limits remain/nopeertermination. Next original2FEAD0/30C0E0calleeclosure: retainedgetter/field evidence first, normalstate/callbackeffect limits; previewsnotclosure. Menu spent/unapproved,EXP127INVALID,K14acceptedclosed. FullL1L2+M0M5goalACTIVE/NOT_MET; no game/PC/native/save/config/reference activity.'
for id,tag in [('FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929','parent-checkpoint95-fresh'),('FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON','uq147-checkpoint95-fresh')]:
    apply(dict(action='checkpoint',task=id,note=note),tag)
(D/'HANDOFF.md').write_text('Reconciled current checkpoint95 supplement\n\n'+note+'\n\nThe original delivery02 timeout receipt remains immutable. Original route01 stopped on its first missing request; its successful FRONTIER/block operations were not repeated. Resume only through fresh checked board and adjudicated delivery receipts.\n')
