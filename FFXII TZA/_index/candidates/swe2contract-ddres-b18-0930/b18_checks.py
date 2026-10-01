"""DD residue batch 18 (SWE2-CONTRACT for OPUS, 2026-10-01): checks behind the lifetime evidence note's Limits items
17-23 and the dated pointers added to its sections 2-20.

Page: 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md (note_kind evidence).
Run: python -B b18_checks.py   (from any folder; FAILS 0). Static, over the certified image through retool.py, plus one
walk of the game extract D:/FFXII_TZA_extract (B4-B6) with the EFX stream walker of type_census.py.

  T1-T5  the prefix tag (Limits 17): the two taggers store low16(arg 3) at payload -0x22 (header +0x1E); what the 66
         call sites of 0036C660 pass; the field's readers (four header copies, one zero test in the dump 0036A570, no
         payload-relative reader image-wide); the free clears it
  A1-A3  arena 11's replacement 0037B3D0 (Limits 18, FABLE's arena-residue record T re-pinned): report, disable, free the
         old backing through the CRT free import, allocate, re-initialise
  U1-U3  the area unload 002628B0 (Limits 19): its two callers, the drain's single caller, the world-tick page's
         subtree and its answered EX-9 box
  B1-B6  the 0x800 / 0xA00 registries (Limits 20, 21): capacities, the registrars' id / subtype reads, and the shipped
         data: every word id below capacity, none 0, none repeated in a stream; the 0x800 subtype byte stays in 0..8
  G1-G5  0024D050 (Limits 22): one direct caller, the game-over widget's countdown task; no other reference; the
         per-instance callees call no release
  S1     0024D540 (Limits 13): the three main-loop frame functions (b7 S1, re-pinned)
  R1     register rows the Limits section cites, lead words at HEAD
  Q1     the board requests the sections route: DONE in TEAM.json (read only; monotonic states only)
  P1     the cited records and pages state what the Limits items quote
  Z1-Z4  the page edit: the struck sentence kept verbatim, every batch-18 note present, LF-only, no '|' in a note
"""
import collections, hashlib, io, json, os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TZA = os.path.abspath(os.path.join(HERE, "..", "..", ".."))              # .../Database/FFXII TZA
DB = os.path.abspath(os.path.join(TZA, ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, os.path.join(TZA, "17-Presentation-Rendering", "Effect-File-Formats", "members"))
import retool as T  # noqa: E402

FAILS = 0
PASSES = 0


def check(name, ok, detail=""):
    global FAILS, PASSES
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if ok:
        PASSES += 1
    else:
        FAILS += 1


def ins(a):
    i = next(T.R.md.disasm(T.R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    got = ins(a)
    check(name, text in got, "%08X  %s" % (a, got))


SZ = T.sizes()


def body(f):
    return list(T.R.md.disasm(T.R.at(f, SZ[f]), f))


def rip(i):
    for op in i.operands:
        if op.type == 3 and op.mem.base == T.RIP:
            return i.address + i.size + op.mem.disp
    return None


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8", sha[:16])
SC = T.scan()


def callers(f):
    return sorted(SC["calls"].get(f, ()))


def refs(g):
    return sorted(SC["refs"].get(g, ()))


def page(p):
    return io.open(os.path.join(TZA, p), encoding="utf-8").read()


H = lambda xs: " ".join("%08X" % x for x in xs)  # noqa: E731

# ---------------------------------------------------------------- T: the prefix tag (Limits 17)
pin("T1 0036C660 keeps arg 3 in edi", 0x0036C66A, "mov edi, r8d")
pin("T1 0036C660 stores its low 16 bits at payload -0x22", 0x0036C6A0, "mov word ptr [rbx - 0x22], di")
pin("T1 0036C6C0 (handle form) keeps arg 3 in esi", 0x0036C6CA, "mov esi, r8d")
pin("T1 0036C6C0 stores it at payload -0x22", 0x0036C72C, "mov word ptr [rbx - 0x22], si")
pin("T1 control: the page's own case passes 0x95C", 0x003303A4, "mov r8d, 0x95c")

sites = callers(0x0036C660)
cls = collections.Counter()
lines_ = []
for f, s in sites:
    b = body(f)
    k = next(j for j, i in enumerate(b) if i.address == s)
    win = b[max(0, k - 25):k]
    r8 = next((i for i in reversed(win) if i.op_str.split(",")[0] in ("r8d", "r8")), None)
    rdx = next((i for i in reversed(win) if i.op_str.split(",")[0] in ("rdx", "edx")), None)
    basename = any(i.mnemonic == "call" and i.op_str == "0x36c750" for i in win[-12:])
    if r8 is not None and r8.mnemonic == "xor":
        cls["zero"] += 1
    elif r8 is not None and r8.mnemonic == "mov" and r8.operands[1].type == 2:
        imm = r8.operands[1].imm
        if basename and rdx is not None and rdx.op_str == "rdx, rbx":
            cls["imm+basename"] += 1
            lines_.append(imm)
        else:
            cls["imm+label"] += 1
    else:
        cls["register/memory"] += 1
check("T2 0036C660 has 63 direct call sites", len(sites) == 63, str(len(sites)))
check("T2 tag argument classes", dict(cls) == {"imm+basename": 25, "zero": 13, "register/memory": 22, "imm+label": 3},
      str(dict(cls)))
check("T2 the basename-labelled immediates lie in 0xF3..0x16E6 (line-like)",
      bool(lines_) and min(lines_) == 0xF3 and max(lines_) == 0x16E6, "%X..%X" % (min(lines_), max(lines_)))
pin("T2 EVTMEM passes its size 0x100000 (low 16 bits 0)", 0x0025A9F7, "mov r8d, 0x100000")

reads = []        # every access to word [reg + 0x1E] in the arena code that is not a store
for f, n in sorted(SZ.items()):
    if not (0x00369000 <= f < 0x0036E000):
        continue
    for i in body(f):
        if "word ptr [" in i.op_str and "+ 0x1e]" in i.op_str:
            is_store = i.mnemonic == "mov" and i.op_str.startswith("word ptr [")
            if not is_store:
                reads.append((f, i.address, i.mnemonic))
want_reads = [(0x0036A2A0, 0x0036A309, "movzx"), (0x0036A570, 0x0036A6E0, "cmp"), (0x0036B980, 0x0036BB61, "movzx"),
              (0x0036CB00, 0x0036CD0E, "movzx"), (0x0036CB00, 0x0036CF6B, "movzx")]
check("T3 reads of header +0x1E in the arena code: four copies and one zero test",
      sorted(reads) == want_reads, "; ".join("%08X@%08X %s" % r for r in reads))
pin("T3 0036CB00's second copy lands in the new header (through its template +0x4E)", 0x0036CFCC, "mov word ptr [rdi + 0x1e], ax")
pin("T3 0036A2A0 copies it into its header template", 0x0036A30D, "mov word ptr [rsp + 0x3e], ax")
pin("T3 0036A2A0 writes the template's word into the rebuilt header", 0x0036A404, "mov word ptr [rbx + 0x1e], ax")
pin("T3 0036B980 copies it header to header", 0x0036BB65, "mov word ptr [rdi + 0x1e], ax")
pin("T3 0036CB00 copies it into its header template", 0x0036CD1A, "mov word ptr [rsp + 0x4e], ax")
pin("T3 the dump's zero test decides only whether the block's name is printed", 0x0036A6E5, "jne 0x36a6ed")
pin("T3 ... and the taken branch copies the name +0x34", 0x0036A6EF, "lea rdx, [rbx + 0x34]")
neg = []
for f, n in sorted(SZ.items()):
    d = T.R.at(f, n)
    if not d:
        continue
    for i in T.R.md.disasm(d, f):
        if re.search(r"(?<![dq])word ptr \[[^\]]*- 0x22\]", i.op_str):
            neg.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str)))
