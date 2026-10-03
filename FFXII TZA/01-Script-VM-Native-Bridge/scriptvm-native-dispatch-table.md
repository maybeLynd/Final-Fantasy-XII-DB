---
system: ScriptVM native dispatch table
category: 01-Script-VM-Native-Bridge
status: AUDITED
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 2
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-07
audit:
  passes: 4
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-index-mapping-exhaustive
  crossref_clean: true
  reopened_count: 0
---

# ScriptVM native dispatch table

> Every zone script verb — `setweatherslot`, `openfullscreenmenu`, all ~1,950 of them — is a
> number that indexes one table to reach the native code that runs it. This locates that table.

> **A successful application of this document's own rule, 2026-09-02.** Four handlers were named
> from this table and then **verified by the argument-count check prescribed below** — rows `0x050F`
> and `0x0514` (1 arg each) against handlers containing exactly one
> `VMValueStack_PopInt32CoerceFloat32`, and rows `0x0513` / `0x0516` (0 args) against handlers
> containing exactly one `VMResult_WriteInt32`. All four matched. See
> [`../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
> §2b. The table is usable exactly as this document prescribes: as a lead, confirmed by arity.

~~**DOCUMENTED.**~~ **AUDITED.** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`)* The table is the **`result` callback column** of a three-callback native command
table (**begin / poll / result**, 32-byte records) whose base is `0x01EED700` — see section 12, which
resolves every contradiction this document previously carried. Base, stride, extent and all aggregate
figures were re-derived in pass 33 and are unchanged; the frame of reference is what moved.

## 1. What the player sees

Nothing directly — but everything scripted. When a cutscene changes the weather, opens a
menu, moves an NPC or checks what you are standing on, a zone script issues a numbered verb
and this table decides which native function answers.

For a modder this is the bridge between the two halves of FFXII: the authored `.ebp` scripts
you can decompile and edit, and the compiled engine you cannot. Knowing which native function
a verb reaches is what makes a script edit predictable instead of experimental.

## 2. Native mechanism

**Table base:** VA `0x01EED700`. For call id `n` (valid while `n < 1496`, the dword at `tbl + 0`) the three accessors read **begin `[tbl + 0x20n + 8]`, poll `[tbl + 0x20n + 0x10]`, result `[tbl + 0x20n + 0x20]`**; nothing reads `tbl + 0x20n + 0x18`. Drawn as a record, call `n`'s 32 bytes therefore start at **`tbl + 8 + 0x20n`** - begin `+0`, poll `+8`, unused `+0x10`, result `+0x18` - and the table occupies `01EED700`..`01EF9208`. `0x01EED720` is `result(0)`. *History: relabelled onto this frame 2026-09-16 (FABLE, OPUS) from the accessor bodies; moved back to a `01EED720` record frame 2026-09-19 (OPUS, `b3ffc2b5c`) on a per-slot census; **restored 2026-09-19 (FABLE) on `OPUS-CON-DISPATCH-TABLE-RECORD-0-AT-PLUS-8`**, the accessors re-disassembled the same day. A census cannot choose between two frames that are rotations of one another - both give clean columns - and this page's own 2026-09-16 block says so. What does choose: (1) the accessor arithmetic; (2) the `01EED720` frame's last record would own `01EF9208`..`01EF921F`, which holds three `0xFFFFFFFF` qwords, and `01EF9220` is a float table that other code (`003590A0`) loads with `movss`; (3) in that frame record `n` would hold `result(n)` beside `begin(n+1)` and `poll(n+1)`. The charge that the relabel was self-inconsistent assumed the result slot is `+16`; by the accessor it is `+0x18`, and `01EED708 + 0x18 = 01EED720`.*
**Stride:** `0x20` (32 bytes) per record
**Index:** ~~*approximately* the call ID — `record N = verb N` holds for `0x021A` and `0x040C`
but is **off by one** at `0x048C`/`0x048D`. At least one discontinuity exists; its location is
unknown (**I-6**).~~ **CORRECTED 2026-09-07 (propagated 2026-09-11, ASTRA-REQ-FABLE-STALE-I6-AY10):** **the call ID, exactly** —
`record N = verb N` for every one of the 1,496 family-0 records (§15–§16, 645 anchors at 89.1 %
against a 55.7 % shifted baseline, no step in any bucket). The `0x048C`/`0x048D` "off by one" was
a column confusion: `003462D0` is `begin(0x048D)` in that record's `+8` (§12, §15). **I-6 closed.**
**Extent:** ~1,496 records covering IDs `0x0000`–`0x05D7`

Each record holds up to four 8-byte pointers into `.text`:

| Field count | Records |
|---:|---:|
| 0 handlers | 105 |
| 1 handler | 1,155 |
| 2 handlers | 122 |
| 3 handlers | 113 |
| ~~4 handlers~~ | ~~1~~ **— see the correction below** |

> **CORRECTED 2026-09-02 — no record carries four handlers.** The single four-field record was an
> **out-of-bounds read**. In this document's frame, record `N`'s field `+24` is
> `table + 56 + 32*N`; for the last record, `N = 1495`, that address is past the end of family 0's
> 1,496 records and reads whatever `.data` holds next. Swept in the correct frame — 1,960 records
> across all five command tables — the third pointer slot is **null everywhere**. Field counts for
> records 0..1494 are unaffected. See §13.
>
> > **The correction is confirmed independently, and the 1,960-record extent reintroduces the same
> > defect — 2026-09-02.** An independent census of `.data` function pointers, certified by
> > `IMAGE_REL_BASED_DIR64` base relocations and built without reference to this document, was run
> > over both extents:
> >
> > | extent | certified slots | offsets used within the 32-byte record | owners |
> > |---|---:|---|---|
> > | **1,496 records** (`01EED720`..`01EF9220`) | 1,739 | `+0` 1,234 · `+8` 276 · `+16` 229 · **`+24` = 0** | ScriptVM 1,685, Movement 19, Party 8 |
> > | 1,960 records (`01EED720`..`01EFCC20`) | 1,941 | `+0` 1,285 · `+8` 327 · `+16` 279 · **`+24` = 50** | …plus **CombatFormula 160** |
> >
> > At 1,496 records **no certified pointer occupies `+24` anywhere**, which is exactly this
> > correction's claim, reached from a different instrument. At 1,960 records the `+24` slot becomes
> > occupied 50 times **and 160 `CombatFormula` pointers appear** — because
> > **`0x01EFA5C0`, the base of the [combat formula step table](../08-Combat-Formula/Step-Table/combat-formula-step-table.md),
> > sits exactly at record 1653 of this frame.** `(0x01EFA5C0 - 0x01EED720) / 0x20 = 1653.00`.
> >
> > So the 1,960-record sweep runs 307 records past this table and into a different one. **The
> > out-of-bounds read was corrected and then re-entered at a larger scale by the extent adopted to
> > fix it.** The `+24`-is-null result holds; the frame it was verified in does not.

Most verbs resolve to a single function at `+0`. A minority carry additional entries at
`+8`, `+16`, `+24` — plausibly lifecycle phases for verbs that span frames, but **that reading
is unproven**.

Verbs with IDs above `0x05D7` — the `0x2000+` developer/debug range — are **not** in this
table and must live elsewhere. 468 catalog entries fall outside it.

### Aggregate validation

Cross-referencing the ff12-script catalog (1,954 authored verb names) against the table:

| Check | Result |
|---|---:|
| IDs in range with a `.text` handler | **1,224** |
| IDs in range with a null slot | 262 |
| Handlers pointing **outside `.text`** | **0** |
| Handlers not landing on a known function entry | **0** |
| Distinct handler functions | 1,166 |
| Verbs sharing a handler | 58 |

Owner distribution of the 1,224: **1,202 `Script/VM Native Bridge`**, 9 Movement, 9 unowned,
3 Party, 1 ActorEntity.

Those are strong signals. A wrong base or stride would scatter pointers outside `.text` and
off function entries; neither happens once in 1,224 samples.

### The contradiction as first resolved — superseded by section 10

> **Superseded 2026-09-02.** The conclusion below (*an index discontinuity*) was
> reached without knowing that `003462D0` is in the table at record `0x048C`,
> field `+8`. Read section 10 first; the argument-count reasoning here is sound and
> is retained, but the index-shift conclusion drawn from it is not.

Three verb→handler pairs were independently established by earlier GN analysis. Two reproduce
exactly; one conflicted:

| Verb | GN evidence | This table | |
|---|---|---|---|
| `0x021A setweatherslot` | `003565C0` | `003565C0` | ✅ |
| `0x040C getweatherslot` | `00356250` | `00356250` | ✅ |
| `0x048D openfullscreenmenu_48d` | `003462D0` | `00346DA0` | ❌ |

**Settled by reading both bodies:**

```c
003462D0:                                        // 2 arguments
    VMValueStack_PopInt32CoerceFloat32(stack)    // twice
    FUN_002e1a60(b, a)                           // fullscreen selector -> request submit

00346DA0:                                        // 0 arguments
    value = FUN_00254710()
    VMResult_WriteInt32(result, value)           // a plain getter
```

`003462D0` pops two operands and drives the fullscreen-menu request path — it **is**
`openfullscreenmenu_48d` (2 args). `00346DA0` takes no input and returns an integer, matching
`getmapgroundtype_48c` (0 args, returns). Argument counts from the authored catalog settle it
independently of either claim.

**The GFZ was right. This document's index mapping was wrong.**

