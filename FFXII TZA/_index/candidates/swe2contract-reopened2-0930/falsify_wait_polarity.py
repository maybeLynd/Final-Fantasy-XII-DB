"""falsify_wait_polarity.py - falsification pass 2026-10-01 (SWE2-CONTRACT for OPUS) on
04-Actor-Entity/the-field-runtime-pass.md. Static. Reads only.

Attacked claim (the page's most load-bearing one, and the one that reopened it): section 11's SECTION-12 wait-completion
polarity table for the wait resolver WorldActor_UpdateRuntimeAndScriptExecutionState 0025DF00 - which wait kind runs
which predicate, which result holds the wait and which completes it, which kinds set the wait slot's +0x27, that
0025E127 is the blocked (no-interpreter) exit and 0025E0BE the interpreter arm - together with the bound sections 8 and
9 draw from it: one 0025DF00 call dispatches at most twice. Also checked, because the same pass read it: section 11's
early movement path (the steering mode passed to Movement_SetRequestedSpeed 0026D6F0).

Every check prints PASS or FAIL (LIMIT lines state what a check does not cover and are not counted). The positive
controls run the table decoder and the store census on corrupted copies and must FAIL there. Last line: FAILS n.
"""
import hashlib, io, os, struct, sys
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "swe2contract-ddres-b1-0930"))
import block_writer_disjoint as b  # noqa: E402  (PE section mapper and functions.tsv extents)

SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x00120000
FN, FN_SIZE, FN_INSNS, FN_RET = 0x0025DF00, 1228, 329, 0x0025E3CB
HEAD, BLOCKED, INTERP_ARM, INTERP = 0x0025DFA0, 0x0025E127, 0x0025E0BE, 0x0025E4C0
PAGE_TABLE = {0: BLOCKED, 1: INTERP_ARM, 2: INTERP_ARM, 3: 0x0025E027, 4: 0x0025E091, 5: 0x0025E00A,
              6: 0x0025E058, 7: 0x0025E083}

fails = 0


def check(cid, ok, what):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", cid, what))
    if not ok:
        fails += 1


exe = io.open(b.EXE, "rb").read()
check("W0", hashlib.sha256(exe).hexdigest() == SHA, "image is the certified FFXII_TZA.exe 73461d08...")
at = b.load()
ext = b.extents()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
size = ext.get(FN)
ins = list(md.disasm(at(FN, size or FN_SIZE), FN)) if size else []
by = {i.address: i for i in ins}
nxt = {ins[k].address: ins[k + 1] for k in range(len(ins) - 1)}


def t(a):
    i = by.get(a)
    return "%s %s" % (i.mnemonic, i.op_str) if i else "<none>"


def seq(a, n):
    out, i = [], by.get(a)
    while i is not None and len(out) < n:
        out.append("%s %s" % (i.mnemonic, i.op_str))
        i = nxt.get(i.address)
    return out


# W1 extent
check("W1", size == FN_SIZE and len(ins) == FN_INSNS and ins and ins[-1].address == FN_RET and
      ins[-1].mnemonic == "ret", "0025DF00 is %s B, %d instructions, last %s at %08X (page: 329 instructions, ret at "
      "0025E3CB)" % (size, len(ins), ins[-1].mnemonic if ins else "-", ins[-1].address if ins else 0))
leaves = [i for i in ins if i.group(capstone.CS_GRP_JUMP) and i.operands[0].type == X.X86_OP_IMM and
          not (FN <= i.operands[0].imm < FN + FN_SIZE)]
check("W1b", not leaves, "no direct jump leaves the extent (%d found)" % len(leaves))

# W2 the dispatch: r14 = image base, movzx eax, byte [rsi+0x14]; cmp eax, 7; ja 0025E127; RVA table at 0025E3CC
l = by.get(0x0025DF88)
r14 = l.address + l.size + l.operands[1].mem.disp if l is not None and l.mnemonic == "lea" else None
mv = by.get(0x0025DFFD)
tab = (r14 + mv.operands[1].mem.disp) if (r14 is not None and mv is not None) else None
ok = r14 == BASE and t(0x0025DFF0) == "movzx eax, byte ptr [rsi + 0x14]" and t(0x0025DFF4) == "cmp eax, 7" and \
    t(0x0025DFF7) == "ja 0x25e127" and tab == 0x0025E3CC and t(0x0025E008) == "jmp rcx"
check("W2", ok, "0025DF88 r14 = %s; dispatch on byte [rsi+0x14], cmp 7, ja 0025E127; table at %s (page: 0025E3CC, "
      "kind >= 8 -> no interpreter arm)" % ("%08X" % r14 if r14 is not None else "?",
                                            "%08X" % tab if tab is not None else "?"))


