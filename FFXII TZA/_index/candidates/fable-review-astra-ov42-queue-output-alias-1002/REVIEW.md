# FABLE review: ASTRA ov42-queue-output-alias

- **Packet:** [ov42-queue-output-alias README](../../../_experiments/evidence/ov42-queue-output-alias/README.md)
- **Producer commit:** `4fe271b46`. The manifest sha256 begins `44d660e4e849ee60`. It equals the manifest committed at
  `4fe271b46`, and all 54 members hash as listed. The packet's two raw ranges (`spattack-queue-reader-raw-01.json`,
  `spattack-info-raw-01.json`) equal the certified image's bytes: the range hashes and every instruction record
  (15 + 42). The 7 input and source pins in `result-02.json` also hash as listed.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every primitive claim re-derives at the bytes: the -1 test, the write-free
  unavailable arm, the null-guarded 4-byte action store, the unit load placed after it, the null-guarded unit store,
  the reset and the DWORD 1 return. The same holds for every bridge claim: both destinations are read after the call
  with no branch between, whatever EAX is. The overlap countermodels equal the reviewer's own byte simulation. The
  narrowings concern a label, the callers, and one premise sentence on FABLE's own page. None contradicts the packet.

## Method

[rv_queue.py](rv_queue.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is copied
unchanged from the filecache-route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It does not import ASTRA's
`prove.py`, `control.py`, its freeze or publication scripts, or the shared role adapter `reg_tracking.py`. It works
as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes both bodies completely.
  - The bridge `00348330` is checked against the image's own `.pdata`: one record, flags 0, 0xA5 bytes.
  - The primitive `00309C00` has no record. It is a leaf with no call. It is bounded by its closed local CFG, its
    last `ret`, an int3 before the entry, and 14 int3 bytes after the end.
- It builds a local CFG for each body from direct branches. It checks dominance for the reset, the return
  definition and the bridge reads.
- It walks the primitive itself over all 8 partitions (queue available or not × RDX null or not × RCX null or not).
  The walk uses concrete register values and evaluates each branch from the preceding `cmp`/`test`. It records
  every memory write and the EAX at `ret`.
- It takes a register-writer census for the bridge's two destination carriers, RBX and RSI.
- It simulates the two output stores byte by byte, in the order the decoded image puts them. It compares the result
  with the packet's nine arithmetic countermodels and with its byte formula.
- It lists the raw `E8`/`E9` references to `00309C00` in `.text` (direct only).
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_queue.out](rv_queue.out).

## Re-derived (49 checks, 49 PASS, 0 FAIL; 11 controls among them)

### Bodies

| Claim | Result |
|---|---|
| Primitive `00309C00` + 0x32 (50 B, 15 instructions) | PASS: it decodes exactly and no `.pdata` covers it. It has no call and no tail or out-of-body branch. It has two `ret`s: `00309C00` + 0x0D (unavailable) and `00309C00` + 0x31 (the last instruction). |
| Bridge `00348330` + 0xA5 (165 B, 42 instructions) | PASS: it decodes exactly and one `.pdata` record covers it exactly. It has no conditional branch and no `ret`. Its one exit is the tail jump at `00348330` + 0xA0 to `0026B4E0`. See narrowing 1 for the byte total. |

### Primitive (claims: unavailable, available order, all-NULL)

