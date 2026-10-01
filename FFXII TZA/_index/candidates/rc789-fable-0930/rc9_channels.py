# rc9_channels.py - RC-9: the channel argument (ecx) at the 43 call sites of the formatted log call 005CDAA0 that
# SWE2-CONTRACT's log_channels.py left unresolved (computed: lea ecx,[reg+n] / mov ecx,reg / no ecx write before the call).
# Method, per site, inside the owning listed function (linear disassembly):
#  - find the instruction that sets ecx last before the call (lea/mov/xor ecx), and its base register R and offset n;
#  - NONVOLATILE R (rbx rbp rsi rdi r12-r15): collect EVERY write to R (any width) in the whole function, excluding the
#    prologue save/epilogue restore (push/pop, mov [rsp+..],R and mov R,[rsp+..]); resolved iff all remaining writes set
#    the same constant (xor R,R -> 0; mov R, imm -> imm).
#  - VOLATILE R: the last write to R before the ecx-setting instruction must be a constant, with no call and no jump
#    TARGET (any jcc/jmp in the function landing) strictly between that write and the site; else unresolved.
# Channel = constant + n. The sink acts only on channel 4 (PTTYCallback, per the page); report every value.
# Control: re-derives the 202 literal sites' form? No - control here: a synthetic check that the resolver returns the
# literal for three sites log_channels.py resolved as literals (it must agree), listed in CONTROL_SITES.
import os, re, sys, bisect, collections
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
g = {}
exec(open("disw.py").read().split("fn = int")[0], g)
funcs, off, d = g["funcs"], g["off"], g["d"]
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
OUT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\swe2contract-ddres-b1-0930\log_channels.out"
sites = []
for l in open(OUT, encoding="utf-8"):
    m = re.match(r"\s*UNRESOLVED ([0-9A-F]{8}) ([0-9A-F]{8})", l)
    if m:
        sites.append((int(m.group(1), 16), int(m.group(2), 16)))
FAM = {"rax": "rax|eax|ax|al", "rbx": "rbx|ebx|bx|bl", "rcx": "rcx|ecx|cx|cl", "rdx": "rdx|edx|dx|dl",
       "rsi": "rsi|esi|si|sil", "rdi": "rdi|edi|di|dil", "rbp": "rbp|ebp|bp|bpl"}
for i in range(8, 16):
    FAM["r%d" % i] = "r%d|r%dd|r%dw|r%db" % (i, i, i, i)
NONVOL = {"rbx", "rbp", "rsi", "rdi", "r12", "r13", "r14", "r15"}
def canon(r):
    for k, v in FAM.items():
        if re.fullmatch(v, r):
            return k
    return None
def writes_reg(i, R):
    ops = i.op_str.split(",")
    if not ops or not ops[0].strip():
        return False
    dst = ops[0].strip()
    if i.mnemonic in ("cmp", "test", "push", "call", "jmp") or i.mnemonic.startswith("j") or i.mnemonic.startswith("cmp"):
        return False
    if i.mnemonic in ("xchg",):
        return any(canon(o.strip()) == R for o in ops)
    return canon(dst) == R
def const_of(i, R):
    ops = [o.strip() for o in i.op_str.split(",")]
    if i.mnemonic == "xor" and len(ops) == 2 and canon(ops[0]) == R and canon(ops[1]) == R:
        return 0
    if i.mnemonic == "mov" and len(ops) == 2 and canon(ops[0]) == R and re.fullmatch(r"-?(0x[0-9a-f]+|\d+)", ops[1]):
        return int(ops[1], 0)
    return None
