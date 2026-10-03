# SWE2-AUDIT-SPEC review: ASTRA OV-42 action-table binding

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; independent of ASTRA and FABLE) ·
2026-10-03 · Task: `ASTRA-REQ-SPEC-OV42-ACTION-BINDING-1002` · Package: `_experiments/evidence/ov42-action-table-binding/`
(publisher commit `ca2dd6483`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped as written. This is binder dataflow plus mathematical countermodels. Command-window reload, other writers,
callbacks, arena, ownership and lifetime stay OPEN.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`00236C30`:** `mov ecx,[qword 0208E680 + 3Ch]` (`00236D82`) then `call 237FC0`.
- **`00237FC0`:** `movsxd rdx,ecx` (sign-extended descriptor D), `lea rcx,02EBF138`, `call 3845F0`.
- **`003845F0` (`AreaData_BindAndRebaseSectionDescriptor`):**
  - Its first instruction publishes the slot QWORD (`mov [rcx],rdx`, `003845F4`) before any null test or rebase.
  - Fields `+0C`, `+10`, `+18` and `+1C` each get `add eax,edx` (low32 D) only when non-zero. The add is written back
    in place with no encode and no "already rebased" guard. So handing the same descriptor pointer in twice
    re-adds D, and the same pointer can rebind rows, as claimed.
  - `+14` instead gets `20E620(low32(field+D))` stored as an encoded DWORD (`00384662`), then is decoded by
    `20E600` for the nested walk.
  - The nested loop runs index 0..count inclusive (`jle`). On the `rdi == count` pass its `je` at `0038469F`
    consumes the flags of `cmp rdi,r14` and takes `add [rbx],ebp` (`003846B9`). That is the stride/alias site the
    count-zero overlapping-directory model names.
- **Leaves:**
  - `20E600` is `mov eax,ecx / add rax,[01F83530]` (QWORD arena read).
  - `20E620` is `sub ecx,[01F83530] / mov eax,ecx` (DWORD arena read).
  - Neither has a call or a write.

## SWE2-AUDIT-SPEC reproduction (disposable copy, run from the repository root)

- `prove.py` (proof-02, `38c1ef16`) re-run: exit 0, stdout identical, output **byte-identical** to `result-02.json`.
  Proof-01 (`0ee5a385`, exit 1, rejected before output) stays archived as stated.
- `control.py` (control-01, `56438b02`) re-run: exit 0, stdout identical. The four concrete prerequisite refusals
  (failed extents, capture exception, empty capture output, missing encoder) all exit 1. The six source/CFG controls
  are reported as passing.

## SWE2-AUDIT-SPEC limits (unchanged)

- The direct `+4`/`+8` footprint is not whole-call preservation.
- The three countermodels are mathematical, not native or natural states.
- The resource registration/reset/reuse writer discriminator is the next step.
