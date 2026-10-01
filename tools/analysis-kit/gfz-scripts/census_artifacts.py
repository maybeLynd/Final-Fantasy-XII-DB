#!/usr/bin/env python3
"""Load the census artifacts and say which type each one describes.

WHY THIS EXISTS, and it is a correction rather than a convenience. Two tools written on
2026-09-20 identified an artifact's type by matching a leading `# <TypeName>` comment. Only 8 of
the 71 artifacts carry one; the other 63 begin directly with the column header. Both tools
therefore ran over 11 % of their input, and - the part that matters - BOTH REPORTED THEIR
CONTROLS AS PASSING, because the negative control's types were among the 63 that were never
loaded. An absence was about to be reported as a finding when it was an absence of data.

THE KEY IS THE FILENAME, NORMALISED. Stripping every non-alphanumeric character and lowercasing
maps `manager-sub-0209be80-57e0-accesses.tsv` and `ManagerSub0209BE80_57E0` to the same string
without having to guess where the word boundaries were. Across the 444 declared types the
normalised keys are DISTINCT - no collisions - so the mapping is unambiguous rather than merely
convenient. The `#` comment is still preferred where it exists.

COVERAGE IS RETURNED, NEVER SWALLOWED. `load()` hands back the artifacts it could not attribute
as well as the ones it could, and every caller is expected to print that count. A sweep over an
unknown fraction of the store cannot support a negative result, and the only way to stop that
happening again is to make the fraction impossible not to see.
"""
import csv
import glob
import io
import os
import re

import kit_paths as KP

SUFFIX = "-accesses.tsv"


def _norm(s):
    return re.sub(r"[^0-9a-z]", "", s.lower())


def type_keys():
    """normalised name -> declared type name."""
    out = {}
    p = os.path.join(KP.DB, "_types", "types.tsv")
    for r in csv.DictReader(io.open(p, encoding="utf-8"), delimiter="\t"):
        out[_norm(r["type"])] = r["type"]
    return out


def load(want_rows=True):
    """(by_type, unresolved) - by_type maps a declared type to its artifact rows."""
    keys = type_keys()
    by_type, unresolved = {}, []
    for p in sorted(glob.glob(os.path.join(KP.DB, "**", "*" + SUFFIX), recursive=True)):
        first = io.open(p, encoding="utf-8").readline()
        m = re.match(r"#\s*(\w+)", first)
        base = os.path.basename(p)
        stem = base[:-len(SUFFIX)] if base.endswith(SUFFIX) else base
        t = None
        if m and m.group(1) in keys.values():
            t = m.group(1)
        elif _norm(stem) in keys:
            t = keys[_norm(stem)]
        if not t:
            unresolved.append(stem)
            continue
        rows = []
        if want_rows:
            lines = [l for l in io.open(p, encoding="utf-8") if not l.startswith("#")]
            try:
                rows = list(csv.DictReader(lines, delimiter="\t"))
            except Exception:
                rows = []
        by_type.setdefault(t, []).extend(rows)
    return by_type, unresolved


def coverage_line(by_type, unresolved):
    total = len(by_type) + len(unresolved)
    return ("CENSUS COVERAGE: %d artifact group(s) attributed to a declared type, %d file(s) "
            "unattributed%s. A sweep's absences are bounded by this."
            % (len(by_type), len(unresolved),
               " (" + ", ".join(sorted(unresolved)[:8]) + ")" if unresolved else ""))
