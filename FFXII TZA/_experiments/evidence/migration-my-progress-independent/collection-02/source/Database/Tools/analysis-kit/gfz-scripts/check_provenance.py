#!/usr/bin/env python3
"""Verify every document's provenance stamp against the current certified parent.

Each system document carries a `verified_against:` block naming the GZF parent, the
annotation snapshot and the EXE it was checked against. Those stamps are written by
hand and are never revisited, so they silently fall behind when the parent advances.

This does NOT rewrite stamps. A stamp records which program state a claim was
verified against; rewriting it to the current hash would assert a verification that
never happened. Documents that fail here owe *re-verification*, not an edit.

Usage:  check_provenance.py [--db <path>] [--parent <sha>] [--exe <sha>]

Exit code 1 if any document is stale or missing a stamp.
"""
import argparse
import collections
import io
import os
import re
import sys
import kit_paths as KP  # noqa: E402

DEFAULT_DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")

# The certified parent lives in ONE place: the `$GfzParentSha` line of GfzEnv.ps1, whose own
# header says "UPDATE THIS BLOCK after every certified checkpoint, or every later run works from
# a stale parent and silently re-does closed work."
#
# This checker used to keep its own copy, and on 2026-09-03 that copy was found naming GN158
# while the sealed parent was GN160 -- **two generations stale, in the tool whose entire job is
# detecting stale stamps.** It reported "<-- current parent" against a superseded checkpoint and
# nothing complained, because a hardcoded constant cannot disagree with itself.
#
# So it is read, not duplicated. The fallback constant remains only so the checker still runs
# when the environment file is absent, and it SAYS which source it used -- an unlabelled fallback
# is how the same defect comes back.
GFZ_ENV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "ghidra", "run", "GfzEnv.ps1")
FALLBACK_GZF = "2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9"
CUR_EXE = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"


def certified_parent(path=GFZ_ENV):
    """-> (sha, source) read from GfzEnv.ps1's $GfzParentSha, else the stale fallback."""
    try:
        txt = io.open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return FALLBACK_GZF, "FALLBACK CONSTANT - GfzEnv.ps1 not found"
    m = re.search(r"^\s*\$GfzParentSha\s*=\s*'([0-9a-fA-F]{64})'", txt, re.M)
    if not m:
        return FALLBACK_GZF, "FALLBACK CONSTANT - no $GfzParentSha in GfzEnv.ps1"
    return m.group(1).lower(), "GfzEnv.ps1"


CUR_GZF, CUR_GZF_SRC = certified_parent()


TRANSFER = re.compile(r"^\s+transfers_to:\s*$(?:\s*^\s+\w+:.*$)*?\s*^\s+parent:\s*([0-9a-f]{64})",
                      re.M)


def transfer_parent(t):
    """-> the parent a transferred stamp names, or None.

    `transfers_to` records that a verification HOLDS against a later parent without rewriting the
    `gzf_sha256` it actually ran against. Only the parent it names counts: a transfer to some other
    generation is not a transfer to the certified one.
    """
    m = TRANSFER.search(t[:6000])
    return m.group(1) if m else None


