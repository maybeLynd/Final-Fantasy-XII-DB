#!/usr/bin/env python3
"""find_setter_by_extent.py - which function's reach fits a type, and when that is worth anything.

THE IDEA, and it is a weak one used carefully. A function that initialises an object writes its
last field, so its largest displacement off the incoming pointer sits just under the object's
size. Run that backwards: given a type's declared size, the functions whose maximum displacement
lands just below it are candidates for being its initialiser.

WHY THIS IS NOT ENOUGH ON ITS OWN, stated first because the tool's whole value is in the refusal.
`EVIDENCE-STANDARD` addendum bz requires a tie that is positive AND EXCLUSIVE. A tight fit is a
property of the FUNCTION'S REACH, not a claim about its type:

  * a setter that leaves the last field alone shows more slack and is still the right function;
  * two classes of the same size are indistinguishable by it;
  * and a function operating on something else entirely can land in the window by accident.

So this reports a CANDIDATE LIST and a margin, and it reports nothing else.

AN EARLIER VERSION OF THIS PARAGRAPH SAID "one candidate with a large margin to the next class is
worth acting on". THAT IS REFUTED, by this tool's own output, and the refutation is the most
useful thing it has produced:

    PersistentFlagPayload  0x1538 : ONE candidate, 0027DED0, slack 16, and THE NEXT CLASS 4,488
                                    BYTES FURTHER OUT. As convincing as this test ever gets.
                                    It is wrong. 0027DED0 never calls either save getter, its
                                    globals belong to another subsystem, and its ONLY caller is
                                    BattleMenu_UpdateCommandSelectionAndDispatch, which does not
                                    fetch the save buffer either. It operates on a battle-menu
                                    object that happens to be about 0x1538 bytes.

> **Uniqueness in the extent window is not exclusivity in bz's sense.** A single candidate with a
> huge margin is still only a statement about one function's reach. THE EXTENT TEST PROPOSES; a
> thunk, a correct-width write to a registered member, or an independent record disposes.

Every attribution made from this tool so far carries a non-extent signal as well:
PDeferredLightingBase by width (the `+0x41D0` bool written as one byte), PMeshParticleSystemBase
and PMotionBlurBase by the Phyre initialiser thunk, ManagerSingleton0209BE80 by the store's own
`ctor` cell naming 00291750 already. Where no such signal exists - ManagerSub0209BE80_7FB0's
00178170, and PersistentFlagPayload above - nothing is attributed.

WHAT IT MEASURED WHEN IT WAS WRITTEN.

  PDeferredLightingBase  0x41D8 : one candidate 006458A0, max +0x41D0, slack 8, next class 352
                                  away. INDEPENDENTLY CONFIRMED by width - it writes the +0x41D0
                                  bool as ONE BYTE - so this row is the control, not a result.
  PMeshParticleSystemBase 0x3248: one candidate 00645F30, max +0x323C, slack 12, NEXT CLASS 3,996
                                  AWAY. Acted on.
  PMotionBlurBase        0xD68  : NINETEEN candidates under a general window. (An earlier note
                                  here said TWO - that was an artefact of a narrower filter that
                                  also required a write to the one registered member, and it
                                  overstated how well the extent test does.) Attributed anyway,
                                  but NOT on the extent: exactly one of the nineteen carries the
                                  Phyre thunk, and that same function writes m_velocityScale at
                                  +0xD10 as a 4-byte float. Two non-extent signals agreeing.

A SECOND, INDEPENDENT SIGNAL the Phyre classes carry: the initialiser is reached through a
44-byte thunk of the form `if (rdx) setter(rdx); return true;`. Where one exists it is reported,
because it corroborates a candidate without being derived from the extent.

usage: find_setter_by_extent.py --type <name> [--window 0x40] [--min-accesses 6]
       find_setter_by_extent.py --all-unknown [--min-span 512]
"""
import argparse
import collections
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

import capstone  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86
SAVED = {X.X86_REG_RBX, X.X86_REG_RBP, X.X86_REG_RDI, X.X86_REG_RSI,
         X.X86_REG_R12, X.X86_REG_R13, X.X86_REG_R14, X.X86_REG_R15}

CONTROLS = [("PDeferredLightingBase", 0x006458A0),
            ("PMeshParticleSystemBase", 0x00645F30)]


def load():
    d, base, secs = G.load_pe(G.EXE)
    sizes, names = {}, {}
    f = io.open(G.FUNCS, encoding="utf-8", errors="replace")
    f.readline()
    for line in f:
        p = line.split("\t")
        try:
            sizes[int(p[0], 16)] = int(p[2])
            names[int(p[0], 16)] = p[1]
        except (ValueError, IndexError):
            pass
    return d, base, secs, sizes, names


