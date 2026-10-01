---
system: The shape of the script verb population — 1,224 handlers, classified
category: 01-Script-VM-Native-Bridge
status: AUDITED
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 1
level: L1
readiness: CLASSIFIED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 23 addresses cited - 1 data, 12 entry, 10 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-verb-population-pass-1
  crossref_clean: true
  reopened_count: 0
function_families:
  - "ScriptVM.VerbAdapter | B | members/scriptvm-verb-adapter-callbacks.tsv | 1030 | registered begin/poll/result callback read from the five image tables; decoded body is operand pops + at most one native + result write/push, no loop; per-member verb id/name/role/native in the TSV (select_verb_adapters.py). 4 member(s) left the family 2026-09-18, since measured as A (A beats a declaration): 0016D6A0, 0050F810, 0053DD10, 005C5230. 3 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 00347E00, 00356BC0, 00356FD0 10 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. Re-running select_verb_adapters.py drops exactly these; it would also admit 2 frontier callbacks that now pass the rule - not added: new membership awaits adjudication (selector-drift.tsv in the same record). 2026-09-29, FABLE family ruling R3 (SWE2-EC7): the 2 frontier callbacks are applied - the re-run adds exactly them and removes none; the leftovers file is regenerated with it (11 rows left the leftover set: 8 since measured A, 3 declared by other families); record _index/candidates/ec7-family-ruling-exec-0929. 2 member(s) left the family 2026-09-30, since measured as A (A beats a declaration) by FABLE's pass-22 publish 4407f8484: removed by re-running select_verb_adapters.py, which drops exactly these two (and one A entry from the leftovers file) and admits nothing (SWE2-EC7). 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 2 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the version-stamps page (8c8406bfd) and the source-block mover page (9bda44687) DOCUMENTED; select_verb_adapters.py re-run on a clean HEAD export drops exactly these two, admits nothing and leaves the leftovers file's membership unchanged; addresses and causing pages in the record. 2026-10-01 (OPUS for SWE2-EC7, A-drift round 5, record _index/candidates/opus-adrift-round5-1001): 2 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the capability-inhibition policy (eef738450) and the gambit evaluation page (95cf8c42f) DOCUMENTED; select_verb_adapters.py re-run on a clean HEAD export drops exactly these two, admits nothing and leaves the leftovers file unchanged; addresses and causing pages in the record. 2026-10-01 (OPUS for SWE2-EC7, A-drift paired with owner re-status batch 20, record _index/candidates/opus-dd-restatus-20-1001): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the battle-record kind page DOCUMENTED (owner batch 20); exact A removal in the same publish (selector not re-run); addresses and causing pages in the record. 2026-10-01 (OPUS for SWE2-EC7, A-drift paired with the native-command-lifecycle page's re-status, record _index/candidates/opus-dd-restatus-23-1001): 2 member(s) left the family, since measured as A (A beats a declaration) after the native-command-lifecycle page's re-status (batch 23); exact A removal in the same publish; addresses and causing pages in the record."
---

# The shape of the script verb population

## 1. What the player sees

Everything scripted. Every cutscene beat, every quest flag, every door that opens when you talk to
somebody, every chest that appears after a boss — a zone script calls a **verb**, and a native
function runs it. There are **1,224** of them.

**Most of those functions do almost nothing.** They pop one number off the script's argument stack
and hand it to somebody else. This document measures exactly how many, so that the ones that
*do* something can be found.

## 2. Why a census instead of 1,224 documents

`knowledge_db.py query script-verbs-undocumented` reports **1,158 of 1,224** verbs whose handler no
document cites. Reading them one at a time is not a plan. The charter's completion disposition **B**
is *a proven member of an understood family, with the shape, the enumeration method and a
reproducible count stated* — and this is the enumeration method.

`script_verb_shapes.py` disassembles every handler from its entry and cuts the population on
**control flow**, because that is what decides whether a handler can be reimplemented by reading it
once.

## 3. The census

**1,224 verbs → 1,166 distinct handlers** (58 verbs share a handler with another verb).

