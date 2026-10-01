"""virtual_slot.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Corrects OPUS's own d8eb6b94e (2026-09-19).

That commit gave 111 Phyre types the dtor cell 'virtual - descriptor destroy slot +0x58 (<thunk>) calls the object's own vtable
slot 0', and the page and gen_phyre_descriptor_vtables.py describe the form as `mov rax,[rcx] ; call [rax]`. Read per thunk:
  V  every cell's thunk adjusts the pointer (lea rcx, [rdx - 8], null-safe), zeroes edx, and calls through the vtable at a slot
     read from the call's displacement:
        0063FC60  call [rax]          slot 0    87 cells
        0068C4E0  call [rax + 0x18]   slot 3    23 cells (the physics shapes)
        00680910  call [rax + 0x10]   slot 2     1 cell  (PScheduler)
     so 24 cells stated the wrong slot
  S  REGRESSION: every 'virtual' cell's stated slot equals the slot its thunk calls; the page's two tables and the generator's
     docstring no longer say slot 0 for all 111 (FAILS before)
Usage: python virtual_slot.py [--patch]
"""
import hashlib, io, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def thunk_slot(f):
    ins = [(x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + 0x30], f)][:10]
    if ("lea", "rcx, [rdx - 8]") not in ins or ("xor", "edx, edx") not in ins or ("mov", "rax, qword ptr [rcx]") not in ins: return None
    calls = [o for m, o in ins if m == "call"]
    m = re.fullmatch(r"qword ptr \[rax(?: \+ (0x[0-9a-f]+|\d+))?\]", calls[0]) if calls else None
    return (int(m.group(1), 0) // 8 if m.group(1) else 0) if m else None
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
TY = os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/phyre-virtual-destroy-slot/virtual_slot.py"
PAGE = os.path.join(DB, "22-Middleware-PhyreEngine", "Reflection-And-Class-Metadata", "class-descriptor-and-metadata-system.md")
GEN = os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts", "gen_phyre_descriptor_vtables.py")
PAT = re.compile(r"virtual - descriptor destroy slot \+0x58 \(([0-9A-F]{8})\) calls the object's own vtable slot\s+(\d+)")   # \s+: a corrected cell reads 'slot ~~0~~ 3' -> 'slot  3' once struck text is removed
def cells(l): return l.rstrip("\r\n").split("\t")
tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
from collections import Counter
got = Counter(); bad = []
for l in tl[1:]:
    c = cells(l); m = PAT.search(re.sub(r"~~.*?~~", "", c[6]))
    if not m: continue
    s = thunk_slot(int(m.group(1), 16)); got[(m.group(1), s)] += 1
    if s != int(m.group(2)): bad.append((c[0], m.group(1), int(m.group(2)), s))
check("V", thunk_slot(0x63FC60) == 0 and thunk_slot(0x68C4E0) == 3 and thunk_slot(0x680910) == 2 and sum(got.values()) == 111,
      "thunks: 0063FC60 slot 0, 0068C4E0 slot 3, 00680910 slot 2; cells per thunk %s" % dict(got))
OLD_ROW = "| **through the object's own vtable slot 0** | 111 | adjust the pointer (113 of the 114 by `-8`), then `mov rax,[rcx] ; call [rax]` |"
NEW_ROW = ("| **through the object's own vtable** (~~slot 0~~) | 111 | adjust the pointer (113 of the 114 by `-8`), then `mov rax,[rcx] ; "
           "call [rax + 8k]` - ~~`call [rax]` for all~~ slot 0 for the 87 on `0063FC60`, **slot 3** (`call [rax + 0x18]`) for the 23 "
           "physics shapes on `0068C4E0`, **slot 2** for `PScheduler` on `00680910` (corrected 2026-09-28, OPUS, "
           "`_index/candidates/phyre-virtual-destroy-slot/virtual_slot.py`) |")
OLD_X = "| indirect, through slot 0 | **111** | 0 |"
NEW_X = "| indirect, through a vtable slot (~~slot 0~~; 0, 3 or 2 by thunk) | **111** | 0 |"
OLD_G = "    111 classes  adjust the pointer, then `mov rax,[rcx] ; call [rax]`    the OBJECT's own slot 0\n"
NEW_G = ("    111 classes  adjust the pointer, then `mov rax,[rcx] ; call [rax+8k]`  the OBJECT's own vtable - slot 0 on\n"
         "                 0063FC60 (87), slot 3 on 0068C4E0 (23 physics shapes), slot 2 on 00680910 (PScheduler); read as\n"
         "                 slot 0 for all until 2026-09-28 (OPUS, _index/candidates/phyre-virtual-destroy-slot/virtual_slot.py)\n")
OLD_G2 = "    indirect, through slot 0           111               0\n"
NEW_G2 = "    indirect, through a vtable slot    111               0\n"
if "--patch" in sys.argv:
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]; m = PAT.search(c[6])
        if not m or "~~" in c[6][:m.end()]: continue
        s = thunk_slot(int(m.group(1), 16))
        if s is not None and s != int(m.group(2)):
            c[6] = (c[6][:m.start(2)] + "~~%s~~ %d (the thunk's call is `call [rax + 0x%X]` on the object at this-8; corrected 2026-09-28, OPUS, %s)"
                    % (m.group(2), s, 8 * s, REC) + c[6][m.end(2):])
            tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8"))
    for path, pairs in ((PAGE, ((OLD_ROW, NEW_ROW), (OLD_X, NEW_X))), (GEN, ((OLD_G, NEW_G), (OLD_G2, NEW_G2)))):
        raw = open(path, "rb").read().decode("utf-8"); crlf = "\r\n" in raw
        for a, b in pairs:
            a2, b2 = (a.replace("\n", "\r\n"), b.replace("\n", "\r\n")) if crlf else (a, b)
            assert raw.count(a2) == 1, (path, a[:40]); raw = raw.replace(a2, b2)
        open(path, "wb").write(raw.encode("utf-8"))
    print("patched"); sys.exit(0)
page = open(PAGE, "rb").read().decode("utf-8"); gen = open(GEN, "rb").read().decode("utf-8")
check("S", not bad and OLD_ROW not in page and OLD_X not in page and "slot 3" in page
      and OLD_G.strip() not in gen and OLD_G2.strip() not in gen,
      "every 'virtual' cell states its thunk's slot (%d wrong); the page tables and the generator docstring corrected" % len(bad))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
