# sp1_counts.py - OV-33 (i) data gap: the polyline copy 002DE800 never bounds dword [src+0x14]; its only authored route
# is 003631B0 -> 003638B0 -> 002DEFA0 with an SP1 emitter record. Over every shipped .mpk slot-16 SP1 block, walk the
# region-C record index {u16 bound; u16 off[]} (record = SP1 + off, as the walker computes it) and report, per record,
# shape = byte[+9] & 0x7F and count = u32[+0x14]. Question: is any class-2 (multi-point) count >= 128 (overflows the
# 128-point area at 0215E734) or >= 140 (reaches 0215EFF4)?
# Control: the map-ctrl page's census says 2,326 records, 400 of shape 2, count 1 in 2,265 - the totals must reproduce.
#
# Usage: python t1b_sp1_counts.py [VBF]   (default: the shipped FFXII_TZA.vbf)
# Terminal status (repair of ASTRA-CONTRA-FABLE-OV33-SP1-PREREQUISITE-0930; before it, a corpus with no .mpk printed
# "CONTROL ... MISMATCH (0, 0, 0)" and then "FAILS 0" with exit 0):
#   the last line is "STATUS COMPLETE" or "STATUS INCOMPLETE: <reasons>";
#   exit 0 = COMPLETE and no count >= 128; exit 1 = COMPLETE with a count >= 128 (a finding); exit 2 = INCOMPLETE
#   (control mismatch, no packs, or any malformed pack / record index / referenced record). An INCOMPLETE run
#   prints no FAILS line, so nothing downstream can read "FAILS 0" from it.
import sys, os, struct, collections, hashlib
sys.path.insert(0, 'C:/Users/Kristian/source/repos/XIIOnline/agent_flow/tools')
import vbfextract
VBF_DEFAULT = r"D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FFXII_TZA.vbf"
CONTROL = (2326, 400, 2265)


def slot16(d, s):
    cnt = struct.unpack_from('<I', d, 0)[0]
    sz = struct.unpack_from('<32I', d, 4)
    off = ((cnt + 1) * 4 + 0x3F) & ~0x3F
    for i in range(32):
        if sz[i]:
            off += 0x40
            if i == s:
                return d[off:off + sz[i]]
            off += sz[i]
    return None


def census(entries):
    """entries: iterable of (pack name, pack bytes). Returns the census dict; never raises on malformed input."""
    r = dict(packs=0, sp1=0, no_region_c=0, recs=0, shape=collections.Counter(), cnt1=0, big=[], top=[],
             bad_pack=[], bad_index=[], bad_ref=[])
    for p, d in entries:
        r["packs"] += 1
        short = p.split('/')[-1]
        try:
            b = slot16(d, 16)
        except struct.error:
            r["bad_pack"].append(short); continue
        if b is None or len(b) < 0x20 or b[:4] != b'SP1\0':
            continue                                   # no SP1 block in this pack: not an SP1 input
        r["sp1"] += 1
        offC = struct.unpack_from('<I', b, 0x0C)[0]
        if not offC:
            r["no_region_c"] += 1; continue            # SP1 without a region-C index
        try:
            bound = struct.unpack_from('<H', b, offC)[0]
            offs = struct.unpack_from('<%dH' % bound, b, offC + 2)
        except struct.error:
            r["bad_index"].append(short); continue     # index header or offset array past the block
        for o in offs:
            if not o:
                continue                               # empty slot in the index
            if o + 0x40 > len(b):
                r["bad_ref"].append((short, hex(o))); continue
            r["recs"] += 1
            sh = b[o + 9] & 0x7F
            n = struct.unpack_from('<I', b, o + 0x14)[0]
            r["shape"][sh] += 1
            r["cnt1"] += (n == 1)
            if sh == 2:
                r["top"].append((n, short, hex(o)))
            if sh == 2 and n >= 128:
                r["big"].append((n, short, hex(o)))
    r["top"].sort(reverse=True)
    return r


def verdict(r):
    got = (r["recs"], r["shape"][2], r["cnt1"])
    why = []
    if r["packs"] == 0:
        why.append("no .mpk packs in the input")
    if got != CONTROL:
        why.append("control mismatch %s != %s" % (got, CONTROL))
    for k in ("bad_pack", "bad_index", "bad_ref"):
        if r[k]:
            why.append("%d %s" % (len(r[k]), k))
    return got, why


def main(vbf):
    f = open(vbf, 'rb')
    names, blocks = vbfextract.load_index(f)          # raises on a non-VBF (bad magic): exit 1 with a traceback
    packs = sorted(n for n in names if n.lower().endswith('.mpk'))
    me = open(os.path.abspath(__file__), 'rb').read()
    st = os.stat(vbf)
    print("input %s  size %d  mtime %d  packs-list sha256 %s" % (vbf, st.st_size, int(st.st_mtime),
          hashlib.sha256("\n".join(packs).encode()).hexdigest()[:16]))
    print("producer sha256 %s" % hashlib.sha256(me).hexdigest())
    r = census((p, vbfextract.read_entry(f, names, blocks, p)) for p in packs)
    got, why = verdict(r)
    print("packs %d  SP1 blocks %d (no region C %d)  records %d  shapes %s  count==1 %d" % (
        r["packs"], r["sp1"], r["no_region_c"], r["recs"], dict(sorted(r["shape"].items())), r["cnt1"]))
    print("malformed: packs %d, record indexes %d, referenced records %d %s" % (
        len(r["bad_pack"]), len(r["bad_index"]), len(r["bad_ref"]), (r["bad_pack"] + r["bad_index"] + r["bad_ref"])[:6]))
    print("CONTROL page census: records %d, shape-2 %d, count==1 %d ->" % CONTROL,
          "PASS" if got == CONTROL else "MISMATCH (%d, %d, %d)" % got)
    print("largest shape-2 counts:", r["top"][:8])
    if why:
        print("STATUS INCOMPLETE: " + "; ".join(why))
        return 2
    print("shape-2 records with count >= 128:", r["big"] if r["big"] else "NONE")
    print("FAILS", len(r["big"]))
    print("STATUS COMPLETE")
    return 1 if r["big"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else VBF_DEFAULT))
