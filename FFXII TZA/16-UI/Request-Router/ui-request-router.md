---
system: Native UI request router
category: 16-UI
status: DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): UQ-162 answered 2026-09-25 (7-9, 13, 16 and 20 have no screen in the image; 12 is the spattack window) (UQ-162 history: 17 the Strahl boarding menu and 22 the map screen named 2026-09-18 from the field scripts, 6 and 10 confirmed; 15 the airship-route map, 17 and 18 further world-map kinds and 19 the hunt list named 2026-09-25 from the code and the shipped text); the state block's owner (UQ-163, a text-draw state embedded in the caption and message widgets or on the text helpers' stacks) answered 2026-09-17
owner_layer: PrimaryOwner:UI
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites `002ABB20`, `003BA7B0`; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  previous_parent: 381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: reverification-against-current-parent
  crossref_clean: true
  reopened_count: 1
---

# Native UI request router

> One numeric mailbox for "open this screen / start this UI operation", with a gameplay
> policy refusal gate in front of it.

~~**Status is PARTIAL:**~~ **Status is DOCUMENTED** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, owner re-status 2026-10-01)*: the mechanism is fully documented; several request IDs have no
recovered player-facing name and are deliberately left numeric.
*Note 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13): every id now has an identity or a ruling (UQ-162, answered
2026-09-25). 7, 8, 9, 13, 14, 16, 20 and 21 are unused request numbers. What is still not read is the game-over
screen's wording (request 11) and the `spattack` window's title (request 12); see §7b.* *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: the game-over wording is read since, §7c P1: the image `gameover_c.tm2`, which reads GAME OVER. The `spattack` window's title is runtime-only and is proposed as register row Q1 in [batch 20's record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md).)*

## 1. What the player sees

Pressing Triangle opens the Party Menu. Pressing the confirm button or Square opens the
Battle Menu. Up/Down changes party leader, Left/Right cycles targets. Scripts can open
fullscreen menus during events. All of it goes through the same numeric request system, and
all of it can be refused by the gameplay capability policy.

## 2. Native mechanism

`00254B50` is the router:

1. normalise `requestId = ECX & 0x7FFF`;
2. rebuild the inhibited-request mask from `002E0FA0` and the policy table `01E0C2C0`;
3. test the requested bit with `BT`;
4. if inhibited, **return failure without dispatch**;
5. otherwise dispatch through a native switch: ids `1`, `3`, `4`, `5`, `12`, `24` to five special routes, **everything else — the other eighteen in `1..24` and every value outside it — to the generic scheduler** (`0028F970` then `00280A00`, which receives the *original* request dword, `00254C2D`–`00254C39`; corrected 2026-09-11).

A separate deferred **request mailbox** (`002E1B10`) carries requests raised from input:
refuse if the mailbox is unavailable/busy, special-case request 2 against aggregate policy
bit 0, set the pending flag, store ID and parameter.

### Dispatch table

| Request | Route | Request | Route |
|---:|---|---:|---|
| 1 | `0035D660` open-gate route | 12 | `0028E970` |
| 2 | `00280A00` generic | 13-23 | `00280A00` generic |
| 3 | `0035D980` | 24 | `0035D080` |
| 4 | `0035D660` — **the same battle-menu open as request 1** (2026-09-12: both reach `0028FD50`, which the UI tick turns into the `0x61F0` battle menu widget; the request id is passed to it) | | |
| 5 | `003C87B0` | | |
| 6-11 | `00280A00` generic | | |

### Identified requests

| ID | Identity | Confidence |
|---:|---|---|
| 1 | Battle Menu open | proven - triggered by configured Decide mask `01E0C2A0` or raw `0x8000` (Square) |
| 2 | Party Menu / Menu Screen family | strong - triggered by raw pad mask `0x1000` (Triangle) with parameter 0 |
| 3 | Field party-leader selection | proven - D-pad Up/Down `0x10 \| 0x40`, needs >= 2 eligible candidates, commits via `0035BAA0` |
| 4 | Battle Menu open by the same route as request 1 (`0035D660`) | proven 2026-09-18 (FABLE); UQ-162 |
| 5 | Field free-target actor cycle | proven - D-pad Left/Right `0x20 \| 0x80`, spatial actor ordering, commits a real target |
| 6 | **save / load menu**, the save crystal's | authored usage: selector `0x8005`, the crystal actors (C-3) |
| 7, 8, 9, 13, 16, 20 | **no screen in the image.** No producer except the developer hook `0050DAB0` (verb `0x2037`), and the generic widgets give them only shared arms. 16 alone first zeroes the word `0209E5E8` and the UI root's byte `+0xDE6` (`0027FCEB`–`0027FCFE`). | census 2026-09-25 (FABLE, Claude Opus 5.5); UQ-162 |
| 10 | **shop menu**; the parameter is the shop inventory id | authored usage (C-3) |
| 11 | **game over** — raised by the field frame when no living playable-type unit (kind 0, type `≤ 6`) exists in the party or the nine reserve entries ([the world-tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) stage 3, `002371B0`) | mechanism proven 2026-09-12 (FABLE); ~~on-screen wording unread~~ wording read 2026-09-30 (§7c P1): the image `gameover_c.tm2`, which reads *GAME OVER* *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15))* *(2026-09-30, DD batch 13: its widget family asks for no text id, so the wording is in the screen's own resources; proposed row P1, §7b)* |
| 12 | **the `spattack` window.** It is opened only by ScriptVM verb `0x2A8` (catalogued `openspattackwindow`) through `002E1AE0`, and polled by verb `0x2A9` (`spattackwindowsync`) through `0028F7C0`. The router's own arm `0028E970` releases and rebuilds a `0x760`-byte widget ~~at `0209BE80 + 0x10FB0`~~ whose pointer it keeps at `[0209BE80] + 0x10FB0` *(corrected 2026-10-02, OPUS: `0028E970+0xF` reads the qword there, `0028E970+0x1B` tears the old widget down, and `0028E970+0x60` stores the new one, which `002D5030` builds through `00244F50` with `ecx = 0x760`)* | mechanism proven 2026-09-25 (FABLE, Claude Opus 5.5); the name rests on the verb catalogue's labels, not on a string |
| 14 | valid fullscreen mode/request slot | structurally proven, **name open** *(answered 2026-09-12 as C-1: an unused request number, §7)* |
| 15 | **airship-route map**: the world map in kind 3, titled "Airship Route"; the parameter is a directed route, 1–14 | proven 2026-09-25 (FABLE, Claude Opus 5.5), static plus shipped data; UQ-162 |
| 17 | **Strahl destination picker**: the world map in kind 2, titled "Choose your destination." | proven 2026-09-18 and 2026-09-25 (FABLE, Claude Opus 5.5) |
| 18 | the world map in kind 7, with no help-line title | mechanism proven 2026-09-25 (FABLE, Claude Opus 5.5); what kind 7 changes is not read *(read 2026-09-30, DD batch 13, §7b R5: kind 7 shows the nodes and the missing title of kind 1, the field menu's own map, but closing it ends the request as kinds 2 and 3 do)* |
| 19 | **hunt list**: the `menuquest.dat` rows, with hunt titles from `questtitle.bin`; the parameter preselects an entry id | proven 2026-09-25 (FABLE, Claude Opus 5.5), static plus shipped data; UQ-162 |
| 21 | valid generic/transient request slot | structurally proven, **name open** *(answered 2026-09-12 as C-2: an unused request number, §7)* |
| 22 | **map screen**; parameters 0, 1 and 2 become the sub-modes `0x40`–`0x42`, and `0x42` is the map tutorial | authored usage 2026-09-18 (FABLE) |
| 23 | **leader incapacitated** — the field frame's stage-19 latch: raised while the party leader carries KO / Stone / X-Zone (`0x80000003`) without the field's bit-15 exemption, cleared otherwise; arms capability-policy row 8 bits 6, 8, 9, 11 (`002548F0`) | mechanism proven 2026-09-12 (FABLE) |
| 24 | **party incapacitated** — a `0xC8`-byte widget with proc `0035D6B0` behind the singleton `022CA428`; raised (stage 3 / stage 18) when every non-guest member of the active party is down while playables remain in the reserves; ~~the widget builds the battle-menu selection state (`0035BC50`) — the reserve-swap prompt by mechanism~~ the widget shows the message *"All members of the party have fallen. Reform the party with one or more reserve members."* (`menu_message.bin` text `0x86F`) and, once that is dismissed, opens the Party Menu by posting request 2 with parameter 0 *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13): `0035BC50` is on the widget's request-3 arm, not request 24's; §7b R2, R3)* | route read (§2); mechanism 2026-09-12 (FABLE); ~~on-screen wording unread~~ wording read 2026-09-30 (§7b R3) *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13))* |

### Fullscreen-menu translator

`002E0DA0` maps a compact ScriptVM selector (low 15 bits, values `0..6`) to request IDs:

| Selector | 0 | 1 | 2 | 3 | 4 | 5 | 6 | other |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Request | 17 | 18 | 10 | 15 | 19 | 6 | 22 | **2** |

Bit `0x8000` is preserved into the returned value. Reached from authored
`0x048D openfullscreenmenu_48d` via handler `003462D0` -> `002E1A60` -> `002E0DA0`.

**What the shipped scripts author (2026-09-12, FABLE; C-3 / C-4).** The verb takes two arguments;
`002E1A60(selector, param)` translates the first and posts both into the router's input mailbox
(`0215F1A4` / `0215F1A8`, `002E1AC4`–`002E1ACA`). All **1,274** calls in the 1,114 decompiled scripts
push immediates (1,267 pairs; 7 through variables):

| selector | request | calls | parameter | authored by |
|---|---|---:|---|---|
| `0x8005` (5, bit 15) | 6 | 1,146 | 0 (1 twice) | `system_crystal_actor` ×243, `Map_Trial_Common_Process` ×900, `EventDirector`, `DIRECTOR`, `LOADPS2SAVE` — **the save crystal's menu** |
| 2 | 10 | 96 | 0–56, one id per call | `NPC01`, `PC03`, `crystaldummyPC`, treasure actors, and the three named shopkeepers `NPC_SHOP_YOROZU` (0x1C), `NPC_SHOP_MAGIC` (0x1A), `NPC_SHOP_GANBIT` (0x1B) — **the shop menu, the parameter a shop inventory id** |
| `0x8000` (0) | 17 | 18 | 0 | `system_anchor_actor` ×13, `NPC01`, `Map_Director` |
| `0x8004` (4) | 19 | 1 | 6 | `PRODUCER` (a debug actor) |
| `0x8006` (6) / 6 | 22 | 2 | 2 → `0x42`; 0 → `0x40` | `__MJ_CTRL005` (a map-jump controller); one unnamed |
| 1, 3 | 18, 15 | 0 | — | never authored |

Two names therefore rest on the authoring actors rather than on strings: **request 6 is the save
menu** (every call but three comes from a crystal actor) and **request 10 is the shop menu** (the
parameter is the shop id, 57 distinct). The others are named only by their callers. **C-4's
`0x40` / `0x41` / `0x42` are the handler's remap of selector 6's parameter** — `0 → 0x40`, `1 → 0x41`,
`2 → 0x42`, anything else `0` (`002E1A81`–`002E1AA1`) — so they belong to request 22's sub-modes, of
which the shipped scripts author `0x42` (once) and `0x40` (once); `0x21`'s producer is not among
the script calls.

`002E0E30` is the inverse for *current* fullscreen mode: it accepts modes `0..19` and maps
them back to request IDs. **Mode 14 maps back to request 14** - which is why request 14 is
structurally real even though no ordinary producer emits it. Mode 21 does not exist in that
translator, which separates request 21 from request 14.

### Complete producer census

Direct transfers to the mailbox `002E1B10`: `00253D78`, `00253EE6`, `00253F44`, `00253F53`,
`0035C81E` (request 11), `0035D750`, and `0050DAC4` (tail-jump). `002E1AE0` stores request 12
directly. **No ordinary hardcoded producer of request 14 or 21 exists.**

`0050DAB0` is the developer hook: it takes one VM numeric value, zeroes the parameter, and
tail-jumps into the real mailbox - bound by the ff12-script catalog to
`0x2037 debug_open_triangle_menu2`. So 14 and 21 are exercisable slots, but that does not
name them.

### The generic route, and the request word every route sets (read 2026-09-11)

`00280A00(request, parameter, flag)` — the `default` arm's target — first tests the UI root
object `*(0209AC30)`: if either of its pointer slots `+0xC0` or `+0xB8` is non-null it returns 0
without doing anything (`00280A13`–`00280A30`, `00280AAD`) — a generic request is already up.
Otherwise it builds **two** objects on its frame (`00280A32`–`00280A5B`; corrected 2026-09-11,
ASTRA-CONTRA-FABLE-UI-PACKET — the first version described one 32-byte record with a self
pointer): a 16-byte **payload** `{u32 request, u32 parameter, u32 flag, u32 0}` at `rsp + 0x20`, and
a separate 24-byte **descriptor** `{u32 0, 4 bytes never written, void* payload, s64 request}` at
`rsp + 0x30` — the descriptor is what the factory receives, its `+8` points at the payload and its
`+0x10` is the sign-extended request (`movsxd`, `00280A4F`). Then it:

