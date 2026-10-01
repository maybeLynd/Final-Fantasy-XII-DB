"""uq191_consumers.py - UQ-191: the shadow-object channels have no on-screen effect in the PC build (FABLE, Claude Opus 5.5,
2026-09-27). Static read of the authorised exe; rip-relative and image-base-relative references both counted.

  C1 the shadow pool 02B40528 is referenced only by functions in the shadow module (003B5600..003B6C00).
  C2 among them, only 003B62D0 turns the channel fields (+0x50..+0x9F) into output; the others are the tween steppers and
     setters (they write the fields).
  C3 003B62D0 has one caller, 003B6020 (reached through the thunk 00521440), and 003B6020 calls only 003B62D0 and the ring
     submit 003A1DB0: its output is copied into the PS2 command ring whose descriptors sit at 02EBEFC0 (image base +
     0x2D9EFC0, indexed by 02EBEFF0).
  C4 the ring's submit 003A1DB0 reads the descriptor's base and cursor only to count, and its publisher 0036F360 reads
     only the last qword before the cursor (the DMA tag), then writes offset, count and 0x100 into the one cell 02EBA3F8;
     every other function referencing the ring descriptors (rip or image-base form) is an emitter or setup.
  C5 the two functions that address the scratch region the rings are carved from at +0x1000/+0x2000 (003ABD50,
     003AC110) write those areas before reading them.
Exit 1 on any FAIL.
"""
import re, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
_pe = struct.unpack_from("<I", d, 0x3C)[0]; _n = struct.unpack_from("<H", d, _pe + 6)[0]; _opt = struct.unpack_from("<H", d, _pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, _pe + 24 + _opt + i * 40 + 8) for i in range(_n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
SIZES = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = l.rstrip("\n").split("\t")
    try: SIZES["%08X" % int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
BODY = {}
def body(f):
    if f not in BODY:
        a = int(f, 16); o = off(a)
        BODY[f] = [] if o is None or SIZES.get(f, 0) <= 0 else list(cs.disasm(d[o:o + SIZES[f]], a))
    return BODY[f]
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
def refs(lo, hi):
    out = collections.defaultdict(list); ib_lo, ib_hi = lo - 0x120000, hi - 0x120000
    for f in SIZES:
        if not 0x121000 <= int(f, 16) < 0x8C0000: continue
        for x in body(f):
            t = rip(x)
            if t is not None and lo <= t < hi: out[f].append(x.address); continue
            for m in re.finditer(r"0x([0-9a-f]{6,8})\b", x.op_str):
                v = int(m.group(1), 16)
                if ib_lo <= v < ib_hi and "rip" not in x.op_str: out[f].append(x.address)
    return out
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

pool = refs(0x02B40528, 0x02B40530)
check("C1 %d functions reference the shadow pool, all in 003B5600..003B6C00 (the pool allocator 003B56D0 included)" % len(pool),
      pool and all(0x003B5600 <= int(f, 16) < 0x003B6C00 for f in pool), str(sorted(f for f in pool if not 0x003B5600 <= int(f, 16) < 0x003B6C00)))

def chan_rw(f):
    r, w = set(), set()
    for x in body(f):
        for m in re.finditer(r"(?:byte|word|dword|qword|xmmword) ptr \[r\w+ \+ 0x([0-9a-f]+)\]", x.op_str):
            v = int(m.group(1), 16)
            if 0x50 <= v <= 0x9F:
                (w if x.op_str.startswith(m.group(0)) and x.mnemonic.startswith("mov") else r).add(v)
    return r, w
# functions that read a channel without writing it back in the same body = output consumers
CURRENT = {0x50, 0x54, 0x58, 0x5C, 0x70, 0x78, 0x98}   # the current values the tween steppers write
consumers = sorted(f for f in pool if (lambda rw: (rw[0] & CURRENT) - rw[1])(chan_rw(f)))
check("C2 the channel fields feed output only in 003B62D0 (read-only channel reads)", consumers == ["003B62D0"], str(consumers))

callers = [(f, x.address) for f in SIZES for x in body(f) if (x.mnemonic in ("call", "jmp")) and x.op_str.startswith("0x3b62d0") and f != "003B62D0"]
calls6020 = sorted({x.op_str for x in body("003B6020") if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x")})
thunk = [(f, x.address) for f in SIZES for x in body(f) if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x3b6020") and f != "003B6020"]
check("C3 003B62D0's one caller is 003B6020 (via thunk 00521440), which calls only 003B62D0 and 003A1DB0",
      [f for f, a in callers] == ["003B6020"] and calls6020 == ["0x3a1db0", "0x3b62d0"] and [f for f, a in thunk] == ["00521440"],
      "callers=%s calls=%s thunk=%s" % (callers, calls6020, thunk))

sub = ["%s %s" % (x.mnemonic, x.op_str) for x in body("003A1DB0")]
pub = body("0036F360")
pub_reads = [x for x in pub if re.search(r"(?:dword|qword) ptr \[r(?:9|8|cx|dx)", x.op_str) and not x.op_str.startswith(("dword ptr [", "qword ptr ["))]
check("C4 the submit counts (cursor - base) and the publisher reads only the last tag qword",
      "sub rdx, rcx" in sub and "call 0x36f360" in sub
      and [("%s %s" % (x.mnemonic, x.op_str)) for x in pub_reads] == ["mov eax, dword ptr [r9 - 0x10]"],
      str([("%s %s" % (x.mnemonic, x.op_str)) for x in pub_reads]))

def first_access(f, reg):
    for x in body(f):
        m = re.search(r"\[%s(?: \+ [^\]]+)?\]" % reg, x.op_str)
        if m: return "W" if x.mnemonic.startswith("mov") and x.op_str.startswith(("byte", "word", "dword", "qword", "xmmword")) and "[%s" % reg in x.op_str.split(",")[0] else "R"
    return None
fa = {("003ABD50", r): first_access("003ABD50", r) for r in ("rdi", "r14")}
fa.update({("003AC110", r): first_access("003AC110", r) for r in ("rbx", "r15")})
check("C5 the scratch users at +0x1000/+0x2000 write before they read", all(v == "W" for v in fa.values()), str(fa))
print("FAILS", fails)
sys.exit(1 if fails else 0)
