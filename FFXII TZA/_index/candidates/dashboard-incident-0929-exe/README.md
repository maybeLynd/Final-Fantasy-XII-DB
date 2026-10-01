# Dashboard incident 2026-09-29: every view INVALID, "input snapshot exe does not match the manifest" (OPUS)

**What the user saw:**
- generation `g20260929T011558Z-a62a41`, committed 01:15:59Z;
- `INVALID: input snapshot exe does not match the manifest`;
- "last failed build: inputs moved during the build: team";
- all seven views INVALID.

**Status:** the first fix (225465c2e) was **REJECTED by SOL/ASTRA** (cccd7c04c, `_experiments/evidence/migration-dashboard-incident/`).
A same-length edit with its modification time restored escaped the server's stat-only cache key. The HTTP status then
reported no problems over bytes it had not re-checked. The served views were the cached original values, not the
tampered bytes. **Repaired and deployed; see section 8.** Non-author re-verification is PENDING. The controller build
path is PENDING (FRONTIER). Dashboard acceptance (A17/A19) stays open.

## 1. What was preserved

The evidence is in `Database/Tools/work/dashboard/_incident-20260929T015519Z/` (work area, not committed). It holds:
- the CURRENT pointer, `FAILURE.json` and `history.jsonl` as found;
- the failing generation's `MANIFEST.json`;
- the server and builder logs;
- the pre-change reader, `generation_before_external_9175ebf03.py`.

The failing generation directory itself is untouched in the store.

## 2. What "exe" is, and what failed