check("T4 image-wide word accesses at [reg - 0x22]: the two tagger stores and one stack slot",
      [a for _, a, _ in neg] == [0x0036C6A0, 0x0036C72C, 0x004197F8], "; ".join("%08X %s" % (a, t) for _, a, t in neg))
pin("T4 control: 00418880's rbp is a stack frame", 0x0041888C, "lea rbp, [rsp - 0x380]")
pin("T5 the free routine clears the tag", 0x00369B3C, "mov word ptr [rbx + 0x1e], si")
pin("T5 ... with the register that clears the name byte", 0x00369B36, "mov byte ptr [rbx + 0x34], sil")

# ---------------------------------------------------------------- A: arena 11's replacement (Limits 18)
seq = [(0x0037B3FE, "mov ecx, 0xb"), (0x0037B403, "call 0x369760"), (0x0037B40D, "call 0x36d160"),
       (0x0037B412, "mov rcx, qword ptr [rip + 0x1c595ff]"), (0x0037B419, "call 0x36d250"), (0x0037B420, "call 0x36d240"),
       (0x0037B42B, "mov qword ptr [rip + 0x1c595e6], rax"), (0x0037B425, "mov r9d, 0x100"), (0x0037B43D, "call 0x369d30")]
for a, t in seq:
    pin("A1 0037B3D0 sequence", a, t)
