"""SWE2-AUDIT-SEM: FRONTIER's pass-22 batch 8, the crossing section on the-handbook-screen.md (11a944474), re-read against
the certified image. E-checks: the caller -> callee edges the six paragraphs state, from this review's own capstone scan
(retool.scan: direct call/jmp targets plus rip-relative lea) with Tools/work/graph/edges.tsv as a second source. R-checks:
the helper readings at the instructions. F-checks: findings this review adds (PASS when the finding reproduces).

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-p22-b8-0930/p22b8_sem.py"
"""
import csv
import os
import sys

ROOT = os.getcwd()
DB = os.path.join(ROOT, "Database")
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool  # noqa: E402

R = retool.R
C = retool.scan()
FAILS = []
ED = set()
for r in csv.DictReader(open(os.path.join(DB, "Tools", "work", "graph", "edges.tsv"), encoding="utf-8"), delimiter="\t"):
    ED.add((r["caller"], r["callee"]))


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def h(x):
    return int(x, 16)


def edge(a, b):
    A, B = h(a), h(b)
    if any(f == A for f, _ in C["calls"].get(B, ())):
        return "scan"
    if any(f == A and k == "lea" for f, _, k in C["refs"].get(B, ())):
        return "lea"
    if (a, b) in ED:
        return "edges.tsv"
    return None


def edges(label, pairs):
    miss, src = [], {}
    for a, bs in pairs:
        for b in bs.split():
            e = edge(a, b)
            if not e:
                miss.append("%s->%s" % (a, b))
            else:
                src[e] = src.get(e, 0) + 1
    check("E %s: %d stated edges hold" % (label, sum(len(bs.split()) for _, bs in pairs)), not miss,
          ("missing " + " ".join(miss)) if miss else " ".join("%s %d" % kv for kv in sorted(src.items())))


def s(i):
    return "%s %s" % (i.mnemonic, i.op_str)


def body(a):
    n = retool.sizes().get(h(a)) or 0x200
    return {i.address: s(i) for i in R.md.disasm(R.at(h(a), n), h(a))}


def ncallers(a):
    return len({f for f, _ in C["calls"].get(h(a), ())})


# ---------------- Presentation ----------------
b = body("00202C90")
check("R 00202C90 is the 16-byte copy movups [rdx] -> [rcx]", list(b.values())[:3] == ["movups xmm0, xmmword ptr [rdx]", "movups xmmword ptr [rcx], xmm0", "ret "])
b = body("0024A5A0")
check("R 0024A5A0 compares a name against the 64 records (0x48 stride) of the registry at 0208F580 (flag +0x38 bit 5)",
      b[0x0024A5B0] == "test byte ptr [r9 + 0x38], 0x20" and b[0x0024A5DA] == "add r9, 0x48" and b[0x0024A5DE] == "cmp r10d, 0x40")
b = body("0024F610")
check("R 0024F610 looks up the bucket table 020910A0 by byte [rcx], then walks the chain matching word [rcx+4]",
      b[0x0024F615] == "movzx eax, byte ptr [rcx]" and b[0x0024F628] == "movzx ecx, word ptr [rcx + 4]" and b[0x0024F630] == "cmp word ptr [rax + 4], cx")
check("R 0036DD90 / 0036DDA0 set 0x80 / 0x40 of the dword 022D9470",
      list(body("0036DD90").values())[0].endswith(", 0x80") and list(body("0036DDA0").values())[0].endswith(", 0x40"))
b = body("003B1310")
check("R 003B1310 walks 02EBE5E0..02EBEBE0 and tests tickets through 0032E4D0 / 0032E520 / 0032E590",
      b[0x003B1386] == "call 0x32e4d0" and b[0x003B1392] == "call 0x32e520" and b[0x003B13AF] == "call 0x32e590")
edges("Presentation", [("0026F470", "0024B270"), ("003B02A0", "0024B270"), ("003B2D80", "0024B270"), ("003B3550", "0024B270"),
                       ("003B2220", "0024B3A0"), ("003B38B0", "0024B3A0"), ("0040ACF0", "0036DD90 0036DDA0"), ("0040D890", "0036DD90 0036DDA0"),
                       ("003B1310", "0032E4D0 0032E520 0032E590")])
fx = sorted({"%08X" % t for t, v in C["calls"].items() if any(f == 0x0024B270 for f, _ in v) and 0x003A7000 <= t < 0x003A9000})
check("R 0024B270 calls three 003A7xxx/003A8xxx bodies", len(fx) == 3, " ".join(fx))
panes = {x: [z for z in "003B2AA0 003B2D80 003B2F50".split() if edge(x, z)] for x in "005734C0 00573690 00572E10 00572920".split()}
check("E three of the four handbook effect panes (005734C0, 00573690, 00572920) call 003B2AA0 / 003B2D80 / 003B2F50",
      all(panes[x] == ["003B2AA0", "003B2D80", "003B2F50"] for x in ("005734C0", "00573690", "00572920")), str(panes))
