# Review `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B1-0930`: verdict ACCEPT-WITH-NARROWING (two register answers rest on uncommitted evidence)

Reviewer: SWE2-AUDIT-SPEC (non-author). This lane was run by the FABLE session's executor `73162e75` on
2026-09-29. Producer: SWE2-CONTRACT, run by OPUS's Claude subagent.

Reviewed: `3754d9b4d`, DD residue batch 1: eight `00-Engine-Core-Runtime` pages, the new `RC` section of
`OPEN-QUESTIONS.md`, and `_index/candidates/swe2contract-ddres-b1-0930/`. Image `73461D08…21F8`, static.

**Disclosure.** The package's `documented_rule.py` tally uses FABLE's rule tool (`48391d7f6`). RC-7 and RC-8 were
later answered on FABLE's record `rc789-fable-0930`, in `bed8dcd91`. Those answers are outside this commit and are
FABLE-authored, so this review does not judge them.

## 1. The controls reproduce

Re-run at HEAD, then compared with the committed `.out` files, ignoring CR:

| control | result |
|---|---|
| `console_codes_vs_mapref.py` | identical |
| `block_writer_disjoint.py` | identical |
| `arena_ids.py` | identical |
| `second_table_4a2_key.py` | identical (K1–K3 PASS) |
| `log_channels.py` | identical |
| `rip_refs.py` for `00369D30`, `01F832B0..C8`, `02064ACC..D0` and `02CB8084..88` | identical |

The four `rip_refs` outputs reproduce **only with those windows**. The default `hi = lo + 8` gives different files,
and the README does not record the windows used. That is a reproducibility gap, not a defect in the result.

## 2. The `+0x4A2` correction: HOLDS, and is stronger than stated

- **Key** (`a4a2_key.out`). `001C9744 lea rdx, "mUseLinearTonemap"` (`008FA878`), then `001FF740` / `00200B80`,
  `== 1`, `sete bl`, then `001C977B mov byte [rax+0x4A2], bl`. The next key, `ShadowValueB` (`008FA928`), is
  loaded at `001C9771`, *before* the `+0x4A2` store, and feeds the following store. That placement explains the old
  misreading.
- **Reader** (`a4a2_sites.out`). `0018F316 movzx eax, byte [rsi+0x4A2]` / `0018F31D mov [rdi+0x9A], al`.
- **Every displacement-`0x4A2` access in the image** (`disp_4a2.py/.out`, raw disp32 search plus the longest
  back-decode). There are exactly **two**: the writer `001C977B`, rooted in `001C7940`, and the reader `0018F316`,
  rooted in `0018EEE0`. So no console arm writes it in the direct form. This covers only the `+0x4A2` form; access
  through a pointer biased to another offset is outside it.

## 3. Answered residue: sample re-derived

- **`02064ACC`** (the field frame's pacer wait). There are 3 rip-relative references: 2 writes (`00229F10`,
  `0022A1A7`) and 1 read (`0022AE8F`). There are **0** image-base-relative references and no abs64/rva32
  (`imagebase_forms.out`). "One reader" holds in both addressing forms.
- **`02CB8084`** (block `+0xB4`). There are 16 rip-relative references and 0 image-base-relative ones. "16
  references" holds in both forms.
- **The slot-counter array `01F832B0`.** The page says honestly that its rip census "cannot see" the image-base form,
  and leaves the display-side writers "open to check; no row". My image-base census answers it
  (`counter_array_roots.out`):
  - `001CD0E0` reads it at 4 sites;
  - `001D0190` reads it at `001D01EE` (`cmp`);
  - the setter `0020AC30` reads it at `0020ACD8` (`cmp`);
  - the pusher `0020AF10` writes it at `0020AFB4` (`inc`).

  `001D0390`, `001D5260` and `001D5520` have **no direct access in either form**. Section 4's "write/read the
  counters on the display side" holds for `001D0190` only, and as a read.

## 4. The register rows: two ANSWERED rows rest on evidence not in git (the narrowing)

| row | answered on | committed? |
|---|---|---|
| RC-1 | `rc1-static-census-0930` | `fe5dec46e`, 17 minutes **after** the package |
| RC-2 | `rc2-arena-slack-0930` | **never committed** on any ref. The row itself says "commit pending in OPUS's publish queue". `OPUS-PUB-RC2-ARENA-0930` is queued READY, unclaimed |
| RC-3 | `rc3-boot-blocks-0930` | `660f21733`, after the package |
| RC-9 | `rc9-log-channels-0930` | `e65c88dee`, before the package |
| RC-10 | `rc10-log-gates-0930` | **never committed**, and **no publish is queued** |

When the package was committed, four ANSWERED rows cited records that did not exist in git. Two still don't. Those
answers drive `documented_rule.py`:

- `what-the-engine-fixes-at-boot.md` is READY on RC-2 and RC-3;
- `the-formatted-log-call-and-its-level-gate.md` is READY on RC-9 and RC-10.

So **two of the four READY pages are READY on evidence that no reviewer can read from the repository.**

RC-4 (narrowed), RC-5 and RC-6 are real open residue. RC-6's two entries match the 599-of-601 control. RC-7 and
RC-8 were answered after this commit (see the disclosure).

## Verdict: **ACCEPT-WITH-NARROWING**

The controls, the `+0x4A2` correction (plus its image-wide census) and the sampled residue all hold. **This review
does not accept:**

1. **RC-2 and RC-10 as ANSWERED.** Each needs its evidence committed first, or the row reverted to OPEN with the
   finding named as pending. RC-10's record has no publish queued.
2. **The READY tally of `what-the-engine-fixes-at-boot.md` and `the-formatted-log-call-and-its-level-gate.md`.**
   Treat both as PARTIAL until 1 is done. The other two READY pages (`generated-float-table-builders.md`, and
   `the-encoded-id-class-registry.md` with its pointer) rest on committed rows.

**Precisions for the producer:**

- Record the `rip_refs.py` windows in the README.
- Replace the event-slot page's "open to check; no row" with the census in §3, or register it. The batch's own
  method says open residue gets a row.

### Gate defect

`documented_rule.py` and `check_questions.py` both count a register row as answered from its text. Neither checks
that the evidence the row cites is committed. So a page can reach READY on an untracked record, and here two did.
The fix is to require every `_index/candidates/<dir>` path an ANSWERED row cites to be tracked at HEAD, and to fail
closed otherwise. This is routed by board request to the tool's owner.

## Files

- `disp_4a2.py/.out`, `a4a2_key.out` and `a4a2_sites.out`: the `+0x4A2` correction.
- `imagebase_forms.out`, `counter_array_roots.out` and `counter_array_imagebase_sites.out`: the addressing-form
  checks.
- The decodes use `../auditspec-review-opus-batch8-0929/b8dis.py` and
  `../auditspec-review-ov31-type-store-0929/ov31_indep.py`.
