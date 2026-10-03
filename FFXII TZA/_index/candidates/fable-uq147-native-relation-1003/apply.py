"""apply.py [--apply] - stage FABLE's consumption of ASTRA's uq147-native-relation-invariant (FABLE, 2026-10-03).

Request ASTRA-REQ-FABLE-UQ147-NATIVE-RELATION-SEMANTICS-1003. Evidence commit 86cdcde10; SWE2-AUDIT-SPEC ACCEPT in
auditspec-review-astra-uq147-native-relation-invariant-1003/REVIEW.md (no narrowing beyond the README's own limits).

  E1  the-status-write-and-its-side-effects.md, section 2.7a: a qualifier after the closing "Static only; ... and
      timing." line of FABLE's 2026-10-03 release clause (what the first bookkeeping call's notification does in the
      native relation cache).
  E2  capability-inhibition-policy.md, the UQ-147 box: one sub-bullet appended after the box's last line (the
      2026-10-03 release sub-bullet's OPEN list).

Strike-free insertions only, each anchored on one unique full line. A page whose content differs from HEAD is refused
(an EOL-only difference is allowed); a page equal to HEAD plus this edit reports ALREADY (idempotent). Line endings
are kept. Dry run unless --apply. Prints FAILS N last."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

STATUS = "10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md"
POLICY = "15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md"

# Both pages sit two folders below the DB root, so the same relative prefixes serve both.
EV = "../../_experiments/evidence/uq147-native-relation-invariant/README.md"
CA = "../../_index/candidates/"
SRC = ("(FABLE, 2026-10-03, on ASTRA's [`uq147-native-relation-invariant`](" + EV + ") evidence accepted by "
       "SWE2-AUDIT-SPEC; [review](" + CA + "auditspec-review-astra-uq147-native-relation-invariant-1003/REVIEW.md), "
       "[record](" + CA + "fable-uq147-native-relation-1003/README.md))")
COMMIT = "../../07-Combat-Action/CONTRACT-commit-action.md"
EXP091 = "../../_experiments/EXP-091-commit-callees-exec.md"
ALLONES = "../../00-Engine-Core-Runtime/the-all-ones-empty-convention.md"
STATUS_LINK = "../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md"

E1_ANCHOR = ("Static only; no game, emulator or native session. Still OPEN: natural KO and the bit-22 state a fallen "
             "unit is in, the helpers' transitive effects, the lifetime of the restored contents, and timing.")
E1_CLAUSE = "\n".join([
    "*Qualified further: what the first bookkeeping call's notification does in the native relation cache " + SRC +
    ".* The first bookkeeping call (`00310780`+0x76) is the notify of [the commit contract](" + COMMIT + ") §13a, "
    "and the release passes it a zero third argument (`00310780`+0x67 `xor r8d,r8d`). §13a already gives what that "
    "argument does: the target's terminal-status mask cannot suppress collection, and every collected record carries "
    "flag `+1` = 1, with kind 1 for the acting unit itself or 2 for another member. That is canonical and is not "
    "proved again here. What is new is where the records go. [EXP-091](" + EXP091 + ") stopped them at a `ret` stub "
    "on the native relation-event handler, which the notify's dispatch reaches on the recipient's character render "
    "record at `+0x650` when that record is live. The handler keeps a fixed pool of 32 sixteen-byte relation rows "
    "with one-byte links ([the all-ones page](" + ALLONES + ") §9, \"What the pooled record is\").",
    "",
    "- **A closed local operation, not an opaque callback.** The handler (532 bytes) and its entry-reachable remover "
    "(162 bytes) transfer only to each other: one call and one tail jump into the remover. There is no indirect "
    "call, no import thunk and no heap free. The two bodies have 26 and 11 persistent write sites, all in the "
    "receiver's inline block, the pool rows, the pool's allocation cursor and two global count bytes. Removing a row "
    "clears its occupancy nibble; it does not free memory.",
    "- **What a flag-1 record does.** A kind-2 record that matches no row creates nothing, because creation needs "
    "flag 0 and a recipient different from the target. On a row matched by kind and actor, the handler first "
    "removes the row when its target equals the record's target. It then removes the row, by a tail jump, when the "
    "record's recipient equals the record's target. Otherwise it overwrites the row's target with the record's, "
    "and it does this even after the first removal, so an inactive row can still be changed. A kind-1 record acts "
    "only on the receiver's inline entry. With flag 1 it clears that entry's kind nibble when the entry's target "
    "equals the record's, and otherwise it writes nothing.",
    "- **At most one removal on a coherent row.** Take a receiver that is the recipient's own cache (the record's "
    "recipient equals the row's), a matched actor, and a row whose target still differs from its recipient, which "
    "creation enforces. Then the two removal tests cannot both pass, because together they need row target = "
    "record target = recipient. ASTRA's reducer covers all 203 equality partitions of the six identities with "
    "flags 0 and 1. Twenty cases are coherent, and none of them removes twice. SWE2-AUDIT-SPEC re-derived the count "
    "with its own enumeration. When neither test removes, the new target still differs from the recipient. The "
    "remover leaves the handler's receiver and record pointers and the record's values unchanged. That is read from "
    "its code under the evidence's disjoint-object premise; it is not assumed from the ABI.",
    "- **The malformed counterexample and the limits are kept.** A row whose six identities are all equal, with "
    "flag 1, reaches both removals. The remover does not test occupancy. It clears the nibble and then decrements "
    "the owner's count byte `+0xE` and a global count byte without a test, so a second removal turns a zero count "
    "into `0xFF`. It never clears the removed row's three identity words or its links, so stale bytes stay in "
    "inactive rows. This is a conditional fact about malformed state. It is not a claim that natural play "
    "produces that state.",
    "- **What it does not close.** \"No import or heap free\" covers these two bodies only. It does not cover the "
    "second bookkeeping call (`00310780`+0x7E), the restore (`00310780`+0x86), the later calls (`00310780`+0x99, "
    "+0xAC, +0xB9 and +0xD6) or the caller flow. It proves nothing about the cache's initialisation, binding, reuse, "
    "scheduling or presentation.",
    "",
    "Static only (Method A); no game, emulator or native session. Still OPEN: natural KO and whether it reaches this "
    "leg, the cache's actual binding and initialisation, outside writers to the count bytes, termination on a "
    "corrupted list, scheduling and presentation.",
])

E2_ANCHOR = "          timing and scheduling; the helpers' transitive effects. UQ-147 stays SUPERSEDED."
E2_CLAUSE = "\n".join([
    "      - *What the release's notification does in the native relation cache " + SRC + ".* Static only.",
    "        - [The status-write page](" + STATUS_LINK + ")",
    "          §2.7a now gives it. On the release's contributor-bookkeeping path above (bit 22 clear), the notify",
    "          ends relation rows in a fixed native pool through a local remover. It is not an opaque callback. On a",
    "          coherent row it removes at most once. A malformed row can be removed twice, and the remover's count",
    "          bytes then underflow. That is a conditional fact about malformed state, not a natural bug.",
    "        - For UQ-147 this removes one opaque effect from the fallen summoner's release and nothing else. It does",
    "          not show that natural summoner KO reaches that leg. It says nothing about the other helpers, the",
    "          caller flow, or the cache's initialisation, reuse, scheduling or presentation.",
    "        - **Still OPEN:** natural summoner KO and its live admission; Esper pending-`0x113` admission; the",
    "          cache's binding and lifetime; timing and scheduling; presentation. UQ-147 as a whole stays open: the",
    "          row stays SUPERSEDED, and its live half `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON` is OPEN.",
])

EDITS = [
    ("E1", STATUS, E1_ANCHOR, "\n\n" + E1_CLAUSE),
    ("E2", POLICY, E2_ANCHOR, "\n" + E2_CLAUSE),
]


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=DB, capture_output=True).stdout


def head_text(rel):
    top = git("rev-parse", "--show-toplevel").decode().strip()
    full = os.path.relpath(os.path.join(DB, *rel.split("/")), top).replace("\\", "/")
    return git("show", "HEAD:" + full).decode("utf-8").replace("\r\n", "\n")


def patch(t, anchor, ins):
    """(status, new_text) for LF-normalised text t; the anchor must be one unique full line."""
    if ins.strip("\n") in t:
        return "ALREADY", t
    lines = t.split("\n")
    idx = [i for i, l in enumerate(lines) if l == anchor]
    if len(idx) != 1:
        return "MISS anchor (%d full-line matches)" % len(idx), None
    i = idx[0]
    new = "\n".join(lines[:i + 1]) + ins + "\n" + "\n".join(lines[i + 1:])
    return "OK", new


def main():
    write = "--apply" in sys.argv
    fails = 0
    for name, rel, anchor, ins in EDITS:
        p = os.path.join(DB, *rel.split("/"))
        raw = io.open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        t = raw.replace("\r\n", "\n")
        h = head_text(rel)
        hst, hnew = patch(h, anchor, ins)
        if hst == "ALREADY":
            print("%s %s: REFUSED - HEAD already carries the clause; nothing to stage" % (name, rel))
            fails += 1
            continue
        if hnew is None:
            print("%s %s: %s at HEAD" % (name, rel, hst))
            fails += 1
            continue
        if t == hnew:
            print("%s %s: ALREADY (page = HEAD + this clause)" % (name, rel))
            continue
        if t != h:
            print("%s %s: REFUSED - content differs from HEAD (not an EOL-only difference)" % (name, rel))
            fails += 1
            continue
        st, new = patch(t, anchor, ins)
        if new is None:
            print("%s %s: %s" % (name, rel, st))
            fails += 1
            continue
        added = new.count("\n") - t.count("\n")
        verb = "PATCHED" if write else "WOULD PATCH"
        if write:
            io.open(p, "w", encoding="utf-8", newline="").write(new.replace("\n", nl))
        print("%s %s: %s (+%d lines after %r; %s kept)" % (name, rel, verb, added, anchor[:60],
                                                           "CRLF" if nl == "\r\n" else "LF"))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
