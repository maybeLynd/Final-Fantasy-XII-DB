"""apply.py [--apply] - stage FABLE's UQ-147 consumption clauses (FABLE, 2026-10-03).

Consumes three pieces of ASTRA evidence accepted by SWE2-AUDIT-SPEC (review commit bff21d191):
  E1  uq147-dismiss-stage (3a25a0be0)    -> battle-runtime-mode-ladder.md, a qualifier paragraph after the section 2c
                                            paragraph that ends "modes' exits."
  E2  uq147-local-boundaries (6d74079f1) -> capability-inhibition-policy.md, two sub-bullets appended inside the UQ-147
      uq147-mode-query (ecbfeb641)          box, after its last sub-bullet (the 2026-10-01 pointer)

Strike-free insertions only, each anchored on one unique full line. A page whose content differs from HEAD is refused
(an EOL-only difference is allowed); a page equal to HEAD plus this edit reports ALREADY (idempotent). Line endings
are kept. Dry run unless --apply. Prints FAILS N last."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))

LADDER = "00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md"
POLICY = "15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md"

EV = "../../_experiments/evidence/"
CA = "../../_index/candidates/"
REC = "[record](" + CA + "fable-uq147-consumption-1003/README.md)"

E1_ANCHOR = "modes' exits."
E1_CLAUSE = (
    "*Qualified: \"when the sequence ends\" is local order on the Dismiss arm (FABLE, 2026-10-03, on ASTRA's "
    "[`uq147-dismiss-stage`](" + EV + "uq147-dismiss-stage/README.md) evidence accepted by SWE2-AUDIT-SPEC; "
    "[review](" + CA + "auditspec-review-astra-uq147-dismiss-stage-1003/REVIEW.md), " + REC + ").* "
    "`00306760` dispatches on the kind word `022C215C` (`003067AA`, through the jump table just past the routine's code), and kind 2, Dismiss (§2d), "
    "selects `00306A3D`. On that arm, if bit 0 of `+0x5B04` is set (`00306A7A` `test al,1` / `00306A7C` `je`), the "
    "routine clears it with a direct store at `00306A81` and calls `0035C620`; if the bit is already clear, the store "
    "is skipped and the same suffix runs from `00306A95`. The suffix clears bits 8-9 of the first dword of each battle "
    "unit (`00306AC0`, stride `0xF50`), calls `00332130(3)` and then writes state 5 to `022C2160` at `00306ADF`, the "
    "routine's only reference to that word. So the clear comes before this routine's own state-5 write, and no "
    "state-6/7 test guards it: it is not one of §2d's finishing arms. Kind 1 (`00306931`) is the set-arm, at "
    "`00306949`. This is local order under normally returning helpers. It is not visible timing, not a lasting clear "
    "and not a first-ever state 5: what the helpers on the path do (`003098D0` and `003299B0` in the prologue, "
    "`0035DAE0`, `00306D90`, `0035C620`, `00236850` / `00236820`, `00332130`) is not read, and state 5 here is an "
    "internal write, not a screenshot. That the kind read at `003067AA` belongs to the row and owner the classifier "
    "saw is a premise. [The availability page](../../07-Combat-Action/Action-Availability/"
    "battle-command-availability-and-reason-codes.md)'s FABLE subsection of 2026-10-02 gives the classifier's "
    "quotient-to-kind map and keeps natural kind-to-row, caller and owner consistency OPEN. Still OPEN: when the "
    "player sees the Esper leave, whether the clear lasts, the opaque helpers' effects, natural summoner KO, and "
    "whether the acting member coexists with a Dismiss in progress."
)

E2_ANCHOR = "        `BattleUnit_GetPartyLeader` returns while its `+0x698` is null."
E2_CLAUSE = "\n".join([
    "      - *Local boundaries of the summon cleanup (FABLE, 2026-10-03, on ASTRA's "
    "[`uq147-local-boundaries`](" + EV + "uq147-local-boundaries/README.md) evidence accepted by SWE2-AUDIT-SPEC, "
    "with its narrowing; [review](" + CA + "auditspec-review-astra-uq147-local-boundaries-1003/REVIEW.md), "
    + REC + ").* Static only; no game, emulator or native session.",
    "        - **Same call.** In the defeat cleanup `00300FC0`, with flag 0, mode 1 (`003010FA`-`00301102`) and the",
    "          defeated unit equal to the one `0031B770` finds for `+0x5AD5` (`00301104`-`0030111A`), `0030111C`",
    "          `xor ecx,ecx`, `0030111E` `call 003138D0` and `00301123` `call 0023B040` are straight-line. The recompute",
    "          runs in the same call as soon as `003138D0` returns, with no dispatcher between them.",
    "        - **An invocation is not a completed cleanup.** `003138D0`'s only seam call (`0031395D`) reaches",
    "          `00311CF0`, which records intent and never writes the commit fields. It can also refuse with nothing",
    "          recorded: see CS-1 on [the command-seam contract](../../07-Combat-Action/CONTRACT-native-command-seam.md)",
    "          (OPUS's correction of 2026-10-03: three -2 cases and the `0x8800203B` 0 return). The mode-bit clear is on",
    "          the Dismiss arm of `00306760` ([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/"
    "battle-runtime-mode-ladder.md)",
    "          §2c, `00306A81`). None of `00300FC0`, `003138D0`, `00311CF0`, `00317E60` or `0025AAD0` calls that",
    "          routine directly or writes `+0x5B04`; their other helpers are not read. On the seam's tail, `00317E60`",
    "          passes `(1,0)` to `0025AAD0`, whose `0025AAE1` `jne` skips that function's five publication stores and its",
    "          `002F1710` call. That excludes those only. Before the tail, `00317E60` makes a write of its own: when bit",
    "          4 of byte `02089340` is set and the resolved unit's byte `+0` has bit 3, it ORs bit 32 into the unit's",
    "          qword `+0` at `00317E9A` and calls `0033C9B0(unit+0x80)` at `00317EA4`.",
    "        - **The roster selector has no KO filter and no cleanup.** The mode-1 leg passes 3 to `0031B8C0`",
    "          (`003138E6`). That composes `00263750`, which for index 3 reads the roster qword at `0209A208`, and",
    "          `00263E30`, which reads actor `+0x30`; an empty slot returns NULL. It reads no HP or status, writes",
    "          nothing and calls nothing else. Index 3 is a roster slot, not ActorStorage class 3.",
    "      - *The mode query and a conditional early return (FABLE, 2026-10-03, on ASTRA's "
    "[`uq147-mode-query`](" + EV + "uq147-mode-query/README.md) evidence accepted by SWE2-AUDIT-SPEC; "
    "[review](" + CA + "auditspec-review-astra-uq147-mode-query-1003/REVIEW.md)).*",
    "        - **Two reads, not atomic.** `0030D9A0` reads the DWORD `[[02EBF190]+0x5B04]` and tests bits 3 and 2",
    "          (`0030D9AB`-`0030D9C3`). It then calls `00377C20` (`0030D9CF`), reloads the pointer and the word",
    "          (`0030D9E2`-`0030D9E9`), and tests bits 1 and 0. \"Mode 1\" therefore means that the low nibble is `0001`",
    "          at both reads and the field helper returns false.",
    "        - **The field helper is closed and read-only.** `00377C20` -> `003148F0` -> `002EF2B0` -> `002EF640` is 133",
    "          bytes with no memory write and no other call; [the field-record page](../../03-World-Area-Field/"
    "Field-Record-Table/field-record-bit15-action-permission.md)",
    "          §2 gives its descriptor test and bit 15. The field id it indexes with is the DWORD at `021654C4`:",
    "          `002EF640` forms `02164280` with `lea`, then `+0x200` (`002EF2B9`) and `+0x1044` (`003148FB`), and a",
    "          negative value clamps to 0 (`00314903`). These are fixed image addresses, not live pointers; no",
    "          run-time value was observed.",
    "        - **The early-return counterexample.** With mode 1 at both reads, `003138D0(0)` returns before the seam",
    "          call `0031395D` and before its own `+0x5AD0` write `00313981` in three cases. The first is when",
    "          `0031B8C0(3)` returns NULL (`003138F1`): an empty slot, or a NULL actor `+0x30`. The other two are the",
    "          pending and committed `0x113` exits that [the periodic-tick page](../../10-Status-Periodic-Terminal/"
    "Periodic-Tick/what-the-periodic-tick-does.md)",
    "          already gives (`00313913`, `0031391C`). On those paths the only store is the home slot `[rsp+0x48]`",
    "          (`003138F9`). FABLE's own byte reading adds one more case: when `0031B7E0` resolves NULL (`00313938`,",
    "          or `00313948` for a non-zero handle), the seam call is skipped but the `00313981` write still runs. So",
    "          an invocation alone does not guarantee a state change. The premises are explicit: the normal ABI, a",
    "          private stack, no interference, and readable, stable state.",
    "        - **Combined with the same call above.** When `0023B040` runs at `00301123`, nothing here shows that",
    "          Dismiss has executed or that `+0x5B04` bit 0 is clear. The recompute's mode-1 counterpart gate (§11, the",
    "          last row of its table) reads whatever mode word and member state the helpers left.",
    "        - **Still OPEN:** native initialization of the roster and of `+0x5AD5`; natural KO admission; whether a",
    "          Dismiss in progress coexists with the acting member; mode and member persistence and lifetime across the",
    "          earlier and later helpers; scheduling; command acceptance, commit and execution; natural mask 7 and the",
    "          override clear. UQ-147 stays SUPERSEDED; its live half is",
    "          `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON`.",
])

EDITS = [
    ("E1", LADDER, E1_ANCHOR, "\n\n" + E1_CLAUSE),
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
        if write:
            io.open(p, "w", encoding="utf-8", newline="").write(new.replace("\n", nl))
            print("%s %s: PATCHED (+%d lines after %r; %s kept)" % (name, rel, added, anchor[:60],
                                                                     "CRLF" if nl == "\r\n" else "LF"))
        else:
            print("%s %s: WOULD PATCH (+%d lines after %r; %s kept)" % (name, rel, added, anchor[:60],
                                                                         "CRLF" if nl == "\r\n" else "LF"))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
