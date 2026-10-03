# SWE2-AUDIT-SEM re-score: S-16 types PARTIAL -> MET (L2 stays NOT MET on the contract cell)

SWE2-AUDIT-SEM (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Closes the S-16 residual of `auditsem-types-rescore-2-1003`

## SWE2-AUDIT-SEM what changed

The previous re-score left S-16's types cell PARTIAL on two undeclared items that `CONTRACT-spawn-placement.md` names.
Its stated condition was "MET when both are declared". Both are now declared:

- `g_nSpawnKeepReturnWindow` (§5, `0208936C`) is `SpawnKeepWindowSeconds0208936C`, declared by OPUS in `51ad88762`. It is
  census3's S-16 residual.
- The format-class-0 candidate record (§3: byte `+0x00` mode, `+0x10` authored position) is `SpawnCandidateRecord`,
  0x30 bytes, declared by SWE2-STRUCT in `f945d05b2` (record `swe2struct-spawn-candidate-record-1003`).
  - `mode` is int8 at `+0x00`, and `position` is float[3] at `+0x10`.
  - Both were read at the bytes through the copier `003DFD00` and the readers `00234AF0` and `002374E0`.

The types cell is therefore **MET**.

**L2 stays NOT MET.** The contract cell is SCOPE-SHORT: OPUS, 2026-10-03, found that the retirement trigger `002350C0`
and the keep-bank rotation `00233780` sit in no credited contract. Every row whose contract cell is SCOPE-SHORT reads L2
NOT MET (S-01, S-08, S-21, S-29, S-38; `scopeshort.py`). The L2 cell's reason is re-worded from "the types cell is
PARTIAL" to the contract cell. The L2 count is unchanged at 33 of 52.

## SWE2-AUDIT-SEM checks

- I re-read the two declarations' evidence at the bytes; the full set is in the STRUCT record. `003DFD00` writes mode 0
  at `003DFD6F` and copies the position at `003DFD7F`-`003DFD96`. `00234AF0` reads x/y/z at `00234B5E`-`00234B6C`
  and compares the mode at `00234BC2`.
- The edit is column-precise (`Tools/work/SWE2-AUDIT-SEM/standin1003/apply_s16.py`). It touches the types, L2 and
  binding-gap cells, and strikes only text that is really there.
- After the edit, the shared reader `l2_verdict_table.py` reads S-16 as NOT MET, with no malformed rows.

## SWE2-AUDIT-SEM limits

Static only. The SCOPE-SHORT contract cell is OPUS's to close: it needs a credited contract for `002350C0` and `00233780`.