> **These are the corrected numbers, regenerated 2026-09-13 (OPUS).** `script_verb_shapes.py`
> now cuts each handler at the end of its real body, taking the cut from the adjudicated
> [`FUNCTION-EXTENT-ERRATA.tsv`](../../_index/FUNCTION-EXTENT-ERRATA.tsv). **Ten of the 1,166
> handlers had an extent that ran into the next function; four of them were classified on a
> call that is not theirs.** §7 lists all four. `CONST`, `BRANCHING` and **the 993 / 85.2 %
> headline are unchanged** — every move is inside the non-branching set.

| family | rule | handlers | share | verbs |
|---|---|---:|---:|---:|
| `CONST` | no call, no jump, no memory operand | 1 | 0.1 % | 7 |
| `TAILJUMP` | no call; one unconditional `jmp` | 145 | 12.4 % | 161 |
| `CALL1` | exactly one direct call | 399 | 34.2 % | 423 |
| `LINEAR` | several calls, **still no branching** | 448 | 38.4 % | 456 |
| `BRANCHING` | **has a conditional branch of its own** | 173 | 14.8 % | 177 |
| unclassified | did not decode | **0** | — | 0 |

> **Superseded, kept so the change is legible:** before the extent cut this table read
> `TAILJUMP` **141 / 12.1 % / 157**, `CALL1` **402 / 34.5 % / 426**, `LINEAR`
> **449 / 38.5 % / 457**. Those rows counted instructions belonging to a neighbouring function.
> `script_verb_shapes.py --no-errata` reproduces them exactly, which is the control that the
> difference is the extent and nothing else.

> **The rules are tested in this order, and the order is load-bearing** (added 2026-09-13,
> §7): `CONST`, `TAILJUMP`, **`BRANCHING`**, `CALL1`, `LINEAR`. Read in the order the table
> prints them — `CALL1` before `BRANCHING` — **24 handlers move out of `BRANCHING` into
> `CALL1`**: they have exactly one direct call *and* a conditional branch, so `BRANCHING`
> reads **149** instead of 173. A census whose value is that anyone can re-run it has to say
> which test wins.

> ### 993 of 1,166 handlers — 85.2 % — contain no conditional branch at all
>
> **Their entire behaviour is the call chain**, readable in one pass. That is disposition **B** for
> 85 % of the script bridge, with a rule anyone can re-run.
>
> **173 handlers (14.8 %) branch.** Those are disposition **D** — each needs reading, and they are
> the real remaining work in this category. **The value of the census is that it names them**: the
> per-verb table is [`scriptvm-verb-shapes.tsv`](scriptvm-verb-shapes.tsv).

### The first taxonomy was wrong and its own numbers said so

A first cut used call and jump counts — `CONST`, `TAILJUMP`, `CALL1`, `GLOBAL` — and dropped
**53 % of the population into `OTHER`**, including `setvelr` and `sin`, which are plainly
straight-line wrappers with two calls each.

> **A taxonomy that cannot classify half its population is measuring the taxonomy, not the
> population.** Recutting on "does it branch at all" took `OTHER` from 621 to **0**.

## 4. Where the wrappers go

Of the **584** verbs whose handler is a single call or a bare tail-jump, the targets are not spread
out at all:

| target | verbs | cumulative |
|---|---:|---:|
| `00267E10` | **238** | 40.8 % |
| `00267DB0` | 37 | 47.1 % |
| `00267F90` | 15 | 49.7 % |
| `002640C0` | 12 | 51.7 % |
| `0026B4E0` | 11 | 53.6 % |
| *…234 distinct targets in all* | | |

**The top ten targets absorb 330 of 584 (56.5 %).**

> **Regenerated 2026-09-13 from bodies cut at the real boundary (§7).** Two of the former 240 and
> one of the former 38 were calls belonging to the **next** function. The family gains a verb —
> `moveblurcaptureonce` was a `LINEAR` row that is really a tail-jump — so the denominator is
> **584**, and the four corrected handlers tail-jump to targets the old rows never named, which is
> why the distinct-target count *rises* to 234 while the top two fall.
>
> **Superseded:** `00267E10` **240**, `00267DB0` **38**, **232** distinct targets, top ten
> **333 of 583, 57.1 %**.
>
> **A correction of my own, recorded rather than quietly fixed:** when this task was queued I
> *predicted* this section would read **233** distinct targets and **330 of 583, 56.6 %**. Measured
> against the regenerated file it is **234** and **330 of 584, 56.5 %** — the predicted target count
> was one low, and the predicted percentage still divided by the old denominator while the same
> paragraph said the denominator had changed. **A predicted correction is not a measured one.**

