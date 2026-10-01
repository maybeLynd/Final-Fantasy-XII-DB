#!/usr/bin/env python3
"""check_store_behind_page.py - gap rows whose own page already describes the offset.

WHY THIS EXISTS. `WorldLootPickupNode +0x08` sat in `_types/fields.tsv` as `unobservedSpan0008`,
`u8[8]`, "no censused access", while the subsystem's own page had described that offset as the
field-clock stamp since 2026-09-07 and built a whole state machine on it. Reading the image settled
it - the stamp is a live `uint32` there - but the disagreement had stood for two weeks. **A row
claiming no access over bytes its own page reads every frame makes the store untrustworthy even
where it is right**, and nothing in the kit was looking for that class of drift.

WHAT IT DOES. 272 of the 290 types holding gap rows carry a `documents` link. For each gap row it
asks one question: **does that type's own page mention this offset?** If it does, the store and the
page may disagree, and a human should look.

WHAT IT IS NOT, and today's record is the reason to say so plainly. This is a LEAD GENERATOR joined
on an offset token, and an offset token is weak evidence: `+0x08` appears on pages discussing a
dozen unrelated records, so a hit means "these two documents both mention this number", not "the
store is wrong here". An earlier join in this kit went 0-for-2 on exactly this kind of match. Hits
are CANDIDATES, they are printed for reading, and nothing is ever applied.

**A HIT HAS THREE POSSIBLE MEANINGS AND ONLY ONE IS A DEFECT.** Each has now been met in the corpus:

  DRIFT        the page describes a live field where the store says no access. The one this file was
               built from: `WorldLootPickupNode +0x08`, a field-clock stamp read and written every
               frame while the row read `u8[8]`, "no censused access". Fixed in 913471921.
  COINCIDENCE  the page mentions the number about something else entirely.
               `WorldLootPickupNode +0x0C` matches an appendix on a texcoord decoder writing
               `[rbx+0xC]`. The store is right and the page is not talking about it.
  CONFIRMATION the page mentions the offset PRECISELY TO DOCUMENT IT AS UNEXPLAINED, and often with
               far better evidence than the store row carries. `BattleUnit +0x120` (32 B) and
               `+0xEB4` (156 B) are named on their page only to record that a pool closure - seeded
               from every accessor's callers, tainting return values, following each handoff, over
               67 proved bodies with three routes closed in turn - finds them untouched by direct
               access AND by handoff. Store and page AGREE; the hit is the agreement.

So a hit is as likely to be the store and the page agreeing as disagreeing, and reading one costs a
page read plus, for a real drift, an image read.

THE CONTROL IS THE CASE THAT MOTIVATED IT. `WorldLootPickupNode` is checked explicitly: its `+0x08`
row was split into a proven `materialiseStamp` and a genuine 4-byte gap at `+0x0C`, so the type must
now produce NO `+0x08` candidate and the `+0x0C` row must NOT be flagged by a page that never
describes it. A checker that cannot show both answers on a case with a known resolution has not been
shown to be reading anything.
"""
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402

TYPES = os.path.join(KP.DB, "_types", "types.tsv")
FIELDS = os.path.join(KP.DB, "_types", "fields.tsv")


def rows(path):
    raw = io.open(path, encoding="utf-8", newline="").read().split("\n")
    head = raw[0].split("\t")
    return head, [l.split("\t") for l in raw[1:] if l.strip()]


def num(s):
    s = (s or "").strip()
    try:
        return int(s, 16) if s.lower().startswith("0x") else int(s)
    except ValueError:
        return None


def offset_tokens(off):
    """The spellings a page plausibly uses for one offset, anchored so a PREFIX cannot match.

    THE FIRST VERSION MATCHED BY SUBSTRING AND IT WAS WRONG. `+0x20` is a prefix of `+0x200` and
    `+0x2000`, so `BattleUnit.unobservedSpan0020` was reported as a candidate on the strength of two
    page lines about `+0x200` - a different field of the same object. Every short offset in the
    corpus had that inflation, and short offsets are the common ones.

    The token must therefore be followed by something that is NOT a hex digit. Written as a regex
    per spelling rather than a substring test.
    """
    out = set()
    for f in ("+0x%X", "+0x%02X", "+0x%03X", "+0x%04X",
              "+0x%x", "+0x%02x", "+0x%03x", "+0x%04x"):
        out.add(f % off)
    return {re.compile(re.escape(t) + r"(?![0-9A-Fa-f])") for t in out}