b = {i.address: i for i in body(0x0037B3D0)}
check("A1 the freed and the stored qword are arena 11's backing slot 01FD4A18",
      rip(b[0x0037B412]) == 0x01FD4A18 and rip(b[0x0037B42B]) == 0x01FD4A18)
pin("A2 0036D250 tail-jumps for a non-null pointer", 0x0036D253, "jne 0x19c590")
i = next(T.R.md.disasm(T.R.at(0x0019C590, 8), 0x0019C590, 1))
check("A2 0019C590 jumps through IAT slot 008C2B48", i.mnemonic == "jmp" and rip(i) == 0x008C2B48)
tsv = io.open(os.path.join(TZA, "24-Compiler-And-CRT-Runtime", "Runtime-Service-Surface", "members", "iat-any-reference.tsv"),
              encoding="utf-8").read()
check("A2 IAT 008C2B48 is the CRT free import", re.search(r"^008C2B48\tapi-ms-win-crt-heap-l1-1-0\.dll\tfree\t", tsv, re.M) is not None)
pin("A3 the report 00369760 runs the dump 0036A570 when the arena is not one whole free block", 0x003697B2, "call 0x36a570")
check("A3 0036D250 has one caller, 0037B3D0", [s for _, s in callers(0x0036D250)] == [0x0037B419])

# ---------------------------------------------------------------- U: the area unload 002628B0 (Limits 19)
check("U1 002628B0 direct callers", callers(0x002628B0) == [(0x0025BFB0, 0x0025C036), (0x0032FCA0, 0x0032FCF6)],
      str([(H([f]), H([s])) for f, s in callers(0x002628B0)]))
check("U2 the drain 0025BFB0 is called only by the tick 00314020 at 00314078",
      callers(0x0025BFB0) == [(0x00314020, 0x00314078)])
wt = page("00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md")
check("U3 the world-tick page owns the unload's subtree and EX-9 is a ticked box",
      "### The `002628B0` exclusive subtree" in wt and re.search(r"^- \[x\] \*\*EX-9\.\*\*", wt, re.M) is not None)

# ---------------------------------------------------------------- B: the registries and the shipped ids (Limits 20, 21)
pin("B1 0x800 table: 003A9560 allocates 0xA00 bytes (320 slots)", 0x003A9564, "mov ecx, 0xa00")
pin("B1 0xA00 table: 003A9920 allocates 0x1800 bytes (768 slots)", 0x003A9924, "mov ecx, 0x1800")
for a, t in ((0x003A973A, "movzx r8d, word ptr [rcx]"), (0x003A974B, "movzx eax, byte ptr [rdi + 2]"),
             (0x003A974F, "mov byte ptr [rcx + 0x282], al"), (0x003A9767, "mov qword ptr [r8 + r9*8], rcx"),
             (0x003A9A7A, "movzx r8d, word ptr [rcx]"), (0x003A9A8B, "movzx eax, byte ptr [rdi + 2]"),
             (0x003A9A8F, "mov byte ptr [rcx + 0x44], al"), (0x003A9AA1, "mov qword ptr [r8 + r9*8], rcx")):
    pin("B2 registrar", a, t)
