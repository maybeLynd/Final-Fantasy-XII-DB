# SWE2-STRUCT: two exact-extent gap rows that contradicted their contract (OrderedCommandList +0x2A, AchievementState +0x04)

SWE2-STRUCT (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Source: FABLE's rule-(a) review
`_index/candidates/auditspec-rules-review-exact-extent-1003/` (UPHELD-WITH-CONDITION: an exact-extent gap row counts as
declared only if it does not contradict the contract)

## SWE2-STRUCT the two rows

**`OrderedCommandList +0x2A`.**
- The row read `unobservedByte2A` u8[1], "zeroed by the constructor ... no other access found".
- The contract `CONTRACT-render-command-list-and-graphics-handshake.md` (L82, and §14.2 item 2 at L448) names it
  `afterwaterActive`.
- The bytes agree with the contract. All three accesses go through the singleton getter `0018B4E0`, which returns
  `[01F7F5E0]`:
  - `001F3531 mov byte [rax+0x2a], 1`, then `0018B1B0(list, rdx, 2, 1)` at `001F3549`;
  - `001F3556 mov byte [rax+0x2a], 0`;
  - `001F5DE2 movzx edi, byte [rax+0x2a]` in `001F5D70`.
- `getter_disp.py` (`Tools/work/SWE2-STRUCT/standin1003/`) checks every one of the 78 getter call sites and finds exactly
  those three. As a control, the same sweep at `+0x29` finds 8 sites, including the three `walkFlag29` cites.
- The row becomes `afterwaterActive` uint8, SEMANTICALLY IDENTIFIED/PROVEN.

**`AchievementState +0x0004`.**
- The row read `unobservedSpan0004`, "no censused access".
- This type is interior to `ImageBackedStateBlock` at `+0x3844`: its `+0x00` is the parent's `firedBitmap`. So `+0x04`
  is the parent's `+0x3848 flagBitmap3848`, a PROVEN bitmap with setter `00315B50` and query `003156E0`.
- The row becomes `flagBitmap004` uint8[4], with its rung following the parent. Which flag the bitmap records stays
  open, as it does on the parent.

## SWE2-STRUCT consumer check

- S-39's types cell rests on `+0x2A` being declared at the contract's granularity. FABLE's review would have taken the
  cell to PARTIAL over the contradicting row. With the row corrected, the cell agrees with the contract and stays MET.
  The L2 table needs no edit.
- S-45 stays PARTIAL for its other items, as FABLE's review says. This row changes none of them.
- No page quotes either old row name.

## SWE2-STRUCT limits

Static only. Neither the meaning of "afterwater" nor the meaning of the second achievement flag is re-derived here.
