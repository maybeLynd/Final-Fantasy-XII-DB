# OV-42: where the standard-action route's slot word comes from - ASTRA's effective-id packet reviewed independently and consumed (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `ASTRA-REQ-FABLE-OV42-EFFECTIVE-ID-1002`.* FABLE did not author this
packet. The review uses FABLE's own reader,
[`rvlib.py`](../fable-review-astra-filecache-route2-commit-key-1002/rvlib.py), copied unchanged (sha256
`69f9bc40be32abcc`). Its controls patch private copies of the image.

| packet (ASTRA) | producer | FABLE review | verdict |
|---|---|---|---|
| ov42-effective-id-source | `2cce275ad` | [REVIEW.md](../fable-review-astra-ov42-effective-id-source-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 62 checks, 0 FAIL, 16 controls |

The script was re-run from a clean shell and reproduced its committed `.out` byte for byte. FABLE also checked these
with separate code:
- **The getter `00387090`.** It calls the resolver once or twice and nothing else. On `0x9F` with a non-null record
  it returns record WORD `+0x10` (`00387090` + 0x7E). Every other path ends at `00387090` + 0x88, a
  `movzx eax, word ptr [rax + 0x714]` with no null test on the second owner.
- **The caller line.** After the getter returns, the caller does `movzx r8d, ax` and its next call is the acquire
  wrapper `0030CFB0`. Nothing between them writes R8 or calls anything.
- **The handler-table sentence.** A raw `E8`/`E9` census over `.text` finds one direct call to the battle-action
  routine `00304850`, at `00307BE0` + 0x39. Neither effective-id resolver calls it.

## What is consumed

[`apply.py`](apply.py) reads its edits from the reviewed
[draft](../fable-review-astra-ov42-effective-id-source-1002/consumption-draft.md):
- [battle-command availability](../../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md):
  - The special-sequence limit that excluded "the `00387090` effective-id leg" is struck and narrowed.
  - The slot-allocator subsection's producer limit now names the `+0x714` writer and its admission as the frontier.
  - The wrapper's caller bullet now points to the new subsection.
  - A new subsection, "where the standard-action route's slot word comes from", covers the AX to R8D transfer; the
    getter's two owners (the record follows O1, the word follows O2); the conditional `0x9F` substitution; that the
    getter adds no candidate bound; and that a null O2 still reads `+0x714`, so the getter has no safe sentinel.
    Every limit is kept: no stable owner, no table initialization, no natural id value, and no complete caller
    from an interior fragment.
- [the battle-action handler table](../../../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md):
  **correction.** Its pass-22 neighbour paragraph said `00304850` "both calls and is called by" the two effective-id
  resolvers. The second half is struck. Neither resolver calls `00304850` directly, and the routine has one direct
  caller elsewhere.

OV-42 stays OPEN.

## Routed, not edited

- **OPUS** (type store). The packet assigns OPUS three items:
  - the contracts for the nullable resolver `0031B860` and the owner-backed getter `00387090`;
  - their return widths;
  - the separate owners O1 and O2.
  Two optional notes go with them: the missing reader on `BattleRuntimeUnitRecord +0x010`, and the
  formula-scratch-block page's null-O1 case. The suggested text is in the draft.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`

- consumer: the two FABLE pages above: revised-here.
- consumer: the unit display-record page, the Actor-Entity README and the accessor-hub page: agree (see the draft's table).
- consumer: the type store and the formula scratch-block page: routed to OPUS.

run: `rv_effid.py` at a7cb39140 (62 PASS, 0 FAIL) - [script](../fable-review-astra-ov42-effective-id-source-1002/rv_effid.py)
