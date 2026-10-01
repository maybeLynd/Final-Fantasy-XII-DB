"""uq68_kind5.py - UQ-68: battle window kind 5 is the Foecraft command's list, and where the kind really comes from
(FABLE, Claude Opus 5.5, 2026-09-27). Static read of the authorised exe, plus the shipped us menubtlwndinfo.bin.

  W1 the window-kind switch 0027E050 indexes its 20-dword table 0027E384 by kind - 1 (0027E06B), so it covers kinds
     1..20, not 0..19; each arm stores the list code at +0x4C0 and, for code 0xB, a sub-selector at +0x4D4.
     Kind 5 -> code 0xB, sub-selector 7.
  W2 the sub-selector is a class-21 encoded id: list code 0xB's arm of BattleMenu_BuildCommandEntryList 0031EB20
     (0031ED58) validates dword [list+0x14] (= +0x4D4) with BattleEncodedId_IsValidForClass(0x15, ...) (0031ED73).
     Class 21 is the battle command list (the encoded-id page): row 7 is Foecraft.
  W3 the next-kind function 0027C3D0: in list codes 6 and 9 (the command lists) a row's command word +0x50 picks the
     next kind through the table 0027C6D0; command 7 -> 0027C532 -> kind 5, and no other command reaches that arm.
  W4 the join: for commands 3, 5, 6, 7 the kind 0027C3D0 returns is the kind whose 0027E050 sub-selector is that same
     command (Items, Summon, Quickening, Foecraft).
  W5 the path into menu +0xD8: the dispatch 002778C0 takes the kind from 0027C3D0 (00278423), pushes the current
     kind onto the navigation stack at [+0x2FE8]+0x70 (00278542-0027854A), raises the depth +0x68 (002785C8), and
     for an ordinary kind calls its own procedure with message 31 and payload = the kind (00278870-00278895); its
     message 31 arm 00279187 is the only word store to +0xD8 (002791AC).
  W6 no other source produces kind 5: the controller's message 33 senders pass 1 (0027AA70, constant 00915BB0) or
     0027C730's result, which is one of 0x10..0x13; the back path (0027881F) restores a kind the stack saved.
  W7 bwin: 0027BDE0 maps kind 5 to entry 4 (table 0027BE88), and the us file's entry 4 is (150, 8), the only
     non-default entry.
  W8 sensitivity: the 0027E050 decode read by kind rather than kind - 1 (the 2026-09-18 page's reading) breaks the
     W4 join for all four commands.
  W9 no shipped command list offers command 7: the lists 0027C3D0 reads commands from (codes 6 and 9) are built by
     0031EB20's codes 6-9 arm from static {flag, command} byte tables - code 6: 00D10650 / 00D10660 (6 rows, picked by
     [02EBF190]+4 bit 0x800), code 9: 00D1065C (2 rows) - and that arm's one row-id store is 0031ED35; the other six
     image-wide writers of a row's command word are other list codes' arms.
Exit 1 on any FAIL.
"""
import re, struct, sys, glob
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
def dis(a, b): return [x for x in cs.disasm(d[off(a):off(b)], a)]
def txt(x): return ("%s %s" % (x.mnemonic, x.op_str)).strip()
def at(a, b): return {x.address: txt(x) for x in dis(a, b)}
def u32(v): return struct.unpack_from("<I", d, off(v))[0]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

# W1 - 0027E050: index = kind - 1; per arm read the code store and the sub-selector store
head = at(0x27E050, 0x27E098)
def arm_codes(a):
    code = sub = None
    for x in dis(a, a + 0x50):
        t = txt(x)
        m = re.match(r"mov dword ptr \[rcx \+ 0x4c0\], (0x[0-9a-f]+|\d+)$", t)
        if m: code = int(m.group(1), 0)
        m = re.match(r"mov qword ptr \[rcx \+ 0x4d4\], (0x[0-9a-f]+|\d+)$", t)
        if m: sub = int(m.group(1), 0)
        if t == "mov dword ptr [rcx + 0x4d4], r15d": sub = 1          # r15d = 1 (0027E076)
        if x.mnemonic == "jmp": break
    return code, sub
def table_e050(bias):
    return {k: arm_codes(BASE + u32(BASE + 0x15E384 + 4 * (k - bias))) for k in range(bias, bias + 20)}
KIND = table_e050(1)
check("W1 0027E050 indexes by kind - 1 (lea eax, [rdx - 1]; 20 entries); kind 5 -> code 0xB, sub-selector 7",
      head.get(0x27E06B) == "lea eax, [rdx - 1]" and head.get(0x27E07A) == "cmp eax, 0x13"
      and head.get(0x27E076) == "lea r15d, [r14 + 1]" and KIND[5] == (0xB, 7),
      "kind->(code,sub): " + ", ".join("%d:(%s,%s)" % (k, hex(c) if c is not None else "-", hex(s) if s is not None else "-")
                                      for k, (c, s) in sorted(KIND.items())))

