"""RM-1 part 3c: the seven Phyre enum registrations on named rows are 4-byte ints (OPUS, 2026-09-27).

The enum member constructor 00632BE0 ORs 0x20 into its sixth argument and passes it as the name node's attribute word
(00632C10-00632C1F), so harvest's a6 (0x10 / 0x08) is the attribute word - bit 5 is the enum flag the packed namespace
also shows - and says nothing about width. The width is the enum's value type: every one of the seven registrars loads
r8 with the descriptor 01F2E550, which the recovered field schema names `int` for 26 members and the type store's
README measures at 4 bytes. a7 is the highest enumerator.
  SPLIT   an enum row wider than 4 bytes keeps 4 as `int (enum)`; the rest becomes an unobserved tail
  RETYPE  a 4-byte enum row whose ctype is a byte blob becomes `int (enum)`
Idempotent; EOL-preserving; --check verifies without writing.
"""
import pathlib, sys

DB = pathlib.Path(__file__).resolve().parents[3]
F = DB / "_types" / "fields.tsv"
MARK = "ENUM MEMBER, RM-1 part 3c 2026-09-27 (OPUS)"
ENUMS = [("PAnimationChannelBase", "m_interp", 0x40, 3, "005AF37F"), ("PAnimationChannelTarget", "m_type", 0x20, 6, "005AF939"),
         ("PAnimationSlotListIndex", "m_interp", 0x08, 3, "005B21D0"), ("PMeshSegmentBase", "m_primitiveType", 0x18, 6, "0066709C"),
         ("PPhysicsShapeBase", "m_type", 0x60, 8, "00697662"), ("PModifierNetwork", "m_streamingStrategy", 0x44, 1, "006D12DC"),
         ("PModifierNetworkInfoPacket", "m_streamingStrategy", 0x10, 1, "006D1AE3")]


def parse(l):
    b = l.rstrip("\r\n"); return b.split("\t"), l[len(b):] or "\n"


def main():
    check = "--check" in sys.argv
    lines = F.read_bytes().decode("utf-8").splitlines(keepends=True)
    acts = []; bad = []
    for cls, mem, off, a7, site in ENUMS:
        hits = [i for i, l in enumerate(lines) if l.startswith(cls + "\t") and int(parse(l)[0][1], 16) == off]
        if len(hits) != 1:
            bad.append((cls, mem, "rows at offset", len(hits))); continue
        i = hits[0]; c, eol = parse(lines[i])
        if MARK in c[8]:
            continue
        if c[3] != mem:
            bad.append((cls, mem, "row named " + c[3])); continue
        size = int(c[2])
        ev = ("%s: registration %s through the enum member constructor 00632BE0 with the value-type descriptor 01F2E550"
              " (int, 4 bytes) and a7=%d, the highest enumerator; a6 is the attribute word, not a width." % (MARK, site, a7))
        if size == 4 and c[4] == "int (enum)":
            continue
        if size < 4:
            bad.append((cls, mem, "narrower than 4")); continue
        acts.append(("SPLIT" if size > 4 else "RETYPE", cls, mem, size, c[4]))
        old = c[4]; c[2], c[4] = "4", "int (enum)"
        c[8] = ev + " Was %d bytes (%s). || %s" % (size, old, c[8])
        new = "\t".join(c) + eol
        if size > 4:
            new += "\t".join([cls, "0x%04X" % (off + 4), str(size - 4), "unobservedTail%04X" % (off + 4), "u8[%d]" % (size - 4),
                              "the %d bytes after the 4-byte enum %s, inside the row it used to fill" % (size - 4, mem),
                              "DISCOVERED", "UNKNOWN", MARK + ": split off " + mem + " by its value type's width."]) + eol
        lines[i] = new
    for a in acts:
        print(*a)
    if bad:
        print("REFUSED", bad); sys.exit(1)
    if check:
        print("CHECK OK", len(acts)); return
    F.write_bytes("".join(lines).encode("utf-8")); print("applied", len(acts))


if __name__ == "__main__":
    main()