~~The table therefore does **not** uniformly satisfy `record N = verb N`. It holds exactly for
`0x021A` (538) and `0x040C` (1036), and is off by one record around `0x048C`/`0x048D` — where
`00346DA0`, a verb `0x048C` handler, sits in slot `0x048D`. A uniform base shift is not the
answer either: moving the base one record breaks `0x021A`, which is independently corroborated
by its decompiled body.~~

~~So the region between those points contains at least one **discontinuity** — a gap, a variable
record size, or a segmented layout — and its location is unknown. Extent of the correct region
is **I-6**.~~

> **Struck (propagated 2026-09-11, ASTRA-REQ-FABLE-STALE-I6-AY10).** Both paragraphs were superseded by §10 and closed by §15–§16:
> the table satisfies `record N = verb N` uniformly; `00346DA0` sits in record `0x048D` because it
> is that verb's *end* callback (`+0x10`), not a displaced `0x048C` handler (§12). Kept as the
> record of how the wrong reading arose.

**What this costs.** The aggregate checks (0 handlers outside `.text`, 0 off a function entry,
1,202/1,224 correctly owned) remain true and still show the table is real and mostly
well-formed. They simply **do not establish per-row correctness**, because a systematic
off-by-one still lands on valid neighbouring functions in the same subsystem. That is the
precise failure mode a favourable summary statistic cannot detect — and the reason a single
counterexample outranked it.

## 3. Key addresses

| Address | Role |
|---|---|
| `0x01EED700` | **dispatch table base (VA)** - count `1496` at `+0`; call 0's begin and poll callbacks at `+8` and `+0x10` (`0034CF90`, `0034DCC0`); `+0x18` the slot no accessor reads. *Restored 2026-09-19 (FABLE): these 32 bytes are not a header - the two `.text` pointers are what the begin and poll accessors return for call 0* |
| `0x01EED720` | **`tbl + 0x20` - `result(0)`**, the fourth qword of call 0's record (`01EED708 + 0x18`); null for call 0. File offset `0x01DCBD20`. *The `01EED720` record frame of `b3ffc2b5c` was withdrawn 2026-09-19 (FABLE); see the Table base line* |
| `003565C0` | `setweatherslot` handler — cross-validated against decompiled body |
| `00356250` | `getweatherslot` handler — cross-validated |
| `003462D0` | `openfullscreenmenu_48d` — **proven** by body: pops two operands, drives `002E1A60` |
| `00346DA0` | a zero-argument getter, consistent with `getmapgroundtype_48c` |

