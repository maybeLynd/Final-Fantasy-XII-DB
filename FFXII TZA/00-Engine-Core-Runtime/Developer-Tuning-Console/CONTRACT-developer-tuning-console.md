---
contract: dispatch a developer console command id to one of 282 arms, keep three per-id tables aligned on one id space, and let an arm nudge the render-settings block the frame is about to read - while the same menu draws rows the dispatcher cannot reach
category: 00-Engine-Core-Runtime
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/console-command-names.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/the-second-console-table.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md
entries: ["001D1660", "001CD0E0", "001A9930", "00193D50", "001DF340"]
registry_slots: []
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the dispatch table, the arm census, the step-constant census and the second table were all
    RE-DERIVED from the authority image on 2026-09-21 (OPUS) - the 282 entries decoded and bounds-checked
    against the body's extent, the body disassembled with capstone (2,861 instructions) and every
    RIP-relative scalar-FP operand resolved through the correct section, and the second table read at the
    address its RVA actually denotes. The nine arm-catalogue slices' per-id semantics are theirs and are
    carried with attribution.
last_reviewed: 2026-09-21
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_state: opus-falsification-pass-1-2026-09-29-exe-73461d08
  crossref_clean: false
  reopened_count: 0
---

# Contract — the developer tuning console

> **Why this one is subsystem-scoped where S-40's is not.** S-06's registry row credits one primary
> page, but the directory holds **thirteen documents** — the dispatcher, nine arm-catalogue slices
> covering ids 12–293, the joined name list, a *second* per-id table, and the settings block the arms
> write. And they share invariants no single page states: **three tables keyed on one id space that
> must stay aligned**, a menu that draws a row the dispatcher cannot reach, and a block the console
> can reach only half of. Those are exactly the cross-operation facts the scope test asks about.
>
> **Provenance.** Sections 2–5, 7 and 10 are **NATIVE/STATIC**, re-derived here. The per-id
> semantics in the nine slices are theirs. Section 13 is **empty**.

## 1. Purpose

FFXII: The Zodiac Age ships with the settings screen its developers kept for themselves. Ambient
occlusion, depth of field, shadows, image-based lighting and the post-processing layer are all on,
tuned to values somebody chose with a controller in their hands, and the retail options menu exposes
none of them. **The console is the dial they used** — a menu of named rows where a press nudges one
value by a hundredth and the renderer reads the result on the very next frame.

## 2. Interface

| | |
|---|---|
| entry point(s) | `001D1660` the dispatcher, **13,753 B** (body `001D1660`–`001D4C19`, 2,861 instructions) · `001CD0E0` the row renderer |
| calling convention | Microsoft x64; the command id arrives in `r9d`. |
| parameters | `r9d` is the id. **Valid ids are 12–293**; the arms are selected after `add r9d, -0xC`. |
| return type | none established — the arms are `jmp` targets inside one body, not callees. |
| return semantics | an out-of-range id reaches a do-nothing arm and the call is a no-op (I-2). |
| callbacks / indirect dispatch | **one indirect jump**, `jmp r9` at `001D16AE`, through a 282-entry table of image-relative offsets at `001D4C1C`. |

## 3. Types

**Three per-id tables, one id space.** Keeping them aligned is this subsystem's central obligation
and is why it is contracted as one.

| table | where | stride | entries | keyed by |
|---|---|---:|---:|---|
| **arm dispatch** | `001D4C1C`, immediately *after* the body | 4 | **282** | `id − 12` |
| **labels** | `ctx + id*8 + 0x130` | 8 | **293** (ids 1–294) | `id` |
| **authored codes** | `01DF6E68` in `.data` | **16** | ~~294 (ids 0–293)~~ 1,314 (rows 0–1313) *(corrected 2026-10-02, OPUS: `+0x08` = row + 1 through row 1313; the next 16 bytes break the pattern)* | ~~`id`~~ the field id `[r15 + 0xAB4]` (`001CD0E0+0xAFF`) |

