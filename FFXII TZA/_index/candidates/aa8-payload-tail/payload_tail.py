"""payload_tail.py - AA-8: the last four bytes of the 0x1538-byte persistent payload (FABLE, Claude Opus 5.5, 2026-09-26).

The payload base is SaveImage_GetActiveRuntimeBuffer() + 0x200 (002EF2B0), so payload +0x1535 is raw buffer +0x1735.
  P1 002EF370 is the one store: `mov byte [buffer + 0x1735], bl` with bl = its first argument.
  P2 its callers: the options apply 002DDA30 at 002DDB4A passes ebx, and ebx is the constant 1. It is set by
     `mov ebx, 1` at 002DDAC4; no branch from outside enters 002DDAC4..002DDB4A; nothing in between writes
     ebx/bx/bl; the calls in between are callee-saved for rbx. The script verb 0x20D1 handler 0050D180 pops an
     int and tail-jumps with it.
  P3 image-wide census over every functions.tsv body, decoded from its own entry: every memory operand with
     displacement 0x1530..0x1537 or 0x1735, with its access width.
       - disp 0x1735: exactly one access, P1's store.
       - disp 0x1535..0x1537: none.
       - disp 0x1534: byte-wide only (no word/dword/qword at +0x1534 that would cover +0x1535..+0x1537).
     Planted positive: the census must find the three +0x1534 readers the page names (0025DBB6, 00262029,
     0026DE41) and the area-unload clear 00262A76.
  Wider accesses at 0x1530 / 0x1538 are printed for the record. The page shows they sit on another object.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
def S(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + size], a)}

A = S(0x2EF370, 0x19); B = S(0x2EF2B0, 0x14)
check("P1 the store and the payload base",
      A[0x2EF378] == "call 0x2ef640" and A[0x2EF37D] == "mov byte ptr [rax + 0x1735], bl" and A[0x2EF376] == "mov ebx, ecx"
      and B[0x2EF2B4] == "call 0x2ef640" and B[0x2EF2B9] == "add rax, 0x200")
F = list(cs.disasm(d[off(0x2DDA30):off(0x2DDA30) + 0x1FA], 0x2DDA30))
lo, hi = 0x2DDAC4, 0x2DDB4A
inside_writes = [x for x in F if lo < x.address < hi and x.operands and x.operands[0].type != X86_OP_MEM
                 and cs.reg_name(x.operands[0].reg) in ("ebx", "rbx", "bx", "bl") and x.mnemonic not in ("test", "cmp")]
entries = []
for x in F:
    if x.mnemonic.startswith("j") and x.op_str.startswith("0x"):
        t = int(x.op_str, 16)
        if lo < t <= hi and not (lo <= x.address < hi): entries.append((x.address, t))
V = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in F}
check("P2 options apply stores the constant 1", V[lo] == "mov ebx, 1" and V[0x2DDB42] == "mov ecx, ebx"
      and V[hi] == "call 0x2ef370" and inside_writes == [] and entries == [],
      "writes %s entries %s" % (inside_writes, entries))
H = S(0x50D180, 0x17)
check("P2 verb 0x20D1 handler pops an int and tail-jumps", H[0x50D187] == "call 0x267e10" and H[0x50D18C] == "mov ecx, eax"
      and H[0x50D192] == "jmp 0x2ef370")
rows = list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]
hits = []
for r in rows:
    try: a, size = int(r[0], 16), int(r[2])
    except (ValueError, IndexError): continue
    o = off(a)
    if o is None or size <= 0: continue
    for x in cs.disasm(d[o:o + size], a):
        for op in x.operands:
            if op.type == X86_OP_MEM and (0x1530 <= op.mem.disp <= 0x1537 or op.mem.disp == 0x1735) and cs.reg_name(op.mem.base) != "rip":
                hits.append((x.address, op.mem.disp, op.size, "%s %s" % (x.mnemonic, x.op_str)))
by = lambda disp: [h for h in hits if h[1] == disp]
check("P3 disp 0x1735: one access, the store", [h[0] for h in by(0x1735)] == [0x2EF37D], str(by(0x1735)))
check("P3 disp 0x1535..0x1537: none", by(0x1535) + by(0x1536) + by(0x1537) == [])
check("P3 disp 0x1534: byte-wide only", by(0x1534) != [] and all(h[2] == 1 for h in by(0x1534)),
      " ".join("%08X/%d" % (h[0], h[2]) for h in by(0x1534)))
got = {h[0] for h in by(0x1534)}
check("P3 planted positive: the named +0x1534 sites are found", {0x25DBB6, 0x262029, 0x26DE41, 0x262A76} <= got)
print("info  disp 0x1530..0x1533 accesses:", " ".join("%08X:+%X/%d" % (h[0], h[1], h[2]) for h in hits if 0x1530 <= h[1] <= 0x1533))
# P4: the three +0x1530 qword operands are not on the payload. The payload ends at +0x1538, and each base object
# carries fields past that end in the same function.
def past_end(fa, size, reg, lo_addr=None):
    L = list(cs.disasm(d[off(fa):off(fa) + size], fa))
    return sorted({op.mem.disp for x in L for op in x.operands
                   if op.type == X86_OP_MEM and cs.reg_name(op.mem.base) == reg and op.mem.disp >= 0x1538})
sz = {r[0]: int(r[2]) for r in rows if len(r) > 2 and r[2].isdigit()}
M = S(0x2778C0, sz["002778C0"])
P = past_end(0x27CE70, sz["0027CE70"], "rbx")
check("P4 the +0x1530 qwords are on objects larger than the payload",
      M.get(0x2792A5) == "lea rax, [rbx + 0x1530]" and M.get(0x27928F) == "mov word ptr [rbx + 0x153e], ax"
      and M.get(0x27929E) == "mov word ptr [rbx + 0x153a], ax"
      and S(0x27CE93, 3)[0x27CE93] == "mov rbx, rcx" and {0x1550, 0x1578, 0x15EF} <= set(P),
      "0027CE70 rbx fields past 0x1538: %s" % [hex(v) for v in P])
print("FAILS", fails)
sys.exit(1 if fails else 0)
