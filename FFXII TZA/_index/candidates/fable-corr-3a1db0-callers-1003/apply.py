"""apply.py [--apply] - correct the caller count of 003A1DB0 in FABLE's pass-22 crossing paragraph on
CONTRACT-auto-status-rebuild.md (FABLE, 2026-10-03, on OPUS-REQ-FABLE-AUTOSTATUS-3A1DB0-CALLERS-1002). Refuses while
the page has uncommitted changes. Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
P = os.path.join(DB, "10-Status-Periodic-Terminal", "CONTRACT-auto-status-rebuild.md")
OLD = "`RenderCommand_SubmitCurrentBufferAndSwap` `003A1DB0` (16 callers, and it calls"
NEW = ("`RenderCommand_SubmitCurrentBufferAndSwap` `003A1DB0` (~~16 callers~~ 47 direct call sites in 38 functions "
       "*(corrected 2026-10-03, FABLE, on OPUS's census: a raw `E8`/`E9` scan gives 41 calls and 6 tail jumps, as "
       "what-happens-between-two-frames.md states)*, and it calls")
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
