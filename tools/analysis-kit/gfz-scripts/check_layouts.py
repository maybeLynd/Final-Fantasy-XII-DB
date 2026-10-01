#!/usr/bin/env python3
"""check_layouts.py - validate the database's `struct` fences, and emit templates from them.

Why the fence exists
--------------------
The database's layouts were prose: 22 documents, 85 field lines, none machine-readable. That is
fine for a reader and useless for a tool, so every layout now goes in a fenced block whose columns
are fixed:

    ```struct EbpContainer base=file size=0x80
    +0x00  u32       magic       'EBP2'
    +0x10  u32[20]   sectionOff  indexed by section number, 0 = absent
    ```

`base=` names what the offsets are relative to -- `file`, `section`, `payload`, `record`. Chunk
start, payload start, file start and section start are four different origins and mixing them is
the most common way a format sheet goes wrong, so it is required rather than assumed.

What this refuses to do
-----------------------
**It does not name gaps.** A byte range no field covers is reported `UNACCOUNTED`, never filled in
with something plausible. `struct_map.py` was written after that judgement was made by hand twice
and was wrong twice: *leftover space is not evidence of what occupies it.*

**A generated template cannot carry the loader contract.** 010, Kaitai and ImHex all describe what
bytes ARE. None can say a field is read by nothing -- which is section 3 of `FORMAT.md`, the column
a modder actually comes for. The emitted template is a lossy view of the document, never a
replacement, and it says so in its own header.

Usage
-----
    python check_layouts.py --db "Database/FFXII TZA"
    python check_layouts.py --db "Database/FFXII TZA" --emit-bt <outdir>   # 010 Editor templates
    python check_layouts.py --self-test
"""
import argparse
import collections
import io
import os
import re
import sys

FENCE = re.compile(r"^```struct\s+(\w+)([^\n]*)$")
FIELD = re.compile(r"^\+0x([0-9A-Fa-f]+)\s+([A-Za-z_][A-Za-z0-9_]*(?:\[\d*\])?)\s+"
                   r"([A-Za-z_][A-Za-z0-9_]*)\s*(.*)$")
KV = re.compile(r"(\w+)=(\S+)")
# `+0x03  ...  count entries of 3 bytes` - a tail whose length is known only at read time.
TAIL = re.compile(r"^\+0x([0-9A-Fa-f]+)\s+\.\.\.\s*(.*)$")

SCALARS = {"u8": 1, "i8": 1, "u16": 2, "i16": 2, "u32": 4, "i32": 4,
           "u64": 8, "i64": 8, "f32": 4, "f64": 8, "char": 1, "byte": 1}
# BIG-ENDIAN FORMS, added 2026-09-16 (OPUS). The PS2 image sheets - as7, btm, cl2 and their
# siblings - are big-endian containers, and `u16be`/`u32be` is how they say so. The width is
# identical to the little-endian form; the suffix records BYTE ORDER, which is precisely the thing
# this fence exists to stop a reader assuming. FORMAT.md's own argument for `base=` applies
# unchanged: chunk start and file start are two origins and mixing them is how a format sheet goes
# wrong, and so is reading a big-endian count little-endian. Rejecting the notation did not make
# the corpus little-endian, it just made five real fences unparseable.
SCALARS.update({k + "be": v for k, v in list(SCALARS.items())
                if k not in ("u8", "i8", "char", "byte")})
BT = {"u8": "uchar", "i8": "char", "u16": "ushort", "i16": "short",
      "u32": "uint", "i32": "int", "u64": "uint64", "i64": "int64",
      "f32": "float", "f64": "double", "char": "char", "byte": "uchar"}
# A 010 template expresses endianness with BigEndian()/LittleEndian() rather than in the type name,
# so the emitted type is the same and the ORDER is lost in that view. The template header already
# says it is a lossy view of the document; this is one more thing it cannot carry.
BT.update({k + "be": v for k, v in list(BT.items()) if k not in ("u8", "i8", "char", "byte")})
# `_templates` holds EXAMPLE fences - `StructName` in SYSTEM.md and a specimen
# `EbpContainer` in FORMAT.md. Scanning them counted two documentation samples as
# recovered layouts and printed UNACCOUNTED warnings about a template's placeholder
# offsets, which is noise that teaches the reader to skip the real ones.
SKIP_DIRS = ("_inbox", "_templates")


