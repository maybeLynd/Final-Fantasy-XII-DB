"""sd62o_reloc.py - which qwords of 01F2E780..01F2E7BF carry a DIR64 base relocation (link-time pointers), lane loader."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
import pefile, struct

pe = pefile.PE(data=T.raw, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_BASERELOC"]])
cells = [0x01F2E780 + 8 * k for k in range(8)]
rel = {T.IB + e.rva for b in pe.DIRECTORY_ENTRY_BASERELOC for e in b.entries if e.type == 10 and T.IB + e.rva in cells}
for c in cells:
    print("%08X  q=%016X  DIR64 %s" % (c, struct.unpack("<Q", T.rd(c, 8))[0], c in rel))
