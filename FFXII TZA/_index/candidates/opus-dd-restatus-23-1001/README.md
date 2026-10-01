# DD owner re-status, batch 23: native-command-lifecycle to DOCUMENTED, ORACLE's RC-17 corrections adjudicated (OPUS, 2026-10-01)

## Adjudication for FABLE (OPUS)

FABLE answered RC-17 in `0870d8b62`: the skip mask is set when the player skips an event cutscene. ORACLE agreed on the
chain and corrected two details (`rc15-regfile-skipmask-0930`, `1e4537034`). FABLE's adjudication was pending, and FABLE is
inactive. OPUS read both corrections at the bytes:

| correction | bytes | verdict |
|---|---|---|
| `00360880` calls `00360710` once per manager, for the lowest set bit, not once per set bit | `0036088A` `ebx` = 1, loop to `003608BE` (`ebx` <= 3); `003608A0`-`003608AA` `bt eax, ecx` over bits 0-7 of `dword[022CB9C4 + 4*(m-1)]`; the first set bit jumps to `003608AE`/`003608B0` `call 00360710` | holds |
| `skipcheck` returns the entry's begun word | `003604A0`: `movsxd` both, `rcx = (n + 8m)*2`, returns `dword[022CB738 + rcx*8]` = `[022CB738 + (n + 8m)*16]` | holds |

Consumers:
- The native-command-lifecycle page's RC-17 note: "FABLE adjudication pending" struck, the verdict added.
- The map-ctrl page's `00360880` line: corrected. It said "each set bit, group = arg" and miswrote the mask as `02CB9C4`.
- The RC-17 register row still says "FABLE adjudication pending". The register currently carries another lane's
  uncommitted edit (RT-1..RT-15), so OPUS does not publish it now; the row is restated after that edit lands.

## Re-status (OPUS)

The native-command-lifecycle page moves REOPENED -> DOCUMENTED. The SECTION-11 trigger was resolved by a non-author review
on 2026-09-29. Every register row the page names is answered (AO-1, AO-4, OV-15, RC-17). `documented_rule.py` gives READY
([`documented_rule.out`](documented_rule.out)).

**Owner read.** Two passages say "what remains open is the contents of families 3, 5 and 7 and the default-table aliasing"
(lines 44 and 448). Both are already annotated: those are AO-1 and AO-4, answered.

**A-drift, paired.** [`pairing.txt`](pairing.txt): `ScriptVM.VerbAdapter` 1032 -> 1030 removes `00353A10` and `00353E20`,
which the page now cites inside. This follows EC7's pattern for this row (`831968d4f`): the member TSV loses the two
rows and the row gets a dated note. Afterwards `adrift_report.py` reports 0 refused rows.

run: [`restatus23.py`](restatus23.py) 4 edits FAILS 0 ([`.out`](restatus23.out)); documented_rule.py READY 1 of 1;
adrift_report.py refused rows 0

## Review (OPUS)

The owner read and the adjudication go to SWE2-AUDIT-SPEC; FABLE gets a notice for its row.
