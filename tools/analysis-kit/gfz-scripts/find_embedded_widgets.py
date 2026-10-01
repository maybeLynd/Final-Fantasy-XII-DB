#!/usr/bin/env python3
"""Which types are Widgets, or contain one, and at what offset?

WHY. On 2026-09-20 a 632-byte `unobserved` span inside ManagerSub0209BE80_8FA0 turned out to be
a Widget, and following that up showed the containing type IS one too. Both were found by hand.
Nothing in the kit would have found either, and there was no reason to think they were the only
ones.

THE TEST IS A RELATIONSHIP, NOT A SHAPE, and that took two failed attempts to arrive at.

  * ATTEMPT 1 - Widget's `flags` at +0x40 plus any five of its declared offsets at a common
    base. Its NEGATIVE CONTROL refused it immediately: ImageAddressArenaRecord, 0xA8 bytes with
    no widget within reach, reported bases at +0x30 and +0x60. Of course it did - Widget's
    +0x10/+0x18/+0x20/+0x28 are four consecutive qwords, and every densely censused 8-aligned
    object has four consecutive qwords somewhere.
  * ATTEMPT 2 - require +0x40 and +0x7C and two of Widget's distinctive far fields. Controls
    passed, and it still reported 25 artifacts including battle-formula-scratch at BOTH +0x0
    and +0x4. Two bases four bytes apart is not two widgets; it is a dense artifact matching
    anything.

  * WHAT WORKS: Widget's constructor and destructor are NAMED ON WIDGET'S OWN TYPE ROW -
    002465F0 and 00244F00. An object either of them operates on is a Widget, because that is
    what a constructor is. No thresholds, no tuning, and the answer is a declared relationship
    rather than a coincidence of spacing.

A CAUTION THIS FILE EXISTS TO CARRY. The note first written when _8FA0 +0xAC0 was identified said
"the accessors are the widget family". That basis was ADDRESS PROXIMITY - the functions sit near
00245000 - and it is worth nothing: NONE of those seven functions calls a widget constructor,
allocator or destructor. This store already records a neighbourhood pass over 108 bodies whose
every hit was worthless. The real corroboration was present all along and is what this tool
uses.

CONTROLS, both required or the output is refused:
  * POSITIVE - ManagerSub0209BE80_8FA0 must report base 0 (its ctor) and +0xAC0 (the dtor).
  * POSITIVE - ManagerSub0209BE80_57E0 must report THREE ctor bases: 0, 0xD0, 0x1A0.
  * NEGATIVE - ImageAddressArenaRecord must report nothing at all.

COUNTING INSTANCES, and v3 got this wrong in a way worth recording. v3 reported the MINIMUM
displacement per function as "the" base, so a type holding several widgets reported one and the
rest vanished silently - a false negative that looks like a clean answer. ManagerSub0209BE80_57E0
holds THREE and was reported as one.

The fix needs no threshold, because the census already carries the answer. ONE INSTRUCTION
REACHED AT N DISPLACEMENTS IS N INSTANCES: site 00246641 is a single `mov qword ptr [rdi], rbx`
writing the proc at +0x00, and it appears in 57E0's artifact at 0x0, 0xD0 AND 0x1A0. The
constructor did not move; the object did. So the instance bases are the displacement set OF THE
ONE SITE THAT PRODUCES THE LOWEST DISPLACEMENT - no tuning, no pattern matching, and it degrades
to the old answer when there is genuinely one instance.
"""
import csv
import glob
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

D = os.path.join(KP.DB, "_types") + os.sep
WIDGET_FN = {"002465F0": "Widget ctor", "00244F00": "Widget dtor"}
CONTROL_POS = "manager-sub-0209be80-8fa0-accesses.tsv"
CONTROL_MULTI = "manager-sub-0209be80-57e0-accesses.tsv"
CONTROL_NEG = "image-address-arena-record-accesses.tsv"


def scan():
    """basename -> {base offset: {which widget function touched it}}"""
    out = {}
    for p in glob.glob(os.path.join(KP.DB, "**", "*-accesses.tsv"), recursive=True):
        lines = [l for l in io.open(p, encoding="utf-8") if not l.startswith("#")]
        if not lines:
            continue
        try:
            rows = list(csv.DictReader(lines, delimiter="\t"))
        except Exception:
            continue
        if not rows or "disp" not in rows[0] or "function" not in rows[0]:
            continue
        hits = {}
        for r in rows:
            fn = (r.get("function") or "").strip().upper()
            if fn not in WIDGET_FN:
                continue
            try:
                d = int(r["disp"], 16)
            except (ValueError, TypeError):
                continue
            hits.setdefault(fn, {}).setdefault((r.get("site") or "").strip(), set()).add(d)
        if hits:
            out[os.path.basename(p)] = hits
    return out


def bases(hits):
    """fn -> sorted instance bases, one per object that function was reached on.

    The instruction producing the lowest displacement is touching the first instance's lowest
    field. EVERY displacement that same instruction is recorded at is another instance of the
    same object, because one instruction cannot reach two offsets of one object. So that site's
    own displacement set IS the set of bases.

    Reported per function rather than merged: a type can both BE a widget (ctor base 0) and
    CONTAIN one (dtor at a non-zero base), which ManagerSub0209BE80_8FA0 does.
    """
    out = {}
    for fn, sites in hits.items():
        lo_site = min(sites, key=lambda s: (min(sites[s]), s))
        out[fn] = sorted(sites[lo_site])
    return out


def main():
    found = scan()
    def show(b, fn):
        return ", ".join("0x%X" % o for o in b[fn]) if fn in b else "none"

    pos_b = bases(found.get(CONTROL_POS, {}))
    mul_b = bases(found.get(CONTROL_MULTI, {}))
    ok_pos = pos_b.get("002465F0") == [0] and pos_b.get("00244F00") == [0xAC0]
    ok_mul = mul_b.get("002465F0") == [0, 0xD0, 0x1A0]
    ok_neg = CONTROL_NEG not in found
    print("CONTROL positive  %s -> ctor base %s, dtor base %s  %s"
          % (CONTROL_POS, show(pos_b, "002465F0"), show(pos_b, "00244F00"),
             "PASS" if ok_pos else "FAIL"))
    print("CONTROL multiple  %s -> ctor bases %s  %s"
          % (CONTROL_MULTI, show(mul_b, "002465F0"), "PASS" if ok_mul else "FAIL"))
    print("CONTROL negative  %s -> %s  %s"
          % (CONTROL_NEG, "nothing" if ok_neg else "reported", "PASS" if ok_neg else "FAIL"))
    if not (ok_pos and ok_mul and ok_neg):
        print("\ncontrols failed - output refused")
        return 2
    print("  both controls pass - the absences below are meaningful\n")

    print("ARTIFACTS WIDGET'S OWN CTOR OR DTOR TOUCHES: %d" % len(found))
    for name in sorted(found):
        b = bases(found[name])
        parts = []
        for fn, offs in sorted(b.items(), key=lambda kv: kv[1]):
            embedded = [o for o in offs if o]
            what = []
            if 0 in offs:
                what.append("IS a Widget")
            if embedded:
                what.append("contains %d at %s"
                            % (len(embedded), ", ".join("+0x%X" % o for o in embedded)))
            parts.append("%s -> %s" % (WIDGET_FN[fn], " and ".join(what)))
        print("  %-52s %s" % (name[:52], "; ".join(parts)))
    print("\nA base of 0 from the CONSTRUCTOR means the type itself is a Widget. A non-zero base")
    print("means an embedded one. Both can be true of the same type.")


if __name__ == "__main__":
    sys.exit(main() or 0)
