"""select_mkvparser.py - EC-7 member selector for the libwebm mkvparser object (SWE2-EC7, 2026-09-13).

  libwebm-mkvparser.tsv    the WebM Project libwebm Matroska/WebM parser (mkvparser.cpp and friends),
                           statically linked, not FFXII code:
                           (a) the contiguous translation-unit run 007FFBC0 up to 00808888 (exclusive),
                               ending where the import-thunk field begins, for every census entry joined
                               to the parser - reached by call or lea from the seeds inside the run, held
                               in a mkvparser class vtable, or called only by the game-side video client /
                               reader region / CRT static-teardown registrars;
                           (b) the mkvparser vtable method bodies the linker scattered outside the run
                               (006CC9F0 IMkvReader's out-of-line deleting destructor in the client region,
                               007AD440 / 007B6C40 / 007BD590 / 007E3260 among the audio bodies), each
                               carrying RTTI for a mkvparser:: class.
  Seeds: census entries tagged GFZ.V121.CodeDomain.Media.Video.WebM_MKV.*, plus every slot target of the
  eight vtables whose RTTI names a mkvparser:: class (01CC6A68 BlockEntry, 01CC6A88 SimpleBlock,
  01CC6AA8 BlockGroup, 01CC6AC8 Track::EOSBlock, 01CC6AE8 Track, 01CC6B08 VideoTrack, 01CC6B28 AudioTrack,
  00D89AE0 IMkvReader). 00861EC6 is _purecall - shared by every abstract class in the image - and is not
  a member. No mkvmuxer:: RTTI exists in the image: only the parse side of libwebm is linked.
  Boundary asserted: inbound calls only from the video client 0067xxxx, the VbfMkv reader region 006Cxxxx,
  CRT static-teardown registrars 008B905C and _Facet_Register (to the shared CRT tail 00808850,
  which is itself excluded), and the unwind funclets 008A5B30-008A5B70 that drive member destructors
  during C++ EH; outbound calls only to CRT (free/delete/memcpy, eh_vector iterators, the
  security cookie, _guard_check_icall). The game's IMkvReader implementation (VbfMkvReader, tagged
  WebM_VbfMkv.Runtime) is the client and is NOT covered.
Usage: python select_mkvparser.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "libwebm mkvparser"
LO, HI = 0x7FFBC0, 0x808888
CLIENT = ((0x670000, 0x680000), (0x6CC000, 0x6CD000))          # video client, VbfMkv reader region
REGISTRAR = ((0x8A0000, 0x8B0000), (0x8B0000, 0x8C0000))      # CRT static-teardown registrar regions
inr = lambda a: LO <= a < HI
IBV = 0x120000                              # image base already folded into the section VAs below
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

# mkvparser vtable slot targets, split by whether they sit inside the contiguous run
vt_in, vt_out, vclasses = set(), set(), {}
for line in open(os.path.join(W, "rtti", "vtables.tsv"), encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    if len(p) < 4 or not p[1].startswith("mkvparser::"): continue
    try: t = int(p[3], 16)
    except ValueError: continue
    vclasses[t] = p[1]
    (vt_in if inr(t) else vt_out).add(t)
PURECALL = 0x861EC6
vt_in.discard(PURECALL); vt_out.discard(PURECALL)
assert PURECALL in vt_out or PURECALL not in vt_in  # documented, never a member

def owner_of(a):
    i = bisect.bisect_right(ents, a) - 1
    if i >= 0 and ents[i] <= a < ents[i] + max(sizes[ents[i]], 1): return ents[i]
callers = collections.defaultdict(set); callees = collections.defaultdict(set)
callsrcs = collections.defaultdict(set)   # target entry -> raw E8/E9 source addresses
text = secs[".text"]; to, tn = text[2], text[3]
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to); t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    callsrcs[t].add(src)   # the E8/E9 exists whether or not its bytes sit inside a census extent
    f = owner_of(src)      #   (the unwind funclets at 008A5B30-77 live in a gap between entries)
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
seeds = {e for e in span if "WebM_MKV" in tags.get(e, "")} | (vt_in & eset)
# membership flows downstream: a member's callees and lea targets are its helpers. A body that is
# only a CALLER of a member is outside code calling in. (The five EH unwind-action destructor
# bodies 007FFCD0/007FFD00/007FFD80/007FFDA0/00800150 were first excluded under this note on a
# WRONG frame attribution - the RVA32 EH tables that drive them belong to member frames, so the
# post-pass below admits them; see FABLE-ADJ-MKV.)
reached = set(seeds); stack = list(seeds)
while stack:
    e = stack.pop()
    for nb in callees[e] | leas[e]:
        if inr(nb) and nb not in reached: reached.add(nb); stack.append(nb)
def in_client(f): return any(a <= f < b for a, b in CLIENT)
def in_registrar(f): return any(a <= f < b for a, b in REGISTRAR)
# public-API surface: in-run bodies called only by the game client. These are members the
# reachability seeds cannot see (called through the interface, never from inside), and seeding the
# downstream walk with them pulls in the private helpers only they use (e.g. 00803230, the parse
# pump called twice by API body 00803190). A registrar-zone caller does NOT admit: 008087C4 is the
# destructor called by ~_Fac_tidy_reg_t (008B905C, CRT locale cleanup) and is MSVC runtime code the
# linker emitted inside the run - a registrar caller must not disqualify a member, but only a
# client caller can admit one.
api = {e for e in span
       if e not in reached
       and {f for f in callers[e] if not inr(f)}
       and all(in_client(f) for f in callers[e] if not inr(f))}
stack = list(api); reached |= api
while stack:
    e = stack.pop()
    for nb in callees[e] | leas[e]:
        if inr(nb) and nb not in reached: reached.add(nb); stack.append(nb)
members, excl = [], collections.defaultdict(list)
for e in span:
    out_callers = {f for f in callers[e] if not inr(f)}
    ok_callers = all(in_client(f) or in_registrar(f) for f in out_callers)
    joined = e in reached or e in vt_in
    if e in a_set: excl["A-measured"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    elif e in vclasses and not vclasses[e].startswith("mkvparser::"): excl["RTTI for " + vclasses[e][:40]].append(e)
    elif sizes[e] <= 6 and d[off(e):off(e) + 2] == b"\xff\x25": excl["import thunk"].append(e)
    elif not ok_callers: excl["called from outside client/registrar: " + " ".join("%08X" % f for f in sorted(out_callers)[:3])].append(e)
    elif not joined and not (out_callers and all(in_client(f) for f in out_callers)):
        excl["joined to the parser by nothing"].append(e)
    else: members.append(e)
# Accounting state does not feed the predicate (FABLE ruling on SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, generalised;
# SWE2-EC7 2026-09-30): an A-measured body that passes the same tests a member passes is a qualifying parser frame for the
# unwind closure below; it stays A and is never written as a member.
def _passes(e):
    out_callers = {f for f in callers[e] if not inr(f)}
    if e in vclasses and not vclasses[e].startswith("mkvparser::"): return False
    if sizes[e] <= 6 and d[off(e):off(e) + 2] == bytes((0xFF, 0x25)): return False
    if not all(in_client(f) or in_registrar(f) for f in out_callers): return False
    return (e in reached or e in vt_in) or bool(out_callers and all(in_client(f) for f in out_callers))
# FABLE ruling point 3 (SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930; SWE2-EC7 2026-09-30): another family's
# declaration no longer decides qualification; such a body that passes the predicate is a qualifying node, but
# ownership stays with the declaring family - it is removed from the output and printed as a collision.
qual_a = {e for e in span if (e in a_set or e in declared) and _passes(e)}
print("A-measured bodies that pass the predicate (qualifying frames, stay A, not members): %d" % len(qual_a))

# C++ exception-unwind closure (T2 repair, FABLE-ADJ-MKV 2026-09-13): a body reached ONLY through
# an unwind funclet of a member frame is a member. The chain is mechanical: .pdata
# RUNTIME_FUNCTION -> UNWIND_INFO (flags = byte>>3; EHANDLER/UHANDLER carry handler + handler_data;
# CHAININFO embeds a secondary RUNTIME_FUNCTION) -> handler_data FuncInfo (magic 0x19930522;
# __GSHandlerCheck_EH frames may point at the FuncInfo directly) -> unwind map action RVA ->
# funclet 'lea rcx,[rdx+off]; jmp body'. The owner frame of a chained secondary range is the
# census entry containing its begin. 007FFCD0/007FFD00/007FFD80/007FFDA0/00800150 join this way:
# their funclets' FuncInfos (01CC6880/858/830/8A8/8D0) hang off member frames 008041F0, 00804860,
# 00804BE0, 00804CF0 and 00807650 (the last under __GSHandlerCheck_EH) - they are the parser's own
# member destructors driven during unwind, not foreign code.
funcinfo_frame = {}
pd = secs[".pdata"]
for o in range(pd[2], pd[2] + pd[3] - 12, 12):
    b, e_, u = struct.unpack_from("<III", d, o)
    if not (0 < b < e_) or u == 0: continue
    uo = off(IBV + u)
    if uo is None: continue
    bcur = b; depth = 0
    while True:
        flags = d[uo] >> 3
        p = uo + ((4 + d[uo + 2] * 2 + 3) & ~3)
        if flags & 3:
            hdata = IBV + struct.unpack_from("<I", d, p + 4)[0]
            fo = off(hdata)
            if fo is not None and struct.unpack_from("<I", d, fo)[0] != 0x19930522:
                # GS handler-data layout: {cookie offset, FuncInfo rva}
                hdata = IBV + struct.unpack_from("<I", d, fo + 4)[0]
                fo = off(hdata)
            if fo is not None and struct.unpack_from("<I", d, fo)[0] == 0x19930522:
                f = owner_of(IBV + bcur)
                if f is not None: funcinfo_frame[hdata] = f
            p += 8
        if not flags & 4 or depth > 8: break
        depth += 1
        cb, ce, cu = struct.unpack_from("<III", d, p)
        uo = off(IBV + cu)
        if uo is None: break
        bcur = cb
funclet_frame = {}
for fi, fr in funcinfo_frame.items():
    fo = off(fi); mx, um = struct.unpack_from("<iI", d, fo + 4)
    umo = off(IBV + um)
    if umo is None or not (0 < mx < 64): continue
    for i in range(mx):
        act = struct.unpack_from("<I", d, umo + i * 8 + 4)[0]
        if act: funclet_frame[IBV + act] = fr
fstarts = sorted(funclet_frame)
def unwind_owned(e):
    # every raw E8/E9 source reaching e must be the jmp of a member-frame funclet
    if not callsrcs[e]: return False
    for s in callsrcs[e]:
        i = bisect.bisect_right(fstarts, s) - 1
        if i < 0: return False
        f = fstarts[i]
        if s - f >= 0x10 or (funclet_frame[f] not in members and funclet_frame[f] not in qual_a): return False
        fo = off(f)
        if fo is None or d[fo:fo + 2] != b"\x48\x8d" or d[off(s)] != 0xE9: return False
    return True
moved = [e for k, v in excl.items() for e in v if e not in a_set and e not in declared and unwind_owned(e)]
for e in moved:
    for k in list(excl):
        if e in excl[k]: excl[k].remove(e)
    members.append(e)
excl = {k: v for k, v in excl.items() if v}
if moved:
    print("  unwind-funclet members %3d  %s" % (len(moved), " ".join("%08X" % e for e in moved)))
print("mkvparser run %08X-%08X: entries %d, seeds %d, reached %d, members %d" % (LO, HI, len(span), len(seeds), len(reached), len(members)))
for k, v in sorted(excl.items()):
    print("  excluded %-70s %3d  %s" % (k[:70], len(v), " ".join("%08X" % x for x in v)))
scattered = sorted(vt_out & eset)
for e in scattered:
    print("  scattered member %08X  %s" % (e, vclasses.get(e, "?")))
blocked = [e for e in scattered if e in a_set or e in declared]
if blocked: print("  scattered members blocked (A/declared):", ["%08X" % e for e in blocked])
outb = collections.Counter()
for e in members:
    for t in callees[e]:
        if not inr(t): outb[t] += 1
print("control outbound targets:", " ".join("%08X(%d)" % kv for kv in sorted(outb.items())))
print("control inbound caller zones:", dict(collections.Counter("%04X" % (f >> 16) for e in members for f in callers[e] if not inr(f))))
all_members = sorted(set(members) | (set(scattered) - set(blocked)))
if "--write" in sys.argv:
    open(os.path.join(HERE, "libwebm-mkvparser.tsv"), "w").write(
        "# libwebm mkvparser - run 007FFBC0-00808888 joined entries plus RTTI-scattered vtable bodies - select_mkvparser.py\n"
        + "\n".join("%08X" % e for e in all_members) + "\n")
    print("wrote", len(all_members))
