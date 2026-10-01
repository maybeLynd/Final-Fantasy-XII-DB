"""falsify_interp_dispatch.py - falsification pass 2026-10-01 (SWE2-CONTRACT for OPUS) on
01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md. Static. Reads only.

Attacked claim (the page's most load-bearing one): the 100-entry computed-goto dispatch of
WorldActorScriptVM_InterpretBytecode 0025E4C0 (sections 2, 3, 4, 13.1): the image-base rebase, the 0x63 bound and its
default 0025E60A, the 32-bit RVA table at 00261DF8, every target inside the one function, 92 distinct targets, exactly
three shared groups, and the register-file handlers 0x36-0x45. Also attacked: the SECTION-11 entry facts that reopened
the page (the shared value-stack depth 02099AC0 is zeroed before the refusal test; the 65,536 instruction budget) and
the operand pre-decode threshold 0x47.

Every check prints PASS or FAIL. The positive controls run the same table checks on deliberately corrupted copies of
the table and must FAIL there; a control that does not catch its corruption counts as a FAIL. Last line: FAILS n.
"""
import hashlib, io, os, struct, sys
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "swe2contract-ddres-b1-0930"))
import block_writer_disjoint as b  # noqa: E402  (PE section mapper and functions.tsv extents)

SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x00120000
FN, FN_SIZE, FN_INSNS = 0x0025E4C0, 14646, 3229
TABLE = 0x00261DF8
DEFAULT = 0x0025E60A
GROUPS = {0x0025E60A: [0x01, 0x02, 0x19, 0x1A, 0x31, 0x47], 0x0026121A: [0x2A, 0x2B, 0x2C], 0x002618A8: [0x51, 0x60]}
REG = {  # opcode: handler, from section 13.1
    0x36: 0x0026161C, 0x37: 0x0026162D, 0x38: 0x0026163E, 0x39: 0x0026164F,
    0x3A: 0x00261660, 0x3B: 0x00261673, 0x3C: 0x00261686, 0x3D: 0x00261699,
    0x3E: 0x002616AF, 0x3F: 0x002616C0, 0x40: 0x002616D1, 0x41: 0x002616E2,
    0x42: 0x002616F3, 0x43: 0x00261706, 0x44: 0x00261719, 0x45: 0x0026172C}

fails = 0


def check(cid, ok, what):
    global fails
    print("%s %s %s" % ("PASS" if ok else "FAIL", cid, what))
    if not ok:
        fails += 1


exe = io.open(b.EXE, "rb").read()
check("I0", hashlib.sha256(exe).hexdigest() == SHA, "image is the certified FFXII_TZA.exe 73461d08...")
at = b.load()
ext = b.extents()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True

# I1 extent and instruction count
size = ext.get(FN)
ins = list(md.disasm(at(FN, size or FN_SIZE), FN)) if size else []
byaddr = {i.address: i for i in ins}
check("I1", size == FN_SIZE and len(ins) == FN_INSNS and sum(i.size for i in ins) == FN_SIZE,
      "0025E4C0 is %s B and decodes linearly to %d instructions covering it (page: 14,646 B, 3,229)" % (size, len(ins)))
check("I1b", TABLE >= FN + FN_SIZE, "the table 00261DF8 lies past the body end %08X, so the linear decode does not "
      "run through it" % (FN + FN_SIZE))


def insn(a):
    return byaddr.get(a)


# I2 the rebase: lea r8, [rip - 0x13E5DD] at 0025E5D6 -> 0x00120000
i = insn(0x0025E5D6)
ok = i is not None and i.mnemonic == "lea" and i.operands[1].mem.base == X.X86_REG_RIP and \
    i.address + i.size + i.operands[1].mem.disp == BASE and i.reg_name(i.operands[0].reg) == "r8"
check("I2", ok, "0025E5D6 lea r8, [rip%+#x] resolves to %08X (page: the image base 00120000)" %
      ((i.operands[1].mem.disp, i.address + i.size + i.operands[1].mem.disp) if i else (0, 0)))

# I3 the bound: cmp eax, 0x63 / ja 0025E60A
c, j = insn(0x0025E5D1), insn(0x0025E5D4)
ok = c is not None and c.mnemonic == "cmp" and c.operands[1].type == X.X86_OP_IMM and c.operands[1].imm == 0x63 and \
    j is not None and j.mnemonic == "ja" and j.operands[0].imm == DEFAULT
