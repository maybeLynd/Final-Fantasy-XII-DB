# Affected-consumer check — the field pass's init core has two call sites (OPUS, 2026-09-26)

**The correction.** `CONTRACT-field-runtime-pass.md` §6 (OPUS, owner, 2026-09-12) said:
- that `002620E0` (the field-runtime init core) and the `+0x12` publish run *"only when the driven actor came back
  settled"*;
- that *"every pass takes exactly one of exit A or exit B"*.

Both hold only inside the drive loop:
- **A pass whose slot has `+0x12 == 0`** takes `0025DB25` / `0025DB29 je 0025DB87`, skips the drive loop, and takes
  neither exit.
- **That branch calls audio `00261F90`** (`0025DB8E`).
- **Then, when `+0x17 < 0x80` and `+0x10` bit 5 is clear,** it calls the init core from a **second call site,
  `0025DC27`**.

**Regression:** `_index/candidates/s15-opus-replay-field-pass-stub-free/arms.py`, ALL PASS (4/4, md5 `8a0a93f9…` over two
runs). It is an executable control on the call sites, not a word match:
- **T1:** the image has exactly two `call 002620E0` sites in the pass, `0025DB7D` and `0025DC27`, and one `call 00261F90`.
- **F1:** with `+0x12 = 0`, the init core's return address is **`0025DC2C`**, after `00261F90` ran.
- **F2:** with `+0x12 = 1`, neither runs.

A reimplementation that calls the init core only from exit A fails F1.

| consumer | state |
|---|---|
| `04-Actor-Entity/CONTRACT-field-runtime-pass.md` §6, the two sentences | revised-here (struck; restated for the drive loop, with the `+0x12 == 0` branch and its second call site added) |
| same contract, §5 `002620E0 … gated, §6` | revised-here (the two call sites named) |
| same contract, §6 exit table (rows A and B) | agrees (they describe the drive loop's two exits, which is still exact) |
| same contract, §15 row "the drive loop's two exits are different continuations" | agrees (a claim about the two exits, still exact) |
| `03-World-Area-Field/CONTRACT-weather.md` entry row, "`002620E0` … the only thing that runs the roll" | agrees (it concerns the roll's caller, not the pass's call sites) |
| `03-World-Area-Field/Weather/weather-probability-and-transition-roll.md` row "`002620E0` … one-shot gate, primary ActorManager only" | agrees |
| `_index/candidates/s12-opus-replay-weather-roll/README.md`, "the init core `002620E0`, which is the roll's only caller" | agrees |
| `_index/candidates/s15-opus-replay-field-pass-stub-free/README.md`, not-covered "the init core `002620E0` (exit A needs bit 6)" | revised-here (the init core is executed on the `+0x12 == 0` branch; exit A itself still needs a settled actor) |
| `_index/candidates/s15-runtime-per-invariant-exposure.md`, EXP-106 row naming the init core among the executed bodies | agrees (it lists bodies, not call sites) |
