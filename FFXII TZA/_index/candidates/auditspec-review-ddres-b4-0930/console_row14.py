"""console_row14.py - SWE2-AUDIT-SPEC (review of 3198ee367, RC-29 incorporation): is the console page table 14 rows
(0x4D0 bytes, ending 008FD2D0) or does a reader index a 15th row?
S1: every store to a [reg + 0xA88] dword image-wide (the page index the three readers multiply by 0x16), with owner
    and the stored source; S2: 001D5260's page-index set before its table loop; S3: row 14's dwords (008FD2D0..)
    and whether each is a command id the row renderer accepts (id-1 <= 0x125).
Control: S1 must find 001D536D (mov dword [rbx+0xA88], 0xE) - the site DATA's record itself cites."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
hits, raw = tk.disp_refs(0xA88, 0xA89)
stores = [(x, k) for x, k, v in hits if tk.is_store(x, k) and tk.memsize(x, k) == 4]
print("S1 dword stores to [reg+0xA88]: %d (all disp-0xA88 accesses %d)" % (len(stores), len(hits)))
for x, k in stores:
    print("   %08X %s %s   owner %08X" % (x.address, x.mnemonic, x.op_str, tk.owner(x.address)[0] or 0))
print("control 001D536D found: %s" % any(x.address == 0x001D536D for x, k in stores))
row = [tk.u32(0x008FD2D0 + 4 * i) for i in range(0x16)]
print("S3 row 14 @008FD2D0:", " ".join("%X" % v for v in row))
nz = [v for v in row if v]
print("S3 non-zero=%d all within renderer bound (1..0x126): %s" % (len(nz), all(1 <= v <= 0x126 for v in nz)))
print("S3 dword after row 14 (008FD328) = %X (ASCII => table ends at 008FD328)" % tk.u32(0x008FD328))
