#!/usr/bin/env python3
"""boundary_discharge.py - which of an experiment's scripted boundaries have been executed as the SUBJECT of
another record? (OPUS, 2026-09-25)

The per-row runtime analysis (s02-runtime-rejudged-against-exp191.md, s14-runtime-boundaries-discharged.md)
asks, for each stub an execution disclosed, whether a separate record ran that body as shipped bytes. This
automates the lookup; it proves nothing by itself - a hit must still be read.

A record's scripted boundaries = the 8-hex addresses in the paragraph(s) that contain "scripted" and
"boundar" (case-insensitive), up to the next blank line. A boundary is DISCHARGED-BY record R when R's
title/heading lines or its "Scope"/"Executed bodies" paragraph name the address (with or without the leading
00) - i.e. R made it its subject, not a passing mention.

    boundary_discharge.py EXP-149 [EXP-150 ...]
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402

EXPDIR = os.path.join(G.DB, "_experiments")
ADDR = re.compile(r"(?<![0-9A-Fa-f])(?:00)?([0-9A-Fa-f]{6})(?![0-9A-Fa-f])")


def rec_path(n):
    for f in sorted(os.listdir(EXPDIR)):
        if f.startswith("EXP-%s-" % n) and f.endswith(".md"):
            return os.path.join(EXPDIR, f)
    return None


def paragraphs(text):
    return re.split(r"\n\s*\n", text)


def boundaries(text):
    """Addresses named as scripted boundaries. Parenthetical context ('via X', 'behind X', 'inside X') is
    dropped, and so is any address the record itself lists as running REAL (EXP-150 names 00237040 and
    00304630 only as context, and lists both among its real bodies)."""
    real = set()
    for p in paragraphs(text):
        if re.search(r"\breal\b", p, re.I) and not re.search(r"scripted", p, re.I):
            real |= {m.group(1).upper() for m in re.finditer(r"`(?:00)?([0-9A-Fa-f]{6})`", p)}
    out = []
    for p in paragraphs(text):
        if re.search(r"scripted", p, re.I) and re.search(r"boundar", p, re.I):
            q = p
            while True:
                r = re.sub(r"\([^()]*\)", "", q)
                if r == q:
                    break
                q = r
            for m in re.finditer(r"`(?:00)?([0-9A-Fa-f]{6})`", q):
                a = m.group(1).upper()
                if a not in out and a not in real:
                    out.append(a)
    return out


def subject_text(text):
    """Title (incl. YAML continuation lines), H1 headings, and every Scope/Executed section or paragraph."""
    L = text.splitlines()
    subj = []
    in_title = False
    for l in L[:60]:
        if l.startswith("title:"):
            in_title = True
            subj.append(l)
            continue
        if in_title and (l.startswith("  ") or l.startswith("\t")):
            subj.append(l)
            continue
        in_title = False
        if l.startswith("# "):
            subj.append(l)
    grab = False
    for l in L:
        if l.startswith("#"):
            grab = bool(re.search(r"scope|executed bodies|executed", l, re.I))
            continue
        if grab:
            subj.append(l)
    for p in paragraphs(text):
        if re.match(r"\s*(\*\*)?(Scope|Executed bodies|Executed)", p, re.I):
            subj.append(p)
    return "\n".join(subj).upper()


def main():
    recs = {}
    for f in sorted(os.listdir(EXPDIR)):
        m = re.match(r"EXP-(\d{3})-", f)
        if m and f.endswith(".md"):
            recs[m.group(1)] = io.open(os.path.join(EXPDIR, f), encoding="utf-8", errors="replace").read()
    subj = {k: subject_text(t) for k, t in recs.items()}
    for arg in sys.argv[1:]:
        n = re.sub(r"\D", "", arg).zfill(3)
        t = recs.get(n)
        if not t:
            print("EXP-%s: no record" % n)
            continue
        b = boundaries(t)
        print("EXP-%s: %d scripted boundaries" % (n, len(b)))
        done = 0
        for a in b:
            hits = [k for k, s in subj.items() if k != n and re.search(r"(?<![0-9A-F])(00)?%s(?![0-9A-F])" % a, s)]
            done += bool(hits)
            print("  %s  %s" % (a, ("executed as subject in EXP-" + ", EXP-".join(hits)) if hits else "-- not the subject of any record"))
        print("  discharged: %d / %d" % (done, len(b)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
