# S-14: the installer's enemy path executed over shipped area files, with the real spawn initializer (OPUS, 2026-09-25, block 343)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
- **Block 333** ran the definition installer `0023A570`'s party path stub-free.
- **EXP-150** ran the enemy path over synthetic joins. The construction contract's I6 still reads *"The actual spawn-record
  initializer remains a scripted EXP-150 boundary."*

This harness runs the **enemy path (class 1)** over shipped area files, bound by the game's own binder `003EA710` (block
342). The spawn-record initializer `0023AC80` runs real. It tests
[`CONTRACT-battle-unit-construction.md`](../../../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md) I1,
I4, I5, I6, I7 and I8.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 342. **No application stub
and no stop boundary.**

Area files, from the shipped extract `ps2data/plan_master/in/plan_map/…`:

| file | sha256 | definitions | used for |
|---|---|---:|---|
| `rsn_b.ard` | `41ac8746…bcd992` | 22 | I1 / I4 / I5 / I6 / I8 |
| `bhm_c.ard` | `c778e09a…eeabbd` | 11 | I7; its codes are 0 **and** 1, while every rsn_b code is 0 |

Each file sits 0x1000 into its own zeroed mapping, as in block 342.

**Fixtures:**
- four idle objects;
- the unit, with flag bit 26 (placement), `+0x10` a zeroed handle object, `+0x40` a spawn index list `{1, 0}` and
  `+0x57` = 0;
- a zeroed spawn pool at `q[0208E690]` (stride 0x250, read by `00236100`);
- the master flag `d[02089300]` = 1.

**5 / 5 pass, and `result.json` is byte-identical over three runs** (md5 `e05ca81b1eeb1d7e1ed7fb9b185e9c70`).

| case | contract item | observed |
|---|---|---|
| `I1_I4_enemy_install_every_definition` | I1, I4, §3 | See the I1 / I4 list below |
| `I8_class1_float_from_byte_27` | I8 | Unit `+0x6C` = float(class row byte `+0x27`), which is 20.0 on this area. No ×1.5, which belongs to class 0's `+0x2B` path |
| `I5_row_bound_is_the_shipped_count` | I5 | A row index equal to the shipped count (22), or `0xFF`, returns 0 **and keeps bit 26**, with no spawn initialization. Row count − 1 installs |
| `I6_freshness_gate` | I6 | See the I6 table below |
| `I7_tracked_registration_needs_a_code` | I7 | See the I7 list below |

**I1 / I4.** Class 1 (ids `0x0100`–`0x0115`) installs every definition of rsn_b and returns 1. For each install:

| field | holds |
|---|---|
| `+0x698` | spawn + 0x80 (the spawn's embedded stats) |
| `+0x6A0` | the spawn |
| `+0xE60` | the definition row |
| `+0xE68` | the `[02EBF150]` row chosen by `def+0` |
| `+0xE70` | the `[02EBF148]` row chosen by `def+0x22` |
| `+0xE78` | the `[02EBF140]` row chosen by `def+0x24` |

Flag bits 2 and 26 are set. The reset and the **real** `0023AC80` run: 166 writes into the spawn record for definition 0.

**I6, the freshness gate:**

| `byte[spawn]` | spawn initializer | counter word | spawn `+0x12` | returns |
|---|---|---|---|---|
| 0 or 2 (`& 5 == 0`) | runs | one write at `0023A838` (`0208D354`) | takes the old count | 1 |
| bit 0 or bit 2 set | does not run | none | keeps `0xAB` | 1 |

**I7, on bhm_c.** `00328FF0(0, def+3 & 3, unit+0xEA9)` behaves as follows:
- For the four code-1 definitions, it writes the tracked table `02EC1380` row 0 = `{slot 0, code 1}`.
- For the seven code-0 definitions, it writes nothing.

## What the execution adds

1. **I6's scripted boundary is gone.** The spawn-record initializer `0023AC80` runs real on every fresh install, and the
   freshness gate is measured on both sides: the initializer and the counter together.
2. **A class-1 bound rejection keeps bit 26.**
   - The failures at `0023A662` (and the other guards) jump to `0023A63A`, which is past the `and qword[unit], ~bit26` at
     `0023A633`.
   - Only a class above 1 takes that clear (I1). So "return 0" does not always mean "bit 26 cleared".
3. **Unit `+0xE70` / `+0xE78` are the ARD base and per-level rows.**
   - They are the `[02EBF148]` row by `def+0x22` and the `[02EBF140]` row by `def+0x24`.
   - Those are the same two rows block 342's stat derivation reads for the foe main value
     (`base+0x20 + perLevel+0x20 × span`).
   - S-32's defeat-rewards contract (DR-4) calls them the FLAT-TERM and MULTIPLIER tables, and reads gil at `+0x30` and
     experience at `+0x34`. **The reward terms and the stat terms are adjacent fields of the same two authored rows.**
     Field meanings beyond the offsets are not claimed.
4. **I5 holds on shipped data.** Every definition of both areas passes the `+0` / `+0x22` / `+0x24` / `+0x50` guards
   against the shipped counts.

Routed to FABLE (I6's boundary sentence, I5's bit-26 note, the `+0xE70` / `+0xE78` identity).

## Not covered

- I2 and I3 on the enemy path (block 333 measured them on the party path);
- the `+0x50` order join's zero-count rejection (no shipped area has a zero count);
- the units the zone script actually places (the spawn list is a fixture);
- a live game.

## I2 and I3 on the enemy path, executed (OPUS, 2026-09-26)

`i2i3_enemy.py` runs over this harness (imported unchanged; its cases run first). It drives the installer `0023A570` with
class byte 1 over the shipped `rsn_b.ard`, every callee real. A code hook on the rekey `00322050` is added, and the
translation cache is flushed.

| case | asserted |
|---|---|
| I2 | master flag `d[02089300]` = 0: the reset `00236A60` runs once and the installer returns 0. All-ones flags (bits 2 and 4 clear, as block 333's party case) come out as **`0xFFEF7FB9FFE7B0E1`**, the conjunction the contract states. `+0xEAC` survives. No rekey, no spawn initializer |
| I3, control | class 1: reset, then the rekey (a nonzero class byte), then the real spawn initializer `0023AC80`; returns 1 |
| I3, zero after rekey | with the unit's `+0x40` spawn index list at count 0: reset, then the rekey, then the installer **returns 0**. A zero return follows an identity change on the enemy path |

Whether that zero-count list is the contract's "`+0x50` join" rejection is not claimed.

**Runs.** 3/3, and two runs give an identical `i2i3_enemy_result.json` (md5 `97e77efc2c32f672ac9bc1f5bbe1e847`).

## I5's `+0x50` order join executed (OPUS, 2026-09-26, `i5_join.py`)

`i5_join.py` imports `check.py`, whose cases run first and unchanged (`result.json` keeps md5 `e05ca81b…`). It drives the
installer `0023A570` on the enemy path through the join guard at `0023A70B`–`0023A726`:
- the count is `word [[02EBF168]]`, or 0 when the slot is null;
- the index is `movzx word [def + 0x50]`;
- the test is `dec ecx; cmp; jg 0023A63A`.

Hooks record which successor runs: `0023A72C` (passed) or `0023A63A` (rejected). **No application stub.** **4 / 4
pass; `i5_join_result.json` is byte-identical over two runs (md5 `65b600b4…`).**

| case | observed |
|---|---|
| `J0_shipped_table_passes` | shipped table (count 15), definition 0 (`+0x50` = 0): passes and installs (returns 1) |
| `J1_missing_count_rejects` | slot `02EBF168` null: **rejected at the guard**, returns 0, no spawn initialisation |
| `J2_zero_count_rejects` | a table whose count word is 0: **rejected**, so the signed compare against −1 refuses index 0 too |
| `J3_bound_is_count_minus_one` | definition 10 (`+0x50` = 14, the largest in the live table): a count of 14 rejects and a count of 15 passes |

*The live definitions' `+0x50` indices run 0..14 against the shipped count 15; the authored data reaches exactly the
bound. The definitions are the ones bound when the file runs: block 343's later cases rebind `[02EBF120]` to the area
file's table (11 definitions), so the live table is read rather than `check.DEFS`.*
