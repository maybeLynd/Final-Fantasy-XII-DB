"""HM-1 (OPUS, 2026-09-27): the order of Fran's c:3 bindp-family call and C:22 bindh call, in the one script of each of
the four maps that makes both (see c22_bind.py for the argument route: PUSHI through the int pool, 0x3000000 + k
through EBP section 12).
  O1 in every map the c:3 bind precedes the C:22 bindh in the script's code
  O2 gol_a0200 and hne_b0102: no jump and no return lies between them - one straight run, so the bind runs first
  O3 dgl_g0102 and rsn_z0200: returns lie between them - the two calls are in different functions of the script, so
     their run-time order is the scene's call order, which this control does not read
Not claimed: the call order in dgl_g0102 / rsn_z0200, or what is drawn."""
import io, os, sys, struct
DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
MAPS = ["dgl_g/dgl_g0102/dgl_g0102", "gol_a/gol_a0200/gol_a0200", "hne_b/hne_b0102/hne_b0102", "rsn_z/rsn_z0200/rsn_z0200"]
verbs = G.load_verbs()
f = io.open(G.VBF, "rb"); names, blocks = G.V.load_index(f); RES = {}
for m in MAPS:
    b = G.V.read_entry(f, names, blocks, "ps2data/plan_master/us/event/%s.ebp" % m)
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); n = U32(sec, diroff)
    starts = sorted({struct.unpack_from("<IHHII", sec, diroff + 4 + si * 0x30)[3] for si in range(n)})
    bounds = sorted(set(starts) | {diroff, len(sec)})

    def val(a):
        if a[0] == "PUSHI":
            v = U32(sec, U32(sec, 0x20) + 4 + int(a[1]) * 4)
            if v >= 0x1000000:
                mo = U32(b, 0x40); k = v & 0xFFFFFF
                v = U32(b, mo + 4 + 4 * k) if k < U32(b, mo) else 0
            return "%s:%d" % (chr(v >> 16), v & 0xFFFF) if 0x41 <= (v >> 16) <= 0x7A else hex(v)
        return "%s:%s" % (a[0], a[1])
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        ins, _ = G.decode(sec[start:end])
        marks = []
        for j, (pc, op, imm) in enumerate(ins):
            if op not in (0x58, 0x59, 0x5D, 0x5E) or imm not in verbs: continue
            nm = str(verbs[imm][2])
            if not (nm.startswith("bindp") or nm == "bindh"): continue
            v = verbs[imm]; need = (v[0] if v[0] is not None else 1) + (1 if op in (0x59, 0x5E) else 0)
            args, st = G.resolve_args(ins, j, need, verbs)
            marks.append((pc, nm, ";".join(val(a) for a in args) if args else ""))
        tgt = [(pc, nm) for pc, nm, a in marks
               if (a.split(";")[0] == "c:3" and nm.startswith("bindp")) or (a.split(";")[0] == "C:22" and nm == "bindh")]
        if len({nm == "bindh" for pc, nm in tgt}) < 2: continue
        first = min(pc for pc, nm in tgt if nm != "bindh"); hb = min(pc for pc, nm in tgt if nm == "bindh")
        lo, hi = min(first, hb), max(first, hb)
        jumps = [pc for pc, op, imm in ins if op in G.JMP_OPS and lo < pc < hi]
        rets = [pc for pc, op, imm in ins if 0x2D <= op <= 0x31 and lo < pc < hi]
        RES[m.split("/")[-1]] = (first < hb, bool(jumps), bool(rets))
        print("%-10s script @%X  c:3 bind pc %X  C:22 bindh pc %X  jumps between %d  returns between %d"
              % (m.split("/")[-1], start, first, hb, len(jumps), len(rets)))
fails = 0
def check(nm, ok, d=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, d)); fails += not ok
check("O1 the c:3 bind precedes the C:22 bindh in all four", len(RES) == 4 and all(v[0] for v in RES.values()))
check("O2 gol_a0200 / hne_b0102: one straight run", all(k in RES and not RES[k][1] and not RES[k][2] for k in ("gol_a0200", "hne_b0102")))
check("O3 dgl_g0102 / rsn_z0200: returns between them - different functions", all(k in RES and RES[k][2] for k in ("dgl_g0102", "rsn_z0200")))
print("FAILS", fails); sys.exit(1 if fails else 0)
