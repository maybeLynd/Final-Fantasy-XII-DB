#!/usr/bin/env python3
"""check_propagation.py - FINAL-AUDIT-PROTOCOL pass 24, which had no tool.

Pass 24: *"for every correction ever made, verify every downstream citer was reopened"*, failing if
**any document still rests on an overturned claim**. Until now that was a read-every-line pass over
the whole corpus against a correction history nobody had collected.

It does not have to be. The board already keeps a structured, machine-readable correction registry:
every `kind: contradiction` task carries `original_claim` - the sentence that was overturned - and
`affected_documents` - where the correction was applied. 119 of them, every one with both fields.
This sweeps the first against the corpus and subtracts the second.

What it looks for
-----------------
The QUOTED SPANS inside `original_claim`. When a contradiction is filed properly it quotes the exact
retracted sentence, and a quoted sentence surviving verbatim in a document that the correction never
touched is the precise shape of a propagation failure. Bare addresses and offsets are deliberately
NOT used: `004B1190` appearing elsewhere is not a stale claim, it is an address that still exists,
and searching for those would bury the real finding under thousands of legitimate citations.

Three verdicts, because a hit is not automatically a defect
-----------------------------------------------------------
    EXPECTED     the hit is inside a document `affected_documents` names - the correction lives there
    QUOTED       the hit sits near a retraction marker - a page quoting what it is retracting
    SURVIVOR     everything else: a document repeating an overturned sentence, untouched  <- the pass

SURVIVOR is the only number that means anything, and it is still a TRIAGE result: a human reads each
one. This tool finds candidates; it does not decide.
"""
import argparse
import hashlib
import io
import json
import os
import re
import sys

# ---- the disposition registry (PROPOSED 2026-09-15, OPUS, pending SWE2-AUDIT-SPEC review) --------
#
# WHY. This tool derives its verdicts from the board and records nothing, so a SURVIVOR that has been
# read and found false is reported again on every run. At HEAD 54b14368 that is seven rows, all read
# and all false (five are one stock subtree sentence matching five unrelated subtrees; two are
# headings the WM-COUNTS repair made true by moving a member). Under "thirty consecutive clean complete
# runs" that is thirty re-adjudications of the same seven rows, and thirty chances to rule one
# differently and reset the streak on a disagreement rather than a defect. Pass 28 does not have this
# problem, because check_doc_claims.py reads a registry. This gives pass 24 the same thing, and no more.
#
# WHAT A ROW IS. `_index/candidates/propagation-dispositions.tsv`, one row per (contradiction, document,
# hit). A row clears a survivor ONLY when every one of these still matches at run time:
#   contradiction  the task id
#   document       the corpus-relative path
#   span_sha       sha256 of the normalised quoted span
#   claim_sha      sha256 of the contradiction's original_claim + affected_documents, normalised.
#                  AMENDING THE CONTRADICTION INVALIDATES EVERY DISPOSITION UNDER IT.
#   context_sha    sha256 of the normalised neighbourhood the marker test reads (the hit line +-3).
#                  EDITING THE TEXT AROUND THE HIT INVALIDATES THE DISPOSITION.
# and the row is REVIEWED: `author` and `reviewer` are both board identities and differ. A row with no
# reviewer, or reviewed by its author, clears nothing and is counted as UNREVIEWED.
#
# WHAT IT NEVER DOES. A cleared survivor is printed as DISPOSED with its verdict and reviewer on every
# run - visible, not re-adjudicated. A row whose hashes no longer match is printed as STALE and its
# hit counts as a SURVIVOR again. A row matching no current hit is printed as ORPHANED; it clears
# nothing and is left for its author to delete.
REGISTRY = os.path.join("_index", "candidates", "propagation-dispositions.tsv")
REG_COLS = ["contradiction", "document", "span_sha", "claim_sha", "context_sha", "verdict",
            "reason", "author", "reviewer", "reviewed_at"]
VERDICTS = ("FALSE-MATCH", "TRUE-AS-WRITTEN")
IDENTITIES = {"FABLE", "OPUS", "ASTRA", "SWE2-AUDIT-SEM", "SWE2-AUDIT-SPEC", "SWE2-CONTRACT",
              "SWE2-DATA", "SWE2-EC7", "SWE2-FRONTIER", "SWE2-ORACLE", "SWE2-STRUCT"}


