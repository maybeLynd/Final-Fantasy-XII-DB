"""party_read_states.py - the per-actor read-in state machine 0037B4D0: its 24-arm jump table, the calls in each arm's
address range, and every write of a state number to the record's byte +8 (`or byte [rsi+8], N`, or `or dl/cl, N` then
`mov byte [rsi+8], dl/cl`).

Arm ranges are layout order (arm target to next arm target). A write inside an arm's range is not necessarily made by that
arm: the fall-back writes at 0037BC72 / 0037BC7F / 0037BC8C / 0037BC99 sit in state 16's range but are jump targets of
states 7, 10, 13 and 15 (0037B940, 0037BA3B, 0037BB43, 0037BBF1), and 0037BDD3 (->18) in state 19's range is state 16's
failure exit (0037BC30 / 0037BC3B). The page's transition table places them by those jumps; nothing else is inferred. Output: party-read-states.tsv beside this script."""
import os, re, struct, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 5))
EXE = os.path.join(REPO, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(REPO, "Database", "Tools", "work", "graph", "functions.tsv")
BASE, F = 0x120000, 0x0037B4D0
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 12)[0], struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 8)[0],
         struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 20)[0]) for i in range(ns)]
def off(va):
    r = va - BASE
    for a, vs, ro in secs:
        if a <= r < a + vs: return ro + r - a
sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64)
ins = list(md.disasm(d[off(F):off(F) + sizes[F]], F))
# the jump table: `cmp eax, 0x17` bound and `mov ecx, [r8 + rax*4 + RVA]`
tab = n = None
for k, x in enumerate(ins):
    m = re.match(r"ecx, dword ptr \[r8 \+ rax\*4 \+ (0x[0-9a-f]+)\]$", x.op_str)
    if x.mnemonic == "mov" and m: tab = BASE + int(m.group(1), 16); break
for x in ins:
    if x.mnemonic == "cmp" and x.op_str == "eax, 0x17": n = 0x18; break
assert tab and n == 24, (tab, n)
targets = [struct.unpack_from("<I", d, off(tab) + 4 * c)[0] + BASE for c in range(n)]
order = sorted(range(n), key=lambda c: targets[c])
writes = []
for k, x in enumerate(ins):
    m = re.match(r"byte ptr \[rsi \+ 8\], (0x[0-9a-f]+|\d+)$", x.op_str)
    if x.mnemonic == "or" and m: writes.append((x.address, int(m.group(1), 0) & 0x7F))
    elif x.mnemonic == "mov" and x.op_str.startswith("byte ptr [rsi + 8], "):
        reg = x.op_str.split(", ")[1]
        for y in reversed(ins[max(0, k - 6):k]):
            mm = re.match(r"%s, (0x[0-9a-f]+|\d+)$" % reg, y.op_str)
            if y.mnemonic == "or" and mm: writes.append((x.address, int(mm.group(1), 0) & 0x7F)); break
rows = []
for i, c in enumerate(order):
    lo = targets[c]; hi = targets[order[i + 1]] if i + 1 < n else F + sizes[F]
    calls = [names.get(int(x.op_str, 16), x.op_str)[:40] for x in ins if lo <= x.address < hi and x.mnemonic == "call" and x.op_str.startswith("0x")]
    ws = ["%08X->%d" % (a, v) for a, v in writes if lo <= a < hi]
    rows.append((c, lo, hi, ws, calls))
with open(os.path.join(HERE, "party-read-states.tsv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("state\tarm\tarm_range_end\tstate_writes_in_range\tcalls_in_range\n")
    for c, lo, hi, ws, calls in sorted(rows):
        f.write("%d\t%08X\t%08X\t%s\t%s\n" % (c, lo, hi, " ".join(ws) or "-", " ".join(calls) or "-"))
print("table %08X, %d arms, %d state writes" % (tab, n, len(writes)))
