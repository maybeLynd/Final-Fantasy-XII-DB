"""classify.py - RC-36 part 2 (FABLE, 2026-09-30): for every +0xC load that rc36_label_readers.py Part 2 listed in the
lmap family (and the non-lmap entries of that list), trace the base register to what it points at, and name the readers
of a menumap_location.bin array-B marker's +0x0C destination-label id.

Every verdict is an instruction pin: the script decodes the owning function linearly from its own entry (tk.fdis) and
checks the named instructions exist, at those addresses, with that text. A verdict with a failed pin prints FAIL.

Sections
  X  accessor facts the verdicts lean on (003BF430 kind out, 003BDFF0 kind-0 filter, 003BE1E0, 003BDDE0 paths).
  L  per-load table: load | base traced to | array | evidence.
  K  caller closure of every function whose +0xC base is a PARAMETER: raw E8/E9 index + 0F 8x jcc sweep +
     rip-relative references + DIR64 relocations, each site checked to sit on an instruction boundary. Every site found
     must be one the table accounts for.
  R  the reach limit: every function that loads the lmap file pointer [[02B457E0]+0xE0] (rip and image-base-relative
     sweeps of 02B457E0), each one classified as a B-pointer former or not.
  C  consumer chain of the B +0x0C readers: text resolver -> draw row +0x10 -> list record -> label pass draw call.
  D  data: the shipped menumap_location.bin (all 9 copies) - B +0x0C dword == -1 count (the fallback arm), B +0x14 link
     bytes vs countA (decides the kind of 003BDDE0's result on two stale-out paths), +0x11 < 48.
  CONTROL  003C0416 (003C0380, the kind-0 membership test) must classify as an A point.
Read-only on the image and the archive extract.
"""
import sys, json, struct, collections, glob, os
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone.x86 import X86_OP_MEM

IDX = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
RAW = collections.defaultdict(list)
for k, v in IDX.items():
    for s in v:
        RAW[int(k, 16)].append(int(s, 16))

_dec = {}
def body(e):
    if e not in _dec:
        _dec[e] = {x.address: x for x in tk.fdis(e)}
    return _dec[e]
def ins(a):
    o, how = tk.owner(a)
    if o is None or how != "listed":
        return None
    return body(o).get(a)
def T(x):
    return ("%s %s" % (x.mnemonic, x.op_str)).replace("  ", " ").strip() if x is not None else "<no instruction>"
def riptgt(x):
    for op in x.operands:
        if op.type == X86_OP_MEM and op.mem.base != 0 and x.reg_name(op.mem.base) == "rip":
            return x.address + x.size + op.mem.disp
    return None

FAILS = []
def pin(a, want):
    """want: exact instruction text ('mnemonic op_str'), or ('rip', target) for a rip-relative operand target."""
    x = ins(a)
    if isinstance(want, tuple):
        ok = x is not None and riptgt(x) == want[1]
        shown = "%s -> %08X" % (T(x), riptgt(x) or 0)
    else:
        ok = x is not None and T(x) == want
        shown = T(x)
    if not ok:
        FAILS.append("%08X: want %r, got %r" % (a, want, shown))
    return ok
def pins(lst):
    r = [pin(a, w) for a, w in lst]
    return all(r)
W = 0x02B457E0

out = []
def P(s=""):
    out.append(s); print(s)

# ---------------------------------------------------------------- X
P("== X  accessor facts")
X = {
 "X1 003BF430 kind out: 0 for i < countA (A at rec+4+24*i), 1 otherwise (B after A), 3 on failure": [
   (0x003BF46F, "mov dword ptr [r8], 3"), (0x003BF4C2, "cmp r10d, ecx"), (0x003BF4C5, "jae 0x3bf4e8"),
   (0x003BF4CC, "mov dword ptr [r8], 0"), (0x003BF4D7, "lea rax, [rcx*8 + 4]"), (0x003BF4F9, "mov dword ptr [r8], 1"),
   (0x003BF504, "sub r10d, eax"), (0x003BF50B, "lea rax, [r11 + rcx*8]")],
 "X2 003BDFF0 considers only kind-0 points (skips kind != 0) and returns a kind-0 index": [
   (0x003BE039, "call 0x3bf430"), (0x003BE03E, "cmp dword ptr [rsp + 0x50], 0"), (0x003BE043, "jne 0x3be1b0"),
   (0x003BE17C, "mov r14d, edi"), (0x003BE1CB, "mov eax, r14d")],
 "X3 003BE1E0 returns the point at 003BDFF0's index: an A point, since that index is < countA": [
   (0x003BE1FD, "call 0x3bdff0"), (0x003BE27C, "cmp edx, r9d"), (0x003BE27F, "jae 0x3be298"),
   (0x003BE289, "lea rax, [rax + rcx*8]")],
 "X4 003BDDE0 writes its kind out [r8] only on the enabled-first path; the 003BDF06 path (start point kind != 0) walks "
 "from countA and returns a same-+0x11 B point with [r8] unwritten": [
   (0x003BDE07, "mov r15, r8"), (0x003BDE7B, "mov eax, dword ptr [rsp + 0x20]"), (0x003BDE7F, "mov dword ptr [r15], eax"),
   (0x003BDEA4, "cmp dword ptr [rsp + 0x20], 0"), (0x003BDEAB, "jne 0x3bdf06"), (0x003BDF0B, "movzx ebx, byte ptr [rdi]"),
   (0x003BDFA7, "cmp byte ptr [rdi + 0x11], r15b"), (0x003BDFE4, "mov rax, rdi")],
 "X5 003C1A20 stores triples {+0 index, +8 point, +0x10 kind}; kind = 003BF430's out or 0 on the 003BE1E0 path; "
 "selector r8d filters (2 = all)": [
   (0x003C1B78, "call 0x3bf430"), (0x003C1B7D, "mov r14d, dword ptr [rsp + 0x50]"), (0x003C1B82, "mov r13, rax"),
   (0x003C1B99, "xor r14d, r14d"), (0x003C1BAB, "call 0x3be1e0"), (0x003C1BB0, "mov r13, rax"),
   (0x003C1BCC, "cmp esi, 2"), (0x003C1BD1, "cmp r14d, esi"),
   (0x003C1CC5, "mov qword ptr [r10 + rax*8 + 8], r13"), (0x003C1CCA, "mov dword ptr [r10 + rax*8 + 0x10], r14d")],
 "X6 003BE3A0 hands each triple to 003C2320 as (row, rdx = point, r8d = kind) and the triple array (rsp+0x60) as arg 5": [
   (0x003BE43A, "lea rcx, [rsp + 0x60]"), (0x003BE44E, "call 0x3c1a20"), (0x003BE51D, "lea rdi, [rsp + 0x70]"),
   (0x003BE538, "mov r8d, dword ptr [rdi]"), (0x003BE53E, "mov rdx, qword ptr [rdi - 8]"),
   (0x003BE545, "lea rax, [rsp + 0x60]"), (0x003BE54F, "mov qword ptr [rsp + 0x20], rax"), (0x003BE554, "call 0x3c2320")],
}
for k, v in X.items():
    P("  %s  %s" % ("PASS" if pins(v) else "FAIL", k))

