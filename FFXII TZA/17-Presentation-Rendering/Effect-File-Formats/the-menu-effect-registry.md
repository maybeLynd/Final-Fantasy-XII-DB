---
system: The menu effect registry — 64 id-keyed effect instances behind the type-4 EFX context
category: 17-Presentation-Rendering
status: DOCUMENTED — the record fields (UQ-208), the owning screens (UQ-210) and the instance field +0x338 (UQ-209, the context's mode base) all answered 2026-09-17
owner_layer: CodeDomain:Presentation (effects) — driven from UI code
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 68 addresses cited - 5 data, 30 entry, 33 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: reproduction
  last_pass_by: OPUS
  last_pass_state: opus-menu-effect-registry-pass-1 - the table shape is confirmed three ways from two routines that were not written to agree. 003B2F50 opens `lea rax,[02EBDBC0]` and `lea r9,[02EBE5C0]` and walks `add rax,0x28`, so base, exclusive end and stride are all read straight out of the image; (02EBE5C0 - 02EBDBC0) / 0x28 = 0xA00 / 0x28 = **64 records exactly**, the structural control this store uses everywhere. 003B2BC0 confirms the same geometry independently: it starts at 02EBDBE8 (base + one record) and tests `[rax-0x28]`, `[rax]`, `[rax+0x28]`, `[rax+0x50]` then `add rax,0xA0` - **four records of 0x28 per iteration**, exactly the unrolled scan for `id == 0` the page describes at 003B2BE0-003B2C11. 003B2F50's parameter write is `mov [rcx+0x338], edx` at 003B2F80 after loading the instance from `[rax+8]` - the address, the offset and the record field all as written. ONE CAUSAL LINK THE PAGE LEAVES IMPLICIT, and it is the reason the design is what it is: 003B2F50 aborts the whole scan at the FIRST record whose id is 0 (`je 003B2F86` on the id test, not `continue`). **The table is therefore required to be compact** - a hole would hide every record behind it from set-parameter. That is what forces 003B2AA0 to shift the rest down rather than simply clear the slot, which the page records as a step without saying what demands it. And the `02EBE598` that remove clears is not a loose address: base + 63 x 0x28 = 02EBE598, the id field of the LAST record - the slot compaction vacates. NOT CHECKED: 003B29B0's reset and EFX type-4 load, the spawn path through 0024B270, the claim that 0024C460 and 0024B270 are two of the ten writers of 02EBEF88, and the fields past +8 that the page already lists as unread.
  crossref_clean: false
  reopened_count: 0
---

# The menu effect registry

> **UI screens drive their effects by id.** A 64-record table at `02EBDBC0` maps an id to a live effect instance.
> `003B29B0` resets the table and loads the **type-4** EFX context. Around it sit spawn, remove and set-parameter
> routines, which menu code calls to spawn an effect and set its parameter, and to refresh it by removing the stored id and
> spawning again (~~spawn → set → remove sequences~~; corrected 2026-09-14, AUDITSEM-CONTRA-FABLE-EFX-REGISTRY). The instances are the same ones the effect
> instance walk updates each frame.

~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: DOCUMENTED`)* Read: the table shape, the API, the link to the instance list, the callers. ~~Not read: the record's~~
~~fields past `+8`, what `+0x338` in an instance means, and which menu uses which id.~~ *(answered: see UQ-208, UQ-209 and UQ-210, answered 2026-09-17; 2026-10-02, OPUS)*

*(2026-09-13, FABLE. Found by placing the unresolved residual functions `00572920`, `005734C0` and `00573690`,
which have no other documented neighbour, through their shared callees. See [the unresolved 158](../../99-Unresolved-Residual/the-unresolved-158.md) §14.)*

## 1. What the player sees

Animated sparkles, highlights and transition effects on menu screens, started and stopped as the player moves
through the menu.

## 2. Native mechanism

### 2.1 The table

```
02EBDBC0 .. 02EBE5C0 (exclusive)   64 records x 0x28 bytes
  record +0x00  u32   id (0 = free)
  record +0x08  ptr   effect instance
  record +0x10 .. +0x27  not read   <- corrected 2026-10-02, OPUS - read: +0x10..+0x1C are the spawn call's four arguments (UQ-208, 2026-09-17)
02EBE5C0   u32   count / state word (cleared by 003B29B0 at 003B2A27)
```

### 2.2 The API

| routine | role | evidence |
|---|---|---|
| `003B29B0` | **reset and load** | clears all 64 records (`003B29CD`–`003B2A20`) and `02EBE5C0`, calls `0024C460(4)` / `0024C550(4)` (`003B2A22`–`003B2A37`), builds an `0x890`-byte EFX context template with byte `+0` = **4** (`003B2A60`) through `0024B3A0`, and parses the EFX data with `003EDAD0` (`003B2A75`), all under an arena selection (`0036C1D0` / `0036C140`) |
| `003B2D80` | **spawn** | creates an instance through `0024B270` (`003B2E27`), takes a free record through `003B2BC0` (`003B2E36`) |
| `003B2BC0` | find a free record | scans for `id == 0`, unrolled four records at a time (`003B2BE0`–`003B2C11`) |
| `003B2AA0(id)` | **remove by id** | finds the record, releases `+8` through `0024EE60` (`003B2AED`), shifts the rest down (`003B2B1F`), clears `02EBE598` |
| `003B2930(instance)` | remove by instance pointer | the same compaction, keyed on `+8` (`003B2948`) |
| `003B2F50(id, value)` | set a parameter | writes `value` to `[instance + 0x338]` of the record with that id (`003B2F80`) |

`0024C460` and `0024B270` are two of the ~~ten~~ **eleven** writers of the effect instance list `02EBEF88`. The eleventh is
`003B8260` (`003B860D`), which a census scoped to `0024xxxx` missed; corrected 2026-09-14 (AUDITSEM-CONTRA-FABLE-EFX-REGISTRY)
([effect element type dispatch](effect-element-type-dispatch.md) §2.4). **So registry instances are ordinary effect
instances, updated by the same per-frame walk.**

### 2.3 Who drives it

- **Reset / load `003B29B0`:** `00558FB0` (`00559227`), `00561390` (`005614CA`), `00572E10` (`00572F44`).
- **Remove by id `003B2AA0`:** among others `00557DB0` (six sites), `005588C0`, `00558960`, `0055B560`.
- **The residual trio:** `00572920`, `005734C0` and `00573690` (callers `00572E10`, `00572E10`, `00573980`) call spawn,
  ~~set and remove in repeated triples~~ spawn, set and remove in two loop shapes (corrected 2026-09-14 from the control
  flow; the address order had been read as a sequence). Take `00572920`:
  - **First loop** (`00572A30`–`00572AAF`, `jl 00572A30`): per entry, spawn `00572A76`, store the id, then set `00572A95`.
  - **Refresh loops** (`00572AD0`–…, and the inner `00572B40`–`00572B90`): per element, if the stored id is not −1, remove it
    (`00572AEE` / `00572B4B`) and store −1. Then spawn (`00572B0A` / `00572B66`), store the new id, and set (`00572B25` /
    `00572B80`).

  The set value is `(0xFF − entry byte +1) × 10000`, the byte at offset `+1` of the entry. So a remove always precedes the spawn that replaces it: the pattern is a
  −1-sentinel replace, not a spawn → set → remove lifecycle.

~~**All of these callers are UI code.**~~ *Scoped 2026-09-14 (AUDITSEM-CONTRA-FABLE-EFX-REGISTRY).* Only some callers carry
evidence of being menu code:
- `00557DB0` and `005588C0` call named `BattleStats_*LicenseBoardSelector*` functions, and `00557DB0` reads
  `LicenseBoard…` layout keys.
- `00558FB0` and `00561390` are widget procedures that load `lic_*.tm2` files
  ([the menu screen atlas](../../16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md)).

~~`00558960`, `0055B560`, the trio and the trio's callers `00572E10` / `00573980` are placed in the menu range by address
only. The trio is still in the unresolved residual. Which screen each belongs to is not read.~~
**Placed 2026-09-17 (FABLE, `UQ-210`).** The trio and its callers are the **achievements screen**: `00572920` loops the
thirty achievement indices against the handbook value (`003165B0`) and a save-block flag query (`00576E10`), spawning one
effect per matched layout entry. `00558960` (only caller `00558A10`, only caller `00557DB0`) and `0055B560` (callers
`0055CD40`, `0055DBD0`, both `BattleStats_*LicenseBoardSelector*` users) are the **licence board**. One spawn caller
outside this list, `0055F010`, is not placed.

## 3. Key addresses

| address | role |
|---|---|
| `02EBDBC0` | the 64-record registry |
| `003B29B0` | reset + type-4 EFX load |
| `003B2D80` / `003B2AA0` / `003B2F50` | spawn / remove by id / set parameter |
| `003B2BC0` / `003B2930` | find free / remove by pointer |

## 7. What is not known

- [x] ~~**UQ-208.** The record fields `+0x10`–`+0x27`, and the comparison with `0x13` in `003B2D80`.~~
      **ANSWERED 2026-09-17 (FABLE): the four fields are the spawn call's four arguments, stored and never read back.** `003B2D80(a, b, c, kind)` writes `+0x10 = a`, `+0x14 = b`, `+0x18 = c`, `+0x1C = kind` (`003B2E8F`–`003B2E9B`) right after the id, clears bit 0 of the byte at `+0x20` (`003B2E89`) and never touches `+0x24`. At all thirteen spawn sites `a`/`b` are a screen position (the licence board's widget `+0x35C`/`+0x360`, the achievements layout entry's words `+2`/`+4`, `0055CD40`'s literal `(0, 0)`), `c` is the literal `0`, and `kind` is the effect kind byte, which the spawn also stamps into the instance at `+0x373` (`003B2F13`). No registry routine reads `+0x10`–`+0x27`, and no caller can: the API hands out ids, never record pointers. The `0x13` test is on `kind`: an instance of kind `0x13` gets the double at `00D114B0` - **2.45** - added to its float `+0x304` (`003B2E9E`–`003B2EBA`); no static site passes `0x13`, so only the data-driven kinds (the achievements table, `0055F010`) can reach that arm. Static.
- [x] ~~**UQ-209.** What instance field `+0x338` controls.~~
      ***NARROWED 2026-09-17 (FABLE): writer and value known, reader not.** The only writer is `003B2F50`, and its only callers are the achievements screen's trio, which pass `(0xFF − entry[+1]) × 10000` per spawned effect - a per-entry authored byte scaled by ten thousand, the shape of a duration or phase in the effect walk's units. The element-type pages read `+0x338` of OTHER effect objects as a pointer pushed to the deferred-free queue (`005294B0`~~, `00460120`~~) *(corrected 2026-10-02, OPUS: `00460120`+0x15 releases `+0x338` directly through `003697F0`; only its `+0x3B0` goes to the queue, `00460120`+0x45 `jmp 0024B1C0`)*, so the field's meaning is per object kind and this instance's own reader is the missing half: a displacement census of `+0x338` over the effect walk's bodies, restricted to the `0024B270`-created instance, not done.*
      ***ANSWERED 2026-09-17 (FABLE): `+0x338` is the context's base for the mode dword: an integer added to every element's own mode value when its matrix is installed on the workbench.** Three things fix it. It is initialised from the effect template: the EFX context build `0026F470` copies the template's dword `+0x10` into instance `+0x338` (`0026F6BB`..`0026F6BE`). It is published when a context is made current: `0024FCF0` copies instance `+0x300`..`+0x31F` to `02096820`/`02096830`, `+0x330` to `02096840` and `+0x338` to `02AEE7F4` (`0024FD58`..`0024FD86`), from the three activation callers `0024D050`, `0024D540` and `003B8260`. And it is consumed by exactly one function: `0039B620(value)` adds `[02AEE7F4]` to its argument and stores the sum at `02AEE7F0` (`0039B620`..`0039B626`), which `Workbench_InstallMatrix4x4` `0039B550` (`0039B55F`..`0039B562`) and the transform `0039AFA0` (`0039AFDC`..`0039AFE6`) then copy into the workbench row `022D8F30` as the integer lane the install converts to float. `0039B620`, with fifty-one callers, is reached only from [the element walks](the-element-types-00-0a.md), each passing its own element's mode field (`+0x244` for type `0x01`, `+0x258`, `+0x270`, `+0x284` and others for their types), so every element of a context draws with `mode + base`. The achievements screen therefore shifts each of its thirty effects' mode by `(0xFF − entry[+1]) × 10000`, a per-entry ordering in the mode's units. What the mode dword means once installed is [the workbench page](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)'s unclaimed item, not this field's. Static, writer, publisher, adder and installer bodies read; `+0x338` census over every function.*
- [x] ~~**UQ-210.** Which menu screens own `00557DB0`, `00558FB0`, `00561390`, `00572E10` and the residual trio, and which ids they use.~~
      **ANSWERED 2026-09-17 (FABLE): every function the row names is placed, and the kinds are censused over all eight spawn callers.** *The residual trio and `00572E10` are the ACHIEVEMENTS screen.* `00572920` loops `r14` over **0–29** (`00572A12 cmp r14d, 0x1E`) - the thirty achievement indices - calling `00576E10(index)` (a kind-7 flag query on the save block through `003154B0`) and `003165B0`, the thunk of the handbook per-achievement value `UQ-274` reads, to match each index to a layout entry; then it spawns one effect per matched entry with the entry's position words `+2`/`+4` and kind byte `+0x16`, and sets `(0xFF − entry[+1]) × 10000`. Nothing but the achievement system has a thirty-entry index space keyed by `003165C0`. `005734C0`/`00573690` repeat the refresh loop; `00573980` and `00572E10` (which also calls the reset) are their callers - in player terms the menu that shows the achievements, the Sky Pirate's Den (that name is game knowledge, the placement is the code). *The licence board owns the rest:* `00557DB0`, `005588C0` and `0055CD40` call the `BattleStats_*LicenseBoardSelector*` API; `00558960` is called only by `00558A10`, itself called only by `00557DB0`, and reads the same widget fields `+0x35C`/`+0x360`; `0055B560` is called only by `0055CD40` and `0055DBD0`, both selector-API users; `00558FB0` and `00561390` load the `lic_*` effects (2026-09-16). *The kinds - the fourth spawn argument, `+0x1C` of the record:* licence board `0x1A`, `0x1B`, `0x1E`, `0x1F`, `0x23` and a per-node byte `+2` (`005581E2`, `005585EA`, `005588F7`, `005589D9`, `0055D11F`, `00558228`/`005589A4`); achievements the layout entry's byte `+0x16` - authored data. The third argument is `0` at every site. *One spawn caller the row did not name stays unplaced:* `0055F010` (recursive; kinds from a loop variable and `00556590`), whose chain `0055EF10 → 0055F3E0 → 0055E9E0` carries no string and no named callee. Registry ids themselves are runtime-assigned (`(count & 0xFFFFFFF) | bit 30`, `003B2DF6`–`003B2DFB`) and held in widget fields, so *which ids* is answered by the kinds. Static.
- [x] ~~Whether type-4 EFX contexts are used anywhere besides this registry.~~ **Answered 2026-09-14 (FABLE): not by any direct
      call in the image.** A census of every `E8`/`E9` call (`tools/rawcalls.json`) shows:
      - `0024C460` has **17** calls, passing types 1, 2, 3, 5, 6, 7 and 9. Type **4** is passed only at `003B28F9`,
        `003B2A2D` and `003B2BAD`.
      - `0024C550` has **5** calls, passing types 2, 3 and 4, and 4 only at `003B2A37` and `003B2BBB`.
      - The six EFX context builds through `0024B3A0` write template byte `+0` = 2 (`0026FC6C`), 1 (`002FC541`),
        5 (`003B0730`), 7 (`003B2250`), 4 (`003B2A60`) and 3 (`003B3977`).

      All three type-4 sites are this registry's own family: `003B29B0` (reset and load), `003B28F0` (34 B; called from
      `0055D605`, `0055D6DB`, `0055F512`, `00573A2C`) and `003B2B40` (80 B; called from `0055900D`, `00561413`,
      `00573A3B`), the same menu-range callers as §2.3. The two neighbours' bodies were not read beyond the type argument.
      A computed call is outside this census.

## 8. Evidence

- **Tier 1 disassembly throughout.** Callers come from the raw E8/E9 index. The registry's reference census is a
  rip-relative scan of `02EBDBC0`–`02EBE5C0`, which finds exactly ten functions: the six above plus `003B28F0`, `003B2B40`, `003B2CA0` and `003B2CE0`, whose roles are not read *(answered for `003B2CE0`: the call-free menu-effect classifier below; 2026-10-02, OPUS)*.
- **The type-4 template byte** matches the constructor table on [EFX and EFB effect containers](efx-and-efb-effect-containers.md).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Resource — SERVICE (SWE2-CONTRACT 2026-09-15, 8 edges).** `003B8260` calls `ResourceTable_ResolveEntryByIndex`
`002ED570` — the registry resolves its effect entries through the resource table (the substantive
edge); `00558FB0`/`00561390`/`00572E10` call the generic helpers `00249580`/`002493D0`/`0024A5A0`/
`00249210`. One real resolution call plus helper fan-in.

**Items_Equipment_Shops_License — CLIENT (6 edges, five accessors read).** `00557DB0`, the screen
handler on this page, asks the licence layer which licence-board channels a unit has in play, and
turns the answer into a bitmask. At `0055809B` it takes the unit index from `[rdi+0x60]`, calls
`00323670` `BattleStats_GetLicenseBoardSelectorA`, and — unless the answer is the `0xFF` sentinel —
folds `1 << selector` into `[rbp+0x364]`; at `005580B8` it does the same with `00323630`
`…SelectorB`. `005588C0` reads selector A again. All five accessors index the battle-unit array at
`[02EBF190] + 8` with stride `0x1C8`, refuse an index above `0x27`, and gate on `byte[+5] == 0` and
`byte[+4] <= 6`; the getters return `byte[+0x1C3]`, `byte[+0x1C4]` and `byte[+0x1C5]`, the setters
bound the value at `0x0B`. **The two setters each write the active-selector byte `+0x1C5` as well as
their own**, so "which selector is active" is not settable on its own — it is a side effect of
setting A or B. The crossing is that this screen reads that record; it does not own it. Read from
the shipping bytes 2026-09-14 (OPUS).



**ActorEntity — CLIENT (1 edge).** `0032E520` on this page is consulted by that layer - fan-in, not an actor relationship. Read from the shipping bytes 2026-09-19 (SWE2-EC7).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Several subjects cited by the EC7 update sections are generic: `0032E4D0`, `0032E520` and `0032E590` work on the 64-slot, `0x80`-stride keyed table at `022C31C0` (live test, busy query or drain, and slot advance), and `00249210`, `00249410`, `00249580`, `0024A480`, `0024A680`, `0024EE10` and `0024F410` are effect-object helpers; most edges below are other layers using them.*

**Audio — SERVICE (1 edge).** The activation caller `0024D540` calls `003B3D20`, a 225-byte Audio-filed body gated on the byte `02EBCC80` (read only at its head here). The registry's activation path also services one audio routine each time it runs; what that routine plays is not read here.

**CombatAction — CLIENT (5 edges).** `002FC3C0` (183 bytes) calls `0032E4D0`, `0032E520`, `0032E590`, `0024F410` and `0024EE10` in that order. An action-layer body runs the same live-test, drain, advance and release sequence on its own keyed slot and effect instance that the registry body uses; it shares the machinery, not the registry's records.

**CoreRuntimeScheduling — CLIENT and SERVICE (5 edges).** `0024D540` is called by `MainLoop_UpdateAndRenderFrame` `0022B8C0` and its sibling frame `0022BC20`, and calls `00229EA0`, an 8-byte getter returning the signed master-tick state byte at `02064AD3`; the boot frame `0022B6E0` and the init frame `0022B7E0` call `0032E520`. The frame loop drives the activation caller once per frame, which reads the master tick's state, and the start-up frames query (or drain) the keyed-slot table.

**Input — CLIENT and SERVICE (9 edges).** `00291D90` (625 bytes) calls `0024A440`, `0024A680` and `0032E4D0`; the list splice `0032E070` calls `0035E810` (an 8-byte getter of the pointer at `022CA5E0`) and `0046DD50`; the rect commit `00368360` calls `001E0A10`, `001E0E30` (which fetches `InputManager_GetSingleton` and jumps on) and `001E0E50`; `0055F3E0` calls `002D6620`, which sets the byte `02F973A2` to 1 and the qword `02F973A4` to −1. An input-filed body creates and releases effect objects with the same helpers, and the splice, the rect commit and the registry's spawn chain reach small Input-filed bodies (one fetches the input-manager singleton, one resets two globals) — the same crossing §7 already names for `0055F3E0`.

**PlatformOnlineAchievements — SERVICE and CLIENT (5 edges).** The bit-7 predicate `00576E10` calls `003154B0`, which calls the bestiary-byte reader `00315420`; `003165C0` is called by the counter updater `00315E90`, `003162E0` and `AchievementCounter_UpdateAndMaybeFire` `00316A50`. The achievements screen that drives the registry's residual trio keys its thirty entries by the achievement layer's own flag query and per-achievement value, which that layer's counter updaters also read.

**SaveLoad and Save_Load_Settings — CLIENT (11 edges).** `00582790` (197 bytes) calls `00249580`, `00393460`, `00249210` (twice) and tail-jumps to `00249410`; `00280140` calls `0032E4D0`; and the commit `00247510` is called by `SaveLoad_FullImageStorageCompletionCallback` `00580840`, `SaveSlotScan_ControllerCallback` `005819F0`, `SaveSlotProbe_StorageCompletionCallback` `00581B70`, `SaveLoad_ControllerLifecycleHandler` `00582860`, `0057E950` and `0057EBB0`. A save-layer body binds and queries the shared effect object with the same get-bind-query-release shape as the achievements pane's init (SWE2-EC7-106 update), and the save and slot-scan callbacks call the same commit `00247510` the page cites; this is shared UI-effect machinery, not a save route into the registry.

**Script_VM_Native_Bridge — CLIENT (4 edges).** The verb bodies `0034DB30`, `0050D0C0`, `0050D9A0` and `0050E1E0` call `0032E520`. Script verbs ask whether the keyed-slot table is busy (or drain it); that is fan-in on a generic wait, not a script route into the registry.

**World and WorldAreaField — CLIENT and SERVICE (4 edges).** `003C63A0` (122 bytes) releases the object it keeps at `02B457F0` through `0024A680` and creates a new one through `0024A480`; `003154B0` calls `FieldData_GetVariable0` `00265270`; `WorldTransition_StageFieldTransition` `003145E0` calls `0032E520`. A world-filed body recycles an effect object with the same helpers, the achievement flag query reads a field variable, and staging a field transition waits on the keyed-slot table.

### Interior citation — frontier hub `0024EE60` (2026-09-18, SWE2-EC7)

`0024EE60` — 113 B, 13 callers: the linked-record release `003B2AA0` runs. The
`byte[rcx]` kind indexes a head table at `020910F0`-region; the walk follows
`[+0x348]` next-links to the target, then splices — `[prev+0x348]`/head cell
updated, and the found node's own `+0x348`/`+0x350` back-link pair rewired at
[`0024EE92`](../../_index/ADDRESS-INDEX.md). The remove-by-id path the registry
table describes, verified as the doubly-linked unlink.

Cross-subsystem note: the registry's `0055F3E0` additionally calls into Input
(one edge) — the input-adjacent consumer alongside the effect paths.
## SWE2-EC7-31 update (2026-09-18) — `0024C550` indexed list drain

`0024C550` (138 B) is the per-kind teardown the registry exposes:
`ecx` in 1..9 (`ecx-1 <= 8`) indexes a four-arm jump table at
`0x12C5DC` whose precondition calls are `002FBEF0`, `003B0130`,
`003B1310`, `00374930`; then the `020910A0 + ecx*8` bucket's
`+8`-linked list is drained through `0024F410` per node, the slot
head cleared, and a tail `jmp 0024C460` finishes. Interior anchor
`0024C5B4` (the `call 0024F410` per-node release).

## SWE2-EC7-39 update (2026-09-19) - `003B1310`

`003B1310` (434 B) is a menu-effect registry body - `02EBE5E0`/`02EBEBB0`/`02EBEBE0`/`02EBEBE4` fields, `0032E4D0` pair plus `0036C1D0`/`0032E520`/`003B21E0`/`0032E590`/`0024F410`/`0024EE10`. Interior anchor `003B1336` (a `0036C1D0` call).

## SWE2-EC7-46 update (2026-09-19) - `0024D050`

`0024D050` (233 B) is a body - `0024FCF0`/`003A7420`. Interior anchor `0024D102` (a `0024FCF0` call).

## SWE2-EC7-47 update (2026-09-19) - `00558A10`

`00558A10` (215 B) is a body - `00558960` single call. Interior anchor `00558A4A` (the `00558960` call).

## SWE2-EC7-50 update (2026-09-19) - `0024F410`

`0024F410` (185 B) is a body - `0024F4D0`/`003697F0`/`003A75B0`/`003A7D30`/`003A9600`/`003A9950`/`003A9EE0`. Interior anchor `0024F465` (a `0024F4D0` call).

## SWE2-EC7-51 update (2026-09-19) - `002FBEF0`

`002FBEF0` (173 B) is a body - `0024C460`/`0036C1D0`. Interior anchor `002FBEFC` (a `0024C460` call).


## SWE2-EC7-64 update (2026-09-19) - `003A7D30`

`003A7D30` (140 B) is a `02EBEFA0`-family body - `003697F0` single call plus `02F97340`. Interior anchor `003A7D4F` (a `003697F0` call).


## SWE2-EC7-67 update - `003B2CE0`

`003B2CE0` (129 B) is a call-free menu-effect classifier - `02EBDBC0`-`02EBE5C0` `0x28`-stride `[rax]==ecx` scan, `word[+0x378]&0x100` gate, `byte[+0x370]`<=6 jump-table -> 2/3/5/4, else 1, not-found 0. Interior anchor `003B2CF3` (the `0x28`-stride scan loop).

## SWE2-EC7-80 update (2026-09-20) - `005738D0` + `00572890` measured

`005738D0` (164 B) is the bit-24 propagate on `[02CA9718]`: `bl` goes
to `byte[*(0209AC30) + 0xDEA]` and `00247920(edx)` runs; then each of
`[+0x110]`, `[+0xE8]` (via `00247730(rcx, ebx)`), and `[[+0xF8]+0xE0]`
gets `+0x40` bit24 rewritten to `(ebx & 1) << 24` when non-NULL;
`0028F570()`'s result takes the same `00247730` tail.
Interior anchor `005738E7` (the `00247920` call).

`00572890` (134 B) is the sibling lazy-create: `[+0x110]` NULL runs
`002CCCA0(&00D236E0, 0xC8)` then `002CD150(rax, 0x37)` to build and
init the child; either way `+0x40` gets `| 0x1000000` (the same bit24
`005738D0` toggles), `byte[rbx+0xCA] = 0xC`,
`00247510([rbx+0xC0], 0xF, 0xB)` commits and `byte[rbx+0xC9] = 6`.
Interior anchor `005728B6` (the `002CCCA0` create call).

## SWE2-EC7-81 update (2026-09-20) - `00561E90` + `00561020` measured

`00561E90` (136 B, stack-cookie) is the `+0x578` lazy-create:
a NULL slot runs `00244F50(0xC8, 005595E0, &args)` carrying the
owner pointer, then `00246AD0([0208EA28], rax)` registers it.
Interior anchor `00561EEA` (the `00244F50` call).

`00561020` (217 B) is the seven-child release: `+0x108`, `+0xE8`,
`+0xF8`, `+0x100`, `+0xF0` each get `0024A680(rcx, 1)` when live and
are zeroed; `+0x110`, `+0x118` get `003697F0` and are zeroed - the
screen object's child sweep.
Interior anchor `0056103E` (the first `0024A680` call).

## SWE2-EC7-90 update (2026-09-20) - `003B21E0` + `003B0130` measured

`003B21E0` (54 B) is the keyed reset the registry callers run:
`0032E4D0(dword[+0x18])` returning 1 leaves the record alone (0
out); otherwise `dword[+0x0]` and `dword[+0x1C]` are zeroed and
`02EBEBE4` is cleared - returning 1.
Interior anchor `003B21EC` (the `0032E4D0` call).

`003B0130` (84 B) is the table init the registry callers run:
`0024C460` fires for indices 5, 6 and 9, then all 36 `02EBEC08`
slots have their key dword and `+8` pointer zeroed - a full
clear of the same table `003B0BF0` scans.
Interior anchor `003B0139` (the first `0024C460` call).

## SWE2-EC7-91 update (2026-09-20) - `0032E590` keyed slot-state advance measured

`0032E590` (129 B) is the slot advance the registry callers run:
`ecx` is masked to `& 0x3F` and indexes a 0x80-stride 64-slot
table whose `+0x64` dword must echo the key; the body clears
`+0x40`, calls `003697F0(dword[+0x24])` when `byte[+0x21]` is not
`0xFF`, then dispatches on `byte[+0x20]` - states below 2 tail
through `0032E2F0` into `0032EC40`, state 3 is rewritten to 4,
and state 4 is left alone.
Interior anchor `0032E5CB` (the `003697F0` call).

## SWE2-EC7-94 update (2026-09-20) - `0032EC40` measured

`0032EC40` (147 B) is the doubly-linked-list splice `0032E070` and
`0032E590` (the 64-entry transition helper measured in batch 56)
run: the node's `+0x10`/`+0x18` pair is unhooked from its current
neighbours in both directions, the two `02CD4Bxx` global heads are
patched to cover the removal, `+0x18` is cleared, the node is
pushed onto the `+0x10` free chain with `+0x64 = -1`, and it tails
`0016D6A0(0)` - the effect-record retire path.
Interior anchor `0032EC84` (the forward-link repair store).

## SWE2-EC7-99 update (2026-09-20) - `002CDEA0` measured

`002CDEA0` (120 B) is the post-if-free `00557DB0` and
`0055CD40` call: when `0209AC30`'s `+0x2E8` object is
already present it returns 0; otherwise command `0xE0`
posts with record `{0, movsxd(ecx), movsxd(edx)}` and
code `002CDF20` through `00244F50` - the vacant-slot
message post the registry arms issue.
Interior anchor `002CDF01` (the `00244F50` call).

## SWE2-EC7-102 update (2026-09-20) - `00295D20` measured

`00295D20` (39 B) is the three-call command sequence
`0055E9E0` and `00565E00` run: `0029E750(0xC8)`, then
`0029E330` on the argument, then a `0029E730(0, 0)`
tail - the id-then-verb-then-close idiom the
effect-registry paths share.
Interior anchor `00295D2D` (the `0029E750`
call).

## SWE2-EC7-106 update (2026-09-20) - `0024A4E0` measured

`0024A4E0` (177 B) is the
`0208F580`-pool slot claim
`002467A0`, `00249380`, `002493D0`,
`0024A440`, `0024A480` and `00280750`
call: the `0x48`-stride entries are
scanned (unrolled four at a time,
`0x40` total) for the first with
`byte[+0x38]` bit 5 clear; a full
pool answers 0. On a hit, a non-null
`rcx` is string-copied into the
entry, else two qwords are zeroed;
`dword[+0x38]` becomes
`(+0x38 & 0x3FF10) | (edx & 0xF) |
0xA0`, `+0x28` and `+0x40` are
zeroed, and `dword[02090780]` is
incremented - the allocator the
menu-effect registry shares.
Interior anchor `0024A4F3` (the first
`byte[+0x38]` probe).

`00576E10` (28 B) is the bit-7 predicate `00572920` (the achievements-screen residual) runs: returns `003154B0(cl, 7)` != 0 — a one-argument flag test against bit 7 of its bank byte.

Interior anchor `00576E19` (function `00576E10`).

`00573690` (562 B) is the keyed page-switch `00573980` invokes: scans the `this+0xD8` stride-0x80 entry table under `+0xCC` for the lowest `[ent]` byte and stores the arg-min index into `+0xCB`; both the outgoing and incoming `+0xD0 + page*0x80` blocks then run the destroy-create-fade cycle — `003B2AA0` releases the live `[+0x10]` id, `003B2D80(+2, +4, 0, byte[+0x16])` / `byte[+0x17]` recreates it, `003B2F50(id, (0xFF - byte[+1]) * 0x2710)` sets the fade, and each `[+0x18]` sub-entry at `+0x30` stride 0x18 repeats the pattern; `+0x11D0` bit 2 marks the swap. `+0xCB == 0x1E` skips everything.

Interior anchor `00573745` (function `00573690`).

`005734C0` (464 B) is the explicit-page twin of `00573690` that `00572E10` runs: no min-key scan — `dl` is written to `+0xCB` directly; the same `+0xCB != 0x1E` gate and out/in `003B2AA0`/`003B2D80`/`003B2F50` destroy-create-fade over both `+0xD0`-based page blocks, old page on `+0x16` params, new on `+0x17`.

Interior anchor `00573504` (function `005734C0`).

`005733F0` (197 B) is the current-page rect commit `00572E10` runs: `+0xCB != 0x1E` gate; `+0x11D0` bit 2 is consumed into a stack flag (cleared, flag=1 when previously set); the current entry `[this+0xD8 + cb*0x80]`'s `+2`/`+4`/`+6`/`+8` words build `{x, y, x+w, y+h}` at `[rsp+0x20]`; `00368360(&ctx)` commits it and `00368A60(2)`/`00368A60(0)` follows on whether the entry's `+6` width word is positive.

Interior anchor `00573451` (function `005733F0`).

`00572D80` (141 B) is the pane's effect-object init `00572E10` runs: `00249580()` yields the shared object; `00393460(obj, 00D23668, this+0x11F0, 1)` binds the `+0x11F0` field; a successful `002F8040(0x18)` gate runs `002491B0(obj, 0x18)` and sets `+0x11D0` bit 1; `00249210(obj, 7, 0xC9, 3, {0})` queries a slot whose `+8` is stored at `this+0x1200`; tail-calls `00249410(obj)`.

Interior anchor `00572D92` (function `00572D80`).

`00572BD0` (423 B) is the directional nearest-entry pick `00572E10` runs for navigation: `+0xCB != 0x1E` gate; the current entry `[this+0xD8 + cb*0x80]`'s `+2`/`+4` words become the float origin; each other `+0xCC`-count entry's `+2`/`+4` point passes a `dl`-selected half-plane filter (the four compare arms) before `003BD6F0(&origin, &cand, &out)` measures it — the argmin rides in `edi`/`xmm6`; returns the winning index, -1 when nothing survives.

Interior anchor `00572D12` (function `00572BD0`).

`0024EEE0` (163 B) is the record registration `0024EE60` runs: `rcx` stores at `02F97348`, `+0x120` at `02EBEF98`, `+0x130` at `02EBEFB0` and `+0x1B8` at `02EBEF88` around `003A81E0`/`003A72E0`/`003A8D70`; then `[rcx+0x380]` either enters `00182CA0` when table word `0209216A` reaches `0x100` or enqueues into the `02091950` slot array, and `003697F0` closes

Interior anchor `0024EF06` (function `0024EEE0`).

`003A9950` (156 B) is the teardown `0024F410` runs on the menu-effect bank: with `02F97340` byte `+3` bit `0` set it `003697F0`s the `[+0x878]` record (when `+2` bit `2` is clear) and clears the slot; otherwise it walks the `02EBEF78` table's `0x1800` bytes freeing each live entry, then tail-frees `02EBEF78`'s own head

Interior anchor `003A99B3` (function `003A9950`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-menu-effect-registry-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00374930` | 28 B | stores 0 to the dword at `02EBFA48` and every `0x70` bytes after it while the address is below `02EC0848` (signed compare), 32 dwords in all | `00374940`, `00374942`, `00374946`, `00374949` |
| `003A7420` | 56 B | for byte offsets 0 to `0x78` in steps of 8 (16 slots), re-reads the pointer qword `02EBEFB0` and calls `00332FA0` on the qword at that offset of its target when the qword is non-null | `003A7430`, `003A7437`, `003A7440`, `003A7449` |
| `00460120` | 80 B | calls `003697F0` on qword `rcx+0x338` and then on qword `rcx+0x3D0`, each only when non-null; then, when bit 0 of byte `rcx+0x3C0` is set and qword `rcx+0x3B0` is non-null, tail-jumps `0024B1C0(qword rcx+0x3B0)`, otherwise returns | `00460135`, `00460146`, `0046014B`, `00460165` |
| `0050D9A0` | 84 B | calls `00267E10(r9)`, `00254CB0(1)`, `00266D00()`, `002EF300` with the `00267E10` result, `0032E520(0)`, `00254CB0(0)` and `0036FCC0()` in that order, then `0026B8E0(k)` for `k` 0 to 3 | `0050D9A9`, `0050D9C1`, `0050D9C8`, `0050D9E2`, `0050D9E9` |
| `005294B0` | 63 B | calls `0024B1C0` on qword `rcx+0x338` when it is non-null; then, when bit 0 of byte `rcx+0x3C0` is set and qword `rcx+0x3B0` is non-null, tail-jumps `0024B1C0(qword rcx+0x3B0)`, otherwise returns | `005294B9`, `005294C5`, `005294CA`, `005294E4` |
| `0057E950` | 238 B | with `rbx` set from `r8d` (zero-extended): for `ecx` 4 with `edx` zero and bit 1 of byte `rbx+0xC0` set, calls `00393630(stack buffer, 0x40)` and, only when qword `02CA99C0` is non-null, copies that NUL-terminated buffer to `+8` of a stack record whose first dword is 5 and calls `00582540(qword 02CA99C0, record)`; for `ecx` 5, or 4 when `edx` is non-zero or that bit is clear, calls `00247510(qword rbx+0xC8, 0x1D, record)` with a record of dword 0xD, byte `+0x39A` of `[02CA99C0]` (0xFF when that qword is null) at `+4` and `edx` at `+8`, then clears bit 0 of dword `rbx+0xC0`; any other `ecx` does nothing | `0057E96E`, `0057E9B1`, `0057E9E9`, `0057EA19`, `0057EA1E` |
