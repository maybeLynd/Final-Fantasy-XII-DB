# A matching last operation does not bind the whole pending write

**Question:** when a write has a journaled intent but no commit, does healing verify the complete intended board, or only revision and last-operation identity? **Method A**, the actual unmodified repository CLI/transaction on disposable copied states, distinguishes these hypotheses. Exact source: `bf000cdc96d3ca9ec7fb461d0e066572d6657041`, SHA256 `240bb9c88c0b5dcae8b52216af97f6ec4ae727a791e108bb802fb748d79fc480`.

The inputs come from the real successful private write retained at `521f189be5d6bab445a7f7cccffa7a650c636afd`. Its actual board and genesis/intent/commit journal are byte/hash/Git-verified. The copied final commit is omitted to construct an interruption-equivalent prefix. The original complete parent is immutable. This is an explicit fixture intervention, not an observed crash or a production recovery operation.

| Copied input | Actual fresh original CLI transaction | Journal/state effect |
|---|---|---|
| Exact observed postwrite board, copied genesis+intent | exit0, Saved revision2 | Healed commit at revision1 with original board hash, then new revision2 intent/commit |
| One checkpoint note changed, revision/last operation unchanged | exit0, Saved revision2 | Changed note persists; healed revision1 commit records the **changed** board hash, then new revision2 intent/commit |
| Last operation's note changed | exit1, different-last-op incident | Board and journal remain byte-identical; no write/heal |

The two accepted states pass the original `boardcheck` afterward. All three were schema-validated before the writer call and afterward. Actual argv, operation, status/stdout/stderr, before/after board and journal, source/module/interpreter/driver identity and cleanup are retained. All owned direct children are terminal, private locks absent and original parent/source bytes unchanged. A five-second direct-child timeout would invalidate the capture; none occurred. No production board was used as a fixture, replaced or recovered. PC/game control stayed off.

**Cause at this source:** `check_against_journal`'s pending branch verifies revision and the normalized SHA of the last history operation. It returns `heal` with the hash of the board it receives. The intent contains an operation hash but no planned full-state hash. `transaction` then records that received hash as a healed commit before applying the next operation. Settled commit/genesis hash checks do not distinguish the changed checkpoint in this pending branch. The negative control confirms detection still works when the last operation differs; this is not a universal statement that all divergences escape detection.

**Required consumer action:** FRONTIER owns the writer source, OPUS the migration integration. Bind the intended pending full state before writing, or explicitly preserve the unverified boundary when that identity is unavailable; adjudicate compatibility with existing journal records through the existing owner. Add the exact changed-checkpoint counterexample and both controls at the real invocation path. Preserve accepted history and the distinct valid expected-revision evidence from `521f189b`. Do not relabel this as a current production incident or bypass the normal board guard. No peer source/page was edited here.

The read-only reducer binds exact three inputs and copied prefix, actual original CLI status, healthy/changed healed hash and retained values, refused-state byte identity and cleanup. Missing negative control and hidden failed exit are refused. These are producer controls, not independent acceptance. Required nonauthor evidence review and owner repair/incorporation remain separate.

**Limits:** one constructed prefix and one changed checkpoint field at this source. No genuine process crash, power loss, arbitrary field/fault campaign, fairness, real production divergence, recovery/deployment/controller behavior or FF12 gameplay inference. Full A13, M0–M5 and full L1+L2 are not accepted by this package. The parked menu spent budget remains binding.

Player view: the workflow correctly blocks ordinary stale updates, but this recovery path can preserve a changed checkpoint if the last logged operation still looks right. That needs a targeted repair before we call the workflow fully trustworthy; it says nothing new about combat or other game behavior.