def parse_type(t):
    """'u32[20]' -> ('u32', 20, 80); returns None for an unknown scalar."""
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)(?:\[(\d*)\])?$", t)
    if not m:
        return None
    # An UNSIZED array - `u32be[]` - is a TYPED TAIL: a run whose element type is known and whose
    # length is not, because it is `count` elements and `count` is a field. The fence already had
    # an untyped tail (`+0x08  ...  count x ...`); this is the same statement carrying more, and
    # discarding it because the count is absent would lose the element width the sheet does know.
    # Width None says "no fixed end here", and the caller stops gap arithmetic exactly as it does
    # for `...`.
    if m.group(2) == "":
        return (m.group(1), None, None) if m.group(1) in SCALARS else None
    base, n = m.group(1), int(m.group(2)) if m.group(2) else 1
    if base not in SCALARS:
        return None
    return base, n, SCALARS[base] * n


def parse_fences(text):
    """-> [{name, opts, fields:[(off,type,name,comment)], line}]"""
    out = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        name, rest = m.group(1), m.group(2)
        opts = dict(KV.findall(rest))
        fields, j = [], i + 1
        while j < len(lines) and not lines[j].startswith("```"):
            ln = lines[j].strip()
            if ln and not ln.startswith("#"):
                fm = FIELD.match(ln)
                tm = TAIL.match(ln)
                if fm:
                    fields.append((int(fm.group(1), 16), fm.group(2), fm.group(3),
                                   fm.group(4).strip()))
                elif tm:
                    # A VARIABLE-LENGTH TAIL, which is a real thing a struct can have and which
                    # this parser used to call unparseable. `MusicCtrlRun` ends
                    #     +0x03  ...   count entries of 3 bytes
                    # because the run's length is 3*count, known only at read time. Recording it
                    # as an error said the document was malformed when it was being precise.
                    fields.append(("TAIL", int(tm.group(1), 16), "", tm.group(2).strip()))
                elif fields and fields[-1][0] not in ("BAD",) and not ln.startswith("+0x"):
                    # A WRAPPED DESCRIPTION, not a field. `AdmGroup`'s field00 comment runs onto a
                    # second indented line, and matching each line independently made the
                    # continuation an unparseable field. A line inside a struct fence that does
                    # not begin with an offset is part of the description above it.
                    p = fields[-1]
                    fields[-1] = (p[0], p[1], p[2], (p[3] + " " + ln).strip())
                else:
                    fields.append(("BAD", ln, "", ""))
            j += 1
        out.append({"name": name, "opts": opts, "fields": fields, "line": i + 1})
        i = j + 1
    return out


def validate(st):
    """-> (errors, unaccounted_ranges)"""
    errs, seen, prev_end, gaps, computed = [], {}, None, [], []
    if "base" not in st["opts"]:
        errs.append("no base= (file/section/payload/record) - offsets have no stated origin")
    open_tail = False
    for f in st["fields"]:
        if f[0] == "BAD":
            errs.append("unparseable field line: %s" % f[1][:60])
            continue
        if f[0] == "TAIL":
            # From here the structure has no fixed end, so there is nothing to compute a gap
            # against and a declared size cannot be checked. Recorded, not counted.
            open_tail = True
            if prev_end is not None and f[1] > prev_end:
                gaps.append((prev_end, f[1]))
            prev_end = None
            continue
        off, ty, nm, _c = f
        pt = parse_type(ty)
        if not pt:
            errs.append("+0x%X %s: unknown type" % (off, ty))
            continue
        _b, _n, width = pt
        if width is None:
            # A typed tail. Same consequence as `...`: no fixed end, so no gap against it and a
            # declared size cannot be checked past this point.
            open_tail = True
            if prev_end is not None and off > prev_end:
                gaps.append((prev_end, off))
            seen[nm] = off
            prev_end = None
            continue
        if nm in seen:
            errs.append("+0x%X: duplicate field name '%s' (also +0x%X)" % (off, nm, seen[nm]))
        seen[nm] = off
        if prev_end is not None:
            if off < prev_end:
                errs.append("+0x%X %s overlaps the field ending at +0x%X" % (off, nm, prev_end))
            elif off > prev_end:
                gaps.append((prev_end, off))
        prev_end = off + width
    size = st["opts"].get("size")
    if size:
        try:
            total = int(size, 16) if size.lower().startswith("0x") else int(size)
            if prev_end is not None and prev_end > total:
                errs.append("fields run to +0x%X, past the declared size=%s" % (prev_end, size))
            elif prev_end is not None and prev_end < total:
                gaps.append((prev_end, total))
        except ValueError:
            # `size=count*4` is a size the sheet cannot state as a constant because it depends on
            # a field. That is a fact about the format, not an error in the fence, and refusing it
            # pushes an author toward writing a WRONG constant. It is recorded and the size-based
            # checks are skipped - and SAID, because a check silently not run is the failure this
            # kit keeps finding.
            computed.append((st["name"], size))
    return errs, gaps, computed


