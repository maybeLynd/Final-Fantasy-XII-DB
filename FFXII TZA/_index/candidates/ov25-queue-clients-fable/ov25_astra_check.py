"""ov25_astra_check.py - FABLE's consumer check (2026-10-02) for ASTRA's namebinding-deletion and lane-stale-release,
both ACCEPTed by SWE2-AUDIT-SPEC, before they correct this record's family S and its stale-lane obligation. Reads the
shipping image through the kit disassembler; PASS/FAIL per check; FAILS n. Control C0: 002EAEB0 must decode from its
entry (the byte load of +0x18), or the rest means nothing."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts", "disasm_fn.py"))
def dis(a, n):
    return subprocess.run([sys.executable, K, hex(a), hex(n)], capture_output=True, text=True, encoding="utf-8").stdout
CHECKS = [
    ("C0 control: 002EAEB0 loads flag byte +0x18", 0x2EAEB0, 0x5, "movzx r8d, byte ptr [rcx + 0x18]"),
    ("N1 removal: +0x18 bit 0x02 set leaves the mark-only arm", 0x2EAEB8, 0x6, "test r8b, 2"),
    ("N2 removal: +0x19 bit 0x04 set also leaves it (the exception)", 0x2EAEBE, 0x6, "test byte ptr [rcx + 0x19], 4"),
    ("N3 mark-only arm: sets +0x18 bit 0x04 ...", 0x2EAEC4, 0x8, "or r8b, 4"),
    ("N4 ... and returns with no other write or call", 0x2EAECC, 0x1, "ret"),
    ("N5 follow-up 002EA6E0 tests +0x18 bit 0x04 first", 0x2EA6EF, 0x4, "test byte ptr [rcx + 0x18], 4"),
    ("L1 stale release 002EAFA0: requested bit already set ...", 0x2EAFB0, 0x4, "jne 0x2eb026"),
    ("L2 ... jumps straight to a ret (no write, no call)", 0x2EB026, 0x1, "ret"),
]
fails = 0
for name, a, n, want in CHECKS:
    out = dis(a, n); ok = want in out; fails += not ok
    print("%s  %s  | %s" % ("PASS" if ok else "FAIL", name, " / ".join(l.strip() for l in out.strip().splitlines()) or "(none)"))
print("FAILS %d" % fails)
