# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-the-actor-manager-record-field-map-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-ACTOR-MANAGER-RECORD-FIELD-MAP-HOM` · Package: `_index/candidates/fable-the-actor-manager-record-field-map-homing-1003/` · Page: `04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md` (commit b35f1958c; reviewed at HEAD 15ec1ea71, and the page is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 2 functions, 10 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 2 rows and 10 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, and 1 correction (`003E94D0`: "divided by 1.0" became "divided by float `01DFE0BC`", because the cell is in `.data`). The README count sentence ("2 staged with 10 anchors ... 0 ... 0 ... 0") matches. Both rows are on the page at lines 1064-1065 (heading at line 1058), byte for byte.
- Homing premise: both bodies call `002E1040`, which the page documents; it leads the heading `Interior citation — frontier hub 002E1040`.
- Semantic pass: **every row** was read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`003E9480`: exact.**
    - It calls `002E1040` with the incoming registers (`003E9490`; `edx` is kept sign-extended in `rdi`, `r8d` in `ebx`).
    - It exits when qword `[rax]` is null (`003E949B`), when `edi >= movzx word [rax+0x54]` (`003E94A1`, `jge`, signed), or when byte `+0x3F3` of the object is negative (`003E94A5`, `jl`).
    - Otherwise it stores `bl << 4` (`003E94BA`) at byte `[qword +0x3F8] + edx*0x60 + 0xD` (`lea rcx,[rdi+rdi*2]` / `shl rcx,5`, `003E94C1`).
  - **`003E94D0`: exact.**
    - It has the same call and the same two guards (`003E94DF`, `003E94F0`).
    - It then calls `002A2650` at +0x45 (`003E9515`) with `rcx` = the qword, `edx`, `r8` = the incoming `r8`, and `r9d` = dword `r8+4`.
    - The fifth argument (`[rsp+0x20]`) is dword `r8+8`, converted through `cvtdq2ps`, divided by float `[01DFE0BC]` (`003E9505`) and truncated through `cvttss2si` (`003E950D`).
    - FABLE's correction is right: `01DFE0BC` lies in `.data`.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
