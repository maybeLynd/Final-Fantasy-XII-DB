"""G-5's two residues (OPUS, 2026-09-27): no authored command sequence can drive a Magi mode change in this build, and
the 4.0 that Audio_SetMode passes to Music::SyncTo is seconds.

  Q1 007EEA00, SEAD's command-sequence interpreter, posts the Magi commands from its opcode arms: 0x100 -> 007A9550 (0x1D),
     0x101 -> 007A94D0 (0x21 SetMode), 0x102 -> 007A95D0 (0x27 Start), 0x103 -> 007A90E0 (0x28 End)
     (007EECB6 sub ecx, 0x101 / je 007EED53; sub ecx, 1 / je 007EED0C; cmp ecx, 1 -> 007EECD0).
  Q2 the interpreter's objects are allocated only by 007EE910, called only at 007B65C3 in 007B6350; their stream is
     installed by 007EE990, called only at 007B65EE in the same function; 007EEA00 is called only by the tick 007B6B00 and
     by 007EE990. 007B6350 resolves a sequence BY
     NAME in the 257-bucket table at 01F41460, and it is called only by the command drain 007AB5C0, from its arm for
     driver command 0x33 (the drain's jump table at 007AC080).
  Q3 nothing posts command 0x33: every one of the 34 queue-allocation sites (call 007AB460) stores an immediate command id
     into the element, none computes one, and 0x33 is not among the 33 distinct ids. POSITIVE CONTROL: 0x21, 0x26, 0x27
     and 0x28 are among them.
  Q4 the 4.0 is seconds: Music::SyncTo (007CAB80) adds samples / [this + 0x64C] to it (007CAE3D..007CAE4B) and scales
     (it + 0.2) by [this + 0x64C] into a sample count (007CACBF..007CACD4); 007C6FB0 loads +0x64C from the music record's
     +0x44 when its version is 6 or more (007C6FF7..007C7015); all 116 shipped music records (.mab 'musc' chunk) are
     version 11 with +0x44 = 48,000 - a sample rate.
Not claimed: which data registers named sequences in 01F41460 (007B67E0), or what they contain - none can start.
Usage: python g5_sequences_and_sync.py [exe] [functions.tsv] [mab dir]
"""
import glob, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = sys.argv[1] if len(sys.argv) > 1 else "Tools/work/exe/FFXII_TZA.exe"
FUN = sys.argv[2] if len(sys.argv) > 2 else "Tools/work/graph/functions.tsv"
MAB = sys.argv[3] if len(sys.argv) > 3 else r"D:/FFXII_TZA_extract/ps2data/sound/music/magi_data/win"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(nsec)]
off = lambda v: next((v - BASE - va + ro for vs, va, rs, ro in secs if BASE + va <= v < BASE + va + rs), None)
sizes = {}
for l in open(FUN, encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
dis = lambda f: [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + sizes[f]], f)]
fails = 0


def check(name, ok, det=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, det)); fails += not ok


def rel_callers(target):
    out = []
    text = [s for s in secs if s[1] == 0x1000][0]; blob = d[text[3]:text[3] + text[2]]; tb = BASE + text[1]
    for i in range(len(blob) - 5):
        if blob[i] in (0xE8, 0xE9) and tb + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == target: out.append(tb + i)
    return out


I = {a: (m, o) for a, m, o in dis(0x7EEA00)}
q1 = I.get(0x7EECB6) == ("sub", "ecx, 0x101") and I.get(0x7EECBC) == ("je", "0x7eed53") and I.get(0x7EECC2) == ("sub", "ecx, 1") \
     and I.get(0x7EECC5) == ("je", "0x7eed0c") and I.get(0x7EECC7) == ("cmp", "ecx, 1") \
     and I.get(0x7EED79) == ("call", "0x7a94d0") and I.get(0x7EED3D) == ("call", "0x7a95d0") and I.get(0x7EECF6) == ("call", "0x7a90e0") \
     and I.get(0x7EEC8E) == ("call", "0x7a9550")
posted = {}
for f in (0x7A94D0, 0x7A95D0, 0x7A90E0, 0x7A9550):
    posted[f] = [int(o.split(", ")[1], 0) for a, m, o in dis(f) if m == "mov" and o.startswith("dword ptr [rax], ")]
