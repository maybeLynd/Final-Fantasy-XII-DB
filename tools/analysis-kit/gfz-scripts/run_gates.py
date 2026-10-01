"""run_gates.py - run the kit's checkers and report what MOVED.

There are 70 `check_*.py` in this directory and, until now, **no runner**. Everyone ran the ones they
remembered. That is not a hypothetical cost: on 2026-09-14 a refused EC-7 family declaration dropped
**1,216 bodies out of the declared surface** - C from 12,202 to 10,986, the frontier up by the same -
and `check_dispositions` exited 1 about it the whole time, while several of my own `progress.py`
reads went past the line underneath the headline. Nothing was broken. Nobody was looking.

WHY THIS DOES NOT DEMAND THAT EVERYTHING BE GREEN. Measured across all 70: 50 exit 0, 11 exit 1, 8
need a target rather than the corpus, 1 crashes. Several of the 11 are reporting **candidates by
design** - `check_provenance` names 176 stale parent stamps that are real, known and adjudicated
debt. A runner that went red on those would be red forever, and **a checker that is always red
teaches people to ignore it**, which is the failure this exists to fix rather than repeat.

**SO IT COMPARES AGAINST A BASELINE OF ACCEPTED STATE AND REPORTS THE DIFFERENCE.** Green means
nothing moved since the baseline. Red means a checker's verdict changed - which is exactly the
signal that was missing when the SEAD family broke, and would have fired within one run.

THE BASELINE IS A RECORD OF DEBT, NOT A TARGET, and it is easy to abuse: re-baselining a red
checker makes the red go away without fixing anything. Two things guard against that. The baseline
stores each checker's whole output digest, so a checker that stays red but gets WORSE still moves
and still reports. And every baseline row carries the date it was taken, so a baseline refreshed to
silence something is visible in the diff of this file.

WHAT IT DOES NOT RUN, stated rather than skipped silently:
  * targeted tools that need a subject - `check_caller_claims` wants an `--addr`,
    `check_field_citations` a `--doc`, `check_extent_overruns` a `--tsv`. Where such a tool has a
    `--self-test` it is run, because proving the tool still works is worth the second it costs.
  * `check_layer_separation`, which needs a FAS2 export prepared first.
A tool this cannot run is listed in the report. Silence about a checker is how the last gap formed.
"""
import argparse, collections, hashlib, io, os, re, subprocess, sys, time

KIT = os.path.dirname(os.path.abspath(__file__))
DB_DEFAULT = "Database/FFXII TZA"
BASELINE = os.path.join("Database", "FFXII TZA", "_index", "gate-baseline.tsv")

