"""shadow_globals.py - SWE2-AUDIT-SPEC (review of 17a146c83, RC-8 row): the two globals said to hold the shadow
object, 01F82EA8 (row: "published only at") and 01F812C8 (ORACLE's correction, filled by 0015CC00).
Lists every rip-relative qword access to each, store/load, owner; plus image-base-relative forms."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
for g in (0x01F82EA8, 0x01F812C8):
    h, raw = tk.rip_refs(g, g + 8)
    dh, draw = tk.disp_refs(g - tk.BASE, g - tk.BASE + 8)
    st = [(x, k) for x, k, t in h if tk.is_store(x, k)]
    print("%08X: rip refs=%d stores=%d imagebase=%d" % (g, len(h), len(st), len(dh)))
    for x, k in st:
        print("   store %08X %s %s owner %08X" % (x.address, x.mnemonic, x.op_str, tk.owner(x.address)[0] or 0))
