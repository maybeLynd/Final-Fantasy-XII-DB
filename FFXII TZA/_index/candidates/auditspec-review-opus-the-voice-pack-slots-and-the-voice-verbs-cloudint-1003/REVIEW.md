# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-voice-pack-slots-and-the-voice-verbs-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VOICE-PACK-SLOTS-AND-THE-VOICE-VE-AEC7F` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-the-voice-pack-slots-and-the-voice-verbs-cloudint-1003/` · Page: `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 5 functions, 23 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 5 rows, 23 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 5 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 5, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `0034E8B0` / `0034EE40`: the pop order is `a` (`ebp`) then `b` (`ebx`), and `003EA0D0` receives `ecx` = `s`, `edx` = `b`, `r8d` = `a`, matching `(s, b, a)`. `00267310` gets the zero-extended byte `[rdx+0x15]` (`rdi` = the incoming `rdx`). `jne` on non-zero skips the rest; `je` on a zero `003EA0D0` result skips `00314D40(1)`. `0034EE40` first calls `00267F90(r9, 0)`. Exact.
  - `003522C0` / `00353080`: `a` = `[r8]` and `b` = `[r8+4]` are loaded before any call. The guards are `je` (`00264170` == 0), `cmp eax, 1; je` and `js` on `a`. The clamp is `inc`, then lower bound 1 (`jge`/`jl`) and `cmovg` to 3. `00353080` uses `edi` = 1 as both the comparand and the low default, after its leading `00314D40(1)`. Exact.
  - `00352DB0`: exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
