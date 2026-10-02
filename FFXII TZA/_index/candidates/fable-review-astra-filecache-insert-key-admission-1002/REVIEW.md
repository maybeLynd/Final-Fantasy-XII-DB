# FABLE review: ASTRA filecache-insert-key-admission

- **Packet:** [filecache-insert-key-admission README](../../../_experiments/evidence/filecache-insert-key-admission/README.md)
- **Producer commit:** `1b2154feb`. The manifest sha256 begins `6efd33a9b850a11b` and all 96 members hash as listed.
  The packet's seven captured range hashes (`source-01.json`, `source-02.json`) equal the certified image's bytes.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every interface, frame, comparison, copy-site and balancing-span claim
  re-derives at the bytes, and the byte totals match (653 + 1364). The narrowings add facts the packet leaves out:
  undefined bytes at node+24h, the find-or-insert exits, the allocation gate and the guard's real test. They do not
  contradict anything the packet states.

## Method

[rv_insert.py](rv_insert.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5, copied
unchanged from the earlier FABLE reviews). It does not import ASTRA's `prove.py`, its capture drivers or the shared
role adapter `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d08…`) and decodes the seven bodies completely. Six are checked against `.pdata`.
  The leaf `0016D840` has no `.pdata` record, so it is bounded by its closed CFG, its single final `ret`, and int3
  padding before it and up to the next record at `0016DA60`.
- It builds a local CFG from direct branches for each body.
- For every key carrier it takes a register-write census, so each carrier must have exactly the expected `mov` writers.
- For every key comparison it finds the flag consumer and requires an unsigned or equality condition.
- It does exact frame arithmetic for the `0020B680` prologue and finds stack-write overlaps on every path from entry
  to the `0020B5F0` call (forward reach intersected with backward reach).
- It identifies each 16-byte copy site structurally: the 30h allocator call, `add rax, 0x20` / `je` past the store, a
  load from the pair register, a store to `[rax]`, and the node passed in rcx to `0016D840`.
- It records the width and span of every write in `0016D840`.
- Controls patch a private in-memory copy of the image. The exe on disk is never written.

Raw output: [rv_insert.out](rv_insert.out).

## Re-derived (81 checks, 81 PASS, 0 FAIL; 15 controls among them)

### Bodies

| Claim | Result |
|---|---|
| `001D6A20..001D6A6D` (77 B), `0020B680..0020B83B` (443 B), `0020B5F0..0020B675` (133 B) total 653 B | PASS: each decodes exactly and one `.pdata` record covers each |
| `001AE9B0..001AEAFC` (332 B), `001AE850..001AE9A8` (344 B), `0020BA70..0020BB0C` (156 B), `0016D840` .. + 0x214 (532 B) total 1364 B | PASS: the first three tile `.pdata` (3, 1 and 1 records; `001AE9B0` is a root plus two chained records). `0016D840` has no record. It is bounded by int3 at `0016D840` - 1 and int3 from `0016D840` + 0x214 up to the next record at `0016DA60`. |
| All seven local CFGs are closed | PASS: there is no tail or out-of-body branch, and each body's single `ret` is its last instruction |

### Claim 1: `001D6A20`

| Claim | Result |
|---|---|
| ECX is the key, saved to EBP and forwarded in EDX | PASS: `mov ebp, ecx` (1D6A3D) and `mov edx, ebp` (1D6A51). Apart from the epilogue restore, ebp has only that writer and edx has only 1D6A51. |
| RDX, R8D and R9D are distinct carriers | PASS: rdx goes to rsi and then to r8 (64-bit pointer). r8d goes to edi and then to r9d (value32). r9d goes to ebx and then to `[rsp+20h]`, which is the callee's entry SP+28h, the fifth argument (frame 38h). These are four distinct callee-saved registers, and none is rewritten before its forward. |
| The getter supplies the receiver | PASS: `call 0020C700`, then `mov rcx, rax` (1D6A44). There is no rcx write before `call 0020B680`. |
| No masking or hashing | PASS: no `and`, `bt*`, shift or arithmetic writes rbp or rdx anywhere in the body |

### Claim 2: `0020B680`

| Claim | Result |
|---|---|
| Key saved as a DWORD at entry SP+10h | PASS: `mov dword ptr [rsp+0x10], edx` is the first instruction, before any push |
| Seven pushes + SUB 40h put the home at SP+88h and the fifth argument at SP+A0h | PASS: the frame is 78h, so 88h − 78h = 10h and A0h − 78h = 28h. rsp changes only in the prologue and epilogue. |
| Key in EDX/EBP | PASS: `mov ebp, edx` (20B6AA). Its only other writer is the epilogue pop. |
| Unsigned full-DWORD key compares | PASS: there are 2 key compares, both DWORD against node+20h: `cmp [rax+20h], ebp` → `jb`, and `cmp ebp, [rbx+20h]` → `jae` |
| Existing-key arm passes EDX = EBP to `0020C300` | PASS: 20B721 `mov edx, ebp`, rcx = receiver, fifth argument = kind from SP+A0h. This arm never calls `0020B5F0`. |
| New arm passes the saved DWORD's address to `0020B5F0` | PASS: 20B7D0 `lea rdx, [rsp+0x88]` and rcx = receiver+20h |
| No own stack write overlaps the key home before that call | PASS: 76 instructions lie on entry → 20B7DC paths. Their stack writes are 30h/8, 90h/8 and 80h/8, and none touches 88h..8Bh. |

