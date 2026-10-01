"""select_jsonbox.py - EC-7 member selector for the JsonBox object in 001FExxx-00202xxx + the 002164xx helper island
(SWE2-EC7-LIB-JSONBOX-IMGUI).

  jsonbox.tsv   census entries in the two link runs 001FE0E0..00202B10 and 002161C0..00216540 that are joined to the
                JsonBox object: reached from the seeds by a call or lea edge in either direction, with every external
                caller inside the JSON client band (001Cxxxx-001Exxxx game consumers) or a declared/funclet/static-life
                convention; less A-measured entries, entries declared by another family, RTTI-carriers referenced from
                more than one table row, and bodies also called from other outside code.
  Upstream identity: RTTI names JsonBox::OutputFilter<JsonBox::VSolidusEscaper / VIndentCanceller / VIndenter>, whose
                vtables sit at 00905070 / 009050F0 / 00905170 - basic_streambuf-derived, JsonBox-specific only at slot 0
                (deleting destructors 001FF930/001FF870/001FF8D0) and slot 3 (the write overrides 002016F0/00201690/
                002016C0); slot 6 is the ICF-folded shared body 00660570 carried by hundreds of Phyre descriptor vtables
                and is NOT JsonBox. The parser error-literal pool 00904FE8-00905038 ('\\u00', 'Expected '"', got '',
                'Expected a digit, '.', 'e' or 'E', got '') is upstream JsonBox Value.cpp wording; the four bodies that
                reference it (002008F0, 00201890, 00201C40, 00201EB0) are all members.
  Edges: 001FE080 below run 1 is an A-measured Presentation.EffectFont body; 00202B10 above run 1 is foreign SIMD code
                called from outside the object; 00216160 below run 2 is A-measured; 00216540 above run 2 is declared
                PhyreCore. Foreign bodies inside the runs (e.g. the EH wrappers 001FE990/001FEA00, declared elsewhere,
                and the PhyreCore filter-policy helpers 002164D0/00216540/002165B0) are enumerated exclusions.
Usage: python select_jsonbox.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "JsonBox JSON library"          # the declaring row's name: its own row is not "declared elsewhere"
RANGES = [(0x1FE0E0, 0x202B10), (0x2161C0, 0x216540)]
VTABLES = (0x905070, 0x9050F0, 0x905170)
DTORS = {0x1FF930, 0x1FF870, 0x1FF8D0}        # vtable slot 0: deleting destructors
WRITES = {0x2016F0, 0x201690, 0x2016C0}       # vtable slot 3: the OutputFilter write() overrides
ICF_SHARED = 0x660570                         # slot 6 - folded across hundreds of Phyre descriptor vtables
POOL = (0x904FC0, 0x905070)
CLIENT = (0x1C0000, 0x1F0000)
inr = lambda a: any(lo <= a < hi for lo, hi in RANGES)
d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(n):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (0x120000 + va, vs, ro, rs)
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs: return ro + (a - va)
sizes = cd.load_functions(); ents = sorted(sizes); eset = set(ents)
tags = {}
for line in open(os.path.join(W, "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: tags[int(p[0], 16)] = p[8] if len(p) > 8 else ""
    except ValueError: pass
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and parts[0] != NAME:
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass
rtti = set()
for line in open(os.path.join(W, "rtti", "methods.tsv"), encoding="utf-8", errors="replace"):
    try: rtti.add(int(line.split("\t")[0], 16))
    except ValueError: pass
q = lambda a: struct.unpack_from("<Q", d, off(a))[0]
# upstream identity asserts: the three OutputFilter vtables carry the JsonBox slot0/slot3 bodies and shared streambuf elsewhere
for v, dtor, wr in zip(VTABLES, (0x1FF930, 0x1FF870, 0x1FF8D0), (0x2016F0, 0x201690, 0x2016C0)):
    assert q(v) == dtor and q(v + 0x18) == wr, hex(v)
    assert q(v + 0x30) == ICF_SHARED          # slot 6 folded shared body - present but never a member
    assert all(q(v + 8 * s) in DTORS or q(v + 8 * s) in WRITES or q(v + 8 * s) == ICF_SHARED or 0x808000 <= q(v + 8 * s) < 0x809000
               for s in range(15)), hex(v)    # every other slot is the shared basic_streambuf implementation
assert d[off(0x905008):off(0x905008) + 19] == b"Expected '\"', got '"        # upstream JsonBox error literal
assert d[off(0x905038):off(0x905038) + 16] == b"Expected a digit"
assert d[off(0x904FE8):off(0x904FE8) + 4] == b"\\u00"

text = secs[".text"]; to = text[2]; tn = text[3]
def owner_of(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
callers = collections.defaultdict(set); callees = collections.defaultdict(set)
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to); t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    f = owner_of(src)
    if f is None or f == t: continue
    callers[t].add(f); callees[f].add(t)
md = Cs(CS_ARCH_X86, CS_MODE_64); rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+)")
span = [e for e in ents if inr(e)]
leas = collections.defaultdict(set); vlea = set(); poolref = set()
for e in span:
    for x in md.disasm(d[off(e):off(e) + sizes[e]], e):
        m = rx.search(x.op_str)
        if not m: continue
        t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if t in VTABLES: vlea.add(e)
        if POOL[0] <= t < POOL[1]: poolref.add(e)
        if inr(t) and t in eset: leas[e].add(t)
slots = collections.Counter()
rd = secs[".rdata"]
for k in range(0, rd[3] - 8, 8):
    v = struct.unpack_from("<Q", d, rd[2] + k)[0]
    if inr(v): slots[v] += 1
CONV_TAGS = ("Funclet", "Unwind", "Lifecycle", "EHCall", "StaticObjectInit", "StaticLifetime", "Teardown", "NamedRegistry")
conv = lambda f: any(t in tags.get(f, "") for t in CONV_TAGS + ("JsonBox",))   # a caller the census tags as this object's own code (e.g. its XC teardown) is a convention caller by identity, not by declaration
client = lambda f: CLIENT[0] <= f < CLIENT[1]
# seeds: vtable constructors, RTTI slot bodies, error-literal referencers, GFZ-tagged JsonBox bodies - in the runs only
seeds = {e for e in span if e in vlea or e in poolref or e in DTORS or e in WRITES or "JsonBox" in tags.get(e, "")}
lea_in = collections.defaultdict(set)
for f, ts in leas.items():
    for t in ts: lea_in[t].add(f)
comp = set(seeds); stack = list(seeds)
while stack:                                        # the object's connected component inside the runs
    e = stack.pop()
    for nb in callees[e] | callers[e] | leas[e] | lea_in[e]:                      # call and lea edges, both directions
        if inr(nb) and nb not in comp: comp.add(nb); stack.append(nb)
# Accounting state does not feed the predicate (FABLE ruling on SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, generalised;
# SWE2-EC7 2026-09-30): an A-measured body in the component is judged like any other body, and a body that passes the
# predicate is a qualifying caller for the shrink; A bodies are removed only from the OUTPUT (no double accounting).
# FABLE ruling point 3 (SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930; SWE2-EC7 2026-09-30): another family's
# declaration no longer decides qualification; such a body that passes the predicate is a qualifying node, but
# ownership stays with the declaring family - it is removed from the output and printed as a collision.
hard = lambda e: (e in rtti and slots[e] > 1) or slots[e] > 1
cand = {e for e in comp if not hard(e)}
mset = set(cand); changed = True                    # shrink: drop candidates with an in-run caller that is itself
while changed:                                      # neither qualifying, the JSON client band, nor convention-owned
    changed = False
    for e in list(mset):
        if any(f not in mset and not client(f) and not conv(f) for f in callers[e]):
            mset.discard(e); changed = True
qualifying_a = mset & a_set
mset -= a_set
collisions = sorted(mset & set(declared))
mset -= set(declared)
print("predicate members owned by another family (collisions, not written): %d %s" % (len(collisions), " ".join("%08X" % e for e in collisions)))
print("A-measured bodies that pass the predicate (qualifying callers, stay A, not members): %d" % len(qualifying_a))
members = sorted(mset)
excl = collections.defaultdict(list)
for e in span:
    if e in mset: continue
    if e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    elif e in rtti and slots[e] > 1: excl["carries RTTI shared across %d table rows" % slots[e]].append(e)
    elif e in rtti: excl["carries RTTI (folded) - not joined"].append(e)
    elif slots[e] > 1: excl["referenced from %d .rdata slots (folded shared body)" % slots[e]].append(e)
    elif e in comp: excl["in the connected component but called from outside the object, its client and conventions"].append(e)
    else: excl["joined to the object by nothing"].append(e)
print("JsonBox runs %s: entries %d, vtable-lea %d, pool-ref %d, seeds %d, members %d" % (
    " + ".join("%08X-%08X" % r for r in RANGES), len(span), len(vlea), len(poolref), len(seeds), len(members)))
for k, v in sorted(excl.items()):
    print("  excluded %-66s %3d  %s" % (k, len(v), " ".join("%08X" % x for x in v)))
outb = collections.Counter()
for e in members:
    for t in callees[e]:
        if t not in members: outb[t] += 1
print("control outbound targets:", " ".join("%08X(%d)" % kv for kv in sorted(outb.items())))
inz = collections.defaultdict(list)
for e in members:
    for f in callers[e]:
        if f in qualifying_a: inz["A-measured qualifying"].append(f)
        elif f not in members: inz["client" if client(f) else ("convention" if conv(f) else "FOREIGN")].append(f)
for k, v in inz.items():
    print("control inbound %s callers: %s" % (k, " ".join("%08X" % x for x in sorted(set(v)))))
# positive foreign controls: known non-JsonBox bodies must be rejected
assert ICF_SHARED not in members and not inr(ICF_SHARED)   # ICF-folded Phyre slot-6 body
assert 0x2164D0 not in members and declared.get(0x2164D0)  # declared PhyreCore inside run 2
assert 0x1FEA00 not in members and declared.get(0x1FEA00)  # declared EHCallWrapper inside run 1
assert "FOREIGN" not in inz, inz.get("FOREIGN")            # no unexplained external caller
# edge asserts: the neighbours are independently identified as something else
assert 0x1FE080 in a_set                                    # below run 1: A-measured EffectFont
assert 0x202B10 in eset and 0x202B10 not in members         # above run 1: foreign SIMD
assert 0x216160 in a_set                                    # below run 2: A-measured
assert 0x216540 in declared                                 # above run 2: declared PhyreCore
assert all(inr(m) for m in members) and 0x1FE0E0 == min(members) and max(members) < 0x216540
if "--write" in sys.argv:
    open(os.path.join(HERE, "jsonbox.tsv"), "w").write(
        "# JsonBox (anhero/JsonBox) Value/Object/parser/serializer object, runs 001FE0E0-00202B10 and 002161C0-00216540,"
        " joined entries only - select_jsonbox.py\n" + "\n".join("%08X" % e for e in members) + "\n")
    print("wrote", len(members))
