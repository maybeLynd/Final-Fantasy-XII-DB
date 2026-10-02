---
system: Event memory at actor bind — and why there is no hunt system (the bestiary half of that was refuted 2026-09-12; see §3)
category: 14-Story-Event-Quest-Hunt
status: AUDITED — DS-1 resolved 2026-09-16 (the eight list ids decoded); this page has no open item of its own — AA-2 and the +0x1394 gap are persistent-flag-banks.md's (status re-derived 2026-09-18, FABLE)
owner_layer: PrimaryOwner:Story_Event_Quest_Hunt
evidence_tier: 1
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: HIGH
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `00576300`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-08
archive_formats:
  - "EVME | explained | eventmemorylist.bin (.bin member): {EVME, MLST, u16 count, u16 ids[count]} (26 B) - (kind 9, 41) published by 00378A50 to 02ADD0A8, scanned by 00377440"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-event-memory-pass-1
  crossref_clean: true
  reopened_count: 1
---

# Event memory at actor bind — and why there is no hunt system

> **⚠ Scope, 2026-09-13.** The title is about **hunts**. The *bestiary* half of the original answer was **refuted on 2026-09-12** — the Clan Primer's monster records **are** native (§3). Everything below that says "neither" means the hunt side only.

> **Answers `AA-6`** — `EventMemory_QueryDefinitionIdAbsent` and its global — **and `AA-7`**, whether
> hunts and the bestiary use the flag banks or separate storage. **For hunts** the answer is that
> ~~neither exists~~ **no hunt subsystem exists** in native code, so there is nothing to ask which
> storage it uses. ~~The answer to the second is that **neither exists in native code**.~~ **The
> bestiary half was refuted 2026-09-12 — the Clan Primer's records are native (§3).**

## 1. What the player sees

A thing that has happened stays happened — and the native side of that is **smaller than its own
naming suggests**. Six flag banks with a uniform script-VM surface carry the persistent state, and
the two lookups this document opens with, despite being named for event memory, **gate a buffer
reallocation at actor bind**. Everything a player would call *a quest* is authored on top.

## 2. Two tables read at actor bind — one event-memory list, and the FIELD RECORD TABLE (corrected 2026-09-25, OPUS)

> **CORRECTED 2026-09-25 (OPUS), consuming FABLE-NOTICE-THE-SECOND-EVENT-MEMORY-TABLE-IS-THE-FIELD-RECORD-TABLE,
> re-measured from the image.** This section was headed *"Two event-memory tables"*. The shapes it gives are
> right; the OWNER of the second is not. `02ADD100` is `FieldRecordTable`, the table
> [the field-record accessor contract](../03-World-Area-Field/CONTRACT-field-record-accessors.md) (S-11) specifies:
> it has **seven rip-relative readers image-wide - `00377480`, `00377700`, `003779F0`, `00377A40`, `00377BA0`,
> `00377C20`, `00377C70` - seven of that contract's nine entries**, and `00377480` returns **bit 15 of the record's
> little-endian word** (`00377499`..`003774AC` `movzx` the bytes at `+9` and `+8`, `shl 8`, `add`, `shr 0xF`; `0` when
> the table is null or the id is out of bounds) - the contract's bit-15 permission, not two independent bytes.
> The genuine event-memory table is the OTHER one, `02ADD0A8`. So the S-34 mechanism here is ONE list plus a
> consult of an S-11-contracted table; it is not an uncontracted second event memory. `02ADD0A8` sits in the
> run of eight table pointers `02ADD0A0`..`02ADD0D8`, seven written by `00377CC0`; `02ADD100` lies past it. Both lookups take the same id,
> `esi = 0032F240(0)` (`0026C9B7`/`0026C9C3`).

`ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) consults **two** different lookups on the
definition id, one after the other, and takes a different action on each:

```asm
0026CA1E  mov  ecx, esi                  ; the definition id
0026CA20  call 0x377440                  ; EventMemory_QueryDefinitionIdAbsent
0026CA25  test eax, eax
0026CA27  je   0x26CA2E                  ; PRESENT -> skip
0026CA29  call 0x25A990                  ; ABSENT  -> reallocate buffer A

