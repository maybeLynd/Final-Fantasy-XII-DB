"""rc5_constprop.py - RC-5 residue (FABLE, 2026-09-29): the value set of every variable (PUSHV) event-id operand in ORACLE's
rc5_verbs.tsv, by constant-set propagation of the script FILE variables over each script's control flow.

rc5_dataflow.py showed every such operand reads a FILE-class variable whose stores include `var + c` (OPADD), and
peek.py showed the shape `var = 7; ...; var = var + 1; startscene(var); ...` - a scene counter.

Why no stack model (v2): the REQ family's stack effects are not modelled by the shared decoder (resolve_args stops at
them), and a stack model that guessed them produced depth mismatches in 25 of 38 files. So the stack is not tracked.
Instead:
  - only file variables are tracked across control flow (dict key -> frozenset of ints, or TOP);
  - the value a POPV stores, and the operand a CALL passes, are read by a small BACKWARD EXPRESSION PARSER over the
    instructions just before it, accepting only pure ops: constants (PUSHII, PUSHI0..3, PUSHI pool), PUSHV of a file
    variable, and OPADD / OPSUB / OPMUL of two such expressions. Anything else makes the value TOP. A pure expression
    has no side effects, so evaluating it with the variable state at the POPV / CALL is exact.
  - control flow: a script (directory entry, stride 0x30) starts at its +8; +0x10 -> {count; {nameOff, offset}[count]}
    function entries; +0x14 -> {count; offset[count]} the jump table, indexed by JMP-family immediates
    (section-000-bytecode.md section 4). Opcode names from the interpreter page's table (the shared decoder's OPN
    mislabels this range as JMPPOPX.. / UNK5A..UNK5C): JMP 0x51 and JMPINTERNAL 0x60 are unconditional; the compare
    jumps 0x52..0x57 (POPCMPY*JMP, POP2CMPYBTWNJMP) and 0x5A POPXJMP, 0x5B POPXCJMP, 0x5C POPXNCJMP take the jump
    AND fall through here (0x5A over-approximated: sound either way); RET family 0x2D..0x31 ends the path; every other
    op falls through. (v2.1: v2 missed the 0x5A..0x5C edges and left three sites unreached.)
  - entry state of every function: each file variable = {0} U everything any function of the file stores into it
    (iterated to a fixpoint), so cross-function flow and re-entry are covered. Sets above 512 values widen to TOP.
  - a verb can write a variable only through a PUSHP reference; rc5_dataflow.tsv records 0 references for every
    startscene / startscene_4b3 variable. Native code does not write file-class storage (the script image's own data,
    script-variables-and-their-storage-classes.md section 3); that is the model's one assumption.
Controls: (1) every variable site is reached with a non-empty value set; (2) every CONSTANT startscene site in the same
files evaluates to exactly its rc5_verbs.tsv value; (3) a jump whose index is outside the table is counted and makes its
file UNSOUND.
"""
import collections, csv, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
TOP = None
WIDEN = 512
TSV = os.path.join(DB, "_index", "candidates", "rc5-event-slot-routes-0930", "rc5_verbs.tsv")
DF = os.path.join(HERE, "rc5_dataflow.tsv")
ARG = {"startscene": (1, 0), "startscene_4b3": (2, 0), "eventread_e8": (2, 1), "summoneventread": (1, 0)}
IDS = {0x11B: "startscene", 0x4B3: "startscene_4b3", 0xE8: "eventread_e8", 0x198: "summoneventread"}
dyn_sites = {(r["file"], int(r["pc"], 16)): r for r in csv.DictReader(io.open(DF, encoding="utf-8"), delimiter="\t")}
const_sites = {}
for r in csv.DictReader(io.open(TSV, encoding="utf-8"), delimiter="\t"):
    if r["verb"] == "startscene" and r["file"] in {k[0] for k in dyn_sites}:
        v = r["resolved_args_push_order"]
        if v.lstrip("-").isdigit():
            const_sites[(r["file"], int(r["pc"], 16))] = int(v)
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)


def join(a, b):
    if a is TOP or b is TOP:
        return TOP
    u = a | b
    return TOP if len(u) > WIDEN else u


