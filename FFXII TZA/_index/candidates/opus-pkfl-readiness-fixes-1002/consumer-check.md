# Consumer check: 26-PKFL contradictions from a cloud reconstruction-readiness map, settled at the bytes and in the shipped packages, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-26-VALUES-1002. A cloud session mapped `26-PKFL-Package-Container/` from a text snapshot
(report `cloud-reports/re-readiness/26-pkfl.md` in maybeLynd/Final-Fantasy-XII-DB). Its 15 value items were page-text
only. A local read-only pass decided them at the shipping image, re-parsing all 10,314 shipped packages under the
{offset, size} reading. OPUS re-checked a sample (`pkfl_check.py`).

Settled:
- **Each slot is an {offset, size} pair.** The second dword is the slot's size (`0032F360+0x2E` reads `+0xC` beside
  the offset at `+8`).
- **Payload placement.** In all 10,287 non-empty packages the offsets ascend in slot order. The first payload sits at
  0x800, and each later payload starts at the next 0x800 boundary.
- **Directory size.** The directory ends at 0x88 / 0x208. The "smallest offset 0x40" was an artefact of the withdrawn
  four-byte reading.
- **Byte 0 is load-bearing.** Every slot reader starts with `0032F260+0x13` `cmp byte ptr [rcx], 0`.
- **Four completions.** Each clears its own bit: 13 `.mot`, 12 `.snd`, 15 `.vpc`, 14 `.vpcjp` (`+0x20` in each of
  `003302B0`, `00331760`, `00331820`, `003317C0`).
- **The loader's arguments.** `0032E620` takes five arguments, and the file offset travels as the record's first dword.
- **The README counts are four-byte figures.** The pair reading gives 4,761 / 0-15 / 4,212 / 558.

The pass drafted 36 strike edits (`apply_26pkfl.py`). All are OPUS's, on two OPUS-led pages. Every edited line was
last written by an unprefixed commit, and there are no carriers or holds.

**Generator corrected here.** The frozen `Tools/work/formats/pkfl-container-census.tsv` matched the withdrawn
four-byte reading on all 10,314 rows, and the pair reading only on the 27 empty packages. Its generator,
`Tools/analysis-kit/gfz-scripts/census_pkfl_container.py`, is a shared script, so OPUS corrected it in this publish:
- `read_dir` reads `slotCount` {offset, size} pairs (8 + 8 * slotCount bytes).
- `slots` reports stored sizes.
- The aliasing text is kept as withdrawn history.
- The self-test now builds a pair directory and refuses a short one.

Re-run over the installed VBF, it reproduces the read-only pass's own parse: 10,314 packages, slot counts 16 (6,696)
and 64 (3,618), 40,203 present pairs, slots 0-15 used. The TSV is unpublished scratch, ignored by git. The page prose
states the pair reading.

- **Affected:** 26-PKFL-Package-Container/Container/pkfl-package-container.md, 26-PKFL-Package-Container/README.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the two OPUS-led 26 pages | revised-here |
  | `census_pkfl_container.py` and its unpublished TSV | revised-here (pair reading; regenerated) |
  | RE repo `docs/readiness/26-pkfl.md` | routed-to-OPUS (filed after this publish, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-pkfl-readiness-fixes-1002/pkfl_check.py, verified at 73a856c52: 6 instructions decode as cited, FAILS 0 ([`pkfl_check.out`](pkfl_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (36), FAILS 0.

**Pass-22 neighbours (2026-10-02, OPUS).** `check_publish_neighbours.py` refused the first form of these edits. Some corrections cited another layer's function by address, and that adds an unaccounted crossing. Those functions are now named by role or by their ledger name on the page, with the offset kept. The applier's `ROLE_NAMES` pass makes the same change to its NEW text, so re-runs stay idempotent. The full deciding addresses remain in the applier's comments and in this record. `Tools/work/OPUS/nb_page.py` shows no new hit.
