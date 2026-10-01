---
contract: Group completion and respawn — the dead-member checklist and the cooldown clock
category: 05-Spawn-Encounter-Lifecycle
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md
entries: [00306F00, 00307090, 00235F50, 00235FB0, 002366E0, 002360D0, 0031B760, 0032A150, 003299B0, 00306E60, 00239710, 0050F8C0, 00307030, 003070E0, 00307110, 00307140, 00238B70, 00238AE0, 0026ADC0, 00233D20]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 127 addresses cited - 18 data, 40 entry, 66 interior, 1 literal, 2 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-spawn-group-pass-1   # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — group completion and respawn

> **The seventh behavioural contract**, and the one that takes the database's **sub-runtime rung
> debt to zero**: after this, every labelled document owes only `RUNTIME VALIDATED`, which is one
> blocked experiment rather than undone work.
>
> **Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`** — §13 holds isolated original-code
> evidence (EXP-011, EXP-014) and one live pre-kill observation (EXP-019); the completion transition
> has no live capture.

## 1. What the player sees

You clear a room. The last enemy of a group drops, something happens on screen, and some time later
they are back. **The game is not counting kills** — it is ticking members off a checklist, and it
does not care in what order or how many times you killed the same one.

## 2. Interface

| operation | entry | signature | returns |
|---|---|---|---|
| record a death, complete the group | `00306F00` (303 B) | `(BattleUnit* rcx)` | `al` — true only on completion |
| reset every group ledger | `00307090` (73 B) | `()` | — |
| read the death count | `00235F50` (93 B) | `(int lane edx)` | `eax` = `u16` at record `+0x08`, or `-1` |
| elapsed **seconds** since last death | `00235FB0` (121 B) | `(int lane edx)` | `eax`, or `-1` |
| read the respawn cooldown | `002366E0` (93 B) | `(int lane edx)` | `eax` = `u16` at record `+0x10`, or `-1` |
| resolve a lane from a bkei index | `002360D0` (39 B) | `(u8* map rcx, int bkei edx)` | lane, or `< 0` |
| the active battle unit | `0031B760` (13 B) | `(ActorWork* rcx)` | `rax`, or `0` when `rcx` is null |
| the raw frame counter | `0032A150` (7 B) | `()` | `eax` = `*(u32*)0x0208D45C` |
| dispatch a presentation event | `003299B0` (83 B) | `(BattleUnit* rcx, int event edx, int r8d)` | — ; `r8d` is parked at `unit +0x2C` across the call and cleared after |
| **register / unregister a member** | `00306E60` (158 B) | `(BattleUnit* rcx, int add edx)` | — ; `memberMask` bit set or cleared, `deadMask` bit **always** cleared |

### 4a. `EE-11` answered — the verb order is observed, and group 0 is a sentinel

FABLE censused the authored corpus: **6,746 `btlAtelSetEventFlagGroup` calls across 502 of the 1,114 `us` scripts, every one inside a `spawnGroup entryNN` preamble immediately after `btlAtelSetLevel`.** The second argument takes only `0/1/2` (mode) and the first only `0..5` (group); **`(0,0)` accounts for 6,206 of them.** So the order and placement are **observed** rather than inferred — see the group-completion page §4.

The native side says *why* `(0,0)` is the overwhelming majority, and it is not that group 0 is disabled:

```asm
00306E84  cmp   byte ptr [rax+5], 1      ; rax = [unit+0x698]; the stats record's KIND byte
00306E88  jne   0x306EF3                 ;   -> only spawn-backed (kind 1) units get here
00306E8F  movzx edi, byte ptr [rcx+0xE98]  ; the unit's group byte
00306E96  test  edi, edi
00306E98  je    0x306EEE                 ; <-- GROUP 0 IS SKIPPED
...
00306EB2  lea   ecx, [rdi-1]             ; group - 1
00306EB8  lea   rcx, [rdx+rdx*2]         ; x 3
00306EC3  lea   r8,  [rdx+rcx*8]         ; base + (group-1) * 0x18
```

> **The group table is 1-based, so `0` means “no group”, not “group zero, suppressed”.** The index is `group − 1` with a `0x18` stride, so entries exist for groups 1–5 and there is no slot a 0 could address. A reimplementation that allocates a zeroth entry and skips it has built a different structure that happens to behave the same until something iterates it.

> **And the precondition above it ties this contract to the unit union:** `00306E60` acts only when `[[unit+0x698] + 5] == 1`, i.e. only on **spawn-backed** units — `+0x05` is the discriminator of the `BattleStatsRecord` union recorded in [`_types/fields.tsv`](../_types/fields.tsv). Party (kind 0) units never reach the group logic at all.
| set group id + mode, then register | `00239710` (114 B) | `(ActorWork* rcx, int mode edx, int group r8d)` | `eax` = `0`, or `-1` with no battle unit |
| verb `0x3030` `btlAtelSetEventFlagGroup` | `0050F8C0` (67 B) | `(…, ActorWork* target rdx, …, VmValueStack* r9)` | two int pops, tail-jumps `00239710` |
| consume every pending flag, post the group | `00307030` (82 B) | `()` | — ; per field frame, gated by `00233D20` |
| any flag pending | `003070E0` (39 B) | `()` | `eax` = 1 if any entry's flags bit 0 |
| raise the flag after the death reaction | `00307110` (40 B) | `(BattleUnit* rcx)` | — ; clears unit bit 47 |
| the dispatch gate | `00233D20` (47 B) | `()` | `eax` = `(02089340 & 0xF00) == 0 && !(01FD46D4 bit 10)` |
| post a value to the field table | `0026ADC0` (35 B) | `(int index ecx, int value edx)` | — ; `((~~u16~~ **i16***)*(02098E68))[index] = value` if `index < 64`, `02098E20` bit 0, pointer non-null — **CORRECTED 2026-09-11 (OPUS-REQ-FABLE-OPERAND):** the element is **signed**: the consumer `AiTargetSelector_ResolveOperandValue` (`00321190`) sign-extends every kind-1 / 2 / 3 element (`movsx ecx, ax` at `003211C2`, `003211D7`, `003211EC`), while its arm 9 reads its own table at `0208D334` with `movzx` (`0032125C`) — the control that shows the extension is deliberate |
| event lock: capability row 12, party suppression | `00307140` (183 B) | `(int on ecx)` | — |
| event lock: `02089340` bit `0x20` + per-unit `0x30B` message | `00238B70` (120 B) | `(int on ecx)` | — |
| event lock: `02089340` bit `0x80` | `00238AE0` (29 B) | `(int on ecx)` | — |

**`-1` is "no such lane", never a value.** All three readers share a seven-check prologue (§4) and
every failure returns `-1`.

> **Rows below the first nine were added 2026-09-10** from the system page's §4–§5. `00306E60` is
> the `memberMask` writer `EE-2` asked for; the three event-lock calls are what completion *does*.

> ### The three record accessors are read by script and by nothing else
>
> Four instruments, each with a positive control: **`E8` = 1, `E9` = 0, code memory-operand = 0**
> for each of `00235F50`, `00235FB0` and `002366E0` — and in every case **the single caller is a VM
> verb wrapper**: `0050F660`, `0050FAB0`, `005101F0`.
>
> ~~**So no native code reads the death count, the death stamp or the cooldown**, and in particular
> **nothing native compares the cooldown against the elapsed seconds.** That comparison, if it
> happens, happens in authored script.~~ *Corrected 2026-09-29 (FABLE, Claude Opus 5.5,
> [`pkg-gp-spawn-respawn`](../_index/candidates/pkg-gp-spawn-respawn/README.md) N):* the three **accessors** are script-only, but the
> automatic spawn selector ([the placement page](spawn-placement-and-retirement.md), "Automatic spawn selection") reads the fields **directly**. It
> skips an entry that has died out (count `+0x08` ≥ limit `+0x0A`). For a committed entry that is not pending range
> re-entry and has a cooldown, it skips while `seconds − stamp (+0x0C) < cooldown (+0x10)`; the sites are in the record. So the native gate re-admits an entry at
> **elapsed ≥ cooldown**, while the scripts' own checks use `>` (§8). The two checks are distinct, and a reimplementation
> needs both.

> ### Two interface rows corrected 2026-09-13 (OPUS, `OPUS-ABI-RECOVERY`)
>
> Found by a liveness-derived signature prober **validated first** against 46 signatures parsed
> mechanically out of this and every other contract's interface table (95.7% agreement). These two
> were the only disagreements, and both were **this document's**, not the instrument's.
>
> **`0031B760` was documented `()`.** Its complete 13-byte body is
> `test rcx, rcx / jne / xor eax, eax / ret / jmp 0x263E30` - it **reads `rcx`, null-tests it, and
> returns 0 when null**. §6 of the system page already names it `ActorWork_GetBattleUnit`, which
> takes an `ActorWork*`, so **the interface row contradicted a name in the same document.**
>
> **`003299B0` was documented with two parameters.** At `003299C2` it executes
> `mov dword ptr [rcx + 0x2C], r8d` - **a third argument**, parked at `+0x2C` across the call to
> `002EB030` and cleared at `003299F6`. A reimplementation built from the two-argument row drops a
> value the callee reads.
>
> See [derived call signatures](../00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md)
> §3.

## 3. Types

**`SpawnRecord`, `0x250`** and **`SpawnGroupLedger`, `0x18`** — both in `_types/`.

```
records:  *(char**)0x0208E690 + slot * 0x250        heap, not image
  +0x08  u16   death count
  +0x0C  u32   the SECOND-stamp of the last death        (see section 10)
  +0x10  u16   respawn cooldown, WHOLE SECONDS            EE-1 ANSWERED 2026-09-13

