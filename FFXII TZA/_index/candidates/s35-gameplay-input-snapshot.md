# S-35's types gap was the contract's shared object, not the 28 tail bytes (OPUS, 2026-09-25)

Evidence class **NATIVE/STATIC**. Instruments: `gfz-scripts/s35_snapshot_refs.py` (read-only) and
hand-read bodies `002498B0`, `0035FAC0`, `0035F760`, `0035FBD0`, `00249860`, `00249880`. EXE
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

## Why this was the gap

FABLE's per-cell census (`eed0787e6`) found **S-35 the only row blocked by `types` alone**, and
asked whether that cell was worth a look (`FABLE-NOTICE-OPUS-THE-CONTRACT-COLUMN-SUMMARY-IS-NOW-INVERTED`).
The row's gap text, OPUS's own 2026-09-21 correction, blames 28 bytes: `InputBindingRecord`'s
`+0x140` tail and `InputBindingProfile`'s type-level rung. **Under SWE2-AUDIT-SEM's accepted `types: MET`
criterion (L2-VERDICTS, 2026-09-21), that is the wrong measure**. Debt bytes inside declared types
are a readiness question. The cell asks whether **every piece of state the contract names** has a
declared type with a measured extent.

`CONTRACT-input-subsystem.md` names its state in §2, "The shared object": **the published gameplay
input snapshot `02F97360`..`02F9739B`, 0x3C bytes**, and four words of it. Every other data address in
the contract is in §4, §5 or §8 invariant prose, which the ruling's precision 2 excludes from the
denominator. **The store had no type for the snapshot**: no row in `types.tsv` or `fields.tsv` named
any address in the band. So the cell was PARTIAL for a reason its text never gave. The binding records'
tail is not contract-named state at all.

## What the image says the snapshot is

**Extent, from the rebuilder's own clear.** `002498B0` zeroes the band with seven qword stores and one
dword (`002498BD`..`002498EE`). Their anchors are `+0x00`..`+0x30` in steps of 8, plus `+0x38`, so
`7 × 8 + 4 = 0x3C` and the clear ends at `02F9739B`. `002284F0` does the same eight stores.

**Three records of 0x14.**

- The fill loop sets `rbx = 02F97372` (`0024990A`) and ORs eight history words into
  `[rbx-0x12]`..`[rbx-0x4]`. It then writes four axis bytes at `[rbx-2]`..`[rbx+1]`, advances
  `rbx` by `0x14` (`00249A4A`) and runs twice (`edi < 2`, `00249A4E`). That gives channel 0 at
  `+0x00` and channel 1 at `+0x14`.
- It then copies channel 0's 16 + 4 bytes to `+0x28` (`00249A5E`/`00249A65` → `00249A71`/`00249A6B`).
  `3 × 0x14 = 0x3C` exactly.
- The two indexed readers `00249860`/`00249880` return `byte[02F97370 + 20·i]` and
  `byte[02F97371 + 20·i]`, the same stride from the reader side.

**One record, field by field.** Each field is the OR over the lookback frames of one history-frame word.

| rec | history word (accessor) | role, from the builder's arithmetic |
|---|---|---|
| `+0x00` | `+0x06` | held (set 1) |
| `+0x02` | `+0x0E` | pressed, `cur & (cur^prev)` (set 1) |
| `+0x04` | `+0x0A` | repeat filter output, index 1 (set 1) |
| `+0x06` | `+0x12` | released, `prev & (cur^prev)` (set 1) |
| `+0x08` | `+0x04` | held (set 0). In record 0 this is the contract's `02F97368` |
| `+0x0A` | `+0x0C` | newly pressed (set 0). In record 0 this is `02F9736A`, which the arbiter consumes |
| `+0x0C` | `+0x08` | repeat filter output, index 0 (set 0). In record 0 this is `02F9736C` |
| `+0x0E` | `+0x10` | released (set 0). In record 0 this is `02F9736E` |
| `+0x10`..`+0x13` | analog bytes 2, 3, 0, 1 | `+0x80`, read back signed, zeroed below the dead-zone from `003590A0` |

**The two mask sets.**

- **Set 0** (frame `+0x04/+0x08/+0x0C/+0x10`) is written by the button converter `0035FAC0` when the
  channel config byte `+9` has bit 1 clear, and by the analog normalizer `0035F760` when it is set
  (`0035FB88`, `0035FA37`).
- **Set 1** (frame `+0x06/+0x0A/+0x0E/+0x12`) is written on every normalizer call from the mask ORed
  with a second mask (`0035FA79 or ebx, r12d`). The button converter writes only set 1's held word
  (`0035FBBD`).
- The four roles are **proven by the arithmetic**. *What distinguishes set 1 from set 0 to a consumer,
  and what `r12d` carries, is MEANING NOT CLAIMED.*

**Record 2, the filtered copy.** When the control byte `02F973A0` is non-zero:

- each mask word of the channel-0 copy is ANDed with a suppress mask (`02F973A4`..`AA`) and ORed with
  an inject mask (`02F973AC`..`B0`);
- the axis bytes are zeroed when `02F973A2` is non-zero, and each is replaced by any non-zero override
  byte in `02F973B4`..`B7`;
- the pressed/repeat inject dword `02F973AE` is cleared afterwards (`00249BF8`), so injection is
  one-shot.

The contract's "filtered word `02F97392`" is record 2's `+0x0A`.

## The reference census (`s35_snapshot_refs.py`)

There are 586 rip-relative references in 207 functions over `02F97340`..`02F973D0`. **Control:**
restricted to the band itself (`--lo 0x02F97360 --hi 0x02F9739C`), the instrument returns **221
references in 74 functions**. That is the figure the contract's §6 published from an independent
sweep.

- Inside the 0x3C band, every write belongs to the two clears, `002498B0`'s fill, or three named
  writers. The first two are `002A3250`'s qword at `+0x08` and the arbiter's five word stores at `+0x0A`.
- Channel 1 (`+0x14`..`+0x27`) has **no** rip-relative reader of any field. It is reached only through
  the two indexed readers, which is what §6a of the contract already bounds.
- The control block at `02F973A0`.. is written by `00249840` and the `002D66xx` family. It is a separate
  object and **not declared here**: the contract does not name it.

## What is declared

- `GameplayInputSnapshot`, 0x3C, `STATIC 0x02F97360`, with three fields: `channel0`, `channel1` and
  `gameplay`.
- `InputSnapshotRecord`, 0x14, `EMBED GameplayInputSnapshot +0x0 stride=0x14 count=3`, with twelve
  fields covering all 20 bytes.
- Both types are **TYPE RESOLVED**, since the extent is proven. The four set-0 words and two snapshot
  fields are SEMANTICALLY IDENTIFIED. Set 1 and the axis bytes are TYPE RESOLVED.
- Validator after: **604 types, 7,366 fields, 0 errors, 0 gaps**. The two new types have no span
  collision (`check_static_spans.py`) and no embed overlap. The four collisions it reports predate
  this change and belong to other rows (`Mt19937State`, `CoreRuntimeStatic02064AA0`, …).

## What is NOT claimed

- **That S-35's types cell is now MET.** That is SWE2-AUDIT-SEM's call under its own criterion, and
  routed to it. OPUS scored neither the criterion nor this row.
- What set 1 means to a consumer, and what the normalizer's second mask is.
- The control block's semantics beyond the arithmetic above.
- Anything live: no capture was made.
