"""rc35_block_reader.py - RC-35: the reader of the 8-byte block between arrays C and D of a menumap_location.bin record.
OPUS, 2026-09-30. Static, the certified image. Reads only. Every fact is an exact instruction.

  B1  003BE680(n, &w2, &w4) takes record n of [[02B457E0] + 0xE0] (003BE68A, 003BE6A1-003BE6A7), forms
      C = rec + 4 + 24*(countA + countB) (003BE6AE-003BE6BD) and block = C + 20*countC (003BE6C0, 003BE6CA, 003BE6D0),
      then returns word [block+0] and stores word [block+2] -> *rdx, word [block+4] -> *r8 (003BE6DE-003BE6F3);
      word [block+6] is not read.
  B2  its only callers: 002B7B80 (002B7FFA) and 002BAF80 (002BB45E, 002BBA8D), each passing the current record
      (word [obj+0x138]) and two stack outs; each divides 0xC80 by the value it picks (002B8052/002B8059,
      002BB4BA, 002BBAEA).
  B3  the census of every function that references the map object 02B457E0 finds only four x5 multiplies
      (lea r, [r + r*4]): 003BD1B0 (a 40-byte stride of its own array, not the table), 003BE680, and the two
      C/D walkers 003BFF20 / 003C1070 that step over the block (+8).
Control: the two walkers add 8 past the C end before reading D (003BFF95-003BFFAA region, section 10.2), and 003BE680
does not - it reads at the C end itself.
"""
import os, sys, collections
import capstone
from capstone import x86 as X

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
fails = 0


def ins(a):
    return next(md.disasm(R.at(a, 16), a, 1))


def expect(tag, a, text):
    global fails
    i = ins(a)
    got = ("%s %s" % (i.mnemonic, i.op_str)).strip()
    ok = got == text
    fails += not ok
    print("%s  %s %08X %s%s" % ("PASS" if ok else "FAIL", tag, a, got, "" if ok else "   (expected: %s)" % text))


for a, t in ((0x003BE68A, "mov r9, qword ptr [rax + 0xe0]"), (0x003BE6A1, "movzx ecx, word ptr [r9 + rax*2 + 0xa]"),
             (0x003BE6AE, "movzx eax, byte ptr [rdx]"), (0x003BE6B1, "movzx ecx, byte ptr [rcx + 1]"),
             (0x003BE6B7, "lea eax, [rcx + rcx*2]"), (0x003BE6BA, "lea ecx, [rdx + 4]"), (0x003BE6BD, "lea ecx, [rcx + rax*8]"),
             (0x003BE6C0, "movzx eax, byte ptr [rdx + 2]"), (0x003BE6CA, "lea rcx, [rax + rax*4]"), (0x003BE6D0, "lea rdx, [rdx + rcx*4]"),
             (0x003BE6DE, "movzx ecx, word ptr [rdx + 2]"), (0x003BE6EB, "movzx ecx, word ptr [rdx + 4]"), (0x003BE6F3, "movzx eax, word ptr [rdx]")):
    expect("B1", a, t)
body = list(md.disasm(R.at(0x003BE680, R.ext[0x003BE680]), 0x003BE680))
reads6 = [i for i in body if any(o.type == X.X86_OP_MEM and o.mem.disp == 6 for o in i.operands)]
ok = not reads6
fails += not ok
print("%s  B1 no read of block +6 in 003BE680" % ("PASS" if ok else "FAIL"))
# B2 callers
sites = []
for f, n in R.ext.items():
    d = R.at(f, n)
    if not d:
        continue
    for i in R.md.disasm(d, f):
        if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == X.X86_OP_IMM and i.operands[0].imm == 0x003BE680:
            sites.append((f, i.address))
ok = sorted(sites) == [(0x002B7B80, 0x002B7FFA), (0x002BAF80, 0x002BB45E), (0x002BAF80, 0x002BBA8D)]
fails += not ok
print("%s  B2 callers %s" % ("PASS" if ok else "FAIL", " ".join("%08X@%08X" % s for s in sorted(sites))))
for a in (0x002B8052, 0x002BB4BA, 0x002BBAEA):
    expect("B2", a, "mov eax, 0xc80")
expect("B2", 0x002B8059, "div ecx")
# B3 census of x5 multiplies in functions referencing the map object
G = 0x02B457E0
hits = collections.defaultdict(list)
for f, n in R.ext.items():
    d = R.at(f, n)
    if not d:
        continue
    lst = list(R.md.disasm(d, f))
    if not any(o.type == X.X86_OP_MEM and o.mem.base == X.X86_REG_RIP and i.address + i.size + o.mem.disp == G for i in lst for o in i.operands):
        continue
    for i in lst:
        for o in i.operands:
            if o.type == X.X86_OP_MEM and o.mem.index != 0 and o.mem.scale == 4 and o.mem.base == o.mem.index:
                hits[f].append(i.address)
ok = sorted(hits) == [0x003BD1B0, 0x003BE680, 0x003BFF20, 0x003C1070]
fails += not ok
print("%s  B3 x5 multiplies in map-object functions: %s" % ("PASS" if ok else "FAIL", " ".join("%08X" % f for f in sorted(hits))))
expect("B3", 0x003BD2B1, "lea rsi, [r15 + rcx*8]")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
