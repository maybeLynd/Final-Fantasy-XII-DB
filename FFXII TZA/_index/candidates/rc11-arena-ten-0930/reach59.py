"""reach59.py - RC-11 part 1: can the arena-10 branch of the 0x59 record loader (00504394 not taken -> 00504398) run?
(ORACLE, 2026-09-30). Static. Reads only. Every fact is asserted against the decoded image (exit 1 on a failure).

The branch tests byte [ [02F97340] ] >= 10 (00504383-00504394). [02F97340] is the published effect context; its byte
+0 is the context's type, copied from the constructor's 0x890-byte template by 0024B3A0 (0024B3C0-0024B432) and used
there as the index of the per-type list heads 020910A0[type] (0024B435-0024B457).

Chain asserted here:
  A1 00504350 has exactly two direct callers, 003AA109 (in 003A9EF0) and 00500A20 (in 00500980); 00500980's only
     caller is 003A9F42 (in 003A9EF0); 003A9EF0's only caller is 003EDAA0 (in 003ED8A0, chunk type 0xB00);
     003ED8A0's only caller is 003EE39B (in 003EE2D0, chunk flag 0x100); 003EE2D0's only caller is 003EE1F2 in the EFX
     parse 003EDAD0. No other reference to these entries except their .pdata / unwind records (checked: rva32 and
     abs64 occurrences outside .pdata are listed).
  A2 003EDAD0's callers are exactly the six context constructors, and 0024B3A0's callers are the same six.
  A3 each constructor stores a constant type byte into its template before 0024B3A0: 2, 1, 5, 7, 4, 3.
  A4 between each constructor's 0024B3A0 call and its 003EDAD0 call there is no store to 02F97340 other than the
     returned context itself (0026FC9F stores rax = 0024B3A0's result) and no callee that stores it (closure.py).
  A5 inside the parse's direct-call closure the only store to 02F97340 is 0024ED80, reached only from 003EE2D0's arms
     for chunk flags 0x101 and 0x102 (003EE33D-003EE344, 003EE365-003EE36C); b00_census.py's C1 shows every shipped
     chunk carries flag 0x100.
  A6 (design bound, reported) the per-type heads 020910A0 hold 10 qwords (the next table, 020910F0, starts 0x50
     later), and the parse's own run-collection gate reads the type as at most 9 (003EDBA2-003EDBB3: cmp al, 9; ja;
     bt 0x37D).
Result: on shipped data the context is always of type 1, 2, 3, 4, 5 or 7 when 00504350 runs, so the loader always
takes 005043A7: 0036C1D0(8, 10) then 0036A190. The arena-10 call 00504398 is unreachable with shipped data.
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import img  # noqa: E402
import closure  # noqa: E402

FAILS = []


def check(ok, text):
    print("%s  %s" % ("PASS" if ok else "FAIL", text))
    if not ok:
        FAILS.append(text)


def callers(t):
    return sorted((a, k, img.owner(a)) for a, k in img.calls_to(t))


def other_refs(t):
    p = img.sec(".pdata")
    out = []
    for pat, nm in ((struct.pack("<Q", t), "abs64"), (struct.pack("<I", t - img.BASE), "rva32")):
        i = img.blob.find(pat)
        while i != -1:
            if not (p[3] <= i < p[3] + p[4]):
                out.append((nm, i))
            i = img.blob.find(pat, i + 1)
    return out


def ins(a):
    x = img.dis(a, 16)[0]
    return ("%s %s" % (x.mnemonic, x.op_str)).strip()


def main():
    # A1
    chain = [(0x00504350, [(0x003AA109, "call", 0x003A9EF0), (0x00500A20, "call", 0x00500980)]),
             (0x00500980, [(0x003A9F42, "call", 0x003A9EF0)]),
             (0x003A9EF0, [(0x003EDAA0, "call", 0x003ED8A0)]),
             (0x003ED8A0, [(0x003EE39B, "call", 0x003EE2D0)]),
             (0x003EE2D0, [(0x003EE1F2, "call", 0x003EDAD0)])]
    for t, want in chain:
        got = callers(t)
        check(got == sorted(want), "A1 callers of %08X: %s" % (t, ["%08X in %08X" % (a, o or 0) for a, _k, o in got]))
        print("      non-.pdata references to %08X: %s" % (t, [(n, hex(i)) for n, i in other_refs(t)]))
    check(ins(0x003EDA81) == "cmp r8d, 0xb00" and ins(0x003EDAA0) == "call 0x3a9ef0", "A1 003ED8A0 arm 0xB00")
    check(ins(0x003EE2EE) == "sub r8d, 0x100" and ins(0x003EE39B) == "call 0x3ed8a0", "A1 003EE2D0 arm flag 0x100")
    # A2
    ctors = {0x0026FB90, 0x002FC4A0, 0x003B0660, 0x003B2220, 0x003B29B0, 0x003B38B0}
    pc = {o for _a, _k, o in callers(0x003EDAD0)}
    cc = {o for _a, _k, o in callers(0x0024B3A0)}
    check(pc == ctors and cc == ctors, "A2 callers of 003EDAD0 and of 0024B3A0 are the six constructors")
    # A3
    stores = {0x0026FC6C: "mov byte ptr [rsp + 0x20], 2", 0x002FC541: "mov byte ptr [rsp + 0x30], 1",
              0x003B0730: "mov byte ptr [rsp + 0x30], 5", 0x003B2250: "mov byte ptr [rsp + 0x20], 7",
              0x003B2A60: "mov byte ptr [rsp + 0x20], 4", 0x003B3977: "mov byte ptr [rsp + 0x20], 3"}
    for a, t in sorted(stores.items()):
        check(ins(a) == t, "A3 %08X %s" % (a, ins(a)))
    check(ins(0x0024B435) == "movzx ecx, byte ptr [rdi]" and ins(0x0024B477).startswith("mov qword ptr [rip"),
          "A3 0024B3A0 indexes the heads by template byte +0 and publishes the copy at 0024B477")
    check(ins(0x00504392) == "cmp byte ptr [rax], dl" and ins(0x00504383) == "mov edx, 0xa"
          and ins(0x00504394) == "jb 0x5043a7" and ins(0x005043A7) == "mov ecx, 8", "A3 the branch: type < 10 -> arena 8")
    # A4
    from capstone.x86 import X86_OP_IMM
    windows = ((0x0026FB90, 0x0026FC8A, 0x0026FCEE), (0x002FC4A0, 0x002FC54B, 0x002FC5D2),
               (0x003B2220, 0x003B2255, 0x003B226D), (0x003B29B0, 0x003B2A6A, 0x003B2A75),
               (0x003B38B0, 0x003B39A4, 0x003B39B3), (0x003B0660, 0x003B073A, 0x003B0745))
    for fn, a, b in windows:
        w = [x for x in img.fn_ins(fn) if a < x.address < b]
        direct = [x.address for x in w if img.ripmem(x) == 0x02F97340 and x.mnemonic == "mov" and x.operands[0].type == 3]
        bad = []
        for x in w:
            if x.mnemonic == "call" and x.operands[0].type == X86_OP_IMM:
                if closure.closure(x.operands[0].imm)[2]:
                    bad.append(x.operands[0].imm)
        ind = [("%08X" % x.address, x.op_str) for x in w if x.mnemonic == "call" and x.operands[0].type != X86_OP_IMM]
        ok = not bad and all(d == 0x0026FC9F for d in direct)
        check(ok, "A4 %08X window %08X..%08X: direct stores %s, storing callees %s, indirect %s" % (
            fn, a, b, ["%08X" % d for d in direct], bad, ind))
    check(ins(0x0026FC8F) == "mov rbx, rax" and ins(0x0026FC9F) == "mov qword ptr [rip + 0x2d2769a], rax",
          "A4 0026FC9F republishes 0024B3A0's own result")
    # A5
    s, _ind, st = closure.closure(0x003EDAD0)
    check([(f, a) for f, a, _o in st] == [(0x0024ED80, 0x0024ED87)], "A5 only store in the parse closure: 0024ED87")
    inside = sorted(a for a, _k, o in callers(0x0024ED80) if o in s)
    check(inside == [0x003EE344, 0x003EE36C], "A5 0024ED80 reached in the closure only from %s" % ["%08X" % a for a in inside])
    # A6
    check(ins(0x0024F68B).startswith("lea rdx, [rip") and img.ripmem(img.dis(0x0024F68B, 8)[0]) == 0x020910F0,
          "A6 the next table 020910F0 is 0x50 bytes above the heads 020910A0 (10 qwords)")
    check(ins(0x003EDBA5) == "cmp al, 9" and ins(0x003EDBA9) == "mov edx, 0x37d", "A6 the parse reads the type as at most 9")
    print("RESULT %s" % ("PASS" if not FAILS else "FAIL"))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
