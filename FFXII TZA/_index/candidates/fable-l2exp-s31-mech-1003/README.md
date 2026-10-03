# FABLE: S-31, the board grid and the writers of `licenceOwnedBits`, staged (2026-10-03)

## What this package is (FABLE)

This is FABLE's staged contract text for the narrow SCOPE-SHORT that SWE2-AUDIT-SPEC's L2 expansion found on S-31
([`../auditspec-l2-expansion-1003/item3.md`](../auditspec-l2-expansion-1003/item3.md), "### S-31"). The registry
subject is "the licence board and the licence check", but
[`CONTRACT-license-check.md`](../../../12-Items-Equipment-Shops-License/CONTRACT-license-check.md) contracts the check
only. No contract states the board-grid loader, or what writes the owned bits `+0x194` that the check reads.

The repair is one new section, **§8a**, inserted before "## 9. Determinism". No tracked file is edited here, and
nothing was committed or posted to the board. `apply.py` was run as a dry run only.

| file | what |
|---|---|
| `section.txt` | the drafted "## 8a. The board grid and the writers of the owned bits" (interface, state, invariants I6–I10, failure paths, evidence class) |
| `check_s31.py` / `.out` | the executed check: 117 cited instructions, raw reference indexes, the bitmap writer census, 15 Unicorn cases over shipped data, 4 sensitivity controls; **FAILS 0** |
| `census_s31.py` | the displacement census that the check imports |
| `rawref.py` | the raw reference index (E8/E9, 0F 8x, EB/7x, rip, `[reg+RVA]`, `.rdata`/`.data` pointers); the fixed version |
| `apply.py` / `apply_dryrun.out` | inserts `section.txt`; anchored, refuses a dirty page, keeps CRLF/LF, idempotent; **FAILS 0** |

## Already stated elsewhere, and what was not (FABLE)

I grepped the DB for every address first. Nothing below is new to the database as page text, but **none of it is
in a contract that S-31 credits**:
- **The setter `00323910`** appears only as a callee summary, in
  [the construction contract](../../../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md) §13
  (L302–307) and in [EXP-196](../../../_experiments/EXP-196-level-grant-proximity-exec.md). Other contracts name it
  only as a neighbour.
- **The purchase gate `00323D10`** is on [the check page](../../../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md)
  §13 (OPUS, 2026-10-02).
- **The grid loader and its readers** are on [the grid page](../../../12-Items-Equipment-Shops-License/license-board-grid-format.md)
  §3 and [the registry page](../../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md).
- **`resetJobs` → `00328BD0`** is on the stats-record field map (L354).

So a pointer sentence would not discharge the gap. The cross-operation dependency, that the check reads only what
these writers write, has to be stated in S-31's own contract. §8a states it and cites the pages.

## The findings (FABLE)

**1. The owned bits have five code writers, and only two of them touch a single bit** (I6). The bit-level writers
are:
- the setter `00323910`, at `00323A29`;
- the un-learn `00328990`, at `00328A76`.

The bulk writers are:
- the SetSaveData preset apply `00239960`, which zeroes all 46 bytes at `00239C0D`–`00239C39`;
- the definition initialiser `0023AC80`, which `memset`s the record at `0023ACBD`;
- the block clear `002370C0`, which zeroes 0x7410 bytes at `002370CD`.

The save image restores the bits wholesale, because the block is save buffer `+0x4E48C`.

**2. The purchase is the setter with `set = 1`, and no caller ever clears.** All four raw references to `00323910`
pass `R8D = 1`:
- the menu wrapper `003235C0`, whose only caller is `0055DA6E` (`mov r8d, 1` at `0055DA60`);
- the two start-licence loops, at `0023AE7C` and `00239D55`.

So the clear arm has no caller, and **a bit is cleared at runtime only by `resetJobs` (script verb `0x05D6`) or by a
whole-range zero**. That answers the contract's L198 "board-purchase rules" question about who writes `+0x194`. It
does not answer whether four Quickening bits are reachable.