# ---------------------------------------------------------------- L
P()
P("== L  per-load classification")
L = []  # (load, base traced to, array, evidence pins)
def add(load, traced, arr, ev):
    L.append((load, traced, arr, ev))

# the wmap / other-file header group
for load, ld, src, fn in ((0x003BCB05, 0x003BCAFE, 0x003BCAF5, "003BCAF0"), (0x003C000F, 0x003C0008, 0x003BFFFA, "003BFFF0"),
                          (0x003C00DF, 0x003C00D8, 0x003C00CA, "003C00C0"), (0x003C019F, 0x003C0198, 0x003C018A, "003C0180")):
    reg = T(ins(ld)).split(" ")[1].rstrip(",")
    add(load, "[[02B457E0]+0xD8] + 0xC: header word of menumap_world.bin (wmap), then added to the file base as a "
        "section offset", "wmap header, not lmap", [(src, ("rip", W)), (ld, T(ins(ld))), (load, T(ins(load)))])
    if "0xd8]" not in T(ins(ld)):
        FAILS.append("%08X is not a +0xD8 load" % ld)
add(0x003BD116, "wmap +word[+0xA] table entry, stride 0x1C (rsi = base + 4 + 0x1C*id)", "wmap entry, not lmap",
    [(0x003BD04A, ("rip", W)), (0x003BD057, "mov rax, qword ptr [r9 + 0xd8]"), (0x003BD05E, "movzx r8d, word ptr [rax + 0xa]"),
     (0x003BD09C, "imul rsi, rax, 0x1c"), (0x003BD116, "movzx eax, word ptr [rsi + 0xc]")])
# C entry
add(0x003BCEEC, "r8 argument = the array-C entry (003C0740's walk, SWE2-CONTRACT lmap_readers C1); +0x10 is C's gate",
    "C", [(0x003BCDEB, "movzx eax, word ptr [r8 + 0x10]"), (0x003BCDFA, "mov rdi, r8"), (0x003BCEEC, "movzx eax, word ptr [rdi + 0xc]")])
# A group
add(0x003BCBAF, "rcx argument; every caller passes an A point (section K, 003BCBA0)", "A",
    [(0x003BCBAF, "movzx esi, word ptr [rcx + 0xc]"), (0x003BCBB8, "call 0x3c0380")])
add(0x003BCBF7, "rdi = rcx argument (as above); +0xC -> MapRef_GetPersistenceGroupId, a field-id consumer", "A",
    [(0x003BCBB3, "mov rdi, rcx"), (0x003BCBF7, "movzx ecx, word ptr [rdi + 0xc]"), (0x003BCBFB, "call 0x264f90")])
add(0x003BF9CA, "rcx argument; sole caller 003C2320's kind-0 arm passes r15 (the point) at 003C2477", "A",
    [(0x003BF9CA, "movzx r14d, word ptr [rcx + 0xc]"), (0x003C23C5, "jne 0x3c248f"), (0x003C2477, "mov rcx, r15"),
     (0x003C2482, "call 0x3bf9a0")])
for a in (0x003C11A6, 0x003C11CA, 0x003C11DC, 0x003C11FE):
    add(a, "rdi = rdx argument; both callers (003BCEE3, 003BCF06) pass rdx = rbx = the kind-0 point of 003BCE66", "A",
        [(0x003C118D, "mov rdi, rdx"), (0x003BCE6B, "cmp dword ptr [rsp + 0x60], 0"), (0x003BCE73, "jne 0x3bd024"),
         (0x003BCED7, "mov rdx, rbx"), (0x003BCEFA, "mov rdx, rbx"), (a, T(ins(a)))])
