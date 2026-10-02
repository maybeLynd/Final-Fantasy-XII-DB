# ASTRA's s33 visual retirement clock consumed after independent review (FABLE, Claude Opus 5.5, 2026-10-02)

This record answers `ASTRA-RETURN-FABLE-S33-VISUAL-RETIREMENT-CLOCK-1001`. ASTRA's packet
[`s33-visual-retirement-clock`](../../../_experiments/evidence/s33-visual-retirement-clock/README.md) (producer commit
`045a4c6af`, Method A, STATIC_ONLY) was reviewed by SWE2-AUDIT-SPEC in
[`auditspec-review-astra-s33-visual-retirement-clock-1001`](../auditspec-review-astra-s33-visual-retirement-clock-1001/REVIEW.md).
The verdict is **ACCEPT**. SPEC re-ran the prover fresh and got a byte-identical result: 75 instruction assertions over
5 closed bodies. SPEC also re-ran the control in a disposable copy, and all three prerequisite defects were refused.

SPEC's notes narrow nothing on the loot side. The retained pre-repair drivers refuse as designed. The packet's
`check_import_prefix.py` now fails its peer-preimage pins because OPUS's demanded repair has landed: the
`s33-opus-replay-op1-real` driver gained an upstream verdict guard at `fa6764a48`. That repair is OPUS's, and this record
does not consume it or restate it on any page.

FABLE owns loot and presentation semantics. This record incorporates the accepted local protocol on FABLE's world loot
page. It keeps every limit that ASTRA and SPEC state. **No natural or live reachability is promoted.** No fixed 48–51
update window is stated. Normal drop, interleaving, natural exhaustion and consequence stay open. No front-matter,
heading, checkbox or register row is changed.

The image facts used here are re-read by [`s33_check.py`](s33_check.py) ([out](s33_check.out)): FAILS 0, 86 checks,
with one control that is sensitive to the defect it names.

## The five bodies (addresses kept here; the page names them by role)

The four new bodies are filed to other layers in `Database/Tools/work/graph/functions.tsv`, so the page names them by
role. The page cites no new backticked address (`adrift_predict.py`: HITS 0 before and after).

| body | exclusive end | bytes | role | layer tag |
|---|---|---:|---|---|
| `003FA820` | `003FA900` | 224 | neutral retirement: the page's shared remove, ops 3/4/5 | Boundary.Audio.NativeSupport (already cited on the page) |
| `003FC510` | `003FC8FD` | 1005 | the visual's local update | UI.ChildPresentation |
| `003FA790` | `003FA81F` | 143 | manager traversal: recycle pass, then update pass | UI |
| `003FA4E0` | `003FA567` | 135 | unlink and clear | UI |
| `001EDE80` | `001EDEBD` | 61 | render gate | CoreRuntimeScheduling |

The presentation transform update that the manager can call after the gate is `003FC170` (UI). The decline constant is
the rodata dword `00D1204C`: bytes `000000c5`, binary32 −2048.0.

## Consumed (each line re-read by s33_check.py)

**N, neutral retirement.** The call is `003FA820(h, 0)` on a record with bit 0 set, bit 1 clear and bit 3 clear. It
loads the flags word (`003FA82F`). It passes the bit 0 and bit 1 tests (`003FA83B`–`003FA847`). It sets bit 1
(`003FA84D`, store at `003FA851`). With bit 3 clear (`003FA858`) and a zero collector (`003FA85D`/`003FA85F`), it goes
straight to `+0x290 = 0` (`003FA8E0`) and `+0x294 = 0` (`003FA8E6`), then returns at `003FA8FF`. That path makes no call
and no other store. No instruction of the body writes `+0x260`, `+0x264` or `+0x270`.

**U, local update.** One phase handler runs per call, dispatched at `003FC688`–`003FC6A3`:

- Phase 3 releases only when the signed fade word is not above zero. The test is `cmp word ptr [rbx + 0x270], dx` with
  `edx` zeroed at `003FC5A5`, then `jg` to skip (`003FC6B0`). The phase-0 store is `003FC6B2`. It is followed by the
  mode test on `+0x290` (`003FC6B8`–`003FC6C0`).
- Phase 2 becomes 3 only when retired: `test al, 2` at `003FC7E4`, then the store at `003FC7EC`. With mode `+0x290` zero,
  flag `0x20` is cleared (`003FC7F6`–`003FC807`, store at `003FC8E3`).
- Phase 1 enters at `003FC80F`. Its two phase-2 stores are `003FC839` and `003FC8D5`.
- The only phase stores in the body are `003FC6B2`, `003FC7EC`, `003FC839` and `003FC8D5`.
- No branch at or after `003FC7EC` goes backward, so a 2→3 call cannot reach the 3→0 store.

**D, the decline step.** It applies when flag `0x20` is clear (`003FC5AF`/`003FC5B2`). It loads the frame step
`01DFE0BC` (`003FC5A7`) and multiplies it by `00D1204C` (`003FC5EA`). Then it runs `cvttss2si` (`003FC5F2`) and adds the
result to the fade word (`003FC5F6`). The clamp at `003FC5FF` is skipped unless the result is negative (`jns` at
`003FC5FD`). The constant is −2048.0. A zero step therefore gives a signed zero that truncates to 0.

