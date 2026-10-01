"""select_magic_static_guards.py - pure thread-safe magic-static
initialisation stubs: bodies whose ENTIRE call set is exactly the MSVC
guard pair plus the atexit wrapper -

    _Init_thread_header 008092FC
    _Init_thread_footer 0080929C
    atexit wrapper       00808B90

- and nothing else. The init payload is inlined (plain stores, no calls):
TLS index load (gs:[0x58] -> _tls_index slot), epoch compare against the
per-static guard cell, init stores, then footer + atexit registration.

Sizes vary 98..474 bytes because the payload is inlined; the call-set
signature is the form. Census-wide predicate scan is self-bounding:
every non-member match is already owned (StaticDescriptorSingleton and
the Phyre module families hold the form's other instances) or A-measured.

Usage: python select_magic_static_guards.py [--write]
"""
import io, os, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", "..", ".."))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
DB = os.path.join(REPO, "Database", "FFXII TZA")
OUT = os.path.join(ROOT, "magic-static-singleton-guards.tsv")

HDR, FTR, AX = 0x8092FC, 0x80929C, 0x808B90
SELF = "members/magic-static-singleton-guards.tsv"

sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as CD
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = io.open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + i * 40
    vsz, va, rsz, ptr = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, vsz, ptr, rsz))


def off(va):
    r = va - base
    for sva, vsz, ptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return ptr + (r - sva)
    return None


sizes = {}
for l in io.open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError):
        pass

md = Cs(CS_ARCH_X86, CS_MODE_64)

a_set, _eo, _ai, _da = CD.measure_a(DB, sizes)
dec = {}
for doc, parts in CD.parse_families(DB):
    if len(parts) < 5 or parts[1] not in ("B", "C", "D"):
        continue
    if parts[2] == SELF:
        continue
    try:
        for m in CD.read_members(doc, parts[2]):
            dec[m] = parts[0]
    except (IOError, OSError, ValueError):
        pass

hits, owned = [], []
for e, sz in sizes.items():
    o = off(e)
    if o is None:
        continue
    calls = {int(i.op_str, 16)
             for i in md.disasm(d[o:o + sz], e)
             if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x")
             and not (e <= int(i.op_str, 16) < e + sz)}
    if calls == {HDR, FTR, AX}:
        (owned if (e in dec or e in a_set) else hits).append(e)

print("pure-guard census hits: %d frontier + %d owned/A"
      % (len(hits), len(owned)))
own = collections.Counter(dec.get(e, "A") for e in owned)
print("   owned by:", ", ".join("%s x%d" % kv for kv in own.most_common()))
for e in sorted(hits):
    print("   %08X %dB" % (e, sizes[e]))

if "--write" in sys.argv:
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("# %d pure thread-safe magic-static singleton initialisation stubs.\n" % len(hits))
        fp.write("# Entire call set is exactly {_Init_thread_header 008092FC,\n")
        fp.write("# _Init_thread_footer 0080929C, atexit wrapper 00808B90}; the payload\n")
        fp.write("# is inlined stores only. Census-wide scan is self-bounding: all other\n")
        fp.write("# matches are owned (StaticDescriptorSingleton x13, Phyre modules x5)\n")
        fp.write("# or A-measured x3. Sizes 98-474B vary with the inlined payload.\n")
        fp.write("# address\tsize\n")
        for e in sorted(hits):
            fp.write("%08X\t%d\n" % (e, sizes[e]))
    print("wrote", OUT, len(hits), "rows")
else:
    print("dry run - pass --write to emit the TSV")
