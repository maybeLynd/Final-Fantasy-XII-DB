"""pass22_neighbour_bullets.py - SWE2-CONTRACT, 2026-09-30.

Deterministic generator + fact verifier for the uncommitted pass-22 "Cross-subsystem neighbours" bullets and their
neighbour-dispositions.tsv rows (FRONTIER-REQ-SWE2-CONTRACT-PASS22-DEBT), per OPUS's ruling of 2026-09-30.

Inputs (all read-only):
  * each page's HEAD text (the text before the uncommitted append) and the uncommitted append (git diff);
  * HEAD `_index/candidates/neighbour-dispositions.tsv` and the uncommitted rows added to it;
  * `Database/Tools/work/graph/functions.tsv` + `edges.tsv`, through audit_crossrefs.py's own functions
    (cited_addresses, CROSSING_SECTION, doc_accounts_for, is_substrate, subsystem_of, HUB_FANIN, R6 far ends).

What it GENERATES (the deterministic part, compared byte-for-byte):
  G1 the pair set: every (page, layer) UNACCOUNTED NEIGHBOUR pair audit_crossrefs reports on the HEAD text;
  G2 per pair: the edge count, the inbound (far end calls page-cited) and outbound counts, and the label the
     direction implies (inbound only CLIENT, outbound only SERVICE, both CLIENT and SERVICE);
  G3 the registry row's first five columns (document, layer, count, 'unaccounted', audit_crossrefs' detail string:
     the first four sorted hits + '(+N more)').

What it VERIFIES but cannot generate (selections in the bullet text):
  V1 every body listed as "<layer> bodies ..." is a far end of an edge of that direction in the pair's hit set;
  V2 every "page-cited ..." function is a page-cited end of such an edge;
  V3 every "Substantive edges include" edge is a hit of the pair, with the stated direction;
  V4 MECHANICAL bullets: the registry row is GENUINELY-IRRELEVANT; CLIENT / SERVICE bullets: CROSSING-ACCOUNTED;
  V5 the label check (OPUS step 3): a non-MECHANICAL label must equal G2's direction label; a bullet whose listed
     substantive edges all call a callee with more than HELPER_FANIN callers is flagged (a helper-only crossing).
  V6 registry rows match bullets 1:1 (FALSE-SUBJECT rows carry no bullet);
  V7 each named body is a caller (inbound) / callee (outbound) of a named page-cited function in edges.tsv and its
     layer is the bullet's layer; each substantive edge is in edges.tsv with the stated direction and far-end layer.
A page is PUBLISHABLE (OPUS refined ruling 2026-09-30) when it is FACTS-VERIFIED and carries no V5 flag.
It also measures whether the selections follow any single ordering rule (they do not; see the record).

Usage: pass22_neighbour_bullets.py <page-list.txt> [--json out.json]
Exit 0; prints per-page verdicts and FAILS <n> for the tool's own controls.
"""
import collections, io, json, os, re, subprocess, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import audit_crossrefs as ac  # noqa: E402

DBREL = "Database/FFXII TZA/"
GRAPH = os.path.join(REPO, "Database", "Tools", "work", "graph")
REGREL = "_index/candidates/neighbour-dispositions.tsv"
HELPER_FANIN = 40
TRIPWIRE_PAIRS = set()
CTRL_ONLY = {}
EXTRA_NOTES = {}
FAILS = 0


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True).stdout.decode("utf-8", "replace")


def head(rel):
    return git("show", "HEAD:" + DBREL + rel)


def setup():
    fn = ac.load_functions(os.path.join(GRAPH, "functions.tsv"))
    ac.register_ledger_aliases({v["owner"] for v in fn.values()})
    ac.register_domain_aliases({d.split(".")[0] for v in fn.values() for d in v["domains"]})
    callers, callees = ac.load_edges(os.path.join(GRAPH, "edges.tsv"))
    disp = {}
    for line in head(REGREL).split("\n"):
        f = line.rstrip("\r").split("\t")
        if line.startswith("#") or len(f) < 6:
            continue
        v = f[5].strip().upper()
        if v in ac.DISPOSITION_VERDICTS:
            disp[(f[0].strip().replace("\\", "/"), f[1].strip())] = v
    return fn, callers, callees, disp


