# GR-8 answered: the per-unit 64-byte record uses only its first 32 bytes; +0x20..+0x3F is never touched (OPUS, 2026-09-30)

Register row GR-8 asks what the unmapped fields of the per-unit 64-byte record hold. The record is `0208D480 + kind × 0x40`
for a party record and `0208DE80 + unit[+0xEA9] × 0x40` otherwise. The row asks two things: what the second half
(`+0x20`..`+0x3F`) holds, and who reads the rest of the first half. Pages: [combos and the guard/parry flag](../../../08-Combat-Formula/combos-and-the-guard-parry-flag.md)
(Limits), [the formula scratch block](../../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.5, and
[the battle-unit field map](../../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md).

Method: static, from the certified image. The checker is `gr8_record_census_check.py` (output `gr8_record_census_check.out`,
**`FAILS 0`**). It uses the kit's `retool.py` and `structflow.py`. Work by SWE2-STRUCT for OPUS.

## The answer (OPUS)

**In player terms:** each fighter carries a small per-battle memo. It holds the damage stashed for the gil-toss, walk
and HP-bank technicks, which targets the current action cannot hit or cannot affect, which targets the fighter has
marked, the random-magick draw for Shades of Black, the combo count, the regen tick counter, the walking-MP carry and
a movement flag. The back half of the memo is empty space that nothing uses.

- **The second half, `+0x20`..`+0x3F`, is never accessed.** No instruction in the image reads it, writes it or copies it.
  The record is 32 bytes of data in a 64-byte stride. The `shl 6` indexing sets the stride; the data does not need it.
  `BattleRuntime_ResetPersistentStatePrefix` (`00386C10`) clears exactly the bytes that exist, `+0x00`..`+0x1F`, with
  four qword stores (`00386C5B`–`00386C66`).
- **Every field of the first half has a reader, except three padding bytes.** `+0x13`, `+0x16` and `+0x17` are written
  only by the wide clears and are never read.
- **The census.** 57 accesses, all inside the 17 functions that form the address. No record pointer is passed to a
  callee, returned for use, stored to memory, copied or bulk-cleared.

### Per-offset table

`w` = write, `r` = read, `rw` = read-modify-write. Every site is in the checker's census listing.

| offset | width | writers | readers | meaning (where the code makes it clear) |
|---|---|---|---|---|
| `+0x00` | u32 (the clears are qword) | `00385680` clear `003857AB`; `00386C10` `00386C5B`; slot 18 `00388D50` `00388E51`; slot 122 `0038DA00` `0038DA5D`; slot 146 `0038EBE0` `0038ECD5`, `0038ECFF` | `00388D50` `00388E60`; `0038DA00` `0038DA68`; `0038EBE0` `0038ED17`; slot 147 `0038ED40` `0038EDD6` | **The recipe damage stash.** Each recipe parks a value here and deals it later. The gil throw parks its preview amount (`00388E51`) and pays it out divided by the target count (`0038EDD6`). The HP bank parks echo C (`0038DA5D`) and deals it (`0038DA68`). The walk parks its product (`0038ECD5` / `0038ECFF`) and re-deals it when no preview is stored (`0038ED17`). See [the count, clock and bank recipes](../../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md) §2.3, §2.4, §2.6. |
| `+0x04` | u32 | `00385680` `00385A7F` (`or`, bit = target index) | resolver `00385F60` `0038633F` (`bt`) | **Preview-failed targets.** A set bit makes the resolver store result kind 6, "miss / failed" (`00386347`). |
| `+0x08` | u32 | `00385680` clear `003857AE` (qword, `+0x08`..`+0x0F`); `00385AC0` (`or`); `00386C10` `00386C5E` | `00385F60` `003862FB` (`bt`) | **Immune-by-kind targets.** A set bit makes the resolver store result kind `0xA` (`00386303`). |
| `+0x0C` | u32 | `00387B00` `00387B97` (`or 1 << target index`), called from 15 formula-slot functions; cleared by `003857AE` and `00386C5E` | `002FA290` `002FA352` (`bt`) | **A per-source set of marked target units.** The bit index is the target's `+0xEA9` slot, or its stats byte `+4` when the target has no owner. The only reader is `002FA290`. The authored-event coordinator `003B8670` reaches it through `00322850` (`003B88B3` → `003228C2`) and ORs the answer into its object's `+0xC` (`003B88D1`). **Cleared at each action's preview**, so it lasts one action. What each of the 15 marking slots means by a mark is not claimed. |
| `+0x10` | u16 | `00387A50` `00387ADE` (the `0x9F` draw); cleared by `003857B2` (dword) and `00386C62`; **`003857E1` restores the value that `003857A3` saved** | `00385680` `003857A3`, `00385801`; `00385F60` `00385FF7`; `00387090` `0038710E` | **The cached random draw for action `0x9F` only.** The preview does not store the previewed id here: it saves the word, clears `+0x10`..`+0x13`, and writes the saved word back. |
| `+0x12` | u8 | `00385680` (`003857D1`–`003857DD`, `00385AD0`–`00385AF2`); `00385F60` `00386402`; `00388660` `0038885D`, `00388865` | `00385680` `0038579C`, `00385ACB`–`00385AE0`; `00385F60` `003860DF`/`EF`/`FD`; `00388660` `0038886B`; `00389C60` `00389D24`; `0038DA00` `0038DA49`; `0038EBE0` `0038EC3A` | Already mapped (scratch block §2.5): bit 0 = preview stored, bits 1–3 = flag word B, bits 4–7 = combo count. The high nibble survives the preview's clear only while unit `+0x6B7` is non-zero (`003857C6`–`003857D9`). |
| `+0x13` | u8 | only the clears `003857B2` and `00386C62` | none | padding |
| `+0x14` | u16 | `00386860` `003869E0`, `00386A27` (`inc`), `00386A2C` | `00386860` `003869A2` | **The periodic HP-credit tick counter** (`BattleFormula_BuildRuntimeCounterPeriodicHpCredit`, [CONTRACT-periodic-tick](../../../10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md)). The function takes `+0x14` directly: `lea 0208D494` / `0208DE94` (`00386885`, `003868AD`). |
| `+0x16` | u16 | only the clear `00386C62` | none | padding |
| `+0x18` | f32 | `002F9400` `002F95A6`; clear `00386C66` | `002F9400` `002F9474` | **The walking-MP carry.** It is compared with the drained accumulator (`00320450`, `002F9419`), then set to the value handed back (`00329A20`, `002F95AE`). See [where MP comes from](../../../10-Status-Periodic-Terminal/where-mp-comes-from.md). |
| `+0x1C` | u32 | `0033CB10` `0033CB60` (`or 1`); `0033D890` `0033DA73` (`or 2`); clear `00386C66` | `0033D890` `0033D953` (`test 1`), `0033DA77` (`test 2`) | Movement flags. Bit 0 is set by the per-category setter and gates the kind-2 solver. Bit 1 latches when the `008C5F6C` heading limit binds. Both clear only at activation (`00386C10`). |
| `+0x20`..`+0x3F` | — | **none** | **none** | **Unused.** Nothing accesses it. |

### How the record is found, and what can reach it

| step | what it shows |
|---|---|
| **S1** | Every rip reference into the banks is a `lea`: 34 of them in 17 functions (`0208D480` ×16, `0208DE80` ×16, `0208D494` / `0208DE94` ×1). The second bank holds 32 records (slot 0..31), so the banks span `0208D480`..`0208E67F`, not `..0208E47F`. |
| **S2** | This check does not depend on retool's function extents. A raw byte scan of `.text` for displacements that land in the banks decodes to the same 34 `lea`s. No aligned dword or qword in any section holds a bank address, as a VA or an RVA. No instruction carries one as an absolute displacement or an immediate. |
| **S3 / S3b** | Neighbouring arrays cannot reach in. The anchors just below the banks (`0208D320`..`0208D354`) are bounded and end by `0208D454`. The anchors above (`0208E680`, `0208E6E0`, `0208E6E4`) index upward only. The only memsets based below the banks (`02064E30`, `0x200` and `0x4000` bytes) end at `02068E30`. |
| **S4** | `structflow` runs from the 17 functions (stride `0x40`, depth 3, returns followed) and finds 57 accesses. There are no unknown offsets, escapes, copies, indirect calls, stack arguments or hand-offs. |
| **S5** | No call or tail jump in the 36 walked functions receives a record pointer in `rcx` / `rdx` / `r8` / `r9`, including callees outside the extent list. No `rep stos` / `movs` runs on a record pointer. |
| **S6** | The extents of the 17 functions are whole: each ends in `ret` / `jmp` before padding or the next function. |
| **S7** | The accessed bytes are exactly `+0x00`..`+0x1F`. Nothing touches `+0x20`..`+0x3F`. |
| **S8** | Positive controls: the four qword clears in `00386C10`; `+0x10` at `00387ADE`, `0038710E` and `00385FF7`; `+0x12` at `003857DD` and `0038886B`; `+0x1C` at `0033CB60` and `0033DA73`. |
| **S9** | The result is stable at depth 5, and at depth 3 without following returns. |
| **S10** | The instruction texts the readings rest on. |

At 11 `ret` sites, `rax` still holds a base or element pointer (a leftover register, not a documented return): `00387B00`, `00386C10`, `0033CB10`,
`00386860`, `00233AD0`, and six callers of `00387B00`. No caller dereferences it: no access occurs outside the 17 functions.

## Limits (OPUS)

- **Static only.** Nothing was executed. The register's runtime plan, a write watch on one party record's 64 bytes
  across a battle, would confirm `+0x20`..`+0x3F` stays zero. It is not needed for "no code accesses it", which S1–S5
  show. Zero is the BSS initial value.
- `structflow` does not follow taint through non-stack memory. It records escapes instead, and there are none. It does
  not resolve indirect call targets; no indirect call receives a record pointer.
- **`+0x0C`:** the mark itself is read. Its game meaning depends on the 15 marking slots (`00387F70`, `00388250`, …,
  `00390240`), which were not each read. The event coordinator's use of the answer (`003B8670` object `+0xC`) is not
  interpreted.
- The preview clear (`003857AB`–`003857B2`) runs only when the previewed target is the source's current target
  (`00385792 cmp rax, rsi`). "Once per action" rests on that compare. How often it runs was not measured.

## Contradictions and consumers (OPUS, routed, not edited here)

- **[The formula scratch block](../../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.5 is contradicted
  in three places.**
  - *`+0x10` "the previewed action id (`003857E1`)" is wrong.* `003857E1` writes back the word `003857A3` saved before
    the clear. The previewed id goes to `02AEDFD4` (`003857EC`). Only the `0x9F` draw (`00387ADE`) stores an id in
    `+0x10`.
  - *The reader column is incomplete.* It says "—" for `+0x00` (read by `00388E60`, `0038DA68`, `0038ED17`,
    `0038EDD6`), for `+0x04` (`0038633F` → kind 6) and for `+0x08` (`003862FB` → kind `0xA`).
  - *Rows are missing* for `+0x0C`, `+0x14`, `+0x18` and `+0x1C`, and the table does not say that `+0x20`..`+0x3F` is unused.
- **The register row `GR-8`** and the combos page Limits both call `+0x00` "u64". Every non-clear access is a dword; the
  u64 is the preview's clear. The row also calls `+0x10` "the previewed / drawn action id"; only the drawn id is stored.
  The row can be marked ANSWERED from this record.
- **[The battle-unit field map](../../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)**, row `0033D890`, says
  the solver "requires the category record's `+0x1C` bit 1 (the bit `0033CB10` sets)". `0033CB10` sets value 1, which
  is bit 0 (`0033CB60`), and the solver tests `1` (`0033D953`). Bit 1 (value 2) is the solver's own latch (`0033DA73`).
  The `0033CB10` row calls `+0xEA9` "the perception category". The same page's `+0xEA9` row calls it the slot index,
  and CS-6 agrees.
- **`_types/fields.tsv` `BattleRuntimeUnitRecord` agrees** with this census. `unobservedSpan020` (confidence UNKNOWN)
  can cite this record as a whole-image negative. `unitBitset00C` can take the per-action lifetime and the
  `003B8670` reader. No edit is made here.

## Kit change (OPUS)

`Tools/analysis-kit/gfz-scripts/structflow.py` gains a backwards-compatible `seed_leas` parameter:

- `seed_leas={(func, address)}` tags `lea r64, [rip -> address]` inside `func` as the array base B.
- `seed_leas={(func, address): k}` tags it as `("B", k)`, a base that points at field `k` of element 0. This handles
  the `0208D494` = base + `0x14` anchors in `00386860`. Accesses and derived element pointers are shifted by `k`.
- A helper `bk(t)` replaces the literal `t == "B"` tests. It returns 0 for `"B"`, so every existing result is unchanged.
- A `seeded` set records the seed sites.

Re-run after the change, all byte-identical to their committed `.out`, each ending in `FAILS 0`:

- `gr1-wait-slot-settled-0930/gr1_settled_check.py`
- `gr4-gr5-action-row-readers-0930/gr4_gr5_row_readers_check.py`
- `gr6-action-row-24-0930/gr6_row24_check.py`, the other structflow user
