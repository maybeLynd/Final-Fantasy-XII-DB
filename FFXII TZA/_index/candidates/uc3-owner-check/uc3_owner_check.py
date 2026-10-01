"""UC-3 owner check (OPUS, 2026-09-27) of FABLE's uc3-libvpx-bytematch record, with a third, independent reader.

For EVERY routine uc3-blocks.tsv claims (name @address sizeB), the routine's bytes are taken from the pinned yasm
objects through this file's own COFF parsing (section table, symbol table incl. aux records, relocation table) and
compared with the shipping image at the claimed address. Relocated bytes are masked (4 bytes for REL32 / ADDR32NB /
SECREL kinds, 8 for ADDR64). The routine is taken from its symbol for the claimed size.
  O1 every claimed routine is found in exactly one object (a name defined twice must have identical bytes)
  O2 every claimed routine matches exactly outside relocation bytes
  O3 null: the same comparison at address + 0x40 matches no routine
  O4 the three non-libvpx blocks are the bytes the record says (FE at 00121E11; 90 + seven RVAs 4A4B..4B3C at 00124BFB;
     41 5E 41 5D 41 5C 5F C3 at 0015AE4A)
Usage: python uc3_owner_check.py OBJ_DIR [exe]
"""
import glob, os, re, struct, sys, hashlib

OBJ = sys.argv[1]
EXE = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/exe/FFXII_TZA.exe"
TSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uc3-libvpx-bytematch", "uc3-blocks.tsv")
BASE = 0x120000

d = open(EXE, "rb").read()
assert hashlib.sha256(d).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(nsec)]


def img(va, n):
    for vs, rva, rs, ro in secs:
        if BASE + rva <= va and va + n <= BASE + rva + rs:
            return d[ro + va - BASE - rva: ro + va - BASE - rva + n]
    return None


RELSZ = {0x1: 8, 0x2: 4, 0x3: 4, 0x4: 4, 0x5: 4, 0x6: 4, 0x7: 4, 0x8: 4, 0x9: 4, 0xA: 2, 0xB: 4}


def parse(path):
    b = open(path, "rb").read()
    mach, ns, ts, psym, nsym, optsz, ch = struct.unpack_from("<HHIIIHH", b, 0)
    strtab = psym + nsym * 18
    def nm(raw):
        if raw[:4] == b"\0\0\0\0":
            o = struct.unpack_from("<I", raw, 4)[0]; return b[strtab + o:b.index(b"\0", strtab + o)].decode()
        return raw.rstrip(b"\0").decode()
    sections = []
    for i in range(ns):
        h = 20 + optsz + i * 40
        name = nm(b[h:h + 8]); size, praw, prel, pln, nrel, nln, flags = struct.unpack_from("<IIIIHHI", b, h + 16)
        data = b[praw:praw + size] if praw else b"\0" * size
        mask = bytearray(size)
        for r in range(nrel):
            va, si, ty = struct.unpack_from("<IIH", b, prel + r * 10)
            for k in range(RELSZ.get(ty, 4)):
                if va + k < size: mask[va + k] = 1
        sections.append((name, data, mask))
    syms = {}
    i = 0
    while i < nsym:
        raw = b[psym + i * 18: psym + i * 18 + 18]
        value, secno, typ, cls, naux = struct.unpack_from("<IhHBB", raw, 8)
        if secno > 0 and cls in (2, 3, 6):
            syms.setdefault(nm(raw[:8]), []).append((secno - 1, value))
        i += 1 + naux
    return sections, syms


objs = [parse(p) for p in sorted(glob.glob(os.path.join(OBJ, "*.obj")))]
claims = []
for l in open(TSV, encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if c[0] == "block" or c[2].startswith("none"): continue
    for m in re.finditer(r"([A-Za-z_][\w]*) @([0-9A-F]{8}) (\d+)B", c[2]):
        claims.append((m.group(1), int(m.group(2), 16), int(m.group(3))))
claims = sorted(set(claims), key=lambda t: t[1])
fails = 0


def check(name, ok, det=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, det)); fails += not ok


found = ok = null_hits = matched = masked = 0; bad = []
for name, va, size in claims:
    cands = []
    for sections, syms in objs:
        for si, val in syms.get(name, []):
            sname, data, mask = sections[si]
            if val + size <= len(data): cands.append((data[val:val + size], bytes(mask[val:val + size])))
    uniq = {c[0] for c in cands}
    if not cands or len(uniq) != 1: bad.append((name, "objects %d / variants %d" % (len(cands), len(uniq)))); continue
    found += 1; code, mk = cands[0]
    im = img(va, size)
    same = im is not None and all(mk[i] or code[i] == im[i] for i in range(size))
    ok += same; matched += size - sum(mk); masked += sum(mk)
    if not same: bad.append((name, "mismatch at %08X" % va))
    shifted = img(va + 0x40, size)
    null_hits += shifted is not None and all(mk[i] or code[i] == shifted[i] for i in range(size))
check("O1 every claimed routine in exactly one object form", found == len(claims), "(%d of %d)" % (found, len(claims)))
check("O2 exact outside relocation bytes", ok == len(claims), "(%d routines; %d bytes compared, %d relocation bytes masked)" % (ok, matched, masked))
check("O3 null at +0x40 matches nothing", null_hits == 0, "(%d)" % null_hits)
o4 = img(0x121E11, 1) == b"\xFE" and img(0x121E10, 1) == b"\xEB" \
     and img(0x124BFB, 1) == b"\x90" and list(struct.unpack_from("<7I", img(0x124BFC, 28))) == [0x4A4B, 0x4A61, 0x4A78, 0x4AB5, 0x4AF1, 0x4B16, 0x4B3C] \
     and img(0x15AE4A, 8) == bytes.fromhex("415E415D415C5FC3")
check("O4 the three non-libvpx blocks", o4)
for x in bad[:10]: print("   ", x)
print("FAILS", fails); sys.exit(1 if fails else 0)
