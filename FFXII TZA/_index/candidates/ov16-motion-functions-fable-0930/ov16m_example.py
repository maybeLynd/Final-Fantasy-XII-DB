"""ov16m_example.py - dump the one waiting slot-17 function the census found (asp_a03, actor 25, function 7 talkterm,
US copy) instruction by instruction, with the REQEW operands resolved (resolve_args need=3: channel, actor, function),
and name the target function in the target actor's own table. Also prints the actor's scriptType (entry +0x04) and
every function name of actor 25, and the census's own counts for that actor's REQCHG / reqenable sites are left to
ov16m_census.out. Read-only."""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G  # noqa: E402

P = "D:/FFXII_TZA_extract/ps2data/plan_master/us/plan_map/asp_a/asp_a03/global/asp_a03.ebp"
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
b = open(P, "rb").read()
sec = b[0x80:0x80 + U32(b, 0x84)]
diroff, pool = U32(sec, 0x18), U32(sec, 0x4C)
cnt = U32(sec, diroff)
cs = lambda o: sec[o:sec.find(b"\0", o)].decode("cp932", "replace")
ents = [diroff + 4 + a * 0x30 for a in range(cnt)]
starts = sorted(set(U32(sec, e + 8) for e in ents))
bounds = sorted(set(starts) | {diroff, len(sec)})


def actor(ai):
    e = ents[ai]
    start = U32(sec, e + 8)
    end = min(x for x in bounds if x > start)
    ft = U32(sec, e + 0x10)
    nf = U32(sec, ft)
    fn = [(cs(pool + U32(sec, ft + 4 + 8 * i)), U32(sec, ft + 8 + 8 * i)) for i in range(nf)]
    sepa = U32(sec, e + 0x18)
    special = [U16(sec, sepa + 2 + 2 * k) for k in range(U16(sec, sepa))]
    return cs(pool + U32(sec, e)), U16(sec, e + 4), start, end, fn, special


verbs = G.load_verbs()
name, stype, start, end, fns, special = actor(25)
print("actor 25 %s scriptType %d code [%x,%x) functions %s" % (name, stype, start, end, [f[0] for f in fns]))
print("footer special[16]=%d special[17]=%d" % (special[16], special[17]))
offs = sorted(set(o for _, o in fns))
o = fns[7][1]
nxt = min((x for x in offs if x > o), default=end - start)
ins, _ = G.decode(sec[start + o:start + nxt])
print("function 7 %s at +%x, %d bytes:" % (fns[7][0], o, nxt - o))
for j, (pc, op, imm) in enumerate(ins):
    extra = ""
    if op in (0x24, 0x27):
        args, st = G.resolve_args(ins, j, 3, verbs)
        extra = "   <- %s %s" % (st, args)
        if st == "ok" and args[1][0] == "PUSHII" and args[2][0] == "PUSHII":
            tn, tt, _s, _e, tf, _sp = actor(args[1][1])
            extra += "  = channel %s, actor %d %s (scriptType %d), function %d %s" % (
                args[0][1] if args[0][0] == "PUSHII" else args[0][0], args[1][1], tn, tt, args[2][1], tf[args[2][1]][0])
    elif op in (0x58, 0x59, 0x5D, 0x5E):
        extra = "   verb %s" % (verbs.get(imm, (None, None, "?"))[2])
    print("  %04x  %-10s %s%s" % (pc, G.OPN.get(op, hex(op)), "" if imm is None else hex(imm), extra))
