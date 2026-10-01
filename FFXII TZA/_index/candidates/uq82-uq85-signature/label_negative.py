"""label_negative.py - the performed negative behind UQ-82 / UQ-85's NO ADMISSIBLE SOURCE, as a re-runnable control
(FABLE, Claude Opus 5.5, 2026-09-27). FABLE ran instruments A and B on 2026-09-17 and OPUS signed on them
(FABLE-ANSWER-OPUS-UQ82-UQ85-REQUIREMENT-3-PERFORMED-AND-THE-NEAR-MISS-RUN-DOWN); they were never committed.

  A   the three shipped navimapdata.bin copies (ch, cn, in) are 3,470 B, magic NAV, with no printable run of 4+ bytes
  AC  control for A: the same run detector finds runs in a file known to hold text (filelistlocalin.bin names navimapdata)
  B   the bit-15 predicate 00377C20, its thunk 00313F60 and every direct caller of either: no instruction in those bodies
      has a rip-relative operand that resolves to a printable C string of 4+ characters
  BC  control for B: the same resolver finds the string in the debug-menu renderer 001CD0E0 ('Use Town' / 'Use Field')
Reads the capstone listing (Y1P_CACHE) and the shipping image (FFXII_EXE); the extract root is EXTRACT.
"""
import os, re, struct, sys
CACHE = os.environ.get("Y1P_CACHE", r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt")
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
EXTRACT = os.environ.get("EXTRACT", r"D:/FFXII_TZA_extract")
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
RUN = re.compile(rb"[\x20-\x7e]{4,}")
sizes, runs = {}, {}
for lang in ("ch", "cn", "in"):
    d = open(os.path.join(EXTRACT, "ps2data/image/ff12", lang, "bin/navimapdata.bin"), "rb").read()
    sizes[lang] = (len(d), d[:3]); runs[lang] = len(RUN.findall(d))
ok("A", all(s == (3470, b"NAV") for s in sizes.values()) and not any(runs.values()), "sizes/magic %r, printable runs %r" % (sizes, runs))
ctl = [os.path.join(r, f) for r, _, fs in os.walk(EXTRACT) for f in fs if f == "filelistlocalin.bin"][:1]
cruns = RUN.findall(open(ctl[0], "rb").read()) if ctl else []
ok("AC", any(b"navimapdata" in r for r in cruns), "control file %s: %d runs, one naming navimapdata" % (ctl[0] if ctl else "-", len(cruns)))
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3c)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]; secs = []
o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8); secs.append((va, vs, ra, rs)); o += 40
def cstr(v):
    r = v - base
    for va, vs, ra, rs in secs:
        if va <= r < va + rs:
            f = ra + (r - va); e = d.find(b"\0", f, f + 256)
            s = d[f:e] if e > f else b""
            return s.decode("latin-1") if len(s) >= 4 and all(0x20 <= c < 0x7f for c in s) else None
    return None
body, callers = {}, set()
for line in open(CACHE, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split(None, 2)
    if len(p) < 3: continue
    body.setdefault(p[1], []).append(p[2])
    if re.search(r"\b(call|jmp) 0x(377c20|313f60)\b", p[2]): callers.add(p[1])
pop = sorted(callers | {"00377C20", "00313F60"})
def strings_in(f):
    out = []
    for ins in body.get(f, []):
        m = re.search(r"=>([0-9A-F]{8})", ins)
        if m and "rip" in ins:
            s = cstr(int(m.group(1), 16))
            if s: out.append(s)
    return out
hits = {f: strings_in(f) for f in pop}
found = {f: s for f, s in hits.items() if s}
ok("B", len(pop) == 112 and not found, "%d bodies (the predicate and %d direct callers, the thunk among them); bodies with a string operand: %r" % (len(pop), len(pop) - 1, found))
cs = strings_in("001CD0E0")
ok("BC", "Use Town" in cs and "Use Field" in cs, "control 001CD0E0 resolves %d strings incl. 'Use Town'/'Use Field'" % len(cs))
print("FAILS", fails); sys.exit(1 if fails else 0)
