"""lift_holds.py CAND_DIR [--apply] - apply a readiness package's OPUS-HELD edits once their pages are clean (OPUS, 2026-10-02).

For every edit apply_by_owner.py classes as OPUS-HELD: refuse if the page is dirty; find the first line of OLD in the page
and `git blame --porcelain` it; when the last writer's commit subject starts with another identity (FABLE, ASTRA,
FRONTIER, SWE2-*, EC7-*), the edit goes to that identity (printed as ROUTE) instead of being applied. The rest are applied
through the package's own applier (its main() over the filtered EDITS), so the strike/idempotency logic is the
applier's. Prints APPLY / ROUTE / DIRTY counts and the applier's FAILS line.
"""
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA"))
IDENT = re.compile(r"^(FABLE|ASTRA|FRONTIER|SWE2[-A-Z0-9]*|EC7-\d+|SWE2CONTRACT[-A-Z0-9]*)\b")


def ident_of(subject):
    m = IDENT.match(subject)
    if not m:
        return "OPUS"
    s = m.group(1)
    if s.startswith(("SWE2-EC7", "EC7-")):
        return "SWE2-EC7"
    if s.startswith("SWE2CONTRACT"):
        return "SWE2-CONTRACT"
    if s.startswith("SWE2-"):
        return "-".join(s.split("-")[:2])
    return s


def blame_subject(page, line_no):
    out = subprocess.run(["git", "-C", DB, "blame", "-L", "%d,%d" % (line_no, line_no), "--porcelain", "--", page],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    for l in out.splitlines():
        if l.startswith("summary "):
            return l[8:]
    return ""


def main():
    cand = sys.argv[1]
    apply = "--apply" in sys.argv
    sys.path.insert(0, cand)
    spec = importlib.util.spec_from_file_location("abo", os.path.join(cand, "apply_by_owner.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    held = [e for e in m.base.EDITS if m.owner_of(e) == "OPUS-HELD"]
    keep, route, dirty = [], [], []
    for e in held:
        page = e[0]
        st = subprocess.run(["git", "-C", DB, "status", "--short", "--", page], capture_output=True, text=True).stdout.strip()
        if st:
            dirty.append(e)
            continue
        text = open(os.path.join(DB, page), encoding="utf-8", errors="replace").read()
        first = e[1].split("\n")[0]
        i = text.find(first)
        if i < 0:
            keep.append(e)  # the applier decides (ALREADY or REFUSING)
            continue
        who = ident_of(blame_subject(page, text.count("\n", 0, i) + 1))
        (keep if who == "OPUS" else route).append((e, who) if who != "OPUS" else e)
    print("held %d: APPLY %d, ROUTE %d, DIRTY %d" % (len(held), len(keep), len(route), len(dirty)))
    for e, who in route:
        print("  ROUTE %-14s %s :: %s" % (who, e[0].split("/")[-1], e[1][:60].replace("\n", " ")))
    for e in dirty:
        print("  DIRTY %s" % e[0].split("/")[-1])
    m.base.EDITS = keep
    if apply:
        sys.argv = [sys.argv[0], "--apply"]
    else:
        sys.argv = [sys.argv[0]]
    return m.base.main()


if __name__ == "__main__":
    sys.exit(main())
