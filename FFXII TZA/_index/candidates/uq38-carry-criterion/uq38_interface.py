"""uq38_interface.py - two more structural criteria for UQ-38, measured and retired (FABLE, Claude Opus 5.5, 2026-09-27).

A whole translation of a PS2 routine could show itself at its interface: taking arguments from the bank's a0-a3
images instead of x64 registers, or keeping the PS2 frame ($sp / $fp / $ra) in the bank. Sets as uq38_carry.py.
  I1  entry block (to the first call / jmp / jcc / ret): reads an x64 integer argument register before writing it
  I2  entry block: any access to the bank's a0-a3 images (022D8F50 + 16k, k = 0..3)
  I3  whole body: any access to the bank's $sp / $fp / $ra images (022D90E0 / 022D90F0 / 022D9100)
  C1  control for I2/I3's detector: over the same member bodies it finds bank a0 and v0 accesses (the census lists them)
  C2  control for I1's detector: it reports no argument read for a body whose entry defines rcx/rdx/r8/r9 before use
Reads the capstone listing (Y1P_CACHE).
"""
import csv, os, re, sys, collections
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
HERE = os.path.dirname(os.path.abspath(__file__))
FRONT = os.path.join(HERE, "../../../00-Engine-Core-Runtime/Shared-Transform-Workbench/members/ee-register-members.tsv")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
fr = {r["address"]: r["split"] for r in csv.DictReader(open(FRONT, encoding="utf-8"), delimiter="\t")}
sets = {}
for r in csv.DictReader(open(os.path.join(HERE, "uq38_carry.tsv"), encoding="utf-8"), delimiter="\t"):
    v, fs = r["verdict"], fr.get(r["function"], "-")
    k = "whole" if v == "whole" else ("C-agreed" if v == "C+fragments" and fs == "C+fragments" else ("undecided" if fs == "translated" and v != "whole" else None))
    if k: sets[r["function"]] = k
body = collections.defaultdict(list)
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) == 3: body[p[1]].append((p[0], p[2]))
ALIAS = {"rcx": r"\b(rcx|ecx|cx|cl|ch)\b", "rdx": r"\b(rdx|edx|dx|dl|dh)\b", "r8": r"\br8[dwb]?\b", "r9": r"\br9[dwb]?\b"}
PUREW = ("mov", "movzx", "movsx", "movsxd", "lea", "pop", "movd", "movq")
GPR = lambda k: (0x022D8F10 + 16 * k, 0x022D8F10 + 16 * k + 16)
A03 = [GPR(k) for k in range(4, 8)]; FRAME = [GPR(29), GPR(30), GPR(31)]; V0 = [GPR(2)]; A0 = [GPR(4)]
def entry(ins):
    out = []
    for a, s in sorted(ins):
        mn = s.split()[0]
        if mn in ("call", "jmp", "ret") or (mn.startswith("j") and mn != "jmp"): break
        out.append(s)
    return out
def xarg(block):
    got, dead = set(), set()
    for s in block:
        mn, ops = (s.split(None, 1) + [""])[:2]; ops = ops.split(";")[0]
        first, rest = (ops.split(",", 1) + [""])[:2]
        for reg, pat in ALIAS.items():
            if reg in got or reg in dead or not re.search(pat, ops): continue
            if mn in ("xor", "sub") and re.fullmatch(r"\s*(\w+)\s*,\s*\1\s*", ops): dead.add(reg); continue
            if mn in PUREW and re.search(pat, first) and "[" not in first and not re.search(pat, rest): dead.add(reg); continue
            got.add(reg)
    return got
def touches(lines, ranges):
    for s in lines:
        m = re.search(r"=>([0-9A-F]{8})", s)
        if m and any(lo <= int(m.group(1), 16) < hi for lo, hi in ranges): return True
    return False
by = collections.defaultdict(collections.Counter)
for f, k in sets.items():
    b = entry(body[f]); allb = [s for a, s in body[f]]
    by[k]["n"] += 1
    by[k]["I1 x64 args at entry"] += bool(xarg(b))
    by[k]["I2 bank a0-a3 at entry"] += touches(b, A03)
    by[k]["I3 bank sp/fp/ra anywhere"] += touches(allb, FRAME)
    by[k]["C1 bank v0 anywhere"] += touches(allb, V0)
    by[k]["C1 bank a0 anywhere"] += touches(allb, A0)
for k in ("whole", "C-agreed", "undecided"): print(k, dict(by[k]))
W, C, U = by["whole"], by["C-agreed"], by["undecided"]
ok("I1", W["I1 x64 args at entry"] >= 0.9 * W["n"] and C["I1 x64 args at entry"] >= 0.9 * C["n"],
   "x64 argument reads at entry in %d/%d whole and %d/%d C-agreed: no separation" % (W["I1 x64 args at entry"], W["n"], C["I1 x64 args at entry"], C["n"]))
ok("I2", not any(by[k]["I2 bank a0-a3 at entry"] for k in by), "no member of any set touches bank a0-a3 in its entry block")
ok("I3", not any(by[k]["I3 bank sp/fp/ra anywhere"] for k in by), "no member of any set touches bank $sp / $fp / $ra anywhere")
ok("C1", sum(by[k]["C1 bank v0 anywhere"] for k in by) > 0 and sum(by[k]["C1 bank a0 anywhere"] for k in by) > 0,
   "the same detector finds bank v0 in %d members and bank a0 in %d" % (sum(by[k]["C1 bank v0 anywhere"] for k in by), sum(by[k]["C1 bank a0 anywhere"] for k in by)))
ctl = [f for f in sorted(body) if (lambda b: b and not xarg(b) and any(re.match(r"(xor|mov) (ecx|rcx), ", s) for s in b[:3]))(entry(body[f]))][:1]
ok("C2", bool(ctl), "a body whose entry defines rcx before any read reports no argument read: %s" % (ctl[0] if ctl else "-"))
print("FAILS", fails); sys.exit(1 if fails else 0)
