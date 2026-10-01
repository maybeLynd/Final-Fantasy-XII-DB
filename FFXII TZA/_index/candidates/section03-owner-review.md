# SECTION-03 (Update03) — owner's review of the reward-binding rewrites (OPUS, 2026-09-25)

SECTION-03 rewrites `13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md` (OPUS's
§15a inside it) from 6,633 to 2,869 words and touches `CONTRACT-defeat-rewards-sequence.md` (**FABLE's**,
S-32 — CORRECTED 2026-09-25: an earlier version of this file called it OPUS's) and three pages,
uncommitted. Evidence class NATIVE/STATIC; `002F8BB0` (the EXP computer) was re-read whole.

## Verdict (OPUS): ACCEPT THE CORRECTIONS — ONE CORRECTS A FABLE CONTRACT — AND RESTORE §15a

### Re-read from the image — agree

| claim | static finding in `002F8BB0` |
|---|---|
| **R03-1** a NULL recipient still divides in shared mode | `002F8BCF test rcx,rcx / je 002F8C11` skips only the recipient checks. `002F8C34 call 003135C0`; on 0 (shared) the path at `002F8C8D` runs **four** `0031B810` lookups (`ebx` 0..3, `002F8CE2 cmp ebx,4`), counts eligible members in `ebp`, and `002F8D1C cdq / idiv ebp` — **independent of `rdi`**. Designated mode with NULL takes `002F8C45 je 002F8C5C` past the designation check and returns the undivided base. The caller really passes NULL: `00312280` does `xor ecx,ecx` at `003124BC` (→ `002F8BB0`) and `003124C6` (→ `002F90C0`). |
| **R03-3** recipient admission ≠ divisor admission | the recipient filter rejects kind-0 ids `0x1B..0x27` (`002F8BF2..002F8BFA`), so `0x1A` is admitted; the divisor loop skips it (`002F8CD8 cmp byte [rcx+4], 0x1A / je`). |
| **R03-4** an empty roster returns 0 before any row read; NULL rows fault at `+0x34` | `esi` is zeroed at `002F8BC7`; `002F8CEC test ebp,ebp / je 002F8D21` skips every row read; the row loads `002F8D07 → 002F8D0E [rcx+0x34]` have nothing between them — **exactly §15a's positional table**. |
| effect modifiers skipped for NULL | `002F8D21 test rdi,rdi / je 002F8D42` |

**Not re-derived:** R03-2 (LP's own gate), R03-3's `0xFFFF` sentinel (not in `002F8BB0` or its direct
callees — deeper), R03-5.

### It corrects a FABLE contract claim (OPUS reading)

`CONTRACT-defeat-rewards-sequence.md` at HEAD (lines 72, 79, 133, 163): *"the display shows the
undivided award; every character receives it divided."* **Wrong in shared mode**: the display call's
NULL recipient divides exactly like a member's. Only designated mode yields the undivided total.
The overlay's correction stands on the image. **The sentence is FABLE's to withdraw, not OPUS's** —
routed to FABLE (an earlier version of this file wrongly said "OPUS withdraws").

### What it must not delete

- **§15a "Falsification pass 1 — 2026-09-12 (OPUS)"**, whole: the purity measurement (0 record
  writes in either computer), the positional null-test table for all six row loads, the 13 + 5
  unrelated null tests counted, and the four bound guards in `0023A570`. **SECTION-03 does not
  contradict any of it — R03-4 depends on it.** Keep it (as a historical/falsification section if
  preferred).
- The citations of **EXP-002** (base reads 0 at the title screen), **EXP-076** (the native reward
  decode control) and **EXP-101** (`0031B860` executed alone).
- The remaining lost addresses are listed in `overlay-drop-census-2026-09-25.tsv`; each needs a
  restated / withdrawn-with-reason / restore disposition.
