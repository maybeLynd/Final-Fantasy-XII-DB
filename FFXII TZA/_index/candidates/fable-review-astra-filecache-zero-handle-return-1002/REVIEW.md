# FABLE review: ASTRA filecache-zero-handle-return

- **Packet:** [filecache-zero-handle-return README](../../../_experiments/evidence/filecache-zero-handle-return/README.md)
- **Producer commit:** `5b659b28d`. The manifest sha256 begins `93e2351f2132231d` and equals the committed manifest.
  All 72 members hash as listed. The packet's ten captured and retained range hashes (`source-01.json`,
  `source-02.json` and the two retained source maps) equal the certified image's bytes. They include all seven bodies
  reviewed here. The retained manifest is `filecache-route2-commit-key`'s (`f3365d0e…`), which FABLE has already
  reviewed (ACCEPT-WITH-NARROWING).
- **Reviewer:** FABLE, reviewing independently. FABLE did not author this packet.
- **Verdict:** **ACCEPT-WITH-NARROWING.** Every claim re-derives at the bytes: the counters before the 16-byte
  allocation, the NULL arm's full zero with no constructor and no rollback, the zero's survival through the unlock,
  the cookie check and the wrapper, the resolver's store and its sign-only test, the import identity and the byte
  totals. The narrowings say which record the counter hits, add the per-arm stamps that the packet's effect list
  leaves out, and limit the "status 0" claim to the resolver, because the reader's constructor discards that status.
  None of them contradicts the packet.

## Method

[rv_zerohandle.py](rv_zerohandle.py) uses the reviewer's own reader, [rvlib.py](rvlib.py) (struct + capstone 5). It is
copied unchanged from the route2-commit-key review (sha256 `69f9bc40be32abcc32b1`). It also uses the reviewer's own
sandbox, which is new in this review and is written into the script. The script does not import ASTRA's `prove.py`,
its capture drivers, its freeze or publication scripts, or `reg_tracking.py`. It works as follows:

- It checks the image sha256 (`73461d0896204b1c259c`) and decodes seven bodies completely.
  - Five are checked against the image's own `.pdata`: `0020C300`, the cookie check `00808C40`, the lookup
    `0020C1B0`, the wrapper `001D6D20` and the resolver `0059EE90`.
  - The two thunks, `00210EC0` and `0085E730`, have no record. Each is bounded by int3 bytes before and after it and
    ends in an unconditional `jmp`.
- It resolves the import from the PE import directory: the descriptor, the IAT slot and the hint/name entry.
- It enumerates every entry → allocation path in `0020C300` (17 paths) and checks dominance and reach sets for the
  counter, the NULL arm and the zero's route to the resolver.
- **Sandbox.** Unicorn 2.1.4 runs the shipped bytes over a private copy of the image's sections.
  - Every callee outside the bodies under review is a recording stub. So is every import: the IAT slots are pointed
    into a stub page.
  - A stub returns a chosen RAX, writes junk into the volatile argument registers (Win64 ABI) and returns to its
    caller. Registers and stack start as junk.
  - It runs `0020C300` on every selector 0–7 × kind 0–6 arm, with the allocation returning NULL and non-NULL: 112
    runs.
  - It runs the resolver over a route-1 hit whose allocation is NULL.
  - It runs one route-1 miss as a contrast.
  - This is a model of the bytes under stubbed callees. It is not native execution of the game.
- Controls patch a private in-memory copy of the image. The exe on disk is never written, and its sha256 is
  rechecked after all controls.

Raw output: [rv_zerohandle.out](rv_zerohandle.out).

**A limit in the reviewer's reader.** rvlib's CFG does not treat the `bnd`-prefixed `jne` and `ret` in `00808C40` as
branches. That body is therefore checked by its exact eight-instruction text and its returning path, not by rvlib's
reach sets.

## Re-derived (52 checks, 52 PASS, 0 FAIL; 11 controls among them)

### Bodies, import and totals

| Claim | Result |
|---|---|
| `0020C300` + 0x138 (312 B), `00210EC0` + 0xB (11 B), `0085E730` + 0x7 (7 B): 330 B; cookie `00808C40` + 0x21 (33 B) | PASS: each decodes exactly. The first and the last are exactly covered by one `.pdata` record each, and the two thunks have no record and are int3-bounded. 330 + 33 = 363. |
| The 16-byte allocation is CRT `malloc` | PASS: `00210EC0` is `or r8d, -1; xor edx, edx; jmp 0085E730`. `0085E730` is `jmp [rip+…]` through IAT `008C2B40`, which the import directory names `api-ms-win-crt-heap-l1-1-0.dll!malloc` (hint/name at `01DEEE88`). That is the static declaration only. |
| Retained `0020C1B0`, `001D6D20`, `0059EE90` | PASS: 322, 79 and 876 B. Each has exactly one `.pdata` record, and their bytes equal the packet's retained ranges. |