add(0x003C17A2, "rcx = inline point arithmetic over [[02B457E0]+0xE0]; r8d = 0 for i < countA, 1 otherwise; load only "
    "when r8d == 0", "A", [(0x003C169D, "mov r8, qword ptr [rax + 0xe0]"), (0x003C1765, "xor r8d, r8d"),
                           (0x003C178A, "mov r8d, 1"), (0x003C179D, "test r8d, r8d"), (0x003C17A0, "jne 0x3c17b6"),
                           (0x003C17A2, "movzx ecx, word ptr [rcx + 0xc]")])
add(0x003C1936, "rdi = rdx argument; every caller reaches 003C18A0 only for kind 0 (section K, 003C18A0)", "A",
    [(0x003C18B7, "mov rdi, rdx"), (0x003C1936, "movzx ecx, word ptr [rdi + 0xc]")])
add(0x003BEAAC, "rbx = triple point [r14]; arm taken when triple kind [r14+8] == 0", "A",
    [(0x003BEA51, "add r14, 8"), (0x003BEA7E, "cmp dword ptr [r14 + 8], 0"), (0x003BEA83, "mov rbx, qword ptr [r14]"),
     (0x003BEA86, "jne 0x3beb01"), (0x003BEAAC, "movzx edi, word ptr [rbx + 0xc]")])
for a, x in ((0x003BF27E, "rax = [rbp-0x68] = local triple 0's point"), (0x003BF30A, "r14 = [r15], r15 = rbp-0x50 = triple 1's point, stepping 0x18"),
             (0x003BF363, "r14 as at 003BF30A")):
    add(a, x + "; 003BED70 stores a triple only when the point's kind (ebx) == 0 (003BF430 out, or 0 on the 003BE1E0 "
        "path, whose result is an A point by X3)", "A",
        [(0x003BEEDE, "test ebx, ebx"), (0x003BEEE0, "jne 0x3befbc"), (0x003BF14E, "test ebx, ebx"), (0x003BF150, "jne 0x3bf22c"),
         (0x003BEFAC, "mov qword ptr [rbp + rax*8 - 0x68], rcx"), (0x003BF21C, "mov qword ptr [rbp + rax*8 - 0x68], rcx"),
         (0x003BF263, "mov rax, qword ptr [rbp - 0x68]"), (0x003BF2EB, "lea r15, [rbp - 0x50]"), (0x003BF300, "mov r14, qword ptr [r15]"),
         (0x003BF3CC, "add r15, 0x18"), (a, T(ins(a)))])
add(0x003C23CB, "rdx = the triple point; kind-0 arm (r8d == 0)", "A",
    [(0x003C23C2, "test r8d, r8d"), (0x003C23C5, "jne 0x3c248f"), (0x003C23CB, "movzx ecx, word ptr [rdx + 0xc]")])
add(0x003C23F3, "r15 = rdx (003C2354); kind-0 arm", "A",
    [(0x003C2354, "mov r15, rdx"), (0x003C23C5, "jne 0x3c248f"), (0x003C23F3, "movzx edi, word ptr [r15 + 0xc]")])
add(0x003C25A4, "rax = 003BDDE0(n, B +0x14 link byte) with kind out [rsp+0x90] == 0 and enabled [rsp+0x80] != 0; "
    "+0xC -> 00377A40 (field-id bit 14). The linked point is A in the data (section D) - see the stale-out note",
    "A (linked zone), data-dependent", [(0x003C2567, "movzx eax, byte ptr [r15 + 0x14]"), (0x003C257B, "lea r8, [rsp + 0x90]"),
                                         (0x003C258B, "call 0x3bdde0"), (0x003C2590, "cmp dword ptr [rsp + 0x90], r14d"),
                                         (0x003C25A4, "movzx ecx, word ptr [rax + 0xc]"), (0x003C25A8, "call 0x377a40")])
# the B readers
add(0x003C25BD, "r15 = rdx (003C2354) = the triple point, in the kind-1 arm (r8d != 0 -> 003C248F; kind 1 = array B by "
    "X1/X5/X6). dword +0xC -> 002F9920 -> row +0x10", "B",
    [(0x003C2354, "mov r15, rdx"), (0x003C23BE, "mov byte ptr [rbp + 2], r8b"), (0x003C23C5, "jne 0x3c248f"),
     (0x003C248A, "jmp 0x3c2636"), (0x003C2565, "jne 0x3c25bd"), (0x003C25AF, "jne 0x3c25bd"),
     (0x003C25BD, "mov ecx, dword ptr [r15 + 0xc]"), (0x003C25C1, "cmp ecx, -1"), (0x003C25C4, "jne 0x3c2629"),
     (0x003C2629, "call 0x2f9920"), (0x003C262E, "mov qword ptr [rbp + 0x10], rax")])
