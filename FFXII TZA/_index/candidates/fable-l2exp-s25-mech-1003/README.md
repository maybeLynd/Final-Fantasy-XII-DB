# FABLE: S-25, the gambit set selector and the switch orders (staged, 2026-10-03)

## What this package is (FABLE)

This is FABLE's staged contract text for SWE2-AUDIT-SPEC's **SCOPE-SHORT on S-25**
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md) item 3, concurring with AUDIT-SEM's
proposal): *"the set selector `00305AB0` appears in `CONTRACT-gambit-walk.md` only in §14 (L405, as a caller's
argument shape), and no contract states the selection policy or the command switch in `002FDDA0`"*. No tracked file is
edited. `apply.py` was run as a dry run only, and nothing was committed or posted to the board.

**Host contract:** [`09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md`](../../../09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md).
It is the S-25 credited contract whose subject is the set: it walks one `AiOrderSet` at a subgroup, and the selector and
the switch orders decide which set and which subgroup it gets. `CONTRACT-enmity.md`, the other credited contract, is
about threat. The new section is **§8a**, inserted after §8 (Composition, which describes the chain below the walk) and
before `## 9. Determinism`.

**Already stated elsewhere? Checked first, and only in part.**
- **The set page** ([`which-gambit-set-fires-and-how-a-command-switches-it.md`](../../../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md))
  has the four sets, their roles and installers, the B-skips-C detail, both switch arms and the arm map.
- **The handler-table contract** (HT-2, HT-3, HT-5) states how ids reach `002FDDA0` and what its `-1` means.
- **The host's §14 item 1** states the walk's four call sites and the `+0x6B5` writers.
- **Missing everywhere:** no contract states the cascade's order, the status overrides (Confuse and Berserk) or the
  field-bit-15 skip, the suspension restore at the head of the selector, what the variant arm checks, or what the
  verb route does not check.

§8a cites the page for the roles and states those mechanisms, with invariants **G-§8a.1–G-§8a.7**. The contract has no
invariant ids of its own; the S-25 exposure note cites its claims as G-§n, and the new ids follow that form.

