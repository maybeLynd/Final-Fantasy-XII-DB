#!/usr/bin/env python3
"""runtime_poke.py - drive the game by writing its own input state. SEPARATE ON PURPOSE.

Why this is not part of runtime_probe.py
----------------------------------------
`runtime_probe.py` opens the process with `PROCESS_VM_READ | PROCESS_QUERY_INFORMATION` and
**never requests write access**, and its docstring says why: *a validation instrument that can
perturb its subject is not a validation instrument*. That guarantee is load-bearing for every
number this project has published from a live process, so it is not being weakened. **This is a
different tool with a different, louder contract.**

What it does
------------
Two OS input paths were tried and both produced **no detectable effect** on the game
(`EXP-004`: scan-code `SendInput`, then virtual-key `SendInput`, both symmetric against the noise
floor). So instead of feeding the operating system, this writes the state the game itself reads.

The chain, read out of the shipped code and confirmed live:

    [0x02EA5368]                 -> the input manager
    manager + 0xDF8              -> the backend                (0017DE10 reads it this way)
    backend + device*8 + 0x118   -> a per-device block, device 0 is the keyboard
    block + 0x30 + (code - 0x1C) -> ONE BYTE PER INPUT, non-zero means "held"

`0079E6A0` is the query every "is it held?" predicate ends in, and it is exactly:

    if device >= 7            -> 0
    if !block                 -> 0
    if (unsigned)(code-0x1C) >= 0x100 -> 0
    return block[0x30 + code-0x1C] != 0

**The codes are the numbers in `GameSetting.ini`'s `[Keyboard1]` section.** Their minimum is 28,
which is exactly the `0x1C` the query subtracts -- so `index = keymap_value - 28`.

Honesty requirements this tool enforces
---------------------------------------
* It **resolves the chain every run**. The per-device block is heap and moves between launches;
  a hardcoded address would write into whatever now lives there.
* It **refuses if the array is not all-zero** unless `--force`, because writing over real held
  input would corrupt the very state being established.
* It **restores** what it wrote, and **verifies** the restore by reading back.
* Every state it produces is **INSTRUMENTATION-INDUCED**, never "naturally reached". Any experiment
  built on it must say so -- charter-directive section 4.
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runtime_probe as RP

MANAGER_PTR = 0x02EA5368
BACKEND_OFF = 0xDF8
DEVICE_TABLE = 0x118
ARRAY_OFF = 0x30
CODE_BIAS = 0x1C
ARRAY_LEN = 0x100

PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008

k32 = ctypes.WinDLL("kernel32", use_last_error=True)

# GameSetting.ini [Keyboard1] -- the names the game itself uses, and the codes it stores.
KEYMAP = {
    "Select": 40, "L3": 79, "R3": 35, "Start": 64, "Up": 36, "Right": 39, "Down": 38,
    "Left": 37, "L2": 55, "R2": 117, "L1": 54, "R1": 56, "Triangle": 45, "Circle": 80,
    "Cross": 30, "Square": 33, "WalkMode": 118,
}


def die(m, code=2):
    sys.stderr.write("runtime_poke: %s\n" % m)
    raise SystemExit(code)


class RW(object):
    def __init__(self, pid):
        self.h = k32.OpenProcess(
            RP.PROCESS_QUERY_INFORMATION | RP.PROCESS_VM_READ
            | PROCESS_VM_WRITE | PROCESS_VM_OPERATION, False, pid)
        if not self.h:
            die("OpenProcess(write) failed for pid %d (error %d). Try an elevated shell."
                % (pid, ctypes.get_last_error()))

    def read(self, va, n):
        buf = (ctypes.c_ubyte * n)()
        got = ctypes.c_size_t(0)
        ok = k32.ReadProcessMemory(self.h, ctypes.c_void_p(va), ctypes.byref(buf),
                                   ctypes.c_size_t(n), ctypes.byref(got))
        return bytes(bytearray(buf)) if ok and got.value == n else None

    def write(self, va, data):
        buf = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
        put = ctypes.c_size_t(0)
        ok = k32.WriteProcessMemory(self.h, ctypes.c_void_p(va), ctypes.byref(buf),
                                    ctypes.c_size_t(len(data)), ctypes.byref(put))
        return bool(ok) and put.value == len(data)

    def q(self, va):
        b = self.read(va, 8)
        return struct.unpack("<Q", b)[0] if b else None

    def close(self):
        k32.CloseHandle(self.h)


def resolve_array(rw):
    """-> (array_va, current_bytes) or die. Resolved fresh: the block is heap and it moves."""
    mgr = rw.q(MANAGER_PTR)
    if not mgr:
        die("the input manager at 0x%08X is NULL -- the game has not built it yet" % MANAGER_PTR)
    backend = rw.q(mgr + BACKEND_OFF)
    if not backend:
        die("the backend at manager+0x%X is NULL" % BACKEND_OFF)
    block = rw.q(backend + DEVICE_TABLE)          # device 0 = keyboard
    if not block:
        die("device 0's block is NULL -- no keyboard device")
    va = block + ARRAY_OFF
    cur = rw.read(va, ARRAY_LEN)
    if cur is None:
        die("the held-array at 0x%X is unreadable" % va)
    return va, cur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--process", default="FFXII_TZA")
    ap.add_argument("--show", action="store_true", help="print the held-array and exit")
    ap.add_argument("--press", help="comma-separated key names, e.g. Cross,Start")
    ap.add_argument("--frames", type=int, default=8,
                    help="how many 16 ms ticks to hold before releasing")
    ap.add_argument("--force", action="store_true",
                    help="write even if something is already held")
    a = ap.parse_args()

    hits = RP.find_process(a.process)
    if not hits:
        die("no %r process is running" % a.process, code=3)
    pid, path = hits[0]
    rw = RW(pid)
    try:
        # the same base control runtime_probe runs, because a wrong base means a wrong everything
        base = RP.module_base(rw.h)
        if base != RP.IMAGE_BASE:
            die("module at 0x%X, not the PE ImageBase 0x%X -- refusing to write"
                % (base or 0, RP.IMAGE_BASE))
        va, cur = resolve_array(rw)
        held = [i for i, c in enumerate(cur) if c]
        print("pid %d  %s" % (pid, path))
        print("held-array at 0x%016X, %d bytes" % (va, ARRAY_LEN))
        print("currently held: %s" % (held if held else "nothing"))
        if a.show or not a.press:
            return 0
        if held and not a.force:
            die("something is already held (%s); refusing to write over real input. --force to "
                "override." % held)

        names = [n.strip() for n in a.press.split(",") if n.strip()]
        idx = []
        for n in names:
            if n not in KEYMAP:
                die("unknown key %r; known: %s" % (n, ", ".join(sorted(KEYMAP))))
            i = KEYMAP[n] - CODE_BIAS
            if not (0 <= i < ARRAY_LEN):
                die("%s maps to index %d, outside the array" % (n, i))
            idx.append((n, i))

        print()
        print("*** WRITING to the game's own input state. This state is INSTRUMENTATION-INDUCED")
        print("*** and must never be reported as naturally reached.")
        for n, i in idx:
            ok = rw.write(va + i, b"\x01")
            print("  press   %-9s index %3d  at 0x%016X  %s"
                  % (n, i, va + i, "ok" if ok else "WRITE FAILED"))
        import time
        time.sleep(a.frames * 0.016)
        for n, i in idx:
            rw.write(va + i, b"\x00")
        back = rw.read(va, ARRAY_LEN)
        restored = back is not None and not any(back[i] for _n, i in idx)
        print("  release  after %d frame(s)   restore verified: %s"
              % (a.frames, "yes" if restored else "NO -- the array is not back to zero"))
        return 0 if restored else 1
    finally:
        rw.close()


if __name__ == "__main__":
    sys.exit(main())
