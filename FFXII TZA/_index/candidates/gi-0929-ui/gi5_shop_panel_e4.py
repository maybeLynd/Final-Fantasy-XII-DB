#!/usr/bin/env python3
"""gi5_shop_panel_e4.py - GI-5 (FABLE 2026-09-29): the trade panel 0056D370's +0xE4 is a bitfield - bit 0 sell,
bits 6-13 the goods kind of the current tab (0x1C0 = kind 7 loot, 0x2C0 = kind 11 bazaar), bits 14-21 the row variant.
Image-wide +0xE4 write sweep (control: 0056D370's own four writes) gives 17 panel writes in five functions; the kind
tables and the Buy / Sell / Bazaar category sets are decoded. Run from any cwd; exits non-zero on any failed check."""
# ---- shared preamble (inlined into each gi-0929-ui checker by build_checkers.py) ----
import struct, sys, bisect, os, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
EXTRACT = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle"
FST = "D:/FFXII MP Mod/FFXII_TestClient1/FileSizeTables/FileSizeTable_US.fst"
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
BASE = 0x120000
d = open(EXE, "rb").read()
_pe = struct.unpack_from("<I", d, 0x3C)[0]; _ns = struct.unpack_from("<H", d, _pe + 6)[0]; _opt = struct.unpack_from("<H", d, _pe + 20)[0]
SECS = []; TEXT = None
for _i in range(_ns):
    _o = _pe + 24 + _opt + _i * 40
    nm = d[_o:_o + 8].rstrip(b"\0"); vs, va, ro = struct.unpack_from("<I", d, _o + 8)[0], struct.unpack_from("<I", d, _o + 12)[0], struct.unpack_from("<I", d, _o + 20)[0]
    SECS.append((va, vs, ro))
    if nm == b".text": TEXT = (BASE + va, BASE + va + vs, ro)
def off(a):
    r = a - BASE
    for va, vs, ro in SECS:
        if va <= r < va + vs: return ro + r - va
FN = []
for _l in open(FUNCS, encoding="utf-8", errors="replace"):
    _p = _l.rstrip("\n").split("\t")
    try: FN.append((int(_p[0], 16), int(_p[2]), _p[1]))
    except (ValueError, IndexError): pass
FN.sort(); FSTART = [f[0] for f in FN]; SIZE = {f[0]: f[1] for f in FN}
def fnof(a):
    i = bisect.bisect_right(FSTART, a) - 1
    return FN[i][0] if i >= 0 and a < FN[i][0] + FN[i][1] else None
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
_cache = {}
def ins_of(fn):
    if fn not in _cache: _cache[fn] = list(md.disasm(d[off(fn):off(fn) + SIZE[fn]], fn))
    return _cache[fn]
def at(a):
    for x in ins_of(fnof(a)):
        if x.address == a: return x
def txt(a):
    x = at(a); return f"{x.mnemonic} {x.op_str}" if x else "<no instruction boundary>"
def riptarget(x):
    for op in x.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP: return x.address + x.size + op.mem.disp
def u8(a): return d[off(a)]
def u16(a): return struct.unpack_from("<H", d, off(a))[0]
def u32(a): return struct.unpack_from("<I", d, off(a))[0]
def rel32_table(tab, n): return [BASE + u32(tab + 4 * i) for i in range(n)]
FAILS = 0
def check(name, ok, detail=""):
    global FAILS
    if not ok: FAILS += 1
    print(("PASS " if ok else "FAIL ") + name + (("  -- " + str(detail)) if detail else ""))
def expect(a, sub):
    t = txt(a); check(f"{a:08X} is '{sub}'", sub in t, t)
def raw_callers(target):
    lo, hi, ro = TEXT; out = []
    blob = d[ro:ro + (hi - lo)]
    for m in re.finditer(b"[\xe8\xe9]", blob):
        i = m.start()
        if i + 5 > len(blob): break
        if lo + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == target: out.append(lo + i)
    # keep only sites that decode as a call/jmp at an instruction boundary of a listed function
    good = []
    for s in out:
        f = fnof(s)
        if f is None: good.append((s, None)); continue
        x = at(s)
        if x is not None and x.mnemonic in ("call", "jmp"): good.append((s, f))
    return good
