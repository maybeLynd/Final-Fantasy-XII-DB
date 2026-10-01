"""a580_check.py - what 0042A580, the render records' +0x294 bit-20 handler, does (OPUS, 2026-09-30; DD prose residue
"0042A580 was not read" on 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md §14).
Static, kit retool.py.

A1  00427DE0 (RenderRecords_ProcessDirtyState) calls 0042A580(record) only when +0x294 bit 20 is set (004282DB-004282E4),
    clears the bit, and moves the return into edi (004282F3). 0042A580's only caller is 00427DE0.
A2  0042A580 walks the record's own node (word +0) and its first child (+8) through the 0x740-byte pool at [022C6F28],
    and the child's subtrees (+8, +0xA) through the tree walker 0042EF90 with the callback 0042E4B0; every per-node call
    goes to 0016D6A0, which is `ret 0` (the empty function); 0042A580 itself stores only its local flag and +0x294.
A3  the returned flag is the local [rsp+0x78] (0042A68D): it is read at 0042A5EA before any store to it, stored only as
    0 when a visited node's +6 is -1 (the cmoves at 0042A5F5 / 0042A636, and 0042E4B0's `mov [rdx+0x58], 0` with
    rdx = rsp+0x20), so otherwise the return is an uninitialised stack dword; the early exit (word +0 == -1,
    0042A5A7) returns it untouched.
A4  00427DE0 uses edi as its rebuild flag: 00429E50's second argument (00428465) and the 00427100 gate (00428482);
    a later handler that runs (bits 0x20, 0x20000, 0x800) sets edi = 1 and overrides it.
Prints PASS/FAIL per check and FAILS n last.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


callers = lambda f: sorted({x for x, _ in c["calls"].get(f, ())})
body = lambda f: list(R.md.disasm(R.at(f, SZ[f]), f))

ok = callers(0x0042A580) == [0x00427DE0] and txt(0x004282DB) == "bt eax, 0x14" and txt(0x004282E4) == "call 0x42a580" \
    and txt(0x004282E9) == "and dword ptr [rbx + 0x294], 0xffefffff" and txt(0x004282F3) == "mov edi, eax"
check("A1", ok, "00427DE0 runs 0042A580 on +0x294 bit 20 and keeps its return in edi")

ins = body(0x0042A580)
calls = [i.op_str for i in ins if i.mnemonic == "call"]
stores = sorted({(i.reg_name(i.operands[0].mem.base), i.operands[0].mem.disp) for i in ins
                 if len(i.operands) > 1 and i.operands[0].type == 3 and i.mnemonic not in ("cmp", "test")})
ok = R.at(0x0016D6A0, 3) == b"\xc2\x00\x00" and calls == ["0x16d6a0", "0x16d6a0", "0x42ef90", "0x42ef90", "0x808c40"] \
    and txt(0x0042A64C) == "lea rdx, [rip + 0x3e5d]" and 0x0042A653 + 0x3E5D == 0x0042E4B0 and 0x0042A66E + 0x3E42 == 0x0042E4B0 \
    and stores == [("r11", 0x10), ("r11", 0x18), ("rdi", 0x294), ("rsp", 0x78), ("rsp", 0xB0)] \
    and txt(0x0042E4D1) == "call 0x16d6a0" and txt(0x0042E4DD) == "mov dword ptr [rdi + 0x58], 0"
check("A2", ok, "per-node calls go to the empty 0016D6A0 (`ret 0`); calls %s; stores %s" % (calls, stores))

reads78 = [i.address for i in ins if "[rsp + 0x78]" in i.op_str and not i.op_str.startswith("dword ptr [rsp + 0x78]")]
writes78 = [i.address for i in ins if i.op_str.startswith("dword ptr [rsp + 0x78]")]
ok = reads78 and reads78[0] == 0x0042A5EA and writes78 and min(writes78) > 0x0042A5EA and txt(0x0042A68D) == "mov eax, dword ptr [rsp + 0x78]" \
    and txt(0x0042A5F5) == "cmove eax, esi" and txt(0x0042A636) == "cmove eax, esi" and txt(0x0042A5EE) == "xor esi, esi" \
    and txt(0x0042A5A7) == "je 0x42a683" and txt(0x0042A647) == "lea r8, [rsp + 0x20]"
check("A3", ok, "flag [rsp+0x78]: first read %s before any store (stores %s); 0 only when a node's +6 is -1"
      % (["%08X" % a for a in reads78[:1]], ["%08X" % a for a in writes78]))

ok = txt(0x00428465) == "test edi, edi" and txt(0x00428467) == "setne dl" and txt(0x0042846A) == "call 0x429e50" \
    and txt(0x00428482) == "test edi, edi" and txt(0x00428489) == "call 0x427100" \
    and txt(0x00428386) == "mov edi, 1" and txt(0x0042844F) == "mov edi, 1" and txt(0x00428479) == "mov edi, 1"
check("A4", ok, "edi is the rebuild flag: 00429E50's argument and the 00427100 gate; later handlers set it to 1")
print("FAILS %d" % fails)
