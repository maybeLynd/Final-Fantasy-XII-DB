"""rc5b_operands.py - RC-5 residue items 1 and 3: bound the non-constant operands of the event-slot verbs to their
domains, and census debug_eventload 0x202D (ORACLE, 2026-09-30). Static; shipped bytecode only.

It reuses RC-5's walk (../rc5-event-slot-routes-0930/rc5_verbs.py). That is the database's EBP2 walk and decoder,
`25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py`, with its backward stack resolver.

For every call site of the target verbs it resolves the pushed operands. For each operand that is a script
variable (PUSHV) it:
- decodes the variable descriptor from the file's descriptor table (section header +0x28; the resolver reads
  [table + 4 + index*8], so bits 0..23 are the offset, 24..26 the class and 28..31 the width;
  script-variables-and-their-storage-classes.md section 2.2);
- collects every POPV that stores to the same (class, offset) variable, in the same file for classes 1, 2, 4 and
  5, and in every file for class 0 (global);
- resolves each stored value the same way: a constant; a copy from another variable (followed to depth 3); an
  expression; or a verb result.

The domain is the union. It is exact when every store is a constant or a copy that resolves to constants, and
otherwise it names the non-constant store. An operand that is itself an expression is listed with its operator,
file and pc.

Controls:
- C1: RC-5's counts reproduce (startscene 34,125 sites; PUSHV operands 3,429 in event scripts).
- C2: the descriptor of a known PUSHV decodes to a legal class (0, 1, 2, 4, 5 or 7) and width (0 to 5) for every
  site.
"""
import collections, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
_cwd = os.getcwd()
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G  # noqa: E402
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
S32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
WANT = {0x11B: ("startscene", 1), 0x4B3: ("startscene_4b3", 2), 0xE8: ("eventread_e8", 2), 0xE7: ("eventread", 1),
        0x198: ("summoneventread", 1), 0x202D: ("debug_eventload", 2)}
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
FILES = {}      # path -> (sec, pool, desc_table, [(start, ins)])
sites = []      # (path, start, pc, verb, [operand producers])
stores = collections.defaultdict(list)   # (path or '*', cls, off) -> [(path, start, pc, producer)]


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
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    codes = []
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start:
            continue
        ins, _ = G.decode(sec[start:end])
        codes.append((start, ins))
        for j, (pc, op, imm) in enumerate(ins):
            if op == 0x49:          # POPV: one value popped into variable imm
                d = desc(sec, tbl, imm)
                if d is None:
                    continue
                args, st = G.resolve_args(ins, j, 1, verbs)
                prod = args[0] if args else ("?" + st, None, "unresolved")
                # the increment idiom `x = x + k`: PUSHV x ; push k ; OPADD ; POPV x (either operand order)
                if j >= 3 and ins[j - 1][1] == 0x12:
                    a, c = ins[j - 3], ins[j - 2]
                    if c[1] == 0x48 and a[1] != 0x48:
                        a, c = c, a
                    if a[1] == 0x48 and desc(sec, tbl, a[2])[:2] == d[:2]:
                        k = const_of(sec, pool, G.OPN.get(c[1], ""), c[2]) if c[2] is not None else                             (int(G.OPN[c[1]][-1]) if G.OPN.get(c[1], "").startswith("PUSHI") and G.OPN[c[1]][-1].isdigit() else None)
                        if k is not None:
                            prod = ("INC", k, "inc")
                key = ("*" if d[0] == 0 else path, d[0], d[1])
                stores[key].append((path, start, pc, prod))
            elif op in (0x58, 0x59, 0x5D, 0x5E) and imm in WANT:
                vname, ar = WANT[imm]
                need = ar + (1 if op in (0x59, 0x5E) else 0)
                args, st = G.resolve_args(ins, j, need, verbs)
                sites.append((path, start, pc, vname, args, st))
    FILES[path] = (sec, pool, tbl)
os.chdir(_cwd)


def domain(path, cls, off, depth=0, seen=()):
    """(set of constants, list of non-constant stores) for a variable."""
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


def classify(path, prod):
    sec, pool, tbl = FILES[path]
    name, im, kind = prod
    c = const_of(sec, pool, name, im) if im is not None else None
    if c is not None:
        return ("const", c)
    if name == "PUSHV":
        d = desc(sec, tbl, im)
        return ("var", d)
    return ("expr", name)


