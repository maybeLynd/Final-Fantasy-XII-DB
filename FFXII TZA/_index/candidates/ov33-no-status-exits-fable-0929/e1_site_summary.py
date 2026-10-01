"""e1_site_summary.py - compact per-site view for the 0032E620/0032E780 producer sites (reading aid, not a verdict).
For each site: the size-getter calls (0032E400, 0046DE70, 002DF960) in the owner before the site, the 5 instructions
after each, and the 10 instructions before the site. Control: site 002492F3 shows its 0032E400 at 00249296.
"""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk, json
raw = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
SIZE = {0x32E400, 0x46DE70, 0x2DF960, 0x24AB90}
sites = [int(a, 16) for a in raw["32E620"]] + [int(a, 16) for a in raw["32E780"]]
fails = 0; ctl = False
for s in sorted(sites):
    o, how = tk.owner(s)
    xs = tk.dis(o, s + 5)
    idx = {x.address: i for i, x in enumerate(xs)}
    if s not in idx:
        print("SITE %08X not on boundary" % s); fails += 1; continue
    print("==== %08X in %s" % (s, tk.fname(s)))
    for i, x in enumerate(xs):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x") and int(x.op_str, 16) in SIZE:
            print("  size-call %08X %s %s" % (x.address, x.mnemonic, x.op_str))
            if s == 0x2492F3 and x.address == 0x249296: ctl = True
            for y in xs[i + 1:i + 6]: print("      %08X %s %s" % (y.address, y.mnemonic, y.op_str))
    print("  -- before site")
    for y in xs[max(0, idx[s] - 10):idx[s] + 1]: print("      %08X %s %s" % (y.address, y.mnemonic, y.op_str))
print("control 00249296 size-call seen for 002492F3: %s" % ctl)
if not ctl: fails += 1
print("sites: %d" % len(sites))
print("FAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
