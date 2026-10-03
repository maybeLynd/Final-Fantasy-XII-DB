# FABLE review: ASTRA ov42-action-table-binding

- **Packet:** [ov42-action-table-binding README](../../../_experiments/evidence/ov42-action-table-binding/README.md)
  (board request `ASTRA-REQ-FABLE-OV42-ACTION-BINDING-1002`).
- **Producer commit:** `ca2dd6483`. The manifest sha256 begins `e2ae054634b26a2c` and equals the manifest committed
  at `ca2dd6483`. All 71 members hash as listed. Every range in `binding-source-01.json` and
  `binding-helper-source-01.json` (the four bodies) and in the two retained leaf maps hashes to the certified image's
  bytes, and its instruction records concatenate to them. Both extents files equal the image's physical bytes, sizes,
  sha256 and `.pdata` records. `retained-resolver-source-01.json` is byte-identical to `d34aa6837`'s
  `skeletonref-producer-slice/source-01.json`, and `retained-encoder-source-01.json` to `134687c7d`'s
  `ov21-count-publication-window/source-01.json`. `result-02.json`'s four scalar-field load/store pairs and its three
  countermodels equal this review's own reading and emulation.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every claim re-derives at the bytes: the registrar -> wrapper -> binder
  argument chain with its sign extension, the slot store before any test, the four plain rebases by low32(D) with no
  already-rebased guard, the `+0x14` encode / store / decode / visit order, the DWORD encoder and QWORD decoder, the
  leaves' lack of calls and stores, the binder's direct store footprint (no displacement 4 or 8), the conditional
  order, the depth-0 child calls, and all three countermodels. An emulation of the original binder, child binder and
  both leaves, with nothing stubbed, agrees on every case tried. The narrowings correct one more line of the AG-12
  wording than the packet names, add the slot as the base of the later rebases, and add censuses that bound where
  a rebind and an arena write can come from. None of them closes the call-window writer question.

## Method

[rv_binding.py](rv_binding.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is
copied unchanged from the kind-row review (sha256 `69f9bc40be32abcc`). It does not import or run ASTRA's `prove.py`,
`prove_owner_reload_order.py`, `prove-before-conditional-order-correction.py`, `capture*.py`, `prepare-*.py`,
`control.py`, `run.py`, `validate-title-source-annotations.py`, or `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`). It checks that the `.pdata` records of the registrar
  `00236C30`, the slot wrapper `00237FC0`, the binder `003845F0` (seven chained records) and the child binder
  `003846F0` tile each extent, and that each body decodes linearly and exactly. It decodes the two leaves `0020E600`
  and `0020E620`, which have no `.pdata`.
- It reads the argument chain and the binder instruction by instruction. The read covers the slot store, the five
  rebases, the encode / decode order, the outer loop, the binder's complete list of non-stack stores and the
  child's depth test. It takes register-write censuses where a claim depends on a register not changing.
- It emulates (unicorn) the **original** binder from its entry, with the child binder and both leaves run from the
  image. Nothing is stubbed, because the binder calls nothing else. The runs are the packet's three countermodels, a
  two-level directory, a null and an all-zero descriptor, 60 random plain-field binds at three descriptor addresses,
  and 200 random inputs to each leaf. It also emulates the registrar's three instructions and the wrapper's head up to
  the binder's entry.
- It runs a raw `E8`/`E9` rel32 and `0F 8x` census for the four bodies. It runs a disp32 census (rip-relative and
  image-base-relative, decoded from each hit's `.pdata` record) for the slot `02EBF138` and the image-address base
  `01F83530`. It re-reads and emulates the published indexed store that reaches `01F83530` (`de52023ee`).
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_binding.out](rv_binding.out).

## Re-derived (57 checks, 57 PASS, 0 FAIL; 17 controls among them)

### Extents and leaves