1. calls **`00252B40(request, 1)`** — the second argument is the literal 1 (`00280A3C`), *not* the
   incoming parameter, which lives only in the payload — and the setter stores **`02092734 = 1`**
   and **`020927D8 = 02092730 = request & 0x7FFF`** (`00252B40`–`00252B52`) and tail-jumps into
   `00254740`: `00255290(id)` yields a handle (negative → nothing more); for ids `3`, `4`, `20`,
   `24` (`bt 0x1100018`), or id `1` when `002DDC30()` is 0, it calls `003B3B40()`; then
   `00226BE0(handle, 0, 0, 0, −1, −1)` and `00226280()` (`00254754`–`002547A2`) — the
   **start and apply steps of the system-stop registry**, both read whole on
   [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §3–§4
   (*"unread" corrected 2026-09-12 (OPUS)*);
2. constructs two `0xD8`-byte widgets through the widget factory `00244F50` with procs
   `0027FB70` and `00280140` and the descriptor as their init message (`00280A65`–`00280A8C`;
   [the widget model](../Widget-Object-Model/the-widget-constructor-and-object-sizes.md));
3. calls the thunk `0028E860`, which zeroes the 0x80 bytes at **`[0209BE80] + 0x7EA0`** (`0028E860` → `0028CA30` → `memset`) — the region the per-frame gate's `0x0800` group updates ([the update gate](../../00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md)) — and returns **1** (`00280A91`–`00280A96`).

So the generic scheduler accepts any request dword the router forwards, and what it *means* is
whatever the two widget procs make of the descriptor — `0027FB70` (1,237 B) is bound with its whole
10-member subtree below; `00280140` (924 B)
turns out to be the area controller that consumes the load controller's restore and field-request bits (§ key
addresses, 2026-09-13). **`00252B40` is not the generic route's alone**: every special route calls it
too (`0035D980`, `003C87B0`, `0028E970`, `0035D6B0`, `0027EFA0`, `00279E20`, `0035C960`,
`0035CF10`, `003F4E70`), so `02092730` is **the id of the last UI request any route posted** and
`02092734` is **that route's second argument — a flag, not the parameter**: 1 from the generic
route and from requests 3 (`0035DA43`), 24's widget (`0035D820`), `0027EFCD`, `0035C9F7`,
`0035CF14` and `003F5004`; 0 from requests 5 (`003C88D0`) and 12 (`0028E9B8`); a variable from
`00279E20` (`00279FCE`). That is why the router's own gate `cmp [02092734], 1` (`00254B71`)
refuses every new request while a request posted with 1 is up — the generic route included —
and lets requests 5 and 12 through behind one another; ~~who clears the word is unread~~ the word is cleared by
`00252D90`, which cancels the request's system stop and zeroes `02092730` and `02092734`, from sixteen sites (the generic
route's area controller among them), and by the reset `00252DE0` on the area unload *(Corrected 2026-09-30
(SWE2-CONTRACT for OPUS, DD batch 13), §7b R1)*. ASTRA's
[EXP-069](../../_experiments/EXP-069-ui-native-feedback.md) closes the loop for the generic route
as original code: the router, the generic scheduler and the setter run together in one memory
state, the setter's three writes (`02092734 = 1`, then `020927D8` and `02092730 = id & 0x7FFF`,
`00252B46`–`00252B52`) land before the prelude and factory stubs, and a second router call on the
same state returns 0 before its policy producer (11 two-call fixtures, including gate 2 replaced
by 1, a busy root, and a policy refusal followed by admission; a mutant posting 0 lets the second
call through and is rejected) — the feedback is native, not a stub assumption; how long the game
leaves the word set, and who clears it, stay outside *(who clears it is read statically in §7b R1, 2026-09-30, DD
batch 13; how long the word stays set is runtime-only)* *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: a stated limit, not an open question. The word is set by `00252B46` and cleared by `00252D90` or the reset `00252DE0` (§7b R1); how many frames lie between depends on the player.)*. And it is why the field frame's predicate
`0035C700` treats `02092730 ∈ {0x0B, 0x18}` as "a UI request is up" ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md);
`EX-2`): those are request ids **11** (generic) and **24** (`0035D080`).

### The two other special routes (read 2026-09-11)

**Requests 1 and 4 — `0035D660`** (75 B): refused (0) unless policy bit 10 is set (`002E0FA0`,
`0035D668`–`0035D671`) and `003669D0()` returns 0 (`0035D67B`–`0035D682`); request 1 is further
refused while `022C8060` bit 0 is clear and `022C806C` is zero (`0035D684`–`0035D697`). Then
`0028FD50(id)` stores the id in the singleton `*(0209BE80)` at `+0x10F60` (word) and ors `0x10`
into `+0x10F68` (`0028FD50`–`0028FD6E`), and the route returns 1 — the same singleton whose
`+0x7EA0` the generic scheduler zeroes. ~~Which screen reads those two fields is not followed here.~~ They are read by
`00290CF0`, the update gate's group `0x2000`: while no request word is up it hands the stored id to `00276650`, which
builds the `0x61F0`-byte battle-menu widget with procedure `00279E20` *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS,
DD batch 13), §7b R8; the dispatch table above already named the result)*.

**Request 24 — `0035D080`** (93 B): if the singleton `022CA428` is null it constructs a
`0xC8`-byte widget through the factory `00244F50` with proc **`0035D6B0`** (515 B) and init message
`{0, id, 0}` (`0035D093`–`0035D0C1`); it returns 1 either way. That proc is the one that later
posts the request word (`00252B40` at `0035D825`) — so `02092730 = 0x18` while its widget lives;
its callees (`002E1B10` the mailbox, `002E1C20` / `002E1CA0`, `0035BC50`, `0028FD70`, `00290450` /
`00290500`, `00428F30`) ~~are unread, and so is what it shows~~ have their roles in this procedure read in §7b R2 (the bodies of
`0035BC50`, `0028FD70`, `00290450`, `00290500` and `00428F30` are not read there) *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: `0035BC50` is read on [the battle-mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md), whose crossings name `0028FD70`'s callees and measure `00290500`. `00290450` forwards to `003F80E0` on `[0209BE80] + 0xA0D0` when that singleton exists, and `00428F30` walks the `0x740`-byte records of `022C6F28` from the head index `+0x48800` through each record's word `+4`, calling `0046D0A0` on its `+0x5F0`. A stated limit: no claim here rests on what those two do inside. [Record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md) F1-F3.)*: the procedure also serves request 3,
shows the dialog text `0x86F` for 24 and opens the Party Menu on close *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS,
DD batch 13))*.

### Request 6 — from the save crystal's menu to the area reset (reviewed 2026-09-13)

*FABLE's independent re-read of ASTRA's [spawn page §22](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)
(`ASTRA-REQ-FABLE-LOAD-CLOSE`); every step below was decoded from the image, and ASTRA's chain holds. It is a
conditional code path, not an observed load.*

**Opening.** `0027F540(request, parameter, third)` does nothing while context `*(0209AC30)+0x100` is occupied;
otherwise it starts a timed transition (`002C99A0`, duration 1 when the request word has bit 15, else 200) and builds
the `0xF0`-byte fullscreen widget with procedure `0027F5D0`. On message 1 that procedure publishes itself at
context `+0x100`, keeps `request & 0x7FFF` at `+0xD0` and the parameter at `+0xD4`; on message 18 it clears
context `+0x100`. **Its per-request table (`0027FAD0`) is read on message 19 — the widget's transition finished
forward** ([the widget protocol §9](../Widget-Object-Model/the-widget-message-protocol.md)). Request 6's arm
(`0027F8DB`) prepares the image — parameter 0: `003C60F0`, then, if still 0, `SaveTransition_PrepareRuntimeImageForCapture`
and `0020E5C0`; otherwise `SaveImage_BackupActiveRuntimeBuffer` — and calls **`SaveLoad_OpenController(parameter, 1)`**
(`0027F984`), which builds the `0x5A0`-byte controller `00582860` with a boolean `1` that its message 1 turns into
`+0xC4` bit 3.

**The controller's message 18** (`00582E81`–`00582F1B`). With `+0xC4` bit 4: when byte `+0x598` is 0, `001831A0`,
`0209AC10 = 1`, **`WorldTransitionSnapshot_RestorePersistencePairForActiveSlot`**, `00182D40`; then, either way,
`00394400` if `00394520()`, and **`SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`**. Always: `00582FC0`, release
`+0x588`/`+0x590`, clear `02CA99B8`. **With bit 3, `002814E0(−2)`** (`00582F0E`); then `002E1CA0(1, 0x15)`. So a
restore, when admitted, returns before the close request — but bit 3 closes without bit 4, and `+0x598` skips the
restore while still normalising; a closed menu is not evidence of a restore.

**The close.** `002814E0(−2)` tail-calls `00244F00` on context `+0x100` when it is non-null (`0028153C`–`00281558`);
`00244F00` sets bit 6 and sends 15 now or through its deferred path. On 15 with bit 6, `0027F5D0` calls `002D6F90`
when the parameter is `0x42`, then `00295CE0` and **`0027F2E0`** (`0027F61F`–`0027F63C`) — which `002814E0(−1)` also
reaches directly. `0027F2E0` runs a fade (`002C98C0`, `00250F30`, `002CC960`; duration 1 when context `+0x400`
bit 11, else 200), re-reads `+0x400` and writes its **low byte**: 2 when bit 9 is clear; 1 when bit 9 is set and bit
10 clear; 2 when both are set (`0027F324`–`0027F33B`); then clears bit 11.

**What the `+0x400` bits mean on this path.**

| bit | set by | read by |
|---|---|---|
| 9 — restore pending | `00285E60` (from the controller, `00582CD0`/`00582CE6`), with bit 10, after which it runs the battle-state guard `00233C10` and tail-calls `002CFD10(−1)` | `0027F2E0`; the area controller's message 18 |
| 10 — the controller already verified the block | `00285E60` | `0027F2E0` (state 2 instead of 1) |
| 8 — plain field transition to `+0x3FC` | `00285EC0` (callers `00228C70`, `003EFAA0`) and the invalid-image branch below | the area controller's message 18 |

**The area controller `00280140`** binds `+0xC0 = context + 0x3F8`, so its `[+0xC0] + 8` is context `+0x400`.
Message 2 by state:

- **state 1 — verify first** (`00280357`–`002803CC`): unless `0032E4D0(context+0x3F8 dword)`, it calls `00254CB0(0)` and
  validates the active image's header (`SaveImage_ValidateRuntimeFormatHeader` on buffer `+0x68`). **Valid** →
  `00233C10`, `002CFD10(−1)`. **Invalid** → `SaveRuntime_ResetActiveImageAndRebindState`, clear bits 9 and 10, **set
  bit 8 with target 0**. Either way it writes state **2**. *This is a second producer of state 2, which §22 does not
  list.*
- **state 2 — wait, then tear down** (`002802D1`–`00280345`): only when `00251D50()` and `003CA0F0()` are non-zero,
  context `+0x300`/`+0x308` are null, and roots `0208EA30` and `0208EA20` have no children, `00245020(self)`, state 0,
  `0024AB30`.

**Its message 18** (`00280184`–`002802A0`), after `0024AB60` if context `+0xDF4`, `003667B0(0)`, `00365980` and, by the
request class message 1 stored at `+0xC8`, `00254440(0, 0x80)` or `00254480(0, 0x80)`: **bit 9** → clear 9 and 10, `WorldPersistence_ResetBanksAndMarkInitializationState`, clear payload
`+0x1061` and `0020E4E0` when `0020E5A0()` is 5, **`WorldTransition_RequeueCurrentFieldForRestore`**, `00360D50`, and
`002EFA70(0, 1, 1, 0)` when `002EFD20(0)`; otherwise **bit 8** → clear it, then `003603E0` when `+0x3FC` is `0xC`,
else `002CFD10(−1)` and **`WorldTransition_RequestFieldTransition(+0x3FC, 0, 0, 0)`**. Then `00251E80`,
`00252D90`, context `+0xDEF = 0`, `+0xC0 = 0`.