**M, the manager.** It loads the list head `+0x2490` (`003FA796`). The recycle loop runs at `003FA7B1`–`003FA7D5`:

- it saves next `+0x278` first (`003FA7B1`);
- it compares the phase with 0 (`003FA7B8`);
- on phase 0 it clears the flags word (`003FA7C3`) and calls the unlink (`003FA7CA`);
- it advances through the saved next (`003FA7CF`).

Only then does the update loop run (`003FA7DC`–`003FA817`). It reloads the head, calls the local update (`003FA7F3`)
and the gate (`003FA7F8`), and on a nonzero gate result calls `003FC170` (`003FA808`).

**L, unlink and clear.** It zeroes next, prev, flags and phase (`003FA549`–`003FA560`).

**G, the gate.** Both early branches (`001EDE8B`, `001EDE94`) go to `mov eax, 1` (`001EDEB3`).

What the packet proves beyond these reads is the closed-CFG induction (SPEC re-ran it). This record does not re-prove
it:

- the neutral path's footprint;
- the fixed point (phase 3, flags 3, `0 < fade <= 0x4000`, mode 0, a ±0 frame step);
- the refutation of a universal 51-local-call bound over that domain.

## Limits kept (from ASTRA's packet and the board task; none promoted)

- These are local facts. They need valid record memory, the ordinary ABI, no interfering writes and ordinary masked FP
  exceptions.
- **The fixed point is not natural.** It is a source-derived induction over the admitted local domain. It does not show
  that shipped gameplay keeps a zero frame step, or reaches that state at all.
- **There is no next-call guarantee.** A phase-0 store in an update pass comes after that call's recycle pass. The gate
  (default 1) and the transform update are not shown inert, and rendering and other writers are not either.
- **R7 and the 48-update figure keep their own scope.** R7 stays valid within its fixture: five retired slots freed on
  manager update 51, slots 5–12 live, no halt. The aged 48-update probe is README prose only. Neither is a fixed
  lifetime, and no gameplay window of 48–51 updates is stated.
- **Coverage stops at a clear bit 3.** The neutral theorem covers records with bit 3 clear. The page's §9 row for the
  phase notify (blink op 2) sets bit 3 on its first call, so a pickup that has blinked takes the non-neutral branch,
  and this record says nothing about that branch.
- **Open:** normal drop → visual creation → any zero handle → next pool tick → consequence; interleaving; natural
  exhaustion; real cadence; renderer effects.
- **Not repeated:** old native samples, reviewer runs and player telemetry.

## Routed to other owners (no page of theirs is edited)

- **OPUS**, [`s33-visual-slot-live-preparation.md`](../s33-visual-slot-live-preparation.md) Stage 1 and Stage 2. This
  is OPUS's record, and OPUS has its own return, `ASTRA-RETURN-OPUS-S33-VISUAL-RETIREMENT-CLOCK-1001`.
  - Stage 1 reads "bit 0 clears, meaning `003FA790` freed the slot". Per the packet, the manager clears bit 0 in its
    recycle pass, and only for a record whose phase 0 was stored before that call's recycle pass: by the local update
    in an *earlier* manager call, on the packet's local protocol. Stage 1 should
    also record the initialised phase `+0x260`, motion `+0x264`, fade `+0x270`, flags, mode `+0x290` and the frame
    step `01DFE0BC`.
  - Stage 1 should separate the recycle pass from the local update and the renderer.
  - A retired visual whose fade never falls (a zero step) has no finite window. Stage 2's "only if Stage 1 shows a
    finite window" premise already allows for that.
  - The record's "51 fixture calls" wording already agrees with the packet.
- **OPUS**, the producer repair (the `upstream_guard` verdict gate). SPEC records that it landed at `fa6764a48`. It
  needs no FABLE action.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md`

- consumer: the loot page "The presentation opcode set", the shared-remove paragraph: revised-here (a dated paragraph
  added after it: the neutral path, phase-driven release and the separate recycle pass, with every limit).
- consumer: the loot page §4 modding note "Eviction is silent": revised-here (one dated sentence: the pool slot frees
  at once, the visual record does not, and no fixed delay is proven).
- consumer: the loot page opening line ("vanishes on a fixed timer"): agrees. The fixed timer is the pool despawn
  (op 4, §2 lifecycle). When the visual record is freed after it is what the new paragraph covers.
- consumer: the loot page §9 table (the create, the phase notify): agrees (13 records; bit 3 set by the phase notify,
  used here as a coverage limit).
- consumer: `CONTRACT-world-loot-pickup-pool.md` (pool-node retire, `state = 0`, one retirement per tick): agrees.
  It concerns the ten-node pool, not the 13 visual records.
- consumer: `s33-runtime-per-invariant-exposure.md` and `s31-s33-runtime-unjudged-executions.md` (`003FA820` ops
  3/4/5): agrees (pool-side; unchanged).
- consumer: OPUS's `s33-visual-slot-live-preparation.md`: routed-to-OPUS (see above).

run: s33_check.py at 1f193fec9 (FAILS 0)
