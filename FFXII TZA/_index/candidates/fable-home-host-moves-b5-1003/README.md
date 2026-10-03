# FABLE: homed rows moved for host fit, batch 5 (the steal roll and the three batch-4 deferrals)

*Draft record, FABLE, 2026-10-03. Not applied and not published. It repairs five homed rows that SWE2-AUDIT-SPEC
rejected for host fit:*
- *the two rows of [the steal-roll review](../auditspec-review-fable-home-the-steal-roll-1003/REVIEW.md), from
  commit `6435250e4`;*
- *the three rows that [`fable-home-host-moves-b4-1003`](../fable-home-host-moves-b4-1003/README.md) deferred, from
  the batch-4 reviews of commit `95d495604`.*

*It is built on the b4 record. `move_rows.py` is that script plus three things: a `host` basis on each move, `adds`
(a row for a body no page states yet), and `unbound` drops (rows returned to the frontier).*

## FABLE headline

| measure | count |
|---|---:|
| rows moved, host cites the caller (`host: caller`) | **1** (`00394380`) |
| rows moved, host states a callee (`host: callee`) | **2** (`004EB910`, `00314D60`) |
| rows moved, caller homed in the same section (`host: row-caller`) | **1** (`001DD0B0`) |
| rows newly homed (`adds`) | **1** (`0017FF20`, from the steal-roll review's sentence) |
| rows returned to the frontier (`drops`, `unbound`) | **1** (`00361480`) |
| target pages | 4, all clean at `410ec4476` |
| source pages | 4, all clean; 3 sections withdrawn whole (steal roll, input contract, ff12config) |
| `move_rows.py` verify on the real tree | `VERIFY 5 functions, 24 anchors, 4 target pages, 1 adds, 1 drops` / `FAILS 0` ([`move_rows.out`](move_rows.out)) |
| `--apply --root` on a clean detached `410ec4476` worktree, twice | first pass: 15 `PATCHED`, `FAILS 0`; second pass: 15 `ALREADY`, `FAILS 0` |
| sensitivity controls ([`controls.py`](controls.py)) | `CONTROLS 7, NOT REFUSED 0` ([`controls.out`](controls.out)) |
| `--only` (rows held) | none |

## FABLE: the rows

Page paths are below `FFXII TZA/`, shortened (`00/` = `00-Engine-Core-Runtime/`, and so on). `moves.json` has the
full paths, the evidence quotes with line numbers, and the anchors.

| fn | from | to / drop | host basis | review |
|---|---|---|---|---|
| `00394380` | `08/Steal/the-steal-roll.md` | `16/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md` | caller `003939B0` is the page's 0x1D0 consumer: "Selected handler" row (L42), "RSI in `003939B0`" (L44) | [review](../auditspec-review-fable-home-the-steal-roll-1003/REVIEW.md), Repair 1 |
| `0017FF20` | (newly homed) | `00/Developer-Tuning-Console/the-282-command-parameter-console.md` | callee `001DDAB0`, the page's 8-byte getter (L120, L258) | [review](../auditspec-review-fable-home-the-steal-roll-1003/REVIEW.md), Repair 2 |
| `001DD0B0` | `08/Steal/the-steal-roll.md` | `00/Developer-Tuning-Console/the-282-command-parameter-console.md` | its only caller `0017FF20` is homed in the same section; it reads the fields the page's setter `001DC920` writes (L599) | [review](../auditspec-review-fable-home-the-steal-roll-1003/REVIEW.md), Repair 2 |
| `004EB910` | `00/CONTRACT-boot-fixups.md` | `17/Legacy-PS2-GS/the-vif1-vu1-layer.md` | callees `0022CC40` / `0022CC30`, the page's VU sticky Z / sticky S helpers (L383, L387-389, L724) | [review](../auditspec-review-fable-home-contract-boot-fixups-1002/REVIEW.md) |
| `00314D60` | `19/Game-Settings-Config/ff12config-and-debglobal.md` | `01/verbs-that-only-wait-and-verbs-that-do-nothing.md` | callee `005C5230`, the page's folded `poll` stub (L201) | [review](../auditspec-review-fable-home-ff12config-and-debglobal-1002/REVIEW.md) |
| `00361480` | `15/CONTRACT-input-subsystem.md` | **drop, unbound**: "returned to the frontier: no host cites a caller or callee" | none (below) | [review](../auditspec-review-fable-home-contract-input-subsystem-1002/REVIEW.md) |

*Line numbers are from the shared tree at `410ec4476`. `move_rows.py` checks each quote by its text, not its line.*

Every moved row keeps its anchors. Its text is copied from the source page's current row, not retyped
(`build_moves.py`). The page and the record agree for every row except `004EB910`, and `build_moves.py` checks that.
For `004EB910` the page is the source, because it carries the `4534596f2` correction and the record's `rows.json`
text is older.

**One text edit, `004EB910`.** On the boot-fixups page the corrected clause reads "to ~~1.0 (`01E0283C`)~~ the sum of
the `.data` floats ... (file values 0.0 and 1.0) *(corrected 2026-10-03, FABLE, ...)*". The moved row keeps the
corrected clause word for word, "to the sum of the `.data` floats `01E02838` + `01E0283C` (file values 0.0 and
1.0)", and drops only the strike and the dated note.

