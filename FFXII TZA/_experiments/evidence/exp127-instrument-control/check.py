"""Retained-API reduction and synthetic dispatch tests; NO native API calls.

Only selected AST definitions are evaluated. WinDLL, load_source and CLI/main
from historical code are never imported/executed. All process/context methods
in the disposable fixture are Python fakes. This is not original FF12 execution.
"""
import argparse
import ast
from collections import Counter
import ctypes
import ctypes.wintypes as w
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

from ownership import owned_step

E = Path(__file__).resolve().parent
OLD = E.parent / 'skeletal-reset-live'
PIN = {
    'capture.py': '41b548c7a71c0713928ed7d8e62a5b4607172da23a29de2e18f3785ab7b93633',
    'timeout_cleanup.py': '865d788d6c98bd5b4de7a19b1d3c845e434cdd96e12119249a00711ad1d3fe7a',
    'api_receipts.py': 'cb80e1ade858bad7372aeec54a712f9db63ee60beaab987018f7c17948e1234a',
    'hwbp-source.py': '81a8510288dc5a4e1d93c221659c49926039e66aa277da3f1fea59aa193879f6',
}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def selected(path, names, namespace):
    tree = ast.parse(path.read_text())
    selected_nodes = [n for n in tree.body if
                      isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names
                      or isinstance(n, ast.Assign) and any(
                          isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                          and t.value.id in names for t in n.targets)]
    assert {n.name for n in selected_nodes if hasattr(n, 'name')} == set(names)
    exec(compile(ast.Module(body=selected_nodes, type_ignores=[]), str(path), 'exec'), namespace)


def receipt_check():
    out = {'method': 'A: existing API-receipt analysis; no process access', 'arms': {}}
    inputs = {}
    for name, digest in PIN.items():
        assert sha(E / 'original' / name) == digest, name
    for arm in ('control', 'skeletal'):
        p = OLD / arm / 'capture'
        raw = json.loads((p / 'api.json').read_text())
        result = json.loads((p / 'result.json').read_text())
        assert result['sources'] == PIN
        assert raw and result['hits']
        slots = [0x3A1C50] if arm == 'control' else [0x3A1C50, 0x3E3C30, 0x3E3C7A, 0x3E3C7F]
        phase, current, groups = 'capture', None, []
        for i, row in enumerate(raw):
            if row['operation'] == 'timeout_cleanup_begin':
                assert current is None
                phase = 'cleanup'
            if row['operation'] == 'WaitForDebugEvent' and row['result']:
                assert current is None, ('event not continued', i)
                current = {'phase': phase, 'event': row, 'api_index': i, 'rows': []}
            elif row['operation'] == 'ContinueDebugEvent':
                assert current is not None
                assert row['pid'] == current['event']['pid'] and row['tid'] == current['event']['tid']
                current['continue'] = row
                groups.append(current)
                current = None
            elif current is not None:
                current['rows'].append(row)
        assert current is None
        steps = [g for g in groups if g['event'].get('exception') == 0x80000004]
        assert steps
        anomalies, changes, counts, replay_hits = [], Counter(), Counter(), []
        for g in steps:
            ev, rows = g['event'], g['rows']
            gets = [r for r in rows if r['operation'] == 'GetThreadContext']
            sets = [r for r in rows if r['operation'] == 'SetThreadContext']
            opens = [r for r in rows if r['operation'] == 'OpenThread']
            if not (len(gets) == (2 if g['phase'] == 'capture' else 1) and len(sets) == 1
                    and all(r['result'] for r in gets + sets)
                    and len(opens) == len(gets)
                    and all(r['tid'] == ev['tid'] and r['result'] for r in opens)
                    and all(o['result'] == r['handle'] for o, r in zip(opens, gets))
                    and sets[0]['handle'] == gets[-1]['handle']
                    and all(r['requested_flags'] == 0x10001B for r in gets + sets)
                    and g['continue']['result'] and g['continue']['status'] == 0x10002):
                anomalies.append({'index': g['api_index'], 'issue': 'API shape'})
                continue
            for r in gets:
                if not owned_step(SimpleNamespace(**r['context']), ev['address'], slots):
                    anomalies.append({'index': g['api_index'], 'issue': 'ownership predicate'})
            before, after = gets[-1]['context'], sets[0]['context']
            expected = dict(before, Dr6=0, EFlags=before['EFlags'] | 0x10000)
            if after != expected:
                anomalies.append({'index': g['api_index'], 'issue': 'recorded context change'})
            changes.update(k for k in before if before[k] != after[k])
            counts[(g['phase'], f"{ev['address']:08X}")] += 1
            if g['phase'] == 'capture':
                replay_hits.append((ev['tid'], ev['address'], gets[0]['context']['Rsp']))
        assert replay_hits == [(h['tid'], h['rip'], h['rsp']) for h in result['hits']]
        assert not anomalies, anomalies
        out['arms'][arm] = {
            'debug_events': len(groups), 'single_steps': len(steps),
            'counts_by_phase_address': {f'{a}/{b}': c for (a, b), c in sorted(counts.items())},
            'recorded_context_changed_fields': dict(changes),
            'raw_hit_sequence_matches': True, 'ownership_or_recorded_write_anomalies': anomalies,
            'unknowns': ['FirstChance was not logged', 'integer registers other than RIP/RSP not in context-write receipts',
                         'floating/vector state not in context-write receipts', 'target-side effects and post-detach events not captured']}
        for name in ('api.json', 'result.json'):
            path = p / name
            inputs[path.relative_to(E.parent).as_posix()] = sha(path)
    out['input_sha256'] = inputs
    out['interpretation'] = ('Saved events do not reproduce the foreign-step dispatch defect. '
                             'Additional cleanup steps exist outside result.hits; they are not semantic samples. '
                             'No cause of the FF12 error established; EXP127 stays INVALID_POST_TRACE.')
    return out


