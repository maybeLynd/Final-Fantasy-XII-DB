"""rc5c_loops.py - RC-5 residue item 1, the premise ORACLE left open: does any increment of a counter that feeds a
variable startscene / startscene_4b3 / counter eventread_e8 operand run more than once between the stores that bound it?
(FABLE, 2026-10-02). Static; shipped bytecode only.

The walk is ORACLE's (../rc5b-event-slot-residue-0930/rc5b_operands.py), copied, not imported: importing that script
runs it and rewrites its .tsv. It is the database's EBP2 walk and decoder,
`25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py`, with its backward stack resolver.
Copied unchanged: the per-file loop, the descriptor decode, the increment idiom, the store table, domain() and
classify(). Added: each actor's function table and jump table (directory entry +0x10 / +0x14, BW-5,
section-000-bytecode.md section 4), kept per actor.

Control flow (opcode semantics: the interpreter page and the handler table in
_experiments/evidence/script-division-unordered-guard/retained/consumer-before.md):
- a JMP-family immediate is an index into the ACTOR's jump table, whose entry is an offset within the actor's code;
- unconditional: 0x51 JMP, 0x60 JMPINTERNAL, 0x5A POPXJMP;
- conditional (fall through or jump): 0x52-0x57 POPCMPY*JMP / POP2CMPYBTWNJMP, 0x5B POPXCJMP, 0x5C POPXNCJMP;
- no successor: 0x2D RET, 0x2E RETN, 0x2F RETT, 0x30 RETTN;
- everything else falls through, including 0x31 DRET (inert) and the REQ / wait / CALL family (a yielding CALL repeats
  only itself).
The CFG is built over the whole actor's code, NOT over a function body cut at the next function offset, so a jump that
leaves its body and a body that falls through into the next function (the OV-16 review's F1 defects,
../auditsem-review-ov16m-0930/ov16m_sem.py) are followed, not lost. Those defects are still counted for the functions
that hold an increment (C5).

Per increment site i of a counter variable V (the POPV of `V = V + k`), with R = the constant (non-increment) stores of
V in the same actor:
- LOOP-ANY:   i lies on a cycle of the actor CFG;
- LOOP-LIT:   the brief's literal test: inside i's function body, a JMP-family source after i targets at or before i;
- LOOP-RESET-FREE: i lies on a cycle that avoids every node of R - only then can i run twice between two stores of V
  inside one invocation (a loop that re-runs the reset re-bounds V on every lap);
- UNDOM-OWN:  i is reachable from its own function's entry without passing a node of R (so it is NOT dominated by a
  reset in its own function); UNDOM-ANY: the same from any function entry of the actor (fall-through into i).
An undominated increment is the case where V accumulates across invocations: the interval bound then holds only if the
function is not entered twice between two resets, which is a run-time fact.

Controls:
- C0 ORACLE's counts reproduce: startscene 34,125 sites and 3,429 variable operands (3,141 constant+increment, 288
  increment-only), startscene_4b3 45, eventread_e8 4 counters.
- C1 / C2 ORACLE's own controls (startscene sites; legal descriptors) - same code.
- C3 synthetic: straight-line reset-then-increment is not a loop and is dominated; an increment under a backward JMP is
  a reset-free loop and undominated; a loop that re-runs the reset is a loop but not reset-free; increment-then-reset
  is undominated. Same functions as the corpus run.
- C4 corpus positive control: over the same population, backward jumps and cycles exist (the I-register `for` idiom
  `... OPLSE POPXNCJMP` with a backward JMP is located and printed), and over EVERY `x = x + k` POPV in the us copy (not
  only the counters) the detector finds increments on reset-free cycles - so a zero on the counters is not a blind
  detector.
- C5 containment: every jump index resolves to an instruction boundary of its actor (else counted).

Bound check: per operand site, ORACLE's interval is recomputed and corrected. The declared value of a class-1 variable
(the image's file-variable area, header +0x38) joins the interval when an increment or the read can run before any
store of the variable; an increment on a reset-free cycle makes the upper end fail (only the store's width clamp,
script-variables page section 2.2, bounds it).

F1 (finding): ORACLE's resolver takes the stack top as the value a POPV stores. For an array (class 7) POPV the top is
the INDEX: the image's store helper resolves (pops the indices) before it pops the value. The four counter
eventread_e8 operands read such an array, so their [0, 3] is an index range. F1 checks the helper in the image and the
four stores in the bytecode.

Outputs: rc5c_loops.out (this report), rc5c_increments.tsv (one row per counter increment site),
rc5c_sites.tsv (one row per operand site: ORACLE's interval and the corrected one).
"""
import bisect, collections, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
_cwd = os.getcwd()
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G  # noqa: E402
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- control-flow primitives (used by corpus and C3)
UNCOND = {0x51, 0x60, 0x5A}
COND = {0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x5B, 0x5C}
JMPF = UNCOND | COND
STOP = {0x2D, 0x2E, 0x2F, 0x30}


