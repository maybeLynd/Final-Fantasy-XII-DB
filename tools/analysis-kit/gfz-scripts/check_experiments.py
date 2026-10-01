#!/usr/bin/env python3
"""check_experiments.py - did the experiment's result ever reach the document it bears on?

Why
---
`EXP-008` read the field-music table out of the running game and ran the differential over it.
`EXP-009` used the game's own call site as the oracle. Both were RUN, both passed, and
`CONTRACT-field-music-selection.md` §13 still read **"Runtime validation: None"** — naming, as the
experiment to try, the one that had already been done. A later block read that line and did it
again.

The experiments carry a `contract:` frontmatter field for exactly this, and **seven of nine did not
fill it in**. An experiment that does not say what it bears on cannot be checked against it, and a
contract has no way to know it has been overtaken.

What it checks
--------------
    NO OWNER      an experiment with no `contract:` field at all. It may genuinely bear on nothing
                  — `none` with a reason is a valid answer — but silence is not that answer.

    NOT CITED     a RUN experiment naming a contract that does not mention the experiment's id.
                  **This is the field-music failure**, and it is exactly checkable.

    DEAD LINK     a `contract:` path that does not resolve.

    STALE EMPTY   a contract whose runtime-validation section still says "None"/"EMPTY" while a RUN
                  experiment names it. The strongest signal, and the one that cost a whole block.

Reach, stated plainly
---------------------
It compares frontmatter to citations. It cannot tell whether a contract *absorbed* an experiment's
finding, only whether it mentions it — a contract could cite the id and still contradict the result.
That is a human's job; this removes the case where nobody could have noticed at all.
"""
import argparse
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
EXPID = re.compile(r"(EXP-\d{3})")
EMPTY = re.compile(r"\*\*(None|EMPTY)\b", re.I)


def frontmatter(text):
    """-> {key: value} from a leading --- block, values kept as written."""
    lines = text.split(chr(10))
    if not lines or lines[0].strip() != "---":
        return {}
    out = {}
    for l in lines[1:]:
        if l.strip() == "---":
            break
        if ":" in l and not l.startswith((" ", "\t", "-")):
            k, v = l.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def runtime_section(text):
    """-> the body of the '## N. Runtime validation' section, or None."""
    lines = text.split(chr(10))
    start = None
    for i, l in enumerate(lines):
        if l.startswith("## ") and "Runtime validation" in l:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return chr(10).join(lines[start + 1:end]).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--control", action="store_true",
                    help="positive control: a planted RUN experiment its contract cannot cite")
    a = ap.parse_args()

    edir = os.path.join(a.db, "_experiments")
    if not os.path.isdir(edir):
        print("no _experiments directory at %s" % edir)
        return 2

    paths = [os.path.join(edir, f) for f in sorted(os.listdir(edir)) if f.endswith(".md")]

    control_path = None
    if a.control:
        # A clean result and a broken parser print the same thing. Plant one that must be found.
        control_path = os.path.join(edir, "EXP-999-positive-control.md")
        io.open(control_path, "w", encoding="utf-8", newline=chr(10)).write(
            "---" + chr(10)
            + "experiment: EXP-999" + chr(10)
            + "title: positive control - delete me" + chr(10)
            + "status: RUN 2026-01-01 - planted" + chr(10)
            + "contract: ../18-Audio/CONTRACT-field-music-selection.md" + chr(10)
            + "---" + chr(10) * 2 + "# control" + chr(10))
        paths.append(control_path)
        print("control planted: EXP-999, RUN, naming a contract that cannot mention it")
        print()

    no_owner, not_cited, dead, stale = [], [], [], []
    for p in paths:
        rel = os.path.relpath(p, a.db).replace(os.sep, "/")
        text = io.open(p, encoding="utf-8", errors="replace").read()
        fm = frontmatter(text)
        eid = fm.get("experiment") or (EXPID.search(os.path.basename(p)) or [None])[0]
        owner = fm.get("contract")
        status = fm.get("status", "")
        if owner is None:
            no_owner.append((rel, eid))
            continue
        if owner.lower().startswith("none"):
            continue
        cpath = os.path.normpath(os.path.join(os.path.dirname(p), owner.split()[0]))
        if not os.path.isfile(cpath):
            dead.append((rel, eid, owner.split()[0]))
            continue
        ctext = io.open(cpath, encoding="utf-8", errors="replace").read()
        crel = os.path.relpath(cpath, a.db).replace(os.sep, "/")
        if eid and eid not in ctext:
            not_cited.append((rel, eid, crel))
        if status.upper().startswith("RUN"):
            sec = runtime_section(ctext)
            if sec is not None and EMPTY.match(sec.lstrip()):
                stale.append((rel, eid, crel, sec.splitlines()[0][:76]))

    ctrl = [x for x in not_cited if x[1] == "EXP-999"]
    not_cited = [x for x in not_cited if x[1] != "EXP-999"]
    stale = [x for x in stale if x[1] != "EXP-999"]
    if control_path:
        os.remove(control_path)
        if ctrl:
            print("CONTROL: FOUND -- the check can see an uncited experiment.")
        else:
            print("CONTROL: **NOT FOUND** -- the parser sees nothing; results below are void.")
            return 2
        print()

    print("experiments : %d" % len([p for p in paths if p != control_path]))
    print()
    print("NO OWNER    no `contract:` field at all              : %d" % len(no_owner))
    for rel, eid in no_owner:
        print("   %s" % rel)
    print()
    print("NOT CITED   a RUN experiment its contract never names : %d" % len(not_cited))
    for rel, eid, crel in not_cited:
        print("   %s  ->  %s does not mention %s" % (rel, crel, eid))
    print()
    print("DEAD LINK   `contract:` path does not resolve         : %d" % len(dead))
    for rel, eid, owner in dead:
        print("   %s  ->  %s" % (rel, owner))
    print()
    print("STALE EMPTY a contract still calling its runtime section empty : %d" % len(stale))
    for rel, eid, crel, first in stale:
        print("   %s names %s, whose runtime section begins:" % (eid, crel))
        print("      %s" % first)
    print()
    print("This compares frontmatter to citations. A contract can cite an experiment and still")
    print("contradict it; that is a human's job. What this removes is the case where nobody")
    print("could have noticed at all.")
    return 1 if (not_cited or dead or stale) else 0


if __name__ == "__main__":
    sys.exit(main())
