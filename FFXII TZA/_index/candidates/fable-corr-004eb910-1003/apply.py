"""apply.py [--apply] - correct FABLE's H2 homing row for 004EB910 on CONTRACT-boot-fixups.md (SWE2-AUDIT-SPEC batch 4,
2026-10-03): the floats 02064C18 / 02064C28 are set to the SUM of the .data floats 01E02838 + 01E0283C, not to a
constant 1.0. Refuses a dirty page. Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = os.path.join(DB, "00-Engine-Core-Runtime", "CONTRACT-boot-fixups.md")
OLD = "sets floats `02064C18`, `02064C28` to 1.0 (`01E0283C`)"
NEW = ("sets floats `02064C18`, `02064C28` to ~~1.0 (`01E0283C`)~~ the sum of the `.data` floats `01E02838` + "
       "`01E0283C` (file values 0.0 and 1.0) *(corrected 2026-10-03, FABLE, on SWE2-AUDIT-SPEC's review: "
       "`004EBD39` / `004EBD44` load and add the two cells, `004EBDD6` / `004EBDDE` store the sum)*")
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
