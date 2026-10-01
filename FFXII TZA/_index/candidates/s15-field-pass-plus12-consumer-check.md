# Affected-consumer check — the slot's `+0x12` is raised by the bind and cleared by exit A (OPUS, 2026-09-26)

**The correction.** `CONTRACT-field-runtime-pass.md` (OPUS, owner) made two statements about `+0x12`:
- §3 said it is *"written `r12b` only on the settled exit"*;
- §6's exit table said exit A *"publishes the running conjunction"* there.

Both are wrong.
- **The bind raises it.** `ActorManager_BindLoadedDefinition` stores `(word [definition + 0x50] >= 0)`
  (`0026CD1A` / `0026CD25` / `0026CD28`). That word is the driven actor's ordinal, the same one the drive loop reads at
  `0025DB31`.
- **Exit A clears it.** The exit stores `r12b`, which the drive loop has just set to 0 (`0025DB2E mov r12d, edi`, with
  `edi` zeroed at `0025DA98`).

So `+0x12` is a one-shot "drive the named actor until it settles" request.

**Regression:** [`s15-opus-replay-boot-world/check.py`](s15-opus-replay-boot-world/). It checks both sides:
- **B2:** the two shipped field scripts bind to `+0x12 = 0` (`ttl_b01`, word −1) and `+0x12 = 1` (`byu_w01`, word 0),
  with the three bind instructions byte-checked.
- **X2:** `+0x12` is 1 after frame 0 and 0 after frame 1's exit A.

A reimplementation that never raises `+0x12` at bind never runs the drive loop, and fails X2. One that publishes a
running conjunction at exit A leaves `+0x12` set, and also fails X2.

| consumer | state |
|---|---|
| `04-Actor-Entity/CONTRACT-field-runtime-pass.md` §3, the `+0x12` row | revised-here (struck; restated with both writers) |
| same contract §6, exit table row A, "publishes the running conjunction" | revised-here (struck; it clears) |
| same contract §6, "The drive loop is entered only when the slot's `+0x12` is non-zero" | agrees |
| same contract §15 row, "the drive loop's two exits are different continuations" (`0025DB79` / `0025DB7D` only on exit A) | agrees |
| same contract, line 408's measurement, "exit A (`cl & 0x40`) clears `+0x12`" | agrees (this is what the correction states) |
| same contract, the return row (`r12d`, "the conjunction the two later folds accumulate") | agrees (the folds at `0025DD5F` / `0025DEAB` run after the drive loop's paths; a separate use of the same register) |
| `_types` `ActorManagerSlot +0x012 slotStateByte12` ("only cmp==0 observed") | agrees as far as it goes (a representation row). The access index already lists both writers (`0025DB79`, `0026CD28`); the meaning is left to the type owner |
| `_index/candidates/s15-opus-replay-field-pass-stub-free/README.md`, cases I1 / I2 (`+0x12` planted to 1 or 3) | agrees (fixtures for the drive loop; the boot world now reaches it from a real bind) |
