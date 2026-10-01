#!/usr/bin/env python3
"""check_name_reservations.py - a field name installed over another agent's reservation.

WHY THIS EXISTS, and it is a defect of mine. On 2026-09-15 OPUS named
`CharacterRenderRecord +0x0F8` resourceRefB. That row's evidence ends "Name is FABLE's" - FABLE
are working the record's semantics and 156 of its rows carry that phrase, 141 of them still
UNRESOLVED. OPUS read the meaning and the first part of the evidence, derived a correct name from
the four already-named members of the same idiom, and installed it without reading to the END of
the cell, which is where the reservation sits. The derivation was right and the act was wrong: a
reserved row is somebody else's to name, and the board's whole value is that a lane means
something.

Nothing would have caught it. The type store has gates for widths, for dangling references, for
census agreement and for the surfaces that quote its totals - and none for the one line that says
who may write a name.

WHAT IT FLAGS, and it is deliberately narrow. A row is a finding when its evidence RESERVES the
name to an agent AND carries a dated naming note crediting somebody ELSE:

    evidence contains   Name is FABLE's
    evidence contains   NAMED resourceRefB 2026-09-15 (OPUS)      <- different agent

WHAT IT DOES NOT FLAG, because the phrase carries two meanings and only one of them is a
reservation. All fourteen CharacterRenderRecord rows that are named while saying "Name is FABLE's"
are FABLE's OWN installs - relatedRecordIndex, rotationYaw, resolvedResourceA and eleven more -
where the sentence reads as ATTRIBUTION rather than as a claim on future work. A gate that read
those as violations would be red on fourteen correct rows from its first run, which is how a
checker teaches people to ignore it. So the trigger is the conflicting ATTRIBUTION, not the
reservation alone.

It also does not judge whether a name is good. That is the owner's call, which is the point.

usage: check_name_reservations.py [--db DB] [--self-test]
"""
import argparse
import io
import os
import re
import sys

DEFAULT_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "..", "..", "Database", "FFXII TZA")

RESERVE = re.compile(r"\bName is ([A-Z][A-Z0-9_-]{1,15})'s", re.I)
# The agent credited with installing the name: "NAMED BY FABLE ..." or "NAMED <what> <date>
# (OPUS)". TWO BUGS FIXED 2026-09-16, both found when the gate fired on a row that was already
# correct - CharacterRenderRecord +0x0F8, which OPUS named, withdrew on seeing the reservation,
# offered to FABLE, and FABLE then installed.
#
#   1. THE AGENT MUST END THE PARENTHESISED TOKEN. The old pattern took the first word inside any
#      parenthesis after NAMED, so "NAMED BY FABLE 2026-09-16 on OPUS's offer
#      (OPUS-REQ-FABLE-RESOURCEREFB-IS-YOURS-TO-INSTALL)" credited *OPUS* - it read a TASK ID as an
#      agent. An agent name is followed by `)`, `,` or `;`, never by a hyphen and more words.
#   2. THE LAST CREDIT WINS. The old pattern took the FIRST, which on that row was OPUS's original
#      install - superseded by a WITHDRAWN note and then by FABLE's install. A row's history is
#      append-only, so the earliest credit is the one least likely to be current.
#
# Both defects pointed the same way: they manufactured a violation on a row whose history is exactly
# what the protocol asks for - name, notice the reservation, withdraw, offer, owner installs.
CREDIT = re.compile(r"\bNAMED\s+BY\s+([A-Z][A-Z0-9_-]{1,15})\b"
                    r"|\bNAMED\b[^.]{0,120}?\(([A-Z][A-Z0-9_-]{1,15})\s*[),;]")


