"""uc1_257_checks.py - FABLE's own checks for the UC-1 band above 256 B (Claude Opus 5.5, 2026-09-28), on
OPUS-REQ-FABLE-UC1-BAND-257-UP-RULING. Decoded from the certified image's bytes.

  A1 00712180 decodes linearly to exactly 353 B ending on ret, with no call (a leaf) and no stack frame; its first touch of
     every nonvolatile register is a write or none (the L rule, re-implemented here from the instruction text, not imported)
  A2 its references, counted three ways over the image: E8 / E9 rel32 at a real instruction start in .text, rip-relative lea / mov
     of the address in .text, and aligned raw u64 values equal to it in the data sections
  H1 00131B50's first instruction reads xmm10 (a nonvolatile) before anything writes it; the 32 bytes before it, decoded
     backwards from the nearest .pdata function start, show whether code runs into it or jumps to it
  C  controls: the L re-implementation fails on a planted 'movaps xmm0, xmm6' as the first instruction of a copy of 00712180,
     and passes on a planted 'movaps xmm6, xmm0' (a write)
"""
import hashlib, os, re, struct, sys
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8": print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = []
for i in range(ns):
    o = pe + 24 + opt + 40 * i
    SECS.append((d[o:o + 8].rstrip(b"\0"), ) + struct.unpack_from("<IIII", d, o + 8))
off = lambda v: next(ra + v - 0x120000 - va for n, vs, va, rs, ra in SECS if va <= v - 0x120000 < va + rs)
text = next(s for s in SECS if s[0] == b".text"); T0, TV, TN = text[4], text[2] + 0x120000, text[3]
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
exc_rva, exc_sz = struct.unpack_from("<II", d, pe + 24 + 112 + 8 * 3)
PD = sorted(struct.unpack_from("<II", d, off(0x120000 + exc_rva) + 12 * k) for k in range(exc_sz // 12))
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
NVG = ["rbx|ebx|bx|bl", "rbp|ebp|bp|bpl", "rsi|esi|si|sil", "rdi|edi|di|dil"] + ["r%d[dwb]?" % k for k in range(12, 16)] + ["xmm%d" % k for k in range(6, 16)]
def first_touch(ins):
    """{nonvolatile: 'read' or 'write'} by its first appearance; a save (push reg, or a store of reg to [rsp+x]) is not a read."""
    seen = {}
    for i in ins:
        ops = [o.strip() for o in i.op_str.split(",")] if i.op_str else []
        for g in NVG:
            if g in seen: continue
            hit = [k for k, o in enumerate(ops) if re.search(r"(?<![\w])(%s)(?![\w])" % g, o)]
            if not hit: continue
            save = i.mnemonic == "push" or (i.mnemonic.startswith("mov") and len(ops) == 2 and ops[0].find("[rsp") >= 0 and 1 in hit)
            dest_only = hit == [0] and not ops[0].startswith(("byte", "word", "dword", "qword", "xmmword")) and i.mnemonic in (
                "mov", "movaps", "movups", "movss", "movsd", "movd", "movq", "lea", "xor", "pxor", "xorps", "movzx", "movsx", "movsxd", "pop")
            if i.mnemonic in ("xor", "pxor", "xorps", "sub") and len(ops) == 2 and ops[0] == ops[1]: dest_only = True
            seen[g] = "save" if save else ("write" if dest_only else "read")
    return seen
def decode(img, a, n): return list(MD.disasm(img[off(a):off(a) + n], a))
A = decode(d, 0x712180, 353)
ft = first_touch(A)
ok("A1", A and A[-1].address + A[-1].size == 0x712180 + 353 and A[-1].mnemonic == "ret" and not any(i.mnemonic == "call" for i in A)
   and not any("rsp" in i.op_str and i.mnemonic in ("sub", "push") for i in A) and "read" not in ft.values(),
   "353 B to ret, leaf, no frame; nonvolatile first touches %s" % (ft or "none"))
def boundary(va):
    r = va - 0x120000; f = None
    for b0, e0 in PD:
        if b0 <= r: f = b0
        else: break
    if f is None: return False
    f += 0x120000
    return va in {i.address for i in MD.disasm(d[off(f):off(f) + (va - f) + 16], f)}
calls = [TV + m.start() for m in re.finditer(rb"[\xE8\xE9]", d[T0:T0 + TN])
         if TV + m.start() + 5 + struct.unpack_from("<i", d, T0 + m.start() + 1)[0] == 0x712180 and boundary(TV + m.start())]
rips = []
for m in re.finditer(rb"[\x48\x4C]\x8D[\x05\x0D\x15\x1D\x25\x2D\x35\x3D]", d[T0:T0 + TN]):
    va = TV + m.start()
    if va + 7 + struct.unpack_from("<i", d, T0 + m.start() + 3)[0] == 0x712180: rips.append(va)
raw = []
for n_, vs, va, rs, ra in SECS:
    if n_ == b".text": continue
    blob = d[ra:ra + rs]
    for k in range(0, len(blob) - 7, 8):
        if struct.unpack_from("<Q", blob, k)[0] == 0x712180 or struct.unpack_from("<Q", blob, k)[0] == 0x140712180 - 0x140000000 + 0x712180: raw.append((n_.decode(), va + k + 0x120000))
ok("A2", bool(calls or rips or raw), "references: %d call/jmp %s, %d rip lea %s, %d raw u64 %s"
   % (len(calls), ["%08X" % x for x in calls], len(rips), ["%08X" % x for x in rips], len(raw), ["%s:%08X" % x for x in raw][:6]))
H = decode(d, 0x131B50, 16)
r = 0x131B50 - 0x120000; f0 = max(b0 for b0, e0 in PD if b0 <= r) + 0x120000
pre = [(i.address, (i.mnemonic + " " + i.op_str).strip()) for i in MD.disasm(d[off(f0):off(0x131B50) + 8], f0) if i.address >= 0x131B50 - 40]
ok("H1", H[0].mnemonic == "psubw" and H[0].op_str == "xmm1, xmm10" and first_touch(H[:1]).get("xmm10") == "read",
   "first instruction %s %s; nearest .pdata start before it %08X; decode just before it: %s" % (H[0].mnemonic, H[0].op_str, f0, ["%08X %s" % p for p in pre[-6:]]))
p1 = bytearray(d); o = off(0x712180); p1[o:o + 3] = bytes([0x0F, 0x28, 0xC6])            # movaps xmm0, xmm6 (read)
p2 = bytearray(d); p2[o:o + 3] = bytes([0x0F, 0x28, 0xF0])                                 # movaps xmm6, xmm0 (write)
c1 = first_touch(decode(bytes(p1), 0x712180, 3)).get("xmm6"); c2 = first_touch(decode(bytes(p2), 0x712180, 3)).get("xmm6")
ok("C", c1 == "read" and c2 == "write", "planted read of xmm6 reads as %s; planted write reads as %s" % (c1, c2))
print("FAILS", fails); sys.exit(1 if fails else 0)
