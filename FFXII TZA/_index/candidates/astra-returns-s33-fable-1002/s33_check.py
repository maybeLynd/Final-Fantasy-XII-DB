"""s33_check.py - FABLE, 2026-10-02: re-reads every image fact that README.md (astra-returns-s33-fable-1002) and the
loot page's 2026-10-02 paragraph state from ASTRA's s33-visual-retirement-clock packet (producer commit 045a4c6af,
SWE2-AUDIT-SPEC ACCEPT). Read-only.

Instructions are decoded by the analysis kit's disasm_fn.py (Database/Tools/analysis-kit/gfz-scripts/disasm_fn.py
ADDR LEN, which prints address, bytes, mnemonic and resolves every rip target). Each of the five bodies is decoded
linearly from its entry over the packet's exclusive end, and each cited instruction is compared with its exact
decoded text and, for a rip operand, its resolved target. One rodata value (the decline constant) is read with
disasm_fn's own section-aware Image reader.

Groups: N = neutral retirement 003FA820, U = local visual update 003FC510, M = manager traversal 003FA790,
L = unlink and clear 003FA4E0, G = render gate 001EDE80, D = the decline constant 00D1204C.
These are static reads of single instructions and orderings. They are not executions, and they do not test caller
cadence, initialized values, interleaving or renderer effects (the packet's and the page's stated limits).

Control (sensitive to the defect it names):
 K1 the phase-3 release guard with the opposite signedness (`jge` for the shipped `jg` at 003FC6B0, which would make
    a zero fade word NOT release) must be reported as a mismatch by the same comparator - so a PASS is not produced
    by a comparator that accepts any text at a valid instruction boundary.
Prints PASS/FAIL per check and FAILS n."""
import hashlib, os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))                 # Database/
KIT = os.path.join(DBROOT, "Tools", "analysis-kit", "gfz-scripts")
DISASM = os.path.join(KIT, "disasm_fn.py")
EXE_SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"

sys.dont_write_bytecode = True                                   # leave no __pycache__ in the kit or the record
sys.path.insert(0, KIT)
import disasm_fn  # noqa: E402  (the same module the subprocess runs; used here only for its Image reader)

fails = 0
def check(name, ok, got=""):
    global fails
    print("%s %s%s" % ("PASS" if ok else "FAIL", name, ("" if ok else "  -> " + str(got))))
    if not ok: fails += 1

LINE = re.compile(r"^([0-9A-F]{8})  ([0-9a-f]+)\s+(.*?)(?:  ; (.*))?$")
def span(addr, end):
    out = subprocess.run([sys.executable, "-B", DISASM, "%08X" % addr, hex(end - addr)], capture_output=True, text=True)
    if out.returncode != 0: raise SystemExit("disasm_fn failed at %08X: %s" % (addr, out.stderr))
    d = {}
    for ln in out.stdout.splitlines():
        m = LINE.match(ln)
        if m: d[int(m.group(1), 16)] = (m.group(3).strip(), m.group(4) or "", m.group(2))
    return d

def same(d, a, text, target=None):
    x = d.get(a)
    if x is None: return False, "no instruction boundary at %08X" % a
    note = x[1][3:] if x[1].startswith("-> ") else x[1]          # disasm_fn writes call targets as "-> XXXXXXXX"
    ok = x[0] == text and (target is None or note.startswith("%08X" % target))
    return ok, "%08X %s ; %s" % (a, x[0], x[1])

def expect(group, d, items):
    for it in items:
        a, text = it[0], it[1]
        tgt = it[2] if len(it) > 2 else None
        ok, got = same(d, a, text, tgt)
        check("%s %08X %s%s" % (group, a, text, (" -> %08X" % tgt) if tgt else ""), ok, got)

img = disasm_fn.Image(disasm_fn.DEFAULT_EXE)
check("image sha256 and base 0x120000", hashlib.sha256(img.d).hexdigest() == EXE_SHA and img.base == 0x120000,
      hex(img.base))

