# Audit-spec review: EC7 Phyre module selectors under the uniform closure-source rule

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `ec7-phyre-uniform-0930`
Board task: `SWE2-EC7-REQ-AUDITSPEC-PHYRE-UNIFORM-0930`

## Verdict: ACCEPT

## What was checked

- **Selectors at HEAD.** `select_phyre_module.py` and `select_phyre_panimation.py` carry the
  uniform rule exactly as the record describes: "predicate is evaluated IGNORING A status … is a
  closure source for its callees, but it stays A", closure-source output lines, and —
  load-bearing — `FIREWALL = (MODULE == "PhyreCore")` at line 192, with
  `blocked = FAIL | ((declared | a_set) if FIREWALL else set())`: the old exclusion is kept only
  for PhyreCore, matching the record's "PhyreCore keeps the old exclusion" after the misfit
  finding.
- **Mutation control present.** `PHYRE_FAIL`/`PHYRE_FAIL_FILE` appear in the selector (`FAIL` in
  the blocked expression) — the ruling's demanded control exists.
- **The PhyreCore refusal is evidence-based, not convenience.** The record states the predicate
  would admit +988 and the 25-body sample caught FFXII-tagged bodies (MovementNavigationSteering
  `003DB150`, a battle-menu-called `0027BD80`, large Presentation bodies). I verified
  `phyre-phyrecore.tsv` stands at 426 members, unchanged as claimed.
- **Honest instrument scoping.** The record flags that `check_family_forms` is *vacuous* for the
  Phyre rows (they claim no member size) and says the sample reads carry the weight — correct
  refusal to lean on a check that can't fail for the case at hand.

## Narrowing / notes

None required.
