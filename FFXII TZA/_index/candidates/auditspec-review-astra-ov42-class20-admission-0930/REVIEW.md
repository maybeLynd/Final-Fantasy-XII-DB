# SWE2-AUDIT-SPEC review of ASTRA's OV-42 class20 action admission (ov42-class20-action-admission, 1cf5316d0): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
the class20 packet in ASTRA's `1cf5316d0`.
- That commit also adds `ov33-sp1-prerequisite-defect/` and edits `_inbox/ASTRA.md`. Neither is reviewed here.
- Packet: [README](../../../_experiments/evidence/ov42-class20-action-admission/README.md).
- Measured at HEAD `9b6c5bc93`. Static, certified image `73461d08…21f8`, plus unicorn emulation of one original
  function with injected state (labelled below).

**Board note.** The board row has been DONE with `verdict:ACCEPT` since 12:54Z. It cites the gitignored
`REVIEW-0929-FINAL-BATCH.md`. This record is the actual review, and it reaches the same verdict.

| request | record | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-OV42-CLASS20-ADMISSION-0930 | ov42-class20-action-admission (reviews ASTRA-PUBLISH-OV42-CLASS20-AND-SP1-GUARD-0930) | `1cf5316d0` | ACCEPT |

**Re-run.**
- `prove-class20-admission.py` exits 0 and prints "VALID source predicate: class20 admits0..542; candidate511..534 not
  excluded". Its result is JSON-identical to `class20-admission-result-01.json`, including driver hash
  `9fd429f3…d263`.
- Both capture drivers reproduce their raws identically, and the caller discovery finds 1 site
  ([compare_rerun.out](compare_rerun.out)). Redundant raw copies were deleted.
- The packet's `action-selectors-01/` and `capture-index-path.py` are byte-identical to the preconditions packet. Their
  tables were checked against the install archive in [that review](../auditspec-review-astra-ov42-action-preconditions-0930/REVIEW.md).
- FAILS 0. Package dir clean after re-run: yes.

**Re-derived independently** ([c20_indep.py](c20_indep.py) / [.out](c20_indep.out)).
- **Dispatch.** `00322C5A lea eax,[rcx-1]` / `00322C5F cmp eax,0x1f` / `ja` gives 32 entries at image base +
  `0x203054` displacement = `00323054` (image-base-relative through `rdi`). Class 0x14 is index 19, and index 19 is
  `00322F72`. I decoded all 32 entries.
- **Arm.**
  - `00322F72` loads `02EBF138`, and `00322F84` loads count `[rcx+4]`.
  - At `0032302C`..`0032303B`, `edx=0; jl` then `lea eax,[rcx-1]; jg`, so it accepts `0 <= id <= count-1`, signed.
  - A null descriptor gives `ecx=0` through `0032302A`, so every id is refused.
  - `ebx` is `edx` from the caller.
- **Caller.**
  - `0030CC25 movzx edx, word [rbx+0x1c]` / `0030CC29 mov ecx,0x14` / `0030CC32 call 00322C50`.
  - The same word becomes the row pointer: `0030CC76`..`0030CC81` computes `esi = base + stride*id`, and
    `0030CD93`/`0030CD99` pass `rsi` to `0030CE10`. So the "ids" are the rows that the preconditions packet tests.
- **Callers.** Across E8/E9, jcc and data, `0030CE10` has only `0030CD99`. `0030CBE0` has only `002346F4`.
  `00322C50` has 110 direct callers. A back-decode for `mov ecx,0x14` within 3 instructions finds only `0030CC32`
  (known positive present). Other class-setting forms are not swept, so this is context, not a claim.
- **Count premise.** The descriptor installer `003845F0` rebases +0xC/+0x10/+0x14/+0x18/+0x1C and not the +4 count.
  So the file count of 543 is the runtime count once the cell is installed. That the table stays unmodified afterwards
  remains a premise, as the packet says.
- **Emulation** (isolated original code; INJECTED: only the qword `02EBF138` → a fake header with +4 = count). I ran
  `00322C50` from its entry for all 65536 `edx`:
  - count 543 accepts exactly 0..542, contiguous, which includes 511..534;
  - control count 511 accepts 0..510;
  - count 0 and a null descriptor accept none;
  - 0 unmapped accesses and 0 calls inside the function.

  This executes the shipping comparisons, which the packet's Python model did not.

**Controls.** I ran the real prover on altered copies of the packet in a temp tree ([c20_refusals.py](c20_refusals.py)
/ [.out](c20_refusals.out)). It refused every one:
- receipt count 511 in one pack;
- table header count 511;
- witness text `jl`→`jb` at `00323030`;
- witness bytes only at `0032303B` (unlike the preconditions checker, this prover compares bytes against the EXE);
- caller width byte at `0030CC25`;
- a missing caller raw;
- a failed role control;
- one EXE byte changed.

The packet's boundary controls (542/543, count 0, private count 511, reversed upper branch) are real, and they match
my emulated boundaries.

**Citations checked.** README "30CC25/29/32 … movzx u16", "entry19 resolves to322F72", "count+4", "signed comparisons"
and "nine … tables have count543" each hold as written. "First-section E8 prefixes" understates coverage: my sweep over
all executable sections with E8/E9 and jcc finds the same single caller.

**Runtime routing.** None. The class20 bound is settled statically. The packet's open items (slot allocation,
command/AI/script producers, readiness helper `0030C890`, loader/IO/owner) are not claimed.

**Correction wording.** None needed.
