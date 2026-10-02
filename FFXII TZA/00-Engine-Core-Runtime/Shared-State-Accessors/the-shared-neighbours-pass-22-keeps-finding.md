---
system: The shared neighbours pass 22 keeps finding
category: 00-Engine-Core-Runtime
status: AUDITED — the last open box (UQ-32: the slot records, bit 7 of +0x10, and its first setter 0026C8C0) answered 2026-09-17, with UQ-33 and UQ-34
owner_layer: PrimaryOwner:CoreRuntimeScheduling
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: image-derived - every address on this page was read from the authorized EXE with
    disasm_fn.py and every caller count recomputed from edges.tsv; no GZF parent is named
    because nothing here rests on a ledger field.
last_reviewed: 2026-09-14
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: OPUS-falsification-headline-falsified-sizes-and-caller-counts-hold
  last_pass_kind: attack
  crossref_clean: true
origin: FINAL-AUDIT pass 22 — the same few functions generate a third of its findings, and none of them had been read
---

# The shared neighbours pass 22 keeps finding

> **Seven functions totalling 1,402 bytes account for 130 of pass 22's 922 unaccounted
> document × subsystem pairs — and six of the seven, 377 bytes between them, account for 93.**
> *(Corrected 2026-09-14 by this page's own falsification pass, §10: the headline read "six
> functions totalling under 700 bytes account for 130", which double-counted — the six small
> ones are the audio chain and give 93; the 37 that make it up to 130 come from `00322C50`,
> which is 1,025 bytes on its own. Both halves of the old sentence were true of different
> sets and the sentence joined them.)* They are shared entry points: a page about menus, a page about
> spawning and a page about the shop all call the same one, so each inherits a neighbour subsystem
> it never mentions. None of them had been read.

This is the [`cross-subsystem-accessor-hubs`](cross-subsystem-accessor-hubs.md) shape again —
*"found by dispositioning UNACCOUNTED NEIGHBOUR findings, not by reading a category"* — applied to
the pass that is currently the only one failing.

## 1. What the player sees

Nothing names these. One of them is why an action that cannot be performed is refused before any
animation starts, and another is why a sound effect follows the thing that made it rather than
playing from nowhere.

## 2. Why a shared neighbour generates findings in bulk

Pass 22 reports a document when an address it cites has a caller or callee owned by a subsystem the
document never mentions. A function called from all over the image therefore lands in every one of
those documents' findings at once. The distribution is steep:

| | pairs | |
|---|---:|---:|
| the top 20 neighbour functions | 313 | 33.9 % |
| the top 50 | 461 | **50.0 %** |
| the top 100 | 571 | 61.9 % |
| all 1,551 neighbours | 922 | 100 % |

`audit_crossrefs` already excludes a function with **more than 100 callers** as a *hub* — *"its
caller set spans the image by construction, so importing it says nothing about the citing
document"* — but only when the hub is the **subject**, never when it is the **neighbour**. Applying
the same rule to neighbours would remove **35 of the 922 pairs, all CoreRuntimeScheduling**
(measured; `0020E600` alone accounts for 72 neighbour appearances). *That change is proposed and
routed, not applied — it moves the population of the pass that gates completion.*

**And the two biggest non-hub neighbours sit just under the threshold**: `00249C60` has **99
callers** and `00322C50` has **71 callers**. The threshold is not wrong — it was measured over the whole
distribution — but at 71–99 callers a function behaves like a hub for this purpose while passing
the test.

## 3. The audio request chain — 93 pairs

**Six** functions, read from the shipping bytes.
*("Four" until 2026-09-14; the chain listed in §6 has always had six — the count in this line
was never updated when `003603C0` and `001DBDB0` were added to it.)* **A document whose cited function calls any of them
has an `Audio` neighbour and usually says nothing about audio**, because what it is really doing is
asking for a sound.

```
00249C60  play the current context's sound      51 B   99 callers
  ├─ guard   dword [02091098] != 0  ->  return -1          (a global mute/disable)
  ├─ 003A1180  resolve the current packed handle -> id     (-1 when nothing is current)
  └─ tail-call 002DF220(id, 0x40, 0x7F)                    pan 0x40, volume 0x7F
```

*The two constants were labelled ~~"volume `0x40`, parameter `0x7F`"~~ until 2026-09-21 (FABLE).* **They
are the other way round, and nobody had flagged this page** — the correction that reached the store was
about the same pair on [the voice-pack page](../../18-Audio/the-voice-pack-slots-and-the-voice-verbs.md) §3.
`002DF220` masks its **third** argument with `0x7F` (`002DF256`) and forwards through `001DBDB0`,
`00210C00`, `0021B5B0` and `00224540` to `00224570`, which hands the **`0x40`** to `002256F0` — **the pan
wrapper this store already names** — at `0022473F`, and the **`0x7F`** to `002257E0` at `00224751`, a body
that clamps against `127.0f` and then divides by `127.0f` (`00225803`, `0022581F`): a level, normalised.

