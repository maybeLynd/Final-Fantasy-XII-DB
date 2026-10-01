"""rc4b_scan.py - RC-4 residue: the two view-pointer escapes into the external object [A+8] (ORACLE, 2026-09-30).

After pass 2, only two routes hand the render object's interior to code that the flow cannot follow:
  E1 0060CE50 stores rdx = view + 8 at [ext + 0xA8], where rcx = [A+8] (00187950: 001880DE / 001880E2);
  E2 001F0AD0 calls [[rdx] + 0x10] on rdx = [A+8] with r8 = a view pair (A+0x358 or A+0x690; 00187D4F / 00187D5D).
[A+8] is the constructor's rdx: the application object's +0xE8 (0017D04F -> 00189000 -> 00184F20 +0x4C).

For such code to write A+0xDAC through a pointer P = A + K it received, it needs a store at displacement
d = 0xDAC - K from P, or an indexed or derived form. This scan lists every store instruction in .text, with or without
.pdata, whose own displacement is exactly one of those d:
  K in {view + 8} = {0x28, 0x1B8, 0x360, 0x4F0, 0x698, 0x828}, K in {pairs} = {0x358, 0x690}; and, because a receiver
  can load the view's own pointer fields, every self-field value at the pass-2 fixpoint (0xF8, 0x288, 0x430, 0x468,
  0x5C0, 0x5F8, 0x360, 0x4F0, 0x698, 0x828, 0x768, 0x7A0, 0x8F8, 0x930).
Control: with K = 0 (d = 0xDAC) the scan must find the five known machine and constructor stores.
"""
import collections, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-as7-pages-0930"))
import arc  # noqa: E402
img = arc.img

KS = sorted({0x28, 0x1B8, 0x360, 0x4F0, 0x698, 0x828, 0x358, 0x690,
             0xF8, 0x288, 0x430, 0x468, 0x5C0, 0x5F8, 0x768, 0x7A0, 0x8F8, 0x930})
t = img.blob[img.TR:img.TR + img.TN]


def stores_with_disp(d):
    pat = struct.pack("<I", d)
    hits = set()
    for m in re.finditer(re.escape(pat), t):
        for back in range(2, 8):
            a = img.T0 + m.start() - back
            xs = img.dis(a, 15)
            if not xs or xs[0].address != a:
                continue
            x = xs[0]
            if x.operands and x.operands[0].type == 3 and x.operands[0].mem.disp == d and x.mnemonic not in (
                    "cmp", "test", "bt", "prefetchnta", "prefetcht0", "lea", "nop") and "rsp" not in x.op_str \
                    and "rip" not in x.op_str and "rbp" not in x.op_str.split(",")[0]:
                hits.add((a, x.mnemonic, x.op_str, x.operands[0].size))
    return sorted(hits)


ctl = stores_with_disp(0xDAC)
known = {0x00185020, 0x00187891, 0x001878B3, 0x001878D5, 0x001878E5}
ok = known <= set(h[0] for h in ctl)
print("%s  control: d = 0xDAC finds the five known stores (%d stores with that displacement)" % ("PASS" if ok else "FAIL", len(ctl)))
tot = 0
for K in KS:
    d = 0xDAC - K
    hs = stores_with_disp(d)
    tot += len(hs)
    print("K %#05x d %#05x: %d store(s)" % (K, d, len(hs)))
    for a, mn, op, sz in hs:
        o = img.owner(a)
        print("    %08X %-6s %-44s size %d in %s" % (a, mn, op, sz, ("%08X" % o) if o else "no .pdata"))
print("total candidate stores: %d" % tot)
sys.exit(0 if ok else 1)
