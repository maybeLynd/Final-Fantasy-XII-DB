"""SWE2-AUDIT-SPEC: image-base-relative accesses to the REC table 022C1740 (disp 022C1740 - 00120000 = 021A1740 with an
image-base register), which ov58d_flow.py does not learn as an escape global (it skips G00120000 at line 317).
Also the same form for the state-pointer cell 02EBF190 (disp 02D9F190). 2026-09-30."""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
for name, lo, hi in (("REC table 022C1740[0..9]", 0x22C1740 - 0x120000, 0x22C1740 - 0x120000 + 0x48),
                     ("state cell 02EBF190", 0x2EBF190 - 0x120000, 0x2EBF190 - 0x120000 + 8)):
    hits, raw = tk.disp_refs(lo, hi)
    print("%s: verified image-base-form accesses %d, raw-only %d" % (name, len(hits), len(raw)))
    for x, k, v in hits:
        print("  %08X %-5s %s | %s | %s" % (x.address, "STORE" if tk.is_store(x, k) else "read", x.mnemonic, x.op_str, tk.fname(x.address)))
