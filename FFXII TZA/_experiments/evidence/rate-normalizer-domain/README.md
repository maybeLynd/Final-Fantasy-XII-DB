# Shared rate normalization: exact write and return domain

Player view: the shared getter keeps a fractional rate such as0.5. It replaces zero or negative rates with1, which differs from clamping everything below1. This checks engine rules, not visible animation speed or a rate observed in the running game.

**Method A only.** Whole37-byte shipping leaf `00229E70`, exact rate/default RIP targets, primary Intel COMISS flags and conditional source calculations. No original-code execution, emulator, native calls, game, instrumentation, PC controls or actual rate/MXCSR observation. Question and competing hypotheses are in [PLAN.md](PLAN.md).

The code loads `float[01E02820]` into XMM1, zeroes XMM0, executes `COMISS XMM0,XMM1`, then `JB 00229E91`. If the branch is taken it copies XMM1 to XMM0 and returns. Otherwise it loads exact1 from `01CEBBA8`, **stores it back** to `01E02820` at `00229E88`, and returns1. These are two locally complete source paths, not a pure read-only getter.

| completed comparison, zero versus effective rate | path |
|---|---|
| ordered less, rate positive | return original bits; no default store |
| ordered equal, either signed zero | load/store/return1 |
| ordered greater, rate negative | load/store/return1 |
| unordered, rate NaN | return original bits; no default store, **only if comparison completes** |

Positive0.5 is unchanged and refutes the shared-neighbours page's “floor1” reading. Negative1 is reset and refutes the Widget EC7-27 zero-only summary. The animation page's notpositive wording needs an ordered/completed-domain qualifier. A completed NaN is not replaced, so this is not a universal positive-return guarantee. If supported DAZ is set, a raw positive subnormal can become effective zero and select the default path; the game's actual MXCSR is unknown.

Primary [Intel SDM Vol2A, COMISS](https://cdrdv2-public.intel.com/819712/253666-sdm-vol-2a.pdf), PDF322/printed3-216, supplies the completed comparison flags and exception boundary. COMISS can signal invalid for either QNaN or SNaN. An unmasked exception leaves flags unupdated; no fault-handler continuation is inferred. DAZ context follows [Intel Vol1 §10.2.3.4](https://cdrdv2-public.intel.com/671436/253665-sdm-vol-1.pdf), previously retained in31. `isa.json` records identifiers and paraphrased limits. The oversized combined-volume fetch failed; the individual primary volume was read successfully. No community source or UCOMISS-only exception rule was substituted.

The selected bit-pattern predictions in `result.json` are source/ISA calculations, not six live or native tests. Positive2 and zero control retention/default paths; labelled private JB→JBE and swapped-comparison source models discriminate reset and fractional-retention behavior, and exact shipping predicates reject both changes. No altered machine instructions were executed.

Current preimages are retained for FABLE's shared-neighbours, Widget contract and animation pages, plus OPUS's Widget+B8 row. That row already records the guarded reciprocal writers, so its initial “1.0f on every widget” text is a constructor default, not a field invariant. Static caller identities at `00244DFE` and `002469C9` are validated against previously retained source; they do not prove normal reachability or a real fractional rate. Any affected family/disposition needs an exact effect/domain qualifier, not bulk reclassification or an invented exclusion.

Readonly `check.py` validates source, widths/targets/branch, predictions, controls and manifest. Own checks are not independent acceptance. Route correction and a focused owner regression/procedure to FABLE/OPUS; SPEC reviews the high-impact shared-state claim. Initialization, actual rate domain, scheduling, lifetime, exceptions and visible animation effects remain open. Published inputs stay immutable. Saves/config/reference and peer files were read-only; menu setup budget remains consumed/unapproved; full L1+L2 DB_GOAL=NOT_MET.
