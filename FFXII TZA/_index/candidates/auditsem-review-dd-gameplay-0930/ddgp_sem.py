"""SWE2-AUDIT-SEM: FABLE's DD content work on the 15 gameplay-folder pages (797b72780), re-derived from the certified
image and the shipped data. Capstone and pefile read Tools/work/exe/FFXII_TZA.exe directly; the producer's own scripts are
re-run separately (producer_rerun/) and are not the evidence here. X-checks are claims or corrections of the package, G-checks
are the premises of GR rows, F-checks are findings this review adds (they PASS when the finding reproduces).

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-dd-gameplay-0930/ddgp_sem.py"
"""
import csv
import os
import re
import struct
import subprocess
import sys

import capstone
import pefile

ROOT = os.getcwd()
DB = os.path.join(ROOT, "Database")
EXE = os.path.join(DB, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(DB, "Tools", "work", "graph", "functions.tsv")
pe = pefile.PE(EXE, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
FAILS = []
F = {r["entry"]: r for r in csv.DictReader(open(FUNCS, encoding="utf-8"), delimiter="\t")}
size = {int(k, 16): int(v["body_bytes"] or 0) for k, v in F.items()}
X86 = capstone.x86


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def raw(va, n):
    o = pe.get_offset_from_rva(va - BASE)
    return bytes(pe.__data__[o:o + n])


def body(fn):
    n = size[fn]
    return [i for i in md.disasm(raw(fn, n + 16), fn) if i.address < fn + n]


def at(va):
    return next(md.disasm(raw(va, 16), va))


def rip(i):
    for op in i.operands:
        if op.type == X86.X86_OP_MEM and op.mem.base == X86.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def tgt(i):
    if (i.mnemonic in ("call", "jmp") or i.mnemonic.startswith("j")) and i.operands and i.operands[0].type == X86.X86_OP_IMM:
        return i.operands[0].imm
    return None


def s(i):
    return f"{i.mnemonic} {i.op_str}"


def f32(va):
    return struct.unpack("<f", raw(va, 4))[0]


def name(fn):
    return F["%08X" % fn]["name"]


# ================================ 13 Rewards: the death page, the award page ==========================================
d = {i.address: i for i in body(0x00312280)}
check("X1 00312280 is named BattleUnit_ProcessDefeatRewardsAndLoot in the function table (the struck ...AndRetire)",
      name(0x00312280) == "BattleUnit_ProcessDefeatRewardsAndLoot", name(0x00312280))
check("X2 counter 11 (0xB) is fed with each recipient's awarded LP: 00312484 edx=esi, 00312489 mov cl,0xb, 00312496 call 00316A50",
      s(d[0x00312484]) == "mov edx, esi" and s(d[0x00312489]) == "mov cl, 0xb" and tgt(d[0x00312496]) == 0x00316A50)
b = {i.address: i for i in body(0x00317090)}
check("X3 00317090 (78 B) = span * [+0xE78]u16 + [+0xE70]u16, span = level +0x1C2 - baseline +0x88; ecx=0x11; jmp 00253770",
      size[0x00317090] == 78 and s(b[0x003170AA]) == "movzx edx, byte ptr [rax + 0x1c2]" and s(b[0x003170B1]) == "movzx eax, byte ptr [rax + 0x88]"
      and s(b[0x003170CB]) == "imul edx, ecx" and s(b[0x003170D1]) == "add edx, ecx" and s(b[0x003170D3]) == "mov ecx, 0x11"
      and tgt(b[0x003170D8]) == 0x00253770)
check("X3 00253770 is a 5-byte thunk jmp 00316A50; 002E2380 (12 B) is ecx=0x11 + jmp 00253770 (the second counter-17 feeder)",
      tgt(at(0x00253770)) == 0x00316A50 and size[0x00253770] == 5 and size[0x002E2380] == 12
      and s(at(0x002E2382)) == "mov ecx, 0x11" and tgt(at(0x002E2387)) == 0x00253770)
check("X4 the LP-to-gil test is byte +0x69 / +0x79 bit 4, i.e. bit 12 of the 16-byte layers at +0x68 / +0x78 (effect id 12)",
      s(d[0x00312409]) == "test byte ptr [rdi + 0x69], 0x10" and s(d[0x0031240F]) == "test byte ptr [rdi + 0x79], 0x10"
      and s(d[0x00312421]) == "lea eax, [r12 + rcx]" and s(d[0x00312425]) == "lea r12d, [rax + rcx*4]",
      "gil += level*LP*5 (r12 + rcx + 4*rcx)")
g = body(0x00236780)
check("X5 00236780 (17 B) returns bit 14 of dword [[02EBF190]+4]",
      size[0x00236780] == 17 and rip(g[0]) == 0x02EBF190 and s(g[2]) == "shr eax, 0xe" and s(g[3]) == "and eax, 1")
check("X5 bit 14 is set from request bit 2 of 02089344 (00239A6C test al,4 -> or [rax+4],0x4000 -> and ~4) and 00238A50 sets that bit",
      s(at(0x00239A6C)) == "test al, 4" and s(at(0x00239A77)) == "or dword ptr [rax + 4], 0x4000"
      and rip(at(0x00238A50)) == 0x02089344 and at(0x00238A50).op_str.endswith(", 4"))
check("X6 the experience add is skipped while 00236780 is up (00312429 call, 00312430 jne over the 00312444 store)",
      tgt(d[0x00312429]) == 0x00236780 and d[0x00312430].mnemonic == "jne" and tgt(d[0x00312430]) == 0x0031244A
      and s(d[0x00312444]) == "mov dword ptr [rdi + 0x18c], ecx")
check("X6 and the presentation EXP is replaced by ebp (0) under the same flag (00312505 call, 00312513 cmovne edi, ebp)",
      tgt(d[0x00312505]) == 0x00236780 and s(d[0x00312513]) == "cmovne edi, ebp")
check("X25 sizes: 00319490 148 B, 003377C0 565 B, 00319CA0 394 B (0x18A), 00319A20 227 B",
      (size[0x00319490], size[0x003377C0], size[0x00319CA0], size[0x00319A20]) == (148, 565, 394, 227),
      str((size[0x00319490], size[0x003377C0], size[0x00319CA0], size[0x00319A20])))
check("G19 the drop is attempted only on a nonzero 00319490 answer (00312588 call, 00312597 je)",
      tgt(d[0x00312588]) == 0x00319490 and d[0x00312597].mnemonic == "je")

# ================================ 08 where a stat number comes from =================================================
r = {i.address: i for i in body(0x002FEF30)}
h1 = body(0x002F8E50)
h2 = body(0x002F9180)
check("X7 002F8E50 (30 B) = (r8+1) * ecx * edx / 100 and 002F9180 (21 B) = ecx * edx / 100 (0x51EB851F, sar 5)",
      size[0x002F8E50] == 30 and size[0x002F9180] == 21 and s(h1[0]) == "inc r8d" and "0x51eb851f" in s(h1[1])
      and s(h2[0]) == "imul ecx, edx" and "0x51eb851f" in s(h2[1]))
check("X7 their call sites pass base HP (stats +0x08) with row bytes +0x18/+0x19, and base MP (s16 stats +0x0C) with row +0x1D - no level",
      s(r[0x002FF06F]) == "movzx r8d, byte ptr [rbx + 0x18]" and s(r[0x002FF074]) == "movzx edx, byte ptr [rbx + 0x19]"
      and s(r[0x002FF078]) == "mov ecx, dword ptr [rdi + 8]" and tgt(r[0x002FF07B]) == 0x002F8E50
      and s(r[0x002FF080]) == "movzx edx, byte ptr [rbx + 0x1d]" and s(r[0x002FF084]) == "movsx ecx, word ptr [rdi + 0xc]"
      and tgt(r[0x002FF090]) == 0x002F9180)
check("X9 the two 'affinity' dwords: rsi = stats+0x24 (002FEFAB); row +0x4C ORed into +0x38 (002FF0D3), row +0x48 into +0x3C (002FF0D9)",
      s(r[0x002FEFAB]) == "lea rsi, [rdi + 0x24]" and s(r[0x002FF0A3]) == "mov ecx, dword ptr [rbx + 0x4c]"
      and s(r[0x002FF0D3]) == "or dword ptr [rsi + 0x14], ecx" and s(r[0x002FF0D6]) == "mov ecx, dword ptr [rbx + 0x48]"
      and s(r[0x002FF0D9]) == "or dword ptr [rsi + 0x18], ecx")
check("X8 the main value floors at 1: r15d = 1 (002FF5A7), cmp r14, r15 / jge / mov r8, r15 (002FF7B1-002FF7B6)",
      s(r[0x002FF5A7]) == "mov r15d, 1" and s(r[0x002FF7B1]) == "cmp r14, r15" and s(r[0x002FF7B6]) == "mov r8, r15")

# ================================ 07 the action definition row ======================================================
check("X10 +0x0A is read as a byte at 002F962B (ComputeModifiedResourceCostAmount) and 0031DBD2 (the class-20 filler)",
      s(at(0x002F962B)) == "movzx ebp, byte ptr [rcx + 0xa]" and s(at(0x0031DBD2)) == "movzx ecx, byte ptr [rbp + 0xa]")
hops = list(csv.DictReader(open(os.path.join(DB, "FFXII TZA", "07-Combat-Action", "Action-Definition-Row", "members",
                                             "action-row-reader-hops.tsv"), encoding="utf-8"), delimiter="\t"))
w0A = {(x["site"], x["width"]) for x in hops if x["offset"] == "0x0A"}
check("G5 every +0x0A reader in the UQ-106 hop census reads one byte (so none reads +0x0B through a word); no +0x0B or +0x28 site",
      w0A and all(w == "1" for _, w in w0A) and not [x for x in hops if x["offset"] in ("0x0B", "0x28")], str(sorted(w0A)))
sys.path.insert(0, os.path.join(DB, "FFXII TZA", "_index", "candidates", "uq80-table-field-coverage"))
import pack  # noqa: E402  (the UQ-80 record's section parser; the tallies below are this review's own)
recs, _h = pack.records(0x3C)
w24 = [struct.unpack_from("<H", x, 0x24)[0] for x in recs]
b30 = [struct.unpack_from("<I", x, 0x0C)[0] >> 30 & 1 for x in recs]
t = (len(recs), sum(v == 0xFFFF for v in w24), sum(v != 0xFFFF and v & 0x8000 and not c for v, c in zip(w24, b30)),
     sum(not v & 0x8000 for v in w24))
check("X11 data: 543 rows; +0x24 is 0xFFFF on 68, bit 15 set with +0x0C bit 30 clear on 39, bit 15 clear on 436", t == (543, 68, 39, 436), str(t))
nz0B = [k for k, x in enumerate(recs) if x[0x0B]]
check("X11 data: +0x0B is non-zero (1-3) only on rows 182-207", nz0B == list(range(182, 208)) and max(x[0x0B] for x in recs) == 3)
v3A = sorted({x[0x3A] for x in recs} - {255})
n3A = sum(x[0x3A] != 255 for x in recs)
check("X11 data: +0x3A takes 10-16 on 68 rows, 10 and 11 once each", v3A == list(range(10, 17)) and n3A == 68
      and sum(x[0x3A] == 10 for x in recs) == 1 and sum(x[0x3A] == 11 for x in recs) == 1, f"{v3A} on {n3A}")
r28 = [k for k, x in enumerate(recs) if x[0x28]]
check("X11 data: +0x28 is 120-153 on 26 rows, 0xD0-0xE5 and 0xE7/0xEA/0xED/0xF1 (18 Quickenings + 8 Concurrences)",
      r28 == list(range(0xD0, 0xE6)) + [0xE7, 0xEA, 0xED, 0xF1] and {recs[k][0x28] for k in r28} <= set(range(120, 154)))
check("X11 data: rows 0x9C / 0x9D point at battle-text bank-0 entries 156 / 157 and carry +0x1E = 13 (GR-12)",
      (struct.unpack_from("<H", recs[0x9C], 0x34)[0], struct.unpack_from("<H", recs[0x9D], 0x34)[0], recs[0x9C][0x1E], recs[0x9D][0x1E])
      == (156, 157, 13, 13))
a = {i.address: i for i in body(0x0030AC50)}
check("G6 0030AC50 returns +0x24 & 0x7FFF only for bit 15 set with +0x0C bit 30 clear (0030AD10-0030AD2F)",
      s(a[0x0030AD10]) == "movzx eax, word ptr [rdi + 0x24]" and s(a[0x0030AD1E]) == "test dword ptr [rdi + 0xc], 0x40000000"
      and a[0x0030AD2A].mnemonic == "jns" and s(a[0x0030AD2F]) == "btr eax, 0xf")
check("G6 00325476 and 00325968 are cmp word [rcx+0x24], di / jne 00325702 and 003259E3, with edi = 0xFFFF (00325384)",
      s(at(0x00325476)) == "cmp word ptr [rcx + 0x24], di" and tgt(at(0x0032547A)) == 0x00325702
      and s(at(0x00325968)) == "cmp word ptr [rcx + 0x24], di" and tgt(at(0x0032596C)) == 0x003259E3
      and s(at(0x00325384)) == "mov edi, 0xffff")
k = {i.address: i for i in body(0x00312170)}
check("G7 00312170 sets bit [+0x3A] (003121F5-00312203), ORs +0x13, +0x0C bits 13/14 as bits 8/9, and writes operand kind 10 via 00329E60 (0031225E)",
      s(k[0x003121F5]) == "movzx ecx, byte ptr [rdi + 0x3a]" and s(k[0x00312203]) == "bts ebx, eax"
      and s(k[0x00312218]) == "bts ecx, 8" and s(k[0x00312228]) == "bts ebx, 9" and s(k[0x0031225A]) == "lea ecx, [r8 + 0xa]"
      and tgt(k[0x0031225E]) == 0x00329E60)
# F7: the readers of operand kind 10 are one caller query away
ev = {i.address: i for i in body(0x00301AD0)}
fe = {i.address: i for i in body(0x002FE660)}
check("F7 AiTargetSelector_ResolveOperandValue 00321190 is called with kind 10 by AiOrder_EvaluateTargetSelector (00303084 ecx=0xA, 00303088)",
      name(0x00321190) == "AiTargetSelector_ResolveOperandValue" and s(ev[0x00303084]) == "lea ecx, [r8 + 0xa]" and tgt(ev[0x00303088]) == 0x00321190)
check("F7 ... and by 002FE660 for action ids 0x4122/0x4123 (esi = 0xA at 002FE6CD, 002FE6E7), which then sets / adds / bts / btr the value",
      s(fe[0x002FE6B3]) == "mov ecx, 0x4122" and s(fe[0x002FE6CD]) == "mov esi, 0xa" and s(fe[0x002FE6E5]) == "mov ecx, esi"
      and tgt(fe[0x002FE6E7]) == 0x00321190 and s(fe[0x002FE732]) == "bts r9d, ebx" and s(fe[0x002FE73D]) == "btr r9d, ebx")

# ================================ 08 ranged recipes ==================================================================
e = {i.address: i for i in body(0x00304850)}
check("X12 the first list runs at execution: BattleUnit_AdvanceStandardActionState calls BattleAction_EvaluateTargetPreviews at 00304F1D, "
      "which calls 00385680 at 00303910; 003859FF is its indirect step call",
      name(0x00304850) == "BattleUnit_AdvanceStandardActionState" and tgt(e[0x00304F1D]) == 0x00303830
      and name(0x00303830) == "BattleAction_EvaluateTargetPreviews" and tgt(at(0x00303910)) == 0x00385680
      and at(0x003859FF).mnemonic == "call" and at(0x003859FF).operands[0].type == X86.X86_OP_MEM)

# ================================ 04 field runtime / battle record kind ============================================
w = {i.address: i for i in body(0x0025DF00)}
jt = BASE + 0x13E3CC
kinds = {kk: BASE + struct.unpack_from("<I", raw(jt + 4 * kk, 4))[0] for kk in range(8)}
check("X13 the wait resolver dispatches kind = slot +0x14 through the table at image+0x13E3CC (0025DFF0-0025E008)",
      s(w[0x0025DFF0]) == "movzx eax, byte ptr [rsi + 0x14]" and "0x13e3cc" in s(w[0x0025DFFD]),
      " ".join("%d:%08X" % (kk, v) for kk, v in kinds.items()))
check("X13 kinds 3 and 6 store +0x27 = 1 (0025E04F, 0025E07A); kind 7 runs 0025E083 and joins kind 6's test at 0025E06E (0025E08F)",
      kinds[3] == 0x0025E027 and kinds[6] == 0x0025E058 and kinds[7] == 0x0025E083
      and s(w[0x0025E04F]) == "mov byte ptr [rsi + 0x27], 1" and s(w[0x0025E07A]) == "mov byte ptr [rsi + 0x27], 1"
      and tgt(w[0x0025E08F]) == 0x0025E06E, "k3 %08X k6 %08X k7 %08X" % (kinds[3], kinds[6], kinds[7]))


def cover27(fn):
    """accesses in fn whose memory operand covers displacement 0x27 of a non-rip base; split into writes and the rest"""
    wr, rd = [], []
    for i in body(fn):
        for n, op in enumerate(i.operands):
            if op.type != X86.X86_OP_MEM or op.mem.base in (0, X86.X86_REG_RIP, X86.X86_REG_RSP) or i.mnemonic == "lea":
                continue
            if op.mem.disp <= 0x27 < op.mem.disp + op.size:
                (wr if n == 0 and i.mnemonic.startswith("mov") else rd).append("%08X %s" % (i.address, s(i)))
    return wr, rd


wr_all, rd_all = [], []
for fn in (0x0025DF00, 0x0025E4C0, 0x002621D0):
    wr_, rd_ = cover27(fn)
    wr_all += wr_
    rd_all += rd_
check("G1 control: the displacement-0x27 sweep over 0025DF00 / 0025E4C0 / 002621D0 finds the 2 sets and the 10 interpreter clears",
      len(wr_all) == 12 and "0025F5CC mov byte ptr [rsi + 0x27], 0" in wr_all, "%d writes" % len(wr_all))
check("G1 and finds no other access covering +0x27 there (byte or wider, any non-rip base)", not rd_all, "; ".join(rd_all[:6]))
c1 = [s(i) for i in body(0x002674B0) + body(0x00267420) if "rbx +" in s(i) and "ptr [rbx" in s(i)]
check("G1 the two callees handed slot+0x18 (002674B0, 00267420) touch only its +4 / +0xA / +0xE (slot +0x1C/+0x22/+0x26), not +0xF",
      c1 and all(re.search(r"\[rbx \+ (0x4|0xa|0xe)\]", x) for x in c1), "; ".join(sorted(set(c1))))
m = body(0x00321810)
check("X14 00321810 (47 B) forms [+0x6A0]+0x19 with lea and stores dl = 0 there (0032181F xor edx,edx; 00321834 mov [rcx], dl)",
      size[0x00321810] == 47 and s(at(0x0032181F)) == "xor edx, edx" and s(at(0x00321824)) == "lea rcx, [rax + 0x19]"
      and s(at(0x00321834)) == "mov byte ptr [rcx], dl")

# ================================ 07/08 combos ======================================================================
check("X15 unit flag bit 22 is set at 003130D2 (or qword [rbx], 0x400000) and cleared in 00308270 (mask 0xFFFFBFFFFFBFFFFF at 003082DF)",
      s(at(0x003130D2)) == "or qword ptr [rbx], 0x400000" and s(at(0x003082CB)) == "movabs rax, 0xffffbfffffbfffff"
      and s(at(0x003082DF)) == "and qword ptr [rbx], rax")
check("X15 the HUD count is two digits one per nibble, capped at 0x12 (00289DE7-00289E08)",
      s(at(0x00289DF2)) == "and r8d, 0xf" and s(at(0x00289DF6)) == "shl r8d, 4" and s(at(0x00289E00)) == "mov eax, 0x12"
      and s(at(0x00289E08)) == "cmovg r8d, eax")
check("G3 00307300 -> 0028E920 (26 B, jmp 00289D70); 0028AAA0 (1,692 B) has one caller, 00289A10 at 00289B7C, walking [+0x428] by +0x18",
      tgt(at(0x00307676)) == 0x0028E920 and tgt(at(0x0028E935)) == 0x00289D70 and size[0x0028E920] == 26 and size[0x0028AAA0] == 1692
      and tgt(at(0x00289B7C)) == 0x0028AAA0 and s(at(0x00289B54)) == "mov rbx, qword ptr [r15 + 0x428]" and s(at(0x00289B81)) == "mov rbx, qword ptr [rbx + 0x18]")
check("X16 02AEDFE4 is stored by ComputeComboChance at 00388648", rip(at(0x00388648)) == 0x02AEDFE4 and at(0x00388648).mnemonic == "mov")

# ================================ 09 gambits ==========================================================================
q = {i.address: i for i in body(0x00233780)}
check("X19 the return window is (int)([01DFE0B8] * 30.0) * [0208936C] (002337DE-00233801): the factor is 30 only at FrameLimit 30",
      rip(q[0x002337DE]) == 0x01DFE0B8 and rip(q[0x002337E8]) == 0x008F8D80 and f32(0x008F8D80) == 30.0
      and q[0x002337F6].mnemonic == "cvttss2si" and rip(q[0x002337FA]) == 0x0208936C and q[0x00233801].mnemonic == "cmp")
o = {i.address: i for i in body(0x003014C0)}
check("X20 entry i chains only when mask 0x20>>i and 0x20>>(i+1) are both set (003016BE-003016E0), copying its own result buffer (r15) to [rsp+0x40]",
      s(o[0x003016C3]) == "mov eax, 0x20" and s(o[0x003016CA]) == "sar eax, cl" and s(o[0x003016D4]) == "lea ecx, [rbx + 1]"
      and s(o[0x003016E2]) == "mov rcx, r15" and s(o[0x00301746]) == "lea rsi, [rsp + 0x40]")
check("X20 otherwise the next entry filters the original list (00301753 rsi = r13) into its own buffer (00301759-00301768)",
      s(o[0x00301753]) == "mov rsi, r13" and s(o[0x00301759]) == "lea r15, [rsp + 0x460]" and s(o[0x00301761]) == "imul rax, rcx, 0x208")
check("X20 a non-empty entry that finds no one fails (003016AF jle 003017CB); the final pick reads buffer 0 only (003017B7)",
      o[0x003016AF].mnemonic == "jle" and tgt(o[0x003016AF]) == 0x003017CB and s(o[0x003017B7]) == "lea rdx, [rsp + 0x460]"
      and tgt(o[0x003017BF]) == 0x003087E0)

# ================================ 11 party ===========================================================================
p = {i.address: i for i in body(0x00321100)}
check("X17 00321100 returns the index both when the class-0x17 check fails (00321130 je 00321158) and when the selector IS 0xFF (0032113D)",
      tgt(p[0x00321129]) == 0x00322C50 and s(p[0x00321125]) == "lea ecx, [r8 + 0x17]" and tgt(p[0x00321130]) == 0x00321158
      and s(p[0x00321139]) == "cmp byte ptr [rdi + rax], 0xff" and tgt(p[0x0032113D]) == 0x00321158 and s(p[0x00321158]) == "mov eax, ebx")
t6 = [i for i in body(0x0025A6A0) if 0x0025A6FC <= i.address <= 0x0025A763 and i.mnemonic == "movups"]
ld = sorted(i.operands[1].mem.disp for i in t6 if i.operands[1].type == X86.X86_OP_MEM)
check("X18 the teardown copies 0xB0 bytes, eleven movups pairs from [rbx=+0x7A0] to [rbp=+0x6F0] (0025A6FC-0025A763)",
      len(t6) == 22 and ld == list(range(0, 0xB0, 0x10)) and s(at(0x0025A6E3)) == "lea rbx, [r15 + 0x7a0]" and s(at(0x0025A6EA)) == "lea rbp, [r15 + 0x6f0]")
ci = [i for i in body(0x0025A180) if i.mnemonic == "movups" and i.operands[1].type == X86.X86_OP_MEM]
check("G11 the context install 0025A180 copies [[[actor+0xC0]+0x138]+0x30..+0xDF] (a pointer at +0x138, not an inline block) to +0x7A0",
      s(at(0x0025A1A2)) == "mov rax, qword ptr [rcx + 0xc0]" and s(at(0x0025A1B2)) == "mov rax, qword ptr [rax + 0x138]"
      and sorted(i.operands[1].mem.disp for i in ci) == list(range(0x30, 0xE0, 0x10)))
check("G10 00359410 is PartyFocus_SetSecondaryPackedActorHandle (154 B) and calls at 00359424 / 00359499",
      name(0x00359410) == "PartyFocus_SetSecondaryPackedActorHandle" and at(0x00359424).mnemonic == "call" and at(0x00359499).mnemonic == "call")

# ================================ 12 equipment / shops ================================================================
u = body(0x00273270)
ua = {i.address: i for i in u}
check("F12 00273270 answers 0xFFFF on its two early exits (0027328F id 0, 00273299 no actor -> 002732C1 mov eax,0xffff)",
      tgt(ua[0x0027328F]) == 0x002732C1 and tgt(ua[0x00273299]) == 0x002732C1 and s(ua[0x002732C1]) == "mov eax, 0xffff")
check("F12 ... and 0 only when 0031FF70 leaves the preset: [rsp+0xCC] = 0x0000FFFF (002732A7), answer = that dword >> 16 (002732B5-002732BC)",
      s(ua[0x0027329B]) == "mov eax, 0xffff" and s(ua[0x002732A7]) == "mov dword ptr [rsp + 0xcc], eax"
      and tgt(ua[0x002732B0]) == 0x0031FF70 and s(ua[0x002732BC]) == "shr eax, 0x10")
check("G12 0027C625-0027C632 choose 0x9D when the entry equals the stashed item or is 0xFFFF, 0x9C otherwise (0027C637, 0027C65A)",
      s(at(0x0027C625)) == "cmp di, ax" and tgt(at(0x0027C628)) == 0x0027C657 and tgt(at(0x0027C632)) == 0x0027C657
      and s(at(0x0027C637)) == "mov r8d, 0x9c" and s(at(0x0027C65A)) == "mov r8d, 0x9d")
check("X21 002536A0 (8 B) returns qword [020927C0]; the countB mask is 1 << (i & 7) (003166AC-003166C1)",
      size[0x002536A0] == 8 and rip(at(0x002536A0)) == 0x020927C0 and s(at(0x003166AC)) == "and ebx, 7"
      and s(at(0x003166B7)) == "mov eax, 1" and s(at(0x003166BF)) == "shl eax, cl")
check("X21 shop_first_open_entry returns a pointer: rbx zeroed (002FAD4F), set per entry (002FADB0/002FADBF), returned at 002FAE2D",
      s(at(0x002FAD4F)) == "xor ebx, ebx" and s(at(0x002FADB0)) == "mov rbx, rax" and s(at(0x002FADBF)) == "add ebx, ecx"
      and s(at(0x002FAE2D)) == "mov rax, rbx")
check("G13 the transaction driver reads layout A: price dword +0x10 (0056D461), id word +8 (0056D464), bit 31 cleared (0056D468)",
      s(at(0x0056D461)) == "mov ebx, dword ptr [rax + 0x10]" and s(at(0x0056D464)) == "movzx ecx, word ptr [rax + 8]"
      and s(at(0x0056D468)) == "btr ebx, 0x1f")
check("G13 layout B (0057DAD0) keeps the price at +8 and sets bit 31 on a zero price (0057DBCC, 0057DBDC); 0020-byte rows",
      s(at(0x0057DBCC)) == "mov dword ptr [rbx + 8], eax" and s(at(0x0057DBDC)) == "bts eax, 0x1f" and s(at(0x0057DBE3)) == "add rbx, 0x20")
check("G14 the list is built into widget +0xE0 (005656AE) and moved to [+0xC0 object]+0xC8, +0xE0 zeroed (0056E55A, 0056E561)",
      s(at(0x005656AE)) == "mov qword ptr [rdi + 0xe0], rax" and s(at(0x0056E55A)) == "mov qword ptr [rsi + 0xc8], rcx"
      and s(at(0x0056E561)) == "mov qword ptr [rdi + 0xe0], 0")

# ================================ 05 spawn: FRONTIER-subtree sizes ===================================================
sz = [size[x] for x in (0x003145E0, 0x00584580, 0x00314440, 0x0032ED80, 0x0037AA90, 0x001831A0)]
check("X24 the corrected subtree sizes are the extents: 563 / 143 / 233 / 1,001 / 491 / 21 B", sz == [563, 143, 233, 1001, 491, 21], str(sz))

# ================================ 13 GR-17 / GR-19 =====================================================================
check("G17 the unit install reads 02EBF148 (0023A965) and stores +0xE78 (0023A9F4)",
      rip(at(0x0023A965)) == 0x02EBF148 and s(at(0x0023A9F4)) == "mov qword ptr [rdi + 0xe78], rcx")
callers = {}
for fn, n in size.items():
    if not n or n > 20000:
        continue
    try:
        ins = body(fn)
    except Exception:
        continue
    for i in ins:
        tg = tgt(i)
        if tg in (0x003377C0, 0x00337700):
            callers.setdefault(tg, []).append("%08X@%08X" % (fn, i.address))
        elif i.mnemonic == "lea" and rip(i) in (0x003377C0, 0x00337700):
            callers.setdefault(rip(i), []).append("%08X@%08X(lea)" % (fn, i.address))
c77 = callers.get(0x003377C0, [])
check("F19 003377C0 is shared: besides 00319490 it is called from 00334E00 (x2), 00339630, 0033BD70 and taken by lea in 00317DE0 (DE-4's validator)",
      {"00319490@0031950C", "00334E00@00334E65", "00334E00@00335093", "00339630@00339935", "0033BD70@0033BE55", "00317DE0@00317E11(lea)"} <= set(c77),
      " ".join(sorted(c77)) + " | 00337700: " + " ".join(sorted(callers.get(0x00337700, []))))

# ================================ register hygiene =====================================================================
reg = subprocess.run(["git", "show", "797b72780:Database/FFXII TZA/_index/OPEN-QUESTIONS.md"], capture_output=True).stdout.decode("utf-8", "replace")
gr = {m.group(1): l for l in reg.splitlines() for m in [re.match(r"^\| (GR-\d+) \|", l)] if m}
leak = sorted(k for k, l in gr.items() if re.search(r"FD-n\d", l))
check("F0 19 GR rows registered; draft placeholder ids leaked into the register rows GR-3 (FD-n401) and GR-8 (FD-n601)",
      len(gr) == 19 and leak == ["GR-3", "GR-8"], str(leak))
c160 = subprocess.run(["git", "merge-base", "--is-ancestor", "af6684173", "797b72780"]).returncode == 0
cen = open(os.path.join(DB, "FFXII TZA", "_index", "candidates", "sd160-free-target-type3-0930", "sd160_census.out"), encoding="utf-8").read()
check("F2 the SD-160 census (af6684173, an ancestor of 797b72780) already tallies every constant both verbs pass: btlAtelSetUnitType 0-3, "
      "setfreetargettype 1/3/4/6 - GR-2 cites none of it",
      c160 and all(x in cen for x in ("'PUSHII:0'", "'PUSHII:6'", "sites whose argument is not a pushed constant: 0"))
      and "SD-160" not in gr["GR-2"] and "sd160" not in gr["GR-2"])
check("F16 GR-16 is a review-status row (no game question); its plan is a board review", "auditor" in gr["GR-16"] and "team.py review" in gr["GR-16"])

print("FAILS %d" % len(FAILS) + ("  " + ", ".join(FAILS) if FAILS else ""))
