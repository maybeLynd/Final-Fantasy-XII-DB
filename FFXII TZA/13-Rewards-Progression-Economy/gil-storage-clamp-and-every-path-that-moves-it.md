---
system: Gil — storage, clamp, and every path that moves it
category: 13-Rewards-Progression-Economy
status: AUDITED
owner_layer: PrimaryOwner:Rewards_Progression_Economy
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 00247AE0, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-gil-pass-1 - both caller censuses reproduce set for set (13, and 19+3 with zero overlap); SETTLED: 00316A50 reads cl, never ecx, rejects kinds >= 30 and indexes a 30-entry table at 00D10460, so section 3's caveat is resolved; both wrappers add behaviour and 003004B0's pre-floor changes what the meter records; 003F4AA0 is a record applier; and a pointer census bounds the direct-write question - 02092758 has 10 rip-relative references in 9 functions and only SetGil writes +0x08, while +0x0C, the walked-distance total, carries gil's exact ceiling
  crossref_clean: false
  reopened_count: 0
---

# Gil — storage, clamp, and every path that moves it

> Gil is a single signed 32-bit field, clamped to `[0, 99,999,999]` on every write, and **every
> change in the game passes through one setter** — which is why the same function serves a chest, a
> shop, a Quickening's cost and a debug menu row.

**Closes `N-7`** ("Gil award path — `GameState_Get/SetGil` decompiled but unread").

## 1. What the player sees

A number that goes up from chests, loot sales and defeated enemies, and down at shops. It stops at
**99,999,999** and never goes below zero. It is also, less visibly, **spent to perform certain
actions in battle** (§5) — and refunded if the action does not happen.

## 2. Storage

```c
gil = *(int32*)(*(void**)0x02092758 + 8);
```

`GameState_GetGil` (`00253690`) is three instructions and does exactly that. The game-state object at
`[02092758]` holds gil as a **signed 32-bit field at `+8`**.

## 3. The setter is where all the behaviour lives

`GameState_SetGil(int newValue)` (`00254EE0`), complete:

```c
delta = newValue - state->gil;
if      (delta > 0)  FUN_00316A50(/*cl=*/6, delta);    // recorded as gained
else if (delta < 0)  FUN_00316A50(/*cl=*/7, -delta);   // recorded as spent
v = (newValue < 0) ? 0 : newValue;                      // floor
if (v > 0x05F5E0FF) v = 0x05F5E0FF;                     // 99,999,999 ceiling
state->gil = v;
```

Three things follow, and none of them is visible from the caller side:

- **The clamp is in the setter, not in the callers.** Every path in §4 inherits `[0, 99,999,999]` for
  free, and **a caller that computes a negative balance silently gets zero** rather than failing.
- **Every change is metered.** `00316A50` (owner: `PlatformOnlineAchievements`) is called with kind
  **6 for gained** and **7 for spent**, by *absolute* delta. Gil movement feeds statistics and
  achievement bookkeeping **as a side effect of the setter** — so any write, from any source,
  is counted.
- **The delta is measured before the clamp.** A write of 200,000,000 records a "gained" delta far
  larger than the gil actually stored. **The meter and the balance can disagree**, by construction.

> A **caveat on the kind argument** — ~~unresolved~~ **settled 2026-09-13 (OPUS): it reads `cl`.**
> `mov cl, 6` sets only the low byte of `ecx`, which at that point still holds `newValue`, so the
> callee receives `(newValue & 0xFFFFFF00) | 6`. `00316A50`'s first instruction is `cmp cl, 0x1E`
> and it then zero-extends `cl` twice (`movzx esi, cl`, `movzx ebp, cl`) into its table index. **The
> upper three bytes are never read. The idiom is correct, not a defect** — §13.

## 4. Every path that moves gil

`GameState_SetGil` has **13 direct callers and no thunks**, across 5 owner subsystems. That is a
complete census of how gil changes:

| Caller | Owner | What it is |
|---|---|---|
| `00312280` `BattleUnit_ProcessDefeatRewardsAndLoot` | Rewards | **the award path** — gil from defeating a unit |
| `002FEEB0` `Shop_CommitPurchaseItemAndGil` | Items/Shops | buying |
| `00310870` `Shop_CommitSaleItemAndGil` | Items/Shops | selling |
| `002FD530` `InventoryBundleClass09_ApplyGilAndNestedItems` | Items/Shops | a container granting gil **and** items together |
| `002FD880` `InventoryEncodedGilClass0E_ApplyGilDelta` | Items/Shops | a gil-carrying inventory object |
| `0030EF20` `BattleAction_PrepareExecutionResources` | CombatAction | **spends gil to start an action** (§5) |
| `00305640` `BattleAction_ConsumeExecutionResources` | CombatAction | commits the spend |
| `00300280` `BattleAction_RefundReservedExecutionResources` | CombatAction | gives it back |
| `003112F0` `BattleFormula_ApplyTargetResult` | CombatFormula | gil changed by an action's result on a target |
| `003004B0` `GameState_AddGilClampedAndNotify` | Rewards | a relative-add wrapper |
| `00300500` `GameState_SetGilClampedNonnegative` | Rewards | an absolute-set wrapper |
| `003F4AA0` | Rewards | reward-bundle record applier (§13a); sole feeder `00290130`, ~~statically orphaned~~ **reached from script verb `037C questresultwindow` through the thunk `002E1A50`** (`CON-174`) |
| `003058B0` `Debug_SetGilToMaximum` | — | the developer console's gil row |

`GameState_GetGil` has **22 callers over the same 5 owners**, so gil is read in about half again as
many places as it is written.

> **CORRECTED 2026-09-03 — this said 19.** `GameState_GetGil` is one of the **57 names in this image
> carried by two functions**: the body `00253690` and a five-byte thunk `00309BF0`. The census counted
> the body's **19** direct callers; **three further functions reach it only through the thunk**
> (`0032A850`, `00388D50`, `0038F6F0`), with **zero overlap**. The true figure is **22**, and
> `CombatFormula` rises from 1 caller to 3.
>
> **The undercount is invisible from the call site and from the number** — 19 is a plausible,
> well-formed answer. It was found by reviewing every caller-count claim in this database that names
> an ambiguous function, which is the enumerable version of the hazard measured in
> [`duplicated-function-names-and-how-to-resolve-them.md`](../00-Engine-Core-Runtime/duplicated-function-names-and-how-to-resolve-them.md):
> **30 of 53 bodies have zero direct callers, and this one had 19, which is why it did not look wrong.**