### What the top two are — prior art, quantified here for the first time

`00267E10` (78 B) and `00267DB0` (84 B) are the **typed argument-pop helpers**, already documented in
[the verb dispatch and parameter encoding](scriptvm-verb-dispatch-and-parameter-encoding.md) and
[the script-to-native calling convention](../Spawn-Verbs/the-script-to-native-calling-convention.md).
Both read the same frame:

```asm
00267E10  mov   eax, [rcx]                       ; the argument count
00267E16  test  eax, eax / jle -> return 0       ; empty stack yields 0
00267E1A  dec   eax / mov [rcx], eax             ; POP: the count is decremented in place
00267E21  movzx edx, byte ptr [r8 + rcx + 4]     ; the type byte for this slot
00267E2A  je    -> int   : return  dword [rcx + r8*4 + 0x184]
00267E42  je    -> float : return cvttss2si dword [rcx + r8*4 + 0x184]
00267E36  else           : 008620C0(1)           ; the type-error path
```

`00267DB0` is the same function returning `xmm0` instead of `eax` — **pop as float** rather than
**pop as int**.

> **The helpers are not new; the distribution is.** *"240 of 583 single-call verb handlers are
> nothing but an integer argument pop"* is a statement about the whole population that no
> per-function document could make, and it is what turns 1,158 unread functions into **one shape and
> a remainder**.

### The declared adapter family — 1,053 of the 1,682 frontier callbacks

`function_families` row **`ScriptVM.VerbAdapter`** (B) names the population this shape story
predicted: every function any of the five image verb tables registers as a **begin**, **poll** or
**result** callback whose decoded body is only operand pops, **at most one native call**, and a
result write/push — **no loop**. Membership is read from the tables themselves (records at
`table + 8 + 32*N`, callbacks at `+0x00` / `+0x08` / `+0x18`), never from a TSV; the selector is
[`members/select_verb_adapters.py`](members/select_verb_adapters.py) and the member list —
one row per callback with its verb id, verb name, role and native callee — is
[`members/scriptvm-verb-adapter-callbacks.tsv`](members/scriptvm-verb-adapter-callbacks.tsv).

The composition, measured on the bodies: **964** pop operands and call exactly one native,
**71** are pure stack/result plumbing with no native at all, and **18** end in a single
`_guard_check_icall` site — a CFG-guarded indirect call, which is the one native call slot whose
target lives in a register rather than the body.

The **629 frontier callbacks that fail the rule** are listed with the reason in
[`members/scriptvm-verb-adapter-leftovers.tsv`](members/scriptvm-verb-adapter-leftovers.tsv):
**590** reach two or more distinct natives (the `setpos` pattern — a flag picks between two
implementations, or a helper resolves a handle before the real call), **38** contain a loop, and
**1** has an unexplained indirect call. Those remain frontier — larger bodies are exactly the
functions worth a page of their own.

#### The marshalling grammar executed — `FABLE-REQ-SWE2-VERB-MARSHAL-B` (2026-09-16)

The strict subset FABLE's request calls the *marshalling adapters* — one non-VM call, operand
moves and constants only, no compare or branch at all — has now been **run, not just decoded**:
[`diff_verb_marshal.py`](../../../../Reconstruction/Tests/Differential/diff_verb_marshal.py)
re-derives the set from the image's five tables, executes **836** grammar members under Unicorn
with every inbound register and every popped slot carrying a distinct tag, and samples rcx /
rdx / r8 / r9 / xmm0–3 / the stack-argument slots at the native-call boundary. **All 836 agree
with the static derivation on native target, primitive sequence and result tail; zero
execution failures.** The population is a superset of FABLE's 683 frontier callbacks — the
other 153 are already dispositioned (683 of this family's members are in the executed set;
the rest were A-measured or declared elsewhere, including the six `PushInt32`-then-forward
variants `00342360` / `00342830` / `00345E70` / `00351B40` / `00351E50` / `0050D180`).

