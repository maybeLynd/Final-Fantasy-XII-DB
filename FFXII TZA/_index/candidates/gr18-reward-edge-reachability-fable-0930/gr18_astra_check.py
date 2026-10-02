"""gr18_astra_check.py - FABLE's consumer check (2026-10-02) for the two ASTRA results incorporated into this record:
ard-callback-width (the four instruction facts the (b) variant now cites) and bts-index-binding (cited, data join not
re-run: SWE2-AUDIT-SPEC re-derived it). Reads the shipping image through the kit disassembler. Prints PASS/FAIL per
check and FAILS n. Control: the 'AREA' string the callback loads must decode, or every other check is meaningless."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts", "disasm_fn.py"))
def dis(addr, n):
    r = subprocess.run([sys.executable, K, hex(addr), hex(n)], capture_output=True, text=True, encoding="utf-8")
    return r.stdout
CHECKS = [
    ("C0 control: the callback 003EA710 loads the 'AREA' tag", 0x3EA72C, 0x6, '"AREA"'),
    ("W1 003EA971 the read destination is the full allocator result", 0x3EA971, 0x3, "mov r8, rax"),
    ("W2 003EA976 the request descriptor keeps the low half", 0x3EA976, 0x4, "mov dword ptr [rsp + 0x38], eax"),
    ("W3 003EA97F the read call follows", 0x3EA97F, 0x5, "-> 0032E620"),
    ("W4 003EA732 the callback zero-extends its argument", 0x3EA732, 0x2, "mov ebp, ecx"),
    ("W5 003EA809 the callback publishes rbp as the root 02B5E0C0", 0x3EA809, 0x7, "02B5E0C0"),
]
fails = 0
for name, a, n, want in CHECKS:
    out = dis(a, n); ok = want in out
    fails += not ok
    print("%s  %s  | %s" % ("PASS" if ok else "FAIL", name, out.strip().splitlines()[0] if out.strip() else "(no output)"))
print("FAILS %d" % fails)