> **There is no gil cheat in the console.** `Debug_SetGilToMaximum` is **one of thirteen** callers of
> the ordinary setter — which is why it moves the same statistics counters a player's gil would. That
> is the same finding the console block reached from the other end; it is recorded there and is not
> re-derived here.

## 5. Gil is an execution resource — confirming `AI-8`'s flagged inference

`AI-8` lists three execution-resource pools — `raw[0x4C]` (int16), `raw[0x4E]` (byte), and a global
pool via `FUN_00253690` with ~~per-unit fallback~~ `unit[0xE58]` *(corrected 2026-10-02, OPUS: `+0xE58` is the gil cost reserved for the action in progress, not a purse: `0030EFC0` stores `00309060`'s result there, the refund `00300280` adds it back and the consume path `00305640` clears it; 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:234; using-an-item-is-an-action-that-costs-an-item.md, "The action gil cost: 00309060")* — and records **gil as a flagged
inference for the third**. The inference is correct, and here is the evidence:

```asm
0030EFBB  call 0x309060                 ; cost = f(unit, actionId)
0030EFC0  mov  [rbx + 0xE58], eax       ; remember the reservation
0030EFC8  test eax, eax
0030EFCA  je   0x30EFDD                 ; zero cost -> nothing to do
0030EFCC  call 0x253690                 ; GetGil
0030EFD1  sub  eax, esi                 ; balance - cost
0030EFD3  cmovns edi, eax               ; keep it only if non-negative
0030EFD8  call 0x254EE0                 ; SetGil
```

So `BattleAction_PrepareExecutionResources` **reads gil through `00253690`, subtracts the action's
cost, and writes the result back** — with the reserved amount stored at `unit + 0xE58`, exactly the
~~per-unit fallback~~ field `AI-8` names *(corrected 2026-10-02, OPUS: a reservation, not a fallback pool; `+0xE58` is the gil cost reserved for the action in progress, not a purse: `0030EFC0` stores `00309060`'s result there, the refund `00300280` adds it back and the consume path `00305640` clears it; 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:234; using-an-item-is-an-action-that-costs-an-item.md, "The action gil cost: 00309060")*. `00305640` commits and `00300280` refunds against the same
field.

**This confirms a flagged inference; it does not discover it.** `AI-8` remains the owner of the
question, and the two other pools (`raw[0x4C]`, `raw[0x4E]`) are untouched here.

## 6. Key addresses

| Address | Name | Body | Role |
|---|---|---|---|
| `00253690` | `GameState_GetGil` | 11 B | reads `[02092758] + 8` |
| `00254EE0` | `GameState_SetGil` | 72 B | meters, clamps, stores |
| `003004B0` | `GameState_AddGilClampedAndNotify` | — | relative-add wrapper |
| `00300500` | `GameState_SetGilClampedNonnegative` | — | absolute-set wrapper |
| `0030EF20` | `BattleAction_PrepareExecutionResources` | — | the gil spend (§5) |
| `02092758` | — | — | game-state object pointer; gil at `+8` |

`00316A50` is named only by role in §3 — it is a 411-byte function owned by
`PlatformOnlineAchievements` with callers well beyond gil, and **this document has not accounted for
its reach**, so it is described rather than cited as an authority.

## 7. Data structures and formulas

```
[02092758] -> game state
    +0x08   int32   gil,  always in [0, 99999999] after any SetGil

unit + 0xE58   int32   gil reserved for the in-flight action (§5)

SetGil(v):
    meter(v > gil ? GAINED : SPENT, |v - gil|)      // before clamping
    gil = min(max(v, 0), 99999999)
```

## 8. Call chain

```
defeat  -> BattleUnit_ProcessDefeatRewardsAndLoot (00312280) --+
shop    -> Shop_CommitPurchase / CommitSale                    |
chest   -> InventoryBundleClass09 / EncodedGilClass0E          +-> GameState_SetGil (00254EE0)
battle  -> Prepare / Consume / Refund ExecutionResources       |      -> 00316A50 (metering)
result  -> BattleFormula_ApplyTargetResult                     |      -> clamp -> [02092758]+8
console -> Debug_SetGilToMaximum ------------------------------+
```

## 9. Modding notes

**Write gil through `GameState_SetGil`, not to `[02092758] + 8` directly.** A direct write skips both
the clamp and the metering — the balance will be whatever you wrote, including values the game cannot
otherwise reach, and the gained/spent statistics will not move.

**The ceiling is a constant in the setter** (`0x05F5E0FF`), not a data-table value.

**An action's gil cost is reserved, not spent immediately** (§5). Editing `unit + 0xE58` between
prepare and consume changes what is refunded.

## 10. What is not known

- ~~**and whether it reads `cl` or `ecx`**~~ — **`cl`, settled §13.** ~~Still open:~~ *(answered: see CONTRACT-gil-storage-and-movement.md GL-2 and §14 — kind 6 adds to the saturating gained dword `[020927C0] + 0x3860`, kind 7 to the spent dword `+0x3864`, and they feed counter ids 8 / `0xA`; 2026-10-02, OPUS)* **what `00316A50`
  does with kinds 6 and 7** beyond rejecting kinds ≥ 30 and indexing its 30-entry table.
- ~~**How the award amount is computed** — `BattleUnit_ProcessDefeatRewardsAndLoot` is named as the~~
  ~~award caller but its computation is not read here. It is the natural next step and belongs beside~~
  ~~[`loot-drops-and-enemy-chain.md`](loot-drops-and-enemy-chain.md).~~ *(answered: see CONTRACT-defeat-rewards-sequence.md DR-4 and what-happens-when-an-enemy-dies.md — gil = (defeated level − baseline) × `[+0xE78] + 0x30` + `[+0xE70] + 0x30`, plus the effect-12 conversion, `0031251D`–`00312546`; 2026-10-02, OPUS)*
- ~~**`003F4AA0`**, the one unnamed caller.~~ **Read §13a (2026-09-22, SWE2-CONTRACT)**: a
  reward-bundle record applier — when bit 0 of `[rcx]` is set it does
  `SetGil(GetGil() + [rcx+4])`, then grants `[rcx+8]` counted items (stride-4 entries at
  `+0x0C`) and `[rcx+0xA]` single items (stride-2 at `+0x1C`) through `00300B80`. The record
  is a fetched bundle — sole caller `00290130` populates it via `003F8C60`→`003F4C30`
  keyed on `(edx, r8d)` (key2 stored at record `+0x24`), applies it, then posts message
  `0x100` via `00244F50`. ~~**`00290130` is statically orphaned** — zero edges of every
  enumerated route form; the bundle-claim entry has no invoker in the shipped image.~~ **`00290130` is reached through its 5-byte thunk `002E1A50` (`jmp 0x290130`), which is called at `00344C9A` in `FUN_00344C60`, the begin handler of script verb `037C questresultwindow`** (2026-09-29, OPUS falsification pass 1, `CON-174`).
- ~~**What determines an action's gil cost** — `00309060` in §5 is called but not read.~~ *(answered: see using-an-item-is-an-action-that-costs-an-item.md, the section "The action gil cost: 00309060" - `10 × trunc(row.b[+0x0A] × 64.0 / 50.0)` under its gates, else 0; 2026-10-02, OPUS)*
- ~~Whether the two wrappers (`003004B0`, `00300500`) add behaviour beyond their names.~~ **Both
  do — §13**, and one of them changes what the meter records.

## 11. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Gil is `int32` at `[02092758] + 8` | `GameState_GetGil` decoded in full (3 instructions) | 1 |
| The clamp `[0, 99999999]` | `cmovns`/`cmovg` against `0x05F5E0FF` in `00254EE0` | 1 |
| Metering with kinds 6 and 7 by absolute delta | `mov cl,6` / `neg edx ; mov cl,7` around `call 0x316A50` | 1 |
| The delta is computed before the clamp | instruction order in `00254EE0`: `sub` at `+0x11`, clamp at `+0x29` | 1 |
| 13 direct callers, 0 thunks, 5 owners | direct-and-thunk caller census over the function list | 1 |
| 22 callers of `GameState_GetGil` | the same census over **both** entries of the name — body `00253690` (19) and thunk `00309BF0` (3), disjoint | 1 |
| Gil is the third execution-resource pool | `0030EFBB`–`0030EFD8` decoded, `unit+0xE58` named in `AI-8` | 1 |

**Controls.** The census tool resolves calls through JMP thunks as well as direct calls and reports
both; the "0 thunks" for `GameState_SetGil` is therefore a measurement, not an untested default. The
claim *"every change passes through one setter"* is bounded by that census: it means **no other
function in the corpus calls the setter**, and it is **not** a claim that nothing writes
`[02092758] + 8` directly — §9 depends on exactly that distinction, and a direct-write path would not
appear in a caller census.

**`check_already_answered.py` was run before this was written**, on `00254EE0` and the terms above.
It returned `N-7` as OPEN and `AI-8` as OPEN with gil already flagged as an inference — which is why
§5 is written as a confirmation rather than a discovery.


## 12. Related

- [`loot-drops-and-enemy-chain.md`](loot-drops-and-enemy-chain.md) — the defeat path that calls the award.
- [`experience-and-license-point-award.md`](experience-and-license-point-award.md) — the other two defeat rewards; it lists these two functions as unread, which this document closes.
- [`the-282-command-parameter-console.md`](../00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md) — `Debug_SetGilToMaximum` as one caller of thirteen.

## 13. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` re-run on the addresses this pass introduced, per EVIDENCE-STANDARD
amendment 2026-09-13c; it returned `AB-5` and `FU-2`, both already ANSWERED and both credited below.
Static only: the shipped image, its function list and a rel32 census. Nothing executed.)*

### The censuses reproduce, set for set

`GameState_SetGil` — **13 distinct caller functions, and they are exactly the thirteen in §4**
(`E8` 12 + `E9` 1). `GameState_GetGil` — **19** on the body excluding the thunk, **3** through the
thunk `00309BF0`, **overlap 0**, **union 22**: the 2026-09-03 correction reproduces exactly, including
which three functions reach it only through the thunk. The setter's body confirms §3 instruction for
instruction, including that a **zero delta calls the meter not at all** (`test edx, edx / jle` then
`jns` skips the call) and that the state pointer is loaded **twice** — once for the delta at
`00254EE6` and again for the store at `00254F18`.

**The one `E9` is `Debug_SetGilToMaximum`.** `003058B0` is ten bytes — `mov ecx, 0x05F5E0FF` then
`jmp 00254EE0` at `003058B5` — so the console row is the single caller of thirteen that reaches the
setter by tail-jump. ("No thunks" stands: no *thunk function* forwards to the setter.)

### ✔ Settled: `00316A50` reads `cl`, and the kind space is 30 wide

§3 raised the `cl`-versus-`ecx` question and declined to answer it. The first instruction answers it:

```asm
00316A50  cmp   cl, 0x1E        ; kinds >= 30 bail out
00316A53  jae   0x316BEA
00316A6F  movzx esi, cl         ; zero-extended
00316A72  movzx ebp, cl         ; and used as the table index
00316A7A  lea   r14, [00120000] ; the image base
00316A81  cmp   byte [r14 + rbp*8 + 0xBF0460], 0
```

**The upper three bytes of `ecx` are never read.** The idiom is correct. Two further facts fall out:
the meter accepts **30 kinds** (`0`–`29`), and it indexes an **8-byte-per-kind table at `00D10460`**.
Kinds 6 and 7 read `04 14` and `04 18`; kinds 11 and 17 read `04 10` and `04 1C` — **a four-member
family whose second byte steps by 4**, which is what four adjacent counters look like. What the rows
mean is not established, and this pass does not read the rest of `00316A50`.

### ✔ Both wrappers add behaviour — and one changes what the meter records

| wrapper | what it adds |
|---|---|
| `003004B0` `GameState_AddGilClampedAndNotify` | `GetGil()`, `ecx = gil + delta`, **floors at 0 itself** (`xor ebx,ebx / test ecx,ecx / cmovns ebx,ecx`) before calling the setter, then branches on `test dil, 1` — a **second argument** gating the notify its name promises |
| `00300500` `GameState_SetGilClampedNonnegative` | floors at 0 the same way, calls the setter, and **returns the floored value** |

> **The pre-floor is not redundant with the setter's clamp — it changes the statistics.** Spending
> 1,000 from a balance of 500 through `003004B0` sets 0 and meters a **spent** delta of **500**; the
> same intent expressed as `SetGil(-500)` ~~meters **500** as well, but~~ meters **1,000**, the distance from 500 to `-500`, because the delta is taken on the raw argument before the floor (`00254EF1`–`00254F02`; GL-3) *(corrected 2026-10-02, OPUS)*; generally, `SetGil(newValue)` computed by a
> caller that went further negative meters the full negative distance. §3 already says the delta is
> measured before the clamp; this says which callers keep the meter honest and which do not.

`003F4AA0` is a **record applier**: `test byte [rcx], 1 / je` guards `SetGil(GetGil() + [rcx+4])`, and
the function then walks a count at `[rcx+8]`. What the record is remains open.

### §13a — the record is a fetched reward bundle; its entry is ~~orphaned~~ the quest-result window's (2026-09-22, SWE2-CONTRACT; corrected 2026-09-29, OPUS, `CON-174`)

`003F4AA0(rcx=record)` in full: the flag byte's bit 0 gates `SetGil(GetGil() + dword[record+4])`
(`003F4AB5`–`003F4AC1`); a `[record+8]`-counted list of stride-4 `{itemId, count}` entries at
`+0x0C` is granted by `00300B80(id, count, 0)` (`003F4AE0`–`003F4AFB`); a `[record+0xA]`-counted
list of stride-2 single items at `+0x1C` is granted by `00300B80(id, 1, 0)` (`003F4B02`–`003F4B2B`).

Its only caller is `00290130(ecx, edx)`: `003F8C60` (a two-instruction thunk storing `edx` at
record `+0x24` and tail-jumping to `003F4C30`) fetches the bundle — `003F4C30` resolves a keyed
record through `0030AAC0`/`0030AEA0` into the gil amount plus the two item lists — then
`003F4AA0` applies it and `003F4BD0` posts message `0x100` through `00244F50` with the record's
key. ~~`00290130` itself has **zero routes of every form**: no `call`/`jmp` edge, no `lea` or
immediate materialisation, no qword slot in any data section, and the only RVA32 slot in the
image is its own `.pdata` entry. The bundle claim is shipped but never invoked; its gil write
is therefore a writer in the census, not a path a player reaches.~~ **Corrected (2026-09-29, OPUS falsification pass 1, `CON-174`).**
`00290130` has exactly one inbound edge, the thunk `002E1A50` (`jmp 0x290130`; catalogued as
`thunk_FUN_00290130`), and that thunk is called at `00344C9A` in `FUN_00344C60`, the begin handler of
script verb `037C questresultwindow`.
- The route census counted edges to `00290130` and never to its thunk. Its other route forms are still
  empty: no `lea` or immediate, no qword slot, and the RVA only in `.pdata`.
- So the bundle claim is how the quest-result window grants its reward, and the gil write is a path a player
  reaches.
- `falsify_gil.py` K1 is the regression.

The same pass bounds §10's last question: **no consumer reconciles the meter against the
balance.** The meter's counter records live behind `0020CE00()` (singleton `01F84450`), which
has exactly three callers — `00863240`/`00863280`/`008632B0` — and every body calling that
accessor family (`00315FDA`, `003162E0`, `00316440`, `00316A63`, `0034C9A0`, `00352250`) is
disjoint from all ~~21~~ 22 bodies calling `GameState_GetGil` or its thunk *(corrected 2026-10-02, OPUS: 19 direct and 3 through `00309BF0`, §4's census and CONTRACT-gil-storage-and-movement.md GL-5)*. Metered totals and the
balance never meet in one body.

### ✔ New: the direct-write question is now bounded

§11's controls note says a direct write to `[02092758] + 8` "would not appear in a caller census".
True — so the pointer itself was censused instead. Over all 38,161 function bodies, `02092758` has
**10 rip-relative references in 9 functions**, and that is every rip-relative holder in the image:

| function | what it does with the pointer |
|---|---|
| `00253970` | **the binder** — `mov [02092758], rax` from `002EF640()`, the active save buffer |
| `GameState_GetGil` `00253690` | reads `+0x08` |
| `002536B0` | reads `+0x18` / `+0x1A` / `+0x1B` (the play clock) |
| `002536D0` | reads `+0x0C`, **clamped to `0x05F5E0FF`** |
| `00253A80` | `memset(ptr, 0, 0x58)` |
| `00254C90` | reads `+0x18` / `+0x1A` / `+0x1B` into out-params |
| `00254CC0` | **`add [ptr+0x10], rcx`** |
| `00254E80` | **`mov [ptr+0x0C], eax`** |
| `GameState_SetGil` `00254EE0` | reads `+0x08`, writes `+0x08` |

**Only two of the eight readers write anything, and neither writes `+0x08`.** So a direct write to gil
would have to arrive through a pointer handed along rather than loaded — the census cannot exclude
that, but it now names the only other way in. §9's warning stands and is no longer untested at the
rip-relative level.

The binder also settles where the object lives: `002EF640()` is the **active save image buffer**, so
the game-state object *is* the image's first bytes and gil at `+0x08` is the same `+0x08` the save
pages read. **Already on record** — the save-payload field map lists `02092758` at payload `-0x200`,
and `AB-5` records the same function binding `020927C0` — credited here rather than re-announced.

### ○ A lead: 99,999,999 is not gil's alone

`002536D0` reads `+0x0C` and clamps it to **the same `0x05F5E0FF`**, and `00254E80` writes `+0x0C`
from `00320D50()`. **`FU-2` names that field**: the **walked-distance total**, mirrored into header
`+0x0C` for the achievement checks and the UI. The *mirror* is on record; **that it carries gil's
exact ceiling is not**, and a reimplementation that clamps only gil would let one of the two fields
run past a limit the engine enforces on both.

**Not claimed.** ~~What `00316A50` does with kinds 6 and 7 — only its argument handling and its table's~~
~~shape were read. How the award amount is computed,~~ *(answered: the kinds 6 / 7 meter — CONTRACT-gil-storage-and-movement.md GL-2 and §14; the award amount — CONTRACT-defeat-rewards-sequence.md DR-4; 2026-10-02, OPUS)* Still not claimed: ~~what determines an action's gil cost (`00309060`~~
~~unread)~~ *(answered: see using-an-item-is-an-action-that-costs-an-item.md, the section "The action gil cost: 00309060"; 2026-10-02, OPUS)* and what `00320D50` returns. Whether anything writes
`[02092758] + 8` through a handed pointer — **outside this instrument's reach and said so.** Nothing
was executed and nothing was observed live.

## 14. The `00253970` exclusive subtree — the binder's 31 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 31 frontier functions to `00253970`, the save-buffer binder
§11 names. All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| pool allocator | `00247AE0` (1,348 B — `00203170` ×5 + `002497B0` ×5 + `002465F0` ×5 + `008626C0`/`00202D70`/`00861EC0` ×2, consts `0090030C`/`384`, `00915248`–`5C`) | the `0x7E00`-byte pool the party page describes; the five-×-five call shape is five parallel sub-pool inits |
| `0209BE80` block family | `0028F2F0` (629 B — `00273B40` ×4 + `003697F0` ×3 + `00274840` ×2 + eight more, table `00290DF0`), `0028F8B0` (190 B — `0028F2F0` + `002B9FD0`/`00271420`/`00291750`/`00296260`/`00296240`/`004FE3C0`/`00244F00`), `00290430`, `00291750` (144 B — `00271420`/`00272470`/`0028A080`/`0028CA30`/`002BE450`/`002BE0A0`/`003FA760`), `00274840` (`002446E0`/`002473B0`/`002482E0`), `002A79E0` (`0209C510`), `002B3550` (`008620A0`/`00254A10`/`0024ABC0`, `0209D490`), `002BE450` (`00245000`/`00246AC0`, table `002BE490`) | the second `0209BE80` accessor family in this census (the `002778C0` battle-menu subtree has its own band) — here serving the binder's UI-facing side |
| `022Cxxxx`/`022CAxxx` cells | `0035C560` (68 B — `0028F8B0`/`00253480`/`00290430`/`003C5E40`, `022C8060`), `0035FF60` (`022CAE95`), `00364950` (`003658F0`, `022CBBB0`), `003658F0` (`0032E400`/`004745D0`/`0032E620`, `022CBE00`), `00365DD0` (`004745D0`, `022CBE00`), `00368270` (`022CBE30`), `0039BB30` (`02AEE810`), `0039C3F0` (`0032E400`/`003EFCD0`/`0032E620`), `003EFCD0` (alloc triple `0036C1D0`/`0036A100`/`0036C140`) | state cells the binder primes — the `022CBExx` band reuses the deque-alloc family |
| leaves | `0017F9E0` (`001B5FB0`), `00229E30` (`01E02818`), `002494A0` (`02090790`/`02090910`), `0024A660` (`0208F580`), `00272470`, `002800F0` (`0209AC60`), `0029CE40` (`00229E30`/`00229E40`/`0017F9E0`/`0039BB30`/`002B3550`/`00364950` — a small fan-out), `002DD4A0`, `003C5E40` (`02B45A00`), `003CA2B0` (`00244F00`, `02B47758`), `003F30A0` (`call rdi` thunk), `003FA760` (`00275550`), `008620A0` | small reads and thunks |

The shape matches the binder's role: one pool allocator, the `0209BE80` block family, and two
dozen cell writes — a save-slot bind is a publish step, not a compute.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

**The layer crossings that bear on gil:**

- **Presentation — SERVICE and CLIENT.**
  - `BattleUnit_ProcessDefeatRewardsAndLoot` publishes its award through `Reward_PublishExpLpPresentation`.
  - `Debug_SetGilToMaximum` (`003058B0`) is called by the 13,753-byte developer console body. That is the console gil
    row §4 names.
- **Gameplay — SERVICE.** `GameState_AddGilClampedAndNotify` (`003004B0`) is called by
  `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects`. **Activating a definition can add gil.**
- **ActorEntity — SERVICE.**
  - `00312280` reads the defeated unit's world position.
  - `00388D50` maps a definition selector.
- **RNG_Random_Selection — SERVICE.** `0038F6F0` draws the gameplay MT.
- **Input — CLIENT.** The save-buffer binder `00253970` calls two Input-filed helpers (24 B and 26 B). The file request
  `0032E620` is also issued by the 177-byte Input-filed loader, which loads the item graphics (see
  [the PKFL container](../26-PKFL-Package-Container/Container/pkfl-package-container.md) crossings).

**The rest of the Presentation, ActorEntity and Gameplay edges are MECHANICAL.** They come from §14's subtree table,
which names shared helpers of the binder:

- the 44-byte vector helper `00203170`, which has 29 rendering and skeleton callers and
  `BattleAction_FindApproachGeometryAroundTarget`;
- the 7-byte locale getter `00229E40` (see [the chain page](the-chain-and-its-sticky-coin.md) crossings);
- the 129-byte encoder `0036A100`, which has 26 Presentation callers;
- the file requests `0032E400` / `0032E620`, whose ActorEntity callers are the actor resource loaders;
- small accessors of 14–41 bytes, and a 529-byte pool helper.

Their callers are not gil paths, and they are recorded in the registry.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE.** A cited function is called by the 978-byte core start-up root, and cited functions call small core helpers (7 bytes twice, 27, 40 and 51 bytes).
- **Status_Periodic_Terminal — CLIENT and SERVICE.** Cited functions are called by `BattleStats_ChangeStatusAndProcessSideEffects` (2), `BattleUnit_RunPeriodicCombatMaintenance` and `BattleStats_ModifyStatusLayerStateAndProcessSideEffects`. They call the first and last of those, and `BattleStats_RecomputeDerivedStateAndAutoStatuses`.


*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — SERVICE (2 edges).** `BattleFormula_ApplyTargetResult` `003112F0` calls `003A1180` and `002DF220`, the resolve-then-play sound pair. The result applier that moves gil through slot 18 also plays its bit-14 sound through the audio layer; the sound does not touch the balance.

**CombatFormula — CLIENT and SERVICE (15 edges).** `003112F0` calls `GameState_GetGil` `00253690` and `GameState_SetGil` `00254EE0`, and also `BattleStats_SetCurrentHP` `00300520`, `BattleStats_ModifyHPAndProcessLethalState` `00300530`, `BattleStats_ModifySecondaryResource` `00300BC0`, `BattleStats_SetPrimaryResourceAbsolute` `00300C90`, `BattleStats_ModifyPrimaryResource` `00300CE0` and two more stat writers; `BattleAction_ConsumeExecutionResources` `00305640` calls `00300BC0` and `00300CE0`; `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` calls `BattleStats_GetByMappedBattleSlot` `00320AB0`; `0038EBE0` calls the walked-distance getter `00320D50`; the selector map `00388D50` calls `BattleStats_FindOwningBattleUnit` `0031B860` and `BattleStats_ResolveByActorHandle` `00320A70`. Gil is one of the execution resources §5 confirms: the same consume step that spends gil spends MP and the secondary resource through the formula layer's writers, and the result applier writes gil beside HP and MP.

**Items_Equipment_Shops_License — CLIENT and SERVICE (19 edges).** `00253690` and `00254EE0` are called by `InventoryBundleClass09_ApplyGilAndNestedItems` `002FD530`, `InventoryEncodedGilClass0E_ApplyGilDelta` `002FD880`, `Shop_CommitPurchaseItemAndGil` `002FEEB0` and `Shop_CommitSaleItemAndGil` `00310870`; `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0` is called by `002FD530`, `002FEEB0`, `00310870`, `BattleAction_RefundReservedExecutionResources` `00300280`, `BattleAction_PrepareExecutionResources` `0030EF20`, `003112F0` and `Inventory_GrantEncodedLootItem` `00300B80`; the shop commits also call `BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState` `0030B180` and `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` `0030B270`; `00300B80` is called by `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` and the bundle applier `003F4AA0`. The shop, bundle and gil-object paths of §4 are that layer's bodies, and each moves the item side of a trade through the same inventory write the action reserve/refund uses for item costs.

**Movement — CLIENT and SERVICE (21 edges).** The binder-subtree helper `00203170` — a 44-byte identity-matrix initialiser (four 16-byte rows copied from constants, the first starting 1.0) — is called by 20 Movement bodies, among them `0022EF20`, `00230790`, `0026EB30`, `00334220` and `00334AB0`; and `00312280` calls `00319490`, which resolves the party-focus actor and passes the defeated unit's position to a movement-side routine. The matrix helper is shared machinery with no gil meaning, and the defeat-reward path's position hand-off is the only movement step on a gil path.

**PlatformOnlineAchievements — SERVICE and CLIENT (35 edges).** `00254EE0` and `00312280` call `AchievementCounter_UpdateAndMaybeFire` `00316A50` (which calls `00315E90`, `003165C0`, `003166F0`, `00316BF0` and `008632B0`); `00305640` calls `00316440`, which fires counter `0x13` once when bit 5 of the game-state byte `+0x3845` is set; the walked-distance clamp `002536D0` and writer `00254E80` are called by `003162E0` and `00316760`; `003162E0` (called by the re-check loop `00316930`) calls `003165C0`, `00863280` and `008632B0`, and `00316440` calls `00863280` and `008632B0`; the counter-object getter `0020CE00` is called only by `00863240`, `00863280` and `008632B0`, which call `0020CB50`, `0020CCA0` and `0020CE60`; `008632B0` is also called by `00315E90`; the verbs `0034C9A0` and `00352250` call `00863240` and `008632B0`. The setter feeds the gil meter, the achievement checks read the header `+0x0C` walked-distance mirror (§13's 99,999,999 lead), and the counter accessors are the achievement layer's own; none of them reads the balance.

**Script_VM_Native_Bridge — CLIENT (19 edges).** `0050FAF0` calls `GameState_AddGilClampedAndNotify` `003004B0` on one arm and `00300B80` on the other; `00254C90` (which reads the game-state bytes `+0x18`, `+0x1A` and `+0x1B` into out-parameters) is called by `00348970`, `00348D70`, `00349370` and `00349700`; `0032A850` (a 7-byte tail call, with argument 0, into the getter's five-byte thunk, which this page counts as the getter's second entry) by `00346000` and `00346510`; the locale getter `00229E40` by `0033FED0` and `0034BA00`; `00203170` by `00356160`; the file requests `0032E400` and `0032E620` by `0050DF70` and `0050DFE0`; `0036A100` by `0050D8F0`; `00863240` and `008632B0` by `0034C9A0` and `00352250`; and the verbs `00344C60` (`questresultwindow`, the thirteenth writer's entry), `0034C9A0` and `00352250` pop their arguments through `VMValueStack_PopInt32CoerceFloat32` `00267E10`. Script can read gil (through `0032A850`), add it (`0050FAF0`) and reach the quest-result bundle writer; the remaining verb edges are shared helpers.

**UI — CLIENT, OUT-OF-SCOPE (222 edges).** The page cites 45 UI-filed helpers as members of the save-buffer binder's §14 subtree or as EC7-measured bodies, and 222 edges are those helpers' other UI callers and callees: the 15-byte bind-to-global prelude `00246AC0` has 31 UI callers, among them `BattleMenu_UpdateCommandSelectionAndDispatch` `002778C0`; `00245000` (a 31-byte wrapper that calls `002465F0` with 1) has 20; the locale test `00254A10` (1 for locale ids 0, 7, 8, 10 or 11) has 12; `0035BB20` (entry *i* of the `0xC0`-stride table at `022C8080`, bounded by the count at `022C8064`) has 11; `002778C0` itself calls 28 UI bodies and `00279E20` calls 17; and the `0209BE80` block family (`0028F2F0`, `0028F8B0`, `00291750`) and the resolve-and-flag `00296AF0` / `00272EE0` pair account for most of the rest. These are menu and binder machinery; none of them moves or reads gil, and the binder's gil-related role is only the save-slot publish §14 describes.

## Interior citation — frontier hub `00246AC0` (2026-09-18, SWE2-EC7)

`00246AC0` — 15 B, 55 callers; the singleton-load leg the `002BE450` family above invokes.
Interior verified: the callee's first argument is rebound to the `0208EA28` global
(`mov rcx, [0208EA28]` at [`00246AC3`](../_index/ADDRESS-INDEX.md)) while the caller's `rcx`
becomes `rdx`, then `jmp 00246AD0` at [`00246ACA`](../_index/ADDRESS-INDEX.md). A shared
"bind to the global object" prelude — the dispatcher is `00246AD0`.

## SWE2-EC7-37 update (2026-09-19) - `008626C0`

`008626C0` (529 B) is ~~a gil move/clamp body~~ the 529-byte pool helper of the binder subtree, not a gil path: an SSE float body that is not among `00254EE0`'s thirteen callers *(corrected 2026-10-02, OPUS: checked at `008626C0`; §4's census)* - `01F44830`, `00203170` pair plus `00202D70`/`00808C40`. Interior anchor `0086275F` (a `00203170` call).


## SWE2-EC7-64 update (2026-09-19) - `0029CE40`

`0029CE40` (142 B) is a rewards leaf body - `0017F9E0`/`00229E30`/`00229E40`/`002B3550`/`00364950`/`0039BB30` plus `0209C320`-`0209C338`. Interior anchor `0029CE4A` (a `00229E30` call).



## SWE2-EC7-65 update (2026-09-19) - `00368270`

`00368270` (136 B) is a `022Cxxxx` cell body - `00861EC0` single call plus `022CBE30`-`022CBE3E`. Interior anchor `00368281` (a `00861EC0` call).


## SWE2-EC7-101 update (2026-09-20) - `00296AF0` measured

`00296AF0` (132 B) is the resolve-and-flag `002778C0` and
`00279E20` call: `00273320` maps `edx` to an index
(negative tails `00296B80`); while `word[+0xB4A]` bit 3
is set and the `0x160`-stride record's `word[+0x2DA]`
minus `word[[+0x298]+6]` plus `word[[+0x118]+6]` still
equals `word[+0x15A]`, nothing changes - otherwise bit 2
arms and the index lands at `+0xB58` - the
position-watch flag ~~the gil paths maintain~~ of the UI binder, which moves and reads no gil *(corrected 2026-10-02, OPUS: the UI crossing paragraph above)*.
Interior anchor `00296B2D` (the `0x160` index).

## SWE2-EC7-103 update (2026-09-20) - `00272EE0` measured

`00272EE0` (71 B) is the keyed table fetch
`00279E20`, `0027C3D0` and `0029B550` call: a
four-iteration `0035BB20(i)` scan finds the entry
with `dword[rax + 4] == edi` and returns
`movsx word[rax + 0x60]`; no match returns 6 -
the code-to-word translate ~~the gil paths share~~ of the UI menus, which no gil path reads *(corrected 2026-10-02, OPUS: the UI crossing paragraph above)*.
Interior anchor `00272EFC` (the `+4`
compare).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-gil-storage-clamp-and-every-path-that-mo-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017F9E0` | 44 B | calls `001B5FB0()` and tail-jumps to `001B44A0` with `rcx` = that result, `edx` = the incoming `ecx` and `r8d` = the incoming `dl` zero-extended | `0017F9EA`, `0017F9EF`, `0017F9F7`, `0017FA07` |
| `0020CB50` | 334 B | scans the seven 12-byte entries ending before `009062E8` (first pair at `00906294 - 4`) for one whose dwords `+0` and `+4` equal `edx` and `r8d`, returning when none does; for match `i` it updates record `k` (`k` = signed dword at `00906298 + i * 12`) of the `0x198`-byte records at qword `rcx+8`, and when `i` is 6 also records 31 to 37 (offsets `0x3168` up to `0x3C90`); a record whose byte `+0x190` is 0 gets that byte set to 1 and dword `+0x194` set to 0 and, when byte `rcx+0x18` is non-zero, the qword `+0x28` of `[008C3190](01DFE0D0)` has its vtable slot `+0x38` called with the record's qword `+8` and then slot `+0x50` | `0020CB74`, `0020CBB0`, `0020CBC8`, `0020CBF2`, `0020CC80` |
| `0020CCA0` | 23 B | returns the zero-extended byte `+0x190` of record `edx` (sign-extended) in the `0x198`-byte records at qword `rcx+8` | `0020CCA3`, `0020CCAA`, `0020CCAE` |
| `002494A0` | 65 B | when qword `0208F578` is 0, stores `02090910` to it and calls `00861EC0(02090910, 0, 0x780)`; on both paths then tail-jumps to `00861EC0(02090790, 0, 0x180)` | `002494A4`, `002494BD`, `002494C4`, `002494CB`, `002494DC` |
| `0024A660` | 20 B | tail-jumps to `00861EC0(0208F580, 0, 0x1208)` | `0024A662`, `0024A669`, `0024A66F` |
| `00272470` | 42 B | zeroes qwords `rcx+0` and `rcx+0x10`, stores the 32-bit sum `ecx + edx` zero-extended to qword `+0x18`, and stores the low 32 bits of `rcx` plus 0x30, rounded up to a multiple of 0x10 in 32 bits when not already one, to qword `+0x20` | `00272472`, `00272477`, `0027247B`, `0027248B`, `00272495` |
| `00274840` | 40 B | when `rcx` is non-null calls `002446E0(rcx)`, `002473B0(rcx)` and `002482E0(rcx)` in that order; a null `rcx` returns at once | `00274843`, `0027484D`, `00274855`, `0027485D` |
| `002800F0` | 38 B | when qword `0209AC30` is 0, stores `0209AC60` to it and tail-jumps to `00861EC0(0209AC60, 0, 0xE00)`; otherwise returns | `002800F8`, `002800FA`, `00280109`, `00280110` |
| `00290430` | 19 B | stores `ecx` to dword `+0xAA44` of the qword at `0209BE80` when that qword is non-null; otherwise returns without writing | `00290437`, `0029043C` |
| `00290DF0` | 28 B | when `rcx` is non-null, tail-jumps to `00273B40` with `rcx` = qword `+0x10FC0` of the qword at `0209BE80` and `rdx` = the incoming `rcx`; a null `rcx` returns | `00290DF5`, `00290DF8`, `00290DFF`, `00290E06` |
| `002BE490` | 88 B | tail-jumps to `005C5230(rcx, rdx)` unless dword `[rdx]` is 2; when it is 2, zeroes word `rcx+0x10F8` if `001EDEC0(dword rcx+0xB4)` is non-zero and `002BF4F0(rcx, word rcx+0x10F8)` returns 1, then calls `002BE290(rcx+0xAC0)` and returns 0 | `002BE4A3`, `002BE4AE`, `002BE4C1`, `002BE4CD`, `002BE4DB` |
| `00300500` | 28 B | clamps `ecx` to 0 when it is negative (`cmovns` keeps it when non-negative), calls `00254EE0` with the clamped value and returns that value | `0030050A`, `0030050F`, `00300514` |
| `0034C9A0` | 50 B | takes `a` = `00267E10(r9)`, calls `00863240(0032F240(dword +0x28 of 002640C0()), a)` and tail-jumps to `0026B750(a)` | `0034C9A9`, `0034C9B5`, `0034C9B8`, `0034C9C1`, `0034C9CD` |
| `0035C560` | 68 B | calls `00861EC0(022C8060, 0, 0x23C8)`, ORs dword `022C83E8` with 0x20, calls `0028F8B0()`, `00253480()` and `00290430(1)`, and stores `003C5E40()` to qword `022C83B8` | `0035C573`, `0035C578`, `0035C58E`, `0035C593`, `0035C598` |
| `00365DD0` | 115 B | takes `p` = `004745D0(0xA00)` and fills 0x40 records of 0x28 bytes there, each with qword `+0` = the previous record, qword `+8` = the next record, dword `+0x10` = 0xFF0000 and qwords `+0x18` and `+0x20` = 0; it then stores `p` to qwords `+0x220` and `+0x228` and `p + 0x9D8` to qword `+0x230` of the qword at `022CBE00`, and zeroes the first record's qword `+0` and the last record's qword `+8` | `00365DD9`, `00365DF4`, `00365DFC`, `00365E1C`, `00365E3A` |
| `0039BB30` | 33 B | calls `00861EC0(02AEE810, 0, 0xF0)` and tail-jumps to `0039C3F0` | `0039BB36`, `0039BB43`, `0039BB4C` |
| `003F30A0` | 48 B | when `rcx` is non-null, walks the chain from `rcx` through each node's qword `+0x70` (read before the call) until it is null, calling `rdx` with the node in `rcx` whenever `rdx` is non-null; a null `rcx` returns at once | `003F30A3`, `003F30B2`, `003F30BB`, `003F30C3` |
| `003F4BD0` | 92 B | builds a stack block (byte 0, qword `rdx`, dword `ecx`) and a stack record (dword 0, a pointer to that block, qword 0), calls `00244F50(0x100, 003F4E70, &record)`, and checks the stack cookie from `01F44830` through `00808C40` | `003F4BE9`, `003F4BF5`, `003F4BF9`, `003F4C15`, `003F4C22` |
| `003FA760` | 35 B | calls `00275550(rcx, 0x26C0)` and then stores 0xFFFF to word `rcx+0x249A` | `003FA766`, `003FA76E`, `003FA773`, `003FA776` |
| `00863240` | 53 B | calls `0020CE00()` and, when it is non-null, calls `0020CB50(0020CE00(), ecx, edx)` with a second `0020CE00()` call supplying `rcx`; a null result returns without the second call | `0086324E`, `00863256`, `00863258`, `00863265` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-gil-storage-clamp-and-every-path-that-mo-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00300490` | 28 B | stores `r8d` as the fifth (stack) argument, sets `r9d` to 4 and `r8d` to 0, and calls `003008A0(rcx, rdx, 0, 4, incoming r8d)`, returning its result | Interior anchor `00300494`; Interior anchor `00300499`; Interior anchor `0030049F`; Interior anchor `003004A2` |
| `0030DD70` | 78 B | when dword `01EEBCFC` is greater than 0 (signed), calls `003008A0(i, 0x63, 0, 1, 0)` for `i` = 0, 1, ... (passed zero-extended from its low word), re-reading dword `01EEBCFC` after each call and looping while `i` is less than it (signed); when the dword is 0 or less it calls nothing; it sets no return value of its own | Interior anchor `0030DD7E`; Interior anchor `0030DDA0`; Interior anchor `0030DDA4`; Interior anchor `0030DDAB`; Interior anchor `0030DDB1` |
| `0032A810` | 24 B | calls `00300B80(rcx, rdx, 0)` and returns its result, except that a negative result (signed) is returned as 0 | Interior anchor `0032A814`; Interior anchor `0032A817`; Interior anchor `0032A81E`; Interior anchor `0032A820` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-gil-storage-clamp-and-every-path-that-mo-ee-1003-2/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0030AEA0` | 132 B | on a stack record `s` with dword 0xE at s+0 and `cx` at word s+6: returns -1 when `0031C5D0(&s)` is negative; otherwise stores dword [s+0x38] at dword [rdx], word [s+0x3C] zero-extended at dword [r8], word [s+0x40] sign-extended at dword [r9], word [s+0x3E] zero-extended at the dword the fifth argument points to and word [s+0x42] sign-extended at the dword the sixth argument points to (no null tests), and returns 0 | `0030AEBF`, `0030AECD`, `0030AEE4`, `0030AEFC`, `0030AF0B` |