add(0x003BEB06, "rbx = triple point [r14] with triple kind [r14+8] != 0 (the triple array is 003BE3A0's, via 003C2320 "
    "arg 5 -> r8 at 003C2690). dword +0xC -> 002F9920 -> 0029CD00 text extents", "B",
    [(0x003C263D, "mov rbx, qword ptr [rsp + 0xa0]"), (0x003C2690, "mov r8, rbx"), (0x003C269A, "call 0x3be950"),
     (0x003BE986, "mov r14, r8"), (0x003BEA51, "add r14, 8"), (0x003BEA7E, "cmp dword ptr [r14 + 8], 0"),
     (0x003BEA83, "mov rbx, qword ptr [r14]"), (0x003BEA86, "jne 0x3beb01"), (0x003BEB01, "call 0x37eb70"),
     (0x003BEB06, "mov ecx, dword ptr [rbx + 0xc]"), (0x003BEB0C, "call 0x2f9920"), (0x003BEB27, "call 0x29cd00"),
     (0x003BEB2C, "mov rax, qword ptr [r14]"), (0x003BEB39, "movzx edx, word ptr [rax + 8]"),
     (0x003BEB3D, "movzx eax, word ptr [rax + 0xa]")])
# CONTROL
add(0x003C0416, "rax = 003BF430(n, i) with kind out == 0 (003C0380, the membership test)", "A",
    [(0x003C040A, "call 0x3bf430"), (0x003C0416, T(ins(0x003C0416)))])
ctl_guard = False
bb = body(0x003C0380)
seq = sorted(a for a in bb if 0x003C040A < a < 0x003C0416)
for a in seq:
    t = T(bb[a])
    if t.startswith("cmp dword ptr [rsp") and t.endswith(", 0") or t.startswith("test") :
        ctl_guard = True
    P("    control window %08X %s" % (a, t))
# non-lmap entries of the census list
NON = [
 (0x0024A33D, "[rbx+0x20] of the image member callback's slot (0024A1D0: rdx -> slot +0x18; caller 00249670 image member callback)", [(0x0024A330, "mov rax, qword ptr [rbx + 0x20]")]),
 (0x002543FB, "[020927D0] + 0xC: another loaded table's header", [(0x002543F4, ("rip", 0x020927D0))]),
 (0x002F99BD, "st2e bank record array (002F9920, the high-pool text resolver)", [(0x002F9926, "mov eax, 0x68db8bad")]),
 (0x00369B49, "rbx = rcx - 0x40: the resource block header (magic 0xFF12 at +0) in front of a released buffer. The widget "
  "releases the lmap buffer here (003BC5EC), so this reads the lmap BLOCK HEADER, not a point", [(0x003698C1, "lea rbx, [rcx - 0x40]"), (0x003698BC, "mov eax, 0xff12"), (0x003BC5E0, "mov rcx, qword ptr [rdi + 0xe0]"), (0x003BC5EC, "call 0x3697f0")]),
 (0x0036AE1C, "rdx: a resource-pool slot descriptor (dword +0xC resolved by ImageAddress_ResolveRuntimePointer)", [(0x0036AE24, "call 0x20e600")]),
 (0x0036B235, "rdx: a resource-pool slot descriptor (as above)", [(0x0036B238, "call 0x20e600")]),
 (0x0036BD6C, "rdi: a resource-pool slot descriptor (as above)", [(0x0036BD6C, "mov ecx, dword ptr [rdi + 0xc]")]),
 (0x0039BC4A, "rdi: 0039BB60's own slot table entry; the widget passes [widget+0x108], not +0xE0", [(0x003BC630, "mov rcx, qword ptr [rdi + 0x108]"), (0x003BC63C, "call 0x39bb60")]),
 (0x0039BFFB, "rdi: the same slot-table shape as 0039BB60", [(0x0039BFFB, "mov ecx, dword ptr [rdi + 0xc]")]),
 (0x003BC92B, "rdi: the widget procedure's message payload", [(0x003BC919, "test rdi, rdi"), (0x003BC928, "mov esi, dword ptr [rdi + 8]")]),
 (0x003DFB6C, "rcx + 4*rdx + 0xC: a cached record's word table (callers are the map pages 002B7B80 / 00402xxx)", [(0x003DFB63, "cmp byte ptr [rcx + 7], 0x32")]),
 (0x003DFBD2, "as 003DFB6C", [(0x003DFBB5, "cmp byte ptr [rcx + 7], 0x32")]),
]
for a, why, ev in NON:
    add(a, why, "not an lmap point", ev + [(a, T(ins(a)))])

rows = []
for load, traced, arr, ev in L:
    ok = pins(ev)
    rows.append((load, ok))
    P("  %s  %08X  [%s]  %s" % ("PASS" if ok else "FAIL", load, arr, traced))
    P("        evidence: %s" % ", ".join("%08X" % a for a, _ in ev))

ctl_row = [r for r in L if r[0] == 0x003C0416][0]
ctl_ok = dict(rows)[0x003C0416] and ctl_guard and ctl_row[2] == "A"
P("CONTROL 003C0416 classified %s, kind-0 guard between call and load: %s -> %s" % (ctl_row[2], ctl_guard, "PASS" if ctl_ok else "FAIL"))
if not ctl_ok:
    FAILS.append("control 003C0416")

