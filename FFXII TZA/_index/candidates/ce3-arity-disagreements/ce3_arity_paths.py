"""ce3_arity_paths.py - CE-3: the 17 catalog/measurement arity disagreements, settled by a path-sensitive,
call-following stack walk (FABLE, Claude Opus 5.5, 2026-09-26; the walker is the delegated read-only pass's
CE-3_ipdeficit.py, re-implemented here self-contained and re-run with its controls).

summary(f) = the set of (need, net) over the acyclic control-flow paths of f, where need = -(min prefix sum) with a
pop as -1 and a push as +1. Pops are calls to 00267DB0 / 00267E10, pushes calls to 00267F60 / 00267F90. Direct calls and
tail jumps to other listed functions are composed recursively. Back edges are cut, so a loop body counts once.

  A1 the 17: family-0 catalog-known verbs whose measured net = pops - pushes is positive and differs from the
     catalog's arity (scriptvm-verb-table.tsv): 612 anchors, 17 disagreements.
  A2 controls on handlers with known arity: 0034C290 (the shared begin) 0, wait 1, setpos 3, ames 5, messync 2, rmove 3.
  A3 11 of the 17 are counting artefacts: the catalog arity is the walk's need on every path. The second pop is in a
     callee (delegation) or on an exclusive arm.
  A4 2 more artefacts, 13 in all: setbattlemember and getbattlemember pop inside a loop. Its trip count is 3 (ebx = 2..0) or 4 (edi = 3..0), which
     equals the catalog.
  A5 4 are real: rturnt/turnt (003425D0) and rturn_4f/turn_67 (003439B0) need 3 or 4 depending on the actor. The
     helper 00357DE0 pops its middle operand only when 00263D00(actor) is 0 (00357E1F..00357E2B). 00263D00 is true
     for a kind-3 actor whose steering byte +0x62 is >= 0x80 (00263D18). The catalog's 4 is the larger path.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
ENTRIES = set()
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: ENTRIES.add(int(p[0], 16))
    except (ValueError, IndexError): pass
POPS = {0x267DB0, 0x267E10}; PUSHES = {0x267F60, 0x267F90}
JCC = {"je", "jne", "ja", "jae", "jb", "jbe", "jg", "jge", "jl", "jle", "js", "jns", "jo", "jno", "jp", "jnp", "jrcxz", "jecxz"}
cs = Cs(CS_ARCH_X86, CS_MODE_64); _c = {}
def insn(a):
    if a not in _c:
        o = off(a); _c[a] = next(cs.disasm(d[o:o + 16], a), None) if o is not None else None
    return _c[a]
def tgt(i):
    try: return int(i.op_str, 16)
    except ValueError: return None
MEMO = {}
def summary(f, stack=()):
    if f in MEMO: return MEMO[f]
    if f in stack or len(stack) > 12: return {(0, 0)}
    res = set(); work = [(f, 0, 0, frozenset())]; npaths = 0
    while work:
        a, dd, lo, seen = work.pop()
        while True:
            if a in seen: res.add((-lo, dd)); break
            seen = seen | {a}; i = insn(a)
            if i is None: res.add((-lo, dd)); break
            m = i.mnemonic; nxt = a + i.size
            if m == "ret": res.add((-lo, dd)); break
            if m in ("call", "jmp"):
                t = tgt(i)
                if t is None:
                    if m == "jmp": res.add((-lo, dd)); break
                    a = nxt; continue
                if m == "jmp" and not (t in ENTRIES and t != f): a = t; continue
                if t in POPS: dd -= 1; lo = min(lo, dd); subs = None
                elif t in PUSHES: dd += 1; subs = None
                else: subs = summary(t, stack + (f,))
                if subs:
                    first = None
                    for need, net in sorted(subs):
                        nlo = min(lo, dd - need); nd = dd + net
                        if m == "jmp": res.add((-nlo, nd))
                        elif first is None: first = (nlo, nd)
                        else: work.append((nxt, nd, nlo, seen))
                    if m == "jmp": break
                    lo, dd = first; a = nxt; continue
                if m == "jmp": res.add((-lo, dd)); break
                a = nxt; continue
            if m in JCC:
                npaths += 1
                if npaths > 4096: res.add((-lo, dd)); break
                t = tgt(i)
                if t is not None: work.append((t, dd, lo, seen))
                a = nxt; continue
            if m in ("int3", "ud2", "hlt"): break
            a = nxt
    MEMO[f] = res or {(0, 0)}
    return MEMO[f]
def needs(f): return sorted({nd for nd, _ in summary(f)})
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
rows = list(csv.DictReader(open(DB / "01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv", encoding="utf-8"), delimiter="\t"))
anch = 0; dis = []
for r in rows:
    if r["family"] != "0" or r["cat_known"] != "True": continue
    try: cat = int(r["cat_args"]); pops = int(r["pops_int"] or 0) + int(r["pops_float"] or 0); pu = int(r["pushes"] or 0)
    except ValueError: continue
    if pops - pu > 0:
        anch += 1
        if pops - pu != cat: dis.append(r)
check("A1 612 anchors, 17 disagreements", anch == 612 and len(dis) == 17, "%d / %d" % (anch, len(dis)))
CTRL = {0x34C290: 0, 0x34CF90: 1, 0x34EBC0: 3, 0x349BF0: 5, 0x3479F0: 2, 0x3488B0: 3}
got = {"%08X" % f: needs(f) for f in CTRL}
check("A2 controls: the walk's need equals the known arity on six handlers",
      all(max(needs(f)) == v for f, v in CTRL.items()), str(got))
LOOP = {"0355", "0357"}; REAL = {"004A", "0064", "004F", "0067"}
art = {r["call_id"]: (r["verb"], int(r["cat_args"]), needs(int(r["arg_handler"], 16))) for r in dis if r["call_id"] not in LOOP | REAL}
bad = {k: v for k, v in art.items() if v[2] != [v[1]]}
check("A3 11 artefacts settle by the walk: the catalog arity is the need on every path (with A4's two, 13)", len(art) == 11 and not bad,
      "n=%d bad=%s" % (len(art), bad))
def at(a): i = insn(a); return "%s %s" % (i.mnemonic, i.op_str)
check("A4 setbattlemember pops in a loop over ebx = 2..0; getbattlemember over edi = 3..0",
      at(0x34D558) == "call 0x267e10" and at(0x34D578) == "sub ebx, r13d" and at(0x34D57B) == "jns 0x34d555"
      and at(0x34F5D3) == "call 0x267e10" and at(0x34F5EB) == "sub rdi, 1" and at(0x34F5EF) == "jns 0x34f5d0"
      and any(at(a) == "mov ebx, 2" for a in range(0x34D4E0, 0x34D555) if insn(a) and insn(a).address == a)
      and any(at(a) == "mov edi, 3" for a in range(0x34F5A0, 0x34F5D0) if insn(a) and insn(a).address == a))
real = {r["call_id"]: (r["verb"], int(r["cat_args"]), needs(int(r["arg_handler"], 16))) for r in dis if r["call_id"] in REAL}
check("A5 the four turn verbs need 3 or 4: 00357DE0 skips its middle pop when 00263D00(actor) is true",
      len(real) == 4 and all(v[2] == [3, 4] and v[1] == 4 for v in real.values())
      and at(0x357E1F) == "call 0x263d00" and at(0x357E26) == "jne 0x357e35" and at(0x357E2B) == "call 0x267db0"
      and at(0x357E35) == "xorps xmm7, xmm7" and at(0x263D18) == "cmp byte ptr [rcx + 0x62], 0x80", str(real))
print("FAILS", fails)
sys.exit(1 if fails else 0)
