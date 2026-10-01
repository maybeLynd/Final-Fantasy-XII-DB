"""gf4_name_refs.py - GF-4: the only code references to the two class names are their class-descriptor registrations
(FABLE, Claude Opus 5.5, 2026-09-27; on ASTRA-RETURN-FABLE-GF4-CALLER-PREFLIGHT). Static.

  N1 "PDeferredLighting\0" and "PLowResParticles\0" each occur once in the image.
  N2 image-wide, the only RIP-relative operands that resolve to either string are 00644280 (lea r8, PDeferredLighting)
     and 00644AA0 (lea r8, PLowResParticles), each the name argument of the registration call that follows; there is no
     absolute qword or image-relative dword naming either string.
  N3 planted positive: the same sweep finds both known leas (a sweep that found nothing would fail N2).
Combined with GF-6 (no shipped .phyre cluster names any of the 36 classes) and GF-2 (no construction in the executable),
no shipped state holds an instance whose slot 6 could be called. Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def va_of(fo):
    for vs, va, rs, ro in secs:
        if ro <= fo < ro + rs: return fo - ro + va + BASE
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
names = {b"PDeferredLighting\0": None, b"PLowResParticles\0": None}
for s in names:
    hits = [m.start() for m in re.finditer(re.escape(s), d)]
    names[s] = [va_of(h) for h in hits]
check("N1 each name occurs once", all(len(v) == 1 for v in names.values()), str({k[:-1].decode(): ["%08X" % x for x in v] for k, v in names.items()}))
targets = {v[0] for v in names.values()}
text = [x for x in secs if x[1] == 0x1000][0]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
refs = []
body = d[text[3]:text[3] + text[2]]
for m in re.finditer(rb"[\x48\x4c][\x8d\x8b][\x05\x0d\x15\x1d\x25\x2d\x35\x3d]", body):
    fo = text[3] + m.start(); va = va_of(fo)
    tgt = va + 7 + struct.unpack_from("<i", d, fo + 3)[0]
    if tgt in targets:
        ins = next(cs.disasm(d[fo:fo + 7], va), None)
        if ins is not None and ins.size == 7: refs.append((va, "%s %s" % (ins.mnemonic, ins.op_str)))
absq = sum(d.count(struct.pack("<Q", t)) for t in targets); rvad = sum(d.count(struct.pack("<I", t - BASE)) for t in targets)
check("N2 the only references are the two registration leas", sorted(a for a, _ in refs) == [0x644280, 0x644AA0] and absq == 0 and rvad == 0,
      str(["%08X %s" % r for r in refs]) + " abs %d rva %d" % (absq, rvad))
check("N3 planted positive: both known leas are found", {a for a, _ in refs} >= {0x644280, 0x644AA0})
print("FAILS", fails)
sys.exit(1 if fails else 0)
