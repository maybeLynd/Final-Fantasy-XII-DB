"""SWE2-AUDIT-SEM RC-14 attack (own code): the writer shape both FABLE's structural census (table-walking functions)
and a displacement sweep (+0x11) miss is a byte store through a pointer that was itself advanced by 0x11, in a
function that does not walk the entry table. Sweep: every `add r64, 0x11` or `lea r64, [r + 0x11]` in .text (raw
byte search for the imm8/disp8 0x11, decoded in place from each aligned start), then the next 40 instructions for a
byte store `[r]`, `[r + k*0x14]` or `[r - ...]` through that register (value printed). Each hit is listed with the
producer's two known promoters and the insert/unlink stores as positive controls.
"""
import struct, re
import img
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
seen = set()
hits = []
for i in range(len(text)):
    if text[i] != 0x11:
        continue
    for back in range(2, 8):
        s = i - back
        x = next(img.md.disasm(text[s:s + 16], va0 + s), None)
        if not x or x.address + x.size != va0 + i + 1 or x.address in seen:
            continue
        ops = [o.strip() for o in x.op_str.split(",")]
        reg = None
        if x.mnemonic == "add" and len(ops) == 2 and ops[1] == "0x11" and re.fullmatch(r"r\w+", ops[0]):
            reg = ops[0]
        elif x.mnemonic == "lea" and re.fullmatch(r"\[\w+ \+ 0x11\]", ops[1] if len(ops) > 1 else ""):
            reg = ops[0]
        if not reg:
            continue
        seen.add(x.address)
        for y in list(img.md.disasm(img.rd(x.address + x.size, 300), x.address + x.size))[:40]:
            yo = [o.strip() for o in y.op_str.split(",")]
            if y.mnemonic in ("ret", "jmp") or (y.mnemonic == "call"):
                break
            if yo and re.fullmatch(r"byte ptr \[%s( [+-] 0x[0-9a-f]+)?\]" % reg, yo[0]) and y.mnemonic in ("mov", "or", "and", "inc", "dec", "add", "sub"):
                hits.append("%08X %s %s   (advance at %08X %s %s)" % (y.address, y.mnemonic, y.op_str, x.address, x.mnemonic, x.op_str))
            if yo and yo[0] == reg and y.mnemonic not in ("cmp", "test", "add") and not (y.mnemonic == "lea"):
                break
print("pointer advances by 0x11 image-wide:", len(seen))
print("byte stores through an advanced pointer:", len(hits))
for h in hits:
    print("  ", h)
for ctl in ("003DBB35", "003DB245", "003DBCAC"):
    print(("PASS" if any(h.startswith(ctl) for h in hits) else "FAIL"), "control", ctl)
