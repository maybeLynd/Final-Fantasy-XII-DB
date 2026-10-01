# Packed script-reference offset carry — bounded question 76

Question: does PUSHP unconditionally preserve class bits and force width exactly
7, or does an unmasked 32-bit offset+scaled-index result contribute upper bits?
Major system: Script VM reference representation; FABLE semantic page, OPUS
descriptor/ABI contract, DATA affected specifications, SPEC independent review.

Known: canonical PUSHP section lists AND offset24, AND original class bits,
ADD scaled index, OR saved class, OR70000000. Package74 proves only source
flatten arithmetic is low32 then read signed; actual shipped large shapes and
storage validity remain open. No evidence that computed offset remains24bit.

Method A first: verify shipping image/reader/address identity and complete PUSHP
instructions through normal epilogue, scaling and jump-table cases, then trace
exact packing sequence. Conditional arithmetic is sufficient if no later mask
or rejecting branch appears; it is NOT isolated original execution or a live
reference. Escalate B only if source cannot distinguish the alternatives.

Controls: a within24-bit offset, positive carry into previously-clear class bit,
negative computed offset carrying sign/high bit; compare final-mask and forced7
alternatives. Check actual shared access adapter for stack write and LEA address
computation. Stop on identity/extent/control ambiguity; no guessed execution.
Retain immutable primary preimage/source/raw/reducer/default and fault controls.
No shipping malformed-input safety/caller/bank/native fault/live claim. No more
guest RC tests; PC OFF. S19 spent budget/unapproved extension persists.

Learned preparation constraints: never name a helper inspect.py (it shadows the
stdlib module imported by Capstone/Unicorn). Preserve its failed source inert;
actual capture/default asserts callable inspect.getfile and external module
origin. This import failed before image/code read, with no accepted conclusion.
First capture also stopped on a dirty peer consumer preimage before raw/result;
use a recorded immutable git-show view and disclose working hash, not assumption
that current working bytes belong to that commit. Do not alter peer changes.
