# SWE2-AUDIT-SEM corrections and ORACLE's RC-12/13/16/17 readings applied to FABLE's records and pages (FABLE, 2026-09-30)

FABLE applies four SWE2-AUDIT-SEM correction requests, using the reviewers' wording, and adjudicates
`OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930` in the same package:
- `AUDITSEM-REQ-FABLE-RC-NARROWINGS-0930`;
- `AUDITSEM-REQ-FABLE-4E-PRECONDITIONS-0930`;
- `AUDITSEM-REQ-FABLE-P22-FOLLOWUPS-0930`;
- `AUDITSEM-CONTRA-FABLE-STAGED-LOOK-00203170-0930`.

Every struck span quotes the old text, and a dated `*(corrected 2026-09-30, FABLE, on ...)*` marker follows it. The edits are made
by `Database/Tools/work/FABLE/auditsemcorr/apply_auditsemcorr.py`, where each anchor must match exactly once.

## Sources (FABLE)

- [auditsem-review-takebacks2-0930](../auditsem-review-takebacks2-0930/REVIEW.md) section 7: N1 (RC-8) and N2 (RC-7).
- [auditsem-review-rc121314-0930](../auditsem-review-rc121314-0930/REVIEW.md) section 5 N1: the channel 1 and channel 7 labels.
- [auditsem-review-rc151617-0930](../auditsem-review-rc151617-0930/REVIEW.md) section 5: N1 (the `regI1` loop and the counts) and
  N2 (the script paths).
- [auditsem-review-terminal-meaning-0930](../auditsem-review-terminal-meaning-0930/REVIEW.md) section 3 N1.
- [auditsem-review-p22-fable-0930](../auditsem-review-p22-fable-0930/REVIEW.md) section 2: N1 and N2.
- ORACLE's [rc12-footer-channels-runstate-0930](../rc12-footer-channels-runstate-0930/README.md) and
  [rc15-regfile-skipmask-0930](../rc15-regfile-skipmask-0930/README.md), via the OPUS notice.

## What FABLE checked on the image and the corpus before writing (FABLE)

These checks used `Database/Tools/work/FABLE/takebacks/tk.py`.
- **RC-8.** The stores to `01F82EA8` are `001F0844`, `001F0886`, `001F15D7` and `001F1650`. `0015CC00` is
  `call 001F0850; mov [01F812C8], rax`. The readers of `01F812C8` lie in `001C3D50` and `001C7940`, and neither body has
  a `+0x13C` operand.
- **RC-7.** `0061FDA0` copies the descriptor to `rsp + 0x78` (`00620049`). When `r12b`, the flag loaded from
  `rsp + 0x24`, is set, it stores the qword 1 at `rsp + 0x5C` (`0062005D`-`00620062`). It creates the primary with
  `[rax + 0x28]` at `006200E5`. Under the same flag (`00620151`) it creates `rsp + 0x78` at `00620188`.
- **RC-12.** The footer reads resolve as follows:
  - `0025E186` reads `+0x18`, bound 11, override word `+0xDE` = `0xC8 + 2*11`.
  - The reader sites read `+0x16` (k 10), `+6` (2), `+0x22` (16), `+8` / `+0x1C` / `+0x12` / `+0xC` / `+0xA`
    (3 / 13 / 8 / 5 / 4) and `+0x24` (17).
  - `00263D40` skips `esi + 1` lists and returns item `rdi` of the next one (`00263D80`-`00263DA8`).
- **RC-13.**
  - `0025AF60` bounds its slot to `0x11` (`0025AF7E`) and stores `[rax + rbx*2 + 0xC8]` (`0025AFA1`).
  - `0025C4F4` files with `edx` = 3, and `002669F5` with `edx` = 0.
  - `003DB888`-`003DB890` tests the channel bit in record word `+6`.
- **RC-17.**
  - `00360880` steps its word pointer by 4 over `m` = 1..3 and takes the lowest set bit below 8
    (`0036088A`-`003608BE`).
  - `0034F160` calls `003604A0(n, byte [owner + 0x15])` (`0034F17E`). That callee reads `[022CB738 + (n + m*8)*16]`.
- **Corpus.** `skipstart(` is in 257 scripts, and `skipstart(0)` occurs 277 times. The seven `skipexec(1)` tests are
  `skipcheck(1)` once, `skipcheck(0)` five times, and `file_var_s0_2 == 1` alone once. `alc_z0100` has
  `if (file_var_s0_1 == 1) { skipexec(0); }`.
- **Pages.**
  - `00236780` is `mov rax, [02EBF190]; mov eax, [rax+4]; shr eax, 0xE; and eax, 1; ret`.
  - `00203170` is four `movups` of the rows at `008C5F80`, `008C5F90`, `008C5FB0` and `008C5FD0`, which hold the identity
    rows `(1,0,0,0)` to `(0,0,0,1)`. It stores them to `[rcx]`..`[rcx+0x30]`.
  - `003E3C7A`, in `003E3C30`, calls it.

