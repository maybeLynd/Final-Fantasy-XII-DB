**What `00323D10` is.** `BattleStats_CheckLicenseNodeAcquireReason(record, node, flags)`, 428 B (`00323D10`–`00323EBB`), read whole from the shipping bytes, with every callee read one level down. It returns a **reason code** (0 means the square may be taken) and **writes nothing**: it has no store to memory, and its only side effects are its callees' reads. Static read only; nothing was executed.

**Arguments.**

- `rcx` is the character's `0x1C8`-byte stats record (`rbp`, `00323D26`). The wrapper `00323600` (43 B) computes it as `[02EBF190] + 8 + slot × 0x1C8` (`0032360F`–`00323627`). It passes `rcx = 0` when `slot > 0x27` (`00323600`–`00323605`).
- `edx` is the node number, zero-extended from a `u16` by the wrapper (`00323607`, `00323624`). It is kept in `ebx` (`00323D22`).
- `r8d` holds the flags. Only bit 0 matters: `esi = ~flags & 1` (`00323D1F`–`00323D29`), so `esi = 1` means "charge LP".

**Callers.**

| caller | site | args | uses the result as |
|---|---|---|---|
| `00323600` (slot wrapper) | `0032360A`, `0032362A` (tail jumps) | `flags` passed through | — |
| ← `0055BFF0` (board sweep) | `0055C163` | `flags = 0` (`0055C111`) | reason → display table `0055C504` (16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md:146-157) |
| ← `0055E2C0` | `0055E363` | `flags = 0` (`0055E35D`) | reasons 3, 4 and 5 are skipped (`0055E368`–`0055E36E`) |
| ← `0055F830` | `0055F96F` | `flags = 0` (`0055F969`) | kept in `ebp`, then story flag `0x4B9` is tested (`0055F974`–`0055F97B`) |
| ← `00282E80` | `00282E87` | `flags = 0` (`00282E84`) | `return reason == 1`, meaning "owns it" (`00282E8E`–`00282E91`) |
| `00323910` (node set/clear) | `0032396D` | `flags = its 4th arg` (`00323965`), and only when `set != 0` (`0032395C`) | any non-zero result returns `-1` with no write (`00323972`–`00323979`) |

Who calls `00323910`, and what it passes:

- The menu grant `003235C0` passes `set = 1` (`0055DA60`) and `flags = 0` (`003235CA`/`003235D5`).
- The definition initialiser `0023AC80` (`0023AE6E`–`0023AE7C`) and the SetSaveData apply `00239960` (`00239D47`–`00239D55`) both pass `set = 1` and `flags = 1`. Those start-owned grants still go through this check.

**The rule, in order** (the first matching line returns):

```
if (record == NULL)                         return 6;   // 00323D2C-00323D43 (lea eax,[rcx+6] with rcx = 0)
if (!BattleEncodedId_IsValidForClass(0x19, node))  return 7;   // 00323D44-00323D6A
        // class 25 = node table 02EBF038; valid iff 0 <= node < [02EBF038]+4 (00322FCB-00322FDC, 0032302C-00323041);
        // the r8d = 1 that 00323D49 passes is not read by the validator (00322C50 never reads incoming r8)
if (record.b[0x194 + node/8] & (1 << node%8)) return 1;  // already owned: 00323D6B-00323DAB
row = res(02EBF038.+0xC) + node * 02EBF038.w[+8];        // 00323DAC-00323DE9 (NULL -> 0 at 00323DED)
switch (row.b[+6]) {                                      // square kind: 00323DF0-00323E09
 case 0:  // ordinary
   if (row.b[+5] == 0x1E)                                 // 00323E88-00323E8C
       return QueryMode0Positive(0xC01F) ? 0 : 8;         // 00323E8E-00323EA3
   return 0;                                              // 00323EA5
 case 1:  return AnyPartyRecordOwnsNode(node) ? 3 : 0;    // 00323E78-00323E86 (neg/sbb/and 3)
 case 2:  return CountLicenseBits00To17(record) >= 3 ? 4 : 0;  // 00323E61-00323E76 (cmovge)
 case 3:  if (AnyPartyRecordOwnsNode(node)) return 3;     // 00323E2C-00323E3C
          if ((unsigned)(node - 0x12) > 0xC) return 5;    // 00323E3E-00323E44, 00323E5A
          return QueryMode0Positive((u16)(node - 0x4000)) ? 0 : 5;   // = 0xC000+node; 00323E46-00323E5F
 default: // kind >= 4
   if (esi && row.b[+4] > record.d[+0x190]) return 2;     // 00323E0B-00323E20 (unsigned jbe)
   return 9;                                              // 00323E25
}
```

**The callees, one level down.**

