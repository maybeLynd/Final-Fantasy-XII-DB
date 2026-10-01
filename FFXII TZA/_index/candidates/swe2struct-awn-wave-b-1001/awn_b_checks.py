# -*- coding: utf-8 -*-
"""awn_b_checks.py - SWE2-STRUCT (for OPUS), 2026-10-01.

Verifies the AWN wave-B edits listed in awn_b_edits.py (SWE2-AUDIT-SPEC's correction wording, second half of
SWE2AUDITSPEC-REQ-OPUS-0930-WAVE-NARROWINGS):

  A  each edit's new text is present exactly once in its target file;
  O  each edit's old text no longer stands outside the new text;
  K  each struck span appears wrapped in ~~ ~~;
  C  control: at the pinned base commit every edit's old text is present and its new text absent, so A/O/K are
     sensitive to the edit actually being made (and would fail on an unedited file);
  T  no front-matter `status:` line of an edited file differs from the base commit (status lines are OPUS's);
  H  every `##` heading this batch added contains "(SWE2-STRUCT for OPUS)";
  R  the register `_index/OPEN-QUESTIONS.md` carries none of this batch's note text, and the four never-edit pages
     carry none of it either;
  P  every table row in this record's README has the header's cell count (no stray literal pipe in a cell).

python -B awn_b_checks.py   (from anywhere; prints FAILS <n> last)
"""
import io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
from awn_b_edits import EDITS  # noqa: E402

BASE = "0ea7dbefc9bb9a5992dfca7a5fc347000db42a37"   # HEAD when the batch started
MARK = "SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's"
NEVER = ["24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md",
         "01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md",
         "17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md",
         "05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md"]
fails = 0


def check(name, ok, detail=""):
    global fails
    print("%-4s %-28s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        fails += 1


def read(rel):
    with io.open(os.path.normpath(os.path.join(ROOT, rel)), encoding="utf-8", newline="") as h:
        return h.read()


def base_blob(rel):
    p = os.path.normpath(os.path.join(ROOT, rel))
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    relgit = os.path.relpath(p, top).replace(os.sep, "/")
    r = subprocess.run(["git", "show", BASE + ":" + relgit], cwd=ROOT, capture_output=True)
    return r.stdout.decode("utf-8")


def norm(t):
    return t.replace("\r\n", "\n")


files = sorted({e["file"] for e in EDITS})
cur = {f: norm(read(f)) for f in files}
base = {f: norm(base_blob(f)) for f in files}

for e in EDITS:
    t, b = cur[e["file"]], base[e["file"]]
    check("A " + e["id"], t.count(e["new"]) == 1, e["file"])
    check("O " + e["id"], e["old"] not in t.replace(e["new"], ""))
    for i, s in enumerate(e["struck"]):
        check("K %s.%d" % (e["id"], i + 1), ("~~" + s + "~~") in t)
    check("C " + e["id"], b.count(e["old"]) == 1 and e["new"] not in b, "base " + BASE[:9])

for f in files:
    st = lambda x: [l for l in x.split("\n")[:12] if l.startswith("status:")]
    check("T " + os.path.basename(f), st(cur[f]) == st(base[f]))
    added = set(l for l in cur[f].split("\n") if l.startswith("## ")) - set(l for l in base[f].split("\n") if l.startswith("## "))
    check("H " + os.path.basename(f), all("(SWE2-STRUCT for OPUS)" in l for l in added), "%d new ## heading(s)" % len(added))

check("R register", MARK not in read("_index/OPEN-QUESTIONS.md"))
for n in NEVER:
    check("R " + os.path.basename(n), MARK not in read(n))

readme = norm(read("_index/candidates/swe2struct-awn-wave-b-1001/README.md"))
bad, tables, width = 0, 0, None
for l in readme.split("\n"):
    if l.startswith("|"):
        cells = l.count("|") - 1
        if width is None:
            width, tables = cells, tables + 1
        elif cells != width:
            bad += 1
    else:
        width = None
check("P README tables", bad == 0 and tables > 0, "%d table(s), %d bad row(s)" % (tables, bad))
for l in readme.split("\n"):
    if l.startswith("## "):
        check("H README " + l[3:30], "(SWE2-STRUCT for OPUS)" in l)

print("EDITS %d in %d files" % (len(EDITS), len(files)))
print("FAILS %d" % fails)
