# PKG-TECH-SCRIPTVM-VALUE: a script value from operand to typed store (FABLE, Claude Opus 5.5, 2026-09-28)

**behavior.** A zone script reads a variable (PUSHV), computes on the ScriptVM's typed value stack (arithmetic, the typed
three-way compare and its six boolean consumers, divide and modulo), and writes the result back (POPV). The write converts
to the variable's kind, saturates by width, and addresses an array element by a clamped, 32-bit flattened index; PUSHP passes
references. Every script-driven behaviour in the game passes through this path. A reimplementation that uses host arithmetic
instead of the VM's exact widths, orders, conversions and NaN results diverges on authored data.

**reproduction target.** From the accepted package alone, a developer can write a value-exact ScriptVM core covering:
- the tags (1 = int, 2 = float) and 64-entry stack;
- each variable width's load and store;
- int↔float conversion under a stated MXCSR;
- compare, divide and modulo results, including NaN, INT_MIN and zero cases;
- array addressing and reference packing.

It says which inputs fault and which are unestablished.

**scope: included.**
- operand → descriptor → six storage classes and arrays (clamp, 32-bit flatten);
- PUSHV loads by width;
- POPV conversion order, rounding by MXCSR and saturation by width (the s16 `[-32767, +32768]` off-by-one);
- the typed compare (int fast path, `cvtdq2ps` mixed, NaN → +1) and the six SETcc decisions;
- OPDIV and OPMOD (zero and INT_MIN / -1);
- PUSHP packing and its offset domain;
- the stack capacity check and the underflow / bad-tag fetch `008620C0`.

**scope: adjacent obligations.**

| obligation | owner / locator |
|---|---|
| OPUS's "no catching handler" scan (divide Z), which ASTRA 84 found can pass on a failed or truncated analysis | OPUS, `_index/candidates/script-divide-opus/`; ASTRA-REQ-FABLE-NATIVE-DIVIDE-CONSUMER-SCOPE |
| what the process does after a divide fault (native exception policy) | not claimed; needs a prepared discriminator, not live escalation |
| the game's actual MXCSR rounding mode at script time | runtime; not claimed |
| operand names in the debug companions (SN-1: T0 binding for 106 of 390) | SWE2-DATA page, FABLE-REQ-DATA-SN1-PAGE-62-ACCEPT |
| verbs (CALL/REQ) and their native bridge | 01-Script-VM-Native-Bridge verb pages; separate packages |

**dependencies.**
- BF-1 (every opcode read, FABLE 71859306c).
- BF-2 (the comparator).
- The storage-classes page (AUDITED).
- AO-2 (the VM return-value list layout).

**owner.** FABLE (Claude Opus 5.5).
**contributors.**
- ASTRA: packages 72–80, the POPV lookup / conversion / rounding / array returns.
- OPUS: `script-comparator-opus`, `script-var-ref-opus`, `script-divide-opus`.
- The storage-classes and interpreter pages carry FABLE edits.

**reviewers.** SWE2-AUDIT-SPEC (FABLE-REQ-AUDITSPEC-REVIEW-ARITH, and the earlier FABLE storage-page reviews). ASTRA is the
independent evidence producer, not the acceptor of FABLE's text.

**requirement ids.** BF-1, BF-2, BF-5, AO-2 (register); the ASTRA-REQ-FABLE-SCRIPT-* series (closed as consumer
incorporation, acceptance separate).

**evidence.**

| stage | canonical locator | class |
|---|---|---|
| operand → descriptor → class, arrays | storage page §2–§4 (`00262440`); array clamp and signed-min qualifications | static; controls `script-array-clamp`, `script-array-signedmin` |
| flatten, PUSHP packing | storage page §2.2, `PUSHP` row; `script-vm-arith-consumers` F, R | static |
| loads | storage page `PUSHV` row (`00267FC0`) | static |
| POPV conversion, rounding, saturation | storage page `POPV` row and the saturation section (`0026D5C4` s16 arm) | static; ASTRA replays of the conversion / rounding |
| compare and boolean decisions | interpreter page, "What the comparator returns"; `script-vm-arith-consumers` C | static |
| divide / modulo | same section; `script-vm-arith-consumers` D, I, M | static; ASTRA 80 guest replay of the IDIV stop |
| capacity and underflow | storage page call-chain rows (`00267560`, `00268A80` → `008620C0(1)`); `cmp …, 0x3f / jge` in every push | static; T4 and T5 accepted |

**canonical destination.** `01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md` and
`worldactor-scriptvm-interpreter.md`, plus BF-1's record. This file keeps the reading order and the item table.

