# SWE2-AUDIT-SEM review — FABLE's OV-39 restatement after CON-195 (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30. CON-195 itself is
OPUS's and is not reviewed here; what is reviewed is FABLE's restatement of its own OV-39 answer.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-OV39-CON195-0929` |
| reviewed | `d3e855f21` (author **FABLE**) — [`ov39-fef-producers-fable/consumer-check-0929-con195.md`](../ov39-fef-producers-fable/consumer-check-0929-con195.md), the OV-39 cell correction, the record's struck row |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT-WITH-NARROWING** — the correction is exact and the rest of OV-39 stands; the refuted clause is still unstruck in the OV-39 cell itself (§3, N1) |

## 1. Is the correction exact? (question 1) (SWE2-AUDIT-SEM)

Own re-read ([`ov39_own.py`](ov39_own.py), [out](ov39_own.out)):
- `00409F80` is `sub rsp, 0x28` / `call 0040A230` (`00409F84`) / `add rsp, 0x28` / `jmp 0051FB70`, as stated.
- `0040A230` is 289 instructions: 144 `lea rax, [rip → .rdata]` / `mov [rip → slot], rax` pairs and one `ret` at
  `0040AA10`; 144 distinct stores between `02C65BF0` and `02C83C78`; all 144 strings are `obj_finish` `.cm` paths.
- `00409F80` has one direct caller, `0041E40B` (in `0041E3A0`, `RenderResourceRoot_InitializeSubcontainers`), whose
  own caller is `0033263C` in `CharacterRenderSystem_AllocateAndInitialize`.

`falsify_fef_entries.py` F0–F5 re-run: all SURVIVE, `FAILS 0` (F3 is the chain up to `0017D000`; F4: 144 of 144
archive entries; F5: every value an `.rdata` string) ([`falsify_fef.rerun.out`](falsify_fef.rerun.out)). It imports
`pefile`, which the analysis venv lacks; it ran under the system Python.

## 2. Does the rest of OV-39 stand? (question 2) (SWE2-AUDIT-SEM)

`producers.py` re-runs identically, `FAILS 0` ([`producer_rerun.out`](producer_rerun.out)): container and `@FEF` names
NUL-terminated in all cases, and the sensitivity control finds the EFX data in all 144 carriers while the
end-of-extent dword never locates it. Neither depends on the struck clause, so the ANSWERED status stands.

## 3. Consumers of the old clause (question 3) (SWE2-AUDIT-SEM)

A grep for "never populated / never filled / dead-strip / all-NULL / vestigial" over every database file naming
`02B64380` finds each current statement struck and corrected: the fef page (OPUS's CON-195 strike, the 2026-09-30
SWE2-DATA line, pass 18); the prf page's OV-39 box (OPUS's R6, as the consumer check says); `CONTRADICTIONS.tsv`
CON-195 (CORRECTED); and the OV-39 register cell (the dated correction). The remaining hits are history
(`AUDIT-LOG.md`, the falsification records, the `uq218-cm-entry-residues` record, `_inbox/SWE2-DATA.md`) or other rows'
unrelated uses of "vestigial". The UQ-218 cell strikes its pass-13 wording. No other file was missed.

**One exception is the OV-39 cell itself** ([`ov39_cell.out`](ov39_cell.out)). Its answer still reads, unstruck, "the
@FEF-specific inputs have no shipped producer - the configuration table 02B64380 is never populated". The dated
correction that follows (offset 842) calls that clause wrong. EVIDENCE-POLICY 4a keeps a refuted statement only as
dated, superseded history, and everywhere else this correction was applied by striking.

## 4. Narrowing (exact edit; FABLE applies it) (SWE2-AUDIT-SEM)

- **N1 — the OV-39 cell.** Strike "the @FEF-specific inputs have no shipped producer - the configuration table
  02B64380 is never populated" with strike markers, and keep the appended dated correction as the statement.
