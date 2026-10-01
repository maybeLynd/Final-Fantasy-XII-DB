#!/usr/bin/env python3
"""contract_named_state_census.py - which contract-named state has no declared type? (OPUS, 2026-09-25)

SWE2-AUDIT-SEM's accepted `types: MET` criterion (L2-VERDICTS.md, 2026-09-21): the cell is MET when
EVERY piece of state the system's contract names has a declared type with a measured extent, at the
granularity the contract names it; the denominator is the contract's state enumeration - its Types
and State sections and any interface-table state column - and NOT addresses cited in invariant prose.
`types` blocks 46 of the 51 NOT-MET verdict rows (FABLE's per-cell census). S-35 was blocked by
exactly one undeclared named object (block 195). This finds the rest mechanically, as a WORKLIST:
it scores nothing - scoring is SWE2-AUDIT-SEM's.

For every CONTRACT-*.md, every backticked 8-hex address inside a section whose heading names Types or
State (or the Interface section's table rows that say "state"), in .data/.bss (01DF0000 .. image end),
is resolved against the type store's static routes (check_static_spans.spans_from: STATIC, ARRAY,
SLOTPTR, PTR/PARRAY cells), then against the covering type's field rows:

  FIELD      inside a declared, named field of a declared type        - satisfies the criterion
  GAP-SPAN   inside a declared type but on an unobservedSpan/gap row  - extent only (precision 1)
  PTR-CELL   the address is a declared pointer cell                   - the cell is declared
  UNDECLARED no static route in the store covers it                   - the criterion's gap

.rdata addresses (008C2000 .. 01DF0000) are reported separately as CONSTANT - named tables are data,
not mutable state, and whether the criterion wants them declared is the scorer's call.

    contract_named_state_census.py [--out rows.tsv]
"""
import argparse
import bisect
import collections
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_absence_claims as G  # noqa: E402
import check_static_spans as SS  # noqa: E402

DATA_LO, DATA_HI = 0x01DF0000, 0x03095400
RDATA_LO = 0x008C2000
ADDR = re.compile(r"`\[?(?:0x)?(0[0-9A-Fa-f]{7})\]?(?:\+0x[0-9A-Fa-f]+)?`")   # `ADDR`, `0xADDR`, `[ADDR]` cells
# The optional 0x was added 2026-09-25 (OPUS): CONTRACT-sound-request writes its whole state table as `0x02091098`,
# and the census returned no rows for it at all - a blind spot, not an empty contract.
HEAD = re.compile(r"^(#{2,4})\s+(.*)$")
STATE_HEAD = re.compile(r"^(?!.*transition).*\b(types?|state|objects?)\b", re.I)   # not "State transitions";
# "The objects" / "The shared object" are the state enumeration of contracts written without a Types/State
# heading (10 of 107 at 2026-09-25, e.g. CONTRACT-input-subsystem section 2, FABLE's post-processing and Steam
# contracts section 2).


def load_store():
    tdir = os.path.join(G.DB, "_types")
    types = list(csv.DictReader(io.open(os.path.join(tdir, "types.tsv"), encoding="utf-8"),
                                delimiter="\t", quoting=csv.QUOTE_NONE))
    fields = collections.defaultdict(list)
    for r in csv.DictReader(io.open(os.path.join(tdir, "fields.tsv"), encoding="utf-8"),
                            delimiter="\t", quoting=csv.QUOTE_NONE):
        try:
            fields[r["type"]].append((int(r["offset"], 16), int(r["size"]), r["name"], r["readiness"],
                                      r["ctype"]))
        except (ValueError, TypeError):
            pass
    sizes = {}
    spans = []                                   # (lo, hi, type, kind, stride)
    for t in types:
        try:
            size = int(t["size"], 16)
        except (ValueError, TypeError):
            size = None
        sizes[t["type"]] = size
        for kind, lo, hi, text in SS.spans_from(t["type"], t.get("route") or "", size):
            m = re.search(r"stride=(0x[0-9A-Fa-f]+|\d+)", text)
            spans.append((lo, hi, t["type"], kind, int(m.group(1), 0) if m else None))
    return spans, fields, sizes


def field_at(tname, off, fields, sizes, depth=0):
    """(class, where) for byte `off` of type `tname`, descending into declared element types."""
    for fo, fs, nm, rd, ct in fields.get(tname, ()):
        if fo <= off < fo + max(fs, 1):
            gap = nm.lower().startswith(("unobserved", "gap", "unresolved")) or "Span" in nm
            if gap:
                return "GAP-SPAN", "+0x%X %s (%s)" % (off, nm, rd)
            base = re.sub(r"\[.*\]$", "", ct).strip()
            if depth < 4 and base in fields and sizes.get(base):
                cls, where = field_at(base, (off - fo) % sizes[base], fields, sizes, depth + 1)
                return cls, "+0x%X %s -> %s" % (off, nm, where)
            return "FIELD", "+0x%X %s (%s)" % (off, nm, rd)
    return "GAP-SPAN", "+0x%X (no field row)" % off


def resolve(v, spans, fields, sizes):
    hits = [sp for sp in spans if sp[0] <= v < sp[1]]
    if not hits:
        return "UNDECLARED", "", ""
    data = [h for h in hits if h[3] != "pointer cell"]
    if not data:
        return "PTR-CELL", hits[0][2], "+0x%X" % (v - hits[0][0])
    lo, hi, tname, kind, stride = data[0]
    off = (v - lo) % stride if stride else v - lo
    cls, where = field_at(tname, off, fields, sizes)
    return cls, tname, where


