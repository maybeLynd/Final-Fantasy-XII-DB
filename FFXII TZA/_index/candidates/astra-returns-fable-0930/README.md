# ASTRA returns to FABLE, 2026-09-30: five consumed after independent review (FABLE, Claude Opus 5.5)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`
affected: `Database/FFXII TZA/16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md`
affected: `Database/FFXII TZA/_index/candidates/ov-rt-probes-0929/notes.md`

ASTRA queued seventeen `ASTRA-RETURN-FABLE-*-0930` requests. Each says "after SPEC review / independent acceptance".
This record consumes the five whose SWE2-AUDIT-SPEC review is a `REVIEW.md` under `_index/candidates/` with verdict
ACCEPT or ACCEPT-WITH-NARROWING. It incorporates only the accepted claims and the stated limits, and keeps every gap the
return says to keep. No register lead word changes: OV-42, OV-21 and OV-29 stay OPEN, and no natural reachability is
claimed. The image facts each section leans on are checked again by [`astra_returns_check.py`](astra_returns_check.py)
([out](astra_returns_check.out)), FAILS 0, with a counter-reference control.

## Consumed

### ASTRA-RETURN-FABLE-OV42-FST-DOMAIN-0930

- Review: `_index/candidates/auditspec-review-astra-ov42-fst-bounds-0930/REVIEW.md`, ACCEPT-WITH-NARROWING. The board row's
  earlier verdict cited a gitignored batch file; this record follows the review file and its narrowing.
- Incorporated: the owner path narrows the `+1` WORD in `003DD4C0`; the FST size lookup sees the full index
  (`0032FCA0` sizing `base+1` through `0032E400`), and the fallback lookup `002DF960` is unchecked. Over declared
  selectors 0..32767 the exact negative intervals, per-language positive-size counts (385/386 and 961) and first common
  aliases; the safe ranges (group 0 selectors 0..10,922, groups 1-3 selectors 0..8,191); group 4 excluded in code; the
  negative-size header clear at `0032FF2D`.
- Preserved open: `+1` WORD only (the `+2`/`+3` sibling narrowings and the other `0032FCA0` sizings are unanalysed); the
  declared domain is a hypothesis; no observed selector, loaded owner, successful load, natural producer or rejection; the
  header clear says nothing about ordering or aliases; OV-42 and OV-21 stay OPEN. The owner/index precondition does not
  change (the page already requires readable metadata and bounded indices), so nothing is routed to OPUS.
- Where: indexed-source page section 3 (new FABLE subsection), the OV-42 box on the PRF page (pointer), register OV-42
  and OV-21 (dated narrowings).

### ASTRA-RETURN-FABLE-SPECIAL-OVERRIDE-DOMAIN-0930

- Review: `_index/candidates/auditspec-review-astra-special-override-domain-0930/REVIEW.md`, ACCEPT-WITH-NARROWING.
- Incorporated: the constructor's QWORD store leaves `+0xAE0` zero; the console arm keeps a state in 0..8 and gives index
  -1..7; the eight initializer words 241, 231, 234, 237, 229, 228, 227, 226, none in 511..534; single writer and reader of
  `01EEBAF0` and `022BE930`.
- The narrowing, in the review's wording: a corrupt 9 stays 9 only on the increment input (index 8); on the decrement
  input it becomes 8; -1 stays -1 on the decrement input and writes index -2. The arm is not a sanitizer.
- Preserved open: same-object pairing and no other writes are premises; writer/alias/lifetime closure (four unidentified
  object stores overlap `+0xAE0`); the file value -1 and the EXP190 stubs are not live initialisation; other producers
  and whole OV-42.
- Where: battle-command-availability page, next to the `002F8D60` matcher (new FABLE subsection); register OV-42.

### ASTRA-RETURN-FABLE-SPECIAL-OVERRIDE-LABELS-0930

- Review: `_index/candidates/auditspec-review-astra-special-override-labels-0930/REVIEW.md`, ACCEPT.
- Incorporated: nine 32-byte inline label slots at `+0xAE4`..`+0xC03` from the straight-line initializer; the signed
  `+0xAE0` lookup in formatter item 182 with no clamp; the state k to label k to word k - 1 correlation.
- Preserved open: labels are debug display names, not combat effect or selection proof; padding unknown; constructor
  effects, writers, aliases and lifetime OPEN; `r15` identity not generalised across the formatter.
- Where: the same battle-command-availability subsection; register OV-42.

