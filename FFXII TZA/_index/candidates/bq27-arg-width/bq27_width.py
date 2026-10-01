"""bq27_width.py - BQ-27 narrowed by the width of the second argument (FABLE, Claude Opus 5.5, 2026-09-27).

OPUS (2026-09-14) settled 262 of the 607 slot-7 / slot-0 indirect call sites by their literal flag and left 345 whose
flag is computed. A deleting destructor's flag is an `unsigned int`, passed in edx. At each site, the instruction that
last writes the rdx family in the call's block sets the second argument:
  W1  population: every `call qword ptr [reg + 0x38]` (slot 7) and `call qword ptr [reg]` (slot 0) in the listed bodies
      - reproduces OPUS's 172 + 435 = 607
  W2  literal flags: none has bit 0 and bit 2 both set (OPUS's negative, reproduced)
  W3  control for the width rule: every literal flag is written as a 32-bit `edx` (never `rdx`), and 32-bit register
      copies into edx occur too - the compiler writes a 32-bit argument through the 32-bit register
  W4  sites whose last write is to the full 64-bit rdx (a qword load, an address `lea`, a 64-bit copy or arithmetic):
      the slot's method takes a pointer-sized second parameter at that site, so it is not a deleting destructor
  W5  the rest - a 32-bit computed write, or no write in the block - are the residue, listed per site in the TSV
Writes bq27-sites.tsv. Reads the capstone listing (Y1P_CACHE).
"""
import os, re, sys, collections
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
HERE = os.path.dirname(os.path.abspath(__file__))
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
body = collections.defaultdict(list)
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3: body[p[1]].append((p[0], p[2]))
S7 = re.compile(r"^call qword ptr \[(r\w+) \+ 0x38\]$"); S0 = re.compile(r"^call qword ptr \[(r\w+)\]$")
FAM = {}
for q, d, w, b in (("rax", "eax", "ax", "al"), ("rbx", "ebx", "bx", "bl"), ("rcx", "ecx", "cx", "cl"), ("rdx", "edx", "dx", "dl"),
                   ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"), ("rbp", "ebp", "bp", "bpl")):
    for n in (q, d, w, b): FAM[n] = q
for k in range(8, 16):
    for n in ("r%d" % k, "r%dd" % k, "r%dw" % k, "r%db" % k): FAM[n] = "r%d" % k
fam = lambda x: FAM.get(x.strip())
BOUND = re.compile(r"^(call|jmp|ret|j[a-z]+)\b"); NOWRITE = ("test", "cmp", "push", "bt")
IMM = re.compile(r"-?(0x[0-9a-f]+|\d+)")
def last_write(ins, i, reg):
    for k in range(i - 1, -1, -1):
        a, s = ins[k]
        if BOUND.match(s): return None
        mn, ops = (s.split(None, 1) + [""])[:2]; parts = [x.strip() for x in ops.split(";")[0].split(",")]
        if mn not in NOWRITE and parts and fam(parts[0]) == reg and "[" not in parts[0]: return k
    return None
def literal(ins, i, reg, depth=0):
    k = last_write(ins, i, reg)
    if k is None: return None
    mn, ops = (ins[k][1].split(None, 1) + [""])[:2]; parts = [x.strip() for x in ops.split(";")[0].split(",")]
    src = parts[1] if len(parts) > 1 else ""
    if mn == "xor" and fam(src) == reg: return (0, parts[0])
    if mn == "mov" and IMM.fullmatch(src): return (int(src, 0) & 0xFFFFFFFF, parts[0])
    if mn in ("mov", "movzx", "movsxd", "movsx") and fam(src) and depth < 4: return literal(ins, k, fam(src), depth + 1)
    return None
rows = []; n7 = n0 = 0
for f in sorted(body):
    ins = sorted(body[f])
    for i, (a, s) in enumerate(ins):
        slot = 7 if S7.match(s) else 0 if S0.match(s) else None
        if slot is None: continue
        n7 += slot == 7; n0 += slot == 0
        lit = literal(ins, i, "rdx"); k = last_write(ins, i, "rdx")
        w = ins[k][1] if k is not None else "-"
        dst = [x.strip() for x in (w.split(None, 1) + [""])[1].split(",")][0] if k is not None else "-"
        if lit is not None: cls = "literal-both" if (lit[0] & 5) == 5 else "literal"
        elif dst == "rdx": cls = "64-bit-arg"
        elif dst in ("edx", "dx", "dl"): cls = "residue-32bit-computed"
        else: cls = "residue-no-write-in-block"
        rows.append((f, a, slot, cls, "%#x" % lit[0] if lit else "-", lit[1] if lit else dst, w))
c = collections.Counter(r[3] for r in rows)
ok("W1", (n7, n0) == (172, 435), "slot 7: %d, slot 0: %d" % (n7, n0))
ok("W2", c["literal-both"] == 0, "literal flags: %d, with bits 0 and 2 both set: %d" % (c["literal"], c["literal-both"]))
lit_dst = collections.Counter(r[5] for r in rows if r[3].startswith("literal"))
copies32 = sum(1 for r in rows if r[3] == "residue-32bit-computed" and re.match(r"mov edx, e", r[6]))
ok("W3", set(lit_dst) == {"edx"} and copies32 > 0, "literal flags written as %s; 32-bit register copies into edx: %d" % (dict(lit_dst), copies32))
k64 = collections.Counter(("qword load" if "qword ptr" in r[6] else "lea" if r[6].startswith("lea") else "64-bit copy" if re.match(r"mov rdx, r", r[6]) else "64-bit arithmetic") for r in rows if r[3] == "64-bit-arg")
ok("W4", c["64-bit-arg"] > 0, "%d sites set a pointer-sized second argument: %s" % (c["64-bit-arg"], dict(k64)))
res = c["residue-32bit-computed"] + c["residue-no-write-in-block"]
ok("W5", c["literal"] + c["64-bit-arg"] + res == len(rows) == 607,
   "settled %d (literal %d + 64-bit %d); residue %d (32-bit computed %d, no write in the block %d)"
   % (c["literal"] + c["64-bit-arg"], c["literal"], c["64-bit-arg"], res, c["residue-32bit-computed"], c["residue-no-write-in-block"]))
# ---- F: reaching definitions of rdx over each function's CFG (calls clobber rdx; entry = the incoming argument) ----
def flow(f, site_hex):
    ins = sorted((int(a, 16), s) for a, s in body[f]); idx = {a: i for i, (a, s) in enumerate(ins)}
    preds = collections.defaultdict(set)
    for i, (a, s) in enumerate(ins):
        mn = s.split()[0]; m = re.match(r"j\w+ 0x([0-9a-f]+)$", s)
        if m and int(m.group(1), 16) in idx: preds[idx[int(m.group(1), 16)]].add(i)
        if mn not in ("jmp", "ret") and i + 1 < len(ins): preds[i + 1].add(i)
    site = idx[int(site_hex, 16)]; defs = set(); seen = set(); stack = list(preds[site])
    if not stack: defs.add(("entry" if site == 0 else "unknown-pred", 0))
    while stack:
        k = stack.pop()
        if k in seen: continue
        seen.add(k); s = ins[k][1]; mn, ops = (s.split(None, 1) + [""])[:2]
        parts = [x.strip() for x in ops.split(";")[0].split(",")]
        if s.startswith("call"): defs.add(("call-clobber", 0)); continue
        if mn not in NOWRITE and parts and fam(parts[0]) == "rdx" and "[" not in parts[0]:
            src = parts[1] if len(parts) > 1 else ""
            if mn == "xor" and fam(src) == "rdx": defs.add(("lit", 0))
            elif mn == "mov" and IMM.fullmatch(src): defs.add(("lit", int(src, 0) & 0xFFFFFFFF))
            else: defs.add(("w64" if parts[0] == "rdx" else "w32", 0))
            continue
        if k == 0: defs.add(("entry", 0)); continue
        if not preds[k]: defs.add(("unknown-pred", 0)); continue
        stack.extend(preds[k])
    kinds = {d[0] for d in defs}
    if defs and all(d[0] == "w64" or (d[0] == "lit" and (d[1] & 5) != 5) for d in defs): return "flow-settled"
    if "call-clobber" in kinds: return "no-second-argument"
    if "entry" in kinds and not (kinds - {"entry", "w64", "lit"}): return "residue-passthrough"
    return "residue-computed"
flows = {}
for r in rows:
    flows[(r[0], r[1])] = flow(r[0], r[1])
fc = collections.Counter(flows[(r[0], r[1])] for r in rows if r[3].startswith("residue"))
ctl = collections.Counter(flows[(r[0], r[1])] for r in rows if not r[3].startswith("residue"))
ok("FC", set(ctl) == {"flow-settled"}, "control for the flow graph: the %d settled sites all come out flow-settled (no call-clobbered or entry path): %s" % (sum(ctl.values()), dict(ctl)))
ok("F", sum(fc.values()) == res, "the %d residue sites: %s" % (res, dict(fc)))
left = fc["residue-passthrough"] + fc["residue-computed"]
print("after F: settled %d of 607; residue %d (the enclosing function's own incoming rdx passed through %d, a computed 32-bit value %d)"
      % (607 - left, left, fc["residue-passthrough"], fc["residue-computed"]))
with open(os.path.join(HERE, "bq27-sites.tsv"), "w", encoding="utf-8", newline="\n") as h:
    h.write("function\tsite\tslot\tclass\tliteral\tdest\tlast_rdx_write\tflow\n")
    for r in rows: h.write("\t".join(map(str, r)) + "\t" + flows[(r[0], r[1])] + "\n")
print("FAILS", fails); sys.exit(1 if fails else 0)
