#!/usr/bin/env python3
"""types_index.py - validate and query the reconstructed type store.

Why a store, and why TSV
------------------------
Charter section 8 makes type recovery a completion dimension: a reconstruction cannot operate on
anonymous offsets. But 680 offset literals were scattered through prose, never collected, so
"field-resolution coverage" could not be computed at all - `program_coverage.py` printed UNMEASURED.

The store is two TSVs under `Database/FFXII TZA/_types/`:

    types.tsv    one row per type   - size, instance, allocation site, ctor/dtor, readiness
    fields.tsv   one row per field  - type, offset, size, name, ctype, meaning, readiness, evidence

TSV because the existing corpus already uses it (`phyre_schema.tsv`), it diffs cleanly in Git, and
it needs no migration of the prose. Charter section 3's rule stands: do not migrate merely because
another architecture would also work.

The rule this store exists to enforce
-------------------------------------
**The physical offset is never replaced by the semantic name - it accompanies it.** A field whose
meaning is unknown is written with `name = UNRESOLVED` and its offset and size intact. That is the
charter section 8 progression made mechanical:

    +0x1A8  ->  int32 at +0x1A8  ->  changes on a lifecycle transition  ->  generation candidate
            ->  cross-referenced / runtime validated  ->  Actor::generation

Every rung keeps the offset. Deleting it to make the record look finished is the failure mode.

What validation catches
-----------------------
* a field that overruns its type's declared size
* two fields that overlap
* declared-byte gaps - reported, not hidden, because an undeclared span is unrecovered layout
* a readiness rung that is not on the charter's ladder
* a confidence label that is not on the charter's list

Usage
-----
    types_index.py --validate
    types_index.py --type GameSettingConfig      layout with gaps marked
    types_index.py --coverage
    types_index.py --coverage --out FILE
"""
import argparse
import collections
import io
import os
import sys

READINESS = ["DISCOVERED", "CLASSIFIED", "SEMANTICALLY IDENTIFIED", "SIGNATURE RESOLVED",
             "TYPE RESOLVED", "DEPENDENCIES RESOLVED", "BEHAVIORALLY UNDERSTOOD",
             "RUNTIME VALIDATED", "CONTRACT READY", "RECONSTRUCTION READY", "IMPLEMENTED",
             "DIFFERENTIAL TESTED", "PARITY CERTIFIED"]
CONFIDENCE = ["PROVEN", "VERY HIGH", "HIGH", "PROBABLE", "HYPOTHESIS", "UNKNOWN",
              "CONTRADICTED", "SUPERSEDED"]
LEVELS = ["L1", "L2", "L3"]


def die(m):
    sys.stderr.write("types_index: %s\n" % m)
    raise SystemExit(2)


def find_store(explicit):
    if explicit:
        return explicit
    here = os.path.dirname(os.path.abspath(__file__))
    root = here
    for _ in range(8):
        cand = os.path.join(root, "Database", "FFXII TZA", "_types")
        if os.path.isdir(cand):
            return cand
        root = os.path.dirname(root)
    die("could not locate Database/FFXII TZA/_types above %s (pass --store)" % here)


