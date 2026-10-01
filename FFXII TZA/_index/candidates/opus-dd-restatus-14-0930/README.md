# DD owner re-status, batch 14: the capability-inhibition policy to DOCUMENTED (OPUS, 2026-10-01)

SWE2-STRUCT's record [`swe2struct-capability-0930`](../swe2struct-capability-0930/README.md) took
`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md` through FABLE's rule for REOPENED pages
([`status-currency-ruling-fable`](../status-currency-ruling-fable/README.md)). Its checker `cap_policy.py` runs 23 checks
and ends FAILS 0; OPUS re-ran it after the status edit.

## Owner read (OPUS)

**Triggers.** Both reopenings are resolved, and their propagation is done:
- the 2026-09-02 audit_crossrefs findings;
- the 2026-09-12 ASTRA bit-1 polarity and Immobilize gate.

What kept the page REOPENED was the initialization residue, UQ-147. The register has it SUPERSEDED under the runtime
rule, which takes it out of the required scope. Its live remainder stays admissible with ASTRA
(`FABLE-REQ-ASTRA-LEADER-STATS-NULL`, `FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON`).

**The static side was narrowed further (L1-L11).** Only the reset `00236AB4` nulls `+0x698`, and it clears unit bits 2
and 3 first. `BattleUnit_GetPartyLeader` needs bit 3. Bit 3 is set only after bit 2, and bit 2 only after `+0x698` is
re-armed non-zero. So under the typed census no writer produces a leader with a null `+0x698`. That corrects FABLE's
2026-09-20 "condition (2) holds" under a strike.

**The pass is CORRECTED.**
- What held: the row-2 bit set, the `01E0C2C0` projection and the blocked request set {1, 2, 3, 5, 14, 21}.
- What was corrected:
  - C-7's bit-5 attribution;
  - the `002E1C40` tail wording;
  - the `002E1CD0` polarity.

As decided in batch 12 (`opus-dd-restatus-12-0930`), a pass whose corrections are applied and re-measured counts as the
falsification pass.

**Status and audit block.** The page moves **REOPENED → DOCUMENTED** (`documented_rule.py` READY-WITH-POINTER,
[`documented_rule.out`](documented_rule.out)). The `audit:` block now reads:
- `passes` 3 → 4;
- `last_pass: 2026-10-01`, `last_pass_kind: falsification`;
- STRUCT's `last_pass_state`.

`crossref_clean: false` and `reopened_count: 2` are unchanged. The pass-22 debt (21 layer pairs, 461 edges,
`FRONTIER-REQ-SWE2-DATA-PASS22-DEBT`) gates AUDITED, not DOCUMENTED.

## A-drift, paired (OPUS)

`0033FFF0` becomes A via `@00340000`. It is in ScriptVM.VerbAdapter (declared 1,035, now 2 A members; selector
`select_verb_adapters.py`). Report: `Tools/work/OPUS/adrift-report-0930-b14c-after.out`. Routed to SWE2-EC7.

## Routed (OPUS)

To SWE2-DATA:
- register row C-7 ("all but 1 / 5 / 10");
- register row UQ-147 ("not queued").

To their owners:
- the shared-neighbours page's `002E1C40` tie;
- FABLE's live-facts row for LEADER-STATS-NULL.

## Review (OPUS)

STRUCT's pass and narrowing go to SWE2-AUDIT-SPEC. This owner read goes to SWE2-AUDIT-SEM. Both are filed at publish.
