"""SWE2-AUDIT-SEM: image-wide sweep for every store (any width, any base register except rsp/rip) whose destination
[base + disp] covers byte offset D, i.e. disp <= D < disp + width. Raw: every 4-byte window in .text equal to a
candidate disp32 in [D-31, D] is decoded from each back-aligned start (1..12 bytes) whose instruction ends 0..4 bytes
after the window; kept when the decoded memory destination has that disp. disp8 forms are included when D-31..D fits
in 0..0x7F. usage: cover_sweep.py <D hex>
Control: the producer-named writers must appear (A: 002832C7, 00283400 for 0xB2D)."""
import sys, struct, re
import img
D = int(sys.argv[1], 16)
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16, "ymmword": 32}
MEM = re.compile(r"^(byte|word|dword|qword|xmmword|ymmword) ptr \[(\w+)(?: \+ \w+\*?\d?)?(?: \+ (0x[0-9a-f]+|\d+))\]$")
NOSTORE = ("cmp", "test", "bt", "prefetch")
found = {}
cands = set(range(max(0, D - 31), D + 1))
def consider(i, dlen):
    for back in range(1, 13):
        s = i - back
        if s < 0:
            continue
        for x in img.md.disasm(text[s:s + 20], va0 + s, 1):
            end = x.address + x.size
            if not (i + dlen <= end - va0 <= i + dlen + 4):
                continue
            ops = [o.strip() for o in x.op_str.split(",")]
            if len(ops) < 2 and x.mnemonic not in ("inc", "dec", "not", "neg"):
                continue
            m = MEM.match(ops[0])
            if not m or m.group(2) in ("rsp", "rip", "esp") or x.mnemonic.startswith(NOSTORE):
                continue
            disp = int(m.group(3), 0)
            w = W[m.group(1)]
            if disp in cands and disp <= D < disp + w:
                found[x.address] = "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
for i in range(len(text) - 4):
    v = struct.unpack_from("<I", text, i)[0]
    if v in cands:
        consider(i, 4)
    if D <= 0x7F and text[i] in cands:
        consider(i, 1)
for a in sorted(found):
    print(found[a])
print("stores covering +%#x: %d" % (D, len(found)))
