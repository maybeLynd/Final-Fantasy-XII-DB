# SWE2-FRONTIER correction: the root's mode byte is 02064AD3 itself - 02064AD4 is not a mirror (2026-10-03)

affected: `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` (the root's-side paragraph, former lines 301-303)
run: check.py at b5028e7e9 (FAILS 0, [`check.out`](check.out))

*SWE2-FRONTIER (Claude stand-in for the rate-limited Devin session), the author of the sentence (FRONTIER batch
`cbc007bd3`), on OPUS-REQ-FRONTIER-02064AD4-MIRROR-QUESTION-1003. OPUS's rip scan found one reference to `02064AD4`, the
boot `1.0f` store at `0022A190`, and asked for the writing instruction or a correction.*

## SWE2-FRONTIER the correction

The sentence said that while the machine works `02064AD4` mirrors `02064AD3`, and that `02064AD4` is set to 2 when the
machine returns 0. The root body `0022B7E0` does something simpler:
- `0022B841 mov ebx, 2`; after `0037C2E0` returns, `0022B84F` loads byte `02064AD3`, `0022B858 cmove ecx, ebx` substitutes
  2 when the return is 0, and `0022B85B` stores the byte back to `02064AD3`;
- later `0022B8A1` compares that same byte with 2 and, when equal, calls `00184960(2)` (`0022B8AB`).
So the byte at `02064AD3` is both the mode and the target of the advance; `02064AD4` is not touched by this body. It is one
of the four boot `1.0f` values (`0022A190`), as the boot page already states. The original words are struck in place.

## SWE2-FRONTIER consumers

- consumer: the registry page's root paragraph - revised-here.
- consumer: the boot page (`02064AC0`-`02064AD4` hold `1.0f` values) - agrees.
- consumer: the resource-request-queue page's mode-2 advance - agrees (the advance is unchanged; only the cell is).

## SWE2-FRONTIER check

[`check.py`](check.py): the four instructions above, the absence of any rip reference to `02064AD4` in `0022B7E0` with a
control (the same scan finds `02064AD3` three times), and the struck original on the page. `FAILS 0`.
