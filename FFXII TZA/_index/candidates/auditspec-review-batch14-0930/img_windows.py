"""img_windows.py - SWE2-AUDIT-SPEC (2026-09-30): print the instruction windows the batch-14 spot checks rest on,
decoded with the takebacks helper tk.py (not the records' img.py). Usage: python img_windows.py [label ...]"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
W = {
    "rc12_wait":   (0x0025E150, 0x0025E1A0),   # 0025DF00's footer read at 0025E186
    "rc12_mj":     (0x0025B6C0, 0x0025B740),   # 0025B600, claimed k=12 mapjump, filed on channel 6 at 0025B72B
    "rc12_reqchg": (0x0025AF60, 0x0025AFB0),   # REQCHG writer: word [rax+rbx*2+0xC8]
    "rc11_sel":    (0x00504385, 0x005043B0),   # cmp byte [ctx],10 / jb
    "rc11_retry":  (0x0036BFE0, 0x0036C008),   # bt at 0036BFF8, self-jump at 0036C000
    "rc11_alloc":  (0x0036BCB8, 0x0036BCE8),   # 0036BCC5 mark byte, 0036BCD8 bit test
    "rc17_loop":   (0x00360880, 0x00360900),   # K4
    "rc19_start":  (0x002EB260, 0x002EB2D0),   # blend compare
    "rc19_neg":    (0x004272E0, 0x00427320),   # the <0 arm
    "rc18_read":   (0x0031B810, 0x0031B850),   # map-1 slot read at 0031B841
}
want = sys.argv[1:] or list(W)
for k in want:
    lo, hi = W[k]
    print("== %s %08X..%08X in %s" % (k, lo, hi, tk.fname(lo)))
    for x in tk.dis(lo, hi):
        print("  %08X  %-8s %s" % (x.address, x.mnemonic, x.op_str))
