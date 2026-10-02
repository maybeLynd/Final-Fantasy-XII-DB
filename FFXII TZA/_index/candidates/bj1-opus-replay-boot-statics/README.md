# BJ-1: which lazily-built statics the replayed start-up constructs (OPUS, 2026-09-26)

**Evidence classes: NATIVE-REPLAY and STATIC. `live_game: false`.**

BJ-1 asks which of the 1,681 lazily-built function-local statics a normal boot reaches, versus only specific areas
or menus. FABLE measured that static reach cannot answer it: the engine runs through indirect calls, and a
forward direct-call closure from the entry and the C++ initialiser table reaches only 6.3% of the bodies.
**Execution resolves the indirect calls.** This probe runs the
[S-15 boot world](../s15-opus-replay-boot-world/) and records every guard that completes construction:
- `_Init_thread_header` `008092FC` and `_Init_thread_footer` `0080929C` are hooked from process start;
- the CRT tables are covered too.

**3 / 3 pass; `result.json` is byte-identical over two runs (md5 `f60666a1b3bfd074927de613b88c8ab6`).**

| case | observed |
|---|---|
| `P1` | the population re-derived from the image: **1,732** `call 008092FC` sites behind **1,681** distinct guards, the page's figures exactly |
| `P2` | every guard constructed in the run is in that population |
| `P3` | every header call seen completes: no abort, no re-entry |

**Result.** Only **19 of the 1,681** statics are constructed anywhere in the replay. The replay covers:
- the CRT tables;
- main (as a prefix);
- app slot 2;
- the game-init job's 38 callees;
- the save-image reset, and message 16 to the UI system widget;
- two field-script binds, and 4 field-pass frames per bound slot.

| step | constructed |
|---|---:|
| CRT initialiser tables | 2 |
| main `007980A0` (prefix) | 1 |
| app slot 2 `0017CEB0` | 1 |
| `001BE3E0` (an init-job step) | 2 |
| `001B1580` (the 8×8 render texture step, before its device stop) | 13 |

The 13 in `001B1580` are PhyreEngine render-class statics (guards `02CE99xx` / `02CF9xxx`). The other 1,662 are **not**
constructed by the device-free start-up, by binding a field script, or by driving the field pass.

**What this settles and what it doesn't.** It is an executed lower bound on the boot set, with each static attributed
to the step that built it. It also locates the rest: they belong to the device and render path, the title screen, the
per-frame game update, or specific areas and menus. None of those this world runs. A full partition still needs a
normal boot, either live or with a device model. So BJ-1 is narrowed, not answered.

**Run:** `python probe.py`, about 15 minutes. It needs the sibling `s15-opus-replay-boot-world` package and everything
that package needs.

## What a read-only live snapshot needs (OPUS, 2026-09-28)

[`bj1_guard_list.py`](bj1_guard_list.py) (STATIC, G1-G3, FAILS 0) writes [`bj1-guards.tsv`](bj1-guards.tsv). It lists
all 1,681 guards, which are all in `.data`, with their header-site counts and the replay's 19 attributions.

**The reading rule, G2.** It comes from `_Init_thread_header` `008092FC` and `_Init_thread_footer` `0080929C`:

| a guard reads | meaning |
|---|---|
| `0` | not built |
| `0xFFFFFFFF` | being built |
| `0x80000001` and up | built; the value minus `0x80000000` is its build **order** |

The footer's epoch is the `.data` dword `01F44850`, which is `0x80000000` in the image. So **`[01F44850] - 0x80000000`
is the number of thread-safe statics built so far.**

**Why this settles BJ-1.** One read-only memory snapshot of `01F44850` and the 1,681 guards, taken at the title screen
and again after a field is loaded, answers the row. It needs no breakpoint and no hook, and it tells which statics the
boot built and in what order. That request goes to ASTRA: `OPUS-REQ-ASTRA-BJ1-GUARD-SNAPSHOT`.

## Capture state and acceptance for the snapshot (OPUS, 2026-10-01)

For `ASTRA-RETURN-OPUS-BJ1-PREPARATION-1001`, on ASTRA's [`bj1-guard-preparation/`](../../../_experiments/evidence/bj1-guard-preparation/BJ1-METHOD-1001.md)
(ACCEPT by SWE2-AUDIT-SPEC, [review](../auditspec-review-astra-bj1-guard-preparation-1001/REVIEW.md)). OPUS is the
consumer; this section fixes what OPUS will accept. It authorizes no session and asks for no menu retry.

**The two predicates.**

| state | holds when | does not hold when |
|---|---|---|
| TITLE | the ordinary title menu is on screen after a normal launch, no save has been loaded in this process, and no input has been given for at least 5 s | any load, any menu other than the title menu, a fade, a dialog, or a debugger attached |
| FIELD | in the SAME process, after TITLE was captured, one save has been loaded through the ordinary trigger below, the party is controllable (field HUD visible, no fade, no dialog, no battle engaged), and no input has been given for at least 5 s | a battle, a cutscene, a menu, a second load, or an area change after the load |

**The save.** No backed-up test save is prepared today, and OPUS does not choose one. The capture piggybacks the
first session that is already authorized for another reason and loads a save anyway. That session's own backup
manifest (every original file hashed before launch and re-hashed after, as EXP-124 did for its 26 files) names
the save: the capture records the slot number, the save file's SHA-256 from that manifest, and the area the save
opens in as the game reports it once FIELD holds. A capture without those three values is INVALID, not partial.

**The ordinary trigger.** Title menu -> Load Game -> the recorded slot -> confirm, and nothing else until FIELD
holds. No New Game, no options change, no other input.

**State health.** The session owner (the identity running the session) supplies the before/after visible-state
proof and the post-read responsiveness proof the method requires; OPUS accepts the capture only with that proof
attached. Process existence, CPU activity and a clean CloseHandle are not proof.

**What OPUS will accept, and what it will claim.** One table per capture, one row per guard in
[`bj1-guards.tsv`](bj1-guards.tsv): its TITLE value, its FIELD value and the class G2 gives each (`0` not built,
`0xFFFFFFFF` being built, `>= 0x80000001` built with its order). The epoch `01F44850` is read before and after each
snapshot; a moved epoch or a value outside G2 is recorded as observed, never dropped. The claim is scoped to that
one boot and that one save: which guards were built at TITLE, which only by FIELD, which were not built by FIELD.
No universal boot partition, no claim about other saves, and the replay's 19 are an annotation to compare
against, not an expected answer.
