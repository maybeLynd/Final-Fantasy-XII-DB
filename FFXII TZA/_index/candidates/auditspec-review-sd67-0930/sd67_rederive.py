"""SWE2-AUDIT-SPEC independent re-derivation for SD-67 (2026-09-30). Read-only on the image.
  R1 every reference to the name string "m_streamBindings" over ALL .text (rip sweep) and stored pointers to it
  R2 00632A10's prologue (frame size) and the stores of each stack argument, to map caller [rsp+0x20..0x38] onto fields
  R3 005EFE60: the value of r15 at 005EFEF9 (so r9d = r15+0x10), the vtable store and its target, and 00632D80's use
     of r9 and its 5th argument (which field receives size / alignment)
  R4 RTTI of vtables 00D4DD98 and 00D58100 by my own complete-object-locator walk
"""
import sys
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk

def L(lo, hi, flt=None):
    for x in tk.dis(lo, hi):
        if flt is None or flt(x): print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))

hits, raw = tk.rip_refs(0x00D4A1C0, 0x00D4A1C1)
print("R1 rip refs to 00D4A1C0: %s raw-only %d; stored pointers %d" % (
    ["%08X %s" % (h[0].address, tk.fname(h[0].address)) for h in hits], len(raw), len(tk.reloc_ptrs(0x00D4A1C0, 0x00D4A1C1))))
o = tk.off(0x00D4A1C0); print("   string %r" % tk.d[o:o + 20].split(b"\0")[0])
print("R1 call setup 005E6818..005E6860 (on the owner's instruction boundaries):")
for s in sorted(b for b in tk.boundaries(0x005E6860) if 0x005E6818 <= b <= 0x005E6860):
    x = tk.dis(s, s + 15)[0]; print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("R2 00632A10 prologue and stack-argument loads:")
L(0x00632A10, 0x00632A70, lambda x: x.mnemonic in ("push", "sub") or "rsp +" in x.op_str or "rdi +" in x.op_str)
print("R3 005EFE60 r15 writes and the 00632D80 call setup:")
fx = tk.fdis(0x005EFE60)
for x in fx:
    if x.op_str.startswith(("r15", "r15d")) or 0x005EFEE0 <= x.address <= 0x005EFF20:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("R3 00632D80 prologue, r9 and stack-argument uses:")
for x in tk.fdis(0x00632D80)[:60]:
    if x.mnemonic in ("push", "sub") or "r9" in x.op_str or "rsp + 0x" in x.op_str:
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
for vt in (0x00D4DD98, 0x00D58100):
    col = tk.u64(vt - 8); td = tk.BASE + tk.u32(col + 0x0C); o = tk.off(td + 0x10)
    print("R4 %08X COL sig %d name %r" % (vt, tk.u32(col), tk.d[o:o + 130].split(b"\0")[0]))
import re
occ = [m.start() for m in re.finditer(rb"m_streamBindings\x00", tk.d)]
print("R5 file copies of the NUL-terminated name: %d %s; substring streamBindings: %d" % (len(occ), [hex(o) for o in occ], len(re.findall(rb"streamBindings", tk.d))))
