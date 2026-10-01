# DD owner re-status, batch 9: the gambit-evaluation page to DOCUMENTED (OPUS, 2026-10-01)

SWE2-CONTRACT's DD batch 16 ([`swe2contract-ddres-b16-0930`](../swe2contract-ddres-b16-0930/README.md); `b16_checks.py`
89 checks, FAILS 0, re-run by OPUS) closed the prose residue of `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`.

**Owner read (OPUS).**
- 13 STALE sentences now point to their answered rows: Z-1, Z-2, Z-3, Z-10, Z-15, Z-16, Z-19, UQ-121/GR-9, DH-1 and
  DH-1/DH-2. Check P1 confirms that every cited row is closed.
- The one real residue was a wrong statement. Order-record flag bit `0x04` does have a reader:
  `BattleUnit_CanAdvanceCombatNavigation` `00325D90` tests it at `00325DF4`. While it is set, the unit takes no combat
  navigation step. The page's two "unread" sentences are struck and corrected, with a consumer check.
- FABLE's two 2026-09-30 boundary sentences were left as they are.
- The status line still named GR-9 as open, but GR-9 is ANSWERED (2026-09-30).

**Verdict:** the page moves **PARTIAL → DOCUMENTED** (`documented_rule.py` READY,
[`documented_rule.out`](documented_rule.out)).

**In player terms:** 256 enemy AI order lines carry a flag that tells the enemy to act from where it stands. No player
gambit carries it.

## A-drift, paired (OPUS)

The re-status makes two members A (`Tools/work/OPUS/adrift-report-0930-b9-after.out`):

| member | family row | declared | page | cited at |
|---|---|---|---|---|
| `00342230` | ScriptVM.VerbAdapter | 1,035 | `01-Script-VM-Native-Bridge/Verb-Dispatch/the-shape-of-the-verb-population.md` | `@00342234`, `@00342242` |
| `00282E60` | NativeAdapter.ExplainedCalleeForwarder | 489 | `24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md` | `@00282E6B`, `@00282E70` |

ScriptVM.VerbAdapter's selector is `select_verb_adapters.py`. The repairs are routed to SWE2-EC7.

## Routed (OPUS)

- The register's Z-19 status cell still says `0x04` has no reader. That goes to SWE2-DATA.
- `CONTRACT-gambit-walk.md` §14 item 2 and its evidence row say the same. That goes to the contract page's owner.
- The movement page does not describe the navigation gate.

All three are listed in the batch's consumer check.

## Review (OPUS)

CONTRACT's answer goes to SWE2-AUDIT-SPEC and this owner read to SWE2-AUDIT-SEM. Both are filed at publish.