The per-member argument map execution produced is
[`members/scriptvm-verb-marshal-argmap.tsv`](members/scriptvm-verb-marshal-argmap.tsv): for
each member, the verb ids and role, the pop/push sequence with kinds, the native target, which
tag landed in each argument slot (`rcx-in(ctx)` passthrough, `pop#i` low-32 slots, constants),
and the result tail. Headline: `rdx` passes the resolved target actor through in 576 of 836,
`r9` forwards the value stack in 817, and popped slots most often land in `ecx`/`xmm0` — the
verb-to-native binding a ScriptVM reimplementation needs is now executed data, not inferred
grammar. Tails: `VMResult_WriteInt32` ×167, `WriteFloat32` ×17, none ×652.

## 5. The dispatch record has three handler slots, and the first import carried one

The record is 32 bytes and holds up to three code pointers. **CORRECTED 2026-09-19 (OPUS): the
record is based at `01EED708`, not `01EED720`, and the slots are begin `+0x00`, poll `+0x08`,
UNUSED `+0x10`, result `+0x18`.** The accessors decide it — `003DC270` reads begin at
`[tbl + 0x20n + 8]`, `003DC240` reads poll at `[tbl + 0x20n + 0x10]`, and `003DC2A0` reads result
at `[tbl + 0x20n + 0x20]` after an `inc rax`; **nothing reads `tbl + 0x20n + 0x18`**, which is the
record's `+0x10`. This page previously named that unread slot as the result, which would put a
reimplementation's result callback where the engine never looks. `0x01EED720` is **`result(0)`**. The import that brought this table into the database on
2026-09-08 took only the first, and **261 further mappings were sitting unread in a file this
database had just adopted**:

> ### The 2026-09-19 correction is right, and a P1 asking to revert it is DECLINED
>
> ***`FRONTIER-REQ-FABLE-DISPATCH-RECORD-SLOT-NAMES` answered 2026-09-22 (FABLE).*** The request
> asks for this section's names to begin `+0x00` / poll `+0x08` / **result `+0x10`**, on a record
> based at `0x01EED720`, reporting 1,496 records with non-null counts 1234 / 277 / 230 and `+0x18`
> sentinel-only. **Those figures reproduce exactly — I re-measured them rather than take them — and
> the conclusion still does not follow, because the base they are measured on is not the base the
> engine uses.** The section above stands unchanged.
>
> **The installer settles the table pointer.** `VMNativeCommandDispatch_Initialize` (`003DC2D0`)
> does `lea rax, [0x01EED700]` at `003DC2F0` and stores it at `003DC2F7` into the slot all three
> accessors load from. So the accessors' `rcx` **is** `0x01EED700`, and `[rcx]` — the bound in
> `cmp edx, dword ptr [rcx]` — is the count word `0x5D8` = 1,496.
>
> **The three accessors then fix the record base at `0x01EED708`, exactly as this section says.**
> `003DC270` reads `[rcx + 0x20n + 8]`, `003DC240` reads `[rcx + 0x20n + 0x10]`, and `003DC2A0`
> **increments the index first** (`003DC2BA inc rax`) and reads `[rcx + 0x20(n+1)]`. For those three
> to be fields of one record, the record must start at `rcx + 8` and run **across** the `0x20`
> boundary. That is `0x01EED708`, stride `0x20`, slots `+0x00` / `+0x08` / `+0x10` / `+0x18`.
>
> **And the occupancy is the falsification, because the right base makes the anomalies vanish.**
> Measured over exactly the 1,496 records the count word declares:
>
> | slot | non-null | in `.text` | on a function ENTRY |
> |---|---:|---:|---:|
> | `begin` `+0x00` | 277 | 277 | **277** |
> | `poll` `+0x08` | 230 | 230 | **230** |
> | `+0x10` — read by nothing | **0** | 0 | 0 |
> | `result` `+0x18` | 1234 | 1234 | **1234** |
>
> **Every non-null value is a function entry, and the unread slot is not merely unread — it is
> entirely zero in all 1,496 records.** On the requested base the same data gives 276 of 277 and 229
> of 230 "plausible" plus a stray `FFFFFFFF`: **those three strays are the terminator.** The block at
> `0x01EF9208`, one stride past the last record, is `FFFFFFFF FFFFFFFF FFFFFFFF` — an end marker
> **after** the array, which a base shifted by `0x18` pulls into the last record's fields. *A wrong
> base does not announce itself; it shows up as a handful of values that are nearly pointers.*
>
> **What the request is right about is that this page IS shifted by one — in §3 and §7, not here.**
> The dense column of 1,234 is `result`, not `begin`. See the two corrections below.

