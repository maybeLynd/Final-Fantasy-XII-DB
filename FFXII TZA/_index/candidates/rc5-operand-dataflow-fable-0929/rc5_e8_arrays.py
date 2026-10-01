"""rc5_e8_arrays.py - RC-5 residue: the eventread_e8 set-id operands that read array-class (class 7) variables
(FABLE, 2026-09-29).

Layout (script-variables-and-their-storage-classes.md sections 2.1-2.3, read from 00262440):
  - class 7 header at img + (descriptor & 0xFFFFFF): element descriptor dword at +0, dimension count u16 at +4,
    dimensions as signed dwords from +8 (002624B3-002624C6); each popped index is clamped into [0, dim-1]
    (002624D2-00262537), so the value read is always one of the array's elements when every dim >= 1;
  - the element descriptor's class 1 (`file`) home is `payload + [payload + 0x38]`, a data area inside the loaded script
    image (0026D2F6); the element address is home + (element descriptor & 0xFFFFFF) + width * flattened index.
For each array a site reads, and only when rc5_dataflow.tsv found no POPV into it and no PUSHP reference (status
NEVER-STORED): print the array's dims and every element value from the image. Those are the only values the site can
read. Arrays with stores, or a dim below 1, are reported and not bounded.
Control: the first eventread_e8 site with a CONSTANT set id in rc5_verbs.tsv is not needed here; the positive control is
structural - the element descriptor's class must be 1 (file) and width 4 (s32), and the element area must lie inside
the section (FAILS otherwise)."""
import csv, io, os, struct, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
rows = [r for r in csv.DictReader(io.open(os.path.join(HERE, "rc5_dataflow.tsv"), encoding="utf-8"), delimiter="\t")
        if r["verb"] == "eventread_e8"]
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
CLS = {0: "global", 1: "file", 2: "local", 4: "scratch1", 5: "scratch2", 7: "array"}
def alias_scan(sec, lo, hi):
    # ALIAS CHECK: another descriptor can name the same file bytes. Any POPV / PUSHP in this file whose file-class storage
    # range (scalar: offset..offset+width; array: element range) overlaps [eoff, eoff + 4n) can write these elements.
    WB = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4}
    vt = U32(sec, 0x28)
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    starts = sorted(set(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    aliases = []
    for st in starts:
        end = min((x for x in bounds if x > st), default=len(sec))
        ins, _ = G.decode(sec[st:end])
        for pc, op, imm in ins:
            if op not in (0x49, 0x4B):
                continue
            d = U32(sec, vt + imm * 8 + 4)
            c, o = (d >> 24) & 7, d & 0xFFFFFF
            if c == 7:
                e2 = U32(sec, o); nd2 = U16(sec, o + 4)
                n2 = 1
                for i in range(nd2):
                    n2 *= max(S32(sec, o + 8 + 4 * i), 0)
                c2, o2, w2 = (e2 >> 24) & 7, e2 & 0xFFFFFF, WB.get((e2 >> 28) & 0xF, 4)
                if c2 == 1 and o2 < hi and o2 + w2 * n2 > lo:
                    aliases.append("%X %s array %X" % (st + pc, G.OPN.get(op), o))
            elif c == 1 and o < hi and o + WB.get((d >> 28) & 0xF, 4) > lo:
                aliases.append("%X %s file +%X" % (st + pc, G.OPN.get(op), o))
    return aliases


fails = 0
controls = []
bounded = collections.Counter()
seen = {}
for r in rows:
    tag = "%s %s" % (r["file"].split("/")[-1], r["pc"])
    if r["class"] != "array":
        print("%s: file scalar at %s, %s (%s) - not bounded here" % (tag, r["offset"], r["status"], r["dynamic_producers"]))
        continue
    off = int(r["offset"], 16)
    b = G.V.read_entry(f, names, blocks, r["file"])
    sec = b[0x80:0x80 + U32(b, 0x84)]
    ed = U32(sec, off); nd = U16(sec, off + 4)
    dims = [S32(sec, off + 8 + 4 * i) for i in range(nd)]
    ecls, eoff, ew = (ed >> 24) & 7, ed & 0xFFFFFF, (ed >> 28) & 0xF
    home = U32(sec, 0x38)
    n = 1
    for d in dims:
        n *= max(d, 0)
    ok = ecls == 1 and ew == 4 and nd >= 1 and all(d >= 1 for d in dims) and home + eoff + 4 * n <= len(sec)
    if not ok:
        fails += (ecls != 1 or ew != 4)
        print("%s: array %X element class %s width %d dims %s - not bounded (structure check %s)" % (
            tag, off, CLS.get(ecls, ecls), ew, dims, "FAIL" if (ecls != 1 or ew != 4) else "dim<1 or out of section"))
        continue
    vals = [S32(sec, home + eoff + 4 * i) for i in range(n)]
    if r["status"] != "NEVER-STORED":
        ctl = alias_scan(sec, eoff, eoff + 4 * n)
        controls.append((tag, len(ctl)))
        print("%s: array %X (file +%X, dims %s) has stores (%s) - elements' initial values %s, not a bound" % (
            tag, off, eoff, dims, r["status"], sorted(set(vals))))
        continue
    aliases = alias_scan(sec, eoff, eoff + 4 * n)
    if aliases:
        print("%s: array %X, file +%X, dims %s - ALIASED by %d store/ref site(s) %s - not bounded" % (
            tag, off, eoff, dims, len(aliases), aliases[:6]))
        continue
    bounded[r["file"].split("/")[-1]] += 1
    print("%s: array %X, file +%X, dims %s, never stored and no alias -> set id is one of %s" % (
        tag, off, eoff, dims, sorted(set(vals))))
print("bounded eventread_e8 sites by file:", dict(bounded), " total", sum(bounded.values()))
ctl_ok = bool(controls) and all(k > 0 for _, k in controls)
print("CONTROL alias scan finds the stores of every stored array:", controls, "PASS" if ctl_ok else "FAIL")
fails += not ctl_ok
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
