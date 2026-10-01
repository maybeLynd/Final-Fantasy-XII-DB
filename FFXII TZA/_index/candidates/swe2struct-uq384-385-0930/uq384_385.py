"""uq384_385.py - UQ-384 and UQ-385 (SWE2-STRUCT for OPUS, 2026-09-30). Static only, certified image via retool.

UQ-384  (a) What object is stored at [01FC35F8], by its writer, its constructor and its vtable (RTTI), and which of its
            methods the GS replay calls.  Steps R0-R13, D1-D3.
        (b) What the GS state handlers store. Both dispatchers' jump tables are decoded from the bytes and every arm's
            stores are read.  Steps H1-H6.
UQ-385  For each of the 19 caller-less VU-state touchers: is it a VU JAL/JR sub-program target, a data-referenced entry,
        or neither?  Steps V1-V9.

Controls (each census has at least one positive control):
  K1  the rip-write census sees a multi-writer global (01FC3603) with all its writers.
  K2  the byte-level rel32 sweep finds the known call 001DB4AC -> 00210320 and the known store 0021037B -> 01FC35F8.
  K3  the data sweep finds the vtable qword 009007F0 = 001DB3D0 and the jump-table RVA 0060AAD0 -> 0060A899.
  K4  the reader census finds the known readers of TEX0_1 (01FC3588): 0020EB60 and 0020ED30.
  K5  the rel8 sweep finds the known short branch 0021047D -> 00210495.
  K6  the slice that ties a lea to a registrar argument REJECTS a lea that is not one (0020F420 lea r14 -> image base).
  K7  the direct-branch sweep finds the E8 caller of a known sub-program (0047BFB0, 'called only from microprograms').
  K8  the base-relocation census contains the vtable slot 009007F0.
"""
import collections, hashlib, json, os, struct, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DBROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))           # .../Database
KIT = os.path.join(DBROOT, "Tools", "analysis-kit", "gfz-scripts")
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
import pefile  # noqa: E402

R = T.R
SZ = T.sizes()
SC = T.scan()
MD = R.md
RIP, MEM, IMM, REG = 41, 3, 2, 1
CERT = "73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8"
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a):
    return next(MD.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, " ".join(i.op_str.split()))).strip()


def pins(pairs):
    bad = [("%08X" % a, txt(a), s) for a, s in pairs if txt(a) != s]
    return not bad, bad


def body(f):
    return list(MD.disasm(R.at(f, SZ[f]), f))


def q(a):
    return struct.unpack("<Q", R.at(a, 8))[0]


def u32(a):
    return struct.unpack("<I", R.at(a, 4))[0]


def i32(a):
    return struct.unpack("<i", R.at(a, 4))[0]


def slot(vt, k):
    return q(vt + 8 * k)


def nslots(vt):
    n = 0
    while slot(vt, n) in SZ:
        if n and T.rtti_class(vt + 8 * n):
            break
        n += 1
    return n


def rip_target(i):
    for op in i.operands:
        if op.type == MEM and op.mem.base == RIP:
            return i.address + i.size + op.mem.disp
    return None


FAMS = {}
for big, rest in {
        "rax": "eax ax al ah", "rbx": "ebx bx bl bh", "rcx": "ecx cx cl ch", "rdx": "edx dx dl dh",
        "rsi": "esi si sil", "rdi": "edi di dil", "rbp": "ebp bp bpl", "rsp": "esp sp spl"}.items():
    for n in [big] + rest.split():
        FAMS[n] = big
for k in range(8, 16):
    for n in ("r%d" % k, "r%dd" % k, "r%dw" % k, "r%db" % k):
        FAMS[n] = "r%d" % k
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}


def canon(name):
    return FAMS.get(name, name)


def writes(i, fam):
    _, w = i.regs_access()
    return any(canon(i.reg_name(r)) == fam for r in w)


def no_write(f, lo, hi, fam):
    """No instruction of f with lo <= address < hi writes register family fam."""
    return [("%08X" % i.address, i.mnemonic, i.op_str) for i in body(f) if lo <= i.address < hi and writes(i, fam)]


# ------------------------------------------------------------------------------------------------------------------
# image
# ------------------------------------------------------------------------------------------------------------------
PE = pefile.PE(R.b.EXE)
BASE = PE.OPTIONAL_HEADER.ImageBase
SECS = []
for s in PE.sections:
    SECS.append((s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, s.get_data(), s.SizeOfRawData,
                 s.Misc_VirtualSize, bool(s.Characteristics & 0x20000000)))
TEXT = [x for x in SECS if x[0] == ".text"][0]
PDATA = [x for x in SECS if x[0] == ".pdata"][0]


def section_of(a):
    for nm, va, data, raw, vsz, ex in SECS:
        if va <= a < va + max(raw, vsz):
            return nm, a - va < raw
    return None, None


def data_sweep(values, width):
    """Every (section, address, value) where a little-endian `width`-byte word at ANY alignment equals one of values."""
    vals = np.array(sorted(values), dtype="<u8" if width == 8 else "<u4")
    out = []
    for nm, va, data, raw, vsz, ex in SECS:
        for k in range(width):
            n = (len(data) - k) // width
            if n <= 0:
                continue
            a = np.frombuffer(data, dtype="<u8" if width == 8 else "<u4", count=n, offset=k)
            for j in np.nonzero(np.isin(a, vals))[0]:
                out.append((nm, va + k + width * int(j), int(a[j])))
    return out


def rel32_sweep(lo, hi, ends=(4, 5, 6, 8)):
    """Byte-level: every 4-byte field in .text that, read as a rel32/rip displacement ending `e` bytes after its start,
    points into [lo, hi). Returns candidate (field_va, end, target)."""
    nm, va, data, raw, vsz, ex = TEXT
    out = []
    for k in range(4):
        n = (len(data) - k) // 4
        a = np.frombuffer(data, dtype="<i4", count=n, offset=k).astype(np.int64)
        pos = va + k + 4 * np.arange(n, dtype=np.int64)
        for e in ends:
            tgt = pos + e + a
            for j in np.nonzero((tgt >= lo) & (tgt < hi))[0]:
                out.append((int(pos[j]), e, int(tgt[j])))
    return out


def decode_field(fva, e, tgt):
    """Find a real instruction that ends at fva + e and whose rip operand or branch immediate is tgt (or covers it).
    Every start is tried and the first decode that lies on its function's own instruction stream is returned, so a
    prefix-less decode one byte late (e.g. 'mov dword' inside 'mov qword') is never taken for the instruction."""
    for i in _decode_candidates(fva, e, tgt):
        if in_stream(i)[0]:
            return i
    return None


def _decode_candidates(fva, e, tgt):
    for back in range(1, 12):
        s = fva - back
        try:
            i = next(MD.disasm(R.at(s, 16), s, 1))
        except StopIteration:
            continue
        if s + i.size != fva + e:
            continue
        hit = False
        for op in i.operands:
            if op.type == MEM and op.mem.base == RIP:
                g = i.address + i.size + op.mem.disp
                if g <= tgt < g + max(op.size, 1):
                    hit = True
            if op.type == IMM and op.imm == tgt and (i.mnemonic == "call" or i.mnemonic.startswith("j")):
                hit = True
        if hit:
            yield i


_STREAM = {}


def in_stream(i):
    """True when i is an instruction of the linear disassembly of its listed function (not a mid-instruction decode)."""
    f = T.func_of(i.address, SZ)
    if f is None:
        return False, None
    if f not in _STREAM:
        _STREAM[f] = {x.address for x in body(f)}
    return i.address in _STREAM[f], f


def real_refs(lo, hi):
    """Decoded, in-stream instructions whose rip operand (or branch target) falls in [lo, hi)."""
    out = []
    seen = set()
    for fva, e, tgt in rel32_sweep(lo, hi):
        i = decode_field(fva, e, tgt)
        if i is None or i.address in seen:
            continue
        seen.add(i.address)
        out.append((in_stream(i)[1], i))
    return out


def kind(i):
    if i.mnemonic in ("call", "jmp") or i.mnemonic.startswith("j"):
        return "branch"
    if i.mnemonic == "lea":
        return "lea"
    for k, op in enumerate(i.operands):
        if op.type == MEM and op.mem.base == RIP:
            if k == 0 and i.mnemonic not in ("cmp", "test", "push", "ucomiss", "comiss", "bt"):
                return "W"
            return "R"
    return "?"


print("=== image ===")
sha = hashlib.sha256(open(R.b.EXE, "rb").read()).hexdigest().upper()
check("R0", sha == CERT and BASE == 0x120000,
      "the image read is the certified shipping EXE (sha256 %s..., image base %08X)" % (sha[:16], BASE))

# ==================================================================================================================
# UQ-384 (a): the object at [01FC35F8]
# ==================================================================================================================
print("=== UQ-384 (a): the object stored at 01FC35F8 ===")
G = 0x01FC35F8
DEVICE = 0x02CC0410 + 0x18C0

