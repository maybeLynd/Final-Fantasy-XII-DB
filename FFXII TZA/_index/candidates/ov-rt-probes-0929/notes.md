# FRONTIER-REQ-FABLE-RT-REMAINDERS-PROBE-SITES — reader notes (2026-09-29)

Read-only reader for FABLE. Image `73461d08…21F8`, image base `0x120000` (addresses below include it).
Every address here was read from the image in this session with `pub140-scratch/disr.py`, `tools/rawcalls.py`,
`tools/ripscan.py` or `tools/dispscan.py`. Scripts and their outputs are in this directory.

Sources read: register rows OV-5/8/16/19/29/33 (`OPEN-QUESTIONS.md` 3414-3442); `batch-K-scope-rulings.md`
(Extension 2026-09-29, runtime rule, lines 489-559); `CONTRACT-encoded-id-space-and-class-registry.md`;
`the-encoded-id-space-and-the-query-record.md` §2.2-2.7 and the §7 box; `the-query-record-from-initialization-to-reuse.md`
(all, including §2 and §7); `the-actor-request-from-arming-through-start-and-return.md` (all);
`the-script-from-bytecode-through-wait-and-resume.md` §8; `the-external-source-owner-and-borrowed-view-lifetime.md`;
`the-indexed-source-request-from-arm-to-terminal-pump.md`; `the-resource-request-queue.md` §2.3 and §8;
`the-title-asset-singleton-and-its-distinct-consumer.md`; `EXP-079-arena-live-placement.md`; the existing carrier
`gg3-scratch/op_add_astra_rt.json` and its two companions.

---

## 1. OV-5 / OV-8 (c) — a state base at or above 4 GiB

**The probe site is exact already, as FRONTIER says:** qword `[01F83530]` in a loaded save. Link to
`OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME` (AQ-ARENA); do not duplicate.

**What the registry's own state block is.** The block handed to the rebase is not dynamic. Both callers compute
`SaveImage_GetActiveRuntimeBuffer() + 0x4E68C` (`00233C2A`, `00238A89`), and that getter is
`lea rax, [02164280]` / `ret` (`002EF640`). So the state is `021B290C`, an image address, and the global `02EBF190` holds
it (`00233C33`, `00238A92`). The PE has no `DYNAMIC_BASE` (contract §7). The only high-pointer surface
left is `0020E600`'s base `qword [01F83530]`, which is what the contract already says.

**An observation already exists and is not cited on the rows.** EXP-079 (2026-09-12, method C, read-only process
observation) read base `01F83530` = **0** in all four samples: title menu ×2 and after an ordinary load of
The Stepping ×2 (`EXP-079-arena-live-placement.md` lines 17 and 100, "base remains zero … in all four samples").
That is a zero observation in a loaded save. Under the batch-K wording it bounds (c) and does not prove absence.
AQ-ARENA's extra ask, whether `003E3C30` executes, is separate.

**Decision per outcome (for the AQ-ARENA result, as it bears on OV-5/OV-8):**
- 0 in a loaded save: (c) is still unreached. This is already observed (EXP-079). The row keeps (c) OPEN with that bound, or FRONTIER rules.
- Non-zero but below 4 GiB: the contract's "zero for the process life … supported, not proven" is falsified. (c) is still unreached, because every sum stays below 4 GiB.
- At or above 4 GiB: (c) is reached. OV-5/OV-8 (c) becomes ANSWERED (reachable). The contract's high-half-loss paths become live behaviour, not only fixture behaviour. These are §6 "query arms perform row stride multiply/add in 32-bit registers" and the S-32 `0030C71D add ebp, eax` observation.

## 2. OV-5 / OV-8 (d) — over-reservation (high6 reserved > low10 total)

**There are three packed-count classes, not four.** FRONTIER's request says "four packed classes". The registry rows
for nibbles 0, 1 and 2 (classes 5, 6 and 7) carry the packed-count handler pair `002FD150`/`002FD8D0`, dumped from the image:

| class | descriptor | `+08` region-A pointer cell | `+3C` count cell (ships) | region A (words) | words at |
|---|---|---|---|---|---|
| 5 items | `01EEBCC0` | `01EEBCC8` | `01EEBCFC` (`0x40`) | +`0x4748`, 64 | `021B7054`–`021B70D3` |
| 6 equipment | `01EEBD18` | `01EEBD20` | `01EEBD54` (`0x1A4`) | +`0x47C8`, 420 | `021B70D4`–`021B741B` |
| 7 loot | `01EEBD70` | `01EEBD78` | `01EEBDAC` (`0x200`) | +`0x4B10`, 512 | `021B741C`–`021B781B` |

The "four" is most likely the query-record page's "four shipped classes have nonnull mutate handlers". Those are the
bundle/gil classes 14, 15, 18 and 19, which have **no storage and no query handler**. The `+08` cells ship 0, and the rebase writes them
(`0030B6CB`). After the rebase they must equal the "words at" column (`021B290C` + region offset). That equality is the probe's
first positive control.

**The comparison, from the reader itself.** `InventoryPackedCountClass_QueryChannel` `002FD8D0` mode 0 (`002FD942`–`002FD95F`)
computes `(w & 0x3FF) - (w >> 10)`, which is signed and so can be negative. Mode 1 is `w & 0x3FF` (`002FD934`/`002FD939`) and
mode 2 is `w >> 10` (`002FD920`/`002FD925`). Over-reservation is `(w >> 10) > (w & 0x3FF)`.

**A static finding that bears on (d). Mine, not yet published, and needing FABLE's check.**
- *The writers found.* An exhaustive rip-relative census of the registry `01EEBCC0`–`01EEC1E8` (`registry_ripscan.txt`) finds 49 reads in 28 functions.
  `registry_fn_stores.out` lists every non-stack store in those 28 functions; its control, `0030B6F1`, is listed. The only stores that
  can reach a packed word are these four:
  - `002FD150`'s three word stores. Channel 2 sets the reserved count and clamps it to `[0, total]` (`002FD26A`, `002FD27E`/`002FD281`, then store `002FD298`).
    Channel 1 sets the total and clamps it to `[reserved, 99]` (`002FD2E9`/`002FD2EC` and `002FD2F5`, then store `002FD31A`).
    Channel 0 moves the reserved count, again clamped to `[0, total]` (`002FD3B7` and `002FD3D2`/`002FD3D5`, then store `002FD3F1`).
  - `003047F0`'s zeroing loop (`0030482A`), which writes 0.
- *The invariant holds on every one of them.* One corner case: channel 0/2 shift the new reserved count left 10 into a 16-bit word (`002FD28C`, `002FD3E5`). A value above 63 loses its high bits,
  so the stored reserved count can only become *smaller*. It never becomes larger than the total. So every in-image
  writer found preserves `reserved <= total`.
- *Other routes checked.*
  - State-relative displacement stores into +`0x4748`..+`0x4F0F`: none (`regionA_disp_writes.txt`). The same scan finds the
    known state write `00233C83 mov word [rax+0x5B0C]` (`control_5B0C.txt`), so the scan can see such stores.
  - Absolute rip references into `021B7054`–`021B781B`: none.
  - Image-base-relative displacements `0x2097054`–`0x209781B`: none. **There is no positive control for this last scan.**
- *What remains.* The save image block `02164280` is loaded from the save file as data. A saved word is carried in without
  any clamp. So in-game mutation cannot create over-reservation; only a loaded save carrying it, or a writer this census
  does not reach, can. One such writer would be a generic copy through a passed pointer, and the census does not see those.
  This would make (d) a static answer ("not produced by the game; enters only through save bytes") once published and
  independently checked. The runtime probe would then corroborate it.

**Decision per outcome:**
- Any word with `high6 > low10` present right after a save loads: a loaded save carries it. The static answer's "save bytes" route is
  confirmed live. Query-record page §7 "a synthetic over-reservation yields a negative result" gains "a loaded save can carry one; no in-game writer creates one".
  OV-5/OV-8 (d) becomes ANSWERED (reachable only through save data).
- A word that becomes over-reserved *after* load: there is a writer outside the census. Put a write watch on that word to name it.
  This falsifies the static finding above.
