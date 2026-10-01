# S-06 runtime: which invariants an execution can test, and a stub-free plan for them (OPUS, 2026-09-25)

**Row:** S-06 developer tuning console. The runtime cell is NOT MET, and the binding gap is *"runtime evidence"*. No
record executes the dispatcher `001D1660`. EXP-190 reaches the label fetcher `001CD0E0` only as a **stub**. The
contract is `00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md` (OPUS). This note
scores nothing.

## Evidence class per invariant

| inv. | claim | class | does execution add anything? |
|---|---|---|---|
| I-1 | 282 table entries at `001D4C1C`, all pointing into the body | image data (a decoded table) | no |
| **I-2** | the bound is unsigned: ids < 12 and > 293 take the same exit (`001D166F add r9d, -0xC`; `001D167D cmp r9d, 0x119`; `ja 001D4C09`) | behaviour | **yes** |
| **I-3** | 227 distinct targets; `001D4BFA` serves 56 ids | image data **plus** behaviour: `001D4BFA` is the common epilogue (restore xmm6/rbp/xmm7, then `001D4C09` pops and returns), and all 338 `jmp 0x1d4bfa` sites converge on it. So those 56 ids **do nothing** | **yes**, for "do nothing" |
| **I-4** | the console is a stepper; 0.01 is the dominant step | an operand census **plus** behaviour | **yes**, for one stepping arm |
| I-5 | 293 labels for 1..294 against dispatcher ids 12..293 | image data | no |
| I-6 | the second table is at `01DF6E68` (an image-base-relative displacement) | an instruction reading (`001CDBF7`) | no |
| I-7 | 111 of 294 code entries are populated, with area-code shapes | image data (a census) | no |

## A stub-free plan (for ORACLE)

The dispatcher's out-of-range exit and its shared do-nothing target call nothing. Calling `001D1660` with these ids
exercises I-2 and I-3 **with no stubs**:
- **I-2:** ids 0, 5, 11 (these wrap below 12), 294 and `0xFFFFFFFF`;
- **I-3:** one id whose table entry is `001D4BFA`.

For each, assert no memory write outside the stack and no call. Also run **one id whose arm only `addss` / `subss`
a global by 0.01 before `jmp 001D4BFA`** (I-4). If that arm calls one of the frequent helpers (`001A9930` ×45 and
`00193D50` ×33 call sites), both are contract entries; pick an arm that calls neither, or run them real.

The plan does not repeat anything EXP-190 did. EXP-190 stubs `001CD0E0` as a format fetcher. The contract's view of
`001CD0E0` is FABLE's `69a3d0d44`: *it prints the settings fields, it does not consume them*.
