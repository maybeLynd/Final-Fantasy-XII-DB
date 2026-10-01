# RC round 3: RC-37, RC-28, RC-30, RC-25 and RC-5 incorporated, and RC-30's byte order answered (SWE2-CONTRACT, 2026-09-30)

affected: _index/OPEN-QUESTIONS.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/btm-exfont-bitmaps.md, 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/as7-menu-graphics-containers.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md
corrects: RC-30 (round-2 NARROWED text and cl2-menu-colour-tables.md §3/§7 "no constant-request site", "no reader found", "component order not established"); RC-25 (the only-writer premise, narrowed)

Requests: `OPUS-REQ-CONTRACT-RC37-ROW-0930`, `DATA-REQ-CONTRACT-RC30-RC28-0930`,
`AUTO-INCORP-DATA-REQ-AUDITSEM-RC30-RC28-0930`, `DATA-REQ-CONTRACT-RC-NARROWINGS-0930`, and the RC-5 / RC-25 / RC-30
parts of `OPUS-REQ-CONTRACT-RC4-5-30-ROWS-0930`. The RC-4 part of that request is not done here (see the last section).

run: `rc_round3_check.py` at `d684a92b7` (an ancestor of the publishing commit), output
[`rc_round3_check.out`](rc_round3_check.out), FAILS 0. Static reads of the certified image
(`73461d08…d89721f8`) and the 20 shipped `loca_*.cl2` files; nothing executed, nothing live.

## What changed (SWE2-CONTRACT)

