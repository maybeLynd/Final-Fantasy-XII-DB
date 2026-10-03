# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-what-the-engine-calls-to-make-a-sound-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-WHAT-THE-ENGINE-CALLS-TO-MAKE-A-SOUND-C7466` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-what-the-engine-calls-to-make-a-sound-cloudint-1003/` · Page: `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 5 functions, 24 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 5 rows, 24 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 5 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 5, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `00212A90`, `00212AE0`, `00212B30`, `00212BD0`: the same sentinel-list walk (head `rcx+8`, first node `[rcx+8]`, next `[node]`, stop on return to `rcx+8`, empty list skipped by the first `cmp`/`je`). The object is `[node+0x10]` and the virtual slots are `+0x20`, `+0x18`, `+0x28` and `+0` (`call qword ptr [rax]`). `edx` is preserved in `esi` and re-passed each time. Exact.
  - `0035D030`: `0028E940(1)`, then a tail jump to `00249C60(4)`. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
