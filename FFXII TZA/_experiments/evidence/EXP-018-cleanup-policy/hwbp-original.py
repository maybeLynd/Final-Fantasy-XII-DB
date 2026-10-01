#!/usr/bin/env python3
"""hwbp.py - hardware breakpoints on FFXII; validate liveness in the actual state.

Why this exists
---------------
`EW-2`: attaching the dbgeng-based MCP debugger **freezes the game** -- 0.000 CPU seconds over
2.0 s wall against a control that burned 1.984, with the engine reporting `running`, and only
detach resumes it. Breakpoints, watchpoints and traces are all unusable through it, and a trace
that reports zero hits is reporting a frozen process rather than a quiet one.

That blocks every causality experiment, and `INTEGRATION` parity in particular: charter section
21 asks for *the caller the game actually uses*, and knowing whether a function is called at all
needs a breakpoint that does not stop the world.

What this does instead
----------------------
The plain Win32 debug API, driven directly:

    DebugActiveProcess -> WaitForDebugEvent / ContinueDebugEvent loop -> DebugActiveProcessStop

**Hardware** breakpoints, via the DR registers of every thread, so **no code byte is modified**.
An INT3 patch would be a write into the reference environment; a debug register is not, and it
also survives code the game may checksum.

On a hit the handler records RIP and the four integer-argument registers, **rewinds nothing**,
sets the resume flag and continues immediately. The game keeps running.

The three things that make this trustworthy
-------------------------------------------
1. **It measures whether the target is still executing.** CPU time is sampled before, during and
   after; a run that froze the game is reported as such rather than as "no hits".
2. **It attempts detach in finally after attachment.** The return from
   `DebugActiveProcessStop` is currently unchecked; verify debugger absence externally.
   After attaching, `DebugSetProcessKillOnExit(FALSE)` must succeed before any event/context
   work begins. If setup fails, attempt detach and abort. This does not protect the interval
   between attach and policy setup, or prevent damage from context writes. EXP-017 tests the
   successful policy with a disposable process; no debugger-loss test against the game is claimed.
3. **A negative needs a positive control.** `--control <addr>` sets a second breakpoint on a
   function that must be called; if the control does not fire, the run reports the instrument as
   unproven and the target's zero means nothing.

**It writes no process memory.** It writes thread debug registers and, on a single-step trap,
the resume flag. Cleanup attempts to clear debug registers to zero; it does not restore a saved
pre-attach context. Check operation results and post-detach behavior externally.

THE THING THAT MATTERS MOST -- a hot breakpoint changes what the program DOES
-----------------------------------------------------------------------------
Historical hit-rate controls (not a general cause for all loaded-state stalls):
measured with the game's own keypress counter, three presses per sample:

    attached, no breakpoints armed, DR registers cleared        3 of 3   input fine
    one COLD breakpoint  (003EAA70 at the front-end, 0 hits)    3 of 3   input fine
    one HOT breakpoint   (0020E600, 255,944 hits in 12 s)       0 of 3   input DEAD

An earlier reading of this file said *attaching* disabled input permanently. **That was wrong**
and is retracted: the `--no-arm` control above attaches, services every debug event, and leaves
input responsive in that tested state. Correction 2026-09-10: --no-arm still calls
set_slots(tid, []), which clears DR0-DR3/DR6/DR7 using SetThreadContext. It is not a
pure attachment/event-loop control. EXP-010 records loaded area227 no-arm survival
with matched input, live code identity and repeated post-detach controls. That does
not resolve historical armed loaded-state stalls or prove attachment universally safe.
That run retained Steam/NVIDIA/Discord overlays; its wrapper's clean label is not overlay-free.

**A hot breakpoint does not merely slow the game down -- it changes which of its code runs.**
With `0020E600` and `00265270` armed together, `003EAA70` recorded **0 hits in 8 s in-world**.
Armed **alone**, in the same state, it recorded **1,130,002 hits in 75 s**. The negative was an
artifact of the instrument's own load.

**The operating rules that follow:**

1. **Never let a hot breakpoint share a run with the target you are measuring.** Arm the target
   alone, and take the control in a separate run.
2. A run whose breakpoints are firing tens of thousands of times a second is **perturbing** the
   program; treat every observation from it, including the target's, as suspect.
3. The historical cold front-end control preserved input; validate other states separately.
"""
import argparse
import ctypes
import io
import ctypes.wintypes as w
import os
import struct
import sys
import time

