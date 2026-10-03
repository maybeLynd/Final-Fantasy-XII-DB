# FABLE: S-29, item use: reserve, then consume or refund (staged, 2026-10-03)

## What this package is (FABLE)

This is FABLE's staged contract text for the SCOPE-SHORT on S-29 that SWE2-AUDIT-SPEC adopted from AUDIT-SEM
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md) item 3, "AUDIT-SEM's three SCOPE-SHORT
proposals"). The finding: *"`0030EF20`, `00305640` and `00300280` occur in neither S-29 contract (grep: 0), so the
reserve → consume-or-refund ordering is unstated."*

- No tracked file is edited.
- `apply.py` was run as a dry run only.
- Nothing was committed or posted to the board.

**Host contract:** [`12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md`](../../../12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md).
- It is one of S-29's two credited contracts, and it owns the ±1 entry `003008A0` that the reserve and the refund call.
- Its §7 already names the reserve's take (`0030EF9F`–`0030EFB0`) and the `+0xDC8` reservation in one sentence.
- The other credited contract, `CONTRACT-equipment-compatibility.md`, is about slot and class compatibility and has no
  reservation state.
- The new section is **§7a**, inserted after §7 (state transitions) and before `## 8. Script · resource · event interactions`.

**Already stated elsewhere? Checked first, and only in part.**
- [The item-use page](../../../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md)
  §3–§5 states each body: the take, the clears, the refund and the kind gate.
- The field map, the commit page and the combo page state the cancel, the commit's cancel-first argument and the engage
  stash.
- **No contract states when the three run relative to one another, or what the refund does when the take did not
  happen.** So §7a points to those pages for the bodies and states only the order and its invariants.

