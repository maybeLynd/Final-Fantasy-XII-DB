"""gi10names.py - join effect element types 0x60-0x74 to ability names (FABLE GI-10 reader, 2026-09-29).
Chain (static): action row word +0x24 -> BattleAction_GetPresentationParameter 0030A190 (returns it unless 0xFFFF,
bit 15 set, or row +0xC bit 30) -> 00328360 -> 0042FCE0 -> 002FCBF0 (magic-effect record, id at +0x20) -> loader 002FC4A0
requests resource kind 0x26 or 0x0B with that id -> the kind-11 / kind-38 path tables 01E18670 / 01EBE740 (bound into
0215F058 / 0215F130 by 002DF9A0) whose entry i is ...\\magic\\m%04d.efx with %04d = i.
Name: bank 0 of the battle text banks (battle_pack directory +0xF8) entry (row +0x34 & 0x7FF).
Element types per file: the GI-8 census gi-scratch/effects/type_census_files.tsv."""
import struct, sys, re, collections, os
exec(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\disw.py").read().split("fn = int")[0])
FAILS = 0
def check(n, ok, det=""):
    global FAILS
    FAILS += (not ok); print(("PASS " if ok else "FAIL ") + n + (("  -- " + str(det)) if det else ""))
PACK = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin"
pk = open(PACK, "rb").read()
u32 = lambda o: struct.unpack_from("<I", pk, o)[0]
def records(doff):
    t = u32(doff); cnt, size, hdr = u32(t + 4), u32(t + 8), u32(t + 0xC)
    return [pk[t + hdr + i * size: t + hdr + (i + 1) * size] for i in range(cnt)]
def dec(b):
    out = []
    for c in b:
        if c == 0: break
        if 0x20 <= c <= 0x39: out.append(chr(65 + c - 0x20))
        elif 0x3A <= c <= 0x53: out.append(chr(97 + c - 0x3A))
        elif 0x54 <= c <= 0x5D: out.append(chr(48 + c - 0x54))
        elif c == 4: out.append(" ")
        elif c == 0xAC: out.append("'")
        elif c == 0xA5: out.append("-")
        else: out.append("{%02X}" % c)
    return "".join(out)
# battle text banks: directory +0xF8 -> {u32 count, u32 offsets[count+1]} ; block {u32 n, u32 off[n+1], strings}
wb = u32(0xF8)
nb = u32(wb)
def bank(k):
    b = wb + u32(wb + 4 + 4 * k); n = u32(b)
    # each string sits 2 bytes past its offset (a u16 prefix, 0 in bank 0); the controls below pin this
    return [dec(pk[b + u32(b + 4 + 4 * i) + 2: b + u32(b + 8 + 4 * i)]) for i in range(n)]
b0 = bank(0)
check("text bank 0 control: entries 0/1/2 = Cure / Blindna / Vox", b0[0:3] == ["Cure", "Blindna", "Vox"], b0[0:3])
check("text bank 0 control: entries 0x106 / 0x112 = Belias / Zodiark (the Esper block)", (b0[0x106], b0[0x112]) == ("Belias", "Zodiark"), (b0[0x106], b0[0x112]))
rows = records(0x3C)
check("action table: 543 rows of 60 bytes", len(rows) == 543 and len(rows[0]) == 60, (len(rows), len(rows[0])))
# image: the reader and the path tables
def ins(a):
    f = max(k for k in funcs if k <= a)
    for x in md.disasm(d[off(f):off(f) + funcs[f]], f):
        if x.address == a: return f"{x.mnemonic} {x.op_str}"
for a, s in [(0x0030A213, "movzx eax, word ptr [rbx + 0x24]"), (0x0030A21C, "cmp ax, cx"), (0x0030A221, "test dword ptr [rbx + 0xc], 0x40000000"),
             (0x0030A22D, "js 0x30a238"), (0x0030A209, "movzx eax, word ptr [rbx + 0x28]"), (0x0030CCC3, "call 0x30a190"), (0x0030CCCA, "call 0x328360"),
             (0x00328368, "jmp 0x42fce0"), (0x002FCC7F, "mov word ptr [rbx + 0x20], di"), (0x002FC585, "mov edx, 0x26"), (0x002FC58C, "mov ecx, 0xb"),
             (0x002FC594, "movzx edx, word ptr [r15 + 0x20]"), (0x002FC599, "call 0x2df980")]:
    t = ins(a); check(f"{a:08X} is '{s}'", t is not None and s in t, t)
paths = {}
for m in re.finditer(rb"[ -~]*effect_finish[ -~]*", d):
    pass
def cstr(v):
    o = off(v); return d[o:d.index(b"\0", o)].decode("latin-1") if o is not None else None
for base in (0x01E18670, 0x01EBE740):
    bad = 0; n = 0
    for i in range(512):
        q = struct.unpack_from("<Q", d, off(base + 8 * i))[0]
        if not q: continue
        s = cstr(q); n += 1
        if not (s and s.lower().endswith("\\magic\\m%04d.efx" % i)): bad += 1
    check(f"path table {base:08X}: every non-null entry i names magic\\m%04d.efx with %04d = i", bad == 0 and n > 300, (n, bad))
# census
CENS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\gi-scratch\effects\type_census_files.tsv"
types_of = collections.defaultdict(set)
for l in open(CENS):
    p = l.rstrip("\n").split("\t")
    if p[0] == "type": continue
    m = re.search(r"/magic/m(\d{4})\.efx$", p[2])
    if m: types_of[int(m.group(1))].add(int(p[0], 16))
band = {n: t for n, t in types_of.items() if any(0x60 <= x <= 0x74 for x in t)}
# join
users = collections.defaultdict(list)
for i, r in enumerate(rows):
    eff = struct.unpack_from("<H", r, 0x24)[0]; flags = struct.unpack_from("<I", r, 0xC)[0]
    if eff == 0xFFFF or eff & 0x8000 or flags & 0x40000000: continue
    users[eff].append((i, b0[struct.unpack_from("<H", r, 0x34)[0] & 0x7FF]))
alt = collections.defaultdict(list)   # the +0x28 path (action ids 0xD0-0xF1 in world state 5 / 6)
for i in range(0xD0, 0xF2):
    alt[struct.unpack_from("<H", rows[i], 0x28)[0]].append((i, b0[struct.unpack_from("<H", rows[i], 0x34)[0] & 0x7FF]))
print(f"\nmagic files carrying element types 0x60-0x74 (census): {len(band)}")
named = 0
out = []
for n in sorted(band):
    t = ",".join("%#04x" % x for x in sorted(band[n]) if 0x60 <= x <= 0x74)
    u = users.get(n, []); a = alt.get(n, [])
    if u or a: named += 1
    out.append((n, t, u, a))
    print(f"m{n:04d}  types {t:24s} actions: " + ("; ".join(f"{i:#05x} {nm}" for i, nm in u) or "-") +
          (("   [+0x28 path, world state 5/6: " + "; ".join(f"{i:#05x} {nm}" for i, nm in a) + "]") if a else ""))
print(f"\ncoverage: {named} of {len(band)} band-carrying magic files get at least one action name by the exact join")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gi10names.tsv"), "w", encoding="utf-8") as f:
    f.write("file\tband_types\taction_ids_names\talt_0x28_path\n")
    for n, t, u, a in out:
        f.write(f"m{n:04d}.efx\t{t}\t" + "; ".join(f"{i:#05x} {nm}" for i, nm in u) + "\t" + "; ".join(f"{i:#05x} {nm}" for i, nm in a) + "\n")
print(f"\nFAILS {FAILS}")
sys.exit(1 if FAILS else 0)
