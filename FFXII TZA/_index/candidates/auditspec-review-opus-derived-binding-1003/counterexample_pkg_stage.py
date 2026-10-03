"""counterexample_pkg_stage.py (SWE2-AUDIT-SPEC, 2026-10-03): a tracked input of PROGRESS.md that the binding does not cover.

progress_report.py reads _index/completion-packages/PKG-*.md (stage scan -> PROGRESS.md row "completion packages by stage")
and folds them into its build fingerprint, but they are neither in the inputs the binding records (`bound`) nor in its
as-of set, and the document-tree preimage skips _index. So a commit that moves a package stage leaves the committed
binding CURRENT, and the publish gate (derived_binding.gate -> state()) commits PROGRESS.md still claiming CURRENT.

This script changes nothing: it evaluates the binding at a revision against a read-only view of that revision in which
one PKG file's stage line is edited in memory, and prints the state() result plus what PROGRESS.md renders for packages.
Usage: python counterexample_pkg_stage.py [REV]   (default HEAD)   exit 1 = counter-example reproduced
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "Database/Tools/analysis-kit/gfz-scripts"))
import derived_binding as B

rev = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
BP = "Database/FFXII TZA/_index/progress/GENERATION-BINDING.json"
read_rev = B.git_reader(str(ROOT), rev=rev)
b = B.load(read_rev(BP))
pkgs = [p for p in subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", rev,
                                   "Database/FFXII TZA/_index/completion-packages/"],
                                  capture_output=True, text=True).stdout.splitlines() if "/PKG-" in p]
covered = [p for p in pkgs if p in b["bound"] or any(v.get("path") == p for v in b["as_of"].values())]
print("binding generation:", b.get("generation"), "| declared state:", b.get("state", "CURRENT"))
print("tracked PKG-*.md at %s: %d | covered by the binding (bound or as-of): %d" % (rev, len(pkgs), len(covered)))
STAGE = re.compile(r"\*\*stage\.\*\*\s*`?([A-Za-z][\w-]*)")
target = next(p for p in pkgs if (STAGE.search(read_rev(p).decode("utf-8")) or [None, "research"])[1] != "research")
orig = read_rev(target).decode("utf-8")
m = STAGE.search(orig)
print("edited in memory:", target, "| stage", m.group(1) if m else "?", "-> research")
edited = (orig[:m.start(1)] + "research" + orig[m.end(1):]) if m else orig + "\n**stage.** `research`\n"


def view(rel):
    return edited.encode("utf-8") if rel == target else read_rev(rel)


s = B.state(b, view)
print("state() over the moved input:", s["state"], "| moved:", s["moved"] or "-", "| outputs_bad:", s["outputs_bad"] or "-")
row = [l for l in read_rev("Database/FFXII TZA/PROGRESS.md").decode("utf-8").splitlines() if "completion packages by stage" in l]
print("PROGRESS.md still renders:", row[0][:140] if row else "(no row)")
if s["state"] == "CURRENT" and not covered:
    print("COUNTER-EXAMPLE: a tracked consumed input moved and the surface stays CURRENT")
    sys.exit(1)
print("no counter-example")
