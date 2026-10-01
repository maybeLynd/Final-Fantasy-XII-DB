#!/usr/bin/env python3
"""check_family_spans.py - does a declared EC-7 family's NOTE actually describe its MEMBERS?

`check_dispositions.py` accepts a family on STRUCTURE: five fields, a non-empty note, a readable
members file, unique members, no cross-family collision. That gate is real and it refuses. What it
cannot do is read the note.

The note is the falsifiable claim - the gate's own refusal text says so: *"C without a note -- the
bar is a falsifiable claim, not a label"*. So a family whose note states a rule the member file does
not obey has passed a gate that never tested the only thing the note is for. **12,202 bodies are
dispositioned C through 94 such families.**

What this checks
----------------
The single most common and highest-risk rule shape: a LINK SPAN. A note saying *"every census entry
in the link span from 007A4380 up to (not including) 007F41A0"* makes a claim that can be tested
against the member list in one pass. A span disposition is the riskiest kind because a wrong
boundary sweeps real engine code out of the frontier as somebody else's library, and nothing
downstream ever looks at it again.

    OUTSIDE   a member is outside every span AND is not named anywhere in the note  <- READ IT
    INSIDE    members all obey the note's span
    NO-SPAN   the note states no address range, so this cannot judge it

NO-SPAN is not a pass. It is this checker declining, and it is reported separately so the number of
families nothing has tested stays visible rather than being folded into a clean-looking total.

OUTSIDE IS TRIAGE, NEVER A VERDICT - and the first run of this tool is why that is in capitals.
It reported three failing families and ALL THREE WERE ITS OWN FAULT:

  * `libwebm mkvparser`, 95 of 100 members "outside". Its note declares the run
    `007FFBC0 up to 00808888`; the regex had instead picked up `007FFCD0-00800150` out of the
    note's **NOT covered** clause. A range in an exclusion clause is not the family's span.
  * `libvpx VP8 DSP kernels`, 3 "outside" - every one of the three NAMED IN ITS OWN NOTE
    ("one at 00133B40 ... two at 00158B40 / 00158C09").
  * `SQEX SEAD sound library span`, 9 "outside" - the note ends
    "plus nine SEAD entries just past the span that RTTI or their only callers prove SEAD's".

The notes are richer than a span: they carry an inclusion range, named individual members, named
exceptions and a NOT-covered clause, all in prose written for a human. A parser will pick the wrong
clause. The named-address test below removes the libvpx class of false positive; nothing removes the
other two, so every OUTSIDE row must be settled by reading the note. **Three agents' families were
one publication away from being reported as defective by this tool.**
"""
import argparse
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# "from 007A4380 up to (not including) 007F41A0", "007A4380-007F41A0", "007A4380..007F41A0"
SPAN = re.compile(
    r"\b0?0?([0-9A-Fa-f]{6,8})\b\s*(?:-|\.\.|up to \(not including\)|up to|to|through)\s*"
    r"\b0?0?([0-9A-Fa-f]{6,8})\b")


# An address written out in the note, word-bounded so it cannot start mid-token.
NAMED = re.compile(r"\b([0-9A-Fa-f]{6,8})\b")


# The trailing clauses of a family note describe what is NOT in it, or what sits beside it. A range
# found in one of them is not the family's extent.
TRAILING = re.compile(r"\bNOT covered\b|\bBoundary\s*:|\bControls?\s*:|\bFingerprint\s*:", re.I)


def inclusion_clause(note):
    """The part of the note before the first exclusion/control/boundary clause."""
    m = TRAILING.search(note)
    return note[:m.start()] if m else note


