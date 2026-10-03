# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-member-registration-and-the-recovered-fi-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-MEMBER-REGISTRATION-AND-THE-RECOVERED` · Package: `_index/candidates/fable-member-registration-and-the-recovered-fi-homing-1003/` · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md` (commit b35f1958c; reviewed at HEAD 89538d085, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

This is an interior package: it ships `interior_applier.py` and no `homing_applier.py`. Only the sentences were reviewed. It has 2 rows, fewer than 15, so I read both clause by clause against the full listings. For `006ABEC0` that included the bytes past its recorded extent. All 10 anchors are correct. Both rows hold, including FABLE's correction about what `006ABEC0` returns.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 2 functions, 10 anchors`, `ALREADY` and `FAILS 0`, exit 0. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 2 rows, 10 anchors, `mode: homing`; rejected 0, skipped 0, missing 0, corrections 1 (`006ABEC0`).
- Semantic pass: **every row** read clause by clause against `disw.py` / `disr.py` output of the certified image (SHA256 73461D08...). The bytes past `006ABEC0`'s extent were decoded raw with `scratch_l/rawdis.py`.
  - `0063BBC0` correct.
    - `rcx = [rcx+0x30]`, then `call [[rcx]+8]` (`0063BBCB`).
    - A non-null result with `test byte [rax+0xFC], 1` set returns `lea 02CF8580` (`0063BBDC`).
    - Otherwise it does `jmp 00630340` (`0063BBEC`). Nothing restores `rcx` after the virtual call, so the callee gets whatever `rcx` the call left.
  - `006ABEC0` correct.
    - `[rcx]` null -> 0.
    - Chain walk from `[rcx+8]` through `+0x78`, compared with `02E404B0` (`006ABEE1`). On a match the key is `[rcx]`.
    - Otherwise `005A7B50([rcx+8], 00D4A458 'getLocalToWorldMatrix')` (`006ABF00`). Then `+0x50` = `006ABF10` -> `006AB600(result, [rcx])`. Either null gives 0. The key is the second result, passed as `rcx` to `006ABF40`.
    - Tree search: the root is `[01F2EB58]` and the sentinel `01F2EB40`. `cmp [node+0x18], key`: above (unsigned) sets `eax` = 1 -> `shr 0x1f` = 0 -> child `[node+0]`; below sets `eax` = -1 -> 1 -> child `[node+8]`; equal stops (`jae`, `006ABF66`). Reaching the sentinel gives 0.
    - Return: `lea rax,[rdx+0x20]` / `cmove` (`006ABF84`). Then, past the extent, `test rax,rax` / `je` / `mov rax,[rax]` / `ret` (`006ABF88..90`), so it returns qword `[node+0x20]`, or `r8` = 0 when nothing matched. That is the corrected clause.
- README count sentences checked against `rows.json`: "named 2 F-frontier functions", "2 staged with 10 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match. The one **FABLE corrections** bullet matches `rows.json` `corrections`, and the row's current text is its `now` value.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): neither function belongs to an accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- `006ABEC0`'s recorded size is 0xC9 (`functions.tsv`). That cuts off its last 12 bytes (`006ABF89..006ABF94`: `test`/`je`/`mov rax,[rax]`/`ret`/`mov rax,r8`/`ret`). All five anchors fall inside the extent. An extent-bound reader, such as `body_bytes` windows, would miss the final dereference, as FABLE's correction notes.