def scan(db):
    found = []
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, db).replace(os.sep, "/")
            for st in parse_fences(io.open(p, encoding="utf-8", errors="replace").read()):
                st["doc"] = rel
                found.append(st)
    return found


def emit_bt(st):
    """One 010 Editor template. Lossy by construction - it cannot carry the loader contract."""
    L = ["// %s - generated from %s by check_layouts.py" % (st["name"], st.get("doc", "?")),
         "// GENERATED - do not edit. Regenerate from the document.",
         "// This shows what the bytes ARE. It cannot show what the engine REJECTS, CLAMPS or",
         "// IGNORES - that is section 3 of the source document, and no template format carries it.",
         "typedef struct {"]
    for f in st["fields"]:
        if f[0] == "BAD":
            continue
        off, ty, nm, c = f
        pt = parse_type(ty)
        if not pt:
            continue
        base, n, _w = pt
        arr = "[%d]" % n if n > 1 else ""
        cm = ("  // +0x%X%s" % (off, "  " + c if c else ""))
        L.append("    %-8s %s%s;%s" % (BT[base], nm, arr, cm))
    L.append("} %s;" % st["name"])
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--emit-bt", metavar="OUTDIR")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.db:
        return ap.error("--db or --self-test required")

    sts = scan(a.db)
    print("STRUCT FENCE VALIDATION")
    print("  %d struct fence(s) in %d document(s), %d field(s)"
          % (len(sts), len({s["doc"] for s in sts}), sum(len(s["fields"]) for s in sts)))
    rc = 0
    total_gap = 0
    all_computed = []
    for st in sts:
        errs, gaps, computed = validate(st)
        all_computed.extend(computed)
        total_gap += sum(b - a2 for a2, b in gaps)
        if errs or gaps:
            print("\n  %s  (%s:%d)" % (st["name"], st["doc"], st["line"]))
        for e in errs:
            rc = 1
            print("    ERROR    %s" % e)
        for a2, b in gaps:
            print("    UNACCOUNTED  +0x%X .. +0x%X  (%d bytes)" % (a2, b, b - a2))
    if all_computed:
        # SAID, NEVER SILENT. A computed size means the size check and the trailing-gap check
        # did NOT run for that fence. A check quietly not run is the failure this kit keeps
        # finding, so the fences it applies to are named.
        print("\n  COMPUTED SIZE - the declared size depends on a field, so the size check")
        print("  and the trailing-gap check did NOT run for these. A fact about the format,")
        print("  not a defect:")
        for nm, expr in all_computed:
            print("      %-28s size=%s" % (nm, expr))
    if total_gap:
        print("\n  %d unaccounted byte(s) total. **A gap is a question, never a label** - do not"
              "\n  fill one with a plausible name." % total_gap)

    # One name, two shapes. Nothing checked this before, and it found three on the
    # first run: Ff12Ar03Header declared at both 0x30 and 0x40, and Cml1Entry with
    # +0x004 as i32 in one document and u32 in another. A layout recorded twice and
    # differently is worse than one recorded once, because each page looks settled.
    dup = collections.defaultdict(list)
    for st in sts:
        dup[st["name"]].append(st)
    clashes = 0
    for name in sorted(dup):
        group = dup[name]
        if len(group) < 2:
            continue
        shapes = {tuple((o, t, n) for o, t, n, _ in g["fields"]) for g in group}
        sizes = {g["opts"].get("size") for g in group}
        if len(shapes) == 1 and len(sizes) == 1:
            continue
        clashes += 1
        rc = 1
        print("")
        print("  SAME NAME, DIFFERENT LAYOUT: %s" % name)
        for g in group:
            print("    %s:%d  size=%s  %d field(s)"
                  % (g["doc"], g["line"], g["opts"].get("size", "none"), len(g["fields"])))
        first = group[0]
        for g in group[1:]:
            # Only integer offsets sort together -- TAIL/BAD sentinel rows are already
            # reported by the per-struct validation above, and mixing them into the
            # key set crashed the sort on the first real duplicate-name clash.
            fa = {o: (t, n) for o, t, n, _ in first["fields"] if isinstance(o, int)}
            fb = {o: (t, n) for o, t, n, _ in g["fields"] if isinstance(o, int)}
            for off in sorted(set(fa) | set(fb)):
                if fa.get(off) != fb.get(off):
                    print("      +0x%03X  %-20s vs  %s"
                          % (off,
                             ("%s %s" % fa[off]) if off in fa else "(absent)",
                             ("%s %s" % fb[off]) if off in fb else "(absent)"))
    if clashes:
        print("")
        print("  %d name(s) declared with more than one layout. Each belongs to the page that"
              % clashes)
        print("  wrote it; reconcile or rename, but two pages cannot both be right.")

    if not sts:
        print("\n  No struct fences yet. Layouts written as free prose are not machine-readable"
              "\n  and will have to be re-extracted by hand; see _templates/FORMAT.md section 2.")

    if a.emit_bt:
        if not os.path.isdir(a.emit_bt):
            os.makedirs(a.emit_bt)
        n = 0
        for st in sts:
            if validate(st)[0]:
                continue                     # never emit from a struct that does not validate
            io.open(os.path.join(a.emit_bt, "%s.bt" % st["name"]), "w",
                    encoding="utf-8", newline="\n").write(emit_bt(st))
            n += 1
        print("\n  emitted %d 010 Editor template(s) to %s" % (n, a.emit_bt))
        print("  Lossy by construction: a template cannot carry the loader contract.")
    return rc


