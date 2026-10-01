#!/usr/bin/env python3
"""check_storage_class.py - the ownership half of the type store, checked against the image.

`types_index.py --validate` checks a type's FIELD layout. Nothing checked the columns that say
who allocates a type, who owns it and how it is reached: `allocation_site`, `ctor`, `dtor` and
the `route` grammar added on 2026-09-17. This is that check.

What it measures
----------------
1. **route grammar** - every ` | `-separated alternative parses against the grammar documented in
   `_types/README.md`; an unknown verb is an error.
2. **anchors** - every STATIC/ARRAY/PTR/PARRAY/SLOTPTR base is resolved to its PE section out of
   the shipped image and must land in data; every FN base must land in `.text`. A `.data` address
   past its section's raw data is reported as `.bss`, because such a global starts as zero.
3. **containment** - an `EMBED Parent +0xOFF` whose child span is known must fit inside the
   parent's declared size, and two EMBEDs into the same parent must not overlap. An `EMBED` that
   does not fit is a layout contradiction wherever it sits.
4. **the parent's field map** - an `EMBED`/`CHAIN` at `Parent +0xOFF` should meet a declared field
   row at that offset. A `CHAIN` should meet a POINTER there; a `CHAIN` through an integer field
   is a different ABI (`parent + *(uint32*)(parent+off)`, a relative reference) and is reported.
5. **storage class** - `allocation_site` is classified into IMAGE (a static object in the image),
   INTERIOR (a sub-object of a named parent), CALLER (a buffer the caller supplies), HEAP (a real
   allocation call), POOL (a slot taken from a pre-existing block, whose own class is named
   alongside), RESOURCE (a buffer the resource system owns, the loader's allocation still open),
   MIXED (more than one of those by instance, size or stage) and UNRESOLVED. Rows outside that
   vocabulary are listed, not failed. UNRESOLVED and RESOURCE are counted separately in the
   summary, because "nobody allocates this" and "we have not found who allocates this" are
   different answers and only the second is a question.
6. **the contradiction this file was written for** - a row whose `dtor` says it has no independent
   storage, or whose `allocation_site` is the same address as its `ctor`, cannot also have an
   allocation site. Those rows name a CONSTRUCTOR in the allocation column.
7. **column confusion** - a `ctor`/`dtor` cell whose only address lands outside `.text` is storage
   being recorded as a constructor.

Controls
--------
`--self-test` mutates an in-memory copy of the store and requires each check to fire: an EMBED
pushed past its parent, a STATIC anchor moved into `.text`, an allocation site copied from a ctor.
A check that cannot fail cannot pass, and the run is refused if any control is silent.
"""
import argparse
import bisect
import csv
import os
import re
import struct
import sys

import kit_paths as KP

DB = KP.DB
EXE = os.path.join(KP.WORK, "exe", "FFXII_TZA.exe")
GRAPH = os.path.join(KP.WORK, "graph", "functions.tsv")
PHYRE = "22-Middleware-PhyreEngine"

VERBS = ("STATIC", "ARRAY", "PTR", "PARRAY", "SLOTPTR", "EMBED", "CHAIN", "RELOFF",
         "FN", "DYNAMIC", "VTABLE", "PTABLE", "PKREF")
DATA_VERBS = ("STATIC", "ARRAY", "PTR", "PARRAY", "SLOTPTR")
CLASSES = ("IMAGE", "INTERIOR", "CALLER", "HEAP", "POOL", "RESOURCE", "MIXED",
           "UNRESOLVED")

# A dtor cell that says the type has no storage of its own.
NO_STORAGE = re.compile(
    r"no independent storage|interior to|inline in|storage is in the image|"
    r"interior storage|built on the caller|caller-supplied|no storage of its own|"
    r"it is the save buffer", re.I)

VA_BARE = re.compile(r"\b0[0-2][0-9A-Fa-f]{6}\b")


def load_image(path):
    with open(path, "rb") as fh:
        d = fh.read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
    secs = []
    for i in range(nsec):
        o = pe + 24 + opt + i * 40
        name = d[o:o + 8].rstrip(b"\0").decode(errors="replace")
        vsz, va, rsz, ptr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((name, va, vsz, ptr, rsz))
    return base, secs


def section_of(va, base, secs):
    r = va - base
    for name, sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            if name == ".data" and (r - sva) >= rsz:
                return ".bss"
            return name
    return None


