#!/usr/bin/env python3
"""parity_status.py - charter section 21: parity status must be explicit, per dimension.

What it does
------------
Reads the `PARITY` declaration out of every `Reconstruction/Tests/Differential/diff_*.py`
**with `ast`, never by importing** - a harness imports unicorn, opens the executable and, run
by accident, takes minutes. Then it writes `_index/PARITY-STATUS.md`: the eleven charter
section-21 dimensions against every pilot, plus the certification verdict from
`Reconstruction/PARITY-STANDARD.md` section 4.

Contract coverage is DERIVED, not declared
------------------------------------------
Each harness also carries a `CONTRACT_MAP`: one row per claim in its contract's section 15
evidence table, each marked `EXERCISED`, `PARTIAL`, `NOT EXERCISED` or `OPEN QUESTION`. This
tool re-reads the contract, **checks the map's claim strings against the table's own wording**
and reports any drift, then derives the `CONTRACT` verdict from the map. A harness whose
declared verdict disagrees with the derived one is a declaration problem.

**Only the `OPEN QUESTION` rows are excluded from the denominator**, and only because a section
15 row recording an `UNKNOWN` states a question rather than a behaviour -- there is nothing to
exercise. Every excluded row is named on the page, so the exclusion is visible rather than
quiet.

With `--run` it also **executes every harness** and parses the comparison and mismatch counts
out of the output, so the page carries measured numbers beside declared ones.

Why declared and measured are separate columns
----------------------------------------------
**A declaration is a claim.** A harness saying `STRUCTURAL: COVERED` is the harness's author
asserting the criterion is met; nothing here checks that assertion. What CAN be checked
mechanically is whether the harness still runs and still reports zero mismatches, and that is a
different fact. Printing them in one column would let a stale claim ride on a fresh run.

**A harness whose output cannot be parsed is reported as UNPARSED, never as zero.** The
six harnesses print their totals in four different shapes; a regex that quietly matched none of
them would produce a page full of confident zeroes, which is the failure this project has already
made once with a citation extractor.
"""
import argparse
import ast
import io
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# The scope markers live in parity_claim_scope.py and nowhere else - a second copy would
# drift. marker_of(why) returns a marker name when a NOT-EXERCISED row's own reason carries
# a literal phrase its author wrote to mean "this claim is about code this pilot does not
# contain or does not reach" (OPUS-REQ-SWE2-CONTRACT-PARITY-395-OF-716-IS-A-SCOPE-MEASUREMENT).
from parity_claim_scope import marker_of

# DERIVED, NOT HARDCODED. The kit lives at <root>/Database/Tools/analysis-kit/gfz-scripts,
# so four dirnames up is the checkout this script belongs to. A hardcoded path meant that
# --diff could redirect the HARNESSES to a HEAD worktree while the CONTRACTS still came
# from the dirty working tree - a run that looks HEAD-scoped and is not. On 2026-09-16
# that reported a CURRENT PARITY-STATUS.md as 1438 lines stale, on one peer's
# uncommitted refutation, and regenerating from it would have published their draft.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
DIFF = os.path.join(ROOT, "Reconstruction", "Tests", "Differential")
DB = os.path.join(ROOT, "Database", "FFXII TZA")
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")

# Charter section 21's list, in the order that section names them, with FULL-SUBSYSTEM last.
DIMENSIONS = ["CALCULATION", "STRUCTURAL", "STATE-TRANSITION", "CONTRACT", "EDGE-CASE",
              "SERIALIZATION", "RNG", "TIMING", "INTEGRATION", "PRESENTATION", "FULL-SUBSYSTEM"]
VERDICTS = ("COVERED", "NOT COVERED", "N/A")
CONTRACT_STATUSES = ("EXERCISED", "PARTIAL", "NOT EXERCISED", "OPEN QUESTION")