Full mapping: [`Verb-Dispatch/scriptvm-dispatch.tsv`](Verb-Dispatch/scriptvm-dispatch.tsv) (~~1,224~~ 1,493 rows *(corrected 2026-10-02, OPUS: the file's own header and its data rows, extended 2026-09-19 and 2026-09-26)*). **Moved into the database 2026-09-08** — it had lived only in
`Tools/work/rtti/`, which is **gitignored**, so the script↔engine bridge was one `rm -rf work/` from gone and invisible to every query. **The `handler` column was re-derived from the binary before the move: 1,224 of 1,224 agree with `table[+0x00]` at `01EED720 + 0x20*id`, 0 outside `.text`, 0 off a function entry** (`scriptvm_dispatch_verify.py`). `verb` and `args` still come from the authored external catalog and are **not** verifiable against the image; the file carries that split per column. **Rows are a lead, not
fact** — the index mapping ~~is known wrong in at least one region~~ is the call id exactly *(answered: CORRECTED 2026-09-07, §2 — the `0x048C`/`0x048D` step was a column confusion, I-6 closed; 2026-10-02, OPUS)*. Verify a handler's argument
count against the catalog before relying on it.

## Which verbs are asynchronous - by the accessors, and by their authored names (2026-09-19, FABLE)

A verb is asynchronous when it has a begin or a poll callback. Read with the accessor arithmetic of the Table base
line, **304 of the 1,496 call ids are asynchronous**
([async_verbs_by_accessor.py](Verb-Dispatch/members/async_verbs_by_accessor.py),
[async-verbs-by-accessor.tsv](Verb-Dispatch/members/async-verbs-by-accessor.tsv)).

**The authored names agree with the accessor frame and with no other.** Every one of the 304 has a name in the bundled
community catalogue, and the list reads like the things a script waits for: `wait`, `waitv`, `aask`, `messync`,
`keywait`, `movesync`, `rcmove`, `move`, `turn`, `turnsync`, `camerasync`, `voicesync`, `mapjump`, `motionsync`. In a
frame one record later the asynchronous verbs would include `getpos` and `setangzx`. *The catalogue is an external
authored source, so a name is a lead and not proof; what it adds here is that it was written without reference to this
table's layout, and it picks the same frame the accessor bodies do.*

*(answered: the TSV's begin / poll columns were re-framed 2026-09-19 (OPUS) and the 259 asynchronous ids added the same day — see its header; 2026-10-02, OPUS)* ~~**`scriptvm-dispatch.tsv` has the two callbacks one call id early.**~~ Over its 1,224 rows the `handler` column equals
`result(n)` on all 1,224. Its trailing begin / poll pair - 146 rows carry one - equals the accessors' `(begin, poll)(n)`
on **2** rows and `(begin, poll)(n + 1)` on **146**. Example: `movesync` is call id `0x3D` and its poll is `00356A90`
([the verbs that only wait](verbs-that-only-wait-and-verbs-that-do-nothing.md) has it right); the TSV attaches
`00356A90` to `0x3C setvelrotangzx`. **259 of the 304 asynchronous verbs have no row in that file at all**, because it
lists the call ids that have a result callback - so `wait`, `move` and `turn` are absent from it. A warning is in the
file's header; the re-frame of the two columns is routed to OPUS.

**And the bodies agree with the names.** Three party handlers read whole the same day, named here by the accessor
frame: `00352AF0` is the begin of `0x35C` **`removeguestbattlemember`** - and the body removes a selector *only when it
is a guest*; `00350160` is the begin of `0x358` **`removebattlemember`** - and the body moves a main character out of
the runtime roster, and only while more than one remains; `0034CDF0` is the poll of `0x354` **`removepartymember`** -
a three-state machine around the main-character remover. In the TSV `00350160` sits on the row of `0x357
getbattlemember`, a getter. **Accessor arithmetic, authored names and handler behaviour: three lines, one frame.**

## 4. Data structures and formulas

```
ScriptVM native dispatch table
  base   = 0x01EED700   (VA)    <- the TABLE base: count 1496 at +0
  call n : begin  = [base + 0x20*n + 0x08]      GetBeginCallback  003DC270
           poll   = [base + 0x20*n + 0x10]      GetPollCallback   003DC240
           (unused  base + 0x20*n + 0x18         read by no accessor, null for all 1,496)
           result = [base + 0x20*n + 0x20]      GetResultCallback 003DC2A0
  as a record: call n = 32 bytes at base + 8 + 0x20*n : begin +0, poll +8, unused +0x10, result +0x18
  extent : 0x01EED700 .. 0x01EF9208 ; from 0x01EF9208 filler, at 0x01EF9220 a float table
  (restored 2026-09-19, FABLE. The 0x01EED720 record frame pairs result(n) with begin(n+1)
   and poll(n+1) and runs 0x18 bytes past the table; a per-slot census cannot see either.)
  stride = 0x20 bytes
  record N serves call ID N          <- HOLDS for all 1,496 records (§15); the 0x048C/0x048D
                                        "failure" was a column confusion (§12) — I-6 closed

Record layout (interpretation UNPROVEN beyond field +0)   <- corrected 2026-10-02, OPUS: settled by §2 (restored 2026-09-19): begin +0, poll +8, unused +0x10, result +0x18 from tbl + 8 + 0x20n (003DC28E, 003DC25E, 003DC2BA)
  +0x00  ptr   primary handler        1,234 records non-null
  +0x08  ptr   secondary                277 records non-null
  +0x10  ptr   tertiary                 230 records non-null
  +0x18  ptr   quaternary                 0 records carry a HANDLER  <- see the correction below
```

> **The `+0x18` count of 1 was not an over-read — corrected 2026-09-11 (OPUS).** Reading all 1,496
> records end to end gives `+0x00` 1234 non-null with **all 1234 inside `.text`**, `+0x08` 277 of which
> 276 are, `+0x10` 230 of which 229 are, and `+0x18` exactly 1 which is not. **The three non-code
> values are one record.** Call id `0x5D7`, the last, holds `0xFFFFFFFF` in `+0x08`, `+0x10` **and**
> `+0x18` — a terminator, inside the table rather than past it. What reading past the end actually
> looks like starts at record 1496, where the bytes are float bit patterns (`0.1f`, `50.0f`, `1.0f`,
> `0.05f`) and a byte permutation — which confirms the extent from the other side. So the handler
> counts are **1234 / 276 / 229 / 0**, and no verb carries a fourth entry: a reimplementation that
> dispatches on `+0x18` dispatches on a sentinel. Installed as `ScriptNativeDispatchRecord` in
> `_types/`.

> **SUPERSEDED 2026-09-16 (OPUS) — the block above is kept as the record of what was believed, and
> its conclusion is withdrawn.** The `2026-09-11` reading reinstated the `tbl + 32 + 32N` frame and
> called the three `0xFFFFFFFF` a *terminator inside the table*. **The three accessors settle it and
> they were not consulted**, so the correction below in §13 and “The real structure” stands:
>
> ```
> GetBeginCallback  003DC270   shl rax,5 / mov rax,[rax+rcx+8]        -> tbl +  8 + 32*id
> GetPollCallback   003DC240   shl rax,5 / mov rax,[rax+rcx+0x10]     -> tbl + 16 + 32*id
> GetResultCallback 003DC2A0   inc rax / shl rax,5 / mov rax,[rax+rcx] -> tbl + 32 + 32*id
> ```
>
> **Why the wrong frame keeps looking right (added 2026-09-19, FABLE, at OPUS's suggestion after the frame was moved
> the wrong way a second time).** The result accessor is the only one of the three **with no displacement in its
> memory operand**. It reaches `tbl + 0x20n + 0x20` by incrementing the *index* before the shift, so its load reads
> `mov rax, [rax + rcx]` - which, without the `inc rax` three instructions earlier, is "offset 0 of a record". The
> result callback is the commonest of the three, so this is the instruction a reader meets first, and it is exactly
> the evidence a record base of `01EED720` would leave. A per-slot census then confirms whichever frame it is run in.
> **Read the `inc`.**
>
> All three bounds-check `edx` against `dword [rcx]`, the count at `tbl+0` (`1496`). Against a
> record based at `tbl + 8 + 32N` that is **begin `+0x00`, poll `+0x08`, result `+0x18`**, and
> **`+0x10` is reached by no accessor at all** — which is why it is null in all 1,496 records.
> A whole-table classification confirms it: under this frame no slot holds a value that is neither
> null nor a `.text` pointer, and only **3** records are entirely null; under the `tbl+32` frame
> **three** non-pointer `0xFFFFFFFF` land in pointer slots and **105** records are entirely null.
>
> **Why the wrong frame survived.** `GetResultCallback`'s `tbl + 32 + 32*id` is *the same address*
> as the old frame's “record `id`, field `+0x00`”, so every handler the old frame reported was a
> real result callback and every spot-check passed — including the 1,224-row catalog check. **The
> data was right and the boundary was wrong**, which is exactly the shape that defeats
> verification-by-sampling.
>
> `_types/` followed the superseded block and has been re-framed to match (OPUS 2026-09-16):
> `beginHandler +0x00`, `pollHandler +0x08`, `unusedSlot +0x10`, `resultHandler +0x18`, all four
> **PROVEN** on the accessor bodies rather than on a byte census.

**Handler address** — ~~correct only where the index mapping holds~~ the index mapping holds for
every record (`I-6` closed 2026-09-07, §15–§16; propagated 2026-09-11, ASTRA-REQ-FABLE-STALE-I6-AY10):

```
handler(id) = *(u64 *)(0x01EED720 + id * 0x20)      // == RESULT callback of verb id, i.e.
                                                    //    tbl + 32 + 32*id, the record's +0x18.
                                                    //    NOT the "+0 callback": corrected
                                                    //    2026-09-16 (FABLE). The VALUE is
                                                    //    unchanged - it is exactly what
                                                    //    GetResultCallback (003DC2A0) reads.
```

**Range:** IDs `0x0000`–`0x05D7` only. The `0x2000+` debug range uses a different table.

## 5. Call chain

```
authored .ebp zone script
  -> compiled bytecode, native call opcode with a numeric verb id
     -> ScriptVM dispatch
        -> table[id]  ->  native handler
           -> engine subsystem (WorldAreaField, UI, Movement, ...)
```

Worked example, fully corroborated:

```
setweatherslot(int)            authored verb, id 0x021A
  -> table[0x021A] = 003565C0  ScriptVM handler
     -> pops the VM integer, validates field/map context, clamps to 1..3
     -> 0026D910(slot)         WorldAreaField apply owner
     -> 0026D8F0()             arms initialization-restore state
```

**Rule that still applies:** a VM wrapper is authored-intent evidence, never a replay seam.
This table tells you *which* native function a verb reaches; the seam is that native function,
not the verb.

## 6. Modding notes

- **`scriptvm_dispatch.tsv` is the script↔engine bridge.** Decompile a zone with
  `ff12-script.exe`, find the verb, look up its handler, read that function.
- **Verify any individual row before relying on it** — see the contradiction in §2. Confirm
  the handler's body matches the verb's argument count and apparent purpose.
- **262 in-range verbs have a null slot.** Those exist in the catalog with no native handler —
  compile-time constructs, or unimplemented in this title.
- **58 verbs share a handler**, so one function can serve several verbs; do not assume 1:1.
- **Debug verbs (`0x2000+`) are elsewhere.** 468 catalog entries are outside this table.
- **XIIOnline:** unchanged guidance — never invoke a VM wrapper as a replay seam. Use it to
  find the native owner, then use that.

## 7. What is not known

- [x] ~~The `0x048D` / `003462D0` contradiction.~~ **RESOLVED 2026-09-02** — settled by reading
      both bodies against the catalog's argument counts. The GFZ was correct; this document's
      index mapping was wrong.
- [x] ~~**Where the index mapping breaks.**~~ **CLOSED 2026-09-07** — `record N = verb N` holds
      across all **1,496** family-0 records. **645 independent anchors** (catalog-known verbs with a
      measured VM pop count) agree at **89.1 %** against a measured shifted baseline of **55.7 %**,
      with **no step in any 128-record bucket**. Residual: a compensating pair of shifts inside one
      anchor-free window ≤ 25 records is not excluded; nothing else is. Section 15. **I-6.**
      *(The 2026-09-02 withdrawal reached the right answer by a circular route — it filtered on a
      reconciled `arity` column that takes the catalog's value whenever catalog and measurement
      disagree, so it selected only rows that already agreed. Section 15 redoes it against
      `cat_args` directly. Recorded in `COVERAGE.md`, because the conclusion surviving does not make
      the method sound.)*
- [x] ~~Why record `0x048C` carries three handlers while its neighbours carry one, and which of
      `003476B0` / `00352E00` serves `getmapgroundtype_48c`.~~ **ANSWERED 2026-09-07** — it does not.
      **`0x048D` `openfullscreenmenu_48d` is the only durative command in the neighbourhood** and all
      three handlers are its own: begin `003462D0`, poll `00352E00`, result `00346DA0`.
      `getmapgroundtype_48c` is instantaneous and its handler is `003476B0`, its own `result`.
      Section 15. **I-7.**
- [x] ~~What fields `+8`, `+16`, `+24` mean.~~ **ANSWERED 2026-09-02** — they are the **next**
      command's callbacks. This document's frame is 24 bytes above the true record boundary, so
      `+0` = `result(N)`, `+8` = `begin(N+1)`, `+16` = `poll(N+1)`. "Lifecycle phases" was the
      right instinct; they belong to the neighbouring command. Section 12. **I-2.**
- [x] ~~Where the `0x2000+` debug verbs dispatch from.~~ **ANSWERED 2026-09-02** — they are
      **family 2** (`0x2000 >> 12 == 2`), which uses the shared default command table. This
      document can only see family 0. See
      [`Native-Command-Lifecycle/native-command-lifecycle.md`](Native-Command-Lifecycle/native-command-lifecycle.md). **I-3.**
- [x] ~~What the other 24 bytes of each record hold when the pointer fields are null.~~
      **ANSWERED 2026-09-07** — the record is four pointer slots; `begin`, `poll`, `result` are
      three of them and the fourth, at record `+0x10`, is **zero in all 1,496 records** and read by
      no accessor. The earlier *"1 record uses `+24`"* was the read past the end of the table that
      section 13 identified. Section 15. **I-4.**
- [x] ~~Why 262 in-range verbs have no handler.~~ **ANSWERED 2026-09-07 — the premise was wrong.**
      262 records lack a **result** callback; only **3** lack a callback of any kind, and none of
      those 3 is a named catalog verb. The other ~~**259 implement `begin` and `poll`**~~ **259** lack a `result`: 160 have `begin` and `poll`, 73 `begin` only and 26 `poll` only *(corrected 2026-10-02, OPUS: family 0 under the five command tables read under the accessor frame - begin `tbl + 8 + 0x20n` (`003DC28E`), poll `+ 0x10` (`003DC25E`), result `tbl + 0x20(n + 1)` (`003DC2BA`))*: they are
      durative commands, and a durative command has nothing to return. Section 15. **I-5.**
- [x] **UQ-64.** ~~No handler body has been read except the three already covered by prior work.~~
      **STALE BY SEVENTY-THREE, measured 2026-09-16 (FABLE)** — and the measurement gives the question
      a better shape than the retraction does. Joining
      [`Verb-Dispatch/scriptvm-verb-table.tsv`](Verb-Dispatch/scriptvm-verb-table.tsv)'s five callback
      columns (`begin`, `poll`, `slot2`, `result`, `arg_handler`) against every address cited anywhere
      in the corpus: **1,886 distinct handler entries**, **76 with an interior citation on a document**
      — the same test `verify_doc_addresses` and `engine_explained` use — across **37 pages**, with
      `_index/` excluded because the register mirrors citations rather than making them.
      **`1,810 of 1,886 are cited only at their entry`**, which is the honest remainder: named, not
      read. **None is uncited.** Among those read: `setnpcname`, `setshopname`, `sethp`, `sethpmode`,
      `mes`, `partyusemapid`, `mapsoundplay`, `lockmapjump`, `unlockmapjump`, `entrysync`, `resetJobs`,
      `setposoffset`, `partystdmotionrecover`.
      *Found while triaging the register rows whose own text carries a universal negative
      (`Tools/work/FABLE/drift5/handlers_read.py`). The same measurement is what `CY-3` needed: not one
      handler body is read **on `what-each-script-verb-touches.md`**, and 76 are read elsewhere.*
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md. See the register row.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Table base, stride and direct-ID indexing | four known handler addresses located in one region; spacing between `0x021A` and `0x040C` is exactly `(0x040C-0x021A) * 0x20`; both indices equal their call IDs | 2 |
| Records are 32 bytes with a pointer at `+0` | byte dump around two known entries: handler at `+0`, remaining 24 bytes zero | 1 |
| Mapping is not spurious | across 1,224 catalog IDs, **0** handlers fall outside `.text` and **0** miss a function entry | 2 |
| Ownership coherence | 1,202 of 1,224 handlers are `Script/VM Native Bridge`-owned | 2 |
| `setweatherslot` / `getweatherslot` rows | reproduce the independently decompiled handlers exactly | 1 + 2 |
| The index mapping is **not** uniformly `record N = verb N` | `003462D0` pops two VM operands and drives the fullscreen request path (= `openfullscreenmenu_48d`, 2 args); `00346DA0` takes none and returns an int (= `getmapgroundtype_48c`, 0 args). The table places them one slot later than the catalog | 1 |

**Why this is PARTIAL rather than DOCUMENTED.** *(answered: the off-by-one was a column confusion, I-6 closed 2026-09-07, and the front matter says `status: AUDITED`; 2026-10-02, OPUS)* Every aggregate check passed cleanly, and the
temptation was to call 1,224 rows proven and treat the outlier as noise. Doing so would have
published a systematically off-by-one mapping in at least part of its range — and because an
off-by-one still lands on a valid, correctly-owned neighbouring function, **no aggregate check
in this document would ever have caught it.**

**A note on which side was wrong.** The prompt for re-examining this was the observation that
the GFZ can itself be wrong — which is true, and now recorded in the evidence standard. But
testing it here found the opposite: the GFZ's attribution was correct and the fresh derivation
was not. The principle is *settle conflicts with evidence*, not *distrust the older claim*.
Both directions of deference are the same mistake.

## 9. Related

- [`../03-World-Area-Field/Weather/weather-slot-state-model.md`](../03-World-Area-Field/Weather/weather-slot-state-model.md) — the `setweatherslot` chain this table's best-corroborated row feeds
- [`../16-UI/Request-Router/ui-request-router.md`](../16-UI/Request-Router/ui-request-router.md) — where `openfullscreenmenu` leads, and the source of the disputed attribution
- [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md) — why one counterexample outranks the aggregate

## 10. Falsification pass 2026-09-02 — the discontinuity does not exist

**Attack chosen.** This document carries a live open question (**I-6**: where the index mapping
breaks) and prescribes its own test — *verify a row by checking the handler's argument count against
the catalog*. That test is mechanical: count direct `E8` calls to the VM pop primitives
(`VMValueStack_PopInt32CoerceFloat32` `00267E10`, `VMValueStack_PopNumericDiscard` `00267DB0`)
inside a handler's body. So it was run over **all 1,224 rows** rather than one at a time.

### SURVIVED: every structural figure, reproduced from the binary

The table was re-read directly out of the EXE (hash-checked `73461d08...721f8`):

| Claim | Re-derived |
|---|---|
| `result(0)` slot VA `0x01EED720` = file offset `0x01DCBD20` | **`01DCBD20`** |
| non-null per accessor: result / begin / poll / unread | **1234 / 277 / 230 / 0** = **1,741** callbacks over the 1,496 call ids. *Restored 2026-09-19 (FABLE). `b3ffc2b5c` changed this to 276 / 229 = 1,739: that is the count over the byte extent `01EED720`..`01EF9220`, which leaves out call 0's begin and poll at `01EED708` / `01EED710`. 1,739 is a true count of that extent - the 2026-09-02 relocation census above used the same extent - and 1,741 is the count of what the accessors can return.* The `+24` count was separately an out-of-bounds read, §13 |
| records by field count 0/1/2/3/4 | **105 / 1155 / 122 / 113 / ~~1~~ 0** over **1,496** records |
| catalog rows with a `.text` handler | **1,224** |
| handlers outside `.text` | **0** |
| handlers not on a function entry | **0** |
| distinct handler functions | **1,166** |
| verbs sharing a handler | **58** |
| owner split | **1,202** Script/VM, 9 Movement, 9 unowned, 3 Party, 1 ActorEntity |

Not one figure drifted.

### WITHDRAWN: there is no index discontinuity

The off-by-one conclusion rested on this: verb `0x048D` `openfullscreenmenu_48d` should reach
`003462D0`, but the table gives `00346DA0`, so the index must be shifted. **The table does contain
`003462D0`** — a full sweep of all 1,496 records finds it at exactly one place:

```
record 048C:   +0 = 003476B0     +8 = 003462D0     +16 = 00352E00     +24 = --------
record 048D:   +0 = 00346DA0     +8 = --------     +16 = --------     +24 = --------
```

`scriptvm_dispatch.tsv` records **only field `+0`**, so `003462D0`'s presence was invisible to the
comparison that produced the contradiction. The premise *"the table places them one slot later than
the catalog"* is not what the table says.

**And a region-wide shift is independently refuted.** Arity agreement across the whole table:

| alignment | n | match | rate |
|---|---:|---:|---:|
| field `+0` vs `args(id)` | 1224 | 850 | **69.4 %** |
| field `+0` vs `args(id-1)` | 1113 | 456 | 41.0 % |
| field `+0` vs `args(id+1)` | 1113 | 434 | 39.0 % |

Broken into 24 bands of `0x40` ids, **`self` beats `prev` in every single band** — including the
`0x0480` band that contains the disputed rows (34 vs 15). A systematic `+1` shift would invert that
comparison wherever it applied. It never does.

The heuristic is ~70 % accurate, not 100 % — pops inside loops, inlined pops and non-integer operand
types all cost it. That makes it unfit to prove any single row, and well fit to detect a *systematic*
shift, which is what was claimed.

### The argument-count reasoning was right; only the conclusion drawn from it was wrong

`003462D0` contains **exactly 2** calls to a pop primitive — confirming `openfullscreenmenu_48d`
(2 args) by byte counting, independent of the decompiler reading in section 2. `00346DA0` contains
**0**. Both halves of the original argument reproduce. What does not follow is the index shift.

### I-2 advanced: a lead on what `+8` holds

If `+8` of record N held verb **N+1**'s handler, that alone would explain `0x048C` carrying
`openfullscreenmenu_48d`. Tested by arity:

| alignment | n | match | rate |
|---|---:|---:|---:|
| field `+8` vs `args(id+1)` | 44 | 31 | **70.5 %** |
| field `+8` vs `args(id)` | 121 | 46 | 38.0 % |
| field `+8` vs `args(id+2)` | 123 | 56 | 45.5 % |

70.5 % is the same rate field `+0` achieves on its own correct alignment. **But this is a lead, not a
finding:** n is only 44, the three rows are drawn from different subsets so their rates are not
strictly comparable, and the pattern **does not extend** — `+16` vs `args(id+2)` gives 47.7 %, no
better than baseline. A simple "record N packs verbs N, N+1, N+2" scheme would show it at `+16` too,
and does not. Recorded against **I-2** for whoever tests it on the handler bodies.

### What this changes for a modder

The practical guidance is unchanged and now better founded: **read all four fields of a record, not
just `+0`.** The one handler this document went looking for and could not find was in the record the
whole time, one field along.

## 12. Falsification pass 2026-09-02 (third) — the table is a *three-callback* command table

**Attack chosen.** None, initially: this was found while reading `VMNativeCommandDispatch_*` in the
Script/VM category for an unrelated document. It resolves this document's oldest confusion outright,
so it is recorded here.

### The real structure

`VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`) fills an array of **16 family tables**
at `0x02B57EF0`: twelve share a default at `0x01F26720`, and families **0, 3, 5 and 7** get their
own. **Family 0's table is `0x01EED700`** — and its first dword is **1496**, exactly the record count
this document has reported since it was written.

The three accessors give the layout without ambiguity:

```
GetBeginCallback (003DC270):   *(void **)(tbl +  8 + 32*id)
GetPollCallback  (003DC240):   *(void **)(tbl + 16 + 32*id)
GetResultCallback(003DC2A0):   *(void **)(tbl + 32 + 32*id)
```

So a command is **three callbacks in a 32-byte record**: **begin**, **poll**, **result** — a
script-visible operation that starts, is polled while it runs, and delivers a result.

### This document has been reading one column of that table

```
documented base 0x01EED720  =  0x01EED700 + 0x20  =  tbl + 32
documented record N         =  tbl + 32 + 32N     =  the RESULT callback of command N
```

Verified against every id this document names:

| id | verb | begin | poll | **result** | this document recorded |
|---|---|---|---|---|---|
| `0x021A` | `setweatherslot` | — | — | **`003565C0`** | `003565C0` |
| `0x040C` | `getweatherslot` | — | — | **`00356250`** | `00356250` |
| `0x048C` | `getmapgroundtype_48c` | — | — | **`003476B0`** | `003476B0` |
| `0x048D` | `openfullscreenmenu_48d` | **`003462D0`** | `00352E00` | **`00346DA0`** | `00346DA0` |

**Every row this document reports is the `result` column.** That is not an error of extraction — the
values are right — but the frame was wrong, and the wrong frame produced two long-running puzzles.

### Both old puzzles dissolve

**The "GFZ contradiction" was never a contradiction.** Section 2 recorded that GN analysis attributed
`003462D0` to `openfullscreenmenu_48d` while this table gave `00346DA0`, and concluded the index
mapping was wrong. **Both are correct**: `003462D0` is that command's **begin** callback and
`00346DA0` is its **result** callback. The arity reasoning in section 2 also stands — a `begin` pops
the operands (2 for `openfullscreenmenu`), a `result` writes the return value (0 pops) — it simply
identified the two callbacks rather than two commands.

**I-2 is answered.** The mysterious extra fields are the *next* command's callbacks, because the two
frames differ by 24 bytes:

| this document's field | actually |
|---|---|
| `+0` | **result** of command N |
| `+8` | **begin** of command N+1 |
| `+16` | **poll** of command N+1 |
| `+24` | the unused slot of record N+1 |

That is why `003462D0` appeared at "record `0x048C`, field `+8`" in pass 33 — it is
`begin(0x048D)`. And it explains the field-count histogram: most commands are instantaneous and have
only a `result`, which is why **1,155 records showed exactly one non-null field**.

*(The "one record showed four" that this paragraph also tried to explain does not exist — it was a
read past the end of the table. §13.)*

### What was right, and stays

Base, stride, extent, the 1,224 catalog rows, 0 handlers outside `.text`, 0 off a function entry,
1,166 distinct handlers, 58 shared, and the owner split — all re-derived in pass 33 and all unchanged.
The recipe/interpreter findings in sections 10 and 11 are unaffected: the interpreter indexes
`0x01EFA5C0`, a different table.

### Status

The document moves to `DOCUMENTED`. Its data was always correct; **its frame of reference was one
column off, and naming the column resolves every open contradiction it carried.**

## 14. All five command tables enumerated — from the bound the accessors enforce

**The four tables beyond family 0 had never been enumerated.** They are now, and not by walking
outward from a base: **every accessor bounds the id against the table's own first dword**, so the
extent is a value the code reads, not a shape inferred from contents.

```asm
VMNativeCommandDispatch_GetBeginCallback  (003DC270)
VMNativeCommandDispatch_GetPollCallback   (003DC240)
VMNativeCommandDispatch_GetResultCallback (003DC2A0)

    movsxd rax, ecx                     ; family
    lea    rcx, [rip -> 02B57EF0]
    mov    rcx, qword ptr [rcx+rax*8]   ; the family's table
    test   rcx, rcx      ; je  -> NULL
    cmp    edx, dword ptr [rcx]         ; <-- THE BOUND: the table's own record count
    jge    -> NULL
    ; begin  = [rcx + 32*id +  8]
    ; poll   = [rcx + 32*id + 16]
    ; result = [rcx + (id+1)*32]        ; == rcx + 32 + 32*id
```

`VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`, 89 B) writes the array: a
`rep stosq` of `0x01F26720` over all 16 slots, then four overrides at `+0x00`, `+0x18`, `+0x28`,
`+0x38` — families **0, 3, 5, 7**.

| family | table base | records | id range | non-null `.text` callbacks |
|---:|---|---:|---|---:|
| **0** | `01EED700` | **1,496** | `0x0000`-`0x05D7` | 1,741 |
| **3** | `01F281B0` | **147** | `0x3000`-`0x3092` | 153 |
| **5** | `01F29418` | **1** | `0x5000` | 2 |
| **7** | `01F29440` | **104** | `0x7000`-`0x7067` | 131 |
| 1, 2, 4, 6, 8-15 | `01F26720` *(shared default)* | **212** | `0xN000`-`0xN0D3` | 250 |
| | | **1,960** | | **2,277** |

**1,960 matches the total this document already stated**, reached here from the five counts
independently rather than from the same source.

~~**The four tables abut exactly**~~ **Three of the four joins abut exactly; the default's end leaves eight zero bytes before family 3** *(corrected 2026-10-02, OPUS: records run to `base + 8 + 0x20×count`: `01F281A8`..`01F281B0` is zero, family 3 ends at `01F29418` and family 5 at `01F29440`)*, which is why a contents walk cannot find their edges: the default's
records end at `01F281A8` and family 3's base is `01F281B0`; family 3's records end at `01F29418`,
which **is** family 5's base; family 5's end at `01F29440`, which **is** family 7's base. **There is
no gap, no terminator and no padding between them** — only the record counts separate them, and a
walk that trusts "looks like a code pointer or null" runs straight from one table into the next.

### The id encoding, proven from the consumer

`VMNativeCommand_ExecuteLifecycle` (`002621D0`, 461 B) is the **only** caller of all three
accessors, and it splits the id before calling them:

```asm
00262205  sar  r12d, 0xc        ; family = id >> 12
0026220C  and  r15d, 0xfff      ; index  = id & 0xFFF
```

**So a command id is `family:index` with a 4-bit family and a 12-bit index**, and the accessors take
the two halves as separate arguments. Independent confirmation from the other end: authored script
primitive `0x3053` resolves to family 3 index `0x053`, whose **result** callback is
`thunk_FUN_0023a520` — see
[the spawn tunables document](../05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md),
which reached the same table from the authored-script side without knowing this frame.

### This resolves the 501-slot cluster

[The unowned-code census](../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md)
reports 734 `.data` pointer slots outside every documented span, **501 of them ScriptVM-owned and
clustering around `01F26xxx`**, and calls them *"consistent with the four further ScriptVM tables."*
They are those tables. Counting the callbacks in the default, 3, 5 and 7 tables gives **536 non-null
`.text` pointers, 500 of them owned by `Script_VM_Native_Bridge`** — a one-slot difference against
the census's 501, which is an attribution difference on a single pointer and not an extent
difference. **The cluster is fully accounted for; the "genuinely undocumented remainder" of ~233
slots is unaffected.**

## 13. Correction 2026-09-02 — the four-handler record was a read past the end of the table

**There is no command with four callbacks.** Swept in the frame section 12 established — 1,960
records across all five command tables, `table + 8 + 32N` with fields `begin / poll / unused /
result` — the third pointer slot is **null in every record of every family**.

**Where the phantom came from.** This document's frame is 24 bytes above the true record boundary, so
its "record `N`, field `+24`" is `table + 56 + 32*N`. For the final record, `N = 1495`:

```
old frame, record 1495, field +24
  = 0x01EED700 + 56 + 32*1495 = 0x01EED700 + 0xBB18 = 0x01EF9218
family 0's records end at
  = 0x01EED700 +  8 + 32*1496 = 0x01EED700 + 0xBB08 = 0x01EF9208
```

**Sixteen bytes past the end.** Every other record's `+24` reads the *next* record's unused slot,
which is genuinely null; the last record has no next record, so it read past the table.

**And the value it found is not a pointer at all.** `0x01EF9218` holds `0x00000000FFFFFFFF` — one of
three consecutive `FFFFFFFF` fillers sitting between the command table and the float table that
follows it:

```
01EF9200 : 0000000000342560     <- the last real callback in family 0
01EF9208 : 00000000FFFFFFFF     <- table ends here; filler
01EF9210 : 00000000FFFFFFFF
01EF9218 : 00000000FFFFFFFF     <- counted as "a fourth handler"
01EF9220 : 3DCCCCCD42480000     <- 0.1f, 50.0f - the float table
```

**Why this is worth more than the fix.** The same document reports, three lines above the histogram,
that **0 handlers point outside `.text`** — and `0xFFFFFFFF` is not in `.text`. The outlier was
counted as *non-null* by one check and never shown to the *pointer-validity* check that would have
rejected it in one step. Two aggregates over the same data, only one of them applied to the row that
mattered.

It then survived into two documents as *"one record carries four handlers"* and *"unused in every
record but one"*, each treating it as a small mystery to be explained rather than a value to be
bounds-checked. **A one-record frame offset does not announce itself at the start of a table; it
announces itself at the end**, in exactly the one row nobody re-reads.

The general form: **when a sweep produces exactly one outlier at the boundary of the swept range, the
first hypothesis is the range, not the data.** This is the same failure family as three other defects
recorded on 2026-09-02 — a plausible-looking result produced by an instrument nobody checked.

**Nothing else moves.** Base, stride, extent, the 1,224 catalog rows, the `+0 / +8 / +16` counts,
1,166 distinct handlers, 58 shared and the owner split were all re-derived independently and are
unchanged; the field-count histogram is correct for records 0..1494. See
[`Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`](Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md)
§10 for the sweep.

## 14. The family tables, bounded by their own headers — 2026-09-02

The extent question is settled, and not by walking outward from a base. **The consumer reads the
record count out of the table's first dword**, so every table declares its own length.

### The accessor, complete

`VMNativeCommandDispatch_GetPollCallback` at `003DC240`, 39 bytes:

```asm
003DC240  movsxd rax, ecx                 ; family index
003DC243  lea    rcx, [0x02B57EF0]        ; the family array
003DC24A  mov    rcx, [rcx + rax*8]       ; table = familyArray[family]     <- 8-byte stride
003DC24E  test   rcx, rcx ; je  fail      ; family not installed -> 0
003DC253  cmp    edx, [rcx]               ; id  vs  *(int32 *)table         <- THE DECLARED COUNT
003DC255  jge    fail                     ; id >= count -> 0
003DC257  movsxd rax, edx
003DC25A  shl    rax, 5                   ; id * 0x20
003DC25E  mov    rax, [rax + rcx + 0x10]  ; return *(void **)(table + 0x20*id + 0x10)
003DC263  ret
fail:     xor eax, eax ; ret
```

`VMNativeCommandDispatch_GetBeginCallback` (`003DC270`) and `…GetResultCallback` (`003DC2A0`) are
~~the same 36 bytes at a different field offset~~ 39 and 41 bytes *(corrected 2026-10-02, OPUS: `003DC270` (0x27 bytes) and `003DC2A0` (0x29 bytes); the result accessor has no field displacement, `003DC2BA inc rax / shl rax, 5`)*. So:

```c
callback(family, id) = (id < *(int32 *)familyArray[family])
                     ? *(void **)(familyArray[family] + 0x20*id + FIELD)
                     : NULL;
```

### The families are sparse, and there are four installed

~~`VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2F0`) is nine instructions and installs~~ `VMNativeCommandDispatch_InitializeFamilyTables` starts at `003DC2D0` (89 B): a `rep stosq` puts the default `01F26720` into all sixteen slots, then nine instructions from `003DC2F0` install *(corrected 2026-10-02, OPUS: `003DC2D5`–`003DC2E8`; `003DC2F0` is an interior address)*
**four** bases. Because the array is indexed `[array + family*8]`, the four destination globals give
the family numbers directly:

| family | destination | base | declared count | extent = base + `0x20`×count |
|---:|---|---|---:|---|
| **0** | `02B57EF0` | `01EED700` | **1496** | ~~`01EED700`..`01EF9200`~~ `01EED700`..`01EF9208` *(corrected 2026-10-02, OPUS: records start at `tbl + 8`, `003DC28E`)* |
| **3** | `02B57F08` | `01F281B0` | **147** | ~~`01F281B0`..`01F29410`~~ `01F281B0`..`01F29418` *(corrected 2026-10-02, OPUS: as row 0)* |
| **5** | `02B57F18` | `01F29418` | **1** | ~~`01F29418`..`01F29438`~~ `01F29418`..`01F29440` *(corrected 2026-10-02, OPUS: as row 0)* |
| **7** | `02B57F28` | `01F29440` | **104** | ~~`01F29440`..`01F2A140`~~ `01F29440`..`01F2A148` *(corrected 2026-10-02, OPUS: as row 0)* |

~~**Families 1, 2, 4 and 6 are never installed** — which is why~~ **Families 1, 2, 4, 6 and 8–15 all get the default `01F26720`** *(corrected 2026-10-02, OPUS: the `rep stosq` at `003DC2E8`)*; the accessor still null-checks the table
pointer before touching it. The four extents do not overlap.

