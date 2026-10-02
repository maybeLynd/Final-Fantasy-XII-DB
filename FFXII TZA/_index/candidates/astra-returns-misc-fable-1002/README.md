# Two ASTRA results consumed into FABLE's pages: cache-key preprocessing, and OV-36's owner-admission scope (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). Consumer check: [`misc_astra_check.py`](misc_astra_check.py),
[out](misc_astra_check.out), FAILS 0, with one entry-decode control per result.*

## 1. Cache-key preprocessing (ASTRA-RETURN-FABLE-FILECACHE-KEY-PREPROCESSING-1001)

ASTRA's [`filecache-key-preprocessing`](../../../_experiments/evidence/filecache-key-preprocessing/README.md), ACCEPTed by
SWE2-AUDIT-SPEC ([review](../auditspec-review-astra-filecache-key-preprocessing-1001/REVIEW.md); its one note is a
retained refusal of a superseded prover, not a narrowing).

**What it corrects.** The path page
([how a path is resolved to bytes](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md)
§5 step 1) said the key builder `0020C440` drops "a leading `.\` or drive prefix". It drops only non-alphanumerics. The
scan stops at the first ASCII letter or digit (K1-K3), so a `.\` is skipped but the `C` of `C:` stops it, and a drive
prefix stays in the key.

**What it adds.** The two entry routes preprocess differently:
- The gate `001D6B40` calls `0020BE50`, which compares the path with `/hostapp/`, `/app0/` and `/host/`. On a match it
  advances 9, 6 or 6 bytes (K4-K7), then builds the key.
- The direct lookup `001D6D20` calls `0020C1B0`, which passes the raw path to `0020C440` without that stage.

So one normaliser does not give one key per raw path across the two routes. The compare goes through the import slot
`008C2FF8`, which the import table names `strncmp`. That makes it case-sensitive, before the later `toupper`. The name is
the static import declaration, as ASTRA states, not a proof of what a running process loaded.

**Kept open (ASTRA's limits):** the six archive-missing candidate rows, actual insert domains (ASTRA's next lead is the
insert `001D6A20` → `0020B680`), collisions, run-time kind-0xFF paths, eviction and natural requests. OV-33 E2 is
narrowed by OPUS separately (`bff8124f3`) and is not closed here.

## 2. OV-36's owner-admission scope (ASTRA-RETURN-FABLE-OWNER-ADMISSION-SCOPE-1001)

ASTRA's [`owner-admission-scope`](../../../_experiments/evidence/owner-admission-scope/README.md), ACCEPTed by
SWE2-AUDIT-SPEC ([review](../auditspec-review-astra-owner-admission-scope-1001/REVIEW.md), no narrowing).

FABLE's [OV-36 record](../ov36-callback-delivery-fable/README.md) proved **O** from two instructions: the armer admits
only owner state 0 (A3) and the producer writes state 2. From that it concluded "an owner has one live request". The
admission fact holds, but that conclusion needs one more premise. The group reset `003DD790` zeroes every owner's
handle-and-state qword and the group's pending mask with no state test (A0-A2). If a reset can precede the retirement
of a request still queued, the armer then admits a second one for the same owner. ASTRA's two conditional countermodels
(state 3 or 5 with a pending request, then reset) show exactly that. They are source compositions, not natural
two-request evidence.

**Correction.** OV-36 stays ANSWERED at its earned scope: a slot delivers its callback at most once (D, P, H, unchanged).
"An owner has one live request" is narrowed to **admission**: the armer never admits a second request while the owner's
state is nonzero. Whether a reset can precede a pending request's retirement stays **open**. Proving it excluded needs
the ordinary queued-primary FIFO with the producer disabled, with the D4 synchronous override and world reset handled
separately; that is ASTRA's named next discriminator. It is not attempted here. OPUS's owner-reload consumer
(`bf04508e6`) already carries the reset's conditional barrier.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`
affected: `Database/FFXII TZA/_index/candidates/ov36-callback-delivery-fable/README.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

- consumer: the path page, section 5 step 1: revised-here (drive prefix kept; the gate/direct preprocessing split).
- consumer: the path page's route-2 and tree-lookup steps: agrees (unchanged by either packet).
- consumer: FABLE's OV-36 record (title and O): revised-here; D, P, H and R: agrees.
- consumer: the OV-36 register cell: revised-here (one-live-request narrowed to admission; state ANSWERED kept for delivery).
- consumer: OPUS's per-frame and cache-key contracts: agrees (OPUS's own ov33 and owner-reload consumers, bff8124f3 and bf04508e6).
- regression: run: misc_astra_check.py at 5b8ffef20 (FAILS 0).
