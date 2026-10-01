# SWE2-AUDIT-SEM review: SWE2-DATA's DD owner read, batch 4 (six Presentation, World, Platform and CRT pages, SD-140, SD-141, SD-160..SD-169), 2026-09-30

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-DD-OWNER-READ-4-0930` (T1, no status raised) |
| reviewed | `4415dba48` (author **SWE2-DATA**): [`dd-data-4-0930/README.md`](../dd-data-4-0930/README.md), the six pages' diffs, the register section "SD (batch 4)" |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` (checked by `dd4_sem.py`) |
| **verdict** | **ACCEPT-WITH-CORRECTIONS.** The four readings the request names hold on the bytes: `_set_new_mode(0)` is called once, `NameEquals` compares 32 bytes and hits on a mismatch, the count is 44, and `0026D910` stores four globals. Every strike quotes real old text, and the reconciliations agree with their rows. The register section is malformed, though: SD-160..SD-169 are each registered twice, with different wording. One "five globals" line survives on the environment page. Five SD rows state limits the parent database or a short read already closes or narrows: SD-161, SD-163, SD-164, SD-166 and SD-167. SD-160 overstates what its answer would decide. |

All evidence here is static: the image bytes, and the register, pages and candidate records as git blobs at `4415dba48^`,
`4415dba48` and HEAD. Nothing was executed. The cross-references in [`dd4_sem.py`](dd4_sem.py) ([out](dd4_sem.out),
`FAILS 0`) come from `retool.scan()`, OPUS's rip/call index. They are a second implementation, independent of the
producer's `pe.raw_rip_refs`.

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

The six scripts are `fx54_consumers`, `frp_checks`, `rrp_checks`, `pf_env_checks`, `pf_steam_checks` and `pf_mem_checks`.
Each exits 0 with `FAILS 0`, and each output is identical to its committed `.out`
([`producer_rerun.out`](producer_rerun.out)). The run pin `f55dd3c9a` is an ancestor of `4415dba48`. The runs wrote
nothing into the tree.

## 2. Questions 1 and 2: strikes and the named readings (SWE2-AUDIT-SEM)

[`strike_check.py`](strike_check.py), [out](strike_check.out): **66 new struck spans over the six pages, all 66 found
verbatim in the parent.**

Re-derived independently (`dd4_sem.py`):
- **`_set_new_mode` (M1).** The import slot `008C2B78` has one reference, the thunk `00862046`. The thunk's only caller
  is `00808D5C`'s tail `jmp`. `00808D5C` calls `00809B44`, which is `lea rcx, handler` followed by
  `jmp [SetUnhandledExceptionFilter]`. It then calls `005C5230` (`xor eax, eax / ret`) and passes that 0 in `ecx`.
  `008C31D0` is a null qword whose address the startup body `00808D78` loads (`lea` at `00808DF5`). `008C31D8` holds
  `00808D5C`, so it is the first initializer. The page's correction holds.
  - *Suggested addition, not a defect.* This is the shape of MSVC's stock `pre_cpp_initialization`: it sets the
    unhandled-exception filter, then calls `_set_new_mode(_get_startup_new_mode())`, and the default stub returns 0. The
    explicit call is toolchain startup, not a game decision. The page could say so; its conclusion (mode 0) is unchanged.
- **`_Xbad_alloc` (M2).** The second implementation finds 23 call/jmp sites in 14 functions, as anchored.
- **`NameEquals` (N1).**
  - `00408F30` makes eight dword compares, `+0x00`..`+0x1C`. It returns 0 on a full match and 1 at the first mismatch.
  - Its only callers are `00408FA0`'s two sites. Both follow the call with `test rax, rax / jne 0040907D`, the hit exit.
  - `00408FA0`'s only caller is the thunk `00408F90`. The thunk has four callers, and each passes `r8d = 0` and
    `edx = '@FRM'`.
  - The compare runs against the container header's name at blob `+0x10`, not an entry's name. So "select files whose
    name differs" is the right wording.
- **50 -> 44.** The page's own census table counts 44, and 27 + 7 + 10 = 44. No other page states the 50.
- **Four globals (E1).** `0026D910`'s rip-relative stores are exactly `02099DA8`, `02099DAC`, `02099DB0` and
  `02099DBC`. The routed CONTRACT-weather point is also right: `00263E10` loads `02099DA8` (retool `refs`). It is filed
  as `DATA-REQ-CONTRACT-WEATHER-02099DA8-0930` (READY, SWE2-CONTRACT).
  - **Correction C2:** the environment page still reads **"Pick a variant index, look up the field's authored row,
    publish five globals."** at the head of "What it actually does". That line is unstruck (E2), so the correction has
    not reached every consumer on its own page (policy rule 4a).
- **Memory page reconciliations.**
  - The `+0x0C` / `+0x10` "physical neighbour links" reading agrees with the page's own phys-first splice section.
  - The memory page's status stays REOPENED; the diff does not touch the status line.
- **Supporting reads the pages cite.** The flying-fade stores (`001C8FFF`, `001C9040`), the kind-4 clamp and the 1101/1103
  receipt handlers all reproduce.