def load_graph(path):
    fns = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        next(fh)
        for line in fh:
            f = line.rstrip("\n").split("\t")
            try:
                fns.append((int(f[0], 16), int(f[2]), f[1]))
            except (ValueError, IndexError):
                pass
    fns.sort()
    return fns


def num(s):
    s = (s or "").strip()
    try:
        return int(s, 16) if s.lower().startswith("0x") else int(s, 10)
    except ValueError:
        return None


def read_store(root):
    with open(os.path.join(root, "types.tsv"), encoding="utf-8", newline="") as fh:
        types = list(csv.DictReader(fh, delimiter="\t"))
    with open(os.path.join(root, "fields.tsv"), encoding="utf-8", newline="") as fh:
        fields = list(csv.DictReader(fh, delimiter="\t"))
    return types, fields


class Report(object):
    def __init__(self):
        self.items = {}

    def add(self, kind, what, why):
        self.items.setdefault(kind, []).append((what, why))

    def count(self, kind):
        return len(self.items.get(kind, []))


def check(types, fields, base, secs, fns, quiet=False):
    rep = Report()
    starts = [f[0] for f in fns]

    def is_text(va):
        return section_of(va, base, secs) == ".text"

    size = {}
    for r in types:
        s = num(r["size"])
        if s is not None:
            size[r["type"]] = s
    known = {r["type"] for r in types}

    byoff = {}
    for f in fields:
        o = num(f["offset"])
        if o is not None:
            byoff.setdefault(f["type"], {})[o] = f

    embeds = {}
    nroutes = 0
    for r in types:
        t = r["type"]
        # THE WRONG SEPARATOR IS SILENT, WHICH IS WHY IT NEEDS A CHECK RATHER THAN A CONVENTION.
        # `PartyReadMachineRecord` joined its two alternatives with a COMMA. The split below is on
        # " | ", so the whole string parsed as ONE alternative, the leading verb and address parsed
        # fine, and everything after the comma - a second real STATIC instance at 02EBF3F0 - was
        # never anchor-checked. Nothing failed; the type simply had half a route. Found 2026-09-18
        # only because the parsed-alternative count was one short of the type count.
        for bad in re.finditer(r",\s*(" + "|".join(VERBS) + r")\b", r["route"] or ""):
            rep.add("SEPARATOR", t,
                    "route joins alternatives with a COMMA before %s; the grammar is ' | ', so "
                    "everything after the comma is invisible to this check" % bad.group(1))

        for alt in (r["route"] or "").split(" | "):
            alt = alt.strip()
            if not alt:
                continue
            nroutes += 1
            verb = alt.split()[0]
            if verb not in VERBS:
                rep.add("GRAMMAR", t, "unknown route verb %r in %r" % (verb, alt))
                continue
            if verb == "PKREF":
                # PKREF 0xFN (Type|0xADDR) +0xOFF - a dword at parent+OFF decoded through
                # the named pack-offset resolver, which is a .text function.
                m = re.match(r"PKREF\s+0x([0-9A-Fa-f]{6,8})\s+(\S+)\s+\+0x([0-9A-Fa-f]+)", alt)
                if not m:
                    rep.add("GRAMMAR", t,
                            "PKREF does not parse as 0xFN (Type|0xADDR) +0xOFF: %r" % alt)
                    continue
                va = int(m.group(1), 16)
                sec = section_of(va, base, secs)
                if sec != ".text":
                    rep.add("ANCHOR", t,
                            "PKREF resolver %08X is in %s, not .text" % (va, sec))
                parent = m.group(2)
                if parent.startswith("0x"):
                    psec = section_of(int(parent, 16), base, secs)
                    if psec == ".text":
                        rep.add("ANCHOR", t, "PKREF parent %s is in .text" % parent)
                elif parent not in known:
                    rep.add("PARENT", t,
                            "PKREF route parent %r is not a declared type" % parent)
                continue
            if verb == "SLOTPTR" and not re.match(r"SLOTPTR\s+0x", alt):
                # Parent-relative table form: SLOTPTR Type +0xOFF ... - same shape as EMBED.
                m = re.match(r"SLOTPTR\s+(\S+)\s+\+0x([0-9A-Fa-f]+)(.*)$", alt)
                if not m:
                    rep.add("GRAMMAR", t,
                            "SLOTPTR does not parse as Type +0xOFF: %r" % alt)
                    continue
                if m.group(1) not in known:
                    rep.add("PARENT", t,
                            "SLOTPTR route parent %r is not a declared type" % m.group(1))
                continue
            if verb in DATA_VERBS or verb in ("FN", "VTABLE", "PTABLE"):
                m = re.search(r"0x([0-9A-Fa-f]{6,8})", alt)
                if not m:
                    rep.add("ANCHOR", t, "%s route with no 0x anchor: %r" % (verb, alt))
                    continue
                va = int(m.group(1), 16)
                sec = section_of(va, base, secs)
                if sec is None:
                    rep.add("ANCHOR", t, "%08X is outside every section (%s)" % (va, verb))
                elif verb == "FN" and sec != ".text":
                    rep.add("ANCHOR", t, "FN base %08X is in %s, not .text" % (va, sec))
                elif verb != "FN" and sec == ".text":
                    rep.add("ANCHOR", t, "%s anchor %08X is in .text" % (verb, va))
            if verb in ("EMBED", "CHAIN", "RELOFF"):
                m = re.match(r"(?:EMBED|CHAIN|RELOFF)\s+(\S+)\s+\+0x([0-9A-Fa-f]+)(.*)$", alt)
                if not m:
                    rep.add("GRAMMAR", t, "%s does not parse as Type +0xOFF: %r" % (verb, alt))
                    continue
                parent, off, tail = m.group(1), int(m.group(2), 16), m.group(3)
                if parent not in known:
                    rep.add("PARENT", t, "route parent %r is not a declared type" % parent)
                    continue
                stride = re.search(r"stride=0x([0-9A-Fa-f]+)", tail)
                count = re.search(r"count=(\S+)", tail)
                fld = byoff.get(parent, {}).get(off)
                span = None
                if stride and count and num(count.group(1)) is not None:
                    span = int(stride.group(1), 16) * num(count.group(1))
                elif size.get(t) is not None:
                    span = size[t]
                elif fld is not None:
                    # SIZED-BY-ARGUMENT child (SWE2-FRONTIER ruling 2026-09-19/20,
                    # OPUS-REQ-FRONTIER-SIZED-WIDGET-NOW-DECIDABLE): Widget has no
                    # sizeof - its size is a construction argument - so an `EMBED`
                    # route for it cannot draw the span from the type's size column.
                    # The extent lives on the PARENT's field row instead: when the
                    # field at this offset spells the child non-pointer (`Widget` or
                    # `Widget[n]`, the same grammar check_ctype_widths governs), that
                    # row's width IS the child's span and containment is checkable.
                    # A `Widget*` field is a pointer to a widget, not one, and never
                    # feeds this rule.
                    fct = (fld["ctype"] or "").strip()
                    fbase = fct.split("[")[0].rstrip("*").strip()
                    if fbase == t and "*" not in fct:
                        span = num(fld["size"])
                psz = size.get(parent)
                if verb == "EMBED":
                    if psz is None or span is None:
                        rep.add("UNCHECKABLE", t,
                                "EMBED %s +0x%X cannot be contained: %s" %
                                (parent, off, "parent size UNRESOLVED" if psz is None
                                 else "child span unknown"))
                    elif off + span > psz:
                        rep.add("OVERRUN", t,
                                "EMBED %s +0x%X spans 0x%X, ending at 0x%X, past %s's declared 0x%X"
                                % (parent, off, span, off + span, parent, psz))
                    else:
                        embeds.setdefault(parent, []).append((t, off, off + span))
                elif psz is not None and off + (8 if verb == "CHAIN" else 4) > psz:
                    rep.add("OVERRUN", t,
                            "%s field %s +0x%X does not fit in %s's declared 0x%X"
                            % (verb, parent, off, parent, psz))
                if fld is None:
                    rep.add("NOFIELD", t,
                            "%s %s +0x%X meets no declared field row at that offset" % (verb, parent, off))
                elif verb == "CHAIN":
                    ct = (fld["ctype"] or "")
                    if "*" not in ct and "ptr" not in ct.lower():
                        rep.add("CHAINABI", t,
                                "CHAIN %s +0x%X but the field there is %r (%s) - a chain through a "
                                "non-pointer is parent + *(intN*)(parent+off), which is RELOFF, a "
                                "different ABI" % (parent, off, fld["name"], ct))
                elif verb == "RELOFF":
                    ct = (fld["ctype"] or "")
                    if "*" in ct or "ptr" in ct.lower():
                        rep.add("CHAINABI", t,
                                "RELOFF %s +0x%X but the field there is %r (%s) - a relative "
                                "reference reads an INTEGER displacement; through a pointer it is "
                                "CHAIN" % (parent, off, fld["name"], ct))

    for parent, kids in embeds.items():
        kids.sort(key=lambda k: k[1])
        for i in range(len(kids) - 1):
            a, b = kids[i], kids[i + 1]
            if a[0] != b[0] and b[1] < a[2]:
                rep.add("OVERLAP", parent,
                        "%s [0x%X,0x%X) overlaps %s [0x%X,0x%X)" % (a[0], a[1], a[2], b[0], b[1], b[2]))

    # ---- ownership columns, game-side only -------------------------------
    game = [r for r in types if r["category"] != PHYRE]
    classes = {}
    for r in game:
        t = r["type"]
        alloc = (r["allocation_site"] or "").strip()
        ctor = (r["ctor"] or "").strip()
        dtor = (r["dtor"] or "").strip()
        head = alloc.split(" ")[0].rstrip(",") if alloc else ""
        if head in CLASSES:
            classes[t] = head
        else:
            classes[t] = None
            rep.add("VOCAB", t, "allocation_site does not open with a storage class: %r" % alloc[:70])

        # A DEREFERENCING ROUTE VERB CONTRADICTS IMAGE STORAGE. PTR/PARRAY/SLOTPTR all mean
        # "read a pointer at ADDR and go there"; IMAGE means "the storage IS at ADDR". A row
        # asserting both is wrong in one column, and the wrong one resolves - PARRAY on an array
        # dereferences the first eight bytes of record 0 and addresses somewhere else without
        # faulting. Three rows carried exactly that until 2026-09-20 (CON-139:
        # NameBindingEntry, NameBindingSubRecord, ScheduledTaskRecord), each contradicting its own
        # allocation_site, and nothing in this checker looked.
        if classes.get(t) == "IMAGE":
            for alt in (r["route"] or "").split(" | "):
                verb = alt.strip().split(" ")[0]
                if verb in ("PTR", "PARRAY", "SLOTPTR"):
                    rep.add("DEREF", t,
                            "storage class IMAGE but the route verb %s dereferences the address "
                            "(%r) - one of the two columns is wrong" % (verb, alt.strip()[:52]))
                    break

        # THE CONVERSE: A FIXED-ADDRESS ROUTE VERB CONTRADICTS HEAP/POOL STORAGE. STATIC and ARRAY
        # mean "the instance is AT this image address"; HEAP and POOL mean it is wherever the
        # allocator put it, which is not knowable at link time. EMBED/CHAIN/RELOFF are exempt -
        # they are parent-relative and a heap object can perfectly well live inside another heap
        # object. Added 2026-09-20 as the inverse of the DEREF check, which found four rows on its
        # first run; running the inverse before assuming it finds none is the whole point.
        if classes.get(t) in ("HEAP", "POOL"):
            for alt in (r["route"] or "").split(" | "):
                verb = alt.strip().split(" ")[0]
                if verb in ("STATIC", "ARRAY"):
                    rep.add("FIXEDHEAP", t,
                            "storage class %s but the route verb %s puts the instance at a fixed "
                            "image address (%r)" % (classes[t], verb, alt.strip()[:52]))
                    break

        # Only a row that CLAIMS an allocation can contradict a dtor that says there is none.
        # A row already classified IMAGE/INTERIOR/CALLER/MIXED/UNRESOLVED cites addresses to
        # locate its storage, not to allocate it, and firing on those is how the first version
        # of this check reported 28 contradictions of which 20 were its own misreading.
        claims_alloc = classes[t] in (None, "HEAP")
        allocva = VA_BARE.findall(alloc)
        if claims_alloc and allocva and NO_STORAGE.search(dtor):
            rep.add("NOTALLOC", t,
                    "allocation_site names %s but dtor says the type has no storage of its own (%r)"
                    % (allocva[0], dtor[:60]))
        elif claims_alloc and allocva and ctor and len(allocva) == 1                 and allocva[0] in VA_BARE.findall(ctor):
            rep.add("SAMEADDR", t,
                    "allocation_site and ctor are the same address %s - confirm the function both "
                    "allocates and constructs, or the allocation column is naming a constructor"
                    % allocva[0])

        for col, label in ((ctor, "ctor"), (dtor, "dtor")):
            vas = VA_BARE.findall(col)
            # A cell that OPENS with "none" is explaining where the storage is, not naming a
            # constructor; firing on those made this check report its own repairs as defects.
            if col.strip().lower().startswith("none"):
                continue
            if vas and not any(is_text(int(v, 16)) for v in vas):
                rep.add("COLUMN", t,
                        "%s cell's only address %s is in %s, not .text - storage recorded as a "
                        "constructor" % (label, vas[0], section_of(int(vas[0], 16), base, secs)))

    return rep, classes, nroutes, len(game)


