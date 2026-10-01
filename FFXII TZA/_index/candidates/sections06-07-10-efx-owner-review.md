# SECTIONs 06 / 07 / 10 — owner's review of the EFX source-rebase rewrite (OPUS, 2026-09-25)

`02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md` is OPUS's; the worktree carries an
uncommitted rewrite (9,073 -> 9,591 words) from SECTIONs 06, 07 and 10. No section claim was
re-derived here; this is the carried-evidence check only.

## Verdict: THE TRIGGER SURVIVES, THE REQUESTER CENSUS DOES NOT — restore before publication

Kept (restated): the rebase is demand-driven — `003E6AA0` queues a resolve, `003B3C00` receives it
(`demand` 3/3 mentions, `003E6AA0` 4 -> 3, `003B3C00` 7 -> 4).

Dropped, with no restatement (17 tokens, `overlay-drop-census-2026-09-25.tsv`):
- **the runtime-mode binding family `003B4B60`–`003B5520`** that requests n on a mode/binding
  transition (2 -> 0 mentions);
- **`003B8260`'s element-kind dispatch** — `jmp rcx` at `003B879B`, byte map `0x3B994C` — and its
  two request sites `003B846F`/`003B855C` (n = 0xA on a link-word mismatch) (6 -> 1);
- **the mount path's n = 3 request** inside `002E73C0` and its two conditional tail branches
  `002E73FA`/`002E743E`;
- the parent-record resolve `003A3FD0(-1)` -> `003326C0`, the `003B50D0`/`003B5660`/`003B56C1`
  sites, and **presentation command `0x28` = `00520720`**, with the delivery site `0042865B`.

These are the census of WHO asks for a rebase. Without them a reader of the contract knows the
mechanism but not its callers — the half a reimplementation needs to decide when to run it.
