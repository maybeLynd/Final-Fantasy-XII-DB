# Returned status-watch specification qualification

Incoming OPUS-REQ-ASTRA-STATUS-SPARSE-SLOT-QUALIFIED-WATCH P3, no L2 cell waits. Read current _index/candidates/status-sparse-slot-watch-preparation.md and existing accepted status-watch-preflight. Corrected row/census/coverage and bounded no-hit interpretation remain accepted, no repeat archive export/census.

Exact questions before expensive C: does RIP mean original accessed instruction or raw post-access trap context; do four RW windows classify only sparse reads; does allFF Doom imply no legitimate read? Competing explanations: intended normalized access-PC with correct positive recognition versus raw-PC comparison that misses it; sparse read versus write/known+13-only overlap; detector defect versus legitimate empty-row read.

Method A sufficient for these criteria: original known read aligned from containing PE RuntimeFunction31C5D0, selected prefix to31E250; MOVZX at31E241 is4B with successor31E245. Intel SDM253669-060US17.3.1.2 (PDF page120) documents data breakpoints after the accessed instruction; Microsoft ba docs distinguish RW from read-only. No assertion that a future normalized source-RIP241 is wrong: require explicit raw-context/source-PC separation and positive native qualification. No current read detector is qualified by these docs.

Watch union+11..+1F includes+13. A different source reading only+13 is not a sparse-slot reader; RW write is not read. AllFF contents alone cannot imply no access; a Doom hit needs opcode/EA/kind/row diagnosis, not automatic invalidity. Access width is opcode-derived, not breakpoint-window width. Sampled after-access memory is not automatically consumed value.

Budget original selected aligned prefix, existing resource/preflight pins, returned preparation and two primary documentation references. Return exact criteria/prerequisites to OPUS; no generic debugger build or new C/native/disposable/guest execution. Original14-byte meaning remains unknown; ordinary action/save/removal and bounded health/cleanup/detector controls required for future live cycle. Extra input setup allowance remains exhausted/pending; not retried. PC OFF, goal NOT_MET.
