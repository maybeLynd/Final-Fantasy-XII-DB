# GR-18: reachability of SECTION-03's four synthetic reward edge states, FABLE's own census (2026-09-30)

Register row **GR-18** asks whether the shipped game can reach the four synthetic states that SECTION-03 ran through the
reward computers `002F8BB0` (EXP) and `002F90C0` (LP). The owning page is
[experience and license point award](../../../13-Rewards-Progression-Economy/experience-and-license-point-award.md), §7.

A research record FABLE commissioned, reviewed and publishes (drafted by a read-only helper). It edits no page or register row.

**Evidence classes.** STATIC means original bytes of the pinned EXE (sha256 `73461d08…`, image base `0x120000` included in
every address). DATA means the shipped files on `D:/FFXII_TZA_extract` (332 `.ard`, 9 `battle_pack.bin`) and the
decompiled `us` script corpus (1,114 `.txt`, `Tools/work/FABLE/pub140-scratch/corpus/us/`). Nothing was executed and
nothing was observed live.

**Run:** `python gr18_fable_census.py > gr18_fable_census.out` (about 1 minute). The output ends `FAILS 0`, md5 `643cd952`.
Every count below is copied from `gr18_fable_census.out`.

## Verdicts

| case | verdict | decisive evidence |
|---|---|---|
| **(a)** zero-count or missing reward descriptor | **UNREACHABLE in every area that ships its own `.ard`.** One residual: the 31 `bts_*` battle-test zones | see (a) |
| **(b)** high relocation base | **UNDECIDED.** It needs a run-time write that static reading cannot rule in or out | see (b) |
| **(c)** level-zero reward | **level = baseline: REACHED** (the base row alone, the ordinary case). **level < baseline** (SECTION-03's synthetic `level 0 / baseline 1`): **UNREACHABLE on every writer this census attributes to a stats record** | see (c) |
| **(d)** `0xFF` selector matching a `0xFFFF` stats identity | **UNREACHABLE with shipped data** | see (d) |

### (a) Zero-count or missing reward descriptor

**Code (STATIC, `A-code`).**
- The `.ard` load callback `003EA710` binds header slot 5 (`+0x24`) to `02EBF148` and slot 6 (`+0x28`) to `02EBF140`,
  through `0023A160` index 3 and index 4.
- A slot is bound as NULL only when its header dword is 0 (`003EA7CA` / `003EA7F3 xor edx, edx`).
- Slots 0, 1 and 2 are always bound. So one file supplies all five slots, and the clear path (`003EA8AD`–`003EA8D5`,
  `edx = 0`) nulls all five together.
- The installer `0023A570` checks `+0x22` / `+0x24` with `dec` / unsigned `ja` (`0023A743`–`0023A747`,
  `0023A764`–`0023A768`). A count of 0 wraps to `0xFFFFFFFF` and passes.
- **The enemy-row guard `0023A65D`–`0023A662` has the same wrap.** A count-0 enemy table does not stop an install.
- With the whole registry NULL, the install reads `[0]` at `0023A6B4` (`esi = 0` from `0023A69F`). That fault comes
  before any reward store.

**Data (DATA, `A-data-ch`, `A-data-in`).**
- 332 `.ard` files: 166 in `plan_master/ch` and 166 in `plan_master/in`. They hold 2,292 enemy rows, 1,146 per copy.
- 162 files per copy have enemy rows. Every row's `+0x22` (max 21) and `+0x24` (max 8) selects inside a present,
  non-empty reward table with a nonzero data offset. Row defects: `{}` in both copies.
- The four files without rows are `asp_a`, `dor_f`, `mrm_a` and `slm_a`. In each, slots 2, 5 and 6 are all present with
  count 0.

**Script side (DATA, `A-script`).** Those four files are the only place a zero-count reward descriptor ships, and the
enemy-row guard does not protect them, so what matters is whether anything installs an enemy there.
- The script install is `btlAtelSetUnit` (verb 3001, `00510160` → `0023A3B0`). It installs `id | 0x100` (kind 1), or
  `0xFFFF` for id 255.
- 6,746 calls, all literal, ids 0..27. Id 255 is used 0 times.
- **0 calls in the four empty-table areas.**
- Every id in an area with its own `.ard` is below that area's enemy count, in both copies.
- The two other installers cannot put an enemy there. `00300E40` passes `0xFFFF`, which is kind `0xFF`, and
  `0023A633` returns without installing. `003266C0` is the party-roster refresh; its ids come from party selector words
  and are not traced further here.

**Controls.**
- `A-ctrl`: one mutated `asp_b.ard` each for `index == count`, slot-6 count 0, slot 5 missing and a slot-5 data offset
  of 0. All four are flagged.
- `A-script-ctrl`: an unknown area, an install into `asp_a`, and `id == count` are all reported.

**Residual, with the exact missing fact.** The 31 `bts_*` battle-test zones (`bts_1` … `bts_z`) have script directories
but no `area/*.ard`. They hold 517 `btlAtelSetUnit` calls, ids 0..27.
- The `.ard` is chosen by area number, not by name: `003EA820` indexes file table `0x15` with `2 × area` through
  `0032E400`.
- **The missing fact is which area number, and therefore which `.ard`, is bound while a `bts_*` zone runs. It is also
  unknown whether the shipped game can enter one at all.**
- If no `.ard` is bound, the install faults at `0023A6B4` before any reward store.
- If a populated `.ard` is bound, the table above covers it.
- Only binding one of the four empty-table areas would reach a zero-count reward descriptor.
- This is static work that was not done here, not a live-only question.

### (b) High relocation base

**Code (STATIC, `B-code`, `B-refs`).**
- The resolver `0020E600` is `mov eax, ecx` / `add rax, [01F83530]`.
- `01F83530` lies past `.data`'s raw end `01F7E400`, so it is 0 at image load.
- Over the function list, the only rip operands that name it are the two reads `0020E602` and `0020E620`. The control:
  both known reads are found.
- The loader's relocation `003845F0` rewrites descriptor `+0xC` as a **32-bit** `add eax, edx` (`0038460C`). It does not
  subtract the base.
- **So any nonzero base misplaces every `.ard` read, not just the reward rows.** The installer's 32-bit `imul` / `add`
  (`0023A99C`–`0023A99F`) is where SECTION-03's high base loses its high bits.
- The one known in-image store route into the cell is the texture-id writer `00210570` with id `0xFFFB`. That is CD-2's
  finding, cited and not re-derived here: undriven at the shipped frame width, and never entered in the S-15 boot
  replay.

**Missing fact.** The value of `qword [01F83530]` in a loaded game state, meaning whether run-time state ever drives
`00210570` with id `0xFFFB`. This is CD-2's remainder, carried by `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME` (AQ-ARENA).

**Related variant: base 0 with a table at or above 4 GiB.**
- `003845F0` would truncate descriptor `+0xC` at load, before the installer runs.
- The PE header sets `LARGE_ADDRESS_AWARE=1`, `DYNAMICBASE=0` and `HIGH_ENTROPY_VA=1`. The header alone does not keep
  allocations below 4 GiB.
- The arena behind the `.ard` buffer is CRT-`malloc`-backed
  ([where the game's memory comes from](../../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md);
  cited, not re-read).
- **Missing fact: where the OS places those `malloc` blocks.** EXP-079 saw one process with base 0 and the arena below
  2 GiB.

### (c) Level at or below the `+0x88` baseline

**Formula (STATIC, `C-code`).** `D = u8[+0x1C2] − u8[+0x88]` (`002F8C63`–`002F8C71`).

**The level grower `0030C470`.**
- It zeroes the level (`0030C496`), then grows it to `min(target, 99)`: a signed `cmovg` at `0030C682`, increments only
  (`0030C7B3`–`0030C7BB`).
- For a kind-1 record it stores the baseline as `r8b` (`0030C4B1`).

**Its six callers.**

| caller | level | baseline |
|---|---|---|
| enemy init `0023AD96` | 1 | 1 (`0023AD37`) |
| `btlAtelSetLevel` → `002398F0` | `base + draw % (n + 1)` | `base` |
| `00239BED`, `003069EE`, `00316E3D`, `0031762C` | any | `r8 = 0` |

- The draw from `00328370` is at most 31 bits (`C-rand`), so the added term is ≥ 0.
- `0030C650`, called by the defeat path and the others, only raises the level.
- **So `D < 0` needs a `btlAtelSetLevel` whose base is outside what `min(base + r, 99)` can reach.** The evaluator control
  (`C-eval-ctrl`) shows `(100, 0)` gives `D = −1`, and u8 truncation makes `(300, 0)` give `+55`.

**Data (`C-script`).**
- 6,746 `btlAtelSetLevel` calls, all literal, 234 distinct pairs. Script argument 1 is 1..99 and argument 2 is 0..40.
- Minimum `D` is **0 under either argument order**. No call can give `D < 0`, and none divides by zero (`n = −1`).
- The native pop order is `pop#0 → rdx (n)`, `pop#1 → r8 (base)` (verb marshal argmap). This file does not fix which of
  those is script argument 1, but the verdict holds either way.

**REACHED at baseline.** Under `base = arg1`, 1,102 calls have range 0, so level = baseline every time. The most common
are `btlAtelSetLevel(1, 0)` ×549, `(46, 0)` ×99 and `(45, 0)` ×33. Every other call can also draw 0.

**Writer census (STATIC).** The sweep covers every write-access memory operand off any base register except `rip` and
`rsp` (`rbp` included). It walks 38,957 listed functions plus a linear `.text` pass that decoded 314,036 more
instructions. The full list is in `gr18_store_sweep.tsv`.

- **Width control (`C-sweep-ctrl`).** The qword store `0023ACC2 [rdi+0x50]` covers `+0x54` and is found. The word store
  `0023ACD5 [rdi+0x1C3]` does not cover `+0x1C2` and is not flagged. The grower's three stores are found.
- **Level byte `+0x1C2`: 5 byte/word writers image-wide.** Two are stats writers: `0030C496` and `0030C7BB`. Three are
  not, as read in their bodies:
  - `003AF80F` is the render block's countdown.
  - `003DCF9E` and `003DD177` write word pairs from `+0x178` to `+0x1C2` at stride `0x18`.
- **Spawn-record copies `+0x242` / `+0x108`.** 0 byte/word writers at `+0x242`. At `+0x108`, the two hits in typed
  functions are a matrix and a float.
- **Baseline `+0x88`: 38 byte/word writers image-wide.** Three sit in a function with any stats-record link:
  - `0030C4B1` is the grower.
  - `00329250` and `003298C6` write into a 0xC0-byte output buffer that `00329220` memsets first (`0032923F`), not the
    stats record.
  - The gambit loader's `00327D57` is kind-0 only (`00327CC3`–`00327CCE`).

**Residual.** These writers are not attributed to a type here:
- the other 35 byte/word `+0x88` writers, whose functions have no in-body stats link;
- the 110 wider or indexed `+0x1C2` stores;
- 4,140 `rep stos` / `rep movs` sites.

A whole-record copy moves level and baseline together. No route that lowers the level or raises the baseline of a kind-1
record was found. The verdict is "unreachable on the attributed writers", not a proof over the untyped remainder.

### (d) The `0xFF` selector against a `0xFFFF` stats identity

**Code (STATIC, `D-code`).**
- The divisor loop (`002F8C94`–`002F8CE5`) counts a non-kind-0 record (`002F8CD6` → `inc ebp`) whenever the lookup
  returns one.
- `0031B810(i)` yields the member byte `[frame+0x5A5A+2i]`. Class `0x17` admits 0..8 by constant (`00322FAF`), so for
  i = 0..3 the byte is always used, and an empty member is `0xFF`.
- **So `0xFF` is reached on every empty party slot.**
- `002367A0(0xFF)` compares against `0xFFFF` (`002367E3`–`002367EE`), but only after
  `BattleEncodedId_IsValidForClass(2, 0xFF)` (`002367BC`).
- Class 2 accepts ids from 0 to `[02EBF130]+4 − 1` (signed compares at `0032302E`–`0032303B`).
- `02EBF130` is bound once, from `battle_pack +0x44` (`00236DA0` / `00236DA7`). It is its only `lea` or store among 83
  rip references.

**Data (`D-data`).** `chr_data` is an `st2e` table with **40 rows in all nine language packs** (ch, cn, de, es, fr, in,
it, kr, us). So `0xFF` is refused and returns 0 before the identity compare, and the slot is not counted.

**Control (`D-ctrl`).** Count 256 admits `0xFF`, which is SECTION-03's fixture; 255 and 40 do not.

## Against the earlier OPUS record [`gr18-reward-edge-reachability-0930`](../gr18-reward-edge-reachability-0930/README.md)

This census agrees on (a), (c) and (d), and states (b) more narrowly. OPUS called (b) a runtime fact about `.ard`
placement. Strictly, SECTION-03's edge is a nonzero `01F83530`, which is CD-2's remainder; the 4 GiB placement is a
related variant. Three points in that record need correcting:

1. **E1 skipped the four empty-table areas** (`if not t2 or not t2[1]: continue`). It treated "no enemy rows" as "no
   install". But the enemy-row guard wraps at count 0 (`0023A65D`–`0023A662`), so the case closes only on the script side:
   0 `btlAtelSetUnit` calls in those areas. The E1 figure "0 zero-count" is true only because they were skipped. The
   `bts_*` residual is not addressed there.
2. **E2's "it cannot produce level < baseline whatever they are" is false as a statement about the code.** The target is
   clamped to 99 while the baseline stores `base & 0xFF`, so `btlAtelSetLevel(100, 0)` gives `D = −1`. It is the shipped
   arguments (1..99, 0..40) that exclude it.
3. **E2's writer sweep counted `mov` stores only and excluded `rbp` as a base register.** The wider sweep here finds the
   same two level writers, so the conclusion stands. What changes is the method, and the `+0x88` residual above.

## Files

- `gr18_fable_census.py`: the census with its controls. It uses `retool.py` for the function list and the rip/call index.
- `gr18_fable_census.out`: the run output, `FAILS 0`.
- `gr18_store_sweep.tsv`: every write covering `+0x1C2`, `+0x88`, `+0x242`, `+0x108` and the `+0x54` control, 2,131 rows.

## Publication and routing (FABLE, Claude Opus 5.5, 2026-09-30)

OPUS answered GR-18 at `8fdc9abe5` (record `../gr18-reward-edge-reachability-0930/`) while this census ran. The two agree
on every verdict: (a), (c)-below and (d) are not reached with shipped data, and (b) needs a runtime value. This record is
therefore published as an independent second census, not as a competing answer. Its three method corrections go to OPUS,
the owner of the answer.

affected: `Database/FFXII TZA/_index/candidates/gr18-reward-edge-reachability-fable-0930/README.md`

- consumer: OPUS's record `gr18-reward-edge-reachability-0930` - routed-to OPUS (`FABLE-NOTICE-OPUS-GR18-CORRECTIONS-0930`).
  The corrections are: E1 skipped the four empty-table areas; E2's "whatever the arguments" is false of the code; E2's
  writer sweep was `mov`-only. Also routed: the `bts_*` test-zone residual of (a).
- consumer: register row GR-18 - routed. SWE2-DATA restates OPUS's answer, and OPUS decides whether the corrections change
  its wording. This publish does not edit the row.

run: gr18_fable_census.py at 3cae47364 (FAILS 0)