check("F4 the fourth, 00572E10, calls none of the three: it calls 003B29B0 (00572F44) and reaches them only through 005734C0 / 00572920",
      not panes["00572E10"] and edge("00572E10", "003B29B0") and edge("00572E10", "005734C0") and edge("00572E10", "00572920"))
check("R 00202C90 has 24 callers in the render layer; the image-wide caller count for context", ncallers("00202C90") >= 24, "%d callers image-wide" % ncallers("00202C90"))
# ---------------- Resource ----------------
b = body("0032E400")
check("R 0032E400(kind, id): kind 0xFF or a missing table -> the fallback; else dword [022C51F0][kind][id] for id < 0x400",
      b[0x0032E404] == "cmp ecx, 0xff" and b[0x0032E41F] == "cmp rdx, 0x400" and b[0x0032E431] == "call 0x46de70")
ld = {x: [z for z in ("0032E400", "0032E620") if edge(x, z)] for x in "00249210 0024AC30 00259DF0 00379E90 00384420 0039C3F0 0051ED10".split()}
check("E Resource: each named loader calls 0032E400 and/or 0032E620 ('both are called by nine loaders ... and peers')", all(ld.values()), str(ld))
pn = {x: [z for z in "00249210 00249580 0024A680 003933F0 00393460 003934F0".split() if edge(x, z)] for x in "0056F2A0 00572D80 00574E80 00575C30 00576F50".split()}
check("E Resource: each handbook pane calls part of {00249210, 00249580, 0024A680, 003933F0, 00393460, 003934F0}, and together all six",
      all(pn.values()) and {z for v in pn.values() for z in v} == set("00249210 00249580 0024A680 003933F0 00393460 003934F0".split()), str(pn))
edges("Resource: 00249210 calls both back; FieldData_GetVariable0 callers", [("00249210", "0032E400 0032E620"), ("001DA220", "00265270"), ("001DA970", "00265270")])
check("R 0024A680 references the registry at 0208F580", any(f == 0x0024A680 for f, _, _ in C["refs"].get(0x0208F580, ())))
b = body("0032E400")
check("F5 kind 0xFF does NOT take the fallback: 0032E40A je 0032E438 'or eax, -1' returns -1; only a missing table or id >= 0x400 calls 0046DE70",
      b[0x0032E40A] == "je 0x32e438" and b[0x0032E438] == "or eax, 0xffffffff" and b[0x0032E41D] == "je 0x32e431" and b[0x0032E426] == "jge 0x32e431")
# ---------------- Save_Load_Settings ----------------
b = body("00315390")
check("R 00315390 reads the game-state block +0x3868 (through 002536A0)", b[0x0031539A] == "call 0x2536a0" and b[0x0031539F] == "add eax, 0x3868")
b = body("003166F0")
check("R 003166F0 reads the game-state block +0x384C", b[0x00316700] == "call 0x2536a0" and b[0x00316705] == "lea edx, [rax + 0x384c]")
edges("Save_Load_Settings", [("00583D60", "00315390 003166F0 0032A8A0"), ("0032A8A0", "002EF2B0")])
check("F1 00315390 forms +0x3868 with a 32-bit add on the returned pointer (add eax, 0x3868 truncates rax) - a note, not a defect of the section",
      body("00315390")[0x0031539F] == "add eax, 0x3868")
# ---------------- Input ----------------
edges("Input", [("00368360", "001E0A10 001E0E30 001E0E50"), ("00253C70", "00265270 0032A8A0"), ("00291D90", "0024A680"), ("00291C80", "0032E620")])
inp = {x: [z for z in "00198790 001986D0 00197700".split() if edge(x, z)] for x in "001E0A10 001E0E30 001E0E50".split()}
check("E Input: the three bodies call 00198790 / 001986D0 / 00197700 between them", {z for v in inp.values() for z in v} == {"00198790", "001986D0", "00197700"}, str(inp))
# ---------------- SaveLoad ----------------
edges("SaveLoad", [("00582790", "00249580 00249210 00249410 003933F0 00393460"), ("00280140", "00245020 002EFD20")])
b = body("002EFD20")
check("F2 002EFD20 clamps to 0..6 and returns the BYTE at 022BDD64 + idx*0x30 (idx*3, *2, then [rax + rcx*8]): a 0x30-byte stride, not 6",
      b[0x002EFD2F] == "cmovg ecx, eax" and b[0x002EFD35] == "lea rcx, [rax + rax*2]" and b[0x002EFD39] == "add rcx, rcx"
      and b[0x002EFD43] == "movzx eax, byte ptr [rax + rcx*8]")
b = body("00249580")
check("F3 00249580 (the SaveLoad paragraph's 'claims a slot') claims a batch record, 12 x 0x20 at 02090790, owner at +8; 00249410 closes that batch",
      b[0x0024959B] == "cmp edx, 0xc" and b[0x002495B7] == "mov qword ptr [rax + 8], rcx"
      and body("00249410")[0x00249425] == "or dword ptr [rcx], 2")
# ---------------- CombatAI ----------------
edges("CombatAI", [("00301AD0", "00309EC0")])

print("FAILS %d" % len(FAILS) + ("  " + ", ".join(FAILS) if FAILS else ""))