# Checkers that do not take the corpus. Value = the arguments to run instead, or None for
# "cannot be run without a prepared input".
NOT_A_CORPUS_GATE = {
    # reads _types and the pages they link from their canonical locations; takes no target.
    "check_store_behind_page.py": [],
    # reads the shipping image and _types from their canonical locations; takes no target, and
    # passed --db it would die on an unrecognised argument.
    "census_field_accessors.py": [],
    # reads _types/fields.tsv and the registered censuses from their own canonical locations, so
    # it takes no target at all; passed `--db` it would die on an unrecognised argument.
    "check_gap_debt.py": [],
    # POSITIONAL, not --db. It takes the corpus root as a bare argument, so `--db` was swallowed
    # as the path and it died with FileNotFoundError on '--db\\_experiments'. It is a healthy
    # corpus gate that my first sweep reported as a crash - the kind of misreading that makes a
    # runner worse than none, since it manufactures a defect in a tool that works.
    "check_contract_runtime_links.py": ["{db}"],
    # takes --graph, not --db; invoked with --db it exits 2 on an argparse error and looks like a
    # refusal rather than a mis-invocation
    "check_census_generation.py": ["--graph", "Database/Tools/work/graph"],
    # NEITHER OF THESE TAKES --db, and both were reported as red for that reason alone. This is the
    # same misreading the entry above records for check_contract_runtime_links, which the first
    # sweep called a crash: the runner manufactured a defect in a tool that works. They sat in
    # "NOT IN THE BASELINE" at exit 2 looking like debt for anyone reading the suite output.
    #   check_publish_neighbours is a PRE-PUBLISH differential over named paths, not a corpus
    #   gate - it measures UNACCOUNTED NEIGHBOUR on HEAD against HEAD plus a batch - so the only
    #   thing a suite run can assert is that the instrument still works. Its self-test does that.
    #   check_literal_base_access scans the IMAGE, not the corpus, and takes --all / --base. Run
    #   bare it reports the population of the reference map's blind spot and exits 0.
    # 2026-09-16, OPUS.
    "check_publish_neighbours.py": ["--self-test"],
    "check_literal_base_access.py": [],
    "check_caller_claims.py": None,        # --exe --funcs --addr : one address at a time
    "check_field_citations.py": None,      # --exe --doc          : one document at a time
    "check_extent_overruns.py": None,      # --tsv                : a prepared export
    "check_layer_separation.py": None,     # --fas2               : needs fas2_export.py first
    "check_already_answered.py": ["--self-test"],
    "check_uncompared_pairs.py": ["--self-test"],
    "check_register_masks.py": ["--self-test"],
    "check_source_hygiene.py": ["--self-test"],
    # NOT --self-test, and this is the same defect audit_protocol_readiness.py was corrected for on
    # 2026-09-16 (d9291ff5, 6b418b62): running these two as self-tests made the suite print a GREEN
    # for invocations THAT MEASURE NOTHING ABOUT THE CORPUS. A self-test is a control on the
    # instrument, never a reading of the database, and a suite that cannot tell them apart is the
    # "green because it never reached the rows" failure. Both have a real corpus invocation and
    # neither can be driven from here:
    #   check_crossref_clean.py needs a FRESH audit_crossrefs --json report (it REFUSES a stale one,
    #     exit 2), which this runner has no way to build - see audit_protocol_readiness.py, which
    #     builds it and then runs `--db <db> --report <json>`;
    #   check_propagation.py needs the board as well as the db: `--db <db> --board <TEAM.json>`.
    # Reported as "needs a target or a prepared input" so the row is visibly UNRUN rather than
    # falsely clean. Pass 30's mechanical enforcement lives in the readiness driver, not here.
    # OPUS, 2026-09-16.
    "check_propagation.py": None,
    "check_crossref_clean.py": None,
    # check_interior_escape.py NEEDS A CLOSURE and cannot be driven from here. It answers "does a
    # pointer INTO this object ever escape to memory?" for ONE type at a time, from a closure
    # gen_actor_arg_closure.py builds, plus a per-type --returns/--slots seed set that is supplied
    # by hand. There is no corpus-wide invocation: run bare it exits 2 from argparse, which this
    # report would file under "NOT IN THE BASELINE ... exit 2" - the exact place where a genuine
    # red and a mis-invocation look identical, which is the failure this runner exists to prevent.
    # Registered as UNRUN so the row is visibly unrun rather than falsely red OR falsely clean.
    # Its own control (the S-14 battle-unit closure, 3 of 3 reachable sites at +0x000) is run by
    # hand and recorded in the file. OPUS, 2026-09-20.
    "check_interior_escape.py": None,
    # SEVENTEEN MORE OF THE SAME CLASS, AND THE TABLE ALREADY RECORDS THE LESSON TWICE ABOVE.
    # Measured 2026-09-20 (OPUS): every one of these exits 2 when the runner appends the corpus
    # path and NONE of them takes a positional - they read the store through `--store`, the image
    # through `--exe`, or nothing at all. Run bare, fourteen exit 0 and three exit 1 with real
    # findings nobody had seen, because the runner's report files them under "NOT IN THE BASELINE
    # (new checker...)" at exit 2, where a genuine red and a mis-invocation look identical - and
    # `--adopt-new` deliberately refuses to adopt a red without being named, so they could never
    # enter the baseline by themselves. That is the exact failure this runner's docstring exists
    # to fix: "Nothing was broken. Nobody was looking."
    # The three that exit 1 are check_alignment, check_copy_displacements and check_static_spans;
    # they are adopted as accepted debt on purpose, not silently.
    "check_alignment.py": [],
    "check_array_heads.py": [],
    "check_copy_displacements.py": [],
    "check_ctor_clears.py": [],
    "check_ctype_width.py": [],
    "check_embed_parent_fields.py": [],
    "check_imagebase_relative_refs.py": [],
    "check_repeated_records.py": [],
    "check_route_counts.py": [],
    "check_route_extents.py": [],
    "check_span_access.py": [],
    "check_stale_reasons.py": [],
    "check_static_spans.py": [],
    "check_storage_class.py": [],
    "check_taken_address_writes.py": [],
    "check_unread_spans_in_image.py": [],
    "check_unread_vs_census.py": [],
}
# volatile output: paths and times differ per run and are not a change in verdict
VOLATILE = re.compile(r"\d+\.\d+ ?s\b|\d{2}:\d{2}:\d{2}|[A-Za-z]:\\[^\s]*|/tmp/[^\s]*")


