# Spawn / Encounter / Lifecycle

**Engine category.** Spawn controllers, member selection, respawn timing, and conditional/rare eligibility.

| | |
|---|---|
| Classification source | PrimaryOwner: Spawn/Encounter/Lifecycle |
| Functions | 52 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`spawn-placement-and-retirement.md`](spawn-placement-and-retirement.md) — ~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: DOCUMENTED`, owner re-status 2026-10-01)*
  Why monsters never appear on top of you (candidate distance validation against up to 4 player
  slots), why they vanish behind you (retire by native range), and why returning quickly finds
  the same ones (**keep window, default 300**). Persistence banks rotate on area transition.

**Weather is a proven input to conditional spawn eligibility** - see [`../03-World-Area-Field/Weather/`](../03-World-Area-Field/Weather/). Much of the orchestration lives in authored `.ebp` scripts rather than native code; decompile the zone script with `ff12-script.exe` to read it.

- [`Spawn-Record/the-spawn-keep-entry-field-map.md`](Spawn-Record/the-spawn-keep-entry-field-map.md) —
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)* The `0x250` spawn-keep entry, offset by offset, from two controlled
  enumerations of everything that reaches it: the eight flag bits, the per-entry rolled death limit
  and cooldown, the persistence key and the whole-record restore it drives, position, facing, the
  persisted affinity bytes, the stats page, and the three ranges nothing touches.
- [`why-the-enemies-you-killed-come-back.md`](why-the-enemies-you-killed-come-back.md) — the two keep banks, their rotation on area transition and the return window — **AUDITED**
- [`spawn-placement-height-and-authored-tunables.md`](spawn-placement-height-and-authored-tunables.md) — the activation-time height, the minimum-distance flags and the script-installed tunables — **AUDITED**
- [`CONTRACT-spawn-placement.md`](CONTRACT-spawn-placement.md) — contract, spawn placement and the return window — readiness **BEHAVIORALLY UNDERSTOOD**
- [`Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`](Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) — the group ledger, completion and respawn timing — **AUDITED**
- [`CONTRACT-group-completion-and-respawn.md`](CONTRACT-group-completion-and-respawn.md) — contract, group completion and respawn — readiness **CONTRACT READY**
- *(corrected 2026-10-02, OPUS: five pages this list omitted, added with the status or readiness each page's own front matter states)*

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
