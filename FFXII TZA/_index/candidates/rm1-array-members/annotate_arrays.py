"""RM-1 part 3d: the last 11 array registrations that land on named rows without their reflected identity (OPUS, 2026-09-27).

Nine of them land on a row that the store already splits word by word - a u32 count row at the member's offset (for
example PAnimationClip +0x08 channelCountPacked), then the header's +4 and +8 words. That split is the PArray/PSharray
header layout itself, so the rows are kept and the count row is annotated as word 0 of the registered member. Two land on
a whole 16-byte blob row (PPhysicsRigidBodyBase m_shapes, PLODGroup m_levels); those are retyped to their template.
Idempotent; EOL-preserving; --check verifies without writing.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parents[2]
F = DB / "_types" / "fields.tsv"
H = json.load(open(HERE / "harvest.json"))
MARK = "REFLECTED ARRAY MEMBER, RM-1 part 3d 2026-09-27 (OPUS)"
sys.path.insert(0, str(HERE))


def elem(mc):
    if not mc:
        return "?"
    a = mc.split("@", 1)[1] if "@" in mc else mc
    prim = {"M": "float", "H": "int", "I": "unsigned int", "E": "unsigned char"}
    ptr = ""
    if a.startswith("PEA"):
        a = a[3:]; ptr = "*"
    if a.startswith("V"):
        a = a[1:].split("@")[0]
    elif a[:1] in prim:
        a = prim[a[:1]]
    else:
        a = "?"
    return a + ptr


def parse(l):
    b = l.rstrip("\r\n"); return b.split("\t"), l[len(b):] or "\n"


def main():
    check = "--check" in sys.argv
    lines = F.read_bytes().decode("utf-8").splitlines(keepends=True)
    idx = {}
    for i, l in enumerate(lines):
        c = parse(l)[0]
        try:
            idx[(c[0], int(c[1], 16))] = i
        except (ValueError, IndexError):
            continue
    todo = []
    for m in H:
        if m["ctor"] != "00632A10" or m["where"] != "lands on named row":
            continue
        i = idx.get((m["cls"], m["offset"]))
        c = parse(lines[i])[0]
        if MARK in c[8] or m["site"] in c[8] or "RM-1" in c[8] or "REFLECTED" in c[8]:
            continue
        todo.append((m, i))
    acts = []
    for m, i in todo:
        c, eol = parse(lines[i])
        t = ("PArray<%s>" if m["a7"] == 3 else "PSharray<%s>") % elem(m.get("member_class"))
        if c[2] == "16" and c[4].startswith("uint8["):
            acts.append(("RETYPE", m["cls"], c[3], c[4], t))
            c[8] = ("%s: registrar %s registers '%s' at offset 0x%X through 00632A10 (a7=%d) at %s; this 16-byte row is its"
                    " %s header (u32 count with bit 31 the keep-buffer flag, +4 untouched, +8 the element pointer). Retyped from"
                    " %s. || %s" % (MARK, m["caller"], m["name"], m["offset"], m["a7"], m["site"], t, c[4], c[8]))
            c[4] = t
        elif c[2] == "4":
            acts.append(("WORD0", m["cls"], c[3], m["name"]))
            c[8] = ("%s: this word is +0 - the count, with bit 31 the keep-buffer flag - of the %s member '%s' that registrar %s"
                    " registers at offset 0x%X through 00632A10 (a7=%d) at %s. The store's rows at +0x%X and +0x%X are the"
                    " header's other two words (+4 untouched, +8 the element pointer); they are kept as rows. || %s"
                    % (MARK, t, m["name"], m["caller"], m["offset"], m["a7"], m["site"], m["offset"] + 4, m["offset"] + 8, c[8]))
        else:
            print("REFUSED", m["cls"], m["name"], c[2], c[4]); sys.exit(1)
        lines[i] = "\t".join(c) + eol
    for a in acts:
        print(*a)
    if check:
        print("CHECK OK", len(acts)); return
    if acts:
        F.write_bytes("".join(lines).encode("utf-8"))
    print("applied", len(acts))


if __name__ == "__main__":
    main()
