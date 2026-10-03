# Consumption draft: ov42-mode17-query-boundaries (FABLE, 2026-10-02)

*Paths in this draft are plain backticked text. When FABLE applies the edits, it turns the packet and record paths in
the proposed page text into page-relative links in the page's usual style.*

This draft is for FABLE to apply. Nothing in it has been applied yet. Its scope is the accepted claims of
`_index/candidates/fable-review-astra-ov42-mode17-query-boundaries-1002/REVIEW.md`, with the review's five
narrowings, at the stated limits. The publication's evidence is the two folders
`_experiments/evidence/ov42-resource-mutator-mode17/` and `_experiments/evidence/ov42-resource-eligibility-domain/`
(narrowing 1). The record path the board request names does not exist, so cite the folders.

It was drafted against these page versions. The availability page was at `1c4c5820f` ("FABLE: the kind-4 classifier
publishes kind 4 exactly for full 32-bit row quotients 208..225 ..."), which contains the 2026-10-02 OV-42 subsections
from `b128c3a2c` and `1c4c5820f`. Console slice A was at `804fe1421`. The repository HEAD was `c2fc944fe`, and
neither page had working-tree changes. The availability page has CRLF line endings, and slice A has LF. If either
page's `git log -1 --format=%h -- <page>` no longer prints those commits, re-read the page before applying.

The request asks FABLE to narrow the OV-42 first-query uncertainty and to record the call-versus-visible-effect
semantics. Edit 1 does both on the availability page. Edit 2 is an optional one-sentence qualification on FABLE's
console slice A, which already names the Invincible reader. OPUS owns the paired WORD mask, ABI and precondition
contracts, and the MP page is not FABLE-led. Both are routed with suggested text.

**Composition with the concurrent drafts.** Another FABLE helper is drafting additions to the availability page for
the caller-row and terminal-helper packets. The terminal-helper packet concerns the consume path `00305640`, which
this packet's modifier is called from. This draft therefore makes **no** OLD -> NEW edit to the availability page.
Its only change there is one new subsection appended at the end, after whatever the other drafts and the
action-table-binding draft append. The subsection describes `00305640` only through its two calls (+ 0xB4, + 0xCD).

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | What it says | Commit subjects by prefix | Lead | Action |
|---|---|---|---|---|
| availability page (`Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`) | the OV-42 subsections; nothing yet on the cost leg's MP modifier, its masks or mode 17 | FABLE 10, OPUS 2, the rest 1 each | **FABLE** | edit 1 (below) |
| console slice A (`Database/FFXII TZA/00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md`) | "**Invincible** is read by `BattleTarget_ComputeUnitEligibilityMask` through `0017D470` ... which is why the arm cycles it through three states." | FABLE 5, OPUS 2, the rest 1 each | **FABLE** | edit 2 (optional) |
| MP page (`Database/FFXII TZA/10-Status-Periodic-Terminal/where-mp-comes-from.md`) | the late veto paragraph cites EXP-061's isolated run with a nonzero global high half | Database 12, OPUS 3, FABLE 2 | Database | **route to OPUS** (suggested text below) |

The regressions for edits 1 and 2 are `rv_mode17q.py`'s query store-list, upper-WORD arm, getter, accessor,
constructor, modifier-leg and census checks, plus its 1024-run global sweep, 3456-state unit grid, two-read, lazy-path
and modifier-order emulations, with controls 1-18.

## Edit 1 (FABLE page): new subsection at the end of the availability page

Append it after the page's last line, with one blank line between. At `1c4c5820f` that line is "- Whole OV-42 stays
OPEN." (the kind-band subsection's limits). If the caller-row, terminal-helper or action-table-binding subsections
have been appended since, append this one after them.

```
### FABLE 2026-10-02: what can veto the consume path's MP decrease, and what has already happened when it does (OV-42)

*From ASTRA's publication `ov42-mode17-query-boundaries` (`7b4e2b92c`), the two folders
`_experiments/evidence/ov42-resource-mutator-mode17/README.md` and
`_experiments/evidence/ov42-resource-eligibility-domain/README.md`, reviewed by FABLE ACCEPT-WITH-NARROWING (record
`_index/candidates/fable-review-astra-ov42-mode17-query-boundaries-1002/REVIEW.md`, 65 checks, 0 FAIL, 18 controls).
Static, plus an emulation of the original eligibility queries, the `+0xC20` getter and the settings accessor, and of
both resource modifiers with their outside callees stubbed.*

- **The call.** The consume path `00305640` (+ 0xB4) passes the negated MP cost to the primary resource modifier
  (`BattleStats_ModifyPrimaryResource`, on the MP page). It passes mode 16 or 17: bit 4 is always set, bit 7 is
  always clear, and bit 0 is set when the path's R12D is nonzero. Its next call (+ 0xCD) passes the same mode to the
  secondary modifier.
- **Mode 17 skips the entry check.** Bit 0 skips the entry leg, which tests the **low** WORDs of the global and unit
  eligibility masks. In mode 16 that leg runs before anything else.
- **On a decrease, the notification comes first.** If the owner unit exists, the modifier first calls the publisher
  that bit 7 leaves enabled. It passes the owner's DWORD `+8`, the old MP, the clamped new MP and 1. Only then does it
  run both mask queries again and test their **upper** WORDs. If either is nonzero, it returns: MP is not stored, and
  the recovery accumulator is not cleared. The publisher has already been called by then. That is a call attempt,
  and what it shows on screen is not read.
- **The global mask cannot veto.** The shipping global query zeroes its result DWORD and writes only its low WORD,
  and it makes no call. So its upper WORD is always 0. This was emulated over every input bit at eight stack
  alignments. The earlier mode-17 model with a nonzero global upper WORD needs a replaced callee. It is an
  intervention, not shipping behaviour.
- **The unit mask's upper WORD is the console's Invincible setting.** The unit must be nonNULL with DWORD bit 4
  set. The unit query then reads `+0xC20` of the console settings object twice, through two separate getter calls.
  Bit 0 is set when the first read is 1, the unit's current stats exist and their byte `+5` is 0. Bit 1 is set when
  the second read is 2. With one value read twice, the upper WORD is 0, 1 or 2. Two different reads could make 3,
  which is a supplied model. So in mode 17, Invincible 1 or 2 stops an MP decrease after its notification attempt.
  A positive delta never consults the queries.
- **The settings object.** Its accessor builds the object only when its root is NULL: it allocates 0x10E8 bytes,
  constructs with `001CCB20` and stores the constructor's result. Otherwise it returns the root with no call and no
  store. In a displacement census the root is stored only on two such NULL paths. One of them is reached from the
  startup manager-init burst. The constructor stores 0 to `+0xC20`, but seven unread calls follow that store, so 0
  is not shown to be the final default.
- **The secondary modifier.** In mode 17 it stores its WORD `+6` and then calls its follow-up with the full mode,
  without consulting the queries.
- **A link to the special-sequence state.** The unit mask's low bit 3 (value 8) is set when the unit's byte `+4`
  bit 5 is set and `022C2160` is not 5 or 6. It is a low-WORD bit, so it matters only to the mode-16 entry check,
  never to the late veto.

**What this changes for OV-42.** The first-query uncertainty in the cost leg's mode-17 decrease is narrowed. A late
veto can come only from the unit mask, that is, from Invincible 1 or 2 on an eligible unit, under the premises
below. A vetoed decrease splits the call from the effect: the notification call is attempted, but the stored MP does
not change.

**Limits kept.** These limits are ASTRA's and FABLE's.

- Natural initialization timing of the settings root is not read, and neither are other writers of the root or of
  `+0xC20` during a query, concurrency, ownership or lifetime. The console's Invincible arm is the known writer of
  `+0xC20`, and it wraps at 3 (console slice A).
- The effects of the two publishers, the accumulator clear and the secondary's follow-up are not read. So no
  visible presentation is claimed for a vetoed decrease, and no whole-call no-effects claim is made.
- Whether normal play reaches mode 17 with a negative delta and Invincible 1 or 2 is not shown.
- Valid storage, private frames and the Win64 ABI are premises. The table binding and whole OV-42 stay OPEN.
```

### Citations and the neighbour gate

The new text has three 8-digit tokens: `00305640` (a function entry, cited 4 times on the page at `1c4c5820f`),
`001CCB20` (a function entry, cited once) and `022C2160` (a `.data` cell, cited 5 times). None is new. The
`00305640` interior offsets are written as `+ 0xB4` and `+ 0xCD` after the entry address, and are not bare
interior addresses.

These are **named by role** and not by address, so that no new caller or callee edges are imported:

- the primary and secondary modifiers `00300CE0` and `00300BC0` (the first by its ledger name, which the MP page
  uses);
- the global and unit queries `0030B770` and `0030B7F0` ("the global mask", "the unit mask");
- the getter `0017D470`, the accessor `001D50D0` and its twin `001D5090`;
- the publisher `0028F1F0`, the accumulator clear `002FA540`, the secondary's follow-up `0030E060`;
- the root cell `01F81428` ("its root").

Their addresses are in the review record. The neighbour pre-check (`xlayer.py`) was **not** run for this draft.
Before publishing, FABLE should run `xlayer.py --only 00305640,001CCB20` and the full-page edge diff on a staged copy
of the page.

## Edit 2 (FABLE page, optional): console slice A, the Invincible bullet

Section 7, the UQ-5 answer, in the list "**That also says what the four consumed fields mean to their readers.**"

OLD (as at `804fe1421`):

```
        - **Invincible** is read by `BattleTarget_ComputeUnitEligibilityMask` through `0017D470` (`0030B883`,
          `0030B8B6`). So invincibility is implemented as a target-eligibility mode, which is why the arm cycles
          it through three states.
```

NEW:

```
        - **Invincible** is read by `BattleTarget_ComputeUnitEligibilityMask` through `0017D470` (`0030B883`,
          `0030B8B6`). So invincibility is implemented as a target-eligibility mode, which is why the arm cycles
          it through three states. *(narrowed 2026-10-02, FABLE, reviewing ASTRA's `ov42-resource-eligibility-domain`:
          the two reads are separate getter calls. Mode 1 sets bit 0 of the mask's upper WORD when the unit's
          current stats exist and their byte `+5` is 0, and mode 2 sets bit 1. A nonzero upper WORD stops an MP
          decrease in `BattleStats_ModifyPrimaryResource` after its notification attempt. See the OV-42 mode-17
          subsection of `07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`.)*
```

The new text adds no address token. All three addresses are already in the bullet.

## Route to OPUS: the paired masks and the MP page

The request assigns OPUS the paired WORD masks, the two independent reads, and the initialized-root, ABI and
no-interference premises. Placement is OPUS's choice. Suggested contract text:

```
- Eligibility masks (FABLE review of ASTRA ov42-mode17-query-boundaries, 2026-10-02,
  _index/candidates/fable-review-astra-ov42-mode17-query-boundaries-1002/REVIEW.md):
  - global 0030B770: DWORD result zeroed at + 0x15, only `mov word ptr [rbp], ax` after; no call. High WORD == 0
    for every input; low WORD in 0..31 from 02089340 (mask 0x3080, bits 10, 9, 11) and bit 0 of 022C2158.
  - unit 0030B7F0(unit, edx): 0 unless unit != NULL and DWORD [unit] bit 4. High WORD =
    (getter#1 == 1 && [unit+0x698] != NULL && byte [[unit+0x698]+5] == 0 ? 1 : 0) | (getter#2 == 2 ? 2 : 0),
    getter = 0017D470 (DWORD [settings + 0xC20]). Two calls, two reads: 0..3 in general, 0..2 when both see one
    value. Low bit 1 needs EDX != 0; 00300CE0 passes EDX = 0 at both call sites.
  - accessor 001D50D0: nonNULL root 01F81428 -> returned, no call, no non-stack store; NULL -> alloc 0x10E8
    (00210EC0), ctor 001CCB20 on success, root := ctor RAX (NULL on failed alloc; the getter then reads [0xC20]).
    Second NULL-path initializer 001D5090 (startup burst, via 001C1940). No other root store in the disp32 census.
  - premises: initialized root, no other root/+0xC20 write during the query, private frames, Win64 ABI (RBX
    carries the unit and then the WORD across the getter calls).
```

The MP page is led by the Database prefix (Database 12, OPUS 3, FABLE 2). Its paragraph "One ordering quirk, real
and visible in the body" cites EXP-061's isolated run of the modifier with a nonzero global high half. That run's
result stands, but its global mask was a substituted callee. Suggested qualification, appended after that paragraph's
sentence ending "...a mutant with the late global test removed is rejected.":

```
*(qualified 2026-10-02, FABLE review of ASTRA `ov42-resource-eligibility-domain`: the global mask in that run was a
substituted callee. The shipping `BattleTarget_ComputeGlobalEligibilityMask` zeroes its result and writes only the
low WORD, so its high half is always 0. On the shipping code the late veto can come only from the unit mask's high
half, which is the console's Invincible setting (`+0xC20`) read twice.)*
```

## Optional: register row OV-42 (FABLE, at publish time)

Append this to the OV-42 status cell and keep its current text:

```
2026-10-02 (FABLE): in the cost leg's mode-17 MP decrease the late veto can come only from the unit mask's upper
WORD (Invincible +0xC20 read twice: 1 with current stats byte +5 == 0, or 2); the global mask's upper WORD is always 0,
so the earlier first-global-nonzero case is an intervention. The notification call precedes the veto (call attempt,
not shown effect). ASTRA ov42-resource-mutator-mode17 + ov42-resource-eligibility-domain, FABLE review
ACCEPT-WITH-NARROWING. Root initialization timing and other +0xC20 writers stay OPEN.
```

Escape any literal `|` before writing it into the row.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edit 1)
- consumer: `Database/FFXII TZA/00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md` Invincible bullet - revised-here if edit 2 is applied
- consumer: `Database/FFXII TZA/10-Status-Periodic-Terminal/where-mp-comes-from.md` late-veto paragraph - routed to OPUS

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_mode17q.py` at HEAD c2fc944fe (65 checks, 65 PASS, 0 FAIL, 18 controls)
