"""What must a selector PROVE to call a body "unreferenced"? Derive the unwind set, do not guess it.

THE REFERENCE IMPLEMENTATION OF EVIDENCE-STANDARD 13be RULE 4. That addendum grants a bar for
claiming a body is unreachable, and rule 4 is "no 32-bit RVA outside a PARSED unwind set - never an
address window". This is the parser. Published because a bar stated only in prose is unenforceable.

It also reads a body list from Database/Tools/work/FABLE/noref_55.txt, which is GITIGNORED - point
it at any two-column <hex addr>	<size> file.

A first pass bucketed .rdata RVA32 hits by an address window (01D7-01D9) and reported 20 of the 55
as having references OUTSIDE unwind. THAT WAS THE WINDOW BEING TOO NARROW, not a finding: the hits
run 01D5xxxx-01DExxxx. Guessing a region is exactly the mistake this file exists to avoid.

So the unwind set is PARSED instead. .pdata is an array of RUNTIME_FUNCTION {begin, end, unwind},
each unwind RVA naming an UNWIND_INFO:

    +0  ver:3 flags:5      flags & 3 -> has an exception handler
    +1  prologue size
    +2  count of unwind codes
    +3  frame register / offset
    +4  count*2 bytes of codes, padded to 4
        then, if EHANDLER|UHANDLER: u32 handler RVA, then handler-specific data
        (for __C_specific_handler / __GSHandlerCheck that data is a SCOPE_TABLE of
         {begin, end, handler, target} RVA quads - every one of which is a function RVA)
    if CHAININFO: a RUNTIME_FUNCTION follows instead

Every RVA that appears inside .pdata or inside a parsed UNWIND_INFO is UNWIND METADATA and is banned
as evidence of use. Anything left is a real reference.
"""
import bisect
import collections
import io
import struct
import sys

EXE = 'D:/FFXII MP Mod/FFXII_TestClient1/x64/FFXII_TZA.exe'
sys.path.insert(0, 'Database/Tools/analysis-kit/gfz-scripts')
import check_dispositions as CD

d = io.open(EXE, 'rb').read()
pe = struct.unpack_from('<I', d, 0x3c)[0]
nsec = struct.unpack_from('<H', d, pe + 6)[0]
optsz = struct.unpack_from('<H', d, pe + 20)[0]
base = struct.unpack_from('<Q', d, pe + 24 + 24)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + i * 40
    nm = d[o:o + 8].rstrip(b'\0').decode('latin1')
    vsz, va, rsz, ptr = struct.unpack_from('<IIII', d, o + 8)
    secs.append((nm, va, vsz, ptr, rsz))


def off(rva, need=1):
    for _n, sva, vsz, ptr, rsz in secs:
        if sva <= rva < sva + max(vsz, rsz):
            o = ptr + (rva - sva)
            return o if (rva - sva) < rsz and o + need <= len(d) else None
    return None


pd = [s for s in secs if s[0] == '.pdata'][0]
_n, psva, pvsz, pptr, prsz = pd

# every FILE OFFSET that is part of unwind metadata
meta = set()
for i in range(0, prsz - 12 + 1, 12):
    meta.update(range(pptr + i, pptr + i + 12))
    uw = struct.unpack_from('<I', d, pptr + i + 8)[0]
    o = off(uw, 4)
    if o is None:
        continue
    ver_flags = d[o]
    flags = ver_flags >> 3
    ncodes = d[o + 2]
    end = o + 4 + ((ncodes + 1) & ~1) * 2
    meta.update(range(o, end))
    if flags & 0x4:                       # CHAININFO
        meta.update(range(end, end + 12))
        continue
    if flags & 0x3:                       # E/U HANDLER
        meta.update(range(end, end + 4))
        so = end + 4
        if so + 4 <= len(d):
            cnt = struct.unpack_from('<I', d, so)[0]
            if 0 < cnt < 4096 and so + 4 + cnt * 16 <= len(d):
                meta.update(range(so, so + 4 + cnt * 16))
print(".pdata entries              : %d" % (prsz // 12))
print("file bytes that are unwind  : %d" % len(meta))

sizes = CD.load_functions(None)
ks = sorted(sizes)
tset = {}
for line in io.open('Database/Tools/work/FABLE/noref_55.txt', encoding='utf-8'):
    p = line.split('\t')
    if len(p) >= 2:
        try:
            tset[int(p[0], 16)] = int(p[1])
        except ValueError:
            pass

real = collections.defaultdict(list)
inmeta = collections.Counter()
for nm, sva, vsz, ptr, rsz in secs:
    if nm == '.text':
        continue
    for i in range(0, max(0, rsz - 4), 4):
        fo = ptr + i
        r = base + struct.unpack_from('<I', d, fo)[0]
        if r in tset:
            if fo in meta:
                inmeta[r] += 1
            else:
                real[r].append((nm, base + sva + i))
        q = struct.unpack_from('<Q', d, fo)[0] if fo + 8 <= len(d) else 0
        if q in tset and fo not in meta:
            real[q].append((nm + '/q', base + sva + i))

print("\nof the %d bodies:" % len(tset))
print("   RVA32 hits accounted for as unwind metadata : %d bodies, %d hits"
      % (len(inmeta), sum(inmeta.values())))
print("   bodies with ANY reference outside unwind    : %d" % len(real))
for a in sorted(real):
    print("      %08X (%d B) : %s" % (a, tset[a], ', '.join(
        '%s@%08X' % (n, v) for n, v in real[a][:4])))
print("\ntop unwind-referenced of the 55 (an EH handler looks exactly like this):")
for a, c in inmeta.most_common(4):
    print("   %08X (%4d B) referenced by %d unwind records" % (a, tset[a], c))
