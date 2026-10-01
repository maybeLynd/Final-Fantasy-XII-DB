# OV-40: do callers register already-relocated borrowed bytes again? (FABLE, Claude Opus 5.5, 2026-09-29)

**The question.** Register row OV-40 (box on `02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md`) asks for the "caller policy for re-registration of fresh versus already-relocated borrowed bytes".

The page found that its registration `00409FE0` rebases a borrowed source in place. For a nonempty A00 chunk, the eight encoded fields go through `004304F0`. Disposing the entry and registering the same bytes again would add the offsets twice, and the page left it to the callers to say whether that happens.

**Answer (static, `reregister.py`, FAILS 0).** On a delivered read, no. Every registration on this path is of bytes a read has just delivered, never of bytes it already rebased. There is one exception, the failure callback (F below).

1. **E: one door.** The borrowing context `003B38B0` and the setup `00409A60` are called only from `00409FE0`. `00409FE0` is called only from the thunk `0041E580`, and the thunk only from the four owner-family completions:
   - the indexed owner `003DD850`;
   - the motion cache `003DC340`;
   - the script name-binding `002E4D20`;
   - the per-lane sub-record `002E4E50`.

   See `../ov25-queue-clients-fable/` for the families.
2. **C: a completion runs only as its request's completion.** Each is taken only by the `lea` at its own submit. None is called, jumped to or stored as a pointer.
3. **B: each submit reads into the backing its completion registers.**
   - **B1, the indexed owner:** it reads into owner `+0`'s block, and the completion registers `+0`.
   - **B2, the motion cache:** it allocates a new block on each state-1 submit, stores its handle at slot `+0`, and reads into it. The completion registers `+0`.
   - **B3, the name binding:** it reads into record `+0x10`'s block again, and the completion registers `+0x10`.
   - **B4, the per-lane sub-record:** it submits only a lane whose handle is 0. It allocates that lane's block and reads into it. The completion registers the lane handle, and the lane release frees the block and zeroes the handle first (`../ov25-queue-clients-fable/families.py` L3).

   The queue calls a completion once, after the read that filled the block, then releases the slot ([the queue page](../../../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) §2.3). So `00409FE0` always sees file bytes, whose offsets are still relative. A block kept across loads (B1, B3) is overwritten by the next read before its next registration.
4. **F: the exception.** The failure helper `0032E370` calls the completion when a read fails, with ok = 0, if the request's byte count is −1. The insert stores the caller's count at slot `+0x28` (`0032E92C`). None of the four completions reads its ok argument, so on that path each one registers a block the read did not fill:
   - a fresh allocation for B2 and B4;
   - whatever the block held for B1 and B3.

   Whether that content can be bytes an earlier registration already rebased is not established. That is the one open precondition, and it sits in OV-42's error-recovery ground as much as here.

**What a developer reproduces.** Rebase in place at registration, and register only freshly read bytes. The shipped callers need no "already relative?" flag, because they never hand the registration the same bytes twice after a successful read. A reimplementation that reuses a loaded block without re-reading it must undo the rebase itself.

**Controls.** `reregister.py` E C B F K K2, FAILS 0 (`reregister.out`). K and K2 give the scans and the ok-read detector known positives; the detector flags a synthetic `test r8d, r8d` and passes a write-first body.

**Not claimed (explicit obligations).**
- **Failure-path content.** What the block holds when a byte-count −1 failure calls a completion back (F).
- **The other drivers of 003EDAD0.** The context driver `003EDAD0` has five other callers: `0026FB90`, `002FC4A0`, `003B0660` (the `c_all.efx` loader), `003B2220` and `003B29B0`. They reach the A00 register `003A9A70` outside `00409FE0`, so this record does not cover them. Whether one of them re-runs a context over bytes it already rebased belongs with OV-41's other subtypes and consumers.
- **Authored reachability.** No live run was made.

**Proposed register disposition.** OV-40 → **ANSWERED** for the page's registration path, with the two obligations above kept in the box text. The page is a SECTION carrier, so FRONTIER applies the row and the box.
