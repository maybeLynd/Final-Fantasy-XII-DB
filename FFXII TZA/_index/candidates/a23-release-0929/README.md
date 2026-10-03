# A23 release candidate receipts - g20260929T213407Z-9c7238 (SWE2-FRONTIER, 2026-09-29)

Deployment-owner evidence for `ASTRA-REQ-FRONTIER-A23-RELEASE-EXPORT-IDENTITY`. It names one release candidate and
binds what was served, what was exported and what code produced both. **It is not an A23 PASS**: acceptance needs
independent comparison against this candidate (REVIEW-POLICY; the release record stays DELIVERED, NOT ACCEPTED).

**2026-10-02:** that comparison exists and was independently accepted - ASTRA's retained packet
[`_experiments/evidence/a23-release-candidate-059ee3a6c/`](../../../_experiments/evidence/a23-release-candidate-059ee3a6c/README.md)
(f0322dd8, `verdict:ACCEPT` at 818e85de6) reproduced this candidate's ZIP/store/manifest/component bindings
byte-exact, with a mutation control refusing. The remaining predicates - module attestation, launcher, live
restart, current-version suite, live rollback - stay open; see
[`workflow/RELEASE-DASHBOARD-2026-09-29.md`](../../workflow/RELEASE-DASHBOARD-2026-09-29.md) section 7 and
[`frontier-incorp-a23-named-1002`](../frontier-incorp-a23-named-1002/README.md).

## What was run (one bounded run, 2026-09-29 21:37:17Z-21:37:20Z)

`release.py` (this directory; it refuses to overwrite a prior run) did, in order:

1. `GET /api/status` on the live listener `127.0.0.1:8765` -> generation `g20260929T213407Z-9c7238`, `problems: []`,
   `reader_stale: false` (`status-before.body`).
2. Read the store's `CURRENT` pointer -> the same generation, manifest sha256 `865299843d41...` (pinned).
3. **Guarded export**: `generation.py export <store> <zip>` (the only export path: it opens CURRENT verified, pins the
   generation, re-verifies the ZIP against the manifest before renaming it, then writes the sidecar) -> **exit 0**,
   `EXPORTED g20260929T213407Z-9c7238`.
4. `generation.py verify-zip <zip>` -> **exit 0**, `VERIFIED {"generation": "g20260929T213407Z-9c7238", "members": 35}`.
5. `GET /api/view/<name>` for all eight required views + `GET /` -> every one HTTP 200.
6. `GET /api/status` again -> the same generation, `problems: []`, `reader_stale: false` (`status-after.body`);
   CURRENT still the same generation with the same manifest hash.

## Results (`release-result.json`)

| check | result |
|---|---|
| served (before) = CURRENT pin = exported = served (after) | **equal**: `g20260929T213407Z-9c7238` |
| export ZIP | `Database/Tools/work/dashboard-exports/g20260929T213407Z-9c7238.zip`, 15,766,618 bytes, 35 members |
| ZIP sha256 / sidecar | `23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7`; sidecar names the same hash |
| ZIP `MANIFEST.json` sha256 | `865299843d41...` = the CURRENT pointer's `manifest_sha256` = the store folder's manifest |
| served view objects vs ZIP outputs | **8/8 equal** (progress, overview, systems, vbf, executable, types, evidence, fleet), each served with `meta.generation` = the candidate |
| builder `build_views.py` | manifest `82064835...` = HEAD blob; last path commit `cdbf25a5d` |
| `requirements.py` | manifest `02cd6ce8...` = HEAD blob; last path commit `69bbf8c81` |
| `uc1_band.py` (declared input) | manifest `746b6fab...` = the worktree file, clean against HEAD (`git hash-object` = HEAD blob `9f4563f2`); the sha differs from the raw blob only by CRLF checkout (`core.autocrlf=true`) |
| verifier `generation.py` | manifest `e4e74924...` = HEAD blob; last path commit `b6e6de3f0` |
| server `server.py` | on-disk file `34d73084...` = HEAD blob; last path commit `7c14ecf56` (2026-09-29 11:37:03Z) |

HEAD at the run: `5a2435b23`.

**Drift, stated rather than hidden.** `/api/status` reports `drift: {"requirements.py": "changed"}` for this
generation: at 21:35Z a peer began an **uncommitted** edit of `Database/Tools/dashboard/requirements.py` (MP-3). The
candidate was built from the committed blob, which is why it is the candidate: a generation built after that edit would
bind to uncommitted source. The drift marks the generation STALE against the working tree, not invalid.

## Process identity (`process-identity.txt`) - MEASURED

`netstat -ano` names the `127.0.0.1:8765` listener **pid 68280**; `Win32_Process` gives its creation time
**2026-09-29 11:38:14Z**, image `C:\Python314\python.exe` and command line
`server.py --root ...\Database\Tools\work\dashboard --port 8765` from the shared checkout (parent process no longer
exists). The process started 71 s after `7c14ecf56` committed the current `server.py`. **Loaded-module identity is
indirect**: `reader_stale: false` is the server's own comparison of the sha it loaded against the file on disk (and the
verifier's); no external module attestation was taken. The release record's section 1 pid (71184, 07:33Z) is historical.

