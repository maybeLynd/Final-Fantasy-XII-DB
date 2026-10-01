"""ramp_recut.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

RampChannelRecord (0xE0 bytes, 160 records in the block at *(void**)02B40528) still carries 18 rows reading
'mixed ... overlapping widths ... NOT resolved', from the 2026-09-25 cell census, and scalar rows that census typed
uint32 although every typed access to them is SSE single-precision. The 2026-09-27 flow re-cut held the type out
('accesses outside the 0xE0 record, so it is an array'). This settles widths and types from three access sources,
unioned by site:
  ramp-flow-accesses.tsv  type_flow_census.py, POOL=02B40528 CELLS=02B40528 TYPE_SIZE=0xE0 (index * 0xE0 + the block:
                          the accessor pattern the contract's section 14 item 5 names)
  ramp-cell-sites.json    census_receiver_fixpoint.py 02B40528 0 0xE0, SEED=cell, EMIT_JSON - adds the allocator's
                          pointer walk from 003B56E0, whose base advances by 0xE0 in a loop the flow census cannot hold
  DIRECT                  the two setters outside functions.tsv, 003B6950 (class 0x10) and 003B69B0 (class 0x0E), which
                          no census reaches; decoded here with the same pool pattern
Every site's access kind is reg_tracking.op_kind on the certified image; no receipt flag is trusted.

Rules
  W  widths - cpe_partial_recut.py's rule: inside a span, reads of <= 8 bytes define fields and must not overlap; every
     other access is a 16-byte move or starts and ends on the new boundaries; unread bytes stay DISCOVERED remainders.
  T  types from every access that carries one: an SSE scalar-single instruction -> float; movsx -> signed; any other
     integer instruction -> unsigned. A plain mov / movd / movq (register or immediate) carries WIDTH ONLY. A field with
     no typed access keeps the store's uintN width convention and says so; float with integer evidence is not typed.
Checks
  R  every union site decodes to an instruction with a [base + disp] operand of the recorded width
  A  the allocator (003B56D0) initialises with QWORD immediate stores that each span two cells - +0x14 (1.0f at +0x14,
     0 at +0x18), +0x5C, +0x78, +0x8C - and zero stores +0x1C / +0x24 / +0x50 / +0x64 / +0x70 / +0x80: the 8-byte widths
     the old census saw are store merges, not 8-byte fields; and +0x00 is one dword zero over four byte counters
  D  the unlisted setters: 003B6950 writes the counter byte +0x03, reads float +0x78, writes float +0x7C;
     003B69B0 the same at +0x01 / +0x70 / +0x74
  C  controls: +0x30 has no read (the contract: a published snapshot with no reader) and stays DISCOVERED; +0xD8 has no
     access; rule T rejects a hand float + integer pair and gives width-only for plain moves
  K  the cut agrees with CONTRACT-authored-command-ramp-channels.md sections 2 and 14 item 5: four counter bytes
     +0x00..+0x03; +0x14 and +0x18 separate; +0x1C unread; +0x20 / +0x24 / +0x28 three cells; +0x30 / +0x34 unread
  S  REGRESSION: no qualifying RampChannelRecord span is still a 'mixed' row, and every TYPE RESOLVED row carries its
     rule-T type (FAILS before the patch)
Usage: python ramp_recut.py [--receipt] [--patch]
  --receipt  regenerates the two receipts (about a minute), then checks
  --patch    applies the re-cut and the re-types to _types/fields.tsv (mixed EOLs, per line), then exits
"""
import csv, hashlib, json, os, struct, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(DB, ".."))
sys.path.insert(0, os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts"))
import reg_tracking as RT
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FIELDS = os.path.join(DB, "_types", "fields.tsv")
FLOW = os.path.join(HERE, "ramp-flow-accesses.tsv")
CELL = os.path.join(HERE, "ramp-cell-sites.json")
REC = "_index/candidates/ramp-channel-recut/ramp_recut.py"
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)

