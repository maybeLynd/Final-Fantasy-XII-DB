# rc12_special_slots.py - RC-12: which special-function slot each reader of an actor entry's +0x18 footer asks for.
# The footer is {u16 count = 0x12; u16 special[18]} (scheduling page section 2.6): special[t] = the index of the actor's
# function declared with special type t, 0xFFFF none. A reader resolves [X+0x18] with ImageAddress_ResolveRuntimePointer
# (0x20e600), bounds the slot against the count (cmp c, word [base]; jge) and reads word [base + 2*t] with t = c + 1
# (special[] is 1-based: mapjump(12) is at +0x18, the wait resolver's site).
# Part 1 (image): for every call to 0x20e600 in the named functions that follows a load of [.. + 0x18], list the word
# reads [reg + reg + DISP] / [reg + DISP] within the next 14 instructions and derive t = (DISP - 2) / 2; also the compare
# constant against the count word. Control: the wait resolver 0025DF00's site must give t = 12 (mapjump).
# Part 2 (authored data): the special-type names, from the shipped scripts' declarations `function NAME(t)`.
import os, re, subprocess, sys, collections
SCR = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch"
FUNCS = ["0025DF00", "0025AE00", "0025B820", "0025BAD0", "0025C230", "0025C830", "00263050", "00263D40"]
rows = []
for f in FUNCS:
    lines = subprocess.run([sys.executable, "disr.py", f], capture_output=True, text=True, cwd=SCR).stdout.splitlines()[1:]
    for k, l in enumerate(lines):
        if "call 0x20e600" not in l:
            continue
        prev = " ".join(lines[max(0, k - 4):k])
        if "+ 0x18]" not in prev:
            continue
        slots, cmps = [], []
        for m in lines[k + 1:k + 7]:
            mm = re.search(r"word ptr \[r\w+ \+ r\w+ \+ (0x[0-9a-f]+|\d+)\]|word ptr \[r\w+ \+ (0x[0-9a-f]+|\d+)\]", m)
            if mm:
                d = int(mm.group(1) or mm.group(2), 0)  # capstone prints small displacements in decimal
                if d >= 2 and d % 2 == 0 and d <= 0x24:
                    slots.append((d // 2, m.split()[0]))
            mc = re.search(r"mov e[a-z]x, (0x[0-9a-f]+|\d+)$", m.strip())
            if mc:
                cmps.append(int(mc.group(1), 0))
            if "call " in m and "0x20e600" not in m:
                break
        rows.append((f, l.split()[0], slots, cmps))
for f, site, slots, cmps in rows:
    print("%s  call@%s  slot reads %s  compare constants %s" % (f, site, [("t=%d" % t, a) for t, a in slots], cmps))
ctl = [r for r in rows if r[0] == "0025DF00" and any(t == 12 for t, _ in r[2])]
print("CONTROL wait resolver 0025DF00 reads special[12] (mapjump):", "PASS" if ctl else "FAIL")
CORPUS = os.path.join(SCR, "corpus", "us")
decl = re.compile(r"\bfunction\s+([^\s(]+)\((\d+)\)")
names = collections.defaultdict(collections.Counter)
for fn in os.listdir(CORPUS):
    if fn.endswith(".txt"):
        for m in decl.finditer(open(os.path.join(CORPUS, fn), encoding="utf-8", errors="replace").read()):
            names[int(m.group(2))][m.group(1)] += 1
print("special types declared in the shipped scripts (type: name x count):")
for t in sorted(names):
    print("  %2d: %s" % (t, ", ".join("%s x%d" % kv for kv in names[t].most_common(4))))