k32 = ctypes.WinDLL("kernel32", use_last_error=True)

DEBUG_PROCESS_EVENTS = {
    1: "EXCEPTION", 2: "CREATE_THREAD", 3: "CREATE_PROCESS", 4: "EXIT_THREAD",
    5: "EXIT_PROCESS", 6: "LOAD_DLL", 7: "UNLOAD_DLL", 8: "OUTPUT_DEBUG_STRING", 9: "RIP",
}
EXCEPTION_SINGLE_STEP = 0x80000004
EXCEPTION_BREAKPOINT = 0x80000003
DBG_CONTINUE = 0x00010002
DBG_EXCEPTION_NOT_HANDLED = 0x80010001
CONTEXT_DEBUG_REGISTERS = 0x00100010
CONTEXT_FULL = 0x0010000B
THREAD_ALL = 0x1FFFFF
TH32CS_SNAPTHREAD = 0x00000004


class EXCEPTION_RECORD(ctypes.Structure):
    pass


EXCEPTION_RECORD._fields_ = [
    ("ExceptionCode", w.DWORD), ("ExceptionFlags", w.DWORD),
    ("ExceptionRecord", ctypes.POINTER(EXCEPTION_RECORD)),
    ("ExceptionAddress", ctypes.c_void_p), ("NumberParameters", w.DWORD),
    ("ExceptionInformation", ctypes.c_ulonglong * 15)]


class EXCEPTION_DEBUG_INFO(ctypes.Structure):
    _fields_ = [("ExceptionRecord", EXCEPTION_RECORD), ("dwFirstChance", w.DWORD)]


class _U(ctypes.Union):
    _fields_ = [("Exception", EXCEPTION_DEBUG_INFO), ("pad", ctypes.c_ubyte * 160)]


class DEBUG_EVENT(ctypes.Structure):
    _fields_ = [("dwDebugEventCode", w.DWORD), ("dwProcessId", w.DWORD),
                ("dwThreadId", w.DWORD), ("u", _U)]


class M128A(ctypes.Structure):
    _fields_ = [("Low", ctypes.c_ulonglong), ("High", ctypes.c_longlong)]


class CONTEXT(ctypes.Structure):
    _pack_ = 16
    _fields_ = [
        ("P1Home", ctypes.c_ulonglong), ("P2Home", ctypes.c_ulonglong),
        ("P3Home", ctypes.c_ulonglong), ("P4Home", ctypes.c_ulonglong),
        ("P5Home", ctypes.c_ulonglong), ("P6Home", ctypes.c_ulonglong),
        ("ContextFlags", w.DWORD), ("MxCsr", w.DWORD),
        ("SegCs", w.WORD), ("SegDs", w.WORD), ("SegEs", w.WORD),
        ("SegFs", w.WORD), ("SegGs", w.WORD), ("SegSs", w.WORD), ("EFlags", w.DWORD),
        ("Dr0", ctypes.c_ulonglong), ("Dr1", ctypes.c_ulonglong),
        ("Dr2", ctypes.c_ulonglong), ("Dr3", ctypes.c_ulonglong),
        ("Dr6", ctypes.c_ulonglong), ("Dr7", ctypes.c_ulonglong),
        ("Rax", ctypes.c_ulonglong), ("Rcx", ctypes.c_ulonglong),
        ("Rdx", ctypes.c_ulonglong), ("Rbx", ctypes.c_ulonglong),
        ("Rsp", ctypes.c_ulonglong), ("Rbp", ctypes.c_ulonglong),
        ("Rsi", ctypes.c_ulonglong), ("Rdi", ctypes.c_ulonglong),
        ("R8", ctypes.c_ulonglong), ("R9", ctypes.c_ulonglong),
        ("R10", ctypes.c_ulonglong), ("R11", ctypes.c_ulonglong),
        ("R12", ctypes.c_ulonglong), ("R13", ctypes.c_ulonglong),
        ("R14", ctypes.c_ulonglong), ("R15", ctypes.c_ulonglong),
        ("Rip", ctypes.c_ulonglong),
        ("FltSave", ctypes.c_ubyte * 512),
        ("VectorRegister", M128A * 26), ("VectorControl", ctypes.c_ulonglong),
        ("DebugControl", ctypes.c_ulonglong), ("LastBranchToRip", ctypes.c_ulonglong),
        ("LastBranchFromRip", ctypes.c_ulonglong), ("LastExceptionToRip", ctypes.c_ulonglong),
        ("LastExceptionFromRip", ctypes.c_ulonglong)]


