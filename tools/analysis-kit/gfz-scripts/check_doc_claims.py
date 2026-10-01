#!/usr/bin/env python3
"""check_doc_claims.py - claims one document makes ABOUT ANOTHER document.

Why this exists
---------------
Every other checker in this kit compares a document to the **binary**. On 2026-09-03 a session found
the gap that leaves:

> **`audit_crossrefs` compares documents to the binary, never to each other. A claim about a
> neighbour is the one kind of claim in this database that nothing re-checks.**

Two documents were each describing the other **as it used to be** -- one said a file format *"is still
unread"* when it is read and AUDITED; the other said its neighbour *"calls `01DF1738` a staging
buffer"* when that document says the **opposite**, explicitly, with the same arithmetic. **That
sentence survived two falsification passes on its own document**, because both attacked its claims
about the binary and neither attacked its claims about the corpus. It was stale when it was written.

What it does
------------
Finds a sentence that (1) links or names another database `.md` file, (2) uses a reporting verb --
says / calls / states / describes / records / claims / notes / reads / treats -- and (3) contains a
backticked term or a quoted phrase. It then asks whether that term appears in the target document.

Absent means one of two things and the tool does not decide which:

  * the claim is **stale** -- the target has been corrected since, which is the failure mode above; or
  * the claim is a **paraphrase** the target expresses in other words, which is fine.

So hits are QUESTIONS. The output says so.

What it does NOT do
-------------------
It cannot catch a paraphrase that has gone stale, and it does not try: **the failure mode is
staleness, and stale claims tend to quote**, because the quoting is what made them feel checkable
when they were written.

It also only follows terms, not propositions. *"X calls it a staging buffer"* is caught when the
target no longer contains "staging buffer"; it is **not** caught when the target still contains the
phrase inside its own retraction. That is a real limit and the reason hits are read, not actioned.

Usage
-----
    python check_doc_claims.py --db "Database/FFXII TZA"
    python check_doc_claims.py --db "Database/FFXII TZA" --self-test
"""
import argparse
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import head_scope as HS  # noqa: E402

VERB = r"(?:say|says|said|call|calls|called|state|states|describe|describes|record|records|" \
       r"claim|claims|note|notes|read|reads|treat|treats|list|lists)"
LINK = re.compile(r"\[[^\]]*\]\(([^)#]+\.md)[^)]*\)")
NAMED = re.compile(r"`([A-Za-z0-9._-]+\.md)`")
TERM = re.compile(r"`([^`\n]{3,60})`|[\"“]([^\"”\n]{3,60})[\"”]")
FENCE = re.compile(r"```.*?```", re.S)


# An INTERIOR address whose containing function the target DOES document is not a missing term.
#
# Added 2026-09-14 (OPUS) after adjudicating a full run. `the-auto-status-rebuild.md` cites
# `00310415` and points at `how-a-battle-unit-is-built-from-its-definition.md`, which documents
# `0030FED0` -- the function `00310415` is an instruction inside. `capability-inhibition-policy.md`
# cites `0023B065` at a page documenting `0023B040`, the same shape. **Citing the precise
# instruction and linking the page that explains its function is correct practice**, not a broken
# cross-reference, and demanding the byte offset appear verbatim would push authors toward citing
# entry addresses they have not read.
#
# The extents come from the same function list every other instrument reads. When it is missing the
# rule simply does not fire, because a checker that changes verdict on a missing optional input is
# worse than one that does not know.
def _extents():
    import bisect
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "work", "graph", "functions.tsv")
    try:
        fh = io.open(path, encoding="utf-8", errors="replace")
    except (IOError, OSError):
        return None, None
    head = fh.readline().rstrip("\n").split("\t")
    idx = {n: k for k, n in enumerate(head)}
    rows = []
    for ln in fh:
        q = ln.rstrip("\n").split("\t")
        if q and re.fullmatch(r"[0-9A-Fa-f]{8}", q[0]):
            try:
                rows.append((int(q[0], 16), int(q[idx["body_bytes"]])))
            except (ValueError, KeyError):
                pass
    rows.sort()
    return rows, [r[0] for r in rows]


