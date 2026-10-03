# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-eastl-string-initialisers-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-EASTL-STRING-INITIALISERS-1003` · Package: `_index/candidates/opus-ee-eastl-string-initialisers-1003/` (asked at `047553008`; reviewed at HEAD `33eb7192f`. Since `047553008` only `fam_rows.py`, `README.md`, `excluded.tsv` header and `fam_rows_check.out` changed, in `c480be543`; `rows.tsv`, `spec.json` and the page section are unchanged; the package is unmodified in the working tree) · Page: `23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md` (section "Per-member rows: the static string object each EASTL basic_string<char> initialiser builds", installed)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 51 rows are correct against the bytes, and each row's S is unique. The lead is wrong in three places:
- It says "What differs from member to member is S". Members also differ in the literal address, in the literal length (three immediates) and in the teardown pointer, which is unique per member.
- It says "All 51 make exactly these external calls" but leaves out the `memmove` import call that every member makes.
- It describes the allocate branch as "a length above 1". The value compared is the literal length + 1.

The narrowing below corrects the lead. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** `fam_rows.py check` was run in place with `-B`, using the analysis venv python, which imports pefile here.
  - Exit 0: `members 51, committed rows 51, declared exclusions 0` / `control swapped-value: refused (2 failure(s) ...)` / `control moved-anchor: refused (1 failure(s) ...)` / `known answer 0015CE70: anchor 0015CEA3 references 01F83230 in its raw bytes = committed value` / `FAILS 0`.
  - The output matches the committed `fam_rows_check.out`, apart from line endings. Check mode writes nothing.
- **What the checker tests.** `ex_string_static` decodes the census extent (`_body` over `check_dispositions.load_functions`).
  - It requires exactly one `movdqu xmmword ptr [rip+d]` and exactly one `lea rsi, [rip+L]`, and a clean C string at L.
  - It anchors the `movdqu`, then compares all six columns with `rows.tsv`. Values shared between members are removed in `derive_all`.
  - It does not check the shared form that the lead describes: the two `001EDF00` calls, the slot `+0x10` call, the sentinel, or the `00808B90` tail. So the README's "the family form is part of the check" means only those two instruction counts.
  - Membership comes from the members file, so this does not affect any row. Fed to the extractor, the six 228-byte variant initialisers (`0015C560`, `0015C650`, ...) are refused (no clean literal). So are `0015DBB0` and `001601C0` (no store).
- **Controls' sensitivity (fed back to the checker in memory).** `cmd_check` was run with `read_rows` / `EXTRACT` patched.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the checker still prints both mutation controls "refused" and FAILS 0. Those two controls exercise the comparison, not the image.
  - The **known-answer** line is a real image control for row 0. It decodes the anchor's raw bytes, so it does not depend on the extractor. Row 0's value + 1 gives `known answer ... FAIL` and FAILS 2.
  - The comparison is sensitive. Each of these mutations failed:
    - values of `0015E870` and `0015E960` swapped: FAILS 2;
    - literal of `0015E870` changed: FAILS 1;
    - anchor of `0015E870` moved 8 bytes back, onto the `mov qword [S+0x10], 0` store: FAILS 1;
    - row deleted: FAILS 1.
- **Independent census** (disw.py image reader with capstone, over `graph/functions.tsv` extents; not retool or fam_rows).
  - **One form.** All 51 members are 240 B and 49 instructions. Rip targets were normalised to S-relative and L-relative, and the instruction streams compared position by position. Only these positions vary:
    - S, at 11 operand sites: `+0x1E`, `+0x2C`, `+0x33`, `+0x59`, `+0x6A`, `+0x77`, `+0x7E`, `+0x8E`, `+0xA5`, `+0xAC`, `+0xB3`, `+0xD0`. Each normalises to the same S-relative operand in every member, so every site in a member names the same S. The movdqu at `+0x33` is one of them.
    - L: `lea rsi, [L]` and `lea rax, [L+n]`.
    - The literal length n (2, 4, 5 or 0x16), in three immediates: `lea rax, [L+n]`, `mov r8d, n`, `lea rax, [rdi+n]`.
    - The teardown pointer: `lea rcx, [T]` before `jmp 00808B90`. There are **51 distinct T**, `008A6D50` ... `008A80A0`, so T is as member-unique as S.
  - The page's own frontmatter says the same: "the other 62 are the operands that must vary: object, literal, dtor".
  - The call/jump skeleton is identical in all 51 members:
    - `call 001EDF00` ×2;
    - `jbe`;
    - `call [rax+0x10]`;
    - `jmp`;
    - **`call [008C2A40]`**, which is VCRUNTIME140 `memmove` (pefile import table);
    - `jmp 00808B90`.
  - The length test is `lea rax,[L+n] / sub eax, esi / inc eax / cmp eax, 1 / jbe`. It is unsigned, and the value compared is n + 1, so the allocate path is taken for any non-empty literal. All 51 literals are 2-22 characters long, so every member allocates.
  - The empty-literal path stores begin = end = `02EBA2E0` and capacity end = `02EBA2E1`.
  - The allocate path stores begin = end = the allocation and capacity end = allocation + n + 1. After `memmove(S.begin, L, n)` it sets end = begin + n and stores a NUL at end.
  - The two `001EDF00` calls take `rcx = rsp+0x30` (name `008F6600` "EASTL basic_string") and then `rcx = S+0x18` (`rdx` = the first result), as the lead says.