def build_cfg(ins, joffs):
    """successor lists over instruction indices; returns (succ, unresolved jump count)."""
    pcj = {pc: j for j, (pc, _o, _i) in enumerate(ins)}
    succ, bad = [], 0
    for j, (pc, op, imm) in enumerate(ins):
        s = []
        if op in JMPF:
            t = joffs[imm] if imm < len(joffs) else None
            if t in pcj:
                s.append(pcj[t])
            else:
                bad += 1
            if op in COND and j + 1 < len(ins):
                s.append(j + 1)
        elif op not in STOP and j + 1 < len(ins):
            s.append(j + 1)
        succ.append(s)
    return succ, bad, pcj


def reach(succ, srcs, goal, avoid=frozenset()):
    """is goal reachable from any of srcs (the sources themselves count) without entering a node of avoid?"""
    seen, st = set(), [s for s in srcs if s not in avoid]
    while st:
        x = st.pop()
        if x == goal:
            return True
        if x in seen:
            continue
        seen.add(x)
        st.extend(y for y in succ[x] if y not in avoid and y not in seen)
    return False


def on_cycle(succ, n, avoid=frozenset()):
    return reach(succ, succ[n], n, avoid)


def lit_backjump(ins, joffs, lo, hi, pc):
    """the brief's literal test: a JMP-family source in [pc, hi) whose target lies in [lo, pc]."""
    for p, op, imm in ins:
        if lo <= p < hi and p > pc and op in JMPF and imm < len(joffs) and lo <= joffs[imm] <= pc:
            return True
    return False


# ---------------------------------------------------------------- C3: synthetic cases
def asm(*xs):
    b = bytearray()
    for x in xs:
        if isinstance(x, tuple):
            b += bytes([x[0], x[1] & 0xFF, x[1] >> 8])
        else:
            b.append(x)
    return bytes(b)


PUSHV, POPV, PUSHII, PUSHI1, OPADD, JMP, RET = 0x48, 0x49, 0x4F, 0x3F, 0x12, 0x51, 0x2D
INC = [(PUSHV, 0), PUSHI1, OPADD, (POPV, 0)]
RESET = [(PUSHII, 0), (POPV, 0)]
syn = {
    "straight reset-then-increment": (asm(*RESET, *INC, RET), [0]),
    "increment under a backward JMP": (asm(*INC, (JMP, 0), RET), [0]),
    "loop re-running its reset": (asm(*RESET, *INC, (JMP, 0), RET), [0]),
    "increment then reset": (asm(*INC, *RESET, RET), [0]),
}
want = {"straight reset-then-increment": (False, False, False),
        "increment under a backward JMP": (True, True, True),
        "loop re-running its reset": (True, False, False),
        "increment then reset": (False, False, True)}
