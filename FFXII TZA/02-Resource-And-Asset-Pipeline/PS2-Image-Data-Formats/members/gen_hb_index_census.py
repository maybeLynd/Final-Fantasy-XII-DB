#!/usr/bin/env python3
"""Corpus validator for the handbook index family (hctg / hchk / hdat).

Walks the extracted corpus:
  Database/Tools/work/DATA/himg/   - <loc>__menuhandbook_<fam>[NNN].dat (hchk/hdat/himg)
  Database/Tools/work/DATA/hctg/   - <loc>__menuhandbook_<fam>.bin      (hctg)

Checks, per 2026-09-18 decode (hchk-hctg-hdat-handbook-indexes.md):
  * hctg: magic, recTableOff (+0x0A) bounds the 12B record table, count (+0x0E),
    hdat file count (+0x14) equals the shipped hdat enumeration.
  * hchk: magic, tag 103, count == hctg count; stride 8 for the five
    non-monster families, 16 (u16[8]) for monster; non-monster w6 (+0x06)
    monotonic non-decreasing; b3 (+0x03) is 0x00 on record 0 / 0x80 after
    (tutorial all 0x00; monster n/a).
  * hdat: magic, tag 103, +0x08 base-ordinal running-total chain,
    recOff[] table at +0x12, record envelope len = 12 + 4k with the
    fixed tail {00 80 | 00 80 | FF FF | FF | chapter}, records end at
    stringsOff, tim2Off lands on TIM2 or is 0xFFFFFFFF.
  * cross: hchk.count == hctg.count == sum(hdat.count) per family.

Usage: python gen_hb_index_census.py [--himg-dir ...] [--hctg-dir ...] [--out tsv]
"""
import os, re, struct, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(ROOT, "..", "..", "..", "..", "Tools", "work", "DATA"))
HIMG = os.path.join(WORK, "himg")
HCTG = os.path.join(WORK, "hctg")
FAMS = ["story", "world", "person", "knowledge", "tutorial", "monster"]
LOCS = ["ch", "cn", "de", "es", "fr", "in", "it", "kr", "us"]

fails = []
stats = collections.Counter()

def chk(cond, msg):
    if not cond:
        fails.append(msg)

def parse_hctg(b):
    chk(b[:4] == b"hctg", f"hctg bad magic")
    tag, f08, taboff, auxoff, cnt, f10, f12, hdatN, f16 = struct.unpack_from("<IHHHHHHHH", b, 4)
    # record table: cnt x 12B starting at taboff
    chk(0x18 <= taboff <= len(b), f"hctg taboff {taboff:#x} out of bounds")
    chk(taboff + cnt * 12 <= len(b), f"hctg table overruns file")
    return dict(tag=tag, f08=f08, taboff=taboff, auxoff=auxoff, cnt=cnt,
                f10=f10, f12=f12, hdatN=hdatN, f16=f16)

def parse_hchk(b, fam):
    chk(b[:4] == b"hchk", "hchk bad magic")
    tag, cnt, fw = struct.unpack_from("<IHH", b, 4)
    chk(tag == 103, f"hchk tag {tag}")
    stride = 16 if fam == "monster" else 8
    chk(0x0C + cnt * stride == len(b), f"hchk size mismatch cnt={cnt} stride={stride} len={len(b):#x}")
    recs = [b[0x0C + i * stride: 0x0C + (i + 1) * stride] for i in range(cnt)]
    return cnt, fw, recs

def parse_hdat(b):
    chk(b[:4] == b"hdat", "hdat bad magic")
    tag, base, cnt, tim2off, stroff = struct.unpack_from("<IHHIH", b, 4)
    chk(tag == 103, f"hdat tag {tag}")
    offs = struct.unpack_from("<%dH" % cnt, b, 0x12)
    chk(min(offs, default=0) >= 0x12 + 2 * cnt, "hdat recOff overlaps the table")
    prev = 0x12 + 2 * cnt
    badlen = badtail = 0
    for i, o in enumerate(offs):
        end = offs[i + 1] if i + 1 < cnt else stroff
        ln = end - o
        if ln < 12 or (ln - 12) % 4:
            badlen += 1
        rec = b[o:end]
        if len(rec) >= 8 and not (rec[-8:-4] == b"\x00\x80\x00\x80" and rec[-4:-2] == b"\xff\xff"):
            badtail += 1
        chk(prev <= o, "hdat recOff not monotonic"); prev = end
    chk(offs[-1] + (stroff - offs[-1]) == stroff, "hdat last record does not end at stringsOff")
    chk(stroff <= len(b), "hdat stroff out of bounds")
    if tim2off != 0xFFFFFFFF:
        chk(tim2off < len(b) and b[tim2off:tim2off + 4] == b"TIM2", "hdat tim2Off not TIM2")
    return dict(base=base, cnt=cnt, tim2off=tim2off, stroff=stroff,
                badlen=badlen, badtail=badtail)

