# Effective action-ID source and owner precondition

**Question.** Does the effective-ID producer `387090` exclude action IDs 511–534 before the standard-action pipeline passes its result to presentation-slot acquisition? What precisely selects its replacement ID, and is a missing owner safe?

**Player view.** This getter usually reads the unit's stored action ID. Action `0x9F` can be replaced by a table value when a table pointer is available. The getter does not itself filter the suspect IDs; the remaining question is which normal commands write them into the unit. A missing-owner check does not provide a safe fallback in this getter.

## Method, identity and controls

Method A is sufficient for these local value/branch/ownership-contract facts. The package inspects verified original code, proves closed control-flow and exact data transfer, and qualifies unresolved state. It executes no original FF12 instruction, native harness, emulator or game.

EXE SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base `120000`. Original getter `387090..387125` is 149 bytes (SHA-256 `7fe996559221d1aae0ad0dfd1991bef228e8cbcc598eaa86eca585c65287fa87`). Its owner resolver `31B860..31B8B3` is 83 bytes (SHA-256 `9a162077226a0c37d235edf972c43ef16187e594054b0d54eb7ddfd2cddcca8f`). The exact committed caller prefix is retained from `0ada5145`; no repeated prefix capture or earlier experiment credit. All source maps are checked against EXE bytes and the reviewed access-role adapter actually used in capture/validation.

The initial feasibility validates the getter's full CFG and discriminators; it is not semantic closure. The semantic producer checks that feasibility's actual exit/result/driver/source identities before output. Its positive and four actual CLI refusal controls include **failed feasibility with an apparent output still present**. Missing feasibility status, failed capture and missing owner source also cannot pass. Seven focused synthetic source controls cover replacement ID, read width, invented safe-null return, second resolver input, helper null return, caller byte truncation and wrong getter. They are producer controls, not independent acceptance or native tests.

## Exact local result

Let `O2` be the mandatory second `31B860(query)` return. With a valid non-null `O2`, the getter returns the zero-extended WORD at `O2+714`, except when that word equals **`0x9F`** and the selected table pointer in `RBX` is nonzero. That exceptional branch returns the zero-extended WORD at `RBX+10`. A zero table pointer returns the stored word directly, including `0x9F`.

There is no local range/category bound on the direct word. In particular, 511–534 differ from `0x9F` and would pass this getter unchanged under its valid-owner premises. This narrows the next question to the `unit+714` writer/admission domain; it does not prove that any normal command supplies those values.

The replacement pointer is selected separately:

- Non-null query whose BYTE `+5` is zero: `208D480 + BYTE(query+4)*64`, without a first owner-resolver call.
- Otherwise: first resolver return `O1` is written to `2EBF188`. A non-null `O1` selects `208DE80 + BYTE(O1+EA9)*64`; a null `O1` gives `RBX=0`.

The second resolver return `O2` then controls the stored-word read. **`O1` and `O2` are distinct observations/call results.** The code alone does not guarantee they match or that the table and owner reads form an atomic snapshot. Table initialization, contents, usable extent and actual type/index admission are not established here.

The original owner resolver returns zero for a null query before calling its registry helpers. For a non-null query, it searches registry count/index helpers and returns a unit whose QWORD `+698` matches the query, or zero. It re-reads count during the scan. Current registry identity, access/termination and stable lifetime are separate premises.

**Missing-owner boundary:** the getter's second-null branch goes to `387118`, which still reads WORD `[RAX+714]`. It does not return a sentinel. For a null query, both verified original resolver calls return zero without registry callbacks, so this composed source path predicts a read at address **`714`**. This is a source prediction, **not an observed crash/fault or a claim that a normal caller passes null**. A normal valid return requires the owner-backed read, and the replacement path also needs its table read to be valid.

At the retained standard-action fragment, `304DFD` obtains the query from `unit+698`; `304E12` calls this getter, and `304E1A` zero-extends returned `AX` into `R8D` before `304E24` calls `30CFB0`, with no intervening call. The preserved prefix starts at an interior fragment, not a complete function entry. No natural caller-entry/receiver/state identity is inferred from it.

## Limits, consumers and cleanup

This is source/dataflow evidence under valid backed query/owner/table/frame accesses, normal native ABI/returns and preserved nonvolatile carriers. It is not actual command acceptance/execution, current table contents, field-writer domain, owner lifetime/reuse, natural interleaving, a safe API for all malformed inputs or whole OV-42 closure.

FABLE owns the standard producer frontier and action-availability qualifications: the getter adds no bound on non-9F valid-owner words; follow the `+714` writer/admission next. OPUS owns the effective-ID/getter versus nullable owner-resolver types/contracts and return widths, including distinct resolver results and the apparent null guard. SPEC must independently review the exact code, CFG/return-load dominance, resolver composition, retained caller scope and concrete prerequisite propagation. No peer-owned consumer is edited here.

All reads/tools are finite and handles close. No PC/game/save/config/reference change, live instrumentation or reconstruction phase occurs. Publication integrity, producer validity and independent project acceptance remain distinct; full L1+L2 is not claimed complete.