for nm, (code, joffs) in syn.items():
    ins, _ = G.decode(code)
    succ, bad, pcj = build_cfg(ins, joffs)
    pops = [j for j, (pc, op, imm) in enumerate(ins) if op == POPV]
    incj = [j for j in pops if j >= 3 and ins[j - 1][1] == OPADD][0]
    R = frozenset(j for j in pops if j != incj)
    got = (on_cycle(succ, incj), on_cycle(succ, incj, R), reach(succ, [0], incj, R))
    check("C3 synthetic '%s': (loop, reset-free loop, undominated) = %s" % (nm, want[nm]), got == want[nm], str(got))

# ---------------------------------------------------------------- ORACLE's walk (copied) + per-actor tables
WANT = {0x11B: ("startscene", 1), 0x4B3: ("startscene_4b3", 2), 0xE8: ("eventread_e8", 2), 0xE7: ("eventread", 1),
        0x198: ("summoneventread", 1), 0x202D: ("debug_eventload", 2)}
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
FILES = {}
ACT = {}        # (path, start) -> dict(ins, foffs, fnames, joffs)
sites = []
stores = collections.defaultdict(list)
WIDTH = {}        # variable key -> descriptor width code


def desc(sec, tbl, idx):
    try:
        v = U32(sec, tbl + 4 + idx * 8)
    except struct.error:
        return None
    return (v >> 24) & 7, v & 0xFFFFFF, (v >> 28) & 0xF, v


def const_of(sec, pool, name, im):
    if name == "PUSHII":
        return im if im < 0x8000 else im - 0x10000
    if name.startswith("PUSHI") and name[-1].isdigit():
        return int(name[-1])
    if name == "PUSHI":
        try:
            return S32(sec, pool + im * 4 + 4)
        except struct.error:
            return None
    return None


def cstr(sec, o):
    return sec[o:sec.find(b"\0", o)].decode("cp932", "replace")


for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18)
    cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        continue
    pool, tbl = U32(sec, 0x20), U32(sec, 0x28)
    npool = U32(sec, 0x4C)
    tabs = {}
    for s in range(cnt):
        en = diroff + 4 + s * 0x30
        st0 = U32(sec, en + 8)
        if st0 in tabs:
            continue
        ft = U32(sec, en + 0x10); nf = U32(sec, ft)
        lt = U32(sec, en + 0x14); nj = U32(sec, lt)
        tabs[st0] = ([U32(sec, ft + 4 + 8 * i + 4) for i in range(nf)],
                     [cstr(sec, npool + U32(sec, ft + 4 + 8 * i)) for i in range(nf)],
                     [U32(sec, lt + 4 + 4 * i) for i in range(nj)], cstr(sec, npool + U32(sec, en)))
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start:
            continue
        ins, anomaly = G.decode(sec[start:end])
        if (path, start) not in ACT:
            fo, fn, jo, an = tabs[start]
            ACT[(path, start)] = dict(ins=ins, foffs=fo, fnames=fn, joffs=jo, actor=an, anomaly=anomaly)
        for j, (pc, op, imm) in enumerate(ins):
            if op == 0x49:
                d = desc(sec, tbl, imm)
                if d is None:
                    continue
                args, st = G.resolve_args(ins, j, 1, verbs)
                prod = args[0] if args else ("?" + st, None, "unresolved")
                if j >= 3 and ins[j - 1][1] == 0x12:
                    a, c = ins[j - 3], ins[j - 2]
                    if c[1] == 0x48 and a[1] != 0x48:
                        a, c = c, a
                    if a[1] == 0x48 and desc(sec, tbl, a[2])[:2] == d[:2]:
                        k = const_of(sec, pool, G.OPN.get(c[1], ""), c[2]) if c[2] is not None else                             (int(G.OPN[c[1]][-1]) if G.OPN.get(c[1], "").startswith("PUSHI") and G.OPN[c[1]][-1].isdigit() else None)
                        if k is not None:
                            prod = ("INC", k, "inc")
                key = ("*" if d[0] == 0 else path, d[0], d[1])
                WIDTH.setdefault(key, d[2])
                stores[key].append((path, start, pc, prod))
            elif op in (0x58, 0x59, 0x5D, 0x5E) and imm in WANT:
                vname, ar = WANT[imm]
                need = ar + (1 if op in (0x59, 0x5E) else 0)
                args, st = G.resolve_args(ins, j, need, verbs)
                sites.append((path, start, pc, vname, args, st))
    FILES[path] = (sec, pool, tbl)