ledger:   0x02EC13C0 + (group - 1) * 24               BSS, 64 entries, 1,536 bytes
  +0x00  u64   memberMask   the members this group waits for   written by 00306E60 (script verb 0x3030 adds, range retire removes)
  +0x08  u64   deadMask     the members confirmed dead          set by 00306F00; a member's bit cleared by 00306E60 either way
  +0x10  u8    flags        bit 0 = completion signal pending   set by 00306F00 (mode 1) or 00307110 (after the death reaction); consumed by 00307030
  +0x11..+0x17 padding
```

**Unit-side fields this contract depends on** (physical offsets on the battle unit; type rows are
~~routed to the type owner~~ *in the type store, 2026-09-27 (FABLE, Claude Opus 5.5): `BattleUnit` `+0x000` `unitFlags` (bit 47), `+0x698` `statsRecord`, `+0x6A0` `spawnRecord`, `+0xE98` `spawnGroupId`, `+0xE99` `spawnGroupMode`*):

```
unit +0x00   u64   bit 47 = completion deferred until the death reaction is handled (4 sites in the image)
unit +0x698  ptr   for definition ids with high byte 1: the spawn record + 0x80, whose byte +5 (== the id's high byte) gates everything here;
                   for high byte 0 (party characters): a BattleSystemState element, *(02EBF190) + 8 + index*0x1C8  (OPUS-CONTRA-BU698, 2026-09-10)
unit +0x6A0  ptr   the spawn record for the first kind, NULL for the second; 00300530 bumps +0x08 / +0x0C through it
unit +0xE98  u8    1-based group id; sole byte writer 00239746
unit +0xE99  u8    bit 0 = mode == 1, bit 1 = mode == 2; sole writer 00239766
```

**64 groups × up to 64 members**, one bit per member. `0x02EC19C0 − 0x02EC13C0 = 1,536`, and
`1,536 / 24 = 64` exactly.

## 4. Preconditions · postconditions · invariants

**The shared accessor prologue — seven checks, identical in nine accessors:**

```c
u = ActorWork_GetBattleUnit();      if (!u) return -1;
map = u->p_40;                      if (!map) return -1;
if (lane < 0)                       return -1;
if (lane > map[0] - 1)              return -1;      /* map[0] is the count */
slot = map[1 + lane];               if (slot == 0xFF) return -1;   /* empty lane */
rec = *(char**)0x0208E690 + slot * 0x250;
if (!rec)                           return -1;
```

> **One arm of that prologue is unreachable and it looks like a check.** After `movzx eax, dl` the
> code runs `test eax, eax / js` — a byte zero-extended into a 32-bit register is never negative.
> **It appears in all nine accessors**: one template, copied. A reimplementation should keep the
> `lane < 0` check, which is real, and may drop this one, which is not.

**Invariants.**

- **Completion is a mask test, not a count**: `(memberMask & deadMask) == memberMask`.
- **A death is idempotent.** `deadMask |= bit` — killing the same member twice changes nothing.
- **A member outside `memberMask` can never complete a group**, however many die.
- **The group id at unit `+0xE98` is 1-based**; `0` disables the whole path.
- **Registration is per member and clears the member's dead bit** (`00306E60`, either direction).
  A respawned member re-registered by its script is alive to the checklist again; the group is
  incomplete until it dies once more.
- **Registration and death resolve the slot from the same two fields** (`unit->p_10 + 0xF6`, the
  map at `+0x40`) with the same sign-extended 32-bit shift, so the two agree bit for bit.
- **The reset empties both masks and clears flag bit 0** — all 64 entries — and runs at area
  initialisation only (`002342F0`). Membership is rebuilt by script on every area entry.
  *(Was "empties everything — both masks and the flag"; corrected 2026-09-13,
  `OPUS-LEDGER-RESET-BIT0`. The masks are whole-qword zero stores; the flag is
  `and byte ptr [...], 0xFE`, which clears **bit 0 only** and preserves bits 1–7. The reset's
  postcondition is `memberMask == 0 && deadMask == 0 && (flags & 1) == 0` — **not** `flags == 0`.)*
- **The completion path has no one-shot.** Neither `00306F00` nor its caller remembers a completion;
  a second completion of the same group needs a further death in it, which the writers as read only
  produce through re-registration.

## 5. State

| | detail |
|---|---|
| **read** | `0x0208E690` (record array), `0x0208D45C` (frame counter), `0x01DFE0B8` (frame-rate scale), `0x008F8D80` (`30.0f`), unit `+0x00`, `+0x10`, `+0x40`, `+0x698`, `+0x6A0`, `+0xE98`, `+0xE99`; `02089340` (`0xF00` gate), `01FD46D4` (bit 10 gate), `02098E20` (bit 0 gate), `02098E68` (table pointer), `0208E688`/`0208E6A0` (unit array and count, in `00238B70`) |
| **written** | the ledger's `memberMask` (`00306E60`), `deadMask` (`00306F00`, `00306E60`) and `flags` (`00306F00`, `00307110` set; `00307030`, `00307090` clear); unit `+0x00` bit 47; unit `+0xE98`/`+0xE99` (`00239710`); spawn record `+0x08`/`+0x0C` (`00300530`); `u16` slot 3 of the table at `*(02098E68)`; capability row 12 at `0215F1C0 + 0x30`; `02089340` bits `0x20`, `0x80` (and `0x2` from `00233F70`); byte `0209A2C4[2]`; the party suppression state behind `00359200`/`00359330` |
| **allocated / freed** | none — the ledger is BSS, the records are pre-existing heap |

## 6. Relationships

```
authored script, in the member's own context
  -> verb 0x3030 btlAtelSetEventFlagGroup(group, mode)  [0050F8C0: pop mode, pop group]
     -> 00239710: unit->E98 = group; unit->E99 = (mode==1) | (mode==2)<<1
        -> 00306E60(unit, 1): memberMask |= bit, deadMask &= ~bit          [THE WRITER]

range retirement (002350C0, mode 1 or 2 retire action)
  -> BattleUnit_TeardownAndDespawn(unit, 1)                                   [00300E40, at 002352B1]
  -> 00306E60(unit, 0): memberMask &= ~bit, deadMask &= ~bit

a member dies (00300530 lethal branch)
  -> record +0x08 += 1, record +0x0C = seconds                                (spawn-backed only)
  -> SpawnGroup_RecordMemberDeathAndHandleCompletion(unit)
     -> FUN_00263D30(unit->p_10) -> bkei
     -> SpawnLaneMap_ResolveBkeiIndex(unit->p_40, bkei) -> slot
     -> ledger[group-1].deadMask |= sx32(1 << (slot & 31))
     -> if complete: 00307140(1), 00238B70(1), 00238AE0(1)                    [EVENT LOCK]
                     mode 1: clear bit 47, flags |= 1, dispatch 0x2005
                     else:   set bit 47,              dispatch 0x2008
  -> completion reported: the caller's own death event is skipped

reaction handler (003250F0) on 0x2007 / 0x2008 / 0x200C / 0x200E
  -> unit |= bit 33; if bit 47: 00307110(unit): clear bit 47, flags |= 1

field frame (00234590)
  -> 00307030: if 00233D20(): for each entry with flags&1: flags &= ~1; 0026ADC0(3, group)
     -> ((i16*)*(02098E68))[3] = group   (read back sign-extended, 003211C2)   [WHAT THE SCRIPT SEES]

unit frame (00233F70)
  -> 003070E0(): any flag pending?  if not: 02089340 |= 2

authored script
  -> VM_SpawnEntry_GetDeathCount / GetElapsedTicksSinceLastDeath / GetRespawnCooldownTicks
     -> the three record accessors                     [THE ONLY READERS]
```

## 7. State transitions

The ledger has one transition per registration, one per death, one on completion and one per frame:

```
(BSS zero) --[ResetLifecycleLedger, area init]--> memberMask 0, deadMask 0, flags bit 0 CLEARED
           --[script: verb 0x3030 on member]----> memberMask |= bit ; deadMask &= ~bit
           --[range retire of a member]---------> memberMask &= ~bit ; deadMask &= ~bit
           --[a member dies]--------------------> deadMask |= bit
           --[(member & dead) == member]--------> COMPLETE: event lock; mode 1: flags |= 1 now
                                                            else: unit bit 47, and flags |= 1 only if
                                                            00307110 runs -- its sole caller 003250F0
                                                            has NO static route (section 10)
           --[next field frame, gate open]------> flags &= ~1 ; table[3] = group
```

> ### The reset clears `memberMask` — CORRECTED 2026-09-10
>
> ~~**`SpawnGroup_ResetLifecycleLedger` clears `deadMask` and `flags` bit 0 but does not clear
> `memberMask`** — it zeroes eight qwords per four entries at `rax-0x10 … rax+0x40` and `and`s four
> flag bytes with `0xFE`.~~
>
> The eight stores were listed correctly and read wrongly. `rax` starts at `02EC13D0`, entry 0's
> **`flags`** byte, so `rax-0x10` is entry 0's `memberMask` and `rax+0x08`, `+0x20`, `+0x38` are the
> `memberMask` of entries 1–3; the four `deadMask`s are `rax-0x08`, `+0x10`, `+0x28`, `+0x40`
> (`003070AF`–`003070CB`, `rcx = 0` from `00307097`). **Eight qwords per four entries is two per
> entry, and each entry has exactly two.** The reset empties both masks of every entry (and clears
> flag bit 0 — see the bullet in §6 and the census below), and membership is
> rebuilt by script after every area initialisation — which is why the writer could be authored
> rather than native. **Instrument:** re-tabulating each store against the `+0x10` bias, which the
> 2026-09-08 reading recorded and then did not apply. The `0x60` stride claim stands.

## 8. Script · resource · event interactions

**This subsystem's read side is entirely script-facing** (§2), and **so is its membership.** Verb
`0x3030` `btlAtelSetEventFlagGroup` — `pops_int = 2`, family 3, handler `0050F8C0` in
[the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv) — is the only
route to `+0xE98`, `+0xE99` and a set `memberMask` bit. As written in a script the order is
`(group, mode)` by the pop-order law; no decompiled script has confirmed it (`EE-11`).

Its write side fires two presentation events, `0x2005` and `0x2008`, through
`BattleUnit_DispatchActorPresentationEvent`, and **posts the completed group's number to `u16` slot 3
of the 64-entry table at `*(02098E68)`** once the flag is consumed. That table is gated by the
ActorManager slot-0 live bit and is also read by the AI target-selector operand resolver
(`00321190` → `00264D20`).

**Its script-side reader for slot 3 is `waitv`, and the postcondition is only observable through it**
(answered 2026-09-18; `EE-9` by FABLE, poll verified from the bytes by OPUS). The zone scripts import
the value as `scratch1` short `@0x06` — 239 of the 1,114 shipped scripts import it and **236 of those
`waitv` on it**. The poll is `00354230`, and it is a *keep-waiting* predicate rather than a read: it
dispatches on a width selector at `[r8+4]` (`movsx byte` / `movsx word` / `mov dword`, arms at
`00354275`/`0035427A`/`0035427F`) and then returns `value == 0` —

```
0035428D  xor  eax, eax
00354294  test ecx, ecx
00354296  sete al            ; 1 = keep waiting
```

So **a group completing with the number 0 would post a completion no script can see**: `waitv`
cannot distinguish "posted 0" from "not posted", and every boss-aftermath script waiting on it
blocks forever. **In the shipped code this cannot happen** — group 0 is the *not-a-member*
sentinel, gated by both ledger paths before any indexing (`00306E8F`, `00306F31`), and the corpus
uses `(0,0)` 6,206 times exactly that way. The hazard is real in `waitv` and a reimplementation must
still not post before the flag is consumed — but nothing that could post 0 ever gets a lane.

> **One thing this does NOT settle.** The width selector's own edge: the jump table covers `0..5`
> and **anything above it falls to `00354283`, which loads `1` and therefore returns "stop waiting"
> immediately**. Nothing read here establishes which widths the group-number import actually uses,
> so that arm is recorded, not attributed.

## 9. Determinism

**RNG:** none. **Timing:** the elapsed-seconds reader divides by the frame-rate scale, so **a
respawn wait is the same number of seconds at 30 and at 60 fps** — the one place in this subsystem
where the frame rate is deliberately cancelled out rather than exposed. **Threading:** the ledger is
a bare global array with no lock; concurrent deaths are not guarded and **single-threaded use is
assumed, not proven**.

## 10. Failure paths and edge conditions

- **Every accessor failure is `-1`**, and `-1` is not a legal value for any of the three fields.
- **A zero `memberMask` completes on the first death**, because `0 & anything == 0`. The ledger is
  BSS and starts at zero, so **whatever writes `memberMask` must run before the first death** or
  every group completes immediately. ~~**That writer is not identified** — `EE-2`.~~ **Identified
  2026-09-10:** `00306E60`, called with `add = 1` from the script verb that also writes the group id
  (`00239746` → `00239770`), so a unit with a group id is registered in the same call, and the
  zero-mask case is a reimplementation edge the writers as read do not produce. A unit whose slot
  fails to resolve at registration (`00306EB0`) keeps its group id unregistered, but its death fails
  the same resolution (`00306F55`) before the test.
- **Range retirement is not a death.** `002350C0` unregisters the member (`002352BB`, `edx = 0`)
  without calling `00306F00`, so a group whose last living member is retired does not complete.
- **The dispatch gate can hold a flag indefinitely.** `00307030` consumes nothing while
  `02089340 & 0xF00` is set or `01FD46D4` bit 10 is set (`00233D24`, `00226BD8`); the flag stays
  raised and is delivered in the first frame the gate opens.
- ~~**The deferred arm may never post.**~~ **REFUTED 2026-09-19/22 (`EE-12`, re-verified
  owner-side).** `00307110`'s only caller `003250F0` **does run**: its guard stub `002E70A0`
  sits in handler-table slot `02CA4470` (id 0xC) and is invoked by the engine when a track
  ends or is switched (`call rax` at `0041DC84`/`0041DD03`/`0041CEC6`). The sisters
  `00325090`/`00325260` run the same way — authored-command classes 6 and 4 dispatch their
  slots, authored 7,008× and 27,631× in the shipped `@FMC` corpus. The presentation event
  still also goes to the animation layer (`003299B0` → `002EB030` → `002EB0D0` → `00427320`).
  A mode ≠ 1 completion sets unit bit 47, plays `0x2008`, and the ledger flag posts when the
  track-end dispatch reaches `003250F0` → `00307110`.
- **A post with a null table pointer, or with ActorManager slot 0 not live, is dropped silently** —
  `0026ADC0` returns without writing (`0026ADCC`, `0026ADD8`) and the flag has already been cleared,
  so that completion is never seen by the table's readers.
- **A null unit, a null kind block, or `kind->b_05 != 1` returns false** before anything is touched.
- **`group == 0` disables the path** — the death is recorded nowhere.
- **A lane that does not resolve is dropped silently**: `lane < 0` skips the mask update and returns
  false, so the death does not count toward completion and nothing reports it.

  > **PREMISE REFUTED, CONCLUSION SURVIVES — 2026-09-16 (FABLE), `EE-12`.** `003250F0` **is** reached — `002E70B0` `jne 003250F0`, a `0F 8x rel32` conditional near jump, which the enumerated forms omitted. **But that route terminates:** the jumping guard is registered into the handler table at `02CA4410`, and a rip-relative sweep over **all** of `.text`, controls passing, finds **exactly two** references to that table in the whole image — the clear and the registration. **Nothing reads it.** So *the deferred arm never posts* stands, on a named mechanism rather than on an absence. *The one hole:* a dispatcher forming the table address other than rip-relative, which is what the re-scoped runtime watchpoint is for. **Final state (EE-12, 2026-09-19;
re-verified owner-side 2026-09-22): the conclusion does not survive — the table is read and
dispatched.** The "no reader" sweep searched the base `02CA4410`; readers reference their own
slots — `call qword [02CA4430]` (id 4) at `00417B52`/`69`/`80`, `call rax` on `[02CA4440]`
(id 6) at `00417CC6`, `call rax` on `[02CA4470]` (id 0xC) at `0041DC84`/`0041DD03`/`0041CEC6`.
`003250F0` runs; the deferred arm can post.

> ### The clock reads seconds, and the imported name said ticks
>
> ```c
> divisor = (int)(*(float*)0x01DFE0B8 * 30.0f);      /* 1.0f -> 30, 2.0f -> 60 */
> elapsed = (*(u32*)0x0208D45C) / divisor - record->u32_0C;
> ```
>
> `00235FB0` was imported as `SpawnEntry_GetElapsedTicksSinceLastDeath`. **It returns seconds**, and
> `+0x0C` is a second-stamp. Carried across unchecked it would have put a factor of 30 or 60 into
> any reimplementation of respawn timing — **and at 30 fps the error would have been invisible**, in
> a system that also contains a 30-versus-60 scale.
>
> **The wrong name is still on the VM wrapper too** (`0050FAB0`
> `VM_SpawnEntry_GetElapsedTicksSinceLastDeath`), because the sanctioned pipeline has no rename
> script — the same constraint recorded under `BQ-8`.

> ### `EE-1` ANSWERED 2026-09-13 — whole seconds, and the box below predicted exactly how
>
> `EE-1` asks whether the cooldown at `+0x10` is in seconds. **Nothing native relates the two
> values**: each of the three accessors has exactly one caller, all three are VM verb wrappers, and
> no function reads more than one of them. **The comparison is made in authored script or not at
> all**, so the unit is a script-side convention. **Answering `EE-1` needs the authored script or a
> runtime observation — a static instrument cannot do it**, and that is now stated rather than left
> as work not yet done.
>
> **That prediction held, and the answer arrived the way it said it would.** FABLE censused the
> authored corpus: **all 1,765 `btlAtelGetRespawnTime` calls across the 1,114 `us` scripts are
> `btlAtelGetElapseTime(i) > btlAtelGetRespawnTime(i)` with the same `i`** — 1,737 also
> `|| btlAtelGetDeadCountNow(i) == 0`, 28 also `|| btlAtelGetRespawnCause() == -1`. **The unit is
> whatever `btlAtelGetElapseTime` returns, and OPUS re-derived that from `00235FB0`:**
>
> ```asm
> 00235FFA  call 0x32A150                ; the 30 Hz tick counter at 0208D45C
> 00235FFF  movss xmm0, [01DFE0B8]       ; 1.0f
> 00236009  mulss xmm0, [008F8D80]       ; x 30.0f
> 00236011  cvttss2si ecx, xmm0          ; ecx = 30
> 00236015  div   ecx                    ; UNSIGNED INTEGER divide  -> whole seconds
> 00236017  sub   eax, dword ptr [rbx+0xC]   ; minus the stored start second
> ```
>
> **So the cooldown at `+0x10` is consumed as whole seconds, compared with a strict `>`.**
>
> **Two truncations compound, and a reimplementation must keep both.** The divide discards the
> sub-second remainder *and* the script test is strictly greater-than, so a cooldown of `N` does
> not elapse at `N.0` seconds — it elapses at the first tick where `floor(ticks/30) > N`, i.e.
> **after `N+1` whole seconds**. Writing `>=`, or comparing in floating point, changes every
> respawn in the game by one second.

## 11. Observable behaviour

- **Order does not matter and overkill does not count.** The checklist is a mask.
- **A respawn wait is the same wall-clock length at either Frame Rate setting.**
- **Two different things happen when the last member dies**, chosen by bit 0 of unit `+0xE99`: the
  arms differ in *three* ways at once — bit 47 of the unit's first qword moves the opposite way, the
  ledger flag is set on one arm only, and the presentation event is `0x2005` or `0x2008`. ~~**What
  distinguishes them is not established** — `EE-3`.~~ **Established 2026-09-10:** the script's mode
  argument. Mode 1 posts the completion in the same call and the last member shows a `0x2005`
  reaction, which the reaction handler routes to the engage/auto-attack path rather than a death
  case; any other mode plays the death reaction and posts the completion when the reaction event
  has been handled. Either way the party is locked first.
- **The player sees the lock, then the script's response.** Completion inhibits ten row-12
  capabilities and party movement before any event is posted; what the field script does with the
  posted group number is authored.

## 12. Reproduction formula

```c
/* lane -> record */    rec = *(char**)0x0208E690 + map[1 + lane] * 0x250;
/* elapsed seconds */   (*(u32*)0x0208D45C) / (int)(*(float*)0x01DFE0B8 * 30.0f) - rec->u32_0C;
/* ledger entry */      L = (Ledger*)(0x02EC13C0 + (group - 1) * 24);
/* member bit */        bit = (int64_t)(int32_t)(1u << (slot & 31));            /* same in BOTH writers */
/* register (add=1) */  L->memberMask |=  bit;  L->deadMask &= ~bit;           /* 00306E60, verb 0x3030 */
/* unregister (0)   */  L->memberMask &= ~bit;  L->deadMask &= ~bit;           /* 00306E60, range retire */
/* record a death */    L->deadMask |= bit;                                     /* CORRECTED, see below */
/* completion test */   (L->memberMask & L->deadMask) == L->memberMask;
/* event lock */        lock(1);   /* row12 |= bits {0,3,4,5,6,7,8,11,12,20}; party suppression; 02089340 |= 0x20|0x80 */
/* arm select */        (unit->b_E99 & 1) ? (unit->q_00 &= ~(1ull<<47), L->flags |= 1, ev = 0x2005)
                                          : (unit->q_00 |=  (1ull<<47),               ev = 0x2008);
/* reaction handled */  on 0x2007/0x2008/0x200C/0x200E: unit->q_00 |= 1ull<<33;
                        if (unit->q_00 & (1ull<<47)) { unit->q_00 &= ~(1ull<<47); L->flags |= 1; }
/* field frame */       if (!(g_02089340 & 0xF00) && !(g_01FD46D4 & (1<<10)))
                            for (i = 0; i < 64; i++) if (ledger[i].flags & 1) { ledger[i].flags &= ~1; post(3, i + 1); }
/* post */              if (index < 64 && (g_02098E20 & 1) && *(u16**)0x02098E68) (*(u16**)0x02098E68)[index] = value;
/* reset (area init) */ for (i = 0; i < 64; i++) { ledger[i].memberMask = 0; ledger[i].deadMask = 0; ledger[i].flags &= ~1; }
```

> ### The dead-mask bit is a 32-bit shift, sign-extended — corrected 2026-09-08
>
> This section previously wrote `L->deadMask |= 1ull << lane`. **The machine does not do that**, and
> the difference is reachable:
>
> ```text
> 00306F68  mov ecx, r8d      ; the value SpawnLane_FromBkei returned
> 00306F6F  mov eax, 1
> 00306F74  shl eax, cl       ; THIRTY-TWO bit: x86 masks the shift count to 5 bits
> 00306F76  cdqe              ; and then SIGN-EXTENDS eax into rax
> 00306F78  or  [rdx+8], rax
> ```
>
> | value | `1ull << v` | what `00306F00` writes |
> |---:|---|---|
> | 0–30 | bit *v* | bit *v* — the same |
> | **31** | bit 31 | **`0xFFFFFFFF80000000`** — bits 31 **through 63** |
> | **32–63** | bit *v* | aliases onto `v & 31`; **32 sets bit 0** |
>
> **And the value is not a 0–63 lane.** `002360D0` returns `map[1 + bkei]` — the record **slot**
> byte, rejecting only the `0xFF` sentinel — so it ranges 0–254 and is used directly as the shift
> count. §3's *"64 groups × up to 64 members, one bit per member"* holds for the ledger's *layout*;
> it does not hold for how a death addresses it. **The upper half of `memberMask` is unreachable
> except through slot 31's sign extension.**
>
> A reimplementation using `1ull << slot` completes groups the original never completes. This is
> exercised: `diff_group_completion.py` puts slots 31 and 32 in its map deliberately.

## 13. Runtime validation

**Evidence class: isolated original-code, plus one live pre-kill observation. Live capture of the
completion transition: still absent** (restated 2026-09-11, OPUS-NOTICE-S13-CLASSES — the earlier
"None" was the live half of a two-valued answer).

| claim | how it was observed live | date | result |
|---|---|---|---|
| §3 completion: `00306F00` makes the three prologue calls (`00307140`, `00238B70`, `00238AE0`, each ECX = 1) and dispatches `0x2005` / `0x2008` to the unit with R8D = 0, returning 0 / 1 | **isolated original-code**, not live: `00306F00` (303 B), `00263D30`, `002360D0` under Unicorn 2.1.4 at their original addresses, SHA-gated, the four callee bodies stubbed to `ret` — [EXP-011](../_experiments/EXP-011-group-completion-validator.md) | 2026-09-10 | 100 calls / 19 completions matched; nine source variants rejected at the callback boundary |
| §4 image layout: the `bkei` word and the ledger flag sit where the map says — a record ending after the `bkei` word and a ledger ending after the flag still complete | the same execution with two synthetic image boundaries — [EXP-014](../_experiments/EXP-014-group-survivor-scope.md) | 2026-09-10 | exact match; two mutants caught only at the byte / callback level |
| §2 registration: a group's `memberMask` is non-zero before the first kill | **live, read-only**: the Stepping save, group 1 member mask 1, dead mask 0, flags 0, field-table slot 3 = 0 before any attack — [EXP-019](../_experiments/EXP-019-group-ledger-live.md) (PARTIAL) | 2026-09-10 | observed; the registration writer and the completion transition were not |

**What those classes do not cover.** ~~The callee bodies (`00307140`, `00238B70`, `00238AE0` and the
dispatch target) are stubbed, so their outputs, ownership effects and scheduling are unproved;~~ *(superseded 2026-09-26: the
S-17 replay [`s17-opus-replay-group-completion`](../_index/candidates/s17-opus-replay-group-completion/README.md) runs every §4
invariant with those callees real, at NATIVE-REPLAY; noted here 2026-09-29, FABLE)* the
synthetic images of EXP-014 say nothing about live allocation sizes; EXP-019 stopped before a kill,
so `deadMask`, the ledger flag and slot 3 across the last death are unobserved. Two of the three
records name this contract in prose rather than by path, so `check_contract_runtime.py` cannot link
them until the keys change (routed to ASTRA as `FABLE-REQ-ASTRA-EXPKEYS`).

The cheapest **live** confirmations remain: read `0x02EC13C0` after entering a room with a group
and confirm `memberMask` is non-zero **before** the first kill — now observed once by EXP-019, and
still a *prediction* for any other room: the static reading says every registered member's bit is
set by its own script's verb `0x3030`, and a zero mask at that point would mean the scripts
register later than assumed, not that the writer is missing; read `0x01DFE0B8` and confirm `1.0f`
or `2.0f`; watch `deadMask` accumulate as members die; on the last death watch ledger `+0x10` bit 0
rise and, in the next field frame, `u16` slot 3 of the table at `*(0x02098E68)` take the group
number while the flag drops.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**94 generated points: 74 KILLED · 11 SURVIVED · 9 EQUIVALENT · 0 NO_BUILD · 0 TIMEOUT · 0 INVALID. Verdict `FAIL`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/group_completion` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**Eleven survivors, and the count is the honest part of this row.** They are the `name_registry` family at scale: most mutate `GroupImage_At`, `load_q` and `load_b`'s resolve-failure returns — **kind B, fixture scaffolding with no counterpart in the original** — and the rest are **kind A** guards a later check makes redundant, of which `count < 0` → `count < 1` is the clearest: `bkei > count - 1` already rejects every non-negative `bkei` when `count` is 0. **This adjudication is by inspection of the bodies and is NOT claimed to be exhaustive per mutant**; the pilot's own `CONTRACT_MAP` reads 2 of 20 claims exercised, so the suite being thin here is already recorded and this campaign agrees with it.

## 14. Unresolved

1. ~~**What writes `memberMask`, and when relative to the first death.** `EE-2`~~ — **answered
   2026-09-10**: `00306E60`, from each member's script via verb `0x3030`; range retirement removes.
2. ~~**What distinguishes the two completion arms.** `EE-3`.~~ **Answered 2026-09-10**: the verb's
   mode argument; both arms converge on the ledger flag.
3. ~~**The unit of the respawn cooldown.** `EE-1`~~ — **ANSWERED 2026-09-13: whole seconds, strict `>`, and `N` elapses after `N+1`.** §10 named the instrument and the instrument delivered.
   `+0x10` is not seen written in this family either.
4. ~~**What `FUN_00307140`, `FUN_00238B70` and `FUN_00238AE0` do**~~ — **read at the write level
   2026-09-10** (event lock: capability row 12, party suppression, `02089340` bits). What the bits
   *inhibit* is `EE-8`; the `0x30B` message is `EE-7`.
5. ~~**What `FUN_00263D30` computes** to produce the bkei index — it is `movzx eax, word [rcx+0xF6]`
   (system page §4); what that word *is* on the `+0x10` object is still open.~~ **RESOLVED
   2026-09-20 (SWE2-CONTRACT): the word is the record's entry-group index — the bkei the zone
   script assigns.** The `+0x10` object is the unit's bound `ActorStorageRecord` (`actorWork`,
   `BattleUnit +0x010`, bound at `002344EF`). `+0xF6` is **zero-initialised** by
   `ActorSystem_InitializeManagerRuntime` — the field map's "written four times" is four parallel
   passes each storing `bp`, and `bp` is `xor ebp,ebp`'d at `0026CED3` and never rewritten, so all
   four stores write **zero** (`0026CF63`/`0026D001`/`0026D0A7`/`0026D182`), inside loops that
   resolve each record through `00358940` (the `+0x08` record-table lookup). **The live writer is
   `0025AE00`** — reached from verb **`00BE` `setentrygroupall`** (`00340970`, dispatch-table slot
   `0x1EEEEE0`), which pops the index off the operand stack (`00267E10`), resolves the bound slot
   (`002640C0` → `*(02099D70)`) and stamps `+0xF6` on records 0–4 via `0025AE00` — all five records
   of the bound slot, which is why the same value lands on whichever of them becomes `unit->p_10`.
   `SpawnLaneMap_ResolveBkeiIndex` (`002360D0`) then turns it through the unit's lane map
   (`unit->p_40` `laneMapCount`, count at +0, slots from +1) into the ledger lane. *Deliberately not
   claimed: which keep-entry/lane numbering the script's operand uses — the value is authored data;
   the lane map, not this word, decides the bit.*
