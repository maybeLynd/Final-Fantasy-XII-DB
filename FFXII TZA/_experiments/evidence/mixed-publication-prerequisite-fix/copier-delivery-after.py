"""One scoped job through the existing exact-path guarded publisher."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ROOT = next(p for p in W.parents if (p / 'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
T = ROOT / 'Database/Tools/analysis-kit/gfz-scripts/team.py'
ID = 'ASTRA-PUBLISH-SD194-COPIER-AND-QUEUE78-1003'
job = dict(slug='sd194-copier-and-queue78', pairs=[
    ['sd194-copier-limit-frozen-ready', 'sd194-copier-limit', 106, 'b918c8860b8ce742d56b7871cb08655c7ce2d49a98b9a126150d6afba320bc21'],
    ['astra-queue-reconciliation-checkpoint78-frozen-ready', 'astra-queue-reconciliation-checkpoint78', 22, 'c952a3cf354a41ba345ff7d563a9d5189e3b084a75934cf5f51f74311ea24928']],
    message='ASTRA: prove namespace copy bounds and finish returned-evidence queue reconciliation',
    result='Checkpoint78: the original30 READY comprised23 automatic notices,2 information,4 substantive requests and1 optional maintenance request. All26 notice/optional dispositions now handled through118 receipted supported operations verified against canonical history; four older scoped deliveries DONE and18 substantive questions retain precise OPEN prerequisites. Snapshot48666:3 substantive READY, SD194 ACTIVE on methodA. Counts are queue handling, not new FF12 answers. Original partial77/failures immutable; current-board CLI, lock/journal/owner guards and exact preimages used. Unknown intermittent WinError5 cause stays FRONTIER once-routed, not a present all-write blocker. SD194 retained original89B/29pins and caller259 yield a signed-counter invariant: nonNULL lookup copies1..max(1,C) bytes thenNUL; zero/negative limit still copiesone byte. Limit259 needs260 writable bytes and establishesNUL byoffset259. ResolvedNULL name returns-1 without destination access, so the successful bound does not initialize inherited stack. Termination checksNEXT byte; initialNUL doesnot itself stop copier. Unchanged-source formula requiresdisjoint/noninterfering spans; write-count bound survives sequentialaliasing undervalidmemory/intactcode/normalABI. No table/index/capacity validation claimed. 54 boundary calculations are analysis controls, not original-code runs; three actual diagnostic-qualified CLI refusals. Original accepted builder/census/samples not repeated. Current producer e8265fe7/controllerbaf3ecc0, immutable drivers/input/cases/results and actual shared reviewed roleadapter qualification preserved. SPEC independent acceptance and DATA/OPUS canonical consumption pending; actual missing-name inheritedbytes/naturalfieldload/requestacceptance/lifetime/importedcopy/presentation remainOPEN. Gauge binding original822B producer frozen separately, currentcallback+38/scheduling/transitiveeffects remainOPEN. Historical4 accepted runtime eliminations unchanged; new30B770 upperWORD0 predicate pendingacceptance, new successfulcopier bound settledoffline locally; wholeSD194/OVrowclosures0. Goal fullL1L2 plus accepteddeployedM0M5 ACTIVE/NOT_MET. Menu budgetspentextensionunapproved,EXP127invalid/crashunknown,K14acceptedclosed. Allownqueue/proof/control children terminal,noPC/game/native/emulator/instrument/save/config/reference/peerchange. Continue next prepared discriminator from the current board; do not select from stale exported headers.')

job['result'] = 'Current checkpoint83 delivery supplement: render link repair88d435193 exact48paths committed/verified/released and bounded ten-link notice DONE. Proper fullDB HEAD check terminal1 has two unrelated AUDITSPEC review placeholder links, routedonce to owner; whole gate remains FAIL. ORACLE two corrected committed prepare/control runs routedonce for existingseal, not independent acceptance. Additive launcher c7319b1b8522410612187190025fb799925aa67d exact8paths verified/released; fresh committed pathcontrol02 terminal0, actual invocation negative/positive controls pass. Earlier pathcontrol01 INVALID_BEFORE_TEST remains immutable. Required procedure review and receipt sealing pending. Frontier3319c2a6f/543493baf read/write fixes consumed, supportedcurrentguard passes; historical checkpoint77 incident is not the present board. SD194callerframes96820750d independently ACCEPTED, DATA/OPUS consumer incorporation pending actual receipts. CurrentREADY six =three research requests plus three prepared science-publication jobs; this delivery removes one, not a semantic whole-system closure. FullL1L2 plus requiredM0M5 ACTIVE/NOT_MET. Menuallowance spent/unapprovedextension;EXP127invalid;K14closed. NoPC/game/native/emulator/input/attach/save/config/reference/peerprocesschanges. ' + job['result']

def publisher():
    spec = importlib.util.spec_from_file_location('existing_guarded_publisher', W / 'prepare-residue-packet-publication.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.JOBS[ID] = job
    m.ANNOTATION_RESULTS[ID] = {'sd194-copier-limit': 'result-03.json', 'astra-queue-reconciliation-checkpoint78': 'result-complete-dispositions-02.json'}
    actual = m.verify_packet_annotations
    def verify(folder, result_name):
        if Path(folder).name == 'astra-queue-reconciliation-checkpoint78-frozen-ready':
            result = json.loads((Path(folder) / result_name).read_text())
            if result['status'] != 'PREPARED_QUEUE_DISPOSITIONS_COMPLETE_UNKNOWNS_PRESERVED' or result['accepted_prefix'] != '1..118' or result['notices_handled'] != 26:
                raise ValueError('owner receipt incomplete')
            return dict(status='OWNER_TRANSITION_RECEIPTS_NOT_SCIENTIFIC_ANNOTATION', limits=result['limits'])
        return actual(folder, result_name)
    m.verify_packet_annotations = verify
    return m

if sys.argv[1] == '--add':
    folder = W / 'copier-queue78-publication-setup'; folder.mkdir()
    op = dict(action='add', task=dict(id=ID, kind='research', priority='P2', assigned_to='ASTRA',
        target='Immutable SD194 local limit proof and additive completed queue dispositions',
        scope='Explicit128 payload members and short owned ASTRA handoff; no peer consumers',
        completion='Exact paths committed/verified and publication released; review/consumer acceptance remains separate',
        checkpoint='Queued by ASTRA', dependencies=[], resources=[dict(key='@publication'),
            dict(key='file:database/ffxii tza/_index/_inbox/astra.md'),
            dict(key='file:database/ffxii tza/_experiments/evidence/sd194-copier-limit'),
            dict(key='file:database/ffxii tza/_experiments/evidence/astra-queue-reconciliation-checkpoint78')]))
    path = folder / 'operation.json'; path.write_text(json.dumps(op, indent=2))
    result = subprocess.run([sys.executable, '-B', str(T), 'apply', '--agent', 'ASTRA', '--session', 'SOL-ASTRA-copier-queue78-publish', '--file', str(path)], capture_output=True, text=True, timeout=90)
    (folder / 'receipt.json').write_text(json.dumps(dict(exit=result.returncode, stdout=result.stdout, stderr=result.stderr), indent=2))
    print(result.stdout); print(result.stderr)
    if result.returncode or 'Saved revision ' not in result.stdout: raise SystemExit(1)
elif sys.argv[1] == '--deliver': publisher().deliver_once(ID, sys.argv[2])
elif sys.argv[1]=='--load-only':pass
elif sys.argv[1]=='--continue':publisher().publish_prepared(ID)
elif sys.argv[1] == '--preflight':
    print(json.dumps(publisher().verify_packet_annotations(W / 'sd194-copier-limit-frozen-ready', 'result-03.json'), indent=2))
else: raise ValueError('usage --add, --preflight, or --deliver FRESH_TAG')
