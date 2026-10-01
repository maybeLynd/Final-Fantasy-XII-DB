# SWE2-AUDIT-SPEC non-author acceptance of SECTION-02, the resource request queue production: ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30).

- **Reviewed:** the SECTION-02 production in `_experiments/evidence/continuation-section02-resource-queue/`
  ([REVIEW](../../../_experiments/evidence/continuation-section02-resource-queue/REVIEW.md), `run_review.py`,
  `native_controls.c`, `original_body_manifest.json`, `original_disassembly.txt`, `results/`).
- **Also read:** its handoff entry `_index/_inbox/EXTERNAL-CONTINUATION.md` SECTION-02, and its canonical consumers
  `the-resource-request-queue.md` and `CONTRACT-resource-request-queue.md`.
- **Measured at:** HEAD `17a959c94`. None of these files changed through `8c853d5d8`.
- **Evidence classes:** static reading of the certified image, and isolated original-code execution, both native Linux
  and Unicorn. Nothing live.

| request | record | commit | verdict |
|---|---|---|---|
| SWE2CONTRACT-REQ-AUDITSPEC-SECTION02-ACCEPT-0930 | continuation-section02-resource-queue (SECTION-02) | `b6c9a74a8` | ACCEPT |

**Independence.**
- **The package.** The production is the external continuation's (2026-09-22). It was committed in `b6c9a74a8`, the
  ORACLE EXP package publish, on 2026-09-25. It is not FABLE-authored, and I did not author it.
- **Dependencies that are not independent.**
  - OPUS's falsification pass (Q1–Q5) was accepted in `OPUS-REQ-AUDITSPEC-REVIEW-BATCH10-0930` by this lane on
    2026-09-30T12:45Z. That is FABLE-session-window work.
  - SWE2-CONTRACT's DD batch 6 is reviewed separately in
    [auditspec-review-ddres-b6-0930](../auditspec-review-ddres-b6-0930/REVIEW.md).
  - This verdict rests on neither of them. It rests on the re-execution below.

**Re-run.**
- **Windows.**
  - `run_review.py` refuses by design, with "Native fixture requires Linux x86-64"
    ([rerun_run_review_windows.out](rerun_run_review_windows.out)). It creates no output directory.
  - `verify_overlay.py --target <FFXII TZA>` is read-only and exits 1
    ([rerun_verify_overlay_windows.out](rerun_verify_overlay_windows.out)). 24 files report `already_applied` and 6
    report `conflict`: the contract, the mechanism page, EXP-146, EXTERNAL-CONTINUATION, `fields.tsv` and `types.tsv`.
    Those six are the canonical files edited after the overlay, as expected.
- **Linux, the package's own gate, reproduced through WSL** (Ubuntu 22.04, Python 3.10.12, gcc 11.4.0, kernel 6.18
  x86-64; [rerun_run_review_wsl.out](rerun_run_review_wsl.out), outputs in [wsl_rerun/](wsl_rerun/)). Exit 0.
  - 22 bodies verified, 72/72 native checks with 0 failures, and the repeat identical.
  - All 6 mutants were detected, each at its intended assertion.
  - 22 retained branches pass. There are 4 corrupted-record controls and the 2 known vacuous loader branches.
  - The inputs are unchanged.
  - All 12 result files the runner writes are **byte-identical** to the committed `results/` (ignoring CR).
  - The committed `overlay_preflight_tests.json` and `section_validation.json` are not produced by `run_review.py`, and
    I did not reproduce them.
- **Package dir clean.** `git status --porcelain` on the package dir is empty after all runs.