The edit is needed because the VIF1 page never said "1.0". `publish_correction_gate` (through `cloud/cgate.py`)
refused the first draft: "the-vif1-vu1-layer.md strikes text it never said: 1.0 (`01E0283C`)". The correction stays
on record in `fable-corr-004eb910-1003` and in the source record's moved entry. `moves.json` `text_edit` records
what was removed and what was kept.

## FABLE: how each host was found

The raw transfer index (E8/E9 rel32, 0F 8x rel32, EB/7x rel8) was taken over all of `.text`. Each hit was decoded as
a direct call or jump to the entry and grouped by its owning function. The bodies' own direct targets came from
their full disassembly. Each address was then searched on every bearing page (no path part starting `_`).

- **`004EB910`** (1387 B). Callers: `004EBE80` only, at +0x74A, +0x804, +0x8BE, +0x978 and +0xA25. That function
  is named on no page but the boot-fixups contract (in the "`008631E0` registers" line and the homed row). Direct
  targets: `0022CC40`, `0022CC30` and `0022CC20`, four times each. The VIF1 page states the first two as its own
  (key addresses: "VU sticky Z / sticky S"), and its §2 says "Forty functions call them". This is the page the review
  named, and it is now reached through a callee instead of waiting for a citation of `004EBE80`. The row carries the
  `4534596f2` correction, so the review's second condition (its defect 2) is met.
- **`00314D60`** (32 B). Caller: `0050C8A0` only (`jmp` at +0x24), named on no page but ff12config's neighbours line.
  Direct target: `005C5230`, which the verbs page states in its key-addresses table as "the stub `poll`". This is the
  page the review named ("the natural home ... through the non-caller stream").
- **`00361480`** (61 B). Callers: `00342770` (+0x83) and `00341C80` (+0x16). Direct targets: none (the body is a
  leaf loop). `00342770` is named on one bearing page, the input contract, in its "OUT-OF-SCOPE" script-verb
  neighbours line. That page is the rejected host. `00341C80` is named on no bearing page. With no caller or callee
  on any host, the row is dropped and the body returns to the frontier. `move_rows.py` re-derives both sets and the
  page list on every pass, so a later citation of either caller fails the check and shows that the row can be
  re-homed.
