# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-a-line-of-text-becomes-glyph-quads-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-A-LINE-OF-TEXT-BECOMES-GLYPH` · Package: `_index/candidates/fable-home-how-a-line-of-text-becomes-glyph-quads-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `c6de67245`; the package and the page are unchanged since that commit and unmodified in the working tree) · Page: `99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`

## SWE2-AUDIT-SPEC verdict: REJECT

The sentence is exact, but the package's only row is mis-homed. `00408AD0` has nothing to do with glyph runs.

- Its "caller" is the 5-byte thunk `003EC850`. This page names that thunk once, inside a list of a dozen subsystem-reset calls that `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) makes. The list sits in section 7, "What is not known" (line 1013).
- The body edits the flag dword `+0xC8` of the `02B62D80` object. That object and its sibling writer are documented on `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`.

So 1 of 1 rows fails host fit, and nothing in the package stands on this page.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python, without `--apply`. It exited 0 and printed `VERIFY 1 functions, 4 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The committed `.out` is the pre-apply `DRY` run with the same counts. The heading is at page line 2059, and the row at line 2065 matches `rows.json` byte for byte.
- **rows.json.** 1 row, 4 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass, `00408AD0` (0x21 B):** `mov rax, [02B62D80]` / `test rax, rax` / `je ret`. Then `mov ecx, [rax+0xC8]` / `test cl, 2` / `jne ret`. Then `and ecx, 0xFFFFFFFB` / `mov [rax+0xC8], ecx`. The text is exact: it guards on bit 1 (`0x2`), clears bit 2, and writes nothing on either guard.
- **entered_from.** `003EC850` is `thunk_FUN_00408ad0`, a lone `jmp 00408AD0`, so "`003EC850` + 0x0" is a correct jump site. The raw byte scan finds these references to the thunk:
  - `00262B94 call` in `002628B0` + 0x2E4, the manager-slot unload;
  - `0026CA52 call` in `0026C8C0` + 0x192, `ActorManager_BindLoadedDefinitionPayload`;
  - `jmp` from `003E9010`, a second thunk, which `00351F10` in turn jumps to.
  No glyph-run function reaches it.
- **Host fit (the defect).**
  - This page's only mention of `003EC850` is the "~12-call subsystem reset" list inside the `0026C8C0` paragraph in section 7 (line 1013). That is a list entry inside an actor-manager paragraph, not a glyph-run statement.
  - The `02B62D80` object is not otherwise on this page.
  - Its sibling `00404D70` has the same guard and the same dword: it sets `0x8` on `[02B62D80]+0xC8` unless `0x2` is set (bytes: `test cl, 2` / `jne` / `or ecx, 8`). That sibling is documented on `the-world-tick-and-the-field-frame.md` line 687 ("the deferred-enable arm").
  - That page also cites both real callers: it has a section for the `002628B0` exclusive subtree, "the manager unload's 26 helpers" (line 529 on), and it cites `0026C8C0` at lines 179 and 959.
- **Advisory (tool).** The applier's caller test is a substring test on the page. That is how a single list mention of a thunk in a "not known" paragraph qualified this page as a host. After the apply, the row's own cell satisfies the test as well.

## SWE2-AUDIT-SPEC repair

1. Remove the section from `how-a-line-of-text-becomes-glyph-quads.md`: the heading at line 2059, its intro and the `00408AD0` row.
2. Re-home the row, text unchanged, to `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`, next to `00404D70` (line 687) or in the `002628B0` subtree section. The applier needs the caller cited on the host before the apply, so first cite the thunk in a body line there, for example: "`003EC850` is a 5-byte thunk to `00408AD0`; `002628B0` + 0x2E4 and `0026C8C0` + 0x192 call it". Then keep `entered_from` as "`003EC850` + 0x0".
3. Regenerate `homing_applier.out` and correct the README to name the new page.

Limits: static evidence only. A cloud draft plus FABLE's re-read is not independent review; this record is.
