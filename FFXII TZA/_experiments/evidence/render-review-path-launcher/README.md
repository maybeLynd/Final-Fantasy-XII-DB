# Explicit import path for the committed publisher-path control

The controller from88d435193 failed before testing the predicate: its unchanged
legacy publisher copy derives ROOT from a fixed ancestor depth and could not
import team from the new tracked location. The failed status/stdout/stderr are
retained here; no valid empty result was produced. Original published inputs,
controller and publisher source remain immutable.

launch.py pins those two committed sources and supplies the repository kit
import path before executing the unchanged controller. That controller overrides
ROOT/W/board only for its labelled private fixture before calling prepare().
This is a dependency-resolution correction, not a real board/publication test.

Commit launch.py first, then run it with one fresh ignored output file. Seal
with all three driver identities: launcher, unchanged controller and unchanged
publisher source. Keep failure01 invalid; only the fresh actual run can qualify
the two case IDs. Independent procedure review remains required.

No FF12/native/PC/input/save/config/reference or peer process changes. The full
L1+L2 goal remains active; no semantic or extra reviewer execution credit.