# R1 writer census, three independent forms
def real_pointer(hit):
    """A data-sweep hit counts as a pointer when it lies outside .text, or, inside .text, when the in-stream instruction
    containing it uses the value as an immediate or as an absolute (base-less) displacement. A rip displacement or
    other encoding bytes that happen to spell the value are not a pointer."""
    nm, a, v = hit
    if nm != ".text":
        return True
    for back in range(0, 15):
        s = a - back
        i = next(MD.disasm(R.at(s, 16), s, 1), None)
        if i is None or not (s <= a < s + i.size) or not in_stream(i)[0]:
            continue
        return any((op.type == IMM and op.imm == v) or (op.type == MEM and op.mem.base == 0 and op.mem.disp == v)
                   for op in i.operands)
    return True                                     # not on any listed stream: keep it, it is reported


def overlaps(i, lo, hi):
    for op in i.operands:
        if op.type == MEM and op.mem.base == RIP:
            g = i.address + i.size + op.mem.disp
            if g < hi and lo < g + max(op.size, 1):
                return True
    return False


w_rip = sorted((f, a) for f, a, k in SC["refs"].get(G, ()) if k == "W")
byte_refs = [(f, i) for f, i in real_refs(G - 15, G + 8) if overlaps(i, G, G + 8)]
byte_w = sorted((f, i.address) for f, i in byte_refs if kind(i) == "W")
byte_r = sorted((f, i.address) for f, i in byte_refs if kind(i) == "R")
raw_ptrs = data_sweep(range(0x01FC3580, 0x01FC3620), 8) + data_sweep(range(0x01FC3580, 0x01FC3620), 4)
ptrs = [x for x in raw_ptrs if real_pointer(x)]
rva_lo, rva_hi = 0x01FC3580 - BASE, 0x01FC3620 - BASE
ibr = [x for x in data_sweep(range(rva_lo, rva_hi), 4) if x[0] == ".text"]
ibr_real = []
for nm, a, v in ibr:
    for back in range(1, 12):
        s = a - back
        try:
            i = next(MD.disasm(R.at(s, 16), s, 1))
        except StopIteration:
            continue
        if s < a < s + i.size and any(op.type == MEM and op.mem.disp == v for op in i.operands):
            ok, f = in_stream(i)
            if ok:
                ibr_real.append((f, i.address))
leas_near = sorted((g, f, a) for g in range(0x01FC3480, 0x01FC3620) for f, a, k in SC["refs"].get(g, ()) if k == "lea")
check("R1", w_rip == [(0x00210320, 0x0021037B)] and byte_w == [(0x00210320, 0x0021037B)] and not ptrs
      and not ibr_real and not leas_near,
      ("01FC35F8 has exactly one writer, 0021037B in 00210320: rip census %s; byte-level rel32 sweep writers %s "
       "(readers %d); no data pointer into 01FC3580-01FC361F (%d; %d byte runs inside rip-relative encodings "
       "dismissed); no image-base-relative operand (%d); no lea of 01FC3480-01FC361F (%d)")
      % (["%08X" % a for f, a in w_rip], ["%08X" % a for f, a in byte_w], len(byte_r), len(ptrs),
         len(raw_ptrs) - len(ptrs), len(ibr_real), len(leas_near))
      + (" %s" % [(n, "%08X" % a, "%08X" % v) for n, a, v in ptrs] if ptrs else ""))
w3603 = sorted(a for f, a, k in SC["refs"].get(0x01FC3603, ()) if k == "W")
check("K1", len(w3603) >= 5 and 0x00210447 in w3603 and 0x0020FCD6 in w3603,
      "control: the same rip-write census sees all %d writers of 01FC3603 (incl. 00210447, 0020FCD6)" % len(w3603))
check("K2", any(i.address == 0x0021037B for f, i in byte_refs)
      and any(i.address == 0x001DB4AC for f, i in real_refs(0x00210320, 0x00210321)),
      "control: the byte-level sweep finds the store 0021037B -> 01FC35F8 and the call 001DB4AC -> 00210320")

# R2 00210320 stores its incoming rdx; its only caller is 001DB3D0
ok, bad = pins([(0x0021037B, "mov qword ptr [rip + 0x1db3276], rdx"), (0x00210330, "mov r14, rdx")])
nw = no_write(0x00210320, 0x00210320, 0x0021037B, "rdx")
callers = sorted(SC["calls"].get(0x00210320, ()))
cb = real_refs(0x00210320, 0x00210321)
q210 = data_sweep([0x00210320], 8) + [x for x in data_sweep([0x00210320], 4) if x[0] not in (".pdata",)]
check("R2", ok and not nw and callers == [(0x001DB3D0, 0x001DB4AC)] and [i.address for f, i in cb] == [0x001DB4AC]
      and not q210,
      "00210320 stores its second argument rdx, unmodified since entry (%s), and its only caller is 001DB4AC in "
      "001DB3D0 (byte sweep %s; no qword/dword names it %s) %s" % (nw or "no write", ["%08X" % i.address for f, i in cb],
                                                                 q210 or "", bad or ""))

# R3 001DB3D0 forwards its own rdx; it is GiVmax slot 1 and is reached only through that slot
ok, bad = pins([(0x001DB3F6, "mov rsi, rdx"), (0x001DB49D, "mov rdx, rsi"), (0x001DB4AC, "call 0x210320")])
nw1 = no_write(0x001DB3D0, 0x001DB3D0, 0x001DB3F6, "rdx")
nw2 = no_write(0x001DB3D0, 0x001DB3F7, 0x001DB4B1, "rsi")
gv = 0x009007E8
qs = T.qword_sites(0x001DB3D0)
check("R3", ok and not nw1 and not nw2 and T.rtti_class(gv) == "GiVmax" and slot(gv, 0) == 0x001DB550
      and slot(gv, 1) == 0x001DB3D0 and qs == [0x009007F0] and not SC["calls"].get(0x001DB3D0)
      and not SC["refs"].get(0x001DB3D0),
      "001DB3D0 passes its own rdx (rsi, not rewritten 001DB3F7-001DB4B0) to every 00210320 call; it is GiVmax "
      "(vtable %08X, RTTI) slot 1, named only by the qword 009007F0, with no direct caller and no rip reference %s"
      % (gv, bad or ""))

# R4 GiVmax constructor
lv = sorted((f, a) for f, a, k in SC["refs"].get(gv, ()) if k == "lea")
ok, bad = pins([(0x001DB22F, "lea rax, [rip + 0x7255b2]")])
check("R4", ok and lv == [(0x001DB220, 0x001DB22F)]
      and sorted(SC["calls"].get(0x001DB220, ())) == [(0x001DB7E0, 0x001DB813), (0x001DB840, 0x001DB88A)],
      "GiVmax's vtable is installed only by 001DB220, whose callers are 001DB840 (registrar build) and 001DB7E0 "
      "(effect-element build) %s" % (bad or ""))

# R5 submission: 0020E630 -> 001FB810 -> 001A17F0 -> [[01F7F4D0]+8] slot 0 = GeometryRenderTargetImmediate 001F48B0
ok, bad = pins([(0x001FB813, "mov rdx, qword ptr [rcx]"), (0x001FB816, "mov rcx, qword ptr [rip + 0x1d83cb3]"),
                (0x001FB81D, "jmp 0x1a17f0"), (0x001A182A, "mov rcx, qword ptr [rdi + 8]"),
                (0x001A1831, "mov rdx, rbp"), (0x001A184B, "jmp qword ptr [rax]"),
                (0x0017D51F, "mov ecx, 0x10"), (0x0017D538, "call 0x1a17d0"),
                (0x0017D547, "mov qword ptr [rip + 0x1e01f82], rax"),
                (0x001A17D0, "lea rax, [rip + 0x754751]"), (0x001A17D7, "mov qword ptr [rcx], rax"),
                (0x001A17DD, "mov qword ptr [rcx + 8], rcx")])
e630 = [i.op_str for i in body(0x0020E630) if i.mnemonic == "jmp"]
w4d0 = sorted(a for f, a, k in SC["refs"].get(0x01F7F4D0, ()) if k == "W")
r4d0 = sorted(f for f, a, k in SC["refs"].get(0x01F7F4D0, ()) if k != "W")
st1850 = [("%08X" % i.address, i.op_str) for i in body(0x001A1850) if i.address < 0x001A188A and i.operands
          and i.operands[0].type == MEM and canon(i.reg_name(i.operands[0].mem.base)) in ("rbx", "rcx")]
gti = 0x008F5F28
check("R5", ok and e630 == ["0x1fb810"] * 4 and w4d0 == [0x0017D547] and r4d0 == [0x001FB810, 0x001FB830]
      and not st1850 and T.rtti_class(gti) == "GeometryRenderTargetImmediate" and slot(gti, 0) == 0x001F48B0,
      "every submit 0020E630 jumps to 001FB810, which hands the command to 001A17F0 with the handler object "
      "[01F7F4D0]; that 0x10 object is built once (0017D538) by 001A17D0 = vtable %08X %s with +8 = itself, and "
      "neither reader of 01F7F4D0 (001FB810, 001FB830->001A1850) stores through it; its slot 0 is 001F48B0 %s"
      % (gti, T.rtti_class(gti), bad or st1850 or ""))

