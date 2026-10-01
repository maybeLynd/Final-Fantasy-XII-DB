"""select_phyre_module.py MODULE [--write] - EC-7 member selector for one
PhyreEngine module (SWE2-EC7, 2026-09-16; generalises the PAnimation pilot
select_phyre_panimation.py for FABLE-REQ-SWE2-EC7-PHYRE-MODULES-AFTER-PILOT).

Members = frontier census entries that are Phyre::<MODULE> module code:

  * SEEDS - bodies sitting at a vtable slot of an own-namespace
    Phyre::<MODULE> class (non-template mangled name whose first
    '@<module>@Phyre@' mention is MODULE), with every class at that body's
    slots MODULE-bound;
  * CLOSURE - bodies whose every inbound reference (call/jmp/lea anywhere in
    .text, or an .rdata slot of a bound class) comes from members or from
    MODULE-bound template referrers, iterated to a fixpoint.

The linker does NOT give most modules a contiguous span (PAnimation was the
exception): PRendering slot targets sit inside 005Cxxxx beside PAnimation's,
Phyre core slot targets appear in nearly every 64KB bucket. Membership
therefore carries no geographic bound; exclusivity does the work, and the
geography is printed as a control.

MODULE-bound (mangled names): a class is bound iff every '@<m>@Phyre@' module
mention is MODULE or PInternal (the shared reflection machinery). For MODULE
'PhyreCore' the rule is every mention is PInternal (core classes like
'.?AVPWorld@Phyre@@' carry no module segment at all). Non-template bound
classes are seeds; template instantiations ('.?AV?$...') are REFERRERS, never
members - FABLE: the instantiations dominate slot counts and are not
provenance. A body at a slot shared with a foreign-parameterised
instantiation is ICF-foreign: excluded, and not a referrer either.

Excluded: A-measured entries, entries declared by other families, ICF-foreign
bodies, bodies with no inbound references, and anything not exclusively
reached from the module - un-joined frontier stays frontier.

Controls asserted before writing: the COL walk finds exactly 2,286 vtables
(the vtable-method-index page's own count). Printed: member geography by 64KB
zone, outbound call/jmp targets by zone, inbound non-member referrer zones,
.data globals shared with non-member code, and the largest foreign-class
bodies sitting inside the densest member bucket.

Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe,
graph/functions.tsv; needs capstone.
CLOSURE SOURCES AND ACCOUNTING STATE (FABLE ruling, SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, applied
2026-09-30 by SWE2-EC7). Module identity and evidence accounting are separate properties. The seed and closure
predicate is evaluated IGNORING A status: an A-measured body that passes the same predicate a member passes (seed
slot, or every inbound reference from qualifying bodies) is a closure source for its callees, but it stays A and is
never written as a member (no double accounting). Being A alone never qualifies a body. Without this, re-statusing a
page DOCUMENTED shrank a module family by cascade (2026-09-30: PAnimation -75, PPostProcessing -18). The same holds
for bodies another family declares (FABLE ruling on SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930, point 3): for the
closure a body counts as a module member by the predicate whichever family declared it, but ownership stays with the
declaring family - it is never written here (the collisions are printed). Derived families (accounting-defined) are
never closure inputs here: the predicate does not read any family's membership. Control hook: PHYRE_FAIL=<hex,hex,...> (or
PHYRE_FAIL_FILE=<file of the same>) forces the named bodies to fail the predicate (the ruling's mutation control);
unset in normal runs."""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

MODULE = sys.argv[1]
NAME = "Phyre %s module" % MODULE
IMG = 0x120000

d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(n):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (0x120000 + va, vs, ro, rs)
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs: return ro + (a - va)
def rq(a):
    return struct.unpack_from("<Q", d, off(a))[0]
sizes = cd.load_functions(); ents = sorted(sizes); eset = set(ents)
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and parts[0] != NAME:
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass

tv, tsz, to, tn = secs[".text"]
rva, rvs, rro, rrs = secs[".rdata"]

# ---- image-derived vtable walk: COL-validated -------------------------------
def col_name(colva):
    o = off(colva)
    if o is None or o + 24 > len(d): return None
    sig, offv, cdo, ptd, pcd, pself = struct.unpack_from("<6I", d, o)
    if sig != 1 or pself + IMG != colva: return None
    to_ = off(ptd + IMG)
    if to_ is None: return None
    raw = d[to_ + 0x10:to_ + 0x160].split(b"\0")[0]
    if not raw.startswith(b".?"): return None
    return raw.decode("utf-8", "replace")

