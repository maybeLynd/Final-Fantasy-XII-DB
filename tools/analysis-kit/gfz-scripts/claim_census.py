"""Claim-level reconciliation: what evidence class does each contract claim actually carry?

COMPLETION-PLAN §1: "34 executed contracts are not 34 established systems. A contract's claims are
established CLAIM BY CLAIM, at the evidence class each one earns." Nothing had counted them.

THREE REVISIONS, EACH BECAUSE THE INSTRUMENT WAS WRONG AND NOT THE DOCUMENTS
---------------------------------------------------------------------------
1. The first version classified every claim from the PROSE of its evidence cell and left 25 %
   unclassified. The database has two §15 schemas - a third column holding a numeric TIER, and one
   holding a CLASS word - and reading a stated class as a tier throws it away.
2. The second read the stated class where present and still left 13.2 %. Inspecting the residue
   showed the cause: eight contracts write a COMPOUND class - "static + executed", "static,
   isolated original code" - which is RICHER than either schema, not malformed. Normalising those
   documents was considered and rejected: it would delete the distinction they are drawing.
3. And one contract's §15 opens with a different table entirely (a per-slot function map), so
   "the first table after the heading" was the wrong table.
4. Matching the header then exposed two more population errors, both silent. Selecting the LAST
   matching table let the §15a FALSIFICATION-PASS records - which are also "| claim | ... |" tables
   - replace the claim table of seven contracts. And a four-column row pattern dropped every row of
   a THREE-column claim table. Columns are now found by NAME in the header row, so neither the
   count nor the order of columns is assumed anywhere.

So: compound classes are split and counted at their STRONGEST component, and the table is chosen by
its header rather than by position. Stated and inferred are still counted separately, because adding
a stated class to a guessed one and printing one percentage is how a measurement becomes a claim.

AND THE CORRECTED INSTRUMENT OVERTURNED WHAT IT WAS BUILT TO MEASURE
-------------------------------------------------------------------
There are not three §15 schemas. All 42 claim tables carry ONE header - `| claim | evidence | tier |
confidence |`. The "schemas" were rows the broken tool had picked up out of OTHER tables in §15.
The real defect is inside the one schema: the column is named `tier`, and more than half the rows
put an evidence CLASS in it. Those vocabularies are different axes. EVIDENCE-STANDARD.md's tiers
1-11 grade the KIND OF SOURCE - disassembly, strings, RTTI, runtime capture - while the class grades
HOW THE CLAIM WAS ESTABLISHED: read, executed in isolation, observed live. A claim proved by running
the original code and a claim read off the instructions are BOTH tier 1. So the tier column cannot
answer COMPLETION-PLAN §1, and a row that states one axis leaves the other unrecorded. `schema_overload()`
prints that split, because it is the thing a reader of this census most needs to know about it.

FIFTH REVISION, AND IT CORRECTS THE RULING THE FOURTH WAS QUOTED IN
-------------------------------------------------------------------
"A row that states one axis leaves the other unrecorded" - the sentence above, and the sentence
EVIDENCE-STANDARD addendum 2026-09-15bl ruled on - IS FALSE FOR 304 OF THE 692 ROWS. They state both
axes in ONE CELL: `1 (isolated original-code)`, `1 (static)`, `10 (live)`, `1 (static + **executed**)`.
classify_stated() split a cell on commas, slashes and dashes and matched whole parts against TOKEN,
so it never looked INSIDE A PARENTHESIS, threw the author's own class away on all 304, and handed
them to the inference pass. Stated classes were counted as 31; they are 333.

That is worse than a miscount. bl's own text says a table that prints an inferred class as if the
author had asserted it "converts a tool's guess into a document's claim, which is the failure this
standard exists to prevent" - and on 110 of the 304 the guess DISAGREED with the author's word, 73
of them reading `executed` as `static`. The distinction COMPLETION-PLAN §1 asks for was being
deleted by the instrument built to report it.

TIER_PAREN opens the parenthesis. `1 (authored data)` still classifies as nothing, because that
parenthesis is a note on the source and not a class. _hits() also takes a word-boundary match as a
FALLBACK when no part matches exactly, so `**executed** in both directions; a latched reconstruction
fails on 2 comparisons` reads at `executed` rather than at its weaker component - and a component
carrying a negation is excluded from that fallback, so `not exercised` cannot read as a claim that
something was. The fallback is the one loosening here; it is named because it is the one that could
over-read a cell.
"""
import collections
import glob
import io
import os
import re
import kit_paths as KP  # noqa: E402

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")

