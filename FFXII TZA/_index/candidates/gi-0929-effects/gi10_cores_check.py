#!/usr/bin/env python3
"""gi10_cores_check.py - GI-10 residue (FABLE reader, 2026-09-29): the four effect simulation cores.
00545650 wave step (three passes: update into y, gradients into z/w with the x<->y exchange, last-row exchange);
00542740 trail history (three 32-entry histories + turn angle; acos table; quarter-turn bend);
00533B20 node chain (N streamers x 32 points; optional damped impulse histories; chain advance);
00548A00 0x71 streamers (same chain advance; the six triples are 3 texture layers x 6 scalars read by 005480E0);
004D40E0 the translated VU1 program: where the layer block lands and what it does with each value (2026-09-29);
0030A190 the world-state gate on the +0x28 word (022C2160 in {5, 6}).
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

print("== 00545650: the wave step")
for a, s in [(0x00545691, "add eax, 0x10"), (0x0054565B, "movsxd r11, dword ptr [rcx + 0x10]"), (0x0054569B, "movsxd rbx, dword ptr [rcx + 0x14]"),
             (0x005456AF, "movsxd r9, dword ptr [rcx + 0x18]"), (0x00545730, "movups xmm0, xmmword ptr [r10 + 0x30]"),
             (0x00545942, "movss dword ptr [rip"), (0x00545964, "movups xmmword ptr [rdx], xmm0"),
             (0x00545B5E, "subss xmm7, xmm1"), (0x00545B6B, "subss xmm8, xmm2"), (0x00545760, "dec dword ptr [rip"),
             (0x00545AE9, "dec dword ptr [rip"), (0x00545E9E, "jg 0x545da0")]:
    expect(a, s)
check("00545691 base register is GPR[0] ($zero, 022D8F10)", riptarget(at(0x0054568B)) == 0x022D8F10)
check("pass-1 result goes to vf05.y (022D91A0 + 5*16 + 4)", riptarget(at(0x00545942)) == 0x022D91A0 + 5 * 16 + 4)
check("pass-2 gradients go to vf05.z / vf05.w", riptarget(at(0x00545C5A)) == 0x022D91A0 + 5 * 16 + 8 and riptarget(at(0x00545C62)) == 0x022D91A0 + 5 * 16 + 12)
check("coefficients land in vf25 (022D9230)", riptarget(at(0x0054573F)) == 0x022D91A0 + 25 * 16)
print("== 00542740: the trail history")
for a, s in [(0x00542763, "test r9d, r9d"), (0x0054277F, "cmp eax, ecx"), (0x005431A4, "movaps xmm0, xmmword ptr [rdx]"),
             (0x005431AF, "movaps xmm1, xmmword ptr [r8]"), (0x005434F5, "call 0x46f460"), (0x00543511, "call 0x202e10"),
             (0x005436A6, "call 0x202b70"), (0x00543724, "mulss xmm2, dword ptr [rip"), (0x00543854, "movss dword ptr [rbx + 0x4b0], xmm6"),
             (0x005438A9, "mulss xmm0, dword ptr [rip")]:
    expect(a, s)
check("0.2 at 008F30F8 and 0.8 at 008F3108", abs(struct.unpack_from("<f", d, off(0x008F30F8))[0] - 0.2) < 1e-6 and abs(struct.unpack_from("<f", d, off(0x008F3108))[0] - 0.8) < 1e-6)
tab = [struct.unpack_from("<f", d, off(0x00D12590 + 4 * i))[0] for i in (0, 8191, 16383)]
check("0046F460's table 00D12590 is acos (pi, ~pi/2, 0)", abs(tab[0] - 3.14159) < 1e-3 and abs(tab[1] - 1.5708) < 1e-3 and abs(tab[2]) < 1e-6, tab)
expect(0x0046F4A0, "and eax, 0x3fff")
print("== 00533B20: the node chain")
for a, s in [(0x00533B4B, "cmp dword ptr [rcx + 0x18], 0"), (0x00533BF9, "test byte ptr [rbx + 0x140], 1"), (0x00533C3F, "je 0x534548"),
             (0x00533C90, "movss xmm2, dword ptr [rbx + 0x138]"), (0x00533CBA, "movss xmm1, dword ptr [rbx + 0x13c]"),
             (0x005344F0, "call 0x202b90"), (0x00534503, "call 0x202b90"), (0x00534590, "movss xmm0, dword ptr [rdi + 0x230]"),
             (0x00534980, "movups xmmword ptr [rdi + 0x10], xmm0"), (0x00535F5B, "movss xmm0, dword ptr [rdi + 0x234]"),
             (0x00535F63, "addss xmm0, dword ptr [rdi + 0x230]"), (0x00535FA2, "cmovg eax, ebp"), (0x00534576, "mov ebp, 0x20")]:
    expect(a, s)
for a, s in [(0x00532FA3, "mov dword ptr [rbx], ebp"), (0x00532F92, "lea rcx, [rbx + 0x20]"), (0x005330E5, "movss dword ptr [rbx + 0x420], xmm1"),
             (0x00533108, "movss dword ptr [rbx + 0x428], xmm7"), (0x0053319E, "mov dword ptr [rbx + 0x430], ebp"), (0x005331DE, "add rbx, 0x440")]:
    expect(a, s)
print("== 00548A00 and its consumers: the 0x71 streamers and the six triples")
for a, s in [(0x00548A0C, "cmp byte ptr [rcx + 0x66], 0"), (0x00548AC0, "cmp dword ptr [rdi + 0x140], ebp"), (0x00548B50, "movss xmm0, dword ptr [rbx + 0x230]"),
             (0x0054A52A, "movss xmm0, dword ptr [rbx + 0x234]"), (0x0054A604, "movzx eax, byte ptr [rdi + 0x7c]"), (0x0054A640, "call 0x44b960"),
             (0x0054A658, "call 0x3a6e60"), (0x0054A576, "add rbx, 0x450")]:
    expect(a, s)
small = sorted({a for a, f, t in sweep(lambda x: any(op.type == X86_OP_MEM and op.mem.base != 0 and op.mem.index == 0 and 0 <= op.mem.disp < 0x48
                                                     and x.reg_name(op.mem.base) == "rdi" for op in x.operands), 0x00548A00, 0x00548A01)})
check("00548A00 reads nothing of P+0x00..+0x47 (the six triples)", small == [], [hex(a) for a in small])
for a, s in [(0x005487D8, "lea rsi, [rbp + 0x3c]"), (0x005487E0, "cmp byte ptr [r12 + rbp + 0x78], 0"), (0x00548807, "movss xmm0, dword ptr [rsi - 0xc]"),
             (0x00548814, "movss xmm1, dword ptr [rsi]"), (0x00548820, "movss xmm0, dword ptr [rsi - 0x3c]"), (0x0054882D, "movss xmm1, dword ptr [rsi - 0x30]"),
             (0x0054883A, "movss xmm0, dword ptr [rsi - 0x24]"), (0x00548847, "movss xmm1, dword ptr [rsi - 0x18]"), (0x0052A581, "add r14, 0x570"),
             (0x0052A686, "add r14, 0xf0"), (0x0052A5E3, "call 0x431830")]:
    expect(a, s)
check("the builder's six stores go to VU1 packet dwords 02AE8848..02AE885C", [riptarget(at(a)) for a in (0x0054880C, 0x00548818, 0x00548825, 0x00548832, 0x0054883F, 0x0054884C)] == [0x02AE8848, 0x02AE884C, 0x02AE8850, 0x02AE8854, 0x02AE8858, 0x02AE885C])
c = raw_callers(0x005480E0)
check("005480E0 is called from the 0x71 walk 0052A360", [f for s, f in c] == [0x0052A360], c)
print("== 004D3FE0 / 005480E0: where the layer block lands in VU memory")
x = at(0x004D4011)
imm = x.operands[1].imm if x and len(x.operands) > 1 else None
check("004D4011 stores the VIF code 0x6C090046 at template +0xC", x is not None and "[rbx + 0xc]" in x.op_str and imm == 0x6C090046, txt(0x004D4011))
if imm is not None:
    check("0x6C090046 decodes as UNPACK V4-32 (cmd 0x6C), 9 cells, to cell 0x46", ((imm >> 24) & 0xFF, (imm >> 16) & 0xFF, imm & 0x3FF) == (0x6C, 9, 0x46), hex(imm))
for a, s in [(0x004D4051, "[rbx + 0x68], 8"), (0x004D405D, "[rbx + 0x78], 6"), (0x004D4070, "[rbx + 0x88], 0x42"), (0x004D4086, "[rbx + 0x98], 0x47"),
             (0x004D402F, "[rbx + 0x40], rax"), (0x004D4000, "movabs rax, 0x8000000080"), (0x00548893, "movups xmmword ptr [r14], xmm0")]:
    expect(a, s)
c = raw_callers(0x004D3FE0)
check("004D3FE0 is called at 0037E317 (from 0037E0F0) on 02AE8830", 0x0037E317 in [s for s, f in c] and riptarget(at(0x0037E310)) == 0x02AE8830, c)
check("005480E0 sends the template head 02AE8830 (00548865) and copies 0xC0 bytes from 02AE8840 (005488A5)",
      riptarget(at(0x00548865)) == 0x02AE8830 and riptarget(at(0x005488A5)) == 0x02AE8840 and "rdi + 0xb0" in txt(0x00548927))
check("the walk colour goes to 02AE8870 = cell 0x49 (0x46 + 3)", riptarget(at(0x00548859)) == 0x02AE8870 == 0x02AE8840 + 3 * 16)
print("== 004D40E0: the translated VU1 program reads the six values")
vi0w = sweep(lambda x: x.mnemonic in WR and len(x.operands) > 0 and x.operands[0].type == X86_OP_MEM and riptarget(x) == 0x02064B0C)
check("no listed function writes VI00 02064B0C through rip (so [r9 + N] is absolute cell N)", vi0w == [], vi0w[:5])
for a, s in [(0x004D63CF, "lea eax, [r9 + 0x46]"), (0x004D67E6, "lea eax, [rdx + 0x47]"), (0x004D63F9, "shufps xmm2, xmm2, 0xaa"),
             (0x004D6401, "subss xmm5, xmm2"), (0x004D6438, "divss xmm2, xmm3"), (0x004D656F, "divss xmm0, xmm5"),
             (0x004D6977, "mulss xmm4, xmm1"), (0x004D6982, "mulss xmm0, xmm1"), (0x004D69FD, "cmp word ptr [r8 + rbp + 4], r9w"),
             (0x004D6A1D, "movzx eax, word ptr [r8 + rbp]"), (0x004D6A85, "seta r8b"), (0x004D6ACD, "lea eax, [r9 + 0x20]"),
             (0x004D6AE4, "jne 0x4d6f46"), (0x004D6B14, "mulss xmm0, xmm13"), (0x004D7503, "mulss xmm0, xmm13"),
             (0x004D7914, "addss xmm13, dword ptr [rip"), (0x004D7992, "jmp 0x4d6a61")]:
    expect(a, s)
for a, t, what in [(0x004D63ED, 0x02064BD0, "cell 0x46 whole"), (0x004D6414, 0x02064BE0, "t4"), (0x004D641C, 0x02064BE8, "1 - t4"),
                   (0x004D643C, 0x02064B00, "1/t4"), (0x004D64B2, 0x02064BE4, "1/t4 kept"), (0x004D6579, 0x02064B00, "1/(1 - t4)"),
                   (0x004D689C, 0x02064D10, "cell 0x47 = triples 0..3"), (0x004D6943, 0x02064BDC, "t5 (lane w)"),
                   (0x004D6A0D, 0x02064BCC, "t2 scale"), (0x004D6A15, 0x02064D18, "t2 scaled"), (0x004D6A33, 0x02064DDC, "mode"),
                   (0x004D7411, 0x02064DDC, "mode test"), (0x004D6AEA, 0x02064BE4, "1/t4 into C44"), (0x004D6B2A, 0x02064C44, "C44 = run/t4"),
                   (0x004D6C58, 0x02064C44, "C44 read"), (0x004D6B32, 0x02064B64, "B64"), (0x004D6B4B, 0x02064C74, "C74 = B64 - B34"),
                   (0x004D74B6, 0x02064D10, "triple 0 -> s"), (0x004D74DB, 0x02064D14, "triple 1 -> t"), (0x004D74E3, 0x02064D18, "triple 2 -> s rate"),
                   (0x004D74C6, 0x02064D1C, "triple 3 -> t span"), (0x004D75F1, 0x02064D10, "mode 1 u offset"), (0x004D7628, 0x02064D14, "mode 1 v offset"),
                   (0x004D7914, 0x02064C50, "run step"), (0x004D793F, 0x02064C54, "run"), (0x004D7077, 0x02064BBC, "BBC"),
                   (0x004D707F, 0x02064B8C, "B8C"), (0x004D7087, 0x02064C9C, "C9C = BBC - B8C"), (0x004D737B, 0x02064C9C, "C9C clamp")]:
    check(f"{a:08X} addresses {t:08X} ({what})", riptarget(at(a)) == t, txt(a))
w = [riptarget(at(a)) for a in (0x004D6986, 0x004D69B2, 0x004D69C3, 0x004D69CB, 0x004D69D4, 0x004D69DC, 0x004D69E5, 0x004D69ED, 0x004D69F5)]
check("t5 products go to the w lanes of nine working vectors (B3C..BBC, each +0xC in its cell)",
      sorted(w) == [0x02064B3C, 0x02064B4C, 0x02064B5C, 0x02064B6C, 0x02064B7C, 0x02064B8C, 0x02064B9C, 0x02064BAC, 0x02064BBC], [hex(v) for v in w])
f = lambda a: struct.unpack_from("<f", d, off(a))[0]
check("constants: 01CEBB70 = 0.5 (loaded 004D73C6), 00915618 = 1792, 0091561C = 1824, 008C5B30 = 1/512, 008C5B40 = 255",
      riptarget(at(0x004D73C6)) == 0x01CEBB70 and (f(0x01CEBB70), f(0x00915618), f(0x0091561C), f(0x008C5B30), f(0x008C5B40)) == (0.5, 1792.0, 1824.0, 1 / 512, 255.0)
      and riptarget(at(0x004D75E5)) == 0x00915618 and riptarget(at(0x004D761B)) == 0x0091561C and riptarget(at(0x004D7649)) == 0x008C5B30)
check("004D737B clamps with 255.0 (0x437F0000)", at(0x004D737B) is not None and at(0x004D737B).operands[1].imm == 0x437F0000, txt(0x004D737B))
print("== 0030A190: the world-state gate on the +0x28 word")
for a, s in [(0x0030A1F4, "cmp eax, 0xf1"), (0x0030A201, "add eax, -5"), (0x0030A204, "cmp eax, 1"), (0x0030A207, "ja 0x30a213"),
             (0x0030A209, "word ptr [rbx + 0x28]"), (0x0030A213, "word ptr [rbx + 0x24]")]:
    expect(a, s)
check("0030A1FB reads 022C2160 (the special-sequence state; 5 on screen, 6 ending)", riptarget(at(0x0030A1FB)) == 0x022C2160, txt(0x0030A1FB))
done()
