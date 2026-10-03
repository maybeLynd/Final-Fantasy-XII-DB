---
system: Battle runtime mode ladder
category: 00-Engine-Core-Runtime
owner_layer: none — the mode function itself is unowned; its consumers span seven subsystems
status: AUDITED — the ladder and its six modes read (O-4 answered 2026-09-12: summon, chocobo, the field bit, the two event-party modes); the 0035BC50 and 00313DB0 sections' lists are all ticked; status line brought up to date 2026-09-18 (FABLE)
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# Battle runtime mode ladder

> One function reduces the whole battle runtime to a number from **0 to 5**, and the engine changes
> behaviour on the answer in seven places. It is really a **party-control authority ladder**: a
> running **cutscene script** outranks the **zone's authored data**, which outranks **combat**,
> which outranks the **interface**. The top two levels are named in the game's own script
> vocabulary — `seteventpartymode` and `seteventparty2mode`.

**PARTIAL.** *(answered: see the front matter, status AUDITED, brought up to date 2026-09-18 (FABLE); 2026-10-02, OPUS)* The ladder, its inputs and its persistence are read at tier 1. **Modes 1, 2, 4 and 5
are named** from the script verbs that set their bits — summon mode, chocobo mode, event party
mode, event party 2 mode (§2b, §2c, 2026-09-12); mode 3 is the area's field-record bit 15 and mode
0 the absence of all four. What keeps the page PARTIAL is the residue of the two consumers opened
below — the battle-menu selection builder `0035BC50` and the target cursor `00313DB0`, each with its
own "what is not established" — not the modes. *(Status paragraph corrected 2026-09-12,
OPUS-CONTRA-LADDER-STATUS: it had still said modes 0, 1 and 2 were unnamed after §2c named them.)*

## 1. What the player sees

Indirectly, quite a lot. This number decides whether your controls lock up when your leader falls,
how input arbitration behaves, what a unit definition applies, and what the presentation layer does
with a queued action.

The visible consequence worth naming is the **per-area override**. Some places in the game behave
differently from others for no reason the game explains — control suppression not biting, an input
path behaving as though nothing is happening. That is one authored bit per area, and the mechanism
is in §2: setting it **pre-empts** the mode that those behaviours test for.

## 2. Native mechanism

### The ladder

`BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) is a strict priority ladder over a
single flags word:

```c
uint BattleRuntime_GetMode0To5FromFlagsAndFieldBit15(void)
{
    flags = *(uint *)(DAT_02EBF190 + 0x5B04);      // 0030D9A4 load, 0030D9AB field

    if (flags & 8)                          return 5;   // test 0030D9B1
    if (flags & 4)                          return 4;   // test 0030D9C0
    if (FieldData_GetActiveFieldRecordBit15()) return 3; // call 0030D9CF (00377C20)
    if (flags & 2)                          return 2;   // test 0030D9EF — the
                                                          // flags word is reloaded
                                                          // at 0030D9E2
    return flags & 1;                       /* 1, else 0 — and+ret 0030DA01 */
}
```

| Mode | Condition | Set by | Named |
|---:|---|---|---|
| 5 | `flags & 8` | script verb **`seteventparty2mode`** | ✅ |
| 4 | `flags & 4` | script verb **`seteventpartymode`** | ✅ |
| **3** | **field-record bit 15 set** | **authored area data** | — |
| 2 | `flags & 2` | **`ridechocobo`** / **`getoffchocobo`** / **`setchocobomode`** — **chocobo mode** (§2c, 2026-09-12) | ✅ |
| 1 | `flags & 1` | **`summonread`** / **`summontopartyread`** / **`btlAtelSetSummonMode`** — **summon mode** (§2c, 2026-09-12) | ✅ |
| 0 | none of the above | — | |

**Only four bits of the word are consulted**, and the test order is fixed — the first match wins.

Each bit is driven by a **different authority**, and the priority order is the point — see §2b.

### Why the per-area bit is powerful

**Mode 3 is checked before mode 2.** So when an area's field-record bit 15 is set, the function
returns `3` and **every site testing `== 2` stops matching** — without those sites knowing anything
about areas. That is the entire mechanism behind
[`../../11-Party/party-roster-and-control-suppression.md`](../../11-Party/party-roster-and-control-suppression.md)
§6's note that control suppression is *"per-area waivable"*: it is not a parallel exemption check,
it is **priority pre-emption inside this ladder**.

The same authored bit is *also* read directly by the engine-wide functional predicate
`((layer0 | layer1) & 0x80000003) != 0 && FieldData_GetActiveFieldRecordBit15() == 0`. So one bit
reaches behaviour by two routes: **directly** as a term in that predicate, and **indirectly** by
outranking mode 2 here.

### 2b. Four authorities, one priority order

Each consulted bit has a matching getter/setter pair, and **each pair is driven by a different part
of the engine**:

| Bit | Mode | Getter | Setter | Driven by |
|---:|---:|---|---|---|
| 0 | 1 | `003135E0` (= `getsummonmodebit`) | `00313550` | **the summon** — `summonread` (1) / `summontopartyread` (0) / `btlAtelSetSummonMode`, and the summon presentation itself (`00306946` sets, `00306A7E` clears); `00313840` (reset) clears. *"UI" was the family's category label, not what drives the bit — corrected 2026-09-12, §2c* |
| 1 | **2** | `00303EE0` (= `getchocobomodebit`) | `00303D90` | **the chocobo** — `ridechocobo` (1) / `getoffchocobo` (0) / `setchocobomode`, the mount block of the presentation sequence (`00306A13`), the ride's end (`00304680`); *"Combat Action / Audio" was a category label — corrected 2026-09-12, §2c* |
| 2 | 4 | `003072E0` | `00307240` | **Script VM** |
| 3 | 5 | `003072A0` | `00307200` | **Script VM** |
| — | **3** | — | — | **authored field-record bit 15**, per area |

> **Corrected 2026-09-02.** This section previously claimed modes 4 and 5 were **dead code**, on the
> grounds that their accessors had zero callers. **That was wrong.** All four bit-2/bit-3 accessors
> are called — each through a **jump thunk**, which a direct-caller census cannot see:
>
> ```
> 00307200 (set bit 3 -> mode 5)  <- thunk 0037D110 <- 00351E50  [Script_VM_Native_Bridge]
> 00307240 (set bit 2 -> mode 4)  <- thunk 0037D120 <- 00351B40  [Script_VM_Native_Bridge]
> 003072A0 (get bit 3)            <- thunk 0037C890 <- 003573A0  [Script_VM_Native_Bridge]
> 003072E0 (get bit 2)            <- thunk 0037C8B0 <- 00356DF0  [Script_VM_Native_Bridge]
> ```
>
> **Every caller is the script VM bridge.** Modes 4 and 5 are not dead — they are **script-set
> modes**, reachable only from event and cutscene scripts, which is exactly why no ordinary gameplay
> code touches those bits.

### The script verbs name modes 4 and 5

`Tools/work/rtti/scriptvm_dispatch.tsv` maps each accessor to an authored script verb, and they sit
in one contiguous block:

| Call id | Verb | Args | Handler | Effect |
|---|---|---:|---|---|
| `0x050F` | **`seteventpartymode`** | 1 | `00351B40` | sets bit 2 → **mode 4** |
| `0x0510` | `geteventpartymode` | 0 | `00355FE0` | — |
| `0x0513` | `geteventpartymodebit` | 0 | `00356DF0` | reads bit 2 |
| `0x0514` | **`seteventparty2mode`** | 1 | `00351E50` | sets bit 3 → **mode 5** |
| `0x0515` | `geteventparty2mode` | 0 | `00356370` | — |
| `0x0516` | `geteventparty2modebit` | 0 | `003573A0` | reads bit 3 |

**These names are verified, not merely looked up.**
[`../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md`](../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md)
warns that its index mapping is wrong in at least one region and that a row is *"a lead, not fact"*
until the handler's **argument count** is checked against the catalog. That check passes on all
four: the `set…` verbs take **1 argument** and their handlers contain exactly one
`VMValueStack_PopInt32CoerceFloat32`; the `…bit` verbs take **0 arguments** and their handlers
contain exactly one `VMResult_WriteInt32`.

**Bits 0 and 1 have no script verbs at all** *(answered: see section 2c, ANSWERED 2026-09-12: both have verbs; 2026-10-02, OPUS)* — the complementary evidence that they are
engine-internal, driven by UI and combat, and unreachable from a script.

### So the modes are about who owns the party

Naming 4 and 5 settles what the ladder is *for*. `seteventpartymode` and `seteventparty2mode` put
the party into an **event configuration**, which is why the ladder's consumers are
`PartyControl_RecomputeSuppressionFromLeaderBattleState` and
`InputGameplay_ArbitrateDigitalInputAndModalState` rather than anything about damage or timing — and
why the bit-1 setter reaches into **party roster slot 3** when it clears.

**In play:** during a cutscene the script asserts an event party mode, and because that sits at the
top of the ladder it overrides the zone's authored bit, combat and the interface together. Normal
control and gambit behaviour stops during events **not because each system checks for "in a
cutscene", but because one number changed underneath all of them.**

### The hierarchy this produces

Reading the ladder as an authority order rather than a list of numbers:

```
   5   script VM — event party 2 mode  (bit 3, seteventparty2mode)   highest priority
   4   script VM — event party mode    (bit 2, seteventpartymode)
   3   authored area data              (field-record bit 15)
   2   chocobo mode                    (bit 1, ridechocobo / getoffchocobo / setchocobomode)
   1   summon mode                     (bit 0, summonread / summontopartyread / btlAtelSetSummonMode)
   0   nothing asserted                                                lowest
```

**A running script outranks the area's authored data, which outranks a chocobo ride, which
outranks a summon.** That ordering is a design statement: whatever a cutscene or event script
asserts about the runtime wins over what the zone's data says, and both win over the two mount-like
states the party can be in. *(Diagram and sentence corrected 2026-09-12, OPUS-CONTRA-LADDER-LABELS:
they still carried the category labels "combat / audio" and "UI" for bits 1 and 0 after §2b retracted
those as names of drivers; every bit is set by a script verb, and §2c names them.)*

It also explains the shape of §2's per-area override. Field bit 15 does not need to be the highest
priority to be effective — it only needs to sit **above mode 2**, and it does.

### Who asks

`00303EC0` is a four-line wrapper — `return BattleRuntime_GetMode0To5FromFlagsAndFieldBit15() == 2;`
— with **6 direct callers and 15 more through a thunk, 21 in total** (corrected 2026-09-02), plus a
further site that tests the same condition inline. The direct callers are:

| Site | Subsystem |
|---|---|
| `PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`) | Party |
| `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`) | Input |
| `BattleUnit_ApplyUnitDefinition` (`0023A570`) | Actor / Combat |
| `00235EA0`, `00320230`, `0035BC50` | unowned |
| `FUN_00313DB0` — tests `== 2` **inline**, without the wrapper | Combat Action (presentation ring) |

**The ladder's reach extends into Movement as well** (30 call edges): the mode query
`0030D9A0` is also asked by `00309AE0` and `00311F70`; `003135C0` is called by `00338490`; and
`00304180` calls `0026A0D0`, `0026B0C0`, `00392170` and `0026B620`, while `00311E20` and
`0033CA00` sit on both sides of the boundary — callers and callees of several ladder bodies.
That is expected rather than anomalous: entering or leaving a runtime mode moves or immobilises
actors, so locomotion code both feeds and consumes the mode word.

### The flags word and its state block

`DAT_02EBF190` is **registry slot `02EBF190`**, which
[`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
§8b established is a **runtime state block, not an authored table** — the single slot that broke
that document's original "every authored number" claim. This is that block in use, and the offset
`0x5B04` (23,300) is consistent with its recorded size of **≥ 23 KB**.

A byte-pattern scan for the displacement `0x00005B04` finds **36 sites across 18 functions**:

| Function | Sites | Owner |
|---|---:|---|
| `BattleAction_UpdateSpecialPresentationSequence` (`00306760`) | 6 | Combat Action |
| `SaveTransitionMetadata_RestoreFromRecord` (`002EF410`) | 3 | Save/Load |
| `00303D90`, `00307200`, `00307240` | 3 each | unowned |
| `00313550` | 3 | UI |
| `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` | 2 | — |
| `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584210`) | 2 | Save/Load |
| `00313840` | 2 | UI |
| `WorldTransitionSnapshot_RestorePersistencePairForActor` (`005843E0`) | 1 | World/Area/Field |
| eight more | 1 each | mixed |

### Bit 1 has a getter and a setter

```c
uint FUN_00303EE0(void)          { return *(uint *)(DAT_02EBF190 + 0x5B04) >> 1 & 1; }
```

`FUN_00303D90(uint on)` is its setter, and it does considerably more than flip a bit:

```c
if (((flags >> 1) & 1) != on) {
    if (on) {
        flags        |= 2;
        state[0x5AE0] |= 0xC;
        state[0x5AE4]  = 0x43340000;          /* 180.0f */
        return;
    }
    flags        &= ~2;
    actor3 = PartyRoster_GetActorBySlot(3);   /* the fourth party slot */
    FUN_002E73C0(PartyRoster_GetActorBySlot(3), 3);
    state[0x5AEC] = 0;
    if (state[0x5AE0] & 2) {
        if (actor3) thunk_FUN_002EB030(actor3, 0x2001);
        /* toggle bit 1 of state[0x5AE0] */
    }
}
```

Two things are worth pulling out. Enabling writes the float constant **`0x43340000` = 180.0f** to
`+0x5AE4`. And disabling reaches into **party roster slot 3** — the fourth slot, which
[`../../11-Party/party-roster-and-control-suppression.md`](../../11-Party/party-roster-and-control-suppression.md)
identifies as the one a guest occupies.

### It survives area transitions and saves

`SaveTransitionMetadata_CaptureToRecord` (`002EF3C0`) writes the block into a transition record:

```
rec+0x04  <- DAT_021B28E4       dword
rec+0x08  <- state+0x5AE0       qword
rec+0x10  <- state+0x5AE8       qword
rec+0x18  <- state+0x5AD0       qword
rec+0x20  <- state+0x5AD8       qword
rec+0x28  <- state+0x5B04       dword   <- the mode flags
```

So the persisted footprint is **`state+0x5AD0 .. +0x5AEF` (32 bytes) plus the mode word at
`+0x5B04`**, restored by `SaveTransitionMetadata_RestoreFromRecord` and normalised by
`SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`. `FUN_0030DA10` zeroes `+0x5B04` and `+0x5B08`
outright, which is the reset path.

**The mode is not transient.** It is captured, carried across an area transition, and restored.

### 2c. Modes 1 and 2 named — summon mode and chocobo mode (2026-09-12, FABLE-S03-MODE-NAMES)

**The two unnamed bits have script verbs after all; they were reached through thunks and a
different verb family.** From [the verb table](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv):

| verb | id | handler | what it does to `+0x5B04` |
|---|---:|---|---|
| `summonread` | `0203` | `0034E1F0` → `00313550(1)` | sets bit 0 |
| `summontopartyread` | `0207` | `0034FE80` → `00313550(0)` | clears bit 0 |
| `btlAtelSetSummonMode` | `3044` | `0050FFB0` → `003139C0(esper)` then `00313550(on)` | sets `+0x5AD4` to the Esper's row and bit 0 |
| `getsummonmodebit` / `getsummonmode` | `0512` / `0408` | thunks `0037C900` → `003135E0`, `0037C8F0` → `003135C0` | read bit 0 / the mode |
| `ridechocobo` | `037E` | begin `00347230` → thunk `0037CFF0` → `00303D90(1)` | sets bit 1 |
| `getoffchocobo` | `037F` | begin `00347820` → thunk `0037CFC0` → `00303D90(0)` | clears bit 1 |
| `setchocobomode` | `03EC` | `003514D0` → thunk `0037D100` → `00303D90(arg)` | either |
| `getchocobomodebit` / `getchocobomode` | `0511` / `0407` | thunks `0037C870` → `00303EE0`, `0037C860` → `00303EC0` | read bit 1 / **`mode == 2`** |
| `btlAtelSetChocoboTurboMode` | `302F` | `0050F8A0` → `00303F00(arg != 0)` | the turbo (below) |

