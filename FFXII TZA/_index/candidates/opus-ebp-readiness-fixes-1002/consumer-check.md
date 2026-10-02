# Consumer check: 25-EBP contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-25-VALUES-1002. Cloud wave 4 mapped `25-EBP-Script-Container/` from a text snapshot
(session `session_01KboLsRxwSDCcdGdhuXddFR`; report `cloud-reports/re-readiness/25-ebp.md` in
maybeLynd/Final-Fantasy-XII-DB, ce22721b; rated NOT YET). Its 16 value items and 18 count items were page-text only. A
local read-only pass decided them at the shipping image and in the shipped `.ebp` data, and OPUS re-checked the
deciding instructions (`ebp_check.py`).

What the bytes and the data show:
- The section count is the whole dword (`00264D74`/`00264D7D`). The two readings differ in 213 of 828 `us` sections.
- The pool table's second dword is the script offset (`00358A0F`).
- `0032ED70` sets pending bit 0 (`or qword [022C6E48+mgr*8], 1`). It is not a teardown, which is `0032ED80`.
- Bit 0x400 is cleared at `00331715`.
- Both resolvers write `0xFFFF` to `+0x18`/`+0x1A`.
- The kind-1 arm of `0032F3D0` returns 0 (`005C5230`), so the index write-backs never run.
- The weather roll also weighs the current slot's byte (`0025ACA0`), so the dated BW-4 correction is only partly right.

The pass drafted 110 strike edits (`apply_25ebp.py`). OPUS applies the 108 on its own lines across 15 pages
(`apply_by_owner.py OPUS`). One line goes to SWE2-EC7 and one to SWE2-DATA; SWE2-DATA is also asked to regenerate a
stale census TSV.

- **Affected:** 25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md, 25-EBP-Script-Container/Container/ebp2-container.md, 25-EBP-Script-Container/README.md, 25-EBP-Script-Container/Sections/section-002-text.md, 25-EBP-Script-Container/Sections/section-003-text.md, 25-EBP-Script-Container/Sections/section-004.md, 25-EBP-Script-Container/Sections/section-006.md, 25-EBP-Script-Container/Sections/section-008.md, 25-EBP-Script-Container/Sections/section-009.md, 25-EBP-Script-Container/Sections/section-010.md, 25-EBP-Script-Container/Sections/section-011.md, 25-EBP-Script-Container/Sections/section-012.md, 25-EBP-Script-Container/Sections/section-014.md, 25-EBP-Script-Container/Sections/section-016.md, 25-EBP-Script-Container/Sections/section-019.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the fifteen OPUS-led 25 pages (OPUS lines) | revised-here |
  | EC7's line 683 on the section-000 page (990a4fbde) | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 1 edit) |
  | DATA's line 497 on the section-000 page, and the stale request-channel census TSV | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 1 edit; regenerate with `gen_req_channel_census.py`) |
  | RE repo `docs/readiness/25-ebp.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-ebp-readiness-fixes-1002/ebp_check.py, verified at 3159f78f1: 15 instructions decode as cited, FAILS 0 ([`ebp_check.out`](ebp_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (108), FAILS 0.
