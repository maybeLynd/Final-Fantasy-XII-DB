"""sd164_arena.py - SD-164 / SD-166 / SD-167: the arena allocator's callback slot, whether anything selects arena 7 after
boot, and which callers take handles (OPUS, 2026-09-30). Static, the certified image, via
Database/Tools/analysis-kit/gfz-scripts/retool.py.
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def callers(t):
    return sorted(c["calls"].get(t, ()))


# ---- SD-164 ----
# H1 - 0036BFE0 calls the qword at heap record +0xA0 (15 records of 0xA8 at 022D7FD0, selected by [022D89BC]) with
#      (heap index, size); the slot is written by the boot initializer 00369D30 (r8, cleared at 00369D57) and by the setter
#      0036C5A0(id <= 0xE, fn), whose only caller is 002EA320: heaps 6 and 0xA get 002E6D60; nothing else addresses the slot
direct = [a for k in range(15) for a in [0x022D7FD0 + 0xA8 * k + 0xA0] if c["refs"].get(a)]
check("H1", txt(0x0036C02D) == "mov rax, qword ptr [rdx + 0xa0]" and txt(0x0036C03B) == "call rax" and txt(0x0036C039) == "mov edx, ebp"
      and txt(0x0036C5B6) == "mov qword ptr [rcx + rax + 0xa0], rdx" and callers(0x0036C5A0) == [(0x002EA320, 0x002EA4F3), (0x002EA320, 0x002EA504)]
      and txt(0x002EA4E7).endswith("0x378e]") and txt(0x002EA4EE) == "mov ecx, 6" and txt(0x002EA4FF) == "mov ecx, 0xa"
      and txt(0x002EA4F8).endswith("0x379f]") and txt(0x00369D57) == "xor r8d, r8d" and txt(0x00369E36) == "mov qword ptr [rbx + 0xa0], r8"
      and not direct,
      "slot +0xA0: null at boot (00369D30), 002E6D60 for heaps 6 and 0xA (002EA320 via 0036C5A0); no other writer")
# H2 - 002E6D60 always returns 0; its work is to take the tail of the request list 0215FD88, deliver it (0041E490) and
#      free it (002E9360) - so a failed allocation in arenas 6 / 0xA first retires one pending request, and the allocator
#      never retries on the callback's answer (0036C0B7 `test esi, esi`: esi is the callback's 0)
check("H2", txt(0x002E6D6D) == "jne 0x2e6e1e" and txt(0x002E6E1E) == "xor eax, eax" and txt(0x002E6E24).strip() == "ret"
      and txt(0x002E6DDD) == "call 0x41e490" and txt(0x002E6DEA) == "call 0x2e9360" and txt(0x002E6D73).endswith("0x1e7900e]")
      and txt(0x0036C043) == "mov esi, eax" and txt(0x0036C0B7) == "test esi, esi",
      "002E6D60 retires the request list's tail and returns 0")

# ---- SD-166 ----
# A1 - the active arena is set by the push wrapper 0036C1D0 (the only caller of 0036C1F0) and by the allocator's own
#      helpers; every push site whose arena is a constant (directly, or `lea ecx, [reg +- k]` over a register constant)
#      selects 2, 3, 4, 5, 6, 8, 9 or 10 - never 7
R32 = {"rax": "eax", "rbx": "ebx", "rcx": "ecx", "rdx": "edx", "rsi": "esi", "rdi": "edi", "rbp": "ebp", "r12": "r12d"}


def const_of(ins, k, reg):
    r32 = R32.get(reg, reg)
    for i in reversed(ins[:k]):
        o = i.op_str
        if o.startswith(r32 + ",") or o.startswith(reg + ","):
            m = re.match(r"mov \w+, (0x[0-9a-f]+|\d+)$", "%s %s" % (i.mnemonic, o))
            if m:
                return int(m.group(1), 0)
            if i.mnemonic == "xor" and o in ("%s, %s" % (r32, r32), "%s, %s" % (reg, reg)):
                return 0
            return None
    return None


arena = collections.defaultdict(list)
for f, s in callers(0x0036C1D0):
    ins = [i for i in R.md.disasm(R.at(f, SZ.get(f, 0x3000)), f) if i.address < s]
    k = next((j for j in range(len(ins) - 1, max(-1, len(ins) - 16), -1) if re.match(r"(ecx|rcx|cl)\b", ins[j].op_str)), None)
    v = "var"
    if k is not None:
        i, o = ins[k], ins[k].op_str
        m = re.match(r"ecx, (0x[0-9a-f]+|\d+)$", o)
        m2 = re.match(r"ecx, \[(\w+) ([+-]) (0x[0-9a-f]+|\d+)\]$", o)
        if i.mnemonic == "mov" and m:
            v = int(m.group(1), 0)
        elif i.mnemonic == "lea" and m2:
            b = const_of(ins, k, m2.group(1))
            v = b + int(m2.group(3), 0) * (1 if m2.group(2) == "+" else -1) if b is not None else "var"
    arena[v].append((f, s))
consts = {k: len(v) for k, v in arena.items() if k != "var"}
print("      push sites by arena: %s; variable %d" % (dict(sorted(consts.items())), len(arena["var"])))
check("A1", len(callers(0x0036C1F0)) == 1 and callers(0x0036C1F0)[0][0] == 0x0036C1D0 and 7 not in consts
      and sum(consts.values()) + len(arena["var"]) == len(callers(0x0036C1D0)),
      "no constant push site selects arena 7 (%d constant, %d variable of %d)" % (sum(consts.values()), len(arena["var"]), len(callers(0x0036C1D0))))

# ---- SD-167 ----
# K1 - the handle-issuing path 0036C4B0 is reached from 0036B160 and 0036B980 only; 0036B160 has 13 call sites in nine
#      functions, and 0036B980's one caller 0036B970 has two (00378BC0, 003DF2C0)
h = sorted(set(f for f, _ in callers(0x0036B160)))
check("K1", sorted(set(f for f, _ in callers(0x0036C4B0))) == [0x0036B160, 0x0036B980] and len(callers(0x0036B160)) == 13
      and h == [0x002E60F0, 0x002E6700, 0x002E6EB0, 0x0036ED50, 0x003A13F0, 0x003AB8B0, 0x003DC5B0, 0x003DD4C0, 0x0050DAD0]
      and callers(0x0036B980) == [(0x0036B970, 0x0036B97B)] and sorted(set(f for f, _ in callers(0x0036B970))) == [0x00378BC0, 0x003DF2C0],
      "handle callers: 0036B160 <- 9 functions (13 sites); 0036B980 <- 0036B970 <- 00378BC0, 003DF2C0")
print("FAILS %d" % fails)
