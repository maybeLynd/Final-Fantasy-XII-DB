---
system: Nonempty PRF registration and specialized relocation lifetime
category: 02-Resource-And-Asset-Pipeline
status: PARTIAL — OV-42 stays open (its remaining producers and natural rejection are runtime; the owner-protocol scope is answered) (status line current 2026-10-02, SWE2-CONTRACT DD batch 21)
readiness: BEHAVIORALLY UNDERSTOOD
confidence: HIGH
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-10 original nonempty PRF/A00 registration, actual movement/repair and disposal on synthetic data"
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-nonempty-prf-falsification-pass-1
  crossref_clean: true
external_production:
  section: SECTION-10
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md
---

# A found resource section is not yet a usable effect

The path studied here is `00409FE0`: reuse/find a bank entry, initialize source storage, find a
same-name `@FEF`, select configuration/file metadata, create an effect ticket/context and parse its
payload. The [Section10 evidence](../_experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md)
executes this path with nonempty PRF0/1 and one actual specialized A00 subtype. It does not load a
real game asset or claim every effect subtype is understood.

## Discovery, not ownership

`00409780` initializes both index and offset to-1, normalizes a name into shared scratch, and tests
the root before its children. Magic0x50524640 spells `@FRP` in memory; PRF is the handoff shorthand.
Version0 child offsets live at+30 and version1 at+40; each is relative to that fixed table base.
Version1 skips zero slots. A PRF root match yields offset0/index-1, whereas a plain root yields0/0.
The index and offset interfaces are therefore not interchangeable success checks.

Setup `00409A60` pads input root/child names BEFORE choosing copy or retention. Mode0 owns a
buffer copy; mode1 retains a tagged source. Name padding mutation is common to both. Count, length,
termination and offset validity are preconditions, not validated asset-parser guarantees.

## Two offsets that must not be collapsed

The named FEF search is only an admission check. The actual parser offset comes from a DWORD at
`source + align64(metadataSize) - 4`, where metadata is obtained through the original selector and
provider chain. Controls put the section at0x100 but the effect data at0x300 or0x700. The latter is
what reaches ticket creation and the parser.

The last five root-name bytes also index a table of configuration strings. The test supplies a
readable no-config string and executes the original rejection path of the optional `.cm` resolver.
Configuration producer validity, substring/scanf parsing and priority assignment remain untested.

## The specialized subtype mutates backing

`003B38B0` creates a type3 borrowing context and runs `003EDAD0`. The nonempty A00 chunk registers
index1/subtype0 through `003A9A70`. `005004C0` dispatches to `00500470`; four `004304F0` calls
rebase eight DWORD encoded fields at+00/+04,+10/+14,+20/+24,+30/+34. The lookup table is context+850.
The fixture uses nonzero field values; merely writing index/subtype cannot satisfy its checks.

A copied entry modifies its owned backing, leaving original payload offsets unchanged. A tagged
entry modifies the external source directly. Reusing an existing bank match does not parse again.
But disposing and explicitly registering the same already-relocated external bytes again repeats
the offset additions. The executed path has no normalization-back-to-relative step. That is an
implementation precondition to trace through callers, not an observed shipped double-rebase bug.

## There are three different success levels

| Observation | What it does not prove |
|---|---|
| Valid bank slot | A named FEF exists or a ticket was created. |
| Ticket0 after exhaustion | Successful ticket/context creation. The bank slot can still exist. |
| Valid ticket/context | The payload signature or records were accepted. |
| Parsed subtype0 record | Other subtypes, child construction, rendering or live scheduling work. |

The fixture disposes all selected partial outcomes through the original code and checks allocator
accounting. It does not claim arbitrary allocation/error recovery.

## Movement and repair

The original compactor moves the source into a separated free hole. Before refresh, the copied
specialized words still point to the old address. The original context driver invokes `003A9BA0`,
which first specializes the new record with the delta and then updates the lookup pointer. Both
lookup and eight encoded values become consistent with the new base. A second unchanged refresh
does not add the delta twice. The borrowed run origin remains stale.

Original disposal cancels/frees context and tables before a separate external-owner release frees
backing. This agrees with [the owner policy](the-external-source-owner-and-borrowed-view-lifetime.md)
and extends [the original mover](the-source-block-mover-and-separate-consumer-refresh.md) to a
nonempty specialized case, not a universal consumer-lifetime certificate.

## Pointer resolution can produce zero by arithmetic

The contract formula stays `sext32(low32(base)+u32(offset))` after explicit entry/-1 guards.
Unsupported mode with offset0 returns0; valid cached0xFFFFFFF0 plus0x10 wraps to0 too. Thus 'no guard
fired' is not equivalent to 'nonnull pointer', and 'nonnull pointer' is not proof of readable storage.
See [the section contract](CONTRACT-resource-section-addressing.md).

## Remaining obligations

