"""bit7_rederive.py - SWE2-AUDIT-SPEC independent re-derivation of the typed-list page's bit-7 answer (B1-B8).

Own tools only (ind.py, textcache.py). Image-wide over every decoded .text instruction:
  W  every immediate write of bit 7 at displacement +0x38 on any non-rsp base, any width (or 0x80 / and ~0x80 /
     bts 7 / btr 7 / byte forms), with the nearest preceding call in the same owner and whether it is 0024A5A0
  R  every immediate test of bit 7 at +0x38 (test/bt/and-into-register not included; noted as the blind form)
  C  callers of 0024A710 (E8/E9/jcc raw + relocated pointers) and the ecx each passes; callers of 0024A5A0
  L  the loop: 0x3F count, stride 0x48, count-down, start 0208F5B8 (slot 0 +0x38)
Control for W: the package's named writer 0027F7DA must appear.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402
import textcache as TC  # noqa: E402

T = TC.load()
print("decoded instructions", len(T))
pos = {a: k for k, (a, s, m, o, w) in enumerate(T)}

W, R = [], []
pat_w = re.compile(r"^(byte|word|dword|qword) ptr \[(r\w+) \+ 0x38\], (0x80|0xffffff7f|0x7f|0xff7f|7)$")
for k, (a, s, m, o, w) in enumerate(T):
    mm = pat_w.match(o)
    if not mm or mm.group(2) == "rsp":
        continue
    width, base, imm = mm.groups()
    ok = (m == "or" and imm == "0x80") or (m == "and" and imm in ("0xffffff7f", "0x7f", "0xff7f")) or \
         (m in ("bts", "btr") and imm == "7")
    if m == "test" and imm == "0x80":
        R.append((a, m, o, w))
        continue
    if m == "bt" and imm == "7":
        R.append((a, m, o, w))
        continue
    if not ok:
        continue
    prev = None
    for j in range(k - 1, max(0, k - 12), -1):
        if T[j][4] != w:
            break
        if T[j][2] == "call":
            prev = (T[j][0], T[j][3])
            break
    W.append((a, m, o, w, prev))

print("W immediate bit-7 writes at +0x38 (any base, any width), image-wide:", len(W))
for a, m, o, w, prev in W:
    print("  %08X %-4s %-36s owner %-12s prev call %s" % (a, m, o, w, ("%08X %s" % prev) if prev else None))
print("W control 0027F7DA present:", any(a == 0x0027F7DA for a, *_ in W))
inside = [x for x in W if 0x0027F5D0 <= x[0] < 0x002D7600]
print("W inside 0027F5D0..002D7600:", len(inside), " outside:", len(W) - len(inside))
print("W whose nearest preceding call (within 12, same owner) is 0024A5A0:",
      sum(1 for x in W if x[4] and x[4][1] == "0x24a5a0"), "of", len(W))
print("W exceptions:", [("%08X" % x[0], x[4]) for x in W if not (x[4] and x[4][1] == "0x24a5a0")])
print("R immediate bit-7 tests at +0x38 (any base):", len(R))
for a, m, o, w in R:
    print("  %08X %s %s owner %s" % (a, m, o, w))

print("C callers of 0024A710:")
for s, kind in I.calls_to(0x0024A710):
    k = pos[s]
    ecx = None
    for j in range(k - 1, max(0, k - 10), -1):
        mn, ops = T[j][2], T[j][3]
        if re.match(r"^(ecx|rcx|cl)\b", ops) and mn not in ("cmp", "test", "push"):
            ecx = "%08X %s %s" % (T[j][0], mn, ops)
            break
        if mn == "call":
            break
    print("  %08X %-4s owner %s  ecx <- %s" % (s, kind, T[k][4], ecx))
print("C relocated pointers to 0024A710:", [("%08X" % a) for a, v in I.abs64_refs(0x0024A710, 0x0024A711)])
c5 = I.calls_to(0x0024A5A0)
print("C callers of 0024A5A0:", len(c5), "sites; kinds", sorted({k for _, k in c5}))
print("C relocated pointers to 0024A5A0:", [("%08X" % a) for a, v in I.abs64_refs(0x0024A5A0, 0x0024A5A1)])

print("L loop pins:")
for a in (0x0024A733, 0x0024A73B, 0x0024A75F, 0x0024A762, 0x0024A778, 0x0024A790, 0x0024A793, 0x0024A796, 0x0024A799,
          0x0024A99C, 0x0024A9B1, 0x0024A9B5, 0x0024A9B9):
    i = I.ins(a)
    s = "  %08X %s" % (a, I.txt(i))
    for _, op in I.mem_ops(i):
        if op.mem.base == I.X86_REG_RIP:
            s += "  -> %08X" % (i.address + i.size + op.mem.disp)
    print(s)
print("L slot 0 of the registry at 0208F580: +0x38 =", "%08X" % (0x0208F580 + 0x38),
      "; 0208F580 file offset:", I.off(0x0208F580), "(None = zero-initialised virtual tail)")
