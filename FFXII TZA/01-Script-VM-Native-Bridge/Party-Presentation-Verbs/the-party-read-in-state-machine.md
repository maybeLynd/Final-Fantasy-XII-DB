---
system: The party read-in state machine — how a party member's actor is rebuilt for its current definition, one state per frame, after the party read-in verbs, a party swap or battle setup
category: 01-Script-VM-Native-Bridge
status: AUDITED — the part slots are SecondaryContext elements bound to model resources (UQ-49), the state-4/5 pair is a refcounted voice-pack swap and state 19 is highmodelreplace (UQ-50), state 16 syncs the def+0x13 variant selector to element 0 (UQ-51), and 022C8018 is an embedded machine record in the 00359800 driver (UQ-52)
owner_layer: Script_VM_Native_Bridge (the verb entries, from the verb table) and the world tick (the slot-mask entry); the machine itself carries no owner tag
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the 24-arm jump table of 0037B4D0 decoded from the image, every state write to the record's byte +8 located
    and placed by the jump that reaches it (members/party_read_states.py -> members/party-read-states.tsv); entries read
    at their call sites
last_reviewed: 2026-09-14
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: swe2-audit-sem-falsification-pass-1 vs exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  falsification_passes: 1
  last_falsification: 2026-09-14
  crossref_clean: true
  reopened_count: 0
---

# The party read-in state machine

> **`0037B4D0` is a 24-state machine that brings one actor's loaded parts in line with the actor's current definition.**
> It runs once per call, and each call advances as far as it can. A state that must wait for a load returns 0 and is
> resumed on the next call. State **23** means done, and the function returns 1.
>
> The script's party read-in verbs drive it slot by slot:
> - `partyallread` `0x3EB` and `summonread` `0x203`: slots 0 → 3;
> - `partyallread2` `0x46F`: slots 3 → 0.
>
> The world tick drives it for party slots flagged in a mask, and the ends of `setupbattle` and of the battle unit
> spawn run it directly.
>
> The machine's record is 12 bytes: an encoded actor pointer, a pending id, the state byte, the slot, and a part
> counter. The work it sequences is:
> 1. hide the actor;
> 2. release what the old definition loaded and request what the new one needs, in ~~four part slots~~ the element slots *(answered: six elements, one enum, UQ-49 2026-09-16; 2026-10-02, OPUS)*;
> 3. wait for each request's ready bit and apply it;
> 4. place the actor and activate its battle unit;
> 5. show the actor again.
>
> [The party standard-motion verbs](the-party-standard-motion-verbs.md) page named the entries. This page is the machine
> behind them.

## 1. What the player sees

Before a cutscene the party's models are loaded, and after a summon the summon joins the party. When a battle is set up,
each member appears in its battle form. Between those moments a party member briefly vanishes, has its model and motions
swapped for the ones its current definition calls for, and reappears in place. The waits are the frames spent loading.
A script that issues `partyallread` blocks (its poll is `0034E3E0`) until every slot has been through the machine.

## 2. Mechanism

### 2.1 The record

```
party read-in record            12 bytes; three statics are known (§2.2)
  +0x00  u32   actor            encoded image pointer (RuntimePointer_EncodeImageAddress 0020E620);
                                resolved each call by ImageAddress_ResolveRuntimePointer - null -> return 1 at once
  +0x04  u32   pending handle   the requested entry's handle (002EAE20 -> 002E9810), written by states 1 (0037B720) and 19 (0037BEA8)   <- corrected 2026-10-02, OPUS: also by states 7, 10 and 13 (0037B95F, 0037BA5A, 0037BB62) and at 0037BDF9, 0037BE31, 0037BE6B, 0037BEC9
  +0x08  u8    state | flag     low 7 bits: state 0..23; bit 7 preserved by every transition (and byte, 0x80 | N)
  +0x09  i8    slot             party slot, -1 when the slot index was negative (0037C206 / 0037C7B9)
  +0x0A  u8    part counter     zeroed at setup; counts the two passes of states 13-15 (0037BBEA)
  +0x0B  u8    002DEBD0 result  stored at setup (0037C23F / 0037C7F1)
```

### 2.2 Who runs it