- [x] ~~**OV-39.** Producer guarantees for names, file-size metadata, offset tables and optional configuration.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): names and offset tables are guaranteed by census (every `@FRP` name NUL-terminated; all 320,736 entries in bounds, OV-26); ~~the two `@FEF`-specific inputs have no shipped producer~~ of the two `@FEF`-specific inputs only the `@FEF` data has no shipped producer *(corrected 2026-10-02, OPUS: the configuration table's populator `0040A230` runs at start-up, `RenderResourceRoot_InitializeSubcontainers+0x6B` calling `00409F80`, which calls it at `00409F80+0x4`)* - ~~the configuration table `02B64380` is never populated~~ **(`CON-195`, 2026-09-29, OPUS: it is seeded at start-up - `0041E3A0` calls `00409F80`, which calls its populator `0040A230`)**, and `@FEF` appears only in 144 PS2-era `obj_finish` `.cm` files whose end-of-extent dword never locates their EFX data; [`ov39-fef-producers-fable/`](../_index/candidates/ov39-fef-producers-fable/README.md). Register OV-39.*
- [x] ~~**OV-40.** Caller policy for re-registration of fresh versus already-relocated borrowed bytes.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5) for this path: `00409FE0` is reached only from the four owner-family completions, and each submit reads into the block its completion registers, so after a successful read only fresh bytes are rebased. Still open, kept here: what a byte-count -1 failure callback registers (no completion reads ok), and the five other `003EDAD0` drivers (OV-41's ground); [`ov40-reregistration-fable/`](../_index/candidates/ov40-reregistration-fable/README.md). Register OV-40.*
- [x] ~~**OV-41.** Other specialized subtypes, child construction and nonempty rendering consumers.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5): child construction is three registrars of one shape (`0x700` -> `003A7E80`, `0x800` -> `003A9730`, `0xA00` -> `003A9A70`, each called once from the walker `003EDAD0`), each followed by a bounded subtype setup switch; the subtypes are a closed set (4 + 9 + 65 element types, 56 element routines - the dispatch page's own census); each setup rebases or links encoded dwords at fixed offsets (`subtypes.tsv` maps 48 of 68 routines); the rendering consumers are the per-type step/update/walk/release methods and UQ-204's emits table. Still open, kept here: the 20 array-bearing setup routines' loops and what the linked `*02EBEF70` nodes are; [`ov41-efx-children-fable/`](../_index/candidates/ov41-efx-children-fable/README.md). Register OV-41.*
- [x] ~~**OV-42.** Held-state1 submission and outer service-error/callback-reuse recovery.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5) at the owner-protocol scope: a held state1 owner is never submitted (OV-34); the owner protocol has no recovery for a rejected submission — the requester rejects only on a negative narrowed index (a full queue blocks, pumping; per the OV-45 insert read), its -1 is ignored, state 3 is written, no queue entry means no callback, and a delete parks it at 5; a failed read calls back only when its byte count is -1. The arena residue is answered: arena 11 is replaced whole at a state change, reclaiming an orphan there; an arena-6 orphan is never reclaimed by any arena-level release — a permanent leak *if a rejection ever happens*, no other per-handle free found ([`ov42-arena-residue-fable/`](../_index/candidates/ov42-arena-residue-fable/README.md)). Still open, kept in the register: whether shipped play ever rejects a submission (RT); [`ov42-submit-recovery-fable/`](../_index/candidates/ov42-submit-recovery-fable/README.md). Register OV-42.* *Narrowed 2026-09-30 (FABLE, [record](../_index/candidates/astra-returns-fable-0930/README.md)): the FST table extent does not bound the narrowed owner index either; see [the indexed-source request page](the-indexed-source-request-from-arm-to-terminal-pump.md), section 3, FABLE 2026-09-30 subsection. Still OPEN.* *Narrowed 2026-10-02 (FABLE, [record](../_index/candidates/astra-returns-ov42-fable-1002/README.md), on ASTRA's four special-action packets, SWE2-AUDIT-SPEC ACCEPT on three and ACCEPT-WITH-NARROWING on one): on the special-sequence selector path only rows 511..534 (word FFFF, bit 30) can give a negative narrowed index; the row `0x113` arm is a separate premise. Class `0x14`, the bit-30 test, the conditional D0..F1 refusal and the queue remap do not exclude those rows. The queue writer's record arm (raw byte +5 zero) and its negative-override fallback cannot queue them. See [the battle-command availability page](../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md), FABLE 2026-10-02 subsection. Still OPEN.*
- [x] ~~**OV-43.** Whole-session scheduling/reentrancy and actual Windows overlapping-copy behavior.~~ *ANSWERED 2026-09-29 (FABLE, Claude Opus 5.5) for the copy half: the game imports `memcpy` from `VCRUNTIME140.dll` and ships none, so it loads System32's (14.51.36247.0); over 31,784 overlapping cases that `memcpy` never differs from an overlap-safe copy. The scheduling universality half stays superseded under OV-2 (register row); [`ov46-overlap-copy-fable/`](../_index/candidates/ov46-overlap-copy-fable/README.md). Register OV-43.*
- [x] ~~Independent acceptance of these new claims; no L2 or global score is changed here.~~ *NOT A QUESTION 2026-09-29 (SWE2-FRONTIER) under the class-2 ruling: an independent-acceptance/process item, carried by board task FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929. Register OV-44.*

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives; the OV-39 box carries CON-195

**Attack.** Each section's static clause was turned into a check at its instructions: "Discovery", the name setup, the two
offsets, the specialized subtype, and movement and repair. SECTION-10's executions are carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_nonempty_prf.py`, output `falsify_nonempty_prf.out`, image `73461d08…`, 0 BROKEN,
exit 0.

| # | Clause attacked | Result |
|---|---|---|
| R1 | "Discovery, not ownership" | **survives**. Both outputs start at −1. The name is normalized into the scratch `02B62E20`, and the magic is `@FRP`. Version 0 walks children at `+0x30` with no skip; version 1 walks `+0x40` and skips zero slots. Each child offset is relative to that fixed table base, and the root is tested first. A PRF root match writes offset 0 and leaves the index at −1; a plain root writes 0/0 |
| R2 | name setup before the mode | **survives**. Three name pads (to 32 bytes) all come before the mode branch at `00409B95`. Mode 1 keeps the tagged source at `+0x30`; mode 0 copies into owned storage |
| R3 | "Two offsets that must not be collapsed" | **survives**: the parser offset is the dword at `source + align64(size) − 4` |
| R4 | "The specialized subtype mutates backing" | **survives**. The A00 registrar stores the record in `*(02EBEF78)` at its subtype word, and `0024ED80` publishes `ctx + 0x850` there (the `0x800` table is `+0x848`). `00500470` makes four `004304F0` calls at `+0x00/+0x10/+0x20/+0x30`, and each re-encodes the two dwords at `+0` and `+4` with the delta: eight dwords |
| R5 | "Movement and repair": specialize first, then move the lookup | **survives**. For each nonzero slot, `003A9BA0` runs `005004C0` on `slot + delta` (`003A9BD9`), then adds the delta to the slot (`003A9BE8`) |
| R6 | the OV-39 box: "the configuration table `02B64380` is never populated" | **broken, by `CON-195`** (the fef page's correction, whose consumer check missed this box). `00409F80` calls the populator `0040A230` (`00409F84`), and the render resource root initializer `0041E3A0` calls `00409F80` (`0041E40B`). The rest of the OV-39 answer is untouched |

**What the player sees.** Nothing new on screen. The page had repeated a claim that the game never fills in the effect
path table. The game fills it at start-up.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`, batch 4): layers pass 22 still reported for this page. Every edge was listed in full and the call sites below were read.*

**UI — CLIENT (1 edge).** `0024B9B0` (1,500 B, filed to no owner, resolved by the audit to UI) calls the publisher `0024ED80` on its record at `0024BB6D` (one path reaches it when byte `+0x370` is 1, `0024BB5D`–`0024BB6D`). That publisher sets the registrar's table pointer `02EBEF78` to `ctx + 0x850` (ctx = `[record + 0x340]`, `0024EDC7`–`0024EDCE`), the table the A00 registrar then indexes by subtype word. The UI-side body registers through the same publisher the A00 records use, and owns nothing on this page.

**Presentation — SERVICE and CLIENT (180 edges, batch 7).** The registration and relocation code this page reads is itself mostly Presentation's, so most edges run inside one mechanism. The chunk walker `003EDAD0` is reached from `003B2220` and from the borrowing-context builder `003B38B0`, which `00409FE0` calls. It calls its three registrars `003A7E80` (`0x700`), `003A9730` (`0x800`) and `003A9A70` (`0xA00`) and the setups `003A77F0`, `003A79C0`, `003A7B50` and `003EE2D0`. The subtype publisher `0024ED80` is called by `003B27A0`, `003B3480` and `003EE2D0`. The relocation helpers carry most of the count. `004304F0` resolves a pair of encoded pointers at `p` and `p+4`, adds the delta, re-encodes both and returns `p + 0x10`. `00500470` applies it to four consecutive pairs, and `005004C0` dispatches to 38 per-element relocation bodies (`00538A60` and peers) and is called by `003A99F0`, `003A9A70` and `003A9BA0`. Fifty-seven Presentation bodies call `004304F0`, and fifty-five call `00500470`, to relocate their own records. `RenderResourceRoot_InitializeSubcontainers` (`0041E3A0`, called by `003325D0`) seeds the `@FEF` table through `00409F80` and initialises eight render containers (`0046E250`, `RenderModelInstanceContainer_InitializeStorage` `00477EE0` and six more). Presentation owns the element records; this page reads how they are registered and moved.
