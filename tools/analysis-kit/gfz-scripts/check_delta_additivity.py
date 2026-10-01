#!/usr/bin/env python3
"""check_delta_additivity.py - the `voided_by` clause of a transfer block, made executable.

WHY THIS EXISTS. 123 documents carry a `transfers_to` block whose basis is the ADDITIVE-ANNOTATION
DELTA, and every one of them carries this instruction:

    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range
               - re-run the additivity test at each checkpoint

An instruction to re-run a test, written in prose, in 123 places, is a test nobody runs. Worse, the
prose names FIVE dimensions and the obvious cheap check - "did the function count change?" - covers
none of them. This runs all five against the FAS2 snapshots and answers the one question the clause
asks: is the transfer still good, or is it void?

WHAT THE FIVE DIMENSIONS ARE, AND WHY A COUNT CANNOT SEE THEM. `GFZFunctionAnnotationSnapshotV2`
records name, namespace, name_source, comment, repeatable_comment, prototype, signature_source,
calling_convention, inline, noreturn, varargs, is_thunk, thunk_target, body_ranges and tags per
function. A rename plus an addition leaves every count identical, so counts are not evidence here.
The test is per-record and per-field:

  1. functions ADDED or REMOVED          must be 0/0
  2. IMMUTABLE fields changed            must be 0 - name, namespace, name_source,
                                         repeatable_comment, prototype, signature_source,
                                         calling_convention, inline, noreturn, varargs, is_thunk,
                                         thunk_target, body_ranges
  3. tag REMOVALS                        must be 0
  4. old tag set a SUBSET of the new     must hold for every changed record
  5. comment REWRITTEN                   must be 0 - a record whose comment was already non-empty
                                         and whose new comment does not contain the old text

Dimensions 4 and 5 are the ones that separate ADDING annotation from REPLACING it, and they are the
whole point. A delta that fills 128 empty comments is additive. A delta that rewrites one populated
comment is not, however small - because a document may be quoting the text that was replaced.

MEASURED 2026-09-14 ACROSS THE WHOLE GN158..GN161 SPAN: 0 added, 0 removed, 128 records changed,
only `comment` and `tags` ever touched, 0 immutable changes, 0 tag removals, 128 of 128 old tag
sets a subset of the new, and 128 of 128 comments EMPTY before and gained one - 0 rewrites. The
sub-spans decompose exactly: 19 (GN158->GN160) + 109 (GN160->GN161) = 128, and 128 is also the
number of addresses that left the residual set over the same span. Three independent quantities
agreeing is what makes this a measurement rather than a reading of the batch applier's own record.

This SUPERSEDES the sample in the original adjudication. FABLE's basis text says "measured 19/19
and 15/15"; that was a sample of the cited functions on one page. This is the full population over
a longer span, and it agrees.

WHAT A PASS DOES NOT MEAN. It means the ADVANCE did not void the basis. It says nothing about the
second half of every transfer clause - "this document makes no uncorrected absence claim about any
of them" - which is per-document and is what `check_transfer_eligible.py` probes. Both halves must
hold before a stamp moves. A pass here is a fleet-level fact; a stamp is a per-document act.

CONTROL: every run re-measures a known-additive span and a deliberately corrupted copy of it, so a
tool that always says "additive" is caught. Run --self-test for the corruption control alone.
"""
import argparse
import copy
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diff_fas2 import parse  # noqa: E402

KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
WORK = os.path.join(REPO, "Database", "Tools", "work")
ENV = os.path.join(REPO, "Database", "Tools", "ghidra", "run", "GfzEnv.ps1")

IMMUTABLE = ("name", "namespace", "name_source", "repeatable_comment", "prototype",
             "signature_source", "calling_convention", "inline", "noreturn", "varargs",
             "is_thunk", "thunk_target", "body_ranges")

SNAPSHOTS = {
    "GN158": os.path.join(WORK, "verify", "snapshot.fas2.GN158"),
    "GN160": os.path.join(WORK, "verify_GFZ_GN160", "snapshot.fas2"),
    # GN161 ADDED 2026-09-21 (OPUS). The file was already in the tree, retained beside the
    # current parent under a _STALE name when GN162 was certified; what was missing was a TAG
    # for it, so `--from GN161 --to PARENT` answered "snapshot not in the tree" and every
    # GN161->GN162 transfer clause read UNMEASURED. That is a naming gap, not absent data:
    # this file's sha256 is c16409ec2c3b9070ea6ce3b6a16f5b4f2d9827380fe5cb626af173cc63739e4c,
    # which is GN161's certified $GfzLineage snapshot, and it is byte-identical to
    # work/batch_R30/pre.fas2 and work/batch_R109/post.fas2 - so the lineage is continuous
    # across the batch that produced each advance.
    "GN161": os.path.join(WORK, "verify_GFZ_PARENT", "snapshot_GN161_0914_STALE.fas2"),
    "PARENT": os.path.join(WORK, "verify_GFZ_PARENT", "snapshot.fas2"),
}


