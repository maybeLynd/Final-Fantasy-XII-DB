"""check_tier_inflation.py - FINAL-AUDIT pass 8, the part of it that is not a judgement.

Pass 8 is *"re-judge each cited tier against the actual evidence; fails if any claim cites a stronger
tier than it earns"*, and `check_tier_presence` says plainly that it does not do this: *"pass 7 asks
whether a tier is cited, not whether it is EARNED - that is pass 8."* Pass 8 has had no instrument,
and most of it genuinely needs a person: deciding whether a body really supports a tier-1 claim is
the reading, not a test.

BUT TWO OF THE ELEVEN TIERS ARE DEFINED IN TERMS THAT A MACHINE CAN CHECK, because
`EVIDENCE-STANDARD.md` states a rule rather than a description:

    tier 11  "Call graph / neighbourhood - supporting context only, NEVER a primary claim"
    tier 10  "Runtime evidence - LiveLab, DynamoRIO traces, Cheat Engine"

I thought the first was airtight, and it is not. Reading the twelve rows it finds is what showed it:
every one makes a claim whose SUBJECT IS THE CALL GRAPH -- "639 references to the array base", "One
caller", "`007AD450`'s 98 callers are all Audio-owned", "Only 1 of the 585 has callers in 3+ owner
categories". For a claim *about* the call graph, the call graph is not a weak substitute for better
evidence; it is the right evidence and the only evidence. One row even reads `tier 11
(corroboration)` -- the page marking its own row as supporting rather than primary.

So "never a primary claim" almost certainly means never primary evidence for a claim about BEHAVIOUR
or OWNERSHIP, not for a claim about the graph itself, and deciding which of the twelve is which is
exactly the reading pass 8 asks for. **Both lists below are CANDIDATES, not defects, and this exits
0** -- a checker that goes red on candidates teaches people to ignore it.

The second is a proxy too, and a leakier one than it looks: two of the rows it finds are annotated
*"(corrected 2026-09-13 from 3: this is runtime evidence, not a qualified symbol)"*, so the document
is asserting runtime evidence in words this checker's marker list does not contain. A row citing tier 10 asserts runtime evidence, so the
document should be able to point at some -- an `_experiments/` link, or a live-evidence marker. A
document citing tier 10 with no runtime evidence anywhere in it is not proof of inflation, but it is
exactly the row pass 8 exists to re-judge, and it is worth handing a human a short list instead of
2,535 rows.

WHAT THIS DOES NOT DO. It does not judge tiers 1-9. Whether a body earns tier 1, whether a string is
really tied to the body for tier 2, whether an RTTI marker is independently verified for tier 4 --
all of that is the reading pass 8 asks for and none of it is mechanical. This checks the two rules
the standard wrote as rules.
"""
import io, os, re, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_dispositions as CD

DB_DEFAULT = "Database/FFXII TZA"
TIERHDR = re.compile(r"^\**\s*tier\s*\**$", re.I)
NUM = re.compile(r"\b(\d{1,2})\b")
LIVE = re.compile(r"_experiments/|live_game:\s*true|LiveLab|DynamoRIO|Cheat Engine|EXP-\d+", re.I)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB_DEFAULT)
    a = ap.parse_args(argv)

    only11, tier10_no_live, rows_seen = [], [], 0
    for p in CD.docs(a.db):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(p, a.db).replace(os.sep, "/")
        has_live = bool(LIVE.search(t))
        col = None
        for n, ln in enumerate(t.split("\n"), 1):
            if not ln.strip().startswith("|"):
                col = None
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            hdr = [i for i, c in enumerate(cells) if TIERHDR.match(c.strip("` "))]
            if hdr:
                col = hdr[0]
                continue
            if col is None or len(cells) <= col or "---" in ln:
                continue
            v = cells[col].strip("* `").strip()
            if not v or v in ("-", "—"):
                continue
            rows_seen += 1
            nums = set(NUM.findall(v))
            if nums == {"11"}:
                only11.append((rel, n, v, cells[0][:60]))
            if "10" in nums and not has_live:
                tier10_no_live.append((rel, n, v, cells[0][:60]))

    print("FINAL-AUDIT pass 8 - the two tier rules the standard wrote as rules\n")
    print("  claim rows with a tier value : %d" % rows_seen)
    print()
    print("  TIER 11 ALONE - CANDIDATES for pass 8's reading, not defects")
    print("    the standard says tier 11 is 'supporting context only, never a primary claim', but")
    print("    every row below claims something ABOUT THE CALL GRAPH, where the call graph is the")
    print("    right evidence rather than a weak substitute. Which of these is a behaviour or")
    print("    ownership claim leaning on 11 is the judgement pass 8 exists to make.")
    print("    rows whose only cited tier is 11 : %d" % len(only11))
    for rel, n, v, claim in only11[:20]:
        print("      %-58s line %-5d tier %-8s %s" % (rel[:58], n, v, claim))
    print()
    print("  TIER 10 WITHOUT A RUNTIME MARKER THIS CHECKER RECOGNISES - a leaky proxy")
    print("    at least two rows below are annotated as CORRECTED TO tier 10 precisely because the")
    print("    evidence is runtime, in words this checker's marker list does not contain.")
    print("    rows citing tier 10 in a document with no experiment or runtime marker : %d"
          % len(tier10_no_live))
    for rel, n, v, claim in tier10_no_live[:20]:
        print("      %-58s line %-5d tier %-8s %s" % (rel[:58], n, v, claim))
    print()
    print("  Tiers 1-9 are not judged here: whether a body earns tier 1, or a string is really tied")
    print("  to it for tier 2, is the reading pass 8 asks for and is not mechanical.")
    # Exit 0: every row here is a candidate for a human reading, and a checker that goes red on
    # candidates teaches people to ignore it. Pass 8 is a judgement; this hands it a short list.
    return 0


if __name__ == "__main__":
    sys.exit(main())
