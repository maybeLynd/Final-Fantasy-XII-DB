"""apply_render_slot.py [--apply] - consume three accepted ASTRA static packets on the character render-record slot
lifecycle into the 17-Presentation-Rendering pages (OPUS, 2026-10-02).

Board requests: ASTRA-REQ-OPUS-RENDER-SLOT-IDENTITY-PUBLICATION-1002 (packet render-slot-identity-publication, aac0489ac),
ASTRA-REQ-OPUS-RENDER-CLEAR-CALLEE-FOOTPRINTS-1002 (render-clear-callee-footprints, 621dbd2cc) and
ASTRA-REQ-OPUS-RENDER-REMOVAL-PHASE-CONTRACTS-1002 (render-removal-phase-contracts, 31f29775a). Accepted by
SWE2-AUDIT-SPEC (three ACCEPT reviews under _index/candidates/auditspec-review-astra-render-*-1002/) and by FABLE
(ACCEPT-WITH-NARROWING, f1a265c5b and b3fb2d6cf). FABLE's narrowings bind and are carried here: the pending-list writes
precede the self-index store, so the id is not the first publication; "clears 160 rows" is memset plus defaults; the
16-byte scalars are four 4-byte movss per call; the mark arm writes three helper-returned objects; retirement sets pool
flag 0x20 after 004200A0 returns; both removers share one count and one cursor.
Every consumed fact was re-read at the shipping image (retool.py dis 0041F730 / 004269A0 / 004279B0 / 00420480 /
00429140 / 00427C90 / 004200A0, 2026-10-02); the deciding instructions are listed in consumption-notes.md.

Edits prefer qualifying additions: *(qualified 2026-10-02, OPUS: ...)* after the statement. One statement is refuted and
is struck and restated (section 15's "every path but the null converges on 00429296": the mark arm's full path
returns at 00429140+0xC3). Every ~~ span opens and closes on one line. Code-block lines get a trailing
`<- qualified` comment (their OLD includes the line end, so NEW never contains OLD). Prose appends also end OLD at the
line end or the table cell end, so NEW never contains OLD and a re-run reports ALREADY. No front-matter edits, no
heading changes, no census TSV edits, no _types edits (the type changes are a request to SWE2-STRUCT).
New text names by address only Presentation-layer bodies (0041F730, 00420480, 004269A0, 004279B0, 00429140,
00427C90, 004200A0); the clear's helpers, the memset import and the root resolver are named by role. Interior sites
are cited as entry+offset. Premises and open items stay as the packets and reviews keep them: no native execution,
lifetime, all-writer coherence, reentrancy or scheduling claim, and no natural fault or hang.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "17-Presentation-Rendering/"
POOL = F + "CONTRACT-render-record-pool-lifecycle.md"
ARR = F + "Character-Render-Records/the-character-render-record-array.md"

SLOT = "render-slot-identity-publication"
CLEAR = "render-clear-callee-footprints"
REM = "render-removal-phase-contracts"

EDITS = [
    # ---------------- CONTRACT-render-record-pool-lifecycle.md ----------------
    # R1 return ABI versus completion (00429140: +0x1C eax 0; +0xC3 and +0x165 eax 1).
    (POOL, "**1 on every other input** |",
     "**1 on every other input**, which is not a free-slot certificate: a 1 can mean a deferred mark, a no-op or a "
     "direct unlink and clear *(qualified 2026-10-02, OPUS: " + REM + ", accepted)* |"),
    # S1 invariant 2: count gate bounds the count only; no positive-count guard before either DEC.
    (POOL, "   the pool holds exactly 160 records and the 161st allocation is refused.\n",
     "   the pool holds exactly 160 records and the 161st allocation is refused *(qualified 2026-10-02, OPUS: the "
     "signed gate bounds the count and nothing else - the starting cursor is read signed at `004279B0`+0x4A with no "
     "range check before the clear it addresses, and neither remover tests the count before its decrement, so the "
     "lower bound is not enforced: a count of 0 would become -1, an arithmetic case and not an observed one; " + SLOT +
     " and " + REM + ", accepted)*.\n"),
    # S2 invariant 5: "free" is the scan predicate; count < 160 does not imply a zero flag exists.
    (POOL, "   (`00427AD2`) and the record initializer sets it non-zero (`0042049A`).\n",
     "   (`00427AD2`) and the record initializer sets it non-zero (`0042049A`) *(qualified 2026-10-02, OPUS: "
     "\"free\" is the scan's predicate, not an ownership certificate - a count below 160 does not by itself imply "
     "that any row has a zero `+0x284`, and nothing checks the count against the 160 flags; " + SLOT +
     ", accepted)*.\n"),
    # S3 + C1 termination argument: conditional scan; composed clear postcondition under premises.
    (POOL, "at `0041F754`, the whole record.\n",
     "at `0041F754`, the whole record *(qualified 2026-10-02, OPUS: both legs are conditional. The cap yields a zero "
     "`+0x284` only while the count agrees with the flags - the accepted countermodel, count 0 with every flag "
     "non-zero, passes the cap and the scan then never meets a zero, a mathematical case and not an observed hang - "
     "and the scan stops within 160 visits only under stable readable flags with at least one zero. Nor is the memset "
     "the clear's last write: 125 direct writes and six calls into four helpers follow it, their composed footprints stay "
     "inside the record and miss `+0x0` and `+0x284`, and so the clear returns with id -1 and `+0x284` 0 under its "
     "premises - a valid writable record, a private frame, readable constant inputs, normal returns, a fill confined "
     "to its span, ABI preservation and no interference; " + SLOT + " and " + CLEAR + ", accepted)*.\n"),
    # R2 retire reaches the clear as 004200A0's tail; the release arm skips 004200A0.
    (POOL, "which calls `0041F730` in turn.\n",
     "which calls `0041F730` in turn *(qualified 2026-10-02, OPUS: as a tail jump at `004200A0`+0x146, after "
     "`004200A0`'s fifteen calls; `00429140`'s direct arm makes no `004200A0` call, so that cleanup does not run on "
     "it - " + REM + ", accepted)*.\n"),
    # S4 construct: memset plus defaults, not all-zero (FABLE narrowing).
    (POOL, "is not evidence that they are one field** — they are read separately at 4 bytes everywhere else.\n",
     "is not evidence that they are one field** — they are read separately at 4 bytes everywhere else *(qualified "
     "2026-10-02, OPUS: each per-record clear is a memset followed by the clear's own sentinel and default stores, so "
     "a constructed row is not all-zero - `+0x0` ends at -1, and no direct store or helper footprint after the "
     "memset touches `+0x284`; " + SLOT + " with FABLE's narrowing and " + CLEAR + ", accepted)*.\n"),
    # S5 allocate step 3: signed cursor, no domain check before the clear.
    (POOL, "`call 0041F730(record)` clears it.\n",
     "`call 0041F730(record)` clears it *(qualified 2026-10-02, OPUS: the cursor is read signed at `004279B0`+0x4A "
     "and nothing compares it before this clear, so the step is in range only under the precondition "
     "0 <= nextFreeIndex <= 159, which the count gate in step 2 does not supply; " + SLOT + ", accepted)*.\n"),
    # S6 allocate step 4: list writes, then id, then +0x284 OR, then count; not atomic (FABLE narrowing).
    (POOL, "   tail. Then `tailPending = index` and `record.id = index`.\n",
     "   tail. Then `tailPending = index` and `record.id = index` *(qualified 2026-10-02, OPUS: in that order - the "
     "list writes precede the self-index WORD store at `004279B0`+0x9D, so the id is not the slot's first "
     "publication; the id store does precede `00420480`'s first OR of `0x2010F9` into `+0x284` (`00420480`+0x1A, "
     "step 5) and the count increment (step 6). These are separate stores, not one atomic publication; " + SLOT +
     " with FABLE's narrowing, accepted)*.\n"),
    # S7 allocate step 7: conditional circular scan.
    (POOL, "until the record it names has `+0x284 == 0`.\n",
     "until the record it names has `+0x284 == 0` *(qualified 2026-10-02, OPUS: from a start in 0..159 every "
     "visited index stays in 0..159 and one full cycle is 160 visits; the loop stops within 160 only if the flags "
     "are stable and readable and at least one is zero, which the count does not prove; " + SLOT +
     ", accepted)*.\n"),
    # R3 retire step 2: DEC before every call, no positive-count guard, no id test.
    (POOL, "— **before** the two end fixups, not after them.\n",
     "— **before** the two end fixups, not after them *(qualified 2026-10-02, OPUS: and before every call of steps "
     "5-7, with no positive-count test and no read of the id at `+0x0` before it - the only selection test is "
     "`+0x290` mask 02 at `00427C90`+0x3D, and the signed next link is cached at +0x44 before the branch. A count "
     "of 0 would decrement to -1 and skip step 4's reset, arithmetic only; " + REM + ", accepted)*.\n"),
    # R4 release intro: 1 is "not null", not completion.
    (POOL, "— and `1` as well when neither applies.\n",
     "— and `1` as well when neither applies *(qualified 2026-10-02, OPUS: so a 1 reports \"not null\", not "
     "completion - it covers path one's deferred mark, the no-op when neither applies (`00429140`+0xC4 jumping to "
     "+0x156, no call and no non-stack write) and path two's direct unlink and clear, and only path two leaves the "
     "row cleared on return; " + REM + ", accepted)*.\n"),
    # R5 release path two: DEC order, no 004200A0, conditional clear postcondition.
    (POOL, "the full reset, which is what returns the record to the free cursor.\n",
     "the full reset, which is what returns the record to the free cursor *(qualified 2026-10-02, OPUS: the count "
     "drops at `00429140`+0x10D, after the neighbour links and before the end fixups, the new-count-0 cursor reset "
     "(+0x148) and the clear (+0x151), with no positive-count test; this arm makes no `004200A0` call, so none of "
     "retirement's step-7 cleanup runs. \"Returns to the free cursor\" means the clear leaves `+0x284` at 0 for the "
     "scan to find, under the clear's premises; " + REM + " and " + CLEAR + ", accepted)*.\n"),
    # S8 section 10 fragility: cursor domain as the second unchecked input.
    (POOL, "  fact, and it is the sharpest fragility in this family.\n",
     "  fact, and it is the sharpest fragility in this family *(qualified 2026-10-02, OPUS: the accepted slot packet "
     "states the same condition as a premise - stable readable flags with at least one zero - and names a second "
     "unchecked input: a starting cursor outside 0..159 addresses a row outside the pool at the first clear, before "
     "the scan begins. Both are conditional countermodels, not observed faults or hangs; " + SLOT +
     ", accepted)*.\n"),
    # R6 section 10 teardown order.
    (POOL, "  teardown that re-entered the pool would see consistent indices but a decremented count.\n",
     "  teardown that re-entered the pool would see consistent indices but a decremented count *(qualified "
     "2026-10-02, OPUS: retirement's teardown is `004200A0`, release's is the bare clear `0041F730` with no "
     "`004200A0`; in both the decrement and the new-count-0 cursor reset precede the call, and retirement then sets "
     "bit 5 of the flag word after `004200A0` returns (`00427C90`+0x123); " + REM + " with FABLE's narrowing, "
     "accepted)*.\n"),
    # C2 section 13 stubbed-effect caveat: the clear's helpers are now bounded statically.
    (POOL, "  and only because the list logic reads them. **A stubbed effect is not a proved one.**\n",
     "  and only because the list logic reads them. **A stubbed effect is not a proved one.** *(qualified 2026-10-02, "
     "OPUS: for the reset's own helper calls this is now bounded statically - their composed write footprints lie "
     "inside the record and miss `+0x0` and `+0x284` (see §4) - which bounds the effect without executing it; the "
     "other scripted callees remain oracles; " + CLEAR + ", accepted)*\n"),
    # C3 section 13a row 5.
    (POOL, "Both release paths reach `0041F730`'s whole-record `memset` |",
     "Both release paths reach `0041F730`'s whole-record `memset` *(qualified 2026-10-02, OPUS: reaching the memset "
     "is not the postcondition by itself - 125 direct writes and six calls into four helpers follow it, and `+0x284` is 0 and "
     "`+0x0` is -1 on return under the clear's premises; " + CLEAR + ", accepted)* |"),
    # S9 section 15 free-cursor row.
    (POOL, "and the scan at `00427AD2` | 1 (static) | PROVEN |",
     "and the scan at `00427AD2`; it stops within 160 visits only under stable flags with at least one zero "
     "*(qualified 2026-10-02, OPUS: " + SLOT + ", accepted)* | 1 (static) | PROVEN |"),
    # R7 section 15 return row: REFUTED convergence claim - strike and restate.
    (POOL, "| every path but the null converges on `00429296 mov eax, 1`.",
     "| ~~every path but the null converges on `00429296 mov eax, 1`.~~ Every non-null path answers 1, through two "
     "returns: the mark arm's full path loads 1 at `00429140`+0xB9 and returns at +0xC3, and every other non-null "
     "path converges on +0x156 *(corrected 2026-10-02, OPUS: three returns - +0x1C with 0, +0xC3 and +0x165 with 1; "
     + REM + " and FABLE's review, accepted)*."),
    # C4 section 15 scripted-callee row: narrowed for the clear only.
    (POOL, "and only because the list logic reads them | none | UNKNOWN |",
     "and only because the list logic reads them; for `0041F730` alone its helper write footprints are now bounded "
     "statically, inside the record and clear of `+0x0` and `+0x284`, which narrows this row for that callee without "
     "executing it *(qualified 2026-10-02, OPUS: " + CLEAR + ", accepted)* | none | UNKNOWN |"),
    # C5 "CLR is a default writer": exact counts, two copies, copy-not-zero, loop bound 10 (FABLE narrowing).
    (POOL, "  **A reconstruction that zero-fills a record produces a different record.**\n",
     "  **A reconstruction that zero-fills a record produces a different record.** *(qualified 2026-10-02, OPUS: "
     "exactly 125 direct non-stack writes plus 47 composed helper writes; the `0x40`-byte block is copied twice, to "
     "`+0x180` and `+0x1C0`, a copy and not a zero fill, whose values hold only while that writable constant is "
     "unchanged; the vec4 helper writes four 4-byte scalars per call, 16 bytes per call, at `+0x210` and `+0x220`; "
     "the channel helper writes ten 8-byte entries `+0x4C0`..`+0x510` (loop bound 10); and a named fill zeroes "
     "`+0x580`..`+0x5D0`; " + CLEAR + " with FABLE's narrowing, accepted)*\n"),

    # ---------------- the-character-render-record-array.md ----------------
    # S10 + R8 "every consumer tests that first": not universal; id is not the first allocation write.
    (ARR, "when the slot is not in use, and every consumer tests that first.\n",
     "when the slot is not in use, and every consumer tests that first *(qualified 2026-10-02, OPUS: not every "
     "consumer - the retire sweep `00427C90` selects a row on `+0x290` mask 02 and decrements the live count before "
     "it reads `+0x0` (`00427C90`+0x3D, +0x88), and the release `00429140` dispatches on `+0x284` mask 04 and "
     "`+0x290` mask 01 and never compares the id with -1, so each consumer carries its own precondition. On a fresh "
     "allocation the id is not the slot's first write either: `004279B0` links the row into the pending list first, "
     "and its self-index store (`004279B0`+0x9D) then precedes the first OR of `0x2010F9` into `+0x284` "
     "(`00420480`+0x1A) and the count increment (`004279B0`+0xCF), as separate stores and not one atomic "
     "publication; " + REM + " and " + SLOT + " with FABLE's narrowing, accepted)*.\n"),
    # S11 code-block field row: trailing comment, no strike.
    (ARR, "  +0x000  i16   id                 -1 when the slot is free; every consumer tests this first\n",
     "  +0x000  i16   id                 -1 when the slot is free; every consumer tests this first   <- qualified "
     "2026-10-02, OPUS: not every consumer, see the qualifier under section 2's list paragraph\n"),
    # S12 tail table: cursor read signed with no range check.
    (ARR, "| the allocator (`004279FA`) |",
     "| the allocator (`004279FA`), read signed with no range check before the clear it addresses, so that clear is "
     "in range only under the precondition 0..159 *(qualified 2026-10-02, OPUS: " + SLOT + ", accepted)* |"),
    # S13 tail table: count gate bounds the count only; no guard before either decrement.
    (ARR, "| the allocator refuses at 160 (`004279E9`, `00427A85`) |",
     "| the allocator refuses at 160 (`004279E9`, `00427A85`) - a bound on the count only, not on the cursor, and "
     "neither remover tests the count before decrementing it *(qualified 2026-10-02, OPUS: " + SLOT + " and " + REM +
     ", accepted)* |"),
    # R9 two-remover table: "same" - the active remover reaches the clear only through 004200A0's tail.
    (ARR, "| `00429291` → `0041F730` | same |",
     "| `00429291` → `0041F730` | the same clear, reached differently: `00427C90`+0x11E calls `004200A0`, which "
     "ends in a tail jump to `0041F730` (`004200A0`+0x146) after its fifteen calls, a step this pending arm skips "
     "*(qualified 2026-10-02, OPUS: " + REM + ", accepted)* |"),
    # R10 "removes from the PENDING list": only one of three non-null arms removes; shared count and cursor.
    (ARR, "previously described that path. Measured with",
     "previously described that path *(qualified 2026-10-02, OPUS: only one of its three non-null arms removes "
     "anything - `+0x284` mask 04 clear with `+0x290` mask 01 set; with mask 04 set it marks the row for the retire "
     "sweep (`+0x290` mask 02, `+0x2AE` mask 01) and writes through three helper-returned objects, with no count "
     "change and no clear, and with both masks clear it makes no call and no non-stack write; all three return 1, so a 1 is not a "
     "free-slot certificate. Both removers decrement the one shared count `+0x0C` and reset the one shared cursor "
     "`+0x08`; " + REM + " with FABLE's narrowing, accepted)*. Measured with"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
