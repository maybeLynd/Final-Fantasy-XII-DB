# Consumption draft: ov42-effective-id-source (FABLE, 2026-10-02)

*Links inside proposed page text are shown as `page-relative link:` paths, because they resolve from the target page, not from this folder.*

This draft is for FABLE to apply. Nothing in it has been applied yet. Its scope is the accepted claims of
[REVIEW.md](REVIEW.md), with the review's five narrowings, at the stated limits. It was drafted against the
availability page at `d9bc7155d`, after the commit "FABLE: actor 25's talk-gate bits ..." landed. The repository HEAD
was `0c4215736` when the draft was written, and the page was unchanged since `d9bc7155d`. The page has CRLF line
endings.

The request asked FABLE to do two things. First, incorporate the non-`0x9F` direct WORD `+0x714` getter, the
conditional `0x9F` table substitution and the exact AX → R8D caller transfer. Second, narrow the standard producer
frontier to the upstream `+0x714` writer and its admission. Edits 1-4 do both on the availability page. The
nullable-resolver contract, the owner-backed read preconditions and the separate O1/O2 belong to OPUS, so they are
routed with suggested text.

## Candidate pages and who leads them

The lead counts come from `git log --format=%s -- <page> | cut -d: -f1 | sort | uniq -c`.

| Page | What it says | Commit subjects by prefix | Lead | Action |
|---|---|---|---|---|
| availability page (`07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`) | special-sequence limits: "the `00387090` effective-id leg ... not covered"; slot-allocator subsection: "No command, AI or authored-VM producer is read" | FABLE 8, OPUS 2, the rest 1 each | **FABLE** | edits 1-4 (below) |
| type store `_types/fields.tsv` / `_types/types.tsv` / `_types/README.md` | `BattleUnit +0x714 actionId u16`; `BattleRuntimeUnitRecord +0x010 word0010` "MEANING NOT CLAIMED" (readers listed without the getter); the 40 / 32 record banks | fields.tsv OPUS 519, SWE2-STRUCT 52; types.tsv OPUS 266, SWE2-STRUCT 21; README OPUS 14, F-6 9 | **OPUS** | **route to OPUS** (getter/resolver contracts and widths, O1/O2); suggested text below |
| battle-action handler table (`07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`), pass-22 neighbours | "`00304850` both calls and is called by `BattleRuntime_GetEffectiveActionId` `00387090` and `...ResolveAndCache...` `00387A50`" | FABLE 4, Database 3, pass22 1 | FABLE | **disagrees** with the bytes in its second half; a correction is suggested below. It is outside this package's scope |
| formula scratch-block page (`08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md`) §2.5 | "`GetEffectiveActionId` (`00387090`) and the two formula entry points then read `+0x10` instead of `0x9F`" | Database 8, OPUS 3, FABLE 3 | tied OPUS / FABLE | **agrees**, but leaves out the null-O1 case; optional qualification in the OPUS route |
| Actor-Entity README (`04-Actor-Entity/README.md`), CombatFormula neighbour | the 149-byte resolution: `+5 == 0` → `0208D480` by `+4`, else owner → `0208DE80` by `+0xEA9`; `+0x10` substituted when `+0x714` is `0x9F` | Database 7, the rest 1 each | Database | **agrees**; it does not separate O1 from O2. No edit |
| unit display-record page (`04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`) | "`00387090` ... 149 B ... the displayed action id" | FABLE 9, FRONTIER 4 | FABLE | **agrees**: no edit |
| accessor-hub page (`00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`) Hub 4 | `0031B860`: "NULL record; no unit bound to it" | SWE2-EC7 5, FRONTIER 4, OPUS 2, FABLE 2 | SWE2-EC7 | **agrees**: no edit |

The regressions for edits 1-4 are `rv_effid.py`'s substitution, direct-leg, no-sentinel and caller-line checks,
with controls 1-6 and 14-16.

## Edit 1 (FABLE page): the special-sequence limits no longer exclude the effective-id leg

File: the availability page. Subsection: "FABLE 2026-10-02: which action rows the special-sequence path could turn
into a rejected request (OV-42)". Section: **Limits kept**, the fourth bullet.

OLD:

```
- `003068D4`, the `00387090` effective-id leg and the other callers of these functions are not covered.
```

