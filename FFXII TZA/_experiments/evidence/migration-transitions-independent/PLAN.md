# Independent review → repair/incorporation routing

Question: do current published transition tools admit only well-formed independent
review data, produce the correct next owner once, and preserve actual supported-writer
status when called through CLI? Consumer OPUS technical owner; FRONTIER deployment
and full host/cancel/quota behavior remain separate obligations.

H1: valid structured input produces one correct task; malformed evidence/link or
inappropriate self acceptance produces no operation and an explicit refusal. H2:
truthy malformed link fields or self-review can create a task, duplicates can escape
the writer, or a caller reports success without a valid completed upstream write.

Method A suffices: actual Python tools, labelled disposable fixtures. Read requirements
and original current source before producer tests. The existing request specifically
authorizes disposable --board/--apply tests; no production board creation/recovery,
global apply, controller restart, board replay or peer ownership change.

Derive and preserve controls: valid REJECT; valid ACCEPT with named owner other than
author; valid no-separate-owner ACCEPT recorded without operation (current convention);
missing/conflicting verdict; verdict only in prose; malformed reviews string; missing
commit; non-SHA/typed commit or typed record; invalid author; self-review. Explicit
commit is a SHA per the tool convention, not any truthy object. Distinguish invalid
input handling from success. Run sequential idempotence and two simultaneous actual
CLI applications through unmodified supported team.py, checking final board/journal.

Use exact copied published code in a private mirrored source root; assert team.ROOT,
BOARD and JOURNAL_DIR all stay inside it. Minimal validated fixtures retain current
identity/schema/phase rules; all dummy work is labelled. No existing peer tasks copied
as mutable experiments. Preserve inputs and before/after boards, subprocess argv,
stdout/stderr/exit, source identity and journal receipts; every child bounded/reaped.
Unpublished owner edits are excluded/limited rather than silently tested as accepted.

Malformed/no-case/partial/exception status cannot receive acceptance. If a concrete
defect appears, publish the smallest actual counterexample plus valid control and
route cause/affected consumers; do not edit claimed production tools. Stop repeating
a settled case. Current routing convention lacks automatic handover when no separate
incorporation owner is named; absence of AUTO-INCORP alone is not a routing defect.
Whole M0-M5/L1+L2 remains NOT_MET; ordinary checkpoints continue the active goal.
