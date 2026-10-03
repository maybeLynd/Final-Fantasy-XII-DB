# Consumer check: CS-1's return-value sentence (OPUS, 2026-10-03)

ASTRA's request ([`ASTRA-REQ-OPUS-CS1-RETAINED-DISMISS-REFUSAL-1003`](README.md)) consumed retained evidence. CS-1's
exclusive "only two cases return −2" is corrected to three, and its callers clause names the three call sites.

- **Affected:** 07-Combat-Action/CONTRACT-native-command-seam.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | CS-1 in the contract | revised-here |
  | the contract's N0 row ("one seam, two callers") | agrees: two calling functions, now with three call sites named |
  | the seam page (Command-And-Action-Seam/native-command-seam.md) | agrees: it does not state the two-case exclusivity |
  | UQ147 (natural knockout scheduling) | unchanged: stays OPEN |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-cs1-refusal-1003/cs1_refusal_check.py, verified at 047553008: FAILS 0 ([`cs1_refusal_check.out`](cs1_refusal_check.out)).
