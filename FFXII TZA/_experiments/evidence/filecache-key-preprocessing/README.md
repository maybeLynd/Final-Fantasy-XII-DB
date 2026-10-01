# Original cache-key preprocessing: two paths into one normalizer

Method A, exact FF12 image
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Producer SOL in ASTRA; independent acceptance/canonical incorporation pending.
Consumer: FABLE path-resolution/OV33 E2 records and OPUS cache-key contracts.

The leading scanner in 0020C440 stops at the first ASCII alphanumeric. A
generic drive prefix beginning with C is therefore retained at the later
copy/case-conversion stage. The canonical path page's statement that this
scanner drops a drive prefix is too broad. It skips a leading .\\, for example;
it does not skip C:. The exact byte classifier equals the 62 ASCII letters and
digits for all 256 byte values. This is finite arithmetic from verified
instructions, not 256 original-code or live tests.

The gate and direct lookup also preprocess their raw paths differently:

- 001D6B40 -> 0020BE50 compares against /hostapp/, /app0/ and /host/, advances
  its path by 9/6/6 respectively on equality, and then calls 0020C440.
- 001D6D20 -> 0020C1B0 passes the original path into 0020C440 without that
  prefix-removal stage.
- The original import declaration at 008C2FF8 names strncmp, not _strnicmp.
  Thus the named CRT contract makes this prefix comparison case-sensitive
  before the subsequent toupper conversion. Static IAT declarations do not
  prove which targets/locale a running process actually loaded.

The shared normalizer and tree do not imply equal keys for every identical raw
input at these two API boundaries. Seven bounded ASCII illustrations preserve
that distinction: unprefixed paths agree; each of the three exact lowercase
prefixes differs; uppercase /HOSTAPP/ is the nonmatching control; C: and .\\C:
both retain the drive prefix. The illustrative 31-bit values use the retained
original signed-byte, modulo-32-bit *33/add and final BTR31 instruction order,
under explicit C-ASCII toupper/normal ABI/nonaliasing premises. They are not
native executions or actual cache entries. The three lowercase-prefix examples
have distinct gate/direct numeric hashes as well as distinct normalized text.

This narrows a prerequisite of the E2 investigation, not the whole E2 row.
The six archive-missing candidate rows, actual cache insert domains, collisions
against the archive namespace, runtime-built kind-FF paths, eviction between
lookups and natural issued requests remain separate. No archive/FST census,
game session, live read or injected native call occurred. Do not count this as
the reviewer's prior corpus run or claim a natural collision/absence result.

Producer checks: positive02 completes with six closed local CFGs and exact
body/tool/import/literal pins. Four actual CLI controls refuse failed upstream
status, an original but incomplete prologue, altered prefix data and a wrong
comparison-import attribution. Missing output/nonzero exits are refusals, not
valid empty successes. The shared reviewed access-role adapter is invoked by
the actual capture and re-decoding validator, with store/LEA/RMW controls.

Retained failed hypotheses/procedure: source01's 43-byte .pdata normalizer
fragment ends in a fallthrough, so it cannot settle normalization. Source02
closes that routine through RET20C550; neighbouring20C560 is excluded. The
producer wrapper and reducer reject the partial fragment for semantic use.
First reducer run also refused a hand-transcribed immediate before result
creation. The repair encodes the specified 64-bit mask little-endian directly
and pins complete original bodies. Its failed receipt and driver preimage stay
immutable. No guard was weakened. The case-insensitive-prefix hypothesis was
rejected by original static import identity before the valid result.

Control copies are losslessly deduplicated: each case's receipt maps unchanged
inputs to the frozen baseline and records their exact hashes. The changed input,
actual stdout/stderr and CLI receipt are retained for each case. Reconstruct in
a fresh directory with the provided control driver; do not run into or modify
published inputs/results. All own finite helpers ended; no PC/game/save/config/
reference or peer process changed. Full L1+L2 goal remains ACTIVE/NOT_MET.

Next discriminator: close which keys the actual insertion functions can place
in the map, then intersect the qualified source domain with the six missing
indexed candidates. Do not assume all insertion sites use one raw-path domain.
The unprefixed six candidates do not automatically exercise the three prefix
examples. Use retained insertion code first; live observation is last if a
natural source/lifetime premise remains.
