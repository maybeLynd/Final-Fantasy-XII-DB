# AA-8 consumer check (FABLE, Claude Opus 5.5, 2026-09-26)

**Corrected claims.**
1. `persistent-flag-banks.md` §7 said the payload byte `+0x1535` is reached "from the options apply `002DDA30` with
   its own argument". It is reached with the **constant 1**. `ebx` is set by `mov ebx, 1` at `002DDAC4` on every
   path, and nothing between there and `002DDB4A` writes it.
2. `CONTRACT-persistent-flag-banks.md` said `002EF370` stores `cl` and that its **only** caller is the
   session-counter function. The store is `bl`, the first argument copied at `002EF376`. There are **two** callers:
   `002DDA30` (`002DDB4A`, constant 1) and the verb `0x20D1` handler `0050D180`, which tail-jumps with the popped
   integer (`0050D192`).

**Regression:** `payload_tail.py` in this directory, 8 checks, FAILS 0.

## Consumers checked

A grep of the database for `+0x1535`, `0x1735`, `002EF370` and `debug_setscreenmode`:

| Consumer | What it says | Disposition |
|---|---|---|
| `persistent-flag-banks.md` §7 AA-8 | "with its own argument" | Struck and corrected in this publish; box ticked with the answer |
| `persistent-flag-banks.md` §4b field map | `+0x1535  ?  reached through the raw buffer accessor` | Replaced with the answer in this publish |
| `persistent-flag-banks.md` line 999 | `+0x1535` "is reached through the raw buffer" | True; it names no caller or value. Unchanged |
| `CONTRACT-persistent-flag-banks.md` item 3 | "`cl`", "only caller is the session-counter function" | Struck and corrected in this publish |
| `OPEN-QUESTIONS.md` AA-8 | "one store, `002EF370` (from `002DDA30` and verb `0x20D1`)" | Agrees (two callers). Restated ANSWERED in this publish |
| `PARITY-STATUS.md` line 462, `PROGRAM-STATE.md` line 7042 | "`+0x1535` is a written-only byte" | Agrees. Unchanged |
| `the-save-payload-field-map.md` line 195 | `+0x1535`: 1 write, 0 reads, `002EF370` | Agrees. Unchanged |
| `save-payload-accesses.tsv`, `_types/field-access-index.tsv` | the `002EF37D` store row | Agree. Unchanged |
| `scriptvm-verb-marshal-argmap.tsv` / `scriptvm-verb-table.tsv` | `0x20D1 debug_setscreenmode` → `002EF370`, pop 0 | Agree. Unchanged |
| `_types/fields.tsv` `PersistentFlagPayload +0x1534 u8[4]` | the last four bytes, extent closed | Still true. A split into four fields is a types-store task, not made here |

No consumer states the stored value as "the options apply's argument" apart from the two corrected sentences.