pin("B3 the teardown walk starts at index 1 (0x800 table)", 0x003A967A, "cmp rbx, 0xa00")
import type_census as TC  # noqa: E402
std = []
for dp, dn, fn in os.walk(os.path.join(TC.ROOT, "ps2data")):
    std += [os.path.join(dp, f) for f in fn if f.lower().endswith((".efx", ".efb"))]
emb = [os.path.join(TC.ROOT, l.strip()) for l in io.open(TC.EMB, encoding="utf-8") if l.strip()]
n, mx, zero, dup, sub8, inexact, nstreams, where = (collections.Counter(), collections.Counter(), collections.Counter(),
                                                    collections.Counter(), collections.Counter(), 0, 0, {})
for p in std + emb:
    data = open(p, "rb").read()
    for ch, exact in TC.streams(data):
        nstreams += 1
        inexact += not exact
        seen = {0x800: set(), 0xA00: set()}
        for ty, o in ch:
            if ty in (0x800, 0xA00):
                idx = struct.unpack_from("<H", data, o + 0xC)[0]
                n[ty] += 1
                if idx > mx[ty]:
                    mx[ty], where[ty] = idx, os.path.relpath(p, TC.ROOT).replace("\\", "/")
                zero[ty] += idx == 0
                dup[ty] += idx in seen[ty]
                seen[ty].add(idx)
                if ty == 0x800:
                    sub8[data[o + 0xE]] += 1
check("B4 control: the walk reproduces the published chunk counts (53,351 0x800; 48,868 0xA00) over exact streams",
      n[0x800] == 53351 and n[0xA00] == 48868 and inexact == 0, "%d streams, %d / %d" % (nstreams, n[0x800], n[0xA00]))
check("B5 every 0x800 id is below 320 and every 0xA00 id below 768", mx[0x800] < 320 and mx[0xA00] < 768,
      "max %d (%s), %d (%s)" % (mx[0x800], where.get(0x800), mx[0xA00], where.get(0xA00)))
check("B5 no chunk uses id 0, the slot the teardown and rebase skip", zero[0x800] == 0 and zero[0xA00] == 0)
check("B5 no id repeats within a stream", dup[0x800] == 0 and dup[0xA00] == 0)
check("B6 the 0x800 subtype byte (chunk +0xE) stays in 0..8", bool(sub8) and max(sub8) <= 8, str(sorted(sub8.items())))

# ---------------------------------------------------------------- G: 0024D050 (Limits 22)
check("G1 0024D050 has one direct caller, 003EF2E0 at 003EF419", callers(0x0024D050) == [(0x003EF2E0, 0x003EF419)])
check("G1 no rip reference and no data qword names 0024D050", not refs(0x0024D050) and not T.qword_sites(0x0024D050))
check("G2 003EF2E0's address is taken once, by 003EF830 at 003EFA2D, and nothing calls it directly",
      [(f, a, k) for f, a, k in refs(0x003EF2E0)] == [(0x003EF830, 0x003EFA2D, "lea")] and not callers(0x003EF2E0)
      and not T.qword_sites(0x003EF2E0))
pin("G2 ... and handed to the task registrar 00244F50", 0x003EFA39, "call 0x244f50")
b = {i.address: i for i in body(0x003EF830)}
check("G3 003EF830 names the game-over layout and image (00D11C88, 00D11CA0; b15 P1)",
      rip(b[0x003EF9BD]) == 0x00D11C88 and rip(b[0x003EF9D7]) == 0x00D11CA0)
for a, t in ((0x003EF405, "sub eax, 1"), (0x003EF408, "mov dword ptr [rbx + 0xc8], eax"), (0x003EF40E, "jne 0x3ef496"),
             (0x003EF414, "call 0x363560"), (0x003EF419, "call 0x24d050")):
    pin("G3 the countdown reaching zero runs 0024D050", a, t)
REL = {0x003697F0, 0x00369800, 0x00369860, 0x0019C590, 0x00210EB0}
bad = []
for f in (0x0024D050, 0x003A7420, 0x00332FA0, 0x0024FCF0, 0x003B3EA0):
    for i in body(f):
        if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == 2 and i.operands[0].imm in REL:
            bad.append("%08X" % i.address)
