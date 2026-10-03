# Namespace copier: successful bound and missing-entry exception

For the player: the game constructs an area's effect-file name using a small name-copy routine. Reading the shipping code tells us exactly how much that routine can write. It does not tell us which missing-name area is visited during a real play session.

**Producer result: Method A, STATIC_ONLY; independent review pending.** No game or original machine-code execution was needed. The input is the existing SPEC-accepted full `002DF880..002DF8D9` capture, not a new capture or repeated field census.

With a valid non-null namespace name, `R9D` is sign-extended as a signed character limit. The routine copies its first byte before testing the limit. It can copy at most `max(1, signed32(R9D))` bytes and then writes one extra NUL. Thus limit zero or negative still writes a copied byte and a NUL: it is not a no-write or zero-capacity request. Its return is zero, not the number of characters copied.

For the effect loader's literal limit `259`, a successful lookup writes only destination offsets `0..259` and establishes a NUL by offset `259`, given valid accesses and normal ABI/noninterference. This requires **260 writable bytes**. A resolved null name slot instead returns `−1` without touching the destination. The loader ignores that return, so the successful-lookup bound does **not** establish a NUL or a bounded inherited string on SD194's missing-name branch.

The termination comparison reads the **next** source byte after each copied byte. A NUL at source offset zero does not itself stop this copier; if offset one is nonzero it can continue copying bytes after the leading NUL. Under a disjoint/noninterfering source, the count is the smaller of `max(1, C)` and the first NUL offset at least one. The later effect-loader scan will still see a leading NUL when the first copied byte was zero. This distinction does not imply a visible game effect or a fault.

The counter invariant covers the whole signed-32 limit domain by two induction cases, `C≤1` and `2≤C≤INT_MAX`. Every back edge requires the incremented count to remain strictly below `C`; no counter wrap occurs. This is a source proof, not proof by samples. Fifty-four boundary calculations are producer sanity controls. Three actual reducer CLI controls reject a failed capture, a truncated source, and coherent altered `JGE` bytes. They are prerequisite controls, not FF12 experiments. The current proof and controller require checked upstream exit/exception/terminal status, exact source bytes and the reviewed access-role adapter in the actual qualification path.

Exact reference: EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image base `0x120000`; 89-byte copier SHA256 `f71f6f4a0633fa327a47b23f16231e23be086270b133f30357e49520d74f9800`. All 29 operations are pinned. The function contains no opaque calls; both returns and the copy-loop CFG are closed. Retained caller `00377E03/00377E09` supplies `259` and calls this function.

Limits: namespace/index and every selected source/destination access must be valid; the routine validates neither pointers nor capacity. Code and private state must remain intact under normal ABI. The write-count bound survives sequential source/destination overlap; the unchanged-source next-NUL formula requires disjoint/noninterfering spans. Actual absent-entry stack contents, field reachability, resource request acceptance, allocator/lifetime, imported `memcpy` behavior and presentation remain OPEN.

DATA/OPUS should attach the successful-lookup bound and null-slot exception to SD194 and the copier contract after independent acceptance. This package closes a local initialization prerequisite without closing SD194's natural-state question. Do not repeat the settled name-builder partitions or launch an unchanged menu attempt. The earlier frozen packet and review remain immutable.

Reproduce: `python -B prove.py <fresh-result>` from this packet with the repository interpreter and reviewed repository adapter. `run.py` records actual finite child status. `control.py <fresh-controls-dir> result-03.json proof-03.status.json` requires the retained successful producer and refuses incomplete input. Published results are never overwritten. The added publication source map and the wording correction are recorded separately from the original receipts; neither creates new scientific cases.

No game, PC control, save/config/reference, instrument, service or peer process was changed. All own children exited. The database goal remains ACTIVE/NOT_MET.
