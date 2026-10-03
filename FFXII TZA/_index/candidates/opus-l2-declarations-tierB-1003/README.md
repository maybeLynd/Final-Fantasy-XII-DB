# L2 Tier B: seven contract-cited statics declared (OPUS, 2026-10-03)

*AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003 item (a), quality debt for systems whose types cell is already MET: state the
contract BODY names (not cells only an appended interior/update table cites). Drafted by repos-91, a local helper,
with a duplicate check against every proposal under _index/candidates; every row re-read at the bytes by a non-drafting
verifier (28 OK, 5 FIX folded, 0 REJECT). [`apply_decls.py`](apply_decls.py) applies [`decls.json`](decls.json)
([`apply_decls.out`](apply_decls.out)).*

## Declared (OPUS)

| type | system | what the bytes show |
|---|---|---|
| StorageReadState02EAF8E0 (0x10) | S-43 | lastResult int32 (every writer's value: open/close/read/seek/getter) and the read cursor |
| PpfxToneSuffixTable02EA2250 (char*[22]) | S-40 | the I-4 suffix table, filled identically by `0072DAC0` / `0072DCF0` / `0072DFD0` under once-flag `01F3CD60` |
| ShadowPoolV2Slot (0x70 x 32 at `02B3F570`) | S-38 | the V2 shadow ramp pool: handle = (generation << 8) or slot, five ramp channels, flag bytes |
| ResultEventRingEntry (0x20 x 10 at `02EBB560`) + ResultEventRingIndex02EBB54C | S-21 | the post-result event ring the poster `0046AB10` writes after its three early exits, and its index advanced as (slot + 1) signed remainder 10 |
| FramePumpArgWord01E0C2B0 (u16) | S-02 | the frame pump's argument word (image 0xF) |
| SlotIndex01DFE40C (int32) | S-02 | the slot index (image -1); the bounded readers check it against 4, but `0020AE70` indexes `01F832B0` with no bound test |

## What the verifier changed (OPUS folded in)

- SlotIndex: "every reader checks the bound" was false; `0020AE70` (via `001EC670`) indexes without one.
- ResultEventRingEntry: the poster returns early at three sites before touching the ring; `+0x08` is described by what
  the code does (the poster's first argument, passed to `005369C0`), with the contract's name "stats".
- ResultEventRingIndex: `0046ACE1 lea rcx, [02EBB54E]` is a loop end bound for other cells; the extent holds.
- ShadowPoolV2Slot `+0x00`: the pool record's own word indexing the CharacterRenderRecord table, not an "owning actor".
- Unaccessed spans are named `unobservedSpanNNNN` (the store's convention).
