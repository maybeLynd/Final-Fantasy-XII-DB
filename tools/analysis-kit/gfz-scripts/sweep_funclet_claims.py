#!/usr/bin/env python3
"""sweep_funclet_claims.py - EC-1: which written conclusions could rest on unwind-funclet edges?

The question
------------
`edges.tsv` carries 3,834 caller edges whose source is a `CompilerGeneratedEH` funclet or catch
handler. The mission prompt bans that evidence class outright -- a prior branch reasoned from it
and lost 182 classifications -- and **the call graph offers the mistake by default**, because an
ordinary `awk` over `edges.tsv` returns those edges alongside real ones.

`program_coverage.py` measured the blast radius: **838** functions have at least one such caller,
and **278** of those are *authored* functions left with **no caller at all** once EH edges are
removed. For one of those 278, any written claim of the form *"nothing calls this"*, *"its only
caller is X"* or *"reachable only from Y"* was, at best, derived from an instrument that was
lying -- and would read as perfectly well-evidenced on the page.

This tool finds those sentences. It does **not** decide whether they are wrong.

What it reports, and what it does not
-------------------------------------
A finding is *an address from the contaminated set cited within one line of reachability
language*. That is a **candidate for adjudication**, not a verdict:

- a document may say *"called from X"* where X is a genuine non-EH caller -- correct, and it will
  still be reported, because the tool cannot read intent;
- a document may state the EC-1 problem itself (the index files do) -- reported, and separated out;
- a claim may be right for reasons the call graph never supplied -- runtime observation, a data
  table, a string reference -- which is exactly why a human closes each finding.

**Severity is the one judgement it does make**, and it is mechanical:

    HIGH   the address is one of the 278: it has NO non-EH caller, so any "reached from" or
           "only caller" claim about it cannot have come from a legitimate call edge.
    WATCH  the address is in the wider 838: it has real callers too, so a claim may be sound;
           what matters is whether the funclet edge was counted among them.

Populations are recomputed from `functions.tsv` and `edges.tsv` on every run -- never read from a
document -- using the same `authored = all - generated - thunks` definition as
`program_coverage.py`, so the two tools cannot drift apart silently.

Both spellings of an address are searched. `ANY_HEX8` requires a non-word character before the
digits, so the GFZ's own `FUN_002f9860` spelling is **not** a match for `002F9860`; missing it
would silently shrink the population, which is how 226 authored functions once went uncounted.
"""
import argparse
import collections
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
WORK = os.path.join(KP.ROOT, "Database", "Tools", "work")

# Identical to program_coverage.py. If these drift, the two tools describe different populations.
GENERATED = (
    "CompilerGeneratedEH",
    "CompilerGeneratedCFG",
    "CompilerGeneratedCpp",
    "Runtime.Callback.ReturnValueAdapter",
    "Runtime.Callback.OwnedBufferResetAdapter",
    "Reflection.PClassDescriptorForType",
    "Reflection.DataMemberMetadataStaticTeardown",
    "Reflection.ClassDescriptorStaticTeardown",
    "Reflection.AnnotationStaticTeardown",
    "Reflection.ReflectionStaticTeardown",
    "Reflection.ObjectTraversalAdapter",
    "ScriptVM.ObjectPushAdapter",
    "ScriptVM.NullableObjectPushAdapter",
    "Thunk.",
)

BARE_HEX8 = re.compile(r"(?<![0-9A-Za-z_])(?:0[xX])?([0-9A-Fa-f]{8})(?![0-9A-Za-z_])")
LEDGER_HEX8 = re.compile(r"(?:FUN|LAB|DAT|thunk_FUN|j_FUN)_([0-9A-Fa-f]{8})")

# Reachability vocabulary. Each entry is (regex, what the claim asserts).
CLAIMS = [
    (re.compile(r"\bno\s+(?:known\s+|other\s+)?callers?\b", re.I), "no caller"),
    (re.compile(r"\bnot\s+called\b|\bnever\s+called\b|\buncalled\b", re.I), "never called"),
    (re.compile(r"\bno\s+(?:x-?refs?|cross-?references?|references?)\b", re.I), "no references"),
    (re.compile(r"\bunreachable\b|\bnot\s+reachable\b|\bno\s+path\b", re.I), "unreachable"),
    (re.compile(r"\b(?:sole|only|single|one)\s+caller\b", re.I), "only caller"),
    (re.compile(r"\bcalled\s+(?:only\s+)?(?:from|by)\b", re.I), "called from"),
    (re.compile(r"\breach(?:ed|able)\s+(?:only\s+)?(?:from|by|through)\b", re.I), "reached from"),
    (re.compile(r"\bcallers?\s*[:=]\s*", re.I), "callers listed"),
    (re.compile(r"\bentry\s+point\b", re.I), "entry point"),
    (re.compile(r"\bdead\s+code\b|\borphan(?:ed)?\b", re.I), "dead/orphan"),
    (re.compile(r"\bits\s+caller\b|\bthe\s+caller\s+is\b", re.I), "the caller is"),
]


