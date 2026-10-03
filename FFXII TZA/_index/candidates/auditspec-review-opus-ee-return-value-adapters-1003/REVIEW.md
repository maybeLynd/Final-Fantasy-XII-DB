# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-return-value-adapters-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-RETURN-VALUE-ADAPTERS-1003` · Package: `_index/candidates/opus-ee-return-value-adapters-1003/` (rows committed in `3a61a9fcd`, reviewed at HEAD `050fd9350`) · Page: `24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 394 rows are correct against the bytes. The stated reason for four of the eight exclusions is false: those bodies are ordinary single-call members, refused only by the checker's fixed read window. The narrowing below corrects the exclusion sentence. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.**
  - Under the analysis venv python, `fam_rows.py check` stops with `ModuleNotFoundError: No module named 'pefile'`. `_rdata_refs` needs pefile, and the venv lacks it.
  - Re-run in place with `-B` under `C:\Python314\python.exe` (3.14.6, which has pefile and capstone): exit 0, `members 402, committed rows 394, declared exclusions 8` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. This is identical to the committed `fam_rows_check.out`.
  - The HEAD-committed `fam_rows.py` text was also run against the same rows in memory and gave FAILS 0. The working-tree copy is an uncommitted later revision.
- **What the checker tests.**
  - `ex_call_class` requires exactly one direct `call` within a **fixed 0x30-byte decode from the entry**, not over the body.
  - The getter is that call's target. T is the template argument of the MSVC RTTI type descriptor behind every `.rdata` vtable slot at index 5 holding the entry, and all such vtables must agree.
  - It compares all six columns with `rows.tsv`. Shared getters are dropped by `derive_all`.
  - It does not test the 26-byte masked form. An independent census (disw.py image reader) shows all **402** members with one masked form at size 0x1a, `push rbx / sub rsp,0x20 / mov rcx,rdx / mov rbx,r8 / call T / mov qword ptr [rbx],rax / add rsp,0x20 / pop rbx / ret`. No member is off the form, and no two rows share a getter.
- **Controls' sensitivity: the printed controls are tautologies.**
  - `ok1` compares row 0's extracted value with a row chosen because its value differs. `ok2` compares an anchor with that anchor + 1. Neither runs the comparison.
  - With an image-blind extractor (echoing `rows.tsv`), an in-memory harness still printed both controls "refused" and FAILS 0 (T6).
  - The comparison is sensitive. Mutating row 197 (`00641E00`) in memory failed each time: value swap (FAILS 2), name replaced (image `PGlow` vs row `PDeferredLighting`, FAILS 1), anchor + 1, mnemonic changed, row deleted (FAILS 1 each).
- **Sampled rows.** 20 rows at 0-based data-row indices 0, 21, 41, 62, 83, 103, 124, 145, 165, 186, 207, 228, 248, 269, 290, 310, 331, 352, 372 and 393.
  - For each, the body is the 26-byte form with its only call at entry + 0xC, the row's anchor and mnemonic. The call target equals the row's getter (for example `0058478C` -> `00599CA0` and `0087A6DC` -> `0087A410`).
  - **T was checked independently.**
    - 14 of the 20 (indices 0, 21, 62, 83, 103, 186, 207, 228, 248, 269, 290, 331, 352 and 372) match the class whose descriptor vtable holds the entry in column `s28` (slot 5) of `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/phyre-class-descriptor-vtable.tsv`. That table is generated separately by `gen_phyre_descriptor_vtables.py`.
    - The other 6 (template and non-Phyre types: indices 41, 124, 145, 165, 310 and 393) were checked with a separate RTTI reader written for this review. Every slot-5 vtable names the same T, for example ForType/Abstract/Concrete of `V?$PArray@PEAVPInputMap@PInputs@Phyre@@$07@Phyre@@` for `0087A6D0`, and ForType/Wrapper of `UD3D11_DEPTH_STENCILOP_DESC@@` for `006245E0`.
  - **20 of 20 exact.**
- **Excluded sample.** All 8 exclusions were examined, not just 5. All 8 have the shared 26-byte form with exactly one direct call inside the body.
  - **Genuine, 3:**
    - `0062F0F0`: ForType<PClassDescriptor> beside the non-template `PClassDescriptorForClassDescriptor`.
    - `0063C000`: ForType<PBase> beside `PClassDescriptorBase`.
    - `006B2950`: Matrix3, Matrix4 and PMatrix4 share the body.
  - **Wrong reason, 5, all "form (not exactly one direct call)":** the 0x30 decode runs 0x16 bytes past each 26-byte body into the next function, which has a call within that window.

    | entry | own call | body end | second call (next function) |
    |---|---|---|---|
    | `005D3460` | `005D346C` | `005D347A` | `005D348B` |
    | `005D46F0` | `005D46FC` | `005D470A` | `005D4717` |
    | `0063EF20` | `0063EF2C` | `0063EF3A` | `0063EF4B` |
    | `006AF570` | `006AF57C` | `006AF58A` | `006AF596` |
    | `006B2970` | `006B297C` | `006B298A` | `006B2994` |

    - Four of the five have a unique T and would derive rows on a body-bounded decode: `005D3460` PShader, `005D46F0` PShaderParameterCaptureBufferTexture2D, `0063EF20` PMotionBlurD3D11, `006AF570` PArray<PTypedObject>.
    - `006B2970` would still be excluded, for the type reason: Vector2, Vector3, Point3, Vector4 and Quat share it.
  - The true split is therefore 4 type-not-unique plus 4 refused only by the window. It is not 5 non-single-call plus 3 type.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors the member's only varying instruction, the call.
  - Each row states two member-specific values from the image: the getter, unique across rows, and T. The getter is printed bare, so only the adapter interior is credited.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met** for the 394 rows. The exclusions are conservative: they earn nothing, so no member is over-credited.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: the exclusion sentence in spec.json `lead` (and so on the page) and README "No rows".** Replace:

> Eight DF-4 members get no row, and each is listed with its reason in [`excluded.tsv`](...): five are not a single direct call, and three sit in descriptor vtables that do not name one template type T (a non-template descriptor class beside the template one, or several Vectormath types sharing one body).

with:

> Eight DF-4 members get no row; they are listed in [`excluded.tsv`](...). All eight have the shared 26-byte form with one direct call. Four sit in descriptor vtables that do not name one template type T: `0062F0F0` and `0063C000` (a non-template descriptor class beside the template one), and `006B2950` and `006B2970` (several Vectormath types sharing one body). The other four, `005D3460`, `005D46F0`, `0063EF20` and `006AF570`, are refused only because the checker decodes a fixed 0x30 bytes from the entry, which reaches a call in the following function. Their `excluded.tsv` reason "form (not exactly one direct call)" describes that window, not their bodies.

In README "No rows", replace "five are not a single direct call; three sit in vtables that do not name one template type" with "four sit in vtables that do not name one template type; four are refused by the checker's fixed 0x30-byte decode window, which reaches the next function's call (their own bodies are single-call members of the form)".

**Notes (non-blocking):**
- **Alternative repair.** Decode the census extent in `ex_call_class` (`R.at(a, _sizes()[a])` instead of 0x30), then re-derive. That gives 398 rows and 4 exclusions. This review has already verified the four new rows' getters and T (above). It needs a re-run of check and a recount in the lead and README (EE +4).
- **Control repair.** Pass mutated copies of `rows.tsv` through the comparison and add a raw-byte known-answer row; see the input-name review. Today's controls cannot fail while the extractor returns anything.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs an interpreter with pefile.
