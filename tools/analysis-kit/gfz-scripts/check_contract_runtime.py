#!/usr/bin/env python3
"""check_contract_runtime.py - does a contract's section 13 agree with the experiments naming it?

WHAT THIS CATCHES THAT NOTHING ELSE DOES. The project's runtime evidence lives in the experiment
records under `_experiments/`, and no subsystem-facing instrument reads them: they are indexed with
`is_template = 1`, so every `is_template = 0` query in `knowledge_db.py` drops all 36. A contract can
therefore sit for months saying "None. Empty deliberately, and this is the gate the subsystem fails"
while a COMPLETE experiment record names it.

**WHAT THE FIRST RUN ACTUALLY FOUND, stated exactly rather than rounded up.** ZERO contracts are
understated *by the matchable link*, because the two that are understated in substance -
`CONTRACT-script-to-native-bridge` against `EXP-013` and `CONTRACT-group-completion-and-respawn`
against `EXP-011` and `EXP-014` - carry PROSE in their records' `contract:` key rather than a path,
so this check refuses to link them and lists them below instead. The understated count is 0 and the
real number is 2; the gap between those is the `contract:` key not being maintained as a link, which
is the defect this check makes visible. Of 22 contracts exactly TWO are linked by path.

TWO DIRECTIONS, AND THE SECOND IS THE DANGEROUS ONE:

  UNDERSTATED  section 13 denies validation that a RAN experiment record reports. A stale document.
  OVERSTATED   section 13 cites validation no experiment record supports. A false claim of evidence,
               and the reason this check reports contracts with no record at all rather than
               silently passing them.

**UNDERSTATED IS NOT AUTOMATICALLY A DEFECT, AND THIS IS THE POINT THE CHECK EXISTS TO MAKE
VISIBLE.** The charter separates static, isolated original-code, live, and integrated proof. Section
13 is one none-or-some field, so a contract with isolated original-code evidence and no live capture
can only say "None" - understating what exists - or claim validation it does not have. Both of the
contracts this check first flagged are in exactly that position: `EXP-013` ran the ORIGINAL BYTES of
`00267E10` and `00267DB0` under Unicorn with a SHA-gated reader and a stubbed `008620C0`, and
`EXP-011` is a differential against a reconstruction. Neither is a live capture, and both are real
evidence. **A flag here means "section 13 and the record disagree about what exists", not "someone
was careless".** Resolve it by naming the class, not by deleting the "None".

MATCHING IS BY THE EXPERIMENT'S OWN `contract:` KEY AND IS NEVER GUESSED. A record whose key is a
path is linked to that path. A record whose key is prose - "group completion - isolated invocation
and state validation" - is REPORTED UNMATCHED, because deciding which contract that means is a
judgement, and a false link in an evidence database is worse than an unlinked record. Five records
were in that state when this was written and they are listed for routing, not resolved.

STATUS IS TAKEN LITERALLY: only RUN, COMPLETE, VALIDATED or REPRODUCED count as having produced an
observation. PREPARED, PARTIAL, INCOMPLETE, CHECKPOINT and OVERTURNED do not - a PREPARED experiment
is a plan.

POSITIVE CONTROL: `CONTRACT-field-music-selection` is named by two records, one reporting 400 cases
over the game's own data with 0 mismatches. If the matcher does not link it, the run exits 2 and
reports nothing, because a linker that links nothing would show a clean board.

Exit codes: 0 clean, 1 disagreements found, 2 the control failed.
"""
import argparse
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA"))
S13 = re.compile(r"^##\s*13\.[^\n]*\n(.*?)(?=^##\s|\Z)", re.S | re.M)
FM = re.compile(r"^---\n(.*?)\n---", re.S)
RAN = ("RUN", "COMPLETE", "VALIDATED", "REPRODUCED")
# A denial is section 13 ANSWERING "none", not the word "none" occurring inside it. The first
# version matched both and produced two false positives (ASTRA-REQ-OPUS-METADATA-CONSUMPTION,
# 2026-09-13): `changes **none** of the 520 bytes` in the target-buffer contract, and
# `none of them survives` in the RNG contract -- the latter matched `^None` only because the PROSE
# HAPPENED TO WRAP there, which is a formatting accident rather than content.
#
# So the token must be LINE-INITIAL (bold markers and blockquote quoting allowed) and must not
# continue as a noun phrase: "None of ..." describes, "None." and "**None**" answer. The documented
# real form `**None.** Empty deliberately, and this is the gate the subsystem fails` still matches,
# and that is the control proving the narrowing did not silence the check.
DENIES = re.compile(r"^[>\s]*\*{0,2}None\b(?! of )|never been executed|not been executed"
                    r"|there is no runtime|no runtime validation", re.I | re.M)