def scan(db):
    docs = []
    for root, _dirs, files in os.walk(db):
        top = os.path.relpath(root, db).split(os.sep)[0]
        if not re.match(r"^\d\d-", top):
            continue
        for f in sorted(files):
            if not f.endswith(".md") or f == "README.md":
                continue
            p = os.path.join(root, f)
            t = io.open(p, encoding="utf-8").read()
            g = re.search(r"gzf_sha256:\s*([0-9a-f]{64})", t)
            e = re.search(r"exe_sha256:\s*([0-9a-f]{64})", t)
            docs.append({
                "rel": os.path.relpath(p, db),
                "gzf": g.group(1) if g else None,
                "exe": e.group(1) if e else None,
                "snapshot": "snapshot_sha256" in t,
                "audit": bool(re.search(r"^audit:", t, re.M)),
                "block": "verified_against:" in t,
                "method": bool(re.search(r"^\s+method:", t[:4000], re.M)),
                # A TRANSFERRED STAMP. The original gzf_sha256 is never rewritten - that would
                # assert a verification nobody performed - but a verification can still HOLD
                # against a later parent, and a document that provably carries is not stale.
                # Adjudicated 2026-09-14, OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0): the
                # witness is the annotation SNAPSHOT, not the function census. Only the parent
                # named here counts; a transfer to some other generation is not a transfer to this
                # one.
                "transfers": transfer_parent(t),
            })
    return docs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--parent", default=CUR_GZF)
    ap.add_argument("--exe", default=CUR_EXE)
    a = ap.parse_args(argv)

    docs = scan(a.db)

    # SECOND SPLIT, 2026-09-14 (OPUS), the same shape as the exe split below and for the same
    # reason. **There are two legitimate provenances and this checker only understood one.**
    #
    #   GZF-derived    gzf_sha256 + snapshot_sha256 + exe_sha256. Goes stale when the parent
    #                  advances - which is what this tool exists to catch.
    #   image-derived  exe_sha256 + `method:`, naming what was disassembled and how. It names no
    #                  parent BECAUSE NO PARENT WAS USED: the evidence is the binary, which
    #                  CLAUDE.md ranks as native semantic authority above any annotation claim.
    #                  **It cannot go stale** - it never referenced the parent and the authority
    #                  EXE hash is fixed.
    #
    # Measured at the split: of 130 documents reported as having no snapshot_sha256, **117 were
    # image-derived and never used a snapshot**; the real snapshot debt is 13. And all 117 carry
    # the authority EXE hash - zero wrong. Telling an image-derived document it owes a gzf stamp
    # asks it to assert a verification against a parent nobody consulted.
    gzf_derived = [d for d in docs if d["gzf"]]
    image_derived = [d for d in docs if not d["gzf"] and d["exe"] and d["block"]]
    noblock = [d for d in docs if not d["block"]]
    thin = [d for d in image_derived if not d["method"]]

    transferred = [d for d in gzf_derived
                   if d["gzf"] != a.parent and d["transfers"] == a.parent]
    stale = [d for d in gzf_derived
             if d["gzf"] != a.parent and d["transfers"] != a.parent]
    # SPLIT 2026-09-14 (OPUS). This was `d["exe"] != a.exe`, which files a document with NO
    # exe_sha256 field under the heading "EXE HASH NOT THE AUTHORIZED BINARY" - that reads as
    # "this document describes a different executable" when it means "this document does not
    # say". Measured at the split: 12 documents were in that bucket, ALL TWELVE with no field at
    # all and ZERO stating a different hash (358 state the authorized one). The two are different
    # defects with different responses. A document resting on another binary is serious and its
    # claims are in doubt; a missing stamp is incomplete provenance, the same class as a missing
    # gzf, and belongs with the re-verification debt rather than above it.
    wrongexe = [d for d in docs if d["exe"] is not None and d["exe"] != a.exe]
    noexe = [d for d in docs if d["exe"] is None]
    # a snapshot is part of GZF-derived provenance; an image-derived document owes none
    nosnap = [d for d in docs if not d["snapshot"] and d not in image_derived]
    noaudit = [d for d in docs if not d["audit"]]

    print(f"documents: {len(docs)}")
    print(f"   {len(gzf_derived):3d}  GZF-derived   (names a parent; CAN go stale)")
    print(f"   {len(image_derived):3d}  image-derived (exe + method; names no parent, CANNOT go "
          f"stale)")
    print(f"   {len(noblock):3d}  no verified_against block at all")
    print(f"   {len(transferred):3d}  stamped to an older parent but TRANSFERRED to the certified "
          f"one\n        (gzf_sha256 untouched; the transfer names its basis and its adjudication)")
    src = CUR_GZF_SRC if a.parent == CUR_GZF else "--parent on the command line"
    print(f"certified parent: {a.parent[:24]}  (from {src})")
    gzf = collections.Counter(d["gzf"] or "MISSING" for d in docs)
    for k, v in gzf.most_common():
        mark = "  <-- current parent" if k == a.parent else ""
        print(f"   {v:3d}  gzf {k[:24]}{mark}")
    if not any(k == a.parent for k in gzf):
        print("   (no document is stamped to the certified parent - the checkpoint has advanced "
              "ahead of\n    every document, which is expected right after a seal and is debt, "
              "not an error)")

    def report(label, items, detail=True):
        print(f"\n{label}: {len(items)}")
        if detail:
            for d in items:
                print(f"   {d['rel']}")

    if wrongexe:
        report("EXE HASH IS A DIFFERENT BINARY - claims on these pages are in doubt", wrongexe)
    if noexe:
        report("NO exe_sha256 stamp (incomplete provenance, NOT a different binary)", noexe)
    if stale:
        report("STALE OR MISSING PARENT STAMP (owe re-verification)", stale)
    if nosnap:
        report("NO snapshot_sha256 (GZF-derived and no-block documents only)", nosnap, detail=False)
    if thin:
        report("IMAGE-DERIVED WITH NO `method:` - thin, not false: it says a document was checked "
               "without saying against what part of the binary or how", thin, detail=False)
    if noaudit:
        report("NO audit block", noaudit, detail=False)

    if not (stale or wrongexe or noexe):
        print("\nprovenance consistent: every document stamped to the current parent")
        return 0
    print("\nThese documents are NOT wrong -- their addresses still resolve (the crossref audit")
    print("checks that against the live graph). What they lack is verification against the")
    print("CURRENT parent. Do not rewrite the stamps; re-verify and then update them.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
