---
contract: Steam integration — one start-up handshake, one per-frame callback pump, and an award path that only reaches Steam after Steam has answered
category: 20-Platform-Online-Achievements
scope: subsystem
readiness: CONTRACT READY   # the lifecycle, the award path and the failure behaviour are STATIC; nothing here was observed live
confidence: PROVEN
implements:
  - 20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md
entries: [007980A0, 0020CD30, 0020C730, 007A3110, 0020C940, 0020CB20, 0020C8C0, 008632B0, 0020CE60, 00863240, 0020CB50]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: read from the authority image on 2026-09-25 (FABLE, Claude Opus 5.5) with capstone. The nine
    steam_api64.dll import slots were parsed from the PE import directory and every instruction reading
    one was listed (Database/Tools/work/FABLE/gg3-scratch/steam_iat.py; control - the page's nine imports).
    Callers come from the raw E8/E9 index with its unlisted-code arm and thunk hop
    (pub140-scratch/tools/rawcalls.py), the jcc sweep and the RTTI vtable finder (uq250/qfind.py).
    Interface slot meanings are read from argument shapes, the callback ids and the log strings each
    call sits beside, not from SDK ordering alone.
last_reviewed: 2026-09-29
falsification_passes: 0
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-steam-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — Steam integration (FABLE, Claude Opus 5.5)

> **Why this exists.** S-45's verdict row says *"the counter is contracted; Steam integration is not"*.
> [The counter contract](CONTRACT-achievement-counters.md) is `family`-scoped over moving an achievement
> counter. This contract is the subsystem around it: how the game connects to Steam, how Steam's
> answers reach it, and what happens to an award on each path, including when Steam is absent.

## 1. What this contract covers (FABLE)

- **Start-up**: initialisation, the achievement manager, callback registration and the relaunch check
  (§3).
- **The pump**: where Steam callbacks are serviced (§4).
- **The award path**: from the counter updater to `SetAchievement` / `StoreStats` (§5).
- **The receipt handlers** and the automatic award of entry 0 (§6).

The evidence page is [the Steam integration and achievement catalogue](steam-integration-and-achievement-catalogue.md).

## 2. The objects (FABLE)

| object | where | role |
|---|---|---|
| the Steam API context | `01DFE0D0`, init callback `001F3E10` | a table of interface pointers, re-fetched through `SteamInternal_ContextInit` before every call; `+0x28` is the user-stats interface every call below uses |
| the achievement manager | `0x80` bytes at `*(01F83450)`, created by `0020CD30` | `+0x00` game id (compared with each callback's `+0x00`), `+0x08` entry array (stride `0x198`), `+0x10` count (**41**), `+0x14` achieved count, `+0x18` "stats received" flag |
| an entry | `0x198` bytes | `+0x08` API name, `+0x10` display name (`0x80`), `+0x90` description (`0x100`), `+0x190` achieved byte, `+0x194` a dword cleared on award |
| the descriptors | `01DFE410` | the static array the manager is built from (AB-2 on the page) |

## 3. Start-up — `007980A0` (FABLE)

1. `SteamInternal_ContextInit(01DFE0D0)` (`00798116`). **If the context's `+0x18` is already set,**
   skip to step 3.
2. `SteamAPI_Init` (`00798123`). **If it fails, go straight to step 4: no manager is created.**
3. Create the manager, `0020CD30` (`0079812D`). It allocates `0x80` bytes and calls `0020C730` with
   the descriptors and 41 entries, and stores the result at `01F83450`. `0020C730` registers three
   callbacks:
   - **1101** `UserStatsReceived` → `0020C940`;
   - **1102** `UserStatsStored` → `0020CB20`;
   - **1103** `UserAchievementStored` → `0020C8C0`.

   It then makes one user-stats call (slot `+0x48`, the stats request) and `0020CCC0`. Next,
   `008655E0` registers callback **331** (`GameOverlayActivated`, `0x14B`).
4. **Always:** `SteamAPI_RestartAppIfNecessary(0x91640)` (`0079813C`). `0x91640` is 595520, this
   game's Steam application id. **If it returns true, the process calls `exit(1)`** (`0079814B`).

Init runs **before** the relaunch check, the reverse of the usual SDK order. The shipped image does
it this way.

## 4. The pump — `007A3110` (FABLE)

Slot 0 of Phyre's `PWindowWin32Base` / `PWindow` vtables (RTTI). It has no direct caller:
- if `[02EA5368]+0x69` is set, it returns 9;
- otherwise it calls **`SteamAPI_RunCallbacks`** (`007A312E`) and then
  `InputBackend_UpdateResolvedDeviceState`.

**Steam callbacks are therefore delivered once per window pump, on that thread, beside the input
update.**

## 5. The award path (FABLE)

- **By index — used by the achievement code:** the counter updater `00316A50` (twice), ~~the periodic~~
  ~~checker~~ the evaluator `00315E90` (run per id by the periodic sweep `00316930`) *(corrected 2026-10-02, OPUS: `00316930+0x109` calls it for ids 0–29)*, `003162E0`, `00316440` and `00352250` call `008632B0(index)`. That thunk fetches
  the manager (`0020CE00` = `mov rax, [01F83450]`), **returns if it is null**, and tail-jumps to
  `0020CE60(manager, index)`.
- **`0020CE60`:**
  1. If the entry is already achieved (`+0x190`), it returns 1 and **makes no Steam call**.
  2. Otherwise it sets `+0x190 = 1` and `+0x194 = 0`.
  3. If stats have been received (`+0x18`), it calls `SetAchievement(entry.name)` (slot `+0x38`) and
     then **`StoreStats`** (slot `+0x50`, tail-jump).
  4. **Otherwise it returns 0 with the award recorded only locally.**
- **By id — a second entry:** `0034C9A0` → `00863240` → `0020CB50`. It makes the same pair of calls,
  with a second conditional `SetAchievement` around `cmp ebx, 6`. That branch's meaning is not read (§9).

## 6. Receipt (FABLE)

- **1101 `UserStatsReceived` (`0020C940`).** On a matching game id with result 1:
  - it sets `+0x18 = 1` and resets the achieved count;
  - for entries 1 … n−1 it **overwrites each entry's `+0x190` with Steam's `GetAchievement`**
    (slot `+0x30`) and copies the display attributes `"name"` / `"desc"` (slot `+0x60`);
  - **if every other entry is achieved and entry 0 is not**, it calls `SetAchievement(entry0)` and
    `StoreStats`.
- **1103 `UserAchievementStored` (`0020C8C0`).** It increments the achieved count. At n−1 it re-reads
  entry 0 and, if that is unachieved, awards it through `0020CE10`.
- **1102 `UserStatsStored` (`0020CB20`).** It only logs success or failure.

## 7. Invariants (FABLE)

**I-1 — Without Steam, achievements are silently off.** If `SteamAPI_Init` fails, `[01F83450]`
stays null and every by-index award returns at the null check.
*Falsified by:* ~~a writer of `01F83450` outside `0020CD30`~~ **a non-null store to `01F83450` outside `0020CD30`** (2026-09-29, OPUS falsification pass 1, `CON-177`), or an award route that skips `0020CE00`'s
test.

> **I-1's falsifier as first written is met, and the invariant survives** (2026-09-29, OPUS falsification pass 1, `CON-177`). There is a second writer:
> - `0020CD80`, the manager's destructor, frees the `0x80` bytes and stores **0** (`0020CDED`).
> - It never installs a manager, so no route turns awards on without `0020CD30`.
> - It adds a second way into "off": after it runs, every by-index award returns at the same null check.

**I-2 — An award reaches Steam only after Steam's stats have arrived.** Before 1101 sets `+0x18`,
`0020CE60` records the award locally and sends nothing. 1101 then overwrites every entry's flag with
Steam's value, **so an award made before the stats arrive is lost unless the game issues it again.**
*Falsified by:* a queue of pre-receipt awards replayed on 1101, or a send path that does not test
`+0x18`.

**I-3 — Awards are idempotent per session.** An entry already marked achieved produces no Steam call.
*Falsified by:* a call path to slot `+0x38` that skips `+0x190`'s test. *(Checked 2026-09-29, OPUS falsification pass 1.)*
- `0020CE10` sends with no `+0x190` test of its own.
- Its one caller, the 1103 handler `0020C8C0`, re-reads entry 0's flag from Steam (slot `+0x30` into `+0x190`) and tests
  it immediately before the call.
- `0020CE10` does not set `+0x190`, so a repeat is prevented by Steam's re-read, not by the local byte.

**I-4 — Entry 0, `ACH_CHAMPION_IVALICE` ("Champion of Ivalice"), is awarded by the game, not by any authored condition.** It is the only entry the
receipt handlers award, and they award it exactly when every other entry is achieved.
*Falsified by:* a by-index caller passing 0.

**I-5 — Callbacks run on the window pump.** `SteamAPI_RunCallbacks` has exactly one call site, in
`PWindow` slot 0.
*Falsified by:* a second call site of the import.

**I-6 — A Steam relaunch request ends the process at start-up.**
*Falsified by:* a path past `0079814B` on a true return.

## 8. What a reimplementation must match (FABLE)

- Construct the manager only after a successful `SteamAPI_Init`, and treat a null manager as
  "achievements off" (I-1).
- Do not send before the stats receipt, and let the receipt overwrite local flags (I-2). A
  reimplementation that queues early awards changes behaviour.
- Auto-award entry 0 on completion (I-4).

## 9. What this contract does NOT establish (FABLE)

- ~~Which achievement entry 0 is.~~ **Answered 2026-09-25:** descriptor slot 0 at `01DFE410` is `ACH_CHAMPION_IVALICE`, *Champion of Ivalice* ([`members/achievement-descriptors.tsv`](members/achievement-descriptors.tsv)), the all-achievements award. That is why only the receipt handlers ever award it.
- Whether any caller re-issues an award that I-2 drops. ~~The periodic checker `00315E90` is the~~
  ~~likely candidate, and it is not read for that here.~~ Not the evaluator `00315E90`: it returns at once when the save block's award bit is set (`00315E90+0x4F`), and its award tail sets that bit before calling `008632B0`. `00316440` does re-issue one: when the save block's bit 13 is set and Steam's entry `0x13` reads unachieved through `00863280`, it calls `008632B0(0x13)` again (`00316440+0x9`..`+0x2D`). `003162E0`, which the sweep tail-jumps to, also tests `00863280` before its `008632B0` call (`003162E0+0x116`..`+0x123`); its condition is not read here *(answered: read 2026-10-02, OPUS)*.
- ~~The `cmp ebx, 6` branch in `0020CB50`,~~ **Answered mechanically, 2026-09-29 (OPUS falsification pass 1):**
  - the by-id table at `00906290` has seven 12-byte rows, `{key1, key2, entry}`, whose entries are 31, 32, 34, 35, 36,
    37 and 38;
  - when the matched row is index 6, `0020CB50` also walks entry offsets `0x3168`–`0x3C90`, which is entries **31–37**,
    awarding each under the same `+0x190` / `+0x18` tests.
  - What the keys name is not read.

  Still open: what `0020CCC0` does after registration.
- What `[02EA5368]+0x69` means (the pump's early return).
- Anything live.

## 10. Related (FABLE)

- [The Steam integration and achievement catalogue](steam-integration-and-achievement-catalogue.md): the evidence page.
- [The achievement counters](CONTRACT-achievement-counters.md): the counter updater this path starts from.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

**CoreRuntimeScheduling — CLIENT.** `007980A0`, the application start-up, owns the Steam handshake
order (§3). This subsystem is a step inside it.

**Input — MECHANICAL.** The pump `007A3110` calls `InputBackend_UpdateResolvedDeviceState` right
after `SteamAPI_RunCallbacks`. They are co-scheduled in one window method, with no shared state.

**Middleware (Phyre) — CLIENT.** The pump is slot 0 of Phyre's `PWindow` vtable; Phyre's window
loop drives it.

**Script_VM_Native_Bridge — CLIENT.** Two script verbs reach the award path directly. `unkCall_5ad` (call 0x5AD, one int argument; handler `00352250`) tail-jumps `008632B0`, **so a script can award an achievement by index**. The `startscene` handler `0034C9A0` (call 0x11B) reaches `00863240` → `0020CB50`. **Measured 2026-09-25** ([`members/script_award_verb_census.py`](members/script_award_verb_census.py) → `members/script-award-verb-census.tsv`, over every shipped `.ebp`): exactly three indices are ever passed. **39** `ACH_TRIAL_MODE_50` (*Judge Magister*) and **40** `ACH_TRIAL_MODE_100` (*Imperator*) are passed by the Trial Mode stage scripts `tri_*`, 900 sites each (100 per locale). **33** `ACH_EVENT_RETURN_RABANASTRE` (*A Traitor Redeemed*) is passed once per locale, in `slm_a01`. Trial Mode's achievements therefore bypass the counter updater entirely.

**CombatAction — CLIENT.** `00316440`, one of the by-index award callers, is itself called from the combat-action body `00305640`. The combat layer decides when; this subsystem transports.

**Gameplay — CLIENT.** ~~The periodic checker~~ The evaluator `00315E90` (its mode-2 arm) *(corrected 2026-10-02, OPUS: the periodic sweep is `00316930`)* consults `00309EC0` before awarding.

**ActorEntity — MECHANICAL.** `0034C9A0` (`startscene`) also calls `0032F240`, the registered-id lookup (read-only: enable byte `022C6D18+i`, id dword `022C6D28+4i`, else `-1`; it notifies nothing). That is unrelated to the award itself.

**Save_Load_Settings — MECHANICAL.** The start-up body `007980A0` also runs the settings loaders `001DE050`/`001DED50`. That is start-up co-scheduling with no shared state with the Steam handshake.

**Rewards_Progression_Economy — CLIENT.** The counter updater `00316A50`, the main by-index award
caller, is itself called from the reward bodies `00254EE0` and `00312280`, which advance counters on
reward events ([the counter contract](CONTRACT-achievement-counters.md)). This subsystem is downstream
of them and owns no reward state.

## Falsification pass 1 — 2026-09-29 (OPUS): tested with the contract's own falsifiers

**Attack.** Each invariant's "Falsified by" clause became a check: I-1 to I-6 and §3. Script:
`Tools/analysis-kit/gfz-scripts/falsify_steam.py`, output `falsify_steam.out`, image `73461d08…`, 0 BROKEN, exit 0.
The execution is OPUS's S-45 replays, and is not repeated.

| # | Clause attacked | Result |
|---|---|---|
| K1 | I-1's falsifier, "a writer outside `0020CD30`" | **met** (`CON-177`): the destructor `0020CD80` stores 0. The invariant's substance survives, since no non-null store exists outside `0020CD30`, and the falsifier is restated |
| W2 | I-2, I-3 | **survives**: every `SetAchievement` is in `0020CE60`, `0020CB50` ×2, `0020C940` or `0020CE10`. The first three test `+0x190` and `+0x18`; `0020CE10` tests `+0x18`, and its one caller re-reads and tests `+0x190` |
| W3 | §9, the `cmp ebx, 6` branch | **answered**: by-id row 6 also awards entries 31–37 under the same tests |
| W4 | I-4 | **survives**: the seven by-id rows map to entries 31–38, and no by-index call site passes a literal 0 |
| W5 | I-5 | **survives**: one `SteamAPI_RunCallbacks` site, `007A312E`, after the `+0x69` early return |
| W6 | I-6, §3 | **survives**: ContextInit → Init → manager → RestartAppIfNecessary(`0x91640`) → exit on true |

Corrected in place: I-1's falsifier; §9 and I-3 gained notes. The consumer record is
`_index/candidates/steam-falsification-pass-1-0929/`.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-steam-integration-subsystem-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001F3E10` | 131 B | zeroes the twenty qwords `rcx+0x00` through `rcx+0x98`, then calls the import through `008C31A0`; when that returns non-zero it tail-jumps `001F3AE0(rcx)`, otherwise it returns that zero | `001F3E1B`, `001F3E6F`, `001F3E76`, `001F3E7E`, `001F3E88` |
| `0020C8C0` | 121 B | returns at once unless the sign-extended dword `[rcx]` equals qword `[rdx]`; otherwise increments dword `rcx+0x14` and, when it then equals dword `rcx+0x10` minus 1, takes the `+0x28` interface of `008C3190(01DFE0D0)` and calls its vtable slot `+0x30` with qword `[[rcx+8]+8]` and `[rcx+8]+0x190`, then calls `0020CE10(rcx, qword [[rcx+8]+8])` when byte `[[rcx+8]+0x190]` is zero; on both count paths it ends with a tail jump to `005CDAA0(2, 00906490)` | `0020C8CC`, `0020C8D4`, `0020C901`, `0020C918`, `0020C92E` |
| `0020CB20` | 48 B | returns at once unless the sign-extended dword `[rcx]` equals qword `[rdx]`; otherwise tail-jumps `005CDAA0(2, 00906458, dword [rdx+8])` when dword `[rdx+8]` is 1 and `005CDAA0(2, 00906470, dword [rdx+8])` for any other value | `0020CB23`, `0020CB31`, `0020CB3E`, `0020CB4A` |
| `0020CCC0` | 105 B | re-fetches `008C3190(01DFE0D0)` before each step and returns 0 in `al` when its qword `+0x28` is null, when its qword `+8` is null, or when vtable slot `+8` of the `+8` interface returns zero in `al`; otherwise tail-jumps vtable slot `+0` of the `+0x28` interface with that interface as `rcx` | `0020CCD1`, `0020CCE5`, `0020CD00`, `0020CD1F`, `0020CD22` |
| `0020CE10` | 78 B | returns 0 in `al` when byte `rcx+0x18` is zero; otherwise calls vtable slot `+0x38` of the `+0x28` interface of `008C3190(01DFE0D0)` with `rdx`, re-fetches that interface and tail-jumps its vtable slot `+0x50` | `0020CE16`, `0020CE36`, `0020CE52`, `0020CE56` |
