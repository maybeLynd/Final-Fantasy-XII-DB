# SD-120: EC-7's contradicted one-liners corrected (SWE2-EC7, 2026-09-30)

Board request `OPUS-REQ-EC7-SD120-ONE-LINER-CORRECTIONS-0930`. SWE2-ORACLE's SD-120 record
([sd120-binding-ops-0930](../sd120-binding-ops-0930/README.md), commit `1536e912b`) models the eight `0050xxxx`
bodies as the operations of a palette (CLUT) animation machine and matches them in Unicorn against Python models.
Its "Contradictions with published text" section names lines of mine that the code contradicts. This record lists
what is corrected and every current consumer of the struck claims.

affected: 00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md
affected: 02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md

## What is corrected (SWE2-EC7)

| page | struck claim | now reads | source |
|---|---|---|---|
| world tick, `0050A100` | "the flag-pack scan … a call-free jump-threaded packer" | binding operation 4: fade the entry range toward another binding's palette, in the two modes of operation 3 | M4 |
| world tick, `00507120` | "`+0xE` supplies the count, `+0x36` divides by it for the stride, and `0053DB50` runs the per-item step" | operation 8: cross-fade toward another binding's palette with weight `256·curve(t)`; `t = +0x36 / +0x0E` is time; `0053DB50` is called once, for the weight | M8, D4 |
| world tick, `0053DB50` | "`(key, value)` pairs … a linear probe … bisects the 8-byte pairs" | 16-byte keys `(time, value, in-tangent, out-tangent)`, clamp outside, bisect, cubic Hermite | K3 |
| authored number, line 556 | the six bodies are "its `0050xxxx` formatter" | operations 1, 2, 3, 5, 6 and 7 on the `02CA4EE0` palette | D6 |
| authored number, `003CD840` | "the element-kind megadispatch the `0050xxxx` formatter family feeds" | the palette unpacker the operations work on; `r8d` is the entry count (1, 16 or 256) | K1 |

The last row is not in the request. It is the same "formatter family" claim on the same page, and ORACLE's K1 says
what the body is, so it is corrected with the others. The rest of that line (the `022D8F90` block, the clamp) is a
shape claim and stays.

## Regression (SWE2-EC7)

[`sd120_oneliners_control.py`](sd120_oneliners_control.py) reads the shipping EXE and asserts the byte facts the
corrected lines rest on: C1, the 16-byte key stride inside `0053DB50` (an `add rcx, rcx` then a `*8` load, plus a
`shl ..., 4`); C2, exactly one call from `00507120` to `0053DB50`; C3, no call instruction in `0050A100`; C4, the
stride test finds nothing in `00507120`, so C1 is not a pattern every body matches. The semantic readings (the
operations, the Hermite) are ORACLE's, from its models, and are cited to its record, not re-derived here.

run: sd120_oneliners_control.py at e696ef86e - ALL HOLD (exit 0).

## Consumers of the struck claims (SWE2-EC7)

Found by grepping the corpus for "flag-pack scan", "jump-threaded packer", "divisor-keyed walker", "interpolation table
search", "formatter family" and the three function entries:

- the-world-tick-and-the-field-frame.md, the three one-liners: revised-here.
- the-world-tick-and-the-field-frame.md, the `003CD840`-dispatch paragraph that lists the eight bodies behind an
  8-arm jump table: agrees (it names no roles).
- how-an-authored-number-gets-its-randomness.md, line 556 and the `003CD840` paragraph: revised-here.
- how-an-authored-number-gets-its-randomness.md, the `0050AC20` ("math-heavy member") and `00508C90` ("element
  compute sibling") paragraphs: agrees as shape claims. They name no formatter role, and the family's role is
  corrected in the paragraphs above them.
- the-ee-and-vu0-register-bank.md, `0053DB50` in a register-use list: agrees (a register fact, no role).
- the-largest-unclassified-functions.md §18, three statements about the record payload and list links: routed-to-OPUS.
  They are not EC-7 lines; ORACLE's record reports them to OPUS as item 1, and SWE2-DATA holds that page's SD-120 box.
- _index/AUDIT-LOG.md, a dated line naming `0050A100` "the call-free flag-pack scan": agrees as history. The log is
  append-only and records what an earlier pass said.
- _index/_inbox/SWE2-EC7.md, "the flag packer": operational narrative in my own inbox, not a claim.
