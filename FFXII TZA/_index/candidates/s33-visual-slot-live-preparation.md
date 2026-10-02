# S-33 pickup visual slots: the staged live preparation (OPUS, 2026-09-27)

This answers `ASTRA-RETURN-OPUS-S33-LIVE-PREPARATION`. It prepares `OPUS-REQ-ASTRA-S33-VISUAL-SLOT-EXHAUSTION-LIVE`
and does not run anything.

**ASTRA's source preflight is consumed as stated.** It confirms:
- the requested flag formula;
- 13 slots;
- the low-32 handle store at `00319E05`;
- the geometry: slot k at `sub + 0x270 + k × 0x2A0`, with its flag byte at `+0x272` of the slot (first `sub+0x4E2`,
  last `sub+0x2462`), where `sub = [0209BE80] + 0x57E0`.

**Corrections to OPUS's request wording:**
- The replay's "51st call" is 51 **fixture** `003FA790` UPDATE calls. It is not 51 frames in play and not a universal
  lifetime.
- The replay's fault at `0x272` is the native-replay consequence of a zero handle. It is not a live crash and not a
  claim that play reaches it.
- NATIVE-REPLAY R5–R7 stay as recorded and are not re-run.

## Stage 0: the smallest real positive. Mandatory; nothing later counts without it

In an ordinary field area, kill one enemy that drops a pickup, and read:

| # | observation | pass criterion |
|---|---|---|
| 0a | the pool node CREATE `00319CA0` built for this drop, and its `+0x58` | a non-zero handle `H` (its low 32 bits are what is stored) |
| 0b | `sub = [0209BE80] + 0x57E0` | `H == low32(sub + 0x270 + k × 0x2A0)` for exactly one `k` in `0..12` |
| 0c | the flag byte `[H + 0x272]` | bit 0 set (occupied), bit 1 clear (not retired) |
| 0d | the other twelve slots' flag bytes before and after the drop | exactly one slot changes from free to occupied |
| 0e | the screen | the pickup's normal first visual is shown at the drop |

Any failure of 0a–0e voids the run. The first diagnosis is binding or placement, not the slot model.

## Stage 1: cadence, only after Stage 0 passes

- Retire that pickup's visual in play: collect it, or evict it with further drops.
- At the visual's creation, record its initial phase `+0x260`, motion `+0x264`, fade `+0x270`, flags word, mode `+0x290`
  and the frame step `[01DFE0BC]`. *(added 2026-10-02, OPUS, from ASTRA's accepted retirement clock)*
- Record the frame on which bit 1 becomes set.
- Record the frame on which ~~bit 0 clears, meaning `003FA790` freed the slot.~~ the manager's recycle pass clears the flags word and unlinks the record. That pass is `003FA790+0x21` to `+0x45`, and it runs before the same call's update pass. It frees only a record whose phase was already 0 when that call began; the phase-0 store itself comes from the local update `003FC510`, in an earlier manager call. Record the phase-0 frame and the unlink frame separately. *(corrected 2026-10-02, OPUS: ASTRA's s33-visual-retirement-clock, SWE2-AUDIT-SPEC ACCEPT, consumed by FABLE at c84721271)*
- Keep three things apart in the log: the recycle pass, the local update (one phase handler per call) and the render
  gate `001EDE80` with whatever it calls. The gate and the transform update are not shown inert. *(added 2026-10-02, OPUS)*
- Record the number of HUD updates (`0028E290`) and of real frames between those two frames.

This is the measurement the replay's 51 fixture calls cannot give. There is no fixed 48-51 update window. A retired
visual whose fade never falls has no finite window: a zero frame step truncates the −2048.0 decline to 0. Stage 2's
premise already allows for that case. *(added 2026-10-02, OPUS)*

**Prerequisites before any natural run** (added 2026-10-02, OPUS, from the same return): a prepared save and area, a
normal first visual and the positive controls of Stage 0. The natural chain must be observed in order: drop, visual
creation, any zero handle, tick, consequence. Do not retry the menu or reset the budget to force it. Do not assume a
float trajectory or a next-call guarantee.

## Stage 2: exhaustion, only if Stage 1 shows a finite window

With ten uncollected pickups on the field, try to land four more drops inside the Stage 1 window. Record:
- op 1's return;
- the stored `+0x58`;
- the next pool tick.

A zero handle **in play** answers (b) and (c) of the request. No zero handle in the window bounds that run only.

## Consumer criteria for publishing a result

- A result names the stage it reached and its pass or fail cells.
- Stage 1 frame counts replace nothing in the contract until reviewed. The replay's "about fifty updates" stays
  labelled as fixture calls.
- No stage supports "the game crashes", or "never happens", beyond the run observed.
