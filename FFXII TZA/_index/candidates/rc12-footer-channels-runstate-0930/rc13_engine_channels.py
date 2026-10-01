"""rc13_engine_channels.py - RC-13 (ORACLE, 2026-09-30): which channel NATIVE code files a request on, and for which
function. The interpreter's REQ family passes the script's own channel operand; native code files requests through two
descriptor builders:
  003DBB60(record rcx, channel dl, function r8w, mode r9d, flag [rsp+0x28])        -> 003DBCF0 (state 1)
  003DBBE0 -> 003DBBF0(target rcx, issuer rdx, channel r8b, function r9w, ...)     -> 003DBCF0 (state 2)
For every call site (raw E8/E9 index, owner by .pdata chain root) the channel register is resolved backwards along the
straight-line predecessor instructions: an immediate, `lea r, [z + n]` with z zeroed, a copy of another resolved
register, `movzx r, byte [rec + 0x88]` (the record's channel count) followed by `dec`/`lea -1` = TOP (count - 1), or a
stack argument. A jump target between the definition and the call is flagged JOIN (then the value is read by hand in
the README). The function operand's source is the nearest preceding footer read (k = (D-2)/2) in the same function.
Control: 0025C4F4 (touch, k=3) must resolve to channel 3 and 002669F5 (main, k=1, record initialiser) to channel 0.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import img

SUBMIT = {0x003DBB60: "edx", 0x003DBBE0: "r8d"}
ALIAS = {"edx": ("edx", "rdx", "dl"), "r8d": ("r8d", "r8", "r8b"), "eax": ("eax", "rax", "al"), "ebx": ("ebx", "rbx", "bl"),
         "ebp": ("ebp", "rbp", "bpl"), "esi": ("esi", "rsi", "sil"), "edi": ("edi", "rdi", "dil"), "ecx": ("ecx", "rcx", "cl"),
         "r9d": ("r9d", "r9", "r9b"), "r10d": ("r10d", "r10", "r10b"), "r13d": ("r13d", "r13", "r13b"),
         "r14d": ("r14d", "r14", "r14b"), "r15d": ("r15d", "r15", "r15b"), "r12d": ("r12d", "r12", "r12b")}


def canon(r):
    for k, v in ALIAS.items():
        if r in v:
            return k
    return r


def targets(ins):
    t = set()
    for x in ins:
        if x.mnemonic.startswith("j") and x.op_str.startswith("0x"):
            t.add(int(x.op_str, 16))
    return t


def resolve(ins, i, reg, jt, depth=0):
    """value of reg just before ins[i], scanning back linearly."""
    reg = canon(reg)
    join = False
    for j in range(i - 1, max(-1, i - 60), -1):
        x = ins[j]
        if ins[j + 1].address in jt:
            join = True
        ops = [o.strip() for o in x.op_str.split(",")]
        if not ops or canon(ops[0]) != reg or x.mnemonic in ("cmp", "test", "push", "bt"):
            continue
        tag = " JOIN" if join else ""
        if x.mnemonic == "mov" and re.match(r"^(0x[0-9a-f]+|\d+)$", ops[1]):
            return "%d%s" % (int(ops[1], 0), tag)
        if x.mnemonic == "xor" and canon(ops[1]) == reg:
            return "0" + tag
        if x.mnemonic == "lea":
            m = re.match(r"\[(\w+) ([+-]) (0x[0-9a-f]+|\d+)\]$", ops[1])
            if m:
                base = resolve(ins, j, m.group(1), jt, depth + 1)
                n = int(m.group(3), 0) * (1 if m.group(2) == "+" else -1)
                if re.match(r"^-?\d+", base or ""):
                    return "%d%s" % (int(base.split()[0]) + n, tag)
                if base and base.startswith("COUNT") and n == -1:
                    return "TOP(count-1)" + tag
                return "(%s)%+d%s" % (base, n, tag)
        if x.mnemonic in ("mov", "movzx") and re.match(r"^byte ptr \[\w+ \+ 0x88\]$", ops[1]):
            return "COUNT" + tag
        if x.mnemonic == "dec":
            base = resolve(ins, j, reg, jt, depth + 1)
            if base and base.startswith("COUNT"):
                return "TOP(count-1)" + tag
            return "(%s)-1%s" % (base, tag)
        if x.mnemonic in ("mov", "movzx") and re.match(r"^\w+$", ops[1]) and depth < 6:
            return resolve(ins, j, ops[1], jt, depth + 1) + tag
        if x.mnemonic == "mov" and "rsp" in ops[1]:
            return "STACK(%s)%s" % (ops[1], tag)
        return "EXPR(%s %s)%s" % (x.mnemonic, x.op_str, tag)
    return "UNRESOLVED"


def footer_k(ins, i):
    for j in range(i - 1, max(-1, i - 40), -1):
        t = ins[j].mnemonic + " " + ins[j].op_str
        m = re.match(r"mov[sz]x \w+, word ptr \[rcx(?: \+ r\w+)? \+ (0x[0-9a-f]+|\d+)\]$", t)
        if m:
            return (int(m.group(1), 0) - 2) // 2
        if ins[j].mnemonic == "call" and ins[j].op_str not in ("0x20e600",):
            return None
    return None


NAMES = {0: "(entry list)", 1: "main", 2: "talk", 3: "touch", 4: "touchon", 5: "touchoff", 6: "across", 7: "spawn",
         8: "fieldsign1", 9: "initevent", 10: "(talk list)", 11: "parameter", 12: "mapjump", 13: "fieldsign2",
         14: "respawn", 15: "(never set)", 16: "talkhold", 17: "talkterm"}


def main():
    rows = []
    for tgt, reg in SUBMIT.items():
        for a, kind in img.calls_to(tgt):
            f = img.owner(a)
            if f is None:
                rows.append((None, a, tgt, "thunk", None))
                continue
            ins = img.fn_ins(f)
            jt = targets(ins)
            i = [n for n, x in enumerate(ins) if x.address == a][0]
            rows.append((f, a, tgt, resolve(ins, i, reg, jt), footer_k(ins, i)))
    print("native submit sites: function, call, builder, channel, footer slot of the function filed (if read just before)")
    for f, a, tgt, ch, k in rows:
        print("  %s %08X -> %08X  channel=%-22s function=%s" % ("%08X" % f if f else "--------", a, tgt, ch,
                                                               ("k=%d %s" % (k, NAMES[k])) if k is not None else "-"))
    c1 = any(a == 0x0025C4F4 and ch.split()[0] == "3" and k == 3 for f, a, t, ch, k in rows)
    c2 = any(a == 0x002669F5 and ch.split()[0] == "0" and k == 1 for f, a, t, ch, k in rows)
    print("CONTROL touch k=3 -> channel 3 at 0025C4F4: %s" % ("PASS" if c1 else "FAIL"))
    print("CONTROL main k=1 -> channel 0 at 002669F5: %s" % ("PASS" if c2 else "FAIL"))
    return 0 if c1 and c2 else 1


if __name__ == "__main__":
    sys.exit(main())
