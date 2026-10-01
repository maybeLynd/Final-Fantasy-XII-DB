"""DD residue batch 7 (SWE2-CONTRACT, 2026-09-30): checks behind the lifetime evidence note's regrouped Limits.

Page: 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md (note_kind evidence).
Run: python -B b7_lifetime.py   (FAILS 0)

  D1  the pass-22 CombatAction line's dispatcher 002FC3C0: 183 B; byte [rec+0x23] & 0xF, bounded to 7, eight-entry RVA
      table at 002FC478 whose every target lies inside the body; the arm at 002FC442 calls 0024F410
  M1  the arena selector map 022D89A8..022D89B6: exactly two rip-relative references, both LEA in the two fillers
      00369D30 / 0036A280; the only other instruction carrying the map's image displacement 0x021B89A8 is the push's
      indexed read 0036C272 (raw dword search over every listed body; the pin is the positive control)
  S1  relocation scheduling: 0024D540 is called directly only by 0022B0B0, 0022B8C0 and 0022BC20 (the main-loop frame
      functions); 003B3480 only by the handle resolver 003B3C00; 0024D970 only by 003B3480 and 003B3550
  E1  005004C0 switches on the definition byte +0x44 (0050050B), bounded to 0xD1 (00500510), two-stage (byte table then
      dword table, 0050051B / 00500524) - the setup dispatcher the effect-dispatch page decodes (its section 2.5)
  G1  header word +0x3E: the free routine clears it as a word (00369B4F); the settings byte 022D8E1C is read by the arena
      allocator as its fallback (0036BD19)
  C1  the handle's copied word: header +0x1C has one store in the arena code (0036A517, the header writer 0036A490's
      fourth argument); all seven callers pass the arena's word +0x60, which the allocation paths increment; six
      readers (the binders copy it into slot +6, the tagged access paths compare it). Range 00369000..0036E000,
      register+displacement forms only
  R1  register state at HEAD of the rows the Limits section cites: J-C / CD-2 / BW-2 / OV-24 SUPERSEDED, OV-25 / OV-26
      ANSWERED, OV-27 / OV-28 NOT A QUESTION, SD-166 OPEN (answered in OPUS's record, row not yet incorporated)
  A1  OPUS's SD-166 record is tracked and states the answer the note cites
"""
import hashlib, io, os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))            # .../Database/FFXII TZA
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    got = ins(a)
    check(name, text in got, "%08X  %s" % (a, got))


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")
sz = T.sizes()
sc = T.scan()

# D1
check("D1 002FC3C0 extent 183 B", sz.get(0x002FC3C0) == 183, str(sz.get(0x002FC3C0)))
pin("D1 reads rec+0x23", 0x002FC3C6, "movzx eax, byte ptr [rcx + 0x23]")
pin("D1 low nibble", 0x002FC3CD, "and eax, 0xf")
pin("D1 bounded to 7", 0x002FC3D0, "cmp eax, 7")
pin("D1 table read (RVA 0x1DC478 = 002FC478)", 0x002FC3E2, "0x1dc478")
pin("D1 indirect jump", 0x002FC3EC, "jmp rdx")
tab = [struct.unpack_from("<I", T.R.at(0x002FC478, 32), 4 * k)[0] + 0x00120000 for k in range(8)]
check("D1 eight table targets inside the body", all(0x002FC3C0 <= t < 0x002FC3C0 + 183 for t in tab),
      " ".join("%08X" % t for t in tab))
pin("D1 arm calls 0024F410", 0x002FC442, "call 0x24f410")

# M1
refs = sorted((ad, f, k) for g in sc["refs"] if 0x022D89A8 <= g <= 0x022D89B6 for f, ad, k in sc["refs"][g])
check("M1 rip references into the map", refs == [(0x00369D79, 0x00369D30, "lea"), (0x0036A282, 0x0036A280, "lea")],
      " ".join("%08X(%08X,%s)" % r for r in refs))
pin("M1 control: the push's indexed read", 0x0036C272, "movzx eax, byte ptr [rax + rbx + 0x21b89a8]")
needle = struct.pack("<I", 0x021B89A8)
hits = []
for f, n in sz.items():
    d = T.R.at(f, n)
    if not d:
        continue
    k = d.find(needle)
    while k >= 0:
        hits.append((f, f + k))
        k = d.find(needle, k + 1)
hits = sorted(set(hits))
check("M1 image-displacement form: one instruction only, in 0036C1F0",
      [f for f, _ in hits] == [0x0036C1F0] and 0x0036C272 < hits[0][1] < 0x0036C272 + 8,
      " ".join("%08X@%08X" % h for h in hits))

# S1
def callers(t):
    return sorted({f for f, _ in sc["calls"].get(t, ())})
check("S1 0024D540 callers = the three main-loop frame functions", callers(0x0024D540) == [0x0022B0B0, 0x0022B8C0, 0x0022BC20],
      " ".join("%08X" % x for x in callers(0x0024D540)))
