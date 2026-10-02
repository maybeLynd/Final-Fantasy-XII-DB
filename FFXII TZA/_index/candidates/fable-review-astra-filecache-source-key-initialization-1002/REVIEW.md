# FABLE review: ASTRA filecache-source-key-initialization

- **Packet:** [filecache-source-key-initialization README](../../../_experiments/evidence/filecache-source-key-initialization/README.md)
- **Producer commit:** `50dd4cc33`. The manifest sha256 begins `d5cc7655d068357e` and all 43 members hash as listed.
  The packet's three captured range hashes (`source-01.json`) equal the certified image's bytes, and its three ranges
  are exactly the three `.pdata` bodies.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** All six claims re-derive at the bytes: the three bodies and their 377-byte
  total, both constructor zero stores and their dominance over the resolver call, the +20h receiver bias, and the
  rebind's lack of any direct key reset (its five full-width writes are listed below). The narrowings make the
  rebind and argument facts more exact and limit what the resolver corroboration shows. None contradicts the packet.

## Method

[rv_srckey.py](rv_srckey.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5, copied
unchanged from the earlier FABLE reviews). It does not import ASTRA's `prove.py`, its capture drivers or the shared
role adapter `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d08…`, image base 120000h included in every address) and decodes the three
  bodies completely. Each body is checked against its `.pdata` record, and int3 padding must lie on both sides.
- It builds a local CFG from direct branches for each body. Dominance is computed on that CFG, and the
  entry-to-call path set is compared with the linear prefix.
- It runs a small forward data-flow over each CFG. Registers are tracked as object + k, stack + k, incoming argument
  or constant. The meet keeps only facts that agree on every edge. At a call the Win64 volatile registers are
  dropped and the nonvolatile ones are kept (the normal-ABI premise).
- Every memory write is resolved against that state to a byte interval [off, off + width) on the object or the
  stack. A write through a biased alias (rcx = object + 20h) therefore lands at its true offset. Any write that does
  not resolve counts against the "no overlap" checks.
- Controls patch a private in-memory copy of the image. Each control names the check that must fail, and the boundary
  control also names one that must not fail. The exe on disk is never written.

Raw output: [rv_srckey.out](rv_srckey.out).

## Re-derived (56 checks, 56 PASS, 0 FAIL; null control + 14 controls among them)

### Claim 1: bodies

| Claim | Result |
|---|---|
| `00597930` + 0x3B (59 B), `00597970` + 0xA2 (162 B), `0059ED70` + 0x9C (156 B), total 377 B | PASS: each decodes exactly, one `.pdata` record covers each, and int3 lies before the entry and at the end |
| Three complete local CFGs | PASS: there is no tail or out-of-body branch, and each body's single `ret` is its last instruction |

### Claim 2: constructor zero stores dominate the resolver call

| Claim | Result |
|---|---|
| `00597930` writes DWORD 0 to record+28h before calling `0059EE90` | PASS: 597951 `mov dword ptr [rcx + 0x28], eax`. The carrier eax has a single earlier writer, 597936 `xor eax, eax`. The store dominates the call at 59795D, and the entry → call path set equals the 12-instruction linear prefix. No later write in the body overlaps 28h..2Bh, before or after the call. |
| `00597970` writes DWORD 0 to reader+48h before calling `0059EE90` | PASS: 5979A3 `mov dword ptr [rcx + 0x48], ebp`. The carrier ebp has a single earlier writer, 597984 `xor ebp, ebp`. The prologue only spills rbp to the stack. The store dominates the call at 5979B6, and the path set equals the 18-instruction prefix. No other write in the body overlaps 48h..4Bh. |
| The resolver is each constructor's first call | PASS: `00597930` makes only that call. `00597970` calls `001C26B0` only afterwards. |

### Claim 3: the +20h bias aligns the fields

| Claim | Result |
|---|---|
| The record constructor passes the record itself as the frame | PASS: rcx = object + 0 at 59795D (rcx is never written in the body) |
| The reader passes reader + 20h | PASS: 5979B2 `add rcx, 0x20`, so rcx = object + 20h at 5979B6 |
| The rebind passes object + 20h | PASS: 59ED90 `add rcx, 0x20`, so rcx = object + 20h at 59ED97 |
| Reader+48h is the same field as frame/record+28h | PASS: 28h − 0 = 48h − 20h = 48h − 20h = 28h on all three paths |