# every Part-2 lmap-family load must be in the table
PART2 = [0x003BCB05, 0x003BCBAF, 0x003BCBF7, 0x003BCEEC, 0x003BD116, 0x003BEAAC, 0x003BEB06, 0x003BF27E, 0x003BF30A,
         0x003BF363, 0x003BF9CA, 0x003C000F, 0x003C00DF, 0x003C019F, 0x003C11A6, 0x003C11CA, 0x003C11DC, 0x003C11FE,
         0x003C17A2, 0x003C1936, 0x003C23CB, 0x003C23F3, 0x003C25A4, 0x003C25BD, 0x003C27B0]
have = {r[0] for r in L}
# 003C26C0's load: base = [slot] where slot = widget + 0x120 + k*0xA8 (the menumap_subNN cache), not lmap
add(0x003C27B0, "003C26C0: rbx = rcx + 0x120 (+0xA8 per slot) - the map-data widget's menumap_subNN.bin cache slot; the "
    "load is off that slot's file table (r12 = [slot] + word[+0xA]), not lmap", "sub-map cache file, not lmap",
    [(0x003C26DA, "lea rbx, [rcx + 0x120]"), (0x003C26F7, "add rbx, 0xa8"), (0x003C271C, "mov rax, qword ptr [rbx]"),
     (0x003C2727, "movzx ecx, word ptr [rax + 0xa]"), (0x003C27B0, T(ins(0x003C27B0)))])
ok = pins(L[-1][3]); rows.append((0x003C27B0, ok))
P("  %s  %08X  [%s]  %s" % ("PASS" if ok else "FAIL", 0x003C27B0, L[-1][2], L[-1][1]))
P("        evidence: %s" % ", ".join("%08X" % a for a, _ in L[-1][3]))
P("        (the base register at 003C27B0: %s; preceding defs:)" % T(ins(0x003C27B0)))
b6 = body(0x003C26C0)
for a in sorted(a for a in b6 if 0x003C2780 <= a <= 0x003C27B0):
    P("          %08X %s" % (a, T(b6[a])))
missing = [a for a in PART2 if a not in {r[0] for r in L}]
P("Part-2 lmap-family loads not classified: %s" % (["%08X" % a for a in missing] or "NONE"))
if missing:
    FAILS.append("unclassified %s" % missing)

# ---------------------------------------------------------------- K
P()
P("== K  caller closure of the parameter-based functions (E8/E9 raw index + 0F 8x jcc + rip refs + DIR64 relocs)")
PARAM = {0x003BCBA0: "rcx", 0x003BF9A0: "rcx", 0x003C1180: "rdx", 0x003C18A0: "rdx", 0x003C1980: "rdx",
         0x003C0F70: "rdx", 0x003BE950: "r8 triples", 0x003C2320: "rdx+r8d", 0x003BCDE0: "r8", 0x003BE810: "rcx row"}
tx = tk.secs[".text"]; TVA, TVS, TRS, TRO = tx
code = tk.d[TRO:TRO + min(TVS, TRS)]
jcc = collections.defaultdict(list)
for i in range(len(code) - 6):
    if code[i] == 0x0F and 0x80 <= code[i + 1] <= 0x8F:
        t = TVA + i + 6 + struct.unpack_from("<i", code, i + 2)[0]
        if t in PARAM:
            jcc[t].append(TVA + i)
rr, rraw = tk.rip_refs(0x003BCA00, 0x003C2700)
riphit = collections.defaultdict(list)
for x, k, t in rr:
    if t in PARAM:
        riphit[t].append(x.address)
RAWSKIP = collections.Counter()
for a, t in rraw:
    if t not in PARAM:
        continue
    # a raw-only hit whose disp32 is the rel32 of a listed E8/E9 site to the same target is that call, not a reference
    if (a - 1) in RAW.get(t, []):
        RAWSKIP["own call rel32"] += 1
        continue
    # otherwise decode the owner linearly and show the instruction covering the hit
    o, how = tk.owner(a)
    cov = None
    if o is not None and how == "listed":
        for x in body(o).values():
            if x.address <= a < x.address + x.size:
                cov = x
    tgt = riptgt(cov) if cov is not None else None
    ref = cov is not None and (tgt == t or (cov.mnemonic in ("call", "jmp") and cov.op_str == hex(t)))
    if not ref:
        RAWSKIP["covered by an instruction that does not reference the target"] += 1
        P("  raw-only candidate %08X -> %08X inside %s: %s (not a reference)" % (a, t, tk.fname(a), T(cov)))
        continue
    riphit[t].append(("raw", a))
P("  raw-only rip candidates dismissed: %s" % dict(RAWSKIP))
rel = collections.defaultdict(list)
for a, q in tk.reloc_ptrs(0x003BCA00, 0x003C2700):
    if q in PARAM:
        rel[q].append(a)
def onb(a):
    b = tk.boundaries(a)
    return b is not None and a in b