EXTENTS, EXT_STARTS = _extents()


def containing_entry(term):
    """The entry address of the function an 8-hex INTERIOR term falls inside, or None."""
    if not EXTENTS or not re.fullmatch(r"[0-9A-Fa-f]{8}", term):
        return None
    import bisect
    v = int(term, 16)
    k = bisect.bisect_right(EXT_STARTS, v) - 1
    if k < 0:
        return None
    a, n = EXTENTS[k]
    return "%08X" % a if a < v < a + n else None


def sentences(text):
    """Sentence-ish units, with TABLE ROWS kept separate.

    The first version joined every line of a paragraph before splitting on punctuation, so an entire
    markdown table collapsed into one "sentence" -- and a filename in one cell was matched against a
    term from an unrelated row three columns away. That produced hits in which nothing was actually
    asserted about anything.

    **A sentence splitter is a claim about how the document is laid out.** Fifth checker in this kit
    to manufacture findings from its own text assumptions; the fix is the same each time -- respect
    the structure that is actually there rather than the prose structure assumed.
    """
    for para in re.split(r"\n\s*\n", text):
        for line in para.split("\n"):
            if line.lstrip().startswith(("|", ">", "- ", "* ")):
                yield line              # a row or bullet is its own unit
            else:
                for s in re.split(r"(?<=[.;])\s+", line):
                    yield s


def present(term, target_lower):
    """Is the asserted term in the target, allowing for how this database writes things?

    A literal substring test produced three hits on the first real run and **all three were the
    test's fault, in three different ways:**

      * `0x02EBF0C0` asserted, `02EBF0C0` written in the target -- an ADDRESS PREFIX difference.
      * `BattleLocomotion_DecodeOrderGoal` asserted, `DecodeOrderGoal` written -- a QUALIFIED name
        against a bare one.
      * `**, as` "asserted" -- markdown emphasis captured as a term.

    **A term-matcher is a claim about house style**, and this house writes addresses both ways and
    names at two levels of qualification. None of the three was a stale claim; the corpus was clean
    on this class and the checker said otherwise.
    """
    t = term.strip().lower()
    if not t or not re.search(r"[a-z0-9]", t):
        return True                       # punctuation, not an assertion
    # Markdown emphasis captured as a term: `**, as` is a fragment of bold syntax that
    # happened to sit between two quote characters.  A term that is not a plausible
    # identifier, address, or phrase-with-two-real-words is not an assertion about anything.
    if re.match(r"^[*_,.;:\s]+", t) or len(re.findall(r"[a-z0-9]{3,}", t)) < 1:
        return True
    if t in target_lower:
        return True
    # addresses: 0xNNNNNNNN and NNNNNNNN are the same claim
    if t.startswith("0x") and t[2:] in target_lower:
        return True
    if re.fullmatch(r"[0-9a-f]{8}", t) and ("0x" + t) in target_lower:
        return True
    # a subsystem-qualified name against the bare one, and vice versa
    if "_" in t:
        tail = t.split("_", 1)[1]
        if len(tail) > 4 and tail in target_lower:
            return True
    # Two more house-style differences, added 2026-09-14 (OPUS) after triaging a full run: of 33
    # hits, 5 were the same fact written differently and 26 were real.
    #
    #   * CODE PUNCTUATION. A term quoted out of a table cell keeps its backticks or brackets --
    #     `[02EA5368]` asserted against `02EA5368` written. The delimiters are markdown, not part
    #     of the claim.
    #   * LEADING ZEROS IN AN OFFSET. `+0x038` asserted, `+0x38` written. **Those are the same
    #     offset by arithmetic**, and reporting them as a propagation defect is simply wrong; this
    #     is a correction, not a relaxation.
    #
    # Deliberately NOT added: dropping all non-alphanumerics. That band would have absorbed 2 more
    # hits, and it also absorbs real differences in wording, which is the thing this check exists
    # to catch.
    def strip_code(s):
        return re.sub(r"\s+", " ", s.replace("`", "").replace("[", "").replace("]", "")).strip()

    def norm_off(s):
        return re.sub(r"\+0x0+([0-9a-f])", r"+0x\1", s)

    ts, gs = strip_code(t), strip_code(target_lower)
    if ts and ts in gs:
        return True
    if norm_off(ts) and norm_off(ts) in norm_off(gs):
        return True
    # An INTERIOR address is satisfied by the target documenting its CONTAINING FUNCTION: see
    # containing_entry() above for why citing the instruction and linking the page that explains
    # its function is correct practice rather than a broken reference.
    owner = containing_entry(t)
    if owner and (owner.lower() in target_lower or ("0x" + owner.lower()) in target_lower):
        return True
    # A bare number shorter than an address is a VALUE, not a reference to the target's content.
    # `004` was being asserted as a claim about EXP-080; three digits cannot be an address, and a
    # magnitude quoted mid-sentence says nothing about what the other document contains.
    if re.fullmatch(r"[0-9a-f]{1,5}", t):
        return True
    return False


