"""fe7_order_reach.py - FE-7: can a direct-state stat order (0x4158-0x415C, 0x4160-0x4162) reach a party (kind 0) stats
record? (FABLE, Claude Opus 5.5, 2026-09-27). Static reads plus a shipped-data census.

  R1 the arms act on the COMMITTING unit's own record: 0x4158 (002FE12B) and 0x4159 (002FE1A3) load [rbx + 0x698], where
     rbx is the dispatcher's own unit argument (002FDDAD mov rbx, rcx). There is no target record to aim at.
  R2 the order precondition passes these ids without a kind test: AiOrder_CheckActionPreconditions (00301830) sends ids
     above 0x4124 to 00301A1B; 0x414B and 0x414D branch off, 0x4165 decodes a goal, and every other id returns 1
     (00301A31). The 0x414D arm is the one that reads the kind byte (00301A6E) - planted positive for the matcher.
  R3 the order id reaches +0x714 only through BattleUnit_CommitAction (0030F760: r8w -> 0030F806), and the image has
     exactly five E8 calls to it (raw sweep, each confirmed as a decoded instruction), each with a fixed id source:
       00305B2F  the issued command's word +0xBA0      00305C9B  the 0x4021 record 01EEC298
       00305DF4  the set walk's evaluated record id    0030FA5C  the unit's current +0x714 again (combo)
       003130DC  immediate 0x96 (auto-attack)
  R4 +0xBA0 is written as a word only by BattleUnit_IssueCommand (00311D7A), image-wide.
  R5 a kind-0 unit's set C is its rebuilt gambit set: the party path of BattleUnit_ApplyUnitDefinition stores
     02089378 + index * 0x170 at +0x6E0 (0023AB64..0023AB9F), and GambitRuntime_RebuildOrderSetFromConfig (00328140)
     writes each record's id (+0x20 of the set, record +0) from the config slot's word +2 (003281AE, 0032826A).
  R6 the shipped gambit presets (battle_pack entry +0x24, 40 x 64, read by 00327CB0) carry action words <= 0xCF in all
     nine language packs: no id >= 0x4000.
  R7 in the 166 shipped .ard files (1,422 sets / 50,050 records - reproduces the published totals), the eight stat
     orders occur exactly three times, all in bhm_d.ard set 0 (0x415B record 3, 0x4158 record 7, 0x4159 record 8), and
     in none of the 826 weighted-id tables. Planted positive: 0x4113 is counted (754).
  R8 image-wide, no instruction forms 0x4112-0x4115 or 0x4158-0x4162 as an immediate except the dispatcher's own three
     (002FDDDB, 002FE048, 002FE17F) - memory displacements excluded, non-rip `lea` operands included.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys, glob, os, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
WORK = ROOT / "Database/Tools/work"
d = (WORK / "exe/FFXII_TZA.exe").read_bytes()
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

# R1
a = dis(0x2FDDA0, 0x2FDDB0); b = dis(0x2FE12B, 0x2FE160); c = dis(0x2FE1A3, 0x2FE1D8)
check("R1 the stat arms load the committing unit's own stats record",
      a.get(0x2FDDAD) == "mov rbx, rcx" and b.get(0x2FE12B) == "mov rdx, qword ptr [rbx + 0x698]"
      and b.get(0x2FE156) == "mov word ptr [rdx + 8], cx" and c.get(0x2FE1A3) == "mov rdx, qword ptr [rbx + 0x698]"
      and c.get(0x2FE1CE) == "mov word ptr [rdx + 0xa], cx")
# R2
p = dis(0x301901, 0x30190D); q = dis(0x301A1B, 0x301A76)
check("R2 the precondition returns 1 for the stat ids; only the 0x414D arm reads the kind",
      p.get(0x301901) == "cmp edx, 0x4124" and p.get(0x301907) == "ja 0x301a1b"
      and q.get(0x301A1B) == "sub edx, 0x414b" and q.get(0x301A27) == "sub edx, 2" and q.get(0x301A2C) == "cmp edx, 0x18"
      and q.get(0x301A2F) == "je 0x301a38" and q.get(0x301A31) == "mov eax, 1"
      and q.get(0x301A6E) == "movzx eax, byte ptr [rax + 5]")

# one pass over every listed function body
funcs = []
for line in open(WORK / "graph/functions.tsv", encoding="utf-8").read().splitlines()[1:]:
    f = line.split("\t"); funcs.append((int(f[0], 16), int(f[2])))
decoded = set(); ba0 = []; imms = []; calls = []
IDS = set(range(0x4112, 0x4116)) | set(range(0x4158, 0x4163))
MEM = re.compile(r"\[[^\]]*\]")
for fa, sz in funcs:
    o = off(fa)
    if o is None or sz <= 0: continue
    for x in cs.disasm(d[o:o + sz], fa):
        decoded.add(x.address)
        s = x.op_str
        if x.mnemonic == "call" and s == "0x30f760": calls.append(x.address)
        if x.mnemonic.startswith("mov") and s.startswith("word ptr [") and "+ 0xba0]" in s.split(",")[0]: ba0.append(x.address)
        for m in re.findall(r"0x[0-9a-f]+", s if x.mnemonic == "lea" and "rip" not in s else MEM.sub("", s)):
            if int(m, 16) in IDS: imms.append((x.address, x.mnemonic, s))
# raw E8 sweep for the commit function, confirmed against decoded boundaries
text = [s for s in secs if s[1] == 0x1000][0]
raw = []
lo = text[3]; hi = text[3] + text[2]
for i in range(lo, hi - 5):
    if d[i] == 0xE8:
        va = i - text[3] + text[1] + BASE
        if va + 5 + struct.unpack_from("<i", d, i + 1)[0] == 0x30F760: raw.append(va)
raw_real = sorted(v for v in raw if v in decoded)
m = dis(0x30F77E, 0x30F80D)
check("R3 the id reaches +0x714 only through CommitAction, called from exactly five sites",
      m.get(0x30F77E) == "movzx edi, r8w" and m.get(0x30F806) == "mov word ptr [rbx + 0x714], di"
      and raw_real == [0x305B2F, 0x305C9B, 0x305DF4, 0x30FA5C, 0x3130DC] and sorted(calls) == raw_real,
      "raw E8 hits %d, on decoded boundaries %s" % (len(raw), ["%08X" % v for v in raw_real]))
s1 = dis(0x305AE4, 0x305B2F); s2 = dis(0x305C7E, 0x305C9B); s3 = dis(0x305DE3, 0x305DF4); s4 = dis(0x30FA45, 0x30FA5C)
s5 = dis(0x313096, 0x3130DC)
check("R3b each commit site's id source",
      s1.get(0x305AE4) == "movzx esi, word ptr [rbx + 0xba0]" and s1.get(0x305B20) == "movzx r8d, si"
      and s2.get(0x305C7E) == "movzx r8d, word ptr [rip + 0x1be6612]"
      and s3.get(0x305DE3) == "movzx r8d, word ptr [rsp + 0x70]"
      and s4.get(0x30FA45) == "movzx r8d, word ptr [rbx + 0x714]" and s5.get(0x313096) == "mov r8d, 0x96")
check("R4 +0xBA0 is word-written only by BattleUnit_IssueCommand", ba0 == [0x311D7A], str(["%08X" % v for v in ba0]))
e = dis(0x23AB64, 0x23ABA6); r = dis(0x3281AB, 0x328273)
check("R5 a kind-0 unit's set C is its rebuilt gambit set, whose record ids are the config slots' word +2",
      e.get(0x23AB64) == "lea rcx, [rip + 0x1e4e80d]" and e.get(0x23AB7E) == "imul rax, r14, 0x170"
      and e.get(0x23AB9F) == "mov qword ptr [rdi + 0x6e0], rax"
      and r.get(0x3281AE) == "movzx r14d, word ptr [rdi + 2]" and r.get(0x32826A) == "mov word ptr [rsi + 0x20], r14w")

# R6 gambit presets
ok6 = True; det = []
for lang in ["us", "de", "fr", "in", "es", "it", "ch", "cn", "kr"]:
    pk = open("D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/%s/binaryfile/battle_pack.bin" % lang, "rb").read()
    u = lambda o: struct.unpack_from("<I", pk, o)[0]
    t = u(0x24); cnt, sz, do = u(t + 4), u(t + 8), u(t + 0xC)
    acts = []
    for row in range(cnt):
        bb = t + do + row * sz
        for sl in range(12):
            cw, aw = struct.unpack_from("<HH", pk, bb + 2 * sl)[0], struct.unpack_from("<H", pk, bb + 0x20 + 2 * sl)[0]
            if cw != 0xFFFF and aw != 0xFFFF: acts.append(aw)
    det.append("%s:%d/%#x" % (lang, len(acts), max(acts)))
    ok6 &= pk[t:t + 4] == b"st2e" and (cnt, sz) == (40, 64) and max(acts) < 0x4000 and 0x96 in acts
check("R6 shipped gambit presets carry no order id (planted positive: Attack 0x96 present)", ok6, " ".join(det))

# R7 order census
pack = open(WORK / "repos-2d/vbf/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin", "rb").read()
u32 = lambda bb, o: struct.unpack_from("<I", bb, o)[0]; u16 = lambda bb, o: struct.unpack_from("<H", bb, o)[0]
sec = u32(pack, 0x2C); nw = u16(pack, sec)
offs = [u32(pack, sec + 4 + 4 * i) for i in range(nw + 1)]
wids = set()
for i in range(nw):
    for pp in range(sec + offs[i], sec + offs[i + 1], 4): wids.add(u16(pack, pp))
STAT = set(range(0x4158, 0x415D)) | set(range(0x4160, 0x4163))
sets = recs = 0; hits = []; c4113 = 0
for f in sorted(glob.glob(str(WORK / "repos-3f/ard/ard/*.ard"))):
    bb = open(f, "rb").read(); s1 = u32(bb, 0x14)
    if not s1: continue
    cnt = u16(bb, s1); so = [u32(bb, s1 + 4 + 4 * i) for i in range(cnt + 1)]
    for k in range(cnt):
        base = s1 + so[k]; nrec = sum(bb[base:base + 12]); sets += 1
        for rr in range(nrec):
            sel = u16(bb, base + 0x20 + 24 * rr); recs += 1
            if sel in STAT: hits.append((os.path.basename(f), k, rr, sel))
            c4113 += sel == 0x4113
check("R7 the stat orders ship only in bhm_d.ard set 0, three records, and in no weighted table",
      (sets, recs) == (1422, 50050) and hits == [("bhm_d.ard", 0, 3, 0x415B), ("bhm_d.ard", 0, 7, 0x4158), ("bhm_d.ard", 0, 8, 0x4159)]
      and not (wids & STAT) and c4113 == 754 and nw == 826,
      "sets %d records %d hits %s 0x4113=%d" % (sets, recs, [(h[0], h[1], h[2], hex(h[3])) for h in hits], c4113))
check("R8 no code forms these ids as an immediate except the dispatcher's own three",
      sorted(a for a, _, _ in imms) == [0x2FDDDB, 0x2FE048, 0x2FE17F], str([("%08X" % a, mn, s) for a, mn, s in imms]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
