# DD owner read: eight Input, Audio and Save pages reconciled, residue registered as SD-1 to SD-42 (SWE2-DATA, 2026-09-30)

affected: 15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md, 15-Input/Input-Stack/input-stack-device-channel-and-bindings.md, 15-Input/Modal-Toggles/r2-force-fight-toggle.md, 18-Audio/sqex-sd-sound-driver-architecture.md, 18-Audio/which-variation-of-a-sound-you-hear.md, 18-Audio/Sound-Selection/sound-variant-selection.md, 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md, 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md, _index/OPEN-QUESTIONS.md

**What this is.** OPUS's owner read (`_index/candidates/dd-owner-read-0929/worksheet.tsv`) keeps these eight pages PARTIAL.
This package does the content work each worksheet row names:
- missing sections are written from verified facts;
- uncited claims are anchored, or struck with a dated correction;
- pending markers are resolved by pointers to existing answers, or registered as residue;
- stale prose is reconciled against the register and the code;
- disposition words are added where the rule asks.

**No status word is raised.** Every page keeps its leading word (PARTIAL; REOPENED on the capability page), and the
status lines now say an owner read is pending where they changed. New residue is registered as `SD-1`–`SD-9`,
`SD-20`–`SD-25` and `SD-40`–`SD-42` in the register's section SD. The prefix is checked free.

run: in_dd_checks.py, sv_callchain.py and au_slot38_39.py at 1f6569546, each FAILS 0 (the .out files beside them).

| script | what it checks |
|---|---|
| [`in_dd_checks.py`](in_dd_checks.py) ([out](in_dd_checks.out)) | the three Input pages: the new call-chain edges (raw call sites), the keymap validator branch, the play-clock pause reader of `020927C8`, event-slot names, aggregate bit 21's consumers (30 checks, positive and negative controls) |
| [`sv_callchain.py`](sv_callchain.py) ([out](sv_callchain.out)) | the version-stamps page's load and save chains, and the complete raw caller sets the page states (16 checks) |
| [`au_slot38_39.py`](au_slot38_39.py) ([out](au_slot38_39.out)) | `SD-23`: the virtual call sites through Sound-family slots 38 / 39 (control: slot 43's stepper call) |

## Per page

| page | rule before | rule after (with the SD rows) | registered | main reconciliations |
|---|---|---|---|---|
| capability-inhibition-policy | READY | PARTIAL (`SD-3`, `SD-4` live; REOPENED kept for the live ASTRA request) | `SD-3` aggregate bit 21, `SD-4` unit flag bit 24 | `01E0C2B8` is the u32 force-fight flag (C-5); events `0x2009` / `0x2031` named (`magic_ready`, `ability_ready`); bit 46 named; the "remain open" lines point to UQ-147 / UQ-148 (SUPERSEDED) |
| input-stack-device-channel-and-bindings | READY | PARTIAL (`SD-5`–`SD-9`) | one-shot bytes, recorded-input table, slot 15's caller, the title's dispatcher mode, `0035E7A0`'s deadline | new §3a Data structures and §3b Call chain; AP-4 / AP-5 / AP-6 / AP-8 / AP-9 and AU-2/3/4 no longer described as open; the keymap-defaults claim anchored |
| r2-force-fight-toggle | READY | PARTIAL (`SD-1`, `SD-2`) | what FLEEING changes for enemies; which `battle_4_c` element the label draws | FM-1 no longer described as open; "no falsification pass" struck (pass 1 ran 2026-09-03); `020927C8` answered: it pauses the play clock |
| sqex-sd-sound-driver-architecture | NEEDS-POINTER | PARTIAL (`SD-20`–`SD-22`) | the source voice's callback class, the unread mix path, the options rows for commands `0x13`–`0x15` | G-2 SUPERSEDED word; the empty Key addresses / Data structures / Call chain sections filled from §2a–2e; the "no body read" banner struck |
| which-variation-of-a-sound-you-hear | READY | PARTIAL (`SD-24` cited) | — | Key addresses, Data structures, Call chain, Modding notes, Evidence and Related sections added; two uncited claims anchored |
| sound-variant-selection | NEEDS-POINTER | PARTIAL (`SD-23`–`SD-25`) | slots 38 / 39, the record at `+0x30`, `rand()` threading | G-2 SUPERSEDED word; §1 player claims struck against §12's census (shipped data builds only the base Sound); §5 chain anchored |
| save-image-buffers-header-and-payload | NEEDS-POINTER | PARTIAL (`SD-40`) | readers of header dwords `0x12` / `0x13` | UQ-271 SUPERSEDED word, V-1 answered; the three "not read" key-address rows pointed at the pages that read them; FV-3 / V-12 / AB-5 staleness reconciled; what a caller does with a failed stamp answered |
| version-stamps-and-what-loading-normalises | NEEDS-POINTER | PARTIAL (`SD-41`, `SD-42`) | the digits' meaning, readers of header `+0x58` / `+0x60` | UQ-271 SUPERSEDED word; new §5b Call chain and §5c Modding notes; "rest of the block" pointed at the AUDITED block field map; "which flag it asks for" answered (V-5) |

"Rule" is `_index/candidates/status-currency-ruling-fable/documented_rule.py`. The measurements after the edits are taken
in the publish step, with the rows applied. The READY verdicts before only meant that no registered id was open; the
worksheet's unregistered "not read" residue is what the SD rows now carry.

## Consumer check (EVIDENCE-POLICY 4a)

| consumer | claim touched | state |
|---|---|---|
| the eight pages above | the struck and re-pointed sentences | revised-here |
| `_index/OPEN-QUESTIONS.md` section SD | the new rows | revised-here |
| `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` (no bit-46 row) | bit 46 = an action in execution (native-command-seam) | routed-to-FABLE (request with the exact row text) |
| the G-2 register row's 2026-09-18 narrowing ("the container the accessors read *is* the 64-byte `SabFile::Sequence`") | contradicts §12 / descriptor `01CB43E0` on which record sits at `this + 0x30` | routed-to-register owner as `SD-24` (unresolved; neither side is struck) |
| force-fight-mode.md, native-command-seam, CONTRACT-binding-profiles (AP-4), sound-trigger, how-a-sound-request-becomes-a-voice (UQ-250/251), rng-streams §8g, the config-screen page (DI-1), the battle-state block field map, the battle-runtime-mode contract | the facts the edits cite | agrees |

## Left over

- The input-stack page gives the channel-record parameter bytes relative to each builder's pointer in §5, while §10
  fixes the record base with the lookback count at `+0x08`. The two bases were not re-derived; §3a does not restate the
  bytes.
- `SD-24` is a real contradiction between sound-variant-selection §12 and the G-2 row's narrowing. The pages state both.
- `REOPENED` on the capability page is held by the live ASTRA request `FABLE-REQ-ASTRA-LEADER-STATS-NULL`, untouched.
