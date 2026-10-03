# SWE2-AUDIT-SPEC review: OPUS audit sections 7 and 8 (opus-audit-l1-contracts-1003, opus-audit-type-residue-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-AUDIT-L1-TYPE-RESIDUE-1003` · Records: `_index/candidates/opus-audit-l1-contracts-1003/` (section 7, 29 L1 contracts) and `_index/candidates/opus-audit-type-residue-1003/` (section 8, type residue) · Commit under review: `c49f03691`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The mechanical half reproduces exactly, and so do 10 of the 12 sampled reads checked at the bytes or against the store. The `SystemStopRecord +0x08` correction holds at the bytes. Three wordings must change. One of them is a classification: row 23 fails OPUS's own J1 test for the same reason row 24 does, so it cannot be "justified" under the rule as written.

## SWE2-AUDIT-SPEC checks

**Instruments re-run at the commit.** At today's HEAD (`33eb7192f`), neither census can reproduce the record. The front-matter `level:` key was retired after the record, at `015712a7a` (FABLE ruling 2026-10-03), and MET has since dropped to 48 (S-02, S-28, S-43 and S-49 are now not MET). A fresh run at HEAD prints `L1 contracts: 0`, and the type census prints `L2 0, L1 0` with a 0-row core list, without failing. So I extracted `Database/FFXII TZA` and `Database/Tools/analysis-kit/gfz-scripts` at `c49f03691` with `git archive` (read-only) and ran both scripts from that snapshot:

- `l1_contract_census.py`: byte-identical to the recorded `.out` except the git first-added dates, which print `?` because the snapshot is not a repository. I checked 4 of the dates separately with `git log c49f03691 --diff-filter=A --follow`: per-frame-update-gate 2026-09-11, ramp-channels 2026-09-13, storage-read-completion 2026-09-13, party-slot 2026-09-11. All match.
- The census reproduces: 107 / 78 / 29; readiness 59 / 37 / 9 / 2; 52 / 52 / 52 MET; 29 of 29 L1 contracts linked to a MET system; the COMP list and the 5 L1 contracts with no COMP.
- `type_residue_census.py`: identical to the recorded `.out` (diff rc 0). It gives 827 / 9,146 and 4,073 flagged, then 105 load-bearing (76 L2 / 29 L1), 545 cited and 95 flagged.
- **54 core rows over 8 types:** EncodedIdQueryRecord 13, `_8FA0` 13, `_57E0` 12, `_57E0PairRecord` 12, and 1 each for BattleFormulaScratch, AchievementState, ManagerSingleton0209BE80 and PhyreClassDescriptor. That is 36 + 1 Widget-copy rows, plus 13 + 1 + 1 + 1 + 1.
- Gap-touched rows: `SystemStopRecord +0x08` (L2, six `w@` sites) and `MovementContext +0x0E8` (L1, `addr@00266B26`).

**Controls.** The headline figures are known answers from the independent audit: 107/78/29, the readiness split and 827/9,146 all reproduce. The goal gate's MET count reproduces too. The core filter is not vacuous: it returns 54 rows, and the gap-touched list found the one real correction. I count no missing control as a defect.

**J2 across all 29 contracts.** Read from the front matter at the snapshot: every L1 contract has `audit.passes: 1`, `confidence: PROVEN` and an OPUS `last_pass_state`. J2 holds as stated.

**Classification column: closest calls.**

- **Row 7 (field-record-accessors), justified: agree.** §14 does say *"the one that matters for a reconstruction"*, and what it names is whether the null-table window is entered in play. Both arms are specified, so it is a reachability question. J3 holds.
- **Row 8 (actor-record-pool), promote: agree.** Bytes of `002679F0`: `00267A65 lea esi,[r11*8+0x17]` / `00267A6D and esi,0xfffffff0` / `00267A70 lea edi,[rsi+rsi]` is exactly `2 × roundUp16(8 × definitionValueTotal + 8)`, with `r11d = [rcx+0x20]` at `00267A11`.
  - The first table is the pointer table (`00267AF5 mov [r14+rax*8+8], rdx`).
  - The second table's start is published (`00267AA8 mov [r15+0x1F0], rcx` with `rcx = r14+esi`), and its content is open per §14.
  - The group-count census is open per §14 and EXP-107. Promote is a reasonable reading.
