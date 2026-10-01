"""sd65_members.py - SD-65 part 2 (OPUS, 2026-09-30): for the classes that declare members in shipped files but have
no row in phyre-field-schema.tsv (sd65_census.out), is each declared (class, member) registered statically by this
build, through any of the five member routes (00632960 plain, 00632A10 array, 00632A70, 00632BE0, 00632B30 dynamic)?

Corpus side: every distinct member-name list those classes declare across FFXII_TZA.vbf.
Image side (certified exe via retool.py's reference cache): a (class, member) is registered when a route call passes
the member's name string in r9 (the CW-3 resolver form) and either (D) one of the class's descriptor globals in rdx -
a global is the class's when it is passed in rcx to a function that references the class's name - or (S) sits in a
function that itself references the class's name. Controls: two schema rows resolve.
"""
import collections, json, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import retool as T  # noqa: E402
import vbfextract  # noqa: E402

CEN = json.load(open(os.path.join(HERE, "sd65_census.json")))["classes"]
CLASSES = [c for c, v in CEN.items() if max(int(k) for k in v["members"]) > 0]   # every class a file gives members
ROUTES = {0x00632960: "plain", 0x00632A10: "array", 0x00632A70: "00632A70", 0x00632BE0: "00632BE0", 0x00632B30: "dynamic"}

