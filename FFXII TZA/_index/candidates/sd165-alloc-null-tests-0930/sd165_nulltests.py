"""sd165_nulltests.py - SD-165: which callers of the arena allocator test its result for null (OPUS, 2026-09-30).
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.

Entry points: the raw-block wrappers 0036A100 / 0036A190 / 0036A1A0 and the handle path 0036B160 (the retry allocator
0036BFE0 is reached only through them and the allocator's own helpers). For every call site, the returned value is
followed linearly from the instruction after the call (the register it is in, copies made of it, up to 24 instructions
or the first unconditional transfer) and the site is classed by what happens FIRST:
  TESTED     test R,R / cmp R,0 (then a conditional branch) - the caller checks for null
  DEREF      a memory operand based on R - used without a check
  PASSED     R becomes a call argument (rcx/rdx/r8/r9) before a check - the callee decides
  STORED     R is written to memory before a check - kept for later
  RETURNED   ret / tail jump with R in rax - the wrapper hands the check to its caller
  UNCLEAR    none of these within the window
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
ENTRIES = {0x0036A100: "0036A100", 0x0036A190: "0036A190", 0x0036A1A0: "0036A1A0", 0x0036B160: "0036B160 (handle)"}
REG64 = {"rax": ("rax", "eax"), "rbx": ("rbx", "ebx"), "rcx": ("rcx", "ecx"), "rdx": ("rdx", "edx"), "rsi": ("rsi", "esi"),
         "rdi": ("rdi", "edi"), "rbp": ("rbp", "ebp"), "r8": ("r8", "r8d"), "r9": ("r9", "r9d"), "r10": ("r10", "r10d"),
         "r11": ("r11", "r11d"), "r12": ("r12", "r12d"), "r13": ("r13", "r13d"), "r14": ("r14", "r14d"), "r15": ("r15", "r15d")}


def classify(site):
    """TESTED if a null test of the value comes before any dereference within the window; DEREF if a dereference comes
    first; otherwise what the value did first (PASSED / STORED / RETURNED) with no test or dereference seen; UNCLEAR if
    the value was lost without any of these."""
    live, first = {"rax"}, None
    full = {REG64[r][1]: r for r in REG64}
    for n, i in enumerate(R.md.disasm(R.at(site, 0x100), site)):
        if n == 0:
            continue
        if n > 24:
            break
        op, mn = i.op_str, i.mnemonic
        regs = list(live)
        alias = regs + [REG64[r][1] for r in regs if r in REG64]
        if any(re.search(r"\[%s(\]| )" % r, op) for r in regs):
            return "DEREF"
        if mn in ("test", "cmp", "or") and any(re.match(r"%s, (%s|0)$" % (r, r), op) for r in alias):
            return "TESTED"
        m = re.match(r"(\w+), (\w+)$", op)
        if mn == "mov" and m and m.group(2) in full and full[m.group(2)] in live and m.group(1) in full:
            live.add(full[m.group(1)])
            continue
        if mn == "mov" and m and m.group(2) in live:
            live.add(m.group(1))
            continue
        if mn == "mov" and re.match(r"\w+ ptr \[", op) and op.split(", ")[-1] in alias:
            first = first or "STORED"
            continue
        if mn == "call":
            if live & {"rcx", "rdx", "r8", "r9"}:
                first = first or "PASSED"
            live -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
            if not live:
                break
            continue
        if mn == "ret" or (mn == "jmp" and op.startswith("0x")):
            if "rax" in live:
                first = first or "RETURNED"
            break
        if mn == "jmp":
            break
        if m and m.group(1) in live and mn not in ("test", "cmp"):
            live.discard(m.group(1))
            if not live:
                break
    return first or "UNCLEAR"


tally = collections.defaultdict(collections.Counter)
rows = []
for e, name in ENTRIES.items():
    for f, s in sorted(c["calls"].get(e, ())):
        k = classify(s)
        tally[name][k] += 1
        rows.append((name, f, s, k))
with open(os.path.join(HERE, "sd165-sites.tsv"), "w", encoding="utf-8", newline="\n") as fo:
    fo.write("entry\tcaller\tsite\tfirst_use\n")
    for r in rows:
        fo.write("%s\t%08X\t%08X\t%s\n" % r)
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


for name in ENTRIES.values():
    print("      %-18s %s" % (name, dict(sorted(tally[name].items()))))
total = collections.Counter()
for t in tally.values():
    total.update(t)
print("      all sites %d: %s" % (sum(total.values()), dict(sorted(total.items()))))
# controls: the three cases the page reads - the nav grid helper and two effect constructors test the result; the nav grid
# rebuild and the actor-pool build 002679F0 do not (DATA's section 1/2 reading)
by = {s: k for _, f, s, k in rows}
check("C1", by.get(0x002E678F) == "TESTED" and by.get(0x0024A2B9) == "DEREF",
      "controls: 002E678F stores then tests the handle (TESTED); 0024A2B9 keeps the pointer in rbp across a call and uses it (DEREF)")
check("C2", total["TESTED"] > 0 and sum(total.values()) == len(rows) == sum(len(c["calls"].get(e, ())) for e in ENTRIES),
      "every site of the four entries classified (%d)" % len(rows))
print("FAILS %d" % fails)