def additivity(A, B):
    """The five dimensions. -> dict; `additive` is True only if every one of them holds."""
    added, removed = sorted(set(B) - set(A)), sorted(set(A) - set(B))
    changed = [e for e in set(A) & set(B) if A[e] != B[e]]
    imm, tag_rem, tag_notsub, comment_rewritten = [], [], [], []
    fields = {}
    for e in changed:
        for k in A[e]:
            if k != "entry" and A[e][k] != B[e][k]:
                fields[k] = fields.get(k, 0) + 1
                if k in IMMUTABLE:
                    imm.append((e, k))
        ta = {x[0] for x in A[e]["tags"]}
        tb = {x[0] for x in B[e]["tags"]}
        if ta - tb:
            tag_rem.append((e, sorted(ta - tb)))
        if not ta <= tb:
            tag_notsub.append(e)
        a, b = A[e]["comment"], B[e]["comment"]
        if a and not (b and a in b):
            comment_rewritten.append(e)
    return {
        "added": added, "removed": removed, "changed": len(changed), "fields": fields,
        "immutable": imm, "tag_removals": tag_rem, "tag_not_subset": tag_notsub,
        "comment_rewritten": comment_rewritten,
        "additive": not (added or removed or imm or tag_rem or tag_notsub or comment_rewritten),
    }


def report(label, r, indent="  "):
    print("%s== %s" % (indent, label))
    print("%s   changed records    %d   fields touched: %s"
          % (indent, r["changed"], r["fields"] or "none"))
    for name, v in (("functions ADDED", r["added"]), ("functions REMOVED", r["removed"]),
                    ("IMMUTABLE field changes", r["immutable"]),
                    ("tag REMOVALS", r["tag_removals"]),
                    ("old tag set NOT a subset", r["tag_not_subset"]),
                    ("comments REWRITTEN", r["comment_rewritten"])):
        flag = "" if not v else "   <- VOIDS THE BASIS"
        print("%s   %-26s %d%s" % (indent, name, len(v), flag))
    print("%s   ADDITIVE: %s" % (indent, r["additive"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="a", help="snapshot path or a tag: %s"
                                             % ", ".join(sorted(SNAPSHOTS)))
    ap.add_argument("--to", dest="b", default="PARENT")
    ap.add_argument("--self-test", action="store_true")
    # ACCEPTED AND IGNORED, DELIBERATELY. `run_gates.py` globs `check_*.py` and hands every corpus
    # gate `--db <path>`; this file reads FAS2 snapshots under `Tools/work`, not the document
    # corpus, so it has no use for the value - but refusing the argument made it exit 2 on every
    # gate run. A checker that crashes every time is noise, and noise trains people to ignore reds.
    # Taking the argument and not using it is honest here; silently scanning the wrong tree would
    # not be.
    ap.add_argument("--db", help=argparse.SUPPRESS)
    a = ap.parse_args()

    have = {k: v for k, v in SNAPSHOTS.items() if os.path.isfile(v)}
    if len(have) < 2:
        print("CANNOT RUN: need at least two snapshots; found %s" % (sorted(have) or "none"))
        return 2

    pairs = ([(a.a, a.b)] if a.a else
             [(x, "PARENT") for x in sorted(have) if x != "PARENT"] +
             ([("GN158", "GN160")] if {"GN158", "GN160"} <= set(have) else []))

    print("ADDITIVITY OF THE ANNOTATION DELTA - the `voided_by` clause, executed")
    worst = 0
    last = None
    for x, y in pairs:
        pa, pb = SNAPSHOTS.get(x, x), SNAPSHOTS.get(y, y)
        if not (os.path.isfile(pa) and os.path.isfile(pb)):
            print("  skipped %s -> %s (snapshot not in the tree)" % (x, y))
            continue
        _, A = parse(pa)
        _, B = parse(pb)
        r = additivity(A, B)
        report("%s -> %s" % (x, y), r)
        last = (A, B, r)
        worst = max(worst, 0 if r["additive"] else 1)
        print()

    # CONTROL - a tool that always says "additive" is worthless. Corrupt a copy and require it
    # to be caught, using the same span that just passed.
    if last:
        A, B, _ = last
        e = sorted(set(A) & set(B))[0]
        C = copy.deepcopy(B)
        C[e] = dict(C[e])
        C[e]["name"] = (C[e]["name"] or "") + "_MUTATED"
        C[e]["comment"] = "a rewritten comment"
        C[e]["tags"] = []
        A2 = dict(A)
        A2[e] = dict(A2[e])
        A2[e]["comment"] = "an original comment that the new one does not contain"
        A2[e]["tags"] = [("ORIGINAL-TAG", "x")]
        rc = additivity(A2, C)
        ok = (not rc["additive"] and rc["immutable"] and rc["tag_removals"]
              and rc["comment_rewritten"])
        print("  CONTROL (one record renamed, its comment rewritten, its tag dropped)")
        print("    caught as NOT additive : %s" % (not rc["additive"]))
        print("    immutable / tag-removal / comment-rewrite all fired : %s" % bool(ok))
        if not ok:
            print("\n  CONTROL FAILED: the test does not detect a delta it must detect.")
            print("  Every ADDITIVE verdict above is unfounded.")
            return 2
        print("    control passed.")

    if a.self_test:
        return 0
    if worst:
        print("\nA SPAN IS NOT ADDITIVE. Every `transfers_to` block whose basis is the")
        print("additive-annotation delta is VOID by its own clause across that span, and the")
        print("documents owe re-verification rather than a re-targeted stamp.")
    else:
        print("\nEvery span measured is ADDITIVE, so the advance does not void the basis.")
        print("That is a FLEET-level fact. The other half of every transfer clause - that the")
        print("document makes no uncorrected absence claim - is per-document and is what")
        print("check_transfer_eligible.py probes. Both must hold before a stamp moves.")
    return worst


if __name__ == "__main__":
    sys.exit(main())