| entry | record | how |
|---|---|---|
| `partyallread` `0x3EB` begin `0034CCD0` → `0037C980` | `02EBF3F0` | allocates a `ScheduledTaskRecord` (`002F16B0` → `022BDEC0 + slot × 0x48`, declared 2026-09-18) whose `+0x10` tick callback is **`0037C730`**, start slot `02EBF3FE` = 0, step `02EBF3FD` = +1; then `00233CF0` |
| `partyallread2` `0x46F` begin `0034D8B0` → `0037CA00`; also `summontopartyread` `0x207` result `0034FE80` (`0034FE99`) *(corrected 2026-10-02, OPUS: `0037CA00`'s second caller)* | `02EBF3F0` | the same task, start slot 3, step −1 (`0037CA56`, `0037CA5D`) |
| `summonread` `0x203` result `0034E1F0` → `0037CA80` | `02EBF3F0` | start 0, step +1, and `02EBF3FC` = 0 where the other two set 1; also reached from `0031A300`, `00324380`, `003261D0`, `003273D0` (`PartyConfiguration_SetSelectorsAndReconcileRoster`) |
| the world tick `World_UpdateSimulationTick` `00314020` (`00314291`) → `0037C1A0` | `02EBF3D0` | for each set bit of the slot mask `02EBF3E0`, loads the slot's actor (`PartyRoster_GetActorBySlot`), fills the record, and runs the machine (`0037C28D`); `02EBF3DE` holds a slot in progress across frames |
| `setupbattle` `0x56` end `003523B0` | caller's | calls the machine through the thunk `0037B4C0` (`00352402`) |
| `00359880` | `022C8018` | runs it (`003598CB`) and polls `0037C8D0` (state == 23) |
| `VM_Spawn_ApplySelectedUnit` `005101B0` | caller's | through the thunk (`005101CE`) |

**The verb task** `0037C730` is its own four-step machine on the task's first dword:
1. **1 → 2** fills the record for the current slot: actor, slot, state preserved with only bit 7, part counter 0. It
   clears the actor's byte `+0x23` and calls `002DEBD0` / `002DEB90`.
2. **2** runs the per-actor machine (`0037C811`) and returns until it reports done.
3. **3** adds the step to the slot. `0037CB50` decides whether the walk is finished (slot ≥ 4 going up, < 0 going down).
   *Added 2026-09-19 (FABLE): that same test, through two one-line wrappers, is what the eight party-changing script
   verbs poll - [how a script changes the battle party](how-a-script-changes-the-battle-party.md), section 4.*
   If not, go back to 1. If so, call `00233AA0` (`0030D8B0(1)`, `PartyFocus_SelectAndRequestDefaultActor`,
   `00311E10(0)`, `00311E20`) and go to 4.
4. **4** clears the task pointer `02EBF400`.

### 2.3 The states

The table is `0037C138` (24 entries; bound `cmp eax, 0x17` at `0037B533`). Every transition writes `(state & 0x80) | N`.

**Waiting and continuing.** A transition that ends by jumping to `0037BDB1` goes straight back to the dispatch in the same
call (`0037BDC3` → `0037B55C`). A wait jumps to `0037C0F4` and returns 0.

| state | what the arm does (calls in order) | next |
|---|---|---|
| 0 | hides the actor: `Actor_SetPresentationVisibilityEnabled(actor, 0)` | 1 (`0037B588`) |
| 1 | compares the actor's current definition key (`002E96B0`) with the key its definition now calls for (`0031C250` → `002EB7A0`). When they differ, it releases what the old one loaded: `002E96D0`, `002E3F00`, and `002E3DC0` per part through `0031BEC0` / `002EB7A0`. It sets actor `+0x23` bit 0 and requests the new one (`002EAE20` → `002E9810`, handle to `+4`) | 2 (`0037B70F`); 3 directly when the keys match (`0037B5B0` → `0037B791`) |
| 2 | waits for the requested entry's ready bit (`002E97C0` resolves the handle, `002E4C20` tests `+0x18` bit 1), then writes 3 and applies it in the same arm: `002EBC90`, `ActorHandle_EncodeRegistryEntry`, `0031C540`, `0026D610`, `ActorHandle_GetPrimaryFormulaResourceByte26`, `002E28E0`, `002681D0`, `002E5C70` (with the three floats at actor `+0xB8`), `002EAC90`, `002E49B0`, `002E4A40`, `002E8450` | 3 (`0037B75D`), falling into 3's arm |
| 3 | — (the matched-keys path from 1 re-dispatches here) | 4 (`0037B816`) |
| 4 | swaps the actor's **voice-pack reference**: `0036EC10` decrements the refcount (`+0x16`) on the entry the old key names in the `0x18`-stride pools at `022D9AB0` / `022D9AE0` (pool picked by `id & 0xF0`, slot by `id & 0xF`), then `0036F0F0` finds-or-evicts an entry for the new key (`+0x14`), bumps its refcount, and returns the entry's packed byte `(+0x02 << 4) \| +0x01`; `002ED910` resolves the key, `00264EC0` reads record byte `+0x12`, `PartyRoster_IsFourSlotIndex` gates the pool choice | 5 (`0037B8A2`); 7 when the lookup is negative (`0037B864` → `0037B86A`) |
| 5 | waits until `0036ECA0` — the entry's state byte `+0x00` — returns 3 (loaded) | 6 |
| 6 | — | 7 |
| 7 | element `+0x30` — the **weapon model** (equip slot 0): releases the old entry (`002E3DC0`), requests the new one (`0031BEC0(actor, 0)` → `002EB7A0` → `002EAE20`), stores its handle | 8 when an id was requested (`0037B946`); 9 when there is none (`0037B940` → `0037BC72`) |
| 8 | waits for ready (`002E4C20`), then applies: `002E3110(actor, k=0)` | 9 (`0037B992`) |
| 9 | — | 10 |
| 10, 11, 12 | the same for element `+0x60` — the **off-hand/shield model** (equip slot 1): `002E3110(actor, k=1)` (`0037BAB9`–`0037BABD`) | 11 / 12 (`0037BA3B` → `0037BC7F`), then 13 |
| 13, 14, 15 | the same for elements `+0xC0`/`+0xF0` — the **part-8 pair** (def row `+0x38`/`+0x3C`): `0031BEC0(actor, 8, counter)`, `002E3110(actor, k=3, counter)` (`0037BB9C`–`0037BBA7`), run twice. 15 increments the counter (`+0xA`) and goes back to 13 while it is < 2 (`0037BBEA`–`0037BBF1` → `0037BC99`) | 14 / 15 (`0037BB43` → `0037BC8C`), then 16 |
| 16 | reads the element-0 selector byte `scx+0x12` (`002E9C00` returns it, `-1` on null) and asks `00320170(handle, &out)` — `003202F0` returns the **authored selector**: definition-row byte `+0x13` for a party member, or the equipment-descriptor-derived byte (`weapon word − 0x1000` → equipment row byte `+0x26` → `0x16`-stride table byte `+4`) for an unarmed other. `out` is then used as a **bit index**: `002EB9D0(entryRec, out)` sets bit `out` in the record's request mask `+0x28` and reports the ready mask `+0x2C`. When `out` is valid and differs from `scx+0x12`, it applies it (`002E6BB0(…, 1)`, `002EC6B0` writes `[scx+0x12]`) and re-dispatches the bound record (`002EB490`) | 17 (`0037BCD0`); 18 when `out` is invalid, equal, or the query fails (`0037BC65`, `0037BDCF`) |
| 17 | waits for that entry (`002E4C30`) | 18 |
| 18 | re-encodes the handle and reads the formula resource byte again (`002EAC90`, `ActorHandle_GetPrimaryFormulaResourceByte26`, `002E8450`, `002699D0`) | 19 (`0037BD11`) |
| 19 | computes the **body model** for element `+0x90`: `0037CB90(key, 002657E0(actor), 00263FC0(actor))` — the `highmodelreplace.bin` story-progress swap on the unit's own id (`0031C250` → `word[stats+4]` → `002EB7A0`) | 20 with a request stored in `+4` (`0037BEB6`, `0037BEA8`); 22 when the id is negative (`0037BDA3` → `0037BDAD`) |
| 20 | waits for ready, applies `002E3110` (k=4 — the `+0x90` flag-set op), `002EAC90` | 21 |
| 21 | — | 22 |
| 22 | places and activates: `00377A90`, `0031BAC0`, `Actor_GetWorldPosition`, `Actor_SetFacingHeading_Variant1`, `Actor_SetDesiredMovementHeading`, `002E4A40`, `002E8060`, `002EB030`, **`Actor_SetPresentationVisibilityEnabled`** (shown again), `BattleUnit_ActivateAppliedDefinitionRuntime`, `00263560`, `00359B10`, `002DEB90` | 23 (`0037C0EB`) |
| 23 | done: returns 1 (`0037C0EE`) | — |

**The entries it loads live in the 128 × 64-byte table at `0215FDA0`**
([how a script names a thing in the world](../how-a-script-names-a-thing-in-the-world.md)):
- `002E97C0` resolves a handle `(+0x24 << 16 | +0x1A | 0x8000)` to its entry.
- `002E3DC0` finds an entry by the id at `+0x14` on the lists `0215FD58` / `0215FD78`. When the entry's count `+0x1C` is
  not positive and `+0x19 & 3` is clear, it releases the entry (`002EAEB0`).
- `002E4C20` returns `+0x18 & 2`, the ready bit the wait states test.

## 3. Key addresses

| address | role |
|---|---|
| `0037B4D0` | the per-actor machine; thunk `0037B4C0` |
| `0037C138` | its jump table |
| `0037C730` | the verb task callback (walks slots) |
| `0037C980` / `0037CA00` / `0037CA80` | task installers for `partyallread` / `partyallread2` / `summonread` and the reconcile callers |
| `0037CB50` | the slot walk's end test |
| `0037C1A0` | the world-tick entry over the slot mask |
| `0037C8D0` | `state == 23` |
| `00233AA0` | the task's completion: focus and default actor |
| `02EBF3D0` / `02EBF3F0` | the two static **`PartyReadMachineRecord`** instances (declared 2026-09-18, size `0x18`), the operand record `0037B4D0` runs on. Shared prefix: `+0x00` `boundRowRef` (base-relative authored-row offset, `0020E620`/`0020E600`), `+0x04` `pendingRequestId` (`002E9810` → `002E97C0` → `NameBindingEntry`), `+0x08` `machineState` (`(old & 0x80) | state`, bit 7 sticky), `+0x09` `partySlot` (s8, −1 allowed), `+0x0A` `partCounter`, `+0x0B` `savedFlagByte` (`0215EF4E` snapshot, held at 1 while running, restored at completion via `002DEB90`). Driver tails differ: `02EBF3D0`'s `+0x0C`/`+0x0D`/`+0x0E` are the `0037C2E0` sub-state machine's state/iteration/in-progress bytes and `+0x10` (`02EBF3E0`) is the pending-slot bitmask; `02EBF3F0`'s `+0x0C`/`+0x0D`/`+0x0E` (`02EBF3FC`–`02EBF3FE`) are verb mode, slot step, current slot and `+0x10` (`02EBF400`) is the `ScheduledTaskRecord*` |

## 4. Modding notes

- A party member that stays invisible after a read-in verb is stuck in a wait state (2, 5, 8, 11, 14, 17 or 20). Byte
  `+8` of `02EBF3F0` names which one.
- Changing a party member's definition is not enough by itself. The machine is what brings the loaded parts in line, and
  it runs only from the entries in §2.2.
- For a multiplayer mirror, the machine is script-driven when entered from the verbs, so per this repository's rule it
  must run on every client and must not be suppressed.

## 7. What is not known

- [x] ~~**UQ-49.** What the four part slots are (`002E3110(actor, k)`, k = 0, 1, 4, 5).~~ **Answered
      2026-09-16 (SWE2-STRUCT):** the "parts" are **element slots of the unit's SecondaryContext** (`actor+0xC0`),
      and each binds a **model resource** — equipment-derived or definition-authored, never texture or motion.
      - *The element map.* SecondaryContext is a **`0x30`-stride element array, six deep** at `+0x00`–`+0xF0` —
        two elements beyond the previously proven four (`002E96D0` / `002E3110` compute `scx + (sub+4)*0x30` →
        `+0xC0`/`+0xF0`; `002EBC90` computes `scx + sel*0x30` for sel ∈ {4,5} → the same two). Each element carries
        `entryId` (`+0x00`, −1 sentinel / low word = index into the `0x740` record pool ~~at `022C6F28`~~ whose base pointer is held at `022C6F28` *(corrected 2026-10-02, OPUS: `003EC3F0 add rbx, qword ptr [022C6F28]`)*), the bound
        resource id (`+0x04`, returned by `002E96D0`), a record pointer (`+0x08`), visibility nibble (`+0x10`
        high bits, written by `002EBC90`) and the selector byte (`+0x12`, element 0's written by `002EC6B0`).
      - *The k-enum is one enum, not "four slots".* `002E96D0`/`002E3110` share it: **k=0 → el `+0x30`, k=1 →
        el `+0x60`, k=2 → el `+0x90` (flag-clear op), k=3 → el `+0xC0`/`+0xF0` by the record's `+0xA` counter,
        k=4 → el `+0x90` again but the flag-SET op** (`rec+0x304 | 0x40`, `rec+0x640 = 0`, `rec+0x290 | 0x2000`,
        gated on byte `01FD49EC == 0` at `002E3187`). `002EBC90`'s selector is the same space renumbered:
        sel 2→`+0x30`, 1→`+0x60`, 3→`+0x90`, 4/5→`+0xC0`/`+0xF0`, else→`+0x00`.
      - *What each element binds.* `0031BEC0(actor, part, sub)` supplies the desired id per arm — part **0** →
        `word[src+0x50]`, part **1** → `word[src+0x52]` (the five-word **equipment array**: party reads the
        definition row's `+0x50` via `0031C0F0`, others fall back to the stats record's `+0x50`; the word is
        validated as a class-6 equipment id by `0031BF60` and resolved to the row's **`+0x30` dword = the model
        resource id**), part **8** → `dword[defRow + 0x38 + sub*4]` (two authored dwords, `+0x38`/`+0x3C`,
        `sub` = record `+0xA`). `0031BE30` reads the same parts' second form via def bytes `+0x40`/`+0x41`.
      - *So per element:* el `+0x30` = **weapon model** (equip slot 0), el `+0x60` = **off-hand/shield model**
        (equip slot 1), el `+0x90` = the **body model** (unit id from `0031C250`, `word[stats+4]`, story-swapped
        by `0037CB90`), els `+0xC0`/`+0xF0` = the **part-8 pair** (def `+0x38`/`+0x3C`), el `+0x00` = the unit's
        own record. `002EB7A0` remaps special ids before the request: `0`/`1` → `0x630000`, `8`/`9` → `0x6E0001`,
        `12`/`13` → `0x770002` (the empty-slot resources), others pass through.
- [x] ~~**UQ-50.** What `0036EC10` / `0036ECA0` / `0036F0F0` resolve and wait for (state 4–5), and what `0037CB90` computes in state 19.~~
      **Answered 2026-09-16 (SWE2-STRUCT):** a **refcounted voice/resource pack swap**. The pools are two
      `0x18`-stride entry tables at **`022D9AB0` (2 slots) and `022D9AE0` (4 slots)** — *the bases are these VAs;
      the registry's earlier `021B9AB0`/`021B9AE0` citations were the raw displacement before the `0x120000`
      image-base add in the lea chain*. Entry: `+0x00` u8 load-state, `+0x01`/`+0x02` u8 packed-id nibbles,
      `+0x0C`/`+0x10` u32 handles released by `00369800` on eviction, `+0x14` u16 key, `+0x16` u16 refcount.
      `0036EC10(id)` decrements `+0x16` (pool = `id & 0xF0`, slot = `id & 0xF`); `0036F0F0(key, which)` finds the
      entry by `+0x14` or evicts the first refcount-0 one and starts the load (`0036ED50` → `0032E400` family
      `0x21` lookup, `0036C1D0`/`0036B160`/`0036C140`/`0036A0B0` — the `0x36xxxx` audio cluster); `0036ECA0`
      returns `+0x00`, and state 5 waits for **3 = loaded**. `0037CB90` is already answered: the
      `highmodelreplace.bin` story-progress swap (22 records, `(a,b,c)` keys) — it supplies el `+0x90`'s
      replacement body-model id in state 19.
- [x] ~~**UQ-51.** What `00320170` answers in state 16, and what definition byte `+0x12` selects.~~
      **Answered 2026-09-16 (SWE2-STRUCT):** `00320170(slot, &out)` → `003202F0(statsRec, &out)` returns the
      member's **authored sub-model selector** — for a party-kind stats record (`byte[+5] == 1`) it is the
      definition row's byte **`+0x13`** (`[actor+0xE60]`, via `0031B860` stats→actor); for others with empty
      weapon slots (`word+0x50 == 0x1000`, `word+0x52 == 0xFFFF`, flag `+0x69`/`+0x79` bit 1) it is a
      `0x16`-stride table byte; otherwise `003203B0` derives it from the weapon's equipment row (`word − 0x1000`
      → row → byte `+0x26` → second `0x16` table → byte `+4`). State 16 compares it to element 0's current
      `scx+0x12` (`002E9C00`) — note the doc's `WorldActor_GetDefinitionByte12OrMinus1` is that runtime byte,
      **not** a definition read — and uses `out` as a bit index into the bound record's request mask
      (`002EB9D0` sets bit `out` of `+0x28`, checks `+0x2C`). So `+0x12` = the element's **active variant
      selector**, `+0x13` on the definition row = the **authored selector** it is synced to.
- [x] ~~**UQ-52.** Which records `003523B0` and `005101B0` pass, and what the list at `022C8018` is (`00359880`).~~
      **Answered 2026-09-16 (SWE2-STRUCT):** both are **verb task steps** — `003523B0` is `setupbattle` `0x56`'s
      step and `005101B0` is `VM_Spawn_ApplySelectedUnit` `0x3001`'s step; each sits third in a vtable triple
      (`01EEE1C0` = `{00351C00, 00351F40, 003523B0}`, `01F281D0` = `{00510440, 00510160, 005101B0}`) and receives
      **the task's own record**, which embeds a `0037B4D0` machine block at `+0x00`–`+0x0B` plus a task phase
      byte at `+0x0C` and its param at `+0x0D` (`00351F40` writes them at init). `003523B0` runs a 3-phase
      lifecycle on that record — `+0xC` 1→2 inits the machine (`0037CE80` fills `+0x00` resolved id, `+0x08`
      state 0, `+0x09` param, `+0x0A` counter 0, `+0x0B` = `002DEBD0`), 2→3 runs it to state 23, 3 cleans up
      (`002681C0`) — while `005101B0` runs a single step and reports `!done`. And `022C8018` **is one such
      machine record embedded in the `00359800`/`00359880` driver** — `0037B4C0` is the `0037B4D0` thunk,
      `0037C8D0` polls `+0x08 & 0x7F == 0x17`. `022C8010` is the driver's own phase word (1–5: `00359A30` /
      init / `0037CB40` gate / the `00359880` loop), ~~and the "list" is the cursor `022C8024` + count `022C8028`
      pair beside it.~~ *Corrected 2026-09-25 (FABLE, Claude Opus 5.5), on OPUS block 279:* `022C8024` / `022C8028` are **the machine record's own driver-private tail**,
      `+0x0C` and `+0x10` of `022C8018`, not a separate list. `+0x0C` is the driver's step: 0 picks the next member,
      1 runs the machine until `0037C8D0` reports state 23, and 2 is done (`003598B0`–`003598F8`). `+0x10` is the
      member index: it is compared with the member count that the driver reads once on entry, and incremented per member (`003598ED`–`00359902`). This is the same
      tail pattern as the `02EBF3D0` / `02EBF3F0` instances.
