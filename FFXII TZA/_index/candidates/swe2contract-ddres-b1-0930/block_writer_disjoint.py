"""block_writer_disjoint.py - test the console-tunes page's unverified claim that 001F0AD0's 144 movss store
addresses into the render-settings block 02CB7FD0..02CB8438 are disjoint from the 29 named offsets the two
scene-config loaders (001C7940, 001C3D50) store there. SWE2-CONTRACT, 2026-09-30. Static. Reads only.

Method: linear-sweep each body (extent from Tools/work/graph/functions.tsv body_bytes) with capstone and collect every
rip-relative memory WRITE whose target lies in the block. Controls (each must hold, else exit 1):
  C1 001F0AD0 yields exactly 144 distinct movss-store targets in the block (published count, OPUS pass 1 2026-09-12);
  C2 the two loaders together yield exactly 29 distinct block targets (published: 48 store sites -> 29 offsets);
  C3 the loaders' movss store sites number 48 (published: 48 store sites; the page's per-function site column,
     30 + 19, also counts one integer `mov` store in 001C7940, reported below).
  C4 positive control for the intersection itself: the 29 meet the console dispatcher 001D1660's block write
     targets in exactly 21 places (published: '29 named in section 4, 21 of them console-arm addresses').
Then prints the intersection of the 144 and the 29.
"""
import io, os, struct, sys
import capstone

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(DB, "..", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(DB, "..", "Tools", "work", "graph", "functions.tsv")
BASE, LO, HI = 0x120000, 0x02CB7FD0, 0x02CB8438 + 4


def load():
    pe = io.open(EXE, "rb").read()
    e = struct.unpack_from("<I", pe, 0x3C)[0]
    nsec = struct.unpack_from("<H", pe, e + 6)[0]
    opt = struct.unpack_from("<H", pe, e + 20)[0]
    secs = []
    for i in range(nsec):
        o = e + 24 + opt + 40 * i
        vsz, va, rsz, rptr = struct.unpack_from("<IIII", pe, o + 8)
        secs.append((BASE + va, rsz, rptr))
    def at(addr, n):
        for va, rsz, rptr in secs:
            if va <= addr < va + rsz:
                return pe[rptr + addr - va: rptr + addr - va + n]
    return at


def extents():
    ext = {}
    for line in io.open(FUNCS, encoding="utf-8").read().splitlines()[1:]:
        c = line.split("\t")
        ext[int(c[0], 16)] = int(c[2])
    return ext


def writes(at, entry, size, md, mnem_filter=None):
    out = []
    for ins in md.disasm(at(entry, size), entry):
        if not ins.operands or ins.operands[0].type != capstone.x86.X86_OP_MEM:
            continue
        m = ins.operands[0].mem
        if m.base != capstone.x86.X86_REG_RIP or m.index != 0:
            continue
        tgt = ins.address + ins.size + m.disp
        if not (LO <= tgt < HI):
            continue
        if ins.mnemonic.startswith(("cmp", "test", "ucomis", "comis")):
            continue
        if len(ins.operands) < 2:
            continue
        if mnem_filter and ins.mnemonic not in mnem_filter:
            continue
        out.append((ins.address, ins.mnemonic, tgt))
    return out


def main():
    at, ext = load(), extents()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    fails = 0
    w = writes(at, 0x001F0AD0, ext[0x001F0AD0], md, ("movss",))
    s144 = set(t for _, _, t in w)
    c1 = len(s144) == 144
    loader_sites = writes(at, 0x001C7940, ext[0x001C7940], md) + writes(at, 0x001C3D50, ext[0x001C3D50], md)
    s29 = set(t for _, _, t in loader_sites)
    movss_sites = [x for x in loader_sites if x[1] == "movss"]
    c2, c3 = len(s29) == 29, len(movss_sites) == 48
    for ok, name, got in ((c1, "C1 001F0AD0 movss block targets == 144", len(s144)),
                          (c2, "C2 loader block targets == 29", len(s29)),
                          (c3, "C3 loader movss block store sites == 48", len(movss_sites))):
        print("%s  %s: %d" % ("PASS" if ok else "FAIL", name, got))
        fails += not ok
    for a, m, t in loader_sites:
        if m != "movss":
            print("  non-movss loader store: %08X %s -> +0x%03X" % (a, m, t - LO))
    con = set(t for _, _, t in writes(at, 0x001D1660, ext[0x001D1660], md))
    c4 = len(con & s29) == 21
    print("%s  C4 the 29 meet 001D1660's block write targets in 21: %d" % ("PASS" if c4 else "FAIL", len(con & s29)))
    fails += not c4
    inter = sorted(s144 & s29)
    print("intersection of the 144 and the 29: %d" % len(inter))
    for t in inter:
        print("  +0x%03X (%08X)" % (t - LO, t))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