def analyse(path):
    b = G.V.read_entry(f, names, blocks, path)
    sec = b[0x80:0x80 + U32(b, 0x84)]
    vt, pool = U32(sec, 0x28), U32(sec, 0x20)
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    ents = [diroff + 4 + s * 0x30 for s in range(cnt)]
    starts = sorted(set(U32(sec, e + 8) for e in ents))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    scripts = []
    for e in ents:
        st = U32(sec, e + 8)
        end = min((x for x in bounds if x > st), default=len(sec))
        ins, _ = G.decode(sec[st:end])
        at = {pc: j for j, (pc, op, imm) in enumerate(ins)}
        fo = U32(sec, e + 0x10); fcount = U32(sec, fo)
        fentry = [U32(sec, fo + 4 + i * 8 + 4) for i in range(fcount)]
        jo = U32(sec, e + 0x14); jcount = U32(sec, jo)
        jt = [U32(sec, jo + 4 + i * 4) for i in range(jcount)]
        scripts.append((st, ins, at, fentry, jt))

    def desc(idx):
        d = U32(sec, vt + idx * 8 + 4)
        return ((d >> 24) & 7, d & 0xFFFFFF, (d >> 28) & 0xF)

    def parse(ins, k):
        """Backward parse of the pure expression ending at index k. Returns (tree, first index) or (None, k)."""
        if k < 0:
            return None, k
        pc, op, imm = ins[k]
        if op == 0x4F:
            return ("c", imm), k
        if 0x3E <= op <= 0x41:
            return ("c", op - 0x3E), k
        if op == 0x4E:
            return ("c", S32(sec, pool + imm * 4 + 4)), k
        if op == 0x48:
            d = desc(imm)
            return (("v", d) if d[0] == 1 else None), k
        if op in (0x12, 0x13, 0x14):
            r, k1 = parse(ins, k - 1)
            if r is None:
                return None, k
            l, k2 = parse(ins, k1 - 1)
            if l is None:
                return None, k
            return (op, l, r), k2
        return None, k

    def ev(t, V, entry):
        if t is None:
            return TOP
        if t[0] == "c":
            return frozenset({t[1]})
        if t[0] == "v":
            return V.get(t[1], entry[t[1]])
        a, b2 = ev(t[1], V, entry), ev(t[2], V, entry)
        if a is TOP or b2 is TOP:
            return TOP
        out = set()
        for x in a:
            for y in b2:
                out.add(x + y if t[0] == 0x12 else x - y if t[0] == 0x13 else x * y)
                if len(out) > WIDEN:
                    return TOP
        return frozenset(out)

    def arg_tree(ins, j, need, ix):
        """Trees of the `need` operands pushed immediately before index j (last pushed first); ix counts from the first
        pushed. Only a contiguous run of pure expressions is accepted."""
        trees, k = [], j - 1
        for _ in range(need):
            t, k1 = parse(ins, k)
            if t is None:
                return None
            trees.append(t); k = k1 - 1
        trees.reverse()                     # push order
        return trees[ix]

    entry = collections.defaultdict(lambda: frozenset({0}))
    bad = 0
    ROUNDS = 12
    for rnd in range(ROUNDS + 1):
        stored = {}
        seen = collections.defaultdict(lambda: frozenset())
        seen_top = set()
        for st, ins, at, fentry, jt in scripts:
            for fe in fentry:
                if fe not in at:
                    bad += 1; continue
                states = {}
                work = [(at[fe], ())]
                while work:
                    j, vars_ = work.pop()
                    prev = states.get(j)
                    if prev is not None:
                        dv = dict(prev)
                        for k, v in vars_:
                            dv[k] = join(dv.get(k, entry[k]), v)
                        for k in list(dv):
                            if k not in dict(vars_):
                                dv[k] = join(dv[k], entry[k])
                        nv = tuple(sorted(dv.items()))
                        if nv == prev:
                            continue
                        vars_ = nv
                    states[j] = vars_
                    V = dict(vars_)
                    pc, op, imm = ins[j]
                    nxt = [j + 1] if j + 1 < len(ins) else []
                    if op == 0x49:
                        d = desc(imm)
                        if d[0] == 1:
                            t, _ = parse(ins, j - 1)
                            v = ev(t, V, entry)
                            V[d] = v
                            stored[d] = join(stored.get(d, frozenset()), v) if v is not TOP else TOP
                    elif op in (0x58, 0x59, 0x5D, 0x5E) and imm in IDS:
                        ar, ix = ARG[IDS[imm]]
                        t = arg_tree(ins, j, ar, ix)
                        v = ev(t, V, entry)
                        if v is TOP:
                            seen_top.add(st + pc)
                        else:
                            seen[st + pc] = join(seen[st + pc], v)
                    elif op in G.RET_OPS:
                        nxt = []
                    elif op in (0x51, 0x60) or 0x52 <= op <= 0x57 or 0x5A <= op <= 0x5C:
                        if imm >= len(jt) or jt[imm] not in at:
                            bad += 1; nxt = []
                        else:
                            nxt = [at[jt[imm]]] + ([] if op in (0x51, 0x60) else nxt)
                    nv = tuple(sorted(V.items()))
                    for n in nxt:
                        work.append((n, nv))
        changed = []
        for k, v in stored.items():
            ne = join(entry[k], v) if v is not TOP else TOP
            if ne != entry[k]:
                entry[k] = ne; changed.append(k)
        if not changed:
            break
        if rnd == ROUNDS - 1:
            # v2.2: no convergence within ROUNDS - a counter that keeps growing across function entries (a loop or a
            # re-entered function). Its values are not bounded by this model (branch conditions are not refined), so
            # the variable goes to TOP and one more round propagates that (sound; v2.1 reported the truncated sets).
            for k in changed:
                entry[k] = TOP
    return seen, seen_top, bad


