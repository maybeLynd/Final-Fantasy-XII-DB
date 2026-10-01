#!/usr/bin/env python3
"""
gen_bin_assembly_census.py — UQ-380 composed-name route, static half.

FABLE's measurement (2026-09-16) proved: no single image string carries both a
'%' conversion and '.bin', so a one-shot sprintf cannot produce a .bin name; but
~95 strings have the shape of two-part path assembly ("%s%s", "./GameData/%s/...
%s_%s.ah"), and a name built as %s%s from a stem plus a ".bin" piece leaves no
literal trace. The remaining static step: enumerate the assembly-format call
sites and ask whether a .bin-bearing piece can reach a %s argument.

Method (all evidence is NATIVE/STATIC over the authorized image):
  1. Extract NUL-terminated strings from .rdata. Two sets:
       A) every string containing '.bin' (case-insensitive) — full filenames and
          any bare '.bin' piece;
       B) every string with >=2 '%' conversions, at least one %s — the
          "two-part assembly" population (rebuilt independently, count compared
          to FABLE's 95).
  2. Scan .text for `lea r64, [rip+disp32]` (REX.W 8D /r, mod=00 rm=101) — every
     literal-string materialization site.
  3. For each set-B string's lea site: locate the enclosing function (FAS2
     entries), the next forward CALL target, and the set of all other rip-lea
     targets inside a bounded window ending at that call — the candidate literal
     variadic args.
  4. Classify each site: any candidate arg containing '.bin' → CAN_COMPOSE_BIN;
     all-args-literal, none .bin → LITERAL_NO_BIN; at least one arg not literal
     → DYNAMIC_ARG (a caller could pass a .bin-ending string; unbounded).

Also emitted: every .bin string's referrer functions (where .bin pieces are
materialized at all) — the supply side of the composition.

Usage:
  python gen_bin_assembly_census.py <embedded_exe.bin> <snapshot.fas2> <out.tsv>
"""
import sys, struct, bisect, re
from io import BytesIO

PRINTABLE = set(range(0x20, 0x7F)) | {0x09}

def read_sections(pe):
    e = struct.unpack_from('<I', pe, 0x3C)[0]
    nsec = struct.unpack_from('<H', pe, e + 6)[0]
    optsz = struct.unpack_from('<H', pe, e + 20)[0]
    opt = e + 24
    imagebase = struct.unpack_from('<Q', pe, opt + 24)[0]
    secs = {}
    for i in range(nsec):
        off = opt + optsz + i * 40
        name = pe[off:off + 8].rstrip(b'\0').decode()
        vsz, va, rsz, rva = struct.unpack_from('<IIII', pe, off + 8)
        secs[name] = (va + imagebase, vsz, rva, rsz)
    return imagebase, secs

def slice_sec(pe, sec):
    va, vsz, rva, rsz = sec
    return pe[rva:rva + rsz], va

def extract_strings(data, base_va, minlen=4):
    out = []
    i, n = 0, len(data)
    while i < n:
        if data[i] in PRINTABLE:
            j = i
            while j < n and data[j] in PRINTABLE:
                j += 1
            if j - i >= minlen and j < n and data[j] == 0:
                out.append((base_va + i, data[i:j].decode('ascii', 'replace')))
            i = j + 1
        else:
            i += 1
    return out

def fmt_conversion_count(s):
    # count real conversions, skipping %%
    cnt = 0
    has_s = False
    for m in re.finditer(r'%+', s):
        run = m.group(0)
        pos = m.end()
        # pairs of %% are literals
        for k in range(0, len(run) - 1, 2):
            pass
        if len(run) % 2 == 1 and pos < len(s):
            spec = s[pos]
            if spec != '%':
                cnt += 1
                if spec == 's':
                    has_s = True
    return cnt, has_s

def lea_scan(text, text_va):
    """yield (site_va, reg, target_va) for `lea r64,[rip+disp]`"""
    i, n = 0, len(text)
    while i < n - 7:
        # REX.W (0x48-0x4F with W bit = 0x48|rex) + 8D + modrm(mod00 rm101)
        if text[i] == 0x48 and text[i + 1] == 0x8D and (text[i + 2] & 0xC7) == 0x05:
            reg = (text[i + 2] >> 3) & 7
            disp = struct.unpack_from('<i', text, i + 3)[0]
            tgt = text_va + i + 7 + disp
            yield text_va + i, reg, tgt
            i += 7
        else:
            i += 1