| Claim | Result |
|---|---|
| Four complete bodies, 1870 B | PASS: registrar 1037 B (one record), wrapper 404 B (one record), binder 252 B (seven chained records), child 177 B (three records). Each tiles and decodes exactly. |
| `0020E600` is the 10-byte decoder, `0020E620` the 9-byte encoder | PASS: `mov eax, ecx` / `add rax, qword ptr [01F83530]` / `ret`, and `sub ecx, dword ptr [01F83530]` / `mov eax, ecx` / `ret`. Neither has `.pdata`, a call or a memory write. Emulated on 200 random inputs each: the decoder returns zero-extend(ECX) + the full QWORD, mod 2^64, and reads exactly those 8 bytes. The encoder returns low32(ECX - the low DWORD), zero-extended, and reads exactly those 4 bytes. |

### The argument chain

| Claim | Result |
|---|---|
| Registrar -> wrapper | PASS: `00236C30` + 0x14B loads QWORD `0208E680` (8 B), + 0x152 reads DWORD `+0x3C` into ECX, + 0x155 calls `00237FC0`. Emulated: a directory whose `+0x3C` is 2^31 + 0x1000 reaches the wrapper with that ECX. |
| Wrapper -> binder, sign-extended | PASS: nothing writes ECX before + 0xF `movsxd rdx, ecx` (`48 63 D1`). + 0x15 forms `02EBF138` in RCX, and + 0x1E calls `003845F0`. No other RCX or RDX write lies between. Emulated: RDX arrives as 0xFFFFFFFF80001000, 0x1000 and 0xFFFFFFFFFFFFFFF0 for the three ECX tried, whatever RCX's upper half held. |

### The binder