- **`003A1180`** (111 B) reads the packed handle at `02AEF3FC`; `-1` means *none*. The low 16 bits
  index a **24-byte record array at `02AEEDC0`**, and the words at `+8` / `+0x0A` are recombined
  into a 32-bit value and compared against the handle — **a generation check**, so a stale handle
  resolves to `-1` rather than to whatever now occupies the slot. On a match the id is
  `(word[+8] << 9) + argument`. It first calls `00267330(0)` and refuses if that is non-zero.
- **`00267330`** (39 B) reads `byte [02098E10 + slot*0x288 + 0x10]`: if bit 0 is set it returns
  **bit 7**, otherwise **1**. A per-slot availability test over `0x288`-byte records.
- **`002DF220`** (92 B) is the play entry: `id == -1` returns 0; `003603C0()` — which is just
  `return (signed char)[022CB726]`, a single global enable byte — must return 0; then it masks the
  parameter to `0x7F`, clears **bit 31** of the id and tail-calls `001DBDB0`.
- **`001DBDB0`** (76 B, `Audio`) forwards the id to the audio manager. It was read on 2026-09-14 (UQ-31, §7).

**Bit 31 of the id is cleared in two different places** (`003A1180` via `btr r8d, 0x1f`, and
`002DF220` via `btr ebx, 0x1f`), so the flag it carries is consumed before the play call and is not
part of the id the mixer sees.

## 4. `BattleEncodedId_IsValidForClass` (`00322C50`) — 37 pairs

1,025 bytes, and `00322C50` has **71 callers** — the reason so many battle-adjacent pages inherit a
neighbour they do not mention. `class - 1 > 0x1F` returns 0; otherwise a **32-entry jump table at image
`0x00323054`** dispatches on the class, and each case validates the id its own way. One case is
worth naming: it maps the id through `00309440` (30 B) and **re-enters the switch** with the
result, so a class can delegate its validity question to a class derived from the id.

It is the shared answer to *"is this encoded id meaningful for this kind of thing"*, which is why
pass 13 found two unrelated bodies calling it — `002FFCF0` with class `0x14` and `00317930` with
class `6` — while deriving an action-availability cascade and an equipment-slot eligibility test.

## 4b. The battle block at actor `+0x698`, and its flag-word pair — 18 pairs and counting

`BattleUnit_UpdateEngagementStateFlag` (`00307D10`, 224 B) was read for its 18 pairs and turned out
to share a structure with two functions read under pass 13 and one under this page's own survey.
**Six entry points in six different subsystems consult the same sub-object and the same two flag
words, each with its own mask:**

| function | subsystem | the test |
|---|---|---|
| `00307D10` | battle engagement | `([sub+0x64] \| [sub+0x3C]) & 0x8000020` |
| `002FFCF0` | action availability | `([sub+0x64] \| [sub+0x3C]) & 0x80000003` |
| `0033D890` | movement | `([sub+0x64] \| [sub+0x3C]) & 1` |
| `0030BFB0` | combat stance | the same pair, after requiring bit 4 of `byte[actor]` |
| `00312280` | defeat and loot | reached through `byte[+5] == 1` on the same block |
| `00308610` | the per-unit combat frame | `([sub+0x64] \| [sub+0x3C]) & 0x10`, behind `byte[02089340] & 0x20` |

`sub` is `[actor + 0x698]` in every case, and every one of them checks it for null first. The two
words are **OR-ed together before the mask**, so a bit means the same thing in either — they are one
flag space held in two places, not two independent words.

**What the sub-object IS, found from the other end.** `BattleStats_FindOwningBattleUnit` (`0031B860`,
83 B) takes a pointer and walks every battle unit looking for the one whose `[unit + 0x698]` **equals
that pointer** — so the block at `+0x698` is the unit's **stats record**, and the ledger name of the
routine that searches for it says so. That closes a question this page had left open: the six entry
points above are not consulting an anonymous sub-object, they are consulting the stats record, and
`BattleStats_GetByMappedBattleSlot` (`00320AB0`, 49 B) reaches the same records from the other
direction — slot bytes `0..0x27` into `[02EBF190] + 8` at a stride of `0x1C8`, which is the same
**40 records of `0x1C8` bytes** that `BattleSystem_ResetRuntimeState` walks.

`00307D10` also reads `byte [sub+4]` and `byte [sub+5]`: the combination `+5 == 0` and `+4 == 0x1A`
short-circuits the whole function to **1** before any other test. So `+4` is a kind or state byte
with at least one distinguished value.

**Why this matters for pass 22 specifically:** a page about movement, a page about menus and a page
about rewards all end up citing a function that touches this block, and each inherits the others'
subsystem as a neighbour. **The edge they share is not a relationship between those subsystems — it
is that all of them ask the same actor the same question.**