os.chdir(_cwd)


def domain(path, cls, off, depth=0, seen=()):
    key = ("*" if cls == 0 else path, cls, off)
    if key in seen or depth > 3:
        return set(), ["cycle-or-depth %s" % (key,)]
    consts, other = set(), []
    for p, start, pc, prod in stores.get(key, []):
        name, im, kind = prod
        if kind == "inc":
            other.append("INC%+d" % im)
            continue
        sec, pool, tbl = FILES[p]
        c = const_of(sec, pool, name, im) if im is not None else None
        if c is not None:
            consts.add(c)
        elif name == "PUSHV":
            d = desc(sec, tbl, im)
            cc, oo = domain(p, d[0], d[1], depth + 1, seen + (key,))
            consts |= cc
            other += oo
        else:
            other.append("%s@%s+%X" % (name, p.split("/")[-1], start + pc))
    return consts, other


def closure(path, cls, off, depth=0, seen=()):
    """the variable keys domain() reads: the operand's own and every PUSHV copy source (same depth limit)."""
    key = ("*" if cls == 0 else path, cls, off)
    if key in seen or depth > 3:
        return []
    out = [key]
    for p, start, pc, (name, im, kind) in stores.get(key, []):
        if kind != "inc" and name == "PUSHV":
            sec, pool, tbl = FILES[p]
            if const_of(sec, pool, name, im) is None:
                d = desc(sec, tbl, im)
                out += closure(p, d[0], d[1], depth + 1, seen + (key,))
    return out


def classify(path, prod):
    sec, pool, tbl = FILES[path]
    name, im, kind = prod
    c = const_of(sec, pool, name, im) if im is not None else None
    if c is not None:
        return ("const", c)
    if name == "PUSHV":
        return ("var", desc(sec, tbl, im))
    return ("expr", name)


# ---------------------------------------------------------------- C0: ORACLE's counter populations
summary = collections.Counter()
bad_desc = 0
rows = collections.defaultdict(list)   # counter class -> [(path, site pc, var key, consts, others)]
nvar = collections.Counter()
for path, start, pc, vname, args, st in sites:
    summary[vname] += 1
    if not args or vname not in ("startscene", "startscene_4b3", "eventread_e8"):
        continue
    for k, prod in enumerate(args):
        kind, v = classify(path, prod)
        if kind != "var":
            continue
        nvar[vname] += 1
        if v is None or v[0] not in (0, 1, 2, 4, 5, 7) or v[2] > 5:
            bad_desc += 1
        cc, oo = domain(path, v[0], v[1])
        if oo and all(o.startswith("INC") for o in oo):
            cls = "%s %s" % (vname, "constant+increment" if cc else "increment-only")
            rows[cls].append((path, start, start + pc, ("*" if v[0] == 0 else path, v[0], v[1]), cc, oo, pc))
            WIDTH.setdefault(("*" if v[0] == 0 else path, v[0], v[1]), v[2])
n = {c: len(r) for c, r in rows.items()}
check("C1 startscene sites %d (RC-5 / ORACLE: 34,125)" % summary["startscene"], summary["startscene"] == 34125)
check("C2 every PUSHV operand's descriptor decodes to a legal class and width (bad: %d)" % bad_desc, bad_desc == 0)
check("C0 ORACLE's counter populations reproduce: startscene variable operands %d (3,429) = constant+increment %d "
      "(3,141) + increment-only %d (288); startscene_4b3 %d (45); counter eventread_e8 %d (4)"
      % (nvar["startscene"], n.get("startscene constant+increment", 0), n.get("startscene increment-only", 0),
         n.get("startscene_4b3 constant+increment", 0), n.get("eventread_e8 constant+increment", 0)),
      nvar["startscene"] == 3429 and n.get("startscene constant+increment") == 3141
      and n.get("startscene increment-only") == 288 and n.get("startscene_4b3 constant+increment") == 45
      and n.get("eventread_e8 constant+increment") == 4 and "startscene_4b3 increment-only" not in n
      and "eventread_e8 increment-only" not in n)

