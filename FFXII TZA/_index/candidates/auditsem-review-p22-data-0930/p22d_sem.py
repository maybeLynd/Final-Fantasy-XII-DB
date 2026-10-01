"""SWE2-AUDIT-SEM: FRONTIER's pass-22 crossing sections on SWE2-DATA's twelve pages (312d1428c, 20da4dbde, 51b93d0b6),
re-read against the certified image. E-checks: every caller -> callee edge the paragraphs state, from this review's own
capstone scan of the v4 extents (retool.scan: direct call/jmp targets plus rip-relative lea), with Tools/work/graph/edges.tsv
as a second source; an edge holds if either has it. R-checks: the helper readings the paragraphs give, at the
instructions. F-checks: findings this review adds (PASS when the finding reproduces).

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-p22-data-0930/p22d_sem.py"
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
    miss = []
    src = {}
    for a, bs in pairs:
        for b in bs.split():
            e = edge(a, b)
            if not e:
                miss.append("%s->%s" % (a, b))
            else:
                src[e] = src.get(e, 0) + 1
    check("E %s: %d stated edges hold" % (label, sum(len(bs.split()) for _, bs in pairs)), not miss,
          ("missing " + " ".join(miss)) if miss else " ".join("%s %d" % kv for kv in sorted(src.items())))


def ins(a, n=40):
    return list(R.md.disasm(R.at(h(a), n), h(a)))


def s(i):
    return "%s %s" % (i.mnemonic, i.op_str)


def body(a):
    n = retool.sizes().get(h(a)) or 0x200
    return {i.address: s(i) for i in R.md.disasm(R.at(h(a), n), h(a))}


# ---------------- 312d1428c (batch D1) ----------------
edges("amap: 00309EC0's callers named", [(x, "00309EC0") for x in "00301AD0 00317BC0 00317C80 00317930 00315E90 00576A50".split()])
edges("himg: pool claim / batch close / label helper", [
    ("003C9950", "00249210"), ("00561390", "00249210"), ("00562F90", "00249210"),
    ("002B7B80", "00249410"), ("002BAF80", "00249410"), ("00582790", "00249210 00249410"),
    ("00291D90", "0024A440"), ("0024A440", "0024A4E0 0024A1D0")])
edges("lst", [("005771F0", "00576F50"), ("00579420", "0037E5B0"), ("0037E8D0", "0037EFC0"), ("00582860", "00582790")])
edges("mg", [("00561300", "00561390 00244F50"), ("00558FB0", "00561300"), ("00560910", "00561300"),
             ("00561390", "00291D70 00291D80 00558F20 0055A810 0055C690"), ("00550540", "00562F90"), ("00552250", "00563110"),
             ("00558FB0", "002493D0"), ("00561390", "002493D0"), ("00562F90", "002493D0"), ("002493D0", "00249210 0024A4E0")])
edges("wmap", [("0032FCA0", "0032E620 00330310"), ("00330310", "0032E620"), ("003B2310", "0032E620"), ("003B53C0", "0032E620"),
               ("00291C80", "0032E620"), ("002EF300", "0032E620"), ("0050DFE0", "0032E620"),
               ("003B25D0", "003B2310"), ("004269A0", "003B53C0")])
edges("dat-and-bin", [("0018D850", "0018D160 001946E0 0061D9C0 0019CB20"), ("001B4D70", "001FC060 001FDCC0 001FE020 001FE080")])
# ---------------- 20da4dbde (batch D2) ----------------
edges("binmenu: rebase callers and callee", [(x, "003845F0") for x in "00236C30 0023A160 00238640 003847B0 00238880 00237FC0".split()]
      + [("003845F0", "003846F0 0020E620")])
edges("cl2", [("001D0390", "001CD0E0"), ("001D5260", "001CD0E0"), ("001CD0E0", "001DCD30 002DEBA0 003166F0 00265270 00314910"),
              ("00180E70", "0017F3B0"), ("00181000", "0017F3B0"), ("0017F3B0", "0061E200"), ("003DD4C0", "003DDA70"),
              ("003DCD00", "003DC8D0"), ("003EADE0", "002DF660"), ("0022A0B0", "002DF9A0"), ("003C63A0", "0024A480"),
              ("0024A480", "0024A1D0"), ("00266D10", "003A13F0"), ("00582790", "003933F0 00393460")])
edges("cmap", [(x, "00265270") for x in "001EDCD0 003145E0 003EAA70 003BD950 00377970 001ED240 00253C70 001CD0E0 001EC760 003154B0 003161A0".split()]
      + [(x, "0032A8A0") for x in "003BD950 00253C70 00281AE0 0029C530 00583D60 0034E0B0".split()]
      + [("0032A8A0", "00377970 002EF2B0"), ("003C1070", "003148F0"), ("003C0380", "00264F90"), ("00576A50", "003779F0"),
         ("00315E90", "003160C0"), ("003160C0", "003779F0"), ("003C5E50", "003779F0"), ("003BE950", "003C0380")])
# ---------------- 51b93d0b6 (batch D3) ----------------
edges("as7/btm/mrp request path", [("0032FC30", "0032FCA0"), ("0032FCA0", "0032E400 0032E620"), ("00330310", "0032E620"),
                                   ("003306E0", "002561C0 002566E0 0037DC30"), ("00291C80", "0024AB90 0032E620"),
                                   ("0050DF70", "00267E10 0026B4E0 0032E400"), ("0050DFE0", "00267E10 0032E620")])
check("F3 only 0050DF70 writes its result through 0026B4E0 (tail jump 0050DFB6); 0050DFE0 queues through 0032E620 and has no 0026B4E0 edge",
      edge("0050DF70", "0026B4E0") and not edge("0050DFE0", "0026B4E0"))
edges("as7 party-row path", [("0023A570", "0023AC80"), ("00237DF0", "0023AC80"),
                             ("0023AC80", "00326030 00327CB0 00327DE0 0031A630 00323910 0030C470"),
                             ("00329220", "00236850 00236820 00263C20 00263E30 003588B0 003589B0 00313F60 003879C0 00387090 00324020 002F8F20 00263750 003590D0"),
                             ("00235AF0", "00322C50 002EF640"), ("00283270", "00327BE0"),
                             ("00328BD0", "00283270"), ("00316930", "00283270"), ("00582860", "00283270"), ("005844A0", "00283270"),
                             ("00580840", "00583C00"), ("00583C00", "002EF640")])
edges("btm allocation and glyph path", [("00249810", "0036A190"), ("002497E0", "0036A100"),
                                        ("0055B560", "002497E0"), ("0057CF20", "002497E0"), ("00582860", "002497E0"),
                                        ("00247AE0", "00249810"), ("00291C80", "00249810"), ("003649A0", "00364210 003A1DB0 003A2020 003A2090"),
                                        ("0053E0B0", "003649A0"), ("0050D9A0", "002EF300"), ("002EF300", "002EF640")])
# "reached from 001D0190 / 001CCB20": 001D0190 calls 001CD0E0 directly; 001CCB20 reaches it through 001D0390
edges("mrp drawers", [("001D0190", "001CD0E0"), ("001CCB20", "001D0390"), ("002435C0", "0029ED50"), ("00243C00", "0029ED50"),
                      ("00245E60", "002435C0"), ("0029F130", "002A0060"), ("002A0060", "0020E600"), ("00582790", "00249210 003933F0 00393460"),
                      ("00291D90", "0024A440")])

# ---------------- helper readings ----------------
b = body("0032E400")
check("R 0032E400: kind 0xFF -> -1; [022C51F0][kind] for id < 0x400; else 0046DE70; rounded up to 64",
      b[0x0032E404] == "cmp ecx, 0xff" and b[0x0032E41F] == "cmp rdx, 0x400" and b[0x0032E428] == "mov eax, dword ptr [r8 + rdx*4]"
      and b[0x0032E431] == "call 0x46de70" and b[0x0032E448] == "and eax, 0xffffffc0")
b = body("0036A100")
check("R 0036A100: pool index from 022D89BC; 0036BC60 first, 0036BFE0 as the fallback",
      b[0x0036A113].startswith("mov ecx, dword ptr [rip") and b[0x0036A11F] == "call 0x36bc60" and b[0x0036A12C] == "jne 0x36a156"
      and b[0x0036A149] == "call 0x36bfe0")
b = body("003845F0")
check("R 003845F0 relocates +0xC/+0x10/+0x18/+0x1C by the base, re-encodes +0x14 through 0020E620 and walks entries through 003846F0",
      b[0x0038460C] == "add eax, edx" and b[0x0038465D] == "call 0x20e620" and b[0x003846B2] == "call 0x3846f0")
b = body("00249210")
check("R 00249210 takes a free 0x28-byte request slot (of 0x30), sizes it (0032E400), allocates (0036A100/0036A190), queues (0032E620) "
      "with the completion 002495C0, stores its rcx at slot +0 and counts it at [rcx+0x18]",
      b[0x0024924C] == "cmp eax, 0x30" and b[0x00249248] == "add rbx, 0x28" and b[0x00249296] == "call 0x32e400"
      and b[0x002492C5] == "call 0x36a100" and b[0x002492CC] == "call 0x36a190" and b[0x002492F3] == "call 0x32e620"
      and b[0x0024928D] == "mov qword ptr [rbx], rbp" and b[0x002492F8] == "inc word ptr [rbp + 0x18]")
b = body("00249580")
check("F1 00249580 claims the batch record: the first free of 12 x 0x20 at 02090790, owner object stored at +8",
      b[0x0024959B] == "cmp edx, 0xc" and b[0x00249597] == "add rax, 0x20" and b[0x002495B7] == "mov qword ptr [rax + 8], rcx")
b = body("002495C0")
check("F1 each request's completion 002495C0 counts [slot+0]'s +0x1A and, once the batch is closed (bit 1) and +0x1A == +0x18, fires it",
      b[0x002495EA] == "mov rdi, qword ptr [rbx]" and b[0x002495ED] == "inc word ptr [rdi + 0x1a]" and b[0x002495F1] == "test byte ptr [rdi], 2"
      and b[0x002495FA] == "cmp ax, word ptr [rdi + 0x18]")
b = body("00249410")
check("F1 00249410 closes a BATCH (the 00249580 record), not a slot: sets bit 1; only if +0x18 == +0x1A does it fire; the choice "
      "callback +0x10 vs notify is +4 != 0, and the notify is message 0x10 (DL-1: 16 = resource batch complete) to +8, then bit 0 cleared",
      b[0x00249425] == "or dword ptr [rcx], 2" and b[0x00249434] == "cmp word ptr [rcx + 0x1a], ax" and b[0x00249438] == "jne 0x249482"
      and b[0x0024943A] == "cmp dword ptr [rcx + 4], 0" and b[0x00249440] == "call qword ptr [rcx + 0x10]"
      and b[0x0024945D] == "mov dword ptr [rsp + 0x20], 0x10" and b[0x0024947F] == "and dword ptr [rbx], 0xfffffffe")
b = body("0024A440")
check("R 0024A440 creates a label (0024A4E0) and calls the image member callback 0024A1D0",
      b.get(0x0024A456) == "call 0x24a4e0" and b.get(0x0024A464) == "call 0x24a1d0")
b = body("00283270")
check("R 00283270's count at 002833C5 is +0x60 in 0..5 AND record bit 1 clear (002833BD js, 002833BF test [r9], 2) - the page states only '<= 5'",
      b[0x002833BD] == "js 0x2833d8" and b[0x002833BF] == "test byte ptr [r9], 2" and b[0x002833C5] == "cmp ax, 5")
b = body("0023AC80")
check("R 0023AC80 stores the definition selector word at +4 (0023AD8E), low byte = the row (AL-6)", b[0x0023AD8E] == "mov word ptr [rdi + 4], r15w")
b = body("00265270")
check("R 00265270 = flag byte 02098E20 bit 0 ? word [[02098E58]] : 0", b[0x00265270].startswith("test byte ptr [rip") and b[0x00265285] == "movzx eax, word ptr [rax]")
b = body("003779F0")
check("R 003779F0 reads a 12-bit entry of the table at [02ADD100], 0xFFF -> -1", b[0x003779F0].startswith("mov r8, qword ptr [rip") and b[0x00377A26] == "and edx, 0xfff")
check("R 0024AB90 is movsxd + tail jump to 0032E400", [s(i) for i in ins("0024AB90", 8)][:2] == ["movsxd rdx, edx", "jmp 0x32e400"])
b = body("0017F3B0")
check("R 0017F3B0 allocates (0085E730), clears (00861EC0 memset) and ends in 0061E200", b.get(0x0017F3EC) == "call 0x85e730"
      and b.get(0x0017F404) == "call 0x861ec0" and b.get(0x0017F4B1) == "call 0x61e200")

# ---------------- volume: the three identical request-path paragraphs ----------------
import re  # noqa: E402
import subprocess  # noqa: E402

P = "Database/FFXII TZA/02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/"
paras = {}
for pg in ("as7-menu-graphics-containers.md", "btm-exfont-bitmaps.md", "mrp-menu-resource-packages.md"):
    t = subprocess.run(["git", "show", "51b93d0b6:" + P + pg], capture_output=True).stdout.decode("utf-8")
    m = re.search(r"^\*\*ActorEntity, WorldAreaField, World, Presentation, Input, Save_Load_Settings, Script_VM_Native_Bridge — CLIENT \(request path\)\.\*\*.*$", t, re.M)
    paras[pg] = m.group(0) if m else ""
base = paras["btm-exfont-bitmaps.md"]
check("F2 the request-path paragraph is the same text on as7, btm and mrp (as7 adds one sentence); %d words" % len(base.split()),
      base and paras["mrp-menu-resource-packages.md"] == base and paras["as7-menu-graphics-containers.md"].startswith(base.rstrip(".")[:-40]))

print("FAILS %d" % len(FAILS) + ("  " + ", ".join(FAILS) if FAILS else ""))
