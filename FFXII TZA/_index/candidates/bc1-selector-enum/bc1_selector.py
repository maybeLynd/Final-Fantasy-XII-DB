"""bc1_selector.py - BC-1: what the renderer selector {3, 5} names (FABLE, Claude Opus 5.5, 2026-09-27). Static.

  S1 the producer of the GS-side values: 001EE650(alphaRegister, out, flag) indexes an 81-entry table at 00902750
     (16-byte entries {selector, op, src, dest}) by 27*A + 9*B + 3*C + D, the four 2-bit fields of the GS ALPHA
     register - the equation (A - B) * C + D with A, B, D in {Cs, Cd, 0} and C in {As, Ad, FIX}.
  S2 the table's selector census: 0 on 67 equations (including standard alpha, #10), 1 on 8, 2 on 3, 3 on exactly one
     (#9, (Cs - Cd) * As + Cs), 4 on 2; 5 does not occur in the table.
  S3 5 is a substitution: with the flag argument set, #10 - standard alpha (Cs - Cd) * As + Cd - takes selector 5; and
     for selector 3 or 5 the function overrides the blend factors to ONE (src) and ZERO (dest). It also remaps every
     source-derived factor to its dual-source form (engine 6 / 7 / 2 / 3 -> 0x11 / 0x12 / 0xF / 0x10).
  S4 the flag's route: 0020FF10 passes byte 01F83560, whose only writer is 002105B0; the GiVmax replay 001DB3D0 sets it
     from its command byte +0x638 and resets it to 0 after the packets; +0x638 is 002105C0() - byte 01FD3698 - taken at
     build time (001DB840); 01FD3698's only writer is 002105D0 (thunk 003A3D00), which the effect-element drawers call
     with the element definition's byte +0x74 and then 0.
  S5 the DynGeo shadow classes pass their selector as an immediate through vtable slot 15: 0 (00213FE0), 0xA
     ShadowFinal (002143E0), 9 Shadow (00214540).
  S6 the consumer's special branch: at the five {3, 5} tests in 006C8CA0 (e.g. 006C9484), a selector of 3 or 5 with
     +0x208D8 == 0 binds the resources at renderer +0x1C0 / +0x1D0 through 00623FA0 into slot +0x160; others skip it.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import collections, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

p = dis(0x1EE650, 0x1EE7BA)
check("S1 001EE650 indexes the 81-entry table at 00902750 by 27A + 9B + 3C + D",
      p.get(0x1EE661) == "lea rdi, [rip + 0x7140e8]" and 0x1EE668 + 0x7140E8 == 0x902750
      and p.get(0x1EE67D) == "lea eax, [r11 + r11*2]" and p.get(0x1EE68B) == "lea edx, [rdx + rdx*2]"
      and p.get(0x1EE69D) == "lea ebx, [rdx + rdx*2]" and p.get(0x1EE6A9) == "add r10, r10"
      and p.get(0x1EE6AC) == "mov eax, dword ptr [rdi + r10*8 + 4]" and p.get(0x1EE74E) == "mov eax, dword ptr [rdi + r10*8]"
      and p.get(0x1EE752) == "mov dword ptr [rcx + 0x1c], eax")
T = 0x902750
sel = collections.Counter(); by = collections.defaultdict(list)
for i in range(81):
    s = struct.unpack_from("<I", d, off(T) + i * 16)[0]; sel[s] += 1; by[s].append(i)
std = struct.unpack_from("<IIII", d, off(T) + 10 * 16)
check("S2 selectors: 0 x67, 1 x8, 2 x3, 3 only on #9 (Cs-Cd)*As+Cs, 4 x2, and no 5; #10 is standard alpha (SRC_ALPHA / INV_SRC_ALPHA)",
      dict(sel) == {0: 67, 1: 8, 2: 3, 3: 1, 4: 2} and by[3] == [9] and std == (0, 0, 6, 7), "%s; #10 %s" % (dict(sel), std))
check("S3 the flag turns #10 into 5; for 3 or 5 the factors become ONE / ZERO; source factors are remapped to their dual-source forms",
      p.get(0x1EE749) == "cmp byte ptr [rsp + 0x30], 0" and p.get(0x1EE757) == "cmp ebx, 0xa" and p.get(0x1EE75A) == "mov r8d, 5"
      and p.get(0x1EE76D) == "sub eax, 3" and p.get(0x1EE770) == "test eax, 0xfffffffd" and p.get(0x1EE777) == "mov dword ptr [rcx], 1"
      and p.get(0x1EE77D) == "mov dword ptr [rdx], r8d" and p.get(0x1EE76A) == "xor r8d, r8d"
      and p.get(0x1EE6C9) == "mov dword ptr [rcx], 0x11" and p.get(0x1EE6D7) == "mov dword ptr [rcx], 0x12" and p.get(0x1EE6E5) == "mov dword ptr [rcx], 0xf")
f = dis(0x210116, 0x21013B); s5 = dis(0x2105B0, 0x2105B7); r = dis(0x1DB432, 0x1DB43E); r2 = dis(0x1DB4BC, 0x1DB4C3)
g = dis(0x2105C0, 0x2105C8); h = dis(0x2105D0, 0x2105D6)
check("S4 the flag is 01F83560 <- GiVmax +0x638 <- 01FD3698 at build <- effect definition byte +0x74",
      f.get(0x210116) == "movzx eax, byte ptr [rip + 0x1d73443]" and 0x21011D + 0x1D73443 == 0x1F83560
      and f.get(0x21012D) == "mov byte ptr [rsp + 0x28], al" and s5.get(0x2105B0) == "mov byte ptr [rip + 0x1d72faa], cl" and 0x2105B6 + 0x1D72FAA == 0x1F83560
      and r.get(0x1DB432) == "movzx ecx, byte ptr [rbx + 0x638]" and r.get(0x1DB439) == "call 0x2105b0"
      and r2.get(0x1DB4BC) == "xor ecx, ecx" and r2.get(0x1DB4BE) == "call 0x2105b0"
      and g.get(0x2105C0) == "movzx eax, byte ptr [rip + 0x1dc30d1]" and 0x2105C7 + 0x1DC30D1 == 0x1FD3698
      and h.get(0x2105D0) == "mov byte ptr [rip + 0x1dc30c2], cl" and 0x2105D6 + 0x1DC30C2 == 0x1FD3698
      and dis(0x455C0E, 0x455C1A).get(0x455C15) == "call 0x3a3d00" and "0x74]" in "".join(dis(0x455C06, 0x455C15).values()))
k = {**dis(0x2140C8, 0x2140D0), **dis(0x2140E9, 0x2140EC)}; k2 = {**dis(0x21446D, 0x214475), **dis(0x21448E, 0x214491)}; k3 = {**dis(0x214556, 0x21455E), **dis(0x21457A, 0x21457D)}
check("S5 DynGeo passes 0, 0xA (ShadowFinal) and 9 (Shadow) as the seventh slot-15 argument",
      k.get(0x2140C8) == "mov dword ptr [rsp + 0x30], 0" and k.get(0x2140E9) == "call qword ptr [rax + 0x78]"
      and k2.get(0x21446D) == "mov dword ptr [rsp + 0x30], 0xa" and k2.get(0x21448E) == "call qword ptr [rax + 0x78]"
      and k3.get(0x214556) == "mov dword ptr [rsp + 0x30], 9" and k3.get(0x21457A) == "call qword ptr [rax + 0x78]")
b = dis(0x6C947C, 0x6C94BB)
check("S6 006C8CA0: selector 3 or 5 (with +0x208D8 == 0) binds renderer +0x1C0 / +0x1D0 through 00623FA0 into +0x160",
      b.get(0x6C9484) == "mov eax, dword ptr [rsi + 0x208d4]" and b.get(0x6C948A) == "sub eax, 3" and b.get(0x6C9492) == "jne 0x6c94d4"
      and b.get(0x6C9494) == "mov rcx, qword ptr [rsi + 0x1c0]" and b.get(0x6C94A3) == "call 0x623fa0" and b.get(0x6C94B4) == "mov qword ptr [rsi + 0x160], rax")
print("FAILS", fails)
sys.exit(1 if fails else 0)