def sha(s):
    return hashlib.sha256(norm(s).encode("utf-8")).hexdigest()


def claim_sha(task):
    return sha((task.get("original_claim") or "") + "\n" + (task.get("affected_documents") or ""))


def load_registry(db):
    """-> (usable {(cid, doc, span_sha): row}, unreviewed [rows], malformed [(line, why)])."""
    p = os.path.join(db, REGISTRY)
    usable, unreviewed, malformed = {}, [], []
    if not os.path.isfile(p):
        return usable, unreviewed, malformed
    for n, line in enumerate(io.open(p, encoding="utf-8"), 1):
        line = line.rstrip("\r\n")
        if not line or line.startswith("#"):
            continue
        cells = line.split("\t")
        if cells == REG_COLS:
            continue
        if len(cells) != len(REG_COLS):
            malformed.append((n, "expected %d columns, got %d" % (len(REG_COLS), len(cells))))
            continue
        row = dict(zip(REG_COLS, cells))
        if row["verdict"] not in VERDICTS:
            malformed.append((n, "verdict %r is not one of %s" % (row["verdict"], VERDICTS)))
            continue
        if not row["reason"].strip():
            malformed.append((n, "no reason"))
            continue
        if (row["author"] not in IDENTITIES or row["reviewer"] not in IDENTITIES
                or row["author"] == row["reviewer"] or not row["reviewed_at"].strip()):
            unreviewed.append(row)
            continue
        usable[(row["contradiction"], row["document"].replace("\\", "/"), row["span_sha"])] = row
    return usable, unreviewed, malformed

MIN_SPAN = 24          # below this, quoted fragments are too generic to mean anything

# The single-quote arm needs guarding: an apostrophe inside a POSSESSIVE or a contraction is not an
# opening delimiter. Without the guards below, `the record's fifth dword is that kind' of thing`
# yields the span "s fifth dword is that kind", which begins mid-word and matches half the corpus.
# So an opening ' must not follow a word character, and a closing ' must not precede one.
QUOTED = re.compile(
    r"(?<![A-Za-z0-9])'([^']{%d,200})'(?![A-Za-z0-9])"
    r"|\"([^\"]{%d,200})\""
    r"|`([^`]{%d,200})`" % (MIN_SPAN, MIN_SPAN, MIN_SPAN))
PATHS = re.compile(r"Database/FFXII TZA/[^\s;,()]+?\.(?:md|tsv)")
MARKER = re.compile(
    r"RETRACT|SUPERSED|CORRECT|WITHDRAWN|OVERTURN|was wrong|no longer|previously|"
    r"~~|formerly|earlier reading|struck", re.I)
SKIP_DIRS = {".git", "_templates", "_inbox"}
WS = re.compile(r"\s+")


def norm(s):
    return WS.sub(" ", s).strip()


def spans_from(task):
    """The quoted, overturned sentences inside one contradiction's original_claim."""
    out = []
    for m in QUOTED.finditer(task.get("original_claim") or ""):
        for g in m.groups():
            if g and len(norm(g)) >= MIN_SPAN:
                out.append(norm(g))
    return out


def corpus(db):
    for root, dirs, names in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in sorted(names):
            if n.endswith((".md", ".tsv")):
                p = os.path.join(root, n)
                try:
                    yield p, open(p, encoding="utf-8").read()
                except (OSError, UnicodeDecodeError):
                    continue