# R6 001F48B0 wraps the command (+0x18) in a GeometryInstanceOrderedObject and pushes it on the 01F7F5E0 vector
ok, bad = pins([(0x001F48C9, "mov rsi, rdx"), (0x001F490C, "mov rdx, rsi"), (0x001F4912, "call 0x1f4950"),
                (0x001F4929, "call 0x18b4e0"), (0x001F4940, "jmp 0x18aff0"), (0x001F4962, "mov rbx, rdx"),
                (0x001F496D, "lea rax, [rip + 0x70efac]"), (0x001F4974, "mov qword ptr [rdi + 0x18], rbx"),
                (0x001F497D, "mov qword ptr [rdi], rax")])
gio = 0x00903920
check("R6", ok and T.rtti_class(gio) == "GeometryInstanceOrderedObject" and slot(gio, 1) == 0x001F49F0,
      "001F48B0 stores the command at record+0x18 of a %s (vtable %08X, slot 1 = 001F49F0) and appends the record "
      "(0018B4E0 list, 0018AFF0 push_back) %s" % (T.rtti_class(gio), gio, bad or ""))

# R7 the drain calls record slot 1; 001F49F0 queues callback 001F4A10 with the command as its argument
ok, bad = pins([(0x0018B187, "call qword ptr [rax + 8]"), (0x001F49F0, "mov r8, qword ptr [rcx + 0x18]"),
                (0x001F49FA, "lea rdx, [rip + 0xf]"), (0x001F4A01, "jmp 0x5fea50"),
                (0x005FEA5F, "mov rsi, r8"), (0x005FEA62, "mov rdi, rdx"), (0x005FEAEE, "mov dword ptr [rcx], 0x2f"),
                (0x005FEAF4, "mov qword ptr [rcx + 8], rdi"), (0x005FEAF8, "mov qword ptr [rcx + 0x10], rsi")])
check("R7", ok and rip_target(ins(0x001F49FA)) == 0x001F4A10,
      "the render pass list's drain 0018B100 calls record slot 1 (0018B187); 001F49F0 queues a 0x80-byte block "
      "{opcode 0x2F, +8 = 001F4A10, +0x10 = the command} through 005FEA50 %s" % (bad or ""))

# R8 the block executor's 0x2F arm hands the callback a frame whose field 0 is r14 = the render context
mp, ot = 0x0060AAD8, 0x0060AAB8
case2f = R.at(mp + 0x2F - 1, 1)[0]
arm = BASE + i32(ot + 4 * case2f)
ok, bad = pins([(0x0060A5B3, "lea rbx, [rsi + 0x70]"), (0x0060A5C0, "mov ecx, dword ptr [rsi]"),
                (0x0060A5C2, "dec ecx"), (0x0060A5D0, "movzx eax, byte ptr [r12 + rax + 0x4eaad8]"),
                (0x0060A5D9, "mov ecx, dword ptr [r12 + rax*4 + 0x4eaab8]"), (0x0060A5E4, "jmp rcx"),
                (0x0060A9D9, "sub rsi, -0x80"), (0x0060A9DD, "sub rbx, -0x80"),
                (0x0060A46A, "call 0x624670"), (0x0060A46F, "mov r14, rax"),
                (0x0060A8BD, "mov qword ptr [rbp - 0x50], r14"), (0x0060A8CA, "mov rax, qword ptr [rbx - 0x60]"),
                (0x0060A8CE, "mov qword ptr [rbp - 0x40], rax"), (0x0060A8D2, "lea rcx, [rbp - 0x50]"),
                (0x0060A8D6, "call qword ptr [rbx - 0x68]")])
r14w = [("%08X" % i.address, i.mnemonic) for i in body(0x0060A410) if writes(i, "r14") and i.mnemonic != "pop"]
check("R8", ok and arm == 0x0060A899 and rip_target(ins(0x0060A5B7)) == BASE and r14w == [("0060A46F", "mov")],
      "the executor 0060A410 switches on block+0 (rbx = block+0x70); opcode 0x2F decodes to the arm %08X, which "
      "calls block+8 with a frame {+0 = r14, +0x10 = block+0x10}; r14 is written once, 0060A46F = 00624670() %s"
      % (arm, bad or r14w))

# R9 00624670 -> 005FD050 returns the magic static 02CC0410, built by 00615840
ok, bad = pins([(0x00624670, "jmp 0x5fd050"), (0x005FD09E, "mov rcx, rbx"), (0x005FD0A1, "call 0x615840"),
                (0x005FD0BF, "mov rax, rbx")])
check("R9", ok and rip_target(ins(0x005FD097)) == 0x02CC0410 and rip_target(ins(0x005FD0C4)) == 0x02CC0410
      and sorted(SC["calls"].get(0x00615840, ())) == [(0x005FD050, 0x005FD0A1)],
      "00624670 jumps to the magic-static getter 005FD050, which returns 02CC0410 on both exits and is the only "
      "caller of its constructor 00615840 %s" % (bad or ""))

# R10 001F4A10: device = frame[0] + 0x18C0, then jmp command->vtable[1](command, device)
ok, bad = pins([(0x001F4A19, "mov rcx, qword ptr [rcx]"), (0x001F4A1C, "call 0x624660"),
                (0x00624660, "lea rax, [rcx + 0x18c0]"), (0x001F4A26, "mov rcx, qword ptr [rbx + 0x10]"),
                (0x001F4A2A, "mov rdx, rax"), (0x001F4A2D, "mov r8, qword ptr [rcx]"),
                (0x001F4A35, "jmp qword ptr [r8 + 8]")])
refs4a10 = sorted(SC["refs"].get(0x001F4A10, ()))
check("R10", ok and refs4a10 == [(0x001F49F0, 0x001F49FA, "lea")] and not SC["calls"].get(0x001F4A10),
      "001F4A10 calls the command's slot 1 with rdx = frame[0] + 0x18C0 = %08X; it is named only by 001F49FA %s"
      % (DEVICE, bad or ""))

# R11 the +0x18C0 subobject's constructor installs PrimitiveRendererD3D11's vtables
ok, bad = pins([(0x00615860, "mov rbp, rcx"), (0x00615B50, "lea rcx, [rbp + 0x18c0]"), (0x00615B57, "call 0x6c8750"),
                (0x006C8768, "mov qword ptr [rcx], rax"), (0x006C877B, "mov qword ptr [rcx + 8], rax")])
nwb = no_write(0x00615840, 0x00615861, 0x00615B57, "rbp")
pr, pr2 = 0x00D86960, 0x00D86AD0
lpr = sorted((f, a) for f, a, k in SC["refs"].get(pr, ()) if k == "lea")
check("R11", ok and not nwb and rip_target(ins(0x006C8761)) == pr and rip_target(ins(0x006C876E)) == pr2
      and T.rtti_class(pr) == "PrimitiveRendererD3D11" and nslots(pr) == 45
      and T.rtti_class(pr2) == "PrimitiveRendererD3D11"
      and lpr == [(0x006C8750, 0x006C8761), (0x006C8870, 0x006C8870)],
      "00615840 (this = rbp, unchanged to 00615B57) constructs this+0x18C0 with 006C8750, which writes vtable %08X "
      "(RTTI %s, %d slots) at +0 and %08X (same class, secondary) at +8; the only other lea of %08X is 006C8870 %s"
      % (pr, T.rtti_class(pr), nslots(pr), pr2, pr, bad or nwb or ""))

# R12 storage: zero-initialised static, no heap allocation
s1, init1 = section_of(0x02CC0410)
s2, init2 = section_of(G)
check("R12", s1 == ".data" and init1 is False and s2 == ".data" and init2 is False,
      "02CC0410 (the context, so the device %08X) and 01FC35F8 lie in the zero-initialised tail of .data: static "
      "storage, constructed in place, not allocated" % DEVICE)

# R13 conclusion of R2-R11
check("R13", fails == 0,
      "so the value 0021037B stores into 01FC35F8 is %08X = 02CC0410 + 0x18C0, the embedded "
      "PrimitiveRendererD3D11 (vtable 00D86960), on the route GiVmax slot 1 <- 001F4A10 <- block 0x2F <- 001F49F0 "
      "<- 0018B100" % DEVICE)

# D: which device methods the replay calls
print("=== UQ-384 (a): which PrimitiveRendererD3D11 methods the GS replay calls ===")


