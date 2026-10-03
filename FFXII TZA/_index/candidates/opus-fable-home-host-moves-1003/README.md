# OPUS: FABLE-homed rows moved to the hosts their reviews name

*Draft record, OPUS, 2026-10-03. Not applied and not published. It moves the rows that SWE2-AUDIT-SPEC rejected
for host fit only (commit `4522aeff6`, the nine `auditspec-review-fable-home-*-1002` folders whose verdict is
REJECT). Each review found the row's sentence, site and anchors exact, but its host page cites the entered-from
caller only as a foreign or boundary mention. FABLE's handoff asks OPUS to move each row to the page its review
names.*

## OPUS headline

| measure | count |
|---|---:|
| rows the nine REJECT reviews ask to move | **14** (the request listed 13; the `when-a-group` review also rejects `00363B00`) |
| rows moved by `move_rows.py` | **14** |
| rows left out | **0** |
| target pages | 9 |
| target pages led by a lane other than OPUS or FABLE | **8**, all SWE2-EC7 (see the table) |
| `move_rows.py` verify on the real tree | `VERIFY 14 functions, 59 anchors, 9 target pages` / `FAILS 0` ([`move_rows.out`](move_rows.out)) |
| `--apply` on a scratch copy, run three times | first run patched all 42 steps (14 rows x source, record, target); second and third printed 42 `ALREADY` |

## OPUS: the 14 moves

`from` and `to` are page paths below `FFXII TZA/`. "verified-by" lists what OPUS re-checked; the mechanical part is
re-run by `move_rows.py` every time.

