"""B-2/c (OPUS, 2026-09-26): individually verify the 136 magic statics whose construction has no _Init_thread_abort
funclet. STATIC over the shipped image.

Per construction site, the region runs from `call _Init_thread_header` (008092FC) to the matching
`call _Init_thread_footer` (0080929C), matched as the footer whose last `lea rcx, [rip+guard]` names the same guard.
Every call in the region is followed through its transitive direct-call / tail-jump closure. Imports are resolved
through their IAT slots and through `jmp [IAT]` thunks:
  THROW    _CxxThrowException, and the msvcp140 ?_X* throw helpers;
  UNKNOWN  any other msvcp140 import (a C++ library call that may throw), and any indirect call;
  NOTHROW  every other import (vcruntime mem*/str*, the UCRT, Win32: C functions that raise no C++ exception).
One indirect call is resolved by name rather than left UNKNOWN: _Init_thread_wait (008093C0) calls through `call rbx`
the pointer that __scrt_initialize_thread_safe_statics (00809130) stored at [02EAED78] (008091E0), ror/xor-encoded
with the security cookie, from GetProcAddress(kernel32, "SleepConditionVariableCS") (the lea at 00809170). C5 asserts
that chain from the bytes. The indirect call is a Win32 wait, not a C++ call.
Site classes, worst per guard: NOCALL < NOTHROW-CLOSED < UNKNOWN < THROW < NOFOOTER.
Control: the 1,545 guards WITH a funclet are classified by the same code.
Writes result.json."""
import os
import struct, re, collections, json, sys, bisect
import pefile, capstone
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
HDR, FTR, ABT = 0x8092FC, 0x80929C, 0x80926C
pe = pefile.PE(EXE); img = pe.get_memory_mapped_image(); IB = 0x120000
TLO, THI = 0x121000, 0x8C0000
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
IMP = {}
for e in pe.DIRECTORY_ENTRY_IMPORT:
    for i in e.imports:
        IMP[i.address] = (e.dll.decode().lower(), i.name.decode() if i.name else "#%d" % i.ordinal)
def imp_kind(slot):
    dll, nm = IMP[slot]
    if nm == "_CxxThrowException" or (dll.startswith("msvcp") and nm.startswith("?_X")): return "THROW"
    if dll.startswith("msvcp"): return "UNKNOWN"
    return "NOTHROW"
def thunk_slot(a):
    o = a - IB
    if 0 <= o < len(img) - 6 and img[o] == 0xFF and img[o + 1] == 0x25:
        t = a + 6 + struct.unpack_from("<i", img, o + 2)[0]
        if t in IMP: return t
    return None
def rel_sites(tgt):
    out = []
    for m in re.finditer(rb"[\xE8\xE9]", img[TLO - IB:THI - IB]):
        o = m.start() + TLO - IB
        if o + IB + 5 + struct.unpack_from("<i", img, o + 1)[0] == tgt: out.append(o + IB)
    return out
