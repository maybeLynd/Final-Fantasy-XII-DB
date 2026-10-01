#!/usr/bin/env python3
"""gi1_tabstrip_marker.py - GI-1 (FABLE 2026-09-29): 00566C10 is a tab-strip marker whose +0x14 bit 0 means
'has a sliding pointer' (1 gambit strip, 0 shop strip); condition vs action is the pick list's +0x588 (1 condition,
2 action) and shows as the tab frame (0 condition, 1 action). Also: the pick list 0056B4D0 is created by the editor.
Run from any cwd; exits non-zero on any failed check."""
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

print("== 1. who installs 00566C10 (rip references, all listed functions; controls: both installers)")
refs = sweep(lambda x: riptarget(x) == 0x00566C10)
check("exactly two rip references to 00566C10, in 00567200 and 0056C170",
      sorted((a, f) for a, f, _ in refs) == [(0x00567440, 0x00567200), (0x0056C2E1, 0x0056C170)], [(hex(a), hex(f)) for a, f, _ in refs])
check("no E8/E9 call to 00566C10", raw_callers(0x00566C10) == [], raw_callers(0x00566C10))
print("== 2. the create record's +0x14 (message at rsp+0x38 -> arg rsp+0x20, so +0x14 is [rsp+0x34])")
for a, s in [(0x0056C2DC, "lea r8, [rsp + 0x38]"), (0x0056C2EC, "lea rax, [rsp + 0x20]"), (0x0056C2F6, "mov ecx, 1"),
             (0x0056C304, "mov dword ptr [rsp + 0x34], ecx"), (0x0056C35E, "or dword ptr [rax + 0xe8], 2"),
             (0x0056740B, "lea r8, [rsp + 0x38]"), (0x00567421, "lea rax, [rsp + 0x20]"), (0x00567319, "xor edx, edx"),
             (0x005673A3, "mov edx, 0"), (0x00567438, "mov dword ptr [rsp + 0x34], edx")]:
    expect(a, s)
print("== 3. the merge and every reader of +0xE8 bit 0 in 00566C10 / 00566B70")
for a, s in [(0x00566F4E, "mov eax, dword ptr [rdi + 0x14]"), (0x00566F51, "xor eax, dword ptr [rbx + 0xe8]"),
             (0x00566F57, "and eax, 1"), (0x00566F5A, "xor dword ptr [rbx + 0xe8], eax"),
             (0x00566C4D, "test byte ptr [rbx + 0xe8], 1"), (0x00566C7D, "call 0x242b90"),
             (0x00566DBB, "test byte ptr [rbx + 0xe8], 1"), (0x00566FB1, "test byte ptr [rbx + 0xe8], 1"),
             (0x00566B70, "test byte ptr [rcx + 0xe8], 1"), (0x00566CA3, "call 0x2cc8d0"), (0x00567630, "call 0x566b70")]:
    expect(a, s)
rd = [a for a, f, t in sweep(lambda x: "0xe8]" in x.op_str and x.mnemonic == "test", 0x00566C10, 0x00566C11)]
check("00566C10 tests +0xE8 exactly at 00566C4D, 00566DBB, 00566E34 (bit 1), 00566FB1", rd == [0x00566C4D, 0x00566DBB, 0x00566E34, 0x00566FB1], [hex(a) for a in rd])
c = raw_callers(0x00242B90)
check("00242B90 (the pointer draw) has one caller, 00566C7D", [s for s, f in c] == [0x00566C7D], c)
print("== 4. writers of +0xE8 in 00560000-00580000 (controls 00566F5A, 0056C35E)")
w = sweep(writes_disp(0xE8), 0x00560000, 0x00580000)
for a, f, t in w: print(f"   {a:08X} in {f:08X}  {t}")
ws = {a for a, f, t in w}
check("controls found: 00566F5A and 0056C35E", {0x00566F5A, 0x0056C35E} <= ws)
mine = [a for a, f, t in w if f in (0x00566C10, 0x0056C170, 0x00567200, 0x00566B70, 0x005674B0, 0x005678F0)]
check("the marker-holding bodies write +0xE8 only at the two controls", sorted(mine) == [0x00566F5A, 0x0056C35E], [hex(a) for a in mine])
print("== 5. condition vs action: 0056ADA0 picks the tab builder by +0x588")
for a, s in [(0x0056ADC1, "cmp dword ptr [rcx + 0x588], 1"), (0x0056ADC8, "jne 0x56add1"), (0x0056ADCA, "call 0x56b100"),
             (0x0056ADD1, "call 0x56ae80"), (0x0056B6BC, "mov eax, dword ptr [rbx + 0x18]"), (0x0056B6BF, "mov dword ptr [rsi + 0x588], eax"),
             (0x0056B3A5, "mov dword ptr [rsp + 0x50], r8d"), (0x0056A45B, "movzx ecx, byte ptr [rbx + 0x336]"),
             (0x0056A462, "mov dword ptr [rax + 0x588], ecx"), (0x0056A516, "call 0x56ae80"), (0x0056A54B, "call 0x56b100"),
             (0x00567E0E, "movsx ecx, byte ptr [rbx + 0x33e]"), (0x00567E69, "lea r8d, [rax + 1]"), (0x00567E39, "lea r8d, [rax + 2]")]:
    expect(a, s)