### Claim 4: `0059ED70` has no direct key reset

| Claim | Result |
|---|---|
| The resolver is its first call and is unconditional | PASS: the call at 59ED97 is first and dominates the `ret`. `001C26B0` and `00584730` follow it. |
| No reset before the resolver | PASS: the entry → 59ED97 path makes no object write and no unresolved write. Its only writes are the four register homes at entry SP+8h..27h (the caller's home area). |
| Five own full-width writes, all disjoint from 48h..4Bh | PASS. Every write in the body resolves to the object or the stack. The five object writes are: |

| Site | Write | Byte span |
|---|---|---|
| 59ED9F | `mov dword ptr [rdi + 8], eax` (resolver result) | 08h..0Bh |
| 59EDCE | `mov qword ptr [rdi + 0x10], rsi` | 10h..17h |
| 59EDE3 | `mov dword ptr [rdi + 0x1c], -1` (imm32 all ones) | 1Ch..1Fh |
| 59EDF0 | `mov dword ptr [rdi + 0x18], eax` (eax = 0) | 18h..1Bh |
| 59EDF5 | `mov dword ptr [rdi + 0x1c], ecx` | 1Ch..1Fh |

All five lie in object 08h..1Fh, which is below the resolver frame at object + 20h, and all five follow the resolver
call. rdi has one writer, 59ED8A `mov rdi, rcx`, plus the epilogue restore.

### Claim 5: composition (conditional)

PASS (G1). Both constructors enter `0059EE90` with frame+28h = 0. The rebind enters it with frame+28h unchanged by
its own code, so the resolver sees whatever value the field held at rebind entry. This holds only under these
premises: valid, distinct record/frame and object; normal Win64 ABI and returns; and no opaque or concurrent
interference. It is an initialized-field rule for these three producers. It is not an all-writer, lifetime or
naturally-feasible-empty-hit proof.

### Claim 6: manifest

PASS: `manifest.json` sha256 = `d5cc7655d068357ee5bd9496b5674f82d4e4679d30d12356ba5411d8b713350e`, and all 43 listed
members hash as recorded. The packet folder has no change in the working tree, and `50dd4cc33` is the only commit
that touches it.

### Beyond the packet

These are corroboration only. They widen nothing.

- **The whole initializer matches across the bias (E2).** Rebasing the reader's pre-call writes at object + 20h by
  −20h reproduces the record constructor's six pre-call writes exactly:
  - frame+0 DWORD = 0;
  - frame+8 QWORD = −1;
  - frame+10h QWORD = 0;
  - frame+18h byte = an incoming argument byte;
  - frame+20h QWORD = −1;
  - frame+28h DWORD = 0.

  So the +20h bias aligns the whole frame, not only the key.
- **The resolver uses frame+28h as an out slot (R1).** Inside `0059EE90`, r15 = rcx (59EEC4). frame+28h is formed
  once, as 59EFD7 `lea r9, [r15 + 0x28]`, which is passed to `001D6D20`. No resolved store in the resolver body
  hits frame+28h..2Bh. See narrowing 5 for why this is not a no-write proof.

## Controls (14, each must FAIL its named check on a privately patched image; all did)

A null control runs first: an unchanged private copy, with the sha check off, passes all 38 image checks. The
packet-bytes cross-check is kept out of the control check set.

1. 597951 key store +28h → +2Ch. Fails C2 "DWORD constant-0 store to object+28h..2Bh exists".
2. 597951 DWORD store → byte store (`mov [rcx+0x28], al`). Fails C2.
3. 597936 `xor eax, eax` → `mov al, 1` (nonzero carrier). Fails C2 (the value is no longer constant 0).
4. The zero store is moved after the call: 597951 becomes a nop and 597962 becomes `mov dword [rbx+0x28], 0`. Fails
   C3 (dominance) while C2 still passes, so the failure is dominance alone.
5. 597949 → `jmp` past the zero store, plus nops. Fails C3 (dominance) and C4 (straight-line).
6. 597954 byte store +18h → +28h (overwrites the key after the zero store). Fails C5.
7. 5979A3 reader +48h zero store replaced with a nop. Fails D2.
8. 597984 `xor ebp, ebp` → `or ebp, ebp` (carrier keeps the caller's rbp). Fails D2.
9. 5979B2 reader bias `add rcx, 0x20` → 0x24. Fails D7 and E1 (alignment).
10. 59ED90 rebind bias `add rcx, 0x20` → 0x28. Fails F4 and E1.
11. 59ED94 → `mov [rcx+0x28], ebp` (a direct reset through the biased alias before the call). Fails F2 and F6.
12. 59ED9F `mov [rdi+8], eax` → `[rdi+0x48]` (the rebind writes the key). Fails F6.
13. 59EDCE QWORD store +10h → +41h (the 8-byte span 41h..48h reaches the key). Fails F6. A check on start offsets
    alone would miss this.
14. Boundary: 59EDCE QWORD store +10h → +40h (span 40h..47h, adjacent to the key). F7 (the exact write list) fails,
    and F6 is required to pass and does. Adjacency is not flagged as overlap.

The packet's three controls-01 CLI refusals were not repeated. These 14 are this review's replacements.

## Narrowings

1. **The rebind result is simpler than "five writes disjoint from 48..4C".** No object write precedes the
   resolver call at all. All five writes come after it, and they lie in object 08h..1Fh, outside the resolver frame.
   So the prior value the resolver sees needs no width argument and no ABI premise, because no call precedes it in
   the body. The disjointness of the post-call writes shows only that the rebind does not reset the key locally after
   resolving. That whole-body fact (F6) does rely on rdi surviving `001C26B0` and `00584730` (nonvolatile-ABI premise).
2. **"Previous value" means the value at rebind entry, not necessarily a stored key.** Both constructors skip the
   resolver when the name pointer is null: 597958 and 5979AA `test rdx, rdx` / `je` jump over the call, while the
   zero store is unconditional. So a rebind of a record whose constructor never resolved sees the constructor's zero.
   The packet's "may carry a previously stored key" is compatible with this.
3. **The rebind calls the resolver unconditionally with the caller's rdx.** The body makes no null test before
   59ED97. This review did not trace what the resolver does with a null name.
4. **The resolver flag differs between the two constructors.** The reader (5979AF) and the rebind (59ED8D) set
   r8b = 1. The record constructor `00597930` forwards its own caller's r8 unchanged. The resolver reads r8b at
   59EEBD. The prior-zero result does not depend on this flag, but an "empty-normalized first construction" may reach
   different resolver arms on the two constructor paths. The frame+18h byte also comes from different argument
   positions: r9b (fourth) in the record constructor and r8b (third) in the reader.
5. **R1 is corroboration, not a no-write proof of the resolver.** 6 of the resolver's 17 memory writes do not resolve
   in this reader. They are byte stores after its `_alloca_probe` / `sub rsp, rax`, so they are probably the
   stack buffer, but that is not shown. The effects of the resolver and of `001D6D20` on frame+28h stay unproved, as
   the packet already states.
6. **"Disjoint 48..4C" is read as half-open.** It means [48h, 4Ch), the DWORD at 48h..4Bh. Controls 13 and 14 show
   the check catches a 1-byte overlap (41h + 8) and correctly passes an adjacent span (40h + 8).

## Scope (kept as the packet states it)

This review supports conditional static facts for three producers only. Each holds under these premises:

- valid, distinct record/frame and object storage;
- the normal Win64 ABI and normal returns;
- no interfering opaque callee and no concurrent writer.

This review does not award:

- an all-writer census of record+28h / reader+48h, including indirect writers and the resolver's own callees;
- the lifetime or reuse scheduling of the key, or allocator freshness for either constructor's storage;
- a natural empty-name archive hit, that is, that an empty-normalized resolve is feasible for real inputs;
- high-bit keys, collisions or eviction;
- all-caller closure of the three producers, or the six-call census and RTTI/base-layout adjudication that the packet
  inherits without repeating;
- acceptance of the prior 99-member backfill packet.

run: `rv_srckey.py` at f348f2f1d (56 checks, 56 PASS, 0 FAIL, 14 controls; output identical to [`rv_srckey.out`](rv_srckey.out))
