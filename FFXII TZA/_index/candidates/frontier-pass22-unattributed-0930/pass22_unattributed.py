"""pass22_unattributed.py - SWE2-FRONTIER for FABLE, 2026-09-30.

Disposition verifier for the unattributed pass-22 "Cross-subsystem neighbours" appends
(OPUS-NOTICE-FABLE-PASS22-UNATTRIBUTED-BLOCKS-0930). It extends SWE2-CONTRACT's
`pass22_neighbour_bullets.py` (copied unchanged beside this file, blob 27b78a9694b2 = HEAD's copy in
swe2contract-pass22-bullets-0930/) to the second bullet style in the tree, the template bullets:

  - **<Layer> - CLIENT|SERVICE|CLIENT and SERVICE (<n> edge[s]).** <cited> is/are called by bodies filed to
    <Layer>: <bodies>; <cited> reach(es) bodies filed to <Layer>: <bodies> - shared machinery across the layer
    boundary, no shared ownership.
  - **<Layer> - MECHANICAL (<n> edge[s]).** Fan-in on the shared accessor <A>[, <B>]. | Shared-helper fan-in on <A>.
    All <n> edges run through it - one accessor's spread, not a per-caller relationship.

Inputs (read-only): the page's HEAD text and its uncommitted diff; HEAD neighbour-dispositions.tsv; the graph
`Database/Tools/work/graph/functions.tsv` + `edges.tsv` through audit_crossrefs' own functions (CONTRACT's
`page_hits`, which is audit_crossrefs check 4 for one page).

Per page, OPUS's refined ruling (2026-09-30; swe2contract-pass22-bullets-0930/README.md):
  (a) FACTS-VERIFIED and (b) every named body / edge in edges.tsv with the stated direction and far-end layer:
      T1  every template bullet maps to a pair audit_crossrefs reports on the HEAD text with the HEAD registry
          (a bullet for a pair already accounted at HEAD, or for no pair, is a mismatch);
      T2  the edge count equals the pair's hit count; the label equals the direction label (inbound only CLIENT,
          outbound only SERVICE, both CLIENT and SERVICE) unless MECHANICAL;
      T3  CLIENT/SERVICE text is regenerated from the hit set (sorted unique page-cited ends and far bodies per
          direction, first four rendered `Name (`ADDR`)` or `` `ADDR` ``, then `(+N more)`) and compared BYTE FOR
          BYTE, from the audit enumeration or the page-cited enumeration of the HEAD text (ENUMERATIONS below);
          a bullet neither reproduces is reported with both strings;
      T4  MECHANICAL: in one of the two enumerations every edge of the pair has a named accessor as one of its
          two ends, and both stated counts equal its size;
  (c) no helper-only relationship dressed as CLIENT/SERVICE:
      T5  a CLIENT/SERVICE bullet whose every edge's callee end has more than HELPER_FANIN (40) callers is
          flagged (CONTRACT's V5 applied to the whole hit set, since template bullets name no substantive list);
  (d) no other party's edits, and the append adds nothing:
      T6  every added line is a template bullet, a blank line or the heading
          `## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)`; every removed line is blank;
      T7  the pairs audit_crossrefs reports on the WORKING text are a subset of the HEAD pairs (no new pair), and
          every bulleted pair is gone from them (the bullet does account for it).
Pages with CONTRACT-style (em-dash) bullets are passed to CONTRACT's own check_page unchanged, plus T6.

A page is PUBLISHABLE when T1-T7 hold with no flag; MIXED when only T6 fails; otherwise NOT-PUBLISHABLE.
Controls (FAILS counts them): K1/K2 from CONTRACT's script; K3 the generator reproduces a bullet it is handed
from a synthetic hit set; K4 a mutated copy of a real bullet (count +1, one body swapped, one address dropped)
is refused by T2/T3 on the real pair - the verifier is sensitive to the defect it is there to catch.

Usage: pass22_unattributed.py <page-list.txt> [--json out.json]
"""
import collections, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pass22_neighbour_bullets as cb  # noqa: E402  (SWE2-CONTRACT's verifier, copied unchanged)