check("G4 0024D050, 003A7420, 00332FA0, 0024FCF0, 003B3EA0 call no release front directly", not bad, " ".join(bad))
pin("G5 003A7420 walks the instance's sixteen +0x130 slots", 0x003A7449, "cmp rbx, 0x80")
pin("G5 ... calling the slot teardown 00332FA0", 0x003A7440, "call 0x332fa0")

# ---------------------------------------------------------------- S: 0024D540 (Limits 13)
check("S1 0024D540 callers = the three main-loop frame functions",
      [f for f, _ in callers(0x0024D540)] == [0x0022B0B0, 0x0022B8C0, 0x0022BC20])

# ---------------------------------------------------------------- R: register rows at HEAD
oq = subprocess.run(["git", "show", "HEAD:Database/FFXII TZA/_index/OPEN-QUESTIONS.md"], capture_output=True,
                    cwd=TZA).stdout.decode("utf-8", "replace")
want = {"SD-164": "ANSWERED", "SD-165": "ANSWERED", "SD-166": "ANSWERED", "J-C": "SUPERSEDED", "CD-2": "SUPERSEDED",
        "BW-2": "SUPERSEDED", "OV-24": "SUPERSEDED", "OV-25": "ANSWERED", "OV-26": "ANSWERED", "OV-27": "NOT A QUESTION",
        "OV-28": "NOT A QUESTION", "OV-41": "ANSWERED", "EX-9": "ANSWERED"}
for rid, w in want.items():
    m = re.search(r"^\|\s*%s\s*\|(.*)$" % re.escape(rid), oq, re.M)
    last = m.group(1).rstrip().rstrip("|").split("|")[-1] if m else ""
    lead = last.strip().lstrip("*~ ").upper()
    check("R1 %s lead word %s" % (rid, w), lead.startswith(w), lead[:40])

# ---------------------------------------------------------------- Q: board requests (read only)
team = json.load(io.open(os.path.join(TZA, "_index", "_inbox", "TEAM.json"), encoding="utf-8"))["tasks"]
tasks = team if isinstance(team, dict) else {t.get("id"): t for t in team}
DONE = ["ASTRA-CONTRA-FABLE-RESOURCE-ARENA", "ASTRA-CONTRA-OPUS-REFERENCE-LIFETIME", "ASTRA-REQ-OPUS-ARENA-BACKING-REVIEW",
        "ASTRA-REQ-FABLE-ARENA-BACKING-SUPPLEMENT", "OPUS-ARENA-CONSUME-EXP077", "ASTRA-REQ-FABLE-ARENA-LINK-CONSUMER",
        "ASTRA-REQ-OPUS-ARENA-LINK-CONSUMER", "ASTRA-CONTRA-FABLE-ARENA-SLOT-COUNT", "ASTRA-CONTRA-OPUS-REFERENCE-MODULO-WINDOW",
        "FABLE-S24-ARENA-SLOTS", "FABLE-S24-ARENA079", "ASTRA-ARENA-CONSUMER-PRIMARY-REVIEW", "ASTRA-CONTRA-OPUS-ARENA-UNLINK-CONSUMER",
        "ASTRA-CONTRA-FABLE-ARENA-CONSUMER-BOUNDS", "ASTRA-REQ-FABLE-ARENA7-EFX-LIFETIME", "ASTRA-REQ-OPUS-ARENA7-EFX-LIFETIME",
        "ASTRA-REQ-FABLE-EFX-INPUT-LIFETIME", "ASTRA-REQ-OPUS-EFX-INPUT-LIFETIME", "ASTRA-REQ-FABLE-EFX-REBASE",
        "ASTRA-REQ-OPUS-EFX-REBASE", "ASTRA-REQ-OPUS-EFX-SOURCE-FIELDS", "ASTRA-CONTRA-FABLE-EFX-BORROW-SOURCES",
        "ASTRA-REQ-FABLE-RESOURCE-SOURCE-OWNERSHIP", "ASTRA-REQ-OPUS-RESOURCE-SOURCE-OWNERSHIP",
        "ASTRA-REQ-FABLE-RESOURCE-RELEASE-TREE", "ASTRA-REQ-OPUS-RESOURCE-RELEASE-TREE", "ASTRA-REQ-FABLE-NATIVE-RECLAMATION",
        "ASTRA-REQ-OPUS-NATIVE-RECLAMATION"]
