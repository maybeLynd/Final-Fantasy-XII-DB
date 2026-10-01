"""thunk_address_taken.py - BU-5: is any Thunk.* function the target of a data reference rather than only called?

Population: every functions.tsv row whose tags contain `Thunk.` (entry, tags). Instruments, each over the whole file:
  (a) 8-byte VA  - little-endian qword equal to the entry, in any section (vtables, pointer tables, .data);
  (b) 4-byte RVA - dword equal to entry - image base, reported per section; .pdata / .xdata hits are unwind records
                   (a function start), not address-taking, and are listed separately;
  (c) rip-relative `lea`/`mov` whose target is the entry, anywhere in .text (REX 8D/8B, ModRM rip form).
Control: the same three instruments on a sample of functions known to be address-taken (the first slot of five
RTTI-named vtables given on the command line as VAs of vtables), which must each report at least one (a) hit.
Usage (from Database/Tools/work/FABLE/pub140-scratch):  python <this> FUNCTIONS_TSV [VTABLE_VA ...]"""
import struct, sys, collections
import pefile

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
BASE = 0x120000
pe = pefile.PE(EXE, fast_load=True)
t = pe.__data__


def section_of(off):
    s = pe.get_section_by_offset(off)
    return s.Name.rstrip(b"\0").decode() if s else "?"


thunks = []
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    if len(p) >= 9 and "Thunk." in p[8]:
        thunks.append((int(p[0], 16), p[1], [x for x in p[8].split(";") if x.startswith("GFZ") and "Thunk." in x]))
print("Thunk.* functions:", len(thunks))

text = next(s for s in pe.sections if s.Name.startswith(b".text"))
tlo, thi = text.PointerToRawData, text.PointerToRawData + text.SizeOfRawData
tva = BASE + text.VirtualAddress
rip = collections.defaultdict(list)
for o in range(tlo, thi - 7):
    if t[o] in (0x48, 0x4C) and t[o + 1] in (0x8D, 0x8B) and (t[o + 2] & 0xC7) == 0x05:
        va = tva + (o - tlo)
        rip[va + 7 + struct.unpack_from("<i", t, o + 3)[0]].append(va)


def refs(entry):
    q = struct.pack("<Q", entry)
    a = []
    i = t.find(q)
    while i >= 0:
        a.append(section_of(i))
        i = t.find(q, i + 1)
    r = struct.pack("<I", entry - BASE)
    b = []
    i = t.find(r)
    while i >= 0:
        b.append(section_of(i))
        i = t.find(r, i + 1)
    return a, b, rip.get(entry, [])


for v in [a for a in sys.argv[2:] if not a.startswith("--")]:
    vt = int(v, 16)
    s0 = struct.unpack_from("<Q", t, pe.get_offset_from_rva(vt - BASE))[0]
    a, b, c = refs(s0)
    print("control vtable %08X slot0 %08X: qword %d %s, rva %s, rip %d" % (vt, s0, len(a), sorted(set(a)), dict(collections.Counter(b)), len(c)))

hit = []
for entry, name, tags in thunks:
    a, b, c = refs(entry)
    b_nonunwind = [s for s in b if s not in (".pdata", ".xdata")]
    if a or b_nonunwind or c:
        hit.append((entry, name, tags, a, b_nonunwind, c))
print("thunks with any data reference (qword, non-unwind RVA, or rip-relative):", len(hit))
fam = lambda tags: ",".join(x.split(".")[-1] for x in tags)
strong = [h for h in hit if h[3] or h[5]]
print("  of which a qword VA or a rip-relative load (the two instruments without chance coincidence):", len(strong))
print("    qword only %d, rip-relative only %d, both %d" % (sum(1 for h in strong if h[3] and not h[5]),
      sum(1 for h in strong if h[5] and not h[3]), sum(1 for h in strong if h[3] and h[5])))
print("    by family:", dict(collections.Counter(fam(h[2]) for h in strong)))
print("    qword sections:", dict(collections.Counter(s for h in strong for s in h[3])))
print("  RVA-only hits (a 4-byte value can equal an RVA by chance; not counted as address-taken):", len(hit) - len(strong))
for entry, name, tags, a, b, c in (strong if "--strong" in sys.argv else hit):
    print("  %08X %-40s %s qword=%s rva=%s rip=%s" % (entry, name[:40], ",".join(x.split(".")[-1] for x in tags), dict(collections.Counter(a)), dict(collections.Counter(b)), ["%08X" % x for x in c[:4]]))
