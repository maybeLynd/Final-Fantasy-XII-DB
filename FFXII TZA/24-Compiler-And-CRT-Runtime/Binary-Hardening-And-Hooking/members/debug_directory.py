"""debug_directory.py - the image's debug directory, read (FABLE, Claude Opus 5.5, 2026-09-26).

The PE debug directory (data directory 6) holds four entries. Three of them carry build facts this page had not read.
  D1 CodeView (type 2): an RSDS record naming the build's PDB, E:\\Jenkins\\workspace\\C11019P16003\\Code\\source\\
     FF12_PS2_IN\\FF12\\x64_Retail\\FF12X64.pdb. The PDB itself is not shipped (checked separately by the package scan).
  D2 VC_FEATURE (type 12): five counts - pre-VC++ 11.00 objects 0, C/C++ objects 1,296, /GS 1,265, /sdl 89, guardN 49.
     Only 49 of the 1,296 objects were compiled guard-aware. That agrees with section 9a's measurement: only the
     statically linked CRT consults the guard slot.
  D3 POGO (type 13, 'GCTL'): the linker's list of section contributions. Two entries decide what S-2 and T-9 rest on:
       .gfids$y  0x30 bytes at the first byte of the .gfids section (RVA 0x02EE3000): the twelve dwords are one
                 grouped INPUT contribution named .gfids$y, not a table the linker built;
       .00cfg    0x10 bytes at RVA 0x007A31C0 = GuardCFCheckFunctionPointer 0x008C31C0 minus the image base, with the
                 dispatch pointer 0x008C31C8 its second qword: the two guard pointers are an input contribution too
                 (the CRT's .00cfg), not linker-generated.
  D4 control: the load config reproduces this page's published figures (check / dispatch pointers, table 0, count 0,
     GuardFlags 0x100) and the twelve .gfids dwords read 49 48 19 10 13 16 69 113 10 98 55 11.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]; opt = pe + 24
secs = {struct.unpack_from("<8s", d, pe + 24 + optsz + i * 40)[0].rstrip(b"\0").decode():
        struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8) for i in range(n)}   # name -> (vsize, rva, rawsize, rawptr)
def off(rva):
    for vs, va, rs, ro in secs.values():
        if va <= rva < va + max(vs, rs): return rva - va + ro
DD = opt + 112                                   # PE32+ data directories
drva, dsz = struct.unpack_from("<II", d, DD + 8 * 6)
ents = [struct.unpack_from("<IIHHIIII", d, off(drva) + 28 * k) for k in range(dsz // 28)]
by = {e[4]: e for e in ents}
# D1
cv = by.get(2); rec = d[cv[7]:cv[7] + cv[5]] if cv else b""
pdb = rec[24:rec.find(b"\0", 24)].decode(errors="replace") if rec[:4] == b"RSDS" else ""
check("D1 CodeView RSDS names the build PDB", pdb.endswith("\\FF12\\x64_Retail\\FF12X64.pdb") and "FF12_PS2_IN" in pdb, pdb)
# D2
vf = struct.unpack_from("<5I", d, by[12][7]) if 12 in by and by[12][5] == 20 else None
check("D2 VC_FEATURE: 0 pre-VC11, 1296 C/C++, 1265 /GS, 89 /sdl, 49 guardN", vf == (0, 1296, 1265, 89, 49), str(vf))
# D3
pg = by.get(13); contrib = {}
if pg and d[pg[7]:pg[7] + 4] == b"GCTL":
    q, end = pg[7] + 4, pg[7] + pg[5]
    while q < end - 8:
        rva, sz = struct.unpack_from("<II", d, q); s = d[q + 8:d.find(b"\0", q + 8)].decode()
        contrib.setdefault(s, []).append((rva, sz)); q = (q + 8 + len(s) + 1 + 3) & ~3
gf = secs[".gfids"]
check("D3 POGO: the .gfids section's content is one .gfids$y input contribution of 0x30 bytes at its first byte",
      contrib.get(".gfids$y") == [(gf[1], 0x30)] and gf[0] == 0x30 and not any(k.startswith(".gfids") and k != ".gfids$y" for k in contrib),
      "%s; .gfids rva %08X vsize %X" % (contrib.get(".gfids$y"), gf[1], gf[0]))
LC = struct.unpack_from("<II", d, DD + 8 * 10)[0]; lc = off(LC)
chk, dsp, tbl, cnt = struct.unpack_from("<QQQQ", d, lc + 0x70); flags = struct.unpack_from("<I", d, lc + 0x90)[0]
check("D3 POGO: the guard check/dispatch pointers are the .00cfg input contribution (0x10 bytes)",
      contrib.get(".00cfg") == [(chk - BASE, 0x10)] and dsp == chk + 8, "%s; check %08X dispatch %08X" % (contrib.get(".00cfg"), chk, dsp))
# D4
g12 = struct.unpack_from("<12I", d, off(gf[1]))
check("D4 control: load-config figures and the twelve .gfids dwords reproduce the page",
      (chk, dsp, tbl, cnt, flags) == (0x8C31C0, 0x8C31C8, 0, 0, 0x100) and g12 == (49, 48, 19, 10, 13, 16, 69, 113, 10, 98, 55, 11),
      "flags %X dwords %s" % (flags, g12))
print("FAILS", fails)
sys.exit(1 if fails else 0)