- None over the coverage, with the controls passing: consistent with the static finding. If the static finding is published, (d) closes
  ANSWERED on it, with this zero as corroboration. Otherwise it is a bound and the row stays OPEN.

**Positive controls (same session):**
1. The `+08` cells equal `021B7054` / `021B70D4` / `021B741C`, and `qword [02EBF190]` = `021B290C`.
2. The `+3C` cells read `0x40` / `0x1A4` / `0x200`.
3. With any party member equipped, at least one class-6 word has `high6 >= 1`, because equipped copies are the reserved count (page §2.7).
   Printing that count shows the probe can see the high field at all.
4. One class-5 word's low10 equals the Items-menu count of that item, for example Potion, id `0x0000` → `021B7054`.

## 3. OV-16 — notification key reused while an older same-key request is pending

**Where the key is made, filed and matched.**
- *Registration (arm).* `ScriptVM_SubmitActorRuntimeRequest` `00268850` builds a stack descriptor at `rsp+0x20`:
  - `+1` mode, from `dl`, the argument at `rsp+0xC0` (`002689AD`);
  - `+2` target channel, `sil` (`002689B1`);
  - `+3` the **issuer's channel** `byte [r15+0x11]` (`002689A4`/`002689A9`);
  - `+0x10` the **continuation offset** `ebp - dword [r15+0x58]` (`0026898D`/`0026898F`, stored `002689BC`).

  `r15` is the issuer actor. The target is resolved at `002689E3`, and the insert returns at `00268A1D`. `00268A3B` is the no-target path, which returns 3.
  The insert copies desc `+3` into entry `+3` and desc `+0x10` into entry `+0xC` (`003DB8D5`/`003DB8CE`, and `003DB9D0`/`003DB9CD`).
- *Filing.* There are two posters. Each calls `ActorResource_AllocateAndSubmitEntry` `003DBCF0` on the **requester** with a mode-4 descriptor.
  In that descriptor, `+2` = entry `+3` (the issuer channel) and `+0x10` = entry `+0xC` (the offset).
  - Start notification: `003DBE5F` in `003DBDC0`, taken when entry `+0x10` == 2.
  - End notification: `003DC122` in `003DC0D0`, called from `003DB37D` in `ActorResource_RemoveActiveEntry` `003DB2A0`.

  In both, `rcx` is the requester actor and `rdx` the descriptor. `003DB7A0` files a mode-4 entry on the detached list, head byte
  `[actor+0x61]`. Channel goes to entry `+2` (`003DB906`) and offset to entry `+0xC` (`003DB8CE`).
- *Match.* `ActorResource_FindScriptRequestEntry` `003DC050` takes `rcx` = actor, `edx` = channel, `r8d` = offset. It walks byte `[actor+0x61]`
  over `0x14`-byte entries at `[actor+0xA0]`, compares `dword [e+0xC]` (`003DC083`) and `sbyte [e+2]` (`003DC092`), and returns the index
  at `003DC0BB`. It returns `0xFF` at `003DC0AB`, including when the walk cap `byte [actor+0x89]+2` is reached. There are two callers:
  - `0025E09F` in `0025DF00` (checked at `0025E0A4`). The key is `sbyte [rdi+0x11]` and `dword [rsi] - dword [rdi+0x58]`.
  - `0025B435` in `0025B400` (checked at `0025B43A`).

  A match is removed by `003DB2A0` (`0025E0B0`, `0025B456`).

**Why the pending case is possible statically (not a claim of occurrence).** A kind-4 waiter cannot re-arm from the same
PC while it is waiting. So a same-key reuse needs the wait to be abandoned, and there are two ways that happens:
- the issuer's own channel entry is removed while it waits;
- the channel restarts.

`003DB2A0` has seven raw callers, among them `00262708` (`002626C0`) and `00262788` (`00262740`), which are removal paths outside the RET/consume sites.
Once the wait is abandoned, the old request's notification is still posted later, and it stays on the
detached list. `0025DF00` removes only matched entries, and `003DB580` (reached only from `ActorStorage_InitializeRecord`) is what
resets the list. A later request armed from the same channel and PC is then satisfied by that stale entry
at once. Unconsumed notifications also occupy the same finite entry pool (OV-10).