def read_tsv(path):
    rows = []
    hdr = None
    for i, line in enumerate(io.open(path, encoding="utf-8", errors="replace")):
        p = line.rstrip(chr(10)).rstrip(chr(13)).split(chr(9))
        if i == 0:
            hdr = {n: j for j, n in enumerate(p)}
        else:
            rows.append(p)
    return hdr, rows


def populations(work):
    """-> (contaminable_278, eh_targets_838, stats). Recomputed, never quoted."""
    gdir = os.path.join(work, "graph")
    hdr, rows = read_tsv(os.path.join(gdir, "functions.tsv"))

    def col(p, name):
        j = hdr.get(name, -1)
        return p[j] if 0 <= j < len(p) else ""

    fns = {}
    for p in rows:
        if not p or not p[0]:
            continue
        tags = col(p, "tags")
        fns[p[0].upper()] = {
            "name": col(p, "name"),
            "owner": col(p, "owner"),
            "thunk": col(p, "thunk").lower() == "true",
            "generated": any(g in tags for g in GENERATED),
            "eh": "CompilerGeneratedEH" in tags,
        }

    callers = collections.defaultdict(set)
    eh_targets = set()
    total = eh_sourced = 0
    _h, erows = read_tsv(os.path.join(gdir, "edges.tsv"))
    for p in erows:
        if len(p) < 2 or p[0] == "caller":
            continue
        a, b = p[0].upper(), p[1].upper()
        total += 1
        if fns.get(a, {}).get("eh"):
            eh_sourced += 1
            eh_targets.add(b)
            continue          # EC-1: banned as semantic evidence
        callers[b].add(a)

    authored = {k for k, v in fns.items() if not v["generated"] and not v["thunk"]}
    contaminable = {t for t in eh_targets if t in authored and not callers.get(t)}
    stats = {
        "functions": len(fns),
        "eh_functions": sum(1 for v in fns.values() if v["eh"]),
        "edges": total,
        "eh_edges": eh_sourced,
        "authored": len(authored),
    }
    return contaminable, eh_targets, fns, callers, stats


