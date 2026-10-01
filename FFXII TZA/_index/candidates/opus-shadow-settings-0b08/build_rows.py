"""Build the type-store rows for the 0xB08 shadow-settings object (OPUS, 2026-09-26). Prints; --write appends to the store."""
import collections, glob, json, os, sys

SP = os.path.dirname(os.path.abspath(__file__))
SIZE = 0xB08
T = "ShadowSettings01F82EA8"
EVID = ("census_receiver_fixpoint.py SEED=call 001F0850 + SEED=ctor 001EF2D0 + SEED=cell 01F82EA8 + SEED=cell 01F812C8, extent 0xB08, "
        "unioned by site (OPUS, 2026-09-26); key names from the cutscene loader 001C3D50 (lea key -> getter -> store, keystore_trace.py)")
# offset -> (name, ctype, size, key, store site) from the loader trace
KEYS = {
    0x0EC: ("shadowValueR", "float", 4, "ShadowValueR", "001C4872"),
    0x140: ("shadowValueLerpMinForMap", "float", 4, "mShadowValueLerpMinForMap", "001C43C1"),
    0x144: ("shadowValueLerpMinForChr", "float", 4, "mShadowValueLerpMinForChr", "001C43E7"),
    0x830: ("decayDistance", "float", 4, "mDecayDistance", "001C44D5"),
    0x83C: ("mapHeightMin", "float", 4, "mMapHeightMin", "001C445D"),
    0x840: ("mapHeightMax", "float", 4, "mMapHeightMax", "001C4483"),
    0x870: ("cascadePartition0", "float", 4, "mCascadePartition0", "001C4774"),
    0x874: ("cascadePartition1", "float", 4, "mCascadePartition1", "001C47A1"),
    0x878: ("cascadePartition2", "float", 4, "mCascadePartition2", "001C47CE"),
    0x890: ("pcfBlurSize", "int32", 4, "m_iPCFBlurSize", "001C4725"),
    0x894: ("pcfBlurSizeForMap", "int32", 4, "m_iPCFBlurSizeForMap", "001C47F4"),
    0x898: ("shadowBias", "float", 4, "ShadowBias", "001C44FB"),
    0x8A0: ("blurBetweenCascades", "int32", 4, "m_iBlurBetweenCascades", "001C4749"),
    0x8A4: ("blurBetweenCascadesAmount", "float", 4, "m_fBlurBetweenCascadesAmount", "001C440D"),
}
CTOR_LO, CTOR_HI = 0x1EF2D0, 0x1EF2D0 + 462      # 001EF2D0, 462 bytes (functions.tsv)
EXTRA = {0x0FC: ("lightDirection", "float[3]", 12,
                 "the scene's key-light direction vector, x/y/z (weather page D-4, ANSWERED 2026-09-26 by FABLE: authored as the angles "
                 "lightOrientation / lightHeight; the setter 001F08A0 materialises it; default straight up). Whether it points at the light "
                 "or away from it is not established")}
sites = collections.defaultdict(dict)          # (disp, width) -> site -> [r, w]
for f in glob.glob(os.path.join(SP, "census_*.json")):
    d = json.load(open(f))
    assert d["converged"], f
    for k, v in d["sites"].items():
        dp, wd = map(int, k.split(":"))
        for s, rw in v.items():
            sites[(dp, wd)][s] = rw                # the same instruction reached by two seeds counts once
by_disp = collections.defaultdict(lambda: {"w": set(), "r": 0, "wr": 0, "sites": set()})
for (dp, wd), ss in sites.items():
    if not (0 <= dp < SIZE):
        continue
    e = by_disp[dp]; e["w"].add(wd)
    for s, (r, w) in ss.items():
        e["r"] += r; e["wr"] += w; e["sites"].add(s)
# check the key fields: each must be censused, and its widths must fit the declared size
problems = []
MERGED = {}
for off, (nm, ct, sz, key, st) in KEYS.items():
    e = by_disp.get(off)
    if not e:
        problems.append("key %s at +0x%X has no censused access" % (key, off))
    elif max(e["w"]) > sz:
        wide = [s for (dp, wd), ss in sites.items() if dp == off and wd > sz for s in ss]
        if not all(CTOR_LO <= int(s, 16) < CTOR_HI for s in wide):
            problems.append("key %s at +0x%X censused at width %s > %d outside the ctor" % (key, off, sorted(e["w"]), sz))
        else:
            MERGED[off] = wide
for off, (nm, ct, sz, why) in EXTRA.items():
    ds = [d for d in by_disp if off <= d < off + sz]
    if not ds or any(d + max(by_disp[d]["w"]) > off + sz for d in ds):
        problems.append("extra %s at +0x%X: census does not fit %d bytes" % (nm, off, sz))
    KEYS[off] = (nm, ct, sz, None, why)
