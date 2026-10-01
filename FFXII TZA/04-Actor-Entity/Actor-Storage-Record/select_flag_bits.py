#!/usr/bin/env python3
"""select_flag_bits.py - query the ActorStorageRecord flag-bit writer census.

Population: every memory WRITE in all 38,161 listed bodies whose byte range covers one of the
flag offsets +0x08,+0x09,+0x0C,+0x0D,+0x0E,+0x13,+0x14 (bytes) or +0x1C (dword) - candidate
writers, not proven ActorStorageRecord writes. Triage with --census (functions already in the
route-proven access census) and by reading the base register / slice columns.

Examples:
  select_flag_bits.py --disp 0x1C                     all writes covering the flags1C dword
  select_flag_bits.py --disp 0x09 --bit 5             writes that can touch flags09 bit 5
  select_flag_bits.py --disp 0x1C --bit 8 --set       writes that can SET flags1C bit 8
  select_flag_bits.py --disp 0x13 --census            writes from census-known functions only
  select_flag_bits.py --disp 0x1C --summary           per-bit writer-class tally
"""
import io, sys, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
WRITES = os.path.join(HERE, "actor-storage-record-flag-bit-writes.tsv")
BITS   = os.path.join(HERE, "actor-storage-record-flag-bits.tsv")

def main():
    a = sys.argv[1:]
    def opt(name, default=None):
        return a[a.index(name)+1] if name in a else default
    disp = int(opt("--disp", "0"), 0)
    bit = int(opt("--bit", "-1"))
    want_census = "--census" in a
    want_set = "--set" in a
    want_summary = "--summary" in a

    if want_summary:
        hdr = None
        print("bit\twrites\tfns\tset_i\tset_r\tclr_i\tclr_r\tcpy_s\tcpy_c\tcpy_r\ttog\trmw\tinit")
        for i, l in enumerate(io.open(BITS, encoding="utf-8")):
            c = l.rstrip("\n").split("\t")
            if i == 0 or int(c[0],16) != disp: continue
            print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                c[1],c[2],c[3],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[13],c[14],c[18]))
        return

    n = 0
    for i, l in enumerate(io.open(WRITES, encoding="utf-8")):
        if i == 0:
            if "--noheader" not in a: sys.stdout.write(l)
            continue
        c = l.rstrip("\n").split("\t")
        if int(c[0],16) != disp: continue
        if want_census and c[12] != "y": continue
        if bit >= 0:
            lo, width, off = int(c[9],16), int(c[5]), disp
            ib = (off - lo)*8 + bit
            if not (0 <= ib < width*8): continue
            if c[10]:
                iv = int(c[10],16)
                if c[4] in ("set","copy","toggle") and not ((iv>>ib)&1): continue
                if c[4] == "clear" and ((iv>>ib)&1): continue
            if want_set and c[4] not in ("set","copy","rmw","arith"): continue
        n += 1
        sys.stdout.write(l)
    print("# %d rows" % n, file=sys.stderr)

if __name__ == "__main__":
    main()