Its side effects are named because they are not local: on one path it clears bits `0x06` of
`byte [022C1F48]`, zeroes the qword at `022C1F40` and zeroes `[actor+0xDCC]`. `00377C20` and
`00253B90` gate the paths and are **not read** *(answered: see force-fight-mode.md, which reads `00253B90`'s whole body; 2026-10-02, OPUS)*.

## 4c. The two hubs are an addition and a subtraction — 32 pairs

The largest single neighbour in the whole pass is `0020E600`, and it is **three instructions**:

```
0020E600  ImageAddress_ResolveRuntimePointer          815 callers
    mov eax, ecx
    add rax, qword ptr [01F83530]      <- add the image base
    ret

0020E620  RuntimePointer_EncodeImageAddress           279 callers
    sub ecx, dword ptr [01F83530]      <- subtract it again
    mov eax, ecx
    ret
```

~~The same global, exact inverses: an offset↔pointer conversion.~~ *Qualified 2026-09-28 (FABLE, Claude Opus 5.5;
re-read from the bytes, on ASTRA's reference-inverse-domain):* the same global, but inverses only inside a 4 GiB
window.
- **Decode** is `D(u) = B + zero-extended u32(u)` (64-bit add; `mov eax, ecx` zero-extends). **Encode** is
  `E(p) = u32(p) − u32(B)` (32-bit; `0020E620` subtracts only the base's low dword).
- `E(D(u)) = u` for every 32-bit `u`, but `D(E(p)) = p` only when `(p − B) mod 2^64 < 2^32`. `p` and `p + 2^32` encode
  identically.
- There is no null rule: `D(0) = B` and `E(0) = −u32(B)`.
- `B` is whatever `01F83530` holds. That it is the PE or module image base is the name's reading, not established here.

**A document whose cited function
calls one of these has inherited an addition**, and pass 22 reports it as a cross-subsystem
relationship with `CoreRuntimeScheduling` because that is the ledger owner of the two functions.

`audit_crossrefs` already drops a >100-caller function when it is the **subject** of a page — *"its
caller set spans the image by construction, so importing it says nothing about the citing
document"* — and keeps it when it is the **neighbour**. On FABLE's ruling R2 the asymmetry is
corrected **as a disposition rather than a filter**, so the rows stay visible with their reason:
**32 pairs** whose every edge to a subsystem runs through a hub are dispositioned `MECHANICAL`.

**44 more pairs have a hub edge AND an ordinary edge, and they keep failing on the ordinary one.**
Hiding a real finding behind a hub it happens to share a subsystem with is precisely the silent
removal the ruling refuses.

## 4d. `BattleUnit_ProcessDefeatRewardsAndLoot` — 18 pairs, and the same block again

`00312280` (857 B) takes the killer in `rcx` and the defeated unit in `rdx`, and its first act is to
read **`[defeated + 0x698]`** — the block of §4b, for the third time in this page.

    [defeated+0x698] exists, byte[+5] == 1, killer exists, byte[killer+5] == 0   ->  00317ED0(defeated)
    003171C0(defeated)                                                            unconditional
    then: the block must still exist and byte[+5] must be 1
    byte[defeated+0xE9A] & 8   ->  nothing is processed
    (byte[defeated+0xE9A] & 5) == 5  ->  a separate path

So `byte[sub+5] == 1` is the condition three independent entry points test before doing anything —
an active-battle-unit predicate — and `+0xE9A` is a per-unit flag byte where **bit 3 suppresses
reward processing entirely**.

**These pairs are not MECHANICAL.** A page whose code reaches defeat-and-loot processing has a real
relationship with `Rewards_Progression_Economy`: FABLE's **SERVICE** or **CLIENT**, and its standard
requires a sentence on the page rather than a registry row. They stay open here, and the reading is
recorded so that whoever writes that sentence does not have to re-derive it.

## 4e. The scheduling accessors — eight functions, 7 to 40 bytes, 20 pairs

After the hub rows, the pairs still failing on a `CoreRuntimeScheduling` edge were dominated by very
small functions. All eight were read, and every one is a global accessor or a two-global predicate:

| address | size | what it is |
|---|---:|---|
| `001EDE70` | 7 B | `return [01F82E38]` |
| `0032A150` | 7 B | `GameClock_GetRawTickCounter` — `return [0208D45C]` |
| `00229E40` | 7 B | `return [01E02814]` |
| `00229DF0` | 8 B | `return (byte)[02064AD2]` |
| `00229EA0` | 8 B | `return (signed char)[02064AD3]` — **the frame-mode byte** |
| `001EDDA0` | 27 B | `[01DFE0C0] != 0 \|\| [01F82E38] == 0` |
| `001EDEC0` | 40 B | the same two globals, the other way round |
| `00229E70` | 37 B | reads the float at `01E02820`, ~~**clamps it to a floor of 1.0**, stores it back~~ returns it when it compares above 0 or is NaN (`comiss 0, rate` / `jb`), and otherwise stores and returns 1.0: 0.5 is kept, and 0, −0 and negatives reset *(corrected 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's rate-normalizer-domain)* *(qualified 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA's return-domain qualifiers: the NaN is kept only when the `comiss` completes. With the invalid exception masked, the unordered result sets CF and takes the `jb`. Unmasked, a QNaN or SNaN operand raises #XM, the flags are not written, and what follows is the handler's. The game's MXCSR at this site is not established)* *With DAZ set, a positive subnormal compares as 0 and resets.* |

**A page that inherits one of these has inherited a global read**, which is why 20 pairs whose every
neighbour is a hub or one of these are dispositioned `MECHANICAL`. **29 further pairs have one of
these beside an unread neighbour and keep failing** — a pair is not dispositioned by explaining some
of it.

**`00229EA0` closes a small loop.** It returns `byte [02064AD3]` — the frame-mode byte that
`0022AF50` sets to **3** and `0022B000` sets to **5** (§3 and §4). The mode bodies and the mode
getter are the same mechanism from two ends, and both were found by dispositioning pass 22 findings
rather than by reading a category.

## 5. What this dispositions, and what it does not

**It dispositions the RELATIONSHIP, not the document.** A page that cites a function which calls
`00249C60` now has somewhere to say *"its `Audio` neighbour is the shared sound request, see this
page"* — which is a disposition, where merely containing the word "audio" was only a coincidence
the instrument could not tell from one.

**It does not clear the findings by itself.** Each of the 130 pairs still belongs to a document
whose owner decides whether the edge matters to that page. Nothing here edits another page.

**Unread, and named as such:** `00226BE0` (1,936 B, 23 pairs),
`00261F90` (335 B, read only to its first branch), and the 1,545 remaining neighbours.

## 6. Key addresses

| Address | Name | Size | Role |
|---|---|---:|---|
| `00249C60` | `FUN_00249c60` | 51 B | play the current context's sound; `00249C60` has 99 callers |
| `003A1180` | `FUN_003a1180` | 111 B | resolve the packed handle to an id, generation-checked |
| `002DF220` | `FUN_002df220` | 92 B | the play entry; masks the parameter, clears bit 31 |
| `00267330` | `FUN_00267330` | 39 B | per-slot availability byte at `02098E10 + slot*0x288 + 0x10` |
| `003603C0` | `FUN_003603c0` | 8 B | the global audio enable byte at `022CB726` |
| `001DBDB0` | `FUN_001dbdb0` | 76 B | forwards `(0, id, volume, parameter)` to the audio manager singleton (UQ-31) |
| `00322C50` | `BattleEncodedId_IsValidForClass` | 1025 B | 32-way class switch; `00322C50` has 71 callers |
| `00309440` | `FUN_00309440` | 30 B | id → class mapping used by one switch case |
| `00307D10` | `BattleUnit_UpdateEngagementStateFlag` | 224 B | the engagement test; reads the `+0x698` block's flag-word pair |
| `00312280` | `BattleUnit_ProcessDefeatRewardsAndLoot` | 857 B | defeat and loot; gated on `byte[+0x698+5] == 1` and `byte[+0xE9A] & 8` |
| `0020E600` | `ImageAddress_ResolveRuntimePointer` | 10 B | adds the image base at `01F83530`; `0020E600` has 815 callers, the largest single neighbour |
| `0020E620` | `RuntimePointer_EncodeImageAddress` | 9 B | subtracts the base's low dword — ~~the exact inverse~~ the inverse within the 4 GiB window above the base (§4c) *(qualified 2026-09-28, FABLE)* *(the window is modular, `(p − B) mod 2^64 < 2^32` as §4c states, so it wraps past the top of the address space when `B` is within 4 GiB of it)*; `0020E620` has 279 callers |

## 7. What is not known

- [x] ~~**UQ-31.** What `001DBDB0` does with the id, and whether the cleared bit 31 is re-used there.~~
      **Answered 2026-09-14 (FABLE):** bit 31 is not re-used. `001DBDB0` forwards the id unchanged to the
      group player, which plays it on the loaded sound group numbered `id >> 9`.
      - **`001DBDB0`** fetches the audio manager singleton at `01FD36A0`, through a 33-byte getter. It passes
        `(manager, 0, id, volume byte, parameter)` to a 40-byte selector that masks the parameter to `0x7F` a second time.
        - Selector `0`, the value the play entry passes, tail-jumps into the player at manager `+0x08`.
        - Any other value goes to `+0x10`.
      - **The player** (138 B) does four things:
        1. It divides the id by 512 with a signed shift. For an id built as `(word[+8] << 9) + argument` (§3), that
           gives back `word[+8]` whenever the argument is below 512.
        2. It takes a new play handle from `00212950`. That function is a global counter at `01FD36B4`, incremented and
           masked to 31 bits, that skips 0.
        3. It walks the intrusive list at player `+0x08` for an object whose `+0x3C` equals the group number.
        4. On a match it calls that object's 36-byte play wrapper with `(handle, id, volume, parameter)`.
        It returns the handle whether or not a group matched, and that handle is the play entry's return value.
      - **Bit 31.** It is always clear from the play entry on, so no later test can see it set. Its only effect is arithmetic: with bit 31 clear, the `cdq` /
        `and edx, 0x1FF` rounding step in the signed divide adds nothing, so `id >> 9` is exact.
      - **Not read:** the group object's play body behind the wrapper, and the selector-`1` player at `+0x10`. Nothing
        was executed.
- [x] ~~**UQ-32.** What the `0x288`-byte records at `02098E10` are, and what bit 7 of `+0x10` means.~~
      **Narrowed 2026-09-14 (FABLE).**
      - **The records** are the five actor-manager slots. Their field map is
        [the-actor-manager-record-field-map.md](../../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md),
        which records `+0x10` bit 0 as *slot live* and leaves bit 7 unnamed.
      - **What bit 7 does** was read in `ActorManager_RunFieldRuntimePass`. It marks a slot whose start-up has not
        settled.
        - **At entry** the pass copies bit 7 into bit 0 of `+0x11` (`shr al, 7`, then `or` into `+0x11`).
        - **When bit 7 is clear**, `cmp byte [slot+0x10], 0x80` / `jb` sends the pass to the ordinary loop: every
          record from 0 to `+0x20` is updated.
        - **When bit 7 is set**, the pass runs a start-up branch instead.
          - It keeps bit 7 set, and skips the record updates, while bit 7 of `+0x17` or bit 5 of `+0x10` still holds.
          - Otherwise it updates each record whose `+0x10` byte is non-zero and notes whether any was.
          - A pass on which none was, with bit 1 of `+0x11` clear, settles the slot. Bit 7 is cleared (`and 0x7F`)
            and then rewritten from that result (`shl bpl, 7` / `or`), so it stays set only while records are still
            running.
          - On the settling pass a slot whose `+0x28` is 0 also runs one-off field-entry work. Among it,
            `WorldTransition_SetOptions` is called with bits 3 and 4 of the options cleared.
      - **Consumers.** The sound gate's slot test (§3, `00267330`) returns bit 7 for a live slot. A sound is
        therefore refused while its slot's start-up is unsettled.
      - **Not located:** the write that first sets bit 7.
        - The 152 functions that reach the slot array, by absolute reference or through the bound-slot pointer,
          were scanned for byte, word and dword writes at `+0x10`.
        - The only writer of bit 7 found is the pass itself.
        - One more function decrements a `+0x10` byte, but on a register whose type was not established.
        - The first set may come through a whole-record copy or a base this scan did not follow.
      - Static reading only; nothing was executed.
      ***ANSWERED 2026-09-17 (FABLE): the records are the five actor-manager slots, bit 7 of `+0x10` is the start-up-unsettled flag, and the write that first sets it is the definition-payload binder `ActorManager_BindLoadedDefinitionPayload` `0026C8C0`.** The binder addresses the slot as `02098E10 + index x 0x288` and publishes the pointer at `02099D70` (`0026C8FE`..`0026C911`). It takes a copy of the slot's `+0x10` after clearing bits 3 and 4 in place (`and 0xE7`, `0026CB0B`), clears bit 0 in the copy (`0026CB12`..`0026CB1B`) and stores it once (`0026CB67`); then, after summing the payload's record counts into `+0x20` (`0026CBCE`..`0026CBD9`), it ORs `0x82` into the copy (`0026CBDC`) and stores it again (`0026CC45`): bits 1 and 7 set together, bit 0 ([slot live](../../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md)) clear, at the moment the loaded definition payload is bound. Its only caller is the load completion `0032F850`, so a slot enters the field pass unsettled from its load, and the pass `0025D9E0` then clears and rewrites the bit each pass until no record still runs (`0025DE36`..`0025DE6F`). The earlier census missed it because the set is a whole-byte store of a register copy, not an `or` into memory. Boot clears it: the slot reset `00266D10` memsets each of the five slots to zero (`00266EF0`..`00266F37`) before setting their index and a few bytes. Static, binder, reset and pass read; image-wide store census over every width at `+0x10`.*
- [x] ~~**UQ-33.** Which of the 32 classes `BattleEncodedId_IsValidForClass` distinguishes, and whether the~~
      class numbers are the same space as the battle command kinds.
      ***ANSWERED 2026-09-17 (FABLE): all 32, each to a table slot, and no, the class numbers are not the command kinds.** [The registry read of 2026-09-03](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) decoded the whole 32-entry table at `00323054`: ~~every class from 1 to 32 resolves to one registry slot (four slots serve more than one class: `02EBF110` classes 22..24, `02EBF068` classes 15, 30, 31, `02EBF138` classes 19, 20, `02EBF038` classes 25, 32), class 13 concatenates three slots~~ classes 2–18, 20, 21 and 24–32 resolve to a registry slot (two slots serve more than one class: `02EBF068` classes 15, 30, 31 and `02EBF038` classes 25, 32), class 19 is the literal range `0xE000`..`0xEFFE`, classes 22 and 23 the literal bounds 4 and 9, and class 13 sums the counts of four slots (`02EBF090`, `02EBF088`, `02EBF080`, `02EBF078`) *(corrected 2026-10-02, OPUS: arms `00322C50+0x313` (19), `+0x356`/`+0x35F` (22, 23), `+0x322` (20, `02EBF138` alone), `+0x368` (24, `02EBF110` alone), `+0x1D8`–`+0x23C` (13); the-encoded-id-class-registry.md)* behind a `0x8000` base, and class 1 maps the id through `00309440` and re-enters; the rule is `0 <= id < count` against the slot's own count dword, a null slot failing every id. So the validator distinguishes exactly the **table classes** of the authored-data registry, which is what its callers name (0x14 the action-id table, 0x17 the definition-selector table, 0x19 the licence node table, 0x1D the status table, 6 equipment). The **battle command kinds** are a different space: the menu kind at `ctx+0`, values 1..`0x23`, on which [`BattleMenu_BuildCommandEntryList`](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md) dispatches to build a command list; the two meet only where the availability path validates an action id with class 0x14. Static; cross-referenced, not re-derived beyond the jump table.*
- [x] ~~**UQ-34.** What `byte [sub+4] == 0x1A` distinguishes, and what the `+0x3C` / `+0x64` flag bits mean~~
      individually — three masks are known (`1`, `0x80000003`, `0x8000020`) and the space is not.
      ***ANSWERED 2026-09-17 (FABLE): a Chocobo, and three status masks over one 32-status vocabulary.** The block at `+0x698` is the `0x1C8`-byte stats record, and its `+4` word is the whole encoded definition id (`BattleStats_InitializeDefinitionRecord`, `0023AD8E`): `+5 == 0` is the party table `02EBF130`, and row `0x1A` = 26 of that table is [the Chocobo](../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) (the rows decode 0..5 the six, 6..16 guests, 17..25 no name, 26 Chocobo, 27..39 the Espers). So `00307D10` returns 1 before any test for the ridden Chocobo. The two words are [the definition-record status pair](../../04-Actor-Entity/the-definition-record-flag-pair.md): `+0x3C` the authored permanent-status word and `+0x64` the runtime status word that the `+0x38` immunity word can block, OR-ed before every test, one bit per status id. The masks are therefore [statuses](../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md): `1` = KO (bit 0); `0x80000003` = KO, Stone and X-Zone (bits 0, 1, 31), the three terminal statuses; `0x8000020` = Confuse and Berserk (bits 5, 27), the pair that takes control away. Static; the words and the statuses are read on their own pages, joined here.*
- [x] ~~**UQ-35.** Whether the hub rule should apply to neighbours as well as subjects — **routed to
      SWE2-FRONTIER and FABLE**, because it changes the population of a gating pass.~~ **Ruled 2026-09-14 (FABLE):** not as a generic cut. The two functions that make it matter are named as substrate instead (**R7**), recorded in [PASS22-WHAT-ACCOUNTING-MEANS.md](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §9.6.
      - **Measured** with `Tools/work/FABLE/regprose/pass22_neighbour_hub.py`, with R1 and R4. A neighbour cut at the subject rule's 100 callers changes the shipped findings by 0, and the R3 clauses-1+2 findings by −12 (299 → 287).
      - **All twelve rest on the codec pair in §6's table.** `ImageAddress_ResolveRuntimePointer` (10 B, 815 callers in 21 owning subsystems) removes 12, and its inverse `RuntimePointer_EncodeImageAddress` (9 B, 279 callers in 11) removes 3, overlapping.
      - **Why the named form.** A pointer codec that 21 layers call has no owning layer to cross into, so declaring those two substrate is a statement about them. A generic neighbour cut would also silence the next 100-caller function that genuinely is a service, and nothing would notice.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The concentration figures | full re-derivation of the finding rule over all 380 citing documents, `Tools/work/OPUS/` | 1 |
| The audio chain and its guards | `disasm_fn.py` over each body; every branch above is from the listing | 1 |
| `00249C60` has 99 callers | `edges.tsv` from `DumpFullCoverageGraph`, 2026-09-14 05:14 | 1 |
| `00322C50` has 71 callers | the same `edges.tsv` | 1 |
| `0020E600` has 815 callers | the same `edges.tsv` | 1 |
| The 32-way switch | the jump table at image `0x00323054`, reached by `jmp rcx` after a `0x1F` bound | 1 |
| `001DBDB0`'s behaviour and the fate of bit 31 | every body in the forward chain read to its call into the group's play routine (UQ-31) | 1 |

## 9. Where the callers actually live — the layer census this page owed

*(Pass 22 disposition, 2026-09-15, SWE2-FRONTIER: the page's own subjects carry the cross-layer
edges it describes, so the layer names belong here in full.)* The citing side of these six
functions spans thirteen subsystems, measured on the live graph:

- `00226BE0` is called by `ActorEntity` `00263230`, `Movement` `0026A1D0`, `CombatAction`
  `00313DB0` and `World` `00266D10`, and calls `ActorEntity` `00358940`, `Party` `003590D0`/
  `00263750` and `WorldAreaField` bodies.
- `002FFCF0` is called by `CombatAI` `00305AB0`/`003014C0` and `CombatAction` `00317BC0`, and
  calls `Gameplay` `0030D9A0`/`00322C50` — the combat stack sits on both sides of it.
- `00322C50` (`BattleEncodedId_IsValidForClass`, 71 callers) is called by `CombatAI`
  `00321770`/`00327A10` (12 AI edges across its callers), `CombatAction` bodies, `Gameplay`
  `0031C5D0` via `00309440`, `Movement` `00326BB0`/`0031BAC0` and `Party` `00358CB0` — every
  layer that validates an id before acting on it.
- `00249C60` (99 callers) is called by `Save_Load_Settings` `00580EB0`/`00581350`,
  `Presentation` `002BAF80` and the rest of its 93-pair spread — every layer that can ask for a
  sound.
- `002DF220` is called by `CombatFormula` `003112F0`, `Rewards_Progression_Economy` `0030C650`
  and `Script_VM_Native_Bridge` `00357040`; `003A1180` by `CombatFormula`, `Rewards_Progression_
  Economy` and `Presentation` `0046CC70`; `00267330` by `Script_VM_Native_Bridge` `0050EEE0` and
  `Party` `00358CB0`; `00261F90` calls `WorldAreaField` `003EAA70`/`003148F0`.

Thirteen layers — `ActorEntity`, `CombatAI`, `CombatAction`, `CombatFormula`, `Gameplay`,
`Movement`, `Party`, `Presentation`, `Rewards_Progression_Economy`, `Save_Load_Settings`,
`Script_VM_Native_Bridge`, `World`, `WorldAreaField` — is the page's thesis measured, not a
defect in it: shared entry points are called from everywhere because that is what shared means.

*(Pass 22 live-graph sweep, second order, 2026-09-15: the callers' own neighbours close the
census — `00263230`/`00263750`/`00266D10` call `Input` `00226BE0`-adjacent bodies (8 edges);
`00313DB0` calls `InputGameplay` `00313A00` (1); `003148F0` is called by
`Platform_Online_Achievements` `003160C0` (1); `003014C0` calls `RNG_Random_Selection`
`00308EC0`/`00328370` (2); `002BAF80` calls `Resource` `00249580` (1). The fan-out is bounded:
nineteen layer names account for every measured edge this page's subjects carry.)*

## 10. Falsification pass — 2026-09-14 (OPUS)

This page had no falsification pass and was one of three documents in the database without one. It
is also the page most of this session's pass-22 dispositions cite as the place a body was read, so
what it claims is load-bearing. Every claim below was attacked from the shipping bytes and
`edges.tsv` on 2026-09-14, not from the page.

### 10.1 The headline did not survive

**Attacked:** *"Six functions totalling under 700 bytes account for 130 of pass 22's 922 unaccounted
pairs."*

**Result: FALSIFIED, and corrected above.** The six small functions are the audio chain — 51 + 111 +
92 + 39 + 8 + 76 = **377 bytes** — and §3 attributes **93** pairs to them. The remaining 37 come from
`00322C50`, which is **1,025 bytes by itself**. So it is seven functions and 1,402 bytes for 130, or
six functions and 377 bytes for 93. The old sentence took the function count and the byte bound from
one set and the pair count from another. Nothing measured was wrong; the sentence joining them was.

**Second finding in the same place:** §3 opened "Four functions" while listing six. The count was
never updated when `003603C0` and `001DBDB0` joined the chain. Corrected.

### 10.2 What survived, and how it was attacked

| claim | attack | result |
|---|---|---|
| `00249C60` has 99 callers | recount from `edges.tsv` | **99** — holds |
| `00322C50` has 71 callers | recount from `edges.tsv` | **71** — holds |
| `0020E600` has 815 callers, the largest single neighbour | recount from `edges.tsv` | **815** — holds |
| `0020E620` has 279 callers | recount from `edges.tsv` | **279** — holds |
| all twelve sizes in §6 | disassemble each and find its terminating `ret` | **all twelve hold** |
| the 32-entry jump table is at image `0x00323054` | disassemble `00322C50`'s tail | `00323050 ret`, `00323051 nop dword`, then data at **`00323054`** — holds |

### 10.3 The attack that was wrong, which is worth recording

The first size check used "the first `int3` after the entry" as the end of a function and reported
**two** disagreements: `00307D10` measured 339 against a claimed 224, and `00322C50` measured nothing
at all. Both were the instrument. `00307D10` ends at `00307DEF` with `ret` and
`BattleUnit_UpdatePartyCombatStanceState` begins at `00307DF0` **with no padding between them**, so
the scan ran straight through into the next function; `00322C50` ends at `00323050` and is followed
by a three-byte `nop` and jump-table data, which contains no `int3` either. **A padding-based size
measure silently merges two adjacent functions whenever the linker did not pad**, and it did not pad
here. The page was right both times.

### 10.4 What this pass does not establish

It does not re-derive the **pair attributions** — the 93, the 37, the 18s and the 20 — because the
pass that produced them has since been driven to zero findings as shipped, so the 922 denominator no
longer exists to recount against. Those numbers are **historical, as of the run that produced them**,
and this page should be read that way. Re-deriving them would need the pass replayed against the
document set as it stood, which is a different piece of work and is not claimed here.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT, 24 edges.** The shared accessors this page catalogues are called by the status layer's main bodies: `BattleStats_ChangeStatusAndProcessSideEffects` and `BattleUnit_RunPeriodicCombatMaintenance` (5 each), `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` and `BattleStats_RemoveStatusesFromMaskAndRecompute` (2 each), and others. That fan-in is why these neighbours keep being found.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Spawn_Encounter_Lifecycle — CLIENT (9 edges through 3 of this page's functions).** The Spawn_Encounter_Lifecycle layer reaches this page at `00328370`, `0032A150`, `003148F0`. `SpawnKeep_RotatePersistenceBanksForAreaTransition` is the worked example, read in full - it is the area-transition bank rotation: it takes a **`0x9428`-byte stack frame** through the stack probe, needs both `[0208E690]` and `[0208E698]`, and compares the current area index against the stored `word[02089372]`; **3 of the 8 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (78 edges through 17 of this page's functions).** The UI layer reaches this page at `00249C60`, `001EDEC0`, `00249580`, `003148F0` and 13 more. `FUN_0024b9b0` is the worked example, read in full - it is a 1,500-byte routine whose second argument being **8** short-circuits it to a single arm before any of the rest runs; **8 of the 65 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
- **Audio — CLIENT and SERVICE (108 edges).** 53 inbound (Audio bodies `002DF010`, `002DEF40`, `002DF220` call page-cited `002257E0`, `002256F0`, `00212950`); 55 outbound (page-cited `00224570`, `0046CC70`, `00261F90` call Audio bodies `003A1180`, `002DF220`, `00210B30`). Substantive edges include `001DBDB0` is called by `002DF010`; `001DBDB0` is called by `002DEF40`; `001DBDB0` is called by `002DF220`; `001DBDB0` calls `00210C00`; the remaining edges run through shared helpers the page cites.
- **Items_Equipment_Shops_License — CLIENT and SERVICE (31 edges).** 29 inbound (Items_Equipment_Shops_License bodies `BattleStats_SetEquipmentSlotByMappedId` (0031A510), `BattleStats_SetEquipmentSlotByStatsIndex` (0031A410), `BattleStats_SetEquipmentSlotDirect` (0031A630) call page-cited `BattleEncodedId_IsValidForClass` (00322C50), `Equipment_CheckItemEligibleForSlot` (00317930), `BattleStats_GetByMappedBattleSlot` (00320AB0)); 2 outbound (page-cited `BattleFormula_ApplyTargetResult` (003112F0), `Equipment_CheckItemEligibleForSlot` (00317930) call Items_Equipment_Shops_License bodies `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0), `BattleStats_HasRequiredLicenseForEquipment` (00323C60)). Substantive edges include `BattleFormula_ApplyTargetResult` (003112F0) calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (003008A0); `Equipment_CheckItemEligibleForSlot` (00317930) is called by `BattleStats_SetEquipmentSlotByStatsIndex` (0031A410); `Equipment_CheckItemEligibleForSlot` (00317930) is called by `BattleStats_SetEquipmentSlotByMappedId` (0031A510); `Equipment_CheckItemEligibleForSlot` (00317930) is called by `BattleStats_SetEquipmentSlotDirect` (0031A630); the remaining edges run through shared helpers the page cites.
- **Platform — SERVICE (1 edge).** 1 outbound (page-cited `00224570` call Platform bodies `005CC930`). Substantive edges include `00224570` calls `005CC930`.
- **SaveLoad — CLIENT (1 edge).** 1 inbound (SaveLoad bodies `00582790` call page-cited `00249580`). Substantive edges include `00249580` is called by `00582790`.
- **Story_Event_Quest_Hunt — SERVICE (1 edge).** 1 outbound (page-cited `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) call Story_Event_Quest_Hunt bodies `EventMemory_QueryDefinitionIdAbsent` (00377440)). Substantive edges include `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) calls `EventMemory_QueryDefinitionIdAbsent` (00377440).
### Interior citation — frontier hub `002E1C40` (2026-09-18, SWE2-EC7)

`002E1C40` — 44 B, 17 callers: the capability flag-word toggle the shared
neighbours read. `ecx` picks the arm — `bts eax, edx` or `btr eax, edx`
([`002E1C4B`](../../_index/ADDRESS-INDEX.md)) on the word at `0215F1AC`; the
second word at `0215F1B4` is always `btr`-cleared at the same bit. Set-or-clear
on one mask, always-clear on its shadow — the pair-write the policy page's
inhibit bits correspond to.

Cross-subsystem note: the slot-record setter `0026C8C0` this page tracks also
calls into Story_Event_Quest_Hunt (one edge), keeping that neighbour accounted.

## SWE2-EC7-39 update (2026-09-19) - `00326BB0`

`00326BB0` (419 B) is the Movement body the page names - the `022C25A0`..`022C2610` field block plus `02089340`, `00322C50`/`002367A0`/`00265020`/`00265200`/`003590D0`/`003588B0`/`00263E30`. Interior anchor `00326C49` (a `00322C50` call).

## SWE2-EC7-97 update (2026-09-20) - `002EACC0` measured

`002EACC0` (14 B) is the two-global publish `0032F850` and
`0032FB70` call: `rcx` lands at `0215FD98` and `edx` at
`021641F0` - the pointer-plus-dword pair the neighbours pass
installs for later readers.
Interior anchor `002EACC7` (the `021641F0` store).

`0057EA40` (228 B) is the save-state transition `0057F360`/`00580EB0` run: with `02CA99D8` live it tests bit `0x2` of its `+0xC0` and, when set and `02CA99C0`'s `+0x398` is nonzero, folds `+0xDC` bit 1 -> bit 2 (`or 2` once) and resets `+0x398`/`+0xCC`; it then writes `rcx` into `02CA99D0`'s `+0xC8` and merges `(edx & 1) * 2` into its `+0xC0`, fires `00582540` twice (message class `1` carrying the `0057E950` fnptr, then class `4`), and finally sets `02CA99D8`'s `+0xC0` bit `0x2` — an ordered state hand-off across three globals.

Interior anchor `0057EAB4` (function `0057EA40`).
