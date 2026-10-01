"""reachdef.py FUNC SITE REG [REG...] - which instructions define REG on the paths reaching SITE inside FUNC.
Backward walk over the function's control-flow graph (direct jumps, fall-through, and MSVC jump tables of the form
`mov e?x, [base + idx*4 + table]` / `add r?x, base` / `jmp r?x` with base = image base 00120000), stopping each path at
the first instruction whose first operand writes the register (any width alias). Calls are assumed to preserve
callee-saved registers (rbx rbp rdi rsi r12-r15) and clobber the others. Reusable; read-only.
Prints each reaching definition and whether the function entry is reachable without one (= a parameter/unknown)."""
import sys, os, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
ALIAS = {"rax": {"rax", "eax", "ax", "al"}, "rbx": {"rbx", "ebx", "bx", "bl"}, "rcx": {"rcx", "ecx", "cx", "cl"},
         "rdx": {"rdx", "edx", "dx", "dl"}, "rsi": {"rsi", "esi", "si", "sil"}, "rdi": {"rdi", "edi", "di", "dil"},
         "rbp": {"rbp", "ebp", "bp", "bpl"}}
for n in range(8, 16): ALIAS["r%d" % n] = {"r%d" % n, "r%dd" % n, "r%dw" % n, "r%db" % n}
CALLEE_SAVED = {"rbx", "rbp", "rdi", "rsi", "r12", "r13", "r14", "r15"}
WRITES = ("mov", "movzx", "movsx", "movsxd", "lea", "xor", "or", "and", "add", "sub", "inc", "dec", "pop", "cmove",
          "cmovne", "cmova", "cmovb", "cmovae", "cmovbe", "cmovg", "cmovl", "cmovge", "cmovle", "cmovs", "cmovns",
          "shl", "shr", "sar", "imul", "neg", "not", "xchg", "setne", "sete", "bts", "btr", "sbb", "adc")
fn = int(sys.argv[1], 16); site = int(sys.argv[2], 16); regs = sys.argv[3:]
body = list(tk.fdis(fn)); by = {x.address: i for i, x in enumerate(body)}
preds = {x.address: set() for x in body}
BASE = 0x00120000
def jt_targets(i):
    # look back for `mov e?x, dword ptr [r? + r?*4 + DISP]` and read entries until they leave the function
    for k in range(i - 1, max(i - 6, -1), -1):
        y = body[k]
        if y.mnemonic == "mov" and "*4 +" in y.op_str and "dword ptr" in y.op_str:
            disp = int(y.op_str.rsplit("+", 1)[1].strip(" ]"), 16)
            out = []
            for e in range(64):
                o = tk.off(BASE + disp + 4 * e)
                if o is None: break
                t = struct.unpack_from("<I", tk.d, o)[0] + BASE
                if t not in by: break
                out.append(t)
            return out
    return []
for i, x in enumerate(body):
    m = x.mnemonic; nxt = body[i + 1].address if i + 1 < len(body) else None
    if m.startswith("j"):
        if x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if t in preds: preds[t].add(x.address)
        elif m == "jmp":
            for t in jt_targets(i): preds[t].add(x.address)
        if m != "jmp" and nxt: preds[nxt].add(x.address)
    elif m == "ret" or (m == "jmp"):
        pass
    elif nxt: preds[nxt].add(x.address)
def writes(x, reg):
    if x.mnemonic == "call": return reg not in CALLEE_SAVED
    if x.mnemonic not in WRITES: return False
    first = x.op_str.split(",")[0].strip()
    if x.mnemonic in ("xchg",): return any(p.strip() in ALIAS[reg] for p in x.op_str.split(","))
    return first in ALIAS[reg]
for reg in regs:
    defs, entry = set(), False
    seen = set(); stack = [site]
    while stack:
        a = stack.pop()
        for p in preds.get(a, ()):
            if p in seen: continue
            seen.add(p)
            x = body[by[p]]
            if writes(x, reg): defs.add(p); continue
            stack.append(p)
        if a == fn: entry = True
        if not preds.get(a) and a == fn: entry = True
    entry = entry or fn in seen or (fn == site)
    print("%s reaching %08X: %s%s" % (reg, site, ", ".join("%08X %s %s" % (d, body[by[d]].mnemonic, body[by[d]].op_str) for d in sorted(defs)) or "-",
                                       "  (+ function entry: parameter/unknown)" if fn in seen or any(fn == s for s in seen) else ""))