**Family 0's declared count is `0x5D8` = 1496**, read from `*(int32 *)01EED700`. That is §1's
"~1,496 records covering IDs `0x0000`–`0x05D7`" — **stated by the data rather than estimated**, and
it is the figure §13's 1,960-record sweep overran.

### `01EED720` is `table + 0x20`

The record base this document has used throughout is **one record above the table base**. The table
header occupies record 0's `+0` field: at `01EED700` the four qwords are
`0x5D8` (the count) · `0034CF90` · `0034DCC0` · `0` — ~~so record 0's `+0` slot holds the count and its~~ so the count is a header and the next two qwords are command 0's `begin` and `poll`; record 0 starts at `tbl + 8` *(corrected 2026-10-02, OPUS: `003DC28E` reads begin at `[tbl + 0x20n + 8]`)*; its
begin/poll fields are live. Recorded as a measurement; **this section does not claim it resolves the
`0x048C`/`0x048D` off-by-one in §6**, which involves the id→record mapping rather than the base.

### No family uses the `+0x18` field — verified against declared counts

Certified function pointers by field offset, each family swept only to its own declared extent:

| family | `+0x00` | `+0x08` | `+0x10` | `+0x18` |
|---:|---:|---:|---:|---:|
| 0 | 1,233 | 277 | 230 | **0** |
| 3 | 143 | 6 | 4 | **0** |
| 5 | — | 1 | 1 | **0** |
| 7 | 73 | 27 | 30 | **0** |