def decode_table(raw):
    return {k: BASE + v for k, v in enumerate(struct.unpack("<8I", raw))}


raw = at(0x0025E3CC, 32)
dt = decode_table(raw)
check("W3", dt == PAGE_TABLE, "kinds -> arms: %s (page: 0->0025E127 1/2->0025E0BE 3->0025E027 4->0025E091 "
      "5->0025E00A 6->0025E058 7->0025E083)" % " ".join("%d->%08X" % kv for kv in sorted(dt.items())))

# W4 kind 3: 003DBF60; result != 0xFF (an entry found) holds; 0xFF completes and sets +0x14 = 1 and +0x27 = 1
ok = "call 0x3dbf60" in seq(0x0025E027, 7) and t(0x0025E040) == "cmp eax, 0xff" and \
    t(0x0025E045) == "jne 0x25e127" and seq(0x0025E04B, 3) == ["mov byte ptr [rsi + 0x14], 1",
                                                                "mov byte ptr [rsi + 0x27], 1", "jmp 0x25dfa0"]
check("W4", ok, "kind 3: 003DBF60 finds an entry -> 0025E127 (holds); 0xFF -> +0x14=1, +0x27=1, back to 0025DFA0")

# W5 kind 4: 003DC050; 0xFF (no notification) holds; found -> 003DB2A0 removes it, +0x14 = 1, +0x27 untouched
ok = "call 0x3dc050" in seq(0x0025E091, 6) and t(0x0025E0A4) == "cmp eax, 0xff" and t(0x0025E0A9) == "je 0x25e127" \
    and seq(0x0025E0AB, 5) == ["mov edx, eax", "mov rcx, rdi", "call 0x3db2a0", "mov byte ptr [rsi + 0x14], 1",
                               "jmp 0x25dfa0"]
check("W5", ok, "kind 4: 003DC050 finds none -> 0025E127 (holds); found -> 003DB2A0(record, index), +0x14=1, no +0x27 "
      "store, back to 0025DFA0")

# W6 kind 5: 002674B0(slot, wait+0x18) non-zero holds; zero -> +0x14 = 1, +0x27 untouched
ok = seq(0x0025E00A, 7) == ["lea rdx, [rsi + 0x18]", "mov rcx, r15", "call 0x2674b0", "test eax, eax",
                            "jne 0x25e127", "mov byte ptr [rsi + 0x14], 1", "jmp 0x25dfa0"]
check("W6", ok, "kind 5: 002674B0 non-zero -> 0025E127 (holds); zero -> +0x14=1, no +0x27 store")

# W7 kind 6: 003DB640(entry, channel byte +0x26) non-zero holds; zero -> +0x14 = 1, +0x27 = 1
ok = "call 0x3db640" in seq(0x0025E058, 6) and t(0x0025E05B) == "movzx ebx, byte ptr [rsi + 0x26]" and \
    seq(0x0025E06E, 5) == ["test eax, eax", "jne 0x25e127", "mov byte ptr [rsi + 0x14], 1",
                           "mov byte ptr [rsi + 0x27], 1", "jmp 0x25dfa0"]
check("W7", ok, "kind 6: 003DB640 bit set -> 0025E127 (holds); clear -> +0x14=1, +0x27=1")

# W8 kind 7: 00267420(slot, wait+0x18) then jmp 0025E06E, kind 6's test and stores
ok = seq(0x0025E083, 4) == ["lea rdx, [rsi + 0x18]", "mov rcx, r15", "call 0x267420", "jmp 0x25e06e"]
check("W8", ok, "kind 7: 00267420 then 0025E08F jmp 0025E06E into kind 6's tail (shares the +0x27 store)")

# W9 0025E127 is the blocked exit: sets wait +0x16 = 1 and falls forward to 0025E12B; no interpreter call
ok = t(BLOCKED) == "mov byte ptr [rsi + 0x16], 1" and nxt[BLOCKED].address == 0x0025E12B
check("W9", ok, "0025E127 mov byte [rsi+0x16], 1 then 0025E12B (the blocked / no-interpreter exit, request+16)")

# W10 0025E0BE is the interpreter arm: 0025E4C0(slot r15, record rdi, wait slot rsi)
ok = seq(0x0025E0CA, 4) == ["mov r8, rsi", "mov rdx, rdi", "mov rcx, r15", "call 0x25e4c0"]
check("W10", ok, "0025E0BE arm calls 0025E4C0 at 0025E0D3 with (r15 slot, rdi record, rsi wait slot)")

# W11 the store census inside the body: byte stores to [rsi + 0x27] and the "= 1" stores to [rsi + 0x14]


