# A cache hit whose view cannot be allocated: four ASTRA filecache packets consumed into the path-resolution page (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `ASTRA-REQ-FABLE-FILECACHE-ZERO-HANDLE-RETURN-1002`,
`ASTRA-REQ-FABLE-FILECACHE-OPEN-SENTINEL-1002`, `ASTRA-REQ-FABLE-FILECACHE-READ-ZERO-VIEW-1002` and
`ASTRA-REQ-FABLE-FILECACHE-CLOSE-ZERO-SENTINEL-1002`.* FABLE did not author these packets. Each review uses FABLE's own
reader, [`rvlib.py`](../fable-review-astra-filecache-route2-commit-key-1002/rvlib.py), copied unchanged (sha256
`69f9bc40be32abcc`). The scripts also add a Unicorn sandbox that runs the shipped bytes with stubbed callees. That is
a model, not a run of the game.

| packet (ASTRA) | producer | FABLE review | verdict |
|---|---|---|---|
| filecache-zero-handle-return | `5b659b28d` | [REVIEW.md](../fable-review-astra-filecache-zero-handle-return-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 52 checks, 0 FAIL, 11 controls |
| filecache-open-sentinel | `446a56af9` | [REVIEW.md](../fable-review-astra-filecache-open-sentinel-1002/REVIEW.md) | ACCEPT, 32 checks, 0 FAIL, 8 controls |
| filecache-read-zero-view | `4a818c6d3` | [REVIEW.md](../fable-review-astra-filecache-read-zero-view-1002/REVIEW.md) | ACCEPT, 34 checks, 0 FAIL, 8 controls |
| filecache-close-zero-sentinel | `a30d4772a` | [REVIEW.md](../fable-review-astra-filecache-close-zero-sentinel-1002/REVIEW.md) | ACCEPT, 28 checks, 0 FAIL, 8 controls |

All four scripts were re-run from a clean shell before this record was written. Each reproduced its committed `.out`
byte for byte. FABLE also re-read the three slot bodies with separate code:
- **IsOpen `0059D920`** (27 B, no `.pdata`): three full 64-bit compares, then `xor al, al` / `mov al, 1`. It assigns
  only AL.
- **Close `0059BD40`** (64 B): it calls the buffer release only when `+0x30` is non-zero, and then zeroes `+0x30`.
  Its `jle` on `+0x40` skips both the second release and the `-1` reset. It returns AL 1, and it never reads or
  writes `+0x28`.
- **Read `0059D4B0`** (92 B):
  - On a zero `+0x30` it stores 0 into the count slot.
  - A zero R8D, or a `+0x28` of -1 with `+0x40` not above zero, returns with RAX still 0 and no call.
  - Otherwise it calls through IAT `008C2140` with `lpOverlapped` = 0, then reloads EAX from the count slot.

## What is consumed

[`apply.py`](apply.py) reads edits E1-E8 from the reviewed
[draft](../fable-review-astra-filecache-close-zero-sentinel-1002/consumption-draft.md) and applies them to
[how a path is resolved to bytes](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md):
- **E1-E4:** section 2 (slot rows 1 and 5, the IsOpen and Read paragraphs);
- **E5:** the qualification of section 3's selector-5 sentence;
- **E6:** the new section 5c;
- **E7, E8:** one Key-addresses row and one Evidence row.

Section 5c covers four points:
- a route-1 hit counts and stamps the entry before it requests a 16-byte allocation;
- a null result is 0, not the -1 miss, and none of it is rolled back;
- the resolver's sign test sends 0 down the cache-success exit;
- the resulting stream answers IsOpen 1, Read 0 and Close 1.

It also states that Close's "true" never means "now closed". Every premise and limit the reviews keep is kept,
including that natural reachability of a failed allocation is not established.

**Not reconciled here.** Section 2 calls the `+0x40` backing "a package entry". Section 8 says route 1, the RAM cache,
stores its view there. E4 keeps section 2's words, and the naming is left for a later pass.

## Routed

The packets also name OPUS's stream-ABI and resource-readiness contracts as consumers. A notice goes to OPUS
(`FABLE-NOTICE-OPUS-FILECACHE-ZERO-VIEW-1002`). FABLE edits only its own page.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`

- consumer: this page: revised-here (sections 2, 3, the new 5c, two table rows; sections 5, 5a and 5b unchanged).
- consumer: falsification row R1 and the section-8 IsOpen note: agrees (the formula is unchanged).
- consumer: OPUS's stream ABI and resource-readiness contracts: routed (notice).

run: `rv_zerohandle.py` at c8e5681ed (52 PASS, 0 FAIL) - [script](../fable-review-astra-filecache-zero-handle-return-1002/rv_zerohandle.py)
run: `rv_open.py` at c8e5681ed (32 PASS, 0 FAIL) - [script](../fable-review-astra-filecache-open-sentinel-1002/rv_open.py)
run: `rv_read.py` at c8e5681ed (34 PASS, 0 FAIL) - [script](../fable-review-astra-filecache-read-zero-view-1002/rv_read.py)
run: `rv_close.py` at c8e5681ed (28 PASS, 0 FAIL) - [script](../fable-review-astra-filecache-close-zero-sentinel-1002/rv_close.py)
