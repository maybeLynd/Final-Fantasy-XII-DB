# Affected-consumer check: OV-15 apply + MS-1..3 registration (SWE2-FRONTIER, 2026-09-29)

Applies board request `FABLE-REQ-FRONTIER-APPLY-OV15-AND-MS-ROWS`: FABLE's staged OV-15 answer
(`8764d1109`, `candidates/ov15-skip-mask-fable/`, `skip_mask.py` A C R W I FAILS 0) and the three
staged map-screens register rows from `status-currency-ruling-fable/worked-examples.md` (`7d92ce3ad`).

affected: `01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md`
(section 4 open-sentence replaced with the staged answer; OV-15 box ticked and pointed at the record);
`_index/OPEN-QUESTIONS.md` (row OV-15 -> ANSWERED 2026-09-29 (FABLE); new `## MS.` section, rows
MS-1..MS-3 OPEN, prefix checked free with `next_question_id.py --check MS`).

**Regression:** `check_questions.py --db <db>` at the apply working tree — rows 1648: ANSWERED 1439,
PARTIAL 2, OPEN 26, BLOCKED 0; checklist blocks 1461 ticked 1436; 0 unticked-answered, 0 ticked-open,
0 malformed-cell rows; "questions consistent".

| consumer | what it said | state |
|---|---|---|
| `ov15-skip-mask-fable/README.md` "For FRONTIER to apply" | replace the section-4 sentence, tick the box, mark OV-15 ANSWERED with the record as evidence | satisfied verbatim |
| the wait-poll claim in section 4 ("reads a byte selected by target actor+0x15 through `02099011 + index*0x288`") | is the skip mask, not the request's own byte | consistent — the staged text keeps the addressing sentence untouched |
| `status-currency-ruling-fable/worked-examples.md` | three OPEN static residues on the map-screens page keep it PARTIAL until registered | satisfied — MS-1..3 rows name the page and the narrowing that states each residue |
| `CONTRACT-native-command-lifecycle.md` 3 | the byte belongs to the target's manager record, not the request | unchanged and consistent |
| the world-tick page's writer table | one bit-level writer `0026A5B0`, one direct writer (the bind) | unchanged and consistent |

run: check_questions.py at this working tree, 2026-09-29, FAILS 0.
