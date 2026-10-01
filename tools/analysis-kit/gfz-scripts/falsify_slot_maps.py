"""Falsification pass 1 on CONTRACT-the-five-parallel-slot-maps (OPUS, 2026-09-29), from the shipping image. Killers first.

  Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.
  K1  section 14 item 2: 003266DB is a separately registered handler, dispatched through two .rdata records, with no direct
      caller, shuffling a CALLER-SUPPLIED five-map record in rdi. Killer: 003266DB is an instruction inside
      BattleGroup_RefreshFourActorDefinitions (003266C0, 1,253 B); rdi there is [02EBF190] + 0x5A48, set at 003266C8/003266D4
      before 003266DB; no branch in the image targets 003266DB; the two .rdata records are UNWIND_INFO with the chain flag
      whose chained RUNTIME_FUNCTION is {003266CF, 003266DB}, and .pdata has entries starting at 003266CF and 003266DB (a
      shrink-wrapped prologue split, not a dispatch table)
  K2  section 4 SM-5 box and section 12: after a refresh the five are two groups - map 3 equals map 0, maps 2 and 4 equal the
      cleared map 1. Killer: after the ordered copies the body switches on BattleRuntime_GetMode0To5 (0030D9A0): modes 1-5
      rewrite entries [0..3] of maps 1, 2 and/or 4, and modes 3 and 5 restore map 4 from the copy taken at 003266F4/00326700
      BEFORE the refresh (003268FD / 003267F3); no store after 00326724 reaches map 3 ([rdi + 0x36, rdi + 0x48)); competing
      case - a later tail restoring the copies: no u16 or 16-byte store follows the point 00326A34 where the arms rejoin
  K3  section 14 item 1: map 0 is rebuilt "from the authored selector table at 0x01EC9260". Killer: 00329CC0 addresses
      01EED260 (00329CE1 lea, 00329DBB byte load) and nothing in the body addresses 01EC9260
  S1  SM-1: the five arms are byte loads [rax + rdi*2 + 0x5A48 / 5A / 6C / 7E / 90]; 0031BA3D is the 0x5A90 arm
  S2  SM-2: 0031BA0F jne past 0031BA11 `mov al, 0xff`, and 0031BA34 `jne 0x31ba11`
  S3  SM-3: 0031BA04 `lea ecx, [r8 + 0x17]` with r8d = 0, then a call to 00322C50; the resolver is 200 B
  S4  SM-4: 00329CC0 fills map 0 from the table (0xFF path gated `cmp al, 0x27` at 00329D30, member path `cmp dil, 0x27` at
      00329D6C) and copies 16 + 2 bytes into maps 1-4 at 00329DF6..00329E27
  S5  SM-5 order: 00326714..0032674B copy map 0 -> 1, map 0 -> 3, clear map 1 [4..8], copy map 1 -> 2 and 4, in that order
  S6  SM-8: 00329DC2 stores the table's first byte (00329DBB) as a u32 at +0x5AA4
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
body = lambda fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa))
sec = lambda n: next(x for x in SECS if x[0] == n)

# ---- K1
R = body(0x003266C0); RI = {x.address: x for x in R}
text = sec(".text"); targets = []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        ins = md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)
        for x in ins:
            if x.group(1) or x.group(7) or x.mnemonic.startswith("j"):     # jump / call groups
                if x.operands and x.operands[0].type == X86_OP_IMM and x.operands[0].imm == 0x003266DB:
                    targets.append(x.address)
    except ValueError:
        continue
rva = 0x003266DB - BASE
pd = sec(".pdata"); praw = blob[pd[3]:pd[3] + pd[4]]
pent = {}
for j in range(0, len(praw) - 11, 12):
    b_, e_, u_ = struct.unpack("<III", praw[j:j + 12])
    pent[b_] = (e_, u_)


def unwind(begin):
    """(flags, chained RUNTIME_FUNCTION or None) of the UNWIND_INFO a .pdata entry names."""
    u = BASE + pent[begin][1]; h = blob[OFF(u):OFF(u) + 4]
    fl, cnt = h[0] >> 3, h[2]
    c = OFF(u) + 4 + 2 * ((cnt + 1) & ~1)
    return fl, (struct.unpack("<III", blob[c:c + 12]) if fl & 4 else None), u


uw = {b: unwind(b) for b in (0x003266CF - BASE, rva) if b in pent}
flags = [uw[b][0] for b in sorted(uw)]
chain = [(b, uw[b][1]) for b in sorted(uw)]
check("K1", 0x003266C0 < 0x003266DB < 0x003266C0 + sizes[0x003266C0] and 0x003266DB in RI and S(RI[0x003266C8]).startswith("mov rdi, qword ptr [rip")
      and rip(RI[0x003266C8]) == [0x02EBF190] and S(RI[0x003266D4]) == "add rdi, 0x5a48" and not targets and len(chain) == 2
      and all(f & 4 for f in flags) and [c[0] if c else None for _b, c in chain] == [0x003266C0 - BASE, 0x003266CF - BASE],
      "(REFUTES a separately dispatched handler on a caller-supplied record) 003266DB inside 003266C0 (%d B): %s; rdi = %s then %s; branches to it %s; .pdata fragments %s, each UNWIND_INFO flagged "
      "CHAININFO (%s) and chained to %s, so both resolve to 003266C0 (the .rdata records naming 003266DB are these chain entries)"
      % (sizes[0x003266C0], S(RI[0x003266DB]), S(RI[0x003266C8]), S(RI[0x003266D4]), ["%08X" % t for t in targets],
         ["%08X-%08X" % (BASE + b, BASE + pent[b][0]) for b in sorted(uw)], flags, ["%08X" % (BASE + c[0]) if c else None for _b, c in chain]))

# ---- K2
mode = {}
seq = [x for x in R if 0x0032674F <= x.address < 0x00326783]
cur = 0
for x in seq:
    if S(x) == "sub eax, 1":
        cur += 1
    elif x.mnemonic == "je" and cur:
        mode[cur] = x.operands[0].imm
    elif S(x) == "cmp eax, 1":
        cur += 1
    elif x.mnemonic == "jne" and cur == 5:
        mode["other"] = x.operands[0].imm
mode[5] = 0x00326783
# every store the mode arms (0032674F..00326A34; the ordered copies before them are pinned by S5) make through the map pointers: rdi = map 0, r15 (and rcx = r15 in mode 3) = map 1, r14 = map 2 advanced
# by 2 per entry, an index register ranges over entries 0..3; a store reaches map 3 if any of its offsets from rdi is in [0x36, 0x48)
BASEOFF = {"rdi": [0], "r15": [0x12], "rcx": [0x12 + 2 * k for k in range(4)], "r14": [0x24 + 2 * k for k in range(4)]}
w_map3, reached = [], set()
for x in R:
    if not (0x0032674F <= x.address < 0x00326A34 and x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov")):
        continue
    mm_ = x.operands[0].mem; bn = x.reg_name(mm_.base)
    if bn not in BASEOFF:
        continue
    idx = [2 * k for k in range(4)] if mm_.index else [0]
    offs = {b + mm_.disp + i for b in BASEOFF[bn] for i in idx}
    reached |= {o // 0x12 for o in offs}
    if any(0x36 <= o < 0x48 for o in offs):
        w_map3.append("%08X" % x.address)
restore = [x.address for x in R if S(x) == "movups xmmword ptr [rdi + 0x48], xmm0" and x.address > 0x0032674F]
saved = S(RI[0x003266F4]) == "movups xmm0, xmmword ptr [rdi + 0x48]" and S(RI[0x00326709]) == "movups xmmword ptr [rsp + 0x20], xmm0" \
    and S(RI[0x00326700]) == "movzx r12d, word ptr [rdi + 0x58]"
reloads = all(any(S(RI[b]) == "movups xmm0, xmmword ptr [rsp + 0x20]" for b in RI if a - 0x10 <= b < a) for a in restore)
mode1_4 = [x.address for x in R if 0x00326754 < x.address < 0x00326A34 and x.operands and x.operands[0].type == X86_OP_MEM and x.mnemonic == "mov"
           and x.operands[0].size == 2]
tail_w = [x.address for x in R if x.address >= 0x00326A34 and x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].size in (2, 16)
          and x.mnemonic.startswith("mov") and x.reg_name(x.operands[0].mem.base) != "rsp"]
check("K2", not tail_w and S(RI[0x0032674F]) == "call 0x30d9a0" and mode == {1: 0x003269D2, 2: 0x00326991, 3: 0x003268F3, 4: 0x0032683F, "other": 0x00326A34, 5: 0x00326783}
      and restore == [0x003267F3, 0x003268FD] and saved and reloads and not w_map3 and reached == {1, 2, 4} and len(mode1_4) >= 10,
      "(REFUTES 'after a refresh maps 2 and 4 equal the cleared map 1' outside mode 0) mode switch on 0030D9A0 %s; map 4 saved before the refresh %s and restored at %s (modes 5, 3); %d u16 map stores in the mode arms; "
      "maps reached by the mode arms' stores %s; stores to map 3 in the arms: %s (the ordered copies are S5's); u16/16-byte stores after the arms rejoin at 00326A34: %s" % ({k: "%08X" % v for k, v in mode.items()}, saved, ["%08X" % a for a in restore], len(mode1_4), sorted(reached), w_map3, tail_w))

# ---- K3
I = body(0x00329CC0); II = {x.address: x for x in I}
refs = sorted({t for x in I for t in rip(x) if 0x01E00000 <= t < 0x01F00000})
check("K3", rip(II[0x00329CE1]) == [0x01EED260] and rip(II[0x00329DBB]) == [0x01EED260] and 0x01EC9260 not in refs,
      "(REFUTES 0x01EC9260) table references in 00329CC0: %s" % ["%08X" % t for t in refs])

# ---- survivors
V = body(0x0031B9F0); VI = {x.address: x for x in V}
arms = sorted(x.operands[1].mem.disp for x in V if x.mnemonic == "movzx" and x.operands[1].size == 1 and x.operands[1].mem.scale == 2)
check("S1", arms == [0x5A48, 0x5A5A, 0x5A6C, 0x5A7E, 0x5A90] and S(VI[0x0031BA3D]) == "movzx eax, byte ptr [rax + rdi*2 + 0x5a90]", "byte arms %s" % [hex(a) for a in arms])
check("S2", S(VI[0x0031BA0F]) == "jne 0x31ba1e" and S(VI[0x0031BA11]) == "mov al, 0xff" and S(VI[0x0031BA34]) == "jne 0x31ba11",
      "%s / %s / %s" % (S(VI[0x0031BA0F]), S(VI[0x0031BA11]), S(VI[0x0031BA34])))
check("S3", S(VI[0x0031B9FD]) == "xor r8d, r8d" and S(VI[0x0031BA04]) == "lea ecx, [r8 + 0x17]" and S(VI[0x0031BA08]) == "call 0x322c50" and sizes[0x0031B9F0] == 200,
      "200 B; class %s" % S(VI[0x0031BA04]))
cp = [(S(II[a])) for a in (0x00329DF6, 0x00329DFD, 0x00329E04, 0x00329E0B, 0x00329E12, 0x00329E19, 0x00329E20, 0x00329E27)]
check("S4", S(II[0x00329D30]) == "cmp al, 0x27" and S(II[0x00329D6C]) == "cmp dil, 0x27"
      and cp == ["movups xmmword ptr [rcx + 0x5a5a], xmm0", "mov word ptr [rcx + 0x5a6a], ax", "movups xmmword ptr [rcx + 0x5a6c], xmm0",
                 "mov word ptr [rcx + 0x5a7c], ax", "movups xmmword ptr [rcx + 0x5a7e], xmm0", "mov word ptr [rcx + 0x5a8e], ax",
                 "movups xmmword ptr [rcx + 0x5a90], xmm0", "mov word ptr [rcx + 0x5aa0], ax"], "0x27 gates; 16 + 2 into maps 1-4")
order = [S(RI[a]) for a in (0x00326714, 0x00326717, 0x0032671B, 0x00326720, 0x00326724, 0x00326728, 0x00326730, 0x00326735, 0x0032673E, 0x00326747, 0x0032674B)]
check("S5", order == ["movups xmm0, xmmword ptr [rdi]", "movups xmmword ptr [r15], xmm0", "mov word ptr [r15 + 0x10], ax",
                      "movups xmmword ptr [rdi + 0x36], xmm0", "mov word ptr [rdi + 0x46], ax", "mov qword ptr [rdi + 0x1a], 0xffffffffffffffff",
                      "mov word ptr [rdi + 0x22], r13w", "movups xmm0, xmmword ptr [r15]", "movups xmmword ptr [r14], xmm0",
                      "movups xmmword ptr [rdi + 0x48], xmm0", "mov word ptr [rdi + 0x58], ax"], "0->1, 0->3, clear 1, 1->2, 1->4")
check("S6", S(II[0x00329DBB]).startswith("movzx ecx, byte ptr [rip") and S(II[0x00329DC2]) == "mov dword ptr [rax + 0x5aa4], ecx", S(II[0x00329DC2]))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
