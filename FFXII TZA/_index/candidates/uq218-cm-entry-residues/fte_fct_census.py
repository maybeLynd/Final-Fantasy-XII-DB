"""@FTE / @FCT census over every .cm under the extract.

Record layout under test (from the readers):
  FTE: count u32@0x0C; u8 n@0x30 + u8 list@0x31..; records at 0x40 + i*0x20 (0053B6C3..0053B6CB: (idx+2)<<5 + FTE)
       rec {u32 bytes@0 (->00537AA0 GS alloc, 0053B740), u16 w@4, u16 h@6, u16 psm@8,
            u16 rrw@A, u16 rrh@C, u16 dpsm@E (0053B826..0053B8A7 BITBLTBUF/TRXREG),
            u32 @10 (not copied by 00504520), u32 dataBytes@14 (->res+0x18, IMAGE loop count),
            u32 dataOff@18 (->res+0x10, added to FTE base), u32 id@1C (00521290/005210F0)}
  FCT: records at 0x30 + i*0x10 (0053BB4D..0053BB59: (idx+3)<<4 + FCT)
       rec {u16 gsBytes@0 (00537AA0 at 0053BB73), u16 clutBytes@2 (IMAGE nloop = >>4),
            u8 rrw@4, u8 pages@5 (clamp 0053BB5D..0053BB68), u16 rrh@6, u32 id@8, u32 payOff@C (005044D0)}
"""
import struct, os, collections, sys
from lib import *

C = collections.Counter
fte = dict(files=0, recs=0, count=C(), fmt=C(), dpsm=C(), f10=C(), wh=C(), fmt_wh=C(),
           bytes_eq_rr4=C(), bytes_eq_data=C(), off_contig=C(), bytes_vs_whbpp=C(), id_form=C(),
           list_n=C(), list_in_range=C(), list_vals=C(), end_ok=C(), rr_by_fmt=C(), f10_by_fmt=C(),
           listn_eq_count=C())
fct = dict(files=0, recs=0, count=C(), gs=C(), clut=C(), rrw=C(), rrh=C(), pages=C(), pay_pages=C(),
           pages_match=C(), id_in_fte=C(), id_same_index=C(), clut_vs_fmt=C(), off_contig=C(),
           rr_clut=C(), gs_vs=C(), fct_count_vs_fte=C(), pages_by_dir=C(), end_ok=C())
examples = collections.defaultdict(list)

def bpp(fmt):
    return {0x13: 8, 0x14: 4, 0x00: 32, 0x01: 24, 0x02: 16, 0x0A: 16, 0x1B: 8, 0x24: 4, 0x2C: 4}.get(fmt)

