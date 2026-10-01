"""uninit.py - RC-11 part 2: what an allocation through the wrappers 0036A100 / 0036A1A0 (and 0036A190, which enters
0036A1A0) does after 0036C1D0(10, ...) selected arena 10, which no code initialises (ORACLE, 2026-09-30). Static.
Every instruction quoted is asserted against the image (exit 1 on a failure).

  S1 the push 0036C1D0 -> 0036C1F0 installs the active arena 022D89BC = map[022D89A8 + 10] (0036C262-0036C27F); the
     map is identity for ids 0-14 (memory page: its only writers are the two identity fills), so 022D89BC = 10. The
     push first raises stack 0's depth 022D89C0 by one (0036C25A-0036C25E).
  S2 0036A100 passes ecx = [022D89BC] = 10, edx = size, r8 = 0, r9 = 0 to 0036BC60 (0036A10F-0036A11F); 0036A1A0
     passes the same with r9 = 1 (0036A1B4-0036A1C9).
  S3 0036BC60 with r8 = 0: spins only when the depth 022D89C0 is 0 (0036BC7E-0036BC87), which the push has made 1 or
     more, so it goes on; ecx = 10 <= 14 selects the descriptor 022D7FD0 + 10 * 0xA8 = 022D8660 (0036BCA1-0036BCBE);
     it writes byte 1 at descriptor +2, 022D8662 (0036BCC5); then tests bit 10 of the init mask 022D89B8 (0036BCD2-
     0036BCDB). The bit is clear, so it returns 0 (0036BCDD-0036BCE9) without touching the free list.
  S4 the wrapper, seeing 0, calls 0036BFE0 with ecx = [022D89BC] = 10 (0036A12E-0036A149; 0036A1D8-0036A1F0).
     0036BFE0 tests bit 10 of 022D89B8 first (0036BFF0-0036BFFB); clear, it falls into `jmp 0x36c000` at 0036C000,
     a jump to itself: the thread spins forever. It never returns, so the wrapper never stamps a header and 0036C140
     (the pop) never runs.
  S5 bit 10 is never set: the mask's only store is 00369DE7 in the initializer 00369D30 (riprefs_022D89B8.out,
     basedisp_022D89B8.out), which ORs 1 << id for the id it is given, and no caller gives 10 (arena_ids.out:
     ids 2-9, 0xB, 0xC, 0xD, 0xE).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import img  # noqa: E402

FAILS = []


def ins(a):
    x = img.dis(a, 16)[0]
    return ("%s %s" % (x.mnemonic, x.op_str)).strip()


def expect(a, t):
    ok = ins(a) == t
    print("%s  %08X  %-44s%s" % ("PASS" if ok else "FAIL", a, ins(a), "" if ok else " (expected %s)" % t))
    if not ok:
        FAILS.append(a)


def rip(a):
    return img.ripmem(img.dis(a, 16)[0])


def main():
    print("-- S1 push installs map[10]")
    expect(0x0036C1DF, "jmp 0x36c1f0")
    expect(0x0036C25A, "lea eax, [r8 + 1]")
    expect(0x0036C25E, "mov dword ptr [r11 + rbx], eax")
    expect(0x0036C262, "movsxd rax, ecx")
    expect(0x0036C272, "movzx eax, byte ptr [rax + rbx + 0x21b89a8]")
    ok = rip(0x0036C27F) == 0x022D89BC
    print("%s  0036C27F stores the active arena 022D89BC" % ("PASS" if ok else "FAIL")); FAILS.extend([] if ok else [1])
    print("-- S2 wrappers")
    expect(0x0036A113, "mov ecx, dword ptr [rip + 0x1f6e8a3]")
    expect(0x0036A119, "xor r9d, r9d")
    expect(0x0036A11C, "xor r8d, r8d")
    expect(0x0036A11F, "call 0x36bc60")
    expect(0x0036A190, "mov edx, 1")
    expect(0x0036A195, "jmp 0x36a1a0")
    expect(0x0036A1C0, "mov ecx, dword ptr [rip + 0x1f6e7f6]")
    expect(0x0036A1C6, "xor r8d, r8d")
    expect(0x0036A1C9, "call 0x36bc60")
    print("-- S3 0036BC60 on arena 10")
    expect(0x0036BC65, "mov dword ptr [rsp + 8], ecx")
    expect(0x0036BC79, "test r8, r8")
    expect(0x0036BC7E, "cmp dword ptr [rip + 0x1f6cd3b], r8d")
    expect(0x0036BC87, "jmp 0x36bc87")
    expect(0x0036BCA1, "cmp ecx, 0xe")
    expect(0x0036BCB0, "imul rbx, rcx, 0xa8")
    expect(0x0036BCB7, "mov ecx, dword ptr [rsp + 0x80]")
    expect(0x0036BCC5, "mov byte ptr [rbx + 2], 1")
    expect(0x0036BCD2, "mov eax, dword ptr [rip + 0x1f6cce0]")
    expect(0x0036BCD8, "bt eax, ecx")
    expect(0x0036BCDB, "jb 0x36bcea")
    expect(0x0036BCDD, "xor eax, eax")
    expect(0x0036BCE9, "ret")
    ok = rip(0x0036BCA9) == 0x022D7FD0 and rip(0x0036BCD2) == 0x022D89B8 and rip(0x0036BC7E) == 0x022D89C0
    print("%s  descriptors 022D7FD0, mask 022D89B8, depth 022D89C0; arena 10's descriptor 022D8660, mark byte 022D8662"
          % ("PASS" if ok else "FAIL")); FAILS.extend([] if ok else [2])
    print("-- S4 retry 0036BFE0 spins")
    expect(0x0036A149, "call 0x36bfe0")
    expect(0x0036A1F0, "call 0x36bfe0")
    expect(0x0036BFF0, "mov eax, dword ptr [rip + 0x1f6c9c2]")
    expect(0x0036BFF8, "bt eax, ecx")
    expect(0x0036BFFB, "jb 0x36c002")
    expect(0x0036C000, "jmp 0x36c000")
    print("-- S5 the mask's only store")
    expect(0x00369DE7, "mov dword ptr [rip + 0x1f6ebca], r9d")
    print("RESULT %s" % ("PASS" if not FAILS else "FAIL %s" % FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