# ---- N: neutral retirement 003FA820..003FA900 (224 B) ------------------------------------------------------------
N = span(0x003FA820, 0x003FA900)
check("N body ends in ret at 003FA8FF", N.get(0x003FA8FF, ("",))[0] == "ret")
expect("N", N, [
    (0x003FA82F, "movzx ebx, word ptr [rcx + 0x272]"), (0x003FA836, "mov esi, edx"),
    (0x003FA83B, "test bl, 1"), (0x003FA83E, "je 0x3fa8f0"),               # not occupied: nothing
    (0x003FA844, "test bl, 2"), (0x003FA847, "jne 0x3fa8f0"),              # already retired: nothing
    (0x003FA84D, "or bx, 2"), (0x003FA851, "mov word ptr [rcx + 0x272], bx"),
    (0x003FA858, "test bl, 8"), (0x003FA85B, "jne 0x3fa861"),
    (0x003FA85D, "test edx, edx"), (0x003FA85F, "je 0x3fa8e0"),            # neutral: straight to the two stores
    (0x003FA8E0, "mov dword ptr [rdi + 0x290], esi"), (0x003FA8E6, "mov dword ptr [rdi + 0x294], 0")])
# the neutral path is 003FA82F..003FA85F then 003FA8E0..003FA8FF: no call and no other store on it
neutral = [a for a in N if a <= 0x003FA85F or a >= 0x003FA8E0]
calls = [a for a in neutral if N[a][0].startswith("call")]
stores = [a for a in neutral if N[a][0].startswith("mov") and re.match(r"mov \w+ ptr \[r(cx|di) ", N[a][0])]
check("N neutral path: no call; object stores exactly 003FA851, 003FA8E0, 003FA8E6",
      not calls and stores == [0x003FA851, 0x003FA8E0, 0x003FA8E6], ([hex(a) for a in calls], [hex(a) for a in stores]))
w = [a for a in N if re.search(r"ptr \[r(cx|di) \+ 0x(260|264|270)\]", N[a][0]) and N[a][0].startswith(("mov", "add", "sub", "or", "and"))]
check("N no instruction of the body writes +0x260, +0x264 or +0x270", not w, [hex(a) for a in w])

# ---- U: local visual update 003FC510..003FC8FD (1005 B) -----------------------------------------------------------
U = span(0x003FC510, 0x003FC8FD)
expect("U", U, [
    (0x003FC5A5, "xor edx, edx"),
    (0x003FC5A7, "movss xmm0, dword ptr [rip + 0x1a01b0d]", 0x01DFE0BC),   # the global frame step
    (0x003FC5AF, "test cl, 0x20"), (0x003FC5B2, "je 0x3fc5ea"),
    (0x003FC5EA, "mulss xmm0, dword ptr [rip + 0x915a5a]", 0x00D1204C),    # x the decline constant
    (0x003FC5F2, "cvttss2si eax, xmm0"), (0x003FC5F6, "add word ptr [rbx + 0x270], ax"),
    (0x003FC5FD, "jns 0x3fc606"), (0x003FC5FF, "mov word ptr [rbx + 0x270], dx"),
    (0x003FC688, "mov ecx, dword ptr [rbx + 0x260]"),                      # one phase handler per call
    (0x003FC68E, "sub ecx, 1"), (0x003FC691, "je 0x3fc80f"),
    (0x003FC697, "sub ecx, 1"), (0x003FC69A, "je 0x3fc7dd"),
    (0x003FC6A0, "cmp ecx, 1"), (0x003FC6A3, "jne 0x3fc8ea"),
    (0x003FC6A9, "cmp word ptr [rbx + 0x270], dx"), (0x003FC6B0, "jg 0x3fc6b8"),   # phase 3: signed fade > 0 skips
    (0x003FC6B2, "mov dword ptr [rbx + 0x260], edx"),                              # phase 3 -> 0
    (0x003FC6B8, "mov edx, dword ptr [rbx + 0x290]"), (0x003FC6BE, "test edx, edx"), (0x003FC6C0, "je 0x3fc8ea"),
    (0x003FC7DD, "movzx eax, word ptr [rbx + 0x272]"), (0x003FC7E4, "test al, 2"), (0x003FC7E6, "je 0x3fc8ea"),
    (0x003FC7EC, "mov dword ptr [rbx + 0x260], 3"),                                # retired phase 2 -> 3
    (0x003FC7F6, "cmp dword ptr [rbx + 0x290], edx"), (0x003FC7FC, "jne 0x3fc8ea"),
    (0x003FC802, "mov ecx, 0xffdf"), (0x003FC807, "and ax, cx"), (0x003FC80A, "jmp 0x3fc8e3"),
    (0x003FC8E3, "mov word ptr [rbx + 0x272], ax"),
    (0x003FC80F, "or word ptr [rbx + 0x272], 0x20"),                               # phase 1 handler entry
    (0x003FC839, "mov dword ptr [rbx + 0x260], 2"), (0x003FC8D5, "mov dword ptr [rbx + 0x260], 2")])
