"""sd166_check.py - SD-166: nothing selects arena 7 for an allocation after boot (OPUS, 2026-09-30).
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py and regval.py; S1 re-runs the shipped-script
census (script_verb_census.py) and keeps its output as sd166-verbs.out.
"""
import os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
import regval as V  # noqa: E402
import pefile  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def callers(a):
    return sorted(c["calls"].get(a, ()))


def rip(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return a + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)


ACTIVE = 0x022D89BC
# P0 - the resolver's own controls (two-path merge, cmp/jne and test/jne pins, cmov)
check("P0", V.self_test(), "regval.py self-test")
# A1 - every allocation reads its arena from the active dword: the arena allocator 0036BFE0 (arena in ecx; spins unless
#      that heap's mask bit is set) has four callers, and each loads ecx from 022D89BC
sites = callers(0x0036BFE0)
loads = {0x0036A100: 0x0036A12E, 0x0036A1A0: 0x0036A1D8, 0x0036B160: 0x0036B16F, 0x0036D050: 0x0036CAE6}
ok = [f for f, s in sites] == sorted(loads) and txt(0x0036BFF8) == "bt eax, ecx" and txt(0x0036C000) == "jmp 0x36c000"
for f, s in sites:
    v = V.value_at(f, s, "rcx", 1)
    ok &= v == {("M", "%08X dword ptr %s" % (loads[f], txt(loads[f]).split(", ", 1)[1].replace("dword ptr ", "")))} or \
        (len(v) == 1 and next(iter(v))[0] == "M" and next(iter(v))[1].startswith("%08X" % loads[f]))
    ok &= rip(loads[f]) == ACTIVE
check("A1", ok, "0036BFE0's four callers (0036A100, 0036A1A0, 0036B160, 0036D050) pass [022D89BC] as the arena")
# A2 - the push maps its argument through the byte table 022D89A8 into 022D89BC; the table is filled with the identity
#      (table[i] = i, i < 15) by 00369D30 and 0036A280, and 0036C272 is the only instruction in executable code that
#      indexes it
pe = pefile.PE(T.R.b.EXE, fast_load=True)
pat, hits = struct.pack("<I", 0x021B89A8), []
for sec in pe.sections:
    if sec.Characteristics & 0x20000000:
        d, va = sec.get_data(), pe.OPTIONAL_HEADER.ImageBase + sec.VirtualAddress
        i = d.find(pat)
        while i >= 0:
            hits.append(va + i)
            i = d.find(pat, i + 1)
check("A2", txt(0x0036C272) == "movzx eax, byte ptr [rax + rbx + 0x21b89a8]" and rip(0x0036C27F) == ACTIVE
      and rip(0x00369D79) == 0x022D89A8 and txt(0x00369DA0) == "mov byte ptr [rcx], al" and txt(0x00369DA8) == "cmp eax, 0xf"
      and rip(0x0036A282) == 0x022D89A8 and txt(0x0036A290) == "mov byte ptr [rcx], al" and txt(0x0036A298) == "cmp eax, 0xf"
      and hits == [0x0036C276],
      "the push's map 022D89A8 is the identity; its one indexed read is 0036C272")
# A3 - the 135 push sites: resolved to constants, no site can pass 7; five sites keep a non-constant term (A4)
agg, rest = {}, {}
for f, s in callers(0x0036C1D0):
    v = V.value_at(f, s, "rcx", 5)
    for x in v:
        if x[0] == "C":
            agg[x[1]] = agg.get(x[1], 0) + 1
    o = sorted((x for x in v if x[0] != "C"), key=str)
    if o:
        rest[f] = o
print("      push-site constants (value: sites): %s" % dict(sorted(agg.items())))
check("A3", len(callers(0x0036C1D0)) == 135 and 7 not in agg
      and sorted(rest) == [0x00249210, 0x00384420, 0x003E9AA0, 0x0050D8F0, 0x0050DAD0],
      "135 push sites: no constant 7; non-constant terms at 00249210, 00384420, 003E9AA0, 0050D8F0, 0050DAD0")
# A4 - the five non-constant terms, closed one by one:
#   00384420: the return of 008478A0, which is `mov eax, 3; ret`
#   00249210: the arena is a dword its callers read - the table 00D23658 walked twice by 003934F0 ({2,1}, {2,2}; count 2 at
#             00574F5C), and stack structs built with +0 = 2 by 005632C0 (00563325) and the three map-screen handlers
#             (002B7CEF, 002BB0F7, 003CB5CB), which 003C1F00 only reads
#   003E9AA0: setexpandvoicememory (0x395, handler 0034D080): the second pop -> ecx; a negative value selects 6 (cmovns)
#   0050D8F0 / 0050DAD0: debug_tkmalloc (0x2003, 0050DA30) and debug_tkmallochandle (0x2008, 0050DBD0): a script integer
t = 0x00574F6B + 0x7AE6ED
recs = struct.unpack("<4I", R.at(t, 16))
r14_writes = [i for i in R.md.disasm(R.at(0x003C1F00, SZ[0x003C1F00]), 0x003C1F00)
              if i.op_str.startswith(("byte ptr [r14", "word ptr [r14", "dword ptr [r14", "qword ptr [r14"))]