```
authored-code entry, read here from the image
  +0x00  char*  codePtr     a pointer to an ASCII code, or NULL
  +0x08  u32    sequence    EQUALS index + 1 for all 294 entries, no exception   <- corrected 2026-10-02, OPUS: for all 1,314 entries, 01DF6E68 + 1,314 x 16
  +0x0C  u32    (zero in every entry read)
```

> **CORRECTED 2026-09-25 (OPUS) - the table is 1,314 entries long, not 294.** Read to its end from the image:
> the `{codePtr, index+1, 0}` pattern holds for **1,314 consecutive entries** (`01DF6E68`..`01DFC088`, end exclusive: 0x01DF6E68 + 1,314 × 0x10); 601
> carry a code (`ous0101` at 0, `rui0108` at 200, `rbn1001` at 295, `enw0107` at 400, `mrm0204` at 600 - field-style
> map codes), and a different dword list begins at that end. **294 is the console's id space, not the table's
> extent**: the console reads one entry by its own id (`001CDBF7`, index from `[r15+0xAB4]`). The type store's
> `DeveloperTuningCodeEntry` route carries the measured 1,314. *What the other 1,020 entries serve, if anything
> outside the console, is not read here.*

**The render-settings block** is 1,132 bytes, 86 of the console's hottest addresses, ~~read by 25
functions~~ referenced by **28 functions, 24 of which access it** (the other four only take its address)
*(Corrected 2026-09-30, OPUS, on SWE2-CONTRACT's recount; `block_refs_count.py`)*. It is **two disjoint things** — a console-tunable settings area and an eight-entry
uniform array the console cannot reach — which is
[what-the-console-tunes.md](what-the-console-tunes.md)'s finding and is carried, not re-derived.

**A declared type this subsystem writes**: `PostProcessParamContext` (`_types`, 0x4A8, lazy
singleton at `[01F7F5F0]` built by `00193D50`), used by ~~**33 arms**~~ **33 call sites, reached by 16 arms** *(CORRECTED
2026-09-29, falsification pass 1: the figure counted call sites, and arms share tail code)*. It is the same block
[the render command list contract](../../17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md)
reads its per-effect switches from, and the same one
[the PPFX contract](../../17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md)
is careful not to be confused with. **The console tunes what the render command list obeys** — that
is the cross-system relationship, and it is why a console arm can change a frame.

## 4. Preconditions · postconditions · invariants

**I-1 — THE TABLE IS AFTER THE BODY AND EVERY ENTRY POINTS BACK INTO IT.** Decoded here: 282 entries
at `001D4C1C`, holding image-base-relative offsets, and **all 282 land inside `001D1660`–`001D4C19`**.
The table is `.text` payload following the last instruction, not code.

**I-2 — THE BOUND IS UNSIGNED, SO A NEGATIVE ID IS AN OUT-OF-RANGE ID.** `001D167D cmp r9d, 0x119`
then `ja` — after `add r9d, -0xC`. An id below 12 wraps to a huge unsigned value and takes the same
exit as an id above 293. **There is no error path**; both reach a do-nothing arm.
*Sharpened by pass 1:* the two no-ops share **one epilogue, entered at two points**:
- the 56 shared ids enter it at `001D4BFA`;
- the out-of-range exit enters it at `001D4C09`, after the `xmm6`, `xmm7` and `rbp` restores. Those three are saved
  only after the check (`001D168A`, `001D1699`, `001D169E`), so there is nothing to restore.

A reimplementation that routes out-of-range ids through the shared arm's full epilogue restores registers it never
saved.

**I-3 — 282 IDS, 227 DISTINCT ARMS, AND ONE ARM SERVES 56 OF THEM.** Counted here from the decoded
table: 227 distinct targets, of which `001D4BFA` is pointed at by **exactly 56 ids**. So **a fifth
of the console's ids do nothing**, and a reimplementation that gives each id its own handler has
invented 55 behaviours.

**I-4 — THE CONSOLE IS A STEPPER, AND THE STEP IS A HUNDREDTH.** Every RIP-relative operand of an
`addss`/`subss`/`movss`/`mulss` in the body, resolved through the correct section:

| constant | refs | | constant | refs |
|---:|---:|---|---:|---:|
| **0.01** | **88** | | 0.05 | 12 |
| −0.01 | 28 | | −0.05 | 8 |
| 0.02 | 19 | | −1.0 | 3 |
| 0.1 | 18 | | −0.03 | 3 |
| 0.001 | 13 | | 0.03 | 3 |

**A hundredth, referenced 88 times, is what this function is mostly made of** — a value being walked
by hand while somebody watches the screen. *One discrepancy with the page, recorded rather than
smoothed: it ranks `1.0` at 8 references and this scan finds **11**. The scan covers
`addss`/`subss`/`movss`/`mulss`; the page does not state its instruction set, so the two are
measuring slightly different things and the difference is method, not error.*

**At run time the steps are these, and two are not in the table above** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 315, which executed every id; [its package](../../_index/candidates/s06-opus-replay-console-arms/README.md) was read.)*. Started from zero, the value a
float-stepping arm writes is its step. **56 arms step by exactly 0.01**, then 0.1 (7), 0.02 (7), 0.001 (6), 0.05 (5),
1.0 (4), **0.005 (4)**, 0.03 (3) and **0.005556 (2)**. ~~The last two are loaded as no literal. The arms compute them,~~ All three are `.rdata` literals: 0.005 at `009002B4` (−0.005 at `009002F0`), 0.03 at `009002C4`, 0.005556 at `009002B8` *(corrected 2026-10-02, OPUS: the scalar-float rip operands of `001D1660`, e.g. `subss` / `addss` on `009002B8` at `001D1660+0x14F9` / `+0x150E`)*;
~~so a census of literal operands, like the one above, cannot list every step size~~ the table above omits them by its cut, not because they are computed. *The headline holds: the step is
mostly a hundredth.*

