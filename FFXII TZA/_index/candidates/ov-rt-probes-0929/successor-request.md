# Successor request (ready to file): FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929

- **Replaces:** `FABLE-REQ-ASTRA-RT-REMAINDERS-0929`. Close that request as superseded by this one.
- **Answers:** `FRONTIER-REQ-FABLE-RT-REMAINDERS-PROBE-SITES`.
- **Companions:** `FABLE-REQ-ASTRA-OV10-OV42-REACHABILITY` and `FABLE-REQ-ASTRA-OV21-BANK-REACHABILITY`.
- **Links, does not duplicate:** `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME` (AQ-ARENA).
- **Board fields:** kind request · priority P3 · requester FABLE · assigned_to ASTRA · resource `request:fable/astra-rt-remainders-probes`.
- **Target:** the live remainders of register rows OV-5, OV-8, OV-16, OV-19, OV-29 and OV-33.
- **Scope:**
  - exact probe sites in ordinary shipped play, with no synthetic state;
  - read-only watches and breakpoints only;
  - one session can cover all items. Suggested coverage: title screen → Load (or New Game) → one field load with scripted events (any town) → an equip change → a shop visit → one battle → one area transition.
- **Standing rule (batch-K runtime rule):** a zero observation bounds reachability without proving absence. One hit answers that case. Each item names a positive control that must fire in the same session; if it does not fire, the zero is void.

Addresses include the image base `0x120000`, for image `73461d08…21F8`.

---

## question

### (1) OV-5 / OV-8 (c): a state base at or above 4 GiB

- **Probe.** Read qword `[01F83530]` in a loaded save. This is AQ-ARENA's remainder, so link and do not duplicate.
- **Known already.** EXP-079 read it as 0 at the title and after loading The Stepping, two samples each.
- **Decision.**
  - 0 in a loaded save: (c) bounded, still unreached.
  - Non-zero but below 4 GiB: the contract's "zero for the process life" is falsified, but (c) is still unreached.
  - At or above 4 GiB: (c) is reached. OV-5/OV-8 (c) closes ANSWERED (reachable), and the contract's 32-bit high-half-loss paths (query row arithmetic; `0030C71D add ebp, eax`) become live behaviour.

### (2) OV-5 / OV-8 (d): over-reservation — **WITHDRAWN 2026-09-30 (FABLE `t3b_ov58d_region_a.md`, applied by SWE2-FRONTIER)**

(d) is answered statically: every in-image writer to region A clamps `reserved <= total`, so the
probe below is no longer required. Kept as the record of what it would have shown.

- **What to read.** There are three packed-count classes, not four: 5 items, 6 equipment and 7 loot. Classes 14/15/18/19 have mutate handlers but no storage. Read these packed u16 words, low 10 bits = total and high 6 bits = reserved:
  - 64 words at `021B7054` (class 5);
  - 420 words at `021B70D4` (class 6);
  - 512 words at `021B741C` (class 7).
- **Comparison.** Flag every word where `(w >> 10) > (w & 0x3FF)`. This is the reader `002FD8D0` mode 0 (`002FD94B`–`002FD95B`) going negative.
- **When to read.**
  - Right after the load-path rebase returns: `00238A9E` in `SaveRuntime_RebindImageBackedGameplayState` `00238A80`, after its call to `0030B6A0` at `00238A99`. The other rebase caller is `00233C3A` in `00233C10`.
  - Again after the equip change, the shop and the battle.
- **Controls.**
  - qword `[01EEBCC8]` / `[01EEBD20]` / `[01EEBD78]` equal `021B7054` / `021B70D4` / `021B741C`, and qword `[02EBF190]` = `021B290C`. These are the rebased region pointers and the state block.
  - dword `[01EEBCFC]` / `[01EEBD54]` / `[01EEBDAC]` = `0x40` / `0x1A4` / `0x200`.
  - With anyone equipped, at least one class-6 word has `high6 >= 1`, because equipped copies are the reserved count. Print that count.
  - One class-5 word's low10 equals its Items-menu count; Potion is `021B7054`.
- **Decision.**
  - Present right after load: a loaded save carries over-reservation. (d) closes ANSWERED as "reachable only through save data". Static reading finds that every in-image writer clamps: `002FD150`, via `002FD27E`, `002FD2E9` and `002FD3D2`.
  - Appears after load: an unknown writer exists. Set a write watch on that word and report the writing IP.
  - None: consistent with the static finding. The row closes on the static answer once that is published; until then it is a bound.