**Zero across all four tables.** §2's "no record carries four handlers" now holds against four
independently-declared extents rather than one guessed one.

> **What that zero is, in the frame the accessors decide — FABLE, 2026-09-16.** The four columns
> above are offsets from the **old** record base `01EED720`, so each maps onto the real frame as
> `record_old(id) + k  =  record_new(id) + 0x18 + k`:
>
> | column above | what it actually is |
> | --- | --- |
> | `+0x00` | **result** callback of `id` |
> | `+0x08` | **begin** callback of `id + 1` |
> | `+0x10` | **poll** callback of `id + 1` |
> | `+0x18` | the **unreached slot** of `id + 1` — the one at `record_new + 0x10` |
>
> **So "no family uses `+0x18`" is, correctly stated, "the slot no accessor reads is null in every
> record" — and those are two independent facts that agree.** `VMNativeCommandDispatch_GetBegin/Poll/
> ResultCallback` read `+0x00`, `+0x08` and `+0x18` of `record_new` and **nothing reads `+0x10`**;
> this table, measured before the frame was settled, finds that same slot empty across all four
> families. That is corroboration, not a coincidence.
>
> **The numbers above are deliberately not rewritten.** Relabelling shifts three of the four columns
> by one record, which changes *which* record each count belongs to — that is a re-measurement and
> not a relabel, and it belongs to whoever measured it. **This note says what the columns mean; it
> does not restate what they counted.**

### A fifth table exists and this initializer does not install it

**232 certified `Script_VM_Native_Bridge` pointers fall outside all four declared families**, almost
all of them between `01F26728` and `01F28180`. The dword at `01F26720` is **212**, and
`01F26720 + 0x20 × 212 = 01F281A0` — landing `0x10` below family 3's base.

That is the shape of a fifth table of the same format, ~~**not installed by `003DC2F0`**~~ installed in every slot first by `003DC2D0`'s `rep stosq` *(corrected 2026-10-02, OPUS: `003DC2D5`–`003DC2E8`)*, which
matches §13's own reference to *"all five command tables"* while this initializer installs four. Its
base, count and extent are **consistent with** `01F26720` / 212 / `01F281A0`; that is a fit to the
header convention, not a traced installation. **BI-x: find what installs it** — the accessor's
`familyArray` is BSS, so whatever writes that slot is the answer, ~~and it is not `003DC2F0`~~ and it is `003DC2D0` itself *(corrected 2026-10-02, OPUS: `003DC2E1 lea rdi, 02B57EF0` / `003DC2E8 rep stosq`, sixteen qwords)*.

One further slot sits at exactly `01EF9200`, family 0's first address past its declared count.

### The five tables do not abut — there are small gaps

The count sits at `base + 0` in all five, verified byte-for-byte:

```
01EED700  d8 05 00 00   = 1496      01F29418  01 00 00 00   = 1
01F26720  d4 00 00 00   = 212       01F29440  68 00 00 00   = 104
01F281B0  93 00 00 00   = 147
```

`01F26728` holds `0050D660`, a function pointer — it is record 0's `+0x08` field, **not a base**.
Taking the base there instead would read a count of 5,297,760.

Laying the five extents end to end:

| table | base | end (`base + 0x20`×count) | next base | gap |
|---|---|---|---|---:|
| default | `01F26720` | ~~`01F281A0`~~ `01F281A8` | `01F281B0` (family 3) | ~~**16 B**~~ **8 B** *(corrected 2026-10-02, OPUS: records start at `tbl + 8`)* |
| family 3 | `01F281B0` | ~~`01F29410`~~ `01F29418` | `01F29418` (family 5) | ~~**8 B**~~ **0 B** *(corrected 2026-10-02, OPUS: as above)* |
| family 5 | `01F29418` | ~~`01F29438`~~ `01F29440` | `01F29440` (family 7) | ~~**8 B**~~ **0 B** *(corrected 2026-10-02, OPUS: as above)* |

So the tables are adjacent but **not contiguous** — ~~16, 8 and 8 bytes of slack~~ 8, 0 and 0 bytes of slack *(corrected 2026-10-02, OPUS: the extents end at `base + 8 + 0x20×count`)*. They are still
invisible to a contents walk, because the gaps are too small and too irregular to read as
terminators; the boundary is the count each table declares, not anything present at its edge.


## 15. Falsification pass 2026-09-07 — the index mapping tested on all 1,496 records, and three neighbouring questions closed

**`xiionline-61`, against GN160** `fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708`
and the authorized EXE `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, read
directly at file offset `0x1DCBD00`.

### Why this pass was run

Section 10 withdrew the index discontinuity **on two sample points** — `0x021A` and `0x040C` held,
`0x048C`/`0x048D` was explained away by the frame correction. `I-6` nevertheless stayed **OPEN** in
the register, correctly: *"no discontinuity was detected at the two places anyone looked"* is not
*"no discontinuity exists."* This pass tests the whole table.

### What a player would notice if the mapping were wrong

Every line of authored zone script — `fadeout`, `turn`, `openfullscreenmenu`, `effectplay` — is a
number. If the number-to-handler mapping slipped by one anywhere, **every verb above the slip would
run the wrong native code**: a fade would turn a character, a camera move would open a menu. The game
plainly does not do that, so the interesting question was never *"is there a slip"* but *"can this
database prove there isn't, or is it just trusting that the game works?"*

### The table, re-derived from the image

The record count is a value the accessors read, not a shape inferred from contents:

```
0x01EED700  dword  1496          <- the bound every accessor compares against
record N occupies  [0x01EED708 + 32N, +32)
   +0x00   begin (N)
   +0x08   poll  (N)
   +0x10   -- never read by any accessor --
   +0x18   result(N)             == 0x01EED700 + 32 + 32N
```

| column | non-null | in `.text` |
|---|---:|---:|
| begin | 277 | 277 |
| poll | 230 | 230 |
| **the unread slot** | **0** | 0 |
| result | 1,234 | 1,234 |

**`scriptvm-verb-table.tsv` reproduces exactly**: 1,496 family-0 rows × 3 columns re-read from the
image, **0 mismatches**. The prior extraction is confirmed independently.