def track(f, seed_regs=()):
    tags = {r: "DEV" for r in seed_regs}
    out, reads = [], []
    for i in body(f):
        ops = i.operands
        if i.mnemonic in ("call", "jmp") and ops and ops[0].type == MEM and ops[0].mem.base not in (0, RIP) \
                and ops[0].mem.index == 0 and tags.get(canon(i.reg_name(ops[0].mem.base))) == "VT":
            out.append((i.address, ops[0].mem.disp))
        new = dst = None
        if i.mnemonic == "mov" and len(ops) == 2 and ops[0].type == REG:
            dst = canon(i.reg_name(ops[0].reg))
            s = ops[1]
            if s.type == MEM and s.mem.base == RIP and i.address + i.size + s.mem.disp == G:
                new = "DEV"
                reads.append(i.address)
            elif s.type == MEM and s.mem.base not in (0, RIP) and s.mem.index == 0 and s.mem.disp == 0 \
                    and s.size == 8 and tags.get(canon(i.reg_name(s.mem.base))) == "DEV":
                new = "VT"
            elif s.type == REG and tags.get(canon(i.reg_name(s.reg))):
                new = tags[canon(i.reg_name(s.reg))]
        _, w = i.regs_access()
        for r in w:
            tags.pop(canon(i.reg_name(r)), None)
        if i.mnemonic == "call":
            for r in VOLATILE:
                tags.pop(r, None)
        if new:
            tags[dst] = new
    return out, reads


REPLAY = {0x0020EB60: ("rdx",), 0x0020ED30: (), 0x0020FF10: (), 0x002104E0: (), 0x0020FCA0: ()}
disp_all, reads_all = [], []
for f, seed in REPLAY.items():
    o, r = track(f, seed)
    disp_all += [(f, a, d) for a, d in o]
    reads_all += r
all_reads = sorted(a for f, a, k in SC["refs"].get(G, ()) if k == "R")
ok_ec80, bad = pins([(0x0020ECA3, "mov rdx, qword ptr [rip + 0x1db494e]"), (0x0020ECAD, "call 0x20eb60")])
# the 0020EC80 read is passed as 0020EB60's rdx (seeded above): 0020EB60 has that one caller
check("D1", sorted(reads_all + [0x0020ECA3]) == all_reads and ok_ec80
      and sorted(SC["calls"].get(0x0020EB60, ())) == [(0x0020EC80, 0x0020ECAD)],
      "every one of the %d rip reads of 01FC35F8 is followed: %d inside the replay functions, plus 0020ECA3 which "
      "becomes 0020EB60's rdx (its only caller) %s" % (len(all_reads), len(reads_all), bad or ""))
# explicit forms: GiVmax slot 1's own calls on rsi, and the PACKED TEXFLUSH arm on the spilled r8
ok1, bad1 = pins([(0x001DB401, "mov rax, qword ptr [rsi]"), (0x001DB416, "call qword ptr [rax + 0x58]"),
                  (0x001DB4C3, "mov rax, qword ptr [rsi]"), (0x001DB4ED, "jmp qword ptr [rax + 0x58]"),
                  (0x00210454, "mov r8, r14"), (0x00210464, "call 0x20f3e0"),
                  (0x0020F3E0, "mov rax, rsp"), (0x0020F3E3, "mov qword ptr [rax + 0x18], r8"),
                  (0x0020F3EF, "sub rsp, 0x50"), (0x0020FA09, "mov rax, qword ptr [r8]"),
                  (0x0020FA0C, "mov rcx, r8"), (0x0020FA0F, "call qword ptr [rax + 0x128]")])
pushes = [i for i in body(0x0020F3E0) if i.address < 0x0020F3EF and i.mnemonic == "push"]
B3E0 = body(0x0020F3E0)
r8w = [i for i in B3E0 if writes(i, "r8")]
reloads = [i.address for i in r8w if " ".join(i.op_str.split()) == "r8, qword ptr [rsp + 0x90]"]
# every other r8 write lies in the PRIM-type index arms 0020F743-0020F97E, which leave only to 0020FA6F; from there
# the loop runs straight into the reload 0020FA84 before it dispatches again
IDX_LO, IDX_HI = 0x0020F743, 0x0020F97F
others = [i.address for i in r8w if i.address not in reloads]
arm_exits = [i for i in B3E0 if IDX_LO <= i.address < IDX_HI and i.mnemonic.startswith("j")]
# 0020FACE is the MSVC range-check failure call: call 00809728 -> 0080973C (int 0x29 fast-fail, else status
# 0xC0000409) followed by int3, so it never returns to the dispatch
RCF = 0x0020FACE
rcf_ok = (txt(RCF) == "call 0x809728" and R.at(RCF + 5, 1) == b"\xcc" and txt(0x00809731) == "call 0x80973c"
          and txt(0x00809758) == "int 0x29" and txt(0x00809790) == "mov dword ptr [rip + 0x26a55f6], 0xc0000409")
exits_ok = rcf_ok and all(i.operands[0].type == IMM and (IDX_LO <= i.operands[0].imm < IDX_HI
                                                         or i.operands[0].imm in (0x0020FA6F, RCF))
                          for i in arm_exits)
tail = [i for i in B3E0 if 0x0020FA6F <= i.address < 0x0020FA84]
spill_ok = (0x18 + 8 * len(pushes) + 0x50 == 0x90 and reloads == [0x0020F492, 0x0020FA84]
            and all(IDX_LO <= a < IDX_HI for a in others) and exits_ok
            and not [i for i in tail if i.mnemonic.startswith("j") or i.mnemonic in ("call", "ret")]
            and txt(0x0020F48D) == "call 0x20ec80" and ins(0x0020F48D).address + 5 == 0x0020F492)
nw_r14 = no_write(0x00210320, 0x00210331, 0x00210464, "r14")
explicit = [(0x001DB3D0, 0x001DB416, 0x58), (0x001DB3D0, 0x001DB4ED, 0x58), (0x0020F3E0, 0x0020FA0F, 0x128)]
check("D2", ok1 and spill_ok and not nw_r14,
      "two more receivers are the same object: 001DB3D0 calls slot 11 on its rsi (= the device) twice, and the "
      "PACKED TEXFLUSH arm 0020FA0F calls slot 37 on r8, which is 00210320's r14 (= its rdx) spilled at entry "
      "(0x18 + %d pushes + 0x50 = 0x90) and reloaded from [rsp + 0x90] at 0020F492 (after the only call before the "
      "dispatch) and 0020FA84 (loop tail); the %d other r8 writes sit in the index arms, which exit only to the loop tail or the no-return range-check failure 0020FACE "
      "%s" % (len(pushes), len(others), bad1 or nw_r14 or "") + ("" if spill_ok else " DIAG reloads=%s "
      "others=%s bad_exits=%s" % (["%08X" % a for a in reloads], ["%08X" % a for a in others],
                                  ["%08X %s" % (i.address, i.op_str) for i in arm_exits
                                   if not (i.operands[0].type == IMM and (IDX_LO <= i.operands[0].imm < IDX_HI
                                                                          or i.operands[0].imm == 0x0020FA6F))])))
rows = []
okd = True
for f, a, d in disp_all + explicit:
    k = d // 8
    m = slot(pr, k) if d % 8 == 0 and k < 45 else None
    okd &= m is not None
    rows.append((f, a, k, m))
used = collections.OrderedDict()
for f, a, k, m in sorted(rows, key=lambda r: r[2]):
    used.setdefault((k, m), []).append("%08X" % a)
for (k, m), sites in used.items():
    print("      slot %2d (+0x%03X) -> %08X  at %s" % (k, 8 * k, m or 0, " ".join(sites)))
must = {(0x0020EB60, 0x0020EC67, 5), (0x0020FCA0, 0x0020FD88, 37), (0x0020F3E0, 0x0020FA0F, 37),
        (0x002104E0, 0x002104F7, 37)}
check("D3", okd and must <= {(f, a, k) for f, a, k, m in rows} and max(k for f, a, k, m in rows) < 45,
      "the replay makes %d dispatches on the device at %d distinct slots, all inside PrimitiveRendererD3D11's 45-slot "
      "table (control: 0020EB60's draw at +0x28 and TEXFLUSH's slot 37 in both dispatchers are among them)"
      % (len(rows), len(used)))

# ==================================================================================================================
# UQ-384 (b): what the GS state handlers store
# ==================================================================================================================
print("=== UQ-384 (b): what the GS state handlers store ===")


def table(mp, ot, n=0x50):
    out = {}
    for dsc in range(n):
        c = R.at(mp + dsc, 1)[0]
        out[dsc] = BASE + i32(ot + 4 * c)
    return out


ok, bad = pins([(0x0020F420, "lea r14, [rip - 0xef427]"), (0x0020F4A1, "cmp ebx, 0x4f"), (0x0020F4A4, "ja 0x20fa6f"),
                (0x0020F4AC, "movzx eax, byte ptr [r14 + rax + 0xefb28]"),
                (0x0020F4B5, "mov ecx, dword ptr [r14 + rax*4 + 0xefad4]"), (0x0020F4C0, "jmp rcx"),
                (0x0020F3F3, "mov rbx, qword ptr [rcx + 0x10]"), (0x0020F451, "lea eax, [rsi + 3]"),
                (0x0020F454, "movsxd rcx, eax"), (0x0020F457, "mov rdx, rcx"), (0x0020F45A, "movsxd rax, esi"),
                (0x0020F45D, "sub rdx, rax"), (0x0020F460, "cmp rdx, 0x3f"), (0x0020F466, "inc rdx"),
                (0x0020F469, "or rax, 0xffffffffffffffff"), (0x0020F46D, "sub cl, dl"), (0x0020F46F, "inc ecx"),
                (0x0020F471, "shr rbx, cl"), (0x0020F474, "mov rcx, rdx"), (0x0020F477, "shl rax, cl"),
                (0x0020F47A, "not rax"), (0x0020F47D, "and rbx, rax"), (0x0020FA7A, "add esi, 4")])
