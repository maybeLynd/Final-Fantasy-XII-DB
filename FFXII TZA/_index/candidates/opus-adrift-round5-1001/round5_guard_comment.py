"""round5_guard_comment.py DB - add the round-5 line to select_documented_global_leafs.py's count-guard history
(the guard value itself stays 230). Idempotent, EOL-preserving."""
import io, os, sys

p = os.path.join(sys.argv[1], "24-Compiler-And-CRT-Runtime", "Generated-Families", "members", "select_documented_global_leafs.py")
t = io.open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in t else "\n"
anchor = '    assert len(members) == 230, "member count drifted: %d" % len(members)'
add = ("    # 230 again = 230 - 1 since measured A + 1 re-admission (the field runtime pass, whose exact cite binds it, is" + nl +
       "    # DOCUMENTED again after OPUS 56a49cc8c), A-drift round 5 (OPUS for SWE2-EC7, 2026-10-01, opus-adrift-round5-1001)." + nl)
if "A-drift round 5" in t:
    print("already"); sys.exit(0)
assert t.count(anchor) == 1, t.count(anchor)
io.open(p, "w", encoding="utf-8", newline="").write(t.replace(anchor, add + anchor))
print("ok")
