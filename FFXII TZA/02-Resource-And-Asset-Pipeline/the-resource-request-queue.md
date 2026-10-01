---
system: The resource request queue — 64 reusable slots, generation-tagged requests, head-driven pumping and guarded callbacks
category: 02-Resource-And-Asset-Pipeline
status: "PARTIAL — SECTION-02 corrects and exercises queue core; the four items outside it are bounded by named records (2026-09-30, SWE2-CONTRACT for OPUS, DD batch 13, section 7b): deeper services by section 8 here, CONTRACT-storage-read-completion for the storage machine and OV-19 / OV-33 (static parts answered, service timing RT under FABLE-REQ-ASTRA-RT-REMAINDERS-0929); live scheduling is runtime-only (SECTION-02 review Q3, the same RT remainder); the path copy by EO-3 SUPERSEDED (live remainder FABLE-REQ-ASTRA-EO3-PATH-POINTER) and section 7b (freed once on every single-call path, twice on a repeated cancel), the callbacks by DD batch 6 Z2 (no part callback) and OV-36 (single delivery); authored reachability by DD batch 6 Z2 and the music-control page (the chunk gate), with which requests run under an active stream runtime-only (was — deeper services, live scheduling, path/callback lifetime and complete authored reachability remain separately bounded). Residue reconciled 2026-09-30 (SWE2-CONTRACT, DD batch 6): the six asking-form callers read, the +0 accumulator and the 16-byte gap shown unread, the part callback shown never installed, EO-3 SUPERSEDED (FABLE 2026-09-26); SECTION-02 peer acceptance is a class-2 process item carried by SWE2CONTRACT-REQ-AUDITSPEC-SECTION02-ACCEPT-0930; the status word waits for OPUS owner read."
owner_layer: PrimaryOwner:Resource
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "3 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-22
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-resource-request-queue-pass-1
  crossref_clean: false
  reopened_count: 0
production_review:
  section: SECTION-02
  by: external-continuation
  status: "PRODUCTION COMPLETE; formal peer acceptance pending"
  evidence: _experiments/evidence/continuation-section02-resource-queue/REVIEW.md
  audit_scope: "The existing audit/annotation-transfer metadata is historical, not acceptance of these edits."
---

# The resource request queue — 64 reusable slots, generation-tagged requests and a head-driven pump

> **The documented resource callers share a pool of 64 requests.** A requester supplies a kind/index
> or a path route, destination, byte count and descriptor. The requester copies two callbacks and
> an argument word; it clears the separate part-callback slot. The pump repeatedly services the
> pending head and can traverse several states and requests in one call. A full queue makes the
> requester pump and pace synchronously until a slot returns. Splitting is gate-dependent, not an
> unconditional consequence of exceeding 512 KB.

**Current production verification:** [SECTION-02 original-code review and controls](../_experiments/evidence/continuation-section02-resource-queue/REVIEW.md).
This section corrects conflicting list/formula summaries and the later queue-head declaration.
It does not recertify every historical caller census, underlying service or installed-game behavior.
The [current contract](CONTRACT-resource-request-queue.md) gives the complete bounded queue rules.

*Peer acceptance (SWE2-CONTRACT, 2026-09-30):* the front matter's "formal peer acceptance pending" is a process
item, not a knowledge question (class 2 of `_index/candidates/register-idless-boxes-0929/`). It is carried by the
board request `SWE2CONTRACT-REQ-AUDITSPEC-SECTION02-ACCEPT-0930` to SWE2-AUDIT-SPEC. The earlier OV-acceptance batch
(`FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929`) covered other 02 sections, not SECTION-02. OPUS's falsification
pass on the contract (`_index/candidates/request-queue-falsification-pass-1-0930/`, Q1–Q5) was accepted by
SWE2-AUDIT-SPEC in `OPUS-REQ-AUDITSPEC-REVIEW-BATCH10-0930`.

## 1. What the player sees

The documented loading paths use this queue. A saturated queue can delay a caller while work is
serviced, but no duration or visible hitch was measured here. There is **no queue-level rule that
a request waits until the next frame**: the frame wrapper, explicit drain and full-pool stall all
call the same pump, and one invocation can issue, observe completion and recycle multiple slots.
The controls also show zero-byte requests calling completion without issuing any file read.

## 2. Native mechanism

### 2.1 The slots and the lists

`0032E450` builds the pool at boot: **64 slots of `0x80` bytes at `022C31C0`**, threaded onto a free
list (`0032E460`–`0032E4A1`, whose cursor runs at **slot `+0x18`**, so its displacements are not
slot offsets: slot **`+0x58`** = its index, **`+0x64`** = −1, **`+0x20`** a zero word and
**`+0x28`** a zero dword, with **`+0x10`** the next slot and **`+0x18`** the previous — *corrected
2026-09-13; this read `+0x40` / `+0x4C` / `+8` / `+0x10`, the instruction displacements*), the
free head at `022C51D0` (`0032E4B1`), the pending head and tail at `022C51C0` / `022C51C8` cleared,
and the request counter at `01EED498` set to 1 (`0032E453`). `0032EA90` (the resource system's
initialiser) calls it, resets the read layer (`003EB050`) and clears the 256 per-kind size-override
pointers at `022C51F0` (`0032EAA0`–`0032EAD8`; corrected from 41 on 2026-09-13 — the loop is `0x20` × 8 qwords),
whose writer-absence claim belongs to the existing DG-6 census, not a new whole-image absence proof in SECTION-02.

`0032E990(flag)` pops the free head and links the slot into the pending list — at the tail when
`flag` is non-zero, at the head otherwise (`0032E9C4`–`0032EA4A`); `0032EC40(slot)` unlinks it from
wherever it is, pushes it back on the free list and sets `+0x64 = −1` (`0032EC40`–`0032ECC5`).
**Neither function clears the whole slot.** The constructor preserves unlisted bytes; the splice
changes linkage/id only and leaves state clearing to its callers. The queue record at `022C51C0`
therefore has **freeHead at +0x10**, not a fixed `slotArrayBase`: `0032E9B5` advances it and
`0032ECBE` pushes a recycled slot. Its initial value happens to equal the pool start. Pending tail
at `+8` is established by actual head/tail insertion and removal, not merely inferred from proximity.

### 2.2 The builder — `0032E620(kind, index, dest, bytes, &descriptor)`

`0032E620` records the selector and index in `022C51D8` / `022C51DC` (`0032E634`–`0032E63D`; a
negative index returns −1), asks whether the script BGM stream is active (`003EB0D0`: the one `0x38`-byte descriptor at
`02B5E0E0` with its `+0x31` set, `003EB0D2`–`003EB0F8` — [the music-control page](../18-Audio/the-music-control-file-and-the-bgm-stream.md) §3).
**When it is not, it falls to `0032E742` and calls
`0032E870(kind, index, dest, bytes, &descriptor, 1)` whole** (corrected 2026-09-11; this page first
read the chunked path as unconditional). Only while a stream is active does it copy the caller's
`0x28`-byte descriptor to its stack or zero one (`0032E678`–`0032E6AF`), call
`0032E870(kind, index, dest, bytes, &copy, 1)`, and on a non-zero request id make the request
**chunked**: `+0x22 = 1`, `+0x30 = 0x80000` (the part cap), `+0x34 = bytes` (remaining), the
first part `+0x28 = min(bytes, 0x80000)`, `+0x50 = 0`, and the file offset `+0x2C` ~~rounded up to~~
**truncated toward zero to a multiple of** `0x800` (`0032E6E9`–`0032E735`; see §*one instruction*
below). The bytes come from the caller, who takes them from
[the file-size table](Loose-Files-And-Size-Tables/file-size-tables-fst.md) through `0032E400`.

`0032E870` is where the queue's only stall lives: **while the free head is null it pumps** —
`0032E070(0)`, `0046DFE0`, `0035EA30(0)` — and loops (`0032E88D`–`0032E8C3`), so a sixty-fifth
request blocks its caller until a slot returns. Then it takes a slot (`0032E990`) and fills it
(`0032E8CE`–`0032E97C`): `+0x24` index, `+0x2C` the descriptor's `+0` offset **truncated toward zero
to a multiple of** `0x800` — ~~rounded up~~, see §*one instruction* below —
`+0x28` bytes, `+0x20 = 1` (queued), `+0x21` kind, `+0x64` the request id — the counter at
`01EED498` shifted left six and or-ed with the slot index, the counter wrapping at `0xFFFFFF`
(`0032E90D`–`0032E947`, signed increment comparison over the constructor-derived domain `1..0xFFFFFF`) — `+0x38` and `+0x70` dest, `+0x40` / `+0x48` the descriptor's `+0x10` /
`+0x18`, `+0x60` its `+8`, word `+0x22`, `+0x5C` and `+0` zero. It returns the request id.
Descriptor `+0x20` is **not** copied to slot `+0x50`; that slot is unconditionally zeroed at
`0032E959`. The chunked builder also clears it at `0032E6FF`. Descriptor `+4` is not consumed
by this requester. Unwritten stamps, caps and tail bytes can retain earlier contents.
`0032E780` provides the negative-index-guarded head-inserting wrapper; its effect on list order
is directly tested, while higher-level priority policy remains separate.

### 2.3 The pump — `0032E070`, six states

