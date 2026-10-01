"""SWE2-AUDIT-SEM UC1-SPAN checks (own code).
P  PPFX: the 733 bodies' size distribution, split referenced / unreferenced; the byte patterns of the small ones
   (grouped); a spread sample of 12 larger unreferenced bodies decoded, with every call target and rip data target
   classified inside / outside the span.
X  independent reference hunt for every PPFX body with refs = 0, beyond the producer's aligned cells: any 8-byte VA
   anywhere in the file (unaligned), any 4-byte RVA at any alignment in .rdata/.data, and any rel32 E8/E9 site at any
   offset in .text (all alignments).
S  SEAD 007EE7C0 decoded whole; every rel32 / rip / VA / RVA reference to it.
V  libvpx: the control map at 01CDB320 (qwords until a non-code value), the four bodies decoded, and every reference."""
import csv, struct, collections, os
import img

HERE = os.path.dirname(os.path.abspath(__file__))
TSV = None
for p in (os.path.join(HERE, "..", "ec7-uc1-span-rows-0929", "uc1-span-tests.tsv"),
          os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA", "_index", "candidates", "ec7-uc1-span-rows-0929",
                       "uc1-span-tests.tsv")):
    if os.path.exists(p):
        TSV = p
rows = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
LO, HI = 0x006DA880, 0x007911E0

def dis(a, n):
    return list(img.md.disasm(img.rd(a, n), a))

pp = [r for r in rows if r["family"] == "PPFX"]
unref = [r for r in pp if r["refs"] == "0"]
ref = [r for r in pp if r["refs"] != "0"]
def bucket(n):
    n = int(n)
    return "<=4" if n <= 4 else "5-16" if n <= 16 else "17-64" if n <= 64 else "65-256" if n <= 256 else ">256"
for name, grp in (("unreferenced", unref), ("referenced", ref)):
    c = collections.Counter(bucket(r["bytes"]) for r in grp)
    print("P %s %d: %s" % (name, len(grp), dict(sorted(c.items()))))
small = collections.Counter()
for r in pp:
    if int(r["bytes"]) <= 16:
        a = int(r["body"], 16)
        small[" ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in dis(a, int(r["bytes"])))] += 1
print("P small bodies (<=16 B) by instruction text, top 15:")
for k, v in small.most_common(15):
    print("   %4d  %s" % (v, k))
big = sorted([r for r in unref if int(r["bytes"]) > 64], key=lambda r: int(r["body"], 16))
sample = [big[i * (len(big) - 1) // 11] for i in range(12)] if len(big) >= 12 else big
for r in sample:
    a, n = int(r["body"], 16), int(r["bytes"])
    xs = dis(a, n)
    calls = []
    for x in xs:
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if not (a <= t < a + n):
                calls.append(("in" if LO <= t < HI else "OUT") + ":%08X" % t)
        if "rip" in x.op_str:
            try:
                disp = int(x.op_str.split("rip ")[1].split("]")[0].replace("+ ", "").replace("- ", "-"), 16)
                t = x.address + x.size + disp
                calls.append("data:%08X" % t)
            except Exception:
                pass
    print("P sample %s (%d B, %d insns): first '%s %s'; refs out: %s" % (
        r["body"], n, len(xs), xs[0].mnemonic if xs else "?", xs[0].op_str if xs else "", " ".join(calls[:12]) or "none"))

# X: independent reference hunt for the unreferenced PPFX bodies
targets = {int(r["body"], 16) for r in unref}
raw = img.raw
hits = collections.defaultdict(list)
# rel32 at every .text offset
for i in range(len(text) - 5):
    if text[i] in (0xE8, 0xE9):
        t = va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0]
        if t in targets:
            hits[t].append("rel32@%08X" % (va0 + i))
# 8-byte VA and 4-byte RVA at every offset of the file outside .text and .pdata
secs = {s[0]: s for s in img.secs}
for name, rva, vsz, rptr, rsz in img.secs:
    if name in (".text", ".pdata", ".reloc"):
        continue
    blob = raw[rptr:rptr + rsz]
    for i in range(len(blob) - 8):
        q = struct.unpack_from("<Q", blob, i)[0]
        if q in targets:
            hits[q].append("va64@%s+%X" % (name, i))
        d = struct.unpack_from("<I", blob, i)[0] + img.BASE
        if d in targets:
            hits[d].append("rva32@%s+%X" % (name, i))
print("X unreferenced PPFX bodies: %d; with a hit in the widened hunt: %d" % (len(targets), len(hits)))
for t in sorted(hits)[:30]:
    print("   %08X %s" % (t, " ".join(hits[t][:6])))

def refs_to(t):
    out = []
    for i in range(len(text) - 5):
        if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == t:
            out.append("rel32@%08X" % (va0 + i))
        if text[i] in (0x0F,) and 0x80 <= text[i + 1] <= 0x8F and i + 6 <= len(text) and \
                va0 + i + 6 + struct.unpack_from("<i", text, i + 2)[0] == t:
            out.append("jcc32@%08X" % (va0 + i))
    for i in range(len(text) - 4):
        if va0 + i + 4 + struct.unpack_from("<i", text, i)[0] == t:
            for L in range(15, 4, -1):
                st = i + 4 - L
                xs = list(img.md.disasm(text[st:st + L], va0 + st, 1))
                if xs and xs[0].size == L and "rip" in xs[0].op_str:
                    out.append("rip@%08X(%s %s)" % (xs[0].address, xs[0].mnemonic, xs[0].op_str))
                    break
    n8 = raw.count(struct.pack("<Q", t))
    n4 = raw.count(struct.pack("<I", t - img.BASE))
    out.append("va64 x%d, rva32-bytes x%d" % (n8, n4))
    return out

print("S 007EE7C0:")
for x in dis(0x007EE7C0, 57):
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("S refs:", refs_to(0x007EE7C0))
print("V control map 01CDB320:")
for k in range(0, 0x100, 8):
    q = struct.unpack("<Q", img.rd(0x01CDB320 + k, 8))[0]
    print("   %08X: %016X" % (0x01CDB320 + k, q))
    if not (img.BASE <= q < img.BASE + 0x2000000):
        break
for b, n in ((0x0016EE40, 48), (0x0016EE80, 63), (0x0016EFF0, 56), (0x0016F030, 49)):
    xs = dis(b, n)
    print("V %08X (%d B): %s" % (b, n, " ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in xs[:8])))
    print("   refs:", refs_to(b))