### (3) OV-16: a notification key reused while an older same-key request is pending

- **The key** is (issuer channel, continuation offset).
  - *Made* in `00268850`, whose stack descriptor is at `rsp+0x20`: channel = byte `[rsp+0x23]` (from `[r15+0x11]`), offset = dword `[rsp+0x30]` (`ebp - [r15+0x58]`), mode = byte `[rsp+0x21]`. `r15` is the issuer actor.
  - *Filed* on the requester's detached list by the posters `003DBE5F` (start) and `003DC122` (end). There, `rcx` is the requester, the channel is byte `[rdx+2]` and the offset is dword `[rdx+0x10]`.
  - *Matched* by `003DC050` (`003DC083` offset, `003DC092` channel), from `0025E09F` / `0025B435`. The result is tested at `0025E0A4` / `0025B43A`; `0xFF` means not found.
- **Probe A (single site).** At `002689E3`, only when mode ∈ {2, 3}, walk the issuer's detached list and count entries whose key equals the new key:
  - start at `b = byte [r15+0x61]`;
  - while `b != 0xFF` and fewer than `byte [r15+0x89]+2` steps: `e = qword [r15+0xA0] + b*0x14`; compare `sbyte [e+2]` with byte `[rsp+0x23]` and dword `[e+0xC]` with dword `[rsp+0x30]`; then `b = byte [e]`.

  A count ≥ 1 is the hit. Record issuer, key, mode, the count, and the return at `00268A1D` or `00268A3B`.
- **Probe B (log, for the not-yet-posted case).** Log three events:
  - arm `002689E3`: issuer, key, mode;
  - post `003DBE5F` / `003DC122`: requester, key, and byte `[rcx+0x60]` = the entry index;
  - consume `0025E0A4` / `0025B43A` when `eax != 0xFF`: actor, key, `eax`.

  Per (issuer, key) the sequence must be arm → post → consume. Two arms with no consume between them, or a consumed entry posted before the latest arm, is a hit.
- **Control.** At least one complete arm → post → consume triple. The shipped scripts call `sysReqew` 10,007 times and `sysReqsw` 3,067 times, so any scripted field event produces one.
- **Decision.**
  - Hit: OV-16 closes ANSWERED ("occurs"). The instance goes under actor-request page §4, and a faithful reimplementation must reproduce the aliasing.
  - Zero with the control passing: a bound; OV-16 stays OPEN.

### (4) OV-19: owner-request issue and completion

- **Sites.**
  - Arm `003DDA20`: state 2 at `003DDA4E`.
  - Submit `003DDAB9`: the call to `0032E620`. State 3 at `003DDABE`.
  - File issue: pump `0032E0F1`. It is an owner request when slot `+0x40` == `003DD850`; slot `+0x60` is the owner.
  - Completion `003DD850`, with `ecx` = owner: state 4 at `003DD8B5`, or state 0 at `003DD88E` after a deferred free.
  - Delete `003DD420`: state 5 at `003DD490`.
- **FABLE's judgement: the timing settles no database claim.**
  - The order is fixed statically. The completion follows the owner's own state-3 store, because the slot's `+0x40` is called only from the pump. Across owners the order is queue FIFO.
  - The frame count depends only on the AsyncLoadManager worker thread and the host disk.
  - FRONTIER is asked to rule this timing half out of scope.
- **The one order case that does add a fact.** Count entries to `003DD850` with dword `[rdi+4] == 5` (compare at `003DD863`): the owner was deleted while its read was in flight, so the deferred-free branch `003DD878` runs in shipped play. Run this only if the half is kept.
- **Control.** `003DDABE` and `003DD8B5` hit during a field load.

### (5) OV-29: title-asset callback order and cancellation

- **Sites.** In handler `00394070`:
  - message 1 → `003940F5`: the publish to `02AEE4C0`;
  - message 16 → `003940E3`: ready bit 0;
  - message 18 → `00394097`: teardown, which zeroes `02AEE4C0` at `003940D2`.

  Message 16 is sent by `00249410` at `0024947D` (synchronous, when the counts are equal at submit) or by `002494F0` at `0024955D` (later, from the watcher `00248700`).
