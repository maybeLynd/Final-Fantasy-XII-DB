# S-20 runtime: per-invariant stub exposure for EXP-033/034/040/043/046/047/091 (OPUS, 2026-09-25, block 305)

*Drafted by a delegated OPUS pass and reviewed before publication (block 305): its concrete address claims were spot-checked against the image; see the block-305 inbox entry for which.*

**Row:** S-20 command commit and dispatch. The runtime verdict is **MIXED**: *"7 records execute the commit path under
isolated original-code replay … no per-invariant stub-exposure analysis yet"*. The binding gap reads *"runtime cell
is ASTRA/ORACLE's gap"*.

The six contracts (column 6 of `important-subsystems.tsv`) are all under `07-Combat-Action/`:

| contract | invariants (§4) |
|---|---|
| `CONTRACT-commit-action.md` | a precondition sentence, the acceptance/refusal postconditions, and one invariant (the block and its copy are consistent) |
| `CONTRACT-battle-target-buffer.md` | append/refuse/reset/find postconditions; `0 <= count <= 32`; insertion order |
| `CONTRACT-combo-continuation.md` | CB-1..CB-6 |
| `CONTRACT-battle-action-handler-table.md` | HT-1..HT-6 |
| `CONTRACT-native-command-seam.md` | CS-1..CS-6 |
| `CONTRACT-the-moment-an-action-is-committed.md` | CM-1..CM-6 |

Evidence classes are original-code replay (Unicorn) and static; nothing here is live. This note scores nothing.

**Probe:** `s20-probes/s20_commit_block_probe.py`, output in `s20_commit_block_probe.out.txt`. It imports EXP-091's own
`check.py` read-only (bytecode writing off) and re-runs its `0030F760` fixtures with planted patterns and extra reads.
Every run records the return value, the final RIP, whether it reached the sentinel `RETQ` `0x62000000`, RSP
restoration and faults.

## Which contract each record belongs to

| record | subject | front matter | actually executes |
|---|---|---|---|
| EXP-033 | the action-id gate | commit-action | a fragment of `0030F760` from `0030F798` to a boundary (`0030F7A7` / `0030F7F2` / `0030F981`). This is CM-2's two bands |
| EXP-034 | the focus resolver chain `0031B7E0` → `003588B0` → `00263FF0` → `00263E30` | commit-action | the resolver that CM-1 calls at `0030F791`, **not** the commit |
| EXP-040 | the cancel `003105D0` | commit-action | the entry gates plus two local blocks (`0031060A`..`00310618`, `003106B9`..`0031072F`). These are CM-6, CM-5's consumer and CB-1's word store; they belong to the-moment and combo more than to commit-action |
| EXP-043 | append `00316CD0` | target-buffer | the whole body |
| EXP-046 | reset `00316CF0` | target-buffer | the whole body, with memset bridged |
| EXP-047 | reset wrappers `00322050` / `00322080` | commit-action | the `+0xEA4`/`+0xEA8` lifetime of commit-action §6. This is not a §4 claim, and the wrappers are also S-14's rekey |
| EXP-091 | the nine commit callees and their closure, then `0030F760` end to end | commit-action | commit-action, the-moment (CM-1..CM-6), and target-buffer (append/reset inside the commit) |

**No record executes a body of combo-continuation (`0030FA00`, `00388660`), of handler-table dispatch (`00305080`,
`002FDDA0`), or of the seam (`00311CF0`, the rings `022BEDA0` / `022BE980`).** I checked by grepping every record,
`check.py` and `bodies.json`. Those three contracts' §13 sections each say "None", and that is accurate.

