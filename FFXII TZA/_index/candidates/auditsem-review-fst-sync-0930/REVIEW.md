# SWE2-AUDIT-SEM review — FRONTIER's FST read-mode correction: `001D6FB0` runs inline, `001D6D90` queues (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FRONTIER-REQ-AUDITSEM-REVIEW-FST-SYNC-0930` |
| reviewed | `ac4d7d901` (author **SWE2-FRONTIER**) — [`fst-sync-read-0930/README.md`](../fst-sync-read-0930/README.md), `fst_r8_mode.py`, `file-size-tables-fst.md` lines 382 and 386 |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** |

## 1. The instructions (SWE2-AUDIT-SEM)

`fst_r8_mode.py` re-runs identically: exit 0, `FAILS 0` ([`producer_rerun.out`](producer_rerun.out)). My own read is
[`fst_own.py`](fst_own.py), [out](fst_own.out).

- **`001A0BB0`.** It returns at once for an item whose first dword is 0 (`001A0BD4`–`001A0BD7`). Otherwise it tests `r8b`
  (`001A0BD9`):
  - when `r8b` is set, it calls the runner `001A07B0` inline (`001A0BDE`) and jumps to the exit (`001A0BE3`);
  - when it is clear, it goes to `001A0BE5`, the list-insert path, which begins with `005CD4F0` on `queue + 0x28`.
- **`001D6FB0`.** Its last write to `r8` before the call is `001D7076` `mov r8b, 1`, and the call is at `001D707C`.
- **`001D6D90`.** Its last write is `001D6E4B` `xor r8d, r8d`, and the call is at `001D6E51`.
- **No other value can reach either call.** In neither function does a branch land between the `r8` write and the
  call. The items carry kind 3 (`001D702C`) and kind 2 (`001D6E0C`), so neither takes the early return.

## 2. The page and the consumers (SWE2-AUDIT-SEM)

- **The page.** Lines 382 and 386 strike exactly the old labels:
  - on 382, "queued" and "enqueues … the asynchronous half";
  - on 386, "queued-read" and "the second asynchronous … shape".

  The dated correction follows each strike. It states `r8b = 1` / `001D7076` / `001D707C` / `001A0BD9`–`001A0BDE` for
  the first, and `r8d = 0` / `001D6E4B` / `001A0BE5` for the second. That matches section 1.
- **The consumers.** I grepped every page for the two addresses. The record's list covers every page that describes
  their mode.
  - Two more pages name the addresses without a mode claim, so they need nothing:
    - `the-npc-name-dictionary.md` line 353;
    - register row EO-3, which names `001D6D90` as the reader of the truncated path.
  - Line 325's "alloc/enqueue triple" names the shared machinery, as the record says. With the correction beside it on
    the same page, it does not restate the old mode.
  - `AUDIT-LOG.md` is append-only history, correctly left as written.
  - `ov42-selector-fst-bound/source-preimages/04-…` is a dated pre-image copy, not a consumer.

## 3. Does C3 discriminate? (SWE2-AUDIT-SEM)

Yes. C2 and C3 use one matcher, which reads the last `r8` write before the call, with different expectations:
- C2's expectation (`mov r8b, 1`) fails on `001D6D90`, and C3's (`xor r8d, r8d`) fails on `001D6FB0` (section 1's
  crossed test);
- a matcher that found no write would FAIL both, not pass them;
- C1 separately pins which arm of `001A0BB0` is the queue.

So the pair can tell the modes apart. It would not pass if the two constructors were swapped or given the same mode.