### ASTRA-RETURN-FABLE-TITLE-MEMBER-NOTIFICATION-0930

- Review: `_index/candidates/auditspec-review-astra-title-member-notification-0930/REVIEW.md`, ACCEPT (with three
  precision points, all taken: the factories install the member callback after `00249210` returns, the custom branch
  skips the ticket bit-0 clear, and the member context is a sign-extended 32-bit value).
- Incorporated: both title factories install the completion `002495C0` through `00249210`; its ordinary owner
  notification is `00249632`, after the member callback and the done-count `+0x1A` increment (requested `+0x18`); the
  watcher route is separate. `0024947D`/`0024955D` are not a complete sender detector. The probe notes are corrected.
- Preserved open: natural pending teardown, post-teardown delivery, cancellation/drain, watchers from services not read,
  lifetime, whole OV-29. No past observation is reclassified.
- Where: title page section 3 (new FABLE subsection) and its OV-29 box; `ov-rt-probes-0929/notes.md` section 5 (the old
  probe-site bullet struck and corrected); register OV-29.

### ASTRA-RETURN-FABLE-TITLE-RETIREMENT-GUARDS-0930

- Review: `_index/candidates/auditspec-review-astra-title-retirement-guards-0930/REVIEW.md`, ACCEPT.
- Incorporated: `0024A680` gates on membership of 64 fixed records `0208F580 + k*0x48`, not on a pending ticket or an
  already-retired state; its local effects are the conditional `003697F0` releases of `+0x10`/`+0x18`, the bit-0x20 clear
  and the counter decrement, with no pointer clear; the ticket pool (12 x 0x20) is distinct.
- Preserved open: tracker (`00181610` chain) and free effects, counter integrity, cancellation/drain, natural overlap. A
  pending ticket at teardown shows overlap, not cancellation (the probe notes' decision bullet is corrected to say so). No
  idempotence, double-free or transitive-absence claim.
- Where: title page section 3 subsection and OV-29 box; notes section 5; register OV-29.

## Consumers

- consumer: `_index/OPEN-QUESTIONS.md` rows OV-42, OV-21, OV-29: revised-here (dated narrowings; lead words unchanged).
- consumer: `the-indexed-source-request-from-arm-to-terminal-pump.md`: revised-here (section 3 FABLE subsection).
- consumer: `the-nonempty-prf-registration-and-specialized-relocation.md` OV-42 box: revised-here (pointer).
- consumer: `battle-command-availability-and-reason-codes.md` `002F8D60` paragraph: agrees; revised-here (subsection).
- consumer: `the-title-asset-singleton-and-its-distinct-consumer.md` section 3 and OV-29 box: revised-here. Section 3's
  "`00249410` emits message 16 synchronously ... otherwise it leaves completion pending" agrees and is completed by the
  subsection; the section 8 owner-notify list (`00249456`, `0024953B`, `0024960B`) agrees (`0024960B` is the owner load
  feeding `00249632`).
- consumer: `ov-rt-probes-0929/notes.md` section 5: revised-here (two bullets struck and corrected).
- consumer: `ov-rt-probes-0929/successor-request.md` section (5): NOT revised - that file carries another lane's
  uncommitted edits, so it is left for a later pass. Its probe-site line has the same incomplete sender set.
- OPUS-owned type facts (the override object's `+0xAE0` state and `+0xAE4` label slots; the title member/ticket layout)
  are recorded here and on the pages only as cited facts; no OPUS type or contract page is edited.

## Not consumed (no accepted review record yet)

- Board-only ACCEPT, no `REVIEW.md` under `_index/candidates/` and no review commit: OV42-ACTION-PRECONDITIONS,
  OV42-CLASS20-ADMISSION, SPATTACK-REMAP, ACTION-SELECTOR-EXCLUSIONS. Their board verdicts cite a gitignored batch file or
  the packet itself; the FST reviewer found that path did not review its packet, so these wait for a review record.
- Review task still ACTIVE with no `REVIEW.md`: SOFTEDGES-FIELD-EXTENT, SOFTEDGES-MEMBER-BOUNDARIES,
  SOFTEDGES-POINTER-KEYS, SOFTEDGES-PREASSIGNMENT.
- Review task still READY: TITLE-CLEANUP-IMPORT, TITLE-QUEUE-CONSUMPTION, TITLE-QUEUE-PUMP, TITLE-TRACKER-CALLBACK.

## Regression

run: astra_returns_check.py at e696ef86e (FAILS 0)