def locate(text, span, window=3):
    """Line number of the first line containing the span, plus its NEIGHBOURHOOD.

    The neighbourhood is what gets tested for a retraction marker, and it has to be: a page that
    quotes a claim while retracting it usually puts the marker in the surrounding sentence, not on
    the quoted line. The first version of this checked only the hit line and duly reported
    `world-loot-pickups...md` as a survivor for repeating "a tuning slot currently set to unity" -
    when the sentence one line above reads "I had spent the morning publishing - and then RETRACTING
    - the claim that ...". The page was recording the correction, which is the opposite of resting
    on it.
    """
    lines = text.splitlines()
    head = span[:40]
    for i, line in enumerate(lines, 1):
        if head in norm(line):
            lo, hi = max(0, i - 1 - window), min(len(lines), i + window)
            return i, norm(" ".join(lines[lo:hi]))

    # The span straddles a line break, so no single line holds its head. Returning an empty
    # neighbourhood here meant the marker test never ran and the hit fell through to SURVIVOR -
    # which is how a wrapped quotation inside a retraction was reported as a stale claim. Fall back
    # to a character window in the normalised document.
    flat = norm(text)
    at = flat.find(span)
    if at < 0:
        return None, ""
    return None, flat[max(0, at - 320):at + len(span) + 320]


DATED_HEAD = re.compile(r"^#{1,4}\s.*20\d\d-\d\d-\d\d")


def dated_scope(text):
    """-> set of 1-based line numbers that sit under a dated heading.

    Sticky down the heading tree: a dated entry contains undated sub-headings ("### What was
    deliberately not claimed"), and resetting on every heading would turn the flag off immediately.
    A section stays dated until a heading at the SAME OR SHALLOWER level says otherwise.
    """
    out, in_dated, level = set(), False, 0
    for i, line in enumerate(text.split("\n"), 1):
        m = re.match(r"^(#{1,6})\s", line)
        if m:
            lv = len(m.group(1))
            if DATED_HEAD.match(line):
                in_dated, level = True, lv
            elif in_dated and lv <= level:
                in_dated, level = False, 0
        if in_dated:
            out.add(i)
    return out


def sweep(db, board, registry=None):
    tasks = [t for t in board["tasks"] if t.get("kind") == "contradiction"]
    docs = list(corpus(db))
    normed = [(p, norm(t)) for p, t in docs]
    raw = dict(docs)
    registry = registry or {}
    disposed, stale, seen_keys = [], [], set()

    counts = {"EXPECTED": 0, "QUOTED": 0, "DATED": 0, "DISPOSED": 0, "SURVIVOR": 0}
    dated_lines = {p: dated_scope(raw[p]) for p, _ in normed}
    survivors = []
    used = 0
    for t in tasks:
        spans = spans_from(t)
        if not spans:
            continue
        used += 1
        affected = set(PATHS.findall(t.get("affected_documents") or ""))
        affected = {a.replace("/", os.sep) for a in affected}
        for span in spans:
            for p, body in normed:
                if span not in body:
                    continue
                rel = os.path.relpath(p, db)
                if any(rel.endswith(a.split("FFXII TZA" + os.sep)[-1]) for a in affected):
                    counts["EXPECTED"] += 1
                    continue
                line_no, line = locate(raw[p], span)
                if MARKER.search(line):
                    counts["QUOTED"] += 1
                    continue
                # A SECTION UNDER A DATED HEADING IS A RECORD OF THAT DATE, not a live claim.
                # Both survivors this test had on 2026-09-14 were of exactly this shape: the same
                # quoted §13 text, once in `AUDIT-LOG.md` under "## 2026-09-08 - a checker validated
                # on the failure it was built for", and once in `COVERAGE.md` under "## 2026-09-08 -
                # the fourth contract...". Neither is a page repeating an overturned sentence - each
                # is a page QUOTING what the contract said on the day it was examined, which is the
                # log and the coverage page doing their job.
                #
                # This is the same structural rule `check_index_figures` and `check_dimension_figures`
                # use, applied here rather than kept as two named waivers: a rule generalises to the
                # next dated entry, a waiver list does not.
                if line_no is not None and line_no in dated_lines.get(p, ()):
                    counts["DATED"] += 1
                    continue
                key = (t["id"], rel.replace(os.sep, "/"), sha(span))
                row = registry.get(key)
                if row is not None:
                    seen_keys.add(key)
                    if row["claim_sha"] == claim_sha(t) and row["context_sha"] == sha(line):
                        counts["DISPOSED"] += 1
                        disposed.append((t["id"], rel, line_no, span, row))
                        continue
                    stale.append((t["id"], rel, line_no, span, row,
                                  "claim amended" if row["claim_sha"] != claim_sha(t)
                                  else "text around the hit changed"))
                counts["SURVIVOR"] += 1
                survivors.append((t["id"], rel, line_no, span, sha(span), claim_sha(t), sha(line)))
    orphaned = [r for k, r in registry.items() if k not in seen_keys]
    return len(tasks), used, counts, survivors, disposed, stale, orphaned


