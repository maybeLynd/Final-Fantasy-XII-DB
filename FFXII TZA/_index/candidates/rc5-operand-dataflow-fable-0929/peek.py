# peek.py - print the bytecode around every POPV / PUSHV of one file variable (dataflow reading aid, FABLE 2026-09-29).
# usage: python peek.py <ebp name substring> <descriptor offset hex>
import os, sys, struct
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
f = open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
path = next(p for p in sorted(names) if sys.argv[1] in p and p.lower().endswith(".ebp") and "/us/" in p.lower())
off = int(sys.argv[2], 16)
b = G.V.read_entry(f, names, blocks, path)
sec = b[0x80:0x80 + U32(b, 0x84)]
vt = U32(sec, 0x28); pool = U32(sec, 0x20)
diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
starts = sorted(set(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)))
bounds = sorted(set(starts) | {diroff, len(sec)})
print(path)
for st in starts:
    end = min((x for x in bounds if x > st), default=len(sec))
    ins, _ = G.decode(sec[st:end])
    for j, (pc, op, imm) in enumerate(ins):
        if op in (0x48, 0x49, 0x4B) and (U32(sec, vt + imm * 8 + 4) & 0xFFFFFF) == off and ((U32(sec, vt + imm * 8 + 4) >> 24) & 7) == 1:
            lo, hi = max(0, j - 4), min(len(ins), j + 5)
            txt = []
            for k in range(lo, hi):
                p2, o2, i2 = ins[k]
                n = G.OPN.get(o2, hex(o2))
                if n == "PUSHI":
                    n += "(%d)" % S32(sec, pool + i2 * 4 + 4)
                elif o2 >= 0x48:
                    n += "(%d)" % i2
                txt.append(("*" if k == j else "") + n)
            print("  %06X  %s" % (st + pc, " ".join(txt)))