- `BattleEncodedId_IsValidForClass` `00322C50`. The class-25 arm reads the count dword `+4` of descriptor `02EBF038` (`00322FCB`–`00322FDC`) and admits `[0, count)` (`0032302E`–`00323041`).
- `0020E600` turns the descriptor's 32-bit `+0xC` handle into the row base. It is called twice, the same pattern as in the setter (`00323DBF`–`00323DD6`).
- `AnyPartyRecordOwnsNode` `00324280` (107 B). It loops over records `i = 0..6` (`cmp r8b, 7 / jb` at `003242DC`) of `[02EBF190] + 8 + i × 0x1C8` (`003242A7`–`003242B6`). It skips a record unless `byte[+0]` has bit 3 (`003242BB`). It returns 1 on the first record whose `+0x194` bitmap holds `node` (`003242C0`–`003242D7`, `003242E5`), otherwise 0 (`003242E2`). Notes:
  - The `cmp r8b, 0x27 / ja` at `003242A1` can never fire.
  - The caller's own record is included, but for that record the own-bit test at `00323D92` has already returned 1.
- `BattleStats_CountLicenseBits00To17` `00324020` (218 B). It runs 3 iterations × 6 bit tests over `+0x194` with a rotating mask (`00324040`–`003240E6`). It returns the number of bits 0–17 set in **this record only**.
- `BattleEncodedId_QueryMode0Positive` `0030B0E0` (146 B):
  - Id `0xFFFF` gives 0 (`0030B0E6`–`0030B0FE`), and a nibble above `0xE` gives 0 (`0030B106`–`0030B11A`).
  - Otherwise it takes record `01EEBCC0 + (id >> 12) × 0x58` (`0030B11C`–`0030B133`).
  - It requires `(id & 0xFFF) ≤ [+0x3C] − 1` (`0030B136`–`0030B143`) and a non-null `[+0x50]` handler (`0030B145`–`0030B14C`).
  - It returns `handler(id, 0) > 0` (`0030B14E`–`0030B15B`).
  - For nibble `0xC` (class 17) the image holds count `0x20` and handler `002FD970`, so `0xC000`–`0xC01F` are all in range. Mode 0 of `002FD970` tests bit `index & 0xF` of word `index >> 4` in the region-A bitset at descriptor `+8` (`002FDA2F`–`002FDA57`). [The encoded-id page](../../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.9 places quickenings at `0xC000`–`0xC011` and the Esper range at `0xC012`–`0xC01E`. `0xC01F` is the 32nd and last bit of that class. Its only immediate in the code is `00323E8E` (whole-image `retool grep 0xc01f`, one hit).

**Data read.**

| what | where | read at |
|---|---|---|
| owned bitmap | record `+0x194 + node/8`, bit `node % 8` | `00323D85` |
| LP pool (`u32`, compared unsigned) | record `+0x190` | `00323E13` |
| node table descriptor | `02EBF038`: count `+4`, stride `u16 +8`, row handle `+0xC` | `00322FD9`, `00323DE2`, `00323DBF` |
| node row: LP cost | `u8 +4` | `00323E0F` |
| node row: category | `u8 +5` | `00323E88` |
| node row: square kind | `u8 +6` | `00323DF0` |
| party records | `[02EBF190] + 8 + i × 0x1C8`, `i < 7`; byte `+0` bit 3 and `+0x194` | `003242A7`–`003242C3` |
| class-17 presence bits | `01EEBCC0 + 0xC × 0x58`: count `+0x3C`, handler `+0x50`; region A `+8` | `0030B13C`, `0030B145`, `002FDA2F` |

**What the shipped table makes reachable.** `02EBF038` has exactly one binder: `00236C30` at `00236D55`–`00236D67`. That binder calls `003845F0` on the STATIC blob's directory dword `+0x34`, and a whole-image `refs` shows no other write or `lea`. That section of `battle_pack.bin` is an `st2e` table of **361 × 24 bytes** in each of the `in`, `ch`, `us`, `kr` and `cn` copies. Over its rows:

- **Kind byte `+6`:** `0` on 330 rows (nodes 31–360), `2` on nodes **0–17** (category `0x13`, no granted ids) and `3` on nodes **18–30** (category `0x14`, granting actions `0x106`–`0x112`). No row has kind 1 or a kind of 4 or above.
- **Category `0x1E`:** one row only, **node 360**: `LP 30, kind 0, start mask 0, ids {0x0080}` (row bytes `6819 8442 1e 1e 00 00 8000 ffff…`).

So on shipped data:

- Quickening squares (0–17) are refused with **4** once the character holds three of them. The check counts only the character's own bits. It does not look at other party members.
- Esper squares (18–30) are refused with **3** if any of the seven party records with `byte[+0]` bit 3 owns that node. Otherwise they are refused with **5** until bit `0xC000 + node` (`0xC012`–`0xC01E`) is set.
- Node 360 is refused with **8** until bit `0xC01F` is set.
- Every other unowned ordinary square returns **0**.
- The kind-1 arm (`00323E78`), reason **2** and reason **9** (`00323E0B`–`00323E25`) are unreachable.

**Not tested here.**

- **Adjacency.** There is no neighbour or grid read in the body. Adjacency belongs to the menu's `0055E090`/`0055E3F0` passes.
- **LP sufficiency for any shipped square.** The LP compare lives only in the kind-4+ arm. The menu grant passes `flags = 0`, gets 0 back for any eligible kind-0/2/3 square, and the setter then deducts `row.b[+4]` from `+0x190` floored at 0 and capped at 99,999 (`003239C3`–`003239E1`: `jns`, `mov edx, ebx`, `cmovg` against `0x1869F`). Affordability is the sweep's bit 14 (`0055C492`, per the UI page), which this read did not re-derive.