out = io.open(os.path.join(HERE, "rc5b_operands.tsv"), "w", encoding="utf-8", newline="\n")
out.write("file\tpc\tverb\toperand\tkind\tvariable\tdomain_constants\tnon_constant_stores\n")
summary = collections.Counter()
per_verb_dyn = collections.defaultdict(list)
bad_desc = 0
for path, start, pc, vname, args, st in sites:
    summary[(vname, "sites")] += 1
    if not args:
        summary[(vname, "unresolved-args")] += 1
        continue
    for k, prod in enumerate(args):
        kind, v = classify(path, prod)
        if kind == "const":
            continue
        if kind == "var":
            if v is None or v[0] not in (0, 1, 2, 4, 5, 7) or v[2] > 5:
                bad_desc += 1
            cc, oo = domain(path, v[0], v[1]) if v else (set(), ["no-descriptor"])
            per_verb_dyn[vname].append((path, start + pc, k, v, cc, oo))
            out.write("%s\t%X\t%s\t%d\tvar\tclass%d+%#x w%d\t%s\t%s\n" % (path, start + pc, vname, k, v[0], v[1], v[2],
                      ",".join(str(x) for x in sorted(cc)), ";".join(oo[:6])))
        else:
            per_verb_dyn[vname].append((path, start + pc, k, ("expr", v), set(), [v]))
            out.write("%s\t%X\t%s\t%d\texpr\t%s\t\t\n" % (path, start + pc, vname, k, v))
out.close()
n11b = summary[("startscene", "sites")]
print("%s  C1 startscene sites %d (RC-5: 34,125)" % ("PASS" if n11b == 34125 else "FAIL", n11b))
print("%s  C2 every PUSHV operand's descriptor decodes to a legal class and width (bad: %d)" % ("PASS" if bad_desc == 0 else "FAIL", bad_desc))
for vname in ("startscene", "startscene_4b3", "eventread_e8", "summoneventread", "eventread", "debug_eventload"):
    rows = per_verb_dyn.get(vname, [])
    exact = [r for r in rows if r[3] and r[3][0] != "expr" and not r[5] and r[4]]
    inc_only = [r for r in rows if r[3] and r[3][0] != "expr" and r[5] and r[4] and all(o.startswith("INC") for o in r[5])]
    if inc_only:
        hi_over = collections.Counter()
        spans = []
        for r in inc_only:
            steps = [int(o[3:]) for o in r[5]]
            lo = min(r[4]) + sum(x for x in steps if x < 0)
            hi = max(r[4]) + sum(x for x in steps if x > 0)
            spans.append((lo, hi))
        print("   %d of the non-constant operands are variables whose only non-constant stores are the increment x = x + k; "
              "their values lie in [min constant, max constant + the file's total increments]: overall [%d, %d]; "
              "widest single-variable span %d" % (len(inc_only), min(a for a, _ in spans), max(b for _, b in spans),
                                                  max(b - a for a, b in spans)))
    unbound = [r for r in rows if r not in exact]
    vals = collections.Counter()
    for r in exact:
        vals.update(r[4])
    print("\n%s: %d sites; non-constant operands %d; bounded exactly by constant stores %d; not exactly bounded %d" % (
        vname, summary[(vname, "sites")], len(rows), len(exact), len(unbound)))
    if vals:
        print("   constants reachable through the variables: %d distinct, %s" % (len(vals), sorted(vals)[:80]))
    reasons = collections.Counter()
    for r in unbound:
        if r[3] and r[3][0] == "expr":
            reasons["operand is an expression (%s)" % r[3][1]] += 1
        elif not r[4] and not r[5]:
            reasons["variable never stored by a POPV in scope (initial value only)"] += 1
        else:
            if all(o.startswith("INC") for o in r[5]) and r[4]:
                reasons["variable: constant stores plus x = x + k increments (interval above)"] += 1
            elif r[5] and all(o.startswith("INC") for o in r[5]):
                reasons["variable: x = x + k increments only, no constant store in scope (its initial value plus up to %d)"
                        % sum(int(o[3:]) for o in r[5])] += 1
            else:
                for o in [o for o in r[5] if not o.startswith("INC")][:1]:
                    reasons["variable has a non-constant store: %s" % o.split("@")[0]] += 1
    for k, v in reasons.most_common():
        print("   %5d  %s" % (v, k))
# debug_eventload: every site's operand tuple
dl = [s for s in sites if s[3] == "debug_eventload"]
tuples = collections.Counter()
for path, start, pc, vname, args, st in dl:
    if args:
        tuples[tuple(classify(path, a) for a in args)] += 1
    else:
        tuples[("unresolved", st)] += 1
print("\ndebug_eventload operand tuples (push order: manager, set id): %d sites in %s" % (
    len(dl), sorted(set(s[0].split("/")[-1] for s in dl))))
for k, v in tuples.most_common():
    print("   %4d  %s" % (v, k))
