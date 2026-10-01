"""sd160_static_indep.py - SWE2-AUDIT-SPEC (review of OPUS af6684173, 2026-09-30). Independent static checks for F1-F3.

Lane loader ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha256 asserted), not retool.py.
  1 the table at 01E09EE8 (4 dwords) and the tail of 002396B0 after the +0x58 store
  2 callers of the nibble writer 00269FE0, of 002396B0, of the reader 00263C20's caller 003171C0, and of the two verb
    handlers (rel32 E8/E9 + jcc 0F 8x + abs64/rva32 data slots) - so "the constant sources are the two verbs" is tested
    against every route into the two writers, not only the verb table
  3 every instruction image-wide that writes the low nibble of a byte at displacement +0x0E through the idiom
    `and byte [r+0xe], 0xf0` (the F2 idiom), with its .pdata root - the other writers of the same nibble
Control: 2 must return 003528D6 for 00269FE0 and 0051035B for 002396B0 (the package's own sites); 3 must return
0026A033.
"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402

print("== 1 table 01E09EE8:", struct.unpack_from("<4I", T.raw, T.off(0x01E09EE8)))
for i in T.dis(0x002396D6, count=14):
    print("  %08X  %-8s %s" % (i.address, i.mnemonic, i.op_str))

print("== 2 callers")
for f in (0x00269FE0, 0x002396B0, 0x003171C0, 0x003528C0, 0x00510340, 0x00263C20):
    r = T.rel32_callers(f)
    print("  %08X rel32 %d %s | jcc %s | data %s" % (f, len(r), r[:40], T.jcc_callers(f), T.data_refs(f)))

print("== 3 'and byte [r+0xe], 0xf0' sites image-wide")
pat = [bytes([0x80, m, 0x0E, 0xF0]) for m in range(0x60, 0x68)]      # 80 /4 disp8, modrm mod=01 reg=4 rm=0..7
pat += [bytes([0x41, 0x80, m, 0x0E, 0xF0]) for m in range(0x60, 0x68)]
hits = set()
for n, v, vs, p, rs in T.TEXT:
    blob = T.raw[p:p + min(vs, rs)]
    for pt in pat:
        k = blob.find(pt)
        while k >= 0:
            a = v + k
            ins = T.dis(a, count=1)
            if ins and ins[0].mnemonic == "and" and ins[0].op_str.endswith("0xe], 0xf0"):
                hits.add((a, ins[0].op_str))
            k = blob.find(pt, k + 1)
for a, op in sorted(hits):
    nxt = T.dis(a, count=4)
    print("  %08X  and %s   next: %s" % (a, op, " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in nxt[1:4])))
print("  total %d" % len(hits))
