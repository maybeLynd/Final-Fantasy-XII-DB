# S-19 MovementBody re-cut: the fields the separation pass actually accesses (OPUS, 2026-10-03)

*This is the last open item of `AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003` (a). OPUS's census (block 214) declared 14
MovementBody rows at the widths of the allocator's zeroing stores, all reading "MEANING NOT CLAIMED". The separation
pass reads them at finer widths with definite meanings. repos-91, a local helper, re-read every width and meaning in
the six contract bodies plus `003DA8A0` (alloc), `003DA830` (shape init), `003DB020` (register), `0046AD20` (cell fill),
`00314E10` (share) and `003DA5A0`/`003DA730` (support). OPUS re-read a sample of anchors at the bytes:
`00314FEA`/`00314FEE` (+6 layer compare), `003DB03D` (+7 = 1), `00314FF7`/`00315002` (+0x119 owner compare),
`0031532B` (+0x100 push x) and `003DABD8` (the +0x18 bitmap test).*

**Applied** by [`apply_s19.py`](apply_s19.py) from [`s19_recut.json`](s19_recut.json): 14 rows out, 21 in (one merged
row deleted), in offset order inside the MovementBody block. It is idempotent ([`apply_s19.out`](apply_s19.out)) and
refuses when an old row is missing or a peer has uncommitted MovementBody lines. Every replaced row's old name and
ctype stay in the new evidence ("was ...").

| offset | was | now |
|---|---|---|
| `+0x06` | field006 u8 | `layer` u8: the resolve refuses a pair whose bytes differ (PROVEN) |
| `+0x07` | field007 u8 | `activeThisTick` u8: 1 at register, 0 at reset (PROVEN) |
| `+0x08` | field008 uint32 | `weight` f32: 1.0 at allocation, read as f32 by every reader (PROVEN) |
| `+0x18` | field018 u64, field020 u64 | `rememberedPairBitmap` u128, one bit per body index (PROVEN) |
| `+0xE8` | field0E8 u64 | `partnerPushSqLength` f32, `pushPending` u8, `contactCount` u8, `soleShareMarker` u8 (HIGH), `unobserved0EF` |
| `+0xF0`/`+0xF4` | field0F0 uint32, field0F4 u64 | `radiusA` f32, `radiusB` f32, `shape0F8` f32 |
| `+0xFC` | field0FC uint32 | `margin` f32 (HIGH) |
| `+0x100`/`+0x108` | field100 u64, field108 uint32 | `pushX`, `pushY` (HIGH: only zeroed), `pushZ` f32 |
| `+0x110` | field110 u64 | `weightMask0` / `weightMask1` u32 (PROVEN) |
| `+0x118` | field118 uint16 | `field118` u8 and `owner` u8 at `+0x119` |
| `+0x120` | field120 uint32 | `cellBitmap` u32, one bit per 16-byte mask at `02B57CE0` |

## Where the bytes disagree with the contract (OPUS; routed to the contract's owner)

`CONTRACT-separation-pass.md` §3 is FABLE's, so these were routed as OPUS-REQ-FABLE-S19-SEPARATION-CONTRACT-1003:
- **`+0x120`:** the contract says u128, but only the dword is the cell set. `0046AD20` fills a 16-byte block: `+0x124`
  is a dword, and `+0x128`/`+0x12C` are f32s.
- **`+0xE8`:** this is the squared length of the increment given to the partner in the latest contact, overwritten per
  contact. It is not the body's own accumulated push length.
- **`+0x08`:** the contract has "?"; it is f32.
- **`+0x104`:** the contract calls it the third push component, but the pass never touches it alone.
- **`+0xEE`:** "immovable" is the contract's label; the bytes show "this body took the whole share".

Not changed, because the contract does not name them, but known stale: `+0x124` is written (`0046AF4A`), and
`+0x128`/`+0x12C` are f32.
