"""Capture validity fixtures; no original-game evidence."""
import ctypes
import struct
from types import SimpleNamespace
import unittest
import capture


class Fixture:
    def __init__(self, failure=None):
        source = capture.load_source()
        for key in ['DEBUG_EVENT','DBG_CONTINUE','DBG_EXCEPTION_NOT_HANDLED',
                    'EXCEPTION_BREAKPOINT','EXCEPTION_SINGLE_STEP']:
            setattr(self,key,getattr(source,key))
        self.k32 = self
        self.failure = failure
        self.events = [(1,11,self.EXCEPTION_BREAKPOINT,0x100),
                       (1,11,self.EXCEPTION_SINGLE_STEP,0x200)]
        self.stopped = False
        self.requested = False
        self.rows = []
        self.order = []
    def mark(self,name,**values): self.rows.append((name,values))
    def OpenProcess(self,*args): return 1
    def CloseHandle(self,*args): return 1
    def DebugActiveProcess(self,*args): return self.failure != 'attach'
    def DebugSetProcessKillOnExit(self,*args): return self.failure != 'policy'
    def DebugActiveProcessStop(self,*args): return self.failure != 'detach'
    def DebugBreakProcess(self,*args):
        self.requested = True
        self.events = [(2,12,0,0),(1,12,self.EXCEPTION_BREAKPOINT,
                                     0x999 if self.failure=='association' else 0x100)]
        return self.failure != 'request'
    def WaitForDebugEvent(self,ptr,timeout):
        if not self.events:
            ctypes.set_last_error(121)
            return 0
        code,tid,exc,addr = self.events.pop(0)
        event = ptr._obj
        event.dwDebugEventCode,event.dwProcessId,event.dwThreadId = code,1,tid
        event.u.Exception.ExceptionRecord.ExceptionCode = exc
        event.u.Exception.ExceptionRecord.ExceptionAddress = addr
        self.stopped = True
        return 1
    def ContinueDebugEvent(self,*args):
        self.order.append('continue')
        self.stopped = False
        return self.failure != 'continue'
    def threads_of(self,pid): return [11,12]
    def set_slots(self,tid,slots):
        assert self.stopped
        return self.failure != ('arm' if slots else 'clear')
    def read_regs(self,tid):
        assert self.stopped
        return SimpleNamespace(Rip=0x200,Rsp=0x60000800,Rcx=0,Rdx=0,R8=0,R9=0,
                               Dr0=int(self.failure=='readback'),Dr1=0,Dr2=0,Dr3=0,Dr7=0)
    def resume_past_breakpoint(self,tid):
        self.order.append('resume')
        return self.failure != 'resume'
    def ReadProcessMemory(self,handle,address,buffer,size,count):
        assert self.stopped and address==0x60000800 and size==64
        self.order.append('stack')
        raw=struct.pack('<8Q',0x140123456,2,3,4,5,6,7,0xFEDCBA9876543210)
        ctypes.memmove(buffer,raw,64)
        count._obj.value=63 if self.failure=='short_stack' else 64
        ctypes.set_last_error(299 if self.failure=='failed_stack' else 0)
        return self.failure!='failed_stack'


class Tests(unittest.TestCase):
    def test_success(self):
        f = Fixture()
        result = capture.capture(f,1,[0x200],0.002,f)
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(len(result['hits']),1)
        self.assertTrue(result['detach'])
        self.assertEqual(result['hits'][0]['stack']['qwords'],
                         [0x140123456,2,3,4,5,6,7,0xFEDCBA9876543210])
        index=f.order.index('stack')
        self.assertEqual(f.order[index:index+3],['stack','resume','continue'])

    def test_bad_stack_invalidates_but_preserves_cleanup(self):
        for failure in ('short_stack','failed_stack'):
            with self.subTest(failure=failure):
                f=Fixture(failure)
                result=capture.capture(f,1,[0x200],.002,f)
                self.assertEqual(result['status'],'INVALID')
                stack=result['hits'][0]['stack']
                self.assertEqual(stack['status'],'INVALID')
                self.assertNotIn('top_qword',stack)
                self.assertTrue(stack['raw'])
                self.assertEqual(result['cleanup']['status'],'PASS')
                self.assertTrue(result['detach'])

    def test_failures_invalidate_capture(self):
        for failure in ('attach','policy','arm','continue','resume','request','clear',
                        'readback','association','detach'):
            with self.subTest(failure=failure):
                f = Fixture(failure)
                result = capture.capture(f,1,[0x200],0.002,f)
                self.assertEqual(result['status'],'INVALID')
                if failure=='arm':
                    self.assertEqual(result['cleanup']['status'],'PASS')
                    self.assertTrue(result['errors'])
                if failure in ('attach','policy','continue'):
                    self.assertFalse(f.requested)


if __name__=='__main__': unittest.main()
