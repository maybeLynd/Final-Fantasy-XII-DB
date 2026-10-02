---
system: How a manual save is committed - the eight-step slot transaction, its completion callback, and the header stamp that makes the file valid
category: 19-Save-Load-Settings
status: AUDITED
owner_layer: PrimaryOwner:Save_Load_Settings
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the slot transaction 00581DA0, its completion callback 00581B70, the two enqueue helpers 00582730 and
    005826D0, the asset-name builder 005837F0 and the storage layer's delete routine 00862130 disassembled from the
    authority image and read whole, 2026-09-19; the queue's per-kind dispatch 00582040 and the storage machine's
    command dispatch in 003BB790 read for the three kinds this transaction uses; the CRT imports resolved by name from
    the import table
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-manual-save-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  note: written by FABLE while placing one of FRONTIER's uncited bodies (00581B70). Static. CORRECTED 2026-09-20
    (FABLE, Claude Opus 5) - the short variant branches inside the state-2 arm, after the icon.sys delete has
    completed, so it skips states 3 and 4 only; the transaction's own progress totals (0x1DA full, 0x17C short) are
    an independent check, and the short-variant gate is byte [rec+0xC8] bit 0 at 00581BFD, copied from the request's
    +0x18. The mechanics of the state
    machine were already on the save-image page as a mechanical note; what the steps ARE - which file, which operation,
    in which order, and why - was not. Not read - the write worker itself, the submission descriptor, the header finaliser; the storage layer's close
    routine read for its calls only; pending first review  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-manual-save-falsification-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# How a manual save is committed

Saving from the menu is not one write. It is **a transaction of storage operations, one at a time, each started only
when the one before has reported back**, and its order is what makes a half-written save recognisable: the file's header
is cleared first and stamped last.

## 1. The pieces

- **The transaction record** - the object `00581DA0` works on. `+0xCC` state (1-8), `+0xCD` slot, `+0xCE` a step counter,
  `+0xC8` flags (bit 0 = the short variant), `+0xD8` the image checksum, `+0xDC` the progress total.
- **The storage queue** `02CA99C0` - packets of a *kind* and arguments. The queue starts its front packet through
  00582040, a thirteen-way switch; the three kinds used here:

  | kind | queued by | starts | the storage machine then runs |
  |---:|---|---|---|
  | 7 | `00582730(path, buffer, size)` (94 B) | a **write** of `size` bytes (storage command 2, the write worker) | *the analysis name of `00582730` says "read"; the command it selects is the writer's* |
  | 8 | the transaction itself | a **write** of the whole image, `0x56690` bytes from the live image | the same worker |
  | 0xB | `005826D0(path)` (83 B) | storage command 7: **delete the file if it exists** | `00862130` (167 B): `_wfopen_s(path, "rb")`; on success `fclose`, then `_wremove` |

- **The three file names**, from `005837F0(kind, slot)` (304 B): kind 0 → `icon.sys`; kind 1 → the base prefix plus the
  slot as three digits - **the slot's data file**; kinds 2, 3, 4 → `static.ico`.
- **The progress gauge.** Every step adds a weight to `+0xDC` and reports the total through 00581860, which scales it
  by ten and moves the save screen's gauge target toward it. *The save-image page's note calls these "result codes";
  they are progress weights.*

## 2. The eight steps - `00581DA0` (640 B) and `00581B70` (514 B)

`00581DA0(record, state)` performs one step and records the state; the completion callback `00581B70(operation kind,
error, record)` - registered when the transaction is set up - checks that the operation that finished is the one the
current state was waiting for, and starts the next.

| state | what it queues | file | weight | waits for |
|---:|---|---|---|---|
| 1 | clears the image's first 8 bytes in memory, then writes those **8 zero bytes** (kind 7) | the data file | `0x10` (`0x50` short) | kind 7 |
| 2 | delete (kind 0xB) | `icon.sys` | `0x10` (`0x14` short) | 0xB |
| 3 | delete | the data file | `0x10` | 0xB |
| 4 | delete | `static.ico` | `0x10` | 0xB |
| 7 | builds the submission descriptor, finalises the header and checksum (kept at `+0xD8`), then **writes the whole image** (kind 8) | the data file, inside the slot's directory | `0x168` (`0xE6` short) | kind 8 |
| 8 | puts **`{checksum, 1}`** in the image's first 8 bytes and writes those 8 bytes (kind 7) | the data file | `0x32` | kind 7 |

