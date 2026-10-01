"""SWE2-AUDIT-SPEC: which original paths feed the mapped (kind, index) of 0032F170 into a size lookup?
For each caller of the mapper, print the mapper call and every later call in the same body that reads the
mapper's out-slots (the [rsp+X] passed as r8/r9) or passes them on; plus the directory-table readers."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
MAPPER = 0x32F170
for site in (0x1DA2FD, 0x3DD562, 0x3DF49A, 0x3E9FE8):
    own = tk.owner(site)[0] if isinstance(tk.owner(site), tuple) else tk.owner(site)
    xs = tk.fdis(own)
    print("== mapper call %08X in %s (%d insns)" % (site, tk.fname(site), len(xs)))
    # the out-slot operands: lea r8/r9 just before the call
    slots = []
    idx = [i for i, x in enumerate(xs) if x.address == site][0]
    for x in xs[max(0, idx - 8):idx]:
        if x.mnemonic == "lea" and x.op_str.split(",")[0] in ("r8", "r9"):
            slots.append(x.op_str.split(",", 1)[1].strip())
    print("   out slots:", slots)
    for x in xs[idx:]:
        s = x.op_str
        if any(sl.replace("qword ptr ", "") in s for sl in [z.replace("ptr ", "") for z in slots]) or \
           any(sl.strip("[]") in s for sl in slots) or x.mnemonic == "call":
            print("   %08X %s %s" % (x.address, x.mnemonic, s))
