# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-adm-add-motion-tables-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-ADM-ADD-MOTION-TABLES-HOMING-1003` · Package: `_index/candidates/fable-adm-add-motion-tables-homing-1003/` · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/adm-add-motion-tables.md` (commit eea05327e; reviewed at HEAD f8b2904c0, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 3 functions, 14 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 3 rows and 14 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. All 3 rows are on the page at lines 526–528 (heading at line 520), byte for byte.
- Semantic pass: **every row** was read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`0034DEA0`: exact.**
    - `00267E10(r9)` (`0034DEB1`) goes through `movd` / `cvtdq2ps` to f (`0034DEBD`).
    - Then `0026DAC0(rdx, f)` at +0x23 (`0034DEC3`, with `rcx` = saved `rdx`, `xmm1` = f).
    - It ends with the tail jump `0025B470(rdx, f)` (`0034DED8`).
  - **`00357570`: exact.**
    - Three pops in the order a (`edi`), b (`ebx`), c (`eax`), then `00359CA0(ecx = c, edx = b, r8d = a)` at +0x46 (`003575B6`).
    - A null result goes to `003575EE`, which writes `0026B4E0(rcx, 0)`.
    - Otherwise `00262F50(r14 = incoming rdx, result)` (`003575C9`). On 0 it writes `0026B4E0(rcx, 0)`. Otherwise `0026B4E0(rcx, 1)` (`003575DA`), then `0035AE10(result, 1)` (`003575E7`).
  - **`003B7210`: exact.**
    - b = `[rcx]`, off = `0020E600(dword b+0x68)` (`003B7229`), then the call at +0x21 (`002E6420`).
    - The returns are `test rdi, rdi` and `cmp dword [b + (int)off], 0` / `jle` (signed, `003B7242`).
    - The list sits at b + `0020E600(dword b+off+4)`. The loop uses `cmp di, [rsi]` / `jae` on entry and `cmp edi, eax` / `jl` per step. `js` skips a negative word `+2+i*2`.
    - i = 0 is skipped when qword `02EBCC68` is 0 (`003B72A1`).
    - For i > 0, it skips unless `i-1 < [02EBCBC0]` (`003B7287`, `jge`, signed), and q = `[02EBCAC0 + (i-1)*8]` (`[rbp + rbx*8 - 8]`).
    - Then `00262F50(00358940(rcx, entry), q)` (`003B72C1`).
- Advisory (not a defect): `02EBCC68`, `02EBCAC0` and `02EBCBC0` are the summoner list that `003B6DE0` fills (`04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md` lines 669–684). A cross-reference would show what q is.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