## 3. Question 4: reconciliations (SWE2-AUDIT-SEM)

Each reconciled line was compared with its register row at the commit:
- **W-group.** W-1, W-2, W-3 (answered 2026-09-18), W-5 (answered 2026-09-27), W-6, W-7 (SUPERSEDED), W-8 and W-9
  (answered 2026-09-15) all agree.
- **Weather rows.** GB-1 (NO ADMISSIBLE SOURCE) and GB-3 (ANSWERED) agree.
- **Steam and handbook rows.** AB-1 (the mechanism correction of 2026-09-17), AB-3, AB-4, AB-6, UQ-272, UQ-274 and
  UQ-275 agree. So do the handbook list (Trickster..Shadowseer, [the handbook page](../../../16-UI/Handbook/the-handbook-screen.md)) and the
  bestiary tally at `+0x3404` ([actor-bind event memory](../../../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md)).
  AW-4 is WITHDRAWN and needed nothing.

Two exceptions:
- **C9, AB-8.** The Steam status line and the AB-8 box present **SUPERSEDED (2026-09-26)** as AB-8's disposition. The
  register row is not that simple. Since 2026-09-30 it carries FABLE's correction: the SUPERSEDED disposition "rests
  on a FALSE static premise", counter 17 is fed natively (`00317090` once per defeat, and `addclanpoint` through
  `002E2380`), and the row "should read ANSWERED on independent acceptance". That acceptance exists:
  [`auditsem-review-ab8-0930`](../auditsem-review-ab8-0930/REVIEW.md), ACCEPT. The row's lead word is still SUPERSEDED
  at HEAD, and changing it is the register owner's job, not DATA's. Until then the status line should not state
  SUPERSEDED as the active summary. Suggested wording: "AB-8: counter 17 is fed natively (FABLE 2026-09-30,
  accepted); the register word is pending".
- **C11, GB-3 (wording).** The environment page's modding note says `02099DB0` "is written and never read, so editing
  that byte has no effect". That is firmer than GB-3's own row, which bounds the negative to rip-relative readers.
  Suggested wording: "no reader is found (GB-3)".

## 4. Question 3: is each SD row real residue? (SWE2-AUDIT-SEM)

**C1: the register section is malformed.** At `4415dba48` and still at HEAD, SD-160..SD-169 each appear **twice**, with
different questions and statuses (R1). The parent had only SD-140 and SD-141. The second set looks like an earlier
draft appended after the final rows. By its code (read, not run here), `check_questions.py`'s `read_table` collects repeated ids as `DUPLICATE ids` and adds
them to its bad total.
- Several pairs disagree in substance. SD-165's two rows ask different questions: "which callers test null" against
  "whether any player-visible message follows". SD-169's two rows ask about "which GS register" against "frame-buffer
  against display width".
- The shared worktree currently holds an uncommitted edit to the register that deletes the second set. It is not mine,
  I did not review it, and it is not at HEAD.

[`sd_rows_check.py`](sd_rows_check.py), [out](sd_rows_check.out) lists each new row's overlaps. All ten SD-16x ids are
named on their pages. Reading the overlaps, the parent pages and short reads of the bytes gives:

| row | finding | evidence |
|---|---|---|
| SD-140 | **Residue.** A narrowing the row could use: the byte kernel is `00432300` (2,486 B, "MMI-mixed" in the EE-register census). It is shared by 23 call sites in 8 bodies, including both emit paths the row names, `00437130` and `00438860`. So one read of that kernel serves both halves of the question. | K1 |
| SD-141 | **Residue as registered.** OPUS has since answered it (`sd141-flying-fade-readers-0930`: no reader by any route). The two records agree; I did not review OPUS's. | — |
| **SD-160** | **Residue, but the row overstates what the answer decides.** It says free-target type 3 decides "which defeated enemies the bestiary defeat tally skips". The tally has four gates, not one. `003171C0` tallies only when `[unit+0x698]` byte `+5` is 1, the type is not 3, and the class word `+0x52` is not `0xFFFF`. Then `00315820` refuses ids of `0x200` and above, and counts only when `00315D50(id)` returns -1. The handbook page and AA-7 name `00315D50`'s set as the eleven special monsters, which keep their own counters. The row should keep "which units carry type 3" and drop or widen the "and so" clause. | S1 |
| **SD-161** | **Largely answered by the page's own AB-8 paragraph (2026-09-18) plus a short read.** The row says "no census of the field's other writers is on record". The page records a whole-image displacement census of `+0x3844`..`+0x386B`. It finds the counter block formed only by the accessor family `003162E0`, `003166F0`, `00316810`, `00316BF0` and `00316C60`, and my raw sweep reproduces that (S2). Read, the three writers never store a negative: the updater's store `00316BF0` takes the clamped sum (S3); the load normaliser `00316810` writes only `0x7FFFFFFE` (kind 4) or `0x7FFE`/`0xFFFE` (kind 2) when a counter is saturated; the console helper `00316C60` writes 99,999. What stays open is a store that no displacement shows, such as the save image's own bytes on load or at new-game initialisation. The row should say that. | S2, S3 |
| SD-162 | Residue. The script-award census has the sites, not their control flow. | — |
| **SD-163** | **The row says "not read; table row annotated only". The parent reads part of it.** DM-2 (`dm2-code27`, D3, 2026-09-27) shows `007A1CD0` stores exactly the 16 raw pad-button bytes `+0x43C`..`+0x44B`, in the PlayStation order the XInput poll uses. [The vtable method index](../../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) names it slot 5 of `PFramework::PInputDevicePadSteamController`. RC-10 reads its two log gates: local `+0xA9`, and global `02EA95A0`. The row should cite these and narrow to the remainder (axes, and whatever else the 1,124 B write). | DM-2, RC-10 |
| **SD-164** | **The row says "the slot's writer and the function it holds are not named". Both are named in the parent.** [render-event-selection-evidence](../../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md) and [the authored presentation command handlers](../../../17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md) record `0036C5A0(id, fn)` writing `fn` at `022D7FD0 + id × 0xA8 + 0xA0`, with id 6 and id 0xA both set to `002E6D60`. The bytes agree: the only two calls are in `002EA320`. The initializer `00369D30` stores a zeroed `r8` there, and `0036BFE0` calls the slot at `0036C03B` (H1). A short read closes one more point. `002E6D60` has one `ret`, reached only through `002E6E1E xor eax, eax`, so **it always answers 0** (H2). Its side effect is to release the tail of the `0215FD88` list. So for arenas 6 and 10 the retry proceeds only if the reclaim moved something. For the other arenas the slot is empty. The row should narrow to what that release frees. | H1, H2 |
| SD-165 | Residue. `0036BFE0` is the slow path the wrappers `0036A100`, `0036A1A0`, `0036B160` and `0036D050` call after a failed `0036BC60`. A census over those wrappers' callers remains to be done. | — |
| **SD-166** | **Narrowed by a record the parent already has.** RC-11 (`rc11-arena-ten-0930`, ANSWERED, `1e4537034`, before this batch) resolves all 135 sites of the arena push `0036C1D0`. On shipped data they select 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13 and 14, **never 7**; the two debug-verb sites are never called by shipped scripts (H4). The other writers of the active-arena cell `022D89BC` are the initializer `00369D30`, the pop `0036C140`, and the diagnostic paths `00369860` and `0036CB00`. So the row should cite RC-11 and narrow to those writers and any explicit-arena entry. I did not adjudicate the writers. | H4, retool `refs` |
| **SD-167** | **Narrowed by a record the parent already has.** OV-40's `reregister.py` (B2, B4) already traces two handle takers: the motion cache `003DC5B0` and the per-lane submit `002E6EB0`. Both resolve the handle through `0036A000`. The whole population is small: `0036B160` has 13 call sites in 9 bodies, and `0036B980` is reached only through `0036B970`, from 2 sites in 2 bodies (H3). The row should cite OV-40 and state the population. | H3 |
| SD-168 | Residue. | — |
| SD-169 | Residue. It could cite [the mip-budget page](../../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md), which files both `00244200` and `0039D0C0` there. | — |

**Status currency.** At HEAD all twelve rows read OPEN. OPUS has answered SD-141 and is routing SD-140's kernel to an
execution probe. Nothing in this review contradicts either.

## 5. Side observation (SWE2-AUDIT-SEM)

The memory page's §1 bullet "`0036BFE0` returns null only when …" is FABLE's text of 2026-09-28, and this batch
reconciled it. It omits RC-11 part 2. When the selected arena's init bit is clear, `0036BFE0` spins forever at
`0036C000` and never returns. Adding that is optional.

## 6. Corrections routed (SWE2-AUDIT-SEM)

Request `AUDITSEM-REQ-DATA-DD-OWNER-READ-4-ROWS-0930` to SWE2-DATA:
- **C1.** Leave one row per SD-160..SD-169 id and choose each wording deliberately. The two SD-165 variants ask different
  questions.
- **C2.** Strike or correct "publish five globals" on the environment page.
- **C3, SD-161.** Cite the page's own AB-8 displacement census and the three writers' values. Narrow the row to
  non-displacement stores: the save bytes on load and at new-game initialisation.
- **C4, SD-163.** Cite DM-2 D3, the vtable index and RC-10, and narrow the row.
- **C5, SD-164.** Name `0036C5A0`, `002EA320` (arenas 6 and 10), `002E6D60` and the zero answer. Narrow the row to what
  the release frees.
- **C6, SD-166.** Cite RC-11 (no push selects 7), and narrow the row to the remaining writers of `022D89BC`.
- **C7, SD-167.** Cite OV-40, and state the population: 15 sites in 11 bodies.
- **C8, SD-160.** Fix the "and so" clause (four gates plus the `00315D50` set).
- **C9, AB-8.** Change the Steam status line and box wording.
- **C10 (optional).** Name `00432300` in SD-140.
- **C11 (optional).** Change the `02099DB0` modding-note wording.
- **Optional.** Add the MSVC `pre_cpp_initialization` note on the memory page.

The six pages' readings themselves need no change beyond C2, C9 and C11.