class Clock:
    def __init__(self): self.now = 0.0
    def monotonic(self): return self.now
    def time(self): return self.now


def functions(candidate, clock, predicate=owned_step):
    ns = {'ctypes': ctypes, 'time': clock, 'owned_step': predicate}
    cleanup_path = E / ('cleanup_candidate.py' if candidate else 'original/timeout_cleanup.py')
    selected(cleanup_path, ['cleanup'], ns)
    capture_path = E / ('capture_candidate.py' if candidate else 'original/capture.py')
    selected(capture_path, ['capture'], ns)
    return ns['capture']


class Fixture:
    DBG_CONTINUE = 0x10002
    DBG_EXCEPTION_NOT_HANDLED = 0x80010001
    EXCEPTION_BREAKPOINT = 0x80000003
    EXCEPTION_SINGLE_STEP = 0x80000004

    def __init__(self, clock, variant, where):
        ns = {'ctypes': ctypes, 'w': w}
        selected(E / 'original/hwbp-source.py',
                 ['EXCEPTION_RECORD', 'EXCEPTION_DEBUG_INFO', '_U', 'DEBUG_EVENT'], ns)
        self.DEBUG_EVENT = ns['DEBUG_EVENT']
        self.clock, self.variant, self.where = clock, variant, where
        self.k32 = self
        self.stopped = self.cleared = False
        self.rows, self.calls, self.resumes = [], [], []
        self.pending_step, self.slots, self.requested = None, [], False
        self.events = [(1, 11, self.EXCEPTION_BREAKPOINT, 0x100, 'attach')]
        if where == 'capture': self.events.append(self.step())

    def step(self):
        return (1, 11, self.EXCEPTION_SINGLE_STEP,
                0x999 if self.variant == 'foreign_rip' else 0x200, self.variant)

    def mark(self, name, **values): self.rows.append((name, values))
    def OpenProcess(self, *args): return 1
    def CloseHandle(self, *args): return 1
    def DebugActiveProcess(self, *args): return 1
    def DebugSetProcessKillOnExit(self, *args): return 1
    def DebugActiveProcessStop(self, *args): return 1
    def threads_of(self, pid): return [11, 12]

    def set_slots(self, tid, slots):
        assert self.stopped
        self.slots = list(slots)
        if not slots: self.cleared = True
        self.calls.append(('slots', tid, list(slots)))
        return True

    def DebugBreakProcess(self, *args):
        self.requested = True
        self.events = ([self.step()] if self.where == 'cleanup' else [])
        self.events += [(2, 12, 0, 0, 'create'), (1, 12, self.EXCEPTION_BREAKPOINT, 0x100, 'cleanup')]
        return 1

    def WaitForDebugEvent(self, ptr, timeout):
        if not self.events:
            self.clock.now += 10
            ctypes.set_last_error(121)
            return 0
        code, tid, exc, addr, label = self.events.pop(0)
        ev = ptr._obj
        ev.dwDebugEventCode, ev.dwProcessId, ev.dwThreadId = code, 1, tid
        ev.u.Exception.ExceptionRecord.ExceptionCode = exc
        ev.u.Exception.ExceptionRecord.ExceptionAddress = addr
        ev.u.Exception.dwFirstChance = 1
        self.pending_step = label if exc == self.EXCEPTION_SINGLE_STEP else None
        self.stopped = True
        self.calls.append(('event', label))
        return 1

    def ContinueDebugEvent(self, pid, tid, status):
        self.calls.append(('continue', self.pending_step, status))
        self.stopped = False
        self.pending_step = None
        return 1

    def read_regs(self, tid):
        assert self.stopped
        if self.cleared:
            return SimpleNamespace(**{k: 0 for k in ('Dr0', 'Dr1', 'Dr2', 'Dr3', 'Dr7')})
        if self.pending_step and self.variant == 'read_failure': return None
        ctx = SimpleNamespace(Rip=0x999 if self.variant == 'foreign_rip' else 0x200,
                              Rsp=0x1000, Rcx=1, Rdx=2, R8=3, R9=4, EFlags=0x202,
                              Dr0=0x200, Dr1=0, Dr2=0, Dr3=0, Dr6=0xFFFF0FF1, Dr7=0x401)
        if self.variant == 'tf_same_rip': ctx.Dr6, ctx.EFlags = 0xFFFF4FF0, 0x302
        if self.variant == 'mixed_cause': ctx.Dr6 = 0xFFFF4FF1
        if self.variant == 'wrong_slot': ctx.Dr6 = 0xFFFF0FF2
        if self.variant == 'disabled': ctx.Dr7 = 0x400
        if self.variant == 'data_break': ctx.Dr7 = 0x10401
        return ctx

    def resume_past_breakpoint(self, tid):
        assert self.stopped
        self.resumes.append(self.pending_step)
        self.calls.append(('resume', self.pending_step))
        return True


