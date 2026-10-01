"""sd107o_diff180.py - which stores does the independent raw scan (sd107o_stores.json, 184) find that the package's
census (180, over regval's function bodies) does not, and vice versa? Uses the kit only to ENUMERATE the package's
input set (V.body over V.SZ, the same loop as the package's C1), not to classify anything."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import regval as V  # noqa: E402

W = {"byte": 1, "word": 2, "dword": 4, "qword": 8}
pkg = {}
for f in V.SZ:
    for i in V.body(f)[0]:
        if i.mnemonic != "mov":
            continue
        m = re.match(r"(byte|word|dword|qword) ptr \[(\w+)(?: \+ (0x[0-9a-f]+))?\], (\w+)$", i.op_str)
        if not m or m.group(2) in ("rsp", "rbp", "rip") or not V.canon(m.group(4)):
            continue
        w, d = W[m.group(1)], int(m.group(3), 16) if m.group(3) else 0
        if d <= 0xA3 < d + w:
            pkg[i.address] = (f, i.op_str)
mine = {int(x[1], 16): x for x in json.load(open(os.path.join(HERE, "sd107o_stores.json")))}
print("package census %d, raw scan %d, common %d" % (len(pkg), len(mine), len(set(pkg) & set(mine))))
for a in sorted(set(mine) - set(pkg)):
    x = mine[a]
    inbody = [f for f in V.SZ if f <= a < f + V.SZ[f]]
    print("  raw-scan only %08X  pdata-root %s  %dB [%s+%#x], %s  in a kit function: %s" % (
        a, x[0], x[2], x[3], x[4], x[5], " ".join("%08X" % f for f in inbody) or "none"))
for a in sorted(set(pkg) - set(mine)):
    print("  package only  %08X  in %08X  %s" % (a, pkg[a][0], pkg[a][1]))