q1 &= posted == {0x7A94D0: [0x21], 0x7A95D0: [0x27], 0x7A90E0: [0x28], 0x7A9550: [0x1D]}
check("Q1 opcodes 0x100-0x103 post 0x1D / 0x21 / 0x27 / 0x28", q1)

tab = BASE + 0x68C080
arm33 = struct.unpack_from("<I", d, off(tab) + 4 * 0x33)[0] + BASE
D = {a: (m, o) for a, m, o in dis(0x7AB5C0)}
q2 = rel_callers(0x7EE990) == [0x7B65EE] and rel_callers(0x7B6350) == [0x7ABF80] and arm33 == 0x7ABF7C \
     and rel_callers(0x7EE910) == [0x7B65C3] and sorted(rel_callers(0x7EEA00)) == [0x7B6B7C, 0x7EE9DD] \
     and D.get(0x7AB674) == ("cmp", "eax, 0x35") and D.get(0x7ABF80) == ("call", "0x7b6350") \
     and d.find(struct.pack("<Q", 0x7B6350)) == -1 and d.find(struct.pack("<Q", 0x7EE990)) == -1
check("Q2 streams reach 007EEA00 only via command 0x33's arm", q2, "(arm 0x33 = %08X)" % arm33)

ids, regs = [], []
bisect_keys = sorted(sizes)
import bisect
for a in rel_callers(0x7AB460):
    f = bisect_keys[bisect.bisect_right(bisect_keys, a) - 1]
    xs = dis(f); k = next(i for i, x in enumerate(xs) if x[0] == a)
    for y in xs[k + 1:k + 14]:
        m = re.match(r"dword ptr \[r\w+\], (.+)$", y[2])
        if y[1] == "mov" and m:
            try: ids.append(int(m.group(1), 0))
            except ValueError: regs.append(y[0])
            break
check("Q3 no site posts 0x33", len(ids) == 34 and not regs and 0x33 not in ids and {0x21, 0x26, 0x27, 0x28} <= set(ids),
      "(%d sites, %d distinct ids)" % (len(ids), len(set(ids))))

S = {a: (m, o) for a, m, o in dis(0x7CAB80)}
Mw = {a: (m, o) for a, m, o in dis(0x7C6FB0)}
q4 = S.get(0x7CAE1D) == ("movd", "xmm1, dword ptr [rsi + 0x64c]") and S.get(0x7CAE47) == ("divss", "xmm0, xmm1") \
     and S.get(0x7CAE4B) == ("addss", "xmm6, xmm0") and S.get(0x7CACD0) == ("mulss", "xmm1, xmm0") \
     and Mw.get(0x7C6FF7) == ("cmp", "byte ptr [rax], 6") and Mw.get(0x7C6FFC) == ("mov", "ecx, dword ptr [rax + 0x44]") \
     and Mw.get(0x7C7015) == ("mov", "dword ptr [rbx + 0x64c], ecx") \
     and abs(struct.unpack_from("<f", d, off(0x7CACCD + 0x12842B))[0] - 0.2) < 1e-6
recs = []
for fn in glob.glob(os.path.join(MAB, "*.mab")):
    b = open(fn, "rb").read()
    if b[:4] != b"mabf": continue
    o = next((struct.unpack_from("<I", b, 0x20 + i * 0x10 + 8)[0] for i in range(8) if b[0x20 + i * 0x10:0x24 + i * 0x10] == b"musc"), None)
    if o is None: continue
    for k in range(struct.unpack_from("<I", b, o + 4)[0]):
        r = o + struct.unpack_from("<I", b, o + 0x10 + 4 * k)[0]
        recs.append((b[r], struct.unpack_from("<I", b, r + 0x44)[0]))
q4 &= len(recs) == 116 and all(v == 11 and rate == 48000 for v, rate in recs)
check("Q4 the 4.0 is seconds (+0x64C = the record's 48,000 sample rate)", q4, "(%d music records)" % len(recs))
print("FAILS", fails); sys.exit(1 if fails else 0)
