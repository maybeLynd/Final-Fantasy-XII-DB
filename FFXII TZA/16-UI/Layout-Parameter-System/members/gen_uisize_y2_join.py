#!/usr/bin/env python3
"""
gen_uisize_y2_join.py — Y-2: why schema (229 trackbars) and data (231 keys)
disagree, and the name mismatches.

Three-way join over the shipped artefacts and the bound set derived from the
image:
  A) jsondata/parametersmanageruisizestruct.csv — 229 'trackbar' names
     (the parameter-manager tool's slider config) + 36 'label' rows;
  B) jsondata/uisize/uisize.json — 231 keys;
  C) the bound set — every `lea rdx, <key>` inside the loader 001CA600
     (VA range 0x1CA600..0x1CC5FA), the name handed to EASTL_LookupByCString /
     Variant_Read*. 227 lea sites over 226 distinct names.

Output TSV: one row per name across the union, with in_schema / in_json /
is_bound flags and a class:
  schema+json+bound   — the working parameters (225)
  schema+json+unbound — trackbar exists, key exists, code never binds (4: NA_*)
  json+bound only     — key bound and in file, no schema row (1)
  json+unbound only   — stale data key, no schema row, no binder (1)

Usage:
  python gen_uisize_y2_join.py <embedded_exe.bin> <uisize.json> <schema.csv> <out.tsv>
"""
import sys, struct, re, csv

def sections(pe):
    e = struct.unpack_from('<I', pe, 0x3C)[0]
    optsz = struct.unpack_from('<H', pe, e + 20)[0]
    opt = e + 24
    ib = struct.unpack_from('<Q', pe, opt + 24)[0]
    out = {}
    for i in range(struct.unpack_from('<H', pe, e + 6)[0]):
        off = opt + optsz + i * 40
        name = pe[off:off + 8].rstrip(b'\0').decode()
        vsz, va, rsz, rva = struct.unpack_from('<IIII', pe, off + 8)
        out[name] = (va + ib, vsz, rva, rsz)
    return out

def bound_keys(pe, secs):
    tva, _, trva, trsz = secs['.text']
    rdva, _, rrva, rrsz = secs['.rdata']
    text = pe[trva:trva + trsz]
    rd = pe[rrva:rrva + rrsz]
    def cstr(va):
        if not (rdva <= va < rdva + rrsz):
            return None
        o = va - rdva
        return rd[o:rd.index(0, o)].decode('utf-8', 'replace')
    sites = []
    for i in range(0x1CA600 - tva, 0x1CC5FA - tva):
        if text[i] == 0x48 and text[i + 1] == 0x8D and text[i + 2] == 0x15:
            d = struct.unpack_from('<i', text, i + 3)[0]
            s = cstr(tva + i + 7 + d)
            if s is not None:
                sites.append((tva + i, s))
    return sites

def main():
    pe = open(sys.argv[1], 'rb').read()
    secs = sections(pe)
    sites = bound_keys(pe, secs)
    bound = set(s for _, s in sites)

    raw = open(sys.argv[2], 'rb').read().decode('utf-8')
    jkeys = set(re.findall(r'"([^"]+)"\s*:', raw))

    rows = list(csv.reader(open(sys.argv[3], encoding='utf-8-sig')))
    tb = set(r[0] for r in rows[1:] if len(r) > 1 and r[1] == 'trackbar')
    lb = set(r[0] for r in rows[1:] if len(r) > 1 and r[1] == 'label')

    universe = sorted(tb | jkeys | bound)
    out = []
    for n in universe:
        ins, inj, inb = n in tb, n in jkeys, n in bound
        if ins and inj and inb:
            cls = 'schema+json+bound'
        elif ins and inj:
            cls = 'schema+json+unbound'
        elif inj and inb:
            cls = 'json+bound_noschema'
        elif inj:
            cls = 'json+unbound_noschema'
        elif ins:
            cls = 'schema_only'
        else:
            cls = 'bound_only'
        out.append((n, int(ins), int(inj), int(inb), cls))

    w = open(sys.argv[4], 'w', encoding='utf-8', newline='')
    w.write('# Y-2 three-way join: schema trackbars x uisize.json keys x bound set (lea rdx in 001CA600)\n')
    w.write(f'# schema_trackbars={len(tb)} labels={len(lb)} json_keys={len(jkeys)} '
            f'lea_sites={len(sites)} bound={len(bound)}\n')
    w.write('name\tin_schema\tin_json\tis_bound\tclass\n')
    for r in out:
        w.write('\t'.join(map(str, r)) + '\n')
    w.close()
    from collections import Counter
    print('sites', len(sites), 'bound', len(bound), 'json', len(jkeys), 'schema', len(tb))
    print(dict(Counter(r[4] for r in out)))

if __name__ == '__main__':
    main()