6. ~~**The other `0x250 − 8` bytes of the spawn record**, and the six other accessors that share the~~
   ~~prologue.~~ **ANSWERED 2026-09-10:** [the spawn-keep entry field map](Spawn-Record/the-spawn-keep-entry-field-map.md)
   — every touched offset with its writers and readers, the 20 direct accessors and 78 hop accessors (47 before the scanner's epilogue fix); the
   last eight bytes are one of three ranges nothing enumerated touches.
7. ~~**Who reads slot 3 of the table at `*(02098E68)`**~~ — **ANSWERED 2026-09-18.** The zone scripts,
   through `waitv` on `scratch1` short `@0x06`; 236 of the 239 shipped scripts that import it wait on
   it, and the poll `00354230` returns *keep waiting* while the value is zero. See §8. ~~**What the
   two dispatch gates represent**~~ — **answered on the system page 2026-09-12 (FABLE), synced here
   2026-09-20:** `02089340 & 0xF00` are the battle-state word's four party-down states (focus actor
   down, every active member incapacitated, whole roster down, leader down — [the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
   §2.5), and `01FD46D4` bit 10 is **time-stop request id 10** (`settimestopmagic` / the
   target-selection cursor `00313DB0`). A wiped group does not post while the party is down, a
   time-stop is active, or the player is choosing a target. ~~**Whether any shipped group is
   numbered 0**~~ — **ANSWERED 2026-09-21 (SWE2-CONTRACT): 0 is the *not-a-member* sentinel, not a
   group number.** `00239710` stores the verb's argument raw at `+0xE98`; both ledger paths gate on
   it before indexing — `00306E8F`/`00306F31` `movzx …, byte [rcx+0xE98]`; `test`/`je` — so a
   group-0 unit never enters `memberMask` and a group-0 "completion" can never reach the `group-1`
   indexing (`00306EB2`, `00306F57`) or the post. FABLE's corpus census matches: 6,746 shipped
   `btlAtelSetEventFlagGroup` calls, group arg `0..5`, and **`(0,0)` accounts for 6,206** — the
   `spawnGroup entryNN` preamble's "no completion group" default. §8's zero-post hazard is real in
   `waitv` but **unreachable through this path** — nothing that could post 0 ever gets a lane.
   `EE-9` closed.
8. ~~**The script-side argument order and placement of `btlAtelSetEventFlagGroup`.** `EE-11`~~ — **OBSERVED, not inferred, 2026-09-13.** See §4a.
9. ~~**Whether `003250F0` ever runs**, and with it the deferred arm's flag.~~ — **ANSWERED:
   all three run. `EE-12` answered 2026-09-19 (FABLE), routes re-verified owner-side
   2026-09-22 (SWE2-CONTRACT).** The handlers sit behind non-`.pdata` cold-stub guards
   (`002E7090`/`002E70A0`/`002E70C0`, orphaned-looking fragments outside every function body —
   the reason function-scoped censuses miss them), registered by `0041D6C0(id, fn)` from
   `002EA320` and `002EA5F0` (eight `lea rdx,[rip→stub]` sites verified) into the per-class
   handler table `02CA4410`, and the table **is** dispatched — `mov rax,[slot]` → `call rax`
   verified at `00417B52`/`00417B69`/`00417B80` (id 4 `02CA4430` → `002E70C0` → `00325260`),
   `00417CC6` (id 6 `02CA4440` → `002E7090` → `00325090`), `0041DC84`/`0041DD03`/`0041CEC6`
   (id 0xC `02CA4470` → `002E70A0` → `003250F0`, engine-invoked on track end/switch). Authored
   corpus (FABLE): class 4 written 27,631× across 62,208 `@FMC` blocks (20,392 route to
   subtypes 0–9 → `002E70C0`), class 6 written 7,008×, id 0xC is engine-invoked, not authored.
   **So the deferred arm can post** — `003250F0` runs whenever a track ends on a unit whose
   guard passes (`[rcx+0x0D]&1` clear, `[rcx+0x30]` non-null) — and the earlier "never posts"
   hazard below is refuted, not just bounded.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| record stride `0x250`, base `*(char**)0x0208E690` | the shared prologue's own arithmetic — `imul rcx, rax, 0x250` / `add rcx, [0208E690]` at `00235F8A`/`00235F91` (same shape `00235FEA`/`00235FF1` in `00235FB0`) | 1 | PROVEN |
| ledger 64 × 24 at `0x02EC13C0` | reset walks `0x02EC13D0`→`0x02EC19D0` at `0x60` per four — `00307090`/`00307099`/`003070CF`; the death handler indexes `[rcx+rcx*2]` then `*8` at `00306F64`/`00306F6B` | 1 | PROVEN |
| completion is a mask test | `(member & dead) == member` at `00306F7F` `and rax, [rdx+8]` / `00306F83` `cmp rax, [rdx]` | 1 | PROVEN |
| elapsed is in **seconds** | `div` at `00236015` by `(int)(scale × 30.0f)` — `00235FFF` loads the scale, `00236009` multiplies, `00236011` truncates | 1 | PROVEN |
| the three readers are script-only | **four instruments** — `E8` 1, `E9` 0, operand 0 — each with a positive control; every caller is a VM verb | 1 (static) | PROVEN |
| the `js` arm is unreachable | `movzx eax, dl` at `00235F83` (same shape `00235FE3` in `00235FB0`) cannot produce a negative dword | 1 | PROVEN |
| the ledger is BSS | past `SizeOfRawData` in `.data` | 1 (static) | PROVEN |
| `00306E60` writes `memberMask`, add/remove by slot, dead bit always cleared | `00306ED4`–`00306EEA`; same gates as `00306F00` | 1 | PROVEN |
| exactly six functions address the ledger | from-entry scan of every body, both addressing forms, control `02089340` = 126. **Reproduced 2026-09-12 by an independently written sweep**: six functions, **one `lea` each**, zero image-base-register references — and the control returns **126**, the same number | 1 | PROVEN |
| `+0xE98`/`+0xE99` have one byte writer | from-entry displacement sweep, control `00239746` | 1 | PROVEN |
| verb `0x3030` is the add caller | `0050F8C0` two pops + `jmp 0x239710`; `00239741 mov edx, 1` | 1 | PROVEN |
| range retire is the remove caller | `002352B6`/`002352BB` | 1 | PROVEN |
| the reset zeroes both masks | the eight stores `003070AF`–`003070CB` in `00307090`, tabulated against the `+0x10` bias | 1 | PROVEN |
| the reset clears flag **bit 0 only**, preserving bits 1–7 | `003070A0`–`003070AB`, four `and byte ptr [...], 0xFE`. Added 2026-09-13 | 1 | PROVEN |
| no instruction in the image touches any bit of the flags byte but bit 0 | whole-byte census over all six rip-relative `lea` references into `02EC13C0`–`02EC19C0`: two `or …, 1`, one `test al, 1`, one `and al, 0xFE`, four `and byte …, 0xFE`, and nothing else. Added 2026-09-13 | 1 | PROVEN |
| bit 47 is touched at four sites only | immediate sweep of every body, controls `00306FBF`/`00306FFD`. **Reproduced 2026-09-12**, and the four are now named: `00306FBF` and `00307110` clear it with `movabs 0xFFFF7FFFFFFFFFFF`, `00306FFD` and `00325192` set it with `movabs 0x800000000000`. **Two set, two clear**, and the fourth is in `BattleUnit_HandleReactionAnimationEvent` | 1 | PROVEN |
| the deferred route inside `003250F0`: `0x2007/8/C/E` → `00307110` | jump table at `00325208`/`00325224` decoded from the image | 1 | PROVEN |
| ~~`003250F0` has no static caller of any enumerated form~~ **— REFUTED 2026-09-16 (FABLE): reached by `jne` from `002E70A0`; the enumerated forms omitted `0F 8x rel32`. The "handler table has no reader" inference was then itself refuted (`EE-12`, 2026-09-19): readers reference their own slots, not the base. Re-verified 2026-09-22 — all three run: `call [02CA4430]` id 4 → `00325260` at `00417B52`/`69`/`80`, `[02CA4440]` id 6 → `00325090` at `00417CC6`, `[02CA4470]` id 0xC → `003250F0` at `0041DC84`/`0041DD03`/`0041CEC6`; guards `lea`'d into the table by `002EA320`/`002EA5F0` (8 sites)** | boundary-free `.text` sweep (`E8`, `E9`, both `LEA` encodings; controls `00265A4F`, `003251A4`), whole-file pointer/VA/RVA searches; owner-side re-verification of every dispatch edge | 1 | PROVEN |
| the flag is consumed per frame into table slot 3 | `00307050`–`00307071`, `0026ADDD` | 1 | PROVEN |
| no one-shot in helper or caller | `00300530` consults no flag before `0030082F` | 1 | PROVEN |
| script-side order `(group, mode)` | pop-order law only; no decompiled script | 2 (static) | PROBABLE |
| the `+0xF6` word is the record's script-assigned entry-group index (the bkei), written by verb `00BE` `setentrygroupall` and zeroed at init | `00263D30` is `movzx eax, word [rcx+0xF6]; ret`. The init loop's four `bp` stores (`0026CF63`/`0026D001`/`0026D0A7`/`0026D182`) all write `xor ebp,ebp`'d zero (`0026CED3`, never rewritten) inside `00358940`-resolved record loops. The live writer is `0025AE00` (`mov word [rax+0xF6], r12w` at `0025AE5A`), reached only from `00340970` = verb `00BE` `setentrygroupall` (dispatch slot `0x1EEEEE0`), which pops the value via `00267E10` and stamps records 0–4 of the bound slot `*(02099D70)`. Added 2026-09-20 (SWE2-CONTRACT) | 1 (static) | PROVEN |
| group `0` is the not-a-member sentinel — both ledger paths gate on `+0xE98` before indexing, so no group-0 completion can post | `00306E8F` and `00306F31` read `movzx edi, byte [rcx+0xE98]` then `test edi,edi`/`je` to the epilogue, ahead of the `group-1` ledger indexing at `00306EB2`/`00306F57`; `00239710` stores the verb's argument raw at `+0xE98`. Corpus side: 6,206 of 6,746 shipped `btlAtelSetEventFlagGroup` calls are `(0,0)` (the `spawnGroup` preamble default — FABLE's census, system page `EE-9`). Added 2026-09-21 (SWE2-CONTRACT) | 1 (static) + authored-data census | PROVEN |
| any runtime observation | ~~**none exists**~~ one: EXP-019, live and read-only, before any kill (the member mask set, the dead mask 0; §13). Nothing is observed across a kill (corrected 2026-09-29, FABLE) | EXP-019 | LIVE (pre-kill only) |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