vtable_cls = {}
vtable_of = collections.defaultdict(set)
for k in range(8, rrs - 8, 8):
    va = rva + k
    v = rq(va)
    if not (tv <= v < tv + tn): continue
    cn = col_name(rq(va - 8))
    if cn is None: continue
    vtable_cls[va] = cn
    s = va
    while s < rva + rrs - 8:
        q = rq(s)
        if q in eset: vtable_of[q].add(cn)
        elif not (tv <= q < tv + tn): break
        s += 8
assert len(vtable_cls) == 2286, "COL walk must reproduce the index page's 2,286 vtables"

MOD = re.compile(r"@([A-Za-z_]\w*)@Phyre@")
# Phyre module namespaces - the fifteen registered PUtility modules PLUS the
# four that register no PUtility object but own their own RTTI namespace
# (PFramework, PGameplay, PVision, PProfiling).  Everything else under
# @X@Phyre@ - PInternal, the VP*/PE* reflection and nested-class encodings,
# single-letter template parameters - is core machinery, not a module.
MODULES = {"PSerialization", "PScene", "PAnimation", "PRendering", "PPostProcessing",
           "PGeometry", "PScripting", "PPhysics", "PDynamicGeometry", "PLOD",
           "PInputs", "PGame", "PHierarchy", "PDeveloperExtensions", "PText",
           "PFramework", "PGameplay", "PVision", "PProfiling"}
CORE = MODULE == "PhyreCore"
def bound_class(c):
    mods = set(MOD.findall(c))
    if CORE:
        # core = Phyre-namespace classes in NO module: 'Phyre::PWorld' has no
        # module segment; 'Phyre::PWorld::PWorldBullet' mentions PWorld, which
        # is a core sub-namespace, not a module.  Any module mention is foreign.
        return not mods & MODULES
    return MODULE in mods and mods <= {MODULE, "PInternal"}
def own_ns(c):
    if not c.startswith(".?AV") or c.startswith(".?AV?$"):
        return False
    if CORE:
        # must actually live under @Phyre@ (a plain '.?AVFoo@@' global class is
        # not Phyre at all), with no module namespace mention
        return "@Phyre@" in c and all(x not in MODULES for x in MOD.findall(c))
    m = MOD.search(c)
    return m is not None and m.group(1) == MODULE

seeds = {e for e, cs in vtable_of.items()
         if any(own_ns(c) for c in cs) and all(bound_class(c) for c in cs)}
bound_templates = {e for e, cs in vtable_of.items()
                   if cs and e not in seeds and all(bound_class(c) for c in cs)}
icf_foreign = {e for e, cs in vtable_of.items()
               if e not in seeds and e not in bound_templates
               and any(MODULE in c for c in cs)}

def body(e): return d[off(e):off(e) + sizes[e]]
md = Cs(CS_ARCH_X86, CS_MODE_64)
rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")

