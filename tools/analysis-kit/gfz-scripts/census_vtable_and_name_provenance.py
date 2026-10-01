"""Find a class vtable from its RTTI name, census its virtual methods, and CLASSIFY THE NAME.

For a type with NO pointer cell - a Phyre class the cluster system creates - there is no
global to track. The receiver-proven entry point is instead the VTABLE: every function in
a class's vtable is entered with `this` in rcx by definition, so [rcx + d] inside it is a
field of that class (or of a base).

    python vtable_census.py <MangledOrPlainName> <extentHex>   e.g. PScheduler 0x2F8

Finds the type descriptor whose name matches, finds every complete-object locator that
points at it, takes the vtable as locator_address + 8, enumerates the slots, and counts
[rcx + d] in each slot body until rcx is redefined.

LIMITS, which any negative from this must carry:
  * only virtual methods are covered - a non-virtual member called directly is not in a
    vtable and is invisible here;
  * a slot shared by several classes (the compiler folds identical bodies) attributes
    that body's accesses to every class that lists it - so a shared destructor or an
    empty stub can import foreign offsets. Slots appearing in many vtables are reported.
  * `lea` is not an access, and index-register accesses are skipped, as in the sibling
    census_receiver_fixpoint.py.
"""
import struct, collections, sys, os, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RCX

NAME = sys.argv[1]
EXTENT = int(sys.argv[2], 16)
HERE = os.path.dirname(os.path.abspath(__file__))
import kit_paths as KP
REPO = KP.ROOT
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FNS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
BASE = 0x120000

d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + optsz + i * 40
    vsz, va, rawsz, raw = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, vsz, raw, rawsz))
def fo(v):
    r = v - BASE
    for va, vsz, raw, rawsz in secs:
        if va <= r < va + vsz and r - va < rawsz:
            return raw + (r - va)
def va_of(off):
    for va, vsz, raw, rawsz in secs:
        if raw <= off < raw + rawsz:
            return BASE + va + (off - raw)

sizes = {}
for ln in open(FNS, encoding="utf-8", errors="replace"):
    c = ln.rstrip("\n").split("\t")
    if len(c) > 2 and len(c[0]) == 8 and c[2].isdigit():
        sizes[int(c[0], 16)] = int(c[2])

# 1. the type descriptor: an RTTI name string preceded by two pointers
pat = (".?AV" + NAME + "@").encode() if not NAME.startswith(".?A") else NAME.encode()
tds = []
for m in re.finditer(re.escape(pat), d):
    td_off = m.start() - 16
    td_va = va_of(td_off)
    if td_va:
        tds.append((td_va, d[m.start():m.start()+160].split(b"\0")[0].decode(errors="replace")))
if not tds:
    # A MISSING .?AV IS NOT A MISSING CLASS, and saying so was my error: I published
    # "no type descriptor anywhere in the image" for PTextureCubeMapD3D11 from this one
    # search, and SWE2-FRONTIER's ruling corrected it. So before reporting anything, look
    # for the other provenances their ruling names.
    tmpl = sorted({m.group().decode(errors="replace")
                   for m in re.finditer(rb"\.\?AV\?\$[A-Za-z0-9_@?$]{0,120}V" +
                                        re.escape(NAME.encode()) + rb"@[A-Za-z0-9_@?$]{0,120}", d)})
    bare = re.search(rb"\x00" + re.escape(NAME.encode()) + rb"\x00", d) is not None
    if tmpl or bare:
        print("NO DIRECT MSVC DESCRIPTOR for %s - but the class IS NAMED in the image, so this"
              % NAME)
        print("is NOT an absence. Provenance is PHYRE REFLECTION (SWE2-FRONTIER ruling,")
        print("_types/README.md, 2026-09-21):")
        if bare:
            print("   bare reflection name string present")
        for t in tmpl[:6]:
            print("   %s" % t[:110])
        print("A class named only through descriptor-template arguments has no RTTI locator of")
        print("its own, so THIS TOOL CANNOT FIND IT A VTABLE - which is a limit of the anchor,")
        print("not evidence about the type. Census it another way.")
    else:
        print("%s: no MSVC descriptor, no descriptor-template mention, no bare name string."
              % NAME)
        print("That is the only combination that supports a store-assigned name.")
    sys.exit(1)
print("type descriptor(s):")
for va, nm in tds:
    print("   %08X  %s" % (va, nm))

# 2. locators whose pTypeDescriptor RVA matches, vtable = locator + 8
vtables = []
for td_va, nm in tds:
    rva = (td_va - BASE).to_bytes(4, "little")
    for m in re.finditer(re.escape(rva), d):
        loc_off = m.start() - 12
        loc_va = va_of(loc_off)
        if loc_va is None: continue
        try:
            sig, offs, cd, ptd, pcd = struct.unpack_from("<IIIII", d, loc_off)
        except struct.error:
            continue
        if sig not in (0, 1) or ptd != td_va - BASE: continue
        # The vtable does NOT start at the locator. The qword IMMEDIATELY BEFORE a vtable
        # holds a pointer to that class's complete-object locator, so the vtable is found
        # by searching for the locator's ADDRESS and stepping 8 bytes past it.
        for mm in re.finditer(re.escape(loc_va.to_bytes(8, "little")), d):
            vt_va = va_of(mm.start() + 8)
            o = fo(vt_va) if vt_va else None
            if o is None: continue
            slots = []
            for i in range(120):
                p = struct.unpack_from("<Q", d, o + i * 8)[0]
                if not (0x120000 <= p < 0x900000): break
                slots.append(p)
            if slots: vtables.append((vt_va, offs, slots))
print("vtables found: %d" % len(vtables))

md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
acc = collections.Counter(); sites = collections.defaultdict(set)
allslots = collections.Counter()
for vt, offs, slots in vtables:
    print("   vtable %08X (base offset %d): %d slots" % (vt, offs, len(slots)))
    for s in slots: allslots[s] += 1
for fn in allslots:
    n = sizes.get(fn); o = fo(fn)
    if not n or o is None or n > 60000: continue
    live = True
    for ins in md.disasm(d[o:o + n], fn):
        if not live: break
        try: _, written = ins.regs_access()
        except Exception: written = ()
        if ins.mnemonic != "lea":
            for op in ins.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RCX and op.mem.index == 0:
                    if 0 <= op.mem.disp < EXTENT:
                        acc[(op.mem.disp, op.size)] += 1
                        sites[(op.mem.disp, op.size)].add("%08X" % ins.address)
        if X86_REG_RCX in written: live = False
print("distinct slot bodies: %d ; distinct displacements: %d ; accesses: %d"
      % (len(allslots), len({k[0] for k in acc}), sum(acc.values())))
import json
for lo, ln in json.loads(os.environ.get("DEBT", "[]")):
    ins_ = sorted((dp, w, acc[(dp, w)]) for (dp, w) in acc if lo <= dp < lo + ln)
    print("\nSPAN +0x%04X len %-5d : %d pairs, %d accesses" % (lo, ln, len(ins_), sum(c for _, _, c in ins_)))
    for dp, w, c in ins_[:10]:
        print("      +0x%04X %dB x%-3d %s" % (dp, w, c, ", ".join(sorted(sites[(dp, w)])[:2])))
    if len(ins_) > 10: print("      ... %d more" % (len(ins_) - 10))