**Two exact image-wide counts, and both reproduce with an independently written instrument.**

| claim | reproduced |
|---|---|
| exactly six functions address the ledger | **six**, and one `lea` each: `SpawnGroup_DispatchPendingCompletionSignals`, `_HasPendingCompletionSignal`, `_MarkCompletionPendingAfterReaction`, `_RecordMemberDeathAndHandleCompletion`, `_ResetLifecycleLedger`, `_UpdateExpectedMemberLaneMask`. **Zero image-base-register references** — this table is reached only RIP-relatively |
| the contract's own control, `02089340` | **126**, the number §15 states |
| bit 47 is touched at four sites only | **four**, now named: `00306FBF` and `00307110` **clear** with `movabs 0xFFFF7FFFFFFFFFFF`; `00306FFD` and `00325192` **set** with `movabs 0x800000000000` |

> **Reproducing a stated control is the strongest thing a census claim can offer**, and this one has
> it. When my count and the document's agree on a number the document chose in advance, the
> instruments are checking each other rather than one checking the other's homework.

### The unreachable arm, and why it is not trivial

`00235F83 movzx eax, dl` / `00235F86 test eax, eax` / `00235F88 js 0x235FA4` — a `movzx` from a byte
gives `0..255`, `test` can never set SF, and **that arm cannot be taken**.