def xmm0_f32(ctx):
    """-> xmm0's low 4 bytes as a float32.

    `CONTEXT.FltSave` is the raw 512-byte `XMM_SAVE_AREA32`. Its layout puts the 8 x87 registers
    at +32 (`M128A * 8` = 128 bytes) and the 16 XMM registers immediately after, so **xmm0 begins
    at +160**. `CONTEXT_FULL` already includes the floating-point state on x64, so nothing else
    had to change to make this readable.

    The offset is asserted by the data, not by this comment: the function this was written for
    returns an angle the contract says lies in (-pi, pi], so a wrong offset produces values that
    fail that test immediately. See the control in the experiment.
    """
    return struct.unpack_from("<f", bytes(ctx.FltSave), 160)[0]


class THREADENTRY32(ctypes.Structure):
    _fields_ = [("dwSize", w.DWORD), ("cntUsage", w.DWORD), ("th32ThreadID", w.DWORD),
                ("th32OwnerProcessID", w.DWORD), ("tpBasePri", ctypes.c_long),
                ("tpDeltaPri", ctypes.c_long), ("dwFlags", w.DWORD)]


class FILETIME(ctypes.Structure):
    _fields_ = [("lo", w.DWORD), ("hi", w.DWORD)]


def cpu_seconds(pid):
    h = k32.OpenProcess(0x0400, False, pid)
    if not h:
        return None
    c, e, kt, ut = FILETIME(), FILETIME(), FILETIME(), FILETIME()
    ok = k32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(e),
                             ctypes.byref(kt), ctypes.byref(ut))
    k32.CloseHandle(h)
    if not ok:
        return None
    q = lambda f: ((f.hi << 32) | f.lo) / 1e7
    return q(kt) + q(ut)


def threads_of(pid):
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0)
    if snap == -1:
        return []
    te = THREADENTRY32()
    te.dwSize = ctypes.sizeof(THREADENTRY32)
    out = []
    if k32.Thread32First(snap, ctypes.byref(te)):
        while True:
            if te.th32OwnerProcessID == pid:
                out.append(te.th32ThreadID)
            if not k32.Thread32Next(snap, ctypes.byref(te)):
                break
    k32.CloseHandle(snap)
    return out


def set_slots(tid, addrs):
    """Program DR0..DR3 with up to four EXECUTE breakpoints. addrs may be shorter; the rest are
    cleared. Returns True if the thread's context was written."""
    h = k32.OpenThread(THREAD_ALL, False, tid)
    if not h:
        return False
    ctx = CONTEXT()
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS
    if not k32.GetThreadContext(h, ctypes.byref(ctx)):
        k32.CloseHandle(h)
        return False
    dr7 = 0
    for i in range(4):
        a = addrs[i] if i < len(addrs) else 0
        setattr(ctx, "Dr%d" % i, a)
        if a:
            dr7 |= (1 << (i * 2))          # local enable
            # RW = 00 (execute), LEN = 00 (1 byte): both zero, so nothing more to set.
    ctx.Dr7 = dr7
    ctx.Dr6 = 0
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS
    ok = bool(k32.SetThreadContext(h, ctypes.byref(ctx)))
    k32.CloseHandle(h)
    return ok


def resume_past_breakpoint(tid):
    """Set EFLAGS.RF and clear DR6 so the SAME instruction does not trap again.

    Without this a hardware execute breakpoint re-fires on the instruction it just reported,
    forever: the debugger loops on one address, the hit count climbs at the speed of the
    debug-event round trip rather than the speed of the program, and the target starves.

    That is not a theory. Sixty consecutive hits on 0020E600 came back as ONE distinct
    (thread, rcx, rdx) triple -- the same call reported sixty times.
    """
    h = k32.OpenThread(THREAD_ALL, False, tid)
    if not h:
        return False
    ctx = CONTEXT()
    ctx.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
    ok = k32.GetThreadContext(h, ctypes.byref(ctx))
    if ok:
        ctx.EFlags |= 0x10000          # RF: skip the breakpoint for exactly one instruction
        ctx.Dr6 = 0                    # and clear the status bits the CPU just set
        ctx.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
        ok = k32.SetThreadContext(h, ctypes.byref(ctx))
    k32.CloseHandle(h)
    return bool(ok)


