# FABLE review: rig owner rebinding preconditions (ASTRA `b1490763c`)

**verdict: ACCEPT** (FABLE, Claude Opus 5.5, 2026-10-02). Request `ASTRA-REQ-FABLE-RIG-OWNER-REBIND-PRECONDITIONS-1002`.
FABLE did not author this packet. The packet is
[`_experiments/evidence/rig-owner-rebind-preconditions/`](../../../_experiments/evidence/rig-owner-rebind-preconditions/README.md),
producer commit `b1490763c`.

## What was re-derived

[`rv_rebind.py`](rv_rebind.py) -> [`rv_rebind.out`](rv_rebind.out): 116 PASS, 0 FAIL, exit 0. The script uses FABLE's own
reader, [`rvlib.py`](rvlib.py), built on `struct` and capstone 5.0.7. It does not use ASTRA's prover or the role adapter.
It checks the image sha256 and the manifest (sha256 `ffe2b7cc1ce2...`; all 68 members hash as listed).

- **Bodies.** `00372350` (84 bytes), `003E3CA0` (196), `003E3D70` (961) and `004215A0` (754) decode exactly, 1,995 bytes
  in total. `.pdata` tiles each body, and no jcc leaves any of them.
- **Primary producer, `00372350`.**
  - Its only guards are `cmp [rcx+90], 0` / `jle`, which require a signed value above 0, and Decode(+94) != 0.
  - It then stores EDX as a DWORD at Decode(+94) + 68h (`00372383`) and calls `003E3D70` on the same decoded pointer.
  - It has no index or owner check.
  - In the factory, r14 = arg0 (`0041F361`, otherwise written only by the epilogue pop). `0041F608` `movsx edx, word
    ptr [r14]` then calls it.
  - Over all 65,536 values, the signed16 value written to the DWORD and read back by the reader's WORD movzx/movsx
    returns the same index.
- **Rebinders `003E3CA0` and `003E3D70`.** The following holds for both:
  - an outer NULL rig returns at once;
  - for a non-NULL rig, WORD +68 equal to -1, or a row whose DWORD +284h is 0, selects rcx = rdi = 0;
  - Encode, the +70 store, Decode and `00421D20` follow, with no compare or test of the derived pointer;
  - rdi stays 0 from `xor edi, edi` to the select, and `00421D20` and the codec do not write rdi;
  - the primary `00421D20` call dominates the +6C compare and the return (`003E3CF4`, `003E3DC4`).
- **Secondary +6C.**
  - The full-DWORD compare against -1 skips, at `003E3D08` -> `003E3D59` and `003E3DD8` -> `003E3E28`.
  - Otherwise the WORD +6C is compared with -1 and sign-extended (`003E3D14`, `003E3DE9`). Both WORD outcomes reach the
    single secondary `00421D20` call (`003E3D49`, `003E3E18`).
  - No direct `[rbx+74..7F]` write can be reached from either skip target, and rbx is written only at entry and by the
    final pop.
  - The link-only `003E3CA0` calls only the codec and `00421D20`, and its skip path goes straight to the return.
  - The full-reset `003E3D70` calls `003E3C30` (`003E3E2B`) on both outcomes.
- **Secondary writer, `004215A0`.**
  - rsi = arg0 from `004215B8` until the epilogue restore.
  - `004216D3` `movsx ebx, word ptr [rsi]` is followed by `004216DB` `mov dword ptr [rax + 0x6c], ebx`, where rax =
    Decode(r14+94). It then calls `003E3CA0` on Decode(r14+94), and r14 is unchanged in between.
  - It is the only direct +6C write in the body.
- **Representation.** This is a Python model over all 65,536 values.
  - The signed16 writer produces the all-ones DWORD only for WORD -1, and never produces the value whose low WORD is
    all-ones and high WORD is zero.
  - That counter-representation takes the WORD-missing lookup path, not the skip.

## Controls (each must be rejected, and is)

Each control reruns the relevant claim group on a patched private copy. All are rejected:
- the secondary skip edge inverted (`003E3D08`);
- a derived-pointer test inserted before `00421D20` (`003E3DC1`);
- the secondary writer changed to a zero-extend (`004216D3`);
- the producer guard changed from `jle` to `jl`;
- a direct +74 clear inserted on the link-only skip path;
- a wrong expectation that `004216D3` is `movzx`.

The width known-answer control and the capstone `movups` access-flag defect are recorded in the sibling
[render-slot review](../fable-review-astra-render-slot-identity-publication-1002/REVIEW.md).

ASTRA's `prove.py` also passes, with its output in scratch. This review does not rely on it.

## Scope

The packet's claims are hedged correctly. Each of the following stays a limit, not a finding:
- outer-NULL safety versus derived-owner validity;
- "skips refresh, no direct clear" (indirect writes through `003E3C30` and the many callees in `003E3D70` are not
  excluded);
- the signed16 agreement only "on the demonstrated caller paths";
- the conditional read at 18h only at decoder base 0;
- no natural reachability, no observed fault and no EXP127 cause.

Not awarded:
- other writers of +68/+6C, or other callers of `00372350`/`003E3CA0`;
- the active-bit persistence after the factory's `0041F4BC` OR;
- owner and index consistency, lifetime and natural reach.

run: rv_rebind.py at 1f193fec9
