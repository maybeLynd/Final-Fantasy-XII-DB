# The status order cache at `022C8B08` gets its types (OPUS, 2026-09-28)

This publication changes the type store (2 new types, 1 instance cell, 8 field rows) and adds this record.

**Question.** The status order cache is described in prose by FABLE's GA-1 record
([`kinds.md`](../ga1-status-open-bytes/kinds.md)) and by the
[00329220 page](../../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md). The type store had no row
for it. What is its extent and layout? Who builds it, who reads it, and does it live for the whole process?

**Discriminator.** Read the builder's own stores, every reader's displacements, and every write to the flag that gates the
build.

**Answer.** [`status_cache.py`](status_cache.py) ([output](status_cache.out)), static on the certified image: FAILS 0.
W failed before the patch.

**B: the builder `00273BA0` fixes the layout.**
- For i = 0 to 31 it calls `0035D330(0x1A, i)` and copies the whole 0x98-byte record to `cache + 0xA8·i`. That is six
  `movups` and one `movsd`. It then stores `i` at entry +0x98.
- It then runs four passes of `002D02C0` (kinds 1 to 4) and `002D03B0`. These fill 32 qwords each at +0x1500, +0x1600,
  +0x1700 and +0x1800. Each qword is `cache + 0xA8 × idx`, where `idx` is a signed byte from the enumeration.
- Nothing writes entry bytes +0x9C to +0xA7, or anything at +0x1900 or above.

**X: the extent is 0x1900.** The only rip-relative references into `[022C8B08, +0x1900)` are the three that load the
base (`0035D4A2`, `0035D4C4`, `0035D5D0`). `022CA408` (+0x1900) is referenced as its own base. GA-1 places the next object
there.

**R: the readers.**
- `00271FB0` picks a table by listing L: 1 → +0x1700, 2 → +0x1600, 3 → +0x1800, anything else → +0x1500. It walks 32
  qwords, reads entry +0x98 as a bit index (`bt edi, eax`), and tests the listing's order key (+0x23, +0x22, +0x24 or
  +0x21), then reads +0x25.
- `00273160` reads the +0x1700 table directly, then +0x98 and +0x23.
- `00273380` reads +0x98.
- `00273410` returns the selected table's address.

**G: built once, never rebuilt, on every direct path.**
- `0035D490` returns the cache, and `0035D5C0` only builds it. Both test bit 0x200 of `dword 022C83E8`, run `00273BA0`
  when the bit is clear, then set it.
- All 48 rip-relative references to `022C83E8` in `.text` are listed. None of the 26 writes clears bit 0x200:
  - the `and` masks (`0xFFFC02EC`, `0xFFFFFFBF`, `0xFFFFFFEF`, `0xFFFFFFEE`) all keep it;
  - the ten register stores are one-bit xor merges (bits 0, 3, 4, 5), a `btr` of bit 7, or `and`/`or` masks that keep it;
  - the only instructions that touch 0x200 are the two that set it (`0035D4B1`, `0035D5DC`).
- The cache sits in `.data`'s zero-filled tail. So it is zero at load, filled on first use, and never rebuilt or released.
- A block write over `022C83E8` through another base register is not ruled out.

**The types:**

| type | offset | field | ctype | |
|---|---|---|---|---|
| `StatusOrderCache022C8B08` (0x1900) | +0x0000 | `entries` | `StatusOrderCacheEntryA8[32]` | entry i from `0035D330(0x1A, i)` |
| | +0x1500 | `orderListOther1500` | `StatusOrderCacheEntryA8*[32]` | L other; kind 1; key +0x21 |
| | +0x1600 | `orderListL2_1600` | `StatusOrderCacheEntryA8*[32]` | L 2; kind 2; key +0x22 |
| | +0x1700 | `orderListL1_1700` | `StatusOrderCacheEntryA8*[32]` | L 1; kind 3; key +0x23 |
| | +0x1800 | `orderListL3_1800` | `StatusOrderCacheEntryA8*[32]` | L 3; kind 4; key +0x24 |
| `StatusOrderCacheEntryA8` (0xA8) | +0x00 | `record` | `EncodedIdQueryRecord` | a whole class-0x1A copy |
| | +0x98 | `rowIndex98` | `uint32` | i; readers use it as a bit index |
| | +0x9C | `unwrittenSpan9C` | `u8[12]` | DISCOVERED: not written, not read by these readers |

**Not claimed:**
- what the unwritten entry bytes are for;
- what a −1 enumeration byte would give;
- the listings' on-screen meaning (GA-1 has it);
- the enumeration's order rule.

| consumer | action | agreement |
|---|---|---|
| `_types/types.tsv` / `fields.tsv` | `StatusOrderCache022C8B08` and `StatusOrderCacheEntryA8` added (2 + 8 rows) | revised-here |
| `_types/types.tsv` `EncodedIdQueryRecord` instance cell | names the 32 embedded copies as a fourth home | revised-here |
| FABLE's GA-1 `kinds.md` (32 × 0xA8, four tables, the L mapping) | the same layout, from the builder's and readers' bytes | agrees |
| the 00329220 page (`0035D490`, `00273BA0` paragraphs) | the same; it could link the types | agrees (no edit needed) |

This is OPUS's own check; independent acceptance is requested separately.
