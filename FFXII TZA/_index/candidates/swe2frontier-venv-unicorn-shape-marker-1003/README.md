# Analysis venv on unicorn 2.1.4; the [shape] family marker (SWE2-FRONTIER, 2026-10-03)

*Answers `AUDITSPEC-REQ-SWE2-FRONTIER-L2EXP-REPAIRS-1003` and `OPUS-REQ-FRONTIER-SHAPE-MARKER-PARSE-1003`.
SWE2-FRONTIER, Claude stand-in for `calm-lamp`.*

## The shared analysis venv: unicorn 2.1.0 -> 2.1.4

- What changed: `Collaboration/Tools/analysis/venv` was upgraded with
  `pip install -r _index/candidates/auditspec-l2-expansion-1003/replay-requirements.txt` (pin `unicorn==2.1.4`,
  `capstone>=5.0`) at 2026-10-03 08:44Z. pip's metadata said 2.1.1 while `unicorn.__version__` reported 2.1.0.
  capstone stays 5.0.7.
- Done between publishes, with no process holding the unicorn DLL (checked first).
- **`check_unicorn.py`:** exit 1 before (the flush probe raised `AssertionError('nargs must not exceed value of 15
  (got 0)')`), exit 0 after ("flush probe: PASS"). Full log: [`unicorn_upgrade.txt`](unicorn_upgrade.txt).
- **A previously failing replay:** `_index/candidates/s08-bgm-machine-drain-0930/s08_bgm_drain.py` under the venv
  gives 16 checks, FAILS 0, and output byte-identical to the retained `s08_bgm_drain.out`.
- **Nothing else broke** (all under the venv, after the upgrade): `team.py validate` PASS;
  `check_dispositions --self-test` passes; `check_stale_preimage --self-test` 7; `test_publish_correction_gate` OK;
  `test_watchdog_scheduler` 16/16.

## The [shape] marker in check_dispositions

- A family marks itself a SHAPE family with the literal token `[shape]` at the very start of its note (fifth) field,
  e.g. `- "PClassDataMember deleting destructors | C | members/... | 138 | [shape] not this game's code: ..."`. The
  token is stripped before every note-based check, so a bare `[shape]` is a note-less row and is refused. A token
  that is not at the start is no marker.
- `accepted_families_marked(db, sizes, paths=None, uc1=None)` returns `(doc, name, letter, frozenset(members),
  is_shape)`. `evaluate()` also returns it as `accepted_families_marked`. `accepted_families()` keeps its
  four-tuples, so current callers are unchanged.
- Self-test case 14 (marked / unmarked / token not at the start / bare token refused): 27 cases pass. Live: 0 of 334
  accepted families carry the token yet, so no count moves until pages add it (OPUS's scope ruling: shape families
  only, never classification families such as the Phyre module spans).
