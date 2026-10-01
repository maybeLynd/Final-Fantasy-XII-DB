#!/usr/bin/env python3
"""window_focus.py - bring the game's own window to the foreground, and SAY WHETHER IT WORKED.

Why this is a separate tool
---------------------------
`EXP-005` wrote a byte into the input state the game reads, watched it persist untouched, and
concluded **nothing consumes it**. One of the three surviving explanations was that the game does
not process input at all while its window is not foreground -- and every measurement in that
experiment was taken with the harness in the foreground, not the game.

That makes focus a **control**, not a convenience. A watchpoint that reports no reader means one
thing if the game was focused and a completely different thing if it was not.

Windows does not simply grant foreground
----------------------------------------
`SetForegroundWindow` fails silently for a process that does not own the foreground: it returns
FALSE and the window stays where it was. So this tool **verifies with `GetForegroundWindow`
afterwards** and reports what it actually achieved, rather than assuming the call did what it was
asked. A tool that cannot tell success from failure is the thing this project keeps having to
rebuild.

The only state it changes is which window has focus, which the operator was going to change by
hand anyway. It restores nothing, because there is nothing to restore.
"""
import argparse
import ctypes
import ctypes.wintypes as w
import sys
import time

u32 = ctypes.WinDLL("user32", use_last_error=True)
k32 = ctypes.WinDLL("kernel32", use_last_error=True)

ENUMPROC = ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
u32.EnumWindows.argtypes = [ENUMPROC, w.LPARAM]
u32.GetWindowTextW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
u32.GetWindowThreadProcessId.argtypes = [w.HWND, ctypes.POINTER(w.DWORD)]
u32.IsWindowVisible.argtypes = [w.HWND]
u32.SetForegroundWindow.argtypes = [w.HWND]
u32.GetForegroundWindow.restype = w.HWND
u32.ShowWindow.argtypes = [w.HWND, ctypes.c_int]
u32.AttachThreadInput.argtypes = [w.DWORD, w.DWORD, w.BOOL]
u32.BringWindowToTop.argtypes = [w.HWND]
u32.GetWindowRect.argtypes = [w.HWND, ctypes.POINTER(w.RECT)]

SW_RESTORE = 9


def windows_of(pid):
    """Every visible top-level window owned by pid, with its title and size."""
    found = []

    def cb(hwnd, _lp):
        p = w.DWORD()
        u32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value != pid or not u32.IsWindowVisible(hwnd):
            return True
        buf = ctypes.create_unicode_buffer(512)
        u32.GetWindowTextW(hwnd, buf, 512)
        r = w.RECT()
        u32.GetWindowRect(hwnd, ctypes.byref(r))
        found.append((hwnd, buf.value, r.right - r.left, r.bottom - r.top))
        return True

    u32.EnumWindows(ENUMPROC(cb), 0)
    return found


def focus(hwnd):
    """Try to foreground hwnd, then CHECK. Returns (ok, foreground_hwnd)."""
    # A process that does not own the foreground cannot simply take it. Attaching our input
    # queue to the current foreground thread's is the documented way round, and it is still
    # allowed to fail -- which is why the result is verified rather than assumed.
    cur = u32.GetForegroundWindow()
    cur_tid = u32.GetWindowThreadProcessId(cur, None) if cur else 0
    our_tid = k32.GetCurrentThreadId()
    attached = False
    if cur_tid and cur_tid != our_tid:
        attached = bool(u32.AttachThreadInput(our_tid, cur_tid, True))
    try:
        u32.ShowWindow(hwnd, SW_RESTORE)
        u32.BringWindowToTop(hwnd)
        u32.SetForegroundWindow(hwnd)
    finally:
        if attached:
            u32.AttachThreadInput(our_tid, cur_tid, False)
    time.sleep(0.25)
    fg = u32.GetForegroundWindow()
    return (fg == hwnd, fg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", type=int, required=True)
    ap.add_argument("--list", action="store_true", help="list the windows and exit")
    ap.add_argument("--hold", type=float, default=0.0,
                    help="seconds to keep checking that focus was KEPT, not just taken")
    a = ap.parse_args()

    wins = windows_of(a.pid)
    if not wins:
        print("pid %d has no visible top-level window" % a.pid)
        return 2
    for hwnd, title, cx, cy in wins:
        print("  hwnd %#018x  %4d x %-4d  %s" % (hwnd, cx, cy, title or "(no title)"))
    if a.list:
        return 0

    # The game's window is the largest one it owns: a splash or a hidden message-only window
    # would otherwise be picked by accident.
    hwnd = max(wins, key=lambda t: t[2] * t[3])[0]
    ok, fg = focus(hwnd)
    print("SetForegroundWindow -> %s  (foreground is now %#018x)"
          % ("OK" if ok else "REFUSED", fg))
    if ok and a.hold:
        t0 = time.time()
        lost = 0
        while time.time() - t0 < a.hold:
            if u32.GetForegroundWindow() != hwnd:
                lost += 1
            time.sleep(0.05)
        print("held focus: %s (%d of %d polls lost it)"
              % ("yes" if not lost else "NO", lost, int(a.hold / 0.05)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
