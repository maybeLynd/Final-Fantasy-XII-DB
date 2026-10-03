# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-numeric-formatting-and-character-mapping-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-NUMERIC-FORMATTING-AND-CHARACTER-MAPPI` · Package: `_index/candidates/fable-numeric-formatting-and-character-mapping-homing-1003/` · Page: `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md` (commit b7c6eb07d; reviewed at HEAD 431017e52, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The package has 2 rows, fewer than 15, so both were read clause by clause against the full listings. All 10 anchors are correct. `00404E10` is correct as written. `003CA530` is correct in every callee, argument slot, store and branch. One arithmetic clause leaves out a signedness that changes the value: the frame difference is converted to float as an **unsigned** 32-bit number. A negative difference therefore becomes about 4.29e9, not a negative angle. The narrowing is wording only.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). It printed `VERIFY 2 functions, 10 anchors`, `ALREADY` and `FAILS 0`, exit 0. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 2 rows, 10 anchors, `mode: homing`; rejected 0, skipped 0, missing 0, corrections 0.
- Notation: "`F`+0xNN" names the call at that offset of the row's own function (the homing convention). Each one was resolved to its call site and callee.
- Semantic pass: **every row** read clause by clause against `disw.py` / `disr.py` output of the certified image (SHA256 73461D08...):
  - `003CA530` correct except for the signedness narrowed below.
    - The dispatch reads `ecx = [rdx]`, `sub ecx,1` / `je` -> case 1 (`003CA554`), then `cmp ecx,1` / `je` -> case 2. Other values go to `+0x32` = `005C5230(rcx)` (`003CA562`), whose `eax` is kept to the exit (`jmp 003CA840`).
    - Case 1: `+0x2A2` = `002432B0(rdi+0x50, [[0209AC30]+0x28], 3, rdi)` (`003CA7D2`). Words `+4/+6/+8/+0xA` go to `+0x98/+0x9A/+0x9C/+0x9E` under `test rdi` (`003CA7E7`). `+0x2E1` = `003200A0(0, rsp+0x38)`. `Q` = `[[rdi+0x60]+8]`; `00272CB0(dword [rsp+0x40] = L+8)` (`003CA82B`) is stored at `Q+0x18`, and `+0x306` = `0020E620(0)` is stored at dword `Q+0x20`.
    - Case 2: `+0x63` = `003200A0(0, L)`. `f` = `[rsp+0x44]` = `L+0xC`; `i` = `cvttss2si`; `t` = `cvttss2si((f-i)*10.0)` (`008F8180` = 10.0). `comiss f, 1.0` / `jb` (`003CA5DD`): not below gives `c` = `+0xB1` = `002DD7E0(0)`.
    - Below 1.0: `r12d` = 0x80, and `comiss 0, f` / `jb` keeps it (`003CA601`). When `f` <= 0, `r12d` = `cvttss2si(sinf((diff)*pi/30)*64+128)` (`003CA635` = `+0x105` = `sinf`; `01CEBC50` = pi, `008F8D80` = 30, `00916318` = 64, `008F3A2C` = 128). `[rcx+0xC0]` = `0208F570` when it was 0 (`003CA651`).
    - Blend: `+0x1C5` = `002752E0(out, bytes of +0x137 = 002DD7E0(6), bytes of +0x144 = 002DD7E0(0), cvttss2si(f*256.0))` (`003CA6F5`). Output dwords 0..2 are each `imul r12d` / `sar 7`, and byte 3 is the output's fourth byte unchanged.
    - `R` = `[[[rdi+0x60]+0x18]+0x18]`. `+0x23A` = `0029F6E0([[R+0x60]] or 0, 3, 5, c, [rsp+0x20] = i)` (`003CA76A`; `[rsp+0x20]` is the 5th argument). `+0x268` = `0029F6E0([[R+0x60]+0x18] or 0, 1, 5, c, t)`. Both cases return 0 (`003CA83E`).
    - **Signedness gap:** `mov eax, r14d` / `sub eax, ebx` (`003CA61B`) writes `eax` and so zero-extends `rax`. `cvtsi2ss xmm0, rax` (`003CA620`) then converts the 64-bit `rax`, so the 32-bit difference is taken as unsigned. The sentence writes it as a plain subtraction.
  - `00404E10` correct. `g = [02B62D88]`. It returns on null `g`, null `[g+0xC0]`, or `test byte [+0xC2], 1` non-zero (`00404E3B`). Then `00406DD0(g, 0)` (`00404E48`), `g` re-read, and `or byte [+0xC2], 1` (`00404E62`). The scan bound is `movzx` byte `g+0xE3`, over the array `[g+0xE8]` from `+8` with stride 0x18. `cmp [rax], 0` / `jg` (signed) breaks out. Index below count -> `jmp 00244F00` with `rcx = [g+0xC0]` (`00404EA9` = `+0x99`). Otherwise `rbx` = 0xC8, 0xD0 over `[[g+0xC0]+rbx]`, with null `g` / `[g+0xC0]` / slot skipped. `test al, 0x10` -> `or eax, 8` stored to `+0x130`, else `+0xDD` = `00245020(obj)` and `g` re-read (`00404EF2`). No `eax` is set on these paths.
- README count sentences checked against `rows.json`: "named 2 F-frontier functions", "2 staged with 10 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only; 331 accepted families, 19 in scope): neither function belongs to an accepted family, so the base rule applies.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.

## SWE2-AUDIT-SPEC narrowings

1. `rows.json` row `003CA530` (and the page block, re-rendered by `interior_applier.py --apply`):
   - old: ``(int)(`003CA530`+0x105((dword `0208F570` - dword `rcx+0xc0`)*pi/30)*64+128)``
   - new: ``(int)(`003CA530`+0x105((dword `0208F570` - dword `rcx+0xc0`, converted as an unsigned 32-bit value)*pi/30)*64+128)``
