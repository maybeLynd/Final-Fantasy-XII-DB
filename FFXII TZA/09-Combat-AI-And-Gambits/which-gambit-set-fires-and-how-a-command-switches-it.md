---
system: Which gambit set fires, and how a command switches it
category: 09-Combat-AI-And-Gambits
status: AUDITED — the four order sets, the switch commands and the stance flip read; what clears bits 50/51 (00307C70 on the animation predicates, and the cancel-and-reset) and the 0030F760/003105D0 bodies read 2026-09-18; 0x414D (Z-14) answered 2026-09-12
owner_layer: PrimaryOwner:CombatAI
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 23 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-which-gambit-set-fires-pass-1
  crossref_clean: true
  reopened_count: 0
---

# Which gambit set fires, and how a command switches it

This document exists because of a **field**, not a function. `unit + 0x6B5` is touched by exactly four
instructions in the whole image, spread across **three heavily documented battle functions that no
document mentions together**. It is the stored **subgroup index** — the value that
[`gambit-evaluation-and-enmity.md`](gambit-evaluation-and-enmity.md) names `subgroup_index` in the
gambit walk's signature but never traces to a source.

**Extents checked**: `00236A60` 452 B ends `ret`; `002FDDA0` 1937 B, 25 returning arms decoded from
three jump tables; `00305AB0` 517 B, 138 instructions, ends `ret` at `00305CB4`.

## 1. What the player sees

A unit that is free to act asks *what do I do next?* — and the engine does **not** consult one gambit
list. It tries **four order sets in a fixed order** and takes the first that yields a committable
action. Only **one of the four** consults the unit's selected subgroup; the other three are always
forced to subgroup 0.

Two consequences a player can feel:

- **A set that is present but produces nothing does not simply "pass".** If the third set
  (`+0x6F8`) exists and fails to commit, the engine **clears it and skips the subgroup-selected set
  entirely** for that decision, dropping to the last set. The unit's chosen bank is not consulted.
- **A unit that reaches the end of all four with nothing still acts.** When the resume flag is
  clear, it commits a hardcoded action, id **`0x4021`**, from a static record. **There is no path
  where the unit is left with no decision.**

## 2. Native mechanism

### 2.1 The four attempts, in order

`BattleUnit_SelectAndCommitNextAction(unit, resume_mode)`. After the player-command pre-empt already
documented in `gambit-evaluation-and-enmity.md` section 8h, the AI cascade is:

| # | site | order set | subgroup passed |
|---|---|---|---|
| **A** | `00305BA5` | `[unit + 0x6E8]` | `0` — `00305B9F xor r8d, r8d` |
| **B** | `00305C1A` | `[unit + 0x6F8]` | `0` — `00305C14 xor r8d, r8d` |
| **C** | `00305C58` | `[unit + 0x6E0]` | **`byte [unit + 0x6B5]`** — `00305C34` |
| **D** | `00305C71` | `[unit + 0x6F0]` | `0` — `00305C6B xor r8d, r8d` |

Each is `BattleUnit_TrySelectAndCommitAiOrderFromSet` (`00305CC0`); a non-zero return jumps to the
epilogue at `00305CA0` and the cascade stops.

**B's failure skips C.** This is the load-bearing control-flow detail and it is not obvious:

```asm
00305C0C  test  rdx, rdx
00305C0F  je    0x305c61          ; B's set is null -> straight to D
00305C1A  call  0x305cc0          ; B
00305C1F  test  eax, eax
00305C21  jne   0x305ca0          ; committed -> return
00305C23  xor   eax, eax
00305C25  mov   qword ptr [rbx + 0x6f8], rax    ; clear the set
00305C2C  mov   dword ptr [rbx + 0x748], eax
00305C32  jmp   0x305c61          ; -> D, NOT C
```

**C is reached only from the three guards at `00305BF1`, `00305BF9` and `00305C03`** — that is, only
when B was never attempted because a context test failed. So the subgroup-selected set is consulted
**only when the `+0x6F8` set is not eligible in the first place**, never after it has been tried.

### 2.2 The final fallback commits a hardcoded action

```asm
00305C7A  test  edi, edi                        ; resume_mode
00305C7C  jne   0x305ca0                        ; resuming -> just return
00305C7E  movzx r8d, word ptr [rip + 0x1be6612] ; = word [01EEC298] = 0x4021
00305C86  lea   rdx, [rip + 0x1be660b]          ; = 01EEC298
00305C90  mov   dword ptr [rsp + 0x20], 1
00305C9B  call  0x30f760                        ; BattleUnit_CommitAction
```

**`0x4021` is the only literal action id in the function** and it is committed unconditionally when
all four sets fail and `resume_mode == 0`.

### 2.3 Two order sets are compiled into the image

Two branches bypass the unit's own pointers and hand a **static** order set to the C and D call
sites, each with the subgroup forced to 0:

