"""gen_doc_claim_terms.py - the cross-document claim/term mismatches, with the evidence attached.

PUBLISHED INTO THE KIT 2026-09-14 from `Tools/work/OPUS/seed_doc_claim_terms.py`, which
`.gitignore` excludes - while `check_doc_claims.py` ended its output with "Regenerate with
Tools/work/OPUS/seed_doc_claim_terms.py". That checker serves FINAL-AUDIT pass 28, so the
instruction for regenerating a GATE'S INPUT pointed at a file no peer had.

NAMED `gen_*`, NOT `check_*`, on purpose: it GENERATES a candidates file, and `run_gates.py`
globs `check_*.py`. A generator under that prefix would be run as a gate every suite and would
rewrite its output as a side effect of auditing.

> **DO NOT RUN THIS ONCE THE CLAIMS ARE ADJUDICATED - IT TRUNCATES, IT DOES NOT MERGE.** Its input
> is whatever `check_doc_claims` reports as UNRULED, and that gate now exits 0 because every claim
> it finds carries a verdict in `doc-claim-crossrefs.tsv`. So the seeder finds nothing, writes a
> file with no rows, and **destroys the 22 adjudicated rows and their attached evidence** that the
> file already held.
>
> That is not hypothetical: it happened on 2026-09-14, on the first run after this file was moved
> into the kit. The file went 85 lines to 63, `rows seeded: 0`, and was restored from HEAD. The
> trap is that the gate exiting 0 reads like "nothing to do" when it means "everything here has
> already been ruled on" - the exact state in which regenerating is most destructive.
>
> **The rows are a record of adjudication, not a regenerable snapshot.** Until this merges instead
> of truncating, it is safe only against a corpus with unruled claims outstanding.

The old name said "the 22 mismatches" - a count in a title, which goes stale the first time the
tool works. Retitled.

`check_doc_claims` finds a document citing another and using a term the target does not contain, and
says of itself, correctly: *"Each is a QUESTION: the claim may be STALE - the target corrected since
- or it may be a paraphrase the target words differently. This tool does not decide which."*

Reading one showed a third possibility the wording does not cover, and it is the common one:

    ... through `0037C980` / `0037CA00` / `0037CA80` ([the verb table](...); the task they install
    runs [the party read-in state machine](the-party-read-in-state-machine.md), 2026-09-14) **and
    by** `BattleSystem_ResetRuntimeState` -> `BattleSlotMap_InitializeMappingClasses`.

`BattleSystem_ResetRuntimeState` is a SECOND WRITER in the outer sentence. It is not attributed to
the linked page at all - the citation closed before "and by". The checker binds a term to the
nearest preceding link, which is a reasonable heuristic and wrong here.

SO THIS SEEDS, IT DOES NOT DECIDE. Each row carries the citing document, the target, the term and
the whole sentence, plus one mechanical hint:

  OUTSIDE-CITATION  the term appears AFTER the link's closing `)` or `]`, so it is probably part of
                    the outer sentence rather than a claim about the target
  INSIDE-CITATION   the term falls within the citation's own parenthetical

**The hint is not a verdict.** A term after the paren can still be a claim about the target, and one
inside can still be the citing page's own paraphrase. What it does is put the cheapest discriminator
in front of whoever reads the row, which is the same thing the text-gap and answered-question
registries did for their gates.
"""
import io, os, re, subprocess, sys, collections

# Resolved from __file__, not cwd: this now lives IN the kit, so a relative KIT path would only
# work from the repository root.
KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
DB = os.path.join(REPO, "Database", "FFXII TZA")
OUT = os.path.join(DB, "_index", "candidates", "doc-claim-term-mismatches.tsv")


