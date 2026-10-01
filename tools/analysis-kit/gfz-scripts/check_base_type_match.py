"""Score a declared type against a candidate BASE type, and say which way the evidence points.

WHY THIS EXISTS, AND WHY IT CHECKS CTYPES. The first version of this test - run inline on the eight
ManagerSub0209BE80_* regions and published in S-02's relationships cell - scored OFFSETS ONLY. It
called ManagerSub0209BE80_00A0 a "partial" match at 4 of 6, and _00A0 is NOT a widget: three of
those four hits are FLOATS sitting where Widget declares POINTERS.

  Eight-byte-aligned fields of ANY type land on eight-byte-aligned pointer slots.

So an offset-only score counts a contradiction as agreement, and it does so most often for
float-heavy structures - exactly the ones that most need telling apart from a pointer header.

THE FIX MADE THE NEGATIVE DECISIVE AND LEFT THE POSITIVE WEAK, which is not what I expected when
writing it. Sweeping the store against `Widget` returns 28 `compatible` against 40 `REFUTED`. Forty
types provably are not widgets; twenty-eight merely have pointer-shaped heads, and
`ItemClassDescriptor` is among them. See `verdict()` - `compatible` is a candidate list and a real
identification needs a second signal this tool cannot supply.

NEITHER LIST IS FILING MATERIAL. The sweep against `Widget` was run and its 40 `REFUTED` rows were
deliberately NOT written into the store: 39 are Phyre middleware, navigation and audio types where
nobody had proposed a widget, and the fortieth - `TextDrawState` - is already TYPE RESOLVED as a
float-headed text state. A negative is worth recording when the base was a LIVE hypothesis for that
type, and worth nothing otherwise. Use this tool to decide where to spend effort, not to generate
rows.

WHAT IT DOES NOT DO. It scores DECLARATIONS, not bytes. A type whose interior is delegated to a
child type has almost no rows of its own left to score and will come back `inconclusive` however
well understood it is - ManagerSub0209BE80_AB30 is the worked case, a known widget with one
scoreable row. `inconclusive` here means "too little is carved to tell", never "no".

    python check_base_type_match.py Widget                 # every type against Widget
    python check_base_type_match.py Widget ManagerSub0209BE80_00A0
    python check_base_type_match.py --self-test
"""
import collections
import io
import os
import sys

STORE = os.environ.get("STORE") or (
    r"C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA")
FIELDS = os.path.join(STORE, "_types", "fields.tsv")

# A pointer slot holds an address. A float never is one, whatever its alignment.
PTRISH = ("*", "u64", "uint64", "void*")
FLOATY = ("float", "f32", "double", "f64")


def _is_ptr(c):
    c = c.strip()
    return c.endswith("*") or c in PTRISH


def _is_float(c):
    c = c.strip()
    return any(c.startswith(f) for f in FLOATY)


def load():
    by = collections.defaultdict(list)
    with io.open(FIELDS, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) < 8:
                continue
            try:
                off = int(f[1], 16)
            except ValueError:
                continue
            by[f[0]].append((off, int(f[2]) if f[2].isdigit() else 0, f[3], f[4]))
    return by


def score(by, base, cand, ceiling=None):
    """Returns (scoreable, hits, contradictions, detail).

    `ceiling` bounds the comparison to the base's own declared extent - beyond it a candidate's
    fields are its own and agreement means nothing.
    """
    bmap = {o: (n, c) for o, _, n, c in by.get(base, ())}
    if not bmap:
        return 0, 0, 0, []
    if ceiling is None:
        ceiling = max(bmap) + 8
    hits = contra = n = 0
    detail = []
    for off, _sz, name, ctype in by.get(cand, ()):
        if off >= ceiling or name.startswith("unobserved"):
            continue
        n += 1
        if off not in bmap:
            continue
        hits += 1
        bname, bctype = bmap[off]
        if _is_ptr(bctype) and _is_float(ctype):
            contra += 1
            detail.append("+0x%03X %s(%s) vs %s %s(%s)"
                          % (off, name, ctype, base, bname, bctype))
    return n, hits, contra, detail


def verdict(n, hits, contra):
    """THE TWO DIRECTIONS ARE NOT EQUALLY STRONG, and the wording says so.

    A FLOAT where the base declares a POINTER is a contradiction no spelling can explain, so
    `REFUTED` is a real negative. A pointer where the base declares a pointer is unremarkable -
    the first 0x30 of `Widget` is six pointers, and ANY pointer-headed struct agrees with that by
    alignment alone. Sweeping the whole store against `Widget` returns 28 `compatible` against 40
    `REFUTED`, and 28 is far too many to be an identification: `ItemClassDescriptor` is in it.

    So `compatible` means "nothing here rules the base out" - a CANDIDATE LIST, not a finding. A
    real identification needs a second signal the layout cannot give: the base's own constructor
    (`002465F0` for `Widget`), a proc or vtable, or a call that passes the object as `this`.
    """
    if contra:
        return "REFUTED"
    if n >= 6 and hits >= n * 0.75:
        return "compatible"
    return "inconclusive"


def report(base, cands=None, ceiling=None):
    by = load()
    if cands is None:
        cands = sorted(t for t in by if t != base)
    print("%-34s %6s %6s %7s  %s" % ("type", "rows", "onMap", "CONTRA", "verdict"))
    out = []
    for c in cands:
        n, h, x, d = score(by, base, c, ceiling)
        if n == 0:
            continue
        v = verdict(n, h, x)
        if v != "inconclusive" or c in (cands if len(cands) < 20 else ()):
            print("%-34s %6d %6d %7d  %s" % (c, n, h, x, v))
            for line in d[:3]:
                print("        contradiction: " + line)
        out.append((c, n, h, x, v))
    return out


def self_test():
    """The four ManagerSub regions the inline version got right, wrong and right again."""
    by = load()
    cases = [
        ("ManagerSub0209BE80_8FA0", "compatible", "13 of 13 offsets, no contradiction"),
        ("ManagerSub0209BE80_57E0", "compatible", "20 of 24, the misses inside Widget's own gap"),
        ("ManagerSub0209BE80_00A0", "REFUTED",
         "the case that broke the offset-only test - floats in pointer slots"),
        ("ManagerSub0209BE80_7EA0", "REFUTED", "two float quads where Widget has six pointers"),
    ]
    bad = 0
    for cand, want, why in cases:
        n, h, x, _ = score(by, "Widget", cand)
        got = verdict(n, h, x)
        ok = got == want
        bad += not ok
        print("%s %-30s want=%-13s got=%-13s  %s"
              % ("ok  " if ok else "FAIL", cand, want, got, why))
    print("self-test: %d case(s), %d failure(s)" % (len(cases), bad))
    return bad


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    report(sys.argv[1], sys.argv[2:] or None)
