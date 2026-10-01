"""hm1_model_selectors.py - HM-1 narrowed: the b/c arguments of the high-model replace lookup, their one writer, and
what the skeleton mapping's values index (FABLE, Claude Opus 5.5, 2026-09-26; first read by a delegated read-only
pass, every step re-checked here). Also the regression for the correction to the secondary-context census, which
said +0x14C/+0x14D/+0x14E had no located writer.

  H1 the two getters read the actor's secondary context ([actor+0xC0]): 002657E0 returns movsx byte [ctx+0x14C]
     (002657FB) and defaults to 1 (00265803); 00263FC0 returns movsx byte [ctx+0x14D] (00263FDB) and defaults to 0
     (00263FE3).
  H2 the only other readers are two debug verbs that print the bytes with "%d ": 0050D860 (+0x14C, 0050D8C2) and
     0050D780 (+0x14D, 0050D7E2). The verb table names them debug_tty_modellocalno and debug_tty_modelclutno. The
     names are developer labels, not a consumer's use.
  H3 the one writer. 002E6090 stores dl at [ctx+0x14C] (002E609C) and r8b at [ctx+0x14D] (002E60A9) through
     [rcx+0xC0]. Its only E8/E9 caller is 00265EE4 in the secondary-context initialiser 00265B60 (called from the
     actor-record initialiser at 00266823). There r8d = 0 (00265DEE) and edx = r8 + 1 = 1 (00265DFB). Neither is
     written again before the call, and no branch enters that stretch from outside. So every initialised actor gets
     localno 1, clutno 0: the getters' own defaults.
  H4 image-wide: every store overlapping +0x14C..+0x14E whose base register was loaded from [x+0xC0] within the six
     instructions before it. The result is exactly 002E609C, 002E60A9 and 0026685D; the last sets +0x14E = 1 in the
     actor-record initialiser. Blind spot: a context pointer that reaches the store any other way (an argument, a
     spill).
  H5 the skeleton mapping's values are joint indices into a second skeleton. 003703A0 uses the mapping only when
     [rsi+0x6C8] == 2 (00370634). Per joint it loads value = dword [r12 + rax] (0037072C) and skips -1 (00370730).
     Otherwise it combines this joint's 0x290-stride entry (+0x150, 00370738) with the entry at index `value` of the
     skeleton resolved from [r14+0xC] (0037069A).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
def txt(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in ins(a, size)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
G1 = txt(0x2657E0, 0x30); G2 = txt(0x263FC0, 0x30)
check("H1 002657E0 returns ctx+0x14C (default 1); 00263FC0 returns ctx+0x14D (default 0)",
      G1.get(0x2657FB) == "movsx eax, byte ptr [rax + 0x14c]" and G1.get(0x265803) == "mov eax, 1"
      and G2.get(0x263FDB) == "movsx eax, byte ptr [rax + 0x14d]" and G2.get(0x263FE3) == "xor eax, eax"
      and any("+ 0xc0]" in v for v in G1.values()) and any("+ 0xc0]" in v for v in G2.values()))
rows = {r["call_id"]: r for r in csv.DictReader(open(DB / "01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv", encoding="utf-8"), delimiter="\t")}
V1 = txt(0x50D860, 0x80); V2 = txt(0x50D780, 0x80)
check("H2 the debug verbs print the two bytes; the verb table names them modellocalno / modelclutno",
      V1.get(0x50D8C2) == "movsx edx, byte ptr [rax + 0x14c]" and V2.get(0x50D7E2) == "movsx edx, byte ptr [rax + 0x14d]"
      and rows["208C"]["verb"] == "debug_tty_modellocalno" and rows["208C"]["arg_handler"] == "0050D860"
      and rows["208B"]["verb"] == "debug_tty_modelclutno" and rows["208B"]["arg_handler"] == "0050D780")
S = txt(0x2E6090, 0x21)
def rel_callers(t):
    hits = []; vs, va, rs, ro = secs[0]; tb = BASE + va
    for op in (b"\xE8", b"\xE9"):
        k = d.find(op, ro)
        while 0 <= k < ro + rs - 5:
            a = tb + k - ro
            if a + 5 + struct.unpack_from("<i", d, k + 1)[0] == t:
                x = ins(a, 16)
                if x and x[0].address == a and x[0].size == 5: hits.append(a)
            k = d.find(op, k + 1)
    return hits
C = rel_callers(0x2E6090)
B = ins(0x265B60, 0x400)
between = [x for x in B if 0x265DFB < x.address < 0x265EE4]
clob = [x.address for x in between if x.mnemonic == "call" or re.match(r"(edx|rdx|dl|dx|r8d|r8|r8b|r8w),", x.op_str)]
inbound = [x.address for x in B if x.mnemonic.startswith("j") and x.op_str.startswith("0x")
           and 0x265DFB < int(x.op_str, 16) <= 0x265EE4 and not (0x265DFB <= x.address < 0x265EE4)]
check("H3 002E6090 is the one setter; its one call passes edx = 1, r8d = 0, unchanged and unentered from outside",
      S.get(0x2E6090) == "mov rax, qword ptr [rcx + 0xc0]" and S.get(0x2E609C) == "mov byte ptr [rax + 0x14c], dl"
      and S.get(0x2E60A9) == "mov byte ptr [rax + 0x14d], r8b" and C == [0x265EE4]
      and txt(0x265DEE, 3).get(0x265DEE) == "xor r8d, r8d" and txt(0x265DFB, 4).get(0x265DFB) == "lea edx, [r8 + 1]"
      and clob == [] and inbound == [] and txt(0x266823, 5).get(0x266823) == "call 0x265b60",
      "callers %s; clobbers %s; inbound jumps %s" % (["%08X" % a for a in C], clob, inbound))
vs, va, rs, ro = secs[0]
cs2 = Cs(CS_ARCH_X86, CS_MODE_64); cs2.skipdata = True
L = list(cs2.disasm(d[ro:ro + rs], BASE + va))
WID = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
hits = []
for i, x in enumerate(L):
    m = re.match(r"(byte|word|dword|qword|xmmword) ptr \[(\w+) \+ (0x[0-9a-f]+)\]", x.op_str)
    if not m or x.mnemonic not in ("mov", "movups", "movaps", "movdqu", "or", "and", "inc", "dec", "add", "sub", "movss", "movsd"): continue
    o = int(m.group(3), 16)
    if o <= 0x14E and o + WID[m.group(1)] > 0x14C:
        if any(y.op_str.startswith(m.group(2) + ",") and "+ 0xc0]" in y.op_str for y in L[max(0, i - 6):i]): hits.append(x.address)
check("H4 image-wide, the only +0x14C..+0x14E stores through an [x+0xC0]-loaded base are 002E609C, 002E60A9, 0026685D",
      sorted(set(hits)) == [0x26685D, 0x2E609C, 0x2E60A9] and txt(0x26685D, 8).get(0x26685D) == "mov byte ptr [rax + 0x14e], 1",
      str(["%08X" % a for a in sorted(set(hits))]))
K = txt(0x370600, 0x280)
check("H5 the mapping's values are joint indices into a second skeleton (mode [rsi+0x6C8] == 2, -1 skips)",
      K.get(0x370634) == "cmp dword ptr [rsi + 0x6c8], 2" and K.get(0x37065D) == "movsxd rax, dword ptr [r14 + 0xb0]"
      and K.get(0x37072C) == "movsxd rbx, dword ptr [r12 + rax]" and K.get(0x370730) == "cmp ebx, -1"
      and K.get(0x370738) == "lea rdx, [r8 + 0x150]" and K.get(0x37069A) == "mov ecx, dword ptr [r14 + 0xc]"
      and any("0x290" in v for v in K.values()))
print("FAILS", fails)
sys.exit(1 if fails else 0)