**Which slot is loaded changes what a load restores — slot 0 is the field-transition autosave (reviewed
2026-09-13, `ASTRA-REQ-FABLE-LOAD-SUCCESS`, [spawn page §24](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)).**
The controller's `+0xC1` is `parameter != 0`, so request 6 with parameter 0 (the capture path) opens it in save mode
and a nonzero parameter (the backup path) in load mode; the slot selector `0057FE80` copies that to `+0xEA` and starts
its list at slot **1** in save mode, slot **0** in load mode (`0057FF56`–`0057FF66`). On subtype `0x8001` it stores
the chosen slot in its own `+0xEB` and in the controller's `+0x598` (`0058050C`–`0058053A`). **The only full-image
write with a fixed slot is the autosave:** `WorldTransition_StageFieldTransition`, when `WorldTransition_ShouldAutosave`
agrees (`00314774`), captures the snapshot, prepares the image, runs
**`WorldTransitionSnapshot_CapturePersistencePairForActiveSlot`** (`003147E4`, its only caller) and opens the write
controller, whose `SaveWrite_PrepareAndSubmitFullImage` names the file with slot **`r9b = 0`** (`0057E3E0`–`0057E3F2`).
So slot 0 is the autosave — a manual save cannot choose it — and **the persistence-pair restore that the controller's
message 18 admits only when `+0x598 == 0` is the inverse of a capture only the autosave performs**. The capture
(`00584580`) exports the group persistent bank and serialises the SpawnKeep banks into image A (active-buffer `+0xE240`/`+0xE440`,
the payload map's `+0xE040`/`+0xE240`), or image B (buffer `+0x2E450`/`+0x2E650`) when the battle-state block's `+4` bit 12 is set (`00236760`), plus the transition-metadata record `+0x4E660` and the
SetSaveData byte; the restore (`005843E0`) reads them back by the same bit — image B unless the load-mode byte `02AEE4D8` (`00394450`) is
3, the Trial Mode route, and the image's `+0x57` bit 0 is clear. The same path sets `0209AC10 = 1` first (`00582E98`), and that flag is what stops
`WorldPersistence_ResetBanksAndMarkInitializationState` (`00268320`), in the area controller's later message 18, from
clearing the group bank `02099FF0` and from setting the weather-restore flag `+0x1061`; `02099DF0` is cleared either
way. **So loading the autosave brings back the group bank and SpawnKeep bank 2 as they were at the transition; loading
a manual slot restores neither and can clear the group bank** (when `01E0C3EC` is set). The success notification itself
is `SaveLoad_FullImageStorageCompletionCallback` `00580840`: operation 9, status 0 → `00247510(parent, 16, 4)`
(`005808E6`), whose parent arm sets `+0xC4` bit 4 and calls `00285E60` (`00582CB3`–`00582CE6`); status 8 or any other
failure instead calls **`SaveUI_RestoreActiveHeaderFromControllerBackup` `00583C00`, which copies back exactly
`0xE240` bytes** (`0x1C4 × 0x80 + 4 × 16`) — ~~the image up to, not including, SpawnKeep image A~~ the `0x200`-byte header and
payload `+0x0000`–`+0xE03F`, **stopping where group persistent bank A begins** (buffer `+0xE240` = payload `+0xE040`; corrected
2026-09-13 — the payload base is buffer `+0x200`, `002EF2B9`). **Not established:** that
nothing else writes `+0x598` before message 18, why the block's bit 12 selects image B, and what a manual-slot load
leaves in SpawnKeep bank 2 (it is not restored, and `00268320` does not clear it).
*Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13), two of three:* the slot selector's `0058052A` is the only
byte store to `+0x598` in the save / load code, the controller only compares it, and the widget factory zeroes every new
widget, so the byte is 0 until a slot is chosen (§7b R9, a displacement census). What a manual-slot load leaves in bank 2
was observed on 2026-09-21: exactly what the session had (`L-13`, SUPERSEDED 2026-09-27). Bit 12's three writers are read
(§7b R10); what the bit stands for is proposed row P3.
*Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15, §7c P3):* the bit says that the session was loaded through load mode 3, the title's Trial
Mode route, so image B is that session's pair.