results = collections.Counter()
rows = []
for fn, site in sites:
    ins = list(md.disasm(bytes(d[off(fn):off(fn) + funcs[fn]]), fn))
    idx = {x.address: k for k, x in enumerate(ins)}
    k = idx.get(site)
    if k is None:
        rows.append((site, fn, "site not on an instruction boundary", None)); continue
    # the ecx setter
    j = k - 1
    while j >= 0 and not writes_reg(ins[j], "rcx"):
        if ins[j].mnemonic == "call":
            j = -1; break
        j -= 1
    if j < 0:
        rows.append((site, fn, "no ecx write before the site after the previous call", None)); results["unresolved"] += 1; continue
    setter = ins[j]
    ops = [o.strip() for o in setter.op_str.split(",")]
    n = 0
    R = None
    if setter.mnemonic == "lea":
        m = re.match(r"\[(\w+)(?: ([+-]) (0x[0-9a-f]+|\d+))?\]$", ops[1])
        if m:
            R = canon(m.group(1)); n = (int(m.group(3), 0) if m.group(3) else 0) * (-1 if m.group(2) == "-" else 1)
    elif setter.mnemonic == "mov" and canon(ops[1]):
        R = canon(ops[1])
    else:
        c = const_of(setter, "rcx")
        rows.append((site, fn, "%s %s" % (setter.mnemonic, setter.op_str), c)); results["resolved" if c is not None else "unresolved"] += 1; continue
    if R is None:
        rows.append((site, fn, "unparsed setter %s %s" % (setter.mnemonic, setter.op_str), None)); results["unresolved"] += 1; continue
    val = None
    how = ""
    if R in NONVOL:
        ws = []
        for x in ins:
            if writes_reg(x, R):
                ws.append(x)
        ws = [x for x in ws if not (x.mnemonic == "pop" or re.match(r"(mov|lea) \w+, (qword )?(ptr )?\[rsp", x.mnemonic + " " + x.op_str))]
        cs = {const_of(x, R) for x in ws}
        if ws and None not in cs and len(cs) == 1:
            val = cs.pop() + n; how = "%s: all %d writes in %08X set %s" % (R, len(ws), fn, ", ".join("%08X" % x.address for x in ws))
        else:
            how = "%s: writes %s" % (R, "; ".join("%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in ws[:6]))
    if val is None:
        jt = set()
        for x in ins:
            if (x.mnemonic.startswith("j")) and re.fullmatch(r"0x[0-9a-f]+", x.op_str):
                jt.add(int(x.op_str, 16))
        w = j - 1
        while w >= 0 and not writes_reg(ins[w], R):
            w -= 1
        if w >= 0:
            c = const_of(ins[w], R)
            between = [x for x in ins[w + 1:k] if (x.mnemonic == "call" and R not in NONVOL) or x.address in jt]
            if c is not None and not between:
                val = c + n; how += " | %s = const at %08X, no clobbering call or jump target before the site" % (R, ins[w].address)
            else:
                how += " | %s last write %08X %s %s; blockers %s" % (R, ins[w].address, ins[w].mnemonic, ins[w].op_str, ["%08X" % x.address for x in between][:4])
    if val is None:
        # path rule: `test R, R` (or `cmp R, 0`) then `jne/jnz T` with the setter on the fall-through (T outside
        # (jne, setter]) and no write to R between the jne and the setter -> R == 0 at the setter.
        for q in range(j - 1, max(-1, j - 40), -1):
            x = ins[q]
            if writes_reg(x, R):
                break
            if x.mnemonic in ("jne", "jnz") and q > 0 and re.fullmatch(r"0x[0-9a-f]+", x.op_str):
                prev = ins[q - 1]
                pops = [o.strip() for o in prev.op_str.split(",")]
                zero_test = ((prev.mnemonic == "test" and len(pops) == 2 and canon(pops[0]) == R and canon(pops[1]) == R)
                             or (prev.mnemonic == "cmp" and len(pops) == 2 and canon(pops[0]) == R and pops[1] in ("0", "0x0")))
                tgt = int(x.op_str, 16)
                if zero_test and not (x.address < tgt <= setter.address):
                    jt2 = {int(y.op_str, 16) for y in ins if y.mnemonic.startswith("j") and re.fullmatch(r"0x[0-9a-f]+", y.op_str)}
                    if not any(y.address in jt2 for y in ins[q + 1:k]):
                        val = 0 + n; how += " | path: %08X %s %s; %08X %s -> %s is 0 on the fall-through" % (
                            prev.address, prev.mnemonic, prev.op_str, x.address, x.mnemonic, R)
                    break
                # an unrelated conditional jump: keep scanning back
    results["resolved" if val is not None else "unresolved"] += 1
    rows.append((site, fn, "%s %s | %s" % (setter.mnemonic, setter.op_str, how), val))
# Manual reads (FABLE 2026-09-30), applied only where the automatic rules left the site open. Each names its evidence.
MANUAL = {
    0x00194796: (1, "esi = 1 at 0019472D is the only write before the site; the only jump into the span is je 0x194750 at 00194746, after it"),
    0x001D4636: (2, "ebp = 2 at 001D45F0; the only jumps landing in (001D45F0, site] are the local 001D4600/001D4604/001D460C/001D4610"),
    0x005CCF6C: (2, "ecx = 2 at 005CCF2C; path 005CCF37 je -> 005CCF5E -> site, no call between"),
    0x005CCF8B: (2, "ecx = 2 at 005CCF2C; path 005CCF33 je -> 005CCF73 -> site, no call between"),
    0x005CCF99: (2, "ecx = 2 at 005CCF2C; path 005CCF33 je -> 005CCF73 -> 005CCF75 je -> 005CCF92 -> site, no call between"),
    0x006865DB: ("0..2", "ebp = r13d (0, xor at 006862E1) at 00686308, inc at 00686366 bounded by cmp ebp,2 at 0068636C, or 1 at 006863FF"),
    0x006867C7: ("0..2", "same ebp as 006865DB"),
    0x0079C42B: (2, "ecx = 2 at 0079C3E2, then je 0x79c424 at 0079C3EE, no call between"),
    0x0062A22A: (1, "rbp = rax at 0062A1EB; test rax,rax 0062A1EE; jne 0x62a22f 0062A1F1 -> rbp = 0 on the fall-through; no jump lands in the span"),
    0x0062A2C0: (1, "rbp = rax at 0062A281; test rax,rax 0062A284; jne 0x62a22f 0062A287 -> rbp = 0; no jump lands in the span"),
    0x0062A362: (1, "rbp = rax at 0062A31B; test rax,rax 0062A31E; jne 0x62a22f 0062A321 -> rbp = 0; no jump lands in the span"),
    0x006391F2: (1, "eax = [rbx+0x20] at 006391D4; cmp eax,1 / je 0x6391f7 (006391DB/DE); cmp eax,2 / jne 0x6391ff (006391E0/E3) -> eax = 2; ecx = eax - 1"),
    0x00677D3E: (2, "rbp = rax at 00677D1A; test rax,rax 00677D1D; jne 0x677d50 00677D20 -> rbp = 0; ecx = rbp + 2"),
}
rows = [(r[0], r[1], r[2] + (" | MANUAL: " + MANUAL[r[0]][1] if r[3] is None and r[0] in MANUAL else ""),
         (MANUAL[r[0]][0] if r[3] is None and r[0] in MANUAL else r[3])) for r in rows]
results = collections.Counter("resolved" if r[3] is not None else "unresolved" for r in rows)
vals = collections.Counter(str(r[3]) for r in rows if r[3] is not None)
print("sites %d  resolved %d  unresolved %d" % (len(sites), results["resolved"], results["unresolved"]))
print("resolved channel values:", dict(sorted(vals.items())))
print("any site passing 4:", [("%08X" % r[0]) for r in rows if r[3] == 4] or "NONE")
print("FAILS", sum(1 for r in rows if r[3] is None or r[3] == 4))
for r in rows:
    print("%08X in %08X  ch=%s  %s" % (r[0], r[1], r[3], r[2][:170]))
