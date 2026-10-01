# SWE2-AUDIT-SPEC review of ASTRA special-action-override-label-binding (a568f9b5e): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75), 2026-09-30. Producer: ASTRA.
Reviewed: `ASTRA-PUBLISH-SPECIAL-OVERRIDE-LABELS-0930` at `a568f9b5e`, packet
`_experiments/evidence/special-action-override-label-binding/` (final result 02, prerequisite controls 02), image SHA
`73461d08…21f8`. Static only; nothing was executed natively.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-SPECIAL-OVERRIDE-LABELS-0930 | ASTRA-PUBLISH-SPECIAL-OVERRIDE-LABELS-0930 | a568f9b5e | ACCEPT |

Accepted in the packet's own scope. This is a label representation and state-to-word correlation under the
unchanged-state and unchanged-table premise. It is not a no-write proof, and constructor return, writers, aliases,
lifetime, combat meaning, presentation and reachability stay OPEN.

**Clause by clause** (from [labels_indep.out](labels_indep.out); my own tk.py decode and store emulation, not the
packet's reducer)

- *Nine NUL-terminated ASCII prefixes from the original stores, without filling padding.* `001D03E1`..`001D04D1` is
  33 instructions with no branch, call or ret. `rdi` is set once, at `001D03C3 mov rdi, rcx`. There are 17 stores
  into +0xAE4..+0xC03, which matches the packet's 17 `writes`, and no `[rdi+disp]` store outside that range.
  Applying them to a byte map, and leaving unwritten bytes unknown, gives:
  - slot 0 `OFF`, slot 1 `Black Hole`, slot 2 `Luminescence`, slot 3 `Ark Blast`, slot 4 `Whiteout`,
    slot 5 `Windburst`, slot 6 `Torrent`, slot 7 `Cataclysm`, slot 8 `Inferno`;
  - every slot has a written NUL, and 19 to 28 bytes per slot after it are never written. HOLDS.
- *OFF plus the eight names mapped to 241/231/234/237/229/228/227/226.* The words at `00D0F9E0` are
  [241, 231, 234, 237, 229, 228, 227, 226]. The control writes index state-1, and the domain review
  (auditspec-review-astra-special-override-domain-0930) confirms that step. So state k gets label slot k and word
  k-1, and state 0 gets OFF with index -1 and no word. HOLDS under the premise.
- *Item 182 is an internal formatter selector.*
  - The formatter is `001CD0E0`. `001CD13A movsxd r13, edx` takes the selector argument, and
    `lea eax, [r13 - 1]; cmp eax, 0x125; ja` bounds the index to 0..293. The only index that reaches `001CE9AA` is
    181, which is item 182.
  - `001CD0E0` has 7 direct call sites (`rawcalls.json`: 3 in `001D0190`, 1 in `001D0390` that loads `edx` from a
    dword table, and 3 in the `001D54xx`..`001D55xx` range), and no address-taken reference or relocation.
  - Nothing here reads it as a script verb or action id. I did not trace each caller's argument source.
- *The 294-entry table from CMP 125h and RET 1CFCEB.*
  - Dispatch is `mov ecx, [rsi + rax*4 + 0xafcec]; add rcx, rsi; jmp rcx` with `rsi` = `rip - 0xad186` = the image
    base, so the table starts at `001CFCEC`. The byte at `001CFCEB` is `C3` (ret).
  - All 294 entries target inside the owner, with 263 distinct targets.
  - Control: the one-past dword + base is `CCDECCCC`, outside the code, so a 295-entry reading would be wrong. HOLDS.
- *The formatter arm and the exact inline layout.*
  - `001CE9AA movsxd rax, [r15 + 0xae0]` sign-extends; `shl rax, 5` gives a 32-byte stride; then
    `lea rcx, [r15 + 0xae4]; add rcx, rax` and `mov [rsp + 0x28], rcx`. No clamp exists between the load and the use.
  - `001CD57F lea r8, [008FFAE0]` loads the format `"%s%s %s "`. The call at `001CD517` (buffer `r12`, size 0x100)
    has `r9` as the first string and `[rsp+0x20]` = `[r15 + r13*8 + 0x130]` as the second, so the label pointer at
    `[rsp+0x28]` is the third `%s`.
  - `r15` is set at `001CD141 mov r15, rcx`, and the path to the arm (`001CD1D5 jmp rcx`) does not redefine it. It
    is also written at `001CF62F`/`001CF632` and `001CF833`/`001CF836`, which are two other branches; this agrees
    with the README's "R15 is reused elsewhere".
  - State 9 would address +0xC04, just past the nine slots. HOLDS.
- *Actual missing, incomplete and corrupt-source refusals.* Reproduced (see Re-run).

**Re-run.**
- I ran the packet's `prove-special-override-label-binding.py`, its `exercise-special-override-label-prerequisites.py`
  and all three capture drivers from the repository root into fresh files in this directory. The result, the three
  raw captures and the control summary are byte-identical to the committed files ([compare_rerun.out](compare_rerun.out)).
  I then removed the raw copies and each case directory's copied inputs, keeping the receipts, stdout and stderr.
- The five cases: `positive` exits 0 with the nine labels. Four cases refuse (exit 1, no result):
  - `missing_raw` (file not found);
  - `incomplete_wrapper` ("capture completion prerequisite");
  - `changed_instruction` ("original instruction/coverage prerequisite");
  - `wrong_table_extent` ("guard-derived switch data prerequisite").
- The packet directory was clean before and after.

**Controls.** Each refusal is sensitive to the defect it names:
- `wrong_table_extent` changes only the entry count and is caught by the table-versus-bytes check;
- `changed_instruction` alters one instruction's bytes (`shl rax, 5` to `shl rax, 4`) and is caught by the per-byte
  check against the pinned EXE;
- the OFF literal is a positive control on the reducer.

These are integrity controls on the evidence chain. My independent emulation above is what checks the semantic
result, and it agrees.

No correction is needed.