def read_tsv(path):
    if not os.path.exists(path):
        die("missing %s" % path)
    with io.open(path, encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        out = []
        for ln in fh:
            if not ln.strip():
                continue
            p = ln.rstrip("\n").split("\t")
            out.append(dict(zip(head, p + [""] * (len(head) - len(p)))))
    return out


def num(x):
    """A size or offset, or 0 when it is honestly unknown.

    `UNRESOLVED` is a legal value in this store - the charter says preserving `unresolved` is
    always correct - and a numeric parser that crashes on it makes recording an unknown size
    impossible. Callers must therefore treat 0 as "no declared size" and skip the checks that
    depend on one, which `validate` does.
    """
    x = (x or "").strip()
    if not x or not (x[0].isdigit() or x[0] == "-"):
        return 0
    try:
        return int(x, 16) if x.lower().startswith("0x") else int(x)
    except ValueError:
        return 0


NOT_CLAIMED_MARKERS = ("MEANING NOT CLAIMED", "MEANING WITHDRAWN", "SEMANTICS OPEN", "NOTHING NAMES THESE BYTES")
NOT_CLAIMED_PREFIXES = ("declared gap span", "UNRESOLVED")


def meaning_stated(cell):
    """The meaning axis, kept apart from access and representation (2026-09-25, OPUS). A row states a meaning unless its
    meaning cell is empty, carries an explicit not-claimed / withdrawn / open marker, or is a declared gap span. LEXICAL:
    an upper bound that detects contradictions, never a verification that a stated meaning is true."""
    t = (cell or "").strip()
    if not t or t.startswith(NOT_CLAIMED_PREFIXES):
        return False
    up = t.upper()
    return not any(m in up for m in NOT_CLAIMED_MARKERS)


def load(store):
    types = {t["type"]: t for t in read_tsv(os.path.join(store, "types.tsv"))}
    fields = collections.defaultdict(list)
    for f in read_tsv(os.path.join(store, "fields.tsv")):
        fields[f["type"]].append(f)
    for k in fields:
        fields[k].sort(key=lambda f: num(f["offset"]))
    return types, fields


def validate(types, fields):
    errs, warns = [], []
    for tn, t in types.items():
        size = num(t["size"])
        if t["readiness"] not in READINESS:
            errs.append("%s: readiness %r not on the ladder" % (tn, t["readiness"]))
        if t["confidence"] not in CONFIDENCE:
            errs.append("%s: confidence %r not on the list" % (tn, t["confidence"]))
        if t.get("level") and t["level"] not in LEVELS:
            errs.append("%s: level %r is not L1/L2/L3" % (tn, t["level"]))
        # A type recovered from a SAMPLE of its members - reflection registrations, say - has
        # gaps by construction, and reporting each one as a finding buries the real gaps in a
        # type whose layout is supposed to be complete. The declared readiness says which is
        # which: below TYPE RESOLVED, gaps are expected and are not warned about.
        # ...but a DECLARED SIZE overrides that. Readiness alone conflated two different things:
        # "we only sampled this type" and "we know its exact extent and half of it is unread".
        # AudioParameterRamp is SIGNATURE RESOLVED because half its 48 bytes have no reader - yet
        # the 0x30 stride is PROVEN, so its gaps are real findings and must stay visible. A type
        # that declares a numeric size has a known extent; its gaps are reported whatever its
        # readiness says.
        partial = (t["readiness"] in ("DISCOVERED", "CLASSIFIED", "SEMANTICALLY IDENTIFIED",
                                      "SIGNATURE RESOLVED")
                   and not size)
        prev_end, prev_name = 0, None
        for f in fields.get(tn, []):
            off, fs = num(f["offset"]), num(f["size"])
            if f["readiness"] not in READINESS:
                errs.append("%s%s: readiness %r not on the ladder" % (tn, f["offset"], f["readiness"]))
            if f["confidence"] not in CONFIDENCE:
                errs.append("%s%s: confidence %r not on the list" % (tn, f["offset"], f["confidence"]))
            if size and off + fs > size:
                errs.append("%s %s (%s, %d B) overruns declared size 0x%X"
                            % (tn, f["offset"], f["name"], fs, size))
            if off < prev_end:
                # A tagged union is declared with the OVERLAY marker: the overlapping row's
                # `meaning` opens with `OVERLAY ` (the tag lives in its own field). Without the
                # marker an overlap is an error; with it the union is the declared layout.
                # 2026-09-21 (SWE2-STRUCT, OPUS-REQ-...-CANNOT-DECLARE-A-UNION).
                if not f["meaning"].startswith("OVERLAY "):
                    errs.append("%s %s (%s) overlaps the previous field %s"
                                % (tn, f["offset"], f["name"], prev_name))
            elif off > prev_end and not partial:
                warns.append("%s: undeclared gap 0x%03X..0x%03X (%d bytes) before %s"
                             % (tn, prev_end, off, off - prev_end, f["name"]))
            prev_end, prev_name = max(prev_end, off + fs), f["name"]
        if size and prev_end < size:
            warns.append("%s: undeclared tail 0x%03X..0x%03X (%d bytes)"
                         % (tn, prev_end, size, size - prev_end))
    for tn in fields:
        if tn not in types:
            errs.append("fields.tsv references unknown type %r" % tn)
    return errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--type")
    ap.add_argument("--coverage", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    store = find_store(a.store)
    types, fields = load(store)

    if a.type:
        t = types.get(a.type) or die("unknown type %r" % a.type)
        size = num(t["size"])
        print("%s  size %s  instance %s  ctor %s  [%s / %s / %s]"
              % (t["type"], t["size"], t["instance"], t["ctor"],
                 t["readiness"], t["confidence"], t.get("level", "-")))
        print()
        print("%-8s %5s  %-22s %-14s %-11s %s" %
              ("offset", "size", "name", "ctype", "readiness", "meaning"))
        prev = 0
        for f in fields[a.type]:
            off, fs = num(f["offset"]), num(f["size"])
            if off > prev:
                print("%-8s %5d  %s" % ("0x%03X" % prev, off - prev,
                                        "*** UNDECLARED GAP ***"))
            print("%-8s %5d  %-22s %-14s %-11s %s"
                  % (f["offset"], fs, f["name"], f["ctype"], f["readiness"], f["meaning"][:70]))
            prev = max(prev, off + fs)
        if size and prev < size:
            print("%-8s %5d  %s" % ("0x%03X" % prev, size - prev, "*** UNDECLARED TAIL ***"))
        return 0

    errs, warns = validate(types, fields)
    if a.validate or not a.coverage:
        for e in errs:
            print("ERROR  %s" % e)
        for w in warns:
            print("gap    %s" % w)
        # The meaning axis (2026-09-25, OPUS; _types/README.md "three axes"): a row at SEMANTICALLY IDENTIFIED whose meaning
        # cell states no purpose, or withdraws / declines part of it, is listed FOR REVIEW. It is not an error: the rule is
        # lexical, and a row that names its purpose while declining one sub-part is legitimately flagged. It never judges truth.
        review = ["%s %s %s" % (tn, f["offset"], f["name"]) for tn, fl in sorted(fields.items()) for f in fl
                  if f.get("readiness") == "SEMANTICALLY IDENTIFIED" and not meaning_stated(f.get("meaning", ""))]
        for rv in review:
            print("review %s: SEMANTICALLY IDENTIFIED with no (or a partly declined) stated meaning" % rv)
        print()
        print("%d type(s), %d field(s), %d error(s), %d gap(s), %d meaning-rung review(s)"
              % (len(types), sum(len(v) for v in fields.values()), len(errs), len(warns), len(review)))
        if not a.coverage:
            return 1 if errs else 0

    L = []
    w = L.append
    w("# Type reconstruction coverage — charter §8")
    w("")
    w("*Generated by `Database/Tools/analysis-kit/gfz-scripts/types_index.py --coverage`. "
      "Regenerate it; do not quote from memory.*")
    w("")
    w("> **The physical offset is never replaced by the semantic name — it accompanies it.** A field "
      "whose meaning is unknown is recorded as `UNRESOLVED` with its offset and size intact, so an "
      "unrecovered field is *visible* rather than absent. Undeclared spans are reported as gaps for "
      "the same reason.")
    w("")
    w("> **Three axes, counted apart (2026-09-25, OPUS; `_types/README.md` \"Access, representation and meaning are "
      "three axes\").** *named* counts rows with any name other than `UNRESOLVED` - a placeholder such as "
      "`unobservedSpan1538` counts, so it measures REPRESENTATION labelling, never understanding. *meaning stated* "
      "counts rows whose meaning cell states something other than an explicit not-claimed / withdrawn / open "
      "marker or a declared gap span. It is a LEXICAL upper bound that detects contradictions (for example a "
      "`TYPE RESOLVED` row with no stated meaning); it does not verify that any stated meaning is true, which "
      "stays an independent review. Readiness never implies meaning.")
    w("")
    w("| type | size | declared | named | meaning stated | gaps | readiness | level |")
    w("|---|---:|---:|---:|---:|---:|---|---|")
    tot_size = tot_decl = tot_named = tot_fields = tot_meaning = 0
    uns_decl = uns_types = 0
    for tn in sorted(types):
        t = types[tn]
        size = num(t["size"])
        fl = fields.get(tn, [])
        decl = sum(num(f["size"]) for f in fl)
        named = sum(1 for f in fl if f["name"] != "UNRESOLVED")
        stated = sum(1 for f in fl if meaning_stated(f.get("meaning", "")))
        gaps = sum(1 for x in warns if x.startswith(tn + ":"))
        tot_named += named
        tot_meaning += stated
        tot_fields += len(fl)
        if size:
            tot_size += size
            tot_decl += decl
            w("| `%s` | 0x%X | %d B (%.1f %%) | %d / %d | %d / %d | %d | %s | %s |"
              % (tn, size, decl, 100.0 * decl / size, named, len(fl), stated, len(fl), gaps,
                 t["readiness"], t.get("level", "-")))
        else:
            # A type with no declared size has NO DENOMINATOR, and printing `0x0`
            # with `0.0 %` says the opposite of the truth - it reads as a type
            # that is known to be large and entirely unrecovered. Most of these
            # are Phyre middleware, whose sizes belong to its SDK rather than to
            # this game's data, and one - `Widget` - has no size BY DESIGN: its
            # size is a construction argument, 26 distinct values across 49 sites.
            uns_decl += decl
            uns_types += 1
            w("| `%s` | *none declared* | %d B (no denominator) | %d / %d | %d / %d | %d | %s | %s |"
              % (tn, decl, named, len(fl), stated, len(fl), gaps, t["readiness"], t.get("level", "-")))
    w("")
    w("**Totals over the %d type(s) that declare a size: %d of %d bytes (%.1f %%).** "
      "A further **%d type(s) declare no size** and carry %d declared byte(s) between them; "
      "those bytes are NOT counted above, because a numerator without a denominator is not a "
      "percentage. An earlier version added them to the numerator alone and reported %.1f %% "
      "where the truth is %.1f %%."
      % (len(types) - uns_types, tot_decl, tot_size,
         100.0 * tot_decl / tot_size if tot_size else 0,
         uns_types, uns_decl,
         100.0 * (tot_decl + uns_decl) / tot_size if tot_size else 0,
         100.0 * tot_decl / tot_size if tot_size else 0))
    w("")
    w("**%d field(s) across all %d type(s), %d named (%.1f %%), %d with a stated meaning (%.1f %%).** "
      "The two figures measure different axes - labelling and stated purpose - and neither is "
      "understanding. The byte percentage above is dominated by whichever types are largest, not by how "
      "much is known: read it beside the per-type rows, never alone."
      % (tot_fields, len(types), tot_named,
         100.0 * tot_named / tot_fields if tot_fields else 0, tot_meaning,
         100.0 * tot_meaning / tot_fields if tot_fields else 0))
    w("")
    # --- the OTHER structured-layout population ---------------------------------------
    # This page used to report `_types/` alone, and a reader comparing categories would conclude
    # that one with no rows here has no recovered layout at all. That is false: authored formats
    # and in-document record shapes live in ```struct fences, validated by check_layouts.py, and
    # on 2026-09-10 there were 53 of them carrying 259 fields in 29 documents. The omission is a
    # denominator problem, not a cosmetic one - it misdirects where recovery effort goes next.
    #
    # The two populations are reported SIDE BY SIDE and never summed. A fence is a layout inside a
    # document; a store row carries readiness, confidence, per-field evidence and an instance. They
    # are different instruments and merging their counts would hide which one backs a given claim.
    fences = []
    try:
        import check_layouts
        fences = check_layouts.scan(os.path.dirname(store.rstrip(os.sep)))
    except Exception as exc:                       # noqa: BLE001 - reported, never silent
        fences = None
        fence_err = str(exc)

    w("## The other structured-layout population — `struct` fences")
    w("")
    if fences is None:
        w("**Not counted: `check_layouts` could not be read (`%s`).** This section is the only "
          "place the two populations are compared, so treat the table above as the store alone."
          % fence_err)
    else:
        bycat = {}
        for st in fences:
            cat = st["doc"].split("/")[0]
            e = bycat.setdefault(cat, [0, 0])
            e[0] += 1
            e[1] += len([f for f in st["fields"] if f[0] != "BAD"])
        w("Authored formats and in-document record shapes are declared as ```` ```struct ```` "
          "fences and validated by `check_layouts.py`, **not** by this store. A category with no "
          "row in the table above may still have a recovered layout here, so the two are listed "
          "side by side and **never summed** — a fence is a layout inside a document, while a "
          "store row carries readiness, confidence, per-field evidence and an instance address.")
        w("")
        w("| category | fences | fields |")
        w("|---|---:|---:|")
        for cat in sorted(bycat):
            w("| `%s` | %d | %d |" % (cat, bycat[cat][0], bycat[cat][1]))
        w("")
        w("**%d fence(s), %d field(s), across %d document(s) in %d categor(y/ies).**"
          % (len(fences), sum(v[1] for v in bycat.values()),
             len(set(st["doc"] for st in fences)), len(bycat)))
    w("")

    w("## Denominator, stated")
    w("")
    w("**This is coverage *of the store*, not of the game.** The store currently holds %d type(s). "
      "The number of FFXII types that exist is unknown, so a game-wide type-coverage percentage "
      "cannot be computed and is not offered here." % len(types))
    w("")
    w("**And the store is not the only place a layout can live** — see the fence table above "
      "before concluding that a category has nothing recovered.")
    w("")
    if errs:
        w("## Validation errors")
        w("")
        for e in errs:
            w("- **%s**" % e)
        w("")
    if warns:
        w("## Undeclared spans")
        w("")
        w("Each is layout that has not been recovered — a real gap, listed so it can be closed.")
        w("")
        for x in warns:
            w("- %s" % x)
    text = "\n".join(L) + "\n"
    if a.out:
        io.open(a.out, "w", encoding="utf-8", newline="\n").write(text)
        sys.stdout.write("wrote %s (%d lines)\n" % (a.out, len(L)))
    else:
        sys.stdout.write(text)
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main())
