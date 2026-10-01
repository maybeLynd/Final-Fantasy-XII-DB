"""typed_rederive.py - SWE2-AUDIT-SPEC re-derivation of the typed-list page's E / S / R / C / L items with own tools.

  E  the emitter 002D9380: r8 (the drawer's node +0x18) kept in rsi; every [rsi+disp] read in the body, listed
  S  the sub-image record decode in 0029F130 (type 7) and 0029F4C0 (types 2/9): the instructions at the pinned sites
  R  callers of 002A0060 and 0024A610 (E8/E9/jcc raw, confirmed, and relocated pointers), owners by .pdata root;
     control: 0029F130's own 0024A610 call must be found
  C  002432B0 callers: sites and distinct .pdata-root owners (E8/E9/jcc raw), plus relocated pointers
  L  the live example bytes 7A 00 64 00 1C C0 01 0B decoded with the S layout
"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ind as I  # noqa: E402

print("E  002D9380 body, rsi uses:")
b = I.body(I.func_of(0x002D9380))
for i in b:
    if i.address in (0x002D93CF,) or "rsi +" in i.op_str or "[rsi]" in i.op_str:
        print("   %08X %s" % (i.address, I.txt(i)))
print("E  drawer site:", "%08X %s" % (0x002437B9, I.txt(I.ins(0x002437B9))), "|", "%08X %s" % (0x002437C2, I.txt(I.ins(0x002437C2))))

print("S  pins:")
for a in (0x0029F4F1, 0x0029F500, 0x0029F50F, 0x0029F531, 0x0029F176, 0x0029F18D, 0x0029F1B1, 0x0029F1E0, 0x0029F1EE,
          0x0029F206, 0x0029F20F, 0x0029F219, 0x0029F21F, 0x0029F227, 0x0029F22C):
    print("   %08X %s" % (a, I.txt(I.ins(a))))
print("S  0029F200..0029F240 in order (where the fields land):")
for i in I.dis(0x0029F1E0, 0x0029F240):
    print("   %08X %s" % (i.address, I.txt(i)))

for t in (0x002A0060, 0x0024A610):
    cs = I.calls_to(t)
    print("R  callers of %08X: %d sites; owners %s; relocated pointers %s" % (
        t, len(cs), sorted({"%08X" % (I.func_of(s) or 0) for s, _ in cs}), [("%08X" % a) for a, _ in I.abs64_refs(t, t + 1)]))
    for s, k in cs:
        print("     %08X %s owner %08X" % (s, k, I.func_of(s) or 0))
drawers = (0x002435C0, 0x00243C00, 0x00243860, 0x0029ED50, 0x0029F5D0, 0x0029FBD0, 0x002A0180)
print("R  drawer owners among them:", [("%08X" % s) for t in (0x002A0060, 0x0024A610) for s, _ in I.calls_to(t)
                                      if I.func_of(s) in drawers])
cs = I.calls_to(0x002432B0)
own = {I.func_of(s) for s, _ in cs}
print("C  002432B0: %d raw sites (%s), %d distinct owners; relocated pointers %d" % (
    len(cs), sorted({k for _, k in cs}), len(own), len(I.abs64_refs(0x002432B0, 0x002432B1))))
print("C  owners None (no .pdata):", [("%08X" % s) for s, _ in cs if I.func_of(s) is None])

bb = bytes.fromhex("7A0064001CC0010B")
x, y = struct.unpack_from("<HH", bb, 0)
v = struct.unpack_from("<I", bb, 4)[0]
print("L  x=%d y=%d w=%d h=%d byte7=0x%02X" % (x, y, v & 0xFFF, (v >> 12) & 0xFFF, bb[7]))
