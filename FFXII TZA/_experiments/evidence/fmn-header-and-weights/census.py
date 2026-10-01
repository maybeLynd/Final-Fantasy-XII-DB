"""The @FMN bone-motion header bits command 0x09 branches on, and the @FMW it looks up by the same name.

Read-only over an extracted copy of the game (FF12_EXTRACT; default D:/FFXII_TZA_extract), every *.ca under ps2data.
What the code reads (00417F40, read whole 2026-09-20, FABLE):
  @FMN dword +4: bits 0-1 'type' (0 and 1 are acted on), bits 4-5 (== 1 -> bind the weights), bits 24-25 (== 2 -> the
  look-controller set-up); byte +0x24 bit 0 -> the playing state's loop flag; name at +0x10.
  For a type-1 motion the invoker finds the '@FMW' section WITH THE MOTION'S OWN NAME.
Predictions that could fail:
  P1  every type-1 @FMN has an @FMW of the same name in the same container
  P2  bits 0-1 never hold 2 or 3 (the invoker does nothing for them)
Control: 18,303 @FMN and 18,303 @FMW in the animation containers (children census).
"""
import os, struct, collections
ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
nfmn = nfmw = 0; typ = collections.Counter(); b45 = collections.Counter(); b2425 = collections.Counter(); loop = collections.Counter()
t1 = t1_ok = anyname = anyname_ok = 0; word4 = collections.Counter()
for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data")):
    for f in fn:
        if not f.endswith(".ca"):
            continue
        d = open(os.path.join(dp, f), "rb").read()
        if d[:4] != b"@FRP":
            continue
        v = u32(d, 4); base = 0x30 if v == 0 else 0x40
        fmn = []; fmw = set()
        for i in range(u32(d, 0xC)):
            o = u32(d, base + 4 * i)
            if v == 1 and not o:
                continue
            b = base + o; t = d[b:b + 4]; name = d[b + 0x10:b + 0x30].split(b"\0")[0]
            if t == b"@FMN":
                fmn.append((name, u32(d, b + 4), d[b + 0x24]))
            elif t == b"@FMW":
                fmw.add(name)
        nfmn += len(fmn); nfmw += len(fmw)
        for name, w, b24 in fmn:
            typ[w & 3] += 1; b45[(w >> 4) & 3] += 1; b2425[(w >> 24) & 3] += 1; loop[b24 & 1] += 1; word4["%08X" % w] += 1
            anyname += 1; anyname_ok += name in fmw
            if w & 3 == 1:
                t1 += 1; t1_ok += name in fmw
print("control: @FMN", nfmn, "; distinct @FMW names per container, summed:", nfmw, "(children census: 18,303 of each; one container repeats a name)")
print("@FMN dword +4, commonest values:", word4.most_common(8))
print("P2  bits 0-1 (value -> motions):", sorted(typ.items()))
print("    bits 4-5:", sorted(b45.items()), "; bits 24-25:", sorted(b2425.items()), "; byte +0x24 bit 0 (loop):", sorted(loop.items()))
print("P1  type-1 motions:", t1, "; with an @FMW of the same name in the same container:", t1_ok)
print("    all motions with a same-name @FMW:", anyname_ok, "of", anyname)
