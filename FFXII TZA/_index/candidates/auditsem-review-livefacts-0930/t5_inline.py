"""SWE2-AUDIT-SEM T5 attack (own code): inline bulk loops (inline_bulk.tsv, which FABLE's CRT/rep bulk table cannot
see) inside functions that reach an ActorStorageRecord: callers of the getter 00358940, functions with a rip-relative
reference into the manager array 02098E10..02099AC0, and their direct callees (one hop). Each loop is printed with its
base definition so the written object can be typed by reading. Owner = .pdata chain root (bisect index)."""
import struct, re, csv, bisect
import img
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
PD = []
for n, rva, vsz, rpp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rpp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE, u + img.BASE))
PD.sort()
STARTS = [p[0] for p in PD]
def chain_root(b, u):
    uo = img.off(u)
    while uo is not None and (img.raw[uo] >> 3) & 4:
        cnt = img.raw[uo + 2]
        co = uo + 4 + ((cnt + 1) & ~1) * 2
        cb, ce, cu = struct.unpack_from("<III", img.raw, co)
        b = cb + img.BASE
        uo = img.off(cu + img.BASE)
    return b
ROOT = [chain_root(b, u) for b, e, u in PD]
def root(a):
    k = bisect.bisect_right(STARTS, a) - 1
    if k >= 0 and PD[k][0] <= a < PD[k][1]:
        return ROOT[k]
    return None
H = set()
for i in range(len(text) - 5):
    if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == 0x00358940:
        r = root(va0 + i)
        if r:
            H.add(r)
for i in range(len(text) - 4):
    d = struct.unpack_from("<i", text, i)[0]
    for tail in (0, 1, 2, 4):
        if 0x02098E10 <= va0 + i + 4 + tail + d < 0x02099AC0:
            r = root(va0 + i)
            if r:
                H.add(r)
print("H0 functions:", len(H))
H1 = set(H)
for k, (b, e, u) in enumerate(PD):
    if ROOT[k] not in H:
        continue
    for x in img.md.disasm(img.rd(b, e - b), b):
        if x.mnemonic in ("call", "jmp") and re.fullmatch(r"0x[0-9a-f]+", x.op_str):
            H1.add(int(x.op_str, 16))
print("H1 functions:", len(H1))
rows = list(csv.DictReader(open("inline_bulk.tsv"), delimiter="\t"))
hits = []
for r in rows:
    h = int(r["head"], 16)
    ro = root(h)
    if ro in H1:
        hits.append((r, ro))
print("inline bulk loops inside H1:", len(hits))
for r, ro in hits:
    print("  %s in %08X  reg %s stride %s span %s..%s  base %s  count %s" % (
        r["head"], ro, r["reg"], r["stride"], r["store_lo"], r["store_hi"], r["base_def"], r["count"]))
print("note: leaf functions without .pdata are not owners here; loops in them are listed only if a caller is in H0")