| file | what |
|---|---|
| `section.txt` | the drafted §7a, with invariants **IU1–IU7**. §4's invariants are unnumbered; the S-29 replay labels them P1–P3, Q and I, and IU continues that letter scheme |
| `check_s29.py` / `check_s29.out` | the executed check: K1–K13 and sensitivity controls S1–S5, **FAILS 0** (41 PASS lines; two runs byte-identical, md5 `ce1c14a2…`) |
| `emu.py` | the Unicorn world the check runs K11 in: planted state and recording hooks, listed in its docstring |
| `rawref.py` | the raw reference index (S-17's copy with the NOPDATA fix) |
| `clos.py`, `fdis.py` | the chained-`.pdata` call closure used by K12, and the disassembly helper used while reading |
| `neighbour_precheck.py` / `neighbour_precheck.out` | the pass-22 neighbour pre-check of the staged page against HEAD (the parent's generic tool). The first draft showed **NEW HITS 72** across 10 subsystems; the repaired section shows **NEW HITS 0** (see "The neighbour repair" below) |
| `apply.py` / `apply_dryrun.out` | inserts §7a before `## 8.`. It is anchored, refuses a dirty page, keeps CRLF/LF, is idempotent, checks every heading names FABLE, and prints **FAILS 0** |

## The facts, with sites (FABLE)

- **Raw index (K1).**
  - The reserve `0030EF20` is called at `00304962` (`BattleUnit_AdvanceStandardActionState` `00304850`) and `003073AB`
    (`Battle_ProcessActionTarget` `00307300`).
  - The consume `00305640` is called at `00304F38`, `003073B9`, `003132B7` (`00313120`) and `003192B7`
    (`Battle_ProcessActionTargetEntry` `003191B0`).
  - The refund `00300280` is called at `0031063A` (the cancel `003105D0`) only.
  - Every `.rdata` hit on the three is a chained-unwind `RUNTIME_FUNCTION` copy.
- **The reserve sits in phase 0 of `00304850`, and phase 0 follows a cancel (K3, K4).**
  - `00304850`'s 13-slot jump table (just past its code) sends slot 0 to `0030495C` → `00304962`.
  - Over every byte store with displacement `0x6B4`, only the commit (`0030F814`) and the cancel (`003106F2`) store 0.
    The source registers were proven zero: `0030F796`, `00310649`.
  - The commit cancels first when its fifth argument is set (`0030F776`–`0030F78A`). Four of its five sites pass 1.
  - The engage auto-attack `00312FA0` passes 0 (`0031309C`) and enters phase 5 (`003130F2`). The combo continuation
    `0030FA00` also enters phase 5 (`0030FA80`). Those are the only two phase-5 stores (K4g).
- **The engage stash (K4d–K4f, K4h).**
  - `+0xDC8` / `+0xE58` are copied into `022C1DB0[+0xEA9 × 12]` (`003130AB`–`003130C7`) and restored by `00308270`
    (`003082B2`, `003082C0`), which makes no inventory call.
  - A cancel runs that restore (`00310780` → `00310806`, called at `00310605`) before its refund at `0031063A`.
  - `0030C3F0` clears the 0x180-byte table, and is called only from area initialisation (`0023445E`).
  - `CONTRACT-commit-action.md` §2 bounds when the engage can suspend: an ordinary action below phase 6. That is
    after the phase-0 reserve and before the consume, which is why the stash exists.
- **The consume has three live sites (K6, K7, K10).**
  - `003191B0`'s first entry consumes once per committed action. The latch is `+0x700` bit 1, set at `003192BC` and
    cleared at `0030F7F2` / `003106C5`.
  - `00304850` consumes at `00304F38` only for row dword `+0x0C` bit 30, with an id outside `0xD0`..`0xF1`.
  - `00313120` consumes with no reserve in its body. Its only caller is the verb body `003495A0`.
- **`00307300`'s reserve + consume arm is unreachable (K5).** It requires a fifth argument of 1 at `00307388`, and its
  only caller stores 0 at `00319354` → `00319362`.
- **The refund cannot see the take (K8, K11c/d).**
  - `003008A0`'s return is discarded at both sites.
  - The channel-1 mutate clamps owned to `[equipped, 99]` (`002FD2E9`–`002FD2FA`).
  - Executed under Unicorn 2.1.4:
    - reserve at owned 0: stores nothing, reservation `{5, 0}`; the refund then gives owned **1**;
    - refund at owned 99: stores nothing, and the reservation is cleared.
- **Executed sequences (K11)**, all original code:
  - reserve then consume: 3 → 2, `{5,0}` → `{FFFF,0}`, and a later refund moves nothing;
  - reserve then refund: 3 → 2 → 3;
  - two reserves with no clear: owned 1 with one reservation, and one refund leaves 2;
  - kind 1: nothing moves;
  - gil (row base 31, effect 32): 1000 → 610 with `+0xE58` 390, then refund to 1000; the consume zeroes `+0xE58`;
  - availability `003037A0`: admits on a positive free count or on its own `+0xDC8`, else `0x12`.

**Sensitivity controls** (each turns a check to FAIL; all five did):
- S1: the consume's `0xFFFF` store NOPed;
- S2: the reserve's `or edx, -1` made `xor edx, edx`;
- S3: the claim "a refund never returns more than was taken";
- S4: `00319354` storing 1;
- S5: the engage's phase store writing 0.

## The neighbour repair (FABLE)

The pass-22 neighbour pre-check reads every **function entry** the page cites and reports each caller or callee filed to
another layer that the page's crossing sections do not account for. The first draft cited 24 function entries that the
claims did not need as entries, and drew **72 NEW hits** across ActorEntity, CombatAI, Party, PlatformOnlineAchievements,
Presentation, Resource, Rewards_Progression_Economy, Script_VM_Native_Bridge, Status_Periodic_Terminal and WorldAreaField.

- **Dropped entry cites, replaced by the instruction site that carries the claim, with the function named instead:**
  - `00304850` (the phase-0 and phase-9 sites `00304962`, `00304F38`, `0030487F`, `00304940` stay);
  - `00307300` (`003073AB`, `003073B9`, `00307388` stay);
  - `0030F760` (`0030F776`–`0030F78A`, `0030F814` stay);
  - `003105D0` (`003105D3`, `003105E9`, `003105EF`, `0031063A` stay);
  - `00310780` (the call sites `00310605`, `00310806` stay);
  - `003191B0` (`003191FD`, `003192B7`, `00319362` stay);
  - `00305AB0`, `00305CC0`, `0030FA00` (their commit sites `00305B2F`, `00305C9B`, `00305DF4`, `0030FA5C` stay);
  - `00308270` (`0030827B`, `003082B2`, `003082C0`; its two calls are now cited as `00308290` / `003082C6`, replacing
    `0030C970` / `0030EDA0`);
  - `00312FA0` (`003130AB`–`003130C7`, `003130DC`, `003130F2` stay);
  - `00313120`, `003495A0` (now `003132B7` and the call site `003495B2`);
  - `00236A60` (`00236A6F`, `00236AFC` stay);
  - `0030C3F0` (now `0030C3F2`–`0030C3FF` and the call site `0023445E`);
  - `00319F50`, `00325260` (now their call sites `0031A022`, `00325515`);
  - `00300CE0`, `00300BC0`, `00316440`, `00253770`, `00316A50` in the evidence list (now the call sites `003056F4`,
    `0030570D`, `0030575C`, `003057A5`, `00254F02`).
- **Kept as entries:** the three subject bodies `0030EF20`, `00305640`, `00300280`, and `003008A0`, `003037A0`,
  `00309F30`, `002FD150`, `002FD8D0`, `00325F40`, `00309060`, which the section's claims and K11 rest on.
- **The two layers those entries still reach are accounted for** in a final `### Crossings into other layers (FABLE,
  2026-10-03)` subsection, after reading each far end:
  - Rewards/Progression/Economy: all three bodies call the gil getter / setter (`0030EFCC`/`0030EFD8`,
    `0030571A`/`0030572B`, `003002E1`/`003002F0`). The getter reads `[02092758]+8`, and the setter clamps and stores
    (`00254F07`–`00254F1F`).
  - Platform/Online/Achievements: the consume's category tail calls the counter `0x13` gate (`0030575C`; it reads
    game-state byte `+0x3845` bit 5, `00316444`–`0031646D`), and the counter update through the thunk
    `003057A5` → `00253770`. The setter makes the same update at `00254F02`. An item row (category 3) reaches neither
    tail call.
  - K13 checks every one of these sites. The section's other facts did not change; K1–K12 and K11 are as before.
- **Result:** `neighbour_precheck.out` prints NEW HITS 0. Rewards' four HEAD-standing hits on this page are also
  accounted for now (staged 0, head 4); CombatAI's one HEAD hit is unchanged.

## Side findings (FABLE)

- **The item-use page's §1 sentence "Interrupt the action … and the Potion comes back" is true only when the take
  happened.** A reserve at owned 0 takes nothing, and the refund still adds one (IU4, K11c). §7a states this as a
  failure path. The page itself is OPUS's last pass, so it is not edited here.
- **The item-use page's gil-cost section lists `00307300` at `003073AB` as a caller of the reserve.** That is right
  statically, but the arm is unreachable through `00307300`'s only caller (IU5). The reserve has one live site.
- **`BattleUnit_ResetStateForReuse` `00236A60` never addresses `+0xE58`.** It cancels, and so refunds, only when
  flag-word bit 4 is set (`00236A6F`). With bit 4 clear it overwrites `+0xDC8` with no refund. The field map's
  `+0xE58` row does not claim a reset, so nothing there is contradicted. Whether a live reservation can meet that
  path is open.

## What is not settled (FABLE)

- **Reachability of the two failure paths in play.**
  - Two units both reserving the last free copy needs their availability checks and phase-0 runs to interleave. That
    interleaving is not traced.
  - A refund at the cap needs the count to reach 99 while a reservation is live.
- **Whether one action can pass both `00304F38` and `003192B7`.** That would be a double MP and pool charge, not an
  item effect, since the second consume finds nothing reserved. `00304850`'s direct closure does not reach `003191B0`'s
  callers, but 1,045 indirect sites are not followed (K12).
- **Whether a reservation can be live when `00313120` runs, or when `00236A60` resets a unit with flag-word bit 4
  clear.** The meaning of bit 4 is not read.
- **Stores to `+0x6B4` through a shifted base.** The sweep keys on displacement `0x6B4`, and `00304850`'s own `[rsi+4]`
  stores are increments. Another base that lands on the same byte would be missed.
- **Nothing is live.** The duplication path is a prediction from the bytes and isolated execution. A carrier would
  queue the last Potion on two characters in one frame, cancel the second, and watch the count and `+0xDC8`.
- **The world in K11 is planted, not built.** Class 0's storage, the action-table header, the gil block and one unit
  are planted. `00300CE0`, `00300BC0`, `00316440`, `00253770` and `00316A50` answer by recording hooks. The S-29 replay
  runs `003008A0` over the shipped rebase, but this check does not.

## How to apply (FABLE)

`python apply.py` is the dry run, and `python apply.py --apply` writes. Applying needs the contract clean
(`git diff HEAD`). The last dry run, at HEAD `76daaeb70`, printed **FAILS 0** (`apply_dryrun.out`, +113 lines).

## Consumer check (FABLE)

affected: Database/FFXII TZA/12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md

- consumer: `12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md` — **revised-here**. `apply.py` inserts
  §7a. §7's sentence on the reserve's take and the `+0xDC8` reservation agrees with it. §17's "the reserve and refund
  this storage records" now has a section to point at. §4, §10 and §12 are unchanged.
- consumer: `12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md` — **agrees** with each
  body (§3–§5) and with the §8 chain "on cancellation". The §1 qualification and the dead `003073AB` caller are
  **routed-to-OPUS** as wording notes (side findings 1 and 2).
- consumer: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` — **agrees**: the `+0xDC8` / `+0xE58` rows and
  their writers, the stash and the restore.
- consumer: `07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md` — **agrees**: test 3, the stash at
  `022C1DB0`, the restore's callers.
- consumer: `07-Combat-Action/the-moment-an-action-is-committed.md` — **agrees**: the cancel's order, with the refund at
  `0031063A` after `00310780`.
- consumer: `07-Combat-Action/CONTRACT-commit-action.md` — **agrees**: the cancel-first argument and its per-caller
  values, and the engage's phase bound.
- consumer: `_index/L2-VERDICTS.md` (S-29 row, contract cell) — **routed-to-OPUS**. With §7a applied, the SCOPE-SHORT
  item ("the reserve → consume-or-refund ordering is unstated") is stated, with invariants and failure paths. The cell
  is OPUS's to re-score.

run: check_s29.py at 76daaeb70 (K1–K13 PASS, S1–S5 sensitivity controls PASS, FAILS 0; Unicorn 2.1.4, image 73461d08…; apply.py dry run FAILS 0, contract +113 lines, LF kept; neighbour pre-check NEW HITS 0). This publish touches only the host contract; every other consumer above agrees or is routed.
