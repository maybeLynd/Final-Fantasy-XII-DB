"""bitsweep.py - independent whole-image sweep for writes of one flag bit (SWE2-AUDIT-SPEC review helper, 2026-09-30).

Walks every listed function (graph/functions.tsv) plus every .pdata range not inside a listed function, and reports every
instruction that can set or clear bit B of the dword/qword at [base + D0], in ALL of these shapes:
  M  memory-destination or/and/xor/bts/btr/btc at ANY width (byte/word/dword/qword) and displacement D0..D0+3,
     immediate or register source (register resolved from a mov/movabs within the 6 previous instructions);
  S  register read-modify-write: a store `mov [base + d], r` (d in D0..D0+3, width covering bit B) preceded within 6
     instructions by `or/bts/and/btr/xor/shl` on the same register (any size alias) that produces or removes bit B.
Base registers rsp/rbp/rip are excluded. Output: (owner, addr, shape, op, effect). Read-only on the image.
"""
import os, re, sys, bisect
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

md = Cs(CS_ARCH_X86, CS_MODE_64)   # no detail: fast text sweep
W = {"byte": 8, "word": 16, "dword": 32, "qword": 64}
ALIAS = {}
for q, dd, w, b in [("rax", "eax", "ax", "al"), ("rbx", "ebx", "bx", "bl"), ("rcx", "ecx", "cx", "cl"), ("rdx", "edx", "dx", "dl"),
                    ("rsi", "esi", "si", "sil"), ("rdi", "edi", "di", "dil"), ("rbp", "ebp", "bp", "bpl"), ("rsp", "esp", "sp", "spl")]:
    for n in (q, dd, w, b): ALIAS[n] = q
for k in range(8, 16):
    for n in ("r%d" % k, "r%dd" % k, "r%dw" % k, "r%db" % k): ALIAS[n] = "r%d" % k
MEM = re.compile(r"^(byte|word|dword|qword) ptr \[(\w+)(?: \+ (0x[0-9a-f]+|\d+))?\], (.+)$")


def ranges():
    out = list(tk.flist)
    for b, e in tk.pdata:
        o, how = tk.owner(b)
        if how == "pdata": out.append((b, e - b))
    return sorted(set(out))


def body(f, n):
    o = tk.off(f)
    if o is None or n <= 0 or n > 0x40000: return []
    return list(md.disasm(tk.d[o:o + n], f))


def imm(s):
    try: return int(s, 0)
    except ValueError: return None


def sweep(D0, B):
    hits = []
    for f, n in ranges():
        xs = body(f, n)
        for k, x in enumerate(xs):
            m = MEM.match(x.op_str)
            mn = x.mnemonic
            if m and m.group(2) not in ("rsp", "rbp", "rip"):
                size, base, disp, src = m.groups()
                dsp = imm(disp) if disp else 0
                pos = B - 8 * (dsp - D0)
                if D0 <= dsp <= D0 + 3 and 0 <= pos < W[size]:
                    if mn in ("or", "and", "xor", "bts", "btr", "btc"):
                        v = imm(src)
                        if v is None:   # register source: resolve a recent constant
                            for y in reversed(xs[max(0, k - 6):k]):
                                mm = re.match(r"(\w+), (0x[0-9a-f]+|\d+)$", y.op_str)
                                if y.mnemonic in ("mov", "movabs") and mm and ALIAS.get(mm.group(1)) == ALIAS.get(src):
                                    v = int(mm.group(2), 0); break
                        if v is None:
                            hits.append((f, x.address, "M?", "%s %s" % (mn, x.op_str), "register source unresolved")); continue
                        v &= (1 << W[size]) - 1
                        if mn in ("bts", "btr", "btc"):
                            if v == pos: hits.append((f, x.address, "M", "%s %s" % (mn, x.op_str), {"bts": "set", "btr": "clear", "btc": "toggle"}[mn]))
                        elif mn == "or" and (v >> pos) & 1:
                            hits.append((f, x.address, "M", "%s %s" % (mn, x.op_str), "set"))
                        elif mn == "and" and not (v >> pos) & 1:
                            hits.append((f, x.address, "M", "%s %s" % (mn, x.op_str), "clear"))
                        elif mn == "xor" and (v >> pos) & 1:
                            hits.append((f, x.address, "M", "%s %s" % (mn, x.op_str), "toggle"))
                    elif mn == "mov" and ALIAS.get(src):
                        r = ALIAS[src]
                        for y in reversed(xs[max(0, k - 6):k]):
                            ym = re.match(r"(\w+), (.+)$", y.op_str)
                            if not ym or ALIAS.get(ym.group(1)) != r: continue
                            v = imm(ym.group(2))
                            eff = None
                            if y.mnemonic == "bts" and v == pos: eff = "set"
                            elif y.mnemonic == "btr" and v == pos: eff = "clear"
                            elif y.mnemonic == "or" and v is not None and (v >> pos) & 1: eff = "set"
                            elif y.mnemonic == "and" and v is not None and not ((v & ((1 << W[size]) - 1)) >> pos) & 1: eff = "clear"
                            elif y.mnemonic == "shl" and v == pos: eff = "set-var(shl)"
                            if eff:
                                hits.append((f, x.address, "S", "%s %s <- %s %s" % (mn, x.op_str, y.mnemonic, y.op_str), eff))
                            break
    return hits


if __name__ == "__main__":
    D0, B = int(sys.argv[1], 0), int(sys.argv[2], 0)
    hs = sweep(D0, B)
    print("ranges swept %d; hits %d" % (len(ranges()), len(hs)))
    for h in sorted(hs):
        print("  %08X %08X %-2s %-60s %s" % h)
