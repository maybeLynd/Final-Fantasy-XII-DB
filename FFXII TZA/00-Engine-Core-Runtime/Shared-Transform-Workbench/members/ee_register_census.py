"""ee_register_census.py - every function that addresses the emulated PS2 EE / VU0 register bank, and which registers it uses.

Map (FABLE 2026-09-14, the-ee-and-vu0-register-bank.md):
  022D8F10 + 16*k   GPR[k], k = 0..31, 16 bytes each (128-bit EE register image); GPR[0] is $zero
  022D9110 / 022D9120   HI / LO (16 bytes each)
  022D9130          VU CLIP flag word (shl 6 | six comparison bits)
  022D9198          VU Q
  022D91A0          VU ACC
  022D91A0 + 16*k   VU vf[k], k = 1..31
  01EF93F0          VU vf00, the constant (0, 0, 0, 1) - written only by the bank clear 0036D9E0
Every rip-relative operand into those ranges is counted as a read, a write (first operand of a storing / arithmetic
mnemonic) or an address (lea). Also reports, per function, a few MMI-shaped mnemonics (16-bit SIMD work).

Inputs: the shipping exe, the function list, the ARCH / C frontier lists of the FABLE instruments, and the database
pages (for "cited"). Output: ee-register-census.tsv beside this script, and a summary on stdout."""
import os, re, struct, collections, glob
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 5))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
FRONT = [os.path.join(REPO, "Database", "Tools", "work", "FABLE", "pub140-scratch", f) for f in ("arch_frontier.txt", "c_frontier.txt")]
DB = os.path.join(REPO, "Database", "FFXII TZA")
BASE = 0x120000
GPR0, HI, LO, CLIP, Q, ACC, VF00 = 0x022D8F10, 0x022D9110, 0x022D9120, 0x022D9130, 0x022D9198, 0x022D91A0, 0x01EF93F0
GPRNAMES = "zero at v0 v1 a0 a1 a2 a3 t0 t1 t2 t3 t4 t5 t6 t7 s0 s1 s2 s3 s4 s5 s6 s7 t8 t9 k0 k1 gp sp fp ra".split()
def classify(t):
    if GPR0 <= t < GPR0 + 32 * 16: return "gpr:" + GPRNAMES[(t - GPR0) // 16]
    if HI <= t < HI + 16: return "HI"
    if LO <= t < LO + 16: return "LO"
    if CLIP <= t < CLIP + 4: return "CLIP"
    if Q <= t < Q + 4: return "Q"
    if ACC <= t < ACC + 16: return "ACC"
    if ACC + 16 <= t < ACC + 32 * 16: return "vf%02d" % ((t - ACC) // 16)
    if VF00 <= t < VF00 + 16: return "vf00"
    return None
READONLY = {"cmp", "test", "comiss", "ucomiss", "bt", "push", "lea"}
MMI = {"psrldq", "pslldq", "pextrw", "pinsrw", "pmullw", "pmulhw", "paddsw", "psubsw", "pminsw", "pmaxsw", "psrlw", "psllw", "psraw", "packsswb", "packuswb", "punpcklbw", "punpcklwd"}
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0], struct.unpack_from("<I", d, o + 20)[0]))
_, tva, tvs, tro = [s for s in secs if s[0] == ".text"][0]
sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
front = {}
for tag, f in zip("AC", FRONT):
    for l in open(f):
        if l.strip(): front[int(l.split()[0], 16)] = tag
cited = set()
for p in glob.glob(os.path.join(DB, "**", "*.md"), recursive=True):
    if os.path.basename(p) in ("ADDRESS-INDEX.md", "AUDIT-LOG.md"): continue
    cited.update(m.upper() for m in re.findall(r"\b0[0-9A-Fa-f]{7}\b", open(p, encoding="utf-8", errors="replace").read()))
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
rows = []
role = collections.defaultdict(lambda: [set(), set()])      # register -> [reader fns, writer fns]
for e in sorted(sizes):
    o = tro + (e - BASE - tva)
    if o < tro or e - BASE + sizes[e] > tva + tvs: continue
    use = collections.defaultdict(lambda: [0, 0, 0]); mmi = 0
    for x in md.disasm(d[o:o + sizes[e]], e):
        if x.mnemonic in MMI: mmi += 1
        for k, op in enumerate(x.operands):
            if op.type == X86_OP_MEM and op.mem.base and x.reg_name(op.mem.base) == "rip":
                c = classify(x.address + x.size + op.mem.disp)
                if not c: continue
                if x.mnemonic == "lea": use[c][2] += 1
                elif k == 0 and x.mnemonic not in READONLY and len(x.operands) > 1: use[c][1] += 1
                else: use[c][0] += 1
    if not use: continue
    for c, (r, w, a) in use.items():
        if r or a: role[c][0].add(e)
        if w: role[c][1].add(e)
    gpr = sorted(c[4:] for c in use if c.startswith("gpr:"))
    vf = sorted(c for c in use if c.startswith("vf") and c != "vf00")
    rows.append((e, names.get(e, ""), sizes[e], front.get(e, "-"), "yes" if "%08X" % e in cited else "no",
                 " ".join(gpr) or "-", " ".join(c for c in ("HI", "LO", "CLIP", "Q", "ACC", "vf00") if c in use) or "-",
                 len(vf), sum(u[1] for u in use.values()), sum(u[0] for u in use.values()), mmi))
with open(os.path.join(HERE, "ee-register-census.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("function\tname\tsize\tfrontier\tcited\tgpr_registers\tvu_and_multiply_registers\tvf_rows\twrites\treads\tmmi_mnemonics\n")
    for r in rows: f.write("%08X\t%s\t%d\t%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d\n" % r)
print("functions addressing the bank:", len(rows), "| frontier A/C:", sum(1 for r in rows if r[3] == "A"), "/", sum(1 for r in rows if r[3] == "C"),
      "| cited:", sum(1 for r in rows if r[4] == "yes"), "| bytes:", sum(r[2] for r in rows))
print("using GPRs:", sum(1 for r in rows if r[5] != "-"), "| using VU rows / ACC / Q / CLIP:", sum(1 for r in rows if r[7] or any(c in r[6] for c in ("ACC", "Q", "CLIP"))),
      "| both:", sum(1 for r in rows if r[5] != "-" and (r[7] or any(c in r[6] for c in ("ACC", "Q", "CLIP")))))
print("register        readers writers")
order = ["gpr:" + n for n in GPRNAMES] + ["HI", "LO", "CLIP", "Q", "ACC"] + ["vf%02d" % k for k in range(1, 32)] + ["vf00"]
for c in order:
    if c in role: print("  %-12s %5d %5d%s" % (c, len(role[c][0]), len(role[c][1]), "   writers: " + " ".join("%08X" % w for w in sorted(role[c][1])) if c in ("gpr:zero", "vf00") else ""))