# corpus: the member names each class declares (every distinct list)
f = open(r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf", "rb")
names, blocks = vbfextract.load_index(f)
decl = collections.defaultdict(collections.Counter)
for p in (n for n in names if n.lower().endswith(".phyre")):
    d = vbfextract.read_entry(f, names, blocks, p)
    hsz, nssz = struct.unpack_from("<II", d, 4)
    ns = d[hsz:hsz + nssz]
    nT, nC, nM, _ = struct.unpack_from("<IIII", ns, 8)
    coff = 0x20 + 4 * nT
    moff = coff + 36 * nC
    poff = moff + 24 * nM
    nm = lambda o: ns[poff + o:ns.index(b"\0", poff + o)].decode("latin-1")
    mi = 0
    for c in range(nC):
        w = struct.unpack_from("<9I", ns, coff + 36 * c)
        cn = nm(w[2])
        if cn in CLASSES:
            decl[cn][tuple(nm(struct.unpack_from("<6I", ns, moff + 24 * (mi + q))[0]) for q in range(w[3]))] += 1
        mi += w[3]

# image: string addresses, their referencing functions, and the route calls with the member name before them
exe = open(os.path.join(T.DB, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", exe, 0x3C)[0]
nsec, opt = struct.unpack_from("<H", exe, pe + 6)[0], struct.unpack_from("<H", exe, pe + 20)[0]
secs = [struct.unpack_from("<IIII", exe, pe + 24 + opt + i * 40 + 8) for i in range(nsec)]


def strva(s):
    out, key, i = [], b"\0" + s.encode() + b"\0", 0
    while True:
        i = exe.find(key, i)
        if i < 0:
            return out
        for vs, va, rs, ro in secs:
            if ro <= i + 1 < ro + rs:
                out.append(0x120000 + va + i + 1 - ro)
        i += 1


c, SZ = T.scan(), T.sizes()


def fns_ref(s):
    return set(fn for a in strva(s) for fn, _, _ in c["refs"].get(a, ()))


def lea_target(i):
    return i.address + i.size + int(i.op_str.split("+ ")[1].rstrip("]"), 0) if "[rip + " in i.op_str else None


def back(fn, site, n):
    ins = [i for i in T.R.md.disasm(T.R.at(fn, SZ.get(fn, 0x400)), fn) if i.address < site]
    return ins[-n:]


PRIM = {"I": "PUInt32", "H": "PInt32", "M": "float", "E": "PUInt8", "PEAE": "PUInt8 *", "PEBE": "PUInt8 *",
        "VPQWord": "PUInt128"}


def element(mangled):
    """the element type of a schema template row's class column, e.g. '$07::Phyre::PAnimation::PEAVPAnimationChannel'
    -> 'PAnimationChannel *', 'I$03' -> 'PUInt32', '$0BA::Phyre::VPQWord' -> 'PUInt128'"""
    last = mangled.split("::")[-1].split("$")[0]
    if last in PRIM:
        return PRIM[last]
    for pre, suf in (("PEAV", " *"), ("PEBV", " *"), ("PEAU", " *"), ("PEBU", " *"), ("V", ""), ("U", "")):
        if last.startswith(pre):
            return last[len(pre):] + suf
    return None


TEMPLATE = collections.defaultdict(set)   # "PArray<T>" -> descriptor globals from phyre-field-schema.tsv
TEMPLATE_FN = collections.defaultdict(set)   # "PArray<T>" -> the registrar functions (schema column 'caller')
for l in open(os.path.join(HERE, "..", "..", "..", "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata",
                           "phyre-field-schema.tsv"), encoding="utf-8"):
    p = l.rstrip("\r\n").split("\t")
    if len(p) > 6 and p[0] in ("PArray", "PSharray"):
        e = element(p[1].split("::V?$P")[0])
        if e:
            TEMPLATE["%s<%s>" % (p[0], e)].add(int(p[6], 16))
            TEMPLATE_FN["%s<%s>" % (p[0], e)].add(int(p[9], 16))


def descriptors(cn):
    """descriptor globals of cn: for a template instantiation, the schema rows' class_obj for the same element type;
    otherwise the `lea rcx, [rip+G]` before each call to a function that references cn's name"""
    if cn in TEMPLATE:
        return set(TEMPLATE[cn])
    out = set()
    for ctor in fns_ref(cn):
        for fn, site in c["calls"].get(ctor, ()):
            for i in reversed(back(fn, site, 8)):
                if i.mnemonic == "lea" and i.op_str.startswith("rcx, [rip"):
                    out.add(lea_target(i))
                    break
    return out


ROUTE_SITES = []   # (route, site, function, descriptor G or None, name address or None)
for r in ROUTES:
    for fn, site in sorted(c["calls"].get(r, ())):
        g = nmva = None
        for i in reversed(back(fn, site, 14)):
            if g is None and i.mnemonic == "lea" and i.op_str.startswith("rdx, [rip"):
                g = lea_target(i)
            if nmva is None and i.mnemonic == "lea" and i.op_str.startswith("r9, [rip"):
                nmva = lea_target(i)
        ROUTE_SITES.append((ROUTES[r], site, fn, g, nmva))


def registered(cn, m):
    """form D: a route call passing one of cn's descriptor globals in rdx and the member name in r9;
    form S: a route call with the member name in r9 inside a function that references cn's name string (the struct and
    matrix types register their members next to their own name)"""
    ds, mv, own = descriptors(cn), set(strva(m)), fns_ref(cn)
    hit = [("D " + r, a, fn) for r, a, fn, g, nv in ROUTE_SITES if g in ds and nv in mv]
    hit = hit or [("S " + r, a, fn) for r, a, fn, g, nv in ROUTE_SITES if fn in own and nv in mv]
    # form T: a template instantiation passes its descriptor in a register; the route call sits in the registrar the
    # schema names for that instantiation
    return hit or [("T " + r, a, fn) for r, a, fn, g, nv in ROUTE_SITES if fn in TEMPLATE_FN.get(cn, ()) and nv in mv], ds


# control: two schema rows resolve through this join
ctl_fail = 0
for cn, m in (("PClusterHeaderBase", "m_size"), ("PLight", "m_color")):
    hit, _ = registered(cn, m)
    ctl_fail += 0 if hit else 1
    print("control %s::%s -> %s" % (cn, m, "PASS" if hit else "FAIL"))


rows = []
print("\n-- the classes with no row in phyre-field-schema.tsv, in full --")
for cn in sorted(decl, key=lambda x: (CEN[x]["static"], x)):
    for mlist, n in decl[cn].items():
        for m in mlist:
            hits, regs = registered(cn, m)
            rows.append((cn, m, n, hits))
            if CEN[cn]["static"] and hits:
                continue
            print("%-48s %-28s files %5d  %s" % (cn, m, n, ", ".join("%s @%08X in %08X" % h for h in hits) or
                                                  "NOT REGISTERED against descriptor(s) %s" % ["%08X" % x for x in sorted(regs)]))
un = [r for r in rows if not r[3]]
print("\n(the classes with schema rows print only unresolved pairs)")
nr = [r for r in rows if not CEN[r[0]]["static"]]
print("no-row classes: %d pairs, %d registered" % (len(nr), sum(1 for r in nr if r[3])))
print("all file-declared (class, member) pairs over %d classes: %d; registered statically (form D, S or T): %d; not: %d"
      % (len(decl), len(rows), len(rows) - len(un), len(un)))
print("FAILS %d" % (ctl_fail + len(un)))
