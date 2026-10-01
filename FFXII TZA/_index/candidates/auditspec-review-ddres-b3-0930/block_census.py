"""block_census.py - SWE2-AUDIT-SPEC independent recount of the console-tunes render-settings block
[02CB7FD0, 02CB843C) (review of 17a146c83). Uses tk.py (FABLE takebacks), not the author's rip_refs.py.
Counts functions (listed owner or .pdata range) with a rip-relative reference into the block, split lea-only vs
accessing; then checks the forms rip_refs cannot see: image-base-relative disp32 (disp = target - 0x120000),
absolute imm/disp32, DIR64-relocated stored pointers. Control: 02064ACC must show the known writer 0022A1A7."""
import sys, collections
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
LO, HI = 0x02CB7FD0, 0x02CB843C
hits, raw = tk.rip_refs(LO, HI)
fn = collections.defaultdict(set)
unowned = []
for x, k, t in hits:
    oe, how = tk.owner(x.address)
    if oe is None: unowned.append(x.address); continue
    fn[oe].add("lea" if x.mnemonic == "lea" else "acc")
lea = sorted(f for f, s in fn.items() if s == {"lea"})
print("rip insns=%d raw-only=%d unowned=%s" % (len(hits), len(raw), ["%08X" % a for a in unowned]))
print("referencing functions=%d accessing=%d lea-only=%s" % (len(fn), len(fn) - len(lea), ["%08X" % f for f in lea]))
print("25 in (referencing, accessing): %s" % (25 in (len(fn), len(fn) - len(lea))))
dh, draw = tk.disp_refs(LO - tk.BASE, HI - tk.BASE)
print("image-base-relative (disp=rva) verified=%d raw-only=%d %s" % (len(dh), len(draw), ["%08X" % x.address for x, k, v in dh][:10]))
ah, araw = tk.abs_refs(LO, HI)
print("absolute imm/disp32 verified=%d" % len(ah))
rp = tk.reloc_ptrs(LO, HI)
print("DIR64 stored pointers into block=%d %s" % (len(rp), ["%08X" % a for a, q in rp][:10]))
ch, _ = tk.rip_refs(0x02064ACC, 0x02064AD0)
print("control 02064ACC writer 0022A1A7 present: %s" % any(x.address == 0x0022A1A7 for x, k, t in ch))
