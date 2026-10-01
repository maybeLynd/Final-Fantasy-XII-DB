# OV-5/8(d) residue — per-function index bounds (SWE2-STRUCT, 2026-09-30)

Completion record for `OPUS-REQ-STRUCT-OV58D-RESIDUE-BOUNDS-0930`, against the census at
`commit:a67cad059` (`ov58d_residue.out`, `ov58d_flow.tsv`). Every function was read in the
shipping binary (`73461D08…`), not from census labels. Bases are stated relative to the state
block at `[02EBF190]`; `REC` means `state + 8 + 0x1C8·k` with `k ≤ 0x27` (the bound enforced in
the getters `00320A40`/`00320AB0` — `cmp cl,0x27`); `image` means the save-image block at
`02166480` (= `state − 0x4E68C`); `payload` means `002EF2B0()` = `002EF640() + 0x200`
(`image + 0x200`); `bank` means a pointer obtained through the `0020E600` resolver, i.e. an
authored table row, not state. Region A is `state + 0x4748..+0x4F0F`.

**Verdict: one named reach — `0030E360` — and it reaches region A only if a caller passes a
status/aux byte id ≥ 0x43 while addressing record k = 39 (see §2).** Every other function in
the residue is bounded by code, by loop count, by sentinel, or by the data contract of a base
that is not state.

## 1. INDEXED-UNKNOWN (12 functions — 7 requested reads + the 5 block-copies already hand-read in the README)

| function | name / base | index bound | reaches region A? |
|---|---|---|---|
| `003266C0` | `BattleGroup_RefreshFourActorDefinitions`; `rdi = state + 0x5A48` | four-iteration loop (`cmp rax,4`), writes `state + 0x5A5A..+0x5A97` | no — entirely above `+0x4F10` |
| `00583D60` | `SaveImage_FinalizeHeaderAndChecksum`; `rdi` = image (from `002EF620`/`002EF640`) | slot loop `esi < 9`, `ebp ≤ 9`; writes `image + 0x20..+0x43` plus one `[rax]` from a resolved row | no — image head only |
| `00252D40` | bitfield writer on `[020927C0]` = `image + 0x8200` | `byte idx = cx >> 3`, store at `+0x3244` | no — image head |
| `00254E00` | same base, store at `+0x32C4` | `cx >> 3` | no — image head |
| `003112F0` | `rdi`, `rbx` = caller record args; `r9 = rdi − rbx` (delta copy) | fixed `0x20`-dword copy `rbx+0x5C → rdi+0xBC..+0x138` and `0x20`-word copy `rbx+0xDC → rdi+0x13C..+0x17A` | no — inside one record on each end |
| `0030B180` | `BattleIdClassD_ResetPurchasedEntry…`; `rsi = state + (id & 0xFFF)` | `id` masked to `0..0xFFF`, store at `+0x59C8` → `state + 0x59C8..+0x68C7` | no — above region A |
| `003279B0` | `GambitConfig_AdjustAvailableEntryCountByStatsRecord`; base `state` | `state + 0x5B42 + 0x34·(b + i)`, `b` = `byte[entry+4]` ≤ 255, `i` = loop counter ≤ 2 → `+0x5B42..+0x7D96` | no — above region A |
| `00583C00` | controller-backup restore loop into state (README hand-read) | image-bounded copy | copy route, not index arithmetic |
| `0030B6A0` | `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState`; `r8`, `rax` = descriptor nodes | field writes `r8+8..+0x40` + 48 B node clear | no — arg objects |
| `00229B40` | state→mirror block copy (README hand-read) | image-bounded | copy route |
| `002EF4A0` | `mirror → state` `0x6000`-byte copy (README hand-read) | fixed extent | **this is the known save-restore writer — it covers region A by design, not by index** |
| `005844A0` | state→mirror copy (README hand-read) | image-bounded | copy route |

`003047F0` (REGISTRY-STORAGE class) is the state memset/zero loop — same whole-image class as
`002EF4A0`. `002FD150` is the registry-storage packed handler — writes registry rows, not state.

## 2. RECORD-INDEXED (5 functions — does the index stay inside one 0x1C8 record?)