**What the success notification does not check — a short read (reviewed 2026-09-13, `ASTRA-REQ-FABLE-STORAGE-COMPLETION`,
[spawn page §25](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)).** The read copies from the decoded file
vector with `00866A00`, which stops at the vector's end, leaves the rest of the destination as it was, and returns 1 only when
the whole count was copied (`00866A61`–`00866A64`) *(for a destination that does not overlap the cursor dword. Each
iteration stores the byte at `00866A4D` and then increments the cursor at `00866A54`, so an aliased destination ends
with the incremented cursor byte and the cursor jumps. See [the storage read contract](../../19-Save-Load-Settings/CONTRACT-storage-read-completion.md)'s
precondition; added 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's storage-read-cursor-alias)*; `00862590` publishes `return × requested` (`008625A9`–`008625AC`), so a
short copy reports **0**, and the read sequence `003BA7B0` tests only the sign before closing (ASTRA's §25.1–25.3, with
method-B traces of both readers). Nothing later on the success path compares a length: `00285E60` runs the guard `00233C10`,
which checks only the battle-state block's stamp at buffer `+0x4E68C`; with bits 9 and 10 both set `0027F2E0` writes state 2
directly, so the area controller's header check (`SaveImage_ValidateRuntimeFormatHeader`, state 1) does not run; and no load
path recomputes the image checksum ([`FV-3`](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md)).
**So a decoded save shorter than `0x56690` bytes would load as its own prefix over the rest of the image that was active
before the load**, reported as success *(narrowed 2026-09-13: the guard's prelude `00235AF0` then re-imports the battle-state block's first `0x6000` bytes from buffer `+0x2200` when its four probe fields differ and rebuilds the gambit banks, so for a 2018-size save the block is converted from its older location — [spawn page §27](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md); the rest of the tail beyond `0x4E690` outside that import stays as it was)* — a conditional composition of read code, not an observed load. The completion's
result override `0017E470` (`+0x10DC` of the parameter dispatcher's settings object) cannot interfere in retail: its only
stores are the constructor's 0 (`001CCE63`) and console id 291's four-state cycle (`001D4BB7`), which is not among the 16
ids the image can issue ([the parameter console](../../00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md)).

**So the three load outcomes separate by bits, not by the menu closing:** a verified restore (9 + 10 → state 2 →
bank reset and requeue of the current field); an unverified one (9 alone → state 1 → header check → the same restore,
or, on a bad header, a reset image and a transition to field `0`); and a plain transition (8 → field `+0x3FC`).
**Not established:** that the fullscreen widget still has procedure `0027F5D0` and context `+0x100` when 15 arrives,
the ordinary delivery order of the controller's 18 against the area controller's 2, what the native callees
(`00394400`, `002CFD10`, the fade calls) do, and whether field `0` is the title. ~~`L-13` stays open for that.~~ `L-13` is
SUPERSEDED (2026-09-27, OPUS); its live remainder is carried by `FABLE-REQ-ASTRA-L13-BANKS` *(Corrected 2026-09-30
(SWE2-CONTRACT for OPUS, DD batch 13))*. *The callees are read on other pages:* `00394400` destroys the title asset
([the title-asset singleton](../Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md)),
`002CFD10` is the two-stage party compose `002527B0(6, 4, 0)` then `0028E880`
([the SetSaveData presets](../../11-Party/the-setsavedata-presets-test-battle-scenarios.md)), and the fade calls belong to
[the layout parameters](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md). The widget's procedure at
message 15 and the delivery order are runtime-only. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: proposed as register row Q2 in [batch 20's record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md), disposition runtime.)* Whether field `0` is the title is proposed row P4 (§7b).
*Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15, §7c P4):* yes. `00314440` replaces target 0 with field `0xC`, `ttl_a01`, while the
debug byte `02B62DB9` is 0, and nothing but the reset writes that byte.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00254B50` | UI request router | 263 B | normalise, refuse, dispatch 1..24 |
| `002E1B10` | deferred request mailbox | 85 B | store pending request+parameter |
| `002E1A60` | fullscreen request submit | 123 B | translate then post |
| `002E0DA0` | selector -> request translator | 104 B | 0..6 -> 17/18/10/15/19/6/22, default 2 |
| `002E0E30` | current fullscreen mode -> request | 236 B | modes 0..19 |
| `0035D660` | open-gate route *(working name `UI_RequestOpenGate`)* | 75 B | requests 1 and 4 |
| `0035D980` | leader-selection route | 251 B | request 3 |
| `003C87B0` | free-target route | 371 B | request 5 |
| `00280A00` | generic request scheduler | 193 B | every id the switch does not special-case; refuses while the root's `+0xB8` / `+0xC0` are occupied (§2) |
| `00252B40` | request-word setter | 29 B | `02092730` / `020927D8` = id & 0x7FFF, `02092734` = the caller's second argument (1 or 0, a flag); called by every route |
| `00254740` | per-id prelude | 114 B | handle from `00255290`, `003B3B40` for ids 1 / 3 / 4 / 20 / 24, then `00226BE0` / `00226280` — the system-stop registry's start and apply, read whole on [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) |
| `0027FB70` / `00280140` | the generic request's two widget procs | 1,237 / 924 B | `0027FB70` bound 2026-09-14 with its 10-member subtree (§ subtree below): message 1 opens + publishes self at `*(0209AC30)+0xB8`, message 2 ticks the `+0xD0` state machine, message 18 unpublishes; `00280140` read by ASTRA ([spawn page §17](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md)) and checked 2026-09-13: message 1 binds `+0xC0 = *(0209AC30) + 0x3F8` (`0028044C`); message 18 consumes request bits 9 (restore: `00268320`, then the requeue `00267C90`) and 8 (field request `00314440`, or `003603E0` for field 12) of `*(0209AC30) + 0x400` |
| `0028FD50` | request 1 / 4's action | 31 B | `[0209BE80] + 0x10F60 = id`, `+0x10F68 \|= 0x10` |
| `0035D6B0` | request 24's widget proc | 515 B | posts the request word; ~~unread~~ read 2026-09-30 (§7b R2): also request 3's; for 24 it blocks capability row 8 bits 0 and 20, shows text `0x86F` after a 24-step countdown, and on close clears the word and posts request 2 *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13))* |
| `0209BE80` | UI / HUD singleton | — | `+0x7EA0` zeroed by the generic scheduler and ticked by the update gate's `0x0800` group; `+0x10F60` / `+0x10F68` written by request 1 / 4 |
| `0035DCC0` | spatial actor target ordering | 492 B | request-5 candidate ordering |
| `003C9250` / `003C9420` | prev/next resolver / commit | 280 / 117 B | request 5 |
| `0050DAB0` | `debug_open_triangle_menu2` handler | 25 B | arbitrary ID injection |
| `0017E210` | DecideButton getter | - | `settings+0x64` |

## 4. Data structures

```
01E0C2A0   u32   configured Decide/Confirm face-button mask
01E0C2A4   u32   the paired other face button
                 DecideButton=Circle -> A0=0x2000, A4=0x4000
                 DecideButton=Cross  -> A0=0x4000, A4=0x2000

Pad masks observed: 0x10 Up, 0x20 Right, 0x40 Down, 0x80 Left,
                    0x1000 Triangle, 0x2000/0x4000 Circle/Cross, 0x8000 Square

Logical command list (14 entries): [13,12,10,8,11,9,1,2,15,14,7,5,4,6]
  DecideButton swaps entries 0 and 9, i.e. logical command IDs 13 and 14.

02092730   u32   the last UI request id posted by any route (id & 0x7FFF); 0x0B / 0x18 = ids 11 / 24
020927D8   u32   a second copy of the same id
02092734   u32   the route's flag argument to 00252B40 (1 on the generic route); the router refuses
                 everything while it is 1

GenericRequestPayload (16 bytes, rsp+0x20 in 00280A00)      GenericRequestDescriptor (24 bytes, rsp+0x30;
  +0x00  u32  request (original dword)                        the init message of the two widgets)
  +0x04  u32  parameter                                        +0x00  u32   0
  +0x08  u32  flag                                             +0x04  u8[4] never written
  +0x0C  u32  0                                                +0x08  void* payload
                                                               +0x10  s64   request (movsxd)
```

## 5. Call chain

```
pad input
  -> 00253C70  InputGameplay_ArbitrateDigitalInputAndModalState
     -> eligibility gates
     -> requestId prepared
     -> 002E1B10 mailbox   OR   00254B50 router directly

authored script
  -> 0x048D openfullscreenmenu_48d -> 003462D0 -> 002E1A60 -> 002E0DA0 -> mailbox

routing
  -> 00254B50
     -> 002E0FA0 + 01E0C2C0  -> inhibit mask  -> refuse, or
     -> switch -> route function -> UI transition
```

**Upstream:** Input arbitration and ScriptVM fullscreen requests.
**Downstream:** UI root pending mode, screen transitions, target selection commits.

## 6. Modding notes

- **To add a UI entry point:** post through the mailbox `002E1B10` or the router `00254B50`,
  not by poking UI root state. The policy gate exists for a reason.
- **DecideButton is a real setting** (settings entry 25, values `Circle`/`Cross`). Read the
  configured mask rather than hardcoding a face button.
- **XIIOnline:** request state is local UI policy. Do not network request IDs, mailbox bits,
  or generic UI object state. Requests 14 and 21 have no proven identity - do not build
  behaviour on a guess. *(2026-09-30, DD batch 13: C-1 / C-2 now rule both unused request numbers, §7.)*

## 7. What is not known

- [x] ~~Friendly identity of request 14 (open question **C-1**).~~
- [x] ~~Friendly identity of request 21 (open question **C-2**).~~ **C-1 / C-2 closed 2026-09-12
      (FABLE): not in the image — neither id has a dedicated handler at any level.** The generic
      route's two widget procs dispatch on `(id & 0x7FFF) − 2` through three jump tables, all read
      from `.rdata`: `0027FB70`'s first table (`00280048`, 18 cases; `0027FC7B`–`0027FC9A`) sends
      cases 0 / 8 / 14 (ids 2 / 10 / 16) and 4, 13, 15–17 (ids 6, 15, 17–19) to dedicated arms and
      **everything else — ids 3, 4, 5, 7, 8, 9, 11, 12, 13, 14 — to the shared arm `0027FD1C`**; its
      second table (`00280090`, 21 cases; `0027FE11`–`0027FE30`) likewise gives ids 2 / 22, 6, 10,
      11, 15–19 their own arms and **ids 3, 4, 5, 7, 8, 9, 12, 13, 14, 20, 21 the shared arm
      `0028000E`**; and the fullscreen proc `0027F5D0`'s table (`0027FAD0`, 21 cases; `0027F8BA`–
      `0027F8D9`) singles out ids 2 / 22, 6, 15, 17, 18, 19 and drops **ids 3, 4, 5, 7–14, 16, 20, 21
      into the shared arm `0027FA31`**, which only clears bit 7 of five ~~widget records'~~ named UI atlas slots' `+0x38` *(corrected 2026-10-01, OPUS, on SWE2-CONTRACT's request, at the bytes: `0024A5A0` finds each slot by name in the 64-slot registry `0208F580`, and bit 7 admits an atlas to the texture-memory layout pass `0024A710`, which takes a slot only when its `+0x38` holds `0xE0 | (1 << k)` - see [a typed list measured once](../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md) §5d)*.
      Request **21** is beyond the first table's range and in the shared arm of the other two;
      request **14** is in the shared arm of all three. With no ordinary producer either (§2), the
      two ids are **unused generic-arm request numbers**: injecting them opens the generic
      fullscreen frame with nothing dedicated behind it. Mode 14's presence in `002E0E30` is the
      identity mapping of an unused slot, not a screen. What they were reserved for is authoring
      history the image does not carry.
- [x] ~~Player-facing names for fullscreen selector values 0..6 (open question **C-3**).~~ **Answered
      from authored usage 2026-09-12 (FABLE)** as far as the data allows: 5 → request 6 is the save
      crystal's menu, 2 → request 10 the shop menu (parameter = shop id); 0, 4 and 6 are named only
      by their calling actors (`system_anchor_actor`, `PRODUCER`, a map-jump controller); 1 and 3
      are never authored. See the table above.
- [x] ~~Meaning of request-2 parameters `0x21`, `0x40`, `0x41`, `0x42` (open question **C-4**).~~
      **C-4 ANSWERED 2026-09-12 (FABLE).** `0x40`–`0x42` are `002E1A60`'s remap of selector 6's
      parameter 0 / 1 / 2 (`002E1A81`–`002E1AA1`), i.e. request 22's sub-modes. **`0x21` is the
      ~~Triangle path's default parameter~~ default parameter of the pad-mask `1` and `2` paths**, produced twice inside *(corrected 2026-10-02, OPUS: Triangle, mask `0x1000`, posts request 2 with parameter 0 — `00253C70+0xF1` `cmp ebp, 0x1000` to `00253C70+0x108`; both `0x21` posts follow `cmp ebp, ebx` with `ebx = 1` from `00253C70+0xA4`, at `00253C70+0x17C` and `00253C70+0x291`)*
      `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`, request id `esi = 2` from
      `00253D88`): once unconditionally after `00236760()` returns 0 (`00253EE1 lea edx, [rax+0x21]`
      → `002E1B10(2, 0x21)` at `00253EE6`), and once at `00253F4E` → `00253F53` when
      `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(0x5E)` (`0032A8A0`) is **clear**; when that
      persistent flag is set the parameter is instead **script operand-bank word 2** —
      `FUN_00264640(2)` reads `i16[2]` of the kind-3 authored-operand bank at `02098E58`
      ([the save payload field map](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) `+0x0000`), ~~posted as-is when non-zero and as `0` when it is zero~~ posted as-is when non-zero and as `1` when it is zero
      (`ebx` = 1 from `00253D14`) *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15): §7c P2)*
      (`00253F2C`–`00253F44`). So request 2 carries three parameter sources: the fixed `0x21`, the
      script-authored operand word under flag `0x5E`, and the `0x40`–`0x42` sub-modes from selector
      6. *Not established:* what the menu handler makes of `0x21` versus a non-zero operand word
      (the consumer side of the parameter), and the authored name of flag `0x5E`.
      *Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13), the first half (§7b R7):* the generic route's close
      arm for request 2 opens the `0x288` menu widget `00280D20` for parameter 0 and hands any other parameter to the
      fullscreen procedure. There `1`–`0x20` open the airship-route page with that route, `0x42` the map tutorial, and
      every other value the location map `0028E660(1)`. So `0x21` opens the location map, and an operand word does the
      same unless it is a route number `1`–`0x20` or `0x42`. The name of flag `0x5E` is proposed row P2.
      *Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15, §7c P2):* no shipped file names the flag. By its role it is the airship-trip
      flag, set by the five aerodrome scripts before the airship map jumps and released by `asp_a02`.
- [x] **UQ-162.** Identity of requests 4, 6-10, 12-13, 15-20, 22. **Narrowed 2026-09-12 (FABLE):** 11, 23 and 24 are named at the mechanism level in the identified-requests table (game over, leader incapacitated, party incapacitated). *Narrowed again 2026-09-12 (FABLE):* **6 is the save-crystal menu and 10 the shop menu** (by propagation from `C-3`'s
      census of `openfullscreenmenu` over the shipped scripts, selector 5 → 6 and 2 → 10). And the generic scheduler's
      two `0xD8` widgets (`00280A00` builds procedures `0027FB70` and `00280140`) dispatch on `(request & 0x7FFF) − 2`
      twice: the **open** table (`0027FE14`, 21 arms, table at `00280090`) sends **2, 6, 15, 17, 18, 19 and
      22** — exactly the stop registry's full-screen-menu group — to one tail that starts a timed transition
      (`002CC9C0` → `002EFA70`, duration ~~scaled from the request parameter~~ of 200 ms, or 1 ms when bit 15 of the request record's first dword is set *(corrected 2026-10-02, OPUS: `0027FB70+0x213` `mov ebp, 0xc8`, `0027FB70+0x224` `bt r15d, 0xf`, `0027FB70+0x229` `cmovb ebp, edi` with `edi = 1`; ×60/1000 to frames at `0027FB70+0x2E4`)*) and builds the `0x140`-byte transition
      widget `00251D90` (procedure `002509D0`); **10** takes its own tail (`00251D90` then `00251F20`), **11** goes to
      `003EF750`, **16** to `0027FFCA`, and the rest (3–5, 7–9, 12–14, 20, 21) only to the common end, which may release
      presentation slots (`00300060`) and ~~closes~~ **attaches itself under the shared root** (`00247950(self, 0)` at `00280033`; corrected 2026-09-13 on `ASTRA-CONTRA-FABLE-WIDGET-ROOTS` — `00247950` loads `*(0208EA28)` and calls `00248220` for a parentless widget, and never reaches teardown; this widget's teardown is the separate `00245020` call at `0027FD62`). The **close** table (`0027FC7E`, 18 arms, table at `00280048`) groups 6, 15, 17,
      18, 19 together, with 2, 10 and 16 each separate. Which screens 2, 15, 17, 18, 19 and 22 open is not named by
      these arms. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: named since, in the narrowings below: 22 the map screen and 17 the Strahl picker (2026-09-18), 15 the airship-route map, 18 the world map in kind 7 and 19 the hunt list (2026-09-25); 2 opens the Party Menu for parameter 0 and otherwise the fullscreen procedure (§7b R7).)*
      **Narrowed 2026-09-18 (FABLE), by a census of `openfullscreenmenu` over all 769 decompiled `us` field scripts — 1,272 calls, the selector being the first push of the two-argument form and the parameter the second; the translation table `002E0DA0` maps selectors 0–6 to requests 17, 18, 10, 15, 19, 6, 22 and anything else to 2, with bit 15 carried through.* **Request 17 is the Strahl boarding menu**: selector `0x8000` is issued 18 times, always in a talk handler after a yes / no `aaske` whose text is the map bank's string 25, *“Board the Strahl?”* (decoded from `ene_a08.ebp`'s text section; the eighteen fields are `alc_e01`, `byu_b01`, `dst_a05`, `ene_a08`, `enw_a05`, `fon_a06`, `mnt_d01`, `nac_b01`, `ozm_b04`, `pbc_c01`, `pla_a06`, `rbn_b01`, `rwf_a01`, `sav_c02`, `sav_f02`, `srb_a04`, `var_b01`, `wdl_a06`). **Request 22 is the map screen**, and parameter 2 its tutorial sub-mode: the single `0x8006, 2` call sits in Rabanastre's function named *map command tutorial* (`rbn_a03`, after `sethpmenufast 0`). **Request 10's parameter is the shop row**: selector 2 is issued 98 times, and its parameters cover every row 0–56 of the shop table (row 24 once, the eight Assistant Storekeeper rows four times each). **Request 6 is confirmed as save / load**: selector `0x8005` is issued 1,148 times — 904 in each map's `main(1)` save-crystal routine, 243 in talk handlers, one in the function named *load screen launch* — and the same bank's strings 16–24 are *Save or load?*, *Save*, *Load*, *Save complete*. Selectors 1, 3 and 4 (requests 18, 15, 19) have **no script producer** at all, and seven calls take their selector from a variable. What remains unnamed: 4, 7, 8, 9, 12, 13, 15, 16, 18, 19, 20. DATA: the archive's scripts decompiled with `ff12-script -d`; the map text decoded with the st2e charset.*
      *Reconciled 2026-09-18 (FABLE): request 4 is named by this page's own table and leaves the list.* The identified-requests table above gives 4 as **the same battle-menu open as request 1** (`0035D660`, both reaching `0028FD50`, which the UI tick turns into the `0x61F0` battle-menu widget with the request id passed to it), so the list of the unnamed is 7, 8, 9, 12, 13, 15, 16, 18, 19 and 20. The cell the table gives for 7, `002AC18B`, is not a router call: it is the countdown block inside `002ABF70` that decrements the word `+0x88` and clears the byte `+0xB0` when it reaches zero (`002AC18B`–`002AC1A4`), so request 7's producer is still to be found. Static. *(Answered 2026-09-25 below: 7 has no producer and is an unused
request number. Marked 2026-09-30, SWE2-CONTRACT for OPUS, DD batch 13.)* *(Provenance note, 2026-09-21 (FABLE), answering `OPUS-REQ-FABLE-THREE-LIVE-ABSENCE-CLAIMS-BLOCK-THE-GN162-CARRY`: **"the unnamed" in this paragraph is the list of request ids, not of functions.** `002ABF70` itself is in the residual set at GN158 and GN160 and **out of it at the current parent GN162**, where it carries `UI.Text.ElementModeStateTick` — which is what a word-decrementing countdown block inside it should be, so the classification corroborates this reading. Request 7's producer remains the open part, and that is a claim about a request id, not about a residual record.)*
      **Narrowed again 2026-09-25 (FABLE, Claude Opus 5.5): requests 15, 17 and 18 open one world-map screen in three kinds, and request 19 is the hunt list.** The fullscreen procedure's table (`0027FAD0`, indexed by id − 2) sends 15, 17 and 18 into one tail (`0027FA27`–`0027FA2C`). It stores a kind byte at `+0x10FA2` of the `0209BE80` object (`002903F0`), and `0028E790` passes that kind, with the word at `+0x10FA6`, to the world-map installer `00550400`; they become the host widget's `+0x172` and `+0x174`. Request 17 stores kind 2 (`0027F98E`–`0027F993`), request 15 kind 3 after `002901B0` stores its parameter as the word (`0027FA11`–`0027FA22`), and request 18 kind 7 (`0027F99D`–`0027F9A2`). The field menu's own world-map entry (`0028E690`) stores kind 1. The host's build arm titles the help line by kind (`00552404`–`00552426`): kind 2 → text `0xC03`, kind 3 → `0xC04`, kind 5 → `0xBFA`, any other kind no text. By the `UQ-299` method (group 3 → loader id 22 → the shipped `help_menu.bin`, 10,856 bytes; `0x82E` and `0x830` reproduce as the control), **`0xC03` is "Choose your destination."**, **`0xC04` is "Airship Route"**, and `0xBFA` is an empty row.
      - **17 is the Strahl destination picker:** the world map in kind 2, titled "Choose your destination.". This agrees with the script census's "Board the Strahl?".
      - **15 is the airship-route map.** Only kind 3 keeps the word (`0028E7AF`–`0028E7BA` clears it for every other kind). The host's build arm hands it to `003BCAF0`, which sets, in the map-data widget's `+0x270` node bitset, both nodes of every link whose byte `+2` equals the word. In the shipped `myoshiok/us/worldmap/menumap_world.bin` (the widget's `+0xD8` resource), the link table (`word[+0xC]` → `0x5C8`, 60 eight-byte entries) numbers exactly fourteen routes. **Routes 1–14 are the seven node pairs 1–12, 1–3, 1–20, 3–12, 3–34, 20–34 and 12–34, each once per direction.** Route 0 is the 45 ordinary links, and 15 a self-link at node 22 with zero coordinates. The parameter is therefore one directed airship leg. Request 2 reaches the same page: the shared 2 / 22 arm sends parameters 1–0x20 to `0027FA11` (`0027F9C1`–`0027F9D7`). Within request 2 only the script-operand path under flag `0x5E` (C-4 above) can carry such a value; request 22's parameters are remapped to `0x40`–`0x42`.
      - **18 is the world map in kind 7,** which gets no help-line title. What kind 7 changes inside the map is not read.
        *Read 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13, §7b R5): nothing inside the map tests for 7, so it draws
        like kind 1, the field menu's own world map. The difference is on close, where 7 ends the request as 2 and 3 do.*
      - **19 is the hunt list.** Its arm calls `0037FF80(parameter)`, which builds a `0xD8`-byte widget with procedure `0037E350`. That builds the `0x5F0`-byte list owner `0037F4D0`, which publishes itself at `02AED490` and loads kind-7 resource `0x128` into `+0xC8`. That resource is `myoshiok/us/quest/menuquest.dat`, the `qstd` table of [five-small-bin-tables.md](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md). The parameter is an entry id: `0037EDB0` returns the row whose packed word carries it in bits 8–17, and a miss falls back to the first row (`0037E3D3`–`0037E404`). The rows' text ids resolve against the id-keyed `test_battle/us/binaryfile/questtitle.bin`, matched by the ids the file contains rather than through the loader. The 45 kind-1 rows are hunt titles: "A Tingling Toast", "The Defense of Ozmone Plain" … "A Dark Rumor", 37 titled and the last 8 empty in this file. The 18 kind-0 rows have empty titles, the leading row's id `0x33550` has no string there, and the two kind-2 rows carry no text id.

      ~~*Still unnamed: 7, 8, 9, 12, 13, 16 and 20, the shared-arm ids.*~~

      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): every id now has an identity or a ruling. 12 is the `spattack` window, and 7, 8, 9, 13, 16
      and 20 have no screen in the image.** The identified-requests table above carries every id.
      - **12.** Its only producer is `002E1AE0`, which stores 12 straight into the mailbox. It is ScriptVM verb `0x2A8`
        (catalogued `openspattackwindow`, through the tail-jump `0034DA80`). The router gives 12 its own arm,
        `0028E970`, outside the generic route. That arm releases the widget ~~at `0209BE80 + 0x10FB0`~~ whose pointer sits at `[0209BE80] + 0x10FB0` and builds a new
        `0x760`-byte one ~~there~~ on the heap, storing its pointer back *(corrected 2026-10-02, OPUS: `0028E970+0x60`; `+0x10FB0` is a pointer slot of the `0x10FD0`-byte block)*. Verb `0x2A9` (`spattackwindowsync`) polls it: `0028F7C0` returns 3 when the widget is
        gone, when its word `+0x752` is 1, or when bit 0 of `+0x749` is set, and 1 otherwise (`0028F7CE`–`0028F7EB`). The name
        rests on the catalogue's `spattack` family (`isfusion_spattack`, `openskillnamewindow_spattack`,
        `spattack_whiteout_menu_callback`), not on a string.
        *Corroborated the same day by the one script that uses the verbs.* The CR-2 triple scan (call opcodes `0x58`,
        `0x59`, `0x5D`, `0x5E` + a 16-bit id) was run over the 1,123 `us` and `bin` `.ebp` files. It finds `0x2A8`,
        `0x2A9`, `0x29E` (`spattacksync`) and `0x2A1` (`isfusion_spattack`) exactly once each, all in
        `plan_master/us/event/spc_z/spc_z0000/spc_z0000.ebp`, a 3,008-byte event script. That is the `spc_` event
        whose name sets the flag `01F832E9` on
        [the event-slot page](../../00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md).
        So the window is opened by the special-attack event and nothing else. Its player-facing name is still not
        read: the script carries no text. *(2026-09-30, DD batch 13, §7b R12: the window's own procedure looks up only
        control-code templates, so no title string names it. Runtime-only: the name needs the screen seen.)* *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: proposed register row Q1, disposition runtime, in [batch 20's record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md).)*
      - **7, 8, 9, 13, 16 and 20.** These have no producer. The request word `0215F1A4` is written in five places:
        - two resets, which write 0 (`002E0B97`, `002E15D9`);
        - the script translator `002E1A60`, whose table yields only 2, 6, 10, 15, 17, 18, 19 and 22;
        - `002E1AE0`, which writes 12;
        - the mailbox `002E1B10`.

        The mailbox's callers post 2 (`00253D78`, `00253EE6`, `00253F44`, `00253F53`, and `0035D750` as 24 − 22) and
        11 (`0035C81E`). The one exception is the developer hook `0050DAB0`, which forwards any value. The router's
        direct callers pass 1, 3 and 24, or replay the last request word. The generic route `00280A00` has one
        caller, the router.
      - **The domain of that absence.** It covers the raw E8 / E9 call index and a conditional-jump sweep, both empty
        for all five entry points, plus an address-taken scan. That scan's only hits are `.pdata`, the hook's verb
        slot, and two unaligned `.rdata` byte matches. In the generic widgets ~~these ids reach only shared arms~~ 7–9, 13 and 20 reach only the default of the open table at `0027FB70+0x520` (`0027FB70+0x49E`), and 16 its own arm (`0027FB70+0x45A` `mov dword ptr [rbx+0xcc], 2`, then the same default) *(corrected 2026-10-02, OPUS: the 21-entry table read from the image)*; 16
        alone first zeroes `0209E5E8` and the UI root's `+0xDE6`. **Like 14 and 21 (C-1 / C-2), they are unused
        request numbers that the debug verb can exercise.**

      *Not established:* the aerodrome names of the route nodes; what world-map kind 7 changes; whether the
      `spattack` window is the Quickening screen (the catalogue labels suggest it, and no string was read); and any
      live observation. **Not established:** the aerodrome names of nodes 1, 3, 12, 20 and 34 (five nodes and seven legs, not resolved from data here); what kind 7 changes; which native path, if any, issues 15, 18 or 19 in play; and any live observation. The evidence is a static reading plus a decode of the shipped data.
      *Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13), three of the five:* the five aerodromes are
      Rabanastre (1), Nalbina Fortress (3), Archades (12), Bhujerba (20) and Balfonheim Port (34) (§7b R6); kind 7 is
      §7b R5; and no native path issues 15, 18 or 19, by the producer census above (the request word's writers give
      them only through script selectors 3, 1 and 4, and through the debug hook). Whether the `spattack` window is the
      Quickening screen, and any live observation, are runtime-only. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: whether it is the Quickening screen is part of proposed row Q1, disposition runtime; any live observation states the scope of this evidence.)*

## 7b. Residue read statically, 2026-09-30 (SWE2-CONTRACT for OPUS)

DD batch 13 (`OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`). Every item below is pinned by
`_index/candidates/swe2contract-ddres-b13-0930/b13_checks.py` (checks R1–R14, FAILS 0) on the certified image, the
shipped US text files and the shipped world map.

- **R1. Who clears the request word.** `00252D90` reads `02092730`, cancels the request's system stop (`00225CD0`
  on the handle from `00255290`, or `002260A0` for id 11 without one), then zeroes `02092730` and `02092734`
  (`00252DC5`, `00252DCB`). It is called from sixteen sites: the generic route's area controller `00280140` (message
  18, `00280286`), request 12's arm `0028E970`, request 24's widget, `0035C960`, `0035CF50`, `0035D8D0`, `0035DA80`, the
  `003C8990`–`003C8B70` bodies (seven sites), `00279E20` and `00290780`. The area
  unload `002628B0` runs the reset `00252DE0`, which zeroes both words too. Image-wide, `02092734` has exactly these
  two writers and the setter `00252B46`.
- **R2, R3. Request 24, "party incapacitated".** `0035D6B0` serves requests 3 and 24 (request 3's route builds it
  through `0035D080` when `022C83E8` bit 6 is set). For 24 it posts the request word and sets capability-policy row 8
  bits 0 and 20 (`002E1C20`). After a 24-step countdown it opens a confirm dialog (`00241C90`) whose text is
  `menu_message.bin` `0x86F`, *"All members of the party have fallen. Reform the party with one or more reserve
  members."* (request 3's text is `0x86E`, *"Select a new party leader."*). A message 12 carrying `0x8100`, the
  dialog's confirm reply on the shared-dialog page's reading, closes the widget. On close it clears the word, clears the two policy bits and posts **request 2 with parameter 0**, the Party
  Menu. In player terms: when the whole active party is down and reserves remain, the game says so and opens the
  party menu to swap them in. `0035BC50` runs only on the request-3 arm.
- **R4. Request 11, game over.** The widget family `003EF750`–`003EFCC0` looks up no text id (no `002F9860` call and
  no text-id immediate), so its wording is in the resources its two descriptors load (`00D11C88`, `00D11CA0`).
  Proposed row P1 *(answered 2026-09-30, DD batch 15, §7c)*.
- **R5. World-map kind 7 (request 18).** The kind is written as 1 by the field menu (`0028E690`, `00281ED0`,
  `00291750`), as 2, 3 and 7 by requests 17, 15 and 18, and as 6 by `002804E0`. Inside the map nothing tests for 7.
  The host compares its kind word only with 6, its title switch covers 2, 3 and 5, and the map widget's node rule
  covers 0, 2, 3, 4 and 6. So kind 7 draws the nodes and leaves out the title exactly as kind 1 does. The one test for
  7 is in the close router: the host closes with code `0x418`, and `002814E0`'s arm `0028179B` ends the fullscreen
  request for kinds 2, 3 and 7 (`00244F00` on context `+0x100`) but returns to the field menu's world map for every
  other kind. In player terms, request 18 is the field menu's world map opened as a stand-alone screen: closing it
  goes back to the game, not to the menu.
- **R6. The airship legs.** The route nodes of `menumap_world.bin` are named through `menu_mapname.bin`: 1
  Rabanastre, 3 Nalbina Fortress, 12 Archades, 20 Bhujerba, 34 Balfonheim Port. Routes 1–14 are
  Rabanastre–Archades (1, 2), Rabanastre–Nalbina (3, 4), Rabanastre–Bhujerba (5, 6), Nalbina–Archades (7, 8),
  Nalbina–Balfonheim (9, 10), Bhujerba–Balfonheim (11, 12) and Archades–Balfonheim (13, 14), each pair listed in both
  directions. Route 15 is the self-link at node 22, the Ogir-Yensa Sandsea.
- **R7. Request 2's parameter.** The close table `00280048` sends request 2 to `0027FC9C`. Parameter 0 opens the
  `0x288`-byte menu widget (`00280D20`, procedure `00280DE0`), and any other value goes to the fullscreen procedure
  (`0027F540`). Its shared 2 / 22 arm (`0027F9C1`–`0027F9F1`) opens the airship-route page for `1`–`0x20`, the map
  tutorial for `0x42`, and the location map `0028E660(1)` for everything else, `0x21` included.
- **R8. The battle menu's builder.** `00290CF0`, group `0x2000` of the update gate, tests `+0x10F68` bit `0x10`. While
  `02092730` is 0 it passes the id at `+0x10F60` to `00276650`, which builds the `0x61F0`-byte widget with procedure
  `00279E20`.
- **R9. The controller's `+0x598`.** Image-wide there are three byte stores at displacement `0x598`. Two are in the
  gambit-screen bodies `0056B4D0` and `0056BE40`, and the third is the slot selector's `0058052A`. The controller
  `00582860` only compares the byte (`00582E8A`), and the widget factory's initialiser zeroes each new object
  (`00246626`). *Limit:* a displacement census does not see a store through a rebased pointer or a block copy.
- **R10. Bit 12 of `[02EBF190] + 4`.** This bit selects SpawnKeep image B (`00236760`). Three functions set or clear
  it: `00233C10` (the battle-state guard, under `02089344` bit 0), `00239960` (copied from a saved flag word) and
  `0023A390`, whose callers are the load normaliser `00584210` and the handler `0050F500` of script verb `0x308D`,
  which the verb table leaves unnamed. What the bit stands for is proposed row P3 *(answered 2026-09-30, DD batch 15, §7c)*.
- **R11. The text stepper.** `002ABF70` has one call site, `002A9945` in the parser slot `002A8C50`, which has no
  direct caller.
- **R12. The `spattack` window.** Its procedure `002D5EB0` looks up text only through `002D5170`, and the four ids
  there (`0x4669`, `0x466A`, `0x466C`, `0x46B4`) are control-code templates in `menu_command_template.bin`, not a
  title.
- **R13. No native producer of 15, 18 or 19.** The translator `002E0DA0` has one caller, `002E1A60`. That function's
  two callers are the handlers of the two `openfullscreenmenu` verbs (`003462D0` for `0x48D`, `003470D0` for
  `0x472`).

**Proposed register rows, id-less, for SWE2-DATA (SWE2-CONTRACT for OPUS):**

| # | question |
|---|---|
| P1 | What the game-over screen shows: which shipped resources the descriptors `00D11C88` and `00D11CA0` name (loaded by `003EF830` through `00393460` and `003933F0`), and what words they draw. The widget family looks up no text id |
| P2 | The authored name, or the setting script, of scenario flag `0x5E`, which `00253C70` tests through `0032A8A0` to choose request 2's operand-word parameter |
| P3 | What state bit 12 of the battle-system flag dword `[02EBF190] + 4` denotes. Writers: `00233C10` at `00233C6E`, `00239960` at `00239A35`, and `0023A390` (callers `0050F500`, the handler of verb `0x308D`, and `00584210`). It selects SpawnKeep image B in the persistence-pair capture and restore |
| P4 | Whether field id 0, the target the area controller requests after an invalid save header (`00280140`, bit 8 with target 0), is the title screen |

*Answered 2026-09-30 in §7c (SWE2-CONTRACT for OPUS, DD batch 15): P1–P4 need no register row.*

**Runtime-only (SWE2-CONTRACT for OPUS):** how long a request word stays set; the delivery order of the save
controller's message 18 against the area controller's message 2, and whether the fullscreen widget is still in place
when message 15 arrives; how many parses a frame runs; the `spattack` window's player-facing name, which needs the
screen seen; any live observation of requests 15, 18 or 19. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: the delivery order and the widget at message 15 are proposed row Q2 and the `spattack` name row Q1, both runtime, in [batch 20's record](../../_index/candidates/swe2contract-ddres-b20-1001/README.md). How long a request word stays set and how many parses a frame runs are quantities of play, kept as stated limits. Requests 15, 18 and 19 have no native producer (§7b R13), so observing them is a scope statement.)*

## 7c. Rows P1–P4 answered statically, 2026-09-30 (SWE2-CONTRACT for OPUS)

DD batch 15 (`OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`). Every item below is pinned by
`_index/candidates/swe2contract-ddres-b15-0930/b15_checks.py` (checks G, F, B and T, FAILS 0) on the certified image, the shipped menu files of every language folder and
the decompiled `us` scripts. None of the four needs a register row.

- **P1. The game-over screen shows the words GAME OVER, and they are drawn from an image.** `00D11C88` is
  `{kind-7 id 0x39, name gameover_c}` and `00D11CA0` is the one-id list `{0x38}`. Through the kind-7 path array they are
  `tm2_menu/gameover_c.tm2` and `mrp_menu/gameover.mrp`. The image is one 1024 × 256 8-bit TIM2, byte-identical in all
  nine full-size language folders (only the SD folder `in_sdver` differs). Its ink falls in two groups split by one wide
  gap, four glyphs and then four, and the decoded render (`gameover_c_us.png` in the record) reads *GAME OVER* in
  red-glowing capitals. The layout `gameover.mrp` has three records: the image at (474, 432); a 360 × 96 box at
  (1212, 878) that names the third record; and that record, one text slot whose string id is −1, which the type-5
  constructor treats as no string (`0029FF45`). The widget family looks up no text id (§7b R4), so the image is the
  screen's only wording. The two words rest on the render; the files, ids and layout are pinned. In player terms: the
  game-over screen is the same picture in every language.
- **P2. Flag `0x5E` has no authored name. By its role it is the airship-trip flag.** It is bit 6 of byte 11 of the
  Primary bank, the map-jump-group flags of [the persistent flag banks](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md).
  The scripts set it with `setmapjumpgroupflag(94)` four times in each aerodrome script (`alc_e01`, `byu_b01`, `nac_b01`,
  `rbn_b01`, `var_b01`), at least once in each in the function `高速移動時のマップジャンプ` ("map jump for high-speed
  travel"), and every time immediately before `mapjump(124, …)` or `mapjump(125, …)`, the airship fields `asp_a01` and
  `asp_a02`. `rsn_z02` sets it once, in its resident director's `init`, next to `global_flag[2] = 15` (route 15, §7b R6).
  `asp_a02` releases it three times and `rsn_z02` once. No script tests it, nothing native sets it, and the new-game
  list `mapjumpgroupinit.bin` does not include it. While it is set, Triangle posts request 2 with operand-bank word 2,
  the scripts' `global_flag[2]`, which the aerodrome scripts use for the route; when that word is 0 the parameter is
  **1**, not 0 (`ebx` = 1 from `00253D14`; §6's sentence is corrected). By §7b R7 every value `1`–`0x20` opens the
  airship-route page. In player terms: during an airship trip, Triangle shows the route page instead of the location
  map. The id is a literal operand in the compiled scripts and no shipped file names it, so the row is answered by role.
- **P3. Bit 12 says that the session was loaded through load mode 3, the title's Trial Mode route.** The save / load
  controller sets `02089344` bit 0 exactly when the load mode `00394450()` is 3 (`00582CBA`–`00582CDE`). `00233C10`,
  run through `00285E60`, copies it into bit 12 and consumes it (`00233C6E`, `00233C7C`), and clears bit 12 whenever it
  runs with the global bit clear (`00233CA6`). `00239960` only keeps the bit across its `002370C0` rebuild. The two
  script arms, verb `0x308D` (`0050F500` → `0023A390`) and verb `0x308F` (`0050F5A0` → `00238A30(1)`), are called by
  no shipped script (control: their neighbour `0x308C`, 854 calls), and the restore path clears the bit (`00584393`).
  FV-1 rules mode 3 the title's Trial Mode route. So persistence image B is the Trial Mode session's, the save
  finaliser stamps the restore flag from the bit, and while it is set the field-menu request paths at `00253E10`,
  `00253ED4` and `00253F11` are skipped, Triangle's included. The three verbs are unnamed, so the bit is answered by
  role. In player terms: a Trial Mode session keeps its own spawn-keep image and cannot open the map from the field.
- **P4. Field `0` becomes the title.** After an invalid save header the area controller requests target 0
  (`002803A3`–`002803B3`), and message 18 hands any target but `0xC` to `00314440` (`00280252`–`0028027C`).
  `00314440` replaces a zero target with field `0xC` while `00408B00()`, the debug byte `02B62DB9`, is 0
  (`0031445E`–`0031446E`), and that byte's only store image-wide is the reset's 0 (`00408BBC`), as
  [the debug-global page](../../19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md) records. Field
  `0xC` is `ttl_a01`, the title map (kind-5 path array `01EE23A0`). Field 0's own path, `tst_a01`, is a bare test map
  (four party members, no exits) that only a set debug byte would reach. In player terms: a save that fails the header
  check returns the player to the title screen.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Router mechanism and dispatch | complete body of `00254B50` (263 B, `9ab5c3f6...4d78`) | 1 |
| Triangle -> request 2 | exact disassembly in `00253C70`: `CMP EBP,0x1000` ... `LEA ECX,[RDX+2]` `CALL 002E1B10` | 1 |
| Decide/Square -> request 1 | `00253C70` tests `01E0C2A0 \| 0x8000` then hardcodes requestId 1 | 1 |
| DecideButton is authored config | settings entry 25 literal key `DecideButton` with `Circle`/`Cross` labels; getter `0017E210` | 2 |
| Selector translation table | complete body of `002E0DA0` (104 B, `7869990c...6a78`) | 1 |
| Mode 14 -> request 14 | complete body of `002E0E30` (236 B, `467b1045...aa398`) | 1 |
| `debug_open_triangle_menu2` binding | ff12-script catalog `0x2037`; handler `0050DAB0` (25 B, `c26b8b8f...09d25`) tail-jumps to `002E1B10` | 9 |
| No ordinary producer for 14/21 | complete direct CALL/JMP census over authorized `.text` | 1 |

## 9. Related

- [`../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md)
- [`../../11-Party/`](../../11-Party/) - request 3 commits party leader via `0035BAA0`

## Re-verification 2026-09-02 (AH-11)

Stamped against parent `381d2aea...`; re-checked against the current `2ed8affb...`.

**Addresses:** 28 cited - 21 function entries, 7 interior - 0 unresolved.

**Central claim re-derived.** The document states that `00254B50` is the router and *"dispatches IDs
`1..24` through a native switch"*.

Decompiled fresh, `00254B50` contains `switch (uVar5)` whose case labels run from `case 1:` to
**`case 0x18:`** - and `0x18` is **24**. The documented range is exact at both ends.

Individual case labels recovered from the decompilation: `1`, `3`, `4`, `5`, `0xC`, `0x18`. Others
are grouped or elided by the decompiler, so the *set* of live ids is not fully enumerated here - only
the bound, which is what the claim asserts.

> **Upgraded 2026-09-02 by the switch-label sweep.** The set **is** now enumerated, and this
> section's caution was well placed. `00254B50` has **exactly six case labels plus one `default`**:
> `1, 3, 4, 5, 12, 24`. The switch is **sparse, not a range** — the other 18 values between 1 and 24
> fall to `default`. Grouped labels would still print individually (as they do in `002ABF70`), so
> nothing is hidden.
>
> ~~**For a modder this is the load-bearing correction:** "IDs `1..24`" describes the *bound*, not the
> vocabulary. There are **six** live request ids, not twenty-four.~~ **Struck 2026-09-11
> (ASTRA-CONTRA-FABLE-UI-DEFAULT): the `default` arm is not a rejection — it is the generic route.**
> `00254C2D` calls `0028F970` and then `00280A00(originalRequest, parameter, flag)` — the same
> generic scheduler the dispatch table above already lists for `2`, `6–11` and `13–23` — and the
> range test `lea eax, [rbx − 1]; cmp eax, 0x17; ja default` (`00254BD6`–`00254BDC`) sends every
> value outside `1..24` there too. So the six labels feed **five** special arms (`1` and `4` share
> `0035D660`; `12`'s arm returns 1 regardless of its callee, `00254C1D`) and the sixth arm is
> generic; the request vocabulary is whatever `00280A00` accepts, ~~which this page has not read~~ which §2 reads
> (*The generic route*, 2026-09-11) *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 13))*.
> One detail the special arms hide: they receive the normalised id (`ecx & 0x7FFF`, `ebx`), the
> generic arm the *original* dword (`ebp`), so `0x8001` reaches `0035D660` as `1` while `0x8002`
> reaches the scheduler as `0x8002`. ASTRA's
> [EXP-067](../../_experiments/EXP-067-ui-router-controls.md) ran the 263-byte body with its three
> tables over 72 fixtures — all 24 ids, 0 / 25 / 32 / 32767, every policy bit, the global gate — with
> the seven callees as recording stubs; a mutant handing the generic route the normalised id is
> rejected. The sweep's own point stands: the *labels* were counted right; the reading of what
> `default` means was mine, and wrong.

