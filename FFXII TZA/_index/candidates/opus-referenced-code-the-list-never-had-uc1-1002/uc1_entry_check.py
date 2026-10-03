"""uc1_entry_check.py - test 1 of FABLE's UC-1 route ruling, re-derived at the bytes for every row of this record
(OPUS, 2026-10-03; repairs SWE2-AUDIT-SPEC's REJECT in auditspec-review-opus-referenced-code-the-list-never-had-uc1-1002).

The first census (uc1_credible.py) took direct references from retool's call index only, which holds `call`/`jmp` rel32.
It missed `0F 8x` conditional jumps and 32-bit image-relative fields, so 15 rows said "no direct reference was found"
for bodies that are referenced. This census is image-wide:
  - every decoded `call` / `jmp` / `jcc` (rel8 and rel32) in every listed function body whose target is the row's body;
  - aligned qwords equal to the start (tables), in any section;
  - 32-bit image-relative values equal to start - image base in .rdata / .data, but not in .pdata, where a function
    start is the unwind entry or the previous function's EndAddress, not a way in.
Each row's entry statement must agree. A row that says "no direct reference was found" must have no evidence. A row
that names a site ("entered from X + 0xNN", "by a jump", "by a conditional jump", "through the qword table entry",
"image-relative") must have that site among the evidence. Last line 'FAILS n'.
"""
import collections
import io
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool  # noqa: E402
import check_dispositions as CD  # noqa: E402
import pefile  # noqa: E402

R = retool.R
cfg = json.load(io.open(os.path.join(HERE, "rows.json"), encoding="utf-8"))
rows = cfg["rows"]
want = {int(r["fn"], 16) for r in rows}
sizes = CD.load_functions()

ev = collections.defaultdict(set)          # body -> {("jump", fn, site, mnemonic) | ("table", va) | ("imgrel", va)}
for f, n in sizes.items():
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        if i.mnemonic.startswith("j") or i.mnemonic == "call":
            if re.fullmatch(r"0x[0-9a-f]+", i.op_str):
                t = int(i.op_str, 16)
                if t in want and not (f <= t < f + n and t != f):
                    if f != t:
                        ev[t].add(("jump", f, i.address, i.mnemonic))
pe = pefile.PE(R.b.EXE, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
rvas = {t - base: t for t in want}
for sec in pe.sections:
    name = sec.Name.rstrip(b"\0").decode("ascii", "replace")
    data = sec.get_data()
    va0 = base + sec.VirtualAddress
    for o in range(0, len(data) - 7, 8):
        q = struct.unpack_from("<Q", data, o)[0]
        if q in want:
            ev[q].add(("table", va0 + o))
    if name in (".rdata", ".data"):
        for o in range(0, len(data) - 3, 4):
            v = struct.unpack_from("<I", data, o)[0]
            if v in rvas:
                # an RVA's bytes that are part of a printable run are string data, not a field (00125753's
                # 'SW' inside the REQSW / FREQSW mnemonic table) - SWE2-AUDIT-SPEC's census excluded them too
                w = data[max(0, o - 2):o + 6]
                if sum(32 <= c < 127 for c in w) >= 5:
                    continue
                ev[rvas[v]].add(("imgrel", va0 + o))

fails = 0
summary = collections.Counter()
for r in rows:
    f = int(r["fn"], 16)
    t = r["text"]
    e = ev.get(f, set())
    claims_none = t.startswith("no direct reference was found")
    if claims_none:
        if e:
            fails += 1
            print("FAIL %s: says no direct reference, but %s" % (r["fn"], sorted(
                ("%s %08X@%08X %s" % (k[0], k[1], k[2], k[3]) if k[0] == "jump" else "%s %08X" % k) for k in e)[:3]))
        else:
            summary["none, confirmed"] += 1
        continue
    named = set(re.findall(r"\b([0-9A-F]{8})\b", t.split(";")[0]))
    # a site past the caller's recorded extent (0037C3F0 + 0x150 / + 0x1F8) is decoded where the row names it
    for m in re.finditer(r"([0-9A-F]{8})`? \+ 0x([0-9A-F]+)", t.split(";")[0]):
        site = int(m.group(1), 16) + int(m.group(2), 16)
        i = next(R.md.disasm(R.at(site, 16), site), None)
        if i is not None and (i.mnemonic == "call" or i.mnemonic.startswith("j")) and i.op_str == hex(f):
            e = set(e) | {("jump", int(m.group(1), 16), site, i.mnemonic)}
    hit = False
    for k in e:
        if k[0] == "jump":
            off = "+ 0x%X" % (k[2] - k[1])
            if "%08X" % k[1] in named and (off in t.split(";")[0] or "+ 0x0" in t.split(";")[0]):
                hit = True
        elif "%08X" % k[1] in named:
            hit = True
    if hit:
        summary["site named, confirmed"] += 1
    else:
        fails += 1
        print("FAIL %s: entry statement names no site the census finds (%s)" % (r["fn"], t.split(";")[0][:120]))
print("rows %d: %s" % (len(rows), dict(summary)))
print("FAILS %d" % fails)