# Four shapes, because the harnesses were written at different times and each prints what its
# own subsystem makes sense of. Collected here rather than forced into one format: rewriting six
# working harnesses to please a reporter is the tail wagging the dog.
MISMATCH_PATS = [
    re.compile(r"^\s*mismatches\s*:\s*(\d+)\s*$", re.M),
    re.compile(r"^\s*(?:return-code|list-order)\s+mismatches\s*:\s*(\d+)\s*$", re.M),
    re.compile(r"(\d[\d,]*)\s+comparisons?,\s*(\d+)\s+mismatch", re.M),
]
# `cases` and `comparisons` are DIFFERENT NUMBERS and were briefly reported as one.
# `flag_banks` runs 918 cases against three payloads for 2,754 comparisons; `angle_wrap`
# runs 4,140 float bit patterns through two forms for 8,280. Taking whichever pattern matched
# first printed the smaller number under the larger one's label -- a wrong denominator, which
# is the error class this project exists to stop making. Both are collected, both are printed,
# and neither stands in for the other.
CASES_PAT = re.compile(r"^\s*cases\s*:\s*(\d[\d,]*)", re.M)
COMPARISONS_PAT = re.compile(r"(\d[\d,]*)\s+comparisons?\b", re.M)


def read_declaration(path):
    """The PARITY dict, by parsing the file. Nothing in the module is executed."""
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "PARITY":
            return ast.literal_eval(node.value)
    return None


# A CORRECTED CLAIM IS THE SAME CLAIM, STRUCK. This database corrects a section-15 row by
# striking it and appending the correction - `~~<claim>~~ **- REFUTED (FABLE): ...**` - which
# is exactly right for a reader and was read here as a NEW claim plus an ORPHANED map row. On
# 2026-09-16 that reported two declaration problems for diff_group_completion.py where nothing
# had drifted. 8 rows across 5 contracts already carry the shape, so this was general.
# Both sides are normalised, so a map carrying either spelling matches. The correction itself
# is NOT discarded: check_contract_map reports a struck-and-mapped claim as its own named
# condition, because a harness quietly keeping a parity verdict over a REFUTED claim is worse
# than the double count it replaces - the double count at least pointed somewhere.
STRUCK = re.compile(r"^~~(.+?)~~\s*(.*)$", re.S)


def claim_key(cell):
    """(the claim itself, the correction appended to it). Emphasis is not part of a claim."""
    c = (cell or "").strip()
    if c.startswith("**") and c.endswith("**") and len(c) > 4:
        c = c[2:-2].strip()
    m = STRUCK.match(c)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return c, ""