PK = table(0x0020FB28, 0x0020FAD4)
IGN_P = 0x0020FA6F
check("H1", ok and rip_target(ins(0x0020F420)) == BASE,
      "PACKED dispatcher 0020F3E0: the descriptor is (REGS >> 4k) & 0xF (width (k*4+3) - k*4 + 1 = 4 bits), so only "
      "descriptors 0-0xF reach the map at 0020FB28; arms above 0xF are unreachable from PACKED %s" % (bad or ""))
ok, bad = pins([(0x0020FCA4, "mov rdx, qword ptr [rcx]"), (0x0020FCA7, "mov qword ptr [rip + 0x1db395a], rdx"),
                (0x0020FCAE, "movzx r8d, byte ptr [rcx + 8]"), (0x0020FCB3, "mov dword ptr [rip + 0x1db3956], r8d"),
                (0x0020FCBA, "lea eax, [r8 - 1]"), (0x0020FCBE, "cmp eax, 4"), (0x0020FCC3, "call 0x20ec80"),
                (0x0020FCD6, "mov byte ptr [rip + 0x1db3926], 1"), (0x0020FCDD, "cmp r8d, 0x4f"),
                (0x0020FCE1, "ja 0x20fdd2"), (0x0020FCF1, "movzx eax, byte ptr [r8 + rax + 0xefe14]"),
                (0x0020FCFA, "mov ecx, dword ptr [r8 + rax*4 + 0xefdd8]"), (0x0020FD05, "jmp rcx")])
AD = table(0x0020FE14, 0x0020FDD8)
IGN_A = 0x0020FDD2
check("H2", ok and rip_target(ins(0x0020FCEA)) == BASE,
      "A+D handler 0020FCA0: stores the data qword at 01FC3608 and the register byte (bits 64-71) at 01FC3610; for "
      "a register outside 1-5 it first flushes (0020EC80) and sets 01FC3603; then registers 0-0x4F go through "
      "the map at 0020FE14 %s" % (bad or ""))

GSN = {0x00: "PRIM", 0x01: "RGBAQ", 0x02: "ST", 0x03: "UV", 0x04: "XYZF2", 0x05: "XYZ2", 0x06: "TEX0_1",
       0x07: "TEX0_2", 0x08: "CLAMP_1", 0x09: "CLAMP_2", 0x0A: "FOG", 0x0C: "XYZF3", 0x0D: "XYZ3", 0x0E: "A+D",
       0x0F: "NOP", 0x14: "TEX1_1", 0x15: "TEX1_2", 0x16: "TEX2_1", 0x17: "TEX2_2", 0x18: "XYOFFSET_1",
       0x19: "XYOFFSET_2", 0x1A: "PRMODECONT", 0x1B: "PRMODE", 0x1C: "TEXCLUT", 0x22: "SCANMSK", 0x34: "MIPTBP1_1",
       0x35: "MIPTBP1_2", 0x36: "MIPTBP2_1", 0x37: "MIPTBP2_2", 0x3B: "TEXA", 0x3D: "FOGCOL", 0x3F: "TEXFLUSH",
       0x40: "SCISSOR_1", 0x41: "SCISSOR_2", 0x42: "ALPHA_1", 0x43: "ALPHA_2", 0x44: "DIMX", 0x45: "DTHE",
       0x46: "COLCLAMP", 0x47: "TEST_1", 0x48: "TEST_2", 0x49: "PABE", 0x4A: "FBA_1", 0x4B: "FBA_2",
       0x4C: "FRAME_1", 0x4D: "FRAME_2", 0x4E: "ZBUF_1", 0x4F: "ZBUF_2"}
STOP = {0x0020F6F6, IGN_P}


def arm_stores(t, stop_jumps=True):
    """Linear walk of one arm until its first unconditional exit; returns (stores, calls, exit)."""
    st, calls, ex = [], [], None
    for i in MD.disasm(R.at(t, 0x200), t):
        if i.address in STOP and i.address != t:
            ex = "falls into %08X" % i.address
            break
        g = rip_target(i)
        if g is not None and kind(i) == "W":
            st.append((g, i.operands[0].size))
        if i.mnemonic == "call":
            calls.append(i.op_str)
        if i.mnemonic in ("jmp", "ret"):
            ex = "%s %s" % (i.mnemonic, i.op_str)
            break
    return st, calls, ex


def fmt(st):
    return ",".join("%08X/%d" % (g, w) for g, w in st)


EXP_P = {
    0x00: ({(0x01F83562, 1), (0x01FC3600, 1), (0x01F8357C, 1), (0x01F8357D, 1), (0x01F8357E, 1), (0x01F8357F, 1),
            (0x01FC3601, 1), (0x01FC3602, 1), (0x01F83574, 4), (0x01F83568, 4)}, ["0x20fba0"]),
    0x01: ({(0x01FC361F, 1), (0x01FC361E, 1), (0x01FC361D, 1), (0x01FC361C, 1), (0x01FC3618, 4)}, []),
    0x02: ({(0x01FCB604, 4), (0x01FCB600, 4), (0x01E027B0, 4)}, []),
    0x03: ({(0x01FCB60C, 4), (0x01FCB608, 4)}, []),
    0x04: ({(0x01F83574, 4), (0x01F83568, 4), (0x01F83563, 1)}, ["0x20ec80"]),
    0x05: ({(0x01F83574, 4), (0x01F83568, 4)}, ["0x20ec80"]),
    0x06: ({(0x01FC3588, 8)}, []), 0x07: ({(0x01FC3590, 8)}, []), 0x08: ({(0x01FC35B8, 8)}, []),
    0x09: ({(0x01FC35C0, 8)}, []), 0x0A: ({(0x01F83563, 1)}, []), 0x0E: (set(), ["0x20fca0"]),
    0x3B: ({(0x01E027B8, 8)}, []), 0x3F: (set(), ["qword ptr [rax + 0x128]"]),
    0x42: ({(0x01FC35D8, 8)}, []), 0x43: ({(0x01FC35E0, 8)}, []), 0x47: ({(0x01FC35C8, 8)}, []),
    0x48: ({(0x01FC35D0, 8)}, []), 0x4E: ({(0x01FC35E8, 8)}, []), 0x4F: ({(0x01FC35F0, 8)}, [])}
EXP_A = {
    0x00: (set(), [], "jmp 0x20fe70"), 0x06: ({(0x01FC3588, 8)}, [], "ret "), 0x07: ({(0x01FC3590, 8)}, [], "ret "),
    0x08: ({(0x01FC35B8, 8)}, [], "ret "), 0x09: ({(0x01FC35C0, 8)}, [], "ret "),
    0x3B: ({(0x01E027B8, 8)}, [], "ret "), 0x3D: ({(0x01FC3604, 1), (0x01FC3605, 1), (0x01FC3606, 1)}, [], "ret "),
    0x3F: (set(), [], "jmp qword ptr [rax + 0x128]"), 0x42: ({(0x01FC35D8, 8)}, [], "ret "),
    0x43: ({(0x01FC35E0, 8)}, [], "ret "), 0x47: ({(0x01FC35C8, 8)}, [], "ret "),
    0x48: ({(0x01FC35D0, 8)}, [], "ret "), 0x4E: ({(0x01FC35E8, 8)}, [], "ret "),
    0x4F: ({(0x01FC35F0, 8)}, [], "ret ")}
badp, bada = [], []
print("    PACKED (0020F3E0) - descriptor: GS register -> arm : stores (address/bytes) ; calls ; exit")
for dsc in range(0x50):
    t = PK[dsc]
    if dsc in EXP_P:
        st, calls, ex = arm_stores(t)
        es, ec = EXP_P[dsc]
        good = set(st) == es and calls == ec
        badp += [] if good else ["%02X" % dsc]
        print("      %02X %-9s %s %08X : %s ; %s ; %s" % (dsc, GSN.get(dsc, "-"), "reach" if dsc <= 0xF else "DEAD ",
                                                         t, fmt(sorted(set(st))) or "-", ",".join(calls) or "-", ex))
    elif t != IGN_P:
        badp.append("%02X(unexpected arm %08X)" % (dsc, t))
ign_p = [d for d in range(0x50) if PK[d] == IGN_P]
print("      ignored (-> 0020FA6F): %s" % " ".join("%02X" % d for d in ign_p))
print("    A+D (0020FCA0) - register -> arm : stores ; exit")
for dsc in range(0x50):
    t = AD[dsc]
    if dsc in EXP_A:
        st, calls, ex = arm_stores(t)
        es, ec, ee = EXP_A[dsc]
        good = set(st) == es and calls == ec and ex == ee
        bada += [] if good else ["%02X" % dsc]
        print("      %02X %-9s %08X : %s ; %s" % (dsc, GSN.get(dsc, "-"), t, fmt(sorted(set(st))) or "-", ex))
    elif t != IGN_A:
        bada.append("%02X(unexpected arm %08X)" % (dsc, t))
