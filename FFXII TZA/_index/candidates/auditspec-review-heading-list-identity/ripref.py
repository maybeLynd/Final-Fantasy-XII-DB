"""ripref.py - every instruction in .text whose rip-relative operand resolves to a target VA.
Candidate: any 4-byte window whose rel32, taken as ending 0..5 bytes before the instruction end,
hits the target; each candidate is confirmed by decoding the instruction from plausible starts
(ends exactly at the computed instruction end, op_str mentions rip). Pure Python, chunked
search on the rel32's high 16 bits. Also counts image-base-relative disp32 byte patterns.
Positive control: pass a target known to be referenced (e.g. 0x02EBEF88 from 003A949A).
Usage: python ripref.py 0x02EBEF88 [0x...]
"""
import struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"Database/Tools/work/exe/FFXII_TZA.exe"
pe = pefile.PE(EXE, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
text = next(s for s in pe.sections if s.Name.rstrip(b"\0") == b".text")
data = text.get_data()
tva = IB + text.VirtualAddress
md = Cs(CS_ARCH_X86, CS_MODE_64)
CH = 0x8000
for T in [int(a, 16) for a in sys.argv[1:]]:
    hits = set()
    for c0 in range(0, len(data) - 4, CH):
        c1 = min(c0 + CH, len(data) - 4)
        hi = set()
        for tail in range(6):
            for p in (c0, c1 - 1):
                d = (T - (tva + p + 4 + tail)) & 0xFFFFFFFF
                hi.add(d >> 16)
        for h in hi:
            pat = struct.pack("<H", h)
            q = data.find(pat, c0 + 2, c1 + 2 + 2)
            while q != -1 and q < c1 + 2:
                p = q - 2
                d = struct.unpack_from("<i", data, p)[0]
                for tail in range(6):
                    end = tva + p + 4 + tail
                    if end + d == T:
                        for back in range(9, 0, -1):  # earliest start first: keep the full (REX-prefixed) form
                            s = p - back
                            if s < 0:
                                continue
                            ins = next(md.disasm(data[s:s + 16], tva + s), None)
                            if ins and ins.address + ins.size == end and "rip" in ins.op_str:
                                hits.add((ins.address, ins.mnemonic, ins.op_str))
                                break
                q = data.find(pat, q + 1, c1 + 2 + 2)
    print("target %08X: %d rip-relative sites" % (T, len(hits)))
    for a, m, o in sorted(hits):
        print("  %08X  %s %s" % (a, m, o))
    print("  image-base-relative disp32 byte-pattern occurrences: %d" % data.count(struct.pack("<I", T - IB)))
