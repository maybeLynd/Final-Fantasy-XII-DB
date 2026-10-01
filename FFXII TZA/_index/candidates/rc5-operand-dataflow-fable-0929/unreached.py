# unreached.py - why a site is not reached from any function entry (FABLE 2026-09-29): prints its script, the function
# entries, the jump-table offsets, and the instructions before the site.   usage: python unreached.py <ebp substr> <pc hex>
import os, sys, struct
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
f = open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
path = next(p for p in sorted(names) if sys.argv[1] in p and p.lower().endswith(".ebp") and ("/us/" in p.lower() or "/in/" in p.lower()))
target = int(sys.argv[2], 16)
b = G.V.read_entry(f, names, blocks, path)
sec = b[0x80:0x80 + U32(b, 0x84)]
diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
ents = [diroff + 4 + s * 0x30 for s in range(cnt)]
starts = sorted(set(U32(sec, e + 8) for e in ents))
bounds = sorted(set(starts) | {diroff, len(sec)})
for e in ents:
    st = U32(sec, e + 8)
    end = min((x for x in bounds if x > st), default=len(sec))
    if not (st <= target < end):
        continue
    ins, _ = G.decode(sec[st:end])
    fo = U32(sec, e + 0x10); fcount = U32(sec, fo)
    fentry = [U32(sec, fo + 4 + i * 8 + 4) for i in range(fcount)]
    jo = U32(sec, e + 0x14); jcount = U32(sec, jo)
    jt = [U32(sec, jo + 4 + i * 4) for i in range(jcount)]
    print(path, "script start %X end %X" % (st, end), "functions", ["%X" % x for x in fentry])
    print("jump table (%d):" % jcount, ["%X" % x for x in jt][:60])
    rel = target - st
    idx = [j for j, (pc, op, imm) in enumerate(ins) if pc == rel][0]
    for j in range(max(0, idx - 25), min(len(ins), idx + 3)):
        pc, op, imm = ins[j]
        print("  %s%06X %-12s %s" % ("*" if j == idx else " ", pc, G.OPN.get(op, hex(op)), "" if imm is None else imm))