# strongest first - a compound class is counted at its strongest component
ORDER = ["live", "executed", "corpus", "static", "none"]
TOKEN = {
    "live": "live", "integrated": "live", "in-game": "live", "runtime": "live",
    "isolated original-code": "executed", "isolated original code": "executed",
    "isolated": "executed", "executed": "executed", "original-code": "executed",
    "original code": "executed",
    "corpus": "corpus", "file corpus": "corpus", "census": "corpus",
    "static": "static", "static only": "static", "read": "static",
    "none": "none", "unknown": "none",
}
# em- and en-dashes separate a class from its qualifier: "static - **not exercised**"
SPLIT = re.compile(r"\s*(?:,|\+|/|\u2014|\u2013|--|\band\b|\bplus\b)\s*")
INFER = [
    ("live", re.compile(r"\blive\b|breakpoint|capture|in-game", re.I)),
    ("executed", re.compile(r"\bEXECUTED\b|diff_\w+\.py", re.I)),
    ("corpus", re.compile(r"\bcorpus\b|\bcensus\b|\bin \d+/\d+ files|shipped table", re.I)),
    # `^\*\*none\*\*` required the emphasis to close right after the word, so `**none exists**` and
    # `**nothing**: all 36 encoder calls took the argument 0` - both of them a cell saying plainly
    # that nothing establishes the claim - fell through to unclassified. 8 rows.
    ("none", re.compile(r"^\s*\*\*(?:none|nothing)\b|not established|\bunknown\b", re.I)),
    # A cell whose evidence is "the page's §9" or "the source page §2.5" cites a reading that was
    # done, on a page, from the bytes. That is `static` by this vocabulary. It sits LAST, so a cell
    # that also says census or EXECUTED still classifies at the stronger word. 10 rows.
    ("static", re.compile(r"re-read|re-derived|read whole|disassembl|the bytes|[0-9A-F]{8}|"
                          r"\bthe (?:source )?page'?s? §", re.I)),
]
# `1 (isolated original-code)` - a tier and a class in ONE cell. The tier is the lead digit and the
# class is inside the parenthesis; `1 (authored data)` is the case where the parenthesis is a note
# on the source and holds no class at all, which stays unclassified.
TIER_PAREN = re.compile(r"^\d+\s*\((.+)\)$", re.S)
NEGATED = re.compile(r"\b(?:no|not|never|none|without|absent|un\w+)\b", re.I)
SEPARATOR = re.compile(r"^\s*\|[\s:|-]*\|\s*$")
# a tier-1 row whose evidence names an executed run - the control for "the tier cannot see it"
EXEC_CITE = re.compile(r"\bEXECUTED\b|diff_\w+\.py|emulated original|pilot", re.I)


def cells(line):
    """The cells of one markdown row. Split on the pipes, minus the leading and trailing empties.

    A pipe ESCAPED as \\| is content, not a boundary - contracts write it inside code spans such as
    `+0x3C \\| +0x64`. Splitting on it shifted every column to its right."""
    parts = [p.replace("\0", "\\|") for p in line.strip().replace("\\|", "\0").split("|")]
    if parts and not parts[0].strip():
        parts = parts[1:]
    if parts and not parts[-1].strip():
        parts = parts[:-1]
    return [p.strip() for p in parts]


def columns(header):
    """Locate the evidence and the class/tier columns BY NAME. Contract tables are three or four
    columns wide and do not agree on order, so position is not safe to assume."""
    names = [c.strip("*` ").lower() for c in cells(header)]
    ev = cls = None
    for i, n in enumerate(names):
        if ev is None and "evidence" in n and "class" not in n:
            ev = i
        if cls is None and ("class" in n or "tier" in n):
            cls = i
    return ev if ev is not None else 1, cls


def _hits(cell):
    """The class tokens a cell states. Exact part matches first; a word-boundary match is the
    fallback for a component carrying a trailing qualifier - `**executed** in both directions` is
    the author saying executed, and exact matching read those rows at their WEAKER component.
    A part carrying a negation is not a fallback candidate: `not exercised` must not read as a
    claim that something was."""
    parts = [p.strip("*` ").lower() for p in SPLIT.split(cell.strip("*` ")) if p.strip("*` ")]
    out = []
    for p in parts:
        if p in TOKEN:
            out.append(TOKEN[p])
            continue
        if NEGATED.search(p):
            continue
        for word, cls in TOKEN.items():
            if re.search(r"\b%s\b" % re.escape(word), p):
                out.append(cls)
                break
    return out


def classify_stated(cell):
    """A stated class, possibly compound. Returns (class, compound?) or (None, False).

    A cell may state BOTH axes at once - `1 (isolated original-code)`, `10 (live)`,
    `1 (static + **executed**)`. Reading only the top level threw the author's own class away on
    299 of 692 rows and handed them to the inference pass, so the parenthesis is opened here."""
    hits = _hits(cell)
    if not hits:
        m = TIER_PAREN.match(cell.strip("*` "))
        if m:
            hits = _hits(m.group(1))
    if not hits:
        return None, False
    best = min(hits, key=ORDER.index)
    return best, len(set(hits)) > 1


