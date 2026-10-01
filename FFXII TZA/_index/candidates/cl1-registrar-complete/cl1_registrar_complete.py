"""cl1_registrar_complete.py - CL-1 rechecked with every member-registrar kind (FABLE, Claude Opus 5.5, 2026-09-26).

CL-1 (2026-09-14) resolved the descriptor at every site of TWO registrars, 00632960 and 00632A10, and concluded that 16
of the 21 classes "register no data member". ASTRA's phyre-array-registration-sentinel showed that a direct count's
zero is not proof of no registration through another route. This control counts every route that reaches the member
record base with the descriptor passed through.

  R1 kinds: the closure of functions that reach 00632FB0 (the member/named-node base) by E8 or E9, at an instruction
     boundary, WITHOUT writing rdx first, so the descriptor argument passes straight through. Expected exactly
     00632960 (PClassDataMember), 00632A10 (array), 00632A70, 00632B30 (PClassDataMemberDynamic), 00632BE0.
     Direct 00632FB0 callers that load their own rdx build other named objects and are not member registrars.
  R2 every E8/E9 site of a kind, from outside the kinds, resolves its rdx to a descriptor, except one: 0063942C in
     006393A0, where the descriptor is the method's own `this`.
  R3 controls: PLight 10 and PClusterHeaderBase 18 at 00632960; the five array holders 1 each at 00632A10.
  R4 PShaderPassParameterLocationTypesBase registers two members through 00632A70: m_parameterStart (005EA16A) and
     m_parameterCount (005EA1E3).
  R5 the other fifteen register nothing through any kind; PBase and PClassDescriptor are included (descriptors
     02CF8270 / 02CF8470, from their static initialisers 00164180 / 00163E30).
  R6 sensitivity: restricted to CL-1's two registrars, the same resolver gives 0 for R4's class - the CL-1 defect.
  R7 006393A0 (the only 00632B30 caller) has one caller, the cluster loader 0059AC00 at 0059AEA7: a member can
     also be added at load time, which no static count sees.
Limits: a registration that calls a descriptor's attach slot (+0x40) without any of these kinds is not swept; a
static registration site is not evidence that its one-time guard ran in any title or scene.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, re, struct, sys
from collections import defaultdict
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
funcs = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
starts = sorted(funcs)
def fn_of(a):
    i = bisect.bisect_right(starts, a) - 1
    if i < 0: return None
    s = starts[i]
    return s if a < s + funcs[s] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
vs, va, rs, ro = secs[0]
TXT0, TXT1 = BASE + va, BASE + va + rs
idx = defaultdict(list)
for op in (b"\xE8", b"\xE9"):
    k = d.find(op, ro)
    while 0 <= k < ro + rs - 5:
        a = BASE + va + k - ro
        t = a + 5 + struct.unpack_from("<i", d, k + 1)[0]
        if TXT0 <= t < TXT1: idx[t].append(a)
        k = d.find(op, k + 1)
def body_until(site):
    f = fn_of(site)
    return f, list(cs.disasm(d[off(f):off(site) + 5], f)) if f else []
def real(site):
    f, L = body_until(site)
    return any(x.address == site and x.mnemonic in ("call", "jmp") for x in L)
def rdx_untouched(site):
    f, L = body_until(site)
    for x in L:
        if x.address >= site: break
        dst = x.op_str.split(",")[0].strip()
        if dst in ("rdx", "edx", "dx", "dl", "dh") and x.mnemonic not in ("cmp", "test", "push"): return False
    return True
ROOTF = 0x632FB0
kinds = {ROOTF}; changed = True
while changed:
    changed = False
    for kf in list(kinds):
        for s in idx[kf]:
            f = fn_of(s)
            if f and f not in kinds and real(s) and rdx_untouched(s): kinds.add(f); changed = True
kinds.discard(ROOTF)
EXP = {0x632960, 0x632A10, 0x632A70, 0x632B30, 0x632BE0}
check("R1 registrar kinds are exactly the five", kinds == EXP, " ".join("%08X" % k for k in sorted(kinds)))
def rip_target(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return None if not m else x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
FAM = [("rax", "eax"), ("rbx", "ebx"), ("rcx", "ecx"), ("rdx", "edx"), ("rsi", "esi"), ("rdi", "edi"), ("rbp", "ebp"),
       ("r8", "r8d"), ("r9", "r9d"), ("r10", "r10d"), ("r11", "r11d"), ("r12", "r12d"), ("r13", "r13d"), ("r14", "r14d"),
       ("r15", "r15d")]
def fam(r):
    for f in FAM:
        if r in f: return f[0]
def getter_ret(g):
    if g not in funcs or funcs[g] > 0x200: return None
    r = None
    for x in cs.disasm(d[off(g):off(g) + funcs[g]], g):
        if x.op_str.split(",")[0].strip() in ("rax", "eax") and x.mnemonic in ("lea", "mov"):
            t = rip_target(x)
            if t is not None: r = t if x.mnemonic == "lea" else ("[%08X]" % t)
    return r
def resolve(site):
    f, L = body_until(site)
    want, depth = "rdx", 0
    for x in reversed([y for y in L if y.address < site]):
        if x.mnemonic == "call" and want == "rax":
            return getter_ret(int(x.op_str, 16)) if x.op_str.startswith("0x") else None
        dst = x.op_str.split(",")[0].strip()
        if fam(dst) != want or x.mnemonic not in ("lea", "mov", "movsxd", "xor", "pop"): continue
        if x.mnemonic == "lea": return rip_target(x)
        if x.mnemonic == "mov":
            t = rip_target(x)
            if t is not None: return "[%08X]" % t
            src = fam(x.op_str.split(",")[1].strip())
            if src and depth < 4: want, depth = src, depth + 1; continue
        return None
    return None
reg = defaultdict(list); unres = []
for kf in sorted(kinds):
    for s in idx[kf]:
        f = fn_of(s)
        if f is None or f in kinds or not real(s): continue
        r = resolve(s)
        if r is None: unres.append((s, kf))
        else: reg[r if isinstance(r, int) else int(r[1:-1], 16)].append((s, kf))
tot = sum(len(v) for v in reg.values())
check("R2 every kind site resolves but the one inside 006393A0", [(s, k) for s, k in unres] == [(0x63942C, 0x632B30)],
      "resolved %d; unresolved %s" % (tot, ["%08X->%08X" % u for u in unres]))
def by(g, kinds_=None):
    return [(s, k) for s, k in reg.get(g, []) if kinds_ is None or k in kinds_]
ctl = {"PLight": (0x02E58DB0, 10, 0x632960), "PClusterHeaderBase": (0x02CA9FA0, 18, 0x632960),
       "PShaderPassParameterLocationTypesConstantBuffer": (0x02CB9800, 1, 0x632A10),
       "PStreamInputLayoutD3D11": (0x02CF1740, 1, 0x632A10), "PNodeContext": (0x02CB7280, 1, 0x632A10),
       "PMaterialSet": (0x02D3A440, 1, 0x632A10), "PMeshInstanceSegmentContext": (0x02CB6D80, 1, 0x632A10)}
bad = {c: len(by(g)) for c, (g, nexp, k) in ctl.items() if not (len(by(g)) == nexp and all(kk == k for _, kk in by(g)))}
check("R3 controls reproduce CL-1's counts (PLight 10, PClusterHeaderBase 18, five array holders 1 each)", not bad, repr(bad))
B = 0x02CB9600
hitsB = sorted(s for s, k in by(B))
def nm(site):
    f, L = body_until(site)
    for x in reversed([y for y in L if y.address < site]):
        if x.op_str.startswith("r9,") and x.mnemonic == "lea":
            t = rip_target(x); o = off(t); return d[o:d.find(b"\0", o)].decode()
names = [nm(s) for s in hitsB]
check("R4 PShaderPassParameterLocationTypesBase registers two members through 00632A70",
      hitsB == [0x5EA16A, 0x5EA1E3] and all(k == 0x632A70 for _, k in by(B)) and names == ["m_parameterStart", "m_parameterCount"],
      "%s %s" % (["%08X" % s for s in hitsB], names))
NONE = {"PShaderVertexProgram": 0x02CBAF00, "PShaderFragmentProgram": 0x02CBB000, "PShaderFragmentProgramD3D11": 0x02CF1A40,
        "PShaderGeometryProgram": 0x02CBB100, "PShaderGeometryProgramD3D11": 0x02CF1B40, "PShaderComputeProgram": 0x02CBB200,
        "PShaderProgramBase": 0x02CBAD00, "PTexture2DD3D11": 0x02CF1D40, "PTextureCubeMapD3D11": 0x02CF1F40,
        "PSamplerStateD3D11": 0x02CF2140, "PDataBlockBufferD3D11": 0x02D39B40, "PIndexDataBlockBufferD3D11": 0x02D39940,
        "PMeshSegmentContext": 0x02E522F0, "PBase": 0x02CF8270, "PClassDescriptor": 0x02CF8470}
nz = {c: len(by(g)) for c, g in NONE.items() if by(g)}
check("R5 the other fifteen register nothing through any of the five kinds", not nz and len(NONE) == 15, repr(nz))
old = len(by(B, {0x632960, 0x632A10}))
check("R6 sensitivity: CL-1's two registrars alone see 0 for R4's class", old == 0, "two-registrar count %d" % old)
c93 = sorted(s for s in idx[0x6393A0] if real(s))
check("R7 006393A0 is reached only from the cluster loader 0059AC00", c93 == [0x59AEA7] and fn_of(0x59AEA7) == 0x59AC00,
      repr(["%08X" % s for s in c93]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
