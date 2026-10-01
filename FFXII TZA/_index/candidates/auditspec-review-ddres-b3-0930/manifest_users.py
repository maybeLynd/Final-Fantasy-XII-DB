"""manifest_users.py - SWE2-AUDIT-SPEC: what the three rip lea's to 008FCE00 (and the image-base hit) do.
Prints the first 0x60 bytes of 008FCE00 as dwords, the image-base-relative hit, and the instructions around each
lea (r14 uses up to 40 instructions after)."""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
o = tk.off(0x008FCE00)
print("008FCE00 dwords:", " ".join("%X" % struct.unpack_from("<I", tk.d, o + 4 * i)[0] for i in range(24)))
dh, draw = tk.disp_refs(0x008FCE00 - tk.BASE, 0x008FD2D0 - tk.BASE)
for x, k, v in dh:
    print("imagebase %08X %s %s disp->%08X owner %s" % (x.address, x.mnemonic, x.op_str, v + tk.BASE, tk.owner(x.address)))
for site in (0x001D150F, 0x001D537D, 0x001D542A):
    e, how = tk.owner(site)
    ins = [x for x in tk.fdis(e) if x.address >= site - 0x20][:36]
    print("--- %08X in %08X" % (site, e))
    for x in ins:
        if x.address >= site - 0x20:
            s = "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
            if "r14" in x.op_str or x.mnemonic in ("call", "jmp") or x.address == site: print("  " + s)
