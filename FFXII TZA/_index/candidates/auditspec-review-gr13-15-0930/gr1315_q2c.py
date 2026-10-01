"""gr1315_q2c.py - type the objects behind the NEW UI-window hits: walk callers of the hit functions up to the root
that is named by a rip lea (a procedure install) or has no caller, printing each step's root and references."""
import os, sys, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
import bisect, struct

IB, raw = T.IB, T.raw
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def root(va):
    rva = va - IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    e = PD[j]
    for _ in range(16):
        uo = T.off(IB + e[2]); fl = raw[uo] >> 3; cnt = raw[uo + 2]
        if not (fl & 4):
            return IB + e[0]
        e = struct.unpack_from("<III", raw, uo + 4 + ((cnt + 1) & ~1) * 2)
    return IB + e[0]


RC = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
# jcc index (one pass)
JCC = collections.defaultdict(list)
for n, v, vs, p, rs in T.TEXT:
    blob = raw[p:p + min(vs, rs)]
    k = blob.find(b"\x0f")
    while k >= 0 and k + 6 <= len(blob):
        if 0x80 <= blob[k + 1] <= 0x8F:
            JCC[v + k + 6 + struct.unpack_from("<i", blob, k + 2)[0]].append(v + k)
        k = blob.find(b"\x0f", k + 1)


def callers(t):
    return [int(x, 16) for x in RC.get("%X" % t, [])] + JCC.get(t, [])


seen = set()


def walk(f, d, pre=""):
    if f in seen or d > 5:
        print("%s%08X (seen)" % (pre, f)); return
    seen.add(f)
    rr = T.rip_refs(f, f + 1)
    cs = callers(f)
    print("%s%08X callers %d %s | rip %s" % (pre, f, len(cs), ["%08X" % c for c in cs[:8]],
                                            ["%08X %s %s" % h[:3] for h in rr]))
    for c in cs[:8]:
        r = root(c)
        if r:
            walk(r, d + 1, pre + "  ")


for f in (0x0056A1D0, 0x0056A890, 0x0056AE80, 0x0056B100, 0x0057FB00):
    print("== up from %08X" % f)
    walk(f, 0)