def docs(db):
    out = []
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in ("_templates",)]
        for f in sorted(files):
            if f.endswith(".md"):
                out.append(os.path.join(root, f))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--work", default=WORK)
    ap.add_argument("--out", help="write the findings as markdown here")
    ap.add_argument("--all", action="store_true",
                    help="also report WATCH findings (the wider 838), not only the 278")
    ap.add_argument("--control", action="store_true",
                    help="positive control: plant a synthetic document this scan MUST find")
    a = ap.parse_args()

    contaminable, eh_targets, fns, callers, st = populations(a.work)
    print("populations, recomputed from functions.tsv + edges.tsv")
    print("  functions                         : %d" % st["functions"])
    print("  tagged CompilerGeneratedEH        : %d of %d" % (st["eh_functions"], st["functions"]))
    print("  edges with an EH caller           : %d of %d (%.2f %%)"
          % (st["eh_edges"], st["edges"], 100.0 * st["eh_edges"] / st["edges"]))
    print("  distinct callees of an EH edge    : %d" % len(eh_targets))
    print("  authored (not generated, not thunk): %d of %d" % (st["authored"], st["functions"]))
    print("  CONTAMINABLE (no non-EH caller)   : %d of %d authored"
          % (len(contaminable), st["authored"]))
    print()

    paths = docs(a.db)

    # A NEGATIVE FROM THIS SCAN IS WORTHLESS WITHOUT A POSITIVE CONTROL THAT IS POSITIVE FOR
    # THIS INSTRUMENT. The plausible outcome here is "no findings", and that reads identically
    # whether the database is clean or the regexes never matched anything, the address spelling
    # was wrong, or the population came back empty. So plant a document that MUST be found:
    # a real contaminable address, in both spellings, beside real reachability language.
    control_path = None
    if a.control:
        addr = sorted(contaminable)[0]
        control_path = os.path.join(a.db, "_EC1_POSITIVE_CONTROL.md")
        io.open(control_path, "w", encoding="utf-8", newline=chr(10)).write(
            "# positive control - delete me" + chr(10) * 2
            + "`%s` has no callers; it is reachable only from the boot path." % addr + chr(10)
            + "FUN_%s is called only from the same place." % addr.lower() + chr(10))
        paths.append(control_path)
        print("positive control planted: %s cited two ways beside 'no callers'/'called only from'"
              % addr)
        print()

    findings = []
    cited_high = set()
    cited_watch = set()
    for path in paths:
        try:
            text = io.open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        lines = text.split(chr(10))
        rel = os.path.relpath(path, a.db).replace(os.sep, "/")
        is_index = rel.startswith("_index/")
        for i, line in enumerate(lines):
            hits = set(m.group(1).upper() for m in BARE_HEX8.finditer(line))
            hits |= set(m.group(1).upper() for m in LEDGER_HEX8.finditer(line))
            if not hits:
                continue
            high = hits & contaminable
            watch = (hits & eh_targets) - contaminable
            # Citation counting is unconditional: it measures how much of the contaminated
            # population the database talks about at all, which is a different question from
            # whether any sentence draws a reachability conclusion.
            cited_high |= high
            cited_watch |= watch
            if not high and not (watch and a.all):
                continue
            window = chr(10).join(lines[max(0, i - 1):i + 2])
            claims = [what for rx, what in CLAIMS if rx.search(window)]
            if not claims:
                continue
            for addr in sorted(high) + (sorted(watch) if a.all else []):
                findings.append({
                    "sev": "HIGH" if addr in contaminable else "WATCH",
                    "doc": rel, "line": i + 1, "addr": addr, "index": is_index,
                    "claims": claims, "text": line.strip()[:160],
                })

    ctrl = [f for f in findings if f["doc"].startswith("_EC1_POSITIVE_CONTROL")]
    findings = [f for f in findings if not f["doc"].startswith("_EC1_POSITIVE_CONTROL")]
    if control_path:
        os.remove(control_path)
        if ctrl:
            print("CONTROL: FOUND (%d hit(s), both spellings) -- the instrument can see a"
                  " finding." % len(ctrl))
        else:
            print("CONTROL: **NOT FOUND** -- this scan cannot detect what it is looking for.")
            print("Every negative below is meaningless. Fix the instrument before reading on.")
            return 2
        print()

    sysf = [f for f in findings if not f["index"]]
    idxf = [f for f in findings if f["index"]]
    print("documents scanned                   : %d" % len(paths))
    print("of the %d contaminable functions, cited anywhere: %d (%.1f %%)"
          % (len(contaminable), len(cited_high),
             100.0 * len(cited_high) / len(contaminable) if contaminable else 0.0))
    print("of the %d EH-touched functions, cited anywhere  : %d (%.1f %%)"
          % (len(eh_targets), len(cited_high | cited_watch),
             100.0 * len(cited_high | cited_watch) / len(eh_targets) if eh_targets else 0.0))
    print()
    print("FINDINGS (a reachability claim within one line of a contaminated address)")
    print("  in system documents               : %d" % len(sysf))
    print("  in _index/ (meta -- these discuss EC-1 itself)  : %d" % len(idxf))
    print()
    for f in sysf:
        print("  %-5s %s:%d  %s  [%s]" % (f["sev"], f["doc"], f["line"], f["addr"],
                                          ", ".join(f["claims"])))
        print("        %s" % f["text"])
    if not sysf:
        print("  none: no system document pairs a reachability claim with a contaminated address.")
        print("  That is a real negative ONLY for this instrument -- see the note below.")
    print()
    print("What a clean result does and does not mean")
    print("  It means no system document states a reachability conclusion within one line of an")
    print("  address whose only caller edges are unwind funclets. It does NOT mean no conclusion")
    print("  rests on such an edge: a claim can be phrased without any of the %d matched forms,"
          % len(CLAIMS))
    print("  or sit further from the address than one line. This instrument has a stated reach.")

    if a.out:
        w = io.open(a.out, "w", encoding="utf-8", newline=chr(10))
        w.write("# EC-1 sweep - conclusions that could rest on unwind-funclet edges" + chr(10) * 2)
        w.write("Generated by `sweep_funclet_claims.py`. Populations recomputed from "
                "`functions.tsv` + `edges.tsv`." + chr(10) * 2)
        w.write("| population | count | denominator |" + chr(10))
        w.write("|---|---:|---:|" + chr(10))
        w.write("| tagged `CompilerGeneratedEH` | %d | %d functions |"
                % (st["eh_functions"], st["functions"]) + chr(10))
        w.write("| edges with an EH caller | %d | %d edges |" % (st["eh_edges"], st["edges"])
                + chr(10))
        w.write("| distinct callees of those edges | %d | — |" % len(eh_targets) + chr(10))
        w.write("| **contaminable** (authored, no non-EH caller) | **%d** | %d authored |"
                % (len(contaminable), st["authored"]) + chr(10) * 2)
        w.write("**Findings in system documents: %d.** " % len(sysf))
        if not sysf:
            w.write("No system document states a reachability conclusion within one line of a "
                    "contaminated address." + chr(10) * 2)
        else:
            w.write(chr(10) * 2)
            for f in sysf:
                w.write("- **%s** `%s:%d` — `%s` (%s)  " % (f["sev"], f["doc"], f["line"],
                                                            f["addr"], ", ".join(f["claims"]))
                        + chr(10) + "  > %s" % f["text"] + chr(10))
        w.close()
        print()
        print("wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
