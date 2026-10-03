"""Freeze two different evidence kinds without confusing notices with science."""
import hashlib
import importlib.util
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ROOT = next(p for p in W.parents if (p / 'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def freeze(source, destination, files, kind, limits):
    destination.mkdir(); members = []
    for path, name in sorted(files, key=lambda x: x[1]):
        copied = destination / name; copied.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(path, copied)
        if copied.read_bytes() != path.read_bytes(): raise ValueError('immutable copy differs')
        members.append(dict(path=name, bytes=path.stat().st_size, sha256=sha(path)))
    (destination / 'manifest.json').write_text(json.dumps(dict(package=kind, members=members,
        limits=limits, acceptance='Producer/owner evidence; independent acceptance not awarded'), indent=2))
    return dict(folder=destination.name, members=len(members), manifest_sha256=sha(destination / 'manifest.json'))

def main():
    team = load('current_team', ROOT / 'Database/Tools/analysis-kit/gfz-scripts/team.py')
    check = subprocess.run([sys.executable, '-B', str(Path(team.__file__)), 'boardcheck'], capture_output=True, text=True, timeout=90)
    if check.returncode or not check.stdout.strip().startswith('board ok: ') or check.stderr.strip(): raise ValueError('current board guard failed')
    board = json.loads(team.BOARD.read_text(encoding='utf-8'))
    Q = W / 'ready-queue-reconciliation-1002'
    terminal = json.loads((Q / 'finish-current-notice-batches-01/terminal.json').read_text())
    if terminal.get('status') != 'PREPARED_NOTICE_TAIL_COMPLETE' or terminal['last'] != 118: raise ValueError('notice tail incomplete')
    sequence = load('prepared_queue', Q / 'resume-bounded.py').ops()
    accepted = {}
    for folder in [Q / 'apply-01', *sorted(Q.glob('bounded-*')), *sorted(Q.glob('current-*'))]:
        for receipt in folder.glob('[0-9][0-9][0-9].receipt.json'):
            serial = int(receipt.name[:3]); value = json.loads(receipt.read_text())
            if value.get('status') != 'SUPPORTED_TRANSACTION_COMMITTED': continue
            if serial in accepted: raise ValueError('duplicate accepted serial')
            operation_path = receipt.with_name('%03d.op.json' % serial)
            prepared = json.loads(operation_path.read_text()); operation = prepared.get('operation', prepared)
            if operation != sequence[serial - 1]: raise ValueError('operation lineage changed')
            history = [h for h in board['history'] if h.get('agent') == 'ASTRA' and h.get('operation') == operation]
            if not history: raise ValueError('accepted receipt not in current canonical history')
            accepted[serial] = dict(serial=serial, operation=operation,
                raw_operation_text=operation_path.read_bytes().decode(), raw_receipt_text=receipt.read_bytes().decode(),
                operation_file_sha256=sha(operation_path), receipt_file_sha256=sha(receipt), history=history)
    if set(accepted) != set(range(1, 119)): raise ValueError('accepted prefix incomplete')
    plan = json.loads((Q / 'dispositions-01.json').read_text())
    rows = {t['id']: t for t in board['tasks']}; scoped, blocked = [], []
    for disposition in plan['records']:
        if rows[disposition['notification']]['status'] != 'DONE': raise ValueError('notice not finished')
        task = disposition['underlying']
        if task:
            expected = 'BLOCKED' if disposition['disposition'] == 'REBLOCK' else 'DONE'
            if rows[task]['status'] != expected: raise ValueError('underlying disposition differs')
            if disposition['disposition'] == 'REBLOCK': blocked.append(task)
            elif disposition['disposition'] == 'FINISH_SCOPED': scoped.append(task)
    summary = dict(status='PREPARED_QUEUE_DISPOSITIONS_COMPLETE_UNKNOWNS_PRESERVED', revision=board['revision'], epoch=board['recovery_epoch'],
        ready_snapshot=len(team.ready(board, 'ASTRA')), ready_tasks=[t['id'] for t in team.ready(board, 'ASTRA')],
        initial_ready=30, initial_automatic=23, initial_information=2, initial_optional=1, initial_substantive=4,
        notices_handled=len(plan['records']), finished_scoped_original_deliveries=scoped, unresolved_original_requests=blocked,
        accepted_prefix='1..118', supported_current_cli_resumption='after valid current guard and three positive documented CLI writes; not an automatic retry of old failure',
        frontier_cause_question='ASTRA-REQ-FRONTIER-ATOMIC-BOARD-WRITE-DENIAL-1003 remains routed once; intermittent WinError5 cause unknown',
        limits=['26 handled notices/optional dispositions are not 26 new game answers.', 'Four older bounded deliveries completed; eighteen game requests remain open with exact revised prerequisites.',
                'The original audit launch driver hash was not pinned; do not fabricate it. Current-batch drivers and raw receipts are pinned.',
                'The partial checkpoint77 capsule remains immutable. This is its additive successor, not a relabeling.',
                'Current ready count excludes resources held by peers; it may change when publication frees or new requests arrive. SD194 is ACTIVE on a new static prerequisite.',
                'EXP127 invalid/crash unknown, K14 accepted closed, parked menu budget spent/unapproved; goal ACTIVE/NOT_MET.'])
    (Q / 'operation-receipts-02.json').write_text(json.dumps(dict(records=[accepted[i] for i in sorted(accepted)]), indent=2))
    (Q / 'result-complete-dispositions-02.json').write_text(json.dumps(summary, indent=2))
    (Q / 'boardcheck-final-02.json').write_text(json.dumps(dict(exit=check.returncode, stdout=check.stdout, stderr=check.stderr), indent=2))
    (Q / 'README-additive-02.md').write_text('# Additive queue reconciliation\n\nAll118 planned supported operations have exact receipts and current canonical history matches. All26 notice/optional dispositions are handled. Four older deliveries are complete within their original evidence scope; eighteen unresolved requests retain explicit prerequisites. The3-ready snapshot is taken while a peer holds publication and SD194 is active. Counts are operational status, not empirical acceptance. The frozen partial77 record and old failed atomic-write receipts remain unchanged. Current CLI guard/owner/preimage controls were used; FRONTIER still owns the unknown cause investigation. No game or PC session. GoalACTIVE/NOT_MET.\n')
    (Q / '.gitattributes').write_bytes(b'* -text\n')
    qnames = ['.gitattributes', 'input-snapshot-01.json', 'dispositions-01.json', 'DISPOSITIONS.md', 'operation-receipts-02.json',
              'result-complete-dispositions-02.json', 'boardcheck-final-02.json', 'README-additive-02.md', 'apply-current-bounded.py',
              'finish-current-notice-batches.py', 'finish-current-notice-batches-01/terminal.json', 'write-denial-additive-current-receipt-01.json']
    qfiles = [(Q / n, n) for n in qnames] + [(p, p.relative_to(Q).as_posix()) for p in (Q / 'finish-current-notice-batches-01').glob('current-*.json')]
    qfiles.append((Path(__file__), 'freeze-copier-and-queue78.py'))

    P = W / 'sd194-copier-limit'
    for tag, driver in [('proof-03', 'prove.py'), ('control-02', 'control.py')]:
        state = json.loads((P / (tag + '.status.json')).read_text())
        if state.get('terminal') is not True or state.get('exit') != 0 or state.get('exception') is not None or state.get('driver_sha256') != sha(P / driver): raise ValueError('current scientific producer/control failed')
        if not (P / (tag + '.stdout')).read_bytes() or (P / (tag + '.stderr')).read_bytes(): raise ValueError('missing output or diagnostics')
    result = json.loads((P / 'result-03.json').read_text()); controls = json.loads((P / 'controls-02/result.json').read_text())
    if result.get('producer_complete') is not True or not result.get('source_pins') or controls['status'] != 'THREE_ACTUAL_PREREQUISITE_REFUSALS': raise ValueError('invalid/zero producer evidence')
    validator = load('actual_reviewed_roles', W / 'validate-title-source-annotations.py')
    for pin in result['source_pins']:
        path = P / pin['path']
        if sha(path) != pin['sha256']: raise ValueError('source-map preimage changed')
        validator.validate(json.loads(path.read_text()))
    (P / '.gitattributes').write_bytes(b'* -text\n')
    (P / 'environment-01.json').write_text(json.dumps(dict(python=sys.version, executable_sha256=sha(Path(sys.executable)),
        platform=platform.platform(), method=result['method']), indent=2))
    # Retain the original first invocation receipts and exact recovered driver.
    (P / 'invocation-history').mkdir()
    for suffix in ['.status.json', '.stdout', '.stderr']:
        shutil.copyfile(W / 'ov42-gauge-callback-binding' / ('sd194-copier-proof-01' + suffix), P / 'invocation-history' / ('proof-01' + suffix))
    pfiles = [(p, p.relative_to(P).as_posix()) for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    pfiles += [(Path(__file__), 'freeze-copier-and-queue78.py'), (W / 'sd194-copier-limit-claim-01/operation.json', 'claim/operation.json'),
               (W / 'sd194-copier-limit-claim-01/receipt.json', 'claim/receipt.json')]
    outputs = [freeze(Q, W / 'astra-queue-reconciliation-checkpoint78-frozen-ready', qfiles, 'astra-queue-reconciliation-checkpoint78', 'Owner transitions and explicit unresolved residues, not new experiments.'),
               freeze(P, W / 'sd194-copier-limit-frozen-ready', pfiles, 'sd194-copier-limit', 'STATIC_ONLY counter/write bound, successful lookup only; natural missing-name bytes and reachability open.')]
    (W / 'freeze-copier-and-queue78-result.json').write_text(json.dumps(outputs, indent=2))
    for output in outputs: print(json.dumps(output))

if __name__ == '__main__': main()