**This document is the sweep's control case.** Every other switch claim checked on 2026-09-02 either
overstated a case set or was written from a truncated excerpt. This one enumerated what it had, said
plainly what it had not covered, and claimed only the bound - and it is the only one that needed no
correction. See
[`../../99-Unresolved-Residual/the-unresolved-158.md`](../../99-Unresolved-Residual/the-unresolved-158.md) §12.

**Stamp advanced because the body was re-read**, per the evidence standard.

## `002ABF70` opened — 2026-09-03, session `repos-78`

This document cited `002ABF70` **at its entry only**, as did three others. It was the top entry on the
corrected *leaned on and never opened* cut. It is opened here; nothing above is retracted.

**Extent checked first**: 122 instructions, ends `ret` at `002AC1B0`, **no `jmp` leaves the extent** —
the tail-call hazard does not apply. **No loops at all**, five `ret` sites, twelve `cmp`: the shape of
a per-frame state step, not a processing pass.

### An eight-mode jump table, with the table in `.text` after the `ret`

```asm
002ABF79  mov   ecx, dword ptr [rcx + 0xb0]        ; mode word
002ABF7F  movzx eax, cl                            ; the MODE is its low byte
002ABF82  cmp   eax, 7
002ABF85  ja    default
002ABF8B  lea   r8, [rip - 0x18bf92]               ; = 00120000, the image base
002ABF92  mov   edx, dword ptr [r8 + rax*4 + 0x18c1b4]
002ABF9A  add   rdx, r8                            ; arm = RVA + image base
002ABF9D  jmp   rdx
```