def sweep(pred, lo=None, hi=None):
    """decode every listed function in [lo,hi) and return [(addr, fn, text)] where pred(x) is true"""
    lo = lo or TEXT[0]; hi = hi or TEXT[1]; out = []
    for f, sz, _n in FN:
        if not (lo <= f < hi): continue
        o = off(f)
        if o is None: continue
        for x in md.disasm(d[o:o + sz], f):
            if pred(x): out.append((x.address, f, f"{x.mnemonic} {x.op_str}"))
    return out
WR = {"mov", "or", "and", "xor", "add", "sub", "inc", "dec", "bts", "btr", "btc", "not", "neg", "shl", "shr", "sar"}
def writes_disp(disp):
    def p(x):
        if x.mnemonic not in WR or not x.operands: return False
        op = x.operands[0]
        return op.type == X86_OP_MEM and op.mem.base not in (0, X86_REG_RIP) and op.mem.disp == disp
    return p
# text ids -> shipped strings (group = id/1000 -> loader id byte 01E09F68[group] -> FST size -> st2e file)
_fst = None; _sizes = {}
def textfile(group, loc="us"):
    global _fst
    if _fst is None:
        _fst = open(FST, "rb").read()
        for fnm in os.listdir(f"{EXTRACT}/us/binaryfile"):
            _sizes.setdefault(os.path.getsize(f"{EXTRACT}/us/binaryfile/{fnm}"), []).append(fnm)
    lid = d[off(0x01E09F68 + group)]
    sz = struct.unpack_from("<i", _fst, 4 * (2 * 5000 + lid))[0]
    return (_sizes.get(sz) or [None])[0]
def _dec(b):
    out = []
    for c in b:
        if c == 0: break
        if 0x20 <= c <= 0x39: out.append(chr(65 + c - 0x20))
        elif 0x3A <= c <= 0x53: out.append(chr(97 + c - 0x3A))
        elif 0x54 <= c <= 0x5D: out.append(chr(48 + c - 0x54))
        elif c == 4: out.append(" ")
        elif c == 2: out.append("/")
        elif c == 0xAC: out.append("'")
        else: out.append("{%02X}" % c)
    return "".join(out)
def text(tid, loc="us"):
    g, r = divmod(tid, 1000)
    fnm = textfile(g)
    fb = open(f"{EXTRACT}/{loc}/binaryfile/{fnm}", "rb").read()
    tab = struct.unpack_from("<I", fb, 0x14)[0]
    o = struct.unpack_from("<I", fb, tab + 16 + 4 * r)[0]
    return _dec(fb[tab + 12 + o: tab + 12 + o + 400])
def text_control():
    t = text(12000); check("text-id control: 12000 -> listhelp_status.bin row 0 (KO help)", textfile(12) == "listhelp_status.bin" and "lost consciousness" in t, t[:60])
def done():
    print(f"\nFAILS {FAILS}")
    sys.exit(1 if FAILS else 0)
# ---- end preamble ----

text_control()
print("== 1. every +0xE4 write, image-wide (control: 0056D4FD, 0056D5EC, 0056D712, 0056D736)")
w = sweep(writes_disp(0xE4))
print(f"   {len(w)} +0xE4 writes image-wide")
ws = {a for a, f, t in w}
check("control: 0056D370's four writes are found", {0x0056D4FD, 0x0056D5EC, 0x0056D712, 0x0056D736} <= ws)
PANEL_FNS = {0x0056D370, 0x0056C490, 0x0056C850, 0x0056D940, 0x0056D9D0}
pw = sorted((a, f, t) for a, f, t in w if f in PANEL_FNS)
for a, f, t in pw: print(f"   panel write {a:08X} in {f:08X}  {t}")
check("17 writes in the five panel bodies", len(pw) == 17, len(pw))
region = [(a, f, t) for a, f, t in w if 0x00563000 <= f < 0x0057E000 and f not in PANEL_FNS]
for a, f, t in region: print(f"   other shop-region write {a:08X} in {f:08X}  {t}")
check("the 00564xxx writes go through [rbx+0xD8] (the list control), e.g. 0056423E base rax loaded from rbx+0xd8",
      "rax, qword ptr [rbx + 0xd8]" in txt(0x00564237) and "rax, qword ptr [rbx + 0xd8]" in txt(0x005646D9) and "rax, qword ptr [rbx + 0xd8]" in txt(0x00564CD4))