# ---------------------------------------------------------------- per-actor CFG cache
CFG = {}


def cfg(a):
    if a not in CFG:
        A = ACT[a]
        succ, bad, pcj = build_cfg(A["ins"], A["joffs"])
        ents = sorted({pcj[o] for o in A["foffs"] if o in pcj})
        CFG[a] = (succ, bad, pcj, ents, sorted(set(A["foffs"])), [x[0] for x in A["ins"]])
    return CFG[a]


def own_func(A, fo, pc):
    """(entry offset, next function offset, name) of the function whose cut body holds pc."""
    k = bisect.bisect_right(fo, pc) - 1
    lo = fo[k] if k >= 0 else None
    hi = fo[k + 1] if k + 1 < len(fo) else 10 ** 9
    nm = A["fnames"][A["foffs"].index(lo)] if lo is not None else "?"
    return lo, hi, nm


def analyse_increment(path, start, pc, key):
    A = ACT[(path, start)]
    succ, bad, pcj, ents, fo, pcs = cfg((path, start))
    nd = pcj[pc]
    R = frozenset(pcj[x[2]] for x in stores[key] if x[0] == path and x[1] == start and x[3][2] != "inc")
    lo, hi, fnm = own_func(A, fo, pc)
    own = pcj.get(lo)
    body = A["ins"][bisect.bisect_left(pcs, lo if lo is not None else 0):bisect.bisect_left(pcs, hi)]
    jo = A["joffs"]
    r = dict(
        loop_any=on_cycle(succ, nd),
        loop_lit=lit_backjump(body, jo, lo, hi, pc),
        loop_rf=on_cycle(succ, nd, R),
        own_reach=own is not None and reach(succ, [own], nd),
        undom_own=own is not None and reach(succ, [own], nd, R),
        undom_any=reach(succ, ents, nd, R),
        n_resets_here=len(R), func=fnm, actor=A["actor"], bad=bad,
        # containment of the cut body, as the OV-16 review measures it
        body_out=sum(1 for p, op, imm in body if op in JMPF and imm < len(jo) and not (lo <= jo[imm] < hi)),
        body_falls=bool(body) and body[-1][1] not in STOP | UNCOND and hi <= pcs[-1])
    return r


# ---------------------------------------------------------------- C4 + C5: corpus-wide positive controls
tot_back = tot_cyc_actors = tot_unres = 0
for_example = None
for a, A in ACT.items():
    succ, bad, pcj, ents = cfg(a)[:4]
    tot_unres += bad
    ins, jo = A["ins"], A["joffs"]
    back = [(j, p, imm) for j, (p, op, imm) in enumerate(ins) if op in JMPF and imm < len(jo) and jo[imm] <= p]
    tot_back += len(back)
    if back:
        tot_cyc_actors += 1
    if for_example is None:
        for j, p, imm in back:
            # the I-register for idiom: the backward jump's target region holds `... OPLSE POPXNCJMP`
            tj = pcj.get(jo[imm])
            if tj is None:
                continue
            seg = [ins[x][1] for x in range(tj, j)]
            if any(seg[x] == 0x0F and seg[x + 1] == 0x5C for x in range(len(seg) - 1)) and on_cycle(succ, j):
                for_example = (a[0].split("/")[-1], A["actor"], own_func(A, cfg(a)[4], p)[2], "%X" % p, "%X" % jo[imm],
                               " ".join(G.OPN.get(ins[x][1], "?") for x in range(tj, min(j + 1, tj + 14))))
                break