| Claim | Result |
|---|---|
| The slot QWORD is stored before validation and rebase | PASS: + 0x4 `mov qword ptr [rcx], rdx` (8 B) is the first non-stack write. It precedes `test rdx, rdx` (+ 0x7) and the `je` to the epilogue (+ 0xA), and it dominates every other store. Emulated: a null descriptor stores the slot as 0 and returns with no other store or call. |
| `+0xC/+0x10/+0x18/+0x1C`: x == 0 ? 0 : low32(x + low32(D)), no guard | PASS: each is a DWORD load, `test eax, eax`, `je`, `add eax, edx` (`03 C2`, 32-bit) and a DWORD store. Before the `+0xC` store the only tests are `test rdx, rdx` and `test eax, eax`, and the only memory read is `+0xC` itself. Emulated: 60 random binds at three descriptor addresses all match the formula. |
| Same pointer, different rows (countermodel 1) | PASS: emulated with D = 0x100000, arena 0, `+0xC` = 0x20. The first bind stores 0x100020, and a second bind of the same pointer stores 0x200020. The slot holds 0x100000 both times, and the decoder returns 0x100020 then 0x200020. The first bind's only stores are the slot and `+0xC`. |
| `+0x14`: encode, store, then decode and visit | PASS: M = low32(`+0x14` + D) (+ 0x62) is kept in EBP. `call 0020E620` (+ 0x6D) and the store of its EAX (+ 0x72) both come before the M == 0 test (+ 0x75). The visit decodes that EAX (+ 0x90), reads a WORD count from the result (+ 0x98), and decodes `+0x14` again as the entry base (+ 0x95, + 0x9C). |
| Encoded DWORD, full-64 decode (countermodel 2) | PASS: emulated with arena 0x100001000 and `+0x14` = 0x100, so M = 0x100100. `+0x14` receives 0xFF100. The binder then reads the count at the full decode 0x100100100 (the WORD read at + 0x98) and adds M to the last entry there (+ 0xC9). Nothing at the low32 address is written. low32(decode) = M, but decode != M. |
| Outer loop and depth-0 children | PASS: for i = 0 .. count inclusive, i < count calls `003846F0` with RCX = the entry's address, EDX = low32(entry + M) and R8D = 0 (+ 0xB3). i == count does `add dword ptr [rbx], ebp` (+ 0xC9). The child's only self-call (+ 0x7B) lies behind its depth test (+ 0x60 / + 0x62). Emulated on a two-level directory: the child is entered exactly twice, both times from the binder, with (0x100204, 0x100500, 0) and (0x100208, 0x100600, 0). Each child stores its encoded base into its entry and adds that base to all count + 1 of its own entries, and no child calls itself. |
| No direct `+4`/`+8` store; the overlap model (countermodel 3) | PASS: the binder's own non-stack stores are exactly seven: `[rcx]`, `[rdx + 0xc]`, `[r8 + 0x10]`, `[r8 + 0x18]`, `[r8 + 0x1c]`, `[rdi + 0x14]` and `[rbx]`. None has displacement 4 or 8. Emulated with `+0x14` = 4 (a count-0 directory at D+4): the last-entry add at + 0xC9 (result-02's `original_store`) turns DWORD D+8 from 60 into 0x100040, so the WORD stride becomes 64. |
| Conditional order (producer-01's rejection) | PASS: from the entry, + 0x6D is reachable without the `+0xC` store (+ 0x1E), because a zero `+0xC` skips it. From + 0x1C (nonzero `+0xC`) every path to + 0x6D passes + 0x1E. |

### Packet integrity

PASS. The manifest sha256 begins `e2ae054634b26a2c` and equals the committed manifest, and all 71 members match.
The README says call-window writer exclusion "remains unresolved". It says the overlap model is "not a stock action
table", that the countermodel is "not a native call ... or proof of natural double binding", and that ownership,
lifetime and natural reachability "remain OPEN".

## Controls (17, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy passes all 24 image checks.

1. Slot store removed (+ 0x4 -> NOP). Fails the slot-first, `+0xC`, store-list and emulated checks.
2. `add eax, edx` -> `add eax, eax` (+ 0x1C). Fails the `+0xC`, countermodel-1 and random-bind checks.
3. `+0xC`'s `je` -> `jmp` (+ 0x1A). Fails countermodel 1 and the random binds.
4. Encoder call -> NOP (+ 0x6D). Fails the `+0x14` read and countermodel 2.
5. Decoder REX.W dropped (a DWORD arena add). Fails the leaf, countermodel-2 and random-leaf checks.
6. Encoder `sub` -> `add`. Fails the leaf, countermodel-2 and random-leaf checks.
7. `movsxd rdx, ecx` -> `mov edx, ecx` (wrapper + 0xF). Fails the wrapper and emulated-chain checks.
8. Wrapper's slot `lea` -> `02EBF140`. Fails the wrapper and emulated-chain checks.
9. Registrar's directory field `+0x3C` -> `+0x40`. Fails the registrar and emulated-chain checks.
10. Last-entry `add dword ptr [rbx], ebp` -> NOP (+ 0xC9). Fails the loop, store-list and countermodel-2/3 checks.
11. The `+0xC` store retargeted to `+8` (+ 0x1E). Fails the `+0xC`, store-list and countermodel-1 checks.
12. `xor r8d, r8d` -> `mov r8d, ebp` (a nonzero depth). Fails the loop and two-level-directory checks.
13. Child's depth `je` -> NOP NOP (+ 0x62). Fails the child and two-level-directory checks.
14. Encoder `mov eax, ecx` -> `mov dword ptr [rcx], eax` (a store in the leaf). Fails the leaf and countermodel checks.
15. Slot reload `mov r8, qword ptr [rcx]` -> `mov r8, rdx` (+ 0x21). Fails the slot-reload check (narrowing 2).
16. `+0x14` zero test forced taken (+ 0x5C). Fails the `+0x14`, conditional-order and countermodel-2/3 checks.
17. The route leaf's signed `jge` -> unsigned `jae` (`00210570` + 0x8). Fails the route re-read and its emulation.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's four CLI refusals and six
source/CFG controls were not repeated. These 17 image patches replace them for this review.

## Narrowings

1. **AG-12 has a second wrong line: the sub-directory entries are rebased by M, not by the descriptor.** The packet
   corrects AG-12's "`+0x14` ... resolved through `0020E620`". The same AG-12 row also says the sub-directory's
   entries "are each rebased by `desc`". At the bytes, EBP holds M = low32(old `+0x14` + low32(D)), the
   sub-directory's own rebased value. The child's argument is low32(entry + M) (+ 0xB9), and the last entry gets `+=
   M` (+ 0xC9). The emulation shows entry + 0x100200 where D was 0x100000. The packet's countermodel 3 already uses
   this ("adds D+4"), but its prose does not state it. Each child then adds its own argument, not D, to its
   entries.
2. **The slot is the base of four of the five rebases.** Only `+0xC` is addressed through RDX. `+0x10`, `+0x18`,
   `+0x1C` and `+0x14` are each addressed through a fresh `mov r8/rdi, qword ptr [rcx]` (+ 0x21, + 0x32, + 0x43,
   + 0x54), a reload of the slot just written. So the early slot store also supplies those bases. The packet's
   "valid separate slot/storage" premise therefore covers more than visibility: a slot that aliased a descriptor
   field would move the later bases. Control 15 shows that the check sees this.
3. **`+0x14` is encoded and stored even when M is 0.** The store (+ 0x72) precedes the M == 0 test (+ 0x75). A
   nonzero `+0x14` whose sum wraps to 0 is still overwritten with low32(0 - low32(A)), and no visit follows. This
   agrees with the packet's order. It is stated here because the AG-12 correction should carry it.
4. **Only one instruction forms the action-table slot's address.** In the disp32 census of `02EBF138`, 720
   anchored instructions touch it. One forms its address (the wrapper's `lea`, `00237FC0` + 0x15), none stores to it
   by displacement, and 719 read it. The wrapper has one raw direct reference (`00236C30` + 0x155), and the registrar
   has one, a tail `jmp` at `00238850` + 0x1F. The binder itself has 42 raw direct references, most from the
   registrar binding other slots. So a direct-reference rebind of this slot goes through this one chain.
   Computed-address slot arguments, aliasing stores and indirect calls are not excluded. This bounds where ASTRA's
   "next discriminator" starts. It does not answer it.
5. **The arena has no direct writer, but a published indexed route reaches it.** No `.pdata`-anchored instruction
   accesses `01F83530` by displacement. The hits lie in the two leaves, which read it. The texture leaf `00210570`
   (published `de52023ee`) bounds a 16-bit id only by a signed `jge` against 0x4000, then stores a QWORD at
   `01F83580` + 16 * id. Re-read and emulated here, id 0xFFFB stores its QWORD argument at `01F83530`. "Arena
   reassignment" in the packet's OPEN list is therefore a real route, not a hypothetical one. Whether it is driven
   during the named window is not read.
6. **The wrapper consumes the fresh binding at once.** After the bind the wrapper reloads the slot on each pass. It
   reads `+4` as the row bound (`cmp esi, dword ptr [rdx + 4]`), `+0xC` through the decoder, and `+8` as a WORD
   stride. It forms each row address in 32 bits (`add eax, ecx` / `mov ecx, eax`) and dereferences it as RCX. This
   confirms AG-12's `+4` count / `+8` stride roles from a reader. The row pointer it uses is a zero-extended low32,
   the same projection the availability page already records for the allocator's row read through `0020E600`.

## What stays OPEN (kept as the packet states them)

This review supports static facts and emulation of the original bytes on supplied descriptors. The following remain
open and are not awarded:

- the call-window writer, alias, callback and concurrency exclusion for the current-row construction through the
  kind-4 quotient (the packet's `304934 -> 304F4D -> 3068A7/3068B2`). Neither the packet nor this review reads that
  window. The previous quotient result stays conditional on equal low32 rows base and equal positive WORD stride;
- registrar completion, resource registration, reset, reuse and free, and arena reassignment during the window
  (narrowing 5 names one route);
- natural double binding of one prepared descriptor; whether a stock action-table resource ever overlaps its header
  with a nested directory;
- the child binder's nonzero-depth arm (reached only from its other callers, not from the binder);
- ownership, lifetime, natural command reachability, and whole OV-42.

The three countermodels are arithmetic on supplied descriptors run through the original bytes in emulation. They
are not native runs or stock resource samples. Valid, separate slot and descriptor storage, the normal Win64 ABI,
and an unchanged arena between paired encode and decode reads are premises.

run: `rv_binding.py` at HEAD c2fc944fe (57 checks, 57 PASS, 0 FAIL, 17 controls; output identical to [`rv_binding.out`](rv_binding.out))