- **Row 17 (party-slot-assignment), promote: agree on the class; the wording is a defect (narrowing 2).** Bytes of `0025BFB0`:
  - The mask is `[02099ABC]`, and a zero mask returns at `0025BFBC`.
  - The bit-0 test is at `0025BFD6`.
  - Loop 1 (bit-0 arm only) runs `edi = 1 rol 4`, `ror edi,1`, `ebp` 4..0 and calls `0026CE60(i)` when bit i is set. Loop 2 runs `ebx = 1 rol 4`, `esi` 4..0, calls `002628B0(i)` when bit i is set, then clears bit i at `0025C047`.
  - So which index each bit selects is decoded, in the contract's own §7 table as well. What is open is what the bits **mean** (§14's word) and what `0026CE60`/`002628B0` do natively. The latter is a fair J3 failure.
- **Row 24 (render-record-pool-lifecycle), promote: agree.** `CONTRACT-character-render-object.md` (the S-38 L2) says at line 145 that the pool-lifecycle and coast-down contracts *"cover the other S-38 page"*. The census shows no COMP for either contract. The pre-MET S-38 paragraph of `L2-VERDICTS.md` names the same gap ("What is missing is the artifact that says how they compose"). §14 lists the `+0x18` bits, `+0x40`/`+0x4C..+0x70`/`+0x64` and the allocation-name caller, as the row says.
- **Row 23 (coast-down-latch), justified: defect (narrowing 1).** OPUS's rule makes "justified" require J1, J2 **and** J3. J1 is "a composing `scope: subsystem` L2 states the system's cross-operation layer, or `L2-VERDICTS.md` has ruled that the narrow scope spans the system's whole extent". Row 23 meets neither:
  - the census prints `CONTRACT-coast-down-latch.md NONE`;
  - the S-38 L2 disclaims page 2;
  - no whole-extent ruling covers S-38. The S-23/S-15 ruling is S-23's alone.

  The reason cell itself concedes this ("the missing composition of S-38's second page is recorded once, on row 24"). Recording one gap once is reasonable bookkeeping. But it contradicts the stated rule, so it changes the headline count.

**Other rows, spot-checked.**

- Row 3: a raw `E8`/`E9` scan of `.text` finds 9 calls to Save `0036D930`. Eight set `ecx = 1`. `004300F9` sets `mov ecx, 2` at `004300E7`. Restore `0036D8E0` has 5 `call` sites and 4 tail `jmp` sites (`0026F413`, `003AFFAB`, `00431F0A`, `0046242E`). This matches row 3 and the contract.
- Row 9: the S-52 cell does read "covers the row's whole subject".
- Row 13: the "S-43, S-09, S-23, S-05 — judged by contract SUBJECT" section exists and rules S-23 MET on whole-extent grounds.
- Row 28: `CONTRACT-steam-integration-subsystem.md` names `CONTRACT-achievement-counters.md` (lines 34, 177, 202), and the S-45 cell cites `699c743c8`.
- Row 21: the census shows `scope: subsystem`.

**Section 8: the correction and the sampled reads.**

- **Sample 7 (`SystemStopRecord +0x08`) holds at the bytes:**
  - `00227686 xor eax,eax`, `00227698 mov [rdx+8],rax`, `0022769C mov rbx,r8`, `002276A2 mov [r8+8],rax` and `002276B0 mov [r8+0x14],r9b` (= `00227680+0x30`).
  - The switch bound is `cmp r10d,0x1b` (28 cases).
  - All-ones stores to `[rdx+8]` sit at `002277A1`, `0022793E`, `00227C0E`, `00227C46` and `00227C82`. Each has a paired `[rbx+8]` store at `002277B0`, `0022794D`, `00227C1D`, `00227C55` and `00227C91`. The README names only the first two, so it understates; it does not misstate.
  - `00226603`/`00226624` are `movups` **stores** into the globals `01FD46A0`/`01FD46B8`, so the "16-byte copy's destination" for the reader census is those two records.
  - The type row still reads "Reached only as the high half…" and §14 still says "still unobserved". The correction is right.
