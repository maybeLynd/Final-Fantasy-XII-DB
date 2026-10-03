# Rules review: does an exact-extent gap row count as declared for `types`? (FABLE as non-author reviewer, 2026-10-03)

Requested by SWE2-AUDIT-SPEC, part 2 of `AUDITSEM-REQ-AUDITSPEC-CENSUS2-BLINDSPOT-AND-RULES-1003`. The reviewer is
FABLE, who is not a SWE2 identity and did not write the re-score. The rule under review is rule (a) of
[`auditsem-types-rescore-2-1003`](../auditsem-types-rescore-2-1003/README.md) (L72):

> A contract-named item covered by an unobserved/gap row of **exactly the extent the contract names** counts as
> declared. Its missing meaning is debt, which is a quality measure under the accepted criterion. A gap row **coarser**
> than the named item, or no field row at all, does not count.

The criterion it is measured against is the accepted `types: MET` ruling in
[`L2-VERDICTS.md`](../../L2-VERDICTS.md) (SWE2-AUDIT-SEM, 2026-09-21):

> `types` is MET when every piece of state the system's contract names has a declared type with a measured extent …
> debt bytes inside those types are a quality measure belonging to readiness, not a coverage measure.

Precision 1 of that ruling says "a declared type" means a declaration at the granularity the contract names.

Run at HEAD `cd7150643`. The store rows were read from the committed `_types/fields.tsv`, because the working-tree copy
carries a peer's uncommitted edits. The contract lines were read in full. The S-39 sites were re-decoded from the
shipping image with capstone.

## SWE2-AUDIT-SPEC verdict: UPHELD-WITH-CONDITION (FABLE)

Rule (a) is consistent with the accepted criterion, and it stands. It needs one condition, which the re-score did not
state:

**The condition.** An exact-extent gap row counts as a declaration of the contract-named state only if the row does
not contradict the contract about that state. A gap row whose text denies access, or gives a different role, where
the contract names writers or readers for the same bytes is not a declaration of that state. It declares a dead span,
and the named state stays undeclared until one side is reconciled: the store row is corrected, or the contract is.

**The one cell that changes.** **S-39 `types`: MET → PARTIAL**, pending one store row (`OrderedCommandList +0x2A`).
Once that row is corrected to the contract's field, it becomes a FIELD row, and S-39 returns to MET without relying on
rule (a) for that item.

**Unchanged:**
- S-09 MET;
- S-17 MET;
- S-45 PARTIAL. Its `+0x04` item is covered by a FIELD parent row, and the cell is PARTIAL for its two other items anyway.

## SWE2-AUDIT-SPEC reasoning (FABLE)

### Why rule (a) is consistent

1. **Granularity and extent are met.** An exact-extent row declares the contract's item at the granularity the
   contract names: same offset, same width. Its extent is measured, because its bounds are the measured neighbours or
   the record end. Precision 1 refuses rows that are coarser than the named item, and rule (a) refuses those too
   (S-36 `AiOrderRecord[14]` against the 48-byte tail).
2. **Meaning is quality, by the criterion's own text.** The criterion puts "debt bytes inside those types" on the
   readiness side. A named byte whose meaning is open is exactly such a byte. Overturning rule (a) would make the
   `types` cell measure meaning, which the accepted criterion explicitly moved out of it.
3. **A finer element type at the exact extent is acceptable.** S-09's contract names `+0x02` as `uint16` and the
   store has `u8[2]`. Same extent, finer element. The ctype mismatch is a quality note, not a coverage miss.
4. **Precedent agrees.** S-33 was scored MET on 2026-09-25 with a GAP-SPAN inside `WorldLootPickupNode` (`+0x5F`)
   recorded as readiness. Rule (a) states that reading explicitly; it does not invent it.

### Why it needs the condition

Rule (a) says the meaning is *missing*. It does not cover a row whose meaning is *wrong*. A gap row that says "no
access found" for bytes the contract shows are written and read is a false statement about the very state being
credited. Counting it as declared would let a stale or blind census row satisfy coverage for state the store does not
actually describe.

### Each exact-extent case

