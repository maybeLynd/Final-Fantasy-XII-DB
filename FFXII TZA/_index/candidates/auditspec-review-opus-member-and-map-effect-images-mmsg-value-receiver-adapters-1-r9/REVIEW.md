# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-and-map-effect-images-mmsg-value-receiver-adapters-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-AND-MAP-EFFECT-IMAGES-MMSG-VAL-84895` · Package: `_index/candidates/opus-member-and-map-effect-images-mmsg-value-receiver-adapters-1-r9/` (reviewed at HEAD `a028be1b9`) · Page: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 24 member rows (family `MMSG value receiver adapters`, mode `member`), 3 anchors each, 72 anchors in total. All 24 rows were checked against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every row holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 24 functions, 72 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Template rows, proven mechanically.** Every body is the same four instructions followed by int3 padding (the byte after the `jmp` is `cc` in all 24):
  - `movsxd rdx, ecx`
  - `mov ecx, K`
  - `mov qword ptr [rip + X], rdx`
  - `jmp 0x238640`
- The first row, `002F76A0`, was read in full: the sign-extension into `rdx`, `ecx` = 3, the qword store resolving to `02EC3D98`, and the tail `jmp` to `00238640`. That matches its sentence exactly.
- **How the other 23 rows were proven equivalent.** A checker (`w10/scratch_kk/chk.py`, output in `chk.out`) decoded each body and required all of the following:
  - exactly the four instructions above, in that order;
  - the `mov ecx` immediate equal to the number in the sentence;
  - the store's rip target (computed as next-instruction address plus displacement) equal to the qword cell in the sentence;
  - the `jmp` target equal to `00238640`;
  - the three anchors equal to the `mov ecx` / store / `jmp` instruction addresses and mnemonics.
- All 24 rows passed (`member rows 24 bad 0`).
- **Body diff and sentence diff.** `tdiff.py` against `002F76A0` shows one differing instruction (`mov ecx, K`) for `002F76C0`, `002F7760` and `002F79A0`. `tdiff.py` normalises rip operands, so the cell substitution does not appear in its output; the checker above resolved each cell separately. Every sentence matches one fixed template whose only variable parts are the cell address and the immediate. So the character diff between any two sentences is exactly the cell and `ecx` substitutions that the bodies show.
- **Per-row values (cell / `ecx`), checked against the bytes:**
  - `002F76A0` 02EC3D98/3, `002F76C0` 02EC3DC0/8, `002F76E0` 02EC3DA8/5, `002F7700` 02EC3DE8/0xD
  - `002F7720` 02EC3DD0/0xA, `002F7740` 02EC3DC8/9, `002F7760` 02EC3E20/0x14, `002F7780` 02EC3DF0/0xE
  - `002F77A0` 02EC3DF8/0xF, `002F77C0` 02EC3E08/0x11, `002F77E0` 02EC3DD8/0xB, `002F7820` 02EC3E00/0x10
  - `002F7840` 02EC3E30/0x16, `002F7860` 02EC3E38/0x17, `002F7880` 02EC3E40/0x18, `002F78A0` 02EC3E48/0x19
  - `002F78C0` 02EC3E50/0x1A, `002F78E0` 02EC3E58/0x1B, `002F7900` 02EC3D88/1, `002F7920` 02EC3E10/0x12
  - `002F7940` 02EC3E18/0x13, `002F7960` 02EC3DB0/6, `002F7980` 02EC3D90/2, `002F79A0` 02EC3DB8/7
- **Callee claims.** The sentences say only what each body passes to `00238640` (`ecx`, `rdx`). They make no claim about what `00238640` does, so no callee read is needed.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test the family name or what the receiver at `00238640` does with the pair.
- The checker proves equivalence to the template. The template itself was confirmed by reading `002F76A0` and spot-reading the dumps of the other rows, not by a second independent decoder.
