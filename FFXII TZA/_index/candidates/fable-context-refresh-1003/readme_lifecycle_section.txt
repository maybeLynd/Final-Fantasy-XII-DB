## Project lifecycle after database completion (FABLE, 2026-10-03)

This database is the canonical, evidence-backed specification for two first-class goals: deep modification of the
original game, and later an independent source reconstruction. The authority is
[`RECONSTRUCTION-CHARTER.md` §0](../../RECONSTRUCTION-CHARTER.md#0-project-lifecycle-fable-user-directive-2026-10-02); this is
its summary.

- **Current phase: DATABASE.** Complete and certify L1 MODDING-GRADE + L2 RECONSTRUCTION-GRADE. L3 is not a
  prerequisite. Bounded probes test whether a claim or contract is sufficient, and nothing more.
- **Transition.** Primary reconstruction begins only after two things: the L1+L2 goal and its thirty-pass terminal
  certification are met, **and the user explicitly authorizes it**. `DATABASE READY - awaiting user authorization`
  is a waiting state. No agent or dashboard leaves it on its own.
- **Reconstruction.** FFXII behaviour in independently authored, maintainable source. The original executable and the
  running game are evidence and a differential and live oracle, never the production backend. These do not count as
  reconstruction:
  - wrappers;
  - oracle delegation;
  - hidden fallbacks into the original binary;
  - circular reference execution.
- **Validation.** Canonical DB contract → reconstructed source → original-machine-code differential → live FF12 where
  needed → integrated behaviour. On disagreement, find the first divergence, then correct the reconstruction, the
  harness or the canonical DB claim, with evidence.
- **Maturity is stated, never implied.** A passing pilot is not a reconstructed subsystem, and a reconstructed
  subsystem is not an integrated game.
- **Long-term target.** A whole-game, high-parity reconstructed runtime. The same knowledge keeps improving
  original-game modding.