NEW:

```
- `003068D4`, ~~the `00387090` effective-id leg~~ and the other callers of these functions are not covered.
  *(narrowed 2026-10-02, FABLE: the effective-id leg is now read where the standard-action route hands its
  word to the acquire wrapper - the effective-id subsection below)*
```

The struck span is the page's own text, and `00387090` stays cited elsewhere on the page.

## Edit 2 (FABLE page): narrow the producer limit of the slot-allocator subsection

Subsection: "FABLE 2026-10-02: what the presentation-slot allocator admits (OV-42)". Section: **Limits kept**, the
first bullet.

OLD:

```
- No command, AI or authored-VM producer is read that supplies 511..534 or FFFF.
```

NEW:

```
- No command, AI or authored-VM producer is read that supplies 511..534 or FFFF. *(narrowed 2026-10-02, FABLE:
  on the standard-action route the word is the effective-id getter's return, which passes the owner's `+0x714`
  word unchanged unless it is `0x9F`; that route's frontier is now whatever writes `+0x714` and what it admits,
  next subsection)*
```

## Edit 3 (FABLE page): point the wrapper's caller line at the new subsection

Same subsection, the **Direct callers** bullet.

OLD:

```
  wrapper has two: the script adapter `0030EEA0` (+ 0x60), and a call in a battle-action routine that this page does
  not otherwise cite. Indirect callers are not covered.
```

NEW:

```
  wrapper has two: the script adapter `0030EEA0` (+ 0x60), and a call in a battle-action routine that this page does
  not otherwise cite (its word source is the next subsection). Indirect callers are not covered.
```

## Edit 4 (FABLE page): new subsection at the end of the page

Append it after the page's current last line, "- Whole OV-42 stays OPEN." (the slot-allocator subsection's limits),
with one blank line between:

```
### FABLE 2026-10-02: where the standard-action route's slot word comes from (OV-42)

*From ASTRA's packet [`ov42-effective-id-source`] (page-relative link: `../../_experiments/evidence/ov42-effective-id-source/README.md`)
(`2cce275ad`), reviewed by FABLE ACCEPT-WITH-NARROWING
([record] (page-relative link: `../../_index/candidates/fable-review-astra-ov42-effective-id-source-1002/REVIEW.md`), 62 checks, 0 FAIL,
16 controls). Static, plus an emulation of the original bytes on synthetic query records, units, tables and a
scripted unit registry.*

- **The transfer.** The acquire wrapper's other direct caller (previous subsection) sits in case 6 of a
  battle-action routine's 13-way phase switch. There the routine passes its unit's QWORD `+0x698` as RCX to the
  effective-id getter `00387090`, and its next call is `0030CFB0`. Between the two calls, the returned AX is
  zero-extended into R8D, and nothing else writes R8 or calls anything. So the word that the wrapper hands to the
  slot allocator is the getter's return. EDX is the unit's DWORD `+8`. R9D is the unit's BYTE `+0xEA9`, loaded
  before the getter call and kept in RBX, which the getter restores. The routine is named by role here; its
  addresses are in the record.
- **The getter `00387090` (149 B; one root and two chained `.pdata` records).** It calls the owner resolver
  `0031B860` once or twice and returns a zero-extended WORD.
  - *Which record.* A non-null query whose BYTE `+5` is 0 selects record BYTE `+4` of the 64-byte bank at
    `0208D480`, without a first resolver call. Otherwise the first resolver return, O1, is stored to `02EBF188`
    (0 when null). A non-null O1 selects record BYTE `+0xEA9` of the bank at `0208DE80`. A null O1 selects none,
    and the record pointer is 0. A selected pointer is never 0, and the getter bounds neither byte index.
  - *Which word.* The second resolver return, O2, is the owner whose WORD `+0x714` is read. If that word is `0x9F`
    and a record was selected, the getter returns the record's WORD `+0x10` instead (`00387090` + 0x7E).
    Otherwise it returns the `+0x714` word itself (`00387090` + 0x88). A stored `0x9F` therefore comes back
    unchanged only when the first resolver returned null.
  - *No bound.* The getter makes six tests: the query, BYTE `+5`, O1, O2, the record pointer, and the one
    compare with `0x9F`. In the emulation, each of 511..534 is returned unchanged on both legs, and through the
    caller's line it reaches the wrapper as R8 unchanged.
  - *Two owners.* O1 and O2 come from separate resolver calls. The record follows O1 and the word follows O2.
    When the registry changes between the calls, the substitute comes from O1's record (emulated). No stable or
    shared owner is assumed. The `0x9F` compare and the returned word are also two separate reads of `+0x714`.
  - *No safe NULL.* The resolver returns 0 for a NULL query before any registry call. Otherwise it returns the
    first registry unit whose QWORD `+0x698` equals the query, or 0. A null O2 goes straight to the `+0x714`
    read, at address 0x714, and there is no sentinel return. That is a source prediction, not an observed
    fault, and no caller is shown to pass NULL.
- **Other direct callers (raw `E8`/`E9` census).** The getter has three. One is this call. One is in a later case
  of the same routine, where its AX goes to EDX for a different callee. One is in the unit display-record builder.
  Only the first is read for the transfer. Indirect callers are not covered.

So on this route the effective-id getter adds no bound. A non-`0x9F` word at O2's `+0x714` reaches the slot
allocator unchanged. The standard producer frontier therefore narrows to whatever writes `+0x714` and what that
writer admits. [The battle-unit field map] (page-relative link: `../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`) lists
three writers of the field in its census: the commit, the cancel and the reuse reset. None of them is read here for its domain. [The
formula scratch-block page] (page-relative link: `../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md`) describes the
`0x9F` substitute as a drawn id. That writer is not read here either.

**Limits kept.** These limits are ASTRA's and FABLE's.

- Valid, readable and stable query, owner, record and frame accesses, the normal native ABI and preserved
  nonvolatile registers are premises.
- O1 and O2 are not shown to be the same unit, or to be the caller's own unit. O2 is the first registry unit with
  the query's `+0x698`. Owner lifetime, reuse and registry order are not read.
- The banks' initialization, contents and extent are not read. No value domain is claimed for record `+0x10`.
- No natural `+0x714` value, NULL caller, fault, command acceptance or execution is observed.
- The caller's line is placed inside one case of the routine. It is not proved from a natural entry, and the
  routine's unit, records and phase byte are premises.
- Whole OV-42 stays OPEN.
```