What makes the claim worth stating is twenty-six bytes earlier: `00235F6C test ebx, ebx` /
`00235F6E js 0x235FA4` **is** reachable, because `ebx` came from `00235F56 movsxd rbx, edx`. **The
same function contains a live sign guard and a dead one**, and only the operand's provenance tells
them apart.

> **A cross-contract pattern, noticed here and worth naming.** `00235F70 movzx eax, byte ptr [rcx]`
> / `00235F73 **dec eax**` / `00235F75 cmp ebx, eax` / `00235F77 **jg**` is the *same* bound idiom as
> `00309F7B`–`00309F82` in
> [the inventory class storage](../12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md):
> **count minus one, compared signed**. Two unrelated subsystems, one construction — and in both, the
> `dec` is what makes a count of zero reject everything.

**Mechanical:** no body-size drift; banned-evidence sweep clean; all forty cited functions resolve.

> **One instrument lesson, mine.** My first ledger sweep looked only for RIP-relative operands. This
> contract's evidence says *"both addressing forms"*, and it is right to: the engine also reaches
> globals through a register holding `0x00120000`. Here that form contributes **zero**, so it changed
> nothing — but the sweep that would have missed it is the same one I ran on the workbench earlier
> today.

## 16. Parity plan

**Testable now, statically:** `CALCULATION` — the elapsed-seconds formula over a frame-counter and
scale sweep; the lane→record arithmetic; the completion test over generated mask pairs.
`STRUCTURAL` — both records against `_types/`. `EDGE-CASE` — every one of the seven prologue
failures, the zero-`memberMask` immediate completion, and the idempotent re-kill.