### Claim 1: the counters come before the allocation

| Claim | Result |
|---|---|
| The manager's dword `+0x88` is incremented before the allocation | PASS: `0020C300` + 0x28 is `inc dword ptr [rcx + 0x88]`, with rcx still the incoming first argument. It dominates the `00210EC0` call at + 0x100, which follows `mov ecx, 0x10`. |
| Exactly one record byte `+0x10` is incremented | PASS: each of the 17 entry → allocation paths passes exactly one of + 0x54, + 0x8B and + 0xF8, all `inc byte ptr [r + 0x10]`. |
| Which record that is | PASS (see narrowing 1): it is `[rax]` after a call to `0020B5F0`. All six of those calls pass the manager's `+0x20` and the key that `0020C300` saved from edx. `0020B5F0` walks root `[rcx+18h]` against header `rcx+8` with that key and returns node + 0x28. That is the lookup's tree (root `+0x38`, header `+0x28`) and the lookup's key. The lookup holds its lock across the call: `005CD4F0` dominates it and `005CD820` follows it. |
| No other non-stack write comes before the allocation except | +0x88 (dword), the three `+0x10` bytes, `+0x14` (dword, + 0x68), `+0x0E` (word, + 0xC3) and `+0x0C` (word, + 0xE1). PASS as a census. See narrowing 1. |
| Sandbox | PASS: in all 112 runs, `+0x88` rises by exactly 1 and record `+0x10` by exactly 1, and both writes come before the malloc call. The record stamps by arm are none in 56 runs, `+0x0C` word in 36, `+0x0E` word in 12 and `+0x14` dword in 8. Each matches the reviewer's reading of the arms. |

### Claim 2: an ordinary NULL returns 0, skips the constructor and rolls nothing back

| Claim | Result |
|---|---|
| NULL → RAX 0, constructor skipped | PASS: + 0x10A `test rax, rax` and + 0x10D `je` go to + 0x123 `xor eax, eax`. From there, there is no call, no memory write and no other rax writer up to the `ret`, and `00217A60` is unreachable. |
| Non-NULL → constructor | PASS: + 0x118 passes rcx = the block to `00217A60`, and that call's RAX is returned unchanged. |
| Sandbox | PASS: in the 56 NULL runs RAX is a full 0, `00217A60` is not called and no non-stack write follows the malloc call. In the 56 non-NULL runs the constructor gets the block and its RAX is returned. |

### Claim 3: a zero from a lookup hit survives the unlock, the cookie check and the wrapper

| Claim | Result |
|---|---|
| Hit path | PASS: `0020C1B0` + 0xFD `mov rbx, rax`, then + 0x103 calls the unlock `005CD820`, then + 0x109 `mov rax, rbx` and a `jmp` to the cookie block. The miss arm's `or rax, -1` at + 0x117 is not on that path. |
| Cookie | PASS: `00808C40` is exactly cmp / `bnd jne` / `rol rcx` / `test cx` / `bnd jne` / `bnd ret` / `ror rcx` / `jmp 00809654`. Its returning path writes no rax. |
| Wrapper | PASS: `001D6D20` writes no rax after its `0020C1B0` call. |
| What the zero rests on | rbx surviving `005CD820` is the Win64 nonvolatile ABI premise. The cookie part is an instruction fact. |

### Claim 4: the resolver stores the zero and tests only its sign

| Claim | Result |
|---|---|
| Store | PASS: `0059EE90` + 0x15A `mov qword ptr [r15 + 0x20], rax` (8 B) directly follows the lookup call. |
| Sign-only test | PASS: + 0x15E `test rax, rax` and + 0x161 `js` are the only test. |
| The zero / positive arm | PASS: it loads eax = `[rbp]` (the size out) and stores it to `[r15]`, then `xor eax, eax` and the epilogue. Its only call is the cookie check, and neither `0019AEE0` nor `0059A9B0` is reachable from it. |
| Sandbox, NULL allocation on a hit | PASS: status RAX 0. The stream ends as `+0x28` = -1, `+0x30` = 0, `+0x40` = 0, and `+0x20` = the entry's size. There is no archive call, and both counters rose by 1. |
| Sandbox contrast, a miss | PASS: `+0x40` = -1, with no allocation and no counter change, and the resolver reaches its archive fallback (`0059EE90` + 0x170). |

### Claim 5: counters and status do not certify a constructed view

PASS. It follows from claims 1 to 4: both counters and any stamp are already written when the allocation fails, and
the resolver returns 0 for the NULL view as it does for a real one.

## Controls (11, each must FAIL a named check on a privately patched image; all did)

A null control runs first: an unchanged private copy, with the sha check off, passes all 35 image checks. The packet,
manifest and range checks are kept out of the control set.