### The test — 645 anchors, and a measured counterfactual

For each verb the ff12-script catalog **knows** (`cat_known`), the catalog states an argument count.
Independently, the handler's body pops a measurable number of VM operands
(`pops_int + pops_float`). **These two numbers come from opposite ends and neither is derived from
the other.** If record N did not serve verb N, the handler at N would be popping verb N±k's operands
and the two would part company.

| | |
|---|---:|
| independent anchors (catalog-known, measured pops > 0) | **645** |
| agree | **575 — 89.1 %** |
| disagree | 70 |
| span | `0x0000` – `0x05D7`, the **entire** table |
| mean gap between anchors | **2.32 records** |
| largest gap between anchors | **25 records** |

**The counterfactual is the load-bearing number.** Shift the table by one record and re-run the same
comparison:

| mapping | agreement |
|---|---:|
| `record N = verb N` | **89.1 %** |
| shifted −1 | 55.7 % |
| shifted +1 | 56.0 % |

### Where a discontinuity would show, and it does not

A slip at record K gives **high agreement below K and ~56 % above it**. Agreement per 128-record
bucket:

| bucket | anchors | agreement |
|---|---:|---:|
| `0x0000`–`0x007F` | 56 | 80.4 % |
| `0x0080`–`0x00FF` | 85 | 77.6 % |
| `0x0100`–`0x017F` | 63 | 87.3 % |
| `0x0180`–`0x01FF` | 55 | 90.9 % |
| `0x0200`–`0x027F` | 56 | 87.5 % |
| `0x0280`–`0x02FF` | 48 | 95.8 % |
| `0x0300`–`0x037F` | 41 | 90.2 % |
| `0x0380`–`0x03FF` | 51 | **100.0 %** |
| `0x0400`–`0x047F` | 51 | 84.3 % |
| `0x0480`–`0x04FF` | 49 | 95.9 % |
| `0x0500`–`0x057F` | 60 | 93.3 % |
| `0x0580`–`0x05FF` | 30 | **100.0 %** |

**No step anywhere.** The lowest buckets are the first two, which is the opposite of what a
discontinuity produces — and they are the movement / camera / fade verbs whose catalog signatures are
the least complete.

### The 70 disagreements are a catalog gap, not a mapping gap

The delta `measured − cat_args` is **+1 in 40 of 70 cases**, +2 in 12:

```
-5:1  -4:1  -3:5  -2:2  -1:7  |  +1:40  +2:12  +3:2
```

The `+1` cluster is one recognisable family — `camerasync`, `motionsync`, `fadesync`, `effectsync`,
`effectreadsync`: catalog arity **0**, measured **1**, every one of them **durative**. These are the
*"wait until the thing I started has finished"* verbs, and the operand they pop is the handle of the
thing being waited on — **implicit in the authored syntax, explicit on the VM stack.** That is a
statement about what ff12-script prints, not about which record the engine reaches.

### Verdict, with its limit stated

> **`record N = verb N` holds across all 1,496 family-0 records.** Any *persistent* shift is excluded:
> it would have to survive 645 anchors at a mean spacing of 2.32 records while agreement stayed
> 33 points above the shifted baseline in every bucket.

**The honest residual:** a *compensating pair* of shifts — one skip and one re-add — falling entirely
inside a single anchor-free window could not be seen. **The largest such window is 25 records.**
Nothing larger, and no single shift of any size, survives this test.

### Three neighbouring questions closed by the same read

**`I-4` — what the rest of the record holds.** The fourth pointer slot at `+0x10` is **zero in all
1,496 records**, and no accessor reads it. The previously reported *"1 record uses `+24`"* was the
read past the end of the table that section 13 identified — bounded by the count, it is zero.

**`I-5` — why 262 in-range verbs have a null handler.** **The premise was wrong, and the correction
is the finding.** 262 records lack a **result** callback; only **3** lack a callback of any kind, and
none of those 3 is a named catalog verb. The other **259 implement `begin` and `poll`** — they are
durative commands, and a durative command has nothing to return. *"Null handler"* was an artefact of
reading one column of a three-column table.

**`I-7` — why `0x048C` carries three handlers.** It does not. **`0x048D` `openfullscreenmenu_48d` is
the only durative command in that neighbourhood**, and all three handlers are its own:

| id | verb | shape | begin | poll | result |
|---|---|---|---|---|---|
| `0x048B` | `getmapid_48b` | instantaneous | — | — | `00347240` |
| `0x048C` | `getmapgroundtype_48c` | instantaneous | — | — | `003476B0` |
| **`0x048D`** | **`openfullscreenmenu_48d`** | **durative** | **`003462D0`** | **`00352E00`** | **`00346DA0`** |
| `0x048E` | `npc_to_gimmick` | instantaneous | — | — | `0034DA20` |

**And it is exactly what the verb means.** Opening a fullscreen menu is not instantaneous: the script
must wait while the player is inside it. `begin` opens the menu, `poll` asks each frame whether the
player is still in it, `result` delivers what they chose. Its neighbours are one-shot queries that
answer immediately and need only a `result`.

> **The document's oldest puzzle was one durative command among instantaneous ones, read through a
> frame shifted by one field.** Two years of table structure hung on that.

### An orthogonal corroboration nobody set up

The callback pattern and the catalog's `shape` classification were produced by entirely separate
means — one by reading `.data` in this image, the other by the ff12-script toolchain — and they
agree:

| pattern | catalog shape | records |
|---|---|---:|
| `--R` result only | instantaneous | 1,187 |
| `B--` / `BP-` / `BPR` has begin | durative | 270 |
| `-P-` poll only | *empty* | 26 |
| `---` nothing | *empty* | 3 |
| `-PR` | instantaneous | 1 |

**Two exceptions in 1,487 classified records.** A shifted mapping would break this agreement as
thoroughly as it breaks the arity one, and it is not built from arity at all.

**Left open:** *(answered: CE-1 is closed — a poll-only record waits for work an earlier verb started, verbs-that-only-wait-and-verbs-that-do-nothing.md; 2026-10-02, OPUS)* the **26 records with a `poll` callback and nothing else**, which the catalog calls
`empty`. A command that can only be polled, never begun and never producing a result, is not
explained. Raised as `CE-1`.

## 16. Correction 2026-09-07 — my own reading of the 70 disagreements was wrong, and the mapping result got stronger

Section 15 (written earlier the same day) explained the `+1` arity cluster like this:

> *"They pop the handle of the thing being waited on: implicit in the authored syntax, explicit on
> the VM stack."*

**That was an inference from a count, and reading the bodies killed it.**

### What the bodies say

`camerasync`, `effectsync` and `effectreadsync` share one `begin` callback, `0034C290`:

```c
VMValueStack_PushInt32(vs, 0);                    /* push a literal 0     */
iVar1 = VMValueStack_PopInt32CoerceFloat32(vs);   /* pop it straight back */
*slot = iVar1;                                    /* store 0              */
```

**The handler pushes its own operand and pops it back.** There is no handle, and nothing arrives
from the script. `fadesync` (`0033F4C0`) and `eventsync`/`eventreadsync` (`00353E20`) do the same.
The catalog was right that these verbs take **zero** arguments; **the pop-counting instrument was
wrong.**

Mechanism written up in
[`Native-Command-Lifecycle/native-command-lifecycle.md`](Native-Command-Lifecycle/native-command-lifecycle.md)
section 13.

### Neither metric measures arity, and that is the useful part

| metric | fails when |
|---|---|
| `pops_int + pops_float` | the handler **self-supplies** an operand (push-then-pop) — **over**-counts |
| `pops − pushes` | the handler **pushes a return value** — `ames` nets **−1**, `messync` **−2** — **under**-counts |

Arity is *pops not matched by a push in the same body*, and neither column is that.

### That measurement now exists — `CE-4` answered 2026-09-15 (FABLE)

**For a stack machine, "pops not matched by a push in the same body" is the MAXIMUM DEFICIT.** Walk
the handler in address order with `push = +1` and `pop = −1`; the number of operands the *caller*
must supply is `−min(prefix sum)`. A push **before** a pop supplies that pop, which is precisely the
self-supply that makes raw pops over-count; a push **after** the pops is a return value, which is
precisely what makes `net` under-count. The metric is not a third approximation — it is the
definition in the line above, computed.

The four helpers are `VMValueStack_PopNumericDiscard` (`00267DB0`) and
`VMValueStack_PopInt32CoerceFloat32` (`00267E10`) for pops, `VMValueStack_PushFloat32Bits`
(`00267F60`) and `VMValueStack_PushInt32` (`00267F90`) for pushes.

**The instrument was validated before it was believed.** Run over the `arg_handler` of every row,
its pop count reproduces this table's own published `pops_int + pops_float` for **1,904 of 1,927**
handlers (98.8 %). The 23 that differ are listed in the residue below; a counter that could not
reproduce the column it is replacing would not be worth reading.

| population | anchors | raw pops | `net` | **max deficit** |
|---|---:|---:|---:|---:|
| catalog-known, **pops > 0** | 796 | 90.5 % | 95.1 % | **96.6 %** |
| catalog-known, any stack op | 845 | 85.4 % | 89.6 % | **91.2 %** |

**The deficit beats both existing instruments on both populations**, against a catalog argument count
derived from the opposite end. **98.0 %** of the bodies are straight-line by the test below, so the
address-order walk is the execution order for all but 17 of them.

