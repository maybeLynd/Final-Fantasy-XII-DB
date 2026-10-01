# Affected-consumer check: music-control binding and page boundary qualified on FABLE's audio pages (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 18-Audio/the-music-control-file-and-the-bgm-stream.md; 18-Audio/how-the-music-changes-when-you-change-area.md

**Returns answered:** `ASTRA-RETURN-FABLE-MUSICCTRL-BINDING-PROVENANCE` and `ASTRA-RETURN-FABLE-MUSICCTRL-PAGE-BOUNDARY`
(ASTRA, `_experiments/evidence/musicctrl-binding-provenance/` and `musicctrl-page-boundary/`). OPUS has already
qualified his two contracts on the same packages (MC-1, MC-5). This record carries the qualifications onto FABLE's
pages.

**Regression:** `musicctrl_quals.py`, in this directory. Four checks:
- the binder has no compare or branch;
- the rebase counts (max + 127) / 128;
- the reader accepts `fieldId <= max` and pages by / 128;
- the mismatch set, with a planted negative.

run: musicctrl_quals.py at 70cd641d2 (PASS, FAILS 0), 2026-09-27.

The control also corrected FABLE's first draft: the page-boundary mismatch includes `maxFieldId` 0, not only the
positive multiples of 128. ASTRA's "max0 analogous" said so.

| consumer | what it said | state |
|---|---|---|
| `18-Audio/the-music-control-file-and-the-bgm-stream.md` §2.1 | "so the table is bound once per process and never rebound or freed: its lifetime is the process." | revised-here (struck; one writer is not one invocation; the binder has no guard; frequency and heap-5 release not established) |
| same §2.2 | "`003EAB90` (71 B) runs once, when the bytes are in:" | revised-here (struck; once per load, as the completion callback) |
| same §2.2 | "the header's page words are absolute 32-bit addresses" | revised-here (qualified: the visited pages only; the multiple-of-128 case, 0 included) |
| same §4 modding | "**The table loads once, at boot.** … nothing rebinds `02B5E0D0`." | revised-here (struck; loads on the boot path; re-run not established); modding line added for the page boundary |
| `18-Audio/how-the-music-changes-when-you-change-area.md` "The table" | the reader's paging | revised-here (boundary note, pointing to §2.2) |
| `18-Audio/CONTRACT-music-control-file-and-bgm-stream.md` MC-1 (OPUS) | "once per process" struck by OPUS | agrees |
| `18-Audio/CONTRACT-field-music-selection.md` MC-5 (OPUS) | the page-boundary qualification | agrees |
| `18-Audio/CONTRACT-field-music-selection.md` §11–12, the dead-actor wording (`ASTRA-RETURN-FABLE-FIELD-MUSIC-GATE-SCOPE`) | struck by OPUS | agrees. No FABLE page states a death-to-music link, so nothing to propagate here. |

**Not claimed:** a second binding in normal play, an invalid shipped table, or any fault. The shipped file has
`maxFieldId` 1311, 11 pages, and a highest index of 10.