**Testable now, statically — added 2026-09-10:** `CALCULATION` — `00306E60` over the same slot sweep
as the death handler, both directions, asserting the dead-bit clear; the reset over a fully
populated ledger — **asserting `memberMask == 0 && deadMask == 0 && (flags & 1) == 0`, and
asserting that bits 1–7 of `flags` are PRESERVED**, which is the discriminating half: pre-fill the
byte with `0xFF` and require `0xFE` afterwards. *(Was "all three fields must read zero after it";
corrected 2026-09-13, `OPUS-LEDGER-RESET-BIT0` — that demanded the whole flag byte become zero,
which the reset does not do and which no evidence supports. A test written to the old wording would
pass on the shipped image, because nothing else uses bits 1–7, and would be asserting something the
code never promised.)* `STATE-TRANSITION` — register → die →
complete → re-register → die, asserting a second completion; register → retire → the remaining
members die, asserting completion of the reduced set.

**Requires the running game:** `STATE-TRANSITION` for the deferred route (the reaction event must be
raised by the animation system), `INTEGRATION` (the event lock and the table post reach the field
script), `PRESENTATION` (the two events are the visible half).

**Will not be tested:** `RNG` — none. `SERIALIZATION` — the ledger is BSS, zeroed at every area
initialisation and repopulated by script; nothing in the six functions that address it persists it.