**I-5 — THE MENU DRAWS A ROW THE DISPATCHER CANNOT REACH.** The label table has **293 labels for ids
1–294** while the dispatcher accepts **12–293**. Id 294 — *"Key Kana Test"* — is a render row with
no action entry. **That asymmetry is the reason two tables exist**, and it is the load-bearing check
on the alignment: a scheme that assumed one table would have to explain away an extra row.

**I-6 — THE SECOND TABLE'S DISPLACEMENT IS AN RVA, AND READING IT AS AN ADDRESS SUCCEEDS.**
`001CDBF7` is `mov rax, qword ptr [rsi + rdx*8 + 0x1cd6e68]` with `rsi` holding the image base, so
the table is at **`01DF6E68`**, not at `01CD6E68`. Verified here: `0x1CD6E68 + 0x120000 = 0x1DF6E68`,
which is in `.data`, while the literal is not. **The failure mode is the point** — a wrong address in
this image does not fault, it returns plausible bytes, and the page that records this says its own
author dumped the wrong memory one tick after being warned. **Nothing in a wrong dump announces
itself.**

**I-7 — 111 OF THE 294 CODE ENTRIES ARE POPULATED, AND THEY ARE AREA CODES.** Read here: the qword
at each entry base is either NULL or a pointer to an ASCII string of the form *three letters + four
digits*. **111 are populated**, and they group into ~~about twenty prefixes occupying contiguous id
bands~~ **15 prefixes in 17 id bands** — `rbn`, `nal`, `dst`, `rui`, `mnt`, `sav`, `pla`, `frs`, `bog`, `mic`, `asp`, `naf`, `dor`,
`ous`, `rwr`. *That these are the engine's area codes is a **reading**, supported by the form
matching the zone-script naming family and by the regional clustering; what is measured is the count,
the shape and the banding.* **One code appears twice** — `dst0104` at ids ~~232 and 233~~ **230 and 232** — which a
reading of the table as a per-id key has to account for.
*Corrected 2026-09-26 (OPUS), on a census re-derived from the image
(`_index/candidates/s06-opus-console-tables-census/`).*
- **The duplicate's ids.** The renderer indexes the table ~~by the id itself~~ by the dword at `[r15 + 0xAB4]`, the field id, not the console id *(corrected 2026-10-02, OPUS: `001CD0E0+0xAFF` `movsxd r8, dword ptr [r15+0xab4]`, `+0xB17` `mov rax, qword ptr [rsi+rdx*8+0x1cd6e68]`)* (`001CDBDF`–`001CDBF7`: `[base + id*16 +
  0x1CD6E68]`), and `+0x08` holds `id + 1`. The two `dst0104` entries are therefore ids **230 and 232**, whose `+0x08`
  fields read 231 and 233. Id 231 holds `dst0109` and id 233 `dst0108`. The earlier "232 and 233" matched no
  convention.
- **The bands are not all contiguous.**
  - `nal` sits at ids 48–49 and again at 51, with `rwr` at 50 between them.
  - `dst` has two bands, 129–133 and 227–233.
  - Every other prefix occupies one run: `ous` 0, `mic` 53–71, `asp` 124–126, `pla` 137–149, `frs` 151–163, `bog`
    167–180, `rui` 184–202, `mnt` 209–223, `sav` 236–270, `naf` 274–282, `dor` 286 and `rbn` 289–292.

**Postcondition.** After a dispatch, either exactly one arm ran or none did; ~~the arms that step a
float have moved one value in the settings block by one constant, and the frame that follows reads
it.~~ **what an arm wrote depends on the arm, and most arms write outside the settings object** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 315, which executed every id; [its package](../../_index/candidates/s06-opus-replay-console-arms/README.md) was read.)*.
Of the 282 ids, **219** run to completion under OPUS's fixture. They split into 56 no-op arms and 3 arms that write
nothing. That leaves **160 writing arms**:

| where the arm writes | arms |
|---|---:|
| only the settings object | 41 |
| only the post-process parameter context | 12 |
| other globals, or several places (ids 30 and 31, for example, write `02CB8148` / `02CB8150`) | 107 |

The other 63 ids stop at an object the fixture did not plant, or at a trapped import. Their write scope is not
measured. So "one value in the settings block" describes 41 of 160 measured arms. A reimplementation that keeps all
console state in one settings object misses the other 119. *Each arm's writes are listed per id in the package's
`result.json`.*

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | the 282-entry table; the label table at `ctx + id*8 + 0x130`; the authored-code table at `01DF6E68` | `001D16A3`, `001CDBF7` |
| written | the 1,132-byte render-settings block, and `PostProcessParamContext` via `00193D50` (~~33 arms~~ 33 call sites, 16 arms; pass 1) | the helper census |
| allocated | `00193D50` lazily constructs the 0x4A8 block on first use | `_types` |
| deallocated | nothing | — |

**The arms reach across the engine and that is deliberate.** 79 distinct callees, including an
`Audio`-owned function (`001DBB00`), a `Resource`-owned one (`002EEEE0`) and battle-side helpers
reading the selector table at `02EBF190`. The most-used are singleton getters — `001A9930` (8 B,
45 ~~arms~~ call sites), `00193D50` (33), `001DF340` (a generic indexed dword store, 13), `001DDAB0` (10),
`001C2F40` (9). **CORRECTED 2026-09-29 (falsification pass 1): those are call sites in the body, not arms.**
Following each arm's own control flow, the arms that reach them number **14, 16, 15, 2 and 4**. `001DF340` is reached by
more arms than it has call sites, because arms share tails. **A tuning console has to reach everywhere, and this one does**, which is also why
it is not owned by any one subsystem.

## 6. Relationships

```
the console menu
   001CD0E0  row renderer  -- prints "%s%s%f", label from [ctx + id*8 + 0x130]
                           -- and reads the authored code at 01DF6E68 + id*16
   a press ->
   001D1660  dispatcher
        add r9d,-0xC ; cmp r9d,0x119 ; ja -> do-nothing         001D167D..001D1684
        jmp [001D4C1C + (id-12)*4 + image base]                 001D16AE
           -> one of 227 arms (56 ids share 001D4BFA)
                -> 001A9930 / 00193D50 / 001DF340 / 001DDAB0 / 001C2F40 ... 79 callees
                     -> the render-settings block  -> read by 24 functions (28 reference it), next frame