**The input.** The logical input `exe` is the certified game image,
`Database/Tools/work/exe/FFXII_TZA.exe`.
- The manifest records sha256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` and 32,864,752 bytes.
  That is the certified identity; the file did not change.
- It is declared `external` (`snapshot: False`): hashed and strict, but never copied into a generation or an export.
  External inputs were added at a5e9a1a0d (about 01:13Z).

**The comparison that failed.** The reader's `open_generation` requires, for every present input, a snapshot file
`inputs/<name>` whose hash matches the manifest. The newer reader skips inputs marked external. The older one does not
know the flag, so it looked for `inputs/exe`, found none, and reported a snapshot mismatch.

**Which reader.** The dashboard server, pid 66912, started at 01:04:53Z. It had loaded `generation.py` from before the
change. The same generation, verified from disk:

| reader | result |
|---|---|
| current `generation.py` | no problems |
| pre-external `generation.py` (9175ebf03) | `input snapshot exe does not match the manifest`: exactly the screenshot |

**Cause.** Reader/writer code skew in a long-running process. **Enabling defect (mine):** the manifest's semantics
changed without a format bump (`ff12-generation-1` both before and after), so the old reader misread the manifest
instead of refusing it as unknown.

**Rejected hypotheses:**
- the game EXE changed (its hash is the certified one);
- bytes were altered after sealing (every output and snapshot matches under the current reader);
- the wrong path or version was used (the manifest path is the certified file).

## 3. The two other findings

- **"inputs moved during the build: team" was a stale record.** `FAILURE.json` dated from 00:43:26Z, before the board
  was declared volatile (9175ebf03). Every later build succeeded, but the page still showed it as "last failed build".
- **No build ran after 01:15:59Z.** The controller process (pid 45016) has been running since 2026-09-28 16:16Z, which
  predates FRONTIER's `maybe_dashboard_build` hook. Its log holds zero `dashboard_build` events. Every generation so far
  was built by hand or by OPUS's stop-gap timer. Routed to FRONTIER.

## 4. The change (225465c2e)

**`gfz-scripts/generation.py`:**
- The manifest format is now `ff12-generation-2`, and the manifest records `verifier`, the writer module's sha256.
- A reader that meets a format it does not know returns **UNSUPPORTED** ("the reader is older than the writer; restart
  it"), never a guessed verdict. Formats 1 and 2 are both readable.
- `reader_stale()` reports when the module on disk differs from the code the process loaded.
- `commit()` verifies the **final on-disk** candidate with `open_generation`, the same function the HTTP server calls,
  before CURRENT is replaced. A rejected candidate is renamed `<id>.rejected` and kept; CURRENT and the success
  history are untouched.
- Every failure is also appended to `failures.jsonl`, with the generation current at the time.

**`dashboard/server.py`:**
- **Rejected CURRENT.** The server serves the newest generation in the success history that still passes
  `open_generation` with its recorded manifest hash. It is labelled **HISTORICAL**, with its id, commit time and the
  reason CURRENT was rejected.
- **Nothing verifies.** The server says "no verified generation is available" and serves nothing. Rejected data is
  never shown.
- **Stale code.** RESTART REQUIRED is shown when the server's own code or `generation.py` changed on disk since it
  started.
- **Old failures.** A failure older than the current generation is shown as resolved.
- **Cache.** The cache key also covers the fallback generation's files and the history log.

**The busy board:**
- It is volatile, so a board write during a build is drift, not a refused commit.
- Strict inputs retry at most three times.
- INVALID (internal corruption) and STALE (newer live inputs) stay distinct statuses.

## 5. Tests (executed by the author)

| test | cases | result |
|---|---|---|
| `test_generation.py` | G1-G15 (new: G13 a candidate failing the reader's verification never becomes CURRENT; G14 an unknown format is UNSUPPORTED; G15 stale reader) | FAILS 0 |
| `test_server.py` | S1-S16 (S5 now: a rejected CURRENT gives HISTORICAL from the last verified generation, tampered bytes never served; new: S13 none verifies, S14 failure ordering, S15 stale reader, S16 unsupported format) | FAILS 0 |
| `test_build_views.py` | B1-B6 | FAILS 0 |

A mutant with the fallback removed fails S5.

## 6. Deployment receipt

| time (UTC) | action |
|---|---|
| 2026-09-29T02:04:09Z | Stopped only the dashboard server (pid 66912). Started pid 46280 from commit 225465c2e. The controller and workers were untouched. |
| immediately after | The same generation `g20260929T011558Z-a62a41` verified clean: no problems; STALE (strict sources had moved); the old failure shown as resolved. |
| 02:04:53Z | A normal refresh while the board advanced (rev 38697 -> 38698) committed **`g20260929T020453Z-93e5fb`**, the working generation: format ff12-generation-2, verifier `b6ef5a5344f2`, exe external at `73461d089620`. All seven `/api/view/*` responses carry that one generation id; no drift; no problems. |

## 7. Still open (not closed by this record)

- **FRONTIER:** restart the controller process only, so `maybe_dashboard_build` (and `maybe_transitions`) run the
  current code. Until then the dashboard does not refresh by itself.
- **SOL (non-author):** execute the incident acceptance cases through the deployed HTTP path:
  - a valid on-disk snapshot passes;
  - a real snapshot mismatch is rejected;
  - a failed build keeps the prior complete generation;
  - board updates during a refresh are handled safely;
  - one normal refresh succeeds while workers are active;
  - all seven views come from one generation.

  Requested with a `reviews` field.
- **Lesson** (for the handoff): a long-running reader must detect its own code going stale, and a manifest whose meaning
  changes must change its format.

## 8. ASTRA's rejection and the repair (2026-09-29, OPUS)

**Finding (cccd7c04c, accepted as correct).** `State._key()` covered the pointer bytes, each file's name, size and
mtime, and the history log's stat. An output edited to the same length, with its mtime restored, changed none of them.
So a warm server never re-ran `open_generation`, and `/api/status` kept reporting "no problems" over content it had not
re-checked. The CLI verifier rejected the same file. My S5 test edited the file normally (a new mtime), so it could not
see this case.

**Repair (`server.py`, this publication):**
- **Every request:** the served generation's manifest bytes and every output are hashed against the manifest (the
  outputs are under 2 MB). Any mismatch forces a full `open_generation`, and the problem is reported.
- **At least every 60 s:** the input snapshots (up to about 81 MB) are re-verified in full.
- **Status** carries `verified_at` (the last full verification) and `verification` (the scope above), so the claim is
  the one actually checked. Everything else is unchanged: the HISTORICAL fallback, no data when nothing verifies, and
  UNSUPPORTED.

**Regression (test_server.py S17, ASTRA's counterexample):** a same-length edit to `view-vbf.json` with the mtime
restored is reported on the next warm request ("output view-vbf.json does not match the manifest"). The edited value is
never served, and status states its verification scope.
- The committed server fails S17 (FAILS 1) and the repaired one passes it (FAILS 0).
- test_server S1-S17, test_requirements MP1-MP10 and test_build_views B1-B6 all have FAILS 0.

**Deployment:** at 2026-09-29T03:03:28Z only the dashboard server was restarted (pid 65568 to 46136). The status for
generation `g20260929T025707Z-bffd92` shows no problems and `verified_at` 03:03:28Z, and all eight views come from that
one generation.

**Still open:**
- SOL/ASTRA re-verifies with the same counterexample (OPUS-REQ-ASTRA-REVERIFY-DASH-INCIDENT-CACHE).
- A same-stat edit to an *input snapshot* is detected within 60 s, not on the next request. That bound is stated in
  status.
