---
system: The time-stop registry — twenty-eight stop requests, seven per-actor stop sets, one combined permission mask
category: 00-Engine-Core-Runtime
status: AUDITED — the registry, its ids and its consumers read; which Config option 002DDC30's bit is (SM-5: Battle Mode, clear = Wait, set = Active) answered 2026-09-18; the combined-mask consumers (SM-3), what sets 3 and 4 mean in player terms (SM-2) and the names of ids 15, 18 and 22 (SM-1) answered 2026-09-17
owner_layer: none — the registry is unowned engine infrastructure; its requesters are Script VM verbs, the UI router, the actor-resource layer and the field hold
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: complete bodies of the start 00226BE0, the per-id record filler 00227680, the apply step 00226280, the per-actor pass 00226640 and 002269A0, the classifiers 00263BE0 / 002647B0, the UI-id map 00255290, every start / cancel wrapper and every call site's id argument (raw E8/E9 index), 00227680 run in isolation for all 28 ids (records tabulated §3.1), and the consumers of each live stop set from the committed access censuses
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-time-stop-registry-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The time-stop registry

> **What freezes the world when a menu opens, a cutscene takes an actor, a time-stop magick is cast or
> a skippable scene runs is one engine registry, not a check in each subsystem.** Twenty-eight request
> slots each hold a *permission* record; starting a request marks every managed actor as stopped for
> that request and then exempts the actors the record names; one apply step folds the pending marks
> into seven live stop sets per actor, fires each set's transition hook, and ANDs every active record
> into one combined mask that switches audio groups, character culling, input and UI globally.
> Authored by FABLE, 2026-09-12.

## 1. What the player sees

Open the main menu in the field and everyone stops mid-step; cast a time-stop and only the caster's side
keeps moving; enter a conversation and the talking actors play while the rest of the scene holds; skip a
scene and the world resumes cleanly. Each of those is a different **request id** in this registry, and the
differences between them — who keeps moving, whether animations freeze or only scripts, whether sound
groups mute — are the per-id records described here. The registry is also why several things stop
*together*: every active request is combined, so the most restrictive request wins for each capability.

## 2. The data

| address | what |
|---|---|
| `01FD46D4` | **active-request bitset** — bit *n* set while request id *n* (0–27) is started |
| `01FD4160` + `id × 0x18` | **record A** for id — a qword pair of permission bits (§3) |
| `01FD4160` + `0x2A0` + `id × 0x18` | **record B** for id — the second permission qword pair, a dword `+0x10` (the request's fade length, one-shot, §4) and a flag byte `+0x14` |
| `01FD46D0` | dirty byte — set by a start or cancel, cleared by the apply step |
| `01FD46A0`–`01FD46C8` | the **combined** A and B masks and fade length the last apply computed |

`00226B10(id)` returns a record address; `00226BC0()` is "any request active" (`01FD46D4 != 0`, callers the
main loop `0022A770` and `00357380`); `00226BA0()` is "the combined masks restrict anything" (`A & B != −1`);
`00226BD0(id)` tests one bit; `00226B30` resets the registry.

## 3. Starting a request — `00226BE0(id, actorHandle, flag, …, count, handles)`

Refused while the id's bit is already set (`00226C08`). Otherwise:

1. **The records are built for the id** by `00227680` (a 28-case switch at `00227744`): both records start
   from a common default, then the id's case sets and clears permission bits. Bit layout, per *category* c
   (0–7): record A **bit c** exempts from set 1, record B **bit c** from set 4, A **bit 8 + c** from set 2,
   B **bit 8 + c** from set 5, A **bit 16 + c** from set 6, B **bit 16 + c** from set 7, and set 3 needs A
   **bit 28 and bit 8 + c** together (§5). A *set* bit is an exemption.
2. **Every managed actor is marked** (`00226CA2`–`00226D87`, over ~~1 or 3 managers by record A bit 30~~ **1 manager
   when record A bit 31 is set, 3 when it is clear** — `00226C77`–`00226C91` computes `(~(A >> 30) & 2) | 1`;
   corrected 2026-09-12, §3.1): the
   id's bit is OR-ed into the seven *pending-set* words and cleared from the seven *pending-clear* words
   (§5).
3. **Exemptions are applied by category** — the id's bit is cleared again from a pending-set word when the
   record's bit for that category is set:

| c | category | how it is found |
|---:|---|---|
| 0 | the party focus actor | `PartyFocus_GetCurrentPackedActorHandle` (`00226DA4`) |
| 5 | the request's own actor | the `actorHandle` argument (`00226E62`) |
| 1 | the other party members | `PartyRoster_GetActorBySlot(0…3)` excluding the focus (`00226F20`) |
| 6 | an explicit handle list | `count` / `handles` arguments (`00226FED`–`002270D4`) |
| 2 / 3 / 4 | every other managed actor, by kind | skipped when `002647B0` (actor `+0x12` ≤ 3, a party slot); else `00263BE0` on actor `+0x0E` low nibble: **1, 2, 7 → 3**, **3 → 4**, **anything else → 2** (`0022713C`–`00227150`) |

4. The bit is set in `01FD46D4` and the dirty byte raised (`00226C7A`–`00226C87`). Callers then run the apply
   step `00226280` (most wrappers tail-jump to it).

**Cancelling** — `00225CD0(id, fade)` raises the dirty byte, clears the id's bit, and for every actor of the
three managers ORs the bit into the seven *pending-clear* words and removes it from the *pending-set* words
(`00225CF3`–`00225E06`); it then resets both records' first qwords to all-ones, zeroes both flag bytes and
stores `fade` as record B `+0x10` (`00225E1C`–`00225E3D`), with per-id side calls for a few ids (`00182D60`, `00182D40`, and
`00182DA0` unless `002DDC30`; the id dispatch at `00225E44`–`00225E5F` is not tabulated here). `00225EB0` is the area-unload variant (one caller, `002628B0`).

### 3.1 The twenty-eight records — what each request stops (2026-09-12, `SM-4`)

Every record's first qwords, as `00227680` builds them. Read from the body and cross-checked by running the
body in isolation for every id, both flag values and both stub returns
([probe](../../_experiments/evidence/stop-registry-permission-records/probe.py), [raw records](../../_experiments/evidence/stop-registry-permission-records/records.tsv)): the four callees
`00182CD0`, `00182CF0`, `00182D10` and `002DDC30` were replaced by `mov eax, 0|1; ret` and change no record
byte — only id 0's call path depends on `002DDC30`. The static block at `0022792D` (all-ones, bits 16–17
cleared in both records, tail jump to `00182CF0` only for id 17) is the control: the run reproduces ids
17–19 exactly and takes the tail jump for 17 alone. The **flag** argument (stored at record B `+0x14`)
changes the records of ids 4, 6 and 7 only.

Columns 1–7 list the categories **stopped** in each set (a clear bit); "all" is every category and "—" none.
**F** the party focus actor, **P** the other active party members, **T127** / **T3** / **T0** a non-party
actor whose free-target type ([the kind-byte page](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) AL-3)
is 1, 2 or 7 / is 3 / is anything else, **R** the request's own actor, **H** the handle list. An actor in
two categories is exempt if either exempts it. R and H matter only when the caller passes them. *Managers* is
how many actor managers the start walks (record A bit 31 set → manager 0 only, clear → three). The last
column lists the §4 global bits the record clears; the apply ANDs them over every active request, so a clear
bit wins.

| id | raised by | flag | A `+0` | B `+0` | 1 movement | 2 script | 3 | 4 | 5 animation | 6 unit `+0x004` b5 | 7 unit flag b36 | managers | global bits cleared |
|---:|---|:-:|---|---|---|---|---|---|---|---|---|:-:|---|
| 0 | UI requests 1/4/20 | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 1 | *no start site* | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 2 | UI requests 3/24 | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 3 | *no start site* | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 4 | field hold mode 1; boot | 0 | `00000024F9040707` | `00001F2B0B001F1F` | T3 T127 R H | T3 T127 R H | T3 T127 R H | R H | R H | F P T3 T127 R H | all | 1 | A25,26 B26 A36 B36 A39 |
| 4 | field hold mode 1; boot | 1 | `00000024F9040505` | `00001F2A09001F1F` | P T3 T127 R H | P T3 T127 R H | P T3 T127 R H | R H | R H | F P T3 T127 R H | all | 1 | A25,26 B25,26 B32 A36 B36 A39 |
| 5 | field hold mode 0 | any | `00000034EB000000` | `00001F3A0B00101F` | all | all | all | R H | F P T127 T0 R H | all | all | 1 | A26 B26 B32 A39 |
| 6 | event script takes actor; `talkfadeout` | 0 | `00000004DB040707` | `00001F0B0B001F1F` | T3 T127 R H | T3 T127 R H | T3 T127 R H | R H | R H | F P T3 T127 R H | all | 1 | A26 B26 A29 A36,37 B36,37 A39 |
| 6 | event script takes actor; `talkfadeout` | 1 | `00000004DB040505` | `00001F0A0B001F1F` | P T3 T127 R H | P T3 T127 R H | P T3 T127 R H | R H | R H | F P T3 T127 R H | all | 1 | A26 B26 A29 B32 A36,37 B36,37 A39 |
| 7 | field hold mode 2 | 0 | `00000024F9044307` | `00001F2B0B005F1F` | T3 T127 R H | T3 T127 T0 R | T3 T127 T0 R | R H | R | F P T3 T127 R H | all | 1 | A25,26 B26 A36 B36 A39 |
| 7 | field hold mode 2 | 1 | `00000024F9044105` | `00001F2A09005F1F` | P T3 T127 R H | P T3 T127 T0 R | P T3 T127 T0 R | R H | R | F P T3 T127 R H | all | 1 | A25,26 B25,26 B32 A36 B36 A39 |
| 8 | *no start site* | any | `00000030BD000060` | `00001F3209001F7F` | F P T3 T127 T0 | all | all | — | R H | all | all | 1 | A25 B25,26 A30 B32 B35 A39 |
| 9 | *no start site* | any | `00000030BD000060` | `00001F3209001F7F` | F P T3 T127 T0 | all | all | — | R H | all | all | 1 | A25 B25,26 A30 B32 B35 A39 |
| 10 | `settimestopmagic`; target cursor | any | `00000030BF7F6060` | `00001F320B001F1F` | F P T3 T127 T0 | F P T3 T127 T0 | F P T3 T127 T0 | R H | R H | — | all | 1 | B26 A30 B32 B35 A39 |
| 11 | `seteventtimestop` | any | `0000002011000000` | `00001F2A0B001F1F` | all | all | all | R H | R H | all | all | 3 | A25,26,27 B26 A29 A30 B32 A36 B36 A39 |
| 12 | `settutorial00timestop` | any | `00000024DD001F01` | `00001F3A0B1F1F1F` | P T3 T127 T0 R H | R H | R H | R H | R H | all | R H | 1 | A25 B26 A29 B32 A36 A39 |
| 13 | full-screen menus | any | `FFFFFFFFD5FFE0FF` | `FFFFFDFDFDFFFFFF` | — | F P T3 T127 T0 | F P T3 T127 T0 | — | — | — | — | 1 | A25,27 B25 A29 B33 B41 |
| 14 | *no start site* | any | `00000000BD000000` | `00001F0A09001F1F` | all | all | all | R H | R H | all | all | 1 | A25 B25,26 A30 B32 A36,37 B36,37 A39 |
| 15 | `002E2240` | any | `00000034D4000000` | `0000003A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 B40,41,42,43,44 |
| 16 | mask verbs | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | A24 B24 |
| 17 | `ucon` | any | `FFFFFFFFFFFCFFFF` | `FFFFFFFFFFFCFFFF` | — | — | — | — | — | F P | F P | 1 | — |
| 18 | `0025C830` | any | `FFFFFFFFFFFCFFFF` | `FFFFFFFFFFFCFFFF` | — | — | — | — | — | F P | F P | 1 | — |
| 19 | definition load | any | `FFFFFFFFFFFCFFFF` | `FFFFFFFFFFFCFFFF` | — | — | — | — | — | F P | F P | 1 | — |
| 20 | *no start site* | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | A24 B24 |
| 21 | *no start site* | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | A24 B24 |
| 22 | `0035C7B0` (game-over route) | any | `00000034D4000000` | `00001F3A09001F1F` | all | all | all | R H | R H | all | all | 1 | A24 A25,27 B25,26 A29 B32 A39 |
| 23 | `…dispdenystatus` | any | `FFFFFFFFFFFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | B24 |
| 24 | `…ctrldenystatus` | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFFFFFFFF` | — | — | — | — | — | — | — | 1 | A24 |
| 25 | `…dispdenystatus_by_menu` | any | `FFFFFFFFFFFFFFFF` | `FFFFFFFFFEFFFFFF` | — | — | — | — | — | — | — | 1 | B24 |
| 26 | `…ctrldenystatus_by_menu` | any | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFFFFFFFF` | — | — | — | — | — | — | — | 1 | A24 |
| 27 | `skipexec` | any | `FFFFFFFFFFFFFFFF` | `FFFFE2FFFFFFFFFF` | — | — | — | — | — | — | — | 1 | B40,42,43,44 |