ac = cb.ac
HELPER_FANIN = cb.HELPER_FANIN
HEADING = "## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)"
TBUL = re.compile(r"^- \*\*([A-Za-z_]+) - (CLIENT and SERVICE|CLIENT|SERVICE|MECHANICAL) \((\d+) edges?\)\.\*\* (.*)$")
TRAIL = " - shared machinery across the layer boundary, no shared ownership."
MECH = re.compile(r"^(?:Fan-in on the shared accessor|Shared-helper fan-in on) (.*?)\. All (\d+) edges run through it"
                  r" - one accessor’s spread, not a per-caller relationship\.$")
FAILS = 0


def render(fn, a):
    n = (fn.get(a) or {}).get("name") or ""
    if not n or n.upper().startswith("FUN_") or n.upper() == "FUN_" + a:
        return "`%s`" % a
    return "%s (`%s`)" % (n, a)


def lst(fn, xs):
    xs = sorted(set(xs))
    s = ", ".join(render(fn, x) for x in xs[:4])
    return s + (" (+%d more)" % (len(xs) - 4) if len(xs) > 4 else "")


def gen_body(fn, sub, h):
    inh = [x for x in h if x[1] == "caller"]
    outh = [x for x in h if x[1] == "callee"]
    parts = []
    if inh:
        c = {x[0] for x in inh}
        parts.append("%s %s called by bodies filed to %s: %s" % (lst(fn, c), "is" if len(c) == 1 else "are", sub,
                                                                  lst(fn, [x[2] for x in inh])))
    if outh:
        c = {x[0] for x in outh}
        parts.append("%s %s bodies filed to %s: %s" % (lst(fn, c), "reaches" if len(c) == 1 else "reach", sub,
                                                        lst(fn, [x[2] for x in outh])))
    return "; ".join(parts) + TRAIL


def gen_line(fn, sub, h):
    n = len(h)
    return "- **%s - %s (%d edge%s).** %s" % (sub, cb.label(h), n, "" if n == 1 else "s", gen_body(fn, sub, h))


# ENUMERATIONS. A template bullet's edge set is checked against two enumerations of the page's HEAD text:
#   audit       audit_crossrefs check 4 exactly (CONTRACT's page_hits): control-only citations and R6 far ends
#               (a function named only inside a crossing section, adjacent to one cited outside it) are dropped;
#   page-cited  every address the HEAD text cites, with the same substrate and hub (HUB_FANIN) filters, nothing
#               dropped. The writer's applier enumerated this way on 38 of the bullets (probe in the README).
# Both are sets of real edges.tsv edges between a function the page cites and a body filed to the layer, so a
# bullet reproduced byte for byte from either states only true edges; T1 still requires the pair to be one
# audit_crossrefs reports (the audit enumeration), so the bullet accounts for a real finding.
def inclusive_hits(text, fn, callers, callees):
    out = {}
    for a in sorted(ac.cited_addresses(text)):
        if a not in fn or ac.is_substrate(fn.get(a)) or len(callers.get(a, ())) > ac.HUB_FANIN:
            continue
        for d, table in (("caller", callers), ("callee", callees)):
            for o in table.get(a, ()):
                if ac.is_substrate(fn.get(o)):
                    continue
                sub = ac.subsystem_of(fn.get(o))
                if sub and sub not in ac.SUBSTRATE:
                    out.setdefault(sub, []).append((a, d, o))
    return {s: sorted(h) for s, h in out.items()}


def diff_lines(rel):
    d = cb.git("diff", "--ignore-cr-at-eol", "-U0", "--", cb.DBREL + rel)
    add, rem = [], []
    for l in d.splitlines():
        if l.startswith("+++") or l.startswith("---"):
            continue
        if l.startswith("+"):
            add.append(l[1:])
        elif l.startswith("-"):
            rem.append(l[1:])
    return add, rem


