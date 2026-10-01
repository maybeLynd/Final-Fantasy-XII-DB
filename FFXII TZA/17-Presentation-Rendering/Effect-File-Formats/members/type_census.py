"""type_census.py - which effect element types the shipped data authors, over EVERY EFX chunk stream in the full
extract (GI-8, FABLE 2026-09-29). Supersedes the population of effect_type_usage.py (kept beside it, unchanged).

Inputs (absolute; runs from any cwd):
  D:/FFXII_TZA_extract                     the full game extract (all nine locale trees)
  efx-embedded-stream-files.txt (here)     the non-effect files that carry an embedded EFX stream (531 files), found by
                                           a byte search for "EFX00" over all 89,414 extract files (rerun: --rescan)
  effect-type-authored-usage.tsv (here)    the earlier census, used as control C3
  effect-type-methods.tsv (here)           the dispatch tables, to classify each authored type main / sub-range

What is walked:
  * the 3,288 .efx files, one EFX stream each;
  * the 410 .efb files: an .efb carries its EFX streams as embedded blobs {u32 size; 12 bytes; EFX[size]}
    (efx-and-efb-effect-containers.md s3) - effect_type_usage.py walked them as bare chunk streams and stopped at
    the first blob header;
  * 531 EFX streams embedded in .cm model files (144) and .mpk map-control plans (387).
  Every stream starts at its magic ('EFX0010' / 'EFX0009' / 'EFX0008'); its header +0xC holds the stream size; the
  chunk walk ({u32 length, u16 flag == 0x100, u16 type}) runs from +0x10 to that size. Element type = byte +0xE of each
  0xA00 chunk (dispatch page s2.8; loader 003EDAD0 -> 003A9A70 -> definition +0x44).

Checks (exit status 1 if any fails):
  C1 every stream walk ends exactly at its declared size;
  C2 every 0x800 chunk's +0xE stays within 0..8 (a misaligned walk breaks it);
  C3 POSITIVE CONTROL: the legacy walk (every .efx/.efb from +0x10 to EOF, as effect_type_usage.py) reproduces every
     row of effect-type-authored-usage.tsv exactly - so the new numbers differ only by the added inputs;
  C4 every listed embedded file exists and carries an EFX magic;
  C5 the 0xA00 payload's first byte (+0x10) is 0 in every record (the dispatch page's s2.8 statement);
  C7 EFX version magics counted per stream: EFX0009 ships exactly once and EFX0008 seven times (rejects "EFX0009 ships
     in no file"); regression pin
  C6 regression pins of the published answer: 55 distinct types; 0x04 = 173 chunks, 0xA3 = 447; no chunk of
     0x03, 0x07, 0x08, 0x70, 0x81, 0x8A, 0x97, 0xA0, 0xA4, 0xA9.
Output: type_census.tsv (per type: chunks and files per source, distinct assets, dispatch class) beside this script."""
import os, sys, struct, collections, csv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "D:/FFXII_TZA_extract"
EMB = os.path.join(HERE, "efx-embedded-stream-files.txt")
MAGICS = (b"EFX0010", b"EFX0009", b"EFX0008")


def rescan():
    hits = []
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if f.lower().endswith((".efx", ".efb")):
                continue
            p = os.path.join(dp, f)
            with open(p, "rb") as fh:
                b = fh.read()
            if b.find(b"EFX00") >= 0:
                hits.append(os.path.relpath(p, ROOT).replace("\\", "/"))
    with open(EMB, "w", newline="\n") as fo:
        fo.write("\n".join(sorted(hits)) + "\n")
    print("rescan: %d files with an embedded EFX magic" % len(hits))


def bound(b, i):
    sz = struct.unpack_from("<I", b, i + 0xC)[0]
    return i + sz if 0x10 <= sz and i + sz <= len(b) else len(b)


def walk(b, start, end):
    cur, out = start, []
    while cur + 8 <= end:
        ln, fl, ty = struct.unpack_from("<IHH", b, cur)
        if ln < 8 or cur + ln > end or fl != 0x100:
            return out, cur
        out.append((ty, cur))
        cur += ln
    return out, cur


MAGIC_COUNT = collections.Counter()


def streams(b):
    """yield (chunks, exact) for every EFX stream in b"""
    for m in MAGICS:
        i = b.find(m)
        while i >= 0:
            e = bound(b, i)
            ch, stop = walk(b, i + 0x10, e)
            MAGIC_COUNT[m.decode()] += 1
            yield ch, stop == e
            i = b.find(m, max(stop, i + 1))


def asset_key(rel):
    r = rel.split("/")
    if len(r) >= 4 and r[1] == "effect_finish":        # ps2data/effect_finish/<locale>/<cat>/<name>
        return "fx:" + "/".join(r[3:])
    return r[-1]


