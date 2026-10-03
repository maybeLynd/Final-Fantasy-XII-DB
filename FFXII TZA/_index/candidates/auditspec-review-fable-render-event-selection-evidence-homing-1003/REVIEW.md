# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-render-event-selection-evidence-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-RENDER-EVENT-SELECTION-EVIDENCE-HOMING` · Package: `_index/candidates/fable-render-event-selection-evidence-homing-1003/` · Page: `17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md` (commit b7c6eb07d; reviewed at HEAD 431017e52, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 5 rows, fewer than 15, so all 5 were read clause by clause against the full listings. All 24 anchors are correct. Every row holds as written, including FABLE's correction to `003E0740`.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 5 functions, 24 anchors`, `ALREADY` and `FAILS 0`, exit 0. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 5 rows, 24 anchors, `mode: homing`; rejected 0, skipped 0, missing 0, corrections 1 (`003E0740`).
- Notation: "`F`+0xNN" names the call at that offset of the row's own function. Each one was resolved to its call site and callee.
- Semantic pass: **every row** read clause by clause against `disw.py` / `disr.py` output of the certified image (SHA256 73461D08...):
  - `003B4DA0` correct. `movzx` word `02B4050C`, `cmp ax, -1` / `je`. `movsx` * 0x740 + `[022C6F28]`. `cmp [+0x284], 0` / `cmove rcx, 0` (`003B4DC7`), `test rcx`, then `003E6AA0(rec, 2)` (`003B4DD9`). The stores run unconditionally after each slot: dword `02B4050C` = -1 (`003B4DE5`), word `02B40508` = 0, byte `02B4050A` = 0. The same pattern follows for `02B40514` (`003B4E28`), then `02B40514` = -1 (`003B4E2D`), `02B40510`, `02B40512`.
  - `003B5180` correct.
    - First selection at `[rsp+0x20]`: word 0, dword `+4` = -1. `cmp byte 02B4050A, 1` / `cmove` qword `02B40508`. Then byte `02B40512` == 1 and `cmp byte [rsp+0x21], byte 02B40511` / `cmovb` qword `02B40510` (`003B51C8`, unsigned, byte 1 of the current choice).
    - `+0x57` = `002EA030(0)` (`003B51D7`), `cmp eax, ebx` (`ebx` = the incoming `ecx`). Equal -> the `02B4050C` slot as in `003B4DA0` (`003B5213`), resetting `02B4050C` = -1, `02B40508` = 0, `02B4050A` = 0. These resets run only inside the equal branch, as the row says.
    - `+0xb5` = `002EA030(1)` does the same for `02B40514` / `02B40510` / `02B40512`. On that reset path `cl`/`dl` are zeroed. Otherwise they are re-read from `02B40511`/`02B40512`, so the rebuild at `[rsp+0x28]` uses the current values.
    - `+0x172` = `003B4FD0` (`003B52F2`) runs when `[rsp+0x24] != [rsp+0x2C]` (`003B52E1`) or byte `[rsp+0x20] != [rsp+0x28]`.
  - `003E0740` correct, and FABLE's correction holds. `rdx = [022C6F28]`, `edi` = dword `[rdx+0x48800]`, `cmp edi, -1` / `je` -> return (`003E0753`). Per index:
    - The guards are `cmp di, -1` (low word), `add rcx, rdx` / `je` (null record), and `cmp [+0x284], 0` / `je` (`003E077F`).
    - `003E6DA0(rec)` (`003E078C`), with null `r` -> next.
    - For each of `r+8`, `+0x28`, `+0x34`, `+0x3C`, `+0x24` the body calls `0020E600(id)`, tests it, then calls `0020E600(id)` again and passes **that** result. This is the corrected clause: `003E07AD`, `003E07CA`, `003E07E7`, `003E0804`, `003E0821`.
    - The targets are `+0x75` = `005154B0` (`003E07B5`), `+0x92` = `00518E60`, `+0xaf` = `004719F0`, `+0xcc` = `00472820` and `+0xe9` = `005175F0`.
    - Next index = `movsx` word `[base + idx*0x740 + 4]` (`003E083E`), looping while it is not -1.
  - `00423980` correct. `edi = [rcx+0xC4]`, `cmp -1` / `je`, `0051BA40([0020E600([rcx+0x10])+0xDA8], edi)` (`004239A9`). `[rcx+0xC4]` = -1 (`004239B1`). `edi = [rcx+0x18]`, `cmp -1` / `je`, `002ED570([0020E600(dword +0x10)+0xD98], edi)` (`004239D6`). Non-null result: `comiss [+0x98], 1.0` / `jb` skip (`004239E8`, `01CEBBA8`). Otherwise `and [rax], ~8` (`004239F1`) and `[+0x98] = 0`.
  - `0046E8D0` correct. `rax = rdx` first (`0046E8D6`). `cmp [rcx+0x10], -1` / `je` -> `ret` with that `rax`. Otherwise `002ED570(rdx, dword)` (`0046E8E7`), then `jmp 00372F60` with (`rcx`, result) (`0046E8F7`, a tail jump).
- README count sentences checked against `rows.json`: "named 5 F-frontier functions", "5 staged with 24 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match. The one **FABLE corrections** bullet matches `rows.json` `corrections`, and the row's current text is its `now` value.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): none of the 5 belongs to an accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- `00423980`: "its float `+0x98` is not below 1.0" is `comiss` / `jb`. An unordered (NaN) value also skips the clear, although NaN is not "below" 1.0 in the IEEE sense. Ordinary reading ("at least 1.0") matches the bytes. Adding "(an unordered value skips it)" would make the row exact for NaN.