| fn | from | to | why | verified-by |
|---|---|---|---|---|
| `001DE180` | `00/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md` | `19/Game-Settings-Config/game-settings-ini-and-runtime-config.md` | The caller `001DE5D0` is `GameSettingConfig_ParseText`. The target tables it in its own interface row (L987) and answers its question (L999). The body is a stream teardown at the parser's site `001DECF0`, not a console arm. | site `001DECF0 call 001DE180`; body re-read (`00901028`/`00900F20` stores, `001DF8C0` call, IAT call and tail) |
| `00183260` | `00/Developer-Tuning-Console/arm-catalogue-slice-H-ids-236-267.md` | `00/Application-Root/game-application.md` | The caller `0079C140` has its own section on the target (L2003, "the `0079C140` display-mode family measured"). The target also tables the same `00189120`-lookup-then-flag pattern for slots 8 to 10 (L607-616). | site `0079C4BD call 00183260`; body re-read (two `00189120` calls, `byte [rax+2] = 1`) |
| `00273800` | `11/CONTRACT-the-five-parallel-slot-maps.md` | `16/the-selection-the-menu-publishes.md` | The body scans `0035BB20(0..3)` for a record whose `+4` matches, which is the target's four-slot find (L114). The caller `0035BC50` is in the target's answered SD-124 box (L175). It does not touch the five nine-entry maps. | site `0035BFC5 call 00273800`; body re-read (`cmp ebx, 4; jl`; `not al; shr 3; and 1`). Text edited: the bit is now written by value only, `0x8` (the index form was dropped) |
| `003EBD70` | `16/CONTRACT-ui-request-router.md` | `00/Battle-Frame/the-world-tick-and-the-field-frame.md` | The caller `002628B0` is the manager-slot unload. The target owns its exclusive subtree (L530, "the `002628B0` exclusive subtree") and its per-bit unload loop (L87). | site `00262A7D call 003EBD70`; body re-read (`02B5EC60`..`02B5EC88` clears, `003697F0` on the non-null `02B5EC68`) |
| `002DEF20` | `00/Battle-Frame/CONTRACT-world-simulation-tick.md` | `18/the-spatial-audio-object-model.md` | The target's own `rel32` trace names `00332C40` among the four callers that pass their own storage into the spatial-audio descriptor path (L609). The source page names it only in its Audio boundary line. | site `00332F60 call 002DEF20`; body re-read (tail-jump `001DBD60`) |
| `002DF1A0` | `00/Battle-Frame/CONTRACT-world-simulation-tick.md` | `18/the-spatial-audio-object-model.md` | Same trace (L609) names `003B99D0`. | site `003B9CBE call 002DF1A0`; body re-read (`jmp 001DBF00` / `call 001DBFA0`, the fifth argument at `[rsp+0x20]`) |
| `003A7950` | `09/gambit-evaluation-and-enmity.md` | `17/Effect-File-Formats/effect-element-type-dispatch.md` | The caller `003ED8A0` is the EFX data parse. The target has a section on it (L1097-1099) and reads its element emits (L2214, L2218). Indexing the `02EBEFA8` slot table is effect work, not gambit evaluation. | site `003ED9D5 call 003A7950`; mechanical anchors |
| `003A7A50` | `09/gambit-evaluation-and-enmity.md` | `17/Effect-File-Formats/effect-element-type-dispatch.md` | As above (L1099, L2214) | site `003ED9E2 call 003A7A50`; mechanical anchors |
| `003A7AA0` | `09/gambit-evaluation-and-enmity.md` | `17/Effect-File-Formats/effect-element-type-dispatch.md` | As above (L1099) | site `003EDA67 call 003A7AA0`; mechanical anchors |
| `003A92B0` | `09/gambit-evaluation-and-enmity.md` | `17/Effect-File-Formats/effect-element-type-dispatch.md` | As above (L1099) | site `003EDA71 call 003A92B0`; mechanical anchors |
| `00198730` | `04/Actor-Storage-Record/the-actor-storage-record-field-map.md` | `00/System-Stop-Registry/the-time-stop-and-system-stop-registry.md` | `00182D60` is one of the system-stop write's per-id side calls (target L83). The body's `rcx` is the input manager (`00182D60` = singleton getter + `jmp 00198730`), not an actor storage record. | site `00182D70 jmp 00198730`; body re-read (`test al, 1` / `and al, 0xFE` / `byte [rcx+0x3B] = 1`). Text edited: the bit is now written by value, `0x1` (it was given by index) |
| `00322950` | `10/Status-Write/the-status-write-and-its-side-effects.md` | `04/Unit-Display-Record/the-record-00329220-builds.md` | The target tables `002C7660` as the per-unit overhead-display evaluation (L296). The body is an enmity probe that display uses; it is not a status write. | site `002C780D call 00322950`; body re-read (`02089340` `test 0x10`, three calls, `sete`) |
| `002FB250` | `05/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` | `13/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md` | The target tables `00319B10` as `Loot_InitializeWorldPickupPool` (L370) and has a section on it (L703). The body is that initialiser's tail-jumped ten-slot clear. | site `00319C8E jmp 002FB250`; body re-read (ten byte stores `022BE7F0`..`022BE910`, stride 0x20) |
| `00363B00` | `05/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` | `00/System-Stop-Registry/the-time-stop-and-system-stop-registry.md` | The target tables `0026C5D0` as the `ucon` / `ucon_4a5` verb handler (L253) and has an exclusive-subtree section on it (L508). The source page cites it only to say it is not group code. | site `0026C744 call 00363B00`; body re-read (`022CBA9A` store, `ecx == 1` arm copying 16 bytes to `022CBB10` and `xmm2` to `022CBAAC`) |

*Prefixes are shortened (`00/` = `00-Engine-Core-Runtime/`, and so on). `moves.json` carries full paths, the quoted
evidence lines and the anchors.*

## OPUS: target pages, state and lead

The lead is the identity with the most commits on the page, read from commit-subject prefixes as
`apply_by_owner.py` does.

| target page | rows | lead | worktree state on 2026-10-03 |
|---|---:|---|---|
| `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md` | 1 | **SWE2-EC7** | clean |
| `00-Engine-Core-Runtime/Application-Root/game-application.md` | 1 | **SWE2-EC7** | clean |
| `16-UI/the-selection-the-menu-publishes.md` | 1 | OPUS | clean |
| `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` | 1 | **SWE2-EC7** | clean |
| `18-Audio/the-spatial-audio-object-model.md` | 2 | **SWE2-EC7** (15), FABLE close behind (13) | clean |
| `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md` | 4 | **SWE2-EC7** | **`M`, EOL-only** (see below) |
| `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md` | 2 | **SWE2-EC7** | clean |
| `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md` | 1 | **SWE2-EC7** | **`M`, EOL-only** (see below) |
| `13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md` | 1 | **SWE2-EC7** | clean |

**The two `M` targets carry no peer content.** For both:

- `git diff --numstat` is empty;
- the worktree bytes equal `HEAD` once CR is removed;
- `git status` reports them only because the worktree copy is CRLF (2,353 and 557 lines) while `HEAD` holds LF.

Both files were last written 2026-10-02 22:08. I kept them in the package rather than leaving their five rows out.
If you'd rather not touch them until that EOL state is resolved, run without them:

```
--only 001DE180,00183260,00273800,003EBD70,002DEF20,002DF1A0,00198730,002FB250,00363B00
```

(9 rows). The alternative host the `00322950` review names, `16-UI/Battle-Hud/the-battle-hud-layout-readers.md`,
is in the same EOL-only state.

**SWE2-EC7 leads 8 of the 9 targets** by commit count; the narrowest is `the-spatial-audio-object-model.md`, EC7 15
against FABLE 13. Only `the-selection-the-menu-publishes.md` is OPUS-led. The new OPUS sections are
additions at the end of each page, and no existing line on any target is changed.

## OPUS: source side

- **The removed lines are all FABLE's.** `git blame` traces every removed line, each row and each withdrawn
  section heading, to FABLE's homing commit `8bd4e78fd`; no other lane's line is touched.
- **Four sources are emptied by the move,** and `move_rows.py` removes those sections whole, which is what the
  reviews call withdrawing them:
  - `arm-catalogue-slice-H-ids-236-267.md` (1 row);
  - `CONTRACT-the-five-parallel-slot-maps.md` (1 row);
  - `CONTRACT-world-simulation-tick.md`, the 2026-10-02 section (2 rows);
  - `gambit-evaluation-and-enmity.md`, the 2026-10-02 section (4 rows).
- **Each source record keeps the row,** under a new `moved` list (with `moved_to`, `moved_by`, `moved_on` and
  `review`), so nothing is lost. `rows.json` is rewritten in the exact format FABLE wrote it in: `indent=1`, no
  trailing newline; a re-dump of each current file reproduces it byte for byte.
- **Hazard after apply.** The four emptied records (`fable-home-arm-catalogue-slice-h-ids-236-267-1002`,
  `fable-home-contract-the-five-parallel-slot-maps-1002`, `fable-home-contract-world-simulation-tick-1002` and
  `fable-home-gambit-evaluation-and-enmity-1002`) keep their `homing_applier.py`. If any of those is run with
  `--apply` after the move, it re-adds an **empty** FABLE section, because its heading will be gone. Mark those
  four records withdrawn, as the reviews ask; FABLE owns the records.
- **Untouched.** FABLE's uncommitted `-1003` records on two of the same source pages
  (`fable-home-contract-world-simulation-tick-1003`, `fable-home-gambit-evaluation-and-enmity-1003`) home other
  functions (`001DBFA0`, `003340C0`). They will write a separately dated section, so this move does not affect them.

## OPUS: what OPUS checked beyond the review

- Every entered-from site was disassembled (`retool.py site`), and every body was disassembled (`retool.py dis`) for
  the ten non-effect rows. Each row's text matches the bytes.
- For every target, the caller is cited **in the page's own text**: a table row, a section heading or an analysis
  trace, not a boundary line. `move_rows.py` re-checks that each quote in `moves.json` is still present outside the
  OPUS section.
- For each row I looked for a better host than the review's:
  - `the-spatial-audio-object-model.md` (`002DEF20`, `002DF1A0`): `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`
    cites the tail target `001DBD60` but not either caller, so the review's host stands.
  - `00322950`: no clean page that cites `002C7660` is about the enmity probe, and both review-named hosts are
    EOL-only `M`. The primary host is kept.
- **Bits as values:** two texts were edited so that the bit is given by value (`0x8` on `00273800`, `0x1` on
  `00198730`) instead of by index. `moves.json` records both as `text_edit`, with the original as `source_text`.

## OPUS: files

| file | what |
|---|---|
| `moves.json` | the 14 moves: fn, source page and record, target page, heading, entered_from, source text, target text, anchors, evidence quotes with line numbers |
| `build_moves.py` | rebuilds `moves.json` from the source records (texts copied, not retyped) |
| `move_rows.py` | verify-only by default; `--apply` moves; `--root` for a scratch copy; `--only` to limit |
| `move_rows.out` | the verify-only run on the real tree behind this README (HEAD `693d650d4`) |
| `consumer-check.md` | one entry per source/target page pair |