# every increment idiom in the us copy (the control needs existence, not a corpus total)
all_inc = [(k, x) for k, lst in stores.items() for x in lst if x[3][2] == "inc" and "/us/" in x[0]]
inc_rf = []
for k, (p, s, pc, prod) in all_inc:
    succ, bad, pcj = cfg((p, s))[:3]
    R = frozenset(pcj[x[2]] for x in stores[k] if x[0] == p and x[1] == s and x[3][2] != "inc")
    if on_cycle(succ, pcj[pc], R):
        inc_rf.append((p.split("/")[-1], ACT[(p, s)]["actor"], own_func(ACT[(p, s)], cfg((p, s))[4], pc)[2],
                       "%X" % pc, k[1], "%#x" % k[2]))
check("C4 the loop detector fires on the corpus: %d backward JMP-family edges in %d of %d actors; an I-register for "
      "loop: %s" % (tot_back, tot_cyc_actors, len(ACT), for_example), tot_back > 0 and for_example is not None)
check("C4 over every `x = x + k` POPV in the us copy (%d increments), %d lie on a reset-free cycle (examples %s)"
      % (len(all_inc), len(inc_rf), inc_rf[:3]), len(inc_rf) > 0)
check("C5 every JMP-family index resolves to an instruction boundary of its actor (unresolved %d)" % tot_unres,
      tot_unres == 0)

# ---------------------------------------------------------------- the counters
FMT = {0: "<B", 1: "<b", 2: "<H", 3: "<h", 4: "<i", 5: "<f"}
WRANGE = {0: (0, 255), 1: (-128, 127), 2: (0, 65535), 3: (-32767, 32768), 4: (-2 ** 31, 2 ** 31 - 1)}


def init_value(key):
    """the declared value of a class-1 (file) variable: the image's file-variable area, header +0x38."""
    p, cls, off = key
    if cls != 1 or key not in WIDTH or WIDTH[key] not in FMT:
        return None
    sec = FILES[p][0]
    return struct.unpack_from(FMT[WIDTH[key]], sec, U32(sec, 0x38) + off)[0]


print()
detail = io.open(os.path.join(HERE, "rc5c_increments.tsv"), "w", encoding="utf-8", newline="\n")
detail.write("counter_class\tfile\tactor\tfunction\tincrement_pc\tvariable\tk\tloop_any\tloop_literal\t"
             "loop_reset_free\tundominated_own\tundominated_any\tresets_in_actor\tbody_jumps_out\tbody_falls_through\n")
sitef = io.open(os.path.join(HERE, "rc5c_sites.tsv"), "w", encoding="utf-8", newline="\n")
sitef.write("counter_class\tfile\tsite_pc\tvariable\tdeclared_value\toracle_interval\tloop_reset_free\t"
            "undominated_increment\tundominated_read\tcorrected_interval\n")
