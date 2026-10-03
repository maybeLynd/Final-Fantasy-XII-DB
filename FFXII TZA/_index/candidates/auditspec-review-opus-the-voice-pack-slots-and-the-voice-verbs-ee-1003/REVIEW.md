# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-voice-pack-slots-and-the-voice-verbs-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-VOICE-PACK-SLOTS-AND-THE-VOICE-VE-D9EAA` · Package: `_index/candidates/opus-the-voice-pack-slots-and-the-voice-verbs-ee-1003/` · Page: `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md` (commit 6a9eb7555; reviewed at HEAD e60842fa0, package and page unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row, fewer than 15, so I read it clause by clause against the full listing. All 5 anchors are correct. Every clause holds, including the order in which the five values are pushed.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 1 functions, 5 anchors`, `ALREADY` and `FAILS 0`, exit 0.
- `rows.json`: 1 row, 5 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `00351020` correct.
    - Saved arguments: `r12 = rcx`, `r15 = rdx`, `r14 = r8`, `rbp = r9`.
    - Three `00267E10(rbp)` calls give `esi` (first), `edi` (second, `00351057`) and `ebx` (third).
    - Five `00267F90(rbp, edx)` calls push -1 (`0035106E`), `ebx` (the third value), `edi` (the second), `esi` (the first, `0035108C`) and 1 (`00351099`).
    - It restores `rcx`/`rdx`/`r8`/`r9` from `r12`/`r15`/`r14`/`rbp` and ends with `jmp 003581B0` (`003510C8`), a tail jump.
- README count sentences checked against `rows.json`: "named 1 F-frontier functions", "1 applied with 5 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): `00351020` is a member of `ScriptVM.VerbAdapter` (letter B), which `01-Script-VM-Native-Bridge/Verb-Dispatch/the-shape-of-the-verb-population.md` declares, not this page. It is not in scope here, so the base rule applies.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title says "cloud-drafted", while its first paragraph and `rows.json` `session` name `local-ee-drafter-r4` (a local agent, no cloud credit). It is a wording inconsistency only.
