# Combat AI and Gambits

**Engine category.** Enemy AI decision-making, Gambit evaluation, and AI target selection.

| | |
|---|---|
| Classification source | PrimaryOwner: CombatAI |
| Functions | 43 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`gambit-evaluation-and-enmity.md`](gambit-evaluation-and-enmity.md) -
  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: DOCUMENTED`)*. The gambit walk (**first match wins**, 24-byte records, 32-byte header)
  and the hidden **40-entry enmity table** that decays by ~~exactly **-10**~~ **-10** per interval down to 1, never to 0 *(corrected 2026-10-02, OPUS: `0032191D`–`00321923`)*, held
  while engaged. Third sighting of the shared foe-class gate.
- [`which-gambit-set-fires-and-how-a-command-switches-it.md`](which-gambit-set-fires-and-how-a-command-switches-it.md) -
  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. Where the walk's `subgroup_index` comes from: a one-byte field at
  `unit + 0x6B5` touched by **four instructions in the whole image**. A unit tries **four order
  sets in a fixed order** and only one of them uses the selected subgroup; **twelve command ids
  map onto subgroups 0-11**; a failed third set **skips the subgroup-selected one entirely**.
  Two order sets are compiled into the image and **decode under the layout the walk implied**.

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
