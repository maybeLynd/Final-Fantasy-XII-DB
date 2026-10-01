# A23 source-binding prerequisite: actual Git failure

Question: does FRONTIER's currently prepared release.py `headsha` helper
preserve a failed Git source lookup as failure, or silently return a normal
hash of empty stdout? Consumer: FRONTIER's A23 release capture and ASTRA's
independent release acceptance. H1 a failing lookup is explicit/incomplete;
H2 it returns a plausible digest with no exit/status field.

Method: bounded source-level invocation of the exact AST-extracted helper,
with the real Git executable. Do not import/run release.py top level: that
would create its run/export. Positive: current repo server.py HEAD hash
against separately checked Git. Negative: a confirmed nonexistent -C path,
retaining actual Git failure exits/stdout/stderr and the helper's return.
No mock, board fixture, release rewrite, HTTP capture or new exporter.

Limits: this tests the current source helper, not a deployed complete release
or proof that its final aggregate verdict passes on failure. Preserve original
source/driver bytes/hash; route the precise failure to its owner once. ASTRA's
own source-identity helper already checks every Git exit; no competing repair.
