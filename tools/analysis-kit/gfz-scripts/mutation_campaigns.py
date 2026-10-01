#!/usr/bin/env python3
"""mutation_campaigns.py - the measured half of Reconstruction/MUTATION-CAMPAIGNS.md.

Why this exists
---------------
Every pilot's mutation count was published as prose inside its contract, one number per
contract, with no page where the campaign that produced it could be compared to the others.
Two consequences, both real:

  * `OPUS-CONTRA-MUTATION-LIT-SUFFIX` - a generator defect made every count before 2026-09-12
    a FLOOR rather than a total, and there was no single place to restate them;
  * a survivor in one pilot could not be recognised as the SAME KIND of survivor as one in
    another, because nobody saw them side by side. Half of them turn out not to be test gaps
    at all.

What it reads and what it will not do
------------------------------------
It reads `campaign.json` receipts - the instrument's own output, never a document - and emits
the counts table. **It does not adjudicate.** Which survivors are equivalent, which are
fixture scaffolding and which are real gaps is a judgement with evidence behind it, and that
half of the page is written by hand and is not regenerated. The marker keeps them apart.

A receipt whose `production_inputs_stable` is false, or whose status is INVALID, is reported
as such rather than dropped: an invalid run is a result about the instrument.
"""
import argparse
import json
import re
from pathlib import Path

BEGIN = "<!-- BEGIN GENERATED: mutation_campaigns.py -->"
END = "<!-- END GENERATED -->"

# The verdict vocabulary, in the order the table shows it.
COLS = ["KILLED", "SURVIVED", "EQUIVALENT", "NO_BUILD", "TIMEOUT", "INVALID"]


def receipts(root):
    """-> {pilot: (path, record)} keeping the LAST campaign per pilot by start time.

    A pilot re-run after a harness change has several receipts; the page must show the one
    that is current, and say how many runs it took.
    """
    out = {}
    for p in sorted(Path(root).glob("*/campaign.json")):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        cmd = rec.get("command") or []
        pilot = next((a for a in cmd[1:] if re.fullmatch(r"[a-z_]+", a or "")), None)
        if not pilot:
            continue
        prev = out.get(pilot)
        if prev is None or rec.get("start_unix", 0) >= prev[1].get("start_unix", 0):
            out[pilot] = (p, rec, (prev[2] + 1) if prev else 1)
        elif prev:
            out[pilot] = (prev[0], prev[1], prev[2] + 1)
    return out


def table(found):
    rows = []
    for pilot in sorted(found):
        path, rec, runs = found[pilot]
        c = rec.get("counts") or {}
        total = rec.get("total_generated")
        status = rec.get("status")
        if not rec.get("production_inputs_stable", True):
            status = "INVALID_INPUT_DRIFT"
        rows.append((pilot, total, [c.get(k, 0) for k in COLS], status, runs, path.parent.name))
    return rows


def render(rows):
    out = [BEGIN, "",
           "| pilot | points | " + " | ".join(COLS) + " | verdict | receipts |",
           "|---|---:|" + "---:|" * len(COLS) + "---|---|"]
    for pilot, total, counts, status, runs, dirname in rows:
        verdict = "**%s**" % status if status != "PASS" else "PASS"
        out.append("| `%s` | %s | %s | %s | `%s` |"
                   % (pilot, total, " | ".join(str(x) for x in counts), verdict, dirname))
    tot = [sum(r[2][i] for r in rows) for i in range(len(COLS))]
    out.append("| **%d pilots** | **%d** | %s | | |"
               % (len(rows), sum(r[1] or 0 for r in rows),
                  " | ".join("**%d**" % x for x in tot)))
    out += ["",
            "**%d of %d campaigns reach PASS.** A campaign with a survivor is `FAIL` by "
            "construction, and a campaign with an INVALID or TIMEOUT case is `FAIL_INCOMPLETE` "
            "or `INCOMPLETE` however few survivors it has - the instrument will not call a run "
            "complete that it could not read end to end."
            % (sum(1 for r in rows if r[3] == "PASS"), len(rows)),
            "", END]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipts", default=r"Database\Tools\work\OPUS\litsuffix")
    ap.add_argument("--page", default=r"Reconstruction\MUTATION-CAMPAIGNS.md")
    a = ap.parse_args()
    rows = table(receipts(a.receipts))
    if not rows:
        raise SystemExit("no campaign receipts under " + a.receipts)
    block = render(rows)
    page = Path(a.page)
    text = page.read_text(encoding="utf-8")
    lo, hi = text.index(BEGIN), text.index(END) + len(END)
    page.write_text(text[:lo] + block + text[hi:], encoding="utf-8", newline="\n")
    print("wrote %s: %d pilot(s), %d PASS" % (page, len(rows), sum(1 for r in rows if r[3] == "PASS")))


if __name__ == "__main__":
    main()
