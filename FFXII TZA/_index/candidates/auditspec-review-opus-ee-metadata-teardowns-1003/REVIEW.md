# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-metadata-teardowns-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-METADATA-TEARDOWNS-1003` · Package: `_index/candidates/opus-ee-metadata-teardowns-1003/` (rows committed in `3a61a9fcd`, reviewed at HEAD `050fd9350`) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Checker re-run.**
  - `fam_rows.py check` was run in place with `-B` under the analysis venv python; check mode writes nothing. Exit 0: `members 853, committed rows 803, declared exclusions 50` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. This is identical to the committed `fam_rows_check.out`.
  - The HEAD-committed `fam_rows.py` text was also run against the same rows in memory and gave FAILS 0. The working-tree copy is an uncommitted later revision.
  - The retool scan cache `Tools/work/OPUS/_re_cache.pkl` was unchanged (mtime 2026-09-30).
- **What the checker tests.**
  - `ex_metadata_teardown` enforces the form strictly: instruction 0 is `lea rcx, [X]` and instruction 1 is `jmp` to `00633240` or `006332A0`.
  - X is the rip target of that `lea`.
  - The registration is every site that loads X with `lea rcx` immediately followed by a call to `00632960` or `00632A10`. Exactly one must exist, and it must be named.
  - The name is the nearest `lea r9` within 10 instructions before the site. The offset is the nearest `mov dword ptr [rsp+0x20]` in the same window.
  - All six columns are compared. With `entry_anchor` set, an anchor equal to the entry is allowed.
  - Independent census: all **853** members have one masked form at size 0xc, `lea rcx,[rip+X] / jmp T`. Over the 803 rows, the helper pairs exactly with the constructor: `00633240` with `00632960` in 641 rows, and `006332A0` with `00632A10` in 162. No two rows share X.
- **Controls' sensitivity: the printed controls are tautologies.**
  - `ok1` compares row 0's extracted value with a row chosen because its value differs. `ok2` compares an anchor with that anchor + 1. Neither runs the comparison.
  - An image-blind extractor (echoing `rows.tsv`) still printed both controls "refused" and FAILS 0 in an in-memory harness (T6).
  - The comparison is sensitive. Mutating row 401 (`008B14E0`) in memory failed each time: value swap (FAILS 2), name/offset text replaced, anchor + 1, mnemonic changed, row deleted (FAILS 1 each).
- **Argument semantics checked against the constructors.**
  - In `00632960`, `r9` goes, as `r8`, to `00632FB0`, which stores it at `+0x18` and copies the string. That is the member name.
  - The 5th argument, the caller's `[rsp+0x20]`, is stored at `[X+0x48]`. The page (line 423) names `+0x48` "the field offset inside the owning object".
  - `00632A10` forwards its 5th argument unchanged as the 5th argument of `00632960`.
  - So "name = `lea r9`" and "offset = `[rsp+0x20]`" are what the bytes give.
- **Sampled rows.** 20 rows at 0-based data-row indices 0, 42, 84, 127, 169, 211, 253, 295, 338, 380, 422, 464, 507, 549, 591, 633, 675, 718, 760 and 802. Both constructors and both offset kinds (immediate, and register: `r15d`, `edi`, `esi`) are covered.
  - Each row was checked with an independent finder that byte-scans `.text` for `48 8D 0D disp32` loads of X.
  - In every case, X has exactly two loaders: the teardown itself and one registration site. The site is followed by the stated constructor call at the stated address, for example `005AD98D`/`005AD994` "m_animationSet" offset 0x20, `0064856E`/`00648575` "m_fogParameters" 0xDC, and `00879E6A`/`00879E71` "m_inputMaps" offset in `edi`.
  - The name and offset were taken from the instructions between the previous `call` and the site, a stricter bound than the checker's 10-instruction window.
  - **20 of 20 exact.**
  - The same segment-bounded check was then run over **all 803 rows**: 0 mismatches. No row's name or offset leaks from a previous registration.
- **Excluded sample.** 5 spread at excluded indices 0, 12, 24, 37 and 49: `008AA320`, `008AEA00`, `008B1800`, `008B4AF0` and `008BDE00`.
  - Each is in the 12-byte form. Its X has one other loader, which is followed by a call to a constructor other than the two data-member ones: `00632A70` for four of them, `00632BE0` for `008AEA00`.
  - Over all 50 exclusions: 29 go to `00632A70` and 21 to `00632BE0`. All 50 carry the reason "registration not unique or unnamed (0)".
  - These are not outside the 12-byte form. They are outside the row derivation, which recognises only `00632960` and `00632A10`. They get no row and earn nothing, which is conservative and correctly disclosed.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Members differ at the entry instruction. The jump target is one of two helpers and tracks the constructor kind exactly, so the adopted sentence's entry-instruction allowance applies.
  - Each row anchors that `lea` and states member-specific values from the image: X, unique, plus the member's name and offset with the registration site. The registration site is printed bare.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC narrowing / notes

- **Control repair (non-blocking).** Pass mutated copies of `rows.tsv` through the comparison and add a raw-byte known-answer row. Today's controls cannot fail while the extractor returns anything.
- **Wording precision (non-blocking).** "50 members have no unique named registration" is true only under the lead's own definition of a registration (a load of X followed by `00632960`/`00632A10`). Each of the 50 *is* registered once, through `00632A70` (29) or `00632BE0` (21). Saying so would let a later package give them rows if those constructors take the same name and offset arguments.
