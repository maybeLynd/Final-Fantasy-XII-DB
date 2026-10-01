---
system: WorldActorScriptVM_InterpretBytecode — the 100-opcode interpreter that runs every zone script
category: 01-Script-VM-Native-Bridge
status: "DOCUMENTED — the SECTION-11 reopening is resolved (accepted non-author 2026-09-29, SWE2-AUDIT-SEM OV-ACCEPTANCE-0929) and a non-author falsification pass survived (2026-10-01, SWE2-CONTRACT for OPUS); every opcode read (BF-1), the inert six unused (BF-5); native access to the register file answered (RC-15: the interpreter only) and its persistence across occupants answered as narrowed on FABLE's adjudication (RC-16) (owner re-status 2026-10-01, OPUS)"
evidence_tier: 1
owner_layer: CodeDomain — none; GFZ-named, previously uncited by this database
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 5
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: swe2contract-interpreter-dispatch-falsification-pass-5
  crossref_clean: true
  reopened_count: 1
local_production_date: 2026-09-23
local_production_status: "SECTION-11 locally validated; accepted non-author 2026-09-29 (SWE2-AUDIT-SEM, OV-18)"
---

> **SECTION-11 current correction (2026-09-23):** The shared stack is image-backed at02099AC0 and
> depth resets on every invocation, including early refusal. Actor registers and request phase/scratch
> persist. There are separate stop-request and plain-advance entries; zero-length handlers do not all
> behave alike. Original wait and result callbacks now run through the interpreter and selected full
> request driver. The historical "always progresses / no resume state / unused read is harmless"
> interpretations are superseded. This page is REOPENED, preserving its older audit receipts.
> [Connected specification](the-script-from-bytecode-through-wait-and-resume.md) ·
> [Execution and limitations](../../_experiments/evidence/continuation-section11-script-resume/REVIEW.md).



# WorldActorScriptVM_InterpretBytecode

**The largest GFZ-*named* function this database had never cited** — 14,646 bytes, 3,229 instructions,
and a **100-opcode dispatch table**. It is the loop that executes FFXII's zone scripts.

*(The headline first read "the largest function in the game". **Twelve functions exceed it**. The
three largest uncited outliers are now read (2026-09-17, SWE2-FRONTIER): `006FF900` 23,568 B is the
`CPostEffect` member-resource populate — every `m_p*` texture/param object bound, each failure arm
diagnostic-labelled (`006DF480` ×119, first at
[`006FF9AC`](../../_index/ADDRESS-INDEX.md)); `006E5A20` 15,896 B remains the one unplaced giant (Pointer 2026-10-01 (SWE2-CONTRACT for OPUS): not this page's residue; the aside only measures sizes to correct the headline. `006E5A20` is called from `00731EA0` at `007321BE` and `0073228A`, and placing it belongs to the unlisted-code census in `99-Unresolved-Residual/Unlisted-Code/`, not to the interpreter);
`004D40E0` 14,891 B is the member body `004D3E20` installs on the `02AE8620` float-table object —
a `0022CC20`/`30`/`40` processor battery with `sqrtf` ×4, first call at
[`004D4238`](../../_index/ADDRESS-INDEX.md). §8 carried the qualifier; the headline had dropped it.)*

## 1. What the player sees

**Almost everything that is not combat maths.**

A guard who turns to watch you pass. A chest that opens. A cutscene that moves the camera, plays a
line, waits, and moves it again. A door that refuses until a flag is set. Every one of those is a
compiled script, and **every script instruction in the game passes through this one function.**

The database already documented **what script verbs call out to** — the
[native dispatch table](../scriptvm-native-dispatch-table.md) of `setweatherslot`,
`openfullscreenmenu` and their hundreds of siblings. **This is the other half: the machine that
decides which verb runs next, and what happens between them.**

## 2. Native mechanism

### A 100-entry computed-goto dispatch

```asm
0025E5C5  movzx edx, byte ptr [r13 + 0x201]
0025E5CD  movzx eax, r12b                    ; the opcode, one byte
0025E5D1  cmp   eax, 0x63                    ; 99
0025E5D4  ja    0x25E60A                     ; out of range
0025E5D6  lea   r8,  [rip - 0x13E5DD]        ; = 0x00120000, the image base
0025E5DD  mov   ecx, dword ptr [r8 + rax*4 + 0x141DF8]   ; 32-bit RVA table
0025E5E5  add   rcx, r8
0025E5E8  jmp   rcx
```

**Opcodes `0x00`–`0x63` — exactly 100.** The table lives at **`0x00261DF8`**, inside `.text`, and
holds **image-relative 32-bit offsets** rebased against `0x00120000`, which the `lea` reconstructs
arithmetically rather than loading.

**All 100 targets land inside this same function.** It is one monolithic interpreter, not a table of
handler functions — which is why 14,646 bytes sit under a single symbol.

### A stack machine over int32 and float32

The interpreter's own callees name its value model. **This table lists only the *named* callees — a
filter that was not stated and that drops the top row.** `FUN_008620C0` has **52 call sites**, more
than any row below; `FUN_0025D740` has 6, `FUN_00267560` and `FUN_003589E0` have 3 each. **So "the
dominant operation is pop-an-int32-coerce-to-float32" is false as a statement about the callees**,
though it remains true of the named ones — see §10 for what `FUN_008620C0` is.

| callee | calls |
|---|---:|
| `VMValueStack_PopInt32CoerceFloat32` | **48** |
| `VMValueStack_PushInt32` | **30** |
| `RuntimePointer_EncodeImageAddress` | 13 |
| `ActorManager_GetRecordByOrdinal` | 11 |
| `ActorResource_IsChannelBitActive` | 9 |
| `ImageAddress_ResolveRuntimePointer` | 6 |
| `VMValueStack_PushFloat32Bits` | 5 |
| `WorldActorScriptVM_ServiceRequestWaitState` | 4 |
| `VMValueStack_PopNumericDiscard` | 4 |
| `ActorResource_SelectPendingEntryForExecution` | 4 |
| `VMNativeCommand_ExecuteLifecycle` | 3 |
| `ActorResource_RecycleEntryRange` | 3 |

**A stack VM whose operands are actors.** The dominant operation by a wide margin is *pop an int32,
coerce to float32* — so the bytecode is integer-encoded and the arithmetic is float, which is the
usual shape for a scripting layer driving positions, timers and angles.

**`WorldActorScriptVM_ServiceRequestWaitState`** is the piece that makes cutscenes possible: a script
can yield and be resumed, rather than running to completion inside one frame.

**`VMNativeCommand_ExecuteLifecycle`** is the seam into the
[native dispatch table](../scriptvm-native-dispatch-table.md) — where a script verb stops being
bytecode and becomes engine behaviour.

## 3. Key addresses

| | |
|---|---|
| interpreter | **`0x0025E4C0`**, 14,646 B, 3,229 instructions |
| opcode jump table | **`0x00261DF8`** (`.text`), 100 × 32-bit RVA |
| rebase constant | `0x00120000`, reconstructed by `lea r8, [rip - 0x13E5DD]` |
| opcode bound | `cmp eax, 0x63` → **0x00–0x63** |
| out-of-range / default handler | `0x0025E60A` |
| dispatch site | `0x0025E5E8` (`jmp rcx`) |

Handler targets span `0x0025E5EA`–`0x00261D36`; **92 are distinct**. ~~most 17–24 bytes, with a few
large ones (222, 281, 533 B)~~ — **both halves wrong.** On the same construct (gap to next distinct
target, n=91): **17–24 B is 35 of 91 = 38 %, not most**, and **51 are larger than 24 B**. **Eight
handlers exceed 533 B** — 983, 983, 963, 963, 864, 863, 824, 759. The original read like a truncated
listing.

## 4. Data structures and formulas

### Six opcodes are indistinguishable from an invalid one

```
0025E60A is the target of the `ja` out-of-range branch
0025E60A is ALSO the table entry for opcodes 0x01, 0x02, 0x19, 0x1A, 0x31, 0x47
```

**The VM treats those six exactly as it treats an opcode it does not recognise.** They are not
rejected loudly — `0025E60A` is `mov [rsp+0xC0], ebp ; mov edi, ebp` and continues into the common
path — but they carry no behaviour of their own.

**Six of one hundred opcodes are inert in the shipped interpreter** — by their corrected names,
**`LABEL`, `TAG`, `OPUMINUS`, `OPFIXADRS`, `DRET` and `LONGCODESTART`** (§11). This is the same shape
as the **ten `NOT USED` markers** shipped in the retail battle command list
([VBF and authored tables](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)):
authored capacity the finished game does not use. Two of the six — `LABEL` and `TAG` — are
compile-time pseudo-instructions that a code generator would never emit as runtime behaviour, so
their being inert is expected rather than surprising.

Two smaller shares, and both group opcodes that plainly belong together:
`0x2A/0x2B/0x2C` → `0x0026121A` is **`PREQ` / `PREQSW` / `PREQEW`**, the three forms of one request;
`0x51/0x60` → `0x002618A8` is **`JMP` / `JMPINTERNAL`**, two jumps sharing an implementation. Under
this document's original (rotated) names those pairings were `PREQSW/PREQEW/RET` and
`POPCMPYEQJMP/REQWAITALL` — groupings with nothing in common. **Coherent sharing is itself evidence
that the corrected names are the right ones.**

**All three shared groups score the same way, and the third is the strongest.** There are exactly
**92 distinct jump-table targets for 100 opcodes**, so only three targets are shared at all. Under
the corrected names all three are clean families; under the rotated names **none** of the three is.
The six-opcode group is decisive on its own: rotated, it contained **`PUSHA` and `PUSHV`** — which
would make this a stack machine whose *push* instructions are inert. Corrected, the six are
`LABEL`, `TAG`, `OPUMINUS`, `OPFIXADRS`, `DRET`, `LONGCODESTART`, every one of them a marker or
pseudo-op that a code generator would not expect to do work at runtime. **This is a whole-table
test using engine data only** — no external name source — and §11 used two thirds of it.

### The operand pre-decode is off by one from the length bands, and exactly one opcode falls in the gap

```asm
0025E59D  movzx r12d, byte ptr [r14]        ; opcode = byte [pc]
0025E5A9  cmp   r12b, 0x47
0025E5AD  jb    0x25e5c2                    ; below 0x47 -> no operand
0025E5AF  movzx ebx, byte ptr [r14 + 2]
0025E5B4  movzx eax, byte ptr [r14 + 1]
0025E5B9  shl   bx, 8
0025E5BD  or    bx, ax                      ; operand = b[pc+2] << 8 | b[pc+1]
```

The operand is pre-decoded for every opcode **at or above `0x47`**, but the **length-3 band starts
at `0x48`**. Exactly one opcode sits in the gap: **`0x47`, whose length is 1**. The VM therefore
reads two operand bytes past the end of a one-byte instruction — once, for one opcode.

**The operand value is discarded, but the read itself remains observable.** Section11's isolated
child faults at `0025E5AF` reading PC+2 when that byte is inaccessible. Unused data do not prove
memory safety; this does not establish that ordinary authored buffers reach the guard-page case.

### The `0x0A`–`0x0F` family — the six comparison operators

Six consecutive opcodes whose handlers are **24 bytes each and open identically**. By their
corrected names they are exactly **`OPEQ`, `OPNE`, `OPGT`, `OPLS`, `OPGTE`, `OPLSE`** — the complete
set of comparison operators, with nothing else mixed in:

```asm
mov  rcx, r10
call FUN_0025D740
xor  r11d, r11d
test eax, eax
```

Six separate blocks with the same opening, dispatched separately — **one operation parameterised by
the opcode**, which remains live in `r12b` across the jump. `FUN_0025D740` pops two typed operands
from the VM return-value list (**BF-2, answered in §10**; this sentence read *"not established"*
until §12, contradicting the ticked box in §7 and §10's own answer).

## 5. Call chain

*Upstream corrected in §10's table and measured in the final section (pointer 2026-09-30, SWE2-CONTRACT): the one
caller is `WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00`, run per frame from the field runtime pass.*

```
frame -> world tick -> ActorManager_RunFieldRuntimePass -> 0025DF00 (the only call site)
   -> WorldActorScriptVM_InterpretBytecode        0025E4C0
        fetch opcode byte -> r12b
        cmp 0x63 / ja  ------------------> 0025E60A   default
        jmp [0x00261DF8 + op*4] + 0x120000
             |
             +-- 92 distinct handlers, all inside this function
                   |
                   +-> VMValueStack_Push/Pop...              the value stack
                   +-> ActorManager_GetRecordByOrdinal       the actor being scripted
                   +-> WorldActorScriptVM_ServiceRequestWaitState   yield / resume
                   +-> VMNativeCommand_ExecuteLifecycle -----> the native dispatch table
```

## 6. Modding notes

- **`0x00261DF8` is the single point of control over the whole scripting language.** Repointing one
  entry replaces one opcode's behaviour for every script in the game.
- ~~**Six opcodes are free** … the natural slots for a new instruction.~~ **WRONG, AND TWO OF THEM ARE
  TRAPS — see §10.** **`0x01 LABEL` and `0x02 TAG` have instruction length 0**: a handler installed
  there never advances the PC and spins until the frame budget expires. **They were recommended
  first.** The other four — **`0x19 OPUMINUS`, `0x1A OPFIXADRS`, `0x31 DRET`, `0x47 LONGCODESTART`** —
  are length 1 and genuinely are free.
  *(The opcode numbers are unchanged; the names attached to them were rotated by one until §11.
  The warning was right about which slots are dangerous from the moment it was written.)*
- ~~**`0x00261DF8` is the single point of control over the whole scripting language.**~~ **FALSE —
  there are two coupled tables.** Repointing a jump-table entry does not change how many bytes the
  instruction consumes; that comes from the descriptor table at `0x01EFEA60`.
- **The table is RVA-based against `0x120000`**, not absolute — entries must be written as offsets.
- **XIIOnline:** `WorldActorScriptVM_ServiceRequestWaitState` is the yield point. Any attempt to make
  scripted sequences agree across clients has to reckon with a VM that suspends and resumes rather
  than running to completion.

## 7. What is not known

- [x] **What any individual opcode does.** The dispatch, the bound, the table and the shared handlers
      are established; **no handler has been read for semantics** beyond the shape noted above.
      **BF-1.**
      *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: all 100 handlers are read, here or on the cited pages, and
      [the BF-1 opcode table](../../_index/candidates/bf1-opcode-semantics/README.md) gives each one's effect (control
      `bf1_opcodes.py`, 11 checks). Twelve opcodes have no effect beyond stack traffic, and `OPMOD` divides without a
      zero test.*
- [x] `FUN_0025D740`, called identically by opcodes `0x0A`–`0x0F`. **BF-2.**
- [x] ~~The VM state record.~~ **ANSWERED 2026-09-11 (§14):** `r13` is the **ActorManagerSlot**
      (`0x288`, `02098E10 + slot × 0x288`), the interpreter's first argument; `[r13 + 0x201]` is a
      byte of it. **BF-3.**
- [x] ~~Where the bytecode comes from and how a script is bound to an actor.~~ **ANSWERED
      2026-09-11:** the slot's bound image (`[r13]`) is the bytecode; `ActorStorage_InitializeRecord`
      plants each actor's entry, function table and bytecode base into its record, and
      `ActorResource_SelectPendingEntryForExecution` walks the channels highest-first —
      [the binding page](how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md). **BF-4.**
- [x] Whether the six inert opcodes were ever live — the retail binary cannot say. **BF-5.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): not in the shipped game. No shipped script emits any of the six.** Control:
      [`bf5_inert_opcode_census.py`](../../_index/candidates/bf5-inert-opcodes/bf5_inert_opcode_census.py) (3 checks, FAILS 0).
      - **The interpreter.** Its opcode table sends exactly `0x01 LABEL`, `0x02 TAG`, `0x19 OPUMINUS`,
        `0x1A OPFIXADRS`, `0x31 DRET` and `0x47 LONGCODESTART` to the default handler; the check reads the table.
      - **The corpus.** Every distinct `.ebp` in the full extract was scanned: 7,565 files, 198,302 scripts,
        114.9 million instructions, decoded linearly (1 byte below `0x48`, 3 at or above). Every script decodes to
        its end with no out-of-range opcode. **None of the six occurs at an opcode position.**
      - **Control.** All six byte values occur hundreds of thousands to millions of times inside `u16` operands, so
        the zero is about instruction positions, not about the bytes.
      - **So:** they were authored into the mnemonic table and never used by the shipped scripts. Whether an earlier
        tool chain emitted them is not answerable from the shipped files. Scope: the `.ebp` corpus; bytecode from
        any other source is not covered.