**Probe, primary, one site.** At `002689E3`, walk the issuer's detached list: `b = byte [r15+0x61]`; while `b != 0xFF`, take
`e = [r15+0xA0] + b*0x14`, compare, then `b = byte [e]`, for at most `byte [r15+0x89]+2` steps. Count any entry with `sbyte [e+2] == byte [rsp+0x23]` and
`dword [e+0xC] == dword [rsp+0x30]`. Only arms with mode `byte [rsp+0x21]` ∈ {2, 3} count; mode 1 posts nothing.
A count ≥ 1 means a notification with this key is already waiting, so the new request's wait will be satisfied by it
before its own target starts or returns.

**Probe, secondary, a log.** This covers the case where the old request has not posted yet. Log three kinds of event:
- arm: `002689E3`, recording issuer, issuer channel, offset, mode, and the return from `00268A1D`/`00268A3B`;
- post: `003DBE5F`/`003DC122`, recording requester, `byte [rdx+2]`, `dword [rdx+0x10]`, and `byte [rcx+0x60]`, which is the entry index the insert will take;
- consume: `0025E0A4`/`0025B43A` when `eax != 0xFF`, recording actor, key and `eax`.

For each (issuer, channel, offset) with mode 2/3, the sequence must be arm → post → consume. Two arms with no consume
between them, or a consumed entry that was posted before the latest arm, is reuse while pending.

**Positive control.** The shipped corpus uses `sysReqew` 10,007 times and `sysReqsw` 3,067 times
(`corpus/us`, 1,114 decompiled scripts; `rbn_a01` alone has 11). So any field load with scripted events produces arm → post → consume triples.
The session must log at least one complete triple, and the post and consume counts should be close.

**Decision per outcome:**
- Any hit: OV-16's RT half is ANSWERED, "occurs". The instance (actor/script, key) is added under actor-request page §4, whose
  sentence "Reuse, duplicate delivery and absent actor lifetime protections cannot be inferred from equality" then has a shipped case.
  The reconstruction requirement is to reproduce the aliasing, not to add identity.
- Zero with the control passing: a bound. The row stays OPEN under the ruling.

## 4. OV-19 — owner-request issue/completion order and timing in one field load

**Sites.**
- Arm: `003DDA20`, which writes state 2 at `003DDA4E`.
- Submit: `003DDA70`. It calls the queue requester `0032E620` at `003DDAB9` with the owner's low32 address in descriptor `+8` and the completion `003DD850` in `+0x10` (`003DDA83`/`003DDA93`). State 3 is written at `003DDABE`, after the call returns.
- Actual file issue: the pump `0032E070`, state 1, at `0032E0F1` (→ `0046E030` → `002DF780`). The slot's `+0x40` == `003DD850` marks an owner request, and `+0x60` is the owner.
- Completion: `003DD850`, entered with `ecx` = owner. It writes state 4 at `003DD8B5`, or at `003DD88E` it writes state 0 after a state-5 deferred free (`003DD863` compare, then `003DD878` path).
- Delete: `003DD420`, which writes state 5 at `003DD490`.

**Order is static.**
- *The completion runs strictly after the owner's own state-3 store.* Slot `+0x40` is called only by `0032E330` (success) and `0032E370` (error, only when `+0x28 == -1`). Both are called only from the pump: `0032E133`, `0032E1FA` and `0032E26F`, and `0032E1D3` and `0032E285`. In the queue module `+0x40` is written only by the requester (`0032E951`) and cleared only by the cancel `0032E590` (`0032E5BD`).
  The requester can pump inside itself: `0032E620` → `0032E870` → `0032E8AA`, which pumps while the free list `022C51D0` is empty.
  But it does that **before** it allocates the new slot at `0032E8C9`, so the nested pump can complete only *other* requests. This nested pump is not stated on the owner page.
- *Across owners the order is the queue's FIFO.* The producer's submission order is group then slot (indexed-source page §6), and the pump
  serves the pending head only, one read in flight at a time.
