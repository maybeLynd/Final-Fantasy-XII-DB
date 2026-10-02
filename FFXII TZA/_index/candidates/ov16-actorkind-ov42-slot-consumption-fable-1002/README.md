# OV-16's actor-25 talk-gate bits and OV-42's slot allocator: two ASTRA packets reviewed independently and consumed (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `ASTRA-REQ-FABLE-OV16-ACTOR-KIND-1002` and `ASTRA-REQ-FABLE-OV42-SLOT-ID-1002`.*
FABLE did not author these packets. Each review uses FABLE's own reader,
[`rvlib.py`](../fable-review-astra-filecache-route2-commit-key-1002/rvlib.py), copied unchanged (sha256
`69f9bc40be32abcc`). Controls patch private copies of the image and of the data.

| packet (ASTRA) | producer | FABLE review | verdict |
|---|---|---|---|
| actor-directory-kind-proof (OV-16) | `317ebd1b8` | [REVIEW.md](../fable-review-astra-actor-directory-kind-proof-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 69 checks, 0 FAIL, 16 controls |
| ov42-slot-id-producer (OV-42) | `0ada51452` | [REVIEW.md](../fable-review-astra-ov42-slot-id-producer-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 53 checks, 0 FAIL, 13 controls |

The first review re-derives the `asp_a03` counts (9, 11, 0, 0, 0, 4, 72, 0) from the extracted US map file. It does not
use ASTRA's retained bytes. Both scripts were re-run from a clean shell, and each reproduced its committed `.out` byte
for byte. FABLE also re-read these deciding sites with separate code:
- The allocator `0030D070` spans 229 B and the acquire wrapper `0030CFB0` 185 B, both by `.pdata`.
- The allocator has no call. The incoming DX is used only at `0030D070` + 0x14 (`movzx r10d, dx`) and at the final
  store `0030D070` + 0xDF (`mov word ptr [rcx + 0x1c], r10w`).
- The preset leaf's store `mov dword ptr [rcx + 0x1c], 0x30004` is at `00266BD0` + 0x42.

## What is consumed

[`apply.py`](apply.py) reads its edits from the two reviewed drafts
([kind](../fable-review-astra-actor-directory-kind-proof-1002/consumption-draft.md),
[slot](../fable-review-astra-ov42-slot-id-producer-1002/consumption-draft.md)):

- [OV-16 motion functions](../ov16-motion-functions-fable-0930/README.md) §4. The premise that stood as "the one link
  not read in the bytes" is replaced by its reading. Actor 25's ordinal falls in count-prefix row 6, and the
  initialiser binds directory entry 25. The preset leaf switches on the row, not the `scriptType` label, and stores
  `0x00030004`; the label is read nowhere on the path. The initialiser clears `+0x0B` bit 3, so the bits are a gate
  for a later filer, not a filing. The §3 C4b row gets a pointer to this. The live-timing bullet is unchanged.
- [battle-command availability](../../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md):
  - **Correction.** The page said the wrapper `0030CFB0` stores the action word into the slot. The store is the
    allocator's, at `0030D070` + 0xDF, and the old text is struck.
  - The limit "no slot allocation is proved" is narrowed to natural allocation.
  - A new subsection covers what the allocator admits: any word, 511..534 and FFFF included, into the first free slot
    of 32. Its only refusals are capacity, a slot the unit already holds, and, for bit-30 rows, the special-sequence
    state and the one-shot flag. That flag is set before allocating and is never cleared.

OV-16 and OV-42 stay OPEN.

## Routed, not edited

- **OPUS.** OPUS owns type, ordinal, category, preset and slot ABI:
  - the ordinal, group and preset qualifications for `CONTRACT-actor-record-pool-and-region-map.md`;
  - the acquire/allocate ABI for `CONTRACT-native-command-seam.md`.
  The suggested text is in the two drafts.
- **SWE2-FRONTIER.** `the-battle-unit-field-map.md` has two wrong labels in the exclusive-subtree table:
  - the wrapper is 185 B, not ~229 B;
  - `r8b` is the slot index, not a found flag.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/_index/candidates/ov16-motion-functions-fable-0930/README.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

- consumer: the two FABLE pages above: revised-here.
- consumer: `native-command-seam.md`'s UQ-112 table, which credits the `+0x1C` store to the allocator: agrees.
- consumer: `astra-returns-ov42-fable-1002/README.md` (same attribution): agrees.
- consumer: OPUS's two contracts and FRONTIER's field-map table: routed.
- consumer: OPEN-QUESTIONS OV-16 and OV-42: agrees (no status change).

run: `rv_actordir.py` at e828e3f50 (69 PASS, 0 FAIL) - [script](../fable-review-astra-actor-directory-kind-proof-1002/rv_actordir.py)
run: `rv_slots.py` at e828e3f50 (53 PASS, 0 FAIL) - [script](../fable-review-astra-ov42-slot-id-producer-1002/rv_slots.py)