check("0056C950 points [mode+0xD8] at the panel's +0xC0 list (0056C9E6/0056C9ED)", "mov rax, qword ptr [rcx + 0xc0]" in txt(0x0056C9E6) and "mov qword ptr [rbx + 0xd8], rax" in txt(0x0056C9ED))
print("== 2. the panel bodies hold the panel")
cal = lambda t: sorted({f for s, f in raw_callers(t)})
check("0056C490 is called only from 0056D370 and 0056C850", cal(0x0056C490) == [0x0056C850, 0x0056D370], [hex(x) for x in cal(0x0056C490)])
check("0056C850 is reached only from 0056D370 (call) and 0056E580 (jmp)", cal(0x0056C850) == [0x0056D370, 0x0056E580])
check("0056D940 and 0056D9D0 only from 0056CA60", cal(0x0056D940) == [0x0056CA60] and cal(0x0056D9D0) == [0x0056CA60])
check("0056CA60 only from 0056DED0", cal(0x0056CA60) == [0x0056DED0])
check("0056C950 (the panel installer) only from 0056DD50 and 0056DED0", cal(0x0056C950) == [0x0056DD50, 0x0056DED0])
check("0056DD50 only from 0057C070", cal(0x0056DD50) == [0x0057C070])
r = sweep(lambda x: riptarget(x) == 0x0056E140)
check("0056E140 (the mode object's procedure) is referenced only at 0056DD66", [a for a, f, t in r] == [0x0056DD66])
print("== 3. the fields")
for a, s in [(0x0056D69C, "movzx edx, byte ptr [r9]"), (0x0056D6B7, "and eax, 0xffffc03f"), (0x0056D6BC, "shl edx, 6"),
             (0x0056D6F8, "movzx r8d, byte ptr [rcx + r8 + 0xc035e8]"), (0x0056D703, "shl r8d, 0xe"), (0x0056D712, "mov dword ptr [rdi + 0xe4], r8d"),
             (0x0056D71D, "mov eax, dword ptr [r9 + 4]"), (0x0056D721, "and eax, 1"), (0x0056D736, "mov dword ptr [rdi + 0xe4], eax"),
             (0x0056D46F, "test r8b, 1"), (0x0056D478, "call 0x310870"), (0x0056D49A, "call 0x2feeb0"),
             (0x0056D488, "cmp eax, 0x1c0"), (0x0056D496, "mov cl, 0xe"), (0x0056D4AC, "cmp eax, 0x2c0"), (0x0056D4C0, "call 0x30b630"),
             (0x0056D4CC, "mov cl, 0x13"), (0x0056D4FD, "or dword ptr [rdi + 0xe4], 0x30"), (0x0056D611, "cmp eax, 0x2c0"), (0x0056D61E, "call 0x57a480"),
             (0x0056D53B, "movzx eax, byte ptr [rax + r8 + 0xc035f8]"), (0x0056C4C5, "lea r12d, [rax*2 + 0xc6b]"),
             (0x0056D9BA, "shl eax, 0x16"), (0x0056DA1F, "shl eax, 3"), (0x0056C83E, "xor dword ptr [rbx + 0xe4], eax")]:
    expect(a, s)
check("prompt 0xC6B + 2*bit0: 'Select an item to buy.' / '... to sell.'", "to buy" in text(0xC6B) and "to sell" in text(0xC6D), (text(0xC6B), text(0xC6D)))
print("== 4. the kind tables")
VAR = [u8(0x00D235E8 + k) for k in range(12)]; MAXQ = [u8(0x00D235F8 + k) for k in range(12)]
check("row variant 00D235E8[kind] = 0,0,0,0,0,1,1,0,2,1,1,3", VAR == [0, 0, 0, 0, 0, 1, 1, 0, 2, 1, 1, 3], VAR)
check("max quantity 00D235F8[kind] = 99 x5, 1, 1, 99, 1, 1, 1, 255", MAXQ == [99, 99, 99, 99, 99, 1, 1, 99, 1, 1, 1, 255], MAXQ)
LIST = [u16(0x00D23D00 + 4 * k) for k in range(12)]
check("inventory list per kind (00D23D00 word 0, codes 8+kind): 1,2,3,4,0,8,9,11,5,6,7", LIST[:11] == [1, 2, 3, 4, 0, 8, 9, 11, 5, 6, 7], LIST)
for a, s in [(0x0056E945, "mov ecx, 0x14"), (0x0056E94C, "mov eax, 8"), (0x0056E956, "add edx, eax"), (0x0057D70F, "lea rbx, [rcx*4 + 0xc03d00]"),
             (0x0057D728, "movzx ecx, word ptr [rbx + r12]"), (0x0057D72D, "call 0x252f40")]:
    expect(a, s)