- **`0017FF20`** (36 B), the steal-roll review's Repair 2 sentence, checked against the bytes:
  - `0017FF24 call 001DDAB0`, then `test rax, rax`, and `0017FF2C je 0017FF3F`, which goes to `add rsp, 0x28; ret`
    with `rax` still null ("when it returns null returns that null");
  - `0017FF2E call 001DDAB0` again, `0017FF33 mov rcx, rax`, then `0017FF3A jmp 001DD0B0` ("tail-jumps ... with the
    result in `rcx`").

  The sentence is exact. The five anchors are those five instructions. The raw index gives one caller, `0023B530`
  (+0xC5, `call`). The steal-roll page reads that function in its EC7-107 section, so `0017FF20` could have been
  caller-homed there. The review homes it on the console page instead, beside `001DD0B0`, and this record follows
  the review. On the console page its basis is the callee `001DDAB0`.

## FABLE: notes and leads

- **The `00361480` leads are not taken here.** Two routes could home it later:
  - OPUS's untracked verb-adapter package, `opus-ee-verb-adapters-1003`, lists `00341C80` (`musicreadsync` begin)
    for a row on the verb-population page. Once that lands, the page cites a caller and FABLE's caller-host stream
    can home the row there.
  - The review's table route: the audio voice page owns the `022CB9F0` slot table and the sibling scans
    `00360C20` / `00361630`. That route is a table host, not a caller or callee, so it is outside this record's rule.
- **New body cites on the target pages.** The rows bring their callers onto the target pages as body cites:
  `0023B530` and `0017FF20` on the console page, `004EBE80` on the VIF1 page, and `0050C8A0` on the verbs page.
  The neighbour pre-check adds no finding (next section).
- **Two batch sections on the VIF1 page.** It already ends with the batch-4 section. This record's heading differs
  (`AUDIT-SPEC batch 5`), so it appends its own section after that one. Neither script matches the other's section.
- **Each section lists why every row is there** in a bullet above its table. `section_text` builds that list from
  every `moves.json` entry for the page, so `--only` does not change it.

## FABLE: gate pre-checks

Both checks ran on the applied worktree (`410ec4476` plus this record), with all 19 paths: 8 pages, 4 records and
the 7 files of this record.

- **`check_publish_neighbours.py`:** `UNACCOUNTED NEIGHBOUR   HEAD 184   HEAD+publish 184   (19 path(s) in the
  batch)` / `ADDS NOTHING`. An earlier pass that named only the 8 pages refused on 4 links to `move_rows.py`. That
  record was not in that batch. The links resolve once it is.
- **`publish_correction_gate`** (`cloud/cgate.py`): `True []`, after the `004EB910` text edit above.

## Consumer check (FABLE)

affected: Database/FFXII TZA/08-Combat-Formula/Steal/the-steal-roll.md
affected: Database/FFXII TZA/16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md
affected: Database/FFXII TZA/00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md
affected: Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-boot-fixups.md
affected: Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md
affected: Database/FFXII TZA/19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md
affected: Database/FFXII TZA/01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md
affected: Database/FFXII TZA/15-Input/CONTRACT-input-subsystem.md

- consumer: the steal-roll page's FABLE homed section (2026-10-03): revised-here (both rows removed; section withdrawn).
- consumer: the boot-fixups contract's FABLE homed section (2026-10-02): revised-here (the 004EB910 row removed; the
  004E7980 row stays, as its review accepts).
- consumer: the ff12config page's FABLE homed section (2026-10-02): revised-here (row removed; section withdrawn).
- consumer: the input contract's FABLE homed section (2026-10-02): revised-here (row removed; section withdrawn).
- consumer: the title-asset page, the console page, the VIF1 page and the verbs page: revised-here (each gains the
  batch-5 section; no existing line changes).
- consumer: the four source records' rows.json (steal roll, boot fixups, ff12config, input subsystem): revised-here
  (rows moved to `moved`, or to `dropped` with the unbound reason).
- consumer: the steal-roll review's Repair block: agrees (items 1-3 as written, including the 0017FF20 sentence).
- consumer: the boot-fixups review: agrees on the host it names (the VIF1 page), reached through a callee instead of
  through the caller citation it waited for; its defect 2 correction is already in the moved text.
- consumer: the 004EB910 correction record (fable-corr-004eb910-1003): agrees (its corrected clause moves word for
  word; only the strike and the dated note stay behind with the removed row).
- consumer: the ff12config review: agrees (the page it names, through the non-caller stream it allows).
- consumer: the input-subsystem review: agrees that the row cannot be caller-hosted. The body is
  routed-to-FABLE-HOMING-CALLER-HOST-1003 for when a page cites one of its callers (leads above).
- consumer: the batch-4 record's deferred list: agrees; this record settles all three rows.

run: move_rows.py at 410ec4476 (VERIFY 5 functions, 24 anchors, 4 target pages, 1 adds, 1 drops / FAILS 0)

Proof of the apply: on a clean detached worktree of that commit, two `--apply --root` passes gave 15 `PATCHED` then
15 `ALREADY`, with `FAILS 0` both times. `git diff --stat` there showed 12 files changed, 175 insertions(+) and
123 deletions(-): the 8 pages above and the 4 source records.

## FABLE: files

| file | what |
|---|---|
| `moves.json` | 4 `moves` (each with `host`), 1 `adds`, 1 `drops` (with `unbound`: reason, raw callers, callees, non-host cites) |
| `build_moves.py` | rebuilds `moves.json` from the source pages and records (texts copied, not retyped) |
| `move_rows.py` | the b4 script plus `host`, `adds` and `unbound` drops; verify-only by default; `--apply`, `--root`, `--only`, `--moves` |
| `move_rows.out` | the verify-only pass on the shared tree at `410ec4476` |
| `controls.py` / `controls.out` | seven one-entry mutations of `moves.json` (wrong host basis, a callee that is uncited or not called, a missing homed caller, an incomplete caller set or cite list, a shifted anchor); each must be refused |
