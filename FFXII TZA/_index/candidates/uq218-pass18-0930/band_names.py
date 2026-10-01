"""UQ-218: classifier band -> @FMN name, by the code path, measured over every shipped .ca (SWE2-DATA 2026-09-30).

Code path (certified image 73461d08...):
  op 0x0A byte[cmd+2] = selector kind; kinds 0 / 0xA / 0xB call the locomotion classifier 004256E0 with arg 0 / 1 / 2.
  004256E0 returns band + ((1 - esi) << 16).  op 0x0B handler 00417110 takes list index i = result & 0xFFFF,
  offset h = result >> 16, and issues a synthetic op 0x01 for track word[cmd+6+2i] + h (00417367 add cx, r15w).
  op 0x01 (00417920) / 0041CD30: the track is the @FMC RECORD index inside the bound @FMC entry (records walked by
  their u16 +4 length from entry+0x30).  The record's op 0x09 (00417F40) selects @FMN index word[cmd+2] >> 1
  (+ s16[ctx+0x2A]); this census reads the index as the .ca slot and REPORTS how often that slot holds an @FMN (the
  control on the reading).
Output: per (kind, band, offset) the distribution of @FMN name stems (digits stripped).
"""
import collections, glob, os, re, struct, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract/ps2data/obj_finish"
files = sorted(glob.glob(os.path.join(ROOT, "**", "*.ca"), recursive=True))


def stem(n):
    return re.sub(r"\d+$", "", n)


def walk(d, o):
    elen = struct.unpack_from("<I", d, o + 8)[0]
    rend = o + elen
    rcount = struct.unpack_from("<I", d, o + 0x0C)[0]
    ro, recs = o + 0x30, []
    for _ in range(rcount):
        if ro + 6 > rend:
            break
        subc = d[ro + 3]
        rlen = struct.unpack_from("<H", d, ro + 4)[0]
        cmds, so = [], ro + 6
        for _ in range(subc):
            key, cw = struct.unpack_from("<HH", d, so)
            slen = (cw >> 6) & 0x3FF
            co, cend = so + 4, so + slen
            while co + 2 <= cend:
                head = struct.unpack_from("<H", d, co)[0]
                op, l = head & 0x7F, (head >> 7) & 0x1FF
                if l < 2 or co + l > cend:
                    break
                cmds.append((op, d[co:co + l]))
                co += l
            so = cend
        recs.append(cmds)
        if rlen < 6:
            break
        ro += rlen
    return recs


tab = collections.defaultdict(collections.Counter)
ctrl = collections.Counter()
nsel = collections.Counter()
for p in files:
    d = open(p, "rb").read()
    if len(d) < 0x40:
        continue
    var, _clen, cnt = struct.unpack_from("<III", d, 4)
    base = 0x40 if var == 1 else 0x30
    slots = {}
    for i in range(cnt):
        v = struct.unpack_from("<I", d, base + i * 4)[0]
        if var == 1 and v == 0:
            continue
        o = base + v
        if o + 0x30 > len(d):
            continue
        slots[i] = (o, d[o:o + 4], d[o + 0x10:o + 0x30].split(b"\0")[0].decode("ascii", "replace"))
    for i, (o, tag, nm) in slots.items():
        if tag != b"@FMC":
            continue
        recs = walk(d, o)
        for cmds in recs:
            kind = None
            for op, b in cmds:
                if op == 0x0A and len(b) >= 6:
                    kind = b[2]
                elif op == 0x0B and kind in (0x00, 0x0A, 0x0B) and len(b) >= 6:
                    cnt_l = struct.unpack_from("<H", b, 4)[0]
                    lst = [struct.unpack_from("<H", b, 6 + 2 * k)[0] for k in range(cnt_l) if 6 + 2 * k + 2 <= len(b)]
                    nsel[kind] += 1
                    for band, t0 in enumerate(lst):
                        for h in (0, 1):
                            t = t0 + h
                            if t >= len(recs):
                                ctrl["track out of range"] += 1
                                continue
                            ops9 = [x for x in recs[t] if x[0] == 0x09]
                            if not ops9:
                                tab[(kind, band, h)]["<no op09>"] += 1
                                continue
                            idx = struct.unpack_from("<H", ops9[0][1], 2)[0] >> 1
                            s = slots.get(idx)
                            if s and s[1] == b"@FMN":
                                ctrl["op09 slot is @FMN"] += 1
                                tab[(kind, band, h)][stem(s[2])] += 1
                            else:
                                ctrl["op09 slot NOT @FMN"] += 1
                                tab[(kind, band, h)]["<slot %s>" % (s[1] if s else None)] += 1
