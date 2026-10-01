"""gen_vif_templates.py: emit members/vif1-packet-templates.tsv - one row per
pre-built VIF1 packet template (66 startup objects + 37 MPG builders).

Columns: family, builder, object, memset_size, header_kind, mpg_program,
mpg_addr, command_sequence, gif_writes, unattributed_stores, payload_stores.
"""
import struct, json, collections, importlib.util, os
spec = importlib.util.spec_from_file_location(
    'vt', os.path.join(os.path.dirname(__file__), 'vif_templates.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

GSREG = {0x00:'PRIM',0x01:'RGBAQ',0x02:'ST',0x03:'UV',0x04:'XYZF2',0x05:'XYZ2',
         0x06:'TEX0_1',0x07:'TEX0_2',0x08:'CLAMP_1',0x09:'CLAMP_2',0x0A:'FOG',
         0x0B:'XYZF3',0x0C:'TEX1_1',0x0D:'TEX1_2',0x0E:'A+D',0x0F:'XYZ3',
         0x14:'TEXA',0x34:'SCISSOR_1',0x35:'SCISSOR_2',0x36:'ALPHA_1',
         0x37:'ALPHA_2',0x38:'DIMX',0x39:'DTHE',0x3A:'COLCLAMP',0x3B:'ZBUF_1',
         0x3C:'ZBUF_2',0x3D:'FRAME_1',0x3E:'FRAME_2',0x3F:'TEXCLUT',
         0x40:'TEX2_1',0x41:'TEX2_2',0x42:'TEXA',0x44:'FOGCOL',0x45:'TEXA_2',
         0x46:'PRMODECONT',0x47:'TEXCLUT_2',0x4C:'TEX2',0x4D:'XYOFFSET_1',
         0x4E:'XYOFFSET_2',0x51:'MIPTBP1_1',0x52:'MIPTBP1_2',0x53:'MIPTBP2_1',
         0x54:'MIPTBP2_2',0x5C:'MIPTBP1_1b',0x61:'FINISH',0x62:'LABEL',0x63:'SIGNAL'}

def decode_gif(buf_bytes):
    """Decode one DIRECT payload as a GIF packet; return list of (regname,value)
    for PACKED/REGLIST register writes. IMAGE/terminator -> []."""
    out = []
    pos = 0
    while pos + 16 <= len(buf_bytes):
        tag, regs = struct.unpack_from('<QQ', buf_bytes, pos)
        pos += 16
        nloop = tag & 0x7FFF
        eop = (tag >> 15) & 1
        flg = (tag >> 58) & 3
        nreg = (tag >> 60) & 0xF or 16
        desc = [(regs >> (4 * i)) & 0xF for i in range(nreg)]
        if flg == 0:      # PACKED
            for _ in range(nloop):
                for rd in desc:
                    if pos + 16 > len(buf_bytes): return out
                    lo, hi = struct.unpack_from('<QQ', buf_bytes, pos); pos += 16
                    if rd == 0x0E:
                        out.append((GSREG.get(hi & 0x7F, '0x%02X' % hi), lo))
                    elif rd <= 0x0F or rd in GSREG:
                        out.append((GSREG.get(rd, '0x%02X' % rd), (lo, hi)))
        elif flg == 1:    # REGLIST
            total = nreg * nloop
            total += total & 1  # padded to even
            for i in range(total):
                if pos + 8 > len(buf_bytes): return out
                lo = struct.unpack_from('<Q', buf_bytes, pos)[0]; pos += 8
                if i < nreg * nloop:
                    rd = desc[i % nreg]
                    out.append((GSREG.get(rd, '0x%02X' % rd), lo))
        else:             # IMAGE / no reg list
            pos += nloop * 16
        if eop: break
    return out

def build_row(fam, a, obj, calls, stores):
    memset = [c for c in calls if c[0] == 'memset']
    hdr = [c for c in calls if c[0] == 'header']
    mpg = [c for c in calls if c[0] == 'mpg']
    # apply the helper stamps so the buffer matches the final object:
    # 008631D0 writes word=dx @X, kind 0x10 @X+3, dword 0 @X+4
    patches = []
    sub_at = set()
    for c in hdr:
        off = c[3]
        if off:
            dx = c[2] or 0
            patches.append((off, bytes([dx & 0xFF, (dx >> 8) & 0xFF, 0, 0x10,
                                        0, 0, 0, 0])))
            sub_at.add(off)
    ev, buf, spans = m.decode_stream(stores, patches)
    cmds, gifs, tail = [], [], []
    cmd_pos = set()
    stored = set()                      # offsets covered by immediate stores
    for off, w, imm, ad in stores:
        stored.update(range(off, off + w))
    for i, (k, o, v) in enumerate(ev):
        if k == 'payload':
            continue
        if o in sub_at:
            # helper-stamped record tag; the interpreter skips code 0x10
            cmds.append('+%x:SUBHDR w=0x%X' % (o, buf[o] | (buf[o + 1] << 8)))
        else:
            cmds.append('+%x:%s' % (o, v))
        cmd_pos.add(o)
        if 'DIRECT' in v:
            cnt = int(v.rsplit(' ', 1)[1])
            data = bytes(buf.get(p, 0) for p in range(o + 4, o + 4 + cnt * 16))
            gifs += decode_gif(data)
        elif 'UNPACK' in v:
            num = int(v.split('num=')[1].split(' ')[0])
            # trailing items shaped {qword reg-id, qword value} where the
            # reg-id qword was written by immediate stores (not loop fills)
            it = num - 1
            while it >= 0:
                base = o + 4 + it * 16
                if not all(p in stored for p in range(base, base + 8)):
                    break
                q0 = struct.unpack_from('<Q', bytes(buf.get(p, 0) for p in range(base, base + 8)))[0]
                q1 = struct.unpack_from('<Q', bytes(buf.get(p, 0) for p in range(base + 8, base + 16)))[0]
                if q0 not in GSREG:
                    break
                tail.append('%s=0x%X' % (GSREG[q0], q1))
                it -= 1
    tail.reverse()
    # every immediate store lands on a command position, inside a covered
    # payload span, or on an unattributed offset (gap/overrun)
    in_pay = lambda off: any(a <= off < b for a, b in spans)
    payload = sum(1 for off, w, imm, ad in stores
                  if off not in cmd_pos and in_pay(off))
    unattrib = sum(1 for off, w, imm, ad in stores
                   if off not in cmd_pos and not in_pay(off))
    obj_hdr = '0x30' if mpg else ('0x10' if hdr else '')
    if hdr and hdr[0][3] == 0:
        obj_hdr += ' w=0x%X' % (hdr[0][2] or 0)
    return dict(family=fam, builder='%08X' % a, object=obj,
                memset=memset[0][2] if memset else '',
                obj_header=obj_hdr,
                subhdrs=' ; '.join('+%s:w=%X' % (('%x' % c[3]) if c[3] is not None else '?', c[2] or 0) for c in hdr if c[3]),
                mpg_program='%08X' % mpg[0][2] if mpg else '',
                mpg_addr=mpg[0][3] if mpg else '',
                commands=' ; '.join(cmds),
                gif_writes=' ; '.join('%s=%s' % (r, '0x%X' % v if isinstance(v, int) else ('0x%X,0x%X' % v)) for r, v in gifs),
                tail_pairs=' ; '.join(tail),
                unattributed=unattrib, payload=payload)

def main():
    pairs = m.hub_pairs()
    cen = json.load(open(m.CEN))
    mpg_builders = [int(x, 16) for x in cen['builders']]
    mpg_set = set(mpg_builders)
    # 77 hub calls = 68 in-region (the documented startup objects; two are
    # E9 tail-jumps, 0037E0E3/0037E33F) + 9 out-of-region (6 MPG builders,
    # 3 plain). Emit one row per hub call plus any remaining solo MPG rows
    # (none after the E9 fix).
    called = set()
    rows = []
    for i, (a, obj, h) in enumerate(pairs):
        called.add(a)
        fam = 'startup' if 0x480000 <= a < 0x500000 else 'startup-ext'
        calls, stores, _ = m.scan(a)
        rows.append(build_row('%s/%d' % (fam, i), a,
                              '%08X' % obj if obj else '', calls, stores))
    for a in mpg_builders:
        if a in called:
            continue
        calls, stores, _ = m.scan(a)
        rows.append(build_row('mpg-solo', a, '', calls, stores))
    out = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                       'vif1-packet-templates.tsv')
    with open(out, 'w', newline='') as f:
        f.write('\t'.join(['family', 'builder', 'object', 'memset_size',
                           'obj_header', 'sub_headers', 'mpg_program', 'mpg_addr',
                           'command_sequence', 'gif_writes', 'tail_reg_pairs',
                           'unattributed_stores', 'payload_stores']) + '\n')
        for r in rows:
            f.write('\t'.join(str(r[k]) for k in
                    ['family', 'builder', 'object', 'memset', 'obj_header',
                     'subhdrs', 'mpg_program', 'mpg_addr', 'commands',
                     'gif_writes', 'tail_pairs', 'unattributed',
                     'payload']) + '\n')
    print('wrote %d rows -> %s' % (len(rows), out))
    no_mpg = [r['builder'] for r in rows if not r['mpg_program']]
    print('templates with no MPG record:', len(no_mpg), no_mpg[:20])
    bad = [r for r in rows if r['unattributed']]
    print('builders with unattributed stores:', len(bad), [r['builder'] for r in bad])

main()
