#!/usr/bin/env python3
"""Resolve import-table calls that the function call graph cannot see.

`edges.tsv` records function-to-function edges from direct calls. It reported **one** caller for
`rand` while **thirty** functions call it -- because an imported function is reached by `FF 15`
through a pointer slot, not by `E8` to an address.

Measured 2026-09-02: **417 of 538 import slots are called, across 3,543 indirect call sites**, none
of which appear in the call graph. Any claim of the form "who calls X" is understated whenever X is
imported.

Two findings came out of it on the day it was written:
  * `rand` is a **gameplay** RNG -- 48 sites across 30 functions, including Movement, Combat Action
    (`BattleAction_ComputeChargeLimitTicks`) and Lua's `math.random`. It had been recorded as the
    sound driver's own generator.
  * Steam registers exactly **8** callbacks (`SteamAPI_RegisterCallback`, 8 sites) and unregisters
    8 -- matching the 8 RTTI `CCallback<>` classes, with **none** for matchmaking or networking.

Usage:
  iat_xrefs.py                   # busiest imports by call site count
  iat_xrefs.py --filter steam    # only imports whose dll!symbol matches
  iat_xrefs.py --callers rand    # list the calling functions for matching imports
"""
import argparse
import bisect
import collections
import csv
import io
import struct
import kit_paths as KP  # noqa: E402
import os

EXE = r"D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe"
G = os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--filter", default=None, help="only imports whose dll!symbol contains this")
    ap.add_argument("--callers", default=None, help="also list calling functions for matches")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--exe", default=EXE)
    ap.add_argument("--functions", default=G)
    a = ap.parse_args()

    d = io.open(a.exe, "rb").read()
    e = struct.unpack_from("<I", d, 0x3C)[0]
    optsz = struct.unpack_from("<H", d, e + 20)[0]
    ib = struct.unpack_from("<Q", d, e + 24 + 24)[0]
    nsec = struct.unpack_from("<H", d, e + 6)[0]
    opt = e + 24
    base = e + 24 + optsz
    secs = []
    for i in range(nsec):
        o = base + 40 * i
        nm = d[o:o + 8].rstrip(b"\0").decode()
        vs, va, rs, pr = struct.unpack_from("<IIII", d, o + 8)
        secs.append((nm, va, max(vs, rs), pr))

    def r2o(rva):
        for nm, va, sz, pr in secs:
            if va <= rva < va + sz:
                return pr + (rva - va)

    # every IAT slot RVA -> "dll!symbol"
    slot_name = {}
    imp_rva, _sz = struct.unpack_from("<II", d, opt + 112 + 1 * 8)
    o = r2o(imp_rva)
    while True:
        oft, _ts, _fc, namerva, firstthunk = struct.unpack_from("<IIIII", d, o)
        if namerva == 0:
            break
        dll = d[r2o(namerva):].split(b"\0")[0].decode()
        t = r2o(oft) if oft else r2o(firstthunk)
        k = 0
        while True:
            v = struct.unpack_from("<Q", d, t + 8 * k)[0]
            if v == 0:
                break
            if v & (1 << 63):
                nm = "ordinal%d" % (v & 0xFFFF)
            else:
                nm = d[r2o(v) + 2:].split(b"\0")[0].decode()
            slot_name[firstthunk + 8 * k] = "%s!%s" % (dll.split(".")[0], nm)
            k += 1
        o += 20

    tx = [s for s in secs if s[0] == ".text"][0]
    lo_rva, sz, pr = tx[1], tx[2], tx[3]
    raw = d[pr:pr + sz]
    rows = sorted((int(r["entry"], 16), int(r["body_bytes"]), r)
                  for r in csv.DictReader(io.open(a.functions, encoding="utf-8"), delimiter="\t"))
    starts = [r[0] for r in rows]

    def owner(va):
        i = bisect.bisect_right(starts, va) - 1
        if i >= 0 and rows[i][0] <= va < rows[i][0] + rows[i][1]:
            return rows[i][2]

    sites = collections.Counter()
    fns = collections.defaultdict(set)
    for i in range(len(raw) - 6):
        if raw[i] == 0xFF and raw[i + 1] == 0x15:
            disp = struct.unpack_from("<i", raw, i + 2)[0]
            slot_rva = lo_rva + i + 6 + disp
            if slot_rva in slot_name:
                sites[slot_rva] += 1
                f = owner(ib + lo_rva + i)
                if f:
                    fns[slot_rva].add((f["entry"], f.get("name") or "-", f.get("owner") or "-"))

    print("import slots referenced by an FF 15 call: %d of %d" % (len(sites), len(slot_name)))
    print("total indirect call sites through the IAT: %d" % sum(sites.values()))

    key = a.callers or a.filter
    if key:
        out = sorted(((s, n) for s, n in sites.items() if key.lower() in slot_name[s].lower()),
                     key=lambda x: -x[1])
        print("\nimports matching %r:" % key)
    else:
        out = sites.most_common(a.top)
        print("\nbusiest %d imports by call site count:" % a.top)

    print("%-46s %6s %7s" % ("dll!symbol", "sites", "callers"))
    for slot, n in out:
        print("%-46s %6d %7d" % (slot_name[slot][:46], n, len(fns[slot])))
        if a.callers:
            for ent, nm, ow in sorted(fns[slot]):
                print("      %s %-36s [%s]" % (ent, nm[:36], ow[:24]))


if __name__ == "__main__":
    main()
