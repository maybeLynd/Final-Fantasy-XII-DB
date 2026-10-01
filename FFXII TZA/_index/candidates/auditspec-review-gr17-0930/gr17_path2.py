"""variants of the direct reach set to 00312280, and a site-by-site decode of one path (reviewer instrument check)"""
import sys, os, struct, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gr17_graph as GG
G = GG.G; T = GG.T
from collections import deque


def build(leaf, jcc):
    ed = {}
    for k, sites in GG.RC.items():
        t = int(k, 16)
        for s in sites:
            s = int(s, 16)
            a = G.root(s) if not leaf else GG.fn(s)
            if a is None:
                continue
            b = GG.tfn(t)
            if a != b:
                ed.setdefault(a, {}).setdefault(b, s)
    if jcc:
        for n, v, vs, p, rs in T.TEXT:
            blob = T.raw[p:p + min(vs, rs)]
            for m in re.finditer(rb"\x0f[\x80-\x8f]", blob):
                k = m.start()
                if k + 6 > len(blob):
                    continue
                d = struct.unpack_from("<i", blob, k + 2)[0]
                t = v + k + 6 + d
                a = G.root(v + k) if not leaf else GG.fn(v + k)
                if a is None or G.root(t) != t or a == t:
                    continue
                # keep only a jcc that decodes at this address
                ins = list(T.md.disasm(blob[k:k + 6], v + k, 1))
                if not ins or ins[0].size != 6:
                    continue
                ed.setdefault(a, {}).setdefault(t, v + k)
    return ed


def reach(ed, tgt=0x00312280):
    rev = {}
    for a, bs in ed.items():
        for b in bs:
            rev.setdefault(b, set()).add(a)
    R = {tgt}; st = [tgt]
    while st:
        x = st.pop()
        for y in rev.get(x, ()):
            if y not in R:
                R.add(y); st.append(y)
    return R


def path(ed, src, tgt=0x00312280):
    prev = {src: None}; q = deque([src])
    while q:
        x = q.popleft()
        if x == tgt:
            break
        for y in ed.get(x, ()):
            if y not in prev:
                prev[y] = x; q.append(y)
    if tgt not in prev:
        return None
    p = []; y = tgt
    while prev[y] is not None:
        x = prev[y]; p.append((x, ed[x][y], y)); y = x
    return list(reversed(p))


if __name__ == "__main__":
    probes = [0x0024CFF0, 0x002693D0, 0x002E3AF0, 0x00319140, 0x002EB780, 0x003603F0, 0x0032E620]
    for leaf, jcc in ((False, False), (True, False), (False, True), (True, True)):
        ed = build(leaf, jcc)
        R = reach(ed)
        print("variant leaf-mapped=%s jcc=%s: %d functions reach 00312280; probes %s" % (
            leaf, jcc, len(R), {"%08X" % p: (p in R) for p in probes}))
    ed = build(False, False)
    for src in (0x002693D0, 0x0024CFF0, 0x002E3AF0):
        p = path(ed, src)
        print("path from %08X (pdata-rooted E8/E9 only): %s" % (src, "none" if p is None else len(p)))
        for a, s, b in (p or []):
            i = T.dis(s, s + 15, 1)[0]
            print("    %08X in %08X: %s %s  -> %08X" % (s, G.root(s), i.mnemonic, i.op_str, b))