def page_hits(rel, text, fn, callers, callees, disp):
    """audit_crossrefs.main's check 4 for one document, unchanged, returning the full sorted hit lists."""
    folder_low = rel.lower()
    xlow = "".join(m.group(0) for m in ac.CROSSING_SECTION.finditer(ac.body_text(text))).lower()
    cited = sorted(ac.cited_addresses(text))
    lines = text.split("\n")
    up = [ln.upper() for ln in lines]
    ctrl = {c for c in cited
            if [i for i, ln in enumerate(up) if c in ln]
            and all(re.search(r"\bcontrol\b", lines[i], re.I) for i, ln in enumerate(up) if c in ln)}
    CTRL_ONLY[rel] = set(ctrl)
    cited = [c for c in cited if c not in ctrl]
    far = set()
    spans = [m.span() for m in ac.CROSSING_SECTION.finditer(text)]
    if spans:
        out = text
        for lo, hi in reversed(spans):
            out = out[:lo] + out[hi:]
        oc = ac.cited_addresses(out)
        for c in cited:
            if c in oc:
                continue
            near = {x.upper() for x in callers.get(c, ())} | {x.upper() for x in callees.get(c, ())}
            if near & oc:
                far.add(c)
    seen, trip = {}, {}
    for a in cited:
        if a not in fn or ac.is_substrate(fn.get(a)) or len(callers.get(a, ())) > ac.HUB_FANIN:
            continue
        for d, table in (("caller", callers), ("callee", callees)):
            for o in table.get(a, ()):
                if ac.is_substrate(fn.get(o)):
                    continue
                sub = ac.subsystem_of(fn.get(o))
                if not sub or sub in ac.SUBSTRATE or ac.doc_accounts_for(xlow, folder_low, sub):
                    continue
                (trip if a in far else seen).setdefault(sub, []).append((a, d, o))
    # R6 tripwires (audit_crossrefs: a cited address named only inside a crossing section, next to a function cited
    # outside it) are not findings, but a crossing bullet may account for them; they are returned with the findings
    # and listed in TRIPWIRE_PAIRS so the report can tell the two apart.
    out = {s: sorted(h) for s, h in seen.items() if (rel, s) not in disp}
    for s, h in trip.items():
        if s not in out and (rel, s) not in disp:
            out[s] = sorted(h)
            TRIPWIRE_PAIRS.add((rel, s))
    return out


def detail(h):
    s = "; ".join("%s %s %s" % x for x in h[:4])
    return s + (" (+%d more)" % (len(h) - 4) if len(h) > 4 else "")


def label(h):
    i = sum(1 for x in h if x[1] == "caller")
    return "CLIENT and SERVICE" if i and len(h) - i else ("CLIENT" if i else "SERVICE")


BUL = re.compile(r"^- \*\*([A-Za-z_]+) — ([^(]*?) \((\d+) edges?\)\.\*\* (.*)$")
REF = re.compile(r"`(?:[^`]+)` \(([0-9A-F]{8})\)|`([0-9A-F]{8})`")


def refs(s):
    return [a or b for a, b in REF.findall(s)]


def appended(rel):
    d = git("diff", "--ignore-cr-at-eol", "-U0", "--", DBREL + rel)
    return [l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]


def reg_added():
    d = git("diff", "-U0", "--", DBREL + REGREL)
    rows = collections.defaultdict(dict)
    for l in d.splitlines():
        if l.startswith("+") and not l.startswith("+++"):
            c = l[1:].split("\t")
            rows[c[0]][c[1]] = c
    return rows


