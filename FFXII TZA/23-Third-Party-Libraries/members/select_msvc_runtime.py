"""select_msvc_runtime.py - EC-7 member selector for the statically linked MSVC runtime tail
(SWE2-EC7-LIB-MSVC-RUNTIME, 2026-09-13).

  msvc-runtime-tail.tsv    the vcruntime/CRT startup block, the CRT math cluster, ATL residue and
                           the stdio COMDAT wrappers the linker placed at the end of .text:
                           (a) the contiguous runtime block 00808900 up to 0080C5A0 (exclusive):
                               __scrt_* startup/lock bodies, the security-cookie / GS-handler
                               bodies, _Init_thread_* condition-variable support, eh_vector
                               iterators, the __isa_available-gated math dispatch and its SSE/libm
                               kernels, and the ATL CAtlBaseModule trio at the end;
                           (b) two CRT bodies the linker emitted inside the libwebm mkvparser run:
                               008087C4 _Fac_tidy_reg_t's scalar deleting destructor (sole caller
                               ~_Fac_tidy_reg_t 008B905C, MSVC locale-tidy) and 00808850
                               _Facet_Register;
                           (c) the COMDAT stdio wrappers emitted among game code elsewhere in
                               .text: free bodies whose ENTIRE callee set is the stdio machinery
                               (__local_stdio_printf_options 0016D670, __stdio_common_* and
                               __acrt_iob_func thunks) - sprintf 0017D2E0 (FID-identified VS2019),
                               printf/vfprintf/vsprintf/vsnprintf/vswprintf-family wrappers - plus
                               the accessor itself. A game body that merely calls a stdio import
                               is NOT a member: 005CDAA0 formats into a 16 KiB stack buffer then
                               virtual-dispatches to a logger - rejected by the purity test.
  Provenance: census names are used only where the body matches the documented routine.
  00808C90 is the __scrt_common_main_seh body (_set_app_type, _configure_narrow_argv,
  _initialize_narrow_environment, __setusermatherr, atexit); 00809124/00809244 are the
  _Init_thread condition-variable init and its atexit-registered teardown (atexit(FUN_00809244)
  is literal in the body); 00809B44/00809B54 are __scrt_set_unhandled_exception_filter and the
  0xE06D7363 'msc' filter (SetUnhandledExceptionFilter(FUN_00809B54) is literal);
  00808D5C is a CRT initializer - a qword to it sits at .rdata 008C31D8, inside the _initterm
  range 008C31D0-008C5678 that the A-measured startup body 00808D78 walks; 00808C64 installs
  type_info::vftable (scalar deleting destructor of the CRT RTTI support class); 0080A270 is the
  vectorized powf4 kernel (ln(2)/log2(e) constants, table banks 03009A00-03009D00 and
  03006800/03006840-030068C0/0300DExx-0300DFC0, calls the 0080B8A0 per-lane special-case
  handler) reached through declared forwarder thunk 00809920.
  Boundary asserted: the entry before the first member is 00808770, a declared libwebm mkvparser
  member; the entry after the last in-block member is 0080C5A0, a declared zlib member. The
  basic_streambuf import thunks 00808888-008088FA and the named import thunks 00861Exx-008620xx are
  declared by external-import-stubs / internal-tail-call-forwarders and are NOT members.
  The vectorized libm kernels 0080A270/0080A720/0080AFE0 are reached ONLY through the CRT thunk
  block (the jmp stubs at 00809920/00809930/00809940 inside census entry 00809920's extent) -
  every code referrer is a declared forwarder, which is the CRT dispatch layer itself.
  Deliberately not members: 008098D4 (shared allocator adapter - called by eight mkvparser members
  and by game code at 001F4250; its thunk referrer 00809948 is not exclusive, real callers exist);
  005CDAA0 (game logger that internally calls __stdio_common_vsnprintf_s - fails wrapper purity);
  the post-thunk strays 00861EAE (EH Unwind node), 008620A0 (memset wrapper), 008620B0 (empty ret),
  008620C0 (the FFXII-authored exit() stub - its own string says so), 008620D0/008620E0
  (atexit-state setters, no CRT witness edge).
Usage: python select_msvc_runtime.py [--write]"""
import sys, os, struct, bisect, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

