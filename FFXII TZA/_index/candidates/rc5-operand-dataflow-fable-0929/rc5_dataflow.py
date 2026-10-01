"""rc5_dataflow.py - RC-5 residue (FABLE, 2026-09-29): bound the non-constant (PUSHV) event-id operands of ORACLE's
rc5_verbs.tsv by bytecode dataflow over the shipped scripts.

For every row of ../rc5-event-slot-routes-0930/rc5_verbs.tsv whose event-id operand is `dyn:PUSHV`
(startscene: the operand; startscene_4b3: the first pushed; eventread_e8: the second; summoneventread: the operand):
  1. find the PUSHV (0x48) that produces the operand (the decoder's backward stack walk, resolve_args), and its 16-bit
     variable index;
  2. read the descriptor [vt + idx*8 + 4] from the script's variable table (section header +0x28; class = bits 24..26,
     offset = bits 0..23, width = bits 28..31; script-variables-and-their-storage-classes.md section 2.2);
  3. collect every POPV (0x49) whose descriptor has the same (class, offset, width) in the variable's scope - the same
     file for classes 1 (file), 2 (local), 4 and 5 (scratch); every script for class 0 (global) - and resolve the value
     each store pushes (constant: PUSHII / PUSHI0..3 / PUSHI pool; otherwise the producing instruction's name);
  4. note any PUSHP (0x4B, a reference that a verb could write through) of the same variable in scope.
A site is BOUNDED when every store is a constant and no reference is passed. Its value set is the stored constants,
plus the variable's initial value (0) if some path could read it before any store, which is not decided here, so 0 is
always included and marked.
Control: every dyn:PUSHV row of ORACLE's TSV must be found at its (file, pc) as a call of the same id (FAILS otherwise).
Limits: class 0 (global) variables can also be written by native code (story state, save load); a bounded global is
bounded only against script stores.
"""
import collections, csv, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
TSV = os.path.join(DB, "_index", "candidates", "rc5-event-slot-routes-0930", "rc5_verbs.tsv")
ARG = {"startscene": (1, 0), "startscene_4b3": (2, 0), "eventread_e8": (2, 1), "summoneventread": (1, 0)}  # (arity, arg idx)
IDS = {"startscene": 0x11B, "startscene_4b3": 0x4B3, "eventread_e8": 0xE8, "summoneventread": 0x198}

rows = [r for r in csv.DictReader(io.open(TSV, encoding="utf-8"), delimiter="\t")]
want = []
for r in rows:
    if r["verb"] not in ARG:
        continue
    vals = r["resolved_args_push_order"].split(";")
    ar, ix = ARG[r["verb"]]
    if len(vals) == ar and vals[ix] == "dyn:PUSHV":
        want.append(r)
print("ORACLE dyn:PUSHV event-id sites: %d  %s" % (len(want), dict(collections.Counter(r["verb"] for r in want))))
files_needed = sorted(set(r["file"] for r in want))
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)


