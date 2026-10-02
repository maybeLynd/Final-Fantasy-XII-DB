"""fa5_check.py - FABLE (2026-10-02): the result-record initialiser 003848E0 fills 32, not 33, entries in each status array.
The loop counter is edx = r8 + 0x21 with r8 = -1 (or r8, -1), decremented once per iteration until zero. Control C0: the
memset size 0x140 the register row also cites must decode, or nothing below is trusted. PASS/FAIL; FAILS n."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts", "disasm_fn.py"))
def dis(a, n): return subprocess.run([sys.executable, K, hex(a), hex(n)], capture_output=True, text=True, encoding="utf-8").stdout
CHECKS = [
    ("C0 control: memset size 0x140", 0x3848EF, 0x6, "mov r8d, 0x140"),
    ("L1 r8 = -1", 0x3848FA, 0x4, "or r8, 0xffffffffffffffff"),
    ("L2 counter = r8 + 0x21 (= 32)", 0x384925, 0x4, "lea edx, [r8 + 0x21]"),
    ("L3 dword array from +0x5C", 0x3848FE, 0x4, "lea rcx, [rbx + 0x5c]"),
    ("L4 word array from +0xDC", 0x384916, 0x7, "lea rax, [rbx + 0xdc]"),
    ("L5 one decrement per iteration", 0x38495F, 0x4, "sub rdx, 1"),
    ("L6 loop back while nonzero", 0x384963, 0x2, "jne 0x384950"),
]
fails = 0
for name, a, n, want in CHECKS:
    out = dis(a, n); ok = want in out; fails += not ok
    print("%s  %s  | %s" % ("PASS" if ok else "FAIL", name, out.strip().splitlines()[0] if out.strip() else "(none)"))
print("count = -1 + 0x21 = %d" % (-1 + 0x21))
print("FAILS %d" % fails)
