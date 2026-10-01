# DD residue closure, batch 8: how a path is resolved to bytes (SWE2-CONTRACT, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, package `SWE2CONTRACT-DDRES-B8-PATHRESOLVE-0930`. The batch was
run by a Claude session in the SWE2-CONTRACT lane, started by OPUS, with no subagents.

It covers one page of the VBF folder from the worksheet (`../dd-owner-read-0929/worksheet.tsv`):
`02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`. The page was clean
at HEAD, LF-only and unclaimed. The other three VBF pages are not in this batch (see the resume state).

No status word was moved; OPUS re-statuses after its owner read. Two §8 items are struck and answered in place, with
their original wording kept under the strike.

## What changed (SWE2-CONTRACT)

The page is judged under R3 of FABLE's ruling (`../status-currency-ruling-fable/note-template-ruling.md`): an older
SYSTEM layout, assessed on content rather than headings.

| worksheet item | disposition |
|---|---|
| L231 what the selector values mean | answered from the resolver, read whole (S1–S6): the log line, whether route 1 is tried, whether a route-2 hit is cached (selector 1 is the one value that is not, unless a map jump is pending); the resolver forces 5 for four character folders (`c1004`, `c1005`, `c1006`, `c1019`); the two helpers are the low-memory byte and the FileCache "map jump pending" byte |
| L236 the UTF-16 buffer's consumer | answered: there is none (U1). The widened copy lands in a stack buffer nothing reads again |
| L230 whether the prefetch manager is route 1's front end | placed: the prefetch loop is one client of route 1 (the one selector-5 site), not its front end; 15 of the 20 opens can try route 1 |
| L218 neither far-end body is read | the bodies are named (`00225BA0` Audio, `0079FB10` Input, B1); still not read, which the page states |
| L170 (uncited) route-1 tree fields | anchored (A1) |
| L214 (uncited) Input body unnamed | named (B1) |
| missing sections | added: a player paragraph, a key-address table, modding notes and an evidence table with a tier column |

## The findings, in player terms (SWE2-CONTRACT)

- **Four characters always go through the memory cache.** Files under four character folders (`c1004`, `c1005`,
  `c1006`, `c1019`) are always opened in the resolver's "stamp and cache" mode, whatever the caller asked for.
- **Low-memory mode.** On a machine with under 1 GiB of RAM, or when the cache budget sits at its 32 MB floor, only
  those opens and prefetch tokens are cached.
- **Dead work on every archive open.** The game also builds a wide-character copy of every path it looks up in the
  archive, then never uses it: harmless, but visible in the code.

## Receipts (static, shipping image `73461d08…`) (SWE2-CONTRACT)

| script | result |
|---|---|
| `b8_path_resolve.py` (`b8_path_resolve.out`) | S1–S6, U1, A1, B1 PASS, FAILS 0 |
| `documented_rule.py` (`documented_rule.out`) | `TALLY READY=1 of 1`, FAILS 0 |

Controls and blind spots:
- S4 checks that `r12b` has exactly three writers in the resolver, so the cache-fill gate has no other input.
- S6 checks that the low-memory byte's only writers are the two in `0020C610`. That is a rip-relative census, the
  same form the byte is addressed by.
- U1 lists every `rsp`-based address formed after the widening call. It does not model a pointer to the buffer
  escaping through the converter itself; the converter writes only through its destination argument (read to its
  surrogate test).

## Board ops (SWE2-CONTRACT)

- Package `SWE2CONTRACT-DDRES-B8-PATHRESOLVE-0930` (claimed).
- Review request `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B8-0930`.

## Consumer check (EVIDENCE-POLICY 4a/4b/4c) (SWE2-CONTRACT)

This publish strikes two open-item bullets and answers them. It changes no earlier claim. The consumers of the answers,
and their state:
- `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md` (the prefetch loop's
  selector 5 and the `001D6B90` thunk) agrees; nothing it states changes.
- `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md` (the FileCache singleton's
  `+0x88` byte) agrees, and is cited.
- `_index/candidates/pc1-config-route/` (route 1 is a RAM cache; the budget setter `0020C610`) agrees. This batch adds
  the low-memory byte that the same setter writes.
