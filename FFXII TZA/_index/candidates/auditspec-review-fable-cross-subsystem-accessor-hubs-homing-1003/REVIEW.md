# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-cross-subsystem-accessor-hubs-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CROSS-SUBSYSTEM-ACCESSOR-HUBS-HOMING-1` · Package: `_index/candidates/fable-cross-subsystem-accessor-hubs-homing-1003/` · Page: `00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md` (commit `eea05327e`, reviewed at HEAD `db98e3d59`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 28 functions, 134 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 968, and every sentence is on the page verbatim.
- **rows.json.** 28 rows, 134 anchors. Rejected 0, skipped 0, missing 0. 1 FABLE correction (`003FC3F0`, "increments while below" narrowed to a single guarded increment). The correction is right: `003FC449 jb` guards one `inc dx` / store at `003FC45E`, with no back edge.
- **Semantic pass.** All 28 rows were read clause by clause against `disr.py` output of the certified image, not just 15.
- **The message-handler rows.**
  - `002CA6C0`: the `sub` / `cmp` ladder maps 1, 2 and 4, and anything else tail-jumps `005C5230` at +0x32. Case 2 calls `002CA2E0` at +0x3A, then picks `and` or `or` on bit 0 by `[[+0x108]+0x168] & 0x10000`. Case 1 is `002432B0(rcx+0x50, [[0209AC30]+0x38], 6, rcx)`, the null-gated word copies, `[rdx+8]` to `+0xD4`, `[rdx+0x10]` to `+0x108`, and the conditional clear.
  - `002CB150`: argument 8 and the `[[+0x60]]` / `[[+0x60]+8]` bit-0 clears.
  - `002D5E00`: `[[0209AC30]+0x18]`, argument 1, OR `0x8000000` into `[[[rcx+0x60]]+0x20]` before the word copies, then `002735E0(5)` passed as `rdx` to `00247570`.
  - `003FC3F0`: case 15 at `cmp ecx, 0xD`. In case 2, `imul` by `0x3C`, then `movsx` and the unsigned `jb`. Case 1: `0035D3F0` at +0x8C, `002432B0(..., 2, rcx)`, `0028F810` at +0xB1 with `+0xC - word +0xA`, then `00247570(rcx, 00D11FF0)` / `00247930(rcx, 0x58)`.
  - `0057FA30`: `00393190(rcx, 0)`, then clear `+0xD8`, set `+0xB0`, set the seven byte-indexed entries from `00D23EAC` (`jb` on 7), clear `+0xD0`. The `sub`/`cmp` ladder maps 3/4/5 to `0x874`/`0x873`/`0x872`, and the default stores the address `01CEB638` itself.
  - `003C9840`: `2` or `1` by `003C5FB0`'s result, and the word `+0xC`/`+0xE` copies after re-reading `+0xC8`.
  - All exact.
- **The `002E97B0` rows.**
  - `002637D0`: the incoming `edx` on null, `-1` or a clear bit 0, else `(byte +0x29 >> 1) & 1`.
  - `00269F60`: the tail `jmp 003EC200` with word `+0`, and the unchanged `rax` otherwise.
  - `0050E3A0`: the tail `jmp 0017D280` with `00D22A18` on null, else `bts eax, 0xC` / `jmp 002EB330` with the incoming `rdx` as `rcx`.
  - All exact.
- **The VM-verb rows.** Each was checked for pop order against the argument registers.
  - `00347580`, `00347AB0` and `00347FF0`: the float in `xmm1` comes from the `rdx` (`rsp+0x20`), `r8` (`rsp+0x20`) and `r9` (`rsp+0x20`) slots respectively, as each sentence says.
  - `00347600` and `00347BE0`: third pop to `00264010`, `edx` = second, `r8d` = first.
  - `00348800`, `0034B060` and `0034C1D0`: the three-deep chain into `004736E0`/`00473710`/`00473770`.
  - `00349490`: `00263CC0`, then `xmm1`.
  - `0034AAD0`, `0034DA30` and `0034E190`: `edx` = the pop.
  - `0034C500` and `0034CC60`: `002640C0` at +0x17, `00358940(result, pop)`, `00263F10`, then `003597B0`/`003597D0`.
  - `0034C6A0`: `cmovs` clamps the first pop to 0.
  - `00351EE0`: qword store to `[r8]`, then tail.
  - `00352270`: `cmp byte [rbx+0x15], 3` / `jne` picks `36E880` at +0x3B, else `36E7E0` at +0x4A.
  - `00352940`: tail at +0x35.
  - All exact.
- **`00240A60`.** `[[rdx+0x10]]` and `[[rdx+0x10]+8]`, `movsxd r9d` into the `00914C60` table at stride 8, `002F9860` / `0020E620(0)` stores at `+0x18` / `+0x20`, and return 1. Exact.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
