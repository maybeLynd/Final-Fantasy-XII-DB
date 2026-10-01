"""Join @FDM key tables, @FDM part descriptors and the @FTR tail-slot count (+0x38).

Code chain (STATIC):
  command 0x14 -> 00521050 -> 005048A0 key -> ordinal -> 00373060(res, ordinal, w6):
      bound ordinal < u16[FTR+0x38] (003730BA), store w6 into slot[ordinal] of the u16 region at
      core + count*0x292 (00373094), set res flag 0x1000 (003730D6).
  draw builder 0053AB50: part record r13 = FDM + u16 list[FDM+0x34+4k]+4 [idx] (0053C308..0053C31D)
      slotA = (dword[r13+4] >> 8) & 0x3FF (0x3FF = none), slotB = (dword[r13+4] >> 18) & 0x3FF
      value = 00371330(res, slot) (u16 tail slot), 0x7FFF -> default s8[r13+2] / s8[r13+3].
Census: (1) FDM key count vs FTR +0x38; (2) every descriptor slot field < FTR +0x38 (or 0x3FF);
(3) do the slot numbers used by descriptors cover 0..n-1.
"""
import struct, os, collections
from lib import *
C = collections.Counter
join = C(); slot_ok = C(); cover = C(); nparts = 0; ex = collections.defaultdict(list)
slotvals = C(); bits = C(); defaults = C(); b8 = C()
for p in cm_files():
    d, es = cm_entries(p)
    base = os.path.basename(p)[:-3]
    tags = {t: o for t, o in es}
    ftr = entry(d, tags['@FTR'])
    tail = struct.unpack_from('<I', ftr, 0x38)[0]
    if '@FDM' not in tags:
        join[('noFDM', tail == 0)] += 1
        continue
    f = entry(d, tags['@FDM'])
    kt = struct.unpack_from('<H', f, 0x32)[0]
    nkeys = struct.unpack_from('<I', f, kt)[0]
    join[('keys==tail', nkeys == tail)] += 1
    if nkeys != tail and len(ex['join']) < 10:
        ex['join'].append((base, nkeys, tail))
    used = set()
    seen = set()
    for k in range(3):
        lo = struct.unpack_from('<I', f, 0x34 + 4 * k)[0]
        if lo == 0xFFFFFFFF:
            continue
        n = struct.unpack_from('<I', f, lo)[0]
        for j in range(n):
            ro = struct.unpack_from('<H', f, lo + 4 + 2 * j)[0]
            if ro in seen:
                continue
            seen.add(ro)
            nparts += 1
            b0, b1, da, db, w = struct.unpack_from('<BBbbI', f, ro)
            sa = (w >> 8) & 0x3FF
            sb = (w >> 18) & 0x3FF
            for s, dflt in ((sa, da), (sb, db)):
                if s == 0x3FF:
                    slot_ok['none'] += 1
                else:
                    slot_ok[s < tail] += 1
                    used.add(s)
                    if s >= tail and len(ex['slot']) < 10:
                        ex['slot'].append((base, hex(ro), s, tail))
            bits[(w & 1, (w >> 28) & 1, (w >> 29) & 1)] += 1
            slotvals[(sa != 0x3FF, sb != 0x3FF)] += 1
            defaults[(da, db)] += 1
            b8[(b0, b1)] += 1
    if tail:
        cover[('slots used == 0..tail-1', used == set(range(tail)))] += 1
        if used != set(range(tail)) and len(ex['cover']) < 6:
            ex['cover'].append((base, tail, sorted(used)[:12], len(used)))
print('FDM key count vs FTR +0x38:', sorted(join.items(), key=str))
print('distinct part descriptors walked', nparts)
print('slot fields: <tail / none:', dict(slot_ok))
print('(slotA present, slotB present):', dict(slotvals))
print('(bit0, bit28, bit29):', sorted(bits.items()))
print('defaults (s8 +2, s8 +3) top:', defaults.most_common(8))
print('bytes (+0, +1) top:', b8.most_common(8))
print('slot coverage:', dict(cover))
for k, v in ex.items():
    print('ex', k, v)
