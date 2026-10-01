"""regval_audit3.py - SWE2-AUDIT-SPEC (2026-09-30): two width defects of regval.py, measured on the 135 push-site walks.
  D1 truncation: regval models `movzx/movsx r, <8- or 16-bit reg>` as a copy of the whole source register, so a value
     like 0x107 would pass through `movzx ecx, cl` as 0x107 instead of 7. Count walk nodes that are such instructions.
  D2 sub-register pin: edge_pin pins the whole register on `cmp al, K` / `test al, al`. Count walk nodes that are a
     je/jne whose preceding instruction compares an 8- or 16-bit register.
A node is (function, instruction address) that val() visited for a site (memo cleared per site).
Control for D1: the unrelated instruction at 001BAD17 (just after `movzx ecx, cl`, regval_audit.out C2) is a D1 node of
its own query.
"""
import collections, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd164-167-0930"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import arena_ix as X  # noqa: E402
import regval as V  # noqa: E402

SMALL = re.compile(r"\b(al|ah|bl|bh|cl|ch|dl|dh|sil|dil|bpl|spl|r\d+b|ax|bx|cx|dx|si|di|bp|sp|r\d+w)\b")
cur, reach = None, collections.defaultdict(set)
_val = V.val


def val(f, k, reg, depth, onpath):
    ins, idx, preds = V.body(f)
    for p in preds[k]:
        reach[cur].add((f, p))
    return _val(f, k, reg, depth, onpath)


V.val = val


def classify(f, k):
    ins, idx, preds = V.body(f)
    i = ins[k]
    out = []
    if i.mnemonic in ("movzx", "movsx") and "ptr" not in i.op_str and SMALL.search(i.op_str.split(",", 1)[1]):
        out.append("D1 %s %s" % (i.mnemonic, i.op_str))
    if i.mnemonic in ("je", "jne") and k > 0:
        c = ins[k - 1]
        if c.mnemonic in ("cmp", "test") and "ptr" not in c.op_str and SMALL.match(c.op_str.split(",")[0].strip()):
            out.append("D2 %s %s / %s" % (c.mnemonic, c.op_str, i.mnemonic))
    return out


SITES = sorted(V.SC["calls"].get(0x0036C1D0, ()))
for s in SITES:
    cur = s
    V._memo.clear()
    V.value_at(s[0], s[1], "rcx", 5)
hits = collections.defaultdict(list)
for s, nodes in reach.items():
    for f, k in nodes:
        for c in classify(f, k):
            hits[s].append((V.body(f)[0][k].address, c))
print("walks: %d; walks crossing a D1 or D2 node: %d" % (len(reach), len(hits)))
for s in sorted(hits):
    print("   site %08X/%08X  value %s" % (s[0], s[1], sorted(V.value_at(s[0], s[1], "rcx", 5), key=str)))
    for a, c in sorted(set(hits[s])):
        print("        %08X %s" % (a, c))
cur = ("ctl",)
V._memo.clear()
CF = max(f for f, n in V.SZ.items() if f <= 0x001BAD17 < f + n)
V.value_at(CF, 0x001BAD17, "rcx", 1)
print("control D1: the walk from 001BAD17 visited in its own walk and classified D1: %s" % any(
    c.startswith("D1") for f, k in reach[("ctl",)] for c in classify(f, k)))
