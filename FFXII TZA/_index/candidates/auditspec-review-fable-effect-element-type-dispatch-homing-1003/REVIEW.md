# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-effect-element-type-dispatch-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-EFFECT-ELEMENT-TYPE-DISPATCH-HOMING-10` · Package: `_index/candidates/fable-effect-element-type-dispatch-homing-1003/` · Page: `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md` (commit eea05327e; reviewed at HEAD f8b2904c0, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 8 functions, 36 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 8 rows and 36 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0. Corrections 1 (`003A87B0`, the partial-entry shift; the corrected text is the one on the page). All 8 rows are on the page at lines 2406–2413 (heading at line 2400), byte for byte.
- Semantic pass: **every row** was read clause by clause against `disr.py` / `disw.py` output of the certified image (SHA256 73461D08...).
  - **`003340C0`: exact.**
    - `cmp edx, 0x1d` / `jge` is a signed guard. S is at `rcx + movsxd(edx)*4 + 0x2c`.
    - A null `0020E600(S)` stops the body (`003340E1`).
    - Otherwise `0046F370` and `003697F0`, each on a fresh `0020E600([rbx+0x2c])`, then `[rbx+0x2c] = 0020E620(0)` (`0033410A`).
  - **`00343E20`: exact.** `003588B0(003590D0())`. Null returns, otherwise the tail jump at +0x1E (`0026AE90`) with `edx = 0`.
  - **`0034C630`: exact.**
    - P = `002640C0()`, then pops a (`ebp`) and b, then `00358940(P, b)`.
    - Non-null: `00265380(P, rec, a)` at +0x4F, with the result stored to `[r8+8]` (`0034C684`). It returns `rax` of that call; the null path returns `rax` = 0.
    - `[r8] = rec` on both paths (`0034C691`).
  - **`0035A1C0`: exact.** `00320CA0(003589B0(), rsp+0x40)` (+0x14). Then `bt eax, ebx` on the 32-bit register, which takes the incoming `edx` mod 32; `jae` returns 0.
  - **`003A87B0`: exact, including FABLE's correction.**
    - The global is `02EBEF88`; the walk starts at `[g+8]`, with next at `+8` and previous at `+0`. The match test is `cmp byte [+0x13a], sil` (`sil` = `movzx cl`).
    - Unlinking patches the head `g+8` or the tail `g+0x10`.
    - When `[node+0x110]` is non-null, it calls `003A92D0(node)` and `003697F0([node+0x110])`.
    - The scan covers ≤ 0x20 entries from `g+0x18` and stops at -1. It matches the dword against node `+0x1c` and `movzx` byte `+4` against `movsx` node `+0x13b`.
    - `sub word [+6], 1` / `jne`, then a `test byte [+5], 1` gate.
    - The copy moves dword `+0`, byte `+4` and word `+6` (not byte `+5`, `003A8890`–`003A88A2`). It stops on a copied -1 or at index 0x1f, and dword -1 is written at the stop slot (`003A88BC`).
    - Then `003A8130(node+0x1c, movsx node+0x13b)`, and `003697F0(node)` for every matched node.
  - **`0042DA00`: exact.** `00421E20(rcx, movzx word rdx+8, dword rdx+0xc, qword rdx+0x10)`. Non-null stores `[rdx+0x10]` and dword 1 at `+0x18`; the result is returned in both cases.
  - **`0046E950`: exact.**
    - `cmp dword [rcx+8], -1` takes the path that clears `0x2` and returns `rax = rdx`.
    - Otherwise `002ED570(rdx, dword rcx+8)`. Null stores -1 and `0xffff` and returns `rax` = `0xFFFFFFFF` (`or eax, -1` zero-extends). Bit `0x2` is cleared on that path too.
  - **`00473B30`: exact.** `003589B0()`, then the tail jump at +0xF (`00290840`) with `ecx` = the dword result.
- Advisory (not a defect): `003340C0` is the row that was held from `gambit-evaluation-and-enmity` (SWE2-AUDIT-SPEC REJECT of that package). Its sentence is unchanged from the version checked there, and it is still exact.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
