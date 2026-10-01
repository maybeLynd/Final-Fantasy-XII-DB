"""uq193_container.py - UQ-193's remaining clauses: resource admission, source ownership and other construction paths of the
render root's generic reference container (FABLE, Claude Opus 5.5, 2026-09-27). Static; the stale-id clause is
uq193-release-sites/ (2026-09-27).

  K1 one construction path: the container init 0051F170 is reached only through 0051B9D0 (64 slots at root+0x30), and
     0051B9D0 only from RenderResourceRoot_InitializeSubcontainers 0041E3A0 (0041E470); no data pointer holds either.
  K2 one admission function with two callers: 0051BA80 is called only at 004247AD (in 00424550) and 00425244 (in 00424D80);
     each passes the render record's own stored id (edx = [record+0xC8] / [record+0xC4]) and, as the source, the record's
     own resource entry resolved from [record+0x10] through 0020E600 (r8).
  K3 the admission contract: id -1 -> capacity check 0051F150, then a new slot from 0051F080; any other id -> the slot is
     looked up (0051F240) and its entry rebuilt in place (0041CA70); a failed initialisation with a live id releases the
     slot (0051F190).
Exit 1 on any FAIL.
"""
import re, struct, sys, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
_pe = struct.unpack_from("<I", d, 0x3C)[0]; _n = struct.unpack_from("<H", d, _pe + 6)[0]; _opt = struct.unpack_from("<H", d, _pe + 20)[0]
SECS = []
for i in range(_n):
    b = _pe + 24 + _opt + i * 40
    SECS.append((d[b:b + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, b + 8))
def off(v):
    for _, vs, va, rs, ro in SECS:
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
def txt(x): return "%s %s" % (x.mnemonic, x.op_str)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
def callers(t):
    out = []
    for f in SIZES:
        if not 0x121000 <= int(f, 16) < 0x8C0000: continue
        for x in body(f):
            if (x.mnemonic == "call" or x.mnemonic.startswith("j")) and x.op_str == hex(t) and int(f, 16) != t:
                out.append((f, "%08X" % x.address))
    return sorted(out)
def data_ptrs(t):
    n = 0
    for nm, vs, va, rs, ro in SECS:
        if nm in (".rdata", ".data"): n += d[ro:ro + rs].count(struct.pack("<Q", t))
    return n
c170, c9d0 = callers(0x0051F170), callers(0x0051B9D0)
check("K1 one construction path: 0051F170 <- 0051B9D0 <- 0041E3A0 (0041E470); no data pointers",
      c170 == [("0051B9D0", "0051B9D9")] and c9d0 == [("0041E3A0", "0041E470")] and data_ptrs(0x0051F170) == 0 and data_ptrs(0x0051B9D0) == 0,
      "%s %s" % (c170, c9d0))
cba80 = callers(0x0051BA80)
def args_before(f, a, n=12):
    b = body(f); k = next(i for i, x in enumerate(b) if x.address == int(a, 16))
    return [txt(x) for x in b[max(0, k - n):k]]
a1, a2 = args_before("00424550", "004247AD"), args_before("00424D80", "00425244")
check("K2 0051BA80's two callers pass the record's stored id and its [record+0x10] resource",
      cba80 == [("00424550", "004247AD"), ("00424D80", "00425244")]
      and "mov edx, dword ptr [rdi + 0xc8]" in a1 and "mov ecx, dword ptr [rdi + 0x10]" in a1 and "mov r8, rbx" in a1
      and "mov edx, dword ptr [rbx + 0xc4]" in a2 and "mov ecx, dword ptr [rbx + 0x10]" in a2 and "mov r8, rdi" in a2,
      str(cba80))
k3 = [txt(x) for x in body("0051BA80")]
check("K3 id -1 -> 0051F150 + 0051F080; else lookup 0051F240 and rebuild 0041CA70; failure releases via 0051F190",
      "cmp edx, -1" in k3 and "call 0x51f150" in k3 and "call 0x51f080" in k3 and "call 0x51f240" in k3
      and "call 0x41ca70" in k3 and "call 0x51f190" in k3)
print("FAILS", fails)
sys.exit(1 if fails else 0)