# W2 - the sub-selector is validated as a class-21 id in list code 0xB's arm
t2 = {c: BASE + u32(BASE + 0x1FFB78 + 4 * d[off(BASE + 0x1FFBA4) + c - 1]) for c in range(1, 0x24)}
e = at(0x31ED58, 0x31ED7A)
check("W2 list code 0xB's builder arm validates [list+0x14] as a class 0x15 (21) encoded id",
      t2[0xB] == 0x31ED58 and [c for c, v in t2.items() if v == 0x31ED58] == [0xB]
      and e.get(0x31ED5E) == "mov edx, dword ptr [rbx + 0x14]" and e.get(0x31ED6F) == "lea ecx, [r8 + 0x15]"
      and e.get(0x31ED73) == "call 0x322c50")

# W3 - 0027C3D0: outer table by list code - 6, inner by command word +0x50
outer = {c: BASE + u32(BASE + 0x15C6A0 + 4 * d[off(BASE + 0x15C6B8) + c - 6]) for c in range(6, 6 + 0x17)}
inner = {cmd: BASE + u32(BASE + 0x15C6D0 + 4 * cmd) for cmd in range(0x15)}
def ret_of(a):
    v = None                                             # the last eax immediate before the arm's ret
    for x in dis(a, a + 0x30):
        m = re.match(r"mov eax, (0x[0-9a-f]+|\d+)$", txt(x))
        if m: v = int(m.group(1), 0)
        if x.mnemonic == "ret": return v
        if x.mnemonic in ("jmp", "call") or x.mnemonic.startswith("cmov"): return None
NEXT = {cmd: ret_of(a) for cmd, a in inner.items()}
k3 = at(0x27C44A, 0x27C462)
check("W3 in list codes 6 and 9 the row's command word picks the next kind; command 7 -> 0027C532 -> kind 5, only it",
      [c for c, a in outer.items() if a == 0x27C437] == [6, 9] and k3.get(0x27C44A) == "movzx eax, word ptr [rdx + 0x50]"
      and inner[7] == 0x27C532 and NEXT[7] == 5 and [c for c, a in inner.items() if a == 0x27C532] == [7],
      "command->kind: " + ", ".join("%d:%s" % (c, NEXT[c]) for c in sorted(NEXT) if NEXT[c] is not None))

# W4 - the join between the two tables
join = {cmd: KIND.get(NEXT[cmd]) for cmd in (3, 5, 6, 7)}
check("W4 commands 3, 5, 6, 7 (Items, Summon, Quickening, Foecraft) open the kind whose sub-selector is the same command",
      all(v == (0xB, cmd) for cmd, v in join.items()), str(join))

# W5 - the dispatch path into +0xD8
t5 = {c: BASE + u32(BASE + 0x159D60 + 4 * d[off(BASE + 0x159D98) + c - 1]) for c in range(1, 0x2E)}
p = at(0x278417, 0x278429); q = at(0x278522, 0x2785D3); r = at(0x278870, 0x278897); s = at(0x279187, 0x2791B3)
SIZES = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    f_ = l.rstrip("\n").split("\t")
    try: SIZES[int(f_[0], 16)] = int(f_[2])
    except (ValueError, IndexError): pass
stores = []                                              # per listed body, the dispatch family's range
for f0, sz in SIZES.items():
    if 0x274000 <= f0 < 0x280000 and sz > 0:
        for x in cs.disasm(d[off(f0):off(f0) + sz], f0):
            if x.mnemonic == "mov" and re.match(r"word ptr \[r\w+ \+ 0xd8\], ", x.op_str): stores.append("%08X" % x.address)
check("W5 dispatch: kind from 0027C3D0, stack push + depth, message 31 to itself; its arm 00279187 is the only +0xD8 store",
      p.get(0x27841E) == "call 0x27c3d0" and p.get(0x278423) == "mov dword ptr [rbp - 0x39], eax"
      and q.get(0x278542) == "xor eax, dword ptr [rcx + rdx*4 + 0x70]" and q.get(0x27854A) == "xor dword ptr [rcx + rdx*4 + 0x70], eax"
      and q.get(0x2785C8) == "inc dword ptr [rax + 0x68]"
      and r.get(0x27887E) == "mov qword ptr [rbp - 1], rcx" and r.get(0x278882) == "mov dword ptr [rbp - 9], 0x1f"
      and r.get(0x27887B) == "mov rax, qword ptr [rsi]" and r.get(0x278895) == "call rax"
      and t5[31] == 0x279187 and s.get(0x2791AC) == "mov word ptr [rsi + 0xd8], ax" and stores == ["002791AC"],
      "word stores to +0xD8 in 00274000..00280000: %s" % stores)