print("== 6. the two tab builders: grid, menu kind, class query, frame constants")
check("00327BD0 reads byte 0208D310 (target-condition grid pages)", riptarget(at(0x00327BD0)) == 0x0208D310)
check("00327BB0 reads byte 0208D300 (action grid pages)", riptarget(at(0x00327BB0)) == 0x0208D300)
for a, s in [(0x0056B16D, "call 0x327bd0"), (0x0056B1D4, "mov dword ptr [rsp + 0x30], 0x23"), (0x0056B273, "lea ecx, [rax + 0xa]"),
             (0x0056B135, "xor esi, esi"), (0x0056B1B8, "mov word ptr [rdi + 4], si"), (0x0056B2B7, "mov eax, 2"), (0x0056B2BC, "mov word ptr [rdi + 4], ax"),
             (0x0056AEE3, "call 0x327bb0"), (0x0056AF65, "mov dword ptr [rsp + 0x30], 0x22"), (0x0056B005, "lea ecx, [rax - 0x74]"),
             (0x0056AF1D, "mov eax, 1"), (0x0056AF49, "mov word ptr [rsi + 4], ax"), (0x0056B060, "mov eax, 3"), (0x0056B065, "mov word ptr [rsi + 4], ax"),
             (0x0056C264, "movsx rax, word ptr [rdi + 4]"), (0x0056C0F9, "mov word ptr [rbx + 0xa], r8w")]:
    expect(a, s)
print("== 7. layout keys (layout-key-slots.tsv) and the 0056B350 slide")
slots = {}
for l in open(DB + r"\16-UI\Layout-Parameter-System\members\layout-key-slots.tsv", encoding="utf-8"):
    p = l.rstrip("\n").split("\t")
    if len(p) > 2: slots[p[2]] = p[0]
check("01F2CB08/0C = GambitIconOffsetX/Y", (slots.get("01F2CB08"), slots.get("01F2CB0C")) == ("GambitIconOffsetX", "GambitIconOffsetY"))
check("01F2CB10 = GambitTargetListMoveX, 01F2CB14 = GambitActionListMoveX", (slots.get("01F2CB10"), slots.get("01F2CB14")) == ("GambitTargetListMoveX", "GambitActionListMoveX"))
expect(0x0056B47D, "cmp edi, 1")
check("mode 1 reads GambitTargetListMoveX (0056B482)", riptarget(at(0x0056B482)) == 0x01F2CB10)
check("otherwise GambitActionListMoveX, negated (0056B48A, 0056B490)", riptarget(at(0x0056B48A)) == 0x01F2CB14 and "neg edx" in txt(0x0056B490))
print("== 8. the pick list is created by the editor (tree direction)")
check("0056B350's callers are 00567E43 and 00567E73 in 00567D80", [s for s, f in raw_callers(0x0056B350)] == [0x00567E43, 0x00567E73])
check("00567D80's caller is 00569E63 in the editor 005691E0", raw_callers(0x00567D80) == [(0x00569E63, 0x005691E0)])
for a, s in [(0x0056B38A, "mov qword ptr [rsp + 0x38], rcx"), (0x0056B3BE, "lea rdx, [rip + 0x10b]"), (0x0056B3CA, "mov qword ptr [rbx + 0xe8], rax"),
             (0x0056B69E, "mov rax, qword ptr [rbx]"), (0x0056B6A1, "mov qword ptr [rsi + 0xc8], rax"), (0x0056A454, "mov qword ptr [rax + 0xc8], rbx")]:
    expect(a, s)
print("== regression: the old readings")
check("REJECTS '0056AE80 = condition side': it builds kind 0x22 pages of the action grid 0208D300", "0x22" in txt(0x0056AF65) and riptarget(at(0x00327BB0)) == 0x0208D300)
check("REJECTS '+0x14 bit 0 = condition/action art': both gambit pickers use the one installer 0056C170 with +0x14 = 1", "mov ecx, 1" in txt(0x0056C2F6))
done()