idx = [u8(0x0056DCD4 + c) for c in range(32)]; arms = rel32_table(0x0056DCA0, 13)
ARMV = {0x56DC52: 0, 0x56DC55: 1, 0x56DC5B: 2, 0x56DC61: 3, 0x56DC67: 4, 0x56DC6D: 5, 0x56DC73: 6, 0x56DC79: 7, 0x56DC7F: 8, 0x56DC85: 9, 0x56DC8B: 10, 0x56DC91: 11, 0x56DC97: 255}
CAT = [ARMV[arms[i]] for i in idx]
check("0056DC30 category -> kind", CAT == [11, 0, 0, 0, 0, 1, 1, 1, 1, 2, 3, 4, 8, 9, 10, 5, 6, 6, 6, 6, 6, 6, 255, 255, 255, 255, 7, 3, 3, 3, 3, 8], CAT)
print("== 5. shop verbs -> key -> category set -> kinds")
keys = [u32(0x00D23920 + 4 * o) for o in range(3)]
check("0057C070 option 0/1/2 keys = 0x5AF / 0x5A2 / 0x5AE", keys == [0x5AF, 0x5A2, 0x5AE], [hex(k) for k in keys])
kmap = {u16(0x00D233A0 + 4 * i): u16(0x00D233A0 + 4 * i + 2) for i in range(0x21)}
def cats(setn):
    p = struct.unpack_from("<Q", d, off(0x01F2CB90 + 8 * setn))[0]; n = struct.unpack_from("<i", d, off(p))[0]
    return [u8(p + 8 * i + 4) for i in range(n)]
got = {k: sorted({CAT[c] for c in cats(kmap[k])}) for k in keys}
check("Buy (0x5AF, set 32) offers kinds 0-7 and 9", got[0x5AF] == [0, 1, 2, 3, 4, 5, 6, 7, 9], got[0x5AF])
check("Sell (0x5A2, set 19) offers kinds 0-4 and 7", got[0x5A2] == [0, 1, 2, 3, 4, 7], got[0x5A2])
check("Bazaar (0x5AE, set 31) offers kind 11", got[0x5AE] == [11], got[0x5AE])
check("buy / sell goods codes (00D23D60 / 00D23D6C) = kind + 0x14 / kind + 8",
      [u8(0x00D23D60 + i) for i in range(9)] == [20, 21, 22, 23, 24, 25, 26, 27, 29] and [u8(0x00D23D6C + i) for i in range(6)] == [8, 9, 10, 11, 12, 15])
for a, s in [(0x0056DE3D, "lea ecx, [rsi - 0x597]"), (0x0056DE49, "cmp ecx, 6"), (0x0056DE4E, "lea ecx, [rsi - 0x59f]"), (0x0056DE54, "cmp ecx, 3")]:
    expect(a, s)
sell = lambda k: (0 <= k - 0x597 <= 6) or (0 <= k - 0x59F <= 3)
check("only the Sell key sets bit 0", [sell(k) for k in keys] == [False, True, False])
print("== regression: the old reading")
check("REJECTS 'buy 0x1C0 vs sell 0x2C0': 0x1C0>>6 = kind 7 = loot (list 11), 0x2C0>>6 = kind 11 = bazaar, and the commit branches on bit 0",
      (0x1C0 >> 6, 0x2C0 >> 6) == (7, 11) and LIST[7] == 11 and "test r8b, 1" in txt(0x0056D46F))
done()
