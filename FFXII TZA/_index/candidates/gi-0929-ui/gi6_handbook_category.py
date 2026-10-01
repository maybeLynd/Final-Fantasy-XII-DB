#!/usr/bin/env python3
"""gi6_handbook_category.py - GI-6 (FABLE 2026-09-29): the handbook pages' arg+8 is the 0056EF60 pane kind, and the
kind is the handbook category. One table of 6-byte records {u16 title, u16 help, u8 value, u8 flag} runs from 00D23688:
four category-menu rows (value = the kind the row posts) then eight kind rows at 00D236A0 (value = cursor slot).
Titles resolve in the shipped text; kind 5 = Bestiary is the control (the monster viewer opens only for kind 5).
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

text_control()
REC = lambda a: (u16(a), u16(a + 2), u8(a + 4), u8(a + 5))
print("== 1. the records")
for i in range(12):
    a = 0x00D23688 + 6 * i; t, h, v, f = REC(a)
    print(f"   {a:08X}  title {t:#06x} help {h:#06x} value {v:3d} flag {f}  '{text(t) if t else ''}'")
menu = [REC(0x00D23688 + 6 * c) for c in range(4)]
kind = [REC(0x00D236A0 + 6 * k) for k in range(8)]
check("menu rows post kinds 6, 5, 7, 4", [m[2] for m in menu] == [6, 5, 7, 4], [m[2] for m in menu])
check("each menu row's label is the title of the kind it posts (one record shape across both halves)", all(m[0] == kind[m[2]][0] and m[1] == kind[m[2]][1] for m in menu))
NAMES = {4: "Traveler's Tips", 5: "Bestiary", 6: "Hunts", 7: "Sky Pirate's Den"}
for k, n in NAMES.items():
    check(f"kind {k} title = '{n}'", text(kind[k][0]) == n, text(kind[k][0]))
check("kinds 0-3 carry empty rows in us and 'Unused' rows in de", all(text(kind[k][0]) == "" and "Unused" in text(kind[k][0], "de") for k in range(4)))
print("== 2. the readers agree on the framing")
for a, s in [(0x0056F324, "lea rax, [rip + 0x7b4375]"), (0x0056F32B, "movzx ecx, word ptr [rax + rcx*2]"), (0x0056F32F, "call 0x2f9860"),
             (0x0056F2B1, "mov byte ptr [rcx + 0xc8], dl"), (0x00574AA6, "lea rax, [rip + 0x7aebf3]"),
             (0x0056F678, "lea r12, [rip + 0x7b4009]"), (0x0056F694, "movzx edx, word ptr [r12 + rcx*2 + 2]"), (0x0056F69A, "movzx ecx, word ptr [r12 + rcx*2]"),
             (0x0056F98D, "movzx eax, byte ptr [r8 + rcx*2 + 0xc0368c]"), (0x0056F9AC, "mov edx, 0x8001"), (0x0056F9B5, "call 0x247510"),
             (0x00571ECD, "movzx edx, byte ptr [r9 + rcx*2 + 0xc036a4]"), (0x00571EDB, "call 0x2527b0")]:
    expect(a, s)
check("0056F2A0 / 00574A90 title table base = 00D236A0", riptarget(at(0x0056F324)) == 0x00D236A0 and riptarget(at(0x00574AA6)) == 0x00D236A0)
check("0056F810's label table base = 00D23688", riptarget(at(0x0056F678)) == 0x00D23688)
print("== 3. control: kind 5 is the Bestiary (text pane opens the monster viewer only for kind 5)")
expect(0x00570245, "cmp byte ptr [rdi + 8], 5"); expect(0x0057025A, "call 0x1846f0")
alt5 = u16(0x00D236A4 + 6 * 5 + 2)
check("REJECTS the 00D236A4 framing ({slot, title, help}): it would title kind 5 as '" + text(alt5) + "'", text(alt5) != "Bestiary" and text(kind[5][0]) == "Bestiary")
print("== 4. who sets the kind")
check("0056F2A0 is called only at 00575480 in 00574E80", raw_callers(0x0056F2A0) == [(0x00575480, 0x00574E80)])
for a, s in [(0x00575424, "movzx eax, byte ptr [rdx + 0x10]"), (0x0057547A, "movzx edx, bl"), (0x00574DA0, "mov r8d, 6"), (0x00574D9B, "mov edx, 0x8001"),
             (0x00574D92, "test byte ptr [rax + 0xc0], 0x40"), (0x00574F3C, "mov dword ptr [rdi + 0xc0], 0x40"),
             (0x0056F780, "cmp bl, 2"), (0x0056F7A9, "mov ecx, 0x400b"), (0x0056F7CD, "cmp al, 7"), (0x0056F686, "cmp bl, 4")]:
    expect(a, s)
check("00575580 (payload open) is called from 002814E0 only; 00574CB0 (plain open) from 00281ED0 only",
      sorted({f for s, f in raw_callers(0x00575580)}) == [0x002814E0] and raw_callers(0x00574CB0) == [(0x0028239B, 0x00281ED0)])
check("the kind-6 host installers 00579990 / 00579A40 are called only from 0056EE10",
      raw_callers(0x00579990) == [(0x0056EEF1, 0x0056EE10)] and raw_callers(0x00579A40) == [(0x0056EED2, 0x0056EE10)])
print("== 5. the pages' arg+8 is the pane kind")
check("00570BF0 (-> 00571A50) is called only from 0056EE10", raw_callers(0x00570BF0) == [(0x0056EF27, 0x0056EE10)])
check("00570080 (-> 005742D0) is called only from 005701B0", {f for s, f in raw_callers(0x00570080)} == {0x005701B0})
for a, s in [(0x0056EE28, "movzx ecx, byte ptr [rcx + 0xc8]"), (0x0056EF1A, "movzx edx, cl"), (0x00570C16, "mov byte ptr [rsp + 0x38], dl"),
             (0x00571A95, "movzx eax, byte ptr [rcx + 8]"), (0x00571A99, "mov byte ptr [rbx + 0xe8], al"), (0x00571ABD, "cmp byte ptr [rbx + 0xe8], 5"),
             (0x0056EC63, "movzx eax, byte ptr [rbx + 0xc8]"), (0x005701FE, "movzx eax, byte ptr [rdi + 8]"), (0x00570202, "mov byte ptr [rbx + 0xe1], al"),
             (0x005700E4, "movzx eax, byte ptr [rdi + 0xe1]"), (0x00574328, "mov byte ptr [rdi + 0x8060], r8b"),
             (0x0057439C, "cmp al, 2"), (0x005743A0, "cmp al, 5"), (0x005743A2, "mov ecx, 0x27"), (0x005743A7, "mov r8d, 0x23"), (0x005743B3, "mov r8d, 0x26")]:
    expect(a, s)
cmp_e8 = [a for a, f, t in sweep(lambda x: x.mnemonic == "cmp" and "[rbx + 0xe8]" in x.op_str, 0x00571A50, 0x00571A51)]
check("00571A50 compares its kind only against 5 (four sites)", len(cmp_e8) == 4 and all(txt(a).endswith(", 5") for a in cmp_e8), [hex(a) for a in cmp_e8])
done()
