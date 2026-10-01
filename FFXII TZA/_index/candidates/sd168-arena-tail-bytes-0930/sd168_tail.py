"""sd168_tail.py - SD-168: what the extra `count` bytes of each arena's boot allocation (size + count) serve (OPUS,
2026-09-30). Static, the certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py.
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
    return "%s %s" % (i.mnemonic, i.op_str)


# T1 - the boot routine 0022A0B0 allocates each backing through 0036D240 (-> 0085E730) with a size that is the arena's
#      size plus exactly its handle count: 0x1DC0000 + 0x10 for arena 2, 0xD20000 + 0x100 for arena 3, 0x100000 + 0x10
#      for arena 4, and so on; the initializer 00369D30 then gets (arena, backing, size, count) separately
ins = list(R.md.disasm(R.at(0x0022A0B0, SZ[0x0022A0B0]), 0x0022A0B0))
allocs = [int(i.op_str.split(", ")[1], 16) for k, i in enumerate(ins[:-3]) if i.mnemonic == "mov" and i.op_str.startswith("ecx, 0x")
          and any(j.mnemonic == "call" and j.op_str == "0x36d240" for j in ins[k + 1:k + 4])
          and not any(j.op_str.startswith("ecx,") for j in ins[k + 1:k + 1 + next(n for n, j in enumerate(ins[k + 1:k + 4]) if j.mnemonic == "call")])]
inits = []
for f, s in sorted(c["calls"].get(0x00369D30, ())):
    if f != 0x0022A0B0:
        continue
    pre = [i for i in ins if i.address < s][-8:]
    r8 = next((int(i.op_str.split(", ")[1], 16) for i in reversed(pre) if i.op_str.startswith("r8d, 0x")), None)
    r9 = next((int(i.op_str.split(", ")[1], 0) for i in reversed(pre) if re.match(r"r9d, (0x[0-9a-f]+|\d+)$", i.op_str)), None)
    inits.append((r8, r9))
pairs = [(s, n) for s, n in inits if s is not None and n is not None]
print("      initializer (size, count): %s" % ", ".join("(%#x, %#x)" % p for p in pairs))
print("      backing allocations      : %s" % ", ".join("%#x" % a for a in allocs[:12]))
matched = [p for p in pairs if p[0] + p[1] in allocs]
check("T1", txt(0x0036D249) == "jmp 0x85e730" and len(pairs) >= 8 and len(matched) == len(pairs),
      "every boot arena's backing is allocated as size + count (%d of %d matched)" % (len(matched), len(pairs)))
# T2 - the initializer carves everything from inside `size`: the header, the bitmap (+0x20), the table (+0x28), the
#      16-byte handle slots (+0x30/+0x40 .. +0x38 = start + count * 16) and the data region (+0x10), whose usable length
#      is size - (data start - base), rounded down to 64 (+0x5C) - so no arena structure reaches past base + size
check("T2", txt(0x00369EB7) == "shl rax, 4" and txt(0x00369EBE) == "mov qword ptr [rbx + 0x38], r10"
      and txt(0x00369F5D) == "mov eax, dword ptr [rbx + 8]" and txt(0x00369F65) == "sub eax, r10d" and txt(0x00369F6C) == "add eax, r13d"
      and txt(0x00369F85) == "and eax, 0xffffffc0" and txt(0x00369F88) == "mov dword ptr [rbx + 0x5c], eax"
      and txt(0x00369D3E) == "mov r13d, r8d" and txt(0x00369D41) == "movsxd rbp, r9d",
      "handle table = count x 16 B inside size; data length = size - metadata, rounded down to 64")
print("FAILS %d" % fails)
