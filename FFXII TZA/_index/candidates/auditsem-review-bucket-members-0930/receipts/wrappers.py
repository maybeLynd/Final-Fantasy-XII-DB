"""SWE2-AUDIT-SEM: lift the unresolved request sites to their wrappers and census the wrappers' callers.
For each request/sizeof site whose kind or id is unresolved, take the containing function (.pdata chain root),
collect every rel32 call/jmp to it, and resolve constant rcx/rdx/r8/r9 at each caller (volatile regs killed at calls,
non-volatile kept). Repeats one more level for callers whose args stay unresolved. Reports every caller that puts
9 in one arg register and any of the probe ids in another, plus the loop-formed kind-9 range found separately."""
import struct, collections, bisect
import img, reqsites as R

# .pdata
pd = [s for s in img.secs if s[0] == ".pdata"][0]
praw = img.raw[pd[3]:pd[3] + pd[4]]
funcs = []
for i in range(0, len(praw) - 11, 12):
    b, e, u = struct.unpack_from("<III", praw, i)
    if b == 0:
        break
    funcs.append((img.BASE + b, img.BASE + e, u))
funcs.sort()
starts = [f[0] for f in funcs]
# chain roots: an unwind info with UNW_FLAG_CHAININFO (flags & 4) points to its parent's RUNTIME_FUNCTION
def root(a):
    i = bisect.bisect_right(starts, a) - 1
    if i < 0:
        return None
    b, e, u = funcs[i]
    for _ in range(16):
        uo = img.off(img.BASE + (u & ~1))
        if uo is None:
            break
        ver_flags = img.raw[uo]
        flags = ver_flags >> 3
        if not (flags & 4):
            break
        ncodes = img.raw[uo + 2]
        co = uo + 4 + 2 * ((ncodes + 1) & ~1)
        pb, pe, pu = struct.unpack_from("<III", img.raw, co)
        b, e, u = img.BASE + pb, img.BASE + pe, pu
    return b

VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
def const_regs(seq):
    known = {}
    for ins in seq:
        m, ops = ins.mnemonic, [o.strip() for o in ins.op_str.split(",")]
        if m == "call":
            for v in VOL:
                known.pop(v, None)
            continue
        if m in ("ret", "jmp"):
            known = {}
            continue
        if len(ops) != 2:
            continue
        d, s = R.norm(ops[0]), ops[1]
        if m == "mov":
            if s.startswith("0x") or s.isdigit():
                known[d] = int(s, 0)
            elif R.norm(s) in known:
                known[d] = known[R.norm(s)]
            else:
                known.pop(d, None)
        elif m == "xor" and R.norm(ops[0]) == R.norm(ops[1]):
            known[d] = 0
        elif m == "lea" and s.startswith("[") and "rip" not in s and "*" not in s:
            inner = s.strip("[]").replace(" ", "")
            val, okk = 0, True
            for p in inner.replace("-", "+-").split("+"):
                if not p:
                    continue
                if p.lstrip("-").startswith("0x") or p.lstrip("-").isdigit():
                    val += int(p, 0)
                elif R.norm(p) in known:
                    val += known[R.norm(p)]
                else:
                    okk = False
            if okk:
                known[d] = val
            else:
                known.pop(d, None)
        else:
            known.pop(d, None)
    return known

sites = []
for e in R.ENTRIES:
    for site, kind in R.refs.get(e, []):
        k = const_regs(R.decode_back(site))
        sites.append((site, e, k.get("rcx"), k.get("rdx")))
unres = [s for s in sites if s[2] is None or s[3] is None]
wr = collections.defaultdict(list)
for s in unres:
    wr[root(s[0])].append(s[0])
print("request/sizeof sites:", len(sites), " unresolved:", len(unres), " wrapper functions:", len(wr))
PROBE = {0x1C: "fhmusicdata(9,0x1C)", 0x01: "test_map_ref(9,0x01)"}
hits, level2 = [], collections.defaultdict(list)
seen = set()
def census(fn, depth):
    if fn in seen or fn is None:
        return
    seen.add(fn)
    callers = R.refs.get(fn, [])
    for c, kind in callers:
        k = const_regs(R.decode_back(c))
        args = {r: k.get(r) for r in ("rcx", "rdx", "r8", "r9")}
        vals = [v for v in args.values() if v is not None]
        if 9 in vals and any(v in PROBE for v in vals if v != 9 or list(args.values()).count(9) > 1):
            hits.append((depth, "%08X" % fn, "%08X" % c, {r: (hex(v) if v is not None else None) for r, v in args.items()}))
        if all(v is None for v in args.values()) and depth < 2:
            level2[depth + 1].append(root(c))
    print("  depth %d wrapper %08X: %d callers" % (depth, fn, len(callers)))
for fn in sorted(w for w in wr if w):
    census(fn, 1)
for fn in sorted(set(x for x in level2[2] if x)):
    census(fn, 2)
print("callers placing 9 beside a probe id (fhmusicdata 0x1C / test_map_ref 0x01) in the arg registers:")
for h in hits:
    print("  ", h)
print("hits:", len(hits))

print("== all wrapper-caller arg tuples carrying the constant 9 (control view)")
seen2 = set()
for fn in sorted(seen):
    for c, kind in R.refs.get(fn, []):
        k = const_regs(R.decode_back(c))
        args = tuple(k.get(r) for r in ("rcx", "rdx", "r8", "r9"))
        if 9 in args:
            print("   %08X <- %08X  rcx,rdx,r8,r9 = %s" % (fn, c, ["?" if v is None else hex(v) for v in args]))
