"""audit_protocol_readiness.py - can the thirty passes actually be run?

FINAL-AUDIT-PROTOCOL names a tool for 13 of its 30 passes and says, in its own cautions:

    "A crash is not a false clean, and it is the good failure. A checker that dies loudly during a
     thirty-pass run costs a re-run; one that returns green because it never reached the rows costs
     the audit."

The streak **resets on any failure**, so a named tool that does not exist, cannot be invoked, or dies
is not a pass-N problem -- it is an N-1-passes-wasted problem. **Nothing has ever checked that the
tools the protocol names can be run at all.**

This does not run the audit. It asks, of each named tool: does the file exist, and does invoking it
produce a verdict rather than a traceback? A non-zero exit is FINE -- that is a checker reporting
findings. A traceback, a missing file, or an argparse refusal is not.
"""
import os, re, subprocess, sys

DB = "Database/FFXII TZA"
KIT = os.path.join("Database", "Tools", "analysis-kit", "gfz-scripts")
PROTO = os.path.join(DB, "_index", "FINAL-AUDIT-PROTOCOL.md")

# Read the pass -> tool table out of the protocol rather than restating it.
rows = []
for line in open(PROTO, encoding="utf-8", errors="replace").read().split("\n"):
    m = re.match(r"^\|\s*(\d+[a-z]?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*`[^|]*)\|\s*([^|]*)\|", line)
    if m and "`" in m.group(3):
        tools = re.findall(r"`([A-Za-z0-9_]+\.py)`", m.group(3))
        if tools:
            rows.append((m.group(1), m.group(2).strip(), tools, m.group(4).strip()))

# THE INVOCATION RECIPE, which is the deliverable. Three of the protocol's tools do NOT take the
# obvious `--db`, and a thirty-pass run that discovers that at pass 22 has wasted twenty-one passes.
# Recorded here from each tool's own --help, verified by running it. 2026-09-14, OPUS.
SCRATCH = os.environ.get("TEMP", ".")
FAS2_TSV = os.path.join(SCRATCH, "fas2.tsv")
# check_crossref_clean judges documents against a report and REFUSES (exit 2) one
# older than any document it judges, so the report has to be built first and this
# path is where the recipe expects it:
#     python audit_crossrefs.py --docs "<db>" --functions ... --edges ... --json CROSSREF_JSON
CROSSREF_JSON = os.path.join(SCRATCH, "crossref-report.json")
BOARD = os.path.join(DB, "_index", "_inbox", "TEAM.json")
ARGS = {
    "verify_doc_addresses.py": ["--db", DB, "--all", "--quiet"],
    # --json is not cosmetic: it writes the report check_crossref_clean needs, and this file
    # already pays for the audit_crossrefs run. Without it pass 30 could only be shown to
    # START (exit 2, "report required"), never to reach the corpus. audit_crossrefs is invoked
    # by passes 2, 4, 17 and 22, all of which precede 30 in the protocol table, so the report
    # exists by the time the checker runs.
    "audit_crossrefs.py": ["--docs", DB,
                           "--functions", "Database/Tools/work/graph/functions.tsv",
                           "--edges", "Database/Tools/work/graph/edges.tsv", "--quiet",
                           "--json", CROSSREF_JSON],
    "check_banned_evidence.py": ["--db", DB],
    "check_tier_presence.py": ["--db", DB],
    # requires a FAS2 export FIRST: fas2_export.py <certified snapshot> --tsv <file>
    "check_layer_separation.py": ["--db", DB, "--fas2", FAS2_TSV],
    "fas2_export.py": ["--help"],
    "check_denominators.py": ["--db", DB],
    # NOT --self-test. Corrected 2026-09-16 (OPUS): this recipe invoked passes 24 and 30 as
    # self-tests and reported "runs (exit 0)" for invocations that measure nothing about
    # the corpus - the same defect that had those two passes reporting a self-test as a
    # corpus verdict (d9291ff5, 6b418b62). A self-test is a control on the instrument, not
    # a reading, and a readiness report that cannot tell them apart is the "green because
    # it never reached the rows" failure this file opens by quoting.
    "check_propagation.py": ["--db", DB, "--board", BOARD],
    "check_doc_claims.py": ["--db", DB],
    "check_links.py": ["--db", DB],
    # requires a FRESH report FIRST (see CROSSREF_JSON above); it refuses a stale one
    "check_crossref_clean.py": ["--db", DB, "--report", CROSSREF_JSON],
    "progress.py": ["--db", DB],
}

print("FINAL-AUDIT PROTOCOL - can the tools it names actually be run?\n")
print("  passes with a named tool: %d of 30\n" % len(rows))

seen, bad = {}, []
for num, name, tools, cov in rows:
    marks = []
    for t in tools:
        if t in seen:
            marks.append("%s %s" % (t, seen[t]))
            continue
        path = os.path.join(KIT, t)
        if not os.path.exists(path):
            seen[t] = "MISSING FROM THE KIT"
            bad.append((num, t, "missing"))
        else:
            a = ARGS.get(t, ["--db", DB])
            try:
                r = subprocess.run([sys.executable, path] + a, capture_output=True,
                                   text=True, timeout=900)
                err = (r.stderr or "")
                if "Traceback" in err:
                    last = [l for l in err.strip().split("\n") if l.strip()][-1][:70]
                    seen[t] = "CRASHES: " + last
                    bad.append((num, t, "crash"))
                elif "error:" in err and "usage:" in err:
                    seen[t] = "REFUSES THESE ARGS"
                    bad.append((num, t, "args"))
                else:
                    seen[t] = "runs (exit %d)" % r.returncode
            except subprocess.TimeoutExpired:
                seen[t] = "TIMEOUT"
                bad.append((num, t, "timeout"))
        marks.append("%s %s" % (t, seen[t]))
    flag = "  " if all("runs" in m for m in marks) else "!!"
    print("%s pass %-3s %-28s %s" % (flag, num, name[:28], "; ".join(marks)))

print("\n  tools named by the protocol : %d" % len(seen))
print("  runnable as invoked here    : %d" % sum(1 for v in seen.values() if "runs" in v))
print("  NOT runnable                : %d" % len(bad))
for num, t, why in bad:
    print("      pass %-3s %-34s %s" % (num, t, why))
