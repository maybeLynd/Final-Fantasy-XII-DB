"""sd41_stamp_digits.py - does anything in the image give the two save stamps a meaning? (OPUS, 2026-09-30; register SD-41)

Asserts, over the certified image (Database/Tools/analysis-kit/gfz-scripts/retool.py):
  F1  every occurrence of each constant's bytes in the whole file is an instruction immediate, and they are exactly the
      four known uses (getter 002EF2A0 for 0x20050223; getter 00235E90, the stamp store 002370DF and the equality test
      00233C4D for 0x05071901)
  F2  no instruction uses either value in any other form (a scan of every catalogued function)
  F3  no string in the file spells either value as a date or a digit run
Prints PASS/FAIL per fact and `FAILS n` last.
"""
import os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402
import pefile  # noqa: E402

R = T.R
raw = open(R.b.EXE, "rb").read()
pe = pefile.PE(R.b.EXE, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def va(off):
    for s in pe.sections:
        if s.PointerToRawData <= off < s.PointerToRawData + s.SizeOfRawData:
            return base + s.VirtualAddress + off - s.PointerToRawData
    return None


KNOWN = {0x20050223: {0x002EF2A0}, 0x05071901: {0x00235E90, 0x002370DF, 0x00233C4D}}
ok1, where = True, {}
for v, sites in KNOWN.items():
    offs = [m.start() for m in re.finditer(re.escape(struct.pack("<I", v)), raw)]
    got = set()
    for o in offs:
        a = va(o)
        # the immediate sits inside the instruction starting at one of the known sites (within 12 bytes)
        s = next((x for x in sites if a is not None and x <= a < x + 12), None)
        got.add(s)
    where[hex(v)] = sorted("%08X" % x if x else "OTHER" for x in got)
    ok1 = ok1 and len(offs) == len(sites) and got == sites
check("F1", ok1, "file occurrences resolved to instructions: %s" % where)
uses = []
for f, n in T.sizes().items():
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        if re.search(r"0x20050223|0x5071901\b", i.op_str):
            uses.append(i.address)
check("F2", sorted(uses) == sorted({0x002EF2A0, 0x00235E90, 0x002370DF, 0x00233C4D}),
      "instructions using either value: %s" % ["%08X" % x for x in sorted(uses)])
pats = [rb"2005[-/._ ]?0?2[-/._ ]?23", rb"20050223", rb"05[-/._ ]?07[-/._ ]?19", rb"05071901",
        "2005".encode("utf-16-le") + rb".{0,4}" + "23".encode("utf-16-le")]
hits = {p: len(re.findall(p, raw)) for p in pats}
check("F3", not any(hits.values()), "date / digit strings in the file: %s" % {k.decode("latin1", "replace")[:24]: v for k, v in hits.items()})
print("FAILS %d" % fails)
