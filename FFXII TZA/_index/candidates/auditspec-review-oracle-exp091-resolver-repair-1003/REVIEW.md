# SWE2-AUDIT-SPEC review: SWE2-ORACLE's EXP-091 resolver-base repair and action-row control (exp091-resolver-base-repair-1003)

Reviewer: FABLE (non-author, independent of the SWE2 stand-in session; on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-EXP091-RESOLVER-REPAIR-1003` · reviewed at HEAD `a1670ab28`
Package: `_experiments/evidence/exp091-resolver-base-repair-1003/` (publisher commit `78271194d`, unchanged since: `git diff --stat 78271194d HEAD` over the folder and over `commit-callees-exec/` is empty). Image pin `73461d08…21f8`, base `0x120000`. Method B (original code under Unicorn, hand-built world). Nothing here is a live observation or an ASTRA sample.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

- **Accepted as stated:**
  - The repair is correct: `G_IMGB = 0x1F83530` is the cell `0020E602` reads.
  - The diff against the archived original is exactly the three disclosed changes.
  - Both positives execute `0020E600` twice. Both read action-row byte 6 at `0x403C0086`, holding 1 and 0, and return 1 and 0.
  - Both old-base negatives are refused by the address/return-trace check. Both read image byte `0x89` at `0x3C0086` without a fault.
  - `canc-fixup` passes with no `imgadd` event.
  - The census holds: no retained case or mutant executes `0020E600` or reads either base cell.
  - Every bit-22, copy, cancel, commit and mutant result of EXP-091 is unaffected.
- **Narrowed (wording only, no result changes):**
  - "Zero old `imgadd`" is a **coverage gap of the retained 87 cases + 10 mutants**. It does not invalidate any retained case, and it does not show that `0020E600` or the action-row arm is unreachable.
  - The six hooked zero-entry bodies are **not executed by the retained fixtures**. That does not mean "never executed", "universally unexecuted" or "false".
  - The package's own consumer item 2 ("This is **false** for `0x20E600`, and … also for six more listed VAs") over-reaches. `bodies.json` predates the retained case set, and the README itself says it "may come from a different case set". The supportable form is "unsupported by the retained fixtures".
  - The exact replacement sentences are in the consumer section below.
- One finding the package left open is closed by this review. The two unhooked listed VAs, `002FD880` and `002FD420`, **do** execute in the retained fixtures (span census below).

## SWE2-AUDIT-SPEC identity and integrity

- `Database/Tools/work/exe/FFXII_TZA.exe` (rvlib) and the harness's own `D:\SteamLibrary\…\FFXII_TZA.exe` both pass the sha256 assert `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
- `check_repaired.py` sha256 is `be27a7fe…a813be`. The working tree, `78271194d` and the reviewer's run copy are identical.
- The archived original `commit-callees-exec/check.py` sha256 is `3a8028419796303e1c9cc27d15440b786eddea5a0be54009600958917be64068`, and `result.json` is `e74106aa…21f5ea`. Both match the README's pins. Neither file has changed since `f7bbac4ef`.
- The consumer pages named below have not changed since `78271194d`. Line numbers are current at `a1670ab28`.
- Tools: Python 3.14.6, unicorn 2.1.4, capstone 5.0.7. No live process, board write, team.py or publish was run. The only file written in the repo is this REVIEW.md, plus the one line appended to `fable_verdicts5.tsv`.

## SWE2-AUDIT-SPEC 1. the resolver cell (rvlib, not the producer's disr.py)

`rv_disasm.py` decodes the bodies with `rvlib` (the reviewer's own PE and capstone reader) and resolves the rip-relative targets:

```
0020E600  8bc1                     mov eax, ecx
0020E602  480305274fd701           add rax, qword ptr [rip + 0x1d74f27]   ; rip-> 01F83530
0020E609  c3                       ret
```

- `0x20E609 + 0x1D74F27 = 0x1F83530`, so `G_IMGB = 0x1F83530` is exact.
- The old cell `0x1F85D30` is 0x2800 higher.
- An image-wide decoded scan of every `.text` disp32 finds these rip-relative references:
  - `01F83530`: `0020E602` (`0020E603` is a misaligned decode of the same bytes) and `0020E620` (`sub ecx, [01F83530]`, the inverse helper).
  - `01F85D30`: none.
- The producer's census (`census_imgadd.py`) uses a `UC_HOOK_MEM_READ` on both cells. That also covers `0020E620` and any image-base-relative access, and it sees no read of either cell in any retained fixture.

`0030C0E0` (pdata `0030C0E0-0030C202`): the decoded path the control relies on.

```
0030C0F1  call 0x236850            ; roster count
0030C105  call 0x236820            ; unit i
0030C116  test byte ptr [rax], 0x10 / je
0030C12F  mov eax,[rcx+0x64] / or eax,[rcx+0x3c] / test eax,0x80000003 / je 0x30c149   (else 00377C20)
0030C149  cmp byte ptr [rbx + 0x6b6], 0 / jne
0030C152  mov ecx, dword ptr [rbx + 0x710] / call 0x31b7e0      ; handle -> target unit
0030C162  test byte ptr [rax], 0x10 / je ; 0030C167 target stats [rax+0x698]
0030C173  movzx eax, byte ptr [rcx + 5] / test / jne 0x30c1cc   ; party kind must be 0
0030C17B  movzx ebx, word ptr [rbx + 0x714] / cmp bx, si(0x21e) / ja
0030C187  mov rax, [rip+…] ; rip-> 02EBF138 / test / je 0x30c1c4
0030C193  mov ecx, [rax+0xc] / 0030C196 call 0x20e600 / test rax,rax / je 0x30c1c4
0030C1A7  mov ecx, [rax+0xc] / 0030C1AA call 0x20e600
0030C1B6  movzx edx, word [rcx+8] / movzx ecx, bx / imul ecx, edx / add ecx, eax   ; 32-bit row
0030C1C6  cmp byte ptr [rcx + 6], 0 / jne 0x30c1ed (ret 1) ; else loop, 0030C1DB ret 0
```

- This agrees with the README's description: two calls to `0020E600`, a 32-bit row, byte 6 against 0, and the party-kind gate at `0030C179`.

### SWE2-AUDIT-SPEC diff against the archived original (`diff commit-callees-exec/check.py check_repaired.py`, 200 lines)

Every hunk falls in one of the three disclosed changes. No case, mutant, fixture default or check of the 87 + 10 was altered.

1. **Base cell.**
   - Header comment L1 is extended to describe the copy.
   - The fixture comment at L92 changes `0x1F85D30` to `0x1F83530`.
   - L154: `G_IMGB = 0x1F85D30` becomes `G_IMGB = 0x1F83530`, plus a new constant `G_IMGB_OLD_WRONG = 0x1F85D30` used only by the negatives.
   - L352: `gm.w(G_IMGB, …)` becomes `gm.w(case.get("imgb_addr", G_IMGB), …)`.
2. **New control group.**
   - New constants: `IMGADD_RET = 0x20E609` and `TV_ROW6_CMP = 0x30C1C6`.
   - `World` gets `imgret`/`row6` lists, and two code hooks that are installed only when `rowwatch` is set. One records `rax` at the resolver's `ret`. The other records `rcx+6` and its byte at the `cmp`.
   - New cases `tv-row6-set`/`tv-row6-zero` with `tv_fixture`/`tv_check`. `BASE_CONTROLS` holds the two old-base variants.
   - New functions: `run_base_control` (detected = the probe's check refused the run, or the run faulted) and `detail()`.
   - `run_case` copies `imgret`/`row6` into the snapshot when `rowwatch` is set.
3. **CLI and output.**
   - `main()` runs the base controls, adds `base_controls_detected/total`, and writes `result_repaired.json`, not `result.json`. Its success condition also requires all base controls detected.
   - New `main_only` and `--only` dispatch, writing `result_repaired_only.json`.

- **Side effect checked:** the base move applies to every old fixture. It cannot change an old trace, because no old fixture reads either cell. The producer's census shows this, my rerun of it reproduces it, and my span census of the **archived** harness agrees (section 3).

## SWE2-AUDIT-SPEC 2. reproduction of the five selected cases

The script was run from the repo root with the system python. To avoid overwriting the published `result_repaired_only.json`, which `--only` writes next to `__file__`, I ran a byte-identical copy (sha `be27a7fe…`) from the reviewer scratchpad:

```
cd C:/Users/Kristian/source/repos/XIIOnline
python "$SCRATCH/exp091rev/run/check_repaired.py" --only tv-row6-set,tv-row6-zero,neg-oldbase-tv-row6-set,neg-oldbase-tv-row6-zero,canc-fixup
PASS tv-row6-set
    detail tv-row6-set: ret=0x1 imgadd=2 ['rcx=3c0000', 'rcx=3c0000'] imgret=['0x403c0000', '0x403c0000'] row6=[['0x403c0086', '01']] faults=[]
PASS tv-row6-zero
    detail tv-row6-zero: ret=0x0 imgadd=2 ['rcx=3c0000', 'rcx=3c0000'] imgret=['0x403c0000', '0x403c0000'] row6=[['0x403c0086', '00']] faults=[]
PASS neg-oldbase-tv-row6-set (old-base run refused by the positive check)
    detail neg-oldbase-tv-row6-set: ret=0x1 imgadd=2 ['rcx=3c0000', 'rcx=3c0000'] imgret=['0x3c0000', '0x3c0000'] row6=[['0x3c0086', '89']] faults=[]
PASS neg-oldbase-tv-row6-zero (old-base run refused by the positive check)
    detail neg-oldbase-tv-row6-zero: ret=0x1 imgadd=2 ['rcx=3c0000', 'rcx=3c0000'] imgret=['0x3c0000', '0x3c0000'] row6=[['0x3c0086', '89']] faults=[]
PASS canc-fixup
    detail canc-fixup: ret=0x40100290 imgadd=0 [] imgret=None row6=None faults=[]
5/5 selected
exit=0
```

- The output is identical to the retained `run_repaired.out`, apart from its `#` header lines. That header records HEAD `45ce9d74e`, which is the producer's terminal record.
- The written `result_repaired_only.json` is parse-equal to the retained one (`json identical: True`).
- **Positives:** each executes `0020E600` twice (`0030C196`, `0030C1AA`), with `rcx=0x3C0000` and return `0x403C0000`. Each tests byte 6 at `0x403C0086`, which holds `01` in -set and `00` in -zero, and returns 1 and 0 respectively. This meets the request.
- **`canc-fixup`:** PASS, `imgadd=0`, no faults.
  - It enters `0030C0E0` once.
  - The deepest instruction it executes before the loop tail is `0030C179` (`jne` taken).
  - It returns 0 through `0030C1DB`.
  - `ret=0x40100290` is the return of the case's entry `00310780`, not of `0030C0E0`.

### SWE2-AUDIT-SPEC the old-base negatives and the return-only ablation (`rv_probe.py` A/B)

Each conjunct of the shipped `tv_check` was evaluated separately on the old-base runs:

```
neg-oldbase-tv-row6-set    ret=0x1 imgret=['0x3c0000', '0x3c0000'] row6=[['0x3c0086', '89']] faults=[]
    conjuncts: {'ret': True, 'imgadd==2&rcx': True, 'imgret': False, 'row6EA+val': False, 'nofault': True}
    return-only check (+nofault) -> PASS (false) ; full shipped check -> refuse ; detected=True
neg-oldbase-tv-row6-zero   ret=0x1 imgret=['0x3c0000', '0x3c0000'] row6=[['0x3c0086', '89']] faults=[]
    conjuncts: {'ret': False, 'imgadd==2&rcx': True, 'imgret': False, 'row6EA+val': False, 'nofault': True}
    return-only check (+nofault) -> refuse ; full shipped check -> refuse ; detected=True
tv-row6-set                (repaired base) conjuncts: all True
tv-row6-zero               (repaired base) conjuncts: all True

== B. old base: does the outcome follow row byte 6?
tv-row6-set    old-base ret=0x1 row6=[['0x3c0086', '89']]
tv-row6-zero   old-base ret=0x1 row6=[['0x3c0086', '89']]
image byte at 0x3C0086 from the PE: 0x89
```

- With the old base, `0020E600` returns the bare RVA `0x3C0000`. That address lies inside the mapped image `0x120000..0x2F800000`, so nothing faults. The code tests the shipped image byte `0x89`, which the PE confirms, and returns 1 **for both fixtures**. The outcome is insensitive to the fixture's row byte.
- A return-only check (with or without the no-fault requirement) **false-PASSes `neg-oldbase-tv-row6-set`**. It happens to refuse `-zero`, only because `0x89 != 0`.
- The shipped detector refuses both through the `imgret` and `row6` effective-address conjuncts, which are False in both runs. That is the defect-sensitive part.
- This matches the README's statement that return-only "would have passed `-set` falsely". The negative is sensitive to the defect it names.

### SWE2-AUDIT-SPEC the fixture binding: roster, handle, kind 0, action row (`rv_probe.py` C, `rv_handle.py`)

Register values at the binding points in `tv-row6-set` (`unit0=40100000`, `unit1=40100F50`, `rec1=400201D0`, `ROWBUF=403C0000`, `COBJ=403A0000`):

```
0030C10D uget ->unit=40100000
0030C15D 0031B7E0 ->target=40100F50          ; +0x710=(2<<16)|1 resolves to unit1
0030C173 target stats (rcx)=400201D0         ; rec1, byte +5 = 0
0030C182 action id bx=10
0030C193 descriptor (rax)=403A0000
0030C1BD stride edx=8
0030C1C6 row (rcx)=403C0080                  ; byte 6 at 403C0086
```

- In `-zero`, the second iteration takes `uget` = unit1, and `0031B7E0` returns 0 there (unit1 `+0x710` = 0). This matches the README.

Each gate was flipped once on the `-set` fixture:

```
baseline                           ret=0x1 imgadd=2 row6=[['0x403c0086', '01']]
target stats+5 = 1 (kind!=0)       ret=0x0 imgadd=0 row6=[]
unit0 +0x6B6 = 1                   ret=0x0 imgadd=0 row6=[]
unit0 [0]&0x10 clear               ret=0x0 imgadd=0 row6=[]
unit0 +0x714 = 0x21F               ret=0x0 imgadd=0 row6=[]
unit0 +0x710 = 0                   ret=0x0 imgadd=0 row6=[]
pgate = 0                          ret=0x0 imgadd=0 row6=[]
ucount = 0                         ret=0x0 imgadd=0 row6=[]
unit0 +0x714 = 0x11 (other row)    ret=0x0 imgadd=2 row6=[['0x403c008e', '00']]
cobj_stride = 0x10                 ret=0x0 imgadd=2 row6=[['0x403c0106', '00']]
unit0 +0x714 = 0x21E, row 0x21E b6=1 ret=0x1 imgadd=2 row6=[['0x403c10f6', '01']]
unit0 stats +0x64 = 1 (mask arm)   ret=0x0 imgadd=0 row6=[]
```

Every gate the README names is live:
- the roster count;
- unit flag `0x10`;
- `+0x6B6`;
- the `+0x710` handle through the `0031B7E0`/`003588B0` gate byte;
- the target's party kind 0;
- the `<= 0x21E` bound. `0x21E` passes and `0x21F` exits, which is an edge the package says it does not exercise; it is exercised here.

The tested address follows `+0x714 × stride + 6` from the descriptor. So the controls bind to the stated roster, handle, kind-0 target and action row, not to an accident of the fixture.

## SWE2-AUDIT-SPEC 3. retained census limits

### SWE2-AUDIT-SPEC census reproductions

`census_imgadd.py` was rerun from a scratch copy, with cwd = repo root. Its output is identical to the retained `census_imgadd.out`, apart from line endings:

```
fixtures executed: 89 cases + 10 mutants
fixtures with imgadd>0, tvalid>0 or a base-cell read: 3
  case   canc-fixup             imgadd=0 tvalid=1 base_cell_reads=-
  case   tv-row6-set            imgadd=2 tvalid=1 base_cell_reads=['1F83530']
  case   tv-row6-zero           imgadd=2 tvalid=1 base_cell_reads=['1F83530']
fixtures with imgadd>0: ['tv-row6-set', 'tv-row6-zero']
```

The two new cases are this census's positive control: its read hook does fire on the cell.

**Independent span census of the archived harness (`rv_census.py`).**
- It imports a scratch copy of the original `check.py` (sha `3a802841`, `G_IMGB=1F85D30`), not the repaired one.
- For each of the 87 cases and 10 mutants, it hooks every instruction inside each of the 54 `bodies.json` spans, not only the entry.

```
bodies.json real_bodies_executed: 54
fixtures executed: 87 cases + 10 mutants
listed bodies with NO instruction executed by any fixture: 7
   0020E600
   0025AAD0
   002F1710
   00316A50
   00317E50
   003BBC80
   003DC780
listed bodies entered mid-body only (any>0, entry==0): []
0030C0E0 fixtures and deepest pre-loop-tail address: {'canc-fixup': 'max<1CC=0030C179'}
fixtures executing any of 0030C187..0030C1CA: []
result.json rows: 97 ; trace entry events for {'lastres': 0, 'bitclear': 0, 'upd': 0, 'fix3': 0, 'zscan': 0, 'recref': 0, 'imgadd': 0}
```

- This confirms the README's set: `0020E600` plus the six hooked bodies, with zero entries in `result.json`.
- Under the retained fixtures, no instruction of those seven executes anywhere in the body. An entry-only hook therefore did not hide a mid-body execution.
- The two unhooked VAs, `002FD880` and `002FD420`, are **not** in the zero set: they execute. The README's "the trace cannot confirm them" is accurate about the trace, and this census settles it.
- 47 of the 54 listed bodies execute.

### SWE2-AUDIT-SPEC how the package and its consumers state these limits

- **"Zero old imgadd = a coverage gap, not invalid bit-22/copy cases."**
  - The README's sections "what was wrong", "impacted-case census" and "which old EXP-091 claims depend on the 0020E600 branch" state this correctly. "No case check depends on the branch". The bit-22, copy, other cancel and mutant cases "never enter `0030C0E0`. They stay supported". The dependent claims are "coverage claims, not case results".
  - The commit message ("no old case depended on the branch") agrees.
  - So does the earlier SPEC review `auditspec-review-astra-uq147-target-fixup-effects-1003/REVIEW.md` L44-46.
  - My span census confirms that only `canc-fixup` enters `0030C0E0`. **Holds.**
- **"Not universally unreachable."** The README never says unreachable. The new control shows that `0020E600` and the action-row arm are reached by the shipped `0030C0E0` under a valid two-unit roster. Its limits correctly add that the runtime value of `01F83530` is a separate question (CD-2 / UQ-83 / UQ-139). **Holds.**
- **Six hooked zero-entry bodies.** The README's "related finding" paragraph is scoped correctly: "this is a statement about the retained cases. `bodies.json` may come from a different case set". `bodies.json` is dated before `785d37b96`, and `run1.log` records an earlier case set (8/10 mutants). Two sentences in the package over-reach, though:
  - Consumer item 1: "`0020E600` was never entered". This must read "was not entered by any retained EXP-091 case or mutant".
  - Consumer item 2: "This is **false** for `0x20E600`, and by the related finding above also for six more listed VAs". This must read "unsupported by the retained fixtures". The retained evidence cannot show that an unretained earlier case set did not execute them, and it says nothing about the game.
  - Neither sentence is written into a canonical page yet. They are the package's proposals to the owner, and the wording below replaces them.
- **Consumer pages that over-claim today (grep of `EXP-?091`, `~54`, `every listed VA` over `Database/FFXII TZA/**/*.md`).**
  - The three the package lists are the over-claims: `CONTRACT-commit-action.md` L322 and L373, and `EXP-091-commit-callees-exec.md` L14 and L139.
  - Additional, candidate-level: `_index/candidates/s20-runtime-per-invariant-exposure.md` L53 puts "~54 bodies (`bodies.json`)" in its **"runs as shipped"** column. That is the same over-claim. None of the 13 bodies it names is among the seven.
  - Minor: `_index/candidates/s25-runtime-per-invariant-exposure.md` L37 says `bodies.json` "lists 53 real bodies". It lists 54. This is a listing statement, not an execution claim.
  - Minor: the earlier SPEC review `auditspec-review-astra-uq147-target-fixup-effects-1003/REVIEW.md` L44 says "result.json and bodies contain zero imgadd". `bodies.json` does list `0x20E600`; the zero is in `result.json`'s traces. That review's conclusion is unaffected.
  - Agreed as needing no change, as the package lists them: `CONTRACT-the-moment-an-action-is-committed.md` L159, `the-action-definition-row.md` L61 (the owner may add this package as execution support), `the-battle-unit-field-map.md` L177, `cross-subsystem-accessor-hubs.md` L319, `opus-audit-l1-contracts-1003/README.md` L87, `swe2oracle-ko-consumers-1003/README.md` L22/L31 and `uq147-ko-release-partition/README.md` L5.
- **Not reviewed here:** the README's aside on the `002FEAD0` bit-20 polarity in `the-record-00329220-builds.md` L428-433 is outside this request. It is not accepted or rejected by this review.

## SWE2-AUDIT-SPEC 4. consumer wording (exact)

The owner of each page, OPUS for the contract and the EXP-091 record, applies these. This review edits none of them.

**A. `07-Combat-Action/CONTRACT-commit-action.md` §13a, L321-324.**

Replace

> ran exactly those insides — every scripted callee plus its bounded transitive closure, ~54 shipped bodies, then `0030F760` re-driven end to end with the real callees wired in.

with

> ran those insides — every scripted callee and 47 of the 54 bodies `bodies.json` lists for their bounded transitive closure — then `0030F760` re-driven end to end with the real callees wired in. The retained 87 cases and 10 mutants execute no instruction of `0020E600`, `0025AAD0`, `002F1710`, `00316A50`, `00317E50`, `003BBC80` or `003DC780`, and run `0030C0E0` only to `0030C179` (`canc-fixup`). That is a coverage gap of the retained fixtures. It invalidates no retained case (bit 22, copy, cancel, commit, mutants), and it does not show that the game never runs those bodies. `0020E600` and `0030C0E0`'s action-row arm `0030C187..0030C1CA` are executed by [`exp091-resolver-base-repair-1003`](../_experiments/evidence/exp091-resolver-base-repair-1003/README.md) (`tv-row6-set`/`tv-row6-zero`, resolver base planted at `01F83530`, method B; returns 1 iff action-row byte 6 != 0).

The same sentence still reads "85/85 cases". The retained result is 87/87 since `f7bbac4ef`, and the owner may correct the count in the same edit.

**B. `07-Combat-Action/CONTRACT-commit-action.md` L372-373.**

Replace

> approximate on jump-table dispatchers**, though every listed VA was genuinely executed.

with

> approximate on jump-table dispatchers**. The list is not an execution record: under the retained 87 cases and 10 mutants, 47 of its 54 VAs execute and the seven named in §13a do not (instruction-level span census, `_index/candidates/auditspec-review-oracle-exp091-resolver-repair-1003/REVIEW.md`).

**C. `_experiments/EXP-091-commit-callees-exec.md` L14.**

Replace

> plus their bounded transitive closure (~54 shipped bodies)

with

> plus their bounded transitive closure (`bodies.json` lists 54 bodies; the retained fixtures execute 47 — see `evidence/exp091-resolver-base-repair-1003/`)

**D. `_experiments/EXP-091-commit-callees-exec.md` L139.**

Replace

> every listed VA was genuinely executed.

with

> 47 of the 54 listed VAs execute under the retained 87 cases and 10 mutants. `0020E600`, `0025AAD0`, `002F1710`, `00316A50`, `00317E50`, `003BBC80` and `003DC780` do not. This is a coverage gap of these fixtures, not a reachability result. The harness planted the resolver base at `0x1F85D30`, not the `0x1F83530` that `0020E602` reads. No retained case reaches `0020E600` or reads either cell, so no retained result changes. The repair and the action-row control are in `evidence/exp091-resolver-base-repair-1003/`.

**E. `_index/candidates/s20-runtime-per-invariant-exposure.md` L53, "runs as shipped" cell.**

Replace

> ~54 bodies (`bodies.json`), including

with

> 54 bodies listed in `bodies.json`, 47 of which the retained fixtures execute (not `0020E600`, `0025AAD0`, `002F1710`, `00316A50`, `00317E50`, `003BBC80`, `003DC780`), including

**F. When citing `exp091-resolver-base-repair-1003/README.md` consumer items 1-2:**
- Use "not entered by any retained EXP-091 case or mutant" for item 1's "never entered".
- Use "unsupported by the retained fixtures" for item 2's "false".
- Add that `002FD880`/`002FD420` do execute, per this review's span census.

## SWE2-AUDIT-SPEC limits

- Method B under a hand-built world. Nothing here observes the game, and nothing here is an ASTRA sample.
- The runtime value of `01F83530`, and whether the game reaches the action-row arm, stay with CD-2 / UQ-83 / UQ-139.
- The 32-bit truncation of the row address is still not stressed: every fixture address fits in 32 bits.
- The mask arm `00377C20` returning nonzero was not driven to the resolver. My one mask-arm flip exits at `00377C20`.
- The full 89-case repaired campaign was not rerun, and neither the producer nor the request requires it.
- The reference scan is rip-relative over `.text`. The producer's memory-read census covers other addressing forms for the fixtures it runs.
- Reviewer scripts and outputs are outside the repo, under the session scratchpad `exp091rev/`: `rv_disasm.py`/`.out`, `rv_probe.py`/`.out`, `rv_handle.py`/`.out`, `rv_census.py`/`.out`, and `run/` (the copies, plus the reproduced `run_repaired.out` and `census_imgadd.out`).