ign_a = [d for d in range(0x50) if AD[d] == IGN_A]
print("      ignored (-> 0020FDD2): %s" % " ".join("%02X" % d for d in ign_a))
check("H3", not badp and len([d for d in EXP_P if d <= 0xF]) == 12 and ign_p[:4] == [0x0B, 0x0C, 0x0D, 0x0F],
      "PACKED: 12 reachable arms (PRIM, RGBAQ, ST, UV, XYZF2, XYZ2, TEX0_1/2, CLAMP_1/2, FOG, A+D) store exactly the "
      "listed globals; XYZF3 / XYZ3 / NOP / 0x0B are ignored; the 8 arms for 0x3B-0x4F exist but are unreachable "
      "%s" % (badp or ""))
check("H4", not bada and all(AD[d] == IGN_A for d in (1, 2, 3, 4, 5, 0x0A, 0x0C, 0x0D)),
      "A+D: 14 registers have arms (PRIM via 0020FE70, TEX0, CLAMP, TEXA, FOGCOL, TEXFLUSH, ALPHA, TEST, ZBUF); "
      "RGBAQ/ST/UV/XYZF2/XYZ2/FOG/XYZF3/XYZ3 written through A+D are ignored %s" % (bada or ""))

# H5: the bit split of PRIM (both writers) and the RGBAQ/ST/UV/FOG value forms, read from the instructions
ok, bad = pins([(0x0020F4C7, "and ecx, 0x7ff"), (0x0020F4CF, "and eax, 7"),
                (0x0020F4DC, "shr rax, 3"), (0x0020F4E5, "setne byte ptr [rip + 0x1db4114]"),
                (0x0020F4EC, "shr rax, 4"), (0x0020F4F5, "setne byte ptr [rip + 0x1d74080]"),
                (0x0020F4FC, "shr rax, 5"), (0x0020F505, "setne byte ptr [rip + 0x1d74071]"),
                (0x0020F50C, "shr rax, 6"), (0x0020F515, "setne byte ptr [rip + 0x1d74062]"),
                (0x0020F51C, "shr rax, 8"), (0x0020F525, "setne byte ptr [rip + 0x1d74053]"),
                (0x0020F52C, "shr rax, 9"), (0x0020F533, "shr rdx, 0xa"),
                (0x0020F53A, "mov byte ptr [rip + 0x1db40c1], al"), (0x0020F540, "setne byte ptr [rip + 0x1db40bb]"),
                (0x0020FE7B, "mov byte ptr [rip + 0x1d736e1], al"), (0x0020FE83, "shr rax, 3"),
                (0x0020FEC3, "shr rax, 8"), (0x0020FEDA, "shr rdx, 0xa"),
                (0x0020F562, "movzx eax, byte ptr [rcx]"), (0x0020F56E, "shr rax, 0x20"),
                (0x0020F57B, "movzx eax, byte ptr [rcx + 8]"), (0x0020F589, "shr rax, 0x20"),
                (0x0020F596, "cvttss2si rax, dword ptr [rip + 0x1bf3211]"),
                (0x0020F5F9, "divss xmm2, xmm0"), (0x0020F5FD, "divss xmm1, xmm0"),
                (0x0020F626, "and eax, 0x3fff"), (0x0020F64B, "and eax, 0x3fff"),
                (0x0020F9CA, "mov rcx, qword ptr [rax + 8]"), (0x0020F9CE, "shr rcx, 0x24"),
                (0x0020F9DC, "mulss xmm0, xmm7"), (0x0020F437, "movss xmm7, dword ptr [rip + 0x6e3cad]"),
                (0x0020FD52, "movzx eax, dl"), (0x0020FD5B, "movzx eax, byte ptr [rip + 0x1db38a7]"),
                (0x0020FD68, "movzx eax, byte ptr [rip + 0x1db389b]"),
                (0x0020FD07, "mov ecx, dword ptr [rip + 0x1db38fb]"), (0x0020FD11, "jmp 0x20fe70")])
f16 = struct.unpack("<f", R.at(0x008F30EC, 4))[0]
check("H5", ok and f16 == 0.0625 and rip_target(ins(0x0020FD5B)) == 0x01FC3609
      and rip_target(ins(0x0020FD68)) == 0x01FC360A,
      "value forms: PRIM bits 0-2 / 3 / 4 / 5 / 6 / 8 / 9 / 10 (type, IIP, TME, FGE, ABE, FST, CTXT, FIX; bit 7 AA1 "
      "dropped) in both writers; RGBAQ R,G,B,A bytes reversed into 01FC361F..1C and (int)Q into 01FC3618; ST stores "
      "S/Q, T/Q and Q; UV the 14-bit U, V as floats; FOG = (int)(F x %.4f) into a byte; FOGCOL bytes 0-2 of the data; "
      "PRIM via A+D passes the data's low dword %s" % (f16, bad or ""))

# H6: who reads each stored global (rip census over listed functions + byte-level rel32 sweep + pointers)
STORED = {}
for d, (es, ec) in EXP_P.items():
    for g, w in es:
        STORED.setdefault(g, w)
for d, (es, ec, ee) in EXP_A.items():
    for g, w in es:
        STORED.setdefault(g, w)
STORED.update({0x01FC3608: 8, 0x01FC3610: 4, 0x01FC3580: 8})
WRITERS = {0x0020F3E0, 0x0020FCA0, 0x0020FE70}
windows = [(0x01F83560, 0x01F83580), (0x01FC3580, 0x01FC3620), (0x01E027B0, 0x01E027C8), (0x01FCB600, 0x01FCB610)]
readers = collections.defaultdict(set)
for lo, hi in windows:
    for f, i in real_refs(lo - 15, hi):
        for op in i.operands:
            if op.type == MEM and op.mem.base == RIP and kind(i) in ("R", "lea", "W"):
                a0 = i.address + i.size + op.mem.disp
                sz = op.size or 1
                for g, w in STORED.items():
                    if a0 < g + w and g < a0 + sz:
                        k = kind(i)
                        if k == "R" or (k == "W" and i.mnemonic in ("add", "sub", "or", "and", "xor", "inc", "dec")):
                            readers[g].add((f, i.address))
                        elif k == "lea":
                            readers[g].add((f, i.address, "lea"))
raw_ptr_hits = data_sweep([g for lo, hi in windows for g in range(lo, hi)], 8) + \
    data_sweep([g for lo, hi in windows for g in range(lo, hi)], 4)
ptr_hits = [x for x in raw_ptr_hits if real_pointer(x)]
def ibr_scan(vals):
    """Image-base-relative operands: an in-stream instruction with a memory displacement equal to an RVA in vals."""
    out = []
    for nm, a, v in data_sweep(vals, 4):
        if nm != ".text":
            continue
        for back in range(1, 12):
            s = a - back
            i = next(MD.disasm(R.at(s, 16), s, 1), None)
            if i is not None and s < a < s + i.size and any(op.type == MEM and op.mem.disp == v for op in i.operands):
                ok_s, f = in_stream(i)
                if ok_s:
                    out.append(("%08X" % i.address, "%08X" % (v + BASE)))
                    break
    return out


ibr_hits = ibr_scan([g - BASE for lo, hi in windows for g in range(lo, hi)])
k9 = ibr_scan([0x01FCB610 - BASE])
check("K9", ("0020F93C", "01FCB610") in k9,
      "control: the image-base-relative detector finds 0020F93C's write [r14 + r9*2 + 0x1eab610] = 01FCB610 "
      "(the index buffer just above the UV window)")
unread = []
print("    stored global -> readers (function@site)")
for g in sorted(STORED):
    rs = sorted(readers.get(g, ()))
    ext = sorted({r[0] for r in rs})
    if not rs:
        unread.append(g)
    print("      %08X/%d : %s" % (g, STORED[g], " ".join("%08X@%08X%s" % (r[0], r[1], "(lea)" if len(r) > 2 else "")
                                                     for r in rs) or "NO READER"))
check("K4", {0x0020EB60, 0x0020ED30} <= {r[0] for r in readers.get(0x01FC3588, ())},
      "control: the reader census finds TEX0_1's known readers 0020EB60 and 0020ED30")
EXP_UNREAD = {0x01F8357D, 0x01FC3602, 0x01F83563, 0x01FC3604, 0x01FC3605, 0x01FC3606, 0x01FC3618, 0x01FC35E8,
              0x01FC35F0}
check("H6", set(unread) == EXP_UNREAD and not ptr_hits and not ibr_hits,
      "nine stored values have no reader anywhere in .text (rip operand of any width, byte-level), no data pointer "
      "into their blocks (%d) and no image-base-relative operand (%d): FGE 01F8357D, FIX 01FC3602, FOG 01F83563, "
      "FOGCOL 01FC3604-06, (int)Q 01FC3618, ZBUF_1 01FC35E8, ZBUF_2 01FC35F0 %s"
      % (len(ptr_hits), len(ibr_hits), sorted("%08X" % g for g in set(unread) ^ EXP_UNREAD) or ""))

