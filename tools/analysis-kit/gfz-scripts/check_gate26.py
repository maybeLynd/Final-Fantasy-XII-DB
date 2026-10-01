#!/usr/bin/env python3
"""Score every contract against RECONSTRUCTION-CHARTER section 26's own checklist.

Why this exists. Section 26 says "do not call a subsystem reconstruction-ready merely
because a lot is known", then lists the questions that decide it. The team keeps asking
whether the shared gate is close, and the honest answer has been an impression. This
turns it into a measurement of the thing section 26 actually asks about.

THREE THINGS THIS DELIBERATELY DOES NOT DO, each of which it got wrong first.

1. It does not score subsystems. It reads contracts. A subsystem may have none, one or
   several, so a high score means the contracts that exist answer section 26 -- never
   that the subsystem is covered. Section 27 is about the database as a whole and is not
   scored here at all.

2. It does not conflate "the section says no" with "there is no such section". An absent
   section is UNMEASURED, not negative. The first version collapsed the two and made
   CONTRACT-hp-write-and-lethal-transition look like the weakest contract in the
   database, when in fact it answers every question under its own headings -- "The
   clamp", "Ordering, which is most of the contract". Contracts are allowed to be
   written well rather than written to a template, and an instrument that punishes that
   is measuring conformity.

3. It does not reduce runtime validation to a boolean. Section 26 asks whether major
   assumptions have been RUNTIME VALIDATED; answering with yes/no erases the
   static / isolated-original-code / live / integrated distinction the charter's
   evidence rules exist to preserve. Section 13 is classified, not scored.

CONTROL, checked on every run: most contracts must come back with nothing executed. The
database's live evidence is a handful of experiments, so a scorer reporting a majority
validated is reading intent. It earned its keep on the first run, when twelve contracts
opening "**Empty.**" were counted as validated because the denial list lacked the word.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "FFXII TZA"

# section 26's questions -> the contract sections that may answer each
CRITERIA = [
    ("responsibilities / owner", ["Purpose", "Interface"]),
    ("key types / what it owns", ["Types"]),
    ("inputs / outputs / callers / callees", ["Interface"]),
    ("initialization & lifetime / destruction",
     ["State transitions", "Relationships"]),
    # Section 26 asks for "update ordering ... state transitions" in one breath, so a
    # contract answering under "Ordering" or "Resume semantics" has answered the
    # charter's question. Accepting those is matching the charter's own wording -- the
    # alternative was renaming four contracts to satisfy this scorer, which is
    # optimizing for the instrument and exactly what section 28 forbids.
    ("update ordering / state transitions",
     ["State transitions", "Ordering", "Resume semantics"]),
    ("important globals / state read & written", ["State"]),
    ("script & resource dependencies", ["Script · resource · event interactions"]),
    ("RNG / determinism", ["Determinism"]),
    ("edge states / what can fail", ["Failure paths and edge conditions"]),
    ("invariants & preconditions", ["Preconditions · postconditions · invariants"]),
    ("observable behaviour", ["Observable behaviour"]),
    ("major assumptions RUNTIME VALIDATED", ["Runtime validation"]),
    ("meaningful parity tests constructible", ["Parity plan"]),
]

RUNTIME_SECTION = "Runtime validation"

OPEN_RE = re.compile(
    r"^\s*(\*\*)?(none|empty|not established|unknown|unresolved|n/?a|tbd)\b", re.I)

LIVE_RE = re.compile(r"observed live|how it was observed live|controlled experiment|"
                     r"live pre-kill observation|bounded captures exist", re.I)
ISOLATED_RE = re.compile(r"isolated original-code|EXP-\d+", re.I)
# The contract denying the live tier in its own words. Checked BEFORE LIVE_RE - see runtime_class.
LIVE_DENIED_RE = re.compile(r"live capture:?\s*(still\s+)?absent|no live capture|"
                            r"not been observed in the running game", re.I)

ANSWERED, DENIED, ABSENT = "answered", "denied", "absent"


# A heading may carry a subtitle after a dash: "7. State transitions — the fork, with
# its compiler trick". Exact-title matching called five of those ABSENT, which is the
# instrument punishing a contract for saying more rather than less. Split only on real
# dashes -- never on the middle dot, which separates words inside two canonical titles.
SUBTITLE_RE = re.compile(r"\s*[—–]\s*|\s+-\s+")


def canon(title):
    return SUBTITLE_RE.split(title, 1)[0].strip()


def sections(text):
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(?:\d+[a-z]?\.\s*)?(.+?)\s*$", line)
        if m:
            if cur:
                out.setdefault(cur, "\n".join(buf).strip())
            cur, buf = canon(m.group(1)), []
        elif cur:
            buf.append(line)
    if cur:
        out.setdefault(cur, "\n".join(buf).strip())
    return out


def state_of(secs, wanted):
    """answered / denied / absent -- absent means this instrument cannot see it."""
    present = [w for w in wanted if w in secs]
    if not present:
        return ABSENT
    for w in present:
        body = secs[w].lstrip()
        if body and not OPEN_RE.match(body) and len(re.sub(r"\s", "", body)) > 24:
            return ANSWERED
    return DENIED


def runtime_class(body):
    """NONE / ISOLATED / LIVE -- what section 13 reports, not what it hopes."""
    if not body:
        return "NONE"
    head = body.lstrip()[:400]
    # A denial wins over anything after it: "Empty. What would fill it: EXP-..." is a
    # description of an experiment that has not happened.
    if OPEN_RE.match(head):
        return "NONE"
    # AND THE SAME PRINCIPLE HAS TO COVER A DENIAL OF THE *LIVE* TIER SPECIFICALLY, which it did
    # not until 2026-09-14. `CONTRACT-script-to-native-bridge` opens "Evidence class: isolated
    # original-code. Live capture: still absent" and was nonetheless classified LIVE - because
    # further down its section 13 carries a TABLE whose COLUMN HEADER reads
    # "| claim | how it was observed live | date | result |", and LIVE_RE matched the header.
    #
    # A column header is not an observation. This is the third time in one day that a table header
    # was read as content in this kit (the others were ASTRA's probes under a "Who produces it"
    # column, and a preserved table annotated by the block after it), so it is a shape worth naming
    # rather than a one-off.
    #
    # THE FIX IS THE PRINCIPLE ALREADY STATED ABOVE, not a narrower LIVE_RE: a contract that says
    # its live capture is absent is not claiming live evidence, whatever a table further down is
    # headed. Exactly one contract is affected and the live count goes 5 -> 4 - which is then the
    # same number `check_experiment_schema` reaches from the experiment records, by a different
    # route. The MEMBERSHIPS still differ by one either way, so that agreement is on the count and
    # not yet on the set; see the note published with this change.
    if LIVE_DENIED_RE.search(head):
        return "ISOLATED" if ISOLATED_RE.search(head) else "NONE"
    if LIVE_RE.search(head):
        return "LIVE"
    if ISOLATED_RE.search(head):
        return "ISOLATED"
    return "NONE"


def main():
    contracts = sorted(ROOT.glob("*/CONTRACT-*.md")) + \
        sorted(ROOT.glob("*/*/CONTRACT-*.md"))
    if not contracts:
        print("no contracts found under", ROOT)
        return 2
    n = len(contracts)

    tally = {name: {ANSWERED: 0, DENIED: 0, ABSENT: 0} for name, _ in CRITERIA}
    rt_class, bespoke = {}, []
    for p in contracts:
        secs = sections(p.read_text(encoding="utf-8", errors="replace"))
        rt_class[p] = runtime_class(secs.get(RUNTIME_SECTION, ""))
        absent = 0
        for name, wanted in CRITERIA:
            if name == "major assumptions RUNTIME VALIDATED":
                st = ANSWERED if rt_class[p] == "LIVE" else DENIED
            else:
                st = state_of(secs, wanted)
            tally[name][st] += 1
            absent += (st == ABSENT)
        if absent >= 3:
            bespoke.append((absent, p))

    print("CONTRACTS SCORED AGAINST CHARTER SECTION 26: %d\n" % n)
    print("  %-42s %8s %7s %8s" % ("section 26 asks", "answered", "denied", "no such"))
    print("  %-42s %8s %7s %8s" % ("", "", "", "section"))
    for name, _ in CRITERIA:
        t = tally[name]
        print("  %-42s %8d %7d %8d" % (name, t[ANSWERED], t[DENIED], t[ABSENT]))

    print("\n\"no such section\" is NOT a finding about the subsystem -- it is this")
    print("instrument saying it cannot see the answer. Contracts written to their own")
    print("headings rather than the template land here and are not weak:")
    for absent, p in sorted(bespoke, reverse=True)[:6]:
        print("   %d unseen  %s" % (absent, p.relative_to(ROOT)))

    live = sorted(p for p, c in rt_class.items() if c == "LIVE")
    isolated = sorted(p for p, c in rt_class.items() if c == "ISOLATED")
    print("\nSECTION 13 BY EVIDENCE CLASS, which is what section 26 asks about:")
    print("  live or controlled experiment : %d" % len(live))
    for p in live:
        print("      %s" % p.relative_to(ROOT))
    print("  isolated original-code only   : %d" % len(isolated))
    for p in isolated:
        print("      %s" % p.relative_to(ROOT))
    # Names, not just a count: a count cannot tell INTAKE LAG (a contract that
    # arrived without evidence yet) from REGRESSION (one that lost it). Both
    # read as a nonzero figure here; the diagnosis is in the membership.
    unexecuted = sorted(p for p, c in rt_class.items()
                        if c not in ("LIVE", "ISOLATED"))
    print("  nothing executed              : %d" % len(unexecuted))
    for p in unexecuted:
        print("      %s" % p.relative_to(ROOT))

    runtime = tally["major assumptions RUNTIME VALIDATED"][ANSWERED]
    parity = tally["meaningful parity tests constructible"][ANSWERED]
    print("\nSECTION 26: \"If major answers are unknown, it is not reconstruction-ready.\"")
    print("  runtime-validated  : %d of %d contracts" % (runtime, n))
    print("  parity plan present: %d of %d contracts" % (parity, n))
    print("\nA parity PLAN is not a parity TEST. Section 26 asks whether meaningful parity")
    print("tests can be CONSTRUCTED; a plan says how, and only a run says whether.")

    # CONTROL -------------------------------------------------------------
    print("\nCONTROL: most contracts must come back with nothing executed. The database's")
    print("live evidence is a handful of experiments, so a majority scored validated means")
    print("the scorer is reading intent. Expected <= 33% live.")
    if runtime > 0.33 * n:
        print("  CONTROL FAILED: %d of %d scored live." % (runtime, n))
        print("  Fix the classifier before trusting any number above.")
        return 2
    print("  control passed: %d of %d live, within expectation." % (runtime, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
