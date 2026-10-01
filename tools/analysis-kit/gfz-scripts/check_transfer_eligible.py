#!/usr/bin/env python3
"""check_transfer_eligible.py - which stale-stamped documents an ADDITIVE advance could have staled.

WHY THIS EXISTS. 242 of 365 documents carry a GZF-derived stamp naming a superseded parent, and
`check_provenance` can only say so: re-verifying each by hand is the stated completion condition of
OPUS-PROVENANCE-REVERIFY-306 and it is 242 readings. But the whole GN158..GN161 lineage is
ADDITIVE, and an additive advance cannot stale most claims. This partitions the 242 into the ones
an additive advance CAN have staled and the ones it cannot, so the hand-reading goes where it can
change an answer.

THE LINEAGE IS ADDITIVE, AND THAT IS MEASURED HERE RATHER THAN ASSERTED. Two independent facts:

  1. `internal` is 38,161 in EVERY generation from GM160 to GN161 (GfzEnv.ps1 $GfzLineage). The
     function SET never changed; only its annotation did.
  2. The residual sets NEST STRICTLY: GN161 (30) is a subset of GN160 (139) is a subset of
     GN158 (158), with ZERO addresses entering the set at any step. This checker re-measures that
     every run and REFUSES to report eligibility if it ever fails, because every ruling below
     depends on it.

  The arithmetic corroborates from a second direction: GN158 -> GN160 resolves 19 addresses, and
  the explicit-name deltas in $GfzLineage are +4 (GN158->GN159) and +15 (GN159->GN160). 4 + 15 = 19.
  GN159's own residual file is not in the tree and is not needed - it is bracketed.

WHAT AN ADDITIVE ADVANCE CAN STILL BREAK, WHICH IS THE POINT OF THE SECOND TEST. "Additive" means
no existing name changed, so a page quoting a function's name is still right. It does NOT mean
nothing can go stale: a page that says an address is UNRESOLVED, UNNAMED or UNOWNED is making a
claim about the residual set, and 128 addresses have left that set since GN158. Those claims are
falsified BY the advance, precisely because it was additive. `99-Unresolved-Residual/` is full of
them by construction. This is the "challenge always/never/only/dead/no callers/complete" rule
applied to the one class of claim an additive delta attacks.

A FLAG IS A QUESTION, NOT A DEFECT - CORRECTED 2026-09-14, SAME DAY, AND THE ORIGINAL WORDING IS
NAMED HERE RATHER THAN QUIETLY REPLACED. The first version of this file printed "a claim the
advance falsified" beside the resolved-citation count. That is stronger than the test can support.
The top-ranked document, `99-Unresolved-Residual/the-unresolved-158.md`, cites 42 resolved
addresses AND already carries a dated `Ledger status, 2026-09-14 (GN161)` block saying the 109 are
no longer unresolved and pointing at `GfzEnv.ps1` for the live count. Its prose was updated; only
its STAMP is behind. A citation of a resolved address means the page's absence claims about that
address need READING - the same standing this corpus gives a `check_index_figures` hit, which
cannot separate a stale figure from a deliberately historical one either.

SO A DOCUMENT IS FLAGGED IF EITHER:
  (a) it quotes decompiler state - `decompiler_tokens.py`, the one canonical pattern. FAS2 witnesses
      FUNCTION annotation only, so a page resting on non-function symbols, the type manager,
      instruction comments, equates or reference overrides is NOT covered by the snapshot identity
      and must be re-read whatever the delta was; or
  (b) it cites an address RESOLVED SINCE ITS OWN STAMP, so any claim it makes about that address
      being nameless or unowned needs reading. Some pages have already been updated in prose and
      are behind only in their stamp; this test cannot tell those apart, and says so.

AND THE CROSS-TAB WITH `transfers_to` IS THE DECISIVE TABLE, not the partition on its own. 123 of
the 242 already carry a completed, adjudicated transfer. *(Those figures were measured when this
file was written; the run that corrected it reads 241 stale-stamped and 145 with a transfer,
2026-09-14. The sentence that stood here - "EVERY ONE of them names GN160 as its target" -
was false by then: the split is 67 GN160 / 78 GN161.)* A superseded target means the transfer
must be RE-POINTED; it does not by itself mean the basis failed. `check_provenance` correctly reports 0 transferred to the CERTIFIED
parent, so from its output alone the work looks undone when it is in fact done and then invalidated
by one further advance. Those blocks carry their own instruction for this: `voided_by: any delta
that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test
at each checkpoint`. This tool re-runs it. Re-adjudicating a voided transfer forward is a much
smaller act than re-verifying a document from nothing, and the two are different work.

AND WHAT CLEARING MEANS, WHICH IS LESS THAN IT SOUNDS. Clearing both tests means the additive
advance gives no REASON to doubt the page. It is not a re-verification and it is not a stamp.
`decompiler_tokens` is explicit that token absence supports a transfer and never proves one. This
tool routes reading effort; the stamp still requires the adjudication behind it.

CONTROLS, every run: the nesting re-measurement above; a document known to quote decompiler state
must flag; and the resolved-address test must find at least one citation somewhere in the corpus,
or the address extractor is not reading what it claims to.
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decompiler_tokens import quotes_decompiler_state  # noqa: E402

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
WORK = os.path.join(REPO, "Database", "Tools", "work")
ENV = os.path.join(REPO, "Database", "Tools", "ghidra", "run", "GfzEnv.ps1")

# Residual sets that exist in the tree, by the generation they belong to. GN159's file was never
# kept; it is bracketed by GN158 and GN160 and a GN159-stamped document is tested against GN158's
# set, which is a SUPERSET - so the test can over-flag a GN159 page and can never clear one it
# should not. Erring toward more hand-reading is the only safe direction here.
RESIDUAL_FILES = {
    "GN158": os.path.join(WORK, "verify", "residual_addrs.txt.GN158"),
    "GN160": os.path.join(WORK, "verify_GFZ_GN160", "residual_addrs.txt"),
    "PARENT": os.path.join(WORK, "verify_GFZ_PARENT", "residual_addrs.txt"),
}
ADDR = re.compile(r"\b(?:0x)?([0-9A-Fa-f]{6,8})\b")
STAMP = re.compile(r"gzf_sha256\s*[:=]?\s*[`\"']?([0-9a-fA-F]{16,64})", re.I)
# A completed transfer names the parent it transferred TO. When that parent is itself superseded
# the transfer's TARGET is stale. Whether the transfer is VOID is a separate question, answered
# by executing the block's own `voided_by` clause - see span_facts / clause_verdict below.
XFER = re.compile(r"transfers_to:\s*\n\s*parent:\s*([0-9a-fA-F]{16,64})")

# AN AGGREGATE CLAIM QUANTIFIES OVER THE FUNCTION SET AND SO CITES NO ADDRESS. Every other test in
# this file is per-address, which means a sentence like "the largest single block in the image -
# 6,768 functions" clears all of them VACUOUSLY while being false. Added 2026-09-14 after the
# transfer basis was applied 64 times without covering this; see EVIDENCE-STANDARD addendum
# 2026-09-14bi for the worked instance (phyre-subsystem-map.md, 6,768 -> 6,769 via 00180A70).
AGGREGATE = re.compile(r"\b(\d[\d,]{2,})\s+(?:functions?|residuals?|unresolved|unowned|"
                       r"unclassified)\b", re.I)
AGG_FLOOR = 100


def load_addrs(path):
    s = set()
    if not os.path.isfile(path):
        return None
    for line in io.open(path, encoding="utf-8", errors="replace"):
        m = re.search(r"([0-9A-Fa-f]{8})", line)
        if m:
            s.add(m.group(1).upper())
    return s


def lineage_tags():
    """-> {gzf_sha_prefix: tag} from GfzEnv.ps1, current parent included."""
    out = {}
    if not os.path.isfile(ENV):
        return out
    txt = io.open(ENV, encoding="utf-8", errors="replace").read()
    m = re.search(r"\$GfzParentGzf\s*=\s*'[^']*?_(G[MN]\d+)_", txt)
    cur = m.group(1) if m else "PARENT"
    m = re.search(r"\$GfzParentSha\s*=\s*'([0-9a-f]{64})'", txt)
    if m:
        out[m.group(1)[:24]] = cur
    for tag, sha in re.findall(r"tag='(G[MN]\d+)'.*?sha='([0-9a-f]{64})'", txt, re.S):
        out[sha[:24]] = tag
    return out


def grown_domain_families():
    """Top-level code-domain families that GAINED members over the span, from the snapshots.

    Derived rather than read from a batch file, so it stays true at any checkpoint: for every
    record whose annotation changed, the tags it GAINED name the domains that grew. A count quoted
    for one of these has a denominator that moved; a count of the whole image does not, because
    `internal` is constant across the lineage.
    """
    try:
        from diff_fas2 import parse as _p
    except ImportError:
        return {}
    a = os.path.join(WORK, "verify", "snapshot.fas2.GN158")
    b = os.path.join(WORK, "verify_GFZ_PARENT", "snapshot.fas2")
    if not (os.path.isfile(a) and os.path.isfile(b)):
        return {}
    _, A = _p(a)
    _, B = _p(b)
    fam = {}
    for e in set(A) & set(B):
        if A[e] == B[e]:
            continue
        gained = {t[0] for t in B[e]["tags"]} - {t[0] for t in A[e]["tags"]}
        for t in gained:
            m = re.search(r"CodeDomain\.([A-Za-z0-9]+)", t)
            if m:
                fam[m.group(1)] = fam.get(m.group(1), 0) + 1
    return fam


# ---------------------------------------------------------------------------------------------
# THE CLAUSE, EXECUTED. Everything below exists so that "the transfer is void" is a measurement
# and not a restatement of "the parent hash differs".
SNAP_BY_TAG = {
    "GN158": os.path.join(WORK, "verify", "snapshot.fas2.GN158"),
    "GN160": os.path.join(WORK, "verify_GFZ_GN160", "snapshot.fas2"),
    # GN161 ADDED 2026-09-21 (OPUS) - see the note in check_delta_additivity.py. Without this
    # tag every one of the 245 GN161-targeted transfers reported UNMEASURED, which reads like a
    # failed basis and is really an unnamed file. The sha256 is certified; see that note.
    "GN161": os.path.join(WORK, "verify_GFZ_PARENT", "snapshot_GN161_0914_STALE.fas2"),
    "PARENT": os.path.join(WORK, "verify_GFZ_PARENT", "snapshot.fas2"),
}

# STRICT 8-HEX, unlike the module-wide ADDR which also takes 6. Zero-filling a 6-hex token invents
# an address in the low image, and an invented address can only manufacture a BROKEN verdict.
ADDR8 = re.compile(r"\b(0[0-9A-Fa-f]{7})\b")
XFER_BLOCK = re.compile(r"transfers_to:\s*\n((?:[ \t]+\w+:.*\n)+)")


def span_facts(from_tag, to_tag="PARENT"):
    """(changed-address set, additive?) across one span, or (None, None) without the snapshots."""
    pa, pb = SNAP_BY_TAG.get(from_tag), SNAP_BY_TAG.get(to_tag)
    if not (pa and pb and os.path.isfile(pa) and os.path.isfile(pb)):
        return None, None
    try:
        from diff_fas2 import parse as _p
        from check_delta_additivity import additivity as _add
    except ImportError:
        return None, None
    _, A = _p(pa)
    _, B = _p(pb)
    changed = {("%08x" % e) for e in (set(A) & set(B)) if A[e] != B[e]}
    return changed, _add(A, B)["additive"]


def clause_verdict(basis, cited, changed, additive):
    """HOLDS / VOID / UNMEASURED for one document, on ITS OWN stated basis."""
    if changed is None:
        return "UNMEASURED", "snapshots for this span are not in the tree"
    b = (basis or "").lower()
    if "additive" in b:
        return (("HOLDS", "delta measured additive on all five dimensions") if additive
                else ("VOID", "delta is NOT additive - the clause fires"))
    if b.startswith("snapshot"):
        hit = sorted(cited & changed)
        return (("VOID", "cites %d changed record(s): %s" % (len(hit), " ".join(hit[:4]))) if hit
                else ("HOLDS", "cites none of the %d changed records" % len(changed)))
    return "UNMEASURED", "basis not recognised: %s" % (basis or "(none)")


def _parent_prefix():
    """The certified parent's sha prefix, so a transfer naming it is not called stale."""
    if not os.path.isfile(ENV):
        return ''
    m = re.search(r"\$GfzParentSha\s*=\s*'([0-9a-f]{64})'",
                  io.open(ENV, encoding='utf-8', errors='replace').read())
    return m.group(1)[:24] if m else ''