1. `0020C300` + 0x10D `je` → `jne`. Fails the NULL-test check and the 112-run sandbox check.
2. `0020C300` + 0x123 `xor eax, eax` → `xor al, al`. Fails the NULL-arm check. RAX is already 0 on that arm, so the
   sandbox cannot see this one; the text check does.
3. `0020C300` + 0x28 `inc [rcx+88h]` → `[rcx+8Ch]`. Fails the counter, census and sandbox checks.
4. `0020C300` + 0xF8 `inc byte [rcx+10h]` → three nops. Fails "exactly one on every path", the census and the
   sandbox check.
5. `0020C300` + 0xFB `mov ecx, 0x10` → `0x20`. Fails the 16-byte check.
6. `0020C300` + 0x48 `lea rcx, [rdi+20h]` → `[rdi+28h]`. Fails the "hit entry itself" check.
7. `0020C1B0` + 0x109 `mov rax, rbx` → `mov rax, rsi`. Fails the hit-return check and the resolver sandbox run.
8. `0059EE90` + 0x161 `js` → `jle`. Fails the sign-only check and the resolver sandbox run.
9. `001D6D20` + 0x3A `mov rbx, [rsp+40h]` → `mov rax, [rsp+40h]`. Fails the wrapper check and both resolver runs.
10. The `0085E730` IAT slot moved by 8 bytes. Fails the import check and the 112-run sandbox check.
11. `00808C40` + 0xA `rol rcx` → `rol rax`. Fails the cookie check and both resolver runs.

After all controls the exe on disk still hashes to `73461d0896204b1c259c`. The packet's five CLI refusals were not
repeated. These 11 replace them for this review.

## Narrowings

1. **The record is the hit entry, and it is stamped as well as counted.** The record whose byte `+0x10` is
   incremented is the entry the lookup has just found: same tree, same key, under the lock the lookup still holds.
   Depending on the fifth argument (the selector, which `0020C1B0` forwards from its own `r8d`) and the sixth (the
   entry's dword `+0x14`), the same entry also gets one stamp before the allocation:
   - selector 5 with kind 1–4: dword `+0x14` = 5;
   - otherwise, kind 5 or selector 5: no stamp;
   - otherwise, selector 3: word `+0x0E` = the word at `[manager+0x18]+0xE8`;
   - otherwise, selector 1, 2 or 4: word `+0x0C` = the manager's word `+0x80`;
   - any other selector: no stamp.

   None of these is rolled back on NULL. "Exactly one byte `+0x10` increment" holds. "The bookkeeping before the
   allocation" is two counters plus at most one stamp.
2. **"Status 0" is the resolver's, and the reader's constructor drops it.** `00597970` overwrites RAX in the first
   instruction after its resolver call and returns `this`. For a `PStreamReaderFile` the zero view is therefore
   visible only as `+0x40` = 0 (see the open-sentinel review), not as a status. The status matters only to the other
   resolver callers, which are not read here.

**Additions, which do not narrow anything:**
- A zero-view stream still carries a size. The lookup writes the entry's dword `+8` through the size out-pointer
  (`0020C1B0` + 0xDC) before it calls `0020C300`, and the resolver copies that into the stream's `+0x20`.
- `00210EC0` also sets edx = 0 and r8d = -1 before tail-jumping to `malloc`, which takes one argument.

## Limits (kept as the packet states them, plus the reviewer's)

This review supports conditional static facts only. Its premises:
- valid manager, tree and record pointers, and disjoint frames;
- normal returns and the Win64 nonvolatile ABI across `005CD4F0`, `005CD820`, `0020B5F0` and `00217A60`;
- no opaque field interference;
- the cookie check succeeds.

The stubs in the sandbox stand in for those premises. They do not establish them. The following remain open and are
not awarded:
- natural allocation failure in play;
- the live DLL binding behind the import;
- the counters as live handle counts, and byte `+0x10` wrapping at 256;
- what the stamps mean;
- ownership, lifetime, reuse and scheduling;
- every writer of these fields, and all callers;
- the exception path;
- later reader consequences beyond the three stream slots (see the open-sentinel, read-zero-view and
  close-zero-sentinel reviews).

The packet warns that two manager roots, `0020C700` → `01F83438` and `001DADA0` → `01F82CF0`, must not be conflated.
This review keeps that warning but reads neither root. Its "manager" is only the object `001D6D20` hands to the
lookup.

Consumption: see the combined draft in
[fable-review-astra-filecache-close-zero-sentinel-1002/consumption-draft.md](../fable-review-astra-filecache-close-zero-sentinel-1002/consumption-draft.md).

run: `rv_zerohandle.py` at c0bf8acd5 (52 checks, 52 PASS, 0 FAIL, 11 controls; output identical to [`rv_zerohandle.out`](rv_zerohandle.out); capstone 5.0.7, unicorn 2.1.4)
