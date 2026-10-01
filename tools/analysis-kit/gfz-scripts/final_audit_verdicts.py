"""final_audit_verdicts.py - what would the terminal gate do TODAY, pass by pass?

PUBLISHED 2026-09-14 FROM `Tools/work/OPUS/final_audit_readiness.py`, WHICH WAS GITIGNORED.
FINAL-AUDIT-PROTOCOL.md quotes this table - "27 clean, 1 would fail, 1 PARTIAL, 1 manual" -
and for a day the instrument behind it lived under `Tools/work/`, which `.gitignore` excludes.
A canonical index was citing a number no peer could reproduce. That is the same defect class
the index-consistency criterion is about, arriving through the tooling rather than the prose.

THAT QUOTED SPLIT IS A 2026-09-14 RECORD AND IS NO LONGER THE TABLE. It sits under a dated
heading in FINAL-AUDIT-PROTOCOL.md and is deliberately left standing there - absorbing preserved
history is the failure the evidence standard forbids. As of 2026-09-18 the table reads 23 clean
and 7 PARTIAL: passes 19, 20 and 21 were clean on check_call_chains.py, an instrument whose own
header says it is for pass 29, and pass 22's class stopped being empty.

NOT NAMED `check_*` ON PURPOSE: `run_gates.py` globs `check_*.py`, and this reads the baseline
`run_gates` writes. Globbing it would make the gate runner invoke a reader of its own output.

The SIBLING `audit_protocol_readiness.py` answers a different question - can each named tool be
INVOKED at all, without a traceback. This one asks what verdict each pass carries. Both matter
and neither substitutes for the other.

`final_audits` is 0/30 and gated on `unresolved = 0` and an empty `OPEN-QUESTIONS.md`, neither of
which OPUS can move alone. What CAN be known now is which of the thirty passes would fail the
moment the gate opens - and that is worth knowing now rather than on pass 6 of a streak, which is
the protocol's own stated reason for running its passes as diagnostics while the gate is shut:

    "a defect found now costs one fix while the same defect on pass 6 of thirty costs the whole
     streak."

So: map every pass to the instrument(s) the protocol names for it, ask `gate-baseline.tsv` what
each of those instruments currently does, and print a readiness table.

WHAT THIS IS NOT. It is not a claim that a green instrument passes its pass. Every coverage note
in the protocol's own table says `partial`, and the protocol says of its own inventory that
"counting instruments as coverage would be the 'volume is not explanation' mistake in a different
costume". A green row here means THE MECHANISED PART IS CLEAN, never that the pass is satisfied.
The value is the RED rows: an instrument that is red today is a pass that fails today.
"""
import io
import os
import re
import subprocess
import sys

# Resolved from __file__, not cwd. The kit learned this the hard way on 2026-09-14:
# check_index_figures.py computed its repo root with three dirname calls from a
# four-deep directory, every path became <repo>/Database/Database/..., and an
# os.path.isfile guard turned the wrong path into a SILENTLY OMITTED metric.
KIT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(KIT))))
BASE = os.path.join(REPO, "Database", "FFXII TZA", "_index", "gate-baseline.tsv")

# Pass -> instruments, from FINAL-AUDIT-PROTOCOL.md's two tables and its dated addenda.
# Where the protocol names a tool that is not a `check_*` corpus gate (audit_crossrefs,
# progress.py, fas2_export) it is listed so the row is honest about what is not in the baseline.
# Gates whose baseline entry is a --self-test result rather than a corpus run. DERIVED
# from run_gates, never retyped: a hand-copied list of machine-checkable facts is the
# COVERAGE rule's own counter-example.
try:
    import run_gates as _RG
    SELFTEST_GATES = frozenset(
        k for k, v in _RG.NOT_A_CORPUS_GATE.items() if v == ["--self-test"])
except Exception:                      # noqa: BLE001 - the map is advisory here
    SELFTEST_GATES = frozenset()

# HOW OLD IS THIS VERDICT? Twice on 2026-09-16 a row was wrong because it was OLD rather than
# badly taken: pass 22 asserted a zero from two days and several hundred commits earlier, and
# pass 29 was certified clean in the morning and broken by the afternoon from a peer publish.
# The measuring commit is already written in the note; nothing read it. A verdict past this
# many commits is MARKED, never downgraded - age is not a failure, and a file whose whole
# purpose is to refuse manufactured verdicts must not manufacture one here.
STALE_AFTER = 50
# IGNORECASE ADDED 2026-09-16 (OPUS), AFTER THIS LINE MISREPORTED A FRESH MEASUREMENT AS 37
# COMMITS OLD. A note written "RE-MEASURED AT HEAD 114558e9" did not match, so the search
# fell through to an older lowercase "at HEAD 342d12f9" preserved further down the SAME note
# and the row printed the age of the verdict it had just superseded - silently, with a
# plausible number. That is the failure this stamp exists to catch, committed by the stamp.
# The first match still wins: notes put the current measurement first and keep older ones
# below, which every note in this file already does.
AT_HEAD = re.compile(r"at HEAD ([0-9a-f]{6,40})", re.I)

# A COMMIT IS THE WRONG PROVENANCE FOR PASS 5 AND THE STAMP WAS ASKING FOR ONE. Pass 5 is
# parent reproducibility: its subject is the GZF and the checkpoint, which do not change when
# this repository commits, so a repo sha beside it would move for reasons having nothing to do
# with what it measures. Its note already names the GZF sha and the snapshot - STRONGER
# provenance than a commit - and the stamp was printing it as though it had none.
# KEPT NARROW ON PURPOSE: artefact provenance is accepted only for the passes listed here,
# because otherwise any row could dodge the commit stamp by writing "snapshot" and some hex.
# A pass whose subject is the corpus must name the commit it read.
ARTEFACT_PASSES = frozenset([5])
AT_ARTEFACT = re.compile(r"snapshot ([0-9a-f]{6,40})")


def verdict_age(note):
    """commits between the sha the note was measured at and current HEAD, or None."""
    m = AT_HEAD.search(note or "")
    if not m:
        return None
    try:
        r = subprocess.run(["git", "rev-list", "--count", m.group(1) + "..HEAD"],
                           capture_output=True, text=True, cwd=os.path.dirname(
                               os.path.dirname(os.path.dirname(os.path.dirname(
                                   os.path.dirname(os.path.abspath(__file__)))))))
        if r.returncode:
            return None
        return int(r.stdout.strip())
    except Exception:                  # noqa: BLE001 - age is advisory, never load-bearing
        return None


PASSES = {
    1:  ("Address existence",        ["verify_doc_addresses.py"]),
    2:  ("Body extent",              ["audit_crossrefs.py"]),
    3:  ("Body hash",                ["check_body_hashes.py"]),
    4:  ("Classification currency",  ["audit_crossrefs.py"]),
    5:  ("Parent reproducibility",   []),
    6:  ("Banned evidence sweep",    ["check_banned_evidence.py"]),
    7:  ("Tier presence",            ["check_tier_presence.py"]),
    8:  ("Tier inflation",           ["check_tier_inflation.py"]),
    9:  ("Killer observation",       ["check_absence_claims.py", "check_caller_claims.py",
                                      "check_novelty_claims.py"]),
    10: ("External isolation",       []),
    11: ("Ownership inheritance",    ["check_global_claims.py", "check_contract_globals.py"]),
    12: ("Layer separation",         ["check_layer_separation.py"]),   # see PER_PASS
    13: ("Independent re-derivation", []),
    14: ("Constants",                ["check_evidence_widths.py", "check_cited_site_widths.py"]),
    15: ("Struct offsets",           ["check_layout_units.py", "check_strided_fields.py"]),
    16: ("Enum namespace",           ["check_names.py"]),
    17: ("Data vs function",         ["verify_doc_addresses.py", "audit_crossrefs.py"]),
    18: ("Arithmetic",               ["check_denominators.py"]),
    19: ("Call chains (up)",         ["check_call_chains.py"]),
    20: ("Call chains (down)",       ["check_call_chains.py"]),
    21: ("Call chains (across)",     ["check_call_chains.py"]),
    22: ("Unaccounted neighbours",   ["audit_crossrefs.py"]),
    23: ("Do not confuse with",      ["check_uncompared_pairs.py", "check_instance_aliases.py"]),
    24: ("Propagation",              ["check_propagation.py"]),
    25: ("Script/EBP re-check",      ["check_script_catalog.py"]),
    26: ("Upstream source match",    ["check_upstream_markers.py"]),
    27: ("Naming",                   ["check_names.py", "check_named_not_cited.py"]),
    28: ("Contradiction sweep",      ["check_doc_claims.py", "check_consistency.py",
                                      "check_self_contradiction.py", "check_doc_self.py"]),
    29: ("Index and link integrity", ["check_links.py"]),
    30: ("Status honesty",           ["check_crossref_clean.py"]),
}


# HAS THIS PASS EVER BEEN RUN AND THE RESULT RECORDED? That is a different question from "does it
# have an instrument", and leaving it out nearly cost a re-run: pass 10 shows as "no instrument;
# hand pass" here, and it was executed by inspection on 2026-09-13 - all ~30 external references
# read, none load-bearing - and DELIBERATELY not mechanised, because at that volume an instrument
# is infrastructure for its own sake. A map that only counts tools says "unknown" about a pass
# somebody already finished.
#
# Sourced from dated addenda in FINAL-AUDIT-PROTOCOL.md and from the kit docstrings that name
# their pass. An entry here is a CITATION, not a pass mark: several record a finding rather than a
# clean result, and passes 20/21/23 record that they are deliberately not mechanisable.
EXECUTED = {
    3:  "check_body_hashes.py, this session; AUDIT-LOG entry owed (SWE2-DATA holds the file)",
    6:  "protocol addendum 2026-09-13 - instrument built, run as a diagnostic",
    7:  "protocol addendum 2026-09-13 - four rounds wrong before one real row",
    10: "protocol addendum 2026-09-13 - ~30 external refs READ; none load-bearing; not mechanised on purpose",
    12: "protocol addendum 2026-09-13 - ledger half full; CONFLATION/INVENTED/SHORTHAND classified",
    20: "protocol addendum 2026-09-13 + closure 2026-09-14 - index rule 5 restated (bb45974f)",
    21: "protocol addendum 2026-09-13 + closure 2026-09-14 - index rule 5 restated (bb45974f)",
    23: "protocol addendum 2026-09-13 - address half clean; completeness half not mechanisable",
    24: "protocol addendum 2026-09-13 - first real finding was that there was nothing to find",
    13: "hand pass 2026-09-14, two rounds: round 1 FAILED (2 document findings, corrected in c81510ed), round 2 clean over a fresh sample - AUDIT-PASS13-ROUND1/2.md",
    25: "hand run: 1,224 of 1,224 verbs identical; now re-runnable as check_script_catalog.py",
    26: "check_upstream_markers.py, this session; AUDIT-LOG entry owed",
}


# Instruments run BY HAND because run_gates cannot see them - it globs `check_*.py`, so
# `verify_doc_addresses.py` and `audit_crossrefs.py` are invisible to it despite serving five
# passes between them. Measured 2026-09-14 against the current graph; without these the map
# reports NO-STATE for passes 1, 2, 4, 17 and 22 and the largest failing pass in the protocol
# does not appear at all.
DIRECT = {
    "verify_doc_addresses.py": (0, "--all: 0 documents needing confirmation"),
    # PASS 9 HAD NO STATE AT ALL until 2026-09-14 - run_gates globs `check_*.py` and this file IS
    # named check_*, but it was absent from the baseline, so the map reported it "unknown, not
    # clean" rather than scoring it. Run by hand: its CONTROL passes (memcpy at 00861EBA -> 632
    # call sites, which is what makes an absence or an "exactly one" result meaningful at all),
    # and all 18 targets reconcile.
    #
    # READ THE DOCUMENTS, NOT THE TOOL'S OWN LABELS. The "claim under test" column is the tool
    # author's shorthand, and three rows read at first glance like documents conflating call SITES
    # with calling FUNCTIONS - "called from 108 sites" measuring 108 fns / 113 sites, "156 call
    # sites between them" measuring 156 fns / 231 sites. Every one of those documents states BOTH
    # numbers correctly in its own text ("113 sites in 108 distinct", "129 ... and 102 ..., 231
    # together"). The conflation was in the shorthand. A finding filed from the tool's summary
    # would have been wrong about three pages at once.
    "check_caller_claims.py": (0, "control passes (632 memcpy sites); 18 targets, all reconciling "
                                  "against calls / distinct functions / either plus jmp thunks; "
                                  "claims re-read in the documents themselves, not the tool's "
                                  "shorthand column"),
    # Re-measured 2026-09-14 against the GN161 re-exported graph (d070e4f6). Two things
    # moved and both are recorded: GHOST ADDRESS 1 -> 0 because 002FE7D0 is now reported as
    # UNLISTED CODE (see PER_PASS[17]), and UNACCOUNTED NEIGHBOUR 1,052 -> 1,057 because the
    # graph was re-exported from the certified parent. The neighbour rise is NEW DENOMINATOR
    # from a fresher graph, not a regression, and it is stated rather than absorbed.
    # 2026-09-14 12:35: ONE finding left, and it is the census debt already reclassified under
    # PER_PASS[17]. UNACCOUNTED NEIGHBOUR went 1,057 -> 0 over this session by reading and
    # dispositioning, with two deliberate rises on the way (R4 +124, two withdrawn clears +2).
    "audit_crossrefs.py": (1, "1 finding: BODY DRIFT 0, CLASSIFICATION 0, GHOST ADDRESS 0, "
                              "UNLISTED CODE 1 (census debt, registered), "
                              "UNACCOUNTED NEIGHBOUR 0"),
}


