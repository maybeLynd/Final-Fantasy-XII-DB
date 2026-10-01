"""Falsification pass 1 on the-unit-shape-distance-primitives (06-Movement-And-Navigation; OPUS, 2026-09-29). Killers first.

  U0  the ten spans in the toolbox table                                                          KILLER: one differs
  U1  FA0 (00380FA0) dispatches on the shape type to the three primitives (sphere 00381AC0, cylinder 00381630, box 00381450)
                                                                                                   KILLER: a primitive not reached
  U2  the box primitive reads the face table 00D11200 and the margin constant 1.001; CF50 reads the index table 00908DE8
  U3  the sphere primitive calls acosf and sinf (imports or CRT bodies)                            KILLER: neither called
  U4  (CORRECTS "F430 plants D4B0") D4B0's address is taken only by F430's caller 002315E0, which calls F430; 0022F8B0 calls EB0
  U5  (REFUTES "zero inbound references") 0022D7E0 / 0022DE60 are planted callbacks (lea in 00231690, 002327D0 / 00230C10) and
      00230790, 0022E7D0, 003810B0 are called by them
  U6  00381D90 is reached from 00232160, which is reached from 003D97E0
  U7  the math leaves 00217150, 00217610, 00202C70, 00380800 have 15-86 CALL SITES each (anonymous-thunk callers counted)
"""
import collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[p[1]] = int(p[0], 16)
        except ValueError:
            pass
S = lambda x: "%s %s" % (x.mnemonic, x.op_str)
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")

refs = collections.defaultdict(list)          # target -> [(function, insn)]
imm_sites = collections.defaultdict(list)     # immediate -> [(function, address)]
calls_to = collections.defaultdict(list)      # target -> [(function, address, mnemonic)]
bodies = {}
WATCH = [(0x02089300, 4), (0x0208E6B0, 4), (0x01FD4A80, 4), (0x02EB4234, 1), (0x01EF93E8, 4), (0x022C256C, 4)]
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    bodies[fa] = ins
    for x in ins:
        for t in rip(x):
            refs[t].append((fa, x))
        for o in x.operands:
            if o.type == X86_OP_IMM:
                imm_sites[o.imm & 0xFFFFFFFF].append((fa, x.address))
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))


import struct as _st
F = {0x0022D4B0: 815, 0x0022E6D0: 249, 0x0022CF50: 381, 0x00380FA0: 263, 0x00381AC0: 708, 0x00381630: 1168, 0x00381450: 477,
     0x00381EB0: 365, 0x0046BF60: 54, 0x0046BFA0: 294}
d0 = {("%08X" % k): (sizes.get(k), v) for k, v in F.items() if sizes.get(k) != v}
check("U0", not d0, "span mismatches %s" % (d0 or "none"))
fa0 = bodies.get(0x00380FA0, [])
tg = {T(x) for x in fa0 if x.mnemonic in ("call", "jmp") and T(x) is not None}
check("U1", {0x00381AC0, 0x00381630, 0x00381450} <= tg, "FA0 reaches %s" % sorted("%08X" % t for t in tg))
box = bodies.get(0x00381450, [])
face = any(0x00D11200 in rip(x) for x in box)
def f32_at(va):
    try: return _st.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]
    except ValueError: return None
margin = sorted({round(f32_at(t), 4) for x in box for t in rip(x) if f32_at(t) is not None and 1.0 < (f32_at(t) or 0) < 1.01})
cf50 = any(0x00908DE8 in rip(x) for x in bodies.get(0x0022CF50, []))
check("U2", face and 1.001 in margin and cf50, "box reads 00D11200 %s, margin constants %s; CF50 reads 00908DE8 %s" % (face, margin, cf50))
imports = {}
for x in pe.DIRECTORY_ENTRY_IMPORT if hasattr(pe, "DIRECTORY_ENTRY_IMPORT") else []:
    pass
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
iat = {imp.address: (imp.name or b"").decode() for e in pe.DIRECTORY_ENTRY_IMPORT for imp in e.imports}
sph = bodies.get(0x00381AC0, [])
called = set()
for x in sph:
    if x.mnemonic == "call":
        for t in rip(x):
            called.add(iat.get(t, "%08X" % t))
        if T(x) is not None:
            tgt = T(x)
            # follow a jmp [IAT] thunk
            th = bodies.get(tgt) or []
            if th and th[0].mnemonic == "jmp" and rip(th[0]):
                called.add(iat.get(rip(th[0])[0], "%08X" % tgt))
            else:
                called.add("%08X" % tgt)
