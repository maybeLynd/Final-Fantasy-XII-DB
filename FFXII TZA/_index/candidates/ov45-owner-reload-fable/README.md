# OV-45: a manager reload releases its source owners in queue order (FABLE, Claude Opus 5.5, 2026-09-29)

**Box (OV-45, `02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md` §"remaining"):**
"Establish external owner replacement/reload and all actual pin/unpin caller obligations." The register classes the "all
callers" universality as superseded under OV-2's limit, which leaves the replacement and reload specifics.

[`reload.py`](reload.py) runs U, I, Q, R, H and E: FAILS 0 ([output](reload.out)). Static. Q and H re-check facts that
[the queue contract](../../../02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md) §5 and
[the queue page](../../../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) (FABLE's 2026-09-12 answer on the
head insert) already state.

**The reload, step by step:**
- **U.** The manager slot unload runs the group deleter over the manager's sixteen source owners:
  - state 1 (prepared, not queued) is freed and cleared;
  - state 3 (queued) goes to 5, and its queued read and callback are kept;
  - state 4 (ready) is disposed.
- **I.** The new payload's bind ends by jumping to the group initialiser, which clears every record and releases nothing.
- **Q.** A full queue blocks: the insert waits, pumping. A request links at the head for flag 0 and at the tail otherwise.
- **R and H.** Only the head wrapper passes flag 0, and its two call sites are both in the BGM stream reader. Every other
  request links at the tail, including the source-owner reads and the manager reload's own loads.

**So the reload is ordered safely.** An owner's read queued before the reload completes before the reload's own requests,
because the pump serves the head in order. Its callback therefore frees the state-5 owner before the new payload binds and
the initialiser clears the records. No late callback lands on a cleared record.

**The pin obligations** follow from OV-34, OV-36 and OV-42. An owner is pinned from preparation until:
- its completion callback unpins it; or
- a deleter frees it (state 1); or
- the callback frees a state-5 owner.

**Residue.** ~~A read that errors never calls back (OV-42).~~ *(Corrected before publication, 2026-09-29: OV-42 is about a submission with no queue entry, not a failed read. `reload.py` E: a failed read calls its completion, with ok = 0, only when the request's byte count is −1 - the insert stores the caller's count at slot `+0x28` (`0032E92C`) and the failure helper `0032E370` tests it - and `003DD850` never reads ok, so it then takes its normal path on bytes the read did not deliver. Any other failed read releases its slot with no callback.)* After such a silent failure the state-5 owner is forgotten by the initialiser at the next
bind. Within the owner code this is not recovered, and a higher-level arena release is not excluded.

**Correction carried in this batch.** The OV-42 record's "a failed queue insert" is corrected: a full queue blocks, and does
not reject (Q).

affected: `_index/candidates/ov42-submit-recovery-fable/README.md` (the Q bullet, struck and corrected)

consumer: FABLE-REQ-FRONTIER-APPLY-OV42-OV19 names "failed queue insert", and FRONTIER is told
(FABLE-NOTICE-FRONTIER-OV42-QUEUE-FULL).

consumer: the queue contract §5 agrees; it already states the stall and the head flag.

run: reload.py at 49adbe4c7, FAILS 0.
