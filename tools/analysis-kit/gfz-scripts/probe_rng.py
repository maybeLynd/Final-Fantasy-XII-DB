# -*- coding: utf-8 -*-
"""Run 003A6E60 -- the bounded draw behind every authored spread -- from the shipped bytes.

It is a LEAF, so it emulates in isolation with no stubs at all. That makes the claims in
`02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md`
re-runnable rather than a one-off measurement.

Two disciplines are built in, because both caught real errors while this was being written:

  * **Every configuration is classified LIVE or DEAD by its own positive control.** The shipped
    globals make *every* bound return 0, so a sweep run against them reports "negative bounds return
    0" -- which is the dead instrument talking, not the function. A negative from a DEAD
    configuration is refused rather than reported.

  * **Writes are RECORDED with a hook, never guessed.** Watching the two globals the body reads
    would have missed four of the five addresses it actually writes.

    python probe_rng.py              # all sections
    python probe_rng.py --self-test  # assert every documented claim, exit non-zero on regression
"""
import argparse
import collections
import importlib.util
import os
import struct
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("disasm_fn", os.path.join(_HERE, "disasm_fn.py"))
_D = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_D)

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UcError, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RSP, UC_X86_REG_RIP

FUNC, FLEN = 0x003A6E60, 345
GATE = 0x022D9138          # read, never written -- gates whether STATE is updated
STATE = 0x01EF93E8         # written twice per call; ships as 3F800000 (1.0f)
ONEF = 0x01CEBBA8          # 1.0f in .rdata
STACK, RETM = 0x40000000, 0x50000000
STACK_LEN = 0x10000

# A seed pair that makes the generator live. Any non-zero pair does; these are the ones the
# document's tables were produced with, so its numbers reproduce exactly.
LIVE_SEED = (0x0123456789ABCDEF, 0xDEADBEEF)


class Draw(object):
    """One emulated generator: its own memory, its own recorded writes."""

    def __init__(self, img, gate=None, state=None):
        self.img = img
        self.writes = []
        self._bss = set()
        uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self._mapped = set()
        self.uc = uc
        self._map(FUNC, FLEN)
        uc.mem_write(FUNC, img.read(FUNC, FLEN))
        for va in (GATE, STATE, ONEF):
            self._map(va, 0x40)
            # Bounded by SizeOfRawData, never the virtual range: past it the loader zeroes, and
            # reading the file would hand back whatever follows on disk.
            page = img.read(va & ~0xFFF, 0x1000)
            if page is not None:
                uc.mem_write(va & ~0xFFF, page)
            else:
                self._bss.add(va)
        self._map(STACK, STACK_LEN)
        self._map(RETM, 1)
        uc.mem_write(RETM, b"\xF4")          # HLT: the return sentinel
        if gate is not None:
            uc.mem_write(GATE, struct.pack("<Q", gate))
        if state is not None:
            uc.mem_write(STATE, struct.pack("<I", state))
        uc.hook_add(UC_HOOK_MEM_WRITE, self._on_write)

    def _map(self, va, n):
        for p in range(va & ~0xFFF, ((va + n - 1) & ~0xFFF) + 0x1000, 0x1000):
            if p not in self._mapped:
                self.uc.mem_map(p, 0x1000)
                self._mapped.add(p)

    def _on_write(self, uc, access, address, size, value, ud):
        if not (STACK <= address < STACK + STACK_LEN):     # the emulator's own stack is not state
            self.writes.append((address, size, value))

    def __call__(self, bound):
        rsp = STACK + 0x8000
        self.uc.mem_write(rsp, struct.pack("<Q", RETM))
        self.uc.reg_write(UC_X86_REG_RSP, rsp)
        self.uc.reg_write(UC_X86_REG_RCX, bound & 0xFFFFFFFF)
        try:
            self.uc.emu_start(FUNC, RETM, count=500000)
        except UcError as e:
            raise RuntimeError("fault at %08X: %s" % (self.uc.reg_read(UC_X86_REG_RIP), e))
        v = self.uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
        return v - 0x100000000 if v >= 0x80000000 else v

    @property
    def bss(self):
        return self._bss

    def written(self):
        return collections.Counter(a for a, _, _ in self.writes)


def is_live(img, gate, state, n=20):
    """The positive control for one configuration: does bound 100 actually vary?

    A configuration that fails this is DEAD, and no negative result from it means anything."""
    d = Draw(img, gate, state)
    return len(set(d(100) for _ in range(n))) > 1


def trunc0(x):
    return int(x) if x >= 0 else -int(-x)


PREDICT_BOUNDS = (2, 3, 7, 8, 10, 100, 1000, 65536, 0x40000000, -2, -10, -50, -1000)


