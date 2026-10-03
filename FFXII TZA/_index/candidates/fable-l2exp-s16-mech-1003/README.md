# FABLE: S-16, range retirement, the return window and the keep-bank rotation (staged, 2026-10-03)

## What this package is (FABLE)

This is FABLE's staged contract text for SWE2-AUDIT-SPEC's **SCOPE-SHORT on S-16**
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md) item 3, [`item3.md`](../auditspec-l2-expansion-1003/item3.md) "### S-16").
The finding: *"range retirement (`002350C0`, two modes) and the keep-bank rotation (`00233780`, `btlKeepCharWork1/2`) are
documented on `spawn-placement-and-retirement.md` §2 and the keep-entry field map, and in no contract"*. The audit's
own correction adds that S-17's contract states only retirement's ledger effect.

No tracked file is edited. `apply.py` was run as a dry run only. Nothing was committed or posted to the board.

**Host contract:** [`05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md`](../../../05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md).
- It is the only contract the registry credits to S-16, and its title already names the return window (§2's interface
  row, §4 I1).
- The new section is **§7a**, inserted after §7 (state transitions) and before
  `## 8. Script · resource · event interactions`.
- Its invariants continue the contract's own scheme as **I9–I12**.
- It ends with a `### Crossings into other layers (FABLE, 2026-10-03)` subsection, which accounts for the ten pass-22
  edges its citations add.

**Already stated elsewhere? Checked first: described yes, contracted no.**
- The spawn page §2, its §8d Correction 4 and its 2026-09-03 re-derivation describe the gate chain and both modes.
- The respawn page describes the rotation, and the field map describes the entry.
- `grep` over every `CONTRACT-*.md` finds `002350C0` only in S-17's group contract (§6 L222, §10 L342: the ledger
  effect) and in pass-22 neighbour lines. It finds `00233780` only in neighbour lines.
- So §7a points to those pages for description and to the group contract for the ledger. It states as contract what
  none of them states:
  - the one trigger and its gates;
  - that retirement is the only teardown that keeps its mark;
  - that the mark skips the cooldown;
  - the exact restore condition and branch effects;
  - that a reset always breaks the A → B → A chain.