def case(candidate, variant, where, predicate=owned_step):
    clock = Clock()
    f = Fixture(clock, variant, where)
    result = functions(candidate, clock, predicate)(f, 1, [0x200], 1, f)
    return dict(status=result['status'], errors=result['errors'], hits=len(result['hits']),
                cleanup=result['cleanup']['status'], resumes=f.resumes,
                step_continues=[c[2] for c in f.calls if c[0] == 'continue' and c[1]], calls=f.calls)


def regressions():
    observations = []
    for where in ('capture', 'cleanup'):
        for variant in ('owned', 'foreign_rip', 'tf_same_rip', 'mixed_cause',
                        'wrong_slot', 'disabled', 'data_break', 'read_failure'):
            old, new = case(False, variant, where), case(True, variant, where)
            if variant == 'owned':
                assert old['status'] == new['status'] == 'PASS'
                assert new['resumes'] == ['owned'] and new['step_continues'] == [0x10002]
            else:
                assert old['resumes'] == [variant] and old['step_continues'] == [0x10002]
                assert new['status'] == 'INVALID' and not new['resumes']
                assert new['step_continues'] == [0x80010001]
                if where == 'capture': assert new['hits'] == 0
            observations.append(dict(phase=where, variant=variant, historical=old, candidate=new))
    # Recreate the address-only policy: same-address TF and mixed causes MUST fail.
    weak = lambda ctx, address, slots: ctx is not None and ctx.Rip in slots
    mutant = case(True, 'tf_same_rip', 'capture', weak)
    assert mutant['status'] == 'PASS' and mutant['resumes'] == ['tf_same_rip']
    return dict(method='Synthetic Python event fixtures only; no WinDLL load/native API/process/FF12 execution',
                cases=observations, checks=16, address_only_mutant_rejected_by_regression=True,
                limits='Candidate fixes this demonstrated dispatch decision only. Native behavior/recovery/session health remain unqualified.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--write', action='store_true')
    args = p.parse_args()
    result = {'receipts': receipt_check(), 'regression': regressions(),
              'python': sys.version, 'native_calls': 0}
    if args.write:
        with (E / 'result.json').open('x') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    print(json.dumps({'arms': result['receipts']['arms'],
                      'synthetic_checks': result['regression']['checks'],
                      'native_calls': 0}, indent=2))


if __name__ == '__main__': main()
