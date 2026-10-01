"""Scoped EO3 candidate v2: explicit completion, not a game launcher.

Retains the qualified native control branch and API ordering. Fixes a synthetic
reproducer: CONTINUE followed by deadline is incomplete, never a matched request.
Native controls apply to capture_scoped.py; v2 status change is checked offline.
"""
import ctypes
import time
from ownership import owned_step
from cleanup_candidate import cleanup


def capture(m,pid,slots,seconds,audit,observe,abort_pending):
    if not slots or len(slots)>4 or len(set(slots))!=len(slots) or not 0<seconds<=10:
        raise ValueError('one to four unique addresses and bounded duration required')
    result=dict(status='INVALID',hits=[],observations=[],arming=[],errors=[],cleanup=None,
                detach=False,abort=None,handle_closed=False,matched=False)
    handle=m.k32.OpenProcess(0x1fffff,False,pid)
    if not handle:
        result['errors'].append('OpenProcess failed');return result
    attached=ready=pending=False;initial=None;abort_attempted=False
    try:
        if not m.k32.DebugActiveProcess(pid):raise OSError('DebugActiveProcess failed')
        attached=True
        if not m.k32.DebugSetProcessKillOnExit(False):raise OSError('DebugSetProcessKillOnExit failed')
        event=m.DEBUG_EVENT();end=time.monotonic()+3
        while time.monotonic()<end:
            if not m.k32.WaitForDebugEvent(ctypes.byref(event),100):
                error=ctypes.get_last_error()
                if error not in (0,121):raise OSError('WaitForDebugEvent failed: '+str(error))
                continue
            pending=True;code=event.dwDebugEventCode;tid=event.dwThreadId
            if event.dwProcessId!=pid:raise OSError('unexpected process event')
            status=m.DBG_CONTINUE;error=None;arm_tids=[];stop_after_continue=False
            if code==1:
                rec=event.u.Exception.ExceptionRecord
                if rec.ExceptionCode==m.EXCEPTION_BREAKPOINT and not ready:
                    initial=rec.ExceptionAddress;arm_tids=m.threads_of(pid)
                    if not arm_tids:error='empty initial thread enumeration'
                    ready=True;end=time.monotonic()+seconds
                elif rec.ExceptionCode==m.EXCEPTION_SINGLE_STEP and ready:
                    ctx=m.read_regs(tid)
                    if not owned_step(ctx,rec.ExceptionAddress,slots):
                        status=m.DBG_EXCEPTION_NOT_HANDLED;error='unowned/unreadable step; no callback or resume write'
                    else:
                        result['hits'].append(dict(unix=time.time(),tid=tid,**{
                            n.lower():getattr(ctx,n) for n in ('Rip','Rsp','Rcx','Rdx','R8','R9','Rdi','R10','Rbx','Rax')}))
                        try:
                            observed=observe(m,pid,handle,tid,ctx,audit)
                            decision=observed['decision']
                            if decision not in ('CONTINUE','STOP_MATCHED_PENDING_HEALTH','HOLD_FOR_OWNED_ABORT'):
                                raise ValueError('unrecognized observer decision')
                            result['observations'].append(observed)
                        except Exception as failure:
                            decision='HOLD_FOR_OWNED_ABORT'
                            result['errors'].append('observer failed: '+type(failure).__name__+': '+str(failure))
                        audit.mark('scoped_decision',pid=pid,tid=tid,decision=decision)
                        if decision=='HOLD_FOR_OWNED_ABORT':
                            abort_attempted=True
                            result['abort']=abort_pending(m,pid,handle,tid,audit)
                            pending=not result['abort'].get('pending_event_serviced',False)
                            break  # NEVER call resume_past_breakpoint here
                        if not m.resume_past_breakpoint(tid):error='resume context failed'
                        stop_after_continue=decision=='STOP_MATCHED_PENDING_HEALTH'
                else:
                    status=m.DBG_EXCEPTION_NOT_HANDLED;error='unexpected exception '+hex(rec.ExceptionCode)
            elif code==2 and ready:arm_tids=[tid]
            elif code==5:error='target exited'
            for t in arm_tids:
                ok=m.set_slots(t,slots);result['arming'].append((t,ok))
                if not ok:error='arming failed'
            if not m.k32.ContinueDebugEvent(pid,tid,status):raise OSError('ContinueDebugEvent failed')
            pending=False
            if error:raise OSError(error)
            if stop_after_continue:
                result['matched']=True
                break
        if not ready:raise OSError('initial breakpoint deadline expired')
    except Exception as failure:
        result['errors'].append(type(failure).__name__+': '+str(failure))
    finally:
        if attached:
            if not abort_attempted:
                try:
                    if ready and not pending:
                        result['cleanup']=cleanup(m,pid,handle,audit,ready=True,initial_break_address=initial,slots=slots)
                    else:result['errors'].append('no prepared cleanup boundary')
                except Exception as failure:result['errors'].append('cleanup exception: '+str(failure))
            # If the target already exited, record the API result; no live-target
            # detach claim follows from the abort branch.
            result['detach']=bool(m.k32.DebugActiveProcessStop(pid))
        result['handle_closed']=bool(m.k32.CloseHandle(handle))
    if abort_attempted:
        if result['abort'] and result['abort'].get('terminal') and result['handle_closed']:
            result['status']='CONTROL_ABORTED'  # intentionally not a semantic verdict
    elif (not result['errors'] and result['cleanup']
          and result['cleanup']['status']=='PASS' and result['detach'] and result['handle_closed']
          and result['arming'] and all(x[1] for x in result['arming'])):
        result['status']='MATCHED_PENDING_HEALTH' if result['matched'] else 'INCOMPLETE'
    audit.mark('scoped_capture_end',status=result['status'],errors=result['errors'],detach=result['detach'])
    return result