| site | static set | enters at |
|---|---|---|
| `00305B89` `lea rdx, [rip + 0x1be6790]` | `01EEC320` | `00305C68` (D's call) |
| `00305BDE` `lea rdx, [rip + 0x1be678b]` | `01EEC370` | `00305C52` (C's call, `r8d` zeroed at `00305BDB`) |

**Both decode cleanly under the layout `gambit-evaluation-and-enmity.md` derived from code alone** —
see 4.2. That is an independent confirmation of the header/record geometry from data the code never
describes.

## 3. Key addresses

| Address | Name | Size | Verified |
|---|---|---:|---|
| `00305AB0` | `BattleUnit_SelectAndCommitNextAction` | 517 B | read here (previously listed "not read") |
| `002FDDA0` | `BattleUnit_ExecuteDirectStateCommandOrder` | 1937 B | read here |
| `00236A60` | `BattleUnit_ResetStateForReuse` | 452 B | read here |
| `00305CC0` | `BattleUnit_TrySelectAndCommitAiOrderFromSet` | 422 B | read previously; re-read for arg 3 |
| `0020E600` | `ImageAddress_ResolveRuntimePointer` | 10 B | read — complete body in 4.3 |
| `0030F760` | `BattleUnit_CommitAction` | 570 B | **read 2026-09-18 (FABLE).** `(unit, params, actionId, targetHandle, cancelFirst)`: with `cancelFirst` it runs `BattleUnit_CancelAndResetCurrentAction` first; resolves the target through `BattleUnit_ResolveByFocusHandle`; for an id up to `0x21E` it resets the target buffer `+0x778` (`BattleTargetBuffer_ResetPreservingFlag0`) and appends the target's actor work, for the direct-state band `0x4000`..`0x4166` it appends nothing, and any other id returns 0 (`0030F7A1`..`0030F7EC`). It then installs the command: `+0x700 &= ~3`, `+0x708` = params, `+0x710` = target handle, `+0x714` = id, `+0x6B4` = 0, and copies the sixteen bytes at `+0x700` and the eight at `+0x710` into the previous-command slots `+0x718` / `+0x728`; `+0x770` is cleared unless the same id and target repeat (or the definition's `byte +5` says so); a pending `+0x6B0` bit 1 is consumed into `+0x6B9` from the table `022C1DB8[+0xEA9 × 12]` with `+0x6B6` = 1; `+0x750` is cleared when `+8` differs from `+0x24`. For a targeted id up to `0x21E`, `BattleTarget_ClassifyRelationshipClass` above 1 stores the handle in `+0x754`, and when the unit's `+8` equals its `+0x24` the same handle is broadcast into `+0x754` of every unit sharing that `+0x24` that is not in a terminal status the field does not keep (`0030F8DD`..`0030F931`), then into `+0x750`; finally, unless unit flag bit 22 is set, the unit's lane bit (`1 << +0xEA9`) is added to the target's `+0xEA4`, the target's `+0xEA8` attacker count incremented, and `BattleUnit_BroadcastPartyCombatTargetRelation(unit, target, 1)` called. Returns 1. |
| `003105D0` | `BattleUnit_CancelAndResetCurrentAction` — writes `+0x6B4`, `+0x6B6`, `+0x6B7` | 418 B | **read 2026-09-18 (FABLE).** For a unit with a definition: `BattleUnit_ReleaseTargetRelationAndActionState`, `+0x6B6` = 0, the two presentation slots `+0x695` / `+0x696` released through `BattleAction_ReleasePresentationSlot` and set to `0xFF`, `BattleAction_RefundReservedExecutionResources`, then the flag qword `+0` loses bits 12, 13, 29, 31, 35 and 46 and `+4` loses bits 7 and 21 (`0031063F`..`00310651`), `+0x690` = 0, and a second mask clears **bits 24, 50 and 51** (`0031066F`); every unit's `+0xEA0` loses this unit's lane bit; the target buffer is reset, the previous-command slots are copied on to `+0x730` / `+0x740`, `+0x700 &= ~3`, `+0x6B7` (word) and `+0x6B4` cleared, `+0x768`, `+0x760`, `+0x6D8`, `+0x6D0`, `+0x75C` zeroed, `+0x714` = `0xFFFF`, `+0x708` and `+0x710` zeroed, `BattleLocomotion_ResetPathAndSetTargets(stats+0x80, 0, 0)`, stats `+0x124` / `+0x120` zeroed, `+0x6D8` / `+0x6D4` zeroed, stats `+0x170` bit 5 cleared, `0033C9B0(stats)`. |

### Data addresses cited by this document

| Address | What | Anchor |
|---|---|---|
| `002FE534` | dispatch target table 1, 6 dwords (RVAs) | `002FDE2C` |
| `002FE54C` | dispatch case-index bytes 1, `0x4C` entries | `002FDE23` |
| `002FE598` | dispatch target table 2, 6 dwords | `002FDFE8` |
| `002FE5B0` | dispatch case-index bytes 2, `0x77` entries | `002FDFDF` |
| `002FE628` | dispatch target table 3, 12 dwords, no index byte | `002FE196` |
| `02EBF168` | authored-table registry slot holding the order-set directory | `002FE060` |
| `01F83530` | runtime base added to a stored 32-bit image offset | `0020E602` |
| `01EEC298` | static **order record**; word at `+0` is `0x4021` | `00305C86` |
| `01EEC320` | static **order set**, 1 subgroup, 2 records | `00305B89` |
| `01EEC370` | static **order set**, 1 subgroup, 1 record | `00305BDE` |

The five `002FExxx` entries above are `.text` addresses that are **not** function entries.
`002FDDA0`'s body is 1937 bytes and ends at `002FE531`; the tables begin at `002FE534` and run
contiguously — `002FE534`+`0x18` = `002FE54C`, `+0x4C` = `002FE598`, `+0x18` = `002FE5B0`, `+0x77` =
`002FE627`, then twelve dwords from `002FE628`. **They tile the gap exactly**, which is what
identifies them as this function's trailing switch data rather than a mis-citation.

## 4. Data structures and formulas

### 4.1 `+0x6B5` is a signed subgroup index, and the walk uses it twice

In `00305CC0` arg 3 is **sign-extended** and then used for two different things:

```asm
00305CCC  movsxd  rax, r8d          ; N = (s64)subgroup_index
00305D30  movzx   eax, byte ptr [r10 + rcx]        ; \  sum bytes [0, N)
00305D37  movzx   eax, byte ptr [r10 + rcx + 1]    ; /  two at a time
00305D89  cmp     byte ptr [r11 + r10], dil        ; count of subgroup N; 0 -> return 0
00305D93  lea     rbx, [r10 + 0x20]
00305D97  lea     rbx, [rbx + rcx*8]               ; rcx = sum*3, so +0x20 + sum*0x18
00305E04  add     rbx, 0x18
```

**`N` is both the number of leading count bytes to sum and the index of its own count byte.** The
loop is an unrolled two-at-a-time sum with an odd-element tail at `00305D4E`; it is exact for
`N = 0`, `N = 1` and `N = 12`.

> **The sign extension is real and unexamined.** Nothing between the four writes and this read
> constrains the byte to be small, and a negative `N` would make `byte [r11 + r10]` read *before*
> the set. Every value the four writers can produce is `0..11` (4.4), so **no reachable path is
> negative** — but that is a property of the writers, not a check in the walk.

### 4.2 The static sets confirm the layout

`01EEC320`, read as bytes:

```
+00  02 00 00 00 00 00 00 00  ...          ; count[0] = 2 subgroup-0 records
+20  96 00 | 00 00 | 00 00 | 01 00 ...     ; record 0: selector 0x0096
+38  25 41 | 00 00 | 00 00 | 00 00 ...     ; record 1: selector 0x4125
```

`01EEC370` is the same shape with `count[0] = 1` and the single record `selector 0x0096`. **Header
`0x20`, records `0x18`, counts leading — every field lands where the code-derived layout says it
should**, and `0x50` is exactly `0x20 + 2 * 0x18`.

### 4.3 The order-set directory is authored data

Arm `002FE025` installs `+0x6E0` from a table, not from a pointer:

```asm
002FE060  mov   rcx, qword ptr [rip + 0x2bc1101]   ; -> 02EBF168
002FE06C  movzx eax, word ptr [rcx]                ; entry count
002FE073  dec   eax
002FE075  cmp   edx, eax
002FE077  jg    0x2fe523                           ; index > count-1 -> unhandled
002FE082  mov   ecx, dword ptr [rcx + rdx*4 + 4]   ; stored 32-bit offset
002FE086  call  0x20e600
002FE08E  mov   qword ptr [rbx + 0x6e0], rdi
```

and the resolver is three instructions:

```asm
0020E600  mov  eax, ecx                          ; zero-extend the stored offset
0020E602  add  rax, qword ptr [rip + 0x1d74f27]  ; + base at 01F83530
0020E609  ret
```

**So an order set is stored as a 32-bit image-relative offset in a registry table** whose slot is
`02EBF168` — a slot adjacent to those identified in
[`../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md).
The directory is `[count:u16][pad:u16][offset:u32 x count]`, bounds-checked against its own count.

### 4.4 The command to subgroup mapping

Arm `002FE0B3` (ids `0x4116`-`0x4121`) is two instructions of arithmetic on the command id itself:

```asm
002FDDB0  movzx edx, word ptr [rcx + 0x714]   ; the pending command id
...
002FE0B8  sub   dl, 0x16
002FE0BB  mov   byte ptr [rbx + 0x6b5], dl
```

**`subgroup = (id & 0xFF) - 0x16`.** For the twelve ids `0x4116`-`0x4121` the low bytes are
`0x16`-`0x21`, so the twelve commands map onto subgroups **0-11** with no gap and no overlap.

> **Twelve commands, twelve subgroups — and section 8l of the gambit document reports a twelve-slot
> config with a sixteen-bit enable mask.** The two twelves agree. **They are recorded as an
> agreement, not as an identification**: nothing read here connects a command id to a config slot,
> and a matching count is the weakest kind of join.

## 5. Call chain

```
BattleUnit_UpdateCombatFrame (00308610)
  -> BattleUnit_SelectAndCommitNextAction (00305AB0)
       -> BattleUnit_TrySelectAndCommitAiOrderFromSet (00305CC0)   x4, sets A..D
            -> AiOrder_EvaluateAndResolveActionTarget (003014C0)
            -> BattleUnit_CommitAction (0030F760)
       -> BattleUnit_CommitAction (0030F760)                       final 0x4021 fallback

BattleUnit_ExecuteDirectStateCommandOrder (002FDDA0)   <- no direct caller; dispatched indirectly
  writes unit->+0x6B5 (subgroup) and unit->+0x6E0 (set)

BattleUnit_ApplyUnitDefinition (0023A570) -> BattleUnit_ResetStateForReuse (00236A60)
  zeroes +0x6B5, +0x6E0, +0x6E8, +0x6F0, +0x6F8
```

### The dispatcher's complete arm map

`002FDDA0` switches on `word [unit + 0x714]` through three tables plus one direct range compare.
**249 ids are handled by 25 returning arms**; everything else reaches `002FE523`, which returns
`-1` and — uniquely — does **not** write `+0x6B4`.

| arm | ids | range |
|---|---:|---|
| `002FDE39` | 2 | `4046-4047` |
| `002FDE7B` | 8 | `4048-404F` |
| `002FDE98` | 1 | `4050` |
| `002FDF18` | 32 | `4051-4070` |
| `002FDF5A` | 32 | `4071-4090` |
| `002FDEC1` | 1 | `4091` |
| `002FDF93` | 64 | `4092-40D1` — reached by `002FDE02 jae`, **not** through a table |
| `002FDFF5` | 64 | `40D2-4111` |
| **`002FE025`** | **4** | **`4112-4115` — installs `+0x6E0`, sets `+0x6B5 = 0`** |
| **`002FE0B3`** | **12** | **`4116-4121` — sets `+0x6B5 = (id & 0xFF) - 0x16`** |
| `002FE0D3` | 8 | `4139-4140` |
| `002FE0FF` | 8 | `4141-4148` |
| `002FE12B` | 1 | `4158` |
| `002FE1A3` through `002FE4FC` | 1 each | `4159`-`4164`, twelve single-id arms |

**Gap:** ids `4122-4138` (23 ids) and `4149-4157` (15 ids) are inside the compared range but reach
the unhandled arm. **`0x414D` — open question Z-14 — is one of them.**

## 6. Modding notes

- **`unit + 0x6B5` is the whole subgroup selector**, one byte, and only four instructions in the
  image write or read it. Poking it changes which bank the C attempt walks and nothing else.
- **Order sets are 32-bit offsets in the table at `02EBF168`, resolved against `01F83530`.** Adding
  a set means adding a directory entry and bumping the `u16` count at `+0`; the bound check at
  `002FE077` reads that count, so it self-describes.
- **`002FDDA0`'s entry guard is `byte [unit + 0x6B4] == 0`** (`002FDDB7`). A non-zero value makes
  every command a no-op that still returns success, so a stuck `+0x6B4` silently swallows commands.
- **The unhandled arm is distinguishable**: return `-1` and `+0x6B4` untouched, versus return `1`
  and `+0x6B4 = 2` for all 25 handled arms.
- **The `0x4021` fallback is a static record at `01EEC298`**, not a table entry — patch the word at
  `+0` to change what a unit does when its whole gambit cascade comes up empty.

## 7. What is not known

- [x] ~~**UQ-122.** **What the four order sets *are*.** Their priority order is read (`+0x6E8`, `+0x6F8`,
      `+0x6E0`, `+0x6F0`); which authored concept each holds is not.~~ **Closed 2026-09-14 (FABLE)**, by the
      role reads below together with UQ-124 and UQ-125:
      - **A** is the static re-plan set: order `0x4022`, follow, for party; `0x414D`, stance flip, for others.
      - **B** is the issued command's set: attack the commanded target.
      - **C** is the unit's own AI list.
        - For a party member it is the gambit list, packed into subgroup 0.
        - For an enemy it is the authored set, whose twelve header counts are the subgroups that orders
          `0x4116`–`0x4121` select.
      - **D** is the static floor: `0x4124`, follow your leader.
      - The final fallback below all four is the never-ending wait `0x4021`. *Roles read from every installer,
      2026-09-12 (FABLE):*
      - **A `+0x6E8` — the re-plan set, installed whenever the unit's combat state is reset.** ~~Installed only by
        `0030F2D0` … and by `BattleUnit_RecoverFromTerminalStatusSetIfClear`~~ *(corrected the same day: six
        installers, from every reference to the two static sets)* — `BattleUnit_EnterPartyCombatStance` (`00313458`),
        `BattleUnit_ExitPartyCombatStance` (`003134DA`), `BattleUnit_SetupEngagedActionState` (`002FED9E`),
        `002FEDC0` (`002FEE05`), `BattleUnit_RecoverFromTerminalStatusSetIfClear` (`0030126B`) and `0030F2D0`
        (`0030F331`), the handler the verbs **`resetemergency`** (`00347970`),
        **`resetemergency_with_animetionmode`** (`003473E0`) and **`resetemergency_one`** (`00346A10`) call. Each
        picks static set `01EEC3C0` for a party-kind record and `01EEC410` otherwise.
      - **B `+0x6F8` — the player-issued command's set.** `BattleUnit_IssueCommand` installs static set `01EEC2D0`
        with the command in `+0x748` (`00311DD4`–`00311DE1`); the stats rebuild when Confuse or Berserk has just changed (`002FF982`–`002FF98E`), the status-transition reset,
        teardown, recovery and the execution timeout clear it (`002FF9CC`, `00300155`, `00300E68`, `0030119C`,
        `0030AFB2`), and the cascade clears it when it fails to commit (`00305C25`, `00305C45`).
      - **C `+0x6E0` — the unit's authored AI variant**, with subgroup `+0x6B5`: from the unit definition
        (`BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit`), from a runtime record `02089378 + i × 0x170`
        (`0023AB7E`–`0023AB9F`, in `BattleUnit_ApplyUnitDefinition`), or from the orders `0x4112`–`0x4115`.
      - **D `+0x6F0` — the static default set `01E09350`** that `BattleUnit_ApplyUnitDefinition` gives every unit
        (`0023ABA6`–`0023ABB5`), saved and restored across action suspension.
      **What the static sets hold** (read from `.data` in the `.ard` set layout — twelve subgroup counts, twenty
      zero bytes, 24-byte records; each set has one subgroup of **one record** and a zero tail):

      | set | address | order | flags | target selectors |
      |---|---|---|---|---|
      | A, party | `01EEC3C0` | **`0x4022`** | `0x2000` (no execution timeout) | none |
      | A, non-party | `01EEC410` | **`0x414D`** | 0 | none |
      | B | `01EEC2D0` | action **`0x0096` = `Attack`** (row 150's bank-0 name) | 0 | one, operand `0x000A` = **relation mode 10, the commanded target** |
      | D | `01E09350` | **`0x4124`** | `0x2000` | none |

      So a party member whose combat state resets runs order `0x4022` first — the order under which the
      "Action interrupted" message is posted and whose locomotion has the fixed-speed escape — while a foe's
      re-plan set names `0x414D`, ~~which the direct-state dispatcher sends to its unhandled arm (return `-1`)~~
      *(corrected again 2026-09-12: the order table itself maps `0x414D` to its own handler — `01EEC460[0x14D]` =
      `002FE840` — so the direct-state sub-dispatcher never sees it)*. Every unit's floor is `0x4124`, one of the ids
      the goal decoder `BattleLocomotion_DecodeOrderGoal` accepts above `0x4035`.

      **What the three orders do (2026-09-12, FABLE)** — the handler table `01EEC460` maps `0x4022` and `0x4124` to
      the movement handler `caseD_4000` (`002FDA60`) and `0x414D` to `002FE840`:
      - **`0x4124` — follow your leader.** The goal is the unit's own `+0x120` vector (a follow goal
        `PartyFollow_ApplyGoal` writes, `00324737`), allowed only while the unit's `+0x24`
        [group leader handle](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) resolves to **another** unit ([the locomotion page](../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md) DE-3).
        `+0x24` is refreshed every maintained frame by `00305E70`: a party-kind unit's is the party's lead
        (`003271E0`), anyone else's is the first active unit with the same team id `+0x54` and team-leader flag bit
        15 — both set by the team verb (`00239170`). So the static default set makes **every unit with nothing
        better to do walk to its place beside its team or party leader**, and a leader's own `0x4124` fails its
        decode. It carries flag `0x2000`, so it is never interrupted by the execution timeout.
      - **`0x4022` — the same follow, for a party member**, with a mode-dependent stop distance
        (`0031289E`–`0031290E`) and the fixed-speed locomotion escape; it is what a party member runs first after
        any combat-state reset.
      - **`0x414D` — flip the combat stance.** `002FE840`, in phase 0, calls `BattleUnit_ExitPartyCombatStance` when
        unit flag bit 23 (in stance) is set and `BattleUnit_EnterPartyCombatStance` otherwise (`002FE884`–`002FE896`);
        enter sets bits 23, 24 and 50, exit clears 23 and sets 24 and 51 (`00313421`, `00313469`; `0031349F`,
        `003134EB`), both re-installing the re-plan set. Phase 1 returns 0 until bits 50 / 51 are clear
        (`002FE8A1`–`002FE8B0`), then completes. So a foe's first order after a combat-state reset toggles its
        stance and waits for the transition. **It cannot flip twice:** phase 0 skips the toggle while unit flag
        bit 24 is set (`002FE864`–`002FE86B`), and both stance functions set bit 24, so the re-installed set only
        advances the phase until bit 24 is cleared — by `BattleUnit_HandleReactionAnimationEvent` (`0032517C`) or
        `003083A0` (`003083A6`), so an animation event re-arms the toggle; `00301140` (`003012A1`) and `00313500` set the
        bit too *(corrected the same day: an earlier wording called those two the clearers)*. ~~What clears bits 50 / 51 is not read.~~ **Answered 2026-09-18 (FABLE), by an image-wide sweep of 64-bit flag masks:** the transition bits are cleared in two places. `00307C70` (called from `00233F70`) clears bit 24 together with bit 50 (`movabs rax, 0xFFFBFFFFFEFFFFFF; and qword ptr [rbx], rax`, `00307CA2`) when `002E7290(unit)` reports the enter transition finished, and bit 24 together with bit 51 (`00307CD7`) when `002E72E0(unit)` reports the exit finished; and `BattleUnit_CancelAndResetCurrentAction` clears bits 24, 50 and 51 at once (`0031066F`). The only setters are the two stance functions above; the other two 64-bit masks that touch those bit numbers (`002D82DD`, `002D8379` in `002D81D0`) act on render transform records, not the unit word. So the stance flip completes when the animation predicate says so, and bit 24's clear rides on the same store.

      - **Set B is "attack the unit you were commanded against".** Its one record is action 150, whose bank-0 name
        decodes as `Attack` (with `Cure`, `Belias` and `Mateus` decoding correctly at rows 0, 262 and 263 as controls),
        and its target selector is relation mode 10 — `BattleTarget_MatchesRelationMode` jump-table slot 10 is
        `0030BE2A`, `candidate[+8] == self[+0x748]` — and `BattleUnit_IssueCommand` stores its target-handle argument
        (`edx`, `00311D16`) at `+0x748` beside installing the set (`00311DD0`–`00311DE1`). So an issued command falls
        back, at priority B, to attacking its target.

      ~~**Still open:** what the `02089378` records are.~~ **Answered by propagation 2026-09-12:** they are the party's
      **gambit sets** — `AiOrderSet` records of `0x170` bytes, twelve 24-byte order records each
      ([the gambit-walk contract](CONTRACT-gambit-walk.md) §3) — so for a party member set C is its own gambit list,
      installed by `BattleUnit_ApplyUnitDefinition` from the party slot index.
- [x] ~~**UQ-123.** What the guards at `00305BF1`, `00305BF9` and `00305C03` test on `[unit + 0x698]` — three byte
      and bit tests on a context object this document does not open.~~ **Answered 2026-09-14 (FABLE):** the
      object is the unit's battle stats record. The guards send a unit to set C, skipping set B, when any of these holds:
      1. **`00305BF1`**: the stats pointer is null.
      2. **`00305BF9`**: the stats kind byte `+0x05` is non-zero, so the unit is not from the party table
         ([the kind byte](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md)).
      3. **`00305C03`**: bit 2 of the stats flag word `+0x00` is set.

      Set B (`+0x6F8`) is therefore tried only for a party-table unit whose bit 2 is clear. The same three tests are
      the predicate `0030BCD0`, which returns 1 on any of them.
      - **Where bit 2 comes from.** Two writers store it through a register at displacement 0, which a displacement
        census cannot see:
        - `BattleStats_InitializeDefinitionRecord` sets it from the party-table row's byte `+0x2C` bit 6
          (`0023AF22`–`0023AF28`,
          [how a battle unit is built](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.5).
        - The area-state party walk sets or clears it from bit 0 of a preset byte (`00239D83`–`00239D94`,
          [the setsavedata presets](../11-Party/the-setsavedata-presets-test-battle-scenarios.md), UQ-129).
      - **The authored bit.** In the party table decoded from `test_battle/us/binaryfile/battle_pack.bin`
        (directory `+0x44`, 40 × 128 bytes), row byte `+0x2C` has bit 6 **clear** only on rows 0 (Vaan), 1 (Ashe),
        6 (Reks) and 26 (Chocobo). It is set on Fran, Balthier, Basch, Penelo, every guest row other than Reks, the
        nine "No name" rows and all thirteen Espers.
      - **Not named:** what the flag means. It is neither a guest mark nor a permanent-member mark, since Fran and
        Penelo carry it and Reks does not. Whether the loaded copy of the table is this file was not re-checked.
- [x] ~~**UQ-124.** Whether the twelve `0x4116`-`0x4121` commands correspond to the twelve config slots in section
      8l. **The counts match; nothing else was read.**~~ **Answered 2026-09-14 (FABLE): no. The two twelves count
      different things.**
      - **A subgroup is a header byte.** `BattleUnit_TrySelectAndCommitAiOrderFromSet(unit, set, subgroup, resume)` treats
        the set's first bytes as per-subgroup record counts.
        - It sums the counts of the subgroups before `subgroup` to find the base record (`00305D24`–`00305D5E`).
        - It walks `[set + subgroup]` records from `set + 0x20 + base × 0x18` (`00305D89`–`00305D97`).
        - The command arm stores `subgroup = (id & 0xFF) − 0x16` into `+0x6B5`, and the set-C call passes that byte
          (`00305C34`–`00305C58`).
      - **A config slot is a line inside one subgroup.** `GambitRuntime_RebuildOrderSetFromConfig` walks the twelve
        4-byte slots in order and emits one 24-byte record for each enabled, non-empty slot. It then stores the emitted
        count into the set's **first** header byte only (`003282A0`). So the player's twelve lines all land in
        subgroup 0, and this writer puts nothing in header bytes 1–11.
      - **Where multi-subgroup sets come from.** For an enemy, `BattleUnit_ApplyUnitDefinition` installs set C from the
        authored row's word `+0x50` through a descriptor table (`0023A94D`–`0023A95E`). For a party member it installs
        the config-rebuilt set `02089378 + index × 0x170` (`0023AB7E`–`0023AB9F`).
      - **So** command `0x4116` selects a party set's whole gambit list, and `0x4117`–`0x4121` select the other
        subgroups, which only an authored set is shown here to fill.
      - **Not read:** whether another writer fills header bytes 1–11 of a party set.
- [x] ~~**UQ-125.** What action `0x4021` is, beyond being the unconditional fallback.~~ **Answered 2026-09-14 (FABLE),
      by propagation: it is the *wait* order.** Its handler is the 106-byte body at `002FE7D0`, which the function
      census lacks ([the handler table](../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md) §5, AT-3).
      - **Phase 0** zeroes the follower focus `+0x750` and advances.
      - **Phase 1** completes once the action age counter `+0x75C` reaches `30 × n`, where `n` is the order record's
        second word.
      - **`n = 0` never completes.** The fallback record `{0x4021, 0, flags 0x2000}` at `01EEC298` is exactly that
        case: the unit idles under an order that never ends, until the next selection replaces it
        ([the locomotion page](../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md), DE-2).
      - Shipped enemy order sets use it 3,018 times, with `n` from 0 to 12.
- [x] ~~**UQ-126.** Why 38 ids inside the compared range reach the unhandled arm.~~ **Answered 2026-09-14 (FABLE):
      none of them does, because the dispatcher never receives them.** The 0x414D case generalises to all 38.
      - **The only route in.** `BattleUnit_ExecuteDirectStateCommandOrder` has no `E8`/`E9` caller and no `rip`
        reference. Its address occurs as a 64-bit pointer exactly 249 times, which is its 249 slots in the order handler
        table `01EEC460`. That table is indexed by `id − 0x4000` and bounded at `0x166`
        ([the handler table](../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md)).
      - **Where the 38 gap ids go.** Their slots in that table point elsewhere:
        - `BattleUnit_AdvanceTargetedMovementOrder`: 25 ids (`0x4126`–`0x4127`, `0x4129`–`0x4138`,
          `0x414B`–`0x414C`, `0x4150`–`0x4154`);
        - the 282-byte handler `002FE660`: 6 ids (`0x4122`, `0x4123`, `0x4149`, `0x4155`–`0x4157`);
        - the goal-following handler `caseD_4000`: 4 ids (`0x4124`, `0x4125`, `0x414A`, `0x414E`);
        - the stance flip: `0x414D`;
        - the 56-byte handler: `0x414F`;
        - a null slot: `0x4128`, which the precondition check rejects (`003018F7`).
      - **So** the dispatcher's compared range spans ids that other handlers own. Its unhandled arm is reached by no
        table slot and serves only as a defensive default.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Three functions take the same structure as arg 1 | `00236A72`, `002FDDAD`, `00305ABE` all `mov <base>, rcx`; `+0x698` q, `+0x6B5` b, `+0x6E0` q agree in width across all three | 1 |
| corroborated by the callee | `00305CC0` receives SelectCommit's pointer (`00305C55`) and reads `+0x698`, `+0x708`, `+0x714` at the same widths ExecDirect uses (`002FDDA6`, `002FDDB0`) | 1 |
| and by a shared callee of Reset | `00236A77` calls `003105D0` with arg 1 unchanged; `003105D0` writes `+0x6B4`, `+0x6B6`, `+0x6B7` | 1 |
| Four attempts in a fixed order | call sites `00305BA5`, `00305C1A`, `00305C58`, `00305C71` with their `r8d` setups | 1 |
| B's failure skips C | `00305C23`-`00305C32`, `jmp 0x305c61` past `00305C34` | 1 |
| `+0x6B5` is the subgroup argument | `00305C34` then `00305C58`; `00305CCC movsxd rax, r8d` | 1 |
| Subgroup drives header sum and count index | `00305D30`-`00305D4E`, `00305D89`, `00305D93`-`00305D97`, `00305E04` | 1 |
| `subgroup = (id & 0xFF) - 0x16` | `002FDDB0`, `002FE0B8`, `002FE0BB` | 1 |
| Order sets resolve from an authored directory | `002FE060`-`002FE08E` plus the complete body of `0020E600` | 1 |
| Reset zeroes the field | `00236B10 xor eax, eax` is the last write to `rax` before `00236BA3` | 1 |
| Static sets decode under the layout | bytes at `01EEC320` and `01EEC370` | 1 |
| The dispatch map | tables at `002FE534`/`002FE54C`, `002FE598`/`002FE5B0`, `002FE628`, decoded against image base `0x120000` (`002FDE1A lea r9, [rip - 0x1dde21]`) | 1 |

**Control on "only four instructions touch `+0x6B5`".** The claim is an absence, and it rests on a
whole-image displacement census over 38,161 functions with a body — the same scan that positively
returns **84** sites for the adjacent `+0x6B4`, **15** for `+0x6B6` and **7** for `+0x6B7`. A scan
that finds those cannot be silently failing on `+0x6B5`.

**Control on the `al = 0` reading in Reset.** The claim is that nothing rewrites `rax` between
`00236B10` and the store. The same pass positively reports the two writes that *do* exist
(`00236A9C`, `00236B10`) and finds no `call` in the interval — a decoded interval, not a search.

> **Scope limit, stated as a rule and not a caveat.** A displacement is only meaningful within one
> structure type. `+0x6F0` and `+0x6F8` have 106 and 157 sites image-wide, but **most of those are
> in the `007Cxxxx` region and are a different structure entirely.** Nothing in this document counts
> a census hit as a battle-unit hit: every offset claim here is anchored to a function proven above
> to hold the same arg-1 pointer.

## 9. Related

- [`gambit-evaluation-and-enmity.md`](gambit-evaluation-and-enmity.md) — the walk itself; this
  document supplies the `subgroup_index` argument it names, and reads the tail of `00305AB0` that
  section 8h left at the player-command pre-empt
- [`../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — the registry family `02EBF168` belongs to
- [`../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`](../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md)
  — `+0x708`, `+0x714` and `+0x6B4`, the fields this dispatcher switches on and sets

## Falsification pass 1 — 2026-09-13 (OPUS)

§3's data table is the checkable core — three dispatch jump tables with exact shapes, each with the
**anchor instruction** that reads it, plus two static records with stated contents. A jump table is
self-checking in a way prose is not: if the index bytes select from six targets, none may be ≥ 6, and
every target must land inside the function.

| claim | measured |
|---|---|
| six stated sizes | **6 of 6 exact** |
| table 1 at `002FE534`: **6 dwords**, index bytes at `002FE54C`, **`0x4C`** entries | 6 dwords, **all 6 land inside `002FDDA0`'s body**; **76 = 0x4C** index bytes, **max value 5** |
| table 2 at `002FE598`: **6 dwords**, index at `002FE5B0`, **`0x77`** entries | 6 dwords, **all 6 inside**; **119 = 0x77** bytes, **max 5** |
| table 3 at `002FE628`: **12 dwords, no index byte** | 12 dwords, **all 12 inside**, and no index table |
| the five anchors `002FDE2C`, `002FDE23`, `002FDFE8`, `002FDFDF`, `002FE196` | **all five land on the instruction named**, each carrying the table's displacement (`0x1DE534` + `0x120000` = `002FE534`, and so on — `r9` is the image base) |
| `01EEC298` word `+0` = `0x4021` | `21 40` — **`0x4021`** |
| `0020E600` is three instructions | `mov eax, ecx` / `add rax, [01F83530]` / `ret` — **10 bytes** |
| §4.2's byte rendering of `01EEC320` | `count[0] = 2`; record 0 `96 00 00 00 00 00 01 00`, selector **`0x0096`**; record 1 `25 41 …`, selector **`0x4125`** — verbatim |
| `01EEC370`: same shape, `count[0] = 1`, single record `0x0096` | exact |

### The layout is confirmed by its neighbour, not only by arithmetic

§4.2 observes that *"`0x50` is exactly `0x20 + 2 × 0x18`"*. The stronger fact is that **`01EEC320 +
0x50` is `01EEC370`** — the second static set begins precisely where the first one ends.

That converts the header and record sizes from a calculation into a measurement. Arithmetic that
merely *fits* a `0x20` header and `0x18` records would fit several other pairs too; a neighbour
landing on the computed end does not. **The two sets being adjacent is what makes this set of static
data prove a layout rather than illustrate one.**

Every index byte in both tables is ≤ 5 and every target lands in the body, so the two dispatch
tables are internally closed as well: nothing selects a seventh arm, and nothing jumps outside the
function.

**Not claimed:** nothing here was executed or observed live. §4.1's sign-extension caveat is
untouched — this pass did not re-derive the four writers, so its "no reachable path is negative"
still rests on 4.4 rather than on any check in the walk. §§5–7 and the dispatcher's arm map were not
re-read; `0030F760` and `003105D0` remain unread here, as § says.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

- **Gameplay.** The chain's functions reach three shared battle services.
  - **The presentation-event dispatcher `BattleUnit_DispatchActorPresentationEvent`.** It is called from
    `BattleUnit_RecoverFromTerminalStatusSetIfClear` (`00301140`), `BattleUnit_UpdateCombatFrame` (`00308610`) and
    `00313500`. `00301140` and `00313500` are the two functions that set flag bit 24 in the set-A note.
  - **The battle target buffer.** `003014C0` and `0030F760` reset it, `0030F760` appends to it, and
    `BattleUnit_CancelAndResetCurrentAction` (`003105D0`) resets it too.
  - **The encoded-id class test `BattleEncodedId_IsValidForClass`.** `BattleUnit_ApplyUnitDefinition` (`0023A570`)
    calls it at `0023AA59` before it takes a definition.
  - In addition, `003014C0` reads `WorldActor_GetDefinitionByte12OrMinus1`, and `002FEDC0` (set A's installer at
    `002FEE05`) is called from a 104-byte function that resolves a mapped definition selector and asks
    `BattleUnit_ShouldEnterEngagedActionState`.
- **RNG_Random_Selection.** `AiOrder_EvaluateAndResolveActionTarget` draws on the shared gameplay LCG
  `RNG_SharedGameplayLCG_NextU32`, with a `% 100` roll at `0030160F`–`0030162C`, and calls `BattleData_ResolveWeightedId`.
  Both use the stream the loot rolls use. [Which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md)
  now carries the challenge this implies.
- **Spawn_Encounter_Lifecycle.** `BattleUnit_ApplyUnitDefinition` is reached from `Spawn_ApplyScriptSelectedUnit`, and
  at `0023A776` it resolves the unit's primary spawn-keep entry through `SpawnKeep_ResolvePrimaryEntry`.
  `SpawnUnit_FinalizeSpawnEntryActivation` calls `002FEDC0`, so a spawned foe can get the re-plan set A when its
  activation finishes, provided `002FEDC0` takes its install branch, which is not read here. That fits set A being
  "installed whenever the unit's combat state is reset".

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **ActorEntity — SERVICE and CLIENT, 22 edges.**
  - Cited gambit functions call `ActorWork_GetBattleUnit` (3), `BattleUnit_GetSlotCount` (3), `BattleUnit_GetBySlotIndex` (2), `BattleUnit_ResetStateForReuse` and a 44-byte helper.
  - They are called by `BattleUnit_TeardownAndDespawn` (2), `BattleGroup_RefreshFourActorDefinitions` (2), `BattleUnit_ApplyUnitDefinition`, `BattleUnit_ActivateAppliedDefinitionRuntime` and a 169-byte body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — SERVICE.** `0023A570` on this page calls `BattleStats_InitializeDefinitionRecord`, owned by that layer. What it reaches is the `0x1C8`-byte record initialiser, and it states the sentinels: `qword[+0x50]` becomes `-1`, `word[+0x58]` and `word[+0x1C3]` become `0xFFFF` and `byte[+0x1C5]` becomes `0xFF`, after which the definition id's **high byte** selects which authored table its low byte indexes; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CoreRuntimeScheduling — MECHANICAL (1 edge).** `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` calls `GameClock_GetRawTickCounter` `0032A150`, the 7-byte raw-clock getter. The recovery reads the raw clock; nothing about which gambit set fires depends on the scheduler.

**Movement — SERVICE and CLIENT (20 edges).** `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70` calls `BattleUnit_ApplyMovementIntentToWorldActor` `0023A070`, `Actor_SetMovementSpeed` `0026A330`, `0033A240` and `Navigation_HasDataset` `00383C80`; `BattleUnit_UpdateCombatFrame` `00308610` also calls `0033A240`; the movement handler `caseD_4000` `002FDA60` calls `BattleLocomotion_DecodeOrderGoal` `00312730`, `BattleLocomotion_SetApproachAndReferenceTargets` `00319110`, `BattleUnit_UpdateCombatNavigationStep` `00325BB0`, `BattleLocomotion_ResetPathAndSetTargets` `003291B0` and `BattleLocomotion_IsApproachConstraintActive` `0033A120`; `BattleUnit_ResetStateForReuse` `00236A60` calls `003839C0` and `Navigation_ResetPathPredecessors` `003839F0`; `BattleUnit_CancelAndResetCurrentAction` `003105D0` calls `003291B0` and `0033C9B0`, which calls `BattleLocomotion_BuildSolverContext` `00336710` and `BattleLocomotion_ResetAvoidanceStateRandomized` `0033E1F0` and is called by `00325BB0`; `00325BB0` also calls `00313500`; `BattleUnit_CanAdvanceCombatNavigation` `00325D90` calls the predicate `0030BCD0`; and `00301140` calls `00311F70`. The direct-state dispatcher routes movement ids to the locomotion layer's handler, and the frame, the reset and the cancel paths this page reads reset or drive the unit's path; which order set fires is decided before any of this runs.

**Party — SERVICE (7 edges).** The handler `002FE660` and `BattleUnit_CommitAction` `0030F760` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`; `002FE840` (the `0x414D` target) calls `BattleUnit_EnterPartyCombatStance` `00313400` and `BattleUnit_ExitPartyCombatStance` `00313480`; `00308610` calls `BattleUnit_UpdatePartyCombatStanceState` `00307DF0`; and the verbs `resetemergency_with_animetionmode` `003473E0` and `resetemergency` `00347970` call `PartyRoster_GetActorBySlot` `00263750`. The stance flip this page reads (`0x414D`) is carried out by the party layer's stance bodies (both of which also install set A), and the emergency-reset verbs pick their actor from the party roster.

**Script_VM_Native_Bridge — CLIENT and SERVICE (8 edges).** `0030F2D0` is called by the verbs `resetemergency_one` `00346A10`, `resetemergency_with_animetionmode` `003473E0` and `resetemergency` `00347970`, which pop their arguments through `VMValueStack_PopInt32CoerceFloat32` `00267E10` (and `00347970` pushes a result through `VMValueStack_PushInt32` `00267F90`); the team verb `00239170` is called by `00510280`. The three `resetemergency` verbs reach `0030F2D0`, one of the six installers of the re-plan set A (static set `01EEC3C0` for a party-kind record, `01EEC410` otherwise), and the team verb sets the team id `+0x54` and team-leader flag that the floor order `0x4124` follows; authored script is one of the documented ways a unit's set changes.

**Status_Periodic_Terminal — SERVICE and CLIENT (11 edges).** `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` calls `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveAllMode0StatusesAndRecompute` `0030E8F0`, `BattleStats_ClearStatusLayer0AndProcessSideEffects` `0030E970` and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`; `00233F70` calls `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0`, which calls `00305E70`; `00236A60` calls `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450`; `00301140` calls `0030E360`; `003105D0` is called by `BattleUnit_ResetActionControlForStatusTransition` `00300140` and `00301140`. Several direct-state arms are status changes applied through the status layer, the maintenance tick refreshes the `+0x24` group-leader handle the floor order `0x4124` needs (through `00305E70`), and status transitions cancel the current action through the same reset.

**WorldAreaField — DEPENDENCY (5 edges).** `00233F70` and `BattleUnit_ApplyUnitDefinition` `0023A570` call `FieldData_GetActiveFieldRecordBit15` through its thunk `00313F60`, and `AiOrder_EvaluateAndResolveActionTarget` `003014C0`, `BattleUnit_SelectAndCommitNextAction` `00305AB0` and `0030F760` call `00377C20` directly. Selection, target resolution and commit all consult the current field's bit 15 (the per-area waiver for disabling statuses), so what a set's order can do depends on the field.