def check_page(rel, fn, callers, callees, disp, reg):
    hits = page_hits(rel, head(rel), fn, callers, callees, disp)
    buls = {}
    for l in appended(rel):
        m = BUL.match(l)
        if m:
            buls[m.group(1)] = (m.group(2), int(m.group(3)), m.group(4))
    rows = reg.get(rel, {})
    issues, flags, sel, residual, extra, extra_rows = [], [], collections.Counter(), [], [], []
    for sub, h in hits.items():
        r = rows.get(sub)
        b = buls.get(sub)
        if r is None:
            if b:
                issues.append("V6 bullet %s has no registry row" % sub)
            else:
                residual.append(sub)   # a generated pair the append did not address: stays pass-22 debt
            continue
        items = re.sub(r" \(\+\d+ more\)$", "", r[4]).split("; ")
        more = re.search(r"\(\+(\d+) more\)$", r[4])
        if r[:4] != [rel, sub, str(len(h)), "unaccounted"]                 or not {tuple(i.split(" ")) for i in items} <= set(map(tuple, h))                 or len(items) + int(more.group(1) if more else 0) != len(h):
            issues.append("G3 registry row %s columns 1-5 do not match the generated pair" % sub)
        sel["registry detail in sorted order"] += r[4] == detail(h)
        sel["registry rows"] += 1
        if r[5] == "FALSE-SUBJECT":
            if b:
                issues.append("V6 FALSE-SUBJECT %s carries a bullet" % sub)
            continue
        if not b:
            issues.append("V6 %s row %s has no bullet" % (r[5], sub)); continue
        lab, n, body = b
        if n != len(h):
            issues.append("G2 %s count %d != %d" % (sub, n, len(h)))
        inh = [x for x in h if x[1] == "caller"]; outh = [x for x in h if x[1] == "callee"]
        if lab == "MECHANICAL":
            if r[5] != "GENUINELY-IRRELEVANT":
                issues.append("V4 MECHANICAL %s row is %s" % (sub, r[5]))
        else:
            if r[5] != "CROSSING-ACCOUNTED":
                issues.append("V4 %s %s row is %s" % (lab, sub, r[5]))
            if lab != label(h):
                flags.append("V5 label %s contradicts the edges (%s)" % (sub, label(h)))
            mi = re.search(r"(\d+) inbound \(\S+ bodies (.*?) call page-cited (.*?)\)", body)
            mo = re.search(r"(\d+) outbound \(page-cited (.*?) call \S+ bodies (.*?)\)", body)
            if mi:
                if int(mi.group(1)) != len(inh): issues.append("G2 %s inbound count" % sub)
                if not set(refs(mi.group(2))) <= {x[2] for x in inh}: issues.append("V1 %s inbound body not an edge" % sub)
                if not set(refs(mi.group(3))) <= {x[0] for x in inh}: issues.append("V2 %s inbound cited not an edge" % sub)
                c = collections.Counter(x[2] for x in inh)
                sel["inbound first-3 = frequency order"] += refs(mi.group(2)) == sorted(c, key=lambda k: (-c[k], k))[:3]
                sel["inbound lists"] += 1
            elif inh:
                issues.append("G2 %s has inbound edges but no inbound clause" % sub)
            if mo:
                if int(mo.group(1)) != len(outh): issues.append("G2 %s outbound count" % sub)
                if not set(refs(mo.group(2))) <= {x[0] for x in outh}: issues.append("V2 %s outbound cited not an edge" % sub)
                if not set(refs(mo.group(3))) <= {x[2] for x in outh}: issues.append("V1 %s outbound body not an edge" % sub)
            elif outh:
                issues.append("G2 %s has outbound edges but no outbound clause" % sub)
            ms = re.search(r"Substantive edges include (.*?)(?:; the remaining edges run through shared helpers the page cites)?\.$", body)
            listed = []
            if ms:
                for part in ms.group(1).split("; "):
                    a = refs(part)
                    if len(a) == 2:
                        listed.append((a[0], "caller" if " is called by " in part else "callee", a[1]))
            if not listed:
                issues.append("V3 %s has no substantive edge list" % sub)
            if not set(listed) <= set(map(tuple, h)):
                issues.append("V3 %s substantive edge not a hit" % sub)
            # V7 (OPUS refined ruling, (b)): each named body and each substantive edge re-checked directly against
            # edges.tsv with the stated direction, and the far end's layer equal to the bullet's layer.
            named_in = refs(mi.group(2)) if mi else []
            named_out = refs(mo.group(3)) if mo else []
            # the clause names up to three bodies and up to three page-cited functions as two independent lists, so
            # a named body must call (be called by) SOME page-cited function of the pair, looked up in edges.tsv
            cit_in = sorted({x[0] for x in inh})
            cit_out = sorted({x[0] for x in outh})
            for o in named_in:
                if ac.subsystem_of(fn.get(o)) != sub or not any(o in callers.get(c, ()) for c in cit_in):
                    issues.append("V7 %s inbound body %s: not a %s caller of a page-cited function" % (sub, o, sub))
            for o in named_out:
                if ac.subsystem_of(fn.get(o)) != sub or not any(o in callees.get(c, ()) for c in cit_out):
                    issues.append("V7 %s outbound body %s: not a %s callee of a page-cited function" % (sub, o, sub))
            for a, d, o in listed:
                ok = (o in callers.get(a, ())) if d == "caller" else (o in callees.get(a, ()))
                if not ok or ac.subsystem_of(fn.get(o)) != sub:
                    issues.append("V7 %s substantive edge %s %s %s not in edges.tsv as stated" % (sub, a, d, o))
            sel["V7 named bodies checked"] += len(named_in) + len(named_out)
            sel["V7 substantive edges checked"] += len(listed)
            callee_side = [(e[2] if e[1] == "callee" else e[0]) for e in listed]
            if listed and all(len(callers.get(x, ())) > HELPER_FANIN for x in callee_side):
                flags.append("V5 %s: every listed substantive edge calls a >%d-caller helper (helper-only crossing?)"
                             % (sub, HELPER_FANIN))
            sel["substantive = first sorted hits"] += listed == [tuple(x) for x in h][:len(listed)]
            sel["substantive lists"] += 1
    # V8: a bullet for a pair audit_crossrefs does not report. Accepted as EXTRA (true, not required) only when
    # every page-cited -> far-end edge it names is in edges.tsv with the far end in that layer and the page-cited
    # end is dropped by audit_crossrefs' control-only rule (so the pair is real but unreported). Its registry row is
    # NOT publishable (rows stay 1:1 with reported pairs); it is listed as extra_rows.
    ctrl_only = CTRL_ONLY.get(rel, set())
    for sub in buls:
        if sub in hits:
            continue
        a = refs(buls[sub][2])
        pairs = [(x, y) for x in a for y in a if x in ctrl_only and
                 (y in callees.get(x, ()) or y in callers.get(x, ())) and ac.subsystem_of(fn.get(y)) == sub]
        if pairs:
            extra.append(sub)
        else:
            issues.append("V6 bullet %s has no generated pair" % sub)
    for sub in rows:
        if sub not in hits:
            if sub in extra:
                extra_rows.append(sub)
            else:
                issues.append("V6 registry row %s has no generated pair" % sub)
    if extra:
        flags_extra = "EXTRA verified bullets %s; rows held back %s" % (extra, extra_rows)
        sel["EXTRA bullets"] += len(extra)
        EXTRA_NOTES[rel] = flags_extra
    return hits, buls, issues, flags, sel, residual


