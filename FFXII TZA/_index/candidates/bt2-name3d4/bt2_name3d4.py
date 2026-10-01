"""BT-2 (OPUS, 2026-09-27): CharacterRenderRecord +0x3D4 lookupName3D4 has no writer, and its one reader never runs.

  N1 the dirty pass 00427DE0 calls 0042F6C0 only when +0x290 bit 19 is clear and bit 18 is set (00427F44 mov eax,
     [rbx+0x290]; 00427F4A bt eax, 0x13 / jae 00427F94; 00427F94 bt eax, 0x12 / jae; 00427F9D call 0042F6C0). That call
     is the only rel32 call or jump to 0042F6C0 in .text.
  N2 0042F6C0 is the only reader of +0x3D4: 0042F7DD lea rdx, [rsi+0x3d4] -> 004218A0 (a by-name attach through
     00372760's strcmp), and 0042F7EF cmp byte ptr [rsi+0x3d4], bpl. It clears bit 18 (0042F84E and 0xfffbffff).
  N3 no store sets +0x290 bit 18. Every store to +0x290 (dword, the qword at +0x28C, the xmmword at +0x280 / +0x288) on
     a base shaped like this record (no displacement at or past 0x740, +0x284 addressed, +0x290 never accessed as a
     float) is classified: and / btr
     clear, an or-immediate must lack 0x40000, and every other store must be one of the sites fixed below with its
     reason. An or-immediate with 0x40000, a bts 0x12 or an unlisted site fails the check.
  N4 nothing stores to +0x3D4..+0x3F3, or takes an address in +0x3C0..+0x3F3 other than 0042F7DD, on such a base. The
     record is cleared whole by CharacterRenderRecord_ResetDefaults (0041F74B r8d = 0x740, 0041F754 memset).
Limits: static displacement forms only - a pointer to +0x290 or +0x3D4 formed by other arithmetic, rep stos/movs, or
code outside the image are not covered. Every check is re-run on a mutant.
Usage: python bt2_name3d4.py [exe]
"""
import copy, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUNCS_TSV = "Tools/work/graph/functions.tsv"
BASE = 0x120000

# N3: every CRR-shaped store to +0x290 in the image, with why it cannot set bit 18
N3_SITES = {
    0x00184E0E: "BootSubBlock0338 element ctor 00184CE0 (a 0x338-byte object, not this record)",
    0x0042F28A: "0042F250: and 0xfff3ffff clears bits 18-19, bts 0x14 sets bit 20",
    0x0042F3A0: "0042F310: and 0xffebffff clears bits 18 and 20, bts 0x13 sets bit 19",
    0x0042F4A4: "0042F3B0: and 0xffebffff clears bits 18 and 20, bts 0x13 sets bit 19",
    0x004FD41F: "004FD060: a qword field of another layout (+0x284 = 0x10000000, +0x278 = 0x47 constants)",
    0x005DF338: "005DEC50: copies +0x284..+0x290 from another object of the same shape (propagates, cannot originate)",
    0x007C0071: "007BFFA0: copies +0x284..+0x290 from another object of the same shape (propagates, cannot originate)",
}


def load():
    d = open(EXE, "rb").read()
    pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
    opt = struct.unpack_from("<H", d, pe + 20)[0]
    secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
    off = lambda v: next((v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs), None)
    sizes = {}
    for l in open(FUNCS_TSV, encoding="utf-8"):
        c = l.split("\t")
        try: sizes[int(c[0], 16)] = int(c[2])
        except (ValueError, IndexError): pass
    cs = Cs(CS_ARCH_X86, CS_MODE_64); funcs = {}
    for f, sz in sizes.items():
        if not (0x121000 <= f < 0x900000) or off(f) is None: continue
        funcs[f] = [[x.address, x.mnemonic, x.op_str] for x in cs.disasm(d[off(f):off(f) + sz], f)]
    text = [s for s in secs if s[1] == 0x1000][0]
    blob = d[text[3]:text[3] + text[2]]; tb = BASE + text[1]
    to6c0 = [tb + i for i in range(len(blob) - 5) if blob[i] in (0xE8, 0xE9)
             and tb + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == 0x42F6C0]
    return funcs, to6c0


def imm(src):
    try: return int(src, 0)
    except ValueError: return None


def crr_shaped(xs, base):
    # the record is 0x740 bytes, its +0x284 is the alive word, and its +0x290 is an integer flags word (never a float)
    disp = {int(v, 16) for a, m, o in xs for v in re.findall(r"\[%s \+ (0x[0-9a-f]+)\]" % base, o)}
    flt = any(m.startswith(("movss", "addss", "mulss", "subss")) and ("[%s + 0x290]" % base) in o for a, m, o in xs)
    return bool(disp) and max(disp) < 0x740 and 0x284 in disp and not flt