**The table is at `002AC1B4`, four bytes after this function's `ret`** — the same construction as the
developer console's dispatcher, and it resolves the same way: a dword RVA plus the image base.

| mode | body | |
|---:|---|---|
| 0, 1, 4 | `002AC06B` | three modes share one body |
| 2 | `002AC04F` | the only mode that consults the flag bit |
| 3 | `002ABF9F` | |
| 5 | `002ABFFC` | |
| **6** | `002AC1AB` | **the function's exit — mode 6 does nothing** |
| 7 | `002AC18B` | |

**Eight modes, six distinct bodies, and one of the eight is a no-op** that jumps straight to the
epilogue.

### The state block it steps

Every body reads and writes fields of the object in `rcx`. The offsets and their widths are exact;
the names are descriptive of use, not recovered:

| offset | width | role, from how it is used |
|---|---|---|
| `+0x5A` | `u16` | **the widget's brightness** — *corrected 2026-09-13, this table first called it "a countdown"*; **zeroed outright when bit 22 of the mode word is set** (`bt ecx, 0x16`), otherwise decremented while positive. It is the field [the rectangle primitive](../../99-Unresolved-Residual/drawing-one-coloured-rectangle.md) scales three colour channels by, [the blinking icon](../../99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md) modulates with its sine, and [the widget-tree draw pass](../../99-Unresolved-Residual/the-widget-tree-draw-pass.md) inherits multiplicatively as `(node[+0xA1] × parent[+0x5A]) >> 7`. **Decrementing it to zero is a fade-out, which is what mode 2 is** |
| `+0x88` | `u16` | a delay; decremented, and **on reaching zero sets `+0x9B` to `0x1E` and clears the mode byte** |
| `+0x8C` | `i16` | the target value, **clamped to `0x7D00` = 32,000** at two separate sites |
| `+0x8E` | `i16` | a saved copy of the target |
| `+0x90` | `i16` | the current value; advanced toward the target by `+0xA0` |
| `+0x92` | `i16` | the previous value, written from `+0x90` before each advance |
| `+0x9B` | `i8` | an accumulator, **compared against `0x1E` = 30** |
| `+0x9C` | `u8` | the per-step increment added to `+0x9B` |
| `+0x9D` | `i8` | a phase, moved toward `+0x9E` by `±[+0xA0]` |
| `+0x9E` | `u8` | the phase limit |
| `+0xA0` | `i8` | **the signed step**, added to `+0x90` and to `+0x8C` |
| `+0xB0` | `u32` | **mode in the low byte, flags above it** — bit 22 is read by mode 2 |