- [x] ~~Record `0x63`'s `+8`, and whether the descriptor table is 100 records or 99.~~
      **ANSWERED 2026-09-02** — 100 records; the mnemonic column is rotated one record relative to the
      numeric columns, so record `0x63`'s name slot would have to name a non-existent opcode `0x64`
      and holds an unrelated global instead, and `'NOP'` at `0x00D11A10` is opcode `0x00`'s name with
      no record pointing at it. Reading (i) is correct. §11. **BF-7.**
- [x] What the descriptor table's `+0x02` field means. It reproduces ff12-script's `unk4` **100/100** **ANSWERED 2026-09-02** — a displacement scan over all 38,161 bodies **with a positive control**: descriptor `+0x00` is touched at 22 sites (reproducing the document's own figure) while `+0x02` and `+0x08` are touched at **0 sites each**. The instrument answers on the field that *is* read, so the zero is a measurement, not a silence.
      under the corrected alignment. **The "no reader anywhere in `.text`" half is now tested with a
      positive control (§12): `+0x00` returns exactly 22 sites and `+0x02` returns 0**, and the
      whole table is touched by exactly one function in the binary. **BQ-6.**

## 8. Evidence

**Tier 1** — dispatch, bound, table and handler set all read out of the shipping image.

**The table was resolved arithmetically, not guessed.** `lea r8, [rip - 0x13E5DD]` at `0x0025E5D6`
(7 bytes) gives `0x0025E5DD - 0x13E5DD = 0x00120000` — the image base, matching this project's
recorded base exactly. The table address `0x00120000 + 0x141DF8 = 0x00261DF8` follows from the
instruction's own displacement, and all 100 entries decode to addresses inside the function, which is
the check that the base is right: **a wrong base would have scattered them.**

**"Six inert opcodes" is a table identity, not an inference.** Those six entries hold the same address
as the branch target of `ja`, read from the same table in the same pass.

**What is deliberately not claimed.** That any opcode is an add, a jump, a call, or anything else.
The value-model reading — a stack machine over int32/float32 operating on actors — comes from the
**names and call counts of the interpreter's own callees**, which is tier-2 authored evidence, and it
is not the same as having read a handler. **BF-1 holds the whole semantic layer open.** *(Stale since 2026-09-27: BF-1 is
ANSWERED — every handler is read and tabled in `_index/candidates/bf1-opcode-semantics/` (§7). Pointer added 2026-09-30,
SWE2-CONTRACT.)*

**Claims, evidence and tier (added 2026-09-30, SWE2-CONTRACT).**

| claim | evidence | tier |
|---|---|---|
| A 100-entry computed-goto table at `00261DF8`, RVA-based | `lea r8, [rip - 0x13E5DD]` at `0025E5D6`; all 100 entries land inside the body | 1 |
| Six opcodes share the default arm | table identity with the `ja` target | 1 |
| Every opcode's effect | BF-1: `_index/candidates/bf1-opcode-semantics/`, `bf1_opcodes.py` 11 checks | 1 |
| The six inert opcodes occur in no shipped script | BF-5: `bf5_inert_opcode_census.py` over 7,565 `.ebp`, with the operand-byte control | 1 + authored data |
| Instruction lengths come from the descriptor table `01EFEA60`; the name column is rotated one record | §11, §12 (BQ-6 with a positive control) | 1 |
| The register file is `+0x64`..`+0x83` of the actor record, reached only by opcodes `0x36`–`0x45` on census routes | §13; FZ-21 | 1 |
| The interpreter has one entry, `0025DF00`, ticked per frame | the final section: one direct call site, no stored pointer, no rip reference | 1 |
| SECTION-11's integrated execution | `continuation-section11-script-resume` re-executed non-author (146 assertions, 10 mutants) | isolated original-code execution |

**Context for why this was missing.** A census of the database against the ledger found that
**86.5 % of the executable's code bytes sit in functions no document has ever cited**, and this was
the largest GFZ-*named* function among them. The dispatch table it documents had been described from
the far side — the native commands it calls — for several passes before the interpreter itself was
opened.

## 9. Related

- [`../scriptvm-native-dispatch-table.md`](../scriptvm-native-dispatch-table.md) — the native command
  table this interpreter calls into via `VMNativeCommand_ExecuteLifecycle`.
- [`../Native-Command-Lifecycle/native-command-lifecycle.md`](../Native-Command-Lifecycle/native-command-lifecycle.md)
  — the three-callback lifecycle of a native command once dispatched.
- [`../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md)
  — the *other*, unrelated scripting system in the binary: Phyre's embedded Lua. **This VM is not
  Lua**, and the two should not be conflated.

## 10. Falsification pass 2026-09-02 — the mechanism survives; the modding advice was dangerous

A peer session attacked every claim here. **The core mechanism survived exactly**, including a check
this document had not run: **all 100 jump-table targets land on real instruction boundaries** (0
exceptions), which a wrong base or stride would break. Also confirmed: **exactly one indirect control
transfer in the whole 14.6 KB body**, so "one monolithic interpreter, one dispatch" is airtight.

**Three independent confirmations of 100:** the `cmp 0x63` bound; the table's physical extent (entry
100 is followed by eight `0xCC` and the next function's prologue); and the descriptor table below,
which is exactly **100 × 24 = 2,400 bytes**.

### The complete instruction set — a second table this document did not know existed

> **The table below was published rotated by one and was corrected on 2026-09-02.** The names shown
> are the corrected ones. The permanent trail — what was believed, what proved it wrong, and why the
> wrong reading was reachable — is in **§11**, which must be read before trusting any earlier
> transcription of this table.

**`0x01EFEA60` in `.data`, stride 24, exactly 100 records**, verified here:

```
records with a readable ASCII mnemonic : 99 / 100
distinct mnemonics / distinct pointers :  99 / 99
all mnemonic strings in .rdata         : yes
CONTROL, records 100 and 101           : <unmapped> - a float table starts there
```

| offset | field |
|---|---|
| `+0` | `s16` **instruction length in bytes of opcode *N*** |
| `+2` | `s16` unknown — reproduces ff12-script's `unk4` exactly, 100/100 (**BQ-6**) |
| `+8` | `const char*` **mnemonic of opcode *N+1*** — this column is rotated one record; see §11 |
| `+16`, `+20` | `u32` unknown — **no reader of any field but `+0` exists anywhere in `.text`** (Pointer 2026-10-01 (SWE2-CONTRACT for OPUS): no reader means no engine meaning to read; the absence is BQ-6's positive-controlled measurement, §7 and §12) |

**The two columns are indexed differently, and that is the whole of the correction in §11.** The
engine only ever reads `+0`, and it reads it with the opcode directly, at **22 sites** inside the
interpreter (`0025E5FE`, `0025E631`, `0025F5DA`, … `00261BAA`), every one of them
`movsx <r>, word ptr [base + (op*3)*8 + 0x1DDEA60]`. So the rotation costs the engine nothing, and
cost this document a hundred wrong names.

```
00 NOP              01 LABEL*           02 TAG*             03 SYSHALT
04 SYSTEM           05 OPLOR            06 OPLAND           07 OPOR
08 OPEOR            09 OPAND            0A OPEQ             0B OPNE
0C OPGT             0D OPLS             0E OPGTE            0F OPLSE
10 OPSLL            11 OPSRL            12 OPADD            13 OPSUB
14 OPMUL            15 OPDIV            16 OPMOD            17 OPNOT
18 OPBNOT           19 OPUMINUS*        1A OPFIXADRS*       1B PUSHA
1C POPA             1D PUSHX            1E PUSHY            1F POPX
20 POPY             21 REQ              22 FREQ             23 TREQ
24 REQSW            25 FREQSW           26 TREQSW           27 REQEW
28 FREQEW           29 TREQEW           2A PREQ             2B PREQSW
2C PREQEW           2D RET              2E RETN             2F RETT
30 RETTN            31 DRET*            32 REQWAIT          33 PREQWAIT
34 REQCHG           35 REQCANCEL        36 POPI0            37 POPI1
38 POPI2            39 POPI3            3A POPF0            3B POPF1
3C POPF2            3D POPF3            3E PUSHI0           3F PUSHI1
40 PUSHI2           41 PUSHI3           42 PUSHF0           43 PUSHF1
44 PUSHF2           45 PUSHF3           46 DVAR             47 LONGCODESTART*
48 PUSHV            49 POPV             4A PUSHDBG          4B PUSHP
4C PUSHTAG          4D PUSHACT          4E PUSHI            4F PUSHII
50 PUSHF            51 JMP              52 POPCMPYEQJMP     53 POPCMPYLOWJMP
54 POPCMPYLOWEQJMP  55 POPCMPYHIGHJMP   56 POPCMPYHIGHEQJMP 57 POP2CMPYBTWNJMP
58 CALL             59 CALLACT          5A POPXJMP          5B POPXCJMP
5C POPXNCJMP        5D CALLPOPA         5E CALLACTPOPA      5F REQALL
60 JMPINTERNAL      61 REQWAITALL       62 INCINITTAG       63 REQIALL
```

`*` = one of the six that dispatch to the default handler.

**Every opcode now has a name, including `0x00` and `0x63`.** Opcode `0x00` is `NOP`, whose string at
`0x00D11A10` no record points at; opcode `0x63` is `REQIALL`, with a real 187-byte handler at
`0x00261C12`. Both were loose ends in the original transcription, and both are consequences of the
rotation rather than of missing data.

**This closes the *identity* half of BF-1 — not the semantics.** The names constrain what each opcode
does; they do not decide it. Handler bodies have now been read for `0x00`, `0x48 PUSHV`, `0x49 POPV`,
`0x4B PUSHP`, `0x4C PUSHTAG`, `0x4D PUSHACT`, `0x57 POP2CMPYBTWNJMP`, `0x58 CALL`, `0x59 CALLACT`,
`0x5A POPXJMP`, `0x5B POPXCJMP`, `0x5C POPXNCJMP`, `0x5D CALLPOPA`, `0x62` and `0x63`, plus the six
24-byte stubs' opening — the four call opcodes are written out in
[the verb-dispatch document](../Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md) §2 —
and, since 2026-09-11, the sixteen register opcodes `0x36`–`0x45` (`POPI0`–`POPF3`, `PUSHI0`–`PUSHF3`),
read in full in §13. **That historical remaining-body count is not refreshed by Section11. BF-1 stays open:** the new
integrated controls cover additional selected arithmetic, control-flow and command paths, not an
exhaustive semantics census of all100 opcodes. *(Stale since 2026-09-27: BF-1 is ANSWERED, all 100 handlers read, §7.)*

### The lengths, and why §6's advice was dangerous

The default handler is **not inert**. It reloads the opcode and performs a **second opcode-indexed
lookup** for the instruction length, then advances the PC:

```asm
movzx edx, byte [rsp+0xb8]                ; the opcode
lea   rcx, [rax+rax*2]                    ; op * 3
movsx rax, word [rax + rcx*8 + 0x1DDEA60] ; -> 0x01EFEA60 + op*24, signed word
add   r14, rax                            ; advance the PC
```

**Verified length distribution:** `0` for `0x00`–`0x02` (3), `1` for `0x03`–`0x47` (69), `3` for
`0x48`–`0x63` (28).

> **`0x01 LABEL` and `0x02 TAG` have length 0.** A handler installed there advances the PC by zero,
> has no generic forward progress. The original stop-request target returns at the same PC when
> depth is empty; opcode00 instead loops until the per-invocation budget. These are distinct behaviors. **§6 recommended
> them as the first choice for a new instruction.** The other four — `OPUMINUS`, `OPFIXADRS`, `DRET`,
> `LONGCODESTART` — are length 1 and are genuinely usable.
>
> The band boundaries are untouched by §11's correction, because the length column was never rotated.
> **The danger was identified correctly the first time; only the names on the dangerous slots were
> wrong.**

### The bytecode format

**`r14` is the program counter** — loaded from `[r8]` at entry `0x0025E4E9`, stored back to `[rsi]` at
six sites; the opcode is `byte [r14]`. At `0x0025E5A9` a `cmp r12b, 0x47 / jb` pre-decodes a
little-endian `u16` from `pc+1..pc+2` for opcodes at or above `0x47`.

**The interpreter modifies the PC by an instruction length in 25 places, and 21 of them subtract.**

```
add r14, <length>   4 sites    advance to the next instruction
sub r14, <length>  21 sites    REWIND to the start of the current one
```

Each `sub` site performs the same descriptor lookup as the advance and then moves the PC *back* by
the length of the instruction just executed. **That is how the VM suspends:** a handler that must
wait rewinds the PC so that, when the frame budget refills and the interpreter re-enters, it
re-fetches and re-executes the very same instruction rather than resuming mid-way. **The request DOES preserve resume state:** PC, phase, selected ordinal, accumulator and command scratch.
The opcode is re-fetched, but a phase1 native CALL skips begin and argument pops.

That is what §6's note about `WorldActorScriptVM_ServiceRequestWaitState` being "the yield point"
means in practice, and it has a consequence for scripts: **a suspending instruction is executed more
than once**, but initialization side effects guarded by phase0 do not repeat on every retry. The original wait
command demonstrates the distinction; other opcode families require their own complete path analysis.

**That threshold is one below the immediate-carrying band** the lengths describe (`0x48`–`0x63`).

> ~~`0x47 PUSHV` is the odd one out — a default-dispatched opcode of length 1 sitting immediately
> below `0x48 POPV` of length 3. A retired immediate-carrying opcode would look exactly like this.~~
> **WITHDRAWN 2026-09-02 — the anomaly was an artefact of the rotated names.** Opcode `0x47` is
> **`LONGCODESTART`**, a length-1 marker that legitimately carries no immediate, and **`PUSHV` is
> `0x48`**, length 3 because it carries a variable id. Neither is odd. The pre-decode simply starts
> one opcode early and the value is discarded for `0x47`. §11.

That 16-bit immediate is what a verb call carries: `0x58 CALL`, `0x59 CALLACT`, `0x5D CALLPOPA` and
`0x5E CALLACTPOPA` hand it to `VMNativeCommand_ExecuteLifecycle` as the native call id — see
[the verb-dispatch document](../Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md).

### `FUN_008620C0`, the 52-call-site callee

```asm
lea rdx, "FFXII tried to call exit(), this might be a serious error!\n"
xor ecx, ecx
jmp 0x0016D6A0          ; three bytes: `ret 0`
```

**The interpreter has 52 fatal-error bailouts that do nothing in the retail build.** `0x0016D6A0` is
confirmed as the CFG check stub from the PE Load Config (directory 10 at `0x01CEBE40`, size 148;
`GuardCFCheckFunctionPointer` at **+0x70** for PE32+): `__guard_check_icall_fptr` holds `0x0016D6A0`,
`GuardCFFunctionTable` = 0, count = 0, `GuardFlags` = `0x100`.

**A reading that died to its own control, recorded because it nearly shipped:** this was almost
reported as "a retail-stubbed message emitter". A census found **273 functions tail-jump to
`0x0016D6A0` and only one carries a string**, the group being dominated by unwind funclets — so the
shared target is `/OPT:ICF` folding every `ret`-bodied function onto three bytes. **Only what the Load
Config proves is claimed.**

### BF-2 partly answered — and it is not new structure

`FUN_0025D740` reads a count at `[rcx]`, calls the exit stub if it is `< 2`, then pops two typed
operands using **the VM return-value list already documented as AO-2** in
[the native command lifecycle](../Native-Command-Lifecycle/native-command-lifecycle.md): count at
`+0`, tag byte at `+4+i`, value words at `+0x84+i*4` and `+0x184+i*4`. The interpreter touches
`+0x184` at 171 sites and `+0x84` at 69, with `cmp …,0x3F / jge` bounds throughout — the same 64-entry
structure.

**So the `0x0A`–`0x0F` family is the binary-operand pop helper.** Under the corrected names it is
shared by **`OPEQ`, `OPNE`, `OPGT`, `OPLS`, `OPGTE`, `OPLSE`** — *exactly* the comparison operators,
and nothing else.

> ~~note it **excludes `0x09 OPEQ`**, which has its own 187-byte inline handler, so *"the comparison
> operators"* is not the right generalisation.~~ **WITHDRAWN 2026-09-02.** That objection was itself
> an artefact of the rotated names: it read the group as five comparisons plus `OPSLL`, a shift, with
> `OPEQ` excluded — which is why the generalisation looked wrong. The opcode actually excluded is
> `0x09 OPAND`, a bitwise operator, which is exactly what one would expect to be excluded.
> **"The comparison operators" is the right generalisation after all.**

### What the comparator returns, and the divide beside it (FABLE, Claude Opus 5.5, 2026-09-28)

The helper is a **typed three-way comparator**, not only a pop. Read from the image for this page
([`script-vm-arith-consumers`](../../_index/candidates/script-vm-arith-consumers/README.md) C, D and I, FAILS 0). It consumes ASTRA's returns 77–80 and OPUS's
[`script-comparator-opus`](../../_index/candidates/script-comparator-opus/README.md). Static only.

- **Two ints** (depth ≥ 2 and both tags 1): a signed `cmp` of the lower operand against the top. The result is 0 when they are
  equal, −1 when the lower is less, and +1 otherwise.
- **Any other pair** takes the float path, and the int side is converted with `cvtdq2ps` under the thread's MXCSR rounding.
  - `ucomiss` / `jp` skip the equality test, so an unordered pair returns **+1**.
  - An ordered pair returns −1 only when the top is greater than the lower.
  - A mixed compare can therefore depend on the rounding mode: int 16777217 against float 16777216 gives 0 under
    round-to-nearest and +1 under round-up (OPUS's check P, a calculation).
- **The six opcodes** test `eax`: `OPEQ` `sete`, `OPNE` `setne`, `OPGT` `setg`, `OPLS` `sets`, `OPGTE` `setns`,
  `OPLSE` `setle`. With a NaN operand they give EQ 0, NE 1, GT 1, LS 0, GTE 1, LSE 0. A host's IEEE `>` and `>=` would give
  false for GT and GTE, so a reimplementation must not substitute them.
- **`OPDIV` (`0x15`), integer path** (both tags 1): the top is the divisor.
  - A zero divisor pushes int 0 (`0025E682`).
  - Otherwise `cdq` / `idiv` divides the lower by the top, truncating toward zero.
  - Nothing tests `INT_MIN / −1`, whose quotient does not fit, so `idiv` raises the CPU's divide error at `0025F0DA`.
- **`OPDIV`, float path:** the top again is the divisor. It is compared with the interpreter's zero `xmm7` by `ucomiss` /
  `jp` / `jne`.
  - Only an ordered ±0 divisor yields +0.0.
  - A NaN divisor divides.
- **`OPMOD` (`0x16`)** pops two ints and runs `cdq` / `idiv` with no test at all, then pushes the remainder. So `MOD 0` and
  `INT_MIN MOD -1` both fault at `0025F1F4`.

**Not claimed:** the game's MXCSR, what the process does after a divide error, or which scripts compare NaNs, mix operand
types or divide by −1.

### Corrections to this document's own record

| § | claim | status |
|---|---|---|
| headline | "the largest function in the game" | **false** — 12 exceed it; §8's qualified version holds |
| §2 | callee table | **filtered to named callees without saying so**; drops a 52-site row |
| §3 | "most 17–24 bytes… a few large ones (533 B)" | **38 %, not most; eight exceed 533 B** |
| §5 | "script execution request" | the interpreter has **exactly one ledger caller**: `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0x0025DF00`, Movement-owned) |
| §6 | "six opcodes are free" | **two are traps** |
| §10 | the 100-entry opcode name list | **every entry off by one** — corrected in §11 |
| §10 | "`0x47 PUSHV` … a retired immediate-carrying opcode would look exactly like this" | **withdrawn** — `0x47` is `LONGCODESTART`; the anomaly was the rotation |
| §10 | "*the comparison operators* is not the right generalisation" | **withdrawn** — with the rotation corrected, that is exactly what the `0x0A`–`0x0F` family is |
| §6 | "single point of control" | **false** — two coupled tables |
| BF-5 | "the retail binary cannot say" | **too strong** — all six carry authored mnemonics in a shipped table. Whether they were ever *live* is still open *(answered since, 2026-09-26: no shipped script emits any of the six, §7)* |

### Record `0x63` — RESOLVED, see §11

Record `0x63`'s `+8` holds `0x0000000A`, not a pointer. The mnemonic blob contains exactly one
unreferenced mnemonic-shaped string — **`'NOP'` at `0x00D11A10`** — sitting immediately before
`LABEL` in blob order. **Two functions address that dword directly**: `FUN_00333C80` reads it,
`FUN_003EDAD0` writes 9 and 10 into it. **Opcode `0x63` is live** — a real 187-byte handler at
`0x00261C12`.

Two readings were held open: (i) 100 records, the last one's name slot doubling as an unrelated
global; (ii) 99 records plus a different object at `0x01EFF3A8` read out of bounds.

**Reading (i) is correct, and §11 explains why the name slot is free to be reused.** The mnemonic
column is rotated one record: record *N* names opcode *N+1*, so record `0x63` would have to name a
non-existent opcode `0x64` and there is no name for it to hold. `'NOP'` is unreferenced for the
mirror-image reason — it is opcode `0x00`'s name, and no record sits one place *before* record `0x00`
to point at it. The blob is contiguous and complete (`… REQIALL, NOP, LABEL, TAG, SYSHALT, …`); only
the pointer column is offset. **BF-7 answered** without needing to read `FUN_00333C80` or
`FUN_003EDAD0` at all, which was the separating observation this document proposed and no longer
needs.

## 11. Falsification pass 2026-09-02 (third) — the opcode name table was off by one, for all 100 entries

This section is the permanent record of the largest single correction this document has taken. It was
found by a peer session reading the four *native call* opcodes for
[the verb-dispatch document](../Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md), not
by an audit of this document, and it invalidated every row of §10's name table at once.

### What was believed

That the descriptor table at `0x01EFEA60` is 100 records of 24 bytes, that record *N* describes
opcode *N* in **all** its fields, and therefore that the `const char*` at record *N* `+8` is
opcode *N*'s mnemonic. §10 published a 100-entry name list built on that pairing.

### What is now believed

The table is 100 records of 24 bytes — that part is right — but **its columns are indexed
differently**:

- record *N*'s **numeric** fields (`+0` length, `+2` unknown) describe **opcode *N***;
- record *N*'s **mnemonic pointer** (`+8`) names **opcode *N+1***.

So the name of opcode *N* is stored in record *N−1*, and opcode `0x00`'s name (`NOP`, at
`0x00D11A10`) has no record pointing at it, while record `0x63`'s name slot has no opcode to name and
holds an unrelated global.

### What proved it

**Mechanical.** Compared field by field against ff12-script's `instrArr`, which has 101 entries with
index 0 = `NOP` and index 100 = `INVALID_OPCODE` — i.e. an array indexed by opcode `0x00`–`0x63` with
a sentinel for the out-of-range case the `cmp 0x63 / ja` branch handles:

| alignment | mnemonic matches | `+0` length matches | `+2` field matches |
|---|---:|---:|---:|
| record *i* ↔ ff12 index *i* | **0 / 100** | **100 / 100** | **100 / 100** |
| record *i* ↔ ff12 index *i+1* | 96 / 100 | 97 / 100 | 83 / 100 |

A perfect score on both numeric columns with a **zero** on the name column is only possible if the
columns disagree with each other. And the numeric alignment is the one **the engine itself uses**:
`descriptor + opcode*24 + 0`, with the opcode unmodified, at **22 sites** in the interpreter — the
default handler at `0025E5FE` and 21 more. The engine never reads the `+8` column at all, which is
why a rotation there can ship without breaking anything.

**Behavioural — eight independent confirmations**, each from a complete handler body reached through
the jump table at `0x00261DF8`, not from any table of names:

| opcode | what its handler actually does | corrected name | old name |
|---|---|---|---|
| `0x48` | calls `00267FC0`, which reads a script variable by declared type and **pushes** it | `PUSHV` | `POPV` |
| `0x49` | calls `00267E60`, which **pops** and stores into a script variable | `POPV` | `PUSHDBG` |
| `0x57` | pops two values, orders them, tests whether a third lies between them, branches | `POP2CMPYBTWNJMP` | `CALL` |
| `0x58` | stores the **current** actor id and calls the native command dispatcher | `CALL` | `CALLACT` |
| `0x59` | **pops** an actor id, then calls the native command dispatcher | `CALLACT` | `POPXJMP` |
| `0x5D` | calls the dispatcher with the **current** actor, then pops the returned value into the A register at `cmdState[0x10]` | `CALLPOPA` | `CALLACTPOPA` |
| `0x5E` | **pops** an actor id, then joins `0x5D`'s path at `00261ABF` | `CALLACTPOPA` | `REQALL` |
| `0x0A`–`0x0F` | six 24-byte stubs sharing one binary-operand pop helper | the six comparison operators | five comparisons + a shift, excluding `OPEQ` |

The first row alone settles it: a function that unambiguously pushes cannot be `POPV`.

**The `CALLPOPA` row is the tightest of them**, because the mnemonic decomposes into two operations
that both appear in the handler in order. Opcode `0x1B PUSHA` pushes `[rsi + 0x10]` and opcode
`0x1C POPA` pops into it, so **`rsi + 0x10` is the script's A register**. Opcode `0x5D` calls the
dispatcher and then pops the returned value into exactly that slot — literally *call, then POPA*.
Under the old names `0x5D` was `CALLACTPOPA`, which would have to pop an actor id first, and it does
not.

**Coherence — three groupings that were incoherent and are now obvious.** The two shared jump-table
targets group `PREQ/PREQSW/PREQEW` and `JMP/JMPINTERNAL` under the corrected names, where before they
grouped `PREQSW/PREQEW/RET` and `POPCMPYEQJMP/REQWAITALL`. The `0x0A`–`0x0F` family becomes exactly
the comparison operators, an objection §10 had raised against its own reading. **This document was
already recording symptoms of the rotation and treating each one as a separate curiosity.**

### Why the earlier reading was reachable — and this is the part worth keeping

**The mnemonic blob is laid out in table order, so it looks like it validates the pairing.** Walk the
`+8` pointers and the strings come out in a clean, sensible sequence — `… REQIALL, LABEL, TAG,
SYSHALT, SYSTEM, OPLOR …` — ascending through `.rdata` with no gaps. Every internal check one would
naturally run on a name column passes: the strings are contiguous, distinct, all in `.rdata`, all
mnemonic-shaped, one per record. **Nothing inside the name column can reveal a rotation of the whole
column.**

The rotation is only visible by leaving the column: comparing the names against the *lengths* in the
same records, or against a handler body, or against an external array. The original pass compared the
name column against **itself** — its ordering, its density, its string section — and it was
self-consistent, because it was.

Two symptoms were noticed at the time and both were filed as anomalies rather than treated as a test:
the unreferenced `'NOP'` string and record `0x63`'s non-pointer. **Both are exact predictions of a
one-record rotation** — one dangling string at each end of the column — and together they were the
observation that would have settled it, sitting in the document as BF-7 for a whole pass.

**The general lesson, which is the same one this database has now recorded three times today:** an
internally consistent reading is not a checked reading. A column that agrees with itself proves only
that it was written by one process. The check has to come from outside the artefact — a second
column, a body, an independent source — and when a document is already carrying two unexplained
loose ends, those are usually not decorations. They are the test.

### Not changed

The dispatch mechanism, the `cmp 0x63` bound, the 100 jump-table entries and their RVA rebasing, the
92 distinct handler targets, the six default-dispatched opcode **numbers**, the three length bands,
the two coupled tables, the `FUN_008620C0` reading and the §6 trap warning all survive untouched.
**Only the names moved.** The correction changes what to call the opcodes, and it does not change one
statement this document makes about what the interpreter does.

---

## 12. Falsification pass 2026-09-02 (fourth) — the first attack on this document's own claims

Passes in §10 and §11 were driven by *other* work colliding with this document. This is the first
pass whose goal was to destroy what it says. **Nothing was overturned.** One stale sentence, three
mechanisms it did not have, and one near-miss of my own.

**Program state:** parent `2ed8affb...`, snapshot `46f02e26...`, embedded EXE `73461d08...`, ledger
38,161 / 38,003 / 158, verified before any reading.
**Instruments:** the descriptor table and the jump table **read directly out of the PE image** by VA
to file-offset — no decompiler, no recovered index, and **no external name source**; capstone over
the interpreter's complete 14,646-byte body; and a displacement scan for the descriptor table across
all 38,161 function bodies with clamped extents.

**Deliberately excluded: ff12-script.** §11's correction rests on it, so re-using it would test
nothing. Everything below is engine data.

### Killer observations named, and hunted

| Claim | What would kill it | Result |
|---|---|---|
| 100 records of 24 bytes at `0x01EFEA60` | a 101st mnemonic-shaped record | **SURVIVED.** Records 100+ decode as `3F800000` floats. |
| lengths `0`/`1`/`3` in bands of 3 / 69 / 28 | any record outside its band | **SURVIVED exactly**, re-derived from the bytes. |
| record `0x63`'s name slot is not a pointer | it being a valid string | **SURVIVED.** It holds `0x0A`. |
| `NOP` at `0x00D11A10` is orphaned | a record pointing at it | **SURVIVED.** It sits immediately before record 0's `LABEL` at `0x00D11A14`, referenced by nothing. |
| the mnemonic column is rotated by one | the name column being engine-readable at the unrotated index | **SURVIVED, independently re-derived** — see below. |
| 92 distinct jump-table targets | a different count | **SURVIVED exactly.** |
| the six inert opcodes are `01,02,19,1A,31,47` | a different membership | **SURVIVED exactly.** |
| `0x0A`-`0x0F` are the six comparison operators | any of the six naming something else | **SURVIVED.** Records `0x09`-`0x0E` are `OPEQ OPNE OPGT OPLS OPGTE OPLSE`. |
| §10's default-handler assembly | the quoted instructions not being there, in that order | **SURVIVED** — and I nearly reported otherwise. See *the near-miss*. |
| **BQ-6: "no reader of `+0x02` exists anywhere in `.text`"** | one reader | **SURVIVED a positive-controlled test.** |

### The rotation, re-derived from engine data alone

§11 proved the rotation with ff12-script and eight handler bodies. Two independent confirmations,
neither of which needs an external source:

**The arithmetic closes, and only under the rotation.** Records `0x00`-`0x62` carry mnemonic-shaped
strings; record `0x63` does not. Under the rotation those 99 strings name opcodes `0x01`-`0x63`, and
`NOP` names opcode `0x00` — **exactly 100 names for exactly 100 opcodes, with nothing left over.**
Under the unrotated reading there are 99 names for 100 opcodes *and* an orphaned `NOP`: one opcode
unnamed and one string unexplained. **The rotation is the only alignment with no remainder.**

**The name column has no readers at all.** A displacement scan across all 38,161 function bodies
finds the descriptor table touched by **exactly one function** — the interpreter — at **22 sites**,
**all of them `+0x00`**. Not one instruction anywhere in the binary reads `+0x08`. §11 asserted this
(*"the engine never reads the `+8` column at all, which is why a rotation there can ship without
breaking anything"*); it is now measured. **A column no code reads is a column nothing can keep
honest**, which is the mechanism by which a build can ship a rotated name table indefinitely.

### BQ-6, tested with a positive control

The claim is an absence, and the evidence standard requires absences to carry a control:

```
descriptor + 0x00  (length)    22 sites    <- POSITIVE CONTROL: matches the document's own figure
descriptor + 0x02  (unknown)    0 sites    <- the absence claim
descriptor + 0x08  (mnemonic)   0 sites
functions touching the table at all : 1    (WorldActorScriptVM_InterpretBytecode)
```

The instrument returns the expected 22 on the field that is read, so its zero on `+0x02` is a
measurement rather than a silence. **The absence holds.**

### Three mechanisms this document did not have

**1. Suspension is implemented by rewinding the PC.** The interpreter modifies `r14` by an
instruction length at 25 sites: **4 advance, 21 rewind**. A handler that must wait subtracts the
length of the instruction it just executed, so the interpreter re-fetches and **re-executes the same
instruction** on re-entry. **Corrected by Section11:** PC, phase, target ordinal, accumulator and
scratch ARE retained continuation state. Re-fetching a native CALL does not rerun its begin callback
or pop its original arguments when phase is already1. Different opcode waits require their own
state contracts. The old universal repeated-side-effect inference is withdrawn.

**2. The operand pre-decode is off by one from the length bands.** Operands are decoded for opcodes
at or above `0x47`; the length-3 band begins at `0x48`. **Exactly one opcode — `0x47`, length 1 —
falls in the gap**, and the VM reads two bytes past it. Section11 demonstrates an isolated
inaccessible-byte fault even though the operand value is unused. This changes the stated safety
argument, not the observed length bands, and does not establish a retail fault.

**3. The third shared-handler group is the strongest evidence for the corrected names, and §11 did
not use it.** §11 cited two of the three shared jump-table targets as coherence. The third — the six
inert opcodes — is decisive: under the rotated names that group contained **`PUSHA` and `PUSHV`**,
making this a stack machine whose *push* instructions do nothing. Under the corrected names it is
six markers and pseudo-ops. **All three groups are incoherent rotated and clean corrected: 0/3
against 3/3**, from engine data only. Added to §4.

### The one defect

**§4 and §7 contradicted each other about BF-2.** §7 ticked it answered and §10 answered it — *the
`0x0A`-`0x0F` helper pops two typed operands from the VM return-value list* — while §4 still read
**"What `FUN_0025D740` does is not established. BF-2."** A stale sentence left behind when the
answer landed in a later section. Corrected in place.

That is the same shape as the `12 of 12` / `13 reads` contradiction found in
[`character-render-object.md`](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md)
earlier today: **a document disagreeing with itself, in two places a reader would not compare.**
Append-only correction sections make this the characteristic defect of a heavily-revised document —
the correction is written where it was discovered, and the original statement stays where it was.

### The near-miss, recorded because it is the third this session

I disassembled from `0x0025E5E0`, found

```asm
0025E5FE  movsx rax, word ptr [r8 + rcx*8 + 0x1ddea60]
0025E607  sub   r14, rax
```

and compared it with §10's block, which quotes the same lookup followed by **`add r14, rax`**. That
looked like the document inverting the direction of the program counter — which would have made
§6's "the other four are length 1 and genuinely are free" advice wrong, since a length-1 handler
would walk *backwards*.

**The document was right and I was reading a different site.** There are 22 descriptor lookups; the
one at `0x25E5FE` is a rewind in a suspend path, and §10 quotes the one at `0x25E631`, which is
followed by `add r14, rax` at `0x25E641` exactly as written. The block is a correct, correctly
ordered quotation.

> **Three near-overturns in one session, all the same shape**: `+0x10D9` from an untracked register,
> 37 phantom callees from counting `JMP imm`, and now an `add`/`sub` inversion from reading one of
> 22 identical sites. Every one was an **attribution** error in an instrument, not a decoding error,
> and every one would have produced a confident, wrong correction to a document that was right.
> **When a document quotes assembly, identify *which* site it quotes before concluding it is wrong** —
> in a 14,646-byte function with 22 copies of one idiom, "the binary says otherwise" is a claim about
> which copy you happened to read.

### Status

**Zero claims overturned.** One stale cross-section contradiction corrected, three mechanisms added,
BQ-6's absence upgraded to a positive-controlled measurement, and §11's rotation independently
re-derived from engine data with no external source. This document has now survived a pass whose
purpose was to break it.

## 13. The register file — opcodes `0x36`–`0x45` keep eight per-actor slots in the ActorStorageRecord (2026-09-11, FABLE-FZ21)

FZ-21 asked what the eight 4-byte slots at ActorStorageRecord `+0x64`–`+0x83` are, after the
generation-3 census found them written and read by this interpreter and by nothing else. They are the
VM's **register file**: four `int32` registers **I0–I3** at `+0x64`, `+0x68`, `+0x6C`, `+0x70` and four
`float32` registers **F0–F3** at `+0x74`, `+0x78`, `+0x7C`, `+0x80`, and they live in the *actor's*
record rather than in the VM context.

### 13.1 The sixteen handlers, from the jump table

The dispatch at `0025E5D6`–`0025E5E8` is `lea r8, [rip-0x13e5dd]` (the image base, `0x00120000`),
`mov ecx, [r8 + rax*4 + 0x141DF8]`, `add rcx, r8`, `jmp rcx` — so every entry of the 100-entry table
at `0x00261DF8` is an image-relative offset. Decoding all hundred and looking up the mnemonic table
(§10, corrected alignment):

| opcode | mnemonic | handler | body |
|---|---|---|---|
| `0x36`–`0x39` | `POPI0`–`POPI3` | `0026161C`, `0026162D`, `0026163E`, `0026164F` | `mov rcx, r10` · `call VMValueStack_PopInt32CoerceFloat32 (00267E10)` · `mov [r15 + 0x64 + 4n], eax` · back to the loop |
| `0x3A`–`0x3D` | `POPF0`–`POPF3` | `00261660`, `00261673`, `00261686`, `00261699` | `mov rcx, r10` · `call 00267DB0` (returns the popped value in `xmm0`, an int entry converted with `cvtdq2ps`) · `movss [r15 + 0x74 + 4n], xmm0` |
| `0x3E`–`0x41` | `PUSHI0`–`PUSHI3` | `002616AF`, `002616C0`, `002616D1`, `002616E2` | `mov edx, [r15 + 0x64 + 4n]` · `mov rcx, r10` · `call VMValueStack_PushInt32 (00267F90)` |
| `0x42`–`0x45` | `PUSHF0`–`PUSHF3` | `002616F3`, `00261706`, `00261719`, `0026172C` | `movss xmm1, [r15 + 0x74 + 4n]` · `mov rcx, r10` · `call VMValueStack_PushFloat32Bits (00267F60)` |

Every body is four instructions; none has a side effect beyond the slot and the value stack. `r15` is
the interpreter's **second argument**, written once at entry (`0025E4D5 mov r15, rdx`) and never
again in the 14 KB body (its only other writes are the two epilogue pops), and the census route that
reaches this function passes the actor record there
(`WorldActor_UpdateRuntimeAndScriptExecutionState` `0025DF00` at `0025E0D3`). `r10` is the value
stack, a single global at `0x02099AC0` (`lea r10, [rip+0x1e3b461]` at `0025E658`): count at `+0`,
tag byte at `+4+i` (1 = int, 2 = float), value at `+0x184+i*4`, 64 entries. The pop helpers coerce
across the tag — `00267E10` truncates a float entry with `cvttss2si`, `00267DB0` widens an int entry
with `cvtdq2ps` — and both call `FUN_008620C0` and return zero on an empty stack; the push helpers
refuse at 63. (`00267DB0` is named `VMValueStack_PopNumericDiscard` in the function list; the
`POPF` handlers store what it returns in `xmm0`. ~~So "discard" describes its *other* call sites,
not this one.~~ **REFUTED 2026-09-14 (OPUS): there are no such call sites.** Every direct `E8`
call to `00267DB0` in `.text` was found and the instructions after it decoded until `xmm0` is read
or written — **436 sites, 385 read it before writing it, ZERO overwrite it first**, and the 51
remaining leave the window on a `jmp`, `call` or `ret` before either. Those 51 are undetermined in
the interesting direction (Pointer 2026-10-01 (SWE2-CONTRACT for OPUS): a limit on the helper's name, not an open question about the interpreter; the popped value is used by the POPF handlers, §13.1, which is all this page relies on): `xmm0` is the first floating-point ARGUMENT register, so a `call` right
after may be passing the popped value on. **The hedge rescued the name by asserting a population,
and the population is empty.**)

### 13.2 What is established, and how

- **Identity and width.** From the jump table and the mnemonic table alone, with the handler bodies
  read: `int32` for I0–I3 (plain `mov`), `float32` for F0–F3 (`movss`). Tier 1.
- **Where they live.** In the actor record, not the context: the context is `r13` (the first
  argument, reloaded from its home slot `[rsp+0xB0]` at every loop head), and the eight slots are
  reached through `r15` only. This is what the generation-3 census corrected — the earlier `+0x68` /
  `+0x70` / `+0x78` / `+0x80` rows were `r13` reads of the context's constant pools (`PUSHI`, `PUSHF`,
  `PUSHTAG` at `00261855`, `0026187D`, `002617C9`), misfiled while `r13` was believed to be the record.
- **Who else touches them.** In the generation-3 census (275 functions reached from the two record
  accessors and the constructor seed, control found) **no function but this one** accesses
  `+0x64`–`+0x83`. `ActorStorage_InitializeRecord` (`00266530`), `00266AD0` and `00266BD0` — the
  initialisers the census does not seed, read directly — store nothing in the range; the pool is
  zeroed once at allocation (`002679F0` → `00861EC0(pool, 0, size)` at `00267A8B`). So on record
  *reuse* the register file is not cleared by anything found (limit: a writer reaching the record by
  a route the census does not follow would be invisible; an image-wide displacement sweep of
  `+0x64`–`+0x83` writes returns hundreds of unrelated structures and cannot attribute).
- **What the shipped scripts do with them.** All 1,115 `us` `.ebp` scripts were decompiled with
  `ff12-script` 3.0 (1,114 succeeded; `evt_t0020` is not an `EBP2` container) and the sixteen
  mnemonics counted per function — the per-script table is
  [`register-opcodes-by-script.tsv`](register-opcodes-by-script.tsv). **57,568 register opcodes in
  4,430 of 108,328 functions across 788 scripts**: `POPI0` 12,334 · `POPI1` 6,716 · `POPI2` 3,742 ·
  `POPI3` 3,197 · `PUSHI0` 20,935 · `PUSHI1` 4,695 · `PUSHI2` 1,652 · `PUSHI3` 2,983 · `POPF0` 408 ·
  `POPF1` 159 · `POPF2` 3 · `POPF3` 3 · `PUSHF0` 576 · `PUSHF1` 159 · `PUSHF2` 3 · `PUSHF3` 3. The
  compiler uses I0–I3 as function locals (loop counters and temporaries: `POPI0 … PUSHI0 PUSHII 0xa
  OPLSE POPXNCJMP` is the `for` idiom) — that is the bulk. Control: the same run counts 6,746
  `btlAtelSetHpLowLimit` call lines in 502 scripts against the byte walk's 6,756 sites in 505 on
  [the battle-unit page](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) §10 (the
  ten missing are the `CALL` / `CALLACTPOPA` forms the decompiler prints numerically, plus the one
  undecoded script).
- **The scripts rely on the slots surviving between functions — which is why they are in the record.**
  172 functions in 84 scripts read a register before writing it: `saveactor.save()` and
  `saveactor.load()` in 81 area scripts open with `PUSHI1 / POPXNCJMP` on an I1 that the same actor's
  `save_load()` wrote; `NPC01.元の角度へ` restores an F0 that `PC向く` saved (`rbn_a16`);
  `CHILDSET01.一時停止解除` restores F0–F3 that `一時避難` saved (`slm_a02`); and in `rbn_a03` the
  *entry-character takeover* functions of `TWN_BANGA_A`, `TWN_CEEK_A` and `SND_WOMAN_A` write and read
  F0–F3 across actors — consistent with those functions running on the entry character's record
  rather than the script actor's, which is the record `r15` names. One case has no writer anywhere in
  its file (`SND_WOMAN_A`'s release function): ~~that is the register file behaving as actor state, not
  a decoder gap.~~ it is not a decoder gap (the bytecode census agrees: F0–F3 are read and never written in
  `rbn_a03.ebp@286AE`, all nine language copies), but the function is not shown to run, so it is not evidence
  that the file carries state into it. *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS), on FABLE's RC-16 adjudication and
  [`auditsem-review-rc151617-0930`](../../_index/candidates/auditsem-review-rc151617-0930/REVIEW.md) §2.*

### 13.3 What is not known

- [x] **RC-15.** Whether any *native* path reads or writes the eight registers by a route the census does not see.
  Registered 2026-09-30 (SWE2-CONTRACT); static (FZ-21's residue: no native access on any census route).
  *Applied 2026-09-30 (records) RC-15:* **ANSWERED 2026-09-30 by FABLE (`rc151617-fable-0930`, `0870d8b62`): only the interpreter reads or writes the register file**; the only native clear is the pool memset `00267A8B`. ORACLE's record `rc15-regfile-skipmask-0930` (commit `1e4537034`) **corroborates** it beyond FABLE's two-hop reach.
- [x] **RC-16.** Whether the register file persists across a record's occupants: whether a new logical actor in a
  reused record can read a register before its own first write. The initialisers do not clear the range (FZ-21), and
  the correction below explains why a live watch on an address cannot decide it. Registered 2026-09-30
  (SWE2-CONTRACT); static first: a first-read-before-write census over the shipped scripts' register opcodes.
  *Applied 2026-09-30 (records) RC-16:* **ANSWERED 2026-09-30 by FABLE (`rc151617-fable-0930`, `0870d8b62`): the file persists across occupants, and shipped scripts read a register before their own first write** ~~(67 actors touch `regI1` first with a read)~~. **ORACLE (`rc15-regfile-skipmask-0930`, commit `1e4537034`) agrees on persistence and read-before-write but disagrees in part and would record NARROWED:** the reads sit in `fn_spawn` / `fn_respawn` functions (516 times in 12 scripts), not `init()`; within one pool a record is initialised once for one authored actor, so the "previous occupant" is the same actor's earlier spawn; the residue is which record a spawn entry's function runs on. ~~**FABLE adjudication pending** (`OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930`).~~
  *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS), on FABLE's adjudication of `OPUS-NOTICE-FABLE-RC12-RC16-RC17-0930` ([`auditsem-corrections-fable-0930/consumer-check.md`](../../_index/candidates/auditsem-corrections-fable-0930/consumer-check.md), commit `a8aed6ca9`) and SWE2-AUDIT-SEM's review ([`auditsem-review-rc151617-0930`](../../_index/candidates/auditsem-review-rc151617-0930/REVIEW.md) §2, §5 N1); the struck count is produced by no committed output.* **FABLE accepts ORACLE's NARROWED.** The register file persists for the life of a pool; the only native clear is the pool memset `00267A8B` when a manager builds its runtime. `rc16_regfile_reads.py` finds 434 bytecode scripts whose first linear `regI1` touch is a read; in the decompiled US corpus the dominant case is the monster spawn-group functions, `fn_spawn spawnNN()` and `fn_respawn respawnNN()` (516 instances in 12 scripts), which on a fresh spawn (`btlAtelGetRespawnCause() == -1`) test `regI1` before writing it. The `SND_WOMAN_A` F0..F3 read is not shown to run. RC-16's stated limit: which record a spawn entry's function runs on (static, not traced).
- Whether any *native* path reads or writes the eight (none on any census route; the sweep cannot
  attribute) and whether the file persists across a record's occupants in play — ~~a live observation
  (a hardware breakpoint on a reused record's `+0x64` after a spawn) would settle both~~; queued, not
  requested, while live automation is paused. (Pointer 2026-10-01 (SWE2-CONTRACT for OPUS): both halves are answered statically, RC-15 and RC-16 above; no live observation is needed for either.)

  > **The observation above would not have settled it, and its premise is gone — corrected
  > 2026-09-21 (FABLE, on `ASTRA-CONTRA-FABLE-ACTOR-POOL-PROCESS-LIFETIME`).**
  >
  > **The premise first.** That design assumes a record address which looks unchanged across a spawn
  > is the same allocation. **It is not sound, because the pool is released.** In the manager unload
  > `002628B0`: `00262D96` loads the pool from `[manager+0x08]`, null-guards it, `00262D9F` calls
  > `003697F0` — thirteen bytes, `test rcx,rcx / je ret / xor edx,edx / jmp 00369860`, the engine's
  > own allocator release rather than the CRT free — and `00262DA4` writes `rbp` back to that same
  > `[manager+0x08]`, `rbp` having been zeroed at `0026292A` and not rewritten in between. *(Read from
  > the image here; the actor-record page carries the same finding from
  > `ASTRA-RETURN-OPUS-ACTOR-POOL-RELEASE-BOUNDARY`.)* **An equal numerical address can therefore be a
  > reused allocation, not a surviving one**, and "a reused record" cannot be identified by address at
  > all.
  >
  > **Three readings have to be told apart, and only the second is the question this section asks:**
  > the same allocation still holding the same logical script actor whose battle unit was rebound
  > — *retained state, not inheritance*; a **different** logical actor occupying a record in the same
  > allocation with the old values surviving until its first read — *the actual hypothesis*; and the
  > manager having released and rebuilt the pool in between. A generic "monster respawn" trigger does
  > not distinguish them.
  >
  > **And four bytes at `+0x64` are one of eight registers.** All-zero before and after is
  > non-discriminating unless a **nonzero write by the old actor is separately observed first**, so a
  > discriminating run needs: the transition named in advance as same-actor rebinding *or*
  > different-actor in-pool reuse; a positive register write in the old actor; **all eight** raw
  > 4-byte registers; continuity evidence sufficient to exclude a release and rebuild between the two
  > observations — *equal endpoint pool and record pointers cannot do that*; the new occupant
  > identified separately; and the chosen register's **first read, before any overwrite**, correlated
  > to the interpreter's actual record argument rather than to the monster on screen. Without
  > continuity, the honest report is endpoints only, with reuse unresolved.
- Whether the register file is part of any save image. No save-page mapping names the actor record;
  nothing here claims either way. *Answered 2026-09-30 (SWE2-CONTRACT, cited): not directly.* The register file is
  bytes of the actor storage record, and the records live in one block allocated per manager slot and released on
  unload (`_types/types.tsv` `ActorStorageRecord`; the pool release in the correction above), not in the save-image
  buffer. Values a script wants to keep reach a save only through script verbs (`saveactor.save` / `load`, FZ-21).
  Tier 1.

## 14. The context register is the ActorManagerSlot, and the immediate tables are the image's rebased sections (2026-09-11, FABLE-BF3)

BF-3 asked what `r13` points at. It is the interpreter's **first argument**, `mov r13, rcx` at
`0025E4DF`, reloaded from that argument's home slot `[rsp+0xB0]` at every loop head (`0025E61B`) —
and the caller passes the **ActorManagerSlot**: `ActorManager_RunFieldRuntimePass` (`0025D9E0`)
computes `rbx = 02098E10 + index × 0x288` (`0025D9EF`–`0025D9FD`) and hands it to
`WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`), which keeps it in `r15` and passes it
on at `0025E0D0`–`0025E0D3` with the actor record in `rdx` and the actor's request entry in `r8`. So
the three arguments are (slot, record, entry): `[r13]` is the bound script image, `r15` the actor
(§13), and `[r8]` the program counter `r14`.

**The 28 accesses.** A census seeded on that argument (`hop_scan.py --argseed 0025E4C0:0`, with the
generation-3 scanner's frame-relative spill tracking so the home-slot reload re-establishes `r13`;
control `0025E4C0:0x201` found) reaches six functions; the rows are appended to
[the manager census](../../04-Actor-Entity/Actor-Manager-Record/actor-manager-record-accesses.tsv)
with the route `argseed 0025E4C0:0`:

| slot offset | store name | read by | what for |
|---|---|---|---|
| `+0x000` | `theBoundDefinitionPayload` | `PUSHTAG` (`002617E5`), `JMPINTERNAL`/`REQ*` tails (`00261B27`, `00261C24`, `00261CCD`), `00268B10`, the resolver (`002624B0`, `00262546`) | the image base every table offset is added to |
| `+0x028` | `slotIndex` | `DVAR` (`0026174A`), `POPV` (`00267F1E`), `00268850` (`002689D5` +1) | which manager this script belongs to |
| `+0x040` / `+0x048` / `+0x058` / `+0x060` / `+0x098` | the variable homes | the resolver `00262440` | [the storage classes](script-variables-and-their-storage-classes.md) |
| `+0x068` | `payloadSectionC` (header `+0x20`, "4-byte records") | `PUSHI` (`00261855`) | **the int constant pool** — `[pool + operand*4 + 4]` |
| `+0x070` | `payloadSectionD` (header `+0x24`, "float32 data") | `PUSHF` (`0026187D`) | **the float constant pool** |
| `+0x078` | `payloadSectionE` (header `+0x28`, "8-byte records") | the resolver (`00262459`) | **the variable descriptor table** |
| `+0x080` | `payloadSectionF` (header `+0x2C`) | `PUSHTAG` (`002617C9`, `00261806`) | **the tag table** — count at `+0`, then 8-byte entries; `PUSHTAG` pushes the entry's word `+0xE` shifted into the operand with bit 14 set (`00261826`–`00261834`) |
| `+0x008` | — | `ActorManager_GetRecordByOrdinal` (`00358940`) | the record table the ordinal indexes |
| `+0x201` | — | the dispatch head (`0025E5C5`) | a byte fed into every handler in `edx` |

Two consequences. The immediate-push opcodes never touch the actor: `PUSHI`, `PUSHF`, `PUSHTAG`
read the slot's rebased sections, which is what the generation-2 census misfiled as actor-record
reads before FZ-16 (the actor page's CORRECTED box). And the binder is the only place the section
pointers are set (`0026CB3C`–`0026CB6B`), so a script image is bound to a manager slot once, and
every actor running under that manager interprets the same image through the same slot.

## Falsification pass 2026-10-01 (SWE2-CONTRACT for OPUS)

*A non-author pass: SWE2-CONTRACT wrote none of the dispatch sections it attacks. Static, on the certified image
`73461d08…`; nothing was executed. Record: [`swe2contract-reopened2-0930`](../../_index/candidates/swe2contract-reopened2-0930/README.md).*

**The claim attacked, and why it carries the page.** The 100-entry computed-goto dispatch (§2, §3, §4, §13.1): the
image-base rebase, the `0x63` bound and its default `0025E60A`, the 32-bit RVA table at `00261DF8`, every target inside
the one 14,646-byte body, 92 distinct targets in exactly three shared groups, and the register-file handlers
`0x36`–`0x45`. Every other result on the page is read through this table: BF-1's per-opcode effects, BF-5's inert six,
§11's name alignment, §13's register file and §6's modding notes. Also attacked: the two SECTION-11 entry facts that
reopened the page (the shared value-stack depth at `02099AC0` is zeroed before the refusal test; the 65,536-instruction
budget) and §4's operand pre-decode from `0x47`.

**Method.** `falsify_interp_dispatch.py` decodes the body linearly with capstone from its `functions.tsv` extent,
resolves the `lea` displacement with its sign, reads the 100 table dwords from the image and compares every figure with
the page's. Positive controls: three corrupted copies of the table (one handler moved outside the body, one extra
shared target, one opcode taken out of the default group). Each must fail its matching check, and each does.

**Result: SURVIVED.**

| check | clause attacked | result |
|---|---|---|
| I1 | 14,646 B and 3,229 instructions | survives exactly; the table starts two bytes past the body end (`00261DF6`) |
| I2–I4 | `lea r8, [rip-0x13E5DD]` = `00120000`; `cmp eax, 0x63` / `ja 0025E60A`; the dword table at base + `0x141DF8` = `00261DF8` | survives |
| I5–I6 | all 100 entries land inside the body, each on an instruction start | survives, 100 of 100 |
| I7–I9 | 92 distinct targets; shared `0025E60A` ← 01 02 19 1A 31 47, `0026121A` ← 2A 2B 2C, `002618A8` ← 51 60; span `0025E5EA`–`00261D36` | survives exactly |
| I10–I11 | `0x36`–`0x45` reach the sixteen §13.1 handlers, which move I0–I3 at `r15+0x64`.. and F0–F3 at `r15+0x74`.. through the pop and push helpers | survives |
| I12 | SECTION-11: `0025E4D2 xor r11d, r11d`, then `0025E4D8` stores it to `02099AC0` before any branch; the refusal at `0025E4FF`/`0025E502` returns 1 | survives |
| I13 | SECTION-11: `mov ecx, 0x10000`, then `sub ecx, ebp` with `ebp` = 1 per instruction | survives |
| I14–I15 | the pre-decode starts at `0x47`; `0025E60A` is `mov [rsp+0xC0], ebp ; mov edi, ebp` | survives |
| C1–C3 | the positive controls | each corruption is caught |

Output `falsify_interp_dispatch.out`, `FAILS 0`. The attacked claim needs no correction. The same pass applied FABLE's
RC-16 adjudication to §13.2 and §13.3 (struck and corrected there) and added pointers to four residue sentences that
carried no id.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Input — CLIENT.** `ActorManager_GetRecordByOrdinal` (`00358940`) is also read by the ~~unread~~ 1,936-byte Input-filed body *(read since: it is `00226BE0`, the system-stop registry's request start, which builds the records, marks every actor and raises the dirty flag — [the system stop registry contract](../../00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md) §2; pointer 2026-09-30, SWE2-CONTRACT)*
([the shared neighbours page](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — SERVICE and CLIENT.** `WorldActor_UpdateRuntimeAndScriptExecutionState` calls three small Presentation-filed helpers (42, 42 and 84 bytes). `ActorManager_GetRecordByOrdinal` is called by four Presentation bodies (963 to 4,782 bytes). `BattleUnit_FindMappedDefinitionSelectorByIndex` is called by `PartyCombat_UpdateStanceState` and `BattleUnit_BroadcastPartyCombatTargetRelation`, whose names are battle-side; the Presentation owner label is not explained by those names.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Citation spellings (R5), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — CLIENT.** A 14-byte function this page cites is called by a 58-byte Resource body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — SERVICE.** `0025D9E0` on this page calls `FUN_00261f90`, owned by that layer. What it reaches is a per-object audio state step: it needs `[obj+0x28] == 0` and bit 6 of `byte[obj+0x10]` clear, then sets bit 5 of that same byte and notifies through `0037C910`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B810` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAction — SERVICE.** `00234150` on this page calls `BattleUnit_SetupEngagedActionState`, owned by that layer. What it reaches is ninety bytes that arm the guard rolls: it **sets bit 23 of the unit's `dword[+0]`** - the bit the parry and special-guard draws both gate on - clears `dword[+0xDCC]`, and points `[+0x6E8]` at `01EEC3C0` or `01EEC410` according to the stats record's `byte[+5]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT (35 edges, one fan-in).** All 35 edges are CombatFormula bodies calling `0031B860` on this page: the reverse lookup from a stats record to its owning battle unit that this page documents. `BattleFormula_RollGuardParryMode` is the worked example - it needs the owning unit before it can test bit 23 of its `dword[+0]`. The crossing is **one shared primitive with 35 callers**, not 35 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — SERVICE.** `0025D9E0` on this page calls `FUN_00234150`, owned by that layer. What it reaches is a 104-byte registration helper that takes the `.text` address `002FED60` as a callback and gates on `byte[+0] & 0x10` of what `0031B810` returns; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Items_Equipment_Shops_License — CLIENT.** `Inventory_QueryOwnedCountIncludingReservedActionItems`, owned by that layer, calls `0031B810` on this page. That caller is the owned-count query for an item id, which returns `-1` for the sentinel id `0xFFFF`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `0025D9E0` on this page calls `PartyFocus_GetCurrentPackedActorHandle`, owned by that layer. What it reaches is a seven-byte getter returning the packed handle at `022C7FE0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `Reward_ComputeExperienceForRecipient`, owned by that layer, calls `0031B810` on this page. That caller is the experience computation for one recipient: it needs `byte[rec+5] == 0` and takes its context from `0031B860`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **Movement — CLIENT and SERVICE (25 edges).** 11 inbound (Movement bodies `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `00349680`, `003548B0` call page-cited `VMValueStack_PushFloat32Bits` (00267F60), `BattleUnit_FindMappedDefinitionSelectorByIndex` (0031B810), `BattleStats_FindOwningBattleUnit` (0031B860)); 14 outbound (page-cited `002628B0`, `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `ActorStorage_InitializeRecord` (00266530) call Movement bodies `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `002E6310`, `Movement_UpdateActorFrame` (002E5030)). Substantive edges include `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E6310`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `Movement_UpdateActorFrame` (002E5030); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `002E4A10`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — SERVICE (3 edges).** 3 outbound (page-cited `ActorManager_RunFieldRuntimePass` (0025D9E0), `002628B0` call Save_Load_Settings bodies `SaveImage_GetPersistentPayloadBase` (002EF2B0), `SaveWrite_GetBusyFlag` (00583920)). Substantive edges include `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `SaveWrite_GetBusyFlag` (00583920); the remaining edges run through shared helpers the page cites.
- **World — CLIENT and SERVICE (3 edges).** 2 inbound (World bodies `0025E400`, `002623A0` call page-cited `ActorManager_GetRecordByOrdinal` (00358940)); 1 outbound (page-cited `ActorManager_RunFieldRuntimePass` (0025D9E0) call World bodies `0025E400`). Substantive edges include `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `0025E400`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (11 edges).** 1 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020) call page-cited `ActorManager_RunFieldRuntimePass` (0025D9E0)); 10 outbound (page-cited `ActorManager_RunFieldRuntimePass` (0025D9E0), `002628B0` call WorldAreaField bodies `003EAA70`, `WorldSimulation_ProcessDeferredModeRequest` (0032FC30), `WorldTransition_GetOptions` (003148D0)). Substantive edges include `ActorManager_RunFieldRuntimePass` (0025D9E0) is called by `World_UpdateSimulationTick` (00314020); `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `003EAA70`; `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `WorldSimulation_ProcessDeferredModeRequest` (0032FC30); `ActorManager_RunFieldRuntimePass` (0025D9E0) calls `WorldTransition_GetOptions` (003148D0); the remaining edges run through shared helpers the page cites.
## SWE2-EC7-113 update (2026-09-21) - `008631E0` measured

`008631E0` (84 B) is the
error-record writer behind
`004D3E20` and ~37 other
sites: the out record takes
`word[+0] = 1` and
`byte[+3] = 0x30`, the
`02EAF930` table at index
`dword[02EB37B0]` (which
increments) stores
`r8d | 0x4A000000` at
`+0` and `rdx` at `+8` of
its 0x10 slot, `0020E620`
then resolves a code into
`dword[+4]` of the out
record. `0x4A000000` is the
tag this family stamps on
table entries.
Interior anchor `0086322B`
(the `+4` code store).

`008631D0` (15 B) is the
sibling record init behind
the same `004D3E20` fan-in
(~44 callers): `word[+0] =
dx`, `byte[+3] = 0x10`,
`dword[+4] = 0` - the same
`+3` tag byte and `+4` dword
shape `008631E0` fills,
without the table write.
Interior anchor `008631D3`
(the `+3` tag store).

## What ticks the interpreter, and why nothing else can (FABLE, 2026-09-22)

> **Not `R-5`.** That row asks what schedules **Phyre/Lua** script execution and is a question
> about `PScripting::PScheduler`; this section is about the **zone-script VM**, a different
> subsystem. *I nearly answered `R-5` with this chain — the register row's wording fits both,
> and only the owning page's own item disambiguates it.*

§16a of [the contract](../CONTRACT-interpreter-core.md) records that the interpreter is *called
from* the movement layer's per-unit pump. **The rest of that chain is now measured, and the question —
*what ticks a zone script* — is answered: a per-frame
hook, with no load-time route — and the interpreter has exactly ONE entry image-wide.**

> **The frame dispatcher runs one of three frame handlers; each ticks the world simulation; the
> world tick runs the actor manager's field runtime pass; that pass updates each world actor's
> runtime and script-execution state; and that is the only thing that enters the interpreter.**
> *Named rather than cited by address on purpose — the frame dispatcher and the world tick belong
> to other layers, and citing them here would import their whole edge sets for a statement this
> page does not make. The addresses are in the `R-5` row.*

**The “or load-time only” half is refuted three ways.** The interpreter has exactly **one** direct
call site image-wide; **no** aligned stored pointer to it exists in any section, so no vtable or
dispatch table reaches it; and **no** RIP-relative reference lands in its body, so nothing takes
its address without storing it. *Each sweep carried a planted known positive or was hand-verified
from the bytes.*

*This page already supplied the corroboration from the other direction:* §4 and §12 establish that
a suspending instruction **rewinds the PC** so the interpreter re-runs it when the frame budget
refills. **A VM that yields and resumes is only meaningful under a per-frame driver** — a
load-time run would have nothing to resume into.

