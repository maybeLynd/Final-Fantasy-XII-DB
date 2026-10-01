# SWE2-AUDIT-SPEC review of SD-22 (sd22-options-volume-rows-0930 at 500458a73): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS. Reviewed
commit `500458a73`, record [sd22-options-volume-rows-0930](../sd22-options-volume-rows-0930/README.md). Static,
checked at HEAD `cb5b622f2`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD22-0930 | sd22-options-volume-rows-0930 | `500458a73` | ACCEPT-WITH-NARROWING |

The answer holds: rows `0x13` / `0x14` / `0x15` send commands `0x13` / `0x14` / `0x15`. The narrowing is to one side
statement of F1's node format, which the answer does not use.

**Re-run.** `sd22_volume_rows.py`: F1-F5 PASS, `FAILS 0`. Output
([rerun_sd22_volume_rows.out](rerun_sd22_volume_rows.out)) is identical to the committed `.out` ignoring CR. The record
directory stayed clean.

**Re-derived independently** ([sd22_rederive.py](sd22_rederive.py) / [.out](sd22_rederive.out), raw bytes via `tk.py`,
not retool):
- **Table and types.** `01E0BF60` holds 45 consecutive image pointers followed by a zero qword, which matches the
  builder's `< 0x2D` bound. Descriptors `0x13`, `0x14` and `0x15` are type 6, and `0x12` is type 2.
- **Parents.** The only descriptors that list `0x13`-`0x15` as children are roots 0, 1 and 2:
  - root 0: child positions 19/20/21;
  - root 1: 18/19/20;
  - root 2: 19/20/21.

  The child entries are `1300fc04000d`, `1400fd04010d` and `1500fe04020d`. F3 holds, including "of no other node".
- **Change path.** `0023EC66 cmp eax, edx` / `je` skips when the value is unchanged. Otherwise
  `0023EC6E movzx ecx, byte [rbx+0xc0]` / `0023EC7A call 00240750` passes the row byte as the first argument. F5 holds.
  `00240750` begins with `lea eax, [rcx-4]; cmp eax, 0x22` (a jump table over ids 4..0x26), so the id is the
  command selector.
- **The narrowing: `+1` is not the descriptor's own id in general.** For 37 of the 45 descriptors, the byte at `+1`
  equals the table index. That includes `0x13`-`0x15`, which is what F3 checks. The other 8 do not:
  - roots `0x00` and `0x01` carry 2;
  - descriptors `0x27`-`0x2C` carry `0x17`. They are type-5, zero-child copies of descriptor `0x17`, and no descriptor
    lists them as a child.

  The row id the handler stores comes from the parent's child entry (item byte 0 → payload `+8` → row `+0xC0`, F4),
  not from `+1`. So the answer is unaffected.

**Controls.** F1, F2, F4 and F5 assert exact instruction text at fixed addresses, so they are sensitive to a
different table, arm or argument. F3 checks `own == k` only for `k` in `0x13`-`0x15`. It could not detect that the
general "own id at `+1`" statement fails for other descriptors, and that is how the over-general wording passed.

**Correction wording for the row owner (SWE2-DATA)** (record text and any page that restates it):
> Each descriptor holds a type byte at `+0`, a byte at `+1`, a u16 child count at `+2` and 6-byte child entries from
> `+4`. The `+1` byte equals the descriptor's own table index for 37 of the 45 descriptors, including `0x13`-`0x15`.
> Roots `0x00` / `0x01` carry 2, and the unreferenced copies `0x27`-`0x2C` of descriptor `0x17` carry `0x17`. A row's
> id comes from its parent's child entry (byte 0), which the builder passes as payload `+8` into row byte `+0xC0`.

A consumer of this correction is
[the-settings-command-table.md](../../../19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md) §4.
It states `Descriptor = {u8 style, u8 id, ...}`, and its `u8 id` has the same over-generality. It is routed to the row
owner to decide; this review does not edit pages.
