"""regress_bound.py - actual invocations of three_check_bound.py on three input pairs (FABLE, Claude Opus 5.5, 2026-09-28,
on ASTRA-REQ-FABLE-CONSUMER-SOURCE-VIEW-BINDING). The producer is run as a subprocess through its documented
FFXII_EXE / Y1P_CACHE inputs; nothing is imported from it.

  V   the four-body view is extracted from the default Y1P_CACHE (only lines whose owner field is one of the four entries);
      the changed view differs from it in exactly one line, 00229E7E jb -> jbe
  M   the changed image is a private DATA copy of FFXII_EXE in REGRESS_TMP with exactly one byte changed (00229E7E 72 -> 76);
      it is never executed, and is deleted at the end after its path and hash are checked
  P1  original view + original image      -> exit 0, PASS B, R1 I1 A1 C PASS
  P2  original view + changed image       -> exit 2, REFUSE B, no semantic tag printed (the stale pair ASTRA ran green)
  P3  changed view + changed image        -> exit 1, PASS B, R1 FAIL, I1 A1 C PASS (the detector's positive)
  P4  changed view + original image       -> exit 2, REFUSE B
  K   cleanup: the changed image and both views are removed; the original image's hash is unchanged
"""
import hashlib, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(HERE, "three_check_bound.py")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
TMP = os.environ.get("REGRESS_TMP", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/regress_bound")
OWN = ("00229E70", "0020E600", "0020E620", "00339630")
MUT_OFF_PC = 0x00229E7E
sha = lambda b: hashlib.sha256(b).hexdigest()
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)

os.makedirs(TMP, exist_ok=True)
orig = open(EXE, "rb").read(); orig_h = sha(orig)
view = [l for l in open(CACHE, encoding="utf-8", errors="replace") if len(l.split(None, 2)) == 3 and l.split(None, 2)[1] in OWN]
chg = [l.replace(" jb 0x229e91", " jbe 0x229e91") if l.startswith("00229E7E ") else l for l in view]
nd = sum(a != b for a, b in zip(view, chg))
vp, cvp = os.path.join(TMP, "view_original.txt"), os.path.join(TMP, "view_changed.txt")
open(vp, "w", encoding="utf-8", newline="").write("".join(view)); open(cvp, "w", encoding="utf-8", newline="").write("".join(chg))
ok("V", len(view) == 242 and nd == 1, "view %d lines (sha256 %s); changed view differs in %d line" % (len(view), sha("".join(view).encode())[:16], nd))

# locate 00229E7E in the file through the section table, then change one byte in a private copy
import struct
pe = struct.unpack_from("<I", orig, 0x3c)[0]; nsec = struct.unpack_from("<H", orig, pe + 6)[0]; opt = struct.unpack_from("<H", orig, pe + 20)[0]
o = pe + 24 + opt; fo = None
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", orig, o + 8); o += 40
    if va <= MUT_OFF_PC - 0x120000 < va + rs: fo = ra + MUT_OFF_PC - 0x120000 - va
m = bytearray(orig); before = m[fo]; m[fo] = 0x76; m = bytes(m)
mp = os.path.join(TMP, "changed-image-data.bin"); open(mp, "wb").write(m)
ndiff = sum(1 for a, b in zip(orig, m) if a != b) if len(orig) == len(m) else -1
ok("M", before == 0x72 and ndiff == 1 and sha(open(mp, "rb").read()) == sha(m),
   "file offset %X: %02X -> 76; %d byte differs; changed image sha256 %s" % (fo, before, ndiff, sha(m)))

def run(name, exe, cache):
    env = dict(os.environ, FFXII_EXE=exe, Y1P_CACHE=cache)
    p = subprocess.run([sys.executable, PROD], env=env, capture_output=True, text=True)
    tags = {}
    for st, tg in re.findall(r"^(PASS|FAIL|REFUSE) (\w+)", p.stdout, re.M): tags[tg] = st
    print("  %s rc=%d tags=%s stdout sha256 %s stderr %d B" % (name, p.returncode, tags, sha(p.stdout.encode())[:16], len(p.stderr)))
    return p.returncode, tags
rc, t = run("P1", EXE, vp)
ok("P1", rc == 0 and t == {"B": "PASS", "R1": "PASS", "I1": "PASS", "A1": "PASS", "C": "PASS"}, "original pair")
rc, t = run("P2", mp, vp)
ok("P2", rc == 2 and t == {"B": "REFUSE"}, "stale view with changed image is refused before any semantic check")
rc, t = run("P3", mp, cvp)
ok("P3", rc == 1 and t == {"B": "PASS", "R1": "FAIL", "I1": "PASS", "A1": "PASS", "C": "PASS"}, "matching changed pair: R1 fails, nothing else")
rc, t = run("P4", EXE, cvp)
ok("P4", rc == 2 and t == {"B": "REFUSE"}, "changed view with original image is refused")

for p in (mp, vp, cvp):
    if os.path.dirname(os.path.abspath(p)) == os.path.abspath(TMP): os.remove(p)
gone = not any(os.path.exists(p) for p in (mp, vp, cvp))
if gone and not os.listdir(TMP): os.rmdir(TMP)
ok("K", gone and sha(open(EXE, "rb").read()) == orig_h, "private files removed; original image sha256 %s unchanged" % orig_h[:16])
print("FAILS", fails); sys.exit(1 if fails else 0)
