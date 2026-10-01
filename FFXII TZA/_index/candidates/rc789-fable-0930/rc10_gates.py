# rc10_gates.py - RC-10: does any caller of the formatted log call 005CDAA0 condition the call on a global or per-thread
# value acting as a verbosity control?
# For every E8/E9 site to 005CDAA0 (raw index), inside the owning listed function (linear disassembly):
#  - collect the conditional jumps within the 24 instructions before the site whose fall-through or target leads to the
#    site (a jcc before the site with no other jcc target landing between it and the site is the guarding branch);
#  - for each guarding jcc, find the flag-setting instruction just before it (cmp/test/bt) and classify its operands:
#      GLOBAL   : a rip-relative memory operand, or a register loaded from a rip-relative cell within the 12 prior instrs
#      TLS      : a gs:/fs: operand in the same window
#      LOCAL    : anything else (argument, heap field, return value)
#  - report per site; GLOBAL/TLS sites are the candidates to read.
# Control: a synthetic self-check is not available; instead the known ungated sink call is at least found as a site,
# and the count of sites must equal SWE2-CONTRACT's 245 (log_channels.out: "call/jmp sites: 245").
import os, re, json, bisect, collections
os.chdir(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch")
g = {}
exec(open("disw.py").read().split("fn = int")[0], g)
funcs, off, d = g["funcs"], g["off"], g["d"]
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
raw = json.load(open("tools/rawcalls.json"))
sites = sorted(int(s, 16) for s in raw.get("5CDAA0", []))
fl = sorted(funcs)
def owner(a):
    k = bisect.bisect_right(fl, a) - 1
    return fl[k] if k >= 0 and a < fl[k] + funcs[fl[k]] else None
def ripea(i):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return (i.address + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)) if m else None
cls = collections.Counter()
rows = []
for s in sites:
    fn = owner(s)
    if fn is None:
        rows.append((s, None, "UNLISTED", "")); cls["unlisted"] += 1; continue
    ins = list(md.disasm(bytes(d[off(fn):off(fn) + funcs[fn]]), fn))
    idx = {x.address: k for k, x in enumerate(ins)}
    k = idx.get(s)
    if k is None:
        rows.append((s, fn, "NOBOUNDARY", "")); cls["noboundary"] += 1; continue
    jt = {int(x.op_str, 16) for x in ins if x.mnemonic.startswith("j") and re.fullmatch(r"0x[0-9a-f]+", x.op_str)}
    guards = []
    for q in range(k - 1, max(-1, k - 25), -1):
        x = ins[q]
        if x.mnemonic.startswith("j") and x.mnemonic != "jmp":
            guards.append(q)
            if len(guards) >= 2:
                break
        if x.address in jt and q != k:
            # a join point: stop after recording the first guard beyond it
            if guards:
                break
    kinds = []
    for q in guards:
        f = ins[q - 1] if q > 0 else None
        if f is None or f.mnemonic not in ("cmp", "test", "bt", "ucomiss", "comiss"):
            kinds.append(("?", "%08X %s" % (ins[q].address, ins[q].mnemonic))); continue
        txt = f.mnemonic + " " + f.op_str
        k2 = "LOCAL"
        if ripea(f) is not None:
            k2 = "GLOBAL %08X" % ripea(f)
        elif "gs:" in f.op_str or "fs:" in f.op_str:
            k2 = "TLS"
        else:
            regs = set(re.findall(r"\b(r\w+|e\w+|\w+l)\b", f.op_str))
            for y in ins[max(0, q - 14):q - 1]:
                dst = y.op_str.split(",")[0].strip()
                if dst in regs and ripea(y) is not None and y.mnemonic.startswith("mov"):
                    k2 = "GLOBAL-VIA-REG %08X (%08X)" % (ripea(y), y.address)
                if dst in regs and ("gs:" in y.op_str or "fs:" in y.op_str):
                    k2 = "TLS-VIA-REG (%08X)" % y.address
        kinds.append((k2, "%08X %s | %08X %s" % (f.address, txt, ins[q].address, ins[q].mnemonic)))
    tag = "UNGUARDED" if not guards else ("CANDIDATE" if any(a.startswith(("GLOBAL", "TLS")) for a, _ in kinds) else "LOCAL-GUARD")
    cls[tag] += 1
    rows.append((s, fn, tag, " || ".join("%s: %s" % kk for kk in kinds)))
print("sites %d (SWE2-CONTRACT census: 245) in %d functions" % (len(sites), len({r[1] for r in rows})))
print("classes:", dict(cls))
cands = [r for r in rows if r[2] == "CANDIDATE"]
gl = collections.Counter(re.findall(r"GLOBAL(?:-VIA-REG)? ([0-9A-F]{8})", " ".join(r[3] for r in cands)))
print("globals compared in candidate guards (cell: sites):", dict(gl.most_common(40)))
for r in rows:
    if r[2] == "CANDIDATE":
        print("%08X in %08X  %s" % (r[0], r[1], r[3][:230]))
