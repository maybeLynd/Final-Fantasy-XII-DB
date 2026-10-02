---
contract: what a save-storage read result and a recovery restore actually did, versus what they report
category: 19-Save-Load-Settings
scope: family
level: L1
readiness: DIFFERENTIAL TESTED # diff_storage_read.py, 77 commands / 100 compared lines / 0 mismatches, 4 mutants killed (SWE2-CONTRACT, 2026-09-14, eab67079)
confidence: PROVEN
implements: 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md
entries: ["00862590", "00866A00", "00583C00"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 48 addresses cited - 3 data, 14 entry, 31 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-13
  last_pass_state: opus-falsification-pass-1-2026-09-13
  crossref_clean: false
  reopened_count: 0
---

# Contract — the storage read returns a byte count it computes as a boolean

The save-storage read **looks like** an API that returns how many bytes it read. It is not one.
It returns **all or nothing**, and on the nothing path it has already modified the destination.

Raised by ASTRA (`ASTRA-REQ-OPUS-STORAGE-COMPLETION` section 25, `ASTRA-REQ-OPUS-LOAD-SUCCESS`
section 24) and re-derived here from the shipping bodies. **§1–§4 are the read; §5 is the recovery
restore.** They are one contract because they share a failure shape: *the call returns normally and
did less than its result suggests.*

## 1. The inner read is a boolean

```asm
00866A00                              ; (cursor* r9=rcx, dest rdx, int r8d)
00866A21  movsxd rsi, r8d             ; requested byte count
00866A27  test r8d, r8d / jle         ; <= 0 -> copy nothing
00866A30  eax = [end] ; rdx = [base] ; ecx = [r9]      ; the cursor, BY REFERENCE
00866A40  sub eax, edx                ; available length
00866A42  cmp ecx, eax / jae 0x866A5C ; cursor at or past the end -> STOP EARLY
00866A46  movzx edx, byte ptr [rcx+rdx]
00866A4A  inc  r11d                   ; bytes actually copied
00866A4D  mov  byte ptr [r10+rdi], dl ; <-- WRITTEN TO THE DESTINATION, byte by byte
00866A54  inc  dword ptr [r9]         ; <-- and the CURSOR ADVANCES with it
00866A5A  jl   0x866A30
00866A61  cmp  r11d, r8d
00866A64  sete bl                     ; <-- 1 IFF EVERY requested byte was copied
00866A67  mov  eax, ebx
```

## 2. The wrapper turns that boolean back into a byte count

```asm
00862590                              ; (mode ecx, ..., elemSize r8d)
00862596  mov  ebx, r8d               ; elemSize kept across the call -- the multiplier below
00862599  test ecx, ecx / jne         ; any mode but 0 -> 008625B8: store -4 and return -4
008625A4  call 0x866A00
008625A9  imul eax, ebx               ; <-- boolean x elemSize
008625AC  mov  dword ptr [global], eax
```

So the returned value is **`allBytesCopied ? requestedBytes : 0`**. A request for 8 bytes with only
3 available returns **0**; the same request with 8 available returns **8**. There is no return value
that means "3".

## 3. What a caller may and may not conclude

| the return is | what it proves | what it does **not** prove |
|---|---|---|
| `requestedBytes` | every requested byte was copied | — |
| `0` | **nothing, on its own** — the call was rejected outright (NULL cursor or NULL destination, `00866A08`/`00866A0D`) **or** it copied a prefix and stopped | which of the two happened. The destination may be untouched, or may hold **part** of the data with the cursor moved by that same partial amount. **Assume the partial write**; nothing in the return value distinguishes them |
| `-4` | the mode argument was non-zero | nothing about the storage |

> **A short read overwrites the front of the destination, leaves its tail holding whatever was there
> before, advances the cursor past the bytes it consumed — and reports `0`.** A caller that reads `0`
> as "no effect" is wrong on all three counts. This is the mechanism behind the player-facing
> statement that *a partial read can change some save data yet report zero*: the copy is byte-by-byte
> at `00866A4D` and the shortfall is only discovered afterwards, at `00866A61`.
>
> The tail is **stale, not zeroed** — nothing writes past the last byte copied — so a partially
> filled structure is a mix of new and previous contents, which is harder to detect than a zeroed
> one.
>
> **A retry does not restart the record.** The cursor advanced by the partial count, so a second call
> resumes mid-structure unless the caller seeks (`008625D0`) first.

**Precondition on everything above: the destination must not overlap the cursor** (qualified 2026-09-28, OPUS; ASTRA
`storage-read-cursor-alias`, check `_experiments/evidence/storage-read-cursor-alias/check.py`, PASS_ORIGINAL_LEAF).
Each iteration stores the copied byte (`00866A4D`), then increments the cursor dword (`00866A54`), then reloads it
(`00866A30`). If `dest` overlaps the 4 bytes at `rcx`, the copy and the cursor write the same memory:
- **count 1, `dest == cursor`:** it returns 1, but the increment overwrites the copied byte. The final byte is `0x0B`,
  not the copied `0x0A`, and the cursor is 11, not 1.
- **count 2, aliased:** it copies 1, reloads a cursor of 11 (past the 4-byte buffer), stops and returns 0.

So with overlap, "`requestedBytes` proves every requested byte was copied" and "the cursor moved by the partial
amount" both fail. The return still reflects the iterations performed. This is an input-state intervention on the
original leaf, not a claim that any caller passes an overlapping destination. The 77-command differential has no
alias case, and the reproduction formula in §12 keeps the original order.

## 4. What this contract does not establish

- **That any shipped caller mishandles it.** This is the API's shape, read from the instructions;
  no caller census is claimed here, and no live short read was observed.
- ~~The callback token/override handling is **ASTRA's reading**, carried forward~~ —
  **fully re-derived 2026-09-18.** `SaveStorageQueue_StartFrontOperation` (`00582040`) is
  a 13-arm dispatch on `dword[+0xD8]` (table `0x46220C`), gated three ways before it: null,
  `[+0x398]==0`, and `+0xDC` bit 0 (the "already started" flag every live arm sets at
  `005820BD`). Arm 1 is the only one that touches the queue's completion fields — it copies
  the front packet's `+0xE0`/`+0xE8` into `+0xC0`/`+0xC8`, so a kind-1 packet carries its
  own callback and token; every other kind completes through whatever `+0xC0`/`+0xC8`
  were already installed (or none — `0058237D` skips a null callback). That is the whole
  "override": no flag, no mode — just which fields the start arm chooses to write.
  The completion's remapping (`00582240`) is two-stage: `dil` defaults to 0 for kinds
  1–2 and to `003BB420()` for higher kinds; `0017E470()` then returns the operation's
  stored status `[001D50D0()+0x10DC]`, and three fix-ups override `dil` on
  `(status, kind)` pairs — status 1 or 3 with kind 7/9 → `dil=8`, status 2 with kind ≠4
  → `dil=3`. When the resulting `dil` is 4 the controller's slot bitmap is **cleared** —
  25 zero bytes at `[02CA99B8]+0x568`..`+0x580` (`rbp` is `xor`'d at `00582264` and never
  reloaded). The callback then runs as `+0xC0(kind, dil, +0xC8)` at `0058238E`, gated by
  `r8d = ~([+0xDC]>>1) & 1` — suppressed exactly when `+0xDC` bit 1 is set, as the carried
  reading said.
- ASTRA additionally records, as bounded code facts rather than live failures, that the metadata
  count check refuses `== 8` rather than `>= 8`, that an empty completion underflows, and that a
  packet-8 auxiliary input above 16 is not clamped. **Re-derived 2026-09-14 — all three
  confirmed, and the first two compose:**
  - `SaveStorageQueue_EnqueueOperation` (`00582540`) refuses a queue count of exactly 8 —
    `0058255B cmp al, 8` / `0058255D je` — equality, not `jae`. A count above 8 passes the
    refusal and `0058256C imul rcx, rax, 0x58` writes past the 8-slot array.
  - `00582240` decrements the count with no zero guard — `00582276 sub al, 1` — so completing
    an empty queue leaves `[+0x398]` at `0xFF`, and the compaction loop in the *same call*
    then runs `0xFF` iterations of the `0x58`-stride shift (`00582290`–`005822D9`, bound
    `ecx < [+0x398]` at `005822D7`) — an out-of-bounds slide inside the completion itself.
    **That is precisely the value the `== 8` check does not refuse**: the next enqueue passes
    `cmp al, 8 / je` and `0058256C` writes slot `0xFF` at `+0xD8 + 0xFF × 0x58`. Neither is a
    live-observed failure; both are shipped instructions.
  - Packet kind 8's auxiliary input (`[rdx+0x50]`) is not clamped: `005825DF cmp ecx, 0x10`
    tests `existing + aux` against 16 and on overflow only resets the aux base `+0x39B` to 0
    (`005825E4`) — the copy loop at `00582600` then still runs `aux` iterations, so an aux
    count above 16 writes past the 16-entry `0x38`-stride array at `+0x3A0`.
- The PC record being **`0x210` of cursor, mode and path plus a shared vector — not a CRT `FILE*`** —
  re-derived 2026-09-14 from `008666B0`'s construction. The reader allocates `0x210`
  (`0086670D`–`00866716` via `0019C580`), writes `+0x00` = cursor 0 and `+0x04` = the caller's
  mode (`00866724`/`00866726`), then copies the caller's wide path into `+0x08` at two bytes a
  step (`00866730`–`0086673F`) — `0x08 + 0x208` = `0x210`, a `wchar_t[260]` (`MAX_PATH`). The
  byte stream the record cursors over is the **shared** `01F44D40`/`01F44D48` vector — sole
  writer `008666B0` — not per-record storage and not a CRT `FILE*`. `008666B0` returns the
  record; `008624D0` stores it at `02EAF8E8` (`00862548`) and finalizes a displaced record
  through `00866200` first (`00862508`); `008620E0` is the close — `00866200` flush/finalize,
  null the pointer, `-3` into `02EAF8E0` on failure (`008620F9`–`0086210B`).

## 5. The recovery path restores the image PREFIX, and stops before the first persistent group bank

`00583C00` is the second place in this subsystem where a result looks whole and is not.

```asm
00583C04  cmp qword ptr [global], 0 / je 0x583CA1   ; null -> restore NOTHING and return
00583C12  call 0x2EF640                              ; the ACTIVE buffer
00583C1E  mov edx, 0x1C4                             ; 452 iterations
00583C23  mov rcx, qword ptr [rcx+0x588]             ; source: parent +0x588
00583C30..00583C81   eight movups pairs per pass     ; 0x80 bytes x 452 = 0xE200
00583C83..00583C9D   four more movups pairs          ; + 0x40
```

**`0x1C4 × 0x80 + 0x40 = 0xE240`** — **57,920 bytes**, against a full image of `0x56690` =
353,936. So this path restores **16.4 % of the image**.

> **`0xE240` is not an arbitrary size — but it is a WHOLE-IMAGE offset, and that changes which
> field it lands on.** `0x2EF640` returns the buffer base, header included, so the copied range is
> whole-image **`[0, 0xE240)`** = payload **`[−0x200, 0xE040)`**. Payload `+0xE040` is the start of
> **group persistent bank A**, not SpawnKeep image A — SpawnKeep A is payload `+0xE240`, which is
> whole-image `+0xE440`, well outside the copy.
>
> **So the restore stops immediately BEFORE the first persistent group bank, and touches neither
> group bank A nor either SpawnKeep image.** That is what makes it a *bounded prefix recovery*, and
> why the player-facing note says error recovery protects the earlier image prefix rather than the
> persistent group data.
>
> > **⚠ Corrected within the hour, 2026-09-13 (`ASTRA-REQ-OPUS-PREFIX-BOUNDARY`).** This section
> > first said the copy ran *"up to the SpawnKeep images"*, by reading `0xE240` against the **payload**
> > map while the instruction produces a **whole-image** offset. **Wrong by the same `0x200` header I
> > had recorded a coordinate note about one task earlier** — and wrong in the direction that
> > matters, since it implied group bank A is rolled back when these copies never touch it. ASTRA
> > raised it, FABLE reviewed it independently, and the arithmetic settles it: `0xE240 − 0x200 =
> > 0xE040`. **Knowing a trap exists is not the same as checking for it**, and the check here is one
> > subtraction.
>
> **It is not the global backup and not the full image.** Neither `0x56690` nor `022676C0` is
> touched here; the source is `parent + 0x588`.
>
> And the null guard at `00583C04` means the same call **restores nothing at all** when that pointer
> is unset — again returning normally, with no indication to the caller.

The rest of ASTRA's section 24 was re-derived from the shipped bodies 2026-09-15
(SWE2-CONTRACT); every reading confirmed, two sharpened and one corrected:

- **`00580840` (`SaveLoad_FullImageStorageCompletionCallback`, 568 B)** is the completion
  dispatcher, gated on `[rbx+0xE0] & 0x10` clear (`0058084C`), and only states **9** and
  **0xC** have bodies — anything else returns at once. On the state-9 arm it releases
  `[rbx+0xD8]` through `00244F00` and nulls it, writes `4` to `[02CA99E0]+0xCC`, calls
  `00581350(result != 0)`, then `00254CB0(0)`. The result mapping is three-way:
  `0` → the success arm (`esi=0`, `r14d=0`); `8` → the `esi=1` arm; anything else →
  `r14d=1`. **Only the success arm runs `00247510([rbx+0xC0], 0x10, 4)` at `005808E6` —
  the `parent` is the queue's `+0xC0` context pointer, not the packet** — immediately
  before `00580EB0(rbx, 9, 0)` enters the transition machine. Result `8` runs
  `00583C00` (the backup restore), posts `{4, 1}` through `003BB600`, sets bit
  `[rbx+0xEB]` of the `02CA99B8`+`0x568` bitmask (refused `>= 0xC8`), optionally clears
  `[rbx+0xC8]`'s `+0x100` and calls `00247870`, then `00580EB0(rbx, 0xE, 0xA)`. Other
  failures take `00580EB0(rbx, 0xD, 6)`. State 0xC mirrors: success clears `[rbx+0xE0]`
  bit 0, sets bit 3, calls `005813E0`, then `00580EB0(rbx, 0xC, 0)`; failure ORs 4 into
  `[02CA99C8]+0xC8` and takes `00580EB0(rbx, 0xD, 4)`.
- **`00580EB0` (`SaveLoad_ControllerTransitionStateMachine`, 950 B)** is the state-9
  result-message machinery ASTRA gestured at: a 15-entry dispatch on `dl` (bounded
  `0xE`, table `0x461268`), writing the state byte to `[rbx+0xE9]` — `00580EE2` skips
  the whole body when the state is already current. Each arm selects a `dil` message
  id; the shared tail at `0058122B` calls `00583990(dil, rbx)` and stores the result
  at `[rbx+0xD8]` — the field the completion callback releases. **State 9's arm is
  `00581141`, `dil = 0x17`.** `00583990` clamps the id to `< 0x1F` and indexes
  `00D23DA0`, a `.rdata` table of `{resource-id, kind-byte}` pairs — entry `0x17` is
  `{0x87F, kind 0}` — resolving the id through `002F9860` and dispatching on the kind
  (1/2/3/4). Arms 8 and 0xB additionally enqueue packets into `02CA99C0` through
  `00582540` with `00580840` as their completion callback — **this is how the
  completion callback is re-entered**: arm 8 enqueues `{1, cb=00580840}` and a
  kind-**9** packet carrying a name and `0x56690`; arm 0xB enqueues `{1, cb}` then
  `{0xC}`. Arm 4 stores a `00244F50`-built timer handle at `[rbx+0xD0]`.
- **`0057FE80` is a two-level dispatcher.** The outer select is
  `dword[msg] − 1`, bounded at `0x11` (18 ids, table `0x4607B8`); the subtype
  select on `qword[msg+8]` runs only inside outer arm **12** (`00580401`).
  Outer arms: id **1** (`0057FEB1`) is the populate arm — copies `msg+0`/`+8`
  to `+0xC0`/`+0xC8` (the callback+token packet kind 1 can later override),
  `+0x10`→`+0xEA`, `+0x14 & 1`→`+0xE0`, `+0x18`→`+0x1C0`, `+0xE9` to `0xFF`
  then `00580EB0(rbx, 0)`; `002432B0` fills the `+0x50` view and copies the
  `[msg+0x20]` record's `+4`/`+6`/`+8`/`+A` words into `+0x98..+0x9E`;
  `+0x1B8` = `[[+0x60]]+0x18`; `+0xE4`/`02CA99B4` = active header `+0x50`.
  Then a `02CA99B8`-gated loop over `dil` 0–0xC7: tests bit `dil` of the
  `+0x568` bitmap (`003BB600(dil, {4,1})` on set bits), resolves every slot
  via `003BB3E0(dil)`, counts `+0xED`/`+0xEE` by slot state, keeps a best
  `+0xEC` by each record's `+0x50` dword, and appends chosen indices to the
  `+0xEF` byte array the `0x8000`/`0x8001` arms read. Post-loop, when
  `msg+0x10 == 1` and a candidate exists, it rotates the `+0xEF` list by
  adjacent swaps, reconciles `+0xE4`/`02CA99B4`, calls `002D45C0(+0x1B8, 1)`,
  sets `[+0x1B8]+0xE0 |= 0x8000000`, runs `002445C0`. Id **2** (`00580356`)
  requires `001EDEC0([+0xB4]) != 0`, `+0xE9 == 0xC`, and `byte[+0xE8]`
  decrementing to zero (one-shot); it releases `+0xD8` through `00244F00`,
  sets `[02CA99E0]+0xCC = 4`, clears `+0xD8`, transitions to 1. Id **10**
  (`005803C7`) runs only while `02CA99E0 == 0`, state 0, `+0x1B8` non-null —
  `002D3900(+0x1B8)`, the per-frame tick over the display words. Id **14**
  (`0058030F`) is the dialog arm: `+0xEA == 0` selects message `0xC82`, else
  `0xC86` when `00394450() == 3` else `0xC84` — resolved via `002F9860`,
  shown via `00291D80(…, 0)` and `002470D0(rbx)`. Ids **15**/**18** notify
  the `+0xC0` parent through `00247510` with messages `0xF`/`0x12`
  (`r8d = 4`). All other ids tail-jump `005C5230`; every path returns 0.
- **Subtype arms inside outer id 12** (`00580401`, on `qword[msg+8]`):
  - `0x12` (`005804E8`) acts only when `qword[msg+0x10] == 0xA`, clearing
    `+0xD0` — the timer handle `00580EB0` arm 4 installed.
  - `0x1D` (`00580495`) requires `+0xE0 & 0x10` clear — the same flag that
    gates `00580840`, so it refuses while a completion dispatch is armed —
    then re-dispatches on `dword[[msg+0x10]]`:
    - `3` → `00580A80`: refuses state `0xD` and zero `[payload+8]`, runs
      `0057ED40`, then its own `+0xE9 − 2` table (`0x460B0C`). Live arms —
      states 2,3,5,6,7,10,12,14 — all run `00580AC5`: release `+0xD8` via
      `00244F00`, set `[02CA99E0]+0xCC = 4`, null `+0xD8`, transition to
      `0xD`. States 4,8,9,11,13 skip to the transition.
    - `0xD` → `00580B40`: two halves. `+0xEA == 0` selects on
      `[payload+8]`: `0` → `+0xE0` flag dispatch (bit 3 → clear it +
      transition 4; bit 1 → transition 3; else transition 2), `1` →
      transition `0xA`, `3` → `00580EB0(0xD, 1)`, `4` → `00580EB0(0xD, 0)`,
      else `00580EB0(0xD, 3)`. `+0xEA != 0` computes a scroll index into
      the `+0xEF` list: `(word[+0xF2] + word[+0xF4]) * byte[+0xEC] +
      sbyte[+0xEE] + sbyte[+0xED]` over `+0x1B8`, giving the record
      `rdi = +0xEF[idx]*0xA0 + [+0x1C0]`; `[payload+8] != 0` →
      `00580EB0(0xD, (ecx==4) ? 0 : 3)`; `== 0` → transition `8` when
      `00394450() == 3` **or the record's own `+0x57` bit 0 is clear**,
      transition `6` when the record's `+0x57` bit 0 is set — the same
      flag byte the `005843E0`/`00584210` split reads.
    - `0xF` → `00580CD0`: releases `+0xD8`, sets `[02CA99E0]+0xCC = 4`,
      nulls `+0xD8`, then `00581350([payload+8] != 0)` — which releases
      `02CA99C8`'s pending `+0xE8` resource through `0024A1A0` (bit-0 gate
      on `+0xCC`, `+0xE8` reset to `-1`) and, when the argument is zero,
      plays a chime through `00249C60`: `0x27` for `+0xD0` modes ≤1 or 4,
      `0x43` for modes 2–3.
  - `0x8000` (`00580433`) reads the same `+0xEF` slot byte as `0x8001` and
    resolves `003BB3E0`; when `*info == 2` it binds
    `edi*0xA0 + [+0x1C0]` into the `+0xC8` object through `0057EFE0`
    (`[+0x100] = record`, `00247870` refresh); otherwise it clears
    `[+0xC8]+0x100` and refreshes with `00247870(0)`.
  - `0x8001` (`00580508`): the selected slot byte is read from the message
    payload's `+0xEF` (`movzx edi, byte [rax+rcx+0xEF]`), resolved through
    `003BB3E0`, and written to **`[02CA99B8]+0x598` as a byte** — `02CA99B8`
    is the controller singleton, and the same byte is stamped on the
    packet's `+0xEB` (the index `00580840` uses for its `+0x568` bitmask)
    while bits 1–2 of `[rbx+0xE0]` are cleared. The tail derives `r8b` ∈
    {7,8,9,0xA} from `*info`, `[info+4]`, and `+0xED` (0xFF when suppressed:
    `+0xEA != 0` needs `*info == 2`; `+0xEA == 0` needs `+0xE0` bit 0),
    sets `+0xE0` bit 1 when `*info == 2` or bit 2 when `*info == 4` on the
    `+0xEA == 0` path, runs `0057ED40`, then transitions to **1** when
    `r8b == 0xFF` else **0xE** passing `r8b`.
  - `0x8002` (`00580769`) sets `+0xE0 |= 0x10` and calls `00244F00(rbx)`.
  - `0x8100`–`0x8102` (`00580602`): sets `[02CA99E0]+0xCC = 4`, clears
    `+0xD8`, runs `0057ED40` (collapses `02CA99C0` to head-only when its
    `+0xDC` bit 0 is set, else empties it via `+0x398 = 0`, `+0xCC = 0`;
    either way clears `02CA99D8+0xC0` low bits), then dispatches on queue
    state `+0xE9 − 2` (table `0x460800`, 13 arms): `0x8100` selects
    transition `4` (states 2–3), `8` (6–7), `0xB` (10); `0x8101` runs
    `00249C60(2)` then transition 0; state 9 sets `+0xE0 |= 0x10` +
    `00244F00`; state 12 takes transition 1 unconditionally; state 13 adds
    `005812B0` (resets `02CA99C8` fields `+0xD4`/`+0xDC`/`+0xC8`/`+0xFC`,
    `00225580(+0xF0, 0)`); state 14 runs `005812B0` + transition 0;
    remaining states take transition 0. Other `>0x8001` values bail.
- **The `005843E0`/`00584210` admission split — corrected.** The split is **not**
  a `parent+0x18`/`+0xC4` bit-4 test. Both bodies compute the same two predicates:
  `esi = (00394450() == 3)` and `ebx = byte[+0x57] & 1`. `00584210`
  (`SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`) takes a **stash** arm when
  `(mode==3 && flag clear)` — copying `rdi+0x10`/`+0x18`/`+0x1A`/`+0x1B` to
  `rbx+0x70..0x7B`, `00320D50()` to `rbx+0x7C`, and `rbx+0x1244..0x1254` (~~six~~ five *(corrected 2026-10-02, OPUS: `0058427B`–`005842B1` and `00584325`–`00584362` copy five; the save-image page's header map, `+0x80 5 dwords`)*
  dwords) to `rbx+0x80..0x90` — and a **restore** arm when `(mode!=3 && flag set)`,
  reversing exactly those copies, reseeding via `00269A20(rbx+0xE240)` /
  `002EF410(rbx+0x4E660)`, clearing `[rbx+0x57]` bit 0, `01E0C3EC`, and
  `[02EBF190]+0x5B04` bit 0, then `0023A390`; `005843E0`
  (`WorldTransitionSnapshot_RestorePersistencePairForActiveSlot`) uses the same
  predicates plus `00236760()` to choose between the `+0x4E660`/`+0xE240`/`+0xE440`
  trio and the `+0x2E450`/`+0x2E650` pair, skipping entirely on
  `(mode==3 && flag clear)`, and clears `[02EBF190]+0x5B04` **bit 1** (not bit 0).
  `rdi+0x18` participates only as stashed payload (a word); `+0xC4` appears
  nowhere. Both tails call `00316810` (PlatformOnlineAchievements) and the
  `008C3060` indirect reseed.
- **`00583CB0` (`SaveUI_BackupActiveHeaderToControllerCache`, 166 B)** copies the
  active header to the controller cache: no-op when `02CA99B8` is null;
  `rax = 002EF640()` is the source and `[[02CA99B8]+0x588]+0x80` the destination;
  the loop is `0x1C4` iterations of `0x80` bytes plus a `0x40` tail —
  **`0xE240` bytes, exactly the whole-image size the restore at `00583C00`
  copies back**, and exactly the byte count §4's recovery arm moves.
  `[parent+0x588]` is itself a pointer — the controller holds a separate cache
  object, not inline storage.

- **The `+0x588` cache-object lifetime — established.** `00582860` is the
  controller's own message dispatcher (a second two-level consumer of the
  same queue protocol): outer select `dword[msg] − 1` bounded at `0x12`
  (19 ids, table `0x462F54`). Its **id-1 arm** (`005828AC`) is the init: it
  stores `rbx` into `02CA99B8`, copies the message's `+8` byte to `+0xC1`
  and sets `+0xC4 = 8` when `qword[msg+0x10] == 1`, zeroes `+0xC0`–`+0xF8`,
  then allocates **`+0x588 = 002497E0(2, 0xE240)`** — the arena alloc
  wrapper (`0036C1D0` push `{2,0xC}` / `0036A100` / `0036C140` pop) — at
  exactly the `0xE240` backup size, plus a sibling
  **`+0x590 = 002497E0(2, 0x7D00)`** zeroed via `00861EC0`, then calls
  `00583CB0` to snapshot the active header into the fresh cache before
  `003678F0` / `00283270` / `00582790` (the widget bind). Its **id-18
  arm** (`00582E81`) is the teardown: `[+0xC4] & 0x10` with `+0x598 == 0`
  runs `001831A0`, sets `0209AC10 = 1`, and calls `005843E0` (the
  persistence-restore pair) inside `00182D40`; `00394520()` non-zero runs
  `00394400`; then `00584210` (the normalize/reseed), `00582FC0` (releases
  `+0x100`/`+0x108`/`+0x110`), **`003697F0` frees `+0x588` and `+0x590`
  and both are nulled**, `02CA99B8` is cleared, `[+0xC4] & 8` runs
  `002814E0(0xFFFFFFFE)`, and `002E1CA0(1, 0x15)` mirrors the init's
  `002E1C20(1, 0x15)`. The cache therefore lives exactly as long as the
  controller instance: **allocated at controller init before the first
  `00583CB0`, freed at controller teardown — never reallocated in
  between.** Arm map for the rest: id 2 (`00582A31`, `001EDEC0`-gated
  `00582540` enqueue), id 12 (`00582B2C`), id 16 (`005829C0`, a
  suspend/hide sequence `003946B0`/`00244F50`/`00394700`/`00247930`/
  `00244960`/`00247870`), id 19 (`00582AE9`, dialog path
  `002F9860`/`002CA150`/`00244F50`/`00246AD0`); other ids bail at
  `00582F24`.

**Arm id 12's nested dispatch (`00582B2C`) is the controller's own subtype
select**, mirroring `0057FE80`'s arm 12. `qword[msg+8]` selects: `0xF` →
`00582CF2` (requires `qword[msg+0x10]==4`: `00581310(+0xD0)`, then
`00244F00(+0xE0)`); `0x10` → `00582CB3` (arms `+0xC4` bit 4, then
`00238A30(00394450()==3 ? 1 : 0)` and `00285E60(-1)`); `0x12` → a payload
dispatch on `qword[msg+0x10]` bounded 2–9 through table `0x462FA0`; `0x1D`
→ `00582D25` (requires `dword[[msg+0x10]] == 0xA`, then
`00583040(rbx)`); `>0x1D` → `00582D41`. The `0x12` payload arms clear or
release one field apiece — 2 → `00582B7C` (releases `+0xC8`, `02CA99D0`,
`02CA99D8`, `02CA99C0`, `rbx` via `00244F00`), 3 → `00582BC7` (clears
`+0xD0`; gated `+0xC4&0x10` and `+0xC0==3`, then `0057ED40` and the same
releases), 4 → `00582C38` (clears `+0xD8`, releases `02CA99D0`/
`02CA99C0`/`rbx`, `+0xC0=1`), 5 → `+0xE0=0`, 7 → `+0xE8=0`, 9 → `+0xF8=0`;
6 and 8 bail. `0x8001` (`00582D8B`, requires `qword[msg+0x10]==2`) builds
two packet records — `+0xD0 = 00244F50(0x110, cb=00581490)` and
`+0xF8 = 00244F50(0xF0, cb=0057F360)` carrying `rbx`, `+0xC1`, `+0x590` —
then `005819A0(+0xC1==1)`, resolves message `0xE` into `+0xF0` via
`00583990`, and moves to state `+0xC0=2`. `0x8100`–`0x8102` share
`00582D59`: `[02CA99E0]+0xCC = 4`, `+0xF0 = 0`, `00581310(+0xD0)`.
`00581310` itself releases its argument (`00244F00`), runs `00291D40` and
`002CA110`, and — when the controller's `+0xC4` bit 3 is set — `002CC9B0`
tailing into `002CC9C0`.

**`00583040` (`SaveLoad_HandleStorageStatusResultAndAdvanceController`)**
re-dispatches on `dword[msg+8]`: `0→edi=0`; `1→edi=(+0xC1!=0 ? 2 : 0xFF)`
with `ebp=1` and `ebx=(+0xC1==0)`; `3→edi=1`; `4→edi=0`; else `3`. The
common tail releases `+0xF0`, marks `[02CA99E0]+0xCC = 4`, and runs
`00581350(ebx==0)` — the same chime/release helper as the queue side. When
`ebx` is set it additionally releases `+0xC8` (`00244DD0`) and builds two
packets — `+0xE0 = 00244F50(0x108, cb=0057EDB0)` and
`+0xD8 = 00244F50(0x1C8, cb=0057FE80)` carrying the controller, `+0xC1`,
`+0x590`, `+0x108` and `ebp` — **a self-post into the queue dispatcher**,
then `+0xC0 = 4`. Otherwise `00583990(edi, rsi)` resolves the result
message, `0057EC60(rsi, 1)`, `+0xC0 = 3`.

**Arm id 16 (`005829C0`)** is the suspend path: `003946B0(+0x108, 6)`;
when `02CA99C0 == 0` it builds `00244F50(0x720, cb=005823B0)`; then
`00394700(0)`, `00247930(0x64)`, `00244960(0208EA28)`, `00247870(0)`, and
arms `+0xC4` bit 1. **Arm id 19 (`00582AE9`)** opens dialog `0x870` or
`0x871` by `+0xC1` through `002F9860`/`002CA150`, self-posts
`00247510(rbx, 0x8001, 2)`, and sets `+0xC0 = 1` — the message that lands
on the `0x8001` arm above.

**The controller readers `00583260`–`00583990`.**
`SaveWrite_OpenOperationController` (`00583260`) posts
`00244F50(0x178, cb=0057E4D0)` with a zeroed payload.
`SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`) memsets the
descriptor, stamps `"PS2D"` (`00D23F10`), bounds the slot `< 0xC8` and two
`0x3C` fields, validates via `00254A10`, then builds paths with the
`0017D2E0` formatter (`00D23F18`/`00D23F38`/`00D23F4C`/`"%s%s%s"` at
`008F80C8`) and calls `005837F0` three times — one per asset name.
`SavePath_BuildSlotDirectoryName` (`00583700`) and
`SavePath_BuildSlotAssetName` (`005837F0`) are both gated on `02CA99B8`
and write into `controller+0x128`: the directory is `"%s%03d"` of a base
(`003935C0`) plus the slot byte, prefixed `"/%s"` when its flag arg is
nonzero; the asset name selects `"icon.sys"`, `"%s%03d"` (≤ `0x40`), or
`"static.ico"` on its kind byte. `SaveWrite_GetBusyFlag` (`00583920`)
returns `[02CA99E8]`. `SaveLoad_OpenController` (`00583930`) posts
`00244F50(0x5A0, cb=00582860)` carrying `{arg3, arg1!=0, arg2!=0}` — the
client-facing way the controller's id-1 init is reached.

The `0057FE80`/`00582860` inventory is now mapped two levels deep at every
point the contract names; deeper leaf helpers (`00244F50`, `00581350`,
`00583990`, `0057EC60`, `0057EDB0`, `005823B0`, `00581490`, `0057F360`,
`005819A0`) keep their established roles — record allocation, resource
release with chime, message resolution — and are not re-opened here.

## 6. Relationships

**Callee/caller.** `00862590` (the wrapper) is the only caller of `00866A00` named here; it loads
the cursor object from `[02EAF8E8]`, calls the inner read, multiplies the boolean by `r8d` and
stores the product at `[02EAF8E0]`. `008625D0` is the sibling **seek** the caller must use to
reposition — §3's retry note depends on it.

**Globals.** The inner read's backing store is the base/end pair `[01F44D40]` (qword) /
`[01F44D48]` (dword end, written as a qword); the base has **exactly one writer in the image** —
`008666B0`, site `00866965` — and the end is stored by the same body at `00866974`.

**The recovery path.** `00583C00` reads the parent pointer `[02CA99B8]`, calls `002EF640` for the
active image buffer (`02164280`, a bare `lea`/`ret`), and copies from `[parent + 0x588]`.

**The load pipeline is now re-derived, 2026-09-14.** `003BA7B0` is a 16-entry sub-state
dispatch on `[02B40E14]` (table `0x3BA944`, `cmp 0xF / ja` at `003BA7BB`–`003BA7BF`):

- **state 0** → `003BA7D9`: clear `[02B40EC0]`, state → 1.
- **state 1** → `003BA7F0`: `008620D0([02B40E20], &path02B40E28)` result-clear stub, state → 2.
- **state 2** → `003BA815`: prior result nonzero → error arm; else `008624D0` — open via
  `008666B0`, record → `02EAF8E8`, `-4`/`-3` on failure — state → 6.
- **state 6** → `003BA845`: `ecx < 0` → error arm; else `[02B40E24]` = read result, and if
  `[02B40EFC] > 0` → `008625D0` seek, state → 15; else `00862590` read, state → 8.
- **state 15** → `003BA896`: `00862590` read with `(count=[02B40E24], dest=[02B40EF0],
  size=[02B40EF8])`, state → 8.
- **state 8** → `003BA8C2`: `ecx < 0` → `003BA8E0` (clear `[02B40E10]`; error sub-state
  `[02B40E18]` = 8 if `ecx == -3` else 9); else `008620E0` close, state → 9.
- **states 9/10** → `003BA90C`: terminal — `ecx == 0` and `r8d == 0xA` keeps state and clears
  `[02B40E10]`; otherwise clears `[02B40E14]` and `[02B40E10]`, resetting the chain.
- **states 3–5, 7, 11–14** → `003BA93D`: idle no-ops.

`00582040` (StartFrontOperation) admits the front packet when the queue is non-empty
(`0058206D`) and `+0xDC` ~~bit 1~~ bit 0 is clear (`00582076`) *(corrected 2026-10-02, OPUS: `00582076` is `test byte ptr [rcx + 0xdc], 1`; bit 1 is the completion-callback suppressor)*, dispatches kind `0..12` through table
`0x58220C`, then sets busy ~~bit 1~~ bit 0 *(corrected 2026-10-02, OPUS: `005820BD` `or dword ptr [rbx + 0xdc], 1`)* and returns 1. **Packet-9's arm** (`0058218A`) calls
`003BB440`, which *is* the acceptance: refuses if a chain is in flight (`[02B40E10] != 0`,
`003BB440`) or the packet's `+0x128` length is 0 (`003BB44F`); copies the packet's inline
name at `+0xE0` into `02B40EC8` (`003BB454`–`003BB46C`); records dest `+0x120` → `02B40EF0`
and length `+0x128` → `02B40EF8`; and arms the chain — `[02B40E14]` = 1 — at `003BB49C`.

## 7. State transitions

```
cursor:    positioned at c within [0, end - base)
             -- inner read, n bytes, c + n <= avail --> advanced to c + n, returns 1 (wrapper: n * elemSize)
             -- inner read, c + n > avail --> advanced to min(c + n, avail), returns 0  (PARTIAL: prefix written)
             -- cursor already >= avail --> unchanged, returns 0 (nothing written)
             -- null cursor or null dest --> unchanged, returns 0 (nothing written - indistinguishable from partial)
             -- n == 0 --> unchanged, returns 1
             -- n < 0 --> unchanged, returns 0
wrapper:   mode != 0 --> result global and return = -4, cursor untouched
restore:   [02CA99B8] == 0 --> no-op (no status returned)
           [02CA99B8] != 0 --> active buffer [0, 0xE240) overwritten from [parent + 0x588]
```

The cursor only ever moves forward inside one buffer; there is no reset inside this family — the
seek `008625D0` is the only reposition.

## 8. Script · resource · event interactions

This is the **file-format layer** of save load: the bytes come from a save-storage buffer, and the
recovery restore is the error-recovery path of the load pipeline (ASTRA's state-9 context, §4). No
script verb or authored table participates directly; the resource is the save image itself. The
`mode` argument is a caller-side discriminator, not read from the file.

## 9. Determinism

- **RNG** — none.
- **Timing / ordering** — the read is a pure sequential copy; the only ordering fact that matters is
  that the cursor is shared state (`[02EAF8E8]` hands the same object to every wrapper call), so
  reads consume the buffer in call order.
- **Threading** — not established. ASTRA's queue/compaction readings (§4) imply an asynchronous
  load pipeline; which thread runs these bodies is not claimed.

## 10. Failure paths and edge conditions

- **`cursor` or `dest` NULL** — return 0, nothing written, cursor unmoved (`00866A08`/`00866A0D`).
- **`count <= 0`** — the copy loop is skipped; `count == 0` returns 1, `count < 0` returns 0.
- **Cursor at or past end** — the unsigned `cursor >= end - base` test stops before the first byte;
  returns 0.
- **Short read** — the prefix is written and the cursor advanced by the shortfall amount, then 0 is
  returned; the destination tail keeps its previous contents (stale, not zeroed).
- **`mode != 0`** — `-4` is written to `02EAF8E0` and returned; the storage is untouched.
- **Null recovery parent** — `00583C00` returns normally having copied nothing; no status tells the
  caller.
- **`0` is ambiguous** — the return value cannot distinguish *rejected arguments* from *partial
  write*. §3's table is the contract on this.

## 11. Observable behaviour

Everything the family does is measurable in memory: the destination buffer's contents (including a
partial overwrite with a stale tail), the cursor dword inside the object `[02EAF8E8]` points at,
the result dword `02EAF8E0`, and the `0xE240`-byte prefix of the active image `02164280` after a
restore — with `+0xE240` untouched as the boundary canary. `diff_storage_read.py` prints and
compares all of them per command.

## 12. Reproduction formula

```
inner read (00866A00):  (rcx = cursor*, rdx = dest, r8d = count)
    if rcx == 0 or rdx == 0: return 0
    avail = (u32)[01F44D48] - (u32)[01F44D40]     # end - base, 32-bit, exact for any buffer < 4 GiB
    copied = 0
    while copied < r8d (signed):                 # r8d <= 0 skips the loop
        if [rcx] >= avail: break                 # unsigned compare, reloaded each iteration
        rdx_dest[copied] = [01F44D40][[rcx]]
        [rcx] += 1; copied += 1
    return copied == r8d                          # boolean, not a count

wrapper (00862590):  (ecx = mode, r8d = elemSize)
    if ecx != 0: [02EAF8E0] = -4; return -4
    r = inner([02EAF8E8], dest, r8d)
    [02EAF8E0] = r * r8d; return r * r8d          # n on success, 0 on any failure

restore (00583C00):
    if [02CA99B8] == 0: return                    # silent no-op
    dst = 002EF640()                              # == 02164280, header included
    src = [[02CA99B8] + 0x588]
    copy 0x1C4 passes x 0x80 bytes, then 0x40     # total 0xE240; payload span ends at +0xE040
```

## Falsification pass 1 — 2026-09-13 (OPUS), re-derived from the shipping bytes

*(Unnumbered: it previously held the `## 6.` heading, which collides with the template's
Relationships section now written above.)*

Every claim in §1–§3 was re-decoded from the reference image rather than re-read
([`falsify_storage_read.py`](../../Tools/analysis-kit/gfz-scripts/falsify_storage_read.py); `capstone`, file offset `VA − 0x121000 + 0x600`).
**Two attacks failed, one found a gap, and one of my own results was a false negative.**

### The attack that mattered, and it failed

§2 says the wrapper returns `allBytesCopied ? requestedBytes : 0` and quotes `imul eax, ebx` — but its
prose calls the multiplier **`elemSize` (`r8d`)**, and `ebx` is a different register. Every caller
conclusion in §3 rests on that formula. The missing instruction is real and it is one line above the
quoted range:

```asm
00862596  mov  ebx, r8d          ; <-- the line §2's listing omits
00862599  test ecx, ecx / jne 0x8625B8
008625A4  call 0x866A00
008625A9  imul eax, ebx          ; therefore: boolean x elemSize, exactly as §2 says
```

**§2's claim is correct and its listing is incomplete.** The line is added above.

### The second attack, and why it also failed — recorded so nobody re-raises it

The loop computes the available length in **32-bit arithmetic over two 64-bit pointers**:

```asm
00866A30  mov eax, dword ptr [rip + 0x16DE312]   ; 01F44D48 - read as a DWORD
00866A36  mov rdx, qword ptr [rip + 0x16DE303]   ; 01F44D40 - the base, full 64-bit
00866A40  sub eax, edx                           ; (uint32)end - (uint32)base
```

`01F44D48` is **written as a `qword`** — its single producer stores `rdi + rax`, an end **pointer**,
at `00866974` — and read here as a `dword`. That is the shape of a truncation defect, and it is not
one: the subtraction is exact modulo 2³², the span `end − base` is a buffer length and therefore below
2³², so `(uint32)end − (uint32)base` **equals** `end − base` for every representable buffer, wherever
it lives in the address space. The byte address itself never uses the truncated value — `movzx edx,
byte ptr [rcx + rdx]` indexes the **full 64-bit** base. **An attack that fails is worth the same
paragraph as one that lands**, because the alternative is that the next reader finds the same
`dword`/`qword` mismatch and re-opens it.

The base pointer has **exactly one writer in the image** — `008666B0`, site `00866965` — which is what
makes the lifetime argument above tractable at all.

### The gap: §3's table is missing a third meaning of `0`

§1's listing begins at `00866A21` and so omits the two argument checks that precede it:

```asm
00866A08  test rcx, rcx / je 0x866A70     ; cursor NULL
00866A0D  test rdx, rdx / je 0x866A70     ; destination NULL
...
00866A70  xor eax, eax / pop rdi / ret    ; -> 0
```

So the inner read returns `0` on a path where **nothing happened at all**: no byte written, no cursor
movement. The wrapper multiplies that `0` by `elemSize` and stores `0`, exactly as it does for a short
read.

> **`0` is ambiguous, and nothing in the return value resolves it.** It means *either* "the arguments
> were rejected and the destination is untouched" *or* "some prefix of the destination was overwritten
> and the cursor advanced past it". §3 currently warns only that `0` does not prove nothing happened;
> the stronger and more useful statement is that **a caller cannot tell the two apart**, and the
> defensive reading — assume the partial write — is the only safe one. §3's table is corrected below.

### One of my own results was a false negative

The first run of the pass reported the `-4` non-zero-mode path **NOT FOUND**, and the claim is true:
`008625B8` stores and returns `0xFFFFFFFC`. My decoder stopped at the first `ret`, and that path lives
**past** it. The instrument now decodes to the `int3` padding instead of to the first `ret`, and
all six claims confirm. *A decoder that stops early reports absence, and absence from a filter is not
absence from the image* — the same lesson the `rep stos` predicate taught earlier today, in a tool I had just
written to avoid it.

## 13. Runtime validation

**Evidence class: isolated original-code execution.** `diff_storage_read.py`
(SWE2-CONTRACT, 2026-09-14, `eab67079`) drives all three entries under Unicorn at their real
virtual addresses and compares return values, cursor state, destination digests and the restore
buffer byte-for-byte against the independent MSVC reconstruction: **77 commands, 100 compared
lines, 0 mismatches** — 5 distinct return values, 7 distinct buffer digests, 5 distinct cursor
values. The pass-1 gap (the NULL-argument `0` path) and the player-visible claim (a partial read
leaves a mixed buffer, advances the cursor, and reports `0`) are both exercised, not just read.

| claim | how it was observed live | date | result |
|---|---|---|---|
| all §1–§3/§5 behaviour as stated | Unicorn execution of the shipped bodies vs the reconstruction | 2026-09-14 | 100/100 lines equal |
| the boolean-not-count return discriminates | mutant returning the copied count | 2026-09-14 | killed (14 lines) |
| the `0xE240` restore bound is exact | mutant dropping the trailing `0x40` block | 2026-09-14 | killed (3 boundary digests) |
| the null-parent guard discriminates | mutant removing it — crash, every line missing | 2026-09-14 | killed |
| the `mode != 0` result write discriminates | mutant skipping the `02EAF8E0` store | 2026-09-14 | killed (2 lines) |

**Still not executed.** No shipped caller has been observed consuming a partial read — that is the
OPEN QUESTION row in §15, which no fixture can answer. A caller census would not move it either:
§4 declines to claim any caller mishandles the return, and counting callers does not execute one.

## 14. Unresolved

1. **Whether any shipped caller mishandles the `0` result** — the contract's own frontier and the
   §15 OPEN QUESTION row. *Resolved by:* a caller census that executes a real short read, not by
   this fixture.
2. **`[parent + 0x588]`'s lifetime** — **answered.** `00582860` outer arm 1
   allocates it via `002497E0(2, 0xE240)` at controller init (immediately
   before the first `00583CB0`), and outer arm 18 frees it via `003697F0`
   at controller teardown, alongside the `+0x590` sibling and the
   `02CA99B8` singleton itself (§5's tail).
3. **Subtype `0x1D`'s callees — answered.** `00580A80` releases the pending
   `+0xD8` message and transitions to `0xD` in 8 of 13 states; `00580B40` is
   the save/load dialog-result arm — `+0xEA == 0` maps `[payload+8]` to a
   transition or `+0xE0`-flag dispatch, `+0xEA != 0` resolves the scroll
   index into `+0xEF` and selects transition 6/8 by the record's `+0x57`
   bit 0; `00580CD0` releases `+0xD8` and `00581350` releases `02CA99C8`'s
   `+0xE8` resource then plays the `+0xD0`-selected chime (§5).

## 15. Evidence

> **Numbered 15, header lowercase `claim`, on purpose.** `parity_status.py` reads a
> contract's claim list from a heading that literally begins `## 15.` and keeps only a table
> whose first header cell is `claim`; miss either and it finds **zero** claims and refuses
> any harness written against this page instead of reporting a mismatch.

| claim | evidence | tier |
|---|---|---|
| the inner read returns a boolean, not a count | `00866A61 cmp r11d, r8d` / `00866A64 sete bl` | 1 |
| the wrapper multiplies that boolean by the element size | `008625A9 imul eax, ebx` | 1 |
| a short read has already written the destination and advanced the cursor | `00866A4D` writes each byte; `00866A54` increments the cursor; the shortfall is found at `00866A61` | 1 |
| the recovery restore copies 0xE240 whole-image bytes and stops before group persistent bank A | `0x1C4 * 0x80 + 0x40`; `0xE240 - 0x200` is payload `+0xE040` | 1 (static) |
| the same restore copies nothing when the parent pointer is null, and returns normally | `00583C04 cmp qword ptr [global], 0` / `je 0x583CA1` | 1 |
| the enqueue refuses a queue count of exactly 8, not `>= 8` | `0058255B cmp al, 8` / `0058255D je` in `SaveStorageQueue_EnqueueOperation` (`00582540`) | 1 |
| an empty completion underflows the queue count, and the same call's compaction then runs 255 `0x58`-stride shifts | `00582276 sub al, 1` with no zero guard; `0xFF` stored at `00582278`; loop bound `005822D7 cmp ecx, [+0x398]` | 1 |
| the underflow and the `== 8` refusal compose — `0xFF` passes the `je` and the next enqueue writes slot `0xFF` | `0058255B` equality check vs `0058256C imul rcx, rax, 0x58` unguarded slot store | 1 |
| packet kind 8's auxiliary input is not clamped | `005825DF cmp ecx, 0x10` tests `existing + aux` and resets the base only (`005825E4`); the copy loop at `00582600` runs `aux` iterations regardless | 1 |
| the queue compaction shifts `0x58`-stride entries down over the completed front | `00582290`–`005822D9` `movups` loop, `ecx < [+0x398]` bound at `005822D7` | 1 |
| the load pipeline is a 16-state dispatch on `[02B40E14]` | `003BA7BB cmp r8d, 0xF` / `003BA7BF ja`, table `0x3BA944`; arm map re-derived at §6 | 1 |
| packet-9 acceptance refuses an in-flight chain and a zero length | `003BB440 cmp [02B40E10], 0` / `je`-return-0 and `003BB44F test r9d, r9d` / `je`-return-0 | 1 |
| packet-9 arms the chain at sub-state 1 with the packet's name, dest and length | `003BB454`–`003BB46C` name copy to `02B40EC8`; `003BB470`–`003BB47E` stores `0`/`+0x120`/`+0x128` to `02B40EFC`/`02B40EF0`/`02B40EF8`; `003BB49C` sets `02B40E14` = 1 | 1 |
| the PC record is `0x210` of cursor + mode + `wchar_t[260]` path, over a shared byte vector | `0086670D` allocs `0x210`; `00866724`/`00866726` write cursor/mode; `00866730`–`0086673F` copies the wide path at `+0x08`; stream is the shared `01F44D40`/`01F44D48` pair | 1 |
| `00580840` runs `00247510` only on the state-9 success arm, parent = `[rbx+0xC0]` | `0058084C` gate `[+0xE0]&0x10`; `0058085E cmp ecx,9`; `005808C8`–`005808CF` `esi==0 && r14d==0` requires `ebp==0`; `005808D6`–`005808E6` `rcx=[rbx+0xC0]`, `edx=0x10`, `r8d=4`; `005808EE` tail `00580EB0(rbx,9,0)` | 1 (static) |
| `00580EB0` is a 15-arm state dispatcher writing `[rbx+0xE9]`; state 9 selects message `0x17` | `00580EF1 cmp eax,0xE` / `ja`, table `0x461268`; arm `00581141 mov dil,0x17`; tail `0058122B` → `00583990` → `[rbx+0xD8]` | 1 (static) |
| `00583990` resolves result messages through `00D23DA0`, a `{id,kind}` table clamped to 32 entries | `005839D9 lea r15,[00D23DA0]`; `005839E0 cmp ecx,0x1F` / `cmovb`; entry `0x17` = `{0x87F, kind 0}`; kinds 1–4 branch at `00583A19`–`00583A28` | 1 (static) |
| `00580840` is re-entered as the completion callback of packets the machine itself enqueues | arms 8 (`0058109E`–`0058111E`) and 0xB (`005811AA`–`005811DF`) build `{kind, cb=00580840}` records and call `00582540` | 1 (static) |
| subtype `0x8001` stamps the selected slot byte at `[02CA99B8]+0x598` and the packet's `+0xEB` | `00580405 cmp rax,0x8001` / `je 00580508`; `0058050C movzx edi,byte[rax+rcx+0xEF]`; `0058052A mov byte[rcx+0x598],dil`; `0058053A mov byte[rbx+0xEB],dil`; `00580537 and ecx,~6` | 1 (static) |
| `0057FE80` is a two-level dispatcher — outer `dword[msg]−1` bounded at `0x11`, subtype select nested in outer arm 12 | `0057FE8D dec eax` / `0057FE92 cmp eax,0x11` / `ja 005807AC`, table `0x4607B8`; nested select at `00580401 mov rax,[rdx+8]` | 1 (static) |
| subtype `0x12` clears `+0xD0` only when `qword[msg+0x10] == 0xA` | `005804E8 cmp qword[rdx+0x10],0xA` / `jne bail`; `005804F3 mov qword[rcx+0xD0],0` | 1 (static) |
| subtype `0x1D` requires `+0xE0 & 0x10` clear and re-dispatches on `dword[[msg+0x10]]` to `00580A80`/`00580B40`/`00580CD0` | `00580495 test byte[rcx+0xE0],0x10` / `jne bail`; `005804A8 cmp eax,3` → `00580A80`, `005804BC cmp eax,0xD` → `00580B40`, `005804D0 cmp eax,0xF` → `00580CD0` | 1 (static) |
| subtype `0x8000` binds `edi*0xA0 + [+0x1C0]` into `+0xC8` when `*003BB3E0(slot) == 2`, else clears `[+0xC8]+0x100` | `00580437 movzx edi,byte[rax+rcx+0xEF]`; `0058044D cmp dword[rax],2` → `0057EFE0` at `00580461`; else `0058047B mov qword[rcx+0x100],0` / `00247870` | 1 (static) |
| `0x8001`'s tail derives `r8b` ∈ {7,8,9,0xA,0xFF} from `*info`/`[info+4]`/`+0xED`, then transitions to 1 or 0xE | `00580555`–`0058059D` select on `*info−2`; `005805B7 cmp r8b,0xFF` → `00580EB0(rbx,1)` else `00580EB0(rbx,0xE)` | 1 (static) |
| subtype `0x8002` arms `+0xE0` bit 4 and calls `00244F00(rbx)` | `00580769 test rbx,rbx`; `0058076E or dword[rcx+0xE0],0x10`; `00580775 call 00244F00` | 1 (static) |
| subtypes `0x8100`–`0x8102` re-dispatch on queue state `+0xE9 − 2` through table `0x460800` | `005805E6 cmp rax,0x8002` / `je 00580769`; `005805F2 add rax,-0x8100` / `cmp 2` / `ja bail`; `00580633 add r8d,-2` / `cmp 0xC` / `ja`, table `0x460800` | 1 (static) |
| the `0x8100`–`0x8102` prelude sets `[02CA99E0]+0xCC = 4`, clears `+0xD8`, and runs `0057ED40` | `00580611 mov dword[rax+0xCC],4`; `0058061B mov qword[rcx+0xD8],0`; `00580626 call 0057ED40` | 1 (static) |
| `0057ED40` collapses `02CA99C0` to head-only when `+0xDC` bit 0 is set, else empties it | `0057ED61 cmp byte[rax+0x398],1` / `jb`; `0057ED70 test dl,1` → `0057ED75 or edx,2` / `+0x398=1`, else `0057ED8D` `+0x398=0` / `+0xCC=0`; `0057ED9B` clears `02CA99D8+0xC0` low bits | 1 (static) |
| outer ids 15 and 18 notify `+0xC0` through `00247510` with messages `0xF`/`0x12` | `00580784 mov edx,0xF` / `0058078B mov edx,0x12` → shared `00580790`: `rcx=[+0xC0]`, `r8d=4`, `call 00247510` | 1 (static) |
| outer id 14 selects dialog `0xC82`/`0xC84`/`0xC86` by `+0xEA` and `00394450()==3` | `0058030F cmp byte[rcx+0xEA],0` → `0xC82`; `00580324 call 00394450` / `cmp al,3` → `cmove edi,0xC86` else `0xC84`; `002F9860` → `00291D80` → `002470D0` | 1 (static) |
| `00582860` is the controller's own dispatcher — outer `dword[msg]−1` bounded at `0x12`, table `0x462F54` | `00582889 dec eax` / `0058288E cmp eax,0x12` / `ja 00582F24`, table `0x462F54` | 1 (static) |
| `+0x588` is allocated at controller init via `002497E0(2, 0xE240)`, exactly the backup size | `005828D1 mov edx,0xE240` / `0058292E call 002497E0` / `00582938 mov [rbx+0x588],rax`; sibling `+0x590 = 002497E0(2, 0x7D00)` at `00582942`/`00582949`, memset `00861EC0` at `00582959`; first `00583CB0` at `00582975` | 1 (static) |
| `+0x588` is freed at controller teardown via `003697F0` and nulled, with `+0x590` and the singleton | `00582EC7`–`00582EDA` `rcx=[rbx+0x588]` / `call 003697F0` / `mov [rbx+0x588],0`; same for `+0x590` at `00582EE1`–`00582EF2`; `00582F00 mov [02CA99B8],0` | 1 (static) |
| `00582860` outer arm 18 is the teardown: persistence restore, normalize/reseed, sub-teardown, frees, singleton clear | `00582E81 test [rbx+0xC4],0x10` gate → `005843E0` at `00582EA2`; `00584210` at `00582EBA`; `00582FC0` at `00582EC2`; frees `00582ED5`/`00582EED`; `002E1CA0(1,0x15)` at `00582F1B` mirrors `002E1C20(1,0x15)` at `005828B4` | 1 (static) |
| subtype `0x1D` payload-3 arm releases `+0xD8` and transitions to `0xD` in 8 of 13 queue states | `00580A92 cmp dword[rdx+8],0` / `je bail`; `00580A98 call 0057ED40`; table `0x460B0C`; live arms → `00580AC5`: `00244F00(+0xD8)` / `[02CA99E0]+0xCC=4` / `+0xD8=0` / `00580EB0(rbx,0xD)` | 1 (static) |
| subtype `0x1D` payload-`0xD` arm's `+0xEA==0` path maps `[payload+8]` to a transition or `+0xE0`-flag dispatch | `00580B5F test edx,edx` → `+0xE0` bits 3/1 select transition 4/3/2; `edx==1` → `0xA`; `==3` → `r8=1`; `==4` → `r8=0`; else `r8=3`, all `r9b=0xD` | 1 (static) |
| `00580B40`'s `+0xEA!=0` path computes `(word[+0xF2]+word[+0xF4])*byte[+0xEC]+sbyte[+0xEE]+sbyte[+0xED]` and indexes `+0xEF` | `00580C30`–`00580C5E`; `rdi = byte[+0xEF+idx]*0xA0 + [+0x1C0]`; `[payload+8]==0` → `00394450()==3` or `byte[rdi+0x57]&1` selects transition 8 or 6 (`00580C9E`–`00580CA7`) | 1 (static) |
| subtype `0x1D` payload-`0xF` arm releases `+0xD8` then `00581350` releases `02CA99C8`'s `+0xE8` resource and plays a `+0xD0`-selected chime | `00580CEC call 00244F00`; `00581368 test byte[rbx+0xCC],1` → `0024A1A0(+0xE8)` / `+0xE8=-1`; `+0xD0` ≤1 or 4 → `00249C60(0x27)`, 2–3 → `00249C60(0x43)` | 1 (static) |
| `00582B2C` is the controller's nested subtype dispatcher — `qword[msg+8]` selects `0xF`/`0x10`/`0x12`/`0x1D`/`>0x1D`, and `0x12` re-dispatches `qword[msg+0x10]` through table `0x462FA0` | `00582B30 cmp rax,0x1D` / `jg 00582D41` / `je 00582D25`; `sub 0xF` → `00582CF2`; `sub 1` → `00582CB3`; `cmp 2` falls to `00582B5E`: `add rax,-2` / `cmp 7` / `ja`, table `0x462FA0` = {`00582B7C`,`00582BC7`,`00582C38`,`00582C83`,bail,`00582C93`,bail,`00582CA3`} | 1 (static) |
| the `0x12` payload arms release or clear one controller field apiece | `00582B7C` clears `+0xC8` and releases `02CA99D0`/`02CA99D8`/`02CA99C0`/`rbx` via `00244F00`; `00582BC7` clears `+0xD0`, gated `+0xC4&0x10`/`+0xC0==3` → `0057ED40`; `00582C38` clears `+0xD8`, `+0xC0=1`; `00582C83`/`00582C93`/`00582CA3` clear `+0xE0`/`+0xE8`/`+0xF8`; payloads 6/8 bail | 1 (static) |
| the `0x8001` arm posts two packets — `+0xD0` (cb `00581490`) and `+0xF8` (cb `0057F360`) — then resolves message `0xE` into `+0xF0` and enters state 2 | `00582D8B` requires `qword[msg+0x10]==2`; `00244F50(0x110,00581490)` at `00582DE2` → `+0xD0`; `00244F50(0xF0,0057F360)` at `00582E46` → `+0xF8` carrying `rbx`/`+0xC1`/`+0x590`; `005819A0(+0xC1==1)` at `00582E5C`; `00583990(0xE,rbx)` at `00582E67` → `+0xF0`; `00582E75 mov byte[rbx+0xC0],2` | 1 (static) |
| `00583040` self-posts into the queue dispatcher — when `+0xC1==0` it builds `+0xD8` = `00244F50(0x1C8, cb=0057FE80)` | `005831C5 lea rdx,[0057FE80]` / `ecx=0x1C8` / `call 00244F50` → `[rsi+0xD8]` at `0058320A`; sibling `+0xE0` = `00244F50(0x108, cb=0057EDB0)` at `00583188`–`005831A8`; `+0xC0=4`; else arm `0058321A` runs `00583990(edi)` + `0057EC60(rsi,1)`, `+0xC0=3` | 1 (static) |
| `00583040`'s nested dispatch maps `dword[msg+8]` to `{0,1,2,3,0xFF}` — `1` selects `2` or `0xFF` by `+0xC1` | `00583076`–`005830C1`: `0`→0; `1`→`edi=0xFF` `cmovne edi,2` on `+0xC1`, `ebp=1`, `bl=(+0xC1==0)`; `3`→1; `4`→0; else 3; shared tail `00583116` releases `+0xF0`, `[02CA99E0]+0xCC=4`, `00581350(bl==0)` | 1 (static) |
| `005829C0` is the suspend path: it builds a `0x720` record when `02CA99C0==0` and arms `+0xC4` bit 1 | `003946B0(+0x108,6)` at `005829D0`; `02CA99C0` test at `005829D5` → `00244F50(0x720,005823B0)` at `005829EE`; `00394700(0)` / `00247930(0x64)` / `00244960(0208EA28)` / `00247870(0)`; `00582A23 or dword[rbx+0xC4],2` | 1 (static) |
| `00582AE9` opens dialog `0x870`/`0x871` by `+0xC1` and self-posts `0x8001` | `00582AE9 cmp byte[rbx+0xC1],0` → `ecx=0x870/0x871`; `002F9860` at `00582AFC`, `002CA150` at `00582B06`; `00247510(rbx,0x8001,2)` at `00582B19`; `00582B20 mov byte[rbx+0xC0],1` | 1 (static) |
| `00581310` releases its argument and, when controller `+0xC4` bit 3 is set, runs `002CC9B0`→`002CC9C0` | `00244F00` at `00581314`; `00291D40`/`002CA110` at `00581319`/`0058131E`; `test byte[rax+0xC4],8` on `02CA99B8` at `0058132A` → `002CC9B0` tail `002CC9C0` | 1 (static) |
| `005832B0` builds the `"PS2D"` submission descriptor — memset, magic stamp, bounds, path formatting, three `005837F0` calls | `00861EC0` memset at `00583302`; `"PS2D"` at `00D23F10` read `00583307`; slot `< 0xC8` at `0058330D`, `0x3C` bounds `00583341`/`0058334D`; `00254A10` gate at `00583358`; `0017D2E0` formats; `005837F0` at `00583644`/`00583675`/`005836A5` | 1 (static) |
| `00583700`/`005837F0` write the slot directory and asset names into `controller+0x128`, gated on `02CA99B8` | `00583700`: `"%s%03d"` (`009153E4`) of `003935C0` base + slot byte, `"/%s"` (`00D23EE4`) prefix when flag arg set; `005837F0`: kind 0 → `"icon.sys"` (`00D23EC8`), kind 1 → `"%s%03d"` ≤ `0x40`, ~~kinds 2/3~~ kinds 2, 3 and 4 *(corrected 2026-10-02, OPUS: checked at `0058383C`–`0058384E`)* → `"static.ico"` (`00D23ED8`); both `cmp [02CA99B8],0` bail | 1 (static) |
| `00583930` posts `00244F50(0x5A0, cb=00582860)` carrying `{arg3, arg1!=0, arg2!=0}`; `00583920` returns `[02CA99E8]`; `00583260` posts `00244F50(0x178, cb=0057E4D0)` | `0058395A lea rdx,[00582860]` / `ecx=0x5A0` / `call 00244F50` at `00583974`, payload built `00583946`–`0058396F`; `00583920 mov eax,[02CA99E8]` / `ret`; `00583288 lea rdx,[0057E4D0]` / `ecx=0x178` / `call 00244F50` at `00583295` | 1 (static) |
| the `005843E0`/`00584210` admission split is `(00394450()==3)` vs `byte[+0x57]&1`, not a `+0x18`/`+0xC4` bit-4 | `00584236 cmp al,3`/`0058423A movzx eax,[rdi+0x57]`/`and eax,1` select stash (`00584255`–`005842DF`) vs restore (`005842F9`–`00584393`); `00584404`/`00584410` same predicates in `005843E0`; `+0x18` is payload, `+0xC4` untouched | 1 (static) |
| `00583CB0` backs up `0xE240` bytes from the active header to `[[02CA99B8]+0x588]+0x80` | `00583CCE mov edx,0x1C4`; `0x80`-stride `movups` loop `00583CE0`–`00583D31` plus `0x40` tail `00583D33`–`00583D4D`; `00583C00` is the exact mirror | 1 (static) |
| `00582040` admits the front packet through a 13-arm dispatch on `dword[+0xD8]` (table `0x46220C`); arm 1 alone copies packet `+0xE0`/`+0xE8` into queue `+0xC0`/`+0xC8`, so only a kind-1 packet carries its own completion callback and token | gates at `0058206D` (`[+0x398]==0` → 0) and `00582076` (`+0xDC` bit 0 → 0); table load `00582092`; arm 1 copy `0058209E`–`005820B2`; every live arm joins `005820BD` `or [+0xDC],1` | 1 (static) |
| `00582240` remaps the result two-stage — `dil` defaults to 0 for kinds 1–2 else `003BB420()`, `0017E470()` returns the stored status `[001D50D0()+0x10DC]`, and `(status, kind)` fix-ups override `dil` (status 1 or 3 with kind 7/9 → 8; status 2 with kind ≠4 → 3); `dil==4` zeroes 25 bytes at controller `+0x568`..`+0x580` | `005822F6`–`0058230E` default select; `0017E470` body is `mov eax,[001D50D0()+0x10DC]`; fix-ups `00582313`–`00582343`; `rbp` xor'd at `00582264` and never reloaded before the `00582357`–`0058236C` stores | 1 (static) |
| the completion callback runs `+0xC0(kind, dil, +0xC8)` only when `+0xDC` bit 1 is clear | `r8d = ~([+0xDC]>>1) & 1` at `0058226C`–`00582272`; `005822ED` skips remap+call when set; `0058237D` also skips a null `+0xC0`; call at `0058238E` | 1 (static) |
| **whether any shipped caller mishandles either** | **not established** | none |

## 16. Parity plan

`diff_storage_read.py` is the harness: a command script drives NEW/SEEK/READ/WRAP/RESTORE/STATE/DEST
operations against both sides — the shipped bodies under Unicorn at `00866A00`/`00862590`/`00583C00`
with the real globals mapped (`01F44D40`/`01F44D48`/`02EAF8E8`/`02EAF8E0`/`02CA99B8` and the active
buffer `02164280`), and `storage_read_driver.c` over the MSVC reconstruction — then compares every
emitted state line.

**Dimensions covered:** `CONTRACT` (derived COVERED — every testable §15 row exercised), `CALCULATION`
(the boolean×count product and the `−4` arm), `STATE-TRANSITION` (cursor compared after every call,
resume-on-retry, result global on both wrapper arms), `EDGE-CASE` (count 0/negative, null cursor and
dest, cursor at/past end, exact boundary, null parent, `0xE240` canary).

**Not covered, recorded:** `INTEGRATION` and `FULL-SUBSYSTEM` — no shipped caller or pipeline stage
participates; `TIMING` — the load pipeline's scheduling is ASTRA's question, not measured here;
`SERIALIZATION` — the container format is the sibling contract's, not this one's. `RNG` is `N/A` —
no stream is drawn.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

**Presentation — CLIENT.** The 95-byte `00247510` is also called by two Presentation bodies, of 1,307 and 2,882 bytes.
It is a shared completion helper rather than a save-only one. Which screens those bodies drive is not read here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**PlatformOnlineAchievements — SERVICE.** `00584210` on this page calls `FUN_00316810`, owned by that layer. What it reaches is an achievement-table scan over `01EED078` against the `.rdata` table at `00D10460`, bounded at `0x7FFE`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — SERVICE.** `005843E0` on this page calls `SpawnKeep_RestorePersistenceBank`, owned by that layer. What it reaches is the bank restore, and it gives the bank a width: ~~**`0x128` bytes**~~ **`0x9400` bytes** (`0x128` passes of `0x80`) *(corrected 2026-10-02, OPUS: `00233560` `mov r8d, 0x128` counts passes; the serializer `00233448` / `0023345D` copies the same)* are copied from the caller's `+0x10` into `[0208E698] + 0x80`, in `0x80`-byte steps; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — SERVICE (4 edges through 3 of this page's functions).** `00580EB0`, `00581350` and `00583990` call the Audio-filed `00249C60`, and `00581350` additionally calls `0024A1A0` — both read from the shipping bytes: each is a guarded call-through shim gated on `dword[02091098]`, forwarding to `002DF220`/`002DF0F0` or returning `-1`. The transition machine resolves its result messages through that layer's fetch helpers; the crossing is those calls, not a shared responsibility. Read from the shipping bytes 2026-09-15 (SWE2).

**UI — CLIENT (9 edges through 4 of this page's functions).** The UI layer reaches this page at `00247510`, `0057FE80`, `00862590`, `008625D0`. `FUN_003ba7b0` is the worked example, read in full - it is a 402-byte state machine on `[02B40E14]`, bounded at **`0xF`** into a sixteen-arm jump table, whose first arm resets the state to 1 and clears `[02B40EC0]`; **1 of the 8 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 165).** `00249210` — the queue helper this page's `003BA680` machine shares — calls `0032E400`/`0032E620` on that layer and is itself reached from `00249180`/`00249320`; the save-storage machine rides the resource queue, not a shared responsibility. Edge detail from `edges.tsv`.

## Interior citation — frontier hub `00247510` (2026-09-17, SWE2-EC7)

`00247510` — 95 B, 51 frontier callers at census; the body §1.4 calls "the callback" on the
state-9 success arm (`00247510([rbx+0xC0], 0x10, 4)`). Interior verified:
[`00247547`](../_index/ADDRESS-INDEX.md) is `call rax` — the body is a **guarded method-pointer
invoker**: it builds a 24-byte stack record `{dword 0xC; qword arg2; qword arg3}` at
`[rsp+0x20]`, then calls `*[rcx]` with `(rcx, &record)` if both `rcx` and the stored pointer are
non-null, else returns `eax=0`. Cookie-protected both arms (`00808C40`). The `0xC` is a constant
the invoker stamps on every call — a message kind tag, not caller data.

NOT claimed: the callback's contract (that lives at each installation site) — only the guard
shape and the record layout `{+0x00: dword 0xC, +0x08: rdx, +0x10: r8}` are measured.


### Interior citation — frontier hub `002497E0` (2026-09-18, SWE2-EC7)

`002497E0` — 42 B, 6 callers: the scoped arena wrapper named above —
`0036C1D0(0xC)` acquires the section, `0036A100(arg)` runs the allocation,
`0036C140` releases at [`002497ED`](../_index/ADDRESS-INDEX.md). The
enter/call/leave shape behind the `+0x588`/`+0x590` arena allocs.

*Crossing note (SWE2-EC7, 2026-09-18):* `00283270`, the widget-bind step the
id-1 arm calls, also has a CombatAI callee edge and is itself called from
the Party layer — the crossings are those edges, not a shared
responsibility.
## SWE2-EC7-20 update (2026-09-18) — `005837F0` asset-name window + `00581350` transition tail

`005837F0` (304 B) is the `SavePath_BuildSlotAssetName` builder this contract
names (`005837F0(1, self+EB, 1)`, three calls, one per asset name): a null
`[02CA99B8]` singleton returns 0 (`0058380F`..`00583821`); else `003935C0`
stamps the `"FFXII_"` prefix into a 32-byte stack buffer (`00583826`..`00583830`)
and `cl` selects the tail — `0` → `"icon.sys"` copied from `00D23EC8`
(`005838AB`..`005838BA`), `1` → `0017D2E0` `"%s%03d"` formats the prefix plus
`dil` (`00583871`..`005838A4`, bounded under 0x40), `2`/`3`/`4` → `"static.ico"`
from `00D23ED8` (`00583850`..`0058386F`). The composed name is then copied
byte-wise into the singleton's `+0x128` field (`005838C4`..`005838FD`).
Cookie-guarded (`005838FF`..`0058390A`). Callers `0057F280`/`00580EB0`/`00581DA0`/
`005832B0` — the slot-asset name build this contract drives.

`00581350` (130 B) is the `02CA99C8`-singleton state release: `rbx =
[02CA99C8]` null exits (`0058135A`..`00581366`); when `+0xCC` bit 0 is set and
`+0xE8 != -1` it calls `0024A1A0(+0xE8)`, resets `+0xE8 = -1`, and clears the
bit (`00581368`..`00581392`). With `edi==0` it dispatches on the `+0xD0` state
byte — `1` or `4` → `00249C60(0x27)`, `2`/`3` → `jmp 00249C60(0x43)`
(`00581396`..`005813CD`). The clear-and-notify close the transition state
machine ends on. Callers `00580840`/`00580CD0`/`00583040` — the SaveLoad controller
transition path this contract names.

## SWE2-EC7-21 update (2026-09-18) — `003935C0` cookie-check tail fragment

`003935C0` (59 B) is the `"FFXII_"` prefix stamper the read-side bodies share:
`edx <= 6` returns the shared `01CEB638` empty string (`003935C9`..`003935DA`);
else `call [008C2F70]` copies the six-byte `"FFXII_"` constant (`00D113D4`) into
`rcx` (`003935DB`..`003935E8`), `[rbx+6] = 0` terminates (`003935F1`), and
`rax=rbx` returns the buffer. The name prefix `005837F0`'s `"%s%03d"` format
builds on. Callers `0017F3B0`/`00580CD0`/`005832B0` zone — the read-completion
helpers this contract names.

## SWE2-EC7-23 update (2026-09-18) — `003BB600`/`003BB3E0` slot bank + `003949B0` record builder

`003BB600` (34 B) is the bounded slot writer for the `[02B407C0]` pointer bank:
`ecx <= 0xC7` gate, `[rdx]` stored at `bank + rcx*8`, returns 1 — the 200-slot
registry's write half. Interior anchor `003BB615`.

`003BB3E0` (26 B) is the read half: same `0xC7` bound, returns
`&bank[rcx]` — the slot-address getter the registry consumers share. Interior
anchor `003BB3F2`.

`003949B0` (218 B) is the message-record builder the read-completion callers
drive: `[0208EA28]` global into the five-qword stack record (`[rbp-0x60..0x40]`
staged via `movups`/`movsd`), `byte[r8+0x14] & 4` setting `edx |= 0x20` mode
bit, `[r9]` tail fetch — the packet assembly the `0057xxxx`/`0058xxxx`
storage-side callers submit. Interior anchor `003949EA` (the record copy).

## SWE2-EC7-29 update (2026-09-18) — `002D3900` display-word tick

`002D3900` (324 B) is the per-frame tick over the display words the id-14
row names: `02F97368`/`02F9736A`/`02F9736C` load the current triple and
`0209E65C` counts calls against `01E0CF88` (=2) — only every other call
runs `001E0A10()` for a signed delta. `|delta| >= 01E0CF84` (=3) with
`word[rsi+0xE8] <= 0xC` reduces the step to `delta / |delta|` (±1);
positive arms bit `0x10`, negative bit `0x40`, on `ebp`/`r14d`. Each of
`|delta|` steps runs `002D0580(rsi, delta)` then
`002D3BA0(rsi, ebp, r14, r12, 0, delta)` then `002D4F10(rsi, delta)` —
either non-zero aborts the loop; the no-delta path runs `002D3BA0` once
with the raw triple. Interior anchor `002D39E2` (the in-loop
`call 002D3BA0` commit).

## SWE2-EC7-29 update (2026-09-18) — `002CA150` `+0x2D8` continuation swap

`002CA150` (154 B) is the `[0209AC30]+0x2D8` continuation swap the
suspend sequence runs: an existing `+0x2D8` object is released through
`00244F00` and the slot cleared, then `00244F50(0x140, 002CA1F0)` builds
the replacement — its `002CA1F0` init arm (kind 1) resolves a 4-arg
`002432B0` geometry into `+0x98..+0x9E`, runs `00247570(00916F80)`,
`00254F30`-copies `0x80` bytes to `+0xC0`, and publishes `+0x18`/`+0x28`
(=0.9f)/`+0x20` (a `0020E620()` id); kind `0x12` returns 0; other kinds
fall to `005C5230`. The new object stores to `+0x2D8` and is submitted
`00246AD0(0208EA28, obj)`. Interior anchor `002CA1B6` (the
`call 00244F50` allocate).

## SWE2-EC7-35 update (2026-09-19) - `00581490`

`00581490` (824 B) is the storage completion record body - `02CA99C8` state, `00247510`/`00225580` pairs plus `00581930`/`00394720`/`00394690`/`002DD7E0`/`0029F4B0`. Interior anchor `005814D9` (a `00247510` call).

## SWE2-EC7-36 update (2026-09-19) - `0057EFE0`

`0057EFE0` (663 B) is a storage completion body - `0029FB50`/`00247870` quintuples, `00394660` triple, `0020E620` pair plus `0057E6D0`. Interior anchor `0057F00C` (a `0029FB50` call).

## SWE2-EC7-46 update (2026-09-19) - `002CA1F0`

`002CA1F0` (229 B) is a body - `0020E620`/`002432B0`/`00247570`/`00254F30`. Interior anchor `002CA23F` (a `0020E620` call).

## SWE2-EC7-46 update (2026-09-19) - `0057F280`

`0057F280` (224 B) is a body - `003BB3E0`/`00582540`/`005837F0`. Interior anchor `0057F2A2` (a `003BB3E0` call).

## SWE2-EC7-47 update (2026-09-19) - `0057EC60`

`0057EC60` (217 B) is a body - `00582540` single call. Interior anchor `0057ED00` (the `00582540` call).

## SWE2-EC7-51 update (2026-09-19) - `005813E0`

`005813E0` (173 B) is a body - `00581930` single call. Interior anchor `00581473` (the `00581930` call).

## SWE2-EC7-56 update (2026-09-19) - `002D0580`

`002D0580` (195 B) is the `002D0580(rsi, delta)` storage-read step the contract names - `001E0E30` single call plus `0209E660`. Interior anchor `002D0596` (a `001E0E30` call).


## SWE2-EC7-71 update (2026-09-19) - `002D3BA0` list-input dispatcher measured

Measured on `the-map-screens-and-their-shared-map-data.md` (PARTIAL -
non-bearing); mirrored here where the CONTRACT names its call site.

`002D3BA0` (1,904 B) measured: it reads the `+0xE0`/`+0xE4` flag words,
runs the `(flags & 0xF000) - 1` six-arm jump table at `02ED4310`
(`00120000` + `0x1B4310`), each arm pairing `002D4A40`/`002D1870`/
`00368860` with escalating `edi` op codes, and carries the
`+0x10B`/`+0x10C` repeat throttle against `0208F574`, the `+0xE4` bit-13
commit, and helpers `002D0A20`/`002D1B10`/`002D1DB0`/`002D2D40`/
`002D4330`/`002445C0`/`0035F110`.
Interior anchor `002D3E2B` (the `jmp rcx` table dispatch).

## SWE2-EC7-80 update (2026-09-20) - `008625D0` + `00581930` + `00581860` measured

`008625D0` (33 B) is ~~the conditional teardown~~ the seek *(corrected 2026-10-02, OPUS: checked at `008625D0`–`008625F0`; `00866A80` writes the cursor absolute, relative or from the end and bounds-checks it — the callee/caller note, "the sibling **seek**")* the `003BA7B0` caller
runs: `ecx == 0` ~~releases~~ repositions `[02EAF8E8]` through `00866A80`; either way
`dword[02EAF8E0]` is zeroed and 0 returns.
Interior anchor `008625D8` (the `02EAF8E8` load).

`00581930` (110 B) is the counter commit `00581860` tails into:
`002DD7E0(0xD1)` seeds the stack dword; when `rcx` is live,
`edx` is stored to `[rcx+0xD8]` and `00225580([rcx+0xF0], edx)` runs;
`edx >= [rcx+0xD4]` re-reads via `002DD7E0(0xD2)`; then
`0029F480([rcx+0xF0], &val, 1)` commits.
Interior anchor `00581944` (the `002DD7E0` fetch).

`00581860` (196 B) is the scaled-duration setter on `[02CA99C8]`:
`ecx == -1` keeps `edx = [rbx+0xD4]`, else `edx = ecx*10`; a request
`<= [rbx+0xD8]` early-outs, else `edx` clamps to `+0xD4`, `+0xC8` bit0
clears, `edx` commits to `+0xDC`. With `r10d` nonzero it fills
`+0x100`/`+0x108` = old `+0xD8`, `+0x104` = span, `+0xF8`/`+0x10C` = 0
and `+0xFC` = `max(1, (span*r10d)/delta)`; with `r10d == 0` it calls
`00581930` and zeroes `+0xFC`.
Interior anchor `00581899` (the `+0xD4` clamp).

## SWE2-EC7-81 update (2026-09-20) - `0029F480` dual-slot dword store measured

`0029F480` (46 B) is the `+0x88`/`+0x64` pair writer `00581930`
calls: `r8d == 0` copies `dword[rdx]` to both slots, `r8d == 1` to
`+0x88` only, `r8d == 2` to `+0x64` only; any other `r8d` writes
nothing.
Interior anchor `0029F491` (the `+0x64` store arm).

## SWE2-EC7-89 update (2026-09-20) - `003BB9B0` + `003BB740` measured

`003BB9B0` (174 B) is ~~the element-array install the read~~
~~completion runs once~~ the write submission — queue kind 8's arm (`00582180`) and the autosave's call (`0057E490`) *(corrected 2026-10-02, OPUS: it arms `02B40E1C` = 2, the write command; how-a-manual-save-is-committed.md, kind 8 → `003BB9B0`)* (`[02B40E10]` gates it): `r8d` is clamped to
five, written to `02B40FE0`, and that many 0x38-stride records
copy from `rdx` into `02B40EC8`; `02B40E1C` is armed to 2, the
`02B40EC0`/`02B40E18`/`02B40FE4` counters are zeroed,
`02B40E10` is set, and `003BAEB0` runs - returning 1.
Interior anchor `003BB9F0` (the 0x38-stride copy loop).

`003BB740` (69 B) is the string arm of the same install: `rcx` is
strcpy'd into `02B4055C`, `02B40E10` is set, the three counters
are zeroed, and the body tails `003BAC90`.
Interior anchor `003BB750` (the copy loop).

## SWE2-EC7-90 update (2026-09-20) - `003BAEB0` + `003BAC90` measured

`003BAEB0` (803 B) is the `02B40E14` state pump ~~the completion~~
~~install arms~~ the write submissions arm, the write worker *(corrected 2026-10-02, OPUS: `003BB920` and `003BB9B0` arm `02B40E1C` = 2 and run it)*: an 18-arm jump table (`02B40E14` states 0-0x11)
drives the `02B40EC8` 0x38-stride records through `008620D0`/
`008624D0`/`008625D0`/`00862620` buffer ops indexed by
`02B40FE4`, accumulates `0017D270`-timed `00583920`-gated
thresholds at `02B4112C`, and lands in terminal states 9/3/6/7/
0xF/0xA/4 with `02B40E10` cleared on completion or failure.
Interior anchor `003BAF10` (the jump-table read).

`003BAC90` (448 B) is the sibling pump `003BB740` tails into: a
21-arm jump table (`02B40E14` states 0-0x14) drives
`003BA320`/`003BA3E0` per `02B40554`-indexed `02B41160` records
(0x40 stride), submits through `00862490` with the `02B40E0C`/
`02B41130` outs, retries up to 4 on `02B40EC0`, and exits via
states 1/2/3/9/0x14.
Interior anchor `003BACE0` (the jump-table read).

## SWE2-EC7-92 update (2026-09-20) - `00394850` + `00394800` + `00393460` measured

`00394850` (83 B) is the two-level record-deref trampoline the
completion path tails into `0029F6E0`: a non-null `rcx` follows
`[rax+0x60]`'s pointer table at index `edx`, the entry must read
`[rcx+8] & 0x3C == 4`, a non-null `[rcx+0x18]` follows a second
`+0x60` table at index `r8d`, then `[rcx]`'s record supplies
`[rdx+0x14]` and the `[rsp+0x28]`/`[rsp+0x30]` argument pair is swapped
before the tail jump.
Interior anchor `00394866` (the `[rcx+8]` kind read).

`00394800` (72 B) is the single-level sibling: same `+0x60` table
deref at index `edx`, same `& 0x3C == 4` kind gate, but the second hop
takes `[rax]`'s first entry and tails `0029F6E0` with `[rdx+0x14]` in
`r9d`.
Interior anchor `00394819` (the `[rcx+8]` kind read).

`00393460` (130 B) is the `002493D0` loop builder the `00582790`
caller runs: `r9d` iterations walk an `r8` array of 0x18-stride
entries, each call is `002493D0(rcx, 7, 2, [rbx-8], 2)` with the
result appended at `rdi`, and the entry's `+0x10` dword lands in the
new record at `+0x40`.
Interior anchor `003934B2` (the `002493D0` call).

## SWE2-EC7-93 update (2026-09-20) - `002493D0` record builder measured

`002493D0` (57 B) is the two-call builder the `00393460` loop calls
per entry: `00249210` allocates the record, `0024A4E0([rsp+0x60],
[rsp+0x68])` resolves the caller's argument pair, and the results land
at `+0x18` (the resolved value) and `+0x10` (a fixed rip-relative
function pointer) - the record shape the loop then tags at `+0x40`.
Interior anchor `002493EF` (the `0024A4E0` call).

## SWE2-EC7-99 update (2026-09-20) - `002D4F10` + `002D1870` measured

`002D4F10` (54 B) is the scroll-boundary probe `002D3900`
and `002D3A50` call: `word[+0xF4] == 0` admits a positive
`edx` step, `word[+0xF4] == word[+0xF0] - 1` admits a
negative one - the first/last-page edge test the scroll
helpers consult before moving the cursor.
Interior anchor `002D4F2D` (the `+0xF0` read).

`002D1870` (556 B) is the masked-code measure `002D3BA0`
and `002D4A40` call: `edx & 0xFFFF0FFF` strips the flag
nibbles, `code - 2` bounds a nine-arm jump table at
`002D1A9C`, and the arms mix `0035F0F0`/`0035F110` metric
queries with page-width formulas - `word[+0x100] * |x|`
and `word[+0xEA] * |y|` scaled by twelfths (the
`0x2AAAAAAB` multiply) and clamped to 8/12/0x14, the
`0x3000`/`0xC000` flag bits picking which axis the
`+0xC0` object's `+0x9E`/`+0x9C` words bound - the
per-class extent estimate the text/layout arms share.
Interior anchor `002D18BB` (the jump-table load).

## SWE2-EC7-100 update (2026-09-20) - `0035F110` measured

`0035F110` (22 B) is the indexed byte fetch `002D1870` and
`002D3BA0` call: `byte[ecx * 0x294 + 022CBE95]` - the
`0x294`-stride metric lookup the measure arms run per row.
Interior anchor `0035F121` (the byte load).

## SWE2-EC7-102 update (2026-09-20) - `0028FD00` measured

`0028FD00` (71 B) is the null-keyed forward pair
`00291D80` and `002BA700` call on the
`[0209BE80] + 0x8FA0` record: a null `rdx` runs
`002BE020` and returns 1; otherwise it tail-jumps
`002BE110` with the argument tuple forwarded - the
query-versus-command split the storage-completion
arms share. A null root returns 0.
Interior anchor `0028FD29` (the `002BE020`
call).

## SWE2-EC7-112 update (2026-09-20) - `00866A80` measured

`00866A80` (66 B) is the
mode-dispatched position
write `008625D0` runs:
`r8d == 0` writes `edx`
outright, `r8d == 1` adds
`edx` to `dword[rcx]`, `r8d
== 2` reseats to
`(01F44D48 - 01F44D40) +
edx`, any other mode keeps
the old value; the result is
then bounds-checked against
`01F44D48 - 01F44D40` and
commits to `dword[rcx]` with
return 0, or answers -1
without touching the field.
The two globals bound the
window.
Interior anchor `00866AB0`
(the window compare).

## SWE2-EC7-113 update (2026-09-21) - `008656B0` measured

`008656B0` (109 B) is the
wide-string assign
`00866200` runs on its
record fields: the source
pointer in `r8` is scanned
for its NUL-terminated
length (zero when
`word[r8] == 0`), then
`00865FF0` runs on the
pair, `qword[+0x18] = 7`
(SSO capacity) and
`qword[+0x10] = 0` (size)
relatch, `word[+0]` zeroes,
and `00865E30` completes
the copy-in - the
`std::wstring` clear-then-
assign shape on an 8-element
inline buffer.
Interior anchor `008656F5`
(the capacity store).

`00862490` (48 B) is the
four-out-parameter state
reset `003BAC90` runs:
`dword[r8] = 0x2000000` and
`dword[r9] = 1` when the
pointers are non-null,
`dword[02EAF8E0]` zeroes,
`dword[rdx] = 2` when `rdx`
is non-null, and zero
returns - every optional out
filled, the global latch
cleared.
Interior anchor `008624AA`
(the `02EAF8E0` clear).

## SWE2-EC7-114 update (2026-09-21) - `00865FF0` / `00865E30` measured

`00865FF0` (350 B) is the
`std::wstring` append body
`008656B0` calls: `+0x18`
capacity 8 splits SSO from
heap, a source pointer inside
`[base, base + size*2)` is
rebased to an index and
tail-jumps `00865EC0` (the
self-append path),
`~size >= count` else
`"string too long"` via IAT
`008C2618`, growth goes
through `00195820`,
`00861EBA` copies
`count * 2` bytes onto the
tail, and `[+0x10]` relatches
with a NUL write. The
`008656B0` assign is this
append onto a cleared
string.
Interior anchor `00866117`
(the `00861EBA` copy call).

`00865E30` (141 B) is the
`std::wstring` move-assign
`008656B0` calls second:
under capacity 8 the source
copies inline via IAT
`008C2A40` (size+1 words),
else the heap pointer is
stolen (`dst[+0] = src[+0]`,
`src[+0] = 0`); size and
capacity transfer, then the
source relatches to
`cap = 7, size = 0, NUL` -
move semantics with the
8-element SSO threshold.
Interior anchor `00865E81`
(the source-capacity reset).

## SWE2-EC7-115 update (2026-09-21) - `00195820` / `00865EC0` measured

`00195820` (260 B) is the
`std::wstring` grow `00865FF0`
and `00865EC0` call:
requested capacity `rdi|7`
clamped to
`0x7FFFFFFFFFFFFFFE`, the
MSVC `max(cap+cap/2, req)`
policy via the `/3` multiply,
`00195C70` allocates
`newcap+1` elements,
`00861EBA` copies
`size*2` bytes of the old
buffer, `00196A50` frees it
at `cap+1`, and the object
relatches
`ptr/size/cap` with the SSO
buffer NUL-parked.
Interior anchor `001958D8`
(the `00861EBA` copy call).

`00865EC0` (293 B) is the
`append(src, pos, count)`
overload `00865FF0`
tail-jumps to when the source
aliases the destination:
`src.size >= pos` else
"invalid string position"
(`008C2620`), `count` clamps
to `size-pos`, the same
`"string too long"` guards
and `00195820` grow run,
then `00861EBA` copies
`count*2` bytes from
`src_base + pos*2` onto the
destination tail.
Interior anchor `00865FA9`
(the `00861EBA` call).

`002D1DB0` (2117 B) is the page-extent walker `002D3BA0` steps: `(+0x9E - +0x13C - 1 + +0x100) / +0x100` and `(+0x9C - 1 + +0xEA) / +0xEA` idiv page counts clamped by `+0xF0`/`+0xEC`, `0x2000` on `+0xE4` and the `0091553C` `0x8000`/`0x1000` mask against `r9d` gate the arms, `+0xF2`/`+0xF4` supply the cursor and `+0x107`/`+0x108` the mode bytes - call-free list navigation on the dispatcher's record.

Interior anchor `002D1E05` (function `002D1DB0`).

`002D1B10` (660 B) is the visible-window step the list-input dispatcher `002D3BA0` calls (the page-extent walker `002D1DB0` is its sibling): `word[+0x100]`/`+0x9E`/`+0x13C`/`+0xEA`/`+0xF0`/`+0x9C` feed two `idiv` page counts, `0091553C`'s mask plus `+0xE4` bit 0x2000 gate the mode, and `dil` bits 0x10/0x40 advance or retreat `word[+0xF2]` inside the window - the record's scroll math, call-free.

Interior anchor `002D1B5F` (function `002D1B10`).

`003BA680` (154 B) is the save-storage substate handler `003BB790` dispatches (this page's `02B40E14` machine): substate `0` writes `1` and zeroes `02B40554`/`02B40EC0`; substate `1` runs `008621E0(ecx = byte[02B40E20], rdx = 02B4055C, 0, 0xC8, out = 02B41140)` then posts `0xD`; substate `0xD` clears `02B40E14`/`02B40E10` when its arg is positive else posts `9` into `02B40E18` - the arm the queue's dispatch table (`0x3BA944`) reaches.

Interior anchor `003BA6E9` (function `003BA680`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**WorldAreaField — BOTH DIRECTIONS, 19 edges: a field transition and a save restore share the persistence pair.**
- **Field-transition bodies call this contract's pieces.** `WorldTransitionSnapshot_CapturePersistencePairForActiveSlot`,
  `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot`, `WorldTransition_StageFieldTransition` and
  `WorldTransition_RequeueCurrentFieldForRestore` call:
  - the mode predicate `00236760`;
  - `SaveImage_GetActiveRuntimeBuffer` (`002EF640`), `SaveTransitionMetadata_RestoreFromRecord` (`002EF410`) and
    `00394450`;
  - the operation opener `SaveWrite_OpenOperationController` (`00583260`).
- **The arena leaf `0036A100`** is also called by `AreaArd_LoadOrUnloadFieldResource` and two field loaders.
- **The other direction.** The normalize step `SaveLoad_NormalizeLoadedRuntimeStateAndReseed` (`00584210`) calls
  `WorldPersistence_ImportGroupPersistentBank` and `WorldTransition_SetActiveOrPendingFieldId`, and the restore
  `005843E0` is itself filed in the field layer.

Which field loads next is the world-transition pages' subject. This contract owns the completion and its status
mapping.

**Input — DEPENDENCY, 19 edges.**
- The storage list's step bodies (`002D0580`, `002D3900`, `002D3A50`, `002D3BA0`, `002D1870`) read the input
  manager through `001E0A10`, `001E0E30`, `0035F0F0` and `0035F110`.
- `00182D40`, `001E0A10` and `001E0E30` fetch `InputManager_GetSingleton`.
- The teardown's `002814E0` calls `001E0F20`.
- The other way:
  - the operation-status getter `001D50D0` is shared with the binding translation
    `InputManager_TranslateBindingProfileToControlState`;
  - `InputGameplay_ArbitrateDigitalInputAndModalState` asks the same predicate `00236760`.

The binding pages own input.

**Script_VM_Native_Bridge — CLIENT, 14 edges.** Script-VM adapters run save and load steps through this contract's
entry points `00254CB0`, `003BB420`, `00236760`, `0023A390`, `0036A100` and `001831A0`. The adapters are `0050D9A0`,
`0050ED70`, `0050EEA0`, `0050EF50`, `0050C670`, `0050C8D0`, `0050C990`, `0050F540`, `0050F500`, `0050D8F0` and
`00354D00`. The verbs are the script VM's; the operations are this contract's.

**InputGameplay — CLIENT, two edges.** `00313A00` calls the `(1, 0x15)` init and teardown pair `002E1C20` / `002E1CA0`
that this contract's controller mirrors.

**RNG_Random_Selection — SERVICE, one edge.** `00584210` reseeds through `RNG_MT19937_Seed` after a load. Which draws
use that generator is in `which-roll-is-on-which-generator`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*
