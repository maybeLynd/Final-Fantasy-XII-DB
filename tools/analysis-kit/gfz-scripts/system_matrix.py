#!/usr/bin/env python3
"""system_matrix.py - the major-system L1/L2 steering matrix.

One row per registered major system (the NN-Category directories). Each column answers one
obligation of the L1+L2 reconstruction-grade bar from inputs the corpus already holds, and
says which instrument's rule computed it so the figures cannot drift from the scorers:

    semantic/mechanism     -> fn_A/B/C/D, reusing check_dispositions.evaluate per category
                              (attribution, NOT a partition: a body cited by two systems
                              counts in both)
    types/ABI              -> types.tsv documents column -> category; unobserved extent
                              per type via the check_unread_vs_census name class
    contract coverage      -> `contract:` frontmatter docs, readiness ladder, audit.passes
    runtime evidence       -> evidence_tier >= 2 docs and _experiments/ references
    questions/contradict.  -> OPEN-QUESTIONS.md rows classified by check_questions.classify
                              and attributed through `../NN-` links; per-doc unticked boxes
    L1 / L2 verdicts       -> PROVISIONAL rule columns, printed in the header - steering
                              labels, not gates

    python system_matrix.py [--tsv OUT] [--md OUT]
"""
import argparse
import bisect
import collections
import io
import os
import re
import sys

import kit_paths as KP
import check_dispositions as cd
import check_questions as cq

CITE = cd.CITE
UNREAD = re.compile(r"^(unobserved|unknown|unread|pad)", re.I)
CAT_DIR = re.compile(r"^\d\d-")
CAT_LINK = re.compile(r"\.\./(\d\d-[A-Za-z0-9-]+)/")
UNBOX = re.compile(r"^\s*-\s*\[ \]", re.M)


def categories(db):
    return sorted(d for d in os.listdir(db)
                  if CAT_DIR.match(d) and os.path.isdir(os.path.join(db, d)))


def cat_docs(db, cat):
    root = os.path.join(db, cat)
    out = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if fn.endswith(".md") and fn != "README.md":
                out.append(os.path.join(dp, fn))
    return sorted(out)


def fm_key(fm, key):
    m = re.search(r"^%s:\s*(.*)$" % key, fm, re.M)
    return m.group(1).strip() if m else ""


def load_sizes():
    sizes = {}
    import csv
    for r in csv.DictReader(io.open(os.path.join(KP.WORK, "graph", "functions.tsv"),
                                    encoding="utf-8", newline=""), delimiter="\t"):
        try:
            sizes[int(r["entry"], 16)] = int(r["body_bytes"])
        except (ValueError, KeyError):
            continue
    return sizes


def load_types(db):
    """type -> (size, documents, unobserved_extent)."""
    import csv
    types = {}
    for r in csv.DictReader(io.open(os.path.join(db, "_types", "types.tsv"),
                                    encoding="utf-8", newline=""), delimiter="\t"):
        try:
            types[r["type"]] = [int(r["size"], 0), r.get("documents", ""), 0]
        except (ValueError, KeyError):
            types[r["type"]] = [None, r.get("documents", ""), 0]
    for r in csv.DictReader(io.open(os.path.join(db, "_types", "fields.tsv"),
                                    encoding="utf-8", newline=""), delimiter="\t"):
        if r["type"] in types and UNREAD.match(r.get("name", "")):
            try:
                types[r["type"]][2] += int(r["size"], 0)
            except ValueError:
                pass
    return types


