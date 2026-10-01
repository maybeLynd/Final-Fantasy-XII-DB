# Consumer-check record — pass-22 crossings for FABLE's pages, and one struck crossing sentence (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `Database/FFXII TZA/15-Input/how-a-gamepad-becomes-a-controller-object.md` (the corrected sentence)
affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` (section 11's crossing note, corrected in prose in the pass-22 section)
affected: `Database/FFXII TZA/07-Combat-Action/how-close-a-unit-must-stand-to-act.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/an-effect-element-frame-by-frame.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md`

Also written by this publish, and deliberately not on a declaration line: the disposition registry
`_index/candidates/neighbour-dispositions.tsv` (9 rows appended) and this record. The correction gate compares declared
paths with the publish's touched *.md* files only, so declaring the registry here would refuse a correct publish.

## What changed

1. **One struck sentence.** `how-a-gamepad-becomes-a-controller-object.md`'s crossing section said "None: every body
   named on this page is owned by the Input layer, and the call graph shows no edge from any of them into another
   layer." That became false on 2026-09-29, when OPUS's falsification pass (G4) named the shared kind leaf `00290180`:
   the script verb `is_ntsc` (handler `003423E0`) calls it. The sentence is struck verbatim, a dated
   "Corrected 2026-09-29 (FABLE)" note is added, and a `Script_VM_Native_Bridge — MECHANICAL` entry names the edge.
   The page's mechanism is unchanged.
2. **One prose correction, no strike.** The field map's section 11 crossing note calls `00236780` "the shared RNG/roll
   helper". Its body is `mov rax,[02EBF190]; mov eax,[rax+4]; shr eax,0xE; and eax,1; ret`, a flag-bit getter. The new
   `Save_Load_Settings — OUT-OF-SCOPE` entry states the correction. The section 11 sentence itself is left as it is (see
   the routed consumer below).
3. **Crossing entries** on the seven pages above, for 10 pass-22 pairs, and 9 registry rows (`GENUINELY-IRRELEVANT`,
   MECHANICAL readings) for the pairs whose only crossing is a shared leaf. No other sentence on any page is changed.

## Consumers

- consumer: `15-Input/README.md` index line for the gamepad page — agrees: it describes the enumeration and makes no crossing claim.
- consumer: `_index/candidates/gamepad-falsification-pass-1-0929/README.md` (OPUS, G4) — agrees: it is the source of the answer "all controller classes answer 2 (`00290180`)" that falsified the sentence.
- consumer: `_index/CONTRADICTIONS.tsv` rows CON-188 and CON-189 — agrees: they correct sections 3 and 7 and step 5, not the crossing sentence; no row carries the struck words.
- consumer: `20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md` and `00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md` — agrees: both link or name the gamepad page as a source and repeat no crossing claim.
- consumer: `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md`, `Save_Load_Settings` paragraph ("the EXP-suppression flag read `00236780`") — agrees with the corrected reading.
- consumer: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md` (`00236760` as the bank selector) — agrees.
- consumer: the field map's own section 11 crossing note ("`00236780` is the shared RNG/roll helper") — routed-to-FABLE-P22-FOLLOWUP: this publish states the correction in the pass-22 section; striking the section 11 words is a follow-up edit of that section.
- consumer: `17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md`, the `Gameplay - CLIENT` / `UI - CLIENT` paragraphs, which call `00203170` "the per-slot visitor" — routed-to-FABLE-P22-FOLLOWUP: the rig registry row reads `00203170` as the 44-byte identity-matrix store; the per-slot visitor is `003E3C30`. Not edited here.
- consumer: `_index/candidates/pass22-debt-0929/pass22-debt.tsv` — agrees: a dated sizing that `pass22_debt.py` regenerates from the next audit; not hand-edited.
- consumer: `_index/candidates/pass22-tripwires.tsv` — agrees: `audit_crossrefs.py` regenerates it; it gains the R6-held far ends these entries name.
- consumer: `06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md` and `13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md` — routed-to-OPUS: their five pairs' drafts are delivered as text (`for-opus.md`); not touched by this publish.

## Regression

- The edge rebuild reproduces all 24 FABLE findings exactly, count and 4-edge sample
  (`rebuild_edges.py`, output `rebuild_control.out`: "CONTROL: ALL 24 MATCH").
- `groups.py` assigns every edge of the 152-, 64- and 57-edge pairs to exactly one group ("GROUP CONTROL: PASS").
- Applied by `apply.py` to a `git archive` export of HEAD, then `audit_crossrefs.py` on that export before and after,
  compared by `compare_audit.py`. Result: the 19 in-scope FABLE pairs clear (10 by the new sections, 9 by registry
  rows); the 5 routed CONTRACT pairs stay open; there is no new finding.

run: apply.py, audit_crossrefs.py and compare_audit.py at d5a70a776 on a git archive export of that commit (FABLE drafts dir `C:/x/p22/drafts/tools/`)