- **All rows re-derived independently: 51 of 51 identical** to `rows.tsv` (entry, anchor, mnemonic, S, literal text and address). There are 51 distinct S.
- **Image-wide completeness.** A raw `E8` index of calls to `001EDF00`, joined with `48 8D 15` loads of `008F6600`, finds every member (51 of 51).
  - A mnemonic-skeleton scan over the 240-B bodies finds 52 matches. The one non-member, **`0015FFE0`** (S `01FD3FB8`, `"\t"`), would derive under this extractor.
  - It is not a defect. The frontmatter records that it left the family as A-measured ("0015FFE0 excluded as A-measured -> 51 members", selector record on the board).
- **Sampled rows.** 15 spread rows were checked from raw bytes only, with no capstone: indices 0, 4, 7, 11, 14, 18, 21, 25, 29, 32, 36, 39, 43, 46 and 50 (`0015CE70` ... `001600D0`).
  - Each anchor is `F3 0F 7F 05 rel32` at entry + 0x33, and the rel32 resolves to the committed S.
  - Each body's `48 8D 35 rel32` resolves to the committed literal address, and the NUL-terminated bytes there are the committed text. For example `009047A0` holds `5C 22` (`"\""`), and `00904788` holds `0123456789ABCDEFabcdef`.
  - **15 of 15 exact.**
- **Excluded sample.** `excluded.tsv` is empty, so there was nothing to sample. The extractor reads the census extent rather than a fixed byte window, so defect (b) cannot arise.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction that distinguishes the member (S-bearing, unique) and states S and the literal, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop and the row-0 known answer.
  - **Conditions met.** The lead's error is in the shared-form description, not in the rows.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: the lead, in spec.json `lead` and the installed page section.** Replace:

> and copies a literal into it: for a length above 1 it allocates through the allocator's slot `+0x10` and stores begin, end and capacity at `S+0`, `S+8` and `S+0x10`, otherwise it points S at the empty-string sentinel `02EBA2E0`; it then tail-jumps to `00808B90` with its teardown (the atexit registration). All 51 make exactly these external calls. What differs from member to member is S: no two members initialise the same object.

with:

> and copies a literal into it: when the literal length + 1 is above 1 (`cmp eax, 1` / `jbe`, so for any non-empty literal) it allocates length + 1 bytes through the allocator's slot `+0x10` and stores begin, end and capacity end at `S+0`, `S+8` and `S+0x10`, otherwise it sets begin and end to the empty-string sentinel `02EBA2E0` and capacity end to `02EBA2E1`; it copies the literal with `memmove` (`call [008C2A40]`), sets end and writes the terminating NUL, then tail-jumps to `00808B90` with its own teardown (the atexit registration). All 51 make exactly these external calls. Members differ in four operands: S (at every S-relative site), the literal address L (`lea rsi` and the end-pointer `lea rax`), the literal length (three immediates) and the teardown pointer passed to `00808B90` (one per member). S is the value stated here: no two members initialise the same object.

**Notes (non-blocking):**
- **Control naming.** "swapped-value" and "moved-anchor" test the comparison only. An image-blind extractor still passes them (T6). The row-0 known answer is the control that reads the image, so the README should say which control does what. Making the known answer cover every row would be cheap: every anchor here is `F3 0F 7F 05 rel32`.
- **Form check.** The README's "refuses a member whose body does not have the family's form" overstates `ex_string_static`, which counts one `movdqu` store and one `lea rsi`. Either add the call-skeleton test (`001EDF00` ×2, `[008C2A40]`, `jmp 00808B90`), or reword.
- **Literal text.** The literal column gives the image bytes verbatim. `"\b"` is the two characters `5C 62`, a JSON escape spelling, not a backspace. A short note in the lead would stop a reader misreading the column.
