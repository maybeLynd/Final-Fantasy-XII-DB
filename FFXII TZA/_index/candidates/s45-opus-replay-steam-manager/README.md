# S-45: the Steam integration's I-2, I-3 and I-4 with the achievement manager built by its own builder (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn) against a disclosed model of the Steam library, `live_game: false`.**

**The gap.** AUDIT-SEM, on `AUDITSEM-REQ-OPUS-412`: *"I-2/I-3/I-4 need the manager built, whose construction binds the
`SteamInternal_ContextInit` import — replay-reachable via an import bridge but unbuilt today"*.

## What was run

`check.py` runs over block 332's world (`../s21-opus-replay-applier-stub-free/check.py`, whose cases run first; `result.json`
keeps md5 `baf273ee…`). The image-backed block is bound by `00253970`'s own prefix, as in `../s45-opus-replay-counters`.
**No application stub.** The manager is built by **`0020CD30`**: `operator new(0x80)`, then the constructor `0020C730` with
the image's 41-entry table.

**The Steam library is modelled, and disclosed.** `steam_api64.dll` is external to the image.
- `SteamAPI_RegisterCallback` records its `(object, id)` and returns.
- `SteamInternal_ContextInit` returns a context whose `+0x08` / `+0x18` / `+0x28` hold three interface objects.
- Their methods sit on a `ret` page. Each is hooked with the library's semantics, and every call is recorded:

| interface | slot | method | model |
|---|---|---|---|
| `ISteamUser` | `+0x08` | `BLoggedOn` | returns 1 |
| `ISteamUtils` | `+0x48` | `GetAppID` | returns 595520 (`0x91640`) |
| `ISteamUserStats` | `+0x00` | `RequestCurrentStats` | returns 1 |
| | `+0x30` | `GetAchievement(name, bool *)` | writes the model's state |
| | `+0x38` | `SetAchievement(name)` | sets the model's state |
| | `+0x50` | `StoreStats` | returns 1 |
| | `+0x60` | `GetAchievementDisplayAttribute(name, key)` | returns a fixed model string |

**Receipts are delivered by calling the game's own handlers** with a callback struct `{u64 game id, u32 result}`: 1101 is
`0020C940`, and 1103 is `0020C8C0`.

**7 / 7 pass; `result.json` is byte-identical over two runs (md5 `c9a8f718…`).**

| case | contract item | observed |
|---|---|---|
| `M0_manager_built_registers_1101_1102_1103_reads_appid_requests_stats` | construction | callbacks **1101, 1102 and 1103** are registered in that order. `GetAppID` is read into `+0x00` (`0x91640`). `0020CCC0` asks `BLoggedOn`, then `RequestCurrentStats`. `[01F83450]` = the manager, `+0x10` = **41**, and `+0x18` = 0 |
| `I2_award_before_1101_marks_locally_no_steam_call` | I-2 | an award by index before 1101 (`008632B0(5)`) marks entry 5's `+0x190` and makes **no Steam call** |
| `I2_control_1101_for_another_game_changes_nothing` | I-2 (control) | a 1101 for another game id is ignored: no call, and `+0x18` stays 0 |
| `I2_1101_sets_flag_and_overwrites_entries_the_early_award_is_lost` | I-2 | 1101 with the right id and result 1 sets `+0x18`. It then overwrites every entry's `+0x190` from `GetAchievement` (40 reads). **Entry 5's early mark is back to 0: the pre-receipt award is lost** |
| `I3_award_after_1101_sends_once_then_is_idempotent` | I-3 | after 1101, the same award calls `SetAchievement("ACH_COUNT_KILL")`, then `StoreStats`. Awarding it again makes **no** Steam call |
| `I4_entry0_awarded_once_on_the_receipt_that_reaches_count_minus_1` | I-4 | 1103 receipts count into `+0x14`. Only the receipt that brings it to **40** (count − 1) looks at entry 0, and with entry 0 not achieved it awards it through `0020CE10`. **One award in 41 receipts** |
| `I4_static_no_by_index_payload_is_0` | I-4 | the by-index route's payload table `00D10550` (the evaluate path's `[r15 + r14*4 + 0xBF0550]`) holds no 0 for ids 0–29. **No authored condition awards entry 0** |

## I-1's failure half: `i1.py` (OPUS, 2026-09-26)

AUDIT-SEM's residual on `AUDITSEM-REQ-OPUS-424` was that *"the modelled `ContextInit` always succeeds, so `SteamAPI_Init`
failing → `[01F83450]` → achievements silently off is unexecuted"*.

`i1.py` runs the shipped start-up `007980A0` from its entry, as a prefix that stops at `00798152`, the first instruction
after the Steam block `00798116`–`0079814B`. It runs over block 332's world, whose cases run first.

**Disclosed models:**
- **Steam, as the library answers when the client is not running:** `SteamInternal_ContextInit` returns a context whose
  interfaces are all null, and `SteamAPI_Init` returns false. `SteamAPI_RestartAppIfNecessary` returns the case's value.
- **OS:** `SetUnhandledExceptionFilter` → 0, `ImmDisableIME` → TRUE, `CoInitializeEx` → S_OK.
- **`exit`** is recorded and stops the run.

**5 / 5 pass; `i1_result.json` is byte-identical over two runs (md5 `b6478d94…`).**

| case | observed |
|---|---|
| `F1_init_fails_no_manager_startup_continues` | the imports run in the order SetUnhandledExceptionFilter, ImmDisableIME, CoInitializeEx, `SteamInternal_ContextInit`, `SteamAPI_Init` (false), `SteamAPI_RestartAppIfNecessary(0x91640)` (false). The builder `0020CD30` is **not entered**, `[01F83450]` stays **0**, and start-up reaches `00798152` |
| `F2_every_award_returns_at_the_null_manager` | in that world `008632B0(k)` for all 41 entries returns at `0020CE00`'s null manager. The award body `0020CE60` is never entered, and **no Steam import is called** |
| `F3_restart_true_exits_1_before_any_manager` | with `RestartAppIfNecessary` true, `exit(1)` is called at `0079814B`, and no manager exists |
| `C1_control_init_true_enters_the_builder` | control: `SteamAPI_Init` true (context still empty) enters `0020CD30` from `0079812D` (stopped at its entry) |
| `S1_the_branches` | `0079811C cmp [rax+0x18], 0` precedes the `SteamAPI_Init` call; `0079812B je 00798137` skips the builder on false |

**So I-1 is executed on both halves:** the failure half here, and the success half in `M0` above.

## Not covered

- **I-5 and I-6:** static.
- **The model is the library's documented behaviour, not the library.** A live run is what would test the model itself.
