#!/usr/bin/env python3
"""Derive the release set from the binary, using the idiom that caught the one known defect.

WHY NOT "FUNCTIONS THAT CALL free". Release in this engine is mostly POOL RETURN, not heap
free. 00245020, the widget release, calls 002448D0 and 00244700, which manipulate the widget
pool at 0208EAC0 / 0208EBC0 / 0208EBC8 and never reach a deallocator. A release set built from
callers of free would miss every widget, which is the family that matters most here.

WHY NOT "ADDRESSES IN dtor CELLS". That was tried on 2026-09-20 and gave 245 addresses, of
which one was a region map mentioned inside a `none -` sentence and another, 002A6190, is a
MESSAGE HANDLER the release path merely passes through. The column names whatever a reader
found useful; it is not a list of releases.

SO USE THE IDIOM. What settled ManagerSub7FB0Record was this shape, at 00296690:

    mov rcx, <R>            ; the object
    call 00273A20           ; body: xor eax,eax / cmp qword ptr [rcx], rax / setne al / ret
    test eax, eax
    je  <skip>
    mov rcx, <R>            ; THE SAME register
    call <F>                ; <F> is a release, by construction

00273A20 asks `is the qword at this address non-null`. A caller that asks that and then hands
the SAME pointer to F is releasing a live object - that is what the question is for. F is
therefore a release without anyone having declared it, and the object is whatever <R> holds.

WHAT THIS IS NOT. It finds releases that use this guard; there will be others. And a `<F>` that
takes the object without freeing it - a reset, say - is indistinguishable here, so the output
is `release candidates` and the count is an upper bound on nothing in particular.

CONTROLS, both required or the output is refused:
  * POSITIVE - 00245020 must be derived, from 0029669F, the call that settled the case.
  * NEGATIVE - 00273A20 itself must never appear as a release.
"""
import collections
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
import disasm_fn as DF  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

GUARD = 0x273A20
CONTROL_POS = "00245020"
WINDOW = 0x30


def main():
    img = DF.Image(DF.DEFAULT_EXE)
    md = Cs(CS_ARCH_X86, CS_MODE_64)

    # every direct call to the null-test helper
    sites = []
    for name, sva, vs, ra, rs in img.secs:
        if not name.startswith(".text"):
            continue
        data, base = img.d[ra:ra + rs], img.base + sva
        for i in range(len(data) - 5):
            if data[i] != 0xE8:
                continue
            rel = struct.unpack_from("<i", data, i + 1)[0]
            if base + i + 5 + rel == GUARD:
                sites.append(base + i)

    rel_set = collections.defaultdict(list)
    for s in sites:
        buf = img.read(s - 8, WINDOW)
        if not buf:
            continue
        ins = list(md.disasm(buf, s - 8))
        # the register handed to the guard, taken from the `mov rcx, R` just before
        src = None
        for x in ins:
            if x.address >= s:
                break
            if x.mnemonic == "mov" and x.op_str.startswith("rcx,") and "[" not in x.op_str:
                src = x.op_str.split(",")[1].strip()
        if not src:
            continue
        # after the call: test/je, then the SAME register into another call
        after = [x for x in ins if x.address > s]
        armed = False
        for n, x in enumerate(after):
            if x.mnemonic == "test" or x.mnemonic.startswith("j"):
                armed = True
                continue
            if x.mnemonic == "mov" and x.op_str.startswith("rcx,") \
                    and x.op_str.split(",")[1].strip() == src:
                nxt = after[n + 1] if n + 1 < len(after) else None
                if nxt is not None and nxt.mnemonic == "call" and armed:
                    t = nxt.op_str.strip()
                    if t.startswith("0x"):
                        f = int(t, 16)
                        if f != GUARD:
                            rel_set["%08X" % f].append("%08X" % nxt.address)
                break
            if x.mnemonic == "call":
                break

    ok_pos = CONTROL_POS in rel_set
    ok_neg = ("%08X" % GUARD) not in rel_set
    print("CONTROL positive  %s derived from the idiom   %s"
          % (CONTROL_POS, "PASS" if ok_pos else "FAIL"))
    print("CONTROL negative  the guard 00273A20 never appears as a release   %s"
          % ("PASS" if ok_neg else "FAIL"))
    if not (ok_pos and ok_neg):
        print("\ncontrols failed - output refused")
        return 2
    print("  controls pass\n")
    print("CALLS TO THE NULL-TEST GUARD 00273A20: %d" % len(sites))
    print("RELEASE CANDIDATES DERIVED FROM THE GUARDED IDIOM: %d\n" % len(rel_set))
    for f in sorted(rel_set, key=lambda k: (-len(rel_set[k]), k)):
        print("   %s   %2d site(s)   %s" % (f, len(rel_set[f]), " ".join(rel_set[f][:6])))
    print("\nEach is a function that receives a pointer the caller has just confirmed non-null")
    print("through 00273A20. That is what the guard is for, so these are releases by the shape")
    print("of their use - not by anyone having declared them. A reset that takes the object the")
    print("same way is indistinguishable here.")


if __name__ == "__main__":
    sys.exit(main() or 0)
