#!/usr/bin/env python3
"""
fas2_export.py - read a GFZ FAS2 annotation snapshot into queryable form.

The FAS2 file produced by GFZFunctionAnnotationSnapshotV2.java is the complete
annotation state of all 38,161 functions. This is the source of truth the
FFXII TZA documentation database is built from.

Usage:
  fas2_export.py <snapshot.fas2> --tsv out.tsv          flat table (one row/function)
  fas2_export.py <snapshot.fas2> --jsonl out.jsonl      full records incl. comments
  fas2_export.py <snapshot.fas2> --domains out.tsv      CodeDomain histogram
  fas2_export.py <snapshot.fas2> --owners  out.tsv      PrimaryOwner histogram
  fas2_export.py <snapshot.fas2> --unresolved out.txt   entries with no classification

Record layout (mirrors diff_fas2.py):
  entry, name, namespace, name_source, comment, repeatable_comment, prototype,
  signature_source, calling_convention, inline, noreturn, varargs, is_thunk,
  thunk_target, body_ranges[], tags[(name, comment)]
"""
import sys
import struct
import json
import argparse
import collections
from io import BytesIO

OWNER_PREFIX = "GFZ.V120.PrimaryOwner."
DOMAIN_PREFIX = "GFZ.V121.CodeDomain."
FINAL_NO = "GFZ.V120.FinalNoPrimaryOwner"


def _i32(f):
    return struct.unpack('>i', f.read(4))[0]


def _i64(f):
    return struct.unpack('>q', f.read(8))[0]


def _bool(f):
    return struct.unpack('>?', f.read(1))[0]


def _s(f):
    n = _i32(f)
    if n < 0:
        return None
    return f.read(n).decode('utf-8')


def parse_rec(data):
    f = BytesIO(data)
    d = {}
    d['entry'] = _i64(f)
    d['name'] = _s(f)
    d['namespace'] = _s(f)
    d['name_source'] = _s(f)
    d['comment'] = _s(f)
    d['repeatable_comment'] = _s(f)
    d['prototype'] = _s(f)
    d['signature_source'] = _s(f)
    d['calling_convention'] = _s(f)
    d['inline'] = _bool(f)
    d['noreturn'] = _bool(f)
    d['varargs'] = _bool(f)
    d['is_thunk'] = _bool(f)
    d['thunk_target'] = _i64(f)
    nr = _i32(f)
    d['body_ranges'] = [(_i64(f), _i64(f)) for _ in range(nr)]
    nt = _i32(f)
    d['tags'] = [(_s(f), _s(f)) for _ in range(nt)]
    if f.read():
        raise ValueError('record trailing bytes')
    return d


def parse(path):
    out = []
    with open(path, 'rb') as f:
        if f.read(8) != b'GFZANN2\0':
            raise ValueError('bad magic - not a FAS2 snapshot')
        ver = _i32(f)
        n = _i32(f)
        for _ in range(n):
            ln = _i32(f)
            out.append(parse_rec(f.read(ln)))
        if f.read():
            raise ValueError('file trailing bytes')
    return ver, out


def classify(rec):
    """Return (owner, final_no, domains) exactly as ReportV121Coverage does."""
    owner = None
    final_no = False
    domains = []
    for name, _comment in rec['tags']:
        if name is None:
            continue
        if name.startswith(OWNER_PREFIX):
            owner = name[len(OWNER_PREFIX):]
        elif name == FINAL_NO:
            final_no = True
        elif name.startswith(DOMAIN_PREFIX):
            domains.append(name[len(DOMAIN_PREFIX):])
    return owner, final_no, sorted(domains)


