"""apply.py [--apply] - stage FABLE's consumption of ASTRA's uq147-ko-release-partition (FABLE, 2026-10-03).

Request ASTRA-REQ-FABLE-UQ147-KO-RELEASE-PARTITION-1003. Evidence commit d02293770; SWE2-AUDIT-SPEC ACCEPT in
auditspec-review-astra-uq147-ko-release-partition-1003/REVIEW.md.

  E1  the-status-write-and-its-side-effects.md, section 2.7a: a qualifier paragraph after the paragraph that ends
      "the summoner's fall ends the summon." ("released" is two separately gated steps).
  E2  capability-inhibition-policy.md, the UQ-147 box: one sub-bullet appended after the box's last line (the
      2026-10-03 mode-query sub-bullet's OPEN list).

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
EV = "../../_experiments/evidence/uq147-ko-release-partition/README.md"
CA = "../../_index/candidates/"
SRC = ("(FABLE, 2026-10-03, on ASTRA's [`uq147-ko-release-partition`](" + EV + ") evidence accepted by "
       "SWE2-AUDIT-SPEC; [review](" + CA + "auditspec-review-astra-uq147-ko-release-partition-1003/REVIEW.md), "
       "[record](" + CA + "fable-uq147-ko-release-1003/README.md))")
COMMIT = "../../07-Combat-Action/CONTRACT-commit-action.md"
COMBO = "../../07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md"
STATUS_LINK = "../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md"

E1_ANCHOR = "party control recomputed** — the summoner's fall ends the summon."
E1_CLAUSE = "\n".join([
    "*Qualified: \"released\" is two separately gated steps " + SRC + ".* The release `00310780` that the non-Esper "
    "path calls first (`00300FC0`+0x4D) returns at once when the unit or its stats pointer `+0x698` is NULL "
    "(`00310780`+0x3, `00310780`+0x19). Otherwise:",
    "",
    "- **Contributor bookkeeping, only with flag bit 22 clear.** The release resolves the unit's target handle "
    "`+0x710` through `0031B7E0` (`00310780`+0x2F). Only when that target is non-NULL, bit 22 of the unit's flag word "
    "is clear (`00310780`+0x3E `bt`; `00310780`+0x43 `jb` skips when it is set) and the target's `+0xEA4` holds the "
    "unit's slot bit `1 << +0xEA9` (`00310780`+0x59 / +0x5B) does it decrement the target's `+0xEA8` "
    "(`00310780`+0x5D), clear that bit in `+0xEA4` (`00310780`+0x6A) and call two helpers (`00310780`+0x76, +0x7E). "
    "This reverses the attacker count that the commit makes only with the same bit clear "
    "([the commit contract](" + COMMIT + ") §6). Bit 22 is the engage-auto-attack flag "
    "([the combo page](" + COMBO + ") §2.5, test 3).",
    "- **The bit-22-set restore is a separate read.** Every admitted path then calls the engage-auto-attack restore "
    "(`00310780`+0x86). That routine reads bit 22 again and runs its body only when the bit is set, as the combo "
    "page's test 3 already gives. Its copy back of the suspended action covers `[+0x6B0, +0xBA0)`: the committed "
    "command `+0x714` is inside, the pending `+0xBA0` outside (the restore row of the commit contract's propagation "
    "table, OPUS's correction of 2026-10-01). On the bookkeeping path the two helper calls and the call into the "
    "restore lie between the two reads, so the partition is local order under normally returning helpers, not one "
    "atomic test.",
    "- **Four direct stores, none to `+0x714`.** The release itself writes the target's `+0xEA8` and `+0xEA4` above, "
    "clears bits 5 and 28 of the unit's flag word (`00310780`+0x8B) and sets `+0x694` to `0xFF` (`00310780`+0xA5). "
    "It has no direct store to `+0x714`, `+0xBA0` or the battle mode. That does not mean the command is kept: with "
    "bit 22 set, the restore can replace the committed `+0x714` with the saved command, and nothing requires the "
    "saved command to erase it. The `+0x714` compare at `00310780`+0xCD reads whatever the restore left. The helpers "
    "(the two bookkeeping calls, the restore's callees, and the calls at `00310780`+0x99, +0xAC, +0xB9 and +0xD6) "
    "are not read here and are not assumed to be free of effects.",
    "",
    "Static only; no game, emulator or native session. Still OPEN: natural KO and the bit-22 state a fallen unit is "
    "in, the helpers' transitive effects, the lifetime of the restored contents, and timing.",
])

E2_ANCHOR = "          `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON`."
E2_CLAUSE = "\n".join([
    "      - *What the earlier release leaves for the Dismiss and the recompute " + SRC + ".* Static only.",
    "        - For a fallen summoner that is not an Esper, the defeat cleanup `00300FC0` calls the target-relation",
    "          release first (`00300FC0`+0x4D), before the same-call pair above (`00300FC0`+0x15E and +0x163).",
    "          [The status-write page](" + STATUS_LINK + ")",
    "          §2.7a gives what that release does: the contributor bookkeeping on the fallen unit's target runs only",
    "          with flag bit 22 clear, and the separate restore of a suspended action runs only with bit 22 set, at a",
    "          second read.",
    "        - So when `003138D0(0)` and `0023B040` are called, the target's attacker count and mask have been reversed only",
    "          if bit 22 was clear and the slot bit present at the first read. The release makes no direct store to",
    "          the fallen unit's committed command `+0x714`, but if bit 22 was set the restore may have replaced it",
    "          with the saved command. Nothing here shows that command was kept, cleared or made Dismiss. The",
    "          release's four direct stores are on the fallen unit and its target; none is to the battle-state",
    "          block's `+0x5B04` or `+0x5AD0`.",
    "        - **Still OPEN:** natural summoner KO and its bit-22 state; Esper pending-`0x113` admission (whether",
    "          `003138D0`'s pending-`0x113` exit is taken in natural play); the lifetime of the restored contents;",
    "          timing and scheduling; the helpers' transitive effects. UQ-147 stays SUPERSEDED.",
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