**Two constants govern the whole thing**: `0x1E` (30) as the accumulator threshold, and `0x7D00`
(32,000) as the ceiling on both `+0x8C` and its advance.

> **`+0xB0` is one dword carrying both a mode and flags.** The dispatcher reads it whole and then takes
> `cl`, so **a reader who treats `+0xB0` as a byte gets the right mode and loses bit 22 entirely** —
> and mode 2 is the only body that reads it.

**Disposition of the `verify_doc_addresses` review flag.** `002AC1B4` is cited as a `.text` address
that is not a function entry. **Confirmed legitimate:** it is the jump table itself, four bytes past
this function's `ret` — the case the checker asks to have confirmed. The six body addresses are
interior addresses of `002ABF70` for the same reason: switch arms are not functions.

### What is not established

- [x] ~~**UQ-163.** **What this state block belongs to.** The field roles are read from use; **no caller was traced~~
      and no allocation site was found**, so what is being animated toward a 32,000 ceiling is unknown.
      ***ANSWERED 2026-09-17 (FABLE): the allocation half closes too: the block is a value-type text-draw state embedded where it is used, in the caption and message widgets or on the stack of the text helpers, and no drawer object is ever allocated on its own.** The 2026-09-16 finding placed `002ABF70` in slot 1 of the drawer table's kind-0 group. The three dispatchers that reach that table, `002ABEC0`, `002ABF20` and `002B3930`, index it by the object's kind byte `+0xA3` times three (`002ABEF1`..`002ABF0F`, `002ABF41`..`002ABF5D`, `002B3930`..`002B394C`), jump to the slot with the same object in `rcx`, and the first two also publish the object's `+0x8C` into the global drawer state `[0209CC40] + 0x10D8` and zero `0209CC48`. Their nine callers show what that object is: `00227EE0`, the GeneralFrame/MessageLine/NobuMessage widget procedure, passes its widget `+0xC0` (`00227F9C`; the widget is `0x190` bytes from [the factory](../Widget-Object-Model/CONTRACT-widget-object.md) at `00227EB8`); `00241D40` and `0057C480`, the ConfirmCaption procedures, pass widget `+0xE0` (`002421A5`, `0057C8E7`, `0057C9B7`; `0057C480`'s widget is `0x640` bytes, `0057C39F`); `002A3730` and `002A5CC0` pass their object's `+0xD0` (`002A37BB`, `002A37D5`, `002A5CED`); and `002A3250`, `002A5590` and `002A6C40`, the measuring helpers, pass stack locals (`[rsp + 0x130]`, `[rbp - 0x40]`, `[rsp + 0x60]`; `002A3492`, `002A56A7`, `002A6D48`). So what is animated toward the 32,000 ceiling is the text state of whichever widget or helper embeds the block, and the drawer table's `this` is that embedded state. Static, dispatchers and every caller read at the call.*
- [x] ~~What `00248F20` (25 B) returns — mode 2 calls it and proceeds only when it returns `1`, but only
      when `+0xA0 <= 1`.~~ **ANSWERED 2026-09-13 (OPUS): it returns `1 + (frameMode == 2)`, so it is
      `1` or `2` and nothing else — the router's gate is the FRAME MODE.** All 25 bytes:

      ```asm
      00248F20  sub  rsp, 0x28
      00248F24  call 00229EA0          ; 8 bytes: movsx eax, byte [02064AD3] ; ret
      00248F29  xor  ecx, ecx
      00248F2B  cmp  eax, 2
      00248F2E  sete cl
      00248F31  lea  eax, [rcx + 1]    ; 1, or 2 when the byte is 2
      00248F38  ret
      ```

      `00229EA0` is an 8-byte accessor over the **signed** byte at `02064AD3`, and the corpus already
      names that global on three other pages — *"frame dispatcher `0022A580` (mode byte `02064AD3`)"*
      in [the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md),
      *"mode byte `02064AD3` in {2,3,5}"* in
      [the input stack](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md), and
      *"while the mode byte `02064AD3` is 2 (`00229EA0`)"* in
      [the resource request queue](../../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md).
      **The identification is theirs; what is added here is that this router predicate is the same
      byte, one accessor away.**
      **So "proceeds only when it returns 1" means: proceed unless the frame dispatcher is in mode
      2.** The predicate cannot return anything but `1` or `2`, so the test is total — there is no
      third outcome for a caller to handle, and the `+0xA0 <= 1` condition is an independent gate
      stacked on top of it rather than a refinement of it.
      **~~Not established here: what mode 2 *is*.~~** The resource queue keys its own behaviour on the
      same value, so the two paths are gated on one state, but naming that state is those pages'
      business and neither of them names it either.
      **NOW ESTABLISHED 2026-09-13 (OPUS): mode 2 is a fade-out**, by the `+0x5A` correction in **The state block it steps** above — the field this document called "a countdown" is the brightness three widget documents
      multiply colours by, and mode 2 walks it to zero (or clears it at once when bit 22 is set).
- [x] ~~What `002ABB20` (918 B) does; mode 2 calls it after copying the target into `+0x8E`.~~
      **ANSWERED 2026-09-13 (OPUS): it was already read in full, on a page this document does not
      cite. `002ABB20` scrolls a text window by one step and snaps to a line boundary.**

      [Measuring text by drawing it with the output off](../../99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md)
      §3–§4 has it: `002ABB20` lays the text out from the current line, and **if no boundary is in
      reach it simply advances `+0x90` by the step at `+0xA0`; otherwise it probes each of the next
      `step` lines through `002B20B0` (line index → byte offset) and stops at the first that comes
      back under 2.** It measures with a **borrowed stop-set** — saving `ctx[0x10C8]`, installing
      `00916548`, calling, and restoring — **at both of its call sites**, which is that page's own
      falsification control: *a field a function restores is not its own.*

      > **THE TWO PAGES DOCUMENT THE SAME FUNCTION AND THE SAME OBJECT, AND NEITHER CITES THE
      > OTHER.** That page's §5 *"the animation stepper"* is **`002ABF70`** — the dispatcher this
      > document opened — switching on `state[+0xB0] & 0xFF` over states 0–5 and 7, with `+0x88`,
      > `+0x8C` (*"clamped at 32000"*), `+0x8E`, `+0x90`/`+0x92`, `+0x9B`/`+0x9C`, `+0x9D`/`+0x9E`
      > and `+0xA0` in a field table that lines up with **The state block it steps** above **row for row**.

      **Each page holds what the other lacks, and that is the useful part.** This document has the
      flag bit 22, the `0x7D00` ceiling, and that mode 6 is a no-op jump to the epilogue; that one
      has **what the object is** — a scrolling text window — and therefore what the fields mean:
      `+0x8C` is the **target line** and `+0x90`/`+0x92` a following pair trailing it, not bare
      "values". **`check_consistency` passes on both** — it compares stated names and sizes, and two
      pages describing one function in different prose collide in neither.

      **Not established by this join:** what `002AF340` returns (that page says so outright, and the
      `< 2` boundary test rests on it), and what `00916548` contains.
      *Answered on other pages (marked 2026-09-30, SWE2-CONTRACT for OPUS, DD batch 13):* `002AF340` returns the
      heavy-node count, or −1 under its `r9` gate, as executed in EXP-208
      ([the auto-status contract](../../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) §13q). `00916548`
      holds the control code `0F 23` (`&0x230F`), which `002ABB20` installs as the painter's terminator word
      ([the text-control contract](../CONTRACT-text-control-codes-and-dyngeo-draw.md), *the painter's `+0x10C8`
      terminator word*).
- [x] ~~Whether the `0x1E` threshold is frames. It is compared against an accumulator that grows by an
      authored per-step amount, so **it is a count of steps, not necessarily of frames.**~~
      **Answered 2026-09-14 (FABLE): no, it is a fixed-point denominator of 30.** Each stepper call adds `+0x9C` to
      `+0x9B` and scrolls only when the sum reaches `0x1E`, then clears it (`002AC003`–`002AC01D`, `002AC072`–`002AC0A0`).
      So `+0x9C` is the step rate in thirtieths per call: 30 scrolls every call, 15 every second call. The text markup
      `/` tag writes exactly that: `+0x9C = 30` and `+0xA0 = v / 30` lines per step, halved (floor 1) when `00248F20`
      returns 1 ([numeric formatting](../Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md), the `/`
      tag). The delay expiry at `002ABFBC` also sets `+0x9B = 30`, which makes the next call step at once. How often the
      stepper itself is called per frame was not traced. *(2026-09-30, DD batch 13, §7b R11: it has one call site,
      `002A9945` in the parser slot `002A8C50`, so it steps once per parse of its text state. How many parses a frame runs
      depends on the windows on screen and is runtime-only.)* *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 20: a stated limit.)* The `00248F20` halving is the only frame-mode term in the
      arithmetic.

## The `0027FB70` exclusive subtree — all 10 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the generic request's first widget proc **10 frontier
functions**. Every member body was disassembled from the shipping image within its declared
extent (2026-09-14). `0027FB70` (1,237 B) is a message proc: `[rdx]` selects **message 1 =
open** (`0027FD74`), **message 2 = tick** (`0027FBC3`), **message 18 = unpublish**
(`0027FBA4` — `*(0209AC30)+0xB8 = 0`); every other message tail-jumps `005C5230`, the
three-byte return-0 stub. The open arm derives a duration `ebp = bit15 ? 1 : 0xC8` and a
fast flag `r15d = (req>>0xD)&4` from the request word, tears down the old presentation child
(`002909F0`), stores the duration (`002CC9F0`), publishes `self` at `*(0209AC30)+0xB8`
(`0027FE02`), copies `{request, parameter, flag}` to `+0xC0`/`+0xC4`/`+0xC8`, then dispatches
on `(request & 0x7FFF) − 2` through the 21-arm table `00280090`; each arm scales `ebp`
milliseconds to frames (`×60/1000` via the `0x10624DD3` magic multiply) and feeds the
transition/widget builders before the `00247950(self, 0)` attach. The tick arm is a state
machine on `+0xD0` ∈ {0..4}: 0 arms it from `+0xCC`, 1–3 walk the `00254A80`/`00254A60`/
`002549F0` gates and the `0024AC10`/`0024AC00` pair, and 4 clears `+0xDF4` and dispatches the
same masked request through the 18-arm **close** table `00280048`; when `+0xCC` reaches 0 the
tail calls `00245020(self)` — the teardown §19.2 of the spawn page separates from attach.

