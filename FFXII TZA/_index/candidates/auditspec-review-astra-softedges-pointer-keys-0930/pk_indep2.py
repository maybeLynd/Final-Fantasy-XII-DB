"""SWE2-AUDIT-SPEC pointer-key review, part 2: registration call continuation, 59EC40 exit arms, 59BED0 rbx origin,
raw callers of 59EC40 / 632A10 (rawcalls.json + raw E8/E9 sweep)."""
import sys, os, json, struct
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, r"..\..\..\..\Tools\work\FABLE\takebacks"))
import tk
def rng(e, lo, hi, tag):
    print("== " + tag)
    for x in tk.fdis(e):
        if lo <= x.address <= hi:
            print("  %08X %-6s %s" % (x.address, x.mnemonic, x.op_str))
rng(0x005E45B0, 0x005E48C6, 0x005E4916, "5E48C6 continuation")
rng(0x005E45B0, 0x005E4951, 0x005E49A2, "5E4951 continuation")
rng(0x005EEB20, 0x005EED9A, 0x005EEDE0, "5EED9A continuation")
rng(0x0059EC40, 0x0059ED0F, 0x0059ED90, "59EC40 recursion arm and exits")
rng(0x0059BED0, 0x0059BED0, 0x0059BF40, "59BED0 entry")
rng(0x0059BED0, 0x0059C040, 0x0059C0B5, "59BED0 loop before 59C0DB")
RAW = json.load(open(os.path.join(HERE, r"..\..\..\..\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json")))
for t in (0x0059EC40, 0x00632A10, 0x0059BED0):
    k = "%X" % t
    print("rawcalls %08X:" % t, RAW.get(k, RAW.get("%08X" % t)))
# independent raw E8/E9 sweep over .text for the same targets
TVA, TVS, TRS, TRO = tk.TVA, tk.TVS, tk.TRS, tk.TRO
text = tk.d[TRO:TRO + TRS]
for t in (0x0059EC40, 0x00632A10, 0x0059BED0):
    hits = []
    for op in (b"\xe8", b"\xe9"):
        i = text.find(op)
        while i >= 0:
            if i + 5 <= len(text):
                rel = struct.unpack_from("<i", text, i + 1)[0]
                if TVA + i + 5 + rel == t:
                    hits.append("%08X%s" % (TVA + i, "c" if op == b"\xe8" else "j"))
            i = text.find(op, i + 1)
    print("raw E8/E9 -> %08X: %d %s" % (t, len(hits), " ".join(hits[:40])))