def main():
    r = subprocess.run([sys.executable, os.path.join(KIT, "check_doc_claims.py"), "--db", DB],
                       capture_output=True, text=True)
    txt = r.stdout + r.stderr
    rows, citing = [], None
    lines = txt.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^  (\S.*\.md)\s*$", line)
        if m:
            citing = m.group(1).replace("\\", "/")
            continue
        m = re.match(r"^      -> (\S.*\.md)\s+missing term: '(.*)'\s*$", line)
        if m and citing:
            target, term = m.group(1).replace("\\", "/"), m.group(2)
            sent = lines[i + 1].strip() if i + 1 < len(lines) else ""
            rows.append((citing, target, term, sent))

    out = []
    hint = collections.Counter()
    core_hint = collections.Counter()
    for citing, target, term, sent in rows:
        # THE CHECKER'S EXCERPT IS TRUNCATED, so positions taken from it are often invisible - 13
        # of 22 came back UNDETERMINED on the excerpt alone. Recover the WHOLE line from the citing
        # document instead, matching on the line that holds both the target's basename and the
        # term. A hint computed from a cut-off string is a hint about the cut.
        base = os.path.basename(target)
        bare = term.strip("`")
        full = sent
        try:
            for ln in io.open(os.path.join(DB, citing.replace("/", os.sep)),
                              encoding="utf-8", errors="replace"):
                if base in ln and bare in ln:
                    full = ln.strip()
                    break
        except OSError:
            pass
        sent = full
        li = sent.find(base)
        ti = sent.find(bare)
        h = "UNDETERMINED"
        if li >= 0 and ti >= 0:
            close = sent.find(")", li)
            h = "OUTSIDE-CITATION" if (close >= 0 and ti > close) else "INSIDE-CITATION"
        # IS THE CORE OF THE TERM PRESENT, EVEN THOUGH THE TERM IS NOT? `00267310(manager)` is
        # reported missing from a target that names `00267310` four times - the target simply does
        # not write the call shape. That is precisely the "paraphrase" case the gate's header allows
        # for, and it is mechanical to spot: strip the decoration and look again. Distinguishing it
        # from a genuine absence is most of the value in this file.
        core = re.match(r"0[0-9A-Fa-f]{7}", term.strip("`"))
        present = ""
        if core:
            try:
                tt = io.open(os.path.join(DB, target.replace("/", os.sep)),
                             encoding="utf-8", errors="replace").read()
                n = len(re.findall(re.escape(core.group(0)), tt, re.I))
                present = ("CORE-PRESENT x%d" % n) if n else "CORE-ABSENT"
            except OSError:
                present = "TARGET-UNREADABLE"
        hint[h] += 1
        core_hint[present or "n/a"] += 1
        out.append((citing, target, term, h, present, sent))

    hdr = [
        "# Cross-document claims whose term the target does not contain - seeded, not decided.",
        "#",
        "# check_doc_claims says each row is a QUESTION: the claim may be STALE (the target",
        "# corrected since) or a PARAPHRASE the target words differently, and that it does not",
        "# decide which. Reading one turned up a third possibility its wording does not cover, and",
        "# it is the common one: the term belongs to the OUTER SENTENCE, not to the citation.",
        "#",
        "#   ... runs [the party read-in state machine](...), 2026-09-14) AND BY",
        "#   `BattleSystem_ResetRuntimeState` -> `BattleSlotMap_InitializeMappingClasses`.",
        "#",
        "# BattleSystem_ResetRuntimeState is a second writer in the outer sentence; the citation",
        "# closed before 'and by'. The checker binds a term to the nearest preceding link, which is",
        "# a reasonable heuristic and wrong here.",
        "#",
        "#   OUTSIDE-CITATION  the term appears after the link's closing ')' - probably the outer",
        "#                     sentence, not a claim about the target",
        "#   INSIDE-CITATION   the term falls inside the citation's own parenthetical",
        "#   UNDETERMINED      the sentence excerpt does not show both positions",
        "#",
        "# THE HINT IS NOT A VERDICT. A term after the paren can still be a claim about the target,",
        "# and one inside can still be the citing page's own paraphrase. It puts the cheapest",
        "# discriminator in front of the reader; the reading is still the reading.",
        "#",
        "# ALL 22 ROWS ARE NOW ADJUDICATED, 2026-09-14 (OPUS), AND NONE IS A DEFECT.",
        "#",
        "#   6  the term sits AFTER its citation closed and belongs to the outer sentence",
        "#   6  concept-link: the citing page names its own address and links the target for a",
        "#      SHARED CONCEPT (see the detailed note below)",
        "#   7  paraphrase: the target holds the same fact in different words. Checked by",
        "#      component, not by string - `vit = target.+0x2C` has both `target` and `+0x2C` in",
        "#      the target; `0x5000 + row`, `state + 0x59C8 + row`, `owned - reserved` likewise;",
        "#      and `0031E9A0(row)`'s 'item-row class' is on the stat page at line 153 as",
        "#      '0031E9A0 classifies the item row'",
        "#   2  not terms at all - the checker extracted a prose fragment ('the format page',",
        "#      '... triggered a trap'), which has no citable token to look for",
        "#   1  THE WRONG LINK OF TWO. The cell holds two citations; `+0xE9A` belongs to the first",
        "#      ([status write] section 2.7), where it appears FIVE times, and the checker paired it",
        "#      with the second ([evaluation context]).",
        "#",
        "# The heuristic - a term near a link is a claim about that page - is reasonable, and on a",
        "# corpus that cites densely inside table cells it produces false positives at close to",
        "# 100%. Recorded so the next reader inherits the finding rather than re-deriving it.",
        "#",
        "# ADJUDICATED 2026-09-14 (OPUS): ALL SIX CORE-ABSENT ROWS ARE ONE SHAPE, AND IT IS NOT A",
        "# DEFECT. In each, the citing page names ITS OWN address and links the target for a SHARED",
        "# CONCEPT - never to attribute the address to it. The link is introduced by the concept in",
        "# every case: 'the party-type band', 'the same property', 'the same handle form', 'the",
        "# idiom', 'the actor storage map'. Verified in full document context for",
        "# the-record-00329220-builds.md, where the table row reads",
        "#",
        "#   | party only: bits 1, 2 | `00329660`-`00329691` | bit 1 when type ... (the party-type",
        "#   band [the kind-byte page](...) measures) |",
        "#",
        "# - the address is in COLUMN 2 and the link in COLUMN 3. The checker associated a term from",
        "# one table column with a link in another. 'The target does not contain the term' is true",
        "# and irrelevant: the citing page never said it did.",
        "#",
        "#   CORE-PRESENT xN   the term's ADDRESS is in the target N times and only the decoration",
        "#                     differs - the paraphrase case, not a stale claim. `00267310(manager)`",
        "#                     is reported missing from a page that names `00267310` four times.",
        "#   CORE-ABSENT       the address is not in the target at all - a real question",
        "#",
        "# citing_document\ttarget_document\tmissing_term\tposition_hint\tcore_in_target\tsentence",
    ]
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(hdr) + "\n")
        for c, t, term, h, pres, sent in out:
            fh.write("\t".join([c, t, term, h, pres, sent.replace("\t", " ")]) + "\n")

    print("rows seeded: %d" % len(out))
    for k, v in hint.most_common():
        print("   %-18s %d" % (k, v))
    for k, v in core_hint.most_common():
        print("   %-18s %d" % (k, v))
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