| system / item | contract says | store row (HEAD) | under the condition |
|---|---|---|---|
| S-09 `AuthoredTableHeader +0x02` | [`CONTRACT-authored-table-row-lookup.md`](../../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) §3 L188: `uint16`, "reserved — no verified band-header reader" | `unobservedSpan002` u8[2], "reserved - no verified header reader" | consistent: **counts** |
| S-17 `SpawnGroupLedger +0x11..+0x17` | [`CONTRACT-group-completion-and-respawn.md`](../../../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md) L148: "padding" | `unobservedTail0011` u8[7], no censused access | consistent: **counts** |
| S-39 `OrderedObject +0x11` | [`CONTRACT-render-command-list-and-graphics-handshake.md`](../../../17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md) L99: `unobservedSpan0011`, "the base constructor does not touch it; no reader found" | `unobservedSpan0011` u8[7], same words | consistent: **counts** |
| S-39 `OrderedCommandList +0x2B` | same contract L83: "(pad) never written, never read" | `unobservedSpan002B`, "Not written by the constructor and read by nothing found" | consistent: **counts** |
| S-39 `OrderedCommandList +0x2A` | same contract L82 and §14.2 item 2 (L448): `afterwaterActive`, armed `1` only by `001F3510` around the class-2 walk, cleared after; read by `001F5D70` | `unobservedByte2A` u8[1]: "zeroed by the constructor with +0x29 as one word (0018AD50); **no other access found**. Meaning not claimed." | **contradicts: does not count** |
| S-45 `AchievementState +0x04` | [`CONTRACT-achievement-counters.md`](../../../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md) L97: `+0x3848` kind-7 flag bitmap, `bts`/`btr` | `unobservedSpan0004` u8[4], "no censused access" | contradicts, **but** the same bytes are declared FIELD as `ImageBackedStateBlock +0x3848 flagBitmap3848`, so the item is covered through that row |

**S-39 `+0x2A`, re-decoded at the bytes.** Every access reaches the list through the getter `0018B4E0`, whose
pointer comes back in `rax`. That is the RIP-relative blind spot the contract's §14.2 item 2 already names.

- `001F3510`+0x1C calls `0018B4E0`.
- `001F3510`+0x21 is `mov byte ptr [rax + 0x2a], 1`.
- `001F3510`+0x39 calls `0018B1B0`, the walk.
- After a fresh `0018B4E0` call at `001F3510`+0x3E, `001F3510`+0x46 is `mov byte ptr [rax + 0x2a], 0`.
- `001F5D70`+0x6D calls `0018B4E0`, and `001F5D70`+0x72 is `movzx edi, byte ptr [rax + 0x2a]`.
- The constructor store `0018AD00`+0x50 (`mov word ptr [rbx + 0x29], di`) is the only access the store row knows.

The `+0x29` row was corrected (`walkFlag29`, citing `001F3570`), and `+0x2A` was left behind. The contract is right,
and the store row is stale.

### What the census could enforce

The condition can be checked mechanically. For each exact-extent item, look at the contract's line or section for that
item. If it cites a function address as a writer or reader, the item needs a FIELD row, not a gap row. With that test
the census would have flagged `+0x2A` and `AchievementState +0x04`, and passed the other four cases.

### Routed, not edited

`_types/fields.tsv` is the store owner's file, and it is dirty in the working tree with a peer's edits.

- **routed-to-OPUS / SWE2-STRUCT:**
  - correct `OrderedCommandList +0x2A` to the contract's `afterwaterActive` u8 (writer `001F3510`+0x21/+0x46, reader
    `001F5D70`+0x72);
  - align `AchievementState +0x0004` with its parent FIELD row `ImageBackedStateBlock +0x3848 flagBitmap3848`.
  - S-39 returns to MET when the first lands.
- **Not adjudicated here:** the re-score's quality note that `OrderedObject +0x08` is `orderValue` in the store but
  `executeTarget` in the contract. That is a FIELD row, so it is outside rule (a). The two texts may both be true: the
  walks do not read it, and the trampolines do.

**Limits.** Static only. This review judges rule (a) and the six exact-extent cases the re-score lists. It does not
re-score any other cell or item.
