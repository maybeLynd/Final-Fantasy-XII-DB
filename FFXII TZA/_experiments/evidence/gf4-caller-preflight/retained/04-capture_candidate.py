"""Offline-tested candidate only. No launcher or native qualification.
Historical capture is preserved in original/. Caller must not deploy this
merely because synthetic controls pass. Full recovery remains separately gated.
"""
import ctypes
import time
from ownership import owned_step
from cleanup_candidate import cleanup

def capture(m, pid, slots, seconds, audit):
    if not slots or len(slots)>4 or seconds<=0:
        raise ValueError('one to four addresses and positive duration required')
    result = dict(status='INVALID', hits=[], arming=[], errors=[], cleanup=None, detach=False)
    handle = m.k32.OpenProcess(0x1FFFFF,False,pid)
    if not handle:
        result['errors'].append('OpenProcess failed')
        return result
    attached = ready = pending = False
    initial = None
    try:
        # Use explicit setup so even a failed policy records detach in this result.
        if not m.k32.DebugActiveProcess(pid):
            raise OSError('DebugActiveProcess failed')
        attached = True
        if not m.k32.DebugSetProcessKillOnExit(False):
            raise OSError('DebugSetProcessKillOnExit failed')
        event = m.DEBUG_EVENT()
        end = time.monotonic()+3.0
        while time.monotonic()<end:
            if not m.k32.WaitForDebugEvent(ctypes.byref(event),100):
                error = ctypes.get_last_error()
                if error not in (0,121): raise OSError('WaitForDebugEvent failed: %d' % error)
                continue
            pending = True
            code, tid = event.dwDebugEventCode,event.dwThreadId
            if event.dwProcessId != pid: raise OSError('unexpected process event')
            status = m.DBG_CONTINUE
            error = None
            arm_tids = []
            if code == 1:
                rec = event.u.Exception.ExceptionRecord
                if rec.ExceptionCode == m.EXCEPTION_BREAKPOINT and not ready:
                    initial = rec.ExceptionAddress
                    arm_tids = m.threads_of(pid)
                    if not arm_tids: error = 'empty initial thread enumeration'
                    ready = True
                    end = time.monotonic()+seconds
                elif rec.ExceptionCode == m.EXCEPTION_SINGLE_STEP and ready:
                    ctx = m.read_regs(tid)
                    if not owned_step(ctx, rec.ExceptionAddress, slots):
                        status = m.DBG_EXCEPTION_NOT_HANDLED
                        error = 'unowned or unreadable single step; no resume write'
                    else:
                        result['hits'].append(dict(unix=time.time(), tid=tid, rip=ctx.Rip,
                            rsp=ctx.Rsp, rcx=ctx.Rcx, rdx=ctx.Rdx, r8=ctx.R8, r9=ctx.R9))
                        if not m.resume_past_breakpoint(tid): error = 'resume context failed'
                else:
                    status = m.DBG_EXCEPTION_NOT_HANDLED
                    error = 'unexpected exception %x' % rec.ExceptionCode
            elif code == 2 and ready:
                arm_tids = [tid]
            elif code == 5:
                error = 'target exited'
            for t in arm_tids:
                ok = m.set_slots(t, slots)
                result['arming'].append((t,ok))
                if not ok: error = 'arming failed'
            if not m.k32.ContinueDebugEvent(pid,tid,status):
                raise OSError('ContinueDebugEvent failed')
            pending = False
            if error: raise OSError(error)
        if not ready: raise OSError('initial breakpoint deadline expired')
    except Exception as error:
        result['errors'].append(str(error))
    finally:
        if attached:
            try:
                if ready and not pending:
                    result['cleanup'] = cleanup(m,pid,handle,audit,ready=True,
                                                initial_break_address=initial, slots=slots)
                else:
                    result['errors'].append('no prepared cleanup boundary')
            except Exception as error:
                result['errors'].append('cleanup exception: '+str(error))
            result['detach'] = bool(m.k32.DebugActiveProcessStop(pid))
        m.k32.CloseHandle(handle)
    if (not result['errors'] and result['cleanup'] and result['cleanup']['status']=='PASS'
            and result['detach'] and result['arming'] and all(x[1] for x in result['arming'])):
        result['status'] = 'PASS'
    audit.mark('capture_end', status=result['status'], errors=result['errors'], detach=result['detach'])
    return result