def _today():
    """The date, for a generated header. Kept in one place so no row hard-codes one."""
    import datetime
    return datetime.date.today().isoformat()


def stranded_live_claims():
    """What `check_stranded_absence` says today about the reading this file calls owed.

    ADDED 2026-09-14 (OPUS). This file's `cites-resolved` bucket used to end "this cannot tell",
    and another instrument can: check_stranded_absence reads exactly those lines, over the same
    resolved sets - both compute "since GN158: 128, since GN160: 109" - and classifies each.

    Its output is parsed rather than its rule re-implemented, so the two can never disagree. A run
    that does not parse returns None and the caller says so, instead of reporting a borrowed clean
    result. -> (live, total) or None
    """
    try:
        import subprocess
        import sys as _sys
        r = subprocess.run([_sys.executable, os.path.join(KIT, "check_stranded_absence.py"),
                            "--db", DB], capture_output=True, text=True, timeout=600)
    except Exception:
        return None
    txt = r.stdout + r.stderr
    m = re.search(r"LINES CITING A RESOLVED ADDRESS WITH ABSENCE LANGUAGE:\s*(\d+)", txt)
    n = re.search(r"^\s*LIVE CLAIM\s+(\d+)", txt, re.M)
    if not (m and n):
        return None
    return int(n.group(1)), int(m.group(1))