| function | index | bound | verdict |
|---|---|---|---|
| `0030E130` | — | all stores `[rbx+0x68]` / `[rbx+0x78]` (rbx = REC) | **in-record** |
| `0030E360` | `id = byte arg [rsp+0x40]`, unmasked | `rec + 0xBC + 4·id` (dword) and `rec + 0x13C + 2·id` (word); `id ≤ 0xFF` | **NAMED REACH** — see below |
| `0030FED0` | — | both "indexed" stores are stack writes: `r9` walks `rbx+0x78`, `r10 = 0x10` iterations → `rsp+0x4F..+0x6E`; remaining stores `[rbx+0x40..+0x4C]` | in-record / stack |
| `0030EA40` | `rax = byte [bankrow + 6]` | guarded `cmp byte [rbx+6],7; ja` → `rax ≤ 7` → `rec + 0x17C + 2·rax ≤ +0x18A` | in-record |
| `0031A630` | `rbp = edx` slot | validated by `00317930` (selector compared against 4-entry sentinel table) → `rec + 0x50 + 2·rbp`, `rbp ≤ ~4` | in-record |

**The named reach — `0030E360` (`BattleStats_ChangeStatusAndProcessSideEffects`).** The byte
arg is the augment/status array index; the code applies no bound. `003112F0` shows the
container contract — it copies exactly `0x20` dwords at `+0xBC` and `0x20` words at `+0x13C`,
i.e. ids `0..31` stay in-record. An id of `0x20..0xFF` writes past the arrays; the absolute
extent is `rec + 0xBC .. rec + 0x4B7` and `rec + 0x13C .. rec + 0x33D`. Region-A reach needs
`8 + 0x1C8·k + 0xBC + 4·id ∈ [0x4748, 0x4F10)`: for records `k ≤ 37` no byte `id` reaches;
`k = 38` reaches for `id ∈ [0xB5, 0xFF]`; `k = 39` reaches for `id ∈ [0x43, 0xFF]`; and if a
caller ever passes a `rsi` that is not a `k ≤ 39` record (`k = 40+` bases inside/above region A
already), nearly any `id` lands inside it. The word site reaches for `k = 39` at `id ≥ 0x46`.
Whether a caller ever does this is a caller-data question: in `003112F0` itself the id is `bpl`
looped `0..0x1F` (bounded), and in `0031A410`/`0031A510`/`0031A630` callers the slot arg is
validated through `00317930`. The code alone does not exclude region A; the authored id space
(≤ ~0x1F for augment slots) and the callers' `k ≤ 0x27` record provenance do.

**Update (same commit family, caller-cone audit):** the full caller cone has now been read —
see [`CALLER-CONE-0030E360-0930.md`](CALLER-CONE-0030E360-0930.md). Two call sites falsify the
`id ≤ 0x1F` assumption: `002FDDA0`'s message-switch arms `dx=0x4049`/`0x404A` pass `id = 0xF8`
and `0xD9`, which escape the record for **every** `k` and land in region A for `k ∈ {38,39}`.
Whether region A is actually written reduces to a runtime allocation question — whether any
unit's `qword[unit+0x698]` stats record is ever index 38/39.

## 3. INDEXED-BELOW — base below `state + 8` (38 functions)