**Re-derived independently.**
- **Original bodies, byte-verified with my own loader** ([s02_bytes.py](s02_bytes.py) / [.out](s02_bytes.out)).
  - File offsets were computed from the section table, not taken from the manifest.
  - All 22 bodies match (2,472 bytes), and so do the 24-byte dispatch table `0032E2D0`: arms `0032E0BD`, `0032E149`,
    `0032E163` ×2, `0032E1AB` ×2.
  - All 670 retained disassembly lines match the image bytes, and my capstone text is identical.
  - Every extent agrees with `.pdata` or ends at a `ret`/`jmp` before `int3` padding. The one exception is `0032E070`,
    whose `.pdata` range runs to `0032E2E7` because it includes the jump table the manifest pins separately.
  - Control: a range shifted by one byte does not match.
  - Mutant targets are the named instructions ([mutant_targets.out](mutant_targets.out)): `0032E9B5` is the freeHead
    store, `0032E922` `inc edx`, `0032E496` the displacement of `mov [rax+0x10],r8d`, `0032ECC7` the displacement of
    `mov dword [rcx+0x64],-1`, `0032E8FC` `and edx,0x7ff`, and `0032E5B7` the `jne` after the generation compare.
- **31 of the 72 native checks, re-executed on Windows by my own harness** ([s02_emu.py](s02_emu.py) /
  [.out](s02_emu.out)).
  - The harness is Unicorn 2.1.4 with the image mapped at its base and every section's raw bytes loaded. It installs no
    bridges and no stubs, and execution is confined to the manifest's original bodies. `CHECKS 33 FAILS 0`: the 31
    checks plus 2 controls.
  - Constructor: all 64 links, indices and ids, with the A5 bytes preserved.
  - Take and recycle: freeHead moves, tail and head insert, the three retire cases, the splice keeps the payload, and
    the 64th take exhausts the list.
  - Request stamps. The descriptor's `+0x20` part callback is ignored (slot `+0x50` = 0).
  - All ten offset truncations: `0x801` → `0x800`, `-0x801` → `-0x800`, `INT32_MIN` unchanged, `INT32_MAX` →
    `0x7FFFF800`.
  - Ids `0x40` / `0x81` / `0xC0`, the wrap at `0xFFFFFF` (id `0x3FFFFFC0`, counter 1), the signed compare
    (`0x7FFFFFFF` → id `0xFFFFFFC0`), and a planted zero id that still takes a slot.
  - Cancel rejects a stale generation and the sentinel ids. A cancel with no callback keeps the byte count.
  - A null part callback returns 1.
  - **Controls.** A round-up expectation is rejected on every offset where it differs. A drain that must leave the
    allow-list (`0032E520(0)`) is caught at the service gate `003EADD0`. So "no stub" is enforced, not assumed.