CITES = re.compile(r"EXP-\d+", re.I)

# A contract may name a record that does not exist yet, PROVIDED it says so on the spot.
# See the classification below for why that is honest rather than overstated.
DISCLAIMED = re.compile(r"not yet written|not written yet|does not exist|no link until|"
                        r"claimed, not|pending|to be written|not yet recorded", re.I)


def near(sec, eid, span=260):
    """The text around a cited id: enough to carry a disclaimer on the same line or clause."""
    i = sec.upper().find(eid.upper())
    if i < 0:
        return ""
    return sec[max(0, i - span):i + span]


def frontmatter(text):
    m = FM.match(text)
    out = {}
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip()
    return out


# UNLINKED PAIRS ADJUDICATED AND ACCEPTED. Not a pattern - a named list with a reason each, so a
# pair nobody has argued still fails. Excusing every UNLINKED row would turn off the check that
# found this one.
#
# The `contract:` key means WHAT THE RECORD WAS DESIGNED TO TEST; section 13 cites WHAT THE
# CONTRACT IS ENTITLED TO USE. Those are different relations and the corpus indexes one direction,
# so an asymmetry here can be correct on both sides rather than a broken link.
ACCEPTED_UNLINKED = {
    "15-Input/Binding-Profiles/CONTRACT-binding-profiles.md": (
        "EXP-005 and EXP-006 are HARNESS-CAPABILITY questions and say so - 'can the game be driven "
        "by writing the input state it reads?' and 'measures the key-to-index mapping and the "
        "harness's reach, not a contract claim'. Answering the first required resolving the "
        "manager -> backend -> device-block -> byte-array chain IN A LIVE PROCESS, and that chain "
        "IS this contract's read path; the second measured the key-to-index mapping, which is this "
        "contract's subject. Designed for one thing, evidence for another - and evidence produced "
        "without the contract in view is MORE independent, not less. Rewriting either `contract: "
        "none` into a link would make the record say something false about its own design. "
        "Adjudicated 2026-09-14 (OPUS) from the records themselves, closing "
        "OPUS-REQ-ASTRA-EXP005-006-CONTRACT-KEY, which asked ASTRA to choose between two answers "
        "when the right answer is that both sides are already correct."),
    "00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md": (
        "EXP-100's frontmatter reads `contract: ../10-Status-Periodic-Terminal/"
        "CONTRACT-auto-status-rebuild.md`, and that is CORRECT - it was designed to test the "
        "auto-status gate chain. Executing 00322C50 was a means to that end: the auto-status "
        "rebuild reaches equipment validity through it, so the record drove arm 6 and recorded it "
        "as real. The encoded-id contract is entitled to cite that execution of ITS validator "
        "without the record being about the encoded-id space, which is the asymmetry this table's "
        "header describes. Rewriting EXP-100's `contract:` key would make it claim a design it did "
        "not have. SECTION 13 ALREADY SCOPES THE CITATION HONESTLY - arm 6 of 32, inside another "
        "contract's experiment, with the fill, both wrappers and the rebase pass named as static "
        "reads. SELF-ADJUDICATED, AND SAID SO: OPUS wrote both the contract and this entry on "
        "2026-09-20, so this is the author excusing his own citation and deserves an independent "
        "look - filed as OPUS-NOTICE-SELF-ADJUDICATED-UNLINKED-PAIR. If the reviewer disagrees, the "
        "fix is to delete this entry, not to weaken section 13."),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DB)
    a = ap.parse_args()
    exp_dir = os.path.join(a.db, "_experiments")

    by_path, prose = {}, []
    for p in sorted(glob.glob(os.path.join(exp_dir, "*.md"))):
        fm = frontmatter(io.open(p, encoding="utf-8", errors="replace").read())
        key, status = fm.get("contract", ""), fm.get("status", "")
        if not key:
            continue
        ran = status.upper().startswith(RAN)
        if ".md" in key:
            tgt = os.path.normpath(os.path.join(exp_dir, key.split("(")[0].strip().strip("`")))
            by_path.setdefault(tgt, []).append((os.path.basename(p), status, ran))
        elif not key.lower().startswith("none"):
            prose.append((os.path.basename(p), key, status, ran))

    contracts = sorted(glob.glob(os.path.join(a.db, "**", "CONTRACT-*.md"), recursive=True))
    linked = [c for c in contracts if os.path.normpath(c) in by_path]
    if not any("field-music-selection" in c for c in linked):
        print("CONTROL FAILED - the record that names CONTRACT-field-music-selection by path was not")
        print("linked, so the matcher is not working and a clean board here would mean nothing.")
        return 2

    print("CONTRACT SECTION 13 vs THE EXPERIMENT RECORDS THAT NAME IT")
    print()
    print("  contracts %d   records naming one by path %d   naming one in prose %d"
          % (len(contracts), sum(len(v) for v in by_path.values()), len(prose)))
    print()

    understated, overstated, unlinked, pending_rows = [], [], [], []
    have = {os.path.basename(p).split("-")[0] + "-" + os.path.basename(p).split("-")[1]: p
            for p in glob.glob(os.path.join(exp_dir, "EXP-*.md"))}
    for c in contracts:
        body = io.open(c, encoding="utf-8", errors="replace").read()
        m = S13.search(body)
        sec = m.group(1) if m else ""
        denies = bool(DENIES.search(sec))
        recs = by_path.get(os.path.normpath(c), [])
        ran = [r for r in recs if r[2]]
        if denies and ran:
            understated.append((c, ran))
        cited = sorted(set(x.upper() for x in CITES.findall(sec)))
        if cited and not recs:
            # THE DISTINCTION THIS CHECK LEARNED FROM ITS FIRST FLAG. Citing a record that does not
            # name the contract back is a BROKEN LINK, not a false claim of evidence. The first run
            # flagged CONTRACT-binding-profiles, whose section 13 is exemplary - it cites EXP-005 and
            # EXP-006, gives the live pointer chain they resolved, and lists what is NOT validated -
            # while both records carry `contract: none - a harness-capability question`. The two
            # sides disagree about whether the evidence belongs to the contract, and the contract is
            # the side that is right. Only a cited record that DOES NOT EXIST is an overstatement.
            missing = [e for e in cited if e not in have]
            # AND THE SECOND DISTINCTION, learned the same way (2026-09-14, OPUS). A contract that
            # names a record it knows is not written yet, AND says so, is not overstating -- it is
            # doing the most honest thing available. CONTRACT-resource-entry-tree's section 13
            # reads "`EXP-083` (claimed, not yet written -- no link until the record exists)", and
            # refuses to link it precisely so no reader mistakes it for evidence. Reporting that as
            # "a false claim of evidence" is backwards, and teaching authors that naming a pending
            # record is punished while staying silent is not would make section 13 less truthful,
            # not more. It is reported as PENDING, visibly, and does not fail the gate; a bare id
            # with no such disclaimer still does.
            pending = [e for e in missing if DISCLAIMED.search(near(sec, e))]
            missing = [e for e in missing if e not in pending]
            if pending:
                pending_rows.append((c, pending))
            if missing:
                overstated.append((c, missing))
            elif not pending:
                unlinked.append((c, cited))

    print("UNDERSTATED - section 13 denies validation a RAN record reports (%d):" % len(understated))
    for c, ran in understated:
        print("  %s" % os.path.relpath(c, a.db).replace("\\", "/"))
        for n, st, _ in ran:
            print("      %-44s %s" % (n[:44], st[:58]))
    if understated:
        print("  Resolve by naming the EVIDENCE CLASS in section 13 - isolated original-code is not")
        print("  a live capture and neither is nothing. Do not simply delete the 'None'.")
    print()
    print("OVERSTATED - section 13 cites an EXP record that DOES NOT EXIST (%d):" % len(overstated))
    for c, missing in overstated:
        print("  %-58s %s" % (os.path.relpath(c, a.db).replace("\\", "/"), ", ".join(missing)))
    print()
    print("PENDING - section 13 names a record it says is NOT YET WRITTEN (%d):" % len(pending_rows))
    for c, pend in pending_rows:
        print("  %-58s %s" % (os.path.relpath(c, a.db).replace("\\", "/"), ", ".join(pend)))
    if pending_rows:
        print("  Not a defect and not fatal: the contract names the record it is waiting on AND")
        print("  says it does not exist, which is more useful to a reader than silence. It becomes")
        print("  OVERSTATED the moment the disclaimer goes without the record arriving.")
    print()
    accepted = [(c, cited) for c, cited in unlinked
                if os.path.relpath(c, a.db).replace("\\", "/") in ACCEPTED_UNLINKED]
    unlinked = [(c, cited) for c, cited in unlinked if (c, cited) not in accepted]
    if accepted:
        print("UNLINKED, ADJUDICATED AND ACCEPTED - both sides correct (%d):" % len(accepted))
        for c, cited in accepted:
            rel = os.path.relpath(c, a.db).replace("\\", "/")
            print("  %-58s %s" % (rel, ", ".join(cited)))
            print("      %s" % ACCEPTED_UNLINKED[rel])
        print()
    print("UNLINKED - section 13 cites a real record that does not name this contract back (%d):"
          % len(unlinked))
    for c, cited in unlinked:
        print("  %-58s %s" % (os.path.relpath(c, a.db).replace("\\", "/"), ", ".join(cited)))
    if unlinked:
        print("  Not a false claim: the contract is citing evidence that exists.")
        print()
        print("  AND USUALLY NOT A STALE RECORD EITHER. The `contract:` key means WHAT THIS")
        print("  EXPERIMENT WAS DESIGNED TO TEST, not what may later cite it. EXP-005 and EXP-006")
        print("  carry `contract: none - a harness-capability question`, which is accurate: they")
        print("  were not run against a contract. CONTRACT-binding-profiles citing the live pointer")
        print("  chain they resolved is also accurate. **Both sides are right**, and evidence")
        print("  produced without the contract in view is MORE independent, not less.")
        print()
        print("  So the remedy is not to rewrite a correct `contract: none` into a link - that")
        print("  would make the record say something false about its own design. A record whose")
        print("  key is EMPTY is a bookkeeping gap; one that says `none` WITH A REASON is a")
        print("  declaration, and this row is then a cross-reference the corpus simply does not")
        print("  index in that direction. (Earlier text here said 'fix it there and this line")
        print("  clears', which would have had the record edited to suit the checker.)")
    print()
    print("RECORDS NAMING A CONTRACT IN PROSE - not matched, listed for routing (%d):" % len(prose))
    for n, key, status, ran in prose:
        print("  %-42s %s%s" % (n[:42], "RAN  " if ran else "     ", key[:58]))
    print()
    print("  A prose key is deliberately not resolved here. Give the record a PATH in its")
    print("  `contract:` frontmatter and it becomes checkable.")
    return 1 if (understated or overstated or unlinked) else 0


def self_test():
    """Both directions of DENIES. The negatives are the two false positives this pattern actually
    produced; the positives are the control, because a narrowing that silences a genuine denial is
    worse than the bug it fixes."""
    cases = [
        # the reported false positives -- the word "none" INSIDE a sentence
        ("changes **none** of the 520 bytes", False),
        ("an ordering fact and\nnone of them survives being cut", False),
        ("the cap refusal, and that it changes **none** of the 520 bytes | **agrees**", False),
        # genuine denials -- section 13 ANSWERING "none"
        ("**None.** Empty deliberately, and this is the gate the subsystem fails", True),
        ("None", True),
        ("None.", True),
        ("**None**", True),
        ("> None. nothing live here", True),
        ("it has never been executed", True),
        ("there is no runtime validation", True),
        ("no runtime validation exists for this contract", True),
    ]
    bad = 0
    for text, want in cases:
        got = bool(DENIES.search(text))
        if got != want:
            bad += 1
            print("  FAIL want=%s got=%s %r" % (want, got, text[:60].replace("\n", "\\n")))
    print("self-test: %d case(s) passed, both directions of the denial pattern" % (len(cases) - bad)
          if not bad else "self-test: %d FAILURE(S)" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
