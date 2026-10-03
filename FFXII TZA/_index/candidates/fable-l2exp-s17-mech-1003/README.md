# FABLE: S-17, the cooldown clock across a reset and a load (staged, 2026-10-03)

## What this package is (FABLE)

This is FABLE's staged contract text for SWE2-AUDIT-SPEC's **narrow SCOPE-SHORT on S-17**
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md) item 3, [`item3.md`](../auditspec-l2-expansion-1003/item3.md) "### S-17"):
*"the clock-across-load interaction … which the contract neither states nor bounds"*. No tracked file is edited.
`apply.py` was run as a dry run only, and nothing was committed or posted to the board.

**Host contract:** [`05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md`](../../../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md).
It is S-17's credited subsystem contract, and its contract line is the registry subject verbatim ("the dead-member
checklist and the cooldown clock"). The clock is its §10 box and §12 formula. The new section is **§10a**, inserted
after §10 (failure paths) and before `## 11. Observable behaviour`.

**Already stated elsewhere? Checked first, and only in part.** The respawn page's §"What a load does to the two banks and
the window" (L83–113) tabulates the load's effect on the counter, the stamp, the history and the banks. The save-image
contract §13 states `0032A160`'s body and its one caller. **No contract states what the cooldown computes when the
counter and the stamps come apart.** So §10a cites those two for their facts and states only that interaction, with the
reset routes the page did not list.