# inbound code references: call/jmp (whole-.text scan) + lea (decoded)
def owner(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
callers = collections.defaultdict(set)
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = tv + (o - to); t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    f = owner(src)
    if f is None or f == t: continue
    callers[t].add(f)
lea_refs = collections.defaultdict(set)
for e in ents:
    if e < 0x121000 or e >= 0x8C2000 or sizes[e] <= 0: continue
    for x in md.disasm(body(e), e):
        if x.mnemonic != "lea": continue
        m = rx.search(x.op_str)
        if not m: continue
        g = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if g in eset and g != e: lea_refs[g].add(e)

def code_refs(e): return callers.get(e, set()) | lea_refs.get(e, set())
def data_refs(e): return vtable_of.get(e, set())

# closure-source rule (see the docstring): the predicate ignores A status; A bodies that pass it are sources, not members
# EXCEPT PhyreCore: its predicate has no geography and no namespace segment, so without the A/declared firewall the
# closure runs into game code (sample read 2026-09-30: FFXII movement, battle-menu and 28 KB presentation bodies among
# the +988). Per the ruling a misfit stops that family's admission: PhyreCore keeps the firewall until its predicate
# is repaired (record ec7-phyre-uniform-0930).
FIREWALL = (MODULE == "PhyreCore")
FAIL = {int(x, 16) for x in (os.environ.get("PHYRE_FAIL", "") + "," + (open(os.environ["PHYRE_FAIL_FILE"]).read() if os.environ.get("PHYRE_FAIL_FILE") else "")).split(",") if x.strip()}
blocked = FAIL | ((set(declared) | a_set) if FIREWALL else set())
members = {e for e in seeds if e not in blocked}
allowed = members | bound_templates
rounds = 0
while True:
    grew = set()
    for e in eset - members - bound_templates:
        if e in blocked or e in icf_foreign: continue
        refs = code_refs(e)
        drs = data_refs(e)
        if not refs and not drs: continue
        if refs <= allowed and all(bound_class(c) for c in drs):
            grew.add(e)
    if not grew: break
    members |= grew; allowed |= grew; rounds += 1
promoted_sources = members & a_set      # qualify ignoring A: closure sources only
collisions = sorted((members - a_set) & set(declared))
members -= a_set
members -= set(declared)                # ownership stays with the declaring family
print("closure sources that are A-measured (qualify, stay A, not members): %d" % len(promoted_sources))
print("predicate members owned by another family (collisions, not written): %d" % len(collisions))
for e in collisions: print("  collision %08X  owned by %s" % (e, declared[e][:60]))
if os.environ.get("PHYRE_SOURCES_OUT"):
    TAB, NL = chr(9), chr(10)
    with open(os.path.join(os.environ["PHYRE_SOURCES_OUT"], "%s-sources.tsv" % NAME.replace(" ", "_")), "w") as _f:
        _f.write("address" + TAB + "role" + TAB + "owner" + NL)
        for e in sorted(promoted_sources): _f.write("%08X" % e + TAB + "A-measured closure source" + TAB + NL)
        for e in collisions: _f.write("%08X" % e + TAB + "predicate member owned elsewhere" + TAB + declared[e] + NL)

# exclusion census over the module's own reach (any entry with a bound class
# slot or exclusively-reachable candidate that stayed out)
print("Phyre %s module: %d members (%d own-ns seed slots, %d joined in %d rounds)"
      % (MODULE, len(members), len(members & seeds), len(members - seeds), rounds))
print("  seeds total (any disposition): %d   bound-template referrers: %d   ICF-foreign: %d"
      % (len(seeds), len(bound_templates), len(icf_foreign)))

# member geography control
geo = collections.Counter("%04X" % (e >> 16) for e in members)
print("control geography (members by 64KB zone):", dict(sorted(geo.items())))

outb = collections.defaultdict(set)
for e in members:
    for x in md.disasm(body(e), e):
        if x.mnemonic not in ("call", "jmp"): continue
        try: t = int(x.op_str, 16)
        except ValueError: continue
        if t in eset and t not in members: outb[t].add(e)
print("control outbound: %d distinct call/jmp targets to non-members, by zone:" % len(outb),
      dict(collections.Counter("%04X" % (t >> 16) for t in outb)))
inb = collections.Counter()
for e in members:
    for f in code_refs(e):
        if f not in members and f not in bound_templates: inb["%04X" % (f >> 16)] += 1
print("control inbound non-member referrer zones:", dict(inb))
DATA = secs[".data"]; shared = collections.defaultdict(set)
for e in members:
    for x in md.disasm(body(e), e):
        m = rx.search(x.op_str)
        if not m: continue
        g = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if DATA[0] <= g < DATA[0] + DATA[1]: shared[g].add(e)
gref = collections.defaultdict(set)
for e in ents:
    if e < 0x121000 or e >= 0x8C2000 or sizes[e] <= 0 or e in members: continue
    for x in md.disasm(body(e), e):
        m = rx.search(x.op_str)
        if not m: continue
        g = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if g in shared: gref[g].add(e)
print("control globals: member-referenced .data cells also touched outside: %d" % len(gref))
for g, fs in sorted(gref.items())[:10]:
    print("    %08X  outside zones %s" % (g, sorted({"%04X" % (f >> 16) for f in fs})))

# edge control: foreign-class vtable bodies inside the densest member bucket
if members:
    dense = max(geo, key=geo.get)
    fore = [e for e in vtable_of
            if (e >> 16) == int(dense, 16) and e not in members
            and not all(bound_class(c) for c in vtable_of[e])]
    print("edge control: %d foreign-class vtable bodies inside densest bucket %sxxxx: %s"
          % (len(fore), dense, " ".join("%08X" % x for x in sorted(fore)[:8])))

if "--write" in sys.argv:
    out = os.path.join(HERE, "phyre-%s.tsv" % MODULE.lower())
    open(out, "w").write(
        "# PhyreEngine %s module: Phyre::%s vtable slot targets plus exclusive-closure members - select_phyre_module.py %s\n"
        % (MODULE, MODULE, MODULE)
        + "\n".join("%08X" % e for e in sorted(members)) + "\n")
    print("wrote", len(members))