| slot, over the 1,224 NAMED call ids | non-null | on a function entry |
|---|---:|---:|
| `begin` `+0x00` | 122 | 121 |
| `poll` `+0x08` | 139 | 138 |

> ⚠ **Relabelled 2026-09-22 (FABLE), figures NOT re-measured.** These two rows are the same counts
> this section has always carried; only the slot names change, because `+0x08` and `+0x10` on the old
> base are `+0x00` and `+0x08` on the real one. **The `1,224`-subset figures themselves need
> regenerating** from the census script against record base `0x01EED708` — routed, not guessed, and
> the full-extent table above is the measured one.
>
> **The `FFFFFFFF` pair this table used to attribute to call id `05D7`** is the terminator described
> above, which is **past** the last record rather than in it.

Only the *begin* handler is classified in §3. **The 261 poll and result handlers are recorded and
unclassified** — `DO-1`.

> **`DO-1` under-states by 246 (2026-09-13, §7).** Both numbers above are counted over the
> **1,224 named** call ids, and they reproduce there exactly. But the table's own extent is
> **1,496** records — the figure §6 cites from
> [the dispatch table](../scriptvm-native-dispatch-table.md) — and the named ids are **sparse**
> inside `0001`…`05D7`, not a prefix: 116 gaps, the largest 28 wide. Over all 1,496 records the
> table holds **277 begin** and **230 poll** pointers, **507** in all, and **1,234** non-null
> **result** handlers. So **246 begin and poll handlers sit on records this census never sees**, and
> **ten records carry a result handler with no name in the authored catalog**.
>
> ⚠ **Slot names corrected 2026-09-22 (FABLE) — the counts are unchanged and were reproduced.**
> This note previously read "277 poll and 230 result … 1,234 begin", which is the same shift §5 now
> records. **The consequence is not cosmetic: the 1,234-strong column that §3 censuses is the
> `result` slot**, so §3's "1,224 verbs → 1,166 distinct handlers" is a census of **result**
> handlers, and `DO-1`'s "261 poll and result handlers recorded and unclassified" is **begin and
> poll**. *Renaming the census itself is not done here* — it is cited from other pages and from
> `script_verb_shapes.py`'s output, so it is routed rather than rewritten under a P1 that asked for
> something else. **What is established here is which displacement carries which callback, and that
> is now measured three ways: the installer, the three accessors, and an occupancy table with no
> anomalies.**


## 6. What this does not claim

- **Nothing about what any verb does.** A shape is not a semantic. `CALL1 -> 00267E10` says the
  handler pops an integer argument; it does not say what the verb then does with it, because in that
  family the handler *is* the whole thing and the effect lives in the caller.
- **That `LINEAR` handlers are trivial.** No branching makes a function readable in one pass; it does
  not make it short. The family spans 4 to 240 bytes.
- **That the verb names are right.** They come from an authored external catalog and are not
  verifiable against the image — see the per-column provenance in
  [`scriptvm-dispatch.tsv`](scriptvm-dispatch.tsv).
- ~~**That call id equals record index everywhere.** At least one discontinuity exists and its location
  is unknown — `I-6`, inherited from
  [the dispatch table](../scriptvm-native-dispatch-table.md).~~ **CORRECTED (propagated 2026-09-11, ASTRA-REQ-FABLE-STALE-I6-AY10):**
  `I-6` was **closed 2026-09-07** — `record N = verb N` holds across all 1,496 family-0 records,
  tested on 645 independent anchors against a measured shifted baseline
  ([the dispatch table](../scriptvm-native-dispatch-table.md) §15–§16). Call id equals record
  index everywhere in the family-0 table; this page's tables can be read on that basis.
  Kept struck here because the page's prose was written while the question was open.

## 7. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment. It returned
`BQ-8`, which already establishes that `00267DB0` returns a float on all four exit paths — §4's
reading of it as *pop as float* is consistent with the register, and is not restated here as new.)*

