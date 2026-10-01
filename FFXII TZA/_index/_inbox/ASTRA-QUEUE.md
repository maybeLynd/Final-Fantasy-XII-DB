# ASTRA runtime queue — current availability in ASTRA.md

**Read the [final skeletal handoff](#astra-final-skeletal-queue-checkpoint--2026-09-20-utc),
then the [detailed correction](#astra-current-handoff-correction--2026-09-19).**
The dated queue below preserves history, including since-refuted
premises. Its old priorities, missing-control statements and reset date are not
the current launch plan.

ASTRA is READY/parked for the user's usage handoff. EXP127 captured skeletal
entry/body/return but then FF12 displayed a runtime-error dialog: full session
INVALID, observations provisional, consumer closure pending independent review.
FF12 and PC control are off; all26 save/config files and reference EXE restored.
Authorization is ACTIVE; read ASTRA.md for the exact offline return action.

One prepared queue for every question that genuinely requires live runtime state while ASTRA is
exhausted. ASTRA is **not an eligible dependency** during this window: nothing waits on it — a
worker preserves the exact request here, blocks only the affected boundary, and continues
role-appropriate work (or raises `BLOCKED_NEEDS_SPECIALIST` / a replan event if that leaves it
without worthwhile local work).

Before anything lands here, the requesting lane must have walked the cheapest-sufficient ladder:

existing evidence → static/call/data analysis → scripts/resources → isolated verified
original-code execution → ASTRA only if real runtime state is still required.

Preferred offline routes: **SWE2-ORACLE** for bounded original-code experiments, **SWE2-DATA** for
authored-data/resource questions, **SWE2-STRUCT** for bounded ABI/type/state questions. Evidence
standards do not drop: no runtime-dependent conclusion is guessed.

## TRIAGE 2026-09-13 (OPUS) — five of the nineteen need no game, and all five are mine

This file's own rule is *"every question that genuinely requires live runtime state"*. Nineteen open
items are addressed to ASTRA on the board. **Five of them are not live questions at all** — they are
notices, a disposition decision and two pieces of bookkeeping, addressed to ASTRA because ASTRA owns
the artefacts, not because they need the game running. **Every one of the five was filed by me.**

| item | what it actually needs |
|---|---|
| `OPUS-NOTICE-GUARD` | nothing — it records a near-miss, and says so in its own first line |
| `OPUS-NOTICE-SWEEP` | a decision about commit `2897620`: leave it, or follow up with the real EXP-030 message |
| `OPUS-NOTICE-GATEAXIS-CONCEDE` | a read of ASTRA's own publications for anything else resting on the withdrawn framing |
| `OPUS-REQ-ASTRA-EXP-METHOD-LAPSE` | `method:` and `live_game:` declared on seven experiment records, by their author |
| `OPUS-REQ-ASTRA-EXP-STATUS-VOCABULARY` | a judgement on whether EXP-008 meets ASTRA's own bar for `VALIDATED` |

> **WHY THIS MATTERS MORE THAN IT LOOKS.** ASTRA's live time is the scarcest evidence this project
> has. A returning session that opens a queue of nineteen and works down it spends the first part of
> a session with the game running on five items that a text editor would close. **These five should
> be cleared at the desk, before or after the live window, and they are listed here so that ordering
> is obvious rather than discovered.**

**The remaining fourteen are genuinely live-only** and stay in the batch: the mask and reachability
questions (`FABLE-REQ-ASTRA-LEDGER`, `-HANDLERS`, `OPUS-NOTICE-REWARDNULL`,
`OPUS-REQ-ASTRA-MGRMARK-RELOAD`), the round-trips (`-STATE-ROUNDTRIP`, `-BAZAAR-RELOAD`,
`-OLD-SAVE-LOAD`), the traces (`-ACTION-PHASE`, `-KIND-INDEX-TRACE`, `-REGFILE-REUSE`,
`-CML1-COLUMN-STABILITY`), the input discriminator (`-TITLE-KEYBOARD-DISCRIMINATOR`), the audio gate
(`OPUS-REQ-ASTRA-AUDIO-GATE-LIVE`) and the options bit (`-OPTIONS-BIT3`).

**I am not moving or closing anyone's items, including my own.** Reassigning a peer's request while
they are away is the kind of tidying that loses context, and four of these five carry questions ASTRA
should still answer — just not with the game running. The triage is a reading order, not a change to
the queue.

## Item format

- **QUESTION / TARGET / STATE / KNOWN EVIDENCE / COMPETING INTERPRETATIONS**
- **WHY OFFLINE IS INSUFFICIENT** — which ladder rungs were tried
- **EXACT DISCRIMINATING OBSERVATION** — the concrete read-out ASTRA must capture
- **DOWNSTREAM CLAIMS BLOCKED / SAVE-AREA-SETUP / PRIORITY / FAN-OUT**
- **COMPATIBLE BATCH** — items sharing a setup are merged into one session's work

Owners (the requesting lane) keep their entries elaborated progressively; SWE2-ORACLE absorbs
anything that turns out answerable by isolated original-code execution. On ASTRA's return,
FRONTIER re-triages: highest-fan-out truly live-only items first.

## Batch D — any loaded save (added 2026-09-13, OPUS)

### AQ-ARENA — what is the qword at `01F83530`? (P1, one read, fan-out 128)
- **OWNER:** OPUS (from the authored-table header work, EVIDENCE-STANDARD 13ah / 13ai)
- **QUESTION:** Is `[01F83530]` a non-zero authored-data **arena base**, or is it **zero**?
- **TARGET/STATE:** any state where authored tables are loaded — a loaded save, or the first field
  after New Game. One read. No input, no walking, no timing.
- **KNOWN EVIDENCE:** `0020E600` is 10 bytes — `mov eax,ecx / add rax,[01F83530] / ret` — and
  `0020E620` is its exact inverse, `sub ecx,[01F83530] / mov eax,ecx / ret`. **128 of the 351
  functions that reference an authored-data registry slot call `0020E600`** on the table header's
  `+0x0C` handle to reach a row. Separately, `003845F0` relocates four header fields — `+0x0C`,
  `+0x10`, `+0x18`, `+0x1C` — by adding the table's **own** 32-bit base, and calls `0020E600` twice
  itself while walking.
- **COMPETING INTERPRETATIONS, and the second is the simpler one:**
  - **(A) ARENA BASE.** Fields are stored as 32-bit offsets into one authored-data arena;
    `003845F0` rebases them within it and `0020E600` promotes a 32-bit value to a real pointer.
    Predicts `[01F83530]` == `table_ptr - low32(table_ptr)`, **identically for every table**.
  - **(B) ZERO, and both helpers are identity.** `003845F0`'s fixup already produces the final
    value, `0020E600` adds nothing, `0020E620` subtracts nothing, and the pair survives as a
    symmetry from the PS2 original where offsets *were* arena-relative. **Nothing in the image
    writes `01F83530`**, which is the evidence that makes (B) at least as likely as (A).
- **WHY OFFLINE IS INSUFFICIENT — every cheaper rung tried:**
  - *existing evidence*: five pages already describe `0020E600` as "the offset resolves through"
    it; **not one states the base's value**.
  - *static analysis*: both helpers and `003845F0` are fully decoded above. The code cannot say what
    a runtime global holds.
  - *call/data relationships*: `data_xref_scan` over all 34,270 bodies finds **exactly 2 references
    to `01F83530` image-wide, and both are READS**. A raw displacement sweep of the whole `.text`
    finds the same two and **zero sites outside any listed body**. **There is no writer to follow.**
  - *isolated original-code execution*: cannot help. Running the helpers under emulation reproduces
    the arithmetic already read off the instructions; it cannot supply the process's own value.
- **EXACT DISCRIMINATING OBSERVATION:** read the **qword at `01F83530`** once. **Zero ⇒ (B).**
  Non-zero ⇒ (A), and then read any registry table pointer — say `[02EBF138]` — and check that
  `[01F83530]` equals `table_ptr - (table_ptr & 0xFFFFFFFF)`.
- **DOWNSTREAM CLAIMS BLOCKED:** whether the authored-table `+0x0C` / `+0x10` / `+0x18` / `+0x1C`
  fields are offsets or pointers **after** relocation — which is the difference between a
  reconstruction that re-bases them and one that does not.
- **SAVE-AREA-SETUP:** none. No input, no navigation, no timing.
- **PRIORITY / FAN-OUT:** **P1, fan-out 128** — every consumer that reaches a row through the shared
  resolver depends on the answer, and the read costs one breakpoint.
- **COMPATIBLE BATCH:** merges with any item already requiring a loaded save; it needs nothing of
  its own beyond being past the title screen.

## Batch A — title screen (no load needed)

### AQ-1+AQ-6 — keyboard path discriminator + registration feasibility (P1, batched)
- **OWNER:** FABLE (requester of both `FABLE-REQ-ASTRA-TITLE-KEYBOARD-DISCRIMINATOR` and
  `ASTRA-INPUT-REGISTRATION-LIVE`)
- **QUESTION:** During a Return press at the title: does the poll run (`022CA5E0` advances), does
  DirectInput see the key (keyboard `+0x231+49` → 1), does the main-thread pass latch it
  (`+0x130+49`, `+0x30+49`), and does the menu move? Registration feasibility is the same four
  stages read on the same screen.
- **TARGET/STATE:** title screen, one Return press; watch `022CA5E0`, `02064AD3` (dispatcher mode
  must be 2/3/5), `[01F7FFE0]+0x39` (InputManager enable must be 1), keyboard block
  `[[[02EA5368]+0xDF8]+0x118]` bytes `+0x231+49`, `+0x130+49`, `+0x30+49`.
- **KNOWN EVIDENCE:** full static chain on the input-stack page sec.2 (FABLE-KBPOLL);
  `022CA5E0` is the only poll path (+1 per `InputControl_UpdateFrame`).
- **COMPETING INTERPRETATIONS:** unpolled (dispatcher mode wrong) / undelivered (DirectInput never
  sees it) / unlatched (main-thread pass drops it) / consumed-then-ignored.
- **WHY OFFLINE IS INSUFFICIENT:** every stage is observable statically only as a write site; the
  failing stage is a runtime state — which of the four fails cannot be derived from the image.
- **EXACT DISCRIMINATING OBSERVATION:** the four byte/counter values above sampled across a single
  title Return press.
- **DOWNSTREAM:** `FABLE-REQ-ASTRA-TITLE-KEYBOARD-DISCRIMINATOR`,
  `ASTRA-INPUT-REGISTRATION-LIVE`, and through them all live keyboard-driven tests (handlers,
  combat, same-session load).
- **SETUP:** launch to title only. **PRIORITY:** P1 — highest fan-out in the queue.

## Batch B — load/transition observers (share a zone-change setup)

### AQ-3 — actor-manager dispose mark across reload (P2)
- **OWNER:** OPUS (`OPUS-REQ-ASTRA-MGRMARK-RELOAD`)
- **QUESTION:** Is `022C6D20[m]` ever observed to go 1 → 0 across an area change?
- **KNOWN EVIDENCE:** static closure of all four clear-routes (one RIP store writes 1; neighbour
  store is byte-wide; 0/114,962 DIR64 relocs point into `[022C6D00,022C6D40)`; no decoded
  static-destination block clear spans it). Raise conditions fully mapped at `0025DA3A`.
- **WHY OFFLINE IS INSUFFICIENT:** only runtime can show whether a re-loaded manager whose mark
  is still 1 is torn down on the pass after its load completes.
- **EXACT OBSERVATION:** read `022C6D20[0..4]` before and after an area change.
- **DOWNSTREAM:** nothing blocked; CONTRACT FP-4 records the consequence either way. P2.

### AQ-2 — CML1 +0x04 column stability across load (P2)
- **OWNER:** OPUS (`OPUS-REQ-ASTRA-CML1-COLUMN-STABILITY`)
- **QUESTION:** After loading `byu_x0100`, does the CML1 entry's `+0x04` stay 14, and does
  `003DA28F` never execute?
- **KNOWN EVIDENCE:** static census — 28 reads / 0 writes with the exact addressing shape in the
  CML1 region; but a shape filter cannot see a computed-pointer write, `rep movs`, or a
  whole-record copy.
- **WHY OFFLINE IS INSUFFICIENT:** the residual is precisely the class static shape-census cannot
  exclude; one observed write or one survived load settles it.
- **EXACT OBSERVATION:** CML1 `+0x04` value before/after `byu_x0100` load; hardware-exec watch on
  `003DA28F`.
- **DOWNSTREAM:** publishing the CML1 index-binds reversal as settled. P2.
- **BATCHES WITH AQ-3** (both observe state across a load; same save/area-change setup).

## Batch C — combat/ledger (needs a live fight)

### AQ-8 — group ledger memberMask / slot-3 (P2)
- **OWNER:** FABLE (`FABLE-REQ-ASTRA-LEDGER`, board BLOCKED)
- **QUESTION:** After zone-in and before the first kill, is `memberMask` at
  `0x02EC13C0+(g-1)*24` non-zero with `deadMask` zero; on the last kill does ledger `+0x10` bit 0
  rise and slot 3 of `*(0x02098E68)` take `g` next field frame?
- **KNOWN EVIDENCE:** static chain complete — `00306E60` sets the bit via script verb `0x3030`;
  `00307030` consumes it; reset `00307090` zeroes at area init. No runtime observation exists.
- **WHY OFFLINE IS INSUFFICIENT:** the question is a value at a moment — no static route exists.
- **EXACT OBSERVATION:** memberMask pre-first-kill; ledger+0x10 bit0 and slot-3 one frame after
  the last kill.
- **DOWNSTREAM:** `FABLE-REQ-ASTRA-LEDGER`; contract stays CONTRACT READY until observed. P2.

### AQ-7 — reaction/timeline handler reachability (P1)
- **OWNER:** FABLE (`FABLE-REQ-ASTRA-HANDLERS`, board BLOCKED)
- **QUESTION:** Are `BattleUnit_HandleReactionAnimationEvent` (003250F0),
  `BattleUnit_HandleActionTimelineEvent` (00325260) and `00325090` ever entered, and from where?
- **KNOWN EVIDENCE:** exhaustive static negatives — no E8/E9/LEA targets, no 64-bit pointers,
  32-bit searches noise; neighbours reached normally.
- **WHY OFFLINE IS INSUFFICIENT:** "never called" needs a controlled zero — only a live
  breakpoint run across combat produces it.
- **EXACT OBSERVATION:** hardware breakpoints on all three across a combat sequence; capture the
  return address on any hit, or a controlled zero.
- **DOWNSTREAM:** `FABLE-REQ-ASTRA-HANDLERS`; EE-3/EE-4 closure past the static caveat. P1.
- **BATCHES WITH AQ-8** — the same combat session serves both.

## FABLE's seven unelaborated live requests — triaged 2026-09-13 (FABLE)

The TRIAGE above counts these seven among the live-only fourteen. They had no entry here. Each was re-walked against the
cheapest-sufficient ladder before it was written up: **one closes at the desk, two have offline routes now open, and four or
five are genuinely live.** The five fit two setups, so a returning session runs them in two passes.

| item | verdict | where |
|---|---|---|
| `FABLE-REQ-ASTRA-BAZAAR-RELOAD` | **desk: finish as superseded.** FZ-3 was answered statically (OPUS-NOTICE-FZ3-STATIC, FABLE.md), and `-STATE-ROUNDTRIP` already asks for the retirement. | no live time |
| `FABLE-REQ-ASTRA-OPTIONS-BIT3` | **answered statically 2026-09-18, no live time.** `FABLE-REQ-SWE2-DATA-OPTIONS-BIT3-STATIC` closed it: command 4 is the in-game Config **Battle Mode** row (descriptor `01E0B930`, choice texts `0x431`/`0x432` = Wait/Active in `menu_command.bin` bank 1). Clear = Wait, set = Active. | AQ-13, closed |
| `FABLE-REQ-ASTRA-STATE-ROUNDTRIP` | live unless `FABLE-REQ-SWE2-STRUCT-MANUAL-SAVE-WRITE` closes it | AQ-9, Batch B |
| `FABLE-REQ-ASTRA-OLD-SAVE-LOAD` | live | AQ-10, Batch B |
| `FABLE-REQ-ASTRA-REGFILE-REUSE` | live | AQ-11, Batch B |
| `FABLE-REQ-ASTRA-ACTION-PHASE` | ~~live~~ withdrawn 2026-09-14, answered statically | AQ-12, Batch C |
| `FABLE-REQ-ASTRA-KIND-INDEX-TRACE` | live, passive | AQ-14, runs across every batch |

### AQ-9 — does a save at a save point re-capture the state block? (P1, Batch B; parked behind its offline route)
- **OWNER:** FABLE (`FABLE-REQ-ASTRA-STATE-ROUNDTRIP`)
- **QUESTION:** After changing one known battle-state-block byte in a field, then saving at a save point without leaving
  the field and reloading, does the reloaded block carry the changed byte?
- **KNOWN EVIDENCE (narrowed 2026-09-13, FABLE):** there is **no indirect handler**. `0020E5C0` fetches the save manager and
  tail-jumps to `_guard_check_icall`, which is `ret 0`. `SaveTransition_PrepareRuntimeImageForCapture` (`005844A0`) writes nothing
  into staging. The staging → submission writer `0057E310` is the slot-0 **autosave**, and staging's block is written only
  by `00229B40` (field transition, boot). A **manual** save's write operation and buffer are not located yet: the storage
  queue's op 9 is the full-image load into the active buffer (`0058111E`), and op 7 is an 8-byte header probe.
  **Offline closure is routed first:** `FABLE-REQ-SWE2-STRUCT-MANUAL-SAVE-WRITE`. If the manual save serialises the active
  image, this item closes without live time. **OFFLINE ROUTE CLOSED 2026-09-16 (SWE2-STRUCT):** the manual save's write is
  queue **op 8**, enqueued only by `SaveSlotTransaction_StateMachine` (`00581DA0`) state 7 (`00581F89`), and its element
  carries the **active** image `02164280` (`SaveImage_GetActiveRuntimeBuffer`, `00581DCA`-`00581DCF` -> element `+0x28`,
  size `0x56690` at `+0x30`; worker `003BAEB0` reads exactly those fields into the file write `00862620`). Staging and the
  submission buffer serve only the slot-0 autosave (`0057E310` -> `003BB9B0` direct). **The file is the live image, so the
  changed byte is predicted to persist (H1) — by direct serialisation, not re-capture.** Whether a live confirm is still
  wanted is FABLE's call; the structural question this item was parked on is answered.
  [save-image-buffers §5](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md).
- **COMPETING INTERPRETATIONS:** H1, the save path re-captures, so the byte persists. H2, the file carries the image from
  the last transition, so the byte is lost unless a transition happened after the change. **Settled offline 2026-09-16:
  a third mechanism — the manual write serialises the ACTIVE image itself, so the byte persists without any capture.**
- **WHY OFFLINE IS INSUFFICIENT:** the handler behind `0020E5C0` is selected at runtime, and SWE2-ORACLE cannot
  reproduce the populated save buffers in isolation.
- **EXACT OBSERVATION:** the byte before the change, after the change, and after the reload. Positive control: payload
  `+0x1044` (field id), which the transition path is known to write.
- **DOWNSTREAM:** every "inside the block, therefore it persists" containment argument (save payload map, bazaar, party
  pages). This has the highest fan-out of FABLE's live items.
- **SETUP:** a save next to a save crystal, and a cheap block byte to change (a gambit slot toggle).

### AQ-10 — what a 2018-size save does in the current build (P2, Batch B)
- **OWNER:** FABLE (`FABLE-REQ-ASTRA-OLD-SAVE-LOAD`)
- **QUESTION:** Loading a `0x4E690`-byte save: does the load report success, and does the battle-state block at buffer
  `+0x4E68C` keep the session's previous contents?
- **KNOWN EVIDENCE:** static prediction (commits 397c170 / 401e080 / d56646d). The reader requests `0x56690`, `00866A00`
  copies `0x4E690`, `00862590` reports 0, and no conversion step exists. `00233C10` checks only the stamp.
- **COMPETING INTERPRETATIONS:** H1, success with stale block contents, as predicted. H2, an unread path rejects the
  file before the read. H3, a conversion exists on a route the census does not follow.
- **WHY OFFLINE IS INSUFFICIENT:** the injected-buffer reading is done; only a real file through the real menu closes
  the unread-path residue.
- **EXACT OBSERVATION:** load one of `FFXII_004`–`008` twice, from a fresh boot and after loading a current save. Record
  the success or error text, the party and inventory shown, and the `+0x4E68C` stamp plus three block fields before and
  after.
- **SETUP:** the 2018 saves beside a current one. **BATCHES WITH AQ-9** (same load menu).

### AQ-11 — does a reused actor record keep the previous occupant's VM registers? (P3, Batch B)
- **OWNER:** FABLE (`FABLE-REQ-ASTRA-REGFILE-REUSE`)
- **QUESTION:** When a monster's storage record is released and reused by the next spawn, do `+0x64`..`+0x83` still hold
  the previous values at the new actor's first register read?
- **KNOWN EVIDENCE:** only `WorldActorScriptVM_InterpretBytecode` touches the range on any census route. The initialisers
  (`ActorStorage_InitializeRecord`, `00266AD0`, `00266BD0`) store nothing there, and the pool is cleared once at
  allocation (`002679F0`).
- **COMPETING INTERPRETATIONS:** H1, inherited (the static reading). H2, cleared or set by a route the census misses.
- **WHY OFFLINE IS INSUFFICIENT:** absence of a clear on every census route is not a controlled zero; reuse order is a
  runtime property of the pool.
- **EXACT OBSERVATION:** a write watch on one reused record's `+0x64`..`+0x83` from its release to the next occupant's
  first read, with the record address and both actor ids.
- **SETUP:** a field with respawning monsters. It can share Batch B's area changes, since respawn on re-entry reuses
  records.

### AQ-12 — who writes the action phase `BattleUnit +0x6B4` on a committed attack (P2, Batch C)
- **WITHDRAWN 2026-09-14 (FABLE): answered statically, so no live run is needed.** H1 holds. `BattleUnit_AdvanceStandardActionState` (`00304850`) loads `rsi = unit + 0x6B0` and advances the phase with 16 `inc byte [rsi+4]` sites through a 13-entry jump table. The census searched `[reg + 0x6B4]` only. See `cb439475` and native-command-seam.md UQ-108.
- **OWNER:** FABLE (`FABLE-REQ-ASTRA-ACTION-PHASE`)
- **QUESTION:** From `BattleUnit_CommitAction` (`0030F760`) to the unit's next idle frame, which PCs write `+0x6B4`, with
  which values?
- **KNOWN EVIDENCE:** static stores 0 (`0030F814`, `003106F2`), 2, 4 (`00300060`), 5 (`0030FA80`, `003130F2`), plus
  increments in the order handlers. Readers compare 0, 3, 6, 6–7 and ≥ 9.
- **COMPETING INTERPRETATIONS:** H1, the phase climbs to 9 through a store the census misses. H2, actions stay at 0/5,
  and the ≥ 9 compares belong to the order path only.
- **WHY OFFLINE IS INSUFFICIENT:** an indexed, pointer-relative or block-copy writer is exactly what the static census
  cannot exclude.
- **EXACT OBSERVATION:** a write log (PC, old, new) on one unit's `+0x6B4`, with the action id at `+0x714`. Positive
  control: the commit store `0030F814`.
- **SETUP:** any fight. **BATCHES WITH AQ-7 / AQ-8** (same combat session).

### AQ-13 — which Config option is options-word bit 3 (closed — answered statically)
- **OWNER:** FABLE (`FABLE-REQ-ASTRA-OPTIONS-BIT3`)
- **STATUS:** closed 2026-09-18 — no live time needed. The offline route answered it: command 4 is the
  in-game Config **Battle Mode** row; options-word bit 3 clear = Wait, set = Active (SM-5 on the
  time-stop registry page; full row/command/text evidence on
  `19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md`).

### AQ-14 — runtime census of resource (kind, index) requests (P2, passive across all batches)
- **OWNER:** FABLE (`FABLE-REQ-ASTRA-KIND-INDEX-TRACE`)
- **QUESTION:** which (kind, index) pairs the game passes to the resource API during an ordinary session.
- **WHY OFFLINE IS INSUFFICIENT:** register-held kinds are not enumerable statically, so "never loaded" has no static
  proof.
- **EXACT OBSERVATION:** a hit-counted log of ECX/EDX on entry to `0032E400` and `0032E620`, and RCX/RDX at `0032E7C0`,
  kept running through Batches A–C and extended by opening every main-menu tab, including the world map and the location
  map. Positive control: any `.ebp` request. Newly relevant: kind 7 ids `0xA2`–`0xA4` and `0x142 + n` (the map files; see
  the map screens page) should appear when a map opens.
- **DOWNSTREAM:** the inert/live verdicts on the lst / mg / mrp / btm / cl2 / as7 / dat / bin sheets.

## Non-runtime ASTRA items (author decisions — parked, not live)

### AQ-4 — EXP status vocabulary / EXP-008 (P2, OPUS)
- `OPUS-REQ-ASTRA-EXP-STATUS-VOCABULARY`: whether EXP-008's `RUN` status meets ASTRA's own
  VALIDATED bar, and whether a controlled status vocabulary is worth adopting. This is an
  **author judgement on ASTRA's own corpus, not a runtime observation** — it waits harmlessly and
  costs ASTRA one reply on return.

### AQ-5 — EXP-075..081 method/lapse frontmatter (P3, OPUS)
- `OPUS-REQ-ASTRA-EXP-METHOD-LAPSE`: seven records need `method:`/`live_game:` declared by their
  author. Same class as AQ-4 — parked, not live.

## FABLE addition 2026-09-14 — AQ-15 (BQ-27)

### AQ-15 — does any destructor take the sized-delete path that frees nothing? (P3, Batch A or D, fan-out ~1,600 destructors)

- **QUESTION.** BQ-27 ([object construction and destruction](../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md)
  §2.1a). About 1,606 deleting destructors test flag bit 0 (free at all) and then bit 2. Bit 2 set calls a sized
  `operator delete(this, size)` that `/OPT:ICF` folded onto `0016D6A0`, a bare `ret 0`. If the engine ever passes flags
  5 or 7, the object is leaked by design.
- **KNOWN EVIDENCE (static bound, FABLE 2026-09-14, `work/FABLE/pub140-scratch/tools/dtor_flags2.py`).**
  - 163 destructors match the immediate-size form (`mov edx, size` / `call 0016D6A0`). Their vtable slots are `+0x00`
    (149), `+0x38` (14) and `+0x18` (10).
  - Of the virtual calls through those slots, **no call site loads a constant 5 or 7**. Constants seen at `+0x00`:
    1 ×87, 3 ×69, 0 ×67, 4 ×4.
  - Most calls carry register-held flags (`+0x18`: 650; `+0x00`: 164; `+0x38`: 99), which static reading does not
    resolve.
  - Direct calls to these destructors: 33, all with flags not visible in the call window.
- **WHY OFFLINE IS INSUFFICIENT.** The register-held flags come from the callers' own arguments. Following them back is
  unbounded, and the population the page measured is ten times the form recognised here.
- **EXACT DISCRIMINATING OBSERVATION.** Do not break on `0016D6A0` itself: it is also the CFG check stub and is hit
  constantly. Instead, over a load, a field walk and one battle, observe whether any **bit-2 call site** executes. The
  163 sites are listed in `work/FABLE/pub140-scratch/bq27_bit2_sites.txt` (e.g. `00185833`, `00185883`, `001EF4E3`,
  `005AC8A3`). Equivalently, watch whether the preceding `test dl, 4` branch is taken with `dl & 1`. Either use a
  sampled software breakpoint over the listed sites, or a conditional break on `0016D6A0` whose return address is in the
  list. Record the first hit's destructor, `rcx` and `edx`.
- **DOWNSTREAM.** BQ-27 (leak vs never-taken), the object-construction page's §2.1a warning, and any memory-growth
  explanation for long sessions. **SAVE-AREA-SETUP:** any loaded save. **COMPATIBLE BATCH:** A (title) for a first
  pass, D for a loaded-save pass.

## FABLE addition 2026-09-15 — AQ-16 (FL-2)

### AQ-16 — the live half of the `02EBF018` ↔ `battle_message.bin` binding (P3, Batch D, two reads)

- **QUESTION.** `FL-2` ([the post-result events and the battle message table](../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) §2.5).
  **Everything cheaper is now exhausted**, which is why this is being queued rather than researched further.
- **WHAT IS ALREADY CLOSED, STATICALLY (FABLE 2026-09-15, `ffc9a94f`).** The load is traced in five steps:
  `002368D0` issues `003843F0(0x13, 00238850, "STATIC")`; the callback `00238850` calls
  `003846F0(&0208E680, blob, 0)` and tail-jumps to `00236C30(1)`; that arm calls
  `AreaData_BindAndRebaseSectionDescriptor` (`003845F0`) with `rcx = &02EBF018`, `rdx = (i32)[pack + 0xC]`;
  `+0xC` is directory entry 2; the manifest at `01E4D830` names entry 2 `battle_message.bin`; and pack entry 2
  is byte-identical to the sibling file in all nine languages. **Nothing about the file half is open.**
- **WHY OFFLINE IS INSUFFICIENT.** Static reading cannot show that the pointer the running game holds is the
  one this chain produces — only that this chain is the one in the image. A second loader, a patch, or a mod
  would not be visible to it. The row was written as a live check and it should be closed as one.
- **EXACT DISCRIMINATING OBSERVATION — two reads and one action, in this order.**
  1. With a save loaded, read the qword at `02EBF018`. It should be non-zero. Follow it and read the two
     dwords at `+4` and `+8`. **Expected on a `us` build: `102` and `8`.** On `de`/`es`/`fr`/`it` also `102`;
     on `ch`/`cn`/`in`/`kr` expect **`100`** at `+4` — the count is a property of the build, not the table,
     so a `100` on a Latin-script build would be the interesting result, not a failure.
     Also read `+0xC`, expected `32`.
  2. Read the dword at `0208E680`. It should be the same descriptor's **owner blob**, and because
     `01F83530` ships as `0` the stored 32-bit value should equal the pointer's low half. A non-zero
     `01F83530` would falsify the "encode/decode are identities" by-product and is worth reporting on its own.
  3. **Steal once from any enemy that carries goods**, then read the ring at `02EBB560`. Expect entries
     `0x33` / `0x34`. This is the half the row names explicitly and the only part that needs an action.
- **WHAT WOULD FALSIFY THE PAGE.** `[02EBF018]` null or pointing outside the loaded pack; `+4` disagreeing
  with the build's language; or the steal producing ring ids other than `0x33` / `0x34`.
- **DOWNSTREAM.** `FL-2` closes; the registry page's slot-7 row stops carrying "by content agreement";
  the evidence row in §8 upgrades from TRACED to CONFIRMED.
  **SAVE-AREA-SETUP:** any loaded save with a stealable enemy in reach. **COMPATIBLE BATCH:** D.

### AQ-17 — read a Phyre default buffer and the largest unknown spans in the store fill themselves in (P2, one read, no action)

- **QUESTION.** What is in `PDeferredLightingBase +0x50`, a **16,384-byte** span, and
  `PMeshParticleSystemBase +0x50`, **12,352 bytes** — the two largest unresolved spans in any
  Phyre type in `_types/fields.tsv`? Offline work has gone as far as it can and the reason is
  now understood rather than suspected.
- **WHAT IS CLOSED, STATICALLY (OPUS 2026-09-19).** Every Phyre object is `memcpy`'d at
  `0063C974` from a per-class **default buffer** at `descriptor+0xC0` — the engine's own term,
  from its diagnostic string at `00D584A0`. The buffer is in `.bss`, so it is **zero in the
  image**, and it is **built at runtime, once per class**, by `00639A60`: `memset` `0xA5`,
  default-construct into it through descriptor vtable `+0x50`, then copy each registered
  member's own default in at `00639C2D`. `00639A60` sets flags bit 31 at its own exit
  (`00639C55`) and both callers skip it afterwards. **This is why no static read can produce
  those bytes** — they do not exist until the class is first instantiated.
- **THE ADDRESSES ARE KNOWN AND FIXED**, from
  [`phyre-class-default-buffers.tsv`](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/phyre-class-default-buffers.tsv)
  (384 classes, three buffers each, generated from each class's own descriptor constructor):

  | class | size | `+0xC0` default buffer | `+0xC8` | `+0xD0` |
  |---|---|---|---|---|
  | `PDeferredLightingBase` | `0x41D8` | **`02CF9970`** | `02CFDB50` | `02D01D30` |
  | `PMeshParticleSystemBase` | `0x3248` | **`02D27BA0`** | `02D2ADF0` | `02D2E040` |

- **EXACT OBSERVATION — one read each, no game action, any loaded scene.**
  1. Read `0x41D8` bytes at `02CF9970` and `0x3248` bytes at `02D27BA0`.
  2. Report the bytes, or at minimum: whether the buffer is **all `0xA5`**, **all zero**, or
     **neither**; and for "neither", the offsets and values of every run that is not `0xA5`.
- **WHAT EACH OUTCOME MEANS, stated before the read so it cannot be fitted afterwards.**
  - **All `0xA5`** — the class is one that stops after the two memsets. `PDeferredLightingBase`
    is expected to be exactly this: its descriptor constructor sets flags bit 1 at `0064433A`,
    and `00639A60` returns at `00639AF4` when bit 1 is set; independently its vtable `+0x50` is
    `00657140`, which is `xor al, al; ret` — **the class has no default constructor**. If this
    is what comes back, the 16,384-byte span has no authored content at all and the store should
    say so, which is a *better* answer than the span it has now.
  - **All zero** — `00639A60` never ran for this class in this session; note which scene, and the
    read should be repeated after a scene that uses deferred lighting.
  - **Neither** — the buffer was built, and every non-`0xA5` run is a field with an authored
    default. Those runs map straight onto field rows, and the two spans stop being unknown.
- **WHAT WOULD FALSIFY THE STATIC READING.** `0xA5` appearing in a class whose vtable `+0x50` is
  a real constructor, or a fully-constructed buffer in `PDeferredLightingBase` despite bit 1 and
  the `xor al,al` stub. Either one means the flags reading in
  [class-descriptor-and-metadata-system](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
  is wrong and should be reported as a contradiction, not reconciled.
- **WHY IT IS WORTH A SLOT.** The same read settles the mechanism for all **384** classes at once:
  one buffer that is neither zero nor uniformly `0xA5` proves the builder runs and the copies land.
  **SAVE-AREA-SETUP:** none — any loaded scene. **COMPATIBLE BATCH:** any read-only batch.

## ASTRA current handoff correction — 2026-09-19

The user requests a durable checkpoint before another approximately six-day
usage absence. ASTRA is READY/parked, not working a live experiment. Permission
is ACTIVE; PC control is OFF; FF12 is CLOSED; @runtime is free. All 26 original
save/config files and the reference EXE were verified again after restoration.
See [ASTRA's newest checkpoint](ASTRA.md#astra-usage-limit-handoff--2026-09-19) and its
raw verification. This is not L1/L2 completion or a reconstruction transition.

The specifications below supersede conflicting older entries. An unselected
save/route or unqualified detector is an explicit preparation gap, not a runnable
recipe. Route that preparation to the existing offline lanes; do not spend live
time discovering controls again. The prior detailed fourteen-item handoff in
ASTRA.md remains supporting detail where not corrected here.

### AQ-18 — do the 778 bytes at `PersistentFlagPayload +0xCF6` ever hold anything? (P3, one read, no action, OPUS)

- **QUESTION.** `PersistentFlagPayload` (`0x1538`, save buffer `+0x200`, so base `0x02164480`) carries a
  single **778-byte** unobserved span at `+0xCF6`, running to `+0xFFF`. It is the largest unexplained range
  in the save payload and the only one left in that type.
- **WHAT IS ALREADY CLOSED, STATICALLY, AND IT IS A LOT — which is why this is queued rather than
  researched further.** Three independent offline passes have found nothing in it:
  1. the type's own evidence records a census of **all 70 callers** of `SaveImage_GetPersistentPayloadBase`
     plus the **28 callers** of the raw-buffer route — 36 displacements, **none in this gap**;
  2. a route-seeded census over `FN 0x002EF640+0x200` with the constructor seeded (OPUS, 2026-09-20)
     reaches 7 offsets — `+0x0`, `+0x1044`, `+0x1048`, `+0x104C`, `+0x1050`, `+0x1054`, `+0x1535` — every
     one already a declared row and **none in this gap**; it is strictly weaker than the 98-caller pass and
     was recorded as a negative so it is not retried;
  3. the region is **zero-initialised** — it lies inside the `0x1538` memset at `002EF2DB`/`002EF2E8`, and
     the sibling finding `OPUS-SAVE-PAYLOAD-SPANS-ARE-ZEROED-WHOLESALE` puts the whole payload inside
     `memset(02164280, 0, 0x56690)`.
- **WHY OFFLINE IS INSUFFICIENT.** Every pass above is a statement about *this image's* code paths. It
  cannot distinguish "nothing writes it" from "nothing we can follow writes it" — a writer reaching the
  region through a base no census models would not appear, and this type has already produced one such
  case elsewhere in the store. Only looking at the bytes in a running game separates the two.
- **EXACT DISCRIMINATING OBSERVATION — two reads, no action, in this order.**
  1. **The control first, because a null result is only meaningful if the buffer is live.** With a save
     loaded, read the dword at `0x021654D4` (payload `+0x1054`, the row named `options`). `EXP-106` executed
     the field runtime pass from shipped bytes and its mode chain reads exactly this cell every frame, so on
     a loaded save it should be **populated, not zero**. If this reads zero the buffer is not bound and the
     rest of the observation is void.
  2. Read the **778 bytes at `0x02165176` through `0x0216547F`** (payload `+0xCF6..+0xFFF`).
- **WHAT THE TWO OUTCOMES MEAN, stated before the read.**
  - **All zero, control passing** → the region is dead space in the save format, reserved or padding. That
    is a *bounded* result, not proof for all saves: it would be one save's state, and the row should say so.
    Worth repeating once on a late-game save before it is written as a general claim.
  - **Any non-zero byte** → something writes it that no census can follow, and the offset and value of the
    first such byte are the whole finding. That immediately becomes an OPUS question about which writer,
    and it falsifies the reading that the payload's unknown space is merely zero-initialised.
- **WHAT WOULD FALSIFY THE PAGE.** Non-zero content in a region three offline passes report as untouched.
- **DOWNSTREAM.** Either way the row stops saying only "no censused access; semantics open": it gains a
  live observation with a named save state. If the region is dead, 778 of the payload's unknown bytes are
  dispositioned rather than open.
  **SAVE-AREA-SETUP:** any loaded save; a late-game save is strictly better for the repeat. **COMPATIBLE
  BATCH:** any — this is two reads with no action and no navigation.
  **RAISED BY:** OPUS, 2026-09-20, after the offline directions were exhausted and recorded as negatives.

### AQ-19 — is `CharacterRenderObject +0x118` ever non-zero? (P3, one pointer chase and one read, no action, OPUS)

- **QUESTION.** `CharacterRenderObject` (`0x668`, heap) carries a **632-byte** span at `+0x118`, the
  largest unexplained range left in any non-Phyre routeless type. Its page
  ([character-render-object.md](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md))
  already closed every offline direction and ends on the standing caveat: *"a route computed in a form the
  taint does not model, or one that exists only at run time, would look identical."*
- **THE FIRST HALF OF THAT CAVEAT IS NOW CLOSED TOO (OPUS, 2026-09-20).** Two addressing forms were added
  to the taint that day — a pointer passed as a **stack argument** (slots 5+), and the
  **image-base-relative** element base — and the type's census was **re-run with both** and came back
  **byte-identical**: 91 offsets, highest `+0x664`, nothing new. The vtable-seeded census that produced it
  is itself the strongest arg0 evidence available (all 31 slots at `00903B68`, control 3/3). So the
  remaining possibility is the second half: **run time**.
- **WHAT IS ALREADY KNOWN ABOUT THE CONTENTS.** `+0x80` and `+0x118` are **one 792-byte construction
  unit**: the constructor zero-fills a `0x318` stack buffer and block-copies it to `this+0x78` in a
  six-iteration unrolled loop plus a `0x10 + 0x8` tail, and `8 + 144 + 8 + 632 = 792` accounts for the
  region exactly, ending where `auxVec36Begin` (`+0x390`) begins. **It is zero at construction and never
  cleared afterwards** — the object comes from an unzeroed heap, so anything found in it was written.
- **HOW TO FIND AN INSTANCE — the part that was missing until now (OPUS, 2026-09-20).**
  1. Read the qword at **`0x01F81248`**. This is the container every instance is created into: the
     allocating function `FUN_001BD4A0` takes it as argument 0, and **both** of its callers (`0017F0D0`,
     `001BC190`) get it from the eight-byte getter `001BDAB0`, which is literally
     `mov rax, qword ptr [01F81248]` / `ret`.
  2. Read the dword at **container `+0xFC`**. **CAUTION, and this is the control:** it counts
     **attempts, not live objects** — `001BD539` branches to the allocation-failure path and the
     `inc dword ptr [rbp + 0xfc]` at `001BD54F` sits on the *merged* path, so a failed `0x668` allocation
     still bumps it. A non-zero value means the path has run; it does **not** mean that many objects exist.
  3. The container exposes the objects through a head at **`+0x28`** and a second slot at `+0x38`. Their
     layout is **not** established — reaching an actual instance from there is the one genuinely open step,
     and a debugger walking the head is the expected way to do it. Any instance will do.
  4. On an instance, read **632 bytes at `+0x118`**.
- **WHAT THE OUTCOMES MEAN, written before the read.**
  - **All zero** → the span is construction-unit padding that nothing ever writes, and 632 bytes are
    dispositioned. Bounded to the instances sampled; say which and how many.
  - **Any non-zero byte** → something writes it that the vtable census, the direct-call routes and both
    new taint forms all miss, and **the offset of the first such byte is the finding** — it points at the
    writer far better than another offline pass would.
- **DOWNSTREAM.** Either way the largest routeless-type gap in the store stops being open-ended. If the
  region is written, it reopens the page's "every indirect target is resolved" conclusion, which is worth
  knowing on its own.
  **SAVE-AREA-SETUP:** any scene with characters rendered — a field map with the party visible is enough.
  **COMPATIBLE BATCH:** any.
  **RAISED BY:** OPUS, 2026-09-20, after the offline half of the page's own caveat was closed.

### ASTRA shared controls and stop conditions

Every future C run needs a fresh exact reference EXE/module/tool identity, new
save/config census and disposable state, Cloud-off proof, actual initial-state
proof, positive detector controls, retained raw transitions and cleanup. Current
reference is the Steam installation named in ASTRA.md, EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Requalify it; do not reuse closed PID34568 or earlier pointers/handles.

Known modern save: `76561198045890736/FFXII_000`, 5,331 bytes, SHA256
`859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825`,
Stepping, SAFH56690. Legacy sample: `76561197960267366/FFXII_004`, 7,066 bytes,
SHA256 `8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc`,
Southgate 006:53:57, SAFH4E690. A filename is not enough: verify bytes and loaded
field/player state. Other scenes below do not yet have a selected save.

Use the existing EXP079/080 read observers, EXP037 recovered command observer,
and EXP030/038 trace instruments only where their exact controls qualify the
required observation. No blanket qualification transfers from a one-second
positive to a longer capture, write watch or stack observer. Before combat,
establish input sent -> registered -> accepted/queued -> executed -> consequence.
Snapshots do not exclude intermediate writes. Equal bytes do not prove idle.
Label all interventions; a forced call/write does not prove normal reachability.

Stop at the declared event/time/health bound, failed control, identity/state
drift, user stop or takeover. Never automatically restart after takeover.
For any proposed negative, declare detection coverage first. A failed or
zero-case instrument run cannot settle the claim. Close/detach, verify restored
state and responsiveness/exit, and release PC control when unused.

### ASTRA current live residue and exact experiment specifications

**Phyre — `OPUS-REQ-ASTRA-PHYRE-HIERARCHY-AT-RUNTIME`. A mapping diagnosis
first, C only the remaining runtime link question.** EXP124 captured 173
default spans and 180 parent nodes. The supplied `CD3D11_BLEND_DESC` address
02CF6678 failed +30 name-pointer identity (value 0x10); the other three D3D
rows were not attempted. H1: wrong address/layout; H2: valid class metadata
requiring another actual state. OPUS must distinguish those statically before
another run. Discriminator: a qualified descriptor name/size/layout and its
actual +78 link. Title-only is sufficient only if the corrected mapping is
initialized there. Reuse EXP124 read controls and a one-class pilot; stop at a
failed identity. Do not repeat the 173 spans to fill four gaps. OPUS owns repair.

**Phyre eventual defaults — seven open initialization claims, not a new count
target. C only if original construction cannot supply the requested semantics.**
EXP124 observed bit31 clear and zero buffers for POccluderGeometryInstance,
POccluderGeometryObject, PQuarryComponent, PScriptableComponent, PTrigger,
PTriggerReceiverComponent and PTriggerReceiverTypeCallbackData. H1: preparation
later creates nonzero values; H2: prepared values stay zero/poison. Discriminator:
same qualified descriptor/C0 before and after an observed preparation transition,
with exact triggering resource/ordinary call. OPUS/FABLE first select a native
resource/scene that instantiates one class; no route/save is selected yet. A
labelled injected preparation could answer its intervention arm only. Do not
interpret the title zeros as eventual defaults or seven A5 buffers as usable
objects. Audit/integration of existing bytes is A and continues immediately.

**Handlers — `FABLE-REQ-ASTRA-HANDLERS`. A consumer reconciliation first.**
The original missing-reference premise is refuted. EE-12 now records guard
conditional jumps, registration, and 35 slot-relative reads in the table range.
Class04 calls id4 at 02CA4430 (00417B52/69/80). The intermediate FABLE notice
about watching base02CA4410 predates that finding. Neither old experiment should
run unchanged. FABLE must agree closure of the existence question or identify a
remaining specific normal event. For that C residue: H1 named event dispatches
the selected registered slot/handler; H2 a different route is observed. Capture
that exact slot, caller/return and event/action identity, with a known registered
dispatch as positive. A base-slot watch cannot detect every slot; choose exact
addresses/coverage after the event is named. Current save/trigger is unselected.
Stepping is only a candidate, not a proven enemy-kill route. Keep actual gameplay
execution unknown until observed. Consumer request: ASTRA-REQ-FABLE-EE12-POST-READER-RESIDUAL.

**Trace qualification — `ASTRA-HWBP-LOADED-DEADLINE`. A review first.**
EXP031 contains bounded positives and a separate post window, but attempted
input timestamps missed the matched protocol. H1 timestamps meet declared
tolerance; H2 they do not. Existing evidence establishes H2. Review7e018ec8
covers the first recovered positive only; EXP037 pins arrived in839793b85.
If a downstream claim still needs matched C qualification, use the known
Stepping idle/menu state, entry003A1C50, recorded baseline/capture/post timing
and repeated detach/liveness controls. Resolve a feasible timing method before
launch; no repetition of the failed interactive schedule. This is an instrument
boundary, not a global input blocker.

**Ledger — `FABLE-REQ-ASTRA-LEDGER`. C.** H1 final-member death posts completion
on the next field frame; H2 different timing/route. EXP019 already has group1
member=1, dead=0, flags=0, slot3=0; player KO supplied no enemy-kill evidence.
Reidentify Stepping group via unit+E98 and table02EC13C0+(g-1)*24. Observe final
death, +10 bit0 and u16 slot3 of *(02098E68), with group/unit/frame and actual
executed action controls. Healthy approach/kill recipe is still unvalidated.
Stop on health floor or failed target/command proof. Only completion timing waits.

**Same-field save — `FABLE-REQ-ASTRA-STATE-ROUNDTRIP` and bazaar arm of
`OPUS-REQ-ASTRA-TWO-PARITY-CLAIMS-ARE-LIVE-ONLY`. C if existing captures do not
already bind the changed value.** H1 ordinary sale/purchase changes B's byte
and the saved payload at the mapped offset; H2 synchronization occurs later or
elsewhere. B=*(02EBF190), image+4E68C; candidate tally+57C8+id or flag+59C8+row.
Select a known item/row, modern disposable save, same-field shop and crystal
route offline first (not yet selected). Capture before/after ordinary action,
decoded save and reload, with field/header+1044 and inventory/tally positives.
Do not substitute a memory write for ordinary persistence. No original slot
overwrite. `FABLE-REQ-ASTRA-BAZAAR-RELOAD`'s old first-bind mask claim already
has FABLE's static return; consume that separately without another live test.

**Old-save same-session residue — `FABLE-REQ-ASTRA-OLD-SAVE-LOAD`. C.** EXP080
already proves the fresh-boot old-save load; do not replay it. H1 modern binding/
keep state survives old load; H2 restore/reinitialization or swap occurs. Need a
distinguishing nonzero keep-bank state (the old zero captures cannot decide),
then verified modern -> title/load -> legacy in one PID. Use saves above and
EXP079/080/081 field/header/B/keep/resource/roster observers, plus visible state.
Ordinary return-to-title/load route still needs a proven recipe. Stop before
repeating an unregistered input or overwriting a real save.

**Actor lifetime — `FABLE-REQ-ASTRA-REGFILE-REUSE`. C.** H1 +64..83 inherits
the prior occupant's registers; H2 native initialization precedes first read.
Choose a repeatable spawn/despawn script/save offline (unselected). Track
allocation and logical occupant/generation, release -> reuse -> first VM read,
with a validated write detector and known register-write positive. Point samples
alone cannot exclude clear/rewrite. Only this reuse boundary waits.

**Resource requests — `FABLE-REQ-ASTRA-KIND-INDEX-TRACE`. C.** H1 suspect
kind/index is used on a named ordinary route; H2 not observed on that route.
First segment can be boot -> title -> known Stepping load. Record ECX/EDX at
0032E400/0032E620 and named arguments at0032E7C0, with known .ebp/.mpk requests
as positives. Pin requested tuples/resources beforehand. Later scene/menu/area
segments need separate named triggers. Bounded route zero is not global absence.

**Path allocation — `FABLE-REQ-ASTRA-EO3-PATH-POINTER`. C.** H1 heap paths stay
below2GB on the selected route; H2 allocation crosses the signed32-bit boundary.
Record full RDI at0032E846 and the post-move EDX separately, then consumer
sign extension at0032E105 and continuation/001D6E20 read. Boot and one Stepping
load are candidate segments. Positive: ordinary named path request with observed
successful consumption. Preserve pool identity associated with022D89BC. Do not
claim the EDX value before its instruction executes, force a bad pointer, or
turn all-low samples into a permanent allocator guarantee. Failure ends the run.

**Camera column — `OPUS-REQ-ASTRA-CML1-COLUMN-STABILITY`. C for temporal claim.**
H1 byu_x0100 CML1 entry+4 remains authored14 until its readers; H2 a write/rebind
intervenes. Select the exact resource/entry and reachable scene/save offline
(unselected). Observe load and reader boundaries003DA456/003DA35E/003DD29F,
with covered writes and resource-identity positives. Zero hits at003DA28F or
equal endpoint samples cannot exclude another writer. Only the temporal claim waits.

**Manager reuse — `OPUS-REQ-ASTRA-MGRMARK-RELOAD`. C.** H1 a mark stays set;
H2 reuse clears it. Choose an area transition proving unload/reload of the same
manager index/resource (unselected). Observe022C6D20[0..4] and manager
02098E10+m*288 +10/+11, with actual lifecycle controls. A1->0 pair falsifies
sticky;1->1 does not prove no intermediate clear or next-pass teardown. Batch
with a load only when it establishes the required reuse.

**Shake scheduling — `FABLE-REQ-ASTRA-MT-CURSOR-ACROSS-A-CAMERA-SHAKE` and
`OPUS-REQ-ASTRA-SHAKE-DRIVER-OCCUPANCY-PER-FRAME`. C.** H1 nonzero drivers
consume16 shared MT draws each frame, including finished state2; H2 scheduling/
occupancy differs. Read gameplay cursor02EB4230 with initialization02EB4234,
the four driver states at manager+170, stride18, word+8, and actual frame identity.
Compare quiet field, ordinary battle, and a named camerashakestart_1a3 scene
before/during/after duration but before clear. Exact scene/save and manager
binding are not selected. Count nonzero states, not only visible shaking.
Positive: verified driver activation/clear plus a qualified MT draw observation.
Other consumers and cursor twist/wrap must be accounted for; raw cursor subtraction
cannot alone attribute16 draws. Capture other draw callers/order if needed.
Do not claim per-frame distribution from unsynchronized sampling. Static count
and loop bound remain usable; only actual occupancy/scheduling consequences wait.

**Transform deposits — title arm of `OPUS-REQ-ASTRA-TWO-PARITY-CLAIMS-ARE-LIVE-ONLY`.
C only if title idleness remains a required claim after capture review.** H1 four
16-byte slots022D9300/022D91A0/022D9310/022D8F90 are idle over a declared title
interval; H2 they are written. No save needed. Read before/after with qualified
write coverage and a known actual writer positive for each claimed coverage.
Different values falsify idle; equal samples alone cannot prove it. Define a
short interval and detector feasibility before launch. Exact arithmetic remains B;
this observation is neither integrated parity nor proof of whole-game idleness.

**Audio gate — `OPUS-REQ-ASTRA-AUDIO-GATE-LIVE`. C.** H1 byte02091098 selectively
gates UI sound; H2 all/no audio changes or another state explains silence. Known
field/UI sound, original byte, labelled reversible gate write, known ungated
audible call00271500 or selected inline path, restore, repeat positive. Requires
qualified stereo/audio capture and selected ungated trigger (not yet prepared).
Separate arms test ordinary voice+1C=7F/+20=40 and00249C60 versus00249CA0
transition liveness. Bound each arm; restore actual old byte. Memory alone cannot
prove silence. No negative without audible controls.

**Force-fight sound — `FABLE-REQ-ASTRA-UQ149-BANK-LOCAL-0X52`. C.** H1 current
bank maps index52 to a valid handle; H2 no bank/another mapping. In a known field
hold the documented R2-equivalent force-fight input; prove registration and
toggle022CBE1A bit4, then capture02AEF3FC and resolver003A1180 return for52 with
bank row identity at02AEEDC0. A snapshot of bank alone is not the returned handle.
Use accepted toggle/release as positive and cleanup; bound to one hold/release.
Do not infer the sound's audible identity from a numeric handle. Exact safe
field/input route must be confirmed from existing control records before launch.

**Rear-half pan — `FABLE-REQ-ASTRA-REAR-HALF-VOICE-PAN-LISTENING-TEST`. C.**
H1 pan240 is heard right (static111 degrees); H2 left/mirrored or later altered.
Preferred exact trigger is bhm_c0100 voicepan(0x01000000,240); alternatives are
naf_b0401 pan215 and grm_a0200 pan250, requiring their own predictions. No save/
scene route selected. Validate left/right output with known positive cues and
stereo capture; identify actual voice/verb. Alternatively read Sound+1B8 target+C
and +1E8 frpan after acceptance, but this answers interpolator state only and
leaves audible side/channel mapping open. Do not collapse those two conclusions.

**Reward initialization — `OPUS-NOTICE-REWARDNULL`. A/B first.** EXP075/076
already distinguish positive-count index rejection, zero count, missing descriptor
and resolver failure. Peers consume those and authored-index results now. A new C
arm needs an explicitly named storage-lifetime/initialization hypothesis, actual
resource/owner generation, and a positive binding/unbinding transition. No such
save/trigger is currently prepared. No repeat arithmetic fixtures as live evidence.

### ASTRA answerable without a new live session

- `OPUS-REQ-ASTRA-ARENA-BASE`: DONE from EXP079's four controlled zero samples;
  no new launch. EXP124 default-byte request is likewise captured, with the
  initialized-state limits above. Both raw audits/consumer interpretations are A.
- `FABLE-REQ-ASTRA-ACTION-PHASE`: requester withdrew it after cb439475 found
  the +6B4 writers using rsi=unit+6B0. Retire the obsolete request administratively;
  do not label the static result a live action trace.
- `FABLE-REQ-ASTRA-OPTIONS-BIT3`: A UI/resource binding first. H1 battle wait/
  active option; H2 another option. If genuinely unresolved, only then C: one
  named Config toggle with u32*(0215E6E0) before/after and another known bit as
  positive; restore backed-up setting. No broad live toggle hunt.
- `FABLE-REQ-ASTRA-TITLE-KEYBOARD-DISCRIMINATOR` and
  `ASTRA-INPUT-REGISTRATION-LIVE`: positive controls were recovered; they no
  longer block input. Optional historical causal C question only: poll022CA5E0,
  mode02064AD3, enable[01F7FFE0]+39 and keyboard arrays+231/+130/+30 index49,
  against a held Return positive/no-input control at title. Vary one parameter,
  stop at failed detection. Do not repeat this solely to resume working controls.
- `FABLE-REQ-ASTRA-KEYMAP-STEAMID-FOLDER`: A retained directory/account evidence.
  H1 generated folder equals the signed-in SteamID64; H2 it differs. Compare
  actual account identity with retained folder name. No launch/instrumentation.
  Folder equality alone does not prove every use of the stack pointer is safe.
- `OPUS-REQ-ASTRA-NONFUNCTION-ANNOTATION-EXPORT`: A offline Ghidra/tooling.
  H1 cited non-function annotation state matches across certified parents;
  H2 material change. Use pinned parents and content diffs, with a known changed
  symbol/type/comment as coverage control; function-only FAS2 cannot settle it.
  OPUS's population notices progress53->163->118->80 or147 conditionally; preserve
  those dates/verdict dependencies. FRONTIER routes existing offline ownership;
  canonical adjudication remains OPUS. No live runtime dependency.
- `OPUS-REQ-ASTRA-PASS5-INDEPENDENT-IMPORT`: the original access premise was
  withdrawn by OPUS in3bc5747d. Inspect that return/independence limits offline;
  do not launch FF12 or repeat a headless import solely because it is addressed
  to ASTRA. Same tooling and -noanalysis limits remain explicit.
- `OPUS-REQ-ASTRA-REGENERATE-PARENT-RESIDUAL-ARTIFACT`: A checkpoint tooling.
  H1 role directory is current with stale residual; H2 superseded. Reconcile
  current certified identity and expected count/hash with its owner before the
  existing verifier runs. Do not choose a flattering expected value or rerun
  the final audit prematurely. FRONTIER can route this while ASTRA is absent.
- `OPUS-REQ-ASTRA-EXP-METHOD-LAPSE`, `-EXP-STATUS-VOCABULARY`,
  `-EXP005-006-CONTRACT-KEY`, `-EXPERIMENT-CONTRACT-KEY-12`, and
  `OPUS-NOTICE-ASTRA-EXP-CONTRACT-FIELD`: A metadata/primary-record consumption.
  Compare actual execution evidence with declared method/status and contract
  scope. The two contract-key requests were explicitly withdrawn by OPUS;
  preserve69887238/1a6b8d83 and the remaining nine-none interpretation question.
  EXP008's resource comparison is not a live run just because a status is green.
- Other guard, sweep, export-population, live-floor and method-vocabulary notices
  are evidence/operating messages, not experiments. Read current corrections;
  no live-ratio target follows. `ASTRA-HANDLE-SEMANTIC-CLOSURE` stays a FABLE
  consumption dependency, not a reason to repeat EXP048 or reclaim peer files.

FRONTIER has `ASTRA-REQ-FRONTIER-OFFLINE-ABSORPTION-20260919`; OPUS has the
staffing notice, Phyre mapping and integration requests; SWE2-AUDIT-SPEC has the
EXP124 raw audit. Only the explicitly stated runtime-dependent conclusions wait.
No worker is logically blocked from independent database work by ASTRA's usage.

## ASTRA new arena request — 2026-09-20 UTC

`OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME` is distinct from the completed one-qword
request because it additionally asks whether003E3C30 actually executes with
shipped data. **A now:** EXP079's four controlled/bracketed zero reads and
readable low addresses are rechecked in ASTRA.md. **C still required for entry.**
Neither those samples nor an absence of static writers determines skeleton
storage kind/extent. OPUS receives ASTRA-CONTRA-OPUS-ARENA-ZERO-STORAGE-INFERENCE;
there is no canonical type change until the consumer reconciles it.

H1: a selected ordinary character pose/load reaches003E3C30; H2: no entry is
observed over that bounded trigger. Base state is a separate observation: zero
or nonzero at recorded sample times. A base0 with a valid low-address input is
also possible; do not impose the original two-way inference on the result.

Candidate setup: backed-up modern Stepping save identified above, visible
loaded models, exact reference/module/text/tool controls. Reuse EXP030's
duration-only capture and EXP031's qualified known-entry003A1C50 positive at
their existing short bound; choose003E3C30 coverage separately. The ordinary
trigger and whether entry is load-only or repeated must be established before
a zero can discriminate. No save/navigation/control rediscovery or new platform.
If capture cannot cover the actual trigger, revise the method rather than repeat
an idle zero. Entry registers/time prove only the captured intervention window;
require additional exact memory reads for any claim about skeleton/array values
at entry. No injected call, no forced pointer, no inferred allocation lifetime.

Stop at the declared short window, failed positive, identity/state drift or
user takeover. Retain detach/clear/readback and repeated post-detach liveness,
then ordinary close/save-config restoration and PC-control release. One observed
ordinary entry answers existence for that route; zero does not mean globally
dead. Base brackets do not prove the value at every intervening instruction.

Static preflight now distinguishes an empty-count entry from the needed body:
003E3C58 skips the loop when unsigned +8C is zero;003E3C7A follows the actual
index read and computed `base+230+index*290`, before00203170;003E3C7F follows
that call's return. The full109-byte function hash is in ASTRA.md. Use those
verified boundaries if the stronger body/return question is required; an entry
alone cannot answer it. Preserve each outcome independently, with the known-entry
positive within the existing four-slot limit or in a separately qualified window.
No native side-effect, storage-kind or lifetime inference follows from hit counts.

## ASTRA usage checkpoint and current routing — 2026-09-20 UTC

**Parked at preparation, not at a live failure.** EXP127 has not run. Its
[prepared recipe](../../_experiments/evidence/skeletal-reset-live/README.md)
records the competing hypotheses, exact four instruction boundaries, Stepping
save/hash, existing observer/input sources, detection controls, missing setup,
one-second limits and cleanup. The raw handoff receipt verifies26 save/config
files against the unchanged backup, reference identity, no FF12/instrument,
and PC control off. No uncommitted game result awaits interpretation.

**First future live candidate:** OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME, only its
ordinary003E3C30 execution/body/return residue. Method C; the base-value return
is already A. Resolve the existing source/task adapter and fresh backup/control
setup before launch. No ordinary trigger has yet been observed. A successful
known-entry control with no target hit is a bounded unobserved route, not proof
that the skeleton path is dead. Owner/extent questions remain separate.

**Current offline ownership, superseding earlier queue wording:**

- FRONTIER-REQ-SWE2-DATA-NONFUNCTION-ANNOTATION-EXPORT and
  FRONTIER-REQ-SWE2-DATA-PARENT-RESIDUAL-ARTIFACT carry the two tooling requests.
  DATA works offline; OPUS retains canonical adjudication and expected-identity
  agreement. Do not duplicate them on ASTRA's return.
- FRONTIER-REQ-AUDITSEM-EXP-METHOD-STATUS-VOCAB carries metadata/primary-evidence
  review; FRONTIER-REQ-CONTRACT-EXP-NINE-NONE-FIELD carries contract-scope review.
  EXP030's specific target-identity correction is also already routed to OPUS.
- FABLE-REQ-ASTRA-KEYMAP-STEAMID-FOLDER has FRONTIER's static return:
  keymap.ini is at the game root, shared across account folders. Consume
  FRONTIER-NOTICE-FABLE-KEYMAP-FOLDER-IS-ACCOUNT-SHARED; no live experiment.
- FABLE-REQ-ASTRA-OPTIONS-BIT3 is answered statically as Battle Mode Wait/Active
  (clear/set). The older optional live-toggle plan is unnecessary. The withdrawn
  action-phase and first-bind bazaar premises likewise need no new run.
- EXP124 raw audit, four D3D mapping diagnosis and current-byte integration are
  offline work for SWE2-AUDIT-SPEC/OPUS. Only a corrected, still-unobserved native
  initialization or parent-link question may return to the live queue.

The detailed live specifications above remain current for ledger timing,
old-save same-session state, actor reuse, resource/path requests, camera column,
manager reuse, shake scheduling and audio/presentation. Each names hypotheses,
discriminator, controls and required setup; an explicitly unselected save,
scene or detector is a preparation dependency for its owner, not permission to
invent a route. The handler existence premise needs FABLE's reconciliation
before any new experiment. Ordinary persistence requires a selected shop/crystal
route and verified accepted action; injected writes answer a separate question.

TEAM parks only the two incomplete skeletal live rows and preserves older
claim-specific blockers. The runtime reservation stays unclaimed. Peers proceed
with these offline routes and their independent database work; ASTRA usage is
not a global database blocker. Required unknowns and consumer contradictions
remain open. No experiment-count, live-ratio or L1/L2 completion claim follows.


## ASTRA final skeletal queue checkpoint — 2026-09-20 UTC

**READY/parked; FF12/PC control off; @runtime released; saves/reference restored.**
EXP127 ran the already-prepared two short windows and later showed a fatal C++
runtime error. The full session is INVALID; raw entry/body/return observations
are provisional pending review. The earlier UNRUN checkpoint is history. No
second attempt is authorized by a green API or CPU receipt alone; ordinary live
permission itself remains ACTIVE. See [EXP127](../../_experiments/EXP-127-skeletal-reset-live.md).

**Immediate next question is A, not C:** ASTRA-REVIEW-EXP127-FAILED-SESSION asks
whether the exact raw contexts/ordering support the narrow observations despite
the later failure. H1: retained boundary records are sound but healthy-session
promotion is unsupported; H2: a context/trace defect also contaminates the records.
Discriminator: original instruction/context semantics and raw event/cleanup order,
not a new game launch. Error cause is separately unknown. A later causal C test
requires a named failure hypothesis, repaired or narrowed instrument, explicit
post-test normal input/response and fatal-dialog check, with the same known
Stepping save and fresh identity/backup. No unchanged four-slot repetition.

The detailed specifications under **ASTRA current live residue and exact experiment
specifications** remain the runnable-design authority below their explicit missing
setup. This compact routing map prevents a READY notice being mistaken for a
prepared live experiment. Each row retains those competing hypotheses/observations;
an unselected route is a real preparation gap, not an implied exclusion.

| Queued question | Cheapest sufficient method and next action | Future C state/instrument prerequisite |
|---|---|---|
| Arena/skeletal entry | A review of EXP127 now; C only remaining accepted gap | Modern Stepping save above; repaired/narrowed trace, source pins, normal post-test response; no extent inference |
| Phyre hierarchy/defaults | A mapping repair and raw audit by OPUS/AUDIT-SPEC; B native construction where sufficient | Corrected four D3D identities; one-class pilot, actual initialization trigger for seven unprepared classes, EXP124 query/read controls; route unselected |
| Handler execution | A FABLE EE-12 reconciliation first; C named ordinary dispatch residue | Exact registered slot/event and caller, positive dispatch, save/trigger unselected; old base-only watch is insufficient |
| Group completion ledger | C after target→queued command→executed action proof | Stepping candidate; verified healthy kill route missing, group/unit/frame identity and ledger/slot3 transition detector |
| Same-field save / bazaar payload binding | A prior capture review, then C ordinary persistence | Selected shop/item/crystal route still missing; disposable modern save, state/header/save decode and inventory/tally positives |
| Old save after modern in same PID | C; EXP080 fresh-boot result already banked | Modern Stepping and legacy Southgate hashes above; nonzero keep state and proven return-to-title route; EXP079/080/081 reads |
| Actor register reuse | C for real lifetime; static/isolated clear logic remains A/B | Spawn/despawn route missing; allocation+occupant generation, qualified write coverage and first VM read |
| Resource kind/index / EO3 path pointer | C for actual requests/allocation | Named tuple/resource list and boot→title→Stepping segments; qualified exact entry/register/consumer trace; healthy-trace review first |
| Camera CML1 column | C for temporal stability; resources A | byu_x0100 entry and reachable save missing; load/write/reader coverage with identity positive |
| Manager dispose mark | C for actual reuse | Exact manager/resource transition missing;022C6D20 and +10/+11 lifecycle observations; equal samples cannot exclude an intermediate clear |
| Shake MT cursor / driver occupancy | C for scheduling;16-draw arithmetic B already independent | Quiet/battle/shake scene and manager binding missing; actual frame, nonzero state including2, other callers and wrap accounting |
| Transform title deposits | A existing capture review then C only required idleness claim | No save; four exact slots from detailed spec, write coverage with writer positive; equal endpoints insufficient |
| Audio gate and voice defaults | C for audibility/state; byte/arithmetic B | Stereo capture, ordinary gated and named ungated cue, reversible original-byte restore; ungated trigger still missing |
| Force-fight bank52 | C for actual bank/return | Documented R2-equivalent, registration/toggle positive in safe field, exact bank and resolver return; route/control confirmation pending |
| Rear-half voice pan | C audible output; B numeric mapping separate | bhm_c0100 pan240 candidate, route/save missing; stereo left/right positive and actual voice binding |
| Reward null initialization | A/B authored/native evidence first | C only named ownership/lifetime gap, with selected resource/generation and actual bind/unbind; no trigger prepared |

The original title-keyboard request has registered-input/visible-load evidence
(retained EXP031 controls and now this session's three Enter receipts); no input-access
blocker remains. Options-bit3, action-phase and bazaar first-bind premises have
static returns; do not rerun them. Keymap folder has FRONTIER's shared-root static
return. Export/nonfunction/PARENT regeneration, experiment metadata, contract-key
and audit notices are A and retain their existing DATA/CONTRACT/auditor/OPUS owners.
Older AQ15 sized-delete and AQ16 resource-binding designs remain historical queued
candidates only if their semantic owners identify a still-required runtime residue;
no broad destructor census or unspecific resource session is scheduled here.

**Exact return order:** consume the offline failure-aware audit and OPUS inference
response; reconcile claims/dirty files/processes; select only an actually prepared
HIGH/BLOCKING live-only residue. Do not repeat EXP079, EXP080 fresh boot, EXP124's173
spans or the failed EXP127 route. Peers continue independent database work now.
No unknown, contradiction or database requirement is closed by this handoff.


## TRIAGE 2026-09-20 (SWE2-FRONTIER) — board-level disposition while ASTRA is parked

ASTRA parks ~6 days. The board still holds ~35 items `assigned_to: ASTRA`; team.py has no
reassign op and only the owner can change a claim, so the mechanism is: (a) bounded
replacement tasks to offline lanes where work remains, (b) this table as the canonical
disposition record — on return ASTRA can claim+finish each marked row in one step, and
peers stop treating routed work as open. Rows marked **parked** are genuinely live-only
or author-decision; they are the reserve, not backlog.

### Answered, withdrawn or superseded — close on return (SWE2-FRONTIER triage)

| board item | disposition | provenance |
|---|---|---|
| `OPUS-REQ-ASTRA-NONFUNCTION-ANNOTATION-EXPORT` | routed offline | `FRONTIER-REQ-SWE2-DATA-NONFUNCTION-ANNOTATION-EXPORT` (DATA, P2) |
| `OPUS-NOTICE-ASTRA-NONFUNCTION-EXPORT-INPUTS` | folded as context into the DATA task | population corrections travel with this triage |
| `OPUS-NOTICE-ASTRA-EXPORT-POPULATION-118` | folded — population is 118 | same |
| `OPUS-NOTICE-ASTRA-EXPORT-POPULATION-80` | folded — 80 under the stated reading, 147 if refused | same |
| `OPUS-REQ-ASTRA-REGENERATE-PARENT-RESIDUAL-ARTIFACT` | routed offline | `FRONTIER-REQ-SWE2-DATA-PARENT-RESIDUAL-ARTIFACT` (DATA, P3) |
| `OPUS-REQ-ASTRA-EXP-METHOD-LAPSE` | routed offline | `FRONTIER-REQ-AUDITSEM-EXP-METHOD-STATUS-VOCAB` (AUDIT-SEM, P3) |
| `OPUS-REQ-ASTRA-EXP-STATUS-VOCABULARY` | routed offline | same task |
| `OPUS-NOTICE-ASTRA-EXP-CONTRACT-FIELD` | answered | `FRONTIER-REQ-CONTRACT-EXP-NINE-NONE-FIELD` — DONE, verdict: OPUS's `contract: none` rulings stand for EXP-023/025/028 |
| `FABLE-REQ-ASTRA-KEYMAP-STEAMID-FOLDER` | answered statically | `keymap.ini` sits **account-shared at the game root**, not inside either SteamID64 folder (`…967366` prior / `…890736` current, both hold only `FFXII_NNN` save dirs). Evidence notice `FRONTIER-NOTICE-FABLE-KEYMAP-FOLDER-IS-ACCOUNT-SHARED` filed to FABLE |
| `FABLE-REQ-ASTRA-BAZAAR-RELOAD` | superseded | FABLE's own 2026-09-13 triage: FZ-3 answered statically (`OPUS-NOTICE-FZ3-STATIC`), STATE-ROUNDTRIP carries the retirement |
| `FABLE-REQ-ASTRA-OPTIONS-BIT3` | answered statically | AQ-13 closed — Config Battle Mode row (Wait/Active), `FABLE-REQ-SWE2-DATA-OPTIONS-BIT3-STATIC` |
| `FABLE-REQ-ASTRA-ACTION-PHASE` family | withdrawn | `FABLE-NOTICE-ASTRA-ACTION-PHASE-ANSWERED-STATICALLY` |
| `FABLE-REQ-ASTRA-HANDLERS` (BLOCKED) | withdrawn | `FABLE-NOTICE-ASTRA-HANDLERS-REQUEST-WITHDRAWN-AS-ANSWERED-FROM-DATA` |
| `OPUS-WITHDRAW-ASTRA-TWO-CONTRACT-KEY-REQUESTS` | withdrawal record | the two contract-key requests it names are closed by it |
| `OPUS-REQ-ASTRA-PASS5-INDEPENDENT-IMPORT` | withdrawn | `OPUS-NOTICE-ASTRA-PASS5-PREMISE-REFUTED` — premise refuted, do not re-run |
| `OPUS-NOTICE-ASTRA-PASS5-PREMISE-REFUTED` | record | same |
| `OPUS-NOTICE-GUARD` | record | its own completion line: "No action required" |
| `OPUS-NOTICE-ASTRA-LIVE-QUESTION-FLOOR` | record | informational floor count |
| `OPUS-NOTICE-ASTRA-LIVE-FLOOR-IS-48` | record | same |
| `OPUS-NOTICE-GATEAXIS-CONCEDE` | record | OPUS's withdrawal stands on the record; the suggested self-sweep of ASTRA publications is a minutes-long check on return, not a routed task |

### Offline-routed this round (SWE2-FRONTIER)

| board item | new home |
|---|---|
| `OPUS-REQ-ASTRA-PREPUBLISH-CLEAN-GATE` | SWE2-FRONTIER (publication tooling owner) — adopt/adapt/decline ruling to be recorded against the proposal |
| EXP-124 raw review / EXP-127 failed-session review | already `assigned_to: SWE2-AUDIT-SPEC` — `FRONTIER-NOTICE-AUDITSPEC-EXP-REVIEWS-AHEAD-OF-SWEEP` orders them ahead of the promotion sweep |

### Parked — live-only or author-decision, the reserve (SWE2-FRONTIER)

Everything else `assigned_to: ASTRA` stays: `FABLE-REQ-ASTRA-STATE-ROUNDTRIP`,
`-OLD-SAVE-LOAD`, `-REGFILE-REUSE`, `-TITLE-KEYBOARD-DISCRIMINATOR`, `-KIND-INDEX-TRACE`,
`-UQ149-BANK-LOCAL-0X52`, `-MT-CURSOR-ACROSS-A-CAMERA-SHAKE`, `-REAR-HALF-VOICE-PAN-LISTENING-TEST`,
`-EO3-PATH-POINTER`, `OPUS-REQ-ASTRA-AUDIO-GATE-LIVE`, `-CML1-COLUMN-STABILITY`,
`-MGRMARK-RELOAD`, `-SHAKE-DRIVER-OCCUPANCY-PER-FRAME`, `-TWO-PARITY-CLAIMS-ARE-LIVE-ONLY`,
`OPUS-NOTICE-SWEEP` (P0 — asks ASTRA to confirm its staged state after commit `2897620`;
only ASTRA can answer), and BLOCKED `OPUS-NOTICE-REWARDNULL`,
`OPUS-REQ-ASTRA-PHYRE-HIERARCHY-AT-RUNTIME`, `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME`,
`FABLE-REQ-ASTRA-LEDGER`. Each parked row needs a falsifiable capture plan and a ready
consumer before it is scheduled — the batch specs above already carry most of them.

## TRIAGE 2026-09-20b (SWE2-FRONTIER) — ASTRA-RETURN consumed; one package prepared

Consuming ASTRA's resumed handoff (uncommitted +314, hash-pinned in
`work/ASTRA/resume-20260920/`; publication stays with ASTRA's own prepared
`publish.py` path — it binds to the ASTRA identity and its ACTIVE-claim
precondition, so it is not delegable). Both OPUS contradictions are consumed:
`71b9cfef2` accepted the four Phyre descriptors and **withdrew the live
reads**; `37d2e302a`/`991e25c1b` repaired AQ18's verdict logic. Board updates
to the 2026-09-20 triage table:

| board item | new disposition |
|---|---|
| `OPUS-REQ-ASTRA-PHYRE-HIERARCHY-AT-RUNTIME` (BLOCKED) | **withdrawn** — OPUS withdrew the live reads after accepting `71b9cfef2`; a new run needs a specific unresolved initialization claim, not the old mapping question |
| AQ-18 span (+0xCF6) | **withdrawn** — another zero sample cannot settle absence of use; the gap stays semantically open, not padding |
| AQ-19 (+0x118) | **still unprepared** — needs the container→instance walk (link offsets, ownership direction, `00903B68` vtable route) before a field-state sample means anything |
| `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME` (BLOCKED) | stays parked — genuinely live-only; spec already in Batch D |
| skeletal trace (EXP127 follow-on) | stays parked — needs AUDIT-SPEC's failure-aware review plus a named hypothesis/control |
| same-field save / STATE-ROUNDTRIP | stays parked — `FRONTIER-REQ-FABLE-MANUAL-SAVE-SHORT-PATH` is working the named-route prerequisite |

### ~~PREPARED~~ SUPERSEDED 2026-09-20c (SWE2-FRONTIER) — `AQ-1+AQ-6` title keyboard discriminator

**This selection was wrong and is corrected on ASTRA's return
(`ASTRA-RETURN-FRONTIER-TITLE-REQUEST-SUPERSEDED`).** `FABLE-REQ-ASTRA-TITLE-KEYBOARD-DISCRIMINATOR`
was already DONE — `ASTRA-RETURN-FABLE-INPUT-RECOVERY` (`3c8303b2`) says *close it without a
run*: ASTRA's re-reduction of the five existing raw pulses found index-49 (Enter) and index-2
(C) positives, and the input-stack page sec.2 consumed the verdict statically. The "all live
keyboard work gates on this" framing was therefore already false when this package was
prepared. `ASTRA-INPUT-REGISTRATION-LIVE` is likewise DONE. Nothing in this section should be
read as pending work; the old failure cause stays *unknown* per the return.

**What the corrected queue actually holds as the next live candidate:**

- `AQ-ARENA` (`OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME`, fan-out 128, spec already in Batch D)
  is **prepared but gated, not ready**: its BLOCKED `resume_when` waits on the
  failure-aware audit determining retained execution scope and OPUS reconciling
  `ASTRA-CONTRA-OPUS-ARENA-ZERO-STORAGE-INFERENCE`. The EXP-127 review is therefore the
  offline prerequisite for the highest-fan-out remaining item — it is not optional
  bookkeeping.
- `AQ-2` / `AQ-3` load observers (P2, specs complete) need a save and an area change.
- So: **no ungated prepared package exists today.** The queue's correct state is *READY
  awaiting the EXP-124 review/integration and the EXP-127 failure review* — exactly what
  ASTRA's return asks to preserve.

*The superseded preparation text is kept below for provenance.*

- **Consumer:** `FABLE-REQ-ASTRA-TITLE-KEYBOARD-DISCRIMINATOR` (READY, assigned
  ASTRA) + `ASTRA-INPUT-REGISTRATION-LIVE` (READY) — both FABLE-owned; the
  five-way verdict (a)–(e) is the request's own completion contract.
- **State/trigger:** title screen only — no save load, no navigation.
  Trigger: SendInput VK_RETURN with scan code `0x1C` held **≥100 ms**
  (350 ms worked in EXP-006).
- **Observations (reads only):** `022CA5E0` poll counter; `02064AD3`
  dispatcher mode; `[01F7FFE0]+0x39` InputManager enable; keyboard block
  `K = [[[02EA5368]+0xDF8]+0x118]` bytes `K+0x231+49`, `K+0x130+49`,
  `K+0x30+49` (index 49 = DIK_RETURN via remap `01F3DAB0`).
- **Bounds:** read-only, ~64 sampled bytes total, one synthetic keypress;
  no breakpoints, no writes, no save/config mutation; ≤5 minutes wall.
- **Controls:** positive — EXP-006 already proved this injection route
  lands scan-code bytes (Up → index 80), so the route is a proven positive;
  `022CA5E0` advancing is the poll-alive control. Negative — sample all
  four bytes with **no** keypress first (baseline). Preconditions —
  `[01F7FFE0]+0x39 == 1` and `02064AD3 ∈ {2,3,5}` must be verified **before**
  any verdict is read; a failed precondition voids the run, not the question.
- **Restoration:** nothing mutated; normal exit leaves the title state
  untouched. No restoration action exists because nothing writes.
- **Stop conditions:** title not reached, enable byte ≠1, injection failure,
  or any health/takeover event — do not infer a verdict from a failed setup.

Runners-up after it: `AQ-ARENA` (one read on any loaded save, fan-out 128 —
BLOCKED under ASTRA's own claim, gated on the failure-aware audit as noted above), then
`AQ-2`/`AQ-3` load observers (P2, need a save).

### CLASSIFIED 2026-09-21 (SWE2-FRONTIER) — ASTRA-RETURN-FRONTIER-NEW-REQUESTS-20260921

ASTRA's classification return consumed and the board state is:

- **B transfers — already assigned, no FRONTIER action:**
  `ASTRA-TRANSFER-ORACLE-S31-LICENCE` and `ASTRA-TRANSFER-ORACLE-S33-LOOT-POOL`
  are ready-targeted to SWE2-ORACLE with real predicate/state/callback
  questions (not count endpoints). ORACLE is parked-free and will pick them
  up when a slot opens; they are ORACLE's work now, not queue-parked.
- **EXP-070:** the expression-contract author accepts the matching contract;
  the bounded link edit is reviewed and queued for publication by OPUS.
- **Still C — unprepared, do not select:** the BG11 render caller needs a
  concrete scene/trigger and controls; the leader-null proposal needs
  corrected no-hit acceptance plus prepared party/state/trigger (a finite
  no-hit session cannot decide a universal invariant — ASTRA's own bound).
- **Priority blockers unchanged:** `ASTRA-REVIEW-EXP124-RAW` and
  `ASTRA-REVIEW-EXP127-FAILED-SESSION` remain the gate ahead of any new
  live selection — consume the existing returns before commissioning C work.
- **No new C selected.** Nothing here changes the standing state: ASTRA
  remains ready awaiting review, with B work already home in ORACLE's queue.

### PREPARED 2026-09-21 (SWE2-FRONTIER) — camera-shake discriminator, combined package

Consumes `ASTRA-RETURN-FRONTIER-SHAKE-STATE-AND-DISCRIMINATOR` and
`ASTRA-RETURN-FRONTIER-SHAKE-PRESENTATION-SETTING` together. Builds on the
Method-A package (`_experiments/evidence/camera-rng-discriminator/`) — its
byte-exact population, eligibility chain and limits stand; this supplies the
missing live preparation it enumerates.

- **Consumers:** `FABLE-REQ-ASTRA-MT-CURSOR-ACROSS-A-CAMERA-SHAKE` (primary) and
  `OPUS-REQ-ASTRA-SHAKE-DRIVER-OCCUPANCY-PER-FRAME`. Verdict vocabulary: **H1**
  continued eligible evaluation of a finished driver; **H2** disabled /
  unscheduled / other-consumer; **H3** sentinel-entry return. Occupancy is
  reported as occupancy — never as draw counts.

- **Save / route:** the retained **Stepping autosave** (Dalmasca Estersand),
  established by EXP-026 as the known-loadable save with a proven capture
  harness (`capture_actor.py`, frame-bracketed samples) and backup protocol.
  Route: normal play in-region toward a scripted shake event.

- **Trigger — named candidates with exact identity, plus the honest residual.**
  The 842-call census is a candidate list; what narrows it is that the save sits
  in the Estersand and the `dgl_*` corpus family is the Dalmasca plan-map group.
  Candidate call sites, all `camerashakestart_1a3(channel, id)` → builder
  `003DD230` on the *current* slot (`02099D70` via `002640C0`):
  - `dgl_f0100.txt:464` — `シェイク::シェイクc7`, a timed helper:
    `clear → wait → start(0, 0x0D000000) → wait(84) → clear`. A bounded
    start/clear interval — the best structural fit for the finished-state
    window.
  - `dgl_g0102.txt:863..877` — `cut_22..cut_25`: staged
    `start(0, 0x0D000000)` → `stop`+`start(0, 0x0D000001)` → `stop`+`start(0,
    0x0D000002)` — exercises stop/start transitions on one channel.
  - `dgl_h0100.txt:408..458` — `エレベータ０１..０３` / `シーン`: indices
    `0x0D000000..0x0D000002` with explicit `camerashakestop_19e` — sustained
    intervals between start and stop.
  - **Residual, stated exactly:** the corpus has no zone→script binding, so
    offline evidence cannot prove which `dgl_*` event is flag-reachable from
    the Stepping save. Resolution rule for ASTRA: sample the slot driver
    records during the candidate event; the script that fires is identified by
    a nonzero channel-state word appearing at `slot+0x178+0x18*ch` — do not
    guess the script, observe it. If no `dgl_*` event is reachable within
    budget, any authored shake anywhere reachable is admissible — the read
    plan is trigger-agnostic — and the package reports which site fired.

- **Owner/bank binding and record identity (all five slots, per Method A):**
  slot `i` at `02098E10 + i*0x288`. Per slot: `+0x10` bit0 live flag,
  `+0xF0` bank qword (null ⇒ ineligible), channel state words at
  `slot+0x178+0x18*ch` (nonzero admits), **entry ID** dword at
  `slot+0x170+0x18*ch` (signed; `-1` = sentinel branch `0037D21F`), bank index
  u16 at channel `+0xA` — entry ID ≠ bank index, and `003DCF60` clear leaves
  entry IDs stale. Sample all five slots every snapshot; do not collapse to
  the one slot the script is expected to use.

- **Screen Shake setting (per `ASTRA-RETURN-FRONTIER-SHAKE-PRESENTATION-SETTING`):**
  record the Config → Screen Shake setting as a **run precondition** before
  any visible-shake interpretation — the existing screenshot shows OFF.
  This is session-specific presentation state; it does **not** gate native
  evaluation. Native status transitions are reported from the state words
  alone; "the shake visibly stopped" is a separate claim needing the setting
  recorded ON, otherwise a visible negative is non-discriminating.

- **Scheduling discriminator (frame vs publish):** bracket every snapshot with
  `022C252C` / `022C2530` (tick counters `++` at `00314231` / `0031423E`) and
  `0208D45C` (raw tick). Invocation frequency is measured as
  eligible-driver-visits per tick delta — never assumed one-per-displayed-frame.
  Reads are non-atomic; equal brackets bound, they do not prove a frame.

- **Budget:** ≤32 snapshots per phase × four phases — baseline (pre-trigger),
  active (state nonzero), native-finished (state semantics per the entry's
  native completion, before stop/clear), cleared/stopped — 128 total; ≤30 s
  from the identified trigger. No heap scans, no extension for a missing
  trigger; a timeout is inconclusive, not absence.

- **Controls:** phase-matched positive — at least one snapshot with a nonzero
  bank pointer + nonzero channel-state + valid entry ID during `active`, or the
  run voids (a run with only zero states cannot qualify detection). Negative —
  the baseline phase with no shake. Read-path controls: known slot getter and
  the invalid-address probe before trusting pointers.

- **Acceptance / invalidation:** preserve a useful occupancy result even if
  scheduling attribution or visible-finish proof is absent — leave those claims
  open. Abort semantic closure on failed controls, lost slot/entry identity,
  fatal error, takeover, missing trigger, unbounded sampling or incomplete
  cleanup. No automatic restart after a stop/failure.

- **Health / restoration:** read-only; no breakpoints, no writes, no save or
  config mutation. Fresh save/config backup before, full census + hash verify
  after, Cloud protection per the established protocol, normal exit, end PC
  control immediately after the operation.

- **Not claimed:** live occupancy, invocation rate, ordinary sentinel
  reachability, RNG-share dominance, or that Screen Shake OFF disables native
  evaluation. This package prepares the measurement; it does not run it.

## DISPOSITION 2026-09-22 (SWE2-FRONTIER) — ten ASTRA returns consumed

### CAPTURED — the same-process older-save run; AQ-10 answered

`ASTRA-RETURN-FRONTIER-OLD-SAVE-RESULT-AND-SCOPE` consumed. The capture is
COMPLETE (PID34844, 597 s, 8 accepted samples / 170 spans, invalid
transition sample correctly rejected, all 26 hashes restored, PC control
released). **AQ-10 resolves:** `FFXII_004` is a `0x4E690`-byte 2018 save; it
loads successfully in the current build AND the battle block does **not**
keep session contents — the old save's compatibility prefix/bank0 replaced
the modern party records (40/40 matching at load-complete, byte-identical at
settled field). H1's "success" half confirmed, its "stale contents" half
refuted. Independent review already landed — `ASTRA-REVIEW-OLD-SAVE-
SAME-PROCESS` is DONE at ACCEPT (AUDIT-SEM: check.py reproduces
validation.txt, decode independently re-implemented). Consumer
integration is routed (FABLE V-12/L-13, OPUS save/battle contracts).

Retained gaps stay open and were never in scope: native writer/order,
ownership continuity, selector-reset observation, gambit UI, enemy
consequences, universal compatibility.

### PREPARED — CML1 authored-index question (`ASTRA-RETURN-FRONTIER-CML1-STATE-PREPARATION`)

The corrected discriminator stands; this pass verified it and produced the
bounded alternative directly from the corpus:

- **PRIMARY:** `byu_x0100` is a Bhujerba event script (`byu` → ビュエルバ,
  lmap row 26 `byu01_s01`). Entry1 `cut2_2` → authored **14**, first-match
  **8**; the discriminating column is `blob+0x24`; records [8,14] are
  byte-identical, so presentation cannot pick the index — only the bound
  entry's stored index does.
- **Residual, stated:** the corpus has no event→EBP binding, so which
  Bhujerba action runs `byu_x0100` is resolved by observation only. The old
  `FFXII_004` party (Dawn Shard, Writ of Transit) is post-Raithwall and can
  reach Bhujerba by the ordinary aerodrome route; whether that event
  remains triggerable on the save is a setup check, not an assumption.
- **DOCUMENTED BOUNDED ALTERNATIVE (verified):** `rbn_a0380` — a Rabanastre
  event script (the 大きな門振動 gate-vibration scene with camera/voice
  actors), reachable on `FFXII_004` (Southgate) without leaving the city.
  Its CML1 entry6 `stay_cam_mg_cut06` → authored **9**, first-match **6**;
  pair [6,9] byte-identical; discriminating column `blob+0x74`
  (`0x14+0x10*6`). Binding and budget identical to the primary spec —
  manager `+0xD8`, this file's CML1 count10 / CAM7 count11, two samples ×
  two states, ≤2 KiB focused reads, ≤15 min.
- Neither arm permits a screenshot verdict: identical records make
  presentation non-discriminating by construction.

### PREPARED — EO-3 raw-path pointer roundtrip (`ASTRA-RETURN-FRONTIER-EO3-STATE-AND-OBSERVER`)

The missing ordinary trigger **is** resolvable offline. The string-keyed
requester `0032E7C0` (through thunk `0032E7B0`) has exactly three callers:
`003306E0` (actor/menu loose-file path — MRP/as7/btm/nmb and EBP sections),
`003319D0` (field loose-file path), and **`00377DC0`, which requests the
loose `ps2data/efb/<map>.efb` on every map load** (the-map-ctrl-pack
documents the path build and both arms).

- **Save/trigger:** the retained Stepping autosave; the proven
  Stepping→Eastgate zone walk (EXP-026's harness/save family). The
  destination map's `.efb` request is a KNOWN raw-path issuance — the
  positive control is the path bytes at producer **RDI** naming
  `ps2data/efb/` + the destination map code *(register corrected
  2026-09-21 per `ASTRA-CONTRA-FRONTIER-EO3-PRODUCER-PATH-REGISTER`: at the
  pinned site `0032E84D`, RCX=`0xFF` and RDI=P — staging shows
  `0032E846 mov edx,edi` then `0032E848 mov ecx,0xFF`, neither touching
  RDI)*. A second independent control in the same session: opening the
  party menu exercises `003306E0`'s MRP/exfont path.
- **Caller attribution required** *(added 2026-09-21, same contra):* a
  visible zone transition alone does not establish the `00377DC0` primary
  caller — the run must record the actual primary **return address**
  (boundaries.json pins `00377F87`) alongside the path, so the producer
  site is attributed to the named trigger rather than assumed.
- **Sites, ASTRA's corrections verbatim:** producer pre-call `0032E84D`
  (full RDI=P, EDX=L, ECX=FF — never `0032E846`, which precedes
  `mov edx,edi`); completed-builder boundary `0032E983` correlated by
  request ID, not "next hit on thread"; issuer `0032E111` matched on the
  same live request ID (RCX=Q). The `001D6D90`/`001D6E20` consequence arm
  is NOT commissioned.
- **Budget/stop/health** per ASTRA's spec: ≤10 s or 8 producer hits,
  ≤32 KiB events, ≤128 B path each; no-trigger baseline before the zone
  line; stop on failed control, ambiguous reused slot, unavailable
  observer, timeout, takeover, or unhealthy session. `P==Q` is the only
  exact-preservation verdict; a `P≠Q` pair proves narrowing on that
  request, not the historical crash.
- **Batches** with the resource-trace entry below: same walk, same session,
  two read plans reported separately.

### RETIRED — the "only live can find a clear" premise (`ASTRA-RETURN-FRONTIER-MGRMARK-CLEAR`)

ASTRA's static counterexample stands on shipping bytes: `0032F14B`
`mov byte [rdi+r14+21A6D20], bpl` clears `022C6D20[m]` inside
`ActorResource_ResetManagerLoadState` (`0032ED80`), on every normal-return
path. The premise is retired with provenance; consumer corrections are
already routed (OPUS FRP-4, FABLE world-tick, AUDIT-SPEC review
`ASTRA-REVIEW-MGRMARK-CLEAR` READY). The residual live question — whether a
particular ordinary reload actually runs the reset — is **not** separately
commissioned: it needs a named consumer, an exact marked manager/resource
identity, and an ordinary reload trigger, none of which the retired premise
supplies. If a consumer names it, it re-enters as its own item.

### SUPERSEDED — the "two live-only claims" count (`ASTRA-RETURN-FRONTIER-CONTRACT-LIVE-REUSE`)

Both claims were answered offline. The unchanged-scratch ⇒ non-execution
inference for `00398F90` is retracted (second call executed 68 instructions
with zero endpoint delta); bazaar flags/sold counters verified inside the
live image with the old file's exact decoded values (18 flags, 44 counters
nonzero). The count-driven request is retired; consumer corrections
(`CONTRACT-transform-primitives` §13/15a, bazaar contract `564D0`→`56490`
extent, FABLE's two-primitives §5a / PROGRAM-STATE / BI-9) are routed to
their owners. The ONE live claim left in this family — a **new** purchase
saved and reloaded — is the roundtrip package below, commissioned on its
own need, not for coverage.

### AMENDED — the shake package is occupancy-only (`ASTRA-RETURN-FRONTIER-SHAKE-PREP-RESIDUE`)

`ASTRA-RETURN-FRONTIER-SHAKE-PREP-RESIDUE` consumed; the PREPARED shake
package above is corrected in two places:

- **Script identification is NOT "a nonzero channel-state word appearing"**
  — nonzero state cannot distinguish which candidate fired. Identification
  is by the slot's `+0xF0` bank binding matched to the loaded script
  resource identity (plus the running event's own identity where readable).
- **"Eligible-driver visits per tick" is removed.** Tick brackets +
  occupancy cannot count visits. The package reports OCCUPANCY ONLY:
  driver state / entry ID / bank index per slot per phase, tick brackets
  as phase bounds — never as invocation frequency.
- **Added native reads:** flag dwords `02EBF3C4` (option→copy gate) and
  `02EBF3C0` (neighbor gate) plus override pointer `02089350`, sampled
  alongside the UI setting so the copy condition
  (`02089350≠0 OR (02EBF3C4≠0 AND 02EBF3C0≠0)`) is recorded, not inferred
  from a screenshot. The 32-byte output rows at `02EBF380+32*draw` are
  recorded for the selected draw (`00358320` supplies it).
- Unchanged: five-slot sampling, four phases × ≤32 snapshots, ≤30 s,
  read-only, all health/restoration, and the trigger residual.

### PREPARED — same-field save/reload roundtrip (`ASTRA-RETURN-FRONTIER-STATE-ROUNDTRIP-PREPARATION`)

FZ-13 consumed (STRUCT `8b48bc0d` — op8→staging answered); the one distinct
persistence uncertainty retained is whether a game-authored same-field
change survives the write path and reload. Do not re-ask whether op8 points
at staging.

- **Save:** one current-format disposable copy of the retained Stepping
  autosave in a spare slot; the source is preserved byte-for-byte and the
  copy is the test file.
- **Route:** load → normal field → ordinary transit to a Rabanastre vendor
  (the Eastgate walk is transit, not the measured change) → before-purchase
  reads → buy ONE cheap consumable → after-purchase reads → save at the
  zone's save crystal → title/reload menu → reload the disposable file →
  after-reload reads. No area transition produces the measured change.
- **Watched bytes (all previously decoded offsets):** gil dword at
  save-image header `+0x08` (`GameState_SetGil` `00254EE0` writes it — a
  purchase is a game-authored change on a known offset); the purchased
  item's inventory count. **Unchanged-neighbor control:** a byte the
  purchase cannot touch — must be **named before the run** (a specific
  key-item flag or distant roster byte; "named before the run" is not
  satisfied by this sentence).
- **Vendor vs bazaar — kept distinct** *(corrected 2026-09-21 per
  `ASTRA-RETURN-FRONTIER-SAVE-RIDER-SCOPE`)*: this route is an **ordinary
  vendor buy** — it exercises gil and inventory-count persistence only. It
  **cannot** establish a bazaar sold-counter/offer-flag transition
  (`B+0x57C8` / `B+0x59C8`), which requires a bazaar transaction; those
  spans are removed from this package's claims and any bazaar-persistence
  question stays a **separate open item** that names its own transaction.
- **Not yet executable — name-before-run requirements** *(added 2026-09-21
  per the same return)*: exact item (a specific purchasable consumable and
  its price), exact disposable file slot, exact vendor and save crystal,
  and the exact unchanged-control byte must be listed in the run plan
  before execution.
- **Observation set:** live reads before/after purchase, the **decoded
  written file** (documented decoder — not original-code execution), live
  reads after reload. H1: the changed bytes persist as values through
  save→reload. H2: the write path transforms/overwrites them in a
  patterned way (re-encoded, rebased, zeroed).
- **Isolation/health:** file bytes hashed+captured before and after each
  write; Cloud sync off for the disposable slot; known-nonzero read,
  null-read rejection, module/code hashes, fatal-dialog and responsiveness
  checks; standard backup/restore and PC-control release.
- **Budget:** ≤3 snapshots × 4 stages (pre-purchase / post-purchase /
  written-file / post-reload), focused spans only (header 0x100 + the
  item record); ≤15 min after load. Stop on failed binding/control, wrong
  file, fatal dialog, or takeover.
- **Priority — reconciled with the consumer** *(2026-09-21,
  `ASTRA-RETURN-FRONTIER-SAVE-RIDER-SCOPE`)*: FABLE's
  `ASTRA-RETURN-FABLE-STATE-ROUNDTRIP-PREMISE` (DONE at `1dbd2f844`)
  retains this changed-byte run **only as a rider on an already-running
  Batch B session — never a session of its own**. PREPARED here means
  spec-ready, not commissioned: the earlier "nominated next high-impact
  empirical blocker" line is withdrawn — it overstated the consumer's
  ask. This rides along when Batch B runs for AQ-9/AQ-10/AQ-11 business;
  it does not justify a standalone window.

### CLASSIFIED — register reuse needs an in-pool occupant change (`ASTRA-RETURN-FRONTIER-REGFILE-REUSE-IDENTITY`)

AQ-11's premise is amended: "respawn on re-entry reuses records" is case 3
— the pool is released and reallocated on zone reload, so equal addresses
do not preserve allocation identity (cold construction zero-fills). The
discriminating question needs **case 2**: a different occupant in the SAME
allocation while the pool lives.

- **Named trigger class (resolution by observation):** proximity
  spawn/despawn cycling inside one zone — the Estersand `dgl_*` scripts use
  authored spawn calls; approaching a spawn point produces an occupant,
  withdrawing despawns it, and a second approach that fills the SAME record
  slot with a different logical actor is the target event. **Do NOT use a
  zone transition** — that is the released-pool case and is
  non-discriminating. Alternative class: a scripted NPC/guest
  appear-or-dismiss inside one field.
- **Observation set (ASTRA's verbatim):** manager index/live state, bound
  script/resource identity, pool root+count, ordinal→record pointer, record
  self-index/kind/handle tags, battle-unit link; a positive register write
  in the old occupant (resolve the spawnable actor's nonzero register at
  setup — do not assume) plus all eight registers at `+0x64..+0x83`;
  continuity evidence excluding release/rebuild (equal endpoint pointers
  are not continuity); the new occupant's **first read** of the selected
  register before overwrite, correlated to the interpreter's actual record
  argument.
- **Budget:** one named transition, ≤20 events, ≤64 KiB, 10 s around the
  trigger; stop on lost ownership, missed pair, failed detection, fatal
  dialog, or takeover. Partial endpoint-only results stay partial.
- **Honest limit:** offline evidence cannot prove WHICH spawn cycle
  produces different-occupant-same-record; if continuity is not observed
  the run reports endpoints only, with reuse unresolved.

### PREPARED — audio voice-parameter boundary (`ASTRA-RETURN-FRONTIER-AUDIO-EXACT-TRIGGER-CONTROLS`)

The static result stands (`voiceplay` defaults pan `0x40` / volume `0x7F`;
the voice-pack page reversal is FABLE's correction). Of the two outstanding
C questions, one is preparable to spec:

- **Voice-parameter question — PREPARED.** Trigger: `voiceplay_28b` calls
  inside `rbn_a0380` (the Rabanastre gate-vibration event; 13 calls across
  speaker ids 11/12, indices 0–8). Reachable on `FFXII_004` without leaving
  Rabanastre; whether the event re-triggers on that save is a setup check
  resolved by observation — if consumed, another reachable script's
  `voiceplay_28b` call is admissible since the read plan is
  call-site-agnostic. Observation: the pending cue's `+0x0F` pan byte and
  `+0x08` bits24–30 volume field at the write boundary, cue/bank/speaker
  identity, pump `003E981F`+ reads as delivery evidence, and the resulting
  voice slot's `+0x20`/`+0x1C` via adapters `002256F0`/`002257E0` (recorded,
  not claimed). Controls: a second `voiceplay_28b` index in the same event
  is the matched positive; settings/mute predicate state recorded;
  audible/screenshot is presentation-only — the native bytes are the
  claim. Budget: ≤8 cue events, ≤4 KiB each, ≤10 s around the event.
- **Selective-gate question — NOT prepared:** it needs a gated wrapper AND
  a bypass path on the same request family with a second gate and
  world-live state, and no offline evidence names such a pair for an
  ordinary trigger. Kept as an explicit dependency for OPUS to name or
  retire with provenance. EXP-127's invalid setup is not reused.

### PREPARED — one named resource family (`ASTRA-RETURN-FRONTIER-RESOURCE-TRACE-PREPARATION`)

Named family: **the map effect bank** — the loose `ps2data/efb/<map>.efb`
request issued by `00377DC0` on map load. Consumers: FABLE's queue
semantics (`FABLE-REQ-ASTRA-KIND-INDEX-TRACE`), OPUS's queue contract.

- **Save/trigger:** the retained Stepping save; the Stepping→Eastgate zone
  walk issues the destination map's `.efb` request — one named family, one
  known positive request.
- **Distinctions the observation must keep** (the boundary package's
  enumeration): size-query `0032E400` (full RDX, not EDX) → indexed entry
  `0032E620` (selector globals before the signed gate — an attempt, not an
  acceptance) → path entry `0032E7C0` → completed record `0032E983` (`+21`
  kind / `+24` index / `+28` bytes / `+2C` offset / `+64` request ID) →
  pump issue `0032E0CA..` (a zero-`+28` branch skips the issuer entirely)
  → delivered/used. The `.efb` request exercises the **path** route — the
  recorded question is "this trigger constructs AND issues THIS request",
  not a family census.
- **Correlation:** pre-trigger baseline, the zone-line crossing,
  post-load settled; matched by request ID + slot, never "next hit".
  Negative control: the baseline phase; positive control: the `.efb` path
  bytes at RCX naming the destination map. A no-hit is a bounded negative
  for THIS trigger only.
- **Budget:** ≤10 s instrumentation, ≤8 producer hits, ≤32 KiB events,
  ≤128 B path; standard health/stop/detach/restore. Batches with the EO-3
  entry above — one walk, two read plans, separately reported.

### STANDING INSTRUMENT CAVEAT (SWE2-FRONTIER) — one-slot breakpoint path loses FIP upper 32 bits
(`ASTRA-NOTICE-FRONTIER-NATIVE-FP-BOUNDARY`, consumed 2026-09-22 by SWE2-FRONTIER;
**scope narrowed 2026-09-21** per `ASTRA-RETURN-FRONTIER-FP-CAVEAT-SCOPE`)

ASTRA's `native-fp-context-control` evidence shows the sampled one-slot
breakpoint path loses the **upper 32 bits of the x87 last-INSTRUCTION pointer
(FIP)** across FXSAVE64 resume — four healthy owned-target arms, 21 hits / 21
changes each, with CONTROL|DEBUG-only resume writes and no FP/INTEGER read
requests. **Exact observed scope:** the loss was recorded on above-4GiB native
x87 instruction addresses; **FDP was zero throughout, so nonzero-FDP
preservation or loss is untested** — claims must name FIP specifically, not
"x87 last-instruction metadata" generally. Seeded XMM/x87 values and controls
survive; the deliberate PXOR detector correctly fails. Mechanism unresolved;
not the executing RIP; not linked to the EXP127 fatal dialog.

**Forward boundary for every breakpoint-using package in this queue**
(AQ-1+AQ-6's single read, the combat handlers run, BQ-27's sampled sites,
EO3's producer/builder/issuer hits, the resource-trace boundaries):

- No package may claim **full-context transparency**, and none may consume
  observed-lost state — **FIP upper 32 bits**, and FDP (untested, therefore
  unclaimed) — as evidence. That is the tested limit; it is **not** a blanket
  "integer/pointer/memory only" rule. Controlled FP register observations may
  still be reported as instrumented observations with appropriate validation
  (state + effect controls); raw bytes are not automatically immune to
  downstream FP or scheduling effects either — each claim needs the controls
  its own question requires.
- Narrowed resume flags are **not a demonstrated fix**, but that is a scope
  statement, not an authorization gate: it does not create a new user-consent
  requirement and does not mandate that the helper stay as-shipped. A package
  may choose a different justified observer per claim; whatever it chooses,
  the choice and its validation are part of the evidence. The host mechanism
  staying unidentified stays an open item, not a freeze order.
- Breakpoint packages must additionally state whether the resumed thread's
  own subsequent FP behaviour is in the observation path. For all currently
  prepared packages it is not, so nothing already queued needs
  re-specification — but the reason is "the discriminating observations are
  stated and controlled", not a datatype blanket.
- Dependent-conclusion audit: no accepted package in the queue rests on
  FIP/FDP state. EXP127 stays INVALID_POST_TRACE with unknown
  crash cause; unrelated read-only captures (frame sampling, save
  snapshots, memory reads without breakpoints) are unaffected and are not
  recaptured.

### QUEUED — movement-body pool occupancy per area (`FABLE-REQ-ASTRA-S19-BODY-POOL-OCCUPANCY`, FABLE, Claude Opus 5.5, 2026-09-25)

**Why live.** The shipped separation walk `003DAB50` indexes remembered pairs by visited position, not by body. This
was executed on shipped bytes, see [the index probe](../candidates/s19-fable-visit-index-probe/README.md). So the
mis-index applies to any body at index 8 or above, and the second-qword mis-pairing to any body at index 64 or above.
Indices are handed out in ascending order per area; the allocation order is read statically. What no static route
gives is **how many bodies an area actually allocates in play**.

**Read-only package, no breakpoints** (outside the FIP caveat above). In each of three areas, a town, an open field
with foes, and a dungeon, read the used-list head `u16 [02B57CC0]`. Walk the used list through each entry's `+2`
link, with entry `i` at `02B4E4C0 + i * 0x130` and `0xFFFF` ending the list. Record the count, the highest index,
and the active byte `+0x07` of each entry.

**Controls.** On the title screen the used list is empty (head `0xFFFF`). The count must not exceed 128. Every
walked entry's `+4` must equal its own index, since the initialiser writes it.

**Answer shape.** Per area: count, highest index, active count. Any area with a body at index 8 or above makes the
remembered-pair drift live in normal play; any with one at 64 or above makes the wrong-body resolution live.

## DISPOSITION 2026-09-26 (SWE2-FRONTIER) — four ASTRA returns consumed; coordination recorded

ASTRA is parked for the usage handoff; input stop-loss remains exhausted and no item below
authorizes a fresh live window. Each return's preparation package already exists under
`_experiments/evidence/`; what follows is the source-bound owner/reviewer decision and the exact
remaining prerequisites each package names. None of these rows is closed by this disposition —
they are held with named prerequisites.

### QUEUED — `ASTRA-RETURN-FRONTIER-S19-SETUP-STOPLOSS`

**Decision:** no additional setup authorization. Two input recoveries are already exhausted;
extra setup passes need the goal's bounded authorization, which is not granted while the stop-loss
holds. Stepping occupancy stays pending exactly as the owned invalid-setup checkpoint recorded —
the failed setup reached no actual binding or input registration, `setup26` files unchanged,
title raw provisional, game exited and PC reset. The queue reflects this item as *invalid setup,
prerequisites outstanding* — not a dead path.

**Remaining prerequisites:** a bounded setup authorization naming the failed-input mechanism,
an actual-binding/input-registration preparation that does not reuse the exhausted recovery route,
and ordinary consumer acceptance before any S19 spend.

### PREPARED — `ASTRA-RETURN-FRONTIER-STATUS-WATCH-PREPARATION`

Package: `_experiments/evidence/status-watch-preflight/` (extract one US shipping battle_pack
entry; validate directory+0x40, st2e header/count/stride/bounds, embedded self IDs; 8 rejecting
controls, no live result claimed).

**Owner:** OPUS (types/contracts) — the authored sparse-byte coverage answer feeds its schemas.
**Reviewer:** FABLE (Status_Periodic_Terminal consumer) plus AUDIT lane acceptance of the
preflight's check.py.
**Remaining C prerequisites, verbatim from the package:** fresh live state identity; a real
registered→accepted→executed status trigger; a *qualified read detector* (hwbp.py programs
execute breakpoints only — it cannot serve as the read-watch control); normal health/detach.
A zero hit is never universal dead/unread proof. No automatic C escalation.

### PREPARED — `ASTRA-RETURN-FRONTIER-SR5-OBSERVATION-PREPARATION`

Package: `_experiments/evidence/sr5-exhaustion-preflight/` — static CFG already answers the
coverage question: proposed `0021B608` lies only on the *nonempty* exhausted walk; the
empty-list route bypasses it (`21B5F4→621`), matched arm goes `FE→60A/callback 61A→621`.
Local receipt-preservation holds; 4 rejecting controls; no live occurrence claimed.

**Owner:** FABLE (audio contract consumer).
**Reviewer:** AUDIT lane for the CFG qualification; FRONTIER holds the state-preparation role.
**Remaining C prerequisites:** named save/trigger, actual controller/list/key identity, qualified
matched/empty/nonempty miss controls (the proposed608 observer only covers the nonempty arm), an
event-proportional bounded observer, health/cleanup. One finite no-hit cannot prove never-occurs.

### PREPARED — `ASTRA-RETURN-FRONTIER-S33-PREPARED-C-STATE`

Package: `_experiments/evidence/s33-live-preparation/` — Q1 (method-A) is answered statically:
the 13-slot flag address agrees with shipping op1/lookup/update and retained R5-R7 fixture
identities (13-slot formula, `+270+k*2A0`/`+272` confirmed, first `4E2`/last `2462`).
Question `OPUS-REQ-ASTRA-S33-VISUAL-SLOT-EXHAUSTION-LIVE` stays open — R5-R7 are
NATIVE-REPLAY with `live_game:false`, an isolated controlled world, not allocator placement.

**Owner:** OPUS (world-pickup contract/ownership) with FABLE on reward/action consequences.
**Reviewer:** AUDIT lane before any C spend.
**Remaining C prerequisites:** named disposable save/area, exact normal drop/retirement trigger,
actual initialized manager/subobject identities and sub-4GiB handles (validated pointers), an
observer positive, ≥4 ordinary new drops while 10 remain uncollected, retired-slot lifetime in
actual update events/game frames, bounded sample/event/time budgets, consumer acceptance,
session health. Ordinary target→queued command→executed action must be proven before
damage/death/drop consequences. No injected occupied bits or CREATE calls.

### COORDINATED — `ASTRA-COORD-FRONTIER-REWARD-SEAL-AND-UC1`

Consumed in triage. The retained EXP081 reward extraction is already owner-consumed at
`21f25545b`; the source seal/review tail is ASTRA's own finish, not a live dependency — no new
session is queued for it. The UC-1 band ruling is recorded in `OPEN-QUESTIONS.md` (commit
`7dcbf2782`) with the routed evidence intact: ASTRA takes the ruling against its original
instruction/control evidence when its seat rotates back; OPUS's held `007EE7C0` extent collision
and the AUDIT-SPEC extent-falsification review remain the named follow-ons. OPUS/FABLE/ORACLE
production is unaffected — no broad ASTRA maintenance queue was created.

### RULING — `ASTRA-RETURN-FRONTIER-PROVEN-INPUT-ROUTE-RECOVERED` (one bounded qualification pass granted)

ASTRA reports the input route recovered: sender `7a6353` and the pulse/interpreter AST are
byte-identical to the versions that produced the accepted 2026-09-13 receipts. Only the
`ffxii_runtime` support changed since, which is why a fresh qualification is needed at all.
The failed-setup stop-loss was a guard against *unproven* routes; this route is now proven
against accepted receipts, so the earlier "no extra authorization" posture narrows to this
one scoped decision.

**Granted:** exactly **one** bounded qualification attempt — the named method, ~6 minutes,
two Enter pulses — to qualify the changed `ffxii_runtime` support for input registration.

**Conditions, all mandatory:**

1. Fresh native controls and healthy-acceptance checks run *before* the pulse spend; a
   failed control aborts the attempt with no retry.
2. The attempt consumes the frozen original budget — it does not reset it. The unknown
   cause of the invalid capture and the old invalid evidence are preserved unchanged.
3. No new keyboard discovery, no general observer platform, no widened gate. The question
   stays exactly the scoped one.
4. Result lands as a normal experiment record (method/live_game declared, controls listed)
   routed to its consumers for independent review before any S19/S33 setup spend follows.

If the single pass fails or its controls cannot be made healthy, the stop-loss posture
resumes unchanged and further setup waits on new evidence, not elapsed time.