## Substitutions per record

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-033** | `0030F798`..boundary of `0030F760` (570 B extracted) | **Fixture:** injected `RDI` (id) and `RAX=0`; the prologue, the resolver and the setup before `0030F798` are skipped. No stubs, no imports |
| **EXP-034** | `0031B7E0`, `003588B0`, `00263FF0`, `00263E30` whole | **Fixtures only:** gate byte `02089340`, manager `02098E10 + sel*0x288`, vector, actor. No stubs, no imports |
| **EXP-040** | `003105D0` entry gates to the sentinel; blocks `0031060A`..`00310618` and `003106B9`..`0031072F` | **Omitted code** (not stubbed, not run): `00310780`, `0030C970` ×2, `00300280`, `0016D6A0`, `00236850`/`00236820`, `00316CF0`, and everything after `0031072F` (`003291B0`, `0033C9B0`). **Fixture:** injected `RBX`/`RSI`/`RBP` at each block start; patterned unit |
| **EXP-043** | `00316CD0` whole (24 B) | **Fixture:** synthetic buffer, including negative counts. No stubs |
| **EXP-046** | `00316CF0` whole (57 B) | **Import bridge:** the hook at thunk `00861EC0` (IAT `008C2A60` `VCRUNTIME140!memset`) performs the fill; the thunk's `jmp` is not executed. **Fixture:** buffer page |
| **EXP-047** | `00322050`, `00322080`, `00263E30` | **Application stub** `003220E0` (the delegate): 5 cases stop at its entry; 5 cases inject a return `0xFEDCBA9876543210` with no memory effect. **Fixture:** unit/actor pages |
| **EXP-091** | ~54 bodies (`bodies.json`), including `0030F760`, `003105D0`, `00310780`, `0031B7E0`, `003588B0`, `00316CF0`, `00316CD0`, `0030AB40`, `0030C970`, `00313B30`, `002ED2A0`, `00308270`, `0030EDA0`. The whole image is mapped | **Application stubs** (`BODYSTUBS`, entry patched to `ret`): `00512F30` event sink; `0033C9B0` MRESET; `002FC9D0` / `002FCBA0` family `+0x48` handlers. **Import bridges:** `memset` (IAT `008C2A60` → hook doing a real fill); IAT `008C3098` = **`api-ms-win-crt-utility!rand`** (the harness calls it "tick" / "timing source") → an incrementing counter; every other IAT slot is zeroed. **Fixtures:** unit array, stats records, `02EBF190` tables, a synthetic nibble table written over `02098E10`, link table `022C17B0`, posture table `022C1DB0`, render table `022C6F28`, `022BEFC0` / `022BEFB0`, cookie `01F44830`, fam3 `+8` |

**Which EXP-091 stubs the commit re-drive actually reaches.** This comes from the traces of the 15 `com-*` cases,
re-run in the probe. **Only `0033C9B0` (MRESET)** is reached, and only through `cancelFirst`, inside `003105D0` at
`00310758`. The memset import is also reached.
- `00512F30` is reached only in the `ed-*` / `ntf-*` cases. In `com-*`, `00313B30` collects no unit that reaches
  `002ED2A0`.
- `002FC9D0` / `002FCBA0` are reached only through `00300280` → `003008A0` when `+0xDC8 != 0xFFFF`. The com fixtures
  keep it at `0xFFFF`.
- `rand` is not reached in any `com-*` case while MRESET is stubbed.

## Can MRESET reach an S-20 invariant? (static reading plus a measured counterfactual)

**Static.** `0033C9B0` builds a stack context through `00336710(ctx, unit+0x80, 0)` and then calls
`0033E1F0(ctx)`.
- `00336710`'s stores in its own body go to the stack context only. Its `rdx`-based accesses are reads. Its callees'
  stores were **not read**.
- `0033E1F0` writes through `ctx+0x100` (= `unit+0x80`) at offsets `+0`, `+0x10`, `+0x14`, `+0x20`, `+0x21`,
  `+0x24`..`+0x33`, `+0x34`, `+0x38`, `+0x3C`, i.e. `unit+0x80`..`unit+0xBF`.
- It also writes `[ctx+0x108]+0x108`, i.e. `unit+0x188`.
- None of this is in `+0x6B4`..`+0x6B8`, `+0x700`..`+0x747`, `+0x770`, `+0x778`..`+0x97F` or `+0xEA4`/`+0xEA8`.

**Measured** (probe P5):
- **P5a:** run `com-cancel-first` with the MRESET stub removed. It **does not return**: final RIP `0x0`, the sentinel
  is not reached, and the fault is a fetch at 0. The last executed addresses are `004686D0`..`004686EE` → `00861F14`.
  That thunk jumps through IAT `008C2BB8` = `api-ms-win-crt-math!sqrtf`, which EXP-091's harness zeroes. So the shipped
  MRESET cannot run under EXP-091's world as written.
- **P5b:** add one disclosed import bridge (`sqrtf` → `sqrtss xmm0,xmm0; ret`). The run **returns 1** at RIP
  `0x62000000` with RSP restored and no faults; the trace now includes `htick` ×2 (the `rand` bridge).
- **Comparison with the stubbed run:** the actor differs **only** at `+0x92..+0x93` and `+0xBD`, and the target does
  not differ. Block = copy holds, and every S-20 invariant field (`+0x6B4..+0x6B8`, `+0x700..+0x72F`, `+0x770`,
  `+0x778..+0x97F`, target `+0xEA4..+0xEA8`) is identical.

