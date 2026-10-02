"""sab_param_census.py [VBF] - every .sab header's +0x05 / +0x0A from the archive, by folder (OPUS, 2026-10-01).

Settles the 18-Audio reconstruction-readiness map's item 33: the container page's "350 distinct values in .sab" and
the map sound list page's "strict ordinal ... one slot per folder ... 268 folders". Read-only; FAILS n against the
figures the pages now state (it refuses if the archive disagrees):
- 4,609 .sab files, all magic `sabf`; +0x05 is 0 in 512 and 1 in 4,097;
- every folder carries exactly one +0x0A value;
- 267 `se` folders under sead_data_win (no se003-se006), ordinals 0-267 with slot 3 unused, one per folder;
- 132 `shout` folders (66 jp, 66 us), 83 distinct values 5172-5256; a jp folder and its us namesake never share one;
- 267 + 83 = 350 distinct values in all.
"""
import collections
import os
import struct
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..",
                                                 "Tools", "dashboard")))
from ff12_content import vbf_load_index, vbf_read_entry  # noqa: E402

VBF = sys.argv[1] if len(sys.argv) > 1 else r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
SE = "ps2data/sound/se/sead_data_win/"


def main():
    with open(VBF, "rb") as f:
        names, blocks = vbf_load_index(f)
        sabs = sorted(n for n in names if n.lower().endswith(".sab"))
        val = {}
        b05 = collections.Counter()
        magic = collections.Counter()
        for n in sabs:
            b = vbf_read_entry(f, names, blocks, n)
            magic[b[:4]] += 1
            b05[b[5]] += 1
            val[n] = struct.unpack_from("<H", b, 0x0A)[0]
    by_folder = collections.defaultdict(set)
    for n, v in val.items():
        by_folder[os.path.dirname(n)].add(v)
    se = {k: v for k, v in by_folder.items() if k.startswith(SE)}
    sh = {k: v for k, v in by_folder.items() if "/shout/" in k}
    se_vals = set().union(*se.values())
    sh_vals = set().union(*sh.values())
    jp = {os.path.basename(k): next(iter(v)) for k, v in sh.items() if "/jp/" in k}
    us = {os.path.basename(k): next(iter(v)) for k, v in sh.items() if "/us/" in k}
    se_dirs = {n[len(SE):].split("/")[0] for n in names if n.startswith(SE) and "/" in n[len(SE):]}
    checks = [
        ("sab files", len(sabs), 4609),
        ("magic sabf", magic[b"sabf"], 4609),
        ("+0x05 == 0", b05[0], 512),
        ("+0x05 == 1", b05[1], 4097),
        ("folders with more than one +0x0A", sum(1 for v in by_folder.values() if len(v) > 1), 0),
        ("se folders holding .sab", len(se), 267),
        ("se directories in the archive", len(se_dirs), 267),
        ("se003-se006 present", len(se_dirs & {"se003", "se004", "se005", "se006"}), 0),
        ("se distinct values", len(se_vals), 267),
        ("se ordinals missing from 0-267", sorted(set(range(268)) - se_vals), [3]),
        ("shout folders", len(sh), 132),
        ("shout jp / us folders", (len(jp), len(us)), (66, 66)),
        ("shout distinct values", len(sh_vals), 83),
        ("shout range", (min(sh_vals), max(sh_vals)), (5172, 5256)),
        ("jp / us namesakes sharing a value", sum(1 for k in jp if us.get(k) == jp[k]), 0),
        ("distinct +0x0A overall", len(set(val.values())), 350),
    ]
    fails = 0
    for label, got, want in checks:
        ok = got == want
        fails += 0 if ok else 1
        print("%s %s: %s%s" % ("ok  " if ok else "FAIL", label, got, "" if ok else " (expected %s)" % (want,)))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
