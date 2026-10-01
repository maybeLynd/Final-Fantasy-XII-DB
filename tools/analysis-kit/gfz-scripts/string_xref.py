#!/usr/bin/env python3
"""
string_xref.py - map authored strings to the functions that reference them.

An authored diagnostic string is tier-2 evidence, but only once you know *which function*
emits it. This scans .text for RIP-relative LEA instructions targeting a set of string
addresses and attributes each reference to its containing function.

Why not Ghidra: this needs no project and no lock, so it runs alongside headless work.

  string_xref.py <exe> --pattern "[sead]" --functions functions.tsv --out refs.tsv

x64 RIP-relative LEA encodings matched:
    48 8D /r disp32     REX.W       -> rax rcx rdx rbx rsp rbp rsi rdi
    4C 8D /r disp32     REX.WR      -> r8..r15
  with modrm.mod == 00 and modrm.rm == 101 (RIP+disp32)
  target = address_of_next_instruction + disp32
"""
import argparse
import bisect
import io
import re
import struct
import sys


def parse_pe(data):
    pe = struct.unpack_from('<I', data, 0x3C)[0]
    n_sec = struct.unpack_from('<H', data, pe + 6)[0]
    opt_sz = struct.unpack_from('<H', data, pe + 20)[0]
    opt = pe + 24
    if struct.unpack_from('<H', data, opt)[0] != 0x20B:
        raise ValueError('not PE32+')
    base = struct.unpack_from('<Q', data, opt + 24)[0]
    secs = []
    off = opt + opt_sz
    for i in range(n_sec):
        o = off + i * 40
        secs.append({
            'name': data[o:o + 8].rstrip(b'\0').decode('ascii', 'replace'),
            'va': struct.unpack_from('<I', data, o + 12)[0],
            'vsz': struct.unpack_from('<I', data, o + 8)[0],
            'raw': struct.unpack_from('<I', data, o + 20)[0],
            'rsz': struct.unpack_from('<I', data, o + 16)[0],
        })
    return base, secs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('exe')
    ap.add_argument('--pattern', required=True, action='append',
                    help='literal prefix to match, e.g. "[sead]". Repeatable; also accepts '
                         'a comma-separated list. All matches go into one output.')
    ap.add_argument('--functions', help='functions.tsv from DumpFullCoverageGraph')
    ap.add_argument('--out', required=True)
    ap.add_argument('--image-base', type=lambda x: int(x, 16), default=None,
                    help='override image base (default: from PE header)')
    a = ap.parse_args()

    data = io.open(a.exe, 'rb').read()
    pe_base, secs = parse_pe(data)
    base = a.image_base if a.image_base is not None else pe_base

    def off_to_va(off):
        for s in secs:
            if s['raw'] <= off < s['raw'] + s['rsz']:
                return base + s['va'] + (off - s['raw'])
        return None

    # ---- collect target strings -------------------------------------------------
    pats = []
    for chunk in a.pattern:
        pats.extend(x for x in (s.strip() for s in chunk.split(',')) if x)
    strings = {}                      # va -> text
    for pfx in pats:
        rx = re.escape(pfx.encode()) + rb'[ -~]{0,200}'
        for m in re.finditer(rx, data):
            va = off_to_va(m.start())
            if va is None:
                continue
            strings[va] = m.group(0).split(b'\0')[0].decode('ascii', 'replace')
    print('patterns: %d, distinct strings matched: %d' % (len(pats), len(strings)),
          file=sys.stderr)
    if not strings:
        return 1

    # ---- function boundaries ----------------------------------------------------
    entries, names, ends = [], {}, {}
    if a.functions:
        rows = []
        with io.open(a.functions, encoding='utf-8') as f:
            hdr = f.readline().rstrip('\n').split('\t')
            i = {n: k for k, n in enumerate(hdr)}
            for ln in f:
                p = ln.rstrip('\n').split('\t')
                if len(p) < len(hdr):
                    continue
                e = int(p[i['entry']], 16)
                rows.append((e, p[i['name']], int(p[i['body_bytes']] or 0),
                             p[i['owner']]))
        rows.sort()
        for e, nm, sz, ow in rows:
            entries.append(e)
            names[e] = (nm, ow)
            ends[e] = e + sz

    def containing(addr):
        if not entries:
            return None
        k = bisect.bisect_right(entries, addr) - 1
        if k < 0:
            return None
        e = entries[k]
        return e if addr < ends[e] else None

    # ---- scan .text for RIP-relative LEA ---------------------------------------
    text = next((s for s in secs if s['name'] == '.text'), None)
    if text is None:
        raise SystemExit('.text not found')
    blob = data[text['raw']:text['raw'] + text['rsz']]
    text_va = base + text['va']

    hits = []
    n = len(blob)
    for idx in range(n - 7):
        b0 = blob[idx]
        if b0 != 0x48 and b0 != 0x4C:
            continue
        if blob[idx + 1] != 0x8D:
            continue
        modrm = blob[idx + 2]
        if (modrm & 0xC7) != 0x05:          # mod=00, rm=101 -> RIP+disp32
            continue
        disp = struct.unpack_from('<i', blob, idx + 3)[0]
        insn_va = text_va + idx
        target = insn_va + 7 + disp
        if target in strings:
            hits.append((insn_va, target))

    print('LEA references into the string set: %d' % len(hits), file=sys.stderr)

    # ---- attribute and write ----------------------------------------------------
    out_rows = []
    unattributed = 0
    for insn_va, target in hits:
        fe = containing(insn_va)
        if fe is None:
            unattributed += 1
            out_rows.append(('', '', '', '%08X' % insn_va, strings[target]))
        else:
            nm, ow = names[fe]
            out_rows.append(('%08X' % fe, nm, ow, '%08X' % insn_va, strings[target]))
    out_rows.sort()

    with io.open(a.out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('function\tname\towner\tinsn\tstring\n')
        for r in out_rows:
            f.write('\t'.join(r) + '\n')

    funcs = {r[0] for r in out_rows if r[0]}
    print('wrote %s: %d references across %d functions (%d unattributed)'
          % (a.out, len(out_rows), len(funcs), unattributed), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