### Claim 3: `0020B5F0`

| Claim | Result |
|---|---|
| Reads the full DWORD | PASS: there are exactly three key reads through rdx (20B607, 20B62F, 20B633), all 4 B. rdx is not rewritten. |
| Unsigned JB/JAE | PASS: `cmp [r8+20h], r9d` → `jb`; `cmp [rdx], ecx` → `jae`. r9 is written only at the key load and at the pair `lea`. |
| Pair+0 = key, QWORD pair+8 = 0, pair passed to `001AE9B0` | PASS: `mov [rsp+30h], ecx` and `mov qword [rsp+38h], 0`, with no rcx write between the load and the store. Then r9 = rsp+30h, rcx = map, rdx = out slot rsp+60h, and `call 001AE9B0`. |
| Returned value slot is node+28h | PASS: `mov rax, [rsp+60h]; add rax, 0x28`. See narrowing 2: this is also the existing-key exit. |

### Claim 4: the five copy sites

| Site | Body | Pair register | Node register |
|---|---|---|---|
| 1AEA28 / 1AEA2C | `001AE9B0` | r14 (from r9) | rbp |
| 1AEAA4 / 1AEAA8 | `001AE9B0` | r14 | r13 |
| 1AE91A / 1AE91E | `001AE850` | r15 (from r8) | r14 |
| 1AE95B / 1AE95F | `001AE850` | r15 | rbx |
| 20BAD1 / 20BAD5 | `0020BA70` | rbp (from r9) | r14 |

PASS. These three bodies contain exactly five 16-byte loads and five 16-byte stores. Every site follows the same
pattern:

1. The allocator callback `call [vtbl+10h]` is made with edx = 30h.
2. The node register is set to rax.
3. `add rax, 0x20` / `je` skips only the store.
4. `movups xmm0, [pair]` is followed by `movups [rax], xmm0`.
5. The node is passed in rcx to `0016D840`.

`001AE9B0` forwards the same pair (`mov r9, r14` to `0020BA70`, `mov r8, r14` to `001AE850`). Each pair register has a
single writer, and nothing is written through a pair register. All 11 DWORD compares in these bodies have unsigned or
equality consumers. Apart from the copy, no write in the three bodies lands in node+20h..2Fh.

### Claim 5: `0016D840`

| Claim | Result |
|---|---|
| Complete leaf with no calls | PASS: there is no call, no indirect jump and no rsp use, and the CFG is closed |
| Every write lies in 0h..19h | PASS: there are 49 writes, all `[reg+disp]` with no index. Their spans are only 0–8, 8–10h, 10h–18h and 18h–19h, so none reaches 20h..30h. The new node gets +10h = parent, +0/+8 = 0 and colour byte +18h = 0. |

### Beyond the packet

These findings are used only to narrow the stability premise:

- `0016D6D0` (68 B) and `0016D720` (94 B) are read-only leaves, with no call and no memory write. They are the only
  direct callees on any entry → copy-site path, including `001AE9B0`'s paths to its two forwards.
- The only other callee before a copy is the 30h allocator callback.

## Controls (15, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy, with the sha check off, passes all 62 image checks. The
packet-bytes cross-check is kept out of the control check set, so no control fails for that trivial reason.

1. 20B60A alignment nop → `btr r9d, 31`. Fails "r9 written only at the key load and the pair address".
2. 1D6A51 `mov edx, ebp` → `mov edx, edi`. Fails the 1D6A20 forwarding check.
3. 20B6AA `mov ebp, edx` → `and ebp, edx`. Fails "ebp = edx; no other writer".
4. 20B6CB `jb` → `jl`. Fails "every key compare has an unsigned consumer".
5. 20B614 `jb` → `jl`. Fails the 20B5F0 unsigned-compare check.
6. Entry key home `[rsp+10h]` → `[rsp+14h]`. Fails the entry-store check.
7. 20B7D0 `lea rdx, [rsp+88h]` → `[rsp+8Ch]`. Fails the new-arm key-address check.
8. 20B74E spill `[rsp+80h]` → `[rsp+84h]`. Fails "no own stack write overlaps 88h..8Bh".
9. Pair+8 seed `[rsp+38h]` → `[rsp+40h]`. Fails the pair checks.
10. 1AEA22 copy store node+20h → node+18h. Fails the five-site copy check.
11. 1AE91A copy loads `[r14]` (node) instead of `[r15]` (pair). Fails the five-site copy check.
12. 16D84D colour store +18h → +20h. Fails "every write lies in 0h..19h".
13. 16D885 alignment nop → `call 0016D6D0`. Fails "no call".
14. 20B66C returned slot +28h → +20h. Fails the return-slot check.
15. 16D6D0 `mov rax, rcx` → `mov [rcx], rax`. Fails "the step helpers are read-only leaves".