SELF = """
```struct Good base=file size=0x1C
+0x00  u32       magic     'EBP2'
+0x04  u32[4]    table     ok
+0x14  byte[8]   tail      ok
```

```struct Gappy base=record size=0x10
+0x00  u32   a   ok
+0x08  u32   b   leaves 0x04..0x08 unaccounted
```

```struct Bad
+0x00  u99   weird   unknown type
+0x00  u32   a       overlaps
+0x00  u32   a       duplicate name
```
"""


def self_test():
    sts = parse_fences(SELF)
    ok = True
    if len(sts) != 3:
        print("SELF-TEST FAILED: parsed %d fences" % len(sts)); ok = False
    good, gappy, bad = sts
    e, g, _c = validate(good)
    if e or g:
        print("SELF-TEST FAILED: clean struct reported %s %s" % (e, g)); ok = False
    e, g, _c = validate(gappy)
    if g != [(4, 8), (12, 16)]:
        print("SELF-TEST FAILED: gaps %s" % g); ok = False
    e, _, _c = validate(bad)
    if not any("unknown type" in x for x in e):
        print("SELF-TEST FAILED: unknown type not caught"); ok = False
    if not any("overlap" in x for x in e):
        print("SELF-TEST FAILED: overlap not caught"); ok = False
    if not any("duplicate" in x for x in e):
        print("SELF-TEST FAILED: duplicate name not caught"); ok = False
    if not any("no base=" in x for x in e):
        print("SELF-TEST FAILED: missing base= not caught"); ok = False
    if "uint     table[4];" not in emit_bt(good):
        print("SELF-TEST FAILED: array emit\n%s" % emit_bt(good)); ok = False

    # THE THREE FORMS ADDED 2026-09-16, each tested in the direction that would be a defect.
    be = parse_type("u32be")
    if be != ("u32be", 1, 4):
        print("SELF-TEST FAILED: u32be -> %s, want a 4-byte scalar" % (be,)); ok = False
    if parse_type("u8be") is not None:
        print("SELF-TEST FAILED: u8be should not exist - a byte has no byte order"); ok = False
    if parse_type("u37be") is not None:
        print("SELF-TEST FAILED: the be suffix must not admit an unknown base"); ok = False
    # An unsized array is a TYPED TAIL: known element, unknown length.
    ua = parse_type("u32be[]")
    if ua != ("u32be", None, None):
        print("SELF-TEST FAILED: u32be[] -> %s, want a typed tail" % (ua,)); ok = False
    if parse_type("nope[]") is not None:
        print("SELF-TEST FAILED: an unsized array of an unknown base must still fail"); ok = False
    # ... and it must STOP the gap arithmetic, not silently extend it.
    tail_st = parse_fences(
        "```struct T base=file size=0x20\n"
        "+0x00  u32be    count   how many\n"
        "+0x04  u32be[]  offs    count entries\n"
        "```\n")[0]
    te, tg, _tc = validate(tail_st)
    if te or tg:
        print("SELF-TEST FAILED: a typed tail reported %s %s - it must open the tail, so there"
              " is no gap to the declared size" % (te, tg)); ok = False
    # A computed size is recorded, not an error, and the fence is NAMED so the skip is visible.
    cs = parse_fences("```struct C base=file size=count*4\n+0x00  u32be  n  count\n```\n")[0]
    ce, _cg, cc = validate(cs)
    if ce:
        print("SELF-TEST FAILED: size=count*4 reported %s - it is a fact, not a defect" % ce)
        ok = False
    if cc != [("C", "count*4")]:
        print("SELF-TEST FAILED: computed size not recorded: %s" % (cc,)); ok = False
    if not ok:
        return 1
    print("self-test ok: gaps reported and not named, big-endian scalars, typed tails and computed sizes, unknown type / overlap / duplicate name / "
          "missing base= all caught, arrays emit correctly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
