"""HM-1 / RenderStrideC0Element: the second skeleton is the element row's PARENT row (OPUS, 2026-09-27). Control. Static.

003703A0 runs on an element row r14 (RenderStrideC0Element, 0xC0 per row, reached through 002ED570 on its bank).
  S1 +0x0C is the encoded pointer to the row's parent: every writer stores 0020E620 of bank[row +0x08 parentSlot] -
     0046E300 (0046E31E-0046E35A), 0046E370 (0046E38E-0046E3CA), 0046E420 (0046E450-0046E47A) - or encoded null
     (0046E420's -1 arm 0046E470; the constructor 003721E0 at 00372201-00372208 with ecx = 0)
  S2 +0xA8 is the row's character-render-record index: all five u16 readers take 0xFFFF as none, else
     [022C6F28] + index * 0x740, and a record whose +0x284 is 0 counts as none - 003703DC (this row), 00370524 (the
     parent row reached through +0x0C), 0037153C, 003724AE, 003738C8
  S3 so the mapped pose path's 'other record' (HM-1's second skeleton) is the render record of the element's parent
     row: 003703A0 decodes [r14+0x0C] (00370512-00370516) and takes that row's +0xA8 (00370524), then builds the
     joint map with 0017EF60(this +0x6B8, parent +0x6B8, map) (0037059E-003705AC)
  S4 the parent linker 0046E420 is called by the presentation-entry initialiser 0041D220 and rebuild 0041D820, 003E6F90
     and 004242B0 (rel32 scan)
Not claimed: who writes parentSlot +0x08, and so which parent the hc1006_03 row has in shipped data; +0xA8's writer.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size):
    out = {}
    for x in cs.disasm(d[off(a):off(a) + size], a):
        s = "%s %s" % (x.mnemonic, x.op_str)
        m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
        if m: s += " ; %08X" % (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16))
        out[x.address] = s
    return out
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

A = ins(0x46E300, 111); B = ins(0x46E370, 111); C = ins(0x46E420, 144); K = ins(0x3721E0, 0x98)
check("S1 +0x0C = 0020E620(bank[row+0x08]) or encoded null, at every writer",
      A[0x46E31E] == "mov edx, dword ptr [rbx + 8]" and A[0x46E349] == "call 0x2ed570" and A[0x46E355] == "call 0x20e620"
      and A[0x46E35A] == "mov dword ptr [rbx + 0xc], eax"
      and B[0x46E38E] == "mov edx, dword ptr [rbx + 8]" and B[0x46E3B9] == "call 0x2ed570" and B[0x46E3C5] == "call 0x20e620"
      and B[0x46E3CA] == "mov dword ptr [rbx + 0xc], eax"
      and C[0x46E450] == "mov edx, dword ptr [rdi + 8]" and C[0x46E45B] == "call 0x2ed570" and C[0x46E470] == "xor ecx, ecx"
      and C[0x46E472] == "call 0x20e620" and C[0x46E47A] == "mov dword ptr [rdi + 0xc], eax"
      and K.get(0x372208) == "mov dword ptr [rbx + 0xc], eax" and K.get(0x372201) == "call 0x20e620"
      and any(v == "xor ecx, ecx" for a, v in K.items() if 0x3721E0 <= a < 0x372201))

R = ins(0x3703A0, 0x300)
def reader(tab, ld, reg_idx, imul, add):
    return (tab.get(ld, "").startswith("movzx") and "+ 0xa8]" in tab.get(ld, "") and tab.get(imul, "").endswith(", 0x740")
            and tab.get(add, "").endswith("; 022C6F28"))
T1 = ins(0x3714A0, 0x100 + 0xC0); T2 = ins(0x3723B0, 0x140); T3 = ins(0x373860, 0xC0)
ok = (reader(R, 0x3703DC, None, 0x3703F6, 0x3703FD) and R[0x370404].startswith("cmp dword ptr [rsi + 0x284]")
      and reader(R, 0x370524, None, 0x37053A, 0x370541) and R[0x37052B] == "cmp cx, -1" and R[0x370548].startswith("cmp dword ptr [rbx + 0x284]")
      and reader(T1, 0x37153C, None, 0x37155D, 0x371564) and T1[0x37156B].startswith("cmp dword ptr [rsi + 0x284]")
      and reader(T2, 0x3724AE, None, 0x3724CE, 0x3724D5) and T2[0x3724DC].startswith("cmp dword ptr [rcx + 0x284]")
      and reader(T3, 0x3738C8, None, 0x3738F6, 0x3738FD) and T3[0x373904].startswith("cmp dword ptr [r13 + 0x284]")
      and R[0x3703E8] == "cmp ax, -1" and T1[0x37154E] == "cmp dx, -1" and T2[0x3724C4] == "cmp ax, -1"
      and T3[0x3738D5] == "cmp ax, -1")
check("S2 +0xA8 is a render-record index at all five u16 readers (0xFFFF none; x0x740 into [022C6F28]; +0x284 == 0 none)", ok)

check("S3 the mapped path's second skeleton is the parent row's render record",
      R[0x370512] == "mov ecx, dword ptr [r14 + 0xc]" and R[0x370516] == "call 0x20e600"
      and R[0x370524] == "movzx ecx, word ptr [rax + 0xa8]" and R[0x37059E] == "mov rdx, qword ptr [rbx + 0x6b8]"
      and R[0x3705A5] == "mov rcx, qword ptr [rsi + 0x6b8]" and R[0x3705AC] == "call 0x17ef60")

callers = set()
for ch, vs, va, rs, ro in SECS:
    if ch & 0x20000000:
        for p in range(ro, ro + rs - 5):
            if d[p] == 0xE8 and BASE + va + p - ro + 5 + struct.unpack_from("<i", d, p + 1)[0] == 0x46E420:
                callers.add(BASE + va + p - ro)
fl = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: fl[int(c[0], 16)] = int(c[2])
    except ValueError: pass
own = sorted({f for s in callers for f in fl if f <= s < f + fl[f]})
check("S4 the parent linker's callers: 0041D220, 0041D820, 003E6F90, 004242B0",
      own == [0x3E6F90, 0x41D220, 0x41D820, 0x4242B0], str(["%08X" % f for f in own]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
