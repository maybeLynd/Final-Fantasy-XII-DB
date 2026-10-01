# UQ-2: typing position 1 of derived-signature rows from their callers (OPUS, 2026-09-27)

**Question (UQ-2).** Liveness derives slots, not types. FABLE typed 47 rows: 40 at vtable slots, 7 constructors or
destructors. The route named for the other 515 is the callers: an argument passed from a typed source.

**Rule, made sound.** Position 1 of `f` is `T*` when two conditions hold.
1. `f`'s address is taken nowhere. The control scans for 8-byte and 4-byte RVA occurrences outside `.pdata`. Every
   function's own `.pdata` record holds its RVA, which first made almost every function look address-taken.
2. Every direct `call` / tail-`jmp` site of `f` passes `T + 0` in `rcx`, on a flow-census record that holds either:
   - in the **empty-entry** context, where the value comes from a getter, pool or cell in the caller itself; or
   - in the context where the caller's own `rcx` was `T + 0`, **and** the caller is itself typed `T` by the same rule.

   The rule is applied to a fixpoint.

A context-free version of rule 2 types 9 rows. Five of those rest on callers that are not themselves proven, so the
sound rule types 4.

**Seeds.** `type-flow-census/type_flow_census.py` gains `SITES_OUT`: every site that passes base + k, with its context.
Without it, the tool's output is byte-identical. BattleUnit is seeded through its nine accessors (5cb89f501), and the
receipt is `sites-BattleUnit.tsv` (586 sites).

**Result.** Four untyped rows take `BattleUnit*` in position 1: `002FFEF0`, `00306B10`, `0030B8E0` and `0030DA30`. In
all, 43 functions are typed `BattleUnit*` at `rcx` by the rule.
- Worked case: `00306B10`'s one caller `0030CBE0` passes `rdi`, which holds the return of
  `BattleUnit_ResolveByFocusHandle` `0031B7E0` across the intervening calls.

**Control.** `uq2_caller_route.py`:
- C1: the four rows;
- P1: the worked case;
- N1: an address-taken callee is not typed;
- N2: the context-free rule's five extras are not typed.

Expected `FAILS 0`.

**Not claimed:**
- positions other than 1;
- rows whose callers pass a type that has not been seeded. Only BattleUnit is seeded here, and the same machinery takes
  any type the census reaches.

**Correction to OPUS's handoff note of 2026-09-27:** "301 of 426 address-taken" counted `.pdata` records. Outside
`.pdata`, 353 of the 515 untyped rows are not address-taken.

## The residue by what position 1 is (OPUS, 2026-09-27, late night)

UQ-2 closed SUPERSEDED (cd73ae1d5) with 511 untyped position-1 rows. Under the Win64 ABI, position 1 is rcx or
xmm0, so the derived signatures already sort them:

| class | rows |
|---|---|
| arity 0: there is no position 1 | 140 |
| xmm0: floating-point (float vs double not claimed) | 3 |
| later arguments read, rcx and xmm0 not: dead, not derivable from the callee | 47 |
| rcx read, type not derived: **the derivation residue** | 321 |

The caller route was re-run with 41 seeded types: the 11 of the first run plus 30 image statics (`STATIC=`
censuses). It types 198 functions, and still only the same 4 signature rows: statics are addressed rip-relative, not
passed as arguments.

**Control:** `uq2_residue.py` (R1-R4, S; FAILS 0, run verified at 4f79e3667).

Affected: UQ-2 in `_index/OPEN-QUESTIONS.md`.

## What position 1 is, for the 321 (OPUS, 2026-09-27, late night)

The callee's own body shows what kind of value its entry rcx is. It does not show the class a pointer
points at, and no meaning is claimed. Tracking is a must-analysis over the CFG.

| position 1 | rows | evidence |
|---|---|---|
| pointer | 151 | entry rcx is the base of a memory operand |
| 32-bit integer | 78 | widest read is ecx, and it is never dereferenced |
| 16-bit integer | 36 | widest read is cx |
| 8-bit integer | 19 | widest read is cl |
| 64-bit, undecided | 16 | only full-width non-dereferencing uses, such as `test rcx, rcx` or a scale-1 index |
| passed on | 19 | only handed to a call or tail jump |
| unused | 2 | - |

The class-derivation residue proper is the 151 pointers, plus the 16 undecided.

**Controls:** `uq2_p1_representation.py` writes `uq2-p1-representation.tsv` with `--write`:
- R: the counts;
- P: `0031B770` INT8, `0018D740` POINTER, `00197990` INT32;
- N: `00324020`, whose entry rcx is only a scale-1 index, is not called a pointer.

FAILS 0, run verified at 0a54455a0. Not claimed: signedness.

Affected: UQ-2 in `_index/OPEN-QUESTIONS.md`.
