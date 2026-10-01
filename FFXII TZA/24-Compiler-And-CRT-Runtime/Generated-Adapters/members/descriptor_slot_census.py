"""descriptor_slot_census.py SLOT [OUT.tsv [SIZE]] - enumerate every vtable whose RTTI complete-object locator names a
Phyre PClassDescriptor* class, take the qword at SLOT, and group the targets by function body (size + bytes with
rel32 call/jmp displacements masked). Prints the groups; with OUT, writes the entries of the largest group (or the group of body size WANT)
whose body is identical across members (masking only rel32 displacements)."""
import sys, struct, collections, re
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUN = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
SLOT = int(sys.argv[1]); OUT = sys.argv[2] if len(sys.argv) > 2 else None; WANT = int(sys.argv[3]) if len(sys.argv) > 3 else None
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
funcs = {}
for line in open(FUN, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except Exception: pass
rdata = [s for s in secs if s[0] == b".rdata"][0]
text = [s for s in secs if s[0] == b".text"][0]
def col_name(p):
    o = off(p)
    if o is None: return None
    sig, _, _, td = struct.unpack_from("<IIII", d, o)
    if sig != 1: return None
    to = off(BASE + td)
    if to is None: return None
    nm = d[to + 16:to + 216].split(b"\0")[0]
    return nm.decode("latin1") if nm.startswith(b".?A") else None
tlo, thi = text[1], text[1] + text[2]
groups = collections.defaultdict(list); vt = 0
for o in range(rdata[3], rdata[3] + rdata[4] - 16, 8):
    q = struct.unpack_from("<Q", d, o)[0]
    if not (rdata[1] <= q < rdata[1] + rdata[4]): continue
    nm = col_name(q)
    if not nm or "PClassDescriptor" not in nm: continue
    start = o + 8
    if start + 8 * (SLOT + 1) > rdata[3] + rdata[4]: continue
    tgt = struct.unpack_from("<Q", d, start + 8 * SLOT)[0]
    if not (tlo <= tgt < thi): continue
    vt += 1
    sz = funcs.get(tgt)
    if sz is None: groups[("not-an-entry",)].append((tgt, nm)); continue
    body = bytearray(d[off(tgt):off(tgt) + sz])
    # mask rel32 after E8/E9 opcodes
    i = 0
    while i < len(body) - 4:
        if body[i] in (0xE8, 0xE9):
            body[i + 1:i + 5] = b"\0\0\0\0"; i += 5
        else:
            i += 1
    groups[(sz, bytes(body))].append((tgt, nm))
print("descriptor vtables", vt, "distinct slot-%d bodies" % SLOT, len(groups))
ranked = sorted(groups.items(), key=lambda kv: -len({t for t, _ in kv[1]}))
for k, v in ranked[:8]:
    ents = sorted({t for t, _ in v})
    print(" size", k[0], "distinct functions", len(ents), "appearances", len(v), "e.g.", ["%08X" % e for e in ents[:3]])
if OUT:
    k, v = [kv for kv in ranked if WANT is None or kv[0][0] == WANT][0]
    ents = sorted({t for t, _ in v})
    open(OUT, "w").write("# slot-%d body group of PClassDescriptor vtables, descriptor_slot_census.py\n" % SLOT + "\n".join("%08X" % e for e in ents) + "\n")
    print("wrote", len(ents))
