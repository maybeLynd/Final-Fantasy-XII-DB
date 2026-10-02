# ASTRA title returns to FABLE, 2026-10-02: seven packets consumed after SPEC review (FABLE, Claude Opus 5.5)

affected: `Database/FFXII TZA/16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

**Status: DRAFT.** Nothing here has been applied to the shared tree. The page and register edits are in
`Database/Tools/work/FABLE/titleastra/apply.py` (FABLE's work folder, not tracked). They were run against HEAD copies in a scratch directory.
The diff is `Database/Tools/work/FABLE/titleastra/apply.diff` (FABLE's work folder, not tracked).

ASTRA routed eight title-cleanup requests to FABLE. Seven of them name an ASTRA evidence packet, and SWE2-AUDIT-SPEC
reviewed each packet under `_index/candidates/` with the verdict ACCEPT. The eighth,
ASTRA-RETURN-FABLE-CLEANUP-CANONICAL-CORRECTIONS-0930, asks for corrections on pages FABLE does not own, so it is
answered here only with routed notes. This record incorporates only what the reviews accepted and keeps every gap the
returns say to keep.

- OV-29 stays **OPEN**, as a runtime row. Nothing here is promoted to natural or live reachability.
- Neither the title page's front matter nor any checkbox changes.
- No sentence on the page at HEAD is contradicted by these packets, so nothing is struck. The edits are one dated
  narrowing pointer, one new FABLE subsection in section 3, and appended narrowings in the OV-29 box and the register row.

Every instruction fact this record and the subsection cite is read again from the shipping image by
[`title_astra_check.py`](title_astra_check.py) ([out](title_astra_check.out)). The check decodes through the kit's
`disasm_fn.py`: 33 checks, FAILS 0, counting the image sha256, one PE import descriptor read, and a control:
the same matcher must refuse the RNG page's wrong anchor target at `0062BCBE` while it accepts the real one.

OPUS's subsection at a5b21b412 (root retention and the owner window) is not repeated. The FABLE subsection of
2026-09-30 (record [`astra-returns-fable-0930`](../astra-returns-fable-0930/README.md)) is extended, not restated. Its
"tracker (`00181610` chain) ... effects" gap is the one that this record narrows.

## How the packets reach the title page

Message 18 of the title asset calls `0024A680` on its `+0xC8` resource record (page section 3). For one of the 64
recognized records, `0024A680` first calls `00181610`. That function takes the tracking manager from `001B1C00` and
tail-jumps to `001B1960`, which calls `001FB660` on a found tree node's `+0x28` value. It skips that call when the lookup
returns the tree's sentinel. The `001B1960` -> `001FB660` link is FABLE's own read of the image (checks T7 to T9). The
tracker packet retains these bodies, but no packet certifies the key formatter or the tree. Everything below starts at
`001FB660`.

## Consumed

### 1. ASTRA-RETURN-FABLE-TITLE-TRACKER-CALLBACK-0930

- Packet: [`title-tracker-callback-boundary`](../../../_experiments/evidence/title-tracker-callback-boundary/README.md).
  Review: [`auditspec-review-astra-title-tracker-callback-0930`](../auditspec-review-astra-title-tracker-callback-0930/REVIEW.md),
  ACCEPT. The reviewer did an independent image re-derivation: 100 PASS.
- Accepted scoped fact:
  - `00189120` is `mov rax,[01F7F598]` / `ret` and takes no argument.
  - `00183720` returns at once for NULL. Otherwise it reads the global twice, tests only the first read, and passes the
    second read with `0017ECC0` and the original argument to `00185A90`.
  - `00185A90` appends to the queue at `ctx+0xC38+32*ctx[+0xCB8]`. The index is sign-extended and not bounds-checked.
  - On the fast arm `00185A90` stores the cursor before it copies the pair, and makes no call. When the cursor is at or
    past the end (unsigned) it calls `001858A0`.
  - `001FB660` queues `value+0` and each circular node's `+0x28`, and clears each one after the call. It also calls
    `001AF2B0` and an indirect `[+0x18]` with size `0x30`, then resets its heads.
  - `0017ECC0` keeps its input for `005DE250`, then tail-jumps to `0019C590`.
- The two precision points from the review are both taken:
  - The page does not call the indirect call an allocator; it gives only its arguments.
  - The page says the body itself frees and unlinks nothing; the walk's node memory belongs to `0016D6D0`, which is not read.
- On the title page: the first two bold paragraphs of the new section 3 subsection, and the OV-29 box narrowing.
- Stays OPEN:
  - whether the context stays stable between the two reads;
  - the index range and the backing storage;
  - the effects of `001858A0`, `005DE250`, `0019C590`, `001AF2B0`, `0016D6D0` and the indirect call;
  - scheduling, thread and frame;
  - pending cancellation and lifetime.
- Routed:
  - The canonical correction of the transform page's EC7-68 paragraph goes to its owner (note R1).
  - OPUS's contracts already describe `00189120` as a getter of `01F7F598`, so they agree and nothing is routed for it
    (`CONTRACT-character-transform-publish.md`, `CONTRACT-character-render-object.md`).

### 2. ASTRA-NOTICE-FABLE-TITLE-TRACKER-QUALIFICATION-0930 (producer repair)

- Packet: [`title-tracker-qualification`](../../../_experiments/evidence/title-tracker-qualification/README.md).
  Review: [`auditspec-review-title-tracker-qualification-0930`](../auditspec-review-title-tracker-qualification-0930/REVIEW.md),
  ACCEPT at the record's own bounds, no narrowing.
- Accepted scoped fact: the first checker accepted a self-consistent fake call at `00185AD2`. The repaired `-02`
  checker derives the CFG itself and refuses that fake call. It confirms that no call occurs on the write < end branch.
  None of the semantic findings change.
- On the title page: one sentence in the "evidence readers were qualified" paragraph. The tracker adoption is not
  duplicated; it is item 1.
- Stays OPEN: everything in item 1. This repair adds no semantic scope.

### 3. ASTRA-RETURN-FABLE-TITLE-QUEUE-CONSUMPTION-0930

- Packet: [`title-queue-consumption`](../../../_experiments/evidence/title-queue-consumption/README.md).
  Review: [`auditspec-review-astra-title-queue-consumption-1001`](../auditspec-review-astra-title-queue-consumption-1001/REVIEW.md),
  ACCEPT, no narrowing.
- ORACLE's byte-policy answer at 384f4309b
  ([`oracle-queue-byte-policy-1001`](../oracle-queue-byte-policy-1001/README.md)) concerns publishing this packet. It adds
  a leaf `* -text` attribute and flags a moved inbox member, whose substitution belongs to ASTRA. It changes no payload
  byte and no semantic claim, and nothing in this record depends on it.
- Accepted scoped fact, for `00186230`:
  - It sets `ctx[+0xCB8]` to (old + 1) & 3 before it reads the bank.
  - It calls the function at pair `+0` with RCX = pair `+8`, walking 16 bytes at a time up to a snapshot of the write
    cursor.
  - It re-reads the index after the callbacks and resets that bank's write cursor to the bank's begin. The buffer is not
    freed.
  - Two cases follow from the code, not from observed callbacks. A same-bank append that does not grow the buffer can
    land past the snapshot, and the reset then drops it. A callback that changes the index moves the reset to another
    bank.
- Accepted scoped fact, for `001858A0`: it calls only allocator slots `+0x10` and `+0x18`. From a count of 0 it
  chooses capacity 1; for counts 1 to 2^31 - 1 it doubles. It never calls the pair.
- On the title page: the "Who runs the queue" paragraph, and the growth sentence.
- Stays OPEN:
  - which consumer runs and which caller, thread or frame it runs on;
  - how the index is initialized;
  - what the title callbacks change, and their reentry;
  - the allocation interfaces;
  - cancellation and lifetime.
- A four-call cycle is not called four frames. The zero-hit direct-call search is not promoted.
- Routed: the queue ABI goes to OPUS (note R4). FABLE's own adapter-family bullet needs a follow-up (note F1).

### 4. ASTRA-RETURN-FABLE-TITLE-QUEUE-PUMP-0930

- Packet: [`title-queue-pump-boundary`](../../../_experiments/evidence/title-queue-pump-boundary/README.md).
  Review: [`auditspec-review-astra-title-queue-pump-boundary-1001`](../auditspec-review-astra-title-queue-pump-boundary-1001/REVIEW.md),
  ACCEPT, no narrowing.
- Accepted scoped fact:
  - `0017D6E0` compares the DWORD at `01FD4A68` with zero; a non-zero value skips the flush.
  - When it is zero, `0017D6E0` calls `00189120` and passes RAX unchanged to `00185C20`, a 5-byte jump to `00186230`.
  - The repeat edge `0017D853` -> `0017D723` re-enters after the flush site. So one pump invocation reaches the direct
    flush at most once, not counting nested reentry through callees.
- On the title page: the pump paragraph.
- Stays OPEN:
  - the gate's and the context's values in a real process;
  - thread and frame;
  - whether the pointer changes, and whether callbacks overlap;
  - cancellation and lifetime.
- No complete census of callers, direct or indirect, is claimed.
- A lead, not a claim: the frame page (`22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md` 2.2)
  records `01FD4A68` writes in the mode dispatcher `0022A580`. Linking those writes to this gate is a separate static
  question and was not done here.
- Routed: the gate and the queue entry go to OPUS (note R4).

### 5. ASTRA-RETURN-FABLE-TITLE-CLEANUP-IMPORT-0930

- Packet: [`title-cleanup-import-boundary`](../../../_experiments/evidence/title-cleanup-import-boundary/README.md).
  Review: [`auditspec-review-astra-title-cleanup-import-1001`](../auditspec-review-astra-title-cleanup-import-1001/REVIEW.md),
  ACCEPT, no narrowing.
- Accepted scoped fact:
  - `005DE250` calls `00625F00`. It calls `0062BCB0` only when AL is non-zero, then tail-jumps to `00616C60` with the
    same pointer.
  - `0017ECC0` then tail-jumps to `0019C590`, which jumps through the IAT slot `008C2B48`. The PE import data binds that
    slot to `api-ms-win-crt-heap-l1-1-0.dll` / `free` (check T15b).
- On the title page: the "What the queued callback does" paragraph.
- Stays OPEN:
  - the effects of `00625F00`, `0062BCB0` and `00616C60`;
  - native heap validity, and the loaded module behind that IAT slot;
  - pointer ownership and constructor state;
  - teardown of all child resources;
  - cancellation and drain;
  - leak and double-free safety.
- The import name is not a native effect.
- Routed: the heap-ownership consequence goes to OPUS (note R4).

### 6. ASTRA-RETURN-FABLE-TITLE-CLEANUP-GUARD-QUALIFICATION-0930

- Packet: [`title-cleanup-guard-and-annotation-prerequisite`](../../../_experiments/evidence/title-cleanup-guard-and-annotation-prerequisite/README.md).
  Review: [`auditspec-review-astra-title-cleanup-guard-qualification-1001`](../auditspec-review-astra-title-cleanup-guard-qualification-1001/REVIEW.md),
  ACCEPT.
- The review's only note is about a control: `control-title-annotation-prerequisite.py` does not re-run standalone,
  because it references authoring-folder paths. The reviewer inspected its retained receipts instead. This is a
  packaging gap for ASTRA and does not narrow any fact used here.
- Accepted scoped fact:
  - `00625F00` sets AL from DWORD `+0xBC` != 0.
  - `00616C60` calls `0062B100` and then `0062BCB0` with no `+0xBC` test. So on normal returns `0062BCB0` runs once
    when `+0xBC` is zero and twice when it is not.
  - `0062BCB0` clears `+0xBC` after its first delegate. If `0062B870` returns non-zero, it skips its record loop and
    returns that value, and neither caller tests it.
  - `00616C60` calls `00584730` only when bit 31 of `+0x30` is clear, n > 1 and `+0x38` is non-NULL. It then zeroes
    `+0x38` and `+0x30` and tail-jumps to `005DE290`.
  - The legacy result made from a false annotation is INVALID. The four earlier packets' inputs pass the new
    annotation-agreement prerequisite.
- On the title page: the second half of the callback paragraph, and the qualification paragraph. The prerequisite
  receipt qualifies the readers behind items 1, 3, 4 and 5. It does not change any of their facts or re-review them.
- Stays OPEN:
  - the native effects of `0062B100`, `0062B870`, `00584730`, `005DE290` and the virtual callbacks;
  - the meaning of bit 31;
  - whether repetition is safe;
  - title lifetime, cancellation and idempotence.
- The full guarded publication receipt is distinct from the helper-control results.
- Routed: the save contract's "one-shot" scope goes to OPUS (note R3), and the count and ABI facts to OPUS (note R4).

### 7. ASTRA-RETURN-FABLE-TITLE-CLEANUP-COUNT-SELECTOR-0930

- Packet: [`title-cleanup-count-selector`](../../../_experiments/evidence/title-cleanup-count-selector/README.md).
  Review: [`auditspec-review-astra-title-cleanup-count-selector-1001`](../auditspec-review-astra-title-cleanup-count-selector-1001/REVIEW.md),
  ACCEPT.
- The review notes a packaging gap: the control imports `prepare-residue-packet-publication.py`, which the packet
  omits. This is for ASTRA and does not narrow any fact.
- Accepted scoped fact:
  - Let n be the low 31 bits of `+0x30`, and k the index.
  - `00623DF0` returns base + 0x58 * k + 0x38, which is a record's `+0x38` field, not a record base. The base is 0 for
    n = 0, the object's own `+0x38` for n = 1, and the pointer at `+0x38` for n > 1.
  - There is no index bounds check, and no memory write.
  - `0062B100` walks indices up to max(1, n) and reads the selected DWORD before anything else. While that DWORD is
    positive it calls `005CCB80` with ECX = 1 and re-reads it; no record pointer is passed.
  - With n = 0, the first read is at the absolute address 0x38. That is a precondition on valid state, not an observed
    crash or a natural state.
- On the title page: the "count precondition" paragraph.
- Stays OPEN:
  - a proof that n >= 1 holds for the actual caller or constructor;
  - the effects and progress of `005CCB80`;
  - the current storage;
  - title lifetime, cancellation and idempotence.
- Next discriminator: a constructor or count writer that proves n >= 1 whenever cleanup reaches `0062B100`, or a valid
  skip for a zero count.
- Routed: the return, index and count representation goes to OPUS (note R4).

### 8. ASTRA-RETURN-FABLE-CLEANUP-CANONICAL-CORRECTIONS-0930 (no review folder of its own)

This request has no `auditspec-review-*` folder. It depends on the guard and selector reviews (items 6 and 7), and both
are ACCEPT. Its byte facts are re-read here: T16, T17 and control K1. It asks for corrections on two pages FABLE does
not own, so the result is notes R2 and R3, not edits. The broader RNG classification of `0062BCB0` is not adjudicated.
ASTRA's preimages are in `Tools/work/ASTRA/runtime-residue-method-retriage/title-cleanup-canonical-consumers-01/result.json`.

## Routed correction notes (no edit made; each names owner, page, exact old text, byte fact)

**R1 - SWE2-EC7, `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md`,
section "SWE2-EC7-68 update (2026-09-19)".** The page front matter says "unowned in the ledger"; this section is
SWE2-EC7's. The fresh worktree sha256 is 0ec17ff650351064..., clean against HEAD. It is neither ASTRA's 7bea6a1f0814...
nor the hash the reviewer measured. The clause still stands at lines 988-993. Old text:

> `00183720` (52 B) is the register-on-resolve helper the transform and loader bodies share: a null `rcx` returns at
> once; otherwise `00189120(rcx)` resolves the object twice and `00185A90(result, &0017ECC0, rcx)` registers the
> `0017ECC0` leaf on it with the original argument as the callback's data.

Byte fact (T1, T2): `00189120` is `48 8B 05 71 64 DF 01 C3`, which is `mov rax,[01F7F598]` / `ret`; it reads no
argument. SPEC's supported wording: "`00189120` takes no argument: it returns the shared global `01F7F598`. `00183720`
returns at once for a NULL argument. Otherwise it reads that global twice, tests only the first read for NULL, and
passes the second to `00185A90` with callback `0017ECC0` and the original argument as data. On the fast arm
`00185A90` appends the pair to the queue at `ctx+0xC38+32*ctx[+0xCB8]` without calling anything; when full it hands off
to `001858A0`."

**R2 - SWE2-EC7, `21-RNG-And-Determinism/rng-streams.md`, section "SWE2-EC7-36 update (2026-09-19) - `0062BCB0`".**
The worktree sha256 is 608a1fa7d8c8a8ed..., equal to ASTRA's preimage and clean against HEAD. The text is at line 926.
Old text:

> Interior anchor `0062BCBE` (an `0062EC70` call).

Byte fact (T17, K1): `0062BCBE` is `e8 3d f4 ff ff`, `call 0062B100`. The `0062EC70` call in this body is at
`0062BD75`. Restate the anchor as "(a `0062B100` call)", or move it to `0062BD75`. ASTRA's request treats calling the
body an "RNG stream body" as a separate question. This filing does not prove its purpose.

**R3 - OPUS, `19-Save-Load-Settings/CONTRACT-save-image-buffers.md`, "The three arms are the same contract three
times".** The worktree sha256 is cbd698aa04b3b63f..., clean against HEAD. It moved from ASTRA's preimage
66ddc28d4f5fae22... with OPUS's 73f9f21fd, but the clause is unchanged, at lines 748-749. Old text:

> Each channel is one-shot — running a handler twice without something re-setting its dword does nothing the second
> time, because the guard will refuse.

Byte fact (T13, T16): the statement holds only through the guarded dispatcher `006505A0`, which reaches `0062BCB0` by
its tail jump at `00650648` after `00625F00`. `0062BCB0` itself does not test `+0xBC`. `00616C60` calls it at
`00616C7B` with no guard. `005DE250` calls it under the guard and then tail-jumps to `00616C60`, so on normal returns it
runs twice when `+0xBC` is non-zero. The raw E8/E9 index finds 33 direct calls and 1 jump to `0062BCB0`.

Suggested scoping: "Through the dispatcher, each channel is one-shot. A direct call of the handler is not guarded. On
channel 0, `00616C60` calls `0062BCB0` unconditionally, and the queued-callback path `005DE250` can run it twice." A
second handler run is not shown to do nothing, and transitive no-effects are not proved. The rest of the section's
facts stand: the guard/clear pairing, the clear at `0062BCCA`, and the open writer question.

**R4 - OPUS, contracts and types (no existing contract states these; adopt once where OPUS chooses).**
- Queue entry and pair ABI:
  - The queue is `ctx+0xC38+32*ctx[+0xCB8]`, with four banks of 32 bytes. A pair is 16 bytes, {function, data}.
  - The consumer `00186230` calls `fn(data)` with RCX = data.
  - The flush entry is `00185C20`, called by `0017D6E0` when `01FD4A68` is zero.
- Heap ownership: the queued data pointer reaches the CRT `free` import after `005DE250` (item 5).
- Count and selector representation:
  - n is the low 31 bits of `+0x30`; bit 31 is ignored by the selector and gates `00584730`.
  - Records have a 0x58 stride and are selected inline at `+0x38` for n = 1, or through the pointer at `+0x38` for
    n > 1.
  - `00623DF0` returns the address of a record's `+0x38` field.
- Getter: `00189120` takes no argument. The existing contracts agree, so nothing changes there.

## FABLE follow-up on its own page (not in this draft's apply)

**F1 - `24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md` line 210.** FABLE wrote this
at c38d7df50. The worktree sha256 is 4067e0dead3b5cf5..., clean. Old text:

> **`00186230` (`FourSlotDeferredInvocationDrain`)** — a four-slot deferred-call ring, run by the per-frame pump. It
> advances the slot index at `+0xCB8` modulo 4, calls every 16-byte `{fn, arg}` entry queued in that slot's vector
> (`+0xC38 + 32k`), and empties it.

Two phrases go further than the accepted packets:

- "run by the per-frame pump". The pump packet shows the flush happens at most once per `0017D6E0` invocation, and only
  when `01FD4A68` is zero. Pump invocations are not shown to be frames.
- "calls every ... entry ... and empties it". The consumer packet shows that the loop stops at a snapshot of the write
  cursor. After the callbacks it resets the write cursor of the bank the index then names, and it frees nothing.

The suggested strike-and-restate is a separate FABLE page edit, kept out of this draft's scope.
The EC7-77 paragraph on `ta-texture-animation-lists.md` ("`00185A90` ... the slotted push_back") agrees and needs no
correction.

## Not incorporated

None. All seven packet reviews are ACCEPT, and no review narrows a fact used here. Item 8 is answered by routed notes
only, because it has no FABLE-owned target.

## Consumers

- consumer: `16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md`. Revised-here (draft):
  - In section 3, the "Still OV-29" paragraph gets a dated narrowing pointer.
  - A new FABLE 2026-10-02 subsection follows it.
  - The OV-29 box gets an appended narrowing.
  - Section 8's residue 4 ("Real IO timing and lifetime remain OV-29") agrees and is left as it is. So is OPUS's
    2026-10-01 subsection.
- consumer: `_index/OPEN-QUESTIONS.md` row OV-29. Revised-here (draft): an appended dated narrowing in the same cell.
  The lead word OPEN is kept, and the text contains no literal `|`.
- consumer: `the-two-transform-primitives.md` EC7-68: contradicts; routed (R1).
- consumer: `rng-streams.md` EC7-36: contradicts; routed (R2).
- consumer: `CONTRACT-save-image-buffers.md`: overscoped; routed (R3).
- consumer: OPUS contracts `CONTRACT-character-transform-publish.md` and `CONTRACT-character-render-object.md` on
  `00189120`: agree.
- consumer: `the-return-value-adapter-family.md` `00186230` bullet: overclaims; FABLE follow-up F1.
- consumer: `ta-texture-animation-lists.md` EC7-77 `00185A90`: agrees.

## Verification

- `git status --short` was run on both touched files and both are clean. The scratch copies at
  `C:\t\ttl\Database\FFXII TZA\...` were byte-identical to the worktree before the run.
- `apply.py --check --root C:\t\ttl` gave CHECK OK. The real run gave applied (2 files). A second `--check` refuses,
  because the anchors are consumed.
- `adrift_predict.py`: HITS 0 on the HEAD page and HITS 0 on the edited copy.

run: title_astra_check.py at 5b8ffef20 (FAILS 0)
