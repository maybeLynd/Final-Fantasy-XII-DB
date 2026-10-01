---
contract: borrow the shared transform workbench and give back exactly what you promised to
category: 00-Engine-Core-Runtime
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md
entries: ["0036D930", "0036D8E0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 53 addresses cited - 5 data, 14 entry, 34 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-workbench-pass-1     # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the transform workbench's save and restore

249 functions write one shared area and nothing restores it; the house rule is *"treat the workbench
as caller-saved."* **Nine functions opt out of that rule** through one explicit save/restore pair,
and this contract states what those nine are promising and what they may rely on.

The first contract in `00-Engine-Core-Runtime`.

## 1. Purpose

The three pages on the workbench establish **what is in it** and **who writes it**. A reimplementer
needs something they do not state: the **obligations**. What must a caller do before Save, what may
it assume after Restore, and what happens if two callers overlap.

## 2. Interface

| | |
|---|---|
| Save | `0036D930` (89 B) — **variadic**: `ecx` = count, then that many pointers in `rdx`, `r8`, `r9` and the stack |
| Restore | `0036D8E0` (66 B) — **no arguments** |

Nine functions call Save; five call Restore and four **tail-jump** to it. The nine users'
own callers are overwhelmingly **Presentation**-layer code — `0042FDB0` is invoked from 80
render-path sites, `003D8E50` from 43, `00462260` from 17, `00431D30` from 9 — so the
workbench exists to serve the draw path, and every Presentation caller of a user is bound
by this contract transitively.

## 3. Types

| | |
|---|---|
| saved pointers | `0x02EC0A00`, one qword per saved item |
| saved values | `0x02EC0800`, **16 bytes** per saved item |
| depth | `0x022D8F08`, a `dword` — **inside the workbench region**, the saved arrays are not |

**Save copies sixteen bytes per pointer**, one `movups` (`0036D974`–`0036D977`) — a row or a vector,
**not a whole matrix**. A caller saving a 64-byte matrix must pass four pointers, and this contract
has no evidence about whether any caller does.

## 4. Preconditions · postconditions · invariants

**Precondition: no save may be outstanding.** See §10 for what happens if one is — and
**§10 now shows that none ever is, on the direct call graph.** The obligation remains part of the
contract because it is what the code relies on, not because it is currently at risk.

**Precondition 2 (added 2026-09-28, OPUS, on ASTRA-RETURN-OPUS-WORKBENCH-DEPTH-TARGET-ALIAS): no saved target's 16-byte span may cover the depth counter's four bytes `022D8F08`..`022D8F0B`.** Precondition 1 alone does not give the postcondition below.
- **Why.** Restore does not latch the count. After each `movups` store (`0036D90F`) it re-reads depth from memory
  (`0036D912`) and compares unsigned (`0036D918 jb`).
- **What happens otherwise.** A target that covers the counter rewrites the loop bound with its Save-time bytes.
  With no save outstanding, those are zero, so Restore stops after that item, and every later item stays clobbered.
  Example: targets `022D8F08` then `022D8F90` restore only the first.
- **Sufficient, not necessary.** A counter-covering target saved *last* restores everything.
- **Evidence.** Class: source-level conditional, not executed:
  [`_experiments/evidence/workbench-depth-target-alias/`](../_experiments/evidence/workbench-depth-target-alias/README.md).
  The instruction order was re-read by OPUS from the certified image. No shipped caller is shown to pass such a
  target (§10's nine callers). The §13 differential used disjoint targets, so it does not bear on this.

**Precondition 3 (added 2026-09-28, SWE2-CONTRACT, on ASTRA-RETURN-CONTRACT-SAVE-POINTER-RECORD-ALIAS): no saved target's 16-byte span may overlap a pointer-record slot written before its own load — in the degenerate case, its own slot `02EC0A00 + i*8`.** "Entry-state snapshot" is a *load-time* snapshot.
- **Why.** Save stores each pointer into its record slot *first* (`0036D969`) and only then loads the
  target's sixteen bytes (`0036D974`/`0036D977`). A target covering the slot being written is captured
  with those bytes already replaced: `target == 02EC0A00 + i*8` records the little-endian pointer value
  itself in bytes 0–7, not the entry bytes. An earlier iteration's slot inside the span corrupts the same
  way; a later iteration's slot lands inside the target *after* the capture — that does not corrupt this
  item's snapshot, but it does overwrite bytes of the target.
- **What Restore does with it.** An immediate Restore writes the doctored snapshot back, leaving the
  target's first eight bytes changed while depth returns to zero — silent.
- **Scope.** Conditional source calculation only
  ([`_experiments/evidence/save-pointer-record-alias-byte-preserved/`](../_experiments/evidence/save-pointer-record-alias-byte-preserved/README.md));
  no shipped caller is shown to pass such a target, and this names only the pointer-record overlap, not
  a general non-alias rule for the snapshot array or the rest of the workbench.

**Postcondition of Restore:** for each item the last Save recorded, the 16 bytes at its saved pointer
are the bytes that were there at Save time; then depth is zero.

**Restore is idempotent.** It loops while `edx < depth` and then zeroes depth (`0036D91A`), so a
second Restore with no intervening Save does nothing at all.

**What a caller may NOT assume:** that anything else in the workbench survived. The house rule stands
for every byte nobody named in a Save.

## 5. State

Written by Save: the two arrays and depth. Written by Restore: through the saved pointers, and depth.
**Unchanged by both:** every byte of the workbench that was not the target of a saved pointer.

## 6. Relationships

- The 249 writers are documented in the sibling pages and are not enumerated here.
- Restore writes **through pointers the caller supplied**, so its reach is whatever those point at —
  it is not confined to the workbench.

## 7. State transitions

**Save**, `0036D930`:

```
spill ecx, rdx, r8, r9 to the shadow space        0036D930-0036D943
if (count == 0) goto tail                         0036D948
rdx = &shadow[0] - 8
for i in 0 .. count-1:                            0036D961
    ptr = *(rdx += 8)
    [02EC0A00 + i*8]  = ptr                       0036D969
    [02EC0800 + i*16] = *(xmmword*)ptr            0036D974-0036D977
tail:
depth = count                                     0036D982   <- ASSIGNMENT, not an increment
```

**Restore**, `0036D8E0`:

```
for i = 0; i < depth; i++:                        0036D8E6, 0036D912
    ptr = [02EC0A00 + i*8]                        0036D8FE
    *(xmmword*)ptr = [02EC0800 + i*16]            0036D906-0036D90F
depth = 0                                         0036D91A
```

## 8. Script · resource · event interactions

None.

## 9. Determinism

Fully deterministic.

## 10. Failure paths and edge conditions

**Neither function can fail, and neither validates anything.** The hazards are all in the caller.

**IT IS NOT A STACK, AND THE MECHANISM IS SHARPER THAN "NESTING LOSES THE OUTER FRAME".** Save
*assigns* depth (`mov`, `0036D982`) and indexes both arrays **from zero**. So a second Save does not
merely lose the outer frame's count — it **overwrites the outer frame's saved pointers and saved
values in place**. The outer caller's Restore then writes the inner caller's bytes through the inner
caller's pointers, and the outer state is gone with nothing reporting it.

**The depth counter sits inside the very area the convention declares clobberable.** `022D8F08` is
eight bytes into the workbench region, which 249 functions write. A single stray write there would
make Restore loop over a wrong count and write through whatever the pointer array happens to hold.

**AND NESTING CANNOT HAPPEN, on the direct call graph — measured 2026-09-11.** From each of the
nine Save callers, the transitive set reachable through direct calls was taken and asked whether Save
is reachable again. **Eight of the nine cannot reach Save by any path**, which is decisive for them:
a function that cannot reach Save at all cannot reach it between its own Save and Restore. The ninth,
`0044BAC0`, can — and only through `0026EE00`, which is itself one of the nine. That reduced the
question to one window:

```
0044BDAB  call 0026EE00     the two paths to a second Save ...
0044C07A  call 0026EE00     ... both far BEFORE the save
0044C43E  call Save         <- the window opens
0044C48E  call 00861F14     the ONLY call inside it - sqrtf, a leaf with no callees
0044C4C3  call Restore      <- and closes
```

**THE LIMIT, and it covers all nine at once:** the edge list holds **direct** calls. An indirect call
— function pointer, vtable, jump table — is not an edge, so this closes nesting on the direct call
graph and not absolutely.

**Measured, because the counter hazard deserves better than a warning too.** An image-wide sweep of
the region's first sixteen bytes finds `022D8F08` touched by **exactly four instructions, all inside
Save and Restore** — two reads and one write in Restore, one write in Save. Nothing else in the executable
references it. So the counter is safe in this build **by absence, not by protection**, which is worth
saying in those words: a reconstruction that added a workbench user writing at `+8` would break
Restore and nothing would catch it.

**And the same sweep found something the region's boundary does not account for.** The dword at
`022D8F0C` — four bytes after the depth counter, inside the region as the referenced page draws it —
is read seven times by `FUN_00501820` and written twice by `FUN_00502280`. *Resolved 2026-09-23
(SWE2-CONTRACT): the "no relationship" reading was wrong — `00502280` is itself one of the heaviest
workbench borrowers in the image (111 rip-operands into `022D8F00`–`022D9500`, writing rows
`022D8F90`–`022D9330` and beyond).* `022D8F0C` is a workbench cell that borrower uses as the
**bit-offset parameter** for the sliding-window extract `00501820`: `00502280` stores
`(mode_byte ^ 2) << 4` at `00502670`/`005027C1` immediately before `call 00501820`, and the callee
reads it rip-relative — 0 = verbatim 16-byte copy, `0x40` = half-swap, else funnel-shift a 128-bit
window at that bit offset from a 32-byte pair. **So the workbench does begin at `022D8F00`; the
cell is borrowed scratch like every other row, and the wholesale-clear hazard stays: clearing the
region between `00502280`'s store and `00501820`'s read would corrupt the parameter.**

## 11. Observable behaviour

Not established. What would be observable: a save/restore pair leaving its named rows unchanged
across a call that otherwise clobbers the workbench.

## 12. Reproduction formula

```c
static void  *saved_ptr[N];      /* 0x02EC0A00 */
static __m128 saved_val[N];      /* 0x02EC0800 */
static int    depth;             /* 0x022D8F08 - inside the workbench */

void Workbench_Save(int count, ...)          /* 0036D930 */
{
    va_list ap; va_start(ap, count);
    for (int i = 0; i < count; i++) {
        void *p = va_arg(ap, void *);
        saved_ptr[i] = p;
        saved_val[i] = *(__m128 *)p;         /* SIXTEEN BYTES, not a matrix */
    }
    depth = count;                           /* assignment - not a push */
}

void Workbench_Restore(void)                 /* 0036D8E0 */
{
    for (int i = 0; i < depth; i++)
        *(__m128 *)saved_ptr[i] = saved_val[i];
    depth = 0;                               /* idempotent thereafter */
}
```

**`count` is a raw u32 at the ABI level, and the `for (int i = 0; i < count; i++)` sketch is valid
only inside the domain callers actually use** (added 2026-09-28, SWE2-CONTRACT, on
ASTRA-RETURN-CONTRACT-SAVE-COUNT-BITS). The real gate is `test ecx, ecx` / `je` (`0036D948`):
**only exact zero skips the loop**. The countdown is `mov r10d, ecx` — a *zero-extension* —
followed by `sub r10, 1` / `jne` (`0036D950`, `0036D97C`–`0036D980`), so any nonzero `ecx`,
including `0x80000000`–`0xFFFFFFFF`, enters the loop and iterates `ecx` times, reading that many
variadic pointers and writing that many 8-byte pointer records and 16-byte snapshots — nothing
bounds either array. A signed sketch would treat a high-bit count as a no-op; the original does
not. Model the loop as `for (u32 n = count; n != 0; --n)`, and treat counts outside the shipped
callers' small positive range as outside the tested domain — not as a signed no-op, and not as a
promised fault (an out-of-domain run interferes or fails for other reasons first). Evidence class:
source-level conditional
([`_experiments/evidence/save-count-bit-semantics/`](../_experiments/evidence/save-count-bit-semantics/README.md)).

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-12)

Both bodies now run at their real virtual addresses under Unicorn against an independent
reconstruction, with the three globals mapped where the shipped rip-relative operands resolve —
values at `0x02EC0800`, pointers at `0x02EC0A00`, depth at `0x022D8F08`. Neither function takes the
workbench as an argument, so planting them anywhere else would not be running this code.

**Instrument:** [`diff_workbench_save.py`](../../../Reconstruction/Tests/Differential/diff_workbench_save.py)
against [`workbench_save.c`](../../../Reconstruction/Game/Math/workbench_save.c).

**Result: 128 commands, 67 compared lines, 0 mismatches** — 17 distinct scratch images out of 17,
depth observed at 0, 1, 2, 3, 4, 5 and 8, and three cases driving stack-passed arguments.

### The two things reading could state and only a run could drive

1. **Save is variadic, and past three items the arguments leave the registers.** A reconstruction
   taking a count and an array is observably identical for one, two and three items — it would agree
   on every case a careless suite would write. The cases at 4, 5 and 8 are the ones that exercise the
   home-area spill at `0036D930`–`0036D943` and the stack slots behind it, and they are the reason
   the reconstruction is written variadic rather than with an array parameter.

2. **It is not a stack, and the consequence was driven rather than asserted.** Two rows saved, one
   different row saved on top, then a Restore: only the inner row came back, the outer frame's
   pointers and values were gone, and the outer rows' clobbers were still visible in the block. §10
   states this; the run shows it happening.

**A positive control on the same claim.** The reconstruction's `depth` assignment was temporarily
changed to `depth +=` — the "make it a proper stack" mistake — and the suite caught it, though not as
a mismatch: Restore then walks past what Save ever wrote and **the driver crashed**. Recorded as it
happened rather than tidied, because it is a real property of the difference: treating this as a
stack does not merely produce other bytes, it dereferences a pointer that was never recorded.

### How far the instrument itself has been tested

**14 mutants: 11 KILLED · 2 EQUIVALENT · 1 SURVIVED · 0 NO_BUILD · 0 TIMEOUT · 0 INVALID.**
Production inputs verified stable.

The one survivor is `WB_VALUES_AT 0x02EC0800 → 0x02EC0801`, which moves the reconstruction's array
capacity from 32 to 31. **It cannot be killed and should not be:** the capacity is this file's array
sizing, not a property of the original. The shipped Save has **no bound at all** — it writes as many
items as the caller asks for — so there is no behaviour here for a case to distinguish. The two
`EQUIVALENT` rows are the other two address constants, which this file carries as documentation and
proves byte-identical.

**Two earlier campaigns are worth recording, because the numbers moved for reasons that were not
improvements to the reconstruction.**

| | KILLED | SURVIVED | INVALID | what changed |
|---|---:|---:|---:|---|
| first | 3 | 3 | **4** | — |
| second | 8 | 4 | 0 | unused pointer slots point at an observable **sink** instead of NULL |
| third | **11** | **1** | 0 | the fixture's own initial state is read back before anything is saved |

**The four INVALIDs were detections being scored as inconclusive.** A mutant that leaves a pointer
slot unset makes Restore dereference NULL, the driver dies, and the campaign cannot say whether the
suite would have noticed. Pointing unused slots at a 16-byte sink the driver prints turns every one
of those crashes into a comparison. The sink lives in the **fixture**, never in Save or Restore —
the same line the transform primitives' contract draws about canaries.

**And the third campaign's gain came from a blind spot the suite had all along.** Three mutations of
the reset survived not because they were equivalent but because **nothing ever looked at what they
changed**: every case overwrote the slots it read before reading them. Adding one case that reads the
starting state back immediately exposed a real disagreement — the emulator side was zeroing the
pointer array while the reconstruction pointed it at the sink, and the suite had been green anyway.
**A fixture that both sides set up differently is a difference the comparison cannot see until
something compares the setup itself.**

### What is still owed, and it is live-only

The indirect-call question §10 leaves open: a breakpoint on `0036D930` reporting a non-zero depth on
entry would catch a nesting no edge list can see. Requested from ASTRA; not claimed here.

~~One check: does a save ever nest?~~ **TAKEN STATICALLY INSTEAD, 2026-09-11** — see §10. The
cheaper route this section named is the one that was available, and it closed the question on the
direct call graph, so the breakpoint is no longer the first thing to ask for.

**What a live check would still add** is the one thing the static reading cannot reach: an *indirect*
call inside a save window. A breakpoint on `0036D930` reporting a non-zero depth on entry would catch
that, and it costs nothing to leave armed alongside other work — but it is no longer a dependency of
this contract, and nothing here is waiting on it.

Requested from ASTRA; not claimed by me.

## 14. Unresolved

- ~~Whether any of the nine callers can nest~~ — **closed on the direct call graph** (§10). What
  remains is only whether an indirect call inside a save window could reach Save, which no edge list
  can answer.
- ~~Whether any caller saves a whole matrix by passing four pointers.~~ **CLOSED 2026-09-23
  (SWE2-CONTRACT): no — and nobody could.** All nine call sites decoded: eight pass `ecx = 1`
  (`0026EE2C`, `002F1CF5`, `002F1DAC`, `003AFDEC`, `003D8E78`, `00431D4C`, `0044C43E`,
  `0046227C`), one passes `ecx = 2` (`004300F9`, saving rows `022D8F30`+`022D8F40`). Since a
  second Save overwrites the first frame in place (§10), a single save window can protect at
  most two rows — a whole matrix is unreachable through this convention.
- ~~What `022D8F0C` belongs to, and therefore where the workbench really begins — see §10.~~
  **CLOSED 2026-09-23 (SWE2-CONTRACT): it belongs to the workbench — specifically to borrower
  `00502280`, which is not foreign at all (111 rip-operands into the region).** The cell is its
  bit-offset parameter for the `00501820` sliding-window extract (§10). The earlier "no
  relationship to the workbench" framing is corrected in §10/§15.
- ~~The bound on `N`: nothing observed limits the count Save accepts, and the two arrays' extents
  are not established here.~~ **BOUNDED 2026-09-23 (SWE2-CONTRACT): the layout itself bounds N
  at 32 — enforced by nothing.** A decode-verified raw-disp32 census over all of `.text`
  (covering the non-`.pdata` Save body `0036D930`, which the `.pdata` census misses) finds:
  values array `lea`'d at `0036D954` = `02EC0800` (16 B/item), pointers `lea`'d at `0036D95B` =
  `02EC0A00` (8 B/item) — exactly `0x200` apart, so `values[32]` would write `pointers[0]`. The
  pointer array is separately bounded at 36 by foreign flag words at `02EC0B24`/`02EC0B28`
  (`0036D840`'s mask pair). No instruction compares `ecx` against anything — the bound is
  structural only, and shipped callers never exceed 2. Note also: `02EC0848`/`02EC08B8` are
  `lea` end-bounds of stride-`0x70` tables (`02EBFA48`/`02EBFAB8` bases, 32 records) whose last
  record `02EC07D8`–`02EC0847` **overlaps values rows 0–4** — a genuine BSS interleave, safe
  only while that record's `+0x28`+ tail stays unused; whether it does is unenumerated.

## 15. Evidence

Static, from the shipping image (`73461D08…`). Both functions were disassembled and read in full;
the page's save/restore identification, its nine callers and its "caller-saved" house rule are cited
and were not re-derived. The two measurements in §10 — that only Save and Restore touch the depth
counter, and that `022D8F0C` has unrelated users — are mine and are image-wide sweeps of a sixteen-
byte window.

**Claim table added 2026-09-12 (`OPUS-WBSAVE-ISOLATED`).** The paragraph above states the method and
is kept. The table enumerates what the contract establishes so a reimplementer can read it row by row
and so `diff_workbench_save.py` can map to it; nothing in it is new analysis.

| claim | evidence | tier | confidence |
|---|---|---|---|
| Save is variadic: ecx is the count, pointers in rdx, r8, r9 and then the stack | `0036D930`–`0036D943` spills the register arguments into the home area so arguments two and beyond form one contiguous array, walked from `[rsp+0x10]`. Executed at 1, 2, 3, 4, 5 and 8 items | 1 (isolated original-code) | PROVEN |
| Save copies sixteen bytes per pointer | one `movups`, `0036D974`–`0036D977` — a row or a vector, not a matrix. Executed; every saved value compared in full | 1 (isolated original-code) | PROVEN |
| Save assigns depth and indexes from zero, so a second Save overwrites the first in place | `mov dword [022D8F08], ecx` at `0036D982`, and both arrays are indexed from zero. Executed: two rows saved, one different row saved on top, restored, and only the inner row came back | 1 (isolated original-code) | PROVEN |
| a count of zero still assigns depth | `test ecx,ecx / je 0036D982` jumps over the loop **to the store**, not past it. Executed | 1 (isolated original-code) | PROVEN |
| Restore writes each saved 16 bytes back through its saved pointer | `0036D8FE`–`0036D90F`: pointer from `022D8F08`-indexed array, value from the 16-byte array, one `movups` back. Executed, with the scratch block clobbered between save and restore in every case | 1 (isolated original-code) | PROVEN |
| Restore zeroes depth, and is therefore idempotent | `mov dword [022D8F08], r8d` with `r8d = 0` at `0036D91A`. Executed twice with no save between | 1 (isolated original-code) | PROVEN |
| the depth counter is touched by exactly four instructions image-wide | an image-wide sweep of `022D8F08`: reads `0036D8E6`/`0036D912` and write `0036D91A` in Restore, write `0036D982` in Save, and nothing else in the executable. **Safe by absence, not by protection** | 1 (static) | PROVEN as a negative over the disassembled image |
| **the nine users DO call one another — just never while holding the workbench** | **measured 2026-09-12 (§15a)**: `0044BAC0` transitively reaches six of the other eight, and calls none of them between its own Save and Restore. Across all nine held windows there are **four calls in total**, **no** call to a user, **nothing** that transitively reaches one, and **no indirect call at all** | 1 | PROVEN |
| **four of the nine restore by TAIL JUMP, not by call** | **re-read 2026-09-12**: `0026EE00` `0026F413`, `003AFDD0` `003AFFAB`, `00431D30` `00431F0A`, `00462260` `0046242E` — each `jmp 0036D8E0` as its last act. The other five use `call`. A census counting only `call` sites reports these four as having no Restore | 1 | PROVEN |
| nesting cannot happen on the direct call graph | from each of the nine Save callers, the transitive set through direct calls was asked whether Save is reachable again. Eight cannot reach it at all; the ninth's only window contains one call, to `sqrtf`, a leaf | 1 (static) | PROVEN for DIRECT calls only — an indirect call is not an edge |
| ~~`022D8F0C` is read and written by functions with no relationship to the workbench~~ **CORRECTED 2026-09-23 (SWE2-CONTRACT): `00502280` is a workbench borrower** — 111 rip-operands into `022D8F00`–`022D9500`. `022D8F0C` is the workbench cell it uses as the bit-offset parameter for `00501820` (§10); the workbench does begin at `022D8F00` | the same sweep: seven reads by `FUN_00501820`, two writes by `FUN_00502280` — plus the full-body read showing `00502280` writes workbench rows `022D8F90`–`022D9330`+ throughout | 1 (static) | PROVEN |
| **N is structurally bounded at 32, unenforced; no caller saves a whole matrix** | decode-verified raw-disp32 census over all `.text`: values `02EC0800` (16 B/item, `0036D954`), pointers `02EC0A00` (8 B/item, `0036D95B`) — `values[32]` aliases `pointers[0]`; pointers bounded at 36 by `02EC0B24` flag words; all nine callers pass `ecx ∈ {1,2}` | 1 (static) | PROVEN |
| any runtime observation | — | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED

### The exact image-wide count reproduces

§15 claims *"the depth counter is touched by exactly four instructions image-wide"* — the most
falsifiable thing a document can say, because one missed reference refutes it. Re-derived by
disassembling **every function in the census from its own entry** — 38,161 functions, **1,787,590
instructions decoded, none skipped** — and counting every RIP-relative operand landing in the
region's first sixteen bytes:

| target | instructions | where |
|---|---:|---|
| **`022D8F08` — the depth counter** | **4** | `0036D8E6` and `0036D912` read it, `0036D91A` zeroes it (Restore); `0036D982` writes it (Save) |
| `022D8F0C` — four bytes later | 9 | seven in `FUN_00501820`, two in `FUN_00502280` |

**Exactly four, exactly where the document says.** And the nine at `022D8F0C` are §15's other claim —
*"read and written by functions with no relationship to the workbench"* — now with the two functions
named. **The document's care in separating `+0x08` from `+0x0C` is the whole reason both claims are
true**; a sweep of "the region" returns 13 and would refute the first if anyone read it loosely.

### Nesting: the claim holds, and the reason is stronger than the claim

*"Nesting cannot happen on the direct call graph"* reads as though the nine users do not reach one
another. **They do.** `0044BAC0` transitively reaches **six of the other eight**. That is not
nesting, and the difference is the whole point: nesting needs a user called **while the workbench is
held**.

Measured per user — Save site to Restore site, the *held window*:

| user | held window | calls inside | reaching a user | indirect |
|---|---|---:|---:|---:|
| `0026EE00` | `0026EE2C`–`0026F413` | 0 | 0 | 0 |
| `002F1CE0` | `002F1CF5`–`002F1D7D` | 1 | 0 | 0 |
| `002F1D90` | `002F1DAC`–`002F1E9B` | 2 | 0 | 0 |
| `003AFDD0` | `003AFDEC`–`003AFFAB` | 0 | 0 | 0 |
| `003D8E50` | `003D8E78`–`003D8FE2` | 0 | 0 | 0 |
| `0042FDB0` | `004300F9`–`0043035E` | 0 | 0 | 0 |
| `00431D30` | `00431D4C`–`00431F0A` | 0 | 0 | 0 |
| `0044BAC0` | `0044C43E`–`0044C4C3` | 1 | 0 | 0 |
| `00462260` | `0046227C`–`0046242E` | 0 | 0 | 0 |

**Four calls inside all nine windows combined, none to a user, none to anything that reaches one,
and not one indirect call anywhere in any window.** `0044BAC0`'s single inside-call is `sqrtf`. That
is a far better guarantee than the call graph alone gives, and it does not depend on the graph being
complete — an indirect call inside a window would break the argument, and there are none.

### Two instrument failures of my own, recorded so they are not repeated

**A linear sweep of `.text` returned ZERO references** to the depth counter — which would have been
a spectacular refutation and was entirely my bug: capstone's `disasm` is a generator that **stops at
the first byte it cannot decode**, so an 8 MB linear pass ends in the first padding it meets. Per
function, from each entry, it finds all four. **A sweep that returns zero should be suspected before
the document is.**

**Counting only `call` sites dropped four of the nine users** as unmatched pairs, because they
restore by **tail jump**. That is now a claim in its own right rather than an artefact.

> **Still unexecuted for the negatives.** §15's first five claims carry isolated original-code
> evidence; claims 6–8 and the two added here are static, and this pass read instructions rather
> than running them. `crossref_clean` stays **false** — not run clean against this document.

## 16. Parity plan

Reproduce: the sixteen-byte save granularity, depth as an **assignment**, Restore's idempotence, and
the fact that the counter lives inside the shared area. A reimplementation that made this a proper
stack would be *safer* than the original and would diverge from it the first time anything nested.

**Done offline 2026-09-12** — see §13. `CALCULATION`, `STRUCTURAL`, `STATE-TRANSITION` and
`EDGE-CASE` are covered. `CONTRACT` is not, and the three rows that keep it open are the two
image-wide sweeps and the call-graph reachability argument — none of which a run of these two
functions can reach, and all of which are already `PROVEN` by the method that suits them.
`INTEGRATION` and `FULL-SUBSYSTEM` are not covered: no caller is reconstructed, and the 249
functions whose clobbering gives this pair its purpose are not exercised.

**Four things a reimplementer must take from this contract:**

1. **Write Save variadic.** A count and an array is observably identical for three items and never
   touches the path every caller with four or more takes.
2. **Assign depth, do not add to it.** Making this a proper stack is safer than the original and
   different from it.
3. **Sixteen bytes per item.** A caller saving a 64-byte matrix passes four pointers.
4. **Nothing is validated.** No count is bounded, no pointer is checked, and the values array runs
   into the pointer array after 32 items.

## 17. Related

- `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md`
- `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md`
- `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`

`00501820` (297 B) is the sliding-window extract `00502280` calls: `dword[022D8F0C]` is the bit position - 0 copies the 16-byte pair verbatim and `0x40` swaps the halves; else `r8 = (lo >> (64-n) & mask) | (hi << n)` and `rbx = (lo >> n & ~mask) | (hi2 << (64-n))` funnel-shift the qword pair into `r10`/`r10+8` - the bit-packed field read whose index `022D8F0C` section 10 left unattributed.

Interior anchor `005018A5` (function `00501820`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Movement — CLIENT (1 edge).** 1 inbound (Movement bodies `003B7E20` call page-cited `0036D840`). Substantive edges include `0036D840` is called by `003B7E20`.
- **Script_VM_Native_Bridge — CLIENT (3 edges).** 3 inbound (Script_VM_Native_Bridge bodies `003B7C60`, `0034D700`, `003B7BB0` call page-cited `0036D840`). Substantive edges include `0036D840` is called by `003B7C60`; `0036D840` is called by `0034D700`; `0036D840` is called by `003B7BB0`.
