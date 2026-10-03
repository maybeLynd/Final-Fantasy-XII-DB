# The type-store share of the L2 expansion repairs (OPUS, 2026-10-03)

*Part (a) of `AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003`, from SWE2-AUDIT-SPEC's census
([`census2_dispositions.tsv`](../auditspec-l2-expansion-1003/census2_dispositions.tsv)). Applied by
[`apply_types.py`](apply_types.py) after SWE2-STRUCT published its own type-store edits (8b6ea9d2e); it refuses to write while
`types.tsv` / `fields.tsv` carry another lane's uncommitted lines, and it compares whole rows, so a corrected tuple cannot
stay stale in the store ([`apply_types.out`](apply_types.out): FAILS 0).*

## Every item re-read at the bytes (OPUS)

| system | address / layout | what the bytes show | declaration |
|---|---|---|---|
| S-10 | `01EF93FC` | written only by `0036D990` / `0036D9E0`, each storing (0, 0, 0, 1.0f from `01CEBBA8`) over `01EF93F0..01EF93FF`; read by 174 sites | `Vf00ConstantVector` 0x10 STATIC (not a pure constant: an initialised one) |
| S-14 | `0208D354` (`02089340 + 0x4014`) | `002339CC lea rax,[0208D354]`, `002339D3 shl rdi,7`: rows of 0x80; the index is the toggle byte `0208D454` (`002339C1 xor al,1`), so 2 rows, ending exactly at it; `002339E2 rep stosw` fills the selected row with 0x40 words of 1 | `SpawnCounterRow` 0x80, ARRAY count 2, field `counters` uint16[64] |
| S-16 | `02089358` | dword; stored as 180 at `0023A550`, as a truncated float at `0023A1F4`; read at `00234B27` | `SpawnArcDegrees` |
| S-17 | `0215F1F0` (`0215F1C0 + 0x30`) | qword stores at `002E069C`, `002E158E` | `CapabilityRow12Cell` |
| S-17 | `0209A2C4[2]` | dword store `002670D7`, word store `002670DD`; byte read `0026E02F` (movsx) | `GroupCompletionBytes0209A2C4` |
| S-28 | `02097D20` | `0025A6BE lea`, `0025A6CB imul r15,rdi,0x860` | `CameraContext` 0x860, ARRAY count 2 |
| S-36 | `0208F570` | 149 dword accesses (143 reads, 6 writes) | `GlobalFrameTick` |
| S-39 | `02EBA3F8` | 62 dword accesses (38 reads, 24 writes); boot spin-wait `0022B720` | `BootHandshakeWord` |
| S-45 | `01F83450` | `0020CD3D cmp qword,0`; alloc 0x80 + ctor `0020C730`, store `0020CD71`; delete + clear `0020CDED` | `AchievementManager` 0x80, PTR |
| S-31 | `0208E680` | 45 qword accesses: `002369A3` load, `002369AF` release through `00384500`, `002369B4` clear, before the next `003843F0` file load; the store's `BattleRuntimeUnitRecord` row calls the region from here "the battle-pool control cells", and this cell is the first of them | `BattlePackBlobPointer` - **not `licenceOwnedBits`** |
| S-09 | `ResourceSectionHeader` | `00409C30`: dword `+0x00` tag (0 / `0x4C4C4140` match any), eight dwords `+0x10..+0x2C` name key | 0x30, two fields |
| S-22 | `ActionDefinition +0x13` | `0038B295 test byte [rcx+0x13],1`; rows `0020E600(header+0x0C) + stride*id` with the stride the header's word `+0x08` (`0030D19B..0030D1E9`) | AUTHORED-stride type, `+0x13` element mask |
| S-25 | `02089378` | `AiOrderSet` already carries `ARRAY 0x02089378 stride=0x170` | already present - no change |

## Three census notes corrected (OPUS)

1. **S-31.** The census paired `0208E680` with "`licenceOwnedBits` uint8[46]". The licence contract names `0208E680` as
   the `battle_pack.bin` blob pointer the node table is read through; every access is a qword pointer operation.
   `licenceOwnedBits` is `BattleStatsRecord +0x194`, already declared (PROVEN). Declaring the cell as the bit array would
   have written a false type into the store.
2. **S-10.** "Declare or rule CONSTANT": it is neither a pure constant nor a variable - two initialisers write it, nothing
   else does; declared with its writers.
3. **S-25.** The static route the census found missing exists (`AiOrderSet` route column).

## Applied, and what is still open (OPUS)

**Applied 2026-10-03:** 12 types and 17 fields, nothing removed. SPEC's `types_census2.py` was re-run against the result:
S-10, S-16, S-22 and S-09's two `ResourceSectionHeader` fields now read FIELD, and S-17 / S-28 read GAP-SPAN (type
present, no field row at `+0`). The census outputs are SPEC's and were left at HEAD for SPEC to regenerate.

**Second pass (2026-10-03, later):** repos-91, a local helper, measured the remaining gaps, and OPUS re-read the anchors
(`0039AF27`, `0039CD8C`, `002FC2C0`/`002FC2C6`, `002FD02F`/`002FD031`/`002FD035`, `0026E01F`/`0026E026`, `0025AB15`,
`002670D7`):
- S-09: `02EBF000` is a lone float, `StaticFloat02EBF000`. Its one store is `0039AF27`, which writes 512.0 once at
  boot; it is not a registry slot.
- S-17: `02EC19C0` starts its own array, `Record02EC19C0`: 512 records of 8 bytes, zeroed by a 0x1000 memset and flush
  with the next object `02EC29C0`, with 3 field rows. `GroupCompletionBytes0209A2C4` `+0`, `+1` and `+3` are 0/1 byte
  flags ANDed by the gate `0026E01F..0026E044`.
- Routed: S-25's count of 40 to SWE2-STRUCT (OPUS-REQ-STRUCT-AIORDERSET-COUNT-1003, HIGH, not PROVEN). S-28's bare base
  to SWE2-AUDIT-SPEC (OPUS-REQ-AUDITSPEC-CENSUS2-BARE-BASE-1003): every `CameraContext` access is `+0x10` or above, and
  OPUS will not declare an unobserved `+0` field just to satisfy the census.

**Still open:**
- S-14: the census resolves `02089340+0x4014` through spans, and an ARRAY without a count has none; `count=2` is now
  declared.
- S-25: `AiOrderSet`'s ARRAY route has no count (a SWE2-STRUCT row).
- S-09 `02EBF000` and S-17 `02EC19C0` are undeclared.
- S-17 / S-28 need `+0` field rows.
- The S-19 `MovementBody` re-cut, the S-51 `BattleUnit +0x080` meaning, the five aliases and S-49's appended-section
  addresses follow as their own package.
