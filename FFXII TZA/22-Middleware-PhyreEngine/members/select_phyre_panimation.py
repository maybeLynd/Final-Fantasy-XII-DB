"""select_phyre_panimation.py - EC-7 member selector for the PhyreEngine PAnimation module
(SWE2-EC7, 2026-09-19; pilot of FABLE-REQ-SWE2-EC7-PHYRE-PANIMATION-C, method of
select_bullet.py: namespace + span + exclusive closure, with printed controls).

  phyre-panimation.tsv   frontier census entries that are Phyre::PAnimation module
               code: vtable slot targets of classes in the Phyre::PAnimation
               namespace, PLUS bodies joined by EXCLUSIVE CLOSURE - every inbound
               reference (code call/jmp/lea, or an .rdata slot of a bound class)
               comes from members or from PAnimation-bound template bodies -
               inside the module span 005A0000 up to 005D0000 (the linker's
               PAnimation range per FABLE's phyre_runmap: PSerialization ends
               0059xxxx, PRendering begins 005Exxxx).

  Membership is derived from the image, not from methods.tsv: the selector walks
  every COL-validated vtable in .rdata itself (2,286 vtables - the same count the
  vtable-method-index page documents), decodes the TypeDescriptor's mangled class
  name, and reads each slot.

  PAnimation-bound (mangled names): a class is bound iff every '@<Module>@Phyre@'
  module mention is PAnimation or PInternal.  '.?AVPAnimationController@PAnimation
  @Phyre@@' is an own-namespace class (member seed).  '.?AV?$PMethodCallerConcrete@
  PCallerImplementation1@PCallerImplementation@PInternal@Phyre@<args>' is a bound
  TEMPLATE iff its argument modules are only PAnimation - such bodies are
  REFERRERS, never members (FABLE: the instantiations dominate the slot counts and
  are not provenance).  A body at a slot shared with a foreign-parameterised
  instantiation (005C51F0: PMethodCallerConcrete<PAnimatableComponent,...> AND
  <PPhysicsRigidBody,...>) is ICF-foreign: excluded and not a referrer either.

  Excluded: A-measured entries, entries declared by other families, ICF-foreign
  bodies, bodies with no inbound references, and anything not exclusively reached
  from the module - un-joined span frontier stays frontier.

  Positive controls asserted before writing:
   - the COL walk finds exactly 2,286 vtables (the index page's own count);
   - 005AD8F0 (PAnimatableComponent's member-registration body) leas the
     member-name strings 'm_animationClips' (00D319C8) and
     'm_animationWeightedBlenderController' (00D319E0) and calls the reflection
     helpers 006388C0 / 00632FB0;
   - 005C51F0 classifies ICF-foreign.
  Edge controls printed: census entries just below/above the span with their
  class sets (PSerialization / PRendering neighbours, not ours); outbound targets
  of members by 64KB zone; inbound non-member referrer zones; .data globals
  referenced by both members and outside code.

  Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe,
  graph/functions.tsv; needs capstone.
  Usage: python select_phyre_panimation.py [--write]
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

NAME = "Phyre PAnimation module"
LO, HI = 0x5A0000, 0x5D0000
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

# ---- image-derived vtable walk: COL-validated, as the vtable index documents ----
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

vtable_cls = {}              # vtable start -> mangled class name
vtable_of = collections.defaultdict(set)   # body entry -> class names at whose slots it sits
for k in range(8, rrs - 8, 8):
    va = rva + k
    v = rq(va)
    if not (tv <= v < tv + tn): continue          # slot 0 points into .text
    cn = col_name(rq(va - 8))
    if cn is None: continue
    vtable_cls[va] = cn
    s = va
    while s < rva + rrs - 8:
        q = rq(s)
        if q in eset: vtable_of[q].add(cn)
        elif not (tv <= q < tv + tn): break       # non-text qword ends the slot run
        s += 8
assert len(vtable_cls) == 2286, "COL walk must reproduce the index page's 2,286 vtables"

MOD = re.compile(r"@([A-Za-z_]\w*)@Phyre@")
def bound_class(c):
    """PAnimation-bound iff the class names PAnimation somewhere AND no other
    Phyre module anywhere (PInternal is the shared reflection machinery)."""
    mods = set(MOD.findall(c))
    return "PAnimation" in mods and mods <= {"PAnimation", "PInternal"}
def own_ns(c):
    """own-namespace PAnimation class: a NON-template class ('.?AV?', never
    '.?AV?$') whose qualified namespace under Phyre is PAnimation - e.g.
    '.?AVPAnimationController@PAnimation@Phyre@@'.  Template instantiations
    ('.?AV?$PClassDescriptorConcrete@VPAnimatableComponent@PAnimation@Phyre@@')
    are referrers, never seeds."""
    if not c.startswith(".?AV") or c.startswith(".?AV?$"):
        return False
    m = MOD.search(c)
    return m is not None and m.group(1) == "PAnimation"

seeds = {e for e, cs in vtable_of.items()
         if any(own_ns(c) for c in cs) and all(bound_class(c) for c in cs)}
bound_templates = {e for e, cs in vtable_of.items()
                   if cs and e not in seeds and all(bound_class(c) for c in cs)}
icf_foreign = {e for e, cs in vtable_of.items()
               if e not in seeds and e not in bound_templates
               and any("PAnimation" in c for c in cs)}
assert 0x5C51F0 in icf_foreign, "005C51F0 must classify ICF-foreign (PAnimation+PPhysics)"

def body(e): return d[off(e):off(e) + sizes[e]]
md = Cs(CS_ARCH_X86, CS_MODE_64)
rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")

# positive control: 005AD8F0 registers PAnimatableComponent's reflected members
hits_g, calls = set(), set()
for x in md.disasm(body(0x5AD8F0), 0x5AD8F0):
    m = rx.search(x.op_str)
    if m:
        hits_g.add(x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1))
    if x.mnemonic == "call":
        try: calls.add(int(x.op_str, 16))
        except ValueError: pass
assert 0xD319C8 in hits_g and 0xD319E0 in hits_g, "PAnimatableComponent member-name strings"
assert {0x6388C0, 0x632FB0} <= calls, "reflection helpers"

# inbound code references: call/jmp (whole-.text scan) + lea (decoded, all bodies)
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

span = {e for e in ents if LO <= e < HI}
# closure-source rule (see the docstring): the predicate ignores A status; A bodies that pass it are sources, not members
FAIL = {int(x, 16) for x in (os.environ.get("PHYRE_FAIL", "") + "," + (open(os.environ["PHYRE_FAIL_FILE"]).read() if os.environ.get("PHYRE_FAIL_FILE") else "")).split(",") if x.strip()}
blocked = FAIL
members = {e for e in seeds if e in span and e not in blocked}
allowed = members | bound_templates
rounds = 0
while True:
    grew = set()
    for e in span - members - bound_templates:
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

excl = collections.defaultdict(list)
for e in sorted(span):
    if e in members: continue
    if e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    elif e in icf_foreign: excl["ICF-foreign (shared with a non-PAnimation class)"].append(e)
    elif e in bound_templates: excl["PAnimation-bound template body (referrer, not member)"].append(e)
    elif e in vtable_of and not all(bound_class(c) for c in vtable_of[e]):
        excl["foreign-class vtable slot (" + sorted(c for c in vtable_of[e] if not bound_class(c))[0][:40] + ")"].append(e)
    elif not code_refs(e) and not data_refs(e): excl["no inbound references"].append(e)
    else: excl["not exclusively reached from the module"].append(e)

print("PAnimation span %08X-%08X: %d entries, %d members (%d own-ns seed slots, %d joined in %d rounds)"
      % (LO, HI, len(span), len(members), len(members & seeds), len(members - seeds), rounds))
for k, v in sorted(excl.items()):
    print("  excluded %-62s %4d  %s" % (k, len(v), " ".join("%08X" % x for x in v[:6]) + (" ..." if len(v) > 6 else "")))

# controls
outb = collections.defaultdict(set)
for e in members:
    for x in md.disasm(body(e), e):
        if x.mnemonic not in ("call", "jmp"): continue
        try: t = int(x.op_str, 16)
        except ValueError: continue
        if t in eset and not (LO <= t < HI): outb[t].add(e)
print("control outbound: %d distinct call/jmp targets outside the span, by zone:" % len(outb),
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

for e in (max(x for x in ents if x < LO), min(x for x in ents if x >= HI)):
    print("edge control %08X classes: %s" % (e, sorted(vtable_of.get(e, ["(none)"]))[:2]))

if "--write" in sys.argv:
    open(os.path.join(HERE, "phyre-panimation.tsv"), "w").write(
        "# PhyreEngine PAnimation module, span 005A0000-005D0000: Phyre::PAnimation vtable slot targets plus exclusive-closure members - select_phyre_panimation.py\n"
        + "\n".join("%08X" % e for e in sorted(members)) + "\n")
    print("wrote", len(members))