```

## 7. State transitions

| previous | resulting | condition |
|---|---|---|
| id in 12..293 with a real arm | that arm runs | table lookup, I-1 |
| id in 12..293 on the shared arm | **nothing** | one of the 56, I-3 |
| id < 12 or > 293 | nothing | unsigned bound, I-2 |
| a setting at *v* | *v* ± one step constant | a stepping arm, I-4 |
| id 294 | a row is drawn, no action exists | I-5 |

## 8. Script · resource · event interactions

**Three authored inputs, and they are different kinds.** The **labels** are the names the engine
prints. The **codes** at `01DF6E68` are authored area codes (I-7). The **settings block** holds
authored default values whose names are in the executable — `EnableAO`, `EnableDof`, `EnableShadow`,
`EnableIBL`, `EnableYebis`, `ShadowBias`, `AODepthFullRes`.

**No script verb reaches the console.** It is driven by the menu, and the menu by a controller.

## 9. Determinism

**RNG — none.** **Timing** — a press takes effect on the next frame, because the block the arms
write is the block the renderer reads; nothing double-buffers it. **Threading** — no lock or atomic
appears in the body; the console and the renderer touch the same block and the only thing separating
them is that both run on the main thread (see
[the graphics handshake contract](../../17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md)
I-10 for why there is no second thread here).

## 10. Failure paths and edge conditions

1. **Out-of-range id** → the shared do-nothing arm; no diagnostic (I-2).
2. **In-range id with no behaviour** → one of the 56; indistinguishable from 1 to the caller (I-3).
3. **Id 294** → drawn, not dispatchable (I-5).
4. **A NULL code pointer** → ~~183 of the 294 entries~~ 713 of the 1,314 entries (183 of the first 294) *(corrected 2026-10-02, OPUS: 601 rows carry a pointer)*; the renderer must tolerate it (I-7).
5. **A stepped value has no clamp in most arms** — ~~110 arms carry both `addss` and `subss`~~ **110 arms reach `addss`,
   and 59 of them also reach `subss`; 51 step one way only** *(CORRECTED 2026-09-29, falsification pass 1)*. The catalogue
   slices record clamped pairs only in slices C and E, so most values walk unbounded.

## 11. Observable behaviour

- **The console's own menu**: 293 named rows, each printing `"%s%s%f"` — label and current value.
- **The renderer changes on the next frame** when a value is stepped; that is the difference between
  a tuning console and a debug readout.
- `Debug_SetGilToMaximum` (`003058B0`, 10 bytes: `mov ecx, 0x5F5E0FF` = 99,999,999, then `jmp`) is
  the one command a reader will have heard of. It is **one arm of roughly 250 call sites** and is
  recorded here in that proportion rather than as the headline.
- **The differential test this contract most wants**: dispatch each of the 56 shared ids and confirm
  nothing changes, then dispatch id 294 and confirm the dispatcher rejects what the menu draws.

## 12. Reproduction formula

```
dispatch(id):                                     # 001D1660
    i = id - 12                                   # 001D166F
    if (unsigned)i > 0x119: goto doNothing        # 001D167D/84, I-2
    base = imageBase                              # 001D168F lea rcx,[rip-0xB1696]
    goto base + u32[0x001D4C1C + i*4]             # 001D16A3..001D16AE

