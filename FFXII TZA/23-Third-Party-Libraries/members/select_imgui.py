"""select_imgui.py - EC-7 member selector for the Dear ImGui object, four link runs in 00791xxx-00798xxx
(SWE2-EC7-LIB-JSONBOX-IMGUI).

  imgui.tsv     census entries in the four runs 00791D80..00792350, 00795F10..00796180, 00796E70..007973D0 and
                00798D70..00798E90 that are joined to the ImGui object: reached from the seeds by a call or lea edge
                in either direction, with every external caller a declared static-init / teardown stub (the object is
                dormant - no live game code calls it); less A-measured entries, entries declared by another family,
                RTTI-carriers and bodies also called from other outside code.
  Upstream identity: 00791D80 is ImGuiIO::ImGuiIO() - memset 0xB88, IniFilename='imgui.ini' (01CB3990) and
                LogFilename='imgui_log.txt' (01CB39A0) stored at +0x10/+0x18, upstream default constants (DeltaTime
                1/60, IniSavingRate 5.0, MouseDoubleClickTime 0.3, MouseDoubleClickMaxDist 6.0), and the three default
                platform-callback bodies stored at +0xA0/+0xA8/+0xC0 (00796E70 / 00798D70 / 00797360). The Phyre-side
                wrapper Phyre::PFramework::PImGuiInternal::PImGuiDynamicMesh (vtable 01CB3950) is INTEGRATION evidence
                only - wrapper bodies are not upstream ImGui members.
  Edges: 00791CD0 (Phyre.Reflection ctor) / 00792350 (Phyre.Framework) bound run 1; 00795DC0 (foreign dispatch, called
                from 007A4050) / 00796180 (Phyre.Framework) bound run 2; 00796E30 (Phyre.ScriptVM) / 007973D0 (Input)
                bound run 3 with the foreign Input body 00796FC0 inside it excluded; 00798AC0 (Boundary.CrossSubsystem)
                / 00798E90 (NativeLeaf) bound run 4. The static-object ctor 00791E70 sits inside run 1 but is A-measured
                (cited interior by the middleware inventory page) and the atexit teardown stubs 008B7B30/008B7D40 are
                declared by the xc-registered teardowns family - both are convention callers, not members.
Usage: python select_imgui.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "Dear ImGui context object"          # the declaring row's name: its own row is not "declared elsewhere"
RANGES = [(0x791D80, 0x792350), (0x795F10, 0x796180), (0x796E70, 0x7973D0), (0x798D70, 0x798E90)]
INI, LOG = 0x1CB3990, 0x1CB39A0
CALLBACKS = (0x796E70, 0x798D70, 0x797360)      # lea'd into the IO at +0xA0/+0xA8/+0xC0 by 00791D80
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
assert d[off(INI):off(INI) + 10] == b"imgui.ini\0" and d[off(LOG):off(LOG) + 14] == b"imgui_log.txt\0"
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
leas = collections.defaultdict(set)
for e in span:
    for x in md.disasm(d[off(e):off(e) + sizes[e]], e):
        m = rx.search(x.op_str)
        if not m: continue
        t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if inr(t) and t in eset: leas[e].add(t)
lea_in = collections.defaultdict(set)
for f, ts in leas.items():
    for t in ts: lea_in[t].add(f)
# provenance asserts: 00791D80 lea's the two upstream default filenames and the three default callback bodies
assert INI in {x.address + x.size + int(rx.search(x.op_str).group(2), 16) for x in md.disasm(d[off(0x791D80):off(0x791D80) + sizes[0x791D80]], 0x791D80) if x.mnemonic == "lea" and rx.search(x.op_str)}
assert {t for t in CALLBACKS} <= leas[0x791D80], leas[0x791D80]
slots = collections.Counter()
rd = secs[".rdata"]
for k in range(0, rd[3] - 8, 8):
    v = struct.unpack_from("<Q", d, rd[2] + k)[0]
    if inr(v): slots[v] += 1
CONV_TAGS = ("Funclet", "Unwind", "Lifecycle", "EHCall", "StaticObjectInit", "StaticLifetime", "Teardown", "NamedRegistry")
conv = lambda f: any(t in tags.get(f, "") for t in CONV_TAGS + ("DearImGui",))   # a caller the census tags as this object's own code (e.g. its XC teardown) is a convention caller by identity, not by declaration
seeds = {e for e in span if "DearImGui" in tags.get(e, "")}
comp = set(seeds); stack = list(seeds)
while stack:                                        # the object's connected component inside the runs
    e = stack.pop()
    for nb in callees[e] | callers[e] | leas[e] | lea_in[e]:
        if inr(nb) and nb not in comp: comp.add(nb); stack.append(nb)
# Accounting state does not feed the predicate (FABLE ruling on SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, generalised;
# SWE2-EC7 2026-09-30): an A-measured body in the component is judged like any other body, and a body that passes the
# predicate is a qualifying caller for the shrink; A bodies are removed only from the OUTPUT (no double accounting).
# FABLE ruling point 3 (SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930; SWE2-EC7 2026-09-30): another family's
# declaration no longer decides qualification; such a body that passes the predicate is a qualifying node, but
# ownership stays with the declaring family - it is removed from the output and printed as a collision.
hard = lambda e: (e in rtti and slots[e] > 1) or slots[e] > 1
cand = {e for e in comp if not hard(e)}
mset = set(cand); changed = True                    # shrink: drop candidates called by an in-run body that is itself
while changed:                                      # not qualifying and not convention-owned
    changed = False
    for e in list(mset):
        if any(f not in mset and not conv(f) for f in callers[e]):
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
    elif e in comp: excl["in the connected component but called from outside the object and conventions"].append(e)
    else: excl["joined to the object by nothing"].append(e)
print("ImGui runs %s: entries %d, seeds %d, members %d" % (
    " + ".join("%08X-%08X" % r for r in RANGES), len(span), len(seeds), len(members)))
for k, v in sorted(excl.items()):
    print("  excluded %-66s %3d  %s" % (k, len(v), " ".join("%08X" % x for x in v)))
outb = collections.Counter()
for e in members:
    for t in callees[e]:
        if t not in mset: outb[t] += 1
print("control outbound targets:", " ".join("%08X(%d)" % kv for kv in sorted(outb.items())))
inz = collections.defaultdict(list)
for e in members:
    for f in callers[e]:
        if f not in mset: inz["A-measured qualifying" if f in qualifying_a else ("convention" if conv(f) else "FOREIGN")].append(f)
for k, v in inz.items():
    print("control inbound %s callers: %s" % (k, " ".join("%08X" % x for x in sorted(set(v)))))
globs = collections.Counter()
for e in members:
    for x in md.disasm(d[off(e):off(e) + sizes[e]], e):
        m = rx.search(x.op_str)
        if not m: continue
        t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
        if 0x1DF0000 <= t < 0x2F9F5B0: globs[t] += 1
print("control .data globals referenced:", " ".join("%08X(%d)" % kv for kv in sorted(globs.items())))
# positive foreign controls: the Input body inside run 3 and the declared teardown stubs must be rejected
assert 0x796FC0 not in mset and 0x796FC0 in span                # foreign body inside run 3
assert declared.get(0x8B7B30) and declared.get(0x8B7D40)        # teardown stubs are convention callers, not members
assert 0x8B7B30 not in mset and 0x8B7D40 not in mset
assert "FOREIGN" not in inz, inz.get("FOREIGN")                 # dormant: no live-code caller into the object
assert "Phyre" in tags.get(0x791CD0, "") and "Phyre" in tags.get(0x792350, "")      # run 1 edges
assert "Phyre" in tags.get(0x796180, "") and "ScriptVM" in tags.get(0x796E30, "")   # runs 2/3 edges
assert 0x795DC0 in eset and 0x795DC0 not in mset                # run 2 lower edge: foreign dispatch
assert "CrossSubsystem" in tags.get(0x798AC0, "") or "Native" in tags.get(0x798AC0, "")
assert "DearImGui" not in tags.get(0x798E90, "")                # run 4 upper edge
assert set(members) >= set(CALLBACKS) | {0x791D80, 0x792090}
assert 0x791E70 in a_set and 0x791E70 not in mset   # the static object's ctor is A-measured by the middleware
                                                  # inventory page - a convention caller of the member ctors
if "--write" in sys.argv:
    open(os.path.join(HERE, "imgui.tsv"), "w").write(
        "# Dear ImGui (ocornut) minimal context object, runs 00791D80-00792350, 00795F10-00796180, 00796E70-007973D0,"
        " 00798D70-00798E90, joined entries only - select_imgui.py\n" + "\n".join("%08X" % e for e in members) + "\n")
    print("wrote", len(members))
