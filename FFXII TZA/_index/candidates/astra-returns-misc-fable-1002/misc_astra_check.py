"""misc_astra_check.py - FABLE's consumer check (2026-10-02) for ASTRA's filecache-key-preprocessing and
owner-admission-scope (both ACCEPTed by SWE2-AUDIT-SPEC). Reads the shipping image through the kit disassembler; PASS/FAIL
per check; FAILS n. Controls: K0 and A0 must decode from their function entries."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts", "disasm_fn.py"))
def dis(a, n):
    return subprocess.run([sys.executable, K, hex(a), hex(n)], capture_output=True, text=True, encoding="utf-8").stdout
CHECKS = [
    ("K0 control: 0020C440 entry tests its path argument", 0x20C440, 0x3, "test rdx, rdx"),
    ("K1 scanner mask: digits (bits 0-9) and A-Z (bits 17-42) of c - '0'", 0x20C497, 0xA, "movabs r8, 0x7fffffe03ff"),
    ("K2 a-z stops the scan", 0x20C4A1, 0x7, "cmp al, 0x19"),
    ("K3 a mask hit (digit or capital, e.g. the C of C:) stops the scan", 0x20C4B4, 0x6, "jb 0x20c4c5"),
    ("K4 gate 0020BE50 compares /hostapp/ ...", 0x20BE93, 0x7, '"/hostapp/"'),
    ("K5 ... through the import slot 008C2FF8", 0x20BE9D, 0x6, "008C2FF8"),
    ("K6 ... and advances 9 on a match", 0x20BEA7, 0x4, "add rbx, 9"),
    ("K7 /host/ advances 6", 0x20BEE1, 0x4, "add rbx, 6"),
    ("A0 control: the group reset 003DD790 entry", 0x3DD790, 0x3, "xor r10d, r10d"),
    ("A1 reset clears each owner's handle+state qword, no state test", 0x3DD7B6, 0x4, "mov qword ptr [rax - 0xd], r10"),
    ("A2 reset clears the group's pending mask", 0x3DD7D0, 0x4, "mov dword ptr [rax + r8*4], r10d"),
    ("A3 the armer admits only owner state 0", 0x3DDA3B, 0x5, "cmp dword ptr [rax + rcx + 4], 0"),
]
fails = 0
for name, a, n, want in CHECKS:
    out = dis(a, n); ok = want in out; fails += not ok
    print("%s  %s  | %s" % ("PASS" if ok else "FAIL", name, " / ".join(l.strip() for l in out.strip().splitlines()) or "(none)"))
print("FAILS %d" % fails)
