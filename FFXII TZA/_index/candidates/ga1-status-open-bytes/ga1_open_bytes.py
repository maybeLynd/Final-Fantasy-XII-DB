"""ga1_open_bytes.py - GA-1: no code reads status_data.bin row bytes +0x11, +0x12 and +0x14..+0x1D
(FABLE, Claude Opus 5.5, 2026-09-27). Static; runs ga1_row_follower.py (a may-taint follower of status-row pointers
from the registry slot 02EBF118 through copies, spills, jump-table arms, callee arguments and row-returning
accessors) and checks its report.
  G1 control: the follower finds the established reads - +0x20 in 00387CB0 (00387E5D), 003908A0 (003909DC) and
     0038FCE0 (0038FE0D); +0x08 in 00387730 (003877A6); +0x13 at 0031E241 in the query filler's jump-table arm.
  G2 no reported row access overlaps +0x11..+0x1D other than the one-byte +0x13 read.
  G3 no row pointer is passed to a callee or stored outside the stack (so nothing reads a row the follower lost).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
out = subprocess.run([sys.executable, str(HERE / "ga1_row_follower.py")], capture_output=True, text=True).stdout
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
acc = []
sec = out.split("== row accesses (offset, width) ==")[1].split("==")[0]
for l in sec.splitlines():
    m = re.match(r"\+0x([0-9A-F]+) w(\d+) ([0-9A-F]{8}) in ([0-9A-F]{8})", l.strip())
    if m: acc.append((int(m.group(1), 16), int(m.group(2)), m.group(3), m.group(4)))
sites = {a[2] for a in acc}
need = {"00387E5D", "003909DC", "0038FE0D", "003877A6", "0031E241"}
check("G1 control: the established +0x20, +0x08 and +0x13 reads are found", need <= sites, "missing %s; %d accesses" % (sorted(need - sites), len(acc)))
bad = [a for a in acc if a[0] <= 0x1D and a[0] + a[1] > 0x11 and not (a[0] == 0x13 and a[1] == 1)]
check("G2 nothing reads +0x11, +0x12 or +0x14..+0x1D", not bad, str(bad))
calls = out.split("== calls receiving R ==")[1].split("==")[0].strip()
escs = out.split("== escapes (R/H stored to non-stack memory) ==")[1].strip()
check("G3 no row pointer is handed to a callee or stored outside the stack", not calls and not escs, "calls %r escapes %r" % (calls[:80], escs[:80]))

# G4 / G5 - which on-screen list each order key feeds (the last open part of GA-1), read from the bytes.
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(ns)]
def off(v):
    for vs, va, rs, ro in secs:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a, n=1): return [("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(a) + 32], a)][:n]
def has(a, text): return at(a)[0] == text
# the listing index L selects a cached ordering table, identically in the three table readers
g4 = (has(0x2733A6, "mov ecx, 0x1500") and has(0x2733AD, "mov ecx, 0x1800") and has(0x2733B4, "mov ecx, 0x1600") and has(0x2733BB, "mov ecx, 0x1700")
      and has(0x27342C, "add rax, 0x1500") and has(0x271FE6, "mov eax, 0x1500")
      # and 00275E40 counts with the matching keys: L0 +0x21, L1 +0x23, L2 +0x22, L3 +0x24
      and has(0x275EA8, "cmp byte ptr [rdx + 0x21], 0xff") and has(0x275ED7, "cmp byte ptr [rdx + 0x23], 0xff")
      and has(0x275EB4, "movzx ecx, byte ptr [rax + 0x22]") and has(0x275EAE, "cmp byte ptr [rdx + 0x24], 0xff"))
check("G4 the listing index selects the cached orderings: L0 +0x1500 (key +0x21), L1 +0x1700 (+0x23), L2 +0x1600 (+0x22), L3 +0x1800 (+0x24)", g4)
g5 = {
 "overhead icon: 002C6F70 calls 00273160, which reads the +0x1700 table (row +0x13)": has(0x2C71D0, "call 0x273160") and has(0x2731B0, "mov r9, qword ptr [rcx + rax + 0x1700]"),
 "target info: 002BFD20 calls 00272F80 with L2 (row +0x27)": has(0x2C01D6, "call 0x272f80") and has(0x2C01D2, "lea r8d, [rdx - 0x1c]"),
 "HUD panel: 0029A0A0 and 00297D10 pass L0 (row +0x26)": has(0x29A423, "call 0x273380") and has(0x29A417, "xor edx, edx") and has(0x297D62, "call 0x271fb0") and has(0x297D58, "xor edx, edx"),
 "party panel: 00283E40 builds the +0x10 list with 002D02C0": has(0x284044, "call 0x2d02c0"),
 "+0x02: read by the reaction queue 003BBD00": has(0x3BBD79, "cmp byte ptr [rax + 0x24], 0xff"),
}
check("G5 each key's list user is where the record says", all(g5.values()), str([k for k, v in g5.items() if not v]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
