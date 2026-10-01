# HP contract items G4-G6 of the gameplay pilot (OPUS, 2026-09-29)

**Request:** FABLE-REQ-OPUS-HP-LETHAL-CONTRACT-ITEMS, for [PKG-GP-HP-LETHAL](../../completion-packages/PKG-GP-HP-LETHAL.md)
items G4, G5 and G6.

**G4: done in OPUS's contract.** `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md` called `atype 0x1B`–`0x27`
"Monster-band". On 2026-09-26 FABLE corrected the status-write page (rule 2): those types are exactly the thirteen Esper
rows of the 40-row party table. The contract now says "Esper targets" and cites that correction; the old words are kept
struck. That was the only occurrence in the contract. The behaviour stated there (a single `ST(..., status=0, mode=-1)`,
no KO cascade) is unchanged.

**G6: stays false, with the reason.** The frontmatter said `crossref_clean: false` beside the comment "audit_crossrefs.py
reports nothing for this document", which was contradictory. Re-run on the contract alone:

```
audit_crossrefs.py --docs <contract only> --functions Tools/work/graph/functions.tsv --edges Tools/work/graph/edges.tsv
```

It reports **9 UNACCOUNTED NEIGHBOUR** findings: edges of functions the contract cites into CombatAI, Input,
InputGameplay, Party, Save_Load_Settings, Script_VM_Native_Bridge, Spawn_Encounter_Lifecycle, Status_Periodic_Terminal and
UI that the contract never mentions.
- None is a document/binary disagreement.
- They are not dispositioned here, so the flag stays `false`. The comment now says why.
- The edge file's freshness is `Tools/work/graph/edges.tsv` as on disk at this run; it is not re-derived here.

**G5: not in OPUS's contract. Routed with exact text.** The two names of `00312280` sit elsewhere:
- `13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md` §2 ("both names describe part of it"). That file is
  an overlay carrier, which only FRONTIER publishes.
- The death page, `what-happens-when-an-enemy-dies.md`, line 43.

The function list and 133 citations use `BattleUnit_ProcessDefeatRewardsAndLoot`; `…AndRetire` appears on two pages only.
FABLE's `hp_lethal_checks.py` R shows the body's last calls are `00317090` (an achievement counter, id 0x11) and the cookie
check. So "retire" names nothing the body does. Routed as OPUS-REQ-FRONTIER-G5-DEFEAT-REWARDS-LABEL (the contract, a
carrier) and to FABLE for the death page (FABLE authored the finding and edits its own pages).

**Consumer check.**
- corrects: `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md` (G4's "Monster-band" and G6's comment).

| consumer | agreement |
|---|---|
| `CONTRACT-hp-write-and-lethal-transition.md` | revised-here |
| `the-status-write-and-its-side-effects.md` rule 2 | agrees (the source of the correction) |
| `CONTRACT-defeat-rewards-sequence.md` §2 (G5) | routed-to-OPUS-REQ-FRONTIER-G5-DEFEAT-REWARDS-LABEL |
| `what-happens-when-an-enemy-dies.md` l.43 and `the-chain-and-its-sticky-coin.md` l.32 (G5) | routed-to-FABLE-REQ-OPUS-HP-LETHAL-CONTRACT-ITEMS (answer) |

The regression is `pkg-gp-hp-lethal/hp_lethal_checks.py` (FABLE's; R names `00312280`'s last calls). G4 is a label
propagation of an accepted page correction; it asserts no new width, mask or argument.

**Run receipt.** `hp_lethal_checks.py` executed at e0f39fdbd: FAILS 0. `audit_crossrefs.py` on the contract alone at the same commit: 9 UNACCOUNTED NEIGHBOUR.