**Two publishes (OPUS adjudication, 2026-09-30).** `_index/OPEN-QUESTIONS.md` holds another lane's uncommitted edits
(SWE2-DATA's SD-60..SD-67 restatements and SD-16x dedup), so it cannot be published without sweeping them in.
- **Publish 1:** this record and the four pages. The register rows keep their prior status, and the RC-30 / RC-37 boxes
  stay unticked. `rc_round3_check.py` checks exactly that state (D0).
- **Publish 2:** once the register is clean, `Database/Tools/work/SWE2-CONTRACT/apply_round3_rows.py` (idempotent,
  row-scoped through `register_row.py`) restates the rows below. The same publish ticks the two boxes, re-runs this
  checker (D1–D8) and adds the register path back to the declaration line at the top.

The table below is the full round-3 content across both publishes. **Publish 2 is done:** the register was clean after SWE2-DATA's `583b096f7`, the rows were applied and the RC-30 / RC-37 boxes ticked in that commit.

| row | page | change | input |
|---|---|---|---|
| RC-37 | `btm-exfont-bitmaps.md` §7 | **ANSWERED** (static), box ticked, status line current | OPUS `rc37-refused-read-0930` (`b2320ed29`) and SWE2-DATA `rc28-callback-0930` (`79e70e154`), derived separately |
| RC-28 | `btm-exfont-bitmaps.md` §7 | stays ANSWERED; the round-2 leftover (the refused read's completion) carries SWE2-DATA's exact answer | `79e70e154`, AUDIT-SEM ACCEPT `f29e44c6e` |
| RC-30 | `cl2-menu-colour-tables.md` §2, §3, §4, §7 | **ANSWERED** with SWE2-DATA's exact text, ORACLE's independent agreement, the byte order answered here (B), AUDIT-SEM's N1 on the superseded round-2 text; box ticked | `79e70e154` (ACCEPT `f29e44c6e`), ORACLE `be7c6fcd6` |
| RC-25 | `as7-menu-graphics-containers.md` §7 | stays ANSWERED; the domain clause carries AUDIT-SEM's N3 proviso word for word; ORACLE corroboration added | AUDIT-SEM `auditsem-review-rc-residue-0930` §6 N3; ORACLE `be7c6fcd6` |
| RC-5 | `the-event-slot-panel-and-its-dead-feeder.md` §6 | **OPEN, NARROWED again** to one value (the number typed at `evctrl.ebp`'s `event_menu` prompt, 1–9999); **ANSWERED proposed** for a non-author reviewer, not self-closed | ORACLE `rc5b-event-slot-residue-0930` (`be7c6fcd6`) beside FABLE's `63f4b8f89` |

No status word on a page's front matter was raised.

## RC-37: the two records compared (SWE2-CONTRACT)

The request asked for any difference to be kept as a contradiction. **None was found.**
- Both read the same core: `0046E030` returns 1 after `002DF780` (A5), the pump completes from the untouched slot
  `0215EFF4`, both helpers call `00364380`, and `00364380` ignores its flag.
- They name different layers of one allocation. OPUS stops at the pool allocators `0036A100` / `0036A190`; SWE2-DATA
  names the arena entry `0036BC60` and its clamp. The chain joins them (A1–A4, static): `00365810` →
  `00249810` / `002497E0` → `0036A190` (→ `0036A1A0`) / `0036A100` → `0036BC60`. `0036BC60` turns the −1 size into
  `max(size, 0)` rounded up to 64, which is 0 (`0036BC8D cmovns`). The 0 then reaches its first-fit tests
  `cmp [block + 0x18], r14d` (`0036BD03`, `0036BD31`).
- SWE2-DATA also bounds the stale status (the slot starts zeroed; completions store clamped counts or −2, citing
  OV-33 E4). OPUS leaves the worker's result "not traced". That is extra detail, not disagreement.
- **Limit, kept in the row:** what `0036BC60` or its retry `0036BFE0` returns for the 0-byte request. RC-37's question
  (wait, or draw without a sheet) does not depend on it.

## RC-30's byte order, answered here (SWE2-CONTRACT; new production, review requested)

SWE2-DATA left one static fact open: *"the byte order the palette upload in `0024A1D0` declares"*. ORACLE read the
path as far as `0017F3B0` and described its argument as "texture format 1". **That argument is a count, not a format.**
`00180E70` passes `edx = 0x10`, `r8d = 1`, `r9d = 1` (`00180F81`–`00180F8A`). `0017F3B0` uses `r9d` as a level count
(`cmp r15d, 1` / `cmova`). The format is a fixed object.

**Static (the image):**
- B5: `0024A1D0` uploads through `00180E70` (`0024A380`, `0024A3B2`) or `00181000` (`0024A422`). Both call `0017F3B0`
  per palette row (`00180F8E`, `00181122`).
- B3: `0017F3B0` builds its texture with the format object `02CF7480` (`0017F419` `lea r9`, then `0060DD70`).
- B1, B2: `00163D00` constructs `02CF7480` with the name string `RGBA8` (`00D56100`). It passes `0x1C` four times, and
  `00616210` stores them at `+0x20`..`+0x2C`.
- B4: after the copy, `0017F3B0` rewrites byte 3 of every entry as `min(255, trunc(a × 255 × (1/128)))`
  (`0017F517`–`0017F54A`; `008C5B34` = 1/128). So byte 3 is the alpha, on the PS2 `0`–`0x80` scale.

**Authored data:**
- B6, B7: all 20 shipped `.cl2` are `CLT2`. In the three distinct contents, every 4th byte is either `0xFF` (239 of
  512 in `loca_bhm` / `loca_gil`, none in `loca_rbl`) or at most `0x6F`.
- On upload, `0xFF` saturates to 255, and the other bytes scale up (`0x6F` → 221).
- The cl2 page's earlier measurement ("0..255 ALPHA, not the PS2 0..128 convention") stays as a description of the file
  bytes. The engine reads the byte on the PS2 scale.

**Inferred:** `0x1C` is the value of `DXGI_FORMAT_R8G8B8A8_UNORM`. The Direct3D call that consumes `+0x20` is not
traced. The component order **R, G, B, A** rests on two static facts: the format name `RGBA8`, and byte 3 being the
alpha the code rescales. The DXGI value only corroborates it.

## Consumer check (EVIDENCE-POLICY 4a/4b) (SWE2-CONTRACT)

| consumer | claim | state |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` RC-30 | round-2 "cannot produce `0xE2`–`0xE4`" residue | revised-here (ANSWERED; round-2 text restated by AUDIT-SEM N1) |
| `cl2-menu-colour-tables.md` §3 | "no constant-request site", "no reader found", "presumed" | revised-here (struck, reader table) |
| `cl2-menu-colour-tables.md` §7 | component order / reader / variant not established | revised-here (struck, answered) |
| `cl2-menu-colour-tables.md` front matter `archive_formats` | "0x40 header, u16 count at +0x1E, count x 4-byte palette at +0x40" | agrees |
| `rc-residue-0930` §2, `rc22-34-resource-readers-0930` §3 | "no route" sentences | agrees (struck by SWE2-DATA in `79e70e154` / `280006c24`) |
| `rc30-cl2-request-bounds-0930` (ORACLE) | "texture format 1" | routed-to-`SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930`: the phrase names a count argument. ORACLE's own conclusion (no byte reordering; file byte order) stands. **PENDING PROPAGATION** |
| `_index/OPEN-QUESTIONS.md` RC-25 | "`0023AD8E` … no other byte or word write" as the only-writer premise | revised-here (N3 wording) |
| `as7-menu-graphics-containers.md` §7 RC-25 | the same premise | revised-here (round-3 note, N3 wording) |
| `rc-residue-0930` §1 (SWE2-DATA) | the same premise | agrees (producer edit applied, per `DATA-REQ-CONTRACT-RC-NARROWINGS-0930`) |
| `rc25-party-definition-rows-0930` (ORACLE) | "nothing else in the image writes `+0x04`" | routed-to-`SWE2CONTRACT-CONTRA-ORACLE-RC30-RC25-0930`: the row states that ORACLE's reading takes the same proviso. **PENDING PROPAGATION** |

Regressions that reject the old readings (in `rc_round3_check.py`):
- C1: the request `003C207A add r8d, 0xe1` / `003C208D call`;
- C2: the reader `003C27A9 call 0x24a9e0` on `+0x118`;
- D4: the RC-30 row no longer states "cannot produce" as live text;
- B4: the alpha rescale, which rejects a straight 0..255 alpha.

## Checks (SWE2-CONTRACT)

- `rc_round3_check.py`: FAILS 0 (A1–A5, B1–B7, C1–C2, D1–D8; controls K1 a TIM2 is not `CLT2`, K2 the kind-0xFF
  branch tests its submit result).
- `check_questions.py` and `documented_rule.py`: receipts in [`checks.out`](checks.out).

## Not done here, and why (SWE2-CONTRACT)

- **RC-4** (ORACLE `rc4b-capture-residue-0930`: ANSWERED, with OPUS closing assumption 1 and assumption 2 stated).
  **RC-13** (`AUDITSEM-REQ-CONTRACT-RC13-DISPOSITION-0930`; the choice is (a) ANSWERED for the question as asked).
  - Both need their page's box ticked with the row.
  - `the-282-command-parameter-console.md` and `how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`
    carry uncommitted "Cross-subsystem neighbours — FINAL-AUDIT pass 22" appends that are not this session's work.
  - Publishing the box would sweep those appends in, so both rows wait until the pages are clean. The exact edits are
    staged in `Database/Tools/work/SWE2-CONTRACT/` (ignored).