# how each accounted call site supplies the parameter
ACC = {
 0x003BCBA0: {0x003BCE7C: "rbx = kind-0 point (003BCE6B/003BCE73)", 0x003BE8DA: "003BDDE0 result, kind out == 0 test (003BE8D0) - stale-out caveat (X4)",
              0x003BEA8B: "triple point with kind 0 (003BEA7E/003BEA86)", 0x003BF9D9: "own rcx = 003C2320 kind-0 point",
              0x003C07AE: "kind-0 point (003C079D/003C07A5)", 0x003C0FEE: "003BDDE0(n, B +0x14) result, NO kind test - A iff +0x14 < countA (section D)",
              0x003C18BA: "own rdx (kind 0 by 003C18A0's callers)", 0x003C1998: "own rdx = kind-0 point (003BCFAF/003BCFB4)"},
 0x003BF9A0: {0x003C2482: "r15 in 003C2320's kind-0 arm"},
 0x003C1180: {0x003BCEE3: "rbx kind 0", 0x003BCF06: "rbx kind 0"},
 0x003C18A0: {0x003BCE49: "kind 0 (003BCE3D/003BCE47)", 0x003BEE76: "kind 0 (003BEE6F/003BEE74)", 0x003BF0E6: "kind 0 (003BF0DF/003BF0E4)",
              0x003BF949: "kind 0 (003BF93D/003BF947)", 0x003C077A: "kind 0 (003C076E/003C0778)", 0x003C0D5E: "tail jmp, kind 0 (003C0D4D/003C0D57)",
              0x003C1428: "kind 0 (003C141B/003C1426)", 0x003C1B59: "kind 0 (003C1B4C/003C1B57)"},
 0x003C1980: {0x003BCFBE: "kind-0 point (003BCFAF/003BCFB4)"},
 0x003C0F70: {0x003BCE50: "kind != 0 (B)", 0x003BEE7D: "kind != 0 (B)", 0x003BF0ED: "kind != 0 (B)", 0x003BF950: "kind != 0 (B)",
              0x003C0781: "kind != 0 (B)", 0x003C0D68: "tail jmp, kind != 0 (B)", 0x003C142F: "kind != 0 (B)", 0x003C1B60: "kind != 0 (B)"},
 0x003BE950: {0x003C269A: "r8 = 003BE3A0's triple array (003C263D/003C2690)"},
 0x003C2320: {0x003BE554: "003BE3A0: rdx = triple point, r8d = triple kind (X6)"},
 0x003BCDE0: {},
 0x003BE810: {0x003C2672: "rcx = the row (003C266F)"},
}
unacc = []
for f in sorted(PARAM):
    e8 = sorted(RAW.get(f, []))
    j = [a for a in jcc.get(f, []) if onb(a)]
    jr = [a for a in jcc.get(f, []) if not onb(a)]
    r = riphit.get(f, [])
    rl = rel.get(f, [])
    P("  %08X (%s): E8/E9 %d, jcc %d (+%d off-boundary), rip refs %d, relocs %d" % (f, PARAM[f], len(e8), len(j), len(jr), len(r), len(rl)))
    for s in e8 + j:
        note = ACC[f].get(s)
        if f == 0x003BCDE0:
            # the C-entry callers: print the r8 setup
            ob = body(tk.owner(s)[0]); pre = [ob[a] for a in sorted(ob) if s - 0x30 <= a < s]
            r8 = [T(x) for x in pre if T(x).startswith(("mov r8,", "lea r8,"))]
            note = "C-entry caller; r8 setup %s" % (r8[-1:] or "not in the 0x30 bytes before")
        P("      %08X in %s: %s" % (s, tk.fname(s), note or "UNACCOUNTED"))
        if note is None:
            unacc.append(s)
    for s in r + rl:
        P("      reference %s in %s: UNACCOUNTED" % (s, tk.fname(s if isinstance(s, int) else s[1])))
        unacc.append(s)
P("K unaccounted sites: %s" % (unacc or "NONE"))
if unacc:
    FAILS.append("K unaccounted %s" % unacc)
for f, sites in (("003C18A0", [0x003BCE47, 0x003BEE74, 0x003BF0E4, 0x003BF947, 0x003C0778, 0x003C0D57, 0x003C1426, 0x003C1B57]),):
    for a in sites:
        x = ins(a)
        if x is None or x.mnemonic != "jne":
            FAILS.append("guard %08X not jne: %s" % (a, T(x)))
P("  003C18A0 kind-0 guards are jne-to-003C0F70 at all 8 sites: %s" % ("PASS" if not [f for f in FAILS if f.startswith("guard")] else "FAIL"))

# ---------------------------------------------------------------- R
P()
P("== R  reach limit: every function that loads [[02B457E0]+0xE0] (the lmap file pointer)")
h, raw = tk.rip_refs(W, W + 8)
h2, raw2 = tk.disp_refs(W - tk.BASE, W - tk.BASE + 8)
owners = collections.OrderedDict()
for x, k, t in h:
    o, how = tk.owner(x.address)
    owners.setdefault(o, set()).add(x.address)
P("  rip refs to 02B457E0: %d in %d functions (raw-only %d); image-base-relative disp refs: %d (raw %d)" %
  (len(h), len(owners), len(raw), len(h2), len(raw2)))
roots = collections.OrderedDict()
for o in owners:
    if o is None:
        continue
    for a, x in sorted(body(o).items()):
        s = T(x)
        if x.mnemonic == "mov" and s.endswith("+ 0xe0]") and "[rsp" not in s and s.split(" ")[1].rstrip(",") in (
                "rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"):
            roots.setdefault(o, []).append(a)
