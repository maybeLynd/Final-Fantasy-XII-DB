# SWE2-AUDIT-SPEC review of SD-141, the flying-fade pair readers (OPUS, 940b5ffcf): REJECT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `940b5ffcf`, [README](../sd141-flying-fade-readers-0930/README.md) and `sd141_readers.py`. Measured at HEAD
`b58c633f7`. Package re-runs repeated at `701f1f01a`, identical. Static analysis of the certified image
(sha256 asserted in [sdx.py](sdx.py)).

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD141-0930 | sd141-flying-fade-readers-0930 | `940b5ffcf` | REJECT |

**Re-run.** [rerun_sd141_readers.out](rerun_sd141_readers.out) is identical to the committed `.out` (CR ignored). F1-F4
and C1 PASS, `FAILS 0`. The package dir was clean after the re-run.

**Re-derived independently.** Tools: [sdx.py](sdx.py), a pefile + capstone + numpy census written for this review
(it does not use retool.py or the `pe` module). Outputs: [sd141_indep.py](sd141_indep.py) / [.out](sd141_indep.out)
and [sd141_handon.py](sd141_handon.py) / [.out](sd141_handon.out).
- **F1, F2 and F4 hold.** All .text operands starting in `02CB83D0`..`02CB8417` were checked in every form:
  - rip-relative;
  - image-base-relative with any base or index, including index-only and scale-1 base+index;
  - absolute disp32.

  Only the writer's two `movss` stores (`001C9040`, `001C8FFF`) cover the pair. The widest operand in the window
  is 4 bytes. No image-base-relative or abs32 operand falls in it. No relocation targets `02CB7C10`..`02CB8417`.
- **The answer does not hold: the pair is read through a handed-on base.** This is the route F3 does not follow, and
  the README's limit dismisses it with a 16-byte criterion.
  - `006084B0` does `0060890A lea rdx, [02CB8160]`, which is the pair − 0x2B0.
  - `rdx` is not rewritten before `00608999 call 005DEC50`, with `rcx = rdi + 0x2A0` (H1).
  - `005DEC50` is a leaf with no `.pdata` entry. It copies 176 dwords `[rdx + d] -> [rcx + d]` up to `d = 0x2BC`.
    Two of those reads are the pair (H2):
    - `005DF3A0 mov eax, dword ptr [rdx + 0x2b0]` = `02CB8410`;
    - `005DF3AC mov eax, dword ptr [rdx + 0x2b4]` = `02CB8414`.
- **Where the copy goes.** `006084B0`'s only caller is `00604879` in `00604750`, which passes `rcx = rbp + 0x270`
  (H3). So the pair lands at `rbp + 0x7C0` / `rbp + 0x7C4`, and `00604750` uses it in two ways:
  - it reads both back, `00605F66 movss xmm1, [rbp + 0x7c0]` and `00605F88 movss xmm1, [rbp + 0x7c4]`, and stores
    them to `[r14 + 0x5D4]` / `[r14 + 0x5DC]`;
  - it memcpy's the whole 0x598-byte struct (`006048B5 mov r8d, 0x598`, `006048C2 call 00861ED2`, an import thunk)
    into a two-slot buffer at `[rsi + 0x4E0 + ([rsi + 0x4D8] & 1) * 0x598]`.

  Who consumes those copies was not traced.

**Controls.**

| instrument | control | result |
|---|---|---|
| the exact-address rip census | K1: the writer's two stores and `02CB8404`'s reader `001FA8D8` (root `001FA820`) | found |
| the width/coverage logic | K2: xmmword `005ADC61`, re-found from a window 8 bytes inside it | flagged COVERS |
| image-base-relative | K3: SD-121's `0036E414` | found |
| index-only / scale-1 forms | K4: `002AECA3`, `002AEE26` | exist and are decoded |
| DIR64 | K5: `01F2E330`'s 6 self pointers | found |
| `sdx.track()`, the hand-on follower | [sd127_leas.out](../auditspec-review-sd127-0930/sd127_leas.out) T1 | reports `00608999`'s `rdx = 02CB8160` |

The package's own C1 control is a rip-relative read. It is sensitive to F1 only, and blind to the defect that
decides this row: a base handed to a callee.

**Defects in the package's gates.**
- F3 follows a `lea`'d register within its own function only.
- F3 counts a hit only when the dereference lands within 16 bytes. The README's limit repeats this: "No such `lea`
  target exists within 16 bytes of either global". But the struct here is 0x2C0 bytes, and the base is 0x2B0 below
  the pair.
- F2's regex needs a base register and exact displacement equality. It is not load-bearing here, since the full-form
  census finds nothing, but it is blind to index-only and scale-1 base+index operands.

**Citations checked.** `001C7940`'s stores `001C9040` / `001C8FFF` and C1's `001FA820` hold. The "flying-shadow"
reading is from names only, as stated.

**Correction wording** (the producer applies). Replace "The answer" and "What it fades" with:

> The pair is read, by a copy. `006084B0` hands `02CB8160` (the pair − 0x2B0) in `rdx` to `005DEC50` (`00608999`).
> That 0x2C0-byte dword copy reads `02CB8410` / `02CB8414` at `005DF3A0` / `005DF3AC` into its destination's
> `+0x550` / `+0x554`. The destination is the 0x598-byte struct that `00604750` builds at `rbp + 0x270`
> (`00604879`). `00604750` re-reads both (`00605F66`, `00605F88`) into `[r14 + 0x5D4]` / `[r14 + 0x5DC]`, and
> memcpy's the struct into a two-slot buffer (`006048C2`). What reads those copies is not traced. So whether the
> parameters have an effect is open.

Also:
- delete "For modding: … has no effect in this build";
- replace the F3 limit with "F3 follows a lea'd base within its function only; a base handed to a callee is not
  followed (the case above)".

Keep SD-141 OPEN, pointing at the consumers of the struct's `+0x550` / `+0x554` and `[r14 + 0x5D4]` / `[r14 + 0x5DC]`.
