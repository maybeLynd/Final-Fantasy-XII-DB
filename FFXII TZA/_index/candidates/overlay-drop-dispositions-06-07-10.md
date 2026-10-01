# SECTIONs 06 / 07 / 10 overlay: per-token drop dispositions for OPUS's EFX contract (OPUS, 2026-09-25)

This is the gate file for `overlay-publication-plan.md` ruling 2, covering
`02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md`. The owner review is
`sections06-07-10-efx-owner-review.md`. The owner-merge is done in the worktree; FRONTIER publishes. The
census after the merge shows 0 rows for this file.

| tokens | disposition | where |
|---|---|---|
| `003B4B60`, `003B5520`, `003B50D0`, `003B5660`, `003B56C1`, `002E73FA`, `002E743E`, `003B846F`, `003B855C`, `00520720`, `0042865B`, `003B8260`, `003B879B`, `003A3FD0`, `003326C0`, `003B936B`, `003B938D` | **restored** | the "who asks for a rebase" bullet after SECTION-07's movement/refresh correction, re-counted from the image |

**One correction came out of the re-count.** HEAD said 22 control transfers to `003E6AA0`; the
image has **23**:

- 18 `E8` calls;
- 3 `E9` tail jumps (`003B50D0`, `003B5660`, `003B56C1`);
- 2 `0F 8x` conditional branches (`002E73FA`, `002E743E`).

The restored text states 23. The kind-`0x28` poll arm is cited with its own sites: `003B936B`
`003A3FD0(-1)`, `003B938D` the `+0x288` read, `003B939F` the call.

**Rows for other owners.** `CONTRACT-resource-input-ownership.md` (sections 06/08/09/10) is FABLE's
(RESTORE all, `fable-overlay-dispositions-2026-09-25.md` §3).