results, fails, filebad = {}, 0, {}
files = sorted({k[0] for k in dyn_sites})
for p in files:
    seen, seen_top, bad = analyse(p)
    filebad[p] = bad
    for (pp, pc), r in dyn_sites.items():
        if pp != p:
            continue
        if pc in seen_top:
            results[(p, pc)] = (r, TOP)
        elif pc in seen and seen[pc]:
            results[(p, pc)] = (r, seen[pc])
        else:
            fails += 1; print("FAIL unreached site", p, "%X" % pc)
    for (pp, pc), want in const_sites.items():
        if pp == p:
            u = TOP if pc in seen_top else seen.get(pc)
            if u != frozenset({want}):
                fails += 1; print("FAIL control: constant site", p, "%X" % pc, "want", want, "got", u)
print("files %d, variable sites %d, constant-site controls %d (all reproduced unless FAIL above)" % (
    len(files), len(dyn_sites), len(const_sites)))
print("files with an unresolvable jump or function entry (UNSOUND):", [(p, n) for p, n in filebad.items() if n])
summ = collections.Counter(); vals = collections.Counter()
with io.open(os.path.join(HERE, "rc5_constprop.tsv"), "w", encoding="utf-8", newline="\n") as w:
    w.write("file\tpc\tverb\tclass\tvalues\tn\n")
    for (p, pc), (r, u) in sorted(results.items()):
        if filebad[p]:
            summ[(r["verb"], "UNSOUND")] += 1
            w.write("%s\t%X\t%s\t%s\tUNSOUND\t-\n" % (p, pc, r["verb"], r["class"])); continue
        if u is TOP:
            summ[(r["verb"], "TOP")] += 1
            w.write("%s\t%X\t%s\t%s\tTOP\t-\n" % (p, pc, r["verb"], r["class"])); continue
        summ[(r["verb"], "exact-1" if len(u) == 1 else "set")] += 1
        for x in u:
            vals[(r["verb"], x)] += 1
        w.write("%s\t%X\t%s\t%s\t%s\t%d\n" % (p, pc, r["verb"], r["class"], ",".join(map(str, sorted(u))), len(u)))
for k, n in sorted(summ.items()):
    print("  %-16s %-8s %d" % (k[0], k[1], n))
for vb in ("startscene", "startscene_4b3", "eventread_e8"):
    xs = sorted(x for (v, x) in vals if v == vb)
    print("  %s values: %d distinct, range %s" % (vb, len(xs), (xs[0], xs[-1]) if xs else "-"))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