notdone = [t for t in DONE if (tasks.get(t) or {}).get("status") != "DONE"]
check("Q1 the %d review / correction requests the sections route are DONE" % len(DONE), not notdone, " ".join(notdone))
for t in ("OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME", "SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930"):
    print("INFO %s status %s (reported, not pinned)" % (t, (tasks.get(t) or {}).get("status")))

# ---------------------------------------------------------------- P: cited records and pages
cand = os.path.join(TZA, "_index", "candidates")
ov41 = io.open(os.path.join(cand, "ov41-efx-children-fable", "README.md"), encoding="utf-8").read()
check("P1 OV-41 record: the 0x800 registrar's subtype byte is record +0x282, a family of its own",
      "| `0x800` | `003A9730` | word | record `+0x282` | `*02EBEF90` | `00442460` |" in ov41
      and "| `0xA00` | `003A9A70` | word | record `+0x44` (the element type)" in ov41)
ov42 = io.open(os.path.join(cand, "ov42-arena-residue-fable", "README.md"), encoding="utf-8").read()
check("P1 FABLE's arena-residue record states the replacement", "Arena 11 is replaced whole." in ov42
      and "frees the old backing (`0036D250` → `free`)" in ov42)
par = page("02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md")
check("P1 the parent reads 003EE2D0 and records the descriptor tail as padding",
      "`003EE2D0` (219 B) is the four-way record dispatch" in par and "The temporary does not initialize that padding" in par)
efxc = page("17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md")
check("P1 the container page's section 2b: the EFB buffer is one block freed only by the map teardown",
      "The EFB buffer is one\n  fixed block that only the map teardown `00378230` frees" in efxc)
b15 = io.open(os.path.join(cand, "swe2contract-ddres-b15-0930", "README.md"), encoding="utf-8").read()
check("P1 b15 P1 names 00D11C88 / 00D11CA0", "`00D11C88` = kind-7 id `0x39` `gameover_c.tm2`; `00D11CA0` = id `0x38` `gameover.mrp`" in b15)
for rec in ("ov41-efx-children-fable/README.md", "ov42-arena-residue-fable/README.md", "sd166-arena-7-0930/README.md",
            "swe2contract-ddres-b15-0930/README.md"):
    tr = subprocess.run(["git", "ls-files", "--error-unmatch", os.path.join(cand, rec)], capture_output=True, cwd=TZA).returncode == 0
    check("P1 cited record tracked: " + rec, tr)

# ---------------------------------------------------------------- Z: the page edit
PG = os.path.join(TZA, "02-Resource-And-Asset-Pipeline", "authored-reference-lifetime-evidence.md")
raw = open(PG, "rb").read()
txt = raw.decode("utf-8")
STRUCK = ("~~**Register: SD-166** still reads OPEN at HEAD. The row has not yet been updated with that answer, and that update\n"
          "     is the register owner's. Until then this note stays PARTIAL on it.~~")
check("Z1 the superseded SD-166 sentence is kept verbatim under a strike", STRUCK in txt)
check("Z1 ... with the batch-18 correction note", "*Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 18)*" in txt)
notes = re.findall(r"\*\(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: [^\n]*?\)\*", txt)
check("Z2 the batch-18 pointer notes", len(notes) == 44, str(len(notes)))
check("Z2 the new Limits subsection", "### Limits items 17–23, brought current 2026-10-01 (SWE2-CONTRACT for OPUS)" in txt
      and all(("\n%d. **" % k) in txt for k in range(17, 24)))
check("Z3 the page stays LF-only", b"\r" not in raw)
check("Z4 no batch-18 note carries a literal '|'", not any("|" in x for x in notes))

print("PASSES %d FAILS %d" % (PASSES, FAILS))
sys.exit(1 if FAILS else 0)