| Claim | Result |
|---|---|
| Reads DWORD `022C2178` and compares it with -1 | PASS: `00309C00` is `mov eax, dword ptr [rip+…]` → `022C2178` (4 B). It is followed by a 32-bit `cmp eax, -1` and `jne`, so only FFFFFFFF takes the unavailable arm. |
| Unavailable: return 0, no own writes | PASS: `xor eax, eax` / `ret` (`00309C00` + 0x0B..0x0D). Nothing reachable from there writes memory or calls. The queue is left unreset. |
| Action DWORD through non-null RDX | PASS: `test rdx, rdx` / `je` skips only `00309C00` + 0x13 `mov dword ptr [rdx], eax` (4 B). On the path from the queue load to that store, nothing writes rax. |
| Unit DWORD `022C218C`, loaded after the action store, through non-null RCX | PASS: `test rcx, rcx` / `je` skips `00309C00` + 0x1A (load `022C218C`, 4 B) and + 0x20 `mov dword ptr [rcx], eax` (4 B). The only `022C218C` read follows the only RDX store on the straight available arm, and the store is not reachable from the read. |
| Reset, then return DWORD 1 | PASS: `00309C00` + 0x22 writes FFFFFFFF to DWORD `022C2178`. Both output stores pass it before the final `ret`. `00309C00` + 0x2C `mov eax, 1` is the last rax writer and dominates the `ret`. |
| Write census | PASS: the primitive writes memory at exactly three sites, `[rdx]`, `[rcx]` and the queue, each 4 B. It writes no rbx, rsi or rsp, so the bridge's carriers survive it from its own bytes, not only by ABI. |
| 8 partitions; all-NULL still consumes | PASS (reviewer's own walk): when unavailable, there are no writes and EAX is 0. When available, the walk gives `[rdx]` = queue DWORD (if non-null), then `[rcx]` = unit DWORD (if non-null), then queue = FFFFFFFF, and EAX is 1. With both pointers NULL, the only write is the reset. |

### Overlap algebra

| Claim | Result |
|---|---|
| The later unit store overwrites the intersection; the formula and its 9 countermodels | PASS: the image's store order is [action, unit]. A byte simulation in that order reproduces all nine rows (delta −4..+4: final bytes, DWORD and overlap count). It also reproduces the packet's formula, in which action byte j = unit byte j − delta when 0 ≤ j − delta < 4. |
| Same buffer leaves the unit DWORD in both views; disjoint byte ranges preserve both | PASS (delta 0; delta ±4, ±8) |

### Bridge (claim: unconditional destination reads)

| Claim | Result |
|---|---|
| RSI = the action destination (RDX at the call) | PASS: the first `002650B0` call (`00348330` + 0x33) returns into rax. `00348330` + 0x3B `mov rsi, rax` and + 0x51 `mov rdx, rsi`. rsi has only that writer plus the epilogue restore. |
| RBX = the unit destination (RCX at the call) | PASS: the second `002650B0` (`00348330` + 0x4C), then + 0x54 `mov rcx, rax` and + 0x57 `mov rbx, rax`. Nothing writes rax or rcx before the `00309C00` call at `00348330` + 0x5A. |
| Both selectors come from `00267E10` | PASS: `00267E10` is called twice (+0x25, +0x3E) on rdi = incoming r9. Each result is the third argument of `002650B0`, with rcx = the `002640C0` context and rdx = incoming rcx. |
| `00348330` + 0x79 reads `[rbx]` and + 0x81 reads `[rsi]` (4 B each) after any normal return | PASS: from the return address (`00348330` + 0x5F) to `00348330` + 0x81 the code is a straight line of 8 instructions, with no branch, no call and no rbx or rsi writer. EAX is only copied to EDX (+0x65) and is never tested. Both reads are dominated by the call. |
| What the reads feed | PASS: `[rbx]` goes to `01EF920C` and `[rsi]` goes to `01EF9214`. The previous values of those two are first copied to `01EF9208` and `01EF9210`. The bridge writes nothing through rbx or rsi. |
| The result is not dropped | PASS: EDX = the primitive's EAX reaches the tail callee `0026B4E0`, with rcx = rbp (incoming rcx). |

### Packet integrity

PASS: the manifest and its 54 members, the committed manifest at `4fe271b46`, the 7 result-02 pins, and the raw
ranges with every instruction's bytes. The README presents the eight partitions as "logical branch partitions… not
eight native calls", and it states no bridge byte total.

## Controls (11, each must FAIL a named check on a privately patched image; all did)

A null control also runs first: an unchanged private copy, with the sha check off, passes all 29 image checks. The
manifest, raw-range, pin and caller checks are kept out of the control check set.

1. `00309C00` + 0x06 `cmp eax, -1` → `cmp eax, 0`. Fails the sentinel check and the 8-partition walk.
2. `00309C00` + 0x0B `xor eax, eax` → `mov [rdx], eax`. Fails the "unavailable arm writes nothing" check and the
   write census.
3. `00309C00` + 0x11 `je` → `jne` (reversed action null guard). Fails the guard check, the walk and the all-NULL
   check.
4. `00309C00` + 0x13 `mov [rdx], eax` → `mov [rcx], eax`. Fails the action-store, order and census checks.
5. `00309C00` + 0x20 `mov [rcx], eax` → `mov [rdx], eax`. Fails the unit-store, order and census checks.
6. The reset immediate FFFFFFFF → 0. Fails the reset check and the walk.
7. `00309C00` + 0x2C `mov eax, 1` → `mov eax, 0`. Fails the return-provenance check and the walk.
8. `00309C00` + 0x0E..+0x21 rewritten in place (20 B) so that `022C218C` is loaded into r8d before the action
   store. Fails the order check, among 7 others.
9. `test eax, eax; je` inserted at `00348330` + 0x5F, which makes the bridge reads conditional on the result. Fails
   the "no conditional branch", straight-line and dominance checks.
10. `00348330` + 0x57 `mov rbx, rax` → `mov rbx, rsi`. Fails the unit-destination carrier check.
11. `00348330` + 0x81 `mov ecx, [rsi]` → `mov ecx, esi`. Fails the destination-read check.

After all controls, the exe on disk still hashes to `73461d0896204b1c259c`. The packet's two CLI refusals and three
synthetic decoded-record mutations were not repeated. These 11 replace them for this review.

## Narrowings

1. **The bridge is 165 B, not 215 B.** The packet states no total. Its raw range and the image's single `.pdata`
   record both give `00348330` + 0xA5. The 215 B figure appeared only in the review request, and nothing consumes
   it.
2. **"Debug state" is a label, not a re-derived fact.** The bytes show both destination DWORDs copied into the
   globals `01EF920C`/`01EF9214`, after those globals' previous values are shifted to `01EF9208`/`01EF9210`. This
   review did not take a reader census of those four globals. Consumers should name them by address.
3. **Nullable describes the body, not a shipped call.** There are two direct callers, and neither passes a literal
   NULL:
   - `002D6175` passes two stack locals 20h apart, which are non-null and byte-disjoint.
   - The bridge passes two `002650B0` results.

   Whether `002650B0` can yield NULL or an invalid pointer is not read here. "All-NULL outputs still consume" is
   the primitive's own guard behaviour, and no shipped all-NULL call is shown. The census is E8/E9 only and does not
   cover indirect callers.
4. **FABLE's own premise wording needs a qualification** (FABLE's page, not ASTRA's packet). FABLE's availability page (the 2026-10-02 subsection's limits) writes
   the transfer premise as "`00309C13` -> `00267E10`". In the bridge, `00267E10` runs twice before the primitive.
   Its results are the two out-reference words that `002650B0` turns into the destinations. The later reader of the
   stored action DWORD is not in this body. The premise is therefore a store into a script-addressed destination,
   followed by an unread later read, and it needs the destinations to be disjoint. Exact text:
   [consumption-draft.md](consumption-draft.md).
5. **On an unavailable return the bridge copies stale values.** When the primitive returns 0 it writes nothing, so
   the bridge's reads copy whatever the destinations already held. This follows from the checks above. The packet
   says the reads happen "even if the primitive returned zero" and does not spell out this consequence.

## Limits (kept as the packet states them)

This review supports conditional static facts only. The following remain open and are not awarded:

- actual authored out-reference binding, backing capacity, alias freedom and lifetime;
- any naturally occurring overlapping pair, and any null or invalid destination;
- faults or exceptions;
- the case where an output aliases `022C2178` or `022C218C` (outside the formula);
- natural command-to-action reachability, concurrency, and whole OV-42.

The nine countermodels are arithmetic, not executions. The primitive's 8 partitions are logical, not native calls.

run: `rv_queue.py` at c0bf8acd5 (49 checks, 49 PASS, 0 FAIL, 11 controls; a second run's output is byte-identical to
[`rv_queue.out`](rv_queue.out))