### Everything in §§3–5 reproduces from the image

Not from the `.tsv`: the census was re-run by disassembling every handler out of the shipped
executable and re-applying the stated rules.

| claim | measured |
|---|---|
| 1,224 verbs → 1,166 distinct handlers | **1,224 / 1,166** |
| `CONST` 1 / 7 … `BRANCHING` 173 / 177 | every family reproduces — see the precedence note below |
| 583 single-call or bare-tail-jump verbs, **232** distinct targets | **583 / 232** |
| `00267E10` 240, `00267DB0` 38, `00267F90` 15, `002640C0` 12, `0026B4E0` 11 | **240, 38, 15, 12, 11** |
| top ten absorb 333 of 583 = 57.1 % | **333 / 583 = 57.1 %** |
| poll `+0x08` 122 non-null, 121 on a function entry | **122 / 121** |
| result `+0x10` 139 non-null, 138 on a function entry | **139 / 138** |
| the two that are neither are both on call id `05D7` and hold `FFFFFFFF` | **both, and `05D7` is the last record of the extent** |

And a check the page does not make: **all 1,224 handler addresses in the `.tsv` equal the pointer
at `01EED720 + 32 × id`** — 0 disagreements.

> **The measurement stands; the conclusion drawn from it did not. CORRECTED 2026-09-19 (OPUS).**
> The original text read *"the table's own `+0x00` pointer … the record layout, the stride and the
> base are confirmed by that alone"*. **An offset that agrees for all 1,224 ids confirms the
> catalogue was built with that offset. It says nothing about which slot the offset names, and a
> base cannot be confirmed by an arithmetic that is self-consistent under any rotation of it.**
> `01EED720 + 32 × id` is record(id) `+0x18` — the **result** callback. So the column is real, the
> stride of 32 is real, and the label was wrong. Recorded as `EVIDENCE-STANDARD` bv/bv.1, where
> the same fallacy is worked through on the census that produced the superseded frame.

### ⚠ The rule is not re-runnable as printed

§3's five rules are applied in an order the page never gives, and the order changes the answer. With
**`BRANCHING` tested before `CALL1`** the published numbers come back exactly; in the order the table
*prints* them, **24 handlers move out of `BRANCHING` into `CALL1`** — they have exactly one direct
call **and** a conditional branch — so `BRANCHING` reads **149** instead of 173. For a census whose whole claim is *"a rule
anyone can re-run"*, that is the one sentence that has to be there.

### ⚠ Ten handler extents ran past the end of the function, and four verbs were misclassified — fixed 2026-09-13

`enable` (call id `001E`) is the clearest. The census reads **37** bytes at `00353630` and classifies
it `CALL1`. The function is **13** bytes:

```asm
00353630  mov   rcx, rdx
00353633  mov   edx, 1
00353638  jmp   0x269E00        ; <- the whole handler: a bare tail-jump
0035363D  int3  / int3 / int3   ; <- padding
00353640  sub   rsp, 0x28       ; <- a DIFFERENT function starts here
00353647  call  0x267E10        ; <- the "single call" the census attributes to `enable`
```

Eleven of the 1,224 rows — **ten distinct handlers** — had a stated `body_bytes` that covers the
handler's own `int3` padding and then more code. **Four change family** once the extent is cut at the
boundary:

| call id | verb | handler | stated | real | census | corrected |
|---|---|---|--:|--:|---|---|
| `001E` | `enable` | `00353630` | 37 | **13** | `CALL1` | **`TAILJUMP`** |
| `03E6` | `hidecomplete` | `00350320` | 56 | **10** | `CALL1` | **`TAILJUMP`** |
| `0435` | `lookat_maxvelr_limit_unlock` | `0034ED80` | 56 | **13** | `CALL1` | **`TAILJUMP`** |
| `03AC` | `moveblurcaptureonce` | `00354950` | 33 | **10** | `LINEAR` | **`TAILJUMP`** |

The other seven rows (`0020`, `0022`, `007A`, `011C`, `0205`, `027F`, `0569`) keep their family —
`setlightallcutstatus` is still `LINEAR` but with **2** direct calls rather than 4, and
`puppet_setcharclipone` is unchanged at 7. Applied:

| family | handlers | verbs |
|---|--:|--:|
| `TAILJUMP` | 141 → **145** | 157 → **161** |
| `CALL1` | 402 → **399** | 426 → **423** |
| `LINEAR` | 449 → **448** | 457 → **456** |

> **`CONST` and `BRANCHING` do not move, and neither does the headline.** All four corrections are
> *inside* the non-branching set, so **993 handlers / 85.2 % with no conditional branch still holds,
> and so does 173 / 14.8 % branching.** The conclusion this page exists to support survives its own
> defect — which is worth saying plainly, because a four-row correction to a census table reads
> worse than it is.

**Ten handlers, not the eight this section first named.** The count rose when the adjudication did.
The detector that found these is a **strict shape rule** — *first `int3` run followed by a listed
entry* — and it sees **23 of the 29** listed-on-listed overruns in the image; a plain overlap census
finds the other six (no-pad adjacencies, `int3` runs ending exactly at an entry, one embedded switch
table). `011C` `lock_charmotion_once` and `0569` `puppet_setcharclipone` are two of those six.
Neither changes family, so the corrected census is the same either way — but *the number of affected
rows was wrong until a census replaced the detector*, which is the general lesson:
**a shape detector finds candidates; it does not count them.**

All ten cuts come from [`FUNCTION-EXTENT-ERRATA.tsv`](../../_index/FUNCTION-EXTENT-ERRATA.tsv),
which adjudicates every overrun **per row**: 29 `merge`, and 13 `legitimate body` whose `int3` run is
an **interior alignment pad that a branch inside the same function jumps over**. Cutting those 13
would truncate real bodies, so the generator reads the verdicts instead of re-running the heuristic.
`script_verb_shapes.py --no-errata` reproduces the superseded numbers exactly — the control that the
only thing that changed is where the bodies end.

§4 inherits it, and its numbers there are **measured from the regenerated file, not predicted**: the
prediction this section carried was two numbers wrong. See the note in §4.

### The defect is upstream, and it is measurable

`body_bytes` agrees with `Tools/work/graph/functions.tsv` for **all 1,224 rows** — the census copied
the function list faithfully. It is the **function list** that merges a short thunk with its
successor. Image-wide:

| | |
|---|--:|
| listed functions decoded | 38,161 |
| extents that run past their own `int3` padding into code that starts a new function | **36 (0.09 %)** |
| …of those, the overrun contains another *listed* entry | 23 |
| bytes counted twice | 4,468 |

> **The control matters here.** A looser rule — any `int3` followed by any instruction — returns
> **235**, and most of the extra 199 are the ordinary MSVC `call <noreturn> ; int3` pattern *inside* a
> body. Requiring the code after the padding to begin a function (16-byte aligned, or itself a listed
> entry) is what separates them; the eight verb handlers above all satisfy it, which is the positive
> control.

**Script-verb handlers are enriched about seven-fold in this defect class** — 8 of 1,166
handlers (0.69 %) against 36 of 38,161 listed functions (0.09 %), and 8 of the 36 image-wide
cases fall in this one bridge. That is not a coincidence: short
tail-jump thunks are exactly what gets merged into the next function, and §3 measures a population
that is mostly thunks. **Any census of this bridge that takes its extents from the function list will
over-read the same way.**

### ⚠ `DO-1` is scoped to the named ids, and under-states by 246

§5's 122 and 139 are counted over the **1,224 named** call ids and are exactly right there. The
table's extent is **1,496** records — §6's own cited figure — and the named ids are sparse inside it:
**116 gaps, the largest 28 wide.** Over all 1,496 records:

| slot | named ids (§5) | the whole extent |
|---|--:|--:|
| begin `+0x00` non-null | 1,224 | **1,234** |
| poll `+0x08` non-null | 122 | **277** |
| result `+0x10` non-null | 139 | **230** |
| poll + result | **261** | **507** |

Two findings fall out of the gap:

1. **Ten records carry a begin handler that the authored catalog does not name** — `059E`, `059F`,
   `05AA`, `05AE`, `05AF`, `05B2`, `05B3`, `05C0`, `05C1`, `05CC`, all in the tail band above
   `0599`, and `05B2` / `05B3` share one handler (`0050C7F0`). None has a poll or result.
