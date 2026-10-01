"""Falsification pass 1 on CONTRACT-world-loot-pickup-pool (OPUS, 2026-09-29), from the shipping image. Killers first.

  W0  section 2: the seven entries' sizes (387, 394, 423, 215, 113, 26, 26) and callers (init 2, the rest 1)
  W1  I1: create scans with `add rbx, 0x60` / `cmp eax, 0xa`; init stores slotIndex 0..9 into the ten nodes; the list head
      02EC1360 is 02EC0FA0 + 10 x 0x60
  W2  I3: every rip-relative store to a node's +0x00 is in init; the other six entries make no zero-displacement dword store
      through a register                                                         KILLER: a second writer of slotIndex
  W3  I4: image-wide, no rip-relative reference to any node's +0x0C or +0x5C, while +0x58 is referenced (control); the
      seven entries have no register-relative operand at +0xC or +0x5C
  W4  I5: append stores the tail at 00319D67; eviction loads the head at 00319CDC
  W5  section 12: the presentation opcodes at each 0028F000 call - eviction 5, despawn 4, collect 3, remove 3, blink 2, create 1
  W6  section 6: 0028F000 validates `lea eax, [rdx-1] / cmp eax, 5 / ja`; jump-table entries 4 and 5 are identical; ops 3
      and 4/5 reach 003FA820; the 4/5 target zeroes edx
  W7  section 10: no store to [rsp+0x20] precedes the eviction's lea (00319D1A) in create; in the tick the only store to
      [rsp+0x20] is the blink's (00319720), later in the loop body, so the despawn's payload is the previous iteration's
      blink value or older stack
  W8  section 5: 022C3174 is incremented only at 00319974 among the pool bodies; EnemyChain_TryAdvanceRank (003183D0) reads
      it as a multiplier and zeroes it (context the contract did not give)
  W9  section 2: no caller uses a return value (the first touch of eax after each call is a write, or none)
  W10 section 9: the call closure of the seven entries reaches no generator entry
"""
import collections, io, os, struct
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
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")

refs = collections.defaultdict(list)          # target -> [(function, insn)]
calls_to = collections.defaultdict(list)      # target -> [(function, address, mnemonic)]
bodies = {}
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
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))

STORES = ("mov", "movss", "movaps", "movups", "movdqa", "movdqu", "movq", "movd", "inc", "dec", "add", "sub", "or", "and", "xor")


def is_write(x):
    return bool(x.operands) and x.operands[0].type == X86_OP_MEM and x.mnemonic in STORES


def at(fa, va):
    return next(S(x) for x in bodies[fa] if x.address == va)


INIT, CREATE, TICK, COLLECT, REMOVE, CIDX, RIDX = 0x00319B10, 0x00319CA0, 0x00319600, 0x00319920, 0x003197B0, 0x00319A00, 0x00319830
E = [INIT, CREATE, TICK, COLLECT, REMOVE, CIDX, RIDX]
POOL, HEAD, TAIL, PRES = 0x02EC0FA0, 0x02EC1360, 0x02EC1368, 0x0028F000

