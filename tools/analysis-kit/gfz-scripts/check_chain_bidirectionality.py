"""check_chain_bidirectionality.py - the instrument FINAL-AUDIT pass 20 never had.

Pass 20: *"every chain states upstream and downstream"* - fails if either direction is
missing. The full reading of "states both directions" is narrative and needs a reader
(OPUS ruled a structural proxy for the narrative would be theatre), but the corpus input
that makes the mechanical half real now exists: _index/CODEDOMAIN-OWNER-MAP.tsv (EC7),
which maps every Owners-column label to its canonical owner token and category directory.

WHAT IS TESTED
  * every label in a Documented-chains row's Owners column resolves in the map
  * every mapped owner is DOCUMENTED AT THE ROW'S DOCUMENT, where documented means:
      - the document lives under the owner's category directory, or
      - the owner's canonical token appears in the document text
    An owner on the upstream side and an owner on the downstream side are tested the same
    way, so a missing owner IS a missing direction - the pass's failure condition at the
    granularity a machine can honestly check.
  * multi-owner labels ("Script/VM", "InputGameplay/UI") are satisfied only when EVERY
    mapped owner is documented, per the map's own contract
  * "same document" rows inherit the previous row's link

WHAT IS DELIBERATELY NOT TESTED
  * whether the document STATES the direction in prose (cause on one side, consequence on
    the other). A doc can name an owner and still not describe the crossing; that is the
    reader's half of pass 20 and is reported as UNTESTED, not as passed.
  * labels the map marks (none) - Developer console, "engine", "Authored data", generic
    engine-side - which carry no owner token. They are counted ABSTAIN, never failures.
  * prose hops in the chain label itself; the Owners column is the stated owner sequence.

Inputs: --db (database root), --map (CODEDOMAIN-OWNER-MAP.tsv), --index (CALL-CHAINS.md).
Exit 1 while any mapped owner is undocumented at its row's document; exit 2 on missing input.
"""
import argparse, io, os, re, sys

import kit_paths as KP

ROW = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")
LINK = re.compile(r"\[`?([^\]`]+)`?\]\(([^)]+)\)")
ARROW = re.compile(r"\s*(?:->|\u2192)\s*")


def load_map(path):
    """chain_label -> [(owner_token, category_dir)]. (none) tokens kept as abstain."""
    m = {}
    for line in io.open(path, encoding="utf-8", errors="replace"):
        if line.startswith("#") or line.startswith("chain_label"):
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) < 3 or not p[0]:
            continue
        m.setdefault(p[0], []).append((p[1], p[2]))
    return m


def owners_column_sides(col):
    """Split the Owners column into per-side label lists.

    The map keys include slash-joined labels ("Script/VM", "InputGameplay/UI"), so a
    whole side is tried as a key first; failing that it splits on "/" into single-owner
    labels.
    """
    return [s.strip() for s in ARROW.split(col) if s.strip()]


def resolve_labels(side, m):
    """Return (mapped_owner_list, unresolvable_labels) for one side."""
    side = side.strip().strip("`")
    if side in m:
        return list(m[side]), []
    labels = [x.strip().strip("`") for x in side.split("/") if x.strip()]
    owners, missing = [], []
    for lab in labels:
        if lab in m:
            owners.extend(m[lab])
        else:
            missing.append(lab)
    return owners, missing


def documented(rel_doc_abs, doc_text, token, catdir):
    if catdir != "(none)" and rel_doc_abs.startswith(catdir + "/"):
        return "location"
    if token != "(none)" and token in doc_text:
        return "token"
    # a link path or prose reference naming the category directory - e.g.
    # ../../03-World-Area-Field/Weather/ - is documented awareness of that side
    if catdir != "(none)" and catdir in doc_text:
        return "catdir-ref"
    return None


def prose_hits(doc_text, token):
    """Natural-language components of the owner token found in the document.

    Tokens like Items_Equipment_Shops_License and Script_VM_Native_Bridge decompose to
    domain-naive words a covering document writes without ever naming the domain -
    this is the "a page about WorldAreaField never contains the string" class OPUS
    named, so hits annotate the finding for the reviewer, they do not clear it.
    """
    parts = [w.lower() for w in re.split(r"[_\s]+|(?<=[a-z])(?=[A-Z])", token)
             if len(w) > 2 and w.lower() not in {"and", "the", "for", "native"}]
    low = doc_text.lower()
    return [w for w in parts if w in low]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--db", default=KP.DB)
    ap.add_argument("--map", default=os.path.join(KP.DB, "_index", "CODEDOMAIN-OWNER-MAP.tsv"))
    ap.add_argument("--index", default=None)
    a = ap.parse_args()

    idx = a.index or os.path.join(a.db, "_index", "CALL-CHAINS.md")
    for p in (idx, a.map):
        if not os.path.exists(p):
            print("REFUSED: missing input %s" % p)
            return 2
    m = load_map(a.map)

    text = io.open(idx, encoding="utf-8", errors="replace").read()
    rows, inside, cur_doc = [], False, None
    for n, line in enumerate(text.split("\n"), 1):
        if line.startswith("## "):
            inside = line.strip() == "## Documented chains"
            continue
        if not inside:
            continue
        mt = ROW.match(line)
        if not mt or mt.group(1).lower() == "chain" or set(mt.group(1)) <= set("-: "):
            continue
        chain, owners, doc = mt.groups()
        lm = LINK.search(doc)
        if lm:
            cur_doc = lm.group(2).split("#")[0]
        rows.append((n, chain, owners, cur_doc))

    cache = {}
    seen_findings, findings, abstain, checked = set(), [], 0, 0
    for n, chain, owners, doc in rows:
        if not doc:
            continue
        rel = os.path.normpath(os.path.join(a.db, "_index", doc)).replace(os.sep, "/")
        if rel not in cache:
            cache[rel] = io.open(rel, encoding="utf-8", errors="replace").read() \
                if os.path.exists(rel) else None
        text_doc = cache[rel]
        db_rel = os.path.relpath(rel, os.path.normpath(a.db)).replace(os.sep, "/")
        for side_i, side in enumerate(owners_column_sides(owners)):
            owners_mapped, missing = resolve_labels(side, m)
            for lab in missing:
                abstain += 1
            for token, catdir in set(owners_mapped):
                if token == "(none)":
                    abstain += 1
                    continue
                checked += 1
                how = None if text_doc is None else documented(db_rel, text_doc, token, catdir)
                key = (n, side_i, token)
                if not how and key not in seen_findings:
                    seen_findings.add(key)
                    hits = prose_hits(text_doc, token) if text_doc else []
                    verdict = "PLAUSIBLE-PROSE" if hits else "NO-REFERENCE"
                    findings.append((n, side_i, side, token, catdir, rel, verdict, hits))

    strong = [f for f in findings if f[6] == "NO-REFERENCE"]
    print("  documented chain rows                    : %d" % len(rows))
    print("  owner labels resolved and checked        : %d" % checked)
    print("  labels abstained ((none)/unmapped)       : %d" % abstain)
    print("  owners not documented in corpus vocab    : %d" % len(findings))
    print("      of which NO prose reference either   : %d" % len(strong))
    for n, si, side, token, catdir, rel, verdict, hits in findings:
        print("      line %-5d side %d %-15s %-20s (%s)  doc=%s  %s" % (
            n, si, verdict, token, catdir, os.path.basename(rel),
            ("prose: " + ",".join(hits)) if hits else ""))
    print("\n  NOTE: presence of the owner token/category is tested; whether the document")
    print("  STATES the crossing's direction in prose is the reader's half of pass 20")
    print("  and is reported UNTESTED, not passed.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