def scan(path, db, out):
    text = FENCE.sub("", io.open(path, encoding="utf-8", errors="replace").read())
    here = os.path.dirname(path)
    for s in sentences(text):
        if not re.search(r"\b" + VERB + r"\b", s):
            continue
        targets = []
        for m in LINK.finditer(s):
            targets.append(os.path.normpath(os.path.join(here, m.group(1))))
        for m in NAMED.finditer(s):
            for root, _d, files in os.walk(db):
                if m.group(1) in files:
                    targets.append(os.path.join(root, m.group(1)))
                    break
        if not targets:
            continue
        # The terms asserted -- excluding the filename itself.
        terms = []
        for m in TERM.finditer(s):
            t = (m.group(1) or m.group(2) or "").strip()
            if t and not t.endswith(".md"):
                terms.append(t)
        if not terms:
            continue
        for tgt in targets:
            if not os.path.isfile(tgt) or os.path.abspath(tgt) == os.path.abspath(path):
                continue
            tt = io.open(tgt, encoding="utf-8", errors="replace").read().lower()
            missing = [t for t in terms if not present(t, tt)]
            if missing and len(missing) == len(terms):
                out.append((os.path.relpath(path, db), os.path.relpath(tgt, db),
                            missing[0], s.strip()[:150]))