# ==================================================================================================================
# UQ-385: the 19 caller-less VU-state touchers
# ==================================================================================================================
print("=== UQ-385: the 19 caller-less VU-state touchers ===")
WORK = os.path.join(DBROOT, "Tools", "work")
cen = json.load(open(os.path.join(WORK, "FABLE", "pub140-scratch", "vu1_census.json")))
reg = {int(x, 16) for x in json.load(open(os.path.join(WORK, "FABLE", "pub140-scratch",
                                                        "vu1_registered_programs.json")))}
micro = {int(x, 16) for x in cen["programs"]} | reg
touch = {int(x, 16) for x in cen["vu_touchers_not_installed"]}
callers = collections.defaultdict(set)
for ln in open(os.path.join(WORK, "graph", "edges.tsv"), encoding="utf-8", errors="replace"):
    p = ln.split("\t")
    try:
        callers[int(p[1], 16)].add(int(p[0], 16))
    except ValueError:
        pass
L19 = sorted(a for a in touch if not callers[a])
only_m = [a for a in touch if callers[a] and callers[a] <= micro]
other = sorted(a for a in touch if callers[a] and not callers[a] <= micro)
check("V1", len(touch) == 54 and len(L19) == 19 and len(only_m) == 33 and other == [0x004A6780, 0x004EF860],
      "rebuilt with the census's own method (vu1_census.json touchers x the E8/E9 edge index, as "
      "Tools/work/SWE2-FRONTIER/vu1_region_tsv.py): 54 touchers = %d with only microprogram callers + %d with "
      "sibling-toucher callers (004A6780, 004EF860) + %d with none; the 19: %s"
      % (len(only_m), len(other), len(L19), " ".join("%08X" % a for a in L19)))
u213 = set()
for ln in open(os.path.join(HERE, "..", "uq213-microprogram-draws", "uq213-programs.tsv"), encoding="utf-8"):
    tok = ln.split("\t")[0]
    if len(tok) == 8 and tok != "program":
        u213.add(int(tok, 16))
check("V2", len(u213) == 57 and set(L19) <= u213 and len(set(L19) & reg) == 9,
      "all 19 are in UQ-213's 57 VU1 microprograms: 9 were already in the 2026-09-13 registrar list the census "
      "itself used (it gave the toucher role without excluding microprograms), 10 were added by UQ-213 through "
      "003A33B0 / 003A2F70")

# direct branches of every width
rel32 = {a: [(f, i) for f, i in real_refs(a, a + 1) if kind(i) == "branch"] for a in L19}
rel8 = collections.defaultdict(list)
nm, va, data, raw, vsz, ex = TEXT
arr = np.frombuffer(data, dtype=np.uint8)
sx = arr.view(np.int8)
op8 = np.isin(arr, np.array([0xEB] + list(range(0x70, 0x80)) + [0xE0, 0xE1, 0xE2, 0xE3], dtype=np.uint8))
idx = np.nonzero(op8[:-1])[0]
tg8 = va + idx + 2 + sx[idx + 1].astype(np.int64)
for t in L19 + [0x00210495]:
    for j in idx[tg8 == t]:
        s = va + int(j)
        i = next(MD.disasm(R.at(s, 4), s, 1), None)
        if i is not None and in_stream(i)[0] and i.operands and i.operands[0].type == IMM and i.operands[0].imm == t:
            rel8[t].append(s)
check("K5", rel8.get(0x00210495) == [0x0021047D],
      "control: the rel8 sweep finds the short branch 0021047D -> 00210495")
sub = 0x0047BFB0
subc = [(f, i) for f, i in real_refs(sub, sub + 1) if kind(i) == "branch"]
check("K7", subc and all(c in micro for c, i in subc),
      "control: the direct-branch sweep finds the sub-program 0047BFB0's callers %s (all microprograms)"
      % ["%08X@%08X" % (f, i.address) for f, i in subc])
bad_br = {("%08X" % a): ["%08X" % i.address for f, i in v] for a, v in rel32.items() if v}
# residue of the byte sweep: 4-byte fields that point at one of the 19 but do not decode as an instruction of a listed
# function's own stream. Each is shown with what does decode there.
raw_unres = []
for a in L19:
    for fva, e, tgt in rel32_sweep(a, a + 1):
        if decode_field(fva, e, tgt) is None:
            raw_unres.append(("%08X" % a, "%08X" % fva, e, list(_decode_candidates(fva, e, tgt)) != []))
bad_b8 = {("%08X" % a): ["%08X" % s for s in rel8.get(a, ())] for a in L19 if rel8.get(a)}
prev = {}
for a in L19:
    pb = R.at(a - 1, 1)[0]
    prev[a] = pb
check("V3", not bad_br and not bad_b8 and all(prev[a] == 0xCC for a in L19) and not any(r[3] for r in raw_unres),
      "none of the 19 is the target of a direct call / jmp / jcc of any width anywhere in .text (byte-level rel32 and "
      "rel8 sweeps), and each is preceded by 0xCC padding, so none is entered by fall-through: no x64 JAL "
      "equivalent reaches them; byte-sweep residue: %d field(s) spelling a rel32 to one of them that decode as no "
      "listed-stream instruction and have no decoding that uses the target at all (False = coincidental bytes) %s %s %s" % (len(raw_unres), raw_unres, bad_br or "", bad_b8 or ""))

# data and relocation references
PE.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BASERELOC"]])
RELOC = set()
for blk in PE.DIRECTORY_ENTRY_BASERELOC:
    for e in blk.entries:
        if e.type:
            RELOC.add(BASE + e.rva)
check("K8", 0x009007F0 in RELOC and len(RELOC) > 100000,
      "control: the base-relocation table (%d slots) contains the vtable slot 009007F0" % len(RELOC))
va_q = data_sweep(L19, 8)
va_d = data_sweep(L19, 4)
rva_d = data_sweep([a - BASE for a in L19], 4)
k3 = data_sweep([0x001DB3D0], 8)
k3r = data_sweep([0x0060A899 - BASE], 4)
check("K3", (".rdata", 0x009007F0, 0x001DB3D0) in k3 and any(x[1] == 0x0060AAD0 for x in k3r),
      "control: the data sweep finds the qword 009007F0 = 001DB3D0 and the jump-table RVA 0060AAD0 -> 0060A899")
pd_nm, pd_va, pd_data, _, pd_vsz, _ = PDATA
chain, handler_blk = {}, {}
uis = []
for o in range(0, pd_vsz - 11, 12):
    b, e, u = struct.unpack_from("<III", pd_data, o)
    if not b:
        continue
    ui = BASE + (u & ~1)
    uis.append((ui, BASE + b))
    hdr = R.at(ui, 4)
    flags, cnt = hdr[0] >> 3, hdr[2]
    pos = ui + 4 + 2 * ((cnt + 1) & ~1)
    if flags & 4:
        chain[pos] = BASE + b
    elif flags & 3:
        handler_blk[ui] = BASE + b
uis.sort()
pd_begin = {pd_va + o: BASE + struct.unpack_from("<I", pd_data, o)[0] for o in range(0, pd_vsz - 11, 12)}


