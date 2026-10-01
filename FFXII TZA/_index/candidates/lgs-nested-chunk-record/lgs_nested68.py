"""lgs_nested68.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

LegacyPs2GsTextureContext +0x40..+0x10F is TWO 0x68-byte nested chunk records, which the store did not declare: it held
26 parent rows over those bytes, six of them 'mixed ... overlapping widths ... NOT resolved', each element's interior
recorded twice. And the ctor-seeded census's unbounded loop invented accesses past the array, two of which were the only
evidence for TYPE RESOLVED rows.

  L1 the extent: 002F6AB0 clears the elements in a loop that runs exactly twice - lea rbx, [rcx+0x40] / mov edi, 2 /
     call 00231F50 / add rbx, 0x68 / sub rdi, 1 / jne - and binds them with 00232380(+0x40) and 00232380(+0xA8)
     (002F6DBA, 002F6DC8). Those are the ONLY calls or jumps to 00231F50 and 00232380 in .text.
  L2 the layout, from the binder 00232380's six-arm jump table (base 00120000 + 0x112470): tag 0 -> +0x00 and the
     computed dwords +0x30..+0x40; tag 1 -> +0x20; tag 2 -> +0x28; tag 3 -> +0x10; tag 4 -> +0x18 (chunk + 0x10) and the
     count +0x44; tag 5 -> +0x08; after the loop four qword zeroes at +0x48 / +0x50 / +0x58 / +0x60 (0x48 + 0x20 = 0x68)
  L3 the arithmetic makes +0x30..+0x3C signed: imul products at +0x30 / +0x34, then cdq / sub / sar 1 / sub for +0x38 /
     +0x3C; the reader 00233050 / 00233059 loads +0x38 / +0x3C with movd and converts with cvtdq2ps (int32 -> float)
  L4 the clear 00231F50 zeroes +0x00..+0x47 with nine qword stores; the ones at +0x30 / +0x38 / +0x40 span two dword
     cells each, so those 8-byte widths are store merges
  P  PHANTOM: the ctor-seeded census reports 00231F50's stores at bases +0x110, +0x178, +0x1E0 - a third, fourth and fifth
     element the two-iteration loop (L1) never produces. The store's rows field0118 (00231F55) and field0148 (00231F69)
     rest on nothing else, and mixed0110 cites 00231F52 beside the ctor's own store 002F6AEF
  S  REGRESSION: LegacyPs2GsNestedChunkRecord68 is declared 0x68; the parent carries one +0x40 row of 208 bytes typed
     LegacyPs2GsNestedChunkRecord68[2] and nothing inside it; field0118 / field0148 are no longer TYPE RESOLVED and
     mixed0110 strikes 00231F52 (FAILS before the patch)
Usage: python lgs_nested68.py [--patch]
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(DB, ".."))
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a): x = next(cs.disasm(d[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
TYPES = os.path.join(DB, "_types", "types.tsv"); FIELDS = os.path.join(DB, "_types", "fields.tsv")
REC = "_index/candidates/lgs-nested-chunk-record/lgs_nested68.py"
CHILD = "LegacyPs2GsNestedChunkRecord68"; PARENT = "LegacyPs2GsTextureContext"

# ---- the child's rows: (offset, size, name, ctype, meaning, readiness, confidence, evidence) ----
CH = [
    (0x00, 8, "chunk00", "void*", "TAG 0: the address of the tag-0 chunk (header base + (entry & 0xFFFFFF) * 16); its dwords "
     "+0x00 / +0x04 / +0x08 / +0x0C / +0x10 / +0x14 / +0x18 feed +0x30..+0x40. Null-tested by the context's builder "
     "(002F70AF, element 0) and read at 00233061", "TYPE RESOLVED", "PROVEN", "00232380 arm 0 at 002323DB `mov qword ptr [r9], r8`"),
    (0x08, 8, "tag5Ptr08", "void*", "TAG 5: the address of the tag-5 chunk. Read at 0022F0A2, 00231CAA, 00231D15, 00231D82, "
     "002325A8, 002325C2 (element 0). What the chunk holds is NOT claimed", "TYPE RESOLVED", "PROVEN", "00232380 arm 5 at 00232440"),
    (0x10, 8, "tag3Ptr10", "void*", "TAG 3: the address of the tag-3 chunk. Read at 0022F0AF, 00231B62, 00231C6E, 0023257C "
     "(element 0). What the chunk holds is NOT claimed", "TYPE RESOLVED", "PROVEN", "00232380 arm 3 at 00232429"),
    (0x18, 8, "tag4Payload18", "void*", "TAG 4: the tag-4 chunk's address + 0x10 - its payload past a 16-byte header whose "
     "first dword is stored at +0x44. No reader in the census", "TYPE RESOLVED", "PROVEN",
     "00232380 arm 4 at 00232432 (`add r8, 0x10`) / 00232436"),
    (0x20, 8, "tag1Ptr20", "void*", "TAG 1: the address of the tag-1 chunk. Read at 00231ADF (element 0)", "TYPE RESOLVED",
     "PROVEN", "00232380 arm 1 at 0023241D"),
    (0x28, 8, "tag2Ptr28", "void*", "TAG 2: the address of the tag-2 chunk. Read at 00231B50 (element 0)", "TYPE RESOLVED",
     "PROVEN", "00232380 arm 2 at 00232423"),
    (0x30, 4, "product30", "int32", "tag-0 chunk dword +0x10 times dword +0x08 (imul). No reader in the census",
     "TYPE RESOLVED", "PROVEN", "002323DE / 002323E2 imul, stored at 002323E7"),
    (0x34, 4, "product34", "int32", "tag-0 chunk dword +0x14 times dword +0x0C (imul). No reader in the census",
     "TYPE RESOLVED", "PROVEN", "002323EC / 002323F2 imul, stored at 002323F9"),
    (0x38, 4, "halfMinus38", "int32", "+0x30 halved (cdq / sub / sar 1, signed) minus the tag-0 chunk's dword +0x00. Read by "
     "00233050 with movd and converted by cvtdq2ps as int32", "TYPE RESOLVED", "PROVEN", "stored at 00232400; reader 00233050 / 00233064"),
    (0x3C, 4, "halfMinus3C", "int32", "+0x34 halved (signed) minus the tag-0 chunk's dword +0x04. Read by 00233059 with movd "
     "and converted by cvtdq2ps as int32", "TYPE RESOLVED", "PROVEN", "stored at 0023240F; reader 00233059 / 00233067"),
    (0x40, 4, "copied40", "u8[4]", "a dword copied from the tag-0 chunk's +0x18 (00232413 / 00232417) and read as a WORD by "
     "00231AC5 (`movzx r9d, word ptr [rsi+0x40]`). One 16-bit field carried by a dword copy, or a dword read in part: NOT "
     "resolved", "DISCOVERED", "PROVEN", "00232417 dword store; 00231AC5 word read"),
    (0x44, 4, "tag4Count44", "uint32", "the tag-4 chunk's first dword (0023242F `mov eax, [r8]`), stored beside its payload "
     "pointer +0x18. Moved only by plain moves: the type is the width, not a claim of integer representation. No reader in "
     "the census", "TYPE RESOLVED", "PROVEN", "00232380 arm 4 at 0023243A"),
] + [(o, 8, "zeroedAtBind%02X" % o, "u8[8]", "written only as a qword ZERO at the end of every bind (%s); never read in the "
      "census. One 8-byte field or two 4-byte cells NOT resolved - a qword zero store is also how this image initialises "
      "dword pairs" % s, "DISCOVERED", "PROVEN", "00232380 tail at %s" % s)
     for o, s in ((0x48, "0023245E"), (0x50, "00232462"), (0x58, "00232466"), (0x60, "0023246A"))]

L1 = (at(0x2F6AFB) == ("lea", "rbx, [rcx + 0x40]") and at(0x2F6AEA) == ("mov", "edi, 2") and at(0x2F6B07) == ("call", "0x231f50")
      and at(0x2F6B0C) == ("add", "rbx, 0x68") and at(0x2F6B10) == ("sub", "rdi, 1") and at(0x2F6B14) == ("jne", "0x2f6b04")
      and at(0x2F6DBA) == ("lea", "rcx, [rsi + 0x40]") and at(0x2F6DBE) == ("call", "0x232380")
      and at(0x2F6DC8) == ("lea", "rcx, [rsi + 0xa8]") and at(0x2F6DD2) == ("call", "0x232380"))
text = next(s for s in SECS if s[1] == 0x1000); vs, va, rs, ro = text
callers = []
for i in range(ro, ro + rs - 5):
    if d[i] in (0xE8, 0xE9):
        v = B + va + i - ro; t = v + 5 + struct.unpack_from("<i", d, i + 1)[0]
        if t in (0x231F50, 0x232380):
            try:
                x = next(cs.disasm(d[i:i + 5], v))
                if x.mnemonic in ("call", "jmp"): callers.append(("%X" % v, "%X" % t))
            except StopIteration: pass
check("L1", L1 and sorted(callers) == [("2F6B07", "231F50"), ("2F6DBE", "232380"), ("2F6DD2", "232380")],
      "two elements at +0x40 / +0xA8, stride 0x68; the only callers %s" % sorted(callers))
tb = 0x2323A9 - 0x1123A9
arms = [tb + struct.unpack_from("<I", d, off(tb + 0x112470 + 4 * k))[0] for k in range(6)]
L2 = (arms == [0x2323DB, 0x23241D, 0x232423, 0x232429, 0x23242F, 0x232440]
      and at(0x2323DB) == ("mov", "qword ptr [r9], r8") and at(0x23241D) == ("mov", "qword ptr [r9 + 0x20], r8")
      and at(0x232423) == ("mov", "qword ptr [r9 + 0x28], r8") and at(0x232429) == ("mov", "qword ptr [r9 + 0x10], r8")
      and at(0x232432) == ("add", "r8, 0x10") and at(0x232436) == ("mov", "qword ptr [r9 + 0x18], r8")
      and at(0x23243A) == ("mov", "dword ptr [r9 + 0x44], eax") and at(0x232440) == ("mov", "qword ptr [r9 + 8], r8")
      and [at(a) for a in (0x23245E, 0x232462, 0x232466, 0x23246A)] ==
          [("mov", "qword ptr [r9 + 0x%x], rdi" % o) for o in (0x48, 0x50, 0x58, 0x60)] and at(0x232386) == ("xor", "edi, edi"))
check("L2", L2, "binder arms (tag -> offset) 0:+0x00 1:+0x20 2:+0x28 3:+0x10 4:+0x18/+0x44 5:+0x08; tail zeroes +0x48..+0x60")
L3 = (at(0x2323E2) == ("imul", "eax, dword ptr [r8 + 8]") and at(0x2323E7) == ("mov", "dword ptr [r9 + 0x30], eax")
      and at(0x2323F2) == ("imul", "ecx, dword ptr [r8 + 0xc]") and at(0x2323F9) == ("mov", "dword ptr [r9 + 0x34], ecx")
      and at(0x2323F7) == ("sar", "eax, 1") and at(0x232400) == ("mov", "dword ptr [r9 + 0x38], eax")
      and at(0x23240F) == ("mov", "dword ptr [r9 + 0x3c], eax") and at(0x232417) == ("mov", "dword ptr [r9 + 0x40], eax")
      and at(0x233050) == ("movd", "xmm1, dword ptr [rcx + 0x38]") and at(0x233064) == ("cvtdq2ps", "xmm1, xmm1")
      and at(0x233059) == ("movd", "xmm0, dword ptr [rcx + 0x3c]") and at(0x233067) == ("cvtdq2ps", "xmm0, xmm0")
      and at(0x231AC5) == ("movzx", "r9d, word ptr [rsi + 0x40]"))
check("L3", L3, "+0x30/+0x34 imul products, +0x38/+0x3C signed halves read as int32 (cvtdq2ps); +0x40 read as a word")
clr = [at(0x231F52 + k) for k in (0, 3, 7, 0xB, 0xF, 0x13, 0x17, 0x1B, 0x1F)]
L4 = at(0x231F50) == ("xor", "eax, eax") and [c[1] for c in clr] == [
    "qword ptr [rcx], rax", "qword ptr [rcx + 8], rax", "qword ptr [rcx + 0x10], rax", "qword ptr [rcx + 0x20], rax",
    "qword ptr [rcx + 0x28], rax", "qword ptr [rcx + 0x30], rax", "qword ptr [rcx + 0x38], rax", "qword ptr [rcx + 0x40], rax",
    "qword ptr [rcx + 0x18], rax"] and at(0x231F75) == ("ret", "")
check("L4", L4, "00231F50 zeroes +0x00..+0x47 with nine qword stores")
check("C", len(CH) == 16 and sum(c[1] for c in CH) == 0x68 and all(CH[i][0] + CH[i][1] == CH[i + 1][0] for i in range(15)),
      "the child's rows tile 0x68 bytes exactly (%d rows)" % len(CH))

tl = open(TYPES, "rb").read().decode("utf-8").splitlines(keepends=True)
fl = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
pidx = [i for i, l in enumerate(fl) if cells(l)[0] == PARENT]
inside = [i for i in pidx if 0x40 <= int(cells(fl[i])[1], 16) < 0x110]
declared = any(cells(l)[0] == CHILD for l in tl)
row = lambda o: next((cells(fl[i]) for i in pidx if int(cells(fl[i])[1], 16) == o), None)

if "--patch" in sys.argv:
    if declared: print("already"); sys.exit(0)
    assert inside == list(range(inside[0], inside[-1] + 1)) and len(inside) == 26, (len(inside))
    old = [cells(fl[i]) for i in inside]
    w = len(old[0]); eol = fl[inside[0]][len(fl[inside[0]].rstrip("\r\n")):]
    def frow(c): return "\t".join(list(c) + [""] * (w - len(c))) + eol
    q40, qA8 = row(0x40), row(0xA8)
    absorbed = "; ".join("%s %s %s %s" % (c[1], c[2], c[3], c[4]) for c in old)
    region = [PARENT, "0x0040", "208", "chunkRecords040", CHILD + "[2]",
              "TWO NESTED CHUNK RECORDS of 0x68 bytes, the first bound from map-ctrl-pack tag 31 and the second from tag 17 "
              "(the map-ctrl-pack page, section 3.5). One region row under FABLE's rule 0 (one description per byte; the "
              "byte belongs to the innermost declared type): the element's fields are " + CHILD + "'s rows.",
              "TYPE RESOLVED", "PROVEN",
              "DECLARED 2026-09-28 (OPUS, " + REC + " L1 L2): 002F6AB0 clears exactly two elements (lea rbx,[rcx+0x40] / "
              "mov edi,2 / add rbx,0x68 / sub rdi,1 / jne) and binds +0x40 and +0xA8 through 00232380; those are the only "
              "callers. ABSORBED ROWS (name and old type verbatim; each element's interior was recorded twice, and the "
              "'mixed' spans were the clear's merged qword stores over dword cells): " + absorbed +
              " || MIGRATED to " + CHILD + " +0x00 with their evidence verbatim: qword0040 and qword00A8"]
    nf = list(fl)
    nf[inside[0]:inside[-1] + 1] = [frow(region)]
    # phantom-only and phantom-citing rows past the array
    for i, l in enumerate(nf):
        c = cells(l)
        if c[0] != PARENT: continue
        e = l[len(l.rstrip("\r\n")):]
        ph = ("the census reached it only through 00231F50 at a base the two-iteration clear loop 002F6AB0 never produces "
              "(+0x110 = a third element); " + REC + " P")
        if c[1] in ("0x0118", "0x0148") and c[6] == "TYPE RESOLVED":
            c[3] = "unobservedSpan" + c[1][2:]; was = c[4]; c[4] = "u8[8]"; c[6] = "DISCOVERED"; c[7] = "UNKNOWN"
            c[5] = "~~" + c[5] + "~~ NO REAL ACCESS: " + ph
            c[8] = c[8] + " || CORRECTED 2026-09-28 (OPUS, " + REC + " P): the only cited site is a census phantom. WAS " + was
            nf[i] = "\t".join(c) + e
        elif c[1] == "0x0110" and "~~r0 w2 at 00231F52, 002F6AEF~~" not in c[5]:
            c[5] = c[5].replace("r0 w2 at 00231F52, 002F6AEF", "~~r0 w2 at 00231F52, 002F6AEF~~ r0 w1 at 002F6AEF (the ctor's "
                                "`mov qword ptr [rcx+0x110], r14`, which also covers dword0114); 00231F52 is a phantom - " + ph)
            nf[i] = "\t".join(c) + e
    # the child's rows, after the parent's block
    last = max(i for i, l in enumerate(nf) if cells(l)[0] == PARENT)
    mig = {0x00: " || MIGRATED from %s +0x40 (qword0040) and +0xA8 (qword00A8), evidence verbatim: %s | %s" % (PARENT, q40[8], qA8[8])}
    crow = [frow([CHILD, "0x%02X" % o, str(s), nm, ct, mean, rd, cf,
                  "DECLARED 2026-09-28 (OPUS, " + REC + "): " + ev + mig.get(o, "")]) for o, s, nm, ct, mean, rd, cf, ev in CH]
    nf[last + 1:last + 1] = crow
    tw = len(cells(tl[0])); teol = tl[0][len(tl[0].rstrip("\r\n")):]
    ti = next(i for i, l in enumerate(tl) if cells(l)[0] == PARENT)
    trow = [CHILD, "0x68", "17-Presentation-Rendering",
            "TWO instances, an ARRAY at LegacyPs2GsTextureContext +0x40 with stride 0x68 (+0x40 and +0xA8); nothing else calls "
            "its clear 00231F50 or its binder 00232380",
            "INTERIOR - none - the storage is LegacyPs2GsTextureContext's; 002F6AB0 clears both elements in place",
            "00231F50 clears +0x00..+0x47 (called twice from 002F6B07); 00232380(element, chunk index) binds it from map-ctrl-pack "
            "tag 31 (+0x40, 002F6DBE) or tag 17 (+0xA8, 002F6DD2) and zeroes +0x48..+0x67",
            "none - interior to LegacyPs2GsTextureContext; the chunk pointers borrow the pack's storage",
            "TYPE RESOLVED", "PROVEN", "L1",
            "DECLARED 2026-09-28 (OPUS, " + REC + " L1-L4, C): the extent is the clear loop's stride and count; the fields tile "
            "0x68 exactly from the binder's six-arm jump table",
            "03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md",
            "EMBED LegacyPs2GsTextureContext +0x40 stride=0x68 count=2"]
    tl[ti + 1:ti + 1] = ["\t".join(trow + [""] * (tw - len(trow))) + teol]
    open(FIELDS, "wb").write("".join(nf).encode("utf-8")); open(TYPES, "wb").write("".join(tl).encode("utf-8"))
    print("declared %s (%d rows); parent: 26 rows -> 1 region row; 2 phantom rows corrected; mixed0110 qualified" % (CHILD, len(CH)))
    sys.exit(0)

r110, r118, r148 = row(0x110), row(0x118), row(0x148)
check("P", r110 is not None and "00231F52" in r110[5], "the store cites 00231F52 at +0x110 and 00231F55 / 00231F69 at "
      "+0x118 / +0x148: the clear at bases past the two elements L1 bounds")
s = (declared and [int(cells(fl[i])[1], 16) for i in inside] == [0x40]
     and cells(fl[inside[0]])[4] == CHILD + "[2]" and cells(fl[inside[0]])[2] == "208"
     and r118[6] != "TYPE RESOLVED" and r148[6] != "TYPE RESOLVED" and "~~r0 w2 at 00231F52, 002F6AEF~~" in r110[5])
check("S", s, "child declared; the parent's +0x40 region row alone; phantom rows corrected")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
