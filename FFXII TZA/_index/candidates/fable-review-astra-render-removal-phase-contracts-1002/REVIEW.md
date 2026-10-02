# FABLE review: ASTRA render-removal-phase-contracts

- **Packet:** [render-removal-phase-contracts README](../../../_experiments/evidence/render-removal-phase-contracts/README.md)
  (board `ASTRA-REQ-FABLE-RENDER-REMOVAL-PHASE-CONTRACTS-1002`)
- **Producer commit:** `31f29775a`. The manifest sha256 begins `fc26ae31f8ddb389` and all 53 members hash as listed.
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every branch, return value and phase-order claim re-derives at the bytes. The
  narrowings add two omitted writes. They do not contradict anything the packet states.

## Method

[rv_removal.py](rv_removal.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It does not
import ASTRA's `prove.py` or the shared role adapter. It works as follows:

- It decodes the three bodies completely and checks each against `.pdata`.
- It builds a local CFG from direct branches.
- For every claim it uses region, dominance and straight-line-predecessor checks. A ret's value is accepted only when no
  branch target joins between the eax definition and the ret.

Raw output: [rv_removal.out](rv_removal.out).

## Re-derived (52 checks, 52 PASS, 0 FAIL)

### Bodies and shared state

| Claim | Result |
|---|---|
| `00429140..004292A6` (358 B), `00427C90..00427DD8` (328 B) and `004200A0..004201EB` (331 B) total 1017 B | PASS: each decodes exactly and its `.pdata` records tile it (3, 3 and 1 records) |
| `00429140` and `00427C90` have closed local CFGs | PASS: no tail or outward branch |
| `004200A0` ends in a tail jump to `0041F730` | PASS: it has no `ret`; its only exit is `jmp 0041F730` with rcx = rbx, after all 15 of its calls |
| Both bodies use the same pool | PASS: both load the global `022C6F28` |

### `00429140` (removal request)

| Case | Result |
|---|---|
| NULL | PASS: returns 0. There is no call, no non-stack write and no record dereference. The only read is the pool global before the test. |
| 284h mask 04 set (mark) | PASS: 290h \|= 2, 2AEh \|= 1, qword 108h = 0, dword 110h = 0, and 284h = (old & ~4) \| bit 30. All of these precede the first call. Then it calls `00422D50`, `0020E600`, `002ED570` and `0020E620`. It makes no count or cursor write and no call to `0041F730` or `004200A0`. It returns 1. |
| 04 clear, 290h mask 01 clear (no-op) | PASS: the path 429204 → 429296 → ret has no call and no non-stack write, and returns 1. The stated input (284h = 2010F9h, 290h = 0) selects this path. |
| 04 clear, 290h mask 01 set (unlink) | PASS: <ul><li>Its only call is `0041F730` at 429291. It never calls `004200A0`.</li><li>It writes the neighbour rows' +4 and +2 WORDs and the pending head (48810h) and tail (48814h).</li><li>The single `dec [pool+4880Ch]` (42924D) dominates both the cursor reset at 429288 (taken when the new count is 0) and the clear.</li><li>No path from 429204 to the dec reads the count, so there is no positive-count guard.</li><li>rdx is not rewritten on this path.</li></ul> |
| Return values | PASS: there are three rets. 42915C returns eax = 0; 429203 and 4292A5 return eax = 1. No branch target joins between the eax definition and the ret. |

### `00427C90` (active sweep)

| Claim | Result |
|---|---|
| Row selection | PASS: the head is read from [pool+48800h], and row = pool + sext(esi) × 740h |
| Test and cached next | PASS: 290h mask 02 is tested. The signed next WORD +4 is cached in esi (427CD4/427CD8) before the branch. esi is written only at the head load, at the cache and in the epilogue. |
| Count decrement first | PASS: the single dec at 427D18 dominates all five calls (`0042F4C0`, `00426EC0` in the child loop, `003B6000`, `003AFBE0`, `004200A0`) |
| Nothing checked before the dec | PASS: no loop path before the dec reads WORD +0 (the ID) or the count |
| Cursor reset | PASS: when the new count is 0, the cursor reset writes ebp = 0. ebp is set once, at 427CBA. |
| Separate list ends | PASS: the active unlink uses 48800h/48804h; the `00429140` pending unlink uses 48810h/48814h |
| Count underflow | Arithmetic: a count of 0 decrements to -1, and the `jne` then skips the reset. This is arithmetic only; no underflow was executed. |

## Controls (9, each must FAIL a named check on a privately patched image; all did)

1. 429296 `mov eax, 1` changed to 2. Fails the return-value check.
2. 429204 test moved onto the count. Fails the no-op dispatch check and the no-positive-count-guard check.
3. Call at 429291 retargeted to `004200A0`. Fails "unlink calls only `0041F730`".
4. Dec at 427D18 NOPed. Fails "dec dominates every call".
5. 427CD4 reads WORD +0. Fails the next-cache check and the no-ID-read-before-dec check.
6. 427CD8 `mov esi, edx` NOPed. Fails the cached-next checks.
7. 42915D mask 04 changed to 08. Fails the dispatch check.
8. The mark-arm OR at 42916F replaced by a `dec [pool+4880Ch]`. Fails "mark arm has no count write".
9. Tail jump at 4201E6 retargeted. Fails the tail check.

The packet's four CLI refusals were not rerun. These nine are this review's replacements.

## Narrowings

1. **The mark arm writes three objects besides the record.** It ANDs ~2 into the dword at +0Ch of the object returned by
   `00422D50` (4291A9). It ANDs ~4 into the dword at +0 of the object returned by `002ED570` (4291E4). It stores the
   result of `0020E620` at +A0h of that same object (4291F3, where rbx = rax at 4291D8). The packet's mark row lists only
   record writes and "helper calls". Phase prose must not call the mark arm "record-only". These writes depend on the
   helpers' return values; this review awards nothing about those helpers.
2. **The sweep's selected iteration does not end at `004200A0` → `0041F730`.** After `004200A0` returns, 427DB3 ORs 20h
   into the pool dword at +48818h. After that, the loop continues on the cached next. Phase prose of the form "count →
   callbacks → resource cleanup → clear" should add "→ pool flag 48818h \|= 20h".
3. **One count, one cursor, two lists.** The `00429140` unlink (pending ends) and the `00427C90` sweep (active ends) both
   decrement the same pool count at 4880Ch and reset the same cursor at 48808h. "Count" in consumer prose means this
   shared counter, not a per-list count. This is consistent with the packet, which does not say otherwise.

## Scope (kept as the packet states it)

This review supports conditional static source contracts only. Return 1 is not a certificate of an immediate free.
This review does not award:

- helper-name semantics or native callee effects (`00422D50`, `0020E600`, `002ED570`, `0020E620`, `0042F4C0`,
  `00426EC0`, `003B6000`, `003AFBE0` or the 15 calls in `004200A0`);
- progress of the child loop;
- reentrancy, atomicity or async observation;
- all-writer closure of the count, list or flags;
- natural reach of the no-op state.

The "every consumer tests ID first" qualifier is supported only for this sweep. The retained clear result is reviewed
separately: see [the clear review](../fable-review-astra-render-clear-callee-footprints-1002/REVIEW.md).

run: rv_removal.py at 80da775cb
