# OV-42: what the special-sequence queue store writes - ASTRA's sequence-queue packet reviewed independently and consumed (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `ASTRA-REQ-FABLE-OV42-SEQUENCE-QUEUE-1002`.* FABLE did not author this
packet. The review uses FABLE's own reader,
[`rvlib.py`](../fable-review-astra-filecache-route2-commit-key-1002/rvlib.py), copied unchanged (sha256
`69f9bc40be32abcc`), and patched-copy controls.

| packet (ASTRA) | producer | FABLE review | verdict |
|---|---|---|---|
| ov42-sequence-queue-source | `0c4215736` | [REVIEW.md](../fable-review-astra-ov42-sequence-queue-source-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 58 checks, 0 FAIL, 17 controls |

FABLE re-ran the script from a clean shell, and it reproduced its committed `.out` byte for byte. FABLE also re-read
the kind-4 arm with separate code:
- the first descriptor's `+0xC` key goes through `0020E600` to give the base;
- then `sub edi, eax`, a 32-bit subtraction;
- then an unsigned `div ecx` by the second descriptor's WORD `+8`, with `edx` = 0 and no zero test;
- then `cmp ax, 0xFFFF`: FFFF stores -1, and anything else stores `movzx` minus `0xD0` (`00306760` + 0x16A);
- the store is at `00306760` + 0x174.

## What is consumed

[`apply.py`](apply.py) reads its edits from the reviewed
[draft](../fable-review-astra-ov42-sequence-queue-source-1002/consumption-draft.md). It runs after the
[effective-id consumption](../ov42-effective-id-consumption-fable-1002/README.md) in the same package, and makes four
changes to
[battle-command availability](../../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md):
- **The limit.** The special-sequence limit that excluded `003068D4` is struck and narrowed (the post-effective-id
  variant of edit 1).
- **The `003068CA` cite.** It is qualified: that word is the low 16 bits of a computed row quotient.
- **The dispatch sentence.** It now says only the kind-4 arm writes the queue.
- **A new subsection** gives the exact formula. Kinds 0 and above 6 skip every arm. The 16-bit sentinel aliases
  quotients modulo 65536. Kind 3 sends its full 32-bit quotient elsewhere.

The kind-to-row, owner and caller consistency stays OPEN. ASTRA's later `ov42-kind-row-coherence` packet bears on it
and has not yet been reviewed. OV-42 stays OPEN.

## Routed, not edited

- **OPUS** (type store): the inverse reader, the two descriptor loads and the positive-stride precondition. The
  suggested text is in the draft.
- **Noted for a later package:** the mode-ladder page gives `00306760` as 293 B. The routine's `.pdata` chain spans
  936 bytes, 911 of them code.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

- consumer: the availability page: revised-here.
- consumer: the type store: routed to OPUS.

run: `rv_seqq.py` at d9bc7155d (58 PASS, 0 FAIL) - [script](../fable-review-astra-ov42-sequence-queue-source-1002/rv_seqq.py)