def read_regs(tid):
    h = k32.OpenThread(THREAD_ALL, False, tid)
    if not h:
        return None
    ctx = CONTEXT()
    ctx.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS
    ok = k32.GetThreadContext(h, ctypes.byref(ctx))
    k32.CloseHandle(h)
    return ctx if ok else None


def attach_with_exit_policy(pid):
    """Establish the debugging connection before selecting detach-on-debugger-exit.

    CORRECTED 2026-09-10: the former unchecked pre-attach call failed with error 6
    in both EXP-016 arms. Windows requires an existing debugging connection.
    Fail before context operations; detach failure is reported, never hidden.
    """
    if not k32.DebugActiveProcess(pid):
        raise OSError(ctypes.get_last_error(), "DebugActiveProcess failed")
    if not k32.DebugSetProcessKillOnExit(False):
        policy_error = ctypes.get_last_error()
        detached = k32.DebugActiveProcessStop(pid)
        detail = "detached before event/context work" if detached else (
            "detach also failed (%d); target may remain attached" % ctypes.get_last_error())
        raise OSError(policy_error, "DebugSetProcessKillOnExit failed; " + detail)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", type=int)
    ap.add_argument("--process", default="FFXII_TZA")
    ap.add_argument("--addr", action="append", default=[],
                    help="code address to break on, hex; repeatable, max 4 with --control")
    ap.add_argument("--control", help="a function that MUST be called, hex -- the positive "
                                      "control without which a zero on --addr means nothing")
    ap.add_argument("--seconds", type=float, default=6.0)
    ap.add_argument("--stop-after", type=int, default=0,
                    help="disarm and finish once this many hits have been seen in total. A hot "
                         "breakpoint perturbs the program, so a BOUNDED sample costs far less "
                         "than a fixed-duration run: it is armed for milliseconds, not seconds")
    ap.add_argument("--trace-out", help="write every recorded hit here as TSV: "
                                        "tid, rip, rax, rbx, rcx, rdx, xmm0 -- in the order seen, so "
                                        "hits in one thread can be paired up afterwards")
    ap.add_argument("--no-arm", action="store_true",
                    help="run the full debug event loop with no breakpoints armed; still clears thread DR registers (not a pure attach-only control)")
    ap.add_argument("--max-hits", type=int, default=40,
                    help="stop recording detail after this many, per address")
    a = ap.parse_args()

    pid = a.pid
    if not pid:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import runtime_probe as RP
        hits = RP.find_process(a.process)
        if not hits:
            sys.stderr.write("hwbp: no %r process running\n" % a.process)
            return 2
        pid = hits[0][0]

    addrs = [int(x, 16) for x in a.addr]
    ctrl = int(a.control, 16) if a.control else None
    slots = list(addrs) + ([ctrl] if ctrl else [])
    if a.no_arm:
        slots = []
    elif not slots:
        sys.stderr.write("hwbp: give at least one --addr\n")
        return 2
    if len(slots) > 4:
        sys.stderr.write("hwbp: x86 has four debug registers; %d requested\n" % len(slots))
        return 2

    print("NOTE: a HOT breakpoint perturbs the game -- it starves input and can stop other code")
    print("      running at all (EW-7). Arm the target ALONE; take the control in its own run.")
    if a.no_arm:
        print("pid %d   --no-arm: attaching and servicing events; no breakpoints armed, DR registers still cleared" % pid)
    else:
        print("pid %d   breakpoints: %s%s"
                    % (pid, ", ".join("%08X" % x for x in addrs),
                       "   control %08X" % ctrl if ctrl else "   (NO CONTROL -- a zero will be unproven)"))

    before = cpu_seconds(pid)
    try:
        attach_with_exit_policy(pid)
    except OSError as error:
        sys.stderr.write("hwbp: %s\n" % error)
        return 3

    counts = {x: 0 for x in slots}
    samples = {x: [] for x in slots}
    trace = [] if a.trace_out else None
    total_hits = 0
    armed_threads = set()
    ev = DEBUG_EVENT()
    t0 = time.time()
    mid_cpu = None
    try:
        while time.time() - t0 < a.seconds:
            if not k32.WaitForDebugEvent(ctypes.byref(ev), 100):
                # No event within the timeout is normal and is NOT a stall: the game runs on.
                for tid in threads_of(pid):
                    if tid not in armed_threads and set_slots(tid, slots):
                        armed_threads.add(tid)
                if mid_cpu is None and time.time() - t0 > a.seconds / 2:
                    mid_cpu = cpu_seconds(pid)
                continue
            code = ev.dwDebugEventCode
            status = DBG_CONTINUE
            if code == 1:                                    # EXCEPTION
                rec = ev.u.Exception.ExceptionRecord
                if rec.ExceptionCode == EXCEPTION_SINGLE_STEP:
                    ctx = read_regs(ev.dwThreadId)
                    if ctx:
                        rip = ctx.Rip
                        hit = next((x for x in slots if x == rip), None)
                        if hit is not None:
                            counts[hit] += 1
                            total_hits += 1
                            if len(samples[hit]) < a.max_hits:
                                samples[hit].append((ctx.Rcx, ctx.Rdx, ctx.R8, ctx.R9))
                            # The ordered trace is what lets an ENTRY hit be paired with the EXIT
                            # hit that follows it in the SAME thread. Registers are recorded raw;
                            # which of them means anything is the caller's business.
                            if trace is not None:
                                trace.append((ev.dwThreadId, rip, ctx.Rax, ctx.Rbx,
                                              ctx.Rcx, ctx.Rdx, xmm0_f32(ctx)))
                            if a.stop_after and total_hits >= a.stop_after:
                                resume_past_breakpoint(ev.dwThreadId)
                                k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, status)
                                break
                    # Only for the thread that actually trapped, and only on a DR trap. Writing
                    # a full context to any other thread, on any other event, wedges the target:
                    # a first attempt did it unconditionally and the game's CPU fell to 0.062 s
                    # over 8.1 s wall.
                    if rec.ExceptionCode == EXCEPTION_SINGLE_STEP:
                        resume_past_breakpoint(ev.dwThreadId)
                elif rec.ExceptionCode == EXCEPTION_BREAKPOINT:
                    pass                                     # the initial attach breakpoint
                else:
                    status = DBG_EXCEPTION_NOT_HANDLED
            elif code == 2:                                  # CREATE_THREAD
                if set_slots(ev.dwThreadId, slots):
                    armed_threads.add(ev.dwThreadId)
            elif code == 3:                                  # CREATE_PROCESS
                for tid in threads_of(pid):
                    if set_slots(tid, slots):
                        armed_threads.add(tid)
            elif code == 5:                                  # EXIT_PROCESS
                print("the target exited during the run")
                break
            k32.ContinueDebugEvent(ev.dwProcessId, ev.dwThreadId, status)
    finally:
        for tid in threads_of(pid):
            set_slots(tid, [])
        k32.DebugActiveProcessStop(pid)

    if a.trace_out and trace is not None:
        with io.open(a.trace_out, "w", encoding="utf-8", newline=chr(10)) as f:
            f.write("tid\trip\trax\trbx\trcx\trdx\txmm0\n")
            for row in trace:
                f.write("%d\t%08X\t%016X\t%016X\t%016X\t%016X\t%.9g\n" % row)
        print("wrote %s: %d hit(s) in the order seen" % (a.trace_out, len(trace)))

    after = cpu_seconds(pid)
    wall = time.time() - t0
    print("threads armed            : %d" % len(armed_threads))
    if before is not None and after is not None:
        used = after - before
        # RATE, not an absolute: a --stop-after run can finish in 0.1 s wall, where even a
        # healthy target has used only a few hundredths of a second. Judging that as FROZEN is
        # a false alarm, and this check exists to stop exactly that kind of mistake.
        frozen = wall > 1.0 and (used / wall) < 0.02
        print("target CPU while attached: %.3f s over %.1f s wall  (%.0f %%, %s)"
              % (used, wall, 100.0 * used / wall if wall else 0.0,
                 "**FROZEN**" if frozen else "it kept running"))
        if frozen:
            print("Every count below is therefore meaningless -- a frozen process is quiet.")
    print()
    for x in slots:
        tag = "control" if ctrl and x == ctrl else "target "
        print("  %s %08X  hits %d" % (tag, x, counts[x]))
        for r in samples[x][:5]:
            print("      rcx=%016X rdx=%016X r8=%016X r9=%016X" % r)
    print()
    if ctrl:
        if counts[ctrl] == 0:
            print("THE CONTROL DID NOT FIRE. The instrument is unproven and a zero on any target")
            print("address says nothing. Do not record a negative from this run.")
            return 1
        print("The control fired %d time(s), so the instrument works and a zero on a target is a"
              % counts[ctrl])
        print("real negative for it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