def stores(lst, disp):
    out = []
    for i in lst:
        if i.mnemonic != "mov" or len(i.operands) != 2 or i.operands[0].type != X.X86_OP_MEM:
            continue
        m = i.operands[0].mem
        if m.base == X.X86_REG_RSI and m.index == 0 and m.disp <= disp < m.disp + i.operands[0].size:
            out.append(i)
    return out


s27 = [i.address for i in stores(ins, 0x27)]
s14 = [i.address for i in stores(ins, 0x14) if i.operands[1].type == X.X86_OP_IMM and i.operands[1].imm == 1]
check("W11", s27 == [0x0025E04F, 0x0025E07A], "stores covering wait +0x27: %s (page: kinds 3 and 6/7 only, 0025E04F "
      "and 0025E07A)" % " ".join("%08X" % a for a in s27))
check("W11b", s14 == [0x0025E01E, 0x0025E04B, 0x0025E076, 0x0025E0B5],
      "'= 1' stores to wait +0x14: %s (page: four, at completing transitions)" % " ".join("%08X" % a for a in s14))

# W12 at most two dispatches per call: every back-edge to the loop head follows a "+0x14 = 1" store, and nothing at or
# after the interpreter arm branches back before it
back = [i for i in ins if i.group(capstone.CS_GRP_JUMP) and i.operands[0].type == X.X86_OP_IMM and
        i.operands[0].imm == HEAD]
prev = {ins[k + 1].address: ins[k] for k in range(len(ins) - 1)}


def block_before(a, n=3):
    """up to n straight-line instructions ending just before a (stops at a branch or a branch target)."""
    targets = {x.operands[0].imm for x in ins if x.group(capstone.CS_GRP_JUMP) and x.operands and
               x.operands[0].type == X.X86_OP_IMM}
    out, cur = [], prev.get(a)
    while cur is not None and len(out) < n and not cur.group(capstone.CS_GRP_JUMP):
        out.append("%s %s" % (cur.mnemonic, cur.op_str))
        if cur.address in targets:
            break
        cur = prev.get(cur.address)
    return out


pre_ok = all("mov byte ptr [rsi + 0x14], 1" in block_before(i.address) for i in back)
late = [i for i in ins if i.address >= INTERP_ARM and i.group(capstone.CS_GRP_JUMP) and
        i.operands[0].type == X.X86_OP_IMM and HEAD <= i.operands[0].imm < INTERP_ARM]
ind = [i for i in ins if i.group(capstone.CS_GRP_JUMP) and i.operands[0].type != X.X86_OP_IMM]
head_writes = [i for i in stores([x for x in ins if HEAD <= x.address < 0x0025DFFD], 0x14)]
check("W12", len(back) == 4 and pre_ok and not late and len(ind) == 1 and not head_writes,
      "%d back-edges to 0025DFA0, each right after '+0x14 = 1'; %d branches from the interpreter arm onward re-enter "
      "the dispatch; the one indirect jump is the dispatch; the loop head stores nothing to +0x14 -> a second dispatch "
      "reads kind 1 and takes the interpreter arm, which only exits (at most two dispatches)" % (len(back), len(late)))

# The re-dispatch re-reads the wait slot index from record +0x11 (0025DFB6). Census of stores covering +0x11 (any
# non-stack, non-rip base) in the direct closure of every callee the arms and the loop head call.
roots = sorted({i.operands[0].imm for i in ins if i.mnemonic == "call" and i.operands[0].type == X.X86_OP_IMM and
                HEAD <= i.address < INTERP_ARM})
seen, stack, hits11 = set(), list(roots), []
while stack:
    f = stack.pop()
    if f in seen or f not in ext:
        continue
    seen.add(f)
    for i in md.disasm(at(f, ext[f]), f):
        if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X.X86_OP_IMM:
            tt = i.operands[0].imm
            if tt in ext and not (f <= tt < f + ext[f]):
                stack.append(tt)
        if not i.operands or i.operands[0].type != X.X86_OP_MEM or len(i.operands) < 2:
            continue
        if i.mnemonic.startswith(("cmp", "test", "ucomi", "comi", "bt")):
            continue
        m = i.operands[0].mem
        if m.base in (X.X86_REG_RIP, X.X86_REG_RSP, 0):
            continue
        if m.disp <= 0x11 < m.disp + i.operands[0].size:
            hits11.append((f, i.address, i.operands[0].size))
