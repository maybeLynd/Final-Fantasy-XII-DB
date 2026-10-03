---
system: What the engine fixes at boot
category: 00-Engine-Core-Runtime
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) — no registered residue left (status line current 2026-09-30, SWE2-CONTRACT); answered: the one arena-10 selection is unreachable with shipped data (RC-11), the extra tail bytes are slack outside every arena structure (RC-2), the two unregistered allocations (RC-3: the oscillator table, and a block nothing reads), the button masks are rewritten only by the DecideButton applier 0022A4F0 (2026-09-18), no code registers arena id 10 (one effect path selects it, RC-11), the field frame reads 02064ACC as its pacer wait, the allocator is the CRT malloc shim, the MT tempering is present (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: PrimaryOwner:CoreRuntimeScheduling
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites `002F0280`; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: false
  reopened_count: 0
---

# What the engine fixes at boot

`0022A0B0`, 978 bytes. Six documents cited it; none had opened it.

**Three things a modder needs are decided here and never revisited: the memory budget, the
confirm/cancel button mapping, and the random seed.**

## The random number generator is seeded with a constant

```c
002648..  func_0x00379CF0(0x11B9);      // through a 5-byte thunk -> 00863D30   <- corrected 2026-10-02, OPUS - the call is at 0022A0B0+0x360 (mov ecx, 0x11B9 at +0x35B), not 002648..; the thunk's only callers are 0022A0B0+0x360 and 00584210+0x1C3
```

```c
void FUN_00863D30(uint32 seed) {
    obj = &PTR_FUN_01ccfac8;
    if (DAT_02EB4234 == 0) FUN_00866D60(obj, 0x1571);   // 5489
    DAT_02EB4234 = 1;
    FUN_00866D60(obj, seed);                            // 4537
}
```

> **`0x1571` is `5489` — the default seed of `std::mt19937`.** A generator whose first-use path seeds
> itself with 5489 is a Mersenne Twister carrying its library default, and this database had already
> bound MT19937 to two flag-setting consumers from the other direction.

**The boot then re-seeds it with `0x11B9` — 4537 — a constant in the instruction stream.** No clock
read, no entropy source, no player input feeds it.

**So the Mersenne Twister's stream is identical on every launch — until a save is loaded.**

> **CORRECTED 2026-09-03, and the correction is the interesting half.** This section first read *"the
> stream is identical on every launch; two players who take the same actions from boot get the same
> rolls."* **That is true from boot and false across a reload.** `RNG_MT19937_Seed` has **two**
> callers: this one, with the constant, and
> **`SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`**, which tail-jumps to the same thunk with a
> seed computed from **`api-ms-win-crt-time-l1-1-0.dll!_time64`** — both halves of the 64-bit clock
> value mixed with a global. The import was resolved through the PE import descriptors, not inferred
> from the call's shape.

**"Deterministic from boot" and "deterministic across a reload" are different claims, and only the
first holds.** Reloading a save rerolls this generator from the wall clock.

**Within a single launch, before any load**, what makes a playthrough differ is **how many draws have
been taken by the time a roll happens**, not the numbers themselves.

**This is not a claim about every random outcome in the game, and the other generator behaves the
opposite way.** Loot, the enemy chain and weighted action selection share **one LCG** with eight draw
sites, all moving the same state — **perfectly correlated with each other, and provably uncorrelated
with anything on the MT**, whose 66 consumers (53 of them in the formula layer) hold disjoint state.
*(Anchors, 2026-09-30, SWE2-CONTRACT: the eight LCG draw sites are §3 of
[which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md), 24 instruction sites,
three per draw; the 66 MT consumers are that page's caller census of `00379CD0`, tier 1.)*

> **Reloading a save rerolls combat outcomes and does not reroll the loot stream.** The LCG's seed is
> a **counter**, post-incremented once per battle-area init, with exactly two instructions in the
> whole image touching it — so **the loot stream's starting point is a function of how many areas you
> have entered since launch, and nothing else.** *(Anchor, 2026-09-30, SWE2-CONTRACT: the counter is `0208E6B0`,
> read at `00234301` and written at `00234315`, both in `BattleSystem_InitializeAreaState`, by an image-wide
> rip-relative sweep — [which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md),
> tier 1.)*

**A note on how the call was nearly missed:** `00379CF0` is a **5-byte thunk** (`jmp 00863D30`) and is
**not in the function list** *(answered: see the key-address table below, listed in the function list since; 2026-10-02, OPUS)*. A caller census of the seeding function that did not follow thunks would
report this site as absent — **the second time tonight the function list's shape decided what could be
absent from an answer.**

## The confirm/cancel swap, applied

```c
DAT_01E0C2A4 = 0x2000;
DAT_01E0C2A0 = 0x4000;
if (DecideButton == 0) { DAT_01E0C2A0 = 0x2000; DAT_01E0C2A4 = 0x4000; }
```

**Two button masks, written twice, exchanged when the setting is zero.** The setting is
`DecideButton` in `GameSetting.ini`, index 25, default `0 = Circle` — documented elsewhere in this
database, and **this is where the choice becomes two globals the rest of the engine reads.** The
engine never asks the setting again; it asks these two globals.

## The frame base decides a second constant

`0022BDF0` — the frame-base selector — runs first, and then:

```c
uRam_02064ACC = 2 / DAT_01DFE0B4;      // frame base: 1 at 30 fps, 2 at 60
```

**So this global is `2` at 30 fps and `1` at 60** — an integer division by the frame base, ~~evaluated
once~~ computed first here *(CORRECTED 2026-09-29, OPUS, `CON-158`: re-evaluated by the area transition `002628B0` → `002695A0`, and settable by the script verb `mainloopallsyncv` through `0026DB10` → `00229F10`)*. It is the same `01DFE0B4` that the frame-limit setting writes — and that setting is now
named: **`FrameLimit` in `GameSetting.ini`**, read through the 11-byte getter `0017D8F0`. `0022BDF0`
is not itself the writer; it computes `(FrameLimit == 1)` and tail-calls `001EDDC0`, which writes the
triple **only on the 60 branch**.

## The memory budget

**Eleven pools are allocated and nine are registered**, all before any content loads.

| id | registered base | size |
|---:|---|---:|
| 2 | `0x01DC0000` | 29.75 MiB |
| 3 | `0x00D20000` | 13.12 MiB |
| 4 | `0x00100000` | 1.00 MiB |
| 5 | `0x001C0000` | 1.75 MiB |
| **6** | **`0x06C00000`** | **108.00 MiB** |
| 7 | `0x03000000` | 48.00 MiB |
| 8 | `0x02000000` | 32.00 MiB |
| 9 | `0x01200000` | 18.00 MiB |
| 11 | `0x00400000` | 4.00 MiB |

**Registered total: 255.6 MiB. Allocated total: 257.1 MiB.**

> **Note for the address checker.** These are **runtime pool bases, not image addresses** — several
> (`0x06C00000`) lie outside the image entirely. `verify_doc_addresses.py` flags `0x03000000` as
> `unwind-BANNED` because it happens to fall inside `.pdata`'s virtual range
> (`0x02F98000`–`0x03000C00`). **It is a false positive**: nothing here cites unwind data as
> evidence. Recorded so the next audit does not re-open it. *(2026-09-08)*

**Three facts the table alone does not show:**

- **Every allocation is its registered size plus a tail** — `+0x10`, `+0x100` or `+0x400` — and the
  same value is passed separately as the registration's ~~alignment~~ fourth argument. ~~**The tail is the
  alignment allowance, requested as part of the block.**~~ *Corrected 2026-09-12
  (ASTRA-CONTRA-FABLE-ARENA-SLOT-COUNT): that argument is the arena's **handle-slot count** (16-byte handle
  records); the initializer aligns everything to 64 bytes by itself and lays out only `size` bytes, so what
  the extra tail bytes serve is not established. See
  [the memory page](../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md) §2.*
  *Narrowed by execution (cited 2026-09-30, SWE2-CONTRACT):* `EXP-142` ran the nine registrations on shipped bytes;
  the registrar's stores stay near the block's head (about `0`–`0x783C`, scaling with the pool) and the last 64 bytes of
  every allocation keep the fixture's fill, so the tail is not a region of slot records at the end
  ([the boot contract](CONTRACT-boot-fixups.md) I5 and §14, tier: isolated original-code execution). Nothing observed
  writes the tail. **What it is for is RC-2** — answered 2026-09-30: slack outside every arena structure (box RC-2
  below).
- **Two allocations are never registered here** (`0x80000` = 0.5 MiB and `0x100000` = 1 MiB). They are
  stored to globals and used elsewhere; **what they are is not established by this function.**
  *Narrowed (cited 2026-09-30, SWE2-CONTRACT):* the 0.5 MiB block's pointer goes to `01FD4A20` (`0022A284`), and
  that slot is **write-only in the whole image** — its single reference is the store; the 1 MiB block's pointer goes
  to `01FD4A90` (`0022A2A3`), read twice, at `0040AF65` and `0040AFF2`, both inside `0040ACF0`
  (`_types/fields.tsv`, `BootAllocationSlot01FD4A20` / `BootAllocationSlot01FD4A90`, OPUS 2026-09-21, tier 1).
  `EXP-142` found both blocks left entirely unwritten by the boot battery. So the 0.5 MiB block is reached through no
  stored pointer this census can see, and the 1 MiB block has one reading function. **What the two blocks are for —
  the 1 MiB one through `0040ACF0`, the 0.5 MiB one through no reader yet found — is RC-3.**
  *RC-3 answered 2026-09-30 (static; SWE2-CONTRACT on OPUS's record
  [`rc3-boot-blocks-0930`](../_index/candidates/rc3-boot-blocks-0930/README.md)):* the **1 MiB block is the per-model
  oscillator subsystem's shared table** — the scope-open call `00415EE0` (arg 1) copies `01FD4A90` into `02CA43C0`, and
  `0040ACF0` uses it for modes 0 and 2 and on the not-listed path; `02CA43C0`'s references all sit in `0040ACF0` and the
  cursor family `00415EE0` / `00416270` / `00416450` / `00416600` / `004167C0` / `00416910`
  ([the per-model oscillator subsystem](../17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md),
  its members table row `00415EE0`). The **0.5 MiB block is allocated, stored and never used**: its slot `01FD4A20`
  has one reference in the image, the boot store `0022A284`, and no absolute or RVA copy exists — the same sweeps find
  all three of `01FD4A90`'s references, the positive control. Tier 1. *Not claimed:* why the 0.5 MiB block is
  allocated.
- **Id 10 is absent from the sequence 2–11.** Nine ids are registered and the gap is exactly one.
  **Whether id 10 is registered elsewhere or does not exist is not answered here** — and it is worth
  asking, because a missing id in an otherwise dense range is either a second registrar or a retired
  pool. *Answered 2026-09-30 (SWE2-CONTRACT), static: no code in the image registers id 10.* The arena initializer
  `00369D30` has five callers in the edge list (calls and tail jumps), and the id each passes is read at the call:
  boot `0022A0B0` passes 2–9 and `0xB` (the positive control, matching `EXP-142`), `0037B3D0` re-registers `0xB` (the
  arena-11 regrowth), `003E9AA0` passes `0xC`, `0025A990` `0xD` and `0025AA30` `0xE` — the nested arenas. No
  rip-relative operand and no absolute qword in the file points at `00369D30`, so no pointer route was missed by the
  edge list. Control `_index/candidates/swe2contract-ddres-b1-0930/arena_ids.py` (output `arena_ids.out`), tier 1.
  *Limit:* a call through a pointer assembled at run time would not be seen. So in this build id 10 is a gap in the
  numbering, not a pool some other registrar sets up; whether code *selects* id 10 is not searched here.
  *Searched 2026-09-30 (SWE2-CONTRACT), static — and one path does select it.* An allocation picks its arena only
  through the selection push `0036C1D0(arena, category)` (the wrappers take no arena argument;
  [the memory page](../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)).
  Reading the arena argument at all 135 push sites in 109 functions (the page's own counts, control C1; `0025A990`'s
  published `5`, control C2) resolves 120: arenas 2 (8), 3 (9), 4 (5), 5 (24), 6 (29), 8 (42), 9 (2) — and **10 once**,
  at `00504398` in `00504350`, the string-record handler of effect element type `0x59`, which selects arena 10 when the
  first byte of the current effect context `[02F97340]` is 10 or more (`00504383`–`00504398`). 15 sites pass an arena
  that arrives in a register from the caller and are listed unresolved. Control
  [`arena_select.py`](../_index/candidates/swe2contract-ddres-b1-0930/arena_select.py) (output `arena_select.out`),
  tier 1. Since no code initialises arena 10, **what that selection does, and whether the branch is reached, is RC-11**.
- [x] **RC-11.** Whether the arena-10 selection at `00504398` (in `00504350`, effect element type `0x59`, taken when
  the current effect context's first byte is 10 or more) is reachable with shipped effect data, and what an
  allocation through the wrappers does when the selected arena was never initialised; plus which arenas the 15
  register-passed push sites select. Registered 2026-09-30 (SWE2-CONTRACT); static.
  *Applied 2026-09-30 (records) RC-11:* **ANSWERED 2026-09-30 (static; ORACLE's record `_index/candidates/rc11-arena-ten-0930/`, commit `1e4537034`): the arena-10 branch is unreachable with shipped data** — the effect context type is always 1–5 or 7, so all 284 shipped `0x59` records select arena 8. An allocation from the never-initialised arena 10 would hang the thread (`0036BC60` marks descriptor byte `022D8662` and returns 0; the retry `0036BFE0` spins at `0036C000`). The 15 register-passed pushes select 2, 3, 4, 6, 8, 11 and 12; two debug-verb sites are script-fed and never called by shipped scripts.

## `WinMain` — CJ-1 answered 2026-09-12 (FABLE)

`007A3770` (45 B), the function in the slot MSVC reserves for `WinMain`, is `WinMain`: it calls
`IsDebuggerPresent` (`008C2180`, `KERNEL32`) and then **`007980A0`** — 2,153 bytes, the game's real
`main` — on both arms; the only difference the debugger check makes is whether the return value is
kept in the shadow slot (`007A3785`–`007A3792`) before returning. `007980A0` is the function the
settings contract already meets as the constructor of the settings object; it is where the boot
sequence this page describes is entered. **CJ-1.**

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `0x1571` really MT19937's default seed, or a coincidence? | It is `5489`, `std::mt19937::default_seed`. **Corroborated independently:** this database had already bound MT19937 to two RNG consumers by a different route. **Not read: the tempering constants** — the identification rests on the seed constant plus that prior binding. *Read since (cited 2026-09-30, SWE2-CONTRACT):* the textbook masks `0x9D2C5680` / `0xEFC60000` occur nowhere in the image, and the tempering is present anyway with the mask applied before the shift, exactly equivalent, in `RNG_MT19937_NextU32` `00863BF0` ([rng streams](../21-RNG-And-Determinism/rng-streams.md), "The tempering constants are absent from the image, and the tempering is present anyway"; [the generator contract](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md)), tier 1. |
| Is `0x11B9` a seed or an id passed to something else? | It reaches `FUN_00866D60(obj, value)` — **the same call and the same object as the 5489 path**, three instructions apart. |
| Could the button masks be set again later? | ~~**Not established here.**~~ **Answered 2026-09-18 (FABLE), by a whole-image sweep:** of the 90 sites that reference `01E0C2A0` or `01E0C2A4`, exactly four store to them: this function (`0022A10C`, `0022A119`) and `0022A4F0` (`0022A51F`, `0022A526`), the mask applier the Config-screen page names as the tail of the `DecideButton` setter (`0017E6E0`, AV-7); every other flagged site is a `test word ptr` read (the input arbiter `00253C70`, the menus, the widget handlers). So the masks are rewritten exactly once more per change of the setting from the Config screen, and by nothing else. |
| Are the pool "sizes" sizes, or addresses that look like sizes? | They are the **first argument to an allocator** whose result is stored and then handed to the registrar with a matching base — round MiB values with a tail equal to the arena's handle-slot count *(2026-09-12; formerly read as an alignment tail)*. **Consistent with sizes; the allocator itself was not read.** *Read since (cited 2026-09-30, SWE2-CONTRACT):* `0036D240(size)` is a 14-byte shim that tail-jumps to the CRT `malloc` thunk `0085E730` → import `008C2B40`, so the first argument is a `malloc` size ([the memory page](../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md), "Where the backing comes from"), tier 1. |
| Does `2 / DAT_01DFE0B4` divide by zero if the base is unset? | **No — but the original reason was wrong; corrected 2026-09-08.** `0022BDF0` writes that global only through its tail call to `001EDDC0`, and **only when `FrameLimit=60`**. At `FrameLimit=30` *nothing* writes it, so ordering guards nothing — the division is safe because `.data` ships the value as **`1`**. See [`../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) section 12. |

**What this document does not claim:** what the pools hold, what the two unregistered allocations are
for, what any of the ~60 further boot calls do, or which random outcomes draw from the seeded
generator rather than from the LCG. *(2026-09-30, SWE2-CONTRACT: the two allocations are RC-3; which roll draws from
which generator is answered on [which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md);
the boot calls are the exclusive-subtree census below; what each pool holds is not claimed here.)*

## Key addresses (SWE2-CONTRACT, 2026-09-30)

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0022A0B0` | the boot fixer | 978 B | seeds the generator, applies the button masks, computes the frame-base constant, allocates eleven pools and registers nine |
| `0017D4C0` | its only caller | 387 B | the render-setup step the readiness writer `0017D000` runs (PA-3 on [the Phyre application page](../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md)) |
| `0022BDF0` | frame-base selector | 146 B | computes `FrameLimit == 1` and tail-calls `001EDDC0` |
| `001EDDC0` | frame-rate bootstrap | 165 B | writes the 60 fps triple only on that branch |
| `00379CF0` | `RNG_MT19937_Seed` thunk | 5 B | `jmp 00863D30`; listed in the function list since this page was written |
| `00863D30` | `RNG_MT19937_Seed` | 69 B | seeds 5489 on first use, then the caller's seed |
| `0036D240` | the allocation shim | 14 B | tail-jumps to the CRT `malloc` thunk |
| `00369D30` | the arena initializer | 707 B | `(id, block, size, slotCount)` |
| `0022A4F0` | the button-mask applier | 66 B | the only other writer of the two masks |
| `0022A770` | the field frame | 2,001 B | the one reader of `02064ACC` (`0022AE8F`) |
| `0035EB70` | the tick pacer | 258 B | waits `max(n, 1)` ticks |
| `00229F10` | frame-base setter | 7 B | `mov [02064ACC], ecx; ret` |

### Data addresses cited by this document (SWE2-CONTRACT, 2026-09-30)

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01E0C2A0` / `01E0C2A4` | confirm / cancel masks | `.data` dword | `0x2000` / `0x4000`, swapped when `DecideButton` is 0 |
| `02064ACC` | frame-base constant | `.data` dword | `2 / FrameLimit`: 2 at 30 fps, 1 at 60 |
| `01DFE0B4` | frame limit / time-base mode | `.data` dword | ships `1`, written `2` on the 60 branch |
| `02EB4234` | generator first-use latch | `.data` byte | set on first seed |
| `01FD4A20` / `01FD4A90` | the two unregistered allocations' slots | `.data` qword | 0.5 MiB (write-only) / 1 MiB (read by `0040ACF0`) |

## Call chain (SWE2-CONTRACT, 2026-09-30)

```
PhyreEngine run loop -> GameApplication startup
  -> 0017D000 (sets the readiness latch +0x113C last)
     -> 0017D4C0
        -> 0022A0B0                                   <- THIS SYSTEM (the owner transition)
             -> 00379CF0 -> 00863D30 (seed 4537)
             -> button masks 01E0C2A0 / 01E0C2A4
             -> 0022BDF0 -> 001EDDC0 (60 fps triple);  02064ACC = 2 / [01DFE0B4]
             -> 0036D240 x11 (malloc) -> 00369D30 x9 (arenas 2-9, 11)
later, every field frame:
  0022A770 -> 0035EC80 -> 0035EB70 (waits [02064ACC] ticks)
```

**Upstream (who causes this):** application startup, once, before any content loads (the boot contract §2).

**Downstream (what this causes):** the generator's stream until the first load reseeds it from the clock; the two
masks every menu and the input arbiter test; the frame pacing interval; the nine arenas every allocation draws from.

**Do not confuse with:** the load-time reseed `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (clock, not
constant), the Config-screen setter path that re-applies the masks (`0017E6E0` → `0022A4F0`), and the area transition
that recomputes `02064ACC` (`CON-158`).

## Modding notes (SWE2-CONTRACT, 2026-09-30)

- **Best intervention point:** `GameSetting.ini`'s `DecideButton` and `FrameLimit` settings, which this function turns
  into globals; the masks are re-applied from the Config screen through `0022A4F0`, so editing the globals directly is
  overwritten on the next change of the setting.
- **Regenerates itself:** `02064ACC` is recomputed on every area change and can be set by the script verb
  `mainloopallsyncv`, so a write to it lasts until the next transition.
- **Breaks if:** a pool is resized without its handle-slot count (the fourth argument): the count bounds how many
  handle-held blocks an arena can issue at once ([the memory page](../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)).
- **Multiplayer / XIIOnline:** the MT stream is identical from boot on every client and diverges at the first load
  (clock reseed); the LCG follows the area-entry count. Neither is a shared source of truth across machines.
- **Mod compatibility:** the seed and the pool sizes are instruction immediates; no authored data changes them.

## What is not known (SWE2-CONTRACT, 2026-09-30)

- [x] **RC-2.** What the extra handle-slot-count bytes on each boot allocation (`+0x10` / `+0x100` / `+0x400`) are
  for. `EXP-142` shows the registrar's stores stay at the block's head and the tail keeps the fixture fill; nothing
  observed writes it.
  **ANSWERED 2026-09-30 (static; SWE2-CONTRACT on OPUS's record
  [`rc2-arena-slack-0930`](../_index/candidates/rc2-arena-slack-0930/README.md), commit `5511c49e9`): slack outside every
  structure the arena defines.** For all nine arenas (ids 2–9 and 11) the allocation is the registered size plus the
  arena's handle-slot count — one byte per slot. `00369D30` builds the header, both page bitmaps and the
  slots × 16-byte handle-slot table from the block's start and bounds the heap by the registered size alone; no arena
  field addresses past base + size. This agrees with `EXP-142`'s untouched tail. Tier 1. *Not claimed:* why the sizing
  adds those bytes.
- [x] **RC-3.** What the two unregistered boot allocations are for: the 0.5 MiB block whose slot `01FD4A20` is
  write-only, and the 1 MiB block read only through `01FD4A90` by `0040ACF0` (`0040AF65`, `0040AFF2`).
  **ANSWERED 2026-09-30 (static):** the 1 MiB block is the per-model oscillator subsystem's shared table; the 0.5 MiB
  block is never read (the memory budget section above; record `rc3-boot-blocks-0930`).

## Evidence — claims, evidence and tier (SWE2-CONTRACT, 2026-09-30)

| Claim | Evidence | Tier |
|---|---|---|
| The generator is seeded 5489 on first use, then 4537 at boot | `00863D30` read; the boot call through `00379CF0` | 1 |
| The stream is rerolled from the clock on load | the second caller of the seed, `_time64` import resolved (the boot contract I2) | 1 |
| The masks are swapped when `DecideButton` is 0 and rewritten only by `0022A4F0` | this page's code block; the 90-site sweep of `01E0C2A0`/`01E0C2A4` (falsification table) | 1 |
| `02064ACC = 2 / FrameLimit`; recomputed on area change; settable by script | `0022A18B`–`0022A1A7`; `CON-158` | 1 |
| The field frame waits `02064ACC` pacer ticks | `0022AE8F` read and the `0035EB70` call; census `rip_refs_02064ACC.out`; EXP-128 execution of the pacer | 1 (static) + isolated original-code execution |
| Eleven allocations, nine registrations, sizes and slot counts | the eleven `0036D240` sites and nine `00369D30` sites listed below; `EXP-142` | 1 + isolated original-code execution |
| No code registers arena id 10 | `arena_ids.py` over the five callers of `00369D30`, boot as the positive control | 1 |
| The 0.5 MiB slot is write-only; the 1 MiB slot is read only by `0040ACF0` | `_types/fields.tsv` (OPUS 2026-09-21) | 1 |
| The 1 MiB block is the oscillator subsystem's shared table; the 0.5 MiB block is never read | `rc3-boot-blocks-0930` (OPUS 2026-09-30); the oscillator page's members table | 1 |
| The LCG has eight draw sites; the MT has 66 consumers; the area counter has two instructions | [which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) claim table | 1 |
| `WinMain` is `007A3770` and calls `007980A0` | CJ-1, read 2026-09-12 | 1 |
| `FrameLimit`=30 leaves `01DFE0B4` at its shipped `1` | `.data` value; `001EDDC0` writes only on the 60 branch | 1 |

## Independent re-derivation of the memory budget — 2026-09-03, session `repos-78`

`0022A0B0` appeared on the *leaned on and never opened* cut — cited by seven documents, **all at its
entry only**. It was read anyway, and **the memory-budget section above is confirmed in full**: the
nine ids, the nine sizes, the tail *(the slot count, 2026-09-12)*, the two unregistered allocations and the absence of id
10 were all re-derived from the image without reference to this document, and agree exactly.

**So this was a false positive on that cut, and the interior addresses are supplied here so it stops
being one.** The cut measures *"cited by entry only"* as a proxy for *"never read"*; this function was
read thoroughly and the proxy misfired. The addresses below are the evidence the table above already
rests on — citing them makes each row checkable rather than merely stated.

**The eleven allocation sites** (`0036D240`, size in `ecx`, result to a global):

```
0022A1E1  0x1DC0010 -> 01FD49F8      0022A236  0x3000100 -> 01FD4A30
0022A1F2  0x0D20100 -> 01FD4A00      0022A247  0x2000100 -> 01FD4A38
0022A203  0x0100010 -> 01FD4A08      0022A258  0x1200010 -> 01FD4A40
0022A214  0x01C0100 -> 01FD49F0      0022A269  0x0400100 -> 01FD4A18
0022A225  0x6C00400 -> 01FD4A10      0022A27A  0x0080000 -> 01FD4A20
                                     0022A28B  0x0100000 -> (not stored here)   <- corrected 2026-10-02, OPUS - stored: 0022A0B0+0x1F3 mov [01FD4A90], rax, after the call at 0022A0B0+0x1DB
```

**The nine registration sites** (`00369D30(id, block, size, slotCount)` — ~~`(id, size, alignment)`~~, corrected 2026-09-12):

```
0022A2AE  id 2   0022A304  id 5   0022A35B  id 8
0022A2CB  id 3   0022A321  id 6   0022A377  id 9
0022A2E7  id 4   0022A33E  id 7   0022A394  id 11
```

Two ids are computed rather than written as literals — `lea ecx, [r9 - 0xE]` at `0022A2AE` and
`lea ecx, [r9 - 0xC]` at `0022A2E7`, with `r9 = 0x10` live — which is why **a scan for
`mov ecx, <literal>` finds seven of the nine.** The first pass of this re-derivation reported exactly
that and was corrected against the disassembly.

**One further boot fact from the same function, linking to another document:**

```asm
0022A18B  mov  eax, 2
0022A19A  div  dword ptr [rip + …]      ; -> 01DFE0B4
0022A1A7  mov  dword ptr [rip + …], eax ; -> 02064ACC
```

**`01DFE0B4` is the time-base mode word** documented as **Z-11** in
[`../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md)
— *"`+0x00` integer mode (ships `1`, written `2`)"*. Boot divides the constant `2` by it and stores the
quotient at `02064ACC`, alongside four `1.0f` values written to `02064AC0`–`02064AD4`. **So the
combat time-base mode is read at boot by a function outside combat**, and with the shipped value of
`1` the quotient is `2`. What `02064ACC` feeds is not established here. *(2026-09-30, SWE2-CONTRACT: its writers are
now known — boot, the 7-byte setter `00229F10` used by the area transition `002628B0` → `002695A0` and by the script
verb `mainloopallsyncv` → `0026DB10` ([the boot contract](CONTRACT-boot-fixups.md) I3, `CON-158`, tier 1).
**Its one reader is the field frame, and it is the frame's wait interval (answered 2026-09-30, SWE2-CONTRACT).** A
rip-relative census of every listed body finds three references to `02064ACC`: the two stores above and one read,
`0022AE8F` in the field frame `0022A770`, which passes the value in `ecx` through the 5-byte thunk `0035EC80` to the
tick pacer `0035EB70` (`0022AE8F`–`0022AE97`). The pacer spins while `ticks − saved < max(ecx, 1)`, a signed floor,
and returns the elapsed difference ([EXP-128](../_experiments/EXP-128-exp109-poll-pump-exec.md), which executes that
body on shipped bytes). So the frame waits 2 pacer ticks at 30 fps and 1 at 60. Control
`_index/candidates/swe2contract-ddres-b1-0930/rip_refs.py` (output `rip_refs_02064ACC.out`, positive control the boot
store `0022A1A7`), tier 1; the pacer's behaviour is isolated original-code execution. *Limit:* a read through a base
register would not be seen by the census; what one pacer tick is in wall time is not claimed here.)*

## The `0022A0B0` exclusive subtree — what boot owns (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 144 frontier functions to `0022A0B0` (the startup sequence
`00808D78` reaches). 77 of them sit in the `0x460000`–`0x4FFFFF` VIF1/VU1 band and are excluded
here (covered by the VU1-region and VIF-packet packages); the **67 in-scope members** were
signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| packet-build drivers | `0037DF90` (344 B — calls **27** distinct `0047xxxx`–`004Exxxx` bodies, `02ADEF40`–`02AE0260` refs), `0037E0F0` (596 B — 48 call sites, 47 distinct targets: **45** in the `0047xxxx`–`004Fxxxx` band plus member calls `002EFF50`/`002F0110`, `02AE8620`–`02AE8CF0`), `002EFF50`/`002F0110` (`008631E0`/`008631D0` pair + `002F0280`) | the in-scope *callers* of the excluded VU1 install band — the boot sequence's DMA/program upload arms |
| `00368xxx` init family | `0035E820` (382 B — `005C5230` ×3 + `00863540`/`008636E0`/`00863610`, `022CA62C`/`30`/`022CAE40`, tables `0035EA40`/`0035EC90`/`00D10C78`), `00368C80`, `00368DD0`, `00368ED0`, `00368F70`, `00369070`, `003692C0` | a `00863540`/`008636E0`/`00863610` + `00D10Cxx` table shape over `022Cxxxx`/`022D7Fxx` cells — device/init register fills |
| `0036Dxxx`/`0036Exxx` cell writers | `0036D280`, `0036D2F0` (`022D8E50`–`B4`), `0036D8B0`, `0036D990` (`00908D68`/`80`), `0036E310`, `0036ECE0` (`022D9AB8`/`AE8`), `0036EFD0` (`002DF420`), `0036F4D0` (eight-helper fan-out), `003694D0` (drives leaves `0032EAF0`/`0032EB10`/`00408B50`), `0036B080` (`022D7FD0`/`022D89B8`), `00375120` (`02ADB6E1`/`61`/`02EBFA48`) | boot-time cell initialisation across `022D8xxx`–`022D9Axx`/`02ADB6xx` |
| alloc/pool primes | `0024C970` (623 B — `0024F240` ×4 + alloc pair, `00915448`–`D8` tables), `0024EF90` (683 B — `02F8F340`), `0024F240` (384 B — `00915430`/`3C`), `002FC200` (`01EEBB10` + `02EC19C0`/`02EC32E0`/`02EC3308`), `003B4790`/`003CD6E0`/`003AC890`/`003B16B0`/`003B3160`/`003A3670` (alloc triple `0036C1D0`/`0036A100`/`0036C140` users over `02B4xxxx`/`02EBxxxx`/`02F8F2C0`), `00259DF0`, `00379E90` | boot's heap/pool construction — the deque-alloc family everywhere |
| named inits | `00259180` (the RNG stream seed — one of two `022D9138` writers, §"random number generator"), `00259250`, `0026E1D0` (`008C5F6C`/`78` + `00900320`/`00915778`), `0026F9F0`, `002AB7D0`, `0039CD50` (`003970D0`/`0039AED0`/`0039AF20`, `008C5B48`/`00900384`), `0039AED0`/`0039AF20` (`02AEDD30`–`60` quad), `003970D0` (`02AEE720`), `00382910` (`004679C0` ×2, `022D8EAC`/`B4` + `02AED4A0`/`500`), `003A1D50` (`004FE3C0` ×2 + `004FE420`, `02EBEFC0`/`D8`), `003ABB60` (`02B3F504`/`10`/`28`), `003D7F10`, `003D8C30` (`0050C450` ×4, `02B4E374`–`E8`) | individually-shaped boot steps |
| leaves | `0017D990`/`0017D9D0` (46/206 B — `01DF0000`/`08` + `01F7F490`/`A0`, one rip-indirect), `0017E410`, `0024F780` (`02091140`), `0025A600`, `0032EAE0`, `0032EAF0` (`022C5AF0`), `0032EB10` (`022C59F0`), `00358510`, `0035B270` (`02EC0B81`), `00360370`, `00364200` (`022CBB9C`), `0036D260`, `00376A80`, `003773C0` (`02ADCFC0`), `0037B390`, `003B3E10` (`02EBCC84`/`CD84`), `00408B50` (`02B62DAA`), `00536120` | ~19 small clears/thunks |

The boot subtree is mostly breadth: dozens of small cell/bank writes plus the two
packet-build drivers — which is what "runs once, fixes everything" looks like as a call tree.

One in-scope member is now bound in full elsewhere: `003325C0`, the 12-byte thunk that
passes the `022C6F30` context block into `CharacterRenderSystem_AllocateAndInitialize`
(`003325D0`), heads a 33-member exclusive subtree — the `0x48930` pool allocation, the
`0041E3A0` subcontainer battery, the `004269A0` record/handler-table init, and the
`00426480` tail publish. All 33 members are disassembled and interior-cited in
[`../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` §15](../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md).

**The subtree is not engine-internal — it deliberately crosses two layers.** Downstream, the
packet-build drivers' `0047xxxx`–`004Fxxxx` targets and the helpers under `0036F4D0`/`0037E0F0`
are **Presentation**-owned bodies (`00465F60`, `0048CE70`, `004FD060`, `004FE420`…) — display and
render-state setup is part of what boot installs. The alloc/pool primes and several leaves call
**Resource**-layer loaders (`001D6FA0`, `001D6EE0`, `001D6F20`, `001D6E80` under `0017D9D0`,
`0024EF90`, `0024F240`; `0032E400`/`0032E620` under `00259DF0`/`00379E90`) — boot primes the
resource pipeline as well as the heap. And upstream, `0036A100` — one of the alloc triple primed
here — is later called from 25 Presentation builders (`00501750`, `00503CD0`, `003EDAD0`…), so the
boot-primed allocator serves the render path at run time, not only startup.

The other directions are smaller but real: `007980A0` calls **platform**/online init
(`007A0C60`, `008655E0`, `0020CD80`…, 8 edges) and the **platform** bodies `0019A510`/`007979B0`
(3) — achievements and OS glue are boot-installed too; `0036F4D0` reaches **movement**
(`0026E1D0` → `0026E640`; `003ED820`/`003ECF70`) and `001EDDC0` calls `00337A00` (5);
`0036A100` is called by **actor** `003306E0`/`00330310` and **field** `003319D0`/`003EA820`/
`00267930` bodies, and `0022A0B0` itself calls actor `002368D0` and world `00266D10` — the
startup sequence hands off to every layer that later ticks.

*(Pass 22 live-graph completion, 2026-09-15: the boot path's reach also runs through `Audio`
— `001D6E80`/`001D6EE0`/`001D6F20`/`001D6FA0` and one more are all called by `00210760` (5
edges), the audio-init leg of the same startup walk the note above describes.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Story, event, quest and hunt — one edge, two call sites, and one goes down each branch of the
callee.** The arbiter this page cites, `00253C70`, asks
`PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` — 122 bytes, owned by that layer — at
**`00253F21`** and **`002540AF`**, and both arguments are constants compiled into the arbiter.

The gate reads its id twice over: it keeps the low fourteen bits and tests bit 14 (`and edi, 0x3fff`
/ `bt ecx, 0xe`). **Set means the authored route** — it tail-jumps with the masked id — and clear
means the primary route, which answers 0 above `0x200`, answers the two lowest ids as constants, and
otherwise indexes a bit per id (`id >> 3` selects the word, `id & 7` the bit).

- `00253F21` passes **`0x5E`**, formed as `lea ecx, [rax + 0x5e]` at `00253F1E` on the path where the
  preceding query has just been tested and found zero. Bit 14 is clear, so this is the primary
  route, and its answer gates the pair of calls that follow.
- `002540AF` passes **`0x4008`** as an immediate. Bit 14 is **set**, so this one takes the authored
  route with id 8.

**This page owns nothing in that layer.** The crossing is that boot-time input arbitration consults a
persistent story-progress flag before it commits — which is the direction worth stating, because the
flag decides the arbiter's behaviour and not the other way round.

*The far end is named by symbol rather than by address on purpose: writing that address here would
make it a citation, and its own neighbours include a Script/VM Native Bridge edge this page does not
mention — so clearing one finding by naming it would have opened another.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — SERVICE.** `002368D0` on this page calls `BattleAction_ResetPresentationSlotPool`, owned by that layer. What it reaches is a 99-byte reset of **32 slots of `0x30` bytes** based at `022C17D8`: it clears the two heads at `[022BEB88]` and `[022BE978]`, and stamps each slot with `0x80000000`, a `-1` counter and an `0xFFFF` sentinel; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (4 edges, one fan-in).** All 4 edges are UI bodies reaching `004FE3C0` on this page. `FUN_0028faf0` is the worked example - it is a 75-byte step over the HUD object at `[0209BE80]`: it sets **bit 8 of `dword[+0x10F68]`** and then works the `+0xA0` and `+0x80` sub-objects. The crossing is **one shared subject with 4 callers on that layer**, not 4 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Script_VM_Native_Bridge — CLIENT on one edge, SERVICE on three (4 edges, every body read).**
`00266D10` on this page calls `VMNativeCommandDispatch_InitializeFamilyTables`, and that is a boot
fixture in the same sense as the rest of this page: it fills all sixteen slots of the table at
`02B57EF0` with one default descriptor (`01F26720`) using `rep stosq`, then overwrites the
individual slots with the real family tables — `01EED700`, `01F281B0`, `01F29418` and the rest. The
default is written first so a family nobody registers still resolves to something.

The other three edges run the other way, and all three have the same shape: a script verb handler
pops its arguments off the VM value stack through `00267E10`
`VMValueStack_PopInt32CoerceFloat32` and hands them to a function cited here. `0050DF70` pops two
and calls `0032E400`, which refuses the id `0xFF`, indexes the pointer table at `022C51F0` and
bounds its second argument at `0x400`; `0050DFE0` pops several and calls `0032E620`, which latches
its first two arguments into `022C51D8`/`022C51DC` before doing anything else; `0050D8F0` calls
`0036A100`, which reads the handle at `022D89BC` and passes the caller's value straight through.
The crossing is those calls; the script layer is a caller here, not a co-owner. Read from the
shipping bytes 2026-09-14 (OPUS).
- **Audio — CLIENT and SERVICE (14 edges).** 5 inbound (Audio bodies `00210760`, `001DBA40` call page-cited `001D6E80`, `001D6EE0`, `001D6F20`); 9 outbound (page-cited `00210760`, `002628B0`, `0022A770` call Audio bodies `002216B0`, `007A5B20`, `007A4D50`). Substantive edges include `001D6E80` is called by `00210760`; `001D6EE0` is called by `00210760`; `001D6F20` is called by `00210760`; `001D6FA0` is called by `00210760`.
- **RNG_Random_Selection — CLIENT and SERVICE (7 edges).** 3 inbound (RNG_Random_Selection bodies `RNG_MT19937_Seed` (00863D30), `RNG_MT19937_NextFloatClosed` (00863C80), `RNG_MT19937_NextU32` (00863BF0) call page-cited `RNG_MT19937_SeedState` (00866D60)); 4 outbound (page-cited `RNG_MT19937_NextU32` (00863BF0), `0022A0B0`, `RNG_MT19937_Seed` (00863D30) call RNG_Random_Selection bodies `RNG_MT19937_SeedState` (00866D60), `RNG_MT19937_Seed` (00379CF0), `RNG_MT19937_TwistState` (00866B90)). Substantive edges include `RNG_MT19937_NextU32` (00863BF0) calls `RNG_MT19937_TwistState` (00866B90); the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT and SERVICE (9 edges).** 2 inbound (Save_Load_Settings bodies `002EF300`, `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210) call page-cited `0032E620`, `RNG_MT19937_Seed` (00379CF0)); 7 outbound (page-cited `0017D4C0`, `007980A0`, `002628B0` call Save_Load_Settings bodies `SaveloadManager_RefreshDisableAutosaveList` (001C1710), `SaveloadManager_GetSingleton` (001C18E0), `SaveloadManager_EnsureSingleton` (001C18A0)). Substantive edges include `0017D4C0` calls `SaveloadManager_RefreshDisableAutosaveList` (001C1710); `0017D4C0` calls `SaveloadManager_GetSingleton` (001C18E0); `0017D4C0` calls `SaveloadManager_EnsureSingleton` (001C18A0); `00266D10` calls `002EF2D0`; the remaining edges run through shared helpers the page cites.
- **CombatFormula — CLIENT (53 edges).** 4 inbound (CombatFormula bodies `BattleFormula_BuildCandidateStatusMask` (003851F0), `00387130`, `BattleFormula_RollSpecialGuardOutcome` (00387FD0) call page-cited `RNG_MT19937_NextU32_Thunk` (00379CD0)).
- **Party — SERVICE (4 edges).** 4 outbound (page-cited `002628B0`, `0022A770`, `002695A0` call Party bodies `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0), `PartyFocus_ClearCurrentActorIfEligible` (00358B40), `PartyControl_SetMovementSuppressionBit` (00359200)).
- **Rewards_Progression_Economy — MECHANICAL (3 edges).** 3 inbound (Rewards_Progression_Economy bodies `EnemyChain_UpdateOnDefeat` (00317ED0), `002F9A60`, `002F9B20` call page-cited `RNG_MT19937_NextU32_Thunk` (00379CD0), `00229E40`) - shared-helper call surface, not a Rewards_Progression_Economy relationship of this page's subjects.
- **Status_Periodic_Terminal — MECHANICAL (1 edge).** 1 inbound (Status_Periodic_Terminal bodies `BattleFormula_AdvanceStatusTimersAndBuildResult` (00386C70) call page-cited `RNG_MT19937_NextU32_Thunk` (00379CD0)) - shared-helper call surface, not a Status_Periodic_Terminal relationship of this page's subjects.
## The `001EDDC0` exclusive subtree — all 10 members bound (SWE2-FRONTIER, followup queue)

`001EDDC0` (~160 B) — the frame-rate/timing bootstrap. `ecx == 0` (the
30 fps arm) queries `timeGetDevCaps` (`008C2A90` import) into an 8-byte
`TIMECAPS` on the stack; on `TIMERR_NOERROR` it stores `caps.wPeriodMin`
at `dword[01F82E40]`, requests that scheduler resolution via
`timeBeginPeriod` (`008C2A98` import), and arms `byte[01F82E3C]`
(`001EDE1F`–`001EDE46`). `ecx != 0` (the 60 fps arm) seeds the timing
block — `dword[01DFE0B4] = 2` (the 30→60 fps divisor),
`float[01DFE0B8] = 2.0f`, `float[01DFE0BC] = 0.5f`,
`dword[01F82E38] = 1` (`001EDDC8`–`001EDDF2`) — runs the LUT battery
`0033F020`, and, when the period flag is armed, releases the earlier
request with `timeEndPeriod(dword[01F82E40])` through the `008C2AA0`
import, clearing the flag (`001EDE01`–`001EDE1D`). Either way it finishes
on `0032AE70`, `003333D0`, `00337A00` (`001EDE4D`–`001EDE57`). The three
imports are `WINMM.dll` slots resolved through the PE import directory —
the same reading
[`../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
§17.1 records; an earlier version of this paragraph misread them as
`QueryPerformanceFrequency`/`QueryPerformanceCounter`/`Sleep`
(corrected 2026-09-21, `FABLE-CONTRA-FRONTIER-001EDDC0-IMPORTS-ARE-WINMM-NOT-QPC`).

| member | role | interior |
| --- | --- | --- |
| `002BDA90` | packs `dword[01DFE0B4]`-derived nibbles — `cl = (d*3)<<2`, `al*0xF` — into `0209E610`/`0209E611` | [`002BDA9B`](../_index/ADDRESS-INDEX.md) |
| `0032AE70` | seeds `float[022C3180]` — `001EDE70()` gate then `00861F5C(0.5)` → `cvtsd2ss` | [`0032AE85`](../_index/ADDRESS-INDEX.md) |
| `003333D0` (30 B) | `dword[02EC0F90] = (int)(float[01DFE0B8] * 30.0f) << 2` | [`003333D8`](../_index/ADDRESS-INDEX.md) |
| `00337A00` | `dword[02EC0F80] = [01DFE0B4]*0xF0`; reciprocal divide `02EC0F84 = 6.28f/…` seeded off the rate | [`00337A32`](../_index/ADDRESS-INDEX.md) |
| `0033ECE0` | float-table entry generator — `(table, index, count)`, `00861EBA` math core | [`0033ED1B`](../_index/ADDRESS-INDEX.md) |
| `0033F020` (43 B) | LUT battery driver — `0046FBF0`, `00471100`, the four `00471xxx` walkers, tail `00473210` | [`0033F02E`](../_index/ADDRESS-INDEX.md) |
| `00471330` | double-and-fill walker — `01F22120` counter `*2`, fills `01F22130`/`01F22170` via `0033E310` | [`00471347`](../_index/ADDRESS-INDEX.md) |
| `004715F0` | same pattern — `01F221B0` counter, `01F221C0`/`01F222B0` tables | [`00471607`](../_index/ADDRESS-INDEX.md) |
| `004718F0` | same pattern — `01F223A0`/`01F223A4`/`01F223A8` counters, `01F223B0` table | [`00471907`](../_index/ADDRESS-INDEX.md) |
| `00472580` | same pattern + SIMD — `01F227E0`/`01F227E4` counters, `mulps` over `01F23FF0`, `01F240F0` byte table | [`0047259A`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001EDE70`, `00861F5C`, `00861EBA`,
`0033E310` (the per-entry fill), `0046FBF0`, `00471100`, `00473210`, and
the three `008C2Axx` imports. Every `00471xxx` walker doubles its sample
counter and rebuilds its float table through `0033E310` — the
frame-rate-dependent LUTs this page's boot pass fixes.

## SWE2-EC7-67 update - `00465F60`

`00465F60` (129 B) is a boot-time Presentation body - `005C5230`/`004FE3C0`/`004FE3D0` pairs plus `02EBB700`-`02EBB730`. Interior anchor `00465F6B` (a `005C5230` call).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*The functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`boot_interior.py`](../_index/candidates/opus-boot-interior-1001/boot_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017D990` | 46 B | calls `0017D9D0(*(01DF0000), 01F7F490)`, then tail-calls `0017D9D0(*(01DF0008), 01F7F4A0)` | `0017D9A2`, `0017D9A7`, `0017D9B9` |
| `0017D9D0` | 206 B | looks up `rcx` through `001D6F20(rcx, 1)`; on failure passes `008C58C0` to `0017D280`; otherwise reads the entry (size from `001D6EE0`) into a stack buffer through `001D6FA0`, calls the import at `008C2F78` on (buffer + 7, `008C58D0`), copies that many bytes from buffer + 7 to `rdx` through `00861EBA`, and releases the entry with `001D6E80` | `0017D9FD`, `0017DA53`, `0017DA63`, `0017DA73` |
| `0017E6E0` | 59 B | calls `001DF340(*(01F82D20), 0x19, ecx)`, then `00198960(00198790(), ecx == 0)`, and tail-calls `0022A4F0` | `0017E6F7`, `0017E6FE`, `0017E70C`, `0017E716` |
| `002216B0` | 86 B | when the qword `01FD4138` is null, allocates `0x8D8` bytes through `00210EC0`, constructs them with `0021E570(object, ecx, edx)` and stores the result at `01FD4138` | `002216C8`, `002216D7`, `002216EE`, `002216F4` |
| `0025A600` | 17 B | stores `xmm0` at `02098DE0` and `xmm1` at `02098DE4` | `0025A608`, `0025A610` |
| `0026DB10` | 24 B | divides `ecx` (2 when `ecx` is negative) by the dword `01DFE0B4` and tail-calls `00229F10` with the quotient | `0026DB17`, `0026DB1B`, `0026DB23` |
| `0026E1D0` | 130 B | stores float constants into the dwords around `0209A6EC`, zeroes qwords beside them, sets the dword `0209A6FC` to 1, copies one 16-byte constant into the four 16-byte globals `0209A380`..`0209A3B0`, and tail-calls `0026E640` | `0026E1E2`, `0026E221`, `0026E231`, `0026E24D` |
| `0026F9F0` | 136 B | clears the low three bits of byte `02F8F29E`, zeroes the dwords `02F8F220` and `02F8F238` and the 16 bytes at `02F8F228`, fills the 96 bytes `02F8F23C`..`02F8F29B` with `0x03`, and sets the word `02F8F29C` to `0x100` | `0026F9F9`, `0026FA12`, `0026FA66`, `0026FA6E` |
| `002AB7D0` | 65 B | calls `00229E40`; when the result is 7, 8 or 11 stores `0x1C` at `01E0CDF8` and 1 at `0209CC38`, otherwise stores `0x18` at `01E0CDF8` | `002AB7D4`, `002AB7DC`, `002AB7E9`, `002AB802` |
| `0032EAF0` | 32 B | fills the `0x100` bytes at `022C5AF0` with `0xFF` when `ecx` is non-zero, else with 0 | `0032EAF7`, `0032EB03`, `0032EB08` |
| `0032EB10` | 39 B | fills the `0x100` bytes at `022C59F0` the same way, then sets bit 7 of byte `022C5A0F` | `0032EB17`, `0032EB28`, `0032EB2F` |
| `00358510` | 52 B | calls `00358450(0, 1)` and `00358450(1, 0)`, sets the bytes `022C7F99` and `022C7F98` to 0 and the byte `022C7F9A` to 1 | `0035851B`, `00358525`, `0035852A`, `00358538` |
| `0035B270` | 119 B | initialises 32 records of `0x20` bytes at `02EC0B80` (byte `+0` = index + 1, byte `+1` = 0, word `+2` = 0, qword `+8` = 0), then sets the byte `02EC0F60` to `0xFF`, clears further fields and sets the dword `02EC0B3C` to 1 | `0035B283`, `0035B288`, `0035B298`, `0035B2DC` |
| `0035E820` | 382 B | resets the dwords and qwords around `022CA5E0`..`022CA62C` (`022CA62C` = -1), creates two objects through `00863540`, calls `008636E0` with a descriptor holding `0035EA40` and `0x4000` and passes its result to `00863610`, spins until the dword `022CA630` is non-zero, registers through `00369070(0, ...)`, and makes its `005C5230` calls | `0035E8A7`, `0035E920`, `0035E930`, `0035E943` |
| `0035EB70` | 258 B | compares `00368C70()` with `00862090()`; when they differ, spins until the qword `022CA5E0` has advanced by max(`ecx`, 1) and returns the advance; when they match, calls `0017D3E0` (and `003691B0(0)` / `00369190(0)` when it returns 0), recomputes its timing dwords, calls `0035E7A0` and records max(`ecx`, 1) and `edx` | `0035EB90`, `0035EBB0`, `0035EBC3`, `0035EC05` |
| `0035EC90` | 169 B | increments the qword `022CA5E0` and the dword `022CA5F0`; when one dword counter has reached another it tests bit 13 of a mode-selected dword and may set the dword `022CA600` to 1; when that flag is set and the function pointer at `022CA5C8` is non-null, calls it and clears the pointer; then calls `0035FCA0` and tail-calls `003690F0` | `0035EC94`, `0035ECFE`, `0035ED1E`, `0035ED34` |
| `00368C80` | 325 B | fills the block around `022D7F68` (an object from `00863540` at `022D7F68`, entry `00368C10`, `0x4000`), calls `0019C5D0`, `008636E0` and `00863610`; when a configured index is non-zero and the qword `022D7F70` (read once) is non-zero, calls `00863520` with `0x24` and `0x22`; with it zero the loop `00368D76`-`00368D81` does not re-read it | `00368CC0`, `00368D41`, `00368D76`, `00368D93` |
| `00368DD0` | 247 B | creates two objects through `00863540`, fills a descriptor block with entry `00369100` and `0x4000`, and calls `0019C5D0`, `008636E0` and `00863610` | `00368E06`, `00368E18`, `00368E7F`, `00368EA9` |
| `00368ED0` | 90 B | stores `00862090()`'s result at `022D7FB0` and passes it to `00863520` with `0x20`; runs `00368F70`, `00368DD0` and `00368C80`; creates an object through `00863540` stored at `022D7F90`; tail-calls `0035E820` | `00368EE1`, `00368EE7`, `00368EF6`, `00368F25` |
| `00368F70` | 214 B | when `003692C0()` has bit 2 set, creates an object through `00863540`, calls `008636E0` with a descriptor holding `00368AE0` and `0x4000`, passes the result to `00863610`, and stores `005C5230(callback, object)`'s result at `022CFF18` | `00368F8E`, `00369000`, `0036901A`, `00369027` |
| `00369070` | 15 B | stores `rdx` in the qword table at `022CFF10`, index `ecx` | `00369073`, `0036907A` |
| `003694D0` | 50 B | calls `0032EAF0(0)` and `0032EB10(0)`, then tail-calls `0016D6A0` with 1 when `00408B50()` is 1, else with 0 | `003694D6`, `003694DD`, `003694E7`, `003694F2` |
| `0036D260` | 23 B | zeroes the qwords `022D8E30` and `022D8E38` and the dword `022D8E40` | `0036D262`, `0036D269`, `0036D270` |
| `0036D8B0` | 47 B | calls `0036C1D0(6, 5)`, `002DEE90(-1)`, `005C5230` and `002DEE90(-1)`, then tail-calls `0036C140` | `0036D8BC`, `0036D8C4`, `0036D8C9`, `0036D8DA` |
| `0036ECE0` | 105 B | initialises two arrays of `0x18`-byte records, 2 at `022D9AB0` and 4 at `022D9AE0`: byte `+0` = 0, byte `+1` = index, word `+2` = 0 (1 in the second array), qwords `+4` and `+0xC` = 0, word `+0x14` = `0xFFFF`, word `+0x16` = 0 | `0036ECF0`, `0036ED04`, `0036ED30`, `0036ED46` |
| `0036EFD0` | 39 B | sets the byte `022D9B41` to 1, calls `002DF420(1)`, sets the byte `022D9B40` to 1 and tail-calls `002DF420(0)` | `0036EFD9`, `0036EFE0`, `0036EFE7`, `0036EFF2` |
| `0036F4D0` | 63 B | calls in order `0036D280`, `00465F60(0x100)`, `003A1D50`, `00467BB0`, `0026E1D0`, `00382910`, `003ECF70`, `00475310` and `003ED820`, then tail-calls `00467AD0` | `0036F4DE`, `0036F4E3`, `0036F501`, `0036F50A` |
| `00376A80` | 64 B | zeroes the byte `02ADBB30`, the dword `02ADBB34` and the dwords at `02ADBB40` + k*`0x90` for k = 0..7 | `00376A89`, `00376A8F`, `00376AB9` |
| `003773C0` | 52 B | zeroes the dword `02ADBFC4` and the first dword of 128 `0x20`-byte records ending at `02ADCFC0` (walking down), then clears the byte `02ADBFC0` and the qwords `02ADBFC8` and `02ADBFD0` | `003773C9`, `003773D7`, `003773DD`, `003773E5` |
| `0037B390` | 49 B | sets the bytes `02ADD931` = 1, `02ADD932` = 4 and `02ADD930` = 0, calls `0037B3D0`, then sets `02ADD931` = 0 and `02ADD933` = 3 | `0037B39B`, `0037B3A9`, `0037B3B5` |
| `0037B3D0` | 127 B | calls `0036B060(0xB)`; when the byte `02ADD930` differs from `02ADD931`, takes `0x3C0000` (when `02ADD930` is 3) or `0x400000`, calls `00369760(0xB)`, `0036D160(0xB)`, `0036D250` and `0036D240(size)`, stores that result and calls `00369D30(0xB, result, size, 0x100)`; finally sets the byte `02ADD932` to 4 | `0037B3F3`, `0037B420`, `0037B43D`, `0037B442` |
| `0039AED0` | 73 B | stores `xmm0` at `02EBEFFC` and `xmm1` at `02EBEFF8`, and copies four 16-byte constants to `02AEE5A0`..`02AEE5D0` | `0039AEDF`, `0039AEEE`, `0039AF11` |
| `0039CD50` | 100 B | between `0036C1D0(9, 10)` and `0036C140` allocates `0x20000` bytes through `0036A100` into `02AEED50`; then runs `003970D0`, calls `0039AED0` with one float constant in both arguments and `0039AF20` with another, sets the byte `02AEE910` to 8 and zeroes the dword `02AEE900` and the qword `02AEE908` | `0039CD66`, `0039CD6B`, `0039CD87`, `0039CD9B` |
| `003A1D50` | 82 B | calls `004FE3C0` on `02EBEFC0` and `02EBEFD8`, clears a dword, then calls `004FE420(02EBEFC0, 0x200, 0)` and tail-calls `004FE420(02EBEFD8, 0x200, 0x200)` | `003A1D5B`, `003A1D67`, `003A1D85`, `003A1D9D` |
| `003ABB60` | 315 B | in the block `*(02B3F528)`, zeroes dword `+0` and byte `+0x20` of 128 `0x70`-byte records; takes the first record whose dword `+0` is 0, increments the serial `02B3F504` (wrapping above `0xFFFFFF` to 1), stores (serial << 8) OR index at `+0`, copies a `0x50`-byte template (byte 0 = 7, byte 3 = 3) to `+0x20`, calls `003AC920`, and links the record at the end of the list headed at `02B3F508` / `02B3F510` | `003ABB83`, `003ABC03`, `003ABC1E`, `003ABC48` |
| `003AC890` | 91 B | when the qword `02B3F528` is 0, allocates `0x3800` bytes through `0036A100` between `0036C1D0(6, 6)` and `0036C140` and stores them there; then sets a float, a qword `0x10000` and a byte beside it, and tail-calls `003ABB60` | `003AC8AF`, `003AC8B4`, `003AC8D0`, `003AC8E6` |
| `003B16B0` | 73 B | after `0036C1D0(8, 10)`, zeroes the `0x600` bytes at `02EBE5E0`, clears the dword `02EBEBE0` and a byte, calls `0024C460(7)` and tail-calls `0036C140` | `003B16C3`, `003B16D0`, `003B16DA`, `003B16F4` |
| `003B3E10` | 35 B | zeroes 32 eight-byte entries from `02EBCC80` (byte `+0`, word `+2`, dword `+4`) | `003B3E20`, `003B3E27`, `003B3E2D` |
| `003D7F10` | 31 B | zeroes the first dword of 32 `0x84`-byte records from `02EBBA00` | `003D7F20`, `003D7F23`, `003D7F29` |
| `003ED820` | 23 B | zeroes the qword `02B5F1B0` and the 16 bytes at `02B5F1A0` | `003ED823`, `003ED82E` |
| `004FE3D0` | 79 B | unless dword `+0x14` is set, calls `003EC8A0` first; zeroes `+0`, `+8` and `+0x10`; when `rdx` is non-zero, allocates `rdx`*16 bytes through `003EC8D0(6, ...)`, stores the block at `+0` and `+8` and the count at `+0x10` | `004FE3E6`, `004FE3ED`, `004FE405`, `004FE411` |
| `00501750` | 203 B | after `00501440`, reads a header from the byte stream at `rdx` (byte 0 to `+0x10`, `0xFF` ends; bytes 2 and 3 to `+0x12` / `+0x13`); for kind 0 or 1 with a non-zero count, allocates count*64 (kind 0) or count*1024 (kind 1) bytes through `0036A100` into `+0x20` and copies them from the stream through `00861EBA`; then calls `00503180` on each record of the list `003AA1F0(1, 0x50)` (stepping with `003AA240`); returns the advanced stream pointer, or 0 for another kind | `00501771`, `005017C1`, `005017D3`, `005017F3` |
| `00536120` | 24 B | makes `rcx` an empty self-linked list head (`+0` and `+8` = `rcx`), zeroes `+0x14` and `+0x18`, and sets `+0x10` to -1 | `00536125`, `00536129`, `00536130` |
| `00863540` | 80 B | allocates 8 bytes through `00210EC0`, constructs them with `008632E0(object, [rcx+8], [rcx+4])`, passes 'non-null' to `0016D6A0` and returns the object | `00863552`, `00863568`, `0086357D` |
| `00863610` | 62 B | passes '`rcx` non-null' to `0016D6A0`, stores `rdx` at `+0x20` of the record `rcx` points to, calls the import at `008C2330` with that record's `+8`, and returns 0 | `00863628`, `00863630`, `0086363B` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-what-the-engine-fixes-at-boot-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003AA240` | 60 B | calls `0020E600(dword +0)` of `rcx` and follows the chain `0020E600(dword +0)` of each result, returning the first record whose word `+0xC` and byte `+0xE` equal those of `rcx`, or 0 once `0020E600` returns null | `003AA24B`, `003AA259`, `003AA263`, `003AA26A`, `003AA274` |
| `00467AD0` | 42 B | stores 0x4000 to dword `02CA5FF0` and stores dword `022D8EB4` times dword `022D8EAC` (signed `imul`), times 3, divided by 64 with signed rounding toward zero (`cdq`, add 63 when negative, `sar 6`) to dword `02CA5FF4` | `00467AD6`, `00467ADD`, `00467AE7`, `00467AF0`, `00467AF3` |
| `00467BB0` | 61 B | calls `00536120` on the address `02EBB6A0`, then stores the dword 0x28 to `02EBB6B0`, the address `00467B20` to qword `02EBB6B8` and zeroes the qwords `02EBB6C0` and `02EBB6C8` | `00467BBB`, `00467BC7`, `00467BD1`, `00467BDA`, `00467BE1` |
| `00475310` | 121 B | stores the floats 10 (`008F8180`) to `02EBA4C4`, 150 (`009155DC`) to `02EBA4C8`, 1.5 (`00901B3C`) to `02EBA4CC` and 16 (`01CEBC84`) to `02EBA4E0`; zeroes the dwords `02EBA4C0` and `02EBA4D0`, stores the dword 5 to `02EBA4D4`, the qword 0x40 to `02EBA4D8`, the dword 0x40800000 to `02EBA4E4` and the qword 0x40800000 to `02EBA4E8` | `00475322`, `00475342`, `0047534A`, `0047535E`, `0047537D` |