What the table says, mechanically:

- **UI overlays, the game-over route and `002E2240`** (ids 0, 2, 22, 15) freeze every actor's movement,
  scripts and both battle-unit sets. Presentation set 4 and animation set 5 are stopped only for R and H, so
  other actors are not queued for the animation-rate change. Id 15 differs from the default only in clearing
  audio bits B40–44.
- **Time-stop magick and the target cursor** (id 10) stop movement, scripts and set 3 for everyone except R
  and H — the request's actor, for the cursor the selected unit, keeps acting — leave set 6 alone, and set
  set 7 on everyone including R and H.
- **`seteventtimestop`** (id 11) is the only request that walks all three managers, and it stops every
  logic set for every category.
- **`settutorial00timestop`** (id 12) leaves the focus actor moving; scripts, set 3 and set 7 stop only for
  R and H.
- **The full-screen menus** (id 13) stop only scripts and set 3, for every non-R, non-H actor. Movement,
  presentation, animation and the battle-unit sets are untouched, and record B bits 8–14 are all set, so a
  menu alone selects the apply's rate-1.0 animation path.
- **The field hold** (ids 4, 7) and **an event script taking an actor** (id 6) keep the focus actor and
  type-T0 actors moving and scripted, and the other party members too unless the flag is 1. Actors of types
  1, 2, 7 and 3 stop, as do R and H. Id 7 also stops type-T0 scripts and exempts H from scripts and
  animation. Id 5 (hold mode 0) stops everything, and animation for all but type-3 actors.
- **`ucon`, `0025C830` and the definition load** (ids 17–19) stop nothing but battle-unit sets 6 and 7,
  for F and P only.
- **The mask verbs** (id 16) clear only A24 and B24. **The status-error deny verbs** clear exactly one of
  them: the two `…dispdenystatus` verbs (23, 25) B24, the two `…ctrldenystatus` verbs (24, 26) A24. So B24
  is the display-deny bit and A24 the control-deny bit, by the verbs' own names (§4: `002EA8B0` reads B24,
  `002EA8E0` A24).
- **`skipexec`** (id 27) stops no actor; it clears audio bits B40, B42, B43 and B44.
- Ids 1 and 3 carry the default record, 8 and 9 an identical pair, 14 and 20 / 21 their own. None has a
  start site (`SM-1`), so their records are latent.

## 4. The apply step — `00226280`

Runs only when dirty (`00226287`). It walks the 28 slots (`002262E0`–`00226315`), **AND-ing records A and B of
every slot into one combined pair** and taking the **smallest non-negative record-B `+0x10`** as the fade
length, which it then resets to `−1` in each slot and marks each record B with bit 41 (`00226301`,
`00226307`). Only each record's **first** qword takes part (`002262E4`, `002262EB`); a cancelled slot holds
all-ones there, so it restricts nothing. Then:

- **Per actor**: `00226640(allExempt, fadeLength, 0)` — §5. `allExempt` is set when record B bits 8–14 are all
  set (`0022642D`–`00226461`).
- **Globally**, each from one combined bit: character distance culling
  (`CharacterRenderSystem_SetDistanceCullEnableByRequester`, B bit 35, `002265C8`–`002265D6`); **audio**
  group mask and level (`Audio_SetGroupMask` `002DF370` with groups `0x20`, `1`, …, and `002DF640`, from B
  bits 32, 33, 40, 41, 42, 43, 44; `002264C9`–`002265BA`, skipped while `01FD46D1` is set); two words
  `0209215E` / `02092162` built from A / B bits 25–27 and stored directly (`00226474`, `0022647C`), and
  `002547C0` / `00254840` given `0x10` or `0x0E` from A / B bits 36–37 (`002263FA`–`0022648C`); a **UI** bit pair `0035B4B0(5)` / `0035B510(0xFF)` on A bit 29; and requester
  bitsets whose consumers are not read here — `002E24C0` / `002E24E0` (A bit 39), `002EA8B0` / `002EA8E0`
  (B / A bit 24) and `0025A5D0` (A bit 30).

## 5. The seven per-actor stop sets — `00226640` and `002269A0`

Each set is a live bitset of the request ids that currently stop that aspect of the actor. The pass folds the
pending words in (`live |= pendingSet; live &= ~pendingClear`, both pending words zeroed) and acts on the
transition. *The three controller triplets (sets 3/4/5 at `+0x170`/`+0x164`/`+0x158`) are named in the store as
`stopSet3Render*`/`stopSet4Presentation*`/`stopSet5Animation*` `Live`/`PendingSet`/`PendingClear` on
`SecondaryContext` — 2026-09-18, SWE2-STRUCT-SECONDARY-STOPSET-FIELDS.*