def check(funcs, to6c0):
    ins = {a: [m, o] for xs in funcs.values() for a, m, o in xs}
    def at(pc, m, o):
        assert ins.get(pc) == [m, o], (hex(pc), ins.get(pc), m, o)
    # N1
    at(0x427F44, "mov", "eax, dword ptr [rbx + 0x290]"); at(0x427F4A, "bt", "eax, 0x13"); at(0x427F4E, "jae", "0x427f94")
    at(0x427F94, "bt", "eax, 0x12"); at(0x427F98, "jae", "0x427fa4"); at(0x427F9D, "call", "0x42f6c0")
    assert to6c0 == [0x427F9D], ("N1 callers", [hex(a) for a in to6c0])
    # N2
    at(0x42F7DD, "lea", "rdx, [rsi + 0x3d4]"); at(0x42F7E7, "call", "0x4218a0")
    at(0x42F7EF, "cmp", "byte ptr [rsi + 0x3d4], bpl"); at(0x42F84E, "and", "dword ptr [rsi + 0x290], 0xfffbffff")
    at(0x41F74B, "mov", "r8d, 0x740"); at(0x41F754, "call", "0x861ec0")
    # N3 + N4
    n3, n3or, n4 = set(), set(), []
    for f, xs in funcs.items():
        for i, (a, mn, op) in enumerate(xs):
            m = re.match(r"(dword|qword|xmmword) ptr \[(r(?!sp)\w+) \+ (0x[0-9a-f]+)\], (.+)$", op)
            if m and mn not in ("cmp", "test", "bt"):
                w, base, dd, src = m.group(1), m.group(2), int(m.group(3), 16), m.group(4)
                covers290 = dd == 0x290 or (w == "qword" and dd == 0x28C) or (w == "xmmword" and dd in (0x280, 0x288))
                if covers290 and crr_shaped(xs, base):
                    if mn in ("and", "btr"): pass
                    elif mn == "or" and imm(src) is not None and not imm(src) & 0x40000: n3or.add(a)
                    elif mn in ("or", "bts") and imm(src) is not None and (mn == "bts" and imm(src) == 0x12 or mn == "or" and imm(src) & 0x40000):
                        raise AssertionError("N3 sets bit 18 at %x" % a)
                    else:
                        back = xs[max(0, i - 6):i]
                        assert not any(b[1] == "bts" and b[2].endswith(", 0x12") for b in back), ("N3 bts 0x12", hex(a))
                        n3.add(a)
                if (dd <= 0x3F3 and dd + {"dword": 4, "qword": 8, "xmmword": 16}[w] > 0x3D4) and crr_shaped(xs, base):
                    n4.append(a)
            m2 = re.match(r"(byte|word) ptr \[(r(?!sp)\w+) \+ (0x3[d-f][0-9a-f])\], ", op)
            if m2 and mn.startswith("mov") and 0x3D4 <= int(m2.group(3), 16) <= 0x3F3 and crr_shaped(xs, m2.group(2)):
                n4.append(a)
            m3 = re.match(r"r\w+, \[(r(?!sp|ip)\w+) \+ (0x3[c-f][0-9a-f])\]$", op)
            if mn == "lea" and m3 and 0x3C0 <= int(m3.group(2), 16) <= 0x3F3 and crr_shaped(xs, m3.group(1)) and a != 0x42F7DD:
                n4.append(a)
    assert n3 == set(N3_SITES), ("N3 site set", sorted(hex(a) for a in n3 ^ set(N3_SITES)))
    assert not n4, ("N4 writers", [hex(a) for a in n4])
    assert len(n3or) > 50, ("N3 or-immediate census too small", len(n3or))
    return len(n3or)


def main():
    funcs, to6c0 = load()
    k = check(funcs, to6c0); print("PASS N1-N4 (%d functions scanned; %d or-immediates without bit 18 and %d classified other stores to +0x290)" % (len(funcs), k, len(N3_SITES)))
    def patch(fs, pc, m, o):
        for xs in fs.values():
            for x in xs:
                if x[0] == pc: x[1], x[2] = m, o; return
    muts = {
        "N1 gate on bit 17": lambda fs, t: patch(fs, 0x427F94, "bt", "eax, 0x11"),
        "N1 a second caller": lambda fs, t: t.append(0x400000),
        "N2 name read elsewhere": lambda fs, t: patch(fs, 0x42F7DD, "lea", "rdx, [rsi + 0x3d8]"),
        "N3 or 0x40000": lambda fs, t: patch(fs, 0x2EDD93, "or", "dword ptr [rcx + 0x290], 0x40008"),
        "N3 setter sets 18": lambda fs, t: patch(fs, 0x42F39C, "bts", "eax, 0x12"),
        "N4 a name writer": lambda fs, t: patch(fs, 0x42F389, "mov", "byte ptr [rcx + 0x3d4], r8b"),
    }
    bad = 0
    for name, mut in muts.items():
        fs2, t2 = copy.deepcopy(funcs), list(to6c0); mut(fs2, t2)
        try:
            check(fs2, t2); print("MUTANT SURVIVED:", name); bad += 1
        except AssertionError:
            print("rejected:", name)
    print("FAILS", bad); sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