def call_scan(text, text_va, lo, hi):
    """first E8 call in [lo,hi): return (site_va, callee_va)"""
    i = lo
    while i < hi - 5:
        if text[i] == 0xE8:
            disp = struct.unpack_from('<i', text, i + 1)[0]
            return text_va + i, text_va + i + 5 + disp
        i += 1
    return None, None

def ripload_scan(text, text_va):
    """every `lea/mov r64, [rip+disp32]` (REX.W + 8D/8B, modrm rip form) —
    the established instrument from thunk_address_taken.py, widened to all
    REX.W prefixes so high-register loads are counted."""
    i, n = 0, len(text)
    while i < n - 7:
        if 0x48 <= text[i] <= 0x4F and text[i] & 8 and \
           text[i + 1] in (0x8D, 0x8B) and (text[i + 2] & 0xC7) == 0x05:
            disp = struct.unpack_from('<i', text, i + 3)[0]
            yield text_va + i, text_va + i + 7 + disp
            i += 7
        else:
            i += 1

# --- FAS2 parse (same layout as fas2_export.py, entry+name only needed) ---
def _i32(f): return struct.unpack('>i', f.read(4))[0]
def _i64(f): return struct.unpack('>q', f.read(8))[0]
def _bool(f): return struct.unpack('>?', f.read(1))[0]
def _s(f):
    n = _i32(f)
    return None if n < 0 else f.read(n).decode('utf-8')

def load_functions(path):
    f = open(path, 'rb')
    assert f.read(8) == b'GFZANN2\0'
    ver = _i32(f); count = _i32(f)
    entries = []
    for _ in range(count):
        rlen = _i32(f)
        rec = BytesIO(f.read(rlen))
        entry = _i64(rec); name = _s(rec); ns = _s(rec)
        _s(rec); _s(rec); _s(rec); _s(rec); _s(rec); _s(rec)
        _bool(rec); _bool(rec); _bool(rec); _bool(rec); _i64(rec)
        nr = _i32(rec)
        for _ in range(nr): _i64(rec); _i64(rec)
        nt = _i32(rec)
        for _ in range(nt): _s(rec); _s(rec)
        entries.append((entry, name or '', ns or ''))
    entries.sort()
    return entries

