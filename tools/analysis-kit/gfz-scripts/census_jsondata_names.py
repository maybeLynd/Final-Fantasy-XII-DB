#!/usr/bin/env python3
"""census_jsondata_names.py - the shipped JSON parameter corpus, joined against the binary.

What this is
------------
`jsondata/maps/*.json` is 459 files of per-area rendering settings **with the engine's own member
names in plain text** -- `mDofFocusDistance`, `mShadowValueLerpMinForMap`, `mSAOBiasSce`. It is a
name oracle for the visual-tuning system, the same role `ff12-script` plays for EBP.

**And an oracle is never an authority.** A name in an authored file proves what the AUTHORING TOOL
called a value; on its own it proves nothing about the binary, which is why the evidence standard
caps authored game data at tier 9. So this does not stop at listing names: it asks whether the
shipping binary contains each one as a literal string, and reports the two populations separately.

Why the join is worth doing
---------------------------
A key present in the binary is no longer merely authored intent. It is a **string tied to a body**
-- tier 2 -- with an xref to the function that reads it, and therefore a direct route from an
authored name to the struct field it lands in.

A key absent from the binary is the more interesting half, and this corpus shows why: the misses
concentrate in names like `mCascadeNumberCheckBoxCheckState` and `mCascadePartition0LockCheckBox-
CheckState`. **Those are a developer tuning tool's own UI state, shipped inside the game's data.**
The engine never reads them.

**But absence of a string is not proof of inertness** -- the standing rule, established here by
`PClusterHeaderBase` (eighteen recovered fields, zero name strings). A JSON reader that dispatches
on a hash needs no literal. So this reports *"no literal found"*, and a format sheet must write
*"no reader found by string search"*, never *"unused"*.

Usage
-----
    python census_jsondata_names.py --vbf "<...>\\FFXII_TZA.vbf" \
        --exe Tools/work/exe/FFXII_TZA.exe \
        --out Tools/work/formats/jsondata-parameter-names.tsv
    python census_jsondata_names.py --self-test
"""
import argparse
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# vbfextract.py lives with the agent tooling, four levels up from gfz-scripts. Resolved here
# rather than left to PYTHONPATH, because a mixed-separator PYTHONPATH on Windows fails silently
# enough to look like a missing file.
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                                 "agent_flow", "tools")))

# Suffixes that mark a key as belonging to the authoring tool's interface rather than the engine.
# Listed explicitly, and the classification is reported beside the string-presence result rather
# than merged into it -- two independent signals agreeing is evidence; one signal renamed twice is
# not.
EDITOR_MARKS = ("CheckBoxCheckState", "LockCheckBox", "UseStateCheckBox", "CheckState")


def load_keys(vbf, subdir):
    """key -> (files containing it, an example file). Requires vbfextract on the path."""
    import vbfextract as V
    f = io.open(vbf, "rb")
    names, blocks = V.load_index(f)
    want = [p for p in names
            if ("/%s/" % subdir) in p.replace("\\", "/") and p.lower().endswith(".json")]
    counts = collections.Counter()
    example = {}
    bad = 0
    for p in want:
        try:
            obj = json.loads(V.read_entry(f, names, blocks, p).decode("utf-8-sig"))
        except Exception:
            bad += 1
            continue
        if not isinstance(obj, dict):
            continue
        for k in obj:
            counts[k] += 1
            example.setdefault(k, p)
    return counts, example, len(want), bad


def is_editor(key):
    return any(m in key for m in EDITOR_MARKS)


def string_vas(exe_path, keys):
    """key -> canonical VA of its first literal occurrence, or None."""
    import ext_string_probe as P
    blob = io.open(exe_path, "rb").read()
    secs = P.sections(blob)
    out = {}
    for k in keys:
        i = blob.find(k.encode("ascii", "ignore"))
        out[k] = P.to_va(secs, i) if i >= 0 else None
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vbf")
    ap.add_argument("--exe")
    ap.add_argument("--subdir", default="maps")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()
    if not (a.vbf and a.exe):
        return ap.error("--vbf and --exe required")

    counts, example, nfiles, bad = load_keys(a.vbf, a.subdir)
    vas = string_vas(a.exe, list(counts))

    present = [k for k in counts if vas[k]]
    absent = [k for k in counts if not vas[k]]
    ed_absent = [k for k in absent if is_editor(k)]
    ed_present = [k for k in present if is_editor(k)]

    print("JSONDATA PARAMETER CORPUS - jsondata/%s" % a.subdir)
    print("  %d files (%d unparseable), %d distinct keys" % (nfiles, bad, len(counts)))
    print("")
    print("  literal string IN the binary : %3d   <- tier 2, an xref away from its reader"
          % len(present))
    print("  no literal found             : %3d   <- NOT proof of inertness" % len(absent))
    print("")
    print("  of the absent, %d carry an authoring-tool marker (%s)"
          % (len(ed_absent), ", ".join(EDITOR_MARKS)))
    print("  of the present, %d do        <- these would contradict the reading" % len(ed_present))
    unexplained = [k for k in absent if not is_editor(k)]
    print("")
    print("  ABSENT AND NOT TOOL-MARKED - %d genuinely open:" % len(unexplained))
    for k in sorted(unexplained):
        print("      %-46s in %d file(s)" % (k, counts[k]))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as o:
            o.write("# jsondata/%s parameter corpus - census_jsondata_names.py\n" % a.subdir)
            o.write("# %d files, %d keys. `va` is the canonical VA of the key's first literal\n"
                    % (nfiles, len(counts)))
            o.write("# occurrence in FFXII_TZA.exe; empty means NO LITERAL FOUND, which is not\n")
            o.write("# the same as unread - a reader dispatching on a hash needs no literal.\n")
            o.write("key\tfiles\tva\ttool_marked\texample\n")
            for k in sorted(counts):
                o.write("%s\t%d\t%s\t%s\t%s\n"
                        % (k, counts[k], "%08X" % vas[k] if vas[k] else "",
                           "yes" if is_editor(k) else "", example[k]))
        print("\nwrote %s" % a.out)
    return 0


def self_test():
    ok = True
    if not is_editor("mCascadeNumberCheckBoxCheckState"):
        print("SELF-TEST FAILED: tool marker not detected"); ok = False
    if is_editor("mDofFocusDistance"):
        print("SELF-TEST FAILED: engine parameter marked as tool state"); ok = False
    if is_editor("mShadowValueLerpMinForMap"):
        print("SELF-TEST FAILED: false positive on a Lerp name"); ok = False
    if not ok:
        return 1
    print("self-test ok: tool-state suffixes detected, engine parameter names not falsely marked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
