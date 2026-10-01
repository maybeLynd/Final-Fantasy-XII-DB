"""ov31_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the OV-31 type-store review (2026-09-29).

Written without the package's ov31_title_asset.py or the kit's census tools: pefile + capstone only, over the shipping
image (sha256 asserted). Addresses are canonical VAs (image base 0x120000 included).

  A  every reference to the cell 02AEE4C0 (and 02AEE4C1..C7), image-wide over executable sections, in all three forms:
     rip-relative disp32 (found by raw arithmetic, then confirmed by decoding the instruction), image-base-relative
     disp32 (0x029CE4C0 as a displacement with a non-rip base), and absolute 64-bit / rva32 in any section.
     Controls: the sibling cell 02AEE4C8 must show its own references; a known single-caller count is re-derived.
  B  raw E8/E9 rel32 callers + abs64/rva32 slots of the handler/consumer bodies the page names.
  C  full linear decode of the own handler 00394070 and the consumer bodies; every memory operand whose base is the
     receiver (tracked from rcx at entry and from loads of the cell), and every type-area displacement +0xC0..+0xE0
     on ANY base in those bodies, with widths.
  D  the extent 0xD8 at 0039449F, the pool/heap branch in 00244F50, the msg-18 jump-table arm in 00582860.
"""
import hashlib, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
raw = open(EXE, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA, "image hash mismatch"
pe = pefile.PE(data=raw, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData,
         bool(s.Characteristics & 0x20000000)) for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True


def off(va):
    for n, v, vs, p, rs, x in SECS:
        if v <= va < v + min(vs, rs):
            return p + (va - v)
    return None


def rd(va, n):
    o = off(va)
    return raw[o:o + n]


def dis(start, end=None, count=None):
    o = off(start)
    size = (end - start) if end else 0x400
    out = []
    for i in md.disasm(raw[o:o + size], start):
        out.append(i)
        if count and len(out) >= count:
            break
    return out


def dis_func(start, limit=0x2000):
    """linear decode to the first ret/int3 run after which no earlier branch targets beyond (simple extent walk)."""
    o = off(start)
    ins = []
    far = start
    for i in md.disasm(raw[o:o + limit], start):
        ins.append(i)
        if i.group(1) or i.group(7):  # jump / branch_relative
            for op in i.operands:
                if op.type == 2:  # IMM
                    t = op.imm
                    if start <= t < start + limit and t > far:
                        far = t
        if i.mnemonic in ("ret", "int3") and i.address >= far:
            break
        if i.mnemonic == "jmp" and i.operands and i.operands[0].type == 2 and i.address >= far and \
                not (start <= i.operands[0].imm < start + limit):
            break
    return ins


TEXT = [(n, v, vs, p, rs) for n, v, vs, p, rs, x in SECS if x]
ALL = [(n, v, vs, p, rs) for n, v, vs, p, rs, x in SECS]
out = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out.append(s)


def mem_ops(i):
    for op in i.operands:
        if op.type == CS_OP_MEM:
            yield op.mem, op.size


def rip_refs(lo, hi):
    """instructions whose rip-relative memory/lea operand resolves into [lo,hi): raw disp32 arithmetic, then decode."""
    hits = []
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        L = len(blob)
        import array
        for k0 in range(4):
            n4 = (L - k0) // 4
            arr = array.array("i")
            arr.frombytes(blob[k0:k0 + 4 * n4])
            base = v + k0 + 4
            cands = [k0 + 4 * j for j, d in enumerate(arr) if lo - 4 <= base + 4 * j + d < hi]
            for k in cands:
              d = struct.unpack_from("<i", blob, k)[0]
              # instruction end is disp end (+0) or followed by imm8/imm16/imm32
              for tail in (0, 1, 2, 4):
                t = v + k + 4 + tail + d
                if lo <= t < hi:
                    # try every start 1..10 bytes before the disp; keep the LONGEST decode that ends exactly at the
                    # computed end and whose rip operand resolves into the window (a shorter decode drops a
                    # REX/prefix byte; an unrelated decode like `adc eax, imm32` has no rip operand)
                    best = None
                    for back in range(10, 0, -1):
                        s = v + k - back
                        ins = list(md.disasm(blob[k - back:k - back + 15], s, 1)) if k - back >= 0 else []
                        if not ins:
                            continue
                        i = ins[0]
                        if i.address + i.size != v + k + 4 + tail:
                            continue
                        for m, sz in mem_ops(i):
                            if m.base == X86_REG_RIP and lo <= i.address + i.size + m.disp < hi:
                                best = (i.address, i.mnemonic, i.op_str, sz)
                        if best:
                            break
                    if best:
                        hits.append(best)
    return sorted(set(hits))


def imagebase_refs(lo, hi):
    """disp32 == target-IB with a non-rip base register (the image-base-relative form)."""
    hits = []
    for tgt in range(lo, hi):
        pat = struct.pack("<I", tgt - IB)
        for n, v, vs, p, rs in TEXT:
            blob = raw[p:p + min(vs, rs)]
            k = blob.find(pat)
            while k >= 0:
                for back in range(1, 9):
                    if k - back < 0:
                        continue
                    ins = list(md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                    if ins and ins[0].address < v + k < ins[0].address + ins[0].size:
                        i = ins[0]
                        for m, sz in mem_ops(i):
                            if m.base not in (X86_REG_RIP, X86_REG_INVALID) and m.disp == tgt - IB:
                                hits.append((i.address, i.mnemonic, i.op_str, sz))
                k = blob.find(pat, k + 1)
    return sorted(set(hits))


def data_refs(tgt):
    """abs64 and rva32 occurrences of a VA in every section's raw data."""
    res = {"abs64": [], "rva32": []}
    for kind, pat in (("abs64", struct.pack("<Q", tgt)), ("rva32", struct.pack("<I", tgt - IB))):
        for n, v, vs, p, rs in ALL:
            blob = raw[p:p + min(vs, rs)]
            k = blob.find(pat)
            while k >= 0:
                res[kind].append("%08X(%s%s)" % (v + k, n, "" if (v + k) % 4 == 0 else ",unaligned"))
                k = blob.find(pat, k + 1)
    return res


def rel32_callers(tgt):
    res = []
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        for opc in (0xE8, 0xE9):
            k = blob.find(bytes([opc]))
            while k >= 0 and k + 5 <= len(blob):
                d = struct.unpack_from("<i", blob, k + 1)[0]
                if v + k + 5 + d == tgt:
                    ins = list(md.disasm(blob[k:k + 5], v + k, 1))
                    ok = bool(ins) and ins[0].size == 5
                    res.append("%08X %s%s" % (v + k, "call" if opc == 0xE8 else "jmp", "" if ok else "(nodecode)"))
                k = blob.find(bytes([opc]), k + 1)
    return res


def jcc_callers(tgt):
    res = []
    for n, v, vs, p, rs in TEXT:
        blob = raw[p:p + min(vs, rs)]
        k = blob.find(b"\x0f")
        while k >= 0 and k + 6 <= len(blob):
            if 0x80 <= blob[k + 1] <= 0x8F:
                d = struct.unpack_from("<i", blob, k + 2)[0]
                if v + k + 6 + d == tgt:
                    res.append("%08X jcc" % (v + k))
            k = blob.find(b"\x0f", k + 1)
    return res


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "ABCD"
    CELL = 0x02AEE4C0
    if "A" in part:
        say("== A. references to the cell 02AEE4C0..C7 (and control 02AEE4C8..CF)")
        for lo, tag in ((CELL, "cell"), (CELL + 8, "control-sibling")):
            r = rip_refs(lo, lo + 8)
            b = imagebase_refs(lo, lo + 8)
            say("  %s %08X: rip %d, image-base %d" % (tag, lo, len(r), len(b)))
            for h in r + b:
                say("    %08X  %s %s  (%dB)" % h)
            say("   data:", data_refs(lo))
    if "B" in part:
        say("== B. raw callers (E8/E9 rel32, 0F 8x jcc) and abs64/rva32 slots")
        for f in (0x00394070, 0x00394400, 0x00394520, 0x00394500, 0x00394460, 0x00394530, 0x003939B0, 0x00394130,
                  0x00511EA0, 0x00511EC0, 0x00511F90):
            say("  %08X  rel32: %s  jcc: %s  data: %s" % (f, rel32_callers(f), jcc_callers(f), data_refs(f)))
        say("  control 00244F00 rel32 count:", len(rel32_callers(0x00244F00)))
    if "C" in part:
        say("== C. linear decode: type-area (+0xB8..+0xE8) displacements on any base, all bases, widths")
        for f in (0x00394070, 0x003939B0, 0x00394400, 0x00394460, 0x00394500, 0x00394520, 0x00394530):
            ins = dis_func(f)
            say("  -- %08X .. %08X (%d insns)" % (f, ins[-1].address + ins[-1].size, len(ins)))
            for i in ins:
                for m, sz in mem_ops(i):
                    if m.base != X86_REG_RIP and 0xB8 <= m.disp < 0xE8:
                        say("    %08X  %-6s %-40s %dB" % (i.address, i.mnemonic, i.op_str, sz))
    if "D" in part:
        say("== D. anchors")
        for a in (0x0039449F, 0x00244F77, 0x00244F90, 0x00244FB2, 0x00582899, 0x005828A0, 0x00582E81, 0x00582EAC,
                  0x00582EB5, 0x0024505A, 0x00394161, 0x00511EC4, 0x00393A98, 0x00393AA5, 0x0039450D, 0x003940E3,
                  0x003940FC, 0x00394033, 0x00394097, 0x00394050, 0x003940A8, 0x003940B9, 0x0039435C, 0x0039436A,
                  0x003944E0):
            i = dis(a, count=1)[0]
            say("  %08X  %s %s" % (i.address, i.mnemonic, i.op_str))
    open(sys.argv[2] if len(sys.argv) > 2 else "ov31_indep.out", "w").write("\n".join(out) + "\n")
