# ScriptVM floating division guard — candidate79

Current canonical BF-1 says OPDIV tests a zero divisor on both paths, yielding0;
bf1_opcodes.py K9 verifies that a UCOMISS occurs but does not test its exact branch
predicate or NaN distinction. Does the float guard distinguish zero from
unordered, or does unordered route through the same zero result? This changes a
faithful arithmetic specification; no need to rerun completed name/NaN samples.
FABLE semantic BF-1 and OPUS comparator/VM contracts are named consumers.

Choose A first: original complete OPDIV handler0025F0AC..0025F1D6, exact float
guard operands/order/branches/common result block; current published BF-1 primary.
If source predicate settles the scoped claim (e.g. bare JE after UCOMISS without
JP distinction), preserve that conditional flag-domain fact. Retained77 actual
masked unordered flag observation may corroborate instruction behavior but is
not a new OPDIV execution or native exception proof; carry its initial incomplete
pipeline limitation. Do not repeat77 NaN guests or build a general VM harness.

Competing explanations: zero-only test, zero-or-unordered test, or operand/
branch identity wrong. Controls: exact guard instruction bytes/operand order,
zero result versus finite nonzero DIVSS path, ordered-positive predicate and
unordered flag tuple; negative-zero equivalence only if source predicate proves
it. Validate addresses by original table/name/handler bytes, not address arithmetic
alone. If prior flags are insufficient for a broader claim, keep it open instead
of treating source predicate as native execution.

Controls/checks: shared reviewed access-role adapter in actual capture/reducer,
store/read/LEA and affected RMW classification. Supplied flag truth-table is a
source calculation, never a list of original tests. Reject zero-only rewrite
when source includes unordered; no crash/native status claim from emulation.
Stop after the named discriminator; no exception experiments or live setup.

Preconditions: supported current board PASS and exact own bounded claim, no
active peer coverage of this float-guard question; freeze source/driver/inputs/
receipts, current committed consumer preimage plus separate dirty hash. Checker
present/compilable before preparation; no inspect.py stdlib shadow; no published
bytes overwritten. Cleanup: only offline reads/copies; no PC/game/save/config/
reference changes. S19 consumed extension remains unapproved. FullL1+L2 NOT_MET.

Learned: source JP25F19A exists and sends unordered to DIVSS; zero-or-unordered
hypothesis refuted. No need to replay77 flags/NaNs. XMM7 local zero setup at
25E55F and EBP1 at25E555 source-backed, not live initialization/callback proof.
First companion offset25E67B was mid-instruction; discarded as evidence, inert
source/note retained. Use actual branch target25E682/full64-byte decode plus
original table/name/handler identity. Producer/check validates this invocation
path. Stop the named guard question after sufficient source controls.
