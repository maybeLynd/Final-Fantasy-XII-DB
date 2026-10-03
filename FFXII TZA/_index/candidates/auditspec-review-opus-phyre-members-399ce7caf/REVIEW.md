# SWE2-AUDIT-SPEC review: 272 Phyre module members in member mode, 11 records (opus-phyre-members-399ce7caf)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-PHYRE-MEMBERS-399CE7CAF` · Records: the 11 `_index/candidates/opus-member-*` records touched by commit 399ce7caf · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 154 rows read are exact at the bytes. Every correction listed in `rows.json` is right. The one defect is the batch-wide correction count: the request and all 11 READMEs give it, and it does not match the records.

**Narrowing (exact wording).** In each of the 11 READMEs, replace "262 stood, 10 clauses in 8 functions were corrected" with:

> 262 stood and 10 were corrected (12 correction entries in the records' `rows.json`, in 10 functions)

Keep the parenthetical list of kinds that follows. In the board request, "10 clauses in 8 functions corrected" reads the same way.

## SWE2-AUDIT-SPEC checks

- **Population.** Commit 399ce7caf touches exactly these 11 records. Their `rows.json` row counts are 40 + 40 + 17 (pinputs 1-3) + 28 (plod) + 18 (pserialization) + 17 (pgameplay) + 40 + 16 (pgeometry 1-2) + 19 (pscripting) + 30 (pdynamicgeometry) + 7 (ptext) = **272**, which matches the request. The `prendering-*` / `phyrecore-*` records in the same folder come from other commits and are out of scope.
- **Instrument.** `interior_applier.py` was re-run fresh without `--apply` on all 11 records. Each printed `ALREADY` and `FAILS 0`, with VERIFY counts (functions/anchors) of 40/200, 40/196, 17/85, 28/139, 18/77, 17/76, 40/197, 16/80, 19/91, 30/149 and 7/33.
- **Correction count (the defect).** Counted across the 11 `rows.json` files: pinputs-2 has 2 (`00873FE0`, `00874080`), plod 1 (`006C7B90`), pserialization 6 (`0059D4B0`, `0059FD10`, `005A0120` x3, `005A0250`), pscripting 1 (`00685DB0`, two clauses in one entry), pdynamicgeometry 2 (`006BB6D0`, `006BB7D0`), and the other six records 0. That is **12 entries in 10 functions**, or about 13 clauses. No count gives "10 clauses in 8 functions". The same README's "262 stood" itself implies 272 - 262 = 10 corrected functions.
- **Corrections, all 12 confirmed at the bytes.**
  - The pinputs-2 pair are signed compares (`cmp ...,0x1a; jle` skip, and `cmp ...,0x1c; jge` skip), which the corrected rows state.
  - The two pdynamicgeometry groupings: `shl rdi,4; add rdi,[rcx+0x28]` then dword `[rdi+8]`.
  - pscripting `00685DB0`: rcx-relative `+0x60` / `+0x48` pairs with per-pair callees `00584730` / `00682D90`.
  - plod `006C7B90` and the pserialization six: see the per-record reviews.
- **Semantic pass: 154 of 272 rows** read clause by clause against `disr.py` output of the certified image, covering all 11 records. All exact:
  - ptext: all 7. Record `auditspec-review-opus-member-teen-modules-registered-before-main-phyre-ptext-module-1`.
  - pdynamicgeometry: 19 of 30. Record `auditspec-review-opus-member-s-registered-before-main-phyre-pdynamicgeometry-module-1`; `006D2DA0` read in full.
  - pscripting: all 19. Record `auditspec-review-opus-member-modules-registered-before-main-phyre-pscripting-module-1`.
  - plod: 21 of 28. Record `auditspec-review-opus-member-fteen-modules-registered-before-main-phyre-plod-module-1`.
  - pserialization: all 18. Record `auditspec-review-opus-member-les-registered-before-main-phyre-pserialization-module-1`; imports resolve to ReadFile / SetFilePointer / WriteFile.
  - pinputs-1: all 40, 15 read by hand and 25 release bodies matched mechanically to the hand-read `0086CE50` (vtable, release size, branch shape). Record `auditspec-review-opus-member-en-modules-registered-before-main-phyre-pinputs-module-1`.
  - pinputs-2: 8 rows. `00873FE0`, `00874080`, `00874120` (`add -0xb; cmp 2; jbe`), `00874170` (the `+0x38` replacement tests slot `+8` of the `+0x30` object), `00873C10`, `00873C30`, `00873090`, `00875F00`.
  - pinputs-3: 5 rows. `00876020`, `00876130`, `008766D0` (name 01CD8458 = `PInputJoypadButtonSemantic`), `008794F0`, `00879600`.
  - pgameplay: 6 rows. `006A91C0`, `006A9290`, `006A97C0` (the final 1.0/0 map, including `+0x44` written 1.0 then 0), `006CD390` (import 008C3000 = `_stricmp`, string 00D4E5C0 "Performance warning"), `006CDB70`, `006CE0D0`.
  - pgeometry-1: 5 rows. `00662890`, `00662B60`, `00663100`, `00665220`, `006652B0`.
  - pgeometry-2: 6 rows. `0066F280`, `0066F330` (`test byte [rsp+0x54], dil` with `dil` = 2; `js` signed), `0066F710`, `00670590`, `006708A0`, `00672A20`.
- **Signed versus unsigned** (the request's named risk). No signed compare is written as above/below in any row read. The forms that carry no stated signedness are all unsigned in the bytes and harmless as worded: every `min(...)` (`cmovb`), "at most 1" (`cmp ...,1; ja` / `jbe`) in pscripting and plod, and "above 1" in pgeometry (a `jbe` on a count masked to 31 bits, so sign-neutral). Optional "(unsigned)" additions are noted in the per-record reviews and are not required.
- **Advisories in the per-record reviews (not defects):**
  - pinputs-1 `0086D670`: `{00873C10, 0}` is written by a 16-byte `movups` whose last dword is uninitialised stack.
  - pserialization `005A0250`: the quoted format string omits its trailing `\n`.
- **Limits hold.** These are body statements and static evidence only. The drafting agent, the second local reader and OPUS's confirmation are not independent; this record and its six per-record siblings are. The superseded per-record board requests whose truncated ids collided are reviewed in those siblings: pscripting stands for the `...MODULES-REGISTERED-BEFORE-MAIN-PHYRE` id and pinputs-1 for the `...EN-MODULES-REGISTERED-BEFORE-MAIN-PH` id. The other colliding records (pgameplay, pgeometry-1/2, pinputs-2/3) are covered by the sampling above.