def _clause_control():
    """The clause verdict must fire on a constructed failure and must refuse to guess. -> bool."""
    changed = {"00aaaaaa", "00bbbbbb"}
    cases = [
        ("snapshot-identity - every function this document cites has byte-identical records",
         {"00aaaaaa", "00123456"}, changed, True, "VOID"),
        ("snapshot-identity - every function this document cites has byte-identical records",
         {"00123456"}, changed, True, "HOLDS"),
        ("additive-annotation delta", {"00aaaaaa"}, changed, False, "VOID"),
        ("additive-annotation delta", {"00aaaaaa"}, changed, True, "HOLDS"),
        (None, {"00123456"}, changed, True, "UNMEASURED"),
        ("something nobody has written yet", {"00123456"}, changed, True, "UNMEASURED"),
        ("snapshot-identity - ...", {"00aaaaaa"}, None, None, "UNMEASURED"),
    ]
    ok = True
    for basis, cited, ch, add, want in cases:
        got, _why = clause_verdict(basis, cited, ch, add)
        if got != want:
            print("  CONTROL FAILED: basis=%r expected %s got %s" % (basis, want, got))
            ok = False
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    ap.add_argument("--list", action="store_true", help="print every flagged document")
    ap.add_argument("--transfers", action="store_true",
                    help="emit the per-document clause verdicts as TSV")
    a = ap.parse_args()

    sets = {k: load_addrs(v) for k, v in RESIDUAL_FILES.items()}
    missing = [k for k, v in sets.items() if v is None]
    if missing:
        print("CANNOT RUN: residual set(s) not in the tree: %s" % ", ".join(missing))
        return 2

    print("RESIDUAL SETS")
    for k in ("GN158", "GN160", "PARENT"):
        print("  %-7s %4d addresses" % (k, len(sets[k])))

    # CONTROL 1 - the nesting. Every ruling below rests on it, so it is re-measured, not cited.
    nest_ok = sets["PARENT"] <= sets["GN160"] <= sets["GN158"]
    entered = (sets["GN160"] - sets["GN158"]) | (sets["PARENT"] - sets["GN160"])
    print("\n  strict nesting PARENT <= GN160 <= GN158 : %s" % nest_ok)
    print("  addresses that ENTERED the residual set : %d" % len(entered))
    if not nest_ok or entered:
        print("\n  CONTROL FAILED: the lineage is NOT purely additive in the residual direction.")
        print("  Every eligibility judgement below would be unfounded. Nothing is reported.")
        return 2
    print("  control passed: no address ever entered the set, so the lineage is additive.")

    resolved = {
        "GN158": sets["GN158"] - sets["PARENT"],
        "GN159": sets["GN158"] - sets["PARENT"],   # superset; see RESIDUAL_FILES
        "GN160": sets["GN160"] - sets["PARENT"],
    }
    print("\n  resolved since GN158 : %d   since GN160 : %d"
          % (len(resolved["GN158"]), len(resolved["GN160"])))

    tags = lineage_tags()
    cur_tag = next((v for k, v in tags.items()
                    if k == _parent_prefix()), 'PARENT')
    buckets, cited_any = {}, 0
    cross, xtarget = collections.Counter(), collections.Counter()
    stale_rows, span_cache = [], {}
    agg_docs, agg_invisible, agg_transferred = [], 0, 0
    flagged_tokens, flagged_resolved, clear = [], [], []
    for dirpath, dirs, files in os.walk(a.db):
        # _templates is skipped because a template's stamp is an EXAMPLE, not a claim about a
        # document. Not skipping it found the defect this exclusion now hides: SYSTEM.md shipped
        # GM160's concrete hashes where FORMAT.md had always used `<current checkpoint>`, so every
        # page built from it began stamped four generations back. Fixed 2026-09-14; the exclusion
        # is here so the template cannot be reported as a stale DOCUMENT, which it never was.
        if any(os.sep + d in dirpath for d in ("_index", "_types", "_templates")):
            continue
        for fn in sorted(files):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            p = os.path.join(dirpath, fn)
            txt = io.open(p, encoding="utf-8", errors="replace").read()
            m = STAMP.search(txt)
            if not m:
                continue
            tag = tags.get(m.group(1)[:24].lower())
            if tag is None or tag not in resolved:
                buckets[tag or "unknown"] = buckets.get(tag or "unknown", 0) + 1
                continue
            buckets[tag] = buckets.get(tag, 0) + 1
            rel = os.path.relpath(p, a.db)
            hits = {h.group(1).upper().zfill(8) for h in ADDR.finditer(txt)} & resolved[tag]
            aggs = {int(x.replace(',', '')) for x in AGGREGATE.findall(txt)}
            aggs = {x for x in aggs if x >= AGG_FLOOR}
            xm = XFER.search(txt)
            held = "has-transfer" if xm else "no-transfer"
            if xm:
                xt = tags.get(xm.group(1)[:24].lower(), "?" + xm.group(1)[:8])
                xtarget[xt] += 1
                if xt not in ("PARENT", cur_tag):
                    xb = XFER_BLOCK.search(txt)
                    bm = re.search(r"basis:\s*(.+)", xb.group(1)) if xb else None
                    stale_rows.append((rel, xt, bm.group(1).strip() if bm else None,
                                       {x.lower() for x in ADDR8.findall(txt)}))
            if aggs:
                agg_docs.append((rel, tag, sorted(aggs)[-3:]))
                if not hits:
                    agg_invisible += 1
                    if xm and xm.group(1)[:24].lower() == _parent_prefix():
                        agg_transferred += 1
            if hits:
                cited_any += 1
                flagged_resolved.append((rel, tag, sorted(hits)[:6], len(hits)))
                cross[(held, "cites-resolved")] += 1
            elif quotes_decompiler_state(txt):
                flagged_tokens.append((rel, tag))
                cross[(held, "decompiler")] += 1
            else:
                clear.append((rel, tag))
                cross[(held, "neither")] += 1

    print("\nSTALE-STAMPED DOCUMENTS BY GENERATION")
    for k in sorted(buckets):
        print("  %-9s %4d" % (k, buckets[k]))

    total = len(flagged_resolved) + len(flagged_tokens) + len(clear)
    print("\nPARTITION OF THE %d STALE-STAMPED DOCUMENTS" % total)
    print("  cite an address RESOLVED since their stamp : %4d  <- their absence claims about it"
          % len(flagged_resolved))
    print("                                                     need READING; some are already")
    print("                                                     updated in prose and behind only")
    print("                                                     in their stamp")
    _sa = stranded_live_claims()
    if _sa is None:
        print("     (check_stranded_absence did not run or its output did not parse - the reading")
        print("      below is NOT claimed)")
    else:
        live, total = _sa
        print("     THE READING IS DONE, BY check_stranded_absence, over the same resolved sets:")
        print("     %d line(s) cite a resolved address with absence language, of which LIVE: %d."
              % (total, live))
        if live == 0:
            print("     So no document in this bucket carries an uncorrected absence claim about")
            print("     the address - because no document anywhere does.")
        print("     AND THE CEILING TRAVELS WITH IT. That tool recognises a FIXED absence")
        print("     vocabulary, so a claim phrased outside the list is not seen; it reads only")
        print("     lines carrying BOTH a resolved address and absence language; and it is a live")
        print("     reading, not a stamp - it says nothing about which parent a document was")
        print("     verified against, which is what the transfer is for.")
    print("  quote decompiler state (no resolved cite)  : %4d  <- outside what FAS2 witnesses"
          % len(flagged_tokens))
    print("  neither                                    : %4d  <- additive advance gives no"
          % len(clear))
    print("                                                     reason to doubt them; NOT a")
    print("                                                     re-verification and NOT a stamp")

    # THE DECISIVE TABLE. A document that already carries a transfer is not in the same position
    # as one that never had one: its basis and adjudication are written down and only its TARGET
    # has been superseded. Collapsing the two into "242 owe re-verification" overstates the work
    # by the size of the has-transfer row.
    print("\nCROSS-TAB WITH `transfers_to`")
    print("  %-14s %14s %11s %8s   total" % ("", "cites-resolved", "decompiler", "neither"))
    for h in ("has-transfer", "no-transfer"):
        r = [cross[(h, b)] for b in ("cites-resolved", "decompiler", "neither")]
        print("  %-14s %14d %11d %8d   %5d" % (h, r[0], r[1], r[2], sum(r)))
    if xtarget:
        print("  transfers point at: %s"
              % ", ".join("%s x%d" % (k, v) for k, v in sorted(xtarget.items())))
        stale_x = sum(v for k, v in xtarget.items() if k not in ("PARENT", cur_tag))
        if stale_x:
            print("  %d name a SUPERSEDED parent, so their TARGET is stale. Whether the TRANSFER"
                  % stale_x)
            print("  is void is a different question, and the clause says how to answer it:")
            print("  `voided_by: any delta that REMOVES or REWRITES ... - re-run the additivity")
            print("  test at each checkpoint`. That is a condition on the DELTA, not on elapsed")
            print("  checkpoints. Executed below rather than assumed.")
            verd = collections.Counter()
            owing = []
            for rel_x, tag_x, basis_x, cited_x in stale_rows:
                if tag_x not in span_cache:
                    span_cache[tag_x] = span_facts(tag_x)
                changed_x, add_x = span_cache[tag_x]
                v, why = clause_verdict(basis_x, cited_x, changed_x, add_x)
                verd[(tag_x, (basis_x or "?").split(" - ")[0][:24], v)] += 1
                if v != "HOLDS":
                    owing.append((rel_x, basis_x, why))
            print()
            for (tg, bs, v), n in sorted(verd.items()):
                print("     %-8s %-26s %-10s %3d" % (tg, bs, v, n))
            holds = sum(n for (_t, _b, v), n in verd.items() if v == "HOLDS")
            print("")
            print("     RE-POINT ONLY (basis measured intact) : %d" % holds)
            print("     GENUINELY OWE RE-ADJUDICATION         : %d" % (stale_x - holds))
            for rel_x, basis_x, why in owing:
                print("        %-58s %s" % (rel_x.replace(os.sep, "/")[:58], why))
            print("")
            print("     A re-pointed target is a much smaller act than a re-verification, and")
            print("     collapsing the two overstates the work by the size of the first number.")
            print("     NEITHER IS A STAMP: this routes reading effort; writing the stamp still")
            print("     needs the adjudication behind it, and at this size an independent review.")
            if a.transfers:
                print("")
                print("# The `voided_by` clause executed per document, %s."
                      % _today())
                print("# Regenerate: check_transfer_eligible.py --db <db> --transfers")
                print("# A HOLDS row is not a stamp. It says the basis this document already")
                print("# carries was re-tested and survived the advance, so what it owes is a")
                print("# re-pointed target rather than a fresh verification.")
                print("#")
                print("# document\ttarget\tbasis\tverdict\treason")
                for rel_x, tag_x, basis_x, cited_x in sorted(stale_rows):
                    changed_x, add_x = span_cache[tag_x]
                    v, why = clause_verdict(basis_x, cited_x, changed_x, add_x)
                    print("\t".join([rel_x.replace(os.sep, "/"), tag_x,
                                     (basis_x or "(none)").split(" - ")[0], v, why]))

    # THE DIMENSION NO ADDRESS TEST CAN SEE. Everything above is per-address; a claim that
    # quantifies over the function SET cites none, so it clears all of them vacuously. This is not
    # a fourth bucket - a document can both cite a resolved address and make an aggregate claim -
    # so it is reported alongside, never folded into, the partition.
    print("\nAGGREGATE CLAIMS - orthogonal to the partition above, invisible to every address test")
    print("  make a claim of %d+ functions/residuals      : %4d" % (AGG_FLOOR, len(agg_docs)))
    print("  of those, citing NO resolved address         : %4d  <- cleared VACUOUSLY by every"
          % agg_invisible)
    print("                                                       per-address test in this file")
    print("  of those, already transferred to the parent  : %4d  <- their basis quantifies over"
          % agg_transferred)
    print("                                                       CITED functions and never")
    print("                                                       covered this; the transfers")
    print("                                                       stand, the basis is silent")
    fam = grown_domain_families()
    if fam:
        print("  code-domain families that GREW over the span (a count quoted for one of these has")
        print("  a denominator that moved; a count of the whole image does not, `internal` is fixed):")
        print("    " + ", ".join("%s +%d" % (k, v) for k, v in
                                 sorted(fam.items(), key=lambda x: -x[1])))

    # CONTROL 2 - the address extractor must actually find resolved citations somewhere.
    if cited_any == 0:
        print("\n  CONTROL FAILED: not one document cites any address resolved since its stamp,")
        print("  across %d documents. The extractor is not reading what it claims to." % total)
        return 2
    if not _clause_control():
        print("\n  THE CLAUSE VERDICT'S CONTROL DID NOT FIRE - every HOLDS above is unsupported.")
        return 2
    print("  control passed: the clause verdict calls a changed-record citation VOID, calls a")
    print("  non-additive delta VOID, and refuses to answer at all when the basis is unrecognised")
    print("  or the snapshots are missing - it never reports HOLDS from an absent measurement.")

    print("\n  control passed: %d document(s) cite a resolved address." % cited_any)

    if a.list:
        print("\nCITE A RESOLVED ADDRESS - read these first; the claim may be the stale part")
        for rel, tag, ex, n in sorted(flagged_resolved, key=lambda r: -r[3]):
            print("  %-4s %-72s %d addr  %s" % (tag, rel, n, " ".join(ex)))
        print("\nQUOTE DECOMPILER STATE")
        for rel, tag in sorted(flagged_tokens):
            print("  %-4s %s" % (tag, rel))
    return 1 if (flagged_resolved or flagged_tokens) else 0


if __name__ == "__main__":
    sys.exit(main())