INCR = {}
written = set()
for cls in ("startscene constant+increment", "startscene increment-only", "startscene_4b3 constant+increment",
            "eventread_e8 constant+increment"):
    R_ = rows[cls]
    keys = collections.OrderedDict()
    rclos = []
    for row in R_:
        path, start, spc, key, cc, oo, pc = row
        cl = closure(key[0] if key[0] != "*" else path, key[1], key[2])
        rclos.append(cl)
        for k2 in cl:
            keys.setdefault(k2, []).append(spc)
    res = []
    for k2 in keys:
        for (p, s, pc, prod) in stores[k2]:
            if prod[2] != "inc":
                continue
            if (k2, p, s, pc) not in INCR:
                INCR[(k2, p, s, pc)] = analyse_increment(p, s, pc, k2)
            r = INCR[(k2, p, s, pc)]
            res.append((k2, p, s, pc, prod[1], r))
            if (cls, p, s, pc) not in written:
                written.add((cls, p, s, pc))
                detail.write("%s\t%s\t%s\t%s\t%X\tclass%d+%#x\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (
                    cls, p, r["actor"], r["func"], pc, k2[1], k2[2], prod[1], r["loop_any"], r["loop_lit"],
                    r["loop_rf"], r["undom_own"], r["undom_any"], r["n_resets_here"], r["body_out"], r["body_falls"]))
    C = collections.Counter()
    for k2, p, s, pc, kk, r in res:
        for t in ("loop_any", "loop_lit", "loop_rf", "undom_own", "undom_any", "body_falls"):
            C[t] += bool(r[t])
        C["body_out"] += bool(r["body_out"])
        C["not_own_reach"] += not r["own_reach"]
        C["bad"] += bool(r["bad"])
    classes = collections.Counter(k2[1] for k2 in keys)
    stems = len({(k2[0].split("/")[-1], k2[1], k2[2]) for k2 in keys})
    print("%s: %d operand sites; %d counter variables (%d distinct by file name and offset; classes %s); %d increment "
          "sites" % (cls, len(R_), len(keys), stems, dict(sorted(classes.items())), len(res)))
    print("   (a) loops: on any cycle %d; literal backward-jump span %d; on a RESET-FREE cycle %d" % (
        C["loop_any"], C["loop_lit"], C["loop_rf"]))
    print("   (b) dominance: increment reachable from its own function entry without a reset %d; from any function "
          "entry %d; own entry does not reach it %d" % (C["undom_own"], C["undom_any"], C["not_own_reach"]))
    print("   containment of the cut body: jumps out %d; falls through %d; actors with unresolved jumps %d" % (
        C["body_out"], C["body_falls"], C["bad"]))
    vstat = collections.Counter()
    for k2 in keys:
        rr = [x for x in res if x[0] == k2]
        und = [x for x in rr if x[5]["undom_any"]]
        has_reset = any(x[3][2] != "inc" for x in stores[k2])
        if any(x[5]["loop_rf"] for x in rr):
            vstat["variables with an increment on a reset-free cycle"] += 1
        if not und:
            vstat["variables: every increment dominated by a reset of the same variable in its actor"] += 1
        elif has_reset:
            vstat["variables with a reset, but some increment undominated"] += 1
        else:
            vstat["variables with no reset in scope (every increment undominated)"] += 1
    for t, v in sorted(vstat.items()):
        print("   %5d  %s" % (v, t))
    # per operand site: ORACLE's interval and the corrected one
    byk = collections.defaultdict(list)
    for x in res:
        byk[x[0]].append(x)
    S = collections.Counter()
    changed = collections.OrderedDict()
    for row, cl in zip(R_, rclos):
        path, start, spc, key, cc, oo, pc = row
        steps = [int(o[3:]) for o in oo]
        init = init_value(key)
        rr = [x for k2 in cl for x in byk.get(k2, [])]
        loop = any(x[5]["loop_rf"] for x in rr)
        uinc = any(x[5]["undom_any"] for x in rr)
        succ, bad, pcj, ents = cfg((path, start))[:4]
        allst = frozenset(pcj[x[2]] for k2 in cl for x in stores[k2] if x[0] == path and x[1] == start)
        uread = reach(succ, ents, pcj[pc], allst)
        if cc:
            olo, ohi = min(cc) + sum(x for x in steps if x < 0), max(cc) + sum(x for x in steps if x > 0)
        else:
            olo, ohi = init, (None if init is None else init + sum(x for x in steps if x > 0))
        base = set(cc) | ({init} if (init is not None and (uinc or uread or not cc)) else set())
        nlo = min(base) + sum(x for x in steps if x < 0) if base else None
        nhi = (max(base) + sum(x for x in steps if x > 0)) if base else None
        if loop:
            nhi = "fails: width clamp %d" % WRANGE.get(WIDTH.get(key), (None, None))[1]
        if key[1] == 7:     # an array operand: the 'counter' is the element index, not the value (F1 below)
            nlo = nhi = "not a counter, see F1"
        S["sites"] += 1
        S["loop"] += loop
        S["uinc"] += uinc
        S["uread"] += uread
        if (nlo, nhi) != (olo, ohi):
            S["changed"] += 1
            changed.setdefault((path.split("/")[-1], key[1], key[2], init, (olo, ohi), (nlo, nhi)), []).append(spc)
        sitef.write("%s\t%s\t%X\tclass%d+%#x\t%s\t[%s, %s]\t%d\t%d\t%d\t[%s, %s]\n" % (
            cls, path, spc, key[1], key[2], init, olo, ohi, loop, uinc, uread, nlo, nhi))
    print("   operand sites: %d; reached by an increment on a reset-free cycle %d; by an undominated increment %d; "
          "read reachable from a function entry before any store of the variable %d; interval changed %d" % (
              S["sites"], S["loop"], S["uinc"], S["uread"], S["changed"]))
    seen_stem = collections.Counter()
    for (stem, vc, vo, init, o, nw), spcs in changed.items():
        seen_stem[(stem, vc, vo, init, o, nw)] += len(spcs)
    agg = collections.Counter()
    for (stem, vc, vo, init, o, nw), nn in seen_stem.items():
        agg[(stem, vc, vo, init, o, nw)] += nn
    for (stem, vc, vo, init, o, nw), nn in sorted(agg.items(), key=lambda t: (t[0][0], t[0][2]))[:40]:
        print("      %-16s class%d+%#x declared %s: ORACLE [%s, %s] -> [%s, %s]  (%d sites, all copies)" % (
            stem, vc, vo, init, o[0], o[1], nw[0], nw[1], nn))
