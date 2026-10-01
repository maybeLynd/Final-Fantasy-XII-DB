"""bc5_final_is_in_place.py - BC-5: `Final` is the in-place text draw, and the composite pass is `ShadowFinal`
(FABLE, Claude Opus 5.5, 2026-09-26). Static reads of the shipping image, plus a disassembly of one embedded shader
through the system d3dcompiler_47.dll.

  F1 the text flush 001E8580 tests the record byte [r12] (+0x2348) at 001E8654 and jumps on ZERO to 001E8F53. That
     arm allocates 0x170 bytes and constructs `Final` (002138C0, vtable 00906EB8) at 001E8F84, and it calls neither the
     target push 0018AFF0 nor the mode setter 001FBD80 before doing so.
  F2 it copies the 4x4 matrix at flush +0xE30..+0xE6F to the stack and calls slot 3 (+0x18) of that object; Final's
     slot 3 is 00214710, which stores the 16 floats to +0x11C..+0x158.
  F3 Final's slot 6 00213B40 reads the matrix (+0x11C, +0x128 ... +0x158) and divides by w (divss) before the
     GS-to-device mapping (subss 2048); the shared slot 6 00213D10 does the mapping and never reads +0x11C.
  F4 Final's slot 11 00214860 passes mode 2 (and 2); the renderer's slot 35 006CAC30 stores the mode at +0x852;
     006C8920 binds +0x140 for mode 2; 006C9CD0 fills +0x140 from the embedded shader 01F38EB8, which disassembles to
     sample / mul_sat / two movs - texture times vertex colour, no PS2 GS-function emulation.
  F5 the other arm (byte non-zero) pushes the target at flush +0x2300 (0018AFF0 with lea rdx,[r14+0x2300]) with mode 1
     (001FBD80(1)), then constructs `ShadowFinal` (00213960) at 001E8A7D; rdi keeps that object (no write to rdi
     between 001E8A87 and the call) until 001E8F49 calls 00214930 with rcx = rdi, and 00214930 has exactly one call site.
  F6 sensitivity: the F4 shader predicate rejects mode 1's program 01F391F4 (vertex RGB with texture alpha).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import ctypes, re, struct, sys
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
def s(x): return ("%s %s" % (x.mnemonic, x.op_str)).strip()
def q(a): return struct.unpack_from("<Q", d, off(a))[0]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

FL = dis(0x1E8580, 0x1E8580 + 0xDF4)
at = {x.address: x for x in FL}
br = at.get(0x1E8659)
arm = [x for x in FL if 0x1E8F53 <= x.address < 0x1E8F89]
calls = [x.op_str for x in arm if x.mnemonic == "call"]
ok1 = (s(at[0x1E8654]) == "cmp byte ptr [r12], 0" and br is not None and br.mnemonic == "je" and br.op_str == "0x1e8f53"
       and "0x2138c0" in calls and "0x18aff0" not in calls and "0x1fbd80" not in calls
       and any(s(x) == "mov edx, 0x170" for x in arm) and q(0x906EB8 + 0) != 0)
check("F1 byte zero -> the in-place arm constructs Final (0x170) with no target push", ok1, "%s; calls %s" % (s(br), calls))
seg = [x for x in FL if 0x1E902F <= x.address <= 0x1E9069]
ok2 = (any("[r14 + 0xe30]" in x.op_str for x in seg) and any("[r14 + 0xe60]" in x.op_str for x in seg)
       and s(at[0x1E9069]) == "call qword ptr [rax + 0x18]" and q(0x906EB8 + 0x18) == 0x214710)
st = [x for x in dis(0x214710, 0x2147A0) if x.mnemonic == "mov" and x.op_str.startswith("dword ptr [rcx + ")]
dst = sorted(int(re.search(r"\+ (0x[0-9a-f]+)\]", x.op_str).group(1), 16) for x in st)
check("F2 the flush's +0xE30 matrix goes to Final's slot 3, which stores +0x11C..+0x158",
      ok2 and dst == list(range(0x11C, 0x15C, 4)), "%d stores" % len(dst))
F6 = dis(0x213B40, 0x213B40 + 0x1CC); P6 = dis(0x213D10, 0x213D10 + 0x110)
reads = {int(m.group(1), 16) for x in F6 for m in [re.search(r"\[rcx \+ (0x1[0-5][0-9a-f])\]", x.op_str)] if m}
div_before = [x.address for x in F6 if x.mnemonic == "divss"]
sub2048 = [x.address for x in F6 if x.mnemonic == "subss" and "rip" in x.op_str]
check("F3 Final's slot 6 applies the matrix with a w divide before the 2048 mapping; the shared slot 6 does not read it",
      {0x11C, 0x128, 0x14C, 0x158} <= reads and div_before and sub2048 and min(div_before) < min(sub2048)
      and not any("0x11c]" in x.op_str for x in P6) and any("subss" == x.mnemonic for x in P6),
      "matrix reads %d, first divss %08X, first subss %08X" % (len(reads), min(div_before), min(sub2048)))
s11 = dis(0x214860, 0x214884)
ok4 = (q(0x906EB8 + 11 * 8) == 0x214860 and any(s(x) == "and r8w, 2" for x in s11)
       and [s(x) for x in dis(0x6CAC30, 0x6CAC3F)] == ["mov byte ptr [rcx + 0x851], dl", "mov word ptr [rcx + 0x852], r8w", "ret"])
b = {x.address: s(x) for x in dis(0x6C8B56, 0x6C8BEF)}
ok4 = ok4 and b.get(0x6C8B62) == "cmp ecx, 1" and b.get(0x6C8B89) == "mov rax, qword ptr [rbx + 0x140]"
cr = dis(0x6C9CD0, 0x6CA200)
fill = [(x.address, x) for x in cr if x.mnemonic == "lea" and "rip" in x.op_str]
blob = None
for i, x in enumerate(cr):
    if s(x) == "lea rsi, [rdi + 0x140]":
        nxt = [y for y in cr[i:i + 6] if y.mnemonic == "lea" and "rip" in y.op_str]
        if nxt: blob = nxt[0].address + nxt[0].size + int(re.search(r"rip \+ (0x[0-9a-f]+)", nxt[0].op_str).group(1), 16)
def ps_ops(bl):
    """opcode list of an embedded DXBC pixel shader, through the system d3dcompiler_47.dll."""
    if not bl or d[off(bl):off(bl) + 4] != b"DXBC": return None
    try:
        dc = ctypes.WinDLL("d3dcompiler_47.dll")
    except OSError:
        return None
    dc.D3DDisassemble.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint, ctypes.c_char_p, ctypes.POINTER(ctypes.c_void_p)]
    size = struct.unpack_from("<I", d, off(bl) + 24)[0]; out = ctypes.c_void_p()
    if dc.D3DDisassemble(d[off(bl):off(bl) + size], size, 0, None, ctypes.byref(out)) != 0: return None
    vt = ctypes.cast(out, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
    gp = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(vt[3]); gs = ctypes.WINFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p)(vt[4])
    t = ctypes.string_at(gp(out), gs(out)).decode("latin-1").replace(chr(0), "")
    return [l.split()[0] for l in t.splitlines() if l.strip() and not l.startswith("//") and not l.startswith("dcl_") and l.strip() != "ps_5_0"]
MODULATE = ["sample_indexable(texture2d)(float,float,float,float)", "mul_sat", "mov", "mov", "ret"]
ops = ps_ops(blob)
check("F4 Final's mode 2 binds +0x140 = shader 01F38EB8: texture times vertex colour, nothing else",
      ok4 and blob == 0x1F38EB8 and ops == MODULATE,
      "blob %s; %s" % ("%08X" % blob if blob else None, ops))
arm2 = [x for x in FL if 0x1E8A21 <= x.address <= 0x1E8A7D]
pre = [s(x) for x in FL if 0x1E8A10 <= x.address < 0x1E8A7D]
wr = [x for x in FL if 0x1E8A88 <= x.address < 0x1E8F49 and x.op_str.split(",")[0].strip() in ("rdi", "edi")
      and x.mnemonic not in ("cmp", "test", "push")]
sites = []
vs, va, rs, ro = secs[0]
k = d.find(b"\xE8", ro)
while 0 <= k < ro + rs - 5:
    a = BASE + va + k - ro
    if a + 5 + struct.unpack_from("<i", d, k + 1)[0] == 0x214930 and a in at: sites.append(a)
    k = d.find(b"\xE8", k + 1)
check("F5 the other arm pushes the +0x2300 target (mode 1), builds ShadowFinal, and composites through it",
      "lea rdx, [r14 + 0x2300]" in pre and "call 0x18aff0" in pre and "mov ecx, 1" in pre and "call 0x1fbd80" in pre
      and s(at[0x1E8A7D]) == "call 0x213960" and not wr and s(at[0x1E8F46]) == "mov rcx, rdi"
      and s(at[0x1E8F49]) == "call 0x214930" and sites == [0x1E8F49],
      "rdi writes between %d; 00214930 E8 sites %s" % (len(wr), ["%08X" % x for x in sites]))
ops1 = ps_ops(0x1F391F4)
check("F6 sensitivity: the F4 predicate rejects mode 1's shader 01F391F4 (+0x148), so it can tell the programs apart",
      ops1 is not None and ops1 != MODULATE, repr(ops1))
print("FAILS", fails)
sys.exit(1 if fails else 0)