check("I3", ok, "0025E5D1 cmp eax, 0x63 then 0025E5D4 ja 0025E60A (opcodes 0x00-0x63, out of range -> default)")

# I4 the load: mov ecx, [r8 + rax*4 + 0x141DF8], add rcx, r8, jmp rcx
m, a_, jj = insn(0x0025E5DD), insn(0x0025E5E5), insn(0x0025E5E8)
ok = m is not None and m.mnemonic == "mov" and m.operands[1].mem.scale == 4 and \
    BASE + m.operands[1].mem.disp == TABLE and a_ is not None and a_.mnemonic == "add" and \
    jj is not None and jj.mnemonic == "jmp" and jj.operands[0].type == X.X86_OP_REG
check("I4", ok, "0025E5DD scaled-by-4 dword load at base + %#x = %08X, add, jmp reg (page: RVA table at 00261DF8)" %
      (m.operands[1].mem.disp if m else 0, BASE + (m.operands[1].mem.disp if m else 0)))


def table_checks(tbl, tag):
    """the table claims; returns a list of (id, ok, text)."""
    tg = [BASE + v for v in tbl]
    out = []
    inside = [t for t in tg if FN <= t < FN + FN_SIZE]
    out.append(("I5" + tag, len(tg) == 100 and len(inside) == 100,
                "all %d entries land inside 0025E4C0's extent (%d inside)" % (len(tg), len(inside))))
    on_boundary = [t for t in tg if t in byaddr]
    out.append(("I6" + tag, len(on_boundary) == 100,
                "every target is an instruction start of the linear decode (%d of 100)" % len(on_boundary)))
    out.append(("I7" + tag, len(set(tg)) == 92, "distinct targets: %d (page: 92)" % len(set(tg))))
    shared = {}
    for op, t in enumerate(tg):
        shared.setdefault(t, []).append(op)
    shared = {t: ops for t, ops in shared.items() if len(ops) > 1}
    out.append(("I8" + tag, shared == GROUPS, "shared targets: %s (page: 0025E60A <- 01 02 19 1A 31 47; 0026121A <- "
                "2A 2B 2C; 002618A8 <- 51 60)" % "; ".join("%08X <- %s" % (t, " ".join("%02X" % o for o in ops))
                                                         for t, ops in sorted(shared.items()))))
    out.append(("I9" + tag, min(tg) == 0x0025E5EA and max(tg) == 0x00261D36,
                "handler targets span %08X-%08X (page: 0025E5EA-00261D36)" % (min(tg), max(tg))))
    out.append(("I10" + tag, all(tg[op] == h for op, h in REG.items()),
                "opcodes 0x36-0x45 dispatch to the sixteen section-13.1 handlers"))
    return out


raw = at(TABLE, 400)
tbl = list(struct.unpack("<100I", raw))
for cid, ok, what in table_checks(tbl, ""):
    check(cid, ok, what)

# I11 the register-file handler bodies: mov rcx, r10 / call pop -> store [r15 + 0x64/0x74 + 4n]; load -> call push
POPI, POPF, PUSHI, PUSHF = 0x00267E10, 0x00267DB0, 0x00267F90, 0x00267F60
bad = []
for op, h in REG.items():
    n = (op - 0x36) % 4
    body = list(md.disasm(at(h, 32), h, 4))
    txt = " ; ".join("%s %s" % (x.mnemonic, x.op_str) for x in body)
    kind = (op - 0x36) // 4
    if kind == 0:
        want = ["mov rcx, r10", "call 0x%x" % POPI, "mov dword ptr [r15 + 0x%x], eax" % (0x64 + 4 * n)]
    elif kind == 1:
        want = ["mov rcx, r10", "call 0x%x" % POPF, "movss dword ptr [r15 + 0x%x], xmm0" % (0x74 + 4 * n)]
    elif kind == 2:
        want = ["mov edx, dword ptr [r15 + 0x%x]" % (0x64 + 4 * n), "mov rcx, r10", "call 0x%x" % PUSHI]
    else:
        want = ["movss xmm1, dword ptr [r15 + 0x%x]" % (0x74 + 4 * n), "mov rcx, r10", "call 0x%x" % PUSHF]
    if [w for w in want if w not in txt]:
        bad.append("%02X@%08X: %s" % (op, h, txt))