for p in cm_files():
    d, es = cm_entries(p)
    base = os.path.basename(p)[:-3]
    top = p.replace('\\', '/').split('/in/')[1].split('/')[0]
    tags = {t: o for t, o in es}
    fte_ids = []
    fte_fmt_by_id = {}
    if '@FTE' in tags:
        e = entry(d, tags['@FTE'])
        fte['files'] += 1
        n = struct.unpack_from('<I', e, 0xC)[0]
        fte['count'][n] += 1
        ln = e[0x30]
        fte['list_n'][ln] += 1
        lst = list(e[0x31:0x31 + ln])
        fte['list_in_range'][all(x < n for x in lst)] += 1
        fte['listn_eq_count'][(ln == n, ln < n)] += 1
        for x in lst:
            fte['list_vals'][x] += 1
        expect = 0x40 + n * 0x20
        last_end = 0
        for i in range(n):
            r = 0x40 + i * 0x20
            b0, w, h, fmt, rrw, rrh, dpsm, f10, dbytes, doff, tid = struct.unpack_from('<IHHHHHHIIII', e, r)
            fte['recs'] += 1
            fte['fmt'][fmt] += 1
            fte['dpsm'][dpsm] += 1
            fte['f10'][f10] += 1
            fte['f10_by_fmt'][(fmt, f10)] += 1
            fte['wh'][(w, h)] += 1
            fte['fmt_wh'][(fmt, w, h)] += 1
            psz = {0: 4, 1: 4, 2: 2, 0x0A: 2}.get(dpsm)
            fte['bytes_eq_rr4'][(b0 == rrw * rrh * psz) if psz else 'dpsm?'] += 1
            fte['bytes_eq_data'][b0 == dbytes] += 1
            fte['off_contig'][doff == expect] += 1
            if doff != expect and len(examples['fte_noncontig']) < 5:
                examples['fte_noncontig'].append((base, i, hex(doff), hex(expect)))
            expect = doff + dbytes
            last_end = max(last_end, doff + dbytes)
            bp = bpp(fmt)
            fte['bytes_vs_whbpp'][('eq' if bp and b0 == w * h * bp // 8 else ('gt' if bp and b0 > w * h * bp // 8 else 'lt/other'), fmt)] += 1
            if bp and b0 != w * h * bp // 8 and len(examples['fte_size_ne']) < 8:
                examples['fte_size_ne'].append((base, i, hex(fmt), w, h, rrw, rrh, hex(b0)))
            fte['rr_by_fmt'][(fmt, dpsm, 'rrw*64' if rrw % 64 == 0 else 'rrw')] += 1
            # id form: letter<<24 | num<<4 | idx ?
            letter = chr(tid >> 24) if 0x20 < (tid >> 24) < 0x7F else '?'
            num = (tid >> 4) & 0xFFFFF
            idx = tid & 0xF
            digits = ''.join(ch for ch in base if ch.isdigit())
            form = (letter == base[0], str(num) == digits.lstrip('0') or (num == 0 and set(digits) <= {'0'}), idx == i)
            fte['id_form'][form] += 1
            if form != (True, True, True) and len(examples['fte_id_odd']) < 10:
                examples['fte_id_odd'].append((base, i, hex(tid)))
            fte_ids.append(tid)
            fte_fmt_by_id[tid] = fmt
            if fmt not in (0x13, 0x14) and len(examples['fte_fmt_other']) < 20:
                examples['fte_fmt_other'].append((base, i, hex(fmt), w, h, rrw, rrh, dpsm, hex(b0)))
        fte['end_ok'][last_end == len(e)] += 1
        if last_end != len(e) and len(examples['fte_end']) < 5:
            examples['fte_end'].append((base, hex(last_end), hex(len(e))))
    if '@FCT' in tags:
        e = entry(d, tags['@FCT'])
        fct['files'] += 1
        n = struct.unpack_from('<I', e, 0xC)[0]
        fct['count'][n] += 1
        fct['fct_count_vs_fte'][(n == len(fte_ids)) if fte_ids else 'noFTE'] += 1
        recs = [struct.unpack_from('<HHBBHII', e, 0x30 + i * 16) for i in range(n)]
        expect = 0x30 + n * 16
        for i, (gs, clut, rrw, pages, rrh, tid, off) in enumerate(recs):
            fct['recs'] += 1
            fct['gs'][gs] += 1
            fct['clut'][clut] += 1
            fct['rrw'][rrw] += 1
            fct['rrh'][rrh] += 1
            fct['rr_clut'][(rrw, rrh, clut, rrw * rrh * 4 == clut)] += 1
            fct['pages'][pages] += 1
            fct['pages_by_dir'][(top, pages)] += 1
            nxt = recs[i + 1][6] if i + 1 < n else len(e)
            span = nxt - off
            fct['off_contig'][off == expect] += 1
            expect = off + span
            pp = span / clut if clut else None
            fct['pay_pages'][pp] += 1
            fct['pages_match'][pp == pages] += 1
            if pp != pages and len(examples['fct_pages_ne']) < 10:
                examples['fct_pages_ne'].append((base, i, pages, pp, hex(clut), hex(span)))
            fct['id_in_fte'][tid in fte_ids] += 1
            fct['id_same_index'][(i < len(fte_ids) and fte_ids[i] == tid)] += 1
            if tid in fte_fmt_by_id:
                fct['clut_vs_fmt'][(hex(fte_fmt_by_id[tid]), clut >> 2)] += 1
            if tid not in fte_ids and len(examples['fct_id_notin']) < 10:
                examples['fct_id_notin'].append((base, i, hex(tid), [hex(x) for x in fte_ids]))
            fct['gs_vs'][(gs, clut)] += 1

out = []
def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s); out.append(s)
for name, D in (('FTE', fte), ('FCT', fct)):
    P('=====', name)
    for k, v in D.items():
        if isinstance(v, C):
            P(k, sorted(v.items(), key=lambda kv: (-kv[1], str(kv[0])))[:40])
        else:
            P(k, v)
P('===== examples')
for k, v in examples.items():
    P(k, v)
open(os.path.join(SCR, 'fte_fct_census.out'), 'w').write('\n'.join(out) + '\n')