def check_scaling(img, n=60):
    """f(bound) == trunc-toward-zero(u * bound)? Recover u from the widest bound, predict the rest.

    Returns (exact, total, mismatches)."""
    wide = 0x7FFFFFFF
    d = Draw(img, *LIVE_SEED)
    u = [d(wide) / float(wide) for _ in range(n)]
    exact = total = 0
    bad = []
    for b in PREDICT_BOUNDS:
        d = Draw(img, *LIVE_SEED)
        for i in range(n):
            got, pred = d(b), trunc0(u[i] * b)
            total += 1
            if got == pred:
                exact += 1
            else:
                bad.append((b, i, got, pred))
    return exact, total, bad, u


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--exe", default=_D.DEFAULT_EXE)
    ap.add_argument("--self-test", action="store_true",
                    help="assert every documented claim; exit non-zero on regression")
    a = ap.parse_args()
    img = _D.Image(a.exe)
    fail = []

    def claim(ok, what):
        print("   %s  %s" % ("ok  " if ok else "FAIL", what))
        if not ok:
            fail.append(what)

    # ---------------------------------------------------------------- shipped image
    print("SHIPPED IMAGE")
    d = Draw(img)
    print("   past SizeOfRawData (BSS, zero at load): %s"
          % (", ".join("%08X" % v for v in sorted(d.bss)) or "none"))
    print("   [%08X] ships as %08X" % (STATE, struct.unpack("<I", img.read(STATE, 4))[0]))
    shipped = [d(100) for _ in range(6)]
    print("   unseeded, bound 100: %s" % shipped)
    claim(GATE in d.bss, "%08X is BSS -- the image ships no gate value" % GATE)
    claim(set(shipped) == {0}, "with the shipped globals every bound returns 0 (inert)")

    # ---------------------------------------------------------------- controls
    print()
    print("CONFIGURATIONS, each judged by its OWN positive control")
    configs = [("shipped", None, None),
               ("gate only", LIVE_SEED[0], None),
               ("state only", None, LIVE_SEED[1]),
               ("both", LIVE_SEED[0], LIVE_SEED[1])]
    live = []
    for name, g, st in configs:
        ok = is_live(img, g, st)
        print("   %-12s %s" % (name, "LIVE (varies)" if ok else "DEAD (flat) -- negatives refused"))
        if ok:
            live.append((g, st))
    claim(len(live) == 1 and live[0] == LIVE_SEED,
          "only a configuration with BOTH globals non-zero is live")

    # ---------------------------------------------------------------- writes
    print()
    print("WRITES PER CALL, recorded with a hook")
    d = Draw(img, *LIVE_SEED)
    for _ in range(20):
        d(100)
    w = d.written()
    for addr in sorted(w):
        print("   %08X   %.1f per call" % (addr, w[addr] / 20.0))
    claim(GATE not in w, "%08X is read and NEVER written -- it gates, it is not state" % GATE)
    claim(w.get(STATE, 0) == 40, "%08X is written twice per call" % STATE)

    # ---------------------------------------------------------------- the scaling law
    print()
    print("SCALING LAW   f(bound) = trunc-toward-zero(u * bound)")
    exact, total, bad, u = check_scaling(img)
    print("   u recovered from bound 0x7FFFFFFF: %s" % ["%.6f" % x for x in u[:6]])
    print("   u over %d draws: min %.4f  max %.4f  mean %.4f" % (len(u), min(u), max(u),
                                                                 sum(u) / len(u)))
    print("   predictions exact: %d / %d across %d bounds" % (exact, total, len(PREDICT_BOUNDS)))
    if bad:
        print("   MISMATCHES: %s" % bad[:5])
    claim(exact == total, "the scaling law predicts every bound exactly")

    # ---------------------------------------------------------------- the sign rule
    print()
    print("SIGN RULE   the result carries the bound's sign and stays strictly inside it")
    for b in (100, -50, -1000, 0):
        d = Draw(img, *LIVE_SEED)
        outs = [d(b) for _ in range(6)]
        print("   bound %-7d -> %s" % (b, outs))
    ok = True
    for b in (2, 8, 100, 1000, -2, -50, -1000):
        d = Draw(img, *LIVE_SEED)
        for _ in range(300):
            v = d(b)
            if b > 0 and not (0 <= v < b):
                ok = False
            if b < 0 and not (b < v <= 0):
                ok = False
    claim(ok, "300 draws x 7 bounds all lie strictly inside the bound, sign included")
    d = Draw(img, *LIVE_SEED)
    claim(set(d(0) for _ in range(6)) == {0}, "f(0) == 0, no fault")

    # ---------------------------------------------------------------- draw count matters
    print()
    print("DRAW COUNT   one extra call shifts the whole sequence by one")
    x, y = Draw(img, *LIVE_SEED), Draw(img, *LIVE_SEED)
    y(50)
    wo = [x(50) for _ in range(8)]
    wi = [y(50) for _ in range(8)]
    print("   without: %s" % wo)
    print("   with   : %s" % wi)
    claim(wo[1:] == wi[:-1], "the sequence shifts by exactly one position")

    # ---------------------------------------------------------------- rough spread
    print()
    print("ROUGH SPREAD, with its denominator")
    d = Draw(img, *LIVE_SEED)
    n = 6000
    c = collections.Counter(d(8) for _ in range(n))
    even = n / 8.0
    dev = 100.0 * max(max(c.values()) - even, even - min(c.values())) / even
    print("   bound 8, %d draws: %s" % (n, dict(sorted(c.items()))))
    print("   even split %.0f, observed %d..%d, worst deviation %.1f %%"
          % (even, min(c.values()), max(c.values()), dev))
    print("   (evidence of ROUGHLY even -- this is not a distribution test)")
    claim(set(c) == set(range(8)), "every value in [0,8) is produced and none outside it")

    print()
    if fail:
        print("FAILED %d claim(s):" % len(fail))
        for f in fail:
            print("   - %s" % f)
        return 1
    print("all claims hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