NAME = "MSVC runtime tail"
LO, HI = 0x8087C4, 0x80C5A0     # 008087C4/00808850 are the two CRT bodies inside the mkvparser run
INITTERM = (0x8C31D0, 0x8C56A0) # .CRT$XI* range walked by _initterm/_initterm_e in 00808D78
inr = lambda a: LO <= a < HI
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
names = {}
for line in open(os.path.join(W, "graph", "functions.tsv"), encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: names[int(p[0], 16)] = p[1]
    except ValueError: pass
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS and parts[0] != NAME:
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass

def owner_of(a):
    # the census tiles .text: an entry's slot runs to the next entry start. Ghidra's recovered
    # body size can under-report (00809920's slot holds three vdecl jmp stubs at +0x00/+0x10/+0x20).
    i = bisect.bisect_right(ents, a) - 1
    if i < 0: return
    hi = ents[i + 1] if i + 1 < len(ents) else ents[i] + max(sizes[ents[i]], 1)
    if ents[i] <= a < hi: return ents[i]
callers = collections.defaultdict(set); callees = collections.defaultdict(set)
text = secs[".text"]; to, tn = text[2], text[3]
for o in range(to, to + tn - 5):
    if d[o] not in (0xE8, 0xE9): continue
    src = text[0] + (o - to); t = src + 5 + struct.unpack_from("<i", d, o + 1)[0]
    if t not in eset: continue
    f = owner_of(src)
    if f is None or f == t: continue
    callers[t].add(f); callees[f].add(t)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True; rx = re.compile(r"rip ([+-]) (0x[0-9a-f]+|\d+)")
span = [e for e in ents if inr(e)]
rev_leas = collections.defaultdict(set)   # target -> {in-block sources whose code takes its address}
for e in span:
    o = off(e)
    if o is None: continue
    # clip at the next census entry = the slot end: ghidra's recovered body extent can overrun
    # into later entries (00809900's listed size covers the thunk block) or under-report it
    nxt = ents[bisect.bisect_right(ents, e)] if bisect.bisect_right(ents, e) < len(ents) else e + sizes[e]
    for x in md.disasm(d[o:o + (nxt - e)], e):
        m = rx.search(x.op_str)
        if m:
            t = x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
            if inr(t) and t in eset: rev_leas[t].add(e)
        # mov reg, imm32/64 callback registration (SetUnhandledExceptionFilter, atexit)
        for op in x.operands:
            if op.imm and inr(op.imm) and op.imm in eset: rev_leas[op.imm].add(e)

# seeds 1: census names matching documented vcruntime/CRT/ATL routines (bodies spot-verified);
# 2: 00808C64 installs type_info::vftable (decompile shows `*param_1 = type_info::vftable`),
#    00808D5C is pointed to from .rdata 008C31D8 inside the _initterm range - a CRT initializer;
# 3: the libm/SSE math cluster, seeded on inspected bodies: 008098C0 is the __isa_available-gated
#    dispatch (roundps fast path, falls through to callee 00809D20), 00809900 calls the 00809D80
#    kernel, 0080A270 is powf4 reached via declared forwarder thunk 00809920. Their callees
#    (00809D20, 00809D80, 0080B8A0) join by closure.
CRT_NAME = re.compile(r"^(__scrt_|_Init_thread_|__GSHandlerCheck|__security_(check|init)_cookie|"
    r"__report_.*failure|__raise_securityfailure|capture_(current|previous)_context|_alloca_probe|"
    r"atexit$|_onexit$|_Facet_Register|`eh_vector_|__ArrayUnwind|__isa_available_init|"
    r"_guard_check_icall|CAtlBaseModule|~CAtlBaseModule|GetHInstanceAt|`scalar_deleting_destructor'$)")
LOCALE_OPTS = 0x16D670
SEED_NOTE = {
    0x808C64: "type_info::vftable slot - scalar deleting dtor of the CRT RTTI class",
    0x808D5C: "qword target inside _initterm range 008C31D0-008C5678 (.rdata 008C31D8)",
    0x8098C0: "__isa_available-gated SSE math dispatch (roundps / fallback 00809D20)",
    0x809900: "SSE math kernel calling fallback 00809D80",
    0x80A270: "vectorized powf4 kernel; sole code referrer is forwarder thunk 00809920",
    LOCALE_OPTS: "__local_stdio_printf_options - called by every __stdio_common_* wrapper",
}
# Accounting state does not feed the predicate (FABLE ruling on SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930, generalised;
# SWE2-EC7 2026-09-30): A-measured bodies are judged by the same seed/join tests as any body and, when they pass, join
# the fixpoint as qualifying nodes; they are removed from the OUTPUT only (no double accounting). Being A alone never
# qualifies a body (the old 'or an A-measured in-block body' caller allowance is gone).
# FABLE ruling point 3 (SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930; SWE2-EC7 2026-09-30): another family's declaration no
# longer decides qualification. A declared body that passes is a qualifying node; ownership stays with its family (it
# is removed from the output and printed as a collision). A thunk/forwarder is recognised by its bytes.
def is_stub(f):
    o = off(f)
    if o is None or sizes.get(f, 99) > 8: return False
    return d[o] == 0xE9 or d[o:o + 2] == bytes((0xFF, 0x25)) or d[o:o + 3] == bytes((0x48, 0xFF, 0x25))
seeds = {e for e in span if CRT_NAME.match(names.get(e, ""))}
seeds |= set(SEED_NOTE)
members = set(); witness = {}
for e in seeds:
    if e != LOCALE_OPTS and not inr(e): continue
    members.add(e)
    witness[e] = SEED_NOTE.get(e) or "named CRT routine: " + names.get(e, "")
# fixpoint inside the block: a free in-block entry joins if a member (or an A-measured in-block
# body - individually verified CRT code) calls it, or leas it (callback registration), or it calls
# a member. Separately below: a pointer to it inside the .CRT$XI initterm range makes it a CRT
# initializer.
changed = True
while changed:
    changed = False
    for e in span:
        if e in members: continue
        joined = next((t for t in callees[e] if t in members), None)
        if joined is not None:
            members.add(e); witness[e] = "calls member %08X" % joined; changed = True; continue
        joined = next((f for f in callers[e] | rev_leas[e]
                       if f in members), None)
        if joined is not None:
            members.add(e); witness[e] = "called/lea'd by member %08X" % joined; changed = True; continue
        # reached only through the CRT's own thunk layer: every code referrer is a declared
        # forwarder/import-stub entry (the vdecl kernels 0080A270/0080A720/0080AFE0 are jmp'ed to
        # by the thunk block at 00809920-00809947). 008098D4 fails this - its other callers are
        # mkvparser members and game code, i.e. it is a shared adapter, not runtime-private.
        refs = callers[e] | rev_leas[e]
        if refs and all(is_stub(f) for f in refs):
            members.add(e)
            witness[e] = "reached only via thunk block " + " ".join("%08X" % f for f in sorted(refs))
            changed = True; continue
rd = secs[".rdata"]
for o in range(rd[2], rd[2] + rd[3] - 8, 8):
    va = rd[0] + (o - rd[2])
    if not (INITTERM[0] <= va < INITTERM[1]): continue
    t = struct.unpack_from("<Q", d, o)[0]
    if inr(t) and t in eset and t not in members:
        members.add(t); witness[t] = "pointer in .CRT initterm table at %08X" % va
# image-wide COMDAT stdio wrappers: a free body that calls the options accessor or a
# __stdio_common_* thunk is a member ONLY when that is all it does - every other callee must be
# the same stdio machinery or an already-declared import/forwarder thunk. 005CDAA0 fails this:
# it additionally calls _Init_thread_*, FUN_005CDA30 and a virtual sink.
STDIO = re.compile(r"^(__stdio_common_|__acrt_iob_func)")
def stdio_use(e):
    return any(t == LOCALE_OPTS or STDIO.match(names.get(t, "")) for t in callees[e])
def pure_stdio(e):
    if not stdio_use(e): return False
    for t in callees[e]:
        if t == LOCALE_OPTS or STDIO.match(names.get(t, "")) or is_stub(t): continue
        return False
    return True
comdat, impure = [], []
for e in ents:
    if e in members or inr(e): continue
    if pure_stdio(e):
        members.add(e); comdat.append(e)
        witness[e] = "COMDAT stdio wrapper"
    elif stdio_use(e):
        impure.append(e)

qualifying_a = members & a_set
members -= a_set
collisions = sorted(members & set(declared))
members -= set(declared)
print("predicate members owned by another family (collisions, not written): %d %s" % (len(collisions), " ".join("%08X" % e for e in collisions[:40])))
print("A-measured bodies that pass the predicate (qualifying nodes, stay A, not members): %d" % len(qualifying_a))
excl = collections.defaultdict(list); final = []
for e in span:
    if e in members: final.append(e)
    elif e in a_set: excl["A-measured (individually dispositioned)"].append(e)
    elif e in declared: excl["declared: " + declared[e][:48]].append(e)
    else: excl["no runtime-exclusive witness (shared or unjoined)"].append(e)
print("MSVC runtime block %08X-%08X: entries %d, seeds %d, members %d (+%d outside block)"
      % (LO, HI, len(span), len(seeds), len(final), len(members) - len(final)))
print("  outside-block member %08X %s  %s" % (LOCALE_OPTS, names.get(LOCALE_OPTS, ""), witness[LOCALE_OPTS]))
for e in final:
    if names.get(e, "").startswith("FUN_") or "thunk" in names.get(e, ""):
        print("  FUN_ member %08X  witness: %s" % (e, witness[e]))
for k, v in sorted(excl.items()):
    print("  excluded %-58s %3d  %s" % (k[:58], len(v), " ".join("%08X" % x for x in v)))
for e in sorted(comdat):
    print("  COMDAT member %08X  %-24s %s" % (e, names.get(e, ""), witness[e]))
for e in impure:
    print("  uses stdio, not a wrapper %08X %s" % (e, names.get(e, "")))
print("  post-thunk strays, not admitted:", " ".join("%08X(%s)" % (a, declared.get(a, "FREE")) for a in
      [0x861EAE, 0x8620A0, 0x8620B0, 0x8620C0, 0x8620D0, 0x8620E0]))
outb = collections.Counter()
for e in members:
    for t in callees[e]:
        if t not in members: outb[t] += 1
print("control outbound targets:", " ".join("%08X:%s(%d)" % (t, names.get(t, "?")[:24], c) for t, c in sorted(outb.items())))
print("control inbound caller zones:", dict(collections.Counter("%04X" % (f >> 16) for e in members for f in callers[e] if f not in members)))
# positive controls: known non-members must stay out
assert 0x8620C0 not in members and 0x8098D4 not in members and 0x80C5A0 not in members
assert 0x80A720 in members and 0x80AFE0 in members         # vdecl kernels, thunk-block reached
assert 0x5CDAA0 not in members                             # game logger, fails wrapper purity
if "--write" in sys.argv:
    open(os.path.join(HERE, "msvc-runtime-tail.tsv"), "w").write(
        "# MSVC vcruntime/CRT tail + math cluster + ATL residue + stdio COMDAT wrappers - select_msvc_runtime.py\n"
        + "\n".join("%08X" % e for e in sorted(members)) + "\n")
    print("wrote", len(members))