def main():
    if "--rescan" in sys.argv:
        rescan()
    fails = []
    std = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data")):
        std += [os.path.join(dp, f) for f in fn if f.lower().endswith((".efx", ".efb"))]
    emb_rel = [l.strip() for l in open(EMB) if l.strip()]
    chunks = {"std": collections.Counter(), "emb": collections.Counter()}
    files = {"std": collections.defaultdict(set), "emb": collections.defaultdict(set)}
    assets = collections.defaultdict(set)
    legacy_c, legacy_f = collections.Counter(), collections.defaultdict(set)
    sub8 = collections.Counter(); c1_bad = []; payload_nonzero = 0; n_streams = collections.Counter()
    c4_bad = []
    for src, paths in (("std", std), ("emb", [os.path.join(ROOT, r) for r in emb_rel])):
        for p in paths:
            if not os.path.isfile(p):
                c4_bad.append(p); continue
            b = open(p, "rb").read()
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            found = False
            for ch, exact in streams(b):
                found = True; n_streams[src] += 1
                if not exact:
                    c1_bad.append(rel)
                for ty, o in ch:
                    if ty == 0xA00:
                        t = b[o + 0xE]
                        chunks[src][t] += 1; files[src][t].add(rel); assets[t].add(asset_key(rel))
                        payload_nonzero += b[o + 0x10] != 0
                    elif ty == 0x800:
                        sub8[b[o + 0xE]] += 1
            if src == "emb" and not found:
                c4_bad.append(rel)
            if src == "std":                              # the legacy walk, for C3
                cur = 0x10
                while cur + 8 <= len(b):
                    ln, _f, ty = struct.unpack_from("<IHH", b, cur)
                    if ln < 8 or cur + ln > len(b):
                        break
                    if ty == 0xA00:
                        legacy_c[b[cur + 0xE]] += 1; legacy_f[b[cur + 0xE]].add(p)
                    cur += ln
    # C1
    print("C1 stream walks ending exactly at the declared size: std %d, emb %d; inexact %d"
          % (n_streams["std"], n_streams["emb"], len(c1_bad)))
    if c1_bad:
        fails.append("C1 %s" % c1_bad[:5])
    # C2
    print("C2 0x800 +0xE values:", sorted(sub8.items()))
    if not sub8 or max(sub8) > 8:
        fails.append("C2")
    # C3
    old = {}
    for r in csv.DictReader(open(os.path.join(HERE, "effect-type-authored-usage.tsv")), delimiter="\t"):
        old[int(r["type"], 16)] = (int(r["chunks"]), int(r["files"]))
    leg = {t: (legacy_c[t], len(legacy_f[t])) for t in legacy_c}
    c3 = old == leg
    print("C3 legacy walk reproduces effect-type-authored-usage.tsv (%d rows): %s" % (len(old), "PASS" if c3 else "FAIL"))
    if not c3:
        fails.append("C3 diff %s" % sorted(set(old.items()) ^ set(leg.items()))[:6])
    # C4
    print("C4 embedded list: %d files, %d missing or without magic" % (len(emb_rel), len(c4_bad)))
    if c4_bad or not emb_rel:
        fails.append("C4 %s" % c4_bad[:5])
    # C5
    total = sum(chunks["std"].values()) + sum(chunks["emb"].values())
    print("C5 0xA00 records %d, payload first byte non-zero in %d" % (total, payload_nonzero))
    if payload_nonzero:
        fails.append("C5")
    # classification from the dispatch tables
    cls = {}
    for r in csv.reader(open(os.path.join(HERE, "effect-type-methods.tsv")), delimiter="\t"):
        if not r or not r[0].startswith("0x"):
            continue
        t = int(r[0], 16)
        main_arm = any(x not in ("default", "-", "") for x in r[1:5])
        sub_arm = any(x not in ("default", "-", "") for x in r[5:9])
        cls[t] = "main" if main_arm else ("sub" if sub_arm else "none")
    types = sorted(set(chunks["std"]) | set(chunks["emb"]))
    allc = {t: chunks["std"][t] + chunks["emb"][t] for t in types}
    # C6
    pins_ok = (len(types) == 55 and allc.get(0x04) == 173 and allc.get(0xA3) == 447
               and all(allc.get(t, 0) == 0 for t in (0x03, 0x07, 0x08, 0x70, 0x81, 0x8A, 0x97, 0xA0, 0xA4, 0xA9)))
    print("C6 regression pins (55 types; 0x04 173; 0xA3 447; ten unauthored types zero): %s" % ("PASS" if pins_ok else "FAIL"))
    if not pins_ok:
        fails.append("C6")
    print("C7 EFX streams by magic:", dict(MAGIC_COUNT))
    if MAGIC_COUNT["EFX0009"] != 1 or MAGIC_COUNT["EFX0008"] != 7:
        fails.append("C7")
    with open(os.path.join(HERE, "type_census.tsv"), "w", newline="\n") as fo:
        fo.write("type\tclass\tchunks\tfiles\tchunks_efx_efb\tfiles_efx_efb\tchunks_embedded\tfiles_embedded\tdistinct_assets\n")
        for t in types:
            fo.write("0x%02X\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (
                t, cls.get(t, "?"), allc[t], len(files["std"][t]) + len(files["emb"][t]), chunks["std"][t],
                len(files["std"][t]), chunks["emb"][t], len(files["emb"][t]), len(assets[t])))
    nfiles = len({f for s in ("std", "emb") for v in files[s].values() for f in v})
    by_cls = collections.Counter(cls.get(t, "?") for t in types)
    single_chunk = [t for t in types if allc[t] == 1]
    single_file = [t for t in types if len(files["std"][t]) + len(files["emb"][t]) == 1]
    print("SUMMARY %d distinct types; %d 0xA00 records in %d files (%d .efx/.efb + %d embedded-stream files); "
          "classes %s; authored once: %s; in one file: %s"
          % (len(types), total, nfiles, len(std), len(emb_rel), dict(by_cls),
             ",".join("0x%02X" % t for t in single_chunk), ",".join("0x%02X" % t for t in single_file)))
    newly = [t for t in types if t not in old]
    print("types absent from the earlier census:", ",".join("0x%02X" % t for t in newly))
    for t in types:
        print("0x%02X %-4s chunks %5d (efx/efb %5d, embedded %4d)  files %4d  assets %4d  earlier %s"
              % (t, cls.get(t, "?"), allc[t], chunks["std"][t], chunks["emb"][t],
                 len(files["std"][t]) + len(files["emb"][t]), len(assets[t]), old.get(t, (0, 0))))
    print("FAILS %d" % len(fails))
    for f in fails:
        print("  FAIL", f)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
