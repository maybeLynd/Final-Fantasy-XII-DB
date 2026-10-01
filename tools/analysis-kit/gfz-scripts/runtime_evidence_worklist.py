#!/usr/bin/env python3
"""runtime_evidence_worklist.py - executed evidence the runtime verdicts have not yet judged (OPUS, 2026-09-25)

A WORKLIST for L2-VERDICTS' runtime column, the way contract_named_state_census.py is for types. It scores
nothing. Found by hand first: S-02's runtime text says "the exercised body is one function of three pages",
while EXP-191 executes the other two - evidence existed that the verdict had never judged.

For every system whose runtime cell is not MET:
  1. its contracts = the `contracts` column of _index/important-subsystems.tsv (the registry), plus any
     CONTRACT-*.md named in the verdict row's contract cell;
  2. its experiments = EXP-NNN ids cited anywhere in those contracts, plus EXP records whose first 3,000
     characters (frontmatter / header) name one of them;
  3. JUDGED = the experiment id appears in the verdict row or in any L2-VERDICTS section headed by the
     system id; UNJUDGED otherwise. No dates are used: a row line's blame date moves whenever ANY cell
     changes, so it cannot date the runtime cell.
  4. each record's class markers are reported: `live_game: true`, and whether it discloses stubs/scripted
     boundaries - the qualifier the table applies (S-10 MET, no stubs; S-01 MIXED, stubs).

    runtime_evidence_worklist.py [--out rows.tsv]
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

DB = G.DB
EXPDIR = os.path.join(DB, "_experiments")
EXP = re.compile(r"\bEXP-(\d{3})\b")
CON = re.compile(r"CONTRACT-[A-Za-z0-9-]+\.md")
SID = re.compile(r"S-\d\d")


def split_row(line):
    return [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]


def contracts_index():
    idx = {}
    for root, _d, files in os.walk(DB):
        if os.path.relpath(root, DB).split(os.sep)[0].startswith("_"):
            continue
        for f in files:
            if f.startswith("CONTRACT-") and f.endswith(".md"):
                idx.setdefault(f, os.path.join(root, f))
    return idx


def exp_records():
    recs = {}
    for f in sorted(os.listdir(EXPDIR)):
        m = re.match(r"EXP-(\d{3})", f)
        if m and f.endswith(".md"):
            recs.setdefault(m.group(1), os.path.join(EXPDIR, f))
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    L = io.open(os.path.join(DB, "_index", "L2-VERDICTS.md"), encoding="utf-8").read().splitlines()
    i = next(k for k, l in enumerate(L) if l.startswith("| system | contract | types |"))
    hdr = split_row(L[i])
    ci, ri = hdr.index("contract"), hdr.index("runtime")
    reg = collections.defaultdict(set)
    for r in io.open(os.path.join(DB, "_index", "important-subsystems.tsv"), encoding="utf-8").read().splitlines()[1:]:
        f = r.split("\t")
        if len(f) > 5:
            reg[f[0]] |= set(CON.findall(f[5]))
    # verdict text per system: every section whose heading names the system id
    sect = collections.defaultdict(list)
    cur = None
    for x in L:
        if x.startswith("#"):
            ids = SID.findall(x)
            # only sections whose heading names the id AND says 'runtime' carry runtime judgements (block 257)
            cur = ids[0] if (ids and "runtime" in x.lower()) else None
        elif cur:
            sect[cur].append(x)
    cidx, recs = contracts_index(), exp_records()
    rtext = {k: io.open(p, encoding="utf-8", errors="replace").read() for k, p in recs.items()}
    by_contract = collections.defaultdict(set)
    for k, t in rtext.items():
        for c in CON.findall(t[:3000]):
            by_contract[c].add(k)
    rows = []
    for l in L[i + 2:]:
        if not l.startswith("|"):
            break
        c = split_row(l)
        m = SID.search(c[0])
        if not m or re.match(r"\**MET\b", c[ri]):
            continue
        sid = m.group(0)
        cons = set(CON.findall(c[ci])) | reg.get(sid, set())
        exps = set()
        for con in cons:
            p = cidx.get(con)
            if p:
                exps |= set(EXP.findall(io.open(p, encoding="utf-8", errors="replace").read()))
            exps |= by_contract.get(con, set())
        exps &= set(rtext)
        # 2026-09-25 (OPUS, block 257): a runtime judgement is a citation in the RUNTIME cell (or a runtime-headed
        # section), not anywhere in the row - S-31's EXP-140 sat in the types cell and was masked. Citations are
        # read in both forms the verdicts use: 'EXP-151' and the short '(151)' / '150-161' / '192-195'.
        judged_text = c[ri] + "\n" + "\n".join(sect.get(sid, []))
        cited = set(EXP.findall(judged_text))
        for a_, b_ in re.findall(r"\b(\d{3})\s*[-–]\s*(?:EXP-)?(\d{3})\b", judged_text):
            if int(a_) <= int(b_) <= int(a_) + 60:
                cited |= {"%03d" % n for n in range(int(a_), int(b_) + 1)}
        for grp in re.findall(r"\((\d{3}(?:\s*/\s*\d{3})*)\)", judged_text):
            cited |= set(re.findall(r"\d{3}", grp))
        unj = sorted(e for e in exps if e not in cited)
        live = sorted(e for e in unj if re.search(r"live_game:\s*true", rtext[e]))
        stub = sorted(e for e in unj if re.search(r"stub|scripted|intercept", rtext[e], re.I))
        rows.append((sid, re.sub(r"\s+", " ", c[ri])[:24], len(cons), len(exps), unj, live, stub))
    rows.sort(key=lambda r: (-len(r[4]), r[0]))
    print("runtime cells not MET: %d   with UNJUDGED executed records: %d   unjudged records in all: %d" % (
        len(rows), sum(1 for r in rows if r[4]), sum(len(r[4]) for r in rows)))
    for r in rows:
        if not r[4]:
            continue
        print("%-5s %-24s contracts %2d  EXPs %3d  unjudged %2d: %s%s%s" % (
            r[0], r[1], r[2], r[3], len(r[4]), ",".join(r[4]),
            ("  | live: " + ",".join(r[5])) if r[5] else "",
            ("  | no-stub: " + ",".join(sorted(set(r[4]) - set(r[6])))) if set(r[4]) - set(r[6]) else ""))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("system\truntime\tcontracts\texps\tunjudged\tlive\tdiscloses_stubs\n")
            for r in rows:
                f.write("\t".join([r[0], r[1], str(r[2]), str(r[3]), ",".join(r[4]), ",".join(r[5]), ",".join(r[6])]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
