# Engine Core Runtime

**Engine category.** Main loop, frame orchestration, scheduling, singleton infrastructure, application bootstrap and cross-subsystem startup services.

| | |
|---|---|
| Classification source | PrimaryOwner: CoreRuntimeScheduling |
| Functions | 73 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`System-Stop-Registry/the-time-stop-and-system-stop-registry.md`](System-Stop-Registry/the-time-stop-and-system-stop-registry.md) —
  **PARTIAL, tier 1.** **The engine's freeze composition**: 28 stop requests (full-screen menus, event
  scripts taking an actor, `settimestopmagic`, `seteventtimestop`, the mask verbs, `ucon`, `skipexec`, the
  status-error deny verbs, the field hold), each a permission record; seven per-actor stop sets (movement,
  script execution, animation rate, controller and battle-unit flags) and one combined mask that also
  switches audio groups, character culling, UI and input words. ~~Open: `SM-1`–`SM-5`.~~ *Corrected 2026-09-26 (FABLE):
  all five were answered on 2026-09-17/18 (the registry page and the register rows).*




- [`Startup-Data-Construction/generated-float-table-builders.md`](Startup-Data-Construction/generated-float-table-builders.md) —
  **PARTIAL, tier 1.** **7 % of the game's code, run once**: 197 functions / 522 KB of
  generated float math that build 75 objects with **no file image**, immediately before the
  startup latch closes. ~~What the objects are is open (**BH-1**).~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **BH-1** was answered on 2026-09-13. The objects are pre-built VIF1 packets for the VU1 microprograms; their contents stay with BH-2.*
- [`Application-Root/game-application.md`](Application-Root/game-application.md) —
  **DOCUMENTED, tier 1.** The application root: **the `FFXII_TZA.vbf` mount at slot 2**
  and a **one-way startup latch at `+0x113C`** with one writer and three readers
  image-wide. Never deleted, hence no stated object size.
- [`Object-Model/vtable-method-index.md`](Object-Model/vtable-method-index.md) —
  **DOCUMENTED, tier 1.** **4,275 function addresses tied to exactly one C++ class and
  vtable slot** — the category README's "highest-leverage task", applied. The 2,611
  linker-folded addresses are excluded with their reason.
- [`Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`](Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md) —
  **DOCUMENTED, tier 1, one falsification pass.** Answers open question **B-4**: the **585
  functions declared to have no owner on purpose** were classified *earned, not inherited* — they
  write module state at **10.1 %** against **21.5 %** for owned functions, and all **107** labelled
  read-side write none at all. **Three sub-labels are wrong** and are named. Also maps the engine's
  **shared geometry scratch**: a 660-byte buffer at `022D9198` written by **215 functions across four
  subsystems**, and why `022D8F00`–`022D9500` is thirteen objects rather than one.

- [`Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md`](Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md) —
  **PARTIAL, tier 1.** The workbench is the **register bank of the PS2 assembly emulation**: EE GPR[32] with `$zero`,
  HI / LO, and VU0 CLIP / Q / ACC / 31 vector rows, with vf00 the constant at `01EF93F0` (`"PS2 Assembly emulation
  initilization completed!"`). Tested register by register at instruction level; census of 267 functions (257
  frontier, 188 uncited). Answers BI-6, BQ-16 and BQ-19.
- [`Shared-Transform-Workbench/the-shared-transform-workbench.md`](Shared-Transform-Workbench/the-shared-transform-workbench.md) —
  **DOCUMENTED, tier 1, one falsification pass.** Answers **BQ-13**. **249 functions write one 1.5 KB
  area and almost none of them call each other** — graphics, sound, character, movement and UI code
  meeting only at the memory. It is an **argument-passing area**, not owned state: every SSE access is
  16-byte aligned (46/46), `003970A0` proves a 4×4 matrix at `022D91B0` — 28 of its 29 callers are
  **Presentation** draw-path bodies (`00456720`, `00450940`, `00458CA0`…; the 29th is the workbench's
  own `0039D430`), the render side taking the matrix back out — the only whole-area clear is unowned, and **exactly one function in the
  image reads a row it did not write**. A relationship class no call-graph reading can find.

- [`Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](Shared-State-Accessors/cross-subsystem-accessor-hubs.md) —
  **DOCUMENTED, tier 1.** Three functions totalling 125 bytes, consulted by **168 callers across
  14 subsystems**. Found by auditing, not by reading a category. The current area id turns out to
  live in the **save image** at `+0x1044`.

- [`Battle-Frame/the-world-tick-and-the-field-frame.md`](Battle-Frame/the-world-tick-and-the-field-frame.md) —
  **DOCUMENTED, tier 1.** `World_UpdateSimulationTick` ticks **five actor-manager slots, up to
  sixteen sub-steps each** (a per-slot byte scripts can set), and the battle layer's field frame
  runs **for slot 0 only** — never behind the full menu. The per-unit lifecycle frame is a
  **callback stored at record `+0x38`** when a battle unit is bound, called from the actor drive
  loop; its address is taken at exactly one `lea` in the image.

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