detail.close()
sitef.close()

# ---------------------------------------------------------------- F1: the eventread_e8 "counters" are array indices
print()
import capstone, pefile  # noqa: E402
EXE = os.path.join(DB, "..", "Tools", "work", "exe", "FFXII_TZA.exe")
pe = pefile.PE(EXE, fast_load=True)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
o = pe.get_offset_from_rva(0x00267E60 - pe.OPTIONAL_HEADER.ImageBase)
pv = {i.address: "%s %s" % (i.mnemonic, i.op_str) for i in md.disasm(pe.__data__[o:o + 0x60], 0x00267E60)}
check("F1 image: POPV's store helper 00267E60 resolves the variable first (call 00262440 at 00267E7F; the resolver "
      "pops one index per array dimension) and only then pops the value (count load / decrement / store at "
      "00267E9C / 00267EA2 / 00267EA7), so for an array POPV the stack top is the INDEX",
      pv.get(0x00267E7F) == "call 0x262440" and pv.get(0x00267E9C) == "mov ecx, dword ptr [rbx]"
      and pv.get(0x00267EA2) == "dec ecx" and pv.get(0x00267EA7) == "mov dword ptr [rbx], ecx",
      "%s / %s / %s" % (pv.get(0x00267E7F), pv.get(0x00267E9C), pv.get(0x00267EA7)))
ekeys = sorted({row[3] for row in rows["eventread_e8 constant+increment"]})
for key in ekeys:
    path = key[0]
    sec, pool, tbl = FILES[path]
    vals, idxs = set(), set()
    for p, s, pc, prod in stores[key]:
        ins = ACT[(p, s)]["ins"]
        j = [x[0] for x in ins].index(pc)
        top, below = ins[j - 1], ins[j - 2]
        idxs.add(classify(p, (G.OPN.get(top[1], ""), top[2], "push")))
        vals.add(classify(p, (G.OPN.get(below[1], ""), below[2], "push")))
    vdom = set()
    other = []
    for kind, v in vals:
        if kind == "const":
            vdom.add(v)
        elif kind == "var":
            cc, oo = domain(path, v[0], v[1])
            vdom |= cc
            other += oo or (["class%d+%#x has no POPV in scope (initial value %s)" % (
                v[0], v[1], init_value((path, v[0], v[1])))] if not cc else [])
    check("F1 bytecode %s class%d+%#x: every store pushes the value, then the index; ORACLE's resolver read the "
          "index. Indices %s; stored values %s -> operand domain %s plus %s"
          % (path.split("/")[-1], key[1], key[2], sorted(map(str, idxs)), sorted(map(str, vals)), sorted(vdom), other),
          len(stores[key]) == 4 and any(k == "var" and v[:2] == (1, 0x904) for k, v in idxs))
print("FAILS %d" % len(FAILS))
sys.exit(1 if FAILS else 0)