> **The completion test is the honest pilot.** It is pure, it is two `u64`s and one comparison, and
> its edge case — a zero mask completing immediately — is a real behavioural claim a differential
> test settles in one sweep.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Status_Periodic_Terminal — SERVICE and CLIENT.**
  - The field frame `BattleSystem_RunFieldFrameOrchestrator` (`00234590`) resets action control through
    `BattleUnit_ResetActionControlForStatusTransition`.
  - `BattleUnit_UpdateLifecycleAndCombatFrame` (`00233F70`) runs `BattleUnit_RunPeriodicCombatMaintenance`.
  - Area initialisation removes a status through `BattleStats_RemoveStatusMode0`.
  - The HP write `00300530` changes status through `BattleStats_ChangeStatusAndProcessSideEffects`.
  - Among the clients of the raw tick counter (`0032A150`) that this contract cites are the periodic maintenance, the
    terminal-status recovery and `BattleFormula_ApplyGlobalPeriodicDrain…`. The terminal-status recovery and the
    status changer also call the presentation dispatcher
    ([the status write](../10-Status-Periodic-Terminal/CONTRACT-status-write.md)).
- **Rewards_Progression_Economy — SERVICE.**
  - Area initialisation builds the world pickup pool (`Loot_InitializeWorldPickupPool`).
  - The field frame ages and despawns pickups (`Loot_UpdateWorldPickupLifetimeAndDespawn`).

  So world pickups are created and aged by the spawn layer's own area and frame functions.
