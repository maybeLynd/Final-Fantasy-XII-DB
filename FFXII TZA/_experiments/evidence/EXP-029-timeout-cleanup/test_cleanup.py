"""Deterministic event/failure controls; not live evidence."""
import ctypes
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from timeout_cleanup import cleanup

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('snapshot', HERE/'hwbp-source.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Fixture:
    def __init__(self, failure=None):
        self.failure = failure
        self.stopped = False
        self.events = iter([(2, 12), (1, 12)])
        self.calls = []
        self.rows = []
        self.k32 = self
        self.DEBUG_EVENT = m.DEBUG_EVENT
        self.DBG_CONTINUE = m.DBG_CONTINUE
        self.DBG_EXCEPTION_NOT_HANDLED = m.DBG_EXCEPTION_NOT_HANDLED
        self.EXCEPTION_BREAKPOINT = m.EXCEPTION_BREAKPOINT
        self.EXCEPTION_SINGLE_STEP = m.EXCEPTION_SINGLE_STEP

    def mark(self, name, **values): self.rows.append((name, values))
    def DebugBreakProcess(self, handle):
        self.calls.append('break')
        return self.failure != 'request'
    def WaitForDebugEvent(self, ptr, milliseconds):
        self.calls.append('wait')
        if self.failure == 'wait':
            ctypes.set_last_error(6)
            return 0
        try: code, tid = next(self.events)
        except StopIteration:
            ctypes.set_last_error(121)
            return 0
        event = ptr._obj
        event.dwDebugEventCode, event.dwProcessId, event.dwThreadId = code, 1, tid
        event.u.Exception.ExceptionRecord.ExceptionCode = self.EXCEPTION_BREAKPOINT
        self.stopped = True
        return 1
    def ContinueDebugEvent(self, pid, tid, status):
        self.calls.append('continue')
        self.stopped = False
        return self.failure != 'continue'
    def threads_of(self, pid): return [] if self.failure == 'empty' else [11, 12]
    def set_slots(self, tid, slots):
        assert self.stopped
        self.calls.append('clear')
        return not (self.failure == 'clear' and tid == 12)
    def read_regs(self, tid):
        assert self.stopped
        return SimpleNamespace(Dr0=int(self.failure == 'readback'), Dr1=0, Dr2=0, Dr3=0, Dr7=0)


class Tests(unittest.TestCase):
    def test_success_waits_past_creation_and_clears_before_continue(self):
        f = Fixture()
        result = cleanup(f, 1, 9, f, ready=True)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(f.calls, ['break','wait','continue','wait','clear','clear','continue'])

    def test_failures_never_pass(self):
        for failure in ('request','wait','continue','clear','readback','empty'):
            with self.subTest(failure=failure):
                f = Fixture(failure)
                self.assertEqual(cleanup(f, 1, 9, f, ready=True)['status'], 'INVALID')

    def test_no_event_is_incomplete(self):
        f = Fixture()
        f.events = iter([])
        self.assertEqual(cleanup(f, 1, 9, f, ready=True, seconds=0.001)['status'], 'INVALID')

    def test_unprepared_call_does_not_request_break(self):
        f = Fixture()
        with self.assertRaises(ValueError): cleanup(f, 1, 9, f, ready=False)
        self.assertEqual(f.calls, [])


if __name__ == '__main__': unittest.main()