byte11 = sorted({f for f, a, s in hits11 if s == 1})
wide11 = sorted({f for f, a, s in hits11 if s > 1})
check("W12b", sorted(roots) == [0x001ED180, 0x001EDDA0, 0x001EDE80, 0x0020E600, 0x00267420, 0x002674B0, 0x003DB2A0,
                                 0x003DB640, 0x003DBF60, 0x003DC050] and len(seen) > len(roots),
      "the loop head and the arms call %d functions; their direct closure is %d functions" % (len(roots), len(seen)))
print("LIMIT W12 a callee that rewrote record +0x11 would make the re-dispatch read another wait slot. In the closure, "
      "byte stores covering +0x11 are in %s (read here: each base is a 0x14-stride resource entry, not the record); "
      "wider stores covering it are in %s, whose bases are not typed here. Indirect calls are not followed."
      % (" ".join("%08X" % f for f in byte11), " ".join("%08X" % f for f in wide11)))

# W13 section 11's early movement path: the mode passed to Movement_SetRequestedSpeed 0026D6F0
one = struct.unpack("<f", at(0x01DFE0BC, 4))[0]
ok_shape = seq(0x0025DF6F, 6) == ["mov r8d, 2", "comiss xmm2, xmm0", "mov rcx, rdi", "mulss xmm1, xmm2",
                                  "cmova r8d, ebp", "call 0x26d6f0"] and t(0x0025DF1F) == "xor ebp, ebp" and \
    t(0x0025DF64) == "xorps xmm0, xmm0" and t(0x0025DF5F) == "movss xmm2, dword ptr [rcx + 0x7c]"
check("W13a", ok_shape and one == 1.0, "0025DF6F-0025DF83: r8d = 2; comiss speed(+0x7C), 0.0; cmova r8d, ebp (ebp = 0); "
      "speed scaled by [01DFE0BC] = %r" % one)
# Execute the image's own bytes for "mov r8d, 2 ; comiss xmm2, xmm0 ; cmova r8d, ebp" under Unicorn, xmm0 = 0.0
# (0025DF64 xorps), ebp = 0 (0025DF1F), for four speeds. The two non-branching instructions between them
# (mov rcx, rdi ; mulss xmm1, xmm2) touch neither the flags nor r8d and are executed too.
import unicorn
from unicorn import x86_const as U


def mode_for(speed):
    lo, hi = 0x0025DF6F, 0x0025DF83
    code = at(lo, hi - lo)
    mu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    page = lo & ~0xFFF
    mu.mem_map(page, 0x2000)
    mu.mem_write(lo, code)
    mu.reg_write(U.UC_X86_REG_RBP, 0)
    mu.reg_write(U.UC_X86_REG_XMM0, 0)
    mu.reg_write(U.UC_X86_REG_XMM1, struct.unpack("<I", struct.pack("<f", 1.0))[0])
    mu.reg_write(U.UC_X86_REG_XMM2, struct.unpack("<I", struct.pack("<f", speed))[0])
    mu.emu_start(lo, hi)
    return mu.reg_read(U.UC_X86_REG_R8) & 0xFFFFFFFF


modes = {s: mode_for(s) for s in (1.5, 0.0, -1.5, float("nan"))}
check("W13b", list(modes.values()) == [0, 2, 2, 2],
      "executed: speed 1.5 -> mode %d, 0.0 -> %d, -1.5 -> %d, NaN -> %d (mode 0 when the speed is positive, 2 "
      "otherwise)" % tuple(modes.values()))
print("BROKEN-ON-PAGE W13 the page's section 11 sentence 'with mode 2 when that speed is positive and 0 otherwise' "
      "inverts this; it is struck and corrected on the page 2026-10-01 (not counted: the check above is the measurement)")

# Positive controls
bad = bytearray(raw); bad[4 * 3:4 * 3 + 4] = struct.pack("<I", 0x0025E0BE - BASE)  # kind 3 -> interpreter arm
check("C1", decode_table(bytes(bad)) != PAGE_TABLE, "control: kind 3's entry repointed to 0025E0BE -> W3's comparison "
      "fails on the copy")
extra = list(ins)
fake = list(md.disasm(b"\xc6\x46\x27\x01", 0x0025E0B5))  # mov byte ptr [rsi + 0x27], 1 planted in kind 4's arm
check("C2", [i.address for i in stores(fake, 0x27)] == [0x0025E0B5] and
      len(stores(extra, 0x27)) + 1 != 2, "control: a planted 'mov byte [rsi+0x27], 1' is seen by the census (W11 "
      "would read three sites)")
wide = list(md.disasm(b"\xc7\x46\x24\x00\x00\x00\x00", 0x0025E000))  # mov dword ptr [rsi + 0x24], 0 covers +0x27
check("C3", len(stores(wide, 0x27)) == 1, "control: a dword store at +0x24 is counted as covering +0x27")

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