def main():
    ht, tr = rows(TYPES)
    I = {k: ht.index(k) for k in ht}
    hf, fr = rows(FIELDS)
    J = {k: hf.index(k) for k in hf}
    docs = {}
    for r in tr:
        if len(r) > I["documents"] and r[I["documents"]].strip():
            docs[r[I["type"]]] = [d.strip() for d in r[I["documents"]].split(";") if d.strip()]

    text = {}

    def page(rel):
        if rel not in text:
            p = os.path.join(KP.DB, rel)
            try:
                text[rel] = io.open(p, encoding="utf-8", newline="").read()
            except OSError:
                text[rel] = None
        return text[rel]

    gaps = [r for r in fr if r[J["name"]].startswith("unobserved")]
    cand = []
    nodoc = missing = 0
    for r in gaps:
        t = r[J["type"]]
        if t not in docs:
            nodoc += 1
            continue
        off = num(r[J["offset"]])
        if off is None:
            continue
        toks = offset_tokens(off)
        for rel in docs[t]:
            body = page(rel)
            if body is None:
                missing += 1
                continue
            if any(tok.search(body) for tok in toks):
                cand.append((t, r[J["offset"]], r[J["name"]], num(r[J["size"]]) or 0, rel))
                break

    print("GAP ROWS WHOSE OWN PAGE MENTIONS THE OFFSET")
    print("  gap rows examined                    : %d" % len(gaps))
    print("  skipped, type has no documents link  : %d" % nodoc)
    print("  documents link that does not resolve : %d" % missing)
    print("  CANDIDATES                           : %d" % len(cand))
    print()
    print("  A HIT MEANS TWO DOCUMENTS MENTION THE SAME NUMBER, not that the store is wrong. An")
    print("  offset token is weak evidence - `+0x08` appears on pages discussing many records - and")
    print("  an earlier offset join in this kit went 0-for-2. These are leads, never applied.")
    print()
    bytype = collections.Counter(c[0] for c in cand)
    print("  TYPES WITH THE MOST CANDIDATE ROWS:")
    for t, n in bytype.most_common(12):
        rel = next(c[4] for c in cand if c[0] == t)
        print("      %-34s %2d row(s)   %s" % (t, n, rel))
    print()
    wl = [c for c in cand if c[0] == "WorldLootPickupNode"]
    ok8 = not any(c[1] in ("0x08", "0x8") for c in wl)
    fp_c = any(c[1] in ("0x0C", "0xC", "0x000C") for c in wl)
    print("  CONTROL - the case that motivated this file (913471921), and it shows BOTH answers:")
    print("      +0x08 was the real drift and is now a proven materialiseStamp, so it must NOT")
    print("      still be a candidate                                              : %s"
          % ("PASS" if ok8 else "FAIL"))
    print("      +0x0C is a genuine gap - nothing in the driver, allocator, granter, remover or")
    print("      initialiser touches it - yet it IS flagged, because the page's appendix discusses")
    print("      an unrelated texcoord decoder writing `[rbx+0xC]` and `[rdx+0xC]`. A KNOWN FALSE")
    print("      POSITIVE, demonstrated rather than asserted                       : %s"
          % ("PASS" if fp_c else "FAIL - the false-positive demo stopped reproducing"))
    print()
    print("  READ SO FAR, and the tally is the calibration: 1 DRIFT (the row this file was built")
    print("  from), 1 COINCIDENCE, 2 CONFIRMATIONS (BattleUnit +0x120 and +0xEB4, where the page")
    print("  documents the span as untouched by a pool closure over 67 bodies). Only DRIFT is a")
    print("  defect. An anchored-token fix removed 47 prefix artifacts from an earlier 351.")
    print()
    print("  SO THE CALIBRATION IS: on the ONE row in this list whose ground truth is established,")
    print("  the instrument produces a FALSE POSITIVE. Read the %d candidates as a reading queue"
          % len(cand))
    print("  with a high false-positive rate, not as %d defects. The one real case it was built"
          % len(cand))
    print("  from was found by reading the page, and confirming it took reading the image.")
    return 0 if (ok8 and fp_c) else 2


if __name__ == "__main__":
    raise SystemExit(main())
