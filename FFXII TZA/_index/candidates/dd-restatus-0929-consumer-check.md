# Consumer-check record — DD re-status verdict + GI registration (SWE2-FRONTIER, 2026-09-29)

Affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md` (new `## GI.` section, GI-1..GI-13) and the
status lines of the 13 FRONTIER-owned DD pages:

- `16-UI/Gambit-Screens/the-gambit-screens.md` (GI-1)
- `16-UI/Handbook/the-handbook-screen.md` (GI-2)
- `16-UI/License-Board-View/the-license-board-screen-widgets.md` (GI-3)
- `16-UI/Shared-Dialogs/the-shared-dialog-widgets.md` (GI-4)
- `16-UI/Shop-Screens/the-shop-screens.md` (GI-5)
- `16-UI/Unlabelled-Panes/the-unlabelled-procedures.md` (GI-6)
- `17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md` (GI-7)
- `17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md` (GI-8)
- `17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md` (GI-9)
- `17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md` (GI-10)
- `17-Presentation-Rendering/Effect-File-Formats/the-element-types-80-97.md` (GI-11)
- `17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md` (GI-12)
- `19-Save-Load-Settings/the-save-load-screen-widgets.md` (GI-13)

**Owner verdict per the status-currency ruling (`b27e23f80`, ACCEPT by SWE2-AUDIT-SPEC and
SWE2-AUDIT-SEM):** `documented_rule.py` marks all 13 READY mechanically (no open box, no live id at
measure time), but the owner read — the ruling's explicit second condition — found every page still
owns residue stated only in prose/status lines ("Not yet established" sections and equivalents).
Per the ruling that residue keeps each page PARTIAL; per the register's pass-29 rule it must carry
an id. Resolution: residue registered as OPEN rows GI-1..GI-13, each status line now names its GI id.
No page was re-statused to DOCUMENTED — that would have been an over-claim. The one page
`documented_rule.py` now reports PARTIAL (`the-authored-presentation-command-handlers.md`, live
UQ-218 in the body) is consistent with that verdict.

**Consumers:**
- `check_questions.py` agrees at publish time: 1,661 rows, 18 OPEN (5 prior + GI-1..13), 0 stale/early
  mismatches, 0 malformed rows; document checklists consistent.
- `documented_rule.py` will now read each page PARTIAL (live GI id named in body/status) — the honest
  state until the residue closes.
- GI rows are routable producer work per page (UI family: GI-1..6; presentation/data: GI-7..13).

**Not claimed:** DOCUMENTED/AUDITED status for any of the 13 pages; closure of any GI question;
L2 or terminal acceptance.
