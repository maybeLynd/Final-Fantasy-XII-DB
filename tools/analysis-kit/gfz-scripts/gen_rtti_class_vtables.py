"""Class name -> class vtable, for every polymorphic class in the image.

S-49's remaining debt is body-reading work, and the instrument that answers it is the class vtable:
a slot is a method whose receiver is the object. The store has class vtables for exactly one family
- the 36 post-effect classes FABLE decoded - and nothing general. So build the general map once.

MSVC x64 RTTI: each polymorphic class's vtable is preceded by a qword pointing at its Complete
Object Locator, and the locator carries `signature == 1`, the RVA of its own address in `pSelf`,
and the RVA of a Type Descriptor whose `name` is the mangled class name. So:

  1. walk the read-only sections on an 8-byte grid for candidate locators (signature 1, pSelf
     resolving to the candidate's own RVA, type-descriptor RVA landing in a data section);
  2. for each locator, find the qwords in the image that equal its address - each such position L
     is a vtable's -8 slot, so the vtable is at L + 8;
  3. read the type descriptor's name at +0x10 and demangle enough of it to get the class.

CONTROLS, and they must all fire:
  - PAtmospherics must come out with vtable 00D628A0 (FABLE's RTTI decode, independently);
  - all six post-effect classes I have addresses for must match;
  - the total must be in the same order as the 2350 RTTI class markers this project already
    recorded for the image, not a handful and not a hundred thousand.
"""
import io, struct, collections, re

EXE = "Database/Tools/work/exe/FFXII_TZA.exe"
IMAGE_BASE = 0x120000

blob = open(EXE, "rb").read()
pe = struct.unpack_from("<I", blob, 0x3C)[0]
nsec = struct.unpack_from("<H", blob, pe + 6)[0]
opt = struct.unpack_from("<H", blob, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    name = blob[o:o + 8].rstrip(b"\0").decode(errors="replace")
    vs, va = struct.unpack_from("<II", blob, o + 8)
    rs, ro = struct.unpack_from("<II", blob, o + 16)
    secs.append((name, va, vs, ro, rs))


def rva_to_off(rva):
    for name, va, vs, ro, rs in secs:
        if va <= rva < va + vs:
            d = rva - va
            return ro + d if d < rs else None
    return None


def qword(rva):
    o = rva_to_off(rva)
    if o is None or o + 8 > len(blob):
        return None
    return struct.unpack_from("<Q", blob, o)[0]


def cstr(rva, limit=512):
    o = rva_to_off(rva)
    if o is None:
        return ""
    e = blob.find(b"\0", o, o + limit)
    return blob[o:e if e > 0 else o + limit].decode("latin1")


# ---- 1. candidate complete object locators -------------------------------
locators = {}
for name, va, vs, ro, rs in secs:
    if name not in (".rdata", ".data"):
        continue
    end = min(vs, rs)
    for d in range(0, end - 24, 8):
        off = ro + d
        sig, offv, cd, ptd, pcd = struct.unpack_from("<IIIII", blob, off)
        if sig != 1:
            continue
        pself = struct.unpack_from("<I", blob, off + 20)[0]
        if pself != va + d:
            continue
        if rva_to_off(ptd) is None:
            continue
        nm = cstr(ptd + 0x10, 400)
        if not nm.startswith(".?A"):
            continue
        locators[va + d] = nm

print("candidate complete object locators: %d" % len(locators))

# ---- 2. the qword slots that point at them -------------------------------
loc_set = set(locators)
vtables = collections.defaultdict(list)
for name, va, vs, ro, rs in secs:
    end = min(vs, rs)
    for d in range(0, end - 8, 8):
        v = struct.unpack_from("<Q", blob, ro + d)[0]
        if v < IMAGE_BASE:
            continue
        r = v - IMAGE_BASE
        if r in loc_set:
            vtables[locators[r]].append(va + d + 8 + IMAGE_BASE)

print("classes with at least one vtable: %d" % len(vtables))
print("vtable slots found: %d" % sum(len(v) for v in vtables.values()))


def clean(mangled):
    m = re.match(r"\.\?A[VU]([A-Za-z0-9_]+)@", mangled)
    return m.group(1) if m else mangled


CONTROLS = {
    "PAtmospherics": 0x00D628A0,
    "PAtmosphericsBase": 0x00D62800,
    "PAtmosphericsD3D11": 0x00D62850,
    "PMotionBlur": 0x00D62170,
    "PMotionBlurBase": 0x00D620D0,
    "PMeshParticleSystemBase": 0x00D623A0,
}
byname = {}
for mangled, vts in vtables.items():
    byname.setdefault(clean(mangled), []).extend(vts)

print()
ok = 0
for c, want in CONTROLS.items():
    got = byname.get(c, [])
    hit = want in got
    ok += hit
    print("  CONTROL %-26s expect %08X  %s" % (c, want, "OK" if hit
                                               else "MISS (%s)" % " ".join("%08X" % g for g in got[:3])))
print("controls passed: %d of %d" % (ok, len(CONTROLS)))

out = ("Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/"
       "rtti-class-vtables.tsv")
with io.open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("class\tmangled\tvtable\n")
    for mangled in sorted(vtables):
        for vt in sorted(set(vtables[mangled])):
            f.write("%s\t%s\t%08X\n" % (clean(mangled), mangled, vt))
print("wrote %s" % out)