**The order after each completion:** 1 → 2; 2 → 3, or **straight to 7 in the short variant**; 3 → 4 with the counter
cleared; 4 → 7; 7 → 8; 8 → done. States 5 and 6 share state 4's arm in both tables but are unreachable: the callback
increments the counter and then asks whether it is at least 1, which it always is.

**Where the short variant branches, corrected 2026-09-20.** The branch is taken **inside the state-2 arm, on that
state's own completion** - `00581BE5` accepts kind `0xB`, and only then `00581BFD test byte ptr [rbx + 0xC8], 1`
chooses `mov dl, 7` (`00581C06`) over `mov dl, 3` (`00581C20`). The callback is entered *because* `icon.sys` has
already been deleted, so **the short variant deletes `icon.sys` too**; what it skips is states 3 and 4 - the data
file and `static.ico`. Its four operations are states **1, 2, 7, 8**.
*This supersedes the earlier clause "which keeps the old `icon.sys` and `static.ico`": only `static.ico` is kept.*

**The transaction's own arithmetic says the same thing, and it was already in the table above.** `005819F0` sets the
gauge total from the variant before the first step - `00581AF0 test byte ptr [rdi + 0xC8], 1` / `mov ecx, 0x17C` /
`mov eax, 0x1DA` / `cmove ecx, eax`, so **full = `0x1DA`, short = `0x17C`** (the gauge target is that minus `0x19`).
The full total is the six full weights, `0x10 + 0x10 + 0x10 + 0x10 + 0x168 + 0x32 = 0x1DA`. The short total is the
four short weights **including state 2's** - `0x50 + 0x14 + 0xE6 + 0x32 = 0x17C`. A short variant that skipped state 2
would total `0x168`. This is an independent check: the weights were read from `00581DA0` per state, the totals from a
different function, and they agree only on the corrected order.