def emit(rep, classes, nroutes, ngame, types):
    ORDER = [
        ("OVERRUN", "an embedding that does not fit inside its parent"),
        ("OVERLAP", "two embeddings claiming the same bytes of one parent"),
        ("GRAMMAR", "a route that does not parse"),
        ("ANCHOR", "a route anchor in the wrong kind of section"),
        ("PARENT", "a route naming a type the store does not declare"),
        ("NOTALLOC", "an allocation site on a type that has no storage of its own"),
        ("SAMEADDR", "one address in both the allocation and the constructor column"),
        ("COLUMN", "storage recorded in a constructor column"),
        ("CHAINABI", "a chain through a non-pointer field"),
        ("NOFIELD", "an embedding the parent's field map does not declare"),
        ("UNCHECKABLE", "an embedding that cannot be contained yet"),
        ("DEREF", "a dereferencing route verb on IMAGE storage"),
        ("FIXEDHEAP", "a fixed-address route verb on HEAP/POOL storage"),
        ("VOCAB", "an allocation_site outside the storage-class vocabulary"),
    ]
    red = 0
    for kind, gloss in ORDER:
        rows = rep.items.get(kind, [])
        if not rows:
            continue
        hard = kind in ("OVERRUN", "OVERLAP", "GRAMMAR", "ANCHOR", "PARENT")
        red += len(rows) if hard else 0
        print("%s %s - %s (%d)" % ("RED " if hard else "note", kind, gloss, len(rows)))
        for what, why in rows:
            print("    %-34s %s" % (what, why))
        print()

    print("route alternatives parsed: %d" % nroutes)
    counts = {}
    for c in classes.values():
        counts[c or "(none)"] = counts.get(c or "(none)", 0) + 1
    print("game-side types: %d; storage class: %s" %
          (ngame, ", ".join("%s=%d" % kv for kv in sorted(counts.items()))))
    print("hard failures: %d" % red)
    return 1 if red else 0


