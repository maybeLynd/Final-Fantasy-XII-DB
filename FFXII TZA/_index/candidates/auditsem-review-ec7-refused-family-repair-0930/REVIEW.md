# SWE2-AUDIT-SEM review — EC-7 refused-family repair (SEAD membership + mechanical removals, 2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-29/30.*

| | |
|---|---|
| request | `SWE2-EC7-REQ-AUDITSEM-REFUSED-FAMILY-REPAIR-0929` (SEAD row T1; the other 30 rows T0 spot-check) |
| reviewed | `839236205` (author **SWE2-EC7**; not an OPUS-lane production) — [`ec7-refused-family-repair-0929/README.md`](../ec7-refused-family-repair-0929/README.md) |
| tree at review | HEAD `0aa544606` (plus peers' uncommitted pages, which move A by +7; see below) |
| **verdict** | **ACCEPT** |

## SEAD row (T1) — re-derived (SWE2-AUDIT-SEM)

- **The selector reproduces the file.** `rerun_audio.py` runs `18-Audio/members/select_audio_libraries.py` through
  `runpy` without `--write` (nothing in the tree is written) and diffs its six lists: **SEAD 1,136 = tracked 1,136,
  identical**; libogg framing 22, Tremor + vorbisfile 102, CRI HCA 53, libvorbis 116, bitwise 4 — all identical to
  the tracked files. Its closure assertions pass with the patch (UC-1 frontier bodies left out of the population).
- **Every member is in the span or one of the nine.** Of the 1,136, exactly nine lie outside `[007A4380, 007F41A0)`:
  `007F7360 007F7380 007F7390 007F73D0 007F7400 007F7420 007F7440 007F74E0 007F7570` — the selector's own "SEAD entries
  past the span added" list, the nine the row names.
- **The arithmetic.** At `839236205^` the file held 1,170; now 1,136; the 34 departures equal the SEAD rows of
  `removed-members.tsv` exactly, and nothing was added (`a_check.out.txt`). 33 are A-measured, **A in the current
  tree** (with peers' uncommitted pages present, A is 9,302; all 33 remain A). The 34th, `007EE7F0`, is **not a census
  entry** any more (the UC-1 series break's false entry).
- **The cause of the 1144 / 1170 mismatch is `8a2c65e08`.** Declared count vs members-file lines, per commit:
  `8a2c65e08^` 1170 / 1170; **`8a2c65e08` 1144 / 1170** (the count changed, the file did not); `839236205^` 1144 /
  1170; `839236205` 1136 / 1136. The 2026-09-20 edit is the break, as the record says.
- **No consumer reads the old counts.** A grep of the database's `.md` / `.tsv` / `.json` for `1144`, `1,144`, `1170`,
  `1,170` beside SEAD/audio finds only the row itself (now 1136) and unrelated sound-bank file names.

## The other 30 rows (T0 spot-check) (SWE2-AUDIT-SEM)

- **All 132 A-measured removals are A now** (`a_check.out.txt`: 132 of 132, all census entries, none a UC-1 body).
- **The 23 cascade returns** are census entries, not A, not UC-1 — frontier, as stated.
- **Selector reproduction, two Phyre modules** (`rerun_phyre.py`, `select_phyre_module.py` via `runpy`, no write):
  PRendering 286 = tracked 286, PPostProcessing 156 = tracked 156, both identical — the cascade-bearing rows.
- **`check_dispositions.py` at HEAD:** families accepted 334, **refused 0**; B 3,063 and C 16,890 exactly as the
  record's "after"; A 9,302 and frontier 5,809 differ from the record's 9,295 / 5,816 by the +7 A that peers' pages
  gained since, not by anything in this package. `--self-test`: 13 cases pass.

## Not reviewed (SWE2-AUDIT-SEM)

The withheld selector additions (`selector-drift.tsv`, 134 would-admit) are T2 family decisions the record routes to
FABLE; they were not applied and are not judged here.

## Receipts (SWE2-AUDIT-SEM)

`receipts/rerun_audio.py`, `a_check.py`, `rerun_phyre.py` and their `.out.txt`, `check_dispositions.out.txt` (run from
`Database/Tools/work/SWE2-AUDIT-SEM/ec70930/`).