Called once per frame by `0032E040` when a loader is present (`001EDE80()` or `0017D930()`) —
from **every one of the seven main-loop mode bodies** of [the between-two-frames page](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) (mode 0 `0022B6E0` at
`0022B7A9`, mode 1 `0022B7E0` at `0022B870`, the field frame `0022A770` at `0022AE79`, the full
menu `0022B8C0` at `0022BB03`, the screen capture `0022AF50` at `0022AFB5`, mode 5 `0022BC20` at
`0022BD53`, mode 6 `0022B000` at `0022B055`), from boot `0022A0B0` (`0022A460`), from the script
native `0036EEB0` (thunk `0050EA60`), which pumps inside a wait loop with `0036D890`,
`0035EA30(2)` and `0036F000` until two `0x18`-stride state tables leave states 1–2, and from
`00379E30` — and by `0032E520(0)`, which drains: pump, then while the pending head `022C51C0` is
non-null or a read is in flight (`0046DFE0()` is 2 while the status word `0215EFF4` is −1)
`0035EA30(0)` and pump again, returning 0 when idle (`0032E561`–`0032E586`; callers `0024AC30`,
`002628B0` ×3, `0032F430`, `003601D0`, `003B0660`, `003DEC90` ×2, `003DEE10` ×2, `003EA200`,
`003EAD10` ×2, `0050D9A0`, and the second site of `WorldTransition_StageFieldTransition`,
`00314621`). **`0032E520` with a non-zero argument does not pump**: it only answers whether
anything is outstanding — 1 when the pending head is non-null or a read is in flight
(`0032E524`–`0032E560`). That is the form the two boot modes call (`0022B737` and `0022B837`,
`mov ecx, 1`; corrected 2026-09-12 — this page said `0032E520(0)`): each boot stage pumps once a
frame like every other mode and advances on the first frame the queue is idle — mode 0 to mode
1 when also the byte `0209273C` is 5, mode 1 to mode 2 when also `0037C2E0()` is 0. Two boot
places because there are two boot stages, each with its own second condition. The asking form's
other callers are `WorldTransition_StageFieldTransition` (`00314609`, 1) and `0050E1E0` (1);
`002FC3C0`, `003B1310`, `003B1710` and `003B18E0` pass `rax + 1` and `0034DB30` / `0050D0C0` a
register — ~~those six are unread~~ *read 2026-09-30 (SWE2-CONTRACT, DD batch 6, `_index/candidates/swe2contract-ddres-b6-0930/b6_request_queue.py` A0–A6): all six pass 1, the non-draining ask. The four `rax + 1` sites reach the call only after `0032E4D0` returned 0 for their own request, and the two register sites hold 1 in `edi` / `ebx` from their prologue. Five act only on "idle": `002FC3C0` clears `02EC3D7C`, `003B1310` / `003B1710` / `003B18E0` call `003B21E0`, and `0034DB30` continues its state. `0050D0C0` calls `00314D40(1)` and reports busy while anything is outstanding.* Each pass takes the pending head (`022C51C0`, `0032E090`) and dispatches on `+0x20`
through the six-entry table at `0032E2D0`:

| state | meaning | what the pass does |
|---|---|---|
| 1 | queued | if the read layer is idle (`003EADD0`, `0032E0BD`): `+0x28 == 0` → the done callback and release (`0032E130`–`0032E13F`); kind ≠ `0xFF` → `0046E030(kind, index, offset, bytes, dest)` → `002DF780`, the read issue (`0032E0D3`–`0032E0F1`); kind `0xFF` → `002DF6C0(index, dest, offset)`, where `index` **is a path pointer** (`0032E105`–`0032E118`); then `+8` = the clock (`0035E810`) and state 2 |
| 2 | issued | `+0` += the counter (**not** elapsed — see below), `+8` = the same reading, state 3 (`0032E149`–`0032E15A`) |
| 3 | waiting | `0046DFE0()` non-zero (the read status word `0215EFF4` is −1: **still in flight**) → leave; else state ← 5 + (`0046E0E0()` < 0), i.e. 5 delivered (the word is ≥ 0) or 6 failed (negative other than −1) (`0032E163`–`0032E1A8`) — address and meaning corrected 2026-09-11, §8 |
| 4 | cancelled | the same entry: `0046DFE0()` clear → the cancel callback `+0x48(+0x60)` with `+0x28 = 0` **when the callback exists**; absent callback preserves that count; then release (`0032E170`–`0032E197`) |
| 5 | part delivered | not chunked → the done callback `0032E330` and release (`0032E266`–`0032E280`); chunked → `+0x34 -= +0x28`; nothing left → done and release (`0032E1ED`–`0032E1FF`); else advance `+0x2C` and `+0x38` by the part, ask the part callback `0032E3B0` (`+0x50(slot)`; 1 = requeue, 2 = pause/re-probe, 3 = return with progress 3 rather than a release; see the callback distinction below; out-of-range values report through `008620C0`), and on 1 size the next part and go back to state 1 (`0032E201`–`0032E248`) |
| 6 | failed | not chunked → the error callback `0032E370` and release (`0032E285`–`0032E296`); chunked with `+0x23 == 2` → the part callback decides as above (`0032E24D`–`0032E264`); else error and release (`0032E1CD`–`0032E1E8`) |

Every returning pass, including empty/busy/drained cases, reaches the common footer: the read layer's tick `0046DD50` (a four-state machine over `02CA6068`),
`003E9780` and, when `0036FD50()` says so, `003BB790` (`0032E2A0`–`0032E2BD`).

#### The pump executed — EXP-128, adopted 2026-09-20 (OPUS)

[`EXP-128-exp109-poll-pump-exec.md`](../_experiments/EXP-128-exp109-poll-pump-exec.md)
(SWE2-ORACLE) runs this pump natively: **137 of 137 cases, 123 of 123 mutants killed**, three-process
stability. **The historical six-state interpretation was broadly corroborated; SECTION-02 below distinguishes callback outcomes and invocation timing more precisely**, which is the main result and the
least quotable one. Four things it adds, and one correction.

**State 2 does not compute an elapsed time, and the page said it did.** The arm is five
instructions and I read them rather than adopting the summary:

```asm
0032E149  call 0035E810          ; the counter -- RESULT DISCARDED
0032E14E  call 0035E810          ; read again
0032E153  add  qword ptr [rbx], rax      ; +0 += the counter itself
0032E156  mov  qword ptr [rbx+8], rax    ; +8 = the same value
0032E15A  mov  byte  ptr [rbx+0x20], 3
```

`0035E810` is **eight bytes** — `mov rax, qword ptr [022CA5E0]` / `ret` — a plain getter of an
absolute counter with no delta and no getter-side effect. The first return is discarded; the
**second** is added and stored. Stable fixture memory makes both reads equal, but the getter alone
does not exclude an intervening external writer in a live process. `+0` accumulates **absolute counter readings**, not elapsed time: there is
no subtraction of the `+8` stamp anywhere in the arm. *What `+0` is therefore FOR is not settled by
this — an accumulator of absolute timestamps is either a deliberate running sum or a defect, and
nothing here distinguishes them. The row above is corrected to what the instructions do.*

*Answered 2026-09-30 (SWE2-CONTRACT, DD batch 6, `_index/candidates/swe2contract-ddres-b6-0930/b6_request_queue.py` M1–M2, Z1, Z3; static): nothing reads it.* The
question above is closed as far as this build goes:
- In the queue module the only accesses to slot `+0` are this add (`0032E153`) and three stores of 0: `0032E229`
  (requeue), `0032E725` (the chunked builder) and `0032E97C` (the builder).
- Only queue functions address the pool: they reference it rip-relative, and no instruction displacement equals a
  pool RVA.
- The module's five indirect calls pass `+0x60` (and `+0x70`), except the part callback, which nothing installs
  (§2.4).

So the accumulator is written and never consumed. Whether it is a leftover or a defect is not a static question and
is not claimed. Limit: the module's direct calls out were read from the listing and pass field values; they are
not machine-checked.

**State 5's part arithmetic has two details the table compresses away**, and a reimplementation
without them diverges:

- the next part is sized `+0x28 = min(+0x30, +0x34)` — the cap against what remains, by
  `cmp` + `cmovl`;
- `+0x2C` then **rounds DOWN to a `0x800` boundary**, by `cdq` / `and edx, 0x7ff` / `add eax, edx` /
  `and eax, 0xfffff800` — the signed-bias form, so a negative `+0x2C` rounds toward zero rather than
  away. EXP-128 verifies that with a negative-`+0x2C` case. *(The operand list previously named a
  `subtract` that is not in the sequence; corrected 2026-09-21 while fixing the same idiom elsewhere
  on this page.)*

### One instruction separates rounding up from truncating — 2026-09-21 (FABLE, on `ASTRA-CONTRA-FABLE-RESOURCE-OFFSET-AND-COUNT`)

**This page said the initial file offset was *rounded up* in three places and *rounded DOWN* in a
fourth.** The fourth was right. The sequence, identical at both builder sites, is

```text
0032E8FB  cdq                     ; EDX = the sign mask of the 32-bit offset in EAX
0032E8FC  and  edx, 0x7ff         ; bias = 0 when non-negative, 0x7FF when negative
0032E90B  add  eax, edx
0032E913  and  eax, 0xfffff800
0032E918  mov  dword ptr [r10 + 0x2c], eax
```

— and `0032E721`–`0032E735` repeats it on the chunked rewrite. **The bias is the sign mask, so a
non-negative offset gets no bias at all**: `0x801` → `0x800`, `0x7FF` → `0`, `-0x801` → `-0x800`,
aligned values unchanged. *That is truncation toward zero, and for every ordinary positive offset it
is a floor.* **A reimplementation that rounds up reads from the wrong sector** whenever the offset is
not already aligned.

**What makes the old wording forgivable and this correction durable is that the difference is one
instruction.** `0032E400`, the size lookup, *does* round up — to 64 — and it does so with the **same**
four-instruction idiom preceded by an explicit positive bias:

| | `0032E400` (the size) | `0032E870` / `0032E620` (the offset) |
|---|---|---|
| guard | `0032E43D jle` — a non-positive size is returned **unrounded** | none |
| **bias** | **`0032E43F add eax, 0x3f`** | **absent** |
| idiom | `cdq` / `and edx, 0x3f` / `add eax, edx` / `and eax, 0xffffffc0` | `cdq` / `and edx, 0x7ff` / `add eax, edx` / `and eax, 0xfffff800` |
| result | **rounds up** to a multiple of 64 | **truncates toward zero** to a multiple of `0x800` |

So "rounded up" is exactly right for the size and exactly wrong for the offset, and the two are told
apart by the presence of `add eax, 0x3f` — not by the mask, which looks the same in both.

**And the byte count is not the offset.** `0032E88A` copies `r9d`, the byte count, into `esi`, and
`0032E92C` stores `esi` at **`+0x28`**; `+0x2C` is the descriptor's offset. *(The FST page said the
table size becomes `+0x2C`; corrected there in the same commit.)*

### Entry is not loading — and one of the three entry points has a different ABI (2026-09-21, FABLE)

`FABLE-REQ-ASTRA-KIND-INDEX-TRACE` is mine, and it proposed logging three entry points during a
broad play route to decide **which resource families are actually used**. The bodies already show
it could not have answered that:

- **`0032E620` writes its selector globals *before* deciding.** The current selector/index globals
  are stored at `0032E634`/`0032E63D`, and only then does the signed gate at `0032E64A`/`0032E64C`
  reject a negative index and return `-1` at `0032E64E`/`0032E651` — **without building a slot**. A
  logged entry is a request *attempted*, not accepted.
- **Acceptance is not issue.** The pump reads and tests `+0x28` at `0032E0CA`/`0032E0CE`/`0032E0D1`
  and branches on **zero bytes** to `0032E130`, which calls the done helper `0032E330` and the
  release `0032EC40` **without ever traversing the read issuer**. A completed record with a
  callback does not establish that a file was read.