| cluster | members | role | interior |
|---|---|---|---|
| dispatcher | `0027FB70` (1,237 B) | message proc: open arm publishes self and runs the 21-arm `(request & 0x7FFF) − 2` table `00280090`; tick arm drives the `+0xD0` state machine and the 18-arm close table `00280048`; message 18 unpublishes | `0027FE02` (`mov [rax+0xB8], rbx` — the self-publish into `0209AC30`) |
| open preamble | `002909F0` (146 B), `002CC9F0` (14 B) | `002909F0` tears down `*(0209BE80)`'s `+0x10F00` child — `0028C4F0`, clears `+0x10F68` bit 3, `+0x10EF0 = 0`, `0028C940(+0x7EA0)`, marks the `+0xD70` chain via `0028C560`, then `0028C4B0` and stores the result back; `002CC9F0` writes the duration to `*(0209AC30)+0xDF0` | `00290A57` (`call 0028C560` — the chain mark) / `002CC9F7` (`mov [rax+0xDF0], ecx`) |
| tick gate pair | `0024AC00` (7 B), `0024AC10` (21 B) | `0024AC00` returns `[02091094]` (state-3 test); `0024AC10` stores `1` to `02091094` when `ecx == 1` and returns 0, otherwise tail-jumps `0024AC30` | `0024AC06` (the getter's `ret`) / `0024AC15` (`mov [02091094], ecx`) |
| event `0xF0` | `0027F540` (142 B) | gated by `*(0209AC30)+0x100`; `002C99A0` with the `01E0C3B8`/`01E0C3BC` pair (bit 15 of the request selects the constant 1 variant), then widget factory `00244F50(0xF0, 0027F5D0, {request, parameter, flag})` — the close arm's re-issue of the request | `0027F5B7` (`call 00244F50` — the `0xF0` construction) |
| event `0x288` pair | `00280D20` (189 B), `002D7070` (123 B) | both gated by `*(0209AC30)+0xD8`; each posts `00244F50(0x288, …, {0, ecx, edx})` — `00280D20` with proc `00280DE0`, `002D7070` with `002D70F0` — followed by `002C99A0`; `00280D20` additionally lazy-builds `*(0209C318)` via `00244F50(0xC0, 0029D340)` + `00247570(00915C10)` + `00246AC0` | `00280D6D` (`call 00244F50`) / `002D70BD` (`call 00244F50`) |
| event `0x268` | `0057B800` (138 B) | for `ecx ≥ 0`: `002C99A0` on the same pair plus `or [0024A5A0(01E0C1F8)+0x38], 0x80` (~~marks a widget record~~ re-admits that atlas to the layout pass - *corrected 2026-10-01, OPUS*); unconditionally posts `00244F50(0x268, 0057B890, {0, ecx})` | `0057B855` (`or dword [rax+0x38], 0x80` — the record mark) |
| chain mark | `0028C560` (36 B) | writes `5` to `+0xD54` of every node in the `+0xD70` intrusive chain — `002909F0`'s teardown marker | `0028C570` (`mov [rcx+0xD54], ax`) |
| flag setter | `00251F20` (32 B) | `*(020927F0)+0xE8` bit 3 ← `ecx & 1` — the id-10 open arm's flag write | `00251F36` (`shl ecx, 3`) |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE, 26 edges.** Cited router functions are called by `MainLoop_UpdateAndRenderFrame` (3), the 978-byte core start-up root, a 387-byte start-up body and core bodies of 463 and 465 bytes. They call small core helpers (7 and 40 bytes, 3 each; 8 bytes twice; 15 bytes) and the 2,001-byte core frame body.
- **ActorEntity - CLIENT and SERVICE (16 edges).** `00226280`, `00226BE0`, `00236760`, `002EFA70` (+1 more) are called by bodies filed to ActorEntity: ActorManager_RunFieldRuntimePass (`0025D9E0`), `00263230`, `00263660`, `0026C5D0` (+1 more); `00226BE0`, `002371B0`, InputGameplay_ArbitrateDigitalInputAndModalState (`00253C70`), `00300060` (+2 more) reach bodies filed to ActorEntity: BattleUnit_GetSlotCount (`00236850`), `0025B4C0`, `00263FF0`, BattleUnit_FindMappedDefinitionSelectorByIndex (`0031B810`) (+4 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT and SERVICE (2 edges).** `00264640` is called by bodies filed to CombatAI: AiTargetSelector_ResolveOperandValue (`00321190`); `00233C10` reaches bodies filed to CombatAI: GambitRuntime_RebuildAllOrderSets (`00327F80`) - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - SERVICE (2 edges).** `00233C10`, `00235AF0` reach bodies filed to Gameplay: BattleSystem_ResetRuntimeState (`00237DF0`), BattleEncodedId_IsValidForClass (`00322C50`) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (36 edges).** `0017E210`, `00236760`, `00247950`, `00254B50` (+8 more) are called by bodies filed to Input: `0022A4F0`, InputGameplay_ArbitrateDigitalInputAndModalState (`00253C70`), `00291D90`, `002E09A0`; `00182D40`, `00226280`, `00228C70`, `0022A580` (+8 more) reach bodies filed to Input: `0017DE10`, `00182D40`, `00182D80`, `001986E0` (+18 more) - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT (2 edges).** `002E1C20`, `002E1CA0` are called by bodies filed to InputGameplay: `00313A00` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (5 edges).** `00226BE0`, `0035BAA0`, `0035BC50` reach bodies filed to Party: PartyRoster_GetActorBySlot (`00263750`), PartyFocus_GetPreferredDefinitionSelector (`003271D0`), PartyFocus_GetCurrentPackedActorHandle_Thunk (`003272E0`), PartyFocus_SetPreferredDefinitionSelectorAndRefresh (`00327850`) (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (30 edges).** `00229EA0`, `00246AC0`, `00247510`, `00247950` (+8 more) are called by bodies filed to Presentation: `002528A0`, `00291320`, `002B0280`, `002B7B80` (+16 more); `00226280`, `00241D40`, `0029D340` reach bodies filed to Presentation: `002DBDD0`, `002DC290`, CharacterRenderSystem_SetDistanceCullEnableByRequester (`002EBBF0`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (24 edges).** `001831A0`, `00229EA0`, `00236760`, `00254CB0` (+7 more) are called by bodies filed to Script_VM_Native_Bridge: `0033FD40`, `003462D0`, `003470D0`, `0034E0B0` (+17 more); `003462D0`, `0050DAB0` reach bodies filed to Script_VM_Native_Bridge: VMValueStack_PopInt32CoerceFloat32 (`00267E10`) - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - SERVICE (2 edges).** WorldTransitionSnapshot_RestorePersistencePairForActiveSlot (`005843E0`), WorldTransitionSnapshot_CapturePersistencePairForActiveSlot (`00584580`) reach bodies filed to Spawn_Encounter_Lifecycle: SpawnKeep_SerializePersistenceBanks (`00233440`), SpawnKeep_RestorePersistenceBank (`00233550`) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (2 edges).** `00226280`, `00226BE0` are called by bodies filed to World: `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (26 edges).** `001831A0`, `00236760`, `002371B0`, `002EFA70` (+5 more) are called by bodies filed to WorldAreaField: BattleSystem_RunFieldFrameOrchestrator (`00234590`), WorldTransition_RequestFieldTransition (`00314440`), WorldTransition_RequeueCurrentFieldForRestore (`00314530`), WorldTransition_StageFieldTransition (`003145E0`) (+4 more); `002371B0`, InputGameplay_ArbitrateDigitalInputAndModalState (`00253C70`), `00280140`, WorldTransition_RequestFieldTransition (`00314440`) (+4 more) reach bodies filed to WorldAreaField: WorldPersistence_ExportGroupPersistentBank (`0025D8E0`), FieldData_GetVariable0 (`00265270`), WorldTransition_RequeueCurrentFieldForRestore (`00267C90`), WorldPersistence_ResetBanksAndMarkInitializationState (`00268320`) (+7 more) - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — SERVICE.** `002371B0` on this page calls `BattleStats_GetByMappedBattleSlot`, owned by that layer. What it reaches is a 49-byte accessor over the battle stats table: the mapped slot byte is rejected above `0x27`, and the rest index `[02EBF190] + 8` at a stride of `0x1C8` - the same **40 records of `0x1C8` bytes** the battle runtime reset walks; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — SERVICE.** `00233C10` on this page calls `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState`, owned by that layer. What it reaches is a 195-byte rebase over the **fifteen `0x58`-byte class descriptors** from `01EEBCC0` to `01EEC1E8`: each descriptor's three offset/pointer pairs are rebased onto the runtime base and given a running index accumulated from its `dword[+0x3C]`, after which `+0x57C8` is zeroed and the low three bits of the `0x80` bytes at `+0x59C8` are cleared; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — SERVICE.** `0032A8A0` on this page calls `PersistentFlag_QueryAuthoredThresholdSchedule`, owned by that layer. What it reaches is a 127-byte parity walk: the authored entry's list of **15-bit thresholds** is compared against the current authored variable, and the answer is the PARITY of how many it passes rather than a count; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE (FABLE, Claude Opus 5.5, 2026-09-25).** The hunt list's owner `0037F4D0` (request 19, UQ-162) opens a load batch through `00249580`, which claims the first free one of twelve `0x20`-byte slots at `02090790`. It then asks `00249210` for kind 7 id `0x128`, and for `0x13A` when its flag bit 4 is set, then hands the batch to `00249410` (body not read here; *it is read on [the handbook image bundles](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/himg-handbook-image-bundles.md) as the generic batch commit, which dispatches when the batch's two count words are equal; marked 2026-09-30, DD batch 13*). The fullscreen procedure's shared arm and `00279E20` call `0024A5A0`, a by-name lookup over sixty-four `0x48`-byte records at `0208F580`. The tick gate `0024AC10` tail-jumps into `0024AC30`. The UI asks and the resource layer loads and owns the buffers; the crossing is those calls, not a shared state.

**CombatAction — MECHANICAL (SWE2-CONTRACT 2026-09-15, 6 edges).** CombatAction bodies share the router's cited
generic accessors — fan-in, not an action relationship.


### UQ-163: the caller, and what the block belongs to (FABLE, 2026-09-16)

**THE CALLER EXISTS, AND THE BLOCK BELONGS TO THE TEXT DRAWER FAMILY - 2026-09-16 (FABLE).** *No caller was traced* was a gap in the tracing, not an absence: the call graph names one directly. **One caller, and it is the same object.** `002ABF70`'s entire reverse cone within eight hops is **one function**, `002A8C50` (3,363 B). At `002A9945` it does `mov rcx, rsi` / `call 002ABF70` - so the state block is `002A8C50`'s **own working object** - and a few instructions earlier it writes `[rsi + 0xC0]` and `byte [rsi + 0xB0]`, **the same `+0xB0` mode word this table documents.** Same object, confirmed by the field rather than assumed. **And `002A8C50` is a dispatch slot, which names the family.** It has no direct callers, and it appears **twice in `.rdata`**, at `009164C8` and `009164E0` - **24 bytes apart**. That is the **drawer table `009164C0`–`00916518`** which [numeric formatting and character mapping](../Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md) §7 decodes as groups of three slots, stride `0x18`. Reading the table: `009164C0` slot 0 is `002A9980`, `009164C8` **slot 1 is `002A8C50`**, `009164D0` slot 2 is `002A9F00` - **and that page already names `002A9F00` as slot 2 of kind 0.** So the first group is kind 0 and **`002A8C50` is slot 1 of kind 0**, and again slot 1 of the next group. **So what is being animated toward a 32,000 ceiling is a text/number drawer's own state** - the same family as `002A9F00`'s glyph-run character loop and `002AAE40`, which that page reaches only as slot 2 of kind 3. The block is a drawer's `this`. **The allocation half is still open, and I am not closing it.** *(Closed 2026-09-17 by FABLE: the block is embedded in its widget or on a helper's stack and never allocated on its own; UQ-163 is ANSWERED, see "What is not established" above. Marked 2026-09-30, SWE2-CONTRACT for OPUS, DD batch 13.)* A dispatch slot's `this` is allocated wherever drawers are made, and **I did not trace that**. What changes is that the row can now ask a specific question - *where are the drawer objects allocated* - instead of *what does this block belong to*. *One caution on the table.* No RTTI Complete Object Locator sits within 64 slots above either entry, so **this is a plain function table, not a C++ vtable** - the class-name route that works for the 346 zero-at-load objects does not apply here.

## The `00365980` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00365980` (5 B) — `jmp 003644B0` thunk.

| member | role | interior |
| --- | --- | --- |
| `003644B0` | `qword[022CBE00]` + `qword[r8+0x220]` double non-null gate (`003644B0`/`003644C3`) | [`003644B0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.
