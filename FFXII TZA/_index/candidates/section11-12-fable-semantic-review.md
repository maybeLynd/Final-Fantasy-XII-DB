# SECTION-11 / SECTION-12 (Update11 / Update12) — FABLE review of the semantic claims

FABLE (Claude Opus 5.5), 2026-09-24. **Scope:** the behaviour claims (`S11-1`…`S11-7`, `A12-1`…`A12-10`)
and the seven semantic row refinements that OPUS's
type review (`_index/candidates/section12-opus-type-review.md`, not yet committed) routed to FABLE. **Out of scope:**
- widths, offsets and type readiness (OPUS's review);
- the first-line exact-behaviour audit, which [REVIEW-POLICY](../_inbox/REVIEW-POLICY.md) gives to
  `SWE2-AUDIT-SPEC` and which this review does **not** replace.

FABLE did not produce either section, so this is an independent review. It is not an acceptance of
the whole package, and it changes no TEAM, L2 or completion state.

## 1. The producers' instruments reproduce

Both `run_review.py` runners were re-run from the overlay folders, unmodified. The environment was
WSL Ubuntu 22.04, GCC 11.4.0 and Python 3.10.12, against this checkout's EXE (sha256
`73461d08…21f8`, identical to the manifests).

| section | result |
|---|---|
| 12 | `PASS`. 85 bodies and 8 data spans hash-verified. 139 assertions, identical repeat. **8 of 8** code mutants fail at their declared first check. |
| 11 | `PASS`. 58 bodies and 7 data spans. 146 assertions, identical repeat. **10** mutants rejected. The retained-record review's 14 checks pass and 8 corruptions are rejected. |

A reproduction is the producer's consistency, not an independent derivation, so §2 is what carries
this review.

## 2. Re-derived from the shipping image with FABLE's own disassembler

| claim | FABLE's independent reading | verdict |
|---|---|---|
| `A12-1` the insertion-state gate reads the **issuer** | `00268850` keeps its 2nd argument in `r15` (`00268883`) and the resolved actor in `rbx` (`002689E8`, from `003587C0`). `002689F0`/`002689F7` test `[r15+2]==1` and `[r15+0x10]==0`. Its only callers are two sites in the interpreter `0025E4C0` (`0025F7D0`, `002602E1`), which pass its own `r15`, the executing actor (`0025E4D5`; its `+0x14` byte is read at entry). | **ACCEPT** |
| `A12-3` start preserves command scratch | `ScriptExecutionState_ResetCore` `0025D460` stores qwords `+0x00` and `+0x08`, a dword at `+0x10`, a word at `+0x14` and a byte at `+0x16`, then `ret`. Nothing at or past `+0x17` is touched. | **ACCEPT** |
| `A12-6` wait polarity and completion footprint | The jump table at `0025E3CC` decodes to kinds 0→`0025E127`, 1/2→`0025E0BE`, 3→`0025E027`, 4→`0025E091`, 5→`0025E00A`, 6→`0025E058`, 7→`0025E083`. Kind 3 stays blocked while `003DBF60` finds a matching entry (`0025E045 jne`). Kind 4 stays blocked while `003DC050` finds **no** request entry (`0025E0A9 je`). | **ACCEPT** |
| `A12-7` the list cursor is a forward scan, not a barrier | `00267420` resolves the list from slot `+0x1C` through `0020E600`. It advances the word at slot `+0x22` (`00267471 inc`) only past inactive actors and returns 1 at the first active actor without rewinding. Passed actors are not re-tested on later polls. | **ACCEPT** |
| row `ActorWaitSlot +0x27 settled`: kinds 3/6/**7** write it; 4 and 5 do not | Kind 7 calls `00267420` and then **`jmp 0x25e06e`** into kind 6's tail, which writes `+0x14 = 1` and `+0x27 = 1` (`0025E076`/`0025E07A`). Kind 5 settles at `0025E01E` and kind 4 at `0025E0B5`, neither writing `+0x27`. **HEAD's row omitted kind 7 because the arm reaches the write through a shared tail.** | **ACCEPT**, and HEAD is corrected by it |
| row `ActorResourceEntry +0x02 channel`: the mode, not only the sign, selects detached removal | `ActorResource_RemoveActiveEntry` tests `byte [entry+0x10] == 4` at `003DB2F8` **before** reading the channel sign at `003DB2FE`. State 4 forces `ebp = -1` and the detached list head `+0x61` (`003DB311`/`003DB314`), whatever the channel byte holds. | **ACCEPT** |
| `S11-1` shared depth is reset at entry, even on refusal | `0025E4D8 mov dword [02099AC0], r11d` (zero) precedes the refusal test at `0025E4FF`/`0025E502`, which returns 1. | **ACCEPT** |
| `S11-5` the instruction budget is 65,536 | `0025E4FA mov ecx, 0x10000`, decremented per dispatched instruction at `0025E570`. | **ACCEPT** |

**Not independently re-derived** (reproduced by the producers' harness only): `A12-2`, `A12-4`,
`A12-5`, `A12-8`, `A12-9`, `A12-10`, `S11-2`, `S11-3`, `S11-4`, `S11-6`, `S11-7`, and the rows
`ActorResourceEntry +0x0C`/`+0x10` and `ActorWaitSlot +0x00`/`+0x14`/`+0x16`. They are not rejected.
They wait for the first-line audit.

## 3. What the sections do not claim, and what stays open

Both sections state their own limits, and those limits stand:
- no live session;
- no outer frame pipeline `0025D9E0`;
- no runtime actor allocation or reuse, which remains ASTRA's separate question;
- no complete opcode coverage;
- no resource lifetime of authored scripts.

One cross-link for the store: the list-wait reference at slot `+0x1C` is an **image-address
reference** resolved through `0020E600`. Its meaning therefore inherits whatever the image-address
base holds, and the base is **zero at load, with one undriven in-image store route**
([the authored-table contract](../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) §7).

## 4. Verdict and routing

**FABLE semantic verdict: ACCEPT at the stated scope for the eight re-derived items above. No
defect was found in the sampled claims.** The package still needs:
1. the first-line audit by **`SWE2-AUDIT-SPEC`** (exact behaviour; REVIEW-POLICY default routing);
2. OPUS's review of SECTION-11's `ActorWaitSlot` head retile and the `VmValueStack` lifetime row,
   which OPUS's Section-12 note left open;
3. publication of the overlays themselves, which touch many shared canonical files, coordinated
   through **FRONTIER**. Nothing in this review commits the overlay text.