def main():
    himg_dir, hctg_dir = HIMG, HCTG
    out = None
    a = sys.argv[1:]
    while a:
        if a[0] == "--himg-dir": himg_dir = a[1]; a = a[2:]
        elif a[0] == "--hctg-dir": hctg_dir = a[1]; a = a[2:]
        elif a[0] == "--out": out = a[1]; a = a[2:]
        else: a = a[1:]

    # index the .dat corpus by (loc, fam, kind, nnn)
    dats = collections.defaultdict(list)
    for n in os.listdir(himg_dir):
        m = re.match(r"(\w\w)__menuhandbook_(\w+?)(\d{3})?\.dat$", n)
        if not m: continue
        loc, fam, nnn = m.group(1), m.group(2), m.group(3)
        dats[(loc, fam)].append((nnn, n))

    rows = []
    for loc in LOCS:
        for fam in FAMS:
            # hctg
            hb = open(os.path.join(hctg_dir, f"{loc}__menuhandbook_{fam}.bin"), "rb").read()
            h = parse_hctg(hb)
            files = dats.get((loc, fam), [])
            unnum = [n for nnn, n in files if nnn is None]
            numd = sorted([(nnn, n) for nnn, n in files if nnn is not None])
            chk(len(unnum) == 1, f"{loc}/{fam}: {len(unnum)} unnumbered .dat")
            # hchk
            kb = open(os.path.join(himg_dir, unnum[0]), "rb").read()
            kcnt, kfw, krecs = parse_hchk(kb, fam)
            chk(kcnt == h["cnt"], f"{loc}/{fam}: hchk {kcnt} != hctg {h['cnt']}")
            if fam != "monster":
                w6 = [struct.unpack_from("<H", r, 6)[0] for r in krecs]
                live = [x for x in w6 if x != 0xFFFF]
                chk(all(live[i] <= live[i + 1] for i in range(len(live) - 1)),
                    f"{loc}/{fam}: hchk w6 not monotonic")
                b3 = [r[3] for r in krecs]
                if fam == "tutorial":
                    chk(set(b3) == {0}, f"{loc}/{fam}: tutorial b3 != 0")
                else:
                    chk(b3[0] == 0 and set(b3[1:]) == {0x80}, f"{loc}/{fam}: b3 pattern")
            # hdat chain
            hdats = [(nnn, n) for nnn, n in numd
                     if open(os.path.join(himg_dir, n), "rb").read(4) == b"hdat"]
            himgs = [(nnn, n) for nnn, n in numd
                     if open(os.path.join(himg_dir, n), "rb").read(4) == b"himg"]
            chk(len(hdates := hdats) == h["hdatN"],
                f"{loc}/{fam}: {len(hdats)} hdat files != hctg +0x14 {h['hdatN']}")
            run = hdat_total = 0
            for nnn, n in sorted(hdates):
                b = open(os.path.join(himg_dir, n), "rb").read()
                hd = parse_hdat(b)
                chk(hd["base"] == run, f"{n}: baseOrdinal {hd['base']} != running {run}")
                run += hd["cnt"]; hdat_total += hd["cnt"]
                stats["badlen"] += hd["badlen"]; stats["badtail"] += hd["badtail"]
                stats["hdat_rec"] += hd["cnt"]
            chk(hdat_total == h["cnt"], f"{loc}/{fam}: hdat total {hdat_total} != {h['cnt']}")
            # resource enumeration: hdat first, then himg, contiguous numbering
            nnn_hd = sorted(int(x) for x, _ in hdats)
            nnn_hi = sorted(int(x) for x, _ in himgs)
            chk(nnn_hd == list(range(len(nnn_hd))), f"{loc}/{fam}: hdat numbering gap")
            if nnn_hi:
                chk(min(nnn_hi) == len(nnn_hd), f"{loc}/{fam}: himg starts at {min(nnn_hi)} != {len(nnn_hd)}")
            rows.append((loc, fam, h["cnt"], h["hdatN"], hdat_total, kcnt,
                         len(himgs), h["tag"], h["f16"]))
            stats["files"] += 2 + len(numd)

    if out:
        with open(out, "w", newline="") as o:
            o.write("loc\tfamily\thctg_count\thdat_files\thdat_records\thchk_count\thimg_files\ttag\tf16\n")
            for r in rows:
                o.write("\t".join(map(str, r)) + "\n")

    print(f"files checked: {stats['files']}  hdat records: {stats['hdat_rec']}  "
          f"bad len: {stats['badlen']}  bad tail: {stats['badtail']}")
    print(f"rows: {len(rows)} (loc x family)")
    if fails:
        print(f"FAILURES: {len(fails)}")
        for f in fails[:40]:
            print("  ", f)
        sys.exit(1)
    print("ALL CHECKS PASS")

if __name__ == "__main__":
    main()
