# Meaning check — the encoded-id query ABI, `handler(id, mode)` (FABLE, Claude Opus 5.5, 2026-09-26)

Answers `FRONTIER-REQ-FABLE-QUERY-ABI-MEANING-CHECK`: does the corrected ABI mean what its producers think it means?
The shape (table `01EEBCC0`, `handler(id, 0)`) is accepted in
[`s05-fable-semantic-review-dispatch-abi.md`](s05-fable-semantic-review-dispatch-abi.md). This record checks the
**semantics**, read independently from the handler bodies, and names the regression that discriminates them.

## 1. What mode 0 and mode 1 return, per handler (NATIVE/STATIC)

| handler | mode 0 (`00309EC0`) | mode 1 (`0030AE30`, `mov edx, 1` at `0030AE8A`) | other modes |
|---|---|---|---|
| packed count `002FD8D0` (rows 0–2) | `(w & 0x3FF) − (w >> 10)` = **free = total − reserved**, **signed; negative when reserved > total** (`002FD942`–`002FD95F`) | `w & 0x3FF` = **total** (`002FD92B`) | 2: `w >> 10` reserved (`002FD917`); 3: the region-B byte (`002FD906`) |
| bitset `002FD970` (rows 3, 4, 6, 8, 12) | the id's **owned bit**, 0/1 (`002FDA2F`) | **the same bit**: modes 0 and 1 share the arm | 2: 0; 3: region-B bit (`002FD9F2`); 4: region-C bit (`002FD9B4`) |
| rows 5, 7, 9–11, 13, 14 (no handler) | **0** (`00309F18` null test → `00309F23`) | 0 | — |

Here `w` is the id's 16-bit word in the class's region A. This agrees with `FY-1` (channels 0/1/2/3 = free / total /
reserved / region-B byte). The dispatcher itself returns **−1** for id `0xFFFF` and for a class nibble above `0xE`,
and **0** past the class's count.

## 2. Two truthiness conventions over the same value — the semantic hazard

- **`0030B0E0` `BattleEncodedId_QueryMode0Positive`** returns `value > 0` (`setg` at `0030B0FB`). The sentinel −1, a
  negative free count and 0 are all **false**.
- **A caller that booleanizes `00309EC0` itself** with `test eax, eax / setne`, such as `002543F0`
  (`0025442B`–`0025442D`), treats −1 and a negative free count as **true**. `002543F0` filters `0xFFFF` before the
  call (`0025441D`), but not nibble-`F` ids or over-reserved stock.
- **Meaning:** "mode 0 ≠ 0" answers *"is there any free-or-negative balance, or an owned bit, or a sentinel"*, not
  *"does the player have one to use"*. Only the `> 0` sibling means "at least one available". A reimplementation that
  uses one convention for both reads the same over-reserved item, or sentinel id, oppositely at different call sites.

## 3. Regression that discriminates the meaning (existing, executed)

`_experiments/evidence/continuation-section05-encoded-query/native_controls.c`, results
`results/native_baseline.json` and `native_repeat.json`. These run the shipped dispatchers and handlers:
- `packed_query_mode0` (word = 19 + 3·1024) → **16**;
- `packed_query_mode1` → **19**;
- `packed_available_can_be_negative` (3 + 7·1024) → **−4**;
- `bitset_mode0` = `bitset_mode1` → **1**;
- `query_absent_handler_returns_zero` → **0**.

All pass. A reading of mode 0 as "total", or as a boolean, fails the first and third. OPUS's
`s05-opus-dispatch-abi-controls/check.py` proves the ABI only and is not a meaning control.

## 4. Consumers

| consumer | state |
|---|---|
| `CONTRACT-encoded-id-space-and-class-registry.md` `00309EC0` paragraph (`handler(id, 0)`) | agrees (shape); it states no return meaning |
| `the-encoded-id-space-and-the-query-record.md` §2.2 "What each channel means per class is not read here (FY-1)" | stale pointer: FY-1 is answered. **Carrier** → routed-to-FABLE-NOTICE-FRONTIER-QUERY-RECORD-FY1-POINTER |
| `Shared-State-Accessors/cross-subsystem-accessor-hubs.md` ~767 "`00309EC0(ecx, 0)` then returns the boolean" | revised-here: the dispatcher returns the signed mode-0 value and the caller booleanizes it with `setne` |
| `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` ~310 "mode-0 ≠ 0" | agrees |
| `16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md` ~276/284 "booleanized sibling" | agrees; §2 above adds that the sibling is `> 0`, not `≠ 0` |
| `05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md` ~527 "`00309EC0(r9w)` >= 1" | agrees; it is the `> 0` reading |

**Status: PENDING PROPAGATION** for the one carrier consumer.
