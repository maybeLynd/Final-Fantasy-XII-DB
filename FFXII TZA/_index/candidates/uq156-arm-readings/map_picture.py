"""map_picture.py - control for UQ-156's map-picture reading (FABLE, Claude Opus 5.5, 2026-09-26).

Re-derives from the shipping image:
  A. 00404230 pushes GS register records in the order TEX0_1 (6), TEX1_1 (0x14), CLAMP_1 (8), TEST_1 (0x47), with
     TEX1 = 0x60 and TEST = 0x3001, TEX0 = [texture+0x30] + (byte[record+0x5C] * 4 << 37), and ends on the
     00272590 quad emit.
     Known positive: the same detector finds the same four tags in 005520F0 (documented on the NPC-name page).
     Planted negative: it finds none in 004043B0 (the line pass).
  B. both arm-4 bodies call 00404230 with rcx = the page's +0x38 draw record, the 6th argument = [[page+0x130]+0x10],
     byte +0x5C forced to 1 before the call and restored after 004043B0.
  C. the track map's 002B8872 byte: loaded only from [[page+0x130]+8]+0x20 (the entry word[+0x44] picks) with no
     xmm read in the slice, so the projected character position does not choose it; and rdi there is still
     [page+0x38] (the only entry is 002B86DD, and no rdi write lies on that path).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
EXE = ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"
BASE = 0x120000
d = EXE.read_bytes()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
    raise ValueError(hex(v))
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return list(cs.disasm(d[off(a):off(b)], a))
def txt(x): return "%s %s" % (x.mnemonic, x.op_str)

fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

def tags(ins):
    """GS register ids stored as `mov qword ptr [rax + 8], imm` (the record's tag word), in order."""
    out = []
    for x in ins:
        m = re.fullmatch(r"qword ptr \[r[a-z0-9]+ \+ 8\], (0x[0-9a-f]+|\d+)", x.op_str) if x.mnemonic == "mov" else None
        if m: out.append(int(m.group(1), 0))
    return out

# A. 00404230
P = dis(0x404230, 0x4043AC)
t = tags(P)
check("A1 00404230 tag order TEX0_1, TEX1_1, CLAMP_1, TEST_1", t == [6, 0x14, 8, 0x47], str([hex(v) for v in t]))
vals = [txt(x) for x in P if re.fullmatch(r"mov qword ptr \[rax\], 0x[0-9a-f]+", txt(x))]
check("A2 TEX1 = 0x60 and TEST = 0x3001", vals == ["mov qword ptr [rax], 0x60", "mov qword ptr [rax], 0x3001"], str(vals))
T = [txt(x) for x in P]
seq = ["movzx ecx, byte ptr [rsi + 0x5c]", "shl ecx, 2", "shl rcx, 0x25", "add rcx, qword ptr [r8 + 0x30]"]
i = T.index(seq[0]) if seq[0] in T else -1
w = T[i:i + 6] if i >= 0 else []
check("A3 TEX0 = [tex+0x30] + (byte[rec+0x5C] * 4 << 37)",
      all(s in w for s in seq) and [w.index(s) for s in seq] == sorted(w.index(s) for s in seq), str(w))
calls = [int(x.op_str, 16) for x in P if x.mnemonic == "call" and x.op_str.startswith("0x")]
check("A4 last emit call is 00272590 (then the cookie check)", calls[-2:] == [0x272590, 0x808C40], str([hex(c) for c in calls[-2:]]))
check("A5 known positive: 005520F0 has the same four tags", tags(dis(0x5520F0, 0x5520F0 + 320)) == [6, 0x14, 8, 0x47])
check("A6 planted negative: 004043B0 has no tag records", tags(dis(0x4043B0, 0x4043B0 + 0x117)) == [])

# B. both arm-4 bodies
for name, a, b, rec in (("track", 0x2B841B, 0x2B8B16, "r13"), ("location", 0x2BBD5C, 0x2BBEEE, "rdi")):
    I = dis(a, b); T = [txt(x) for x in I]
    k = next(j for j, x in enumerate(I) if txt(x) == "call 0x404230")
    before = T[max(0, k - 30):k]
    check("B1 %s: +0x5C forced to 1 before 00404230" % name, "mov byte ptr [%s + 0x5c], 1" % rec in before)
    check("B2 %s: rcx = the record at the call" % name, "mov rcx, %s" % rec in before)
    check("B3 %s: 6th argument = [[page+0x130]+0x10]" % name,
          "mov rax, qword ptr [rax + 0x10]" in before and "mov qword ptr [rsp + 0x28], rax" in before
          or "mov rax, qword ptr [rdi + 0x10]" in before and "mov qword ptr [rsp + 0x28], rax" in before)
    after = T[k:k + 6]
    check("B4 %s: restored after 004043B0" % name, "call 0x4043b0" in after and any(
        re.fullmatch(r"mov byte ptr \[%s \+ 0x5c\], (sil|bl)" % rec, s) for s in after))
    if name == "track":
        j = T.index("mov rdi, qword ptr [r14 + 0x38]")
        stores = [s for s in T if re.match(r"mov \w+ ptr \[rbp - 0x80\],", s)]
        check("B5 track: r13 = [rbp-0x80] = [page+0x38] (one store to the slot)",
              T[j + 1] == "mov qword ptr [rbp - 0x80], rdi" and stores == ["mov qword ptr [rbp - 0x80], rdi"]
              and "mov r13, qword ptr [rbp - 0x80]" in T, str(stores))
    else:
        check("B5 location: rdi = [page+0x38]", T[0] == "mov rdi, qword ptr [r14 + 0x38]")

# C. the 002B8872 byte
S = dis(0x2B882D, 0x2B8875); ST = [txt(x) for x in S]
check("C1 slice opens on [page+0x130] -> +8 -> +0x20 and word[+0x44]",
      ST[:5] == ["mov rax, qword ptr [r14 + 0x130]", "mov rcx, qword ptr [rax + 8]", "mov r9, qword ptr [rcx + 0x20]",
                 "movzx eax, word ptr [r9 + 0x44]", "movzx r10d, word ptr [r9 + 0x40]"], str(ST[:5]))
check("C2 no xmm register in the slice", not any("xmm" in s for s in ST))
check("C3 slice ends in the +0x5C store", ST[-1] == "mov byte ptr [rdi + 0x5c], al")
PROC = dis(0x2B7B80, 0x2B7B80 + 0x12EF)
def branches_into(lo, hi):
    return [x.address for x in PROC if x.mnemonic.startswith("j") and x.op_str.startswith("0x") and lo <= int(x.op_str, 16) <= hi
            and not (lo <= x.address <= hi)]
wr = lambda x: re.match(r"(mov|lea|xor|pop|add|sub|imul|cvt\w+|movzx|movsx|movsxd|and|or) (rdi|edi|di|dil),", txt(x))
check("C4 only 002B86DD enters 002B87EF..002B8872", branches_into(0x2B87EF, 0x2B8872) == [0x2B86DD],
      str([hex(v) for v in branches_into(0x2B87EF, 0x2B8872)]))
check("C5 only 002B861B enters 002B86D9..002B86DD", branches_into(0x2B86D9, 0x2B86DD) == [0x2B861B])
prev = {x.address: p for p, x in zip(PROC, PROC[1:])}
check("C6 no fall-through into 002B87EF or 002B86D9",
      txt(prev[0x2B87EF]).startswith("jmp ") and txt(prev[0x2B86D9]).startswith("jmp "))
check("C7 no rdi write on 002B8431..002B861B or 002B87EF..002B8872",
      not any(wr(x) for x in PROC if 0x2B8431 <= x.address <= 0x2B861B or 0x2B87EF <= x.address < 0x2B8872))
print("FAILS", fails)
sys.exit(1 if fails else 0)