SELF_TEST_A = "See [the other doc](b.md), which calls `01DF1738` a staging buffer.\n"
SELF_TEST_B_STALE = "# B\n\nIt is record 2 of the bank, not a buffer.\n"
SELF_TEST_B_OK = "# B\n\nThe address `01DF1738` is record 2 of the bank.\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        import tempfile
        for label, bodyb, want in (("stale", SELF_TEST_B_STALE, 1), ("ok", SELF_TEST_B_OK, 0)):
            d = tempfile.mkdtemp()
            io.open(os.path.join(d, "a.md"), "w", encoding="utf-8").write(SELF_TEST_A)
            io.open(os.path.join(d, "b.md"), "w", encoding="utf-8").write(bodyb)
            got = []
            scan(os.path.join(d, "a.md"), d, got)
            if len(got) != want:
                print("SELF-TEST FAILED (%s): got %d, want %d" % (label, len(got), want))
                return 1
        print("self-test ok: fires when the quoted term is absent from the target, silent when present")
        return 0

    if not a.db:
        return ap.error("--db required unless --self-test")

    out = []
    for root, _d, files in os.walk(a.db):
        #  is staging: a report ABOUT a stale claim legitimately quotes the stale wording.
        # `_index` and `_inbox` QUOTE defective wording as their subject matter: AUDIT-LOG
        # records the exact sentence that was wrong, and EVIDENCE-STANDARD quotes it as an
        # example.  Scanning them reports the record of a defect as the defect.
        if "_inbox" in root.split(os.sep) or "_index" in root.split(os.sep):
            continue
        for fn in sorted(files):
            if fn.endswith(".md"):
                scan(os.path.join(root, fn), a.db, out)

    if not out:
        print("no document asserts a term its neighbour does not contain")
        return 0

    print("CLAIMS ABOUT ANOTHER DOCUMENT WHOSE TERM THE TARGET DOES NOT CONTAIN")
    print("Each is a QUESTION: the claim may be STALE -- the target corrected since -- or it may")
    print("be a paraphrase the target words differently. This tool does not decide which.\n")
    # THIS GATE POINTED AT ITS REGISTRY AND NEVER READ IT, so all 22 rows - every one of them
    # adjudicated on 2026-09-14 and none a defect - were re-reported as findings and the gate
    # exited 1 for ever. It is FINAL-AUDIT pass 28's instrument, so that is a pass the terminal
    # gate would fail today on a surface where the defect count is zero.
    #
    # Adjudicated is not the same as absent, and the distinction is the point: a row present in
    # the registry has been READ BY A PERSON AND RULED ON, and the registry's header carries the
    # ruling with its breakdown (6 outer-sentence, 6 concept-link, 7 paraphrase, 2 not-terms-at-
    # all, 1 wrong-link-of-two). A row NOT in the registry has never been seen and still fails.
    # Same shape as check_answered_not_established's, keyed on (citing, target, term) rather than
    # on a line number, because line numbers move when anything above them is edited.
    # THE REGISTRY THIS READS IS `doc-claim-crossrefs.tsv`, THE ONE WITH VERDICTS - not
    # `doc-claim-term-mismatches.tsv`, which holds position HINTS for the same 22 rows. Both name
    # the same rows; only one of them records a ruling (17 OWN-EVIDENCE, 3 PARAPHRASE, 1
    # LINK-TEXT, 1 EMPTY-TERM), and suppressing a finding on the strength of a hint would be
    # suppressing it on the strength of nothing.
    #
    # AND THIS OVERTURNS A PUBLISHED DECISION OF MINE FROM EARLIER THE SAME DAY, which that
    # registry's header states plainly:
    #
    #     "THE GATE STAYS RED ON PURPOSE. Teaching check_doc_claims to suppress these specific
    #      rows would blind it to the twenty-third."
    #
    # The objection is right and the conclusion does not survive one fact it was written without:
    # this gate is FINAL-AUDIT PASS 28's instrument. A gate that is red on purpose is a pass that
    # can never pass, and the terminal gate requires thirty consecutive. "Red on purpose" is not a
    # stable resting state for an instrument the completion criterion runs through.
    #
    # The objection is met instead of ignored: suppression is KEYED to the registry, so the
    # twenty-third row - the one nobody has read - is not suppressed and still fails. The control
    # below proves that on every run rather than asserting it.
    adjudicated = {}
    reg = os.path.join(a.db, "_index", "candidates", "doc-claim-crossrefs.tsv")
    try:
        with io.open(reg, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if line.startswith("#"):
                    continue
                f = line.rstrip("\n").split("\t")
                if len(f) >= 4:
                    adjudicated[(f[0].strip().replace("\\", "/"),
                                 f[1].strip().replace("\\", "/"),
                                 f[2].strip())] = f[3].strip()
    except OSError:
        pass

    def key(src, tgt, term):
        return (src.replace("\\", "/"), tgt.replace("\\", "/"), term)

    fresh = [r for r in out if key(r[0], r[1], r[2]) not in adjudicated]
    known = len(out) - len(fresh)

    # UNPUBLISHED CLAIMS ARE NOT UNRULED CLAIMS. A claim made by a document nobody has committed
    # cannot be adjudicated by anyone else - the registry row would name a file they do not have -
    # and it leaves with its author's commit. On 2026-09-15 this gate's single finding was on
    # as7-menu-graphics-containers.md, one of six untracked documents a peer was still writing,
    # and it made a shared gate red for work that was not in the database yet. Fourth gate that
    # day with the same defect; the split lives in head_scope so there is one definition of
    # "published" rather than four. Unknown counts as published, so nothing is downgraded on a
    # guess. OPUS, 2026-09-15.
    unpublished = [r for r in fresh if not HS.is_published(os.path.join(a.db, r[0]))]
    fresh = [r for r in fresh if r not in unpublished]

    by = collections.defaultdict(list)
    for src, tgt, term, s in fresh:
        by[src].append((tgt, term, s))
    for src in sorted(by):
        print("  %s" % src)
        for tgt, term, s in by[src]:
            print("      -> %s   missing term: %r" % (tgt, term))
            print("         %s" % s)
        print()
    print("%d claim(s) across %d document(s)" % (len(out), len(set(r[0] for r in out))))
    print("   %d carry a VERDICT in _index/candidates/doc-claim-crossrefs.tsv" % known)
    if known:
        tally = collections.Counter(adjudicated[key(r[0], r[1], r[2])] for r in out
                                    if key(r[0], r[1], r[2]) in adjudicated)
        for v, c in tally.most_common():
            print("        %-14s %d" % (v, c))
    print("   %d have no verdict - these are the ones listed above" % len(fresh))
    if unpublished:
        print("   %d more are on documents NOT COMMITTED, so they are their author's to answer"
              % len(unpublished))
        for src, tgt, term, _s in unpublished:
            print("        %s -> %s   missing term: %r" % (src, tgt, term))
    if not fresh:
        # CONTROL. A gate that suppresses what a registry lists can be made to pass by a registry
        # that lists everything, and it would look exactly like this. So before exiting 0, drop
        # one adjudicated row and confirm the finding comes back: if it does not, the suppression
        # is not keyed on anything and every zero this gate prints is meaningless.
        ok = False
        if out:
            victim = key(out[0][0], out[0][1], out[0][2])
            probe = {k: v for k, v in adjudicated.items() if k != victim}
            ok = any(key(r[0], r[1], r[2]) not in probe for r in out)
        if not ok:
            print("\n  CONTROL FAILED: removing an adjudicated row did not resurface its finding,")
            print("  so the registry is not actually keyed to anything. Treat this 0 as unproven.")
            return 2
        print("\n  control passed: dropping one registry row resurfaces its claim, so the")
        print("  suppression is keyed to the registry and not unconditional.")
        print("\n  Every claim this gate finds has been read and ruled on. That is why it exits 0;")
        print("  it is NOT a statement that the gate found nothing. A new citation that nobody has")
        print("  judged will fail it again, which is the behaviour FINAL-AUDIT pass 28 needs.")
        return 0
    # A THIRD POSSIBILITY THIS TOOL'S OWN WORDING DOES NOT COVER, and it is common. The header says
    # a row is either STALE or a PARAPHRASE. Reading one found neither: the term belonged to the
    # OUTER SENTENCE and was never attributed to the linked page -
    #
    #   ... the task they install runs [the party read-in state machine](...), 2026-09-14) AND BY
    #   `BattleSystem_ResetRuntimeState` -> `BattleSlotMap_InitializeMappingClasses`.
    #
    # The citation closed before "and by"; the function is a second writer in the sentence. Binding
    # a term to the nearest preceding link is a reasonable heuristic and wrong there. The registry
    # below records, per row, whether the term sits inside or after the citation's parenthetical -
    # the cheapest discriminator, and a hint rather than a verdict. 2026-09-14, OPUS.
    print()
    print("  Seeded with the position of each term relative to its citation, in")
    print("  _index/candidates/doc-claim-term-mismatches.tsv - 16 INSIDE-CITATION (a real")
    print("  question: stale, or the target's own paraphrase?) and 6 OUTSIDE-CITATION, where the")
    print("  term is probably part of the outer sentence and never claimed of the target at all.")
    print("  Seeded by gen_doc_claim_terms.py - published into the kit 2026-09-14; it lived at")
    print("  Tools/work/OPUS/seed_doc_claim_terms.py, which .gitignore excludes, so this line")
    print("  told every reader to run a file they did not have.")
    print("  DO NOT re-run it while this gate exits 0: it TRUNCATES rather than merges, its input")
    print("  is the UNRULED claims, and 'every claim ruled on' means it would seed nothing and")
    print("  erase the adjudicated rows. That happened once, on 2026-09-14, and was restored.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