- **The remaining claims, read statically** in [module_listing.txt](../auditspec-review-ddres-b6-0930/module_listing.txt),
  a full linear decode of `0032E000`–`0032ED80):
  - **Head-driven pump.** Every arm returns to `jmp 0032E090`, which reloads `[022C51C0]`. The busy gate
    (`0032E0C4`) and the in-flight test (`0032E16A`) exit to the footer.
  - **Footer.** It is `0046DD50`, `0016D6A0`, `003E9780`, `0016D6A0`, `0036FD50`, then `003BB790` when that returns
    nonzero. An empty pending list adds `003EADD0` (`0032E29B`). Nothing there is a shutdown.
  - **Part results.**
    - `0032E208` stores the result at `+0x23`, and anything other than 1 exits.
    - On the next pass, only 2 takes the re-probe branch: `cmp byte [rbx+0x23],2` / `je 0032E24D`.
    - 3 falls to `0032E1ED`, which subtracts `+0x28` from `+0x34` again.
    - An out-of-range result calls `008620C0(0)`.
  - **State 2.** `0032E149` / `0032E14E` call `0035E810` twice. Only the second result is added to `[rbx]` and stored
    at `+8`.
  - **Signed path.** `movsxd rcx,[rbx+0x24]` appears at `0032E105`, `0032E357`, `0032E39A` and `0032E5C7`.
  - **Guards.**
    - The error callback runs only when `+0x28 == -1` (`0032E382`).
    - The gated error helper `0032E370` can return the callback pointer in `rax`.
    - Cancel zeroes the count only when `+0x48` is nonnull (`0032E2F6`–`0032E302`).
  - **Free list.** Its empty test is `0032E88D cmp [022C51D0],rbx` with `rbx = 0` (`0032E888`).
  - **Poll and drain.** The poll form (`ecx ≠ 0`) never pumps. The drain form calls `0032E070` first (`0032E563`).
  - **EXP-146 lifecycle.** It retains kind 3 and index 256 after retirement (`retained_review.json`, reproduced).
- **Canonical rows.** All 14 row changes (1 `types.tsv` row, 13 `fields.tsv` rows) are unchanged at git HEAD
  ([s02_rows_at_head.py](s02_rows_at_head.py) / [.out](s02_rows_at_head.out)).

**Verdict per section** (the shape of S69 in `auditspec-ratify-legacy-verdicts-0929/source-REVIEW-0929-FINAL-BATCH.md`):

```json
{
  "task": "SWE2CONTRACT-REQ-AUDITSPEC-SECTION02-ACCEPT-0930",
  "reviewer": "SWE2-AUDIT-SPEC",
  "method": "own byte verification of all 22 retained bodies + table + 670 retained instruction lines vs certified image 73461d08; the package's Linux fixture re-executed under WSL (72/72, outputs byte-identical); 31 of the 72 checks re-executed independently in Unicorn on Windows with no stubs; remaining claims read statically",
  "reviews": {
    "Q1 freeHead (022C51D0 moves; 0032E88D is an empty-list test)": "ACCEPT",
    "Q2 links +0x10 next / +0x18 previous; selective init and recycle": "ACCEPT",
    "Q3 head-driven, multi-request pump (64 in one call; 65th self-pumps)": "ACCEPT",
    "Q4 common service footer, not shutdown": "ACCEPT",
    "Q5 descriptor part callback not copied (0032E959 clears slot +0x50)": "ACCEPT",
    "Q6 part results 2 / 3 distinct; callback-presence guards; gated error helper return": "ACCEPT",
    "Q7 generation fencing, 32-bit id, signed counter wrap, offset truncation toward zero": "ACCEPT",
    "Q8 state 2 adds the second counter reading, no subtraction": "ACCEPT",
    "Q9 two historical EXP-146 branches are vacuous": "ACCEPT"
  },
  "verdict": "ACCEPT",
  "limitations": [
    "isolated original code only: service calls, readers, pacer and predicates are scripted boundaries in the package's host; my Unicorn run stops at them",
    "mutant runs stop at the first failing check, so 'fails its intended assertion' means the first failure is the intended one",
    "no live-game, real-I/O, timing or installed-game reachability claim is made or accepted",
    "acceptance covers SECTION-02's claims; the page's other bounded items (deeper services, path/callback lifetime, authored reachability) are not accepted by this"
  ]
}
```

**Runtime routing.** Nothing is routed. Static reading and isolated execution settle every SECTION-02 claim. What
remains open is live-only by its nature: real I/O completion, timing and scheduler behaviour. The package names it.

**Correction wording.** None is needed for SECTION-02 itself. Consumer items for the owners:
1. **`CONTRACT-resource-request-queue.md` §13.** The adjudication paragraph still says "and the pump drains to teardown,
   not idle". SECTION-02 Q4 retired "teardown". Change it to "and the pump drains to the common service footer, not
   idle". The contract is ` M` with a peer's edits, so this goes to OPUS.
2. **Contract §14 and the front matter.** "Formal peer review of SECTION-02" and `production_review.status: …formal
   peer acceptance pending` can now cite this record. On the mechanism page, the front-matter status sentence
   "SECTION-02 peer acceptance is a class-2 process item carried by …" can say "accepted
   (`SWE2CONTRACT-REQ-AUDITSPEC-SECTION02-ACCEPT-0930`)". That clears OPUS's stated reason for keeping the page PARTIAL
   ([opus-dd-restatus-02-0930/README.md](../opus-dd-restatus-02-0930/README.md)).