| file | what |
|---|---|
| `section.txt` | the drafted §7a: interface, reads and writes, invariants **I9–I12**, failure paths, evidence class, and a crossings subsection |
| `check_s16.py` / `check_s16.out` | the executed check: K1–K7 and sensitivity controls S1–S5, **FAILS 0** |
| `rawref.py` | the raw reference index (a copy of the S-17 package's fixed helper, unchanged) |
| `neighbour_precheck.py` / `neighbour_precheck.out` | the staged page run through `check_page_neighbours.hits()` against HEAD: **NEW HITS 0** (a preview, not the gate) |
| `apply.py` / `apply_dryrun.out` | inserts §7a before `## 8.`. It is anchored, refuses a dirty page, keeps CRLF/LF, is idempotent, checks that every heading names FABLE, and prints **FAILS 0** |

## The facts, with sites (FABLE)

- **The trigger (K1).**
  - `002350C0` has one caller, `00234022` in `BattleUnit_UpdateLifecycleAndCombatFrame` `00233F70`. The call is on
    that function's ACTIVE branch and passes `rcx = [unit+0x10]`.
  - `00233F70` is named only by `lea r13` at `00265A4F`, which stores it at record `+0x38` (`00265AA8`). The drive loop
    calls it at `0025E222`.
  - The retire's first gate, `002672F0`, returns record `+0x0D` bit 6. The drive loop clears that bit at `0025E1AD` and
    sets it at `0025E217`, just before the call. Unit `+0x10` is the record (`002344EF`, `002134A0`), so the opt-in
    means "scheduled in this pass".
- **Two senses (K2, K7).**
  - **Mode 1** (unit `+0x50` = 1) keeps the unit while an eligible focus slot is strictly nearer than the global range
    `02089368` (`0023527D` `ja`). It retires at or beyond the range.
  - **Mode 2** retires when the leader is within (`jbe`, `002351B9`) the per-unit threshold `+0x4C` of the anchor
    `+0x51`. Any other mode returns 0.
  - The range has two writers, `0023A1D0` (verb `0x300B`) and `0023A520` (43.0, verb `0x3053`), and one reader,
    `00235205`. `00238FC0` (verb `0x3019`) writes `+0x4C`/`+0x51` only for mode 2.
  - Executed: range 43 keeps at 10 and retires at 43 and at 50. An unset range (0.0) retires at 0.5. Threshold 6
    retires at 5 and 6 and keeps at 7. NaN retires in both modes.
- **The mark survives only this teardown (K3, K7h).**
  - `002352A6` sets keep-entry bit 0 before `00300E40(unit, 1)`.
  - `00300E40` clears bits 0/2/7 through `00237080` only when its second argument is 0 (`00300F5D`).
  - Of its **ten** call sites, the retire is the only one that passes 1; the other nine pass `xor edx, edx`.
  - The selector `00235720` admits a bit-0 entry past the cooldown (`002358B9`/`002358BB`), after the death-limit test.
  - Executed: flags `0x03` at the teardown, then `00306E60(unit, 0)`, then return 1.
- **The window (K4).**
  - `0208936C` has two writers (`00236A0D` = 300 in `002368D0`; the setter `0023534A`) and two readers (the rotation
    `002337FA`; the getter `00235330`).
  - The getter's and the setter's only callers are the verb wrappers `00510810` and `005107F0`.
  - The tunables page measures 0 of 1,114 shipped scripts calling `0x306C`. So the window is 300 s in shipped play.
- **The rotation (K5, K6).**
  - It has one caller, `00234423` in `002342F0`, on both arms of `002343CB` and after the reset route `00239960`.
  - It restores only when the field equals `02089372` (two transitions back) and the unsigned elapsed time is at most
    `30 × scale × window`. The restore exchanges **contents**; the pointers stay.
  - A wipe copies bank 1 over bank 2, zeroes bank 1, flips the parity and sets the new parity's 64 counters to 1.
  - Both branches shift the history and stamp the clock. A null bank returns before any of that.
  - The history has three writers: the tail, the reset `00237DF0` (−1, −1, stamp 0) and the slot-0 restore
    `00233550` (field words only). The window and the stamp are never saved.
  - Executed: restore at 9,000 ticks and wipe at 9,001 (18,000 / 18,001 at scale 2.0). A third field, a stamp later than
    the clock, field == last and the reset's −1 history each wipe.

**Sensitivity controls** (each turns a check to FAIL; all five did):
- S1: `ja`→`jg` at `00233803`;
- S2: the compare reading `02089370` instead of `02089372`;
- S3: `jbe`→`ja` at `002351B9`;
- S4: the teardown argument 1→0 at `002352A9`;
- S5: the claim "an unset range never retires a unit 0.5 away".

## Side findings (FABLE)

- **The battle-unit field map labels mode 2 "the ranged retire"** (`04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`,
  the `+0x050` row). It names `+0x4C` `nativeLifecycleRange`.
  - The bytes and the execution (K7) say mode 1 is the range retire, on the global `02089368`.
  - Mode 2 is the approach retire, on a per-unit threshold. That is the spawn page's "POINT retire" and its
    `flLifecyclePointThreshold`.
  - The row's sites are right; only the label is crossed. Mode 3 and above also return 0 (`0023517B`), which the row's
    "0 = none" leaves out.
- **The spawn page's L284 calls `RANGE_REENTRY_PENDING` "the mechanical link between retirement and the return
  window".** Its only native consumer is the selector's **cooldown** skip (`002358B9`). The return window gates only the
  bank rotation, which never reads bit 0.
- **The `rawref.py` copy is the S-17 package's fixed version.** It decodes a leaf's padded entry first, which matters
  here for `00235330`/`0023534A` and `00510710` (all outside `.pdata`).

## What is not settled (FABLE)

- **Which shipped scripts set mode 1 or 2** through `0x3019` `btlAtelSetDeSpawnType` is not censused. So whether
  retirement fires in shipped play, and in which zones, is not measured here.
- **The opt-in bit between `0025E217` and `00234022`.** The calls `00233F70` makes before the retire were not read
  for `+0x0D` writes. A 238-row displacement sweep of byte `+0x0D` was taken, but not narrowed to the actor record.
- **What the teardown's callees write in the keep entry** (`00300FC0`, `003105D0`, `00319E30`, `0023A570`) was not
  read. I10 rests on the teardown's own body and the field map's §2.3 census of bit-0 clearers.
- **Whether the slot release `00234200`** (bit 2, which `00236670` reads) runs after a retirement is not traced.
- **Nothing is live.** The player-visible effect has not been observed: a retired monster re-admitted at once without
  its cooldown, and a `-2` request or any reset wiping the kept bank.

## How to apply (FABLE)

`python apply.py` is the dry run, and `python apply.py --apply` writes. Applying needs the contract clean
(`git diff HEAD`). The last dry run, at HEAD `890844135`, printed **FAILS 0** (`apply_dryrun.out`): the contract
grows by 207 lines and keeps LF. Before publishing, run the real neighbour gate on the batch;
`neighbour_precheck.out` is only its preview.

## Consumer check (FABLE)

affected: Database/FFXII TZA/05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md

- consumer: `05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md` — **revised-here**. §7a is inserted by
  `apply.py`. §1–§7 and I1–I8 are unchanged; I1 (the setter's `cmovs`) is cited, not restated. The front matter's
  `contract:` line and `entries:` still describe placement only. Widening them to name `002350C0`/`00233780` is
  **routed-to-OPUS**, the contract's assembler.
- consumer: `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` — **agrees**. §2's gate chain, both
  modes, the retire action, the tunables and the rotation pseudocode all match K2/K6/K7. The L284 wording (side finding
  2) is **routed-to-FABLE**, as a page edit held out of this publish because it touches only the host.
- consumer: `05-Spawn-Encounter-Lifecycle/why-the-enemies-you-killed-come-back.md` — **agrees** (A → B → A, the unsigned
  window, the parity on both paths, the wipe-only counter fill, and the load table).
- consumer: `05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md` — **agrees**. Its §2.3 lists
  bit 0's setter `002352A6`, its clearers including `00237080`, and the selector test. §7a adds which teardown skips
  the clear.
- consumer: `05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md` — **agrees** (§6 L222, §10 L342:
  the retire unregisters with `edx = 0` and is not a death; K7h executes that call).
- consumer: `05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md` — **agrees** (`0x306C`
  called by 0 of 1,114 scripts; `0x3053` installs 43.0 into `02089368`).
- consumer: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` — **agrees** (§2.4: the
  callback install at `00265A4F`/`00265AA8`, the call at `0025E222`, the bit-6 set at `0025E217`).
- consumer: `_index/candidates/fable-l2exp-s17-mech-1003/section.txt` (staged S-17 §10a) — **agrees**. Its G9d's
  slot-0 bank-2 import is pointed to, not restated, and its reset routes are the ones I12 relies on.
- consumer: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` (`+0x04C`/`+0x050` rows) — **routed-to-OPUS**,
  for the mode-label repair (side finding 1). The page is filed to ActorEntity, and the routing follows the audit's
  ownership mapping; the receiving lane should forward it if that mapping is wrong.
- consumer: `_index/L2-VERDICTS.md` (S-16 row, contract cell) — **routed-to-OPUS**. With §7a applied, the SCOPE-SHORT
  item (retirement and the keep-bank rotation in no contract) is stated as contract. The cell is OPUS's to re-score.
  The S-16 types cell (`arcDeg` `02089358`) is a separate item and is not touched.

run: check_s16.py at 890844135 (K1–K7 PASS, S1–S5 sensitivity controls PASS, FAILS 0; Unicorn 2.1.4, image 73461d08…; neighbour pre-check NEW HITS 0; apply.py dry run FAILS 0, contract +207 lines, LF kept). This publish touches only the host contract; every other consumer above agrees or is routed.