- **Probe.**
  - At `00394097`, scan the 12 tickets at `02090790`, stride `0x20`, for one with `(dword [t] & 1) && qword [t+8] == rbx`. That is a ticket still pending at teardown. Record `word [t+0x18]`, `word [t+0x1A]` and `dword [rbx+0xC0] & 1`.
  - At `0024947D`, `0024955D` and `003940E3`, record the owner. A delivery to a widget already torn down is message 16 after teardown.
- **Control.** `003940F5` and `003940E3` at the title; `fsttl_initialize` holds until bit 0 is set. `00394097`, or `02AEE4C0` returning to 0, when leaving the title.
- **Decision.**
  - A pending ticket at teardown: the cancellation path runs in shipped play.
  - Message 16 after teardown: shipped play delivers to a torn-down widget. Either result answers OV-29's cancellation/lifetime half.
  - Neither: a bound on that half.
- **Settles no claim, and FRONTIER is asked to rule it out of scope:** whether readiness came synchronously or later, and how long it took. Both branches are already specified on the page, and the latency is host IO.

### (6) OV-33: the read-layer status word `0215EFF4`

- **The writers, statically**, all through the pointer `01F82CC0`:
  - `-1` at `001D6DD4` (archive route) and at `001D6FF4` (loose route), both before the job is handed on;
  - the result at `001D6D7C`. That write is inline for the loose route and on the AsyncLoadManager worker for the archive route.
- **Readers:** `0046DFE7` (in flight) and `0046E0E0` (the result).
- **Probes.**
  - (i) A hardware write watch on `0215EFF4` (4 bytes). Record the IP, value and thread. Any IP outside {`001D6DD4`, `001D6FF4`, `001D6D7C`} falsifies the writer set.
  - (ii) At `0032E19C`, the return of `0046E0E0`, record `eax` when it is negative, together with slot `+0x21` / `+0x24` / `+0x40`. A hit with `+0x40 == 003DD850` is a shipped owner request stranded at state 3 with its source pinned (indexed-source page §7). That bears on OV-33 and OV-42.
  - (iii) Count the issue exits that write no status: `002DF7B9` taken (fst entry -1), `002DF801` taken (`001D6F20` null), `001D6DB9` / `001D6FD9` taken (`001A1220` null). On these paths the pump completes the request from the previous status value.
- **Control.** During the field load, `0032E0F1` hits and `001D6D7C` writes values ≥ 0.
- **Settles no claim, and FRONTIER is asked to rule it out of scope:** the time between issue and completion, and the loading-state duration. The pump polls, has no timeout, and never reads its counter stamps.

## known_evidence

- The six pages' SECTION reviews, and OPUS's falsification passes of 2026-09-29.
- `batch-K-scope-rulings.md` Extension 2026-09-29 (runtime rule).
- `CONTRACT-encoded-id-space-and-class-registry.md` §7 (the base `01F83530`); EXP-079 (base 0 in four samples).
- The query-record page §2 and §7; encoded-id page §2.2–2.7.
- Actor-request page §3–§5 and falsification A3; indexed-source page §6–§7; resource-request-queue §2.3 and §8; title-asset page §3 and §8.
- FABLE reader notes: `Database/Tools/work/FABLE/ovprobes/notes.md`, with the registry store census and control outputs.

## missing_information

- Per item, the observed hits and counts with the recorded fields, the positive-control result and the coverage walked.
- For (1), the AQ-ARENA value.

## why_it_matters

- These are the last runtime halves of the register.
- Each probe settles a named row sentence:
  - OV-5/8 (c) and (d) reachability;
  - OV-16 key aliasing, a reconstruction requirement;
  - OV-29 teardown-before-readiness lifetime;
  - OV-33 stranded owners and the stale-status completions;
  - OV-19 deferred free.
- The timing halves of OV-19, OV-29 and OV-33 are flagged as settling no claim, pending FRONTIER's scope ruling.

## what_is_blocked

- OV-5 and OV-8: (c) is linked to AQ-ARENA; (d) stays open.
- OV-16.
- OV-19: the timing half.
- OV-29.
- OV-33: the timing half.

## completion

- Observations with coverage and positive controls, per item.
- Or FRONTIER's scope ruling on the three timing halves, plus observations for the rest.
