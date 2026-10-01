"""rc16_check.py - RC-16: who can occupy a record, when the register file is zeroed, and where shipped scripts read a
register before writing it. ORACLE, 2026-09-30. Static.

Image (through ../k14-closure-stores-0930):
 S1 ActorStorage_InitializeRecord 00266530 has one rel32 caller, 00267B79 in the pool allocator 002679F0, and no rip
    reference (not reached through a pointer);
 S2 002679F0 has one caller, ActorSystem_InitializeManagerRuntime 0026CE60 (0026CEB0), and zeroes the whole pool with
    memset at 00267A8B right after the allocation call at 00267A79; 0026CE60's callers are listed.
Authored data (the decompiled US corpus, ../../../../Tools/work/FABLE/pub140-scratch/corpus/us, 1,114 scripts):
 D1 every `while ((regI1 != -1 && regI0 < 64))` loop and the function it sits in (control: gol_b01 spawn00 must be
    among them);
 D2 every by-name request of a function called エントリキャラ乗っ取り解除 / エントリキャラ乗っ取り２ (the F0..F3 reader and
    writer the interpreter page and FABLE cite), and the computed-target requests in rbn_a03.
"""
import collections, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K  # noqa: E402
from capstone import x86 as X  # noqa: E402
R = K.R
FAILS = 0


def check(ok, name):
    global FAILS
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    FAILS += not ok


calls = collections.defaultdict(list)
riprefs = collections.defaultdict(list)
for f in sorted(K.ext):
    for i in R.md.disasm(R.at(f, K.ext[f]), f):
        if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x"):
            calls[int(i.op_str, 16)].append((f, i.address))
        for op in i.operands:
            if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
                riprefs[i.address + i.size + op.mem.disp].append((f, i.address))
check(calls[0x00266530] == [(0x002679F0, 0x00267B79)] and not riprefs[0x00266530],
      "S1 00266530: one caller 00267B79 in 002679F0, no rip reference")
check(calls[0x002679F0] == [(0x0026CE60, 0x0026CEB0)] and not riprefs[0x002679F0],
      "S2a 002679F0: one caller 0026CEB0 in 0026CE60, no rip reference")
a = {i.address: i for i in R.md.disasm(R.at(0x002679F0, K.ext[0x002679F0]), 0x002679F0)}
check(a[0x00267A79].op_str == "qword ptr [r15 + 0x88]" and a[0x00267A8B].op_str == "0x861ec0" and
      a[0x00267A83].op_str == "edx, edx" and a[0x00267A80].op_str == "r8, ebx" and a[0x00267A77].op_str == "ecx, ebx",
      "S2b 00267A79 allocates ebx bytes; 00267A8B memset(pool, 0, the same ebx)")
print("  0026CE60 callers: %s" % ", ".join("%08X in %08X" % (s, f) for f, s in calls[0x0026CE60]))

CORPUS = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "FABLE", "pub140-scratch", "corpus", "us")
files = sorted(glob.glob(os.path.join(CORPUS, "*.txt")))
print("corpus scripts: %d" % len(files))
fnre = re.compile(r"^\s*(?:fn_\w+|function)\s+(\S+)\(")
actre = re.compile(r"^actor\s+(\S+)")
loops = collections.Counter()
ctrl = False
reqname = collections.Counter()
for p in files:
    act, fn = None, None
    for line in open(p, encoding="utf-8", errors="replace"):
        m = actre.match(line)
        if m:
            act = m.group(1)
        m = fnre.match(line)
        if m:
            fn = m.group(1)
        if "while ((regI1 != -1 && regI0 < 64))" in line:
            loops[fn] += 1
            if os.path.basename(p) == "gol_b01.txt" and fn == "spawn00":
                ctrl = True
        for name in ("エントリキャラ乗っ取り解除", "エントリキャラ乗っ取り２"):
            if "::" + name in line:
                reqname[name] += 1
check(ctrl, "D1 control: gol_b01 spawn00 holds the regI1 loop")
print("  regI1 loops by enclosing function: %s (total %d, files %d)" % (
    dict(loops), sum(loops.values()),
    sum(1 for p in files if "while ((regI1 != -1 && regI0 < 64))" in open(p, encoding="utf-8", errors="replace").read())))
print("D2 by-name requests of the takeover release / save functions, all scripts: %s" % (dict(reqname) or "none"))
src = open(os.path.join(CORPUS, "rbn_a03.txt"), encoding="utf-8", errors="replace").read().splitlines()
for k, l in enumerate(src):
    if re.search(r"sysReq\w*\(", l) and "::" not in l and "reqArr" not in l:
        print("   rbn_a03:%d computed-target request: %s" % (k + 1, l.strip()))
print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