def open_questions_by_cat(db):
    """question id -> status, attributed to categories through `../NN-` links."""
    p = os.path.join(db, "_index", "OPEN-QUESTIONS.md")
    t = io.open(p, encoding="utf-8", errors="replace").read()
    per = collections.Counter()
    for m in re.finditer(r"^\|\s*(%s)\s*\|(.*)$" % cq.QID, t, re.M):
        st, _ = cq.classify(m.group(2))
        if st != "OPEN":
            continue
        cats = set(CAT_LINK.findall(m.group(2)))
        for c in cats or {"(unattributed)"}:
            per[c] += 1
    return per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv")
    ap.add_argument("--md")
    a = ap.parse_args()

    db = KP.DB
    sizes = load_sizes()
    types = load_types(db)
    oq = open_questions_by_cat(db)

    # type -> category via its documents column (doc paths inside the category dir)
    type_cat = collections.defaultdict(list)
    for t, (sz, docs_s, un) in types.items():
        cats = set(re.findall(r"(\d\d-[A-Za-z0-9-]+)/", docs_s))
        for c in cats:
            type_cat[c].append(t)

    rows = []
    for cat in categories(db):
        paths = cat_docs(db, cat)
        ev = cd.evaluate(db, sizes, paths=paths) if paths else None
        stat = collections.Counter()
        contracts = {"n": 0, "ready": 0, "passes": 0}
        tier2 = 0
        exp_refs = 0
        unbox = 0
        sysdocs = 0
        for p in paths:
            t = io.open(p, encoding="utf-8", errors="replace").read()
            fm = cd.frontmatter(t)
            s = fm_key(fm, "status") or "(none)"
            stat[s.split(" ")[0].split("—")[0].strip() or "(none)"] += 1
            if fm_key(fm, "system"):
                sysdocs += 1
            if fm_key(fm, "contract"):
                contracts["n"] += 1
                if fm_key(fm, "readiness") in ("CONTRACT READY",
                                             "BEHAVIORALLY UNDERSTOOD"):
                    contracts["ready"] += 1
                if re.search(r"passes:\s*[1-9]", fm):
                    contracts["passes"] += 1
            try:
                if int(fm_key(fm, "evidence_tier") or "0") >= 2:
                    tier2 += 1
            except ValueError:
                pass
            if "_experiments/" in t:
                exp_refs += 1
            unbox += len(UNBOX.findall(t))

        ty = type_cat.get(cat, [])
        ty_unob = sum(types[t][2] for t in ty)
        reopened = stat.get("REOPENED", 0)
        partial = stat.get("PARTIAL", 0)
        bearing = sum(v for k, v in stat.items() if k != "(none)")  # rough; refine below
        # evidence-bearing is the honest doc count for the semantic gate
        nbear = sum(1 for p in paths
                    if cd._bearing(io.open(p, encoding="utf-8", errors="replace").read()))

        # PROVISIONAL verdict rules (steering labels, printed in the header):
        #   L1 = the system has at least one evidence-bearing doc and nothing REOPENED
        #   L2 = L1, plus at least one ready contract AND at least one declared type
        #        AND no more open attributed questions than PARTIAL docs
        l1 = nbear > 0 and reopened == 0
        l2 = l1 and contracts["ready"] > 0 and len(ty) > 0 and oq.get(cat, 0) <= partial
        rows.append((cat, len(paths), sysdocs, nbear, stat.get("DOCUMENTED", 0),
                     partial, reopened, stat.get("(none)", 0),
                     ev["A"] if ev else 0, ev["B"] if ev else 0,
                     ev["C"] if ev else 0, ev["D"] if ev else 0,
                     contracts["n"], contracts["ready"], contracts["passes"],
                     len(ty), ty_unob, tier2, exp_refs, oq.get(cat, 0), unbox,
                     "L2" if l2 else ("L1" if l1 else "below-L1")))

    hdr = ("category", "docs", "sys_docs", "bearing", "documented", "partial",
           "reopened", "no_status", "fn_A", "fn_B", "fn_C", "fn_D",
           "contracts", "contract_ready", "contract_passes",
           "types", "type_unobserved_B", "tier2plus_docs", "exp_citing_docs",
           "open_questions", "unticked_boxes", "verdict")
    if a.tsv:
        with io.open(a.tsv, "w", encoding="utf-8", newline="") as f:
            f.write("\t".join(hdr) + "\n")
            for r in rows:
                f.write("\t".join(str(x) for x in r) + "\n")
    if a.md:
        import subprocess
        try:
            rev = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                          cwd=KP.ROOT).decode().strip()
        except Exception:
            rev = "(unknown)"
        with io.open(a.md, "w", encoding="utf-8") as f:
            f.write("# System matrix — major-system L1/L2 steering surface\n\n"
                    "<!-- GENERATED by gfz-scripts/system_matrix.py -- do not edit by hand. -->\n\n"
                    "Input revision `%s`, board raw state at generation time. One row per\n"
                    "registered major system. `fn_*` columns are ATTRIBUTION (a body cited by\n"
                    "two systems counts in both), not a partition. `verdict` is a PROVISIONAL\n"
                    "steering label: L1 = >=1 evidence-bearing doc & 0 REOPENED; L2 = L1 +\n"
                    "ready contract + declared type + open questions <= PARTIAL docs. It is\n"
                    "not the final-audit bar.\n\n" % rev)
            f.write("| " + " | ".join(hdr) + " |\n")
            f.write("|" + "---|" * len(hdr) + "\n")
            for r in rows:
                f.write("| " + " | ".join(str(x) for x in r) + " |\n")

    print("SYSTEM MATRIX - %d categories, %d census bodies" % (len(rows), len(sizes)))
    print("verdicts are PROVISIONAL steering labels: L1 = >=1 evidence-bearing doc & 0 "
          "REOPENED; L2 = L1 + ready contract + declared type + open questions <= PARTIAL")
    print()
    h = "%-38s %4s %4s %5s %5s %5s %5s %5s %5s %5s %4s %5s %6s %5s %5s %8s"
    print(h % ("category", "docs", "bear", "A", "B", "C", "D", "ctrs", "rdy", "types",
               "unobsB", "tier2", "exp", "openQ", "unbox", "verdict"))
    for r in rows:
        print(h % (r[0][:38], r[1], r[3], r[8], r[9], r[10], r[11], r[12], r[13],
                   r[15], r[16], r[17], r[18], r[19], r[20], r[21]))


if __name__ == "__main__":
    main()
