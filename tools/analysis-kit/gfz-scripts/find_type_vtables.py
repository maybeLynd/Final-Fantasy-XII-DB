#!/usr/bin/env python3
"""Which declared types are POLYMORPHIC, and where is each one's vtable?

WHY. CharacterRenderObject was censused on 2026-09-20 from its vtable - 31 slots, every one of
them proved to take the object in rcx by definition - and that produced an extent correction no
route-seeded census could have reached, because the type is heap-allocated and has no route.
The method should generalise. It does not, from stored data: the store names a vtable for
EXACTLY ONE non-Phyre type, the one that was just done. So the vtables have to be found.

HOW, AND THE RULE IS MECHANICAL. MSVC installs the vtable at the top of the constructor:
`lea rX, [rip -> vtable]` followed by a store of that register to `[this]`, i.e. offset 0 of the
object. The store's own `ctor` column already names the constructor for many types, so this
reads that column, disassembles the body, and looks for exactly that pair.

A SHAPE TEST, ADDED AFTER THE FIRST RUN PRODUCED A FALSE POSITIVE. The first version matched
`lea rX,[rip->T]` followed by any `mov [rY], rX`, and reported ImageAddressArenaRecord's vtable
as 022D7FD0 - which is the ARENA RECORD TABLE in .data, stored into some object's first qword by
the same initialiser. A vtable is not just an address stored at offset 0. So the candidate must
now ALSO look like one: it must live in .rdata, and its first three slots must all be addresses
inside .text. That is the same reasoning disasm_fn.py already applies when it flags a possible
vtable, and it rejects the .data table outright.

WHAT IT REFUSES TO DO. It does not guess. A `lea` of an rdata address that is never stored to
`[this + 0]` is not reported; a store to `[this + 8]` is not a vtable. A type whose ctor column
is prose rather than an address is reported as UNPARSEABLE rather than skipped silently, because
"no vtable found" and "never looked" are different findings - the same distinction this kit's
data_xref_scan enforces with its mandatory control.

THE CONTROL IS CharacterRenderObject: ctor 001F4DA0 must yield vtable 00903B68, which the store
already records independently. If the control fails the sweep is wrong and the output is void.
"""
import collections
import csv
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

KIT = KP.GFZ_SCRIPTS
D = os.path.join(KP.DB, "_types") + os.sep
FN = os.path.join(KP.WORK, "graph", "functions.tsv")

CONTROL_TYPE = "CharacterRenderObject"
CONTROL_VT = 0x00903B68

LEA = re.compile(r"^([0-9A-F]{8})\s+\S+\s+lea (r[a-z0-9]+), \[rip \+ [^\]]+\]\s*;\s*([0-9A-F]{6,8})")
STORE0 = re.compile(r"^([0-9A-F]{8})\s+\S+\s+mov qword ptr \[(r[a-z0-9]+)\], (r[a-z0-9]+)")


def sizes():
    out = {}
    for line in io.open(FN, encoding="utf-8"):
        p = line.rstrip("\r\n").split("\t")
        if len(p) > 2:
            try:
                out[int(p[0], 16)] = int(p[2])
            except ValueError:
                pass
    return out


def load_image():
    sys.path.insert(0, KIT)
    import check_absence_claims as G
    d, base, secs = G.load_pe(G.EXE)
    return d, base, secs


def _read(d, base, secs, va, n):
    for nm, rva, vsz, ptr, rsz in secs:
        lo = base + rva
        if lo <= va < lo + max(vsz, rsz):
            off = ptr + (va - lo)
            return d[off:off + n], nm
    return None, None


def looks_like_vtable(img, va):
    """.rdata, and the first three slots all land in .text. Rejects a .data table outright."""
    import struct
    d, base, secs = img
    raw, sec = _read(d, base, secs, va, 24)
    if raw is None or len(raw) < 24 or sec != ".rdata":
        return False, (sec or "unmapped")
    text = [(base + s[1], base + s[1] + max(s[2], s[4])) for s in secs if s[0] == ".text"][0]
    slots = [struct.unpack_from("<Q", raw, i * 8)[0] for i in range(3)]
    if all(text[0] <= q < text[1] for q in slots):
        return True, sec
    return False, "%s but slots %s not all .text" % (sec, ["%X" % q for q in slots])


def vtable_of(va, n, body_cache):
    """The vtable a constructor installs, or None. `lea rX,[rip->T]` then `mov [rY], rX`."""
    if va not in body_cache:
        body_cache[va] = subprocess.run(
            [sys.executable, "disasm_fn.py", hex(va), str(n)],
            cwd=KIT, capture_output=True, text=True).stdout
    held = {}
    for line in body_cache[va].splitlines():
        line = line.strip()
        m = LEA.match(line)
        if m:
            held[m.group(2)] = int(m.group(3), 16)
            continue
        m = STORE0.match(line)
        if m and m.group(3) in held:
            # a store of a lea'd rdata address to [reg] - the vtable install
            return held[m.group(3)], m.group(1)
    return None


