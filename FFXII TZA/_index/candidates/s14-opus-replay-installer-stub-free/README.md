# S-14: the definition installer executed end to end with its real reset and rekey (OPUS, 2026-09-25, block 333)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-14's binding gap reads *"the reset is a stub"*.
EXP-150 ran the installer `0023A570` with scripted callees, and SECTION-01 ran the reset with its cleanup callback
bridged. This harness runs `0023A570` with **no application stub and no stop boundary**:
- the reset `00236A60`;
- the rekey `00322050` / `003220E0`;
- the party install;
- the pulse reset `002FEAB0`.

It runs over the shipped `battle_pack` tables.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 332. `shipped_pack.py`
binds the tables by shipped code; the heap-6 binders are skipped.

**Fixtures:**
- four idle objects;
- the unit pool `[0208E688]` / `[0208E6A0]`;
- the unit's `+0x10` handle object, a zeroed block. The rekey resolves through `q[unit+0x10]`, and its generation bump
  `002659D0` has no null guard (EXP-151).
- the unit's flag qword;
- the master flag `d[02089300]`.

**5 / 5 pass, and `result.json` is byte-identical over three runs** (md5 `5ef9a185e69beb020572ef7b595d2682`).

| case | contract item | observed |
|---|---|---|
| `I4_I8_party_install` | I4, I8, §2 | For ids `0x0000`, `0x0003` and `0x0005` the installer returns 1. `+0x698` = `q[02EBF190] + 8 + row·0x1C8` (the shipped party rows), `+0x6A0` = 0, and flag bit 2 is set. The reset runs once. **The pulse reset `002FEAB0` zeroes exactly the qword at `+0xEAC`**; `+0xEB4` survives |
| `I2_reset_then_master_reject` | I2 | With master flag 0, the reset runs and masks the flags `…FFEB` → **`FFEF7FB9FFE7B0E1`**, and nulls `+0x698`. The installer then returns 0. `+0xEAC` survives, because only the success path's pulse reset clears it |
| `I1_other_class_clears_bit26` | I1, I3 | Class 2 (id `0x0203`): the rekey runs (the class byte is nonzero). Then the dispatch **clears bit 26** (`…FFE7B0E1` → `…FBE7B0E1`) and returns 0. **Bit 42 stays set.** Class 2 can rekey and then fail |
| `I3_rekey_selection` | I3 | With class byte 0 there is no rekey for a fresh unit, and none when the saved old id equals the incoming one. A different saved old id rekeys. Teardown `0xFFFF` with an old id rekeys and returns 0 |
| `I7_party_path_registers_nothing` | I7 | A party install makes **no** `00328FF0` call and leaves the tracked table `02EC1380` untouched |

## What the execution adds

1. **The reset runs real, answering the gap.** The installer's party path, the reset, the rekey and the pulse reset
   execute end to end with no stub.
2. **I2's measured mask needs no bridge.** SECTION-01's `FFEF7FB9FFE7B0E1` was measured with the cleanup callback
   bridged. Here the same value comes from the shipped reset with that path legitimately off: flag bit 4, tested at
   `00236A6F`, gates the cleanup call `003105D0`. The reset also nulls `+0x698`.
3. **I1's "not bit 42" is confirmed on a unit whose bit 42 was set.** EXP-150's case began with bit 42 clear (§13).
4. **I7's registration is not on the party path.**

## Not covered

- the enemy path (class 1). Its tables `02EBF120` / `02EBF150` are not in `battle_pack`, so I5, I6 and I7's write are
  not reached;
- the reset's cleanup callback `003105D0` (flag bit 4; EXP-161 executed it separately);
- a live game.