def self_test(types, fields, base, secs, fns):
    """Each control mutates the store and requires its check to fire."""
    import copy
    ok = True

    def run(mut, kind, label):
        t2 = copy.deepcopy(types)
        f2 = copy.deepcopy(fields)
        mut(t2, f2)
        rep, _, _, _ = check(t2, f2, base, secs, fns, quiet=True)
        fired = rep.count(kind) > rep0.count(kind)
        print("  control %-46s %s" % (label, "FIRES" if fired else "SILENT - CHECK IS BROKEN"))
        return fired

    rep0, _, _, _ = check(types, fields, base, secs, fns, quiet=True)

    def push_embed(t2, f2):
        for r in t2:
            if r["type"] == "WorldLootDropEntry":
                r["route"] = "EMBED WorldLootPickupNode +0x5C stride=0x8 count=7"

    def move_anchor(t2, f2):
        for r in t2:
            if r["type"] == "BattleFormulaScratch":
                r["route"] = "STATIC 0x00266AD0"

    def fake_alloc(t2, f2):
        for r in t2:
            if r["type"] == "BattleTargetEntry":
                r["allocation_site"] = "00316CD0"

    def bad_verb(t2, f2):
        for r in t2:
            if r["type"] == "SpawnGroupLedger":
                r["route"] = "SLAB 0x02EC13C0 stride=0x18"

    print("self-test controls:")
    ok &= run(push_embed, "OVERRUN", "EMBED pushed past its parent's declared size")
    ok &= run(move_anchor, "ANCHOR", "STATIC anchor moved into .text")
    ok &= run(fake_alloc, "NOTALLOC", "allocation site copied onto an interior type")
    ok &= run(bad_verb, "GRAMMAR", "route verb replaced with one the grammar lacks")
    print("  %s" % ("all controls fire" if ok else "AT LEAST ONE CONTROL IS SILENT; refuse the run"))
    return 0 if ok else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=os.path.join(DB, "_types"))
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--funcs", default=GRAPH)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(a.exe):
        print("image missing: %s" % a.exe)
        return 2
    base, secs = load_image(a.exe)
    fns = load_graph(a.funcs) if os.path.exists(a.funcs) else []
    types, fields = read_store(a.store)

    if a.self_test:
        return self_test(types, fields, base, secs, fns)

    rep, classes, nroutes, ngame = check(types, fields, base, secs, fns)
    return emit(rep, classes, nroutes, ngame, types)


if __name__ == "__main__":
    sys.exit(main())
