"""RC-29 follow-on: the kind-7 ids that have no constant request ride .rdata id lists handed to three list-request
helpers (SWE2-DATA 2026-09-30), static.

  003933F0(pool, out, u32 ids[], n)          -> 00249320(pool, 7, ids[i]) for i < n
  00393460(pool, out, rec[], n)              -> 002493D0(pool, 7, rec.id, 2, rec.ptr, 2), rec stride 0x18 {u32 id; u64 ptr@+8; u32@+0x10}
  003934F0(pool, out, rec[], pairs[], n@stack) -> 002493D0 per rec (stride 0x18), pairs supply r9/arg
Every raw call site of the three helpers is decoded: r8 = lea [rip+table] and the count register (mov r9d, imm / the
0x20 stack slot / lea r9d,[reg+1] with reg zeroed in the caller) are recovered by a linear scan back from the call.
Each id is resolved through the kind-7 path array (kind7.py). The output lists which file each list requests.
Then the ids the owning pages call 'no constant request' are looked up: the .mrp set and the .cl2 ids 0xE2..0xE4.
Controls: K1 save_load.mrp (0x6F) must come out of 00582790's list (the MRP sheet's own traced request, 003933F0);
K2 a raw sweep of every .rdata/.data u32 equal to 0xE2/0xE3/0xE4 followed or preceded by another kind-7 .cl2/.mrp id
is printed so a list outside these helpers would still show.
"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, BASE, secs, owner, dis, u32, u64, text_range, containing_ins  # noqa
from kind7 import paths

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


arr, P = paths(7, 0x4D2, stop_on_miss=False)  # the first language arm; the array repeats per arm from 0x4D2
B = chr(92)


def nm(i):
    s = P.get(i)
    return s.split(B)[-1] if s else "(no path 0x%X)" % i


def rawcallers(t):
    t0 = [s for s in secs if s[0] == ".text"][0]
    name, va, vs, ro, rs = t0
    blob = d[ro:ro + rs]
    out = []
    for p in range(len(blob) - 5):
        if blob[p] in (0xE8, 0xE9):
            rel = struct.unpack_from("<i", blob, p + 1)[0]
            if BASE + va + p + 5 + rel == t:
                out.append(BASE + va + p)
    return out


def rip_t(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


def args_at(site):
    f = owner(site)
    body = dis(f)
    i = [k for k, x in enumerate(body) if x.address == site][0]
    r8 = cnt = stack20 = None
    zero = set()
    R64 = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
    R64.update({"r%dd" % k: "r%d" % k for k in range(8, 16)})
    for x in body[:i]:
        if x.mnemonic == "xor":
            a = x.op_str.split(", ")
            if len(a) == 2 and a[0] == a[1]:
                zero.add(R64.get(a[0], a[0]))
    for x in reversed(body[max(0, i - 24):i]):
        if r8 is None and x.mnemonic == "lea" and x.op_str.startswith("r8,"):
            r8 = rip_t(x)
        if cnt is None and x.op_str.startswith("r9d,"):
            src = x.op_str.split(", ", 1)[1]
            if x.mnemonic == "mov" and src.startswith("0x") or src.isdigit():
                cnt = int(src, 0)
            elif x.mnemonic == "lea":
                m = re.match(r"\[(\w+) \+ (0x[0-9a-f]+|\d+)\]", src)
                if m and m.group(1) in zero:
                    cnt = int(m.group(2), 0)
        if stack20 is None and x.mnemonic == "mov" and x.op_str.startswith("dword ptr [rsp + 0x20],"):
            v = x.op_str.split(", ")[1]
            if v.startswith("0x") or v.isdigit():
                stack20 = int(v, 0)
    return f, r8, cnt, stack20


rows = []
for helper, stride in ((0x003933F0, 4), (0x00393460, 0x18), (0x003934F0, 0x18)):
    for s in sorted(set(rawcallers(helper))):
        f, tab, n, st = args_at(s)
        if helper == 0x003934F0:
            n = st
        ids = [u32(tab + stride * k) for k in range(n)] if tab and n else []
        rows.append((helper, s, f, tab, n, ids))
        print("%08X <- %08X in %08X  table %s  n=%s  %s" % (helper, s, f, "%08X" % tab if tab else "?", n,
              ", ".join("0x%X %s" % (v, nm(v)) for v in ids)))

req = {v: (h, s, f) for h, s, f, t, n, ids in rows for v in ids}
check("K1 save_load.mrp (0x6F) is requested through 00582790's list", req.get(0x6F, (0, 0, 0))[2] == 0x00582790)
mrps = {i: nm(i) for i in P if P[i].lower().endswith(".mrp")}
print("kind-7 .mrp ids in the path array:", ", ".join("0x%X %s" % (i, s) for i, s in sorted(mrps.items())))
for i, s in sorted(mrps.items()):
    print("   %-16s 0x%03X  %s" % (s, i, "list %08X in %08X" % (req[i][1], req[i][2]) if i in req else "not in these lists"))
cl2 = [i for i in P if P[i].lower().endswith(".cl2")]
print(".cl2 ids:", ", ".join("0x%X %s" % (i, nm(i)) for i in cl2), "- in these lists:", [hex(i) for i in cl2 if i in req])

# K2: any u32 list in file-backed data holding a .cl2 id next to another menu-resource id (+-4 bytes or +-0x18)
menu_ids = set(mrps) | set(cl2)
hits = []
for name, va, vs, ro, rs in secs:
    if name not in (".rdata", ".data"):
        continue
    for p in range(0, rs - 4, 4):
        v = struct.unpack_from("<I", d, ro + p)[0]
        if v in cl2:
            a = BASE + va + p
            nb = [u32(a + k) for k in (-0x18, -4, 4, 0x18)]
            if any(x in menu_ids for x in nb if x is not None):
                hits.append((a, v, nb))
print("K2 data dwords equal to a .cl2 id with a menu-resource id neighbour: %d" % len(hits))
for a, v, nb in hits[:20]:
    # classify: the console page table (manifest_walker.py) or an identity run (id k at stride 0x18, 0..0xFF)
    ident = u32(a - 0x18) == v - 1 and u32(a + 0x18) == v + 1
    kind = "console page table 008FCE00 (manifest_walker.py)" if 0x008FCE00 <= a < 0x008FD2D0 else (
        "identity run (id at +0, id-1 / id+1 at -0x18 / +0x18)" if ident else "UNCLASSIFIED")
    print("   %08X = 0x%X  neighbours %s  -> %s" % (a, v, nb, kind))
check("K2 every data hit is the console page table or an identity run (no request list carries a .cl2 id)",
      all((0x008FCE00 <= a < 0x008FD2D0) or (u32(a - 0x18) == v - 1 and u32(a + 0x18) == v + 1) for a, v, nb in hits))
k3 = 0x01F435F8
while u32(k3 - 0x18) == u32(k3) - 1:
    k3 -= 0x18
k4 = 0x01F435F8
while u32(k4 + 0x18) == u32(k4) + 1:
    k4 += 0x18
print("   the identity run spans %08X..%08X, ids 0x%X..0x%X, stride 0x18" % (k3, k4, u32(k3), u32(k4)))
# K3: the .mrp ids with neither a list nor a constant request: sweep the image for the id as an argument-shaped
# immediate (the same instrument as cl2_requests.py S1, whose controls C1/C2 find the Loca.mrp and w_menu.mrp constants)
t0, t1, ro = text_range()
blob = d[ro:ro + (t1 - t0)]
REQ = re.compile(r"^(r8d|edx|ecx|r9d|r8|rdx), 0x|^dword ptr \[rsp \+ 0x2[08]\], 0x|^(r8d|edx), \[\w+ \+ 0x")
API = {"0x249180", "0x249210", "0x2493d0", "0x249350", "0x249320", "0x32e400", "0x32e620", "0x32e3f0"}
for v in sorted(i for i in mrps if i not in req):
    found = []
    start = 0
    pat = struct.pack("<I", v)
    while True:
        p = blob.find(pat, start)
        if p < 0:
            break
        start = p + 1
        x, how = containing_ins(t0 + p)
        if x is None or not REQ.search(x.op_str) or ("0x%x" % v) not in x.op_str:
            continue
        f = owner(x.address)
        if f and any(y.mnemonic == "call" and y.op_str in API and x.address < y.address <= x.address + 0x30 for y in dis(f)):
            found.append(x.address)
    print("K3 %-16s 0x%03X constant request sites: %s" % (mrps[v], v, " ".join("%08X" % a for a in found) or "none"))
print("FAILS %d" % FAILS)
