"""vtable_slots.py MEMBERS.tsv - for every member entry, find each qword in .rdata holding it, walk back to the vtable
start (the qword after an RTTI complete-object-locator pointer), and report slot index and the RTTI class name.
A vtable start is the first slot after a qword that points at a valid COL (signature 1, image-relative type descriptor)."""
import sys, struct, collections
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
BASE = 0x120000
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    name = d[o:o + 8].rstrip(b"\0"); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, BASE + va, vs, ro, rs))
def off(a):
    for nm, va, vs, ro, rs in secs:
        if va <= a < va + rs: return ro + (a - va)
    return None
def va_of(o):
    for nm, va, vs, ro, rs in secs:
        if ro <= o < ro + rs: return va + (o - ro)
rdata = [s for s in secs if s[0] == b".rdata"][0]
def col_name(p):
    o = off(p)
    if o is None: return None
    sig, offv, cdoff, td_rva = struct.unpack_from("<IIII", d, o)
    if sig != 1: return None
    to = off(BASE + td_rva)
    if to is None: return None
    nm = d[to + 16:to + 16 + 200].split(b"\0")[0]
    return nm.decode("latin1") if nm.startswith(b".?A") else None
members = [int(l.strip(), 16) for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
mset = set(members)
lo, hi = rdata[3], rdata[3] + rdata[4]
hits = collections.defaultdict(list)
for o in range(lo - lo % 8, hi - 8, 8):
    q = struct.unpack_from("<Q", d, o)[0]
    if q in mset:
        hits[q].append(va_of(o))
summary = collections.Counter(); bad = []
for m in members:
    rows = []
    for v in hits.get(m, []):
        # walk back up to 64 slots to find the COL pointer
        slot = None; cname = None
        for k in range(0, 64):
            prev = struct.unpack_from("<Q", d, off(v - 8 * (k + 1)))[0]
            nm = col_name(prev)
            if nm:
                slot = k; cname = nm; break
        rows.append((slot, cname))
    kinds = {(s, (c or "")[:24]) for s, c in rows}
    summary[len(rows)] += 1
    if not rows or any(s is None or "PClassDescriptor" not in (c or "") for s, c in rows):
        bad.append(("%08X" % m, rows[:3]))
    slots = collections.Counter(s for s, c in rows)
    for s in slots: summary[("slot", s)] += slots[s]
print("members", len(members), "appearance-count histogram", {k: v for k, v in summary.items() if not isinstance(k, tuple)})
print("slots", {k[1]: v for k, v in summary.items() if isinstance(k, tuple)})
print("members with an appearance outside a PClassDescriptor vtable or none:", len(bad))
for b in bad[:12]: print("  ", b)