**3. The setter's semantics, executed over the shipped node table** (I7, check X2–X7):
- a silent grant sets one bit and leaves LP alone;
- a charged grant takes `row +4` from LP, floors LP at 0, and still lands when LP is short;
- a duplicate returns −1;
- node 361, kind byte 1 and a null record each return −1 with no write.

**4. Two corrections to recorded text**, from the rank-byte arm (`+0x20`), which EXP-196 records only in part:
- **Nodes 18..30 are inclusive.** `lea eax,[rbp-0x12]` / `cmp eax,0xc` / `ja` (`00323B12`–`00323B18`) puts node 30
  in the `00308FF0` arm. Executed: node 30 → 2, node 31 → 0 (X10). The C2 control fails when the bound is mutated
  to `0xb`. EXP-196 and the construction contract write `[0x12,0x1E)`.
- **The Quickening grants raise `+0x20` to min(count of bits 0..17, 3).** Executed: grants of nodes 0..3 leave it
  at 1, 2, 3, 3 (X9). This happens because `esi` still holds `00324020`'s count at `00323B64`. EXP-196's notes do
  not record it.

**5. The check and the setter agree bit for bit** (I8, X8). `00323BB0(rec, 1, id 1)` returns 0, then 1 after the
setter grants node 182. The C1 control (`bts`→`btr`) fails it.

**6. The board grid** (I9):
- **Loading:** boot `0022A0B0` → `002368D0` (`0022A41A`) clears the twelve slots and requests loader ids `0x47 + k`
  through `00238260` and the resident gate `00233E00`. The twelve generated setters store the buffer pointers.
- **Validation:** none. The magic is unread, which X14 executes. No reader checks the header against the buffer, and
  the header's width and height are the only cell bounds.
- **Readers:** the raw index finds **nine reading functions**. The grid page's list lacks `00560610`, the menu
  minimap pane, which reads the header only. The registry page has `0055BFF0`.

**7. What `resetJobs` takes back** (I10, X11–X13, over the shipped `board_1.bin`):
- every owned square on the record's two job boards whose node row `+7` (the start mask) lacks the slot's bit is
  cleared, and its `row +4` cost is refunded, capped at 99,999;
- start squares and off-board nodes are kept;
- board 12 and the unset selector −1 are refused.

**8. `0208E680`** is the u32 cell that holds the `battle_pack.bin` blob's encoded handle. `003846F0` stores it at
`00384709`, and X1b executes that. This is AUDIT-SEM's UNDECLARED item-1 row; it is described here, not declared.

## Check result (FABLE)

`check_s31.py` printed **FAILS 0** in about 3 minutes, at HEAD `890844135`, with unicorn 2.1.4 (`C:\Python314`). The
full output is in `check_s31.out`.
- **Static:** S1 (117 instructions), S2.0–S2.11 (raw indexes), S2.v (the native-table slot), S2.u (the `.rdata` hits
  are CHAININFO), S3 (39 slot-array sites in 25 functions), S4/S4a/S4b/S4c (the census).
- **Executed:** X1–X15.
- **Sensitivity controls:** each FAILS on its mutated image, as required. They are C1 (`bts`→`btr` at `00323A04`),
  C2 (`cmp eax,0xc`→`0xb` at `00323B15`), C3 (NOPs over the keep `jne` at `00328A68`) and C4 (the last zeroing store
  of `00239960` moved to `+0x1C2`; the census no longer matches its dispositions).

## Consumer check (FABLE)

affected: Database/FFXII TZA/12-Items-Equipment-Shops-License/CONTRACT-license-check.md

- **revised-here:** `12-Items-Equipment-Shops-License/CONTRACT-license-check.md`. §8a is inserted before §9. §3, I1–I5
  and §10 are unchanged and agree with it: the check's read at `00323C18` is the byte the setter writes. §8's "the grid
  format has its own page" stands; §8a states the grid only as far as the check depends on it.
- **agrees:** `12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md` §13. The gate rule,
  the setter's LP floor and cap, and "the kind-1 arm, reasons 2 and 9 are unreachable" all match.
