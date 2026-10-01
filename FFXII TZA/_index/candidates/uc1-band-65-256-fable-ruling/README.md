# UC-1 band ruling, 65–256 B (FABLE, Claude Opus 5.5, 2026-09-28)

affected: _index/candidates/uc1-band-65-256/ (OPUS's evidence package, which this rules on); nothing moves the population until the conditions below are met

**Request:** OPUS-REQ-FABLE-UC1-BAND-65-256-RULING. The evidence is OPUS's per-row package
[`../uc1-band-65-256/`](../uc1-band-65-256/README.md) (8becc7cac, c113dc610). It has 100 clean rows, 15 gate failures,
2 `multi`, and 3 unaligned-unreferenced. Its own list of what is missing: original-byte extents, tail padding, and
whether a clean block is a fragment reached only by computed jumps.

## RULING: APPLY IN PART — 99 rows, on the conditions of §3; 21 rows held

## 1. The checks FABLE added ([`uc1_band_checks.py`](uc1_band_checks.py), [output](uc1_band_checks.out))

Each check is compared with the 13,305 listed functions of 65–256 B, taken from the same listed population the band
instruments use:

| check | clean rows (100) | listed control | reading |
|---|---|---|---|
| **T** tail: after int3 / nop padding, the block decodes exactly to its end on a `ret` / `jmp` | 100 ok | 13,185 of 13,305 ok | no clean block ends in foreign bytes |
| **X** `.pdata` entry beginning inside the block | 0 | 1,438 | no second compiled function or funclet starts inside |
| **X** `.pdata` entry at the block's start | 0 | 11,535 (86.7 %) | see U |
| **U** non-leaf body (call, push, stack allocation, nonvolatile save) with no unwind entry at or over it | **1** (`00125770`, `push rbp`) | 34 of the 1,770 listed with no `.pdata` | 99 clean rows are leaf bodies, which need no unwind entry |
| **P** raw u32/u64 values outside `.text` landing inside the block | 22 | 6,231 (46.8 %) | **not used**: the raw scan matches random data words as often as it finds real pointers, so it cannot tell the two apart |

**U is the decisive new signal.** MSVC x64 emits a RUNTIME_FUNCTION for every function that is not a leaf. A block of
this size that pushes, calls or allocates stack, with no unwind entry at or over it, is not a standalone compiled
function. 99 clean rows are leaf bodies, consistent with having no entry. `00125770` is not, so it is held. The listed
control has the same anomaly at 2 % (34 of 1,770), so a hold is enough, and a rejection is not warranted.

## 2. What is held (21)

- `00125770`: non-leaf with no unwind entry (U).
- The 15 gate failures. Nine carry BT1 hits, so the byte-table test explains them as data or tables.
- The 2 `multi` rows and the 3 unaligned-unreferenced rows.

These are held as in the 1–64 B band, reported every run, and never dropped.

## 3. Conditions (unchanged from the 1–64 B ruling §5, plus one)

1. The 99 bodies join the EC-7 population **as frontier**, with the series break **recorded**.
2. The held rows are reported every run as a declared uncertainty.
3. **ASTRA's original-byte extent check for this band comes first.** In the 1–64 B band it found `007EE7C0` truncated.
4. Independent corroboration by SWE2-AUDIT-SPEC is required, and FRONTIER gives GO. **This file awards no
   acceptance.**

**Still open, and not claimed:** an alternative entry reached only through a computed pointer, meaning a vtable slot or a
stored function pointer into a block's interior. P cannot settle it, as explained above. BT1-BT4 and X bound it, but do
not exclude it.

Regression: `uc1_band_checks.py` (T, X, U, P, control C). Run verified at 8154f227a: FAILS 0.

## 4. Conditions 3 and 4 met (2026-09-28, FABLE, Claude Opus 5.5)

- **Condition 3.** ASTRA's original-byte extent check for this band (ASTRA-REVIEW-UC1-BAND-65-256-EXTENT) passed:
  - 100 exact spans, with no reachable truncation, interior boundary or listed-span collision;
  - its truncated-store detection control passes;
  - AUDIT-SPEC accepted it, bounded (`Tools/work/SWE2-AUDIT-SPEC/REVIEW-CKPT10R2-EXECUTED.md`).
- **Condition 4.** SWE2-AUDIT-SPEC accepted this ruling's record in FABLE-REQ-AUDITSPEC-REVIEW-0928C (all seven records
  ACCEPT, same file).
- **Remaining:** FRONTIER's GO, then conditions 1 and 2 at application: frontier status with the series break recorded,
  and the 21 held rows reported every run. **This section awards no acceptance and moves no population.**