| # | live set | pending set / clear | on change | consumers of the live set — what it stops |
|---:|---|---|---|---|
| 1 | battle unit `+0xF10` (`[actor+0x30] + 0xED0` `+0x40`) | `+0x54` / `+0x60` | **when it becomes non-zero**: `Actor_StopRequestedMovement` (`0022672C`) | **movement** |
| 2 | actor `+0x10C` | `+0x110` / `+0x114` | — | **script execution**: `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025E230`) and `WorldActorScriptVM_InterpretBytecode` (`0025E52C`) skip the actor unless its `+0x0B` bit 5 exempts it; OR-ed with actor `+0x13` bit 0; `00264DF0` (← `PartyControl_ApplyAnalogLocomotionToActor`) |
| 3 | controller `+0x170` | `+0x174` / `+0x178` | `002E92F0` (`002267C3`) | `00264DC0` (the hook's own test, OR-ed with actor `+0x13` bit 0) — the render record's `+0x284` side (§7) |
| 4 | controller `+0x164` | `+0x168` / `+0x16C` | — | `Actor_RefreshPresentationVisibility` (`002E904A`), `002E7E90` (← `00272DE0`), `002E9FE0` (← `PartyFocus_TryGetCurrentActorWorldPosition` and seven actor-pass functions) — a non-zero set overrides their presentation-state test (§7) |
| 5 | controller `+0x158` | `+0x15C` / `+0x160` | the actor is queued on its manager (`+0x1F0` / `+0x1F8`, `002269A0`) | **animation** *(a label this row should not have kept - corrected 2026-09-19, FABLE: **the value is an opacity, not a rate.** `00428940` is the character render record's fade-channel forwarder and `2` is the channel; channel 2 is a factor of all three of the record's fade products - [how a character fades](../../17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md). So set 5 **fades the queued actors out and back in**; whether their animation also stops is not decided by this call)*: per manager, every queued actor gets `002E8B10(actor, rate, fade + 1)` → `00428940(record, 2, rate, frames)` on the character render record — rate `0.0` with the global pair `0024FCA0` / `0024FBF0`, or `1.0` with `0024FC80` / `0024FB90` when the apply's all-exempt condition (combined record B bits 8–14 all set) holds (`002268B2`–`0022696E`) |
| 6 | battle unit `+0xF14` (`U+0x44`) | `+0x4C` / `+0x58` | `00238B40(actor, stopped ‖ actor+0x09 bit 5)` → battle unit `+0x004` bit 5 | the battle unit's stop flag word |
| 7 | battle unit `+0xF18` (`U+0x48`) | `+0x50` / `+0x5C` | `00312130(actor, !(stopped ‖ actor+0x09 bit 5))` → **battle unit flag bit 36 set while stopped** (or while that actor bit is set) | the battle unit's flag qword |

`00226A50` / `00226AB0` (← `0035A720`, `0035A7A0`, `0035A8D0`) and `00263560` also reach sets 6 and 7's hooks
for a single actor outside the registry pass; their bodies are not read here.

> **Note 2026-09-19 (FABLE): what the "rate" triple of the two rate arms below is spent on.** The global the arms ramp,
> `020926E8` (target `020926EC`, frames `020926E6`, step `020926F0`; stepped once a frame by `0024BFD0`), has exactly two
> consumers, and both multiply **the alpha of an effect element** by it when the element's container carries bit 2 of
> `+0x368` - the bit the 0.0 arm's walk sets. So the triple is the *dimming of effects* under a time stop, to 0.0 and
> back to 1.0 over the given frames; no reader uses it as a simulation rate. Read on
> [the distance-fade node's page, section 12](../../17-Presentation-Rendering/Position-To-Scalar/how-a-position-becomes-a-single-number.md).

### 5a. The `00226640` exclusive subtree — all 10 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the per-actor pass **10 frontier functions** — the set-5
animation-rate machinery §5 named and the helper layer beneath it. Interior cites are one
instruction inside each declared extent (`interior_cite.py`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| manager queue | `002269A0` (162 B) | the set-5 fold + enqueue — folds the controller's `+0x15C` / `+0x160` pending words into live `+0x158`; on a 0↔nonzero transition it calls `003589B0` once for the actor's id, appends it to the manager's `+0x1F0` array and increments `+0x1F8` (the queue §5's replay reads) | `002269B4` |
| rate arm, 0.0 | `0024FBF0` (129 B), `002FD090` (43 B), `003B1050` (216 B) | `0024FBF0` — the rate-0.0 global set: rate `xmm2` → `020926EC`, fade clamped ≥ 1 (`cmovle`) → `020926E6`, flag word `020926E4` gets `& ~0x200` then `| 0x100`, elapsed/rate ratio → `020926F0`; calls `002FD090` — walks the `02EC3D60` list setting bit `4` of `+0x368` on each node's `+0x10` linked object (the post-set dirty pass) — then tail-jumps `003B1050` | `0024FC0D` / `002FD0A9` / `003B1080` |
| rate arm, 1.0 | `0024FB90` (86 B), `0024FC80` (30 B) | `0024FB90` — the rate-1.0 scalar write: same triple, flag word `020926E4` gets `& ~0x100` then `| 0x200`; `0024FC80` — writes the `0x3FF` mask to `02092160`, runs the `003B3B50` search, tail-jumps `003B1130` (clears bit `1` of `+0x368` on the `02EBEC08` records) | `0024FBC3` / `0024FC89` |
| mask + apply | `0024FCA0` (52 B), `003B3BA0` (83 B), `003B1180` (216 B) | `0024FCA0` — writes the `0x3FE` mask to the same cell `02092160`, calls `003B3BA0` — a 32-entry `0x38`-stride walk of `02EBD490`, gated on `[slot−0x10] & 0xFFFFFC0`, marking `+0x368 |= 2` on entries whose `+8` id is in the caller's changed list — then tail-jumps `003B1180` | `0024FCB1` / `003B3BD0` / `003B11B0` |
| twin apply-walks | `003B1050`, `003B1180` (above) | near-identical 216-B loops over the `02EBEC08` slot table — 36 entries at `0x18` stride, kind-`5` objects (`[obj]==5`) in slot-kinds `([slot+0xB]>>1)&3 ∈ {1,3}`, id-membership test (raw compare, or `002E9B80`-resolved per `[slot+9]`), `+0x368 |= 4` for `003B1050` vs `|= 2` for `003B1180` — one per rate arm, as the tail of `0024FBF0` / `0024FCA0` | — |
| animation hook | `002E8B10` (77 B) | §5's per-actor call: `actor+0xC0` → `word` index → `0x740`-stride record in `022C6F28`, gated on `+0x284` nonzero → `00428940(record, 2, rate, frames)` | `002E8B33` |

`003B3B50` and `003B1130` — the sibling search and walk the `0x3FF` arm uses — are *not*
exclusive members (they serve other callers); the census set is the ten above exactly.

## 6. The ids and who raises them

Start and cancel wrappers are one per id (start `002273B0`… with `xor edx, edx; lea ecx, [rdx + id]`, cancel
`002260A0`… with `or edx, −1; lea ecx, [rdx + id + 1]`); every call site's id was recovered from its
instructions.

| id | raised by | released by |
|---:|---|---|
| 0 | UI request 1 (Battle Menu open) **when options bit 3 is clear**, UI request 4 **when it is set**, and UI request 20 always — `00255290` cases `002552B9` / `002552C7` / `002552D9` — through `00254740` | the UI close path (`00252D90`, `002544C0`) |
| 2 | UI requests 3 and 24 | same |
| 4, 5, 7 | **the field hold** — `00263480(ctx, mode)`: mode 1 → 4, mode 0 → 5, mode 2 → 7 with the actor's handle; the boot `00266D10` raises 4 (`00266F83`) and 5 (`00266FEA`) and cancels 5, 4 and 7 (`00266F92`–`00266FAE`); `0026A1D0` raises 5 | `00263480` / `00266D10` / `0026A1D0` when the hold reasons clear |
| 6 | **an event script taking the actor** (`00263230`, the mode-1 path of `ActorResource_StartEntryScriptExecution`) and the verb **`talkfadeout`** (`0026B980`) | the entry's removal (`00263050`) and **`talkfadein`** (`0026B970`) |
| 10 | verb **`settimestopmagic`**; the target-selection cursor `00313DB0` (with the selected unit as the request's actor) | **`cleartimestopmagic`**; the cursor's close |
| 11 | verb **`seteventtimestop`** (on) | the same verb (off) |
| 12 | verb **`settutorial00timestop`** | the same verb |
| 13 | **the full-screen menus** — UI requests 2, 6, 15, 17, 18, 19, 22 (`00255290` maps them) | the UI close path |
| 15 | `002E2240` (← `00228930`, `00229510`) | the same function |
| 16 | the screen-mask verbs **`maskopen`**, **`maskopenfast`**, **`mesvmaskopen`**, **`mesvmaskopenfast`** (`002E2440`) | **`maskclose`**, **`maskclosefast`** (`002E2400`), area unload, `003601D0` (`002E06B0`) |
| 17 | verbs **`ucon`** / `ucon_4a5` (`0026C5D0`); `00263660` (← `ActorManager_RunFieldRuntimePass`, `002628B0`); `0026C3E0` | the same functions |
| 18 | `0025C830` (← `0025C170`) | `0025B500` (← `WorldActorScriptVM_InterpretBytecode`, the entry removal, `0025C830`) |
| 19 | **a definition payload load** (`002678C0`, beside battle-state bit 12) | verb **`clearmapjumpstatus`** (`0025D580`) |
| 22 | `0035C7B0` (← `0027EFA0`) | UI request 11's close (`00252D90`, `002544C0`) |
| 23 | verb **`setstatuserrordispdenystatus`** | same verb |
| 24 | verb **`setstatuserrorctrldenystatus`** | same verb |
| 25 | verb **`setstatuserrordispdenystatus_by_menu`** | same verb |
| 26 | verb **`setstatuserrorctrldenystatus_by_menu`** | same verb |
| 27 | verb **`skipexec`** (`00360710`) | verb **`skipend`**; area unload (`003603F0`) |
| 1, 3, 8, 9, 14, 20, 21 | **no start route of any kind** (2026-09-12): no wrapper exists for them (the thirteen start wrappers `00227370`–`00227640` carry ids 10, 11, 12, 15, 16, 17, 18, 22, 23, 24, 25, 26, 27); the nine direct callers of `00226BE0` pass 0, 2, 13 (`00254740`, whose map `00255290` returns only −1, 0, 2 or 13), 4, 5, 6, 7, 10 and 19; no `lea` loads the start's address (the same scan finds both references to `00238850`); and its address occurs in data only inside unwind records | — |

## 7. What is not known

- [x] **SM-1.** ~~**The seven ids with no start site** (1, 3, 8, 9, 14, 20, 21) — reached by a route the raw `E8` / `E9`
  index does not see, or unused;~~ *narrowed 2026-09-12: statically unused* — no wrapper, no direct call with
  those ids, no `lea` or data pointer to the start (§6 row, each instrument with a positive control), so their
  records are latent in this build. ~~Still open: the player-facing names of ids 15, 18 and 22, whose requesters
  are engine functions not yet named.~~ `SM-1`.
  ***ANSWERED 2026-09-17 (FABLE): the three names, from their raisers.** *Id 22 is the game-over screen.* Its raiser `0035C7B0`, reached from `0027EFA0` on the game-over route, sets bit 8 of the request word `022C83E8` and posts transition request `0x16` (`0035C806`..`0035C81E`); [the router](../../16-UI/Request-Router/ui-request-router.md) names request 11 *game over*, raised by the field frame when no living playable unit is left, and request 11's close (`00252D90`, `002544C0`) is the release. *Id 15 is the capture-backed screen hold.* `002E2240(flag)` with a non-zero flag sets bits 0, 1, 9 and 20 of the system-stop flag word `0215F1DC` and asks the frame-mode setter `00229F00` for mode 6 (`002E2248`..`002E2257`), the one-shot that draws the field once and hands to mode 5 ([the frame page](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) §2.2), the capture-backed interactive mode; with a zero flag it clears the same bits and asks for mode 2, the field frame (`002E2265`..`002E2274`). Its callers are the two transition paths that put a screen over a still of the field: `00229510` from the area controller's message-18 arm (the plain field transition), which tests request kinds 2, 8, 16 and 22 (`00229534`..`00229576`), and `00228930`, which reads the router context `0209AC30` and tests kind 16 (`0022897F`). So id 15 is held while the field is frozen behind a captured frame, and released when the field frame resumes. *Id 18 has no player-facing name: it is an actor entry being built.* `0025C830` is one of the actor pass functions run once per kind by `0025C170` from `ActorManager_RunFieldRuntimePass`; it raises 18 while it builds an entry (five of its sites resolve the entry's `+0x18` payload through `ImageAddress_ResolveRuntimePointer`) and the entry removal `0025B500` releases it, which is why the id stops nothing but battle-unit sets 6 and 7 for F and P: a unit being built must not be ticked as a battle unit until its entry is complete. Static; bodies and the router's and frame page's tables read.*
- [x] **SM-2.** ~~**What sets 3 and 4 stop in player terms**~~ — set 3's hook tests the character render record `+0x284`,
  set 4 overrides a presentation-state predicate used by focus and actor-pass code. `SM-2`. *Set 3 narrowed 2026-09-12:* its hook `002E92F0` writes
  "not stopped" into the render record's `+0x304` bit 4 and queues request bit 26 (resume) or 27 (stop) of `+0x290`
  (`00428FE0`). `RenderRecords_ProcessDirtyState` serves them (`004281C3` → `0042BA90`, `004285D7` → `0042B970`),
  and both walk the character's render hierarchy — the record, its `+8` child and the `+0xA` chain through
  `CharacterRenderHierarchy_TraverseIndexDepthFirst` — setting or clearing **`+0x284` bit 24** and bit 18 of each
  presentation entry's `+0xC` (`00420EA0`). Bit 24 is read by `004213E0` and `00423B10`; what it changes on screen
  is the residue.
  *Set 4 answered at the mechanism level 2026-09-12 (FABLE): a stopped actor counts as absent.* The three readers apply
  one predicate to a kind-3 actor (`+0x03 & 0xE0 == 0x60`): the context at actor `+0xC0` must have **set 4 (`+0x164`) at
  zero** and its flag bytes must match — `+0x10` bits 0, 1, 3 (bits 0, 1 when `+0x11` bit 5 is set) and `+0x11` bits 1–2
  (`002E9FFC`–`002EA024`, `002E7EA9`–`002E7ED1`, `002E904A`–`002E906E`); any other actor kind passes `002E9FE0`
  outright. **`+0x10` bit 0 is the script's show flag**: `hidetargetgroup` (`0x3C3`, `003487E0`) clears it and
  `showtargetgroup` (`0x3C4`, `00349180`) sets it, through `0026DC70` → `002ECD50`, which then refreshes visibility
  ([the context census](../../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md) `+0x010`). So a non-zero set 4 has the effect of a script hide for these readers:
  `002E9FE0` answers "not present", which drops the actor from the three actor managers' target-candidate arrays
  ([command availability](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md)) and
  from `PartyFocus_TryGetCurrentActorWorldPosition`; `002E7E90` returns `0.0` instead of the character render
  record's channel 11 (`0042FB20`, Q12 → float); and `Actor_RefreshPresentationVisibility` takes its other branch.
  Per §3.1, set 4 is only ever applied to **the request's own actor and handle list** (ids 0–7, 10–12, 14, 15, 22), so
  the actor a cutscene, a hold or a time-stop names is taken out of targeting and presence while the rest of the field
  is not. What channel 11 carries and what the other flag bits of `+0x10` / `+0x11` mean are open.
  ***ANSWERED 2026-09-17 (FABLE): set 3 freezes the character's additive motions at their current frame, and that is the whole of what reaches the screen.** Of the two fields bit 24 fans out to, ~~the byte `+5` of the `0x3C0` table at `02CA8420` has no reader~~ **(CORRECTED 2026-09-19, FABLE: it has one. The pool's per-frame update (0051C3C0, 2,128 B, head read only - so written without code marks) reaches each entry through the LIST pointer `02CA8408`, not through the pool base, and skips an entry while bit 0 of its byte `+5` - or of the global byte `02CA8402` - is set (0051C450..0051C45C). The entries are the up-to-four auxiliary objects a render record builds from its model's FCP section 4: each tracks a bone's base and tip, sixteen samples deep, and 202 of the 216 models that have them are weapons. So set 3 freezes those histories as well as the pose sequencer. The scan below listed the functions that reference the pool's BASE; a reader that walks the list never references it.)** The original reasoning, kept: the six functions that reference that base are `0051BC10`, `0051C270`, `0051C380`, `0051CC10`, `0051CC30` and `0051CDC0`, and the only access to `+5` among them is the writer's own read-modify-write (`0051C39F`..`0051C3A5`). The word `+2` of the `0x40` record at `02CA6CA0` is read once outside its writer, in `00477480` (347 B, called twice from `CharacterRenderRecord_Update`, `0042C410` and `0042C8F0`): it selects the handle's record (`0047749C`..`004774BD`, validated by `[rec+4] == handle`), then leaves at once when `word[rec+2]` or the global `02CA6C98` is non-zero (`004774D3`..`004774DD`); otherwise it steps the record's per-channel counters (`[rec+0x28+i]`, `[rec+0x30+i]`, `[rec+0x38+i]`, the loop, hold and reset arms at `00477580`..`0047759F`) through the packed channel table [the add-motion page](../../17-Presentation-Rendering/Model-And-Motion-Formats/adm-add-motion-tables.md)'s decoder `004776D0` reads. So `004775E0(h, 1)` parks the character's add-motion channels and `004775E0(h, 0)` lets them run again, and `02CA6C98` does the same for every character at once. The other reads of a word at `+2` in `004778D0` and `00477B10` are into decoded channel data, not the record. Set 4 stands as answered at the mechanism level on 2026-09-12: the actor drops out of the presence predicate like a `hidetargetgroup` hide. Static; bodies read.*
- [x] ~~**SM-3.** **The consumers of the combined mask's un-named global bits** — the requester bitsets behind~~
  `002E24C0` / `002E24E0`, ~~`002EA8B0` / `002EA8E0`~~ *(named by §3.1: status-error display deny and control
  deny)*, `0025A5D0`, the speed words on A / B bits 36–37, and what
  the input words `0209215E` / `02092162` and the UI pair `0035B4B0` / `0035B510` gate. `SM-3`.
  ***ANSWERED 2026-09-17 (FABLE): every listed consumer is named, and one label is corrected.** *A bit 39*, `002E24C0`/`002E24E0`: set or clear bit `ecx` of the requester byte `0215F1B3` (its other writers are the root `002E09A0`, `002E1450` and the reset `002E24B0`), then tail into `00404D70` while the byte is non-zero, which sets `+0xC8` bit 3 on the object at `02B62D80` unless its bit 1 is set and bit 7 on the object at `02B62D88` unless its bit 5 is set, or into `00404DC0` when it reaches zero, which clears both: a deferred enable on two presentation objects, held while any requester bit stands. *A bit 30*, `0025A5D0(x)`: writes the camera system's byte `02098DEB` (1 or 0; `CameraSystem_InitializeRecords` zeroes it), which the per-frame camera function `00259990` reads beside its neighbour `02098DEA`: a non-zero value routes the frame through `003D9930` instead of `003D9950` on the camera's `+0x10`/`+0x640` records and counts down from values above 1 (`002599F6`..`00259A36`), a camera-hold request. *A/B bits 25..27*, the input words `0209215E`/`02092162`: they are button-allow masks, ten bits per word, set to `0x3FF` at boot by `0024C970` (`0024C98A`), and the button query `0024D4E0` ANDs `02092162`, `02092164` and `02092166` before testing bit `button - 1` (`0024D4F5`..`0024D512`; `0024D540`, `0024D770` and `0024B9B0` read them the same way), so a stop denies the buttons whose bits it clears. *A/B bits 36..37*, the words `01E0C2B0`/`01E0C2AC` given `0x10` or `0x0E`: they are not speed words but **UI layer masks**: `01E0C2B0` is the argument of the battle-HUD draw `0028E290` (named scope `display UI : battle`, `002508A4`), `01E0C2AC` of the menu draw `0028EAB0` (`display UI : menu`, `00252AD3`); the battle draw tests bit 0 and the menu draw bits 0, 2 and 3 (`0028E3B7`; `0028EC63`, `0028EC94`, `0028ED7E`), so `0x0E` draws the menu's bit-2 and bit-3 layers and `0x10` draws neither; both words are also restored by the save apply `00253970`. *A bit 29*, the pair `0035B4B0(5)`/`0035B510(0xFF)`: not a UI pair but the **pad-vibration pause and resume**: `0035B4B0` ORs the bits into `02EC0B40` and moves every playing vibration slot whose byte `+0x1B` carries them from state 2 to 3, `0035B510` clears the bits and moves every state-3 slot back to 2 (the slot array [the five-tables page](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md) reads for VIB0). Static, bodies read; what each of the two presentation objects draws is on [the world-tick page](../Battle-Frame/the-world-tick-and-the-field-frame.md)'s terms, not re-derived here.*
- [x] ~~**Each id's permission record in player terms** — the 28 cases of `00227680` are read as bit
  operations; which categories each id exempts from which set is recoverable from them but is not tabulated
  here.~~ **Tabulated 2026-09-12, §3.1** — every id's records, the categories each set stops, the manager
  count and the global bits cleared. What each *set* means in player terms stays with `SM-2` / `SM-3`. `SM-4`.
- [x] **SM-5.** **What `002DDC30` decides** for UI requests 1 and 4. `SM-5`. *Narrowed 2026-09-12:* it returns **bit 3
  of the saved options word** `*(0215E6E0)` — the record `002DDE60` points at the active save buffer + 8 and
  fills with defaults (bit 3 = 0). **Settings command 4** writes it (`002407F0` → `002DE060`) and reads it
  (`002403F0` → `002DDC30`). The bit selects which of UI requests 1 and 4 raises id 0, gates `003B3B40` (sets
  `02EBDBBC` bit 0) for request 1 only while clear (`00254775`), skips id 0's builder tail call `00182D10` while
  set (`002277FD`), and gates `00182DA0` in the cancel. *(2026-09-12: requests 1 and 4 are both the battle menu open — the same `0x61F0` widget, [the widget page](../../16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md) — so the bit decides **which of the two battle-menu requests freezes the field**.)* **Open:** the option's name on the Config screen
  (asked live, `FABLE-REQ-ASTRA-OPTIONS-BIT3`).
  ***ANSWERED 2026-09-18 (FABLE), statically: the option is the Config screen's Battle Mode row, and bit 3 clear is Wait, set is Active.** The Config rows issue their command id from the row byte `+0xC0` (`0023D77E`..`0023D78A` and its three siblings) into `00240750`, whose command-4 arm `00240784` only normalises the value to 0 or 1 before `002407F0` dispatches to `002DE060`, which stores `value & 1` at bit 3 (`002DE067`..`002DE070`); the read side `00240330` arm `00240390` normalises the same way after `002403F0` returns the bit. The row's value label comes from the 45-entry command descriptor table `01E0BF60` (indexed by command id, `0023DA22`..`0023DA8D`): command 4's descriptor `01E0B930` is kind 2 with two 6-byte value entries whose text ids are `0x431` (1073) for value 0 and `0x432` (1074) for value 1, and in `menu_command.bin` (bank 1 of the string pool, ids 10000..12205, positions 73 and 74) those decode as *Wait* and *Active*. So the saved options bit the registry reads through `002DDC30` is the Battle Mode setting: clear (the default the filler `002DDE60` leaves, per the reading above) is Wait, and while clear the ordinary battle-menu open (request 1) raises stop id 0 and freezes the field; set is Active, and then only request 4 does. The two help ids `0xC5B` / `0xC5C` are the row's help texts and are not needed for the name. Static, from the image and the `us` text bank; the live request `FABLE-REQ-ASTRA-OPTIONS-BIT3` is withdrawn as no longer needed.*

## 7a. Cross-subsystem neighbours — disposition (2026-09-12)

`audit_crossrefs.py` against the current graph reports two findings:

- **CombatAction — `00313DB0` calls the start, the apply and the cancel.** `00313DB0` is the target-selection
  cursor, already named in §6 as a raiser and releaser of id 10; the finding is only that the page did not
  name its subsystem. A battle-targeting UI freezing the field while the player chooses is the §3.1 id-10
  record. *Accounted for.*
- **PlatformOnlineAchievements — `0022A770` calls `00316930`.** `0022A770` is cited only as a caller of the
  "any request active" test `00226BC0`; its call to an achievement-tagged function is main-loop work unrelated
  to the registry. *Irrelevant here, with the reason stated.*

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| 28 slots, bitset `01FD46D4`, two `0x18`-byte record arrays at `01FD4160` / `+0x2A0` | `00226BE0` (`00226BFD`–`00226C2E`), `00227680`'s `cmp r10d, 0x1b`, `00226280`'s slot walk | 1 | PROVEN |
| Start marks all managed actors and exempts by category | `00226BE0` read whole; `00263BE0`, `002647B0` | 1 | PROVEN |
| The apply ANDs all records and drives the listed globals | `00226280` read whole | 1 | PROVEN (the global callees are named only where another page names them) |
| Seven live sets, their pending words and hooks | `00226640`, `002269A0` read whole; transition tests at `00226720`–`0022672C`, `002267BB`–`002267C3`, `00226A0B` | 1 | PROVEN |
| Set 2 stops script execution; set 5 ~~drives animation rate~~ **fades the queued actors through fade channel 2** *(corrected 2026-09-19: the callee is the fade-channel forwarder, see the set-5 row of section 5)* | census readers `0025E230`, `0025E52C`; `002E8B10` → `00428940` | 1 | PROVEN (mechanism) |
| Every id's records (§3.1) | `00227680` read whole; run in isolation for ids 0–27 × flag 0/1 × stub 0/1 ([probe](../../_experiments/evidence/stop-registry-permission-records/probe.py), body sha256 `e50bed1d…`), static control at `0022792D` | 1 | PROVEN (records); the category meanings rest on the start's tests |
| Id owners | raw E8/E9 index of every start / cancel wrapper and direct call, id argument read at each site; verb names from the verb table | 1 | PROVEN |

## 9. Related

- [The world tick and the field frame](../Battle-Frame/the-world-tick-and-the-field-frame.md) — the frame this
  registry freezes, and the field hold whose ids 4 / 5 / 7 it carries
- [The field record table](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) §4 —
  the hold request's parameter byte
- [The UI request router](../../16-UI/Request-Router/ui-request-router.md) — the UI requests that raise ids 0, 2
  and 13
- [The battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) — flag bit 36 and
  `+0x004` bit 5
- [The capability inhibition policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) — a
  separate, per-capability policy the input words feed

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

| claim | measured |
|---|---|
| 28 slots of `0x18`, record A at `01FD4160`, record B at `+0x2A0` | **28 × 0x18 = 0x2A0 exactly** — the B array begins on the byte after the A array ends, so the layout closes with no gap and no overlap |
| the 28-slot bound `cmp r10d, 0x1b` in `00227680` | present, and **three times** — `0022773A`, `0022778A`, `002277CC` |
| **thirteen** start wrappers in `00227370`–`00227640` | **13 listed entries in the range, and all 13 call `00226BE0`** |
| the ids they carry: 10, 11, 12, 15, 16, 17, 18, 22, 23, 24, 25, 26, 27 | **exactly that set**, recovered from each wrapper's own instructions |
| **nine** direct (non-wrapper) callers | **22 call sites in total − 13 wrappers = 9**, in `00266D10` (×2), `00263480`, `0026A1D0`, `00263230`, `0026B980`, `00313DB0`, `002678C0`, `00254740` |

### The negative half survives an attempt to break it, and the attempt is the interesting part

§6 claims ids **1, 3, 8, 9, 14, 20, 21** have *"no start route of any kind"*. I tried to rebuild that
set mechanically and **got a different, wrong answer twice** — which is what makes the page's version
worth trusting.

**First attempt: zero ids, from 22 call sites.** The wrappers do not load the id as an immediate:

```asm
00227380  xor  edx, edx
00227398  lea  ecx, [rdx + 0x16]     ; ecx = 22
```

The id is a **displacement off a register the compiler has just zeroed**. A scan for `mov ecx, imm`
finds nothing at all — and "nothing" reads as "no start route" for *every* id. **A census that
returns zero for every case cannot test a negative**; had I reported it, all 28 ids would have looked
unreachable.

**Second attempt: too many.** With zero-tracking the wrappers resolve, but the census still says ids
**0, 2, 7 and 13** have no start site — four more than §6 claims. They are not missing; they are
**computed**:

- `00254740` passes an id from `00255290`'s map, so no literal appears at the call. §6 already
  bounds it: *"whose map `00255290` returns only −1, 0, 2 or 13"* — which is exactly how ids **0, 2
  and 13** are raised;
- `00263480(ctx, mode)` selects **4, 5 or 7** from its `mode` argument, and a linear scan sees only
  the arm it walks.

So the narrower set is the right one, and §6 reaches it the only way a negative like this can be
reached: **not by failing to find a caller, but by naming the map and bounding its returns**, then
checking that no `lea` takes the start's address and that the address occurs in data only inside
unwind records. That is a controlled negative; my two attempts were uncontrolled ones.

**Not claimed:** nothing here was executed or observed live. §4's bit numbers, §5's seven per-actor
sets and §3.1's twenty-eight records were not re-derived — this pass took the layout arithmetic, the
wrapper census and the negative that rests on it.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Gameplay — SERVICE.** A cited function calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15`.
- **Resource — SERVICE.** Cited functions call `ResourceTable_ResolveEntryByIndex` and three small Resource helpers (107 bytes twice, and 417 bytes).
- **CombatAI — MECHANICAL (SWE2-EC7-95, 5 edges).** `0031B760` — the flag-owner resolver this page cites inside `00312130` — is called by `00239040`, `003014C0`, `00301AD0`, `003087E0` and one more body on the CombatAI layer. Shared-resolver fan-in; no CombatAI relationship to the stop registry. Edge list from `edges.tsv` 2026-09-20.
- **Spawn_Encounter_Lifecycle — MECHANICAL (SWE2-EC7-95, 24 edges).** The same `0031B760` resolver is reached through 24 edges on the Spawn_Encounter_Lifecycle layer (`002350C0`, `00235360`, `002354F0`, `002355A0`, +20 more). Shared-resolver fan-in; no spawn relationship to the stop registry. Edge list from `edges.tsv` 2026-09-20.
- **Presentation — MECHANICAL (SWE2-EC7-160, 600 edges).** Batch-125's `0024DEE0`/`0024F240` name the registry helpers `00182B20`, `00375900`, `0018A330` and the `001D6F20`/`001D6EE0`/`001D6FA0`/`001D6E80` family; those helpers' callers on the Presentation layer (`00477B10`, `002512B0`, `003756B0`, `003AAxxx`, +596 more) dominate the pair. Shared-helper fan-in, not a registry responsibility.



**ActorEntity — MECHANICAL (SWE2-EC7-161, 177 edges).** `003D9E20` — the registry mode-flip this
page measured — calls `003588B0`/`002E7F70`/`003D8DA0`; the registry's subject set shares
ActorEntity-layer neighbours (`00225CD0` calls `00263FF0`/`00358940`/`00359B80` and is called by
`002630xx` there). Registry-to-actor fan-out is mechanical; no ownership either way.

**Input — MECHANICAL (SWE2-EC7-167, 66 edges).** Batch-132's `0024DA40` names the actor-accessor
ladder `00263FF0`/`00358940`/`003589B0`; those shared accessors are called from the Input layer
(`00226BE0`, `002E09A0` among 66 edges). Shared-accessor fan-in, not an input relationship of
the stop registry. Edge list from `edges_live.tsv` 2026-09-23.

**Movement — MECHANICAL (SWE2-EC7-167, 93 edges).** The same `0024DA40` accessor ladder —
`00263FF0`/`00263C30`/`00358940`/`003589B0` — is called from the Movement layer (`002E28E0`,
`00392740`, `002E5610`, `002EBFA0` among 93 edges). Shared-accessor fan-in; no movement
relationship to the stop registry.

**Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-167, 104 edges).** The `0024DA40` accessors
`00263FF0`/`00263C30`/`00358940`/`003589B0` carry the pair: script-bridge bodies `00352000`,
`0034AF50`, `0050D780`, `0034BB80` and ~100 more call the same shared accessors. Fan-in through
the actor-accessor ladder, not a bridge responsibility of the registry.

**World — MECHANICAL (SWE2-EC7-167, 9 edges).** `00358940` (`ActorManager_GetRecordByOrdinal`,
named in `0024DA40`'s ladder) is called by `0025E400`/`002623A0` on the World layer — shared
accessor fan-in, nothing World-side owned here.

- **Party — MECHANICAL (SWE2-EC7-170, 29 edges).** `00280B70` — the roster pump
  this page names as a `0035C750` caller — calls the Party-filed `003271D0` and
  `00327850` and sits in the pair's wider fan; the pump's own party reach, not a
  registry relationship. Edge list from `edges.tsv` 2026-09-22.
- **Story_Event_Quest_Hunt — MECHANICAL (SWE2-EC7-170, 1 edge).** `00253C70` —
  the input arbiter this page names as a `0035C750` caller — calls `0032A8A0` on
  the Story/Event/Quest/Hunt layer; the arbiter's own reach. Edge list from
  `edges.tsv` 2026-09-22.
- **UI — MECHANICAL (SWE2-EC7-170, 47 edges).** `00253C70` (called by five UI
  bodies including `00254B50`/`0028F970`/`003669D0`), `00280B70` (called by
  `00281ED0`) and the already-cited `0035C7B0` (`0027EFA0`/`0035C7A0`/`00254B40`)
  carry the pair — shared-helper fan-in to the arbiter and pump, no UI
  relationship to the registry. Edge list from `edges.tsv` 2026-09-22.
- **Audio — CLIENT and SERVICE (30 edges).** 9 inbound (Audio bodies `00210760`, `00229AF0`, `00229AB0` call page-cited `002DF370`, `001D6E80`, `001D6EE0`); 21 outbound (page-cited `003601D0`, `002628B0`, `00226280` call Audio bodies `002DF370`, `003636A0`, `0036F460`). Substantive edges include `00226280` calls `002DF370`; `00226BD0` is called by `00229AF0`; `0022A770` calls `0036F460`; `002407F0` calls `002DE110`; the remaining edges run through shared helpers the page cites.
- **CombatAction — CLIENT (10 edges).** 10 inbound (CombatAction bodies `00313DB0`, `BattleAction_ResolveSpecialSequenceTargets` (0030EC00), `00306010` call page-cited `ActorWork_GetBattleUnit` (0031B760), `ActorHandle_EncodeRegistryEntry` (003589B0), `PartyFocus_GetCurrentPackedActorHandle` (003590D0)). Substantive edges include `00225CD0` is called by `00313DB0`; `00226280` is called by `00313DB0`; `00226BE0` is called by `00313DB0`; the remaining edges run through shared helpers the page cites.
- **PlatformOnlineAchievements — CLIENT and SERVICE (4 edges).** 1 inbound (PlatformOnlineAchievements bodies `00316670` call page-cited `00316930`); 3 outbound (page-cited `00316930`, `0022A770` call PlatformOnlineAchievements bodies `00316930`, `00315E90`, `003162E0`). Substantive edges include `0022A770` calls `00316930`; `00316930` is called by `00316670`; `00316930` calls `00315E90`; `00316930` calls `003162E0`.
- **SaveLoad — CLIENT (1 edge).** 1 inbound (SaveLoad bodies `00280140` call page-cited `00252D90`). Substantive edges include `00252D90` is called by `00280140`.
- **Save_Load_Settings — CLIENT and SERVICE (6 edges).** 2 inbound (Save_Load_Settings bodies `SaveLoad_ControllerLifecycleHandler` (00582860), `SaveRuntime_InitializeHeaderAndImageBackedState` (00253A80) call page-cited `00182D40`, `002DDE60`); 4 outbound (page-cited `00253970`, `002628B0`, `00266D10` call Save_Load_Settings bodies `SaveImage_GetActiveRuntimeBuffer` (002EF640), `SaveImage_GetPersistentPayloadBase` (002EF2B0), `002EF2D0`). Substantive edges include `00182D40` is called by `SaveLoad_ControllerLifecycleHandler` (00582860); `00266D10` calls `002EF2D0`; `002DDE60` is called by `SaveRuntime_InitializeHeaderAndImageBackedState` (00253A80); `003601D0` calls `SaveImage_ClearActiveRuntimeBuffer` (002EF5F0); the remaining edges run through shared helpers the page cites.
- **PlatformOnlineAchievements — CLIENT and SERVICE (4 edges).** 1 inbound (PlatformOnlineAchievements bodies `00316670` call page-cited `00316930`); 3 outbound (page-cited `00316930`, `0022A770` call PlatformOnlineAchievements bodies `00316930`, `00315E90`, `003162E0`). Substantive edges include `0022A770` calls `00316930`; `00316930` is called by `00316670`; `00316930` calls `00315E90`; `00316930` calls `003162E0`.
- **Items — SERVICE (1 edge).** 1 outbound (page-cited `00236C30` call Items bodies `00238660`).
### Set 3's bit 24, fanned out (FABLE, 2026-09-16)

**BIT 24'S FANOUT READ FROM THE BODIES - 2026-09-16 (FABLE). The open effect is now two named fields in two named tables, not an unknown.** **It is read at four sites, and every one is a two-way select.** Three in `004213E0` and one in `00423B10`, all `test dword ptr [reg + 0x284], 0x1000000`. *(a)* `0042142F` - set means `ebx = 1` **without consulting `+0x6A4`**: the alternative branch calls `003E7D10([+0x6A4], 3)` and uses its result. **So bit 24 is an override that forces this condition true rather than a value that is tested alongside it.** *(b)* `004214BC` - set calls `004775E0(handle, 1)`, clear calls `004775E0(handle, 0)`. *(c)* `0042155C` - set gives `edx = 9`, clear `edx = 8`. *(d)* and `ebp`, derived from *(a)*, chooses `0051C380(entry, 9)` against `0051C380(entry, 8)` across the **four-entry array at `+0x438`**, releasing entries through `0051BC10` and storing `0xFFFF`. **AND 8-VERSUS-9 IS ONE BOOLEAN, FROM THE CALLEE.** `0051C380(h, v)` is 50 bytes: it indexes a **`0x3C0`-stride table at `02CA8420`**, validates `[r9] == h`, then computes `[r9+5]` as *(old AND (v >> 2)) OR (v AND 3)*. With **`v = 8`** that is *keep bit 1, clear bit 0*; with **`v = 9`**, *keep bit 1, set bit 0*. **The entire 8/9 distinction is bit 0 of `[record + 5]`.** **The other write lands in a table this database already documents.** `004775E0(h, v)` is 39 bytes: it indexes **`02CA6CA0`, 32 records of `0x40`**, validates `[r8+4] == h`, and stores **`word[r8+2] = v`**. That is the **packed channel table** whose decoder `004776D0` is read on [adm add-motion tables](../../17-Presentation-Rendering/Model-And-Motion-Formats/adm-add-motion-tables.md) - the decoder reads `word[r8+0]` and `byte[r8+0x10+i]`, and **`+2` is the neighbour nobody had attributed.** **So set 3's bit 24 is a single boolean fanned out to two runtime tables**: bit 0 of `[02CA8420 + h × 0x3C0 + 5]`, and `word[02CA6CA0 + h × 0x40 + 2]` set to 1 or 0. **The row's remaining question is what those two fields do**, which is a much smaller thing than *the on-screen effect of bit 24*. *What I did not read.* `00423B10` in full - only its one bit-24 test; `003E7D10`, the alternative that bit 24 overrides; and the **consumers** of either field. I have the writes and the tables, not the display path.

## The `00263230` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00263230` — the mode-1 `ActorResource_StartEntryScriptExecution`
path (`edx` vs 1, `00263230`): `dword[02099DB4]` / `byte[0209A2A8]`
gates (`0026324D`/`00263260`), `byte[rcx+0xC]` (`00263278`),
`00377700` (`00263283`), `00226BE0` with `4` (`002632AD`), the
`02099D70` swap to `02098E10` and restore (`002632B9`/`002632D8`),
`003590D0` → `003588B0` unit resolve (`002632C0`/`002632CB`),
`002E7600` on the unit (`002632F0`), then `byte[rsi+3]` vs 2,
`word[rsi]`, `r9 = 0x30B`, `byte[rsi+0x15]` into `002EBFA0`
(`00263309`–`00263323`).

| member | role | interior |
| --- | --- | --- |
| `002EAB80` (99 B) | object-kind gate — `byte[rcx+0x18]` vs 1 (`002EAB86`), `byte[rcx+3]` vs `0x60` (`002EAB95`), `rdi = [rcx+0xB8]`, `byte[rdi+0xDC]` check (`002EABA5`) | [`002EABA5`](../../_index/ADDRESS-INDEX.md) |
| `002627C0` (161 B) | script-entry helper — `r8 = rax` pass-through into the entry call (`002627C8`) | [`002627C8`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00377700`, `00226BE0`, `003590D0`,
`003588B0`, `002E7600`, `002EBFA0`. The `0x30B` literal is the
entry-script event id the page's mode-1 path names.

## The `002E2240` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`002E2240` (77 B) — the `0215F1DC` system-stop flag setter/clearer:
`ecx != 0` → `or dword[0215F1DC], 0x100203`, `ecx = 6`, `00229F00`,
tail `002274A0` (`002E2248`–`002E2260`); `ecx == 0` → `and
dword[0215F1DC], 0xFFEFFDFC` (clears exactly `0x100203`), `ecx = 2`,
`00229F00`, tail `00226140` (`002E2265`–`002E227D`).

| member | role | interior |
| --- | --- | --- |
| `00226140` (24 B) | `01FD46D4` bit `0x8000` gate → tail `00225CD0` (`00226140`–`00226152`) | [`00226140`](../../_index/ADDRESS-INDEX.md) |
| `002274A0` (53 B) | gated init — same `0x8000` gate (`002274A4`), `-1` stack writes (`002274B2`/`002274BD`), `00226BE0` (`002274CB`); twin shape of `002273E0` | [`002274CB`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00229F00`, `00225CD0`, `00226BE0`.
`0215F1DC` is the shared system-stop flag word; `01FD46D4` the shared
mode-flag cell.

## The `0025B500` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0025B500` (~120 B) — `byte[+0xC]` bit-6 clear then `byte[+0x15] * 0x288`
indexes the registry record (`0025B508`/`0025B515`).

| member | role | interior |
| --- | --- | --- |
| `00226100` (24 B) | flag-gated forward — `dword[01FD46D4] & 0x40000` → `00225CD0(edx = -1 + 0x13)`; clear → ret (`00226100`/`00226112`) | [`00226100`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00225CD0`.

## The `0026C3E0`/`0026C5D0` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`0026C3E0` (~25 B) — thin forward under a `rax = rsp` prologue.

| member | role | interior |
| --- | --- | --- |
| `00254FC0` | paired call — `0017E7D0()`, `0035DA80()`, tail `003C8990` (`00254FC4`/`00254FD2`) | [`00254FC4`](../../_index/ADDRESS-INDEX.md) |

`0026C5D0` (~170 B) — census body under a `rax = rsp` prologue.

| member | role | interior |
| --- | --- | --- |
| `0035A8D0` | zero-init walk — `esi = ecx`, `edi = 0` counter (`0035A8DF`/`0035A8E1`) | [`0035A8DF`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0017E7D0`, `0035DA80`, `003C8990`.

## The `0035C7B0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0035C7B0` (~62 B) — `dword[022C83E8] & 0x100` test
(`0035C7BA`/`0035C7C6`).

| member | role | interior |
| --- | --- | --- |
| `00227370` | `dword[01FD46D4] & 0x400000` gate, `-1` default write (`00227374`/`00227382`) | [`00227374`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-18 update (2026-05-15) — `002DDC30` registry-bit getter, split-head

`002DDC30` (16 B) is the Config/registry-bit reader this page names for SM-5 — a complete five-instruction getter: `rax = [0215E6E0]` (`002DDC30`), `eax = [rax]`, `eax >>= 3`, `eax &= 1` (`002DDC37`..`002DDC3C`), `ret` — it returns bit 3 of the `0215E6E0`-pointed options dword, no arguments consulted. 6 measured callers (`00225CD0`, `00225EB0`, `00227680`, `002403F0`, `00254740`, `00255290`) all reach it to gate on that stored option bit, consistent with this page's SM-5 reading (clear = Wait, set = Active).

## SWE2-EC7-33 update (2026-09-19) - `00423B10`

`00423B10` (**1,028 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,032 B, a wrong literal in the batch-33 append — the body is 1,028 B per the function list*) is the registry's record enumerator - `0020E600`/`0051B9E0`/`0041D790`/`00426FA0`/`00424C40`/`003AB7F0`/`002ED570`. Interior anchor `00423BB0` (an `0020E600` call).

## SWE2-EC7-34 update (2026-09-19) - `00477B10`

`00477B10` (889 B) is the stop-registry row accessor - `cl*64` row into `02CA6CA0`, `003E55B0`/`005047C0`/`00477E90`/`003A1FE0`/`00505150`/`0017F250`. Interior anchor `00477C1A` (an `003E55B0` call).

## SWE2-EC7-35 update (2026-09-19) - `0042C8F0`

`0042C8F0` (753 B) is a stop-registry record op - `022C6F28` registry, seven `0020E600` image-pointer resolves plus `003E5710`/`00477480`/`0042D830`/`00426220`/`00421120`. Interior anchor `0042C961` (a `0020E600` call).

## SWE2-EC7-37 update (2026-09-19) - `004778D0`

`004778D0` (571 B) is a system-stop registry body - `022C6F28`/`01F44830`/`02CA6CA0`, `003E55B0`/`005047C0`/`003A1FE0` pairs plus `00505150`/`00808C40`. Interior anchor `004779B0` (an `003E55B0` call).

## SWE2-EC7-39 update (2026-09-19) - `0024D770`

`0024D770` (431 B) is a system-stop body - `02092162`/`02092164`/`02092166`/`020926E4`/`02EBD480` fields, `003B0BF0`/`00254A70`/`002EF9F0`/`003B2CA0`. Interior anchor `0024D809` (a `003B0BF0` call).

## SWE2-EC7-40 update (2026-09-19) - `0051CC30`

*(Corrected 2026-09-19, FABLE: `0051CC30` is not a system-stop body. It is the constructor of a bone trail - it takes a
free entry of the sixteen-entry pool at `02CA8420`, copies an FCP section 4 descriptor into it and takes the first bone
sample; [bone trails](../../17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md). The registry's only
contact with the pool is that set 3 writes entry byte `+5`. The mechanical description below is accurate as a list of
what the body touches.)*

`0051CC30` (385 B) is a system-stop body - `022C6F28`/`02CA8400`/`02CA8404`/`02CA8408`/`02CA8410`/`02CA8420` fields, `00861EC0` triple plus `00422170`. Interior anchor `0051CCF6` (an `00861EC0` call).

## SWE2-EC7-43 update (2026-09-19) - `0042B970`

`0042B970` (283 B) is a time-stop-registry body - `0042E650`/`01F44830`/`022C6F28`, `00420EA0`/`00426220`/`0042EF90`/`00808C40`. Interior anchor `0042B9D0` (a `00420EA0` call).

## SWE2-EC7-43 update (2026-09-19) - `0042BA90`

`0042BA90` (283 B) is a time-stop-registry body - `0042E650`/`01F44830`/`022C6F28`, `00420EA0`/`00426220`/`0042EF90`/`00808C40`. Interior anchor `0042BAF0` (a `00420EA0` call).

## SWE2-EC7-44 update (2026-09-19) - `0051C270`

`0051C270` (265 B) is a body - `001837A0`/`00184140`/`0036A100`/`0036C140`/`0036C1D0`/`005409C0`. Interior anchor `0051C2B5` (an `001837A0` call).

## SWE2-EC7-54 update (2026-09-19) - `00424C40`

`00424C40` (309 B) is a time-stop registry body - `0020E600`/`0041C7C0`/`0041D110`/`0041D790`/`0041D7E0`/`0051B9E0` plus `01CEBC9C`. Interior anchor `00424C69` (a `0020E600` call).

## SWE2-EC7-56 update (2026-09-19) - `00505150`

`00505150` (231 B) is a call-free packed-record builder - `shl`/`or` dword packs into `rcx`/`r9` qwords, `+0x14`=`0x10000000`, `+0x18`=`0xE`, `+0x48`=`0x51` tag. Interior anchor `00505195` (the first `shl` pack).



## SWE2-EC7-64 update (2026-09-19) - `00421120`

`00421120` (142 B) is a stop-registry record op - `0020E600`/`002ED570` plus `022C6F28`. Interior anchor `00421188` (a `0020E600` call).



## SWE2-EC7-65 update (2026-09-19) - `0041C7C0`

`0041C7C0` (137 B) is a call-free float quantizer - `ucomiss`, `movss [rdx+0x14]`, `cvttss2si`/`cvtdq2ps` round-trip, `r10d=0x400` stride, `008F8D80`/`01DFE0BC`. Interior anchor `0041C7F5` (the `movss [rdx+0x14]` store).


## SWE2-EC7-68 update (2026-09-19) - `003A1FE0` registry block quantizer

`003A1FE0` (50 B) is the block-count quantizer the registry row
accessors (`00477B10`/`004778D0`) call: `edx <= 0x2C` with bit
`edx` of `0x101008180000` set returns
`((ecx + 0x7F) & ~0x7F) sar 6` - the 128-rounded count over 64;
every other `edx` returns the signed-rounding `(ecx + 0x3F) sar 6`
sequence (`cdq`/`&0x3F`/add/`sar`) - the plain 64-ceiling. The
bitmask flags the coarse rows: bits 0x13, 0x17, 0x1F, 0x20 and
0x28 of the constant. Call-free. Interior anchor `003A1FEF` (the
`bt` select).

## SWE2-EC7-72 update (2026-09-19) - `00420EA0` two-record flag mirror measured

`00420EA0` (126 B) is the flag mirror the stop-registry bodies call:
`edx` sets or clears `+0x284` bit `0x18`; `00422D50(rcx)` and
`00422D10(rcx)` each resolve a sub-record whose `+0xC` is cleared of
bit 18 then OR'd `0x40000` iff `edx` was truthy (the `neg`/`sbb`/
`and 0x40000` idiom), and the body tails `004213E0(rcx, 0)` - the
three-place mirror of one flag.
Interior anchor `00420ED3` (the first `+0xC` mask).

## SWE2-EC7-81 update (2026-09-20) - `005047C0` indexed record lookup measured

`005047C0` (49 B) is the `+0x100`-indexed fetch the registry callers
run: `word[rcx + rdx*2 + 0x100]` selects the id, `005212E0` resolves
it, and a live record whose `byte[+0x1C]` bit0 is set returns
`[rax+0x14] >> 8` - anything else returns 0.
Interior anchor `005047CF` (the `005212E0` resolve call).

## SWE2-EC7-83 update (2026-09-20) - `0042D830` record-apply measured

`0042D830` (122 B, stack-cookie) is the `+0x288`-gated apply the
registry callers run: when `dword[rcx+0x288] != -1`, `004210D0`
testing true runs `00420FB0` then `003B33A0([+0x288], eax)`; either
way `003E5710(rcx, &stack)` fills the frame before
`003B3AA0([+0x288], &stack)` and `003B3080([+0x288])` commit it.
Interior anchor `0042D877` (the `003E5710` call).

## SWE2-EC7-84 update (2026-09-20) - `00422D10` + `00421010` measured

`00422D10` (57 B) is the `+0xC8`-gated tail the registry callers
run: `[rcx+0xC8]` != -1 forwards `0020E600([rcx+0x10])`'s
`[rax+0xDA8]` field plus the stored index into `0051B9E0` - else 0.
Interior anchor `00422D2D` (the `0020E600` call).

`00421010` (29 B) is the bit-3 setter the same callers run: `edx == 1`
sets bit 3 of `+0x284`, anything else clears it - call-free.
Interior anchor `00421015` (the `or` arm).

## SWE2-EC7-86 update (2026-09-20) - `003E7C70` two-arm enable toggle measured

`003E7C70` (71 B) is the flag-split enable/disable the registry
callers run: `[02B59D71] = cl`; the set arm runs
`003ACA80(0x20)`, `003AC8F0(0)` and tails `003E0B40(1)`; the
clear arm runs `003ACA90(0x20)`, `003AC8F0(1)` and tails
`003E0B40(0)` - mirrored triples on either side of the flag.
Interior anchor `003E7C83` (the enable-arm `003ACA80` call).

## SWE2-EC7-87 update (2026-09-20) - `003ACA80` + `003E4140` measured

`003ACA80` (7 B) is the flag-OR the `003E7C70` toggle and the other
registry callers run: `cl` is OR-ed straight into
`byte[02B3F501]` and the body returns - the whole helper is one
global-flag merge.
Interior anchor `003ACA86` (the `ret`).

`003E4140` (169 B) is the three-slot scalar apply the registry
callers run: each of `[rbx]`, `[rbx+0x20]`, `[rbx+0x18]` is a
handle resolved twice through `0020E600` (existence, then the
object) and receives `004158F0(rec, (xmm1+xmm2+xmm3)*const
00D117B4)`, `005175B0(rec, xmm3)`, and `004717D0(rec, xmm2)`
respectively, each arm skipped on a null resolve.
Interior anchor `003E418D` (the `004158F0` call).

## SWE2-EC7-89 update (2026-09-20) - `003B6900` flag-byte merge measured

`003B6900` (43 B) is the keyed flag merge the stop-registry
callers run: `ecx` selects the 0xE0-stride slot in `[02B40528]`,
and when `dword[+0x10]` matches, `byte[+0x41]` becomes
`(edx & 3) | (old & (edx >> 2))` - a two-field merge into the
slot's flag byte.
Interior anchor `003B6918` (the merge sequence).

## SWE2-EC7-90 update (2026-09-20) - `003B0BF0` keyed slot lookup measured

`003B0BF0` (54 B) is the keyed lookup the stop-registry callers
run: the 36-slot `02EBEC00` table (0x18 stride) is scanned for
a `dword` matching `ecx` - returning the slot pointer, or 0 on
a miss.
Interior anchor `003B0C1B` (the matched arm).

## SWE2-EC7-93 update (2026-09-20) - `00373030` resolve-and-tail measured

`00373030` (40 B) is the forwarder the `0042C410`/`0042C8F0` stop-list
callers use: `[rcx+0x84]` resolves through `0020E600`, then the body
tails `0046D100` with `rax + 0x1F0` as the record and the original
`rdx` preserved.
Interior anchor `0037303F` (the `0020E600` call).

## SWE2-EC7-95 update (2026-09-20) - `00312130` measured

`00312130` (60 B) is the `0x1000000000` flag write `00226640`,
`00226AB0` and `00263560` run: `0031B760` resolves the flag
qword's owner, `edx == 0` ORs the bit in, nonzero ANDs
`~0x1000000000` - the arm/clear pair the stop registry toggles.
Interior anchor `00312138` (the `0031B760` call).

## SWE2-EC7-97 update (2026-09-20) - `002E92F0` measured

`002E92F0` (97 B) is the validated dispatch `00226640` and
`002E28E0` call: `00264DC0(rcx)` folds to `edx = (eax == 0)`,
then the usual `[+0xC0]` word idiom resolves the `0x740` record
and `[+0x284] != 0` admits a tail `jmp 00428FE0` - the
predicate-plus-resolve the stop registry's write path runs.
Interior anchor `002E92F9` (the `00264DC0` call).

## SWE2-EC7-104 update (2026-09-20) - `0026A770` measured

`0026A770` (65 B) is the two-bit flag write
`0035A720`, `0035A7A0` and `0035A8D0` call on
`[rcx + 0xC0]` records: bit 1 of
`byte[rec + 0x154]` takes `(edx != 0)`, bit 0
takes `(r8d != 0)` - a paired enable/disable
publish, skipped entirely when the record
pointer is null.
Interior anchor `0026A77C` (the bit-1
clear).

## SWE2-EC7-106 update (2026-09-20) - `00249840` measured

`00249840` (24 B) is the
three-pointer clear `00253970` and
`002D6F90` call: qwords `02F973A0`,
`02F973A8` and `02F973B0` are zeroed
- the contiguous head reset every
subsystem runs when it publishes its
stop record.
Interior anchor `00249849` (the
second qword clear).

## SWE2-EC7-108 update (2026-09-20) - `00226AB0` + `00226A50` measured

`00226AB0` (91 B) and `00226A50`
(89 B) are the pending-mask fold
twins `0035A720`, `0035A7A0` and
`0035A8D0` run: `00359B80()`
resolves the record - null
returns early - then the
`+0x50`/`+0x4C` set-mask is OR'd
into the `+0x48`/`+0x44` live word
and cleared, the `+0x5C`/`+0x58`
clear-mask is AND'd out and
cleared, and the nonzero result
(`byte[rbx + 9] & 0x20` forcing it
armed) feeds the tail call -
`00226AB0` passes it inverted to
`00312130`, `00226A50` passes it
raw to `00238B40` - the
set/clear-publish pair the
stop-registry arms share.
Interior anchors `00226ACE` and
`00226A6E` (the two `or` folds).

`004158F0` (389 B) is the per-slot worker the three-slot scalar apply `003E4140` and the loader helper `0054B1F0` call: `[rcx+0x10]` is compared against `xmm1` and replaced, `1.0/xmm1` lands at `+0x14`, then a `byte[rdi+4]`-bounded loop over the `[rax+4]` element array runs `0020E600` x5 to re-resolve each record - the registry scalar's reciprocal-publishing setter.

Interior anchor `0041592E` (function `004158F0`).

`0024EF90` (683 B) is the five-field record parser the boot primer `0024C970` runs: `001D6F20`, `00861EC0` x2, `001D6EE0`, `0036A100`, `001D6FA0`, `001D6E80` open the buffer, then comma/CR splitting counts exactly five fields into `rbp+0xF` buffers, CRT calls, `0018A330` x2 and `003697F0` on `02F93340` under the cookie check - the boot table's delimited-line reader.

Interior anchor `0024EFC2` (function `0024EF90`).

`0024DEE0` (385 B) is the gated action `0024D540` calls: `020926E4 & 6` must be set and `ecx` must be 0; `(020926E4 >> 1) & 3` picks the arm - value 1 builds an `00861EC0` frame, runs `00182B20` and `00375900` twice, value 2 takes the second path, anything else returns - the registry's mode-gated stop action.

Interior anchor `0024DF4B` (function `0024DEE0`).

`0024F240` (384 B) is the entry builder `0024C970` calls: `001D6F20(rcx, 1)` resolves the slot, `001D6EE0` counts it, `0036A100(ebx + 2)` allocates, `001D6FA0`/`001D6E80` populate, `0018A330` twice publishes, `003697F0` releases - the registry's counted insert.

Interior anchor `0024F261` (function `0024F240`).

`003D9E20` (378 B) is the mode toggle `00259990` calls: `00252E50` latches `al` into `02B4E4A5`, zeroes `02B4E4A6`/`02B4E4A4`, `00252E30` refreshes, then `02B4E4A0 != eax` selects `ecx = 1|2` via `cmovne` and `003588B0`/`002E7F70`/`003D8DA0` run the transition - the registry's armed-mode flip.

Interior anchor `003D9E39` (function `003D9E20`).

`0051D2F0` (17 B) is the two-bit merge `00421280`/`004213E0` call: `byte[rcx + 7] = ((edx >> 2) & byte[rcx + 7]) | (edx & 3)` - the registry's smallest flag write, keeping the high bits and splicing in the low pair.

Interior anchor `0051D2F8` (function `0051D2F0`).

`0024DA40` (314 B) is the `020926E4`-gated pump `0024D540` calls: always writes `020926C0` = `(1.0f, 1.0f)` (movaps from `00900320`); when `byte[020926E4]&0x80` it loops `esi` over `00263FF0`/`00263C30` pairs, then `00358940` -> `003589B0` -> `002E9B80` resolve a word index (`-1`/`0xFFFF` skip), `sx(ax)*0x740 + 022C6F28` live-checks the record (`dword[+0x284]`), and the tail writes through `rcx` - the stop-registry's gated effect-record refresh beside `0024DEE0`/`0024B7B0`.

Interior anchor `0024DA82` (function `0024DA40`).

`0035C750` (13 B) is the bit-4 getter on the request word `022C83E8` - `eax = (dword >> 4) & 1`, the single-flag sibling of `0035C7B0`'s `& 0x100` test: the input arbiter `00253C70` and `00280B70`'s fail arm consult it before touching the party roster - the request-word read that reports whether the held-stop class is active.

Interior anchor `0035C756` (function `0035C750`).

`0035C750` (13 B) is the bit-4 getter on the request word `022C83E8` - `eax = (dword >> 4) & 1`, the single-flag sibling of `0035C7B0`'s `& 0x100` test: the input arbiter `00253C70` and `00280B70`'s fail arm consult it before touching the party roster - the request-word read that reports whether the held-stop class is active.

Interior anchor `0035C756` (function `0035C750`).

`004233D0` (209 B) is the `@FRM` section walker `00423B10` calls: `0020E600`/`003AB7F0` resolve the `+0x42C` owner, `00408F90` finds the `0x4D524640` tag and `00408F80` returns the `+0x30` section; `edx & 0xFFF < 0x100` returns the index directly, otherwise the section's `[+4]`-sized `0xFFFF`-terminated u16 list is walked - the registered-stop record lookup

Interior anchor `004233EF` (function `004233D0`).

`0041D790` (74 B) is the emit-and-clear helper `00423FC0` and `00424C40` run on the registry record: it sets `or [rcx+0xC], 0x10000000`, and when `[rcx+0x344]` differs from `1.0f` calls `0041D820(rcx, 1)`; either way it then clears the bit (`and [rbx+0xC], ~0x10000000`), stores `word [rbx+0x24] = 1`, and returns - a one-shot publish that always ends the same way

Interior anchor `0041D79A` (function `0041D790`).

`0041D7E0` (60 B) is the float-triple commit `00424870`, `00424A40`, `00424C40` and batch-164's `004253D0` call: stores `xmm1`/`xmm2`/`xmm3` into `[rcx+0x344]`/`+0x348`/`+0x34C`, then when both `xmm1` and `xmm3` differ from `-1.0f` and `xmm1 > xmm3` it rewrites `[+0x344]` with `xmm3` - a store-all-three plus a conditional min-clamp on the first lane.

Interior anchor `0041D813` (function `0041D7E0`).

`0035A590` (140 B) is the member-release sibling of this registry's `0035A7A0` time-stop sweep, called from `00359A30`/`0035AB20`: `00263FF0` fetches the manager, `00358940` walks the `+0x1D6` entry range, and each populated record's `+0x30` payload is torn down through `0026D6D0`/`00233F50`/`002ED020` with `002E97B0`/`00269D60`/`0026A770`/`00226AB0`/`00226A50` finishing the record state - the release pass the actor storage runs beside its freeze sweep.

Interior anchor `0035A5DA` (function `0035A590`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`timestop_interior.py`](../../_index/candidates/opus-timestop-interior-1001/timestop_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017F250` | 16 B | for a non-null `rcx`, tail-calls its virtual `+0x90` | `0017F253`, `0017F255`, `0017F258` |
| `00229AB0` | 32 B | tail-calls `002DF370(0x3F, 1, 1)` when `ecx` is non-zero, else `002DF370(0x3F, 0, 0)` | `00229AB2`, `00229AC1`, `00229ACB` |
| `00238850` | 36 B | calls `003846F0(0208E680, sign-extended ecx, 0)`, then tail-calls `00236C30(1)` | `0023885A`, `00238861`, `0023886F` |
| `002544C0` | 59 B | looks up `00255290(ecx AND 0x7FFF)`; a non-negative result tail-calls `00225CD0(result, -1)`; a negative one tail-calls `002260A0` when `ecx` is 11 and otherwise returns | `002544C8`, `002544CE`, `002544E1`, `002544E6`, `002544F0` |
| `002547C0` | 12 B | stores `cx` in word `01E0C2B0` (its entry instruction), then tail-jumps to `003BBF90` | `002547C7` |
| `00264DC0` | 37 B | returns 1 when qword `+0xC0` is non-null and both bit 0 of byte `+0x13` and dword `+0x170` of the `+0xC0` object are 0, else 0 | `00264DC7`, `00264DD0`, `00264DD3`, `00264DDE` |
| `0026B980` | 70 B | calls `00226BE0(6, 0, 0, 0, ecx, flag)`, where flag is 1 when `edx` is 0, 0 when `edx` is positive, and for a negative `edx` 1 when `00377700()` is non-zero | `0026B992`, `0026B9A0`, `0026B9B3`, `0026B9B6` |
| `002DF640` | 25 B | when `ecx` is -1, stores `r8d` in dword `01E0CF98` (through a compare and `cmovne` that store `r8d` either way) | `002DF645`, `002DF64E`, `002DF652` |
| `002E06B0` | 51 B | calls `0029D210(1)` and `00226160`, clears bits 0, 1, 9 and 20 of dword `0215F1D0`, calls `00267D40(1, 0)` and clears byte `0215F1B2` | `002E06B9`, `002E06BE`, `002E06C3`, `002E06D2`, `002E06D7` |
| `002E2400` | 55 B | calls `0029D210(ecx != 0)` and `00226160`, clears bits 0, 1, 9 and 20 of dword `0215F1D0`, calls `00267D40(1, 0)` and clears byte `0215F1B2` | `002E2408`, `002E240D`, `002E2417`, `002E2426`, `002E242B` |
| `002E2440` | 65 B | calls `0029D290(m)`, m being (`ecx` != 0) plus 0x10 when `edx` is non-zero, then `002274E0`; sets bits 0, 1, 9 and 20 of dword `0215F1D0`, calls `00267D40(1, 1)` and sets byte `0215F1B2` to 1 | `002E2448`, `002E2452`, `002E2455`, `002E245F`, `002E2475` |
| `002E24C0` | 29 B | sets bit `ecx` of byte `0215F1B3`, then tail-jumps to `00404D70` when the byte is non-zero, else to `00404DC0` | `002E24C7`, `002E24CA`, `002E24D2`, `002E24D8` |
| `002E24E0` | 29 B | clears bit `ecx` of byte `0215F1B3`, then tail-jumps to `00404D70` when the byte is still non-zero, else to `00404DC0` | `002E24E7`, `002E24EA`, `002E24F2`, `002E24F8` |
| `0034BB80` | 67 B | tail-calls `0026B4E0(rcx, 00320790(003589B0(00263F10(00264010(00267E10(r9)))), 1))` | `0034BB8C`, `0034BB93`, `0034BBA3`, `0034BBAF`, `0034BBBE` |
| `00352000` | 31 B | tail-calls `0026C5D0(00263FF0(00267E10(r9)))` | `00352007`, `0035200E`, `0035201A` |
| `0035A720` | 118 B | with `edx` 0: sets bit 5 of byte `+9` and, when qword `+0x30` is non-null, calls `00233F50(rcx, 1)`, `002ED020` and `0026D6D0`; with `edx` non-zero: clears that bit, calls `00269D60(it, 0, 0)` on `002E97B0()` when that is non-null with dword `+0` not -1, then `0026A770(rcx, 0, 0)`; in both cases then calls `00226AB0` and tail-calls `00226A50` | `0035A72D`, `0035A73D`, `0035A754`, `0035A77C`, `0035A791` |
| `0035B4B0` | 91 B | ORs `cl` into dword `02EC0B40`, then, among the 32 entries of 0x20 bytes from `02EC0B81`, sets byte `+0` to 3 where it is 2 and byte `+0x1B` shares a bit with `cl` | `0035B4BA`, `0035B4C7`, `0035B4CC`, `0035B4D1`, `0035B501` |
| `0035B510` | 60 B | clears the bits of `cl` in dword `02EC0B40`, then sets back to 2 every byte `+0` that is 3 among the 32 entries of 0x20 bytes from `02EC0B81` (whatever `cl` was) | `0035B51A`, `0035B51C`, `0035B530`, `0035B536`, `0035B542` |
| `003756B0` | 578 B | zeroes a 0x60-byte and a 0x58-byte stack descriptor (`00861EC0`); returns 0 when qword `02ADB6D0` is null or dword `02ADB6D8` is not 1 to 4. Otherwise it fills the first descriptor with byte fields, `00182B20()`, `sil` and a qword of bit fields whose mode bits depend on `02ADB6D8` (values 3 and 4 also store the addresses `02ADB720` and `02ADB6E0`), packs the low nibbles of `002D8150(0x200)` and `002D8150(0x1C0)` into that qword, stores `00182B20(02ADB6D0)`, and stores `00375900` of the descriptor in dword `02EC07F4`; it fills the second descriptor (the 16 bytes at `009155F0`, `r14d` times 1/255 (`00D11104`) as a float, `sil`, the same qword), stores `00375900` of it in dword `02EC07F8` and returns 1 | `003756F4`, `0037575A`, `0037577C`, `00375857`, `003758C2` |
| `003D9930` | 21 B | copies dword `+0x64` to `+0x3CC`, then tail-jumps to `0032AEC0(rcx + 0x2B0)` | `003D9933`, `003D9939`, `003D9940` |
| `0041D110` | 101 B | calls `0041CFC0`, clears bit 12 of qword `+0x2C8`, sets bit 28 of dword `+0xC`, calls `0041D820` (`r8d` = 1, float `+0x344` in `xmm1`) unless that float is -1.0 (`01CEBC9C`), then clears bit 28 and stores 1 in word `+0x24` | `0041D11D`, `0041D12E`, `0041D13A`, `0041D15A`, `0041D166` |
| `00424A40` | 510 B | when bit 20 of dword `+0x284` is set or `xmm1` is 0.0: calls `00426FA0`, sets bit 1 of dword `+0xC` of the `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC8)` record and calls `0041D790` on it when it exists, and returns `00424C40(rcx)`. Otherwise it returns 0 when the record for dword `+0xC4` exists with word `+0x24` = 1. Else, for that record: calls `0041D7E0` with floats `+0x2B0`, `+0x2B4` and `+0x2B8` and sets the three to -1.0; then calls `0041D790` (after setting bit 1 of its `+0xC` and its word `+0x24` to 1) or `0041D110`; stores 1.0 / `xmm1` in its float `+0x354`; sets bit 11 of its `+0xC` (and bit 17 when `r8d` is 1); clears bit 8 when its float `+0x344` is -1.0. It always ends with `00423AB0(rcx)` on float `+0x2BC`, returning 1 when the record existed, else 0 | `00424A56`, `00424A98`, `00424B29`, `00424B8A`, `00424BE5` |
| `0042E650` | 51 B | calls `00420EA0(rcx, dword +0x38 of rdx)` when `00426220(rcx, qword +8 of rdx)` returns 0 | `0042E660`, `0042E664`, `0042E66D`, `0042E673` |
| `00477E90` | 76 B | for `cx` not -1, takes the 0x740-byte record (signed `cx`) of `[022C6F28]`; when its dword `+0x284` is non-zero and `003E55B0(record)` returns an object, tail-calls `00504800(object, edx)`; otherwise returns 0 | `00477EAA`, `00477EBA`, `00477EC3`, `00477ED7`, `00477E9E` |
| `0051CC10` | 26 B | clears byte `+4` of record `cl` of the 0x3C0-byte records at `[02CA8420]` when its dword `+0` equals `ecx` | `0051CC13`, `0051CC1A`, `0051CC21`, `0051CC25` |
| `0051CDC0` | 27 B | stores `xmm1` in float `+8` of record `cl` of the 0x3C0-byte records at `[02CA8420]` when its dword `+0` equals `ecx` | `0051CDC3`, `0051CDCA`, `0051CDD1`, `0051CDD5` |

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-time-stop-and-system-stop-registry-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002F18D0` | 121 B | computes n = dword `+4` of `rcx` plus dword `01DFE0B4` and v = (n minus the integer dword `+0`, as floats) / n * 255 (`008C5B40`); when byte `+0x28` has bit `0x4` set it first calls `003587B0(1)` and `00374D40(0, dword +0x38, 2)`; then calls `003756B0(dword +0x30, v truncated)` and tail-jumps to `00182610(1)` | `002F18DC`, `002F1905`, `002F1924`, `002F1930`, `002F1944` |
| `00344120` | 32 B | calls `002ECE00(rdx, 0)` and then tail-jumps to `002ED020(rdx)`, passing its second argument as the first argument of both | `00344129`, `0034412E`, `0034413B` |
| `0034E530` | 66 B | calls `00267E10(r9)` twice, keeping the first result as a and passing the second to `00359CA0(second, 1, 1)`, then tail-jumps to `0035A720` with that result and a | `0034E540`, `0034E54A`, `0034E559`, `0034E56D` |
| `003531A0` | 51 B | calls `00267E10(r9)` (its result unused), `002E2440(1, 0)` and `002E1C40(0, 3)`, then tail-jumps to `002E1C70(1, 3)` | `003531A7`, `003531B1`, `003531BD`, `003531CE` |
| `003535F0` | 53 B | calls `00267E10(r9)` (its result unused), `002E2440(1, 1)` and `002E1C40(0, 3)`, then tail-jumps to `002E1C70(1, 3)` | `003535F7`, `00353603`, `0035360F`, `00353620` |
| `00353A60` | 52 B | calls `00267E10(r9)` (its result unused), `002E2400` with `ecx` = 1 and `002E1C40(1, 3)`, then tail-jumps to `002E1C70(1, 3)` | `00353A67`, `00353A71`, `00353A7E`, `00353A8F` |
| `00354300` | 106 B | when `00267310(byte [rdx+0x15])` is non-zero calls `00267E10(r9)`, `002E2440(1, 1)` and `002E1C40(0, 3)` and tail-jumps to `002E1C70(1, 3)`; when it is 0 calls `00267E10(r9)` and `002E2440(0, 1)` and tail-jumps to `002E1C40(0, 3)` | `0035430D`, `00354317`, `00354325`, `00354343`, `00354354` |
| `00354800` | 101 B | when `00267310(byte [rdx+0x15])` is non-zero calls `00267E10(r9)`, `002E2400` with `ecx` = 1 and `002E1C40(1, 3)` and tail-jumps to `002E1C70(1, 3)`; when it is 0 calls `00267E10(r9)` and `002E2400` with `ecx` = 0 and tail-jumps to `002E1C40(1, 3)` | `0035480D`, `00354817`, `00354823`, `00354842`, `0035484E` |
| `0042D740` | 88 B | calls `003E55B0` with the incoming `rcx` and `rdx` and, when it returns a record, copies bit 0 of dword `+0x5C` of `rdx` into bit `0x10` of the record's dword `+0x244`, bit 0 of dword `+0x60` into bit `0x20` of the same dword, and byte `+0x8C` of `rdx` to byte `+0xBC` of the record | `0042D749`, `0042D765`, `0042D77E`, `0042D78B` |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; move drafted by OPUS)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `4522aeff6`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged except where `moves.json` records a bits-as-values edit. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../../_index/candidates/opus-fable-home-host-moves-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `00198730` | 18 B | `00182D60` + 0x10 | when bit `0x1` of byte `+0x3A` of `rcx` is set, sets byte `+0x3B` to 1 and clears that bit (AND `0xFE`); otherwise returns without work | Interior anchor `00198734`; Interior anchor `00198736`; Interior anchor `00198738`; Interior anchor `0019873A`; Interior anchor `0019873E` | [the-actor-storage-record-field-map](../../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md) |
| `00363B00` | 31 B | `0026C5D0` + 0x174 | stores `cl` into byte `022CBA9A`; when `ecx` is 1 it also copies the 16 bytes at `rdx` to `022CBB10` and the float in `xmm2` to dword `022CBAAC` | Interior anchor `00363B06`; Interior anchor `00363B0B`; Interior anchor `00363B0E`; Interior anchor `00363B16` | [when-a-group-is-wiped-and-when-it-comes-back](../../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-the-time-stop-and-system-stop-registry-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `001986B0` | 18 B | `00182CF0` + 0x10 | reads byte `+0x3A` of `rcx`; when its bit 0 is clear, stores 1 to byte `+0x3B` and writes byte `+0x3A` back with bit 0 set (OR 1); when bit 0 is already set it changes nothing | Interior anchor `001986B4`; Interior anchor `001986B8`; Interior anchor `001986BA`; Interior anchor `001986BE` |
| `002FD060` | 43 B | `0024BFD0` + 0x67 | walks the list headed by qword `02EC3D60` through qword `+0x28` of each node until a null link (returning at once when the head is null), and for every node whose qword `+0x10` is non-null clears bit `0x4` of word `+0x368` of that object (AND `0xFFFB`) | Interior anchor `002FD067`; Interior anchor `002FD071`; Interior anchor `002FD07A`; Interior anchor `002FD081`; Interior anchor `002FD088` |
| `003B1000` | 68 B | `0024BFD0` + 0x6C | walks up to 36 (`0x24`) records of stride `0x18` whose qword field starts at `02EBEC08`, stopping at the first record whose dword 8 bytes before that qword is 0; for each record whose qword is non-null and whose pointee's word `+0x368` has bit `0x4` set, writes that word back with the bit cleared (AND `0xFFFB`) | Interior anchor `003B1010`; Interior anchor `003B1026`; Interior anchor `003B1030`; Interior anchor `003B103A`; Interior anchor `003B103E` |
| `003C8B20` | 34 B | `00252E30` + 0x0 | returns dword `+0xC8` of qword `02B47730` when that pointer is non-null and bit `0x4` of its byte `+0xC0` is set; returns 0 when the pointer is null or the bit is clear | Interior anchor `003C8B27`; Interior anchor `003C8B2C`; Interior anchor `003C8B35`; Interior anchor `003C8B3F` |
| `003C9590` | 33 B | `00252E50` + 0x0 | returns 1 when qword `02B47730` is non-null, bit `0x4` of its byte `+0xC0` is set and its dword `+0xC8` is non-zero (`setne`); returns 0 otherwise | Interior anchor `003C9599`; Interior anchor `003C959E`; Interior anchor `003C95A7`; Interior anchor `003C95AD` |
