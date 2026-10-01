"""s02_bytes.py - SWE2-AUDIT-SPEC independent byte verification of SECTION-02's retained original bodies (2026-09-30).

Own loader (../auditspec-review-ddres-b6-0930/ind.py, sha asserted; file offsets computed from VAs by the section
table, NOT taken from the manifest). Reads only.
  B  each of the 22 manifest bodies: my file offset vs the manifest's, sha256 of the VA range vs the manifest's, and the
     range vs the .pdata extent (a leaf without .pdata: the range must end at a ret / jmp and be followed by int3 pad)
  X  the extra_data dispatch table 0032E2D0 (24 bytes): sha256, and the six RVA entries decoded to arm VAs
  D  every instruction line of original_disassembly.txt: its hex bytes == image bytes at its VA, and my capstone decode
     text == the retained text (a table line is compared as bytes only)
  C  control: one deliberately shifted range (entry + 1) must NOT match its manifest sha
"""
import hashlib, json, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ddres-b6-0930"))
import ind as I  # noqa: E402

PKG = os.path.join(HERE, "..", "..", "..", "_experiments", "evidence", "continuation-section02-resource-queue")
m = json.load(open(os.path.join(PKG, "original_body_manifest.json")))
assert m["exe_sha256"] == I.SHA
ok_b = 0
total_bytes = 0
for b in m["bodies"]:
    joined = b""
    for r in b["ranges"]:
        a = int(r["start"], 16)
        e = int(r["end_inclusive"], 16)
        n = e - a + 1
        o = I.off(a)
        blk = I.raw[o:o + n]
        joined += blk
        same_off = (o == r["file_offset"])
        same_sha = hashlib.sha256(blk).hexdigest() == r["sha256"] and n == r["bytes"]
    body_ok = hashlib.sha256(joined).hexdigest() == b["sha256"]
    f = int(b["entry"], 16)
    root = I.func_of(f)
    if root == f:
        pr = I.RANGES[f]
        ext = "pdata %s" % [("%08X" % x, "%08X" % (y - 1)) for x, y in pr]
        ext_ok = (min(x for x, _ in pr) == f and max(y for _, y in pr) - 1 == e)
    else:
        last = I.dis(a, e + 1)[-1]
        nxt = I.raw[I.off(e + 1)]
        ext = "no .pdata; last %s, next byte %02X" % (I.txt(last), nxt)
        ext_ok = last.mnemonic in ("ret", "jmp") and last.address + last.size == e + 1
    ok_b += body_ok and same_off and same_sha
    total_bytes += len(joined)
    print("B %s %5d B  file_offset %s  range sha %s  body sha %s  extent %s (%s)" % (
        b["entry"], len(joined), "same" if same_off else "DIFF", "ok" if same_sha else "MISMATCH",
        "ok" if body_ok else "MISMATCH", "ok" if ext_ok else "DIFFERS", ext))
print("B bodies matched %d / %d, %d bytes" % (ok_b, len(m["bodies"]), total_bytes))

for x in m["extra_data"]:
    a = int(x["start"], 16)
    blk = I.raw[I.off(a):I.off(a) + x["size"]]
    ents = struct.unpack("<6I", blk)
    print("X %s %d B sha %s; arms %s" % (x["start"], x["size"], "ok" if hashlib.sha256(blk).hexdigest() == x["sha256"] else "MISMATCH",
                                       ["%08X" % (I.IB + v) for v in ents]))

lines = open(os.path.join(PKG, "original_disassembly.txt"), encoding="utf-8").read().splitlines()
nb = nt = bad = tbad = 0
pat = re.compile(r"^([0-9A-F]{8})  ([0-9a-f]+)\s+(\S+)\s*(.*)$")
for L in lines:
    mm = pat.match(L)
    if not mm:
        continue
    a = int(mm.group(1), 16)
    hx = bytes.fromhex(mm.group(2))
    nb += 1
    if I.rd(a, len(hx)) != hx:
        bad += 1
        print("D BYTES MISMATCH", L)
        continue
    i = I.ins(a)
    mine = ("%s %s" % (i.mnemonic, i.op_str)).strip()
    theirs = ("%s %s" % (mm.group(3), mm.group(4).strip())).strip()
    if re.sub(r"\s+", " ", mine) != re.sub(r"\s+", " ", theirs):
        tbad += 1
        if tbad <= 5:
            print("D text differs %08X mine=%r retained=%r" % (a, mine, theirs))
    nt += 1
print("D retained instruction lines: %d; bytes equal: %d; decode text equal: %d" % (nb, nb - bad, nt - tbad))

b0 = m["bodies"][1]
r0 = b0["ranges"][0]
a = int(r0["start"], 16) + 1
blk = I.raw[I.off(a):I.off(a) + r0["bytes"]]
print("C shifted-range control (entry+1) matches manifest sha:", hashlib.sha256(blk).hexdigest() == r0["sha256"], "(must be False)")
