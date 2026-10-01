# S-42 runtime: per-invariant stub exposure for EXP-099 (+ EXP-008 / EXP-009 live, EXP-093 / EXP-098 misattributed) (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-42 field music selection. Runtime **MIXED**, qualifier *"isolated original-code execution under
disclosed stubs — no per-invariant stub-exposure analysis yet"*. Binding gap: *"types PARTIAL, runtime
ASTRA/ORACLE's gap"*. Contracts (column 6 of `important-subsystems.tsv`):
`18-Audio/CONTRACT-field-music-selection.md` (entries `003EAA70`, `00265270`; §4 = one precondition, one
postcondition, three unlabelled invariant bullets, numbered FM-a..FM-c here) and
`18-Audio/CONTRACT-music-control-file-and-bgm-stream.md` (entries `003EAB90`, `0051EDB0`; §4 = MC-1..MC-8).
This note scores nothing.

## Which records belong to this row

| record | its own `contract:` field | touches a S-42 contract? | evidence class |
|---|---|---|---|
| **EXP-099** field-music-selection-exec | `CONTRACT-field-music-selection.md` | **yes** | NATIVE-REPLAY (Unicorn, `live_game: false`) |
| **EXP-008** the real music table | `CONTRACT-field-music-selection.md` | yes | **live** read-only capture of `[02B5E0D0]` + an offline replay differential over the captured bytes |
| **EXP-009** the game's own answer | `CONTRACT-field-music-selection.md` | yes | **live** hardware-breakpoint capture at `003EAA7D` / `003EAAFE` / `003EAB54` + an offline replay leg |
| **EXP-093** hp-write-execution | `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md` | **no** | NATIVE-REPLAY |
| **EXP-098** battle-mode-composition-exec | `00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md` | **no** | NATIVE-REPLAY |

**EXP-093 and EXP-098 do not execute any S-42 body.** Checked against the harnesses: neither
`hp-write-execution/check.py` + `bodies.json` (64 real bodies, list read) nor
`battle-mode-composition-exec/check.py` + `bodies.json` (5 real, 0 stubbed) contains `003EAA70`, `00265270`,
`003EAB90`, `0051EDB0`, `003EAB60`, `0051ED10`, `02B5E0D0` or `02B5E0E0` (grep, case-insensitive: zero hits).
They share only the field-table predicate `00377C20` / field-index chain `003148F0`→`002EF2B0`→`002EF640`,
which no S-42 invariant mentions. The only place either id appears in either S-42 contract is the method note
at the end of field-music §13a (line 268), which cites *"EXP-093's and EXP-098's mutation tables"* as a
precedent for the patched-byte site convention — a citation of convention, not of coverage.

