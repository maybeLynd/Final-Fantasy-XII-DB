#!/usr/bin/env python3
"""Two types describing the same memory, found by resolving addresses rather than matching them.

`types_index.py` validates fields WITHIN a type - overlaps, gaps, overruns. Nothing checked
types against EACH OTHER, so two entries could describe one object and the store would report
both as clean. Two such cases surfaced in one week, both by accident:

  * `AchievementCounterBlock` and the save page's "image-backed state block" are one object,
    and they disagreed on its size - 0x3848 against 0x4818.
  * `ActorManagerSlot` and `ActorManagerRecord` are one 0x288 object at 02098E10, and neither
    name appeared in the other's home.

TWO RULES, EACH LEARNED FROM A WRONG ANSWER THIS TOOL GAVE.

**Resolve the arithmetic, do not match the literal.** The `instance` column is prose written
for readers: one row says `0x02164480` and another says `SaveImage_GetActiveBuffer() + 0x200`,
and those are one address. A literal scan reported them as different and walked past
`PersistentFlagPayload` sitting wholly inside `SavePayload`.

**A pointer's address is not the object's address.** `*(char**)0x0208E688 + slot * 0xF50` puts
nothing at 0208E688 but a pointer. Reading it as the object start made `BattleUnit` a 0xF50
block that swallowed `SpawnRecord`'s pointer global eight bytes later, and reported two
adjacent pointer variables as an aliased object. When a row dereferences, this resolves the
TARGET - from a stated value, or a named base below - and when it cannot, it says so rather
than falling back to the pointer's own address.

Named bases are declared here, with their evidence, instead of being parsed out of the prose
that states them. Prose is a convention and not a contract - three schema assumptions broke
that way in one week - and a table that is wrong is at least a table somebody can read.

It reports candidates and never renames or merges. Overlap is often legitimate: an interior
region does live inside its container, and the store's way of saying so is a ctype naming the
inner type. What is NOT legitimate is two types describing one object with neither mentioning
the other, which is what a reader trips over.

    check_instance_aliases.py [--verbose]
"""
import io
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", ".."))
TYPES = os.path.join(ROOT, "Database", "FFXII TZA", "_types", "types.tsv")
FIELDS = os.path.join(ROOT, "Database", "FFXII TZA", "_types", "fields.tsv")

# Accessor returns, each with the evidence that fixes it. A name absent here leaves the row
# unresolved and listed as such; it is never guessed from a nearby literal.
NAMED_BASES = {
    # 002EF640 returns the active runtime save buffer. Read at 00233C25: call 0x2ef640,
    # add rax, 0x4e68c, mov [0x02EBF190], rax - and the callee's returned literal is 02164280.
    "SaveImage_GetActiveRuntimeBuffer": 0x02164280,
    "SaveImage_GetActiveBuffer": 0x02164280,
    # payload base = buffer + 0x200, i.e. past SaveImageHeader.
    "SaveImage_GetPersistentPayloadBase": 0x02164480,
}

LO, HI = 0x00100000, 0x30000000
ADDR = re.compile(r"0x([0-9A-Fa-f]{6,8})")
DEREF = re.compile(r"\*\s*\(")
# "NAME() + 0x200" / "NAME(002EF640) + 0x8200"
CALLBASE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^)]*\)\s*\+\s*(0x[0-9A-Fa-f]+|\d+)")
# "0x02164280 + 0x200"
LITPLUS = re.compile(r"0x([0-9A-Fa-f]{6,8})\s*\+\s*(0x[0-9A-Fa-f]+|\d+)")
# "+ slot * 0x250", "+ (group - 1) * 24"
STRIDE = re.compile(r"\*\s*(0x[0-9A-Fa-f]+|\d+)")
COUNT = re.compile(r"(\d+)\s*(?:entries|slots|profiles|nodes|instances|elements)\b")


def val(s):
    return int(s, 16) if s.lower().startswith("0x") else int(s)


def first_literal(s):
    for m in ADDR.finditer(s):
        v = int(m.group(1), 16)
        if LO < v < HI:
            return v
    return None