## Rollback drill (`rollback-result.json`, `rollback_drill.py`) - EXERCISED on a spare port

The record's rollback procedure was exercised without touching the live server: `git archive 763d466d6` of
`Database/Tools/dashboard` + `generation.py` into a scratch directory outside the tree (same effect as the record's
`git worktree add --detach` step, without a full checkout), then that older server started on **127.0.0.1:8766** against
the same store (child pid 26556). It answered `/api/status` HTTP 200 with the candidate generation, `problems: []`,
`reader_stale: false`, and its served progress view equalled the store's `view-progress.json`. The live 8765 listener
served the same generation during the drill. The drill stopped only its own child (by handle; exit 1 = Windows
TerminateProcess) and port 8766 then refused connections.

## Not exercised, and why

- **Launcher** (`START-DASHBOARD.cmd`): not run. With a listener present its only branch opens a browser on the
  operator's desktop and exits; the build+serve branch needs the live server stopped. Static read only.
- **Live restart**: not performed and not needed - the running code equals HEAD `server.py` (`reader_stale: false`,
  process start after the last server commit). Restarting would interrupt the operator's view for no identity gain.
- **Test suites**: `test_generation.py` G-suite re-run on an isolated HEAD copy: **FAILS 0** (it uses a temp store).
  The dashboard suites (`test_server`, `test_build_views`, `test_requirements`, `test_live`) read tracked and ignored
  inputs from the live tree, and the tree's `requirements.py` is currently a peer's uncommitted edit, so a run now would
  test undeployed code; an isolated copy lacks their inputs (its failures were environment-induced and are not
  reported as results). The author runs in the record's section 4 stand for the code at `763d466d6`; the candidate's
  builder/requirements/server commits are later (`cdbf25a5d`, `69bbf8c81`, `7c14ecf56`) and were not re-tested here.
- An earlier export `g20260929T210933Z-e40dd5.zip` (21:12:52Z) was left by a previous executor of this lane with no
  retained served-status or verifier receipt. It is **not** the candidate.

## For SOL (independent comparison)

Compare the ZIP to the served generation yourself: `verify-zip` it, hash its members against the store folder
`Database/Tools/work/dashboard/g20260929T213407Z-9c7238/`, and bind the manifest's source hashes to Git blobs. The
store folder and the ZIP are retained; CURRENT will have moved on by the time you read this, which is expected.

## Repair 2026-09-30 (SWE2-FRONTIER): the source lookup ignored Git exits (ASTRA-REQ-FRONTIER-A23-GIT-LOOKUP-ADMISSION)

ASTRA found (and reproduced with real Git, `work/ASTRA/migration-a23-current-release/source-binding-prerequisite-01/`)
that the first `release.py`'s `headsha()` never read the exit codes of `git show` / `git log`: a failed lookup (a
missing `-C` directory gives exits 128/128) came back as `SHA256(b"")` and an empty commit, a normal-looking digest.
The candidate's binding above was not affected in fact - every lookup in that run succeeded - but nothing in the
helper would have said so had one failed.

- **`source_lookup.py`** (new): every Git call keeps its argv, exit, stderr and stdout size; a lookup is `ok` only when
  `git show`, `git cat-file --filters` and `git log` all exit 0 and the last commit is 40-hex. `bind()` returns
  `equal=None` / `INCOMPLETE` for a failed lookup or a missing recorded hash - never a match or a mismatch - and
  names which form matched: the raw blob, or the checkout (eol-filtered) bytes. That second form is why the first
  run printed `uc1_band.py equal: false` while the file was clean: the manifest recorded the CRLF checkout.
- **`release.py`**: the source-binding block now resolves HEAD once (checked, recorded as `source_rev`) and binds every
  component through `source_lookup.bind()`. The capture itself was not re-run.
- **`test_source_lookup.py`** (real Git, no mocks; output `test_source_lookup.out`): P1 positive lookup equals an
  independent `git cat-file blob` digest; P2 raw-blob bind; P3 checkout-form bind (`uc1_band.py`); P4 a real mismatch;
  F1 missing `-C` directory (exits 128/128/128, `INCOMPLETE`, no digest); F2 path absent at the revision; F3 unknown
  revision; F4 no recorded hash; F5 the empty-stdout digest is never returned on failure. **FAILS 0.** A mutant that
  restores the old behaviour (exits ignored) fails F1, F2, F3 and F5.
- **`rebind.py`** -> **`rebind-result.json`**: the candidate's recorded hashes re-bound with the checked lookup at the
  run's HEAD `5a2435b23` (no recapture): `build_views.py`, `requirements.py`, `generation.py`, `server.py` BOUND (raw
  blob), `uc1_band.py` BOUND (checkout form); `all_bound: true`. The candidate's source identity stands.
