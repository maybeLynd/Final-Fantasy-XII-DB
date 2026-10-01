# callee_nonvol.py - for each direct callee of 002E45E0: does its own body write r14 or rbp, and if so is the register
# saved in its prologue (push / mov [rsp+..],reg) and restored before each ret? Direct level only (not transitive).
import subprocess, re, sys
CALLEES = sys.argv[1:]
REGS = {"r14": r"\b(r14|r14d|r14w|r14b)\b", "rbp": r"\b(rbp|ebp|bp|bpl)\b"}
for c in CALLEES:
    out = subprocess.run([sys.executable, "disr.py", c], capture_output=True, text=True).stdout.splitlines()
    head = out[0] if out else "?"
    body = [l for l in out[1:] if l.strip()]
    res = []
    for r, rx in REGS.items():
        writes = [l for l in body if re.search(r"^\s*\S+ (mov|lea|xor|add|sub|and|or|movzx|movsxd|movsx|inc|dec|pop|cmov\w+|imul|shl|shr|sar|neg|not|xchg) " + rx.replace(r"\b(", r"(").rstrip(r"\b") , l)
                  and not re.search(r"\[", l.split(" ", 3)[-1].split(",")[0])]
        pushes = [l for l in body if re.search(r"push " + rx, l) or re.search(r"mov qword ptr \[(rsp|r11|rax)[^\]]*\], " + r, l)]
        rets = [l for l in body if re.search(r"\bret\b", l)]
        pops = [l for l in body if re.search(r"pop " + rx, l) or re.search(r"mov " + r + r", qword ptr \[rsp", l)]
        if writes:
            res.append("%s: %d writes, saved=%d, restores=%d, rets=%d" % (r, len(writes), len(pushes), len(pops), len(rets)))
    print(c, "|", head[:70], "|", "; ".join(res) if res else "no r14/rbp write")
