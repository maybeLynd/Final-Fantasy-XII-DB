"""oeb_ps2.py - guard parts 1 and 3 for the PS2-executable rows (MH-1, UQ-36, UQ-39) under OUT OF EVIDENCE BOUNDARY
(FABLE, Claude Opus 5.5, 2026-09-27).

  P1  the excluded source is named by a shipped file: ps2data/cdi/in/system.cnf says BOOT2 = cdrom0:\\SLPM_667.50;1
  P2  that executable does not ship: no file named SLPM_667.50 (any case or separator) and no ELF of any machine type in
      the extract or in the install (x64/, the shipped data trees lost_build_scan.py walks)
  PC  control for P2: a planted MIPS ELF header and a planted SLPM_667.50 in a scratch directory are both found by the
      same walker and detector
Args: [INSTALL] [EXTRACT] (defaults as lost_build_scan.py).
"""
import os, re, struct, sys, tempfile
INSTALL = sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII MP Mod/FFXII_TestClient1"
EXTRACT = sys.argv[2] if len(sys.argv) > 2 else "D:/FFXII_TZA_extract"
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
NAME = re.compile(r"^slpm[_-]?667\.?50", re.I)
def walk(roots):
    n, names, elfs = 0, [], []
    for root in roots:
        for dp, _, fs in os.walk(root):
            for f in fs:
                n += 1; p = os.path.join(dp, f)
                if NAME.match(f): names.append(p)
                try:
                    with open(p, "rb") as h: b = h.read(20)
                except OSError: continue
                if b[:4] == b"\x7fELF" and len(b) >= 20: elfs.append((p, struct.unpack_from("<H", b, 18)[0]))
    return n, names, elfs
cnf = open(os.path.join(EXTRACT, "ps2data/cdi/in/system.cnf"), "rb").read().decode("ascii", "replace")
ok("P1", re.search(r"BOOT2\s*=\s*cdrom0:\\SLPM_667\.50;1", cnf) is not None, "system.cnf: %r" % cnf.strip().splitlines()[0])
roots = [EXTRACT] + [os.path.join(INSTALL, d) for d in os.listdir(INSTALL)]
n, names, elfs = walk(roots)
ok("P2", n > 89000 and not names and not elfs, "%d files walked (extract + install); SLPM names %r; ELF files %r" % (n, names[:3], elfs[:3]))
with tempfile.TemporaryDirectory() as d:
    open(os.path.join(d, "SLPM_667.50"), "wb").write(b"x")
    open(os.path.join(d, "planted.elf"), "wb").write(b"\x7fELF" + b"\x01\x01\x01" + b"\0" * 9 + struct.pack("<HH", 2, 8))  # e_ident is 16 bytes; e_machine at 18
    cn, cnames, celfs = walk([d])
ok("PC", len(cnames) == 1 and celfs and celfs[0][1] == 8, "planted: names %d, ELF machine %r (8 = MIPS)" % (len(cnames), [m for _, m in celfs]))
print("FAILS", fails); sys.exit(1 if fails else 0)
