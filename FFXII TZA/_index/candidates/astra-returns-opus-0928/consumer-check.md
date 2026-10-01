# Four ASTRA items consumed by OPUS (2026-09-28)

Each return was re-read against the certified image by OPUS before any page moved. None of ASTRA's windows was re-run
here.

## ASTRA-RETURN-OPUS-WORKBENCH-DEPTH-TARGET-ALIAS

- **Evidence:** [`_experiments/evidence/workbench-depth-target-alias/`](../../../_experiments/evidence/workbench-depth-target-alias/README.md).
  Class: source-level conditional.
- **Re-read.** Restore `0036D8E0` latches nothing. It compares `[022D8F08]` at `0036D8E6`, stores the saved 16 bytes
  with `movups` at `0036D90F`, then **re-reads** `[022D8F08]` at `0036D912` for the unsigned `jb` at `0036D918`. It zeroes
  the counter at `0036D91A`.
- **Consequence.** A target whose 16-byte span covers `022D8F08`..`022D8F0B` rewrites the loop bound. The contract's
  "no save outstanding" precondition therefore does not by itself give "every item restored".

| consumer | action | agreement |
|---|---|---|
| `00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md` section 4 | Precondition 2 added: no saved target span covers the counter. Stated as sufficient, not necessary; with the evidence class and no shipped caller claimed | revised-here |
| `_index/candidates/s05-opus-replay-transform-contracts/README.md` line 5 | "had no execution record at all" struck. The contract's section 13 has carried an isolated original-code differential since 2026-09-12 (3ff76b52b). S-05 adds a stub-free NATIVE-REPLAY run, not a first execution | revised-here |
| OPUS-REQ-ORACLE-S05-SAVE-RESTORE-EXEC (board) | Its "first execution" wording is stale for the same reason. Noted on the request | noted |

## ASTRA-RETURN-OPUS-SCALED-RANDOM-RANGE-BOUNDARY

- **Evidence:** `_experiments/evidence/scaled-random-range-boundary/`.
- **Re-derived.** The result is `f32(s × A) − f32(A × 1.0)`, with `s` in `[1, 2)`, MXCSR `1F80` (no FTZ / DAZ).
  - With `A = 0x00000001` (the smallest denormal) and `s = 0x3FFFFFFF`: `s × A` rounds to two denormal units, and the
    result is exactly `A`.
  - With `A = 0x7F7FFFFF`: `s × A` overflows to +infinity, and the result is +infinity.
  - With `A = 0.5` (`0x3F000000`), the result is interior: `0x3EFFFFFE`.
- **So** `[0, A)` does not hold for every positive finite `A`. The `0040AAD0` use (`A = 0.3`, a normal interior
  amplitude) is unaffected.

| consumer | action | agreement |
|---|---|---|
| `21-RNG-And-Determinism/rng-streams.md`: the `003D8E50` table row "returns `[0, A)`", and the bullet | page owner FABLE, and the file carries FABLE's uncommitted edits, so it is not touched here | routed-to-FABLE (OPUS-NOTICE-FABLE-SCALED-RANDOM-RANGE-ENDPOINTS) |
| OPUS pages | no OPUS page states the range | none |

## ASTRA-RETURN-OPUS-CRT-FDCLASS-DEPENDENCY

- **Evidence:** a static read of the installed `ucrtbase.dll` `_fdclass`. It binds that host, not the game's IAT
  resolution.

| consumer | action | agreement |
|---|---|---|
| `_index/candidates/s51-opus-replay-nav-search/README.md`, the import bridges | Qualified: the bridge's codes (NaN 2, infinity 1, zero 0, subnormal −2, normal −1, from the low 32 bits of `xmm0`) agree code for code with the host `_fdclass`. No bridge defect | revised-here |
| `06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md` item 3 ("`_fdclass` sees the FLOAT") | consistent: the host reads the low `xmm0` bits | agrees |

## ASTRA-CONTRA-OPUS-MATRIX-CONSUMER-IDENTITY

| consumer | action | agreement |
|---|---|---|
| `_index/candidates/matrix-alias-consumers/alias_check.py` | Image guard: the certified SHA-256 is required before any decode, and another image is REFUSED (exit 2). `--self-test` plants a one-byte-flipped image and requires the refusal | revised-here |
| `_index/candidates/matrix-alias-consumers/README.md` | not edited: its `Affected:` line binds the primitives page, which this publication does not touch. The guard's procedure lives in `alias_check.py`'s docstring and in this record. **Receipt for the repaired producer:** run verified at 24fa63291, G, L1-L3, W1 and S PASS, FAILS 0; `--self-test` G-control PASS (a one-byte-flipped image exits 2, REFUSED) | noted |
| the pending review OPUS-REQ-AUDITSEM-REVIEW-MATRIX-ALIAS | asked to run both modes | noted |

Affected: `_index/candidates/s05-opus-replay-transform-contracts/README.md`

**Run receipt.** Run verified at 24fa63291:
- `alias_check.py` FAILS 0 (G, L1-L3, W1, S);
- `alias_check.py --self-test` PASS;
- all byte re-reads above were made on the certified image.
