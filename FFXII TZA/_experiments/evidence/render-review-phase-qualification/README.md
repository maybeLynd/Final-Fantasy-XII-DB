# Returned render reviews: phase, width and helper-object qualification

Method A, STATIC_ONLY. This additive packet checks the narrower contracts returned
by independent review. Original published packets and their results remain
immutable. No recapture, original-code execution, game session or setup.

For the player: creating a model joins it to a list before publishing its slot
ID, then marks/counts it. A reset writes four individual floats per group.
Removing a model can also change linked helper objects and notify the pool after
cleanup. These are reconstruction details, not observed gameplay faults.

## Accepted parents and returned evidence

| Parent | Producer commit | Independent review |
|---|---|---|
| render-slot-identity-publication | aac0489acecac507503bfc3ed28f063b37e631b2 | SPEC ACCEPT fd96f1634; FABLE ACCEPT-WITH-NARROWING f1a265c5b |
| render-clear-callee-footprints | 621dbd2cc584f14de1d993f844d0a0122ca9a56d | SPEC ACCEPT fd96f1634; FABLE ACCEPT-WITH-NARROWING b3fb2d6cf |
| render-removal-phase-contracts | 31f29775afd989f8678d0e364cd0066de63cda52 | SPEC ACCEPT fd96f1634; FABLE ACCEPT-WITH-NARROWING b3fb2d6cf |

`parent-identities.json` binds retained source, invocation/status, driver/result
and manifests to exact published blobs. `review-identities.json` binds six
retained review records to committed blobs. Checkout differences are CRLF only;
the packet preserves exact committed review bytes and checkout hashes. The
original setup's overstrict checkout check refused before semantic output;
`retention-recovery-01.json` records the cause and unfinished-suffix recovery.
No accepted board ADD/claim was replayed. Original byte/receipt checks stay exact.

Review executions are the reviewers' corroboration, not additional ASTRA tests.
FABLE review commits contain review files; they do not certify canonical page
incorporation. The existing OPUS consumption requests remain the consumer lane.

## Required additive contracts

1. On the empty pending-list arm, 427A21 writes the pool head48810. On the
   nonempty arm,427A37 writes the previous tail's WORD4 and427A43 writes the new
   row's WORD2. Both arms write pending tail48814 at427A47 before WORD ID0 at
   427A4D. The ID precedes metadata/active publication and count increment; it
   is not the first list publication. Reset calls include sentinel/default
   writes, so returned rows are not described as all-zero.
2. 6C0520 makes **four4-byte MOVSS stores per call,16 bytes total per call**.
   The two calls target210..220 and220..230. The original normalized footprints
   were correct; the old README/board phrase could imply16 bytes per store.
3. The mark arm of429140 conditionally writes returned helper objects:
   4291A9 AND~2 DWORD[result422D50+0C] if non-NULL;4291E4 AND~4 DWORD[result2ED570]
   on the reached non-NULL binding branch;4291F3 stores20E620 EAX at DWORD[result
   2ED570+A0]. The original full nonstack-write list included these sites, while
   its prose summary omitted them. Marking is not described as row-only.
4. After4200A0 returns,427DB3 ORs20h into DWORD[pool+48818], before the cached-next
   comparison/continuation. This is an explicit caller write, separate from
   opaque cleanup internals.
5. Pending48810/48814 and active48800/48804 endpoints share the same DWORDcount
   4880C and DWORDcursor48808 at the pool root loaded from022C6F28. They do not
   have independent counts. A source global is not an observed runtime pointer.

## Producer path and controls

`prove.py` first requires successful, driver-bound parent invocations/results,
selected manifest-member identities, exact source aliases and returned-review
identities. It re-decodes all retained source through the reviewed shared
access-role adapter, compares shipping bytes to EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8 and checks complete
local CFGs. Its actual `derive()` then checks the exact operations, full-width
roles, branch partitions, carrier/order and shared-root/field contracts before
writing `result-01.json`.

Producer01 terminal0, driver7346d436e99072e9079ee449a7615a693aba1218793c1bcf00adb7abb332eed4.
Control01 terminal0, driver09a4d3950623f11f132a3f1f30bc8f2d309ff34a21b7ddaa541562d57d4e1b21.
Three actual disposable CLI refusals: failed parent producer, missing parent
result, missing returned review. Five **synthetic derive-record controls** use
the exact function called by the positive producer: wrong pending-tail phase,
scalar width16, helper-object width8, omitted poolflag mask and changed pool
root. These are not patched-image or machine-code executions. No old census,
settled scan campaign or reviewer controls were repeated.

Reproduce with the existing analysis venv: `python -B prove.py fresh-result.json`.
For refusals, restore `controls-01/*/input-identities.json` overlays and explicit
removals. Inspect raw status/stdout/stderr and precise diagnostics.

## Consumers, bounds and cleanup

OPUS: incorporate these qualifications through the existing READY slot/clear/
removal requests; cite both original packet and this additive supplement. Do not
promote success to lifetime release or assume two independent counts.
FABLE: canonical dual-list lifecycle/clear prose consumption is still required;
the completed reviews alone did not modify those pages. Route only that missing
consumer work once, preserving current page ownership.
SPEC: independently verify this supplemental producer/controls and narrowed
summary. Original independent acceptance remains valid at its stated scope.

Normal-return source phases require valid pool/rows/list indices, private frames,
nativeABI/normalreturns, reached valid helper pointers, no alias/interference.
No native helper effects, natural reachability, runtime pointers, atomicity,
scheduling, allwriter coherence, ownership/reuse or lifetime are established.
No game/PC/instrument/save/config/reference/peer changes; owned bounded processes
are terminal. Four historical accepted runtime-needs eliminations unchanged;
zero wholeOV rows closed. Full L1+L2 goal remains ACTIVE/NOT_MET; K14 closed,
EXP127 invalid, menu allowance spent/extension unapproved.