2. **157 records carry a poll and/or result handler with no begin handler at all**, spread across
   `002E`…`0533`, and **not one of them is a named verb**. So a dispatch record can hold the second
   and third slots without the first — a shape §5 does not describe — and those 157 records are
   where the 246 unseen handlers live.

**[`scriptvm-verb-shapes.tsv`](scriptvm-verb-shapes.tsv) is unchanged.** The four rows still
carry the old family, because the file is generated by `script_verb_shapes.py` and hand-editing
four rows of a generated artefact makes it disagree with its generator, which is worse than the
defect. The fix belongs with the generator: cut each body at the first `int3` run that is
followed by a 16-byte-aligned instruction or a listed entry. Filed as `OPUS-VERB-SHAPES-REGEN`.

**Not claimed.** Which verb *any* handler implements, still. That the 1,496 extent is right — it is
taken from [the dispatch table](../scriptvm-native-dispatch-table.md), not re-derived here. What the
poll and result slots are *called with*, or when — `DO-1` stays open and gets larger. The four
reclassified verbs were re-read only far enough to establish the family. The verb **names** remain
unverifiable against the image, as §6 says. Nothing was executed and nothing was observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Resource — CLIENT.** The 14-byte `008620C0` is also called by a 58-byte Resource-filed body.
- **CoreRuntimeScheduling — MECHANICAL (1 edge).** 1 CoreRuntimeScheduling-side calls into shared helper(s) the page cites (`InputDevice_QueryAvailabilityState_Always1` (0053DD10)) - the helpers' general call surface, not a CoreRuntimeScheduling relationship of this page's subjects.
- **Input — MECHANICAL (4 edges).** 4 Input-side calls into shared helper(s) the page cites (`InputDevice_QueryAvailabilityState_Always1` (0053DD10)) - the helpers' general call surface, not a Input relationship of this page's subjects.
- **Party — SERVICE (1 edge).** 1 outbound (page-cited `VMPartyCommand_SetMovementSuppressionBit0` (00347E00) call Party bodies `PartyControl_SetMovementSuppressionBit` (00359200)). Substantive edges include `VMPartyCommand_SetMovementSuppressionBit0` (00347E00) calls `PartyControl_SetMovementSuppressionBit` (00359200).
- **Presentation — MECHANICAL (2 edges).** 2 Presentation-side calls into shared helper(s) the page cites (`InputDevice_QueryAvailabilityState_Always1` (0053DD10)) - the helpers' general call surface, not a Presentation relationship of this page's subjects.
- **Save_Load_Settings — SERVICE (1 edge).** 1 outbound (page-cited `0050D180` call Save_Load_Settings bodies `002EF370`). Substantive edges include `0050D180` calls `002EF370`.
- **UI — MECHANICAL (1 edge).** 1 UI-side calls into shared helper(s) the page cites (`InputDevice_QueryAvailabilityState_Always1` (0053DD10)) - the helpers' general call surface, not a UI relationship of this page's subjects.
- **World — CLIENT (1 edge).** 1 inbound (World bodies `00266D10` call page-cited `VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0)). Substantive edges include `VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0) is called by `00266D10`.
- **WorldAreaField — MECHANICAL (1 edge).** 1 WorldAreaField-side calls into shared helper(s) the page cites (`InputDevice_QueryAvailabilityState_Always1` (0053DD10)) - the helpers' general call surface, not a WorldAreaField relationship of this page's subjects.
### Crossings — 2026-09-18 departures (SWE2-EC7)

Naming the four departed callbacks (`0016D6A0`, `0050F810`, `0053DD10`, `005C5230`) exposes
`0053DD10`'s non-Verb caller edges on this page: **Input** (4 edges), **Presentation**
(2), and one edge each into **CoreRuntimeScheduling**, **UI** and **WorldAreaField** — and,
through the scheduling-side caller, one callee edge into **RNG_Random_Selection** whose own
callers span **CombatAction**, **CombatFormula**, **Rewards_Progression_Economy** and
**Status_Periodic_Terminal**. These are callers of a departed member, not verb-population
machinery; the A-measurement's evidence page owns the semantic account.
