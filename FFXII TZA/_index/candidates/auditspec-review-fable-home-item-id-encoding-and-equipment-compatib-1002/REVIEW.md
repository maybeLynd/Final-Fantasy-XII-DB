# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-item-id-encoding-and-equipment-compatib-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ITEM-ID-ENCODING-AND-EQUIPMENT-CO` · Package: `_index/candidates/fable-home-item-id-encoding-and-equipment-compatib-1002/` · Page: `12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 3 functions, 14 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 3 rows, 14 anchors; mechanically rejected 3, skipped 0, missing 0. Each row's text is on the page verbatim.
- Semantic pass: **all 3 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `003DFDD0`: `[r8]` and `[r8+8]` are zeroed before the `lea eax, [rcx-1]; cmp eax, 7; ja 003DFE24` bound (unsigned). The table was read from the image at `00120000 + 0x2BFE38` = `003DFE38`, eight dword slots rebased on `00120000`: `ecx` 1,2 -> `003DFE05` (+0x35, `00264A40`; result to `[rbx]`, and when non-null `rax+0x10` to `[rbx+8]`), 3,5,6,8 -> `003DFE1C` (+0x4C, `00264CA0`; result to `[rbx]`), 4,7 -> `003DFE24` (the return test). Every path ends `cmp [rbx], rdi(0); setne dil`, with `rbx` = the incoming `r8`. Exact.
- `003FE3A0`: calls at +0x6 (`xor ecx, ecx` first), +0xB (no argument set; the text states none), +0x12 (`xor ecx, ecx`); `mov rax, [0209AC30]; mov rcx, [rax+0x130]; test; je` skips the +0x33 call, which takes `rcx = [rcx+0xC0]`, `edx = 0`; the tail `jmp 002858A0` at +0x40 has `ecx = edx = 0`. Exact.
- `003FE6E0`: +0x6 call with `ecx = 0`; the `+0x130` null test returns (`003FE710`), otherwise the tail jump at +0x2B with `rcx = [obj+0xC0]`, `edx = 0`. Exact.
- Sites: `003DFBE0` + 0x2F = `003DFC0F call 003DFDD0`; `003FF360` + 0x4F2 = `003FF852 call 003FE3A0`; `003FF360` + 0x3A6 = `003FF706 call 003FE6E0`.
- Host: `003FF360` is the page's equip-menu body (L245, and its own SWE2-EC7-33 update at L495-L497, with L544/L564 reading its callees). `003DFBE0` is cited only on this page in the whole DB (grep outside `_index/candidates`), at L505 as one of the item-record lookup helpers the page's `00400CF0` calls; `003DFDD0` is its by-kind record resolver, so it belongs with that helper here.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
