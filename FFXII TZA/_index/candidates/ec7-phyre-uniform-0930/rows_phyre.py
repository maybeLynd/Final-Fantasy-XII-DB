"""rows_phyre.py DB - counts + dated sentence for the Phyre rows the uniform closure-source rule changes; PhyreCore gets a
sentence that its admission is stopped. Idempotent; no addresses in notes."""
import io, os, re, sys
DB = sys.argv[1]
PAGE = "22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md"
TAG = " 2026-09-30 (SWE2-EC7, closure-source ruling - uniform, record _index/candidates/ec7-phyre-uniform-0930):"


def count_members(path, rel):
    mf = os.path.join(os.path.dirname(path), rel.strip().replace("/", os.sep))
    n, first = 0, True
    for ml in io.open(mf, encoding="utf-8", errors="replace"):
        ml = ml.split("#", 1)[0].strip()
        if not ml: continue
        tok = ml.split()[0].replace("0x", "")
        if first:
            first = False
            if not re.fullmatch(r"[0-9A-Fa-f]{6,8}", tok): continue
        n += 1
    return n


def joined(k):
    return (" %d member(s) joined the family under FABLE's closure-source ruling (SWE2-EC7-REQ-FABLE-CLOSURE-CASCADE-RULE-0930,"
            " uniform per SWE2-EC7-REQ-FABLE-PHYRE-UNIFORM-RULE-0930): the selector's predicate now ignores accounting state,"
            " so an A-measured body or another family's body that passes the module predicate is a closure source (it stays"
            " A or stays with its declaring family and is never written here); this restores the 2026-09-30 re-status"
            " cascade and the bodies the same exclusion kept out since declaration. Falsified by reading a seeded random"
            " sample against this row's description (no misfit) and by check_family_forms (0 MISMATCH); per-family member"
            " diff, A-source list and the predicate members owned by other families are in the record." % k)


rows = {}
p = os.path.join(DB, PAGE)
L = io.open(p, encoding="utf-8", newline="").read().split("\n")
for i, l in enumerate(L):
    m = re.match(r'  - "(Phyre [A-Za-z]+ module) \| ', l)
    if not m: continue
    name = m.group(1)
    raw = l.rstrip("\r"); cr = l.endswith("\r")
    if TAG in raw: raw = raw[:raw.index(TAG)].rstrip() + '"'
    parts = raw.split(" | ")
    old, new = int(parts[3]), count_members(p, parts[2])
    if name == "Phyre PhyreCore module":
        s = (" The uniform rule is NOT applied to this row: a sample read of the +988 bodies it would admit found game code"
             " (FFXII movement, battle-menu and multi-kilobyte presentation bodies), because this predicate has no"
             " namespace segment or geography and the A/declared exclusions were acting as its firewall. Per the ruling"
             " a misfit stops the admission; the selector keeps the old exclusion for this module until its predicate is"
             " repaired.")
        assert new == old, (name, old, new)
    elif new == old:
        continue
    else:
        assert new > old, (name, old, new)
        s = joined(new - old)
        parts[3] = str(new)
    body = " | ".join(parts)[:-1].rstrip()
    L[i] = body + ("" if body.endswith(".") else ".") + TAG + s + '"' + ("\r" if cr else "")
    print(name, old, "->", new)
io.open(p, "w", encoding="utf-8", newline="").write("\n".join(L))