def self_test():
    """A checker that cannot demonstrate a known positive is not evidence of anything."""
    board = {"tasks": [{
        "id": "TEST-CONTRA", "kind": "contradiction",
        "original_claim": "the page said 'the widget pool holds exactly 112 fixed slots' and it does not",
        "affected_documents": "Database/FFXII TZA/16-UI/fixed.md"}]}
    import tempfile
    d = tempfile.mkdtemp()
    ui = os.path.join(d, "16-UI")
    os.makedirs(ui)
    # the corrected page - names the claim while retracting it
    open(os.path.join(ui, "fixed.md"), "w", encoding="utf-8").write(
        "RETRACTED: the widget pool holds exactly 112 fixed slots\n")
    # an untouched downstream page still asserting it  <- must be found
    open(os.path.join(ui, "stale.md"), "w", encoding="utf-8").write(
        "As established, the widget pool holds exactly 112 fixed slots.\n")
    # a page that quotes it while marking it superseded  <- must NOT be found
    open(os.path.join(ui, "quoting.md"), "w", encoding="utf-8").write(
        "SUPERSEDED claim: the widget pool holds exactly 112 fixed slots\n")
    _n, used, counts, surv, _d, _s, _o = sweep(d, board)
    ok = (used == 1 and counts["SURVIVOR"] == 1
          and surv and surv[0][1].endswith("stale.md"))
    print("self-test 1 (known positive): %s  (used %d, survivors %d: %s)"
          % ("PASS" if ok else "FAIL", used, counts["SURVIVOR"], [s[1] for s in surv]))
    if not ok:
        return 1

    # The registry's own controls. Each is a way a disposition could clear something it should not.
    cid, rel, _ln, span, span_sha, c_sha, ctx_sha = surv[0]
    doc = rel.replace(os.sep, "/")

    def reg(**over):
        row = dict(contradiction=cid, document=doc, span_sha=span_sha, claim_sha=c_sha,
                   context_sha=ctx_sha, verdict="FALSE-MATCH", reason="control", author="OPUS",
                   reviewer="SWE2-AUDIT-SPEC", reviewed_at="2026-09-15")
        row.update(over)
        os.makedirs(os.path.join(d, "_index", "candidates"), exist_ok=True)
        with io.open(os.path.join(d, REGISTRY), "w", encoding="utf-8") as fh:
            fh.write("\t".join(REG_COLS) + "\n" + "\t".join(row[c] for c in REG_COLS) + "\n")
        usable, unrev, bad = load_registry(d)
        return sweep(d, board, usable), unrev, bad

    results = []
    (_n, _u, c, s, disp, st, orph), unrev, bad = reg()
    results.append(("a reviewed, matching row clears the survivor and shows it as DISPOSED",
                    c["SURVIVOR"] == 0 and c["DISPOSED"] == 1 and len(disp) == 1))
    (_n, _u, c, s, disp, st, orph), unrev, bad = reg(reviewer="OPUS")
    results.append(("a row reviewed by its own author clears nothing",
                    c["SURVIVOR"] == 1 and len(unrev) == 1))
    (_n, _u, c, s, disp, st, orph), unrev, bad = reg(reviewer="")
    results.append(("an unreviewed row clears nothing", c["SURVIVOR"] == 1 and len(unrev) == 1))
    (_n, _u, c, s, disp, st, orph), unrev, bad = reg(context_sha="0" * 64)
    results.append(("changed text around the hit makes the row STALE and the survivor returns",
                    c["SURVIVOR"] == 1 and len(st) == 1 and st[0][5] == "text around the hit changed"))
    (_n, _u, c, s, disp, st, orph), unrev, bad = reg(claim_sha="0" * 64)
    results.append(("an amended contradiction makes the row STALE",
                    c["SURVIVOR"] == 1 and len(st) == 1 and st[0][5] == "claim amended"))
    (_n, _u, c, s, disp, st, orph), unrev, bad = reg(span_sha="1" * 64)
    results.append(("a row for a hit that no longer exists is ORPHANED and clears nothing",
                    c["SURVIVOR"] == 1 and len(orph) == 1))
    (_n, _u, c, s, disp, st, orph), unrev, bad = reg(verdict="LOOKS FINE")
    results.append(("an unknown verdict is malformed and clears nothing",
                    c["SURVIVOR"] == 1 and len(bad) == 1))
    for why, good in results:
        print("self-test registry: %s  %s" % ("PASS" if good else "FAIL", why))
    return 0 if all(g for _w, g in results) else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--board")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--gate", action="store_true",
                    help="exit 1 on any SURVIVOR, STALE or malformed registry row")
    ap.add_argument("--emit-rows", action="store_true",
                    help="print an unreviewed registry row for every survivor (author fills verdict)")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not (a.db and a.board):
        return ap.error("--db and --board, or --self-test")

    board = json.load(open(a.board, encoding="utf-8"))
    usable, unreviewed, malformed = load_registry(a.db)
    total, used, counts, survivors, disposed, stale, orphaned = sweep(a.db, board, usable)
    print("FINAL-AUDIT-PROTOCOL pass 24 - propagation sweep")
    print("  registry %s: %d reviewed row(s), %d unreviewed (clear nothing), %d malformed"
          % (REGISTRY, len(usable), len(unreviewed), len(malformed)))
    print("  %d contradiction tasks on the board; %d carry a quoted span of >=%d chars"
          % (total, used, MIN_SPAN))
    print("    EXPECTED  %4d   hit inside a document the correction names" % counts["EXPECTED"])
    print("    QUOTED    %4d   hit beside a retraction marker - a page quoting what it retracts"
          % counts["QUOTED"])
    print("    DATED     %4d   hit under a dated heading - a log or a page recording what it"
          % counts["DATED"])
    print("                      found on that date, not a live claim. REPORTED, never hidden:")
    print("                      absorbing preserved history silently is the failure the")
    print("                      evidence standard forbids, and it is what a bare 0 would do.")
    print("    DISPOSED  %4d   read, ruled false by an author and an independent reviewer, and"
          % counts["DISPOSED"])
    print("                      unchanged since - listed below on every run, never re-adjudicated")
    print("    STALE     %4d   a disposition whose claim or surrounding text changed - its hit"
          % len(stale))
    print("                      is counted as a SURVIVOR again")
    print("    ORPHANED  %4d   a disposition matching no current hit - clears nothing"
          % len(orphaned))
    print("    SURVIVOR  %4d   <- the only number that matters" % counts["SURVIVOR"])
    for cid, rel, line, span, row in disposed:
        print("\n  DISPOSED %s  %s:%s\n    %r\n    %s by %s, reviewed by %s %s - %s"
              % (cid, rel, line, span[:100], row["verdict"], row["author"], row["reviewer"],
                 row["reviewed_at"], row["reason"][:160]))
    for cid, rel, line, span, row, why in stale:
        print("\n  STALE %s  %s:%s  (%s)\n    %r" % (cid, rel, line, why, span[:100]))
    for n, why in malformed:
        print("\n  MALFORMED registry line %d: %s" % (n, why))
    if a.list or a.emit_rows:
        for cid, rel, line, span, s_sha, c_sha, x_sha in survivors:
            if a.emit_rows:
                print("\t".join([cid, rel.replace(os.sep, "/"), s_sha, c_sha, x_sha,
                                 "<VERDICT>", "<reason - line %s: %s>" % (line, span[:60]),
                                 "<author>", "", ""]))
            else:
                print("\n  %s\n    %s:%s\n    %r" % (cid, rel, line, span[:150]))
    if not counts["SURVIVOR"]:
        print("\n  No document repeats an overturned sentence outside its own correction.")
        print("  The self-test demonstrates a known positive, so that is a real negative.")
    if a.gate and (counts["SURVIVOR"] or stale or malformed):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