### Citations and the neighbour gate

Edit 4 cites four functions: `00387090`, `0031B860`, `0030CFB0` and `0030D070`. All four are already cited on the page
at `d9bc7155d`, so none is new. The interior addresses are written `00387090` + 0x7E and + 0x88. The only new
8-digit tokens in the page are the data cells `0208D480`, `0208DE80` and `02EBF188`, which are not `.text`.

These functions are **named by role** and not by address, so that no new caller edges are imported:

- the battle-action routine `00304850`, which holds the transfer and the getter's second call (its ledger name is
  `BattleUnit_AdvanceStandardActionState`);
- the unit display-record builder `00329220`, the getter's third direct caller;
- the registry count and by-index helpers `00236850` / `00236820`, which the text calls "the registry". The page
  already cites them elsewhere, but edit 4 does not need them.

Their addresses are in the review record.

Pre-check: FABLE's `Database/Tools/work/FABLE/pub140-scratch/tools/xlayer.py` was run on a scratch copy of the page at
`d9bc7155d` with edits 1-4 applied (in this session's scratchpad, never in the repository), using
`--only 00387090,0031B860,0030CFB0,0030D070`. It reported **`UNACCOUNTED: 0`**. The only foreign layers are
`0031B860`'s existing edges (ActorEntity, Items_Equipment_Shops_License, Movement, Rewards_Progression_Economy and
Status_Periodic_Terminal), all of them accounted, and the HEAD copy gives the same output. Over the whole page,
`xlayer.py` and `xlayer_full.py` give byte-identical output for the HEAD copy and the edited copy (`UNACCOUNTED: 0`),
so the edits add no edge.

## Route to OPUS: the type store (`_types/`), getter versus resolver contracts

The packet assigns OPUS the effective-id getter versus nullable owner-resolver types and contracts, the return
widths and the separate O1/O2. OPUS leads the type store: `_types/fields.tsv` has OPUS 519 commit subjects of about
620, `_types/types.tsv` has OPUS 266, and `_types/README.md` has OPUS 14. Placement is OPUS's choice. Suggested
text:

```
- Effective-id getter vs owner resolver (FABLE review of ASTRA `ov42-effective-id-source`, 2026-10-02,
  _index/candidates/fable-review-astra-ov42-effective-id-source-1002/REVIEW.md):
  - Owner resolver `0031B860` (83 B), NULLABLE: RCX = a stats-record query. NULL -> RAX = 0 before any registry
    call. Otherwise it returns the FIRST registry unit (by-index order, null entries skipped, the count re-read
    each step, signed compare) whose QWORD +0x698 equals the query, as a full 64-bit pointer, or 0.
  - Effective-id getter `00387090` (149 B; root + two chained .pdata records), OWNER-BACKED: RCX = the same query.
    It returns EAX = a zero-extended u16. Precondition: the second resolver call (O2) is non-null. There is no NULL
    guard: a null O2 still reads WORD [0 + 0x714].
    - Two separate resolver calls: O1 (resolver leg only, stored to QWORD 02EBF188, 0 included) selects the
      BattleRuntimeUnitRecord (0208DE80 bank by O1 +0xEA9; or the 0208D480 bank by query byte +4 when query +5 == 0,
      with no O1 call). O2 supplies BattleUnit +0x714. O1 == O2 is not guaranteed.
    - Result = O2 +0x714, except 0x9F with a selected record -> record WORD +0x10. The record pointer is 0 only
      for a null O1. The byte index is not bounded against the 40 / 32 bank sizes.
  - BattleRuntimeUnitRecord +0x010 (word0010): reader 00387090 + 0x7E (the 0x9F substitution) is missing from the
    row's reader list.
```

The formula scratch-block page's §2.5 sentence "`GetEffectiveActionId` (`00387090`) and the two formula entry points
then read `+0x10` instead of `0x9F`" is right for the getter whenever a record is selected. It leaves out the
null-O1 case, where the getter returns `0x9F` itself. The page is tied OPUS 3 / FABLE 3, so the qualification is
offered to OPUS with the type-store route and is optional.

## Noted for FABLE, outside this package: the handler-table neighbour sentence

The battle-action handler table's pass-22 neighbour paragraph says "`00304850` both calls and is called by
`BattleRuntime_GetEffectiveActionId` `00387090` and `BattleRuntime_ResolveAndCacheEffectiveActionId` `00387A50`".
The bytes show otherwise. The getter's only calls are the two resolver calls (the review's CFG check). The raw
census gives `00304850` exactly one direct caller, `00307BE0` + 0x39 (the `rv_effid.out` NOTE line). Suggested
correction, for a later FABLE package with its own correction record:

OLD:

```
layer's effective-action-id resolvers directly: `00304850` both calls and is called by
`BattleRuntime_GetEffectiveActionId` `00387090` and `BattleRuntime_ResolveAndCacheEffectiveActionId`
`00387A50` — the handler table resolves the effective action id through them before dispatching.
```

NEW:

```
layer's effective-action-id resolvers directly: `00304850` ~~both calls and is called by~~ calls
`BattleRuntime_GetEffectiveActionId` `00387090` and `BattleRuntime_ResolveAndCacheEffectiveActionId`
`00387A50` — the handler table resolves the effective action id through them before dispatching. *(corrected
2026-10-02, FABLE: neither calls `00304850` directly; the getter's only calls are its two owner-resolver calls,
and the raw census gives `00304850` one direct caller elsewhere; FABLE review of ASTRA `ov42-effective-id-source`)*
```

Before applying it, check whether `00307BE0` is already cited on that page.

## Optional: register row OV-42 (FABLE, at publish time)

Append this to the OV-42 status cell and keep its current text:

```
2026-10-02 (FABLE): on the standard-action route the slot word is the effective-id getter's return - the owner's
+0x714 word unchanged unless it is 0x9F with a selected record, then the record's +0x10 word; no candidate bound
(ASTRA ov42-effective-id-source, FABLE review ACCEPT-WITH-NARROWING). The route's frontier is the +0x714 writer and
its admission.
```

Escape any literal `|` before writing it into the row.

- consumer: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md` OV-42 subsections - revised-here (edits 1-4)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

run: `rv_effid.py` at HEAD a7cb39140 (62 checks, 62 PASS, 0 FAIL, 16 controls)