| function | base | index bound | verdict |
|---|---|---|---|
| `00234ED0` | stack buffer (`rsp+0x50` init chain) | sentinel `0xFFFF` list, `≤ 0x1D` stores at `−0x858..−0x108` of a stack object | bounded — stack, not state |
| `00235AF0` | `rdx = 0x7370`, then `state + 0x5B10 + rsi` | single dword at `state + 0x7370` + `movups` at `+0x5B10..` | bounded — above region A |
| `002370C0` | `state` | `word [state + i] = 0xFFFF`, `i = 0x5A48..0x5A59` step 2 (`cmp rcx,0x5A5A`) | bounded — above region A |
| `00252610` | `r9 = [020927C0]` = `image + 0x8200` | `eax = min(edx, edi)` via `cmovg` — clamped to `r8 + 0x64` | bounded — image head |
| `002527B0` | `image + 0x8200` | `edx` clamped `≤ 0x64` (`cmovg`) → `+0x90 + 4·i`, `+0x70 + i`, `+0x30 + 2·i` | bounded — image head |
| `00252E60` | `rdi = image + 0x8200 + 4·edi` | table-append counter cell, `edi` = entry count | bounded — image head |
| `00253240` | `rbx` = static row `02097260 + 8·esi` | `esi ≤ 0xB` (`cmp esi,0xB; jbe`, else arg→0) | bounded — static table / image head |
| `002534C0` | `r14 = image + 0x8200 + 4·ecx` | `ecx ≤ 0xB`; copy count = `dword [r14+0x47B8]` (image count cell) | bounded — image head + bank rows |
| `0030C470` | `rbx = rcx` arg record | field writes `+0x1C2`, `+8`, … `≤ +0x1C2` | in-object (record) |
| `00315820` | `rax = 002536A0()` = `image + 0x8200` | `ecx < 0x200` → `+0x32CC + ecx` | bounded — image head |
| `00315910` | `image + 0x8200` | `rdi = (esi + word[cls+…]) >> 3`; `esi` bounded by per-class bit count (`cmp/jae`) | bounded — image head |
| `00315A20` | `image + 0x8200` | `ecx < 0x100` → `+0x32CC + (ecx>>3)` | bounded — image head |
| `00315A90` | `image + 0x8200` | `ecx < 0x200` → `+0x3404 + ecx` | bounded — image head |
| `00315AD0` | `image + 0x8200` | `edi < 8` → `+0x3604 + rsi` | bounded — image head |
| `00315B50` | `image + 0x8200` | same per-class bitcount pattern as `00315910` | bounded — image head |
| `00315CD0` | `image + 0x8200` | `ecx < 0x100`, `dl < 0x10` → `+0x336C + (ecx>>1)` | bounded — image head |
| `00315E90` | `image + 0x8200` | `esi < 0x1E` → `+0x3844 + (esi>>3) ≤ +0x3847` | bounded — image head |
| `00316930` | `image + 0x8200` | loop `edi < 0x200` → `+0x3404 + edi` | bounded — image head |
| `00316A50` | `image + 0x8200` | `esi < 0x1E` → `+0x3844` area | bounded — image head |
| `00316DF0` | `rdi` arg record | `or [rdi]`, `[rdi+0x48]` — no index | in-record |
| `00317480` | `r14` arg record | `[r14+0x190]` — no index | in-record |
| `00323540` | `rdi` arg record | `and [rdi]` — no index | in-record |
| `00329CC0` | `REC` via `dil ≤ 0x27` (twice) | writes through bounded helpers `00323540`/`00316DF0`; `rsi` walk `0x5A48..` is read-only | bounded — in-record |
| `0032AB60` | `payload` | `ecx ≤ 0x1FD+2` (`cmp eax,0x1FD; ja`) → `edi ≤ 0x40` → `+0x14F4 + edi` | bounded — image payload |
| `0032ABF0` | `payload` | `ecx ≤ 0x7FF` → `edi ≤ 0x100` → `+0x13B4 + edi` | bounded — image payload |
| `0032AC70` | `payload` | `ecx < 0x40` → `edi ≤ 8` → `+0x1384 + edi` | bounded — image payload |
| `0032ACF0` | `payload` | `ecx < 0x40` → `edi ≤ 8` → `+0x138C + edi` | bounded — image payload |
| `0032AD70` | `payload` | `ecx ≤ 0xFF` → `edi ≤ 0x20` → `+0x14B4 + edi` | bounded — image payload |
| `0032ADF0` | `payload` | `ecx ≤ 0xFF`, `eax = ecx+0x100` → `edi ≤ 0x40` → `+0x14B4 + edi` | bounded — image payload |
| `003C5E50` | `rax = 002551B0()` slot object (`02B4xxxx` region) | `movups [rax]` / `[rax+0x10]` — no index | bounded — slot object |
| `003C60F0` | same (`002551B0`) | same | bounded — slot object |
| `003C8670` | same (`002551B0`) | same | bounded — slot object |
| `0046B290` | `payload` | `edi = id>>3`, `bl = bit`; `+0x1000`/`+0x1020` bitfields; `id` = save-flag arg (flag-table data) | bounded to flag-array — reaching `state + 0x4748` would need `id ≈ 0x273140`, outside any flag id |
| `0046B350` | `payload` | `rbx = id` → word `+0x1164 + 2·id` | bounded — flag entry table |
| `0046B380` | `payload` | `edi = id>>3` → `+0x1364` | bounded — flag array |
| `0046B3F0` | `payload` | `edi = id>>3` → `+0x1000`; `rsi = id` → word `+0x1164 + 2·id` | bounded — flag arrays |
| `0046B490` | `payload` | `rbx = id` → byte `+0x1064 + id` | bounded — flag byte array |
| `00583D60` | image head | `esi < 9`, `ebp ≤ 9` → `+0x20..+0x43` | bounded — image head |

## 4. INDEXED-BELOW — base inside the record array (27 functions)

`REC` bases all come through `00320A40`/`00320AB0` or equivalent inline `cmp 0x27` guards —
records end at `state + 0x4748`.

