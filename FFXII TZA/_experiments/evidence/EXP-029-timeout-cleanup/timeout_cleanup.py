"""Private EXP029 cleanup candidate. Not approved for reference-game use.

Caller owns a successful debug attachment with kill-on-exit disabled, has serviced
the initial breakpoint, and has no outstanding event. This helper never detaches.
On failure the caller must preserve INVALID and perform explicit recovery.
DebugBreakProcess is an intervention, including its remote thread; it is not a
read-only observation. A returned success covers API sequencing, not liveness.
"""
import ctypes
import time


def cleanup(m, pid, process_handle, audit, *, ready, seconds=3.0):
    if not ready:
        raise ValueError('successful attach/policy and serviced initial break required')
    result = dict(status='INVALID', reason='not finished', clears=[], verified=[])
    audit.mark('timeout_cleanup_begin', pid=pid)
    if not m.k32.DebugBreakProcess(process_handle):
        result['reason'] = 'DebugBreakProcess failed'
        audit.mark('timeout_cleanup_end', **result)
        return result
    end = time.monotonic() + seconds
    created = set()
    event = m.DEBUG_EVENT()
    while time.monotonic() < end:
        if not m.k32.WaitForDebugEvent(ctypes.byref(event), 100):
            error = ctypes.get_last_error()
            if error not in (0, 121):
                result['reason'] = 'WaitForDebugEvent failed: %d' % error
                break
            continue
        code, tid = event.dwDebugEventCode, event.dwThreadId
        status = m.DBG_CONTINUE
        terminal = False
        if event.dwProcessId != pid:
            result['reason'] = 'unexpected process event'
            break
        if code == 2:
            created.add(tid)
        elif code == 1:
            exception = event.u.Exception.ExceptionRecord.ExceptionCode
            if exception == m.EXCEPTION_BREAKPOINT and tid in created:
                # Do not clear on CREATE_THREAD: the requested exception must be
                # delivered and handled before detaching from this experiment.
                tids = m.threads_of(pid)
                result['clears'] = [(t, m.set_slots(t, [])) for t in tids]
                for t in tids:
                    ctx = m.read_regs(t)
                    result['verified'].append((t, ctx is not None and all(
                        getattr(ctx, key) == 0 for key in ('Dr0','Dr1','Dr2','Dr3','Dr7'))))
                ok = bool(tids) and all(x[1] for x in result['clears'] + result['verified'])
                result.update(status='PASS' if ok else 'INVALID',
                              reason='stopped-event clear and readback' if ok else 'clear/readback failed',
                              breakpoint_tid=tid)
                audit.mark('stopped_cleanup', **result)
                terminal = True
            elif exception == m.EXCEPTION_SINGLE_STEP:
                if not m.resume_past_breakpoint(tid):
                    result['reason'] = 'resume during cleanup failed'
                    terminal = True
            else:
                status = m.DBG_EXCEPTION_NOT_HANDLED
                result['reason'] = 'unexpected exception during requested stop'
                terminal = True
        elif code == 5:
            result['reason'] = 'target exited before cleanup'
            terminal = True
        if not m.k32.ContinueDebugEvent(pid, tid, status):
            result.update(status='INVALID', reason='ContinueDebugEvent failed')
            break
        if terminal:
            break
    else:
        result['reason'] = 'requested breakpoint not received within deadline'
    audit.mark('timeout_cleanup_end', **result)
    return result
