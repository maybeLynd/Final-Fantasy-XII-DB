# A03 configured verdict parser — independent REJECT

The helper's public custom-line boundary accepts a recognized required **FAIL**.
An exact fixed tab-separated pattern recognizes `FAIL\tA\trequired failure`;
the upstream exits0 with a misleading `FAILS 0` footer, and the actual composer
subprocess nevertheless exits0 and prints COMPOSER_PASS. The same-format PASS
positive works. Default format rejects the tab failure as malformed.

Cause: the configurable parser recognizes the captured PASS/FAIL group, but the
helper detects failures only with literal `startswith('FAIL ')`. A matching FAIL
without that space bypasses the required failure condition. OPUS owns repair at
the actual helper and a regression through the composer; ASTRA changes no peer file.
This is a valid documented `line` configuration, not a replaced helper or stub.

Other bounded observations preserve the valid behavior: default upstream FAIL/
nonzero/missing/exception/malformed/changed-set/same-count/missing-object/footer
refuse composition; explicit validated complete data may accept named findings
exit1, whereas exit2 and a half-built object refuse. Names-only means presence,
not arbitrary shape correctness; a caller-specific validator is needed for that
promise. The external composer deadline is explicit, not an intrinsic deadline
in the in-process helper. Sixteen cases retain input/declaration/source/stdout/
stderr/exit/timeout, not blanket full integration acceptance.

The requested authored first-adopter test_sn1_prereq.py was actually re-executed
and exited0/FAILS0, separately labelled. Its source/output is pinned; its complete
native/resource input closure is not independently sealed here. No new SN1 table
census, native interpreter reachability or storage/lifetime fact follows. The
legacy helper has the same textual predicate by source inspection; its custom
format needs owner followup, not a claim that ASTRA executed that legacy boundary.
Default and current single-space consumers are not automatically invalidated.

Method A: original software helper copied byte-for-byte at de83673fd and synthetic
private Python inputs; actual composer subprocesses, no shipping FF12 instructions,
game process, PC controls, save/config/reference mutation or production edits.
The scientific result is REJECT at this configured API boundary. `python check.py`
validates the retained receipt without rewriting it; do not overwrite an old run.
Freeze driver/inputs/cases/raw/result and independent re-review exact repaired code.
Migration M0–M5 and the full L1+L2 database remain NOT_MET.
