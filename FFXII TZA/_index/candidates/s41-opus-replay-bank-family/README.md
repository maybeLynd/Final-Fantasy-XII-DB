# S-41: the audio bank family executed for the first time — the broadcast, the slot-10 command mask per class, the id band (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** `CONTRACT-audio-bank-and-controller-family` had **no execution record**. AC-1/2/3/5 are vtable-layout facts,
which is static structure.

## What was run

`check.py` runs over block 355's world, plus two real initialiser steps (as in `../s41-opus-replay-spatial-sources`): the
audio object's own initialiser `00210AF0`, and `007AD620(00210EC0, 00210EB0)` with the library init's own arguments.

**Planted data (disclosed):**
- bank objects: a real bank vtable at `+0`, the circular list sentinel at `+0x08`, and list nodes `{+0 next, +0x10
  payload}`;
- on the audio object: readiness dword `+0x38` = 1, and the command dword `+0x3C`;
- the game-mode byte `02064AD3` = 5. The readiness check `00210930` needs `+0x38 ≠ 0`, and `002287A0` needs mode 5 or 6;
- Seb's own bank `+0x38`, and Sep's bank id `+0x38`, `+0x50` and `+0x49`.

**One disclosed perturbation, for the AC-4 control only.** During the first slot-9 call, the bank's vtable pointer is
switched to Seb's real vtable. **No application stub.**

**10 / 10 pass, and `result.json` is byte-identical over two runs** (md5 `54792e746cd67d5fa87358e8496a3325`).

| case | item | observed |
|---|---|---|
| `AC4_slot9_once_per_entry_in_list_order_with_the_payload` | AC-4 | `00222550` over a three-node list calls the real slot 9 (`00222340`) once per node, in list order, passing each node's payload |
| `AC4_control_vtable_reloaded_every_entry` | AC-4 | with the vtable switched after the first entry, **entries 2 and 3 go to Seb's slot 9 (`00223F40`)**. The vtable is re-loaded on every entry (`00222580`) |
| `AC6_each_class_dispatches_its_own_subset_of_bits` | AC-6 | see the table below |
| `AC6_only_non_returning_rows_…` | — | Seb's direct callees for bits 8 and `0x10` fault on the planted all-zero payload, **after** the dispatch observed. No other row fails |
| `AC6_bit2_is_a_tail_jump_that_ends_slot10_in_Seb_and_Sep` | AC-6 | with all bits set (`0x3F`), Seb and Sep take only slot 9: bit 2 is a tail jump |
| `AC6_seb_also_gates_on_its_own_plus38` | AC-6 | with Seb's own `+0x38` clear, nothing is dispatched |
| `AC6_AudioBank_slot10_is_purecall` | AC-6 | `AudioBank`'s slot 10 reaches the `_purecall` import: the base class's slot 10 is abstract |
| `AC6_contract_reading_every_bank_maps_every_bit_is_contradicted` | AC-6 | see below |
| `AC7_sep_slot3_skips_the_band_150000_to_150999_only` | AC-7 | Sep's slot 3 (`sub eax, 0x249F0` / `cmp eax, 0x3E8` / `jb → ret`) reaches slot 0 for ids **149999, 151000 and 152000**, and not for **150000 or 150999** |

**What slot 10 dispatches, per class**, read from the bytes and executed:

| class | bit `1` | bit `2` | bit `4` | bit `8` | bit `0x10` | bit `0x20` |
|---|---|---|---|---|---|---|
| `MusicAudioBank` (`00222C70`) | **slot 0** | — | — | — | — | — |
| `SebAudioBank` (`00224B30`, also gated on its own `+0x38`) | — | slot 9 | — | direct `00224290` | direct `002240B0` | direct `00224470` |
| `SepAudioBank` (`00223540`) | — | slot 9 | — | slot 3 | slot 4 | slot 5 |
| `ShoutAudioBank`, `StreamAudioBank` (`00225440`) | — | — | **slot 9** | — | — | — |
| `AudioBank` | `_purecall`: slot 10 is abstract | | | | | |

## Corrections for the contract (FABLE's; routed)

- **AC-6.** The contract says *"every concrete bank reads the manager's `+0x3C` and re-dispatches a different slot per bit —
  `&1` → slot 0, `&2` and `&4` → slot 9, `&8` → slot 3, …"*, carried from the page and not re-derived.
  - **Each class handles its own subset.** Only the union across classes matches the list.
  - Seb's bits 8, `0x10` and `0x20` are **direct calls**, not its vtable slots 3/4/5.
  - `AudioBank`'s slot 10 is `_purecall`.
- **AC-7.** Sep's slot-3 gate skips **the 1000-id band 150000–150999**. The split at 150999/151000 is that band's upper edge;
  ids below 150000 pass too.

## Not covered

- AC-7's Seb iterator copies (the reciprocal divide);
- the controllers' slots;
- a loaded bank, or a live game.