- **The residual has one dominant cause, and it is not the metric.** Of the 74 disagreements on the
  wider population, **47 are handlers that pop NOTHING AT ALL** (`ames` catalogued at 5, `aask` at 5,
  `messync` at 2, `dir`/`rmove`/`rcmove` at 1–3, each measuring 0). A body that never touches the
  value stack cannot have its arity read from the value stack: those handlers **delegate their
  popping to a callee**, and this instrument does not follow calls. Excluding them leaves **27
  disagreements in 796**, i.e. **3.4 %**.
- **Limits, stated rather than implied.** The walk is in **address order**, which equals execution
  order only for straight-line bodies; a body is counted straight-line only when no branch source or
  target lies between its first and last stack operation, which holds for 828 of 845. The instrument
  **does not follow calls**, which is the 47. And agreement with the catalog is **corroboration, not
  proof** — the metric is correct by construction, and where it and the catalog differ, either may
  be the wrong one.
- **What this settles for the rest of this document:** the sentence *"every arity figure in this
  category is an approximation"* no longer holds. The per-verb column is not regenerated here — that
  is the table's to rewrite — but the figure it should carry is the deficit, and the scratch
  instrument is `Tools/work/FABLE/drift5/ce4.py` (git-ignored).

### The mapping conclusion survives both, which is the strongest form of the result

Re-running section 15's anchor test with `net = pops − pushes`:

| metric | anchors | agreement under `record N = verb N` | agreement under a one-record shift |
|---|---:|---:|---:|
| `pops` | 645 | **89.1 %** | 56.0 % |
| **`net`** | **612** | **97.2 %** | 59.0 % |

**Two independently flawed metrics, flawed in opposite directions, both put the identity mapping
33–38 points above its own shifted baseline.** The disagreement count falls from **70 to 17**.

> **`I-6` stands, and stands more firmly than section 15 argued it.** What changes is the
> explanation of the residue: 17 rows, not 70, and not the story section 15 told about them.
> **`CE-3` is re-scoped from 30 unexplained rows to 17.**

**`CE-3` answered 2026-09-26 (FABLE, Claude Opus 5.5): 13 of the 17 are counting artefacts, and 4 genuinely depend on the actor.**
Control: [`ce3_arity_paths.py`](../_index/candidates/ce3-arity-disagreements/ce3_arity_paths.py) (5 checks, FAILS 0). It is a path-sensitive stack walk that follows calls and tail jumps, first
written by a delegated read-only pass and re-run here. Its six known-arity handlers all come out right.
- **11 of the 13 artefacts.** The catalog count is the handler's need on every path. The "missing" pop is in a
  callee the counter did not follow, such as `setrect_25`'s tail jump or the turn-at helpers, or the counter added
  two mutually exclusive arms, as in `maskopen`, `maskclose` and `sethpmenu`.
- **The other 2.** `setbattlemember` and `getbattlemember` pop inside a loop of 3 and 4 trips, which is their
  catalog count.
- **The 4 real cases: `rturnt`/`turnt` and `rturn_4f`/`turn_67` pop 3 or 4 operands, depending on the actor.** Their
  shared helper pops its middle operand only when the actor is **not** a kind-3 actor whose steering byte `+0x62`
  is `>= 0x80`. The catalog's 4 is the larger path. So a script pushes 4, and on such an actor the handler consumes
  3; no single count is right in every actor state.

### One over-generalisation, retracted

Section 15 called the `+1` cluster *"one family … every one durative."* Of the 15 family-0 verbs
with `cat_args = 0` and one measured pop, **seven are instantaneous** (`effectcancel`, `eventplay`,
`fadecancel`, `camerashakestop`, `istouchuc`, `getnowmapmusicno`, `resetemergency`). The five named
were durative; the generalisation from five to forty was not checked.

### An independent confirmation of `record N = verb N` that was sitting in the decompile header

The GFZ's own per-function evidence record carries `DISPATCH_PROVENANCE=family0[185].BEGIN` on
`0033F4C0`, and `fadesync` is call id `0x00B9` = **185**. **A third, unrelated derivation of the
same mapping**, recorded here because it was not used to reach the conclusion and therefore
corroborates it.


## SWE2-EC7-64 update (2026-09-19) - `0050D660`

`0050D660` (142 B) is the `01F26728` record-0 `+0x08` function pointer - `00267E10`/`0026D610`/`002E35A0`/`002E97B0`/`002E9A60`/`002EAE20`. Interior anchor `0050D67B` (a `002E35A0` call).


**Presentation — CLIENT (SWE2-EC7 2026-09-19, 1 edge).** `002E97B0`, a callee this page's `0050D660`
section cites, is also called by the Presentation-filed `003B70B0`. The presentation caller is a
mechanical user of the same shared helper.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **ActorEntity — CLIENT and SERVICE (8 edges).** 7 inbound (ActorEntity bodies `0037B4D0`, `0035A7A0`, `0035A8D0` call page-cited `002E97B0`, `0026D610`, `002E9A60`); 1 outbound (page-cited `VMNativeCommand_ExecuteLifecycle` (002621D0) call ActorEntity bodies `ActorManager_GetRecordByOrdinal` (00358940)). Substantive edges include `0026D610` is called by `0037B4D0`; `002E9A60` is called by `0026E060`; `002EAE20` is called by `0037B4D0`; the remaining edges run through shared helpers the page cites.
- **CoreRuntimeScheduling — SERVICE (2 edges).** 2 outbound (page-cited `003462D0`, `0034CF90` call CoreRuntimeScheduling bodies `00229EB0`, `00265880`). Substantive edges include `003462D0` calls `00229EB0`; `0034CF90` calls `00265880`.
- **Input — CLIENT (1 edge).** 1 inbound (Input bodies `InputGameplay_RebuildFrameSnapshotFromChannelHistory` (002498B0) call page-cited `003590A0`). Substantive edges include `003590A0` is called by `InputGameplay_RebuildFrameSnapshotFromChannelHistory` (002498B0).
- **Movement — CLIENT (6 edges).** 6 inbound (Movement bodies `00349680`, `003548B0`, `003488B0` call page-cited `VMValueStack_PushFloat32Bits` (00267F60), `002E97B0`). Substantive edges include `VMValueStack_PushFloat32Bits` (00267F60) is called by `00349680`; `VMValueStack_PushFloat32Bits` (00267F60) is called by `003548B0`; `VMValueStack_PushFloat32Bits` (00267F60) is called by `003488B0`; `VMValueStack_PushFloat32Bits` (00267F60) is called by `00345430`; the remaining edges run through shared helpers the page cites.
- **Party — CLIENT and SERVICE (10 edges).** 1 inbound (Party bodies `PartyFocus_ProcessActorControlPresentationState` (00358F90) call page-cited `002E97B0`); 9 outbound (page-cited `VMPartyCommand_MoveSelector00To06OutOfRuntimeRosterWhenMultiple` (00350160), `VMPartyCommand_RemoveSelector00To06_Async` (0034CDF0), `VMPartyCommand_RemoveSelector07To25` (00352AF0) call Party bodies `PartyRoster_GetActorBySlotOrCurrentFocus` (00263770), `PartyConfiguration_IsSelector07To25` (00322350), `PartyConfiguration_IsAsyncMutationPending` (003596B0)). Substantive edges include `00347240` calls `PartyRoster_GetActorBySlotOrCurrentFocus` (00263770); `003476B0` calls `PartyRoster_GetActorBySlotOrCurrentFocus` (00263770); `VMPartyCommand_RemoveSelector00To06_Async` (0034CDF0) calls `PartyConfiguration_IsAsyncMutationPending` (003596B0); `VMPartyCommand_RemoveSelector00To06_Async` (0034CDF0) calls `PartyConfiguration_RemoveSelector00To06` (00328B20); the remaining edges run through shared helpers the page cites.
- **Presentation — CLIENT and SERVICE (2 edges).** 1 inbound (Presentation bodies `003B70B0` call page-cited `002E97B0`); 1 outbound (page-cited `003B70B0` call Presentation bodies `Actor_RefreshPresentationVisibility` (002E8FD0)). Substantive edges include `003B70B0` calls `Actor_RefreshPresentationVisibility` (002E8FD0); the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — MECHANICAL (2 edges).** 2 calls from page-cited bodies into shared Save_Load_Settings plumbing (`SaveImage_GetPersistentPayloadBase` (002EF2B0)) - the helpers' general call surface, not a Save_Load_Settings relationship of this page's subjects.
- **World — CLIENT (2 edges).** 2 inbound (World bodies `00266D10` call page-cited `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910), `VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0)). Substantive edges include `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910) is called by `00266D10`; `VMNativeCommandDispatch_InitializeFamilyTables` (003DC2D0) is called by `00266D10`.
- **WorldAreaField — CLIENT and SERVICE (4 edges).** 1 inbound (WorldAreaField bodies `0025ACA0` call page-cited `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910)); 3 outbound (page-cited `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910), `003565C0` call WorldAreaField bodies `00377850`, `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910)). Substantive edges include `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910) is called by `0025ACA0`; `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910) calls `00377850`; `003565C0` calls `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910); the remaining edges run through shared helpers the page cites.

## SWE2-EC7-223 update (2026-10-03) - the `debug_isnewcharsep` id-validity predicate

`debug_isnewcharsep` is a one-instruction predicate on the verb's own argument - a sign/validity test with no module state, homed on the dispatch table that carries the verb.

| function | size | verb / caller | what the body does | interior anchors |
|---|---|---|---|---|
| `003A1640` | 13 B | `debug_isnewcharsep` `0x2070` (handler `0050CAD0` calls it and returns its value) | returns 1 when `ecx != -1` and `ecx` is non-negative - the id-validity predicate the debug verb is | Interior anchor `003A1647` |
