# Canonical evidence and correction policy

**Canonical policy, placed 2026-09-26 (SWE2-FRONTIER, from the OPUS draft at
`_index/candidates/canonical-evidence-policy-draft.md`) and binding on every lane.** This is the
single authoritative statement; restatements buried in session logs and handoffs are superseded.
`CLAUDE.md` and `_index/_inbox/TEAM.md` link here. The derived-data mechanics this policy invokes
live in [`DERIVED-DATA.md`](DERIVED-DATA.md).

## Evidence

1. **Three axes, never merged.**
   - The three axes are **physical access** (instructions, widths), **representation** (offset,
     width, ctype, extent, layout, values) and **semantic purpose**.
   - `PROVEN` access, `TYPE RESOLVED` or a tiled layout cannot overrule `MEANING NOT CLAIMED`.
   - Readiness never implies meaning.
   - A known variable-size rule is a known extent.
   - Names that are labels are not semantic claims. Never rename to move a percentage. (Details:
     `_types/README.md`, "Access, representation and meaning are three axes".)
2. **A sampled value is representation.** A sampled zero never proves "no write" or "no default";
   read or run the producer.
3. **Keep evidence classes apart:** static, replay, live and inference. Negative results are
   domain-limited.

## Corrections

4. **A correction updates every affected current consumer:** type, field, contract, mechanism and
   page. It links to the primary evidence and names the changed assumption.
   - **4a.** An accepted or routed correction is **not** a repaired canonical claim until its owning
     page/contract and every dependent current explanation carry it. A board request, a notice, an
     accepted review or a correction on another page does not close it. The correction propagates
     through the owning page's authorized editor; the finding records its propagation state
     (routed / owner-published with commit / consumers updated), and it stays open while any
     current consumer still states the refuted text as the active summary. Earlier conclusions
     stay only as dated, superseded history. *(User instruction of 2026-09-25 via FABLE.)*
   - **4b.** Rule 4a is enforced at publish, not by memory: `publish_paths.sh` refuses a
     publish whose staged diff adds a struck claim plus a correction keyword without a
     consumer-check record under `_index/candidates/` — listing each current consumer's
     agreement (agrees / revised-here / routed-to-\<task\>) and the regression that
     measures it. Reset widths/masks, argument orders and byte/register binds require
     that record to name an existing `.py` control; matching words is not executing the
     control. A routed consumer leaves the record **PENDING PROPAGATION** and the
     publish prints it. When a dependent claim changes, keep the old receipt and
     invalidate only the affected acceptance until re-reviewed.
     *(FABLE-REQ-FRONTIER-CONTRACT-CORRECTION-PUBLISH-NEEDS-CONSUMER-CHECK, 2026-09-26.)*
   - **4c.** The record must declare its scope explicitly (2026-09-27 directive): an
     `affected:`/`corrects:` line naming the corrected claim (row id or path) — and any
     path it declares must be a file the publish actually touches. Strike/keyword
     detection is only the supplement that catches undeclared corrections; a declared
     correction needs no strike markers. A record naming a `.py` control must also pin
     the run to a commit that is an ancestor of HEAD (`run:`/`receipt:`/`verified at
     <sha>`) — naming the script is not proof it ran, and a receipt at a non-ancestor
     revision is not a receipt. `PUBLISH_NO_CORRECTION_CHECK=1` is not an escape: it
     downgrades the refusal only when the commit message carries
     `correction-override: <authorizer>` and `override-reason: <why>`, so every
     override is attributable and greppable. *(FRONTIER-TODO-CORRECTION-DECLARATION-AND-OVERRIDE.)*
5. **Old raw results stay immutable, and old conclusions stay visible**, marked superseded.
6. **Every correction ships the smallest regression that would reject the original wrong
   interpretation.**
7. **Automated label and consistency checks detect contradictions, not semantic truth.** Independent
   review of the original evidence remains.

## Review and acceptance

8. **A review receipt binds to the claim, its content and its dependencies.** A changed dependency
   marks only the affected acceptance for re-review, not the whole project.
9. **Exact pending acceptance goes to a reviewer other than the author.**
   - A finding is never closed because a request was sent.
   - Producer tests and selected ACCEPTs are not whole-package acceptance.
   - Unresolved required debt stays visible even when a scoped cell is MET.

## Derived data

10. **Use canonical sources, or a mirror whose freshness is verified by the shared check.**
    - `knowledge_db.py check` / `knowledge_db.freshness_report` is the single freshness verdict;
      timestamps, `integrity_check=ok` and "built from HEAD" are not freshness evidence.
    - A stale mirror is history only, never proof of current counts, absence, meaning or readiness.
      An as-of read is legal only through `query --snapshot`, which labels the output with the
      build's pin, hashes and stale list.
    - DATA owns generator repair and mirror/dashboard freshness.
    - The full mechanics — what `provenance` records, staging builds, the reader contract — are in
      [`DERIVED-DATA.md`](DERIVED-DATA.md).

## Persistence and publication

11. **Checkpoint Git often.** Preserve peer preimages, and publish only your own authorized paths.
12. **Run affected regressions and mutations**, not full campaigns, at each edit.
13. **Keep current work and next obligations at the top of the identity's handoff.**
14. **Report `DB_GOAL=NOT_MET`** while accepted L1+L2 and the required terminal reviews remain
    incomplete.
15. **After each package, start the next eligible obligation.** Explicit stops and genuine limits
    are `PAUSED`, and no automatic continuation is claimed that the host does not support.
16. **Operative views are generated and checked, never hand-maintained.** An inbox's
    `TEAM-CURRENT` block, queue summary or NEXT list is a *derived read* of TEAM state,
    bound to the board revision, `recovery_epoch` and a queue fingerprint — not a
    second source of truth. A `STALE-*` verdict makes it non-authoritative: re-derive
    through `team.py current` rather than acting on it. Hand-maintained counts are what
    silently replayed completed work before; the generated block exists so a stale
    header fails visibly instead.