# W0
sz = [sizes.get(e) for e in E]; nc = [len(calls_to[e]) for e in E]
check("W0", sz == [387, 394, 423, 215, 113, 26, 26] and nc == [2, 1, 1, 1, 1, 1, 1], "sizes %s; call sites %s" % (sz, nc))
# W1
cb = [S(x) for x in bodies[CREATE]]
init_slot = sorted((t - POOL) // 0x60 for t in range(POOL, HEAD) for f, x in refs[t] if (t - POOL) % 0x60 == 0 and f == INIT and is_write(x))
check("W1", at(CREATE, 0x00319CCC) == "add rbx, 0x60" and at(CREATE, 0x00319CD0) == "cmp eax, 0xa" and init_slot == list(range(10)) and HEAD == POOL + 10 * 0x60,
      "create scan %s / %s; init writes +0x00 of nodes %s; head %08X = pool + 10 x 0x60" % (at(CREATE, 0x00319CCC), at(CREATE, 0x00319CD0), init_slot, HEAD))
# W2
w0 = sorted({"%08X" % f for t in range(POOL, HEAD) if (t - POOL) % 0x60 == 0 for f, x in refs[t] if is_write(x)})
zd = [("%08X" % e, S(x)) for e in E if e != INIT for x in bodies[e] if is_write(x) and x.operands[0].mem.base != X86_REG_RIP
      and x.operands[0].mem.disp == 0 and x.operands[0].mem.index == 0 and x.operands[0].size == 4]
check("W2", w0 == ["00319B10"] and not zd, "rip-relative writers of +0x00: %s; zero-displacement dword stores elsewhere: %s" % (w0, zd or "none"))
# W3
h = {o: sum(len(refs[POOL + 0x60 * k + o]) for k in range(10)) for o in (0x0C, 0x58, 0x5C)}
rr = [("%08X" % e, S(x)) for e in E for x in bodies[e] for o in x.operands
      if o.type == X86_OP_MEM and o.mem.base not in (0, X86_REG_RIP) and x.reg_name(o.mem.base) not in ("rsp", "rbp") and o.mem.disp in (0x0C, 0x5C)]
check("W3", h[0x0C] == 0 and h[0x5C] == 0 and h[0x58] >= 10 and not rr,
      "image-wide rip hits: +0x0C %d, +0x5C %d, +0x58 %d (control); register-relative +0xC/+0x5C in the entries: %s" % (h[0x0C], h[0x5C], h[0x58], rr or "none"))
# W4
check("W4", rip(next(x for x in bodies[CREATE] if x.address == 0x00319D67)) == [TAIL] and at(CREATE, 0x00319D67).startswith("mov qword ptr [rip")
      and rip(next(x for x in bodies[CREATE] if x.address == 0x00319CDC)) == [HEAD] and at(CREATE, 0x00319CDC).startswith("mov rbx, qword ptr [rip"),
      "append %s -> tail; eviction %s <- head" % (at(CREATE, 0x00319D67), at(CREATE, 0x00319CDC)))
# W5 the opcode at each presentation call
def op_before(fa, call_va):
    ins = bodies[fa]; k = next(i for i, x in enumerate(ins) if x.address == call_va)
    for y in reversed(ins[max(0, k - 6):k]):
        if S(y).startswith("mov edx, "):
            return int(S(y).split(", ")[1], 16)
ops = {"eviction": op_before(CREATE, 0x00319D24), "create": op_before(CREATE, 0x00319E00), "despawn": op_before(TICK, 0x003196C9),
       "blink": op_before(TICK, 0x00319732), "collect": op_before(COLLECT, 0x003199BF), "remove": op_before(REMOVE, 0x003197FE)}
pc = sorted(("%08X" % f, "%08X" % a) for f, a, _m in calls_to[PRES] if f in E)
check("W5", ops == {"eviction": 5, "create": 1, "despawn": 4, "blink": 2, "collect": 3, "remove": 3} and len(pc) == 6, "%s; presentation calls from the pool %d" % (ops, len(pc)))
# W6
jt = [struct.unpack("<I", blob[OFF(0x0028F09C + 4 * k):OFF(0x0028F09C + 4 * k) + 4])[0] for k in range(6)]
t45 = BASE + jt[3]
check("W6", [S(x) for x in bodies[PRES] if 0x0028F017 <= x.address <= 0x0028F01D] == ["lea eax, [rdx - 1]", "cmp eax, 5", "ja 0x28f094"]
      and jt[3] == jt[4] and at(PRES, BASE + jt[2] + 6) == "call 0x3fa820" and at(PRES, t45 + 3) == "xor edx, edx"
      and any(S(x) == "call 0x3fa820" for x in bodies[PRES] if t45 <= x.address < t45 + 12),
      "table %s; ops 4 and 5 -> %08X (%s / %s); op 3 -> %08X" % (["%X" % v for v in jt], t45, at(PRES, t45), at(PRES, t45 + 3), BASE + jt[2]))
# W7 the payload residue
pre_evict = [S(x) for x in bodies[CREATE] if x.address < 0x00319D1A and is_write(x) and "[rsp + 0x20]" in x.op_str]
tick_st = [("%08X" % x.address, S(x)) for x in bodies[TICK] if is_write(x) and "[rsp + 0x20]" in x.op_str]
loop_back = [S(x) for x in bodies[TICK] if x.mnemonic.startswith("j") and T(x) is not None and T(x) < 0x003196BF and x.address > 0x00319720]
check("W7", not pre_evict and [a for a, _s in tick_st] == ["00319720", "0031976F"] and loop_back,
      "stores to [rsp+0x20] before the eviction lea: %s; tick stores %s; loop back-edge after them %s" % (pre_evict or "none", tick_st, loop_back[:2]))
# W8 the collected counter and its reader
cnt = sorted(("%08X" % f, "%08X" % x.address, S(x)) for f, x in refs[0x022C3174])
check("W8", [c[0] for c in cnt] == ["003183D0", "003183D0", "00319920"] and names.get("EnemyChain_TryAdvanceRank") == 0x003183D0
      and any(c[2].startswith("imul") for c in cnt) and any(c[2].startswith("mov dword ptr") and c[2].endswith(", 0") for c in cnt)
      and any(c[1] == "00319974" and c[2].startswith("inc") for c in cnt), "%s" % cnt)
# W9 callers never read the return value
def first_eax(fa, call_va):
    ins = bodies[fa]; k = next(i for i, x in enumerate(ins) if x.address == call_va)
    for y in ins[k + 1:k + 12]:
        rd, wr = y.regs_access()
        rd = {y.reg_name(r) for r in rd}; wr = {y.reg_name(r) for r in wr}
        if rd & {"eax", "rax", "al", "ax"}:
            return "read"
        if wr & {"eax", "rax"} or y.mnemonic in ("call", "ret", "jmp"):
            return "write"
    return "none"
uses = {("%08X" % f, "%08X" % a): first_eax(f, a) for e in E if e not in (COLLECT, REMOVE) for f, a, m in calls_to[e] if m == "call"}
check("W9", uses and all(v != "read" for v in uses.values()), "%s" % uses)
# W10 no generator in the closure
seen, st = set(), list(E)
while st:
    f = st.pop()
    if f in seen or f not in bodies:
        continue
    seen.add(f)
    for x in bodies[f]:
        t = T(x) if x.mnemonic in ("call", "jmp") else None
        if t is not None and t in bodies and not (f <= t < f + sizes[f]):
            st.append(t)
GEN = [0x00328370, 0x00379CD0, 0x00863BF0, 0x00863D30, 0x0018EE20, 0x0018D740]
lcg = sorted({"%08X" % f for f, _x in refs[0x022C256C] if f in seen})
pres_rng = sorted({"%08X" % f for f, _x in refs[0x01EF93E8] if f in seen})
check("W10", not [g for g in GEN if g in seen] and not lcg,
      "closure %d bodies; generator entries %s; gameplay LCG cell users %s; presentation PRNG cell users %s"
      % (len(seen), [hex(g) for g in GEN if g in seen] or "none", lcg or "none", pres_rng or "none"))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
