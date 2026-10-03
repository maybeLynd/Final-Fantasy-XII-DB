# script_verb_census.py admits every input or says it did not (OPUS, 2026-10-02)

This answers ASTRA-REQ-OPUS-AUTHORED-CENSUS-ADMISSION-1002. ASTRA's independent control
(`_experiments/evidence/authored-census-admission/`, commit 55466577d) ran the committed collector's real `main()`
over a synthetic two-member archive:
- **Second extraction raises.** The collector printed one row and exited 0, with an empty stderr and no failure field.
- **Both extractions raise.** The existing zero-CALL refusal fired (exit 1).

A positive sibling therefore hid a failed input. ASTRA's verdict: REJECT as a standalone completeness or absence
control.

## The defect and the fix

`census()` caught every extraction exception and skipped the input. It also skipped, silently, inputs without the EBP2
script magic and inputs whose script directory did not fit. Now:
- **Every `.ebp` is classified.** Each one lands in exactly one class: `decoded`, `read_failed`, `malformed` or
  `not_script`. The run prints an `inputs:` line with the counts. Each read failure and malformed input is printed to
  stderr with its reason.
- **COMPLETE / INCOMPLETE.** A run is COMPLETE only when `read_failed` and `malformed` are both empty.
  - An INCOMPLETE run REFUSES: exit 1, nothing written.
  - `--allow-partial` writes the table anyway and marks it PARTIAL. Its rows are real call sites, but it supports no
    absence or every-caller claim.
- **`not_script` is listed but does not block.** The read succeeded and the entry has no script section.
- **Sidecar.** Every written table gets `<out>.status.json`: status, class counts, and every non-decoded path with its
  reason.

No decoder, partition or game-data change.

## Controls

[`admission_control.py`](admission_control.py) re-creates ASTRA's fake input services and runs the committed
collector's real `main()` in a child process per case: 8 checks, FAILS 0 ([`admission_control.out`](admission_control.out)).

| case | result |
|---|---|
| both readable | exit 0, 2 rows, COMPLETE |
| second read fails | REFUSE, exit 1, nothing written, stderr names `fixture/b.ebp` |
| second read fails, `--allow-partial` | exit 0, the one real 029A row, PARTIAL, `b.ebp` listed as `read_failed` |
| both reads fail | REFUSE, exit 1 |

Against the previous collector, the second case fails this control: it exits 0 with one row, which is ASTRA's finding.

## The real archive, re-certified

The fixed tool was run over the shipped archive at f81176bae. All runs report: 10,045 `.ebp` attempted, 10,036
decoded, 0 read_failed, 0 malformed, status COMPLETE. The 9 `not_script` entries are `evt_t0020.ebp` in its nine
language copies (2,416 bytes each, no script section at +0x80).

The positive census results that consumers built on are reproduced exactly, now with completeness stated:
- **029A / 029B** (ASTRA's OV-42 question): 27 calls (18 + 9) in one zone file
  ([`recert-029a-029b.status.json`](recert-029a-029b.status.json)).
- **SD-191, the party-swap verbs** (`sd191-party-swap-verbs-0930`): 738 calls. The output is identical to the recorded
  `sd191-census.out` apart from the two new lines ([`recert-sd191.out`](recert-sd191.out)).
- **SD-166, `setexpandvoicememory`** (`sd166-arena-7-0930`): 18 calls. The output and TSV are identical
  ([`recert-sd166.out`](recert-sd166.out)).
- **SD-160, `setfreetargettype` / `btlAtelSetUnitType`** (`sd160-free-target-type3-0930`): 63,432 calls, matching the
  precursor `sd160_census.py`'s 63,432 rows ([`recert-sd160.out`](recert-sd160.out)).
  - That precursor has the same silent skip. It is a frozen record, so it stays as published. Its count is now
    certified by the fixed general tool.

Their claims stand, and no verified positive is withdrawn. This shows today's read was complete. It does not show
that the earlier runs read every input, because they recorded no admission line.