class Img(object):
    def __init__(self):
        self.d, self.base, self.secs, self.sizes, self.names = load()
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
        self.md.detail = True
        self._reach = None

    def blob(self, va, n):
        r = va - self.base
        for nm, sva, vs, ra, rs in self.secs:
            if nm == ".text" and sva <= r < sva + max(vs, rs):
                o = r - sva
                if o < rs:
                    return self.d[ra + o: ra + o + n]
        return None

    def reach(self):
        """max displacement and access count off the incoming RCX, for every function."""
        if self._reach is not None:
            return self._reach
        out = {}
        for e, n in self.sizes.items():
            if n <= 0 or n > 0x8000:
                continue
            b = self.blob(e, n)
            if not b:
                continue
            held = {X.X86_REG_RCX}
            mx, cnt = -1, 0
            for i in self.md.disasm(b, e):
                for o in i.operands:
                    if (o.type == X86_OP_MEM and o.value.mem.base in held
                            and not o.value.mem.index):
                        mx = max(mx, o.value.mem.disp)
                        cnt += 1
                if (i.mnemonic == "mov" and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_REG
                        and i.operands[1].type == X86_OP_REG
                        and i.operands[1].reg in held):
                    held.add(i.operands[0].reg)
                    continue
                try:
                    _r, w = i.regs_access()
                except capstone.CsError:
                    w = []
                for r in w:
                    held.discard(r)
                if i.mnemonic == "call":
                    held = {x for x in held if x in SAVED}
            if mx >= 0:
                out[e] = (mx, cnt)
        self._reach = out
        return out

    def thunk_for(self, setter):
        """a <=64-byte `if (rdx) setter(rdx)` wrapper, if one exists"""
        for e, n in self.sizes.items():
            if n <= 0 or n > 64:
                continue
            b = self.blob(e, n)
            if not b:
                continue
            mov, calls = False, []
            for i in self.md.disasm(b, e):
                if (i.mnemonic == "mov" and len(i.operands) == 2
                        and i.operands[0].type == X86_OP_REG
                        and i.operands[0].reg == X.X86_REG_RCX
                        and i.operands[1].type == X86_OP_REG
                        and i.operands[1].reg == X.X86_REG_RDX):
                    mov = True
                if i.mnemonic == "call":
                    if i.operands and i.operands[0].type == X86_OP_IMM:
                        calls.append(i.operands[0].imm)
                    else:
                        calls.append(None)
            if mov and calls == [setter]:
                return e
        return None


def type_sizes(db):
    rows = list(csv.reader(io.open(os.path.join(db, "_types", "types.tsv"),
                                   encoding="utf-8", newline=""), delimiter="\t"))
    out = {}
    for r in rows[1:]:
        if r and len(r) > 1 and r[1].lower().startswith("0x"):
            try:
                out[r[0]] = int(r[1], 16)
            except ValueError:
                pass
    return out


def candidates(img, size, window, minacc):
    lo = size - window
    return sorted(((e, mx, cnt) for e, (mx, cnt) in img.reach().items()
                   if lo <= mx < size and cnt >= minacc),
                  key=lambda t: -t[1])


def report(img, name, size, sizes, window, minacc, verbose=True):
    cands = candidates(img, size, window, minacc)
    others = sorted(s - max((c[1] for c in cands), default=0)
                    for t, s in sizes.items() if t != name and s > max((c[1] for c in cands), default=0))
    margin = None
    if cands:
        mx = max(c[1] for c in cands)
        above = sorted(s for t, s in sizes.items() if s > mx and t != name)
        margin = (above[0] - size) if above else None
    if verbose:
        print("%-42s size 0x%-6X  candidates %d" % (name, size, len(cands)))
        for e, mx, cnt in cands:
            th = img.thunk_for(e)
            print("     %08X %-24s max +0x%-6X slack %-4d accesses %-4d %s"
                  % (e, img.names.get(e, ""), mx, size - mx, cnt,
                     ("thunk %08X" % th) if th else "no thunk"))
        if len(cands) == 1 and margin is not None:
            print("     the next class above this reach is %d bytes further out" % margin)
            print("     ONE CANDIDATE IS NOT A TIE. PersistentFlagPayload had one candidate with a")
            print("     4,488-byte margin and it was the wrong function. Confirm with a thunk, a")
            print("     correct-width write to a registered member, or an independent record.")
        if len(cands) != 1:
            print("     NOT ACTIONABLE - %s" % ("no candidate" if not cands
                                                else "%d candidates; under bz a narrowed list is still a list" % len(cands)))
    return cands


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type")
    ap.add_argument("--all-unknown", action="store_true")
    ap.add_argument("--min-span", type=int, default=512)
    ap.add_argument("--window", type=lambda s: int(s, 0), default=0x40)
    ap.add_argument("--min-accesses", type=int, default=6)
    ap.add_argument("--db", default=G.DB)
    a = ap.parse_args()

    img = Img()
    sizes = type_sizes(a.db)

    # CONTROLS
    ok = True
    for cname, expect in CONTROLS:
        if cname not in sizes:
            print("CONTROL %-40s type absent from the store  FAIL" % cname)
            ok = False
            continue
        cs = candidates(img, sizes[cname], a.window, a.min_accesses)
        got = [e for e, _m, _c in cs]
        hit = got == [expect]
        print("CONTROL %-40s expect exactly [%08X]  got %-28s %s"
              % (cname, expect, "[" + ", ".join("%08X" % g for g in got) + "]",
                 "PASS" if hit else "FAIL"))
        ok = ok and hit
    print()
    if not ok:
        print("A CONTROL FAILED -> discard the output. The window or the reach tracker has moved")
        print("and the tool has not shown it can recover a setter whose class is already known.")
        return 2

    if a.type:
        if a.type not in sizes:
            print("no sized type named %r" % a.type)
            return 2
        report(img, a.type, sizes[a.type], sizes, a.window, a.min_accesses)
        return 0

    if a.all_unknown:
        # types whose largest UNKNOWN span is at least --min-span
        rows = list(csv.reader(io.open(os.path.join(a.db, "_types", "fields.tsv"),
                                       encoding="utf-8", newline=""), delimiter="\t"))
        worst = collections.Counter()
        for r in rows[1:]:
            if len(r) >= 9 and (r[7] == "UNKNOWN" or "unobserved" in r[3].lower()):
                worst[r[0]] = max(worst[r[0]], int(r[2]))
        actionable = 0
        for t, span in worst.most_common():
            if span < a.min_span or t not in sizes:
                continue
            cs = report(img, t, sizes[t], sizes, a.window, a.min_accesses)
            if len(cs) == 1:
                actionable += 1
            print()
        print("types with exactly one candidate: %d" % actionable)
    return 0


if __name__ == "__main__":
    sys.exit(main())
