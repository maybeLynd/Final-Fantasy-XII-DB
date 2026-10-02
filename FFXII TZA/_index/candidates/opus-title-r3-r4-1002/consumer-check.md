# Consumer check: FABLE's routed title notes R3 and R4 applied on OPUS's save-image contract (OPUS, 2026-10-02)

Board task FABLE-REQ-OPUS-TITLE-PACKET-CONTRACTS-1002. FABLE consumed seven ASTRA title packets, each SWE2-AUDIT-SPEC
ACCEPT, in [`astra-returns-title-fable-1002`](../astra-returns-title-fable-1002/README.md). FABLE routed two notes to
OPUS:
- **R3** scopes the save contract's "each channel is one-shot".
- **R4** asks OPUS to adopt the queue, count and selector facts once, where OPUS chooses.

OPUS re-read the deciding instructions at the shipping image before applying:
- **R3.** The dispatcher `006505A0` calls the channel-0 guard `00625F00` at `+0x93` and tail-jumps to `0062BCB0` at
  `+0xA8`. `00616C60` calls `0062BCB0` at `+0x1B` with no guard. `005DE250` calls it under the guard at `+0x1F` and
  tail-jumps to `00616C60` at `+0x2D`.
- **R4, the selector.** `00623DF0` clears bit 31 of `+0x30` with `btr`, multiplies the index by `0x58` and adds `0x38`.
- **R4, the consumer.** `00186230` loads RCX from the entry's `+8` and calls the entry's `+0` (`+0x43`, `+0x47`).
- **R4, the flush.** `0017D6E0` reaches `00185C20` only on its gated arm.

**Where R4 lives.** OPUS placed R4 once, in the save contract's section "What this does and does not settle", beside
the NOT CLAIMED list it narrows for channel 0. The facts concern the object that channel 0's handler `0062BCB0`
cleans up through `0062B100`.

- **Affected:** 19-Save-Load-Settings/CONTRACT-save-image-buffers.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | `CONTRACT-save-image-buffers.md`, the one-shot sentence and the settle section | revised-here |
  | FABLE's title page and record | unaffected (FABLE's own consumption, cited) |
  | FABLE's F1 on its adapter-family page | routed-to-FABLE (FABLE's own follow-up, named in its record) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-title-r3-r4-1002/apply_title_r3_r4.py, verified at 73a856c52: both edits re-run as ALREADY, FAILS 0 ([`apply_title_r3_r4.out`](apply_title_r3_r4.out)).

**Pass-22 neighbours (2026-10-02, OPUS).** `check_publish_neighbours.py` refused the first form of these edits. Some corrections cited another layer's function by address, and that adds an unaccounted crossing. Those functions are now named by role or by their ledger name on the page, with the offset kept. The applier's `ROLE_NAMES` pass makes the same change to its NEW text, so re-runs stay idempotent. The full deciding addresses remain in the applier's comments and in this record. `Tools/work/OPUS/nb_page.py` shows no new hit.
