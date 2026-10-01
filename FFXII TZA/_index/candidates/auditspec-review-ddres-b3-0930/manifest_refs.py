"""manifest_refs.py - SWE2-AUDIT-SPEC check of RC-29's premise (review of 17a146c83): "no rip-relative or
pointer-table reference reaches" the menu resource manifest .rdata [008FCE00, 008FD2D0).
Every addressing form tk.py can census: rip-relative, image-base-relative disp32 (disp = rva), absolute imm/disp32,
DIR64 stored pointers, raw unaligned qwords. Also widened 0x100 below the block (a base pointer to a header just
before the lists would reach the lists by offset). Control: the same census over 02064ACC finds writer 0022A1A7."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
for lo, hi, tag in ((0x008FCE00, 0x008FD2D0, "block"), (0x008FCD00, 0x008FCE00, "0x100 below")):
    rh, rraw = tk.rip_refs(lo, hi)
    dh, draw = tk.disp_refs(lo - tk.BASE, hi - tk.BASE)
    ah, araw = tk.abs_refs(lo, hi)
    rp = tk.reloc_ptrs(lo, hi)
    rq = tk.raw_q(lo, hi)
    print("%s [%08X,%08X): rip=%d (raw-only %d) imagebase=%d abs=%d dir64=%d rawq=%d" % (
        tag, lo, hi, len(rh), len(rraw), len(dh), len(ah), len(rp), len(rq)))
    for x, k, t in rh[:8]:
        print("   rip %08X %s %s -> %08X owner %s" % (x.address, x.mnemonic, x.op_str, t, tk.owner(x.address)[0] and "%08X" % tk.owner(x.address)[0]))
    for a, q in rp[:8]:
        print("   dir64 at %08X (%s) -> %08X" % (a, tk.sec_of(a), q))
ch, _ = tk.rip_refs(0x02064ACC, 0x02064AD0)
print("control 02064ACC writer 0022A1A7 present: %s" % any(x.address == 0x0022A1A7 for x, k, t in ch))
