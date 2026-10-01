#!/usr/bin/env python3
"""Refuse a census that cannot name the parent generation it was taken from.

52 kit scripts read work/graph/functions.tsv and every figure in the database
rests on it - the population, the declared EC-7 surface, the measured bodies.
The file carries no parent, no manifest, only an mtime: a wrong-generation
export is byte-plausible and silent. That is not hypothetical - the
*_0109_STALE.tsv pair in the same directory is a stale export that nothing
flagged.

The fix is a stamp, not trust: DumpFullCoverageGraph writes
functions.parent.json beside the census, recording the sha256 it MEASURED on
the parent GZF plus what the program says about itself (the program name
carries the generation tag; the executable sha ties it to the binary). This
checker compares the stamp against GfzEnv.ps1's $GfzParentSha /
$GfzParentGzf / $GfzAuthorizedExeSha and refuses on any mismatch.

Reading the parent from GfzEnv.ps1 rather than holding a copy is deliberate -
check_provenance keeps the same rule, because a duplicated constant named a
parent two generations stale on 2026-09-03 and reported it current.

    check_census_generation.py [--graph <dir>]

Exit code 1 (REFUSE) on: missing/unparseable sidecar, parent sha mismatch,
program-name generation tag not the certified one's, or a foreign executable.
"""
import argparse
import io
import json
import os
import re
import sys

GRAPH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "work", "graph")
GFZ_ENV = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "ghidra", "run", "GfzEnv.ps1")

GENERATION = re.compile(r"G[MN]\d+")


def env_value(txt, name, inner):
    m = re.search(r"^\s*\$%s\s*=\s*'(%s)'" % (name, inner), txt, re.M)
    return m.group(1) if m else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default=GRAPH)
    a = ap.parse_args(argv)

    sidecar = os.path.join(a.graph, "functions.parent.json")
    funcs = os.path.join(a.graph, "functions.tsv")

    try:
        env = io.open(GFZ_ENV, encoding="utf-8", errors="replace").read()
    except OSError:
        print("REFUSE: cannot read %s - the certified parent is unknowable" % GFZ_ENV)
        return 1
    want_sha = env_value(env, "GfzParentSha", r"[0-9a-fA-F]{64}")
    want_gzf = env_value(env, "GfzParentGzf", r"[^']+")
    want_exe = env_value(env, "GfzAuthorizedExeSha", r"[0-9a-fA-F]{64}")
    if not (want_sha and want_gzf):
        print("REFUSE: GfzEnv.ps1 carries no $GfzParentSha/$GfzParentGzf block")
        return 1
    want_tag = GENERATION.search(want_gzf)

    failures = []

    try:
        stamp = json.load(io.open(sidecar, encoding="utf-8"))
    except OSError:
        print("REFUSE: %s does not exist" % sidecar)
        print("  The census carries no parent stamp - a wrong-generation export is")
        print("  indistinguishable from a current one. Re-export through")
        print("  ghidra/run/Export-GfzCensus.ps1, which makes DumpFullCoverageGraph")
        print("  hash the certified parent and write the sidecar.")
        return 1
    except ValueError as e:
        print("REFUSE: %s is not parseable JSON: %s" % (sidecar, e))
        return 1

    got_sha = stamp.get("parent_gzf_sha256", "")
    if got_sha.lower() != want_sha.lower():
        failures.append(
            "parent sha %s is not the certified parent %s"
            % (got_sha[:24] or "<absent>", want_sha[:24]))

    got_tag = GENERATION.search(stamp.get("program_name") or "")
    if want_tag and (not got_tag or got_tag.group(0) != want_tag.group(0)):
        # The program-name tag is what actually catches 'exported from a stale
        # PROJECT while the new GZF already sits at the parent path' - hashing
        # the file measures the file, the program name measures the export.
        failures.append(
            "program_name %r is generation %s, not the certified %s"
            % (stamp.get("program_name"), got_tag.group(0) if got_tag else
               "<none>", want_tag.group(0)))

    got_exe = (stamp.get("executable_sha256") or "").lower()
    if want_exe and got_exe and got_exe != want_exe.lower():
        failures.append(
            "executable_sha256 %s is a different binary than the authorized %s"
            % (got_exe[:24], want_exe[:24]))

    print("census generation check - %s" % sidecar)
    print("  program:      %s" % stamp.get("program_name"))
    print("  parent gzf:   %s  sha %s" % (stamp.get("parent_gzf"),
                                              got_sha[:24]))
    print("  certified:    %s  sha %s" % (want_gzf, want_sha[:24]))
    print("  exported_utc: %s   functions: %s   edges: %s"
          % (stamp.get("exported_utc"), stamp.get("function_count"),
             stamp.get("edge_count")))

    try:
        rows = sum(1 for _ in io.open(funcs, encoding="utf-8")) - 1
        if stamp.get("function_count") not in (None, rows):
            print("  ADVISORY: sidecar function_count %s but functions.tsv has %d rows"
                  " - census and stamp may be from different exports"
                  % (stamp["function_count"], rows))
    except OSError:
        print("  ADVISORY: no functions.tsv beside the sidecar")

    if failures:
        print()
        for f in failures:
            print("REFUSE: %s" % f)
        print("\nDo not edit the stamp to match - re-export from the certified")
        print("parent. The stamp records what the export measured.")
        return 1
    print("\nstamp consistent with the certified parent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
