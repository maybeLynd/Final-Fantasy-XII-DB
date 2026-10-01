"""Independent AB-4 check: read the two namespace-21 arrays straight from the file image, section-aware,
and classify each slot by the string it points at. Also count every NUL-terminated string in .rdata
ending in .ard (case-insensitive) with a scan that does not depend on the arrays."""
import struct, re, pefile
EXE = r"Database/Tools/work/exe/FFXII_TZA.exe"
pe = pefile.PE(EXE, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
raw = open(EXE, "rb").read()
secs = [(s.Name.rstrip(b"\0").decode(), IB + s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData) for s in pe.sections]
def rd(va, n):
    for name, st, vs, rp, rs in secs:
        if st <= va < st + vs:
            o = va - st
            if o + n <= rs:
                return raw[rp + o: rp + o + n]
            return b"\0" * n  # virtual tail
    raise ValueError(hex(va))
def cstr(va):
    out = b""
    while len(out) < 300:
        c = rd(va + len(out), 1)
        if c == b"\0": break
        out += c
    return out.decode("latin-1")
def sec(va):
    return next((n for n, st, vs, rp, rs in secs if st <= va < st + vs), None)
for base in (0x01E0CFA0, 0x01EDC280):
    print("array %08X in %s" % (base, sec(base)))
    first = None; ard = fpk = other = 0; cross = 0; strs = set(); lastnz = None
    for i in range(0, 700):
        p = struct.unpack("<Q", rd(base + 8 * i, 8))[0]
        if p == 0:
            continue
        if sec(p) not in (".rdata", ".data"):
            print("  slot %d -> %X non-string section %s; stop" % (i, p, sec(p))); break
        s = cstr(p)
        if first is None: first = i
        lastnz = i
        l = s.lower()
        if l.endswith(".ard"):
            ard += 1; strs.add(p); cross += (i % 2 != 0)
        elif l.endswith(".fpk"):
            fpk += 1; cross += (i % 2 != 1)
        else:
            other += 1
            if other < 4: print("  slot %d other: %r" % (i, s))
    print("  first non-null %s last non-null %s; .ard %d .fpk %d other %d parity-crossovers %d" % (first, lastnz, ard, fpk, other, cross))
    globals().setdefault("ALL", set()).update(strs)
# independent .ard string census in .rdata
n, st, vs, rp, rs = next(x for x in secs if x[0] == ".rdata")
blob = raw[rp: rp + rs]
starts = set()
for m in re.finditer(rb"[\x20-\x7e]{1,200}?\.ard\x00", blob, re.I):
    # walk back to the string start (previous NUL)
    e = m.end() - 1
    s0 = blob.rfind(b"\0", 0, e) + 1
    starts.add(st + s0)
print(".ard strings in .rdata: %d; reached by the two arrays: %d; unreached: %s" % (len(starts), len(starts & ALL), [cstr(x) for x in sorted(starts - ALL)][:10]))