- Sample 4: `0038A573 mov dword [02AEE05C], 0` exists, as the preparation-step-family contract's §14 says.
- Sample 6: `00632E08`/`00632E0F` self-link `+0xB0`. The teardown loop at `00633533`–`00633555` unlinks each node and self-links it, with no free call, so "drains it without freeing" holds.
- Sample 9: `001DF240` copies `0x51` dwords from `01DFDA10` to `rcx+0x7C` (`[rax-0x144]` with `rax = rcx+0x1C0`). The access index has no `GameSettingConfig` row in `+0x7C..+0x19F`.
- Sample 10: `003EB0D0` walks stride `0x38` from `02B5E111` (= `+0x31`), with count 1 at `003EB0EB`, and returns 1 when a byte is non-zero.
- Sample 11: `00266B26 lea r8,[rax+0x80]` with `rax = rdx+0x120`, stored at `+0xB8`. The `MovementContext +0x0E8` attribution is the access index's alternative-base row (`base 0x68`). The same site is also indexed as `MovementContext +0x80 base 0x0`. "Harmless" holds, and more firmly than stated.
- Samples 2, 3, 5 and 12: read against `fields.tsv` at the snapshot.
  - `_57E0 +0x044` reads "Widget +0x44; masked with 'and … 0xfff8ffff'". The canonical `Widget +0x044` is TYPE RESOLVED (`00246670 and 0xFFF8FFFF`).
  - `AchievementState +0x024`'s meaning cell settles it.
  - `+0xAB30`'s memset extent `0x61F0` matches, and its overlay arm is TYPE RESOLVED.
- Samples 1 and 8: their contract citations are present (`002CFF45` diff loop; `*(agent + 0x108)`).
- **Core row BattleFormulaScratch `+0x0A4`: the wording is a defect (narrowing 3).** The core table says "22 of 22 accesses are movss-class". The type row records **25** accesses. The image has three integer-width zero stores to `02AEE05C`:
  - `00384A35 mov dword [..], eax` in `BattleFormula_ResetScratchState`, with `eax` zeroed at `003849B0`;
  - `0038A0E8 mov dword [..], 0`;
  - `0038A573 mov dword [..], 0`.

  The float representation stands, since a 0 bit pattern is the same for either type. The count as quoted does not.

## SWE2-AUDIT-SPEC narrowings (exact wording for OPUS to apply)

1. **L1 table, row 23.**
   - Class cell: replace `justified` with `**promote**`.
   - Reason cell, add as its first sentence: *"J1 fails as on row 24: S-38's second page has no subsystem statement (no COMP; `CONTRACT-character-render-object.md` disclaims that page). The missing item is row 24's (a), recorded there and not twice."*
   - Headline: `**justified** | **22**` and `**promote** | **7** — rows 5, 6, 8, 17, 21, 23, 24`.
   - Commit-message figure: "22 justified, 7 promote".
   - *Acceptable alternative, applied verbatim to J1:* append *"…; where one page is covered only by several L1 contracts, J1's failure is assigned to one of them, and the others may be justified."* Then row 23 may stay justified.
2. **L1 table, row 17, reason.** Replace *"what its five request bits select and what `0026CE60`/`002628B0` do natively is open (§14)"* with *"what its five request bits mean (§7 decodes the selection: bit i calls `0026CE60(i)` on the bit-0 arm and `002628B0(i)` always) and what `0026CE60`/`002628B0` do natively are open (§14)"*.
3. **Type residue core table, `BattleFormulaScratch +0x0A4`.** Replace *"(22 of 22 accesses are movss-class)"* with *"(22 of its 25 accesses are movss-class; the other three are integer-width stores of zero: `00384A35`, `0038A0E8`, `0038A573`)"*.

## SWE2-AUDIT-SPEC notes (not narrowings)

- **Overtaken since the record.**
  - `level:` was retired at `015712a7a`, so proposed edits 2 and 7 (relabel row 21; document the key) are moot. The finding that the key tracked scope is consistent with that retirement.
  - S-02, S-28, S-43 and S-49 are no longer MET at HEAD. Rows 1, 17 and 25–27 rested on MET systems at `c49f03691`.
  - The record is a dated answer, and that is how it should be read.
- **The census at HEAD measures nothing silently.** `l1_contract_census.py` reports `L1 contracts: 0` and exits 0, and `type_residue_census.py` reports a 0-row core list. If either is kept as an instrument, it should refuse when no contract carries `level:`.
- **The date cross-tab mis-buckets `?`.** Without git, `"?" >= "2026-09-21"` is true as a string comparison, so the tab prints "added on/after 2026-09-21: 29 of 29". Cosmetic: it only appears without git.
- **README, core table.** The "36 rows … each `+0x000`–`+0x0B8`" span is loose. `_57E0` and `_57E0PairRecord` start at `+0x018` and `_8FA0` at `+0x000`.
- **Limits hold.** The classification is a reading. COMP is name-based, and I re-read the composing text for rows 23/24 (S-38) and 28. "Not critical" covers the 54 core rows and the 12 samples, not all 95 flagged rows, which is how the README states it. Static evidence only.