print("files", len(files), "selector commands by kind", dict(nsel))
print("control", dict(ctrl))
for k in sorted(tab):
    c = tab[k]
    tot = sum(c.values())
    top = ", ".join("%s %d" % (n, v) for n, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:5])
    print("kind 0x%02X band %2d off %d  n=%5d  %s" % (k[0], k[1], k[2], tot, top))


# ---- checks: the side-step and turn bindings are exclusive (the yaw-sign reading) ----
def count(kind_set, band, off, pred):
    return sum(v for (k, b, h), c in tab.items() if k in kind_set and b == band and h == off
               for n, v in c.items() if pred(n))

fails = 0
def check(name, ok, detail):
    global fails
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    fails += 0 if ok else 1

side = lambda s: (lambda n: n.startswith(s))
K = (0x00, 0x0A)
for off in (0, 1):
    wl3, wr3 = count(K, 3, off, side("walk_l")), count(K, 3, off, side("walk_r"))
    wl4, wr4 = count(K, 4, off, side("walk_l")), count(K, 4, off, side("walk_r"))
    check("S%d band 3 -> walk_l only" % off, wl3 > 0 and wr3 == 0, "walk_l %d / walk_r %d" % (wl3, wr3))
    check("S%d band 4 -> walk_r only" % off, wr4 > 0 and wl4 == 0, "walk_r %d / walk_l %d" % (wr4, wl4))
tl0 = count((0x00, 0x0B), 6, 0, lambda n: n.endswith("trn_l")); tr0 = count((0x00, 0x0B), 6, 0, lambda n: n.endswith("trn_r"))
tl1 = count((0x00, 0x0B), 6, 1, lambda n: n.endswith("trn_l")); tr1 = count((0x00, 0x0B), 6, 1, lambda n: n.endswith("trn_r"))
check("T band 6: offset 0 (turn delta >= 0) -> trn_l, offset 1 -> trn_r", tl0 > 0 and tr0 == 0 and tr1 > 0 and tl1 == 0,
      "off0 trn_l %d trn_r %d | off1 trn_r %d trn_l %d" % (tl0, tr0, tr1, tl1))
hl = count((0x00,), 7, 0, lambda n: n.endswith("hi_trn_l")); hr = count((0x00,), 7, 0, lambda n: n.endswith("hi_trn_r"))
check("T7 band 7 offset 0 -> hi_trn_l", hl > 0 and hr == 0, "hi_trn_l %d hi_trn_r %d" % (hl, hr))
rl = count((0x0A,), 9, 0, side("run_l_")); rr = count((0x0A,), 9, 0, side("run_r_"))
rl10 = count((0x0A,), 10, 0, side("run_l_")); rr10 = count((0x0A,), 10, 0, side("run_r_"))
check("R kind 0xA: band 9 -> run_l_*, band 10 -> run_r_*", rl > 0 and rr == 0 and rr10 > 0 and rl10 == 0,
      "b9 run_l %d run_r %d | b10 run_r %d run_l %d" % (rl, rr, rr10, rl10))
check("C control: every op 0x09 index read as a .ca slot lands on an @FMN", ctrl["op09 slot NOT @FMN"] == 0,
      "%d on @FMN, %d not" % (ctrl["op09 slot is @FMN"], ctrl["op09 slot NOT @FMN"]))

# ---- static: the code path the join follows (certified image) ----
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d as IMG, off  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
_md = Cs(CS_ARCH_X86, CS_MODE_64)
def _ins(a):
    o = off(a); x = next(_md.disasm(IMG[o:o + 16], a)); return "%s %s" % (x.mnemonic, x.op_str)
EXPECT = {
    0x00417281: "movzx r14d, dx",                        # list index = result & 0xFFFF
    0x0041727D: "sar r15d, 0x10",                        # track offset = result >> 16
    0x0041735C: "movzx ecx, word ptr [r13 + r14*2 + 6]", # list[index]
    0x00417367: "add cx, r15w",                          # + offset
    0x0041CDC8: "mov dword ptr [rdx + 0x80], r11d",      # the track is the record index (0041CD30)
    0x004258C6: "subss xmm1, xmm0",                      # heading(+0x244) - facing(+0x124)
    0x00425919: "mov ebx, 3",                            # (45, 135] -> band 3
    0x00425931: "mov ebx, 4",                            # [-135, -45) -> band 4
    0x0042576B: "subss xmm6, xmm1",                      # facing(+0x124) - previous facing(+0x254)
    0x0042588F: "setae sil",                             # esi = (turn >= 0); offset = 1 - esi
}
_bad = ["%08X %s" % (a, _ins(a)) for a, t in EXPECT.items() if _ins(a) != t]
check("P the code path", not _bad, "%d sites%s" % (len(EXPECT), "" if not _bad else " - " + "; ".join(_bad)))
print("FAILS %d" % fails)
