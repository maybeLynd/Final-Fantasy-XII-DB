"""Read-only reconciliation of one interrupted publication. Never publishes/finishes."""
import ctypes
from ctypes import wintypes as wt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
ROOT = next(p for p in W.parents if (p / 'Database/Tools/analysis-kit/gfz-scripts/team.py').is_file())
sys.path.insert(0, str(ROOT / 'Database/Tools/analysis-kit/gfz-scripts'))
import team

OUT = W / sys.argv[1]
OUT.mkdir()
COMMIT = 'd02293770e149fae885dbf77c8282b8f7ed1399d'
PUB = W / 'publication-uq147-ko-release-partition-01'

def write(name, value):
    with (OUT / name).open('x', encoding='utf8') as f:
        json.dump(value, f, indent=2)

def run(args, data=None):
    p = subprocess.run(args, cwd=ROOT, input=data, capture_output=True, timeout=35)
    if p.returncode:
        raise RuntimeError((args, p.returncode, p.stderr.decode(errors='replace')))
    return p.stdout

class ProcessEntry(ctypes.Structure):
    _fields_ = [('dwSize', wt.DWORD), ('cntUsage', wt.DWORD),
                ('th32ProcessID', wt.DWORD), ('th32DefaultHeapID', ctypes.c_size_t),
                ('th32ModuleID', wt.DWORD), ('cntThreads', wt.DWORD),
                ('th32ParentProcessID', wt.DWORD), ('pcPriClassBase', wt.LONG),
                ('dwFlags', wt.DWORD), ('szExeFile', wt.WCHAR * 260)]

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.CreateToolhelp32Snapshot.argtypes = [wt.DWORD, wt.DWORD]
k32.CreateToolhelp32Snapshot.restype = wt.HANDLE
k32.Process32FirstW.argtypes = [wt.HANDLE, ctypes.POINTER(ProcessEntry)]
k32.Process32FirstW.restype = wt.BOOL
k32.Process32NextW.argtypes = [wt.HANDLE, ctypes.POINTER(ProcessEntry)]
k32.Process32NextW.restype = wt.BOOL
k32.CloseHandle.argtypes = [wt.HANDLE]
k32.CloseHandle.restype = wt.BOOL

def snapshot():
    h = k32.CreateToolhelp32Snapshot(2, 0)
    if h == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        e = ProcessEntry(); e.dwSize = ctypes.sizeof(e)
        if not k32.Process32FirstW(h, ctypes.byref(e)):
            raise ctypes.WinError(ctypes.get_last_error())
        result = {}
        while True:
            result[int(e.th32ProcessID)] = dict(pid=int(e.th32ProcessID),
                parent=int(e.th32ParentProcessID), name=e.szExeFile)
            if not k32.Process32NextW(h, ctypes.byref(e)):
                if ctypes.get_last_error() != 18:
                    raise ctypes.WinError(ctypes.get_last_error())
                break
        return result
    finally:
        if not k32.CloseHandle(h):
            raise ctypes.WinError(ctypes.get_last_error())

try:
    ok, detail = team.board_status(team.BOARD)
    if not ok:
        raise RuntimeError(detail)
    b = json.loads(team.read_board_text(team.BOARD))
    t = next(t for t in b['tasks'] if t['id'] == 'ASTRA-PUBLISH-UQ147-KO-RELEASE-PARTITION-1003')
    if t['status'] != 'ACTIVE' or t.get('agent') != 'ASTRA':
        raise RuntimeError('Current publication ownership changed; no reconciliation writes')
    write('board-preimage.json', dict(revision=b['revision'], epoch=b.get('recovery_epoch'), task=t))
    attempt = json.loads((PUB / 'automated-publication-attempt-01.json').read_text())
    timeout = json.loads((W / 'uq147-ko-release-partition-deliver-02.status.json').read_text())
    if attempt['own_pid'] != 48564 or attempt['status'] != 'STARTED' or timeout['terminal'] is not False:
        raise RuntimeError('Prior attempt changed; reconcile its actual status')
    # Detection control is one disposable child we own, never a peer process.
    c = subprocess.Popen([sys.executable, '-B', '-c', 'import time; time.sleep(12)'],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        processes = snapshot()
        if os.getpid() not in processes or c.pid not in processes or processes[c.pid]['parent'] != os.getpid():
            raise RuntimeError('Process inventory positive/parent control failed')
        descendants = set()
        frontier = {attempt['own_pid']}
        while frontier:
            found = {p for p, row in processes.items() if row['parent'] in frontier}
            found -= descendants | {attempt['own_pid']}
            descendants |= found
            frontier = found
        observation = dict(status='CONTROLLED_SNAPSHOT', root_pid=attempt['own_pid'],
            root_present=attempt['own_pid'] in processes,
            descendants=[processes[p] for p in sorted(descendants)],
            detection_control=dict(parent=os.getpid(), child=c.pid, observed=processes[c.pid]),
            limits='Snapshot only; exited intermediate parents can break ancestry. No peer-by-name termination; no all-process absence claim.')
    finally:
        c.terminate(); c.wait(timeout=10)
    observation['control_child_terminal_exit'] = c.returncode
    write('process-observation.json', observation)
    expected = json.loads((PUB / 'reviewed-sha256.json').read_text())
    paths = json.loads((PUB / 'paths.json').read_text())
    if len(expected) != 69 or set(paths) != set(expected) or len(paths) != 69:
        raise RuntimeError('Reviewed path set invalid')
    message = (PUB / 'message.txt').read_bytes()
    actual_msg = run(['git', 'show', '-s', '--format=%B', COMMIT])
    if actual_msg.rstrip() != message.rstrip():
        raise RuntimeError('Candidate message differs')
    changed = run(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', COMMIT]).decode().splitlines()
    if len(changed) != len(paths) or set(changed) != set(paths):
        raise RuntimeError('Candidate changed paths differ')
    spec = importlib.util.spec_from_file_location('existing_guarded_publisher', W / 'prepare-residue-packet-publication.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    members = m.verify_git_blobs(COMMIT, expected, handoff_bytes=(ROOT / 'Database/FFXII TZA/_index/_inbox/ASTRA.md').read_bytes())
    write('candidate-blob-verification.json', dict(status='EXACT_CANDIDATE_BLOBS_VERIFIED',
        commit=COMMIT, exact_paths=len(paths), members=members,
        commit_identity_basis='Explicit candidate from prior git history, corroborated by exact reviewed payload/message; NOT recovered publisher stdout.',
        limits='This is not the TEAM-required committed-sha receipt, publisher exit, complete delivery or independent scientific acceptance. No task finished.'))
    write('result.json', dict(status='RECONCILED_READ_ONLY', current_revision=b['revision'], current_epoch=b.get('recovery_epoch'),
        producer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        candidate_commit=COMMIT, current_board_check=detail,
        attributable_descendants=len(descendants), publication_receipt_missing=True,
        next='Release only owned publication hold after process ownership reconciliation; ask FRONTIER/OPUS to adjudicate missing receipt and timeout invocation. Never republish unchanged payload.'))
    print('RECONCILED_READ_ONLY: candidate 69 exact blobs; attributable descendants', len(descendants), '; missing publication receipt remains open')
except BaseException as e:
    write('failure.json', dict(type=type(e).__name__, detail=str(e)))
    raise
