# Context refresh follow-up: supersession index, consumer-check map, phase cap, UC-1 census (FABLE, 2026-10-03)

*Follows [`fable-context-refresh-1003`](../fable-context-refresh-1003/README.md) (published `042b50ca9`). It finishes the
items of the user's improvement addendum (§7, §15) and the corpus audit follow-up that the first publish left open. The
last two items were handed back by OPUS (`OPUS-REQ-FABLE-HANDBACK-1003`).*

## What this publish adds

- **`_index/workflow/SUPERSESSION.json`** (addendum §15). This is a machine-readable index of the artifacts a reader
  could mistake for the current state:
  - the GM160 / GN handoffs and their recovery package;
  - `_inbox/EXTERNAL-CONTINUATION.md`, which still calls itself "current handoff" although SECTION-12 was accepted on
    2026-09-29;
  - the migration ZIP's `START-HERE.md`;
  - TEAM.md's September starting instructions;
  - the readiness gate in its old role as the endpoint;
  - the GN161 residual list;
  - the user-supplied `knowledge.sqlite` snapshots.

  No artifact is edited. `EXTERNAL-CONTINUATION.md` is labelled only, because the user's external-update overlay
  writes it.
- **`check_lifecycle_consumers.py` check 5** (addendum §9's startup guard, made mechanical). The README and TEAM.md may
  link an indexed artifact only on a line that carries its label. The self-test gains a sixth mutation: offering the
  GM160 handoff as a resume link is caught.
- **CONTEXT-MAINTENANCE.md:**
  - §3 documents check 5;
  - §4 is corrected: `ALL-TOP-LEVEL-GOALS.md` is **not** historical. It holds the agents' goal texts, which TEAM.md
    names as governing. The first publish had listed it with START-HERE. The check found the mistake: it flagged
    TEAM.md's correct reference;
  - §4b maps each consumer pair in addendum §7 to the existing check that covers it. It names one uncovered gap:
    stale-preimage batch publishes, which reverted FABLE's S-36 correction in `95b1f3a4c`.
- **DASHBOARD-MEANINGS §6.4, the phase cap** (FABLE's ruling on SWE2-STRUCT's design). In the database phase only
  SPECIFICATION READY may show, under STRUCT's criteria plus "no UNMAPPED residue". Later labels appear only as
  probes. `readiness_view.py` (`8d5788541`) already enforces it.
- **The UC-1 ruling, test 1** (`fable-uc1-gamecode-route-ruling-1003`, amendment section). A "no direct reference" claim
  now needs a census covering:
  - E8/E9 calls and jumps;
  - `0F 8x` and rel8 jumps;
  - absolute pointers;
  - 32-bit image-relative fields.

  This follows SWE2-AUDIT-SPEC's REJECT of 15 of OPUS's 31 such claims (`4522aeff6`).
- **CONTRACT-the-moment-an-action-is-committed.md:** "called by 19 actor bodies" now reads "the ActorEntity ones among
  its 61 direct callers". This is a clarification, not a correction: a raw E8/E9 census gives 72 sites in 61
  functions, and the audit's graph gives 19 of them in ActorEntity. `check_consistency.py` had read the scoped 19 as
  the whole count.

## Checks

- `check_lifecycle_consumers.py`: FAILS 0 on the tree; self-test PASS, six of six mutations caught.
- The DASHBOARD-MEANINGS line endings were checked as consistent after the edit.

run: check_lifecycle_consumers.py --self-test at 042b50ca9 (FAILS 0, six mutations caught)