- *Timing is the host.*
  - Every pump caller is a main-loop, boot or script path (`0032E040` ← seven mode bodies, boot `0022A0B0`, `0036EEB0`, `00379E30`).
  - Archive reads complete on the **AsyncLoadManager** worker. That is `CreateThread` (import `008C21C8`, called in `005CD1E0`) on the thread body `001A1240` (thunk `001A1230`), named at `008F46F8`, which loops with `Sleep(1)` while its list is empty.
  - The frame on which the pump sees the result depends only on when the worker finishes. No branch compares time:
    - The slot's `+0`/`+8` counter stamps are written by the pump (`0032E0FB`, `0032E123`, `0032E153`/`0032E156`) and never read by it.
    - No qword load of `+0`/`+8` appears in the eight queue functions that address the slot array (`0032E450`, `0032E4D0`, `0032E520`, `0032E590`, `0032E620`, `0032E990`, `0032EC40`, `0032E070`).
    - The part callback receives the slot, so a callee read is not excluded.

**Judgement: timing settles no claim.** No page sentence depends on how many frames or milliseconds pass between
issue and completion; it is host disk speed. That is the scope question FRONTIER said it would rule on separately.
**One order observation does add a fact.** A completion entering `003DD850` with `dword [rdi+4] == 5` means the owner was
deleted while its read was in flight, and the deferred-free branch `003DD878`–`003DD88E` runs in shipped play. That is the reachability of
the page §4 row "`003DD850` with state5". Offer it only if FRONTIER wants an RT half kept on OV-19.

## 5. OV-29 — title asset load callback order, timing, cancellation

**Sites.**
- The asset handler `00394070` dispatches on `dword [rdx]`, the message id:
  - message 1 → `003940F2`. It publishes `02AEE4C0` at `003940F5`, zeroes `+0xC0` at `003940FC`, and calls `00393FF0` at `00394106`.
  - message 16 → `003940E3`, `or dword [rbx+0xC0], 1`: ready.
  - message 18 → `00394097`. This is teardown. It calls `0024A680([rbx+0xC8], 1)` and `003697F0([rbx+0xD0])`, and zeroes `02AEE4C0` at `003940D2`.
- The ticket is from the twelve-slot pool `02090790`–`0209090F`, stride `0x20`, allocated by `00249580`. Its fields are:
  - `+0` flags: bit 0 = in use, bit 1 = submitted;
  - `+8` owner;
  - `+0x18` requested count;
  - `+0x1A` done count.
- `00393FF0` tail-jumps to the submit `00249410`. With equal counts at `00249434`, the submit sends message 16 **synchronously** at `0024947D` and frees the ticket at `0024947F`.
- Otherwise message 16 comes later. The watcher widget `00248700` polls `002F8040` and calls `002494F0(ticket, 1)` at `00248746`. That function adds to `+0x1A` and, when the counts are equal, sends message 16 at `0024955D` and frees the ticket at `00249564`.

**The cancellation/lifetime case that matters.** Message 18 does not free the ticket, does not detach the watcher, and does
not clear the owner. So if teardown comes while the ticket is pending, a later `002494F0` can deliver message 16
to a torn-down widget. That is the static branch; whether shipped play takes it is the runtime question.

**Probe.**
- At `00394097`, scan the 12 tickets for any with `(dword [t] & 1) && qword [t+8] == rbx`. Record `[t+0x18]`, `[t+0x1A]` and `[rbx+0xC0] & 1`.
- ~~At `0024947D`, `0024955D` and `003940E3`, record the owner. A delivery to a widget already seen at `00394097` is message 16 after teardown.~~ *Corrected 2026-09-30 (FABLE, [record](../astra-returns-fable-0930/README.md), after ASTRA [`title-member-notification-routing`](../../../_experiments/evidence/title-member-notification-routing/README.md) and its SWE2-AUDIT-SPEC ACCEPT):* those two sender sites are not complete. The title tickets' ordinary later completion is `002495C0`, installed by `00249210`: it calls the member callback at member `+0x10` first, increments done `+0x1A` (requested is `+0x18`) and sends message 16 at `00249632`. Record the owner at `0024947D`, `0024955D`, **`00249632`** and `003940E3`, with ticket, member and owner identity and a healthy positive control; a negative from the old sites alone is not a result. No past observation is reclassified by this correction.

