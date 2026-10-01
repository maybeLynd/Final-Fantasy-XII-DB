"""page_checks.py - SWE2-AUDIT-SPEC mechanical checks for an owner re-status (2026-09-30). Reads only.

  python page_checks.py PAGE [PAGE ...]      (paths relative to Database/FFXII TZA)

Per page:
  F  front matter: status (first 90 chars), evidence_tier, external_production.status if present
  H  level-2 headings, and which template sections (SYSTEM 1-9 / FORMAT 1-8 by keyword) are missing
  B  open boxes '- [ ]'
  T  every markdown table whose header has a 'tier' column: rows whose cell count differs from the header's, and rows
     whose tier cell is not an integer 1..11 (a struck row still counts - its tier cell is what a reader sees)
  N  'no reader' / 'not read' / 'unread' / 'inert' phrases (table rows and prose), each with whether the same line is
     struck (~~) or carries a superseded / answered marker, and the nearest following 'Superseded' note line number
"""
import io, os, re, sys

DB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SYSTEM = ["what the player sees", "native mechanism|where it sits|mechanism", "key addresses", "data structures|layout",
          "call chain", "modding", "what is not known|not known|does not claim", "evidence", "related"]
FORMAT = ["what the player sees", "layout", "loader contract", "key addresses", "corpus", "falsification",
          "does not claim|not known", "related"]


def cells(line):
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s[1:-1] if s.endswith("|") else s[1:]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def check(rel):
    p = os.path.join(DB, rel)
    t = io.open(p, encoding="utf-8").read()
    L = t.split("\n")
    fm_end = L.index("---", 1) if L[0] == "---" else 0
    fm = "\n".join(L[1:fm_end])
    st = re.search(r"^status:\s*(.*)$", fm, re.M)
    et = re.search(r"^evidence_tier:\s*(.*)$", fm, re.M)
    ep = re.search(r"^external_production:\s*\n((?:\s+.*\n?)+)", fm + "\n", re.M)
    eps = re.search(r"status:\s*(.*)", ep.group(1)).group(1) if ep else None
    print("=== %s" % rel)
    print("F status: %s" % ((st.group(1)[:90] + "...") if st else None))
    print("F evidence_tier: %s   external_production.status: %s" % (et.group(1) if et else None, eps))
    h2 = [(k + 1, l[3:].strip()) for k, l in enumerate(L) if l.startswith("## ")]
    kind = "FORMAT" if re.search(r"^## \d+\.\s*The (layout|loader contract)", t, re.M | re.I) else "SYSTEM"
    want = FORMAT if kind == "FORMAT" else SYSTEM
    miss = [w for w in want if not any(re.search(w, h.lower()) for _, h in h2)]
    print("H template %s; %d level-2 headings; missing sections: %s" % (kind, len(h2), miss or "none"))
    ob = [k + 1 for k, l in enumerate(L) if re.match(r"\s*- \[ \]", l)]
    print("B open boxes: %d %s" % (len(ob), ob[:10]))
    k = fm_end
    while k < len(L):
        c = cells(L[k])
        if c and k + 1 < len(L) and re.match(r"^\|?\s*:?-{2,}", L[k + 1].strip()):
            hdr = [x.lower() for x in c]
            ti = next((j for j, x in enumerate(hdr) if x == "tier" or x.startswith("tier")), None)
            j = k + 2
            while j < len(L) and L[j].strip().startswith("|"):
                r = cells(L[j])
                if ti is not None:
                    bad = []
                    if len(r) != len(c):
                        bad.append("cells %d != header %d" % (len(r), len(c)))
                    if ti < len(r):
                        tv = re.sub(r"[~*`]", "", r[ti]).strip()
                        if not re.fullmatch(r"(1[01]|[1-9])(\s*[-/,]\s*(1[01]|[1-9]))*", tv):
                            bad.append("tier cell %r" % r[ti][:40])
                    if bad:
                        print("T line %d: %s :: %s" % (j + 1, "; ".join(bad), L[j][:150]))
                j += 1
            k = j
            continue
        k += 1
    sup = [k + 1 for k, l in enumerate(L) if re.search(r"superseded", l, re.I)]
    for k, l in enumerate(L):
        if k < fm_end:
            continue
        if re.search(r"no reader|not read\b|unread|\binert\b|nothing reads", l, re.I):
            struck = "~~" in l
            marked = bool(re.search(r"superseded|answered|read 20|→|->.*§|corrected", l, re.I))
            nxt = next((s for s in sup if s >= k + 1), None)
            print("N line %d struck=%s marked=%s next-superseded-line=%s :: %s" % (
                k + 1, struck, marked, nxt, l.strip()[:140]))


for a in sys.argv[1:]:
    check(a)