| file | what |
|---|---|
| `section.txt` | the drafted §10a, with invariant **G9** (a–d). G9 continues the G1–G8 ids that the S-17 replay gives §4's invariants; §4 itself has unnumbered bullets |
| `check_s17.py` / `check_s17.out` | the executed check: K1–K7 and sensitivity controls S1–S4, **FAILS 0** |
| `rawref.py` | the raw reference index the check uses (the parent's helper, with a NOPDATA decode fix, see below) |
| `apply.py` / `apply_dryrun.out` | inserts §10a before `## 11.`. It is anchored, refuses a dirty page, keeps CRLF/LF, is idempotent and prints **FAILS 0** |

## The facts, with sites (FABLE)

- **The counter `0208D45C` has exactly two writers** (K1). One is `0032A135` `inc`, which runs only when `003EBA90(0)`
  differs from `[022C317C]` (`0032A12A`–`0032A133`). The other is `0032A160`, which stores 0.
  - Seven instructions read it: `0032A150`, `00317680`, `00319220`, `0031967C`, `00319712`, `00319746` and `00324DAD`.
  - No pointer constant and no image-base-relative operand names it, so no save writes or restores it.
- **`0032A160` has one caller**, `00237E37` in `00237DF0`, and that tail is branch-free to the `ret` (K2).
- **`00237DF0` has six entry sites over four routes** (K3):
  - the lazy bind `00233C10`. When the block is null it runs the reset twice (`00233C3F`, `00233C48`); on a stamp
    mismatch it runs it once (`00233C59`);
  - the save-image reset `002EF650` → `00238A80`;
  - area initialisation `002342F0` → `00239960`, when byte `0208D455` is −2 (`00239982`). Verb `302B`
    `btlAtelSetNextSetSaveData` (`0050F81C`) and the slot-0 restore (`00584482`) write that byte;
  - verb `7055` `fsttl_initialize` → `00394460`.

  A load enters through `SaveLoad_ControllerLifecycleHandler` → `00285E60` (`00582CD0`/`00582CE6`) → `00233C10`, so a
  load restarts the counter only when the stamp mismatches.
- **The stamp `+0x0C`** is the counter divided by `(int)(30 × [01DFE0B8])`, stored at `00300829` (K4). The initialiser
  zeroes it only for an uncommitted entry (`002395E3`/`002395E7`, `00239657`).
- **A restart keeps the stamps** (K5).
  - `00237DF0`'s own body addresses neither the banks nor `+0x0C`.
  - Its loop hands `0023AC80` an index below `0x28`, so that function takes its kind-0 arm.
  - Its chained-`.pdata` closure has 2,156 functions, with 843 indirect sites not followed. In that closure the only
    bank-pointer touch is a read, `0023612D` in `00236100`.
  - `002395A0` is unreachable from it. `00300530` is reachable only through the refill `0030F340`, which passes
    `max − current` (`0030F3C2`–`0030F3DC`).
- **Executed under Unicorn 2.1.4** (K6). It runs `00235FB0`'s whole body with `0031B760` answered by a hook,
  `00300530`'s stamp tail, and the selector's seconds and gate:
  - one clock: the stamp is 40 and elapsed is 60. The script's `>` holds and the gate admits;
  - **a restart below a kept stamp** (stamp 40, 5 s later): the accessor returns **−35**, and the selector's unsigned
    `jb` (`002358D7`) **admits at once**. The scripts' signed `>` first holds at **second 71 = stamp + cooldown + 1**
    of the new clock;
  - stamp 1 at counter 0 returns **−1**, which is the accessor's own failure value (`00236020`);
  - scale 2.0 gives the same outcomes.
- **A slot-0 load imports the saving session's stamps into bank 2** (K7, and the respawn page). `00233550` copies
  0x128 × 0x80 bytes, structure-blind. The rotation can then make them current.

**Sensitivity controls** (each turns a check to FAIL; all four did):
- S1: `jb`→`jl` at `002358D7`;
- S2: `0032A160`'s store replaced by NOPs;
- S3: the stamp store moved to `+0x10`;
- S4: the claim "elapsed is never negative after a restart".

## Side findings (FABLE)

- **`00394130` is not orphaned.** `00394640` registers it with `lea rdx, [00394130]` at `0039464D` and then calls
  `00244F50`. This is the `fsttl_newgamestart` path that the SetSaveData page answered on 2026-09-11.
  `CONTRACT-battle-runtime-mode.md` line 462 still says "fully orphaned — zero callers, zero stored pointers, zero
  `lea`". That premise underlies its "moot" note about `00394130`'s pre-init calls (line 460) and its "dead code" note
  about the two `002EF650` sites. K3g is the check.
- **The host contract's §10 note says `0032A100` "increments it once per `00234590` frame".** The increment is
  conditional (`0032A12A`–`0032A133`), so the correct wording is "at most once per frame". The world-tick page already
  states the condition. §10a states it too; the inline note is OPUS's, so it is not edited here.
- **`rawref.py` fix.** Outside `.pdata` (leaf functions), the parent's helper accepted the first decode that spanned the
  site, even a misaligned one. That missed `0032A160`, and it read `00317680` / `0023612D` one byte late. The copy here
  decodes linearly from the leaf's padded entry first. **The other three `fable-l2exp-*` packages carry the unfixed
  copy.**

## Consumer check (FABLE)

affected: Database/FFXII TZA/05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md

- consumer: `05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md` — **revised-here**. §10a is inserted by
  `apply.py`. §4, §10's clock box and §12's formula are unchanged, and they agree with G9: the formula is the same, and
  G9 states its domain. The §10 inline note's "once per frame" is **routed-to-OPUS** (side finding 2).
- consumer: `05-Spawn-Encounter-Lifecycle/why-the-enemies-you-killed-come-back.md` — **agrees**. Its L83–113 table says
  the counter is never restored and is zeroed on the guard's null or mismatch path. §10a adds three more reset routes
  and the cooldown consequence; it contradicts nothing there.
- consumer: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md` — **agrees** (§13: `0032A160` has one caller and the
  tail is branch-free; the EXP-080 counter 0 at "Load complete" is cited as consistent, not as a capture).
- consumer: `05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md` — **agrees** (`+0x0C` writers
  `00300530` and `00239657`; readers `00235FB0` and `002358D1`).
- consumer: `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` — **agrees** (the automatic selector's
  `elapsed ≥ cooldown` gate; §10a adds that the gate is unsigned).
- consumer: `_index/L2-VERDICTS.md` (S-17 row, contract cell) — **routed-to-OPUS**. With §10a applied, the narrow
  SCOPE-SHORT item ("the clock-across-load interaction … neither states nor bounds") is stated and bounded. The cell is
  OPUS's to re-score.
- consumer: `00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md` — **routed-to-OPUS**. Line 462,
  "`00394130` is fully orphaned", is refuted at `0039464D` (side finding 1). No lane is named on the page; the routing
  follows the audit's contract-ownership mapping, and the receiving lane should forward it if that mapping is wrong.

run: check_s17.py at e1b42c48b (K1–K7 PASS, S1–S4 sensitivity controls PASS, FAILS 0; Unicorn 2.1.4, image 73461d08…; apply.py dry run FAILS 0, contract +88 lines, LF kept). This publish touches only the host contract; every other consumer above agrees or is routed.

## What is not settled (FABLE)

- **Static closures are over-approximations, and they are also incomplete.**
  - 843 indirect call/jmp sites in `00237DF0`'s closure are not followed.
  - It is not traced whether the reachable `00236100` callers (through `0023AC80` → `0031A630` → `00324470` →
    `00300E40` → `0023A570`) run during a reset.
  - The refill route to `00300530` is not executed.
- **Which routes fire in ordinary play** is not measured: how often a load's bound block mismatches, whether `302B` ever
  posts −2, and the title and new-game entry order.
- **The selector's other gates were not executed**: the death limit `+0x0A`, the range checks, and the per-channel
  loop past `002358DD`. K6 runs only the cooldown gate.
- **Nothing is live.** The player-visible effect, an entry respawning at once through the selector while the scripts
  wait stamp + cooldown + 1 seconds, is a prediction. A carrier would record a stamped death, force a restart (title →
  load with a mismatched block, or a new game), and watch `+0x0C`, `0208D45C` and the entry's re-admission.

## How to apply (FABLE)

`python apply.py` is the dry run, and `python apply.py --apply` writes. Applying needs the contract clean
(`git diff HEAD`). The last dry run, at HEAD `e1b42c48b`, printed **FAILS 0** (`apply_dryrun.out`).