check("U3", any("acos" in c for c in called) and any("sin" in c for c in called), "the sphere primitive calls %s" % sorted(called))
# U4 (CORRECTS the wording "F430 plants D4B0"): the planter is F430's caller 002315E0 - `lea rax, [D4B0]` into its stack context,
# then the call to F430, which invokes the callback; F430 itself takes no address of D4B0.
planter = sorted({"%08X" % f for f, _x in refs[0x0022D4B0]})
f430_self = [S(x) for x in bodies.get(0x0022F430, []) if 0x0022D4B0 in rip(x)]
p_calls = any(T(x) == 0x0022F430 for x in bodies.get(0x002315E0, []) if x.mnemonic in ("call", "jmp"))
eb0 = [("%08X" % f, "%08X" % a) for f, a, _m in calls_to[0x00381EB0]]
check("U4", planter == ["002315E0"] and not f430_self and p_calls and any(f == "0022F8B0" for f, _a in eb0),
      "D4B0's address is taken only in %s, which calls F430 %s (F430 itself: %s); EB0 called from %s" % (planter, p_calls, f430_self or "none", eb0))
# U5 (REFUTES "zero inbound references - dead or runtime-dispatched"): all five are reached. 0022D7E0 and 0022DE60 are planted
# callbacks (lea in 00231690 / 002327D0 and 00230C10); 00230790, 0022E7D0 and 003810B0 are called directly by those two.
lea5 = {t: sorted({"%08X" % f for f, x in refs[t] if x.mnemonic == "lea"}) for t in (0x0022D7E0, 0x0022DE60)}
call5 = {t: sorted({"%08X" % f for f, _a, _m in calls_to[t]}) for t in (0x00230790, 0x0022E7D0, 0x003810B0)}
check("U5", lea5 == {0x0022D7E0: ["00231690", "002327D0"], 0x0022DE60: ["00230C10"]}
      and call5 == {0x00230790: ["0022D7E0"], 0x0022E7D0: ["0022D7E0"], 0x003810B0: ["0022D7E0", "0022DE60"]},
      "planted: %s; called: %s" % ({"%08X" % k: v for k, v in lea5.items()}, {"%08X" % k: v for k, v in call5.items()}))
c6a = [f for f, _a, _m in calls_to[0x00381D90]]
c6b = [f for f, _a, _m in calls_to[0x00232160]]
check("U6", 0x00232160 in c6a and 0x003D97E0 in c6b, "00381D90 <- %s; 00232160 <- %s" % (["%08X" % f for f in c6a], ["%08X" % f for f in c6b]))
# U7: the range holds as CALL SITES (a direct site, or a site calling an anonymous one-jmp thunk of the leaf; the named wrapper
# Matrix4x4f_Copy 0046D100 is its own function and not counted as the leaf's)
def sites(t):
    th = [f for f, b in bodies.items() if len(b) == 1 and b[0].mnemonic == "jmp" and T(b[0]) == t and not names_rev.get(f, "FUN_").split("_")[0] not in ("FUN", "thunk")]
    return len([1 for f, _a, _m in calls_to[t] if f not in th]) + sum(len(calls_to[x]) for x in th)
names_rev = {v: k for k, v in names.items()}
cnt = {("%08X" % t): sites(t) for t in (0x00217150, 0x00217610, 0x00202C70, 0x00380800)}
check("U7", all(15 <= v <= 86 for v in cnt.values()) and min(cnt.values()) == 15 and max(cnt.values()) == 86,
      "call sites %s (as calling functions the range is 10-52; the page's 'callers' means call sites)" % cnt)
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
