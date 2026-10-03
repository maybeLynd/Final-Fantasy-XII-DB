"""check_s25.py - FABLE, 2026-10-03: the S-25 gambit set selector 00305AB0 and the set/subgroup switch in 002FDDA0.

Settles, at the bytes of the certified image (73461d08..., base 0x00120000), the claims of section.txt (§8a, G-§8a.1-.6):

  K1  00305AB0 has exactly two .text callers, 0030874C in 00308610 (edx = 1, resume) and 00313D89 in the queue drain
      00313CD0 (edx = 0, fresh); no pointer constant names it.
  K2  the walk 00305CC0 has exactly four callers, all in 00305AB0 (00305BA5, 00305C1A, 00305C58, 00305C71); the
      subgroup register r8d is zeroed for three (00305B9F, 00305C14, 00305C6B) and loaded from byte +0x6B5 for the
      fourth (00305C34); the static-set entry into the third call zeroes it too (00305BDB).
  K3  the exact-displacement census of +0x6B5 is four instructions (00236BA3, 002FE09F, 002FE0BB store; 00305C34
      reads); the verb body 00239040 (whole, 0x65 bytes) has no operand at +0x6B0..+0x6B7.
  K4  the forced sets: 01EEC320 = {0x0096 relation 1, 0x4125}, 01EEC370 = {0x0096 relation 1}, fallback record
      01EEC298 = {0x4021, flags 0x2000}; references: 01EEC320/01EEC370 only from 00305AB0 (00305B89 / 00305BDE) and
      the membership test 0030BF20; 01EEC298 only from 00305C7E/00305C86; 0030BF20 has one caller, 00307DC2.
  K5  0023A570 (the definition apply): the definition-kind split is at 0023A626/0023A62E; over direct control flow
      the kind-1 arm (0023A641) reaches the +0x6E0 variant-0 store 0023A95E and NOT the +0x6F0 store 0023ABB5; the
      kind-0 arm (0023AA49) reaches 0023AB9F and 0023ABB5; 0023ABA6 is the only reference to 01E09350.  Image-wide,
      the qword stores at displacement +0x6F0 are listed, and the two in battle-unit code are 00236BB6 (0) and
      0023ABB5.
  K6  002FDDA0 has no E8/E9 caller; table 01EEC460 names it in 249 slots, among them every id 0x4112..0x4121.
  K7  the order-set directory slot 02EBF168: its .text readers are 00239060, 0023A1A8 (the binder), 0023A70B,
      0023A92F and 002FE060; a count bound precedes the index in 0023A570 (0023A71E-0023A726) and 002FE025
      (002FE06C-002FE077) and in no instruction of 00239040.
  K8  the remaining cited sites (reset zero stores, IssueCommand's B install, the kind-1 jumps, the party set
      arithmetic, the selector's read-before-null-test, 002FDDA0's read-before-guard, the verb wrapper), the
      variant-0 bound on the kind-1 arm, and the count (12) of qword stores at +0x6F0.
  K9  the suspension pair: 0030EFF0 (one caller, 0031307B) copies +0x6B0..+0xB9F (0x4F0 bytes) to a buffer, zeroes
      the block and keeps the buffer at +0xB88; 0030EDA0 (one caller, 003082C6 in 00308270) copies it back.
  E   executed (Unicorn 2.1.4, original code): the selector 00305AB0 whole, with its five callees supplied by hooks
      (walk 00305CC0, commit 0030F760, field bit 00377C20, availability 002FFCF0, bit-22 helper 00308270), in 14 cases
      E1-E14 (traces of which set is offered with which subgroup, and what is committed); E15-E16 run the suspension
      0030EFF0 (allocator 0030DFA0 answered, the memset import bridged) and then the selector, E15 with 00308270 and
      0030EDA0 as shipped (0030C970 supplied);
  W   executed: 002FDDA0 whole for ids 0x4112..0x4121 and the edge cases W1-W6 (0020E600 runs as shipped);
  V   executed: the script verb's body 00239040 (0031B760 answered by a hook) V1-V2.

Sensitivity controls (each must make a check FAIL; the control PASSES when it does):
  S1  image: 00305C32 `jmp 00305C61` -> `jmp 00305C34` (B's failure falls to C): E2 must fail.
  S2  image: 00305B57 `je 00305C7A` NOPed (the field-bit party skip removed): E8 must fail.
  S3  image: 002FE09F stores 5 instead of 0: W2 must fail.
  S4  image: 002FE077 `jg` NOPed (the directory bound removed): W4 must fail.
  S5  image: 0023AA44 `jmp 0023ABCA` -> `jmp 0023ABA6`: K5 must fail.
  S6  claim: "every variant switch restarts at subgroup 0" checked against V1 must fail.
  S7  image: 003082C6 `call 0030EDA0` NOPed (no restore): E15 must fail.

Prints FAILS N last.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, disp_sweep  # noqa: E402
from capstone.x86 import X86_OP_MEM, X86_OP_IMM  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, __version__ as UC_VERSION  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,  # noqa: E402
                               UC_X86_REG_R9, UC_X86_REG_RSP, UC_X86_REG_RIP)

SEL, WALK, COMMIT, FIELD15, AVAIL, BIT22 = 0x00305AB0, 0x00305CC0, 0x0030F760, 0x00377C20, 0x002FFCF0, 0x00308270
SWITCH, VERB, RESOLVE, GETUNIT = 0x002FDDA0, 0x00239040, 0x0020E600, 0x0031B760
FORCED_ALL, FORCED_PARTY, FALLBACK = 0x01EEC320, 0x01EEC370, 0x01EEC298
DIRSLOT, RTBASE = 0x02EBF168, 0x01F83530
SLOTREL, SUSPEND, RESTORE, ALLOC, MEMSET = 0x0030C970, 0x0030EFF0, 0x0030EDA0, 0x0030DFA0, 0x00861EC0

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


def one(img, va):
    ci = next(img.cs.disasm(img.read(va, 16), va, 1))
    return ci, (ci.mnemonic + " " + ci.op_str).strip()


def body(img, s, e):
    return list(img.cs.disasm(img.read(s, e - s), s))


# ---------------------------------------------------------------- static
def k1(img):
    refs, unc = text_refs(img, SEL)
    got = [(r["site"], r["form"], r["func"]) for r in refs]
    report("K1a", [(g[0], g[1]) for g in got] == [(0x0030874C, "call"), (0x00313D89, "call")] and not unc,
           "00305AB0 callers: %s" % ["%08X %s fn=%08X" % g for g in got])
    _, a = one(img, 0x00308744)
    _, b = one(img, 0x00313D84)
    report("K1b", a == "mov edx, 1" and b == "xor edx, edx", "resume mode at the two sites: 00308744 `%s`, 00313D84 `%s`"
           % (a, b))
    report("K1c", not [d for d in data_refs(img, SEL) if d[2] == "va64"], "no 8-byte pointer constant names 00305AB0")


def k2(img):
    refs, _ = text_refs(img, WALK)
    got = [(r["site"], r["func"]) for r in refs]
    want = [(0x00305BA5, SEL), (0x00305C1A, SEL), (0x00305C58, SEL), (0x00305C71, SEL)]
    report("K2a", got == want, "00305CC0 callers: %s" % ["%08X fn=%08X" % g for g in got])
    want_r8 = {0x00305B9F: "xor r8d, r8d", 0x00305C14: "xor r8d, r8d", 0x00305C6B: "xor r8d, r8d",
               0x00305BDB: "xor r8d, r8d", 0x00305C34: "movzx r8d, byte ptr [rbx + 0x6b5]"}
    bad = [(hex(a), one(img, a)[1]) for a, t in want_r8.items() if one(img, a)[1] != t]
    report("K2b", not bad, "subgroup setups: three xor, the static-set entry xor (00305BDB), one byte +0x6B5 (00305C34) %s"
           % bad)


def k3(img):
    rows = disp_sweep(img, 0x6B5)
    got = [(r[0], r[3]) for r in rows]
    report("K3a", [g[0] for g in got] == [0x00236BA3, 0x002FE09F, 0x002FE0BB, 0x00305C34],
           "+0x6B5 exact-displacement census: %s" % ["%08X %s" % (r[0], r[1]) for r in rows])
    hits = []
    for ci in body(img, 0x00239040, 0x002390A5):
        for op in ci.operands:
            if op.type == X86_OP_MEM and 0x6B0 <= op.mem.disp <= 0x6B7:
                hits.append("%08X" % ci.address)
    report("K3b", not hits, "00239040 (0x65 bytes, whole) has no operand at +0x6B0..+0x6B7 %s" % hits)


def rec(img, a):
    b = img.read(a, 0x18)
    sel, par, fl = struct.unpack_from("<HhH", b, 0)
    return sel, par, fl, struct.unpack_from("<H", b, 6)[0]


def k4(img):
    a = img.read(FORCED_ALL, 0x20)
    b = img.read(FORCED_PARTY, 0x20)
    ok = (a[0] == 2 and not any(a[1:]) and rec(img, FORCED_ALL + 0x20) == (0x96, 0, 0, 1)
          and rec(img, FORCED_ALL + 0x38) == (0x4125, 0, 0, 0)
          and b[0] == 1 and not any(b[1:]) and rec(img, FORCED_PARTY + 0x20) == (0x96, 0, 0, 1)
          and rec(img, FALLBACK)[:3] == (0x4021, 0, 0x2000))
    report("K4a", ok, "forced sets decode: 01EEC320 = {0x0096 rel 1, 0x4125}, 01EEC370 = {0x0096 rel 1}; fallback "
                      "01EEC298 = {0x4021, flags 0x2000}")
    r1, _ = text_refs(img, FORCED_ALL, FORCED_ALL + 0x50)
    r2, _ = text_refs(img, FORCED_PARTY, FORCED_PARTY + 0x50)
    r3, _ = text_refs(img, FALLBACK, FALLBACK + 0x18)
    s1 = [(r["site"], r["func"]) for r in r1]
    s2 = [(r["site"], r["func"]) for r in r2]
    s3 = [r["site"] for r in r3]
    report("K4b", s1 == [(0x00305B89, SEL), (0x0030BF25, 0x0030BF20), (0x0030BF44, 0x0030BF20)]
           and s2 == [(0x00305BDE, SEL), (0x0030BF60, 0x0030BF20), (0x0030BF77, 0x0030BF20)]
           and s3 == [0x00305C7E, 0x00305C86]
           and not data_refs(img, FORCED_ALL, FORCED_ALL + 0x50) and not data_refs(img, FORCED_PARTY, FORCED_PARTY + 0x50),
           "references: 01EEC320 %s; 01EEC370 %s; 01EEC298 %s" % (["%08X" % x[0] for x in s1], ["%08X" % x[0] for x in s2],
                                                                ["%08X" % x for x in s3]))
    r4, _ = text_refs(img, 0x0030BF20)
    report("K4c", [r["site"] for r in r4] == [0x00307DC2], "the membership test 0030BF20 has one caller: %s"
           % ["%08X" % r["site"] for r in r4])


def reach(img, start, s, e, stop=()):
    """Direct-flow reachability inside [s, e) from start (fall-through, jcc both ways, jmp imm)."""
    ins = {ci.address: ci for ci in body(img, s, e)}
    seen, work = set(), [start]
    while work:
        a = work.pop()
        if a in seen or a not in ins or a in stop:
            continue
        seen.add(a)
        ci = ins[a]
        m = ci.mnemonic
        nxt = a + ci.size
        if m == "ret" or m == "int3":
            continue
        if m == "jmp":
            op = ci.operands[0]
            if op.type == X86_OP_IMM:
                work.append(op.imm)
            continue
        if m.startswith("j") and ci.operands and ci.operands[0].type == X86_OP_IMM:
            work.append(ci.operands[0].imm)
        work.append(nxt)
    return seen


def k5(img):
    s, e = 0x0023A570, 0x0023AC80
    _, t1 = one(img, 0x0023A626)
    _, t2 = one(img, 0x0023A628)
    _, t3 = one(img, 0x0023A62E)
    split = (t1 == "test esi, esi" and t2 == "je 0x23aa49" and t3 == "cmp esi, 1")
    k1arm = reach(img, 0x0023A641, s, e)
    k0arm = reach(img, 0x0023AA49, s, e)
    ok = (split and 0x0023A95E in k1arm and 0x0023ABB5 not in k1arm and 0x0023AB9F not in k1arm
          and 0x0023AB9F in k0arm and 0x0023ABB5 in k0arm)
    report("K5a", ok, "kind split 0023A626-0023A62E; kind-1 arm reaches 0023A95E %s, 0023ABB5 %s; kind-0 arm reaches "
                      "0023AB9F %s, 0023ABB5 %s" % (0x0023A95E in k1arm, 0x0023ABB5 in k1arm, 0x0023AB9F in k0arm,
                                                   0x0023ABB5 in k0arm))
    r, _ = text_refs(img, 0x01E09350, 0x01E09350 + 0x38)
    report("K5b", [x["site"] for x in r] == [0x0023ABA6] and not data_refs(img, 0x01E09350, 0x01E09350 + 0x38),
           "01E09350 (the {0x4124} set) is referenced only at %s" % ["%08X" % x["site"] for x in r])
    stores = [x for x in disp_sweep(img, 0x6F0, 8) if x[3] & 2]
    note("qword stores at +0x6F0 image-wide: %s" % ["%08X fn=%08X" % (x[0], x[4]) for x in stores])
    report("K5c", [x[0] for x in stores if x[4] in (0x00236A60, 0x0023A570)] == [0x00236BB6, 0x0023ABB5]
           and one(img, 0x00236A93)[1] == "xor esi, esi" and one(img, 0x00236BB6)[1] == "mov qword ptr [rdi + 0x6f0], rsi",
           "battle-unit stores to +0x6F0: 00236BB6 (rsi = 0 from 00236A93) and 0023ABB5; %d others, in non-unit code"
           % (len(stores) - 2))


def k6(img):
    refs, _ = text_refs(img, SWITCH)
    tab = 0x01EEC460
    slots = [img.u64(tab + 8 * i) for i in range(0x167)]
    n = sum(1 for v in slots if v == SWITCH)
    sw = all(slots[i - 0x4000] == SWITCH for i in range(0x4112, 0x4122))
    report("K6", not refs and n == 249 and sw, "002FDDA0: %d E8/E9 callers; table 01EEC460 names it in %d slots; ids "
                                              "0x4112..0x4121 all route to it: %s" % (len(refs), n, sw))


def k7(img):
    refs, _ = text_refs(img, DIRSLOT, DIRSLOT + 8)
    report("K7a", [r["site"] for r in refs] == [0x00239060, 0x0023A1A8, 0x0023A70B, 0x0023A92F, 0x002FE060],
           "02EBF168 .text readers: %s" % ["%08X" % r["site"] for r in refs])
    a = [one(img, x)[1] for x in (0x0023A71E, 0x0023A722, 0x0023A724, 0x0023A726)]
    b = [one(img, x)[1] for x in (0x002FE06C, 0x002FE073, 0x002FE075, 0x002FE077)]
    cmps = [ci.address for ci in body(img, 0x00239040, 0x002390A5) if ci.mnemonic == "cmp"]
    report("K7b", a == ["movzx eax, word ptr [rsi + 0x50]", "dec ecx", "cmp eax, ecx", "jg 0x23a63a"]
           and b == ["movzx eax, word ptr [rcx]", "dec eax", "cmp edx, eax", "jg 0x2fe523"] and cmps == [0x00239049],
           "count bound in 0023A570 %s and 002FE025 %s; 00239040's only cmp is 00239049 `cmp edi, 3`" % (a[2:], b[2:]))


def k8(img):
    """The remaining sites section.txt cites, read at the bytes."""
    want = {
        0x00236A93: "xor esi, esi", 0x00236B10: "xor eax, eax",
        0x00236BA3: "mov byte ptr [rdi + 0x6b5], al", 0x00236BAF: "mov qword ptr [rdi + 0x6f8], rsi",
        0x00236BB6: "mov qword ptr [rdi + 0x6f0], rsi", 0x00236BBD: "mov qword ptr [rdi + 0x6e8], rsi",
        0x00236BC4: "mov qword ptr [rdi + 0x6e0], rsi", 0x00236BD2: "mov qword ptr [rdi + 0x748], rsi",
        0x00311DDB: "mov dword ptr [rbx + 0x748], edi", 0x00311DE1: "mov qword ptr [rbx + 0x6f8], rax",
        0x0023AA2A: "jmp 0x23abca", 0x0023AA44: "jmp 0x23abca",
        0x0023AB64: "lea rcx, [rip + 0x1e4e80d]", 0x0023AB7E: "imul rax, r14, 0x170",
        0x0023AB9F: "mov qword ptr [rdi + 0x6e0], rax", 0x0023ABB5: "mov qword ptr [rdi + 0x6f0], rax",
        0x0023A95E: "mov qword ptr [rdi + 0x6e0], rax",
        0x00305B66: "mov rax, qword ptr [rbx + 0x698]", 0x00305B6D: "mov ecx, dword ptr [rax + 0x64]",
        0x00305B78: "test rax, rax", 0x00305C3E: "mov rdx, qword ptr [rbx + 0x6e0]",
        0x002FDDA6: "mov rax, qword ptr [rcx + 0x708]", 0x002FDDB7: "cmp byte ptr [rbx + 0x6b4], 0",
        0x002FDDBE: "movsx ecx, word ptr [rax + 2]",
        0x0051058C: "call 0x267e10", 0x0051059B: "jmp 0x239040",
    }
    bad = [("%08X" % a, one(img, a)[1]) for a, t in want.items() if one(img, a)[1] != t]
    report("K8a", not bad, "%d cited instructions read as stated %s" % (len(want), bad))
    s, e = 0x0023A570, 0x0023AC80
    k1arm = reach(img, 0x0023A641, s, e)
    report("K8b", 0x0023A71E in k1arm and 0x0023A726 in k1arm and 0x0023A95E in k1arm,
           "the variant-0 count bound 0023A71E-0023A726 lies on the kind-1 arm before the store 0023A95E")
    n = len([x for x in disp_sweep(img, 0x6F0, 8) if x[3] & 2])
    report("K8c", n == 12, "qword stores at +0x6F0 image-wide: %d" % n)


# ---------------------------------------------------------------- execution
STACK, HEAP, MAGIC = 0x7F000000, 0x10000000, 0x7E000000
UNIT, STATS, CTX, DIR, ROW = HEAP, HEAP + 0x2000, HEAP + 0x3000, HEAP + 0x4000, HEAP + 0x5000
SET_A, SET_B, SET_C, SET_D, SET_V = 0x5A000000, 0x5B000000, 0x5C000000, 0x5D000000, 0x56000000
NAMES = {SET_A: "A", SET_B: "B", SET_C: "C", SET_D: "D", FORCED_ALL: "F320", FORCED_PARTY: "F370", 0: "null"}


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
    uc.mem_map(HEAP, 0x10000)
    uc.mem_map(MAGIC, 0x1000)
    uc.mem_write(MAGIC, b"\xC3" * 16)
    return uc


def q(uc, a, v):
    uc.mem_write(a, struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF))


def rq(uc, a, fmt="<Q", n=8):
    return struct.unpack(fmt, bytes(uc.mem_read(a, n)))[0]


def stub(uc, ret):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    uc.reg_write(UC_X86_REG_RAX, ret & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_RIP, rq(uc, rsp))
    uc.reg_write(UC_X86_REG_RSP, rsp + 8)


def run_sel(img, kind=1, bit2=0, confuse=0, berserk=0, field15=0, mode=0, sg=0, setB=SET_B, unit_flags=0,
            issued=None, avail=0, walk_ok=(), commit_ret=1, uc=None, real22=False):
    if uc is not None:
        return run_sel_on(uc, kind, field15, mode, avail, walk_ok, commit_ret, real22)
    uc = make_uc(img)
    q(uc, UNIT, unit_flags)
    q(uc, UNIT + 0x698, STATS)
    uc.mem_write(STATS, struct.pack("<I", 4 if bit2 else 0))
    uc.mem_write(STATS + 5, bytes([kind]))
    uc.mem_write(STATS + 0x3C, struct.pack("<I", (0x08000000 if berserk else 0)))
    uc.mem_write(STATS + 0x64, struct.pack("<I", (0x20 if confuse else 0)))
    q(uc, UNIT + 0x6E0, SET_C)
    q(uc, UNIT + 0x6E8, SET_A)
    q(uc, UNIT + 0x6F0, SET_D)
    q(uc, UNIT + 0x6F8, setB)
    uc.mem_write(UNIT + 0x748, struct.pack("<I", 0x77))
    uc.mem_write(UNIT + 0x6B5, bytes([sg]))
    if issued is not None:
        uc.mem_write(UNIT + 0xBA0, struct.pack("<H", issued))
        uc.mem_write(UNIT + 0xBB8, struct.pack("<I", 0x100005))
    return run_sel_on(uc, kind, field15, mode, avail, walk_ok, commit_ret, real22)


def run_sel_on(uc, kind, field15, mode, avail, walk_ok, commit_ret, real22):
    trace = []

    def hook(u, addr, size, _):
        if addr == WALK:
            s = u.reg_read(UC_X86_REG_RDX)
            nm = NAMES.get(s, "%X" % s)
            trace.append(("walk", nm, u.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF, u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF))
            stub(u, 1 if nm in walk_ok else 0)
        elif addr == COMMIT:
            rsp = u.reg_read(UC_X86_REG_RSP)
            trace.append(("commit", u.reg_read(UC_X86_REG_RDX), u.reg_read(UC_X86_REG_R8) & 0xFFFF,
                          u.reg_read(UC_X86_REG_R9) & 0xFFFFFFFF, rq(u, rsp + 0x28, "<I", 4)))
            stub(u, commit_ret)
        elif addr == FIELD15:
            stub(u, field15)
        elif addr == AVAIL:
            trace.append(("avail", u.reg_read(UC_X86_REG_RCX) & 0xFFFF))
            stub(u, avail)
        elif addr == BIT22:
            trace.append(("bit22",))
            if not real22:
                stub(u, 0)
        elif addr == SLOTREL:
            stub(u, 0)
    hooks = [uc.hook_add(UC_HOOK_CODE, hook, begin=a, end=a) for a in (WALK, COMMIT, FIELD15, AVAIL, BIT22, SLOTREL)]
    uc.mem_write(STACK, struct.pack("<Q", MAGIC))
    uc.reg_write(UC_X86_REG_RSP, STACK)
    uc.reg_write(UC_X86_REG_RCX, UNIT)
    uc.reg_write(UC_X86_REG_RDX, mode)
    uc.emu_start(SEL, MAGIC, count=20000)
    for h in hooks:
        uc.hook_del(h)
    return {"trace": trace, "ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, "B": rq(uc, UNIT + 0x6F8),
            "748": rq(uc, UNIT + 0x748, "<I", 4), "flags": rq(uc, UNIT)}


FB = ("commit", FALLBACK, 0x4021, 0, 1)


def W(nm, sg=0, mode=0):
    return ("walk", nm, sg, mode)


def e_cases(img, which=None):
    cases = {
        "E1": (dict(kind=1, sg=5), [W("A"), W("C", 5), W("D"), FB], dict(B=0, **{"748": 0}),
               "kind 1: A, C with subgroup +0x6B5, D, fallback; B is never tried and +0x6F8/+0x748 are cleared"),
        "E2": (dict(kind=0, bit2=0), [W("A"), W("B"), W("D"), FB], dict(B=0, **{"748": 0}),
               "party, stats bit 2 clear: A, B, then D after B fails (C skipped); +0x6F8/+0x748 cleared"),
        "E3": (dict(kind=0, bit2=0, setB=0), [W("A"), W("D"), FB], {},
               "party, bit 2 clear, no B set: A then D, C never walked"),
        "E4": (dict(kind=0, bit2=1, sg=3), [W("A"), W("C", 3), W("D"), FB], dict(B=0),
               "party, stats bit 2 set: A, C with the subgroup, D"),
        "E5": (dict(kind=1, confuse=1), [W("F320"), FB], dict(B=SET_B),
               "Confuse (status bit 5): only the forced set 01EEC320, then the fallback; A is not tried"),
        "E6": (dict(kind=1, berserk=1), [W("F320"), FB], {}, "Berserk (bit 27) on a kind-1 unit: as E5"),
        "E7": (dict(kind=0, berserk=1), [W("A"), W("F370"), W("D"), FB], dict(B=SET_B),
               "Berserk on a party unit: A, the forced set 01EEC370, D; +0x6F8 kept"),
        "E8": (dict(kind=0, field15=1), [FB], {}, "field bit 15, party unit: no set walked, the fallback commits"),
        "E8r": (dict(kind=0, field15=1, mode=1), [], dict(ret=0), "field bit 15, party unit, resume mode: nothing, 0"),
        "E9": (dict(kind=1, field15=1, confuse=1, sg=2), [W("A"), W("C", 2), W("D"), FB], {},
               "field bit 15, kind 1, Confuse: the status sets are skipped"),
        "E10": (dict(kind=1, unit_flags=0x4000, issued=0x4116),
                [("commit", UNIT + 0xBA0, 0x4116, 0x100005, 1)], dict(flags=0, ret=1),
                "issued command in the 0x4000 band: committed without the availability check; flag 0x4000 consumed"),
        "E11": (dict(kind=1, unit_flags=0x4000, issued=0x0096, avail=4),
                [("avail", 0x96), W("A"), W("C"), W("D"), FB], dict(flags=0),
                "issued action refused by availability (reason 4): flag consumed, the cascade runs"),
        "E12": (dict(kind=1, mode=1, sg=1), [W("A", 0, 1), W("C", 1, 1), W("D", 0, 1)], dict(ret=0),
                "resume mode 1, every set fails: no fallback commit, return 0"),
        "E13": (dict(kind=1, walk_ok=("A",)), [W("A")], dict(ret=1), "the first set that commits ends the cascade"),
        "E14": (dict(kind=1, unit_flags=1 << 22, walk_ok=("A",)), [("bit22",), W("A")], {},
                "unit flag bit 22: 00308270 runs first"),
    }
    out = {}
    for tag, (cfg, want, post, text) in cases.items():
        if which is not None and tag not in which:
            continue
        r = run_sel(img, **cfg)
        want_t = [(t[0], t[1], t[2], cfg.get("mode", 0)) if t[0] == "walk" and len(t) == 4 and t[3] == 0 else t
                  for t in want]
        ok = r["trace"] == want_t and all(r[k] == v for k, v in post.items())
        out[tag] = r
        report(tag, ok, "%s: %s" % (text, " ".join(fmt_t(t) for t in r["trace"]) or "(nothing)"))
    return out


def suspend_cases(img, which=None):
    """E15/E16: the suspension snapshot 0030EFF0 (0030DFA0 answered with a buffer, the memset import bridged), then the
    selector with unit flag bit 22: E15 runs 00308270 and the restore 0030EDA0 as shipped (0030C970 supplied);
    E16 runs the selector on the suspended unit without bit 22."""
    out = {}
    for tag in ("E15", "E16"):
        if which is not None and tag not in which:
            continue
        uc = make_uc(img)
        buf = HEAP + 0x8000
        q(uc, UNIT, 0)
        q(uc, UNIT + 0x698, STATS)
        uc.mem_write(STATS + 5, b"\x01")
        q(uc, UNIT + 0x6E0, SET_C)
        q(uc, UNIT + 0x6E8, SET_A)
        q(uc, UNIT + 0x6F0, SET_D)
        q(uc, UNIT + 0x6F8, SET_B)
        uc.mem_write(UNIT + 0x6B5, b"\x04")
        uc.mem_write(UNIT + 0x714, struct.pack("<H", 0xFFFF))

        def hook(u, addr, size, _):
            if addr == ALLOC:
                stub(u, buf)
            elif addr == MEMSET:
                d, v, n = u.reg_read(UC_X86_REG_RCX), u.reg_read(UC_X86_REG_RDX) & 0xFF, u.reg_read(UC_X86_REG_R8)
                u.mem_write(d, bytes([v]) * n)
                stub(u, d)
        hs = [uc.hook_add(UC_HOOK_CODE, hook, begin=a, end=a) for a in (ALLOC, MEMSET)]
        uc.mem_write(STACK, struct.pack("<Q", MAGIC))
        uc.reg_write(UC_X86_REG_RSP, STACK)
        uc.reg_write(UC_X86_REG_RCX, UNIT)
        uc.emu_start(SUSPEND, MAGIC, count=5000)
        for h in hs:
            uc.hook_del(h)
        zeroed = (rq(uc, UNIT + 0x6E0) == 0 and rq(uc, UNIT + 0x6F0) == 0 and rq(uc, UNIT + 0x6B5, "<B", 1) == 0
                  and rq(uc, UNIT + 0xB88) == buf and rq(uc, buf + 0x30) == SET_C and rq(uc, buf + 0x40) == SET_D
                  and rq(uc, buf + 0x5, "<B", 1) == 4)
        if tag == "E15":
            q(uc, UNIT, 1 << 22)
            r = run_sel(img, uc=uc, kind=1, real22=True)
            ok = zeroed and r["trace"] == [("bit22",), W("A"), W("C", 4), W("D"), FB] and not (r["flags"] >> 22) & 1
            report(tag, ok, "suspended (block +0x6B0..+0xB9F zeroed, copied to the buffer at +0xB88: %s), then bit 22: "
                            "00308270 -> 0030EDA0 restores it before any set is read: %s"
                   % (zeroed, " ".join(fmt_t(t) for t in r["trace"])))
        else:
            r = run_sel(img, uc=uc, kind=1)
            ok = zeroed and r["trace"] == [W("null"), W("null", 0), W("null"), FB]
            report(tag, ok, "suspended, no bit 22: every set pointer reads 0 and the fallback commits: %s"
                   % " ".join(fmt_t(t) for t in r["trace"]))
        out[tag] = r
    return out


def k9(img):
    want = {
        0x0030EFFF: "bt rax, 0x18", 0x0030F02A: "call 0x30dfa0", 0x0030F04A: "lea rax, [rbx + 0x6b0]",
        0x0030F051: "mov edx, 9", 0x0030F0AC: "mov r8d, 0x4f0", 0x0030F0E5: "lea rcx, [rbx + 0x6b0]",
        0x0030F0EC: "call 0x861ec0", 0x0030F0F1: "mov qword ptr [rbx + 0xb88], rdi",
        0x0030EDA0: "mov r8, qword ptr [rcx + 0xb88]", 0x0030EDA7: "add rcx, 0x6b0", 0x0030EDB1: "mov edx, 9",
        0x003082C6: "call 0x30eda0", 0x003082CB: "movabs rax, 0xffffbfffffbfffff",
    }
    bad = [("%08X" % a, one(img, a)[1]) for a, t in want.items() if one(img, a)[1] != t]
    r1, _ = text_refs(img, SUSPEND)
    r2, _ = text_refs(img, RESTORE)
    report("K9", not bad and [x["site"] for x in r1] == [0x0031307B] and [x["site"] for x in r2] == [0x003082C6],
           "suspend 0030EFF0 (one caller %s) copies and zeroes +0x6B0..+0xB9F (9 x 0x80 + 0x70 = 0x4F0 bytes) and keeps "
           "the buffer at +0xB88; restore 0030EDA0 (one caller %s, in 00308270) copies it back %s"
           % (["%08X" % x["site"] for x in r1], ["%08X" % x["site"] for x in r2], bad))


def fmt_t(t):
    if t[0] == "walk":
        return "%s/%d" % (t[1], t[2])
    if t[0] == "commit":
        return "commit(%s,%04X,%X,%d)" % ("01EEC298" if t[1] == FALLBACK else ("+BA0" if t[1] == UNIT + 0xBA0 else "%X" % t[1]),
                                          t[2], t[3], t[4])
    return "/".join(str(x) for x in t)


def run_switch(img, oid, kind=1, b4=0, dir_count=8, dir_null=False, row_word=2, sg0=7):
    uc = make_uc(img)
    q(uc, UNIT + 0x708, CTX)
    uc.mem_write(CTX, struct.pack("<Hh", oid, 0))
    uc.mem_write(UNIT + 0x714, struct.pack("<H", oid))
    uc.mem_write(UNIT + 0x6B4, bytes([b4, sg0]))
    q(uc, UNIT + 0x698, STATS)
    uc.mem_write(STATS + 5, bytes([kind]))
    q(uc, UNIT + 0xE60, ROW)
    for k in range(4):
        uc.mem_write(ROW + 0x50 + 2 * k, struct.pack("<H", row_word + k))
    q(uc, UNIT + 0x6E0, 0x1111)
    q(uc, DIRSLOT, 0 if dir_null else DIR)
    uc.mem_write(DIR, struct.pack("<HH", dir_count, 0))
    for i in range(16):
        uc.mem_write(DIR + 4 + 4 * i, struct.pack("<I", 0x100 * (i + 1)))
    q(uc, RTBASE, 0x40000000)
    uc.mem_write(STACK, struct.pack("<Q", MAGIC))
    uc.reg_write(UC_X86_REG_RSP, STACK)
    uc.reg_write(UC_X86_REG_RCX, UNIT)
    uc.emu_start(SWITCH, MAGIC, count=5000)
    ret = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    return {"ret": ret - (1 << 32) if ret & 0x80000000 else ret, "b4": rq(uc, UNIT + 0x6B4, "<B", 1),
            "sg": rq(uc, UNIT + 0x6B5, "<B", 1), "set": rq(uc, UNIT + 0x6E0)}


def w_cases(img, which=None):
    res = {}
    if which is None or "W1" in which:
        got = [run_switch(img, 0x4116 + k, kind=kk) for kk in (0, 1) for k in range(12)]
        ok = all(g["ret"] == 1 and g["b4"] == 2 and g["sg"] == k and g["set"] == 0x1111
                 for g, k in zip(got, list(range(12)) * 2))
        report("W1", ok, "ids 0x4116..0x4121, kind 0 and 1: +0x6B5 = 0..11, +0x6B4 = 2, return 1, +0x6E0 untouched")
    if which is None or "W2" in which:
        got = [run_switch(img, 0x4112 + k, kind=1) for k in range(4)]
        want = [0x40000000 + 0x100 * (2 + k + 1) for k in range(4)]
        ok = all(g["ret"] == 1 and g["b4"] == 2 and g["sg"] == 0 and g["set"] == w for g, w in zip(got, want))
        res["W2"] = got
        report("W2", ok, "ids 0x4112..0x4115, kind 1: +0x6E0 = [01F83530] + dir[row word +0x50+2k] (%s), +0x6B5 7 -> 0, "
                         "+0x6B4 = 2, return 1" % ["%X" % g["set"] for g in got])
    if which is None or "W3" in which:
        g = run_switch(img, 0x4113, kind=0)
        report("W3", g == {"ret": 1, "b4": 2, "sg": 7, "set": 0x1111},
               "id 0x4113 on a kind-0 unit: return 1, +0x6B4 = 2, set and subgroup untouched %s" % g)
    if which is None or "W4" in which:
        g = run_switch(img, 0x4112, kind=1, dir_count=2, row_word=2)
        report("W4", g == {"ret": -1, "b4": 0, "sg": 7, "set": 0x1111},
               "row word 2 with a 2-entry directory: return -1, +0x6B4 untouched, nothing installed %s" % g)
    if which is None or "W5" in which:
        g = run_switch(img, 0x4112, kind=1, dir_null=True)
        report("W5", g == {"ret": -1, "b4": 0, "sg": 7, "set": 0x1111},
               "null directory slot: return -1, nothing installed %s" % g)
    if which is None or "W6" in which:
        g = run_switch(img, 0x4118, kind=1, b4=2)
        report("W6", g == {"ret": 1, "b4": 2, "sg": 7, "set": 0x1111},
               "+0x6B4 already non-zero: return 1, nothing written %s" % g)
    return res


def run_verb(img, k, sg0=5, dir_count=8, row_word=2):
    uc = make_uc(img)
    uc.mem_write(UNIT + 0x6B4, bytes([0, sg0]))
    q(uc, UNIT + 0xE60, ROW)
    for i in range(4):
        uc.mem_write(ROW + 0x50 + 2 * i, struct.pack("<H", row_word + i))
    q(uc, UNIT + 0x6E0, 0x1111)
    q(uc, DIRSLOT, DIR)
    uc.mem_write(DIR, struct.pack("<HH", dir_count, 0))
    for i in range(16):
        uc.mem_write(DIR + 4 + 4 * i, struct.pack("<I", 0x100 * (i + 1)))
    q(uc, RTBASE, 0x40000000)

    def hook(u, addr, size, _):
        stub(u, UNIT)
    uc.hook_add(UC_HOOK_CODE, hook, begin=GETUNIT, end=GETUNIT)
    uc.mem_write(STACK, struct.pack("<Q", MAGIC))
    uc.reg_write(UC_X86_REG_RSP, STACK)
    uc.reg_write(UC_X86_REG_RCX, 0x1234)
    uc.reg_write(UC_X86_REG_RDX, k)
    uc.emu_start(VERB, MAGIC, count=2000)
    return {"sg": rq(uc, UNIT + 0x6B5, "<B", 1), "set": rq(uc, UNIT + 0x6E0)}


def v_cases(img):
    g = [run_verb(img, k) for k in range(4)]
    ok = all(x["sg"] == 5 and x["set"] == 0x40000000 + 0x100 * (2 + k + 1) for k, x in enumerate(g))
    report("V1", ok, "verb 3060 body 00239040, k = 0..3: +0x6E0 installed (%s), +0x6B5 kept at 5"
           % ["%X" % x["set"] for x in g])
    h = run_verb(img, 3, dir_count=1, row_word=6)
    report("V2", h["set"] == 0x40000000 + 0x100 * 10, "row word 9 with a 1-entry directory: no bound, entry 9 read "
                                                       "(+0x6E0 = %X)" % h["set"])
    return g


def main():
    print("FABLE check_s25 - the S-25 gambit set selector and the set/subgroup switch (2026-10-03)")
    print("unicorn %s" % UC_VERSION)
    img = Img.load()
    print("image sha256 verified (rvlib), base %08X" % img.base)
    report("V0", UC_VERSION.startswith("2.1.4"), "unicorn pinned 2.1.4")
    k1(img)
    k2(img)
    k3(img)
    k4(img)
    k5(img)
    k6(img)
    k7(img)
    k8(img)
    k9(img)
    e_cases(img)
    suspend_cases(img)
    w_cases(img)
    v = v_cases(img)

    def failing(fn, im):
        global fails
        before = fails
        quiet[0] = True
        try:
            fn(im)
        except Exception:
            fails += 1
        quiet[0] = False
        failed = fails > before
        fails = before
        return failed

    s1 = img.patched(0x00305C32, b"\xEB\x00")
    report("S1", failing(lambda im: e_cases(im, ("E2",)), s1), "00305C32 jmp -> 00305C34 (B's failure falls to C): E2 fails")
    s2 = img.patched(0x00305B57, b"\x90" * 6)
    report("S2", failing(lambda im: e_cases(im, ("E8",)), s2), "00305B57 je NOPed (no field-bit party skip): E8 fails")
    s3 = img.patched(0x002FE09F, b"\xC6\x83\xB5\x06\x00\x00\x05")
    report("S3", failing(lambda im: w_cases(im, ("W2",)), s3), "002FE09F stores 5: W2 fails")
    s4 = img.patched(0x002FE077, b"\x90" * 6)
    report("S4", failing(lambda im: w_cases(im, ("W4",)), s4), "002FE077 jg NOPed (no directory bound): W4 fails")
    rel = 0x0023ABA6 - (0x0023AA44 + 5)
    s5 = img.patched(0x0023AA44, b"\xE9" + struct.pack("<i", rel))
    report("S5", failing(k5, s5), "0023AA44 jmp -> 0023ABA6 (kind-1 arm through the +0x6F0 store): K5 fails")
    claim = all(x["sg"] == 0 for x in v)
    report("S6", not claim, "the mutated claim 'every variant switch restarts at subgroup 0' is refuted by V1 "
                            "(subgroups after the verb: %s)" % [x["sg"] for x in v])
    s7 = img.patched(0x003082C6, b"\x90" * 5)
    report("S7", failing(lambda im: suspend_cases(im, ("E15",)), s7), "003082C6 call 0030EDA0 NOPed (no restore): "
                                                                     "E15 fails")
    print("FAILS %d" % fails)
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