| file | what |
|---|---|
| `section.txt` | the drafted §8a, ending in a `### Crossings into other layers` subsection for the three edges the field-bit getter `00377C20` adds |
| `neighbour_precheck.py` / `.out` | the pass-22 neighbour pre-check of the staged page (`check_page_neighbours.hits`, staged vs HEAD): **NEW HITS 0**. The first run printed 7: 4 from citing the library function by entry (now cited by its store sites) and 3 from `00377C20`'s item and reward callers (now accounted). A preview, not the gate |
| `check_s25.py` / `check_s25.out` | the executed check: K1–K9 static, E1–E16 / W1–W6 / V1–V2 executed, sensitivity controls S1–S7, **FAILS 0** |
| `rawref.py` | the raw reference index (the S-17 package's fixed copy) |
| `fdis.py`, `probe1.py`–`probe3.py` | scratch: disassembly, the raw index over the cited targets, `+0x6F0` writer hallmarks; not part of the check |
| `apply.py` / `apply_dryrun.out` | inserts §8a before `## 9. Determinism`. It is anchored, refuses a dirty page, keeps CRLF/LF, is idempotent, and prints **FAILS 0** |

## The facts, with sites (FABLE)

- **The selector has two callers** (K1): `0030874C` in the combat frame (resume mode 1, `00308744`) and `00313D89` in
  the queue drain (mode 0, `00313D84`). The walk has four call sites, all in it (K2).
- **The cascade, executed** (E1–E14; the walk, the commit, `00377C20`, `002FFCF0` and `00308270` supplied by hooks):
  - bit 22 → `00308270`;
  - the issued command (flag `0x4000` consumed; the band `0x4000`–`0x4166` skips availability);
  - field bit 15 with a party-kind record → no set, the fallback (`00305B3C`–`00305B57`);
  - Confuse, or a kind-1 Berserk, → the static set `01EEC320` alone (`00305B66`–`00305B89`);
  - A `+0x6E8`;
  - party Berserk → `01EEC370` (`00305BB2`–`00305BE5`);
  - then **either C** (stats null, not party-kind, or stats bit 2: `+0x6F8`/`+0x748` cleared, subgroup `+0x6B5`)
    **or B** (fails → cleared → D, never C, `00305C32`);
  - D `+0x6F0`;
  - fallback: in resume mode return 0, else commit `01EEC298` = {`0x4021`, `0x2000`} (`00305C7E`–`00305C9B`).
- **The forced sets decode** as `01EEC320` = {Attack `0x0096` relation 1, `0x4125`} and `01EEC370` = {Attack relation
  1}. Their only other reader is the membership test `0030BF20` (one caller, `00307DC2`) (K4).
- **The switch orders, executed** (W1–W6, `002FDDA0` whole):
  - `0x4116 + k` sets `+0x6B5 = k` for any unit;
  - `0x4112 + k` needs kind 1. Otherwise it returns 1 having done nothing (`002FE50C`). It checks the directory count
    (`002FE06C`–`002FE077`, `-1` past it or on a null directory), installs `+0x6E0` and **zeroes `+0x6B5`**
    (`002FE09F`);
  - a non-zero `+0x6B4` makes every id a no-op returning 1.
- **Verb `3060` `btlAtelSetDefaultLogic` → `00239040`** (V1–V2): it installs `+0x6E0` with no kind test and no count
  bound (V2 reads entry 9 of a one-entry directory), and **keeps `+0x6B5`** (K3b: no operand at `+0x6B0`–`+0x6B7` in its
  whole body).
- **A kind-1 unit gets no D floor from its definition** (K5).
  - `0023A570` splits on the definition kind at `0023A626`–`0023A62E`. The kind-1 arm jumps from `0023AA2A`/`0023AA44`
    to `0023ABCA`, past the `+0x6F0` store `0023ABB5`, and `0023ABA6` is the only reference to `01E09350`.
  - So D stays at the reset's 0 (`00236BB6`), and an enemy whose A and C produce nothing waits (`0x4021`); it does not
    follow (`0x4124`).
- **The suspension pair** (K9, E15, E16).
  - `0030EFF0` (one caller, `0031307B`) copies `+0x6B0`–`+0xB9F` (0x4F0 bytes, which hold every set pointer and the
    subgroup) to a pool buffer, zeroes the block, and keeps the buffer at `+0xB88`.
  - `0030EDA0`, called only from `00308270` (`003082C6`), copies the block back.
  - Executed: after a suspension, bit 22 restores A/C/D and subgroup 4 before the first walk. Without bit 22 the
    selector walks four null sets.

**Sensitivity controls** (each turns a check to FAIL; all seven did):
- S1: `00305C32` jumps to C;
- S2: the field-bit party skip NOPed;
- S3: `002FE09F` stores 5;
- S4: `002FE077` NOPed;
- S5: `0023AA44` routed through `0023ABA6`;
- S6: the claim "every variant switch restarts at subgroup 0";
- S7: `003082C6` (the restore call) NOPed.

## Side findings (FABLE)

- **The set page overstates the D floor.**
  - Its UQ-122 box says *"D `+0x6F0` — the static default set `01E09350` that `BattleUnit_ApplyUnitDefinition` gives
    every unit"*, and *"Every unit's floor is `0x4124`"*.
  - Only the party (kind-0) arm stores it (K5a, S5). A kind-1 unit's D is null, so its floor is the wait `0x4021`.
  - §1's *"There is no path where the unit is left with no decision"* holds outside resume mode only (E12, E8r).
- **The variant-switch premise behind UQ-121 and GR-9 is incomplete.**
  - The gambit page's UQ-121 box says *"Changing variant restarts at subgroup 0, so no subgroup carries across"*.
    GR-9's record (`gr9-order-subgroup-entry-0930`) lists *"a variant switch, which sets it to 0"* among the only three
    ways a subgroup changes.
  - That is true of the order arm `0x4112`–`0x4115` and false of verb `3060` (V1, S6), which installs a variant and
    keeps the subgroup. UQ-121's own sibling-set union check models carry-over approximately, so GR-9's conclusion may
    survive; its stated reason does not.
  - GR-9's "exactly three byte writers" of `+0x6B5` is true for displacement stores. The suspension pair also writes
    the byte (a round trip of the unit's own value).
- **The set page's §2.1 cascade table omits three steps:** the field-bit-15 skip (`00305B3C`–`00305B57`), the status
  sets' triggers (§2.3 lists the two static sets but not that Confuse and Berserk select them) and the bit-22 restore.
  These are additions; nothing on the page is contradicted except the D floor above.

## What is not settled (FABLE)

- **The selector's callees are supplied in E1–E14.** The walk is executed in §13/§13a, and the commit in its own
  contract. E15 runs `00308270` and the restore as shipped, with only `0030C970` supplied.
- **Which party units carry stats flag bit 2** in a loaded game, and so which party members are routed to B and which
  to C. The set page's UQ-123 reads the authored bit from `test_battle`'s `battle_pack.bin` only.
- **What field bit 15 means for a given area.** The DB calls it the per-area waiver for disabling statuses. Here it
  also removes a party unit's whole cascade.
- **Who sets unit flag bit 22**, and whether a selection can run on a suspended unit without it (E16 is a constructed
  case).
- **Whether any shipped script calls verb `3060`** on a unit whose subgroup is non-zero. That is what would turn
  G-§8a.5's carry-over into an observed behaviour.
- **The `+0x6F0` census** is an exact-displacement census plus the two block copies read whole. The ten non-unit
  stores were attributed by function identity (the console, a stack frame, a render-object pair, post-processing, the
  `007C` library), not by a full read of each body.
- **Nothing is live.**

## How to apply (FABLE)

`python apply.py` is the dry run, and `python apply.py --apply` writes. Applying needs the contract clean
(`git diff HEAD`). The last dry run, at HEAD `890844135`, printed **FAILS 0** (`apply_dryrun.out`).

## Consumer check (FABLE)

affected: Database/FFXII TZA/09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md

- consumer: `09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md` — **revised-here**. §8a is inserted by `apply.py`.
  §14 item 1 (the four call sites, the `+0x6B5` writers) and §10 item 1 (a null set returns 0) agree with it and are
  cited, not edited.
- consumer: `09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md` — **routed-to-FABLE**.
  The UQ-122 box's "gives every unit" and "Every unit's floor is `0x4124`" are contradicted by G-§8a.7 (side finding
  1). The rest of §2 and §4 agrees.
- consumer: `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` — **routed-to-FABLE** for the UQ-121 box's
  "Changing variant restarts at subgroup 0" (side finding 2). Section 8h (the issued command, the Confuse and Berserk
  bits) **agrees**.
- consumer: `_index/candidates/gr9-order-subgroup-entry-0930/README.md` (register row GR-9) — **routed-to-OPUS**: the
  premise "a variant switch, which sets it to 0" holds for the order arm only (side finding 2).
- consumer: `07-Combat-Action/CONTRACT-battle-action-handler-table.md` — **agrees** (HT-2: 249 slots; HT-3: the id
  re-read at `002FDDB0`; HT-5: the ambiguous `-1`, which §8a's failure paths name for the variant arm).
- consumer: `07-Combat-Action/CONTRACT-commit-action.md` — **agrees** (§3: `0x4021` is in band 2, so the fallback is
  committable).
- consumer: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` — **agrees** (the `+0x6E0` / `+0x6F0` writer
  lists include `00239081`, `0023A95E`, `0023ABB5` and the restore `0030EDE7`).
- consumer: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md`
  — **agrees** (CB-1: the verb and the order arm read row word `+0x50 + 2k`, and only the arm is bounds-checked).
- consumer: `_index/L2-VERDICTS.md` (S-25 row, contract cell) — **routed-to-OPUS**. With §8a applied, the SCOPE-SHORT
  item (the selection policy and the command switch) is stated. The cell is OPUS's to re-score.

run: check_s25.py at 890844135 (K1–K9, E1–E16, W1–W6, V1–V2 PASS; S1–S7 sensitivity controls PASS; FAILS 0; Unicorn 2.1.4, image 73461d08…; neighbour pre-check NEW HITS 0; apply.py dry run FAILS 0, contract +162 lines, LF kept). This publish touches only the host contract; every other consumer above agrees or is routed.