| function | index | bound | verdict |
|---|---|---|---|
| `00239960` | — | `rbx = 00320A40()` (REC or NULL, guarded); writes `+0x20..+0x1C0` | in-record |
| `0023AC80` | — | `rdi` = REC arg (init, `memset 0x1C8` + field tail) | in-record |
| `002FEF30` | — | `rsi` = caller buffer (`rdx` arg or `rdi+0x24`); fixed `0x24`-byte init | bounded — arg object |
| `00300530` | — | `[rsi+0x48]` — arg object, no index | in-object |
| `00300BC0` | — | `[rdi+6]` — arg object | in-object |
| `00300CE0` | — | `[rsi+0x4C]` — arg object | in-object |
| `0030C650` | — | `rdi` arg record fields `+8`, `+0xC` | in-record |
| `0030E060` | — | `[rdi+0x4E]` — arg object | in-object |
| `0030E130` | — | `[rbx+0x68]/[+0x78]` | in-record |
| `0030E360` | `id` byte arg | **named reach — §2** (also flagged INDEXED-BELOW on its in-record sites `+0x38/+0x3C/+0x64`) | **NAMED REACH** |
| `0030EA40` | `byte[bankrow+6] ≤ 7` | `rec + 0x17C..+0x18A` | in-record |
| `0030FED0` | — | stack writes + `[rbx+0x40..+0x4C]` | in-record / stack |
| `003112F0` | — | delta copies `rdi+0xBC..+0x17A` (fixed `0x20` loops) | in-record |
| `00311AF0` | — | `rax = 00320A40()` (REC/NULL); `or/and [rax]` = `rec + 0` | in-record |
| `00318B40` | — | `[rbx]`/`[rbx+2]` — `rbx = rcx` arg | in-object |
| `0031A410` | `r14` slot | `cl ≤ 0x27` → REC; `r14` validated by `00317930` → `rec + 0x50 + 2·r14` | in-record |
| `0031A510` | `r15` slot | `cl = byte[state + 2·rbx + 0x5A7E] ≤ 0x27` → REC; `r15` via `00317930` | in-record |
| `0031A630` | `rbp` slot | `00317930` validation → `rec + 0x50 + 2·rbp` | in-record |
| `003236F0` | `cl` byte arg | `r8 = state + 8 + 0x1C8·cl`; store `+0x1C4/+0x1C5` — for `cl ≤ 39` in-record; for `cl ≥ 40` the stride lands the store at `≥ state + 0x4FED` — the `0x1C8` stride **skips over** `0x4748..0x4F0F` entirely | bounded — cannot land in region A for any `cl` |
| `00323740` | `cl` byte arg | same shape, store `+0x1C3/+0x1C5` | bounded — same stride argument |
| `00323790` | — | `[rcx+0x190]` / `+0x190` — arg record, no index | in-object |
| `00323910` | `rdx = −byte[bankrow+4]` | negative index → `rdi + 0x95..+0x194` | in-record |
| `003242F0` | — | `[rdx+0x1C5]` — arg record | in-record |
| `00327CB0` | `rbx` list counter | sentinel-terminated: loop exits on `word == 0xFFFF` in the bank word list → `rdi + 0x88 + 4·i`, `i` ≤ authored list length | bounded — authored sentinel |
| `00328990` | `rdx = rsi>>3`, `rsi` = authored table word | `r14` = REC; sole caller `00328BD0` bounds record kind `≤ 5` → max write `state + 0x9A8 + 0x194 + 0x1FFF = state + 0x2B3B` | bounded — caller clamps `k ≤ 5` |
| `00328BD0` | `ebx ≤ 5`, `bl ≤ 0x27` | `rdi = REC`; `[rax−0x10]/[rax]` loop = `rdi + 0x68..` (16-iter window), `[rdx+0xBA]` bank row, `[rdi+0x20..+0x1C5]` | in-record |
| `00329220` | `rdx = rdi − r14` (delta) | 4-byte copy at `rdi + (src−0x1C..0x19)`; remaining writes `rdi+0x20..+0x62` | bounded — arg objects |

## Method note

Census classes `INDEXED-BELOW`/`INDEXED-UNKNOWN` were found to contain three different things:
(i) genuinely unbounded-looking index arithmetic — resolved by caller clamps (`00328990`),
stride arithmetic (`003236F0`/`00323740`), or sentinels (`00327CB0`, `00234ED0`);
(ii) induction-window artifacts — loop unrolling produced displacement lists at trip values
the bound never reaches (`003266C0`, `00329220`, `00235AF0`, `002FEF30`);
(iii) bases that are not state at all — `image + 0x8200` (the `002536A0`/`020927C0` family,
28 of the 38 below-`+0x8` functions), `payload` = `image + 0x200` (the `0032AB*`/`0046B*`
family, 11 functions), and `002551B0` slot objects (`003C*` family).

The three census limits recorded in the README (437 depth cuts, 15 indirect calls, 26 escapes)
are untouched by this record — they are out of scope for the bound exercise.
