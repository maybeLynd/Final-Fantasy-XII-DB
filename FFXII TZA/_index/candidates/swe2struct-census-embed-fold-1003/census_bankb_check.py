"""census_bankb_check.py [census.tsv] - every bank-B (r8 / rbx = r8) SystemStopRecord access of the builder 00227680 must be in
the record census (SWE2-STRUCT, 2026-10-03). The set is decoded from the shipping image, not read from the census: each
instruction in 00227680..00227CD2 whose memory operand is [r8 (+k)] or [rbx (+k)] (rbx = r8 from 0022769C, written once
before the epilogue pops). FAILS n = sites missing, or present at a different offset. Before the element-fold fix in
gen_route_seeded_census.py the census held none of the 82."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402
DEFAULT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "00-Engine-Core-Runtime", "System-Stop-Registry",
                                        "system-stop-record-accesses.tsv"))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    d, off = fp.load_image()
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    want = {}
    for i in md.disasm(d[off(0x00227680):off(0x00227CD3)], 0x00227680):
        m = re.search(r"\[(r8|rbx)(?: \+ (0x[0-9a-f]+|\d+))?\]", i.op_str)
        if m and i.address >= 0x0022769F:
            g = m.group(2)
            want["%08X" % i.address] = int(g, 16) if g and g.startswith("0x") else int(g or 0)
    have = {}
    for l in open(path, encoding="utf-8").read().splitlines()[1:]:
        c = l.split("\t")
        if len(c) > 4 and c[0] == "00227680":
            have[c[2]] = int(c[3], 16)
    miss = [s for s in want if have.get(s) != want[s]]
    print("bank-B sites decoded: %d; in census at the right offset: %d" % (len(want), len(want) - len(miss)))
    for s in miss[:10]:
        print("  missing", s, hex(want[s]))
    print("FAILS", len(miss))
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