def body_size(rec):
    return sum(hi - lo + 1 for lo, hi in rec['body_ranges'])


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('snapshot')
    ap.add_argument('--tsv')
    ap.add_argument('--jsonl')
    ap.add_argument('--domains')
    ap.add_argument('--owners')
    ap.add_argument('--unresolved')
    a = ap.parse_args()

    ver, recs = parse(a.snapshot)
    print("FAS2 v%d: %d functions" % (ver, len(recs)), file=sys.stderr)

    dom_hist = collections.Counter()
    own_hist = collections.Counter()
    unresolved = []
    overlap = 0
    rows = []

    for r in recs:
        owner, final_no, domains = classify(r)
        layers = (1 if owner else 0) + (1 if final_no else 0) + (1 if domains else 0)
        if layers > 1:
            overlap += 1
        if layers == 0:
            unresolved.append(r['entry'])
        if owner:
            own_hist[owner] += 1
        for d in domains:
            dom_hist[d] += 1
        rows.append((r, owner, final_no, domains))

    print("  owner=%d domains=%d unresolved=%d overlap=%d"
          % (sum(own_hist.values()), sum(dom_hist.values()),
             len(unresolved), overlap), file=sys.stderr)

    if a.tsv:
        with open(a.tsv, 'w', encoding='utf-8', newline='') as f:
            f.write("entry\tname\tnamespace\tname_source\tbody_bytes\tis_thunk\t"
                    "owner\tfinal_no_owner\tcode_domains\tprototype\n")
            for r, owner, final_no, domains in rows:
                f.write("\t".join([
                    "%08X" % r['entry'],
                    r['name'] or '',
                    r['namespace'] or '',
                    r['name_source'] or '',
                    str(body_size(r)),
                    str(r['is_thunk']).lower(),
                    owner or '',
                    str(final_no).lower(),
                    ";".join(domains),
                    (r['prototype'] or '').replace('\t', ' '),
                ]) + "\n")
        print("wrote %s" % a.tsv, file=sys.stderr)

    if a.jsonl:
        with open(a.jsonl, 'w', encoding='utf-8') as f:
            for r, owner, final_no, domains in rows:
                thunk = None
                if r['thunk_target'] >= 0:
                    thunk = "%08X" % r['thunk_target']
                f.write(json.dumps({
                    'entry': "%08X" % r['entry'],
                    'name': r['name'],
                    'namespace': r['namespace'],
                    'name_source': r['name_source'],
                    'body_bytes': body_size(r),
                    'body_ranges': [["%08X" % lo, "%08X" % hi]
                                    for lo, hi in r['body_ranges']],
                    'is_thunk': r['is_thunk'],
                    'thunk_target': thunk,
                    'prototype': r['prototype'],
                    'calling_convention': r['calling_convention'],
                    'noreturn': r['noreturn'],
                    'owner': owner,
                    'final_no_owner': final_no,
                    'code_domains': domains,
                    'comment': r['comment'],
                }, ensure_ascii=False) + "\n")
        print("wrote %s" % a.jsonl, file=sys.stderr)

    if a.domains:
        with open(a.domains, 'w', encoding='utf-8') as f:
            f.write("count\tcode_domain\n")
            for k, v in sorted(dom_hist.items(), key=lambda x: (-x[1], x[0])):
                f.write("%d\t%s\n" % (v, k))
        print("wrote %s (%d distinct)" % (a.domains, len(dom_hist)), file=sys.stderr)

    if a.owners:
        with open(a.owners, 'w', encoding='utf-8') as f:
            f.write("count\tprimary_owner\n")
            for k, v in sorted(own_hist.items(), key=lambda x: (-x[1], x[0])):
                f.write("%d\t%s\n" % (v, k))
        print("wrote %s (%d distinct)" % (a.owners, len(own_hist)), file=sys.stderr)

    if a.unresolved:
        with open(a.unresolved, 'w', encoding='utf-8', newline='\n') as f:
            for e in sorted(unresolved):
                f.write("%08X\n" % e)
        print("wrote %s (%d entries)" % (a.unresolved, len(unresolved)), file=sys.stderr)


if __name__ == '__main__':
    main()
