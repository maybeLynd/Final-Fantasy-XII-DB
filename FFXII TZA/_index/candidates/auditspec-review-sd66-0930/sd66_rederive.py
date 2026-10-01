"""sd66_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-66 (2026-09-30). Read-only on the image.
The author's scan walks only catalogued functions, only `call`, and silently drops a static whose vtable its
lea->mov pattern cannot find. This sweep is independent of the function list: every byte position in .text that
decodes as `call/jmp qword ptr [reg + 0x40]` (any register, disp8 or disp32), then up to 8 instructions back (linear
decode from the owner's boundary when there is one, else from 24 bytes back) for how reg was loaded. Each static G
is classified by the RTTI of the vtable stored into it, found with tk.rip_refs over [G, G+8) (stores whose source
register was just loaded by `lea reg, [rip]`)."""
import sys, re, collections, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\analysis-kit\gfz-scripts")
import tk
import retool as T

ROUTES = {0x00632960, 0x00632A10, 0x00632A70, 0x00632BE0, 0x00632B30}
blob = tk.d[tk.TRO:tk.TRO + min(tk.TRS, tk.TVS)]
sites = []
for i in range(len(blob) - 8):
    if blob[i] != 0xFF: continue
    a = tk.TVA + i
    for s in (a - 1, a):            # optional REX prefix
        x = tk._decode_at(s)
        if x is None or x.mnemonic not in ("call", "jmp"): continue
        if re.fullmatch(r"qword ptr \[\w+ \+ 0x40\]", x.op_str) and "rip" not in x.op_str and "rsp" not in x.op_str:
            sites.append(x); break
sites = {x.address: x for x in sites}
print("raw call/jmp [reg + 0x40] sites in .text:", len(sites))

vtcache = {}
def static_vt(g):
    if g in vtcache: return vtcache[g]
    out = None
    hits, raw = tk.rip_refs(g, g + 1)
    for x, k, t in hits:
        if not tk.is_store(x, k) or x.operands[1].type != tk.X86_OP_REG: continue
        src = x.reg_name(x.operands[1].reg)
        o, how = tk.owner(x.address)
        if o is None: continue
        prev = [y for y in tk.dis(max(o, x.address - 40), x.address + 1)]
        for y in reversed(prev[:-1]):
            if y.mnemonic == "lea" and y.op_str.startswith(src + ", [rip"):
                out = y.address + y.size + y.operands[1].mem.disp; break
        if out: break
    vtcache[g] = out
    return out

leaform = collections.defaultdict(list)
classes = collections.Counter(); per_fn = collections.defaultdict(list); unknown = collections.Counter(); nonstatic = 0
for a, x in sorted(sites.items()):
    reg = re.match(r"qword ptr \[(\w+) \+", x.op_str).group(1)
    o, how = tk.owner(a)
    start = o if o is not None and a - o < 0x4000 else a - 24
    prev = [y for y in tk.dis(max(start, a - 64), a + x.size) if y.address < a]
    # keep only a decode that lands on a
    if not any(y.address + y.size == a for y in prev):
        prev = [y for y in tk.dis(a - 24, a + x.size) if y.address < a]
    g = None
    for y in reversed(prev[-8:]):
        if y.mnemonic == "mov" and y.op_str.startswith(reg + ", qword ptr [rip"):
            g = y.address + y.size + y.operands[1].mem.disp; break
        if y.op_str.startswith(reg + ",") or y.op_str.startswith(reg.replace("r", "e", 1) + ","):
            break
    if g is None:
        nonstatic += 1
        # second form: `lea rX, [rip -> G]` ... `mov reg, qword ptr [rX]` (the static object's vtable read through its address)
        for j in range(len(prev) - 1, max(-1, len(prev) - 9), -1):
            y = prev[j]
            m = re.fullmatch(reg + r", qword ptr \[(\w+)\]", y.op_str) if y.mnemonic == "mov" else None
            if m:
                for z in reversed(prev[max(0, j - 8):j]):
                    if z.mnemonic == "lea" and z.op_str.startswith(m.group(1) + ", [rip"):
                        leaform[z.address + z.size + z.operands[1].mem.disp].append(a)
                        break
                break
        continue
    vt = static_vt(g)
    try: cn = T.rtti_class(vt) if vt else None
    except Exception: cn = None
    if cn is None:
        unknown[g] += 1; continue
    if "PClassDescriptor" in cn:
        per_fn[o].append((a, x.mnemonic, g, cn))
print("sites whose register is not loaded from a static within 8 instructions:", nonstatic)
print("  of those, vtable read through `lea rX, [static]` (second form): %d sites, statics %s"
      % (sum(len(v) for v in leaform.values()), ["%08X (%s) x%d" % (g, tk.sec_of(g), len(v)) for g, v in sorted(leaform.items())]))
print("statics with no vtable found (unclassified): %d statics, %d sites" % (len(unknown), sum(unknown.values())))
for g, n in unknown.most_common(8): print("   %08X x%d  (in .%s)" % (g, n, tk.sec_of(g)))
tot = 0
for o in sorted(per_fn, key=lambda v: v or 0):
    v = per_fn[o]; tot += len(v)
    print("  %s  %2d sites (%s) via [%08X] %s%s" % (tk.fname(v[0][0]), len(v), ",".join(sorted(set(m for _, m, _, _ in v))),
          v[0][2], v[0][3], "  ROUTE" if o in ROUTES else ""))
print("PClassDescriptor static sites: %d in %d bodies" % (tot, len(per_fn)))
