"""check_s38.py - FABLE, 2026-10-03: the render pool's shared flag word (tail +0x18 = pool +0x48818) and its owners
outside the pool family.

Settles, at the bytes of the certified image (73461d08..., base 0x00120000), the claims of section.txt (section 14a,
invariants 6-10):

  K1  raw census of the word: every .text instruction whose displacement lies in 0x48818..0x4881B (any base register,
      any width) - exactly 25 sites in 12 functions; no access of a wider operand from 0x48800..0x48817 covers it; no
      lea/add/sub/immediate forms a biased base anywhere in 0x48800..0x4881B; the pool pointer's one mirror 02EBB740
      is written twice and never read.
  K2  the bit algebra of the 19 writes: after the constructor's zero store, every write sets only bits 0, 2, 4, 5,
      bit 2 is cleared by no write after construction, and the two plain stores carry what section.txt says.
  K3  the owners and their routes (raw index, all forms): 002E8700 <- 0025D950 <- 00314020; 002E8CC0 <- 002628B0
      right after 002E63C0; 002EBBB0 <- 0026A470 <- 00347830; 002EBBF0 <- 00226280 (requester 1, bit 35);
      0042ED30 <- 002E8050 <- 0026C8C0; 002E63C0 <- 002628B0, 00266D10; the veto byte 0215FD56 has three writers;
      retire and promote have one caller each, 0042ED60, between its bit-5 clear and its bit-5 test; bit 4's source
      byte 02099DA3 is written by 0025D950 alone, and its override pair 02099DA4/02099DA5 by 0026AB50 (verbs 0552 /
      0553), the area unload and the area reset (K3e).
  K4  the readers: bit 0 x3 and bit 4 in 0042E850, bit 2 in 0042CF70 and 0042D050, bit 5 in 0042ED60; the two bit-2
      readers receive the pool base as their second argument from 00425FB0 (registrations 004264A0 / 00426500).
  K5  static closures: nothing directly reachable from the promotion callee 0042C410 touches the word or the veto
      byte; nothing directly reachable from the constructor reaches the per-record walker 00425FB0.
  K6  orders, by dominance in one body: 0026CAC0 on every path of 0026C8C0; 002265D6 on every path of 00226280 past
      its dirty gate; 00426C59 after 00426A00 on every path of 004269A0; 00314346 before 00314020's only ret.
  K7  executed (Unicorn 2.1.4, original code):
        a. the veto mask: two requesters, bit 0 follows (byte == 0), other bits kept;
        b. 0042ED30 sets bit 0 over a held veto, and 002E8CC0 then clears it;
        c. 002E63C0 drops every veto without touching bit 0, and 002E8CC0 then sets it;
        d. 002E8700(x) makes bit 4 = (x != 0) and keeps the other bits;
        e. promotion's pin (00428790..004287BD): the callee sees bit 0 clear, bit 0 returns to its PRE value, the
           callee's change to bit 2 survives;
        f. 0042CF70 whole (callees answered by hooks): instance +8 bit 1 is set only for flag bit 2 AND child bit 23
           AND parent bit 23, cleared otherwise;
        g. 0042ED60 whole (callees answered by hooks): the rebuild 0041E500 runs exactly when retire or promote set
           bit 5 in this pass; a bit 5 left over from before is ignored.

Sensitivity controls (each must make a check FAIL; the control PASSES when it does):
  S1  image: 002EBC1E jne -> je: K7a must fail.
  S2  image: 0042ED37 `or ..., 5` -> `or ..., 4`: K7b must fail.
  S3  image: 004287B4 `and eax, 1` -> `and eax, 5`: K7e must fail.
  S4  image: 0042D004 `test byte ..., 4` -> `test byte ..., 1`: K7f must fail.
  S5  image: 0042ED83 `and ..., ~0x20` NOPed: K7g must fail.
  S6  claim: "bit 2 is never read" (the field row and the record-array page) checked against K1 must fail.

Prints FAILS N last.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from s38lib import Img, text_refs, data_refs, disp_sweep, root_of, body, pdata_roots, txt, sec  # noqa: E402
from rawref import decode_fn, text_array, _i32  # noqa: E402
import numpy as np  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, __version__ as UC_VERSION  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RSP, UC_X86_REG_RIP,  # noqa: E402
                               UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_RBX, UC_X86_REG_R8, UC_X86_REG_R9)

sys.path.insert(0, os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Body  # noqa: E402

POOLPTR = 0x022C6F28
MIRROR = 0x02EBB740
VETO = 0x0215FD56
FLAGS = 0x48818
STACK = 0x0F000000
POOL = 0x10000000
INST = 0x10100000
MAGIC = 0x0FF00000

fails = 0
quiet = [False]


def report(tag, ok, text=""):
    global fails
    if not ok:
        fails += 1
    if not quiet[0]:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))
    return ok


def note(s):
    if not quiet[0]:
        print("      " + s)


def leaf_entry(img, site):
    """Entry of the leaf (outside .pdata) holding site: a 16-aligned start after int3 padding whose linear decode
    reaches site at an instruction boundary."""
    a = site & ~0xF
    for _ in range(0x40):
        if img.read(a - 1, 1) == b"\xCC":
            for ci in img.cs.disasm(img.read(a, site - a + 16), a):
                if ci.address == site:
                    return a
                if ci.address > site:
                    break
        a -= 0x10
    return None


def func_of(img, site):
    r = root_of(img, site)
    return r if r is not None else leaf_entry(img, site)


def insn(img, va):
    return next(img.cs.disasm(img.read(va, 16), va, 1))


# ------------------------------------------------------------------------------------------------ K1: the census
EXPECT_SITES = {
    0x002E8707: ("002E8700", "and dword ptr [rax + 0x48818], 0xffffffef"),
    0x002E871C: ("002E8700", "or dword ptr [rdx + 0x48818], eax"),
    0x002E8CD0: ("002E8CC0", "or dword ptr [rax + 0x48818], 1"),
    0x002E8CD8: ("002E8CC0", "and dword ptr [rax + 0x48818], 0xfffffffe"),
    0x002EBBD2: ("002EBBB0", "or dword ptr [rax + 0x48818], 1"),
    0x002EBBDA: ("002EBBB0", "and dword ptr [rax + 0x48818], 0xfffffffe"),
    0x002EBC20: ("002EBBF0", "or dword ptr [rax + 0x48818], 1"),
    0x002EBC28: ("002EBBF0", "and dword ptr [rax + 0x48818], 0xfffffffe"),
    0x00426A00: ("004269A0", "mov dword ptr [rsi + 0x48818], ebx"),
    0x00426C59: ("004269A0", "or dword ptr [rax + 0x48818], 5"),
    0x00427DB3: ("00427C90", "or dword ptr [rdi + 0x48818], 0x20"),
    0x00428790: ("00428710", "mov ebx, dword ptr [rdi + 0x48818]"),
    0x004287A1: ("00428710", "mov dword ptr [rdi + 0x48818], eax"),
    0x004287AC: ("00428710", "mov eax, dword ptr [rdi + 0x48818]"),
    0x004287B7: ("00428710", "xor dword ptr [rdi + 0x48818], eax"),
    0x00428863: ("00428710", "or dword ptr [rdi + 0x48818], 0x20"),
    0x0042D004: ("0042CF70", "test byte ptr [rsi + 0x48818], 4"),
    0x0042D3A2: ("0042D050", "test byte ptr [r14 + 0x48818], 4"),
    0x0042EA43: ("0042E850", "test byte ptr [rsi + 0x48818], 1"),
    0x0042EA6C: ("0042E850", "test byte ptr [rsi + 0x48818], 1"),
    0x0042EAB1: ("0042E850", "test byte ptr [rsi + 0x48818], 1"),
    0x0042EB79: ("0042E850", "test byte ptr [rsi + 0x48818], 0x10"),
    0x0042ED37: ("0042ED30", "or dword ptr [rax + 0x48818], 5"),
    0x0042ED83: ("0042ED60", "and dword ptr [rbx + 0x48818], 0xffffffdf"),
    0x0042ED94: ("0042ED60", "test byte ptr [rbx + 0x48818], 0x20"),
}
OUTSIDE = ("002E8700", "002E8CC0", "002EBBB0", "002EBBF0", "0042ED30", "0042ED60", "0042CF70", "0042D050", "0042E850")
FAMILY = ("004269A0", "00427C90", "00428710")


def census(img):
    got = {}
    for d in range(FLAGS, FLAGS + 4):
        for r in disp_sweep(img, d):
            f = func_of(img, r[0])
            got[r[0]] = ("%08X" % f if f else "--------", r[1], r[2])
    return got


def k1(img):
    got = census(img)
    for s in sorted(got):
        note("%08X  fn=%s  w%d  %s" % (s, got[s][0], got[s][2], got[s][1]))
    ok = {s: (g[0], g[1]) for s, g in got.items()} == EXPECT_SITES
    fns = sorted(set(g[0] for g in got.values()))
    report("K1a", ok and len(got) == 25 and len(fns) == 12,
           "%d sites in %d functions at displacement 0x48818..0x4881B, as listed: %s" % (len(got), len(fns), fns))
    widths = sorted(set((g[2], g[1].split()[0]) for g in got.values()))
    report("K1b", all((w == 4) or (w == 1 and m == "test") for w, m in widths),
           "every write and plain load is a dword; the byte accesses are `test` only: %s" % widths)
    cover = []
    for d in range(0x48800, FLAGS):
        for r in disp_sweep(img, d):
            if d + r[2] > FLAGS:
                cover.append("%08X %s" % (r[0], r[1]))
    report("K1c", not cover, "no wider operand from +0x48800..+0x48817 covers the word %s" % cover)
    tva, a = text_array(img)
    n = len(a) - 3
    dd = _i32(a, n)
    biased = []
    for i in np.nonzero((dd >= 0x48800) & (dd < FLAGS + 4))[0]:
        site = int(tva + i)
        pd, ins = decode_fn(img, site)
        cands = []
        if ins is None:
            le = leaf_entry(img, site)
            if le is not None:
                cands = [ci for ci in img.cs.disasm(img.read(le, site - le + 16), le)]
        else:
            cands = [ins.get(site - b) for b in range(1, 15) if ins.get(site - b) is not None]
        hit = None
        for ci in cands:
            if ci.address < site < ci.address + ci.size:
                hit = ci
        if hit is None:
            continue
        for op in hit.operands:
            v = None
            if op.type == X86_OP_IMM:
                v = op.imm & 0xFFFFFFFF
            elif op.type == X86_OP_MEM and hit.mnemonic == "lea":
                v = op.mem.disp & 0xFFFFFFFF
            if v is not None and 0x48800 <= v < FLAGS + 4:
                biased.append("%08X %s" % (hit.address, txt(hit)))
    report("K1d", not biased, "no lea / immediate in 0x48800..0x4881B forms a biased base or an address %s" % biased)
    mir = text_refs(img, MIRROR, MIRROR + 8)[0]
    mtxt = [(r["site"], r["text"]) for r in mir]
    report("K1e", [m[0] for m in mtxt] == [0x004260D1, 0x0042ED6D] and all(t.startswith("mov qword ptr [rip") for _, t in mtxt)
           and not data_refs(img, MIRROR, MIRROR + 8),
           "the pool pointer's mirror 02EBB740 is written at 004260D1 and 0042ED6D and read nowhere: %s"
           % ["%08X %s" % m for m in mtxt])
    return ok


# ------------------------------------------------------------------------------------------------ K2: bit algebra
def k2(img):
    got = census(img)
    sets, clears, bad = set(), set(), []
    for s, (f, t, w) in sorted(got.items()):
        ci = insn(img, s)
        m = ci.mnemonic
        if m in ("test",) or (m == "mov" and ci.operands[0].type != X86_OP_MEM):
            continue
        imm = ci.operands[1].imm & 0xFFFFFFFF if ci.operands[1].type == X86_OP_IMM else None
        if m == "or" and imm is not None:
            sets |= set(b for b in range(32) if imm >> b & 1)
        elif m == "and" and imm is not None:
            clears |= set(b for b in range(32) if not imm >> b & 1)
        elif s == 0x002E871C:          # or [rdx+..], eax with eax = (-(ecx != 0)) & 0x10
            seq = [txt(insn(img, x)) for x in (0x002E8715, 0x002E8717, 0x002E8719)]
            if seq != ["neg ecx", "sbb eax, eax", "and eax, 0x10"]:
                bad.append(("002E871C", seq))
            sets.add(4)
        elif s == 0x004287A1:          # mov [..], eax with eax = PRE & ~1
            seq = [txt(insn(img, x)) for x in (0x00428790, 0x00428799, 0x0042879E)]
            if seq != ["mov ebx, dword ptr [rdi + 0x48818]", "mov eax, ebx", "and eax, 0xfffffffe"]:
                bad.append(("004287A1", seq))
            clears.add(0)
        elif s == 0x004287B7:          # xor [..], eax with eax = (POST ^ PRE) & 1
            seq = [txt(insn(img, x)) for x in (0x004287AC, 0x004287B2, 0x004287B4)]
            if seq != ["mov eax, dword ptr [rdi + 0x48818]", "xor eax, ebx", "and eax, 1"]:
                bad.append(("004287B7", seq))
            sets.add(0)
            clears.add(0)
        elif s == 0x00426A00:          # the constructor's zero store
            between = [ci2 for ci2 in body(img, 0x004269A0) if 0x004269DF < ci2.address < 0x00426A00]
            if txt(insn(img, 0x004269DF)) != "xor ebx, ebx" or any(
                    ci2.operands and ci2.operands[0].type != X86_OP_MEM and "bx" in ci2.op_str.split(",")[0]
                    for ci2 in between):
                bad.append(("00426A00", "ebx not provably 0"))
        else:
            bad.append(("%08X" % s, txt(ci)))
    report("K2a", sets == {0, 2, 4, 5} and not bad,
           "after the constructor's zero store (00426A00, ebx = 0 from 004269DF) the writes set only bits %s %s"
           % (sorted(sets), bad))
    report("K2b", 2 not in clears, "bit 2 is cleared by no write except the constructor's zero store (cleared: %s)"
           % sorted(clears))
    return sets == {0, 2, 4, 5} and 2 not in clears and not bad


# ------------------------------------------------------------------------------------------------ K3: owners, routes
def callers(img, va):
    return [(r["site"], r["form"]) for r in text_refs(img, va)[0]]


def k3(img):
    want = {
        0x002E8700: [(0x0025D9B8, "jmp")],
        0x0025D950: [(0x00314346, "call")],
        0x002E8CC0: [(0x00262B85, "call")],
        0x002EBBB0: [(0x0026A470, "jmp")],
        0x0026A470: [(0x00347842, "jmp")],
        0x002EBBF0: [(0x002265D6, "call")],
        0x0042ED30: [(0x002E8050, "jmp")],
        0x002E8050: [(0x0026CAC0, "call")],
        0x002E63C0: [(0x00262B80, "call"), (0x00266DBF, "call")],
        0x00427C90: [(0x0042ED8A, "call")],
        0x00428710: [(0x0042ED8F, "call")],
        0x004269A0: [(0x00332641, "call")],
        0x0042ED60: [(0x003326B6, "jmp")],
    }
    bad = {}
    for f, w in want.items():
        g = callers(img, f)
        ptr = [d for d in data_refs(img, f) if d[2] == "va64"]
        if g != w or ptr:
            bad["%08X" % f] = (["%08X %s" % x for x in g], ptr)
    report("K3a", not bad, "every owner's callers, raw index (E8/E9, 0F 8x, EB/7x, rip, [reg+RVA], 8-byte pointers): "
           "002E8700<-0025D9B8<-00314346; 002E8CC0<-00262B85; 002EBBB0<-0026A470<-00347842; 002EBBF0<-002265D6; "
           "0042ED30<-002E8050<-0026CAC0; 002E63C0<-00262B80,00266DBF; retire<-0042ED8A, promote<-0042ED8F; "
           "ctor<-00332641; 0042ED60<-003326B6 %s" % bad)
    roots = {s: "%08X" % func_of(img, s) for s in (0x00314346, 0x00262B85, 0x00262B80, 0x00266DBF, 0x00347842,
                                                     0x002265D6, 0x0026CAC0, 0x0042ED8A, 0x003326B6, 0x00332641)}
    report("K3b", roots == {0x00314346: "00314020", 0x00262B85: "002628B0", 0x00262B80: "002628B0",
                            0x00266DBF: "00266D10", 0x00347842: "00347830", 0x002265D6: "00226280",
                            0x0026CAC0: "0026C8C0", 0x0042ED8A: "0042ED60", 0x003326B6: "00332660",
                            0x00332641: "003325D0"},
           "call sites lie in 00314020, 002628B0 (x2), 00266D10, 00347830, 00226280, 0026C8C0, 0042ED60, 00332660, "
           "003325D0 %s" % roots)
    vt = text_refs(img, VETO, VETO + 1)[0]
    vw = [(r["site"], r["text"]) for r in vt]
    want_v = [(0x002E63C0, "mov byte ptr [rip + 0x1e7998f], 0"), (0x002E8CC0, "cmp byte ptr [rip + 0x1e7708f], 0"),
              (0x002EBBB0, "movzx eax, byte ptr [rip + 0x1e7419f]"), (0x002EBBC1, "mov byte ptr [rip + 0x1e7418f], al"),
              (0x002EBBF0, "movzx eax, byte ptr [rip + 0x1e7415f]"), (0x002EBC0F, "mov byte ptr [rip + 0x1e74141], al")]
    report("K3c", vw == want_v and not data_refs(img, VETO, VETO + 1),
           "the veto byte 0215FD56: writers 002E63C0 (zero), 002EBBC1, 002EBC0F; readers 002E8CC0, 002EBBB0, 002EBBF0 "
           "only %s" % (["%08X %s" % x for x in vw] if vw != want_v else ""))
    seq = {0x00262B80: "call 0x2e63c0", 0x00262B85: "call 0x2e8cc0", 0x00266DBF: "call 0x2e63c0",
           0x00266DC4: "call 0x2ef2d0", 0x002265CC: "mov ecx, 1", 0x002265C8: "shr rbx, 0x23", 0x002265D1: "and ebx, 1",
           0x002265D4: "mov edx, ebx", 0x00347837: "call 0x267e10", 0x0034783C: "mov ecx, eax",
           0x0025D9AA: "movsx ecx, dl", 0x0025D9AD: "mov byte ptr [rip + 0x1e3c3f0], dl",
           0x0042ED83: "and dword ptr [rbx + 0x48818], 0xffffffdf", 0x0042ED8A: "call 0x427c90",
           0x0042ED8F: "call 0x428710", 0x0042ED94: "test byte ptr [rbx + 0x48818], 0x20", 0x0042ED9B: "je 0x42edee",
           0x0042EDAB: "call 0x41e500"}
    # bit 4's inputs: byte 02099DA3 (computed by 0025D950 alone) and the override pair 02099DA4 / 02099DA5
    src = {}
    for a in (0x02099DA3, 0x02099DA4, 0x02099DA5):
        src[a] = [(r["site"], "w" if r["text"].startswith("mov byte ptr [rip") else "r") for r in text_refs(img, a, a + 1)[0]]
    want_src = {0x02099DA3: [(0x0025D958, "w"), (0x0025D976, "r"), (0x0025D980, "w"), (0x0025D98B, "r"),
                             (0x0025D9AD, "w"), (0x00263FB0, "r")],
                0x02099DA4: [(0x0025D99E, "r"), (0x00262A24, "w"), (0x00266D47, "w"), (0x0026AB50, "w")],
                0x02099DA5: [(0x0025D994, "r"), (0x00262A2B, "w"), (0x00266D4E, "w"), (0x0026AB56, "w")]}
    ov = callers(img, 0x0026AB50)
    ovshape = [txt(insn(img, a)) for a in (0x0035603C, 0x0035603E, 0x003563C0, 0x003563C2, 0x0026292A)]
    report("K3e", src == want_src and ov == [(0x00356047, "jmp"), (0x003563C4, "jmp")] and ovshape == [
        "mov edx, eax", "mov ecx, 1", "xor edx, edx", "xor ecx, ecx", "xor ebp, ebp"],
        "bit 4's source: byte 02099DA3 is written only by 0025D950; the override pair 02099DA4/02099DA5 is written "
        "by 0026AB50 (cl, dl) from verb handlers 00356030 (1, popped int) and 003563C0 (0, 0), and zeroed by the area "
        "unload 002628B0 (00262A24/00262A2B, ebp = 0 from 0026292A) and the area reset 00266D10 (00266D47/00266D4E) "
        "%s" % ("" if src == want_src else src))
    badseq = [("%08X" % a, txt(insn(img, a))) for a, t in seq.items() if txt(insn(img, a)) != t]
    report("K3d", not badseq, "route shapes: 002E63C0 then 002E8CC0 at 00262B80/00262B85, 002E63C0 then no re-derive "
           "at 00266DBF; requester 1 = bit 35 (002265C8..002265D4); the verb passes its popped int (0034783C); "
           "0025D950 passes byte 02099DA3 (0025D9AA/0025D9AD); 0042ED60 clears bit 5, retires, promotes, tests "
           "bit 5, rebuilds %s" % badseq)
    return not bad and not badseq


# ------------------------------------------------------------------------------------------------ K4: readers
def k4(img):
    exp = {0x00425FC7: "mov rdi, r8", 0x00426006: "mov rdx, rdi", 0x00426009: "mov rcx, rbx", 0x0042600C: "call r14",
           0x0042601D: "mov rdx, rdi", 0x00426031: "call rbp", 0x00425FCA: "mov rbp, rdx", 0x00425FCD: "mov r14, rcx",
           0x004264D5: "mov r8, qword ptr [rip + 0x1ea0a4c]", 0x004264DC: "lea rdx, [rip + 0x670d]",
           0x004264E3: "lea rcx, [rip + 0x6b66]", 0x004264EA: "call 0x425fb0",
           0x00426500: "mov r8, qword ptr [rip + 0x1ea0a21]", 0x00426507: "lea rdx, [rip + 0x6a62]",
           0x0042650E: "lea rcx, [rip + 0x728b]", 0x00426515: "jmp 0x425fb0",
           0x0042CF81: "mov rsi, rdx", 0x0042D072: "mov r14, rdx"}
    bad = [("%08X" % a, txt(insn(img, a))) for a, t in exp.items() if txt(insn(img, a)) != t]
    dec = {}
    for a in (0x004264D5, 0x00426500):
        ci = insn(img, a)
        dec[a] = ci.address + ci.size + ci.operands[1].mem.disp
    for a in (0x004264DC, 0x004264E3, 0x00426507, 0x0042650E):
        ci = insn(img, a)
        dec[a] = ci.address + ci.size + ci.operands[1].mem.disp
    okp = (dec[0x004264D5] == POOLPTR and dec[0x00426500] == POOLPTR and dec[0x004264E3] == 0x0042D050
           and dec[0x004264DC] == 0x0042CBF0 and dec[0x00426507] == 0x0042CF70 and dec[0x0042650E] == 0x0042D7A0)
    report("K4a", not bad and okp,
           "00425FB0(root cb, child cb, ctx) passes ctx (r8 -> rdi) as rdx to both callbacks; 004264A0 registers root "
           "0042D050 / child 0042CBF0 and 00426500 root 0042D7A0 / child 0042CF70, each with ctx = [022C6F28]; the "
           "two bit-2 readers keep that pool base (0042CF81 rsi, 0042D072 r14) %s" % bad)
    gate = {0x0042D004: "test byte ptr [rsi + 0x48818], 4", 0x0042D00B: "je 0x42d039",
            0x0042D00D: "test dword ptr [rdi + 0x284], 0x800000", 0x0042D019: "test dword ptr [rbx + 0x284], 0x800000",
            0x0042D025: "or dword ptr [rax + 8], 2", 0x0042D039: "and dword ptr [rax + 8], 0xfffffffd",
            0x0042CFFF: "call 0x3e55b0", 0x0042D39D: "call 0x3e55b0",
            0x0042D3A2: "test byte ptr [r14 + 0x48818], 4", 0x0042D3B5: "je 0x42d3c9",
            0x0042D3B7: "test dword ptr [rbx + 0x284], 0x800000", 0x0042D3C3: "or dword ptr [rax + 8], 2",
            0x0042D3C9: "and dword ptr [rax + 8], 0xfffffffd"}
    badg = [("%08X" % a, txt(insn(img, a))) for a, t in gate.items() if txt(insn(img, a)) != t]
    report("K4b", not badg, "the two bit-2 gates: model instance (003E55B0's answer) +8 bit 1 = flag bit 2 AND record "
           "+0x284 bit 23 (root, 0042D3A2..0042D3C9), AND the parent's bit 23 too (child, 0042D004..0042D039) %s" % badg)
    return not bad and okp and not badg


# ------------------------------------------------------------------------------------------------ K5: closures
def closure(img, root):
    frags = pdata_roots(img)
    tva, tlen = sec(img, ".text")[0], sec(img, ".text")[1]
    seen, indirect, stack = set(), 0, [root]
    while stack:
        f = stack.pop()
        if f in seen or not (tva <= f < tva + tlen):
            continue
        seen.add(f)
        parts = frags.get(f)
        if parts is None:
            pd = img.pdata(f)
            parts = [pd] if pd else None
        if parts is None:
            end = f
            for ci in img.cs.disasm(img.read(f, 0x800), f):
                end = ci.address + ci.size
                if ci.mnemonic in ("ret", "int3", "jmp"):
                    break
            parts = [(f, end)]
        lo, hi = min(p[0] for p in parts), max(p[1] for p in parts)
        for s, e in parts:
            for ci in img.cs.disasm(img.read(s, e - s), s):
                if ci.mnemonic in ("call", "jmp"):
                    op = ci.operands[0]
                    if op.type == X86_OP_IMM:
                        t = op.imm
                        if ci.mnemonic == "call" or not (lo <= t < hi):
                            stack.append(t)
                    else:
                        indirect += 1
    return seen, indirect


def k5(img):
    owners = set(int(x, 16) for x in OUTSIDE + FAMILY) | {0x002E63C0}
    seen, ind = closure(img, 0x0042C410)
    hit = sorted("%08X" % f for f in seen & owners)
    note("closure of 0042C410: %d functions, %d indirect call/jmp sites not followed" % (len(seen), ind))
    report("K5a", not hit and 0x0042C410 in seen,
           "no function directly reachable from the promotion callee 0042C410 touches the word or the veto byte %s" % hit)
    seen2, ind2 = closure(img, 0x004269A0)
    hit2 = sorted("%08X" % f for f in seen2 & {0x00425FB0, 0x0042EF90, 0x004264A0, 0x00426500, 0x0042CF70, 0x0042D050})
    note("closure of 004269A0: %d functions, %d indirect sites not followed" % (len(seen2), ind2))
    report("K5b", not hit2, "the constructor reaches no per-record walker or bit-2 reader between its zero store and "
           "its OR of 5 %s" % hit2)
    # positive control: the closure of 0042ED60 must contain both family entries that set bit 5
    seen3, _ = closure(img, 0x0042ED60)
    report("K5c", {0x00427C90, 0x00428710} <= seen3, "positive control: the same closure walk from 0042ED60 reaches "
           "retire 00427C90 and promote 00428710")


# ------------------------------------------------------------------------------------------------ K6: orders
def k6(img):
    out = {}
    b = Body(img, 0x0026C8C0, 0x0026CDF4)
    rets, tails, outs = b.exits()
    ends = rets + [a for a, t in tails]
    pre = [a for a in b.order if a < 0x0026C95D]
    rcx_written = [a for a in pre if b.ins[a].mnemonic not in ("test", "cmp") and b.ins[a].op_str.split(",")[0].strip()
                   in ("ecx", "rcx", "cx", "cl")]
    out["0026C8C0 reaches 0026CAC0 exactly when its first argument is 0: `test ecx, ecx` / `jne 0026CAC5` at "
        "0026C95D/0026C95F with ecx unwritten before it, and every path from 0026C965 to the one exit %s passes "
        "0026CAC0 (the other two ends call 00809728, the range-check failure)" % ["%08X" % r for r in ends]] = (
        b.exact and ends == [0x0026CDE3] and not outs and not rcx_written
        and txt(insn(img, 0x0026C95D)) == "test ecx, ecx" and txt(insn(img, 0x0026C95F)) == "jne 0x26cac5"
        and all(r not in b.reach(0x0026C965, avoid=[0x0026CAC0]) for r in ends)
        and 0x0026CDE3 in b.reach(0x0026C8C0, avoid=[0x0026CAC0])
        and [txt(insn(img, a)) for a in (0x0026CDE8, 0x0026CDEE)] == ["call 0x809728", "call 0x809728"])
    b = Body(img, 0x00226280, 0x00226638)
    rets = b.exits()[0]
    out["002265D6 on every path of 00226280 past the dirty gate 0022628E"] = b.exact and all(
        r not in b.reach(0x00226294, avoid=[0x002265D6]) for r in rets) and txt(insn(img, 0x00226287)).startswith(
        "cmp byte ptr [rip") and txt(insn(img, 0x0022628E)) == "je 0x226633"
    b = Body(img, 0x004269A0, 0x00426C85)
    rets = b.exits()[0]
    out["00426C59 after 00426A00 on every path of 004269A0"] = b.exact and all(
        r not in b.reach(0x00426A00, avoid=[0x00426C59]) for r in rets) and b.dominates(0x00426A00, 0x00426C59)
    b = Body(img, 0x00314020, 0x0031436D)
    rets, tails, outs = b.exits()
    out["00314346 before 00314020's only ret 0031436C"] = b.exact and rets == [0x0031436C] and not tails and not outs \
        and b.dominates(0x00314346, 0x0031436C)
    bad = [k for k, v in out.items() if not v]
    report("K6", not bad, "; ".join(out) + (" FAILED: %s" % bad if bad else ""))


# ------------------------------------------------------------------------------------------------ K7: execution
def make_uc(img):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    lo = img.base
    hi = max(img.base + va + max(vs, rs) for n, va, vs, ra, rs in img.secs)
    hi = (hi + 0xFFFF) & ~0xFFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(lo, img.d[:0x1000])
    for n, va, vs, ra, rs in img.secs:
        uc.mem_write(img.base + va, img.d[ra:ra + min(rs, vs if vs else rs)])
    uc.mem_map(STACK - 0x10000, 0x20000)
    uc.mem_map(POOL, 0x50000)
    uc.mem_map(INST, 0x1000)
    uc.mem_map(MAGIC, 0x1000)
    uc.mem_write(MAGIC, b"\xC3" * 16)
    uc.mem_write(POOLPTR, struct.pack("<Q", POOL))
    return uc


def rd32(uc, a):
    return struct.unpack("<I", uc.mem_read(a, 4))[0]


def wr32(uc, a, v):
    uc.mem_write(a, struct.pack("<I", v & 0xFFFFFFFF))


def flags(uc):
    return rd32(uc, POOL + FLAGS)


def veto(uc):
    return uc.mem_read(VETO, 1)[0]


def run(uc, entry, stop=MAGIC, rcx=0, rdx=0, r8=0, regs=None, stubs=None):
    """Call entry with a return to MAGIC. stubs: {callee VA: fn(uc)} answered at the callee's entry by popping the
    return address (works for call and tail jmp alike)."""
    stubs = stubs or {}
    sp = STACK - 0x100
    uc.mem_write(sp, struct.pack("<Q", MAGIC))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    uc.reg_write(UC_X86_REG_R8, r8)
    for r, v in (regs or {}).items():
        uc.reg_write(r, v)

    def hook(u, addr, size, _):
        if addr in stubs:
            stubs[addr](u)
            spv = u.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", u.mem_read(spv, 8))[0]
            u.reg_write(UC_X86_REG_RSP, spv + 8)
            u.reg_write(UC_X86_REG_RIP, ret)
    h = uc.hook_add(UC_HOOK_CODE, hook) if stubs else None
    try:
        uc.emu_start(entry, stop, count=200000)
    finally:
        if h is not None:
            uc.hook_del(h)


def k7a(img):
    uc = make_uc(img)
    wr32(uc, POOL + FLAGS, 0x25)
    uc.mem_write(VETO, b"\x00")
    trace = []
    for fn, c, d in ((0x002EBBB0, 0, 0), (0x002EBBF0, 1, 0), (0x002EBBB0, 1, 0), (0x002EBBF0, 1, 1)):
        run(uc, fn, rcx=c, rdx=d)
        trace.append((veto(uc), flags(uc)))
    ok = trace == [(1, 0x24), (3, 0x24), (2, 0x24), (0, 0x25)]
    report("K7a", ok, "veto mask: script off -> (byte, word) %s; tick veto %s; script on %s (tick still vetoes, bit 0 "
           "stays 0); tick on %s; bits 2 and 5 untouched" % tuple("(%d, %02X)" % t for t in trace))
    return ok


def k7b(img):
    uc = make_uc(img)
    wr32(uc, POOL + FLAGS, 0x04)
    uc.mem_write(VETO, b"\x01")
    run(uc, 0x0042ED30)
    after_reset = flags(uc)
    run(uc, 0x002E8CC0)
    after_refresh = flags(uc)
    ok = after_reset & 1 == 1 and veto(uc) == 1 and after_refresh & 1 == 0 and after_reset & 4 == 4
    report("K7b", ok, "0042ED30 over a held veto (byte 1): word %02X (bit 0 set, the byte unread); 002E8CC0 then: %02X"
           % (after_reset, after_refresh))
    return ok


def k7c(img):
    uc = make_uc(img)
    wr32(uc, POOL + FLAGS, 0x24)
    uc.mem_write(VETO, b"\x03")
    run(uc, 0x002E63C0)
    a = (veto(uc), flags(uc))
    run(uc, 0x002E8CC0)
    b = (veto(uc), flags(uc))
    ok = a == (0, 0x24) and b == (0, 0x25)
    report("K7c", ok, "002E63C0 on byte 3 / word 24: (%d, %02X) - no veto, culling still off; 002E8CC0 then (%d, %02X)"
           % (a + b))
    return ok


def k7d(img):
    uc = make_uc(img)
    res = []
    for start, x in ((0x25, 0), (0x25, 1), (0x05, 0x80000000), (0x35, 0), (0x35, 0x100)):
        wr32(uc, POOL + FLAGS, start)
        run(uc, 0x002E8700, rcx=x)
        res.append(flags(uc))
    ok = res == [0x25, 0x35, 0x15, 0x25, 0x35]
    report("K7d", ok, "002E8700(x): bit 4 = (x != 0), others kept: %s" % ["%02X" % r for r in res])
    return ok


def k7e(img):
    res = []
    for pre, callee_xor in ((0x25, 0x05), (0x24, 0x01), (0x25, 0x00), (0x24, 0x04)):
        uc = make_uc(img)
        wr32(uc, POOL + FLAGS, pre)
        seen = []

        def callee(u, m=callee_xor):
            seen.append(flags(u))
            wr32(u, POOL + FLAGS, flags(u) ^ m)
        run(uc, 0x00428790, stop=0x004287BD, regs={UC_X86_REG_RDI: POOL, UC_X86_REG_RSI: POOL + 0x740},
            stubs={0x0042C410: callee})
        res.append((pre, callee_xor, seen[0] if seen else None, flags(uc)))
    want = [(0x25, 0x05, 0x24, 0x21), (0x24, 0x01, 0x24, 0x24), (0x25, 0x00, 0x24, 0x25), (0x24, 0x04, 0x24, 0x20)]
    ok = res == want
    report("K7e", ok, "promotion pin (pre, callee xor, callee sees, after): %s - the callee sees bit 0 clear, bit 0 "
           "returns to PRE, the callee's bit-2 change survives" % ["(%02X,%02X,%02X,%02X)" % r for r in res])
    return ok


def k7f(img):
    res = {}
    for fb2 in (0, 1):
        for cb in (0, 1):
            for pb in (0, 1):
                uc = make_uc(img)
                wr32(uc, POOL + FLAGS, 0x21 | (4 if fb2 else 0))
                parent, child = POOL, POOL + 0x740
                wr32(uc, parent + 0x284, 0x4 | (0x800000 if pb else 0))
                wr32(uc, child + 0x284, 0x4 | (0x800000 if cb else 0))
                uc.mem_write(child + 0x2AE, b"\x00")
                uc.mem_write(child + 6, struct.pack("<h", 0))
                wr32(uc, INST + 8, 0xFFFFFFFD if fb2 else 0x2)   # start opposite to make both arms visible

                def ret_inst(u):
                    u.reg_write(UC_X86_REG_RAX, INST)
                nop = (lambda u: None)
                run(uc, 0x0042CF70, rcx=child, rdx=POOL,
                    stubs={0x00420A40: nop, 0x00421030: nop, 0x00421010: nop, 0x003E55B0: ret_inst})
                res[(fb2, cb, pb)] = (rd32(uc, INST + 8) >> 1) & 1
    ok = all(v == (1 if k == (1, 1, 1) else 0) for k, v in res.items())
    report("K7f", ok, "0042CF70: instance +8 bit 1 by (flag bit 2, child bit 23, parent bit 23): %s"
           % " ".join("%d%d%d->%d" % (k + (v,)) for k, v in sorted(res.items())))
    return ok


def k7g(img):
    res = []
    for pre5, ret_sets, pro_sets in ((0, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0)):
        uc = make_uc(img)
        wr32(uc, POOL + FLAGS, 0x05 | (0x20 if pre5 else 0))
        wr32(uc, POOL + 0x48800, 0xFFFFFFFF)
        called = []

        def setter(flag):
            def f(u):
                if flag:
                    wr32(u, POOL + FLAGS, flags(u) | 0x20)
            return f

        def rec(name):
            def f(u):
                called.append(name)
            return f
        stubs = {0x0016D6A0: rec("16D6A0"), 0x00427C90: setter(ret_sets), 0x00428710: setter(pro_sets),
                 0x0020E600: rec("20E600"), 0x0041E500: rec("41E500"), 0x0042DA30: rec("42DA30"),
                 0x003697C0: rec("3697C0"), 0x00427DE0: rec("427DE0"), 0x00427BD0: rec("427BD0")}
        run(uc, 0x0042ED60, stubs=stubs)
        res.append(((pre5, ret_sets, pro_sets), "41E500" in called, "427BD0" in called))
    ok = [r[1] for r in res] == [False, True, True, False] and all(r[2] for r in res)
    report("K7g", ok, "0042ED60 (pre bit 5, retire sets, promote sets) -> rebuild 0041E500: %s; tail 00427BD0 reached "
           "in every case" % " ".join("%d%d%d->%s" % (r[0] + ("yes" if r[1] else "no",)) for r in res))
    return ok


# ------------------------------------------------------------------------------------------------ main
def main():
    img = Img.load()
    img.cs.detail = True
    print("FABLE check_s38 - the render pool flag word +0x48818 and its owners outside the family (2026-10-03)")
    print("unicorn %s" % UC_VERSION)
    print("image sha256 verified (rvlib), base %08X" % img.base)
    report("V0", UC_VERSION == "2.1.4", "unicorn pinned 2.1.4")
    k1(img)
    k2(img)
    k3(img)
    k4(img)
    k5(img)
    k6(img)
    for f in (k7a, k7b, k7c, k7d, k7e, k7f, k7g):
        f(img)

    def failing(fn, im):
        global fails
        before = fails
        quiet[0] = True
        try:
            r = fn(im)
        except Exception as e:  # a crash under the mutation also counts as the check failing
            r = False
            note("exception %r" % e)
        quiet[0] = False
        globals()["fails"] = before
        return not r

    def pat(va, b):
        im = img.patched(va, b)
        im.cs.detail = True
        return im

    report("S1", failing(k7a, pat(0x002EBC1E, b"\x74")), "002EBC1E jne -> je: K7a fails")
    report("S2", failing(k7b, pat(0x0042ED37 + 6, b"\x04")), "0042ED37 or ..., 5 -> or ..., 4: K7b fails")
    report("S3", failing(k7e, pat(0x004287B4 + 2, b"\x05")), "004287B4 and eax, 1 -> and eax, 5: K7e fails")
    report("S4", failing(k7f, pat(0x0042D004 + 6, b"\x01")), "0042D004 test ..., 4 -> test ..., 1: K7f fails")
    report("S5", failing(k7g, pat(0x0042ED83, b"\x90" * 7)), "0042ED83 bit-5 clear NOPed: K7g fails")
    got = census(img)
    readers2 = [s for s in got if txt(insn(img, s)).startswith("test") and insn(img, s).operands[1].imm & 4]
    report("S6", bool(readers2), "the claim 'bit 2 is never read' is refuted by the census: %s"
           % ["%08X" % s for s in readers2])
    print("FAILS %d" % fails)
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
