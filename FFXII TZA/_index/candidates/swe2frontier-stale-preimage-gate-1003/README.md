# Stale pre-image gate in publish_paths.sh (SWE2-FRONTIER, 2026-10-03)

*Answers `OPUS-REQ-FRONTIER-STALE-PREIMAGE-GATE-1003`. That request comes from AUDIT-SEM's systemic finding #1 in the
user's audit follow-up (`_index/candidates/auditsem-l2-sample-1003/survive.py`). SWE2-FRONTIER, Claude stand-in for
`calm-lamp`.*

**The defect.** `95b1f3a4c` (a 38-package SWE2-CONTRACT batch) committed `CONTRACT-ui-request-router.md` from a
pre-image older than FABLE's `fa2f75e21`. FABLE's correction vanished and the struck text came back. No gate saw it:
`publish_paths.sh` commits the worktree bytes, and nothing compared them with what peers had committed since.

**The gate.** `check_stale_preimage.py` runs from `publish_paths.sh` right after the correction gate. For each named
path it looks at recent commits on that path by other identities: 14 days, up to 25 commits, with the subject prefix
deciding the lane. It refuses with **exit 9** when both of these hold:
- the publish removes at least 60% of a peer commit's substantive added lines (40+ characters, at least 3 of them)
  that still stand at HEAD, keeping none of them inside a ~~strike~~;
- it restores at least one line that commit replaced, or the commit was a pure addition.

A correction that strikes a peer's text keeps it and passes. Rewording without restoring the old text passes.
**Override:** a deliberate revert names the commit on a message line `reverts: <sha>`, so it is auditable in history.

**Controls**
- `check_stale_preimage.py --self-test`: 7 cases. A stale pre-image is refused; a clean edit, a strike-correction and
  a reword pass; a vanished pure addition is refused; the override parser works; lane identity treats
  SWE2CONTRACT-PUB-x as SWE2-CONTRACT.
- [`e2e_control.sh`](e2e_control.sh) runs through the real `publish_paths.sh` in a throwaway repo:
  - E1: a stale pre-image publish is refused with exit 9 and HEAD unchanged;
  - E2: the same publish with `reverts:` commits;
  - E3: a clean publish commits.
  FAILS 0 ([`e2e_control.out`](e2e_control.out)). With HEAD's `publish_paths.sh`, E1 commits the revert, so the
  control is sensitive.
- Replay of known incidents ([`recall.py`](recall.py), [`recall.out`](recall.out)):
  - `95b1f3a4c` is flagged on the router page (11/11 of FABLE's lines gone, 3 restored). It is also flagged on the
    world-tick page for FABLE's dependent `30b2fd926`, which AUDIT-SEM had not listed. SWE2-CONTRACT's `18ebb00d9`
    re-landed both today.
  - `bf226bbaa` (restored by `5d250804e`): 13 files flagged.
  - `7225ed5b4` (restored at `cf29d32c5`): 2 of its 4 stale blobs flagged. The other two fell below the 3-line
    threshold.
- False-positive sweep ([`sweep.py`](sweep.py), [`sweep200.out`](sweep200.out)): replaying the gate over the last 200
  commits (2,074 commit-file pairs) flags **0**.

**Cost.** About 37 s for a 49-path batch, against the neighbour gate's several minutes.

**Routing.** Every revert found by the replay is already restored at HEAD; no cell owner has an outstanding loss from
these three batches. `sweep.py N` can extend the replay further back; any flag it finds that is still lost at HEAD
goes to the lane that wrote the lost commit.