def resolve(instance):
    """(address, how) for the object's own start, or (None, why-not).

    A dereference is resolved to its target or not at all: the pointer variable's address is
    never used as a fallback, because that is what produced a false alias."""
    s = instance.strip()
    if not s:
        return None, "no instance stated"

    if DEREF.search(s):
        tail = s[s.index("*"):]
        # "*(void**)0x02EBF190 = SaveImage_GetActiveBuffer() + 0x4E68C = 0x021B290C"
        eqs = re.findall(r"=\s*0x([0-9A-Fa-f]{6,8})", tail)
        if eqs:
            v = int(eqs[-1], 16)
            if LO < v < HI:
                return v, "dereference, target stated"
        m = CALLBASE.search(tail)
        if m and m.group(1) in NAMED_BASES:
            return NAMED_BASES[m.group(1)] + val(m.group(2)), "dereference via %s" % m.group(1)
        return None, "dereference, target not stated offline"

    m = CALLBASE.search(s)
    if m and m.group(1) in NAMED_BASES:
        return NAMED_BASES[m.group(1)] + val(m.group(2)), "%s + offset" % m.group(1)
    if m:
        return None, "base %s() not in NAMED_BASES" % m.group(1)

    m = LITPLUS.search(s)
    if m and LO < int(m.group(1), 16) < HI:
        return int(m.group(1), 16) + val(m.group(2)), "literal + offset"

    v = first_literal(s)
    if v is not None:
        return v, "literal"
    return None, "no address in range"


def extent(instance, size):
    """How many bytes the row's instance actually covers. An array of N covers N*stride."""
    c = COUNT.search(instance)
    if not c:
        return size, ""
    n = int(c.group(1))
    st = STRIDE.search(instance)
    stride = val(st.group(1)) if st else size
    if n > 1 and stride >= size:
        return n * stride, " [%d x 0x%X]" % (n, stride)
    return size, ""


def num(s):
    try:
        return val(s)
    except ValueError:
        return 0


def main():
    verbose = "--verbose" in sys.argv
    placed, unplaced, prose = [], [], {}
    for n, line in enumerate(io.open(TYPES, encoding="utf-8")):
        if not n:
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 5:
            continue
        name, size, inst = c[0], num(c[1]), c[3]
        prose[name] = (inst + " " + (c[10] if len(c) > 10 else "")).lower()
        addr, how = resolve(inst)
        if addr is None:
            if ADDR.search(inst):
                unplaced.append((name, how, inst))
            continue
        if not size:
            unplaced.append((name, "no size declared", inst))
            continue
        span, tag = extent(inst, size)
        placed.append((addr, span, name, how, tag))
    placed.sort()

    refs = set()
    for n, line in enumerate(io.open(FIELDS, encoding="utf-8")):
        if not n:
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) > 4:
            base = re.sub(r"\[\s*\d*\s*\]$", "", c[4].strip()).rstrip("*").strip()
            if base:
                refs.add((c[0], base))

    print("TYPES PLACED AT A RESOLVED ADDRESS: %d" % len(placed))
    if verbose:
        for a, sp, nm, how, tag in placed:
            print("    %08X + 0x%-7X %-26s (%s)%s" % (a, sp, nm, how, tag))

    if unplaced:
        print()
        print("STATED AN ADDRESS BUT NOT PLACED: %d  (not compared; not a clean result)" % len(unplaced))
        for nm, why, inst in unplaced:
            print("    %-26s %s" % (nm, why))
            if verbose:
                print("        %s" % inst.strip()[:110])

    found = []
    for i, (a1, s1, n1, _h1, _t1) in enumerate(placed):
        for a2, s2, n2, _h2, _t2 in placed[i + 1:]:
            if a2 >= a1 + s1:
                break
            structural = (n1, n2) in refs or (n2, n1) in refs
            noted = (n2.lower() in prose.get(n1, "")
                     and n1.lower() in prose.get(n2, ""))
            found.append((a1, s1, n1, a2, s2, n2, structural, noted,
                          a1 == a2, a2 + s2 <= a1 + s1))
    print()
    if not found:
        print("OVERLAPS: none. No two placed types occupy the same memory.")
        return 0
    print("OVERLAPPING TYPE RANGES: %d" % len(found))
    for a1, s1, n1, a2, s2, n2, declared, noted, same, nested in found:
        if declared:
            tag = "declared containment"
        elif noted:
            tag = "recorded in prose on both rows, NOT structurally declared"
        elif same:
            tag = "** SAME BASE, NEITHER MENTIONS THE OTHER **"
        elif nested:
            tag = "** NESTED, NEITHER MENTIONS THE OTHER **"
        else:
            tag = "** PARTIAL OVERLAP, NEITHER MENTIONS THE OTHER **"
        print("    %-26s %08X+0x%-7X" % (n1, a1, s1))
        print("    %-26s %08X+0x%-7X  at +0x%X" % (n2, a2, s2, a2 - a1))
        print("      %s" % tag)
    blind = [f for f in found if not f[6] and not f[7]]
    if blind:
        print()
        print("Overlap is often legitimate - an interior region does live inside its container -")
        print("but the store says so with a ctype naming the inner type. Two types describing one")
        print("object with neither mentioning the other is what a reader trips over.")
        return 1
    if any(not f[6] for f in found):
        print()
        print("Every overlap above is recorded in prose on both rows, so no reader is unwarned,")
        print("and none is structurally declared, so no tool can follow it. Prose is the weaker")
        print("of the two and is not a substitute for a ctype.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