def worktree_text(rel):
    with io.open(os.path.join(cb.REPO, cb.DBREL + rel), encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


def check_template(rel, fn, callers, callees, disp):
    head_hits = cb.page_hits(rel, cb.head(rel), fn, callers, callees, disp)
    add, rem = diff_lines(rel)
    issues, flags, other = [], [], []
    buls = {}
    for l in add:
        m = TBUL.match(l)
        if m:
            if m.group(1) in buls:
                issues.append("T1 two bullets for %s" % m.group(1))
            buls[m.group(1)] = (m.group(2), int(m.group(3)), m.group(4), l)
        elif l.strip() == "" or l.strip() == HEADING:
            continue
        else:
            other.append("+" + l)
    other += ["-" + l for l in rem if l.strip() != ""]
    regen = 0
    enum_used = collections.Counter()
    incl = inclusive_hits(cb.head(rel), fn, callers, callees)
    for sub, (lab, n, body, line) in sorted(buls.items()):
        h = head_hits.get(sub)
        if h is None:
            issues.append("T1 bullet %s has no pair at HEAD (accounted already, or never reported)" % sub)
            continue
        # The bullet's edge set may be either enumeration of the HEAD text (see ENUMERATIONS); every edge in
        # either is an edges.tsv edge between a function the HEAD text cites and a body filed to the layer.
        cands = [("audit", h)] + ([("page-cited", incl[sub])] if incl.get(sub) and incl[sub] != h else [])
        if lab == "MECHANICAL":
            mm = MECH.match(body)
            if not mm:
                issues.append("T4 %s MECHANICAL text does not parse" % sub)
                continue
            acc = set(cb.refs(mm.group(1)))
            ok = [k for k, s in cands if n == len(s) and int(mm.group(2)) == len(s) and acc
                  and not [x for x in s if x[0] not in acc and x[2] not in acc]]
            if ok:
                enum_used[ok[0]] += 1
            else:
                s = h
                miss = [x for x in s if x[0] not in acc and x[2] not in acc]
                issues.append("T4 %s MECHANICAL (%d edges, accessors %s): no enumeration matches (audit %d edges, "
                              "%d not through the accessors; page-cited %d)"
                              % (sub, n, sorted(acc), len(s), len(miss), len(incl.get(sub, []))))
        else:
            ok = [(k, s) for k, s in cands if gen_line(fn, sub, s) == line]
            if ok:
                regen += 1
                k, s = ok[0]
                enum_used[k] += 1
                callee_end = [x[0] if x[1] == "caller" else x[2] for x in s]
                if all(len(callers.get(c, ())) > HELPER_FANIN for c in callee_end):
                    flags.append("T5 %s: every edge calls a >%d-caller helper (helper-only, would be MECHANICAL)"
                                 % (sub, HELPER_FANIN))
            else:
                if n != len(h):
                    issues.append("T2 %s count %d != audit %d (page-cited %d)" % (sub, n, len(h), len(incl.get(sub, []))))
                if lab != cb.label(h):
                    issues.append("T2 %s label %s != direction label %s" % (sub, lab, cb.label(h)))
                issues.append("T3 %s text matches neither enumeration: HAVE %r WANT(audit) %r"
                              % (sub, line, gen_line(fn, sub, h)))
    if other:
        issues.append("T6 %d added/removed line(s) are not template bullets: %s" % (len(other), other[:2]))
    # T7 counts FINDINGS only: page_hits also returns R6 tripwire-only pairs (a function named only inside a
    # crossing section, adjacent to one cited outside it), which audit_crossrefs does not report; it records
    # them in TRIPWIRE_PAIRS, cleared here so the working-text call can be told apart.
    cb.TRIPWIRE_PAIRS.clear()
    wt_all = cb.page_hits(rel, worktree_text(rel), fn, callers, callees, disp)
    wt_hits = {s: h for s, h in wt_all.items() if (rel, s) not in cb.TRIPWIRE_PAIRS}
    new = sorted(set(wt_hits) - set(head_hits))
    if new:
        issues.append("T7 the append ADDS pairs %s" % new)
    stay = sorted(s for s in buls if s in wt_hits)
    if stay:
        issues.append("T7 bulleted pairs still reported on the working text %s" % stay)
    t6_only = other and all(i.startswith("T6") for i in issues)
    verdict = ("PUBLISHABLE" if not flags else "FLAGGED") if not issues else ("MIXED" if t6_only else "NOT-PUBLISHABLE")
    return {"verdict": verdict, "style": "template", "issues": issues, "flags": flags, "bullets": len(buls),
            "regenerated_byte_exact": regen, "enumeration": dict(enum_used), "head_pairs": len(head_hits),
            "accounted_by_append": sorted(s for s in buls if s in head_hits and s not in wt_hits),
            "residual": sorted(s for s in head_hits if s not in buls), "other_lines": other}


def controls(fn, callers, callees, disp):
    global FAILS
    cb.controls(fn, callers, callees, disp)
    FAILS += cb.FAILS
    h = [("00000010", "caller", "00000020"), ("00000010", "caller", "00000030"), ("00000011", "callee", "00000040")]
    want = ("- **X - CLIENT and SERVICE (3 edges).** `00000010` is called by bodies filed to X: `00000020`, `00000030`;"
            " `00000011` reaches bodies filed to X: `00000040`" + TRAIL)
    ok = gen_line({}, "X", h) == want
    FAILS += not ok
    print("%s  K3 generator renders a synthetic hit set exactly" % ("PASS" if ok else "FAIL"))


def sensitivity(rel, fn, callers, callees, disp):
    """K4 on one real page: mutate a verified bullet three ways; each mutation must be refused."""
    global FAILS
    hits = cb.page_hits(rel, cb.head(rel), fn, callers, callees, disp)
    add, _ = diff_lines(rel)
    for l in add:
        m = TBUL.match(l)
        if not m or m.group(2) == "MECHANICAL" or m.group(1) not in hits or gen_line(fn, m.group(1), hits[m.group(1)]) != l:
            continue
        sub, h = m.group(1), hits[m.group(1)]
        muts = {"count+1": l.replace("(%d edge" % len(h), "(%d edge" % (len(h) + 1), 1)}
        a = cb.refs(l)
        muts["address dropped"] = l.replace("`%s`, " % a[0], "", 1) if "`%s`, " % a[0] in l else l.replace(a[0], "00000000", 1)
        muts["body swapped"] = l.replace(a[-1], "00121000", 1)
        for k, v in muts.items():
            refused = v != l and (gen_line(fn, sub, h) != v)
            FAILS += not refused
            print("%s  K4 %s on %s / %s is refused" % ("PASS" if refused else "FAIL", k, rel, sub))
        return
    FAILS += 1
    print("FAIL  K4 no byte-exact bullet found on %s to mutate" % rel)


def main():
    pages = [l.strip()[len(cb.DBREL):] if l.strip().startswith(cb.DBREL) else l.strip()
             for l in io.open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
    fn, callers, callees, disp = cb.setup()
    controls(fn, callers, callees, disp)
    out, tot = {}, collections.Counter()
    reg = cb.reg_added()
    for rel in pages:
        add, _ = diff_lines(rel)
        if any(TBUL.match(l) for l in add):
            r = check_template(rel, fn, callers, callees, disp)
        else:
            hits, buls, issues, flags, s, residual = cb.check_page(rel, fn, callers, callees, disp, reg)
            # (d) for CONTRACT-style pages: every added line a CONTRACT bullet, a blank line or a crossing heading
            add, rem = diff_lines(rel)
            other = ["+" + l for l in add if not (cb.BUL.match(l) or l.strip() == ""
                                                   or l.startswith("## Cross-subsystem neighbours"))]
            other += ["-" + l for l in rem if l.strip() != ""]
            if other:
                issues = issues + ["T6 %d added/removed line(s) are not pass-22 bullets: %s" % (len(other), other[:2])]
            t6_only = other and all(i.startswith("T6") for i in issues)
            v = ("PUBLISHABLE" if not flags else "FLAGGED") if not issues else ("MIXED" if t6_only else "NOT-PUBLISHABLE")
            r = {"verdict": v, "style": "contract", "issues": issues, "flags": flags, "bullets": len(buls),
                 "head_pairs": len(hits), "residual": residual, "other_lines": other}
        out[rel] = r
        tot[r["verdict"]] += 1
        tot["bullets"] += r["bullets"]
        tot["byte-exact CLIENT/SERVICE bullets"] += r.get("regenerated_byte_exact", 0)
        tot["pairs accounted by publishable appends"] += len(r.get("accounted_by_append", [])) if r["verdict"] == "PUBLISHABLE" else 0
        print("%-15s %-3d %s%s%s" % (r["verdict"], r["bullets"], rel,
                                     ("\n    ISSUES: " + "\n    ".join(r["issues"])) if r["issues"] else "",
                                     ("\n    FLAGS: " + "\n    ".join(r["flags"])) if r["flags"] else ""))
    ctl = next((p for p in pages if out[p]["verdict"] == "PUBLISHABLE" and out[p].get("regenerated_byte_exact")), None)
    if ctl:
        sensitivity(ctl, fn, callers, callees, disp)
    else:
        global FAILS
        FAILS += 1
        print("FAIL  K4 no publishable page to run the sensitivity control on")
    print("TOTAL", dict(tot))
    if "--json" in sys.argv:
        json.dump(out, io.open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), indent=1)
    print("FAILS %d" % FAILS)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
