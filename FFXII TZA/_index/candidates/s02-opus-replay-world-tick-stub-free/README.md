# S-02: the world tick executed with NO application stub, in all six frame modes (OPUS, 2026-09-25, block 318; world revised block 319)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-02's binding gap reads *"runtime MIXED on EXP-191 (all
three pages executed, stubs disclosed, one named exposure `0026A5F0` on WT-4) … L2 closes on a no-stub or live tick
execution"*. **This is the no-stub tick execution.** EXP-191 ran the tick over about 95 scripted leaves. Here nothing
on the tick's path is scripted.

## What was run

`check.py` runs the tick `00314020` in modes 0–5. `world.py` builds the world and runs it; `world.json` holds the world
recipe, and `printf_bridge.py` the formatting bridge.

- **No application stub.** Every function entered is shipped code inside ALLOWED: the tick's static closure plus the
  shipped jump and indirect targets that `edges.tsv` does not follow, which are `002284F0`, `00253C50`, `00268D10`,
  `002900C0`, `0035D640`, `005CDB90`, and the EASTL allocator's `001EDF80` / `001EDFE0`. **Each run must reach the
  tick's own `ret` (`0031436C`).**
- **The world is BUILT by shipped initialisers where one exists.** Five are run before the tick:
  - `00809124`, the CRT startup routine that sets up the module's onexit / lock state (without it the CRT `atexit`
    shim jumps through an unset encoded pointer);
  - `0019CDE0`, the string pool (new 0x120 + ctor `0019C7C0` -> `[01F81150]`);
  - `003DAE30`, the movement-body pool (a zeroed pool is not an empty one: its free list needs the `0xFFFF`
    sentinels this writes);
  - `001B7EE0` (new 0xBB8 + ctor `001B6D90` -> `[01F81218]`) and `001DAD60` (new 0x1C0 + ctor `001D9400` ->
    `[01F82CF0]`). Block 318 had planted zero blocks for both; this revision (block 319) builds them.
- **Nine singleton cells get zero-filled blocks** (`world.json` `fixes`). Their constructors belong to the engine's boot
  and are not run:
  - `02EBF190` (a loaded data table);
  - `02EA5368` (the PApplication instance);
  - `0208EA40` / `48` / `58` (the widget pools, built by the large UI routine `00247AE0`);
  - `0209AC30` (`Manager0209AC60`'s cell, set by a setter `002800F0` from its creator);
  - `022C6F28` (the render-record array; `003325D0` takes an owner argument);
  - `01F83438` and `01F82D20` (`GameSettingConfig`, filled from `GameSetting.ini`), both reached by `001DAD60`'s
    constructor.
  **This is the harness's main limitation.** A zero block is planted data, not an idle object built by its
  constructor. One visible consequence: the sound layer logs `[sead][!!error!!]LayAction exhausted!!` (a zeroed pool
  reads as exhausted).
- **Emulation environment:** a TEB for `gs:` (stack bounds for `__chkstk`), and TLS set up from the PE TLS directory
  as the loader does.
- **Imports.** Every IAT slot is trapped; only named bridges are serviced (listed in `world.py`):
  - memory and CRT;
  - a faithful `vs*printf` over the emulated `va_list`;
  - maths (the single-precision family, exact then rounded to f32);
  - OS synchronisation, which always succeeds and never blocks;
  - `GetProcAddress` returning 0, so the CRT takes its own fallback;
  - onexit registration;
  - debugger and stdout output (recorded);
  - a **deterministic clock**.

  Any other import stops the run.

**All checks pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `stub_free_all_modes` | the binding gap | **modes 0–5 all run to the tick's `ret`**, entering 311 (mode 0), 250 (mode 1) and 195 (modes 2–5) shipped functions (the functions entered include the initialisers) |
| `WT1_mode_consulted_at_five_sites` | WT-1 | in every mode the tests at `003140CF`, `003140DC`, `00314103` and `00314249` each run once. The paired `cmp r14d, 1` sites (`00314108`, `0031424E`) run whenever the preceding test did not settle the mode |
| `WT2_drain_before_mode` | WT-2 | the drain `0025BFB0` is entered **before** the first mode test in every mode |
| `WT3_active_word_set_and_cleared` | WT-3 | `022C2548` is written **exactly twice** per tick: 1 at `00314047`, 0 at `0031435D`. It reads 0 afterwards, and the tick leaves through its single `ret` |
| `WT4_sentinels_and_unstaged_writes` | WT-4 | both words hold `0xFFFFFFFF` in the image. With nothing staged, the tick writes `01EED060` once (`00314092`) and never `01EED064`. **The staged consume path is not executed:** a staged request drives a world transition (`003C5E50` …) that reaches the UI manager and beyond this world |
| `WT5_loop_bounds_observed` | WT-5 | mode 0: the sub-step compare at `0031421F` runs **16** times, the slot compares at `003141E9` / `00314218` **80** (16 × 5), and `00314270` **5**. **Mode 1: `00314132` and `0031425D` each run twice**, because both mode-1 loops start at slot **3** (see below) |

## What the execution adds

1. **The first stub-free execution of the S-02 tick, in all six modes.** This is the closer the binding gap names,
   with the limitation above (nine zero-filled singletons) stated rather than hidden.
2. **In mode 1 the per-slot loops cover slots 3 and 4 only.** `003140FF lea ebp, [r13+3]` (with `r13 = 0`) seeds both
   mode-1 loops, the four-call loop at `00314112` and the `002623A0` loop at `00314254`, at 3. So slots 0–2 get no
   per-slot call in a mode-1 frame. WT-5's "five slots" is the mode-0 shape; WT-6's slot-0 work does not happen in
   mode 1 at all.

## Not covered

- the staged mode-request consume path (WT-4's one-shot, static only);
- WT-6's per-slot no-op claim (the contract carries it without re-deriving it; not re-derived here);
- idle objects built by their own constructors for the nine singletons;
- a live game.

## WT-6 (OPUS, 2026-09-25)

`wt6.py` runs a mode-0 tick in the same world with **no application stub**. It counts the instructions inside each
per-slot call of the loop `003141C3`-`003141EC`. The hooks are added in the tick hook and then `uc.ctl_flush_tb()`
is called.
- **`00234590` and `00234520`:** each opens with `test ecx, ecx / jne epilogue`. Their guarded bodies (`002345B9`,
  `00234533`) run **for slot 0 only** (3,461 and 224 instructions). Slots 1-4 take the guard exit (20 and 9).
- **`0025D9E0`, the actor drive pass:** it has no slot guard and runs the **same path for all five slots** (31
  instructions each). This world holds no actors for it to drive, so the claim executed is "not gated on slot 0".
  The volume of its work is not executed.
- Only sub-step 0 calls the three; later sub-steps are gated per slot by `00267310`, which returns 0 here. The 80
  loop-site hits of `WT5_loop_bounds_observed` are consistent with this.
- Two runs give an identical `wt6_result.json` (md5 `d442c6e824629a4b43e01c95e40449c4`). Independent review is requested
  from SWE2-AUDIT-SEM (author OPUS).