**Positive control.**
- The title screen certainly hits `003940F5` and `003940E3`. The `fsttl_initialize` verb polls `00394500` → `+0xC0` bit 0 and holds until it is set (page §8).
- Leaving the title (New Game or Load) should hit `00394097`. That can also be seen as `02AEE4C0` returning to 0.

**Decision per outcome:**
- ~~Teardown with a pending ticket: the cancellation path is exercised in shipped play.~~ *Corrected 2026-09-30 (FABLE, [record](../astra-returns-fable-0930/README.md), after ASTRA [`title-retirement-local-guards`](../../../_experiments/evidence/title-retirement-local-guards/README.md) and its SWE2-AUDIT-SPEC ACCEPT):* teardown with a pending ticket shows overlap only, not cancellation or draining; message 18's `0024A680` gates on resource-record address membership and never touches the ticket pool. OV-29's cancellation/lifetime half gets a
  live instance, and a static follow-up owes what completes the orphan ticket.
- Message 16 after teardown: shipped play delivers to a torn-down widget. That answers OV-29 "lifetime: unsafe in practice", and page §3's "Common widget storage-freeing, real cancellation completion and external lifetimes remain outside this section's certification" gets the fact.
- Neither over the coverage: a bound on the cancellation half.
- Whether readiness came synchronously or from the watcher, and how long it took: **no claim changes**. Both branches are already specified (page §3, "Publication is earlier than readiness"), and the latency is host IO.

## 6. OV-33 — read-layer status word `0215EFF4`

**The writers (static).**
- The word is written only through the pointer `01F82CC0`:
  - `-1` at `001D6DD4` (archive route, `001D6D90`) and at `001D6FF4` (loose route, `001D6FB0`). Both come **before** the job is handed on (`001D6E51`/`001D707C` → `001A0BB0`).
  - The result at `001D6D7C`, in the completion `001D6D70`, which then clears the pointer.
- Every rip reference to `0215EFF4` is one of:
  - an address-take by the two issuers (`002DF719`, `002DF75F`, `002DF808`, `002DF838`);
  - one of the two reads: `0046DFE7`, the in-flight test, and `0046E0E0`, the result.
- `0046E030` is the only caller of `002DF780` and `0032E070` the only caller of `002DF6C0`, so all issues come from the pump.

**The route decides the thread.**
- `001D6FB0` passes `r8b = 1` to `001A0BB0`, which then calls `001A07B0` **inline**. So the loose-file read and its status write happen synchronously, inside the issue call.
- `001D6D90` passes `r8d = 0`, which appends the job under the lock and leaves it to the AsyncLoadManager thread. So the archive status is written from the worker.
- This contradicts `file-size-tables-fst.md` line 382, which calls `001D6FB0` "the asynchronous half".

**Judgement: timing settles no claim.** The pump polls. State 3 leaves as soon as the word is not -1, and nothing times out.
When a read completes is host disk speed.

**Value and branch observations that do settle claims.**
- (i) *A negative status other than -1.* Hit `0032E19C` with `eax < 0`, and record slot `+0x21` kind, `+0x24` index and `+0x40` callback.
  A hit with `+0x40 == 003DD850` is a shipped owner request that stays at state 3 with its pin. That is the stranding path page §7 describes ("Error-2 … State3 and source pin persist"), and it is OV-42/OV-33 reachability.
  Sources: the archive lookup gives `-2` when `0059D920` rejects (`001A0D57`–`001A0D87`); the loose route gives `-2` when `0059D900` says unset (`001A0ED2`).
- (ii) *An issue that writes no status.* The paths are:
  - `002DF7B9` taken, when the fst entry is -1;
  - `002DF801` taken, when `001D6F20` returns null;
  - the `001A1220()`-null gates `001D6DB9`/`001D6FD9`;
  - the null-out-pointer gates `001D6DC7`/`001D6FE7`, which are dead, because the pointer is always `lea 0215EFF4`.

  On these paths the pump still moves to state 2 and loops back to state 3 in the same pass (`0032E0FF`/`0032E103` → `0032E090`). It then reads whatever the previous read left: 0 at boot, since the word is BSS. **Lead, unverified here:** a refused request therefore completes as delivered (state 5) or failed (6) according to a stale value.
  The fst page says only "refuses the request", and the S-08 replay (`s08-opus-replay-queue-static-invariants`) planted the word. So publish the stale-value consequence statically first. Hits then show whether shipped play reaches it.