def load(path):
    b = G.V.read_entry(f, names, blocks, path)
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        return None
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    starts = sorted(set(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    funcs = []
    for st in starts:
        end = min((x for x in bounds if x > st), default=len(sec))
        if st < len(sec) and end > st:
            ins, _ = G.decode(sec[st:end])
            funcs.append((st, ins))
    return sec, funcs


def desc(sec, idx):
    vt = U32(sec, 0x28)
    d = U32(sec, vt + idx * 8 + 4)
    return ((d >> 24) & 7, d & 0xFFFFFF, (d >> 28) & 0xF)


def const_of(sec, a):
    name, im, kind = a
    if name == "PUSHII":
        return im
    if name.startswith("PUSHI") and name[-1].isdigit():
        return int(name[-1])
    if name == "PUSHI":
        return S32(sec, U32(sec, 0x20) + im * 4 + 4)
    return None


scripts = {}
all_ebp = sorted(p for p in names if p.lower().endswith(".ebp"))
# stores and references, per file, keyed by descriptor; globals also pooled image-wide (script stores only)
def stores_of(path):
    if path in scripts:
        return scripts[path]
    got = load(path)
    out = collections.defaultdict(list); refs = collections.Counter()
    if got:
        sec, funcs = got
        for st, ins in funcs:
            for j, (pc, op, imm) in enumerate(ins):
                if op == 0x49:
                    k = desc(sec, imm)
                    args, s = G.resolve_args(ins, j, 1, verbs)
                    v = const_of(sec, args[0]) if args else None
                    out[k].append(v if v is not None else ("dyn:%s" % (args[0][0] if args else s)))
                elif op == 0x4B:
                    refs[desc(sec, imm)] += 1
    scripts[path] = (got, out, refs)
    return scripts[path]


need_global = False
sites = []
fails = 0
for r in want:
    got, st_, rf_ = stores_of(r["file"])
    if not got:
        fails += 1; print("FAIL unreadable", r["file"]); continue
    sec, funcs = got
    pc = int(r["pc"], 16)
    hit = None
    for st, ins in funcs:
        for j, (ipc, op, imm) in enumerate(ins):
            if st + ipc == pc:
                hit = (st, ins, j, op, imm)
    if not hit or hit[4] != IDS[r["verb"]]:
        fails += 1; print("FAIL site not found", r["file"], r["pc"]); continue
    st, ins, j, op, imm = hit
    ar, ix = ARG[r["verb"]]
    args, s = G.resolve_args(ins, j, ar + (1 if op in (0x59, 0x5E) else 0), verbs)
    a = args[ix] if args else None
    if not a or a[0] != "PUSHV":
        fails += 1; print("FAIL operand is not PUSHV", r["file"], r["pc"], a); continue
    k = desc(sec, a[1])
    need_global |= (k[0] == 0)
    sites.append((r, k))
if need_global:
    for p in all_ebp:
        stores_of(p)
glob = collections.defaultdict(list); grefs = collections.Counter()
for p, (got, st_, rf_) in scripts.items():
    for k, v in st_.items():
        if k[0] == 0:
            glob[k] += v
    for k, n in rf_.items():
        if k[0] == 0:
            grefs[k] += n
CLS = {0: "global", 1: "file", 2: "local", 4: "scratch1", 5: "scratch2", 7: "array"}
summary = collections.Counter(); allvals = collections.Counter(); out = []
for r, k in sites:
    got, st_, rf_ = scripts[r["file"]]
    vals = glob[k] if k[0] == 0 else st_.get(k, [])
    refs = grefs[k] if k[0] == 0 else rf_.get(k, 0)
    consts = sorted(set(v for v in vals if isinstance(v, int)))
    dyn = sorted(set(v for v in vals if not isinstance(v, int)))
    status = "BOUNDED" if not dyn and not refs else ("REF-PASSED" if refs and not dyn else "DYNAMIC-STORE")
    if k[0] == 0 and status == "BOUNDED":
        status = "BOUNDED-SCRIPT-ONLY"
    if not vals and not refs:
        status = "NEVER-STORED"
    summary[(r["verb"], CLS.get(k[0], str(k[0])), status)] += 1
    for v in consts:
        allvals[v] += 1
    out.append((r["file"], r["pc"], r["verb"], CLS.get(k[0], str(k[0])), "%X" % k[1], k[2], status, len(vals),
                ",".join(map(str, consts)), ",".join(dyn), refs))
with io.open(os.path.join(HERE, "rc5_dataflow.tsv"), "w", encoding="utf-8", newline="\n") as w:
    w.write("file\tpc\tverb\tclass\toffset\twidth\tstatus\tstores\tconst_values\tdynamic_producers\trefs\n")
    for t in out:
        w.write("\t".join(map(str, t)) + "\n")
print("sites analysed: %d (control: all ORACLE dyn:PUSHV rows found as calls with a PUSHV operand: %s)" %
      (len(sites), "PASS" if len(sites) == len(want) else "FAIL"))
for (v, c, s), n in sorted(summary.items()):
    print("  %-16s %-9s %-20s %d" % (v, c, s, n))
print("distinct stored constants across the sites' variables (+0 initial not listed): %d" % len(allvals))
print("  values:", sorted(allvals)[:80], "..." if len(allvals) > 80 else "")
print("FAILS %d" % (fails + (len(sites) != len(want))))
sys.exit(1 if fails or len(sites) != len(want) else 0)