0026CA30  call 0x377480                  ; the sibling lookup
0026CA35  test eax, eax
0026CA37  jne  0x26CA3E
0026CA39  call 0x25AA30                  ; zero   -> reallocate buffer B
```

### What the two consequences are: buffer reallocation

Both are the same 155-byte routine over different globals, and they were read in full:

| | `0025A990` | `0025AA30` |
|---|---|---|
| buffer pointer | `02099DD0` | `02099DD8` |
| release tag | **13** | **14** |
| allocation size | **`0x100000`** = 1 MiB | **`0x19000`** = 100 KiB |
| pool selected first | 5 | 5 |

Each frees the existing buffer if one is held, then allocates a fresh one from pool 5. **Both pointers
are touched only by `ActorEntity` functions and these two allocators** -- including
`ActorManager_BindLoadedDefinitionPayload` itself, immediately before the queries -- so they are
**actor-definition payload buffers**.

> **So at this call site the two lookups gate memory, not story state.** The engine asks whether a
> definition id is already known and, if it is not, **makes room for it**.

**The name and the behaviour diverge here, and the behaviour is what this document reports.** The
query is named `EventMemory_*` and carries the `Story_Event_Quest_Hunt` owner, but its **only** call
site reads as buffer lifetime management. Whether the lists mean anything story-shaped elsewhere is
**not established** -- there is no elsewhere: the function has one caller.

**They are not two copies of one mechanism — the two tables have different shapes.**

### `EventMemory_QueryDefinitionIdAbsent` (`00377440`) — a linear id list

```c
t = [02ADD0A8];
if (!t) return 1;                        // no table -> absent
n = *(uint16*)(t + 8);                   // entry count
if (!n) return 1;
p = t + 0xA;
for (i = 0; i < n; i++, p += 2)
    if (*(uint16*)p == id) return 0;     // present
