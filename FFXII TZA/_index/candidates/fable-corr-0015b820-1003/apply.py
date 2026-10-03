"""apply.py [--apply] - correct FABLE's published interior row for `0015B820` (the `.dll` test stated backwards) on
what-the-game-asks-windows-for.md (FABLE, 2026-10-03, on SWE2-AUDIT-SPEC's REJECT). Refuses while the page has
uncommitted changes. Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = os.path.join(DB, "24-Compiler-And-CRT-Runtime", "Runtime-Service-Surface", "what-the-game-asks-windows-for.md")
OLD = "`0015A9B0(rsi, 01CC6BE8)` when `00861F20(suffix, 01CC6BF8)` is 0;"
NEW = ("`0015A9B0(rsi, 01CC6BE8)` when `00861F20(suffix, 01CC6BF8)` (\".dll\") is ~~0~~ non-zero *(corrected 2026-10-03, "
       "FABLE, on SWE2-AUDIT-SPEC's REJECT: the `je` after the compare at `0015B820`+0xD0 skips the try when the suffix "
       "is \".dll\")*;")
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