- ***And one of the three does not take a kind/index tuple at all.*** `0032E7C0` takes a **path** in
  `rcx` (`0032E7DA`–`0032E7E8`), copies it, and passes kind `0xFF` with a pointer to `0032E870`
  (`0032E833`–`0032E84D`). **A trace keyed on `(kind, index)` would have recorded nothing for the
  path route and read that silence as absence.**

So a trace of these three sites yields *attempts*, mixed with a family it cannot represent. The
distinctions a usable observation must keep are **size query → attempted → accepted record → issued
read → callback → delivered and used**, and `0032E400` needs its **full `rdx`** preserved, not the
low dword, because `0032E41F` compares and `0032E428` indexes with the whole register.

**`0046E030`'s fifth argument is read from `rsp+0x28` at callee entry**, not `+0x20` — the
caller's outgoing-argument slot sits above the return address. The experiment's first model read
`+0x20` and produced a systematic difference, which is how the slot was pinned.

**`0032E370`'s gated-out return is the callback pointer, not zero**: the gate skips only the
`call rax`, and `rax` was loaded at entry. And `003697F0`, in the retire arms' free tail, is a
**PREL thunk** (`test rcx,rcx` / `je` / `xor edx,edx` / `jmp`) rather than a boundary — so the
retire path runs the real allocator free path end to end, the one EXP-126 executed.

**One observation that is deliberately NOT recorded as a property of the pump.** The experiment
notes that the direct `call 0046DFE0` arrives with `rdx` and `r8` still holding whatever the
previous arm left. That is true and it is an artefact of the callee taking no arguments — dead
registers are dead, and writing it here would invite a reader to think the values mean something.
It belongs to the harness's model, where it is recorded, and not to this contract.

### 2.4 The callbacks

| slot | from the descriptor | called | signature |
|---|---|---|---|
| `+0x40` | `+0x10` | on delivery by `0032E330` (`0032E336`–`0032E34F`), on failure by `0032E370` (`0032E376`–`0032E392`) | `cb(+0x60, dest0 = +0x70, ok)` — `ok` = 1 delivered, 0 failed; `0032E370` calls it only when `+0x28 == −1` |
| `+0x48` | `+0x18` | on cancel completion (state 4) and by `0032E590` for a request not yet issued (`0032E2F0`, `0032E302`–`0032E30C`) | `cb(+0x60)`, with `+0x28 = 0` |
| `+0x50` | **not copied from descriptor +0x20 by these requesters; initialized null** | consulted between parts (`0032E3B0`) | `int cb(slot)`; null returns 1; see the result-specific behavior below |
| `+0x60` | `+8` | — | the word handed to `+0x40` and `+0x48` as their first argument |

**Part callback returns 2 and 3 are not equivalent terminal outcomes.** `0032E3B0` returns 1
when no part callback exists. The pump stores a nonnull callback result at `+0x23`. Result 1
requeues; result 2 leaves the request pending and selects the re-probe branch on a later call.
Result 3 also returns without releasing the record, but a subsequent state-5 pass need not re-probe:
it can repeat subtraction of the previous part. Seeded callbacks distinguish this behavior; actual
shipped producers of these states are not established by the controls. Do not flatten all non-1
results into "cancel" or "finished". The common footer is not proof of queue shutdown.

*Answered 2026-09-30 (SWE2-CONTRACT, DD batch 6, `_index/candidates/swe2contract-ddres-b6-0930/b6_request_queue.py` Z2; static): no shipped code produces them.* The
part-callback slot `+0x50` is stored only as 0: at `0032E6FF` with `r14 = 0` (`0032E670`, not rewritten before the
store), and at `0032E959`. It is read only at `0032E3B4`, so `0032E3B0` returns 1 in the shipped build. Results 2
and 3 are reached only by the seeded callbacks of the SECTION-02 controls. The rest of this paragraph describes
what the pump would do and is kept as written.

**The first argument of the delivery callback is the descriptor's `+8` word, not the buffer.** A
requester that wants its bytes reads them at `dest0`. The twelve licence-board requests of
`00238260` hand `3` in that word (`00238364`), so their generated setters (`00238390` + `0x30·k`)
store **3** into registry slots `02EBF1A0`–`02EBF1F8` on delivery and on failure alike — the slots
are completion markers, and the board bytes live in the resource block the loader allocated
([the registry page](authored-data-table-registry.md), *the tail read*, corrected 2026-09-11).
With a null descriptor, `0032E870` clears the two copied callbacks and argument; it clears the
part callback regardless of descriptor presence. The pump's callback sites test for null (`0032E33D`, `0032E37D`, `0032E3BB`).

### 2.5 Asking and cancelling

`0032E4D0(id)` says whether request `id` is still in flight: the slot at `id & 0x3F` must carry
`+0x64 == id` and a non-zero state (`0032E4DD`–`0032E4FA`); zero and −1 are refused. `0032E590(id)`
cancels: for a request the read layer holds (states 2 and 3) it sets state 4 and lets the pump
finish it (`0032E5D4`–`0032E5DA`, `0032E603`); for one still queued it fires the cancel callback
and releases the slot at once (`0032E5E0`–`0032E5F4`); state 4 is left alone; and for kind `0xFF`
it frees the path the index pointed at (`0032E5B9`–`0032E5CB`, `003697F0`). Callers: `00280140`,
`00291D90`, `002CEB40`, `002E60F0`, `002FC3C0`, `002FCF00` and the `003B1310`–`003B21E0` family.

## 3. Key addresses

| Address | Name | Size | Role |
|---|---|---|---|
| `022C31C0` | — | 64 × `0x80` | the request slots |
| `022C51C0` / `022C51C8` | — | 8 / 8 | pending list head / tail |
| `022C51D0` | — | 8 | free list head |
| `022C51D8` / `022C51DC` | — | 4 / 4 | last selector / index recorded by the builder |
| `01EED498` | — | 4 | the request counter |
| `0215EFF4` | — | 4 | the read status word: −1 while a read is in flight, ≥ 0 on delivery, another negative on failure (was written here as `01F5EFF4`, −1 = error; corrected 2026-09-11, §8) |
| `0032E450` | — | 126 B | build the pool |
| `0032EA90` | — | 79 B | the resource system's initialiser |
| `0032E620` | — | 340 B | the builder |
| `0032E870` | — | 285 B | take a slot, fill it, stall while none is free |
| `0032E990` / `0032EC40` | — | 186 / 147 B | link into the pending list / return to the free list |
| `0032E070` | — | 605 B | the pump |
| `0032E040` / `0032E520` | — | 38 / 107 B | pump once per frame / drain until idle (argument 0) or only ask whether anything is outstanding (non-zero) |
| `0032E330` / `0032E370` / `0032E3B0` / `0032E2F0` | — | 59 / 62 / 58 / 50 B | the delivery, error, part and cancel callback sites |
| `0032E4D0` / `0032E590` | — | 66 / 129 B | in flight? / cancel |
| `0046E030` → `002DF780` | — | 29 / 243 B | issue a read (loose file first, then the archive) |
| `002DF6C0` | — | 192 B | issue a read of a raw path (kind `0xFF`) |
| `003EADD0` → `003EADE0` | — | 12 / 522 B | the script BGM stream's eight-state machine over the descriptor at `02B5E0E0` — served before the queue in the state-1 arm ([the music-control page](../18-Audio/the-music-control-file-and-the-bgm-stream.md) §3) |

### The `0032E070` exclusive subtree — all 15 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the pump **15 frontier functions**. Every one is already
described above — this table binds the set and gives each member one interior instruction cite
inside its declared extent (`interior_cite.py scan`; no boundary crossings).

| cluster | members | interior |
|---|---|---|
| read issue | `0046E030` (29 B — dispatcher) → `002DF780` (243 B — loose file, then archive); `002DF6C0` (192 B — kind `0xFF` raw path) | `0046E03E` / `002DF7D0` / `002DF6E1` |
| slot callbacks | `0032E370` (62 B — error callback `+0x40`, fires only when `+0x28 == −1`), `0032E3B0` (58 B — part callback `+0x50`) | `0032E392` (`call rax`) / `0032E3C2` (`call rax`) |
| read-layer tick (dormant) | `0046DD50` (251 B — four-state machine over `02CA6068`, §8), `00368F30` (62 B — pointer-table slot test), `00369050` (19 B — callback register), `0046E0E0` (7 B — status-word getter `0215EFF4`) | `0046DD54` / `00368F39` / `00369057` / `0046E0E6` |
| post-pass services | `003E9780` (297 B — starts voice cues whose bank finished loading, §8), `0036FD50` (8 B — `02AD9E00` gate byte getter) | `003E97B0` / `0036FD57` |
| save-storage machine | `003BB790` (400 B — the substate machine, gated by `0036FD50`), `003BA7B0` (402 B — handler), `003BA680` (154 B — handler), `00862600` (31 B — PC storage stub driving `02B40E10`/`02B40E14`) | `003BB7B2` / `003BA7B4` / `003BA684` / `00862610` |

The subtree's shape matches the page's own account: the pump issues reads, runs the slot
callbacks, ticks the dormant read layer, and services two post-pass machines — the voice-bank
starter and the save-storage queue.

### The `0022B6E0` exclusive subtree — all 11 members bound (SWE2-FRONTIER, followup queue; census corrected 9 → 11 on `AUDITSPEC-REQ-FRONTIER-22B6E0-MISSED-PAIR`)

