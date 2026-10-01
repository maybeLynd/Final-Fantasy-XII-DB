"""gr17_lifetime_check.py - GR-17: can the .ard reward tables a battle unit's +0xE70 / +0xE78 point into be freed while
that unit can still reach a reader? (SWE2-ORACLE for OPUS, 2026-09-30)
Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py (extents, disassembly, the cached
direct call/jmp graph and rip-reference scan).

S1  reader entry: 002F8BB0 / 002F90C0 / 00317090 are called only from 00312280; 00312280 only from 0030E360 @0030E884;
    none of the four is named by a rip reference or by any qword in the image (no vtable / callback slot).
S2  the unit whose +0xE70/+0xE78 the readers load is the DEFEATED unit: each reader copies its base from the rdx (or,
    00317090, rcx) argument, 00312280 passes its own rdx (r14), and 0030E360 passes rbx = 0031B860(holder).
S3  0031B860 selects that unit as the first pool entry (00236820(i), i < 00236850()) whose +0x698 equals the holder;
    no other test (no bit-0 "allocated" or bit-4 "in battle" check).
S4  0030E360 reaches 00312280 only on the status arms 0 / 1 / 31 (jump table 00120000+0x1EE8C4 / +0x1EE8A4), and only
    when [rsp+0x44] != 0, i.e. the mode argument is 3 or 4 (set).
S5  allocation: 00234480 is the only allocator (memset 0xF50 of a free unit, then bit 0) - called only from 00265A20,
    which calls it only when [mgr + 0x28] == 0 and actor +0x14 >= 0x80; 00265A20 is called only by the manager init
    0026CE60; [mgr + 0x28] is the manager index (0026C8C0 stores ebp = movsxd ecx into 02098E10 + idx*0x288 + 0x28).
    The only other setter of actor +0x30 (002134A0) is used by 001E8580 on a 0x98-byte object, not an actor.
    => only manager-0 actors ever own a battle unit.
S6  release: 00234200 is called only from 0025B070 @0025B225 under the allocation predicate (+0x14 >= 0x80 and
    +0x30 != 0) and memsets the whole 0xF50 unit (+0x698, +0xE70, +0xE78 -> 0) at 002342CE; 0025B070 is called only by
    the manager unload 002628B0 @00262D34, skipped only for manager 4 and when the manager's loaded bit is clear.
S7  order: the .ard buffer (02B5E0C0) is freed only at 003EA888 / 003EA992 in 003EA820 (003EA6B0 zeroes the pointer
    without freeing); 003EA820 is reached only by the tail jump in 003EA6E0, called only by 0032FC30 @0032FC4B (mode 0),
    which then always calls 0032FCA0 @0032FC7B, which always calls 002628B0(mode = 0) @0032FCF6.
S8  manager 0's loaded bit ([mgr+0x10] bit 0): set only by the init at 0026D305 (after its unit allocation), cleared by
    the unload at 00262DA8 (after the release) and by the setup 0026C8C0, whose only routes are load callbacks issued by
    0032FCA0 after its own unload call.
S9  the window from each free to each unit's memset (003EA820 after the free, 0032FC30 after 003EA6E0, 0032FCA0 up to
    its 002628B0 call, 002628B0 up to its 0025B070 call, all of 0025B070, 00234200 up to the memset): no indirect call,
    and exactly two call sites whose direct-call closure reaches 00312280 - 0025B225 (-> 00234200) and 0023423F
    (-> 00300140(unit, 1)).
S10 that route is a single chain: every path from 00300140 to 00312280 runs through the edge 00310780 @0031082C ->
    00319420 (stop the unit's effect handle +0x6B0+0xC4 with sequence 1) and through the sequence starter 0046EFD0,
    whose 003B8670 launch is gated by the effect data (track kind byte +1 == 2, flag +5 bit 0). Removing either cuts
    every route. This is the one sub-fact left to data.
S11 party path: 0023A570 stores +0xE70 / +0xE78 only at 0023A9A5 / 0023A9F4 (the .ard arm); the party arm reaches the
    common tail 0023ABCA without them. A stale value can therefore only come from an earlier install in the SAME
    allocation, and no allocation outlives a manager-0 unload (S5-S8), so it points into the live buffer, not a freed one.
Controls: the closure search finds 0030E360 -> 00312280 (positive) and the S9 scan does flag 00234200 (non-vacuous);
S10 shows the chain is live before either cut.
Prints PASS/FAIL per check and FAILS n last.
"""
import collections, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, SC = T.R, T.sizes(), T.scan()
CALLS, REFS = SC["calls"], SC["refs"]
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def ins(a, n=16):
    return next(R.md.disasm(R.at(a, n), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def callers(t):
    return sorted(CALLS.get(t, ()))


def fmt(cs):
    return " ".join("%08X@%08X" % c for c in cs) or "-"


FWD = collections.defaultdict(set)
for t, cs in CALLS.items():
    for f, s in cs:
        FWD[f].add((t, s))
REV = collections.defaultdict(set)
for f, es in FWD.items():
    for t, s in es:
        REV[t].add(f)
TGT = 0x00312280


def reaches(src, dst=TGT, cut_node=None, cut_site=None):
    seen, q = {src}, [src]
    while q:
        f = q.pop()
        if f == dst:
            return True
        for t, s in FWD.get(f, ()):
            if t == cut_node or s == cut_site or t in seen:
                continue
            seen.add(t)
            q.append(t)
    return False


# S1 - reader entry
rd = {0x002F8BB0: callers(0x002F8BB0), 0x002F90C0: callers(0x002F90C0), 0x00317090: callers(0x00317090)}
only_312 = all(c and all(f == TGT for f, _ in c) for c in rd.values())
c312 = callers(TGT)
no_rip = all(not REFS.get(a) for a in (0x002F8BB0, 0x002F90C0, 0x00317090, TGT))
no_q = all(not T.qword_sites(a) for a in (0x002F8BB0, 0x002F90C0, 0x00317090, TGT))
check("S1", only_312 and c312 == [(0x0030E360, 0x0030E884)] and no_rip and no_q,
      "readers <- %s; 00312280 <- %s; rip refs none=%s; qword slots none=%s"
      % (["%08X" % f for f in sorted({f for c in rd.values() for f, _ in c})], fmt(c312), no_rip, no_q))

# S2 - the dereferenced unit is the defeated unit returned by 0031B860
s2 = {0x002F8BC9: "mov r14, rdx", 0x002F8C7E: "mov rax, qword ptr [r14 + 0xe70]",
      0x002F90CA: "mov rdi, rdx", 0x002F9136: "mov rax, qword ptr [rdi + 0xe70]",
      0x00317090: "mov r8, rcx", 0x003170BA: "mov rax, qword ptr [rcx + 0xe78]", 0x003170C4: "mov rax, qword ptr [r8 + 0xe70]",
      0x003122AB: "mov r14, rdx", 0x00312534: "mov rax, qword ptr [r14 + 0xe78]", 0x0031253F: "mov rax, qword ptr [r14 + 0xe70]",
      0x003123C7: "mov rdx, r14", 0x003124B9: "mov rdx, r14", 0x003125B9: "mov rcx, r14",
      0x0030E3A7: "call 0x31b860", 0x0030E3B3: "mov rbx, rax", 0x0030E3B6: "mov qword ptr [rsp + 0x70], rax",
      0x0030E881: "mov rdx, rbx", 0x0030E884: "call 0x312280"}
bad2 = [("%08X" % a, txt(a)) for a, t in s2.items() if txt(a) != t]
# rbx writes inside 0030E360 other than the capture, its spill reload and the epilogue restore
rbxw = [i for i in body(0x0030E360) if re.match(r"(mov|lea|xor|pop) rbx", "%s %s" % (i.mnemonic, i.op_str))]
rbx_ok = sorted(i.address for i in rbxw) == [0x0030E3B3, 0x0030E6D9, 0x0030E83D] and \
    txt(0x0030E6D9) == "mov rbx, qword ptr [rsp + 0x70]"
check("S2", not bad2 and rbx_ok, "base = entry rdx/rcx in every reader; 0030E360 rdx = rbx = 0031B860(holder); "
      "rbx writes %s; mismatches %s" % (["%08X" % i.address for i in rbxw], bad2))

# S3 - 0031B860 matches +0x698 only
b3 = [("%s %s" % (i.mnemonic, i.op_str)) for i in body(0x0031B860)]
tests = [t for t in b3 if t.startswith(("cmp", "test"))]
check("S3", "call 0x236820" in b3 and "call 0x236850" in b3 and
      tests == ["test rcx, rcx", "test eax, eax", "test rax, rax", "cmp qword ptr [rax + 0x698], rdi", "cmp ebx, eax"],
      "tests in 0031B860: %s" % tests)

# S4 - status arms and mode gate
base = 0x00120000
idx = R.at(base + 0x1EE8C4, 32)
arm = {s: struct.unpack("<I", R.at(base + 0x1EE8A4 + 4 * idx[s], 4))[0] + base for s in range(32)}
to_ko = sorted(s for s, t in arm.items() if t in (0x0030E80A, 0x0030E850, 0x0030E85E))
gate = [txt(0x0030E80D), txt(0x0030E80F), txt(0x0030E853), txt(0x0030E855), txt(0x0030E861), txt(0x0030E863),
        txt(0x0030E3C2), txt(0x0030E3C5), txt(0x0030E3C8), txt(0x0030E3CB), txt(0x0030E5E6)]
check("S4", to_ko == [0, 1, 31] and gate == ["test edi, edi", "jne 0x30e875", "test edi, edi", "je 0x30e811",
      "test edi, edi", "je 0x30e811", "lea ecx, [rdx - 3]", "cmp ecx, 1", "setbe al", "mov dword ptr [rsp + 0x44], eax",
      "mov edi, dword ptr [rsp + 0x44]"],
      "status arms reaching 0030E875 -> 00312280: %s; gated on edi = (mode - 3 <= 1)" % to_ko)

# S5 - allocation only for manager-0 actors
a5 = callers(0x00234480) == [(0x00265A20, 0x00265A9F)] and callers(0x00265A20) == [(0x0026CE60, 0x0026CECE)]
m5 = [txt(0x002344C7), txt(0x002344C9), txt(0x002344D2), txt(0x002344D7), txt(0x002344E7)] == \
    ["xor edx, edx", "mov r8d, 0xf50", "call 0x861ec0", "or dword ptr [rbx], 1", "call 0x2134a0"]
g5 = [txt(0x00265A70), txt(0x00265A74), txt(0x00265A83), txt(0x00265A87), txt(0x00265A89), txt(0x00265A30)] == \
    ["cmp dword ptr [rbp + 0x28], r12d", "jne 0x265b16", "movzx eax, byte ptr [rax + 0x14]", "cmp al, 0x80",
     "jb 0x265b16", "xor r12d, r12d"]
i5 = [txt(0x0026C8ED), txt(0x0026C8FE), txt(0x0026C907), txt(0x0026C90E), txt(0x0026C957)] == \
    ["movsxd rbp, ecx", "lea rdi, [r14 + 0x1f78e10]", "imul r8, rbp, 0x288", "add rdi, r8", "mov dword ptr [rdi + 0x28], ebp"] \
    and txt(0x0026C8F0).startswith("lea r14, [rip")
o5 = callers(0x002134A0) == [(0x001E8580, 0x001E9230), (0x00234480, 0x002344E7)] and txt(0x001E91C9) == "mov edx, 0x98" \
    and txt(0x001E91DA) == "mov r15, rax" and txt(0x001E91F3) == "call 0x2130e0"
check("S5", a5 and m5 and g5 and i5 and o5,
      "00234480 <- 00265A20 <- 0026CE60 only; memset 0xF50 + bit0; gate [mgr+0x28]==0 (= manager index, 0026C957) "
      "and actor+0x14>=0x80; 002134A0 other caller 001E8580 builds a 0x98-byte object")

# S6 - release
r6 = callers(0x00234200) == [(0x0025B070, 0x0025B225)] and callers(0x0025B070) == [(0x002628B0, 0x00262D34)]
p6 = [txt(0x0025B212), txt(0x0025B216), txt(0x0025B218), txt(0x0025B21D), txt(0x0025B222)] == \
    ["cmp byte ptr [rax + 0x14], 0x80", "jb 0x25b22a", "cmp qword ptr [rax + 0x30], 0", "je 0x25b22a", "mov rdx, rax"]
k6 = [txt(0x00234210), txt(0x002342C3), txt(0x002342C5), txt(0x002342CB), txt(0x002342CE), txt(0x002342A8), txt(0x002342AB)] == \
    ["call 0x263e30", "xor edx, edx", "mov r8d, 0xf50", "mov rcx, rbx", "call 0x861ec0", "cmp rbx, rdx", "jae 0x2342c3"]
u6 = [txt(0x0026292C), txt(0x00262930), txt(0x00262D2C), txt(0x00262D2F), txt(0x00262DA8)] == \
    ["test byte ptr [rbx + 0x10], sil", "je 0x262d96", "cmp edi, 4", "je 0x262d96", "and byte ptr [rbx + 0x10], 0xfe"]
check("S6", r6 and p6 and k6 and u6 and sorted(f for f, _ in callers(0x002628B0)) == [0x0025BFB0, 0x0032FCA0],
      "00234200 <- 0025B070 <- 002628B0 only; predicate = allocation predicate; memset 0xF50 at 002342CE for every pool "
      "unit; skipped only for manager 4 / not-loaded; 002628B0 <- %s" % fmt(callers(0x002628B0)))

# S7 - the free is always followed by manager-0 unload in the same call
fr = sorted(a for g, sites in REFS.items() if g == 0x02B5E0C0 for f, a, k in sites)
f7 = fr == [0x003EA65E, 0x003EA6C3, 0x003EA809, 0x003EA86D, 0x003EA88F, 0x003EA999] and \
    [txt(0x003EA86D), txt(0x003EA888), txt(0x003EA992)] == ["mov rcx, qword ptr [rip + 0x277384c]", "call 0x3697f0", "call 0x3697f0"] \
    and txt(0x003EA6C3).startswith("movdqu") and "0x3697f0" not in " ".join(txt(i.address) for i in body(0x003EA6B0))
o7 = callers(0x003EA820) == [(0x003EA6E0, 0x003EA700)] and callers(0x003EA6E0) == [(0x0032FC30, 0x0032FC4B)]
seq = [txt(a) for a in (0x0032FC3E, 0x0032FC40, 0x0032FC4B, 0x0032FC77, 0x0032FC79, 0x0032FC7B, 0x0032FCBF, 0x0032FCF4, 0x0032FCF6)]
s7 = seq == ["test ecx, ecx", "jne 0x32fc77", "call 0x3ea6e0", "mov edx, edi", "mov ecx, ebx", "call 0x32fca0",
             "movsxd rdi, ecx", "mov ecx, edi", "call 0x2628b0"]
# every conditional branch between 0032FC4B and 0032FC7B lands on 0032FC77 (no exit), same for 0032FCC2..0032FCF6 -> 0032FCEE/0032FCF4
br = [i for i in R.md.disasm(R.at(0x0032FC50, 0x2B), 0x0032FC50) if i.mnemonic.startswith("j")]
br2 = [i for i in R.md.disasm(R.at(0x0032FCC2, 0x34), 0x0032FCC2) if i.mnemonic.startswith("j")]
nb = all(int(i.op_str, 16) == 0x0032FC77 for i in br) and all(int(i.op_str, 16) in (0x0032FCEE, 0x0032FCF4) for i in br2)
check("S7", f7 and o7 and s7 and nb,
      "02B5E0C0 refs %s; frees 003EA888/003EA992 only; 003EA820 <- 003EA6E0 <- 0032FC30@0032FC4B; then 0032FCA0@0032FC7B "
      "-> 002628B0(0)@0032FCF6 on every path" % ["%08X" % a for a in fr])

# S8 - manager loaded bit
w8 = []
for f in (0x0026CE60, 0x002628B0, 0x0026C8C0):
    for i in body(f):
        if re.match(r"(or|and|mov) byte ptr \[r\w+ \+ 0x10\], ", "%s %s" % (i.mnemonic, i.op_str)):
            w8.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
setup = callers(0x0026C8C0) == [(0x0032F850, 0x0032F966)] and callers(0x0032F850) == [(0x003304A0, 0x00330514)] and \
    sorted(REFS.get(0x0032F850, ())) == [(0x003306E0, 0x00330FAD, "lea")] and callers(0x003304A0) == [(0x00330310, 0x0033040E)] and \
    callers(0x00330310) == [(0x0032FCA0, 0x00330030)] and callers(0x003306E0) == [(0x0032FCA0, 0x00330029)]
order = 0x0026CECE < 0x0026D305 and 0x00262D34 < 0x00262DA8 and 0x0032FCF6 < 0x00330029
check("S8", setup and order and "0026D305 or byte ptr [rbx + 0x10], 1" in w8 and "00262DA8 and byte ptr [rbx + 0x10], 0xfe" in w8,
      "bit-0 writers in init/unload/setup: %s; setup 0026C8C0 reached only via 0032FCA0 @00330029/@00330030 (after 0032FCF6)" % w8)

# S9 - the free -> memset window
W = [(0x003EA820, 0x003EA88D, 0x003EA9F8), (0x0032FC30, 0x0032FC50, 0x0032FC7B), (0x0032FCA0, 0x0032FCC2, 0x0032FCF6),
     (0x002628B0, 0x002628B0, 0x00262D34), (0x0025B070, 0x0025B070, 0x0025B249), (0x00234200, 0x00234200, 0x002342CE)]
hit, indirect, nsites = [], [], 0
for f, lo, hi in W:
    for i in R.md.disasm(R.at(lo, hi - lo), lo):
        if i.mnemonic in ("call", "jmp"):
            if not i.op_str.startswith("0x"):
                indirect.append("%08X %s %s" % (i.address, i.mnemonic, i.op_str))
                continue
            t = int(i.op_str, 16)
            if i.mnemonic == "jmp" and f <= t < f + SZ[f]:
                continue
            nsites += 1
            if reaches(t):
                hit.append("%08X->%08X" % (i.address, t))
check("S9", not indirect and hit == ["0025B225->00234200", "0023423F->00300140"],
      "%d direct call/tail sites in the window; reaching 00312280: %s; indirect %s" % (nsites, hit, indirect))

# S10 - the single residual chain and its data gate
live = reaches(0x00300140)
cut_n = not reaches(0x00300140, cut_node=0x0046EFD0)
cut_e = not reaches(0x00300140, cut_site=0x0031082C)
gate10 = [txt(a) for a in (0x0030014B, 0x0030014D, 0x003105DE, 0x00310605, 0x0031082C, 0x00319429, 0x0031943C,
                           0x0046F092, 0x0046F098, 0x0046F0AF, 0x00333303, 0x0024FF42)]
g10 = gate10 == ["je 0x300152", "call 0x3105d0", "cmp qword ptr [rcx + 0x698], 0", "call 0x310780", "call 0x319420",
                 "mov ecx, dword ptr [rcx + 0xc4]", "call 0x2eaea0", "test byte ptr [rax + 5], r12b", "cmp byte ptr [rax + 1], 2",
                 "call 0x3b8670", "call 0x46efd0", "call 0x333280"]
check("S10", live and cut_n and cut_e and g10 and txt(0x0023423F) == "call 0x300140" and txt(0x00234237) == "mov edx, 1",
      "00300140(unit,1) reaches 00312280=%s; still reaches with node 0046EFD0 removed=%s, with edge 0031082C removed=%s; gates %s"
      % (live, not cut_n, not cut_e, "as read" if g10 else gate10))

# S11 - party path
st = [i.address for i in body(0x0023A570) if re.match(r"mov qword ptr \[\w+ \+ 0xe7[08]\], ", "%s %s" % (i.mnemonic, i.op_str))]
arms = [txt(0x0023A626), txt(0x0023A628), txt(0x0023A62E), txt(0x0023A631), txt(0x0023AA2A), txt(0x0023AA44)]
party_range = [i.address for i in R.md.disasm(R.at(0x0023AA49, 0x0023ABCA - 0x0023AA49), 0x0023AA49)
               if "0xe70]" in i.op_str or "0xe78]" in i.op_str]
check("S11", st == [0x0023A9A5, 0x0023A9F4] and not party_range and
      arms == ["test esi, esi", "je 0x23aa49", "cmp esi, 1", "je 0x23a641", "jmp 0x23abca", "jmp 0x23abca"],
      "+0xE70/+0xE78 stores in the install %s; party arm 0023AA49..0023ABCA touches them %d times" % (["%08X" % a for a in st], len(party_range)))

# Controls
check("C1", reaches(0x0030E360) and not reaches(0x00319140) and not reaches(0x002EB780),
      "closure finds 0030E360 -> 00312280; 00319140 / 002EB780 (window callees) do not reach")

print("FAILS %d" % fails)