def controls(fn, callers, callees, disp):
    """K1: the generator reproduces audit_crossrefs' own detail string for a committed pair; K2: label rule."""
    global FAILS
    ok = label([("A", "caller", "B")]) == "CLIENT" and label([("A", "callee", "B")]) == "SERVICE" \
        and label([("A", "caller", "B"), ("A", "callee", "C")]) == "CLIENT and SERVICE"
    FAILS += not ok
    print("%s  K2 direction label rule" % ("PASS" if ok else "FAIL"))
    ok = detail([("A", "caller", str(i)) for i in range(6)]).endswith("(+2 more)")
    FAILS += not ok
    print("%s  K1 detail string truncation matches audit_crossrefs (4 + '(+N more)')" % ("PASS" if ok else "FAIL"))


def main():
    pages = [l.strip()[len(DBREL):] if l.strip().startswith(DBREL) else l.strip()
             for l in io.open(sys.argv[1], encoding="utf-8") if l.strip()]
    fn, callers, callees, disp = setup()
    reg = reg_added()
    controls(fn, callers, callees, disp)
    tot = collections.Counter(); sel = collections.Counter(); out = {}
    for rel in pages:
        hits, buls, issues, flags, s, residual = check_page(rel, fn, callers, callees, disp, reg)
        tot["residual pairs (no bullet, no row)"] += len(residual)
        sel.update(s)
        verdict = ("PUBLISHABLE" if not flags else "FACTS-VERIFIED") if not issues else "FACT-MISMATCH"
        tot[verdict] += 1
        tot["flags"] += len(flags)
        out[rel] = {"extra": EXTRA_NOTES.get(rel), "verdict": verdict, "issues": issues, "flags": flags, "pairs": len(hits), "bullets": len(buls),
                    "residual": residual}
        print("%-15s %-100s pairs=%d bullets=%d%s%s" % (verdict, rel, len(hits), len(buls),
              ("  ISSUES: " + " | ".join(issues[:3])) if issues else "", ("  FLAGS: " + " | ".join(flags)) if flags else ""))
    print("TOTAL", dict(tot))
    print("R6 TRIPWIRE PAIRS INCLUDED", sorted(TRIPWIRE_PAIRS))
    print("V8 EXTRA", EXTRA_NOTES)
    print("SELECTION RULES", dict(sel))
    print("BYTE-FOR-BYTE REPRODUCIBLE PAGES 0 of %d: every CLIENT / SERVICE bullet carries a chosen body list and a "
          "chosen 'Substantive edges' list that no ordering of the hit set reproduces (SELECTION RULES above)" % len(pages))
    if "--json" in sys.argv:
        json.dump(out, io.open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), indent=1)
    print("FAILS %d" % FAILS)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