armStep(slot, +k):                                # the 110 stepping arms
    block[slot] += k                              # k is 0.01 in 88 of the references

renderRow(id):                                    # 001CD0E0
    label = [ctx + id*8 + 0x130]                  # ids 1..294
    code  = qword[0x01DF6E68 + id*16]             # NULL in 183 of 294   <- corrected 2026-10-02, OPUS: indexed by dword [r15+0xAB4] (001CD0E0+0xAFF), not by id; 1,314 rows, 713 NULL
    print("%s%s%f", label, code?, block[slot])
```

## 13. Runtime validation

**Empty.** The console is a developer build's menu; nothing here has been observed running *(answered: see the 2026-09-25 note above, OPUS block 315 executed every id; 2026-10-02, OPUS)*.

| claim | how it was observed live | date | result |
|---|---|---|---|
| — | — | — | — |

## 14. Unresolved

1. **Whether the 111 codes are area codes** (I-7) *(answered: see the second-console-table page, Answered 2026-09-30 (SWE2-CONTRACT): map-pack names indexed by field id; 2026-10-02, OPUS)* — the form and the banding support it; nothing
   read here binds one to a map load. Resolved by following one id's arm to what it does with the
   pointer.
2. **Why `dst0104` appears at two ids** (I-7).
3. **What the 56 shared ids were** before they were retired to the do-nothing arm — the labels still
   exist for them, so the names may say.
4. **The eight-entry uniform array the console cannot reach** *(answered: see what-the-console-tunes.md, eight shadow-map cascade matrices, UQ-24 2026-09-16; 2026-10-02, OPUS)* — owned by
   [what-the-console-tunes.md](what-the-console-tunes.md) §4.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| 282 entries, all inside the body, 227 distinct, 56 on one arm | the table decoded from the image at `001D4C1C` and every entry bounds-checked against `001D1660`–`001D4C19` | 1 | PROVEN |
| The unsigned bound and the id range 12–293 | `001D166F`, `001D167D`, `001D1684`, `001D16A3`, `001D16AE` | 1 | PROVEN |
| The step-constant census | capstone over the body, 2,861 instructions, every RIP-relative scalar-FP operand resolved through its own section | 1 | PROVEN |
| The second table is at `01DF6E68`, stride 16, `+0x08 == index+1` | `001CDBF7` read as an RVA and confirmed against the section map; all 294 entries decoded | 1 | PROVEN |
| 111 populated code pointers, and one duplicate | the same decode, strings resolved and read | 1 | PROVEN |
| The label table, its 293 names and id 294 | [console-command-names.md](console-command-names.md), alignment proven four ways plus a 20-pair cross-source control | carried, tier 1 at source | VERY HIGH |
| The settings block and its two disjoint halves | [what-the-console-tunes.md](what-the-console-tunes.md) | carried, tier 1 at source | VERY HIGH |
| Per-id arm semantics | the nine arm-catalogue slices, ids 12–293 | carried | VERY HIGH |

## 16. Parity plan

| dimension | tested how |
|---|---|
| **STRUCTURAL** | the three tables' strides and extents, and the id-space alignment of I-5 |
| **STATE-TRANSITION** | §7's five edges, especially that 56 ids are no-ops |
| **EDGE-CASE** | §10, particularly the unsigned bound of I-2 |
| **CALCULATION** | the step constants of I-4, which are the whole arithmetic |
| **INTEGRATION** | that a stepped value reaches the renderer on the next frame |

**Not tested:** **RNG** (none), **SERIALIZATION** (nothing persisted here), **PRESENTATION** (what
the tuned values do to the image belongs to the render contracts), **TIMING** beyond the next-frame
claim, and **FULL SUBSYSTEM** while §13 is empty.

`001C0330` (197 B) is the display-string materialiser `001CD0E0` runs per console row: `[rcx+9] == 0` emits a two-string `Disabled` pair (`001EDF00` EASTL basic_string construct + `001A4BF0` assign), a live `[rcx+0x10]->+8` instead runs `001B3860` for the real value text, and neither emits `NULL` - the three display states of a tuneable

Interior anchor `001C0381` (function `001C0330`).

## Cross-subsystem neighbours

The console borrows shared helpers rather than owning them, and two of its named helpers are
shared across real layer boundaries. **Presentation**: `00193D50`, the singleton getter 33 of
the dispatch arms lean on, is also reached by the render pass list `00187950` and its siblings
`00189CE0` and `0018B1B0` - the page uses the same getter the renderer does, with no shared
state beyond it. **Resource**: `002EEEE0` is the `Resource`-owned callee §5 already credits;
`001A4BF0`, the string-assign `001C0330` runs to materialise `Disabled`/`NULL`, is shared with
resource-side callers `001AD130`, `001B1750` and `001B4D70`, and `00193D50` is reached again
from `001A7A50`. These are crossings of shared machinery, not obligations this page absorbs.

`001B3860` (71 B) is the value-record materialiser `001C0330` calls for a live tuneable (and `001B4D70` on the font side): it zeroes the `+0`/`+8`/`+0x10` header triple, `001EDF00`-constructs the EASTL basic_string at `rcx+0x18` from the caller's `[rdx+0x18]` source, then `001A4BF0`s the `{ptr, len}` view `[rbx]`/`[rbx+8]` into the record - a three-word header plus an owned string body, returned in `rax`

Interior anchor `001B3885` (function `001B3860`).

`001C0480` (181 B) is the keyed string-field emit `001CD0E0` runs per tuneable: a live `[rcx+9]` flag with a `[rcx+0x10]` table materialises the `EASTL basic_string` scratch record via `001EDF00`, `001E3E90` resolves the handle into `rdx`, and `001BE660(rdi, table, string)` performs the keyed write; a dead source instead zeroes the destination's three header qwords, `001EDF00`-builds an empty `basic_string` at `rdi+0x18`, and `001A4BF0`s the empty `01CEB638` range into `rdi` - emit or blank, never partial

Interior anchor `001C04CC` (function `001C0480`).

## Falsification pass 1 — 2026-09-29 (OPUS): the tables hold; two counts were call sites, not arms

Every claim was re-derived from the shipping image (`73461d08…`) by
[`falsify_developer_tuning_console.py`](../../../Tools/analysis-kit/gfz-scripts/falsify_developer_tuning_console.py). Each
check states its killer first. `audit_crossrefs.py` ran on this folder first.

| check | killer searched for | result |
|---|---|---|
| D0 physical | a different extent or instruction count; an anchor that decodes otherwise | survives: 13,753 B, 2,861 instructions; `001D166F`, `001D167D` and `001D16AE` as cited; `001D168F` loads the image base |
| D1 I-1 | a table entry outside `001D1660`..`001D4C19` | survives: all 282 are inside; the 283rd dword points outside, so the table ends where stated |
| D2 I-2 | a signed branch in the dispatch | survives, **sharpened**: `ja` only; out of range enters the shared epilogue at `001D4C09`, not `001D4BFA` (see I-2) |
| D3 I-3 | a write or call in the shared arm | survives: 227 distinct arms; `001D4BFA` ×56 is a pure epilogue |
| D4 I-4 | any constant count differs | survives: all eleven, including 1.0 ×11. The census also finds 0.5 ×4, −0.02 ×3 and 0.002 ×3, which the table did not list |
| D5 I-5 | id 294 inside the dispatcher's arithmetic range | survives: 294 − 12 = 282 > 0x119 |
| D6 I-6 | the literal read as an address yields the table, or the RVA reading does not | survives: `rsi` = image base at `001CD17F`; 20/20 entries fit at `01DF6E68` and 0/20 at `01CD6E68` |
| D7 I-7 | any count, band or duplicate differs | survives: 1,314 entries with `+0x08 = index+1`; 111 populated; 15 prefixes in 17 bands; `dst0104` at 230 and 232 |
| D8 §5 | the per-callee figures are not arm counts | **corrected**: they are call sites (45/33/13/10/9 exact); the arms reaching each are 14/16/15/2/4 |
| D9 §9 | a lock prefix or `xchg` on memory | survives: none |
| D10 §10.5 | another count of arms with both `addss` and `subss` | **corrected**: 110 arms reach `addss`; 59 also reach `subss` |
| D11 §11 | `003058B0` other than `mov ecx, 0x5F5E0FF; jmp` in 10 bytes | survives |

**Method note, and the attack on my own first run.**
- My first arm census cut the body at each next table entry. That found 14 arms for `001A9930` and 59 for "both",
  and it looked like the page was wrong twice.
- Arms share tail code, so that cut is wrong. The counts above follow each arm's control flow from its entry,
  through direct branches, to `ret`.
- The page's own figures are then **exact as call-site counts**. What was wrong was the word "arms", not the numbers.

**Crossref (audit_crossrefs, this folder): open neighbours, recorded rather than resolved.**
- Audio: `001CD0E0` → `002DEBA0`, `001D1660` → `001DBB00` / `002DEBA0`, `001DBB00` → `00210B30`.
- CoreRuntimeScheduling: `0017D6E0` → `001A9930` / `001C2F40`.
- Platform: `001DD170` → `001DF340`.
- PlatformOnlineAchievements: `001CD0E0` → `003166F0`, `007A0C60` → `001DF340`.
- Rewards: `003058B0` → `00254EE0` (the gil setter's target).

`crossref_clean` stays `false`.

**Not attacked by this pass:**
- the nine slices' per-id semantics and the label table (carried);
- the settings block's two halves (carried);
- §4's runtime-step paragraph (FABLE, on block 315's execution).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Audio — SERVICE, 62 edges: the console's audio legs, which the pass above recorded as open.**
- The dispatcher `001D1660` calls `001DBB00` and `002DEBA0`, and the renderer `001CD0E0` calls `002DEBA0`.
- `001DBB00` sets a sound category through the audio registry resolver `00210B30` and `002112D0`. `00210B30` has 54
  audio callers because every audio body resolves through it.
- `002DEBA0` has one more audio caller, `00362F70`.
- The display-object getter `001DDAB0` has two callers filed Audio, `00182E80` and `001DC3D0`. `00182E80` is the
  display-height getter, so that label is the ledger's, not an audio relationship.

What the audio calls do is owned by the 18 pages.

**Rewards_Progression_Economy, Items_Equipment_Shops_License, CombatAction, CombatFormula — CLIENT, thirteen edges
through one setter.** The console's gil arm writes through `GameState_SetGil` (`00254EE0`). That is the game's one
gil setter, and its other callers are the whole economy:
- `GameState_AddGilClampedAndNotify`, `GameState_SetGilClampedNonnegative` and `BattleUnit_ProcessDefeatRewardsAndLoot`
  (rewards);
- `Shop_CommitPurchaseItemAndGil`, `Shop_CommitSaleItemAndGil` and the two inventory gil classes (items and shops);
- `BattleAction_PrepareExecutionResources`, `BattleAction_ConsumeExecutionResources` and
  `BattleAction_RefundExecutionResources` (combat action);
- `BattleFormula_ApplyTargetResult` (combat formula).

`Debug_SetGilToMaximum` calls it too. The economy pages own gil; this contract owns only that the console arm calls
the same setter.

**PlatformOnlineAchievements — CLIENT, six edges.** The renderer `001CD0E0` calls the achievement counter `003166F0`
(112 B). That counter is also called by `00315E90`, `00316760`, `00316A50` and `SaveImage_FinalizeHeaderAndChecksum`,
and `00316A50` also reaches the gil setter. The online init `007A0C60` calls the generic indexed dword store
`001DF340`.

**Platform — SERVICE, four edges.** The platform init `001DD170` calls `001DF340` and the device helpers `00623C10`,
`00623CB0` and `00624490`.

**Save_Load_Settings — MECHANICAL, three edges.** The frame step `0017D6E0` calls `SaveloadManager_GetSingleton` and
`SaveloadManager_ProcessPendingCaptureCopy`, and `SaveImage_FinalizeHeaderAndChecksum` calls `003166F0`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the arm catalogue read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*