def guard_before(a):          # the header / abort idiom puts `lea rcx, [rip+guard]` right before the call
    for back in range(7, 80):
        ins = list(md.disasm(img[a - back - IB:a - IB], a - back))
        if ins and ins[-1].address + ins[-1].size == a:
            for i in reversed(ins):
                m = re.match(r"rcx, \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
                if i.mnemonic == "lea" and m: return i.address + i.size + int(m.group(1), 16)
            return None
hdr = [(a, guard_before(a)) for a in rel_sites(HDR) if img[a - IB] == 0xE8]
abt = [(a, guard_before(a)) for a in rel_sites(ABT)]
hg = {g for _, g in hdr if g}; ag = {g for _, g in abt if g}
nof = hg - ag
# ---- function bodies, direct edges, imports and indirect calls
funcs = {}
for l in open(FT, encoding="utf-8", errors="replace"):
    c = l.split("\t")
    try: funcs[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
starts = sorted(funcs)
def owner(a):
    k = bisect.bisect_right(starts, a) - 1
    return starts[k] if k >= 0 and a < starts[k] + max(funcs[starts[k]], 1) else None
edges = collections.defaultdict(set); indirect = collections.Counter(); fimps = collections.defaultdict(set)
def scan_call(i, f, lo, hi):
    op = i.op_str
    if op.startswith("0x"):
        t = int(op, 16)
        s = thunk_slot(t)
        if s: fimps[f].add(s)
        elif not lo <= t < hi: edges[f].add(t)
        return
    m = re.match(r"qword ptr \[rip \+ (0x[0-9a-f]+)\]", op)
    if m:
        t = i.address + i.size + int(m.group(1), 16)
        if t in IMP: fimps[f].add(t); return
    if i.mnemonic == "call": indirect[f] += 1
for f, sz in funcs.items():
    if not TLO <= f < THI or sz <= 0: continue
    for i in md.disasm(img[f - IB:f - IB + sz], f):
        if i.mnemonic in ("call", "jmp"): scan_call(i, f, f, f + sz)
def node(t):
    s = thunk_slot(t)
    if s: return ("imp", s)
    o = t if t in funcs else owner(t)
    return ("fn", o) if o is not None else ("lost", t)
memo = {}
def closure(root):
    if root in memo: return memo[root]
    seen = set(); st = [root]; kinds = set(); imps = set()
    while st:
        n = st.pop()
        if n in seen: continue
        seen.add(n)
        if n[0] == "imp": kinds.add(imp_kind(n[1])); imps.add(n[1]); continue
        if n[0] == "lost": kinds.add("UNKNOWN"); continue
        f = n[1]
        if indirect[f]: kinds.add("UNKNOWN")
        for s in fimps.get(f, ()): st.append(("imp", s))
        for t in edges.get(f, ()): st.append(node(t))
    memo[root] = (kinds, imps, len(seen))
    return memo[root]
ORDER = ["NOCALL", "NOTHROW-CLOSED", "UNKNOWN", "THROW", "NOFOOTER"]
def site_class(site, g):
    calls = []; ind = 0; lastrcx = None
    for i in md.disasm(img[site + 5 - IB:site + 5 - IB + 0x1800], site + 5):
        m0 = re.match(r"rcx, \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
        if i.mnemonic == "lea" and m0: lastrcx = i.address + i.size + int(m0.group(1), 16)
        if i.mnemonic == "call":
            if i.op_str.startswith("0x") and int(i.op_str, 16) == FTR and lastrcx == g:
                kinds = set(); imps = set()
                for n in calls:
                    k, im, _ = closure(n) if n[0] != "imp" else ({imp_kind(n[1])}, {n[1]}, 1)
                    kinds |= k; imps |= im
                if ind: kinds.add("UNKNOWN")
                cls = "NOCALL" if not calls and not ind else "THROW" if "THROW" in kinds else "UNKNOWN" if "UNKNOWN" in kinds else "NOTHROW-CLOSED"
                return cls, i.address, calls, ind, imps
            if i.op_str.startswith("0x"): calls.append(node(int(i.op_str, 16)))
            else:
                m = re.match(r"qword ptr \[rip \+ (0x[0-9a-f]+)\]", i.op_str)
                t = i.address + i.size + int(m.group(1), 16) if m else None
                if t in IMP: calls.append(("imp", t))
                else: ind += 1
        if i.mnemonic in ("ret", "int3"): break
    return "NOFOOTER", None, calls, ind, set()
bysite = collections.defaultdict(list)
for a, g in hdr:
    if g: bysite[g].append(a)
def guard_class(g):
    rs = [site_class(s, g) for s in bysite[g]]
    return max(rs, key=lambda r: ORDER.index(r[0])), rs
KNOWN_WAIT = 0x8093C0
_old = closure
def closure(root):                 # as above, but _Init_thread_wait's one indirect call is the named Win32 wait
    if root in memo: return memo[root]
    seen = set(); st = [root]; kinds = set(); imps = set()
    while st:
        n = st.pop()
        if n in seen: continue
        seen.add(n)
        if n[0] == "imp": kinds.add(imp_kind(n[1])); imps.add(n[1]); continue
        if n[0] == "lost": kinds.add("UNKNOWN"); continue
        f = n[1]
        if indirect[f] and f != KNOWN_WAIT: kinds.add("UNKNOWN")
        if f == KNOWN_WAIT: kinds.add("WAIT")
        for s in fimps.get(f, ()): st.append(("imp", s))
        for t in edges.get(f, ()): st.append(node(t))
    memo[root] = (kinds, imps, len(seen))
    return memo[root]
res = {g: guard_class(g) for g in sorted(nof)}
ctrl = {g: guard_class(g) for g in sorted(ag & hg)}
cnt = collections.Counter(v[0][0] for v in res.values()); cc = collections.Counter(v[0][0] for v in ctrl.values())
print("header sites %d, guards %d; abort sites %d, guards %d; no-funclet guards %d" % (len(hdr), len(hg), len(abt), len(ag), len(nof)))
print("no-funclet guards, worst site:", {k: cnt[k] for k in ORDER if cnt[k]})
print("control, funclet guards, worst site:", {k: cc[k] for k in ORDER if cc[k]})
def nm(n):
    if n[0] == "imp": return IMP[n[1]][1]
    return "%08X" % n[1] if n[1] else "?"
wait_users = sorted("%08X" % g for g, (w, rs) in res.items() if any(n[0] == "fn" and "WAIT" in closure(n)[0] for r in rs for n in r[2]))
# C5: the wait pointer chain, from the bytes
ins = {i.address: i for i in md.disasm(img[0x809130 - IB:0x809450 - IB], 0x809130)}
def rip(a):
    i = ins[a]; m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", i.op_str); return i.address + i.size + int(m.group(1), 16)
def cstr(a):
    o = a - IB; return img[o:img.index(b"\0", o)].decode()
wait_ind = [a for a, i in ins.items() if 0x8093C0 <= a < 0x809457 and i.mnemonic == "call" and not i.op_str.startswith("0x") and "rip" not in i.op_str]
c5 = (cstr(rip(0x809170)) == "SleepConditionVariableCS" and ins[0x80917A].op_str == "rsi, rax" and ins[0x80918D].op_str == "rdi, rax"
      and ins[0x8091E0].mnemonic == "mov" and rip(0x8091E0) == 0x2EAED78 and ins[0x8091E0].op_str.endswith("rdi")
      and rip(0x8093E5) == 0x2EAED78 and ins[0x8093E5].mnemonic == "xor" and wait_ind == [0x80940B] and ins[0x80940B].op_str == "rbx")
cases = {
    "C1_population_1732_sites_1681_guards_1545_with_funclet_136_without": (len(hdr), len(hg), len(ag), len(nof)) == (1732, 1681, 1545, 136) and ag <= hg,
    "C2_every_site_of_the_136_reaches_its_own_footer": cnt["NOFOOTER"] == 0,
    "C3_none_of_the_136_reaches_a_throw_or_an_unresolved_call": cnt["THROW"] == 0 and cnt["UNKNOWN"] == 0 and cnt["NOCALL"] + cnt["NOTHROW-CLOSED"] == 136,
    "C4_control_most_funclet_guards_reach_an_unresolved_call_none_of_the_136_do": 2 * (cc["UNKNOWN"] + cc["THROW"]) > len(ctrl) and cc["NOFOOTER"] == 0,
    "C5_the_one_named_indirect_call_is_SleepConditionVariableCS": c5,
}
out = {"evidence": ["STATIC"], "live_game": False,
       "no_funclet_by_class": {k: cnt[k] for k in ORDER if cnt[k]}, "funclet_control_by_class": {k: cc[k] for k in ORDER if cc[k]},
       "guards_whose_only_wait_is_a_nested_magic_static": wait_users,
       "guards": {"%08X" % g: {"class": w[0], "sites": [{"site": "%08X" % s, "class": r[0], "calls": [nm(n) for n in r[2]], "indirect": r[3],
                  "imports_reached": sorted(IMP[x][1] for x in r[4])} for s, r in zip(bysite[g], rs)]} for g, (w, rs) in res.items()},
       "cases": cases, "ok": all(cases.values())}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json"), "w"), indent=1, sort_keys=True)
print("guards whose calls reach _Init_thread_wait (nested magic statics):", len(wait_users), wait_users)
for k, v in cases.items(): print("%-72s %s" % (k, "PASS" if v else "FAIL"))
print("ALL PASS" if out["ok"] else "FAILED")
sys.exit(0 if out["ok"] else 1)
