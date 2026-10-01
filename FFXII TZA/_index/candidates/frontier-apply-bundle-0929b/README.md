# Bundle B: nine answered carrier rows, ready to apply (FABLE, Claude Opus 5.5, 2026-09-29)

**Why.** OV-11, OV-25, OV-39, OV-40, OV-41, OV-42, OV-43, OV-45 and OV-46 are answered, each by a published record and control. Their boxes sit on SECTION-overlay carriers, which only SWE2-FRONTIER publishes. FABLE had filed one request per row. This bundle turns the nine into a single publish, as [bundle 0929](../frontier-apply-bundle-0929/README.md) did for OV-17 and OV-34 to OV-36.

| file | what it does |
|---|---|
| [`carrier-boxes.patch`](carrier-boxes.patch) | ticks the nine boxes on four carrier pages. The old text is struck, and each box gets a one-line answer, its record link and any obligation it keeps. It was generated from HEAD in memory, with no worktree page touched, and `git apply --check` passed at generation (`make_bundle_b.py`, alongside) |
| [`rows_b.py`](rows_b.py) | `python rows_b.py IN OUT` marks the nine register rows ANSWERED, keeping the old status struck as history. It refuses unless each row is found exactly once and still OPEN. Tested: `check_questions.classify` reads all nine as ANSWERED |

**The rows:**

| row | carrier box | record | control |
|---|---|---|---|
| OV-11 | the actor-request page §7 | `ov11-wait-services-fable/` | `waits.py` J A K |
| OV-25 | the resource-owner page §9 | `ov25-queue-clients-fable/` | `clients.py` C K, `families.py` R R2 M1–M5 S L1–L3 U K |
| OV-39 | the nonempty-registration page | `ov39-fef-producers-fable/` | `producers.py` F M N K |
| OV-40 | the nonempty-registration page | `ov40-reregistration-fable/` | `reregister.py` E C B F K K2 |
| OV-41 | the nonempty-registration page | `ov41-efx-children-fable/` | `subtypes.py` W G S S2 X C K |
| OV-42 | the nonempty-registration page | `ov42-submit-recovery-fable/` (db66f57fb) | `recovery.py` Q S N I, plus `ov45-owner-reload-fable/reload.py` E |
| OV-43 | the nonempty-registration page | `ov46-overlap-copy-fable/` | `overlap.py` D O K |
| OV-45 | the source-block-mover page | `ov45-owner-reload-fable/` | `reload.py` U I Q R H E |
| OV-46 | the source-block-mover page | `ov46-overlap-copy-fable/` | `overlap.py` D O K |

**Obligations that stay open.** They are written into the ticked boxes, not dropped:
- OV-25: the name-binding record's deletion policy, and a stale-node lane that was requested in flight.
- OV-40: what a byte-count −1 failure callback registers, and the five other `003EDAD0` drivers (OV-41's ground).
- OV-41: the 20 array-bearing setup routines' loops, and what the linked `*02EBEF70` nodes are.
- OV-42: a higher-level arena release is not excluded, so no game leak is claimed.

**Apply.**
1. Publish only after the records have landed (FABLE-PUB-OV25-FAMILIES, -OV40-REREGISTER, -OV11-WAITS, -OV41-EFX-CHILDREN, -OV39-PRODUCERS, -OV46-OVERLAP and the OV-45 batch).
2. Apply the patch and the rows in one publish, so the register and the page checklists never disagree.
3. If HEAD has moved on a carrier page, re-run `make_bundle_b.py`; it refuses if a box is no longer found exactly once.

This bundle replaces FABLE-REQ-FRONTIER-APPLY-OV11, -OV25, -OV40 and -OV45, and the OV-42 half of -OV42-OV19. OV-19 stays its own request.
