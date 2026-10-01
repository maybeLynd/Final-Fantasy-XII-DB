"""sd60_rederive2.py - SWE2-AUDIT-SPEC (2026-09-30): the three other address-takers of 02AEEB20 (do any write it?),
and which classes' vtables could be the execute's device (who else has a PrimitiveRenderer RTTI name)."""
import sys, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk

def around(a, before=6, after=6):
    o, how = tk.owner(a)
    xs = tk.dis(o, a + 0x40)
    i = next(k for k, x in enumerate(xs) if x.address == a)
    for x in xs[max(0, i - before):i + after + 1]:
        print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))

for a in (0x00376748, 0x0039CE25, 0x0039CF67, 0x0024E1EE):
    print("== context of %08X in %s" % (a, tk.fname(a)))
    around(a)
for f in (0x00216720,):
    print("== %08X head" % f)
    for x in tk.dis(f, f + 0x30)[:8]: print("  %08X %s %s" % (x.address, x.mnemonic, x.op_str))
# RTTI type-descriptor names containing PrimitiveRenderer
names = sorted(set(m.group(0).decode() for m in re.finditer(rb"\.\?AV[A-Za-z0-9_]*PrimitiveRenderer[A-Za-z0-9_]*@@", tk.d)))
print("== RTTI names with PrimitiveRenderer:", names)
# vtable slots holding 006CAF40
print("== DIR64 pointers to 006CAF40:", ["%08X" % p for p in [x[0] if isinstance(x, tuple) else x for x in tk.reloc_ptrs(0x006CAF40, 0x006CAF41)]])
