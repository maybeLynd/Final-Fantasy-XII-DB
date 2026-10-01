# Resource request queue, I1–I7 re-adjudicated against EXP-121 / EXP-128 / EXP-146 (OPUS, 2026-09-25)

**Request:** `REQ-OPUS-QUEUE-CONTRACT-S13-READJUDICATE` (SWE2-ORACLE). **Contract:**
`02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md` (OPUS), read at HEAD. The
worktree carries the uncommitted SECTION-02/08/09 overlay, so the edit follows that merge
(`sections02-08-09-queue-owner-review.md`). The verdicts are recorded now.

**Evidence classes, kept separate:**

- **NATIVE-REPLAY:**
  - EXP-128: 137/137 functional, 123/123 mutants;
  - EXP-121: 27/27 functional, 22/22 mutants;
  - EXP-146: 22/22 functional.

  All stable ×3; scripted boundaries disclosed in the records.
- **STATIC:** the contract's reading, plus the re-read below.

| inv. | statement (short) | verdict | basis |
|---|---|---|---|
| I1 | the builder's free-list displacements are cursor-relative; the slot fields are `+0x58` index, `+0x64` −1, `+0x20`, `+0x28`, `+0x10` next, `+0x18` prev | **STANDS — static; replay consistent, not field-exact** | EXP-146 executed `0032E450` linking all 64 slots, and a clean rerun over a dirty pool. It records the linking, not each field value, so the field list stays a static reading. |
| I2 | the chunked path is taken only while a script BGM stream is active | **CONFIRMED — replay and static** | EXP-146 executed both polarities of the builder's gate. **Re-read here:** the gate `003EB0D0` (called at `0032E656`) walks the `BgmStream` records at stride **0x38** (`003EB0E7`, count 1 at `003EB0EB`) and returns 1 if any record's byte **`+0x31`** is non-zero (`003EB0E0`). So "stream active" is `BgmStream +0x31`. |
| I3 | the 65th request blocks its caller | **CONFIRMED — replay** | EXP-146: `0032E870`'s stall loop ran three real `0032E070 → 0046DFE0 → 0035EA30` passes before taking the injected slot. **Add:** `0032E990` has no empty-free-list guard (a null head faults on `[0x10]`, observed), so the stall in `0032E870` is the only protection. |
| I4 | `id = counter << 6 \| slotIndex`, counter at `01EED498` from 1, wrapping at `0xFFFFFF` | **CONFIRMED for the encoding — replay; the wrap stays static** | EXP-146: `(ctr++ << 6) \| slot_index`, `id & 0x3F` recovers the slot, and `id = 0` reads as failure. The wrap was not executed. |
| I5 | the insertion end is a parameter; tail at both builder sites | **CONFIRMED for the mechanism — replay** | EXP-146 executed `0032E990`'s head/tail link moves. The caller census stays the page's static count. |
| I6 | the offset is truncated toward zero to `0x800` | **STANDS — static** | The `cdq` / `and edx, 0x7FF` / `add` / `and 0xFFFFF800` idiom at `0032E721`–`0032E730`. EXP-146 records that `+0x2C` is re-rounded on the chunked path but does not state a direction, so no replay evidence moves this. |
| I7 | the 256 size-override pointers at `022C51F0` are cleared and never filled | **STANDS — static; not reached by the replays** | `ResourceKindOverrideTable` (0x800 at `022C51F0`) is declared. No EXP writes it. EXP-121's resolver `0032E400` is the lookup side. |

**New from EXP-146, for the contract:** the pump drains to teardown, not to idle. With the pending
list empty it still calls the submit-A read and the `0046DD50` / `003E9780` / `0036FD50` teardown
externals, scripted in the record. That belongs in §7 when the contract is edited.
