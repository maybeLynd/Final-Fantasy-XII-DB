# Canonical evidence and correction policy — draft for startup-loaded instructions (OPUS, 2026-09-25)

*A draft for SWE2-FRONTIER to place in the instructions every session loads at startup (`CLAUDE.md`'s database section,
or `_index/_inbox/TEAM.md` if that is where FRONTIER keeps fleet rules). It restates the user's repair instruction of
2026-09-25 as operative rules. OPUS drafted it and does not place it alone: one canonical copy, placed by the planner,
replaces any restatement buried in a session log.*

## Evidence

1. **Three axes, never merged.**
   - The three axes are **physical access** (instructions, widths), **representation** (offset, width, ctype, extent,
     layout, values) and **semantic purpose**.
   - `PROVEN` access, `TYPE RESOLVED` or a tiled layout cannot overrule `MEANING NOT CLAIMED`.
   - Readiness never implies meaning.
   - A known variable-size rule is a known extent.
   - Names that are labels are not semantic claims. Never rename to move a percentage. (Details: `_types/README.md`,
     "Access, representation and meaning are three axes".)
2. **A sampled value is representation.** A sampled zero never proves "no write" or "no default"; read or run the
   producer.
3. **Keep evidence classes apart:** static, replay, live and inference. Negative results are domain-limited.

## Corrections

4. **A correction updates every affected current consumer:** type, field, contract, mechanism and page. It links to the
   primary evidence and names the changed assumption.
5. **Old raw results stay immutable, and old conclusions stay visible**, marked superseded.
6. **Every correction ships the smallest regression that would reject the original wrong interpretation.**
7. **Automated label and consistency checks detect contradictions, not semantic truth.** Independent review of the
   original evidence remains.

## Review and acceptance

8. **A review receipt binds to the claim, its content and its dependencies.** A changed dependency marks only the
   affected acceptance for re-review, not the whole project.
9. **Exact pending acceptance goes to a reviewer other than the author.**
   - A finding is never closed because a request was sent.
   - Producer tests and selected ACCEPTs are not whole-package acceptance.
   - Unresolved required debt stays visible even when a scoped cell is MET.

## Derived data

10. **Use canonical sources, or a mirror whose freshness is verified by FRONTIER/DATA's reader check.**
    - A stale mirror is history only, never proof of current counts, absence, meaning or readiness.
    - DATA owns generator repair.

## Persistence and publication

11. **Checkpoint Git often.** Preserve peer preimages, and publish only your own authorized paths.
12. **Run affected regressions and mutations**, not full campaigns, at each edit.
13. **Keep current work and next obligations at the top of the identity's handoff.**
14. **Report `DB_GOAL=NOT_MET`** while accepted L1+L2 and the required terminal reviews remain incomplete.
15. **After each package, start the next eligible obligation.** Explicit stops and genuine limits are `PAUSED`, and no
    automatic continuation is claimed that the host does not support.