The packet's controls-01 and controls-02 CLI refusals were not repeated. These 15 are this review's replacements.

## Narrowings

1. **node+24h..27h is undefined.** `0020B5F0` writes only pair+0 (DWORD) and pair+8 (QWORD). Its stack writes are
   exactly 50h/8, 30h/4, 20h/1 and 38h/8, so pair+4..+7 (rsp+34h..37h) is never written. Every 16-byte copy carries
   those four stale stack bytes into node+24h..27h. The packet correctly says the key is the DWORD at node+20h.
   Consumers must not read node+20h as a QWORD key, and must not assume node+24h is zero.
2. **`0020B5F0` is find-or-insert, not insert.** It repeats the lookup. If the key is present, 20B631 `jae` goes to
   20B66C and returns that existing node+28h with no copy. `001AE850` behaves the same way: its 1AE97F exit stores
   the found node with flag 0 and makes no copy. Whether a fresh node is created therefore depends on three things:
   - `0020B680`'s earlier absence test;
   - the bracket from `0020B6B3` (call `005CD4F0`) to `0020B7E8` (call `005CD820`);
   - no interference, including from the `001BA860` call made in between.

   If the key is present, 20B7E1 overwrites the existing node's value pointer. The packet's "returned value slot is
   node+28h" is true for both exits.
3. **The insertion is gated on `001BA860`.** If it returns null, 20B75B skips `0020B5F0` entirely, so no map
   insertion happens. Execution still continues to `00210EC0` / `00217A60` and adds r14 to receiver+90h. The packet
   does not state this gate.
4. **The copy guard does not check for NULL.** `add rax, 0x20; je` skips the copy only when node+20h == 0, which means
   node == −20h. A NULL allocator result is not caught, and the store would go to address 20h. The packet's "valid
   fresh nonwrapping 30h node" premise covers this. Consumers must not describe the guard as a null check.
5. **The existing-key arm also calls `0020B0F0`.** It calls `0020B0F0` with (receiver, `[pointer]`) before
   `0020C300`. The packet's table row names only `0020C300`, although its OPUS line does list `0020B0F0`.
6. **The stability premise is narrower than stated, but the packet does not say so.** Between the pair's creation
   and any copy, the only callees are the read-only leaves `0016D6D0` / `0016D720` and the allocator callback. So the
   "stable input-pair contents" premise reduces to the allocator callback plus external interference. The key home is
   read three times inside `0020B5F0` with no call in between. This strengthens the packet's argument and does not
   widen what is awarded.
7. **`0016D840` completeness rests on a different method.** There is no `.pdata` record, so completeness here comes
   from the closed CFG, the single final `ret` and the int3 padding. The packet's "complete" stands.
8. **Carrier widths.** R8 and R9 are forwarded as 32-bit values (`mov edi, r8d` / `mov ebx, r9d`), so their upper
   halves are dropped. RDX stays 64-bit. In `0020B680` it is a pointer to a QWORD, read again at several sites through
   r12. This is consistent with the packet's "pointer preservation does not prove source-memory stability".

## Scope (kept as the packet states it)

This review supports conditional static facts only. Every one of them holds only under these premises:

- a stable input pair and readable private frames;
- valid, fresh, disjoint 30h node allocations at non-wrapping addresses;
- valid, ordered, pointer-linked nodes and header;
- normal returns and ABI register preservation, including that `0020C700` preserves rbx/rbp/rsi/rdi;
- no interference.

Pointer-carrier preservation does not prove that the source memory stays stable.

This review does not award:

- natural high-bit inputs or the original callers' key domain (actual callers may still restrict every key to 31 bits);
- allocator-callback effects (`[map+30h]` vtable +10h);
- `001BA860`, `00210EC0`, `00217A60`, or the lock pair `005CD4F0` / `005CD820`;
- replacement through `0020B0F0` / `0020C300`;
- eviction, lifetime, collisions, the archive-missing candidates or cache occupancy;
- the tree's ordering direction (only that every key compare is unsigned).

run: `rv_insert.py` at 77356569f (81 checks, 81 PASS, 0 FAIL, 15 controls; output identical to [`rv_insert.out`](rv_insert.out))
