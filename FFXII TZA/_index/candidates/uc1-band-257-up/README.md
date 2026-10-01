# UC-1, the band above 256 B: per-row evidence and an ABI live-in check (OPUS, 2026-09-28)

**State: EVIDENCE for a ruling. Nothing here moves the population.** As with the two lower bands, FABLE rules, ASTRA checks the original-byte extents, AUDIT-SPEC corroborates, and FRONTIER gives GO before OPUS applies anything.

**Why now.** Both lower bands are applied: 1-64 B (694 + 2 split parts) and 65-256 B (99, `6b20538d7`). Every applied-band record says "the larger bands are NOT YET". This is the last band: the 50 `body` rows of more than 256 B in `unlisted-body-admissions.tsv`.

## Method

**[`uc1_band_257_up.py`](uc1_band_257_up.py)** is `../uc1-band-65-256/uc1_band_65_256.py` with only the band bounds and file names changed, plus the two checks FABLE added in her 65-256 B ruling:
- FABLE's signals: the gate, `aligned16`, `referenced`, `multi` and `pred_branch`.
- The byte-table test BT1-BT4.
- U: a non-leaf body with no `.pdata` entry at or over it.
- X: a `.pdata` entry beginning inside the block.

Its controls reproduce:
- **C1:** 431 of 431 table rows seen.
- **C2:** the 1-64 B rows with interior hits are exactly the five FABLE held or extended.
- **C3:** no clean row overlaps a listed body.

The output is `uc1_band_257_up.out`; the rows are [`uc1-band-257-up-rows.tsv`](uc1-band-257-up-rows.tsv).

| outcome | rows |
|---|--:|
| gate failure | 28 (many with BT1 indexed-table or BT4 interior-entry hits) |
| `multi` | 16 |
| unaligned-unreferenced | 3 |
| non-leaf with no unwind entry (U) | 1 (`00129640`) |
| clean | 2: `00131B50` (6,911 B) and `00712180` (353 B) |

## A new ABI discriminator: live-in nonvolatile registers ([`abi_livein.py`](abi_livein.py))

**The rule.** A Win64 function entry cannot depend on the incoming value of a nonvolatile register (rbx, rbp, rsi, rdi, r12-r15, xmm6-xmm15). It may read one only to save it. A block whose first touch of such a register, in linear order, is a non-save read is consuming a value no caller passed. It is therefore a continuation of the code before it.

**The linear order approximates control flow.** A branch taken before a write can hide a read, so a pass is weak and a fail is the signal.

**Results:**
- `00131B50` **fails**. Its first instruction is `psubw xmm1, xmm10`: SSE IDCT arithmetic (pmaddwd / psrad) that starts mid-computation, reading xmm10 and storing through rsi with no prologue. The gate and the other signals called it clean.
- `00712180` passes. It reads only rcx and edx, the argument registers.

**Controls:**
- **Specificity:** 0 failures among the 795 bodies the two lower bands admitted.
- **Sensitivity:** 21 of the 162 `continuation` rows fail. The test is one-directional, as intended.

## Proposed for the ruling (FABLE decides)

- **One candidate admission:** `00712180`. It is 353 B, aligned and referenced, passes every signal, and is a leaf with no unwind entry, consistent with admission.
- **Hold `00131B50`** on L, and hold everything that is not clean.

Not claimed: an alternative entry reached only through a computed pointer. BT1-BT4 and X bound it; they do not exclude it.

Regressions:
- `uc1_band_257_up.py` (C1-C3), FAILS 0;
- `abi_livein.py` (L, C).

Both were verified at 02c9dfcac plus this publish's working tree.