check("I11", not bad, "the sixteen register handlers move I0-I3 at r15+0x64.. and F0-F3 at r15+0x74.. through the "
      "pop/push helpers%s" % ("" if not bad else " - " + " | ".join(bad)))

# I12 SECTION-11: depth zeroed at entry before the refusal test, on every path
z, st, t40, jn, ret1 = insn(0x0025E4D2), insn(0x0025E4D8), insn(0x0025E4FF), insn(0x0025E502), insn(0x0025E511)
ok = z is not None and z.mnemonic == "xor" and z.op_str == "r11d, r11d" and st is not None and st.mnemonic == "mov" \
    and st.operands[0].type == X.X86_OP_MEM and st.operands[0].mem.base == X.X86_REG_RIP and \
    st.address + st.size + st.operands[0].mem.disp == 0x02099AC0 and st.op_str.endswith("r11d") and \
    t40 is not None and t40.op_str == "dl, 0x40" and jn is not None and jn.operands[0].imm == 0x0025E511 and \
    ret1 is not None and ret1.op_str == "eax, 1"
# no branch between the entry and the store
early = [x for x in ins if FN <= x.address < 0x0025E4D8 and x.group(capstone.CS_GRP_JUMP)]
check("I12", ok and not early, "0025E4D2 xor r11d,r11d; 0025E4D8 stores it to dword 02099AC0 before any branch; the "
      "refusal test 0025E4FF/0025E502 then returns 1 at 0025E511 (SECTION-11: depth reset even on refusal)")

# I13 SECTION-11: the instruction budget 0x10000, decremented by ebp = 1 per dispatched instruction
bud, one, dec_ = insn(0x0025E4FA), insn(0x0025E555), insn(0x0025E570)
ok = bud is not None and bud.op_str == "ecx, 0x10000" and one is not None and one.op_str == "ebp, 1" and \
    dec_ is not None and dec_.mnemonic == "sub" and dec_.op_str == "ecx, ebp"
check("I13", ok, "0025E4FA mov ecx, 0x10000; 0025E555 mov ebp, 1; 0025E570 sub ecx, ebp (budget 65,536)")

# I14 the operand pre-decode: cmp r12b, 0x47 / jb -> no operand; else b[pc+2]<<8 | b[pc+1]
c47, jb, o2 = insn(0x0025E5A9), insn(0x0025E5AD), insn(0x0025E5AF)
ok = c47 is not None and c47.op_str == "r12b, 0x47" and jb is not None and jb.mnemonic == "jb" and \
    o2 is not None and o2.op_str == "ebx, byte ptr [r14 + 2]"
check("I14", ok, "0025E5A9 cmp r12b, 0x47 / 0025E5AD jb; 0025E5AF reads byte [pc+2] (pre-decode from 0x47)")

# I15 the default handler's body (section 4): mov [rsp+0xC0], ebp ; mov edi, ebp, then the common path
d1 = insn(DEFAULT)
d2 = insn(DEFAULT + d1.size) if d1 else None
ok = d1 is not None and d1.mnemonic == "mov" and d1.op_str == "dword ptr [rsp + 0xc0], ebp" and \
    d2 is not None and d2.mnemonic == "mov" and d2.op_str == "edi, ebp"
check("I15", ok, "0025E60A is mov dword [rsp+0xC0], ebp ; mov edi, ebp (the inert six carry no behaviour of their own)")

# Positive controls: corrupted copies of the table must fail the matching checks
c1 = list(tbl); c1[0x36] = (0x00262000 - BASE)                  # one handler moved outside the function
c2 = list(tbl); c2[0x03] = c2[0x04]                               # one extra shared target
c3 = list(tbl); c3[0x19] = c3[0x18]                               # remove 0x19 from the inert six
r1 = {cid: ok for cid, ok, _ in table_checks(c1, "")}
r2 = {cid: ok for cid, ok, _ in table_checks(c2, "")}
r3 = {cid: ok for cid, ok, _ in table_checks(c3, "")}
check("C1", not r1["I5"] and not r1["I10"], "control: entry 0x36 repointed to 00262000 -> I5 and I10 FAIL on the copy")
check("C2", not r2["I7"] and not r2["I8"], "control: entry 0x03 duplicated from 0x04 -> I7 (91 distinct) and I8 FAIL")
check("C3", not r3["I8"], "control: entry 0x19 taken out of the default group -> I8 FAIL")

print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
