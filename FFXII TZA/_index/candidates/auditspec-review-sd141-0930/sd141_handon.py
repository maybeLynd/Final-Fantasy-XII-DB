"""sd141_handon.py - SWE2-AUDIT-SPEC (SD-141 review, 2026-09-30). The handed-on base the package's F3 does not follow.

  H1 0060890A `lea rdx, [02CB8160]` (pair - 0x2B0) in 006084B0; rdx is not rewritten before 00608999 `call 005DEC50`
     with rcx = rdi + 0x2A0.
  H2 005DEC50 (no .pdata entry: a leaf) copies dwords [rdx + d] -> [rcx + d] up to its ret; list the reads at
     d = 0x2B0 / 0x2B4 (= 02CB8410 / 02CB8414 when rdx = 02CB8160) and the maximum d.
  H3 the caller of 006084B0 (00604879 in 00604750) passes rcx = rbp + 0x270, so the pair lands at rbp + 0x7C0 / 0x7C4;
     list every [rbp + 0x7B0 .. 0x7CF] operand of 00604750 and every lea of rbp + 0x270 (the struct handed on).
"""
import sdx

fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def body(a, b):
    o = sdx.off(a)
    return list(sdx.md.disasm(sdx.raw[o:o + (b - a)], a))


# H1
ins = body(0x0060890A, 0x0060899E)
for i in ins:
    print("  %08X %s %s" % (i.address, i.mnemonic, i.op_str))
rdx_w = [i for i in ins[1:] if i.op_str.startswith(("rdx", "edx", "dx,", "dl,")) and i.mnemonic not in ("cmp", "test")]
check("H1", ins[0].op_str == "rdx, [rip + 0x26af84f]" and ins[0].address + ins[0].size + 0x26af84f == 0x02CB8160
      and ins[-1].mnemonic == "call" and ins[-1].op_str == "0x5dec50" and not rdx_w
      and any(i.op_str == "rcx, [rdi + 0x2a0]" for i in ins),
      "006084B0 hands 02CB8160 in rdx to 005DEC50 (rcx = rdi + 0x2A0); rdx not rewritten in between")
# H2
o = sdx.off(0x005DEC50)
reads, end = [], None
for i in sdx.md.disasm(sdx.raw[o:o + 0x1000], 0x005DEC50):
    for m, sz in sdx.mem_ops(i):
        if i.reg_name(m.base) == "rdx":
            reads.append((i.address, m.disp, sz, "%s %s" % (i.mnemonic, i.op_str)))
    if i.mnemonic == "ret":
        end = i.address
        break
hit = [r for r in reads if r[1] in (0x2B0, 0x2B4)]
for r in hit:
    print("  %08X d=0x%X w%d  %s   -> global %08X" % (r[0], r[1], r[2], r[3], 0x02CB8160 + r[1]))
print("  005DEC50: %d [rdx+d] reads, max d 0x%X, ret at %08X, .pdata entry: %s; callers %s" % (
    len(reads), max(r[1] for r in reads), end, sdx.pdata_of(0x005DEC50), ["%08X %s" % x for x in sdx.rel32(0x005DEC50) + sdx.jcc(0x005DEC50)]))
check("H2", [r[0] for r in hit] == [0x005DF3A0, 0x005DF3AC] and all(r[2] == 4 for r in hit),
      "005DEC50 reads [rdx + 0x2B0] and [rdx + 0x2B4] = 02CB8410 / 02CB8414 (dword each)")
# H3
print("  00604879: %s   (preceded by %s)" % (sdx.txt(0x00604879), sdx.txt(0x00604872)))
e = sdx.pdata_of(0x00604750)
lst = []
for i in body(0x00604750, sdx.IB + e[1]):
    for m, sz in sdx.mem_ops(i):
        if i.reg_name(m.base) == "rbp" and (0x7B0 <= m.disp < 0x7D0 or (i.mnemonic == "lea" and m.disp == 0x270)):
            lst.append(i)
            print("  %08X %s %s" % (i.address, i.mnemonic, i.op_str))
check("H3", sdx.txt(0x00604872) == "lea rcx, [rbp + 0x270]" and sdx.txt(0x00604879) == "call 0x6084b0"
      and sdx.txt(0x00605F66) == "movss xmm1, dword ptr [rbp + 0x7c0]" and sdx.txt(0x00605F6E) == "movss dword ptr [r14 + 0x5d4], xmm1"
      and sdx.txt(0x00605F88) == "movss xmm1, dword ptr [rbp + 0x7c4]" and sdx.txt(0x00605F90) == "movss dword ptr [r14 + 0x5dc], xmm1"
      and sdx.txt(0x006048B5) == "mov r8d, 0x598" and sdx.txt(0x006048C2) == "call 0x861ed2",
      "the snapshot at rbp+0x270 carries the pair at +0x550 / +0x554; 00604750 re-reads them (00605F66, 00605F88) into "
      "[r14+0x5D4] / [r14+0x5DC] and memcpy's the whole 0x598-byte snapshot (006048C2)")
print("  00861ED2: %s" % sdx.txt(0x00861ED2))
print("FAILS %d" % fails)