def main():
    exe_path, fas2_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    pe = open(exe_path, 'rb').read()
    imagebase, secs = read_sections(pe)
    rdata, rdata_va = slice_sec(pe, secs['.rdata'])
    text, text_va = slice_sec(pe, secs['.text'])
    funcs = load_functions(fas2_path)
    fentries = [e for e, _, _ in funcs]
    fmap = {e: (n, ns) for e, n, ns in funcs}
    def enclosing(site):
        k = bisect.bisect_right(fentries, site) - 1
        return fentries[k] if k >= 0 else 0

    strs = extract_strings(rdata, rdata_va)
    by_va = {va: s for va, s in strs}
    bins = [(va, s) for va, s in strs if '.bin' in s.lower()]
    fmts = [(va, s) for va, s in strs
            if fmt_conversion_count(s)[0] >= 2 and fmt_conversion_count(s)[1]]

    # every rip-lea in .text
    leas = list(lea_scan(text, text_va))
    tgt2sites = {}
    for site, reg, tgt in leas:
        tgt2sites.setdefault(tgt, []).append((site, reg))

    # census A supply side: for each .bin string —
    #   (a) direct lea materialization sites;
    #   (b) data-section qword slots holding its VA (pointer tables);
    #   (c) .text rip-loads (lea/mov) of those slots — the only way a .bin
    #       pointer can reach a register without a direct lea.
    bin_vas = set(va for va, _ in bins)
    # index all data qwords -> VA for the .bin set (rdata + data)
    qword_slots = {}
    for sname in ('.rdata', '.data', '_RDATA'):
        if sname not in secs:
            continue
        d, dva = slice_sec(pe, secs[sname])
        for off in range(0, len(d) - 8, 8):
            v = struct.unpack_from('<Q', d, off)[0]
            if v in bin_vas:
                qword_slots.setdefault(v, []).append(dva + off)
    # .text rip-loads of slot addresses
    slot_vas = set()
    for slots in qword_slots.values():
        slot_vas.update(slots)
    slot_loads = {}  # slot_va -> [site]
    for site, tgt in ripload_scan(text, text_va):
        if tgt in slot_vas:
            slot_loads.setdefault(tgt, []).append(site)

    bin_rows = []
    for va, s in bins:
        direct = sorted(tgt2sites.get(va, []))
        slots = qword_slots.get(va, [])
        slotrefs = [(sl, site) for sl in slots for site in slot_loads.get(sl, [])]
        fe = enclosing(direct[0][0]) if direct else (enclosing(slotrefs[0][1]) if slotrefs else 0)
        n, ns = fmap.get(fe, ('?', '?'))
        bin_rows.append((va, s, len(direct),
                         ','.join(f'{x[0]:08X}' for x in direct),
                         len(slots), len(slotrefs),
                         ','.join(f'{x[1]:08X}' for x in slotrefs),
                         fe, n, ns))

    # census B: format sites. A %s arg carries a .bin piece iff, in the window
    # before the call, code either (a) leas a .bin string directly, or
    # (b) rip-loads a data slot whose qword holds a .bin string VA.
    bin_slot_contents = {}  # slot_va -> .bin string VA
    for v, slots in qword_slots.items():
        for sl in slots:
            bin_slot_contents[sl] = v
    all_loads = sorted(ripload_scan(text, text_va))
    load_sites = [s for s, _ in all_loads]

    fmt_rows = []
    for va, s in fmts:
        for site, reg in sorted(tgt2sites.get(va, [])):
            fe = enclosing(site)
            n, ns = fmap.get(fe, ('?', '?'))
            # forward call within 96 bytes of the lea
            csite, callee = call_scan(text, text_va, site - text_va + 7,
                                      site - text_va + 103)
            args = set()
            if csite:
                lo = csite - 80
                k0 = bisect.bisect_left(load_sites, lo)
                k1 = bisect.bisect_left(load_sites, csite)
                for s2, t2 in all_loads[k0:k1]:
                    if t2 in by_va:
                        args.add(by_va[t2])
                    elif t2 in bin_slot_contents:
                        args.add('*(slot)->' + by_va[bin_slot_contents[t2]])
            has_bin = any('.bin' in a.lower() for a in args)
            # is every %s arg a literal? heuristic: count leas vs conversion count
            nconv, _ = fmt_conversion_count(s)
            verdict = ('CAN_COMPOSE_BIN' if has_bin else
                       ('LITERAL_NO_BIN' if len(args) >= nconv - 1 and args
                        else 'DYNAMIC_ARG' if not args else 'LITERAL_NO_BIN'))
            fmt_rows.append((va, s, site, fe, n, ns, csite, callee,
                             has_bin, verdict,
                             '|'.join(sorted(args))[:300]))

    with open(out_path, 'w', encoding='utf-8', newline='') as w:
        w.write('# UQ-380 composed-name census\n')
        w.write(f'# exe={exe_path}\n# rdata strings={len(strs)} '
                f'bin_strings={len(bins)} assembly_fmts={len(fmts)} '
                f'(FABLE measured ~95)\n')
        w.write('[FMT-SITES]\tfmt_va\tfmt_text\tsite_va\tfunc_va\tfunc_name\t'
                'call_va\tcallee_va\thas_bin_arg\tverdict\tliteral_args\n')
        for r in fmt_rows:
            w.write('\t'.join(str(x) for x in r) + '\n')
        w.write('[BIN-STRINGS]\tstr_va\tstr_text\tdirect_lea_count\tdirect_lea_sites\t'
                'ptr_slots\tptr_slot_loads\tptr_slot_load_sites\tfunc_va\tfunc_name\tfunc_ns\n')
        for r in bin_rows:
            w.write('\t'.join(str(x) for x in r) + '\n')
    print(f'bin_strings={len(bins)} assembly_fmts={len(fmts)} '
          f'fmt_sites={len(fmt_rows)} '
          f'bin_direct_leas={sum(r[2] for r in bin_rows)} '
          f'bin_ptr_slots={sum(r[4] for r in bin_rows)} '
          f'bin_slot_loads={sum(r[5] for r in bin_rows)} '
          f'can_compose={sum(1 for r in fmt_rows if r[8])}')

if __name__ == '__main__':
    main()
