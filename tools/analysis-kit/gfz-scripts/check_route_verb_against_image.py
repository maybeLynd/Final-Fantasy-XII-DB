"""Verify each route verb against the IMAGE, not against another column.

WHAT THE OTHER CHECKS DO. check_storage_class.py's DEREF and FIXEDHEAP notes compare the `route`
column against the `allocation_site` column. That catches a row contradicting itself, and it found
four (CON-139), but both columns are ASSERTIONS. Two columns agreeing is consistency, not truth.

WHAT THIS DOES. The image itself says whether an address holds records or holds a pointer, by how
code reaches it:

    lea  rax, [ADDR]        takes the ADDRESS OF something -> the storage IS at ADDR
    mov  rax, [ADDR]        READS eight bytes and uses them -> ADDR holds a POINTER

So `PTR`/`PARRAY`/`SLOTPTR` REQUIRE a load: a pointer must be read before it can be followed. The
converse is NOT true and assuming it was is what the first version of this check got wrong - a
static needs no `lea`, because code addresses its fields directly. A `STATIC`/`ARRAY` verb is
therefore supported by ANY reference landing inside [addr, addr+size). A verb with no support of
its own kind is wrong in the route column, whatever the other columns say.

VALIDATED THREE WAYS, because a checker nobody tested is an assertion too. It DISCRIMINATES (the
two controls below), it FIRES (re-injecting the three CON-139 verbs into a copy of the store
reports all three), and it is QUIET on the corrected store (zero).

THE TEST DISCRIMINATES, AND THAT IS CHECKED RATHER THAN ASSUMED. --self-test runs it against two
known answers: SpawnRecord's pool cell 0208E690 (a pointer: 24 loads, no lea) and ActorManagerSlot's
array base 02098E10 (an array: 53 lea). A check that cannot tell those apart is not evidence.

WHAT IT DELIBERATELY DOES NOT CALL A DEFECT:

  * NO REFERENCE AT ALL. An address nothing reaches rip-relative cannot be tested this way; it may
    be reached through a computed base, which no scan of rip-relative operands can see. Reported
    apart, as untestable rather than wrong. RenderModelInstanceContainer's 022C7CD0 is one.
  * A FIXED VERB REACHED ONLY BY LOADS. This was the first rule and it was WRONG. A static does
    not need its address taken: code addresses its fields DIRECTLY. SharedGameplayLcgState is four
    bytes read 17 times as `mov eax, [022C256C]` - that reads its VALUE - and BattleFormulaScratch
    is a 0xA8 block whose 77 loads reach its fields at absolute addresses. Both are correctly
    STATIC and both were flagged until the rule was corrected to: a FIXED verb is supported by ANY
    rip-relative reference landing inside [addr, addr+size), lea or direct. A DEREF verb still
    requires an actual LOAD at the address, because a pointer must be read before it can be
    followed - that is what the three CON-139 rows lacked.

Usage:  python check_route_verb_against_image.py [--store <db>/_types] [--self-test]
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP, disasm_fn as DF, resolve_switch_arms as R
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import capstone.x86 as X

try:
    from regcanon import canon
except ImportError:                                   # regcanon is optional here
    def canon(n):
        return n

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_types"))

ADDR_VERB = re.compile(r"\b(STATIC|ARRAY|PTR|PARRAY|SLOTPTR)\s+(0x[0-9A-Fa-f]+)")
# ARG <reg> 0xFUNC (SWE2STRUCT-REQ-FRONTIER-ARG-ROUTE-RULING-1001) names a FUNCTION,
# not a data address - its check is extent membership, not a rip-relative form.
ARG_VERB = re.compile(r"\bARG\s+(rcx|rdx|r8|r9)\s+(0x[0-9A-Fa-f]+)", re.I)
FIXED = ("STATIC", "ARRAY")
DEREF = ("PTR", "PARRAY", "SLOTPTR")


def reference_forms():
    """address -> Counter({'lea': n, 'load': n}) over every rip-relative operand in the image."""
    md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
    img = DF.Image(KP.EXE)
    ex = R.extents()
    forms = collections.defaultdict(collections.Counter)
    for va, n in sorted(ex.items()):
        if not n or n <= 0:
            continue
        try:
            ins = R.decode(img, md, va, n)
        except BaseException:
            continue
        for i in ins:
            for op in i.operands:
                if op.type == X.X86_OP_MEM and op.mem.base and \
                        canon(i.reg_name(op.mem.base)) == "rip":
                    t = i.address + i.size + op.mem.disp
                    forms[t]["lea" if i.mnemonic == "lea" else "load"] += 1
    return forms


CONTROLS = [
    (0x0208E690, "SpawnRecord pool cell", "load"),
    (0x02098E10, "ActorManagerSlot array base", "lea"),
]


def self_test(forms):
    bad = 0
    for addr, what, expect in CONTROLS:
        c = forms.get(addr, collections.Counter())
        got = "load" if c["load"] > c["lea"] else ("lea" if c["lea"] else "none")
        ok = got == expect
        if not ok:
            bad += 1
        print("%s %-34s %08X  lea=%-3d load=%-3d  dominant=%s (want %s)"
              % ("ok  " if ok else "MISS", what, addr, c["lea"], c["load"], got, expect))
    print("self-test: %d control(s), %d failure(s)" % (len(CONTROLS), bad))
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", default=DEFAULT)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    forms = reference_forms()
    if a.self_test:
        raise SystemExit(1 if self_test(forms) else 0)

    lines = io.open(os.path.join(a.store, "types.tsv"),
                    encoding="utf-8", newline="").read().split("\n")
    H = {n: i for i, n in enumerate(lines[0].split("\t"))}

    extents = R.extents()
    wrong, untestable, ok = [], [], 0
    bad_arg = []
    for ln in lines[1:]:
        f = ln.split("\t")
        if len(f) <= H["route"]:
            continue
        for alt in (f[H["route"]] or "").split(" | "):
            am = ARG_VERB.search(alt)
            if am:
                # A mistyped function address would seed zero hosts silently; the
                # route claims FUNC's entry, so FUNC must be a function start.
                if int(am.group(2), 16) not in extents:
                    bad_arg.append((f[H["type"]], int(am.group(2), 16)))
                else:
                    ok += 1
                continue
            m = ADDR_VERB.search(alt)
            if not m:
                continue
            verb, addr = m.group(1), int(m.group(2), 16)
            c = forms.get(addr)
            if not c:
                untestable.append((f[H["type"]], verb, addr))
                continue
            if verb in FIXED:
                # supported by any reference INSIDE the extent - lea or a direct field access
                size = 0
                try:
                    size = int(f[H["size"]], 16)
                except (ValueError, KeyError):
                    size = 0
                span = max(size, 1)
                supported = any(forms.get(addr + k) for k in range(0, span))
            else:
                supported = c["load"] > 0
            if not supported:
                wrong.append((f[H["type"]], verb, addr, c["lea"], c["load"]))
            else:
                ok += 1

    print("ROUTE VERBS CHECKED AGAINST THE IMAGE\n")
    print("  verb supported by the image        %4d" % ok)
    print("  verb CONTRADICTED by the image     %4d" % len(wrong))
    print("  untestable (no rip-relative ref)   %4d" % len(untestable))
    if bad_arg:
        print("\nARG VERBS NAMING NO FUNCTION:")
        for t, addr in bad_arg:
            print("   %-32s ARG -> %08X is not a function extent" % (t, addr))

    if wrong:
        print("\nCONTRADICTED - the verb has ZERO references of its own kind:")
        for t, verb, addr, l, ld in wrong:
            print("   %-32s %-8s %08X   lea=%-3d load=%-3d  -> should be %s"
                  % (t, verb, addr, l, ld, "PTR/PARRAY/SLOTPTR" if verb in FIXED else "STATIC/ARRAY"))
    if untestable:
        print("\nUNTESTABLE - nothing reaches the address rip-relative; may use a computed base:")
        for t, verb, addr in untestable:
            print("   %-32s %-8s %08X" % (t, verb, addr))


if __name__ == "__main__":
    main()
