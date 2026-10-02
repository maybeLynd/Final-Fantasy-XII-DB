---
contract: Load the music-control table (one writer; how often it is bound is not established, MC-1) and rebase it in place, and run the one script BGM stream
category: 18-Audio
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 18-Audio/the-music-control-file-and-the-bgm-stream.md
entries: ["003EAB90", "0051EDB0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's two load-bearing invariants
    **read from the shipping bytes rather than carried** — the callback trampoline disassembled in
    full (six bytes) and the rebase loop read to its zero test, which is the fact `MC-5`'s second
    half turns on. **This records checks performed on that date, not the method of the original
    derivation**, which is on the music page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-music-control-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the music control file and the BGM stream

> **Authored 2026-09-22 by FABLE.** S-42's contract column carries one contract over two pages, and
> it implements the other one. **This takes the music-control/BGM page, so both of S-42's pages now
> carry a contract.**
>
> Written against FRONTIER's adequacy test. **`MC-3` and `MC-5` are a pair:** the loader hands back
> a block *before its bytes exist*, and a later callback rewrites that block's header in place — so
> the table's validity is a function of two operations separated by a queue, which neither can
> state.

## 1. Purpose

Get the music-control table into memory for the life of the process, and stream one script-chosen
BGM.

## 2. Interface

| | body | note |
|---|---|---|
| **the rebase** | `003EAB90`, 71 B | the completion callback; runs once, when the bytes are in |
| **the trampoline** | `0051EDB0`, **6 B** | `movsxd rax, ecx` / `jmp rax` — how the real callback is reached (`MC-4`) |

## 3. Types

```
02B5E0D0   u8*   the music-control table -- ONE writer in the image (MC-1)
  +0x04  u32   maxFieldId
  +0x08  u32[] page offsets -- FILE-relative before the rebase, ABSOLUTE after (MC-5)

02B5E0E0   BgmStream, 0x38 B, and there is exactly one (MC-6)
  +0x00  i32   requestId, -1 idle        +0x24  i32  fileBytes
  +0x08  u8*   script-allocated ring     +0x28  i32  bytesRead
  +0x10  i32   bufferBytes               +0x2C  i32  ringCursor
  +0x1C  i32   kind, always 0x24         +0x30  u8   state 1..8
  +0x32  u8    0x40   \  handed to the sound layer at play (MC-8)
  +0x33  u8    0x7F   /
```

## 4. Preconditions · postconditions · invariants

### The eight cross-operation invariants

**MC-1 — ~~The table is bound ONCE PER PROCESS and never rebound or freed.~~ The table has ONE WRITER, and the binder has no guard.** `02B5E0D0` has **exactly
one writer** image-wide. ~~*Its lifetime is the process, so nothing needs to re-read it and nothing
may assume it can be replaced.*~~

> *Qualified 2026-09-27 (OPUS, on ASTRA's musicctrl-binding-provenance).* One writer instruction is not an invocation count. The binder `003EAB60` passes kind 9, index `0x20` and the callback `003EAB90` to `0051ED10`, then stores the returned `rax` at `003EAB78` without loading or testing the old pointer. Its only route is the application's init job:
> `GameApplication` vtable `008C5760` slot 3 (`0017CF30`) builds a job `{0017D150, this}` and queues it (`00199F10` / `0019A000`); the job runs `0017D000` → `0017D4C0` → `0022A0B0` → `00379D20`, which tail-jumps `003EAB60` (`00379D32`).
> `0017D000`'s ready byte `+0x113C` is stored and never read by it, so it is no one-shot guard. **How often the framework dispatches slot 3, and whether heap 5 is ever released or reset, are NOT established**, so "once per process" and "never freed" are not claimed. The field-selection contract's lifetime row (`UNKNOWN / NOT EXERCISED`) is the current statement. Evidence: `_experiments/evidence/musicctrl-binding-provenance/` (ASTRA; three artifact-corruption controls) and the `0017CF30` / `0017D150` job route re-read by OPUS.

**MC-2 — Its loader is reached by a TAIL JUMP, which is why a call-site scan finds none.** The boot
body ends `jmp` into the music loader rather than calling it — the page records this as `DG-5`.
*An "is this ever invoked?" answer built from `call` sites alone says no, and is wrong.*

**MC-3 — The loader returns the block BEFORE the bytes arrive.** It sizes the file, allocates from
heap 5, queues the read and **hands the pointer back immediately**. *So a returned pointer is not a
loaded table, and every consumer is downstream of a queue completion it cannot see.*

**MC-4 — The real callback is carried as a SIGN-EXTENDED 32-BIT POINTER, and that is only sound
because the image never relocates.** The descriptor's `+8` "arg" word holds the callback; the slot's
`onDone` is `0051EDB0`, whose entire body is **`movsxd rax, ecx` / `jmp rax`** — six bytes,
disassembled in full.

> ***A function pointer is being round-tripped through a 32-bit field and sign-extended back.*** That
> works because the image is loaded at `0x120000` and stays there. **A reimplementation on a
> relocatable or high-address image must widen that field or the jump target is garbage** — and
> nothing in the descriptor declares it as a pointer, so a port has no reason to notice.

**MC-5 — The completion callback REBASES the page offsets IN PLACE, with a 32-bit add — and a zero
offset stays zero.** `003EAB90` computes the page count from `maxFieldId` by a signed
divide-by-128, then walks the header adding the table's own address to each non-zero entry
(`003EABBA test ecx, ecx` / `je` skips). **After it runs the header holds absolute addresses**, which
is exactly how the reader consumes them.

> **The page count, exactly, and the one field id it misses** *(qualified 2026-09-27 (OPUS, on ASTRA's musicctrl-page-boundary))*. The count is
> `(maxFieldId + 127) / 128` with a signed, biased divide: `003EAB9A mov eax, [r8+4]` / `003EAB9E add eax, 0x7F` /
> `cdq` / `and edx, 0x7F` / `add` / `003EABA7 sar eax, 7`, and `003EABAF jle` visits nothing when that is 0. The reader
> (`CONTRACT-field-music-selection.md` §3) admits `fieldId == maxFieldId` (`003EAA8C jl` rejects only `maxFieldId < fieldId`)
> and selects page `fieldId / 128`. The two agree except when `maxFieldId` is a positive multiple of 128: then the reader's
> page `maxFieldId / 128` is one past the visited set, so that final page word is never rebased - a non-zero word there
> is consumed as an absolute address though it is still file-relative, and a zero word returns `-1`. (At `maxFieldId = 0`
> nothing is visited and the reader's page 0 is unrebased too.) **So "after it runs the header holds absolute addresses"
> holds for the visited pages, `(maxFieldId + 127) / 128` of them, not for every slot the reader can select.** The
> shipped table (`maxFieldId` 1311, 11 pages) is not at the seam, and no fault or invalid shipped table is claimed. A
> modder raising the maximum to a multiple of 128 must leave that final page word zero, or raise the maximum by one.
> Regression: `_experiments/evidence/musicctrl-page-boundary/check.py` (ASTRA; five corrupted-derivation controls).
> EXP-099 plants every page absolute and excludes the loader, so its reader results do not test this producer seam.

> *Two consequences, both a modder's and a porter's:* **the block must live below 2 GB** for the
> reader's sign-extension to land — heap 5 is where the whole-file loader puts every such table —
> and **a page offset of 0 stays 0**, which the reader reads as "no page". *The rebase is therefore
> not idempotent in general but is safe against zero, and running it twice would double every real
> offset.*

**MC-6 — There is exactly ONE BGM stream, and the code says so in an odd way.** The checker is
written as a loop over a `0x38`-stride array **bounded to one iteration**. *So the singular is a
property of a bound, not of the data layout — a port that reads the loop as an array and raises the
bound gets a second stream the rest of the system does not expect.*

**MC-7 — The stream's buffer is SCRIPT-allocated, and the ring is shrunk to the file when the file
is smaller.** `+0x08` comes from the `usebgmstream` verb; `+0x10` is reduced to `fileBytes` in that
case. *So the ring size is authored data clamped by the asset, and `ringCursor` is `bytesRead mod
bufferBytes` against the clamped value.*

**MC-8 — The pair handed to the sound layer at play is `0x40` and `0x7F`** — the two literals
[the sound-request path](Audio-Boundary/CONTRACT-sound-request.md) documents as centre pan and full
scale in a 0–127 field. *Cited as the same literals in the same role, not re-derived here; what a
listener hears is that contract's refusal to say.*

## 5. State

**Owned:** the two globals and the `0x38`-byte descriptor. **Not owned:** the ring buffer, which the
script allocates, and the heap-5 block, ~~which is never freed (`MC-1`)~~ whose release or reset is not established (`MC-1`, qualified 2026-09-27).

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-field-music-selection.md`](CONTRACT-field-music-selection.md) — S-42's other page |
| **Delivered by** | the resource request queue — `MC-3`'s completion is that subsystem's |
| **Plays through** | [`CONTRACT-sound-request.md`](Audio-Boundary/CONTRACT-sound-request.md) — `MC-8` |

## 7. State transitions

*boot → tail-jump into the loader → size, allocate, queue, return the block → (later) delivery →
trampoline → rebase in place → the table is usable.* The stream: *idle (`requestId = −1`) → the verb
supplies a ring → read, play, advance `ringCursor` → state `1…8`.*

## 8. Script · resource · event interactions

`usebgmstream` supplies the ring buffer and the file index; the table and the stream file both
arrive through the resource queue. The table's path is the kind-9 array's entry 32.

## 9. Determinism

Deterministic. No generator is drawn. **Delivery ORDER is not guaranteed by this contract** — the
queue decides when `MC-3`'s gap closes.

## 10. Failure paths and edge conditions

- A consumer that reads the table before delivery sees unrebased, file-relative offsets (`MC-3`,
  `MC-5`).
- A page offset of 0 survives the rebase and reads as "no page" (`MC-5`).
- A block above 2 GB breaks the reader's sign-extension (`MC-5`) and the callback trampoline
  (`MC-4`). **Measured** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 325, which executed it; its package was read.)*: at `0x90000000` the rebase stores `90000034`, and the reader's `movsxd`
  sign-extends it and faults. At `0x200100000` the 32-bit add keeps only the low half, `00100034`, and the reader
  faults there too. Over the shipped `musicctrl.bin` the rebase touches **11 page words**.

## 11. Observable behaviour

The music that plays when you enter an area, and the streamed track a script can start directly.

## 12. Reproduction formula

Assert `02B5E0D0` has exactly one writer image-wide (`MC-1`). Disassemble `0051EDB0` and assert it
is **six bytes**, `movsxd` then `jmp` (`MC-4`). Run the rebase twice on a table with a zero page
offset and assert the zero is unchanged while a non-zero entry has doubled (`MC-5`). Raise the
checker's loop bound and assert a second descriptor is reached (`MC-6`).

## 13. Runtime validation

~~**None.** No experiment executes these bodies. S-42's runtime cell is not addressed by this
contract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*~~ **Superseded** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 325, which executed it; its package was read.)*. [OPUS block 325](../_index/candidates/s42-opus-replay-music-control/README.md) ran the loader, the rebase, the reader and the stream machine
as shipped code over the shipped `musicctrl.bin`. The evidence class is native replay, not live. MC-5's zero-skip,
its doubling on a second run and its address limits are measured there.

## 14. Unresolved

- What the stream's eight states mean individually. `MC-7` establishes the fields they drive.
- Whether any consumer of the table runs before the rebase in practice, which `MC-3` makes possible
  but does not demonstrate.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `MC-4` — the sign-extended callback | `0051EDB0` disassembled in full: two instructions, six bytes | 1 |
| `MC-5` — the in-place rebase and the zero skip | `003EAB90` read from its table load through the page-count arithmetic to the `test ecx, ecx` / `je` | 1 |
| `MC-1`, `MC-2`, `MC-3`, `MC-6`, `MC-7` | [the music page](the-music-control-file-and-the-bgm-stream.md) §§2–3, falsified 2026-09-13 | 1 |
| `MC-8` | [the sound-request contract](Audio-Boundary/CONTRACT-sound-request.md) for what the two literals are | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `MC-1` through `MC-8`. **`MC-4` is the one that
cannot survive a port unexamined** — a 64-bit function pointer stored in a 32-bit field is invisible
until the address is high. **`MC-5` is the one a port makes idempotent** and thereby changes, since
the original doubles real offsets on a second run. **`MC-6` is the one a port generalises**, reading
a bounded loop as an array.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Audio — internal.** The table, the stream descriptor and the rebase are this category's own.
- **Resource — SERVICE, and `MC-3` is the statement.** The whole-file loader, the queue and the
  file-size table belong to that layer. **This contract asserts only that the block is returned
  before delivery and that the done callback reaches the trampoline**, both visible at this side, and
  nothing about how the queue schedules.
- **Script_VM_Native_Bridge — CLIENT, through `MC-7`.** The `usebgmstream` verb supplies the ring
  buffer; *the verb itself is not read here.*
- **Every other layer reached is MECHANICAL**, through these two bodies' own callees. *Only the
  rebase and the six-byte trampoline are cited by address — the two `MC-4` and `MC-5` rest on; the
  loader, the queue bodies and the sound-layer entries are named, not cited.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Audio", "resource" and "script" would otherwise each
> be cleared by the word alone.*

## 17. Related

- [The music control file and the BGM stream](the-music-control-file-and-the-bgm-stream.md) — the mechanism
- [Contract — field music selection](CONTRACT-field-music-selection.md) — S-42's other page
- [Contract — the sound request](Audio-Boundary/CONTRACT-sound-request.md) — `MC-8`

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives, as qualified on 2026-09-27

**Attack.** §2, MC-1 (as qualified), MC-2, MC-4 to MC-8 and §3's stream fields became checks at their instructions.
MC-1's writer census ran on both instruments. Script: `Tools/analysis-kit/gfz-scripts/falsify_music_control.py`, output
`falsify_music_control.out`, image `73461d08…`, 0 BROKEN, exit 0. MC-3 is the resource queue's behaviour and is carried.
The 2026-09-27 page-boundary qualification rests on ASTRA's own check.

| # | Clause attacked | Result |
|---|---|---|
| M0 | §2, MC-4 | **survives**: 71 B; the trampoline is exactly `movsxd rax, ecx` / `jmp rax` |
| M1 | MC-1 as qualified | **survives**: one store to `02B5E0D0` on both instruments; the binder passes `(9, 0x20, 003EAB90)` and never reads the old pointer |
| M2 | MC-2 | **survives**: no call site; the one edge is the tail-jump at `00379D32` |
| M3 | MC-5 | **survives**: the biased divide by 128, the `jle` on zero, the zero-word skip, and the 32-bit add in place |
| M4 | MC-6 | **survives**: stride `0x38`, bound `cmp ecx, 1`, over byte `+0x31` |
| M5 | MC-7 | **survives**: the file size is stored to `+0x24`, a `jge` guards the store to `+0x10`, and the cursor is `idiv [rbx + 0x10]` |
| M6 | MC-8, §3 | **survives**: requestId -1; `+0x32 = 0x40` (via a word at `+0x31`); `+0x33 = 0x7F`; kind `0x24` at `+0x1C` |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity — OUT-OF-SCOPE (1 edge).** The boot body `0022A0B0` calls `BattleStorage_InitializeWorkArrays` `002368D0`. This contract cites `0022A0B0` only as one link of the init job that reaches the musicctrl binder; setting up the battle work arrays is another step of the same boot body.

**CoreRuntimeScheduling — CLIENT and OUT-OF-SCOPE (8 edges).** The job chain is itself scheduling code: `0017D000` calls `0017D4C0`, which calls `0022A0B0`, `001A14E0` and `001DB500`; `0022A0B0` calls `0022BDF0` and `00379D20`. The musicctrl binding rides the application's init job (`0017CF30` queues it, and it runs `0017D000` → `0017D4C0` → `0022A0B0` → `00379D20`); the other calls on those bodies are the rest of process start-up and carry no audio meaning.

**Input — OUT-OF-SCOPE (2 edges).** `0017D4C0` calls `InputManager_CreateSingleton` `00198750`, and `0022A0B0` calls `0035B270`. The same init job creates the input manager; that is start-up order, not a link between the input layer and the BGM stream.

**Presentation — OUT-OF-SCOPE (3 edges).** `0017CF30` calls `0018D850`, and `0022A0B0` calls `AddMotion_LoadSkeletonMapping` `0036FFF0` and `AddMotion_LoadHighModelReplace` `0037CCC0`. The application's slot 3 and the boot body also load presentation tables; they share the init job with the music binding and nothing else.

**RNG_Random_Selection — OUT-OF-SCOPE (1 edge).** `0022A0B0` calls `RNG_MT19937_Seed` `00379CF0`, a 5-byte jump into the generator's seed routine. The boot body seeds the gameplay generator; the musicctrl path draws nothing from it.

**Resource — SERVICE (17 edges).** `00379D20` calls `003EAC40` and `00473D20` and tail-jumps to the binder `003EAB60`; each of the three calls `0051ED10` with a loader kind of 9 and an index (`0x1F`, `0x21` and the musicctrl `0x20`) and stores the returned pointer, and `0051ED10` calls `0032E400` and `0032E620`; `0017D4C0` also calls `001A11B0` and `001DB1E0`, and `0022A0B0` calls `00259DF0`, `002DF9A0`, `0032EAE0` (which zeroes one global qword) and `00379E90`. The musicctrl file is bound as one of three kind-9 loader slots through the resource layer's registration (`0051ED10`), so its delivery is a resource service; the boot body's other resource calls are separate start-up work.

**Save_Load_Settings — OUT-OF-SCOPE (3 edges).** `0017D4C0` calls `SaveloadManager_RefreshDisableAutosaveList` `001C1710`, `SaveloadManager_EnsureSingleton` `001C18A0` and `SaveloadManager_GetSingleton` `001C18E0`. The init job also sets up the save manager; it shares the job with the music binding and is unrelated to it.

**World — OUT-OF-SCOPE (1 edge).** `0022A0B0` calls `00266D10`. One more start-up step of the boot body, outside the binding chain this contract cites the body for.
