# Script VM / Native Bridge

**Engine category.** The ScriptVM that runs authored `.ebp` zone scripts, and the native call catalog bridging script verbs to engine code.

| | |
|---|---|
| Classification source | PrimaryOwner: Script/VM Native Bridge |
| Functions | 1,900 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category


- [`Interpreter-Core/worldactor-scriptvm-interpreter.md`](Interpreter-Core/worldactor-scriptvm-interpreter.md) —
  **DOCUMENTED, tier 1.** The interpreter itself: **14,646 bytes, a 100-opcode computed-goto
  dispatch** through a 32-bit RVA table at `0x00261DF8`, a stack machine over int32/float32
  operating on actors. **Six opcodes are indistinguishable from an invalid one.**
- [`Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`](Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md) —
  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)* How a 16-bit call id in the bytecode reaches a native handler: the 4-bit
  family / 12-bit command split, the five command tables (**1,960 slots**), the begin/poll/result
  record, and the **exact parameter encoding** — value-stack layout, both coercion rules, argument
  order, reference out-parameters and actor handles. **1,870 of the 1,960 slots carry a measured
  arity**, agreeing with the authored catalog 1,209 times out of 1,210 *(answered: BQ-9 measured the other 90 on 2026-09-27; all 1,960 now carry one, 1,269 of 1,270 agree; 2026-10-02, OPUS)*. Carries
  [`Verb-Dispatch/scriptvm-verb-table.tsv`](Verb-Dispatch/scriptvm-verb-table.tsv), the full
  1,960-row id → handler → arity table.

- [`scriptvm-native-dispatch-table.md`](scriptvm-native-dispatch-table.md) —
  ~~**DOCUMENTED, tier 2.**~~ **AUDITED, tier 2.** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`; its TSV now holds 1,493 rows)* The predecessor: family 0's `result` column, 1,224 catalog rows mapped
  through it.

- [`Native-Command-Lifecycle/native-command-lifecycle.md`](Native-Command-Lifecycle/native-command-lifecycle.md) —
  **DOCUMENTED, tier 1.** The begin / poll / result lifecycle and the 16-family id encoding.

The bundled ff12-script source (`CScriptContainerInitializers.cpp`) is the authored call catalog:
1,954 verb names with argument counts and parameter types. It is tier-9 evidence — it names verbs the
binary only numbers, and it is what the verb table is cross-checked against.

**Hard rule: ScriptVM wrappers are authored-intent evidence, never replay seams.** Always descend to the native owner transition beneath the wrapper.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
