# SWE2-AUDIT-SPEC review of the attached-bit readers (OPUS, 8643f130c): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
[sd192-attached-bit-readers-0930](../sd192-attached-bit-readers-0930/README.md) at 8643f130c, measured at HEAD
17a959c94 (first worker's census at HEAD 3cae47364; the package is unchanged between them). Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD192-0930 | `_index/candidates/sd192-attached-bit-readers-0930/` | `8643f130c` | ACCEPT-WITH-NARROWING |

**Re-run.** `sd192_readers.py` -> [rerun_sd192_readers.out](rerun_sd192_readers.out): identical to the committed
`.out` (ignoring CR), R1 and R2 PASS, `FAILS 0`. Package dir clean after re-run: yes (`git status --porcelain` on it
prints nothing).

**Re-derived independently.**
- Raw census ([sd192_census.py](sd192_census.py) / [sd192_census.out](sd192_census.out)): every executable section
  searched for a disp32 of 0x140..0x14F on a non-rip base, image-wide, not only listed bodies. The byte-exact bit-0
  tests of `+0x14F` are 10 `test byte [r+0x14F], 1` sites (`0025B637`, `0025B76F`, `00267286`, `002E274A`,
  `002E506A`, `002E5776`, `002E602C`, `002E634B`, `002EA816`, `003B7934`) plus `003B7812`
  `test byte [rax+0x14F], r12b`, with r12d = `lea r12d,[r15+1]` after `xor r15d,r15d` = 1 ([dump_h.out](dump_h.out)).
  That is the author's 11-site census exactly. `002E602B`, `002EA815`, `003B7813` in the `.out` are the same
  instructions decoded one byte off, not extra sites.
- The five `movzx` readers, decoded from their function starts ([dump_e.out](dump_e.out), [dump_d.out](dump_d.out),
  [fdis.py](fdis.py)): each loads the byte and shifts right with nothing between. `002E2A82` and `002E8273` store
  `byte >> 3` to `[slot+0x413]`; `002E9B4C` returns bit 1; `002EA2BE` and `002EAC0D` take bit 1 (forced to 1 when
  controller `+0x12` >= 0x10). None reads bit 0, which closes the README's second limit.
- Wider non-SIMD reads covering `+0x14F` on non-rsp bases (76 census rows, `lea` excluded): 9 dword/word GPR reads
  (copies, one `cmp`, one `sub` - no bit test as first use), 4 MMX `movd` decodes, the two `003B7812` rows, and 61
  qword rows at `+0x148` (some are one-byte-off duplicates). None of the 61 has a bit test as its first use; where a
  use is visible it is a pointer test, dereference, compare or copy. A struct with a qword at `+0x148` is not the
  controller, whose `+0x14F` is a flags byte. No `bt`, `cmp` or `shr` on the byte in memory.
- All eight branch targets dumped to `ret` from the function starts ([dump_a.out](dump_a.out),
  [dump_b.out](dump_b.out), [dump_c.out](dump_c.out)): `0025B735`, `0025B7CD`, `00267272`, `002E5951`, `002E6071`,
  `002E639F`, `002EA858` are register restores and `ret`; `002E5164` adds only the cookie check `00808C40`. No store
  to memory and no other call on any of them. The author's `epilogue()` exemption of `00267272` hides nothing:
  `00267272` is `xor eax,eax; add rsp,0x20; pop rbx; ret`. In `002E6000` the two instructions between the test and
  the `jne` (`mov [rsp+0x58], rdi`; `mov rdi, [rcx+0xB8]`) do not touch flags.
- The base in every reader is `[actor+0xC0]`, the controller per the owning page's layout (`+0xC0 ptr controller`).
- R2: `00267272` = `xor eax, eax`; `002EA7FA` = `xor edi, edi` and `002EA858` = `mov eax, edi`. Confirmed.

**Controls.** The defect to catch is a bit-0 reader outside the `test byte [r+0x14F], 1` form. The raw census is
sensitive to it: it returned the register-mask form `003B7812` and all five `movzx` readers, which the author's
form-restricted sweep could not see. Blind spot left: `+0x14F` reached through a pre-offset pointer
(`lea r,[ctrl+0x1xx]` then a disp8) or a whole-struct copy; not searched here.

**Citations checked.** The eight test/branch/target triples in `sd192_readers.py` match the bytes. The skipped work
per reader matches the calls behind each branch: `0025B740` tail-jumps `00238B20` with ecx = 1; `002E6000` calls
`00263910` and `003EC3D0` only past the branch; `002E6330` tests actor `+9` bit 6 and calls `002E9FE0`; `002EA7F0`
reads `[+0x138]+0xF0` only past the branch.

**Narrowing.** The measurement is sound; the headline overreaches. The census has 11 bit-0 readers. Three do not refuse
movement: the attach guard `002E274A` (calls `002E6B10` when the bit is set) and the presentation readers
`003B7812` / `003B7934` (select a value with `cmovne`). "Every reader" is true of the eight movement-side readers.

**Correction wording.** In the README title and the SD-192 row lead, replace "every reader of the attached bit
refuses movement on it" / "every reader refuses" with: "every movement-side reader of the attached bit (the eight
checked; not the attach guard `002E274A` or the two presentation readers) refuses movement on it". In the Limits,
replace "Those five were not read here." with "SWE2-AUDIT-SPEC read them (2026-09-30): they use bits 1 and 3-7, not
bit 0."
