"""musicctrl_quals.py - the owner's static re-read behind the two music-control qualifications on FABLE's audio pages
(FABLE, Claude Opus 5.5, 2026-09-27; on ASTRA-RETURN-FABLE-MUSICCTRL-BINDING-PROVENANCE and -PAGE-BOUNDARY).

  M1 the binder 003EAB60 is straight-line: loader call, unconditional store to 02B5E0D0 (003EAB78), ret - no compare,
     no branch, so nothing in it refuses a second binding.
  M2 the rebase 003EAB90 visits (max + 127) / 128 page words (signed biased divide, 003EAB9A-003EABA7).
  M3 the reader 003EAA70 accepts fieldId <= max (003EAA88 cmp [r8+4], ebx / jl) and selects fieldId / 128 (sar 7).
  M4 arithmetic from M2/M3: the reader's highest page equals the last rebased page for every max in 0..4096 except the
     multiples of 128, 0 included (0 rebases no page, yet field 0 reads page 0), where it is one past it; the shipped max 1311 gives 11 pages, highest index 10.
     Planted negative: a rebase counting max / 128 + 1 pages would leave no mismatch - the check must see the difference.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, b): return [(x.address, ("%s %s" % (x.mnemonic, x.op_str)).strip()) for x in cs.disasm(d[off(a):off(b)], a)]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

b = ins(0x3EAB60, 0x3EAB84); bm = dict(b)
check("M1 the binder stores unconditionally",
      bm.get(0x3EAB73) == "call 0x51ed10" and bm.get(0x3EAB78) == "mov qword ptr [rip + 0x2773551], rax"
      and 0x3EAB7F + 0x2773551 == 0x02B5E0D0 and bm.get(0x3EAB83) == "ret"
      and not any(t.split()[0] in ("cmp", "test") or t.startswith("j") for _, t in b))
r = dict(ins(0x3EAB90, 0x3EABD7))
check("M2 the rebase counts (max + 127) / 128 pages",
      r.get(0x3EAB9A) == "mov eax, dword ptr [r8 + 4]" and r.get(0x3EAB9E) == "add eax, 0x7f"
      and r.get(0x3EABA7) == "sar eax, 7" and r.get(0x3EABBE) == "add ecx, r9d")
q = dict(ins(0x3EAA88, 0x3EAAA1))
check("M3 the reader accepts fieldId <= max and pages by fieldId / 128",
      q.get(0x3EAA88) == "cmp dword ptr [r8 + 4], ebx" and q.get(0x3EAA8C) == "jl 0x3eaaf6"
      and q.get(0x3EAA96) == "sar eax, 7" and q.get(0x3EAA9C) == "movsxd rax, dword ptr [r8 + rcx*4 + 8]")
def rebased(mx): return (mx + 127) // 128
mism = [mx for mx in range(0, 4097) if mx // 128 > rebased(mx) - 1]
planted = [mx for mx in range(0, 4097) if mx // 128 > (mx // 128 + 1) - 1]
check("M4 the mismatch is exactly the multiples of 128, 0 included; shipped 1311 unaffected",
      mism == list(range(0, 4097, 128)) and rebased(1311) == 11 and 1311 // 128 == 10 and planted == []
      and 127 not in mism and 129 not in mism,
      "mismatches %d (first %s), planted %d" % (len(mism), mism[:3], len(planted)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