- [x] ~~**UQ-53.** Who sets bits of the slot mask `02EBF3E0`.~~ **Answered 2026-09-14 (FABLE):** the verb `partystdmotionrecover` `0x14C`, and it sets all four bits at once. RIP census of the dword, seven references:
      - **The one setter.** `0037CFD0` (23 B) writes `0xF` when the mask is 0 and leaves it unchanged otherwise. Its one caller is the verb's begin entry (verb table row `0x14C`), which calls `003601B0(0x12)` and tail-jumps into it (`00342CA2`). So a recover request marks all four party slots; a request made while slots are still pending adds none.
      - **Per-slot clears.** The world-tick entry `0037C1A0`, reached from `World_UpdateSimulationTick` (`00314291`), handles flagged slots 0–3 **one at a time**.
        - For a flagged slot with no machine in progress (`02EBF3DE` = 0), it binds the record to `PartyRoster_GetActorBySlot(slot)`.
        - If the slot has no actor (`0037C266`), or `002EA6A0` refuses it (`0037C27D`), the bit is cleared without running the machine.
        - Otherwise it sets `02EBF3DE` = 1 and runs the machine. If the machine returns 0, the tick returns and resumes that slot next frame. If it returns 1, the in-progress byte and the slot's bit are cleared (`0037C296`–`0037C2A9`), and the walk goes on to the next slot.
      - **Whole clear.** `0037CB10` zeroes the mask and byte `02EBF3DE`. It is reached once, from the boot-subtree call site `00266E29`.
      No other RIP-relative write exists. Writes through a pointer into `02EBF3D0`–`02EBF3FF` were not excluded.

