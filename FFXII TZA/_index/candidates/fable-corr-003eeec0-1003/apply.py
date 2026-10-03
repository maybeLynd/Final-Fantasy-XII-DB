"""apply.py [--apply] - correct FABLE's published interior row for `003EEEC0` on the ui-layout page (FABLE, 2026-10-03, on
SWE2-AUDIT-SPEC's REJECT). Refuses while the page has uncommitted changes (a peer's hunk must not ride along).
Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = os.path.join(DB, "16-UI", "Layout-Parameter-System", "ui-layout-parameters-and-editor-schema.md")
OLD = "2 sets it to 3, 3 calls `003EEEC0`+0xB4 with `rcx`;"
NEW = ("2 sets it to 3, ~~3 calls~~ 4 calls `003EEEC0`+0xB4 with `rcx`, and 3 or any other value returns 0 *(corrected "
       "2026-10-03, FABLE, on SWE2-AUDIT-SPEC's REJECT: after the two `sub ecx, 1` the `cmp ecx, 2` at `003EEEC0`+0xA8 "
       "matches state 4, not 3)*;")
if subprocess.run(["git", "diff", "--quiet", "--", P], cwd=HERE).returncode != 0:
    print("REFUSED: the page has uncommitted changes"); print("FAILS 1"); sys.exit(1)
raw = io.open(P, encoding="utf-8", newline="").read()
if NEW in raw:
    print("ALREADY"); print("FAILS 0"); sys.exit(0)
if raw.count(OLD) != 1:
    print("MISS (%d)" % raw.count(OLD)); print("FAILS 1"); sys.exit(1)
if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8", newline="").write(raw.replace(OLD, NEW)); print("PATCHED")
else:
    print("WOULD PATCH")
print("FAILS 0")