return 1;                                // absent
```

A **count at `+8`, `uint16` entries from `+0xA`**, searched linearly. The function returns *absent*,
not *present* — the name is accurate and the polarity matters at the call site above.

### `FUN_00377480` — a directly-indexed record table: the field record's bit 15 (S-11; OPUS 2026-09-25)

```c
t = [02ADD100];
if (!t) return ...;
if (id >= *(uint32*)(t + 4)) return ...;  // a bound, so id indexes directly
rec = t + 8 + id*3;                       // stride 3
b0 = rec[0]; b1 = rec[1];                 // two bytes per entry
```

**A count at `+4` and three-byte records from `+8`, indexed by the definition id itself.** No search.

> **One table asks "is this id in a list?", the other asks "what does this id's record say?"** A list
> that grows as events happen and a table sized to the id space are different kinds of memory, and
> the engine consults both before binding an actor.

The list at `02ADD0A8` is written by `FUN_00377CC0` (`WorldAreaField`) and `FUN_00378A50` — **it is
populated at area load**, not at the moment an event occurs.

> ### Reopened 2026-09-08 — the list is a shipped file, and it is named
>
> `00378A50` is not called by anything. It is **address-taken** at `0037881D` inside
> `WorldAreaField_RequestAuthoredMapTables` (`00378540`), where it is installed as the publisher
> for resource **`(kind 9, index 0x29 = 41)`** — which the executable's own path array names
> **`PS2Data\image\ff12\common\eventmemorylist.bin`**. The shipped
> `FileSizeTable_*.fst` give it **26 bytes**, identically in all twelve languages: an 8-byte
> header, the `u16` count at `+8`, and room for **at most 8** `uint16` entries from `+0x0A`.
>
> So *“what fills the entries”* is **authored data on disk**, not runtime accumulation — and the
> reading below that the list *“grows as events happen”* is **not supported**: nothing writes the
> list body, only the pointer. The derivation, the controls and the caution that 8 is a capacity
> rather than a count are in
> [`persistent-flag-banks.md` §8f](persistent-flag-banks.md). The ids themselves are still
> unread — `DS-1`.

## 3. `AA-7`: hunts are not a native system — ~~and the bestiary~~ **the bestiary is** (refuted 2026-09-12)

The question was whether hunts and the bestiary use the flag banks or separate storage. **Neither,
for hunts.** ~~Neither.~~ — the bestiary answer below is **withdrawn**; see the 2026-09-12
correction at the end of this section.

| Probe | Result |
|---|---|
| `"bestiary"` / `"Bestiary"` anywhere in the file | **0 occurrences** |
| `"hunt"` | 1 — inside `"onSessionDisconnected ServerShuntdown"`, a network log string |
| `"Hunt"` | 1 — `"Hunter Extraordinaire"` in `.data`, an **achievement name** |
| `"clan"` | 1 — `"Set clan point: "`, a debug-menu row label |
| Functions owned by `Story_Event_Quest_Hunt` | **two**: the `PersistentFlag_*` setters and `EventMemory_QueryDefinitionIdAbsent` |

> **The only three occurrences of hunt-like words in the image are a typo in a network string, an
> achievement title, and a debug menu label.** There is no hunt code to ask which storage it uses.
>
> *(~~48 MB~~ — the shipping EXE is **32,864,752 bytes, 31.3 MB**; corrected 2026-09-13. The four
> string counts themselves reproduce exactly, §9.)*

What the native side actually provides is generic:

- **~~six~~ five persistent flag banks** (six accessor families) *(corrected 2026-10-02, OPUS: `Bank512`'s Low and High pairs address one `+0x14B4` region - queries `0032AA60` / `0032AAD0`, setters `0032AD70` / `0032ADF0`, the High pair adding `0x100` at `0032AAE7` / `0032AE04`; persistent-flag-banks.md AA-4)*, each with an identical script-VM surface of one query and two setter
  opcodes ([`persistent-flag-banks.md`](persistent-flag-banks.md) §8b);
- **two event-memory lookups** at actor bind (§2);
- **a statistics counter** (`00316A50`) with about twenty kinds, incremented by defeat processing and
  by the gil setter among others — the counters the debug menu displays as *"Count of killed
  monsters"* and similar.

**And the two event-memory lookups turn out to gate buffer allocation** (section 2), which leaves even
less native story machinery than the list above suggests.

**A hunt is therefore a flag convention plus a counter, authored in script over that surface.** That
is the same shape three other blocks have found: *the mechanism you are looking for is one field on a
table everything else already uses.*

> **Corrected 2026-09-12 (FABLE): the bestiary half of this answer is wrong — the Clan Primer's
> monster records are native.** No string says "bestiary" because the code keys it by number: the
> `.ard` slot-0 **class row's word `+0x52` is the Clan Primer entry id** (0–376, 374 distinct over the
> 954 shipped class rows, `0xFFFF` on 107 — [the unit-definition page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)), the same index space as the 384
> `MonsterId` entries of [the monster gallery file](../16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md), and a **512-byte block at save payload `+0xB404`** (block
> `+0x3404` of what `002536A0` returns, [the save-payload field map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)) holds one byte per entry: **0 = never
> encountered, otherwise 1 + defeats.** Three functions own it, each bounded by `id < 0x200`:
>
> | function | does | reached from |
> |---|---|---|
> | `00315A90` (thunk `00253760`) | **registers** an entry — sets the byte to 1 when it is 0 | `00306010`, on an action's execution: every enemy in the acting unit's target buffer, and the acting enemy itself, whenever the other side is party-kind (`0030606F`–`003060B4`) |
> | `00315820` (thunk `00253750`) | **counts a defeat** — `count = byte − 1` (0 if unregistered), `byte = min(count + 1, 0xFE) + 1`, but **only when `00315D50(id)` returns −1** (`00315871`–`0031588E`) | `003171C0` on an enemy-kind defeat, right after the kill achievement counter (`00317207`–`0031721F`, [the achievement catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md)) — and only for actors whose free-target type is not 3 |
> | `00315420` (thunk `00253720`) | **reads** `byte − 1`, or −1 when unregistered | the achievement store dispatcher `00315E90` and the Clan Primer menus (`003154B0`, `003161A0`, `005760A0`, `00576E30`) |
>
> `00315D50` walks a relative-offset chain from the static `022C2550` (three `u16` hops) to a list of
> at most eleven `u16` ids and, when the id is listed, returns a word from the table at `01EED130` —
> a per-field exclusion list whose meaning (marks, story bosses) is not read here. So: the hunts are
> script conventions, but **the bestiary's sighting and defeat counts are one native block, separate
> from the flag banks** — which is the answer AA-7 asked for.

> **This is a complete answer, not a thin one.** "The native side is banks, two id lists and a
> counter; the quest logic is authored" is what the code supports, and there is no further native
> layer to read.

## 4. Key addresses

| Address | Name | Role |
|---|---|---|
| `00377440` | `EventMemory_QueryDefinitionIdAbsent` | linear id-list lookup (§2) |
| `00377480` | — | the field record's bit 15, explicit id — an S-11 `FieldRecordTable` accessor (§2, corrected 2026-09-25) |
| `0026C8C0` | `ActorManager_BindLoadedDefinitionPayload` | the **only** caller of the first; calls both |
| `00377CC0` | — | writes the list pointer, `WorldAreaField` |
| `00378A50` | `EventMemoryList_PublishLoadedTable` | publishes the list pointer; **address-taken only**, at `0037881D` |
| `00378540` | `WorldAreaField_RequestAuthoredMapTables` | requests `(9, 41)` and installs the publisher |
| `02ADD0A8` | — | the id list: count `+8`, `uint16` entries from `+0xA` |
| `02ADD100` | `FieldRecordTable` | the field record table (S-11): count `+4`, 3-byte records from `+8` |
| `0032AD70` | `PersistentFlag_SetBank512Low` | the setter the authored trigger points call |

## 5. What is not known

- **What the two payload buffers hold.** Their sizes (1 MiB, 100 KiB), tags (13, 14) and lifetime are
  read; their contents are not.
- **What the three bytes of an `02ADD100` record mean.** Two are read at the call site examined; the
  third was not seen used. *(2026-09-25: the first two form the field record word the S-11 contract
  specifies; the third byte is read by no accessor in that family - FABLE's observation, still open.)*
- [x] ~~**What populates the `02ADD0A8` list** with ids.~~ **ANSWERED 2026-09-08** — the shipped
  `eventmemorylist.bin`, resource `(kind 9, index 41)`, 26 bytes, published by `00378A50`.
- [x] ~~**Which ids it carries** — `DS-1`.~~ **ANSWERED 2026-09-16** — the file extracts whole from
  the VBF as a standalone member (`common/eventmemorylist.bin`, 26 B, sha `5027c063…`), not from
  inside an `SRYK` container. Decoded byte by byte:

  ```
  +0x00  char[4]  "EVME"
  +0x04  char[4]  "MLST"
  +0x08  u16      8          entry count — the fill, not a capacity: 0x0A + 8*2 = 0x1A = 26
  +0x0A  u16[8]   {0x0000, 0x0031, 0x029C, 0x029E, 0x030E, 0x0367, 0x0368, 0x0390}
  ```

  This is exactly the shape `00377440` scans (`u16` count at `+8`, `u16` entries from `+0xA`).
  The eight ids are the definition ids the actor-bind path treats as **already provisioned** —
  present in the list → skip the 1 MiB buffer-A reallocation. `00377440` never reads the
  `EVME`/`MLST` tags; they are shipped markers only.
- **Whether the two lookups concern the same kind of event.** They are consulted consecutively on the
  same id, which is suggestive and is not evidence.
- `AA-2` and the `+0x1394` gap remain open in
  [`persistent-flag-banks.md`](persistent-flag-banks.md); nothing here touches them.
  *Status 2026-09-26 (FABLE, Claude Opus 5.5): both are now closed in the register. `AA-2` is ANSWERED as `UQ-138` (the same question, answered 2026-09-18 from the script verbs), and the `+0x1394` gap is `AA-5`, ANSWERED 2026-09-21 by SWE2-CONTRACT on the flag-bank contract: reserved space that only the payload clear touches. Nothing here depended on either.*

## 6. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The query is a linear `uint16` search | `00377440` decoded in full, 62 bytes | 1 |
| It returns *absent*, not *present* | the `return 1` on fall-through and `return 0` on match | 1 |
| The sibling is directly indexed, stride 3 | `cmp ecx,[r8+4]` bound then `[r8+rcx*2]` plus `rcx`, bytes at `+8`/`+9` | 1 |
| Both are consulted at actor bind, with different consequences | `0026CA20`-`0026CA39` decoded | 1 |
| The consequences are buffer reallocations, 1 MiB and 100 KiB | `0025A990` and `0025AA30` decoded in full; sizes `0x100000` / `0x19000` at `0025A9D5` / `0025AA75` | 1 |
| The buffers are actor-payload buffers | image-wide sweep of both pointers: every non-allocator site is `ActorEntity`-owned | 1 |
| The query has exactly one caller | direct-and-thunk caller census | 1 |
| The list pointer has two writers | image-wide rip-relative sweep of `02ADD0A8` | 1 |
| No bestiary or hunt code | byte search of the whole file for four terms, with every hit inspected | 1 |

**Controls.** The `AA-7` negative is a **string and ownership** measurement, and its limits are
stated: it shows there is no hunt subsystem *named* in the image, and that only two functions carry
the `Story_Event_Quest_Hunt` owner. It does **not** show that no code implements hunt behaviour under
another name — that is why §3's positive half matters, describing what the native surface *does*
provide rather than resting on the absence.

**Every string hit was read rather than counted.** Three of the four terms matched, and all three
matched something unrelated — a typo, an achievement title and a menu label. **A count of matches
would have reported "hunt: 1" and been misleading in the opposite direction.**

## 7. Related

- [`persistent-flag-banks.md`](persistent-flag-banks.md) — the ~~six~~ five banks *(corrected 2026-10-02, OPUS: five storage regions, six accessor families; AA-4)*, their payload offsets, and the uniform script-VM query/setter surface; this document answers its `AA-6` and `AA-7`.
- [`gil-storage-clamp-and-every-path-that-moves-it.md`](../13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md) — the same statistics counter, reached from the gil setter.
- [`loot-drops-and-enemy-chain.md`](../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md) — the defeat path whose retire chain increments that counter.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

### §3's string census reproduces exactly — and that is the point

| probe | page | measured |
|---|--:|--:|
| `"bestiary"` | 0 | **0** |
| `"Bestiary"` | 0 | **0** |
| `"hunt"` | 1 | **1** — `"…Disconnected ServerShuntdown…"`, the same typo |
| `"Hunt"` | 1 | **1** — `"Hunter Extraordinaire"` |
| `"clan"` | 1 | **1** — `"Set clan point: "` |

**Every count is right, and the conclusion drawn from them was half wrong.** §3's own 2026-09-12
correction says why: *"No string says 'bestiary' because the code keys it by number."* The Clan
Primer entry id is the `.ard` class row's word `+0x52`, and a 512-byte block in the save holds the
per-monster state — a whole native subsystem that a name census **cannot see by construction**,
because it has no name in the binary to find.

> This is the sharpest example in the database of a correct measurement supporting a wrong claim.
> The instrument was not broken and the numbers were not wrong; **the inference from
> `0 occurrences` to `no system` is what failed**, and it failed on exactly the systems that are
> addressed numerically — which is most of this engine.

### ⚠ The refuted half was still being asserted in four places

The correction sat at the end of §3 while the **`system:` line, the H1, §1's blockquote, §3's
heading and §3's opening answer** all still said hunts *and the bestiary* are not native. Scoped to
the hunt half in all five, with the withdrawal marked rather than deleted.

### ⚠ "a 48 MB image"

The shipping EXE is **32,864,752 bytes — 31.3 MB**. Corrected; the rhetorical force of *three
occurrences in the whole image* survives the smaller number.

**Not claimed:** §2's two lookups, the buffer reallocation they gate, the six flag banks and the
statistics counter at `00316A50` were **not** re-derived — this pass took §3's census and the
stranded assertions. The Clan Primer's three owning functions and the `id < 0x200` bound are the
2026-09-12 correction's evidence and were not re-read. Nothing was executed or observed live.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `00576300` | 578 | event-memory record body (caller `00570080`): `[rbx+0x50]`, `[rcx+0xC9]`/`+0xCE`/`+0xF0`, `[r9+0xA]`; `00861EC0`, `00576E30` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Presentation — SERVICE.** `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) configures character fading at
  bind time. It reads and writes the built-in and default fade parameters (`CharacterRenderConfig_Get/SetBuiltInFade…`,
  `…DefaultFade…`) and sets `CharacterRenderSystem_SetFadeWidth` / `…SetFadeStartDi…`.
