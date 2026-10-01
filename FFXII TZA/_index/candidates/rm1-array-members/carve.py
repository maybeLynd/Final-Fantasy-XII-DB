"""RM-1 part 1: carve the array members that land inside declared gaps (kinds 3/4, 16-byte header), and name the
PArray / PSharray +0x8 rows from the template registrations (m_els / m_u). Idempotent; EOL-preserving; refuses a member
that does not fit wholly inside one gap row."""
import json, pathlib, collections, re
DB = pathlib.Path(r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA")
F = DB / "_types" / "fields.tsv"
H = json.load(open(pathlib.Path(__file__).with_name("harvest.json")))
MARK = "REFLECTED ARRAY MEMBER, RM-1 2026-09-27 (OPUS)"
EXE = "exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
PKG = "_index/candidates/rm1-array-members/ (harvest.py, carve.py, check.py)"
def elem(mc):
    if not mc: return "?"
    a = mc.split("@", 1)[1] if "@" in mc else mc
    prim = {"M": "float", "H": "int", "I": "unsigned int", "E": "unsigned char"}
    ptr = ""
    if a.startswith("PEA"): a = a[3:]; ptr = "*"
    if a.startswith("V"): a = a[1:].split("@")[0]
    elif a[:1] in prim: a = prim[a[:1]]
    else: a = "?"
    return a + ptr
def tmpl(m):
    return ("PArray<%s>" if m["a7"] == 3 else "PSharray<%s>") % elem(m.get("member_class"))
HDR = {3: ("the shared PClassDataMemberPhyreArray accessors (all 59 member vtables): u32 count at +0 with bit 31 as the "
           "keep-buffer flag, +4 untouched, element pointer at +8"),
       4: ("the shared PClassDataMemberPhyreSharray accessors (all 10 member vtables): u32 count at +0 with bit 31 as the "
           "keep-buffer flag, +4 untouched, +8 the element pointer above count 1 or the single element inline at count 1")}
lines = F.read_bytes().decode("utf-8").splitlines(keepends=True)
if any(MARK in l for l in lines):
    print("already applied"); raise SystemExit
gap = [m for m in H if m.get("where") == "inside declared gap" and m.get("a7") in (3, 4)]
by = collections.defaultdict(list)
for m in gap: by[m["cls"]].append(m)
def parse(l):
    body = l.rstrip("\r\n"); return body.split("\t"), l[len(body):] or "\n"
def row(t, off, size, name, ctype, mean, rd, conf, ev):
    return "\t".join([t, "0x%04X" % off, str(size), name, ctype, mean, rd, conf, ev])
n_members = 0
for cls, ms in sorted(by.items()):
    ms.sort(key=lambda m: m["offset"])
    # group members by the gap row that contains them
    idx = [i for i, l in enumerate(lines) if l.startswith(cls + "\t")]
    rows = {}
    for i in idx:
        c, e = parse(lines[i])
        rows[i] = (int(c[1], 16), int(c[2]) if c[2].isdigit() else 0, c[3], c, e)
    plan = collections.defaultdict(list)
    for m in ms:
        hit = [i for i, (o, s, nm, c, e) in rows.items() if nm.startswith("unobserved") and o <= m["offset"] and m["offset"] + 16 <= o + s]
        assert len(hit) == 1, "%s.%s +0x%X does not fit one gap: %s" % (cls, m["name"], m["offset"], hit)
        plan[hit[0]].append(m)
    for i in sorted(plan, reverse=True):          # bottom-up so indices stay valid
        o, s, nm, c, e = rows[i]
        new, cur = [], o
        for m in sorted(plan[i], key=lambda m: m["offset"]):
            if m["offset"] > cur:
                new.append(row(cls, cur, m["offset"] - cur, "unobservedSpan%04X" % cur, "u8[%d]" % (m["offset"] - cur),
                               c[5], c[6], c[7], c[8] + " || RE-TILED " + MARK + ": the part of this gap before the reflected member " + m["name"] + "."))
            mean = ("engine-registered member name %s (Phyre reflection); a 16-byte %s header. What the elements are for is NOT "
                    "CLAIMED beyond the registered name." % (m["name"], tmpl(m)))
            ev = ("%s: registrar %s calls the PClassDataMemberArray constructor 00632A10 at %s with name '%s', offset 0x%X, a7=%d, "
                  "a8=%s%s. The recovered field schema never harvested 00632A10 sites (RM-1). Header from %s. Evidence %s. %s"
                  % (MARK, m["caller"], m["site"], m["name"], m["offset"], m["a7"], m.get("a8"),
                     (", then installs the vtable of " + m["member_class"]) if m.get("member_class") else
                     " (the template vtable is installed outside the eight instructions read; the kind comes from a7)",
                     HDR[m["a7"]], PKG, EXE))
            new.append(row(cls, m["offset"], 16, m["name"], tmpl(m), mean, "TYPE RESOLVED", "PROVEN", ev))
            cur = m["offset"] + 16; n_members += 1
        if cur < o + s:
            new.append(row(cls, cur, o + s - cur, "unobservedSpan%04X" % cur, "u8[%d]" % (o + s - cur), c[5], c[6], c[7],
                           c[8] + " || RE-TILED " + MARK + ": the part of this gap after the reflected member(s)."))
        lines[i:i + 1] = [r + e for r in new]
# PArray / PSharray +0x8 names from the template registrations
els = [m for m in H if m.get("name") == "m_els" and m.get("offset") == 8]
mu = [m for m in H if m.get("name") == "m_u" and m.get("offset") == 8]
for t, oldname, newname, grp in (("PArray", "dataPtr", "m_els", els), ("PSharray", "dataOrSingleElement", "m_u", mu)):
    k = next(i for i, l in enumerate(lines) if l.startswith(t + "\t0x0008\t8\t" + oldname + "\t"))
    c, e = parse(lines[k])
    c[3] = newname
    c[8] = ("%s: the template's own registration names this word: %d %s<T> instantiations register member '%s' at offset 8 "
            "through 00632A10 with a7=2 (PClassDataMemberArrayDynamic), e.g. %s; renamed from %s. || " % (MARK, len(grp), t, newname,
            ", ".join(m["site"] for m in grp[:3]), oldname)) + c[8]
    lines[k] = "\t".join(c) + e
F.write_bytes("".join(lines).encode("utf-8"))
print("carved", n_members, "members in", len(by), "classes; PArray+8 -> m_els (%d), PSharray+8 -> m_u (%d)" % (len(els), len(mu)))