check("A4", txt(0x008478A0) == "mov eax, 3" and txt(0x008478A5) == "ret"
      and rip(0x00574F64) == 0x00D23658 and recs == (2, 1, 2, 2) and txt(0x00574F5C) == "mov dword ptr [rsp + 0x20], 2"
      and txt(0x0039352E) == "mov r9d, dword ptr [rbx]" and txt(0x0039355D) == "add rbx, 8"
      and txt(0x00563325) == "mov dword ptr [rsp + 0x20], 2" and txt(0x00563315) == "lea r8, [rsp + 0x20]"
      and txt(0x002B7CEF) == "mov dword ptr [rbp - 0x70], 2" and txt(0x002BB0F7) == "mov dword ptr [rbp - 0x50], 2"
      and txt(0x003CB5CB) == "mov dword ptr [rsp + 0x20], 2" and txt(0x003C2193) == "mov r8, rdx" and not r14_writes
      and txt(0x0034D0A1) == "mov ecx, eax" and txt(0x0034D0AD) == "jmp 0x3e9aa0"
      and txt(0x003E9AB3) == "mov ecx, 6" and txt(0x003E9ABF) == "cmovns ecx, ebx"
      and [f for f, s in callers(0x0050D8F0)] == [0x0050DA30] and [f for f, s in callers(0x0050DAD0)] == [0x0050DBD0]
      and txt(0x00267E14) == "mov eax, dword ptr [rcx]" and txt(0x00267E1F) == "mov dword ptr [rcx], eax",
      "the five: 3; 2 (table and structs); the script's value or 6; a script integer (two debug verbs)")
# S1 - the shipped scripts: debug_tkmalloc and debug_tkmallochandle are never called; setexpandvoicememory is called 18
#      times (byu_z9900 and rrp_z9900, nine languages), its arena argument always PUSHII 65535, and PUSHII sign-extends
#      its 16-bit operand (the interpreter's handler for opcode 0x4F is 0026186D movsx edx, bx), so the arena is -1 -> 6
out = subprocess.run([sys.executable, "-B", os.path.join(KIT, "script_verb_census.py"), "--verbs", "0x2003,0x2008,0x395",
                      "--out", os.path.join(HERE, "sd166-verbs.tsv")], capture_output=True, text=True).stdout
open(os.path.join(HERE, "sd166-verbs.out"), "w", encoding="utf-8", newline="\n").write(out)
rows = [l.split("\t") for l in open(os.path.join(HERE, "sd166-verbs.tsv"), encoding="utf-8").read().splitlines()[1:]]
h4f = 0x00120000 + struct.unpack("<I", R.at(0x00261DF8 + 4 * 0x4F, 4))[0]
check("S1", "matching calls: 18" in out and len(rows) == 18 and all(r[3] == "0x395" for r in rows)
      and all(r[7].split(";")[0] == "PUSHII:65535" for r in rows)
      and sorted(set(r[0].split("/")[-1] for r in rows)) == ["byu_z9900.ebp", "rrp_z9900.ebp"]
      and h4f == 0x0026186D and txt(0x0026186D) == "movsx edx, bx",
      "no shipped call of the two debug verbs; setexpandvoicememory x18, arena PUSHII 0xFFFF = -1 -> 6")
# W1 - the other writers of 022D89BC: the first heap init (00369D30, only while the heap mask is 0: the boot initialiser
#      0022A0B0 inits 2, 3, 4, 5, 6 and then 7 in straight-line calls, so 7 is never the first), the pop (restores a
#      pushed record), and four error stores (00369860 x2, 0036CB00 x2) that each end in an exit import and int3
w = sorted(set(f for f, s, k in c["refs"][ACTIVE] if k == "W"))
boot = [s for f, s in callers(0x00369D30) if f == 0x0022A0B0]
between = [i for i in R.md.disasm(R.at(0x0022A2AE, 0x0022A33E - 0x0022A2AE), 0x0022A2AE) if i.mnemonic.startswith("j")]
term = all(txt(a) == "int3" for a in (0x00369A7F, 0x00369ABD, 0x0036CB75, 0x0036CB9F))
check("W1", w == [0x00369860, 0x00369D30, 0x0036C140, 0x0036C1F0, 0x0036CB00] and txt(0x00369D71) == "jne 0x369dcc"
      and [sorted(V.value_at(0x0022A0B0, s, "rcx", 1))[0][1] for s in boot] == [2, 3, 4, 5, 6, 7, 8, 9, 11]
      and not between and term,
      "writers: first init (boot inits 2 first), push, pop, and four terminal error stores")
print("FAILS %d" % fails)
