"""SWE2-AUDIT-SEM own rip-relative reference sweep.
usage: ripref.py <lo-hex> <hi-hex>   finds every .text instruction whose rip-relative operand lands in [lo,hi).
Candidate: every 4-byte window read as disp32 with 0/1/2/4 trailing immediate bytes; each candidate is
confirmed by disassembling backwards-aligned starts (up to 15 bytes before) and requiring an instruction
that covers the window and whose decoded operand text names the target."""
import sys, struct, re
import img
lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
hits = set()
n = len(text)
for i in range(n - 4):
    d = struct.unpack_from("<i", text, i)[0]
    for tail in (0, 1, 2, 4):
        tgt = va0 + i + 4 + tail + d
        if lo <= tgt < hi:
            hits.add((i, tail, tgt))
found = {}
for i, tail, tgt in sorted(hits):
    for back in range(1, 12):
        s = i - back
        if s < 0:
            continue
        ins = next(img.md.disasm(text[s:s + 16], va0 + s), None)
        if ins and ins.size == back + 4 + tail and "rip" in ins.op_str:
            m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", ins.op_str)
            if m:
                dd = int(m.group(2), 0) * (1 if m.group(1) == "+" else -1)
                if ins.address + ins.size + dd == tgt:
                    found[ins.address] = "%08X  %s %s    ; -> %08X" % (ins.address, ins.mnemonic, ins.op_str, tgt)
                    break
for a in sorted(found):
    print(found[a])
print("refs:", len(found))
