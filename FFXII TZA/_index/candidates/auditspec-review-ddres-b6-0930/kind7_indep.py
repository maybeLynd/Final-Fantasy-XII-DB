"""kind7_indep.py - own-tool re-derivation of K1-K3 (kind 7 ids 111 / 127, control 0xBF) without kind7.py.

002DF9A0 installs the per-kind path arrays into the directory 0215F000[kind]. Every store into 0215F038 (kind 7) in its
body is found, with the array address its source register was loaded with (lea reg, [rip+X]); for each such array
the qword at array + 8*id is read (a relocated pointer is required) and the C string printed.
"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402

f = I.func_of(0x002DF9A0)
seq = I.body(f)
print("002DF9A0 .pdata root %08X, %d instructions" % (f, len(seq)))
last, arrays = {}, []
for i in seq:
    rip = [i.address + i.size + op.mem.disp for _, op in I.mem_ops(i) if op.mem.base == I.X86_REG_RIP]
    if i.mnemonic == "lea" and rip:
        last[i.op_str.split(",")[0]] = rip[0]
    elif i.mnemonic == "mov" and rip and i.op_str.startswith("qword ptr [rip") and rip[0] == 0x0215F038:
        reg = i.op_str.rsplit(", ", 1)[1]
        arrays.append((i.address, reg, last.get(reg)))
print("stores to 0215F038 (kind 7):", [("%08X" % a, r, "%08X" % v if v else None) for a, r, v in arrays])
rel = I.relocs()
for a, r, arr in arrays:
    if not arr:
        continue
    for kid in (0x6F, 0x7F, 0xBF):
        cell = arr + 8 * kid
        q = I.rd(cell, 8)
        p = struct.unpack("<Q", q)[0] if q else 0
        s = (I.rd(p, 128) or b"").split(b"\0")[0].decode("latin-1") if p else None
        print("  store %08X array %08X id 0x%02X cell %08X %s -> %s" % (a, arr, kid, cell, "reloc" if cell in rel else "NOT-reloc", s))
