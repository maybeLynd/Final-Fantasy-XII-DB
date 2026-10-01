"""typed_store.py - control for the image-backed block's +0x30..+0x223 region (FABLE, Claude Opus 5.5, 2026-09-26).

The region the save payload holds at +0x8030..+0x8223 is ONE typed store with three element classes, not a u16[48] and a
u32[101]. Read here:
  T1 the three accessors (00252610 range write, 002527B0 single write, 002526F0 single read) all take the class in ecx
     and address [*(020927C0) + ...]:
       class 6 -> word  [base + idx*2 + 0x30], idx clamped to 0x1F  (u16[32], +0x30..+0x6F)
       class 7 -> byte  [base + idx   + 0x70], idx clamped to 0x1F  (u8[32],  +0x70..+0x8F)
       class 8 -> dword [base + idx*4 + 0x90], idx clamped to 0x64  (u32[101], +0x90..+0x223)
     and a negative index becomes 0.
  T2 the header initialiser clears the region with one memset of 0x1F4 bytes from +0x30 (00253B36..00253B42);
     32*2 + 32 + 101*4 = 500 = 0x1F4, so the three arrays tile it exactly.
  T3 the single read 002526F0 returns 0 unless its third argument is non-zero or 002DDD50 (bit 15 of [[0215E6E0]]) is set.
Planted negative: T1 also asserts that no accessor addresses the u16 class past +0x6F (a u16[48] would need idx up to
0x2F; the clamps are 0x1F).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys, bisect
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
STARTS = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
                errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
def whole(a):
    i = bisect.bisect_right(STARTS, a)
    return list(cs.disasm(d[off(a):off(STARTS[i])], a))
def T(a): return ["%s %s" % (x.mnemonic, x.op_str) for x in whole(a)]
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

for f in (0x252610, 0x2527B0, 0x2526F0):
    X = whole(f); S = T(f)
    base = [rip(x) for x in X if x.mnemonic == "mov" and "qword ptr [rip" in x.op_str]
    acc = [s for s in S if re.search(r"\+ 0x(30|70|90)\]", s) and "rsp" not in s and "qword" not in s]   # not the epilogue
    w16 = [s for s in acc if "word ptr" in s and "dword" not in s]
    w8 = [s for s in acc if "byte ptr" in s]
    w32 = [s for s in acc if "dword ptr" in s]
    ok = (base == [0x20927C0] and w16 and all("*2 + 0x30]" in s for s in w16) and w8 and all("+ 0x70]" in s for s in w8)
          and w32 and all("*4 + 0x90]" in s for s in w32))
    check("T1 %08X: base [020927C0]; u16 at *2+0x30, u8 at +0x70, u32 at *4+0x90" % f, ok,
          "%d/%d/%d accesses" % (len(w16), len(w8), len(w32)))
    subs = [s for s in S if re.fullmatch(r"(sub|cmp) (ecx|esi), [0-9]+", s)]
    clamps = sorted({int(m.group(1), 16) for s in S for m in [re.search(r", (0x1f|0x64)$", s)] if m})
    if "lea edi, [r8 + 0x64]" in S and "lea ebx, [rdi - 0x45]" in S: clamps = sorted(set(clamps) | {0x64, 0x64 - 0x45})   # 00252610 builds them with lea
    check("T1 %08X: class codes 6/7/8 and clamps 0x1F / 0x64 (planted: no clamp above 0x1F for u16)" % f,
          any("6" in s for s in subs) and 0x1F in clamps and 0x64 in clamps
          and not any(re.search(r", 0x2f$", s) for s in S), "subs %s clamps %s" % (subs, [hex(c) for c in clamps]))
M = T(0x253A80)
check("T2 00253A80 clears 0x1F4 bytes from [020927C0] + 0x30 with one memset",
      any(s == "mov r8d, 0x1f4" for s in M) and "lea rcx, [rbx + 0x30]" in M and "call 0x861ec0" in M)
check("T2 the three arrays tile the cleared region exactly", 32 * 2 + 32 + 101 * 4 == 0x1F4)
R = T(0x2526F0)
check("T3 002526F0 returns 0 unless arg3 or 002DDD50 (bit 15 of [[0215E6E0]])",
      "call 0x2ddd50" in R and "test ebx, ebx" in R and "test eax, eax" in R
      and T(0x2DDD50)[:4] == ["mov rax, qword ptr [rip + 0x1e80989]", "mov eax, dword ptr [rax]", "shr eax, 0xf", "and eax, 1"])
print("FAILS", fails)
sys.exit(1 if fails else 0)
