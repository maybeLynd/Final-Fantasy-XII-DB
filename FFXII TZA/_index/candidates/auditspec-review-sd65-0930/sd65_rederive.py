"""sd65_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-65 (2026-09-30). Read-only on the image.
R1  L1 by raw sweep: every E8/E9/0F8x branch in .text to 00632B30, 006393A0 and 0059AC00, plus address-taken forms
    (rip-relative lea/mov and DIR64 relocations), independent of the function list.
R2  "entry +8 = file class record": the 0x30-byte entry builder in 0059B430 (called from 0059E070 before 0059AC00)."""
import sys, struct, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk

blob = tk.d[tk.TRO:tk.TRO + min(tk.TRS, tk.TVS)]
T = (0x00632B30, 0x006393A0, 0x0059AC00)
br = collections.defaultdict(list)
for i in range(len(blob) - 6):
    b = blob[i]
    if b in (0xE8, 0xE9):
        t = tk.TVA + i + 5 + struct.unpack_from("<i", blob, i + 1)[0]
        if t in T: br[t].append(("E8" if b == 0xE8 else "E9", tk.TVA + i))
    elif b == 0x0F and 0x80 <= blob[i + 1] <= 0x8F:
        t = tk.TVA + i + 6 + struct.unpack_from("<i", blob, i + 2)[0]
        if t in T: br[t].append(("jcc", tk.TVA + i))
for t in T:
    rr, raw = tk.rip_refs(t, t + 1)
    rel = tk.reloc_ptrs(t, t + 1)
    print("R1 %08X raw branches: %s; rip address-taken: %d (raw-only %d); DIR64 pointers: %d" % (
        t, ["%s %08X in %s" % (k, a, tk.fname(a)) for k, a in br[t]], len(rr), len(raw), len(rel)))
print("R2 the entry builder, 0059B430 at 0059B7BE..0059B7E6 (rsi walks the namespace's 36-byte class records):")
for x in tk.dis(0x0059B5D7, 0x0059B62E):
    if x.address in (0x0059B5D7, 0x0059B5E7, 0x0059B5EB, 0x0059B5F3, 0x0059B604): print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
for x in tk.dis(0x0059B7B9, 0x0059B7EA): print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