def classify(nm, a, v, form):
    if nm == ".pdata":
        if form == "rva" and a in pd_begin and pd_begin[a] == v + BASE:
            return "own .pdata entry (RUNTIME_FUNCTION.BeginAddress)"
        if form == "rva":
            return None                    # an EndAddress / UnwindData equal to the entry: not expected, report it
        return ".pdata field %s: an RVA, so it names VA %08X, not this address" % (
            ("Begin", "End", "Unwind")[((a - pd_va) % 12) // 4] if (a - pd_va) % 4 == 0 else "(unaligned)", v + BASE)
    if nm == ".rdata" and form == "rva" and a in chain:
        frag = chain[a]
        par = BASE + u32(a)
        return "chained unwind: fragment %08X's unwind info names its parent's RUNTIME_FUNCTION (begin %08X)" % (frag,
                                                                                                                 par)
    if nm == ".rdata" and form == "va":
        import bisect
        k = bisect.bisect_right([x[0] for x in uis], a) - 1
        ui, owner = uis[k]
        if ui in handler_blk and owner - BASE == v:
            return "exception-handler data of %08X (unwind %08X): the RVA of its own start, 0x%X" % (owner, ui, v)
    if nm == ".text":
        for back in range(1, 12):
            s = a - back
            i = next(MD.disasm(R.at(s, 16), s, 1), None)
            if i is not None and s < a < s + i.size and in_stream(i)[0]:
                vals = [op.imm for op in i.operands if op.type == IMM] + \
                       [op.mem.disp for op in i.operands if op.type == MEM]
                if v not in vals:
                    return "bytes inside the encoding of %08X %s %s (no operand equals the value)" % (
                        i.address, i.mnemonic, i.op_str)
    return None


per = {a: [] for a in L19}
uncls = []
for lst, form in ((va_q, "va"), (va_d, "va"), (rva_d, "rva")):
    for nm, a, v in lst:
        tgt = v + BASE if form == "rva" else v
        c = classify(nm, a, v, form)
        if c is None:
            uncls.append((nm, "%08X" % a, "%08X" % v, form))
        else:
            per[tgt].append(c)
own_pd = all(sum(1 for c in per[a] if c.startswith("own .pdata")) == 1 for a in L19)
in_rel = [a for a in RELOC if q(a) in set(L19)]
check("V4", not uncls and own_pd and not in_rel and not va_q,
      "data: no qword anywhere holds any of the 19 (and no relocated slot does); every 32-bit VA or RVA match is "
      "metadata - each one's own .pdata entry, chained-unwind parent links, one handler table naming 005A5790, two "
      ".pdata RVAs of other functions, and one stray byte run inside 00315EC5 - none is a pointer to the entry "
      "%s" % (uncls or ""))
for a in L19:
    other_meta = [c for c in per[a] if not c.startswith("own .pdata")]
    if other_meta:
        print("      %08X: %s" % (a, "; ".join(other_meta)))

# the only formation of each address: lea -> registrar program argument
REGARG = {0x003A34D0: "r9", 0x003A33B0: "r9", 0x003A35E0: "r8", 0x003A2F70: "r8"}


def lea_to_registrar(f, site):
    i0 = ins(site)
    if i0.mnemonic != "lea":
        return None
    dst = canon(i0.reg_name(i0.operands[0].reg))
    for i in body(f):
        if i.address <= site:
            continue
        if i.mnemonic == "call":
            t = i.operands[0].imm if i.operands[0].type == IMM else None
            return t if t in REGARG and REGARG[t] == dst else None
        if i.mnemonic in ("jmp", "ret") or writes(i, dst):
            return None
    return None


forms = {}
okv = True
v5bad = []
for a in L19:
    rs = sorted(SC["refs"].get(a, ()))
    byte = real_refs(a, a + 1)
    sites = sorted(i.address for f, i in byte)
    if sites != sorted(x[1] for x in rs) or not all(x[2] == "lea" for x in rs):
        v5bad.append(("%08X" % a, "byte", ["%08X" % s for s in sites], "rip", ["%08X" % x[1] for x in rs]))
    forms[a] = [(f, s, lea_to_registrar(f, s)) for f, s, k in rs]
    v5bad += [("%08X" % a, "noslice", "%08X" % s) for f, s, r in forms[a] if r is None]
    okv &= bool(forms[a])
okv &= not v5bad
nsites = sum(len(v) for v in forms.values())
by_reg = collections.Counter(r for v in forms.values() for f, s, r in v)
check("V5", okv,
      "each of the 19 has its address formed only by rip-relative lea (%d sites, byte sweep = rip census), and every "
      "lea feeds the program argument of a registrar call with no rewrite in between (%s)"
      % (nsites, ", ".join("%08X x%d" % (k, v) for k, v in sorted(by_reg.items() if not None in by_reg else
                                                                    [x for x in by_reg.items() if x[0]])))
      + (" %s" % v5bad if v5bad else ""))
check("K6", lea_to_registrar(0x0020F3E0, 0x0020F420) is None and lea_to_registrar(0x0044E530, 0x0044E8D9) == 0x003A34D0,
      "control: the slice rejects 0020F420 (lea r14 -> image base, no registrar) and accepts 0044E8D9 -> 003A34D0")

# the registrar -> MPG -> MSCAL route; no VU microcode exists to hold a JAL/JR
ok, bad = pins([(0x003A3500, "mov rsi, r9"), (0x003A357A, "mov r9, rsi"), (0x003A35B9, "call 0x1db840"),
                (0x003A33E1, "mov rsi, r9"), (0x003A3457, "mov r9, rsi"), (0x003A34A4, "call 0x1db840"),
                (0x003A35FD, "mov rdi, r8"), (0x003A3616, "mov r9, rdi"), (0x003A363D, "call 0x1db840"),
                (0x003A2F8D, "mov rdi, r8"), (0x003A2FA6, "mov r9, rdi"), (0x003A2FDE, "call 0x1db840"),
                (0x001DB85B, "mov r15, r9"), (0x001DB970, "mov qword ptr [rip + 0x1c216c9], r15"),
                (0x0022CA3D, "cmp cl, 0x4a"), (0x0022CA4B, "mov rax, qword ptr [rax + rbp]"),
                (0x0022CA4F, "mov qword ptr [r9 + rcx*8], rax"), (0x0022CA5D, "add edi, 8"),
                (0x0022CB17, "lea rax, [rip + 0x1e3c312]"), (0x0022CB1E, "call qword ptr [rax + r9*8]")])
nwr = (no_write(0x003A34D0, 0x003A3501, 0x003A357A, "rsi") + no_write(0x003A33B0, 0x003A33E2, 0x003A3457, "rsi")
       + no_write(0x003A35E0, 0x003A35FE, 0x003A3616, "rdi") + no_write(0x003A2F70, 0x003A2F8E, 0x003A2FA6, "rdi")
       + no_write(0x001DB840, 0x001DB85C, 0x001DB970, "r15"))
t68 = sorted({(f, k) for g in range(0x02068E30, 0x02068E30 + 0x2000, 8) for f, a, k in SC["refs"].get(g, ())})
w040 = sorted((f, a) for f, a, k in SC["refs"].get(0x01DFD040, ()))
check("V6", ok and not nwr and rip_target(ins(0x001DB970)) == 0x01DFD040 and w040 == [(0x001DB840, 0x001DB970)]
      and t68 == [(0x0022C970, "lea")] and rip_target(ins(0x0022C999)) == 0x02068E30,
      "route: each registrar carries the program to 001DB840's 4th argument, which stores it as the MPG chunk's "
      "+8 pointer (01DFD040, its only writer); the interpreter's MPG case copies that 8-byte payload into the program "
      "table 02068E30 (touched only by 0022C970's leas), and MSCAL calls it (0022CB1E) %s" % (bad or nwr or ""))
mpg = [i for i in MD.disasm(R.at(0x0022CA3D, 0x0022CA68 - 0x0022CA3D), 0x0022CA3D)]
mpg_back = [("%08X" % i.address, i.op_str) for i in mpg if i.mnemonic.startswith("j") and i.operands
            and i.operands[0].type == IMM and i.operands[0].imm <= i.address]
mpg_ld = [i for i in mpg if i.mnemonic == "mov" and "qword ptr [rax + rbp]" in i.op_str]
ok7, bad7 = pins([(0x0022CA42, "add edi, 4"), (0x0022CA5D, "add edi, 8")])
check("V7", ok7 and not mpg_back and len(mpg_ld) == 1,
      "no VU microcode is embedded anywhere the layer reads: the MPG arm (0022CA3D-0022CA67) has no loop, loads "
      "exactly one qword of payload and advances the cursor 4 + 8 bytes whatever NUM says, so MPG carries one x64 "
      "pointer and there is no VU instruction stream in which a JAL / JR could be decoded; a VU JAL compiled to x64 "
      "is a direct call (V3: none reaches the 19) %s" % (bad7 or mpg_back or ""))
cls = {a: ("neither: a VU1 microprogram entry, address taken in code by %d lea(s) as a registrar's program "
           "argument, started by MSCAL through the program table" % len(forms[a])) for a in L19}
for a in L19:
    print("      %08X  %s; registrars %s" % (a, cls[a], " ".join(sorted({"%08X" % r for f, s, r in forms[a]}))))
check("V8", okv and not bad_br and not bad_b8 and not uncls and not va_q,
      "classification: of the 19, 0 are JAL / JR sub-program targets, 0 are data-referenced entries; all 19 are "
      "neither - they are registered microprogram entries (UQ-213's population), reached only by MSCAL")
TSV = os.path.join(DBROOT, "FFXII TZA", "17-Presentation-Rendering", "Legacy-PS2-GS", "members",
                   "vu1-region-functions.tsv")
subrows, rolemap = [], {}
for ln in open(TSV, encoding="utf-8"):
    p = ln.rstrip("\r\n").split("\t")
    if len(p) >= 4 and len(p[0]) == 8 and p[0] != "address":
        rolemap[int(p[0], 16)] = p[3]
        if p[3] == "sub-program":
            subrows.append(int(p[0], 16))
sub_called = [a for a in subrows if [1 for f, i in real_refs(a, a + 1) if kind(i) == "branch"]]
roles19 = collections.Counter(rolemap.get(a, "?") for a in L19)
check("V9", len(subrows) == 21 and not set(subrows) & set(L19) and len(sub_called) == 21
      and sum(v for k, v in roles19.items() if k.startswith("microprogram(registrar)")) == 9,
      "the region table's real sub-programs are a different set: its 21 'sub-program' rows are disjoint from the "
      "19 and every one has a direct-branch caller in the byte sweep; of the 19 rows, 9 already carry "
      "'microprogram(registrar)' beside the toucher role and 10 carry 'VU1-microprogram(VU-state-toucher)' (%s)"
      % dict(roles19))

print("FAILS %d" % fails)