def findings(rows, I):
    out = []
    for r in rows:
        if len(r) <= I["evidence"]:
            continue
        name = r[I["name"]].strip()
        if not name or name == "UNRESOLVED":
            continue
        ev = r[I["evidence"]]
        res = RESERVE.search(ev)
        if not res:
            continue
        creds = [m for m in CREDIT.finditer(ev)]
        if creds:
            last = creds[-1]                      # the most recent act, not the first
            who = last.group(1) or last.group(2)
            if who.upper() != res.group(1).upper():
                out.append((r[I["type"]], r[I["offset"]], name, res.group(1), who))
    return out


def self_test():
    """Both ways: the violation must fire and the fourteen legitimate shapes must not."""
    I = {"type": 0, "offset": 1, "name": 2, "evidence": 3}
    cases = [
        (["T", "0x10", "someName", "width stuff. Name is FABLE's. census..."], 0,
         "reserved and named, no conflicting credit - FABLE's own install"),
        (["T", "0x10", "someName",
          "Name is FABLE's. NAMED someName 2026-09-15 (OPUS). derivation..."], 1,
         "reserved to FABLE, credited to OPUS - the violation"),
        (["T", "0x10", "someName",
          "Name is FABLE's. NAMED someName 2026-09-15 (FABLE)."], 0,
         "reserved and credited to the SAME agent"),
        (["T", "0x10", "someName",
          "Name is FABLE's. NAMED someName 2026-09-15 (OPUS). NAME WITHDRAWN 2026-09-15 (OPUS). "
          "NAMED BY FABLE 2026-09-16 on OPUS's offer (OPUS-REQ-FABLE-INSTALL-IT)."], 0,
         "withdrawn by OPUS then installed by the owner - the LAST credit wins"),
        (["T", "0x10", "someName",
          "Name is FABLE's. NAMED someName 2026-09-16 (OPUS-REQ-FABLE-SOMETHING)."], 0,
         "a task id in the parenthesis is not an agent"),
        (["T", "0x10", "UNRESOLVED",
          "Name is FABLE's. NAMED someName 2026-09-15 (OPUS)."], 0,
         "not named at all - nothing was installed"),
        (["T", "0x10", "someName", "no reservation here at all. NAMED x 2026-09-15 (OPUS)."], 0,
         "no reservation - naming is unrestricted"),
    ]
    ok = True
    for row, want, why in cases:
        got = len(findings([row], I))
        mark = "ok  " if got == want else "FAIL"
        if got != want:
            ok = False
        print("  %s %-52s fired %d, want %d" % (mark, why, got, want))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        print("check_name_reservations self-test")
        return 0 if self_test() else 1

    p = os.path.join(a.db, "_types", "fields.tsv")
    if not os.path.exists(p):
        print("no field store at %s" % p)
        return 2
    lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
    hdr = lines[0].split("\t")
    I = {k: hdr.index(k) for k in hdr}
    rows = [l.split("\t") for l in lines[1:] if l.strip()]

    reserved = sum(1 for r in rows if len(r) > I["evidence"] and RESERVE.search(r[I["evidence"]]))
    unres = sum(1 for r in rows if len(r) > I["evidence"] and RESERVE.search(r[I["evidence"]])
                and r[I["name"]].strip() == "UNRESOLVED")
    print("field rows: %d" % len(rows))
    print("  rows reserving the name to an agent : %d  (%d still UNRESOLVED)" % (reserved, unres))

    if not self_test_quiet():
        print("\n  CONTROL FAILED: the self-test does not pass, so the count below means nothing.")
        return 2

    bad = findings(rows, I)
    print("  named over ANOTHER agent's reservation : %d" % len(bad))
    if not bad:
        print("\nno field name is installed over another agent's reservation.")
        return 0
    print()
    for t, off, name, who, by in bad:
        print("  %s %s is named %r by %s, but the row reserves the name to %s"
              % (t, off, name, by, who))
    print("\nA reserved row is its owner's to name. Offer the derivation, do not install it.")
    return 1


def self_test_quiet():
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return self_test()


if __name__ == "__main__":
    sys.exit(main())