## 8. Evidence

| claim | evidence | tier |
|---|---|---|
| 24 states, table `0037C138` | `0037B533` bound, `0037B572` dispatch; [`members/party_read_states.py`](members/party_read_states.py) | 1 |
| every transition and its site | [`members/party-read-states.tsv`](members/party-read-states.tsv); fall-back jumps `0037B940`, `0037BA3B`, `0037BB43`, `0037BBF1`, `0037BC30` / `0037BC3B` | 1 |
| state 23 = done, returns 1 | `0037C0EE` `mov r12d, 1`; `0037C8D0` tests `== 0x17` | 1 |
| verb entries | [the verb table](../Verb-Dispatch/scriptvm-verb-table.tsv) rows `03EB`, `046F`, `0203`; `0034CCE2`, `0034D8C2`, `0034E20C` | 1 |
| task slot walk | `0037C730`–`0037C850`, `0037CB50` | 1 |
| world-tick entry | `00314291` → `0037C1A0`; `0037C28D` | 1 |
| entry table accessors | `002E97C0`, `002E3DC0`, `002E4C20` bodies | 1 |

## 9. Falsification pass 2026-09-14 — SWE2-AUDIT-SEM

**Program state:** shipping EXE `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
**Attack chosen:** decode the whole `0037C138` jump table from the image and compare all 24 entries
against `members/party-read-states.tsv`, then re-read the machine head, the state-23 terminal, the
thunk and every entry callsite, the three verb installers' parameter bytes, the world-tick entry,
the record fills, the slot-walk end test, and the three entry-table accessor bodies.

### SURVIVED — every attacked claim

- All **24** table entries decode exactly to the TSV's arm addresses; bound `cmp eax,0x17` at
  `0037B533`, dispatch `0037B572`, redispatch `0037BDB1` → `0037B55C`, wait return `0037C0F4`.
- Null actor → return 1 (`0037B501`); state 23 → `mov r12d,1`; `0037C8D0` = `[rcx+8]&0x7f == 0x17`.
- Verb rows `03EB`/`046F`/`0203` → `0034CCD0`/`0034D8B0`/`0034E1F0` → installers `0037C980`/
  `0037CA00`/`0037CA80`; mode `02EBF3FC` = 1/1/**0**, slot 0/3/0, step +1/−1/+1 — all byte-exact;
  shared poll `0034E3E0`. Reconcile callers `0031A300`/`00324380`/`003261D0`/`003273D0` each call
  `0037CA80` once.
- World tick `00314291` → `0037C1A0`; mask `02EBF3E0`, in-progress `02EBF3DE`, machine run
  `0037C28D` → `0037B4D0`. Record `+9` = −1 on negative slot (`cmovs` `0037C206`/`0037C7B9`),
  `+0xA` counter `inc;cmp 2` at `0037BBEA`, `+0xB` = `002DEBD0` result at `0037C7F1`/`0037C23F`.
- `0037CB50` end test, thunk `0037B4C0`, callsites `00352402`/`005101CE`/`003598CB`, and the
  `002E97C0`/`002E3DC0`/`002E4C20` accessors — all exact.

### Result

Zero defects found. Full attack record:
`Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-two-unattacked-tier1.md`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Items_Equipment_Shops_License — SERVICE and CLIENT.**
  - `BattleStats_ClearAllEquipmentSlotsByMappedId` (`0031A300`) clears through `BattleStats_SetEquipmentSlotByMappedId`,
    and it is also run by `InventoryEquipment_SnapshotAndClearTemporary…`.
  - The id-validity query is shared with thirteen licence, equipment and class-D functions (MECHANICAL).
- **Audio, Input and Party — SERVICE, through the world tick.** `World_UpdateSimulationTick` (`00314020`) calls the
  1,036-byte positional Audio body, a 9-byte audio leg, the 1,002-byte Input body and an 83-byte Input helper.
  So the world tick also updates positional sound and input state.
- **Audio — CLIENT.** `002F16B0` is also read by three Audio-filed bodies (120–309 B).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** `World_UpdateSimulationTick`, which runs the slot-mask entry, is called by `MainLoop_UpdateAndRenderFrame` and by two other core frame bodies (463 and 2,001 bytes). A small entry this page cites is called by the main loop and the 463-byte body too. The core main loop drives this machine; it owns nothing of it.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleEnmity_AnyAboveThreshold`, owned by that layer, calls `00322C50` on this page. That caller is the threshold scan over the same enmity bytes at `[+0x6A0] + 0x19`, id by id; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_RebuildEffectiveStatsAndAffinityState`, owned by that layer, calls `00322C50` on this page. That caller is the effective-stats re-form, and it says where its output lives: with no explicit destination it writes the record's **own `+0x24` block, `0x24` bytes wide**, and the block at `+0x50`, taking its mode from the flag word at `+0x3C`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — CLIENT (51 edges through 17 of this page's functions).** The Movement layer reaches this page at `0037B4D0`, `002E28E0`, `002E4A40`, `00314020` and 13 more. `FUN_002681d0` is the worked example, read in full - it is a 10-byte null guard that returns at once on a null argument and otherwise tail-jumps to the routine that follows it; **3 of the 44 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — SERVICE.** `0034E1F0` on this page calls `FUN_00313550`, owned by that layer. What it reaches is a 58-byte setter for **bit 0 of the same `dword[[02EBF190] + 0x5B04]` the mode ladder reads**: it writes only when the bit differs from what it is asked for, and then tail-jumps into the notify; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

> **Dispositioned 2026-09-14 (OPUS).** Pass 22 reports a neighbouring subsystem this
> page never mentions. These are shared entry points — the relationship is that this
> page's code asks a common question, not that the two subsystems interact here. Each
> was read from the shipping bytes; the reading is in
> [`the shared neighbours pass 22 keeps finding`](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md).

| this page cites | which calls | owned by | and that is |
|---|---|---|---|
| `0031BAC0` | `00322C50` | **Gameplay** | `BattleEncodedId_IsValidForClass`, the shared *is this encoded id valid for this class* query — a 32-entry jump table on the class |
| `0031C250` | `00322C50` | **Gameplay** | `BattleEncodedId_IsValidForClass`, the shared *is this encoded id valid for this class* query — a 32-entry jump table on the class |

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Rewards_Progression_Economy — CLIENT.** `Reward_ComputeExperienceForRecipient` (`002F8BB0`),
owned by that layer, calls **`BattleStats_FindOwningBattleUnit`** (`0031B860`) on this page at
**`002F8BDE`**. Read from the shipping bytes: the reward body takes a stats pointer in `rcx`, refuses
a null (`002F8BCF`), tests the kind byte `[rcx+5]` (`002F8BD4`), and only then calls the accessor;
a null result sends it to the refusal path at `002F8D46` (`002F8BE3`–`002F8BE6`). The accessor itself
refuses a null and otherwise walks the unit array (`0031B869`, `0031B87D` → `00236850` for the
count).

**The crossing is that the reward layer consults this page's accessor, not that this page owns
anything in that layer.** It is the same function `EXP-090` measures as its `FIND` gate — *"resolves
stats → unit via the `[0208E6A0]` count scan of `[0208E688] + i*0xF50` on `unit+0x698`"* — so the
edge is the reward gate chain reaching in, and it is documented from the other end in
[`CONTRACT-experience-and-licence-award.md`](../../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md) §14.

**ActorEntity — SERVICE (SWE2-EC7, batch 159).** `00320170`'s resolution machinery is the actor layer's own: `003588B0` resolves the slot record, `00263750` the slot accessor, `00263E30` the record unwrap, and `00233AA0`/`00233CF0`/`00237650` carry the same family to ActorEntity callers `0025D9E0`/`0026CE60`/`003266C0` — the machine asks the actor layer for the record; it owns nothing there.

**Combat, CombatAction — CLIENT (SWE2-EC7, batch 159).** `00263E30` is also read by `003206E0` (Combat) and by `00317E60`/`00319090`/`003191B0`/`00319Fxx` (CombatAction) — shared accessor consultation, not a machine consumer.

**Status_Periodic_Terminal — CLIENT (SWE2-EC7, batch 159).** `00263E30` is also read by `00386860`, `002E8060` by `00301140`, and `0031B860` by `002F9400` on that layer — the status/periodic side consults the same accessors this page documents.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Resource — SERVICE and MECHANICAL (10 edges).** The pool-slot loader `0036ED50` calls `0032E400` and `0032E620`; `0032E400` is also called by `00249210`, `0024AC30`, the boot worker spawn `00259DF0`, `00379E90`, `00384420`, `0039C3F0`, `003EADE0` and `0051ED10`. `0032E400` (read) looks up a per-kind dword table by kind and index (-1 for kind `0xFF`) and rounds a positive answer up to a multiple of 64; the machine's pool-entry load (the one state 5 waits on) reaches it through `0036ED50` as the family `0x21` lookup, and the eight other callers are the resource layer's ordinary users of the same table.

**Save_Load_Settings — OUT-OF-SCOPE (2 edges).** `ActorManager_RunFieldRuntimePass` `0025D9E0` calls `SaveWrite_GetBusyFlag` `00583920` and `SaveImage_GetPersistentPayloadBase` `002EF2B0`. The field runtime pass branches on the save-write busy flag at its entry and reads two persistent-payload bytes (`+0x1063` bit 6 and `+0x1534`) to choose a field id; this page cites `0025D9E0` only as a caller of the `00233AA0` toggle, and those save reads are not part of the read-in machine.

**Spawn_Encounter_Lifecycle — CLIENT and SERVICE (25 edges).** `VM_Spawn_ApplySelectedUnit` `00510160`, the middle entry of the verb triple UQ-52 lists, calls `Spawn_ApplyScriptSelectedUnit` `0023A3B0`; and 24 spawn bodies call the unit resolver `ActorWork_GetBattleUnit` `0031B760`, among them `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0`, `Spawn_SelectAndPrepareAutomaticEntry` `00235720`, `SpawnEntry_GetScriptSelection` `00236140`, `SpawnUnit_BindEntryAndMarkCapTracked` `00239840` and `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410`. The verb body (read) pops a unit index, applies it through the spawn layer, and only when the bit-2 probe `00237650` then reports an applied definition does it initialise an actor operation on the event context (`VMEventContext_InitializeActorOperation`); the spawn code resolves units through the same resolver the bit-2 probe `00237650` uses.

## SWE2-EC7-69 update (2026-09-19) - `002F16B0` ScheduledTaskRecord alloc measured

`002F16B0` (95 B) measured - **the page's allocation claim is exact**: it
finds the first clear bit in the allocation mask `dword[022BE7C0]` (≤ `0x20`
slots; none free returns NULL), sets the bit, and initializes the record at
`022BDEC0 + slot*0x48` - three qwords zeroed, `+0x18 = slot`, `+0x1C = 1`,
`byte[+0x20] = 1`, `+0x28 = 0` - returning the record pointer the caller
fills with the tick callback.
Interior anchor `002F16DE` (the `022BE7C0` mask store).

## SWE2-EC7-92 update (2026-09-20) - `0037CE80` + `0037C8D0` measured

`0037CE80` (123 B) is the presentation-record init `003523B0` calls:
`002E97B0` resolves the target and clears its `+0x11` bit 0,
`0020E620` builds the id (`r8d` negative -> -1) into `[rbx]`, bytes
`+8`/`+9`/`+0xA`/`+0xB` come from the `002DEBD0`/`002DEB90` pair
under the `0016D6A0` gate, `[rdi+0x23]` is cleared, and `+8` gains
`0x80`.
Interior anchor `0037CEB4` (the `0020E620` call).

`0037C8D0` (32 B) is the paired predicate: a null record answers 1,
otherwise the answer is whether `([rcx+8] & 0x7F) == 0x17`.
Interior anchor `0037C8E9` (the `cmp cl, 0x17`).

## SWE2-EC7-97 update (2026-09-20) - `002EBD60` + `002EB490` measured

`002EBD60` (79 B) is the two-list keyed find `0037B4D0` and
`003EC630` call: the `0215FD58` chain is walked for `[+0x14] ==
ecx`, then the `0215FD78` chain the same way; a hit rewrites
`byte[+0x19]` bit 0 from `dl & 1` - the find-and-flag the
read-in state machine uses to mark a member.
Interior anchor `002EBD90` (the second chain's key compare).

`002EB490` (12 B) is the fixed-flags shim `0037B4D0` and
`0050D660` call: `r8d = 1, r9d = 0` and a tail `jmp 002EB5E0` -
the (1,0)-specialization of the shared helper.
Interior anchor `002EB493` (the `r8d` arm before the jump).

## SWE2-EC7-107 update (2026-09-20) - `00237650` measured

`00237650` (32 B) is the bit-2
probe `00510160` and `005101B0`
call: `0031B760()` resolves the
record - null answers 0, live
answers `(dword[rax] >> 2) & 1` -
the single-flag fetch the read-in
state machine consults.
Interior anchor `00237665` (the
`shr eax, 2`).

## SWE2-EC7-108 update (2026-09-20) - `00233AA0` measured

`00233AA0` (41 B) is the ordered
four-call toggle `0025D9E0` and
`0037C730` run: `0030D8B0(1)`,
`00326500()`, `00311E10(0)`,
`00311E20()` in fixed sequence,
then return 1 - the paired
assert/release the read-in arms
share.
Interior anchor `00233AA9` (the
`0030D8B0(1)` call).

`00320170` (179 B) is the selector resolver `0037B4D0` consults at state 16 (the UQ-51 question above): with `02089340` bit `0x10` armed, `003588B0` resolves the reference record `rdi` and slots `0..3` are scanned via `00263750` for its match - a hit `00320230`-resolves that slot's record directly; a miss falls back to `003588B0(ecx)` -> `00263E30` -> `[rax+0x698]` and dispatches through `003202F0` - the authored-selector lookup feeding `002EB9D0`'s bit-index write

Interior anchor `003201B0` (function `00320170`).

`002E96D0` (147 B) is the mode-indexed element resource-id read `0037B4D0` state 1 uses (the page's `scx + (sub+4)*0x30` note): `edx` selects over `[rcx+0xC0]`'s SecondaryContext - modes 0/1/2 return `dword[+0x30/+0x60/+0x90 + 4]` respectively, mode 3 walks `(r8 + 4) * 0x30` into the element span, and everything outside the table returns 0 - the part-N resource id the machine compares against the definition key.

Interior anchor `002E975B` (function `002E96D0`).