FENCE_ADDR = re.compile(r"(?<![0-9A-Za-z_])(?:0x)?(0[0-9A-Fa-f]{7})(?![0-9A-Za-z_])")
# Inside a ``` fence nothing is backticked, so the fence gets a bare-address pattern (OPUS, 2026-09-25, block 215):
# CONTRACT-field-music-selection declares its table as `struct MusicTable { /* pointed to by *(void**)0x02B5E0D0 */`
# and the census never saw it. .text addresses in asm listings fall below DATA_LO/RDATA_LO and are dropped there.


def state_sections(text):
    """Yield (heading, line, fenced) for lines inside Types/State sections, plus 'state' rows of Interface."""
    cur = None
    fenced = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        m = None if fenced else HEAD.match(line)
        if m:
            cur = m.group(2) if (len(m.group(1)) == 2 and STATE_HEAD.search(m.group(2))) else (
                cur if len(m.group(1)) > 2 and cur else None)
            if len(m.group(1)) == 2 and re.search(r"interface", m.group(2), re.I):
                cur = "INTERFACE"
            continue
        if cur == "INTERFACE":
            if line.startswith("|") and re.search(r"\bstate\b|\bglobal", line, re.I):
                yield "Interface (state row)", line, False
        elif cur:
            yield cur, line, fenced


RANGE = re.compile(r"`?(?:0x)?(0[0-9A-Fa-f]{7})`?\s*(?:\.\.|–|—|…)\s*`?(?:0x)?(0[0-9A-Fa-f]{7})`?")
# RANGE BOUNDS (OPUS, 2026-09-25, block 219), from SWE2-AUDIT-SEM's review of this tool: a range written
# `A`..`B` / `A`–`B` names the REGION, not state at its endpoints. An undeclared END is RANGE-END (a bound,
# exclusive by convention). An undeclared START is RANGE-START only when the declared store already covers at
# least 90% of [A, B) - otherwise it stays UNDECLARED, because the region itself may be the undeclared state.


def covered_fraction(lo, hi, spans):
    iv = sorted((max(s[0], lo), min(s[1], hi)) for s in spans if s[3] != "pointer cell" and s[0] < hi and s[1] > lo)
    tot, cur = 0, lo
    for a, b in iv:
        a = max(a, cur)
        if b > a:
            tot += b - a
            cur = b
    return tot / float(hi - lo) if hi > lo else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    spans, fields, sizes = load_store()
    rows = []
    for root, _d, files in os.walk(G.DB):
        rel = os.path.relpath(root, G.DB)
        if rel.split(os.sep)[0] in ("_index", "_experiments", "_types"):
            continue
        for fn in sorted(files):
            if not (fn.startswith("CONTRACT-") and fn.endswith(".md")):
                continue
            p = os.path.join(root, fn)
            seen = set()
            for sec, line, fenced in state_sections(io.open(p, encoding="utf-8", errors="replace").read()):
                ends, starts = set(), {}
                for rm in RANGE.finditer(line):
                    lo, hi = int(rm.group(1), 16), int(rm.group(2), 16)
                    if lo < hi:
                        ends.add(hi)
                        starts[lo] = hi
                for m in (FENCE_ADDR if fenced else ADDR).finditer(line):
                    v = int(m.group(1), 16)
                    if v in seen:
                        continue
                    if DATA_LO <= v < DATA_HI:
                        seen.add(v)
                        cls, tname, where = resolve(v, spans, fields, sizes)
                        if cls == "UNDECLARED" and v in ends:
                            cls, where = "RANGE-END", "end bound of a range named on this line"
                        elif cls == "GAP-SPAN" and v in ends:
                            # an INCLUSIVE end bound (`A` … `B` with B the region's last byte) lands inside the
                            # declared object, often on its tail gap row; it is still a bound, not named state
                            # (OPUS, 2026-09-25, block 254; e.g. the loot-node array 02EC0FA0 … 02EC135F).
                            cls, where = "RANGE-END", "inclusive end bound of a range named on this line (%s)" % where
                        elif cls == "UNDECLARED" and v in starts:
                            f = covered_fraction(v, starts[v], spans)
                            if f >= 0.9:
                                cls, where = "RANGE-START", "start of %08X..%08X, %.1f%% declared" % (v, starts[v], 100 * f)
                    elif RDATA_LO <= v < DATA_LO:
                        seen.add(v)
                        cls, tname, where = "CONSTANT", "", ""
                    else:
                        continue
                    rows.append((os.path.relpath(p, G.DB).replace(os.sep, "/"), sec[:40], "%08X" % v,
                                 cls, tname, where))
    per = collections.defaultdict(collections.Counter)
    for r in rows:
        per[r[0]][r[3]] += 1
    tot = collections.Counter(r[3] for r in rows)
    print("contracts with named state: %d   addresses: %d   %s" % (len(per), len(rows), dict(tot)))
    print("contracts with UNDECLARED named state, most first:")
    for c, cnt in sorted(per.items(), key=lambda kv: -kv[1]["UNDECLARED"]):
        if cnt["UNDECLARED"]:
            print("  %3d undeclared  %3d field  %3d gap  %s" % (cnt["UNDECLARED"], cnt["FIELD"],
                                                                 cnt["GAP-SPAN"], c))
    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("contract\tsection\taddress\tclass\ttype\twhere\n")
            for r in rows:
                f.write("\t".join(r) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