## Per invariant

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| commit-action **§4 invariant**: the block `+0x700..+0x717` and its copy `+0x718..+0x72F` are consistent after every accepted commit | EXP-091 runs the stores and the copy (`0030F7F2`–`0030F82A`), but its memprobes **do not read** `+0x700..+0x72F`. **Probe P1:** with a planted pattern over `+0x700..+0x72F`, block = copy byte-for-byte in all 10 accepted `com-*` re-runs (bands 1 and 2, unresolved target, gate off, cancel-first, latch, posture, masked). All returned 1 at the sentinel with no faults | **no.** The copy is taken right after the stores, with no call between them. MRESET is measured as not reaching it (P5b). Caveat: the planted `+0x700` low bits were already 0, so the `and ~3` is not discriminated by P1 |
| commit-action **§4 precondition**: the cancel runs before the band test, so a refused commit can still have cancelled | EXP-091 `com-cancel-first` (accepted id only) orders `commit → cancel → resolv`. **Probe P4:** refused id `0x300` with `cancelFirst=1` returns **0** at the sentinel, and the cancel's stores are present: `+0x714=0xFFFF`, `+0x708=0`, `+0x710=0`, old copy → `+0x730`, buffer count 0. The target is untouched | **ordering: no** (body-local, `0030F776`–`0030F78A` before `0030F7A1`). The cancel's own outcome runs with MRESET stubbed; P5b shows that stub does not reach the fields the cancel is judged on |
| commit-action **postcondition on refusal**: only the optional cancel has run | **Probe P3:** `com-badid`, `com-b1-edge2` (`0x21F`), `com-b2-oob` (`0x4167`). Each returns **0** at the sentinel with no faults, and the actor and target units are **byte-identical** before and after | **no** |
| commit-action **postcondition on acceptance**: block written; buffer reset and refilled; target attacker mask updated | EXP-091 `com-b1-basic` (target `+0xEA8` 0→1, `+0xEA4`=4), `com-masked` (no second increment, no notify) | **no.** The mask RMW (`0030F940`–`0030F962`) precedes the notify `00313B30`, which runs real; its downstream `00512F30` is not reached in `com-*` |
| **CM-1**: an unresolved target is not an error | EXP-091 `com-notarget` (param 0) and `com-gateoff` (gate byte clear) both return 1. EXP-034 runs the resolver's null arms (14 of its 17 cases return 0) | **no.** The resolver is real in EXP-091; its inputs are fixtures |
| **CM-2**: bands `<= 0x21E` and `0x4000..0x4166` | EXP-033 (11 ids, fragment, 2 mutants); EXP-091 `com-b1-edge`/`-edge2`/`b2-lo`/`b2-hi`/`b2-oob`/`badid`; mutants `0030F79A`, `0030F7E5` | **no** |
| **CM-3**: only band 1 touches `+0x778` | **Probe P2:** with a planted `+0x778..+0x97F`, band-2 runs (`0x4000`, `0x4166`) leave the whole 0x208 bytes **unchanged**; band 1 resets it (flag `0xFF` → `0x01`, word `+1` = 0, rest zero) and appends (count 1) | **no** for the band split. The reset's fill is the memset **import bridge** (a real fill in the hook) |
| **CM-4**: band 1 appends even when the target does not resolve, as a null entry | EXP-091 `com-notarget` traces `append`, but **EXP-091's fixture cannot tell a null append from a resolved one**: target `+0x10` is 0, so both store 0. **Probe P2b:** with target `+0x10` planted as `0x40611000`, the resolved commit stores `0x40611000` and the unresolved one stores `0x0`; count 1 in both | **no** |
| **CM-5**: the block is shadowed as it is written; the cancel consumes the shadow | commit half: as the §4 invariant above. Cancel half: EXP-040 (`003106B9` → `+0x730..+0x747` = old `+0x718..+0x72F`) and probe P4 (`shadow730_equals_old_copy` True, full cancel) | **no.** In EXP-040 the omitted `00308270` → `0030EDA0` can write `+0x730..` (a copy of 0x4F0 bytes from `[+0xB88]`), but it runs **before** the `movups` at `003106D7`, which is the last write to `+0x730..+0x747` |
| **CM-6**: the cancel's null-unit and null-stats gates make it a no-op | EXP-040 (null unit, null stats reach the sentinel with no unit writes); EXP-091 mutant at `003105EA` | **no** |
| target-buffer **append** postconditions (accepted / refused unchanged / other 8 entry bytes not written) | EXP-043 (10 cases, whole page, write order); EXP-091 `app-*` | **no** (no stubs) |
| target-buffer **reset** postcondition: 0x208 zero except flag bit 0 | EXP-046 (4 cases); probe P2 inside the commit | **import-class only.** The zeroing is done by the memset bridge, not by the DLL. What `00316CF0` itself does (bit-0 save and restore, word `+1`, the argument tuple `(buf,0,0x208)`) is shipped code |
| target-buffer **find** postcondition | **not in this row's records.** `00316D70` is executed by EXP-093, EXP-149 and ~35 other harnesses (grep); not read | coverage by this row's records: none |
| target-buffer **invariant** `0 <= count <= 32` from a reset; insertion order | EXP-043 (0 → 32, cap refusal at 32/33/INT32_MAX); EXP-046 (count → 0) | **no** |
| commit-action §6 / EXP-047: attacker registration ends at a reset | EXP-047: the mask and count are cleared **before** the delegate (5 cases stop at `003220E0`'s entry) | **The clear: no.** Stubbed `003220E0` could only undo it afterwards; its own body has no `+0xEA4`/`+0xEA8` access (disassembled, 176 B). Its callees (`003589B0`, `002659D0`, `00327150`, `003588B0`, `00263E30`, `00326500`) were **not read** |
| combo **CB-1**: `+0x6B7`/`+0x6B8` are two byte fields; one word store | the census is static. EXP-040 executes the word store `003106EB` (`+0x6B7` word → 0) | n/a (a census claim); the executed store is unsubstituted |
| combo **CB-2..CB-6** (`0030FA00`, `00388660`) | **not executed** | coverage, not exposure |
| handler-table **HT-1..HT-6** | **not executed by this row's records.** The dispatch `00305080` runs nowhere. HT-4's availability half, `00301830` (window `003018DD`/`003018E3`, empty-slot test `003018F7` on `01EEC460`), runs real in **EXP-095**, which is S-25's record | coverage, not exposure. HT-4's "the two consumers agree" needs the dispatch half |
| seam **CS-1..CS-6** | **not executed** (CS-2 and CS-6 are static censuses; `00311CF0` and the rings are not run) | coverage, not exposure |

## Findings and contradictions

- **The-moment contract §13 is stale.** It says the commit "is unexecuted". EXP-091 re-drives `0030F760` end to end
  with real callees, and commit-action §13a records that.
- **EXP-091's record misstates the reset.** It says "`00316CF0` resets … byte `+0` bit1 → `memset` 208 B". The shipped
  reset preserves **bit 0** (`00316D05 and ebx,1`), and the fill is **0x208** bytes. Probe P2 measured flag
  `0xFF → 0x01` and the fill argument `0x208` (EXP-046).
- **The import names are wrong in two places.** Commit-action §13a says "Two host helpers (`memset`, `tick`) are IAT",
  and EXP-091 calls IAT `008C3098` a "timing source". The PE import directory names it `rand`. EXP-091 also zeroes
  `sqrtf` (`008C2BB8`), which is why the shipped MRESET cannot run in its world (P5a).
- **EXP-091's commit fixtures under-measure two claims.**
  - No memprobe reads the block copy.
  - Target `+0x10` = 0 makes CM-4's null append indistinguishable from a resolved append.

  Probes P1/P2b close both measurements; EXP-091's pass/fail is unaffected.
- **The binding gap names no remaining gap.** The runtime work actually left is:
  - combo, handler-table dispatch and seam, which are unexecuted;
  - target-buffer find, which is executed only outside the cell.
- **Cross-row, for the S-25 lead; noted only, not verified.**
  - EXP-095 describes `00301830`'s table as "`0x1ED0460`", which holds zeros in the image. The instruction at
    `003018F0` addresses `01EEC460`, the handler table.
  - EXP-095's "probed holes" (`0x4038–0x4047`, `0x4128–0x412F`) do not match the table's 18 null slots: `0x4025`,
    `0x4036..0x4045`, `0x4128`.

## For the scorer

- **Substitutions:**
  - EXP-091: 4 application stubs (`00512F30`, `0033C9B0`, `002FC9D0`, `002FCBA0`), import bridges `memset` and
    `rand`, and all other IATs zeroed.
  - EXP-047: 1 application stub (`003220E0`).
  - EXP-046: the memset import bridge.
  - EXP-033 and EXP-040: fragment execution with injected registers; EXP-040 also omits calls.
  - EXP-034 and EXP-043: fixtures only.
- **Of these, only MRESET `0033C9B0` is reached inside the commit re-drive.** Its reach on every S-20 invariant field
  was measured as **none**: P5b returned at the sentinel with one sqrtf bridge, and the differences lie only at actor
  `+0x92..+0x93` and `+0xBD`.
- **Exposure verdict:**
  - Commit-action, the-moment (CM-1..CM-6) and target-buffer append/reset/count are **not reached by any application
    stub**.
  - The buffer reset's zero fill is **import-class** (memset).
- **Coverage gaps, not exposure:**
  - combo CB-2..CB-6;
  - handler-table HT-1..HT-6 (dispatch runs nowhere; HT-4's availability half runs only in S-25's EXP-095);
  - seam CS-1..CS-6;
  - target-buffer find (run only by records outside the cell).
- **Newly measured by the OPUS probe** (original-code replay, not a record):
  - the commit-action invariant (block = copy);
  - the refused-plus-cancel precondition;
  - refusal writes nothing;
  - CM-3's untouched buffer on band 2;
  - CM-4 discriminated from the resolved append.
- `live_game` is false for all seven records.