- **agrees:** `12-Items-Equipment-Shops-License/license-board-grid-format.md` §3, with one omission routed below.
- **agrees:** `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`, the twelve-slot paragraph. "At most six
  resident" is not contradicted, but it is not settled at the boot calls either; see below.
- **agrees:** `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`, on `+0x20`, `+0x190`, the
  selectors and `resetJobs`.
- **routed-to-OPUS:** `04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md` L307 says
  `id∈[0x12,0x1E)`; the bytes give `0x12..0x1E` inclusive (X10, C2). The same callee summary omits the
  Quickening `+0x20` = min(count, 3) write (X9).
- **routed-to-SWE2-ORACLE:** `_experiments/EXP-196-level-grant-proximity-exec.md` has the same `[0x12,0x1E)`
  wording. Its note "`id==0xE5`: after the bit set" should say that the hook also runs on the clear path
  (`00323A30` precedes the set test at `00323A4D`).
- **routed-to-OPUS:** `12-Items-Equipment-Shops-License/license-board-grid-format.md` §3. Its reader list should gain
  `00560610`, a header-only reader that the menu atlas documents.
- **routed-to-SWE2-STRUCT:** `_types` declaration of `0208E680` (the blob-handle cell; item 1's UNDECLARED row).
  §8a describes it, and §8a is not a state section, so the S-31 types denominator is unchanged (apply C1/C2).
- **routed-to-OPUS:** `_index/L2-VERDICTS.md` S-31 contract cell. The SCOPE-SHORT item can be re-scored once §8a
  lands; the cell is OPUS's.

run: check_s31.py at 890844135 (FAILS 0; 117 sites, raw indexes, census of 1,319 window writes to 17 route sites and 9 bitmap writers, X1–X15 executed over shipped battle_pack.bin us / board_1.bin in, controls C1–C4 fail on their mutants; apply.py dry run FAILS 0, contract +195 lines). This publish touches only the contract; every other consumer above agrees or is routed.

## What is not settled (FABLE)

- **The resident gate at boot.** `002368D0` makes its twelve requests right after clearing the slots. Whether a
  delivery lands between two calls, so that the "fewer than six set" gate can refuse, depends on the request queue.
  That was not executed.
- **The census bound.**
  - Base-only writes were route-filtered: 393 roots that reference `02EBF190`, `02EBF038` or the board slots, or
    that appear in the record access file.
  - The 30 non-byte index-form writes off the route were listed but not hand-read.
  - Bulk copies are invisible to a displacement sweep. They are named by reading only: `memset` ×2, the 46-byte
    zero and the save image.
- **Not executed:** the `0xE5` hook (`0031B860` → `00324470`); the Quickening action grant `00300B80`, whose id path
  was stubbed; `00308FF0`'s value (stubbed); and the other eight grid readers.
- **Which shipped script calls `resetJobs`, and when.** One decompiled zone script, `rbn_a14` (gitignored corpus),
  contains the call. Its context was not read.
- **Nothing live.**

## How to apply (FABLE)

Run `python apply.py` for the dry run and `python apply.py --apply` to write. The contract must be clean against
`git diff HEAD`. The dry run at HEAD `890844135`:

```
FABLE S-31 section 8a, dry run (no file is written)
HEAD 890844135
PASS  G1  Database/FFXII TZA/12-Items-Equipment-Shops-License/CONTRACT-license-check.md is clean
      line endings kept: LF
PASS  A1  anchor '## 8. Script' occurs 1 time(s) at line 149
PASS  A2  anchor '## 9. Determinism' occurs 1 time(s) at line 154
PASS  A3  8 < 9 and nothing but section 8 lies between them: []
PASS  H1  section.txt's heading is the marker and carries 'FABLE, 2026-10-03'
PASS  E1  8a inserted before line 154 (## 9. Determinism)
PASS  L1  8 relative links in section.txt resolve from the contract's folder
PASS  C1  the census does not read 8a as a state section (state sections: ['3. Types', '5. State'])
PASS  C2  the census's state lines are identical before and after (26 lines)
PASS  K1  125 addresses cited in section.txt; every one is in check_s31.py or listed as carried
      dry run: contract +195 lines
FAILS 0
```