**The short-variant flag is not the save system's own.** `005819F0` copies it in from the request: `00581AB7
mov eax, dword ptr [rbx + 0x18]` / `and eax, 1` / `00581AC4 mov dword ptr [rdi + 0xC8], eax`, where `rbx` is the
message payload at `[rdx + 8]`. So bit 0 of the requesting message's `+0x18` decides the variant, and the record's
`+0xC8` is a copy of it. *Who posts that message, and on what, is still not read.*

*The `cmp dl, 1` at `00581C94` is not this gate.* It is in the **state-4** arm, on the counter at `+0xCE` that the
state-3 arm cleared, and it is what makes states 5 and 6 unreachable. (The 2026-09-19 shadow audit of this page
recorded it as the short-variant gate while stating that the per-state transitions were not re-derived; the ACCEPT
stands for what it audited - the dispatch shape, the kind routing and the 5/6 claim - and this note corrects the
by-the-way attribution.)

**Any error, at any state,** ends the transaction the same way as success: message `0x1D` with payload `0xF` - the slot
byte and the error code - goes to the controller, the record is released, and on an error the record's `+0xD4` is copied
into the live image's `+0x50` and bit 2 is raised in the save controller's flags. *What the controller does with that
message is on [the storage read completion contract](CONTRACT-storage-read-completion.md) (its `0x1D` / `0xF` arm).*

## 3. Why this order

- **The header is the commit stamp.** The image's first dword is its checksum and the second is 1 only on a finished
  save; the first thing the transaction does is zero both - in memory and on disk - and the last thing is to write them.
  A save interrupted anywhere between has a data file whose ~~first 8 bytes are zero~~ decoded image's first 8 bytes are zero (the file itself opens with the `SAFH` container header) *(corrected 2026-10-02, OPUS: every write-mode close builds the container — `0086623F`, `'SAFH'` at `008663BD`, the 12-byte header `fwrite` at `008663FB`; CONTRACT-save-container-transform.md)*, or no data file at all.
- **The old save is removed before the new one is written**, but not equally in the two variants: **`icon.sys` goes in
  both** (state 2 runs either way), while **the data file and `static.ico` go only in the full variant** (states 3 and
  4). So in a full save the slot holds nothing between step 3 and step 7; in a short save the old data file survives
  until step 7 writes over it, and only the header zeroed by step 1 marks it as incomplete meanwhile.
- **Step 8 patches, it does not replace (read 2026-09-19).** The storage layer under the write worker never writes a file
  in place. *Open* (`008666B0`, 833 B) always tries `_wfopen_s "rb"` first and, if the file exists, **reads all of it
  into a byte vector** (`01F44D40`); in write mode a missing file is simply an empty vector. *Write* (`00866AD0`, 176 B)
  touches no file: it overwrites the vector's bytes at the record's cursor and appends past its end. *Close* (`00866200`,
  1,195 B) ~~writes the whole vector to a file~~ deflates the whole vector (`compress2`, level 9), RC4-encrypts it behind a 12-byte `SAFH` header and writes that to a file *(corrected 2026-10-02, OPUS: mode 0 takes the container path at `0086623F`, `'SAFH'` at `008663BD`, `rand` rotation at `008663C5`–`008663ED`, header `fwrite` at `008663FB`; CONTRACT-save-container-transform.md)* under `GetTempPathW` (`"wb"`), copies it over the target with `CopyFileW`,
  and removes the temporary. So the 8-byte header write loads the image step 7 wrote, replaces its first 8 bytes in
  memory, and rewrites the file - and every file written through this storage layer is replaced by a copy of a completed
  temporary, never written through. *`00866200` was read for its calls, not whole.*

## 4. What a reimplementation must keep

- Six operations in this order for a full save - states 1, 2, 3, 4, 7, 8 - and four for the short variant - states
  **1, 2, 7, 8** - never overlapping. The short variant is not "no deletes": it still deletes `icon.sys`.
- Header `{0, 0}` on disk before anything is deleted; `{checksum, 1}` only after the image write has completed.
- A failure at any step reports once, with the slot and the error, and leaves whatever is on disk as it is.

**Not read:** the write worker 003BAEB0 beyond its command number and the three storage-layer routines it reaches; the
submission descriptor and the header finaliser; **what posts the request whose `+0x18` bit 0 sets the short-variant
flag** (the copy into the record is read, the sender is not); ~~what re-creates `icon.sys` and `static.ico` - which a
short save also needs, since it deletes `icon.sys` without skipping that step~~. *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5),
`FR-2`: nothing re-creates them on PC. The transaction deletes them, and the `icon.sys` image it builds is never
submitted; see [the shipped formats page](../02-Resource-And-Asset-Pipeline/Standard-Formats/shipped-standard-formats.md) §7.)*

## Evidence

| body | interior anchors |
|---|---|
| `00581DA0` slot transaction (640 B) | `00581DCA`, `00581DD2`, `00581DFA`, `00581E0E`, `00581E1C`, `00581E2D`, `00581E32`, `00581E55`, `00581E5D`, `00581E8F`, `00581E9E`, `00581ED2`, `00581EE7`, `00581EF8`, `00581F2F`, `00581F51`, `00581F89`, `00581F8E`, `00581FA8`, `00581FBA`, `00581FD9`, `00581FE3`, `00581FEF`, `00581FF4` |
| `00581B70` completion callback (514 B) | `00581B8B`, `00581BA6`, `00581BB3`, `00581BCD`, `00581BE5`, `00581BFD`, `00581C06`, `00581C20`, `00581C4F`, `00581C81`, `00581C97`, `00581CB8`, `00581CE7`, `00581CEC`, `00581D04`, `00581D19`, `00581D25`, `00581D3A`, `00581D52`, `00581D5A` |
| `005837F0` asset name (304 B) | `00583830`, `0058383C`, `00583850`, `00583857`, `00583898`, `005838A4`, `005838AB`, `005838B2` |
| `00862130` delete if present (167 B) | `0086217D`, `00862182`, `0086219C`, `008621AB`, `008621B6` |
| `008666B0` open: load the whole file (833 B) | `008666C0`, `008666E5`, `008666F2`, `00866716`, `00866755`, `00866760`, `008667A2`, `008667AD` |
| `00866AD0` write into the vector (176 B) | `00866B00`, `00866B10`, `00866B1C`, `00866B31`, `00866B40`, `00866B4E`, `00866B53` |

Under 128 bytes, read whole: `00582730`, `005826D0`. Read in part, and for that reason written without code marks so
that they earn no citation credit here: 00582040 (the queue's switch, jump table
0058220C: kind 7 → 003BB920, kind 8 → 003BB9B0, kind 0xB → 003BB2F0), 003BB790 (the storage machine's command
dispatch 003BB803..003BB8B7: command 2 → the write worker, command 7 → 003BA5F0, which calls `00862130`),
00581860 (the gauge). Imports resolved from the import table: `008C2E00` `_wfopen_s`, `008C2F00` `fclose`,
`008C2B08` `_wremove`. Strings: `icon.sys` at `00D23EC8`, `static.ico` at `00D23ED8`, `%s%03d` at `009153E4`.

## Cross-subsystem neighbours

**Resource - SERVICE.** The storage command machine and its handlers (003BB790, 003BB920, 003BB9B0, 003BB2F0,
003BA5F0) are filed under the Resource layer
([the resource request queue](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) names the machine). This
page reads them only for which command each queue kind selects.

**CoreRuntimeScheduling - SERVICE.** The write worker this page names but does not read, 003BAEB0, calls the
nine-byte getter 0017D270 at 003BB097, which returns the double at `01F7F4B0` and is filed under the core runtime's
scheduling layer. What the double holds was not established and nothing on this page depends on it; the edge is
recorded because naming the worker imports it.

**UI - CLIENT.** The transaction reports through the save controller's message path, which the save screen's widgets
observe; described by role.

## SWE2-EC7-113 update (2026-09-21) - `00862620` measured

`00862620` (60 B) is the
`02EAF8E0` global update
`003BAEB0` runs: on
`ecx == 0` it calls
`00866AD0` on the
`02EAF8E8` object, scales
the result by `ebx`, and
stores the product to the
global; on `ecx != 0` the
global is set to `-4`
instead. Both arms return
zero - success flag and
scaled value share one
field.
Interior anchor `0086263C`
(the product store).

*(CORRECTED 2026-09-29, OPUS, CON-191: `00582730` is not a diagnostic sink. It is the storage queue's kind-7 write
enqueue of section 1; `02CA99C0` is the storage queue, and `rdx` / `r8d` are the buffer and the size - the transaction
passes the image and 8 - not a slot/error pair. The original sentence follows, struck.)* ~~`00582730` (94 B) is the gated diagnostic sink `00581DA0` invokes during the slot transaction: when global `02CA99C0` is null it returns silently; otherwise it `strcpy`-loops `rcx` into a stack record `{7, str, rdx, r8d}` at `[rsp+0x20]` and calls `00582540(r10, &rec)` — the global is the sink object, `7` a fixed message class, and `rdx`/`r8d` the transaction's slot/error pair.~~

Interior anchor `00582781` (function `00582730`).

*(CORRECTED 2026-09-29, OPUS, CON-191: the kind-`0x0B` delete enqueue of section 1, not a string event.)*
~~`005826D0` (83 B) is the second `02CA99C0`-gated sink `00581DA0` invokes: identical `strcpy`-into-stack-record shape to `00582730` but message class `0x0B` and no extra payload slots — a plain string event into `00582540`, silent when the sink global is null.~~

Interior anchor `00582716` (function `005826D0`).

`003BA990` (756 B) is a command arm the storage machine `003BB790` dispatches to (with uncited `003BB4C0`): `00861EC0`, `005C5230`, `008621E0`, `003BA320`, `008624D0`, `008625D0`, `00862590`, `008620E0` and `003BA3E0` run the commit step - the save transaction's `0086xxxx`-heavy arm.

Interior anchor `003BA9F6` (function `003BA990`).

`003BA3E0` (520 B) is the budget accountant the manual-save commit arm `003BA990` calls (the request-queue's storage-read handlers run it too): SSE-parallel sum over the `02B40610` record band (stride 0x40) of `(x+0x3FF)>>10` page counts, subtracted from the `02B40544` total and added into `[rdi]` clamped at zero - the queue's remaining-capacity tally, call-free.

Interior anchor `003BA488` (function `003BA3E0`).

`003BA320` (181 B) is the name matcher the manual-save commit arm `003BA990` calls (the request-queue's storage-read handlers run it too): counts non-`/`/`*` characters in `02B4055C` against the argument string, then digit-suffix compares through two CRT string calls - the queue's path-key compare.

Interior anchor `003BA3B2` (function `003BA320`).

`003BB4C0` (309 B) is the snapshot publish `00582040` calls: the `[rcx]` name copies byte-wise to `02B4055C`, `02B40550` resets to `-1`, `02B40554`/`02B40E28`/`02B40EC8` clear, `[rcx+8]`/`[rcx+0x10]` store into `02B40EF0`/`02B40EF8` with `02B40EFC`/`02B40FE0` zeroed, then a `movups` loop copies `rax` x 0x80 bytes of the source record into `02B40FF0` - the save queue's per-kind record stage the thirteen-way dispatch selects.

Interior anchor `003BB5E6` (function `003BB4C0`).

## Falsification pass 1 — 2026-09-29 (OPUS): the page's sections survive; the appended EC7-113 reading of the two enqueue helpers refuted (CON-191); a consumer's state numbers corrected (CON-192)

**Attack.** Sections 1 and 2 were turned into checks at their instructions, together with the appended notes. The
competing case came from inside the page: the SWE2-EC7-113 note calls `00582730` and `005826D0` "gated diagnostic
sinks" whose `rdx` / `r8d` are "the transaction's slot/error pair", while section 1 calls them queue helpers for a
write and a delete. Script: `Tools/analysis-kit/gfz-scripts/falsify_manual_save.py`, output
`falsify_manual_save.out`, image `73461d08…`, 0 BROKEN after the correction, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| M0 | sizes | **survives**: all six |
| M1 | section 1 against the EC7-113 note | **section 1 survives; the note is REFUTED (CON-191).** Both helpers build a stack packet `{kind, path, …}` and hand it to the storage queue's enqueue `00582540` when the queue `02CA99C0` exists. `00582730` is kind 7 with `(rdx, r8d)` = (buffer, size): both of its calls in the transaction pass the image and 8. `005826D0` is kind `0x0B` with the path alone |
| M2 | section 1's file names | **survives**: `icon.sys`, `static.ico`, `%s%03d`. State 2 deletes kind 0, state 3 kind 1 |
| M3 | section 2's weights and totals | **survives**. Each state's weight, read from `00581DA0`, sums to `005819F0`'s totals: full `0x1DA`, short `0x17C`, the short over states 1, 2, 7 and 8 |
| M4 | section 2: where the short variant branches | **survives**: inside state 2's completion (`00581BE5`, `00581BFD`), on the request's `+0x18` bit 0 |
| M5 | section 2: states 7 and 8 | **survives**: `0x56690` bytes, then `{checksum, 1}` |
| M6 | section 1: delete if present | **survives**: `_wfopen_s` in mode `rb`, then `fclose`, then `_wremove` |
| M7 | a consumer: the save-image page's arm list | **REFUTED there (CON-192).** The table at `00582020` sends states 4, 5 and 6 to one arm, 7 to the submission and 8 to the stamp, as section 2 of this page says. The save-image page had numbered them 5 and 7 |