def spans_in(note):
    out = []
    for m in SPAN.finditer(note):
        lo, hi = int(m.group(1), 16), int(m.group(2), 16)
        # An address range, not a pair of counts: both ends must look like code addresses and
        # run upward. Without this a note saying "1216 - 1259" parses as a span.
        if 0x100000 <= lo < hi <= 0x1000000:
            out.append((lo, hi))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)

    import check_dispositions as CD
    rows = CD.parse_families(a.db)

    stats = collections.Counter()
    findings = []
    span_rows = []
    for doc, parts in rows:
        if len(parts) < 5:
            continue
        name, letter, rel, _count, note = parts[0], parts[1], parts[2], parts[3], "|".join(parts[4:])
        if letter not in ("B", "C", "D"):
            continue
        spans = spans_in(inclusion_clause(note))
        if not spans:
            stats["NO-SPAN"] += 1
            continue
        try:
            members = CD.read_members(doc, rel)
        except (IOError, OSError, ValueError):
            stats["UNREADABLE"] += 1
            continue
        # THE ENDPOINT IS TESTED PERMISSIVELY, ON PURPOSE. The SEAD note spells its convention out
        # -- "up to (not including) 007F41A0" -- but "007B9D70..007BA970" does not say whether the
        # upper bound is inclusive. The first version of this assumed exclusive and duly reported
        # libogg's single "outside" member as 007BA970: the span's own endpoint. That is a report
        # about my convention, not about the family. So a member is only counted OUTSIDE when it
        # falls outside the range under the MOST GENEROUS reading, hi included.
        # A note may name individual members outright ("one at 00133B40 ... two at 00158B40 /
        # 00158C09"). An address written in the note is accounted for, wherever it sits.
        named = set(int(h, 16) for h in NAMED.findall(note))
        outside = sorted({m for m in members
                          if not any(lo <= m <= hi for lo, hi in spans) and m not in named})
        if outside:
            stats["OUTSIDE"] += 1
            findings.append((os.path.basename(doc), name, letter, spans,
                             len(members), outside))
        else:
            stats["INSIDE"] += 1
        span_rows.append((os.path.basename(doc), name, letter, spans, set(members), note))

    # ---- THE OTHER DIRECTION, added 2026-09-14 (OPUS) ----------------------------------------
    #
    # Everything above asks whether the MEMBERS obey the NOTE. Nothing asked whether the NOTE's
    # span is FULL: a family can declare "every census entry in 007A4380..007F41A0", satisfy every
    # structural check, and leave bodies inside that range belonging to no family at all. That is
    # the shape check_float_typed_as_int names about itself -- an empty half of a symmetric test is
    # a result and a MISSING half is a blind spot.
    #
    # Found on the largest C family in the corpus: SQEX SEAD sound library span, 1,216 bodies, the
    # single biggest block of "explained". Its note says the members are the span "less the libogg
    # framing object inside". Inside the span, 52 census entries are not members -- 22 are libogg
    # as stated, 10 more belong to four OTHER families the note never mentions (the thunk layer,
    # libwebm mkvparser, NativeLeaf.MemberAddressAccessor), and 20 BELONG TO NOBODY.
    #
    # Unclaimed bodies inside a declared span are not necessarily a defect: the selector may have
    # excluded them deliberately. What is a defect is that nothing says so, and nothing asked.
    # THE GAP MUST BE CLASSIFIED, NOT COUNTED. check_dispositions REFUSES a family member that is
    # already measured as A -- "A beats a declaration" -- and a generated selector excludes
    # A-measured entries by design. So a body inside a span that belongs to no family is usually
    # INDIVIDUALLY EXPLAINED instead, and reporting the raw count would manufacture alarm: on the
    # SEAD family, 18 of the 20 are exactly that. Only a body inside a declared span that no
    # document cites at all is worth a reader's time.
    unclaimed = []
    if span_rows:
        claimed = set()
        for doc, parts in rows:
            if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
                continue
            try:
                claimed |= set(CD.read_members(doc, parts[2]))
            except (IOError, OSError, ValueError):
                pass
        sizes = CD.load_functions(None)
        a_set, _eo, _ai, documented_any = CD.measure_a(a.db, sizes)
        for doc, name, letter, spans, _members, note in span_rows:
            gap = sorted({f for f in sizes
                          if any(lo <= f <= hi for lo, hi in spans)} - claimed)
            if not gap:
                continue
            # AND THE SAME EXEMPTION THE OUTSIDE HALF ALREADY HAS. That half exempts a member the
            # note names outright; this half must exempt an UNCLAIMED address the note names
            # outright, for the identical reason -- an address written in the note is accounted
            # for, wherever it sits. Both of the two bodies this check first reported as DARK are
            # named in their own family's note as deliberate exclusions: libvorbis says "less
            # three A-measured entries AND 00887630, which nothing references and no fingerprint
            # identifies", and the libvpx DSP note says "kernels with no reference at all (e.g.
            # 001274D0 ...) are NOT claimed". I filed both as findings before reading the notes.
            # 2026-09-14, OPUS.
            note_named = set(int(h, 16) for h in NAMED.findall(note))
            gap = [g for g in gap if g not in note_named]
            if not gap:
                continue
            in_a = [g for g in gap if g in a_set]
            cited = [g for g in gap if g not in a_set and g in documented_any]
            dark = [g for g in gap if g not in a_set and g not in documented_any]
            unclaimed.append((doc, name, letter, spans, gap, in_a, cited, dark))

    total = sum(stats.values())
    print("EC-7 family span check - does the NOTE describe the MEMBERS?")
    print("  %d declared B/C/D families" % total)
    print("    INSIDE     %4d   every member obeys the span its note names" % stats["INSIDE"])
    print("    OUTSIDE    %4d   <- READ THE NOTE; this is triage, never a verdict"
          % stats["OUTSIDE"])
    print("    NO-SPAN    %4d   note states no address range; NOT a pass, this checker declining"
          % stats["NO-SPAN"])
    if stats["UNREADABLE"]:
        print("    UNREADABLE %4d" % stats["UNREADABLE"])

    for doc, name, letter, spans, n, outside in findings:
        print("\n  %s :: %s  [%s]" % (doc, name, letter))
        print("    note's span(s): %s" % ", ".join("%08X..%08X" % s for s in spans))
        print("    %d members, %d OUTSIDE every declared span" % (n, len(outside)))
        show = outside if a.list else outside[:10]
        print("      %s%s" % (" ".join("%08X" % x for x in show),
                              "" if len(show) == len(outside) else " ..."))

    print("\n  THE OTHER DIRECTION - census bodies INSIDE a declared span that NO family claims")
    print("  Split three ways, because the raw count is misleading: a selector EXCLUDES A-measured")
    print("  entries by design, so most of a gap is individually explained rather than missing.")
    print("  Only DARK - inside a declared span and cited by no document at all - is worth reading,")
    print("  AND RUN THE FAMILY'S SELECTOR FIRST. A note is an abridgement; the selector is the")
    print("  rule, and it usually excludes these by name with a reason ('joined to the parser by")
    print("  nothing', 'RTTI not Bullet's', 'called only from outside'). 9 of the first 11 DARK rows")
    print("  reported here were already answered that way. 2026-09-14, OPUS.")
    if not unclaimed:
        print("    none - every span is full")
    tot = [0, 0, 0, 0]
    for doc, name, letter, spans, gap, in_a, cited, dark in unclaimed:
        tot[0] += len(gap); tot[1] += len(in_a); tot[2] += len(cited); tot[3] += len(dark)
        print("\n  %s :: %s  [%s]" % (doc, name, letter))
        print("    note's span(s): %s" % ", ".join("%08X..%08X" % s for s in spans))
        print("    %d unclaimed = %d A-measured + %d cited-not-A + %d DARK"
              % (len(gap), len(in_a), len(cited), len(dark)))
        if dark:
            show = dark if a.list else dark[:10]
            print("      DARK: %s%s" % (" ".join("%08X" % x for x in show),
                                        "" if len(show) == len(dark) else " ..."))
    if unclaimed:
        print("\n    TOTAL %d unclaimed = %d A-measured + %d cited-not-A + %d DARK"
              % tuple(tot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