FORMERS = {  # what each lmap root function forms from the file pointer
 0x003BF430: "forms A and B; kind out 0/1 (X1); returns the point",
 0x003BDFF0: "forms A and B inline, keeps only kind 0 (X2); returns an index",
 0x003BE1E0: "forms from 003BDFF0's kind-0 index -> A (X3); returns the point",
 0x003BDDE0: "forms B on the 003BDF06 path (X4); returns the point - consumers 003BE810, 003C0F70, 003C2320 x2",
 0x003C1680: "forms A and B inline; +0xC only for r8d == 0 (row 003C17A2); returns 0/1",
 0x003BE700: "forms B inline (index from countA), reads byte +0x11 only, returns an index (003C2320's 0xD -> 0x2F remap)",
 0x003BE680: "forms rec+4+24*(A+B)+20*C = the 8-byte block, reads block +0/+2/+4 (RC-35 lead); no point",
 0x003BFF20: "C and D arithmetic (section 10.2); no point",
 0x003C1070: "C and D arithmetic (section 10.2); no point",
 0x003C0340: "countA + countB only; no point",
 0x003C0740: "C walk (C entry -> 003BCDE0 r8); no point",
 0x003BBFB0: "releases the lmap resource (003697F0); no point",
 0x003BC4E0: "releases the lmap resource (003697F0); no point",
}
unk = []
for o, sites in roots.items():
    P("  %s  %s  roots %s" % (tk.fname(o), FORMERS.get(o, "NOT READ"), ", ".join("%08X" % a for a in sites)))
    if o not in FORMERS:
        unk.append(o)
    # every memory operand at displacement 0x0C..0x13 in a root function: the folded forms (rec-relative +0x10 = point
    # +0xC) a '+0xc]' census cannot see. Stack operands are skipped.
    fold = []
    for a, x in sorted(body(o).items()):
        for op in x.operands:
            if op.type == X86_OP_MEM and 0x0C <= op.mem.disp <= 0x13 and op.mem.base != 0 and \
                    x.reg_name(op.mem.base) not in ("rsp", "rip"):
                fold.append("%08X %s" % (a, T(x)))
    for f in fold:
        P("      disp 0x0C..0x13: %s" % f)
P("  root functions not read: %s" % ([("%08X" % o) for o in unk] or "NONE"))
if unk:
    FAILS.append("R unread roots %s" % unk)
P("  (functions reading 02B457E0 without an +0xE0 load are outside the lmap reach and not listed)")
# the Part-2 census closure must contain every consumer of a returned point
callees = collections.defaultdict(set)
for t, ss in RAW.items():
    for s in ss:
        o, how = tk.owner(s)
        if o is not None and how == "listed":
            callees[o].add(t)
SEED = {0x003BC2D0, 0x003BC4E0, 0x003BC450} | {tk.owner(x.address)[0] for x, k, t in h if tk.owner(x.address)[1] == "listed"}
RC = set(SEED); fr = set(SEED)
for _ in range(3):
    nx = set()
    for f in fr:
        nx |= {c for c in callees[f] if tk.fsize(c)}
    nx -= RC; RC |= nx; fr = nx
need = set()
for f in (0x003BF430, 0x003BDDE0, 0x003BE1E0):
    need |= {tk.owner(s)[0] for s in RAW.get(f, [])}
need |= {0x003C2320, 0x003BE950, 0x003BE3A0, 0x003C0F70, 0x003BCBA0, 0x003C18A0, 0x003C1180, 0x003C1980, 0x003BF9A0, 0x003BE810}
outside = sorted(f for f in need if f not in RC)
P("  census closure (rc36 Part 2 recipe): %d functions; point consumers checked %d; outside the closure: %s" %
  (len(RC), len(need), [("%08X" % f) for f in outside] or "NONE"))
if outside:
    FAILS.append("consumers outside the census closure %s" % outside)