So **`00303EC0`, the `mode == 2` predicate with 21 callers, is `getchocobomode`**: every site that
tests mode 2 — party-control suppression, the input arbiter, the unit-definition installer, the
battle-menu builder, the target cursor — is asking *"is the party riding a chocobo?"*, and mode 1 is
*"is an Esper out?"*. The ladder's order reads: a script's event party outranks the area's bit 15,
which outranks a chocobo ride, which outranks a summon.

**The chocobo's companion block** (`+0x5AE0`–`+0x5AEC`, [the battle-state block](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)), read from `00303D90`,
`00303F00`, `00304060`, `00304140`, `00304400`, `00304440` and `00304680`:

| field | meaning | evidence |
|---|---|---|
| `+0x5AE4` | **the ride time**: `180.0` on mount; the mount handler starts countdown channel 1 at `max(2.0, +0x5AE4)` toward 0 (`003040C6`–`003040E4`); the frame handler copies the channel back each frame (`00304474`–`00304485`) or holds `180.0` while console command **229 "Enable infinite chocobo time"** is on (`0017D380` → the console block's `+0xE1D`, `00304458`–`00304468`); when the channel arrives (`003EBB70(1)`) and the mode is still 2 with a slot-3 unit present, the ride's end path runs (`00311E20`, `0035CFA0(1)`, `003044A6`–`003044E7`) | `00304440`, [the console command names](../Developer-Tuning-Console/console-command-names.md) |
| `+0x5AE8` | **the turbo time**: `1.0 × 10.0` (`01DFE0B8`, `008F8180`) when `btlAtelSetChocoboTurboMode` turns the turbo on with a charge left and the mode is 2; countdown channel 2 (`00303F98`–`00303FC8`) | `00303F00` |
| `+0x5AE0` bit 0 | the ride's timers are armed (set at the end of the mount handler `00304131`; cleared by the leave handler `0030440B`) | |
| `+0x5AE0` bit 1 | **the turbo is on** — toggled with the actor event: `0x2010` to the mount when it starts, `0x2001` when it ends (`0030400A`–`0030403B`; the frame handler ends it when channel 2 arrives, `003044EC`–`00304584`) | |
| `+0x5AE0` bits 2–3 | **turbo charges left, three per ride** (`\|= 0xC` on mount, `00303DC6`); each turbo start spends one (`lea eax, [rbx*4 - 4]`, `00303FED`–`00303FFD`) unless console command **230 "Enable infinite chocobo turbo time"** holds them at three (`0017D3A0` → `+0xE1E`, `00303FCD`–`00303FDD`) | |
| `+0x5AEC` | the last turbo argument (`00303F59`); zeroed on dismount | |

**Roster slot 3 is the mount.** The dismount path (`00303D90(0)`, `00304680`, the turbo's end)
takes `PartyRoster_GetActorBySlot(3)`, forwards `(actor, 3)` to its render record through
`002E73C0` (a live-record check, then `003E6AA0` — a **presentation request** of sub-resource 3 on the mount's render object, read below), zeroes `+0x5AEC` and, when the turbo
was on, posts actor event `0x2001` to it — `002EB030` writes the id into the actor record's `+0xF0`
with `+0xEC = 0`, `+0xF5 = 0xFF` ([the actor storage record map](../../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md)) and, unless the record's `+0x18` is 1, hands it to
`002EB0D0(record, +0xC0, id, 1, -1.0)`. The mount handler `00304060` attaches the leader
(`00327200` finds `+0x5AA4` in the nine-entry selector at `+0x5A48`) to the slot-3 unit
(`002E28C0([mount + 0x10], rider)`, `002ECF10(rider, 1, 0)`) before arming the timers. The status
view's bit 11 marks that rider while bit 1 is on, and its bit 10 marks the summoner (`+0x5AD5`)
while bit 0 is on ([the battle-state block](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) §2.4).

**The summon is the special-presentation sequence's mode-1 block, and the chocobo its mode-2
block.** `BattleAction_UpdateSpecialPresentationSequence` (`00306760`) at `00306931`–`003069F3`:
sets bit 0, stores the caster's type byte at `+0x5AD5` and the action row's `+0x26` — the Esper's
party-table row — at `+0x5AD4`, stores party row `+0x32` of that Esper as both timers
`+0x5AD8` / `+0x5ADC` (`002FA0E0`; the shipped table carries **250** on all thirteen Esper rows and
0 elsewhere), and sets the Esper's level to the summoner's (`0030C470(esperStats, caster.+0x1C2, 0)`,
the level writer [the level-up page](../../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md) names, at `003069E1`–`003069EE`). At `003069F8`–`00306A31` it
sets bit 1 with the three charges and `180.0`; at `00306A6D`–`00306A87` it clears bit 0 when the
sequence ends. `+0x5AD4`'s reset value `0x1B` is Belias's row, the first of the thirteen
([the kind-byte page](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)). The `Dismiss` / `Dismount` commands [the handler table page](../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md) keeps issuable are the two
modes' exits.

**A transition dispatcher runs the modes' enter and leave handlers.** `0030D8B0(commit)` — called
by `00233AA0`, which [the field runtime pass](../../04-Actor-Entity/the-field-runtime-pass.md) §5 reaches when all four roster members are idle, and by
`00233CF0` — reads the ladder, compares it with the previous mode at `+0x5B08`, and indexes the
32-byte rows of `01EECFC0` (`0030D8CC`–`0030D97C`; only modes 0–4 are in the table):

| mode | same-mode (`commit = 0` / `≠ 0`) | leave (`commit = 0` / `≠ 0`) |
|---:|---|---|
| 1 summon | the empty stub `0016D6A0` / `00313600` — starts channel 2 from `+0x5AD8` and sets `+0x5AD0` bit 1 | `00313730` — ends the sequence, makes the summoner the preferred selector / `00313650` — resets through `00313840` ~~if bit 0 is still on~~ only when bit 0 is clear *(corrected 2026-10-02, OPUS: `00313650+0x7` `test byte [rax+0x5B04], 1`, `+0xE` `je 00313840`)* |
| 2 chocobo | `00304180` (Party, 639 B: collects the main members, types 0–6, into `022C1740`) / `00304060` — the mount | `00304400` — disarms and detaches the rider (`002E28D0`) / `00304140` — dismounts through `00304680` when bit 1 is already clear |
| 3 area bit 15 | the empty stub, all four | |
| 0, 4 | none | |

*(2026-09-14 — NOCALLER-INSTALLERS: the matrix's five no-caller members bound. The table is
rows ×4 cells of `01EECFC0`, 32-byte rows, reached only by `0030D8B0`'s two computed
`call [rbx + rdx*8]` sites (`0030D920`, `0030D952`); nothing else references any row. Per-member
interior cites:*

| row, col | address | role | interior |
|---|---|---|---|
| 1, 1 | `00313730` | clears `+0x5AD0` bit 1, then `00327850(byte[+0x5AD5])` | `00313737`/`0031373C` `mov ecx, 0xFFFD` + `and word [rax+0x5AD0], cx` |
| 1, 2 | `00313600` | `maxss(2.0, [+0x5AD8])`, `003EBC50(2)`/`003EBD00(2)`, sets `+0x5AD0` bit 1 | `00313616` `maxss xmm1, [rax+0x5AD8]` |
| 1, 3 | `00313650` | 21 B gate — `+0x5B04` bit 0 **clear** → tail `00313840`, set → `ret` (the doc table's "if bit 0 is still on" reads it the other way; `je` at `0031365E` jumps on clear) | `00313657` `test byte [rax+0x5B04], 1` |
| 2, 0 | `00304180` | `0031B8C0(3)` object, then `00327240` — the same-mode collect | `00304195` `mov ecx, 3` |
| 2, 1 | `00304400` | clears `+0x5AE0` bit 0, `00327200`→`0031ABF0`, clears `022C1F48` bits, tail `002E28D0` | `0030440B` `and dword [rax+0x5AE0], ~1` |
| 2, 2 | `00304060` | `0031B8C0(3)` object, `00327200`→`0031ABF0`, reads its `+0x10` | `00304066` `mov ecx, 3` |
| 2, 3 | `00304140` | `00327200`→`0031B950`→`0025A160`, gates on `+0x5B04` bit 1, `00304680` | `00304144` `call 00327200` |

*Row 3 is `0016D6A0` ×4 and rows 0 and 4 are all zero — a bound-not-entered mode (area bit 15)
and the table's own margins.)*

With `commit ≠ 0` the dispatcher also writes the new mode into `+0x5B08`. The persisted footprint
§"It survives area transitions" describes is therefore the chocobo's block plus ~~the two mode~~ the one mode
~~words~~ word `+0x5B04` *(corrected 2026-10-02, OPUS: the capture `002EF3C0` copies `+0x5AE0`, `+0x5AD0` and `+0x5B04` only, `002EF3C0+0x13`–`+0x3D`, and the restore `002EF410` writes back the same; `+0x5B08` is not captured)* — a ride survives a zone change and a save.

### 2d. The special-sequence state word `022C2160` — the machine behind summons, quickenings, Esper ultimates and the chocobo mount (2026-09-12, FABLE-SPECIAL-SEQUENCE-WORD)

The word this page's target-cursor section and [the world tick](../Battle-Frame/the-world-tick-and-the-field-frame.md) test for *"modes 5 and 6"* is not
the ladder's. It is the **global special-sequence state**, a second small machine with its own kind,
owner and flag words, read from every `.text` reference to `022C2160` (26 sites, `ripscan`):

| word | meaning |
|---|---|
| `022C2160` | the state, 0–7 (below) |
| `022C215C` | **the kind** — from the action id through a 128-byte table at `00306D08` over ids `0x94`–`0x113` (`00306C71`–`00306CDB`): **1** the thirteen summons (`0x106`–`0x112`, Belias … Zodiark), **2** Dismiss (`0x113`), **3** the 26 Esper ultimates (`0xB6`–`0xCF`, Painflare … Final Eclipse), **4** the eighteen quickenings (`0xD0`–`0xE1`, Red Spiral … Resplendence), **5** Mount (`0x94`), **6** Dismount (`0x95`), **7** every other id in the range (and any id above `0x113`) |
| `022C2168` | the owning unit (`00306C1B`; compared at `00306BFC`, `00306B16`) |
| `022C2158` | flags: bit 0 the one-shot has fired (set through the callback `00306560` that `0023B020` arms, cleared at `00306B4A`); bits 0–1 cleared at the end (`00306708`) |
| `022C1F50` | the accumulated-HP table: ~~32 entries of 16 bytes (`+8` the target unit, `+0x10` the HP delta), the source at `+0`,~~ the source qword at `+0`, then 32 entries of 16 bytes from `+8`, each the target unit at its `+0` and the HP delta at its `+8` *(corrected 2026-10-02, OPUS: `0030EB10+0x30`–`+0xB7` reads `[base + 8 + 16i]` and `[base + 0x10 + 16i]` for `i` below 32, and `+0xBF`–`+0xC8` clears `0x208` bytes)*, filled from the unit's `+0x780` list (`+0x77C` entries) by the presentation sequence (`003068F7`–`0030692A`) |

**The states**, from the four writers:

| state | set by | meaning |
|---:|---|---|
| 0 | the end (`003066F0`–`00306727`) | idle |
| 1 | `BattleAction_InitializeGlobalSpecialSequenceMode` (`00306BD0`, `00306C11`) when idle or re-entered by the same owner | requested — the owner is recorded |
| 2 | the same function, `00306C40`, after `0032F6E0(3)` allows it | accepted — `WorldSimulation_ProcessDeferredModeRequest(3, code)` is raised with `BattleSpecialSequence_DeriveActionPresentationCode`'s result, `0032ED70(3)` set, and the kind computed |
| 3 | `00306B10` (`00306B58`), from the owner's frame, when state 2 and `0032F6C0(3)` is clear | armed — flag bit 0 cleared and the one-shot at `0208E6A8` registered for the owner (`0023B020`; [the world tick](../Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5 bit 0) |
| 4 | `00306B10` (`00306B83`), when state 3 and flag bit 0 | ready — `00306B10` returns 1 only here |
| 5 | `BattleAction_UpdateSpecialPresentationSequence` (`00306ADF`), after its per-slot clears and `00332130(3)` | **the presentation is on screen** |
| 6 | `003065D0` (`0030662D`) on the field frame's step 11, when state 5 and `002671F0(3)` — manager slot 3's `+0x10` bit 0 — is clear | **the presentation is ending** |
| 7 | `003065D0` (`003066F5`) after the kind's finishing arm | done; then owner and flags are cleared, the one-shot nulled (`00238A60`), `00332190(3)` |

**The finishing arm depends on the kind** (`00306633`–`003066EB`, jump table `0030673C`): kinds 1,
2, 5 and 6 finish with nothing extra; **kind 3** (an Esper ultimate) applies the accumulated-HP
table — `BattleStats_ModifyHPAndProcessLethalState(target, delta, source, 0)` per entry
(`00306681`–`003066B0`) — after `0017F5B0(0)`, then clears it; **kind 4** (a quickening) runs
`0030D810`, `BattleSpecialSequence_CommitAccumulatedTargetHp(1)` — the same table, and with the
argument 1 every hit unit also has Sleep and Confuse removed (`0030EB68`–`0030EBB7`, the two
`ChangeStatus` mode-0 calls [the field-record page](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) §"4 = Sleep and 5 = Confuse" saw) — then
`BattleAction_ReleasePresentationSlot(unit +0x696)` and `0030D720`. That is the mechanism behind a
quickening chain's damage landing at the end of the chain.

**Entry**: `BattleAction_TryEnterGlobalSpecialSequence(unit, actionId)` (`0030CE10`) admits only an
action whose row `+0xC` has bit 30 (`0030CE93`), refuses a quickening or concurrence
(`0xD0`–`0xF1`) while the state is 5 or 6 (`0030CEC2`–`0030CEFE`), clears unit flag bit 29, calls
the initializer and sets bit 29 on success — **unit flag bit 29 = owns the special sequence**
([the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md)). Eleven readers test `state − 5 ≤ 1`: the tick skips its maintenance
(`00310E02`), the standard action state (`00304F6C`), target eligibility (`0030B81D`), the target
cursor (`00313EBC`, this page's cursor section), the presentation-slot acquisition (`0030D02B`),
the three presentation-event selectors and `00306BB0` — so "modes 5 and 6" everywhere mean *a
summon, quickening, ultimate or mount cinematic is playing*. `0032F6E0` / `0032F6C0` / `0032ED70`
/ `002671F0` are a resource-slot family indexed with 3, not read further here.

**One more consumer, read whole 2026-09-19 (FABLE): a distance threshold - `00309A90` (78 B).** It returns a float.
While the force-fight flag is set ([force-fight mode](../Force-Fight-Mode/force-fight-mode.md): its 12-byte predicate
answers false) the result is **24.0**. Otherwise it asks this page's mode function and returns **3.8 in mode 1**
(`3.6 + 0.2`) and **2.2 in every other mode** (`2.0 + 0.2`). It has four call sites - the AI order precondition check,
the locomotion order-goal decoder, and one further body twice - none read here, so *what the distance is compared
against is not stated*; the shape says an approach or reach distance that widens in mode 1 and is thrown wide open
under force-fight.

## 3. Key addresses

| Address | Role |
|---|---|
| `0030D9A0` | `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` — the ladder |
| `003135E0` | getter for flags bit 0 |
| `003072E0` / `00307240` | getter / setter for flags bit 2 — **no direct callers; both reached through jump thunks from the script VM** (section 2b) |
| `003072A0` / `00307200` | getter / setter for flags bit 3 — **no direct callers; both reached through jump thunks from the script VM** (section 2b) |
| `00303EC0` | `mode == 2` predicate — **21 callers** in total: 6 direct, plus 15 that reach it through a jump thunk (section 2b) |
| `00303EE0` | getter for flags bit 1 |
| `00303D90` | setter for flags bit 1, with side effects |
| `0030DA10` | zeroes `+0x5B04` and `+0x5B08` (reset) |
| `0030D8B0` / `01EECFC0` | the mode-transition dispatcher and its handler table (§2c) |
| `00303F00` / `00304440` | the chocobo turbo (`btlAtelSetChocoboTurboMode`) / the ride's per-frame timer handler (§2c) |
| `00304060` / `00304140` / `00304180` / `00304400` | the chocobo mode's mount, dismount, same-mode and leave handlers (§2c) |
| `00313600` / `00313730` / `00313650` | the summon mode's start and two leave handlers (§2c) |
| `00347230` / `00347820` / `0050FFB0` / `0050F8A0` | `ridechocobo`, `getoffchocobo`, `btlAtelSetSummonMode`, `btlAtelSetChocoboTurboMode` (§2c) |
| `002EF3C0` | `SaveTransitionMetadata_CaptureToRecord` |
| `002EF410` | `SaveTransitionMetadata_RestoreFromRecord` |
| `00584210` | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` |
| `00306760` | `BattleAction_UpdateSpecialPresentationSequence` — heaviest user, 6 sites |
| `02EBF190` | registry slot holding the runtime state block pointer |

## 4. Data structures and formulas

```
state = *(void **)0x02EBF190          runtime state block (>= 23 KB), NOT an authored table

state + 0x5AD0 .. 0x5AEF    32 B   persisted across transitions
state + 0x5AE0              u32    chocobo flags: bit 0 timers armed, bit 1 turbo on, bits 2-3 turbo charges (3 per ride)
state + 0x5AE4              f32    chocobo ride time, 180.0 on mount, counted down by channel 1
state + 0x5AE8              f32    chocobo turbo time, 10.0 per charge, counted down by channel 2
state + 0x5AEC              u32    the last turbo argument; cleared on dismount
state + 0x5B04              u32    THE MODE FLAGS; bits 0..3 consulted
state + 0x5B08              u32    the previous mode, kept by the transition dispatcher 0030D8B0; zeroed alongside 0x5B04

mode = (flags & 8) ? 5
     : (flags & 4) ? 4
     : FieldRecordBit15() ? 3
     : (flags & 2) ? 2
     : (flags & 1)
```

## 5. Call chain

```
authored field record --> FieldData_GetActiveFieldRecordBit15 --.
                                                                 |
state[0x5B04] bits 0..3 -----------------------------------------+--> 0030D9A0 mode 0..5
                                                                          |
                                          .-------------------------------+
                                          v                               v
                                   00303EC0 (== 2)                 inline == 2 tests
                                          |                        (FUN_00313DB0)
       .----------------------------------+----------------.
       v              v            v                        v
   Party         Input        Actor/Combat            three unowned
   suppression   arbitration  unit definition
```

## 6. Modding notes

- **Field-record bit 15 is the lever.** Setting it for an area forces the mode to **3**, which
  silently disables every behaviour gated on mode 2 — control suppression among them. No code needs
  patching.
- **The mode word is saved.** Editing `state+0x5B04` in memory is not enough to make a change
  survive an area transition; the transition record at `+0x28` carries it.
- **A zone script can seize party control.** `seteventpartymode` and `seteventparty2mode` are
  ordinary script verbs taking one argument, sitting at the **top** of the ladder — above the area's
  own authored bit. A script that sets one and never clears it leaves the party in an event
  configuration.
- **All four bits are live, but from different places.** Bit 0 is UI, bit 1 is combat/audio *(answered: see the ANSWERED 2026-09-12 notes, bit 0 the summon and bit 1 the chocobo; 2026-10-02, OPUS)*, and
  **bits 2 and 3 are set by event scripts**.
- **XIIOnline:** this mode is per-client runtime state that is *persisted*, so two clients can
  disagree about it across a transition. Anything gated on mode 2 — input arbitration included —
  will diverge unless the word is synchronised.

## 7. What is not known

- [x] ~~**What the six modes mean.** The ladder is exact; the semantics are not established. "Mode 2
      is in-battle" is the obvious reading and is **not** asserted.~~ **ANSWERED 2026-09-12 (FABLE):**
      0 nothing, 1 **an Esper is summoned**, 2 **the party is riding a chocobo**, 3 the area's bit 15,
      4 / 5 the event party modes (§2c). **O-4.**
- [x] ~~What flags bits 0 and 1 represent.~~ **ANSWERED 2026-09-12:** bit 0 the summon
      (`summonread` / `summontopartyread` / `btlAtelSetSummonMode`), bit 1 the chocobo
      (`ridechocobo` / `getoffchocobo` / `setchocobomode`); `getsummonmodebit` and
      `getchocobomodebit` read them (§2c).
- [x] ~~What bits 2 and 3 represent.~~ **ANSWERED**: script verbs `seteventpartymode` (bit 2 →
      mode 4) and `seteventparty2mode` (bit 3 → mode 5), arity-verified.
- [x] ~~What distinguishes **event party mode** from **event party 2 mode**, and what
      `geteventpartymode` / `geteventparty2mode` (`00355FE0` / `00356370`) return that the `…bit`
      variants do not.~~ **ANSWERED 2026-09-12 (FABLE).** *The verbs:* the setters only move one
      bit — `seteventpartymode(v)` (`00351B40` → `00307240`) sets or clears bit 2 of `+0x5B04` to
      `v`, `seteventparty2mode(v)` (`00351E50` → `00307200`) bit 3, each writing nothing when the
      bit already equals `v`. `geteventpartymodebit` / `geteventparty2modebit` (`00356DF0` →
      `003072E0`, `003573A0` → `003072A0`) return the raw bit; `geteventpartymode` /
      `geteventparty2mode` (`003072C0` / `00307280`) return **`ladder() == 4`** / **`ladder() == 5`** —
      so `geteventpartymode` is 0 while bit 3 is also set (5 outranks 4), which is the only value
      the bit variant does not give; `geteventparty2mode` and its bit variant can never differ.
      *The modes:* among the ladder's 21 callers only `BattleGroup_RefreshFourActorDefinitions`
      (`003266C0`, `00326756`–`0032677D`) has separate arms for 4 and 5. Both arms rewrite the
      **battle slot map** ([the battle-state-block field map](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) ~~`+0x5A58`, four 18-byte entries~~ the class tables at `+0x5A5A`, `+0x5A6C`, `+0x5A7E`, `+0x5A90`, 18 bytes each *(corrected 2026-10-02, OPUS: `00329CC0+0x123`–`+0x167` copies the 18-byte table at `+0x5A48` into the four; `+0x5A58` is the last word of `+0x5A48`'s table)*) to the **leader alone**:
      the leader `+0x5AA4`'s position among the nine selectors (or the focus slot `003272F0`
      when the field's bit 15 is on, its id then `00377C70()`) keeps its selector, the other
      three slots become `0xFFFF`. **Event party (mode 4, `0032683F`–`003268EE`) writes entries
      0, 1 and 3 that way; event party 2 (mode 5, `00326783`–`0032683A`) writes entries 0 and 1
      only and restores entry 3 to what it held before the refresh (`003267E8`–`003267F7`, from
      the copy taken at `003266F4`).** Entry 2 keeps all nine selectors in every mode. That is the
      whole native distinction; which of entry 3's readers (`0031B950`,
      `BattleSlotMap_ResolveMappedBattleSlot`, five more) an event script relies on is not read *(answered: see the mode contract, ANSWERED 2026-09-22 (SWE2-CONTRACT): the party read-in state machine `0037B4D0`; 2026-10-02, OPUS)*.
- [x] ~~What modes 0, 1 and 2 are in their own terms. Neither live bit has a script verb.~~
      **ANSWERED 2026-09-12:** both have verbs, reached through thunks (§2c).
- [x] ~~Why enabling the mode-2 bit writes **180.0f** to `+0x5AE4`, and what that field is.~~
      **ANSWERED 2026-09-12:** the chocobo ride time, counted down by channel 1 and held at 180 by
      console command 229 (§2c). The channel's unit is the countdown API's (`003EBC50`: `0.016675`
      or `0.02` per tick by `00290180()`), not converted here.
- [x] ~~Why disabling it acts on **party slot 3**~~ **narrowed 2026-09-12:** slot 3 is the mount, and
      `0x2001` / `0x2010` are actor events posted to it (§2c); ~~what `002E73C0`'s render-record call
      `003E6AA0(record, 3)` does is unread.~~ **Read 2026-09-12 (FABLE):** `002E73C0(actor, n)` finds
      the actor's render record (`+0xC0` → word index into the `0x740`-stride array at `[022C6F28]`,
      [the character render record array](../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md)) and, when its `+0x284` is non-zero, calls `003E6AA0(record, n)`, which stores
      `n` in the record's 5-bit field `+0x304` bits 27–31 and raises the dirty bit `+0x294` bit 27
      (`003E6AA0`–`003E6ABD`). `RenderRecords_ProcessDirtyState` (`00427DE0`) delivers it
      (`0042863B`–`00428660`): when the record's `+0x288` handle is not −1 it calls
      `003B3C00(handle, n)` and clears the bit. `003B3C00` resolves the handle through the 64-entry,
      `0x38`-stride table at `02EBD480` (entry `+0` must equal the handle, `+0x10` is the render
      object), returns 1 for `n = 0`, rejects `n ≥ 11`, and otherwise (`003B3480`, then
      `0024FE70(object, n)`) loads the object's resource `+0x130` if needed and takes the resource's
      ten-entry table — byte index `+0xA + n`, reference `+0x2C + 4 × index`, resolved by `0020E600`
      ([the authored-table row lookup contract](../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md)) — and `00333280` instantiates that reference as a `0x170`-byte instance in one
      of the object's sixteen slots (`0046EE30`, `0046EFD0`; the owner's `+0x92` counts). So the
      dismount posts **sub-resource 3 of the mount's render object**; the five other requesters of
      `0024FE70` (`00270150`, `002FD0C0`, `003B1260`, `003B1BA0`, `003B2830`) pass a register, the
      `003B4B60`–`003B5520` family writes 2 and `n + 2`, `003B8260` (interior read 2026-09-17, SWE2-FRONTIER: 1,028 B — `0031E880` first at [`003B82D7`](../../_index/ADDRESS-INDEX.md), `0020E600` ×7 + `003E6AA0`/`003B3CA0` ×2) up to `0xB`, and `00520720` a
      table word. Which authored asset row 3 names is that resource's matter, not this page's.
- [x] ~~What `+0x5AE0`'s bits mean, and what `+0x5B08` is.~~ **ANSWERED 2026-09-12:** timers armed /
      turbo on / turbo charges, and the previous mode (§2c, §4).
- [x] ~~What the other 16 functions touching `+0x5B04` do with it.~~ **Narrowed 2026-09-12:** the
      transition dispatcher `0030D8B0` (reads, keeps `+0x5B08`), the special-presentation sequence
      (sets and clears both bits, §2c), the two bit-0 writers `00313550` / `00313840`, the status
      view's bits 10 / 11 and the save capture / restore / normalise trio are accounted for.
      **Completed 2026-09-12 (FABLE) — all 36 sites in 18 functions, by bit:** the ladder
      `0030D9A0` reads bits 0–3; the getters `003135E0` (bit 0), `00303EE0` (bit 1), `003072E0`
      (bit 2), `003072A0` (bit 3) read one bit each; the setters `00313550` and `00313840` (bit 0),
      `00303D90` (bit 1), `00307240` (bit 2), `00307200` (bit 3) each rewrite the word;
      `00313650` ~~sets bit 0 through `00313840` when it is clear~~ tail-jumps to `00313840` when bit 0 is clear, and `00313840` clears bit 0 only when it is set *(corrected 2026-10-02, OPUS: `00313840+0x13`–`+0x18`)* (the summon reset, §2c);
      `00304140` tests bit 1 and dismounts through `00304680` when it is clear (§2c);
      `BattleAction_UpdateSpecialPresentationSequence` sets and clears bits 0 / 1 around the
      summon and mount blocks; `FUN_0030DA10` zeroes the word and `+0x5B08` for
      `BattleSystem_ResetRuntimeState`; `SaveTransitionMetadata_CaptureToRecord` reads the word
      into the save record and `…RestoreFromRecord` writes it back, then clears bit 0 and sets
      bit 1 as the record says; `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` clears bit 0
      (a load never resumes summon mode) and
      `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` clears bit 1 (`0058446A` — a
      transition-snapshot restore always dismounts). Nothing else in `.text` addresses the word.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The full 0..5 ladder and its order | complete body of `0030D9A0` | 1 |
| Mode 3 pre-empts mode 2 | the ladder's fixed test order, read directly | 1 |
| `00303EC0` is `mode == 2` with 6 direct callers, 21 including the thunk | complete body + caller census over `edges.tsv`, plus a JMP/CALL byte scan for the thunk | 1 |
| A seventh site tests `== 2` inline | body of `FUN_00313DB0`, read 2026-09-02 for the AH-6 pass | 1 |
| 36 sites across 18 functions touch `+0x5B04` | byte-pattern scan for disp32 `0x00005B04` in `.text`, attributed to containing functions | 1 |
| Bit 1 getter and setter, and the setter's side effects | complete bodies of `00303EE0` and `00303D90` | 1 |
| `0x43340000` is 180.0f | IEEE-754 decode of the literal | 1 |
| The special-sequence machine: eight states, seven kinds, the accumulated-HP table | `00306BD0`, `00306B10`, `003065D0`, `0030CE10`, `00306BA0`, `00306BB0`, `0030EB10` read whole; the kind table at `00306D08` (128 bytes) and its seven-entry jump table at `00306CEC` decoded against bank 0 names; the finishing jump table at `0030673C`; all 26 references to `022C2160` listed (2026-09-12) | 1 |
| Bit 1 is the chocobo, bit 0 the summon | verb-table rows `037E` / `037F` / `03EC` / `0407` / `0511` and `0203` / `0207` / `3044` / `0408` / `0512`, each handler and thunk followed to `00303D90` / `00303EE0` / `00303EC0` / `00313550` / `003135E0` (2026-09-12) | 1 |
| `+0x5AE4` / `+0x5AE8` are the ride and turbo times, `+0x5AE0` the armed / turbo / charges bits | `00303D90`, `00303F00`, `00304060`, `00304440`, `00304680` read whole; console commands 229 / 230 through `0017D380` / `0017D3A0` (`+0xE1D` / `+0xE1E`) | 1 |
| The summon block stores the Esper's row, the summoner's selector, party row `+0x32` (250) and the summoner's level | `00306931`–`003069F3`; `002FA0E0` reads `02EBF130` row `+0x32`; the party table decoded from `battle_pack.bin` directory entry `+0x44` (rows 27–39 = 250, others 0) | 1 |
| The transition dispatcher and its five populated rows | `0030D8B0` read whole; `01EECFC0` dumped as six 32-byte rows; callers `00233AA0` / `00233CF0` from `edges.tsv` | 1 |
| The block is captured and restored across transitions | complete body of `SaveTransitionMetadata_CaptureToRecord` | 1 |
| Bits 2 and 3 are set only by the script VM | each accessor reached through a jump thunk whose sole caller is `Script_VM_Native_Bridge`-domained (`0037D110`->`00351E50`, `0037D120`->`00351B40`, `0037C890`->`003573A0`, `0037C8B0`->`00356DF0`) | 1 |
| Modes 4 and 5 are `seteventpartymode` / `seteventparty2mode` | `scriptvm_dispatch.tsv` rows `0x050F` and `0x0514`, each confirmed by the **argument-count check** that document requires | 2 |
| `02EBF190` is runtime state, not an authored table | `authored-data-table-registry.md` §8b, corroborated independently here and by `BattleStorage_InitializeWorkArrays` | 1 |

## 9. Related

- [`../../11-Party/party-roster-and-control-suppression.md`](../../11-Party/party-roster-and-control-suppression.md) — where the mode-2 gate was found
- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) — the state block's registry slot
- [`../Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — the field-bit-15 accessor's reach
- [`../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`](../../03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md)

## 10. Falsification pass 2026-09-02

**Attack chosen.** This document was written during the same session that is now auditing it, so the
attack targeted what a fresh author is worst at: **claims retracted in one section and left standing
in another**, and counts summarised in prose but tabulated separately. Every mechanical figure was
also re-derived from the binary.

### SURVIVED: every measurement, exactly

| Claim | Re-derived | Result |
|---|---|---|
| the 0–5 ladder body | bytes at `0030D9A0` | `8B 88 04 5B 00 00` (`mov ecx,[rax+0x5B04]`), `F6 C1 08`→`mov eax,5`, `F6 C1 04`→`mov eax,4` — **exact** |
| 36 sites across 18 functions touch `+0x5B04` | disp32 scan of `.text` | **36 / 18, 0 unattributed** |
| `00303EC0` direct-caller count | `edges.tsv` | **6**, the same six named |
| …and 15 more through a thunk, 21 total | JMP/CALL scan | one thunk, `0037C860`, with **15 callers** → **21** |
| the four script-VM thunk chains | `E9` rel32 decode | **all four MATCH** |
| `0x43340000` is 180.0f | IEEE-754 | **180.0** |

The four thunk targets were read from the bytes rather than the graph, because **`edges.tsv` does
not contain these edges at all** — a `JMP` thunk is not a call, so a caller census over the edge list
reports zero for all four accessors. That is precisely the blind spot that produced the original
"dead code" error, and it is worth stating as a property of the instrument: *the edge list sees
`E8`, not `E9`.*

### CORRECTED: the retracted claim was still standing in section 3

Section 2b retracts "modes 4 and 5 are dead code" in full, with the thunk chains. **Section 3's
address table still read "both uncalled"** for all four accessors — the retracted claim, in the table
a reader is most likely to consult. Both rows corrected.

This is the failure mode the database has hit before: a correction applied where the argument lives,
not everywhere the claim appears. Notably `check_consistency.py` cannot catch it, because "uncalled"
is prose, not a caller *count* — the checker only compares numbers. A retraction has to be chased by
hand.

Section 3's `00303EC0` row gave only the direct figure while section 2b gives the total. Both are
true of different things; the row now says which.

### CORRECTED: the site table was one row short of its own headline

The headline "36 sites across 18 functions" is right. The table beneath it accounted for
**34 sites across 17 functions** — `00313840` (2 sites, UI) was missing. Added. The rest of the
table reconciles exactly, including the nine functions with a single site.

### Not changed

The interpretive core — the ladder as a **party-control authority ladder**, mode 3 pre-empting
mode 2, and the reading that a script outranks authored area data which outranks combat which
outranks UI — rests on the ladder's fixed test order, which was re-read byte for byte and holds.
**O-4 stays open** *(answered: see O-4, ANSWERED 2026-09-12 (FABLE); 2026-10-02, OPUS)*: what the six modes *mean* is still not established, and this pass did not
attempt it.

## `0035BC50` opened — the battle-menu selection state builder (2026-09-03, `repos-78`)

Handed over rather than published by the session that took it from the ranked cut, because **the
decompiled listing distorts every local in this function**. Read here from the image.

### First: the frame is fixed, and the diagnosis of *why* the listing distorts was wrong

The listing renders the prologue as a call whose result is negated and added to every stack reference,
which reads as a **dynamically sized frame**. It is not one:

```asm
0035BC54  mov  eax, 0x1128        ; a compile-time constant
0035BC59  call 0x808f10           ; _alloca_probe
0035BC5E  sub  rsp, rax
...
0035C03B  add  rsp, 0x1128        ; the epilogue, a LITERAL
```

**`_alloca_probe` is called with a constant size.** This is MSVC's standard large-frame stack probe —
required for any frame over one page — not `alloca`. **The literal `add rsp, 0x1128` in the epilogue
is the proof that the frame is fixed**, and the stack cookie sits at the fixed offset `+0x1100`.

**Censused image-wide:** **34 functions use the constant-size probe and 0 use a non-constant size.**
So **this executable contains no dynamically sized stack frame at all**, and the distortion is a
rendering artefact over a known, enumerable set of 34 functions.

> **The consequence runs the other way from the warning.** The locals are *not* unreadable — they are
> at fixed offsets, and the listing simply cannot prove it. **A reader who trusts the listing loses
> nothing except confidence; a reader who distrusts the frame size loses the function.**

### Four gates before anything runs

| gate | address | passes when |
|---|---|---|
| a predicate call | `003C5FF0` | returns non-zero |
| a flag byte | `022C83EC` | bit 0 clear |
| a mode word | `02092730` | **not** `0x0B` and **not** `0x18` |
| a flag word | `022C83E8` | bit `0x100` clear |

### The command list, then four member slots

`BattleMenu_BuildCommandEntryList` fills a stack buffer, whose count and payload are published to
`022C83F0` / `022C83F4`, and then **compacted from 8-byte stride to 4-byte stride** into `022C83F8`.

The walk itself is **four iterations** (`cmp ebp, 4`) over slots **`0xC0` bytes apart**:

```asm
0035BDB0  lea  rsi, [rdi - 0x60]     ; rsi = slot base, rdi = slot base + 0x60
0035BE53  add  rdi, 0xc0             ; the stride
0035BE69  cmp  ebp, 4
```

> **The stride is `0xC0`, not `0x60`.** `rsi` and `rdi` are two cursors into the *same* slot, sixty
> bytes apart — a listing that shows both invites reading their difference as the stride. **The slots
> are at `022C8080`, `022C8140`, `022C8200` and `022C82C0`**, and a parallel array of four resolved
> registry pointers runs at `022C8388` with stride 8.

Per slot the function reads a **flags byte at `+0x00`**, a **packed actor handle at `+0x04`**, and a
**word at `+0x60`**.

**The slots are compacted** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 279)*. The output cursor `rdi` advances
by `0xC0` only on the accept path (`0035BE53`); a rejected member takes `0035BE5C` and leaves it in place. So slot *k* holds
the *k*-th **accepted** member, not member *k*.

### The selection state block, decoded

| address | width | what the walk puts there |
|---|---|---|
| `022C8060` | dword | **bit 0 set when some slot's handle equals the current party focus** |
| `022C8064` | word | ~~the running slot index~~ **the count of accepted slots**: it is incremented and stored only on the accept path (`0035BE49`–`0035BE4C`), so it is also the index of the next compacted slot *(corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 279)* |
| `022C8066` | word | **counts accepted slots whose flags byte lacks bit `0x02`** (`0035BE34` `test byte [rsi], 2` / `je` → `0035BE42` `inc word [022C8066]`); the sibling of `022C8076` *(added 2026-09-25, same source)* |
| `022C8068` | dword | **counts slots whose flags byte lacks bit `0x40`** |
| `022C806C` | dword | the current focus handle, read once before the walk |
| `022C8070` | dword | the preferred definition selector, read once before the walk |
| `022C8074` | word | **the index of the slot that matched the focus** (initialised to `-1`) |
| `022C8076` | word | the definition selector of the last slot whose flags carry bit `2` (init `-1`) |
| `022C8078` | qword | **a pointer to the slot that matched the focus** |

So the three questions the handover could not answer:

- **Which slot is selected** — the one whose **packed actor handle at `+0x04` equals the current party
  focus handle**. Its pointer lands in `022C8078` and its index in `022C8074`.
- **What the counters count** — `022C8068` counts slots **without** flags bit `0x40`; a second,
  register-only counter counts slots without bit `0x40` **and** without bits `1`–`2`.
- **Which flag suppresses the pass** — none of the four gates is a single "suppress" bit; the pass is
  refused by **any** of them, and two are per-mode rather than per-flag.

### What is not established

- [x] ~~What the flags byte's bits `0x40`, `0x02` and `0x04` mean. Their *effect* here is read; their
      names are not.~~ **Named 2026-09-12 (FABLE) by cross-reference.** Each slot is filled by
      `00320040(2, i, slot)` (`0035BDB0`–`0035BDBE`), which resolves member `i`'s mapped battle slot
      (`BattleSlotMap_ResolveMappedBattleSlot`) to its stats record and tail-jumps
      `00329220(stats, i, slot, 1)` — so **the four selection slots are unit display records**, and
      the flags byte is that record's `+0x00` ([the unit display record page](../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md) §2.3): **`0x40` = bit 6 = unit flag
      bit 1** — the unit is torn down ([the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md): set only by `BattleUnit_TeardownAndDespawn`),
      **`0x02` = bit 1 = a guest-typed member** (party type `7..0x19`), **`0x04` = bit 2 = an
      Esper-typed member** (type `0x1B..0x27`). So `022C8068` counts members whose unit is alive
      in the pool, and the walk's `0x40` test at `0035BDE2` is "has no live unit".
- [x] ~~What the second, register-only counter is used for after the loop.~~ **Read 2026-09-12
      (FABLE):** `r15` counts the slots that are neither torn down nor guest- nor Esper-typed — the
      playable members present — and the tail tests it (`0035BED4`) as one precondition of the
      automatic party-leader-selection post (the tail item below): no playable member, no picker.
- [x] ~~What mode values `0x0B` and `0x18` at `02092730` are.~~ Narrowed 2026-09-11: the word is the last UI request id any route posted (`00252B40`), so they are request ids 11 and 24 ([the router](../../16-UI/Request-Router/ui-request-router.md) §2); **EX-2 answered 2026-09-12 (FABLE):** 11 is the game-over request and 24 the party-incapacitated request (the router page's table) — so the selection builder refuses to run while either is the last request posted.
- [x] ~~What the tail after the walk does with `022C8074` — it compares against a saved copy and clears
      bit 0 of `022C8060` on one path, which was not followed.~~ **Read 2026-09-12 (FABLE),
      `0035BE72`–`0035BF46`, three steps.** (1) If no slot matched the focus (`022C8074 == −1`) the
      index saved before the walk (`0035BD4E`) is kept — clamped to 0 when it exceeds the running
      slot count `022C8064` — written back to `022C8074`, and `022C8060` bit 0 is cleared
      (`0035BE75`–`0035BE90`): the cursor stays where it was. (2) If `022C83E8` bit 3 is set and the
      ladder reads chocobo mode (`00303EC0`), it arms [the capability policy](../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) row 8 through `002547D0(1)` and
      leaves (`0035BE98`–`0035BEBC`). (3) Otherwise, when the published count is non-zero, some
      slot lacks flags `0x40` (`022C8068`), the two walk flags `r12` / `r15` are set and `022C8060`
      bit 2 is clear, it scans the four slots for one with flags bit 0, a non-zero handle and a
      non-negative word `+0x60` (`0035BEF0`–`0035BF0B`); finding one while **no UI request is posted**
      (`02092730 == 0`) it sets bit 2, runs `0028F970`, sets `022C83E8` bit 6 and posts **request 3 —
      the field party-leader selection** ([the router](../../16-UI/Request-Router/ui-request-router.md)) — through `00254B40(3)`; a refused post
      clears both bits again (`0035BF17`–`0035BF3F`). So the builder itself raises the leader
      picker once, latched by `022C8060` bit 2, whenever a selectable member exists and nothing
      else is on screen.

## `00313DB0` opened — the target-selection cursor, and a 64-entry candidate ring

Cited by three documents by name only; the last-but-one entry on the *leaned on and never opened* cut.

**Extent checked**: 91 instructions, and **the last instruction is `jmp 0x313a00`, a genuine tail call**
into a 289-byte function. Third real instance of that hazard tonight.

### With nothing selected: pop candidates until one is viable

**A circular queue**: head byte at `022BEDA0`, tail byte at `022BEDA1`, entries at `022BEDA4` with
**stride 8**, and the head advances with `inc cl ; and cl, 0x3f` — **64 slots.**

```asm
00313DE0  movzx ecx, byte ptr [022BEDA0]      ; head
00313DE7  cmp   cl, byte ptr [022BEDA1]       ; tail — equal means empty
00313DF6  inc   cl
00313DF8  and   cl, 0x3f                      ; wrap at 64
00313DFB  mov   eax, dword ptr [rsi + rax*8]  ; the handle
00313E06  call  BattleUnit_ResolveByFocusHandle
```

Per candidate:

```asm
00313E17  and   qword ptr [rax], 0xffffffffffffefff   ; clear bit 0x1000
00313E1E  or    qword ptr [rax], 0x2000               ; set   bit 0x2000
```

> **Every candidate popped is marked whether or not it is chosen** — bit `0x1000` cleared and `0x2000`
> set. **The mark records "considered", not "selected"**, and a unit rejected on the next test keeps it.

The rejection is the familiar predicate: `((status0 | status1) & 0x80000003)` with the
`FieldRecordBit15` waiver — **and here a failure `continue`s the loop rather than aborting**, so the
cursor skips incapacitated units and keeps popping. **The queue draining is what ends it**, since an
empty queue yields handle `0`, which resolves to null.

On success the unit is stored to **`02089350`** — the global the capability-policy document already
tracks as *"CombatAction current-selected-BattleUnit state"* — and a notification chain runs.

### With something already selected: the same predicate, used to deselect

```asm
00313EBC  mov  eax, dword ptr [022C2160]
00313EC2  add  eax, -5
00313EC5  cmp  eax, 1
00313EC8  jbe  return                    ; modes 5 and 6 do nothing
...
00313EEC  bt   rax, 0xd                  ; flags bit 13 -> keep the selection
00313EFA  mov  qword ptr [02089350], 0   ; otherwise clear it
```

**So one function both advances and cancels the cursor**, chosen by whether `02089350` is already set,
and **the same `0x80000003` test decides "skip this candidate" on one path and "drop the selection" on
the other.** Two more sightings, and the first where it is used to *revoke* something already granted.

### What is not established

- [x] ~~Who fills the 64-entry ring, and what a stride-8 entry holds beyond the handle in its first dword.~~
      **Read 2026-09-12 (FABLE).** The ring is the 64 × 8 block at `022BEDA4` behind the head / tail
      bytes `022BEDA0` / `022BEDA1`. Its one filler is `BattleUnit_AdvanceStandardActionState`
      (`00304E4B`–`00304E74`): after the phase's presentation event is dispatched (`0030A370`,
      `003299B0`) and `BattleAction_CheckPresentationSlotReady(+0x694, unit, &slot)` has changed the
      slot word from its "none" value, it stores **the unit's own handle `+0x08`** into the entry at
      the tail, advances the tail modulo 64 and sets the unit's flag bit 12. Nothing writes an
      entry's second dword — not the filler, and not `BattleAction_ResetPendingQueueBanks`
      (`0030FE60`), whose loops zero only the first dword of each entry of both banks before
      zeroing the head / tail word (`0030FEB0`–`0030FEBB`). So an entry is one handle and four
      bytes of padding, and the ring is **the queue of units whose action presentation has just
      acquired a slot**, which this cursor drains to pick the shown unit.
- [x] ~~What flags bit `0x1000` means, given `0x2000` replaces it on every candidate.~~ **Read
      2026-09-12 (FABLE):** bit 12 is **queued in this ring** — set at the push (`00304E74`) and
      cleared only here, when the cursor pops the entry (`00313E17`); a whole-`.text` scan of every
      `or` / `and` on a memory qword with `0x1000` / `0x2000` finds no other writer of these two
      unit bits ([the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md), rows 12 and 13).
- [x] ~~What modes `5` and `6` at `022C2160` are.~~ **ANSWERED 2026-09-12:** the special-sequence
      state — 5 the cinematic is on screen, 6 it is ending (§2d).
- [x] ~~What flags bit 13 on a selected unit means.~~ **Read 2026-09-12 (FABLE):** bit 13 is
      **popped — its presentation is the one being shown**: set by the pop (`00313E1E`), kept as
      the reason to hold the selection (`00313EEC`), and cleared by the same action-state advance
      when `0030BC40(unit)` reports the presentation finished (`00304FDD`–`00304FE9`), which is what
      lets the cursor move on.

*(Pass 22 adjacency, 2026-09-14: the ladder's bodies reach the layers a mode change touches —
`0030C470` calls **items/equipment** `00324100` and `00329220` calls `00324020`, while `00377C20`
is called by the items-side `00309FB0`/`0030FD10` (4 edges), and `00584210` calls
**achievements** `00316810` (1). Entering or leaving a battle mode walks equipment state and can
report to the achievement layer; these are the ladder's consumers, not its owners.)*

## The `00253C70` exclusive subtree — what the Input-side mode consumer actually is (SWE2-FRONTIER, followup queue)

`InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`, 1,599 B) is the ladder's Input
consumer (§"Who asks"), and the exclusive-callee census assigns it **22 frontier functions** —
the per-frame input arbitration family. Every member body was disassembled from the shipping
image (2026-09-15); roles below are what the instructions do, and names already claimed on
[r2-force-fight-toggle.md](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md) are kept.
Eleven members are called by the root directly (`0017DE10`, `00228380`, `002287D0`, `002500F0`,
`002501A0`, `00252B60`, `002B6220`, `003C9570`, `003CA200`, `003CB3E0`, `00862CF0`); the other
eleven are reached through member-to-member edges and are helpers, not independent entry points.

| cluster | members | role |
|---|---|---|
| device probes | `0017DE10` (67 B — `00796E20` singleton, `+0xDF8` device slot, `00197710` query then `0079E6A0` probe → bool), `0017E4C0` (25 B — `00796E20` → `0079E640` → one byte of manager state), `00862CF0` (68 B — lazy `00862C70` init if `02EAF8F0` unset, then an indirect `call qword ptr [02EBA3F0]` with args `(0, &02EBA3E0)` — a device-state poll through a stored entry point into a fixed record; returns 1 iff the returned word `02EBA3E4` carries `0x400`) | the raw input-side facts the arbitration reads — manager state and a direct device-state poll through a stored entry point |
| `01FD4948` gate | `00228380` (204 B — `002E0FA0` button word; if `0017E4C0` reports 0 and `01FD4948` is null, `00228490` builds it; refuses on `003603C0`/`0017D930`/`01FD4950`; a bit-`0x15` held-vs-edge test through `002E1020(1)` can veto; while `01FD4940` is null it ticks the `01FD46FC` countdown, and at zero with the dialog object present it tail-calls `002282F0`), `00228490` (91 B — `cmp [01FD4948],0 → jne done → 00244F50(0xD0, proc 002284F0, zeroed params) → store`) | the first arbitration gate plus the lazy create of one `01FD4948` dialog object — same ensure-singleton shape as the boot layer's stubs |
| modal state machine (`0209AC30`, fields `+0xC8`/`+0xD0`/`+0xDED`) | `002287D0` (346 B — early-out 0 on `003603B0`/`003603C0`; returns 1 early when the mode query `00229EA0` is 5 or 6 or `+0xC8` is already set; when `+0xC8` is clear, `00280120` holds and `+0xDED` is still positive it decrements that byte and returns 1 — a per-call countdown gate; the main path folds `003641F0` and button bits `0x10`/`0x11` into the `00227D70` countdown, compares pad word `02F9736A` against the constant mask at `00915538`, weighs `00265680` plus bits `0xC`/`0xD`/`0x13` and the `003606B0` channel scan, then calls `00228700(esi, edi)` and zeroes `01FD46F8` when it fires), `00228700` (149 B — if `+0xC8` set, returns 0; else seeds `01FD46F4` from `0208F570`, calls `002289D0`, and `00244F50(0xD8, proc 00228130)` installs the object at `+0xC8`; returns 1 on create), `002289D0` (148 B — lazy-creates `+0xD0` via `00244F50(0xF8, proc 00228C70)` carrying both caller args, then `00251D90(obj, 2+([+0xE2]!=0), 6)` sets its state), `00227D70` (90 B — `0035F150(0,0,0)` reloads `01E027F8` to 6 and returns 0/2; on failure the counter decrements each call and returns 1 at zero — a six-frame arming countdown), `003606B0` (39 B — linear scan of the three dwords `022CB9C4`–`022CB9CC`, returns 1 on the first nonzero) | the modal-dialog open/tick/dismiss machine: two lazily built objects on the `0209AC30` manager, a countdown that must expire, and a three-channel "anything active" scan |
| permission predicates | `002500F0` (56 B — if `ecx` bit `0xB` is set and `00236760` is clear, asks `002E25B0(ebx, 0x21)` and returns its answer), `002501A0` (59 B — `InputGameplay_TestAggregatedMask62Bit1WithTemporalGate`; when `00229DF0` and `00229E00` both hold, the frame accumulator `020927DC` modulo `cvttss2si(xmm0)` must be zero or the answer is 0 — a temporal decimator — then returns bit 1 of `02F97362`), `002E25B0` (44 B — suppressed outright when `0215F1A1` is set; selector `ecx == 2` additionally requires `002E0FA0` bit 0 clear; otherwise permitted) | the "is this action allowed right now" tests the root asks before letting a press through |
| force-fight toggle | `00252B60`, `00252C80`, `00366870`, `003669F0` | the R2 force-fight apply path — documented in full on [r2-force-fight-toggle.md](../../15-Input/Modal-Toggles/r2-force-fight-toggle.md) §2d–2g; `00252B60` re-decides against the policy mask and hands `003669F0`'s engaged bit to `00252C80`, the second writer of `01E0C2B8` |
| presentation objects (`0209E5C0`, `02B47730`/`58`/`60`) | `002B6220` (62 B — lazy-creates `0209E5C0` through `002B6350(5)`, ORs `0x500` into its `+0x179D2` flags word, tail-jumps `002B6570`), `002B6570` (220 B — copies `0x20` bytes of state from `02B47760+0x190` into the `0209E5C0` object at `+0x190`, sets `+0x179D2` bits `0–1`, invokes `vtable[0]` twice with arg blocks `0x10` then `0x20`, and returns a base pointer selected by bit 2 of that flags word — `obj + 0x1B0 + (bit2 ? 0xBC10 : 0)`), `003C9570` (31 B — `02B47730` object: when `+0xC0` bit 3 is set returns dword `+0xCC`, else 0 — a gated getter), `003CA200` (121 B — `02B47758` object: when `00273A20(+0x2A0)` returns 1 and `+0x2E0` bit 4 is set, calls `*[rbx+0x2A0]` with a `0x1F` arg block — a conditional notification dispatch), `003CB3E0` (34 B — `02B47760` `+0x179D2 & 0x83 == 0x83` — the "fully materialised" readiness mask for the object `002B6570` mirrors) | a per-frame presentation sync: one lazily built `0209E5C0` object mirrors a `0x20`-byte state block out of `02B47760`, takes two indirect dispatches, and is gated by readiness/getter predicates on the three `02B477xx` globals |

Interior citations — one instruction each, verified inside the declared extents:

| body | interior cite | what is there |
|---|---|---|
| `0017DE10` | `0017DE1B` | `mov rbx, [rax+0xDF8]` — the device-object slot on the `00796E20` manager |
| `0017E4C0` | `0017E4CC` | `call 0079E640` — the manager byte-state query |
| `00227D70` | `00227D84` | `mov dword [01E027F8], 6` — the countdown reload on `0035F150` success |
| `00228380` | `00228405` | `dec eax; mov [01FD46FC], eax` — the countdown tick while `01FD4940` is null |
| `00228490` | `002284CD` | `call 00244F50` — the widget constructor, `0xD0` bytes, proc `002284F0` |
| `00228700` | `00228777` | `mov [rcx+0xC8], rax` — installs the new object on `0209AC30` |
| `002287D0` | `00228856` | `dec al; mov [rcx+0xDED], al` — the `+0xDED` countdown byte on `0209AC30` |
| `002289D0` | `00228A33` | `cmp word [rdx+0xE2], bx` — the state-word test that picks the `00251D90` arg `2` or `3` |
| `002500F0` | `0025010C` | `call 002E25B0` — the second probe, `edx = ebx + 0x21` |
| `002501A0` | `002501BD` | `idiv ecx` — `020927DC % cvttss2si(xmm0)`, the temporal decimator's remainder test |
| `00252B60` | `00252BE6` | `and esi, 0x400` — the stick-direction bit folded into the capability decision |
| `00252C80` | `00252CD0` | `mov dword [01E0C2B8], 1` — the force-fight latch write |
| `002B6220` | `002B6249` | `mov ecx,0x500` at `002B6244` feeding `or word [rax+0x179D2], cx` — the flag OR on the freshly ensured `0209E5C0` object |
| `002B6570` | `002B65DC` | `call rax` — the first of the two `vtable[0]` dispatches, arg block `0x10` |
| `002E25B0` | `002E25B4` | `cmp byte [0215F1A1], 0` — the suppression flag checked before any selector case |
| `003606B0` | `003606C0` | `cmp dword [rcx], 0` — the scan loop over `022CB9C4`–`022CB9CC` |
| `00366870` | `00366902` | `cmp eax, r8d` — the accumulated count `022CBE18` vs the threshold `022CBE08` |
| `003669F0` | `003669F7` | `shr eax, 2` — the bit-2 extract from `022CBE1A` |
| `003C9570` | `003C957C` | `test byte [rax+0xC0], 8` — the gate bit before the `+0xCC` read |
| `003CA200` | `003CA264` | `call rax` — the conditional dispatch through `[rbx+0x2A0]` |
| `003CB3E0` | `003CB3F3` | `and al, 0x83; cmp al, 0x83` — the three-bit readiness mask on `+0x179D2` |
| `00862CF0` | `00862D0B` | `call qword [02EBA3F0]` — the indirect device-state poll |

The subtree's shape is an arbiter: read the raw device facts, decide whether the modal objects
own this frame, apply the force-fight toggle, and mirror the presentation object — which is why
the root can sit on the consumer list of a *mode* ladder without itself deciding any mode.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Rewards_Progression_Economy — SERVICE and CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot` and `Reward_ComputeExperienceForRecipient` sit on cited edges, as does `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`. Two further rewards bodies (432 and 488 bytes) and a 122-byte helper complete the eight.

- **Developer — CLIENT.** *(R3 clause 1 pair at HEAD, 2026-09-14, FABLE; tier 1 for the two instructions named)* The device probes above fetch their manager through the 8-byte getter `00796E20`, which returns the singleton `[02EA5368]`. The Developer layer calls the same getter: the 1,046-byte `MultipleDebugDisplay` body calls it at `001C2F77` and returns at once unless byte `+0x10D4` of that manager is set (`001C2F7C`–`001C2F83`). The crossing is one shared singleton getter, not a shared responsibility.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — SERVICE.** `0030D810` on this page calls `BattleStats_ModifySecondaryResource`, owned by that layer. What it reaches is the secondary-resource modification: it resolves the owning unit, and bit 0 of its flags argument chooses between the direct path and the one that consults the two helpers either side of it; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — SERVICE.** `0023A570` on this page calls `SpawnKeep_ResolvePrimaryEntry`, owned by that layer. What it reaches is a 56-byte bounds-checked index into the keep: the count is `byte[+0]`, the entry byte is `byte[+1 + index]`, `0xFF` means empty, and the record it names sits at a **`0x250`-byte stride**; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).


**ActorEntity — CLIENT (SWE2-EC7-156, 155 edges).** That layer's bodies consult this page's helpers — `00263660`/`0026C5D0` call `00226280`, `0025D9E0` calls `00233AA0`, and batch-121's `002E26F0` adds its own `0025D480`/`0025D540`/`002EDAA0`/`0042F3B0` to the same fan-in; the crossing is shared-helper consultation, not a shared responsibility.
**Presentation — CLIENT and SERVICE (SWE2-EC7-156, 219 edges).** `001D50D0` is called by `00187950`/`001BC190`/`001D5xxx` of that layer and calls `001CCB20` in return; the render layer and the ladder exchange helpers both ways — not a second owner.
**Script_VM_Native_Bridge — CLIENT (SWE2-EC7-156, 169 edges).** `0033FED0`/`0034BA00` call `00229E40`, `00354D00` calls `00229EA0`, and `00236760` is reached the same way; the script bridge consults this page's helpers — shared fan-in, not a shared responsibility.

**UI — CLIENT (SWE2-EC7 batch-149).** `0028FD70`, a callee the `0035D980` entry's teardown arm cites, sits inside that layer's fan-in: it calls UI bodies `00290E10`/`002964D0`/`00296AA0`/`002970C0`/`00297100`/`003CA1C0`/`003CA1E0` and is itself called by the UI-filed `0035D6B0` - the ladder borrows a shared teardown step; the UI edges are that helper's own traffic, not a UI responsibility of this page.

**WorldAreaField — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 166).** `00236760` is reached from that layer's `003145E0`/`005843E0`/`00584580` while `0023A570` (this page's SpawnKeep resolve above) is one of its callees; batch-166's `003EBBB0` rides `0032A100`'s clock-advance, which the field frame consults - the ladder and the field layer exchange helpers; no shared ownership.

**Party — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 167).** The batch-167 `00299BD0` row-eligibility sweep resolves each row through `0035BB00`/`0035BB20`/`00247930` helpers that layer also drives (`00303F00`/`00358A20` call in; `00326500`/`003272A0` are its far ends), so the ladder's Party traffic is shared-helper consultation on both sides - 90 edges, no shared ownership.


**Combat, CombatAI, Gameplay and Status_Periodic_Terminal — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 169).** `00263E30`, the mode-object getter the batch-169 `00320CA0` gate reaches through `[+0x698]`, is a shared helper those layers' bodies call directly (`003206E0`, `003247F0`, `00324F20`, `003176E0`, `0031ADB0`, `00321380`, `00386860`, `00310DB0`, `00301140` among them), while `00309A90`, `0030EC00`, `0023A570`, `00265680`, `002ECF10` and `0030C470` exchange calls with the same layers in return - shared-helper fan-in on a runtime getter, not a shared responsibility with any combat or status layer.
- **Audio — CLIENT and SERVICE (20 edges).** 11 inbound (Audio bodies `00229AF0`, `003638B0`, `00362850` call page-cited `003603C0`, `00229EA0`, `002E0FA0`); 9 outbound (page-cited `00228C70`, `00366870`, `00226280` call Audio bodies `002DF370`, `002DEE70`, `00363560`). Substantive edges include `00228C70` calls `00363560`; `00228C70` calls `00360D70`; `00228C70` calls `00249CA0`; `00228C70` calls `002DEE70`; the remaining edges run through shared helpers the page cites.
- **Input — CLIENT and SERVICE (110 edges).** 81 inbound (Input bodies `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70), `0017DE10`, `0017DDC0` call page-cited `00796E20`, `InputBackend_IsControlCode28To283ActiveForBank` (0079E6A0), `00197710`); 29 outbound (page-cited `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70), `InputControl_PollAndBuildChannelHistory` (0035F420), `002284F0` call Input bodies `0035F150`, `001E0F20`, `InputGameplay_TestCombinedMaskBit1WithTemporalGate` (00250200)). Substantive edges include `0017DE10` is called by `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70); `0017DE10` calls `InputBackend_IsControlCode28To283ActiveForBank` (0079E6A0); `0017DE10` calls `00197710`; `00197710` is called by `0017DE10`; the remaining edges run through shared helpers the page cites.
- **InputGameplay — CLIENT and SERVICE (4 edges).** 3 inbound (InputGameplay bodies `00313A00` call page-cited `002E1C20`, `002E1CA0`, `FieldData_GetActiveFieldRecordBit15` (00377C20)); 1 outbound (page-cited `00313DB0` call InputGameplay bodies `00313A00`). Substantive edges include `00313DB0` calls `00313A00`; `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `00313A00`; the remaining edges run through shared helpers the page cites.
- **RNG_Random_Selection — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_Seed` (00379CF0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **Save_Load_Settings — CLIENT and SERVICE (20 edges).** 16 inbound (Save_Load_Settings bodies `SaveLoad_ControllerLifecycleHandler` (00582860), `SaveImage_FinalizeHeaderAndChecksum` (00583D60), `SaveTransitionMetadata_RestoreFromRecord` (002EF410) call page-cited `00236760`, `002E1C20`, `002E1CA0`); 4 outbound (page-cited `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210), `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` (005843E0) call Save_Load_Settings bodies `SaveImage_GetActiveRuntimeBuffer` (002EF640), `SaveTransitionMetadata_RestoreFromRecord` (002EF410)). Substantive edges include `00236760` is called by `SaveImage_FinalizeHeaderAndChecksum` (00583D60); `00236760` is called by `SaveloadManager_ShouldAutosaveForTransition` (001C1720); `00236760` is called by `SaveImage_CopyCaptureToWriteSubmissionBuffer` (002EF690); `SaveTransitionMetadata_RestoreFromRecord` (002EF410) is called by `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210); the remaining edges run through shared helpers the page cites.
- **Story_Event_Quest_Hunt — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared Story_Event_Quest_Hunt plumbing (`PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0)) - the helpers' general call surface, not a Story_Event_Quest_Hunt relationship of this page's subjects.
## The `002EF410` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`SaveTransitionMetadata_RestoreFromRecord` (`002EF410`, 117 B) is the mode
restore half of the `002EF3C0`/`002EF410` pair: `xmmword[rcx+8]` →
`[02EBF190]+0x5AE0` (`002EF420`–`002EF424`), `dword[rcx+0x28]` → `+0x5B04`
(`002EF432`–`002EF435`); when `byte[rcx+0x18] & 2` the `+0x18`/`+0x20`
block restores through `003139D0` (`002EF43B`–`002EF458`); when
`byte[rbx+8] & 1` the `+0xC`/`+0x10` floats restore through `00304790` /
`003047C0` (`002EF463`–`002EF472`) and `+0x5B04 |= 2` marks them present
(`002EF47E`).

| member | role | interior |
| --- | --- | --- |
| `00304790` (42 B) | keyed float setter, slot 1 — `maxss xmm1, xmm0` floors the argument at `2.0f` (`movss` 2.0f at `00304794`, `maxss` at `0030479F`), `r8d = 0`, `003EBC50`, `ecx = 1`, tail `003EBD00` (`003047B5`) | [`0030479F`](../../_index/ADDRESS-INDEX.md) |
| `003047C0` (33 B) | keyed float setter, slot 2 — same shape but `movaps xmm1, xmm0` passes the argument unmodified, **no floor** (`003047C7`), `ecx = 2` (`003047D3`) | [`003047C7`](../../_index/ADDRESS-INDEX.md) |
| `003139D0` (42 B) | keyed float setter, slot 2 — `xmm1 = 2.0f` (`003139D4`), `003EBC50`, `ecx = 2`, tail `003EBD00` (`003139F5`) | [`003139D4`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003EBC50`, `003EBD00`. The restore's
`& 2` / `& 1` record flags and the `+0x5B04 |= 2` present-mark are the same
flags `002EF3C0` writes on the save side — the two bodies must be read
together.

## The `00306760` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00306760` `BattleAction_UpdateSpecialPresentationSequence` (~~293 B~~ 911 B of code, to the `ret` at `00306760+0x38E`, followed by its switch table up to `00306760+0x3A8`) *(corrected 2026-10-02, OPUS: measured)* —
the special-presentation tick: `003098D0` (`00306798`), `003299B0`
(`003067A5`), `dword[022C215C]` sequence state (`003067AA`), the
`[02EBF190]` context (`003067DB`), member `00306D90` (`003067F4`),
record `022C1F50` (`003067FB`), then `[02EBF138]` + `0020E600` row
lookups (`0030680D`/`00306817`) and `0030EC00` (`00306834`).

| member | role | interior |
| --- | --- | --- |
| `002FA0E0` (86 B) | authored-row accessor — `[02EBF130]` context, `dword[rax+0xC]` key → `0020E600` (`002FA0E6`/`002FA0F4`/`002FA0F7`), second pass `002FA101`/`002FA108` | [`002FA0F7`](../../_index/ADDRESS-INDEX.md) |
| `00306D90` (207 B) | presentation worker — `(rcx, edx, r13d)`; stack-cookie prologue, null-gate on `rcx` (`00306DC5`) | [`00306DC5`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003098D0`, `003299B0`, `0020E600`,
`0030EC00`. The `022C215C` dword is the sequence state; `022C1F50` the
record base.

## The `00303F00`/`00304060` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`00303F00` ~~(~27 B)~~ (342 B, `ret` at `00303F00+0x155`) *(corrected 2026-10-02, OPUS: measured)* — `qword[02EBF190]` base load (`00303F14`).

| member | role | interior |
| --- | --- | --- |
| `0017D3A0` | `001D50D0()` → `byte[rax+0xE1E] != 0` bool getter (`0017D3A4`/`0017D3AB`) | [`0017D3AB`](../../_index/ADDRESS-INDEX.md) |

`00304060` ~~(~11 B)~~ (222 B, `ret` at `00304060+0xDD`) *(corrected 2026-10-02, OPUS: measured)* — `0031B8C0(3)` non-null gate (`0030406B`/`00304073`).

| member | role | interior |
| --- | --- | --- |
| `002E28C0` | `r8d = 0xF` forward to `002E26F0` (`002E28C0`/`002E28C6`) | [`002E28C0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001D50D0`, `0031B8C0`, `002E26F0`.
`0017D380` is the `+0xE1D` twin getter.

## The `00303F00`/`00304060` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`00303F00` ~~(~27 B)~~ (342 B, `ret` at `00303F00+0x155`) *(corrected 2026-10-02, OPUS: measured)* — `qword[02EBF190]` base load (`00303F14`).

| member | role | interior |
| --- | --- | --- |
| `0017D3A0` | `001D50D0()` then `byte[rax+0xE1E] != 0` bool getter (`0017D3A4`/`0017D3AB`) | [`0017D3AB`](../../_index/ADDRESS-INDEX.md) |

`00304060` ~~(~11 B)~~ (222 B, `ret` at `00304060+0xDD`) *(corrected 2026-10-02, OPUS: measured)* — `0031B8C0(3)` non-null gate (`0030406B`/`00304073`).

| member | role | interior |
| --- | --- | --- |
| `002E28C0` | `r8d = 0xF` forward to `002E26F0` (`002E28C0`/`002E28C6`) | [`002E28C0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001D50D0`, `0031B8C0`, `002E26F0`.
`0017D380` is the `+0xE1D` twin getter.

## The `00347820` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00347820` (5 B) — `jmp 0037CFC0` thunk.

| member | role | interior |
| --- | --- | --- |
| `0037CFC0` | `ecx = 0` then `jmp 00303D90` — mode-0 forward (`0037CFC0`/`0037CFC2`) | [`0037CFC0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00303D90`.

## The `0037D110`/`0037D120` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

Two plain `jmp` thunks into the `02EBF190 + 0x5B04` bit ~~getters~~ setters *(corrected 2026-10-02, OPUS: each compares the bit with `ecx` and writes the word when they differ, `00307200+0x16`–`+0x2C` and `00307240+0x16`–`+0x2C`)*.

| root | member (target) | role | interior |
| --- | --- | --- | --- |
| `0037D110` | `00307200` | ~~`dword[+0x5B04] >> 3 & 1`~~ sets or clears bit 3 to `ecx`, no write when equal *(corrected 2026-10-02, OPUS: `00307200+0x1E`/`+0x29`)* | [`00307210`](../../_index/ADDRESS-INDEX.md) |
| `0037D120` | `00307240` | ~~`dword[+0x5B04] >> 2 & 1`~~ sets or clears bit 2 to `ecx`, no write when equal *(corrected 2026-10-02, OPUS: `00307240+0x1E`/`+0x29`)* | [`00307250`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-19 update (2026-05-15) — `003EBC50` timer-floor query tail

`003EBC50` (162 B) is the `02B5EBC0` row-commit the mode-1/2 arm runs (`003EBC50(2)`/`003EBD00(2)` callers): `ecx` indexes a `0x14`-stride row (`rbx = rcx*5*4` at `003EBC6C`), `[row+4]=r8d`, `[row+0]=cvttss2si(xmm1)` (`003EBC70`..`003EBC79`); then `00290180` (`003EBC7C`) selects the rate constant — `eax==2` reads `[00D1181C]`, else `[009002BC]` (`003EBC86`/`003EBC90`) — and when `[row+0] >= [row+4]` that rate is sign-flipped (`xorps` with `01CEBDA0` at `003EBCA1`). The row closes with `[row+0xC]=rate`, `[row+8]=cvtdq2ps([row+0])` then overwritten by `xmm6` (`003EBCDC`), `[row+0x10]=0`, and `[row+0x11] = (rate==0)` (`003EBCBB`..`003EBCD7`) — the (value, bound, rate, arrived-flag) record the mode ladder's timer arms maintain.

## SWE2-EC7-22 update (2026-09-18) — `003EBB70` *20-stride byte getter

`003EBB70` (19 B) is the table byte getter the ladder's mode readers share:
`movsxd rax, ecx`, `rax*5` then `[02B5EBD1 + rax*4]` — an index*20 row byte,
sign-extended out. Interior anchor `003EBB73` (the stride multiply). The
`02B5EBD1` base is the static row bank the runtime-mode dispatchers read.

## SWE2-EC7-25 update (2026-09-18) — `00332130` + `003272F0` slot helpers

`00332130` (93 B) clears bit 0 of `022C6E48[ecx]`'s pointer: on transition
to zero it `00263FF0`-resolves the index and clears `byte[+0x11] & ~8`, and
on was-nonzero-becomes-zero it runs `0032F1B0` — the unmark-and-notify arm.
Interior anchor `00332150` (the `and ~1`).

`003272F0` (103 B) finds which of the four `00263750(i)` slots holds the
`003588B0(003590D0())`-resolved object — gated on `02089340 & 0x10` — and
returns the slot index or -1. Interior anchor `00327322` (the compare call).
## SWE2-EC7-31 update (2026-09-18) — `00254B40` zero-option forward

`00254B40` (10 B) is the shim the ladder posts through
`00254B40(3)`: it zeroes `edx` and `r8d` and tail-jmps `00254B50`
— the mode-ladder body proper — so the post runs with both option
registers cleared. Interior anchor `00254B45` (the `jmp 00254B50`
tail).
## SWE2-EC7-32 update (2026-09-18) — `00254B50` gated request executor

`00254B50` (263 B) is the body `00254B40`'s zero-option post reaches:
`ecx & 0x7FFF` is the request id, `02092734 == 1` refuses outright,
and the `002E0FA0()` mask folded through the `01E0C2C4` table (the
same 11-bit `rol` loop `00254500` runs) must carry the request's bit
— `bt r10d, ebx` fails to 0. Past the gate `0017E7D0`/`0035DA80`/
`003C8990` run, then `ebx - 1 <= 0x17` dispatches a six-arm jump
table at `0x134C58`/`0x134C70` (`0035D660`, `0035D980`, `003C87B0`,
`0028E970` returning 1, `0035D080`); out-of-range ids fall to
`0028F970()` plus a `00280A00(ecx, edx, r8)` passthrough. Interior
anchor `00254BF9` (the `jmp rcx` dispatch).

## SWE2-EC7-33 update (2026-09-19) - `003B1BA0`

`003B1BA0` (**1,599 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,739 B, a wrong literal in the batch-33 append — the body is 1,599 B per the function list*) is the ladder's record enumerator - 19 `0020E600` id-record calls plus `0036C140`/`0036C1D0`/`00229E40`/`0024EE60`/`0024C460`. Interior anchor `003B1DEB` (an `0020E600` call).

## SWE2-EC7-37 update (2026-09-19) - `003B4B60`

`003B4B60` (567 B) is a battle-runtime mode body - `02B40512`/`02B4050A`/`02B40508`/`02B40511` byte flags, `002EA030`/`003E56C0` pairs plus `003B54C0`/`003E6AA0`/`003B4FD0`. Interior anchor `003B4BBF` (an `002EA030` call).

## SWE2-EC7-39 update (2026-09-19) - `003B5520`

`003B5520` (428 B) is a battle-runtime-mode body - `02B40508`..`02B40514` byte fields/`022C6F28`, `003E6AA0` quadruple. Interior anchor `003B5578` (a `003E6AA0` call).

## SWE2-EC7-45 update (2026-09-19) - `0024FE70`

`0024FE70` (238 B) is a body - `0020E600`/`0024ED80`/`00333280`/`003A7460`/`003A74F0`. Interior anchor `0024FE8A` (a `0020E600` call).

## SWE2-EC7-46 update (2026-09-19) - `0030D720`

`0030D720` (229 B) is a call-free `022C2170`-region defaults reset - `-1`, `0x40800000`x2, a 4x`0x40` qword-zero loop, then trailing string-field zeroing. Interior anchor `0030D722` (the `-1` store).

## SWE2-EC7-47 update (2026-09-19) - `00270150`

`00270150` (218 B) is a body - `0024F650`/`0024F680`/`0024FE70`/`0036C140`/`0036C1D0`/`00808C40`. Interior anchor `0027019D` (a `0024F650` call).

## SWE2-EC7-49 update (2026-09-19) - `003A74F0`

`003A74F0` (189 B) is a battle-runtime ladder body - `003337B0`/`003A7360`/`003A7460`/`003A81E0`/`003A9160`/`003AA430`. Interior anchor `003A74FD` (a `003337B0` call).

## SWE2-EC7-51 update (2026-09-19) - `003B2830`

`003B2830` (179 B) is a body - `0024FE70`/`0036C140`/`0036C1D0`. Interior anchor `003B288F` (a `0024FE70` call).

## SWE2-EC7-54 update (2026-09-19) - `003A9160`

`003A9160` (331 B) is a battle-runtime ladder body - `003697F0`/`003A8130`/`003A92D0` plus `02EBEF88`. Interior anchor `003A91B8` (a `003A92D0` call).

## SWE2-EC7-55 update (2026-09-19) - `003B4FD0`

`003B4FD0` (270 B) is a battle-runtime mode body - `003E6AA0` single call plus `022C6F28`/`02B4050A`/`02B4050C`/`02B40512` byte flags. Interior anchor `003B5042` (a `003E6AA0` call).

## SWE2-EC7-57 update (2026-09-19) - `003A7360`

`003A7360` (177 B) is a battle-runtime ladder body - `0024C6B0`/`0024C870`/`00333350`/`003697F0`/`003AF330` plus `02EBEFB0`/`02F97348`. Interior anchor `003A7380` (a `00333350` call).


## SWE2-EC7-57 update (2026-09-19) - `003A8130`

`003A8130` (176 B) is a battle-runtime ladder body - `003697F0` single call plus `02EBEF98`. Interior anchor `003A81BC` (a `003697F0` call).

## SWE2-EC7-59 update (2026-09-19) - `003B1260`

`003B1260` (164 B) is a battle-runtime ladder body - `0024FE70`/`0036C140`/`0036C1D0` plus `02EBEC00`/`02EBEF60`. Interior anchor `003B12CA` (a `0036C1D0` call).

## SWE2-EC7-62 update (2026-09-19) - `003B3C00`

`003B3C00` (148 B) is the `003B3C00(handle, n)` resolver the ladder names - `0024FE70`/`0036C140`/`0036C1D0`/`003B3480` plus `02EBD480`. Interior anchor `003B3C4D` (a `003B3480` call).



## SWE2-EC7-66 update (2026-09-19) - `003C8990`

`003C8990` (132 B) is the `003C8990` run body - `002470C0`/`00249C60`/`00252D90`/`0028FFE0`/`0035C080`/`0035D060` plus `02B47730`. Interior anchor `003C89AB` (a `00249C60` call).


## SWE2-EC7-74 update (2026-09-19) - `0035DA80` mode reset chain measured

`0035DA80` (61 B) is the reset chain the ladder callers run:
`002904B0()` nonzero triggers `00290450(1)`, `022C8380` zeroed,
`00290500(0)`, `00252D90()`, and a `00254980(0)` tail - the
five-step mode teardown.
Interior anchor `0035DAA8` (the `00252D90` call).

## SWE2-EC7-84 update (2026-09-20) - `00421030` flag resolver measured

`00421030` (157 B) is the `+0x284` flag resolver the ladder callers
run: bit 3 plus `(flags & 0x30) == 0x30` gate a `word[+6]`-chain
walk to its tail (`r9d` goes 1 when the link is -1); bit `0xA`
set with `r9d` clears `0xA` and sets `0x40`, `r9d` alone sets
`0x40`, otherwise `0x40` clears - the resolved dword and the
unchanged `word[+0x64]` commit together.
Interior anchor `004210AB` (the `+0x284` flag commit).

## SWE2-EC7-88 update (2026-09-20) - `003C87B0` ladder-step dispatch measured

`003C87B0` (371 B) is the mode-step the ladder callers run: a
null `[02B47730]` or a nonzero `003669D0()` returns 0;
`0035C150(0, eax+6)` runs and `[rdx+0xC4]` is cleared before an
8-arm jump on `dword[rdx+0xD0]` - arms run `003C9370`, the
`0035BAD0`/`0035D3E0`/`0035DCC0` sequence, or `02F9736A`
flag tests selecting `003C9250(3|4)`; a nonzero result then
runs `003C9420`, `00252B40(ecx,0)`, `002470D0([02B47730])` and
`0028FFE0(1,1)` to return 1.
Interior anchor `003C8834` (the jump-table index read).

## SWE2-EC7-89 update (2026-09-20) - `0028FFE0` + `00252B40` + `003C9420` + `003C9370` measured

`0028FFE0` (76 B) is the word-flag write the ladder arms call
last: on the `[0209BE80+0x10F80]` record it clears `0xFFEF`
(mode 0) or `0xFFDF` (mode 1) in `word[+0x1D7A]` and re-arms
`0x10` or `0x20` under `edx`.
Interior anchor `00290014` (the `and` write).

`00252B40` (29 B) is the masked-global store the ladder arm runs:
`ecx &= 0x7FFF` lands in `020927D8` and `02092730`, `edx` in
`02092734`, then a tail `00254740`.
Interior anchor `00252B58` (the `00254740` tail).

`003C9420` (117 B) is the mode-commit the ladder arms run:
`0035C150(6, ecx)` first; when `[02B47730+0xC4]` would change and
`ecx` is nonzero, `00249C60(1)` runs; `+0xC4` takes `ecx`, and a
nonzero `ecx` that `00273710` accepts and `0035BAD0` confirms is
also written to `+0xC8` (otherwise `+0xC8` is cleared).
Interior anchor `003C9439` (the `0035C150` call).

`003C9370` (112 B) is the membership scan the ladder arms run:
repeated `0035D3E0()` calls walk `dword[base + 8 + i*4]` for a
value equal to `ecx`, bounded by `dword[base]` - returning 1 on
the match, 0 otherwise.
Interior anchor `003C93A0` (the loop's `0035D3E0` call).

## SWE2-EC7-90 update (2026-09-20) - `00273710` mode validator measured

`00273710` (63 B) is the accept-check `003C9420` runs before
committing a mode: `0031FD20()` must pass, then
`00320CA0(ecx, &out)` must return 1 with the `0x80000003` bits
clear in the out flags - anything else returns 0.
Interior anchor `00273728` (the `00320CA0` call).

## SWE2-EC7-94 update (2026-09-20) - `0035F150` measured

`0035F150` (80 B) is the rung-read accessor `00227D70` and
`00228C70` call on the `0x294`-stride record table at `02CDB1C7`:
`ecx >= 2` returns 0; otherwise byte `+1` is advanced by `r8d`,
wrapped into 0-15 (negative input is `+0x10 & ~0xF` corrected), and
the result picks the signed byte at `+0x44` in the record's `9*4`
index row - the same `+0x44` layout `0035F420` writes.
Interior anchor `0035F19A` (the `+0x44` byte fetch).

## SWE2-EC7-95 update (2026-09-20) - `00313550` measured

`00313550` (58 B) is the mode-bit setter `00328BD0`, `0034E1F0`,
`0034FE80` and `0050FFB0` call: `ecx` is compared against bit 0
of the `+0x5B04` dword on the ~~`02EC4BA9` object~~ `[02EBF190]` block *(corrected 2026-10-02, OPUS: `00313550+0x0` `mov r8, [02EBF190]`)* - equal returns,
nonzero `ecx` ORs the bit, zero ANDs it off, and both changed
paths tail `0035C620` to propagate *(qualified 2026-10-02, OPUS, from ASTRA's SPEC-accepted [`mode-summon-tail`](../../_experiments/evidence/mode-summon-tail/README.md): 'equal' is the raw 32-bit ECX against bit 0, so 'changed' holds for 0/1 arguments only - with the bit set, any other nonzero value rewrites the same flags and still tails (a source countermodel, no natural caller shown); and the tail is more than propagation: it hands the fixed object `022CA408` to a 2,382-byte UI initializer whose prefix zeroes the object's first 32 bytes, under a normal stack probe, a valid frame and receiver and no interference; the rest of that body is not read)*.
Interior anchor `00313575` (the `0035C620` tail on the set arm).

## SWE2-EC7-96 update (2026-09-20) - `00304630` measured

`00304630` (17 B) is the byte-truncating thunk `0023A570` and
`003200A0` call: `003271D0` runs and `al` is zero-extended into
`eax` - the bool-shaped read the mode ladder consumes.
Interior anchor `00304634` (the `003271D0` call).

## SWE2-EC7-97 update (2026-09-20) - `002EA8E0` measured

`002EA8E0` (46 B) is the flag-bit toggle `00226280` and
`0030D8B0` call: `edx` nonzero sets bit `ecx` of
`byte[0215FD44]`, zero clears it, then `003E7CC0` runs with 1
when any bit remains, 0 when the byte is empty - the
set-and-notify the mode ladder applies to its flag byte.
Interior anchor `002EA8EB` (the `bts` arm).

## SWE2-EC7-98 update (2026-09-20) - `002E1020` measured

`002E1020` (14 B) is the indexed fetch `00228380`, `00228930`
and `00229AF0` call: `eax = dword[0215F1C0 + movsxd(ecx)*4]` -
the signed-index dword lookup the mode ladder's arms share.
Interior anchor `002E102A` (the table fetch).

## SWE2-EC7-99 update (2026-09-20) - `002CCC70` measured

`002CCC70` (36 B) is the indexed field fetch `00228C70`
calls: `0209AC30`'s `+0x290` pointer table at
`movsxd(ecx) * 8` yields the object, a null object returns
1, else `dword[obj+0xE8]` - the default-1 status read the
mode arms share.
Interior anchor `002CCC87` (the `+0xE8` fetch).

## SWE2-EC7-103 update (2026-09-20) - `00273950` measured

`00273950` (93 B) is the multi-gate predicate
`00253C70`, `002736B0` and `002C6F70` call:
`00254500()` supplies the id, `00254550(id, 1)`
nonzero or `00254550(id, 0x15)` nonzero short-out
to a `dword[02092730] == 1` check (returns 0),
`003669D0()` nonzero also returns 0, and otherwise
the answer is `(~002E0FA0() >> 4) & 1` - the
inverted flag bit the runtime-mode arms consult.
Interior anchor `00273997` (the `002E0FA0`
call).

## SWE2-EC7-104 update (2026-09-20) - `0028FA00` measured

`0028FA00` (44 B) is the flag gate `00253C70`
and `002736B0` call before tailing into
`002C6450`: it loads `[0209BE80 + 0x10F80]`,
returns 0 when that pointer is null, otherwise
reads `word[ptr + 0x1D7A]`, computes
`(~(w >> 3)) & 1`, and only when the bit is set
falls through to `002C6450` - a one-bit
permission check in front of the shared tail.
Interior anchor `0028FA16` (the `+0x1D7A` word
read).

## SWE2-EC7-106 update (2026-09-20) - `00250200` + `00250130` + `0024F650` measured

`00250200` (110 B) is the combined
frame-modulo gate `00253C70` and
`002B7B80` run: the first arm probes
`02F97362` bit 1 when `00229DF0()`
answers 0 or `dword[020927DC] %
cvttss2si(00229E00())` lands on the
beat; the second probes `02F97392`
bit 0 when `00229DF0()` answers 0,
`002B9FC0()` answers nonzero, or the
modulo lands - a modulo miss on the
second arm answers 0 - the
period-locked flag test the runtime
ladder shares.
Interior anchor `00250223` (the first
flag test).

`00250130` (66 B) is the narrower
sibling `00253C70` and `002BAF80`
run: `00229DF0() == 0`,
`002B9FC0() != 0` or `dword[020927DC]
% cvttss2si(00229E00()) == 0` gates
the `02F97392` bit-0 answer - the
same cadence counter with a single
flag behind it.
Interior anchor `00250163` (the
`02F97392` read).

`0024F650` (45 B) is the chain find
`0026FDB0` and `00270150` call:
from `rcx` it walks the `[+0x348]`
links comparing `word[+4]` against
the start node's own `word[+4]`, and
answers the first matching sibling
or 0 - the locate half of
`0024F920`'s tag write.
Interior anchor `0024F668` (the
`word[+4]` compare).

## SWE2-EC7-107 update (2026-09-20) - `00229E00` measured

`00229E00` (20 B) is the indexed
cadence-divisor read `00250130`,
`002501A0` and `00250200` fold into
their frame-modulo gates: `xmm0 =
float[00908BA8 + movsxd(dword
[01FD4A98]) * 4]` - a four-byte-stride
float table indexed by a live global
selector, the period every `020927DC`
modulo is taken against.
Interior anchor `00229E0E` (the
indexed `movss`).

`00238A60` (23 B) is the two-slot
clear `00306570` and `003065D0` run:
`dword[02089340] &= ~1`, then qword
`0208E6A8` and dword `0208E6A4` are
zeroed - the flag drop plus head
reset the field-frame and runtime
arms share.
Interior anchor `00238A69` (the first
qword clear).

`00254980` (101 B) is the mode-selecting call battery the `0035D6B0`/`0035D8D0`/`0035D980`/`0035DA80` ladder quartet shares: `ecx == 0` picks `002E1C20`, any other mode picks `002E1CA0`, and the selected helper runs six `(8, n)` pairs - `edx` = 1, 8, 0, 0xB, 9, 6 - before a tail `(8, 0x14)`; `ecx` itself is consumed only by the selection, the battery is fixed.

Interior anchor `002549A2` (function `00254980`).

`00290500` (26 B) is the conditional forwarder the ladder quartet calls: `rax = [0209BE80]`, `rcx = [rax+0x10F78]` - a null field returns, otherwise `00296BE0(rcx, ecx)` runs as a tail call on the same `0209BE80` global the gate family reads.

Interior anchor `00290509` (function `00290500`).

`002E26F0` (454 B) is the two-record comparator `002E28C0`/`0034A640` call: `rsi = [rcx+0xC0]` / `rdi = [rdx+0xC0]` null-gate, `byte[rax+0x14F] & 1` runs `002E6B10(rbx)`, `dword[rsi] == -1` sentinels short-circuit, then `0025D480`/`0025D540`/`002EDAA0`/`0042F3B0` compare the pair - the ladder's transition test.

Interior anchor `002E2756` (function `002E26F0`).

`0035D980` (251 B) is the four-slot claim probe `00254B50` runs: gated on `002E0FA0()` bit `0xA` and a `0035BC50(0)` refresh, it scans the `022C8080` 0xC0-stride slots bounded by `022C8064` for the first claimant (`+0x60` bound ok, `+4` nonzero, flag bit0 clear); on a claimant, `022C83E8` bit `0x40` set runs `0035D080(kind)` and clears the bit, bit clear runs the `0035BC50`/`0028FD70`/`00290450(2)`/`00290500(1)`/`00254980(1)`/`00252B40(kind,1)` teardown - both return 1; with the `0xA` gate clear it clears `022C83E8` bit `0x40`, calls `00249C60(5)` and returns 0

Interior anchor `0035DA0E` (function `0035D980`).

`0028FD70` (193 B) is the request-state probe `0035D980` and `0035D6B0` share: a null `0209BE80` returns `0`; `003CA2E0() == 1` runs the `00290E10` + `002970C0` + `003CA1E0` arm and returns `1`; otherwise `003CA1C0()` then the `002E0FA0()` bit `0xA` gate picks `00290E10` + `00297100` (return `1`), and the fall-through runs `002970C0`, lazily fills `0209BE80`'s `+0x10F78`/`+0x10FC8` via `002964D0`/`00296AA0`, and returns whether `+0x10F78` came back non-null

Interior anchor `0028FDD1` (function `0028FD70`).

`0035D080` (93 B) is the deferred-register shim `00254B50` and `0035D980` call: while `022CA428` is empty it registers `0035D6B0` through `00244F50` (`0xC8` frame) with a two-field `{0, ecx}` stack record, then returns `1` either way

Interior anchor `0035D0B5` (function `0035D080`).

`00290E10` (148 B) is the two-slot teardown `0028FD70` arms inside its `003CA2E0` and `002E0FA0` branches: on a non-null `[0209BE80 + 0x10F78]` it first sets the object's `+0x40` bit `0x10000` when `002544B0()` returns `1`, closes it through `00244F00`, clears the slot and runs `0028F0C0(0)`; a non-null `[0209BE80 + 0x10FC8]` is then torn down through `00296A70` and cleared - both pending request objects released in one pass

Interior anchor `00290E42` (function `00290E10`).

`002970C0` (64 B) is the single-slot close `0028FD70` shares with the `+0x10F78` arm: on a non-null `0209C300` it sets the object's `+0x40` bit `0x10000` when `002544B0()` returns `1`, closes it through `00244F00`, and nulls the global - the same flag-then-release shape `00290E10` uses per slot

Interior anchor `002970DF` (function `002970C0`).

`00429F70` (223 B) is the recursive record walk `00427DE0` runs over the `022C6F28` `0x740`-stride table: from `rcx`'s u16 head index (`-1` ends) it `0042DF10`-visits each record into a stack out-pair, then recurses through `0042EF90` on the `+8` and `+0xA` u16 links - a depth-first sweep of the chain with the caller's `+0x308` float carried in the out record

Interior anchor `00429FD0` (function `00429F70`).

`00429500` (220 B) is the sibling walk `00427DE0` runs with visitor `0042BED0`: identical `022C6F28` `0x740`-stride recursion over the `+8`/`+0xA` u16 links through `0042EF90`, the caller's `edx` carried in the out record - the same graph shape with the other visitor

Interior anchor `0042955D` (function `00429500`).

`0042B690` (216 B) is the `0042EF90`-recursion sibling `00427DE0` runs with visitor `00420D80`: identical `022C6F28` `0x740`-stride chain walk over the `+8`/`+0xA` u16 links, this one carrying `(+0x304 >> 0xA) & 1` in the stack out-record's flag slot

Interior anchor `0042B6E2` (function `0042B690`).

`0042B770` (216 B) is the fourth sibling walk over the same table - visitor `00420E70`, flag `(+0x304 >> 0xB) & 1`, recursion through `0042EF90` on the `+8`/`+0xA` links - the batch-152 `00429F70`/`00429500` pair completed into a four-visitor ladder

Interior anchor `0042B7C2` (function `0042B770`).

`00420D80` (228 B) is the visitor `0042B690` applies per `022C6F28` record: `+0x18`'s index `0020E600`-resolves a container whose `+0xD98` `002ED570`-resolves the record; `00422D50`/`00422D10` fetch the linked pair, `+0x2AE` bit 0 takes the `ebp` flag, the resolved record's `[+0]` bits are rewritten `(clear 4) | (ebp ? 0 : 4)`, and `r14`'s `+0xC` gets `0x800000` when `ebp` is nonzero

Interior anchor `00420DA9` (function `00420D80`).

`0042DF10` (167 B) is the mode-commit selector `00429F70` runs: after the `00426220` gate on `[rdx+8]` passes, a live `[rbx+6]`/`[rbx+0x2F8]` pair (with `+0x2F2 != ax`) computes `r8d = sword[rax+0xCC]` and `edx = (byte[rax+0x40B] << 6) >>s 6`; a non`-1` `0041E5B0` result tail-jumps `00423FC0`, otherwise `+0xCC < 0x1000` picks `00422E40(xmm1 = [rdi+0x28])` over `00422E50`

Interior anchor `0042DF66` (function `0042DF10`).

`003EBBB0` (148 B) is the `02B5EBC0` `0x14`-row updater `0032A100` calls, the same record shape this page's `003EBC50` commits: `[row] = edx`, `[row+4] = r8d`; `00290180()` picks the rate constant (`00D1181C` when `eax == 2`, else `009002BC`), negated via `01CEBDA0` when `[row] >= [row+4]`; then `[row+0xC] = rate`, `[row+8] = float(edx)`, `[row+0x10] = 0`, `[row+0x11] = (rate == 0.0)` - the value/bound/rate/arrived record the ladder arms maintain.

Interior anchor `003EBBD0` (function `003EBBB0`).

`00299BD0` (318 B) is the row-eligibility mark `00296BE0` runs under this ladder's mode: after `003590D0` reads the population count it loops the `+0x318` rows to `byte[rbp+0xB42]`, resolving each row's `byte[+7]` index through `0035BB00`/`0035BB20` and gating on `002739D0`/`00247930`; rows whose record passes get `or word[+0], 1` set and feed the `r14`/`r15` match counts the ladder's mode step consumes.

Interior anchor `00299BEC` (function `00299BD0`).

`002739D0` (41 B) is the pure predicate form of the `00320CA0` gate this page names at the mode-check row: `00320CA0(ecx, &out)` must return 1 and the out-dword must carry none of the `0x80000003` bits - the caller-visible availability test `00299B90`/`00299BD0`/`003F77F0` run.

Interior anchor `002739D9` (function `002739D0`).

`00320CA0` (80 B) is the availability gate `002739D0`'s predicate wraps: when `byte[02089340] & 0x10` it runs `003588B0` for the mode object, `00263E30` for its `+0x698` child, and writes `dword[+0x64] | dword[+0x3c]` of that child into the caller's out-dword with a 1 return; any missing link or the flag clear falls to the 0 arm - the ladder's `mode is up and its flags are these` contract.

Interior anchor `00320CC9` (function `00320CA0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-battle-runtime-mode-ladder-cloudint-1001/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0025D540` | 64 B | returns without work when byte `+0x18` of `rcx` equals 1; otherwise loads qword `+0xC0`, and when it and that object's qword `+0x138` are both non-null calls `003DA9F0(qword +0x138)` and stores byte 0 at that object's `+0xEF` | `0025D544`, `0025D54F`, `0025D55B`, `0025D56A`, `0025D56F` |
| `0028E970` | 122 B | loads the pointer at `0209BE80`; when its qword `+0x10FB0` is non-null calls `00245020(that qword)`, zeroes the field and calls `00252D90()`; then, when the field is zero, calls `00252B40(ecx, 0)` and stores `002D5030()`'s result in it; returns the field's low dword | `0028E98B`, `0028E997`, `0028E9BC`, `0028E9D0`, `0028E9DE` |
| `00296A70` | 44 B | calls `002544B0()` and, when it returns 1 and `rcx` is non-null, ORs `0x10000` into dword `+0x40` of `rcx`; then tail-jumps `00244F00(rcx)` | `00296A79`, `00296A7E`, `00296A88`, `00296A97` |
| `00296AA0` | 68 B | calls `00244F50(0xC0, 0029BC80, 0)`; when `002544B0()` returns 1 and that result is non-null ORs `0x8000` into its dword `+0x40`; calls `00246AC0(result)` and returns the result | `00296AB5`, `00296ABD`, `00296ACC`, `00296AD6` |
| `00296BE0` | 544 B | returns 0 when `rcx` is null; with `edx` zero and byte `+0xB49` equal to 1 it calls `00246AC0(qword +0xB38)`, clears bit `0x80` of word `+0xB4A`, calls `00290630()`, zeroes `+0xB49`, calls `002470C0(rcx)` and, when `00273A20(rcx+0xC0)` is non-zero, `00244F00(rcx+0xC0)`, clears bit 0 of `+0xB4A`, ANDs `0xFF78` into the word at `+0x318` of each of byte `+0xB42` records of stride `0x160` and zeroes qword `+0xB20`; with `edx` non-zero, byte `+0xB49` of 2 returns 0, and any value other than 1 is set to 1, stores the byte `0035BAE0` returns at `+0xB48`, `rcx` at qword `+0xB30` and `00297640` at qword `+0xB20`, clears bit 1 of `+0xB4A`, calls `00299BD0(rcx)`, `00244DD0(qword +0xB38)` and `0035BB00(byte +0xB48)`, ORs 4 into the `+0x318` word of record `+0xB48` when its bit 0 is set, else scans forward (wrapping) for a record with bit 0 set, stores its index (or the old one if none) at `+0xB48`, ORs 4 into its word and calls `0035BB00` again; it then clears bit 0 of `+0xB4A`, sets it when `0029C9D0(rcx)` returns 0, calls `003678F0()` and `002470D0(rcx)` and sets bit `0x80`; every other path returns 1 | `00296C17`, `00296C80`, `00296CF4`, `00296D74`, `00296DEE` |
| `00297100` | 97 B | loads the pointer at `0209C300`; when null calls `00244F50(0xF0, 0029C530, 0)` and stores the result there, otherwise ANDs `0xFFFC` into its word `+0xE6`; when `002544B0()` returns 1 and the pointer is non-null ORs `0x8000` into its dword `+0x40`; tail-jumps `00246AC0(pointer)` | `00297121`, `00297129`, `00297137`, `0029714D`, `0029715C` |
| `00299B90` | 59 B | calls `0035BB20()` and returns 0 when it is null, when its dword `+4` is zero, or when its dword `+0` has bit 0 or bit `0x40` set; otherwise returns 1 when `002739D0(dword +4, dword +0)` is non-zero, else 0 | `00299B94`, `00299BA8`, `00299BB3`, `00299BB8`, `00299BC1` |
| `002C6450` | 103 B | calls `003590D0()` and walks the list at qword `+0x1D70` of `rcx` (next at `+0x18`) for a node whose dword `+0x10` equals the result; with no match returns 1 when signed word `+0x1D78` is at least `0x80`, else 0; with a match returns 1 when (signed word `+0x1D78` times the node's byte `+0x14`) AND `0xFFFFFF80` is, signed, at least `0x4000`, else 0 | `002C6459`, `002C6470`, `002C6475`, `002C648C`, `002C64A8` |
| `002EA030` | 14 B | returns the dword at `01EEBAA0` indexed by sign-extended `ecx` times 4 | `002EA033`, `002EA03A` |
| `00309FB0` | 318 B | computes `ebx` from word `cx`: -1 for `0xFFFF` or when `cx` AND `0xF000` exceeds `0xE000` (unsigned); otherwise, in the `0x58`-byte row of `01EEBCC0` selected by `cx >> 12`, when `cx` AND `0xFFF` is at most (signed) dword `+0x3C` minus 1 and qword `+0x50` is non-null, the result of calling it with (`cx`, 0), else 0; then for i 0 to 3 calls `0031B810(i)` and keeps (up to 4, in `022C1788`) each non-null result whose qword `+0x698` is non-null and either has dwords `+0x64` OR `+0x3C` free of `0x80000003` or passes `00377C20(qword +0x698)` non-zero; adds 1 to `ebx` for each kept entry whose word `+0xDC8` equals `cx`, and returns `ebx` | `0030A00D`, `0030A039`, `0030A054`, `0030A089`, `0030A0D6` |
| `00321380` | 127 B | stores -1 at dword `[rdx]`; returns -1 when byte `02089340` lacks bit `0x10`, when `003588B0()` is null or when `00263E30(that)` is null; otherwise re-stores -1, returns -2 when the object's qword `+0x698` is null, else (with -3 for a null `+0x698` plus `0x50`) calls `00321400(word at +0x698 +0x50, rdx)` and returns 0 | `00321386`, `0032138F`, `003213B5`, `003213C1`, `003213DE` |
| `00327240` | 39 B | loads the pointer at `02EBF190` and its byte `+0x5AA4`; returns 0 when the byte exceeds `0x27` (unsigned), otherwise returns the pointer plus 8 plus the byte times `0x1C8` | `00327247`, `0032724E`, `00327258`, `00327263` |
| `0034A640` | 91 B | calls `00267E10(r9)` twice, then `00358940(002640C0(), second result)`; when that is non-null calls `002E26F0(it, rdx, first result)` and returns its value, otherwise returns 0 | `0034A658`, `0034A662`, `0034A673`, `0034A686` |
| `0034FE80` | 30 B | calls `00313550(0)` and `00314D40(1)`, then tail-jumps `0037CA00` | `0034FE86`, `0034FE90`, `0034FE99` |
| `0035D660` | 75 B | returns 0 when `002E0FA0()` has bit 10 set or `003669D0()` is non-zero, or when `ecx` is 1 with bit 0 of byte `022C8060` clear and dword `022C806C` zero; otherwise calls `0028FD50(ecx)` and returns 1 | `0035D66D`, `0035D67B`, `0035D689`, `0035D691`, `0035D69B` |
| `0035D8D0` | 171 B | returns without work when `002904B0()` returns 0; otherwise calls `00290450(1)`, zeroes dword `022C8380`, calls `00290500(0)`, clears bit 2 of dword `022C8060`, calls `00252D90()` and `00254980(0)`, then tests dword `022C83E8` (re-read after each call): bit 4 set calls `002548F0(1)`; bit 0 set calls `00254940(1)` and clears bit 4; bit 1 set calls `00254850(1)` and clears bits 0 and 4 | `0035D8DB`, `0035D8FC`, `0035D927`, `0035D944`, `0035D96F` |
| `00363560` | 96 B | calls `002DF0F0(0, dword 022CBA7C)` when dword `022CBA70` or dword `022CBA7C` is non-zero; then zeroes dword `022CBA70` and bytes `022CBB2D` and `022CBB2E`, calls `00362850()`, `003636A0()`, `00363750()`, `00362850()` and `002DF690(-1)`, and tail-jumps `002DF0F0(0, -1)` | `00363579`, `0036357E`, `00363596`, `003635AD`, `003635BB` |
| `003AA430` | 56 B | walks a chain starting at the qword the pointer at `02EBEF70` points to: for each non-null node calls `005043F0(node)` when its byte `+0xE` is `0x59`, then moves to `0020E600(dword [node])` | `003AA43D`, `003AA445`, `003AA44E`, `003AA455`, `003AA460` |
| `003B54C0` | 82 B | stores byte 2 at `+2` of `rcx`; before that, when word `+4` is not -1, takes the `0x740`-byte record it indexes (sign-extended) from the pointer at `022C6F28` and, when that record's dword `+0x284` is non-zero, calls `003E6AA0(record, 2)` | `003B54CD`, `003B54E0`, `003B54ED`, `003B54F9`, `003B54FE` |
| `003CA1E0` | 27 B | when the pointer at `02B47758` is non-null, clears bit 1 and sets bit 0 of its dword `+0xA90` | `003CA1E7`, `003CA1EC`, `003CA1F3` |
| `00420E70` | 41 B | clears bit 1 of byte `+0x2AE` of `rcx` and sets it again when `edx` is non-zero; tail-jumps `00421280` with `rcx`, `edx` = 1 when the incoming `edx` is zero else 0, `r8b` = 2 when the incoming `edx` is non-zero else 0, and `r9d` = the incoming `edx` | `00420E7E`, `00420E87`, `00420E91`, `00420E94` |
| `00422E50` | 96 B | when dword `+0xC8` of `rcx` is not -1, calls `0051B9E0(qword +0xDA8 of 0020E600(dword +0x10), dword +0xC8)` and, when that is non-null, ORs 2 into its dword `+0xC` and calls `0041D790(it)`; then tail-jumps `00424A40` with `rcx`, the incoming `xmm1` and `r8d` = 1 | `00422E56`, `00422E6D`, `00422E7F`, `00422E89`, `00422EAB` |
| `0050FFB0` | 59 B | calls `00267E10(r9)` twice, calls `003139C0` with the low byte of the first result, and tail-jumps `00313550` with the second | `0050FFC0`, `0050FFCA`, `0050FFD5`, `0050FFE6` |