def digest(text):
    return hashlib.sha256(VOLATILE.sub("", text).replace("\r", "").encode("utf-8",
                                                                          "replace")).hexdigest()[:16]


def checkers():
    return sorted(f for f in os.listdir(KIT) if re.match(r"^check_.*\.py$", f))


def run_one(name, db, timeout=900):
    if name in NOT_A_CORPUS_GATE:
        args = NOT_A_CORPUS_GATE[name]
        if args is None:
            return None, "", "needs a target or a prepared input"
        args = [x.replace("{db}", db) for x in args]
    else:
        args = ["--db", db]
    try:
        r = subprocess.run([sys.executable, os.path.join(KIT, name)] + args,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", "exceeded %ds" % timeout
    err = r.stderr or ""
    if "Traceback" in err:
        last = [l for l in err.strip().split("\n") if l.strip()][-1][:90]
        return "CRASH", digest(r.stdout + err), last
    out = (r.stdout or "").strip().split("\n")
    tail = out[-1].strip()[:90] if out and out[-1].strip() else ""
    return r.returncode, digest(r.stdout), tail


def load_baseline(path):
    base = {}
    if not os.path.isfile(path):
        return base
    for line in io.open(path, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) >= 3:
            base[c[0]] = (c[1], c[2])
    return base


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB_DEFAULT)
    ap.add_argument("--baseline", default=BASELINE)
    ap.add_argument("--write-baseline", action="store_true",
                    help="record the CURRENT state as accepted. Re-baselining a red checker hides "
                         "it; the dated rows in the file make that visible in review.")
    ap.add_argument("--adopt-new", nargs="*", metavar="CHECKER",
                    help="append checkers that are NOT YET in the baseline, leaving every existing "
                         "row byte-identical. A new checker exiting 0 is adopted; a new checker "
                         "exiting non-zero is adopted only if named here, because recording a red "
                         "as accepted debt is a decision someone has to make on purpose.")
    ap.add_argument("--only", nargs="*", help="run just these checkers")
    a = ap.parse_args(argv)

    names = a.only if a.only else checkers()
    base = load_baseline(a.baseline)
    rows, t0 = [], time.time()
    for n in names:
        code, dig, tail = run_one(n, a.db)
        rows.append((n, code, dig, tail))

    unrunnable = [r for r in rows if r[1] is None]
    runnable = [r for r in rows if r[1] is not None]
    crashed = [r for r in runnable if r[1] == "CRASH"]
    moved, fresh = [], []
    for n, code, dig, tail in runnable:
        if n not in base:
            fresh.append((n, code, dig, tail))
        elif (str(code), dig) != base[n]:
            moved.append((n, code, dig, tail, base[n]))

    print("kit gates - %d checkers, %d run, %.0fs\n" % (len(names), len(runnable),
                                                        time.time() - t0))
    codes = collections.Counter(str(r[1]) for r in runnable)
    print("  exit codes: %s" % ", ".join("%s x%d" % (k, v) for k, v in sorted(codes.items())))
    print("  baseline  : %s" % (a.baseline if base else "NONE - nothing to compare against"))
    print()

    if crashed:
        print("  CRASHED - always a defect, in the checker or in what it reads:")
        for n, code, dig, tail in crashed:
            print("      %-42s %s" % (n, tail))
        print()
    if moved:
        print("  MOVED since the baseline - this is the signal this runner exists for:")
        for n, code, dig, tail, was in moved:
            print("      %-42s exit %s -> %s" % (n, was[0], code))
            if tail:
                print("          %s" % tail)
        print()
    if fresh and base:
        print("  NOT IN THE BASELINE (new checker, or baseline not refreshed):")
        for n, code, dig, tail in fresh:
            print("      %-42s exit %s" % (n, code))
        print()
    if unrunnable:
        print("  NOT RUN - named so that silence is never mistaken for a pass:")
        for n, _c, _d, why in unrunnable:
            print("      %-42s %s" % (n, why))
        print()

    if a.adopt_new is not None:
        # WHY THIS IS NOT --write-baseline. A checker written today is invisible to this runner until
        # it has a baseline row, so it reports nothing and nobody notices it stopped being run -
        # which is the exact gap this runner exists to close, reopened one checker at a time.
        # --write-baseline closes it, but it also re-records all 80 EXISTING rows at their current
        # state, so any checker that went red since the last baseline is silently accepted in the
        # same stroke. That is not hypothetical here: 15 checkers are red against the 2026-09-14
        # baseline right now. Adopting a new checker and accepting a regression must not be one
        # command.
        if a.only:
            print("  --adopt-new needs the WHOLE suite: a partial run cannot tell a new checker\n"
                  "  from one it simply did not run. Drop --only.")
            return 2
        if not base:
            print("  --adopt-new has nothing to append to. Use --write-baseline for a first record.")
            return 2
        named = set(a.adopt_new)
        take = [r for r in fresh if r[1] == 0 or r[0] in named]
        left = [r for r in fresh if r not in take]
        if not take:
            print("  nothing to adopt.")
            return 0
        with io.open(a.baseline, "a", encoding="utf-8", newline="\n") as fh:
            fh.write("#\n# Adopted %s - checkers that post-date the baseline above. Nothing already\n"
                     "# in this file was re-recorded.\n" % time.strftime("%Y-%m-%d"))
            for n, code, dig, tail in sorted(take):
                fh.write("%s\t%s\t%s\t%s\n" % (n, code, dig, tail.replace("\t", " ")))
        print("  ADOPTED into %s:" % a.baseline)
        for n, code, _d, _t in sorted(take):
            print("      %-42s exit %s" % (n, code))
        if left:
            print("\n  LEFT UNADOPTED - a new checker that is already red records accepted debt,")
            print("  so it is adopted only when named on the command line:")
            for n, code, _d, _t in sorted(left):
                print("      %-42s exit %s" % (n, code))
        return 0

    if a.write_baseline:
        with io.open(a.baseline, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Accepted state of the kit's checkers, recorded %s.\n"
                     % time.strftime("%Y-%m-%d"))
            fh.write("#\n")
            fh.write("# THIS IS A RECORD OF DEBT, NOT A TARGET. A non-zero exit here means a\n")
            fh.write("# checker is reporting findings that are known and adjudicated - 176 stale\n")
            fh.write("# provenance stamps, for instance. run_gates.py reports what MOVED against\n")
            fh.write("# this file, because a runner that demanded universal green would be red\n")
            fh.write("# forever and would teach everyone to ignore it.\n")
            fh.write("#\n")
            fh.write("# Re-baselining a red checker makes the red go away without fixing\n")
            fh.write("# anything. The digest column covers each checker's whole output, so a\n")
            fh.write("# checker that stays red but gets WORSE still moves; and a refresh that\n")
            fh.write("# silences something shows up in this file's own diff.\n")
            fh.write("#\n")
            fh.write("# checker\texit\tdigest\tlast_line\n")
            for n, code, dig, tail in sorted(runnable):
                fh.write("%s\t%s\t%s\t%s\n" % (n, code, dig, tail.replace("\t", " ")))
        print("  wrote baseline %s (%d checkers)" % (a.baseline, len(runnable)))
        return 0

    if not base:
        print("  No baseline. Run --write-baseline once to record the accepted state.")
        return 0
    if crashed or moved:
        return 1
    print("  nothing moved since the baseline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
