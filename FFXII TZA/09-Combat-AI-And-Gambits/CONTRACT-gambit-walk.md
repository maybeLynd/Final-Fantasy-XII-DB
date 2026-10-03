---
contract: walk one subgroup's gambit lines in order and commit the first that both matches and succeeds
category: 09-Combat-AI-And-Gambits
scope: operation
readiness: DIFFERENTIAL TESTED   # the WALK; its three callees executed 2026-09-18 (EXP-095, §13a) — see §13
confidence: PROVEN
implements: 09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md
entries: ["00305CC0"]
calls_supplied_as_oracles: ["003014C0", "0030F760", "004697C0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 53 addresses cited - 2 data, 11 entry, 40 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-gambit-walk-pass-1   # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the gambit walk

`BattleUnit_TrySelectAndCommitAiOrderFromSet` (`00305CC0`, 422 B). The player's gambit list is a
priority list, and this is the function that makes it one. It is also where the familiar complaint
that "a gambit with a satisfied condition did nothing" is explained exactly.

## 1. Purpose

Given a unit, an order set and a subgroup within it, try each order in turn and commit the first that
both **matches its condition** and **succeeds at being committed**. First match wins — but matching is
not sufficient, and that is the whole of the behaviour players see.

## 2. Interface

| | |
|---|---|
| entry point | `00305CC0` |
| calling convention | Microsoft x64 |
| `rcx` | the battle unit |
| `rdx` | the order set; **null returns 0 immediately** (`00305CF2`–`00305D01`) |
| `r8d` | the subgroup index, sign-extended (`00305CCC movsxd rax, r8d`) |
| `r9d` | resume mode |
| return | `int32` — non-zero when an order was committed, or when a resume reached its starting point |

## 3. Types

`AiOrderSet` at `0x02089378 + setIndex * 0x170`; `AiOrderRecord`, 24 bytes, ~~twelve per set~~ room for fourteen per set (`0x170` = `0x20` + 14 × `0x18`, `00328160`), of which the rebuilders fill at most twelve (`00328187`) *(corrected 2026-10-02, OPUS)*.

| | | |
|---|---|---|
| `set + 0x00` | `u8[32]` | per-subgroup order counts — the header this operation exists to walk |
| `set + 0x20` | ~~`AiOrderRecord[12]`~~ `AiOrderRecord[14]`, at most 12 filled *(corrected 2026-10-02, OPUS: `00328160`, `00328187`)* | the records, stride 24 |
| `record + 0x04` | `uint16` | flags; bit `0x40` and bit `0x80` govern resumption (§6) |
| `unit + 0x708` | pointer | the action context; its `+0x04` word's `0x4000` says a resume is in progress, **and the same pointer is compared against a record address** for the resume point (§6) |
| `unit + 0x714` | `uint16` | **ADDED 2026-09-11.** Latched at `00305CE5` before anything else; used only as the third call's third argument (§7) |
| `unit + 0x698` | pointer | **ADDED 2026-09-11.** The third call's first argument (§7) |

**The 24-byte stride is proven by the pre-multiply, not by the record count**: `00305D67 lea rcx,
[rax + rax*2]` triples the order index and `00305D97 lea rbx, [rbx + rcx*8]` scales by eight.

## 4. Finding the subgroup's first order

```c
a = b = c = 0;
for (i = 0; i < subgroupIndex - 1; i += 2) {   /* 00305D30-00305D47, two accumulators */
    a += set[i];
    b += set[i + 1];
}
if (i < subgroupIndex) c = set[i];             /* 00305D4E, the odd leftover */
first = set + 0x20 + (a + b + c) * 24;         /* 00305D5A-00305D97 */
```

The loop is entered only when `subgroupIndex >= 2` (`00305D24 cmp rax, 2 / jl`), and the two
accumulators are a compiler's unrolling of one sum — **not two independent quantities**. A
reimplementation summing a single counter over `[0, subgroupIndex)` is equivalent and simpler.

**`set[subgroupIndex]` must be non-zero or nothing is walked at all** (`00305D89 cmp byte ptr
[r11 + r10], dil / jbe`): an empty subgroup is not an error, it simply does nothing.

**And it is RE-READ on every iteration, not latched — ADDED 2026-09-11.** The loop's bound comes
from `00305DFD movzx eax, byte ptr [r12]`, inside the loop body, where `r12 = set + subgroupIndex`
was computed once. So a callee that changes the subgroup's count byte changes the number of orders
the walk will try, **while the walk is running**. A reimplementation that reads the count once
before the loop — the obvious way to write it — diverges the moment the evaluation or the commit
touches that byte. The differential suite drives it in both directions: shortening the count
mid-walk stops the original early (`E0 E1` where a latched version continues to `E5`), and
lengthening it makes the original continue where a latched version stops.

Whether any real evaluator or commit does write it is **not established here** and would need the
live game; what is established is that the walk would follow it if one did.

## 4a. One global bit stops every gambit in the game

`AiOrder_EvaluateAndResolveActionTarget` tests **bit 5 of the battle state word at `02089340`** at
`00301511` and returns 0 when it is set, ~~before doing anything~~ **after two writes it always makes**.
*Corrected 2026-09-26 (OPUS), by execution in `_index/candidates/s25-opus-replay-gambit-walk/`, case G4.* Ahead of the
bit-5 test the evaluator:
- zeroes `*param` (`003014ED`);
- decodes the order through `00308EC0`, stores the action id into `*out` (`00301500`), and returns 0 early if the id is
  `0xFFFF`.

So a suspended evaluator still overwrites both out-parameters. `00308EC0` and the stack-cookie check are the only
functions entered below it, and the commit is never reached. FABLE's reading of that word names the
bit **"combat AI suspended"**, and its three writers are worth having here because one of them is a
combat event rather than a script:

| writer | when |
|---|---|
| `SpawnGroup_RecordMemberDeathAndHandleCompletion` via `00238B70(1)` at `00306FA4` | **a kill that wipes a group** — see [`../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md`](../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md) §9 step 5 |
| `00359A30` and `0035AB20` | two sequence starters |
| `0035A6F0` | the only clearer |

**Bit 5 is always set and cleared together with bit 7**, the presentation veto — at the completion
site the two calls are adjacent. So the moment that suppresses the HP write's death event is the same
moment that stops every gambit evaluation in the game, and this contract and the HP write contract
describe two halves of one transition.

`AiOrder_EvaluateAndResolveActionTarget` is the first of seven readers of the bit.

## 5. Preconditions · postconditions · invariants

**Preconditions.** A unit in `rcx`. A null order set is ordinary and returns 0.

**Postconditions.** On a non-zero return either one order was committed, or — in resume mode — the
walk reached the order it left off at. On zero, **nothing was committed and no state was changed by
this function**; the evaluation and commit it calls may have changed state of their own.

**Invariant.** Orders are tried in address order from the subgroup's first. There is no priority
re-sort anywhere: **the order in the set is the priority.**

## 6. Resume semantics

Three bits, and they are not symmetrical.

| bit | where | meaning | site |
|---|---|---|---|
| `0x4000` | action context flags | a resume is in progress — this is what makes `resuming` true | read via `unit + 0x708` |
| `0x40` | `record + 0x04` | **evaluate this order even while resuming** | `00305DB2 test byte ptr [rbx + 4], 0x40 / je skip` |
| `0x80` | `record + 0x04` | **skip this order when in resume mode** | `00305DBC test byte ptr [rbx + 4], 0x80 / jne skip` |

The two record bits are tested against *different* conditions: `0x40` is consulted only when
`resuming` is set, `0x80` whenever `resume_mode` is non-zero. `resuming` and `resume_mode` are not the
same thing — the first additionally requires a context with `0x4000`.

**In resume mode, reaching the order the context points at returns 1 without evaluating it**
(`00305DA4 cmp r14, rbx / je`). That is the walk recognising where it left off.

## 7. The rule that explains the player-visible behaviour

```asm
00305DD2  call 003014C0        ; AiOrder_EvaluateAndResolveActionTarget
00305DD7  test eax, eax / je   ; condition failed -> next order
00305DF4  call 0030F760        ; BattleUnit_CommitAction
00305DF9  test eax, eax / jne  ; committed -> the success tail, which has a THIRD call
```

**Both must succeed.** A satisfied condition whose commit fails does not stop the walk and does not
act — the loop moves to the next order. ~~This is why a gambit can visibly do nothing while its~~
~~condition is plainly true, and~~ *(answered: not in the game — over the shipped action table a matched line is never refused by the commit, see the 2026-09-26 reachability note below; 2026-10-02, OPUS)* A reimplementation that treats a matched condition as a commitment
will act where the original declines.

*Reachability, qualified 2026-09-25 (FABLE, Claude Opus 5.5), on OPUS block 305:* the control flow above is real, but
its cause is narrower than it reads. **The action-band bound cannot refuse a condition-arm match**: the condition
check `AiOrder_CheckActionPreconditions` rejects `id − 0x4000 > 0x166` (`003018DD`–`003018E8`), and
`BattleUnit_CommitAction`'s band-2 test is the same bound (`0030F7D9`–`0030F7EC`). So no id that passed the condition
arm fails that test. EXP-095's *satisfied condition whose commit fails* was supplied by a stub. ~~Whether the unit arm~~
~~or the slot combiner can still make a real commit refuse is open~~ *(answered: neither can, see the 2026-09-26 reachability note below; 2026-10-02, OPUS)*, so the parity case above stays, as a control-flow
case rather than a demonstrated game state.

*Reachability, answered 2026-09-26 (OPUS, owner), measured in
[`candidates/s25-opus-commit-refusal-unreachable`](../_index/candidates/s25-opus-commit-refusal-unreachable/check.py), 6/6:*
**over the shipped action table, a line whose condition matched is never refused by the commit.**
- **The unit arm cannot produce a refusal.** Its availability check `002FFCF0` asks `BattleEncodedId_IsValidForClass(20,
  id)` (`002FFD8B`) and refuses with reason 4 (`002FFD94`) before any target selector. Class 20 accepts exactly
  `0`–`0x21E`, because the action table `[02EBF138]` has 543 rows *(qualified 2026-10-02, OPUS, from FABLE's review `fable-review-astra-ov42-actor-predicate-domain-1002`: the count is bound at run time, since `02EBF138` lies in `.data`'s zero-filled virtual tail past the section's raw bytes; a null descriptor refuses every id with reason 4)*, and that is the commit's first band. Measured:
  reason 4 for `0x21F`, `0x3FFF`, `0x4167` and `0x7FFF`.
- **The slot combiner cannot either.** It never touches the action. The evaluator's action slot has one writer, the
  decode at `00301500`, and the walk hands that slot only to the evaluator (`00305DCA`).
- **The commit's only return 0** is `0030F981`, and its one branch source is the band test `0030F7EC`. The commit
  called directly still refuses `0x21F` and `0x4167`, so the band is real.
- **The bound is the table's row count.** A pack with more than `0x21F` action rows would let the unit arm pass ids the
  commit refuses.
- The parity case above therefore stays as a control-flow case, not as a game state.

**Executed 2026-09-11**: a reconstruction that treats a match as a commitment is caught on **3**
comparisons of a 29-case suite, including one where the two disagree on the *return value* and not
only on which line acted.

~~The target is passed as a word from a stack slot initialised to **`0xFFFF`, the no-target sentinel**
(`00305CCF`–`00305CD6`), and the parameter from a second slot initialised to 0.~~
**Corrected 2026-09-26 (OPUS, owner), measured in `candidates/s25-opus-replay-gambit-walk/commit_walk.py` (W2, W3):**
the two slots hold the **action** and the **target**, in that order.
- The word slot `[rsp+0x70]`, initialised to `0xFFFF` (`00305CCF`–`00305CD6`), is the evaluator's `out`. The evaluator
  stores the decoded **action id** there (`00301500 mov word [r12], ax`), and the walk passes it to the commit as `r8w`
  (`00305DE3`), the commit's action id.
- The dword slot `[rsp+0x30]`, initialised to 0, is the evaluator's `param`. The evaluator stores the **target id** there
  (`003017E7`), and the walk passes it as `r9d` (`00305DDB`), the commit's target.
- Executed: an authored "Foe: nearest visible → Attack" line commits with `r8w = 0x96` (the record's action word) and
  `r9d = 0x100000`, and the commit writes them to `+0x714` and `+0x710`.

### There is a THIRD call, on the success path — ADDED 2026-09-11

```asm
00305E31  test ebp, ebp / je 00305E5F        ; resume_mode == 0 -> no third call
00305E35  movzx eax, word [rsp+0x78]         ; the word LATCHED from unit+0x714 at entry
00305E3F  cmp ax, 0xFFFF / je 00305E5F       ; the sentinel -> no third call
00305E44  movzx edx, word [rsp+0x70]         ; the ACTION word the evaluator decoded (corrected 2026-09-26)
00305E49  mov r9d, 4                         ; a constant
00305E4F  mov rcx, [r13 + 0x698]
00305E56  movzx r8d, ax                      ; the latched word
00305E5A  call 004697C0                      ; return value DISCARDED
```

So after a successful commit, **when resume mode is non-zero and the latched `unit + 0x714` is not
`0xFFFF`**, the walk makes a third call with `[unit + 0x698]`, ~~the resolved target word~~ **the committed action
word** (`[rsp+0x70]`, `00305E44`; see the correction above), the latched word, and the literal `4`. Its result is not
read.
- *Corrected 2026-09-26 (OPUS, owner).* Executed in `commit_walk.py` W6, with `+0x714` set to `0x4021` first so that the
  two words differ: a resumed commit of Attack calls `004697C0([unit + 0x698], 0x96, 0x4021, 4)`.
- `+0x714` is also the commit block's action id (CONTRACT-commit-action CM-5). So the latched word is **the action
  this unit committed last**, and the third call carries both the previous action and the new one.

**Two consequences.** A reimplementation built from the two-call description above silently drops a
notification on every resumed commit — the differential test catches it on the trace, not on the
return value, because the return value is identical. And **`unit + 0x714` is a field this contract's
§3 did not list**; it is read once at `00305CE5`, before anything else, and exists only to be this
call's third argument. `004697C0` itself is unidentified — 251 bytes, not read for this contract.

## 8. Composition

This operation is the top of a chain this database now specifies end to end:
the walk commits through `BattleUnit_CommitAction`, which fills the unit's target buffer
(`CONTRACT-battle-target-buffer.md`); the resulting action's targets are processed into the parallel
result array; and any HP change reaches
`CONTRACT-hp-write-and-lethal-transition.md`, whose event variant is read back out of that same
target buffer. **A gambit firing and a combatant dying are two ends of one specified path.**

## 8a. Where the walk's set and subgroup come from: the set selector and the switch orders (FABLE, 2026-10-03)

*Added for SWE2-AUDIT-SPEC's SCOPE-SHORT on S-25 ([`auditspec-l2-expansion-1003`](../_index/candidates/auditspec-l2-expansion-1003/README.md) item 3, adopting AUDIT-SEM's proposal): the registry
subject is "gambit evaluation, set selection and enmity", and this contract named the selector `00305AB0` only in §14
item 1, as the shape of the walk's `r8d`. Static and isolated original-code; every fact below is checked by
[`check_s25.py`](../_index/candidates/fable-l2exp-s25-mech-1003/check_s25.py) (FAILS 0). The four sets' roles and their installers are
[the set page](which-gambit-set-fires-and-how-a-command-switches-it.md) §2 and its UQ-122 box; how an order id reaches
`002FDDA0` is [the handler-table contract](../07-Combat-Action/CONTRACT-battle-action-handler-table.md) HT-2 and HT-3.
This section states what neither does: the order in which the sets are offered, what decides between them, and what the
switch orders write. The contract's claims carry no ids (the S-25 exposure note cites them as G-§n), so the invariants
here are **G-§8a.1–G-§8a.7**.*

**Interface.** Two entries and one script route:

| entry | reached from | arguments | return |
|---|---|---|---|
| `BattleUnit_SelectAndCommitNextAction` `00305AB0` (517 B) | `0030874C` in the combat frame `00308610` (resume mode 1, `00308744`) and `00313D89` in the queue drain `00313CD0` (mode 0, `00313D84`); no pointer constant | `rcx` the unit; `edx` the resume mode, kept in `edi` and passed to every walk as `r9d` | the first non-zero walk; else the fallback commit's return; else 0 |
| `BattleUnit_ExecuteDirectStateCommandOrder` `002FDDA0` (1937 B) | no `E8`/`E9` caller; 249 slots of the order table `01EEC460`, every id `0x4112`–`0x4121` among them, tail-called with only `rcx` (HT-3) | `rcx` the unit; the id re-read from `+0x714` (`002FDDB0`) | 1 for a handled id (`+0x6B4` = 2); `-1` unhandled (`+0x6B4` untouched) |
| verb `3060` `btlAtelSetDefaultLogic` `00510580` → `00239040` | the tail jump `0051059B` | the actor; `k` popped by `00267E10` | none read |

**The cascade.** One call of `00305AB0` offers sets to the walk (§4–§7) in this order, and the first walk that returns
non-zero jumps to the epilogue `00305CA0`:

0. **Unit flag bit 22** set: `00308270` runs first (`00305AC1`–`00305AC8`). Its call `003082C6` to `0030EDA0` copies
   the suspension snapshot at `[+0xB88]` back over `+0x6B0`–`+0xB9F`, which holds all four set pointers, the subgroup
   byte and `+0x748`. It then clears bits 22 and 46 (`003082CB`–`003082DF`). So the sets this call reads are the ones
   the unit had when it was suspended (executed E15).
1. **The issued command.** With unit flag `0x4000` set (`00305ADF`) the flag is cleared (`00305AEB`, `00305AF0`) and the
   word `+0xBA0` is committed with target `+0xBB8` and cancel-first 1 (`00305B12`–`00305B2F`). An id in `0x4000`–`0x4166`
   skips the availability check (`00305AF3`–`00305B01`); any other needs `002FFCF0` to return 0 (`00305B09`–`00305B10`).
   A commit ends the call; a refusal falls through to the sets (the gambit page's section 8h).
2. **Field bit 15** (`00377C20`) with a party-kind stats record (`[+0x698]+5` = 0): no set at all, straight to step 9
   (`00305B3C`–`00305B57`).
3. **The forced set for Confuse and a kind-1 Berserk.** With field bit 15 clear, status bit 5 (Confuse) in the stats
   masks `+0x64` or `+0x3C` (`00305B66`–`00305B76`), or bit 27 (Berserk) on a kind-1 record (`00305B7D`–`00305B87`),
   sends the unit to the static set `01EEC320` at subgroup 0 through the fourth call site (`00305B89` → `00305C68`), and
   from there to step 9. No other set is offered.
4. **A**, `+0x6E8`, subgroup 0 (`00305B95`–`00305BA5`).
5. **The party Berserk set.** With field bit 15 clear, a party-kind record with bit 27 sends the unit to the static set
   `01EEC370` at subgroup 0 through the third call site (`00305BB2`–`00305BE5` → `00305C52`), then to step 8.
6. **C**, when the stats pointer is null, the record is not party-kind, or the record's flag bit 2 is set
   (`00305BE7`–`00305C03`): `+0x6F8` and `+0x748` are cleared (`00305C45`, `00305C4C`) and C = `+0x6E0` is walked with
   **the subgroup byte `+0x6B5`** (`00305C34`–`00305C58`).
7. **B** otherwise, `+0x6F8` at subgroup 0 (`00305C05`–`00305C1A`). A null B goes to step 8 (`00305C0F`); a B that fails
   is cleared with `+0x748` (`00305C25`, `00305C2C`) and also goes to step 8 (`00305C32`). **C is not offered.**
8. **D**, `+0x6F0`, subgroup 0 (`00305C61`–`00305C71`).
9. **The fallback.** In resume mode the call returns (`00305C7A`, `00305C7C`). Otherwise it commits the static record
   `01EEC298`, `{0x4021, flags 0x2000}`, with target 0 and cancel-first 1 (`00305C7E`–`00305C9B`): the wait order with
   `n` = 0, which never completes (the set page, UQ-125).

The two forced sets decode as `01EEC320` = {`0x0096` with one target entry of relation 1, then `0x4125`} and
`01EEC370` = {`0x0096` with relation 1}. Besides `00305AB0`, the only code that names either is the membership test
`0030BF20`, which compares a record pointer against each set's records and has one caller, `00307DC2` in `00307D10`, on
the unit's current order `+0x708`.

**The switch orders.** `002FDDA0` returns 1 at once, writing nothing, when `+0x6B4` is already non-zero
(`002FDDB7`–`002FDDCE`). Otherwise:
- **`0x4116 + k`, k = 0…11, selects a subgroup.** `+0x6B5` = `(id & 0xFF) - 0x16` (`002FE0B8`, `002FE0BB`), with no
  test of the unit's kind.
- **`0x4112 + k`, k = 0…3, selects a variant set.** It needs a stats record of kind 1 (`002FE025`–`002FE042`); any
  other unit returns 1 with only `+0x6B4` written (`002FE50C`). The row word `[+0xE60] + 0x50 + 2k` indexes the directory
  at `[02EBF168]`, bounded by its `u16` count (`002FE05B`–`002FE077`). Out of range, or a null directory, returns `-1`
  (`002FE523`). In range, `+0x6E0` = `0020E600(entry)` = the stored offset + `[01F83530]` (`002FE082`–`002FE08E`) and
  **`+0x6B5` = 0** (`002FE09F`).
- **Verb `3060` selects a variant without the arm's checks.** `00239040` takes `k` unsigned up to 3 (`00239049`), finds
  the unit through `0031B760`, and stores `+0x6E0` from the same row word and directory (`00239060`–`00239081`), or 0 when
  the directory slot is null (`00239093`). It tests no kind and no count, and **it does not touch `+0x6B5`**.

**Reads and writes.**

| unit field | read by the selector | written |
|---|---|---|
| `+0x6E8` A | `00305B95` | the six re-plan installers on the set page (UQ-122); 0 at reset `00236BBD` |
| `+0x6F8` B, `+0x748` | `00305C05` | 0 by the selector at `00305C25`/`00305C2C` (B failed) and `00305C45`/`00305C4C` (C entered); `BattleUnit_IssueCommand` `00311DE1`/`00311DDB`; the clearers on the set page |
| `+0x6E0` C | `00305C3E` | the kind-1 bind `0023A95E` (variant 0, its count bound at `0023A71E`–`0023A726`); the party bind `0023AB9F` (`02089378 + i * 0x170`, §3); the switch `002FE08E`; the verb `00239081` / `00239093`; 0 at reset `00236BC4` |
| `+0x6B5` subgroup | `00305C34`, the only read | `00236BA3` (reset, 0), `002FE09F` (0), `002FE0BB` (0…11), which is the whole exact-displacement census; and the block pair in the next row |
| `+0x6F0` D | `00305C61` | `0023ABB5` (`01E09350` = {`0x4124`, flags `0x2000`}) on the party arm of `0023A570` only; 0 at reset `00236BB6`; and the block pair |
| the block `+0x6B0`–`+0xB9F` (all of the above) | — | the suspension `0030EFF0` (one caller, `0031307B` in `00312FA0`) copies it to a pool buffer (`0030F04A`–`0030F0E1`), zeroes it (`0030F0E5`–`0030F0EC`, `0x4F0` bytes) and keeps the buffer at `+0xB88` (`0030F0F1`); the restore `0030EDA0` copies it back. Pointer-loop copies, which no displacement census sees |
| `+0x00` flags | bits 14 and 22 (`00305ADF`, `00305AC1`) | bit 14 cleared at `00305AF0` |
| `+0x6B4` | — | `002FDDA0`: 2 on every handled id |

**Invariants.**
- **G-§8a.1 — One set at a time, in a fixed order, and the first commit ends the decision.** Steps 1–9 above; the walk's
  own order inside a set is §5. Executed E1–E13: each trace offers the sets in that order and stops at the first set
  whose walk returns 1.
- **G-§8a.2 — B and C are exclusive, chosen by the stats record before either is walked.** The three tests of step 6
  route a unit to C or to B. B's failure goes to D (`00305C32`), never to C. A unit routed to C loses any pending B set
  first. Executed E1–E4.
- **G-§8a.3 — Status replaces or splices the cascade, and field bit 15 overrides status.** Confuse, or Berserk on kind
  1, replaces A–D with `01EEC320`. Berserk on a party unit inserts `01EEC370` after A and before D, and keeps `+0x6F8`.
  With field bit 15 set no forced set is used, and a party-kind unit walks no set at all. Executed E5–E9.
- **G-§8a.4 — Only C reads the subgroup.** `00305C34` is the one read of `+0x6B5`; the other three call sites and the
  forced-set entry pass `r8d` = 0 (`00305B9F`, `00305C14`, `00305C6B`, `00305BDB`).
- **G-§8a.5 — Three routes change C or its subgroup, and only the order arm keeps them consistent.** `0x4116 + k` sets
  the subgroup for any unit. `0x4112 + k` installs a variant for a kind-1 unit and restarts it at subgroup 0. Verb `3060`
  installs a variant and **keeps the old subgroup**, so the next C walk indexes the new set with the subgroup the old set
  last selected. Executed W1–W2 and V1 (subgroup 5 before, 5 after, for k = 0…3).
- **G-§8a.6 — Outside resume mode, every decision commits something.** When no set commits, the fallback commits the
  never-ending wait `0x4021`. In resume mode the same exhaustion returns 0 with nothing committed. Executed E1 and E12.
  (`0x4021` lies in the commit's second band, [the commit contract](../07-Combat-Action/CONTRACT-commit-action.md) §3; the
  commit itself is supplied in E.)
- **G-§8a.7 — A kind-1 unit has no D floor from its definition.** In `0023A570` the definition-kind split is at
  `0023A626`–`0023A62E`. The kind-1 arm jumps from `0023AA2A` / `0023AA44` to `0023ABCA`, past the `+0x6F0` store at
  `0023ABB5`, and `0023ABA6` is the only reference to `01E09350`. The kind-1 unit's `+0x6F0` therefore keeps the reset's
  0 (`00236BB6`, `rsi` zeroed at `00236A93`), D walks nothing (§10 item 1), and a kind-1 unit whose A and C produce
  nothing waits (`0x4021`) rather than following its leader (`0x4124`). Image-wide there are twelve qword stores at
  `+0x6F0`. The other ten are in the developer console `001D0390`, a stack frame (`0035E100`), a render-object pair that
  stores 0 (`0041F730`, `004200A0`), post-processing (`006FF5D0`, `006FF900`, `00705520`) and the `007Cxxxx` library
  (stores `007C091D`, `007C0B23` and `007CE47D`). The suspension pair moves the unit's own block out and back, so it carries no `01E09350`
  to a unit that never had it.

**Failure paths.**
- **A null stats record faults in the selector unless field bit 15 is set.** `00305B6D` reads `[stats + 0x64]` before
  the null test at `00305B78`.
- **`002FDDA0` reads `[+0x708] + 2` before its guard** (`002FDDA6`, `002FDDBE`). A null context pointer faults even for
  an id it would not handle.
- **A variant order on a unit that is not kind 1 reports success and does nothing** (1, `+0x6B4` = 2). An index past the
  directory's count, or a null directory, returns `-1` with `+0x6B4` untouched, which is HT-5's ambiguous `-1`.
- **Verb `3060` has no bound.** A row word at or past the directory's count reads past its end (executed V2: entry 9 of
  a one-entry directory). A null directory installs 0, so C then walks nothing.
- **A suspended unit has no sets until its restore.** Between `0030EFF0` and the restore, every set pointer and the
  subgroup read 0. A selection on such a unit without bit 22 walks four null sets and commits the wait (executed E16).
  Whether the game ever selects for a suspended unit without bit 22 is not traced.
- **After a verb switch, `+0x6B5` can name a subgroup the new set leaves empty** (C walks nothing, §4), or a populated
  subgroup that the new set never switches into (G-§8a.5).
- **A reimplementation that tries C after B fails**, applies Confuse or Berserk after A instead of before it, gives every
  unit the `0x4124` floor, or resets the subgroup on every variant change, diverges on E2, E5–E7, G-§8a.7 and V1.

**Evidence class.** Static: K1–K9 of `check_s25.py`. The raw reference index covers `E8`/`E9`, `0F 8x`, `EB`/`7x`,
rip-relative, image-base-relative and pointer constants; the census is an exact-displacement census of `+0x6B5` and
`+0x6F0`, plus the two block copies read whole; reachability is direct control flow inside `0023A570`. Isolated
original-code, under Unicorn 2.1.4:
- the selector `00305AB0` whole in fourteen cases (E1–E14), with its five callees supplied by hooks (the walk, the
  commit, `00377C20`, `002FFCF0`, `00308270`);
- the suspension `0030EFF0` and then the selector, with `00308270` and the restore `0030EDA0` as shipped (E15–E16; the
  allocator `0030DFA0` and `0030C970` supplied, the memset import bridged);
- `002FDDA0` whole for every id `0x4112`–`0x4121` and four edge cases (W1–W6), with `0020E600` as shipped;
- the verb body `00239040` (V1–V2), with `0031B760` answered by a hook.

Seven sensitivity controls each turn a check to FAIL: B's failure jumping to C, the field-bit skip removed, the variant
arm storing 5, its bound removed, the kind-1 arm routed through the `+0x6F0` store, the restore call removed, and the
claim "every variant switch restarts at subgroup 0". **Live: none.** **Not traced:**
- which units carry stats flag bit 2 in a loaded game (the set page's UQ-123 reads the authored bit from
  `battle_pack.bin` and does not re-check the loaded copy);
- what field bit 15 means for a given area;
- what `00308270` does besides the restore (the `+0x695` slot release `0030C970`, the `+0xDC8` / `+0xE58` refresh);
- who sets unit flag bit 22, and whether a selection can run on a suspended unit without it;
- whether any shipped script calls verb `3060` on a unit whose subgroup is non-zero.

### Crossings into other layers (FABLE, 2026-10-03)

*The edges this section's citations add, each with what crosses it.*

- **Items_Equipment_Shops_License and Rewards_Progression_Economy — SERVICE (3 edges).** The selector's field test
  `00377C20` (`FieldData_GetActiveFieldRecordBit15`) takes the active field id from `003148F0` (`00377C24`) and returns
  bit 15 of that field's 16-bit table word (`00377C42`–`00377C55`), or 0 when the table is null or the id is out of
  range (`00377C33`, `00377C39`, `00377C5F`). The inventory count query `00309FB0` (`0030A07A`), the unequip
  `0030FD10` (`0030FD5F`) and the defeat-rewards pass `00312280` (`00312382`) call the same getter.

  The selector reads a field bit that item and reward code also read. It is a shared getter, not shared ownership,
  and §8a states nothing about what those callers do with the bit.

## 9. Determinism

No RNG here — any randomness is inside the evaluation. The walk is a deterministic function of the
set, the subgroup, the unit's state and the resume context. No timing dependence and no
synchronisation.

## 10. Failure paths and edge conditions

1. Null order set → 0, nothing touched.
2. `subgroupIndex` 0 or 1 skips the summing loop; index 0 sums nothing and starts at record 0.
3. A subgroup whose count byte is zero walks nothing and returns 0.
4. A commit failure continues the walk (§7).
5. The subgroup index is **sign-extended** and never bounds-checked against the header, so a negative
   or oversized index reads count bytes outside the header.

## 11. Observable behaviour

Externally: which gambit line acts, and in particular a line whose condition holds while a lower line
acts instead — the signature of §7. In memory: the committed order's address appears in the action
context, which is what a later resume compares against.

## 12. Reproduction formula

§4 for the base, §6 for the resume tests, §7 for the two-call rule, in that order.

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-11)
~~Empty.~~ The shipped 422 bytes have been executed at
their real virtual address under Unicorn against an independent reconstruction.

**Instrument:** [`Reconstruction/Tests/Differential/diff_gambit_walk.py`](../../../Reconstruction/Tests/Differential/diff_gambit_walk.py)
against [`Reconstruction/Game/Combat/gambit_walk.c`](../../../Reconstruction/Game/Combat/gambit_walk.c).

**What is compared is the CALL TRACE, not the return value.** This operation returns `0` or `1` and
writes no memory of its own (§5), so a walk that tried the lines in the wrong order, or evaluated a
line it should have skipped, would return the same `1` on most inputs. The suite compares **the
sequence of records the walk offered to its callees**, with the target and parameter it passed —
`E3 C3 t1003 p203` — which is the behaviour this contract is actually about.

**What is supplied.** All three callees are hooked at their real addresses and answer from a
per-case script, identically on both sides: `003014C0` (876 B), `0030F760` (570 B) and the third
call `004697C0` (251 B). None of them is the subject, and driving both of their outcomes is the
only way to test §7's rule at all. Their bodies are deliberately **not** loaded — loading them
would quietly make them the subject.

**Result: 34 cases, 68 comparisons, 0 mismatches.** 24 return `1`, 30 offer at least one record,
and **11 offer more than one** — which is the number that matters, because a suite in which the
first line always acts never tests a walk.

| what was executed | outcome |
|---|---|
| §4's offset, at subgroup 0 and 1 (loop skipped), even and odd indices (pair loop and odd leftover) | **agrees** |
| §7's two-call rule, including match-then-commit-fails-then-a-later-line-succeeds | **agrees**; a reconstruction treating a match as a commitment is caught on **3** comparisons, one of them a differing return value |
| §6's three bits in all combinations, including mode-set-with-no-context | **agrees** |
| §6's resume point, context pointer planted equal to a record address | **agrees**; the trace stops before that record and contains no evaluate for it |
| all five of §10, including the sign-extended negative index reading a count byte from in front of the header | **agrees** |
| the count byte re-read (§4) | **agrees**; shortening it mid-walk stops the original early and lengthening it makes it continue, and a latched reconstruction is caught on **2** comparisons |
| the third call (§7) | **agrees**; a reconstruction omitting it is caught on **1** comparison — on the trace only, since the return value is identical |

### 13a. The walk, the evaluator and the notify, executed — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-095)

EXP-095 ran `00305CC0`, `003014C0` and `004697C0` from shipped bytes — **35/35 cases, 14/14 mutants,
two processes**. The scripted-callee caveat above is retired. `0030F760` stays scripted here per
EXP-091 and `00301AD0` is scripted per slot, both disclosed by the experiment.

**Finding 4's correction is to the experiment's own reading, not to this contract**, and that is
recorded rather than absorbed: §6 already reads `0x40` as *"evaluate this order even while
resuming"* and `0x80` as *"skip this order when in resume mode"*, at `00305DB2` and `00305DBC`, and
already says the two are tested against different conditions. Re-read here: `00305DAD test r15, r15`
/ `je` skips the `0x40` test entirely unless resuming, and `00305DB8 test ebp, ebp` / `je` skips the
`0x80` test unless the mode is set. Unchanged.

#### The roll gate, which is new here and holds exactly

`00301830`'s condition arm (`AiOrder_CheckActionPreconditions`, 670 B):

```asm
0030193B  test ebp, ebp          ; chance
0030193D  je   0x301964          ; chance == 0 -> match, unconditionally
0030193F  call 00328370          ; roll
00301944  ...                    ; roll % 100, by the 0x51EB851F magic-number division
0030195F  cmp  r8d, ebp
00301962  jge  0x301969          ; roll%100 >= chance -> no match
00301964  mov  edi, 1            ; match
```

**`chance == 0` is an unconditional match, and otherwise ~~the order~~ an order that reaches this arm fires iff `roll % 100 < chance`.** *(corrected 2026-10-02, OPUS: the arm is reached only by `0x4051`–`0x4121` other than `0x4091` (`00301917`–`00301935`) and by `0x414B` (`00301A1B`–`00301A21`); every other order id takes an arm without a draw — the wait `0x4021` and the rest up to `0x4050`, `0x4091`, `0x4122`–`0x4123` and most ids above `0x4124` return 1 at `00301A31`, `0x4022`, `0x4124` and `0x4165` decode a goal, `0x414D` reads the stance — and an action-row id is rolled instead in `003014C0` at `00301608`–`00301637`, so one evaluation draws at most one percent roll)*
*The division truncates toward zero and the comparison is signed, so a negative roll would match any
non-zero chance; EXP-095 describes the generator as folding 30 bits of state, which would keep the
value non-negative — so the signedness is unobservable rather than harmless, and a reimplementation
using an unsigned remainder agrees only while that holds.*

#### Three things in finding 7 do not survive a read of the image

The finding's headline is right and it is the important half: **the old "only `0x4086`–`0x408D`
nonzero" static reading was wrong.** Read from the shipped `.data`, **341 of the 359 entries are
non-zero**. The details around it differ:

| finding 7 | read from the image |
|---|---|
| table at `0x1ED0460` | **`0x01EEC460`** — `003018F0 lea rcx, [rip + 0x1beab69]`, next instruction `003018F7` |
| covers `0x4000`–`0x4167`; `≥ 0x4168` returns 0 | **`0x4000`–`0x4166`** — `003018DD lea eax, [rdx - 0x4000]` / `003018E3 cmp eax, 0x166` / `ja`, so `0x4167` is already out |
| holes `0x4038`–`0x4047` and `0x4128`–`0x412F` | **zero ENTRIES at `0x4025`, `0x4036`–`0x4045`, `0x4128`** — 18 of 359 |

Entries are **qwords**, `[rcx + rax*8]`, tested against zero at `003018F7`.

**The hole lists are not measuring the same thing ~~and neither side can settle it alone~~; the image settles the table** *(corrected 2026-10-02, OPUS: `01EEC460` re-read whole, below)*. EXP-095
probed *returns*, and a spec can return 0 without its entry being zero — the ladder immediately below
the table test (`00301901`–`00301935`) routes `0x4124`, `0x4022`, `≤ 0x4050`, `0x4091` and
`≥ 0x4122` to other arms, ~~which plausibly accounts for `0x4129`–`0x412F` answering 0 with non-zero~~
~~entries.~~ but `00301830` returns 1 for `0x4129`–`0x412F` (`00301A1B`–`00301A36`: above `0x4124` only `0x414B`, `0x414D` and `0x4165` go elsewhere), so the ladder does not account for the finding's second hole either *(corrected 2026-10-02, OPUS: all 359 qwords at `01EEC460` re-read — the 18 zero entries are exactly `0x4025`, `0x4036`–`0x4045` and `0x4128`; `0x4046`/`0x4047` hold `002FDDA0` and `0x4129`–`0x412F` hold `002FDC30`)*. **What that does not explain is the two-id shift on the first run**: `0x4036` and `0x4037`
hold zero entries here and the finding reports them populated, while `0x4046` and `0x4047` hold
non-zero entries and the finding reports them as holes. Routed to the experiment's author rather than
resolved here, because the probe's per-id returns are in its trace and not in this image read.

### What this does NOT show

- ~~**No evaluation and no commit ran.**~~ *(answered: the evaluator `003014C0` ran from shipped bytes in EXP-095, §13a, its selector `00301AD0` scripted per slot, and the commit in `commit_walk.py`, §7's 2026-09-26 correction; 2026-10-02, OPUS)* Nothing here says which gambits would fire in a real
  battle, only that the walk offers the right lines in the right order given answers.
- ~~**The `02089340` bit-5 suspension (§4a) was not driven.** It sits inside~~
  ~~`AiOrder_EvaluateAndResolveActionTarget`, which is supplied here, so this run says nothing about~~
  ~~it.~~ *(answered: driven by execution 2026-09-26, case G4 — §4a's correction; 2026-10-02, OPUS)*
- **`004697C0` is unidentified, but it is no longer unconnected.** *(Falsification pass 1,
  2026-09-12.)* It **calls `0046AB10`** — the function
  [the status write](../10-Status-Periodic-Terminal/CONTRACT-status-write.md)'s **`SW-4`** is already
  about — and its **three callers are the whole action lifecycle**:
  `00305CC0 BattleUnit_TrySelectAndCommitAiOrderFromSet` (this contract),
  `00307BE0 BattleUnit_AdvanceActionState` and
  `0030AF30 BattleAction_CheckAndHandleExecutionTimeout`. Its own body gates on a mode (`cmp esi, 4`),
  an id bound (`mov ecx, 0x21F` / `cmp bp, cx` / `jae`) and a specific id `0x4022`, after zeroing a
  `0x30`-byte local. **What the posted event means is still unknown** — that is `SW-4`, and this
  changes it from two unrelated unknowns into one.
- **`004697C0` is unidentified.** 251 bytes, not read for this contract. Its arguments are known
  exactly; what it does with them is not.
- **Nobody has observed a real evaluator or commit writing the subgroup's count byte.** The walk
  would follow it; whether anything does is live-only.

### What is still owed, and it is live-only

1. **Does anything write the count byte during a walk?** A watchpoint on `set + subgroupIndex`
   across one battle. Blocks: whether the re-read is a live behaviour or only a latent one.
2. **What is `004697C0`?** Static reading would answer it; it is out of this package's scope
   rather than blocked.
3. **Which line acts, in play, when a higher line's condition holds.** The §7 signature, observed
   rather than constructed.

Queued; the live-automation pause stands.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**38 generated points: 37 KILLED · 0 SURVIVED · 1 EQUIVALENT · 0 NO_BUILD · 0 TIMEOUT · 0 INVALID. Verdict `PASS`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/gambit_walk3` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**This campaign PASSES with zero survivors**, and it is the only one here that does. Three mutants of the same shape had survived — `mask` → `mask | 1` on `ctx->flags & 0x4000`, `record[4] & 0x40` and `& 0x80` — because every case drove those words with ONLY the tested bit set, so a mask that also accepts bit 0 behaved identically in all of them. Cases that set bit 0 while leaving the tested bit clear kill all three, and they establish something this contract asserts throughout and nothing had checked: **each gate reads exactly the bit it names and ignores the rest of the word.**

## 14. Unresolved

1. ~~**How many of the 32 header bytes are counts.**~~ — **answered 2026-09-22 (SWE2-CONTRACT), owner-side:**
   **at most twelve — bytes `0..0x0B`** — and the bound is proven from the writers, not assumed from the
   command list. `subgroupIndex` reaches the walk only as `r8d`, and the walk's sole caller is
   `00305AB0` (four sites): three pass `xor r8d, r8d` outright (`00305B9F`, `00305C14`, `00305C6B`)
   and the fourth passes `movzx r8d, byte ptr [rbx+0x6B5]` (`00305C34`). The `+0x6B5` byte has an
   image-wide toucher census of exactly four instructions: `00236BA3` and `002FE09F` store `0`
   (`al` is `xor`'d at `00236B10`; the second is an immediate), `002FE0BB` stores `dl - 0x16` on the
   direct-command arm `0x4116`–`0x4121` giving `0..11`, and `00305C34` is the read itself. No writer
   can produce a value above 11, so the walk never indexes header bytes `0x0C..0x1F` — they are not
   counts, only reserved tail. Corollaries, both verified: on the rebuilt sets at
   `02089378 + statsIndex*0x170` the header is **byte 0 only** — `00327F60`, `0032810B` and the
   `00328140` twin each store `set[0] = record count` and nothing else, and the array sits in
   `.data`'s uninitialized tail so bytes 1–31 are born zero and stay zero (rebuilt sets are flat:
   every order lands in subgroup 0). Multi-subgroup headers arrive only through the authored sets —
   the `002FE025` arm (`0x4112`–`0x4115`) resolves `+0x6E0` through `0020E600` from the unit's
   `+0x0E60` table, and authored bytes `0x0C..0x1F` are whatever the file carried, still unread.
   The walk itself does not enforce this — §10.5's "oversized index reads outside the header" stays
   true; what this adds is that **no shipped code path can produce such an index**.
2. ~~**What the remaining bits of `record + 0x04` do** — only `0x40` and `0x80` are read here.~~ —
   **answered 2026-09-22 (SWE2-CONTRACT): all sixteen bits are accounted for** by the sibling page's
   Z-19 census over the 50,050 shipped order records, owner-verified at the readers: `0x08`/`0x10`/
   `0x20` are a shifted test `0x20 >> i` in the evaluator (`003016BE movzx edx, word [r14+4]` /
   `003016C3 mov eax, 0x20` / `sar eax, cl` / `test edx, eax`), one bit per target-selector entry —
   keep the intermediate candidate set; `0x100`/`0x200` are locomotion flags read off the *current*
   record via `unit+0x708` (`00325CAA` / `00325C83` `test word [rax+4]`, writing `+0x170` bits 1/0);
   `0x400` sets an evaluator mode word for non-party units (`00301B79`–`00301BA2`); `0x800` is
   no-re-issue-while-current (`00301587 mov eax, 0x800` feeding `003015A6 test word [r14+4], ax`,
   gated on `r14 == [rdi+0x738]`); `0x1000` is retry-after-cancel (`00301B47`–`00301B74`, compared
   against `+0x744`); `0x2000` skips the execution-timeout check while current (`002FFCB1 test word
   [rax+4], 0x2000`); `0x4000` is the resumable bit the walk itself reads (`00305D74`–`00305D84`).
   `0x0004` is authored but ~~has no reader~~ is read by the navigation gate `00325D90` at `00325DF4` *(answered: see the gambit page's section 8g table, corrected 2026-10-01; 2026-10-02, OPUS)*, and `0x0001`/`0x0002`/`0x8000` are never set in shipped
   data. **The word is not "two resume bits plus unknown" — it is the record's whole behaviour
   flags word, consumed by four different functions.**
3. ~~**What makes a commit fail**~~ — **answered**, in
   [`../07-Combat-Action/CONTRACT-commit-action.md`](../07-Combat-Action/CONTRACT-commit-action.md) §3:
   the action id must fall in one of two bands, `<= 0x21E` or `0x4000..0x4166`, and an id outside both
   is refused with the commitment untouched. Note that the optional cancel runs *before* that test, so
   a refused commit can still have cancelled the previous action — which means a gambit line that
   fails to commit is not always inert.

## 15. Evidence

> **The tier column was reworded 2026-09-11.** Seven rows read *"static, isolated original code"*
> while §13 read *"Empty"*, which is only consistent if "isolated original code" meant *the shipped
> bytes, read* — and it did. Now that the bytes have actually been **run**, that label means two
> different things in the same table, so the column now distinguishes **`static`** (decoded) from
> **`executed`** (run and compared against a reconstruction). No row's confidence changes; the
> ambiguity was in the label, not in the evidence.

| claim | evidence | tier | confidence |
|---|---|---|---|
| null set returns 0 | `00305CF2 test rdx, rdx / jne` then `00305CF7 xor eax, eax / ret` | 1 (static + **executed**) | PROVEN |
| the action slot starts at `0xFFFF` and the target slot starts at 0 | `00305CCF mov ecx, 0xffff` / `00305CD6 mov word ptr [rsp+0x70], cx`; `00305CDE mov dword ptr [rsp+0x30], edi` with `edi = 0`. *Relabelled 2026-09-26 (OPUS): this row said "the no-target sentinel is `0xFFFF` and the parameter slot starts at 0"; the evaluator writes the decoded action id into `[rsp+0x70]` (`00301500`) and the target id into `[rsp+0x30]` (`003017E7`), §7* | 1 (static + **executed**; the real evaluator writing both, `commit_walk.py` W2/W3) | PROVEN |
| the header is per-subgroup count bytes | `00305D30`/`00305D37` byte reads with `add rcx, 2`, leftover at `00305D4E` | 1 (static + **executed**) | PROVEN |
| records begin at `+0x20`, stride 24 | `00305D93 lea rbx, [r10 + 0x20]`, `00305D67 lea rcx, [rax + rax*2]`, `00305D97 lea rbx, [rbx + rcx*8]` | 1 (static + **executed**) | PROVEN |
| an empty subgroup walks nothing | `00305D89 cmp byte ptr [r11 + r10], dil / jbe` | 1 (static + **executed**, and the trace is empty rather than merely the return being 0) | PROVEN |
| the count byte is re-read on every iteration | `00305DFD movzx eax, byte ptr [r12]`, inside the loop body | 1 (static + **executed** in both directions; a latched reconstruction fails on 2 comparisons) | PROVEN |
| the two record resume bits are tested against different conditions | `00305DAD`–`00305DC0`: `0x40` only when `resuming`, `0x80` whenever `resume_mode` | 1 (static + **executed**, including mode-set-with-no-context, which is the case that separates them) | PROVEN |
| reaching the resume point returns 1 without evaluating it | `00305DA4 cmp r14, rbx / je` | 1 (static + **executed** with the context pointer planted equal to a record address) | PROVEN |
| both the evaluation and the commit must succeed | `00305DD2`/`00305DD7` then `00305DF4`/`00305DF9` | 1 (static + **executed**; a match-is-commitment reconstruction fails on 3 comparisons) | PROVEN |
| there is a third call on the success path | `00305E31`–`00305E5A`, gated on resume mode and on the latched `unit+0x714` not being `0xFFFF` | 1 (static + **executed**; omitting it fails on the trace only) | PROVEN |
| the subgroup index is sign-extended and never bounds-checked | `00305CCC movsxd rax, r8d` with no compare against the header | 1 (static + **executed**, with a negative index reading a planted byte in front of the header) | PROVEN |
| at most twelve header bytes are counts; `subgroupIndex` cannot exceed 11 | `+0x6B5` writer census — four touchers: `00236BA3`/`002FE09F` store 0, `002FE0BB` stores `(id&0xFF)-0x16` ∈ 0–11, `00305C34` reads; sole walk caller `00305AB0` passes `r8d=0` on three of four sites | 1 (static) | PROVEN |
| `record + 0x04` is the record's whole behaviour flags word — every shipped bit has a named reader | Z-19 census over 50,050 authored records, owner-verified at `003016BE`, `00301587`/`003015A6`, `00301B47`, `00301B79`, `00325C83`/`00325CAA`, `002FFCB1`, `00305D74`; ~~`0x0004` unread~~ `0x0004` read at `00325DF4` *(answered: the gambit page's section 8g table; 2026-10-02, OPUS)*, `0x0001`/`0x0002`/`0x8000` never set | 1 (static; readers outside the walk are not replayed) | PROVEN |
| what `004697C0` does | **not established** — 251 bytes, not read for this contract | none | UNKNOWN |
| nothing observed live | — | none | — |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

**Checked at the instructions, and every claim holds.**

| claim | what the bytes say |
|---|---|
| the subgroup index is sign-extended and never bounds-checked | `00305CCC movsxd rax, r8d`, and the only test on it is `00305D24 cmp rax, 2` / `jl` — a **lower** test that decides whether to sum earlier subgroup counts, **not a bound** |
| the count byte is re-read on every iteration | `00305DFD movzx eax, byte ptr [r12]` / `00305E08 cmp edi, eax` / `00305E0A jl 0x305DA0` — a **load at the bottom of the loop**, not hoisted |
| the two record resume bits are tested against different conditions | `00305DB2 test byte ptr [rbx+4], **0x40**` and `00305DBC test byte ptr [rbx+4], **0x80**` — the same byte, two bits, each reached under its own preceding `test ebp, ebp` |
| there is a third call on the success path | three, and only three: `00305DD2 call 0x3014C0`, `00305DF4 call 0x30F760`, `00305E5A call 0x4697C0` |

### The unidentified callee is no longer unconnected

`004697C0` **calls `0046AB10`**, which is exactly the function
[the status write](../10-Status-Periodic-Terminal/CONTRACT-status-write.md)'s `SW-4` asks about. And
its three callers are the whole action lifecycle — AI order selection, action-state advance, and
execution timeout.

> **This answers neither question.** What the posted event *means* is still `SW-4`, and what
> `004697C0` is *for* is still §14. **What it does is stop them being two unknowns.** Two contracts
> were each carrying an open question about the same posting path without knowing the other existed.

**Mechanical:** no body-size drift; banned-evidence sweep clean; `00305CC0` resolves at 422 bytes.

## 16. Parity plan

`CONTRACT` — a subgroup whose first line's condition holds but whose commit fails must act on the
second line.
`STATE-TRANSITION` — resume with the context pointing at the third order and assert lines one and two
are skipped without evaluation.
`EDGE-CASE` — a subgroup with a zero count byte must do nothing; `subgroupIndex` 0 must start at
record 0.

**All three are done** — see §13. Per-dimension verdicts are declared by the harness and generated
into [`PARITY-STATUS.md`](../_index/PARITY-STATUS.md): `CALCULATION`, `STATE-TRANSITION`,
`EDGE-CASE` covered; ~~and **`CONTRACT`**~~ — **amended 2026-09-22:** `CONTRACT` was covered while
every testable §15 row was exercised (11 of 13; the first pilot in the tree to reach that), and the
two rows added for §14 items 1–2 — the header-byte bound and the `record+0x04` bit census — are
provable only by writer census and cross-function reads, which a walk replay cannot drive. It now
reads 11 of 13 testable exercised, honestly `NOT COVERED`. `INTEGRATION` and `FULL-SUBSYSTEM` are
not covered. ~~because all three callees are scripted~~
**They ran as shipped bytes on 2026-09-18 (§13a)** — what keeps those two dimensions uncovered is that
the enmity input and the `02089340` suspension are outside this operation, and that the run is on
hand-built fixtures rather than in a battle.

**Four things a reimplementer must take from this contract that the old plan did not name:**

1. **Implement the third call.** Success path, resume mode non-zero, `unit + 0x714` not `0xFFFF`.
   Omitting it changes nothing a return value can show, and drops a notification on every resumed
   commit.
2. **Re-read the count byte each iteration.** Reading it once before the loop is the obvious way to
   write this and it is not what the original does.
3. **`resuming` is not `resume_mode`.** The `0x40` test needs a context carrying `0x4000`; the
   `0x80` test needs only the mode. Collapsing them is invisible on most inputs.
4. **Do not add the bounds check.** The subgroup index is sign-extended and unchecked, and a
   negative index really does read a count byte from in front of the header. Whether to reproduce
   that is a deliberate decision — reproducing it is faithful, refusing it is a divergence, and
   either is fine as long as it is recorded as one.

## 17. Related

- `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` — the page this formalises.
- `07-Combat-Action/CONTRACT-battle-target-buffer.md` and
  `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md` — the rest of the chain in §8.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

The walk's three supplied callees and §4a's bit-5 writers have edges into five other layers. None of the edges changes
the walk's rule; each is a service the callee uses. The edges come from `edges.tsv`, and the roles below are the
ledger names unless a call site is given.

- **ActorEntity.**
  - `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) turns actor work into a battle unit through
    `ActorWork_GetBattleUnit`.
  - `BattleUnit_CommitAction` (`0030F760`) walks the unit table through `BattleUnit_GetBySlotIndex` and
    `BattleUnit_GetSlotCount`.
  - §4a's writers are actor-sequence code. The starter `00359A30` and the second starter `0035AB20` both call a helper
    that reaches `ActorManager_GetRecordByOrdinal` and `Actor_StopRequestedMovement`. The
    first starter also encodes an actor handle (`ActorHandle_EncodeRegistryEntry`) and reads the 32-byte manager
    accessor the render cluster uses.
  - **The one clearer, `0035A6F0`, has three raw callers**, a thunk and two bodies. One of those bodies is the area unload
    that [the actor manager record](../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md)
    describes. So the suspension bit is also dropped when an area unloads, not only when a sequence ends. Whether any sequence can
    still be running at that point is not read.
- **Gameplay.** Both supplied callees own the battle target buffer. `003014C0` resets it
  (`BattleTargetBuffer_ResetPreservingFlag0`) and reads `WorldActor_GetDefinitionByte12OrMinus1`. `0030F760` resets it
  and appends to it (`BattleTargetBuffer_TryAppendActorWork`).
- **Party.** `0030F760` resolves the party focus handle through `BattleUnit_ResolveByFocusHandle`.
- **CoreRuntimeScheduling and Movement.** `004697C0` calls `0046AB10`, the battle event poster. That poster stamps
  with `GameClock_GetRawTickCounter` and resolves its message table through `ImageAddress_ResolveRuntimePointer`.
  **Eighteen** bodies in the `00469xxx`–`0046Axxx` range post through it (48 raw call sites). One of them is filed
  under Movement, and that one also reads
  `BattleUnit_GetPartyLeader`. These are the poster's other clients, not the walk's.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — SERVICE.** `0030AF30` on this page calls `FUN_00290540`, owned by that layer. What it reaches is an 80-byte step over the HUD object at `[0209BE80] + 0x10F78`, which it skips when that slot is empty; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-46 update (2026-09-19) - `00359A30`

`00359A30` (223 B) is the actor-sequence starter - `00238AE0`/`00238B70`/`0025AB30`/`00263C30`/`002647B0`/`002E63D0`/`002E6570`. Interior anchor `00359A40` (a `00238AE0` call).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Presentation — CLIENT, eight edges.**
- The actor-sequence helper `00263C30` (reached from the sequence starter `00359A30`) has five presentation callers:
  `00256F60`, `003A4290`, `003A56F0`, `00465120` and one more.
- The walk's own bodies consult presentation-filed helpers:
  - `AiOrder_CheckActionPreconditions` → `BattleUnit_ComputePartyBattleStance`;
  - `AiOrder_EvaluateTargetSelector` → `BattleUnit_TestActorViewFrustumAtCurrentPosition`;
  - `BattleUnit_CommitAction` → `BattleUnit_BroadcastPartyCombatTargetRelation`.

**Spawn_Encounter_Lifecycle — BOTH DIRECTIONS, seven edges.**
- `SpawnGroup_RecordMemberDeathAndHandleCompletion` sets the AI-suspend and presentation-veto bits through
  `00238B70` / `00238AE0`. Those are the bits this walk checks (§5, and `CONTRACT-hp-write-and-lethal-transition`
  §9 step 5).
- The shared generator `RNG_SharedGameplayLCG_NextU32` has five spawn callers: placement, candidate selection,
  authored-region positions and the keep initialiser.

**Script_VM_Native_Bridge — CLIENT, six edges.**
- The bit clearer `0035A6F0` and the starter `0035AB20` are reached from script through their thunks (`003574B0`,
  `00356970`).
- `0033F330` calls `0025AB30`, and `0034AF50` calls `00263C30`.

**WorldAreaField — DEPENDENCY, six edges.** `AiOrder_EvaluateTargetSelector`, `AiOrder_EvaluateAndResolveActionTarget`,
`BattleAction_CheckActionAvailabilityReason`, `BattleUnit_SelectAndCommitNextAction` and `BattleUnit_CommitAction`
read `FieldData_GetActiveFieldRecordBit15`, and the selector also reads `FieldData_GetFormat0RecordVectorByIndex`.

**RNG_Random_Selection — SERVICE, five edges.** Target resolution and the precondition roll draw
`RNG_SharedGameplayLCG_NextU32`, directly and through `BattleData_ResolveWeightedId`, as mapped in
`which-roll-is-on-which-generator`.

**CombatFormula — BOTH DIRECTIONS, two edges.** `0046AB10` (the status write's `SW-4` function) is called by
`BattleFormula_DispatchPostResultEvents` and calls `BattleStats_FindOwningBattleUnit`.

**Input — MECHANICAL, one edge.** `00226BE0` calls the sequence helper `002647B0`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 debt `42a617a9a`).*
