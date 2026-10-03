"""apply.py [--apply] - correct the reversed edge on the-box-renderer-that-is-never-called.md's UI crossing line
(SWE2-EC7 batch-150): the stat-bar handlers 0029B7D0 / 0029B810 call 002973E0, not the reverse (FABLE, 2026-10-03, on
ASTRA-REQ-FABLE-OV42-GAUGE-BINDING-1003 after SWE2-AUDIT-SPEC's ACCEPT). Anchored; refuses a page with content changes
(an EOL-only difference is allowed and line endings are kept). Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.normpath(os.path.join(HERE, "..", "..", "..", "99-Unresolved-Residual", "Dead-Nine-Patch-Renderer",
                                  "the-box-renderer-that-is-never-called.md"))
OLD = "and the installed callbacks `0029B7D0`/`0029B810` are themselves called by UI's `002973E0`"
NEW = ("and the installed callbacks `0029B7D0`/`0029B810` ~~are themselves called by UI's `002973E0`~~ themselves call "
       "UI's `002973E0` (at `0029B7EA` and `0029B851`; `002973E0` reaches neither handler) *(corrected 2026-10-03, FABLE, "
       "on ASTRA-REQ-FABLE-OV42-GAUGE-BINDING-1003 and SWE2-AUDIT-SPEC's ACCEPT of its evidence; "
       "[`fable-ov42-handler-edge-1003`](../../_index/candidates/fable-ov42-handler-edge-1003/README.md))*")
num = subprocess.run(["git", "diff", "--numstat", "--", P], cwd=HERE, capture_output=True, text=True).stdout.strip()
if num:
    print("REFUSED: content changes on the page:", num); print("FAILS 1"); sys.exit(1)
raw = io.open(P, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
t = raw.replace("\r\n", "\n")
if NEW in t:
    print("ALREADY"); print("FAILS 0"); sys.exit(0)
if t.count(OLD) != 1:
    print("MISS (%d)" % t.count(OLD)); print("FAILS 1"); sys.exit(1)
if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8", newline="").write(t.replace(OLD, NEW).replace("\n", nl)); print("PATCHED")
else:
    print("WOULD PATCH")
print("FAILS 0")
