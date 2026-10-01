"""CPostEffect +0xC70 glareRemapFactor: what the engine gives the library (OPUS, 2026-09-27). Clears the store's last
meaning-rung review ('SEMANTICALLY IDENTIFIED with no (or a partly declined) stated meaning').

  G1 SetGlareParameters 00707560 reads its fifth argument ([rsp + 0x60]); a value <= 0 returns E_FAIL (0x80004005) and
     stores nothing; otherwise it stores max(arg, 0.001f) (0x3A83126F at 007075B7, cmovbe) at +0xC70 (007075E1)
  G2 its three callers all pass 1.0 as that argument:
       the frame path 0065E670 (-> 006CC1E0 -> 006DB9A0 -> jmp 00707560) stores [01CEBBA8] = 1.0 at [rsp + 0x20];
       006DEEE0 stores [01CEBBA8] = 1.0 at [rsp + 0x20];
       the initialiser 006FF900 stores xmm9 at 00704EF2, where xmm9 = [01CEBBA8] = 1.0 (007047E7). It is callee-saved,
       and nothing in 006FF900 between 007047E7 and 00704EF2 writes it; no direct jump enters that range from outside.
  S  the store row states that provenance and no longer declines a meaning
Not claimed: what the library does with the factor.
"""
import struct, sys, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
def rip(x):
    m = re.search(r"rip \+ (0x[0-9a-f]+)\]", x.op_str); return x.address + x.size + int(m.group(1), 16) if m else None
f32 = lambda v: struct.unpack_from("<f", d, off(v))[0]
args = sys.argv[1:]
FIELDS = Path(args[args.index("--fields") + 1]) if "--fields" in args else ROOT / "Database/FFXII TZA/_types/fields.tsv"
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
s = {x.address: x.op_str for x in dis(0x707560, 142)}
check("G1 00707560: arg5 <= 0 -> E_FAIL, else max(arg5, 0.001f) stored at +0xC70",
      s.get(0x707564) == "xmm3, dword ptr [rsp + 0x60]" and s.get(0x7075A1) == "eax, 0x80004005"
      and s.get(0x7075B7) == "dword ptr [rsp + 0x20], 0x3a83126f" and s.get(0x7075E1) == "dword ptr [rcx + 0xc70], eax")
a = dis(0x65E670, 0x20); b = dis(0x6DEEE0, 0x24); c = dis(0x7047E7, 9)
init = dis(0x7047E7, 0x704F07 - 0x7047E7 + 5)
xmm9_writes = [x for x in init[1:] if x.op_str.startswith("xmm9,") and x.mnemonic not in ("comiss", "ucomiss")]
whole = dis(0x6FF900, 0x707560 - 0x6FF900)
into = [x for x in whole if x.mnemonic.startswith("j") and x.op_str.startswith("0x") and 0x7047E7 < int(x.op_str, 16) <= 0x704F07
        and not 0x7047E7 <= x.address <= 0x704F07]
check("G2 all three callers pass 1.0 as the fifth argument",
      rip(a[1]) == 0x1CEBBA8 and a[4].op_str == "dword ptr [rsp + 0x20], xmm0"
      and rip(b[1]) == 0x1CEBBA8 and b[4].op_str == "dword ptr [rsp + 0x20], xmm2"
      and rip(c[0]) == 0x1CEBBA8 and c[0].op_str.startswith("xmm9,") and not xmm9_writes
      and any(x.address == 0x704EF2 and x.op_str == "dword ptr [rsp + 0x20], xmm9" for x in init)
      and f32(0x1CEBBA8) == 1.0 and not into, "(xmm9 writes between: %d; jumps in from outside: %d)" % (len(xmm9_writes), len(into)))
row = [l.split("\t") for l in FIELDS.read_bytes().decode("utf-8").splitlines() if l.startswith("CPostEffect\t0xC70\t")]
check("S the store states the provenance and declines no meaning",
      len(row) == 1 and "MEANING NOT CLAIMED" not in row[0][5] and "1.0" in row[0][5] and "00707560" in row[0][5])
print("FAILS", fails)
sys.exit(1 if fails else 0)
