# SWE2-AUDIT-SPEC review of SD-25 (sd25-sound-thread-rand-0930 at d7d7e52c9): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS. Reviewed
commit `d7d7e52c9`, record [sd25-sound-thread-rand-0930](../sd25-sound-thread-rand-0930/README.md). Static, checked at
HEAD `cb5b622f2`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD25-0930 | sd25-sound-thread-rand-0930 | `d7d7e52c9` | ACCEPT-WITH-NARROWING |

The conclusion stands and gains a corroboration: the Sound selects do not share gameplay's `rand()` stream. The
narrowing is to F3's wording. The rand calls that make the Sound selects' choices are **not** among the four inside
the direct closure. They are four of the "27 gameplay and other callers" outside it, reached only through vtable
slots.

**Re-run.** `sd25_sound_thread.py`: F1-F3 PASS, `FAILS 0`. Output
([rerun_sd25_sound_thread.out](rerun_sd25_sound_thread.out)) is identical to the committed `.out` ignoring CR. The
record directory stayed clean.

**Re-derived independently** ([sd25_rederive.py](sd25_rederive.py) / [.out](sd25_rederive.out), `tk.py`, not retool):
- **Imports, from the PE import directory.** The rand family is `rand` at `008C3098` and `srand` at `008C30A0`, both
  `api-ms-win-crt-utility-l1-1-0.dll`. There is no second `rand` slot. A raw rip census of `008C3098` gives 49
  references in 31 functions, matching F3's 31.
- **Closure.** My own direct-call closure of `007A5400` follows E8 calls and E9 jumps to listed starts, and it has 569
  functions. The record's has 1,359; the closure methods differ, and mine is the narrower. Both contain the stepper
  `007BD120` and `007BDFA0`. The rand users inside are the same four: `007D0260`, `007E6DD0`, `007E7E00` and
  `007F3E30`. There are 27 outside.
- **New corroboration: the thread seeds its own stream.** The thread body's first call is `007A5404 call 007AD680`,
  followed by `007A540B call [srand]` with that result. `srand` has one other user, `008193E0`. Since the UCRT state is
  per thread, the sound thread's `rand()` sequence is seeded and advanced on that thread alone.
- **The Sound selects' own rand calls (the narrowing).** Four of the 27 outside callers are the Sound family's select
  methods, found by where each is stored:
  - `007E5160` is `RandomSound` slot 43;
  - `007E65B0` is `CycleSound` slot 40;
  - `007E6620` is `CycleSound` slot 42, one of F1's virtual roots;
  - `007E5E80` is called directly only from `007E6566` / `007E669A`, inside the two `CycleSound` methods.

  The direct closure has exactly one call site through each of those slot offsets:
  - `0x158` at `007BD205`, inside the stepper `007BD120` itself;
  - `0x140` at `007B3168` (in `007B2F70`);
  - `0x150` at `007B4B06` (in `007B4A70`).

  These are offset-only matches, not type-traced. They are evidence, not proof, that the virtual selects are
  dispatched on the sound thread. The record's "virtual roots" limit remains, and this is the best static evidence for
  it.

**Controls.** F1 and F2 assert the exact root set and the `_beginthreadex` argument shape, so they are sensitive to a
different start routine. F3 checks that the in-closure rand users all fall in the audio range. That control cannot
detect the case the row is about: the selects' own rand calls lie outside a direct-call closure, and F3 is silent on
them. Its "outside: 27" is correct but unlabelled.

**Correction wording for the row owner (SWE2-DATA)** (record F3 and the register row's answer):
> Of the 31 `rand` callers, 4 are inside the sound thread's direct-call closure (`007D0260`, `007E6DD0`, `007E7E00`,
> `007F3E30`). Of the 27 outside it, 4 are the Sound selects themselves, reached through vtable slots:
> `RandomSound` slot 43 `007E5160`, `CycleSound` slots 40 / 42 `007E65B0` / `007E6620`, and their helper `007E5E80`.
> The closure dispatches each of those slot offsets once, at `007BD205` (in the stepper), `007B3168` and `007B4B06`
> (offset match, not type-traced). The thread body seeds its own stream (`007A540B` `srand(007AD680())`). The other
> 23 lie outside the audio module: 19 in `00177850`-`0055B3F0` and 4 in `00819270`-`00866200`.
