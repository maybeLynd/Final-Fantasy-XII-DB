"""Deterministic Win32 event fixture; NOT original-game evidence."""
import ctypes
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent


class EventFixture:
    def __init__(self, module, fail_clear=False):
        self.m = module
        self.fail_clear = fail_clear
        self.stopped = False
        self.events = iter([(3,0),(1,0x3A1C50),(1,0x3A1C8C)])
        self.rip = 0
        self.stores = []
        self.registers = {tid:[0]*6 for tid in [11,12]}

    def DebugSetProcessKillOnExit(self, flag): return 1
    def DebugActiveProcess(self, pid): return 1
    def DebugActiveProcessStop(self, pid): return 1
    def OpenThread(self, flags, inherit, tid): return tid
    def CloseHandle(self, handle): return 1

    def WaitForDebugEvent(self, ptr, timeout):
        code,self.rip = next(self.events)
        e = ptr._obj
        e.dwDebugEventCode, e.dwProcessId, e.dwThreadId = code,1,11
        e.u.Exception.ExceptionRecord.ExceptionCode = self.m.EXCEPTION_SINGLE_STEP
        e.u.Exception.ExceptionRecord.ExceptionAddress = self.rip
        self.stopped = True
        return 1

    def ContinueDebugEvent(self, pid, tid, status):
        self.stopped = False
        return 1

    def GetThreadContext(self, handle, ptr):
        ctx = ptr._obj
        ctx.Rip,ctx.Rsp,ctx.EFlags = self.rip,0x100000,0x202
        for key,value in zip(['Dr0','Dr1','Dr2','Dr3','Dr6','Dr7'],self.registers[handle]):
            setattr(ctx,key,value)
        return 1

    def SetThreadContext(self, handle, ptr):
        ctx = ptr._obj
        values = [getattr(ctx,k) for k in ['Dr0','Dr1','Dr2','Dr3','Dr6','Dr7']]
        self.stores.append(dict(tid=handle, stopped=self.stopped, flags=ctx.ContextFlags,
                                dr0=ctx.Dr0, rip=ctx.Rip))
        if self.fail_clear and handle == 12 and self.rip == 0x3A1C8C and not ctx.Dr0:
            ctypes.set_last_error(5)
            return 0
        self.registers[handle] = values
        return 1


class Tests(unittest.TestCase):
    def run_fixture(self, before, fail_clear=False):
        spec=importlib.util.spec_from_file_location('variant_under_test',HERE/'hwbp-variant.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        fake=EventFixture(m,fail_clear);m.k32=fake
        m.threads_of=lambda pid:[11,12]
        m.cpu_seconds=lambda pid:None
        with tempfile.TemporaryDirectory(prefix='exp016-unit-') as tmp:
            api=Path(tmp)/'api.json';trace=Path(tmp)/'trace.tsv'
            saved=sys.argv
            sys.argv=['hwbp-variant.py','--pid','1','--addr','003A1C50','--addr','003A1C8C',
                      '--stop-after','2','--seconds','1','--api-out',str(api),'--trace-out',str(trace)]
            if before:sys.argv+=['--cleanup-before-continue']
            try:self.assertEqual(m.main(),0)
            finally:sys.argv=saved
            rows=json.loads(api.read_text())
            self.assertEqual([r['operation'] for r in rows[:2]],
                             ['DebugActiveProcess', 'DebugSetProcessKillOnExit'])
            self.assertEqual(len(trace.read_text().splitlines()),3)
            self.assertEqual(rows[-1]['operation'],'DebugActiveProcessStop')
            return fake,rows

    def test_only_original_order_clears_after_continue(self):
        old,oldrows=self.run_fixture(False)
        new,newrows=self.run_fixture(True)
        clears=lambda f:[x for x in f.stores if x['flags']==0x100010 and x['dr0']==0]
        self.assertEqual(len(clears(old)),2)
        self.assertTrue(all(not x['stopped'] for x in clears(old)))
        self.assertEqual(len(clears(new)),2)
        self.assertTrue(all(x['stopped'] for x in clears(new)))
        # Both branches retain the two original resume-context operations.
        self.assertEqual(sum(x['flags']==0x10001B for x in old.stores),2)
        self.assertEqual(sum(x['flags']==0x10001B for x in new.stores),2)

    def test_failed_clear_is_retained_and_fallback_is_identifiable(self):
        fake,rows=self.run_fixture(True,True)
        failures=[x for x in rows if x['operation']=='SetThreadContext' and not x['result']]
        self.assertTrue(failures)
        self.assertTrue(all(x['error']==5 for x in failures))
        done=next(x for x in rows if x['operation']=='clear_before_continue_end')
        self.assertFalse(done['all_succeeded'])
        self.assertTrue(any(x['operation']=='fallback_or_original_clear_after_continue' for x in rows))

    def test_policy_failure_preserves_receipt_without_context_work(self):
        spec=importlib.util.spec_from_file_location('variant_policy_failure',HERE/'hwbp-variant.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        fake=EventFixture(m);m.k32=fake
        def fail_policy(flag):
            ctypes.set_last_error(6)
            return 0
        fake.DebugSetProcessKillOnExit=fail_policy
        m.cpu_seconds=lambda pid:None
        with tempfile.TemporaryDirectory(prefix='exp018-policy-') as tmp:
            api=Path(tmp)/'api.json'
            saved=sys.argv
            sys.argv=['hwbp-variant.py','--pid','1','--no-arm','--api-out',str(api)]
            try:self.assertEqual(m.main(),3)
            finally:sys.argv=saved
            rows=json.loads(api.read_text())
            self.assertEqual([r['operation'] for r in rows],
                             ['DebugActiveProcess','DebugSetProcessKillOnExit','DebugActiveProcessStop'])
            self.assertEqual(rows[1]['error'],6)
            self.assertEqual(fake.stores,[])


if __name__=='__main__':unittest.main()