check("S1 003B3480 caller = the handle resolver", callers(0x003B3480) == [0x003B3C00],
      " ".join("%08X" % x for x in callers(0x003B3480)))
check("S1 0024D970 callers", callers(0x0024D970) == [0x003B3480, 0x003B3550],
      " ".join("%08X" % x for x in callers(0x0024D970)))

# E1
pin("E1 switch byte +0x44", 0x0050050B, "movzx eax, byte ptr [r8 + 0x44]")
pin("E1 bound 0xD1", 0x00500510, "cmp eax, 0xd1")
pin("E1 byte index table", 0x0050051B, "movzx eax, byte ptr [r9 + rax + 0x3e0774]")
pin("E1 dword target table", 0x00500524, "mov ecx, dword ptr [r9 + rax*4 + 0x3e06b4]")

# G1
pin("G1 free clears the +0x3E word", 0x00369B4F, "mov word ptr [rbx + 0x3e], si")
pin("G1 022D8E1C is the allocator's fallback read", 0x0036BD19, "mov eax, dword ptr [rip + 0x1f6d0fd]")

# C1: the handle's copied word. Census of 16-bit accesses at +0x1C and of the arena's +0x60 word, over the arena code
# range 00369000..0036E000 (register+displacement forms only - the stated blind spot)
def grep_range(rx, lo=0x00369000, hi=0x0036E000):
    out = []
    for f, n in sorted(sz.items()):
        if not lo <= f < hi:
            continue
        d = T.R.at(f, n)
        for i in T.R.md.disasm(d, f) if d else ():
            if re.search(rx, "%s %s" % (i.mnemonic, i.op_str)):
                out.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str)))
    return out
w1c = grep_range(r"word ptr \[r[a-z0-9]+ \+ 0x1c\]")
st1c = [x for x in w1c if x[2].startswith("mov word ptr")]
check("C1 one store to header +0x1C: 0036A517 in the header writer", [x[1] for x in st1c] == [0x0036A517],
      " ".join("%08X" % x[1] for x in st1c))
pin("C1 the stored word is the writer's fourth argument", 0x0036A4C0, "mov edi, r9d")
check("C1 readers of +0x1C", sorted(x[1] for x in w1c if x not in st1c) ==
      [0x0036A034, 0x0036A266, 0x0036A36D, 0x0036A45D, 0x0036B005, 0x0036D19A],
      " ".join("%08X" % x[1] for x in w1c if x not in st1c))
cs = sorted(sc["calls"].get(0x0036A490, ()))
arg = []
for f, site in cs:
    body = list(T.R.md.disasm(T.R.at(f, site - f), f))
    last = [i for i in body if "r9d" in i.op_str.split(",")[0]]
    arg.append((site, "%s %s" % (last[-1].mnemonic, last[-1].op_str) if last else "?"))
check("C1 every caller of 0036A490 passes the arena's word +0x60",
      len(arg) == 7 and all(re.fullmatch(r"movzx r9d, word ptr \[r[a-z0-9]+ \+ 0x60\]", a) for _, a in arg),
      "; ".join("%08X:%s" % a for a in arg))
inc = [x[1] for x in grep_range(r"^inc word ptr \[r[a-z0-9]+ \+ 0x60\]")]
check("C1 the +0x60 word is a counter the allocation paths increment", inc == [0x0036BC31, 0x0036BFC5, 0x0036C35B,
      0x0036C470, 0x0036CE3E], " ".join("%08X" % x for x in inc))

# R1: register lead words at HEAD (the committed register, not a peer's worktree edit)
oq = subprocess.run(["git", "show", "HEAD:Database/FFXII TZA/_index/OPEN-QUESTIONS.md"], capture_output=True,
                    cwd=DB).stdout.decode("utf-8", "replace")
want = {"J-C": "SUPERSEDED", "CD-2": "SUPERSEDED", "BW-2": "SUPERSEDED", "OV-24": "SUPERSEDED", "OV-25": "ANSWERED",
        "OV-26": "ANSWERED", "OV-27": "NOT A QUESTION", "OV-28": "NOT A QUESTION", "SD-166": "OPEN"}
for rid, w in want.items():
    m = re.search(r"^\|\s*%s\s*\|(.*)$" % re.escape(rid), oq, re.M)
    last = m.group(1).rstrip().rstrip("|").split("|")[-1] if m else ""
    lead = last.strip().lstrip("*~ ").upper()
    check("R1 %s lead word %s" % (rid, w), lead.startswith(w), lead[:40])

# A1
rec = os.path.join(DB, "_index", "candidates", "sd166-arena-7-0930", "README.md")
tracked = subprocess.run(["git", "ls-files", "--error-unmatch", rec], capture_output=True, cwd=DB).returncode == 0
t = io.open(rec, encoding="utf-8").read()
check("A1 SD-166 record tracked and states the answer", tracked and "No code path in the shipped game selects arena 7" in t)

print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