- **Movement — SERVICE.** The same bind sets `Movement_SetRequestedSpeed`.
- **CombatAction — CLIENT.**
  - `00306010` is called by `BattleUnit_AdvanceStandardActionState`, and it calls a 266-byte presentation-gated
    relationship check.
  - The persistent-flag setter `0032AD70` is also used by `BattleUnit_TryTriggerNearbyAuthoredFieldAction`
    ([walking into an authored trigger point](../03-World-Area-Field/walking-into-an-authored-trigger-point.md)).
- **Gameplay — MECHANICAL.** `00315E90` asks `BattleEncodedId_DispatchQueryMode0Va…`.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **PlatformOnlineAchievements — CLIENT and SERVICE, not read, 38 edges.** Cited event-memory functions are called by Platform-filed bodies (80 to 519 bytes) and call others (44 to 172 bytes). Which platform or achievement service these are is not read here.
- **Rewards_Progression_Economy — CLIENT.** Cited functions are called by `BattleUnit_ProcessDefeatRewardsAndLoot` (2) and `GameState_SetGil`.
- **CombatAI - CLIENT (3 edges).** `00377C20` is also called by bodies filed to combat AI: `003014C0`, `00301AD0`, `00305AB0` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (1 edge).** `00377C20` is also called by bodies filed to combat formula: `00300530` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT (1 edge).** `00377C20` is also called by bodies filed to input: `00253C70` - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT (1 edge).** `00377C20` is also called by bodies filed to InputGameplay: `00313A00` (FieldBattleCapabilityAndUIRequestInhibitMaskReconciliation) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (2 edges).** `00377C20` is also called by bodies filed to items/equipment: `00309FB0`, `0030FD10` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (4 edges).** `00377C20`, `00377C70` are also called by bodies filed to party: `00304180`, `00326500`; `0026C8C0` reaches bodies filed to party: `003590D0`, `00359200` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (2 edges).** `00378540` reaches bodies filed to resource: `0032E400`, `0032E620` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (2 edges).** `0026C8C0`, `0032AD70` reach bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (10 edges).** `0032AD70`, `0032F240` are also called by bodies filed to script VM / native bridge: `00353750`, `00353BD0`, `00267E60` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (3 edges).** `00377C20` is also called by bodies filed to status/periodic terminal: `0030E360`, `0030F690`, `00310DB0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (40 edges).** `002B58B0` is also called by bodies filed to UI: `00273E30`, `0027D480` (BattleMenu), `0027F210` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT and SERVICE (2 edges).** `00377CC0` is also called by bodies filed to World: `00266D10` (NativeSupport); `00377CC0` reaches bodies filed to World: `00378540` (Area) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (17 edges).** `002F9920` is also called by bodies filed to WorldAreaField (world area): `003C0450` (PersistenceGroupEntryCollection), `00576A50` (ConditionalBattleIdResolution); `0026C8C0`, `003154B0` reach bodies filed to WorldAreaField (world area): `0026DB30`, `00265270` - shared machinery across the layer boundary, no shared ownership.

## The `00315820` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00315820` (~112 B) — `ecx >= 0x200` bound check (`00315820`/`00315826`).

| member | role | interior |
| --- | --- | --- |
| `00315D50` | `qword[022C2550]` non-null + `+8` null check (`00315D50`/`00315D63`) | [`00315D50`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-37 update (2026-09-19) - `005760A0`

`005760A0` (597 B) is a Clan Primer menu body - `02CA9738`/`00D237A0`/`00D23790`, `002B58B0` pair plus `002F9920`/`003214B0`/`0035D330`/`00315420`/`00576860`/`00808C40`. Interior anchor `0057616E` (a `002F9920` call).

## SWE2-EC7-37 update (2026-09-19) - `00576300`

`00576300` (578 B) is an event-memory sibling - `02CA9738`/`01CEB638`, `00861EC0`/`00576E30`. Interior anchor `00576317` (an `00861EC0` call).

## SWE2-EC7-43 update (2026-09-19) - `00570080`

`00570080` (295 B) is an event-memory body - `00570630`/`005742D0`/`01F44830`, `00244F50`/`00576300`/`00808C40`. Interior anchor `005700CC` (a `00244F50` call).