# ---------------------------------------------------------------- C
P()
P("== C  consumer chain of the B +0x0C label")
C = {
 "C1 002F9920 is the high-pool st2e resolver (id / 10000 = bank; 60,2xx -> bank 6)": [(0x002F9926, "mov eax, 0x68db8bad"), (0x002F992F, "sar edx, 0xc"), (0x002F9939, "cmp edx, 0x1c")],
 "C2 fallback when B dword +0xC == -1: menumap_common entry[byte +0x11] dword +4 -> 002F9920 -> row +0x10": [
   (0x003C25CD, "movzx ebx, byte ptr [r15 + 0x11]"), (0x003C25D2, "mov rax, qword ptr [rdx + 0xe8]"), (0x003C25F1, "lea rax, [rbx*8 + 4]"),
   (0x003C25FC, "mov ecx, dword ptr [rax + 4]"), (0x003C2604, "call 0x2f9920"), (0x003C2613, "mov qword ptr [rbp + 0x10], rdi")],
 "C3 locked marker (row +0x1C bit 0 clear and the +0x14 zone's 00377A40 bit clear): row +0x10 = 002F9860(0x3EC)": [
   (0x003C24F0, "and dword ptr [rbp + 0x1c], 0xfffffffe"), (0x003C250D, "or dword ptr [rbp + 0x1c], 1"), (0x003C2562, "and eax, 1"),
   (0x003C25B1, "mov ecx, 0x3ec"), (0x003C25B6, "call 0x2f9860"), (0x003C262E, "mov qword ptr [rbp + 0x10], rax")],
 "C4 B +8/+0xA -> row +0x18/+0x1A; row +2 = kind (1 for a marker)": [
   (0x003C23A6, "movzx eax, word ptr [rdx + 8]"), (0x003C23AA, "mov word ptr [rbp + 0x18], ax"), (0x003C23AE, "movzx eax, word ptr [rdx + 0xa]"),
   (0x003C23B2, "mov word ptr [rbp + 0x1a], ax"), (0x003C23BE, "mov byte ptr [rbp + 2], r8b")],
 "C5 00402C30 copies the 0x30 row into the list record and measures its +0x10 string (0029CD00) into +0x48/+0x4A": [
   (0x00402C43, "movups xmmword ptr [rcx], xmm0"), (0x00402C4A, "movups xmmword ptr [rcx + 0x10], xmm1"),
   (0x00402C56, "cmp qword ptr [rdx + 0x10], 0"), (0x00402C6A, "mov rcx, qword ptr [rcx + 0x10]"), (0x00402C7A, "call 0x29cd00"),
   (0x00402CAC, "cmp byte ptr [rdi + 2], 1")],
 "C6 the label pass 004044D0 draws a kind-1 record's +0x10 through 002D8670 at +0x18/+0x1A; grey 0x80404040 unless "
 "+0x4E bit 3 or +0x1C bit 0; the 0x3EC string is dropped unless 00254A10 answers": [
   (0x00404570, "cmp byte ptr [rdi + 2], 1"), (0x00404597, "movsx eax, word ptr [rdi + 0x18]"), (0x004045A7, "movsx eax, word ptr [rdi + 0x1a]"),
   (0x004045E3, "mov rax, qword ptr [rdi + 0x10]"), (0x0040463F, "test byte ptr [rdi + 0x1c], 1"),
   (0x00404645, "mov dword ptr [rsi + 0x90], 0x80404040"), (0x00404676, "call 0x254a10"), (0x0040467F, "mov ecx, 0x3ec"),
   (0x00404695, "cmove rcx, rax"), (0x004046AB, "call 0x2d8670")],
 "C7 003BE950 (the directional next-target search) measures the B label (002F9920 -> 0029CD00) and centres it on B +8/+0xA "
 "before the distance test 003BD6F0; the result is the row's direction byte +8..+B": [
   (0x003BEB0C, "call 0x2f9920"), (0x003BEB27, "call 0x29cd00"), (0x003BEB4C, "sar ecx, 1"), (0x003BEC15, "call 0x3bd6f0"),
   (0x003C269F, "mov byte ptr [r12], al"), (0x003C2369, "lea r12, [rcx + 8]")],
}
for k, v in C.items():
    P("  %s  %s" % ("PASS" if pins(v) else "FAIL", k))
P("  rawcalls: 004044D0 callers %s; 00402C30 callers %s; 003BE3A0 callers %s" % (
  ["%08X" % s for s in sorted(RAW.get(0x004044D0, []))], ["%08X" % s for s in sorted(RAW.get(0x00402C30, []))],
  ["%08X" % s for s in sorted(RAW.get(0x003BE3A0, []))]))

# ---------------------------------------------------------------- D
P()
P("== D  data (shipped menumap_location.bin, all copies under D:/FFXII_TZA_extract)")
H = lambda b, o: struct.unpack_from("<H", b, o)[0]
I = lambda b, o: struct.unpack_from("<I", b, o)[0]
paths = sorted(glob.glob(r"D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/*/worldmap/menumap_location.bin"))
P("  copies: %d" % len(paths))
for p in paths:
    b = open(p, "rb").read()
    cnt = b[9]
    offs = [H(b, 0xA + 2 * i) for i in range(cnt)]
    nb = neg1 = lab = link_in_a = link_ff = link_b = dest_ok = 0
    labels = set(); sel_to_b = 0; sel_tot = 0
    for r in offs:
        A, Bn = b[r], b[r + 1]
        for e in range(A + Bn):
            o = r + 4 + 24 * e
            for s in range(4):
                v = b[o + 4 + s]
                if v != 0xFF:
                    sel_tot += 1
                    if v >= A:
                        sel_to_b += 1
        for e in range(Bn):
            o = r + 4 + 24 * A + 24 * e
            nb += 1
            dw = I(b, o + 0xC)
            if dw == 0xFFFFFFFF:
                neg1 += 1
            elif 60201 <= dw <= 60244:
                lab += 1; labels.add(dw)
            l14 = b[o + 0x14]
            if l14 == 0xFF: link_ff += 1
            elif l14 < A: link_in_a += 1
            else: link_b += 1
            if b[o + 0x11] < cnt: dest_ok += 1
    P("  %-3s B entries %d: dword +0xC == -1: %d; in 60201..60244: %d (%d distinct); +0x14 link < countA: %d, == 0xFF: %d, "
      "indexes B: %d; +0x11 < %d records: %d; point selector bytes +4..+7 indexing a B point: %d of %d" %
      (p.replace("\\", "/").split("/")[-3], nb, neg1, lab, len(labels), link_in_a, link_ff, link_b, cnt, dest_ok, sel_to_b, sel_tot))

# ---------------------------------------------------------------- verdict
P()
breaders = [r[0] for r in L if r[2] == "B"]
P("B +0x0C readers: %s" % ", ".join("%08X (%s)" % (a, tk.fname(a)) for a in breaders))
P("FAILS %d" % len(FAILS))
for f in FAILS:
    P("  " + f)
sys.exit(1 if FAILS else 0)
