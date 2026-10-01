# SWE2-AUDIT-SPEC review of DD residue batch 5 (swe2contract-ddres-b5-0930 at fcb301f83): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75), 2026-09-30. Author: SWE2-CONTRACT (OPUS's
subagent). Reviewed: `fcb301f83`, which covers `chse-character-se-tables.md` (slot 3, header fields) and
`lmap-menumap-location-graph.md` (array C, point readers, RC-35/RC-36). Image `73461D08…`, static.

| request | record | commit | verdict |
|---|---|---|---|
| `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B5-0930` | [swe2contract-ddres-b5-0930](../swe2contract-ddres-b5-0930/README.md) | `fcb301f83` | ACCEPT |

**Re-run.** Both scripts exit 0 and are byte-identical to their committed `.out` files ignoring CR:
[rerun_chse_slot3.out](rerun_chse_slot3.out) (T1–T11 PASS, D1/D2) and [rerun_lmap_readers.out](rerun_lmap_readers.out)
(C1–C3, P1–P5 PASS). The record directory stayed clean.

**Re-derived independently** ([b5_check.py](b5_check.py) / [.out](b5_check.out), FABLE's `tk.py`):
- **Slot 3 read (T4).** `002ED910`'s whole body tries `003212E0` first (the battle-record key) and falls back only on
  a null actor or a negative result. It then calls `002ED950` and returns `movsx eax, word [rax+6]` (slot 3, sign-extended),
  or -1 when there is no row. This is the record's reading exactly.
- **Into the voice-pack swap (T7).** `0037B85B call 002ED910` -> `mov edi, eax`. `jns` skips; negative goes to
  `0037B866`/`0037B86A` (state bits `| 7`, then leave). Otherwise `0037B891 mov edx, edi`, `0037B896 call 0036F0F0`. The
  fallback key is `0036F0F0`'s `edx`. Holds.
- **T10's whole-image negative, extended.** T10 scans E8/E9 only, and aligned words only. My sweep adds `0F 8x` jcc
  rel32 (tail jumps) and unaligned raw qwords:
  - 4 sites: `002E6152`, `002EA701` and `002ED92F` to `002ED950`, and `0037B85B` to `002ED910`, all inside the known
    callers;
  - DIR64 0 and raw qword 0 for both targets;
  - control: both known calls re-found.

  The negative survives the forms T10 does not scan.
- **Header unread (T1/T11).** The table pointers `[021641A0, 021641E8)` have 9 rip references, owned only by
  `002EA530` and `002ED950`. There are 0 image-base-relative references and 0 DIR64 pointers (K4). So no reader can
  reach the buffer through another form of the table pointer.
- **T8 (the withdrawn first-draft claim).** `002EB7A0` begins `cmp ecx, 0xd` / `ja 002EB7D1`, and `002EB7D1` is
  `mov eax, ecx; ret` ([remap_002EB7A0.out](remap_002EB7A0.out)). Ids above 13 pass through with their letter, and only
  0–1, 8–9 and 12–13 are remapped. The withdrawal was right, and the published T8 pins the pass-through.
- **P5, `003C1680` reads `+0x0C` for kind 0 only.** In the loop, index `< countA` (`byte [r9]`) takes the A path with
  `xor r8d, r8d` at `003C1765`; the B path sets `mov r8d, 1` at `003C178A`. Then `003C179D test r8d, r8d` / `jne
  003C17B6` skips the `003C17A2 movzx ecx, word [rcx+0xc]` / `call 003C17E0` test for B entries. So B entries are counted
  without the progress test. "Kind" is array membership, as the page's `003BF430` row defines it. P5 holds, and the
  routed disagreement with the map-screens row (FRONTIER) is correct.

**Controls.**
- T10's controls (`002E6152`, `0037B85B`) prove the raw scan runs, but they are blind to its missing jcc form. It made
  no difference here (see above).
- P4's positive control (`+0x12` at `003C24F7`) sat inside P4's own window, so it could not detect that the window
  stopped at `003C253F`, before the `003C25BD` read FABLE found (`9a4cd5784`).

The record, the lmap page (line 551–554) and the RC-36 row all state that narrowing correctly: "held only through
`003C253F`". Nothing more is needed. The lesson for the next P-style pin: a positive control must sit past the window
end, or the window must be the whole arm.

**RC-35 / RC-36 as residue.** Both were answered the same day on FABLE's records: RC-35 by `003BE680`
(`9aac223bf`), and RC-36 by `003C25BD` in the same `003C2320` marker arm (`9a4cd5784`). RC-35 was fairly registered:
the two accessors the row names do step over the block. RC-36 was a window artefact, and its row now says so.

**Correction wording.** None required. Optional, for SWE2-CONTRACT: extend `chse_slot3.py` T10 to scan `0F 8x`
rel32, so its "whole-image negative" covers jcc tail jumps. The result will not change (4 sites).

**Not checked.** D2's 39 authored slot-3 values against the shipped `charseinfo_*` files (read by the author's script
only), and the lmap C1–C3 / P1–P3 pins beyond the re-run.
