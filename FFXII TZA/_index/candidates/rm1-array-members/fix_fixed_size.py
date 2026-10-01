"""RM-1 part 3b: the 19 fixed-size registrations on named rows, given their element type and count (OPUS, 2026-09-27).

For each 00632A70 registration the element descriptor is the value the registrar puts in r8: the return of a
primitive getter (006301F0 -> 01F2E690 float, 006300A0 -> 01F2E500 unsigned short, 00630180 -> 01F2E5A0 unsigned int,
0062FFC0 -> 01F2E460 unsigned char - each named by the recovered field schema's own type_obj column) or a lea of a class
descriptor. a7 is the element count. The member's width is therefore count x element size, and each row is checked
against it:
  WIDEN   a row narrower than the member that is followed by an unobserved span it tiles exactly
          (PShaderPassParameterLocationTypesBase m_parameterStart / m_parameterCount: uint16 -> uint16[4], which the
          packed namespace's `PUInt16 m_parameterStart[4]` states independently; PAnimationConstantChannel m_value:
          float -> float[4], closing the class at 0x58)
  SPLIT   a row wider than the member: the member keeps its width and the rest becomes an unobserved tail
          (PMeshInstanceBounds m_min / m_size: 16 -> float[3] + 4)
  RETYPE  a row of the right width whose ctype is a byte blob (uint8[N] -> float[n] / uint32[32])
Rows whose ctype already agrees are left alone. Enum registrations (00632BE0) are not resized: their a6 (8 or 16) is not
understood. Idempotent; EOL-preserving; --check verifies without writing.
"""
import pathlib, sys

DB = pathlib.Path(__file__).resolve().parents[3]
F = DB / "_types" / "fields.tsv"
MARK = "FIXED-SIZE MEMBER, RM-1 part 3b 2026-09-27 (OPUS)"
E = {"float": 4, "unsigned short": 2, "unsigned int": 4, "unsigned char": 1}
C = {"float": "float", "unsigned short": "uint16", "unsigned int": "uint32", "unsigned char": "uint8"}
# (class, member, offset, a7, element, site, getter)
REGS = [
    ("PAnimationConstantChannel", "m_value", 0x48, 4, "float", "005B0C36", "006301F0"),
    ("PAnimationDataSourceListEntry", "m_inputIndex", 0x0C, 32, "unsigned int", "005B0FDE", "00630180"),
    ("PMeshInstanceBounds", "m_min", 0x00, 3, "float", "005E671D", "006301F0"),
    ("PMeshInstanceBounds", "m_size", 0x18, 3, "float", "005E678B", "006301F0"),
    ("PShaderPassParameterLocationTypesBase", "m_parameterStart", 0x00, 4, "unsigned short", "005EA16A", "006300A0"),
    ("PShaderPassParameterLocationTypesBase", "m_parameterCount", 0x08, 4, "unsigned short", "005EA1E3", "006300A0"),
    ("PSkeletonJointBounds", "m_min", 0x00, 3, "float", "00667789", "006301F0"),
    ("PSkeletonJointBounds", "m_size", 0x10, 3, "float", "006677FE", "006301F0"),
    ("PBitmapFontCharInfo", "m_uv", 0x0C, 2, "float", "0067D592", "006301F0"),
    ("PBitmapFontCharInfo", "m_offset", 0x1C, 2, "float", "0067D6ED", "006301F0"),
    ("PBitmapFontCharInfo", "m_advance", 0x24, 2, "float", "0067D762", "006301F0"),
    ("PPhysicsCapsuleBase", "m_radiusArray", 0x70, 2, "float", "006941AA", "006301F0"),
    ("PPhysicsCylinderBase", "m_radiusArray", 0x70, 2, "float", "0069551A", "006301F0"),
    ("PPhysicsTaperedCapsule", "m_upperRadiusArray", 0x70, 2, "float", "006977ED", "006301F0"),
    ("PPhysicsTaperedCapsule", "m_lowerRadiusArray", 0x78, 2, "float", "00697862", "006301F0"),
    ("PPhysicsTaperedCylinder", "m_upperRadiusArray", 0x70, 2, "float", "0069799D", "006301F0"),
    ("PPhysicsTaperedCylinder", "m_lowerRadiusArray", 0x78, 2, "float", "00697A12", "006301F0"),
    ("PModifierNetworkInfoPacket_ModifierInstance", "m_inputOutputIndices", 0x09, 23, "unsigned char", "006D20C9", "0062FFC0"),
]


def parse(l):
    b = l.rstrip("\r\n"); return b.split("\t"), l[len(b):] or "\n"


def main():
    check = "--check" in sys.argv
    lines = F.read_bytes().decode("utf-8").splitlines(keepends=True)
    actions = []; bad = []
    for cls, mem, off, n, el, site, getter in REGS:
        want = n * E[el]; ctype = "%s[%d]" % (C[el], n)
        idx = {int(parse(lines[i])[0][1], 16): i for i, l in enumerate(lines) if l is not None and l.startswith(cls + "\t")}
        if off not in idx:
            bad.append((cls, mem, "no row at offset")); continue
        i = idx[off]; c, eol = parse(lines[i])
        if MARK in c[8]:
            continue
        if c[3] != mem:
            bad.append((cls, mem, "row named " + c[3])); continue
        size = int(c[2]); ev = ("%s: registration %s through the fixed-size member constructor 00632A70 with a7=%d and"
                                " the element descriptor from %s (%s, named by the field schema's type_obj); width %d x %d"
                                " = %d bytes." % (MARK, site, n, getter, el, n, E[el], want))
        if size == want:
            if c[4] == ctype:
                continue
            actions.append(("RETYPE", cls, mem, c[4], ctype))
            c[8] = ev + " Retyped from " + c[4] + ". || " + c[8]; c[4] = ctype
            lines[i] = "\t".join(c) + eol
        elif size < want:
            nxt = idx.get(off + size)
            nc = parse(lines[nxt])[0] if nxt is not None else None
            if not nc or not nc[3].startswith("unobserved") or off + size + int(nc[2]) != off + want:
                bad.append((cls, mem, "narrow row and the next span does not close it")); continue
            actions.append(("WIDEN", cls, mem, size, want))
            old = c[4]; c[2], c[4] = str(want), ctype
            c[8] = ev + " WIDENED from %d bytes (%s) and absorbs %s. || %s" % (size, old, nc[3], c[8])
            lines[i] = "\t".join(c) + eol; lines[nxt] = None
        else:
            actions.append(("SPLIT", cls, mem, size, want))
            old = c[4]; c[2], c[4] = str(want), ctype
            c[8] = ev + " NARROWED from %d bytes (%s); the remaining %d bytes are a separate unobserved tail. || %s" % (size, old, size - want, c[8])
            tail = [cls, "0x%04X" % (off + want), str(size - want), "unobservedTail%04X" % (off + want), "u8[%d]" % (size - want),
                    "the %d bytes after %s's %d-byte member, inside the row the member used to fill" % (size - want, mem, want),
                    "DISCOVERED", "UNKNOWN", MARK + ": split off " + mem + " by its registration width; nothing here names these bytes."]
            lines[i] = "\t".join(c) + eol + "\t".join(tail) + eol
    for a in actions:
        print(*a)
    if bad:
        print("REFUSED", bad); sys.exit(1)
    if check:
        print("CHECK OK", len(actions), "actions"); return
    F.write_bytes("".join(l for l in lines if l is not None).encode("utf-8"))
    print("applied", len(actions))


if __name__ == "__main__":
    main()