- **Gameplay — SERVICE.**
  - The HP write `00300530` looks up the target buffer (`BattleTargetBuffer_FindActorWorkIndex`) and dispatches a
    presentation event (`BattleUnit_DispatchActorPresentationEvent`). The group-death path `00306F00` also dispatches
    one.
  - That dispatcher calls `002EB030`, and it is also called by `Battle_EmitReactionPresentationForSlot`.
  - `ActorWork_GetBattleUnit` (`0031B760`) is shared with the stance and relationship queries
    `WorldActor_QueryCombatStanceState`, `WorldActor_HasActiveBattleActionOrUn…` and
    `BattleUnit_HasRelationshipClass2PlusInTrackedActorList`.
  - The timeline-event handler `BattleUnit_HandleActionTimelineEvent` (`00325260`) calls a 552-byte helper that reads
    the field action-permission bit.
- **InputGameplay — SERVICE.** The field frame calls a 289-byte Input-filed helper that also reads the field
  action-permission bit.
- **ActorEntity - CLIENT and SERVICE (93 edges).** `00233D20` is also called by bodies filed to ActorEntity: `0025C830`; `00233F70` reaches bodies filed to ActorEntity: `00236300`, `002671C0`, `00267240` - shared machinery across the layer boundary, no shared ownership.
- **Audio - SERVICE (1 edge).** `00313DB0` reaches bodies filed to audio: `002DEE70` - shared machinery across the layer boundary, no shared ownership.
- **Movement - SERVICE (23 edges).** `00233F70` reaches bodies filed to movement: `0023A070`, `0026A330`, `0033A240` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (11 edges).** `00234590`, `002350C0` reach bodies filed to party: `0023B040`, `003272A0`, `003273B0` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `002342F0` reaches bodies filed to random selection: `00328D80` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (1 edge).** `00427320` reaches bodies filed to resource: `002ED570` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (2 edges).** `002E1C20` is also called by bodies filed to save/load/settings: `005823B0`, `00582860` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (33 edges).** `00235F50`, `00235FB0`, `002366E0` are also called by bodies filed to script VM / native bridge: `0050F660`, `0050FAB0`, `005101F0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (5 edges).** `002E1C20` is also called by bodies filed to UI: `00276650`, `00279E20`, `0035CF10`; `00234590` reaches bodies filed to UI: `0035C7A0` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** Cited functions read `GameClock_GetRawTickCounter` (three times) and call a 72-byte core helper.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — SERVICE.** `00234590` on this page calls `BattlePerception_AdvanceCandidateCacheGeneration`, owned by that layer. What it reaches is **eighteen bytes** that give the generation counter its width: `[022C2578] = ([022C2578] + 1) & 7`, which is the same three bits the cache check compares `byte[+0xEA9] & 7` against; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_SetCurrentHP`, owned by that layer, calls `00300530` on this page. That caller is **eight bytes** that turn the delta-based HP path into an absolute set: it subtracts `dword[+0x48]` from the value it is given and jumps straight into the modification entry point - which is what fixes `+0x48` as the current value; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## The `00307140` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00307140` (~97 B) — `ecx` switch over the `002E1C20` arm
(`0030714A`/`0030714C`).

| member | role | interior |
| --- | --- | --- |
| `00359330` | `movsxd ecx` into the `022C8004` byte table, `r8d` gate (`00359334`/`00359344`) | [`00359334`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `002E1C20`.