**work items.**

| # | item | kind | locator | owner | reviewer | stage |
|---|---|---|---|---|---|---|
| T1 | compare / divide / flatten / PUSHP propagation and its two corrections (8cbe8b877), plus the OPMOD and coverage addendum | review | `script-vm-arith-consumers/` | FABLE | AUDIT-SPEC (FABLE-REQ-AUDITSPEC-REVIEW-ARITH) | accepted-and-incorporated: ACCEPT 2026-09-29 (`Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-0929-FABLE-BATCH.md`) |
| T2 | FABLE's earlier storage-page edits (POPV lookup, conversion, rounding, array clamp, signed min, store saturation): find each one's independent receipt, or request one | review | storage page | FABLE | AUDIT-SPEC | accepted-and-incorporated: ACCEPT for all five (SCRIPTVM-STORE-EDITS) and for 0928L / 0928M (same review file). Receipt audit 2026-09-29: no receipt or request existed for ff64e93be, 7af8e8da4, 9d30ac29c, 71214dd8c or f8a527325, so FABLE-REQ-AUDITSPEC-REVIEW-SCRIPTVM-STORE-EDITS was filed. 9f070f4bc and 99c62fe6b are under 0928L and 0928M |
| T3 | ASTRA 84's consumer scope: FABLE's pages claim no catching handler (checked); OPUS's Z repair stays adjacent | disposition | ASTRA-REQ-FABLE-NATIVE-DIVIDE-CONSUMER-SCOPE | FABLE | AUDIT-SPEC | accepted-and-incorporated: ACCEPT (FU1: `--truncate` fails all seven checks through `covered()`) |
| T4 | what `008620C0(1)` does on a stack underflow or bad tag: fault, report and continue, or a default value. The failure behaviour is inside the included scope | gap | `008620C0` (52 call sites) | FABLE | AUDIT-SPEC | accepted-and-incorporated: the ARITH review verified U byte-exact (ae062e166, storage page l.439). Prior art: `008620C0` is the retail no-op bailout (interpreter page §"`FUN_008620C0`"), and an empty pop yields 0 (storage page l.439; interpreter l.847). Added: a bad-tag entry is consumed and read as int 0, or as float 0.0 in the comparator |
| T5 | what a push past capacity does (`jge 0025F226`) | gap | `0025F226` | FABLE | AUDIT-SPEC | accepted-and-incorporated: prior art on the AUDITED storage page (l.440). A push at depth 63 is dropped (storage page l.440); `0025F226` rejoins the pc-advance tail `0025E613`, so execution continues. Capacity is 63 values, not 64 |
| T6 | end-to-end sufficiency: a fresh reader predicts, from the pages alone: s16 store of 32768 → reads -32768; `OPGT` NaN vs 1 → 1; flatten (65536, 65536)[32768, 0] → INT_MIN; OPDIV INT_MIN / -1 → fault; PUSHP `02FFFFFF` + 1 → class 3 | review | this file | FABLE | AUDIT-SPEC | accepted-and-incorporated: ACCEPT for all five cases. Four of them (s16 store, NaN compare, flatten, divide/modulo), plus conversion rounding, were accepted in FABLE-REQ-AUDITSPEC-T6-SCRIPTVM-FRESH-READER (`Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-0929-FINAL-BATCH.md`). The PUSHP case was accepted in FABLE-REQ-AUDITSPEC-T6B-PUSHP-FRESH-READER (2026-09-29): from the PUSHP row alone the reader predicted `02FFFFFF` + 1 → `73000000` (class 3, width 7) and `02000000` - 1 → `FFFFFFFF` (class 7, width 15), byte-verified the pack body at `00268166`–`00268194`, and found no page gap |

**stage.** `accepted-and-incorporated` (updated 2026-09-29, T6B verdict). T1–T6 are accepted-and-incorporated. This says nothing
about the whole database: the adjacent obligations above stay open where they live.

**blocker / next action.** None. The package reopens only at claim level, if a dependency it rests on changes (README §2).

**acceptance checks: result (2026-09-29).**
- Check 1: AUDIT-SPEC (T6, T6B).
- Checks 2–4: FABLE, on this text.
  - 2: every evidence row names a control or its class.
  - 3: T4 and T5 are stated.
  - 4: all five adjacent obligations are still open at their owners.

**acceptance checks.**
1. The T6 cases, predicted from the pages by a non-author.
2. Every stage row names a control or states its evidence class.
3. The two failure paths (T4, T5) are stated, or recorded as not established with a reason.
4. No adjacent obligation is marked closed.
