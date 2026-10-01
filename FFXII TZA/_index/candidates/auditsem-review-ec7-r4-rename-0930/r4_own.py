"""SWE2-AUDIT-SEM R4 check (own RTTI walk; does not read rtti/methods.tsv). For the 17 family members and the 28 bodies
tagged ...ConditionalTeardownReturnTrue in functions.tsv: find every qword in the file equal to the body address; for
each, walk back slot by slot until the qword before the slot is a CompleteObjectLocator (x64 COL: signature 1, pSelf
RVA equals its own RVA); report the slot index and the class name from the COL's type descriptor (+0x10 string).
Control: a known RTTI vtable slot (the class-descriptor slot map's +0x40 AttachMember neighbour, slot 8) is reported
for the same vtables."""
import struct, re, io, collections
import img
raw = img.raw
BASE = img.BASE
def rva(a):
    return a - BASE
def is_col(va):
    o = img.off(va)
    if o is None or o + 24 > len(raw):
        return False
    sig, off, cdo, td, ch, self_ = struct.unpack_from("<IIIIII", raw, o)
    return sig == 1 and self_ == rva(va)
def class_of(col):
    o = img.off(col)
    td = struct.unpack_from("<I", raw, o + 12)[0] + BASE
    s = img.rd(td + 0x10, 200)
    return s.split(b"\0")[0].decode("latin-1") if s else "?"
qidx = collections.defaultdict(list)
for o in range(0, len(raw) - 8, 8):
    v = struct.unpack_from("<Q", raw, o)[0]
    if 0x00121000 <= v < 0x00900000:
        qidx[v].append(o)
def off2va(o):
    for n, r, vsz, rp, rs in img.secs:
        if rp <= o < rp + rs:
            return BASE + r + (o - rp)
def slots(addr):
    out = []
    for o in qidx.get(addr, []):
        va = off2va(o)
        for k in range(0, 64):
            prev = struct.unpack_from("<Q", raw, o - 8 * (k + 1))[0]
            if is_col(prev):
                out.append((k, class_of(prev), "%08X" % (va - 8 * k)))
                break
    return out
MEM = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\24-Compiler-And-CRT-Runtime\Generated-Families\members\cxxobjectlifecycle-conditionalteardownreturntrue.tsv"
members = []
for l in io.open(MEM, encoding="utf-8", errors="replace"):
    m = re.match(r"^([0-9A-Fa-f]{8})\s*$", l)
    if m:
        members.append(int(m.group(1), 16))
tagged = []
for l in io.open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv", encoding="utf-8", errors="replace"):
    if "ConditionalTeardownReturnTrue" in l:
        tagged.append(int(l.split("\t")[0], 16))
print("members:", len(members), " tagged bodies:", len(tagged), " members inside tagged:", len(set(members) & set(tagged)))
tally = collections.Counter()
for tag, pop in (("MEMBER", members), ("TAGGED", tagged)):
    for a in pop:
        s = slots(a)
        kinds = sorted(set((k, re.sub(r"<.*", "<T>", c)) for k, c, v in s))
        tally[(tag, tuple(kinds))] += 1
        if tag == "TAGGED" and not all(k == 10 for k, c, v in s):
            print("   non-slot-10:", "%08X" % a, s[:4])
for (tag, kinds), n in sorted(tally.items()):
    print("%-7s x%-3d %s" % (tag, n, kinds))
names = collections.Counter()
for a in tagged:
    for k, c, v in slots(a):
        names["WithoutDefault" in c] += 1
print("tagged vtable hits naming PClassDescriptorWithoutDefaultConstructor:", names[True], " others:", names[False])
