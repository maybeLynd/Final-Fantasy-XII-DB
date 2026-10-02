# FABLE review: ASTRA notification-retirement-order

- **Packet:** [notification-retirement-order README](../../../_experiments/evidence/notification-retirement-order/README.md)
- **Producer commit:** `e46090c35`. The manifest sha256 begins `814b83ad01338551` and equals the manifest committed at
  `e46090c35`. All 41 members hash as listed. The packet's 8 captured range hashes (`source-01.json`) and the 8
  entries of `retained-body-identities.json` (lengths sum 1041) equal the certified image's bytes.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every order, store, gate, return and byte-total claim re-derives at the
  bytes over the eight complete bodies (1041 B). The conditional lost-notification composition holds under the
  premises below. The narrowings make three gates explicit that the packet folds into "valid head mode 3", and
  add one return path the packet's EAX sentence does not name. None contradicts the packet.

## Method

[rv_order.py](rv_order.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the filecache-route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It does not import ASTRA's
`prove.py`, `capture.py`, `control.py`, its freeze or publication scripts, or the shared role adapter
`reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes the eight bodies completely.
  - Three bodies have exactly one `.pdata` record each: `003587C0`, `003DB2A0`, `003DC0D0`.
  - `003DBCF0` has three records that tile its 194 B: an unchained one at the entry and two CHAININFO records
    (flags 4) at `003DBCF0` + 0x31 and + 0x57, both rooted at `003DBCF0`.
  - Four leaves have no record: `00263FF0`, `003DB550`, `003DB650`, `003DC1B0`. Each is bounded by its closed CFG, a
    final `ret`, int3 padding after it, and int3 or the neighbouring record's end before it.
- It builds a local CFG from direct branches for each body and takes dominance and post-dominance for the order
  claim.
- It censuses every write that could reach actor+60h before the attempt, in the removal and in every callee on the
  way to the capacity read.
- It runs its own reverse reaching-definition walk for every return value a claim names. A call counts as a
  definition.
- It does exact descriptor arithmetic for the posted stack descriptor.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_order.out](rv_order.out).

## Re-derived (74 checks, 74 PASS, 0 FAIL; 15 controls among them)

### Bodies and totals

| Claim | Result |
|---|---|
| Eight complete original bodies, 1041 B | PASS: 21 + 50 + 378 + 35 + 133 + 194 + 93 + 137 = 1041. Each decodes exactly and has a closed local CFG whose last instruction is a `ret`. |
| `.pdata` extents | PASS: one record each for `003587C0` + 0x32, `003DB2A0` + 0x17A and `003DC0D0` + 0x5D. `003DBCF0` + 0xC2 is a three-record chain rooted at its entry. The four leaves have none; `003DB550` begins exactly where the record before it ends. |
| Captured bytes | PASS: all 8 packet range hashes equal the image. The control check set leaves this check out. |

### The order (claim 1)

| Claim | Result |
|---|---|
| A head removal unhooks the links and clears entry+11h | PASS: `003DB2A0` + 0x8B (`cmp esi, eax` against the list head) branches straight to the unhook call at `003DB2A0` + 0xA6 → `003DC1B0`. The unhook writes three bytes, all through entry-pool pointers derived from `[actor+0A0h]`: next.prev = prev, prev.next = next, entry+11h = 0. The clear dominates its single `ret`. It writes nothing through the actor pointer and makes no call. |
| The end notification is attempted next | PASS: the unhook dominates the attempt at `003DB2A0` + 0xDD → `003DC0D0`, whose call to `003DBCF0` is at `003DC0D0` + 0x52. |
| Free-list relink and head publish come later | PASS: the relink call (`003DB2A0` + 0x150 → `003DB650`) and the head publish (`003DB2A0` + 0x159, `mov byte ptr [rbx + 0x60], sil`) both post-dominate the attempt's return (`003DB2A0` + 0xE2). No path leads from them back to the attempt. |
| Nothing frees the slot before the attempt | PASS: before the attempt, the removal writes nothing that overlaps actor+60h. Its only actor+60h write is the publish. `003DB650` writes only entry bytes. |

### Admission and capacity (claim 2)

| Claim | Result |
|---|---|
| The descriptor selects function 0 | PASS: at `[rsp+20h]`, `003DC0D0` stores word 402h, entry+3, dword 80000000h at +4, byte 1, entry+8 and entry+0Ch. The WORD at +4 is 0. No other store overlaps +4..+5. `003DBCF0` + 0x11 reads it as `movzx r9d, word ptr [rdx + 4]`. |
| Function-0 admission precedes capacity | PASS: `003DBCF0` + 0x1C `cmp r9d, dword ptr [rax]` with rax = [actor+48h], then an unsigned `jb`. If id >= count, EAX = 3. This compare dominates the capacity read at `003DBCF0` + 0x36, and that read cannot be reached from the result-3 path. |
| A free head of FF returns 2 with no calls and no own-object writes | PASS: `003DBCF0` + 0x36 `movzx edi, byte ptr [rcx + 0x60]`, with rcx being the incoming actor and unwritten before it. If it is FF, EAX = 2 at `003DBCF0` + 0x42. The result-3 and result-2 paths make no call and write only home slots on their own stack. |
| A non-FF head reaches the insertion helpers | PASS: `003DC130` and `003DB7A0` are called first. `003DB650`, `00263FF0` and `00263E40` follow only when `003DB7A0` returns 3. These are the packet's five sites. Their success and effects are not derived here, matching the packet. |
| Return provenance of `003DBCF0` | PASS (reverse definitions): the three `ret`s take EAX from the constant 3, the constant 2, and `mov eax, ebp` (= the `003DB7A0` result) respectively. |

### The conditional loss (claim 3)

| Claim | Result |
|---|---|
| Requester resolution | PASS: `003DC0D0` passes zero-extended word entry+6 and dword entry+8 to `003587C0`. The requester is `[list + 8 + ordinal*8]`, where list = [slot+8] and slot = 2098E10h + (int)entry+8 × 288h. A NULL list or an out-of-range ordinal gives 0 (signed `jge` at `003587C0` + 0x1D), and a NULL requester skips the post. |
| The same actor's free head is unchanged up to the capacity read | PASS: from removal entry to `003DBCF0` + 0x36, nothing writes actor+60h through the actor pointer. That covers the removal census, plus `003DC1B0`, `003DB550`, `003DC0D0`, `003587C0` and `00263FF0`, which write no actor field. |
| Flags 0/1 skip the reference helper | PASS: `003DB2A0` + 0xE6 `cmp al, 2` with an unsigned `jb` skips the `00263050` call at `003DB2A0` + 0xF2. That call is placed after the attempt. |

### The outer return (claim 4)

| Claim | Result |
|---|---|
| EAX = saved entry+12h bit 0, not a delivery result | PASS: r14d = `movzx` entry+12h, then `and 1` (`003DB2A0` + 0x4A, + 0x4F), before any call. r14 has no other writer except the restore. The reverse definitions of EAX at the final `ret` are exactly `003DB2A0` + 0x162 `mov eax, r14d`. The attempt's result is overwritten unread by the next instruction. See narrowing 1 for the other `ret`. |

## Controls (15, each must FAIL a named check on a privately patched image; all did)

A null control runs first: an unchanged private copy, with the sha check off, passes all 51 image checks. The
packet-integrity checks are kept out of the control check set.

1. The attempt call at `003DB2A0` + 0xDD → five nops. Fails the gate check and the discarded-result check.
2. `003DB2A0` + 0x53 → `mov [rbx+60h], sil; nop`, which publishes the slot before the attempt. Fails the actor+60h
   census and the composition check.
3. `003DB2A0` + 0x106 `jne` retargeted to `003DB2A0` + 0x15D, so a path skips the relink and the publish. Fails the
   post-dominance check.
4. `and r14d, 1` → `and r14d, 3`. Fails the return-carrier check.
5. `mov eax, r14d` → `nop; mov eax, ebp`. Fails the reverse-definition check.
6. Descriptor dword 80000000h → 80000001h, which selects function 1. Fails the descriptor check.
7. Admission `jb` → `jl`, a signed compare. Fails the admission check.
8. Capacity `jne` → `je`. Fails the capacity check.
9. `mov eax, 2` → `call 003DC130`. Fails three checks: capacity, no-call paths, and helper list.
10. The unhook clear `[r8+11h]` → `[r8+12h]`. Fails the unhook census.
11. The mode gate `cmp …, 3` → `4`. Fails the gate check.
12. The flags `jb` → two nops, so `00263050` runs for flags 0/1. Fails the flags check.
13. The unhook's next.prev store → `mov [r9+60h], r11b`, a write to the free head. Fails the unhook census and the
    composition check.
14. The capacity read `[rcx+60h]` → `[rcx+61h]`. Fails the capacity check.
15. The requester sentinel 8000h → 8001h. Fails the gate check.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's three CLI refusals and five
static countermodels were not repeated. These 15 replace them for this review.

## Narrowings

1. **The index-FF return.** `003DB2A0` returns a constant 1 at `003DB2A0` + 0x18 when the index is `0xFF`. That
   path reads no entry. "Removal EAX = entry+12h bit 0" holds on every other path, which all end in the shared
   `003DB2A0` + 0x162.
2. **The attempt has three gates beyond "mode 3".** All are in the bytes, and the packet's "valid head mode 3"
   leaves them unstated:
   - **A non-negative signed channel byte entry+2.** The `jns` at `003DB2A0` + 0xAD decides it. A negative channel,
     or mode 4, takes the detached-list branch, which relinks with no notification call.
   - **A requester word entry+6 that is not 8000h.** This is a 16-bit compare.
   - **A non-NULL requester resolution.** `003DC0D0` + 0x18 decides it.

   The conditional loss also needs the requester's function-table pointer [actor+48h] to be readable and its count
   non-zero. The packet states the count.
3. **"Same actor" means pointer identity at the resolver.** The requester is the slot-table entry for
   (entry+8, entry+6). The premise is that this pointer equals the removing actor. It is not a comparison of
   ordinals that the code performs.
4. **The observer site.** `003DBCF0` is also reached from other submitters. A probe at `003DBCF0` + 0x36 / + 0x42
   counts for this question only when its return origin is `003DC0D0` + 0x57 and its rcx is the removing actor.
   The packet names both; this review keeps them as joint conditions.

**What this review does not narrow.**

- **The flags premise.** `00263050` runs only after the attempt has returned, so for any flags value it cannot
  change whether the attempt was refused. The flags 0/1 premise is needed only to keep the code between the attempt
  and the relink/return free of an opaque helper. The packet's flags 0/1 scope is kept as stated.
- **Outside the packet: the non-head walk.** For a non-head index, the "walk" at `003DB2A0` + 0x86 to + 0x9F passes
  the removed index itself to `003DB550` on every iteration (`mov edx, esi`). It does not pass the walked index.
  - If the entry's own next byte is `0xFF`, it returns with no unlink.
  - If that byte equals the entry's own index, it unlinks.
  - Otherwise it repeats the same iteration.

  The record page's removal table calls this "linear from the head … O(list)". That is routed to its lead (see
  `consumption-draft.md`). It is not consumed from this packet, which claims head removal only.

## Limits (kept as the packet states them)

This review supports conditional static facts only, under these premises:

- valid, initialized, disjoint actor / entry-pool / caller-frame storage;
- normal ABI and returns;
- no concurrent writer.

The following remain open and are not awarded:

- a naturally reached full self-pool, or a same-actor requester in shipped play;
- actor lifetime and reuse, concurrent mutation, and cancel / re-entry scheduling;
- the success and effects of the insertion helpers on a non-FF free head;
- the effects of `00263050` for flags ≥ 2;
- all callers of the removal and all callers of `003DBCF0`.

run: `rv_order.py` at c0bf8acd5 (74 checks, 74 PASS, 0 FAIL, 15 controls; output identical to [`rv_order.out`](rv_order.out))