# ONE TOOL, FOUR PASSES, ONE EXIT CODE - and the exit code cannot say which pass failed.
# `audit_crossrefs` serves passes 2, 4, 17 and 22 and exits 1 if ANY finding exists, so scoring
# all four from it marks passes 2 and 4 as failing when their own finding kinds are empty. The
# per-kind counts are the per-pass verdicts, and they are what belongs here.
PER_PASS = {
    6:  (2, "PARTIAL - TO READ 33 AT HEAD 34e07aeb, AND THE INDEPENDENT-REVIEWER CHAIN HAS "
        "RUN ONCE END TO END. 597 files, 444 banned-term lines, split PATH 91, EXCLUDED 289, "
        "SUBJECT 23, REVIEW 41 - of which EIGHT now sit on pages with a REVIEWED "
        "disposition, so TO READ is 33. SWE2-AUDIT-SPEC signed the two rows FABLE declined: "
        "what-the-game-asks-windows-for.md and the-code-the-function-list-does-not-contain.md, "
        "the two pages whose residue is the only class where unwind metadata carries a STATED "
        "FIGURE. FABLE declined them because FABLE wrote the 2026-09-16 ruling those pages "
        "rest on; I re-routed rather than asking them to review their own ruling, and a third "
        "identity signed. THAT IS THE MECHANISM DOING THE THING IT WAS BUILT FOR, and it is "
        "worth recording because on its first contested use it caught a wrong verdict of mine "
        "(d824884c). EIGHTEEN ROWS REMAIN UNSIGNED and suppress nothing. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: PARTIAL - TO READ 41 AT A CLEAN HEAD, ALL 49 "
        "OF THEM READ WHEN THERE WERE 49, "
        "AND 20 PAGE DISPOSITIONS STANDING UNSIGNED. Measured 2026-09-18 by OPUS at HEAD "
        "a517e8e4, on a `git archive HEAD` export of that commit rather than on the working "
        "tree, which carried heavy uncommitted peer work: 596 files, 440 lines mentioning a "
        "banned term, split PATH 91, EXCLUDED 285, SUBJECT 23, REVIEW 41. "
        "THE LAST EIGHT MOVED BECAUSE OF A RULING OF MINE, NOT BECAUSE ANY PAGE CHANGED: "
        "4ea1472c added `bans`, `excl.` and `inadmissible` to EXCLUDE on "
        "FABLE-REQ-OPUS-PASS6-SIX-REFUSAL-WORDS-EXCLUDE-LACKS, and REFUSED `nothing`, `none` "
        "and `non-` - the last of which the request itself offered as narrow-safe, though it "
        "clears vtable-method-index 2640 (`non-funclet`, arithmetic rather than refusal) and "
        "clears unowned-code 729 only by coincidence of matching a SECTION-NAME negation. "
        "THAT CHANGE INVALIDATED SEVEN OF MY OWN ROWS AND THE REGISTRY REPORTED EVERY ONE: 4 "
        "LAPSED, 3 ORPHANED, none silent. Repaired in the same commit - four re-keyed with "
        "their reasons' line counts corrected, three retired with the reason recorded - and "
        "re-run clean of both states afterwards. "
        "THE EARLIER READINGS, KEPT BECAUSE THE SEQUENCE IS THE EVIDENCE: 49 at 8cd2a078 "
        "where all 49 were read by hand and 23 rows authored (f8c058f7), 49 again at "
        "6b7ced3f four commits later with an identical split and NO DISPOSITION LAPSED. "
        "SUBJECT 23, REVIEW 49 - TO READ 49 across 23 pages, down from the 142 this row carried at "
        "17f6c744. "
        "THE FALL IS NOT MINE AND SAYING SO IS THE POINT: most of it is FABLE's 2026-09-17 ruling "
        "widening the refusal test from the physical LINE to the PARAGRAPH - 146 per line, 98 per "
        "sentence, 48 per paragraph with one variable changed. EXCLUDED went 148 -> 277 because "
        "the instrument got better at seeing refusals, not because the corpus withdrew claims. "
        "ALL 49 WERE READ, against the page and - where a count or an identity was at stake - "
        "against the cited bodies. NONE RESTS A CLAIM ON .pdata OR UNWIND DATA, in three "
        "mechanisms: (1) the page REFUSES the evidence in a place the paragraph unit still cannot "
        "reach, such as a table header cell reading 'stored RVA (excl. all unwind data)', a "
        "section heading, or the tail of a refusal that wraps mid-list; (2) .pdata is the SUBJECT "
        "being measured - two PE section tables, the exception directory as the comparison "
        "population for the function list (35,713 records against 38,161 listed bodies), a census "
        "of where an RVA occurs at all before the .pdata hits are excluded; (3) 'unwind' as the "
        "ordinary verb or as the dump's `Unwind@` naming, with the claim resting on instruction "
        "bytes. THE TWO THAT NEEDED TRACING RATHER THAN READING: lazy-statics' 1,545 comes from "
        "the funclet BODIES - the intersection of header-site guards with the guard operands of "
        "the _Init_thread_abort funclets, which that page states at its own line 603 - and "
        "COVERAGE's array-element-destructor role for 0016D6A0 comes from the complete body of "
        "Unwind@0089dd0e passing it to _eh_vector_destructor_iterator. "
        "WHY THIS ROW IS STILL PARTIAL AND NOT CLEAN: the 23 rows published in f8c058f7 all carry "
        "an EMPTY reviewer column. dispositions.py refuses to apply a row whose reviewer is blank "
        "or equal to its author, so TO READ is still 49 and every one of those findings is live. "
        "Verified against the export with the new TSV in place: 23 reported as NOT APPLIED - no "
        "independent reviewer, TO READ unchanged at 49, nothing suppressed. That they reported as "
        "UNREVIEWED rather than not at all also proves every digest matches what the gate "
        "recomputes; a hand-typed hash would have matched nothing and been reported nowhere. "
        "Routed as OPUS-REQ-FABLE-PASS6-SIGN-OR-REFUSE-23-DISPOSITIONS. Marking this row clean on "
        "rows I authored and could sign myself is the blindfold the registry exists to prevent, "
        "and on its first contested use that rule caught a wrong verdict of mine (d824884c). "
        "STILL UNBUILT, AND NOBODY HAS CLAIMED IT: check_unwind_citations, the address sweep, does "
        "not consume the registry at all - SWE2-AUDIT-SPEC flagged that and it is unchanged. "
        "ONE NOTE FOR WHOEVER WRITES THE NEXT ROW IN THIS FILE: verdict_age dates an entry by the "
        "FIRST `at HEAD <sha>` in its text, so a new measurement phrased any other way is dated by "
        "the preserved history underneath it. This row printed '690 commits ago - RE-MEASURE' over "
        "a reading taken the same hour until the phrase was fixed. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: PARTIAL - TO READ 142, AND THIS ROW USED TO SAY CLEAN BY READING A DIAGNOSTIC'S EXIT "
        "CODE. Measured 2026-09-17 by OPUS in a clean detached worktree at HEAD 17f6c744. "
        "check_banned_evidence exits 0 and its OWN FIRST LINE reads 'pass 6 - banned evidence sweep "
        "(DIAGNOSTIC, not a gate pass)'. 584 files, 427 lines mentioning a banned term, split PATH "
        "92, EXCLUDED 148, SUBJECT 44, REVIEW 143 - and TO READ 142, which the tool itself labels "
        "'the only number that matters'. A pass with 142 unread REVIEW lines is not clean. "
        "WHAT THIS ROW WAS DOING WRONG, and it is OPUS's own row rather than a peer's: it recorded "
        "'clean check_banned_evidence.py=0' from the gate baseline, which reads the EXIT CODE of a "
        "tool that declares itself a diagnostic on its first line, and it carried NO measuring "
        "commit and no date. That is the ninth instrument caught in two days reporting exit 0 over "
        "an unfinished question - the same shape as check_experiments printing 5 findings and "
        "exiting 0, check_surface_figures printing 'SURFACE FIGURES STALE: 6' and exiting 0, and "
        "check_propagation's --self-test being read as a corpus verdict. "
        "WHAT IS GENUINELY ADJUDICATED AND IS NOT DISTURBED BY THIS: SWE2-AUDIT-SPEC's "
        "ACCEPT-WITH-NARROWING on the address sweep stands, and pass 6 MAY read clean ON THAT CLASS "
        "- 1,119 SCOPE_TABLE records cross-checked against FABLE's independent ehmap_sweep, 7 of 7 "
        "controls passing, real exit 1, and the 58 flagged lines resolved into 14 numeric or "
        "file-offset coincidences, 39 identifying-or-correcting, and 5 resting-but-admissible. "
        "FABLE separately ruled the two game-side `__try` ranges ADMISSIBLE and corroborated them "
        "against the instruction stream TO THE BYTE rather than granting a subject exemption, which "
        "is the stronger answer: an exemption makes the subject the excuse, corroboration is what "
        "would have caught a decoding error. The 142 is the BROADER review queue, not that class, "
        "and conflating them would be the same error pointing the other way. "
        "THE QUEUE REFILLS, WHICH IS THE PART THAT MATTERS FOR A STREAK: FINAL-AUDIT-PROTOCOL "
        "records OPUS having read all 115 REVIEW lines, and the corpus now presents 143. Like the "
        "four pass-29 waves in one day, this is a cadence problem rather than a backlog, and a row "
        "that says clean between refills is telling the truth about a moment nobody can locate. "
        "THE DISPOSITION REGISTRY IS WORKING HERE AND IS NOT WIRED EVERYWHERE: 1 finding is "
        "suppressed by a reviewed disposition (EXP-061-mp-writer-controls.md, FALSE-POSITIVE, "
        "authored by OPUS and reviewed by FABLE 2026-09-16), so the mechanism runs in production on "
        "this gate - while check_unwind_citations, the address sweep, does NOT consume the registry "
        "at all, which SWE2-AUDIT-SPEC flagged as unbuilt and nobody has claimed."),
    10: (0, "CLEAN AT HEAD a756d9a3 - THE HAND PASS REDONE RATHER THAN LEFT AS A NOTE. No instrument, "
        "deliberately not mechanised; OPUS swept the corpus's whole external surface instead. 590 "
        "markdown files, THREE distinct external hosts, 20 references: learn.microsoft.com 17, "
        "github.com 2, www.microsoft.com 1. BANNED-CLASS REFERENCES: ZERO - no wiki, fandom, "
        "gamefaqs, reddit, forum, steamcommunity, youtube or stackexchange host appears anywhere in "
        "the database, separated by host name rather than by impression. "
        "THE ALLOWED ONES ARE NOT AN EXCEPTION, THEY ARE TWO OTHER PASSES: learn.microsoft.com is "
        "the published contract of a Windows API the image calls, and github.com is upstream source "
        "for a third-party identification, which pass 26 positively REQUIRES. A checker flagging "
        "those would enforce the opposite of two passes at once. "
        "THE ONE NEEDING JUDGEMENT WAS READ: www.microsoft.com is an MSRC advisory on mandatory "
        "ASLR, cited in authored-reference-lifetime-evidence.md beside the MSDN process-policy "
        "structure - vendor platform documentation, and it supports a REFUSAL rather than a claim: "
        "'The header alone does not establish the effective process policy.' External documentation "
        "used to WITHHOLD a conclusion is the opposite of the banned class. The surface has shrunk "
        "from the roughly thirty references of the 2026-09-13 reading to 20 of the same composition. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "HAND PASS, SATISFIED ONCE ON 2026-09-13 AND NOT SINCE - PARTIAL, NOT CLEAN, AND THE CHANGE IS"
        "OPUS'S JUDGEMENT RATHER THAN A MEASUREMENT. This pass has NO INSTRUMENT and is not mechanised on"
        "purpose: the recorded run read about thirty external references and found none load-bearing. That"
        "reading was true of the corpus on 2026-09-13. It names NO COMMIT, so nothing can place it against"
        "any HEAD since, and the corpus has taken several hundred commits in the meantime. WHY IT NO LONGER"
        "PRINTS GREEN: it was scoring clean off the EXECUTED record - a note that a hand run happened - and"
        "a green cell for a hand pass nobody has redone is exactly the shape this table was built to stop."
        "Section 11.4 requires every pass re-satisfied PER RUN. A hand pass is not exempt from that; it is"
        "the pass for which it is HARDEST to satisfy, because nothing fails automatically when it goes"
        "stale. WHAT WOULD MAKE IT GREEN AGAIN: the same reading, redone at a named HEAD, with the count of"
        "external references and the load-bearing verdict recorded here. It is cheap and nobody has claimed"
        "it."),
    13: (2, "PARTIAL - ROUND 3 FOUND 2 DIFFERENCES IN 4, AND THE OFF-BY-TERMINATOR FAMILY IS "
        "NOW FOUR INSTANCES DEEP. Run at HEAD 1022bd2b with the sampler flaw round 2 exposed FIXED "
        "- the draw now comes from `git ls-files`, so it cannot pick untracked scratch. "
        "TWO OF SIX WERE DISCARDED AS CONTAMINATED, and the reason is a real limit on this pass in "
        "a long session: 00379D60's row had been read while investigating pass-29 links and "
        "002EF7C0's in a commit diff. The exclusion list covered pages OPUS had EDITED, not pages "
        "it had incidentally READ. Blindness erodes as a session runs, and a round that does not "
        "account for that is scoring itself. Four stood. "
        "TWO MATCHED: 00638C90 (TLS via gs:[0x58], index [02EAED3C], slot+4 - the page is more "
        "complete than the 0x48 bytes read, which is not a differing reading) and 00582FC0 (the "
        "+0x100/+0x108 releases and the +0xC1-gated free). "
        "TWO DIFFERED. 0017D240: the page said 18 B, the body ends on the `ret` at 0017D252 with "
        "padding at 0017D253, so it is 19 - and the ledger agrees at 19. THAT IS THE FOURTH "
        "OFF-BY-TERMINATOR SIZE, after 003333D0's 29, 00236A40's 23 and 0033F020's 39. Four "
        "independent pages producing the same off-by-one is a producer, not four slips. "
        "002508E0: the page said `00248030` x3 on three globals. The first call is GATED - "
        "`cmp qword [rcx+0x18], 0` / `je` at 002508F0/002508F5 - so it is two unconditional and "
        "one conditional. THE PAGE'S OWN ANCHOR CITES 002508F0, the gate instruction itself, so "
        "the author was looking at it and still wrote x3. Both repaired here; both pages were "
        "clean, unlike round 2's subject. "
        "ROUND 3 FAILS TOO, and the trend is the point rather than the verdict: 7 of 7, then 1 of "
        "5, now 2 of 4. This pass has produced a real defect in every round anyone has run it. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "PARTIAL - ROUND 2 RAN AT HEAD 8eb25b1f AND FOUND 1 DIFFERENCE IN 5, SO IT FAILS "
        "TOO - but 1 in 5 against round 1's 7 in 7 is the corpus getting better, not the pass "
        "getting easier. METHOD, built to enforce the blindness rather than trust it: a sampler "
        "drew rows stating an address, a size and a one-line behaviour, EXCLUDING every page this "
        "session edited and round 1's seven subjects, printed ONLY the addresses, and sealed the "
        "pages' claims to a file unread until the derivations existed. A sample chosen by reading "
        "is a sample chosen to pass. "
        "ONE OF THE SIX WAS DISCARDED BY OPUS AS CONTAMINATED: 003DC240's claim had been read "
        "earlier the same day while reviewing the pass-22 crossings section, so it was not blind "
        "and is not counted. Five stood. "
        "FOUR MATCHED: 001D70D0 (two gates selecting one of two .rdata floats), 0017E720 (bool-"
        "normalise then forward to a singleton setter), 002EB780 (call with second argument 0, "
        "return 1 unconditionally), 005372D0 (resolve through 0020E600 then a bounded test) - the "
        "last being thinner on the page than in the bytes, which is less detail rather than a "
        "differing reading. "
        "ONE DIFFERED, AND IT IS A DIFFERENT FUNCTION RATHER THAN A WORDING QUIBBLE. "
        "battle-runtime-mode-ladder.md:942 calls 00304790's `xmm1 = 2.0f` a DEFAULT. The bytes are "
        "`movss xmm1, [01CEBC08]` - whose dword is 0x40000000 = 2.0f, so the VALUE is right - "
        "followed by `maxss xmm1, xmm0`, which takes the LARGER of the constant and the argument. "
        "That is a FLOOR applied on every call, not a default applied when none was supplied; a "
        "reimplementer writing `if (!arg) arg = 2.0f` diverges on every argument below 2.0. "
        "THE SIBLING ROW PROVES THE READING CANNOT BE DONE BY COMPARISON: row 943 calls 003047C0 "
        "'same shape, no default load', when what it actually does is `movaps xmm1, xmm0` - pass "
        "the argument through UNCLAMPED. Both cells are consistently wrong about the same verb, so "
        "reading them against each other can never find it. Only the bytes do. Routed as "
        "OPUS-REQ-FRONTIER-LADDER-MAXSS-IS-A-FLOOR-NOT-A-DEFAULT-TWO-ROWS; not edited here because "
        "that page is dirty in the working tree with FRONTIER mid-edit. "
        "A FLAW IN OPUS'S OWN SAMPLER, RECORDED SO THE NEXT ROUND FIXES IT: the draw did not "
        "restrict itself to TRACKED files and picked ladder_head.md, which is untracked scratch. "
        "The finding survives only because the same row exists on the tracked page - it was "
        "checked, not assumed. A sample that can draw from unpublished files is not sampling the "
        "corpus. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "PARTIAL - A ROUND RAN AT HEAD a756d9a3 AND IT FAILED, WHICH IS THE HONEST RESULT. Pass "
        "13 is 're-derive each mechanism from the body WITHOUT READING THE DOCUMENT, then compare; "
        "fails if the independent reading differs.' THE ROUND: seven function extents were computed "
        "from the shipping image - disassembled to the terminator with the following byte checked "
        "for int3 padding - and only then compared with what the pages said. ALL SEVEN DIFFERED: "
        "001E71B0 717 against 507, 00236A40 28 against 23, 002E5180 506 against 96, 003333D0 30 "
        "against 29, 0033F020 43 against 39, 003DAC70 131 against 438, 00424D80 1607 against 1588. "
        "Every one corrected in a756d9a3. "
        "SEVEN OF SEVEN IS A FAILED ROUND AND THIS ROW SAYS SO. Under the pass's own criterion a "
        "round where every sampled mechanism differed is a failure, not a success with repairs "
        "attached. The 2026-09-14 pass had the same shape - round 1 failed with 2 findings, "
        "corrected in c81510ed, and only a round 2 over a FRESH sample came back clean. That second "
        "round has not been run, and this row will not print clean until one does. "
        "HONEST ABOUT THE BLINDNESS, because that is where this pass's power lives: the extents were "
        "derived independently of the pages' stated numbers. In two OTHER re-derivations today - the "
        "status-write contract and the battle-unit +0x58 consumer - a peer's FINDING was in hand "
        "while the derivation ran, and although the documents were not the source that is a weaker "
        "blindness, so those are NOT counted in this round. "
        "WHAT IT BOUGHT: three of the seven share one cause - 23 and 39 stop immediately before a "
        "five-byte tail jmp, 29 excludes the one-byte ret - a defect in whatever produced the "
        "numbers rather than seven independent slips, and no amount of reading the pages against "
        "each other would have found it. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "HAND PASS, TWO ROUNDS ON 2026-09-14, NOT REDONE SINCE - PARTIAL for the same reason as pass"
        "10. No instrument. The recorded run is worth keeping because it is the best evidence in this table"
        "that hand passes CAN fail: ROUND 1 FAILED with 2 document findings, they were corrected in"
        "c81510ed, and round 2 came back clean over a fresh sample. THE COMMIT NAMED IS THE REPAIR, NOT THE"
        "MEASUREMENT. c81510ed is where round 1's findings were fixed; the clean round-2 reading names no"
        "HEAD of its own, so this row cannot be placed in time either, and writing c81510ed into the age"
        "stamp would be dating a verdict by a commit it was not taken at. That distinction is the whole"
        "subject of this table today. THAT ROUND 1 FAILED IS THE ARGUMENT AGAINST LEAVING IT GREEN: an"
        "independent re-derivation that found two real defects the first time it was attempted is not a"
        "pass that stays true by itself for three hundred commits."),
    # ------------------------------------------------------------------------------------------
    # THE UNDATED TWENTY, DATED 2026-09-17 (OPUS) AT HEAD 267baccd.
    #
    # Until today these twenty carried NO PER_PASS entry at all. They printed `clean tool.py=0`
    # off the gate baseline - no HEAD, no date, no instrument detail - and the provenance block
    # below the table counted them as NAME NO MEASURING COMMIT AT ALL. An undated verdict is
    # WEAKER than a stale one: a stale one can be dated and re-run, an undated one cannot even be
    # interrogated, and section 11.4's per-run re-satisfaction cannot be claimed for a row that
    # cannot be placed in time.
    #
    # HOW THEY WERE MEASURED, because the method is the only thing that makes these entries worth
    # more than the bare baseline they replace: run_gates.py --db in a CLEAN DETACHED WORKTREE at
    # HEAD 267baccd, with the machine-local inputs the corpus does not track - the shipping image,
    # the graph exports and the GFZ ledger - JUNCTIONED into the worktree. That matters: the same
    # suite run in a bare worktree reported 10 CRASHes and 10 CANNOT-RUNs, and every one of those
    # was a missing untracked input rather than a corpus defect. Reporting them as findings would
    # have been the session's ninth instance of real evidence about the wrong population.
    #
    # TWO CORRECTIONS OPUS MADE TO ITS OWN READING OF THAT RUN, both caught before anything was
    # written down. (1) run_gates prints ONLY checkers that MOVED since the baseline, so a checker
    # absent from its report has its BASELINE value - the first mapping read absence as "did not
    # run" and wrongly disqualified eight passes. (2) The NOT RUN block is real and must not be
    # read as silence-equals-pass: check_caller_claims serves pass 9 and did not run at all.
    1:  (0, "RE-MEASURED AT HEAD 5cf96b34 (OPUS) in a clean detached worktree: verify_doc_addresses.py --db --all --quiet, exit 0 over 385 document(s) - 31,696 entry, 29,652 interior, 368 text-data, 28 range-bound, 8,038 data, 289 literal, 6 unwind-BANNED, and 25 document(s) with .text non-function citations to confirm. THE TWO NON-ZERO CLASSES MOVED SINCE THIS ROW WAS LAST WRITTEN, 17 -> 25 to confirm and 5 -> 6 unwind-BANNED, so the exit code carried a change the row would not have shown. This instrument is still one run_gates NEVER SEES - the runner enumerates check_*.py only. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd, AND ITS INSTRUMENT IS ONE run_gates NEVER SEES. "
        "verify_doc_addresses.py --db --all --quiet in a clean detached worktree: exit 0. "
        "run_gates enumerates `check_*.py` only, so this checker - the sole instrument pass 1 names "
        "- is outside the suite entirely and outside the gate baseline. That is why this row could "
        "never be dated from the baseline, and it is a gap in the RUNNER rather than in the pass. "
        "NOT A BARE ZERO: the run also reports 17 document(s) with .text non-function citations to "
        "confirm, and 5 unwind-BANNED citations, alongside 7,279 data and 275 literal. The exit "
        "code does not carry those, so they are recorded here rather than left to a future reader "
        "of a green cell."),
    3:  (0, "RE-MEASURED AT HEAD 2aae130d (OPUS) in a clean detached worktree with the graph and image copied in: check_body_hashes.py exit 0, 'no mismatch: every citation that can be recomputed reproduces, head and tail.' THE QUALIFIER IS STILL THE BOUNDARY - a citation that CANNOT be recomputed is not evidence of agreement. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd. check_body_hashes.py in the suite: 'no mismatch: every citation "
        "that can be recomputed reproduces, head and tail.' The qualifier is the interesting part "
        "and is the pass's own boundary - a citation that CANNOT be recomputed is not evidence of "
        "agreement, and this row should not be read as covering those."),
    7:  (0, "RE-MEASURED AT HEAD 2aae130d (OPUS) in a clean detached worktree: check_tier_presence.py exit 0. The checker still states its own limit - a tier is STATED here, never deserved - so this row asserts presence and pass 8 attacks the value. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd. check_tier_presence.py: exit 0. The checker states its own "
        "limit - 'No tier VALUE is judged here, and PROVEN is as much a stated tier as 1' - so this "
        "row asserts that a tier is STATED, never that it is deserved. Pass 8 is the one that "
        "attacks the value."),
    8:  (0, "RE-MEASURED AT HEAD 2aae130d (OPUS) in a clean detached worktree: check_tier_inflation.py exit 0, and its own output repeats that the judgement it supports 'is the reading pass 8 asks for and is not mechanical'. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd. check_tier_inflation.py: exit 0, and it says in its own output "
        "that the judgement it supports 'is the reading pass 8 asks for and is not mechanical'. A "
        "green cell here means the mechanised half found nothing, not that the reading was done."),
    9:  (2, "PARTIAL AT HEAD 267baccd - ITS MAIN INSTRUMENT DID NOT RUN, AND WHEN RUN BY HAND IT "
        "DISAGREES WITH THE CORPUS IN A UNIT IT DOES NOT SHARE. check_absence_claims and "
        "check_novelty_claims exit 0; check_caller_claims.py is in run_gates' own NOT RUN list "
        "('needs a target or a prepared input'), which that list exists to stop being read as a "
        "pass. OPUS ran it directly with --db, --funcs and --exe: exit 0, control passing (00861EBA "
        "memcpy, 632 sites), 18-claim fixture running - AND 12 DISAGREEMENTS PRINTED UNDER AN EXIT "
        "OF 0. "
        "MOST OF THEM LOOK LIKE THE INSTRUMENT, NOT THE CORPUS, AND THE CLEAREST IS DECISIVE: two "
        "documents state '00633240 has zero call sites. Every one of its 703 references is a tail "
        "jump.' The sweep reports measured 703 incl-EH - THE DOCUMENT'S OWN NUMBER. The page is "
        "drawing exactly the distinction the comparison drops, in the same sentence. Two more "
        "absence claims (001D1660, 002EF570) sit beside lines reading 'reached by a single E9 tail "
        "call'. A separate unit confusion runs alongside: 002432B0 is scored stated-108 against "
        "measured-113 while the checker's OWN fixture records \"page said 108 sites; 108 fns / 113 "
        "sites\". "
        "Routed as OPUS-REQ-EC7-CALLER-CLAIMS-COUNTS-TAIL-JUMPS-AS-CALLS-AND-SITES-AS-FUNCTIONS. "
        "OPUS did NOT edit the pages: three of them are the CAREFUL ones, saying 'zero call sites' "
        "and then immediately saying what the 703 references are, and editing them to satisfy the "
        "comparison would trade accuracy for a green cell. The five remaining disagreements are "
        "deliberately UNRULED until the units are aligned."),
    11: (0, "RE-MEASURED AT HEAD 2aae130d (OPUS) in a clean detached worktree: check_global_claims.py exit 0 with 'With the control passing, that is a real negative', and check_contract_globals.py exit 0 reporting its control - '3 visible writer(s): 001E04B4, 001E04CB, 001E0610'. BOTH ZEROES CARRY A PASSING CONTROL, which is the difference between a real negative and an instrument that reached nothing. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd. check_global_claims.py and check_contract_globals.py both exit "
        "0, and the second reports a PASSING CONTROL - '3 visible writer(s): 001E04B4, 001E04CB, "
        "001E0610' - so its zero is a real negative rather than an instrument that reached nothing. "
        "In the bare worktree this same checker said 'image or function graph missing'; it is green "
        "here only because the image and graph were junctioned in."),
    14: (0, "RE-MEASURED AT HEAD 2aae130d (OPUS) in a clean detached worktree: check_evidence_widths.py and check_cited_site_widths.py both exit 0, the second printing its NEGATIVE CONTROL beside the result - 'CONTROL, same probe at a neighbouring aligned displacement: 9'. A width check without that control cannot tell 'the cited widths are right' from 'the probe matched nothing'. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd. check_evidence_widths.py and check_cited_site_widths.py both "
        "exit 0, the latter with its NEGATIVE CONTROL reported beside the result - 'CONTROL, same "
        "probe at a neighbouring aligned displacement: 6'. A width check without that control "
        "cannot distinguish 'the cited widths are right' from 'the probe matched nothing'."),
    15: (0, "CLEAN AT HEAD 5cf96b34 - AND THIS TIME WITH THE CONTROL THE INSTRUMENT ITSELF DEMANDS. check_layout_units.py --db prints 'no suspect layout strides found' and, unprompted, 'run --self-test to confirm the check still fires; a clean run from a broken parser is worthless'; that self-test was run and reports 'ok: 2 hits on the index-as-offset block, 0 on the real layout'. check_strided_fields.py --db exit 0 over a control of 381 indexed memory accesses: 10 declared scalars indexed at a non-size stride, ALL TEN already explained as array elements in the field's own meaning cell, 3 nested type interiors indexed as expected, and its own negative control passes - 'clearing one meaning cell returns its row to the unexplained list'. THE PREVIOUS ROW RESTED ON AGREEMENT WITH THE GATE BASELINE; this one rests on both instruments' printed output. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd. check_strided_fields.py exits 0 and check_layout_units.py "
        "agrees with the baseline at 0. check_strided_fields prints its own warning with the pass: "
        "'UNEXPLAINED - not because nothing was found. A new stride with a silent row fails again.' "
        "That is the correct reading of this row - it holds for the strides that exist today."),
    16: (0, "CLEAN AT HEAD 5cf96b34 - RE-MEASURED (OPUS) in a clean detached worktree: check_names.py --db exit 0, 602 markdown files scanned, 4,668 distinct name-shaped tokens quoted, 916 verified against the ledger, 185 legitimate shorthand, and TRUNCATED 0 - the defect class. The other 3,500 lines are an inventory of tokens the ledger cannot confirm (asset and script names), which the tool lists rather than judges. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 6662e859 - RE-MEASURED AFTER THE REPAIR LANDED, WHICH IS THE HALF THE "
        "row promised and the half that usually never happens. check_names.py --db in a clean "
        "detached worktree: exit 0, TRUNCATED 0, 4,478 name-shaped tokens over 589 files. "
        "WHAT THIS ROW SAID WHEN IT WAS RED, PRESERVED: "
        "RED AT HEAD 267baccd, AND REPAIRED IN THE COMMIT THAT CARRIES THIS ROW. check_names.py "
        "exit 1. Its exit is driven by ONE bucket - `return 1 if trunc else 0` - so the 3,393 names "
        "listed as NOT IN THE LEDGER are a judge-each diagnostic and not what fails it. The four "
        "TRUNCATED names are: ActorResource_OnDefinitionPayload, "
        "Inventory_QueryOwnedCountIncludingReserved, PartyControl_ApplyAnalogLocomotion and "
        "PresentationAuthoredCommand_Class04_Dispatch, each a strict prefix of EXACTLY ONE ledger "
        "name, so the completion is determined rather than chosen. Seven occurrences across five "
        "documents completed; one was a display ellipsis. check_names now exits 0 with TRUNCATED 0. "
        "THE ROW IS PUBLISHED RED BECAUSE THAT IS WHAT 267baccd MEASURED: marking it clean on the "
        "strength of its own pending repair is the error pass 29 recorded today."),
    18: (0, "CLEAN AT HEAD 5cf96b34 - RE-MEASURED (OPUS) in a clean detached worktree: check_denominators.py --db exit 0, 'no percentage relies on an undeclared certified population', over a stated population of every .md under the database root EXCLUDING 33 in _inbox/ and 1 append-only log. The exclusion is printed by the tool and is recorded here because a denominator check that does not say what it counted is the thing this pass exists to catch. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 6662e859 - RE-MEASURED AFTER THE REPAIR LANDED. check_denominators.py "
        "--db in a clean detached worktree: exit 0, 'no percentage relies on an undeclared "
        "certified population'. "
        "WHAT THIS ROW SAID WHEN IT WAS RED, PRESERVED: "
        "RED AT HEAD 267baccd, AND REPAIRED IN THE COMMIT THAT CARRIES THIS ROW. "
        "check_denominators.py exit 1: one undeclared denominator, PROGRAM-STATE.md line 6202, "
        "'20,802 explained (60.70%)'. A bare percentage leaves the reader to guess whether the base "
        "is the 38,161 ledger functions or something narrower, and those two readings differ by "
        "more than five points - which is exactly how '70.4 % of the executable' once meant 63.2 %. "
        "The line now names 34,270 non-funclet functions, 38,161 less the 3,891 Unwind@/Catch_All@ "
        "funclets, and the checker reports 'no percentage relies on an undeclared certified "
        "population'."),
    19: (2, "PARTIAL AT HEAD 5cf96b34 (OPUS) - THE INSTRUMENT IS AN INSTRUMENT FOR PASS 29. This row, and passes 20 and 21 with it, has been clean on check_call_chains.py, whose own header opens 'check_call_chains.py - the one index FINAL-AUDIT pass 29 names that nothing tests' and whose WHAT IS TESTED section lists three things: that every row's Document link points at a file that exists, that every row either links a document or defers to the previous row, and how many rows claim a crossing. PASS 19 IS CHAIN RE-DERIVATION - rebuild every call chain from a freshly regenerated call graph, failing if any chain has gained or lost an edge - and nothing in that tool regenerates a graph or compares an edge. The run is real and its result is real: exit 0, 46 rows parsed, 43 links resolve, 3 defer, 0 broken, 0 documents in a call-chains/ directory missing from the index, total mechanical defects 0. It is simply not this pass. The previous row already recorded that 19, 20 and 21 are one measurement and not three; what it did not record is that the measurement belongs to a different pass. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd. check_call_chains.py agrees with the baseline at 0. Passes 19, "
        "20 and 21 all rest on THIS ONE INSTRUMENT, so they share a single point of failure and "
        "their three green cells are one measurement, not three."),
    20: (2, "PARTIAL AT HEAD 5cf96b34 (OPUS) - AND THE TOOL SAYS THIS ONE IN SO MANY WORDS. Pass 20 is BIDIRECTIONALITY: every chain states upstream and downstream, failing if either direction is missing. check_call_chains.py prints, in its own WHAT IS DELIBERATELY NOT TESTED section and again in its output, 'the header's documented in both directions claim is NOT TESTED here - owner labels are CodeDomain names no page writes as one token, so a text test reports false one-sidedness. It needs a label -> owner mapping the corpus does not publish', and records that an earlier version reported 13 of 35 crossings one-sided and all 13 were the test rather than the corpus. 35 OF THE 46 ROWS CLAIM A CROSSING AND NONE OF THE 35 IS CHECKED IN BOTH DIRECTIONS. The zero this row rested on is index integrity, which is pass 29's subject. THE MISSING PIECE IS NAMED AND IS WORK, NOT WORDING: a label-to-owner mapping the corpus does not publish. See pass 19. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd, on check_call_chains.py - the same single run that carries "
        "passes 19 and 21. See pass 19."),
    21: (2, "PARTIAL AT HEAD 5cf96b34 (OPUS) - NOTHING HAS EVER MEASURED THIS PASS. Pass 21 is OWNER TRANSITION VERSUS TRIGGER: each chain marks which transitions are authority and which are triggers, failing if any is mislabelled or unlabelled. check_call_chains.py - the only instrument this row names, and an instrument written for pass 29 - counts how many rows claim a crossing and does not read a single authority or trigger label. There is no mislabelled-or-unlabelled test anywhere in the kit. The run is clean for what it does measure and carries nothing about this. See pass 19. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd, on check_call_chains.py - the same single run that carries "
        "passes 19 and 20. See pass 19."),
    23: (0, "CLEAN AT HEAD 267baccd. check_uncompared_pairs.py and check_instance_aliases.py both "
        "agree with the baseline at 0."),
    25: (0, "CLEAN AT HEAD 5cf96b34 - RE-MEASURED (OPUS) in a clean detached worktree, on printed output rather than on baseline agreement: check_script_catalog.py --db exit 0, bundled catalog 1,954 entries against the database side file's 1,224 rows, and VERBS IDENTICAL IN NAME AND ARG COUNT 1,224 OF 1,224. The 730 in the catalog and not in the database are expected - the database documents the image's 1,224-record dispatch table while the catalog is an authored community list - and the failing direction, database ids absent from the catalog, is 0. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd. check_script_catalog.py agrees with the baseline at 0, and the "
        "pass's hand run is recorded separately: 1,224 of 1,224 verbs identical, now re-runnable "
        "through this checker rather than by hand."),
    26: (0, "CLEAN AT HEAD 5cf96b34 - RE-MEASURED (OPUS) in a clean detached worktree against the shipping image: check_upstream_markers.py --db exit 0, each third-party identification CONFIRMED by upstream's own strings quoted back - zlib 1.2.11 on 'deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler', Lua 5.2.1 on its $LuaVersion banner, and so on down the inventory. A version CONFIRMED against a string the vendor shipped is the only form of this pass that means anything. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 267baccd, AND IT WAS ABSTAINING AN HOUR EARLIER. check_upstream_markers."
        "py agrees with the baseline at 0 in this run. In the SAME worktree WITHOUT the junctioned "
        "image it printed 'pass 26: no image at Database\\Tools\\work\\exe\\FFXII_TZA.exe - "
        "ABSTAINING' and exited 3. The pass is green on the strength of an UNTRACKED machine-local "
        "artifact, so a peer on another machine cannot reproduce this row - that is a real limit on "
        "this verdict and it is recorded rather than hidden behind the colour."),
    27: (0, "CLEAN AT HEAD 5cf96b34 - RE-MEASURED (OPUS) in a clean detached worktree: check_names.py --db exit 0 with TRUNCATED 0 over 4,668 quoted name-shaped tokens, and check_named_not_cited.py --db exit 0. THE SECOND TOOL'S NUMBER IS NOT A DEFECT COUNT AND THE ROW SAYS SO: 2,013 mentions across 282 documents, 57 of them AMBIGUOUS, which the tool itself labels 'suspicions, not defects - a passing reference needs no anchor', and warns against bulk anchoring because 'an address supplied from a name lookup is a TRANSCRIPTION, not a citation'. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 6662e859 - RE-MEASURED AFTER THE REPAIR LANDED. check_names.py exit 0 "
        "with TRUNCATED 0, check_named_not_cited.py exit 0. "
        "WHAT THIS ROW SAID WHEN IT WAS RED, PRESERVED: "
        "RED AT HEAD 267baccd, AND REPAIRED IN THE COMMIT THAT CARRIES THIS ROW - the same "
        "check_names.py failure as pass 16, which is the other pass that instrument serves. See "
        "pass 16 for the four truncated names and their completions. check_named_not_cited.py "
        "exits 0."),
    28: (0, "CLEAN - ALL SEVEN SIZE DISAGREEMENTS RESOLVED FROM THE SHIPPING IMAGE, NOT FROM THE CENSUS. check_consistency, check_doc_claims, check_self_contradiction and check_doc_self all exit 0; check_consistency prints 'consistent: no address is described two different ways'. EACH EXTENT WAS READ TO ITS TERMINATOR AND CHECKED THAT THE NEXT BYTE IS int3 PADDING, so the number comes from the bytes rather than from deferring to the ledger: 001E71B0 = 717 (ends 001E747C ret), 00236A40 = 28 (ends 00236A57 jmp 00237CA0), 002E5180 = 506 (ends 002E5379 ret), 003333D0 = 30 (ends 003333ED ret), 0033F020 = 43 (ends 0033F046 jmp 00473210), 003DAC70 = 131 (ends 003DACF2 ret), 00424D80 = 1607 (ends 004253C6 ret). THREE OF THE SEVEN SHARE ONE CAUSE AND NAMING IT IS WORTH MORE THAN THE SEVEN FIXES: 23 for 00236A40 and 39 for 0033F020 both stop immediately BEFORE a five-byte tail `jmp`, and 29 for 003333D0 excludes the one-byte `ret`. A counter that treats the terminator as outside the body produces exactly those three numbers. THE OTHER FOUR ARE NOT THAT SHAPE - 96 against 506 and 438 against 131 are not off-by-a-terminator, and 003DAC70 is the one case where the page claimed MORE than the body holds. THE EARLIER CAUTION WAS RIGHT TO EXIST AND WAS DISCHARGED CASE BY CASE: a smaller cited extent is sometimes a deliberate partial reading, so each sentence was read before editing. All seven turned out to be whole-body claims in the form `ADDR` (N B), and the one site that had looked like a counter-example - 00236A40 cited elsewhere as a jump thunk - states its own extent in a separate sentence that was checked independently. check_doc_claims's single unruled cross-document claim was also adjudicated: as7-menu-graphics-containers.md -> the-menu-screen-atlas.md, term 002CF440, verdict OWN-EVIDENCE, read against BOTH documents - the target carries only a `| silhouette | 1 |` element tally while the citing page states the address on its own authority. The gate's control passes: dropping a registry row resurfaces its claim, so the suppression is keyed to the registry and not unconditional. WHAT THIS ROW SAID WHEN IT WAS RED, PRESERVED: RED AT HEAD 267baccd, AND NOT REPAIRED HERE. Two of its four instruments are non-zero: "
        "check_consistency.py reports 7 SIZE disagreements over 384 documents (NAME 0, CALLER-COUNT "
        "0, frontmatter gaps 0, duplicate keys 0), and check_doc_claims.py exits 1. "
        "check_self_contradiction.py and check_doc_self.py both exit 0. "
        "THE SEVEN ARE ADDRESSES WHOSE STATED BYTE EXTENT DIFFERS BETWEEN TWO DOCUMENTS, and the "
        "ledger decides every one of them: 001E71B0 is 717 (not 507), 00236A40 is 28 (not 23), "
        "002E5180 is 506 (not 96), 003333D0 is 30 (not 29), 0033F020 is 43 (not 39), 003DAC70 is "
        "131 (not 438), 00424D80 is 1607 (not 1588). NO CASE IS ONE WHERE NEITHER DOCUMENT MATCHES, "
        "which is what would have made this hard. "
        "OPUS DELIBERATELY DID NOT REWRITE THE SEVEN SMALLER FIGURES. A smaller cited extent is "
        "sometimes a deliberate PARTIAL reading - an interior run, an entry-only extent, or a body "
        "'complete for its field reads' - and this corpus distinguishes those on purpose. One "
        "inspected site already shows the hazard: 00236A40's page cites it as a JUMP THUNK reached "
        "from 00237CA0, not as a whole body. Overwriting seven numbers from a census without "
        "reading what each sentence claims would trade seven true statements for a green cell, "
        "which is the trade this row exists to refuse."),
    24: (0, "SURVIVOR 0 - AND THE MECHANISM CLOSED IT THE WAY THE GOAL SPECIFIES, WITH TWO "
        "IDENTITIES. check_propagation at HEAD: SURVIVOR 0, 8 findings suppressed by a reviewed "
        "disposition, up from 7. "
        "SWE2-FRONTIER AUTHORED THE EIGHTH ROW in answer to the routed request, leaving the "
        "reviewer field EMPTY - which does not suppress anything: Registry.state returns "
        "UNREVIEWED and the gate reports it. OPUS then SIGNED IT AS REVIEWER, which the rule "
        "permits because the rule is reviewer != author. OPUS had earlier routed the whole row "
        "away on the grounds that it had verified the count; that conflated AUTHORING with "
        "REVIEWING and left the pass waiting on somebody to redo a reading that was already done. "
        "THE REVIEW CHECKED THE ONE THING THE AUTHOR COULD NOT. OPUS had edited two member rows "
        "of that very section hours earlier - 003333D0 29 B -> 30 and 0033F020 39 B -> 43 - so "
        "the live risk was that the disposition had LAPSED against changed evidence. It had not: "
        "the span is the heading phrase, and the digest recomputes to 006bd8828690a037, matching "
        "the row. Re-verified independently of the author at HEAD: the heading binds 001EDDC0, "
        "names 00582860 nowhere on its line, and the section lists exactly 10 member rows. "
        "THIS IS PASS 24 DOING ITS JOB: seven findings stayed suppressed across the whole session "
        "without re-adjudication, the eighth surfaced the moment a new page used the phrase, and "
        "closing it took an author and a different reviewer. "
        "WHAT THIS ROW SAID WHILE RED, PRESERVED: SURVIVOR 1 - REGRESSED AT HEAD 6662e859. Re-measured 2026-09-17 (OPUS) in a clean detached worktree with --db and --board: 243 contradiction tasks, 112 carrying a quoted span, QUOTED 20, DATED 6, SURVIVOR 1, and 7 findings still suppressed by reviewed dispositions. THE SURVIVOR IS A KNOWN FALSE-POSITIVE CLASS IN A NEW PAGE, NOT A NEW DEFECT: AUDITSEM-CONTRA-FRONTIER-582860-238A30 matched 00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md:298, the phrase 'exclusive subtree - all 10 members bound'. The overturned claim was 00582860's exclusivity of 00238A30; THIS heading binds a DIFFERENT root, 001EDDC0, and asserts that section's own count. VERIFIED BEFORE SAYING SO: the 001EDDC0 section lists EXACTLY 10 member rows, counted at HEAD. That is the identical reasoning behind the five dispositions SWE2-FRONTIER authored and FABLE reviewed for the same contradiction on 2026-09-16. OPUS DID NOT AUTHOR THE DISPOSITION ITSELF. The mechanism requires reviewer != author, the five precedents are FRONTIER-authored and FABLE-reviewed, and the stock heading is FRONTIER's own phrasing - so it is routed rather than self-signed. THE MECHANISM IS WORKING EXACTLY AS PASS 24 ASKS: seven findings stay suppressed without re-adjudication, and the eighth surfaced the moment a new page used the phrase. WHAT THIS ROW SAID BEFORE, PRESERVED: SURVIVOR 0, RE-MEASURED AT HEAD 114558e9 on 2026-09-16 (OPUS) with --db and --board, 37 commits later: no document repeats an overturned sentence outside its own correction and the self-test still demonstrates a known positive. EARLIER: re-measured at HEAD 342d12f9 on 2026-09-16 by OPUS in a clean detached worktree with --db and --board: no document repeats an overturned sentence outside its own correction, 7 findings suppressed by dispositions SWE2-FRONTIER authored and FABLE reviewed, and the self-test still demonstrates a known positive so the zero is a real negative. THIS ROW ALREADY SAID 0 AND THE RE-RUN IS THE POINT: it was standing on a reading taken SIX COMMITS BACK. FABLE re-measured it at 7583874d and recorded the argument in 342d12f9 - a verdict measured commits ago is not evidence about now, and the commits in between are the ones most likely to have broken something - but THE TABLE NEVER LEARNED IT, which is a defect in the instrument of record rather than in the pass: the best available measurement disagreed with the row and nothing here could say so. Passes 2, 4, 17, 22, 24 and 30 now rest on the SAME COMMIT, which is what a streak run's evidence should look like and is NOT a streak run - a run is all thirty passes together with the publish guard on every publish in it. WHAT THIS ROW SAID BEFORE, PRESERVED: SURVIVOR 0, measured at HEAD fb4381ec on 2026-09-16 by OPUS - the propagation sweep finds no document repeating an overturned sentence outside its own correction, with 7 findings suppressed by dispositions SWE2-FRONTIER authored and FABLE reviewed. THE TWO THAT SURVIVED THIS MORNING WERE BOTH OPUS'S AND BOTH WERE CLOSED BY REPAIR, NOT BY SUPPRESSION. the-blinking-icon-and-its-atlas.md section 5 called 01D70800/01D70810 a dispatch table of 4-byte RVAs; they are record 0 and record 1 FIELD 2, the Handler slot, of a SCOPE_TABLE spanning 01D707F4-01D72AF8, so the conclusion survives and strengthens (fb4381ec). BUT THE SENTENCE I ADDED WITH IT WAS FALSE AND I WITHDREW IT THE SAME DAY: I wrote that 002B7B80 has NO ADMISSIBLE STATIC REFERENCE AT ALL. It has one. 002B6427 lea r8, [rip+0x1752] materialises it inside 002B6350, and r8 is written nowhere before 002B6474 call 0x245000, so the address is passed as the Win64 THIRD ARGUMENT - a use, not metadata. FABLE's half was right and my extra step was not. THE ABSENCE RESTED ON get_xrefs_to, WHICH REPORTED THREE, and an absence claim needs an image-wide boundary-free sweep, which this database already required of me. Swept with a positive control (0020E600, 4,365 call sites found): 1 LEA in .text, 2 RVA words in .rdata at the scope-table Handler slots, 1 in .pdata, and 38 four-byte coincidences inside .text instruction streams that are not references - a raw byte count would have said 42. NOTE WHAT THIS IS AN INSTANCE OF: this morning FABLE found my UQ-1 repair had struck the body sentences and left the heading. Correcting a page and leaving the verdict table asserting the withdrawn sentence would have been the same defect again, which is why this row moved with the page. The holder of the missed reference, 002B6350, is one of the thirty bodies with no CodeDomain. AND THE OTHER ONE IS THE MECHANISM'S BEST RESULT SO FAR, BECAUSE IT WENT AGAINST ME. I filed a FALSE-POSITIVE disposition for derived-call-signatures.md:124, reasoning that the detector had matched a correction marker over a repaired page, and I left it UNSIGNED because OPUS wrote both the original bound and the repair. FABLE reviewed it and found the disposition WRONG (d824884c): my repair had struck the two BODY sentences carrying '37 of 562' and left the HEADING, which states the same figure, so the bullet still opened on the number its own correction rejects - and a heading is the first thing read. FABLE repaired the heading. The disposition is WITHDRAWN, not re-verdicted, because the defect is gone at its source and there is nothing to disposition. HAD OPUS BEEN ABLE TO SIGN ITS OWN ROW, A REAL SURVIVING CLAIM WOULD HAVE BEEN SUPPRESSED by the agent most certain it was not one. The independent-reviewer rule is not ceremony; on its first contested use it caught a wrong verdict from the author. WHAT THIS ROW DOES NOT MEAN: the streak has not begun. final_audits is 0/30, every pass is re-satisfied PER RUN under section 11.4, and pass 29 demonstrated today that a pass certified clean in the morning can be red by the afternoon from a peer publish. WHAT THIS ROW SAID BEFORE, PRESERVED: SURVIVOR 2, re-measured at HEAD 05926097 on 2026-09-16 by OPUS - down from 9, and SEVEN WERE CLOSED BY THE MECHANISM RATHER THAN BY EDITING THE PAGES. check_propagation now reports '7 finding(s) suppressed by a reviewed disposition', every one authored by SWE2-FRONTIER and reviewed by FABLE on 2026-09-16, which is the persistent independently reviewed suppression FINAL-AUDIT pass 24 asks for, working in production on its own pass. SWE2-AUDIT-SPEC RULED THE MECHANISM SUFFICIENT the same day (OPUS-REQ-AUDITSPEC-DISPOSITION-MECHANISM-REVIEW): persistent, reviewed and evidence-invalidated are all mechanical, the sha256[:16] over whitespace-normalised evidence is accepted with a recommendation to fold in a checker version, LAPSED must not block, the reviewer field should be constrained to board identities, check_doc_claims and check_links should migrate one gate per change, and the per-page granularity chosen for the pass-6 consumer is right. THE TWO SURVIVORS ARE BOTH OPUS'S AND NEITHER IS A PAGE DEFECT SOMEONE ELSE CAN FIX: derived-call-signatures.md:124 is the correction-marker false positive whose disposition is filed and DELIBERATELY UNREVIEWED - it sits with FABLE as OPUS-REQ-FABLE-REVIEW-UQ1-MARKER-DISPOSITION, and OPUS signing its own row is the blindfold the mechanism exists to prevent; and the-blinking-icon-and-its-atlas.md section 5 is a REAL unrepaired claim OPUS owns and has claimed, blocked because the file carries a peer's uncommitted frontmatter line and publish_paths.sh commits a named path whole. WHAT THIS ROW SAID BEFORE, PRESERVED: MEASURED AGAINST THE CORPUS 2026-09-16 at HEAD d9291ff5 by OPUS - the first time this row has rested on anything but check_propagation's own --self-test. Run in a CLEAN DETACHED WORKTREE at HEAD with --db and --board. 221 contradiction tasks on the board, 100 carrying a quoted span of >=24 chars; EXPECTED 8, QUOTED 15, DATED 6, and SURVIVOR 9 - a corrected claim still live somewhere in the corpus. THE GATE EXITS 0 BECAUSE IT IS A DIAGNOSTIC, which is exactly how a headline of 9 was being read as a pass. The nine, by contradiction: AUDITSEM-CONTRA-FRONTIER-WM-COUNTS x2 in 16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md:217 and :274; AUDITSEM-CONTRA-FRONTIER-582860-238A30 x5, the same phrase 'exclusive subtree - all 10 members bound' in the-time-stop-and-system-stop-registry.md:208, ta-texture-animation-lists.md:159, battle-command-availability-and-reason-codes.md:192, ui-layout-parameters-and-editor-schema.md:277 and ui-request-router.md:646; FABLE-CONTRA-OPUS-UQ1-BOUND-IS-38-ROWS-TOO-STRONG x1 in derived-call-signatures.md:124; FABLE-CONTRA-OPUS-THE-BLINKING-ICON-IS-REACHED-ONLY-THROUGH-AN-EXCEPTION-SCOPE-TABLE x1 in the-blinking-icon-and-its-atlas.md:124. ONE IS ALREADY A FALSE POSITIVE AND IT IS OPUS'S OWN: derived-call-signatures.md:124 matched the string 'BOUNDED 2026-09-13 (OPUS)', which is the CORRECTION MARKER, not a live claim - the too-strong sentences beneath it are struck through and a 'RE-STATED 2026-09-16 (OPUS), on FABLE's contradiction' block carries the corrected derivation. That is precisely the shape the pass-24 disposition registry exists to record, and it is the first candidate for it. THE OTHER OPUS ONE IS REAL AND UNREPAIRED: FABLE-CONTRA-OPUS-THE-BLINKING-ICON... is READY with agent=None and its own affected_documents says 'sections 5 and 7 - NOT edited'. Section 5 still reads 'Reached only through a table' over a claim that 01D70800/01D70810 are a dispatch table of 4-byte RVAs, when FABLE decoded them as record 0 and record 1 FIELD 2 - the Handler slot - of a SCOPE_TABLE spanning 01D707F4..01D72AF8. That makes the 'table' unwind metadata, which this database bans as evidence. OPUS owns the repair and has not done it. WHAT THIS ROW SAID BEFORE, PRESERVED: clean, on check_propagation.py=0 - the gate baseline's record of a --self-test, since run_gates maps the tool through NOT_A_CORPUS_GATE."),
    29: (0, "RE-MEASURED AT HEAD 2aae130d (OPUS) in a clean detached worktree: check_links.py exit 0, 'all relative links resolve, on this filesystem and on a case-sensitive one', over the WHOLE TRACKED TREE rather than a database subtree - the distinction that matters here, because an export of Database/FFXII TZA alone cannot resolve ../../Tools/README.md and reports a corpus that is fine as broken. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 940ad933 - AND THIS IS THE FIRST READING TODAY TAKEN WITH THE RIGHT "
        "SELECTOR. Measured 2026-09-17 by OPUS with `check_links.py --db \"Database/FFXII TZA\"` "
        "from inside a clean detached worktree: exit 0, 623 files, 38,017 relative links, all "
        "resolving on this filesystem and on a case-sensitive one, STRICT_WAIVERS 0. THE FILE COUNT "
        "IS THE TELL: 623 is the worktree's own database. Every earlier 'clean' today reported 659, "
        "which is the MAIN working tree's database plus Tools - a different corpus on a different "
        "tree. "
        "THE 47 ARE GONE BECAUSE THEY WERE FINALLY PUBLISHED, not because they were re-repaired: "
        "940ad933 carries the wave-2 edits that had been sitting uncommitted in OPUS's working tree "
        "since the hung publisher, 19 files, every changed line touching `_index/` and zero "
        "non-link lines. One of the 19, third-party-middleware-inventory.md, had to be RESTORED "
        "FROM HEAD FIRST and the link fix re-applied: OPUS's stale copy would have reverted six "
        "peer census recounts (104->103, 475->474, 603->602, 119->118, 60->63, 54->52), because "
        "publish_paths.sh commits a path's whole working-tree state and peers' commits never update "
        "that working tree. Caught by diffing every path against current HEAD before naming it. "
        "THE GOAL'S PASS-29 ITEM IS SATISFIED AND WAS NEVER WHAT WAS RED: the two case-sensitive "
        "links stay REPAIRED rather than waived, STRICT_WAIVERS is empty, and the checker prints "
        "that it is empty so silence cannot be mistaken for an absent mechanism. "
        "WHAT THIS ROW MUST STILL NOT BE READ AS: a pass measured correctly ONCE. The emitter fix "
        "8fa4a6de holds, but the instrument that reports this pass will keep answering about the "
        "author's own machine whenever it is run without a selector, and that is routed as "
        "OPUS-REQ-FRONTIER-KIT-SCRIPTS-HARDCODE-ONE-MACHINES-WORKING-TREE. Any future reading of "
        "this row that does not name its file count is not checkable. final_audits remains 0/30. "
        "WHAT THIS ROW SAID BEFORE, AND IT WAS WRONG THREE TIMES BEFORE THIS: "
        "RED AT HEAD 37d1bb7f - 47 BROKEN. EVERY 'CLEAN' THIS ROW CARRIED TODAY WAS MEASURED "
        "AGAINST THE WRONG TREE, AND THE TREE IT MEASURED WAS OPUS'S OWN UNPUBLISHED FIX. "
        "Re-measured 2026-09-17 by OPUS with `check_links.py --db \"Database/FFXII TZA\"` inside a "
        "clean detached worktree: exit 1, 623 files, 38,017 links, 47 broken. "
        "THE MECHANISM, because it defeats the discipline this fleet adopted and will defeat anyone "
        "else who trusts it: check_links.py hardcodes ABSOLUTE ROOTS - "
        "`C:\\Users\\Kristian\\source\\repos\\XIIOnline\\Database\\FFXII TZA` and `...\\Database"
        "\\Tools`. Invoked with NO ARGUMENTS it walks those two paths NO MATTER WHAT DIRECTORY IT "
        "IS RUN FROM. Every pass-29 measurement OPUS published today was `python check_links.py` "
        "with no arguments, run from inside a detached worktree, believing it measured that "
        "worktree. IT MEASURED THE MAIN WORKING TREE EVERY TIME. Proven by three runs in one "
        "worktree: no args gives 659 files exit 0; `--db` on the worktree's own DB gives 623 files "
        "exit 1 with 48 broken; `--db` pointed at the MAIN tree's DB gives 624 files exit 0. Same "
        "checker, same commit, same directory - the variable is WHICH TREE, and only the no-args "
        "form silently picks the author's. "
        "WHY THAT MADE THIS ROW SAY CLEAN, which is the part that is OPUS's fault rather than the "
        "tool's: THE MAIN WORKING TREE CONTAINS OPUS'S OWN UNCOMMITTED WAVE-2 REPAIRS. 18 of the 19 "
        "files carrying the 47 broken links are modified in the working tree with the fix applied "
        "and NEVER COMMITTED. So the checker was reading OPUS's repair, and OPUS reported it as the "
        "state of HEAD. A verdict certifying the corpus on the strength of an unpublished local "
        "edit is the worst form this session's recurring error has taken. "
        "HOW THE REPAIRS WERE BELIEVED TO HAVE LANDED: OPUS's publisher for them hung five hours "
        "without ever claiming @publication and was terminated. OPUS then checked whether the work "
        "had landed by another route using a path list written with Windows newline translation - "
        "every path carried a trailing CARRIAGE RETURN, so `git status -- \"$p\"` asked about paths "
        "that do not exist and answered clean for all nineteen, and a content grep over the same "
        "list failed the same way. From those two silent misses OPUS concluded FRONTIER's b775a7ba "
        "and 3668e438 had swept the repairs in. THE SAME CRLF DEFECT WAS FOUND AND FIXED FOR WAVE 4 "
        "HOURS LATER AND WAVE 2 WAS NEVER RE-CHECKED - finding a measurement bug and not re-running "
        "the earlier measurements it had already corrupted is the whole failure in one sentence. "
        "WHAT IS ACTUALLY TRUE ABOUT THE CORPUS: the emitter fix 8fa4a6de is real and holding - not "
        "one of the 47 comes from a batch published after it. The 47 are the ORIGINAL wave-2 "
        "population, still at HEAD because their repair was never published. 18 files carry the fix "
        "uncommitted with every changed line touching `_index/` and ZERO non-link lines, so "
        "publishing them sweeps nobody's work; the 19th, heading-speed-to-position-delta.md, was "
        "repaired by its own holder in the interval. "
        "THE REPAIR IS IN THE SAME COMMIT AS THIS ROW. The 47 are fixed by publishing the wave-2 "
        "edits that have been sitting uncommitted, so this verdict is RED as measured at 37d1bb7f "
        "and the commit carrying it is the one that clears them. IT IS DELIBERATELY NOT WRITTEN AS "
        "CLEAN: the next measurement has to be taken at a HEAD that contains the fix, with `--db`, "
        "and by someone who has read why the last three readings were wrong. A row that marked "
        "itself clean on the strength of its own pending repair would be committing the identical "
        "error this row exists to record. "
        "ROUTED AS A TOOL DEFECT, NOT ONLY A ROW CORRECTION: hardcoded absolute roots plus an "
        "optional selector means the SAFE-LOOKING invocation is the wrong one, and this fleet's "
        "standing practice is to measure in a clean detached worktree. The tool's own header records "
        "that `--db` was once accepted and SILENTLY IGNORED and that this was fixed; the fix left "
        "the no-args path still pinned to one machine's working tree. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED, AND IT WAS WRONG THREE TIMES TODAY: "
        "CLEAN AT HEAD 5834fb05. Re-measured 2026-09-17 by OPUS in a clean detached worktree: "
        "check_links exit 0, 659 markdown files, 38,059 relative links, all resolving on this "
        "filesystem and on a case-sensitive one, STRICT_WAIVERS 0 - so the goal's two "
        "case-sensitive links remain REPAIRED rather than excused, and an empty waiver table still "
        "prints as empty rather than as silence. "
        "THE TWO THAT WERE RED AN HOUR AGO WERE LANDED BY THEIR HOLDERS, which is the second time "
        "today that leaving a dirty file alone produced the right outcome without OPUS touching it. "
        "OPUS declined to repair them because both were dirty in the working tree and "
        "publish_paths.sh commits a named path's WHOLE working-tree state; their holders published "
        "them correct. One of the two was an OPUS repair from c65b1a16 written in the wrong "
        "direction, and OPUS said so in the row while it was red rather than after it was fixed. "
        "THE GENERATOR REMAINS FIXED AND THAT IS WHAT MADE THIS STICK: SWE2-FRONTIER's 8fa4a6de "
        "routes ADDRESS-INDEX backlinks by page depth, and the corpus has since taken several more "
        "subtree batches and GAINED links without gaining a single wave. Four red cycles in one day "
        "ended when the emitter was named instead of the links being repaired a fifth time. "
        "THIS ROW HAS EXPIRED ONCE TODAY ALREADY, within the hour of asserting a KNOWN EXPIRY, so "
        "it is not carried between runs on anybody's authority. final_audits remains 0/30. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "RED AT HEAD 8fa4a6de - 2 BROKEN, AND THE ROW'S OWN STATED EXPIRY ARRIVED WITHIN THE "
        "HOUR. Re-measured 2026-09-17 by OPUS in a clean detached worktree: check_links exit 1, 659 "
        "files, 38,033 relative links, STRICT_WAIVERS 0. "
        "THE GENERATOR WAS FIXED AND THE FIX WORKED. SWE2-FRONTIER landed 8fa4a6de 'subtree emitter "
        "routes ADDRESS-INDEX backlinks by page depth' within the hour of "
        "OPUS-REQ-FRONTIER-SUBTREE-EMITTER-WRITES-A-DEPTH-2-BACKLINK-ONTO-EVERY-PAGE, and the count "
        "went 24 -> 2 ACROSS THREE MORE SUBTREE BATCHES that would previously each have added their "
        "own wave. That is what naming a generator buys and a fifth repair would not have. "
        "THE REMAINING 2 ARE NOT THE EMITTER AND NOT THE FIX OVERSHOOTING - they run the OPPOSITE "
        "way, depth-2 pages carrying `../` where `../../` is owed, and the check was made "
        "specifically because a fix landing beside two inverse-direction defects is exactly what an "
        "overshoot would look like. 18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md "
        "traces to c65b1a16, 2026-09-15 - AN OPUS PASS-29 REPAIR COMMIT, so one of the two is OPUS's "
        "own repair written in the wrong direction. "
        "NEITHER IS REPAIRED HERE AND THE REASON IS A RULE, NOT A SHRUG: both files are DIRTY in the "
        "working tree, and publish_paths.sh commits a named path's WHOLE working-tree state, so "
        "repairing them would sweep a peer's unpublished work into an OPUS commit - the failure "
        "b85ffb4c and ddc28021 demonstrated from the other side. The save-payload page's offending "
        "line is a SWE2-FRONTIER interior read dated 2026-09-17, so its holder is actively in it. "
        "WHAT THIS SEQUENCE ESTABLISHES FOR THE STREAK, which is worth more than either count: this "
        "row asserted CLEAN at 673b129a with an explicit KNOWN EXPIRY, and the expiry arrived before "
        "the next verdict was even published. Section 11.4's per-run re-satisfaction is not "
        "paperwork, and no pass-29 verdict should be carried between runs. final_audits remains "
        "0/30. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 673b129a - AND THE GENERATOR IS FINALLY NAMED, WHICH MATTERS MORE THAN "
        "THE COLOUR. Re-measured 2026-09-17 by OPUS in a clean detached worktree: check_links exit "
        "0, 659 markdown files, 37,952 relative links, all resolving on this filesystem and on a "
        "case-sensitive one, STRICT_WAIVERS 0. "
        "THIS ROW WAS STALE ACROSS TWO MORE RED CYCLES. It said CLEAN AT HEAD ce4084f8 from "
        "2026-09-16 while the pass went red twice more - a third wave of 25 documents and a fourth "
        "of 24 links across 7 files - which is exactly the defect row 24 names: a verdict measured "
        "commits ago is not evidence about now, and the commits in between are the ones most likely "
        "to have broken something. "
        "FOUR RED CYCLES IN ONE DAY IS NOT CARELESSNESS AND IS NOT A PEER PROBLEM, IT IS ONE "
        "GENERATOR. Census over the 10 'exclusive-subtree roots' batches reachable from HEAD, ADDED "
        "lines only, grouped by the receiving page's own directory depth: depth 2 with `../../` - "
        "247 links, ALL CORRECT; depth 1 with `../../` - 70 links, ALL BROKEN; depth 3 with "
        "`../../` - 4 links, ALL BROKEN; depth 1 with `../` - 2 links, correct. 323 emitted, 74 "
        "wrong. THE PREFIX IS RIGHT EXACTLY WHEN THE PAGE IS DEPTH 2, the corpus's modal depth, so "
        "the emitter was validated on the one population where its constant happens to be true. "
        "That is the same shape as the eight instruments corrected on 2026-09-16 and 17: REAL "
        "EVIDENCE, WRONG POPULATION - and it is why repairing the links four times never made it "
        "stop. "
        "IT IS NOT A PURE CONSTANT, WHICH IS THE HALF THAT MAKES IT FIXABLE: in 04dc361c, inside the "
        "single depth-1 file 05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md, the "
        "rows for 002EF74C and 002EF7CC carry the CORRECT `../` while other rows added to that same "
        "file in that same commit carry `../../`. A path that computes the depth already exists in "
        "the generator, so the fix is to route every row through it. Filed as "
        "OPUS-REQ-FRONTIER-SUBTREE-EMITTER-WRITES-A-DEPTH-2-BACKLINK-ONTO-EVERY-PAGE. OPUS did NOT "
        "chase which path that is: FRONTIER can see it in their own source faster than it can be "
        "inferred from diffs, and guessing it would have been the fourth parser OPUS built in two "
        "days without checking prior art. "
        "OPUS CHECKED ITSELF BEFORE NAMING ANYONE, because on 2026-09-16 OPUS filed a P2 against "
        "FRONTIER for a lock OPUS was holding itself. Both hits for the wrong-depth string under "
        "Database/Tools/work/OPUS/ were read: the one in pass29_apply.py is a one-off repair for a "
        "depth-2 page correcting `../` to `../../`, the RIGHT direction for that file. Not a "
        "generator, and not the source. "
        "WHAT THIS ROW MUST NOT BE READ AS: a pass that is clean now and was clean four times today "
        "is not a pass that will be clean at the next batch. Until the emitter is routed and "
        "check_links joins the pre-publish neighbour guard, THIS ROW HAS A KNOWN EXPIRY and section "
        "11.4's per-run re-satisfaction is the only thing standing between it and a false streak. "
        "final_audits remains 0/30. "
        "THE WAVE-3 AND WAVE-4 REPAIRS, for the record: 49 links across 20 files reached HEAD "
        "without OPUS's publisher - that process hung five hours without ever claiming @publication "
        "and was terminated, while the repairs were swept in by FRONTIER's own publishes b775a7ba "
        "and 3668e438, the same whole-working-tree behaviour of publish_paths.sh this corpus has "
        "twice been bitten by from the other side. Verified present and correct at HEAD before "
        "being counted. Wave 4's 24 links across 7 files are 673b129a, with every diff line "
        "confirmed to be a link-depth change - 48 changed lines against 24 repairs, nonlink count 0 "
        "on all seven files - after the FIRST confinement check was wrong: the path list carried "
        "CRLF endings, so `git status -- \"$p\"` was asking about paths with a trailing carriage "
        "return and answered 'clean' for all seven regardless. Same class as `git status` without "
        "`--` earlier that day: an instrument answering truthfully about the wrong population. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD ce4084f8 - RECOVERED THE SAME DAY IT WENT RED. Re-measured 2026-09-16 by "
        "OPUS in a clean detached worktree: check_links exit 0, no broken link anywhere in the "
        "corpus. THE REPAIR WAS SPLIT THREE WAYS AND THAT IS THE INTERESTING PART. (1) OPUS repaired "
        "26 links across 9 files in f4e46dc7 - pure path arithmetic, the checker naming the "
        "replacement beside every hit, so no judgement was involved and routing all 30 would have "
        "been ceremony. (2) TWO FILES WERE DELIBERATELY LEFT UNTOUCHED because they were dirty in "
        "the working tree: repairing them would have swept a peer's unpublished work into an OPUS "
        "commit, which is the failure b85ffb4c and ddc28021 already demonstrated from the other "
        "side. Their holders landed them with the links correct. (3) The last two were NOT a depth "
        "error at all - cmap-menumap and wmap-menumap linked "
        "`../../../Tools/work/DATA/menumap/decode_menumap.py`, whose `../` count was RIGHT and whose "
        "TARGET IS NOT IN GIT: `git ls-files --error-unmatch` refuses it and the file exists only in "
        "a local checkout, so the link resolved for its author and was broken for everyone else. "
        "Routed to SWE2-DATA, and SWE2-FRONTIER resolved it in ed4c533f - 'de-link two menumap "
        "scratch paths, clean-worktree check_links green' - taking the cite-as-prose option rather "
        "than publishing a private work directory into the kit. THE COMMIT MESSAGE IS WORTH AS MUCH "
        "AS THE FIX: a peer measured it in a CLEAN WORKTREE and said so, which is the discipline "
        "this table spent the day arguing for, adopted by somebody else without being asked. "
        "STILL TRUE AND WORTH KEEPING IN FRONT OF THE STREAK: this pass was clean this morning, RED "
        "by the afternoon from a batch publish, and clean again by evening. Section 11.4's per-run "
        "re-satisfaction is not paperwork. WHAT THIS ROW SAID WHILE RED, PRESERVED: "
        "BROKEN LINKS 30, ACROSS 13 DOCUMENTS - RED AT HEAD 3ae38a40, re-measured 2026-09-16 by "
        "OPUS in a clean detached worktree, check_links exit 1. Every one is a `../_index/...` that "
        "needs `../../` or deeper - the number of `../` is the page's own depth. Example, verified "
        "against the COMMITTED blob rather than the working tree: "
        "18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md links `../_index/ADDRESS-INDEX.md` "
        "three times from a directory two levels down, and `git status` reports the file CLEAN, so "
        "these are committed defects and not somebody's dirty tree. ATTRIBUTED MECHANICALLY by each "
        "file's last commit: 6 files from 0cdb6009 (SWE2-FRONTIER batch-6), 3 from a5232d9c, 2 from "
        "dbfbef29 (batch-7), 2 from 9d8f0e73. SO BATCH-6 BROKE THREE PASSES, NOT TWO - 22, 30 and "
        "29 - and a5232d9c IS THE FIX FOR THE FIRST TWO: 'FRONTIER: pass-22 batch-6 accounting, 39 "
        "neighbour crossings dispositioned'. IT WORKED AND IT REGRESSED THIS PASS WHILE WORKING, "
        "which is the most useful thing this row has ever recorded: a repair landing 39 correct "
        "accounting sentences also landed three broken relative links, and nothing in the publish "
        "path stopped it. That is an argument for the link gate joining the pre-publish guard, not "
        "an argument against the repair. 9d8f0e73's own subject already says 'pass 29 regressed', so "
        "this was seen once and not carried into the table - the defect this table was built to "
        "stop. THIS ROW PREVIOUSLY CARRIED NO NOTE AT ALL and printed 'clean check_links.py=0' from "
        "a bare tool run with NO HEAD, NO DATE AND NO INSTRUMENT DETAIL - a verdict that cannot say "
        "how far behind it is, the same defect corrected for passes 2, 4, 17, 22, 24 and 30 earlier "
        "today. ON THE GOAL'S PASS-29 ITEM, WHICH IS SEPARATE AND IS DONE: the two case-sensitive "
        "links were repaired rather than waived, STRICT_WAIVERS is EMPTY, and check_links prints "
        "'case-sensitivity waivers in STRICT_WAIVERS: 0 - nothing is being excused' so an empty "
        "waiver table cannot be misread as an absent mechanism. That is not what is red here. "
        "Routed as OPUS-REQ-FRONTIER-PASS29-THIRTY-BROKEN-RELATIVE-LINKS."),
    30: (0, "CLEAN AT HEAD 5834fb05. Re-measured 2026-09-17 by OPUS in a clean detached worktree "
        "against a report built in that same worktree: check_crossref_clean exit 0, 'every "
        "crossref_clean satisfies its definition'. 1 true-with-census-debt-only "
        "(battle-action-handler-table.md, UNLISTED CODE 002FE7D0, listed so it stays visible), 277 "
        "false-with-no-defect reported as ELIGIBLE rather than as failures, 0 violations. "
        "THE VIOLATION WAS FIXED BY ITS OWNER WITHIN THE HOUR, AND BY ACCOUNTING RATHER THAN BY "
        "FLIPPING THE KEY. native-command-lifecycle.md claimed clean while holding 3 UNACCOUNTED "
        "NEIGHBOUR findings; OPUS routed it as "
        "OPUS-REQ-FRONTIER-PASS30-NATIVE-COMMAND-LIFECYCLE-CLAIMS-CLEAN-WITH-THREE-CROSSINGS with "
        "the explicit argument that `false` asserts nothing and the page's claim was recoverable, "
        "and SWE2-FRONTIER's 5834fb05 accounted for those three plus six more. AS PREDICTED WHEN "
        "ROUTING IT, CLEARING PASS 22 AND PASS 30 WAS ONE ACT: they are the same finding seen from "
        "two passes, exactly as a5232d9c demonstrated on 2026-09-16. "
        "THE ROUTED NOTE CARRIED A CAVEAT AND IT MATTERED: CombatFormula's set included "
        "`0030E360 callee 003112F0`, a STATICALLY PRESENT AND DYNAMICALLY DEAD edge - EXP-086 "
        "measured zero calls across 67 cases, and 7fc6e8b7 struck it from the status-write "
        "contract's callee list the same hour, on OPUS's own re-derivation that 003848E0 sets "
        "result+0x2C bit 0 and both builders clear it. An accounting sentence presenting it as a "
        "live crossing would have been accurate about edges.tsv and wrong about the program. "
        "THIS ROW WAS 63 COMMITS STALE WHEN IT WAS CAUGHT SAYING CLEAN, and it is now clean again "
        "on a measurement one commit old. Those are not the same statement, and the age stamp is "
        "what distinguishes them. final_audits remains 0/30. "
        "WHAT THIS ROW SAID WHILE RED, PRESERVED: "
        "RED AT HEAD 673b129a - 1 DOCUMENT CLAIMS CLEAN AND IS NOT. Re-measured 2026-09-17 by "
        "OPUS in a clean detached worktree against a report built in that same worktree: "
        "check_crossref_clean exit 1. "
        "01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md carries "
        "`crossref_clean: true` while holding 3 UNACCOUNTED NEIGHBOUR findings - CombatAI 5 edges, "
        "CombatAction 8 edges, CombatFormula 6 edges. The rest of the definition still holds: 1 "
        "true-with-census-debt-only (battle-action-handler-table.md, UNLISTED CODE 002FE7D0), 274 "
        "false-with-no-defect reported as ELIGIBLE rather than as failures, 10 findings over 7 "
        "documents across 410. "
        "THIS ROW SAID CLEAN AND WAS 63 COMMITS OLD, which is the failure this table was built to "
        "stop and the second time in two days it has been caught: a verdict that cannot say how far "
        "behind it is cannot be trusted forward. The row was not wrong when written; it was wrong to "
        "still be standing. "
        "THE PAGE ALREADY NAMES THE TWO ANCHOR FUNCTIONS AND STILL FAILS, which is the instructive "
        "part. Its crossings section ends 'Shared callees outside the census: 0031B760, 0030E360' - "
        "so the ADDRESSES are mentioned and the LAYERS they cross into are not, and accounting is "
        "about the layer. Naming the callee without naming where it lands is the same omission as a "
        "movement-veto list that says what a bit was folded WITH and never where the fold LANDED. "
        "ONE OF THE UNACCOUNTED EDGES IS A DEAD EDGE, AND THE ACCOUNTING MUST SAY SO RATHER THAN "
        "SIMPLY LIST IT: CombatFormula's set includes `0030E360 callee 003112F0`, and EXP-086 "
        "measured ZERO calls to 003112F0 across all 67 cases while OPUS re-derived the reason from "
        "the image - 003848E0 sets result+0x2C bit 0 at 0038498D and BOTH builders clear it at "
        "00386A66 and 00386AC3, so the gate is shut before it is tested. A static call graph shows "
        "the edge and the edge is dead. An accounting sentence that presents it as a live crossing "
        "into CombatFormula would be accurate about edges.tsv and wrong about the program. "
        "ROUTED, NOT REPAIRED HERE: the page's crossings section is SWE2-FRONTIER's, and the last "
        "pass-30 violation of exactly this shape was cleared by its owner accounting for the "
        "crossings (a5232d9c), which fixed pass 22 at the same time because they are the same "
        "finding seen from two passes. Flipping the key to `false` would be the WRONG repair: "
        "`false` asserts nothing, and the page's claim is recoverable. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN AT HEAD 3ae38a40 - RECOVERED. Re-measured 2026-09-16 by OPUS in a clean detached "
        "worktree against a fresh audit_crossrefs report, exit 0: 'every crossref_clean satisfies "
        "its definition', 276 false-and-eligible reported as eligible rather than as failures, 0 "
        "violations. THE VIOLATION THIS ROW CARRIED WAS FIXED BY ITS AUTHOR WITHIN THE DAY: "
        "the-ordered-render-command-list.md claimed `crossref_clean: true` while holding 3 "
        "UNACCOUNTED NEIGHBOUR findings, both defects coming from 0cdb6009, and SWE2-FRONTIER's "
        "a5232d9c accounted for the crossings - which cleared pass 30 as a side effect of clearing "
        "pass 22, exactly as OPUS predicted when routing them together ('accounting for the three "
        "crossings fixes both at once, and flipping the key to false would be the wrong repair'). "
        "The key was not flipped and did not need to be. WHAT THIS ROW SAID WHILE RED, PRESERVED: "
        "VIOLATED AT HEAD 12d39348 - 1 document CLAIMS CLEAN AND IS NOT. Re-measured 2026-09-16 "
        "by OPUS in a clean detached worktree against a fresh audit_crossrefs report, exit 1: "
        "`17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md` carries "
        "`crossref_clean: true` while holding **3 UNACCOUNTED NEIGHBOUR** document-defect findings "
        "(ActorEntity, Party, Status_Periodic_Terminal). That is precisely what the canonical "
        "definition forbids: `true` ASSERTS a fresh report shows zero document-defect findings "
        "against the document, and every kind is a defect except the census-debt kinds named by "
        "name. **THE SAME COMMIT BROKE BOTH PASSES.** That page is one of the 17 affected by "
        "0cdb6009 (SWE2-FRONTIER batch-6), which took pass 22 from 1 unaccounted neighbour to 40; "
        "here the same three findings also falsify a frontmatter claim the page still makes. A "
        "`crossref_clean: true` is a claim with a shelf life - it is true of the corpus at the "
        "moment it was written, and any later edit that adds a crossing silently falsifies it - "
        "which is the argument for re-deriving it every run rather than stamping it, and is why the "
        "definition requires freshness to be re-derived rather than recorded. Routed with pass 22 as "
        "OPUS-REQ-FRONTIER-PASS22-BATCH6-39-UNACCOUNTED-NEIGHBOURS: accounting for the three "
        "crossings fixes both passes at once, and flipping the key to `false` would be the wrong "
        "repair because `false` asserts nothing and the page's own claim is recoverable. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLEAN at HEAD 114558e9, 2026-09-16, re-measured by OPUS against a fresh audit_crossrefs report in a clean detached worktree 37 commits after the consolidation: every crossref_clean satisfies its definition, 276 eligible-and-not-raised (up from 274 as the corpus grew to 408 documents), 0 violations. EARLIER: CLEAN at HEAD 342d12f9, 2026-09-16, re-measured by OPUS against a FRESH audit_crossrefs report built in the same clean detached worktree: exit 0, 'every crossref_clean satisfies its definition', 1 true-with-census-debt-only (battle-action-handler-table.md, UNLISTED CODE 002FE7D0), 274 false-with-no-defect reported as ELIGIBLE rather than as failures, 0 violations. THE RE-RUN IS THE POINT, NOT THE VERDICT: this row was standing on a reading taken TWENTY-EIGHT COMMITS BACK over 403 documents, and the corpus now holds 405 - the eligible count moved 271 to 274 underneath a standing clean. A verdict that cannot say how far behind it is cannot be trusted forward, which is the whole reason the age stamp went in today. The definition, its independent review by SWE2-AUDIT-SPEC and the promotion of the reviewed checker into the kit are unchanged and preserved below. WHAT THIS ROW SAID BEFORE, PRESERVED: CLEAN at HEAD 05926097, 2026-09-16, and this is the first time all three parts of the pass are satisfied at once. FINAL-AUDIT pass 30 asks for ONE CANONICAL DEFINITION of crossref_clean, INDEPENDENTLY REVIEWED, and THEN ENFORCED MECHANICALLY. Definition: written by OPUS 2026-09-15. Review: SWE2-AUDIT-SPEC ACCEPT 2026-09-16 on OPUS-REQ-AUDITSPEC-REVIEW-CROSSREF-CLEAN-DEFINITION - 'the definition is well-formed, the checker implements it faithfully, and its self-test passes' - record Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-P30-CROSSREF-CLEAN.md, journal 26cb7ea7. Enforcement: the reviewed checker is PROMOTED OUT OF proposals/ INTO THE KIT, which is what 'then' meant, and its own header now says the review is the reason it is there. Corpus run at HEAD against a FRESH report built in a clean detached worktree: 'every crossref_clean satisfies its definition'. 1 true-with-census-debt-only (battle-action-handler-table.md, UNLISTED CODE 002FE7D0, listed so it stays visible), 271 false-with-no-defect reported as ELIGIBLE rather than as failures, 0 violations. THE THREE MALFORMED VALUES ARE GONE AND THAT WAS THE REVIEW'S OWN INSTRUCTION: cross-subsystem-accessor-hubs.md, heading-speed-to-position-delta.md and persistent-flag-banks.md carried crossref_clean: dispositioned, a word outside the closed vocabulary. The reviewer ruled that failing them is correct BECAUSE it forces the cleanup - their dispositioned findings are registry-cleared and no longer findings, so each is eligible for true. Measured before flipping rather than assumed: the HEAD report carries exactly ONE finding across 403 documents and none of the three is the document it belongs to. THE FRESHNESS RULE PROVED ITSELF IN PASSING: editing those three made the report older than a document it judged and the checker REFUSED (exit 2) rather than using it, naming the offending path. A LIMIT DECIDED RATHER THAN DISCOVERED, as the review asked: freshness compares the report against DOCUMENT mtimes only, not against functions.tsv, edges.tsv or the registries. Extending it would couple this checker to a GN161 re-export cadence it does not control and would fail a true claim for a reason having nothing to do with the document; a stale graph input produces a wrong FINDING SET, which is pass 2's and pass 4's subject. The decision is recorded in the checker's header. WHAT THIS ROW SAID BEFORE, PRESERVED: MEASURED AGAINST THE CORPUS 2026-09-16 at HEAD d9291ff5 by OPUS, which is the first time this row has rested on anything but check_crossref_clean's own --self-test. Method: audit_crossrefs.py --json in a CLEAN DETACHED WORKTREE at HEAD (the tool reads the working tree, and this one carries heavy uncommitted peer work - the same care pass 22 needed), then check_crossref_clean.py against that report. Result: 265 documents disagree with the checker. THE TWO NUMBERS ARE DIFFERENT AND THE DIFFERENCE IS THE WHOLE POINT OF THE DEFINITION. 263 of the 265 are CLAIMS DIRTY, HAS 0 FINDINGS - the field is stale-pessimistic, not wrong about anything a reader would act on. Under the canonical definition written for FRONTIER-REQ-OPUS-PASS30-DEFINITION, 'false asserts nothing; false-with-zero is ELIGIBLE, not a failure', so those 263 are NOT defects. ONLY 2 ARE: 07-Combat-Action/Action-Dispatch/battle-action-handler-table.md claims clean and carries 1 finding (UNLISTED CODE 002FE7D0, which is pass 17's census debt), and 15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md claims clean and carries 1 finding (the Party edge 0017DFC0 caller 003594E0, already routed with the other four pass-22 findings). Both are known and neither is new. THE ENFORCEMENT HALF OF THIS PASS IS NOT DONE, and that is what keeps the row RED rather than the two documents. The goal requires one canonical definition of crossref_clean, independently reviewed, THEN enforced mechanically. The definition exists; OPUS-REQ-AUDITSPEC-REVIEW-CROSSREF-CLEAN-DEFINITION is READY and unclaimed with SWE2-AUDIT-SPEC; and check_crossref_clean does NOT yet implement it - it reports both directions as 'disagree', so its 265 is wider than the definition's 2. The tool is deliberately NOT changed ahead of that review: writing the definition and then certifying my own implementation of it is the thing independent review exists to prevent. WHAT THIS ROW SAID BEFORE, PRESERVED: clean, on check_crossref_clean.py=0 - which was the gate baseline's record of a --self-test, since run_gates maps the tool through NOT_A_CORPUS_GATE. It asserted that the instrument parses its own fixtures and was read as a reading of the corpus."),
    2:  (0, "BODY DRIFT 0 - RE-MEASURED AT HEAD 5cf96b34 (OPUS) in a clean detached worktree against a fresh audit_crossrefs run over 412 document(s): 3 finding(s) and NONE is this class. The three are two UNACCOUNTED NEIGHBOUR (pass 22, both new today) and one UNLISTED CODE (002FE7D0, pass 17's registered census debt). NOTE FOR ANYONE READING THE EXIT CODE: audit_crossrefs returns 1 whenever ANY finding exists, so this pass is read from the CLASS COUNT and not from the process status. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "BODY DRIFT 0, RE-MEASURED AT HEAD 6662e859 on 2026-09-17 (OPUS) in a clean detached worktree with the graph exports junctioned in: audit_crossrefs reports 2 findings across 410 documents and NEITHER is this class - one UNLISTED CODE (002FE7D0, pass 17 census debt) and one UNACCOUNTED NEIGHBOUR (pass 22). This row had been standing on a reading taken 2026-09-16 and was one of the five the provenance block flagged STALE. WHAT THIS ROW SAID BEFORE, PRESERVED: BODY DRIFT 0. RE-MEASURED AT HEAD 114558e9 on 2026-09-16 (OPUS), 37 commits after the six-pass consolidation at 342d12f9, in a clean detached worktree: still 0, in the same audit_crossrefs run that carried passes 2, 4, 17 and 22 - 1 finding across 408 documents and it is the registered UNLISTED CODE census debt.  Measured at HEAD 342d12f9 on 2026-09-16 by OPUS in a CLEAN DETACHED WORKTREE, in one audit_crossrefs run that also carried passes 17 and 22: 1 finding across 405 documents, and it is UNLISTED CODE 002FE7D0, pass 17's registered census debt - so this class is 0. ONE RUN, FOUR PASSES (2, 4, 17, 22), ONE COMMIT. Recorded because until now this row named NO measuring commit at all, which is weaker than stale: a stale verdict can be dated and re-run, while this one could not be interrogated. I had a 6f689a26 run in hand and re-ran rather than record it, because FABLE's argument in 342d12f9 - that a verdict measured commits ago is not evidence about now - applied to my own figure too."),
    # RESTATED 2026-09-14 - the earlier "3 of 4 verified" understated what exists and misnamed
    # what is missing. ALL FOUR artifacts retained in work/verify_GFZ_PARENT hash-match their
    # canonical values in GfzEnv.ps1 TODAY: embedded_exe.bin = $GfzAuthorizedExeSha, snapshot.fas2
    # = $GfzParentSnapshot, residual_addrs.txt = $GfzResidualSha, and all EIGHT coverage.tsv ledger
    # fields = $GfzLedger. A fresh import was performed - the certification note says so and the
    # gn161_certify project shell (04:53) sits one minute before the artifacts (04:55).
    #
    # SO THE GAP IS NOT A MISSING PROOF, IT IS A NON-INDEPENDENT ONE, and that is the sharper and
    # more troubling statement. The fresh import at seal time was performed BY the sealing process,
    # so using it to validate the sealing process is circular. Pass 5 is "the only pass that
    # re-validates the parent every other pass is measured against" - a check that cannot be
    # re-run by anything other than the thing it checks does not do that. PARTIAL stands, for a
    # better reason than before: not "we did three quarters of it" but "the fourth quarter is not
    # independent, and re-running it needs Ghidra headless, which the kit cannot reach."
    # WAS PARTIAL UNTIL 2026-09-14, ON A CLAIM ABOUT THE ENVIRONMENT THAT WAS FALSE. The reason
    # read "an independent re-run needs Ghidra headless and is not reachable from the kit" - and
    # analyzeHeadless.bat, a bundled JDK and `Import-GfzParent.ps1` ("the GFZ contract requires a
    # fresh import for every checkpoint verification") were all present the whole time. The claim
    # propagated from the protocol into this table and into a request nobody could act on.
    5:  (0, "ALL FOUR PROOFS REPRODUCE FOR GN162 - VERIFIED AT HEAD 5cf96b34 (OPUS), and the row this replaces stood on GN161. THE PROVENANCE OF THIS ROW IS A PARENT GENERATION, NOT A CORPUS COMMIT: the commit above records when the verification was performed, because a reader needs to know when this was last looked at, but nothing here moves when the corpus moves. THE EVIDENCE IS SWE2-AUDIT-SEM'S STAGE-4 RE-CERTIFICATION, 2026-09-16 - a fresh import of the sealed GN162 GZF into their own new project (work/auditsem_stage4/proj_gn162) via Import-GfzParent.ps1 with auto-analysis off, then Verify-GfzCheckpoint.ps1, with none of EC7's or OPUS's exported artifacts trusted. Different agent, different session, new project directory. I DID NOT QUOTE THEIR REPORT - I recomputed the sha256 of the GZF they imported and of all four artifacts out of their own output directory, which closes the chain end to end. THE GZF IN THE PARENT SLOT hashes to 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92 at 82,201,392 bytes, head and tail the sealed claim - so the file certified is the file present. Then: embedded EXE 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8, which IS THE SHIPPING-EXE AUTHORITY HASH THIS REPOSITORY STATES IN CLAUDE.md - an external anchor rather than a self-consistent one, and the strongest single fact in this row; snapshot.fas2 16a2a832d8856ba3d5c78d531ef0fd2295ef7dce956ca5cd545cf54f065bd192, 78,260,429 bytes; residual_addrs.txt ONE BYTE, a bare newline, sha 01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b - consistent with unresolved 0 rather than asserted to be; and the ledger read out of their coverage.tsv banner, internal 38161 owner 9409 finalNo 585 codeDomain 28167 explicit 38161 overlap 0 unresolved 0 pct 100.00000. WHAT IS STILL NOT INDEPENDENT, and AUDIT-SEM states it first: the same three PowerShell scripts, and -noanalysis restores the checkpoint rather than re-analysing the raw EXE, which is what the GFZ contract specifies. AND I DID NOT PERFORM AN IMPORT - I verified four output artifacts byte for byte. That is corroboration by a second reader, not a third import. THIS PASS HAS NO KIT INSTRUMENT and will not get one: FINAL-AUDIT-PROTOCOL line 763 records it as unmechanised because a fresh GZF import is a Ghidra run rather than a checker, so this row is re-satisfied by a re-import and by nothing else. Record: Database/Tools/work/SWE2-AUDIT-SEM/REVERIFY-residual30-stage4-gn162.md. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "INDEPENDENT re-import 2026-09-14 (OPUS): Import-GfzParent.ps1 into a new project "
            "(GZF sha 11110a34 verified first), then Verify-GfzCheckpoint.ps1 - ledger "
            "38161/9409/585/28137, overlap 0, explicit 38131, unresolved 30, 99.92139%; snapshot "
            "c16409ec; embedded EXE 73461d08; residual 30 @ 955da8c9. Different agent, different "
            "session, new project dir - the circularity is broken. NOT independent of the TOOLING "
            "(same three scripts), and -noanalysis restores the checkpoint rather than "
            "re-analysing the raw EXE, which is what the GFZ contract specifies."),
    12: (0, "CONFLATION 0, INVENTED 0, SHORTHAND 0 - RE-MEASURED AT HEAD 41288c9d (OPUS) in a clean detached worktree, against an export of SWE2-AUDIT-SEM's certified GN162 Stage-4 snapshot (fas2_export.py snapshot.fas2 --tsv: FAS2 v2, 38,161 functions, owner 9,409, domains 28,167, unresolved 0, overlap 0). check_layer_separation exit 0: 164 documents declaring a PrimaryOwner, 22 distinct labels over 164 uses all matching the ledger exactly, canary quiet at 0 functions carrying both layers. AND THE GATE CAN NOW TELL THIS RUN FROM ONE THAT MEASURED NOTHING, which until today it could not. Pointed at coverage.tsv - which sits beside snapshot.fas2 in the same verify directory and is the obvious thing to reach for - it has no header of the expected shape, so DictReader took its V121_COVERAGE banner line as the header, row.get('owner') came back None for all 38,161 rows, half one printed 'PrimaryOwner labels: 0' and declared the canary quiet BECAUSE THERE WAS NOTHING TO BE NOISY ABOUT, half two compared 164 document labels against an empty ledger, called all 164 INVENTED, filed them under 'NOT A LAYER ERROR' - and returned 0. TWO RUNS, BOTH EXIT 0, opposite readings. ledger_owners now checks for the owner and code_domains columns first and refuses a file without them with exit 2, so a wrong input is a refusal rather than a clean pass; an empty ledger from a WELL-FORMED file is still reported, because that is a real reading, and --self-test now carries both directions plus the canary so the demonstration can be re-run rather than only read here. THE DISCRIMINATING HALF IS HALF TWO, in the checker's own words: half one cannot fail while the one-label-per-function rule holds upstream, so its zero carries no information, and it is half two that reports 0 in all three defect classes over 164 real comparisons. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CONFLATION 0, INVENTED 0, SHORTHAND 0 - RE-MEASURED AT HEAD a756d9a3 on 2026-09-17 (OPUS) in a clean detached worktree: check_layer_separation exit 0, 164 documents declaring a PrimaryOwner, 22 distinct labels over 164 uses all matching the ledger exactly, and the canary quiet at 0 functions carrying both layers. This was the LAST of the five rows the provenance block flagged STALE, at 242 commits. THE EXPORT IT WAS MEASURED AGAINST IS THE WHOLE STORY OF THIS RE-RUN. The protocol recipe is 'fas2_export.py <certified snapshot>' and the obvious certified snapshot is verify_GFZ_PARENT/snapshot.fas2 - which exports as domains=28137 unresolved=30. THAT IS GN161, one certification and thirty functions stale, while coverage.tsv in the SAME DIRECTORY reads codeDomain=28167 unresolved=0. Taking the obvious path would have dated this row against the wrong generation with no error and a perfectly plausible result. Measured instead against auditsem_stage4/verify/snapshot.fas2, which exports domains=28167 unresolved=0 - SWE2-AUDIT-SEM's own fresh GN162 import, the one that reproduced sha256 16a2a832 byte-exact. Filed as OPUS-NOTICE-EC7-VERIFY-GFZ-PARENT-SNAPSHOT-IS-ONE-GENERATION-BEHIND-ITS-COVERAGE. AND THAT EXPORT INDEPENDENTLY CORROBORATES THE RESIDUAL-30 CLOSURE: 28,137 + 30 = 28,167 with unresolved 0, read by OPUS out of AUDIT-SEM's snapshot rather than out of AUDIT-SEM's report. WHAT THIS ROW COVERS AND WHAT IT DOES NOT, in the checker's own words: half one is a regression detector that CANNOT fail while the one-label-per-function rule holds upstream, so its zero carries no information. Half two - the documents - is the discriminating half, and that is the half reporting 0 distinct and 0 uses in all three defect classes. WHAT THIS ROW SAID BEFORE, PRESERVED: CONFLATION 0, INVENTED 0, SHORTHAND 0, re-measured at HEAD dd21f94d on 2026-09-16 by OPUS in a clean detached worktree against a FRESH fas2 export of batch_R109/post.fas2: 22 PrimaryOwner labels, 0 functions carrying both layers (the half-one canary, which cannot fail while the one-label-per-function rule holds upstream), 162 documents declaring an owner and all 162 uses matching the ledger exactly. THE OLD NOTE SAID GN160 AND THE GRAPH SAYS GN161: functions.parent.json names FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GN161_99P921_2026-09-14, so this row was resting on an export ONE GENERATION BEHIND the one the rest of the database is built from. batch_R109/post.fas2 is identified as the certified GN161 snapshot because its ledger reproduces pass 5's exactly - 38161 functions, owner 9409, domains 28137, unresolved 30, overlap 0 - rather than because of its filename. AND THE DECLARING COUNT MOVED 160 -> 162: two documents had entered the corpus that the standing verdict had never read. It still passes. This row is measured rather than back-filled; guessing which commit the 2026-09-14 hand pass was taken at would be the fabricated provenance this stamp exists to catch, so the pass was re-run instead. WHAT THIS ROW SAID BEFORE, PRESERVED: run 2026-09-14 on the certified GN160 export: overlap 0; "
            "CONFLATION 0, INVENTED 0, SHORTHAND 0 across 160 declaring documents"),
    4:  (0, "CLASSIFICATION 0 - RE-MEASURED AT HEAD 5cf96b34 (OPUS) in a clean detached worktree, in the SAME audit_crossrefs run that carries passes 2, 17 and 22: 3 finding(s) across 412 document(s) and none is this class. Read from the class count, not the exit status, which is 1 because findings exist in other classes. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "CLASSIFICATION 0, RE-MEASURED AT HEAD 6662e859 on 2026-09-17 (OPUS) in a clean detached worktree, in the SAME audit_crossrefs run that carries passes 2, 17 and 22: 2 findings across 410 documents, neither of this class. ONE RUN, FOUR PASSES, ONE COMMIT - which is what a streak run's evidence should look like and is still NOT a streak run. WHAT THIS ROW SAID BEFORE, PRESERVED: CLASSIFICATION 0. RE-MEASURED AT HEAD 114558e9 on 2026-09-16 (OPUS), 37 commits after the six-pass consolidation at 342d12f9, in a clean detached worktree: still 0, in the same audit_crossrefs run that carried passes 2, 4, 17 and 22 - 1 finding across 408 documents and it is the registered UNLISTED CODE census debt.  Measured at HEAD 342d12f9 on 2026-09-16 by OPUS in a CLEAN DETACHED WORKTREE, in one audit_crossrefs run that also carried passes 17 and 22: 1 finding across 405 documents, and it is UNLISTED CODE 002FE7D0, pass 17's registered census debt - so this class is 0. ONE RUN, FOUR PASSES (2, 4, 17, 22), ONE COMMIT. Recorded because until now this row named NO measuring commit at all, which is weaker than stale: a stale verdict can be dated and re-run, while this one could not be interrogated. I had a 6f689a26 run in hand and re-ran rather than record it, because FABLE's argument in 342d12f9 - that a verdict measured commits ago is not evidence about now - applied to my own figure too."),
    # PASS 17 IS `DATA VS FUNCTION`, AND ITS ONE RED WAS NEITHER. 002FE7D0 is not data
    # mis-presented as code - it is 106 bytes of REAL .text that the function list does not
    # contain, reached by one relocation, independently decoded as the 0x4021 wait handler and
    # registered since 2026-09-13 in Unlisted-Code/unlisted-code-blocks.tsv (1,471 blocks, 143
    # of them provably referenced). audit_crossrefs could not tell the two apart because it
    # holds only the function list; verify_doc_addresses, which HAS the section table, passed
    # the same document as ok. Two instruments serve this pass and they disagreed; the one with
    # more information was right.
    #
    # THE COUNTER-ARGUMENT, recorded so it can be challenged: reclassifying a finding to clear a
    # RED is exactly how a metric gets made to agree by weakening evidence. Three things separate
    # this from that - the finding is still REPORTED, in its own category, in the same report and
    # counted in the same total; the register it is keyed to was built on independent relocation
    # evidence the day before this question arose; and the reclassification is mutation-controlled
    # (remove the register, or just that one block from it, and the address reports GHOST again).
    # What is NOT claimed is that the debt is gone: 1,309 unlisted blocks and 244,619 bytes remain
    # the corpus's largest measured shortfall and are tracked in 99-Unresolved-Residual/.
    17: (0, "GHOST ADDRESS 0 - RE-MEASURED AT HEAD 5cf96b34 (OPUS) in a clean detached worktree, from the same audit_crossrefs run as passes 2, 4 and 22 plus verify_doc_addresses.py exit 0. The class is absent from the report. THE ONE UNLISTED CODE FINDING IS STILL 002FE7D0 on battle-action-handler-table.md, registered in Unlisted-Code/unlisted-code-blocks.tsv as census debt and named here rather than absorbed. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "GHOST ADDRESS 0, RE-MEASURED AT HEAD 6662e859 on 2026-09-17 (OPUS) in a clean detached worktree, same run as passes 2, 4 and 22: 2 findings across 410 documents. The single UNLISTED CODE finding is 002FE7D0, THIS PASS'S OWN REGISTERED CENSUS DEBT, recorded in unlisted-code-blocks.tsv and labelled by the report itself as census debt rather than a document defect - so the ghost-address class is 0 and the debt is visible rather than absorbed. WHAT THIS ROW SAID BEFORE, PRESERVED: GHOST ADDRESS 0. RE-MEASURED AT HEAD 114558e9 on 2026-09-16 (OPUS), 37 commits after the six-pass consolidation at 342d12f9, in a clean detached worktree: still 0, in the same audit_crossrefs run that carried passes 2, 4, 17 and 22 - 1 finding across 408 documents and it is the registered UNLISTED CODE census debt. EARLIER: measured at HEAD 342d12f9 on 2026-09-16 by OPUS in a clean detached worktree, 405 documents - the single finding is 002FE7D0, reclassified UNLISTED CODE: "
            "real .text the census lacks, registered and referenced, which is census debt "
            "rather than the pass-17 defect of citing data as a function"),
    # A HARDCODED COUNT IN A VERDICT TABLE GOES STALE, AND THIS ONE WENT STALE BY 356. It read
    # "1,052" while the audit reported 696, because the fleet dispositioned the difference. The
    # figure is dated now and points at the live sources; re-running audit_crossrefs from here
    # would cost 200 s on every invocation of a table that exists to be read quickly.
    # 2026-09-14 12:35 - THE COUNT IS ZERO AND THE PASS IS STILL NOT CLEAN, WHICH IS THE
    # honest state rather than a pessimistic one. The instrument reports 0 UNACCOUNTED
    # NEIGHBOUR against 1,052 when this row was first written, and the fall is reads and
    # dispositions, not removals - the count went UP twice on the way, +124 when FABLE's R4
    # stopped the alias table merging `combat` into three separately owned layers, and +2
    # when two clears that rested on the letters `ui` inside the word `requires` were
    # withdrawn. But FABLE ruled (PASS22-WHAT-ACCOUNTING-MEANS.md 4.4) that the pass does
    # NOT count toward 30/30 on the word test alone, and that ruling has not been revisited
    # against the current mix. A green instrument under a standing ruling is PARTIAL.
    # 2026-09-14, LATER - THIS ROW MOVES BACK TO RED, AND NOT ON THE QUESTION IT WAS WAITING FOR.
    # `OPUS-REVIEW-AUDITSPEC-PASS22-DISCHARGE` asked SWE2-AUDIT-SPEC whether R1 registry clearing
    # does more work than the protocol intends. Their answer (19bf0ace) CLEARS R1 - the
    # GENUINELY-IRRELEVANT / FALSE-SUBJECT rows carry per-row verifiable reasons and the sampled
    # claims verify against functions.tsv - and instead REJECTS "discharged once" as the wrong
    # instrument, then re-derives the count at HEAD: UNACCOUNTED NEIGHBOUR **1**.
    #
    # Re-run here independently: 1. The fifteen-modules page against Audio, 5 edges through the
    # shared `CreateEventA` thunk 005CD0A0, real, undispositioned, no registry row. The citation
    # entered in a1812431 at 17:30, AFTER the zero measured at 60c846be at 16:14 - so the zero was
    # real and section 9.8's predicted dynamic killed it inside an hour, exactly as written.
    #
    # THE ROW IS RED BECAUSE THE INSTRUMENT READS 1, NOT BECAUSE THE RULING CHANGED. FABLE's
    # section 11.4 stands: a non-zero neighbour count on any streak run is a failure that resets the
    # count. A row that said "clean" while the instrument read 1 would be the gate asserting a
    # measurement nobody could reproduce - and OPUS printed "30 clean" in eight publications after
    # 17:30 on that stale basis, which is the reason this comment is here rather than a silent edit.
    # Disposition routed to SWE2-FRONTIER as AUDITSPEC-REQ-FRONTIER-PASS22-AUDIO-NEIGHBOUR.
    # 2026-09-14, LATER STILL - THE EDGE IS DISPOSITIONED AND THE COUNT IS BACK TO 0.
    # OPUS read 005CD0A0 and 005CD0E0 from the shipping image: a 63-byte CREATE-ONCE GUARD around
    # CreateEventA (IAT 008C21A8), with 32 callers across SIX layers - NativeRoutine 13, Resource 5,
    # Phyre 5, Audio 5, EASTL 3, Presentation 1. The fifteen-modules page names it in ONE table cell,
    # as the tail-jump target of 00677450, which is the function that cell is about. So the subject
    # was mis-seeded: FALSE-SUBJECT, registered with the body read as its evidence.
    #
    # THE ROW IS WRITTEN ON MERITS AND THE APPEARANCE IS BAD, WHICH IS WHY THIS SAYS SO. Four hours
    # earlier OPUS published that a registry row written to keep a number still is inadmissible, and
    # FABLE upheld it. The test applied here is whether the row would be correct with no streak at
    # stake - five Audio calls to a shared Win32 event wrapper say nothing about a page on module
    # registration, so it would. A reader who distrusts that has the body read and the caller census
    # to check it against, which is the point of putting them in the row.
    22: (2, "THE CLASS IS NO LONGER EMPTY - UNACCOUNTED NEIGHBOUR 2 AT HEAD 5cf96b34 (OPUS), measured in a clean detached worktree, and this row is a CORRECTION rather than a re-date: it asserted 0 and 'THE CLASS IS EMPTY'. The two, out of 3 findings across 412 documents: 15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md, Developer, 1 edge - 0017D6E0 callee 001C2F50; and 22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md, Resource, 46 edges - 0062FFC0 callers 00585270, 005862F0, 00586470, 005865F0 and 42 more. BOTH PAGES WERE PUBLISHED TODAY BY FABLE (c776fd737, b574846c2 and a4076ce01 on the keymap page; d0e2d6dff on the Lua page), so this is the citation fan-out the pass-22 notes describe - a newly cited entry imports its neighbours - rather than a regression in the instrument. INDEPENDENTLY CORROBORATED: check_publish_neighbours, run twice today against the live tree for unrelated publishes, reported UNACCOUNTED NEIGHBOUR 2 at HEAD both times. AND THE CLASS IS STILL GROWING: a third check_publish_neighbours run, forty minutes later against a live tree whose HEAD had moved on to 90c62d194, reports UNACCOUNTED NEIGHBOUR 3 out of 4 findings. The 2 above is exact for 5cf96b34f and is already behind; the third is not identified here because it was seen in a differential, not in a clean-HEAD run, and this row does not name what it has not measured. Routed to FABLE, whose pages they are; the remedy is a crossing section or an accounted note, which belongs to the page owner. WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "UNACCOUNTED NEIGHBOUR 0 AT HEAD 34e07aeb - THE CLASS IS EMPTY, AND THE HONEST "
        "PART OF THAT SENTENCE IS THE COMMIT IN IT. audit_crossrefs reports 1 finding across "
        "412 documents and it is 002FE7D0, pass 17's REGISTERED census debt, so this pass's "
        "own kind is zero - the same basis on which passes 2, 4 and 17 are recorded clean in "
        "runs that report that same debt. "
        "THE COUNT MOVED TEN TIMES IN ONE SESSION: 21 -> 20 -> 18 -> 16 -> 11 -> 9 -> 5 -> 0 "
        "-> 2 -> 1 -> 0. The rises are all peer publishes and the first zero lasted exactly "
        "ONE COMMIT before a new page arrived. NINE PAGES were accounted here - the movement "
        "body pool, the VU0 register bank, five-small-bin-tables, derived-call-signatures, "
        "the clamp page, the blinking icon, the camera snapshot, the second console table and "
        "the save-load widgets - and SWE2-DATA cleared EIGHTEEN findings of their own across "
        "two pages within hours of being routed. "
        "ONE FINDING IN THREE OF THOSE PAGES WAS THE SAME 51-BYTE SOUND WRAPPER, and the "
        "reason is arithmetic rather than coupling: 00249C60 has NINETY-NINE callers against "
        "the >100 hub cut this surface excludes as substrate. One caller either way decides "
        "whether citing it costs a paragraph. Filed as "
        "OPUS-NOTICE-99-CALLERS-IS-SUBSTRATE-BY-ANY-READING - a question about SHAPE versus "
        "caller count, NOT a proposal to move a threshold to make a count fall. "
        "AND A PREMISE OF MINE WAS RETRACTED FROM THIS PROTOCOL TO GET HERE: I had routed "
        "three findings away as structural because 'an ABI-recovery page cites hundreds of "
        "functions by construction', while the same page already carried ELEVEN "
        "CROSSING-ACCOUNTED rows - one of them ActorEntity at 31 edges, marked OPUS-MULTI, "
        "which was mine. "
        "SECTION 11.4 IS NOT SATISFIED BY THIS AND THE ROW DOES NOT CLAIM IT IS: the class "
        "must be re-satisfied PER RUN with the pre-publish neighbour guard on every publish "
        "in that run. A ZERO TODAY IS A ZERO TODAY. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: UNACCOUNTED NEIGHBOUR 14 AT HEAD 6b7ced3f, "
        "AND ELEVEN OF THEM ARE ONE PAGE THAT "
        "DID NOT EXIST THIS MORNING. Measured 2026-09-18 by OPUS on `git archive HEAD` exports "
        "throughout, never on the working tree: 15 findings across 411 documents, of which 14 are "
        "this class and 1 is pass 17's registered census debt at 002FE7D0. "
        "THE SEQUENCE IS THE FINDING, AGAIN, AND THIS TIME IT RAN INSIDE ONE SESSION: 7 at "
        "8cd2a078, 4 after accounting, 5 before that accounting could be published, 4 again, then "
        "15 when SWE2-DATA's the-settings-command-table.md landed in 8a5bc471. NOT ONE OF THOSE "
        "MOVES CAME FROM ANYTHING DECAYING - every one is a peer publish, which is exactly why "
        "this pass cannot be held at zero by repair and why section 11.4's pre-publish neighbour "
        "guard on EVERY publisher is the only thing that could hold it. "
        "WHAT OPUS CLOSED TODAY, in two commits, all of it citation fan-out: 9405e0d1 accounted "
        "the three that arrived with 1a816977 - the-party-standard-motion-verbs.md against the "
        "spawn and encounter layer, where 24 of the 31 edges arrive through ActorWork_GetBattleUnit "
        "(0031B760), a THIRTEEN-BYTE null-guarded forwarder the spawn layer calls from 24 distinct "
        "bodies, and the-definition-record-flag-pair.md's two reads of "
        "WorldTransition_GetActiveOrPendingFieldId (003148F0, 27 B) verified at the call sites "
        "0026200F and 003160F3, the second of which the preceding query JUMPS OVER when it returns "
        "positive. Then 6b7ced3f accounted the boot page's Story_Event_Quest_Hunt edge: "
        "00253C70 asks PersistentFlag_QueryPrimaryOrAuthoredThresholdGate at TWO sites with "
        "constant ids 0x5E and 0x4008, and since the gate branches on bit 14 of its id, one site "
        "goes down each of its two routes. "
        "ONE OF THOSE FIXES WAS MEASURED BEFORE IT WAS WRITTEN AND THAT IS THE REUSABLE PART: "
        "naming the boot page's 122-byte callee BY ADDRESS would have made it a citation, and its "
        "own neighbours include a Script/VM Native Bridge edge that page does not mention - so "
        "clearing the Story finding that way would have opened a Script/VM one. It is named by "
        "SYMBOL instead. An address in an accounting paragraph is a new citation, and a new "
        "citation has neighbours. "
        "WHAT IS LEFT AND WHY OPUS IS NOT WRITING IT: three on derived-call-signatures.md "
        "(Items/Equipment/Shops/License 25, UI 31, Rewards 1), routed as "
        "OPUS-REQ-FABLE-PASS22-DERIVED-CALL-SIGNATURES-IS-THE-LAST-THREE, and eleven on "
        "the-settings-command-table.md, routed as "
        "OPUS-REQ-SWE2-DATA-PASS22-SETTINGS-COMMAND-TABLE-ELEVEN-LAYERS. BOTH ARE THE SAME SHAPE: "
        "a page that cites its handlers BY CONSTRUCTION, where the treatment that cleared every "
        "other page would mean naming dozens of layers for edges the page makes no claim about. "
        "Which of eleven layers a command table claims something about is the page owner's "
        "judgement, and guessing a class to clear a gate is what section 4.2 exists to forbid. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: UNACCOUNTED NEIGHBOUR 2 - THE ONE OPUS WAS ROUTED IS FIXED AND TWO NEW ONES ARRIVED "
        "WHILE IT WAS BEING FIXED. That sequence is the finding. "
        "FIXED: the Audio crossing on class-descriptor-and-metadata-system.md is accounted, and "
        "it is gone from the report. 005CD4F0 is a nine-byte ADJUSTOR THUNK - `lea rdx, [rcx + "
        "0x20]` then `jmp 005CD450` - carrying no behaviour of its own, and what the eleven Audio "
        "call sites use it FOR is 005CD450, a LOCK ACQUIRE: `lock xadd [rcx+0x18], 1` counts the "
        "waiter, `lock cmpxchg [rbx], 1` takes the flag at the thunk's +0x20 sub-object, and on "
        "contention the handle at +8 is waited on with an INFINITE timeout and the result tested "
        "against 0x80, WAIT_ABANDONED. Class CLIENT, evidence tier READ BODY for both functions "
        "and edges.tsv for the call sites. It also gave one of the tail-643 aux targets the "
        "provenance that page said it lacked. "
        "ARRIVED IN THE MEANTIME, both from peer batches and both single-edge: "
        "mg-worldmap-mesh.md against SaveLoad (00249210, caller 00582790) and "
        "CONTRACT-widget-object.md against ActorEntity (00273270 calling 003588B0, which is an "
        "encoded-id decoder - returns 0 for id 0, else shifts the id right by 0x14 for its class "
        "field). CONTRACT-widget-object.md's last commit is a2cfa20d, a FRONTIER block-20 batch. "
        "OPUS did NOT account for these two: it can state the ActorEntity one from the bytes but "
        "not yet what SaveLoad wants from 00249210, and guessing a class to clear a gate is the "
        "thing §4.2 exists to forbid. "
        "SO THE COUNT WENT 1 -> 0 -> 2 INSIDE ONE WORKING SESSION, which is the sharpest "
        "statement of the case already routed: THIS PASS CANNOT BE HELD AT ZERO BY REPAIR. Only "
        "the pre-publish neighbour guard running on EVERY publisher can hold it, which is exactly "
        "what section 11.4 requires of a streak run and exactly what is not yet true. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "UNACCOUNTED NEIGHBOUR 1 - REGRESSED AT HEAD 6662e859, AND IT LASTED ABOUT AN HOUR. Re-measured 2026-09-17 (OPUS) in a clean detached worktree with the graph exports junctioned in: 2 findings across 410 documents, one being pass 17's registered census debt and one being this. 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md against Audio: 11 edges never mentioned, anchored on 005CD4F0 with callers 00212050, 002120E0, 00212300, 00219C40 and seven more. ATTRIBUTED MECHANICALLY: that page's last commit is 8428f38e, SWE2-EC7's atexit-tail-643 decomposition. A batch publish raised the count again, which is the fourth time in three days this pass has moved on somebody's batch rather than on anybody's error - 1 to 40 to 1 to 10 to 0 and now to 1. THE PATTERN IS THE FINDING: this pass cannot be held at zero by repair, only by the pre-publish neighbour guard running on every publish, which is exactly what section 11.4 requires of a streak run and exactly what is not yet true of every publisher. Routed to SWE2-EC7. WHAT THIS ROW SAID WHEN IT WAS CLEAN, PRESERVED: UNACCOUNTED NEIGHBOUR 0 - CLEAN AT HEAD 5834fb05, THE FIRST TIME THIS PASS HAS BEEN "
        "CLEAN IN THIS SESSION. Re-measured 2026-09-17 by OPUS in a clean detached worktree against "
        "a report built in that same worktree: 1 finding across 410 documents, and it is the "
        "standing UNLISTED CODE 002FE7D0 - census debt registered in unlisted-code-blocks.tsv, "
        "which the report itself labels 'census debt, not a document defect' and which is pass 17's "
        "subject rather than this one's. "
        "SWE2-FRONTIER CLEARED NINE CROSSINGS IN ONE COMMIT: 5834fb05 'account nine unaccounted "
        "layer crossings; pass 30 green' - CombatAI, CombatAction and CombatFormula on "
        "native-command-lifecycle.md, Audio and UI on the-script-to-native-calling-convention.md, "
        "Input, Rewards_Progression_Economy, Gameplay and ActorEntity on four more. "
        "THE STANDING FINDING IS ALSO GONE: effect-mesh-records-kind-54.md against "
        "CoreRuntimeScheduling, the b85ffb4c shared-index amend that landed SWE2-DATA's pages under "
        "FABLE's subject so their author never ran the accounting, no longer appears. "
        "AN OPUS NEAR-MISS RECORDED BECAUSE IT IS THE SESSION'S RECURRING ERROR: OPUS measured 9 "
        "UNACCOUNTED NEIGHBOUR at 673b129a and was composing the routing when mechanical "
        "attribution showed all six affected documents had the SAME last commit - 5834fb05, THE "
        "FIX. The report predated the repair. Reporting it would have been the ninth instance of "
        "real evidence about the wrong population, and the attribution step that has been catching "
        "other agents' stale figures all day caught OPUS's own. RE-MEASURED AT HEAD BEFORE ANY "
        "CLAIM WAS MADE, which is the only reason this row says 0 instead of 9. "
        "WHAT THIS DOES NOT MEAN: the streak has not begun. final_audits is 0/30, section 11.4 "
        "requires all thirty passes re-satisfied PER RUN with the publish guard on every publish in "
        "that run, and this pass went 1 -> 40 -> 1 -> 10 -> 0 in two days on batch publishes alone. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "UNACCOUNTED NEIGHBOUR 1 - RECOVERED FROM 40, AND STILL NOT CLEAN. Re-measured at HEAD "
        "3ae38a40 on 2026-09-16 by OPUS in a clean detached worktree: 2 findings across 410 "
        "documents, and one is the standing UNLISTED CODE 002FE7D0 census debt. The single real "
        "finding is the one that was here this morning: effect-mesh-records-kind-54.md against "
        "CoreRuntimeScheduling, 2 edges to 00229E40, from b85ffb4c - the shared-index amend that "
        "landed SWE2-DATA's pages under FABLE's subject so their author never ran the accounting. "
        "Routed to SWE2-DATA and still open. THE 39 FROM BATCH-6 ARE GONE: SWE2-FRONTIER's a5232d9c "
        "('pass-22 batch-6 accounting, 39 neighbour crossings dispositioned') answered the routed "
        "request inside the day and cleared pass 30 with it. WHAT THE EPISODE COST AND WHY IT IS "
        "KEPT: one batch publish took this pass from 1 to 40 and the repair took it back to 1, so "
        "nothing was lost but the interval - and in that interval the repair itself broke pass 29 "
        "with three malformed relative links. A pass can be red, fixed, and the fix can regress a "
        "different pass, all inside one day; that is what section 11.4's per-run re-satisfaction is "
        "for, and it is why a streak cannot be assembled from passes measured on different commits. "
        "WHAT THIS ROW SAID AT ITS WORST, PRESERVED: "
        "UNACCOUNTED NEIGHBOUR 40 - AND IT WAS 1 THIS MORNING. Re-measured at HEAD 4e408893 "
        "on 2026-09-16 by OPUS in a clean detached worktree: 41 findings across 410 documents, 40 "
        "UNACCOUNTED NEIGHBOUR plus the standing UNLISTED CODE 002FE7D0. **39 OF THE 40 TRACE TO ONE "
        "COMMIT**, attributed mechanically by taking each affected document's last commit: 0cdb6009, "
        "'SWE2-FRONTIER batch-6: 47 subtree sections, five entry-only-large identifications, the "
        "authored-command family page, the D-4 fold and the UQ-24 carry'. 17 documents are affected; "
        "the heaviest are adm-add-motion-tables.md (13, across ActorEntity / CombatAI / CombatAction "
        "/ CombatFormula / Gameplay / Input / InputGameplay / Items / Movement / Party / Rewards / "
        "ScriptVM / Status), the-authored-presentation-command-handlers.md (6), "
        "the-resource-request-queue.md (3) and the-ordered-render-command-list.md (3). The 40th is "
        "effect-mesh-records-kind-54.md from b85ffb4c, already routed to SWE2-DATA. "
        "THIS IS THE CLEAREST DEMONSTRATION YET OF WHY THE PRE-PUBLISH GUARD EXISTS AND WHAT IT "
        "COSTS TO SKIP IT: one batch publish of 47 sections moved this pass from 1 to 40, and the "
        "guard run on that publish would have refused it. The guard costs 36 minutes a publish, "
        "which is the reason to batch publishes, not the reason to omit the guard. Section 11.4 "
        "makes a non-zero neighbour count on any streak run a failure that RESETS the count, so the "
        "terminal streak is further away than it was this morning. Routed to SWE2-FRONTIER. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: "
        "UNACCOUNTED NEIGHBOUR 1 - THIS PASS IS NOT CLEAN AT HEAD 205ad904, re-measured "
        "2026-09-16 by OPUS in a clean detached worktree: 2 findings across 409 documents. One is the "
        "standing UNLISTED CODE 002FE7D0, pass 17 census debt and not a document defect. THE OTHER IS "
        "A REAL PASS-22 FINDING AND IT IS THIS PASS'S OWN CLASS: "
        "17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md, domain "
        "CoreRuntimeScheduling, 2 edges never mentioned - 00434CD0 callee 00229E40 and 00435050 "
        "callee 00229E40. VERIFIED BY HAND rather than taken from the count: the page cites 00434CD0 "
        "once and 00435050 once, and mentions 00229E40 ZERO times and CoreRuntimeScheduling ZERO "
        "times. It is undispositioned, so nothing is suppressing it. HOW IT GOT IN IS THE PART WORTH "
        "READING. That page's last commit is b85ffb4c - the commit FABLE identified in "
        "OPUS-REQ-FABLE-AMEND-NOT-PUBLISH-IS-THE-SWEEP as having absorbed SWE2-DATA's kind-0x54 "
        "effect-mesh work, five files and 7,853 lines, under FABLE's subject through the shared-index "
        "`git commit --amend`. So THE SWEEP DID NOT ONLY MISATTRIBUTE WORK: it landed corpus content "
        "that never passed its author's pass-22 accounting, because the agent publishing it did not "
        "know the files were in the commit and the agent who wrote them did not know they had been "
        "published. The publication-integrity defect and this audit finding are the same event seen "
        "from two ends. Routed to SWE2-DATA, who wrote the page; accounting for a neighbour is a "
        "statement about that page's content and is not OPUS's to write. AND A MEASUREMENT WARNING "
        "THAT COST ME A WRONG NUMBER FIRST: run against the WORKING TREE this same audit reported 34 "
        "findings. The extra 32 are peers' UNCOMMITTED edits, not the corpus. A pass-22 figure is a "
        "property of a COMMIT, and a dirty tree inflates it silently - the clean detached worktree is "
        "not ceremony. The same run also rewrote the shared _index/candidates/pass22-tripwires.tsv in "
        "the main checkout as a side effect, from that same dirty state; it was restored with git "
        "checkout rather than left for a peer to publish. "
        "WHAT THIS ROW SAID BEFORE, PRESERVED: UNACCOUNTED NEIGHBOUR 0, RE-MEASURED AT HEAD 114558e9 on 2026-09-16 by OPUS in a clean detached worktree: 1 finding across 408 documents and it is UNLISTED CODE 002FE7D0, pass 17 census debt. THIRTY-SEVEN COMMITS OF FLEET WORK LANDED BETWEEN THIS READING AND THE SIX-PASS CONSOLIDATION AT 342d12f9 AND THE COUNT DID NOT MOVE - which is the opposite of what pass 29 did earlier the same day, when a morning clean was red by the afternoon from a peer publish. Both are the same lesson: the number is a property of a commit, not of the project. EARLIER: re-measured at HEAD 342d12f9 on 2026-09-16 by OPUS in a CLEAN DETACHED WORKTREE with the committed instrument: 1 finding across 405 documents and it is UNLISTED CODE 002FE7D0, pass 17 census debt; 141 pairs dispositioned by the registry (CROSSING-ACCOUNTED 11, FALSE-SUBJECT 7, GENUINELY-IRRELEVANT 123). THE ROW ALREADY SAID 0 AND I RE-RAN IT ANYWAY, which is the only part of this worth reading: the previous reading was taken at 05926097, TWENTY-SEVEN COMMITS BACK, over 403 documents rather than 405 - so two documents had entered the corpus that the standing verdict had never seen. It still reads 0. FABLE made this argument first in 342d12f9 about pass 24 and it is general: a verdict measured commits ago is not evidence about now, and the commits in between are the ones most likely to have broken something. SECTION 11.4 STILL FORBIDS A STREAK HERE - a zero today is a zero today. WHAT THIS ROW SAID BEFORE, PRESERVED: UNACCOUNTED NEIGHBOUR 0, re-measured at HEAD 05926097 on 2026-09-16 by OPUS in a CLEAN DETACHED WORKTREE with the committed instrument: 1 finding across 403 documents and it is UNLISTED CODE 002FE7D0, which belongs to pass 17 as census debt. The five findings this row carried this morning were closed by FABLE in 2f8cf337, which landed accounting sentences for all five - and FABLE's own message records that TWO OF THE FIVE WERE FABLE'S. SWE2-FRONTIER verified independently with the pre-publish differential (0 -> 0) before I did, so this zero has three witnesses on two instruments. THE ROW IS CLEAN AND THE STREAK STILL CANNOT START: section 11.4 makes pass 22 re-satisfied PER RUN, so a zero today is a zero today, and pass 24 is not clean (pass 30 returned to clean the same day). WHAT THIS ROW SAID BEFORE, PRESERVED: WOULD FAIL TODAY - UNACCOUNTED NEIGHBOUR 5, measured at HEAD 7f2008b1 on 2026-09-16 by OPUS with the committed instrument. THE PREVIOUS READING WAS TAKEN TWO DAYS AND SEVERAL HUNDRED COMMITS AGO AND THIS ROW WENT ON ASSERTING IT. The five, four documents: 01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md vs Input, 1 edge, 00358940 caller 00226BE0; 04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md vs Movement, 2 edges, 00266530 callee 00265FF0 and 00266530 callee 00268380; 15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md vs Party, 1 edge, 0017DFC0 caller 003594E0; 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/katano-debug-savedata.md vs Audio, 1 edge, 002DDE60 callee 002DF530, and vs Input, 2 edges, 002DDE60 callee 001E0FF0 and 002DDE60 callee 001E1020. HOW IT WAS MEASURED, because the number depends on it: the tool reads the WORKING TREE, and the working tree carried heavy uncommitted peer work. Run against it the count is 41 across 17 documents, 12 of which are dirty. Run in a clean detached worktree at HEAD it is 5 across 4. THE 41 IS NOT THE PASS-22 NUMBER AND THE 5 IS - a pass is measured at HEAD, and reporting 41 would have charged peers for work they have not published. The registry dispositioned 140 pairs in the same run (CROSSING-ACCOUNTED 11, FALSE-SUBJECT 7, GENUINELY-IRRELEVANT 122), so these 5 are what survives it. UNLISTED CODE 1 (002FE7D0) also stands and belongs to pass 17. PER FABLE SECTION 11.4 A NON-ZERO NEIGHBOUR COUNT ON ANY STREAK RUN IS A FAILURE THAT RESETS THE COUNT, so no streak may begin here. Routed to the four documents' owners. THE GUARD'S COST IS 36 MINUTES A PUBLISH, NOT FIVE, AND THAT BELONGS IN THE STREAK PLAN. The preserved text below says the pre-publish guard 'now costs about five minutes a publish rather than the tens of minutes that were the real reason to skip it'. Measured 2026-09-16 on an OPUS publish with check_publish_neighbours wired into pub_once for the first time: 36 minutes wall. The guard is NOT doing wasteful work - it is already sparse-checked to the DB subset, 8,736 files per worktree rather than a full 7,317-file checkout twice - so this is a figure to correct rather than a defect to fix. It matters because section 11.4 requires the guard on EVERY publish in a streak run, and thirty runs of publishes at 36 minutes each is a schedule, not a footnote. OPUS's adaptation is to batch publishes. WHAT THIS ROW SAID BEFORE, PRESERVED: UNACCOUNTED NEIGHBOUR 0, re-measured at HEAD bc37bc30 on 2026-09-14 by OPUS. THE ROW WAS AT 1 FOR ABOUT AN HOUR AND THAT IS KEPT HERE ON PURPOSE - a zero with no account of how it was reached is the thing this protocol is supposed to prevent. WHAT HAPPENED: UNACCOUNTED NEIGHBOUR 1, measured at HEAD 2cfd6913 on 2026-09-14 by OPUS with the committed instrument: 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md against RNG_Random_Selection, 1 edge, 0022A0B0 callee 00379CF0 RNG_MT19937_Seed. IT IS A REGRESSION AND ITS ORIGIN IS KNOWN: babab7ec added section 15 to that page, citing 0022A0B0 at line 687 - after the crossing section and under its own ## heading, so outside the R6 guard. 0022A0B0 is a 978-byte CoreRuntimeScheduling boot initialiser that calls 51 subsystem initialisers; the crossing is the seed call, a five-byte thunk, and one section-4.2 sentence naming that edge and its class closes it. Routed to SWE2-FRONTIER, who published babab7ec, as OPUS-REQ-FRONTIER-PASS22-CRR-RNG-EDGE. THIS ROW IS NOT BEING HELD AT 0 WHILE THE CORPUS SAYS OTHERWISE. FABLE section 11.4 is explicit that a non-zero neighbour count on any streak run is a failure that resets the count, and this is exactly the case it describes - a regression that got past a guard. It is also the first demonstration that the pre-publish guard was needed and was not yet fleet-wide when babab7ec landed. HOW IT CLOSED: SWE2-FRONTIER landed 8f2bcc4d 'Request fixes: CRR RNG-edge accounting' inside the hour, accounting for the edge at line 686 of that page - the startup hub's rng seeding - and the count returned to 0 on the next measurement. Total time from the regression reaching HEAD to a clean re-measurement: one routed request. THE LESSON IS NOT THAT IT WAS CHEAP TO FIX, IT IS THAT IT REACHED HEAD AT ALL: this is the class the pre-publish guard refuses, the guard now costs about five minutes a publish rather than the tens of minutes that were the real reason to skip it, and no streak run should be started without it having been run on every publish in that run. WHAT THIS ROW SAID BEFORE, PRESERVED: UNACCOUNTED NEIGHBOUR 0 - the Audio edge that failed this row was dispositioned "
            "FALSE-SUBJECT on a body read (005CD0A0 is a create-once CreateEventA guard with 32 "
            "callers across six layers; the page names it as 00677450's tail-jump target). "
            "WHAT THIS ROW SAID BEFORE, PRESERVED: "
            "WOULD FAIL TODAY - UNACCOUNTED NEIGHBOUR 1, re-derived 2026-09-14 by SWE2-AUDIT-SPEC "
            "(19bf0ace) and independently here: the fifteen-modules page against Audio, 5 edges "
            "through the shared CreateEventA thunk 005CD0A0, undispositioned and with no registry "
            "row. Routed to SWE2-FRONTIER. The review that could have moved this row CLEARED R1 - "
            "registry rows sample-verify against functions.tsv - and rejected 'discharged once' as "
            "the wrong instrument instead. WHAT THE EARLIER CLEAN READING WAS, PRESERVED: "
            "CLEAN, on FABLE's adjudication - not on mine. UNACCOUNTED NEIGHBOUR 0 on the "
            "committed instrument (R1 + R3 clauses 1+2 + R4 + R5 + guarded R6 + R7) across 394 "
            "documents; the only other finding is UNLISTED CODE 002FE7D0, which belongs to pass 17. "
            "FABLE discharged it in PASS22-WHAT-ACCOUNTING-MEANS.md section 11 after re-deriving "
            "the zero from the committed tool on their own export and attacking R6, which OPUS had "
            "flagged as the rule carrying the whole result: with R6 off, 40 pairs across 23 "
            "documents; four far ends checked BY HAND (005CC930, 00263C20, 00326BB0, 002628B0), "
            "each occurring exactly once, inside its page's crossing section, in a section-4.2 "
            "sentence naming the far end of an edge that sentence accounts for; and every one of "
            "the 40 resting on an address the page also cites outside the section, which is the "
            "guard doing its job. "
            "WHAT THE STREAK INHERITS (section 11.4): a pass-22 run uses the committed instrument, "
            "must report UNACCOUNTED NEIGHBOUR 0, and reads every other class under the pass that "
            "owns it. A NON-ZERO NEIGHBOUR COUNT ON ANY STREAK RUN IS A FAILURE THAT RESETS THE "
            "COUNT. That answers the instability OPUS raised - the zero read 0 and then 2 an hour "
            "later when peers published - not by denying it but by putting it where it belongs: "
            "pass 22 is re-satisfied per run, like every other pass, rather than discharged once. "
            "TWO DEFECTS FABLE FOUND IN OPUS'S APPLICATION, both corrected 2026-09-15 and neither "
            "changing a count: R6 was removing far ends from `cited` before checks 1-3, so a wrong "
            "size written beside a far end would have escaped body drift later - it is now scoped "
            "to the neighbour enumeration alone; and ADDR_R5 accepted bare lowercase hex, which "
            "section 9.7 had dropped on OPUS's own widening measurement - the tool now says what "
            "the ruling says. "
            "STILL OPEN, and it could reopen this row: OPUS-REVIEW-AUDITSPEC-PASS22-DISCHARGE asks "
            "SWE2-AUDIT-SPEC whether R1 registry clearing - 137 pairs today - does more work than "
            "the protocol intends, which is the one thing OPUS cannot review impartially because "
            "most of those rows are OPUS's. FABLE's ruling does not cover it. A finding there is a "
            "reason to move this row back."),

}


def main():
    if not os.path.isfile(BASE):
        print("no gate baseline at %s - run run_gates.py --write-baseline first" % BASE)
        return 2
    state = {}
    for line in io.open(BASE, encoding="utf-8", errors="replace"):
        if line.startswith("#"):
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) >= 2 and f[1].strip().isdigit():
            state[f[0].strip()] = int(f[1])

    red, green, unmech, notgate, partial = [], [], [], [], []
    print("FINAL-AUDIT READINESS - what the thirty passes would do today")
    print("(a green row means THE MECHANISED PART is clean, never that the pass is satisfied)\n")
    for n in sorted(PASSES):
        name, tools = PASSES[n]
        # PER_PASS FIRST. It was consulted only in the has-tools branch, so pass 5 - which has no
        # kit instrument and a recorded partial verdict - fell into "no state" while its verdict
        # sat one dict away. A result that exists and is not read is the defect this whole map
        # was written to find.
        if n in PER_PASS:
            code, note = PER_PASS[n]
            # 2 is PARTIAL, and it is deliberately not folded into clean. Pass 5's four artifacts
            # verify and its FRESH IMPORT does not run from here; calling that clean would be the
            # flattering half of a two-part answer, which is the failure this file exists to catch.
            tag = {0: "clean", 1: "RED", 2: "PARTIAL"}[code]
            (red if code == 1 else partial if code == 2 else green).append(n)
            age = verdict_age(note)
            art = AT_ARTEFACT.search(note or "") if n in ARTEFACT_PASSES else None
            if age is None and art is not None:
                stamp = "  [measured against snapshot %s, not a commit]" % art.group(1)
            elif age is None:
                stamp = "  [no measuring commit named]"
            elif age > STALE_AFTER:
                stamp = "  [measured %d commits ago - RE-MEASURE]" % age
            else:
                stamp = "  [measured %d commit(s) ago]" % age
            print("  %2d  %-26s  %-8s%s %s" % (n, name, tag, stamp, note))
            if n in EXECUTED:
                print("      run: %s" % EXECUTED[n])
            continue
        if not tools:
            if n in EXECUTED:
                print("  %2d  %-26s  RUN      %s" % (n, name, EXECUTED[n]))
                green.append(n)
            else:
                unmech.append(n)
                print("  %2d  %-26s  -- no instrument, never recorded as run" % (n, name))
            continue
        # A TOOL THAT IS NOT IN THE BASELINE HAS NO STATE, AND THE FIRST CUT OF THIS FILE SCORED
        # IT AS CLEAN - so passes 1, 2, 4, 17 and 22, whose ONLY instruments run_gates does not
        # invoke, printed "clean" on no evidence at all. That is the defect this whole readiness
        # exercise exists to find, committed by the instrument measuring it. Unknown is its own
        # state and never folds into clean.
        if n in PER_PASS:
            code, note = PER_PASS[n]
            tag = {0: "clean", 1: "RED"}[code]
            (red if code else green).append(n)
            print("  %2d  %-26s  %-8s %s" % (n, name, tag, note))
            if n in EXECUTED:
                print("      run: %s" % EXECUTED[n])
            continue
        marks = []
        worst = 0
        unknown = 0
        selftest_only = bool(tools) and all(t in SELFTEST_GATES for t in tools)
        for t in tools:
            if t in state:
                marks.append("%s=%d" % (t, state[t]))
                worst = max(worst, state[t])
            elif t in DIRECT:
                code, note = DIRECT[t]
                marks.append("%s=%d(hand)" % (t, code))
                worst = max(worst, code)
            else:
                marks.append("%s=NO-STATE" % t)
                unknown += 1
                notgate.append((n, t))
        if worst > 0:
            tag = "RED" if worst == 1 else "REFUSES"
            red.append(n)
        elif unknown == len(tools):
            tag = "UNKNOWN"
            unmech.append(n)
        elif unknown:
            tag = "partial"
            green.append(n)
        elif selftest_only:
            # THE BASELINE ENTRY FOR THESE IS A --self-test RESULT. run_gates maps
            # them through NOT_A_CORPUS_GATE because they do not take --db, so a 0
            # means the instrument parses its own fixtures - it is not a reading of
            # the corpus and must never print as one. Same shape as the unknown
            # state above: passes 24 and 30 printed clean on this for as long as the
            # map has existed, and both are FINAL-AUDIT blockers.
            tag = "SELFTEST"
            partial.append(n)
        else:
            tag = "clean"
            green.append(n)
        print("  %2d  %-26s  %-8s %s" % (n, name, tag, "  ".join(marks)))
        if n in EXECUTED:
            print("      run: %s" % EXECUTED[n])

    print("\n  mechanised and clean today : %d passes  %s" % (len(green), green))
    print("  WOULD FAIL TODAY           : %d passes  %s" % (len(red), sorted(red)))
    print("  PARTIAL / SELF-TEST ONLY   : %d passes  %s" % (len(partial), sorted(partial)))
    print("  hand pass OR no state      : %d passes  %s" % (len(unmech), sorted(unmech)))

    # PROVENANCE, ADDED 2026-09-17 (OPUS), BECAUSE THE FOUR LINES ABOVE CAN READ AS 30/30.
    # On this date every one of the thirty printed `clean` for the first time, and that is NOT a
    # streak and not a readiness: section 11.4 requires every pass re-satisfied PER RUN, so a run
    # is thirty passes measured TOGETHER with the publish guard on every publish inside it.
    # A row that cannot name the commit it was measured at cannot join a run, because nothing can
    # decide whether it was measured inside that run or two hundred commits before it. That is a
    # WEAKER position than a stale row: a stale verdict can be dated and re-run, an undated one
    # cannot even be interrogated. The split is printed rather than left to be counted by hand,
    # because it was counted by hand once and the hand-written parser got it wrong - it put three
    # freshly stamped rows in the undated bucket, and only a direct grep caught it.
    fresh, stale, artefact, undated = [], [], [], []
    for n in sorted(PASSES):
        if n not in PER_PASS:
            undated.append(n)                       # rests on the gate baseline: no HEAD, no date
            continue
        note = PER_PASS[n][1]
        age = verdict_age(note)
        if age is None:
            # Pass 5 and its kin are measured against a SNAPSHOT rather than a commit. That is a
            # real provenance and must not be filed under "names nothing" - the row can be placed,
            # just not on this axis. Calling it undated would be the same imprecision this block
            # exists to expose, committed by the block itself.
            art = AT_ARTEFACT.search(note or "") if n in ARTEFACT_PASSES else None
            (artefact if art is not None else undated).append(n)
        else:
            (stale if age > STALE_AFTER else fresh).append(n)
    print("\n  PROVENANCE OF THOSE VERDICTS - a colour is not a date")
    print("    measured at a named commit within %d : %d passes  %s"
          % (STALE_AFTER, len(fresh), fresh))
    print("    named a commit but are STALE         : %d passes  %s" % (len(stale), stale))
    print("    measured against a SNAPSHOT          : %d passes  %s" % (len(artefact), artefact))
    print("    NAME NO MEASURING COMMIT AT ALL      : %d passes  %s" % (len(undated), undated))
    if len(fresh) < len(PASSES):
        print("    => NOT A STREAK RUN. %d of %d verdicts cannot be placed in time, so they cannot"
              % (len(PASSES) - len(fresh), len(PASSES)))
        print("       be re-satisfied 'per run' in any sense section 11.4 would accept.")
    if notgate:
        print("\n  named by the protocol but NOT in the gate baseline - these are real tools that")
        print("  run_gates does not invoke, so their state here is unknown, not clean:")
        for n, t in sorted(set(notgate)):
            print("    pass %-2d  %s" % (n, t))
    return 0


if __name__ == "__main__":
    sys.exit(main())
