# ecx_review.py - FABLE's independent reader for ASTRA-REQ-FABLE-EFFECT-CONTEXT-EXCEPTION-DISPATCH (ASTRA b51b50668).
# Own raw-PE parse (struct only; not ASTRA's check.py, not pefile). For each of the three call continuations in 003B3CA0:
#   C1  the E8 bytes and rel32 targets at 003B3CE0 / 003B3CE7 / 003B3CFD;
#   C2  the .pdata RUNTIME_FUNCTION selected for the continuation (binary search, as RtlLookupFunctionEntry does; the
#       unwinder looks up ControlPc = the return address) and for continuation-1 (the call's last byte);
#   C3  walk UNWIND_INFO: version, flags, code count; follow UNW_FLAG_CHAININFO (4) to the chained RUNTIME_FUNCTION until a
#       record without CHAININFO; report whether that root has EHANDLER(1)/UHANDLER(2) and, if so, the handler RVA.
#       (x64: a chained record's flags are CHAININFO only; the language handler, if any, is read from the primary record.)
#   CONTROL+ the entry at 00121F40 must show a handler (ASTRA: flags 3, handler 00808BA8) - the reader can say "handler";
#   CONTROL- a chain cycle budget (8) and bounds checks refuse malformed chains (exercised on a private in-memory copy).
# Exit 0 only when every check ran; the verdict lines are printed, not inferred.
import struct, sys, hashlib
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
CERT = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
b = open(EXE, "rb").read()
sha = hashlib.sha256(b).hexdigest()
print("exe sha256", sha, "certified" if sha == CERT else "NOT CERTIFIED")
pe = struct.unpack_from("<I", b, 0x3C)[0]
nsec = struct.unpack_from("<H", b, pe + 6)[0]; opt = pe + 24; optsz = struct.unpack_from("<H", b, pe + 20)[0]
assert struct.unpack_from("<H", b, opt)[0] == 0x20B
exc_rva, exc_sz = struct.unpack_from("<II", b, opt + 112 + 3 * 8)   # data directory 3 = exception
secs = []
for i in range(nsec):
    o = opt + optsz + i * 40
    name = b[o:o + 8].rstrip(b"\0").decode(); vsz, va, rsz, raw = struct.unpack_from("<IIII", b, o + 8)
    secs.append((name, va, vsz, raw, rsz))


def off(rva):
    for name, va, vsz, raw, rsz in secs:
        if va <= rva < va + max(vsz, rsz):
            if rva - va >= rsz:
                raise ValueError("rva %X in virtual tail of %s" % (rva, name))
            return raw + rva - va
    raise ValueError("rva %X unmapped" % rva)


def sec_of(rva):
    return next((n for n, va, vsz, raw, rsz in secs if va <= rva < va + max(vsz, rsz)), "?")


print("exception directory rva %X size %X (%d entries) in %s" % (exc_rva, exc_sz, exc_sz // 12, sec_of(exc_rva)))
PD = [struct.unpack_from("<III", b, off(exc_rva) + 12 * i) for i in range(exc_sz // 12)]
assert all(PD[i][0] < PD[i + 1][0] for i in range(len(PD) - 1)), ".pdata not sorted"


def lookup(rva, pd=PD):
    lo, hi = 0, len(pd) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        s, e, u = pd[m]
        if rva < s: hi = m - 1
        elif rva >= e: lo = m + 1
        else: return pd[m]
    return None


def walk(rf, data=b, budget=8):
    """Follow CHAININFO from a RUNTIME_FUNCTION. Returns (chain list, root flags, handler rva or None)."""
    chain, seen = [], set()
    while True:
        if len(chain) >= budget: raise ValueError("chain budget exceeded")
        s, e, u = rf
        if u in seen: raise ValueError("chain cycle at unwind %X" % u)
        seen.add(u)
        o = off(u); v = data[o]; ver, fl = v & 7, v >> 3; cnt = data[o + 2]
        raw = data[o:o + 4 + 2 * ((cnt + 1) & ~1) + 12].hex()
        chain.append((s, e, u, ver, fl, cnt, raw))
        if ver not in (1, 2): raise ValueError("bad version %d at %X" % (ver, u))
        tail = o + 4 + 2 * ((cnt + 1) & ~1)
        if fl & 4:
            if fl & 3: raise ValueError("CHAININFO with handler flags at %X" % u)
            rf = struct.unpack_from("<III", data, tail)
            continue
        h = struct.unpack_from("<I", data, tail)[0] if fl & 3 else None
        return chain, fl, h


ok = True
calls = [(0x003B3CE0, 0x0024ED80), (0x003B3CE7, 0x003A9490), (0x003B3CFD, 0x0024ED80)]
for site, want in calls:
    o = off(site - BASE)
    op = b[o]; tgt = site + 5 + struct.unpack_from("<i", b, o + 1)[0]
    c1 = op == 0xE8 and tgt == want
    cont = site + 5
    rf = lookup(cont - BASE); rf1 = lookup(cont - 1 - BASE)
    c2 = rf is not None and rf == rf1
    chain, fl, h = walk(rf)
    print("C1 %08X E8 -> %08X %s | C2 continuation %08X selects [%X..%X) unwind VA %08X (cont-1 same: %s)" % (
        site, tgt, "PASS" if c1 else "FAIL", cont, rf[0], rf[1], rf[2] + BASE, rf == rf1))
    for s, e, u, ver, f, cnt, raw in chain:
        print("     C3 record [%X..%X) unwind VA %08X  version %d flags %d codes %d  raw %s" % (s, e, u + BASE, ver, f, cnt, raw))
    print("     root flags %d -> %s" % (fl, "handler VA %08X" % (h + BASE) if h is not None else "NO language handler"))
    ok &= c1 and c2 and h is None
# positive control
rf = lookup(0x00121F40 - BASE)
chain, fl, h = walk(rf)
pos = h is not None and h + BASE == 0x00808BA8
print("CONTROL+ 00121F40 selects [%X..%X): root flags %d handler %s -> %s" % (rf[0], rf[1], fl, "%08X" % (h + BASE) if h is not None else None, "PASS" if pos else "FAIL"))
# negative control: private copy, make the chained record point back at itself -> must be refused as a cycle
rf = lookup(0x003B3CE5 - BASE); o = off(rf[2]); cnt = b[o + 2]; tail = o + 4 + 2 * ((cnt + 1) & ~1)
priv = bytearray(b); struct.pack_into("<III", priv, tail, rf[0], rf[1], rf[2])
try:
    walk(rf, bytes(priv)); neg = False
except ValueError as ex:
    neg = "cycle" in str(ex)
print("CONTROL- private self-cycle refused:", "PASS" if neg else "FAIL")
# redirect control: private copy, chain to the 00121F40 entry -> the reader must now report its handler
priv = bytearray(b); struct.pack_into("<III", priv, tail, *lookup(0x00121F40 - BASE))
_, fl2, h2 = walk(rf, bytes(priv))
red = h2 is not None and h2 + BASE == 0x00808BA8
print("CONTROL redirect: private chain to 00121F40's record -> handler %s -> %s" % ("%08X" % (h2 + BASE) if h2 is not None else None, "PASS" if red else "FAIL"))
ok &= pos and neg and red and sha == CERT
print("RESULT", "ALL PASS - H2 at all three continuations (handler-free chained root)" if ok else "FAIL")
sys.exit(0 if ok else 1)