ph = sorted(a for a in U if re.match(r"mov dword ptr \[rbx \+ 0x260\], ", U[a][0]))
check("U the only phase stores are 003FC6B2 (0), 003FC7EC (3), 003FC839 (2), 003FC8D5 (2)",
      ph == [0x003FC6B2, 0x003FC7EC, 0x003FC839, 0x003FC8D5], [hex(a) for a in ph])
# phase 2 -> 3 cannot reach the phase-3 -> 0 store in one call: from 003FC7EC the straight line runs to 003FC7FC's jne
# (to 003FC8EA) or 003FC80A's jmp (to 003FC8E3), both past 003FC6B2, and the tail 003FC8E3..003FC8FC has no backward
# branch (checked here by text).
tail_back = [a for a in U if a >= 0x003FC7EC and U[a][0].split()[0].startswith("j")
             and int(U[a][0].split()[-1], 16) < 0x003FC7EC]
check("U no branch at or after 003FC7EC goes backward (2->3 cannot reach the 3->0 store)", not tail_back,
      [hex(a) for a in tail_back])
dec = struct.unpack("<f", img.read(0x00D1204C, 4))[0]
raw = img.read(0x00D1204C, 4)
check("D 00D1204C = bytes 000000c5 = binary32 -2048.0", raw == b"\x00\x00\x00\xc5" and dec == -2048.0, (raw.hex(), dec))
z = struct.unpack("<f", struct.pack("<f", 0.0 * dec))[0]
check("D frame step +0.0 x -2048.0 is a signed zero that truncates to 0 (fade word unchanged)",
      z == 0.0 and int(z) == 0, z)

# ---- M: manager traversal 003FA790..003FA81F (143 B) --------------------------------------------------------------
M = span(0x003FA790, 0x003FA81F)
expect("M", M, [
    (0x003FA796, "mov rdx, qword ptr [rcx + 0x2490]"),
    (0x003FA7B1, "mov rbx, qword ptr [rdx + 0x278]"),                     # next saved first
    (0x003FA7B8, "cmp dword ptr [rdx + 0x260], esi"), (0x003FA7BE, "jne 0x3fa7cf"),
    (0x003FA7C3, "mov word ptr [rdx + 0x272], si"), (0x003FA7CA, "call 0x3fa4e0", 0x003FA4E0),
    (0x003FA7CF, "mov rdx, rbx"), (0x003FA7D5, "jne 0x3fa7b1"),
    (0x003FA7DC, "mov rbx, qword ptr [rdi + 0x2490]"),                    # second pass from the head again
    (0x003FA7F3, "call 0x3fc510", 0x003FC510), (0x003FA7F8, "call 0x1ede80", 0x001EDE80),
    (0x003FA7FD, "test eax, eax"), (0x003FA7FF, "je 0x3fa80d"), (0x003FA808, "call 0x3fc170", 0x003FC170),
    (0x003FA80D, "mov rbx, qword ptr [rbx + 0x278]"), (0x003FA817, "jne 0x3fa7f0"), (0x003FA81E, "ret")])
check("M recycle loop (003FA7B1..003FA7D5) lies wholly before the update loop (003FA7F0..003FA817)",
      0x003FA7D5 < 0x003FA7F0 and M[0x003FA7D5][0] == "jne 0x3fa7b1" and M[0x003FA817][0] == "jne 0x3fa7f0")

# ---- L: unlink and clear 003FA4E0..003FA567 (135 B) ---------------------------------------------------------------
L = span(0x003FA4E0, 0x003FA567)
expect("L", L, [(0x003FA549, "xor eax, eax"), (0x003FA54B, "mov qword ptr [rdx + 0x278], rax"),
                (0x003FA552, "mov qword ptr [rdx + 0x280], rax"), (0x003FA559, "mov word ptr [rdx + 0x272], ax"),
                (0x003FA560, "mov dword ptr [rdx + 0x260], eax"), (0x003FA566, "ret")])

# ---- G: render gate 001EDE80..001EDEBD (61 B) ---------------------------------------------------------------------
G = span(0x001EDE80, 0x001EDEBD)
expect("G", G, [(0x001EDE8B, "je 0x1edeb3"), (0x001EDE94, "jne 0x1edeb3"), (0x001EDEB3, "mov eax, 1"),
                (0x001EDEBC, "ret")])

# ---- control -------------------------------------------------------------------------------------------------------
ok, got = same(U, 0x003FC6B0, "jge 0x3fc6b8")
check("K1 control: the opposite-signedness release guard (jge for jg) at 003FC6B0 is reported as a mismatch",
      not ok, got)
print("FAILS", fails)
