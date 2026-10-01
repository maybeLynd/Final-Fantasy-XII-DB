# Affected-consumer check — NS-4, the namespace byte-order mark (FABLE, Claude Opus 5.5, 2026-09-26)

The claim corrected is "the loader never reads the namespace's byte-order mark" (contract §14 `NS-4`, the evidence row
"a byte-order mark nothing reads", the line-86 box "the loader acts on the header's, not on this one", and the register
row).

The bytes show a reader. The header reader's only caller, `0059E070`, tests the namespace's first dword against
`0x01020304` after the fixup (`0059E167`). A mismatch returns 6 (`0059E295`), and the same body then checks the
self-size identity (`0059E191`).

This is a propagation failure, not a new finding. The namespace page has recorded the check since `b3d6f43df`
(2026-09-14, FABLE), and FABLE's 2026-09-22 `+0x18` section cites the same site. The contract item and the register
row were never updated.

**Regression, run by FABLE 2026-09-26:** `_index/candidates/ns4-bom-reader/bom_reader.py`, FAILS 0.
- The known positive: the header marker's two compares, `0059A3FF` and `0059A419`, as the cluster-header contract lists
  them.
- B1: the only `.text` compare against `0x01020304` is `0059E167` in `0059E070`, with no off-boundary hits.
- B2: `rdi` is the namespace buffer's data pointer.
- B3: the mismatch branch sets 6, and the self-size compare sits at `0059E191`.

| consumer | state |
|---|---|
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md` §14 item 4 `NS-4` | revised-here (struck; answered with the sites) |
| same contract, evidence row "why the namespace carries a byte-order mark nothing reads" | revised-here (label restated as "the load path reads the namespace byte-order mark and refuses a mismatch", PROVEN) |
| same contract, §3 box "the loader acts on the header's, not on this one" | revised-here (fixup vs check distinguished) |
| same contract, §15a "`NS-4` stay[s] open" | history: a dated 2026-09-12 falsification pass, left as written |
| `Reconstruction/Tests/Differential/diff_phyre_namespace.py` `CONTRACT_MAP` entry | revised-here (identical label; NOT EXERCISED, because the check lives outside the swap routine the harness drives) |
| `_index/PARITY-STATUS.md` (generated) | not hand-edited; follows the harness on its next `parity_status.py` run |
| `_index/OPEN-QUESTIONS.md` NS-4 row | revised-here (ANSWERED) |
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md` `+0x1C` note (2026-09-14) and `+0x18` section (2026-09-22) | agrees (the source of the evidence) |
