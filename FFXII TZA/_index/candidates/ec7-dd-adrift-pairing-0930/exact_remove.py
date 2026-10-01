"""exact_remove.py KIT DB - stage 1 of the A-drift repair: in every row check_dispositions refuses ONLY for A overlap,
delete the A members' lines from the members file and set the row's count to the new length. Keeps line endings.
Prints row, old -> new, removed addresses. Notes are NOT written here."""
import io, os, re, sys

KIT, DB = sys.argv[1:3]
sys.path.insert(0, KIT)
import check_dispositions as CD  # noqa
sizes = CD.load_functions()
r = CD.evaluate(DB, sizes)
a_set = CD.measure_a(DB, sizes)[0]
refA = {w for w, why in r["refusals"] if "already measured as A" in why}
other = [(w, why) for w, why in r["refusals"] if w not in refA]
if other:
    print("NON-A REFUSALS (not touched):")
    for w, why in other:
        print("  ", w, why[:150])
for doc, parts in CD.parse_families(DB):
    who = "%s :: %s" % (os.path.basename(doc), parts[0])
    if who not in refA:
        continue
    mf = os.path.join(os.path.dirname(doc), parts[2].replace("/", os.sep))
    raw = io.open(mf, encoding="utf-8", newline="").read()
    L = raw.split("\n")
    gone = []
    keep = []
    for l in L:
        tok = l.split("#", 1)[0].strip()
        tok = tok.split()[0].replace("0x", "") if tok else ""
        if re.fullmatch(r"[0-9A-Fa-f]{6,8}", tok) and int(tok, 16) in a_set:
            gone.append(tok.upper())
            continue
        keep.append(l)
    io.open(mf, "w", encoding="utf-8", newline="").write("\n".join(keep))
    new = len(CD.read_members(doc, parts[2]))
    # count field on the row line
    t = io.open(doc, encoding="utf-8", newline="").read()
    pat = re.compile(r'^(  - "' + re.escape(parts[0]) + r' \| ' + re.escape(parts[1]) + r' \| ' + re.escape(parts[2])
                     + r' \| )(\d+)( \|)', re.M)
    hits = pat.findall(t)
    assert len(hits) == 1, (who, len(hits))
    old = int(hits[0][1])
    t = pat.sub(lambda g: g.group(1) + str(new) + g.group(3), t)
    io.open(doc, "w", encoding="utf-8", newline="").write(t)
    print("%s | %d -> %d | removed %s" % (who, old, new, " ".join(gone)))