def read_contract_map(path):
    """The CONTRACT_MAP list, by parsing. Nothing in the module is executed."""
    tree = ast.parse(io.open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "CONTRACT_MAP":
            return ast.literal_eval(node.value)
    return None


def contract_claims(rel):
    """The first column of the contract's section 15 table, in order.

    Read from the document every time rather than cached, because the point of the cross-check
    is to notice when a contract is edited and a harness's map is not."""
    p = os.path.join(DB, rel.replace("/", os.sep))
    if not os.path.isfile(p):
        return None
    lines = [l.rstrip(chr(10)) for l in io.open(p, encoding="utf-8")]
    lo = next((i for i, l in enumerate(lines) if l.strip().startswith("## 15.")), None)
    if lo is None:
        return []
    hi = next((i for i in range(lo + 1, len(lines)) if lines[i].strip().startswith("## ")), len(lines))
    # A section 15 is a run of table rows, prose, and possibly a SECOND table with its own header
    # (the field-music contract lists a loader's three call sites in one). Rows belong to the
    # evidence table when their run is headed `claim` or has no header at all (the evidence table
    # resuming after prose); a run headed anything else is skipped whole. Reading every table as
    # claims had reported the nested table's header and first-column cells as missing claims -
    # 4 of 7 "missing" rows were noise (OPUS-CONTRA-FIELDMUSIC-S15-DOUBLE, 2026-09-12). Claim
    # strings are compared with surrounding emphasis stripped, so a bolded row is the same claim.
    def is_sep(t):
        return t.startswith("|") and set(t) <= set("|-: ")
    rows, i = [], lo + 1
    while i < hi:
        t = lines[i].strip()
        if not t.startswith("|"):
            i += 1
            continue
        header = None
        if i + 1 < hi and is_sep(lines[i + 1].strip()):
            header = [c.strip() for c in t.strip("|").split("|")][0]
            i += 2
        keep = header in (None, "claim")
        while i < hi and lines[i].strip().startswith("|"):
            t = lines[i].strip()
            if keep and not is_sep(t):
                cells = [c.strip() for c in t.strip("|").split("|")]
                if cells and cells[0] and cells[0] != "claim":
                    rows.append(claim_key(cells[0]))
            i += 1
    return rows


def derive_contract(cmap):
    """Charter section 21's CONTRACT dimension, computed from the map."""
    if cmap is None:
        return (None, None)
    if not cmap:
        return ("NOT COVERED", "this subsystem has no behavioural contract at all")
    testable = [r for r in cmap if r[1] != "OPEN QUESTION"]
    ex = [r for r in testable if r[1] == "EXERCISED"]
    if testable and len(ex) == len(testable):
        return ("COVERED",
                "all %d testable claims of the contract's %d section-15 rows are exercised; the "
                "other %d record open questions" % (len(testable), len(cmap),
                                                    len(cmap) - len(testable)))
    gaps = [r[0] for r in testable if r[1] != "EXERCISED"]
    sc = sum(1 for r in testable if r[1] != "EXERCISED" and marker_of(r[2]))
    scope_note = (" (%d of the unexercised carry an out-of-pilot-scope marker -- "
                  "integration work, not test cases)" % sc) if sc else ""
    return ("NOT COVERED",
            "%d of %d testable claims exercised, of the contract's %d section-15 rows (%d record "
            "open questions)%s; unexercised: %s"
            % (len(ex), len(testable), len(cmap), len(cmap) - len(testable), scope_note,
               "; ".join(gaps)))


def check_contract_map(name, decl, cmap):
    """The map against the contract it claims to map, and against the declared verdict."""
    problems = []
    rel = decl.get("contract")
    if cmap is None:
        problems.append("%s: no CONTRACT_MAP -- the CONTRACT verdict is asserted, not derived"
                        % name)
        return problems
    for i, row in enumerate(cmap):
        if len(row) != 3:
            problems.append("%s: CONTRACT_MAP row %d is not (claim, status, why)" % (name, i))
        elif row[1] not in CONTRACT_STATUSES:
            problems.append("%s: CONTRACT_MAP status %r is not one of %s"
                            % (name, row[1], CONTRACT_STATUSES))
        elif not row[2].strip():
            problems.append("%s: CONTRACT_MAP row %r carries no reason" % (name, row[0]))
    if not rel:
        if cmap:
            problems.append("%s: declares no contract but maps %d claim(s)" % (name, len(cmap)))
        return problems
    claims = contract_claims(rel)
    if claims is None:
        problems.append("%s: contract %s not found" % (name, rel))
        return problems
    mapped = [claim_key(r[0])[0] for r in cmap]
    struck = [(c, ann) for c, ann in claims if ann]
    claims = [c for c, _ in claims]
    # A claim the contract has STRUCK, which this harness still maps and still carries a
    # parity verdict for. Reported rather than matched away: the verdict may well still be
    # the right parity answer - "no run establishes an absence" survives the absence being
    # refuted - but that is a judgement for whoever owns the harness, not for a matcher.
    # ONLY THE ONES THE HARNESS HAS NOT NOTICED. A row demoted to OPEN QUESTION with its
    # reason recording the withdrawal is the CORRECT handling - derive_contract already
    # excludes it from testable claims, so nothing downstream credits it - and reporting it
    # would teach readers to skip this line. A struck claim still carrying EXERCISED or
    # NOT EXERCISED is a live parity verdict over a claim the contract has withdrawn.
    status_of = dict((claim_key(r[0])[0], r[1]) for r in cmap if len(r) == 3)
    for c, ann in struck:
        if status_of.get(c, "OPEN QUESTION") != "OPEN QUESTION":
            problems.append("%s: section-15 claim STRUCK but still verdicted %s: %s -- %s"
                            % (name, status_of[c], c, ann))
    if mapped != claims:
        # Wording drift is the failure this check exists for: a contract row reworded, or a
        # claim added, leaves a map that still LOOKS complete.
        missing = [c for c in claims if c not in mapped]
        extra = [c for c in mapped if c not in claims]
        if missing:
            problems.append("%s: %d section-15 claim(s) not in CONTRACT_MAP: %s"
                            % (name, len(missing), "; ".join(missing)))
        if extra:
            problems.append("%s: %d CONTRACT_MAP row(s) match no section-15 claim: %s"
                            % (name, len(extra), "; ".join(extra)))
        if not missing and not extra:
            problems.append("%s: CONTRACT_MAP is in a different order from section 15" % name)
    derived = derive_contract(cmap)[0]
    declared = decl["dimensions"].get("CONTRACT", ("", ""))[0]
    if derived != declared:
        problems.append("%s: CONTRACT declared %s but the map derives %s"
                        % (name, declared, derived))
    return problems


def validate(name, decl):
    """Every dimension present exactly once, every verdict legal, every non-COVERED with a reason."""
    problems = []
    dims = decl.get("dimensions", {})
    for d in DIMENSIONS:
        if d not in dims:
            problems.append("%s: dimension %s not declared" % (name, d))
    for d in dims:
        if d not in DIMENSIONS:
            problems.append("%s: %s is not one of charter section 21's dimensions" % (name, d))
    for d, v in sorted(dims.items()):
        verdict, reason = (v + ("",))[:2] if isinstance(v, tuple) else (v, "")
        if verdict not in VERDICTS:
            problems.append("%s/%s: verdict %r is not one of %s" % (name, d, verdict, VERDICTS))
        if verdict != "COVERED" and not reason.strip():
            # Charter section 21 again: a label with no statement of what is unproven is the
            # vague label the section forbids.
            problems.append("%s/%s: %s with no reason" % (name, d, verdict))
    return problems


def run_harness(name, exe, timeout):
    driver = os.path.join(DIFF, name.replace("diff_", "").replace(".py", "") + "_driver.exe")
    cmd = [sys.executable, os.path.join(DIFF, name), "--exe", exe, "--driver", driver]
    try:
        p = subprocess.run(cmd, cwd=DIFF, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return ("TIMEOUT", None, None)
    out = (p.stdout or "") + (p.stderr or "")
    if p.returncode != 0:
        return ("EXIT %d" % p.returncode, None, None)
    mism = None
    for pat in MISMATCH_PATS:
        hits = pat.findall(out)
        if hits:
            vals = [int(h[-1] if isinstance(h, tuple) else h) for h in hits]
            mism = max(vals) if mism is None else max(mism, max(vals))
    def num(pat):
        m = pat.search(out)
        return int(m.group(1).replace(",", "")) if m else None
    cases, comps = num(CASES_PAT), num(COMPARISONS_PAT)
    if mism is None or (cases is None and comps is None):
        return ("UNPARSED", (cases, comps), mism)
    return ("ok", (cases, comps), mism)


def main():
    global ROOT, DIFF, DB          # rebound from --root below, before anything reads them
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT,
                    help="checkout to read harnesses AND contracts from; point it at a HEAD worktree for a HEAD-scoped run")
    ap.add_argument("--diff", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--run", action="store_true", help="execute every harness and measure")
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    # EVERY path follows --root together, or the run is half one tree and
    # half another, which is the defect this flag exists to remove.
    ROOT = a.root
    DIFF = a.diff or os.path.join(ROOT, "Reconstruction", "Tests", "Differential")
    DB = os.path.join(ROOT, "Database", "FFXII TZA")
    a.diff = DIFF
    a.out = a.out or os.path.join(DB, "_index", "PARITY-STATUS.md")

    names = sorted(f for f in os.listdir(a.diff)
                   if f.startswith("diff_") and f.endswith(".py"))
    pilots, problems, undeclared = [], [], []
    for fn in names:
        decl = read_declaration(os.path.join(a.diff, fn))
        if decl is None:
            undeclared.append(fn)
            continue
        cmap = read_contract_map(os.path.join(a.diff, fn))
        problems += validate(fn, decl)
        problems += check_contract_map(fn, decl, cmap)
        pilots.append((fn, decl, cmap))

    # FINDABILITY, swept on every run (OPUS-VERIFY-ALL-47-CONTRACT-CLAIM-TABLES-FINDABLE):
    # contract_claims returns [] -- not an error -- when a contract's `## 15.` heading is
    # missing/renamed or its claim table's first header cell is not `claim`.  A page in that
    # state reports zero claims: a harness mapping it gets every row back as "no section-15
    # claim" instead of the real diagnosis, and an unmapped page is never noticed at all.
    # OPUS's one-time sweep found all 47 pages findable on 2026-09-18; this makes it a gate.
    for p in sorted(Path(DB).rglob("CONTRACT-*.md")):
        rel = p.relative_to(DB).as_posix()
        found = contract_claims(rel)
        if not found:
            problems.append("%s: section 15 yields no claims -- the '## 15.' heading or the "
                            "'claim' table header is missing or renamed" % rel)

    measured = {}
    if a.run:
        for fn, _d, _c in pilots:
            measured[fn] = run_harness(fn, a.exe, a.timeout)
            print("  ran %-26s %s" % (fn, measured[fn]))

    o = []
    w = o.append
    w("# Parity status — the eleven dimensions, per reconstructed subsystem")
    w("")
    w("**GENERATED — do not hand-edit.** `Tools/analysis-kit/gfz-scripts/parity_status.py`")
    w("")
    w("Criteria: [`../../../Reconstruction/PARITY-STANDARD.md`](../../../Reconstruction/PARITY-STANDARD.md). "
      "Charter §21 requires parity status to be explicit per dimension; this is that table.")
    w("")
    if undeclared:
        w("> **%d harness(es) carry no `PARITY` declaration and are listed as such, not omitted:** %s"
          % (len(undeclared), ", ".join("`%s`" % u for u in undeclared)))
        w("")
    if problems:
        w("> **%d declaration problem(s):**" % len(problems))
        for p in problems:
            w("> - %s" % p)
        w("")
    else:
        w("**All %d declarations are well formed** — every dimension present, every verdict legal, "
          "every non-`COVERED` carrying a reason." % len(pilots))
        w("")

    subs = [d["subsystem"] for _f, d, _c in pilots]
    w("| dimension | " + " | ".join("`%s`" % s for s in subs) + " |")
    w("|---|" + "---|" * len(subs))
    marks = {"COVERED": "**yes**", "NOT COVERED": "no", "N/A": "n/a"}
    for dim in DIMENSIONS:
        cells = []
        for _f, d, _c in pilots:
            v = d["dimensions"].get(dim, ("MISSING", ""))
            cells.append(marks.get(v[0], "**?**"))
        w("| **%s** | %s |" % (dim, " | ".join(cells)))
    w("")

    tally = {}
    for dim in DIMENSIONS:
        c = sum(1 for _f, d, _c in pilots if d["dimensions"].get(dim, ("", ""))[0] == "COVERED")
        n = sum(1 for _f, d, _c in pilots if d["dimensions"].get(dim, ("", ""))[0] == "NOT COVERED")
        tally[dim] = (c, n)
    w("| dimension | covered | not covered | n/a |")
    w("|---|---:|---:|---:|")
    for dim in DIMENSIONS:
        c, n = tally[dim]
        w("| %s | %d | %d | %d |" % (dim, c, n, len(pilots) - c - n))
    w("")

    # A dimension is UNIVERSALLY unmet only when every pilot declares NOT COVERED. Scoring it
    # as "0 covered" instead counted `N/A` as a failure -- SERIALIZATION is n/a for five of the
    # six and was reported as failing for all of them.
    blocked = [dim for dim in DIMENSIONS if tally[dim][1] == len(pilots) and pilots]
    w("## Contract coverage — derived, not declared")
    w("")
    w("Charter §21's `CONTRACT` dimension asks whether the harness exercises the claims its "
      "contract makes. **Each harness now carries a `CONTRACT_MAP`** and this table is computed "
      "from it; the claim strings are checked against each contract's §15 table on every run, so "
      "a reworded claim shows up as drift rather than as silent coverage.")
    w("")
    w("> **`OPEN QUESTION` rows are excluded from the denominator and named anyway.** A §15 row "
      "whose confidence is `UNKNOWN` records a question, not a behaviour, and no case can "
      "exercise it. Excluding it without saying so would be the quiet kind of denominator this "
      "project keeps catching.")
    w("")
    w("| subsystem | §15 rows | exercised | partial | not exercised | of which scope | open questions | verdict |")
    w("|---|---:|---:|---:|---:|---:|---:|---|")
    for _f, d, cmap in pilots:
        if cmap is None:
            w("| `%s` | ? | ? | ? | ? | ? | ? | **no map** |" % d["subsystem"])
            continue
        if not cmap:
            w("| `%s` | — | — | — | — | — | — | **no contract exists** |" % d["subsystem"])
            continue
        c = {k: sum(1 for r in cmap if r[1] == k) for k in CONTRACT_STATUSES}
        sc = sum(1 for r in cmap if r[1] == "NOT EXERCISED" and marker_of(r[2]))
        w("| `%s` | %d | %d | %d | %d | %d | %d | %s |"
          % (d["subsystem"], len(cmap), c["EXERCISED"], c["PARTIAL"], c["NOT EXERCISED"],
             sc, c["OPEN QUESTION"], derive_contract(cmap)[0]))
    w("")
    w("> **`of which scope` counts `NOT EXERCISED` rows whose own reason carries a literal marker "
      "saying the claim is about code this pilot does not contain or does not reach.** Those "
      "rows close through `INTEGRATION` — the pilot growing into a subsystem harness — not "
      "through new test cases. It is a floor: only author-written markers count "
      "(`parity_claim_scope.py`), so an unmarked unexercised row is neither confirmed work nor "
      "confirmed scope.")
    w("")
    tot = [r for _f, _d, cm in pilots if cm for r in cm]
    if tot:
        ex = sum(1 for r in tot if r[1] == "EXERCISED")
        oq = sum(1 for r in tot if r[1] == "OPEN QUESTION")
        sc = sum(1 for r in tot if r[1] == "NOT EXERCISED" and marker_of(r[2]))
        # The denominator is COUNTED, not written down. It said "five pilots" while six had a
        # contract, one block after the sixth was written -- a hardcoded denominator in a
        # generated page, which is the exact error class this project exists to stop making.
        nc = sum(1 for _f, _d, cm in pilots if cm)
        w("**%d of %d testable contract claims are exercised across the %d pilot(s) that have a "
          "contract** — %d of the %d §15 rows record open questions and are excluded. At least "
          "**%d of the unexercised are out of pilot scope**, not test debt."
          % (ex, len(tot) - oq, nc, oq, len(tot), sc))
        w("")
    for _f, d, cmap in pilots:
        if not cmap:
            continue
        w("### `%s` — %s" % (d["subsystem"], d.get("contract", "?")))
        w("")
        w("| claim | status | note |")
        w("|---|---|---|")
        for claim, status, why in cmap:
            mark = "**%s**" % status if status == "EXERCISED" else status
            if status == "NOT EXERCISED" and marker_of(why):
                mark = "NOT EXERCISED · scope"
            w("| %s | %s | %s |" % (claim, mark, why))
        w("")

    w("## Certification")
    w("")
    w("```text")
    w("PARITY CERTIFIED  requires  every APPLICABLE dimension COVERED")
    w("                  and       INTEGRATION covered AGAINST THE RUNNING GAME")
    w("```")
    w("")
    certified = [d["subsystem"] for _f, d, _c in pilots
                 if all(v[0] != "NOT COVERED" for v in d["dimensions"].values())]
    w("**%d of %d pilots certified.**" % (len(certified), len(pilots)))
    w("")
    if blocked:
        w("**%d dimension(s) are `NOT COVERED` by every pilot without exception:** %s — every "
          "other dimension is either covered somewhere or genuinely `n/a`."
          % (len(blocked), ", ".join("**%s**" % b for b in blocked)))
        w("")
        w("> **That is the mechanical reason the ladder reads 0 PARITY CERTIFIED**, and it is a "
          "list of declared shared gaps. `INTEGRATION` requires native caller/replacement and "
          "consequence evidence; isolated original-code execution and bounded input/return captures "
          "do not establish it. `FULL-SUBSYSTEM` requires the applicable subsystem scope and entry "
          "points to be covered, beyond one local operation.")
        w("")
        near = [(d["subsystem"],
                 [k for k, v in d["dimensions"].items()
                  if v[0] == "NOT COVERED" and k not in blocked])
                for _f, d, _c in pilots]
        near = [(s_, g) for s_, g in near if len(g) <= 2]
        if near:
            w("**Closest to the gate, ignoring the universal blockers:** %s."
              % "; ".join("`%s` owes %s" % (s_, ", ".join(sorted(g)) or "nothing else")
                          for s_, g in sorted(near, key=lambda t: len(t[1]))))
            w("")

    w("## Per pilot")
    w("")
    for fn, d, cmap in pilots:
        cov = [k for k, v in d["dimensions"].items() if v[0] == "COVERED"]
        napp = [k for k, v in d["dimensions"].items() if v[0] == "N/A"]
        gaps = [(k, v[1]) for k, v in sorted(d["dimensions"].items()) if v[0] == "NOT COVERED"]
        w("### `%s` — entry `%s`" % (d["subsystem"], d.get("entry", "?")))
        w("")
        con = d.get("contract")
        w("- **contract:** %s" % ("`%s`" % con if con else "**none — this subsystem has no behavioural contract**"))
        w("- **covered:** %d of 11 — %s" % (len(cov), ", ".join(sorted(cov)) or "none"))
        w("- **not applicable:** %d — %s" % (len(napp), ", ".join(sorted(napp)) or "none"))
        if fn in measured:
            state, counts, mism = measured[fn]
            if state == "ok":
                cases, comps = counts
                parts = []
                if cases is not None:
                    parts.append("%s case(s)" % "{:,}".format(cases))
                if comps is not None:
                    parts.append("%s comparison(s)" % "{:,}".format(comps))
                w("- **measured this run:** %s, **%d mismatch(es)**"
                  % (", ".join(parts), mism))
            else:
                w("- **measured this run:** `%s` — no number is reported rather than a wrong one" % state)
        w("")
        w("  | not covered | what would cover it |")
        w("  |---|---|")
        for k, why in gaps:
            w("  | %s | %s |" % (k, why))
        w("")

    w("## What this page does not claim")
    w("")
    w("- **A declaration is a claim, not a measurement.** Nothing here checks that a harness "
      "marked `COVERED` actually meets the §3 criterion; the `measured` line only says the "
      "harness still runs and still reports zero mismatches.")
    w("- **An `EXERCISED` mark is still a human judgement.** It asserts that breaking the claim "
      "breaks the test; nothing here mutates the reconstruction to confirm that it would. The "
      "claim STRINGS are checked mechanically, the mapping is not.")
    w("- **Runtime captures have bounded scope.** Consult each experiment's process/input "
      "controls and limitations; the declarations here do not independently verify those captures "
      "or promote return-value agreement to integration, scheduling or ownership evidence.")

    io.open(a.out, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(o) + chr(10))
    print("wrote %s: %d pilot(s), %d declaration problem(s), %d certified"
          % (a.out, len(pilots), len(problems), len(certified)))
    return 1 if problems or undeclared else 0


if __name__ == "__main__":
    sys.exit(main())
