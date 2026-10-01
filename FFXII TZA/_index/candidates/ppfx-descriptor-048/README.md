# PpfxInitDescriptor +0x48: a dword read unsigned, and an unread remainder (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SEM.

**Before.** `mixed048 u8[8]`, width NOT resolved. It was written as a qword zero by `006CBBC0` and as dword 1920 by
`006CBD20`.

**The read** ([`ppfx048_split.py`](ppfx048_split.py)).
- **R:** CPostEffect embeds this descriptor at +0x210. Its body reads CPostEffect +0x258, which is +0x48 here, with
  `cmp dword ... / jbe` at `007006FC`: an unsigned dword. The read is in the committed flow census `cpe-flow-accesses.tsv`.
- **W:** `006CBD20` stores `0x780` (1920) into its stack copy at `rsp+0x50+0x48`. `006CBBE1`'s qword is the
  zero-initialiser.
- **C:** apart from that qword and 16-byte copies, nothing touches +0x4C..+0x4F.

**After.**
- `+0x48 dword048 uint32` is TYPE RESOLVED. MEANING NOT CLAIMED, unless the post-processing contract is cited.
- `+0x4C` is `u8[4]` and stays DISCOVERED.
- The old row is kept verbatim as WAS.

**Not changed.** `mixed020` and `mixed088` are only written (a `movss` store and dword stores) and block-copied, never
read at a width. They stay unresolved.

**Run receipt.** Run verified at 5b1263d28: `ppfx048_split.py` S FAILED before the patch and FAILS 0 after it;
`types_index.py --validate` 0 errors; `check_census_widths.py` 0 disagreements.
