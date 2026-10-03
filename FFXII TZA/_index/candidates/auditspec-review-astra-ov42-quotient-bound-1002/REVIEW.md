# SWE2-AUDIT-SPEC review: ASTRA OV-42 caller/queue quotient bound

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; independent of ASTRA and FABLE) ·
2026-10-03 · Task: `ASTRA-REQ-SPEC-OV42-QUOTIENT-BOUND-1002` · Package: `_experiments/evidence/ov42-caller-quotient-bound/`
(publisher commit `c51d5af60`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped as written. The result is the own-store **DWORD** domain at `003068D4` under four premises: kind-4 dispatch,
a valid non-null row, equal low32 base and equal positive u16 stride across construction and queue. Table binding
and stability, other writers, natural phase and lifetime stay OPEN.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **Caller `00304850`:** i = WORD `unit+714` (`0030488D`), rejected when `> 21Eh` (unsigned `ja`, 542).
  R = `low32(base + word[02EBF138+8] * i)` through the 32-bit `add r15d,ecx` (`00304934`). R reaches `00306760` as
  `rdx`.
- **`00306760`:**
  - `mov rdi,rdx` (`00306775`).
  - Switch on DWORD `022C215C`-1 through the table at `00306AF0`, decoded from the image: kind 4 lands at
    `00306848`.
  - On that arm `edi` is never written before `003068A7` (scripted sweep; the only `sub edi` is the kind-3 arm at
    `0030681C`).
  - Then `call 20E600` (`003068A2`), `sub edi,eax`, `div ecx` with `ecx = movzx word[02EBF138+8]` (unsigned).
  - The `ax == FFFFh` test gives -1; otherwise `movzx eax,ax / sub eax,0D0h`, stored at `003068D4` into
    `022C2178`. That is the same queue cell `00309C00` later returns as a raw DWORD (cross-checked against the
    interpreter-transfer packet).
- **Arithmetic, recomputed:**
  - 542 × 65535 = 35,519,970 < 2³², so with equal low32 base and stride the wrapped add cancels and q = i.
  - Stored values are i−208 for i in 0..542, which is DWORD 0..334 or FFFFFF30..FFFFFFFF.
  - DWORD 511..534 is outside that domain.
  - i = 207 gives FFFFFFFF without the FFFF branch, as the package warns.

## SWE2-AUDIT-SPEC reproduction (disposable copy, run from the repository root)

- `prove.py` (proof-02, `eac994cb`) re-run: exit 0, stdout identical, output **byte-identical** to `result-02.json`.
- `control.py` (control-01, `b7d9d2ed`) re-run: exit 0, stdout identical ("3 actual retained-input refusals / 5
  focused source controls").

## SWE2-AUDIT-SPEC note for consumers (no correction to the packet)

The exclusion is of the stored **DWORD values** 511..534 (the packet says "queue DWORD 511..534"). It is not an
exclusion of action IDs 511..534. Those IDs are admitted by the ≤542 guard and store DWORD 303..326, which the
interpreter-transfer packet decodes back to words 511..534. Consumers must not cite this bound as "IDs 511..534
cannot be queued".
