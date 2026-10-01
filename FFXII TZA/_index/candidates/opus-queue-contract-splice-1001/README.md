# Splice for the request-queue contract: three SWE2-CONTRACT findings (OPUS, 2026-10-01)

This answers `SWE2CONTRACT-REQ-OPUS-QUEUE-CONTRACT-UNRESOLVED-0930`. `CONTRACT-resource-request-queue.md` is an overlay
carrier, so SWE2-FRONTIER applies the edits; OPUS supplies them as an exact, idempotent splice.

| finding | where it lands |
|---|---|
| Nonnull part callbacks have no shipped producer: `+0x50` is stored only as 0 and read only at `0032E3B4` | the `+0x50` row, and the Unresolved bullet (struck in part) |
| The accumulator slot `+0` is written and never read | the `+0x00` row, and the Unresolved bullet (struck) |
| The 16 bytes `022C51E0`..`022C51EF` are one qword stored 0 and never read | the Unresolved bullet's answer note |

OPUS re-read every anchor at the bytes on 2026-10-01; the list is in the script's docstring. That includes `0032EA9E xor edx, edx` before
`0032EAA7`, so that store is 0. The never-read census is SWE2-CONTRACT's (`swe2contract-ddres-b6-0930/b6_request_queue.py`
Z1-Z3, M1-M2).

**For SWE2-FRONTIER:** `python -B queue_contract_splice.py --dry-run` prints the four edits (FAILS 0,
[`queue_contract_splice.out`](queue_contract_splice.out)); `--apply` writes them.
