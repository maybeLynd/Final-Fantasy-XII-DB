"""print a shortest direct path (with the concrete site of each edge) from each given function to 00312280"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gr17_graph as GG
from collections import deque
site = {}
for k, sites in GG.RC.items():
    t = int(k, 16)
    for s in sites:
        a = GG.fn(int(s, 16)); b = GG.tfn(t)
        if a != b:
            site.setdefault((a, b), int(s, 16))
def path(src):
    prev = {src: None}; q = deque([src])
    while q:
        x = q.popleft()
        if x == GG.TARGET:
            break
        for y in GG.edges.get(x, ()):
            if y not in prev:
                prev[y] = x; q.append(y)
    if GG.TARGET not in prev:
        return None
    p = []; y = GG.TARGET
    while prev[y] is not None:
        x = prev[y]; p.append("%08X -[%s]-> %08X" % (x, "%08X" % site[(x, y)] if (x, y) in site else "jcc", y)); y = x
    return list(reversed(p))
for a in sys.argv[1:]:
    print(a, path(int(a, 16)))
