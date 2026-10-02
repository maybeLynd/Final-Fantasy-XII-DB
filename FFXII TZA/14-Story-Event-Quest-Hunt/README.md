# Story / Event / Quest / Hunt

**Engine category.** Story flags, quest stages, hunts, marks, Rare Game, and event triggers.

| | |
|---|---|
| Classification source | PrimaryOwner: Story/Event/Quest/Hunt |
| Functions | 15 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`persistent-flag-banks.md`](persistent-flag-banks.md) -
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. Story progress is **bits** in ~~six banks~~ five banks, six accessor families *(corrected 2026-10-02, OPUS: `Bank512`'s Low and High pairs address one `+0x14B4` region - queries `0032AA60` / `0032AAD0`, setters `0032AD70` / `0032ADF0`, the High pair adding `0x100` at `0032AAE7` / `0032AE04`; persistent-flag-banks.md AA-4)*, at mapped save-payload
  offsets (`+0x1384`, `+0x13B4`, `+0x14B4`, `+0x14F4`), verified contiguous. Flag 0 = always,
  flag 1 = never; bit 14 of an authored id switches to the threshold schedule.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.

## Systems in this category

- [`persistent-flag-banks.md`](persistent-flag-banks.md) -
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. Story progress is **bits** in ~~six banks~~ five banks, six accessor families *(corrected 2026-10-02, OPUS: `Bank512`'s Low and High pairs address one `+0x14B4` region - queries `0032AA60` / `0032AAD0`, setters `0032AD70` / `0032ADF0`, the High pair adding `0x100` at `0032AAE7` / `0032AE04`; persistent-flag-banks.md AA-4)*, at mapped save-payload offsets
  (`+0x1384`, `+0x13B4`, `+0x14B4`, `+0x14F4`), verified contiguous. Flag 0 = always, flag 1 =
  never; bit 14 of an authored id switches to the threshold schedule.
