# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-bazaar-recipe-unlock-and-purchase-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-BAZAAR-RECIPE-UNLOCK-AND-PURC` · Package: `_index/candidates/fable-home-the-bazaar-recipe-unlock-and-purchase-1002/` · Page: `12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 0, skipped 0, missing 0. The row's text is on the page verbatim.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved, float constants peeked). Every call offset and branch polarity was checked. The entered_from site was disassembled and confirmed as a direct jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002ABAA0`: `ebx` = incoming `ecx`. The +0x8 call (`00254A10`) is followed by `test eax, eax; jne 002ABB03`, so the +0x11 call (`00229E40`) runs only on 0. `cmp eax, 7; jne` and `test ebx, ebx; je 002ABAD6` give the 7-and-zero arm, which is `movss 26.0 (00916484); cvttss2si` with no call. All four other paths make exactly one `0024ABA0` call: +0x1F (`002ABABF`, 7 and non-zero), +0x48 (`002ABAE8`, not 7) or +0x63 (`002ABB03`, first call non-zero). Each then multiplies by 15.0 (`00916314`) when `ebx` is non-zero (`002ABAC4`, `002ABAF1`, or the `jne 002ABAC4` from `002ABB0A`) or by 10.0 (`008F8180`, `002ABB0C`) when it is zero, then `cvttss2si`. Exact.
- Site: `0029CCD0` + 0xE = `0029CCDE jmp 002ABAA0` (the `edx <= 0` arm, which sets `ecx = 0`).
- Host: L562 (in the page's SWE2-EC7 section) reads `002CC780`, the purchase loop that `002CA7C0` calls, as iterating over `0029CCD0`. The bytes confirm `002CC833 call 0029CCD0`. The only other page naming `002CC780` (`16-UI/Shop-Screens/the-shop-screens.md` L101) lists it without reading it, so this page is the natural host.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