rows = []
def census_note(lo, hi):
    ds = [d for d in by_disp if lo <= d < hi]
    r = sum(by_disp[d]["r"] for d in ds); w = sum(by_disp[d]["wr"] for d in ds)
    return ds, r, w
off = 0
named = sorted(KEYS)
accessed = sorted(by_disp)
while off < SIZE:
    if off in KEYS:
        nm, ct, sz, key, st = KEYS[off]
        ds = [d for d in by_disp if off <= d < off + sz]
        r = sum(by_disp[d]["r"] for d in ds); w = sum(by_disp[d]["wr"] for d in ds)
        ss = sorted(set().union(*[by_disp[d]["sites"] for d in ds]))
        cen = "census: %d displacement(s), r%d w%d (%s)" % (len(ds), r, w, ", ".join(ss[:3]) + (" +%d more" % (len(ss) - 3) if len(ss) > 3 else ""))
        if off in MERGED:
            cen += "; the constructor initialises it with a merged 8-byte store that also covers the next 4 bytes (%s) - an access width, not the field's" % ", ".join(MERGED[off])
        if key is None:
            rows.append((off, sz, nm, ct, "%s. %s" % (st, cen), "SEMANTICALLY IDENTIFIED", "HIGH"))
        else:
            rows.append((off, sz, nm, ct, "scene-JSON key %s: the cutscene loader stores it here (%s). %s" % (key, st, cen),
                         "SEMANTICALLY IDENTIFIED", "PROVEN"))
        off += sz
        continue
    nxt_named = min([k for k in named if k > off] + [SIZE])
    # extent of accessed bytes starting here
    acc_here = [d for d in accessed if off <= d < nxt_named]
    if not acc_here:
        rows.append((off, nxt_named - off, "unobservedSpan%04X" % off, "u8[%d]" % (nxt_named - off),
                     "no censused access from any of the four seeds (a lower bound, not proof of disuse)", "UNOBSERVED", "HIGH"))
        off = nxt_named
        continue
    first = acc_here[0]
    if first > off:
        rows.append((off, first - off, "unobservedSpan%04X" % off, "u8[%d]" % (first - off),
                     "no censused access from any of the four seeds (a lower bound, not proof of disuse)", "UNOBSERVED", "HIGH"))
        off = first
        continue
    # a censused stretch: extend while accesses (with their widths) stay contiguous up to the next named field
    end = off
    for d in acc_here:
        if d > end:
            break
        end = max(end, d + max(by_disp[d]["w"]))
    end = min(end, nxt_named)
    ds, r, w = census_note(off, end)
    rows.append((off, end - off, "span%04X" % off, "u8[%d]" % (end - off),
                 "an unnamed stretch: %d censused displacements, %d accesses (%d reads, %d writes); first +0x%X, last +0x%X"
                 % (len(ds), r + w, r, w, min(ds), max(ds)), "DISCOVERED", "HIGH"))
    off = end
def period_note(o):
    for base, n in ((0x1C0, 8), (0x8C0, 3)):
        if base <= o < base + n * 0xD8:
            k, rel = divmod(o - base, 0xD8)
            return " (0xD8-periodic run from +0x%X: stretch %d, +0x%X - an element type is not declared, and the first run's last stretch overlaps the dense +0x800 region)" % (base, k, rel)
    return ""
rows = [(o, s, n, c, m + (period_note(o) if n.startswith(("span", "unobserved")) else ""), rd, cf) for o, s, n, c, m, rd, cf in rows]
named = sorted(KEYS)
assert sum(r[1] for r in rows) == SIZE and all(rows[i][0] + rows[i][1] == rows[i + 1][0] for i in range(len(rows) - 1)), "tiling"
print("problems:", problems)
print("rows:", len(rows), "named:", sum(1 for r in rows if r[6] == "PROVEN"), "spans:", sum(1 for r in rows if r[2].startswith("span")),
      "unobserved:", sum(1 for r in rows if r[2].startswith("unobserved")))
print("censused displacements:", len(by_disp), "accesses:", sum(e["r"] + e["wr"] for e in by_disp.values()))
for r in rows:
    print("+0x%04X %5d %-28s %-10s %s" % (r[0], r[1], r[2], r[3], r[4][:110]))
if "--write" in sys.argv:
    assert not problems
    P = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_types\fields.tsv"
    raw = open(P, "rb").read().decode("utf-8")
    assert ("\n" + T + "\t") not in raw, "already declared"
    eol = "\r\n" if raw.endswith("\r\n") else "\n"
    add = "".join("\t".join([T, "0x%04X" % o, str(s), n, c, m, rd, cf, EVID]) + eol for o, s, n, c, m, rd, cf in rows)
    open(P, "wb").write((raw + ("" if raw.endswith(("\n",)) else eol) + add).encode("utf-8"))
    print("wrote", len(rows), "rows")