The exclusive-callee census assigns boot frame mode 0 **11 frontier functions**. Every member
body was disassembled from the shipping image within its declared extent (2026-09-14). The
root's frame reads: `GraphicsSync_WaitBackendState100ClearAndResetSharedState`, the
stage-gated input rebuild `00249C30`, misc services and the MT tick, widget pass `00252A20`,
the `02EBA3F8` shared-command-state drain spin (`0022B720`, the handshake page's cite),
widget pass `00250730`, then `0032E520(1)` — and only when the queue is idle **and**
`0209273C == 5`, the advance block: `02064AD3 = 1`, input-channel ops, `00236A40`'s mode-flag
set + `002376F0`/`00237CA0` pair, the `00253A10` lazy-build fan-out,
`SaveRuntime_ResetActiveImageAndRebindState` (`0022B78B`, the bazaar page's cite), the
`003318C0` mode-dependent message dispatch, `0037CB30`'s flag clears; finally
`GraphicsSync_ClearSharedCommandStateBits`, the pump `0032E040`,
`InputControl_SetOneShotFrameCallback(0022BFD0)`, return 1.

| cluster | members | role | interior |
|---|---|---|---|
| boot frame | `0022B6E0` (255 B) | mode-0 frame: graphics wait, two widget passes, drain spin, idle + `0209273C == 5` advance block, pump | `0022B74E` (`mov byte [02064AD3], 1` — the advance flag) |
| stage gate | `00249C30` (39 B) | runs `0035FF90` + `InputGameplay_RebuildFrameSnapshotFromChannelHistory` only while `0209273C ∈ {2, 4}` (`add eax,-2; test eax,~2`) | `00249C44` (`call 0035FF90`) |
| widget pass B | `00250730` (130 B) | `edi = 2/[01DFE0B4]` frame step (forced to 1 in stages 2/4), `0208F570 += eax`, `002481A0`/`00248030`/`00248190` on root `0208EA28`, `00244970` recursive completion on both roots (`0208EA28`, `0208EA40`), tail `00367200(edi)` | `00250763` (`add [0208F570], eax` — the accumulate) |
| widget pass A | `00252A20` (71 B) | `2/[01DFE0B4]` → `0208F574 += eax`, `0039BDA0`/`00365990`/`0024A710(1)`, then `002450B0` on both roots | `00252A31` (`add [0208F574], eax`) |
| advance fan-out | `00253A10` (28 B) | the four lazy widget builds + refresh, in call order `0035C0D0` → `003CA2F0` → `0035DC60` → `003C8A20` | `00253A19` (`call 003CA2F0`) |
| lazy builds | `0035C0D0` (46 B), `0035DC60` (46 B), `003C8A20` (46 B) | create-once through the `00244F50` factory: `022C83E0` (`0xF8`/proc `0035C160`), `022C83A8` (`0xD0`/proc `0035DAF0`), `02B47730` (`0xD8`/proc `003C8B70`) | `0035C0ED` / `0035DC7D` / `003C8A3D` (`call 00244F50` each) |
| flag clears | `0037CB30` (15 B) | `02EBF3DC = 02EBF3DD = 0` in the advance block | `0037CB37` (`mov byte [02EBF3DC], 0`) |
| advance-block pair | `00236A40` (28 B), `003318C0` (89 B) | `00236A40` sets `02089300 = 1`, runs `002376F0`, tails `00237CA0` — the mode-flag + refresh pair called at `0022B77C`; `003318C0` dispatches on `00408B90()` — 0 → `00314440(0xC,0,0,0)`, 2 → `00408B20` → `0016D6A0`, else `00408B60` → `00314440(code,0,0,0)` — called at `0022B790` between the save reset and the flag clears | `00236A44` (`mov dword [02089300], 1`) / `003318C4` (`call 00408B90`) |
| widget refresh | `003CA2F0` (17 B) | `00246AC0([02B47758])` when non-null | `003CA2FA` (`jne 00246AC0`) |

### The `00280140` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`00280140` (924 B) is the async-request state machine §2's free path names as a
caller: a four-case dispatcher on `dword[rdx]` — case `1` (register: `(+0x10 &
0x7FFF)` in {2, 6, 0xB, 0x10} selects `+0xC8` mode 1 or 2, `6` additionally gated
on `dword[02092744] == 0`, then parks the record at `[0209AC30] + 0x3F8` and posts
`003667B0(1)`/`00365980`), case `2` (run: sub-state `byte[+0xC0+8]` 1 → the
settled-check chain `00251D50`/`003CA0F0`/three null gates → `00245020`,
2 → `0032E4D0` + save-header check `00255260`/`002EF650` rewriting flag bits
8/9/10), case `4` is a bare `return 0`, case `0x11` (the post-load battery: `003667B0(0)`,
mode register via `00254440`/`00254480`, bit-9/bit-8 work through `00268320`,
`0020E5A0`, `002EF2B0`, `0020E4E0`, `00267C90`, `00360D50`, `002EFD20`,
`002EFA70`, `002CFD10`, `00314440`, `003603E0`), default → tail `005C5230`.
The exclusive census assigns it **5 frontier functions**.

| member | role | interior |
| --- | --- | --- |
| `0024AB30` (42 B) | the end-of-arm assert — when `dword[02091094] != 0`, `0037B330()` must not be 4, else `0016D6A0(0x80000)` | [`0024AB3D`](../_index/ADDRESS-INDEX.md) |
| `00254480` (42 B) | mode-2 register — stores `ecx` → `02092744` (the case-2 gate cell `0024AB30` reads), `edx & ~0x80` → `020927EC`, and `[01E0C320]` or 0 (by `dl` bit 7) → `020CC320` | [`0025448F`](../_index/ADDRESS-INDEX.md) |
| `00360D50` (11 B) | pending marker — `dword[022CBA60] = 1` | — |
| `003667B0` (42 B) | bit-7 toggle — `word[022CBE1A] &= ~0x80`, then `|= 0x80` when `ecx != 0` — the request-in-flight bit the case arms bracket | [`003667CF`](../_index/ADDRESS-INDEX.md) |
| `003CA0F0` (75 B) | the load-settled predicate — state `[02B47748]` 0 → `dword[02B47750] == 0`; 5 → `[02B47750] == 0 && 0032F6E0(3) == 0`; else false | [`003CA11E`](../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `005C5230` (default arm),
`0024AB60`, `00365980`, `00254440`, `00268320`, `0020E5A0`, `002EF2B0`,
`0020E4E0`, `00267C90`, `002EFD20`, `002EFA70`, `002CFD10`, `00314440`,
`003603E0`, `00251E80`, `00252D90`, `00251D50`, `0032E4D0`, `00254CB0`,
`002EF640`, `00255260`, `002EF650`, `00233C10`, `00245020`, `0037B330`,
`0016D6A0`, `0032F6E0`.

## 4. Data structures and formulas

```
ResourceRequestSlot (0x80 B, 64 at 022C31C0)
  +0x00 u64  counterAccum      +0x08 u64 counterStamp (0035E810)
  +0x10 ptr  next              +0x18 ptr prev          (BOTH pending and free lists)
  +0x20 u8   state             1 queued, 2 issued, 3 waiting, 4 cancelled, 5 part delivered, 6 failed
  +0x21 u8   kind              resource kind; 0xFF = index is a path pointer
  +0x22 u8   chunked           +0x23 u8 partVerdict (2 re-probes; 3 is not a release)
  +0x24 i32  indexOrPath32     path-array position, or SIGN-EXTENDED to a pointer for kind 0xFF
  +0x28 i32  bytesThisPart     +0x2C i32 fileOffset (TRUNCATED toward zero to 0x800)
  +0x30 i32  partCap 0x80000   +0x34 i32 remaining
  +0x38 ptr  dest              (advanced per part)     +0x70 ptr dest0
  +0x40 ptr  onDone(arg, dest0, ok)   +0x48 ptr onCancel(arg)   +0x50 ptr onPart(slot)
  +0x5C i32  zero              +0x60 i32 arg (descriptor +8)     +0x64 i32 requestId = (counter << 6) | slot
RequestDescriptor (0x28 B, the caller's)
  +0x00 i32 fileOffset   +0x04 i32 (set to 0x80000 by the builder)   +0x08 i32 arg
  +0x10 ptr onDone       +0x18 ptr onCancel    +0x20 storage not consumed by 0032E870
requestId = ((counter++) << 6) | slotIndex; counter wraps to 1 past 0xFFFFFF
```

## 5. Call chain

```
requester -> 0032E400(kind, index) [size] -> 0032E620(kind, index, dest, bytes, &desc)
          -> 0032E870 -> [stall: 0032E070 / 0046DFE0 / 0035EA30 while 022C51D0 == 0] -> 0032E990
frame     -> 0022A770 / 0022AF50 / 0022B000 -> 0032E040 -> 0032E070
             state 1 -> 0046E030 -> 002DF780 -> loose file (001D6F20 ..) or archive (001D6D90)
             state 5 -> 0032E330 -> desc.onDone(arg, dest0, 1) ; state 6 -> 0032E370 -> onDone(arg, dest0, 0)
             every pass -> 0046DD50, 003E9780
boot      -> 0022B6E0 / 0022B7E0 -> 0032E040 once a frame; advance when 0032E520(1) == 0 (idle)
drain     -> 0024AC30, 002628B0, 003145E0 .. -> 0032E520(0) until the pending list is empty
```

## 6. Modding notes

- **The stall is the trap.** A sixty-fifth outstanding request blocks the requester's thread inside
  `0032E870` until the pump frees a slot; a mod that issues many small requests in one frame pays
  for it there.
- **`kind 0xFF` loads a path directly** — `+0x24` stores 32 bits that are sign-extended at issue/free, not a full-width `char*`; cancellation frees through `0032E590` — so a raw-path
  read can be queued without a path-array entry; the size still has to be supplied.
- **The delivery callback's first argument is your descriptor word**, not the buffer; read the
  bytes at `dest0`.

## 7. What is not known

- [x] ~~The read layer's eight states (`003EADE0`)~~ — `003EADE0` is the script BGM stream's machine,
      read 2026-09-11 ([the music-control page](../18-Audio/the-music-control-file-and-the-bgm-stream.md) §3);
      ~~still open: the four-state tick (`0046DD50`), and what the status word holds on success.~~
      **ANSWERED 2026-09-11** — §8: the tick is dormant, the word is `0215EFF4` and −1 means in
      flight. `FZ-14`.
- [x] ~~Which frame function each of the three per-frame drivers belongs to, and why boot pumps
      through `0032E520` from two places.~~ **ANSWERED 2026-09-12 (FABLE)**, §2.3: the
      once-per-frame pump is called from all seven main-loop mode bodies, boot, a script native and
      `00379E30`; the boot modes call the *asking* form `0032E520(1)`, not the draining form, and
      there are two because there are two boot stages.
- [x] ~~What `003E9780` and `003BB790` do after each pass.~~ **Read 2026-09-11**, §8: `003E9780`
      starts sounds whose bank has finished loading; `003BB790` is a substate machine of its own
      (`FZ-18`). The sound-bank slot family it walks is `FZ-19`.
- [x] ~~Whether any requester uses the head-insert form of `0032E990` — `0032E620` and its fallback
      both pass 1.~~ **ANSWERED 2026-09-12 (FABLE): yes, one.** `0032E990`'s only caller in the graph is
  the requester `0032E870`, which forwards its own stack argument (`[rsp+0x68]`, `0032E8C5`); of
  its three callers, `0032E620` passes 1 at both sites (`0032E6B9`, `0032E742`) and the
  string-keyed `0032E7C0` passes 1 (`0032E836`), but **`0032E780` passes 0** (`0032E795`) — the
  head insert — and is reached twice from `003EADE0`, the script BGM stream's eight-state machine
  (§3; `003EAE4C`, `003EAF9A`). So the BGM stream's reads jump the pending queue.

> **`EO-3` — the static mechanism behind the `001D6E20` crashes, found 2026-09-14 (FABLE).** *The hypothesis was a
> 64-bit pointer round-tripped through a 32-bit field. That round trip exists, in this queue, on the raw-path (kind
> `0xFF`) route. Its three live crashes are not re-observed here, so the link to them is the address shape and the site.*
> 1. **The pointer is truncated when the request is built.** The string-keyed requester `0032E7C0` (reached through the
>    thunk `0032E7B0`) copies the path into a fresh heap block from the engine allocator `0036A190` (`0032E80E`–`0032E82C`),
>    then enqueues with **`mov edx, edi`**, the block's 64-bit address cut to 32 bits, and kind `0xFF`
>    (`0032E846`–`0032E84D`). `0032E870` stores that dword as the request's `+0x24` (`0032E902`).
>
> > **Where to stand to watch this happen — added 2026-09-21 (FABLE, on
> > `ASTRA-RETURN-FABLE-EO3-OBSERVATION-BOUNDARY`).** The two ends of that range are not two views of
> > one thing; **they answer different questions, and a trace needs both.**
> >
> > | site | instruction | what is readable there |
> > |---|---|---|
> > | `0032E846` | `mov edx, edi` | **before** the truncation — `rdi` holds the whole 64-bit block address and `edx` has not yet been written |
> > | `0032E84D` | `call 0032E870` | **after** both argument instructions — `rdi` **still** holds the whole address, `edx` holds the surviving low half and `ecx` the kind `0xFF` |
> >
> > **Corrected 2026-09-21 (FABLE) on `ASTRA-CONTRA-FABLE-EO3-RDI-REMAINS-AT-CALL`. One stop is
> > enough, and the earlier claim that `0032E846` is *the only place the original pointer exists* was
> > wrong.** `mov edx, edi` does not write `rdi`, so a single breakpoint at `0032E84D` holds
> > `rdi = P` and `edx = zero_extend(low32(P))` **in one context**, which is exactly the comparison
> > the open question needs. ASTRA raised this; the reading is theirs and it is right.
> >
> > *What that argument does not cover, and this page now does.* `rdi` is loaded at `0032E816`
> > (`mov rdi, rax`, the allocator's return) and the interval down to the call is not two
> > instructions — it contains the copy loop and **a call, `0032E82E`**. "Neither argument
> > instruction writes `rdi`" is therefore not sufficient on its own, and neither is the Win64
> > non-volatile convention, which is a claim about a callee's manners rather than about this
> > callee. So the callee was read: `0036C140`, the shared allocator-support helper this page's
> > neighbours already document (`Runtime.MemoryAllocatorSupport`), is 84 bytes and writes only
> > ~~`eax`~~ `rax` / `eax`, `rcx`, `rdx` and five globals — it **never touches `rdi`**. The survival of `P` in
> > `rdi` at `0032E84D` is established by reading that body, not assumed from the ABI.
> > *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-EO3-CALLEE-WIDTH`:
> > - `0036C17C mov rax, qword ptr [rdx + rcx*8 + 8]` writes the full `rax`, and the other writes are `eax`;
> > - the helper returns only when its depth counter is positive, and otherwise spins at `0036C150`. The `rdi`
> >   argument therefore holds on the path that arrives at `0032E84D`, which is not proof that the caller ran.
> >
> > The `rdi` conclusion is unchanged.)*
> >
> > What the earlier note got right and this correction does not disturb: a breakpoint at
> > `0032E846` **fires before that instruction executes**, so an observer placed there expecting the
> > truncated value reads a register that has not been written yet; and *a hit on a call instruction
> > does not show the call completed*.
> >
> > **The same care inside the builder.** `0032E897 mov ebp, edx` preserves the incoming index, and
> > `0032E902` stores **`ebp`**, not the then-live `edx`; `0032E906` restores `rbp` from
> > `[rsp+0x48]` on the very next instruction, so `ebp` carries the index across exactly those two.
> > A stop **at** the store is still before its effect, and the record is complete only at the
> > epilogue boundary `0032E983` — where the actual request ID should be matched, rather than
> > treating an early slot as a finished record.
> >
> > *Nothing live has run.* Whether the allocator supplies a high half at all is the question these
> > sites exist to ask, and it is open.
> >
> > *Disposed 2026-09-26: register row EO-3 is SUPERSEDED under the runtime rule (FABLE), because the round trip
> > is tier-1 static. The live observation is prepared in `_index/_inbox/ASTRA-QUEUE.md`
> > (`ASTRA-RETURN-FRONTIER-EO3-STATE-AND-OBSERVER`) and is not needed for the static claim. Marked 2026-09-30,
> > SWE2-CONTRACT.*
> 2. **It is sign-extended when the request is issued.** The pass `0032E070` handles kind `0xFF` with
>    **`movsxd rcx, dword ptr [rbx + 0x24]`** and hands the result to `002DF6C0` as the path (`0032E105`–`0032E111`).
> 3. **The first byte of the path is read at `001D6E20`.** When the loose-file checks fail (`0017D930` is 0 unless the
>    loose-file byte `+0x88` is set; then `001D6EF0` and `001D6B40`, `002DF6E1`–`002DF6FD`), `002DF6C0` passes the path
>    straight to `001D6D90` (`002DF75F`–`002DF777`). That function touches the string for the first time in its copy loop,
>    `001D6E20 movzx ecx, byte ptr [rbx]`. So in a normal install the crash lands exactly there.
>
> **So when the surviving low dword has bit 31 set, the pass reads `0xFFFFFFFF` followed by that low half:
> exactly the `0xFFFFFFFF8BC1x000` values `EO-3` recorded.**
>
> > **Corrected 2026-09-21 (ASTRA, `FABLE-REQ-ASTRA-EO3-PATH-POINTER`; consumed by FABLE).** This sentence used to
> > read *"whenever the allocator returns a block at or above `0x80000000`"*, which makes the roundtrip a property
> > of the **64-bit magnitude**. It is not. `mov edx, edi` **always** discards the high half, whatever the address
> > was; the `movsxd` that follows then depends on **bit 31 of the surviving low dword alone**. A block at
> > `0x1_8000_0000` sign-fills exactly like one at `0x8000_0000`, and a block at `0x2_0000_0000` — far above 2 GB
> > — does not sign-fill at all, because its low dword is zero.
> >
> > ***And that costs this note a causal claim it was quietly making.*** Because many distinct originals collapse
> > onto the same post-roundtrip value, **the recorded `0xFFFFFFFF8BC1x000` addresses do not identify the pointer
> > that produced them**, and therefore do not by themselves establish that the arena sat above 2 GB. They are
> > consistent with that and with other originals sharing the same low half. *A fault-shaped address is not a
> > causal chain* — ASTRA's wording, and it is the right bar here. The
> image itself loads at `0x120000` (PE `ImageBase`), so pointers into the image stay safe; only heap copies are exposed.
> - **Who uses the route:** the ATEL sibling loader `003306E0` (10 call sites), `003319D0` (4) and the map `.efb` loader
>   `00377DC0` (2).
> - **Not established:** why the arena behind `0036A190` (`022D89BC`) sometimes sits above 2 GB, and whether the page
>   alignment of the three crash values is the allocator's. *(2026-09-30, SWE2-CONTRACT for OPUS, DD batch 13: the first
>   half is answered by the 2026-09-20 trace just below, a boot-time CRT `malloc` in a large-address-aware process.
>   The second is runtime-only: the 2026-09-21 correction above shows the recorded values do not identify the block,
>   and the live remainder is `FABLE-REQ-ASTRA-EO3-PATH-POINTER`.)* The `004096C0` sign extension (`RS-2` on
>   [section addressing](resource-section-addressing.md)) is a separate instance of the same defect class, not this site.

> - *TRACED 2026-09-20 (FABLE, Claude Opus 5), static, and it closes this item.* **The creating `malloc`
>   site is `0022A1E1`**, in the boot hub `0022A0B0`. That function allocates each arena through the 14-byte
>   wrapper **`0036D240`** — `movsxd rcx, ecx ; xor edx, edx ; or r8d, -1 ; jmp malloc` — and stores the
>   returned pointers in `01FD49F8`, `01FD4A00`, `01FD4A08`, `01FD49F0`, `01FD4A10`, `01FD4A30` and more, then
>   registers each one with **`00369D30(index, pointer, size, handleSlotCount)`** (`0022A2AE`, `0022A2CB`, `0022A2E7`,
>   `0022A304`, `0022A321`, …).
>
>   **`00369D30` is the heap registrar, and it writes the table this page already names.** It fills the
>   **168-byte** descriptor at `022D7FD0 + index × 0xA8` (`00369E02` `imul rbx, rsi, 0xa8`, `00369E1C`
>   `lea rax, [022D7FD0]`) — the 168-byte heap descriptors of the paragraph above — and **on the first
>   registration only** (`dword[022D89B8]` still zero) it stores that index into **`022D89BC`**
>   (`00369D73`). *That is why `[022D89BC]` is the heap id this queue uses: it is simply the first heap
>   registered at boot.*
>
>   **Which heap, concretely.** The first call is `0022A2AE` with `ecx = 2`, pointer `[01FD49F8]`, size
>   `0x1DC0000` and fourth argument `0x10`; its block is the `malloc` of `0x1DC0010` bytes at `0022A1E1` —
>   about **31 MB**, requested sixteen bytes over the registered size.
>
>   **The fourth argument is a handle-slot count, not an alignment — corrected the same day, and the mistake was
>   mine.** I first wrote "alignment" here without grepping for prior art on it; `00369D30` settles it against
>   me: `00369EB7` does `mov rax, rbp ; shl rax, 4`, laying `count × 16` bytes of handle records after the
>   block's base, while the alignment is a separate `and r10, ~0x3F` — **64 bytes, and the registrar does it
>   itself**. That is exactly the reading
>   [what the engine fixes at boot](../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md) already carried
>   from `ASTRA-CONTRA-FABLE-ARENA-SLOT-COUNT` on 2026-09-12. **So the `+0x10` / `+0x100` / `+0x400` tail on each
>   `malloc` is not alignment slack, and what it serves stays open on that page** — this trace gives the call
>   site, not the answer to that.
>
>   **And the subsystem names itself.** The registrar's diagnostic format string is
>   `TKMALLOC EXECSPACE=%02d/START ADRS=%p` (`00D10F20`, loaded at `00369E2A`), so these arenas are
>   **TKMALLOC "exec spaces"**, numbered by the same index.
>
>   **So the above-2-GB observation needs no further explanation:** the arena is a ~31 MB CRT `malloc` taken at
>   boot in a large-address-aware, non-ASLR process, exactly as the narrowing below predicted — now with the
>   call site rather than by elimination.
>
> - *Narrowed 2026-09-18 (FABLE), static:* the arena is CRT heap and nothing places it. The block chain is `0036A190` → `0036A1A0` (heap id `[022D89BC]`, block from `0036BC60` or `0036BFE0`, header stamped with an encoded address at `0036A209`) over the 168-byte heap descriptors at `022D7FD0`; the image imports no `VirtualAlloc`, `HeapAlloc` or `MapViewOfFile`, only `malloc` (37 sites), `_aligned_malloc` (3) and `calloc` (1), and it is large-address-aware without `DYNAMIC_BASE` (DllCharacteristics `0x8120`, base `0x120000`). So where a CRT block lands is the runtime's and the OS's choice, and a large-address-aware process may receive it above 2 GiB; the engine asks for no placement and checks none, which is why the sign extension bites. Which `malloc` call creates the arena buffer was not traced *(traced 2026-09-20 in the item above: `0022A1E1` in the boot hub `0022A0B0`; marked 2026-09-30, DD batch 13)*: the nineteen heap-family functions reach none of the five `malloc` wrappers within two hops, and three of the wrappers (`0020D7B0`, `006CB810`, `006DA8D0`) are address-taken. The `0xFFFFFFFF8BC1x000` values are the low half of a 2..4 GiB block, as the reading above says.

## 7b. What bounds the four items outside SECTION-02, 2026-09-30 (SWE2-CONTRACT for OPUS)

DD batch 13 (`OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`). The status line said the four items "remain separately
bounded" without naming the bounds. They are named here, and the path copy's lifetime is read. The checks are
`_index/candidates/swe2contract-ddres-b13-0930/b13_checks.py` Q1–Q2 (FAILS 0).

| item | bounded by | what is left |
|---|---|---|
| deeper services | §8 here (the read layer `FZ-14`, the dormant tick `0046DD50`, the voice slots `FZ-19`, the storage machine `FZ-18`); the storage machine's handlers on the save pages; OV-19 ([the external-source owner](the-external-source-owner-and-borrowed-view-lifetime.md)) and OV-33 ([the indexed-source request](the-indexed-source-request-from-arm-to-terminal-pump.md)), both PARTLY ANSWERED; the SECTION-02 review Q4, which keeps the footer services as scripted boundaries | actual service issuance, status production and loading-state timing, runtime-only (OV-19 / OV-33, carried by `FABLE-REQ-ASTRA-RT-REMAINDERS-0929`); two storage handlers, proposed row P8 |
| live scheduling | the SECTION-02 review Q3 (*live elapsed time and actual scheduler/concurrency behavior remain unresolved by these fixtures*); §1 here (no duration measured) | runtime-only, the same RT remainder |
| path / callback lifetime | the path pointer's round trip: EO-3, SUPERSEDED 2026-09-26 (tier-1 static; live remainder `FABLE-REQ-ASTRA-EO3-PATH-POINTER`). The copy's frees: the paragraph below. The part callback: none is installed (DD batch 6 Z2, §2.4). The delivery callbacks: OV-36, ANSWERED (a slot delivers at most once) | whether a raw-path id is ever cancelled twice, proposed row P9 |
| complete authored reachability | the part callback and results 2 / 3: unreachable in the shipped build (DD batch 6 Z2); the chunk gate: `003EB0D0`, the script BGM stream's descriptor ([the music-control page](../18-Audio/the-music-control-file-and-the-bgm-stream.md) §3); the six asking-form callers (DD batch 6 A0–A6) | which requests run while a stream is active, and so are chunked, runtime-only |

**The path copy is freed once on every single-call path, and twice on a repeated cancel.** The raw-path requester
copies the path into a heap block and keeps its address, cut to 32 bits, at `+0x24`. Three helpers free that block for a
kind-`0xFF` request: the done helper `0032E330` (`0032E360`), the error helper `0032E370` (`0032E3A3`) and the cancel
`0032E590` (`0032E5CB`). They are the only frees in the slot code. The pump's state-4 completion
(`0032E170`–`0032E197`) calls the cancel callback and releases the slot without freeing, so a request cancelled while the
read layer holds it is freed once, by the cancel. **The cancel frees before it tests the state** (`0032E5B9`–`0032E5D0`),
and a request already in state 4 returns at `0032E5DE` after that free. So a second cancel of the same in-flight id frees
the block again, because `+0x24` is never cleared. None of the three raw-path users (`003306E0`, `003319D0`, `00377DC0`) calls the cancel directly.
Whether an id reaches it twice through memory is proposed row P9. In player terms this is a latent double free on a
loading path the shipped callers do not take directly.
*Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15, §7c P9):* no id of a raw-path request reaches the cancel even once, because every raw-path
caller discards the id.

**Proposed register rows, id-less, for SWE2-DATA (SWE2-CONTRACT for OPUS):**

| # | question |
|---|---|
| P8 | What the save-storage machine's handlers `003BA5F0` and `003BA720` do, and which of `003BB790`'s ten substates reaches each of its seven handlers |
| P9 | Can a kind-`0xFF` request id be cancelled twice while in state 4, so that `0032E590` frees its path copy a second time (`0032E5CB`, before the state test at `0032E5D0`)? Its direct callers are `002FC3C0`, `003B1310`, `003B1710` and `003B18E0`; the raw-path users are `003306E0`, `003319D0` and `00377DC0` |

*Answered 2026-09-30 in §7c (SWE2-CONTRACT for OPUS, DD batch 15): P8–P9 need no register row.*

## 7c. Rows P8–P9 answered statically, 2026-09-30 (SWE2-CONTRACT for OPUS)

DD batch 15 (`OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`). Every item below is pinned by
`_index/candidates/swe2contract-ddres-b15-0930/b15_checks.py` (checks S and C, FAILS 0) on the certified image. Neither needs a register row.

- **P8. The storage machine runs on a command word.** `003BB790` dispatches on `02B40E1C`, values 0–9, not on the
  substate `02B40E14`: 0 → `003BAC90`, 1 → `003BA7B0`, 2 → `003BAEB0`, 6 → `003BA990`, 7 → `003BA5F0`, 8 →
  `003BA720` and 9 → `003BA680`. Commands 3, 4 and 5 have no handler and set the machine idle. `02B40E14` is each
  handler's own step counter, and `02B40E18` is the result class (4, 7 or 9). Ten functions store the command, one
  value each (5, 7, 9, 3, 4, 1, 6, 8, and 2 twice); none stores 0, so command 0 is the word's initial zero.
  - **`003BA5F0` (command 7) deletes a file.** Step 0 goes to step 1. Step 1 calls `00862130(port, name)`, which runs
    `_wfopen_s(path, "rb")` and, if that opens, `fclose` and then `_wremove`, and goes to step 12. At step 12 a result
    of 0 or −4 ends cleanly and anything else is result class 9. Its issuer `003BB2F0` serves queue packet kind
    `0xB`, which [the manual-save page](../19-Save-Load-Settings/how-a-manual-save-is-committed.md) reads as *delete
    the file if it exists*.
  - **`003BA720` (command 8) checks that a slot's save fits.** In one pass it asks `003BA3E0` for the named file's
    block count (sizes rounded up to 1 KiB), compares it with the free-block word `02B4054C`, and on a fit subtracts
    it and marks the slot's record (the high dword of `02B407C0[slot]`) 1, else 0. Its issuer `003BB6A0` takes slots
    0–199 from queue packet kind 6, which `0057F280` queues for one slot's data file at a time as it walks slots
    0–199.

  In player terms: command 7 is how a save slot's old file is removed, and command 8 is how the save list learns
  which slots have room.
- **P9. No. Shipped code cannot cancel a raw-path request at all.** All sixteen call sites of the raw-path entry
  `0032E7B0` (in `003306E0`, `003319D0` and `00377DC0`) discard the returned id on every path. This is a register-flow
  check; as a control, the same flow finds `0032E620`'s use of the id. The id counter `01EED498` is read only by the
  builder `0032E870`, and the slot table only by the slot module. The cancel's four callers pass ids from their own
  objects' `+0x18`. So no kind-`0xFF` id ever reaches `0032E590`, and the double free above is latent in the API only.
  *Limit:* 36 of `0032E620`'s callers compute their kind. A computed kind of `0xFF` through that entry would put a file
  id, not a heap copy, at `+0x24` (`0032E902`), which is a different defect and is not modelled here. In player terms:
  no loading path in the game can trigger it, but a mod that keeps a raw-path id and cancels it twice could.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the pool, the lists and the counter | `0032E450`–`0032E4CD`; `0032E990`–`0032EA4A`; `0032EC40`–`0032ECC5` | 1 |
| the builder's fields and the chunking | `0032E634`–`0032E75E`; `0032E870`–`0032E97C` | 1 |
| the stall | `0032E88D`–`0032E8C3` | 1 |
| the six states and their transitions | the table at `0032E2D0`; `0032E0BD`–`0032E2C2` | 1 |
| the callback sites and their arguments | `0032E330`–`0032E36A`; `0032E370`–`0032E3AD`; `0032E3B0`–`0032E3E9`; `0032E2F0`–`0032E321` | 1 |
| the twelve setters store the descriptor word | `00238364`; `003844B9` (`+8 = r9d`); `0032E961` (`+0x60`); `0032E34C`; `002383C6`–`002383DA` | 1 |
| in flight and cancel | `0032E4D0`–`0032E511`; `0032E590`–`0032E610` | 1 |
| the per-frame drivers and the boot loop | `0032E040`–`0032E065`; `0032E520`–`0032E58B` and their callers | 1 (graph + bodies) |

## 9. Related

- [`file-size-tables-fst.md`](Loose-Files-And-Size-Tables/file-size-tables-fst.md) — where the bytes count comes from.
- [`area-nmb-index.md`](VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md) — the path arrays `(kind, index)` select from.
- [`how-the-bigfile-index-loads-and-is-verified.md`](VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md) — the archive read the issue falls through to.
- [`authored-data-table-registry.md`](authored-data-table-registry.md) — the twelve board requests and their completion words.
- [`how-the-music-changes-when-you-change-area.md`](../18-Audio/how-the-music-changes-when-you-change-area.md) — the music table's request goes through this builder (DG-4).
- [`the-music-control-file-and-the-bgm-stream.md`](../18-Audio/the-music-control-file-and-the-bgm-stream.md) — the whole-file loader `0051ED10` that uses the `+8` word as its callback, and the BGM stream this pump ticks.
## 8. The read layer, closed — 2026-09-11 (`FZ-14`)

**The status word is `0215EFF4`, and −1 means "in flight", not "error".** This page first printed
it as `01F5EFF4`; the operand at `0046DFE7` resolves to `0215EFF4`, inside the audio / file layer's
global block. The read issuer `002DF780` passes its address to whichever reader it chooses — the
loose-file open (`001D6FB0`, `002DF808`) or the archive read (`001D6D90`, `002DF838`) — and the
archive reader stores the pointer in a global (`001D6DCD`) and writes **−1** into the word when the
job is queued (`001D6DD4`), before the job's completion (its callback `001D6D70`) overwrites it.
`0046DFE0` returns 2 while the word is −1 — the pump's "leave, still waiting" — and once it changes,
`0046E0E0` returns it and the pump takes state 5 for a non-negative value and 6 for a negative one
(`0032E19C`–`0032E1A8`). What a non-negative value counts is not read here. **Read 2026-09-18 (FABLE): it is the entry's byte count.** The worker `001A07B0` dispatches a kind-2 record to `001A0CF0`, which stores into the record's `+0x10` either `0059F4A0`'s return — the size the archive lookup reports for the entry, when `0059D920` accepts it — or `−2` when it does not (`001A0D57`–`001A0D87`), issues no read for a value `≤ 0` (`001A0D95`), and otherwise reads exactly that many bytes (`001A0DB0`, the length handed to `00597970`); the completion then calls the record's `+8` callback with `+0x10` in `ecx` (`001A084F`–`001A0853`), and `001D6D70` copies it into the word. So state 5 is *bytes delivered* (a zero-length entry included) and state 6 is *rejected* (`−2`); `−1` never reaches the test, because `0046DFE0` holds the pump at 2 while it stands.

**`0046DD50` is dormant.** Its state word `02CA6068` has no writer but itself (whole-image scan):
it writes 0, 3 and 4 and copies the word back — never 1 or 2 — and state 0 returns at once
(`0046DD72`–`0046DD75`), so states 1 … 4 are unreachable in this build. What they would do reads as
a console media pump: state 2 rounds two sizes up to `0x800` (`0046DDE6`–`0046DE11`, the 2 KB
sector), states 3 and 4 wait on `InputDevice_QueryAvailabilityState_Always1` (`0053DD10`, a PC stub
that returns 1) and on `00368F30(0)`, which tests a slot of a pointer table at `02CD7F70`, and state
3 registers a callback through `00369050(0, 00536F30)`. The machine is the shape of a disc-read
state pump left in place with its trigger removed.

**`003E9780` starts voice cues whose bank has finished loading** — the 64 blocks are the **voice-pack
slots** of the `voice*` script verbs ([the voice page](../18-Audio/the-voice-pack-slots-and-the-voice-verbs.md), 2026-09-11). It walks **64 blocks of `0x40` bytes at
`02B5D0B0`** (`+4` a state byte, 3 = loaded; `+0x20` / `+0x28` two entry tables, one selected per
pass by `002DEBB0` — bit 10 of the word at `[020BE6E0] + 4` — and copied to `+0x30`); each table
holds `+4` entries of 16 bytes: `+8` flags (bit 31 = pending), `+0xB` and `+0xF` two parameters,
`+0x10` an id, `+0x14` a load handle. For a pending entry whose handle has completed
(`002DEE90`) and while the mode byte `02064AD3` is 2 (`00229EA0`), it calls `002DF680(id, +0xF,
+0xB & 0x7F)` — the same sound-layer start the BGM stream uses — clears the pending bit and the
handle, and writes −1 to the slot's `+0x08` word (`003E981F`–`003E9844`; first written here as `−0x28`, corrected 2026-09-11); an entry without a handle is
re-asked through `003E9A10` and dropped when that says no. Twenty functions between `003E98B0` and
`003EA5C0` own the blocks (loader `003E98B0` frees the two tables through `003697F0` and resets the
state); the kinds are 8 and 37 — the `.vpc` / `.vpcjp` voice packs — and the slots are the voice page's (`FZ-19`, answered).

**`003BB790` is a machine of its own, gated by the byte at `02AD9E00` (`0036FD50`; corrected 2026-09-13 from
`02ADA000`).** Its word `02B40E10` and substate `02B40E14` are driven by `00862600(0, &result)`, a **PC stub** that
returns 1 and copies the global `02EAF8E0` into `result` (corrected from `02EB38E0`); the result code is classified (`−19` … `−11` and a
mask over `−79` … `−40` ~~→ substate 4; `−5` → substate 7) and dispatched over substates 0 … 9 to~~ → result class 4 at `02B40E18`; `−5` → class 7),
and the command word `02B40E1C`, values 0 … 9, is dispatched to *(Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15): the classes are stored at `02B40E18`, and the dispatch
reads `02B40E1C`, not the substate `02B40E14`; §7c P8)*
seven handlers (`003BA7B0`, `003BA990`, `003BAEB0`, `003BAC90`, `003BA5F0`, `003BA720`, `003BA680`,
135 – 803 B) that carry no strings. What it services is `FZ-18` — *answered 2026-09-13:* `003BB790` is the **save-storage command machine**. Its seven handlers call a small PC storage layer at `00862xxx` that keeps a result word at `02EAF8E0` and ~~a file handle~~ **an opaque open-file record** at `02EAF8E8` and is built on the CRT file calls (`008621E0` formats a wide path and opens, seeks, tells and closes through the `008C2Exx` imports; ~~`008625D0` closes the handle;~~ *corrected 2026-09-13 on `ASTRA-CONTRA-FABLE-STORAGE-SEEK`, re-read:* the record is the `0x210`-byte cursor / mode / path object `008666B0` returns after reading the file and closing the CRT stream itself (`fclose` import at `008667AD`), not a `FILE *`; **`008625D0` seeks** — for port 0 it calls `00866A80(record, offset, origin)`, which sets the cursor for origin 0 / 1 / 2 and refuses a position at or past the length, and then publishes result 0 **whatever that returned** (`008625D4`–`008625E6`); **`008620E0` releases** — `00866200(record)`, clears `02EAF8E8` and publishes 0 or −3 by the release's result, or −4 when there is no record (`008620E0`–`00862122`); `00862490` reports a fixed card type `0x2000000` and a formatted flag 1) — a re-implementation of a PS2 memory-card-style interface over files. `003BAEB0` also consults `SaveWrite_GetBusyFlag` (`00583920`). The machine runs only while the byte **`02AD9E00`** is non-zero (getter `0036FD50`; this page and the ledger had cited `02ADA000`, which nothing references). The byte is set to 1 by `0036FD80` from `SaveWrite_PrepareAndSubmitFullImage` (`0057E479`), `SaveStorageQueue_ControllerStateHandler` (`0058242C`), `00393EA0` and `00252030`, set to 0 by the same setter at `0057E591`, and cleared by `0036FD70` (boot `0022A3E3`, `00252030`, `00393EA0`, `005823ED`, the thunk `0050C980`) and `0036FD60` (via `00379D40`). What each of the ten substates does is not decoded. *(2026-09-30, DD batch 13: five of
the seven handlers are read on the save pages, `003BA7B0`, `003BA680`, `003BAC90` and `003BAEB0` on
[the storage-read contract](../19-Save-Load-Settings/CONTRACT-storage-read-completion.md) and `003BA990` on
[the manual-save page](../19-Save-Load-Settings/how-a-manual-save-is-committed.md). `003BA5F0` and `003BA720`, and the
substate-to-handler map, are proposed row P8, §7b.)* *Answered 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 15, §7c P8):* the ten values are the command word `02B40E1C`, and seven of
them have handlers; command 7 deletes a file and command 8 checks that a slot's save fits.

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| twenty stated function sizes in §3 | **20 of 20 exact** |
| **64 slots of `0x80`** at `022C31C0` | the loop is `cmp edx, 0x40` / `jl` with `lea rax, [rax + 0x80]` — **64 iterations, `0x80` stride** |
| the request counter at `01EED498` is set to **1** | `0032E453 mov dword ptr [rip…], 1` |
| the free head at `022C51D0` | `0032E4B1`, loaded with `022C31C0` — slot 0 |
| the pending head and tail at `022C51C0` / `022C51C8` cleared | `0032E4BF` / `0032E4C6` |
| the id is the counter shifted left **six** or-ed with the slot index | consistent by construction: **64 slots need exactly 6 bits**, and `2⁶ = 64` |

### The pool's end is the pending head

`022C31C0 + 64 × 0x80 = 022C51C0` — **the slot array ends on the byte the pending head begins.** The
three list pointers then fill `022C51C0`–`022C51D7` and the builder's selector/index follow at
`022C51D8`/`022C51DC`, contiguously.

That is the check that turns "64 slots of `0x80`" from a loop bound into a layout: the next named
datum lands exactly where the array stops. *(`022C51E0`–`022C51EF` is a 16-byte gap before the 256
size-override pointers at `022C51F0`; `022C51E0` itself is a qword `0032EA90` and `0032EAE0` zero.)*

### §2.1's builder fields were instruction displacements, not slot offsets

The builder's cursor does not start at a slot base:

```asm
0032E460  lea  rax, [rip + 0x1f94d71]     ; -> 022C31D8  = slot 0 + 0x18
0032E470  lea  rcx, [rax - 0x98]          ; the previous slot
0032E477  mov  dword ptr [rax + 0x40], edx
0032E47F  mov  dword ptr [rax + 0x4c], 0xffffffff
0032E486  lea  rcx, [rax + 0x68]          ; the next slot
0032E48A  mov  qword ptr [rax - 8], rcx
0032E48E  mov  word  ptr [rax + 8], r8w
0032E493  mov  dword ptr [rax + 0x10], r8d
0032E497  lea  rax, [rax + 0x80]
```

`022C31D8 − 022C31C0 = 0x18`, so every displacement above is **`0x18` short of the slot offset**. The
fields the builder actually writes are:

| slot offset | written | what |
|---|---|---|
| `+0x10` | `rax + 0x68` = slot + `0x80` | **the next slot** |
| `+0x18` | `rax − 0x98` = slot − `0x80` | **the previous slot** |
| `+0x20` | 0 (a **word**) | |
| `+0x28` | 0 (a dword) | |
| `+0x58` | the index | |
| `+0x64` | −1 | |

**The page's own text is the witness.** §2.1 goes on to say `0032EC40(slot)` *"sets `+0x64 = −1`"* —
and `0032ECC5` is `mov dword ptr [rcx + 0x64], 0xffffffff`, with the **slot base** in `rcx`. So one
paragraph names the same field `+0x4C` and `+0x64`. Independently, `0032E990` — which links a slot
into the pending list from its base — uses only the displacements **`+0x10` and `+0x18`**, exactly
the two list pointers the cursor arithmetic predicts.

This matters for reconstruction rather than for prose: a pool built from the old list would put the
index at `+0x40`, zero `+8`/`+0x10`, and so **zero the next-slot pointer** — which is the one field
the free list cannot lose.

> The general shape is worth naming: **a decompiler prints the displacement, and the displacement is
> only an offset when the register holds the base.** Here the compiler biased the cursor by `0x18` to
> keep both list pointers in signed-byte reach, and the bias silently rides into every field name.

**Not claimed:** nothing here was executed or observed live. §§2.2–2.5, the six pump states and §8's
read layer were not re-derived; the 16-byte gap before the size overrides is unexplained.

*The gap, read 2026-09-30 (SWE2-CONTRACT, DD batch 6, `_index/candidates/swe2contract-ddres-b6-0930/b6_request_queue.py` G1, M2; static):* `022C51E0`–`022C51EF` holds one
qword that the initialiser `0032EA90` (`0032EAA7`) and `0032EAE0` (called from the boot hub `0022A0B0`) set to 0.
Nothing reads it, and nothing addresses its second half. The gap is an unused cleared field, not part of the list
record or of the override table.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**The queue's pump runs in almost every frame mode.** `0032E040` is called by frame modes 0, 1, 2, 4, 5 and 6, by the
978-byte boot initialiser and by `MainLoop_UpdateAndRenderFrame`. It asks the
per-frame gate body `001EDE80`. This page names those call sites. The crossings are what those frame bodies also do:

- **Presentation — SERVICE.**
  - The field frame `0022A770` runs `MainLoop_Draw`, `RenderSystem_RunCharacterUpdatePipeline`,
    `EffectSystem_ProcessQueuedGraphicsEffectsFor…`, the graphics-sync pair and several more bodies.
  - `0022A0B0` loads the AddMotion skeleton and high-model tables.
  - The frame-mode getter `00229EA0` is read by `PresentationEntry_UpdateForCurrentGlobalPhas…` and
    `RenderModelInstanceContainer_ProcessActiveEn…`.
  - `001EDE80` is read by `CharacterRender_UpdateCombatLookAndAuxContro…`.
  - The ~~loose-file~~ open `001D6F20` *(corrected 2026-09-27, FABLE, Claude Opus 5.5: a stream open that the resolver serves from the RAM file cache or the `FFXII_TZA.vbf` archive, never a loose file - [record](../_index/candidates/pc1-config-route/README.md))* is shared with the AddMotion loaders.
- **Party — SERVICE.** The field frame, the full-menu frame and mode 5 each commit a pending party focus handle.
- **ActorEntity — CLIENT and SERVICE.**
  - The request family is issued by `ActorResource_BeginPrimaryPayloadLoad` and `ActorResource_BeginManagerResourceSetLoad`.
  - `0032E520` is issued by the 1,689-byte area unload.
  - The ATEL sibling loader `003306E0` is run by `ActorResource_BeginManagerResourceSetLoad`.
  - `BattleStorage_InitializeWorkArrays` is both a boot callee and the caller of `00238260` (`"BOARD"`).
  - The area unload `002628B0` releases manager records (`ActorSystem_ReleaseManagerRecords`).
- **Movement and CoreRuntimeScheduling — SERVICE.**
  - The frame bodies call movement helpers (67 B and 219 B).
  - `001EDE80` is read by `WorldActor_UpdateRuntimeAndScriptExecutionState`.
  - The frame and boot bodies call core bodies of 7–2,232 bytes.
  - The mode dispatcher (465 B) calls every frame body.

**The area unload `002628B0`, which this page cites, is a multi-layer teardown — SERVICE.** It calls `PartyControl_SetMovementSuppressionBit` and `PartyFocus_ClearCurrentActorIfEligible` (**Party**), six movement helpers (**Movement**), three small Audio-filed bodies (**Audio**), `CharacterRenderSystem_RefreshDistanceCullEna…` and three Presentation bodies (**Presentation**), and a 126-byte Input helper (**Input**).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `FUN_002fc3c0`, owned by that layer, calls `0032E4D0` on this page. That caller is a 183-byte dispatcher: `byte[rec+0x23] & 0xF`, bounded to 7, into an eight-entry jump table; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `0022A770` on this page calls `FUN_00316930`, owned by that layer. What it reaches is a 287-byte walk of the same `[022C2550]` table against the data at `01EED130`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `0022B6E0` on this page calls `RNG_MT19937_NextU32_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863BF0` - onto the CRT's Mersenne Twister next-u32; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI / Gameplay — SERVICE (two descents).** `00233C10` on this page calls `00327F80` (CombatAI)
and `00237DF0` (Gameplay) — the resource-queue body reaches into both layers during its work; descent,
not shared ownership. Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).

**Story_Event_Quest_Hunt — CLIENT (12 edges through one accessor).** `0032A8A0`, `0032A930`,
`0032A9A0`, `0032AA00` and eight more, owned by that layer, call `002EF2B0` —
`SaveImage_GetPersistentPayloadBase`, the persistent-flag payload accessor this page names in its
request-queue context. The story-event layer reads the same payload base when queueing its own
requests; fan-in to the shared accessor, not a queue responsibility.
- **Items_Equipment_Shops_License — SERVICE (1 edge).** 1 outbound (page-cited `00233C10` call Items_Equipment_Shops_License bodies `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0)). Substantive edges include `00233C10` calls `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (0030B6A0).
- **Script_VM_Native_Bridge — CLIENT and SERVICE (62 edges).** 61 inbound (Script_VM_Native_Bridge bodies `0050D9A0`, `00354D00`, `0050F0A0` call page-cited `InputDevice_QueryAvailabilityState_Always1` (0053DD10), `008620C0`, `002EFA70`); 1 outbound (page-cited `0050D9A0` call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10)). Substantive edges include `00254CB0` is called by `0050F0A0`; `00254CB0` is called by `0050EEA0`; `00254CB0` is called by `0050D9A0`; `00254CB0` is called by `0050ED70`; the remaining edges run through shared helpers the page cites.
## The `00379D40` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`00379D40` (13 B) — a two-step wrapper: `call 00379D60` (`00379D44`),
tail `jmp 0036FD60` (`00379D4D`).

| member | role | interior |
| --- | --- | --- |
| `00379D60` (198 B) | list-link body — `rbp = 02ADD170` (`00379D76`), `rsi` → `02ADD878`/`02ADD870` (`00379D7D`/`00379D87`), `02ADD1E0`/`02ADD790` stored into `02ADD170`/`02ADD178` (`00379DE5`/`00379DF3`) — a linked-list splice | [`00379DE5`](../_index/ADDRESS-INDEX.md) |
| `0036FD60` (8 B) | flag clear — `byte[02AD9E00] = 0`, `ret` (`0036FD60`/`0036FD67`); the `jmp 003696D0` is sibling `0036FD70` | [`0036FD60`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003696D0` (reached through sibling
`0036FD70`). The `02ADD170`/`02ADD790`/`02ADD870` cells are the shared
queue links; `02AD9E00` the shared flag byte.

## The `003EADE0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`003EADE0` (512 B) — the request state machine: `byte[rbx+0x31]` gates the
whole pass (`003EADF4`), `byte[rbx+0x30]-1` in 0..7 selects one of eight
state arms through the `dword[rdx+rax*4+0x2CAFEC]` jump table
(`003EAE04`/`003EAE16`/`003EAE20`). Arms call `0032E400`/`0032E4D0`/
`002DF660`/`002DEE90`/`002DF680`/`002DF630`/`002DF600`/`0032E780`; exits
write `byte[rbx+0x30] = 7` or `8` (`003EAFD4`/`003EAFAD`), accumulate
`dword[rbx+0x28]` (`003EAF9F`), leave `dword[rbx+0x2C] = [+0x28] %
[+0x10]` (`003EAFB1`/`003EAFB6`), and return the code in `[rbx]`
(`003EAFA7`).

| member | role | interior |
| --- | --- | --- |
| `002DF600` (6 B) | constant arm — returns `0x10000` | [`002DF600`](../_index/ADDRESS-INDEX.md) |
| `0032E780` (44 B) | signed gate + forward — `edx < 0` → `0xFFFFFFFF`; else passes through to `0032E870` with one stack arg (`0032E788`/`0032E7A2`) | [`0032E7A2`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0032E400`, `0032E4D0`, `002DF660`,
`002DEE90`, `002DF680`, `002DF630`, `0032E870`.

## The `0022B000` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0022B000` (~80 B) — a five-call init battery over `0036F2F0`,
`0035AF10`, `0035AE30`, `0035FF90`, `0036FDF0` (`0022B004`–`0022B018`).

| member | role | interior |
| --- | --- | --- |
| `00375F20` | `02EBF9F0`/`02EC07F0` pair record — `+0x58` non-null gate, `or dword[rax], 1` set (`00375F30`/`00375F36`) | [`00375F30`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0036F2F0`, `0035AF10`, `0035AE30`,
`0035FF90`, `0036FDF0`. `00375EC0` is the clearing twin (`and [rax],
0xFFFFFFFE`).

## The `0032F430` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0032F430` (~43 B) — `ebp = 0`, `r14 = 00120000` image base
(`0032F43B`/`0032F43D`).

| member | role | interior |
| --- | --- | --- |
| `003EA6B0` | state reset — `02B5E0B8 = -1`, `movdqu` zeroes `02B5E0C0`, calls `003DCF00` (`003EA6B7`/`003EA6CB`) | [`003EA6B7`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003DCF00`.

## The `0050EA60` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0050EA60` (5 B) — `jmp 0036EEB0` thunk.

| member | role | interior |
| --- | --- | --- |
| `0036EEB0` | four-register request body (`0036EEB0`/`0036EEC0`) | [`0036EEB0`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Evidence-only read — frontier hub `0032E040` (2026-09-18, SWE2-EC7)

`0032E040` — 38 B, 8 A-measured callers; the guarded queue-kick. Read against the shipping
image (page stays PARTIAL — evidence-only): when `001EDE80()` is non-zero **or** the
`0017D930` thunk's target answers true, the function tail-jumps to `0032E070(0)` at
[`0032E05C`](../_index/ADDRESS-INDEX.md) — the 605 B `FFXII.ResourceDataLoading` routine this queue drains
through; otherwise it returns without touching the queue. A two-predicate enable on the
load-drain path.
