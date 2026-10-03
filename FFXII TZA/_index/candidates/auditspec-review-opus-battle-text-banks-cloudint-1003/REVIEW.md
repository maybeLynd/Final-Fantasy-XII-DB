# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-battle-text-banks-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-BATTLE-TEXT-BANKS-CLOUDINT-1003-5F8BD` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-battle-text-banks-cloudint-1003/` · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 2 functions, 7 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 2 rows, 7 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 2 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 2, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `00197A40`: `movsx eax, byte [rcx+0x3a]; bt eax, edx; setb al`. A register `bt` takes the bit offset mod 32, and bits 8..31 of the sign-extended byte equal bit 7. Exact. The result is in `al` only: the upper bits of `eax` keep the sign-extended byte. A raw rel32 sweep finds one caller (`001E0F12`, in `001E0F00`), and it does `movzx eax, al`, so "returns 1 / 0" holds as a bool return.
  - `002902D0`: `r9d` = 0x40, `r8d` = `lea [r9-0x3f]` = 1, `[rsp+0x20]` = 0x28 (fifth), `[rsp+0x28]` = 0x30 (sixth), and `rcx`/`rdx` passed through. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
