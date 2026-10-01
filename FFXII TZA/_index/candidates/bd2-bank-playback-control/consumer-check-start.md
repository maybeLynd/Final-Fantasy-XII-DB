# Affected-consumer check — BD-2 start commands, and the G-16 arm-step branch (FABLE, Claude Opus 5.5, 2026-09-26)

Two corrections, both found while identifying SEAD commands `0xA` and `0x1C`.

1. **"`0xA` and `0x1C` (from `007A78B0`, reached from Seb's slot 2)"** — FABLE's BD-2 box, earlier the same day.
   The control read each vtable body up to its first `ret`. Seb's slot 2, `00223E60`, is a teardown ending in
   `jmp 00222000`, with no `ret`, so the read ran on into the following functions and credited the slot with
   their calls: `007A78B0`, `007A6DB0`, `007A8CF0`, and one of `007A7010`'s three attributions. Bounded by the next
   function start, no bank vtable slot reaches `007A78B0` within two calls. Its bank-range callers are five
   non-virtual functions: the voice starts `00224570` / `00223190` and `00224E40`, `00224F10`, `002252C0`. Every
   other attribution the box states survives the bounded read: base slot 9 pause/resume, the teardowns' stop,
   Music slot 0, and Seb slot 6's `0xE`.
2. **G-16 table, state 2: "the object's vcall `+0x128` returned true"** (FABLE, 2026-09-12). In `007BDFA0` the call is
   followed by `test al, al` / `jne 007BE07D` (`007BE06E`). A non-zero answer jumps to the stepper `007BD120`, and
   state 2 is stored only on the zero fall-through (`007BE072`). The callee, `007BD0A0`, answers 1 once the referenced
   object reports ready. So the trigger waits "armed" when nothing is ready yet, and is stepped at once otherwise.
   The state's meaning (armed) and every other row of the table hold.

**Regression, run by FABLE 2026-09-26:** `_index/candidates/bd2-bank-playback-control/bank_sead_calls.py`, 13 checks,
FAILS 0.
- N1 reproduces the defect as a sensitivity check: read unbounded, Seb slot 2 "reaches" `007A78B0`; read bounded, it
  does not.
- N2–N6 read the wrapper's type dispatch, both drain arms and their resolvers, both state-1 arm methods, the two
  classes' status slots, and the wrapper's raw caller index.
- N7 checks the `007BDFA0` branch direction.

| consumer | state |
|---|---|
| `18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md`, BD-2 box | revised-here (struck, corrected, start path added) |
| `_index/OPEN-QUESTIONS.md` BD-2 row ("Open: … `0xA` / `0x1C` unidentified") | revised-here (struck, ANSWERED) |
| `18-Audio/Sound-Selection/sound-trigger.md`, G-16 table row 2 | revised-here (struck "true", corrected) |
| `_index/OPEN-QUESTIONS.md` G-16 row ("2 armed (`007BDFA0`, vcall `+0x128`)") | agrees (states no direction) |
| `18-Audio/Sound-Selection/sound-trigger.md`, "Where `+0x500` comes from" (`007A78B0` dispatch and callers) | agrees (the same dispatch, the same five callers) |
| `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md` §5, "`007A78B0` start" | agrees |
| `_index/AUDIT-LOG.md`, `_index/_inbox/*` | history; "Seb's slot 2" and "`+0x128` returned true" do not occur there (grepped 2026-09-26) |
