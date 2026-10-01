#!/usr/bin/env python3
"""gi3_dialog_reply_and_wheel_layers.py - GI-3 (FABLE 2026-09-29): message 285 (0x11D) is the shared dialogs' reply
{0x11D, code the opener passed, answer}; 0055CD40 routes code-0xA through the 18-slot table 0055DB88; the board opens
codes 0xA-0xF, 0x1A, 0x1B (message box) and 5-8, 0x1C (Yes/No box, out of range -> 0055D978); texts resolved from the
shipped us tables. The three draw children belong to the board chooser 00557DB0 (backdrop / emblems / faces).
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
print("== 1. the 18-slot table of 0055CD40's id-285 arm")
for a, s in [(0x0055CD53, "cmp eax, 0x11d"), (0x0055D84B, "mov rax, qword ptr [rdx + 8]"), (0x0055D84F, "add rax, -0xa"),
             (0x0055D853, "cmp rax, 0x11"), (0x0055D857, "ja 0x55d978")]:
    expect(a, s)
EXP = {0xA: 0x55DB10, 0xB: 0x55D870, 0xC: 0x55D93B, 0xD: 0x55D925, 0xE: 0x55D95B, 0xF: 0x55D95B, 0x1A: 0x55D8D8, 0x1B: 0x55D906}
EXP.update({c: 0x55D978 for c in range(0x10, 0x1A)})
tab = rel32_table(0x0055DB88, 18)
check("slots 0xA..0x1B decode to the published arms", {0xA + i: t for i, t in enumerate(tab)} == EXP, [hex(t) for t in tab])
print("== 2. who sends 0x11D (immediate stores image-wide; controls: the two dialog replies)")
st = sweep(lambda x: x.mnemonic == "mov" and x.op_str.endswith(", 0x11d") and "ptr [rsp" in x.op_str)
for a, f, t in st: print(f"   {a:08X} in {f:08X}  {t}")
check("0x11D is stored into a message record only by 002C2320, 002CDF20, 002CE370", sorted(f for a, f, t in st) == [0x002C2320, 0x002CDF20, 0x002CE370])
for a, s in [(0x002CE33D, "lea rdx, [rip + 0x2c]"), (0x002CE4BB, "mov qword ptr [rbp + 0xc8], rcx"), (0x002CE4C5, "mov dword ptr [rbp + 0xd0], eax"),
             (0x002CE40E, "mov qword ptr [rsp + 0x28], rax"), (0x002CE437, "mov qword ptr [rsp + 0x30], 0xfffffffffffffffe"),
             (0x002CDEED, "lea rdx, [rip + 0x2c]"), (0x002CE093, "mov edx, 0x8100"), (0x002CE09F, "mov ecx, 0x3e8"),
             (0x002CE0A9, "mov edx, 0x8101"), (0x002CE0AE, "mov ecx, 0x3e9"), (0x002CE15B, "mov dword ptr [rbx + 0xd4], 2"),
             (0x002CE165, "mov qword ptr [rsp + 0x38], 1")]:
    expect(a, s)
check("Yes/No option texts are 'Yes' / 'No'", (text(0x3E8), text(0x3E9)) == ("Yes", "No"))
print("== 3. message-box code -> text (table 002CE728, 28 slots) and the board's texts")
arms = rel32_table(0x002CE728, 0x1C)
def arm_text(code):
    for x in ins_of(0x002CE370):
        if x.address >= arms[code] and x.mnemonic == "mov" and x.op_str.startswith("esi, 0x"): return int(x.op_str.split(", ")[1], 16)
        if x.address >= arms[code] and x.mnemonic == "jmp": break
TX = {0xA: (0xCD9, "Insufficient license points"), 0xB: (0x426B, "Esper"), 0xC: (0x426C, "new Mist ability"),
      0xD: (0x4268, "Only one character can obtain this license"), 0xE: (0x4269, "summon Espers"), 0xF: (0x426A, "quickenings"),
      0x18: (0x836, "twelve boards"), 0x1A: (0x428A, "Second Board license has been added"), 0x1B: (0x88C, "Second Board")}
for code, (tid, sub) in TX.items():
    got = arm_text(code); s = text(got) if got else ""
    check(f"message code {code:#x} -> text {tid:#x} containing '{sub}'", got == tid and sub in s, f"{got and hex(got)}: {s[:70]}")
print("== 4. the board's opener sites (code in edx before the call)")
OPEN = [(0x0055D709, 0x0055D711, "002CE2F0", 0xA), (0x0055EC58, None, "002CE2F0", 0xB), (0x0055F557, 0x0055F566, "002CE2F0", 0xC),
        (0x0055EC9F, 0x0055ECA7, "002CE2F0", 0xD), (0x0055F5B0, None, "002CE2F0", 0xE), (0x0055F5D6, None, "002CE2F0", 0xF),
        (0x0055ECEA, None, "002CE2F0", 0x1A), (0x0055ECF8, 0x0055ECFD, "002CE2F0", 0x1B), (0x00557F1B, 0x00557F23, "002CE2F0", 0x18),
        (0x00558460, 0x00558468, "002CDEA0", 0x19), (0x005584BE, 0x005584C6, "002CDEA0", 0x19)]
for a, call, tgt, code in OPEN:
    expect(a, f"mov edx, {code:#x}")
    if call: expect(call, f"call 0x{int(tgt, 16):x}")
for a, s in [(0x0055D749, "mov ebx, 6"), (0x0055D754, "mov ebx, 7"), (0x0055D75F, "mov ebx, 8"), (0x0055D76A, "mov ebx, 5"),
             (0x0055D76F, "mov eax, 0x1c"), (0x0055D77C, "call 0x2cdea0"), (0x0055D983, "mov ecx, dword ptr [rcx + 0x160]"),
             (0x0055D978, "cmp qword ptr [rdx + 0x10], 1"), (0x0055DA6E, "call 0x3235c0")]:
    expect(a, s)
CONF = {5: (0x860, "Obtain"), 6: (0x861, "Only one character can obtain this license"), 7: (0x863, "three quickening"),
        8: (0x864, "for this Esper"), 0x1C: (0x88D, "unable to return to the"), 0x19: (0x835, "Choose this license board")}
for code, (tid, sub) in CONF.items():
    check(f"Yes/No code {code:#x} -> text {tid:#x} '{sub}'", sub in text(tid), text(tid)[:70])
for a, s in [(0x002CDFF8, "mov ecx, 0x860"), (0x002CE02A, "mov ecx, 0x861"), (0x002CE023, "mov ecx, 0x863"), (0x002CE01C, "mov ecx, 0x864"),
             (0x002CE00E, "mov ecx, 0x88d"), (0x002CDFFF, "mov ecx, 0x835")]:
    expect(a, s)
ce = sorted(f for s, f in raw_callers(0x002CE2F0)); cd = sorted(f for s, f in raw_callers(0x002CDEA0))
check("002CE2F0 raw callers (control: 0055CD40, 0055E9E0, 0055F3E0, 00557DB0 among them)", {0x0055CD40, 0x0055E9E0, 0x0055F3E0, 0x00557DB0} <= set(ce), [hex(x) for x in ce])
check("002CDEA0 raw callers are 00557DB0 (x2) and 0055CD40", cd == [0x00557DB0, 0x00557DB0, 0x0055CD40], [hex(x) for x in cd])
print("== 5. the draw children belong to 00557DB0")
for inst, proc, site in [(0x00557370, 0x00557760, 0x005581AC), (0x005572B0, 0x005565E0, 0x005581BC), (0x00557430, 0x0055A340, 0x005581CA), (0x005571F0, 0x005569F0, 0x005581D7)]:
    c = raw_callers(inst)
    check(f"{inst:08X} (installs {proc:08X}) is called once, at {site:08X} in 00557DB0", c == [(site, 0x00557DB0)], c)
    leas = [x for x in ins_of(inst) if x.mnemonic == "lea" and riptarget(x) == proc]
    check(f"{inst:08X} leas {proc:08X}", len(leas) == 1)
check("00557DB0 is installed by 00557AE0, called from 00558FB0", raw_callers(0x00557AE0) == [(0x0055937C, 0x00558FB0)])
print("== 6. art sources: root texture names -> root slots -> 00557DB0 +0x140/+0x148/+0x150 -> children")
def cstr(a): o = off(a); return d[o:d.index(b"\0", o)].decode()
for lea, name, store in [(0x00561679, "lic_bk", 0x005616A8), (0x0056170F, "lic_8_c2", 0x00561738), (0x0056173F, "lic_8_c3", 0x00561765)]:
    check(f"{lea:08X} names '{name}'", cstr(riptarget(at(lea))) == name)
expect(0x005616A8, "mov qword ptr [rsi + 0x100], rax"); expect(0x00561738, "mov qword ptr [rsi + 0xf0], rax"); expect(0x00561765, "mov qword ptr [rsi + 0xf8], rax")
for a, s in [(0x00557FFE, "mov rcx, qword ptr [rax + 0xf0]"), (0x00558005, "mov qword ptr [rbp + 0x140], rcx"),
             (0x00558013, "mov rcx, qword ptr [rax + 0xf8]"), (0x0055801A, "mov qword ptr [rbp + 0x148], rcx"),
             (0x00558028, "mov rcx, qword ptr [rax + 0x100]"), (0x0055802F, "mov qword ptr [rbp + 0x150], rcx"),
             (0x005579D2, "mov rax, qword ptr [rdx + 0x140]"), (0x005579E0, "mov rax, qword ptr [rdx + 0x148]"),
             (0x00556986, "mov rax, qword ptr [rdx + 0x150]"), (0x0055A796, "mov rax, qword ptr [rdx + 0x148]")]:
    expect(a, s)
print("== 7. what each id-4 arm draws")
for a, s in [(0x00556695, "lea r15d, [rbp + 0x5a]"), (0x005568DB, "add r15d, 0x1e"), (0x005568EB, "cmp r15d, 0x1c2"),
             (0x00556763, "test dword ptr [rax + 0x364], r14d"), (0x005580AE, "or dword ptr [rbp + 0x364], eax"),
             (0x005575CB, "mov dword ptr [rbp - 0x30], 4"), (0x00557684, "mov dword ptr [rbp - 0x30], 5"),
             (0x005576D8, "mov dword ptr [rbp - 0x30], 6"), (0x00557721, "mov dword ptr [rbp - 0x30], 7"),
             (0x005575A6, "mov dword ptr [rbx + 0x90], 0x50000000"), (0x0055A3F7, "mov r12d, 0xc"), (0x0055A3E0, "lea rsi, [rdx + 0x190]"),
             (0x0055A5C2, "mov eax, 0x55555556"), (0x0055A5C7, "imul r15d"), (0x005587F9, "add rcx, 0x16c"),
             (0x0055661C, "mov rax, qword ptr [rsi + 0xd8]"), (0x0055A385, "mov rax, qword ptr [rbx + 0xd8]")]:
    expect(a, s)
check("005566A9 and 0055A3CC read LicenseBoardBallLength (01F2CAD8); 0055A3D2 FaceLength (01F2CADC); 0055A5E6 BallFaceSecondOffsetY (01F2CAE8)",
      riptarget(at(0x005566A9)) == 0x01F2CAD8 and riptarget(at(0x0055A3CC)) == 0x01F2CAD8 and riptarget(at(0x0055A3D2)) == 0x01F2CADC and riptarget(at(0x0055A5E6)) == 0x01F2CAE8)
print("== regression: the old readings")
check("REJECTS '285 = node-select / confirm / LP spend vocabulary': 17 of 18 slots are dialog-close arms and 0x11D has only dialog senders",
      sorted(set(f for a, f, t in st)) == [0x002C2320, 0x002CDF20, 0x002CE370])
check("REJECTS 'BallFaceSecondOffsetY = per-second hand': it is multiplied by index/3 (0x55555556)", "0x55555556" in txt(0x0055A5C2))
done()
