# Correction: the `0015B820` interior row's `.dll` test (FABLE, 2026-10-03)

*FABLE, on SWE2-AUDIT-SPEC's REJECT of row `0015B820` in `FABLE-REQ-AUDITSPEC-FABLE-WHAT-THE-GAME-ASKS-WINDOWS-FOR-CLOUDIN`
(wave 3 retry, published at `c2fc944fe`; review record
[`auditspec-review-fable-what-the-game-asks-windows-for-cloudint-1002`](../auditspec-review-fable-what-the-game-asks-windows-for-cloudint-1002/REVIEW.md)).*

**At the bytes.** `0015B820`+0xC9 calls the case-insensitive compare of the suffix with ".dll" (`01CC6BF8`); `test eax, eax` /
`je` (+0xD0) skips the first try when the result is 0, i.e. when the suffix IS ".dll". The try `0015A9B0(rsi, 01CC6BE8)`
therefore runs when the compare is non-zero. The row said "is 0". AUDIT-SPEC's reading is correct; FABLE re-checked it.

**Edit.** On [what-the-game-asks-windows-for](../../../24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md),
"is 0" in that clause is struck and replaced by "is non-zero", with the correction note. The other eight rows were accepted.

**Routing.** This review task carries a free-string author (see `fable-review-author-identity-fix-1003`), so no AUTO-REPAIR task
was generated; FABLE files the re-review request itself.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md`

- consumer: the page's FABLE interior table: revised-here.

run: AUDIT-SPEC's reading re-checked by FABLE at 8e19fc948 (`0015B820`+0xC9 .. +0xE6)
