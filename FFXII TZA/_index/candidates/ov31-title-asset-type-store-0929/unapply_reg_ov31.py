"""Withdraw ONLY SWE2-STRUCT's own OV-31 register cell from the worktree (restores the prior cell text),
so a peer's whole-file publish of OPEN-QUESTIONS.md cannot sweep it in. Idempotent. Re-apply with
apply_ov31.py when the register is publishable."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], "--check"]
spec = importlib.util.spec_from_file_location("a", os.path.join(HERE, "apply_ov31.py"))
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)          # --check: loads constants, writes nothing
L = a.load(a.REG)
for i, ln in enumerate(L):
    if ln.startswith("| OV-31 |") and a.REG_NEW in ln:
        L[i] = ln.replace(a.REG_NEW, a.REG_OLD, 1)
        with open(a.REG, "w", encoding="utf-8", newline="") as f:
            f.write("".join(L))
        print("withdrawn")
        break
else:
    print("nothing to withdraw")