## Substitutions per record

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-099** (`evidence/field-music-selection-exec/check.py`) | `003EAA70` (229 B) and `00265270` (28 B) — `bodies.json` `"stubbed": []`. The two `UC_HOOK_CODE` hooks (`on_call`) only append a trace token; they do not redirect or return | **no application stub, no import bridge** (neither body reaches an IAT slot; disassembled: `003EAA70`'s only call is `003EAA78 call 00265270`; `00265270` is call-free). **Fixtures:** the table pointer `[02B5E0D0]` → synthetic `MusicTable` with **already-absolute** s32 page pointers (i.e. the post-`MC-5` state is planted, not produced); liveness byte `[02098E20]`; varblock pointer `[02098E58]` and the u16 progress at `varblock+0`. All are in scope by field-music §2/§3 (the table pointer and the progress source are named inputs) |
| **EXP-008** replay leg (`Reconstruction/Tests/Differential/diff_field_music.py`, `run_emulated`) | `003EAA70` only | **application stub `00265270`**, written as `B8 imm32 C3` (`mov eax, progress&0xFFFF; ret`). Table = the live-captured `MUS0` bytes at their captured base (live-sourced fixture) |
| **EXP-008** live leg | the running game | nothing substituted (read-only memory read of `[02B5E0D0]` and the table) |
| **EXP-009** live leg | the running game | nothing substituted (hwbp reads of `rbx` = field id, `rax` = progress at `003EAA7D`; `rax` at the `ret`s) |
| **EXP-009** replay leg | `003EAA70` | same `00265270` stub as EXP-008, fed the game's own captured progress (68, 1580) |
| EXP-093 / EXP-098 | — (other contracts) | — |

## Per invariant — field-music-selection

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| **pre** — `*(void**)02B5E0D0` non-NULL, not checked | not driven (no case plants a null table pointer; EXP-099 always writes `[02B5E0D0]=TAB`) | coverage, not exposure |
| **post** — returns `1..255` or `-1`; **no state written** | EXP-099 (return values, 22 cases) — but **EXP-099 has no write hook**, so "no write" is not measured there. The no-write half is measured only by EXP-008's replay (80/400 cases re-read table + pointer) under the `00265270` stub. Static: `003EAA70` has no non-stack store and `00265270` has no store at all (disassembled) | **no.** The stub writes nothing, and neither does the real callee (no store in its 28 bytes), so the substituted and shipped effects on memory are identical |
| **FM-a** runs ordered by `start`; `start > fieldId` ends the walk | EXP-099 `run-gap`, `start-eq-arg`, `run-second`, `run-after`, `m-start-ja`, `m-stride`; EXP-008 replay over real data | **no.** The run walk (`003EAAA5`..`003EAAD2`) reads only table bytes and `ebx` (the field id); the progress value (`r11d`, the only stub-sourced value) is not read on the walk |
| **FM-b** ladder takes the **last** threshold passed | EXP-099 `thr-eq`, `neg-progress`, `neg-prog-8000`, `m-thr-jle`, `m-movsx` — with the **real** callee | **EXP-099: no.** **EXP-008/009 replay:** the stub supplies the compared value (progress), not the comparison or its order; the stub's `mov eax, imm32` with a u16 immediate leaves the same zero-extended `eax` that the real `movzx eax, word [rax]` at `00265285` leaves, and sign handling happens in the subject (`movsx r11d, r11w` at `003EAB10`). Input-value reach only |
| **FM-c** `trackId == 0` folded to `-1` (`cmove` at `003EAB48`) | EXP-099 `zero-result`, `m-cmove` | **no** |
| composition finding (13a: dead actor / null varblock → progress 0 → `defaultTrack`) | EXP-099 `dead-actor`, `varblock-null`, real callee | not a §4 invariant. **This is exactly the behaviour EXP-008/009's stub removes** — the stub cannot model either gate |

## Per invariant — music-control-file-and-bgm-stream

The contract's own §13 reads *"**None.** No experiment executes these bodies."* Confirmed: no record above
executes `003EAB90`, `0051EDB0`, `003EAB60`, `0051ED10`, `00379D20` or any `02B5E0E0` stream code.

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| **MC-1** `02B5E0D0` bound once, one writer | not executed (static census only) | coverage, not exposure |
| **MC-2** loader reached by tail jump | not executed | coverage |
| **MC-3** loader returns before bytes arrive | not executed | coverage |
| **MC-4** six-byte sign-extending trampoline `0051EDB0` | not executed | coverage |
| **MC-5** in-place rebase, zero offsets stay zero | not executed. **EXP-099 plants the rebased (absolute) form as a fixture**, i.e. assumes MC-5's post-state. EXP-008's live read *observes* absolute page pointers in a running process (live observation of the post-state, not execution of `003EAB90`) | coverage |
| **MC-6** exactly one BGM stream (loop bound 1) | not executed | coverage |
| **MC-7** script-allocated ring clamped to file size | not executed | coverage |
| **MC-8** `0x40` / `0x7F` handed to the sound layer | not executed | coverage |

## Stale or incorrect cell text

1. **Runtime cell:** *"EXP-093/098/099 replay the selection and bgm paths with stubs"* — incorrect on three
   points: EXP-093 and EXP-098 belong to other contracts (above); EXP-099 and EXP-098 are stub-free
   (`bodies.json` `stubbed` empty / `{'stubbed': 0}`); and no record executes a bgm path (MC contract §13
   says none). The row's only disclosed application stub is `00265270` in the **replay legs of EXP-008 and
   EXP-009** (`diff_field_music.py`), which the cell does not name as stub records.
2. **Binding gap:** *"types PARTIAL"* is stale — the row's types cell reads MET (re-scored 2026-09-25,
   block-214 worklist).

## For the scorer

- **EXP-099 (the one replay record of this row's contract): exposure empty** — zero application stubs, zero
  import bridges; fixtures are the contract's own named inputs (table pointer, progress source).
- **EXP-008 / EXP-009 replay legs: one application stub, `00265270`**, which reaches only the *value* of the
  progress input to FM-b, not FM-a/FM-b/FM-c's relations, and cannot reach "writes nothing" (both stub and real
  callee are store-free). What the stub hides is the callee's two gates, which EXP-099 executes real.
- **Live evidence exists and is separate:** EXP-008 (table contents, one process, two launches) and EXP-009
  (two input conditions, game's own return 100 / 20, 126 pairs each, all via `003EAB54`). Neither is
  counted above as replay.
- **Coverage gaps, not exposure:** the pre-condition (null table) is not driven; "writes nothing" is not
  measured in EXP-099 (only in EXP-008's stubbed replay and statically); **MC-1..MC-8 have no execution at
  all** (the contract says so itself).
- EXP-093 and EXP-098 contribute nothing to S-42's contracts.
- Not read: `field_music_table.py` and `hwbp.py` internals; EXP-008's full record past line 60; EXP-099
  `result.json` per-case traces (the case list and harness were read, the result file was not re-parsed).
