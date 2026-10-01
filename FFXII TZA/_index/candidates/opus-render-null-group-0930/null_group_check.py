"""null_group_check.py - can 0041CF00 hand 00372280 a null group? (OPUS, 2026-09-30; DD prose residue on
17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md section 10). Static, kit retool.py.

N1  0041CF00: when payload +0xC has bit 0x1000 and +0x338 == -1 it calls 00372280 with rcx = 0 (rcx is zeroed at
    0041CF09 and the subrecord loop only stores it).
N2  00372280 dereferences rcx (+0x84) before any test of rcx.
N3  image-wide, the only instruction that sets bit 0x1000 of a dword at +0xC by an OR is 0041D4D0's (every other
    immediate `mov` with that bit is listed: -1 or float constants; AND masks only clear bits and are not setters); 0041D4D0's only caller is 00424550.
N4  00424550 calls 0041D4D0(payload, 1) at 004247FA only after the admission 0051BA80 (004247AD), whose definition at
    rsp+0x30 carries +0x14 = [rdi+0x18] (00424722), on a path entered only when [rdi+0x18] != -1 (00424653).
N5  0041D220 (the admission's builder) stores definition +0x14 into +0x338 (0041D26D-0041D270); 0041CB90 stores -1 at
    +0x338 and runs before 0041D220 in the admission (0051BACA, 0051BAD7) and at 0041CF00's tail, after the bit is
    cleared (0041CFAC, 0041CFBB).
Control: the N3 census finds 0041D4D0's own OR (positive control) and the -1 store 0051F202 of the container node.
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


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


callers = lambda f: sorted({x for x, _ in c["calls"].get(f, ())})

ins = body(0x0041CF00)
rcx_writes = [i.address for i in ins if i.operands and i.operands[0].type == 1 and i.reg_name(i.operands[0].reg) in ("rcx", "ecx", "cx", "cl")
              and len(i.operands) > 1 and i.mnemonic not in ("cmp", "test")]
# rcx is written only at 0041CF09 (zero), 0041CF98 / 0041CFA4 (the group lookup, on the +0x338 != -1 branch) and 0041CFB3
ok = txt(0x0041CF09) == "xor ecx, ecx" and txt(0x0041CF84) == "test dword ptr [rbx + 0xc], 0x1000" \
    and txt(0x0041CF8D) == "mov edx, dword ptr [rbx + 0x338]" and txt(0x0041CF96) == "je 0x41cfa7" \
    and txt(0x0041CFA7) == "call 0x372280" and rcx_writes == [0x0041CF09, 0x0041CF98, 0x0041CFA4, 0x0041CFB3]
check("N1", ok, "0041CF00: bit 0x1000 with +0x338 == -1 -> 00372280(rcx = 0); rcx written only at %s"
      % " ".join("%08X" % a for a in rcx_writes))

ins = body(0x00372280)
first_rcx = next((i for i in ins for op in i.operands if op.type == 3 and op.mem.base and i.reg_name(op.mem.base) == "rcx"), None)
tests = [i.address for i in ins if i.mnemonic == "test" and "rcx" in i.op_str and first_rcx and i.address < first_rcx.address]
ok = first_rcx is not None and first_rcx.operands[1 if first_rcx.operands[0].type != 3 else 0].mem.disp == 0x84 and not tests
check("N2", ok, "00372280's first access through rcx is %08X `%s %s`, with no test of rcx before it"
      % (first_rcx.address, first_rcx.mnemonic, first_rcx.op_str) if first_rcx else "no rcx access")

ors, movs = [], []
for f, n in SZ.items():
    try:
        fi = list(R.md.disasm(R.at(f, n), f))
    except Exception:
        continue
    for i in fi:
        o = i.operands
        if len(o) == 2 and o[0].type == 3 and o[0].size == 4 and o[0].mem.disp == 0xC and o[0].mem.base \
                and i.reg_name(o[0].mem.base) != "rip" and o[1].type == 2 and (o[1].imm & 0x1000):
            ({"or": ors, "mov": movs}.get(i.mnemonic, [])).append((f, i.address, i.mnemonic, o[1].imm & 0xFFFFFFFF))
ok = [(f, a) for f, a, _, _ in ors] == [(0x0041D4D0, 0x0041D4D9)] and all(m == "mov" for _, _, m, _ in movs) \
    and (0x0051F190, 0x0051F202, "mov", 0xFFFFFFFF) in movs and callers(0x0041D4D0) == [0x00424550]
check("N3", ok, "OR-setters of +0xC bit 0x1000: %s; mov stores with the bit: %s; 0041D4D0 callers %s"
      % (["%08X" % a for _, a, _, _ in ors], ["%08X=%X" % (a, v) for _, a, _, v in movs], ["%08X" % x for x in callers(0x0041D4D0)]))

ok = txt(0x00424653) == "cmp dword ptr [rdi + 0x18], -1" and txt(0x00424657) == "je 0x424842" \
    and txt(0x0042471F) == "mov eax, dword ptr [rdi + 0x18]" and txt(0x00424722) == "mov dword ptr [rsp + 0x44], eax" \
    and txt(0x00424793) == "lea rcx, [rsp + 0x30]" and txt(0x004247A1) == "mov qword ptr [rsp + 0x20], rcx" \
    and txt(0x004247AD) == "call 0x51ba80" and txt(0x004247EF) == "mov edx, 1" and txt(0x004247FA) == "call 0x41d4d0"
check("N4", ok, "00424550: admission definition +0x14 = [rdi+0x18], reached only when it is not -1, then 0041D4D0(payload, 1)")

ok = txt(0x0041D26D) == "mov eax, dword ptr [rbx + 0x14]" and txt(0x0041D270) == "mov dword ptr [rsi + 0x338], eax" \
    and txt(0x0051BACA) == "call 0x41cb90" and txt(0x0051BAD7) == "call 0x41d220" \
    and txt(0x0041CFAC) == "and dword ptr [rbx + 0xc], 0xffffefff" and txt(0x0041CFBB) == "jmp 0x41cb90" \
    and any(i.mnemonic == "mov" and i.op_str.startswith("dword ptr [rcx + 0x338]") for i in body(0x0041CB90))
check("N5", ok, "+0x338 = definition +0x14 (0041D220); the -1 reset 0041CB90 runs before it and after the bit is cleared")
print("FAILS %d" % fails)
