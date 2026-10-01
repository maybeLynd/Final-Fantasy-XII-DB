"""RM-1 part 2: the D3D11 description-struct members registered through the enum constructor 00632BE0 and the
fixed-size constructor 00632A70, carved into the store's declared gaps. The builder -> struct binding is the field
schema's own class_obj for the same builders (and the store's 02CF57B0 note for D3D11_DEPTH_STENCILOP_DESC).
Idempotent; EOL-preserving; refuses anything that does not tile its gap exactly."""
import json, pathlib, collections
DB = pathlib.Path(__file__).resolve().parents[3]
F = DB / "_types" / "fields.tsv"
H = json.load(open(pathlib.Path(__file__).with_name("harvest.json")))
MARK = "REFLECTED MEMBER, RM-1 part 2 2026-09-27 (OPUS)"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BUILDER = {"00613E80": ("CD3D11_RASTERIZER_DESC", "02CF52C0"), "00613A30": ("CD3D11_DEPTH_STENCIL_DESC", "02CF5A80"),
           "006143B0": ("D3D11_DEPTH_STENCILOP_DESC", "02CF57B0"), "00614640": ("D3D11_RENDER_TARGET_BLEND_DESC", "02CF5EB0"),
           "00613800": ("CD3D11_BLEND_DESC", "02CF6320")}
ms = [m for m in H if m["caller"] in BUILDER and m["ctor"] in ("00632BE0", "00632A70")]
assert len(ms) == 15, len(ms)
lines = F.read_bytes().decode("utf-8").splitlines(keepends=True)
if any(MARK in l for l in lines):
    print("already applied"); raise SystemExit
by = collections.defaultdict(list)
for m in ms: by[BUILDER[m["caller"]][0]].append(m)
def parse(l):
    b = l.rstrip("\r\n"); return b.split("\t"), l[len(b):] or "\n"
def row(t, off, size, name, ctype, mean, rd, conf, ev):
    return "\t".join([t, "0x%04X" % off, str(size), name, ctype, mean, rd, conf, ev])
n = 0
for cls, lst in sorted(by.items()):
    lst.sort(key=lambda m: m["offset"])
    idx = [i for i, l in enumerate(lines) if l.startswith(cls + "\t")]
    gaps = []
    for i in idx:
        c, e = parse(lines[i])
        if c[3].startswith("unobserved"): gaps.append((i, int(c[1], 16), int(c[2]), c, e))
    for i, o, s, c, e in sorted(gaps, reverse=True):
        inside = [m for m in lst if o <= m["offset"] < o + s]
        if not inside: continue
        new, cur = [], o
        for m in inside:
            assert m["offset"] == cur, (cls, m["name"], hex(m["offset"]), hex(cur))
            desc = BUILDER[m["caller"]][1]
            if m["ctor"] == "00632BE0":
                size, ctype = 4, "int (enum)"
                mean = ("engine-registered member name %s (Phyre reflection of the D3D11 description struct); an enum field whose"
                        " registration carries %d as a7, the enumeration's highest value in the D3D11 SDK." % (m["name"], m["a7"]))
                how = "the enum member constructor 00632BE0"
            else:
                size, ctype = 32 * m["a7"], "D3D11_RENDER_TARGET_BLEND_DESC[%d]" % m["a7"]
                mean = ("engine-registered member name %s; a fixed-size array of %d D3D11_RENDER_TARGET_BLEND_DESC (0x20 each)."
                        % (m["name"], m["a7"]))
                how = "the fixed-size member constructor 00632A70"
            ev = ("%s: builder %s (the %s descriptor %s, as the field schema's class_obj shows for the same builder) calls %s"
                  " at %s with name '%s', offset 0x%X, a7=%d. The recovered field schema never harvested these sites (RM-1)."
                  " Width: the members tile the declared gap exactly with the neighbouring registered rows. Evidence"
                  " _index/candidates/rm1-array-members/. %s" % (MARK, m["caller"], cls, desc, how, m["site"], m["name"],
                  m["offset"], m["a7"], EXE))
            new.append(row(cls, m["offset"], size, m["name"], ctype, mean, "TYPE RESOLVED", "PROVEN", ev))
            cur += size; n += 1
        assert cur == o + s, (cls, "members do not tile the gap", hex(o), s, hex(cur))
        lines[i:i + 1] = [r + e for r in new]
F.write_bytes("".join(lines).encode("utf-8"))
print("carved", n, "members in", len(by), "D3D11 structs")