def claim_table(text):
    """The §15 table whose header names a claim - NOT simply the first table in the section."""
    m = re.search(r"^## 15\.[^\n]*\n(.*?)(?=^## 16\.)", text, re.S | re.M)
    if not m:
        return None
    tables, cur = [], []
    for line in m.group(1).splitlines():
        # ANY leading pipe is part of the table. The separator row is |---|---|, which does not
        # start with "| " - cutting on that ended every table one line after its header and gave
        # a census of zero claims across all 42 contracts.
        if line.lstrip().startswith("|"):
            cur.append(line)
        else:
            if cur:
                tables.append(cur)
            cur = []
    if cur:
        tables.append(cur)
    for t in tables:
        # The FIRST header match. §15a falsification-pass records are also "| claim | ... |"
        # tables and sit BELOW the claim table; taking the last match let them replace it.
        if re.match(r"^\|\s*\**\s*claim\s*\**\s*\|", t[0], re.I):
            return "\n".join(t)
    return None


def main():
    stated = collections.Counter()
    inferred = collections.Counter()
    compound = 0
    schema = collections.Counter()
    overload = collections.Counter()
    both = t_exec = t_plain = 0
    docs = 0
    for path in sorted(glob.glob(os.path.join(DB, "**", "CONTRACT-*.md"), recursive=True)):
        text = io.open(path, encoding="utf-8").read()
        tbl = claim_table(text)
        if not tbl:
            schema["no claim table found"] += 1
            continue
        docs += 1
        kinds = set()
        axes = set()
        lines = tbl.splitlines()
        ev_i, cls_i = columns(lines[0])
        for line in lines[1:]:
            if SEPARATOR.match(line):
                continue
            cl = cells(line)
            if not cl:
                continue
            claim = cl[0]
            evidence = cl[ev_i] if ev_i < len(cl) else ""
            third = cl[cls_i] if cls_i is not None and cls_i < len(cl) else ""
            if claim.startswith("---") or claim.strip("*` ").lower() == "claim":
                continue
            bare = third.strip("*` ")
            lead = bare.split()[0].rstrip(".") if bare.split() else ""
            has_tier = lead.isdigit()
            has_class = classify_stated(third)[0] is not None
            # A cell can state BOTH - `1 (isolated original-code)`. Bucketing it as a tier, which is
            # what the lead digit alone says, was how the author's class went missing on 299 rows.
            if has_tier and has_class:
                overload["BOTH - a tier AND a class, in one cell"] += 1
                axes.add("tier")
                axes.add("class")
            elif has_tier:
                overload["a NUMBER ONLY - a source tier"] += 1
                axes.add("tier")
            elif has_class:
                overload["a CLASS WORD ONLY - how it was established"] += 1
                axes.add("class")
            elif bare:
                overload["neither"] += 1
            else:
                overload["empty"] += 1
            if lead == "1":
                if EXEC_CITE.search(evidence):
                    t_exec += 1
                else:
                    t_plain += 1
            cls, comp = classify_stated(third)
            if cls:
                stated[cls] += 1
                compound += 1 if comp else 0
                kinds.add("compound" if comp else "class")
            else:
                got = "unclassified"
                for name, rx in INFER:
                    if rx.search(evidence):
                        got = name
                        break
                inferred[got] += 1
                kinds.add("tier" if third.strip("*` ").isdigit() else "other")
        schema["+".join(sorted(kinds)) or "empty"] += 1
        both += 1 if len(axes) > 1 else 0

    ns, ni = sum(stated.values()), sum(inferred.values())
    print("=== the third column is named `tier` in all %d tables, and holds two vocabularies" % docs)
    for k, v in overload.most_common():
        n = sum(overload.values())
        print("   %-34s %4d  %5.1f%%" % (k, v, 100.0 * v / n if n else 0))
    print("   %-34s %4d contracts use BOTH in one table" % ("", both))
    print("   tier 1 rows citing an executed pilot: %d; not citing one: %d - SAME TIER\n"
          % (t_exec, t_plain))
    print("=== %d contracts with a claim table" % docs)
    for k, v in schema.most_common():
        print("   %-24s %d" % (k, v))
    print("\n=== class STATED by the table (%d claims, %d of them compound)" % (ns, compound))
    for k in ORDER:
        print("   %-10s %4d  %5.1f%%" % (k, stated[k], 100.0 * stated[k] / ns if ns else 0))
    print("\n=== class INFERRED from the evidence prose (%d) - weaker, counted apart" % ni)
    for k in ORDER + ["unclassified"]:
        print("   %-10s %4d  %5.1f%%" % (k, inferred[k], 100.0 * inferred[k] / ni if ni else 0))
    tot = collections.Counter()
    tot.update(stated)
    tot.update(inferred)
    n = sum(tot.values())
    print("\n=== both, %d claims" % n)
    for k in ORDER + ["unclassified"]:
        print("   %-10s %4d  %5.1f%%" % (k, tot[k], 100.0 * tot[k] / n if n else 0))


if __name__ == "__main__":
    main()
