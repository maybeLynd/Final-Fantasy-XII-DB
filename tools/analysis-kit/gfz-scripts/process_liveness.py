# -*- coding: utf-8 -*-
"""Sample a process's CPU over a wall interval. GetProcessTimes, no dependencies.

A wedged game and a busy game are told apart by a RATE, not a total: the earlier session's
symptom was 0.062 s of CPU across 8.1 s wall, and a total alone would not have shown it.
"""
import ctypes
import ctypes.wintypes as w
import sys
import time

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


class FT(ctypes.Structure):
    _fields_ = [("lo", w.DWORD), ("hi", w.DWORD)]

    def val(self):
        return (self.hi << 32) | self.lo


def times(h):
    c, e, kern, u = FT(), FT(), FT(), FT()
    if not k32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(e),
                               ctypes.byref(kern), ctypes.byref(u)):
        raise OSError(ctypes.get_last_error())
    return (kern.val() + u.val()) / 1e7          # 100 ns units -> seconds


def main():
    pid = int(sys.argv[1])
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
    label = sys.argv[3] if len(sys.argv) > 3 else ""
    h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h:
        print("%-26s NO PROCESS (pid %d)" % (label, pid))
        return 2
    a = times(h)
    time.sleep(secs)
    b = times(h)
    used, rate = b - a, (b - a) / secs
    print("%-26s %6.3f s CPU over %.1f s wall = %5.1f %% of one core   %s"
          % (label, used, secs, rate * 100.0,
             "ALIVE" if rate >= 0.02 else "**WEDGED**"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
