"""PhyreClassDescriptor +0xFC bits 4 (0x10) and 5 (0x20) have no reader (OPUS, 2026-09-27).

  B1 every non-write access of [reg + 0xFC] in the descriptor code range 0x5E0000..0x6A0000 is classified: byte / dword
     tests with masks 1, 2, 4, 8 or 0x40000000; dword loads whose register is then tested with bt 0x1C / 0x1E, a sign
     test, 'and 0x7FFFFFF' followed by tests of bits 0, 1 and 3 (00639A60), 'and 0x8000000' (00639C80); byte loads reduced
     to bit 0 (0063ABF0, 0063C910); one copy of the word to another descriptor (00692290); and loads on bases that are not
     descriptors (fields past +0x100: 00625830, 00628B40, 0065D720). No test reaches bit 4 or 5.
  B2 image-wide, the only tests of 0x10 / 0x20 at +0xFC (00280B70, 00284450, 002845E0, 00284C90) are on bases that
     read +0x98 / +0x9A / +0x9C or +0xAC8 - not a 0x100-byte descriptor.
  POSITIVE CONTROL: the scan finds the known readers of bits 1 (0063954C), 3 (0063A99A) and 30 (00639A49).
Usage: python desc_flags_bits45.py [exe] [functions.tsv]
"""
import re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUN = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/graph/functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next((v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs), None)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
sizes = {}
for l in open(FUN, encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
fails = 0


def check(name, ok, det=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, det)); fails += not ok


def dis(f):
    o = off(f)
    return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[o:o + sizes[f]], f)] if o is not None else []


def wordish_9x(xs, base):
    # a descriptor's +0x90..+0x9F is methodList (two pointers): a byte or word access there means the base is not one
    return any(re.search(r"(byte|word) ptr \[%s \+ 0x9[0-9a-f]\]" % base, op) for a, mn, op in xs)


def maxdisp(xs, base):
    v = [int(m, 16) for a, mn, op in xs for m in re.findall(r"\[%s \+ (0x[0-9a-f]+)\]" % base, op)]
    return max(v) if v else 0


tested = set(); unexplained = []; positive = set()
for f in sorted(sizes):
    if not (0x5E0000 <= f < 0x6A0000): continue
    xs = dis(f)
    for i, (a, mn, op) in enumerate(xs):
        m = re.search(r"\[(r(?!sp)\w+) \+ 0xfc\]", op)
        if not m: continue
        base = m.group(1); first = op.split(",")[0].strip()
        if first.startswith(("byte ptr", "dword ptr", "word ptr", "qword ptr")) and mn in ("mov", "and", "or", "bts", "btr"): continue  # writes
        if maxdisp(xs, base) >= 0x100: continue  # not a descriptor
        if mn == "test":
            mask = int(op.split(", ")[-1], 0); tested.add(mask)
            if a in (0x63954C, 0x63A99A, 0x639A49): positive.add(a)
            continue
        if mn.startswith("movss"): continue  # a float view of +0xFC is another type's field, not the flags word
        reg = first
        fam = {"eax": "eax|al", "ebx": "ebx|bl", "ecx": "ecx|cl", "edx": "edx|dl"}.get(reg) or (re.sub(r"[dwb]$", "", reg) + "[dwb]?")
        uses = [(y[1], y[2]) for y in xs[i + 1:i + 60] if re.search(r"\b(%s)\b" % fam, y[2])]
        masks = set()
        shift = 0
        for mn2, op2 in uses:
            if mn2 == "shr": shift = int(op2.split(", ")[-1], 0)
            if mn2 in ("test", "and") and re.search(r", (0x[0-9a-f]+|\d+)$", op2) and not op2.startswith(("byte ptr", "dword ptr")):
                masks.add(int(op2.split(", ")[-1], 0) << shift)
            if mn2 == "bt": masks.add(1 << int(op2.split(", ")[-1], 0))
        if a == 0x6924A8: continue  # a whole-word copy to another descriptor (00692290)
        if not masks and not any(mn2 in ("test", "js") for mn2, _ in uses): unexplained.append(a)
        tested |= masks
bits45 = any(m & 0x30 for m in tested if m not in (0x7FFFFFF,))
check("B1 no descriptor-code reader tests bit 4 or 5", not bits45 and not unexplained,
      "(masks seen: %s; unexplained loads: %s)" % (sorted(hex(m) for m in tested), [hex(a) for a in unexplained]))
check("POSITIVE CONTROL: the bit-1, bit-3 and bit-30 readers are found", positive == {0x63954C, 0x63A99A, 0x639A49})
b2 = []
for f in sorted(sizes):
    if not (0x121000 <= f < 0x900000): continue
    xs = dis(f)
    for a, mn, op in xs:
        m = re.match(r"(byte|dword) ptr \[(r\w+) \+ 0xfc\], (0x[0-9a-f]+|\d+)$", op)
        if mn == "test" and m and int(m.group(3), 0) & 0x30: b2.append((f, a, maxdisp(xs, m.group(2)), wordish_9x(xs, m.group(2))))
check("B2 image-wide 0x10 / 0x20 tests at +0xFC are on non-descriptors",
      sorted(a for f, a, md, w in b2) == [0x280BD6, 0x284525, 0x28471B, 0x284CE0] and all(md >= 0x100 or w for f, a, md, w in b2),
      str([("%08X" % a, hex(md), w) for f, a, md, w in b2]))
print("FAILS", fails); sys.exit(1 if fails else 0)