- (iii) *A writer census check.* Put a hardware write watch on `0215EFF4` (4 bytes). Any writing IP outside `{001D6DD4, 001D6FF4, 001D6D7C}` falsifies the static writer set.
  Record the thread as well, to confirm archive completions come from the worker.

**Positive control.** Any field load goes through the pump, so `0032E0F1` hits and `001D6D7C` writes with a value ≥ 0.

---

## Items judged to settle no database claim (for FRONTIER's scope ruling)

1. **OV-19 IO issuance/completion timing.** The order is static: callback strictly after the state-3 store (the `+0x40` callers are pump-only); FIFO across owners;
   nested pumps in `0032E870` only complete *other* requests. Timing is host disk speed; no page sentence depends on it.
   (The one order case with content is delete-before-completion at `003DD863`, which is reachability, not timing.)
2. **OV-29 callback timing, and synchronous versus deferred readiness.** Both branches are already specified. The latency is host IO.
   (The cancellation/teardown-before-readiness order case does settle a claim; see §5.)
3. **OV-33 status/loading timing.** The pump polls with no timeout, and the stamps are never read by the queue. The frame count is host IO.
   (The value cases (i)-(iii) in §6 do settle claims.)

## Contradictions / defects found while reading

1. **The contract's "only two functions address the registry" is false.**
   - *Where it appears.* `CONTRACT-encoded-id-space-and-class-registry.md` says: "The only functions that address the table are the rebase `0030B6A0` and `0030B270`." The batch-K Extension 2026-09-29 quotes it: "names the only two functions that address the registry".
   - *What the image shows.* `ripscan.py 01EEBCC0 01EEC1E8` finds **49 rip references in 28 functions** (`registry_ripscan.txt`). They include both packed handlers, both bitset handlers, the query dispatchers and `0030FAA0`/`0030FBE0`.
   - *The conclusion survives.* All 49 are reads. `registry_fn_stores.out` (control `0030B6F1` listed) shows no store into the registry by any of the 28 except the rebase's `+08`/`+20`/`+30`/`+40`, so "no count writer" still holds. The citation needs correcting, and the ruling asks the reviewer to re-run exactly this sweep.
2. **The rows do not cite EXP-079.** EXP-079 already observed `qword [01F83530]` = 0 in a loaded save (The Stepping) and at the title, but OV-5/OV-8 (c) cite neither it nor its bound.
3. **FRONTIER's "four packed classes" should be three** (5, 6, 7). See §2.
4. **`file-size-tables-fst.md` line 382 says `001D6FB0` is "the asynchronous half".** The image says otherwise: `001A0BB0` with `r8b = 1` runs `001A07B0` inline (`001A0BD9`–`001A0BDE`). Only `001D6D90` (`r8d = 0`) is queued to the worker.
5. **Lead, out of scope and unverified.** `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0` passes the backed-up packed word
   as a *relative* channel-1 delta: `movsx edx, word [...+0x4F84]` / `[+0x5004]`, with `r8d = 0` (`0030FAE7`, `0030FB37`). That word includes the reserved bits.
   A snapshot word carrying reserved bits would restore to a clamped 99 rather than the old total. `0030FBE0` unequips before it snapshots (`0030FC2F`), so this may never arise.

## Scripts and outputs (this directory)

| file | what | control |
|---|---|---|
| `registry_ripscan.txt` | `ripscan.py 01EEBCC0 01EEC1E8`: 49 references, 28 functions | — |
| `registry_fn_stores.py` / `.out` | every non-stack store in those 28 functions | `0030B6F1` listed: True |
| `regionA_word_stores.py` / `.out` | word stores and bulk writes in those functions | `002FD298`, `002FD31A` listed: True |
| `regionA_disp_writes.txt` | `dispscan.py 4748 4F0F --writes`: 9 hits, none on the state block | `control_5B0C.txt` finds `00233C83` |
| `ticket_done.py` | finds the ticket-completion compare sites (`002494F0`) | `00249410` listed: True |
