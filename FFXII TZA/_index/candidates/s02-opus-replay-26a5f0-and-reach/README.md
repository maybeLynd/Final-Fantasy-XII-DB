# S-02: `0026A5F0` executed as shipped code, and the per-request reach table measured (OPUS, 2026-09-25, block 287)

**Evidence class: NATIVE-REPLAY (original-code emulation, unicorn 2.1.4), `live_game: false`.** This was executed by
OPUS on a **copy** of EXP-191's harness. The published harness
`_experiments/evidence/s02-world-tick-stop-registry-exec/check.py` is untouched. This is not an ORACLE EXP. It is
offered to ORACLE for adoption and to SWE2-AUDIT-SEM for scoring. OPUS does not award its own acceptance.

## What was run

`check_patched.py` is EXP-191's `check.py` plus four changes:

1. **Block 263's patch** (`../s02-oracle-harness-patch/pending_oracle_s02_26a5f0_case.py`): a `pokes` fixture hook
   and the case **`wt-latch-store-real`**.
   - Entry `00314410`, `rcx = 9`, latch `-1`, drain mask `0x3`.
   - **`realbodies = {0x26A5F0}`**, so `0026A5F0` and its call-free callees `002E15D0` / `002E1690` run as shipped
     bytes.
   - The mailbox is pre-seeded non-zero, so every clear is observable.
2. **Block 266's patch** (`../s02-oracle-harness-patch/pending_oracle_s02_ss7_reach_table.py`): 28 cases
   `ss-record-id-NN`. Each enters `00227680` with `rcx = id`, `rdx = REG + id*0x18` and `r8 = REG + 0x2A0 + id*0x18`,
   `00226BE0`'s own call (`00226C27`..`00226C72`). Each records the built records A / B and
   `reach = (~(A >> 30) & 2) | 1`, the arithmetic of `00226C77`..`00226C94`.
3. **Instrumentation only**: two notes per record case.
   - `calls=`: the harness's scripted-call list.
   - `entered=`: every `functions.tsv` entry point the case executed, other than the case entry.

Inputs:
- EXE SHA-256 `73461D08…D89721F8`. The harness asserts it.
- `check_patched.py` SHA-256 `f505cf1e…6598ebdb`.
- The `result.json` here is from the third of three identical runs.

## Result: 61 / 66, identical over three runs

**All 37 of EXP-191's own cases still pass.** The new cases:

| case | result | what it shows |
|---|---|---|
| `wt-latch-store-real` | **PASS**, no fault, no scripted `s26a5f0` call | Every predicted effect holds on shipped bytes: latch = 9; drain mask = `0x3 | 0x10`; `b[0215F1A0] = 0`; `b[0215F1A1] = 1`; `d[0215F1A4] = d[0215F1A8] = 0` |
| `ss-record-id-01..11, 14, 16, 18..27` (23 ids) | **PASS**; `calls=[]`, `entered=[]` | Stub-free: `00227680` ran with no scripted call and entered no other function |
| `ss-record-id-00, 12, 13, 15, 17` (5 ids) | fault: a read of address `0x3A` at `00198690` / `001986B0` / `00198670` | These ids leave `00227680`: id 0 through the scripted `002DDC30` and `00182D10`; the others through `00182CD0` / `00182CF0`. They then read through a null global. This is live-state dependent, and **no reach is claimed for them** |

**The measured reach, 23 of 28 request ids: id 11 builds reach 3. The other 22 build reach 1.**

| id | record A (qword) | reach |
|---|---|---|
| 1, 2, 3, 22 | `00000034D4000000` | 1 |
| 4 | `00000024F9040707` | 1 |
| 5 | `00000034EB000000` | 1 |
| 6 | `00000004DB040707` | 1 |
| 7 | `00000024F9044307` | 1 |
| 8, 9 | `00000030BD000060` | 1 |
| 10 | `00000030BF7F6060` | 1 |
| **11** | **`0000002011000000`** | **3** |
| 14 | `00000000BD000000` | 1 |
| 16, 20, 21, 24, 26 | `FFFFFFFFFEFFFFFF` | 1 |
| 18, 19 | `FFFFFFFFFFFCFFFF` | 1 |
| 23, 25, 27 | `FFFFFFFFFFFFFFFF` | 1 |

Record B for every id is in `result.json`.

## What this does and does not establish

- **`0026A5F0` has run real on the WT-4 first-writer-wins path.** L2-VERDICTS names this stub exposure as S-02's
  runtime closer ("`0026A5F0` run real"). Whether that discharges the row is **AUDIT-SEM's call**.
- **SS-7:**
  - **The reach is authored per request id.** Measured on stub-free leaf execution for 23 ids, only id 11 reaches both managers.
  - The reach arithmetic itself (`00226C77`..`00226C94`) is **re-computed by the check, not executed**.
  - `00226BE0`'s per-manager loop is not executed here. It is 1,936 B and calls `00263FF0`, `00358940`, `00359B80`, `003590D0` and `003588B0`, none of which the harness scripts.
- **Correction of OPUS's own staged note (block 266):** "`00227680` makes NO calls" was wrong. The note is corrected
  in place.

## Reproduce

```
python check_patched.py        # needs unicorn; paths to the EXE and functions.tsv are absolute in the file
```
