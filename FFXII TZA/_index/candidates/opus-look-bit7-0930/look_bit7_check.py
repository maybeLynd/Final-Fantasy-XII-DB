"""look_bit7_check.py - who reads bit 7 of the look record's byte +0x1C (OPUS, 2026-09-30; SWE2-CONTRACT's proposed row P2,
_index/candidates/swe2contract-ddres-b10-0930). Static, kit retool.py.

L1  the writers: 003E29F0's kind-4 arm (op 0x12 through 005207C0) clears and sets bit 7 of [rec + 0x1C], with rec the
    0020E600 resolve of [obj + 8] (003E2A27-003E2A56); 0041DD40 sets it (0041DECF `or byte ptr [rax + 0x1c], 0x80`).
L2  image-wide, every test / bt of a memory operand whose width covers +0x1C and selects its bit 7 is listed: the only one
    is 002698AC in 00269860, whose record is an actor (manager slot from byte +0x15, 0x288-byte slots at 02098E10).
L3  image-wide, every load of byte [reg + 0x1C] followed within three instructions by a bit-7 operation (shr/sar 7,
    and/test 0x80, js/jns) is listed: none.
L4  right after each of the 4,373 0020E600 call sites, the byte accesses to [result + 0x1C] within 16 instructions are the
    writers above and the bit-0..2 setters 0051E620 / 0051E670 / 0051E9C0 / 0051EA10 and the bit-0 test 003E2C99 -
    no bit-7 read (positive control: the census finds 003E29F0's own write).
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, sys

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


ok = txt(0x003E2A27) == "mov ecx, dword ptr [rbx + 8]" and txt(0x003E2A2F) == "call 0x20e600" \
    and txt(0x003E2A4E) == "and byte ptr [rax + 0x1c], 0x7f" and txt(0x003E2A56) == "or byte ptr [rax + 0x1c], bpl" \
    and txt(0x0041DECF) == "or byte ptr [rax + 0x1c], 0x80" and txt(0x0041DECA) == "call 0x20e600"
check("L1", ok, "writers of bit 7: 003E29F0 kind 4 (op 0x12) and 0041DD40")

tests, loads = [], []
for f, n in SZ.items():
    try:
        ins = list(R.md.disasm(R.at(f, n), f))
    except Exception:
        continue
    for k, i in enumerate(ins):
        if len(i.operands) == 2 and i.mnemonic in ("test", "bt"):
            a, b = i.operands
            if a.type == 3 and b.type == 2 and a.mem.base and i.reg_name(a.mem.base) not in ("rip", "rsp"):
                d, w = a.mem.disp, a.size
                if d <= 0x1C < d + w:
                    bit = (0x1C - d) * 8 + 7
                    imm = b.imm & ((1 << (8 * w)) - 1)
                    if (i.mnemonic == "bt" and imm == bit) or (i.mnemonic == "test" and (imm >> bit) & 1):
                        tests.append((f, i.address))
        if i.mnemonic in ("movzx", "movsx", "mov") and re.search(r"^\w+, byte ptr \[r\w+ \+ 0x1c\]$", i.op_str):
            for j in ins[k + 1:k + 4]:
                if (j.mnemonic in ("shr", "sar") and j.op_str.endswith(", 7")) or (j.mnemonic in ("and", "test") and j.op_str.endswith("0x80")) \
                        or j.mnemonic in ("js", "jns"):
                    loads.append((f, i.address))
                    break
ok = tests == [(0x00269860, 0x002698AC)] and txt(0x0026988E) == "movzx eax, byte ptr [rcx + 0x15]" \
    and txt(0x00269892) == "imul rcx, rax, 0x288" and txt(0x002698A5) == "add rcx, rax"
check("L2", ok, "bit-7 tests covering +0x1C: %s (an actor record)" % ["%08X" % a for _, a in tests])
check("L3", not loads, "byte loads of +0x1C followed by a bit-7 operation: %s" % ["%08X" % a for _, a in loads])

after = []
for f, site in sorted(c["calls"].get(0x0020E600, ())):
    ins = list(R.md.disasm(R.at(site, 0x60), site, 16))
    regs = {"rax"}
    for j in ins[1:]:
        if j.mnemonic == "mov" and re.match(r"^(r\w+), rax$", j.op_str):
            regs.add(j.op_str.split(",")[0])
        m = re.search(r"byte ptr \[(r\w+) \+ 0x1c\]", j.op_str)
        if m and m.group(1) in regs:
            after.append((f, j.address, j.mnemonic, j.op_str))
            break
        if j.mnemonic in ("call", "ret", "jmp"):
            break
seen = {(f, a) for f, a, _, _ in after}
bit7_reads = [x for x in after if x[2] in ("test", "bt") and x[3].endswith("0x80")]
ok = len(c["calls"].get(0x0020E600, ())) == 4373 and (0x003E29F0, 0x003E2A4E) in seen and (0x003E2C00, 0x003E2C99) in seen and not bit7_reads
check("L4", ok, "post-resolve byte +0x1C accesses: %s; bit-7 reads among them: %d"
      % (["%08X %s %s" % (a, m, o) for _, a, m, o in after], len(bit7_reads)))
print("FAILS %d" % fails)