def main():
    sz = sizes()
    cache = {}
    rows = list(csv.DictReader(io.open(D + "types.tsv", encoding="utf-8"), delimiter="\t"))
    fields = collections.defaultdict(int)
    for r in csv.DictReader(io.open(D + "fields.tsv", encoding="utf-8"), delimiter="\t"):
        if "unobserved" in (r.get("name") or "").lower():
            fields[r["type"]] += int(r["size"])

    IMG = load_image()
    found, none, unparse, rejected, declared_none = [], [], [], [], []
    for r in rows:
        if (r.get("category") or "").startswith("22-"):
            continue
        ctor = (r.get("ctor") or "").strip()
        if not ctor:
            continue
        # A COLUMN THAT SAYS "none" IS AN ANSWER, NOT A GAP - and the first version of this tool
        # got that wrong in a way that reached a published draft. `ActorManagerSlot`'s column
        # reads "none - the slot is image storage at 02098E10 and is not constructed.
        # CORRECTED 2026-09-18 (OPUS): this cell held 02098E10, which is the storage address,
        # not a constructor". The bare hex search matched the address INSIDE THE EXPLANATION OF
        # THE CORRECTION and reported the column as naming a bad address, when the column is
        # right and already carries its own correction. A type with no constructor cannot
        # install a vtable, which is a resolved negative and belongs in its own bucket.
        if re.match(r"^\s*(none|no\b|not\b)", ctor, re.I):
            declared_none.append((r["type"], ctor[:60]))
            continue
        # `FUN_003DA400` is an ADDRESS, and the first version did not see it: `\b` does not
        # match inside `FUN_003DA400` because underscore is a word character, so
        # ActorManagerSlotEntry - whose column names TWO real constructors, FUN_003DA400 for
        # the +0x110 array and FUN_003DD230 for the +0x170 array - was filed as "never looked".
        m = (re.search(r"FUN_([0-9A-Fa-f]{6,8})", ctor)
             or re.search(r"\b([0-9A-Fa-f]{6,8})\b", ctor))
        if not m:
            unparse.append((r["type"], ctor[:52]))
            continue
        va = int(m.group(1), 16)
        if va not in sz:
            unparse.append((r["type"], "%s (not a known function)" % m.group(1)))
            continue
        hit = vtable_of(va, sz[va], cache)
        if hit:
            ok_shape, why = looks_like_vtable(IMG, hit[0])
            if ok_shape:
                found.append((fields.get(r["type"], 0), r["type"], r.get("size"),
                              va, hit[0], hit[1]))
            else:
                rejected.append((r["type"], hit[0], why))
        else:
            none.append((r["type"], va))

    ctrl = [f for f in found if f[1] == CONTROL_TYPE]
    ok = bool(ctrl) and ctrl[0][4] == CONTROL_VT
    print("CONTROL %s: expect vtable %08X -> %s"
          % (CONTROL_TYPE, CONTROL_VT,
             ("%08X  PASS" % ctrl[0][4]) if ctrl else "NOT FOUND  FAIL"))
    if not ok:
        print("\ncontrol failed - output void")
        return 2
    print("  control passes - the absences below are meaningful\n")

    print("POLYMORPHIC: constructor installs a vtable (%d)" % len(found))
    print("%-32s %-9s %-9s %-9s %8s" % ("type", "size", "ctor", "vtable", "unobs B"))
    for ub, t, s, va, vt, site in sorted(found, reverse=True):
        print("%-32s %-9s %08X  %08X  %8d" % (t, s, va, vt, ub))
    print("\nNOT polymorphic - ctor read, no vtable install: %d" % len(none))
    print("   " + ", ".join(t for t, _ in none[:14]) + (" ..." if len(none) > 14 else ""))
    print("\nREJECTED by the shape test - stored at offset 0 but NOT a vtable: %d"
          % len(rejected))
    for t, a, why in rejected:
        print("   %-30s %08X  %s" % (t, a, why))
    print("\nctor column DECLARES no constructor - a resolved negative, not a gap: %d"
          % len(declared_none))
    for t, c in declared_none[:8]:
        print("   %-30s %s" % (t, c))
    print("\nctor column not an address (NEVER LOOKED, not 'no vtable'): %d" % len(unparse))
    for t, c in unparse[:10]:
        print("   %-30s %s" % (t, c))


if __name__ == "__main__":
    sys.exit(main() or 0)
