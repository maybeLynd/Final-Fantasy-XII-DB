"""sd2_static.py - SWE2-AUDIT-SPEC static re-derivation for SD-2 (2026-09-30), lane tools only (ov31_indep loader).

  S1 who reaches 00366B80: E8/E9 raw index, jcc sweep, and stored 64-bit / rva32 pointers in every section
  S2 the per-item helpers 00366A30 / 00367110 are private to the widget (raw index)
  S3 0036705C is a 002432B0 call site; the 002432B0 site count
  S4 [01E0C1E8] -> "battle_4_c"; 0024A1D0 stores the picture header (buffer+0x10) at slot +0x20
Controls: S1's scanner must find a known stored handler pointer (the 002432B0 raw count must equal the index's).
"""
import json, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

RC = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
rc = lambda a: RC.get("%X" % a, [])
raw, IB = T.raw, T.IB


def refs(target):
    """rel32 E8/E9/0F8x sites in executable sections, and u64 / rva32 stored values in all sections."""
    e8, jcc, q, r = [], [], [], []
    for n, v, vs, p, rs, x in T.SECS:
        blob = raw[p:p + rs]
        if x:
            for i in range(len(blob) - 5):
                b = blob[i]
                if b in (0xE8, 0xE9):
                    d = struct.unpack_from("<i", blob, i + 1)[0]
                    if v + i + 5 + d == target:
                        e8.append(v + i)
                elif b == 0x0F and 0x80 <= blob[i + 1] <= 0x8F and i + 6 <= len(blob):
                    d = struct.unpack_from("<i", blob, i + 2)[0]
                    if v + i + 6 + d == target:
                        jcc.append(v + i)
        pat64 = struct.pack("<Q", target)
        pat32 = struct.pack("<I", target - IB)
        k = blob.find(pat64)
        while k >= 0:
            q.append((n, v + k)); k = blob.find(pat64, k + 1)
        k = blob.find(pat32)
        while k >= 0:
            if (n, v + k) not in q:
                r.append((n, v + k))
            k = blob.find(pat32, k + 1)
    return e8, jcc, q, r


for t in (0x00366B80, 0x002432B0, 0x00366A30, 0x00367110):
    e8, jcc, q, r = refs(t)
    print("%08X  E8/E9 %d (index %d)  jcc %d  u64 %s  rva32 %d %s" % (
        t, len(e8), len(rc(t)), len(jcc), ["%s:%08X" % x for x in q], len(r), ["%s:%08X" % x for x in r[:6]]))
    if t == 0x002432B0:
        print("          0036705C in sites: %s" % (0x0036705C in e8))
    if t in (0x00366A30, 0x00367110):
        print("          sites %s" % ["%08X" % s for s in e8])

p = struct.unpack("<Q", T.rd(0x01E0C1E8, 8))[0]
s = T.rd(p, 16).split(b"\0")[0]
print("[01E0C1E8] = %08X -> %r" % (p, s))
for i in T.dis(0x0024A1D0, 0x0024A260):
    if "0x20]" in i.op_str or "0x18]" in i.op_str or "rdx + 0x10" in i.op_str:
        print("%08X  %s %s" % (i.address, i.mnemonic, i.op_str))
