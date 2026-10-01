# SWE2-AUDIT-SPEC review of SD-107 (sd107-kind1-writers-0930 at 0b1f3a2fb): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `0b1f3a2fb`, [the record](../sd107-kind1-writers-0930/README.md) and `sd107_kind1.py`. Static, the certified
image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD107-0930 | [sd107-kind1-writers-0930](../sd107-kind1-writers-0930/README.md) | `0b1f3a2fb` | ACCEPT-WITH-NARROWING |

**Re-run.** `sd107_kind1.py` at HEAD: K1-K5 PASS, `FAILS 0`; identical to the committed `.out` ignoring CR
([rerun_sd107_kind1.out](rerun_sd107_kind1.out)).

**Re-derived independently** ([sd107_review.py](sd107_review.py), [sd107_review.out](sd107_review.out)).

K1 classes a store as "constant 1" only when it is `mov [m], imm`. Other store shapes can also leave 1 in a zeroed kind
byte: `setcc`, `inc`, and `or` / `add` / `xor` / `bts` with an immediate.

I swept every body in `functions.tsv`. For each memory destination whose byte range covers `+0xA3` off a non-rip,
non-rsp base, I took the width from capstone's operand size and classed the store by kind. That gives 509 stores; the
author's `pe` body list gives 552. By class:
- `mov-reg` 351, `mov-imm-other` 100, `movss` 39, `movsd` 11;
- `and-imm` 3;
- `inc` 1, `or-imm` 1, `sub-imm` 1, `add-imm` 1;
- `mov-imm-1` 1: `007E7401`, the author's K1 hit, which is the positive control;
- `setcc` 0.

**The finding: a second constant store of 1.** `00500CC2 or byte ptr [rdi + 0xa3], 1` in `00500C00` sets bit 0 of
the byte. Its partner is `00500CCB and byte ptr [rdi + 0xa3], 0xfe`, taken on the flag `[[..]+2] & 8`.
- `00500C00` is the initialiser of effect record kind `0x52`, size `0x1D0`. See
  [effect-element-type-dispatch.md](../../../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md),
  the kind table row for `0x52`.
- In the same body it writes `+0x1C8`-`+0x1CE` on the same `rdi`. That is past the 0xD0 bytes a text element occupies
  (K5's `memset(..., 0, 0xD0)`), so the object is not a text element.
- The other non-`mov` hits are dword counters at `+0xA0`: `00332A46 inc dword ptr [rdi + 0xa0]` and
  `0087BB00 add dword ptr [rbx + 0xa0], -1`.

So the **conclusion holds**: no traced store puts kind 1 into a text element. But K1's sentence "of every store with an
immediate value, exactly one puts 1 into that byte" is **false as worded**, and its control cannot see the `or` form,
because the checker filters on `x.mnemonic == "mov"`.

**Controls.**
- K1 is a genuine image-wide sweep, but it is insensitive to read-modify-write stores (the defect found above).
- K3 and K4 are sensitive within their stated neighbourhood: they list the known 3/2/0/0 writers.
- K5 is a pinned-text check.
- My sweep's control is `007E7401`, found. It also found `00500CC2`, which shows the sweep is sensitive to the
  RMW shape the author's sweep skips.

**Correction wording for the row owner (SWE2-DATA)**, for SD-107's NARROWED text and the record's K1 line:

> K1 (narrowed by SWE2-AUDIT-SPEC review): of the `mov`-immediate stores covering `+0xA3`, exactly one stores 1
> (`007E7401`, a sound handle's). One read-modify-write store also sets that byte's bit 0, `00500CC2 or byte ptr
> [rdi+0xa3], 1`, in the kind-0x52 effect-record initialiser `00500C00`. Its object runs to `+0x1CE`, so it is not a
> text element. No `setcc` store covers `+0xA3`. The kind-1 conclusion is unchanged.