if "--receipt" in sys.argv:
    subprocess.run([sys.executable, os.path.join(DB, "_index", "candidates", "type-flow-census", "type_flow_census.py"),
                    EXE, os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv"), FLOW],
                   env=dict(os.environ, POOL="02B40528", CELLS="02B40528", TYPE_SIZE="0xE0"), check=True)
    subprocess.run([sys.executable, os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts", "census_receiver_fixpoint.py"),
                    "02B40528", "0", "0xE0"], env=dict(os.environ, SEED="cell", EMIT_JSON=CELL),
                   stdout=subprocess.DEVNULL, check=True)

B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def ins(a): return next(cs.disasm(d[off(a):off(a) + 16], a))
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

def memop(x, disp=None):
    for oi, op in enumerate(x.operands):
        if op.type == X86_OP_MEM and op.mem.index == 0 and (disp is None or op.mem.disp == disp): return oi, op
    return None, None

# ---- the union: (field, width, kind, instruction, site) ----
A, bad = set(), []
def add(field, width, site):
    x = ins(site); oi, op = memop(x)
    if op is None or op.size != width: bad.append("%08X" % site); return
    A.add((field, width, RT.op_kind(x, op, oi), x.mnemonic + " " + x.op_str, "%08X" % site))
for r in csv.DictReader(open(FLOW, encoding="utf-8"), delimiter="\t"):
    if not r["field"].startswith("-"): add(int(r["field"], 16), int(r["width"]), int(r["site"], 16))
for k, sites in json.load(open(CELL, encoding="utf-8"))["sites"].items():
    dp, w = map(int, k.split(":"))
    for s in sites: add(dp, w, int(s, 16))
# DIRECT: the two unlisted setters - `movzx r8d, cl ; imul r9, r8, 0xe0 ; add r9, [02B40528]`, then [r9 + disp]
DIRECT = {0x3B6950: 0x47, 0x3B69B0: 0x47}
direct = []
for f, ln in DIRECT.items():
    body = list(cs.disasm(d[off(f):off(f) + ln], f))
    pool = (body[1].mnemonic, body[1].op_str, body[2].mnemonic) == ("imul", "r9, r8, 0xe0", "add") and \
           body[2].operands[1].type == X86_OP_MEM and body[2].address + body[2].size + body[2].operands[1].mem.disp == 0x2B40528
    for x in body[3:]:
        oi, op = memop(x)
        if pool and op is not None and x.reg_name(op.mem.base) == "r9":
            direct.append((op.mem.disp, op.size, RT.op_kind(x, op, oi), x.mnemonic + " " + x.op_str, "%08X" % x.address))
        if x.mnemonic == "ret": break
A |= set(direct)
A = sorted(a for a in A if a[2] != "addr" and 0 <= a[0] < 0xE0)
check("R", not bad, "%d union accesses; sites whose operand width disagrees with the receipt: %s" % (len(A), bad[:5]))

# ---- rules ----
def tclass(t, w):
    m = t.split()[0]
    if m in ("mov", "movd", "movq"): return None
    if m.endswith("ss") or m in ("comiss", "ucomiss") or m.startswith("cvtss"): return "float"
    if m in ("movsx", "movsxd"): return "int%d" % (8 * w)
    return "uint%d" % (8 * w)
def rule_t(texts, w):
    ts = {tclass(t, w) for t in texts} - {None}
    if not ts: return "uint%d" % (8 * w), "width-only"
    if ts == {"float"}: return "float", "typed"
    if "float" in ts: return None, "float and integer evidence"
    return (next((t for t in ts if t.startswith("int")), sorted(ts)[0]), "typed")
def plan(o, n, acc_all=None):
    acc = [a for a in (acc_all or A) if a[0] < o + n and a[0] + a[1] > o]
    rd = [a for a in acc if "r" in a[2] and a[1] <= 8 and o <= a[0] and a[0] + a[1] <= o + n]
    rl = sorted({(a[0], a[1]) for a in rd})
    if not rl: return None, "no reads"
    if any(x[0] < y[0] + y[1] and y[0] < x[0] + x[1] and x != y for x in rl for y in rl): return None, "overlapping reads"
    bounds = {f for f, _ in rl} | {f + w for f, w in rl} | {o, o + n}
    for a in acc:
        if a[1] == 16: continue
        if a[0] < o or a[0] + a[1] > o + n or a[0] not in bounds or a[0] + a[1] not in bounds:
            return None, "crossing access %s %d %s at %s" % (hex(a[0]), a[1], a[2], a[4])
    out, cur = [], o
    for f, w in rl:
        if f > cur: out.append(("gap", cur, f - cur, None, None, [], []))
        same = [a for a in acc if (a[0], a[1]) == (f, w)]
        t, why = rule_t([a[3] for a in same], w)
        if t is None: return None, "type conflict at %s: %s" % (hex(f), why)
        out.append(("field", f, w, t, why, sorted({a[4] for a in same if "r" in a[2]}), sorted({a[4] for a in same if "w" in a[2]})))
        cur = f + w
    if cur < o + n: out.append(("gap", cur, o + n - cur, None, None, [], []))
    return out, "ok"

lines = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
mine = [(i, cells(l)) for i, l in enumerate(lines) if cells(l)[0] == "RampChannelRecord"]
qual = [(i, c, plan(int(c[1], 16), int(c[2]))) for i, c in mine if c[6] == "DISCOVERED" and c[3].startswith("mixed")]
qual = [(i, c, p) for i, c, (p, why) in qual if p]
retype = []
for i, c in mine:
    if c[6] != "TYPE RESOLVED": continue
    o, w = int(c[1], 16), int(c[2])
    t, why = rule_t([a[3] for a in A if (a[0], a[1]) == (o, w)], w)
    if t and why == "typed" and t != c[4]: retype.append((i, c, t))

if "--patch" in sys.argv:
    out = list(lines)
    for i, c, t in retype:
        eol = lines[i][len(lines[i].rstrip("\r\n")):]
        sites = sorted({a[4] for a in A if (a[0], a[1]) == (int(c[1], 16), int(c[2])) and tclass(a[3], int(c[2]))})
        c = list(c); was = c[4]; c[4] = t
        c[5] = c[5] + " || RE-TYPED %s 2026-09-28 (OPUS): every typed access is SSE single-precision (%s); the %s came " \
                      "from the access width alone" % (t, ", ".join(sites[:3]), was)
        c[8] = c[8] + " || RE-TYPED 2026-09-28 (OPUS, %s rule T). WAS %s" % (REC, was)
        out[i] = "\t".join(c) + eol
    for i, c, p in sorted(qual, key=lambda x: -x[0]):
        eol = lines[i][len(lines[i].rstrip("\r\n")):]; width = len(c); new = []
        for kind, f, w, t, why, rs, ws in p:
            if kind == "field":
                mean = ("read at %s%s. %s MEANING NOT CLAIMED here (see the contract's field table)"
                        % (", ".join(rs[:3]), ("; written at " + ", ".join(ws[:3])) if ws else "",
                           "Type from its typed accesses (rule T)." if why == "typed" else
                           "Moved only by plain moves: the type is the width, not a claim of integer representation."))
                r = ["RampChannelRecord", "0x%03X" % f, str(w), "field%03X" % f, t, mean, "TYPE RESOLVED", "PROVEN",
                     "RAMP RE-CUT 2026-09-28 (OPUS, %s W T): reads define the width; no other access crosses it. "
                     "|| WAS %s %s %s %s: %s" % (REC, c[1], c[2], c[3], c[4], c[5])]
            else:
                r = ["RampChannelRecord", "0x%03X" % f, str(w), "unobservedSpan%03X" % f, "u8[%d]" % w,
                     "the unread bytes of the former span %s; no read in the three sources" % c[3], "DISCOVERED", "UNKNOWN",
                     "RAMP RE-CUT REMAINDER 2026-09-28 (OPUS, %s)" % REC]
            new.append("\t".join(r + [""] * (width - len(r))) + eol)
        out[i:i + 1] = new
    open(FIELDS, "wb").write("".join(out).encode("utf-8"))
    print("re-cut %d spans; re-typed %d rows" % (len(qual), len(retype))); sys.exit(0)

def at(a): x = ins(a); return x.mnemonic, x.op_str
ALLOC = {0x3B572E: "qword ptr [rbx + 0x14], 0x3f800000", 0x3B5786: "qword ptr [rbx + 0x5c], 0x3f800000",
         0x3B578E: "qword ptr [rbx + 0x78], 0x3f800000", 0x3B57B0: "qword ptr [rbx + 0x8c], 0x3f800000",
         0x3B575F: "qword ptr [rbx + 0x1c], rsi", 0x3B5765: "qword ptr [rbx + 0x24], rsi", 0x3B5777: "qword ptr [rbx + 0x50], rsi",
         0x3B5796: "qword ptr [rbx + 0x64], rsi", 0x3B577B: "qword ptr [rbx + 0x70], rsi", 0x3B579F: "qword ptr [rbx + 0x80], rsi",
         0x3B579D: "dword ptr [rbx], esi"}
check("A", all(at(a) == ("mov", o) for a, o in ALLOC.items()) and at(0x3B56E6) == ("xor", "esi, esi")
      and at(0x3B56F6) == ("add", "rbx, 0xe0"),
      "003B56D0's pointer walk (add rbx, 0xe0) initialises with qword stores spanning two cells and a dword zero at +0x00")
dk = sorted((a[0], a[1], a[2]) for a in direct)
check("D", dk == [(0x1, 1, "w"), (0x3, 1, "w"), (0x10, 4, "r"), (0x10, 4, "r"), (0x70, 4, "r"), (0x74, 4, "w"),
                  (0x78, 4, "r"), (0x7C, 4, "w")], "unlisted setters 003B6950 / 003B69B0: %s" % [(hex(a), b, c) for a, b, c in dk])
c30 = plan(0x30, 8)[1]; cd8 = [a for a in A if 0xD8 <= a[0] < 0xE0]
t1 = rule_t(["addss xmm0, dword ptr [rbx + 0x48]", "cmp dword ptr [rbx + 0x48], 1"], 4)
t2 = rule_t(["mov eax, dword ptr [rbx + 0x20]", "mov dword ptr [r9 + 0x20], eax"], 4)
check("C", c30 == "no reads" and not cd8 and t1[0] is None and t2 == ("uint32", "width-only"),
      "+0x30 -> %s; +0xD8 accesses %d; float+cmp -> %s; plain moves -> %s" % (c30, len(cd8), t1, t2))
cut = {}
for i, c, p in qual:
    for kind, f, w, t, why, rs, ws in p: cut[f] = (kind, w)
k = (all(cut.get(o) == ("field", 1) for o in (0, 1, 2, 3)) and cut.get(0x14) == ("field", 4) and cut.get(0x18) == ("field", 4)
     and cut.get(0x1C) == ("gap", 4) and all(cut.get(o) == ("field", 4) for o in (0x20, 0x24, 0x28)))
F = {int(c[1], 16): c for i, c in mine}
k_after = (all(F.get(o, [0] * 7)[6] == "TYPE RESOLVED" and F[o][2] == "1" for o in (0, 1, 2, 3))
           and F.get(0x1C, [0] * 7)[6] == "DISCOVERED" and all(F.get(o, [0] * 7)[2] == "4" for o in (0x14, 0x18, 0x20, 0x24, 0x28)))
check("K", k or k_after, "the cut matches the contract's counters, +0x14 / +0x18, the unread +0x1C and the +0x20 vec3 cells")
check("S", not qual and not retype, "mixed spans still qualifying: %d %s; rows to re-type: %s"
      % (len(qual), [c[1] for i, c, p in qual][:6], [(c[1], c[4], t) for i, c, t in retype]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
