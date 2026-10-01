# HM-1 (OPUS, 2026-09-27): in the four maps whose manifest loads hc1006_03 (C:22), list every call of a
# bind-family script verb (the verbs whose handlers reach 002E3110) with its resolved arguments and owning script.
# Reuses the decoder of attach_census.py / c22_scripts.py; PUSHI operands are resolved through the int constant pool. Control: a map with no decoded CALL-family site refuses.
import io, os, sys, struct
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
MAPS = sys.argv[1:] or ["dgl_g/dgl_g0102/dgl_g0102", "gol_a/gol_a0200/gol_a0200", "hne_b/hne_b0102/hne_b0102", "rsn_z/rsn_z0200/rsn_z0200"]
verbs = G.load_verbs()
WANT = {k: v[2] for k, v in verbs.items() if "bind" in str(v[2]) and not str(v[2]).startswith("debug")}
WANT[0xD9] = "attach"
f = io.open(G.VBF, "rb"); names, blocks = G.V.load_index(f); SUMMARY = {}
def cstr(b, o): return b[o:b.index(b"\0", o)].decode("cp932", "replace")
for m in MAPS:
    path = "ps2data/plan_master/us/event/%s.ebp" % m
    b = G.V.read_entry(f, names, blocks, path)
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff, nm = U32(sec, 0x18), U32(sec, 0x4C); n = U32(sec, diroff)
    ents = []
    for si in range(n):
        e = diroff + 4 + si * 0x30
        nameOff, stype, pcid, start, ninstr = struct.unpack_from("<IHHII", sec, e)
        ents.append((start, si, cstr(sec, nm + nameOff) if nm else str(si), stype))
    starts = sorted(e[0] for e in ents); bounds = sorted(set(starts) | {diroff, len(sec)})
    calls, hits = 0, []
    for start in sorted(set(starts)):
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        ins, _ = G.decode(sec[start:end])
        for j, (pc, op, imm) in enumerate(ins):
            if op not in (0x58, 0x59, 0x5D, 0x5E): continue
            calls += 1
            if imm not in WANT: continue
            v = verbs.get(imm)
            need = (v[0] if v and v[0] is not None else 1) + (1 if op in (0x59, 0x5E) else 0)
            args, st = G.resolve_args(ins, j, need, verbs)
            owner = max((e for e in ents if e[0] <= start + pc), default=None)
            def val(a):  # PUSHI (0x4E) reads the int constant pool, [pool + operand*4 + 4] (section-000-bytecode.md); PUSHII is immediate
                if a[0] == "PUSHI":
                    v = U32(sec, U32(sec, 0x20) + 4 + int(a[1]) * 4)
                    if v >= 0x1000000:  # 002E9A60 -> 00263F80: [ctx+0x100] = EBP section 12 (file +0x40), {count; u32 id[count]}, index v & 0xFFFFFF
                        mo = U32(b, 0x40); k = v & 0xFFFFFF
                        v = U32(b, mo + 4 + 4 * k) if k < U32(b, mo) else 0
                        return "PUSHI:%d=m[%d]=%s:%d" % (int(a[1]), k, chr(v >> 16), v & 0xFFFF)
                    return "PUSHI:%d=%s" % (int(a[1]), ("%s:%d" % (chr(v >> 16), v & 0xFFFF)) if 0x41 <= (v >> 16) <= 0x7A else hex(v))
                return "%s:%s" % (a[0], a[1])
            hits.append((start + pc, WANT[imm], G.OPN.get(op), st, ";".join(val(a) for a in args) if args else "", owner))
    if calls == 0: sys.exit("REFUSE: no CALL-family site decoded in " + m)
    print("==", m, "| scripts", n, "| CALL-family sites", calls, "| bind-family", len(hits))
    for pc, name, opn, st, args, o in hits:
        print("   %-12s pc %5x %-6s %-8s args %-28s script #%s '%s' type %s" % (name, pc, opn, st, args, o[1], o[2], o[3]))
    c3 = [(name, o[2]) for pc, name, opn, st, args, o in hits if "=c:3" in args]
    SUMMARY[m] = sorted(set(c3))
# Assertion (HM-1 body bind): in each map every bind of c:3 (c1006) is a bindp-family verb - the route through the
# replacement poll 003409F0 - and all of them come from one script.
bad = 0
for m, c3 in SUMMARY.items():
    ok = bool(c3) and all(v.startswith("bindp") for v, _ in c3) and len({s for _, s in c3}) == 1
    print("%s c:3 binds in %s: %s" % ("PASS" if ok else "FAIL", m.split("/")[-1], c3)); bad += not ok
print("FAILS", bad); sys.exit(1 if bad else 0)