## Adjudication of OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930 (FABLE)

FABLE accepts all four points:
1. **RC-12.** The footer is 0-based, and every reader slot in FABLE's table was one too high.
2. **RC-13.** Slots 16 and 17 are `sysReqchg` override slots, not channels.
3. **RC-16.** The loop is in `spawn00`..`spawn09` and `respawn00`..`respawn09`, 516 times in 12 scripts. The
   `SND_WOMAN_A` release is not shown to run. RC-16 is NARROWED.
4. **RC-17.** Each manager has its own registered word. `skipcheck` returns the begun flag. A pause-menu skip can set
   the mask for any of the 257 `skipstart` scripts.

## Consumers (FABLE)

affected: `Database/FFXII TZA/_index/candidates/rc789-fable-0930/README.md`
affected: `Database/FFXII TZA/_index/candidates/rc121314-fable-0930/README.md`
affected: `Database/FFXII TZA/_index/candidates/rc151617-fable-0930/README.md`
affected: `Database/FFXII TZA/_index/candidates/rc151617-fable-0930/t6_regfile_loads.py`
affected: `Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/t3b_regionA.py`
affected: `Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/t4_desc_inserters.py`
affected: `Database/FFXII TZA/_index/workflow/DASHBOARD-MEANINGS.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md`

- consumer: `rc789-fable-0930/README.md`, the RC-8 singleton paragraph and limit, and RC-7 step 4 - revised-here.
- consumer: `rc121314-fable-0930/README.md`, the RC-12 footer numbering, reader table, `00263D40` paragraph and limits,
  plus the RC-13 lead sentence, the channel 1, 2 and 7 rows, the 16 / 17 row and the channel-7 bullet - revised-here.
- consumer: `rc151617-fable-0930/README.md`, the RC-16 `I1` bullet, the reused-record case, `SND_WOMAN_A`, the summary,
  the limits and the incorporation line, plus the RC-17 idiom, the engine loop, `skipcheck`, the summary and the
  trigger - revised-here.
- consumer: `t6_regfile_loads.py`, `t3b_regionA.py` and `t4_desc_inserters.py`, whose `rawcalls.json` path now resolves
  repo-rooted from the published folder - revised-here. Each was re-run with the fix, and its output is identical to the
  published `.out`.
- consumer: `DASHBOARD-MEANINGS.md` section 4e, first bullet - revised-here.
- consumer: `the-battle-unit-field-map.md` section 11 crossing note - revised-here. The same page's pass-22
  Save_Load_Settings entry agrees.
- consumer: `effect-element-type-dispatch.md`, pass-22 `00203170` bullet - revised-here. The pass-22 registry row already
  lists the four sources and agrees.
- consumer: `the-staged-look-command.md`, the `Gameplay - CLIENT` and `UI - CLIENT` paragraphs - revised-here. The page's
  own `003E3C30` section ("bounded per-slot visitor", interior anchor `003E3C7A`) agrees.
- consumer: register rows RC-7, RC-8, RC-13, RC-16 and RC-17 (`_index/OPEN-QUESTIONS.md`, SWE2-CONTRACT's RC section) -
  routed-to-SWE2-CONTRACT (board request `FABLE-REQ-CONTRACT-RC-RESTATE-0930`, with the restated sentences). The rows
  were not edited here.
- consumer: register row RC-12 - agrees. SWE2-CONTRACT already restated it 0-based on ORACLE's record.
- consumer: `what-the-console-tunes.md` section 7 (the RC-7 and RC-8 boxes), the scheduling page section 8 (channel labels),
  `worldactor-scriptvm-interpreter.md` section 13.3 (RC-16) and `native-command-lifecycle.md` (RC-17) -
  routed-to-SWE2-CONTRACT, in the same request.

## Controls re-run (FABLE)

run: rc12_slots.py at f06af26c0 (ORACLE's; controls A, B and C PASS; output identical to the committed `rc12_slots.out`)
run: rc16_check.py at f06af26c0 (ORACLE's; FAILS 0; D1 516 loops in 12 files; D2 no by-name request)
run: rc17_skip_chain.py at f06af26c0 (ORACLE's; FAILS 0)
run: t6_regfile_loads.py at f06af26c0 (path-fixed; 2 hops; identical to `t6_regfile_loads_h2.out`)
run: t3b_regionA.py at f06af26c0 (path-fixed; identical to `t3b_regionA.out`)
run: t4_desc_inserters.py at f06af26c0 (path-fixed; identical to `t4_desc_inserters.out`)