# W6 - the other kind sources
c730 = [txt(x) for x in dis(0x27C730, 0x27C862)]
imm = sorted({int(m.group(1), 0) for t in c730 for m in [re.match(r"mov (?:eax|r15d), (0x[0-9a-f]+|\d+)$", t)] if m})
lea = sorted({t for t in c730 if re.match(r"lea r15d, \[r(?:13|ax) \+ 0x[0-9a-f]+\]$", t)})
cst = struct.unpack_from("<4I", d, off(0x915BB0))
check("W6 message 33's other sources: 0027AA70 sends {1, 0} (00915BB0); 0027C730 yields only 0x10..0x13",
      cst[:2] == (1, 0) and imm == [1, 2, 0x10, 0x11, 0x12, 0x13] and "mov r13d, 3" in c730 and lea == ["lea r15d, [r13 + 0xd]", "lea r15d, [rax + 0x10]"],
      "00915BB0=%s imm=%s lea=%s (1 and 2 are loop seeds; r13d=3 so r13+0xd = 0x10, rax=2 so rax+0x10 = 0x12)" % (cst, imm, lea))

# W7 - bwin
t7 = {k: BASE + u32(BASE + 0x15BE88 + 4 * (k - 2)) for k in range(2, 20)}
def ent_of(a):
    t = txt(dis(a, a + 8)[0]); m = re.match(r"mov edx, (0x[0-9a-f]+|\d+)$", t)
    return int(m.group(1), 0) if m else (0 if t == "xor edx, edx" else None)
ent = {k: ent_of(a) for k, a in t7.items()}
files = sorted(glob.glob("D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/us/bin_menu/menubtlwndinfo.bin"))
if files:
    b = Path(files[0]).read_bytes(); cnt = struct.unpack_from("<I", b, 8)[0]
    rows = [struct.unpack_from("<HH", b, 0xC + 4 * i) for i in range(cnt)]
    check("W7 0027BDE0 maps kind 5 to entry 4, and the us file's entry 4 is (150, 8), the only non-default entry",
          ent[5] == 4 and b[:4] == b"bwin" and rows[4] == (150, 8) and [i for i, r in enumerate(rows) if r != (10, 8)] == [4],
          "entries=%s" % rows)
else:
    check("W7 0027BDE0 maps kind 5 to entry 4 (data file not present - the exe half only)", ent[5] == 4)

# W9 - no shipped command list offers command 7
g = at(0x31EB83, 0x31EBF7)
def rows(a, cnt): b = d[off(a):off(a) + 2 * cnt]; return [(b[2 * i], b[2 * i + 1]) for i in range(cnt)]
L6a, L6b, L9 = rows(0xD10650, 6), rows(0xD10660, 6), rows(0xD1065C, 2)
arm_lo, arm_hi = 0x31EB71, 0x31ED58                      # the codes 6-9 arm (W2's table: codes 6..9 -> 0031EB71)
writers = []
for f0, sz in SIZES.items():
    if sz > 0 and f0 < 0x8C0000:
        for x in cs.disasm(d[off(f0):off(f0) + sz], f0):
            if x.mnemonic == "mov" and re.match(r"word ptr \[r\w+ \+ r\w+\*8 \+ 0x50\], ", x.op_str): writers.append(x.address)
in_arm = ["%08X" % a for a in writers if arm_lo <= a < arm_hi]
check("W9 the command lists 0027C3D0 reads (codes 6, 9) are the static tables 00D10650/00D10660 (6 rows) and 00D1065C (2 rows); "
      "command 7 is in neither, and the arm's one row-id store is 0031ED35 (byte [table+1])",
      [c for c, v in t2.items() if v == 0x31EB71] == [6, 7, 8, 9]
      and g.get(0x31EB9B) == "lea rbp, [rip + 0x9f1aba]" and g.get(0x31EBA2) == "mov dword ptr [rsp + 0xb8], 2"
      and g.get(0x31EBD3) == "lea rbp, [rip + 0x9f1a86]" and g.get(0x31EBE1) == "lea rax, [rip + 0x9f1a68]" and g.get(0x31EBE8) == "cmove rbp, rax"
      and g.get(0x31EBEC) == "mov dword ptr [rsp + 0xb8], 6"
      and 7 not in [c for _, c in L6a + L6b + L9] and in_arm == ["0031ED35"]
      and at(0x31EC50, 0x31EC5E).get(0x31EC50) == "movzx eax, byte ptr [rbp + 1]",
      "code 6=%s / %s, code 9=%s; row-id writers image-wide=%s" % ([c for _, c in L6a], [c for _, c in L6b], [c for _, c in L9],
                                                                 ["%08X" % a for a in writers]))

# W8 - sensitivity: the page's kind-indexed reading breaks the join
WRONG = table_e050(0)
wjoin = {cmd: WRONG.get(NEXT[cmd]) for cmd in (3, 5, 6, 7)}
check("W8 sensitivity: read by kind (not kind - 1) the join fails for all four commands",
      all(v != (0xB, cmd) for cmd, v in wjoin.items()), str(wjoin))
print("FAILS", fails)
sys.exit(1 if fails else 0)
