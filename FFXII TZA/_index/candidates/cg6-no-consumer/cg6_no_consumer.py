"""cg6_no_consumer.py - CG-6: who consumes the render-command double buffer 02EBEFC0 / 02EBEFD8 (index 02EBEFF0)?
(FABLE, Claude Opus 5.5, 2026-09-27). Static.

  C1 the submit 003A1DB0 flips the index, takes the finished half's record count as (cursor - begin) >> 4, hands
     (begin, count) to 0036F360, and resets the new half's cursor to its begin.
  C2 0036F360 calls nothing and reads one dword of the batch - the last record's first dword, to append or overwrite
     an end tag {0x10000000, 0}; everything else it writes goes to the single cell 02EBA3F8 (address & 0x3FF0, count,
     0x100) - UQ-211's PS2 DMA registers collapsed onto one word.
  C3 every descriptor-forming site in the 36 functions that reference the pair or its index indexes it with the CURRENT index
     loaded from 02EBEFF0, except 003A1DB0, the only site that forms the finished half.
  C4 the current-descriptor getter 005044B0's callers read the begin pointer only as an end bound
     (end = [desc + 0x10] << 4 + [desc]) or as the used count ((cursor - begin) >> 4) before the flush 00504450, which
     appends the end tag and tail-jumps to the submit; planted positive: the submit's own begin read.
  C5 the shared emitter 003A22A0 appends: it reads the cursor [desc + 8] and advances it by 0x10.
  C6 OPUS's lead (2026-09-13): the arena pointer's alias 01EF9438 is pointed either at the arena (00370DF0) or at a
     static buffer 02AD9EC0 (00370DE0), and its readers 00370BD0 / 00370CD0 write 12-byte list nodes into it and a
     count at +0x1804 - scratch space, not a walk of command records.
  C7 the descriptor-passing sites (00474600, 0051BC70, 003649A0 through the thunk 00474650) all hand it to 003A22A0.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from collections import Counter
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
W = ROOT / "Database/Tools/work"
d = (W / "exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(W / "graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: SIZES[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a): return list(cs.disasm(d[off(a):off(a) + SIZES[a]], a))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
RIP = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+)\]")
def tgt(x):
    m = RIP.search(x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

s = body(0x3A1DB0); sd = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in s}
check("C1 the submit flips the index, counts (cursor - begin) >> 4, calls 0036F360(begin, count), resets the new cursor",
      tgt(s[2]) == 0x2EBEFF0 and sd.get(0x3A1DC8) == "sub eax, edx" and tgt([x for x in s if x.address == 0x3A1DCA][0]) == 0x2EBEFF0
      and sd.get(0x3A1DE8) == "sub rdx, rcx" and sd.get(0x3A1DEB) == "sar rdx, 4" and sd.get(0x3A1DEF) == "call 0x36f360"
      and sd.get(0x3A1DF4) == "mov rcx, qword ptr [rbx]" and sd.get(0x3A1DFA) == "mov qword ptr [rbx + 8], rcx")

p = body(0x36F360)
reads = [x for x in p if "ptr [" in x.op_str and "rip" not in x.op_str and x.op_str.split(",")[0].strip() in ("eax", "ecx", "edx", "rax", "rcx", "rdx", "r8", "r9")]
cells = {tgt(x) for x in p if tgt(x) is not None}
check("C2 0036F360 calls nothing, reads one batch dword (the last record), writes only the end tag and the cell 02EBA3F8",
      not any(x.mnemonic == "call" for x in p) and [x.address for x in reads] == [0x36F372]
      and cells == {0x2EBA3F8}, "reads %s, cells %s" % (["%08X" % x.address for x in reads], ["%08X" % c for c in cells]))

funcs = set(); formers = []
for f in sorted(SIZES):
    o = off(f)
    if o is None or SIZES[f] <= 0 or not (0x160000 <= f < 0x880000): continue
    raw = d[o:o + SIZES[f]]
    ins = None
    for x in cs.disasm(raw, f):
        t = tgt(x)
        if t is not None and 0x2EBEFC0 <= t < 0x2EBEFF4:
            funcs.add(f)
    if f in funcs:
        ins = body(f)
        for k, x in enumerate(ins):
            if x.mnemonic == "lea" and re.search(r"\[(\w+) \+ (\w+)\*8\]$", x.op_str):
                b = re.search(r"\[(\w+) \+", x.op_str).group(1)
                prev = ins[max(0, k - 12):k]
                if any(q.mnemonic == "lea" and q.op_str.startswith(b + ",") and tgt(q) == 0x2EBEFC0 for q in prev):
                    loads = [q for q in prev if tgt(q) == 0x2EBEFF0]
                    formers.append((f, x.address, loads[-1].mnemonic + " " + loads[-1].op_str.split(",")[0] if loads else "?"))
cur = [s_ for s_ in formers if s_[2].startswith("mov e") or s_[2].startswith("mov r")]
fin = [s_ for s_ in formers if s_ not in cur]
check("C3 all descriptor-forming sites use the current index loaded from 02EBEFF0, except the submit",
      len(funcs) == 36 and len(formers) == 21 and {s_[0] for s_ in fin} == {0x3A1DB0},
      "functions %d, sites %d, non-current %s" % (len(funcs), len(formers), sorted({"%08X" % s_[0] for s_ in fin})))

P = ROOT / "Database/FFXII TZA/_index/candidates/f1-weather-apply-thread/f1_thread_reach.py"
g = {"__file__": str(P)}; exec(compile(open(P, encoding="utf-8").read().split("APPLY = 0x26D910")[0], str(P), "exec"), g)
def begin_uses(getter):
    out = []
    for c in sorted(g["callers"].get(getter, ())):
        ins = body(c)
        for k, x in enumerate(ins):
            if x.mnemonic == "call" and x.op_str == hex(getter):
                for j, y in enumerate(ins[k + 1:k + 12]):
                    if re.search(r"\[rax\]", y.op_str):
                        before = [z.mnemonic + " " + z.op_str for z in ins[k + 1:k + 1 + j]]
                        after = [z.mnemonic + " " + z.op_str for z in ins[k + 2 + j:k + 10 + j]]
                        bound = any("[rax + 0x10]" in z for z in before) and any(z.startswith("shl") and z.endswith(", 4") for z in before)
                        used = y.mnemonic == "sub" and any(z.startswith("sar") and z.endswith(", 4") for z in after) and "call 0x504450" in after
                        out.append((y.address, y.mnemonic + " " + y.op_str, bound or used))
                    if y.mnemonic in ("call", "ret") or (y.op_str.split(",")[0].strip() == "rax" and y.mnemonic in ("mov", "lea", "xor", "pop")): break
    return out
bu = begin_uses(0x5044B0)
fl = dis(0x504450, 0x504485)
check("C4 the getter's callers read begin only as the end bound (begin + capacity*16) or as the used count before the flush 00504450, which appends the end tag and tail-jumps to the submit; planted positive: the submit's own begin read",
      len(bu) > 0 and all(y[2] for y in bu) and sd.get(0x3A1DE5) == "mov rcx, qword ptr [r8]"
      and fl.get(0x50445D) == "mov qword ptr [rax], 0x10000000" and fl.get(0x504480) == "jmp 0x3a1db0",
      "%d begin reads, all end-bound: %s" % (len(bu), all(y[2] for y in bu)))

e = dis(0x3A22E5, 0x3A2302)
check("C5 the shared emitter 003A22A0 reads the cursor [desc + 8] and advances it by 0x10",
      e.get(0x3A22E5) == "mov r8, qword ptr [r13 + 0x10]" and e.get(0x3A22F2) == "mov rdx, qword ptr [r8 + 8]"
      and e.get(0x3A22F9) == "lea rcx, [rdx + 0x10]" and e.get(0x3A22FD) == "mov qword ptr [r8 + 8], rcx")

a1 = dis(0x370DE0, 0x370DFF); r1 = body(0x370BD0); r2 = body(0x370CD0)
alias_uses = [x for x in r1 + r2 if tgt(x) == 0x1EF9438]
check("C6 the alias 01EF9438 points at the arena or at 02AD9EC0, and its readers write list nodes and a count into it",
      tgt(list(cs.disasm(d[off(0x370DE0):off(0x370DE7)], 0x370DE0))[0]) == 0x2AD9EC0
      and tgt(list(cs.disasm(d[off(0x370DF0):off(0x370DF7)], 0x370DF0))[0]) == 0x1FD4A78
      and tgt(list(cs.disasm(d[off(0x370DF7):off(0x370DFE)], 0x370DF7))[0]) == 0x1EF9438
      and len(alias_uses) >= 3 and any(x.op_str == "dword ptr [r9 + 0x1804], ebx" for x in r1)
      and any(x.op_str == "qword ptr [rbx + 4], 0xffffffffffffffff" for x in r1) and any("[rdx + 0x1804]" in x.op_str for x in r2))
t1 = dis(0x474650, 0x474673); t2 = dis(0x47462C, 0x474646); t3 = dis(0x51BCF9, 0x51BD23)
check("C7 the sites that hand the descriptor on give it to the same emitter: 00474600 and 0051BC70 call 003A22A0, and 003649A0's 00474650 is a jmp to it",
      t1.get(0x47466E) == "jmp 0x3a22a0" and t2.get(0x47463C) == "call 0x3a22a0" and t2.get(0x474641) == "call 0x3a1db0"
      and t3.get(0x51BD1E) == "call 0x3a22a0" and any(x.op_str == "0x474650" for x in body(0x3649A0) if x.mnemonic == "call"))
print("FAILS", fails)
sys.exit(1 if fails else 0)
